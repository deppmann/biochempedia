"""Reelin and the reeler mouse: one missing protein, a cortex built wrong  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole film)
  ORANGE = the first-born neurons (the first thin sheet)
  BLUE   = the next-born neurons
  GREEN  = the last-born neurons
  YELLOW = Reelin and the Cajal-Retzius cells that make it
  TEAL   = the two receptors (ApoER2, VLDLR)
  PURPLE = Dab1, the adaptor
  PINK   = the Src-family kinases (Fyn and Src)
  GOLD   = a phosphate group (the little "P" badge)
  RED    = the reeler problem: a block, a stop, a missing runner
  GREY   = tissue, membranes, outlines, labels
  WHITE  = the baton in the relay picture
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E8789F"

SL_W, SL_H = 4.4, 5.7
TOP, BOT = 2.85, -2.85
DR = 0.17
LA = [-1.8, -1.08, -0.36, 0.36, 1.08, 1.8]      # lanes for waves one and three
LB = [-1.44, -0.72, 0.0, 0.72, 1.44]             # lanes for wave two
LSUB = [-1.44, 0.0, 1.44]

# resting rows in the normal cortex
Y_CR, Y_LATE, Y_EARLY, Y_SUB = 2.58, 1.45, 0.35, -0.8
Y_START = -2.55


def neuron(x, y, color):
    return Circle(radius=DR, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.65).move_to([x, y, 0])


def wave(cx, lanes, y, color):
    return VGroup(*[neuron(cx + l, y, color) for l in lanes])


def slab(cx, with_vz=True):
    body = Rectangle(width=SL_W, height=SL_H, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.07).move_to([cx, 0, 0])
    g = VGroup(body)
    if with_vz:
        vz = Rectangle(width=SL_W, height=0.55, stroke_width=0, fill_color=GREY, fill_opacity=0.22).move_to([cx, BOT + 0.275, 0])
        g.add(vz)
    return g


def lab(text, color=GREY, size=26):
    return T(text, size, color)


def left_of(mob, x, y):
    return mob.move_to([x, y, 0]).align_to([x, 0, 0], LEFT)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(center, size=0.3, color=RED, w=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-size, -size, 0], c + [size, size, 0], color=color, stroke_width=w),
                  Line(c + [-size, size, 0], c + [size, -size, 0], color=color, stroke_width=w))


def pbadge(size=0.2):
    c = Circle(radius=size, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22, BG, weight=BOLD).move_to(c))


def normal_final(cx, tint_cr=True):
    """the finished normal cortex, rebuilt in the same place."""
    cr = VGroup(*[neuron(cx + LA[i], Y_CR, YELLOW if tint_cr else ORANGE) for i in (0, 2, 4)])
    late = wave(cx, LA, Y_LATE, GREEN)
    early = wave(cx, LB, Y_EARLY, BLUE)
    sub = wave(cx, LSUB, Y_SUB, ORANGE)
    return cr, late, early, sub


class S00Title(TitleCard):
    LESSON = "Reelin and the reeler mouse"
    TITLE = "One missing protein, a cortex built wrong"


# ---------------------------------------------------------------------------------------------
class S01Reeler(SpokenScene):
    def construct(self):
        # the walk
        path = ParametricFunction(lambda t: np.array([-6.0 + 4.8 * t, 1.3 + 0.8 * np.sin(2 * PI * 3 * t), 0]),
                                  t_range=[0, 1, 0.01], color=GREY, stroke_width=5)
        mouse = Dot([-6.0, 1.3, 0], radius=0.28, color=TEXT)
        walk_lbl = lab("a mouse that reels as it walks", TEXT, 28).move_to([-3.6, -0.3, 0])
        self.at("reels from side")
        self.play(Create(path), MoveAlongPath(mouse, path), run_time=2.4, rate_func=linear)
        self.play(FadeIn(walk_lbl), run_time=0.4)

        cb = chip("small cerebellum", GREY, 28).move_to([-3.6, -1.4, 0])
        self.at("cerebellum")
        self.play(FadeIn(cb, shift=UP * 0.2), run_time=0.5)

        # two cortex stacks
        def stack(cx, order):
            bands = VGroup()
            for k, col in enumerate(order):
                r = Rectangle(width=2.4, height=1.5, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.5)
                r.move_to([cx, 3.0 - 0.75 - 1.5 * k, 0])
                bands.add(r)
            return bands
        st_n = stack(1.5, [GREEN, BLUE, ORANGE])
        st_r = stack(4.9, [ORANGE, BLUE, GREEN])
        for b, dx in zip(st_r, (0.1, -0.08, 0.06)):
            b.shift(RIGHT * dx)
        ln = lab("normal cortex", GREY, 26).move_to([1.5, -1.95, 0])
        lr = lab("reeler cortex", RED, 26).move_to([4.9, -1.95, 0])
        self.at("cerebral cortex")
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in st_n], lag_ratio=0.25), FadeIn(ln), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in st_r], lag_ratio=0.25), FadeIn(lr), run_time=1.0)
        q = T("?", 64, RED, weight=BOLD).move_to([3.2, 0.75, 0])
        self.at("Why would")
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.play(Indicate(q, color=RED, scale_factor=1.25), run_time=0.7)

        prot = chip("one missing protein", YELLOW, 30).move_to([0.0, -3.05, 0])
        a1 = arr([-1.6, -2.85, 0], [-3.5, -1.95, 0], YELLOW)
        a2 = arr([1.6, -2.85, 0], [3.0, -2.35, 0], YELLOW)
        self.at("One missing protein")
        self.play(FadeIn(prot, shift=UP * 0.2), run_time=0.6)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Waves(SpokenScene):
    def construct(self):
        cx = -3.9
        sl = slab(cx)
        vz_lbl = lab("ventricular zone", GREY, 26)
        left_of(vz_lbl, -1.2, -2.58)
        self.at("Neurons leave")
        self.play(FadeIn(sl), FadeIn(vz_lbl), run_time=0.6)

        pre = wave(cx, LA, Y_START, ORANGE)
        self.play(FadeIn(pre, scale=0.5), run_time=0.5)
        self.at("climb toward")
        self.play(pre.animate.shift(UP * (2.1 - Y_START)), run_time=1.6)
        status = left_of(lab("first neurons: a thin sheet", ORANGE, 26), -1.2, 2.1)
        self.at("thin sheet")
        self.play(FadeIn(status, shift=LEFT * 0.2), run_time=0.4)

        blue = wave(cx, LB, Y_START, BLUE)
        st2 = left_of(lab("the next wave enters the sheet", BLUE, 26), -1.2, 2.1)
        self.at("The next ones")
        self.play(FadeIn(blue, scale=0.5), run_time=0.4)
        self.play(blue.animate.shift(UP * (2.1 - Y_START)), ReplacementTransform(status, st2), run_time=1.5)

        # split: upper orange rises, lower orange drops, blue settles
        st3 = left_of(lab("the sheet splits in two", GREY, 26), -1.2, 1.1)
        self.at("split it in two")
        up = VGroup(*[pre[i] for i in (0, 2, 4)])
        down = [pre[i] for i in (1, 3, 5)]
        self.play(*[m.animate.set_y(Y_CR) for m in up],
                  *[d.animate.move_to([cx + x, Y_SUB, 0]) for d, x in zip(down, LSUB)],
                  blue.animate.set_y(Y_EARLY), ReplacementTransform(st2, st3), run_time=1.6)

        band = Rectangle(width=SL_W, height=0.55, stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.08).move_to([cx, TOP - 0.275, 0])
        mz = left_of(lab("marginal zone: Cajal-Retzius cells", YELLOW, 26), -1.2, Y_CR)
        self.at("marginal zone")
        self.play(FadeOut(st3), FadeIn(band), FadeIn(mz), run_time=0.6)
        self.at("holds")
        self.play(*[m.animate.set_stroke(YELLOW).set_fill(YELLOW, 0.65) for m in up], run_time=0.6)

        green = wave(cx, LA, Y_START, GREEN)
        self.at("Each new wave")
        self.play(FadeIn(green, scale=0.5), run_time=0.4)
        self.play(green.animate.shift(UP * (Y_LATE - Y_START)), run_time=2.0)
        l_deep = left_of(lab("early-born: deep", BLUE, 26), -1.2, Y_EARLY)
        l_sup = left_of(lab("late-born: superficial", GREEN, 26), -1.2, Y_LATE)
        self.at("end up deep")
        self.play(FadeIn(l_deep, shift=LEFT * 0.2), Indicate(blue, color=BLUE, scale_factor=1.12), run_time=0.8)
        self.at("end up superficial")
        self.play(FadeIn(l_sup, shift=LEFT * 0.2), Indicate(green, color=GREEN, scale_factor=1.12), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Inverted(SpokenScene):
    def construct(self):
        cxn, cxr = -3.9, 3.9
        sn, sr = slab(cxn), slab(cxr)
        cr, late, early, sub = normal_final(cxn)
        ln = lab("normal", GREY, 26).move_to([cxn, -3.2, 0])
        lr = lab("reeler", RED, 26).move_to([cxr, -3.2, 0])
        self.add(sn, cr, late, early, sub, ln)
        self.add(sr)
        self.play(FadeIn(lr), run_time=0.5)

        c1 = chip("wrong neurons?", GREY, 26).move_to([0, 0.9, 0])
        c2 = chip("wrong place?", GREY, 26).move_to([0, -0.5, 0])
        self.at("wrong neurons")
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.5)
        self.at("wrong place")
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.5)

        # legend: the birth schedule
        keys = []
        for k, (col, name) in enumerate([(ORANGE, "born first"), (BLUE, "born next"), (GREEN, "born last")]):
            d = neuron(-1.2, 1.5 - 0.9 * k, col)
            t = left_of(lab(name, col, 26), -0.9, 1.5 - 0.9 * k)
            keys.append(VGroup(d, t))
        # reeler: the waves rise
        r1 = wave(cxr, LA, Y_START, ORANGE)
        r2 = wave(cxr, LB, Y_START, BLUE)
        r3 = wave(cxr, LA, Y_START, GREEN)
        rng = np.random.RandomState(3)
        for g in (r1, r2, r3):
            for m in g:
                m.jit = rng.uniform(-0.1, 0.1)
        self.at("showed the same")
        self.play(FadeOut(c1), FadeOut(c2), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(k, shift=RIGHT * 0.2) for k in keys], lag_ratio=0.6), FadeIn(r1, scale=0.5), run_time=1.2)
        self.at("same schedule")
        self.play(*[m.animate.set_y(2.3 + m.jit) for m in r1], FadeIn(r2, scale=0.5), run_time=1.0)
        self.play(*[m.animate.set_y(1.2 + m.jit) for m in r2], run_time=1.0)

        self.at("near the surface")
        self.play(Indicate(r1, color=ORANGE, scale_factor=1.15), Indicate(keys[0], color=ORANGE, scale_factor=1.1), run_time=1.0)
        self.at("neurons deep")
        self.play(FadeIn(r3, scale=0.5), run_time=0.25)
        self.play(*[m.animate.set_y(0.1 + m.jit) for m in r3], Indicate(keys[2], color=GREEN, scale_factor=1.1), run_time=1.0)

        nosplit = chip("no split", RED, 26).move_to([0, 2.3, 0])
        self.at("fails to split")
        self.play(FadeIn(nosplit, shift=UP * 0.2), Indicate(r1, color=RED, scale_factor=1.1), run_time=0.7)
        bar1 = Line([cxr - 2.1, 1.74, 0], [cxr + 2.1, 1.74, 0], color=RED, stroke_width=7)
        bar2 = Line([cxr - 2.1, 0.64, 0], [cxr + 2.1, 0.64, 0], color=RED, stroke_width=7)
        self.at("stops beneath")
        self.play(Create(bar1), run_time=0.4)
        self.play(Create(bar2), run_time=0.4)

        self.at("cannot get past")
        self.play(r3.animate.shift(UP * 0.35), r2.animate.shift(UP * 0.35), run_time=0.35)
        self.play(r3.animate.shift(DOWN * 0.35), r2.animate.shift(DOWN * 0.35), run_time=0.35)
        self.play(r3.animate.shift(UP * 0.35), r2.animate.shift(UP * 0.35), run_time=0.35)
        self.play(r3.animate.shift(DOWN * 0.35), r2.animate.shift(DOWN * 0.35), run_time=0.35)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Pathway(SpokenScene):
    def construct(self):
        mem = RoundedRectangle(corner_radius=0.1, width=11.0, height=0.34, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.35).move_to([0.5, 0.2, 0])
        mem_in = lab("inside the neuron", GREY, 24).move_to([-4.4, -0.6, 0])
        mem_out = lab("outside", GREY, 24).move_to([-4.9, 0.8, 0])
        rec1 = RoundedRectangle(corner_radius=0.2, width=0.6, height=1.7, stroke_color=TEAL, stroke_width=4,
                                fill_color=TEAL, fill_opacity=0.3).move_to([-1.9, 0.2, 0])
        rec2 = rec1.copy().move_to([1.9, 0.2, 0])
        # the cell that makes Reelin (for the receptor beat)
        crc = Circle(radius=0.5, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.3).move_to([-4.2, 2.7, 0])
        crc_lbl = left_of(lab("Cajal-Retzius cell", YELLOW, 26), -3.5, 2.7)

        # the finished cortex from the waves scene, rebuilt in the same place
        cx = -3.9
        sl = slab(cx)
        cr, late, early, sub = normal_final(cx)
        band = Rectangle(width=SL_W, height=0.55, stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW,
                         fill_opacity=0.08).move_to([cx, TOP - 0.275, 0])
        ctx = VGroup(sl, band, cr, late, early, sub)
        cr_lbl = left_of(lab("Cajal-Retzius cells", YELLOW, 28), -1.2, Y_CR)
        self.play(FadeIn(ctx), FadeIn(cr_lbl), run_time=0.6)

        reelin = chip("Reelin", YELLOW, 30).move_to([cx, Y_CR, 0])
        reelin_lbl = left_of(lab("a very large secreted protein", YELLOW, 26), 1.0, 1.3)
        self.at("very large")
        self.play(FadeIn(reelin, scale=0.6), run_time=0.4)
        self.play(reelin.animate.move_to([-0.15, 1.3, 0]), FadeIn(reelin_lbl), run_time=0.9)

        top_lbl = left_of(lab("made at the top of the cortex", YELLOW, 26), 1.0, 1.3)
        stop_arr = arr([cx + 2.5, -1.0, 0], [cx + 2.5, Y_LATE, 0], GREEN)
        self.at("top of the cortex")
        self.play(ReplacementTransform(reelin_lbl, top_lbl), Indicate(band, color=YELLOW, scale_factor=1.05),
                  Indicate(cr, color=YELLOW, scale_factor=1.2), run_time=0.8)
        self.play(GrowArrow(stop_arr), Indicate(late, color=GREEN, scale_factor=1.12), run_time=0.9)

        self.at("binds two")
        self.play(FadeOut(ctx), FadeOut(cr_lbl), FadeOut(top_lbl), FadeOut(stop_arr), run_time=0.4)
        self.play(FadeIn(crc), FadeIn(crc_lbl), FadeIn(mem), FadeIn(mem_out), FadeIn(mem_in), FadeIn(rec1), FadeIn(rec2),
                  reelin.animate.move_to([0.0, 1.0, 0]), run_time=0.5)
        lbl1 = lab("ApoER2", TEAL, 26).move_to([-1.9, 1.5, 0])
        lbl2 = lab("VLDLR", TEAL, 26).move_to([1.9, 1.5, 0])
        b1 = Line(reelin.get_left(), [-1.6, 0.9, 0], color=YELLOW, stroke_width=5)
        b2 = Line(reelin.get_right(), [1.6, 0.9, 0], color=YELLOW, stroke_width=5)
        self.play(Create(b1), Create(b2), run_time=0.2)
        self.at("lipoprotein receptors")
        self.play(Indicate(rec1, color=TEAL, scale_factor=1.15), Indicate(rec2, color=TEAL, scale_factor=1.15), run_time=0.8)
        self.play(FadeIn(lbl1, shift=DOWN * 0.1), run_time=0.4)
        self.wait(0.3)
        self.play(FadeIn(lbl2, shift=DOWN * 0.1), run_time=0.4)

        dab = chip("Dab1", PURPLE, 30).move_to([0.0, -1.3, 0])
        t1 = Line([-1.9, -0.65, 0], dab.get_left() + [0.0, 0.0, 0], color=PURPLE, stroke_width=4)
        t2 = Line([1.9, -0.65, 0], dab.get_right() + [0.0, 0.0, 0], color=PURPLE, stroke_width=4)
        self.at("Inside the neuron")
        self.play(Indicate(mem_in, color=TEXT, scale_factor=1.1), FadeIn(dab, shift=UP * 0.2), Create(t1), Create(t2), run_time=0.9)
        kin = chip("Fyn and Src", PINK, 28).move_to([0.0, -3.0, 0])
        ar = arr([0.0, -2.55, 0], [0.0, -1.85, 0], PINK)
        self.at("neuron, the")
        self.play(FadeIn(kin, shift=UP * 0.2), run_time=0.5)
        self.play(GrowArrow(ar), run_time=0.4)
        pb = pbadge().move_to(dab.get_corner(UR) + [0.05, 0.05, 0])
        self.at("add a phosphate")
        self.play(FadeIn(pb, scale=0.4), run_time=0.5)
        self.play(Indicate(dab, color=GOLD, scale_factor=1.12), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def dim(c, o=0.35):
    return [c[0].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[1].animate.set_opacity(o)]


def undim(c):
    return [c[0].animate.set_stroke(opacity=1).set_fill(opacity=0.16), c[1].animate.set_opacity(1)]


class S05Relay(SpokenScene):
    def construct(self):
        names = [("Reelin", YELLOW), ("two receptors", TEAL), ("Fyn and Src", PINK), ("Dab1", PURPLE), ("cortex layers", TEXT)]
        ys = [2.7, 1.35, 0.0, -1.35, -2.7]
        cx = -3.6
        chips = [chip(n, c, 30, pad=0.2).move_to([cx, y, 0]) for (n, c), y in zip(names, ys)]
        arrows = [arr(chips[i].get_bottom(), chips[i + 1].get_top(), GREY, w=4, tip=0.18) for i in range(4)]
        baton = Dot(chips[0].get_left() + [-0.45, 0, 0], radius=0.17, color=TEXT)
        baton.set_z_index(5)

        def cx_(i):
            return np.array([cx - 1.25, ys[i], 0])

        def case_lbl(text, i):
            return left_of(T(text, 34, RED), -1.1, ys[i])

        def result(text, col=RED):
            return left_of(T(text, 34, col), -1.1, ys[4])

        # starts at once: the narrator is already saying "relay race"
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in chips], lag_ratio=0.12), run_time=0.55)
        self.play(*[GrowArrow(a) for a in arrows], FadeIn(baton, scale=0.5), run_time=0.25)
        self.play(baton.animate.move_to(cx_(0)), run_time=0.15)
        x1 = cross(chips[1].get_center())
        self.at("remove any runner")
        self.play(baton.animate.move_to(cx_(1)), run_time=0.3)
        self.play(Create(x1), *dim(chips[1]), run_time=0.4)
        qm = left_of(T("the baton never arrives", 30, GREY), -1.1, ys[4])
        self.play(FadeIn(qm, shift=UP * 0.1), run_time=0.4)

        # case 1: no Reelin
        x_reelin = cross(chips[0].get_center())
        case1 = case_lbl("reeler: no Reelin", 0)
        self.at("mice lack")
        self.play(FadeOut(x1), *undim(chips[1]), FadeOut(qm), baton.animate.move_to(cx_(0)), FadeIn(case1), run_time=0.4)
        self.play(Create(x_reelin), *dim(chips[0]), run_time=0.3)
        res1 = result("cortex like reeler")
        self.play(FadeIn(res1, shift=UP * 0.1), run_time=0.3)

        # case 2: no Dab1
        x_dab = cross(chips[3].get_center())
        case2 = case_lbl("no Dab1", 3)
        self.at("Mice without")
        self.play(FadeOut(x_reelin), *undim(chips[0]), FadeOut(res1), FadeOut(case1), FadeIn(case2), Create(x_dab), *dim(chips[3]),
                  run_time=0.5)
        res2 = result("cortex like reeler")
        self.at("look the same")
        self.play(FadeIn(res2, shift=UP * 0.1), run_time=0.3)

        # case 3: no receptors
        x_rec = cross(chips[1].get_center())
        case3 = case_lbl("no receptors", 1)
        self.at("both receptors")
        self.play(FadeOut(x_dab), *undim(chips[3]), FadeOut(res2), FadeOut(case2), FadeIn(case3), Create(x_rec), *dim(chips[1]),
                  run_time=0.5)
        res3 = result("cortex like reeler")
        self.play(FadeIn(res3, shift=UP * 0.1), run_time=0.3)

        # matching mutants do not give the order; biochemistry does

        base_y = -2.5
        scale_h = 3.6

        def bar(x, h, col, op):
            r = Rectangle(width=1.3, height=h * scale_h, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=op)
            r.move_to([x, base_y + h * scale_h / 2, 0])
            return r
        axis = Line([-6.0, base_y, 0], [6.0, base_y, 0], color=GREY, stroke_width=3)
        xs = [-4.6, -3.0, 1.8, 3.4]
        b_n1 = bar(xs[0], 0.5, PURPLE, 0.25)
        b_r1 = bar(xs[1], 0.5, PURPLE, 0.7)
        b_n2 = bar(xs[2], 0.5, PURPLE, 0.25)
        b_r2 = bar(xs[3], 0.5, PURPLE, 0.7)
        g1 = lab("Dab1 protein", PURPLE, 30).move_to([-3.8, 2.3, 0])
        g2 = lab("phosphorylated Dab1", PURPLE, 30).move_to([2.6, 2.3, 0])
        ln1 = lab("normal", GREY, 26).move_to([xs[0], base_y - 0.4, 0])
        ln2 = lab("no Reelin", RED, 26).move_to([xs[1], base_y - 0.4, 0])
        ln3 = lab("normal", GREY, 26).move_to([xs[2], base_y - 0.4, 0])
        ln4 = lab("no Reelin", RED, 26).move_to([xs[3], base_y - 0.4, 0])
        self.at("Matching mutants")
        clear = VGroup(*chips, *arrows, x_rec, case3, res3, baton)
        self.play(FadeOut(clear), run_time=0.5)
        self.play(Create(axis), FadeIn(g1), FadeIn(g2), run_time=0.6)
        self.at("biochemistry did")
        self.play(FadeIn(VGroup(b_n1, b_r1, b_n2, b_r2)), FadeIn(VGroup(ln1, ln2, ln3, ln4)), run_time=0.8)
        self.at("Brains without")
        self.play(b_r1.animate.stretch_to_fit_height(0.85 * scale_h).move_to([xs[1], base_y + 0.85 * scale_h / 2, 0]), run_time=0.9)
        self.at("held more")
        self.play(b_r2.animate.stretch_to_fit_height(0.2 * scale_h).move_to([xs[3], base_y + 0.2 * scale_h / 2, 0]), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Open(SpokenScene):
    def construct(self):
        centers = [-4.3, 0.0, 4.3]
        PY, PH = 0.55, 4.7
        panels = []
        for cx in centers:
            p = RoundedRectangle(corner_radius=0.2, width=3.7, height=PH, stroke_color=GREY, stroke_width=2.5).move_to([cx, PY, 0])
            band = Rectangle(width=3.5, height=0.5, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=0.3).move_to([cx, 2.6, 0])
            fiber = Line([cx - 0.9, -1.5, 0], [cx - 0.9, 2.15, 0], color=GREY, stroke_width=4)
            panels.append(VGroup(p, band, fiber))

        def cell(x, y):
            d = Circle(radius=0.28, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5).move_to([x, y, 0])
            lp = Line([x, y + 0.28, 0], [x, y + 0.75, 0], color=BLUE, stroke_width=4)
            return VGroup(d, lp)

        t1 = lab("stop here", TEXT, 30).move_to([centers[0], -2.3, 0])
        t2 = lab("let go of the fiber", TEXT, 30).move_to([centers[1], -2.3, 0])
        t3 = lab("come toward me", TEXT, 30).move_to([centers[2], -2.3, 0])
        yellow_tag = left_of(lab("Reelin", YELLOW, 24), -6.2, 3.35)

        n1 = cell(centers[0] - 0.9, -1.0)
        self.at("what does it tell")
        self.play(*[FadeIn(pp) for pp in panels], FadeIn(n1), FadeIn(yellow_tag), run_time=0.8)

        self.at("stop here")
        self.play(FadeIn(t1), n1.animate.shift(UP * 2.5), run_time=1.0)
        stopbar = Line([centers[0] - 1.4, 2.15, 0], [centers[0] - 0.4, 2.15, 0], color=RED, stroke_width=7)
        self.play(Create(stopbar), run_time=0.2)

        n2 = cell(centers[1] - 0.9, 1.0)
        self.at("let go of")
        self.play(FadeIn(t2), FadeIn(n2), run_time=0.4)
        self.play(n2.animate.shift(RIGHT * 1.0 + UP * 0.3), run_time=0.9)

        spot = Circle(radius=0.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.7).move_to([centers[2] + 1.0, 1.5, 0])
        n3 = cell(centers[2] - 0.9, -0.2)
        self.at("come toward")
        spot_lbl = lab("Reelin source", YELLOW, 22).move_to([centers[2] + 0.85, 2.1, 0])
        self.play(FadeIn(t3), FadeIn(n3), FadeIn(spot, scale=0.5), FadeIn(spot_lbl), run_time=0.4)
        n3.remove(n3[1])
        tip = Line([centers[2] - 0.9, 0.08, 0], [centers[2] + 0.7, 1.4, 0], color=BLUE, stroke_width=4)
        self.play(FadeOut(n3[0:0]), Create(tip), run_time=0.9)

        qs = VGroup(*[T("?", 44, RED, weight=BOLD).move_to([cx + 1.4, -1.35, 0]) for cx in centers])
        self.at("point different ways")
        self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in qs], lag_ratio=0.2), run_time=0.8)

        p1 = T("a missing signal shows only that it is needed,", 26, TEXT)
        p2 = T("not what it says", 26, RED)
        g = VGroup(p1, p2).arrange(RIGHT, buff=0.18).move_to([0, -3.1, 0])
        self.at("A missing signal")
        self.play(FadeIn(p1, shift=UP * 0.1), run_time=0.6)
        self.at("not what it says")
        self.play(FadeIn(p2, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "A missing signal shows only that it's needed, not what it says."
