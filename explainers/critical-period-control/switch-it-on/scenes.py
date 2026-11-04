"""Switch It On with a Drug (chapter 2 of "Opening and closing a critical period")

COLOR MAP (one color per concept, shared with every chapter of this lesson)
  BLUE   = the closed eye and the cortex response to it
  ORANGE = the open eye and the cortex response to it
  YELLOW = inhibition (GABA, inhibitory terminals, basket cells)
  PURPLE = the GAD enzymes that make GABA
  PINK   = the GABA receptor
  TEAL   = diazepam
  GREEN  = the open window (plasticity possible)
  RED    = missing or blocked: the knockout, "never opened", "gone"
  GREY   = structure, frames, labels
  TEXT   = neutral marks (current, pyramidal cells, spikes)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB8"
LGREY = "#C9CFDA"     # brighter grey for labels that must be read


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def eye_open(color):
    return VGroup(Ellipse(width=0.9, height=0.5, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.15),
                  Dot(radius=0.12, color=color))


def eye_shut(color):
    lid = ArcBetweenPoints(LEFT * 0.45, RIGHT * 0.45, angle=-PI / 2.6, stroke_color=color, stroke_width=5)
    lashes = VGroup(*[Line(lid.point_from_proportion(p), lid.point_from_proportion(p) + DOWN * 0.12 + RIGHT * dx,
                           stroke_color=color, stroke_width=3) for p, dx in ((0.2, -0.04), (0.5, 0), (0.8, 0.04))])
    return VGroup(lid, lashes)


def pt(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------------------------------------
# cortex-response panel (two bars: closed eye, open eye)
# ---------------------------------------------------------------------------------------------
BASE = -1.85
BASE_H = 2.2          # height of the "no shift" baseline


def mkbar(x, h, color, w=1.1, base=BASE):
    h = max(h, 0.03)
    return Rectangle(width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to([x, base + h / 2, 0])


class Panel:
    def __init__(self, cx, title, tcolor=TEXT, sub="age P28", subcolor=LGREY, hc=BASE_H, ho=BASE_H,
                 closed=False, ghost=False, tsize=30):
        self.cx = cx
        self.frame = RoundedRectangle(corner_radius=0.2, width=5.4, height=6.9, stroke_color=GREY, stroke_width=2).move_to([cx, -0.1, 0])
        self.title = T(title, tsize, tcolor, weight=BOLD).move_to([cx, 2.85, 0])
        self.sub = T(sub, 26, subcolor).move_to([cx, 2.35, 0])
        self.axlab = T("response to each eye", 26, GREY).move_to([cx, 1.85, 0])
        self.bc = mkbar(cx - 1.0, hc, BLUE)
        self.bo = mkbar(cx + 1.0, ho, ORANGE)
        self.ec = (eye_shut if closed else eye_open)(BLUE).move_to([cx - 1.0, -2.45, 0])
        self.eo = eye_open(ORANGE).move_to([cx + 1.0, -2.45, 0])
        self.lc = T("closed eye", 26, BLUE).move_to([cx - 1.0, -3.05, 0])
        self.lo = T("open eye", 26, ORANGE).move_to([cx + 1.0, -3.05, 0])
        self.bl = DashedLine([cx - 1.9, BASE + BASE_H, 0], [cx + 1.9, BASE + BASE_H, 0], color=TEXT, stroke_width=3, dash_length=0.12)
        parts = [self.frame, self.title, self.sub, self.axlab, self.bc, self.bo, self.ec, self.eo]
        if closed:
            parts += [self.lc, self.lo]
        self.q = T("?", 90, YELLOW, weight=BOLD).move_to([cx, 0.75, 0])
        if ghost:
            self.bc.set_fill(opacity=0.22)
            self.bo.set_fill(opacity=0.22)
            parts.append(self.q)
        else:
            parts.append(self.bl)
        self.everything = VGroup(*parts)

    def close_eye(self):
        self.ec_new = eye_shut(BLUE).move_to(self.ec)
        return AnimationGroup(ReplacementTransform(self.ec, self.ec_new), FadeIn(self.lc), FadeIn(self.lo))

    def ghost_bars(self):
        return [self.bc.animate.set_fill(opacity=0.22), self.bo.animate.set_fill(opacity=0.22), FadeIn(self.q, scale=0.6)]

    def solid_bars(self):
        a = [self.bc.animate.set_fill(opacity=0.85), self.bo.animate.set_fill(opacity=0.85), FadeOut(self.q)]
        if self.bl not in self.everything.submobjects:
            a.append(FadeIn(self.bl))
        return a

    def set_bars(self, hc, ho):
        return [Transform(self.bc, mkbar(self.cx - 1.0, hc, BLUE)), Transform(self.bo, mkbar(self.cx + 1.0, ho, ORANGE))]


def countdown(scene, x0, x1, y, secs, label="think"):
    """A bar that shrinks over the silent pause, so a still frame shows time passing."""
    w = x1 - x0
    bar = Rectangle(width=w, height=0.14, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([x0 + w / 2, y, 0])
    lab = T(label, 26, GOLD).move_to([x0 - 0.95, y, 0])
    scene.add(bar, lab)

    def upd(m, a):
        ww = max(0.02, w * (1 - a))
        m.become(Rectangle(width=ww, height=0.14, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([x0 + ww / 2, y, 0]))
    scene.play(UpdateFromAlphaFunc(bar, upd), run_time=secs, rate_func=linear)


# ---------------------------------------------------------------------------------------------
# inhibitory terminal (scenes 1-3)
# ---------------------------------------------------------------------------------------------
TCY, TW, TH = 0.0, 9.6, 4.8
SITE_Y = TCY - TH / 2
VPOS = [(-4.0, -0.5), (-3.3, -1.3), (-3.3, 0.3), (-2.5, -0.5), (2.5, -0.5), (3.3, 0.3), (3.3, -1.3), (4.0, -0.5)]
G65_POS = (0.0, -1.15)
G67_POS = (-2.6, 1.45)


def terminal():
    body = RoundedRectangle(corner_radius=1.4, width=TW, height=TH, stroke_color=LGREY, stroke_width=5,
                            fill_color=GREY, fill_opacity=0.08).move_to([0, TCY, 0])
    stub = Line([0, TCY + TH / 2, 0], [0, 3.0, 0], color=LGREY, stroke_width=5)
    post = Rectangle(width=11.6, height=0.3, stroke_width=0, fill_color=GREY, fill_opacity=0.55).move_to([0, -2.75, 0])
    site = Line([-1.3, SITE_Y, 0], [1.3, SITE_Y, 0], color=TEXT, stroke_width=9)
    return VGroup(body, stub, post, site)


def term_labels():
    nl = T("inhibitory neuron", 26, LGREY, weight=BOLD).move_to([-3.0, 3.0, 0])
    tl = T("target neuron", 26, LGREY).move_to([0, -3.4, 0])
    return nl, tl


def vesicle(p):
    return Circle(radius=0.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.55).move_to(pt(*p))


def vesicles():
    return VGroup(*[vesicle(p) for p in VPOS])


# ---------------------------------------------------------------------------------------------
# right-hand age timeline (scenes 6, 14, 15, 16)
# ---------------------------------------------------------------------------------------------
def mx(a):
    return 0.95 + (a - 10) * 0.095


MAY = -1.2
M_N, M_K = 1.85, 0.2     # band centres: normal mouse row, knockout row
RCX = 3.6                # centre of the right column


def mini_axis():
    ax = Arrow([0.7, MAY, 0], [6.8, MAY, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    return VGroup(ax, T("age", 26, GREY).move_to([6.5, MAY + 0.35, 0]))


def mini_tick(a, text, color=LGREY):
    return VGroup(Line([mx(a), MAY - 0.12, 0], [mx(a), MAY + 0.12, 0], color=GREY, stroke_width=3),
                  T(text, 26, color).move_to([mx(a), MAY - 0.5, 0]))


def mini_band(a0, a1, y, op=0.55, h=0.8):
    return RoundedRectangle(corner_radius=0.1, width=mx(a1) - mx(a0), height=h, stroke_color=GREEN, stroke_width=3,
                            fill_color=GREEN, fill_opacity=op).move_to([(mx(a0) + mx(a1)) / 2, y, 0])


def mini_labels():
    return (T("normal mouse", 26, TEXT, weight=BOLD).move_to([0.8, M_N + 0.7, 0], aligned_edge=LEFT),
            T("knockout", 26, RED, weight=BOLD).move_to([0.8, M_K + 0.7, 0], aligned_edge=LEFT))


def mini_normal_band():
    b = mini_band(20, 32, M_N)
    return VGroup(b, T("window", 26, GREEN).move_to([mx(32) + 0.15, M_N, 0], aligned_edge=LEFT), mini_tick(28, "P28"))


def never_box():
    """Empty dashed band across P20-P55: the window that never opened."""
    r = RoundedRectangle(corner_radius=0.1, width=mx(55) - mx(20), height=0.8, stroke_color=RED, stroke_width=3)
    r.move_to([(mx(20) + mx(55)) / 2, M_K, 0])
    return DashedVMobject(r, num_dashes=40)


def normal_mini():
    """Faint 'normal mouse at P28' bar pair: the shift every comparison is made against."""
    cx, base = RCX, -0.7
    title = T("normal mouse, P28", 26, LGREY).move_to([cx, 1.75, 0])
    bc = mkbar(cx - 0.95, 0.5, BLUE, w=0.8, base=base).set_fill(opacity=0.55)
    bo = mkbar(cx + 0.95, 1.5, ORANGE, w=0.8, base=base).set_fill(opacity=0.55)
    bl = DashedLine([cx - 1.6, base + 0.9, 0], [cx + 1.6, base + 0.9, 0], color=TEXT, stroke_width=2.5, dash_length=0.12)
    lc = T("closed eye", 26, BLUE).move_to([cx - 0.95, -1.05, 0])
    lo = T("open eye", 26, ORANGE).move_to([cx + 0.95, -1.05, 0])
    sh = T("a shift", 26, TEXT).move_to([cx + 2.35, 0.55, 0])
    return VGroup(title, bc, bo, bl, lc, lo, sh)


# ---------------------------------------------------------------------------------------------
# pyramidal neuron (scenes 24)
# ---------------------------------------------------------------------------------------------
class Pyr:
    def __init__(self, cx, cy, R=1.2, up=2.3, axon=2.7):
        self.cx, self.cy, self.R = cx, cy, R
        self.soma = RegularPolygon(3, radius=R, start_angle=PI / 2, stroke_color=TEXT, stroke_width=4,
                                   fill_color=GREY, fill_opacity=0.3).round_corners(0.3).move_to([cx, cy, 0])
        top = cy + R
        base = cy - R * 0.5
        self.base = base
        d = [Line([cx, top - 0.1, 0], [cx, top + up, 0]),
             Line([cx, top + up * 0.55, 0], [cx - 0.8, top + up * 0.95, 0]),
             Line([cx, top + up * 0.55, 0], [cx + 0.8, top + up * 0.95, 0]),
             Line([cx - R * 0.8, base + 0.1, 0], [cx - R * 0.8 - 1.2, base - 1.0, 0]),
             Line([cx + R * 0.8, base + 0.1, 0], [cx + R * 0.8 + 1.2, base - 1.0, 0])]
        self.dend = VGroup(*d).set_stroke(color=TEXT, width=4)
        self.axon = Line([cx, base, 0], [cx, base - axon, 0], color=TEXT, stroke_width=4)
        self.all = VGroup(self.dend, self.axon, self.soma)

    def edge_pt(self, t):
        """point t of the way down the left edge of the soma (0 = top vertex)."""
        R, cx, cy = self.R, self.cx, self.cy
        a = np.array([cx, cy + R, 0.0])
        b = np.array([cx - R * 0.866, cy - R * 0.5, 0.0])
        return a + (b - a) * t


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Opening and closing a critical period"
    TITLE = "Switch It On with a Drug"


# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    """The question, shown as an inhibitory terminal whose GABA release is blocked."""

    def construct(self):
        t, vs = terminal(), vesicles()
        nl, tl = term_labels()
        self.play(FadeIn(t), FadeIn(vs), FadeIn(nl), FadeIn(tl), run_time=0.5)
        self.at("window")
        chipw = bchip("window", GREEN, 28).move_to([5.3, 3.0, 0])
        self.play(FadeIn(chipw, shift=DOWN * 0.15), run_time=0.4)
        self.at("inhibition")
        lab = T("inhibition", 28, YELLOW).move_to([2.2, 3.5, 0])
        a = arr([0.4, 3.0, 0], [4.15, 3.0, 0], YELLOW, w=6)
        self.play(FadeIn(lab), GrowArrow(a), run_time=0.8)
        self.at("what happens")
        q = T("?", 90, YELLOW, weight=BOLD).move_to([5.95, 0.4, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.4)
        self.at("cannot release")
        self.play(vs[3].animate.move_to([-0.4, -1.85, 0]), vs[4].animate.move_to([0.4, -1.85, 0]), run_time=0.6)
        x = Cross(Square(0.6).move_to([0, SITE_Y, 0]), stroke_color=RED, stroke_width=8)
        self.play(Create(x), run_time=0.4)
        self.at("GABA")
        gl = T("GABA", 26, YELLOW).move_to([-3.3, 0.95, 0])
        self.play(FadeIn(gl), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Enz(SpokenScene):
    """Two enzymes make GABA; GAD65 sits at the release site."""

    def construct(self):
        t, vs = terminal(), vesicles()
        nl, tl = term_labels()
        self.add(t, vs, nl, tl)
        self.play(Indicate(nl, color=YELLOW, scale_factor=1.1), run_time=0.9)
        self.at("make GABA")
        gl = T("GABA", 26, YELLOW).move_to([-3.3, 0.95, 0])
        self.play(Indicate(vs, color=YELLOW, scale_factor=1.1), FadeIn(gl), run_time=0.8)
        g67 = bchip("GAD67", PURPLE, 26).move_to([*G67_POS, 0])
        g65 = bchip("GAD65", PURPLE, 26).move_to([2.8, 1.45, 0])
        self.at("two enzymes")
        self.play(FadeIn(g67, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(g65, shift=DOWN * 0.2), run_time=0.5)
        rest = T("most GABA at rest", 26, PURPLE).move_to([-2.6, 0.9, 0])
        self.play(FadeOut(gl), run_time=0.2)
        self.play(FadeIn(rest), run_time=0.4)
        self.at("one")
        self.play(Indicate(g65, color=PURPLE, scale_factor=1.15), run_time=0.9)
        self.at("sits at")
        site = T("release site", 26, LGREY).move_to([3.0, -1.95, 0])
        sl = Line([1.85, -2.05, 0], [1.4, SITE_Y + 0.05, 0], color=LGREY, stroke_width=2.5)
        self.play(g65.animate.move_to([*G65_POS, 0]), FadeIn(site), Create(sl), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Ko(SpokenScene):
    """GAD65 tops up the supply during strong firing; the knockout cannot."""

    def construct(self):
        t, vs = terminal(), vesicles()
        nl, tl = term_labels()
        g67 = bchip("GAD67", PURPLE, 26).move_to([*G67_POS, 0])
        rest = T("most GABA at rest", 26, PURPLE).move_to([-2.6, 0.9, 0])
        g65 = bchip("GAD65", PURPLE, 26).move_to([*G65_POS, 0])
        self.add(t, vs, nl, tl, g67, rest, g65)

        def spike():
            d = Dot(radius=0.15, color=YELLOW).move_to([0, 3.0, 0])
            self.add(d)
            self.play(d.animate.move_to([0, 2.3, 0]), run_time=0.25, rate_func=linear)
            self.play(FadeOut(d), run_time=0.05)

        SLOTS = [-1.3, -0.65, 0.0, 0.65, 1.3]

        def release(idx, slots):
            moves = [vs[i].animate.move_to([sx, -2.05, 0]) for i, sx in zip(idx, slots)]
            self.play(*moves, run_time=0.5)

        self.at("tops up")
        a1 = arr([-1.1, -1.15, 0], [-2.0, -0.65, 0], PURPLE, w=6)
        a2 = arr([1.1, -1.15, 0], [2.0, -0.65, 0], PURPLE, w=6)
        self.play(Indicate(g65, color=PURPLE, scale_factor=1.12), GrowArrow(a1), GrowArrow(a2), run_time=0.9)
        self.at("fires hard")
        spike()
        spike()
        idx = [3, 4, 2, 5, 1]
        release(idx, SLOTS)
        newv = [vesicle(VPOS[i]) for i in idx]
        n5 = T("5 released", 26, YELLOW).move_to([2.9, -1.95, 0])
        self.play(*[FadeOut(vs[i]) for i in idx], *[FadeIn(n, scale=0.4) for n in newv], FadeIn(n5), run_time=0.5)
        for i, n in zip(idx, newv):
            vs[i] = n
        self.at("knockout lacks")
        x = Cross(Square(0.55).move_to([1.65, -1.15, 0]), stroke_color=RED, stroke_width=7)
        kl = T("knockout", 26, RED, weight=BOLD).move_to([0, -0.35, 0])
        self.play(FadeOut(a1), FadeOut(a2), g65[1].animate.set_stroke(RED), g65[2].animate.set_color(RED),
                  g65.animate.set_opacity(0.55), FadeIn(kl), Create(x), run_time=0.8)
        self.at("working copy")
        spike()
        spike()
        release([3, 4], [-0.35, 0.35])
        n2 = T("2 released", 26, RED, weight=BOLD).move_to([2.9, -1.95, 0])
        less = T("less GABA released", 26, RED, weight=BOLD).move_to([2.2, 1.6, 0])
        self.play(ReplacementTransform(n5, n2), FadeIn(less), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def predict_right_1():
    head = T("Pause and predict", 34, GOLD, weight=BOLD).move_to([RCX, 3.45, 0])
    note = bchip("inhibition quiets neurons", YELLOW, 24, pad=0.14).move_to([RCX, 2.45, 0])
    chips = VGroup(*[bchip(txt, GREY, 24, pad=0.12).move_to([RCX, y, 0]) for txt, y in
                     (("more shift than normal", -1.9), ("the same", -2.65), ("less shift", -3.4))])
    return head, note, chips


class S04Pred(SpokenScene):
    def construct(self):
        pan = Panel(-3.6, "GAD65 knockout", RED, sub="age P28")
        head, note, chips = predict_right_1()
        nm = normal_mini()
        self.play(FadeIn(pan.everything), FadeIn(head), run_time=0.7)
        self.at("inhibition quiets")
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.at("should a")
        self.play(Indicate(pan.title, color=RED, scale_factor=1.08), run_time=0.7)
        self.at("cortex shift")
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in chips], lag_ratio=0.3), run_time=1.2)
        self.at("than normal", lead=0.5)
        self.play(FadeIn(nm), run_time=0.6)
        self.at("one eye closes")
        self.play(pan.close_eye(), *pan.ghost_bars(), run_time=0.9)
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        pan = Panel(-3.6, "GAD65 knockout", RED, sub="age P28", closed=True, ghost=True)
        head, note, chips = predict_right_1()
        nm = normal_mini()
        self.add(pan.everything, head, note, chips, nm)
        countdown(self, 1.75, 6.75, 3.0, 4.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Reveal(SpokenScene):
    def construct(self):
        pan = Panel(-3.6, "GAD65 knockout", RED, sub="age P28", closed=True, ghost=True)
        head, note, chips = predict_right_1()
        nm = normal_mini()
        self.add(pan.everything, head, note, chips, nm)
        self.at("does not shift")
        self.play(FadeOut(head), FadeOut(note), *pan.solid_bars(), run_time=0.7)
        ns = T("no shift", 30, RED, weight=BOLD).move_to([-3.6, 0.95, 0])
        self.at("at all")
        self.play(FadeIn(ns), chips[0].animate.set_opacity(0.3), chips[1].animate.set_opacity(0.3),
                  chips[2][1].animate.set_stroke(GREEN), chips[2][2].animate.set_color(GREEN), run_time=0.6)
        self.at("neurons still respond")
        resp = T("neurons still respond to vision", 28, TEXT).move_to([RCX, 3.3, 0])
        self.play(Indicate(pan.bc, color=BLUE, scale_factor=1.06), Indicate(pan.bo, color=ORANGE, scale_factor=1.06),
                  FadeIn(resp), run_time=1.0)
        self.at("vision")
        self.play(FadeOut(chips), FadeOut(nm), run_time=0.4)
        self.at("what failed")
        la, lk = mini_labels()
        nb = mini_normal_band()
        self.play(FadeOut(resp), Create(mini_axis()), FadeIn(la), FadeIn(lk), FadeIn(nb), run_time=0.7)
        nvb = never_box()
        nw = T("no window", 28, RED, weight=BOLD).move_to([(mx(20) + mx(55)) / 2, M_K, 0])
        self.play(Create(nvb), FadeIn(nw, scale=0.8), run_time=0.6)
        self.at("change")
        credit = T("Hensch, Fagiolini, Stryker\nand colleagues, 1998\nbars schematic", 24, LGREY, line_spacing=0.9).move_to([RCX, -2.7, 0])
        self.play(FadeIn(credit), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
# GABA-A receptor: a ring of five subunits (labelled cartoons, not a structure)
# ---------------------------------------------------------------------------------------------
RING_R, SUB_R = 2.0, 1.05
SUBS = ["gamma", "beta", "alpha", "beta", "alpha"]       # clockwise from the top


def ring(cx, cy):
    parts, centres = [], []
    for i, nm in enumerate(SUBS):
        ang = PI / 2 - i * TAU / 5
        c = np.array([cx + RING_R * np.cos(ang), cy + RING_R * np.sin(ang), 0])
        centres.append(c)
        parts.append(Circle(radius=SUB_R, stroke_color=PINK, stroke_width=4, fill_color=PINK, fill_opacity=0.28).move_to(c))
    pore = Circle(radius=0.38, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([cx, cy, 0])
    return VGroup(*parts, pore), centres


def iface(cx, cy, k, r=2.1):
    """point at the groove between subunit k and subunit k+1 (clockwise), at radius r."""
    ang = PI / 2 - (k + 0.5) * TAU / 5
    return np.array([cx + r * np.cos(ang), cy + r * np.sin(ang), 0])


def gaba_dot(p, r=0.2):
    return Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to(p)


def dz_dot(p):
    return Circle(radius=0.27, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.9).move_to(p)


def subunit_names(cs, which=("alpha", "gamma", "beta")):
    out = VGroup()
    for i, nm in enumerate(SUBS):
        if nm in which:
            out.add(T(nm, 28, TEXT if nm != "beta" else LGREY).move_to(cs[i]))
    return out


def receptor_full(cx, cy, gaba=True, dz=True, names=True):
    rg, cs = ring(cx, cy)
    g = VGroup(rg)
    gd = VGroup(*[gaba_dot(iface(cx, cy, k, 2.0)) for k in (1, 3)])
    dd = dz_dot(iface(cx, cy, 4, 2.15))
    if gaba:
        g.add(gd)
    if dz:
        g.add(dd)
    if names:
        g.add(subunit_names(cs))
    return g, gd, dd


class S08Dz(SpokenScene):
    def construct(self):
        cx, cy = -1.2, 0.0
        rg, cs = ring(cx, cy)
        rl = T("GABA receptor", 30, PINK, weight=BOLD).move_to([4.7, 3.0, 0])
        tgt = cs[1] + (rl.get_left() + LEFT * 0.1 - cs[1]) / np.linalg.norm(rl.get_left() + LEFT * 0.1 - cs[1]) * SUB_R
        lead = Line(rl.get_left() + LEFT * 0.1, tgt, color=PINK, stroke_width=2.5)
        pl = T("chloride channel", 26, LGREY).move_to([cx, -3.4, 0])
        pline = Line([cx, -3.12, 0], [cx, -0.42, 0], color=LGREY, stroke_width=2.5)
        self.play(FadeIn(rg, scale=0.85), FadeIn(rl), Create(lead), FadeIn(pl), Create(pline), run_time=0.8)
        dz = bchip("diazepam", TEAL, 28).move_to([-5.45, 3.05, 0])
        self.at("add")
        self.play(FadeIn(dz, shift=DOWN * 0.2), run_time=0.5)
        # GABA sites: grooves between beta and alpha (k=1 and k=3); diazepam site: alpha and gamma (k=4)
        g1, g2 = iface(cx, cy, 1, 2.0), iface(cx, cy, 3, 2.0)
        gd = VGroup(gaba_dot(g1), gaba_dot(g2))
        gl = VGroup(T("GABA", 26, YELLOW).move_to([3.4, -0.9, 0]), T("GABA", 26, YELLOW).move_to([-5.7, -0.9, 0]))
        gld = VGroup(Line([2.6, -0.84, 0], g1 + RIGHT * 0.22, color=YELLOW, stroke_width=2.5),
                     Line([-4.95, -0.84, 0], g2 + LEFT * 0.22, color=YELLOW, stroke_width=2.5))
        self.at("binds")
        site = iface(cx, cy, 4, 2.15)
        dot = dz_dot(site)
        a = arr(dz.get_right() + RIGHT * 0.05, site + np.array([-0.45, 0.3, 0]), TEAL, w=6)
        self.play(GrowArrow(a), FadeIn(dot, scale=0.5), run_time=0.7)
        self.at("receptor")
        self.play(FadeIn(gd), FadeIn(gl), Create(gld), run_time=0.7)
        self.at("alpha")
        al = [T("alpha", 28, TEXT).move_to(cs[2]), T("alpha", 28, TEXT).move_to(cs[4])]
        self.play(FadeIn(al[0]), FadeIn(al[1]), run_time=0.5)
        self.at("gamma")
        gm = T("gamma", 28, TEXT).move_to(cs[0])
        self.play(FadeIn(gm), Indicate(dot, color=TEAL, scale_factor=1.3), run_time=0.7)
        bl = [T("beta", 28, LGREY).move_to(cs[1]), T("beta", 28, LGREY).move_to(cs[3])]
        self.play(FadeIn(bl[0]), FadeIn(bl[1]), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09Mod(SpokenScene):
    def construct(self):
        rec, gd, dd = receptor_full(-1.2, 0.0)
        self.add(rec)
        cx, cy = -3.8, -0.2
        self.play(rec.animate.scale(0.9).move_to([cx, cy, 0]), run_time=0.6)
        rl = T("GABA receptor", 28, PINK, weight=BOLD).move_to([cx, 3.2, 0])
        # chart on the right
        bb = -2.5
        ax = Line([0.7, bb, 0], [6.7, bb, 0], color=GREY, stroke_width=3)
        ay = Line([0.7, bb, 0], [0.7, 3.0, 0], color=GREY, stroke_width=3)
        ttl = T("chloride current", 30, TEXT, weight=BOLD).move_to([3.7, 3.3, 0])
        xs = [1.9, 3.8, 5.7]
        labs = [T("GABA", 26, YELLOW), T("GABA +\ndiazepam", 26, TEAL, line_spacing=0.8), T("diazepam\nalone", 26, TEAL, line_spacing=0.8)]
        for l, x in zip(labs, xs):
            l.move_to([x, bb - 0.55, 0])
        pl = T("chloride channel", 26, LGREY).move_to([cx, -3.45, 0])
        pline = Line([cx, -3.2, 0], [cx, cy - 0.38 * 0.9 - 0.04, 0], color=LGREY, stroke_width=2.5)
        self.play(Create(ax), Create(ay), FadeIn(ttl), FadeIn(rl), FadeIn(pl), Create(pline), run_time=0.5)
        cl = lambda y: pt(cx, cy + y)
        thin = arr(cl(0.8), cl(-0.8), TEXT, w=3, tip=0.18)
        thick = arr(cl(0.88), cl(-0.88), TEXT, w=12, tip=0.4)
        b1 = mkbar(xs[0], 1.5, TEXT, w=1.3, base=bb).set_fill(opacity=0.8)
        b2 = mkbar(xs[1], 4.2, TEXT, w=1.3, base=bb).set_fill(opacity=0.8)
        self.at("respond")
        self.play(GrowArrow(thin), GrowFromEdge(b1, DOWN), FadeIn(labs[0]), run_time=0.4)
        self.at("more strongly")
        self.play(Transform(thin, thick), GrowFromEdge(b2, DOWN), FadeIn(labs[1]), run_time=0.9)
        self.at("cannot open")
        zero = T("no current", 28, RED, weight=BOLD).move_to([xs[2], bb + 0.6, 0])
        self.play(FadeOut(gd), FadeOut(thin), FadeIn(labs[2]), run_time=0.5)
        self.at("alone")
        self.play(FadeIn(zero, scale=0.8), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S10Rescue(SpokenScene):
    def construct(self):
        pan = Panel(-4.0, "GAD65 knockout", RED, sub="age P28")
        self.add(pan.everything)
        # Identical small GABA inputs; only diazepam and the current differ.
        def small_receptor(y):
            rg, _ = ring(0, 0)
            gd = gaba_dot(iface(0, 0, 1, 2.0), 0.2)
            rec = VGroup(rg, gd).scale(0.36).move_to([0.8, y, 0])
            return rec
        rec1, rec2 = small_receptor(1.85), small_receptor(-1.1)
        lab1 = T("GABA alone", 26, YELLOW).move_to([0.8, 3.25, 0])
        lab2 = T("same GABA + diazepam", 24, TEAL).move_to([0.8, -2.55, 0])
        cap = T("same small GABA input", 24, YELLOW).move_to([0.8, 0.35, 0])
        thin = arr(pt(0.8, 2.3), pt(0.8, 1.4), TEXT, w=3, tip=0.16)
        thick = arr(pt(0.8, -0.65), pt(0.8, -1.55), TEXT, w=10, tip=0.25)
        bb = 0.0
        ttl = T("chloride current", 26, TEXT, weight=BOLD).move_to([5.1, 3.35, 0])
        bx = [4.4, 6.0]
        bar1 = mkbar(bx[0], 0.7, TEXT, w=1.0, base=bb).set_fill(opacity=0.8)
        bar2 = mkbar(bx[1], 2.4, TEXT, w=1.0, base=bb).set_fill(opacity=0.8)
        base_ln = Line([3.7, bb, 0], [6.7, bb, 0], color=GREY, stroke_width=3)
        l1 = T("GABA\nalone", 26, YELLOW, line_spacing=0.8).move_to([bx[0], bb - 0.65, 0])
        l2 = T("with\ndiazepam", 26, TEAL, line_spacing=0.8).move_to([bx[1], bb - 0.65, 0])
        self.add(rec1, lab1, thin, ttl, base_ln, bar1, l1)
        dotp = dz_dot(rec2[0][-1].get_center() + iface(0, 0, 4, 2.15) * 0.36).scale(0.7)
        self.at("amplifies")
        self.play(FadeIn(rec2), FadeIn(dotp), FadeIn(lab2), FadeIn(cap),
                  GrowArrow(thick), GrowFromEdge(bar2, DOWN), FadeIn(l2), run_time=0.65)
        self.at("still releases")
        self.play(Indicate(rec1[1], color=YELLOW, scale_factor=1.2),
                  Indicate(rec2[1], color=YELLOW, scale_factor=1.2), run_time=0.4)
        inf = T("infused into the\nvisual cortex", 26, TEAL, line_spacing=0.85).move_to([4.5, -2.2, 0])
        self.at("given during", lead=1.3)
        self.play(FadeIn(inf), pan.close_eye(), *pan.set_bars(0.7, 2.6), run_time=0.55)
        ok = T("shift restored", 30, GREEN, weight=BOLD).move_to([3.4, -3.3, 0])
        self.at("restored")
        self.play(FadeIn(ok, scale=0.8), run_time=0.5)
        self.at("shift")
        self.play(Indicate(pan.bo, color=ORANGE, scale_factor=1.05), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S12Not(SpokenScene):
    def construct(self):
        left = Panel(-3.55, "both eyes open", sub="+ diazepam", subcolor=TEAL)
        right = Panel(3.55, "one eye closed", sub="+ diazepam", subcolor=TEAL, closed=True)
        self.play(FadeIn(left.everything), FadeIn(right.everything), run_time=0.5)
        self.at("drug did")
        ns = T("no shift", 30, RED, weight=BOLD).move_to([-3.55, 0.95, 0])
        self.play(FadeIn(ns), run_time=0.5)
        self.at("itself")
        self.play(Indicate(left.bc, color=BLUE, scale_factor=1.05), Indicate(left.bo, color=ORANGE, scale_factor=1.05), run_time=0.8)
        self.at("the shift went", lead=1.1)
        sh = T("shift toward open eye", 28, ORANGE, weight=BOLD).move_to([3.55, 1.2, 0])
        self.play(*right.set_bars(0.7, 2.6), FadeIn(sh), run_time=0.6)
        self.at("stayed open")
        self.play(Indicate(right.bo, color=ORANGE, scale_factor=1.08), Indicate(right.eo, color=ORANGE, scale_factor=1.3), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S13Perm(SpokenScene):
    def construct(self):
        gx, gy = -3.6, 0.5
        frame = Rectangle(width=2.4, height=4.4, stroke_color=LGREY, stroke_width=5).move_to([gx, gy, 0])
        door = Rectangle(width=2.2, height=4.2, stroke_width=0, fill_color=YELLOW, fill_opacity=0.55).move_to([gx, gy, 0])
        lab = T("inhibition", 34, YELLOW, weight=BOLD).move_to([gx, 3.35, 0])
        stub = arr([-6.5, gy, 0], [-5.15, gy, 0], GREEN, w=8)
        self.play(FadeIn(frame), FadeIn(door), FadeIn(lab), FadeIn(stub), run_time=0.6)
        self.at("permissive")
        full = arr([-6.5, gy, 0], [-0.9, gy, 0], GREEN, w=8)
        opened = Rectangle(width=2.2, height=0.9, stroke_width=0, fill_color=YELLOW, fill_opacity=0.55).move_to([gx, gy + 2.1 - 0.45 + 0.0, 0])
        perm = T("permissive", 34, YELLOW, weight=BOLD).move_to([gx, -2.4, 0])
        pl = T("plasticity", 26, GREEN).move_to([0.6, gy, 0])
        self.play(Transform(door, opened), Transform(stub, full), FadeIn(perm), FadeIn(pl), run_time=1.0)
        self.at("difference between")
        bb = -1.0
        bc, bo = mkbar(2.9, 2.2, BLUE, base=bb), mkbar(5.1, 2.2, ORANGE, base=bb)
        ec, eo = eye_shut(BLUE).move_to([2.9, -2.3, 0]), eye_open(ORANGE).move_to([5.1, -2.3, 0])
        lc, lo = T("closed eye", 26, BLUE).move_to([2.9, -3.0, 0]), T("open eye", 26, ORANGE).move_to([5.1, -3.0, 0])
        self.play(FadeIn(bc), FadeIn(bo), FadeIn(ec), FadeIn(eo), FadeIn(lc), FadeIn(lo), run_time=0.8)
        self.at("instructive")
        ins = T("instructive", 34, TEXT, weight=BOLD).move_to([4.0, 3.35, 0])
        ins2 = T("chooses the direction", 26, LGREY).move_to([4.0, 2.75, 0])
        a1, a2 = arr([2.9, -1.85, 0], [2.9, -1.15, 0], BLUE, w=5), arr([5.1, -1.85, 0], [5.1, -1.15, 0], ORANGE, w=5)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(ins), FadeIn(ins2), run_time=0.5)
        self.play(Transform(bc, mkbar(2.9, 0.8, BLUE, base=bb)), Transform(bo, mkbar(5.1, 3.2, ORANGE, base=bb)), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def k_pieces():
    la, lk = mini_labels()
    ax = mini_axis()
    tick60 = mini_tick(60, "P60", RED)
    guide60 = DashedLine([mx(60), MAY + 0.12, 0], [mx(60), M_K - 0.4, 0], color=RED, stroke_width=3, dash_length=0.1)
    dzchip = bchip("diazepam", TEAL, 26, pad=0.12).move_to([mx(60) - 0.75, -0.65, 0])
    dzblock = Rectangle(width=0.3, height=0.8, stroke_width=0, fill_color=TEAL, fill_opacity=0.9).move_to([mx(60), M_K, 0])
    return la, lk, ax, tick60, guide60, dzchip, dzblock


def answer_row():
    # Choices belong to the response card, spatially separate from the age axis.
    cap = T("does the cortex shift?", 26, LGREY).move_to([-3.6, 1.3, 0])
    chips = VGroup(bchip("shift", GREY, 26, pad=0.14).move_to([-4.7, 0.65, 0]),
                   bchip("no shift", GREY, 26, pad=0.14).move_to([-2.5, 0.65, 0]))
    return cap, chips


class S14Pred(SpokenScene):
    def construct(self):
        pan = Panel(-3.6, "GAD65 knockout", RED, sub="age P60")
        head = T("Pause and predict", 34, GOLD, weight=BOLD).move_to([RCX, 3.45, 0])
        la, lk, ax, tick60, guide60, dzchip, dzblock = k_pieces()
        self.play(FadeIn(pan.everything), FadeIn(head), Create(ax), run_time=0.8)
        self.at("raise a")
        self.play(FadeIn(lk), run_time=0.4)
        self.at("day")
        self.play(FadeIn(tick60, scale=0.6), Create(guide60), run_time=0.6)
        self.at("long past")
        self.play(FadeIn(la), run_time=0.4)
        nb = mini_normal_band()
        self.at("normal window")
        self.play(GrowFromEdge(nb, LEFT), run_time=0.7)
        self.at("give diazepam")
        sub2 = T("age P60 + diazepam", 26, TEAL).move_to(pan.sub)
        self.play(FadeIn(dzchip, shift=UP * 0.15), FadeIn(dzblock), ReplacementTransform(pan.sub, sub2), run_time=0.6)
        cap, chips = answer_row()
        self.at("close one eye")
        pan.q.move_to([-3.6, -0.75, 0])
        self.play(pan.close_eye(), *pan.ghost_bars(), FadeIn(cap), FadeIn(chips), run_time=0.9)
        self.finish()


def s14_frame():
    pan = Panel(-3.6, "GAD65 knockout", RED, sub="age P60 + diazepam", subcolor=TEAL, closed=True, ghost=True)
    pan.q.move_to([-3.6, -0.75, 0])
    la, lk, ax, tick60, guide60, dzchip, dzblock = k_pieces()
    nb = mini_normal_band()
    return pan, [pan.everything, ax, la, lk, tick60, guide60, nb, dzchip, dzblock]


class S15Pause(NarratedScene):
    def construct(self):
        pan, items = s14_frame()
        head = T("Pause and predict", 34, GOLD, weight=BOLD).move_to([RCX, 3.45, 0])
        cap, chips = answer_row()
        self.add(*items, head, cap, chips)
        countdown(self, 1.9, 6.7, 3.0, 4.9)
        self.finish()


class S16Reveal(SpokenScene):
    def construct(self):
        pan, items = s14_frame()
        cap, chips = answer_row()
        self.add(*items, cap, chips)
        self.at("shifts")
        self.play(*pan.solid_bars(), chips[0][1].animate.set_stroke(GREEN), chips[0][2].animate.set_color(GREEN),
                  chips[1].animate.set_opacity(0.3), run_time=0.3)
        self.play(FadeOut(cap), FadeOut(chips), run_time=0.2)
        self.play(*pan.set_bars(0.8, 3.2), run_time=0.7)
        self.at("capacity")
        nvb = never_box()
        nv = T("never opened", 26, RED, weight=BOLD).move_to([(mx(20) + mx(55)) / 2, M_K, 0])
        self.play(Create(nvb), FadeIn(nv), run_time=0.8)
        self.at("adulthood")
        band = mini_band(63, 70, M_K)
        wl = T("window", 26, GREEN).move_to([(mx(63) + mx(70)) / 2, M_K + 0.7, 0])
        self.play(GrowFromEdge(band, LEFT), FadeIn(wl), run_time=0.8)
        credit = T("Fagiolini and Hensch, 2000\nbars and bands schematic", 24, LGREY, line_spacing=0.9).move_to([RCX, -2.7, 0])
        self.at("age had")
        self.play(FadeIn(credit), run_time=0.4)
        self.at("never opened")
        self.play(Indicate(nv, color=RED, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# full-width age timeline (scenes 17-19): row labels live in a left gutter, items to the right
# ---------------------------------------------------------------------------------------------
def fx(a):
    return -4.3 + (a - 10) * 0.35


FAY = -2.7
YA_CHIP, YA_USUAL, YA_EARLY, YA_GUT = 3.3, 2.55, 1.6, 2.1     # group A rows (final positions)
YW, YD = 0.15, -1.0                                            # group B lanes: window, diazepam


def full_axis():
    ax = Arrow([fx(10) - 0.2, FAY, 0], [6.8, FAY, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    g = VGroup(ax, T("age", 26, GREY).move_to([6.4, FAY + 0.4, 0]))
    for a, col in ((15, TEAL), (28, BLUE)):
        g.add(Line([fx(a), FAY - 0.14, 0], [fx(a), FAY + 0.14, 0], color=col, stroke_width=5))
        g.add(T(f"P{a}", 26, col).move_to([fx(a), FAY - 0.55, 0]))
    return g


def full_band(a0, a1, y, h=0.8, op=0.55):
    return RoundedRectangle(corner_radius=0.1, width=fx(a1) - fx(a0), height=h, stroke_color=GREEN, stroke_width=3,
                            fill_color=GREEN, fill_opacity=op).move_to([(fx(a0) + fx(a1)) / 2, y, 0])


def block(x0, x1, y, color, h=0.8, op=0.9):
    return RoundedRectangle(corner_radius=0.08, width=x1 - x0, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=op).move_to([(x0 + x1) / 2, y, 0])


def gutter(text, y, color=TEXT):
    return T(text, 26, color, weight=BOLD, line_spacing=0.8).move_to([-5.65, y, 0])


def a_pieces(dy, name="normal\nmouse"):
    chip = bchip("diazepam", TEAL, 26).move_to([fx(15) + 1.35, YA_CHIP + dy, 0])
    arrow = arr([fx(15), YA_CHIP + dy - 0.05, 0], [fx(15), YA_EARLY + dy + 0.45, 0], TEAL, w=7)
    usual = DashedVMobject(RoundedRectangle(corner_radius=0.1, width=fx(32) - fx(20), height=0.55, stroke_color=LGREY, stroke_width=3)
                           .move_to([(fx(20) + fx(32)) / 2, YA_USUAL + dy, 0]), num_dashes=44)
    ul = T("usual window", 26, LGREY).move_to([fx(32) + 0.15, YA_USUAL + dy, 0], aligned_edge=LEFT)
    early = full_band(15, 25, YA_EARLY + dy)
    el = T("window", 26, TEXT, weight=BOLD).move_to(early)
    sch = T("schematic", 26, GREY).move_to([fx(25) + 0.2, YA_EARLY + dy, 0], aligned_edge=LEFT)
    gut = gutter(name, YA_GUT + dy)
    return dict(chip=chip, arrow=arrow, usual=usual, ul=ul, early=early, el=el, sch=sch, gut=gut)


def b_pieces():
    gb = gutter("second\ngroup", (YW + YD) / 2)
    ey = eye_open(GREY).move_to([fx(11.5), YD, 0])
    eyl = T("eye opening", 26, LGREY).move_to([fx(11.5), YD - 0.65, 0])
    blk = block(fx(15), fx(17), YD, TEAL)
    tl = T("two days of diazepam", 26, TEAL).move_to([fx(15) + 0.05, YD - 0.65, 0], aligned_edge=LEFT)
    es = eye_shut(BLUE).move_to([fx(28), YD, 0])
    dl = T("one eye closed", 26, BLUE).move_to([fx(28) + 0.65, YD, 0], aligned_edge=LEFT)
    return dict(gb=gb, ey=ey, eyl=eyl, blk=blk, tl=tl, es=es, dl=dl)


class S17Early(SpokenScene):
    def construct(self):
        dy = -1.2
        axis = full_axis()
        A = a_pieces(dy)
        self.play(Create(axis), run_time=0.3)
        chipd = A["chip"]
        chipd.move_to([fx(40), YA_CHIP + dy, 0])
        self.at("diazepam")
        self.play(FadeIn(chipd, shift=DOWN * 0.15), run_time=0.5)
        self.at("normal mouse")
        self.play(FadeIn(A["gut"]), run_time=0.4)
        self.at("day")
        self.play(chipd.animate.move_to([fx(15) + 1.35, YA_CHIP + dy, 0]), run_time=0.6)
        self.play(GrowArrow(A["arrow"]), run_time=0.5)
        self.at("before its", lead=0.3)
        self.play(Create(A["usual"]), FadeIn(A["ul"]), run_time=0.7)
        self.at("shifts early")
        self.play(GrowFromEdge(A["early"], LEFT), run_time=0.9)
        self.play(FadeIn(A["el"]), FadeIn(A["sch"]), run_time=0.3)
        self.finish()


class S18Late(SpokenScene):
    def construct(self):
        dy = -1.2
        axis = full_axis()
        A0 = a_pieces(dy)
        self.add(axis, *A0.values())
        A1 = a_pieces(0, "first\ngroup")
        B = b_pieces()
        self.play(*[Transform(A0[k], A1[k].set_opacity(0.25)) for k in A0], run_time=0.5)
        A0["gut"].become(A1["gut"].set_opacity(0.25))
        self.at("second group")
        self.play(FadeIn(B["gb"]), run_time=0.4)
        self.at("two days")
        self.play(GrowFromEdge(B["blk"], LEFT), FadeIn(B["tl"]), run_time=0.7)
        self.at("after eye opening")
        self.play(FadeIn(B["ey"]), FadeIn(B["eyl"]), run_time=0.6)
        self.at("then close")
        self.play(FadeIn(B["es"], scale=0.7), FadeIn(B["dl"]), run_time=0.6)
        self.at("day")
        self.play(Indicate(axis[-1], color=BLUE, scale_factor=1.3), run_time=0.5)
        self.finish()


def s18_items():
    axis = full_axis()
    A = a_pieces(0, "first\ngroup")
    B = b_pieces()
    for m in A.values():
        m.set_opacity(0.25)
    return axis, A, B


class S19Gone(SpokenScene):
    def construct(self):
        axis, A, B = s18_items()
        self.add(axis, *A.values(), *B.values())
        self.at("much less")
        bx0, bx1, bb = fx(28) - 0.4, fx(28) + 0.4, -0.25
        b1 = mkbar(bx0, 0.45, BLUE, w=0.7, base=bb)
        b2 = mkbar(bx1, 0.75, ORANGE, w=0.7, base=bb)
        bl = DashedLine([bx0 - 0.5, bb + 0.6, 0], [bx1 + 0.5, bb + 0.6, 0], color=TEXT, stroke_width=2.5, dash_length=0.1)
        lab = T("little shift\nleft", 26, TEXT, weight=BOLD, line_spacing=0.85).move_to([5.55, 0.95, 0])
        lab2 = T("response to\neach eye", 24, GREY, line_spacing=0.85).move_to([5.55, -0.1, 0])
        self.play(GrowFromEdge(b1, DOWN), GrowFromEdge(b2, DOWN), Create(bl), FadeIn(lab), FadeIn(lab2), run_time=0.8)
        self.at("window opened")
        band = full_band(15, 25, YW)
        self.play(GrowFromEdge(band, LEFT), run_time=0.9)
        self.at("was gone")
        self.play(band.animate.set_fill(opacity=0.15).set_stroke(opacity=0.5), run_time=0.5)
        gone = T("gone", 28, RED, weight=BOLD).move_to([fx(25), YW + 0.7, 0])
        end_tick = Line([fx(25), YW + 0.45, 0], [fx(25), YW - 0.45, 0], color=RED, stroke_width=4)
        self.at("day")
        self.play(FadeIn(gone, scale=0.8), Create(end_tick), run_time=0.5)
        cr = T("Iwai and colleagues, 2003\nschematic", 24, LGREY, line_spacing=0.85).move_to([4.7, -3.35, 0])
        self.play(FadeIn(cr), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
# lanes (scenes 20-21)
# ---------------------------------------------------------------------------------------------
LX0, LX1 = -3.6, 5.2
LY_P, LY_D, LY_E, LAY = 1.9, 0.2, -1.5, -2.7
WIN_END = 3.9


def lane_axis():
    ax = Arrow([LX0 - 0.4, LAY, 0], [LX1 + 0.5, LAY, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    return VGroup(ax, T("time", 26, GREY).move_to([6.1, LAY + 0.4, 0]))


def lane_label(text, y, color):
    return T(text, 26, color).move_to([-6.5, y, 0], aligned_edge=LEFT)


def lane_rail(y, h=0.9):
    return DashedVMobject(RoundedRectangle(corner_radius=0.1, width=LX1 - LX0, height=h, stroke_color=GREY, stroke_width=2)
                          .move_to([(LX0 + LX1) / 2, y, 0]), num_dashes=60).set_opacity(0.45)


def lane_bar(x0, x1, y, color, op=0.6, h=0.9):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=op).move_to([(x0 + x1) / 2, y, 0])


def closes_later():
    t = T("closes later", 26, GREEN).move_to([WIN_END - 0.2, 2.85, 0])
    tick = Line([WIN_END, 2.62, 0], [WIN_END, LY_P + 0.5, 0], color=GREEN, stroke_width=3)
    return VGroup(t, tick)


class S20Ko2(SpokenScene):
    def construct(self):
        ttl = T("GAD65 knockout", 32, RED, weight=BOLD).move_to([0, 3.35, 0])
        dl = lane_label("diazepam", LY_D, TEAL)
        el = lane_label("deprivation", LY_E, BLUE)
        pl = lane_label("window", LY_P, GREEN)
        rails = VGroup(lane_rail(LY_P, 1.0), lane_rail(LY_D), lane_rail(LY_E))
        self.play(FadeIn(ttl), Create(lane_axis()), FadeIn(rails), FadeIn(dl), FadeIn(el), FadeIn(pl), run_time=0.9)
        self.at("two days")
        dz = lane_bar(LX0 + 0.2, LX0 + 0.8, LY_D, TEAL, op=0.9)
        dd = T("two days", 26, TEAL).move_to([LX0 + 0.5, LY_D + 0.75, 0])
        self.play(GrowFromEdge(dz, LEFT), FadeIn(dd), run_time=0.7)
        self.at("near the start")
        dep = lane_bar(LX0 + 1.4, LX1 - 0.2, LY_E, BLUE, op=0.35)
        stopped = T("drug stopped", 26, TEAL).move_to([LX0 + 1.0, LY_D, 0], aligned_edge=LEFT)
        self.play(GrowFromEdge(dep, LEFT), FadeIn(stopped), run_time=1.0)
        self.at("switched")
        band = lane_bar(LX0 + 0.8, WIN_END, LY_P, GREEN, op=0.6, h=1.0)
        txt = T("fully on", 30, TEXT, weight=BOLD).move_to(band)
        self.play(GrowFromEdge(band, LEFT), run_time=1.0)
        self.at("fully")
        self.play(FadeIn(txt), FadeIn(closes_later()), run_time=0.4)
        self.finish()


class S21Rule(SpokenScene):
    def construct(self):
        ttl = T("young cortex", 32, TEXT, weight=BOLD).move_to([0, 3.35, 0])
        dep = lane_bar(LX0 + 1.4, LX1 - 0.2, LY_E, BLUE, op=0.35)
        el = lane_label("deprivation", LY_E, BLUE)
        dl = lane_label("brief boost", LY_D, TEAL)
        pl = lane_label("window", LY_P, GREEN)
        rails = VGroup(lane_rail(LY_P, 1.0), lane_rail(LY_D), lane_rail(LY_E))
        self.add(ttl, lane_axis(), rails, dep, el, dl, pl)
        boost = lane_bar(LX0 + 0.2, LX0 + 0.8, LY_D, TEAL, op=0.9)
        self.at("brief boost")
        self.play(GrowFromEdge(boost, LEFT), run_time=0.7)
        band = lane_bar(LX0 + 0.8, WIN_END, LY_P, GREEN, op=0.6, h=1.0)
        self.at("start a window")
        self.play(GrowFromEdge(band, LEFT), FadeIn(closes_later()), run_time=0.7)
        gone = T("drug stopped", 26, TEAL).move_to([LX0 + 1.0, LY_D, 0], aligned_edge=LEFT)
        self.at("without having")
        self.play(FadeIn(gone), run_time=0.5)
        note = T("drug not needed during deprivation", 28, TEXT).move_to([-0.3, -3.4, 0])
        self.at("present")
        self.play(FadeIn(note), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S23Paradox(SpokenScene):
    def construct(self):
        bb = -2.7
        bi = mkbar(-2.8, 4.0, YELLOW, w=2.4, base=bb)
        bp = mkbar(2.8, 4.0, GREEN, w=2.4, base=bb)
        li = T("inhibition", 32, YELLOW, weight=BOLD).move_to([-2.8, bb - 0.5, 0])
        lp = T("plasticity", 32, GREEN, weight=BOLD).move_to([2.8, bb - 0.5, 0])
        ar = arr([-1.3, -0.7, 0], [1.3, -0.7, 0], GREY, w=8)
        self.play(FadeIn(bi), FadeIn(bp), FadeIn(li), FadeIn(lp), GrowArrow(ar), run_time=0.9)
        qt = T("less inhibition, less plasticity?", 42, TEXT, weight=BOLD).move_to([0, 3.3, 0])
        self.at("why would")
        self.play(FadeIn(qt, shift=DOWN * 0.15), Indicate(bi, color=YELLOW, scale_factor=1.03), run_time=0.6)
        self.at("less inhibition")
        self.play(Transform(bi, mkbar(-2.8, 1.0, YELLOW, w=2.4, base=bb)), run_time=0.7)
        q = T("?", 120, YELLOW, weight=BOLD).move_to([0, 0.8, 0])
        self.at("make a cortex")
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.at("harder")
        self.play(Transform(bp, mkbar(2.8, 1.0, GREEN, w=2.4, base=bb)), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S24Basket(SpokenScene):
    def construct(self):
        P = Pyr(1.2, -0.3, R=1.3, up=1.7, axon=2.0)
        pn = T("pyramidal neuron", 28, TEXT, weight=BOLD).move_to([4.7, 2.1, 0])
        pn_lead = Line([2.95, 2.1, 0], [2.0, 2.0, 0], color=TEXT, stroke_width=2.5)
        self.play(Create(P.dend), Create(P.axon), FadeIn(P.soma), FadeIn(pn), Create(pn_lead), run_time=1.6)
        # basket cell, left
        bcc = np.array([-4.8, -0.6, 0.0])
        bc = Circle(radius=0.8, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.3).move_to(bcc)
        bl = T("basket cell", 28, YELLOW, weight=BOLD).move_to([-4.8, -1.75, 0])
        self.at("basket cells")
        self.play(FadeIn(bc, scale=0.6), FadeIn(bl), run_time=0.7)
        ax_y0 = P.base
        sites = [P.edge_pt(0.18), P.edge_pt(0.42), P.edge_pt(0.66), P.edge_pt(0.9),
                 pt(1.2, ax_y0 - 0.45), pt(1.2, ax_y0 - 1.05), P.dend[3].point_from_proportion(0.4)]
        lines = VGroup(*[Line(bcc + (s - bcc) / np.linalg.norm(s - bcc) * 0.8, s, color=YELLOW, stroke_width=3) for s in sites])
        bout = VGroup(*[Circle(radius=0.17, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.95).move_to(s) for s in sites])
        self.at("their synapses")
        self.play(Create(lines), run_time=0.7)
        self.at("cluster")
        self.play(LaggedStart(*[FadeIn(b, scale=0.3) for b in bout], lag_ratio=0.12), run_time=0.8)
        self.at("cell bodies")
        sp = Circle(radius=0.22, stroke_color=TEXT, stroke_width=4).move_to([1.2, ax_y0 - 1.75, 0])
        spl = T("spike starts here", 26, TEXT).move_to([1.7, ax_y0 - 1.75, 0], aligned_edge=LEFT)
        ctl = T("strong control over\nwhether and when\nthe cell fires", 28, TEXT, line_spacing=0.85).move_to([5.0, 0.5, 0])
        self.play(Indicate(P.soma, color=TEXT, scale_factor=1.12), Create(sp), FadeIn(spl), FadeIn(ctl), run_time=0.7)
        self.at("pyramidal neurons")
        self.play(Indicate(pn, color=TEXT, scale_factor=1.12), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S25Timing(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(7)
        rows, events = 9, [-3.6, 0.0, 3.6]
        u = np.clip(rng.normal(0, 1, (rows, 3)), -1.7, 1.7)
        y0 = 2.45

        def ticks(sigma):
            g = VGroup()
            for r in range(rows):
                for e, ev in enumerate(events):
                    x = ev + sigma * u[r, e]
                    g.add(Line([x, y0 - r * 0.42 - 0.14, 0], [x, y0 - r * 0.42 + 0.14, 0], color=TEXT, stroke_width=5))
            return g

        loose, tight = ticks(0.95), ticks(0.11)
        axis = Arrow([-6.2, -1.3, 0], [6.4, -1.3, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
        tl = T("time", 26, GREY).move_to([6.0, -0.9, 0])
        head = T("pyramidal cells, each row one cell", 26, TEXT).move_to([0, 3.6, 0])
        evm = VGroup(*[VGroup(Triangle(color=GOLD, fill_color=GOLD, fill_opacity=0.9, stroke_width=1).scale(0.14).rotate(PI).move_to([ev, 3.05, 0]),
                              DashedLine([ev, 2.9, 0], [ev, -1.3, 0], color=GOLD, stroke_width=2, dash_length=0.1).set_opacity(0.35)) for ev in events])
        evl = T("repeating event", 26, GOLD).move_to([-1.8, 3.1, 0])
        self.play(Create(axis), FadeIn(tl), FadeIn(head), FadeIn(evm), FadeIn(evl), run_time=0.5)
        self.play(FadeIn(loose, lag_ratio=0.01), run_time=1.0)

        def ybar(h):
            return Rectangle(width=1.3, height=h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.85).move_to([-5.15, -3.55 + h / 2, 0])
        yl = T("inhibition matures", 28, YELLOW, weight=BOLD).move_to([-4.2, -2.6, 0], aligned_edge=LEFT)
        yb = ybar(0.15)
        self.at("maturing")
        self.play(FadeIn(yl), FadeIn(yb), run_time=0.4)
        self.play(Transform(yb, ybar(1.0)), run_time=1.0)
        self.at("sharpens")
        self.play(Transform(loose, tight), Transform(yb, ybar(1.8)), run_time=1.5)
        self.at("fire")
        done = T("tight, well-timed firing", 34, GREEN, weight=BOLD).move_to([2.3, -2.7, 0])
        self.play(FadeIn(done), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S26Compare(SpokenScene):
    def construct(self):
        cell = Pyr(3.4, 0.0, R=2.0, up=0.0, axon=0.0).soma
        cl = T("pyramidal cell", 26, TEXT).move_to([3.4, -2.55, 0])
        eb, eo = eye_shut(BLUE).scale(1.3).move_to([-5.6, -1.6, 0]), eye_open(ORANGE).scale(1.3).move_to([-5.6, 1.6, 0])
        eln_b, eln_o = T("closed eye", 26, BLUE).move_to([-5.6, -2.25, 0]), T("open eye", 26, ORANGE).move_to([-5.6, 0.95, 0])
        start_b, start_o = pt(-4.7, -1.6), pt(-4.7, 1.6)
        end_b, end_o = pt(1.95, -0.6), pt(2.55, 0.5)
        lb = Line(start_b, end_b, color=BLUE, stroke_width=4)
        lo = Line(start_o, end_o, color=ORANGE, stroke_width=4)
        fires = T("cell fires", 26, LGREY).move_to([3.4, 3.35, 0])
        self.play(FadeIn(cell), FadeIn(cl), FadeIn(eb), FadeIn(eo), FadeIn(eln_b), FadeIn(eln_o), Create(lb), Create(lo), FadeIn(fires), run_time=0.7)
        # pulses: the open eye's arrive in a fixed rhythm and the cell fires right after each one;
        # the closed eye's arrive at scattered times and the cell does not follow them.
        T_RUN, TRAVEL = 2.2, 0.4
        open_t = [0.0, 0.8, 1.6]
        closed_t = [0.12, 0.5, 1.05, 1.4, 1.9]
        tr = ValueTracker(0.0)

        def pulse(t0, p0, p1, color):
            d = Dot(radius=0.2, color=color).move_to(p0).set_opacity(0)

            def up(m):
                f = (tr.get_value() - t0) / TRAVEL
                if 0 <= f <= 1:
                    m.move_to(p0 + (p1 - p0) * f).set_opacity(1)
                else:
                    m.set_opacity(0)
            d.add_updater(up)
            return d
        dots = [pulse(t, start_o, end_o, ORANGE) for t in open_t] + [pulse(t, start_b, end_b, BLUE) for t in closed_t]
        ticks = []
        for t in open_t:
            tk = Line([2.45 + (t + TRAVEL) * 0.9, 2.55, 0], [2.45 + (t + TRAVEL) * 0.9, 2.95, 0], color=ORANGE, stroke_width=6).set_opacity(0)

            def tup(m, t=t):
                m.set_opacity(1 if tr.get_value() >= t + TRAVEL else 0)
            tk.add_updater(tup)
            ticks.append(tk)

        def flash(m):
            v = 0.3
            for t in open_t:
                dt = tr.get_value() - (t + TRAVEL)
                if 0 <= dt <= 0.3:
                    v = max(v, 0.3 + 0.5 * (1 - dt / 0.3))
            m.set_fill(opacity=v)
        cell.add_updater(flash)
        self.add(*dots, *ticks)
        lo_l = T("locked to the cell's firing", 26, ORANGE).move_to([-1.4, 2.45, 0])
        lb_l = T("scattered", 26, BLUE).move_to([-1.4, -2.4, 0])
        cap = T("could tell which eye drives the cell", 28, TEXT, weight=BOLD).move_to([-1.0, -3.4, 0])
        self.at("tell")
        self.play(tr.animate.set_value(T_RUN),
                  Succession(Wait(0.8), FadeIn(lo_l, run_time=0.4)),
                  Succession(Wait(1.2), FadeIn(lb_l, run_time=0.4)),
                  Succession(Wait(1.5), FadeIn(cap, run_time=0.5)),
                  run_time=T_RUN, rate_func=linear)
        cell.clear_updaters()
        for m in dots + ticks:
            m.clear_updaters()
        self.finish()


# ---------------------------------------------------------------------------------------------
class S28Hyp(SpokenScene):
    def construct(self):
        cy = 0.0
        c1 = bchip("basket-cell\ninhibition", YELLOW, 30).move_to([-4.1, cy, 0])
        c2 = bchip("sharp\ntiming", TEXT, 30).move_to([0.2, cy, 0])
        c3 = bchip("eyes told\napart", TEXT, 30).move_to([4.3, cy, 0])
        a1, a2 = arr(c1.get_right(), c2.get_left(), GREY, w=5), arr(c2.get_right(), c3.get_left(), GREY, w=5)
        box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=12.4, height=3.0, stroke_color=GOLD, stroke_width=3).move_to([0.05, cy, 0]), num_dashes=90)
        hl = T("hypothesis", 40, GOLD, weight=BOLD).move_to([0, cy + 2.35, 0])
        qs = VGroup(T("?", 48, GOLD, weight=BOLD).move_to([(c1.get_right()[0] + c2.get_left()[0]) / 2, cy + 0.75, 0]),
                    T("?", 48, GOLD, weight=BOLD).move_to([(c2.get_right()[0] + c3.get_left()[0]) / 2, cy + 0.75, 0]))
        chain = VGroup(box, c1, a1, c2, a2, c3, hl)
        self.add(chain)
        self.at("hypothesis")
        self.play(Indicate(hl, color=GOLD, scale_factor=1.15), run_time=0.8)
        self.at("not a settled")
        self.play(FadeIn(qs), run_time=0.5)
        self.at("experiments")
        grp = VGroup(chain, qs)
        self.play(grp.animate.scale(0.55).move_to([0, 2.5, 0]).set_opacity(0.45), run_time=0.8)
        est = T("what the experiments establish: the order", 32, TEXT).move_to([0, 0.85, 0])
        self.play(FadeIn(est), run_time=0.6)
        self.at("inhibition first")
        i1 = bchip("inhibition", YELLOW, 46).move_to([-3.4, -0.15, 0])
        f1 = T("first", 36, YELLOW, weight=BOLD).move_to([-3.4, -1.4, 0])
        self.play(FadeIn(i1, shift=RIGHT * 0.2), FadeIn(f1), run_time=0.6)
        self.at("then plasticity")
        i2 = bchip("plasticity", GREEN, 46).move_to([3.4, -0.15, 0])
        f2 = T("then", 36, GREEN, weight=BOLD).move_to([3.4, -1.4, 0])
        arrow = arr(i1.get_right() + RIGHT * 0.15, i2.get_left() - RIGHT * 0.15, TEXT, w=10)
        self.play(GrowArrow(arrow), run_time=0.5)
        self.play(FadeIn(i2, shift=LEFT * 0.2), FadeIn(f2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S29Take(SpokenScene):
    def construct(self):
        tk = T("Takeaway", 36, GOLD, weight=BOLD).move_to([0, 3.3, 0])
        inh = bchip("inhibition", YELLOW, 38).move_to([-4.3, 0.3, 0])
        arrow = arr([-2.3, 0.3, 0], [1.4, 0.3, 0], GREEN, w=9)
        win = bchip("window opens", GREEN, 38).move_to([4.2, 0.3, 0])
        self.add(tk, inh, arrow, win)
        self.at("inhibition")
        self.play(Indicate(inh, color=YELLOW, scale_factor=1.05), run_time=0.35)
        self.at("window")
        self.play(Indicate(win, color=GREEN, scale_factor=1.05), run_time=0.35)
        self.at("trigger")
        trig = T("trigger", 30, GREEN, weight=BOLD).move_to([-0.5, 0.95, 0])
        perm = T("permits", 30, GREEN).move_to([-0.5, -0.35, 0])
        row1 = VGroup(inh, arrow, win, trig, perm)
        self.play(FadeIn(trig), FadeIn(perm), run_time=0.5)
        self.at("open eye")
        eye = eye_open(ORANGE).scale(1.7).move_to([-4.3, -1.35, 0])
        el = T("open eye", 30, ORANGE).move_to([-4.3, -2.45, 0])
        self.play(row1.animate.shift(UP * 1.55), FadeIn(eye, scale=0.7), FadeIn(el), run_time=0.8)
        self.at("decides")
        a2 = arr([-3.0, -1.35, 0], [1.4, -1.35, 0], ORANGE, w=9)
        ins = T("instructs", 30, ORANGE, weight=BOLD).move_to([-0.8, -0.8, 0])
        bb = -2.6
        bc, bo = mkbar(3.0, 1.4, BLUE, base=bb), mkbar(5.0, 1.4, ORANGE, base=bb)
        lc, lo = T("closed", 26, BLUE).move_to([3.0, bb - 0.4, 0]), T("open", 26, ORANGE).move_to([5.0, bb - 0.4, 0])
        baseline = Line([2.2, bb, 0], [5.8, bb, 0], color=GREY, stroke_width=3)
        reference = DashedLine([2.2, bb + 1.4, 0], [5.8, bb + 1.4, 0], color=TEXT, stroke_width=2, dash_length=0.1)
        self.play(Create(baseline), Create(reference), GrowArrow(a2), FadeIn(ins), FadeIn(bc), FadeIn(bo), FadeIn(lc), FadeIn(lo), run_time=0.8)
        self.at("shifts")
        self.play(Transform(bc, mkbar(3.0, 0.5, BLUE, base=bb)), Transform(bo, mkbar(5.0, 2.7, ORANGE, base=bb)), run_time=0.9)
        self.finish()


class S30End(EndCard):
    LINE = "Inhibition opens the window; the open eye decides which way it shifts."
