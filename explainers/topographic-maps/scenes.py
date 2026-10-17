"""Topographic maps: axons find their place among neighbours  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = retinal axon / retinal cell / EphA receptor (brighter = more EphA)
  ORANGE = ephrin-A ligand in the tectum (more opaque = more ephrin)
  PURPLE = retinal cells given extra EphA (the knock-in mouse)
  YELLOW = the lure, and "compare with neighbours" highlights
  RED    = repelled / stop / wrong turn / cut
  GREEN  = the ordered result
  GREY   = eye, tectum and other structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def bar(x, y, h, w=0.6, color=GREY):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.15).move_to([x, y, 0])


def grad_bar(x, y, h, color, w=0.6, n=20, top_high=True, lo=0.08, hi=0.9):
    """vertical bar made of n slices whose opacity runs low to high."""
    sh = h / n
    g = VGroup()
    for i in range(n):
        f = i / (n - 1)
        op = hi - (hi - lo) * f if top_high else lo + (hi - lo) * f
        g.add(Rectangle(width=w, height=sh + 0.005, stroke_width=0, fill_color=color, fill_opacity=op)
              .move_to([x, y + h / 2 - sh * (i + 0.5), 0]))
    g.add(RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_opacity=0).move_to([x, y, 0]))
    return g


def cell(x, y, op=1.0, color=BLUE, r=0.17):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=op).move_to([x, y, 0])


def axline(a, b, color=BLUE, w=4, op=1.0):
    return Line(a, b, color=color, stroke_width=w, stroke_opacity=op)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def tag(text, size=24, color=GREY):
    return T(text, size, color)


class S00Title(TitleCard):
    LESSON = "Topographic maps"
    TITLE = "Axons find place among neighbours"


# ---------------------------------------------------------------------------------------------
class S01Newt(SpokenScene):
    def construct(self):
        EX, TX = -3.2, 4.4
        ys = [0.9, 0.0, -0.9]
        ops = [1.0, 0.6, 0.3]
        eye = Circle(radius=1.55, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([EX, 0, 0])
        pupil = Circle(radius=0.38, stroke_width=0, fill_color=GREY, fill_opacity=0.7).move_to([EX - 1.0, 0, 0])
        dots = VGroup(*[cell(EX + 0.95, y, o, r=0.2) for y, o in zip(ys, ops)])
        eye_lbl = tag("newt eye", 24).move_to([EX, -2.15, 0])
        tect = bar(TX, 0, 3.4, 0.6)
        marks = VGroup(*[Circle(radius=0.1, stroke_width=0, fill_color=GREY, fill_opacity=0.9).move_to([TX, y, 0]) for y in ys])
        tect_lbl = tag("tectum", 24).move_to([TX, -2.15, 0])
        start = lambda y: [EX + 1.15, y, 0]
        end = lambda y: [TX - 0.35, y, 0]
        lines = VGroup(*[axline(start(y), end(y), BLUE, 4, o) for y, o in zip(ys, ops)])
        self.play(FadeIn(eye), FadeIn(pupil), FadeIn(dots), FadeIn(eye_lbl), FadeIn(tect), FadeIn(marks),
                  FadeIn(tect_lbl), Create(lines), run_time=0.9)
        # flip the eye (dots swap top and bottom through an arc)
        self.at("upside down")
        self.play(FadeOut(lines),
                  dots[0].animate(path_arc=PI).move_to([EX + 0.95, ys[2], 0]),
                  dots[2].animate(path_arc=PI).move_to([EX + 0.95, ys[0], 0]),
                  run_time=1.0)
        # cut
        self.at("cut the optic nerve")
        x1 = Line([0.1, 0.5, 0], [0.9, -0.5, 0], color=RED, stroke_width=7)
        x2 = Line([0.1, -0.5, 0], [0.9, 0.5, 0], color=RED, stroke_width=7)
        cut = VGroup(x1, x2)
        cut_lbl = tag("cut", 26, RED).move_to([0.5, 1.0, 0])
        self.play(Create(cut), FadeIn(cut_lbl), run_time=0.5)
        # regrow: the bright cell is now at the bottom but still reaches the top spot
        self.at("let it regrow")
        new = VGroup(axline(start(ys[2]), end(ys[0]), BLUE, 5, 1.0),
                     axline(start(ys[1]), end(ys[1]), BLUE, 5, 0.6),
                     axline(start(ys[0]), end(ys[2]), BLUE, 5, 0.3))
        self.play(FadeOut(cut), FadeOut(cut_lbl), Create(new), run_time=1.1)
        # lure and wrong head turn
        self.at("Hold a lure")
        lure = Circle(radius=0.2, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([EX, 3.0, 0])
        lure_lbl = tag("lure", 24, YELLOW).next_to(lure, RIGHT, buff=0.2)
        self.play(FadeIn(lure, scale=0.5), FadeIn(lure_lbl), run_time=0.5)
        self.at("turns its head down")
        arrow = arr([-5.6, 0.9, 0], [-5.6, -1.0, 0], RED, 7)
        a_lbl = tag("turns down", 24, RED).move_to([-5.2, -1.55, 0])
        self.play(GrowArrow(arrow), FadeIn(a_lbl), run_time=0.7)
        self.at("anyone watched")
        self.play(Indicate(arrow, color=RED, scale_factor=1.1), run_time=0.8)
        self.at("went back to the place")
        self.play(*[Indicate(l, color=YELLOW, scale_factor=1.0) for l in new], run_time=1.0)
        self.at("know where to go")
        qs = VGroup(*[T("?", 40, YELLOW, weight=BOLD).move_to([TX + 0.75, y, 0]) for y in ys])
        self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in qs], lag_ratio=0.25), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
RX, TX2 = -3.0, 3.0


def map_ys(n=7, top=2.4):
    return np.linspace(top, -top, n)


class S02Map(SpokenScene):
    def construct(self):
        ys = map_ys()
        ops = np.linspace(1.0, 0.25, len(ys))
        rbar, tbar = bar(RX, 0, 5.7), bar(TX2, 0, 5.7)
        r_lbl = tag("retina", 26).move_to([RX, 3.3, 0])
        t_lbl = tag("tectum", 26).move_to([TX2, 3.3, 0])
        self.play(FadeIn(rbar), FadeIn(tbar), FadeIn(r_lbl), FadeIn(t_lbl), run_time=0.8)
        cells = VGroup(*[cell(RX, y, o) for y, o in zip(ys, ops)])
        slots = VGroup(*[Circle(radius=0.11, stroke_width=0, fill_color=GREY, fill_opacity=0.9).move_to([TX2, y, 0]) for y in ys])
        lines = VGroup(*[axline([RX + 0.2, y, 0], [TX2 - 0.2, y, 0], BLUE, 4, o) for y, o in zip(ys, ops)])
        self.at("The retina sends")
        self.play(FadeIn(cells), run_time=0.5)
        self.at("target in the midbrain")
        self.play(FadeIn(slots), LaggedStart(*[Create(l) for l in lines], lag_ratio=0.12), run_time=1.6)
        self.at("The map is orderly")
        self.wait(0.3)
        self.at("Neighbors in the retina")
        box_r = SurroundingRectangle(VGroup(cells[2], cells[3]), color=YELLOW, buff=0.15, corner_radius=0.1)
        box_t = SurroundingRectangle(VGroup(slots[2], slots[3]), color=YELLOW, buff=0.15, corner_radius=0.1)
        self.play(Create(box_r), run_time=0.6)
        self.at("neighbors in the tectum")
        self.play(Create(box_t), run_time=0.6)
        self.at("In the chick")
        self.play(FadeOut(box_r), FadeOut(box_t), run_time=0.4)
        tl = [tag("temporal", 26).move_to([-5.2, ys[0], 0]), tag("nasal", 26).move_to([-5.2, ys[-1], 0]),
              tag("front", 26).move_to([5.0, ys[0], 0]), tag("back", 26).move_to([5.0, ys[-1], 0])]
        self.play(*[FadeIn(t) for t in tl], run_time=0.6)
        self.at("temporal retina")
        hot = lines[0].copy().set_color(YELLOW).set_stroke(width=8, opacity=1)
        self.play(Create(hot), run_time=0.6)
        self.at("Nasal axons end")
        hot2 = lines[-1].copy().set_color(YELLOW).set_stroke(width=8, opacity=1)
        self.play(FadeOut(hot), Create(hot2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Slopes(SpokenScene):
    def construct(self):
        TXx = 3.4
        tect = bar(TXx, 0, 5.7)
        t_lbl = tag("tectum", 26).move_to([TXx, 3.3, 0])
        self.play(FadeIn(tect), FadeIn(t_lbl), run_time=0.7)
        # the growth cone: a tip with a small circle of what it can sense
        trail = axline([-5.5, 0.4, 0], [1.4, 0.4, 0], BLUE, 5)
        cone = Triangle(color=BLUE, fill_opacity=1, stroke_width=0).scale(0.28).rotate(-PI / 2).move_to([1.55, 0.4, 0])
        self.at("A growth cone")
        self.play(Create(trail), FadeIn(cone), run_time=1.0)
        ring = DashedVMobject(Circle(radius=0.8, color=YELLOW, stroke_width=4)).move_to(cone)
        ring_lbl = tag("senses only what is close", 24, YELLOW).move_to([0.0, -1.0, 0])
        self.at("senses only what is close")
        self.play(Create(ring), FadeIn(ring_lbl), run_time=0.8)
        self.at("spans the whole target")
        span = DoubleArrow([4.5, 2.7, 0], [4.5, -2.7, 0], color=GREY, stroke_width=5, buff=0)
        span_lbl = tag("whole target", 24).move_to([5.5, 0, 0]).rotate(PI / 2)
        self.play(GrowFromCenter(span), FadeIn(span_lbl), run_time=0.8)
        self.at("pair of opposite slopes")
        self.play(*[FadeOut(m) for m in (trail, cone, ring, ring_lbl, span, span_lbl, t_lbl)], run_time=0.6)
        # retina gradient (EphA, high at top = temporal)
        rg = grad_bar(-3.4, 0, 5.4, BLUE)
        r_title = tag("retina: EphA", 26, BLUE).move_to([-3.4, 3.3, 0])
        self.at("In the retina")
        self.play(FadeIn(rg), FadeIn(r_title), run_time=0.7)
        hi = tag("temporal: high", 24, BLUE).move_to([-5.35, 2.3, 0])
        lo = tag("nasal: low", 24, BLUE).move_to([-5.45, -2.3, 0])
        self.at("high on the temporal")
        self.play(FadeIn(hi), run_time=0.4)
        self.at("low on the nasal")
        self.play(FadeIn(lo), run_time=0.4)
        # ephrin gradient (low at top = front, high at bottom = back)
        tg = grad_bar(TXx, 0, 5.4, ORANGE, top_high=False)
        t_title = tag("tectum: ephrin-A", 26, ORANGE).move_to([TXx, 3.3, 0])
        self.at("In the tectum")
        self.play(FadeOut(tect), FadeIn(tg), FadeIn(t_title), run_time=0.7)
        f = tag("front: low", 24, ORANGE).move_to([5.45, 2.3, 0])
        b = tag("back: high", 24, ORANGE).move_to([5.45, -2.3, 0])
        self.at("rises from front")
        self.play(FadeIn(f), run_time=0.4)
        self.at("to back")
        self.play(FadeIn(b), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Stop(SpokenScene):
    def construct(self):
        LY_T, LY_N, BY = 2.0, 0.55, -1.15
        X0, X1 = -5.4, 5.4
        n = 24
        w = (X1 - X0) / n
        tect = VGroup()
        for i in range(n):
            tect.add(Rectangle(width=w + 0.005, height=0.9, stroke_width=0, fill_color=ORANGE,
                               fill_opacity=0.08 + 0.82 * i / (n - 1)).move_to([X0 + w * (i + 0.5), BY, 0]))
        tect.add(RoundedRectangle(corner_radius=0.12, width=X1 - X0, height=0.9, stroke_color=ORANGE, stroke_width=3,
                                  fill_opacity=0).move_to([0, BY, 0]))
        front = tag("front", 24).move_to([X0 + 0.5, BY - 0.9, 0])
        back = tag("back", 24).move_to([X1 - 0.5, BY - 0.9, 0])
        eph = tag("ephrin-A: low to high", 24, ORANGE).move_to([0, BY - 0.9, 0])
        self.play(FadeIn(tect), FadeIn(front), FadeIn(back), FadeIn(eph), run_time=0.8)

        def runner(y, op, label, lx):
            x = ValueTracker(X0)
            trail = always_redraw(lambda: axline([X0 - 0.4, y, 0], [x.get_value() - 0.05, y, 0], BLUE, 5, op))
            cone = always_redraw(lambda: Triangle(color=BLUE, fill_opacity=op, stroke_width=0).scale(0.3)
                                 .rotate(-PI / 2).move_to([x.get_value() + 0.15, y, 0]))
            lbl = tag(label, 24, BLUE).move_to([lx, y + 0.55, 0])
            return x, trail, cone, lbl

        xt, trail_t, cone_t, lbl_t = runner(LY_T, 1.0, "temporal axon: much EphA", -3.9)
        xn, trail_n, cone_n, lbl_n = runner(LY_N, 0.45, "nasal axon: little EphA", 1.2)
        self.at("Temporal axons carry")
        self.add(trail_t, cone_t)
        self.play(FadeIn(lbl_t), run_time=0.5)
        self.at("repels them")
        self.play(xt.animate.set_value(-2.6), run_time=1.3, rate_func=linear)
        stop_bar = Line([-2.15, LY_T - 0.35, 0], [-2.15, LY_T + 0.35, 0], color=RED, stroke_width=8)
        drop_t = DashedLine([-2.6, LY_T - 0.35, 0], [-2.6, BY + 0.45, 0], color=RED, stroke_width=4)
        self.play(Create(stop_bar), run_time=0.3)
        self.at("stop in the front")
        self.play(Create(drop_t), run_time=0.6)
        self.at("Nasal axons carry")
        self.add(trail_n, cone_n)
        self.play(FadeIn(lbl_n), run_time=0.5)
        self.at("tolerate more")
        self.play(xn.animate.set_value(3.8), run_time=2.0, rate_func=linear)
        drop_n = DashedLine([3.8, LY_N - 0.3, 0], [3.8, BY + 0.45, 0], color=GREY, stroke_width=4)
        self.at("into the back")
        self.play(Create(drop_n), run_time=0.6)
        self.at("stops where its own")
        rule = chip("stops where receptor meets enough ligand", YELLOW, size=26)
        rule.move_to([0, -3.05, 0])
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
RXX, TXX = -3.0, 3.0
N8 = 8
YS8 = np.linspace(2.2, -2.2, N8)
KNOCK = [1, 2, 5, 7]           # cells given extra EphA (scattered across the retina)
NORM = [0, 3, 4, 6]
Y_PURPLE = np.linspace(2.2, 0.35, 4)
Y_BLUE = np.linspace(-0.35, -2.2, 4)


def map_base(scene, knock=False):
    rbar, tbar = bar(RXX, 0, 5.4), bar(TXX, 0, 5.4)
    rl = tag("retina", 24).move_to([RXX, -3.2, 0])
    tl = tag("tectum", 24).move_to([TXX, -3.2, 0])
    cells = VGroup(*[cell(RXX, y, 0.85, PURPLE if (knock and i in KNOCK) else BLUE) for i, y in enumerate(YS8)])
    return rbar, tbar, rl, tl, cells


def numbered_ends():
    return VGroup(*[M(str(k + 1), 22, PURPLE, weight=BOLD).move_to([TXX, y, 0]) for k, y in enumerate(Y_PURPLE)],
                  *[M(str(k + 1), 22, BLUE, weight=BOLD).move_to([TXX, y, 0]) for k, y in enumerate(Y_BLUE)])


class S05Test(SpokenScene):
    def construct(self):
        rbar, tbar, rl, tl, cells = map_base(self)
        lines = VGroup(*[axline([RXX + 0.2, y, 0], [TXX - 0.2, y, 0], BLUE, 4, 0.85) for y in YS8])
        q1 = chip("absolute level?", BLUE, size=26).move_to([-3.0, 3.3, 0])
        q2 = chip("vs neighbours?", YELLOW, size=26).move_to([3.0, 3.3, 0])
        self.play(FadeIn(rbar), FadeIn(tbar), FadeIn(rl), FadeIn(tl), FadeIn(cells), Create(lines), run_time=1.0)
        self.at("absolute level")
        self.play(FadeIn(q1), run_time=0.5)
        self.at("compare itself")
        self.play(FadeIn(q2), run_time=0.5)
        self.at("In mouse")
        self.play(FadeOut(q1), FadeOut(q2), run_time=0.4)
        self.at("random half")
        anims = []
        for i in KNOCK:
            anims += [cells[i].animate.set_color(PURPLE).set_fill(PURPLE, 0.85), lines[i].animate.set_color(PURPLE)]
        lab = chip("extra EphA", PURPLE, size=24).move_to([-5.3, 0.0, 0])
        self.play(*anims, FadeIn(lab), run_time=0.8)
        self.at("absolute levels")
        ghosts = VGroup()
        for i in KNOCK:
            y = YS8[i]
            ghosts.add(DashedLine([RXX + 0.2, y, 0], [TXX - 0.2, y + 0.5, 0], color=PURPLE, stroke_width=4))
            ghosts.add(Circle(radius=0.12, stroke_color=PURPLE, stroke_width=3).move_to([TXX, y + 0.5, 0]))
        pred = tag("predicted", 24, PURPLE).move_to([5.4, 0.0, 0])
        self.play(Create(ghosts), FadeIn(pred), run_time=0.9)
        # clear the old answer before the new one
        self.at("Instead")
        self.play(FadeOut(ghosts), FadeOut(pred), run_time=0.4)
        self.at("took the front")
        self.play(*[lines[i].animate.put_start_and_end_on([RXX + 0.2, YS8[i], 0], [TXX - 0.2, Y_PURPLE[k], 0])
                    for k, i in enumerate(KNOCK)], run_time=1.3)
        self.at("pushed to the back")
        self.play(*[lines[i].animate.put_start_and_end_on([RXX + 0.2, YS8[i], 0], [TXX - 0.2, Y_BLUE[k], 0])
                    for k, i in enumerate(NORM)], run_time=1.3)
        self.at("Two orderly maps")
        br1 = Brace(Line([TXX + 0.4, Y_PURPLE[0], 0], [TXX + 0.4, Y_PURPLE[-1], 0]), RIGHT, color=PURPLE)
        br2 = Brace(Line([TXX + 0.4, Y_BLUE[0], 0], [TXX + 0.4, Y_BLUE[-1], 0]), RIGHT, color=BLUE)
        l1 = tag("extra EphA", 24, PURPLE).next_to(br1, RIGHT, buff=0.12)
        l2 = tag("normal", 24, BLUE).next_to(br2, RIGHT, buff=0.12)
        ends = numbered_ends()
        self.play(GrowFromCenter(br1), GrowFromCenter(br2), FadeIn(l1), FadeIn(l2), FadeIn(ends), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        rbar, tbar, rl, tl, cells = map_base(self, knock=True)
        lines = VGroup()
        for i, y in enumerate(YS8):
            if i in KNOCK:
                ty, col = Y_PURPLE[KNOCK.index(i)], PURPLE
            else:
                ty, col = Y_BLUE[NORM.index(i)], BLUE
            lines.add(axline([RXX + 0.2, y, 0], [TXX - 0.2, ty, 0], col, 4, 0.85))
        br1 = Brace(Line([TXX + 0.4, Y_PURPLE[0], 0], [TXX + 0.4, Y_PURPLE[-1], 0]), RIGHT, color=PURPLE)
        br2 = Brace(Line([TXX + 0.4, Y_BLUE[0], 0], [TXX + 0.4, Y_BLUE[-1], 0]), RIGHT, color=BLUE)
        l1 = tag("extra EphA", 24, PURPLE).next_to(br1, RIGHT, buff=0.12)
        l2 = tag("normal", 24, BLUE).next_to(br2, RIGHT, buff=0.12)
        ends = numbered_ends()
        self.add(rbar, tbar, rl, tl, cells, lines, br1, br2, l1, l2, ends)
        self.wait(0.3)
        self.at("judged against the others")
        box = SurroundingRectangle(VGroup(cells[2], cells[3], cells[4]), color=YELLOW, buff=0.15, corner_radius=0.1)
        nb = tag("neighbours", 24, YELLOW).move_to([-5.0, (YS8[2] + YS8[4]) / 2, 0])
        self.play(Create(box), FadeIn(nb), run_time=0.7)
        self.at("relative to its")
        rule = chip("EphA signal compared with neighbours", YELLOW, size=26).move_to([0, 3.3, 0])
        self.play(FadeIn(rule, shift=DOWN * 0.15), run_time=0.7)
        self.at("compete for space")
        a1 = VGroup(arr([5.9, 0.12, 0], [5.9, 1.0, 0], PURPLE, 6), tag("to front", 24, PURPLE).move_to([4.85, 0.58, 0]))
        a2 = VGroup(arr([5.9, -0.12, 0], [5.9, -1.0, 0], BLUE, 6), tag("to back", 24, BLUE).move_to([4.9, -0.58, 0]))
        self.play(FadeOut(box), FadeOut(nb), FadeIn(a1), FadeIn(a2), run_time=0.8)
        self.at("short distance")
        ring = DashedVMobject(Circle(radius=0.55, color=YELLOW, stroke_width=4)).move_to([TXX, Y_PURPLE[1], 0])
        self.play(FadeOut(a1), FadeOut(a2), Create(ring), run_time=0.7)
        self.at("global order")
        glow = SurroundingRectangle(tbar, color=GREEN, buff=0.12, corner_radius=0.15, stroke_width=5)
        order = chip("local rules, global order", GREEN, size=26).move_to([0, 3.3, 0])
        self.play(FadeOut(ring), FadeOut(rule), Create(glow), FadeIn(order), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Axons place themselves relative to their neighbours."
