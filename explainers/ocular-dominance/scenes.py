"""Ocular dominance and the critical period: the more active eye wins  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole film)
  BLUE   = eye A, the eye that gets closed (the weak eye in amblyopia), and cortical cells only it drives
  YELLOW = eye B, the other eye (the open or good eye), and cortical cells only it drives
  PURPLE   = a cortical cell driven by both eyes
  RED    = abnormal or silent cell; a crossed-out idea
  GOLD   = the critical-period window, small tags ("6 days")
  GREY   = outlines, the cortex, neutral (unmeasured) cells
Histogram bars run from blue (group 1) through teal (group 4) to yellow (group 7).
"""
import numpy as np

PURPLE = "#B58CD9"
from bp_style import *  # noqa: F401,F403

# ------------------------------------------------------------------ helpers
COLS = [-0.2, 1.7, 3.6, 5.5]
ROWS = [1.5, 0.0, -1.5]
CELL = {"B": (BLUE, .55), "Y": (YELLOW, .55), "T": (PURPLE, .55), "R": (RED, .6), "N": (GREY, .05)}
N_NORMAL = "TTBTYTTTTYTB"
N_SHIFT = "YTYYYYTYYYYT"
N_BOTH_A = "TNBTYTTTNYTB"   # both eyes closed, before the odd cells are named
N_BOTH_B = "TRBTYTTTRYTB"   # same, with the abnormal or silent ones
N_NEUTRAL = "N" * 12
EYE_A = np.array([-4.8, 1.5, 0])
EYE_B = np.array([-4.8, -1.5, 0])


def arr(a, b, color=GREY, w=6, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def make_eye(color, scale=1.0):
    ell = Ellipse(width=2.0, height=1.1, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.15)
    pup = Circle(radius=0.3, stroke_width=0, fill_color=color, fill_opacity=1)
    glint = Circle(radius=0.08, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(pup.get_center() + UR * 0.1)
    return VGroup(ell, pup, glint).scale(scale)


def eye_close(g):
    return [g[0].animate.stretch_to_fit_height(g[0].width * 0.07), g[1].animate.set_opacity(0), g[2].animate.set_opacity(0)]


def eye_open(g):
    return [g[0].animate.stretch_to_fit_height(g[0].width * 0.55), g[1].animate.set_opacity(1), g[2].animate.set_opacity(1)]


def make_cells(codes):
    cs = VGroup()
    for i, ch in enumerate(codes):
        r, c = divmod(i, 4)
        col, op = CELL[ch]
        cs.add(Circle(radius=0.4, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=op).move_to([COLS[c], ROWS[r], 0]))
    return cs


def cells_to(cells, codes):
    return [c.animate.set_stroke(CELL[ch][0]).set_fill(CELL[ch][0], CELL[ch][1]) for c, ch in zip(cells, codes)]


def cortex_box():
    return RoundedRectangle(corner_radius=0.3, width=7.4, height=5.5, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.05).move_to([2.5, 0.25, 0])


def legend(red=False, y=-3.15, x=0.4):
    pre = T("cell driven by:", 22, GREY)
    items = [(BLUE, "A only"), (PURPLE, "both"), (YELLOW, "B only")] + ([(RED, "abnormal or silent")] if red else [])
    g = VGroup(pre)
    for col, name in items:
        d = Circle(radius=0.14, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.55)
        g.add(VGroup(d, T(name, 22, col)).arrange(RIGHT, buff=0.12))
    g.arrange(RIGHT, buff=0.45).move_to([x, y, 0])
    return g


class Stage:
    """eyes, arrows, cortex and a 4x3 grid of cells, always in the same place."""

    def __init__(self, codes=N_NORMAL, leg=True, red=False, lab=True, illus=True):
        self.eA = make_eye(BLUE).move_to(EYE_A)
        self.eB = make_eye(YELLOW).move_to(EYE_B)
        self.aA = arr([-3.6, 1.5, 0], [-1.35, 0.8, 0], BLUE, 8)
        self.aB = arr([-3.6, -1.5, 0], [-1.35, -0.8, 0], YELLOW, 8)
        self.box = cortex_box()
        self.cap = T("visual cortex", 24, GREY).move_to([0.4, 2.65, 0])
        self.cells = make_cells(codes)
        self.lA = T("eye A", 24, BLUE).move_to([-4.8, 2.4, 0]) if lab else VGroup()
        self.lB = T("eye B", 24, YELLOW).move_to([-4.8, -2.4, 0]) if lab else VGroup()
        self.leg = legend(red) if leg else VGroup()
        self.ill = T("illustrative counts", 22, GREY).move_to([5.0, -2.8, 0]) if illus else VGroup()
        self.all = VGroup(self.box, self.cap, self.cells, self.aA, self.aB, self.eA, self.eB, self.lA, self.lB, self.leg, self.ill)

    def add(self, scene):
        scene.add(self.all)
        return self


def electrode(cell_idx=1):
    r, c = divmod(cell_idx, 4)
    tip = np.array([COLS[c] + 0.28, ROWS[r] + 0.28, 0])
    return VGroup(Line(tip + np.array([0.75, 1.1, 0]), tip, stroke_width=5, color=TEXT), Dot(tip, radius=0.06, color=TEXT))


def relabel(old, text, color, size=24):
    new = T(text, size, color).move_to(old)
    return AnimationGroup(FadeOut(old), FadeIn(new)), new


# histogram -----------------------------------------------------------------------------------
HX = [(i - 3) * 1.5 for i in range(7)]
BASE = -2.0
H_NORMAL = [3, 6, 10, 12, 9, 5, 2]
H_SHIFT = [0.5, 1, 2, 3, 6, 10, 13]


def gcol(i):
    B, T_, Y = ManimColor(BLUE), ManimColor(PURPLE), ManimColor(YELLOW)
    return interpolate_color(B, T_, i / 3) if i <= 3 else interpolate_color(T_, Y, (i - 3) / 3)


def hbars(h, hx=HX, base=BASE, unit=0.3, bw=1.2):
    out = VGroup()
    for i, v in enumerate(h):
        hh = max(v * unit, 0.03)
        out.add(Rectangle(width=bw, height=hh, stroke_color=gcol(i), stroke_width=2, fill_color=gcol(i),
                          fill_opacity=0.6).move_to([hx[i], base + hh / 2, 0]))
    return out


def hnums(hx=HX, base=BASE, size=26, dy=0.4):
    return VGroup(*[T(str(i + 1), size, TEXT).move_to([hx[i], base - dy, 0]) for i in range(7)])


def hline(hx=HX, base=BASE, pad=0.9):
    return Line([hx[0] - pad, base, 0], [hx[-1] + pad, base, 0], color=GREY, stroke_width=3)


def hist_frame():
    ax = hline()
    nums = hnums()
    yl = T("number of cells", 22, GREY).rotate(PI / 2).move_to([-5.85, -0.2, 0])
    return VGroup(ax, nums, yl)


def tags(a="only one eye", b="only the other eye", mid="both"):
    ta = T(a, 22, BLUE).move_to([HX[0], -3.05, 0])
    tb = T(b, 22, YELLOW).move_to([HX[6], -3.05, 0])
    tm = T(mid, 22, PURPLE).move_to([HX[3], -3.05, 0]) if mid else VGroup()
    return ta, tm, tb


def corner_eyes(closedA=False):
    a = make_eye(BLUE, 0.5).move_to([-5.3, 2.85, 0])
    b = make_eye(YELLOW, 0.5).move_to([5.3, 2.85, 0])
    if closedA:
        a[0].stretch_to_fit_height(a[0].width * 0.07)
        a[1].set_opacity(0)
        a[2].set_opacity(0)
    return a, b


def fade_cap(text, y=3.4, x=2.5, size=28, color=TEXT):
    return T(text, size, color).move_to([x, y, 0])


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Ocular dominance and the critical period"
    TITLE = "The eyes compete for cortex"


class S01Kitten(SpokenScene):
    def construct(self):
        st = Stage()
        self.play(FadeIn(st.all), run_time=1.4)
        self.at("Close one eye")
        lA, nlA = relabel(st.lA, "closed", BLUE)
        self.play(*eye_close(st.eA), st.aA.animate.set_opacity(0.2), lA, run_time=0.8)
        days = chip("6 days", GOLD, size=24).move_to([-4.8, 0.45, 0])
        self.at("days")
        self.play(FadeIn(days, shift=UP * 0.1), run_time=0.4)
        self.at("one at a time")
        el = electrode(1)
        self.play(FadeIn(el, shift=DOWN * 0.2), run_time=0.5)
        self.play(Flash(st.cells[1], color=TEXT, flash_radius=0.6, line_length=0.15), run_time=0.7)
        self.at("closed eye can now drive")
        self.play(*cells_to(st.cells, N_SHIFT), FadeOut(el), run_time=1.6)
        self.at("Now close both eyes")
        # clear the old result first: reopen A, cells back to neutral, then close both
        lB3, nlB3 = relabel(st.lB, "closed", YELLOW)
        self.play(FadeOut(days), *cells_to(st.cells, N_NEUTRAL), run_time=0.6)
        self.play(*eye_close(st.eB), st.aB.animate.set_opacity(0.2), lB3, run_time=0.8)
        self.at("far smaller")
        self.play(*cells_to(st.cells, N_NORMAL), run_time=0.9)
        q = T("?", 80, GOLD, weight=BOLD).move_to([-2.45, 0, 0])
        self.at("Why would")
        self.play(FadeIn(q, scale=1.3), run_time=0.6)
        self.finish()


class S02Scale(SpokenScene):
    def construct(self):
        st = Stage(leg=True).add(self)
        el = electrode(1)
        self.at("fine electrode")
        self.play(FadeIn(el, shift=DOWN * 0.2), run_time=0.5)
        self.at("records its spikes")
        self.play(Flash(st.cells[1], color=TEXT, flash_radius=0.6, line_length=0.15), run_time=0.7)
        bar = Rectangle(width=0.14, height=0.8, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([-6.2, 1.5, 0])
        self.at("bar of light")
        self.play(FadeIn(bar), Indicate(st.aA, color=BLUE, scale_factor=1.15), run_time=0.8)
        self.at("then the other")
        self.play(bar.animate.move_to([-6.2, -1.5, 0]), Indicate(st.aB, color=YELLOW, scale_factor=1.15), run_time=0.9)
        self.play(FadeOut(bar), run_time=0.2)
        # to the histogram
        frame = hist_frame()
        ca, cb = corner_eyes()
        ta, tm, tb = tags()
        self.at("Each cell goes into")
        self.play(FadeOut(VGroup(st.box, st.cap, st.cells, st.aA, st.aB, st.lA, st.lB, st.leg, st.ill, el)),
                  ReplacementTransform(st.eA, ca), ReplacementTransform(st.eB, cb), FadeIn(frame), run_time=1.4)
        samp = VGroup(Circle(radius=0.35, stroke_color=BLUE, fill_color=BLUE, fill_opacity=.55, stroke_width=3).move_to([HX[0], BASE + 0.8, 0]),
                      Circle(radius=0.35, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=.55, stroke_width=3).move_to([HX[3], BASE + 0.8, 0]),
                      Circle(radius=0.35, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=.55, stroke_width=3).move_to([HX[6], BASE + 0.8, 0]))
        self.at("only to one eye")
        self.play(FadeIn(samp[0], scale=0.6), FadeIn(ta), run_time=0.6)
        self.at("only to the other eye")
        self.play(FadeIn(samp[2], scale=0.6), FadeIn(tb), run_time=0.6)
        self.at("about equally to both")
        self.play(FadeIn(samp[1], scale=0.6), FadeIn(tm), run_time=0.6)
        zero = hbars([0] * 7)
        bars = hbars(H_NORMAL)
        self.at("Count the cells")
        self.play(FadeOut(samp), run_time=0.3)
        self.add(zero)
        self.play(Transform(zero, bars), run_time=1.8)
        tops = [[HX[i], BASE + max(v * 0.3, .03) + 0.05, 0] for i, v in enumerate(H_NORMAL)]
        curve = VMobject(color=TEXT, stroke_width=4).set_points_smoothly([np.array(p) for p in tops])
        self.at("a hump")
        self.play(Create(curve), run_time=1.0)
        self.at("middle groups")
        self.play(Indicate(VGroup(zero[2], zero[3], zero[4]), color=PURPLE, scale_factor=1.05), run_time=1.0)
        self.finish()


class S03Shift(SpokenScene):
    def construct(self):
        frame = hist_frame()
        ca, cb = corner_eyes()
        ta, tm, tb = tags()
        bars = hbars(H_NORMAL)
        self.add(frame, ca, cb, ta, tm, tb, bars)
        self.at("shut one eye")
        t1, na = relabel(ta, "closed eye", BLUE)
        t2, nb = relabel(tb, "open eye", YELLOW)
        self.play(*eye_close(ca), t1, t2, run_time=0.8)
        days = chip("6 days", GOLD, size=24).move_to([-3.3, 2.85, 0])
        self.at("days")
        self.play(FadeIn(days, shift=RIGHT * 0.1), run_time=0.4)
        self.at("closed eye can drive")
        self.play(Indicate(na, color=BLUE, scale_factor=1.15), run_time=0.8)
        shifted = hbars(H_SHIFT)
        move = arr([-1.6, 2.2, 0], [1.6, 2.2, 0], TEXT, 6)
        self.at("Most of the histogram")
        self.play(Transform(bars, shifted), GrowArrow(move), run_time=2.2)
        lab = T("shift in ocular dominance", 28, TEXT).move_to([0, 3.0, 0])
        self.at("ocular dominance")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        far = H_SHIFT_FAR = [0.1, 0.3, 0.5, 1, 3, 8, 13]
        m3 = chip("about 3 months from birth", GOLD, size=24).move_to([-2.2, 2.85, 0])
        ret = chip("retina still responds", BLUE, size=24).move_to([2.4, 2.85, 0])
        self.at("from birth")
        self.play(FadeOut(lab), FadeOut(move), FadeOut(days), run_time=0.3)
        self.play(FadeIn(m3, shift=RIGHT * 0.1), Transform(bars, hbars(far)), run_time=1.2)
        self.at("retina")
        self.play(FadeIn(ret, shift=LEFT * 0.1), run_time=0.5)
        self.play(Indicate(VGroup(*ret[1:]), color=BLUE, scale_factor=1.05), run_time=0.8)
        self.finish()


class S04Compete(SpokenScene):
    def construct(self):
        st = Stage(leg=True, red=True)
        st.leg[-1].set_opacity(0)
        st.add(self)
        cap = fade_cap("disuse?", color=GREY)
        self.at("Is this disuse")
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.at("closing both eyes")
        lA, nA = relabel(st.lA, "closed", BLUE)
        lB, nB = relabel(st.lB, "closed", YELLOW)
        self.play(*eye_close(st.eA), *eye_close(st.eB), st.aA.animate.set_opacity(0.2), st.aB.animate.set_opacity(0.2), lA, lB, run_time=0.8)
        cap2 = fade_cap("disuse predicts: large loss of responses", color=GREY)
        self.at("large loss")
        self.play(ReplacementTransform(cap, cap2), *cells_to(st.cells, N_NEUTRAL), run_time=1.2)
        cap3 = fade_cap("what was seen", color=TEXT)
        self.at("It did not")
        self.play(ReplacementTransform(cap2, cap3), run_time=0.5)
        self.at("many cells still answered")
        self.play(*cells_to(st.cells, N_BOTH_A), run_time=1.4)
        self.at("abnormal or silent")
        self.play(*cells_to(st.cells, N_BOTH_B), st.leg[-1].animate.set_opacity(1), run_time=0.8)
        cap4 = fade_cap("one eye closed", color=TEXT)
        # new case: clear the old answer in the same move that names the new case
        self.at("So the open eye")
        self.play(ReplacementTransform(cap3, cap4), *eye_open(st.eB), st.aB.animate.set_opacity(1),
                  *cells_to(st.cells, N_NEUTRAL), st.leg[-1].animate.set_opacity(0), nB.animate.set_opacity(0), run_time=0.8)
        lB2, nB2 = relabel(nB, "open", YELLOW)
        self.play(nB.animate.set_opacity(1), lB2, run_time=0.01)
        self.at("hurts the closed one")
        self.play(*cells_to(st.cells, N_SHIFT), run_time=1.6)
        self.at("compete for the same cortex")
        self.play(Indicate(st.aA, color=BLUE, scale_factor=1.15), Indicate(st.aB, color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.at("takes territory")
        ys = VGroup(*[c for c, ch in zip(st.cells, N_SHIFT) if ch == "Y"])
        self.play(Indicate(ys, color=YELLOW, scale_factor=1.12), run_time=1.2)
        self.finish()


class S05Window(SpokenScene):
    def construct(self):
        # two small histograms
        hx = [(i - 3) * 0.8 for i in range(7)]
        base = -1.2

        def mini(cx, heights):
            sh = np.array([cx, 0, 0])
            bars = hbars(heights, hx=hx, base=base, unit=0.2, bw=0.65).shift(sh)
            ax = hline(hx=hx, base=base, pad=0.5).shift(sh)
            nums = hnums(hx=hx, base=base, size=22, dy=0.35).shift(sh)
            return bars, VGroup(ax, nums)

        kb, kf = mini(-3.3, H_SHIFT)
        ab, af = mini(3.3, H_NORMAL)
        kt = T("young kitten", 30, TEXT).move_to([-3.3, 3.0, 0])
        at_ = T("adult cat", 30, TEXT).move_to([3.3, 3.0, 0])
        ke = make_eye(BLUE, 0.5).move_to([-3.3, 2.15, 0])
        ae = make_eye(BLUE, 0.5).move_to([3.3, 2.15, 0])
        for e in (ke, ae):
            e[0].stretch_to_fit_height(e[0].width * 0.07)
            e[1].set_opacity(0)
            e[2].set_opacity(0)
        kc = T("one eye closed", 24, BLUE).move_to([-3.3, -2.4, 0])
        ac = T("one eye closed, for months", 24, BLUE).move_to([3.3, -2.4, 0])
        an = T("histogram stays normal", 24, PURPLE).move_to([3.3, -3.0, 0])
        self.at("Age matters")
        self.play(FadeIn(kt), FadeIn(ke), FadeIn(kf), FadeIn(kb), FadeIn(kc), run_time=1.0)
        self.at("adult cat")
        self.play(FadeIn(at_), FadeIn(ae), FadeIn(af), FadeIn(ab), run_time=0.8)
        self.at("even for months")
        self.play(FadeIn(ac), run_time=0.4)
        self.at("left the histogram normal")
        self.play(FadeIn(an), run_time=0.5)
        # curve plot
        x0, x1, ybase, ytop = -5.2, 5.4, -2.0, 2.0
        sx = (x1 - x0) / 14.0

        def px(w):
            return x0 + w * sx

        def sens(w):
            s = lambda z: 1 / (1 + np.exp(-z))
            return s((w - 4.0) / 0.35) * (1 - 0.97 * s((w - 9.6) / 0.9))

        ax = VGroup(Line([x0, ybase, 0], [x1, ybase, 0], color=GREY, stroke_width=3),
                    Line([x0, ybase, 0], [x0, ytop + 0.3, 0], color=GREY, stroke_width=3))
        ticks = VGroup(*[T(str(w), 24, TEXT).move_to([px(w), ybase - 0.4, 0]) for w in (2, 4, 6, 8, 10, 12)])
        xl = T("postnatal week", 24, GREY).move_to([px(7), ybase - 0.95, 0])
        yl = T("sensitivity to closure", 24, GREY).rotate(PI / 2).move_to([x0 - 0.5, 0, 0])
        ttl = T("kitten series (schematic)", 26, GREY).move_to([px(7), 3.3, 0])

        def seg(a, b):
            ws = np.linspace(a, b, 60)
            pts = [np.array([px(w), ybase + (ytop - ybase) * sens(w), 0]) for w in ws]
            return VMobject(color=YELLOW, stroke_width=6).set_points_smoothly(pts)

        s1, s2, s3 = seg(1.5, 5.2), seg(5.2, 8.2), seg(8.2, 13.8)
        self.at("In kittens")
        self.play(FadeOut(VGroup(kt, ke, kf, kb, kc, at_, ae, af, ab, ac, an)), run_time=0.5)
        self.play(FadeIn(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl), FadeIn(ttl), run_time=0.6)
        self.at("near the start")
        self.play(Create(s1), run_time=1.0)
        self.at("stayed high")
        self.play(Create(s2), run_time=1.2)
        self.at("declined")
        self.play(Create(s3), run_time=1.6)
        # soft band: opacity ramps up at onset and fades away on the right, no hard edge
        a0, a1 = px(3.6), px(14.0)
        n = 60
        zone = VGroup()
        for i in range(n):
            w = 3.6 + (14.0 - 3.6) * (i + 0.5) / n
            op = 0.16 * min(1.0, (w - 3.6) / 1.4) * (1 - min(1.0, max(0.0, (w - 7.5) / 6.5)))
            zone.add(Rectangle(width=(a1 - a0) / n + 0.01, height=ytop - ybase + 0.1, stroke_width=0, fill_color=GOLD,
                               fill_opacity=op).move_to([a0 + (a1 - a0) * (i + 0.5) / n, (ytop + ybase) / 2 + 0.05, 0]))
        lab = chip("critical or sensitive period", GOLD, size=28).move_to([px(7.5), 2.65, 0])
        self.at("critical period or")
        self.play(FadeIn(zone), FadeIn(lab, shift=DOWN * 0.1), run_time=0.9)
        lab2 = chip("critical: experience essential", GOLD, size=28).move_to([px(7.5), 2.65, 0])
        self.at("Sensitive periods")
        self.play(FadeOut(lab), FadeIn(lab2), run_time=0.6)
        self.finish()


class S06Patch(SpokenScene):
    def construct(self):
        st = Stage(codes=N_NEUTRAL, leg=False, lab=False, illus=False)
        st.aA.become(arr([-3.6, 1.5, 0], [-1.35, 0.8, 0], BLUE, 8))
        self.play(FadeIn(st.all), run_time=1.2)
        self.at("amblyopia")
        weak = T("weak eye", 24, BLUE).move_to([-4.8, 2.4, 0])
        good = T("good eye", 24, YELLOW).move_to([-4.8, -2.4, 0])
        self.at("sees poorly")
        self.play(FadeIn(weak), FadeIn(good), run_time=0.5)
        self.at("unequal input")
        thinA = arr([-3.6, 1.5, 0], [-1.35, 0.8, 0], BLUE, 3).set_opacity(0.5)
        thickB = arr([-3.6, -1.5, 0], [-1.35, -0.8, 0], YELLOW, 13)
        self.play(Transform(st.aA, thinA), Transform(st.aB, thickB), run_time=1.0)
        gl = chip("glasses: no quick fix", RED, size=26).move_to([-2.6, -3.1, 0])
        cross = VGroup(Line([-0.2, -0.2, 0], [0.2, 0.2, 0], color=RED, stroke_width=5),
                       Line([-0.2, 0.2, 0], [0.2, -0.2, 0], color=RED, stroke_width=5)).move_to([-4.35, -3.1, 0])
        self.at("Glasses alone")
        self.play(FadeIn(gl, shift=UP * 0.1), run_time=0.4)
        self.play(Create(cross), run_time=0.5)
        patch = VGroup(RoundedRectangle(corner_radius=0.15, width=1.6, height=1.0, stroke_color=GREY, stroke_width=3,
                                        fill_color="#2a2f3a", fill_opacity=1),
                       Line([-0.45, -0.25, 0], [0.45, 0.25, 0], color=GREY, stroke_width=3),
                       Line([-0.45, 0.25, 0], [0.45, -0.25, 0], color=GREY, stroke_width=3)).move_to(EYE_B)
        self.at("with a patch")
        self.play(FadeOut(gl), FadeOut(cross), FadeIn(patch, scale=1.3), run_time=0.7)
        newA = arr([-3.6, 1.5, 0], [-1.35, 0.8, 0], BLUE, 13)
        newB = arr([-3.6, -1.5, 0], [-1.35, -0.8, 0], YELLOW, 3).set_opacity(0.5)
        act = chip("useful images", BLUE, size=26).move_to([-2.45, 2.55, 0])
        self.at("useful images")
        self.play(Transform(st.aA, newA), Transform(st.aB, newB), FadeIn(act, shift=DOWN * 0.1), run_time=1.2)
        yc = chip("works best in young children", GOLD, size=26).move_to([2.5, -3.1, 0])
        self.at("young children")
        self.play(FadeIn(yc, shift=UP * 0.1), run_time=0.6)
        rule = T("the eyes compete for cortex", 36, TEXT, font=TITLE_FONT).move_to([2.5, 3.42, 0])
        self.at("Keep the rule")
        self.play(FadeIn(rule, shift=DOWN * 0.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "The eyes compete for cortex, most easily when young."
