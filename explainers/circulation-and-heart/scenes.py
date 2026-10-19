"""Circulation and the heart: a pump is a pressure difference  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
The lesson's own numbers only: 120 over 80 mmHg (adult human left ventricle and aorta, at rest),
right ventricle peak near 25 mmHg. Pressure levels are a schematic, "not to scale".

COLOR MAP (one color per concept, whole video)
  BLUE   = oxygen-poor blood and the chambers that hold it (right side of a mammal)
  ORANGE = oxygen-rich blood and the chambers that hold it (left side of a mammal)
  YELLOW = pressure (the level inside a chamber)
  GREEN  = a valve that is open
  RED    = a valve that is shut
  GREY   = structure: loops, pump, lungs, body, outlines, notes
  TEXT   = generic blood in the first scene (before oxygen content matters)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def btext(text, size=22, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.16, height=t.height + 0.1, stroke_width=0, fill_color=BG,
                     fill_opacity=0.85).move_to(t)
    return VGroup(back, t)


def arr(a, b, color=GREY, w=6, tip=0.25):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def dot(color, r=0.14):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1)


class S00Title(TitleCard):
    LESSON = "Circulation and the heart"
    TITLE = "A pump is a pressure difference"


# ---------------------------------------------------------------------------------------------
class S01Pump(SpokenScene):
    def construct(self):
        L, R, Bt, Tp, Mid = -4.1, 4.7, -2.2, 1.8, -0.2
        loop_col = GREY
        pump = bchip("pump", GREY, 28).move_to([L, Mid, 0]).set_z_index(6)
        a1 = arr([L, Mid + 0.45, 0], [L, Tp, 0], loop_col)
        a2 = arr([L, Tp, 0], [R, Tp, 0], loop_col)
        a3 = arr([R, Tp, 0], [R, Bt, 0], loop_col)
        a4 = arr([R, Bt, 0], [L, Bt, 0], loop_col)
        a5 = arr([L, Bt, 0], [L, Mid - 0.45, 0], loop_col)
        loop = VGroup(a1, a2, a3, a4, a5)

        segs = [((L, Mid), (L, Tp)), ((L, Tp), (R, Tp)), ((R, Tp), (R, Bt)), ((R, Bt), (L, Bt)), ((L, Bt), (L, Mid))]
        lens = [np.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]
        total = sum(lens)

        def pos(s):
            d = (s % 1.0) * total
            for (a, b), ln in zip(segs, lens):
                if d <= ln:
                    f = d / ln
                    return np.array([a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, 0])
                d -= ln
            return np.array([L, Mid, 0])

        prog = ValueTracker(0)
        dots = VGroup(*[dot(TEXT, 0.13) for _ in range(8)]).set_z_index(1)
        for i, d in enumerate(dots):
            d.add_updater(lambda m, i=i: m.move_to(pos(prog.get_value() + i / 8)))
        dots.set_opacity(0)

        c1 = bchip("an adult human: about 5 litres of blood", TEXT, 28).move_to([0.3, 0.7, 0]).set_z_index(5)
        c2 = bchip("each side of the heart, at rest:\nabout 5 litres every minute", GREY, 24).move_to([0.3, -0.9, 0]).set_z_index(5)

        self.at("adult human")
        self.play(FadeIn(pump), Create(loop), run_time=1.2)
        self.add(dots)
        self.play(FadeIn(c1), dots.animate.set_opacity(1), run_time=0.6)
        self.play(prog.animate.set_value(0.35), run_time=1.2, rate_func=linear)
        self.at("At rest")
        self.play(FadeIn(c2, shift=UP * 0.1), prog.animate.set_value(0.8), run_time=1.0, rate_func=linear)
        self.at("go round again")
        self.play(prog.animate.set_value(2.0), run_time=self.t_of("How does a pump") - self.elapsed() - 0.2 if False else 1.5, rate_func=linear)
        self.at("How does a pump")
        q = T("How does a pump manage that?", 34, TEXT, font=TITLE_FONT).move_to([1.0, -0.2, 0]).set_z_index(5)
        self.play(FadeOut(c1), FadeOut(c2), FadeIn(q), run_time=0.5)
        # pressure columns, shown on the narrator's words
        base = -1.3
        k = 0.016
        tall = Rectangle(width=0.9, height=130 * k, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                         fill_opacity=0.45).move_to([-2.0, base + 65 * k, 0])
        short = Rectangle(width=0.9, height=35 * k, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                          fill_opacity=0.45).move_to([1.0, base + 17.5 * k, 0])
        t_hi = T("higher pressure", 26, YELLOW).next_to(tall, DOWN, buff=0.15)
        t_lo = T("lower pressure", 26, YELLOW).next_to(short, DOWN, buff=0.15)
        self.at("higher pressure")
        self.play(FadeOut(q), FadeIn(tall, shift=UP * 0.2), FadeIn(t_hi), run_time=0.6)
        flow = arr([-1.4, base + 100 * k, 0], [0.4, base + 100 * k, 0], GREY)
        self.at("to lower")
        self.play(FadeIn(short, shift=UP * 0.2), FadeIn(t_lo), GrowArrow(flow), run_time=0.7)
        f_lbl = T("fluid flows", 24, GREY).next_to(flow, UP, buff=0.12)
        self.play(FadeIn(f_lbl), run_time=0.3)
        self.at("pressure difference")
        dash = DashedLine([1.0 - 0.45, base + 130 * k, 0], [1.0 + 1.0, base + 130 * k, 0], color=YELLOW, stroke_width=3)
        dbl = DoubleArrow([1.7, base + 35 * k, 0], [1.7, base + 130 * k, 0], buff=0, color=YELLOW, stroke_width=5,
                          tip_length=0.2)
        diff = T("pressure\ndifference", 24, YELLOW).next_to(dbl, RIGHT, buff=0.12)
        self.play(Create(dash), GrowFromCenter(dbl), FadeIn(diff), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Route(SpokenScene):
    def construct(self):
        XL, XM, XR = -4.2, 0.0, 4.2
        YT, YB = 1.5, -1.5
        body = bchip("body", GREY, 28).move_to([XL, YB, 0])
        ra = bchip("right atrium", BLUE, 26).move_to([XL, YT, 0])
        rv = bchip("right ventricle", BLUE, 26).move_to([XM, YT, 0])
        lungs = bchip("lungs", GREY, 28).move_to([XR, YT, 0])
        la = bchip("left atrium", ORANGE, 26).move_to([XR, YB, 0])
        lv = bchip("left ventricle", ORANGE, 26).move_to([XM, YB, 0])
        leg1 = T("oxygen-poor blood", 24, BLUE)
        leg2 = T("oxygen-rich blood", 24, ORANGE)
        legend = VGroup(leg1, leg2).arrange(DOWN, buff=0.18).move_to([0, 0, 0])
        self.at("mammal")
        self.play(*[FadeIn(m) for m in (body, ra, rv, lungs, la, lv)], FadeIn(legend), run_time=1.0)

        # arrows (edge to edge, with a small gap)
        a_br = arr([XL, YB + 0.55, 0], [XL, YT - 0.55, 0], BLUE)
        a_ar = arr([ra.get_right()[0] + 0.05, YT, 0], [rv.get_left()[0] - 0.05, YT, 0], BLUE)
        a_rl = arr([rv.get_right()[0] + 0.05, YT, 0], [lungs.get_left()[0] - 0.05, YT, 0], BLUE)
        a_la = arr([XR, YT - 0.55, 0], [XR, YB + 0.55, 0], ORANGE)
        a_al = arr([la.get_left()[0] - 0.05, YB, 0], [lv.get_right()[0] + 0.05, YB, 0], ORANGE)
        a_lb = arr([lv.get_left()[0] - 0.05, YB, 0], [body.get_right()[0] + 0.05, YB, 0], ORANGE)

        bd = dot(BLUE).move_to(body.get_center() + UP * 0.1)
        self.at("from the body")
        self.play(FadeIn(bd), GrowArrow(a_br), run_time=0.4)
        self.play(bd.animate.move_to([XL, YT - 0.35, 0]), run_time=0.9)
        self.at("right atrium")
        self.play(Circumscribe(ra, color=BLUE, buff=0.12), run_time=0.7)
        self.at("right ventricle pushes")
        self.play(GrowArrow(a_ar), bd.animate.move_to(rv.get_center() + DOWN * 0.05), run_time=0.8)
        self.at("to the lungs")
        self.play(GrowArrow(a_rl), bd.animate.move_to(lungs.get_center() + LEFT * 0.0), run_time=0.8)
        self.play(FadeOut(bd), run_time=0.2)

        od = dot(ORANGE).move_to(lungs.get_center())
        self.at("returns to the left")
        self.play(FadeIn(od), GrowArrow(a_la), run_time=0.4)
        self.play(od.animate.move_to(la.get_center() + UP * 0.45), run_time=0.7)
        self.at("left ventricle pushes")
        self.play(Circumscribe(la, color=ORANGE, buff=0.12), GrowArrow(a_al),
                  od.animate.move_to(lv.get_center()), run_time=0.9)
        self.at("the body", nth=1)
        self.play(GrowArrow(a_lb), od.animate.move_to(body.get_right() + RIGHT * 0.3), run_time=0.9)
        self.play(FadeOut(od), run_time=0.2)

        # the animal's own right and left
        rr = SurroundingRectangle(VGroup(ra, rv), color=GREY, buff=0.25, corner_radius=0.2, stroke_width=3)
        ll = SurroundingRectangle(VGroup(lv, la), color=GREY, buff=0.25, corner_radius=0.2, stroke_width=3)
        rr = DashedVMobject(rr, num_dashes=60)
        ll = DashedVMobject(ll, num_dashes=60)
        rt = T("the animal's right side", 24, GREY).next_to(rr, UP, buff=0.12)
        lt = T("the animal's left side", 24, GREY).next_to(ll, DOWN, buff=0.12)
        self.at("own right")
        self.play(Create(rr), Create(ll), FadeIn(rt), FadeIn(lt), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
K = 3.5 / 130.0          # screen units per mmHg in the sketch
Y0 = -2.3                # bottom of the chamber boxes
BOX_H = 3.8
PC = -0.4                # passage centre line
XLA, XLV, XAO = -4.45, 0.0, 4.45
WLA, WLV, WAO = 2.6, 3.0, 2.6
XMIT, XAOV = -2.325, 2.325


class Valve:
    def __init__(self, x):
        self.x = x
        self.passage = Rectangle(width=1.5, height=1.6, stroke_width=0, fill_color=GREY, fill_opacity=0.18
                                 ).move_to([x, PC, 0])
        self.mid = Line([x, PC + 0.8, 0], [x, PC - 0.8, 0], stroke_width=10, color=RED)
        self.top = Line([x, PC + 0.8, 0], [x, PC + 0.45, 0], stroke_width=10, color=RED)
        self.bot = Line([x, PC - 0.8, 0], [x, PC - 0.45, 0], stroke_width=10, color=RED)
        self.mob = VGroup(self.passage, self.mid, self.top, self.bot)

    def set(self, is_open, instant=False):
        col = GREEN if is_open else RED
        anims = [self.mid.animate.set_opacity(0 if is_open else 1).set_color(col),
                 self.top.animate.set_color(col), self.bot.animate.set_color(col)]
        return anims

    def init(self, is_open):
        col = GREEN if is_open else RED
        for m in (self.mid, self.top, self.bot):
            m.set_color(col)
        self.mid.set_opacity(0 if is_open else 1)


class Sketch:
    """Left atrium, left ventricle and aorta as boxes, with pressure levels and two valves."""

    def __init__(self, pa=10, pv=6, pao=80, mit_open=False, ao_open=False, show=0.0):
        self.pa, self.pv, self.pao = ValueTracker(pa), ValueTracker(pv), ValueTracker(pao)
        self.show = ValueTracker(show)

        def box(x, w, col):
            return RoundedRectangle(corner_radius=0.15, width=w, height=BOX_H, stroke_color=col, stroke_width=4,
                                    fill_color=col, fill_opacity=0.07).move_to([x, Y0 + BOX_H / 2, 0])
        self.b_la, self.b_lv, self.b_ao = box(XLA, WLA, ORANGE), box(XLV, WLV, ORANGE), box(XAO, WAO, ORANGE)
        self.l_la = T("left atrium", 26, ORANGE).move_to([XLA, 2.0, 0])
        self.l_lv = T("left ventricle", 26, ORANGE).move_to([XLV, 2.0, 0])
        self.l_ao = T("aorta", 26, ORANGE).move_to([XAO, 2.0, 0])
        self.boxes = VGroup(self.b_la, self.b_lv, self.b_ao, self.l_la, self.l_lv, self.l_ao)

        self.v_m, self.v_a = Valve(XMIT), Valve(XAOV)
        self.v_m.init(mit_open)
        self.v_a.init(ao_open)
        self.l_m = T("mitral\nvalve", 22, GREY, line_spacing=0.6).move_to([XMIT, 0.92, 0])
        self.l_a = T("aortic\nvalve", 22, GREY, line_spacing=0.6).move_to([XAOV, 0.92, 0])
        self.valves = VGroup(self.v_m.mob, self.v_a.mob, self.l_m, self.l_a)

        def fill(tr, x, w):
            def mk():
                h = max(tr.get_value() * K, 0.01)
                return Rectangle(width=w - 0.16, height=h, stroke_width=0, fill_color=YELLOW,
                                 fill_opacity=0.45 * self.show.get_value()).move_to([x, Y0 + h / 2 + 0.01, 0])
            return always_redraw(mk)
        self.fills = [fill(self.pa, XLA, WLA), fill(self.pv, XLV, WLV), fill(self.pao, XAO, WAO)]
        self.note = VGroup(T("yellow level = pressure", 22, YELLOW), T("in this sketch, not to scale", 22, GREY)
                           ).arrange(DOWN, aligned_edge=RIGHT, buff=0.08).move_to([4.2, 3.2, 0])
        self.title = None

    def put_title(self, text):
        t = T(text, 38, font=TITLE_FONT).move_to([-2.4, 3.2, 0])
        t.align_to([-6.2, 0, 0], LEFT)
        return t

    def cmp(self, text, color):
        c = bchip(text, color, 26).move_to([0, -3.15, 0])
        return c

    def mark(self, p, text, w):
        y = Y0 + p * K
        ln = DashedLine([-w / 2 + 0.08, y, 0], [w / 2 - 0.08, y, 0], color=TEXT, stroke_width=3)
        return ln

    def flow(self, scene, x0, x1, y=PC, n=4, rt=1.8):
        ds = [dot(ORANGE, 0.14).move_to([x0, y + (i - 1.5) * 0.22, 0]) for i in range(n)]
        scene.add(*ds)
        scene.play(LaggedStart(*[d.animate.move_to([x1, d.get_center()[1], 0]) for d in ds], lag_ratio=0.25),
                   run_time=rt, rate_func=linear)
        scene.play(*[FadeOut(d) for d in ds], run_time=0.25)


def base_scene(sc, sk, title, **kw):
    sc.add(sk.boxes, sk.valves, sk.note, *sk.fills)


class S03Filling(SpokenScene):
    def construct(self):
        sk = Sketch(pa=20, pv=8, pao=80, mit_open=False, ao_open=False, show=0.0)
        self.add(*sk.fills)
        title = sk.put_title("Filling")
        self.at("Now follow")
        self.play(FadeIn(sk.boxes), run_time=0.8)
        self.at("valve opens")
        self.play(FadeIn(sk.valves), run_time=0.6)
        self.at("pressure behind it")
        self.play(sk.show.animate.set_value(1.0), FadeIn(sk.note), run_time=0.9)
        self.at("First comes filling")
        self.play(FadeIn(title, shift=UP * 0.1), run_time=0.5)
        c = sk.cmp("ventricular pressure < atrial pressure", YELLOW)
        self.at("Ventricular pressure is below")
        self.play(FadeIn(c, shift=UP * 0.1), Indicate(sk.b_lv, color=YELLOW, scale_factor=1.03),
                  Indicate(sk.b_la, color=YELLOW, scale_factor=1.03), run_time=0.8)
        self.at("the mitral valve is open")
        self.play(*sk.v_m.set(True), run_time=0.4)
        self.play(sk.pv.animate.set_value(10), run_time=0.01)
        sk.flow(self, XMIT - 0.6, XMIT + 1.5, rt=1.6)
        self.at("adds the last part")
        self.play(Indicate(sk.b_la, color=ORANGE, scale_factor=1.05), sk.pa.animate.set_value(26),
                  sk.pv.animate.set_value(14), run_time=1.0)
        sk.flow(self, XMIT - 0.6, XMIT + 1.5, rt=1.2)
        self.finish()


class S04Squeeze(SpokenScene):
    def construct(self):
        sk = Sketch(pa=26, pv=14, pao=80, mit_open=True, ao_open=False, show=1.0)
        self.add(sk.boxes, sk.valves, sk.note, *sk.fills)
        title = sk.put_title("Filling")
        self.add(title)
        c0 = sk.cmp("ventricular pressure < atrial pressure", YELLOW)
        self.add(c0)
        self.at("Then the ventricle contracts")
        t2 = sk.put_title("Isovolumic contraction")
        self.play(ReplacementTransform(title, t2), Indicate(sk.b_lv, color=YELLOW, scale_factor=1.03), run_time=0.7)
        self.at("rises above atrial")
        c1 = sk.cmp("ventricular pressure > atrial pressure", YELLOW)
        self.play(sk.pv.animate.set_value(40), ReplacementTransform(c0, c1), run_time=1.0)
        self.at("the mitral valve closes")
        self.play(*sk.v_m.set(False), run_time=0.4)
        self.at("still below aortic")
        c2 = sk.cmp("ventricular pressure < aortic pressure", YELLOW)
        self.play(sk.pv.animate.set_value(68), ReplacementTransform(c1, c2), run_time=1.4)
        self.at("aortic valve stays shut")
        self.play(Indicate(sk.v_a.mob, color=RED, scale_factor=1.1), run_time=0.8)
        self.at("Both valves are closed")
        both = bchip("both valves shut", RED, 26).move_to([0, -3.15, 0])
        self.play(ReplacementTransform(c2, both), run_time=0.6)
        self.at("cannot change")
        self.play(Indicate(sk.b_lv, color=ORANGE, scale_factor=1.03), run_time=0.7)
        self.at("This phase is called")
        self.play(Indicate(t2, color=GOLD, scale_factor=1.05), run_time=0.8)
        self.finish()


class S05Eject(SpokenScene):
    def construct(self):
        sk = Sketch(pa=26, pv=68, pao=80, mit_open=False, ao_open=False, show=1.0)
        self.add(sk.boxes, sk.valves, sk.note, *sk.fills)
        title = sk.put_title("Isovolumic contraction")
        self.add(title)
        self.at("keeps rising")
        self.play(sk.pv.animate.set_value(79), run_time=1.0)
        c = sk.cmp("ventricular pressure > aortic pressure", YELLOW)
        self.at("passes aortic pressure")
        self.play(sk.pv.animate.set_value(82), FadeIn(c, shift=UP * 0.1), run_time=0.5)
        ln80 = sk.mark(80, "", WAO)
        ln80.shift(RIGHT * XAO)
        l80 = btext("about 80 mmHg", 22, TEXT).move_to([XAO, Y0 + 80 * K + 0.3, 0])
        self.at("millimeters of mercury")
        self.play(Create(ln80), FadeIn(l80), run_time=0.7)
        t3 = sk.put_title("Ejection")
        self.at("the aortic valve opens")
        self.play(*sk.v_a.set(True), ReplacementTransform(title, t3), run_time=0.4)
        self.play(sk.pv.animate.set_value(100), sk.pao.animate.set_value(100), run_time=0.01)
        ds = [dot(ORANGE, 0.14).move_to([XAOV - 0.7, PC + (i - 1.5) * 0.22, 0]) for i in range(4)]
        self.add(*ds)
        self.play(LaggedStart(*[d.animate.move_to([XAOV + 0.9, d.get_center()[1], 0]) for d in ds], lag_ratio=0.2),
                  sk.pv.animate.set_value(120), sk.pao.animate.set_value(120), run_time=1.4, rate_func=linear)
        self.play(*[FadeOut(d) for d in ds], run_time=0.2)
        ln120 = DashedLine([-1.42, Y0 + 120 * K, 0], [1.42, Y0 + 120 * K, 0], color=TEXT, stroke_width=3)
        l120 = btext("near 120 mmHg", 22, TEXT).move_to([XLV, Y0 + 120 * K + 0.3, 0])
        self.at("peak near")
        ln120a = DashedLine([XAO - 1.22, Y0 + 120 * K, 0], [XAO + 1.22, Y0 + 120 * K, 0], color=TEXT, stroke_width=3)
        l120a = btext("near 120 mmHg", 22, TEXT).move_to([XAO, Y0 + 120 * K + 0.3, 0])
        self.play(FadeOut(ln80), FadeOut(l80), Create(ln120), FadeIn(l120), Create(ln120a), FadeIn(l120a),
                  FadeOut(c), run_time=0.8)
        self.at("relaxes")
        t4 = sk.put_title("Isovolumic relaxation")
        c2 = sk.cmp("ventricular pressure < aortic pressure", YELLOW)
        self.play(FadeOut(l120), FadeOut(ln120), FadeOut(l120a), FadeOut(ln120a), run_time=0.4)
        self.play(sk.pv.animate.set_value(70), sk.pao.animate.set_value(105), FadeIn(c2, shift=UP * 0.1),
                  run_time=1.2)
        self.at("the aortic valve closes")
        self.play(*sk.v_a.set(False), ReplacementTransform(t3, t4), run_time=0.4)
        self.play(sk.pv.animate.set_value(10), sk.pao.animate.set_value(85), run_time=1.0)
        self.at("Both valves are shut")
        both = bchip("both valves shut", RED, 26).move_to([0, -3.15, 0])
        self.play(ReplacementTransform(c2, both), run_time=0.4)
        self.at("mitral valve opens again")
        self.play(*sk.v_m.set(True), FadeOut(both), run_time=0.5)
        sk.flow(self, XMIT - 0.6, XMIT + 1.5, rt=1.2)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        base, kk = -1.7, 3.1 / 120.0
        W = 1.6

        def col(x, p, color=YELLOW):
            return Rectangle(width=W, height=max(p * kk, 0.05), stroke_color=color, stroke_width=3, fill_color=color,
                             fill_opacity=0.45).move_to([x, base + max(p * kk, 0.05) / 2, 0])

        head = M("120 / 80 mmHg", 48, TEXT).move_to([0, 3.0, 0])
        sub = T("adult human at rest: left ventricle over aorta", 24, GREY).next_to(head, DOWN, buff=0.12)
        self.at("in the reading")
        self.play(FadeIn(head), FadeIn(sub), run_time=0.8)
        xa, xv = -2.8, 2.8
        ao = col(xa, 80)
        ao_v = M("80 mmHg", 28, YELLOW).next_to(ao, UP, buff=0.12)
        ao_l = T("aorta:\nlowest pressure", 24, ORANGE, line_spacing=0.7).next_to(ao, DOWN, buff=0.15)
        self.at("lowest pressure")
        self.play(FadeIn(ao, shift=UP * 0.2), FadeIn(ao_v), FadeIn(ao_l), run_time=0.8)
        lv = col(xv, 4)
        lv_v = T("a few mmHg", 28, YELLOW).next_to(lv, UP, buff=0.12)
        lv_l = T("left ventricle:\nwhile it fills", 24, ORANGE, line_spacing=0.7).next_to(lv, DOWN, buff=0.15)
        self.at("It is not")
        self.play(FadeIn(lv, shift=UP * 0.1), FadeIn(lv_v), FadeIn(lv_l), run_time=0.8)
        # the right ventricle
        lv2 = col(xa, 120)
        lv2_v = M("near 120 mmHg", 28, YELLOW).next_to(lv2, UP, buff=0.12)
        lv2_l = T("left ventricle:\npeak", 24, ORANGE, line_spacing=0.7).next_to(lv2, DOWN, buff=0.15)
        rv = col(xv, 25, BLUE)
        rv_v = M("near 25 mmHg", 28, YELLOW).next_to(rv, UP, buff=0.12)
        rv_l = T("right ventricle:\npeak", 24, BLUE, line_spacing=0.7).next_to(rv, DOWN, buff=0.15)
        self.at("The right ventricle runs")
        self.play(ReplacementTransform(ao, lv2), ReplacementTransform(ao_v, lv2_v), ReplacementTransform(ao_l, lv2_l),
                  ReplacementTransform(lv, rv), ReplacementTransform(lv_v, rv_v), ReplacementTransform(lv_l, rv_l),
                  FadeOut(head), FadeOut(sub), run_time=1.2)
        lungs_t = T("same cycle, against the low resistance of the lungs", 24, BLUE).move_to([0, 2.9, 0])
        self.play(FadeIn(lungs_t), run_time=0.5)
        self.at("same volume at a fifth")
        fifth = T("same volume, a fifth of the pressure", 26, TEXT).move_to([0, -3.15, 0])
        self.play(FadeIn(fifth), Indicate(rv, color=BLUE, scale_factor=1.05), run_time=0.8)
        # the rule
        self.at("Keep this rule")
        self.play(*[FadeOut(m) for m in (lv2, lv2_v, lv2_l, rv, rv_v, rv_l, lungs_t, fifth)], run_time=0.6)
        bx_b = RoundedRectangle(corner_radius=0.15, width=2.8, height=3.0, stroke_color=ORANGE, stroke_width=4,
                                fill_color=ORANGE, fill_opacity=0.07).move_to([-3.4, 0.7, 0])
        bx_a = RoundedRectangle(corner_radius=0.15, width=2.8, height=3.0, stroke_color=ORANGE, stroke_width=4,
                                fill_color=ORANGE, fill_opacity=0.07).move_to([3.4, 0.7, 0])
        hb, ha = 2.5, 1.2
        f_b = Rectangle(width=2.64, height=hb, stroke_width=0, fill_color=YELLOW, fill_opacity=0.45
                        ).move_to([-3.4, 0.7 - 1.5 + hb / 2 + 0.01, 0])
        f_a = Rectangle(width=2.64, height=ha, stroke_width=0, fill_color=YELLOW, fill_opacity=0.45
                        ).move_to([3.4, 0.7 - 1.5 + ha / 2 + 0.01, 0])
        pas = Rectangle(width=2.0, height=1.2, stroke_width=0, fill_color=GREY, fill_opacity=0.18).move_to([0, -0.2, 0])
        vtop = Line([0, 0.4, 0], [0, 0.16, 0], stroke_width=9, color=GREEN)
        vbot = Line([0, -0.8, 0], [0, -0.56, 0], stroke_width=9, color=GREEN)
        l_b = T("pressure behind", 26, YELLOW).next_to(bx_b, DOWN, buff=0.15)
        l_a = T("pressure ahead", 26, YELLOW).next_to(bx_a, DOWN, buff=0.15)
        fl = arr([-0.8, -0.2, 0], [0.8, -0.2, 0], GREEN)
        self.play(*[FadeIn(m) for m in (bx_b, bx_a, f_b, f_a, pas, vtop, vbot, l_b, l_a)], GrowArrow(fl), run_time=0.9)
        rule = T("A valve opens when pressure behind it\nexceeds pressure ahead.", 34, font=TITLE_FONT,
                 line_spacing=0.8).move_to([0, -2.75, 0])
        self.at("A valve opens when")
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "A valve opens when pressure behind it exceeds pressure ahead."
