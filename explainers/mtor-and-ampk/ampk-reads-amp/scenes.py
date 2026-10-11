"""Why AMPK reads AMP, not ATP  (Biochemistrypedia section film, lesson: mTOR and AMPK)

COLOR MAP (one color per concept, whole film)
  BLUE   = ATP
  TEAL   = ADP
  YELLOW = AMP (the thing that moves most)
  PURPLE = AMPK and its subunits
  ORANGE = LKB1, the upstream kinase
  GOLD   = a phosphate group (the "P" badge)
  GREEN  = easier / on
  RED    = poor, harder, crossed out
  GREY   = axes, structure, de-emphasised
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
ATPc, ADPc, AMPc = BLUE, TEAL, YELLOW

K = 0.5  # the lesson's round number


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pbadge(size=0.24):
    c = Circle(radius=size, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 24, BG, weight=BOLD).move_to(c))


class S00Title(TitleCard):
    LESSON = "mTOR and AMPK"
    TITLE = "Why AMPK Reads AMP, Not ATP"


# ---------------------------------------------------------------------------------------------
class S01Alarm(SpokenScene):
    def construct(self):
        head = T("Is there enough ATP?", 38, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.at("Is there enough")
        self.play(Write(head), run_time=1.0)

        # a flat ATP trace (idealised)
        x0, x1, y0 = -5.9, -0.9, -0.3
        axis = Line([x0, y0 - 1.3, 0], [x1, y0 - 1.3, 0], color=GREY, stroke_width=3)
        yax = Line([x0, y0 - 1.3, 0], [x0, y0 + 1.7, 0], color=GREY, stroke_width=3)
        tl = T("time", 24, GREY).next_to(axis, DOWN, buff=0.15).align_to(axis, RIGHT)
        yl = T("ATP", 28, ATPc, weight=BOLD).next_to(yax, UP, buff=0.15).align_to(yax, LEFT)
        xs = np.linspace(x0 + 0.05, x1, 120)
        wob = 0.03 * np.sin(xs * 7)
        trace = VMobject(color=ATPc, stroke_width=6).set_points_smoothly([[x, y0 + 0.5 + w, 0] for x, w in zip(xs, wob)])
        note = T("nearly constant (idealised)", 24, ATPc).next_to(trace, UP, buff=0.35)
        self.at("healthy cell")
        self.play(Create(axis), Create(yax), FadeIn(tl), FadeIn(yl), run_time=0.8)
        self.play(Create(trace), run_time=1.2)
        self.play(FadeIn(note), run_time=0.5)

        # ATP is a poor alarm
        bell = bchip("alarm", RED, size=28)
        bell.move_to([-3.4, -2.7, 0])
        cross = VGroup(Line(bell.get_corner(UL), bell.get_corner(DR), color=RED, stroke_width=4),
                       Line(bell.get_corner(DL), bell.get_corner(UR), color=RED, stroke_width=4))
        poor = T("a poor alarm", 28, RED).next_to(bell, RIGHT, buff=0.3)
        self.at("poor alarm")
        self.play(FadeIn(bell, shift=UP * 0.1), run_time=0.4)
        self.play(Create(cross), FadeIn(poor), run_time=0.6)

        # AMPK answers by reading AMP
        ampk = bchip("AMPK", PURPLE, size=36).move_to([3.7, -1.2, 0])
        amp = bchip("AMP", AMPc, size=36).move_to([3.7, 1.5, 0])
        a = arr(amp.get_bottom(), ampk.get_top(), AMPc, 6)
        reads = T("reads", 28, AMPc).next_to(a, RIGHT, buff=0.25)
        self.at("The kinase")
        self.play(FadeIn(ampk, scale=0.9), run_time=0.6)
        self.at("reads")
        self.play(FadeIn(amp, shift=DOWN * 0.15), GrowArrow(a), FadeIn(reads), run_time=0.8)
        self.play(Indicate(VGroup(*amp[1:]), color=AMPc, scale_factor=1.15), run_time=0.8)
        self.at("instead")
        self.play(FadeOut(VGroup(bell, cross, poor, note, trace, axis, yax, tl, yl)), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Square(SpokenScene):
    def construct(self):
        y = 2.3
        d1 = bchip("ADP", ADPc, size=34).move_to([-4.4, y, 0])
        d2 = bchip("ADP", ADPc, size=34).move_to([-2.7, y, 0])
        plus_l = T("+", 34, GREY).move_to([(-4.4 - 2.7) / 2, y, 0])
        at = bchip("ATP", ATPc, size=34).move_to([2.3, y, 0])
        am = bchip("AMP", AMPc, size=34).move_to([4.3, y, 0])
        plus_r = T("+", 34, GREY).move_to([3.3, y, 0])
        fwd = arr([-1.4, y + 0.18, 0], [1.1, y + 0.18, 0], GREY, 5)
        bwd = arr([1.1, y - 0.18, 0], [-1.4, y - 0.18, 0], GREY, 5)
        enz = T("adenylate kinase", 26, GREY).move_to([-0.15, y + 0.75, 0])

        self.at("Adenylate kinase")
        self.play(FadeIn(enz), run_time=0.6)
        self.at("near equilibrium")
        self.play(GrowArrow(fwd), GrowArrow(bwd), run_time=0.6)

        eq1 = M("[AMP] = K × [ADP]² / [ATP]", 34).move_to([0, 0.5, 0])
        self.at("Two")
        self.play(FadeIn(VGroup(d1, d2, plus_l)), run_time=0.4)
        self.play(FadeIn(VGroup(at, plus_r, am)), run_time=0.4)
        self.play(Write(eq1), run_time=1.2)

        left = M("[AMP] / [ATP] = K × ( [ADP] / [ATP] )", 32)
        sq = M("2", 34, AMPc, weight=BOLD)
        eq2 = VGroup(left, sq).arrange(RIGHT, buff=0.04, aligned_edge=UP).move_to([0, -1.1, 0])
        sq.shift(UP * 0.12)
        self.at("Divide by")
        self.play(eq1.animate.set_opacity(0.45), run_time=0.3)
        self.play(Write(eq2), run_time=1.0)
        self.at("goes as")
        self.play(Indicate(left, color=GOLD, scale_factor=1.04), run_time=0.6)

        lab = T("AMP : ATP goes as (ADP : ATP) squared", 30, AMPc).move_to([0, -2.6, 0])
        self.at("the square")
        self.play(FadeIn(lab), Indicate(sq, color=AMPc, scale_factor=1.8), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Numbers(SpokenScene):
    def construct(self):
        # numbers computed from the lesson's equation  [AMP] = K [ADP]^2 / [ATP]
        atp0, adp0 = 5.0, 0.5
        amp0 = K * adp0 ** 2 / atp0               # 0.025
        atp1, adp1 = 4.5, 0.93                    # the lesson's values after work uses a tenth of the ATP
        amp1 = K * adp1 ** 2 / atp1               # 0.096
        rest = {"ATP": (atp0, ATPc), "ADP": (adp0, ADPc), "AMP": (amp0, AMPc)}
        after = {"ATP": atp1, "ADP": adp1, "AMP": amp1}

        base_y, per = -2.3, 4.4 / 400.0           # 400 percent of resting value = 4.4 units
        xs = {"ATP": -4.3, "ADP": -2.2, "AMP": -0.1}
        w = 0.8

        axx = Line([-5.7, base_y, 0], [1.2, base_y, 0], color=GREY, stroke_width=3)
        axy = Line([-5.7, base_y, 0], [-5.7, base_y + 400 * per + 0.1, 0], color=GREY, stroke_width=3)
        ticks = VGroup()
        for v in (0, 100, 200, 300, 400):
            ticks.add(M(str(v), 22, GREY).next_to([-5.7, base_y + v * per, 0], LEFT, buff=0.12))
        ylab = T("percent of resting value", 22, GREY).rotate(PI / 2).next_to(ticks, LEFT, buff=0.15)
        ylab.align_to(axy, DOWN)
        legend = T("values in mM, K = 0.5 (round numbers)", 22, GREY).move_to([-2.2, 3.4, 0])
        key1 = VGroup(Square(0.22, stroke_color=TEXT, stroke_width=2, fill_opacity=0.0),
                      T("at rest", 22, GREY)).arrange(RIGHT, buff=0.12)
        key2 = VGroup(Square(0.22, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.85),
                      T("after work uses a tenth of the ATP", 22, GREY)).arrange(RIGHT, buff=0.12)
        keys = VGroup(key1, key2).arrange(RIGHT, buff=0.5).move_to([-2.2, 2.9, 0])

        self.play(Create(axx), Create(axy), FadeIn(ticks), FadeIn(ylab), FadeIn(legend), run_time=0.3)

        names = {}
        for k, (v, c) in rest.items():
            names[k] = T(k, 28, c, weight=BOLD).move_to([xs[k], base_y - 0.4, 0])
        rbars, rvals = {}, {}
        for k, (v, c) in rest.items():
            h = 100 * per
            b = Rectangle(width=w, height=h, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.18)
            b.move_to([xs[k] - 0.45, base_y + h / 2, 0])
            rbars[k] = b
            rvals[k] = M({"ATP": "5.0", "ADP": "0.5", "AMP": "0.025"}[k], 22, c).next_to(b, UP, buff=0.1)
        self.at("At rest")
        self.play(FadeIn(keys[0]), FadeIn(VGroup(*names.values())), run_time=0.5)
        for k in ("ATP", "ADP", "AMP"):
            self.play(GrowFromEdge(rbars[k], DOWN), FadeIn(rvals[k]), run_time=0.5)

        abars, avals = {}, {}
        for k, (v, c) in rest.items():
            pct = after[k] / v * 100
            h = pct * per
            b = Rectangle(width=w, height=h, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.85)
            b.move_to([xs[k] + 0.45, base_y + h / 2, 0])
            abars[k] = b
            txt = f"{after[k]:.3g}"
            if k == "AMP":
                txt = f"{amp1:.3f}"
            avals[k] = M(txt, 22, c).next_to(b, UP, buff=0.1)
        self.at("Let work")
        self.play(FadeIn(keys[1]), run_time=0.5)
        self.at("falls to")
        self.play(GrowFromEdge(abars["ATP"], DOWN), FadeIn(avals["ATP"]), run_time=0.6)
        self.at("settles near")
        self.play(GrowFromEdge(abars["ADP"], DOWN), FadeIn(avals["ADP"]), run_time=0.6)
        self.at("becomes")
        self.play(GrowFromEdge(abars["AMP"], DOWN), FadeIn(avals["AMP"]), run_time=0.8)

        fell = T("down 10%", 26, ATPc, weight=BOLD).move_to([xs["ATP"] + 0.45, base_y + 2.35, 0])
        rose = T("almost 4×", 28, AMPc, weight=BOLD).move_to([xs["AMP"] - 1.7, base_y + 3.4, 0])
        self.at("fell")
        self.play(FadeIn(fell, shift=DOWN * 0.1), run_time=0.5)
        self.at("rose almost")
        self.play(FadeIn(rose, shift=DOWN * 0.1), Indicate(abars["AMP"], color=AMPc, scale_factor=1.04), run_time=0.8)

        # fuel gauge + lamp, schematic
        c0 = np.array([4.5, 0.6, 0])
        arc = Arc(radius=1.3, start_angle=0, angle=PI, arc_center=c0, color=GREY, stroke_width=5)
        e_l = T("E", 22, GREY).move_to(c0 + LEFT * 1.3 + DOWN * 0.3)
        f_l = T("F", 22, GREY).move_to(c0 + RIGHT * 1.3 + DOWN * 0.3)
        g_t = T("ATP", 28, ATPc, weight=BOLD).move_to(c0 + UP * 1.9)
        f0 = 0.9
        ang = PI * (1 - f0)
        needle = Line(c0, c0 + 1.15 * np.array([np.cos(ang), np.sin(ang), 0]), color=ATPc, stroke_width=7)
        hub = Dot(c0, radius=0.09, color=ATPc)
        lamp = Circle(radius=0.45, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.15).move_to([4.5, -1.5, 0])
        lamp_t = T("AMP", 26, AMPc, weight=BOLD).next_to(lamp, DOWN, buff=0.4)
        sch = T("schematic", 22, GREY).move_to([4.5, -3.2, 0])
        self.at("needle has barely")
        self.play(FadeIn(VGroup(arc, e_l, f_l, g_t, needle, hub, lamp, lamp_t, sch)), run_time=0.6)
        self.play(Rotate(needle, angle=PI * 0.09, about_point=c0), run_time=0.8)
        self.at("light is on")
        glow = Circle(radius=0.62, stroke_width=0, fill_color=AMPc, fill_opacity=0.25).move_to(lamp)
        self.play(lamp.animate.set_stroke(AMPc).set_fill(AMPc, 0.95), FadeIn(glow), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Gamma(SpokenScene):
    def construct(self):
        cy = -0.1
        BW, BH = 3.4, 3.0
        def sub(sym, word, x, sy=0.2, wy=-0.55):
            r = RoundedRectangle(corner_radius=0.3, width=BW, height=BH, stroke_color=PURPLE, stroke_width=4,
                                 fill_color=PURPLE, fill_opacity=0.2).move_to([x, cy, 0])
            s_ = T(sym, 56, PURPLE, weight=BOLD).move_to([x, cy + sy, 0])
            wd = T(word, 28, PURPLE).move_to([x, cy + wy, 0])
            return VGroup(r, s_, wd)
        al = sub("α", "kinase", -4.0, 0.35, -0.2)
        be = sub("β", "holds the\ncomplex together", 0.0, 0.5, -0.35)
        be[2].scale(0.88)
        ga = sub("γ", "sensor", 4.0, 0.15, -0.6)
        link1 = Line(al[0].get_right(), be[0].get_left(), color=PURPLE, stroke_width=5)
        link2 = Line(be[0].get_right(), ga[0].get_left(), color=PURPLE, stroke_width=5)
        title = T("AMPK", 36, PURPLE, weight=BOLD).move_to([0, 3.1, 0])

        self.at("In")
        self.play(FadeIn(title), run_time=0.5)
        self.at("alpha carries")
        self.play(FadeIn(al, scale=0.9), run_time=0.6)
        self.at("beta holds")
        self.play(FadeIn(be, scale=0.9), Create(link1), run_time=0.6)
        self.at("gamma carries")
        self.play(FadeIn(ga, scale=0.9), Create(link2), run_time=0.6)

        # three binding sites on gamma; the three nucleotides compete for them
        slots = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.98, height=0.5, stroke_color=GREY,
                                          stroke_width=3, fill_color=BG, fill_opacity=1)
                         .move_to([4.0 + dx, cy + 1.05, 0]) for dx in (-1.05, 0, 1.05)])
        chips = VGroup(bchip("ATP", ATPc, size=22), bchip("ADP", ADPc, size=22), bchip("AMP", AMPc, size=22))
        for c_, dx in zip(chips, (-1.05, 0, 1.05)):
            c_.move_to([4.0 + dx, cy + 2.2, 0])
        self.at("compete for")
        self.play(FadeIn(slots), FadeIn(chips, shift=DOWN * 0.1), run_time=0.7)
        rd = T("reads the ratio", 28, GREY).move_to([4.0, cy - BH / 2 - 0.35, 0])
        self.at("reads their ratio")
        self.play(FadeIn(rd), run_time=0.4)
        self.play(*[Indicate(c, scale_factor=1.15) for c in chips], run_time=0.8)

        # the main switch on alpha
        thr = bchip("Thr 172", GOLD, size=24).move_to([-4.0, cy - 0.95, 0])
        lkb = bchip("LKB1", ORANGE, size=30).move_to([-4.0, -2.65, 0])
        self.at("main switch")
        self.play(FadeIn(thr, scale=0.9), run_time=0.5)
        self.at("phosphorylated by")
        self.play(FadeIn(lkb, shift=UP * 0.1), run_time=0.4)
        pb = pbadge().move_to(lkb.get_top() + UP * 0.1)
        self.play(FadeIn(pb), run_time=0.2)
        self.play(pb.animate.move_to(thr.get_right() + RIGHT * 0.3), run_time=0.7)
        
        # AMP on gamma
        self.at("With")
        self.play(chips[2].animate.move_to(slots[2].get_center()), slots[2].animate.set_stroke(AMPc), run_time=0.7)
        rem = VGroup(Line([0, 0, 0], [0.6, 0, 0], color=RED, stroke_width=5),
                     Line([0.6, 0.2, 0], [0.6, -0.2, 0], color=RED, stroke_width=6))
        rem_t = T("remove the phosphate: harder", 26, RED)
        add_a = Arrow([0, 0, 0], [0.6, 0, 0], buff=0, color=GREEN, stroke_width=5, tip_length=0.2)
        add_t = T("add it: easier (by most accounts)", 26, GREEN)
        r1 = VGroup(rem, rem_t).arrange(RIGHT, buff=0.2)
        r2 = VGroup(add_a, add_t).arrange(RIGHT, buff=0.2)
        rr = VGroup(r1, r2).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([0.9, -2.9, 0])
        self.at("harder to remove")
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.5)
        self.at("easier to add")
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.5)

        rule = T("AMP moves most, so AMPK reads AMP", 34, AMPc, weight=BOLD).move_to([0, 3.1, 0])
        self.at("moves most")
        self.play(FadeOut(title), FadeIn(rule), run_time=0.5)
        self.finish()


class S05End(EndCard):
    LINE = "AMP moves most, so AMPK reads AMP."
