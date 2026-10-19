"""Water pulled up, not pushed: cohesion-tension in the xylem  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = liquid water, the xylem water column
  YELLOW = the pull (tension, evaporation's drop in potential)
  TEAL   = dry air, water vapour
  GREEN  = a push (root pressure, the heart)
  ORANGE = the cost of gravity
  RED    = the question, what does not happen
  GREY   = outlines, axes, structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def box(w, h, color, x, y, op=0.2, sw=3):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=op).move_to([x, y, 0])


def lines(txt, size=24, color=GREY, **kw):
    return VGroup(*[T(s, size, color, **kw) for s in txt.split("\n")]).arrange(DOWN, buff=0.08)


class S00Title(TitleCard):
    LESSON = "Moving water and sugar in plants"
    TITLE = "Water Pulled Up, Not Pushed"


# ---------------------------------------------------------------------------------------------
class S01Tree(SpokenScene):
    def construct(self):
        soil = box(6.0, 0.8, GREY, -2.2, -3.0, op=0.25)
        soil_l = T("roots in the soil", 26, GREY).move_to(soil)
        trunk = Rectangle(width=1.0, height=4.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([-2.2, -0.3, 0])
        crown = box(4.2, 1.1, GREEN if False else BLUE, -2.2, 2.55, op=0.12)
        crown.set_stroke(GREY)
        crown_l = T("leaves", 28, GREY).move_to(crown)
        self.at("coast redwoods")
        self.play(FadeIn(soil), FadeIn(soil_l), run_time=0.5)
        self.play(GrowFromEdge(trunk, DOWN), run_time=1.0)
        self.play(FadeIn(crown), FadeIn(crown_l), run_time=0.5)
        sc = DoubleArrow([-0.4, -2.6, 0], [-0.4, 2.55, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
        sc_l = lines("more than\n100 m", 28, TEXT).move_to([1.2, 0.0, 0])
        self.at("more than 100 meters")
        self.play(GrowFromCenter(sc), FadeIn(sc_l), run_time=0.8)
        wat = arr([-2.2, -2.4, 0], [-2.2, 1.8, 0], BLUE, w=6)
        wl = T("water", 26, BLUE).next_to(trunk, LEFT, buff=0.25).shift(DOWN * 0.3)
        self.at("Every leaf at the top")
        self.play(Indicate(crown, color=BLUE, scale_factor=1.05), run_time=0.8)
        self.at("from roots in the soil")
        self.play(GrowArrow(wat), FadeIn(wl), run_time=1.4)
        nh = chip("no heart, no pump", RED, 30).move_to([3.6, -1.3, 0])
        self.at("no heart and no pump")
        self.play(FadeIn(nh, shift=UP * 0.1), run_time=0.7)
        q = chip("?", RED, 48, pad=0.3).move_to([-2.2, 0.0, 0])
        ql = lines("what lifts\nthe water?", 32, RED).move_to([3.6, 0.5, 0])
        self.at("what lifts the water")
        self.play(FadeIn(q, scale=0.8), FadeIn(ql), run_time=0.8)
        self.play(Indicate(q, color=RED, scale_factor=1.15), run_time=0.7)
        air = chip("dry air", TEAL, 32).move_to([3.6, 2.55, 0])
        aa = arr([1.9, 2.55, 0], [0.2 + 0.0, 2.55, 0], TEAL)
        self.at("dry air around the leaves")
        self.play(FadeIn(air, shift=LEFT * 0.2), GrowArrow(aa), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Ladder(SpokenScene):
    def construct(self):
        head = T("water potential, in MPa (illustrative values, not to scale)", 28, GREY).to_edge(UP, buff=0.4)
        zero = DashedLine([-6.0, 2.6, 0], [6.0, 2.6, 0], color=BLUE, stroke_width=3)
        zero_l = T("pure water at atmospheric pressure: 0", 24, BLUE).next_to(zero, UP, buff=0.1).align_to(zero, LEFT)
        self.at("Water potential predicts")
        self.play(FadeIn(head), run_time=0.6)
        self.at("Pure water")
        self.play(Create(zero), FadeIn(zero_l), run_time=0.8)
        ys = [1.4, 0.45, -0.5, -2.5]
        xs = [-4.6, -1.5, 1.6, 4.7]
        names = ["soil", "root", "leaf", "air, 50% RH, 20 °C"]
        vals = ["-0.3", "-0.6", "-1.5", "-94 MPa"]
        cols = [GREY, GREY, GREY, TEAL]
        parts = []
        for x, y, n, v, c in zip(xs, ys, names, vals, cols):
            b = box(2.7 if c != TEAL else 3.2, 1.15, c, x - (0 if c != TEAL else 0.3), y, op=0.18)
            nm = T(n, 26 if c != TEAL else 22, c if c != GREY else TEXT).move_to([x - (0 if c != TEAL else 0.3), y + 0.2, 0])
            vl = M(v, 28, YELLOW).move_to([x - (0 if c != TEAL else 0.3), y - 0.2, 0])
            parts.append((b, nm, vl))
        arrs = []
        for i in range(3):
            arrs.append(arr([xs[i] + 1.35, ys[i], 0], [xs[i + 1] - (1.35 if i < 2 else 1.65), ys[i + 1], 0], BLUE, w=6 if i < 2 else 9))
        down = T("water moves toward lower potential", 26, BLUE).move_to([0, 2.05, 0])
        self.at("lower total water potential")
        self.play(FadeIn(down), *[FadeIn(p[0]) for p in parts], *[FadeIn(p[1]) for p in parts], run_time=1.0)
        self.at("illustrative values")
        self.wait(0.1)
        self.at("Soil is")
        self.play(FadeIn(parts[0][2]), Indicate(parts[0][0], color=YELLOW, scale_factor=1.06), run_time=0.6)
        self.at("Root is")
        self.play(FadeIn(parts[1][2]), Indicate(parts[1][0], color=YELLOW, scale_factor=1.06), run_time=0.6)
        self.at("Leaf is")
        self.play(FadeIn(parts[2][2]), Indicate(parts[2][0], color=YELLOW, scale_factor=1.06), run_time=0.6)
        self.at("Air at 50")
        self.play(FadeIn(parts[3][2]), Indicate(parts[3][0], color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.at("about minus 94")
        self.play(Indicate(parts[3][2], color=YELLOW, scale_factor=1.25), run_time=0.8)
        self.at("Every step")
        dot = Dot([xs[0], ys[0] + 0.75, 0], radius=0.14, color=BLUE)
        self.play(FadeOut(down), FadeIn(dot), run_time=0.3)
        for i in range(3):
            self.play(GrowArrow(arrs[i]), dot.animate.move_to([xs[i + 1], ys[i + 1] + 0.75, 0]), run_time=0.8)
        self.at("biggest drop")
        bd = T("biggest drop: leaf to air", 28, YELLOW).move_to([-0.8, -2.3, 0])
        self.play(FadeIn(bd, shift=UP * 0.1), Indicate(arrs[2], color=YELLOW, scale_factor=1.05), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Pull(SpokenScene):
    def construct(self):
        air = box(9.0, 0.6, TEAL, 0, 3.05, op=0.15)
        air_l = T("dry air", 24, TEAL).move_to(air)
        leaf = box(9.0, 1.6, GREY, 0, 1.5, op=0.1)
        leaf_l = T("leaf", 24, GREY).move_to([-4.0, 2.05, 0])
        cell = box(3.2, 1.1, GREY, 1.8, 1.4, op=0.2)
        cell_l = lines("inner photosynthetic\ncell", 22, TEXT).move_to(cell).shift(DOWN * 0.1)
        wall = Line(cell.get_corner(UL) + RIGHT * 0.15, cell.get_corner(UR) + LEFT * 0.15, color=BLUE, stroke_width=9)
        wall_l = T("wet wall", 24, BLUE).move_to([-0.1, 2.0, 0]).align_to(cell, LEFT).shift(LEFT * 1.35)
        soil = box(9.0, 0.7, GREY, 0, -3.1, op=0.25)
        soil_l = T("roots in the soil", 24, GREY).move_to(soil)
        tube = Rectangle(width=0.8, height=4.45, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([-2.6, -0.575, 0])
        tube_l = lines("xylem:\ndead, hollow\ncells", 24, GREY).move_to([-5.0, -0.7, 0])
        self.at("Inside a leaf")
        self.play(FadeIn(air), FadeIn(air_l), FadeIn(leaf), FadeIn(leaf_l), FadeIn(cell), FadeIn(cell_l), FadeIn(soil), FadeIn(soil_l), run_time=0.9)
        self.play(Create(wall), FadeIn(wall_l), run_time=0.6)
        vap = VGroup(*[arr([x, 2.2, 0], [x, 2.7, 0], TEAL, w=4, tip=0.15) for x in (1.0, 1.8, 2.6)])
        self.at("evaporates")
        self.play(LaggedStart(*[GrowArrow(a) for a in vap], lag_ratio=0.25), run_time=1.0)
        press = T("held tighter, pressure falls", 24, YELLOW).move_to([3.0, 0.4, 0])
        self.at("The water left in the walls")
        self.play(Indicate(wall, color=YELLOW, scale_factor=1.05), run_time=0.9)
        self.at("its pressure falls")
        self.play(FadeIn(press, shift=UP * 0.1), run_time=0.9)
        self.at("Water moves in from the xylem")
        self.play(Create(tube), FadeIn(tube_l), run_time=0.8)
        inn = arr([-2.1, 1.2, 0], [0.1, 1.2, 0], BLUE, w=6)
        self.play(GrowArrow(inn), run_time=0.6)
        self.at("dead and hollow")
        self.play(Indicate(tube_l, color=TEXT, scale_factor=1.05), run_time=0.7)
        col = Rectangle(width=0.5, height=4.25, stroke_width=0, fill_color=BLUE, fill_opacity=0.55).move_to([-2.6, -0.575, 0])
        self.at("continuous pathway")
        self.play(GrowFromEdge(col, DOWN), run_time=1.3)
        coh = chip("cohesion: water molecules attract", BLUE, 24).move_to([2.4, -0.9, 0])
        self.at("Cohesion")
        self.play(FadeIn(coh, shift=UP * 0.1), run_time=0.7)
        pull = arr([-1.75, -2.2, 0], [-1.75, 0.6, 0], YELLOW, w=9)
        pl = T("pulled like a rope", 28, YELLOW).move_to([2.4, -2.0, 0])
        self.at("a thin column")
        self.play(GrowArrow(pull), run_time=1.2)
        self.at("like a rope")
        self.play(FadeIn(pl), Indicate(pull, color=YELLOW, scale_factor=1.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Gravity(SpokenScene):
    def construct(self):
        x0, y0 = -5.6, -2.3
        W, H = 10.2, 4.8     # plot area: 0..120 m, 0..1.4 MPa
        sx, sy = W / 120.0, H / 1.4
        xa = Line([x0, y0, 0], [x0 + W, y0, 0], color=GREY, stroke_width=3)
        ya = Line([x0, y0, 0], [x0, y0 + H, 0], color=GREY, stroke_width=3)
        ticks = VGroup()
        for h in (0, 30, 60, 90, 120):
            t = Line([x0 + h * sx, y0, 0], [x0 + h * sx, y0 - 0.1, 0], color=GREY)
            ticks.add(t, M(str(h), 22, GREY).move_to([x0 + h * sx, y0 - 0.38, 0]))
        for v in (0, 0.5, 1.0):
            t = Line([x0, y0 + v * sy, 0], [x0 - 0.1, y0 + v * sy, 0], color=GREY)
            ticks.add(t, M(f"{v:.1f}", 22, GREY).move_to([x0 - 0.55, y0 + v * sy, 0]))
        xl = T("height of the leaf above the roots (m)", 24, GREY).move_to([x0 + W / 2, y0 - 0.85, 0])
        yl = lines("extra tension\n(MPa)", 22, GREY).move_to([x0 - 0.1, y0 + H + 0.45, 0])
        title = T("gravity alone, holding a still column: no flow", 26, ORANGE).move_to([0.4, 3.15, 0])
        self.at("Gravity sets a floor")
        self.play(Create(xa), Create(ya), FadeIn(ticks), FadeIn(xl), FadeIn(yl), run_time=1.2)
        self.play(FadeIn(title), run_time=0.5)
        self.at("each meter of height")
        line = Line([x0, y0, 0], [x0 + 110 * sx, y0 + 1.1 * sy, 0], color=ORANGE, stroke_width=6)
        sl = T("about 0.01 MPa per metre", 28, ORANGE).move_to([1.4, -0.95, 0])
        self.play(Create(line), run_time=1.4)
        self.play(FadeIn(sl), run_time=0.5)
        p30 = Dot([x0 + 30 * sx, y0 + 0.3 * sy, 0], radius=0.12, color=YELLOW)
        g30 = DashedLine([x0 + 30 * sx, y0, 0], p30.get_center(), color=YELLOW, stroke_width=3)
        h30 = DashedLine(p30.get_center(), [x0, y0 + 0.3 * sy, 0], color=YELLOW, stroke_width=3)
        l30 = T("30 m: 0.30 MPa", 26, YELLOW).move_to([x0 + 30 * sx + 1.4, y0 + 0.3 * sy - 0.5, 0])
        self.at("A leaf 30")
        self.play(Create(g30), Create(h30), FadeIn(p30), run_time=1.0)
        self.at("extra tension")
        self.play(FadeIn(l30), Indicate(p30, color=YELLOW, scale_factor=1.6), run_time=0.9)
        p110 = Dot([x0 + 110 * sx, y0 + 1.1 * sy, 0], radius=0.12, color=RED)
        l110 = lines("110 m redwood:\nover 1 MPa", 26, RED).move_to([x0 + 110 * sx + 0.1, y0 + 1.1 * sy + 0.85, 0])
        self.at("At the top")
        self.play(FadeIn(p110, scale=0.5), FadeIn(l110), run_time=0.9)
        self.at("gravity alone adds")
        self.play(Indicate(p110, color=RED, scale_factor=1.6), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Roots(SpokenScene):
    def construct(self):
        top = -2.8
        soil = box(11.0, 0.7, GREY, 0, top - 0.35, op=0.25)
        soil_l = T("roots in the soil", 24, GREY).move_to(soil)
        push = arr([-3.5, -2.6, 0], [-3.5, -0.9, 0], GREEN, w=9)
        pq = chip("root pressure: a push?", GREEN, 28).move_to([-3.5, 3.0, 0])
        self.at("Could the roots push")
        self.play(FadeIn(soil), FadeIn(soil_l), GrowArrow(push), FadeIn(pq), run_time=1.0)
        b1 = Rectangle(width=1.5, height=0.75, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.4)
        b1.move_to([-3.5, top + 0.375, 0])
        l1 = lines("about 15 m,\nin principle", 24, GREEN).next_to(b1, UP, buff=0.12)
        l1b = lines("0.15 MPa: highest value in a\nsurvey of 109 tropical vines\nand woody species", 22, GREEN).next_to(l1, UP, buff=0.15)
        self.at("Where measured")
        self.play(FadeOut(push), run_time=0.4)
        self.play(GrowFromEdge(b1, DOWN), run_time=0.8)
        self.at("highest value")
        self.play(FadeIn(l1b), run_time=0.7)
        self.at("That is enough")
        self.play(FadeIn(l1), Indicate(b1, color=GREEN, scale_factor=1.1), run_time=0.8)
        b2 = Rectangle(width=1.5, height=5.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15)
        b2.move_to([0.6, top + 2.5, 0])
        l2 = lines("tallest coast redwoods:\nmore than 100 m", 24, TEXT).next_to(b2, RIGHT, buff=0.3).shift(UP * 1.0)
        nt = T("not to scale", 22, GREY).move_to([3.9, -2.2, 0])
        self.at("weak or absent")
        self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), FadeIn(nt), run_time=1.0)
        weak = lines("weak or absent when\ntranspiration is fastest", 24, RED).move_to([3.9, -0.5, 0])
        self.play(FadeIn(weak), b1.animate.set_fill(opacity=0.12), run_time=0.8)
        self.wait(0.3)
        self.at("Cut the xylem")
        left = VGroup(soil, soil_l, pq, b1, l1, l1b, b2, l2, nt, weak)
        self.play(FadeOut(left), run_time=0.7)
        tube = Rectangle(width=1.0, height=4.6, stroke_color=GREY, stroke_width=3, fill_color=BLUE, fill_opacity=0.35).move_to([0, -1.0, 0])
        tl = lines("xylem of a\ntranspiring tree", 26, GREY).move_to([-3.0, -1.0, 0])
        ten = T("under tension", 26, YELLOW).move_to([-3.0, -2.3, 0])
        cutl = DashedLine([-0.9, 1.3, 0], [0.9, 1.3, 0], color=TEXT, stroke_width=3)
        cut = T("cut", 26, TEXT).move_to([-1.7, 1.3, 0])
        self.play(FadeIn(tube), FadeIn(tl), FadeIn(ten), run_time=0.8)
        self.play(Create(cutl), FadeIn(cut), run_time=0.5)
        air = arr([0, 2.9, 0], [0, 1.45, 0], TEAL, w=8)
        airl = T("air drawn in", 28, TEAL).move_to([-2.4, 2.5, 0])
        self.at("air is drawn in")
        self.play(GrowArrow(air), FadeIn(airl), run_time=0.9)
        self.at("Sap does not spurt out")
        sp = arr([2.0, 1.3, 0], [2.0, 2.7, 0], RED, w=7)
        x1 = Line([1.7, 1.75, 0], [2.3, 2.25, 0], color=RED, stroke_width=7)
        x2 = Line([1.7, 2.25, 0], [2.3, 1.75, 0], color=RED, stroke_width=7)
        spl = lines("sap does not\nspurt out", 28, RED).move_to([4.2, 2.0, 0])
        self.play(GrowArrow(sp), run_time=0.4)
        self.play(Create(x1), Create(x2), FadeIn(spl), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        ay = -1.3
        axis = Line([-6.0, ay, 0], [6.0, ay, 0], color=GREY, stroke_width=3)
        z = Line([0, ay - 0.15, 0], [0, ay + 0.15, 0], color=GREY, stroke_width=3)
        zl = T("0, atmospheric", 22, GREY).move_to([0, ay - 0.45, 0])
        neg = T("negative: a pull", 24, YELLOW).move_to([-3.9, ay - 0.45, 0])
        pos = T("positive: a push", 24, GREEN).move_to([3.9, ay - 0.45, 0])
        axl = T("pressure (MPa), not to scale", 22, GREY).move_to([0, ay - 0.95, 0])
        self.at("vertebrate heart")
        heart = chip("vertebrate heart", GREEN, 30).move_to([3.4, 2.7, 0])
        push = arr([3.4, 2.2, 0], [3.4, 0.9, 0], GREEN, w=9)
        self.play(FadeIn(heart), run_time=0.6)
        self.at("closed loop")
        loop = lines("blood round a\nclosed loop", 24, GREEN).move_to([5.1, 1.5, 0])
        self.play(GrowArrow(push), FadeIn(loop), run_time=0.8)
        self.play(Create(axis), Create(z), FadeIn(zl), FadeIn(pos), FadeIn(neg), FadeIn(axl), run_time=0.8)
        self.at("peak arterial pressure")
        m = Dot([0.9, ay, 0], radius=0.13, color=GREEN)
        mm = Dot([0.9, ay, 0], radius=0.13, color=GREEN)
        ml = lines("about +0.016 MPa, peak arterial\npressure, resting adult human", 22, GREEN).move_to([3.0, 0.0, 0])
        ml_c = DashedLine([0.9, ay + 0.1, 0], [1.6, -0.45, 0], color=GREEN, stroke_width=2)
        self.play(FadeIn(m, scale=0.5), FadeIn(ml_c), run_time=0.7)
        self.at("resting adult human")
        self.play(FadeIn(ml), run_time=0.7)
        self.at("megapascals")
        self.play(Indicate(m, color=GREEN, scale_factor=1.8), run_time=0.8)
        self.at("transpiring plant")
        tube = Rectangle(width=0.7, height=2.9, stroke_color=GREY, stroke_width=3, fill_color=BLUE, fill_opacity=0.35).move_to([-3.6, 1.45, 0])
        top = T("leaf", 24, GREY).move_to([-4.6, 2.6, 0])
        bot = T("root", 24, GREY).move_to([-4.6, 0.3, 0])
        xl = lines("xylem,\ntranspiring plant:\none way, root to leaf", 24, TEXT).move_to([-1.1, 1.75, 0])
        self.play(FadeIn(tube), FadeIn(top), FadeIn(bot), run_time=0.7)
        self.at("negative pressure")
        pl = arr([-3.6, 0.3, 0], [-3.6, 2.6, 0], YELLOW, w=9)
        m2 = Dot([-2.4, ay, 0], radius=0.13, color=YELLOW)
        mc = DashedLine([-2.4, ay + 0.1, 0], [-3.4, -0.05, 0], color=YELLOW, stroke_width=2)
        self.play(GrowArrow(pl), FadeIn(m2, scale=0.5), FadeIn(mc), FadeIn(xl), run_time=1.0)
        self.at("Evaporation powers it")
        ev = T("powered by evaporation", 26, YELLOW).move_to([-0.9, 0.75, 0])
        self.play(FadeIn(ev, shift=DOWN * 0.1), run_time=0.7)
        rule = chip("Xylem water is pulled, not pushed", GOLD, 34).move_to([0, -3.1, 0])
        self.at("pulled, not pushed")
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Xylem water is pulled by evaporation, not pushed."
