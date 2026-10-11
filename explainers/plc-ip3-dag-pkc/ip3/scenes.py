"""IP3 is sufficient: the 1983 permeabilized-cell experiment  (Biochemistrypedia section film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole film)
  BLUE   = the hormone (the signal outside)
  PINK   = IP3
  YELLOW = calcium (dots and its chip)
  PURPLE = the internal calcium store (later named the endoplasmic reticulum)
  ORANGE = the mitochondria
  RED    = blocked / ruled out (crosses)
  GREEN  = the result that was shown (IP3 was sufficient)
  GREY   = membranes, channel, labels, structure

No molecular structures: IP3 is a labelled chip, the cell is a rounded outline, compartments are
labelled boxes, the channel is four simple blocks (schematic, marked as such), calcium is a dot.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#F08BB4"
PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

CELL_C = np.array([1.5, -0.35, 0])
HOLE_Y = [0.6, -0.35, -1.3]
HORM_AT = np.array([-4.6, 2.0, 0])
IP3_OUT = np.array([-4.6, -0.35, 0])
MITO_AT = np.array([-0.4, -1.5, 0])
STORE_AT = np.array([3.5, -1.5, 0])


def P(x, y):
    return np.array([x, y, 0.0])


def bchip(text, color=BLUE, size=26, pad=0.2, **kw):
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def cross(center, w=0.5, color=RED, sw=6):
    c = np.array([center[0], center[1], 0.0])
    a = Line(c + P(-w, -w), c + P(w, w), color=color, stroke_width=sw)
    b = Line(c + P(-w, w), c + P(w, -w), color=color, stroke_width=sw)
    return VGroup(a, b)


def strike(center, color=RED, sw=5):
    c = np.array([center[0], center[1], 0.0])
    return Line(c + P(-0.85, -0.3), c + P(0.85, 0.3), color=color, stroke_width=sw)


def pop(m, s=1.15):
    return m.animate(rate_func=there_and_back).scale(s)


def dashed_arrow(a, b, color=GREY, w=3):
    d = DashedLine(a, b, color=color, stroke_width=w, dash_length=0.14, buff=0.0)
    d.add_tip(tip_length=0.2)
    return d


def solid_arrow(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def qbox(center, size=0.9):
    c = np.array([center[0], center[1], 0.0])
    shape = RoundedRectangle(corner_radius=0.14, width=size, height=size)
    back = shape.copy().set_stroke(width=0).set_fill(BG, 1).move_to(c)
    edge = DashedVMobject(shape.copy().move_to(c), num_dashes=24).set_color(GREY)
    q = T("?", 40, TEXT, weight=BOLD).move_to(c)
    return VGroup(back, edge, q)


def cell_wall():
    return RoundedRectangle(corner_radius=0.5, width=7.6, height=4.6, stroke_color=GREY, stroke_width=6,
                            fill_opacity=0).move_to(CELL_C)


def holes():
    return VGroup(*[Rectangle(width=0.34, height=0.46, stroke_width=0, fill_color=BG, fill_opacity=1)
                    .move_to(P(-2.3, y)) for y in HOLE_Y])


def mito():
    return bchip("mitochondria", ORANGE, size=24).move_to(MITO_AT)


def store():
    box = RoundedRectangle(corner_radius=0.2, width=3.0, height=1.1, stroke_color=PURPLE, stroke_width=3,
                           fill_color=PURPLE, fill_opacity=0.2)
    lab = T("internal store", 24, PURPLE)
    return VGroup(box, lab.move_to(box)).move_to(STORE_AT)


def hormone_crossed():
    h = bchip("hormone", BLUE, size=26).move_to(HORM_AT)
    return VGroup(h, strike(HORM_AT)), h


def ca_spots(n=14, seed=5):
    rng = np.random.RandomState(seed)
    return [P(rng.uniform(1.0, 4.9), rng.uniform(-0.2, 1.4)) for _ in range(n)]


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "PLC, IP3, DAG and Protein Kinase C"
    TITLE = "Is IP3 Alone Enough?"


# =============================================================================================
class S01Gap(SpokenScene):
    def construct(self):
        H = bchip("hormone", BLUE, size=28).move_to(P(-5.0, 0.3))
        I = bchip("IP3", PINK, size=30).move_to(P(-0.8, 1.7))
        C = bchip("calcium", YELLOW, size=28).move_to(P(4.6, 1.7))
        QB = qbox((1.9, -1.2), 1.0)
        tag = T("Berridge: blowfly salivary glands", 22, GREY).move_to(P(-3.3, 3.15))
        secs = T("appears within seconds", 22, PINK).move_to(P(-1.6, 2.55))
        mich = T("Michell's proposal", 22, GREY).move_to(P(3.2, 2.45))
        third = T("a third event?", 24, TEXT).next_to(QB, DOWN, buff=0.2)

        a_hi = solid_arrow(H.get_right() + P(0.05, 0.2), I.get_left() + P(-0.05, -0.1), PINK)
        a_ic = dashed_arrow(I.get_right() + P(0.05, 0), C.get_left() + P(-0.05, 0), YELLOW, 4)
        a_hq = dashed_arrow(H.get_right() + P(0.05, -0.25), QB.get_left() + P(-0.05, 0))
        a_qi = dashed_arrow(QB.get_top() + P(-0.2, 0.05), I.get_bottom() + P(0.2, -0.05))
        a_qc = dashed_arrow(QB.get_top() + P(0.2, 0.05), C.get_bottom() + P(-0.2, -0.05))
        q1 = T("?", 36, TEXT, weight=BOLD).move_to(a_ic.get_center() + P(0, -0.4))

        self.at("worked on blowfly")
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.5)
        self.at("showed that")
        self.play(FadeIn(H, shift=RIGHT * 0.2), run_time=0.5)
        self.at("appears within seconds")
        self.play(GrowArrow(a_hi), FadeIn(I, scale=0.6), FadeIn(secs), run_time=0.9)
        self.at("hormone arriving")
        self.play(pop(H, 1.12), run_time=0.7)
        self.at("Eight years earlier")
        self.play(FadeIn(mich, shift=DOWN * 0.1), run_time=0.5)
        self.at("raise calcium")
        self.play(FadeIn(C, scale=0.6), Create(a_ic), run_time=0.9)
        self.play(FadeIn(q1))
        self.at("starts many things")
        self.play(Create(a_hq), FadeIn(QB, scale=0.6), run_time=0.9)
        self.play(Create(a_qi), Create(a_qc), run_time=0.8)
        self.at("third event")
        self.play(FadeIn(third), pop(QB, 1.15), run_time=0.8)
        self.finish()


# =============================================================================================
class S02Open(SpokenScene):
    def construct(self):
        wall, mi, st = cell_wall(), mito(), store()
        hz, h = hormone_crossed()
        ip3 = bchip("IP3", PINK, size=30).move_to(IP3_OUT)
        cap = T("pancreatic acinar cell", 24, GREY).move_to(CELL_C + P(0, -2.75))
        t1 = T("Schulz laboratory, Frankfurt", 22, GREY).move_to(P(2.0, 3.15))
        t2 = T("H. Streb", 22, GREY).move_to(P(2.0, 2.65))
        hl = holes()
        x = cross(P(-2.55, -0.35), 0.28, RED, 7)
        seal = VGroup(SurroundingRectangle(mi, color=ORANGE, buff=0.08, stroke_width=5),
                      SurroundingRectangle(st, color=PURPLE, buff=0.08, stroke_width=5))

        self.at("To test it")
        self.play(Create(wall), FadeIn(cap), run_time=1.0)
        self.play(FadeIn(mi), FadeIn(st), run_time=0.6)
        self.at("inside a cell")
        self.play(FadeIn(ip3, shift=RIGHT * 0.2), run_time=0.5)
        self.at("no hormone")
        self.play(FadeIn(h, scale=0.7), run_time=0.5)
        self.play(Create(hz[1]), run_time=0.5)
        self.at("too charged")
        self.play(ip3.animate.move_to(P(-3.15, -0.35)), run_time=0.7)
        self.at("cross a membrane")
        self.play(Create(x), ip3.animate.move_to(P(-3.5, -0.35)).shift(LEFT * 0.35), run_time=0.5)
        self.wait(0.3)
        self.play(ip3.animate.move_to(IP3_OUT), FadeOut(x), run_time=0.5)
        self.at("has to be opened")
        self.play(FadeIn(hl, scale=1.0), run_time=0.8)
        self.at("laboratory in Frankfurt")
        self.play(FadeIn(t1, shift=DOWN * 0.1), FadeIn(t2, shift=DOWN * 0.1), run_time=0.6)
        self.at("leaky to small molecules")
        self.play(Indicate(hl, color=TEXT, scale_factor=1.4), run_time=0.8)
        self.at("compartments inside")
        self.play(Create(seal), run_time=0.8)
        self.finish()


# =============================================================================================
class S03Add(SpokenScene):
    def construct(self):
        wall, mi, st, hl = cell_wall(), mito(), store(), holes()
        hz, h = hormone_crossed()
        cap = T("pancreatic acinar cell", 24, GREY).move_to(CELL_C + P(0, -2.75))
        ip3 = bchip("IP3", PINK, size=30).move_to(IP3_OUT)
        self.add(wall, mi, st, hl, hz, cap, ip3)
        t1 = T("Robin Irvine, England", 22, GREY).move_to(P(-4.3, 1.05))
        t2 = T("from human red blood cells", 22, GREY).move_to(P(-4.3, 0.6))
        spots = ca_spots()
        dots = [Dot(STORE_AT + P(np.random.RandomState(i).uniform(-1.0, 1.0), 0.15), radius=0.1, color=YELLOW)
                for i in range(len(spots))]
        cal = T("calcium", 24, YELLOW).move_to(P(3.0, 1.62))
        xm = cross(MITO_AT, 0.4, RED, 6)
        notm = T("not the mitochondria", 24, RED).move_to(P(-0.4, -2.2))

        self.at("Robin Irvine")
        self.play(FadeIn(t1, shift=DOWN * 0.1), FadeIn(t2, shift=DOWN * 0.1), run_time=0.7)
        self.at("human red blood cells")
        self.play(pop(ip3, 1.2), run_time=0.7)
        self.at("added to the opened")
        self.play(ip3.animate.move_to(P(-2.3, -0.35)), run_time=0.6)
        self.play(ip3.animate.move_to(P(-0.2, 0.45)), run_time=1.0)
        self.at("No hormone")
        self.play(Indicate(hz[1], color=RED, scale_factor=1.3), run_time=0.8)
        self.at("Calcium came out")
        self.play(FadeIn(cal), *[FadeIn(d) for d in dots], run_time=0.4)
        self.play(*[d.animate.move_to(p) for d, p in zip(dots, spots)], run_time=2.0, lag_ratio=0.05)
        self.at("not the mitochondria")
        self.play(Create(xm), FadeIn(notm), run_time=0.8)
        self.finish()


# =============================================================================================
class S04Channel(SpokenScene):
    def construct(self):
        wall, mi, st, hl = cell_wall(), mito(), store(), holes()
        hz, h = hormone_crossed()
        cap = T("pancreatic acinar cell", 24, GREY).move_to(CELL_C + P(0, -2.75))
        ip3 = bchip("IP3", PINK, size=30).move_to(P(-0.2, 0.45))
        xm = cross(MITO_AT, 0.4, RED, 6)
        notm = T("not the mitochondria", 24, RED).move_to(P(-0.4, -2.2))
        cal = T("calcium", 24, YELLOW).move_to(P(3.0, 1.62))
        spots = ca_spots()
        dots = [Dot(p, radius=0.1, color=YELLOW) for p in spots]
        old = VGroup(wall, mi, st, hl, hz, cap, xm, notm, cal, *dots)
        self.add(old, ip3)

        suff = bchip("IP3 was sufficient", GREEN, size=28).move_to(P(0.0, 3.0))
        self.at("sufficient")
        self.play(FadeIn(suff, scale=0.8), run_time=0.6)

        # --- the new picture: ER band, channel, calcium inside and out
        er = RoundedRectangle(corner_radius=0.25, width=11.0, height=2.2, stroke_color=PURPLE, stroke_width=4,
                              fill_color=PURPLE, fill_opacity=0.2).move_to(P(0, -2.0))
        er_lab = T("endoplasmic reticulum", 26, PURPLE).move_to(P(-2.9, -2.8))
        er_calc = T("free calcium: a thousand times or more", 22, YELLOW).move_to(P(2.2, -2.8))
        rng = np.random.RandomState(3)
        er_dots = VGroup(*[Dot(P(rng.uniform(-5.1, 5.1), rng.uniform(-2.4, -1.15)), radius=0.09, color=YELLOW)
                           for _ in range(34)])
        pitch = 0.54
        subs = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.5, height=0.9, stroke_color=GREY, stroke_width=3,
                                         fill_color="#4A505C", fill_opacity=1).move_to(P((i - 1.5) * pitch, -0.9))
                        for i in range(4)])
        ch_lab = T("IP3 receptor", 26, GREY).move_to(P(-4.0, -0.35))
        ch_ln = seg_line = Line(P(-2.75, -0.45), P(-1.3, -0.8), color=GREY, stroke_width=3)
        four = T("four subunits", 26, GREY).move_to(P(4.0, -0.35))
        four_ln = Line(P(2.75, -0.45), P(1.3, -0.8), color=GREY, stroke_width=3)
        sch = T("schematic, not to scale", 22, GREY).move_to(P(4.6, 3.3))
        rest = VGroup(T("cytosol at rest", 24, TEXT), M("about 100 nM", 24, YELLOW)).arrange(DOWN, buff=0.12).move_to(P(-4.3, 1.5))
        rest_dots = VGroup(*[Dot(P(x, y), radius=0.09, color=YELLOW) for x, y in [(-5.2, 0.5), (-3.2, 0.7), (-4.6, 2.5)]])
        ip3_top = ip3.copy().move_to(P(0, 0.05))

        self.at("Later work")
        self.play(FadeOut(old), FadeOut(suff), FadeOut(ip3), run_time=0.7)
        self.play(Create(er), FadeIn(er_dots), run_time=1.0)
        self.at("endoplasmic reticulum")
        self.play(FadeIn(er_lab), FadeIn(rest), FadeIn(rest_dots), FadeIn(sch), run_time=0.6)
        self.at("receptor")
        self.play(FadeIn(subs, scale=0.8), FadeIn(ch_lab), Create(ch_ln), run_time=0.8)
        self.at("four subunits")
        self.play(FadeIn(four), Create(four_ln),
                  *[pop(sb, 1.15) for sb in subs], run_time=0.9)
        self.at("opens when")
        ip3_top.move_to(P(0, 1.0)).set_z_index(5)
        self.play(FadeIn(ip3_top, shift=DOWN * 0.2), run_time=0.4)
        self.play(ip3_top.animate.move_to(P(0, -0.04)), run_time=0.5)
        self.play(subs[0].animate.shift(LEFT * 0.35), subs[1].animate.shift(LEFT * 0.35),
                  subs[2].animate.shift(RIGHT * 0.35), subs[3].animate.shift(RIGHT * 0.35), run_time=0.5)

        def wave(seed, n, run):
            rr = np.random.RandomState(seed)
            ds = [Dot(P(rr.uniform(-0.25, 0.25), -1.5), radius=0.09, color=YELLOW) for _ in range(n)]
            dst = [P(rr.uniform(-2.4, 2.4), rr.uniform(0.9, 2.8)) for _ in range(n)]
            self.add(*ds)
            self.play(*[d.animate.move_to(p) for d, p in zip(ds, dst)], run_time=run, lag_ratio=0.12)

        wave(40, 9, 3.2)
        self.at("thousand times")
        self.play(FadeIn(er_calc), run_time=0.5)
        wave(50, 8, 3.0)
        self.at("fast rise")
        wave(60, 8, 2.6)
        self.finish()


# =============================================================================================
class S05End(EndCard):
    LINE = "IP3 alone, with no hormone, released calcium from an internal store."
