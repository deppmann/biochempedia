"""Antigen receptors and checkpoints: two phosphates, two signals  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = recognition chains: the alpha and beta chains of the T-cell receptor
  PURPLE = signalling partner chains (CD3, zeta), their tails and tyrosines (the ITAM)
  ORANGE = kinases: Lck, ZAP-70 and the SH2 cups that grip a phosphate
  GOLD   = a phosphate group (the little "P" badge)
  YELLOW = the antigen peptide, and signal one
  TEAL   = the second signal: CD28 and B7
  PINK   = transcription factors (NFAT, NF-kB, AP-1)
  GREEN  = on / tight / switched on
  RED    = absent, weak, anergic
  GREY   = membranes, MHC, the co-receptor, LAT, outlines, quiet labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB5"

# ---------------------------------------------------------------------------------------------
# wide-view geometry (presenting cell on top, T cell below)
# ---------------------------------------------------------------------------------------------
YP = 3.05            # presenting-cell membrane
YT = 0.9             # T-cell membrane
BX0, BX1 = -5.4, 4.0
LBL_X = 5.15         # x of the membrane labels
X_CD3L, X_CD3R, X_Z = -1.7, 1.7, 3.0
X_CO = -3.6          # co-receptor
TAIL_Y0 = 0.6        # y where a partner tail starts
TAIL_L = 3.0

# big-view geometry (one tail, drawn sideways)
TY = -1.0
BYX = (-1.7, 1.7)
CUP_R = 0.8
CUP_Y = TY + 0.62
BAR_Y = 2.35


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, color, size=26):
    c = chip(text, color, size=size)
    box = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height), num_dashes=36)
    box.set_color(color).move_to(c[0])
    return VGroup(box, c[1])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pbadge(r=0.3, size=26):
    c = Circle(radius=r, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", size, BG, weight=BOLD).move_to(c))


def tyr(r=0.26, size=24):
    c = Circle(radius=r, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=1)
    return VGroup(c, T("Y", size, BG, weight=BOLD).move_to(c))


def chain(x, y0, y1, color, w=18):
    return Line([x, y0, 0], [x, y1, 0], color=color, stroke_width=w, cap_style=CapStyleType.ROUND)


def mem_h(y, x0=BX0, x1=BX1, color=GREY):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=0.32, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def tcr(x=0.0):
    return VGroup(chain(x - 0.22, YT - 0.55, 1.78, BLUE, 24), chain(x + 0.22, YT - 0.55, 1.78, BLUE, 24))


def mhc(x=0.0, w=3.2):
    blk = RoundedRectangle(corner_radius=0.16, width=w, height=0.64, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.3).move_to([x, 2.55, 0])
    return VGroup(blk, T("MHC", 26, GREY).move_to(blk))


def peptide(x=0.0):
    return Circle(radius=0.15, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=1).move_to([x, 2.02, 0])


def partner(x):
    return chain(x, YT - 0.25, YT + 0.5, PURPLE, 18)


def tail_xy(x, t, ph=0.0):
    return np.array([x + 0.1 * np.sin(3.2 * t + ph), TAIL_Y0 - t, 0.0])


def tail_v(x, ph=0.0, L=TAIL_L):
    return ParametricFunction(lambda t: tail_xy(x, t, ph), t_range=[0, L], color=PURPLE, stroke_width=7)


ITAM_H = 1.15        # height of the frame round one ITAM (two tyrosines)


def itam_frame(x, t_mid):
    return RoundedRectangle(corner_radius=0.3, width=0.95, height=ITAM_H, stroke_color=PURPLE,
                            stroke_width=2.5).move_to([x, TAIL_Y0 - t_mid, 0])


# the three partner tails: (x, wave phase, tail length, ITAMs as (t of first tyrosine, t of second)).
# The lesson gives one ITAM on each CD3 tail and three on each zeta tail.
PARTNERS = [(X_CD3L, 0.0, 2.0, [(0.4, 1.0)]),
            (X_CD3R, 1.7, 2.0, [(0.4, 1.0)]),
            (X_Z, 3.1, 3.95, [(0.4, 1.0), (1.7, 2.3), (3.0, 3.6)])]


def stage_base():
    """presenting cell + T cell membranes, MHC with its peptide, and the receptor."""
    d = {}
    d["pm"] = mem_h(YP)
    d["tm"] = mem_h(YT)
    d["pm_lbl"] = T("infected cell", 26, GREY).move_to([LBL_X, YP, 0])
    d["tm_lbl"] = T("T cell", 26, GREY).move_to([LBL_X, YT, 0])
    d["mhc"] = mhc()
    d["pep"] = peptide()
    d["pep_lbl"] = T("peptide", 24, YELLOW).move_to([0.95, 2.02, 0])
    d["tcr"] = tcr()
    return d


def partner_set():
    d = {"chains": VGroup(*[partner(x) for x, *_ in PARTNERS])}
    d["tails"] = VGroup(*[tail_v(x, ph, L) for x, ph, L, _ in PARTNERS])
    d["ys"] = VGroup(*[VGroup(*[tyr(0.22, 22).move_to(tail_xy(x, t, ph)) for pr in prs for t in pr])
                       for x, ph, L, prs in PARTNERS])
    d["frames"] = VGroup(*[VGroup(*[itam_frame(x, sum(pr) / 2) for pr in prs]) for x, ph, L, prs in PARTNERS])
    l1 = T("CD3", 24, PURPLE)
    l2 = T("CD3", 24, PURPLE)
    l3 = T("zeta", 24, PURPLE)
    l1.move_to([X_CD3L - 0.2 - l1.width / 2, YT + 0.45, 0])
    l2.move_to([X_CD3R - 0.2 - l2.width / 2, YT + 0.45, 0])
    l3.move_to([X_Z + 0.2 + l3.width / 2, YT + 0.45, 0])
    d["lbls"] = VGroup(l1, l2, l3)
    itam = []
    for x, ph, L, prs in PARTNERS:
        if len(prs) == 1:      # CD3: the label sits under the tail
            itam.append(VGroup(T("ITAM", 24, PURPLE, weight=BOLD).move_to([x, TAIL_Y0 - L - 0.4, 0])))
        else:                  # zeta: one label beside each of the three
            itam.append(VGroup(*[T("ITAM", 24, PURPLE, weight=BOLD).move_to([x + 0.5 + 0.55, TAIL_Y0 - sum(pr) / 2, 0])
                                 for pr in prs]))
    d["itam"] = VGroup(*itam)
    return d


def tcr_label(text):
    t = T(text, 26, BLUE)
    return t.move_to([-0.65 - t.width / 2, 1.85, 0])


# ---- big (one tail, sideways) --------------------------------------------------------------
def big_membrane():
    return RoundedRectangle(corner_radius=0.1, width=0.32, height=3.4, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([-5.6, TY, 0])


def big_tail():
    return ParametricFunction(lambda x: np.array([x, TY + 0.08 * np.sin(2 * np.pi * (x - BYX[0]) / 3.4), 0.0]),
                              t_range=[-5.4, 5.2], color=PURPLE, stroke_width=7)


def big_ys():
    return VGroup(*[tyr(0.32, 28).move_to([x, TY, 0]) for x in BYX])


def big_ps():
    return VGroup(*[pbadge(0.3, 26).move_to([x, CUP_Y, 0]) for x in BYX])


def cup(x, gap, color=ORANGE):
    a = Arc(radius=CUP_R, start_angle=np.radians(-90 + gap / 2), angle=np.radians(360 - gap),
            stroke_color=color, stroke_width=9)
    return a.move_to([x, CUP_Y, 0])


OPEN, SHUT = 150, 52


class Zap:
    """ZAP-70: a kinase bar on two legs, each ending in an SH2 cup. Built at the docked pose."""

    def __init__(self, left_gap=SHUT, right_gap=SHUT, color=ORANGE):
        box = RoundedRectangle(corner_radius=0.18, width=4.7, height=1.0, stroke_color=color, stroke_width=3,
                               fill_color=color, fill_opacity=0.18)
        back = RoundedRectangle(corner_radius=0.18, width=4.7, height=1.0, stroke_width=0, fill_color=BG, fill_opacity=1)
        label = T("ZAP-70 kinase", 32, color)
        self.bar = VGroup(back, box, label).move_to([0, BAR_Y, 0])
        self.legs = [Line([x, CUP_Y + CUP_R, 0], [x, BAR_Y - 0.5, 0], color=ORANGE, stroke_width=8) for x in BYX]
        self.cups = [cup(BYX[0], left_gap), cup(BYX[1], right_gap)]
        self.parts = VGroup(self.bar, *self.legs, *self.cups)

    def set_color(self, color):
        return [self.bar[1].animate.set_stroke(color).set_fill(color, 0.2), self.bar[2].animate.set_color(color)]


def lck_big():
    return bchip("Lck", ORANGE, 30).move_to([0, 1.0, 0])


def hook_pieces():
    """the co-receptor: a chain through the membrane that hooks onto the MHC protein."""
    base = chain(X_CO, YT - 0.55, YT + 0.5, GREY, 22)
    hook = VMobject(joint_type=LineJointType.ROUND, cap_style=CapStyleType.ROUND)
    hook.set_points_as_corners([[X_CO, YT + 0.5, 0], [X_CO, 2.55, 0], [-1.65, 2.55, 0]])
    hook.set_stroke(GREY, width=22)
    return base, hook


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Antigen receptors and checkpoints"
    TITLE = "Two phosphates, two signals"


# =============================================================================================
def puzzle_items():
    """what S01 builds up for the puzzle (rebuilt, finished, at the start of S02)."""
    enz = ghost_chip("enzyme", ORANGE, 28).move_to([3.0, -1.3, 0])
    x1 = Line(enz.get_corner(UL) + [0.1, -0.05, 0], enz.get_corner(DR) + [-0.1, 0.05, 0], color=RED, stroke_width=8)
    x2 = Line(enz.get_corner(DL) + [0.1, 0.05, 0], enz.get_corner(UR) + [-0.1, -0.05, 0], color=RED, stroke_width=8)
    qbox = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=3.0, height=1.0), num_dashes=40).set_color(GREY)
    qbox.move_to([0, -2.4, 0])
    q = T("?", 56, GREY, weight=BOLD).move_to(qbox)
    dl = DashedLine([0, 0.2, 0], [0, -1.62, 0], color=GREY, stroke_width=4, dash_length=0.14)
    tip = Triangle(color=GREY, fill_opacity=1, stroke_width=0).scale(0.13).rotate(PI).move_to([0, -1.72, 0])
    qlbl = T("a message to the cell", 26, GREY).move_to([0, -3.3, 0])
    tick = Line([0.5, 0.35, 0], [0.8, 0.35, 0], color=GREY, stroke_width=3)
    tail_lbl = T("tail: a few amino acids", 26, GREY).next_to(tick, RIGHT, buff=0.15)
    return dict(enz=enz, x1=x1, x2=x2, qbox=qbox, q=q, dl=dl, tip=tip, qlbl=qlbl, tail_lbl=tail_lbl, tick=tick)


class S01Puzzle(SpokenScene):
    """a receptor with a stub of a tail and no enzyme: how does it send a message?"""

    def construct(self):
        DROP = 1.5   # the stage starts lower, centred in the frame, and lifts when the puzzle needs room
        tm = mem_h(YT)
        tm_lbl = T("T cell", 26, GREY).move_to([LBL_X, YT, 0])
        rec = tcr()
        rec_lbl = tcr_label("T cell receptor")
        pm = mem_h(YP)
        pm_lbl = T("infected cell", 26, GREY).move_to([LBL_X, YP, 0])
        mh = mhc()
        pep = peptide()
        pep_lbl = T("peptide", 24, YELLOW).move_to([0.95, 2.02, 0])
        stage = [tm, tm_lbl, rec, rec_lbl, pm, pm_lbl, mh, pep, pep_lbl]
        for m in stage:
            m.shift(DOWN * DROP)
        it = puzzle_items()

        self.at("This is the")
        self.play(Create(tm), FadeIn(tm_lbl), run_time=0.5)
        self.play(FadeIn(rec, shift=UP * 0.3), FadeIn(rec_lbl), run_time=0.8)

        self.at("It tells a")
        self.play(FadeIn(pm, shift=DOWN * 0.3), FadeIn(mh, shift=DOWN * 0.3), FadeIn(pep, shift=DOWN * 0.3),
                  FadeIn(pep_lbl, shift=DOWN * 0.3), run_time=0.9)
        self.at("found an infected")
        self.play(FadeIn(pm_lbl), Indicate(pep, color=YELLOW, scale_factor=1.6), run_time=0.8)

        self.at("But inside")
        self.play(*[m.animate.shift(UP * DROP) for m in stage], run_time=0.9)
        self.at("its tail")
        self.play(FadeIn(it["tail_lbl"]), Create(it["tick"]), Indicate(rec, color=YELLOW, scale_factor=1.0), run_time=0.9)

        self.at("no enzyme")
        self.play(FadeIn(it["enz"], shift=UP * 0.15), run_time=0.7)
        self.at("not even")
        self.play(Create(it["x1"]), Create(it["x2"]), run_time=0.5)

        self.at("how does it")
        self.play(Create(it["dl"]), FadeIn(it["tip"]), run_time=0.6)
        self.play(Create(it["qbox"]), FadeIn(it["q"]), run_time=0.6)
        self.at("a message")
        self.play(FadeIn(it["qlbl"]), Indicate(it["q"], color=TEXT, scale_factor=1.3), run_time=0.8)
        self.finish()


# =============================================================================================
class S02Partners(SpokenScene):
    """partner chains and their tails; two tyrosines on each; the pair is an ITAM."""

    def construct(self):
        st = stage_base()
        lbl = tcr_label("T cell receptor")
        it = puzzle_items()
        puzzle = VGroup(*it.values())
        self.add(st["tm"], st["pm"], st["pm_lbl"], st["tm_lbl"], st["mhc"], st["pep"], st["pep_lbl"], st["tcr"], lbl, puzzle)
        ps = partner_set()

        new_lbl = tcr_label("alpha and beta chains")
        self.at("The alpha")
        self.play(FadeOut(puzzle), ReplacementTransform(lbl, new_lbl), run_time=0.6)
        self.at("do the")
        self.play(Indicate(st["tcr"], color=BLUE, scale_factor=1.0), Indicate(st["pep"], color=YELLOW, scale_factor=1.6), run_time=0.9)

        self.at("partner chains")
        self.play(LaggedStart(*[GrowFromEdge(c, DOWN) for c in ps["chains"]], lag_ratio=0.25), run_time=1.0)
        self.at("and zeta")
        self.play(FadeIn(ps["lbls"], shift=DOWN * 0.1), run_time=0.6)

        self.at("Their tails")
        self.play(LaggedStart(*[Create(t) for t in ps["tails"]], lag_ratio=0.2), run_time=1.5)

        self.at("two tyrosines")
        self.play(LaggedStart(*[LaggedStart(*[FadeIn(y, scale=0.4) for y in pair], lag_ratio=0.3) for pair in ps["ys"]],
                              lag_ratio=0.2), run_time=1.5)
        self.at("fixed short")
        self.play(LaggedStart(*[Create(f) for f in ps["frames"]], lag_ratio=0.2), run_time=1.0)
        self.at("called an")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in ps["itam"]], lag_ratio=0.2), run_time=0.9)
        self.finish()


# =============================================================================================
class S03Borrowed(SpokenScene):
    """the kinase is borrowed: Lck rides on a co-receptor that grips MHC; it phosphorylates both tyrosines."""

    def construct(self):
        st = stage_base()
        ps = partner_set()
        lbl = tcr_label("alpha and beta chains")
        self.add(st["tm"], st["pm"], st["pm_lbl"], st["tm_lbl"], st["mhc"], st["pep"], st["pep_lbl"], st["tcr"], lbl,
                 ps["chains"], ps["tails"], ps["ys"], ps["frames"], ps["lbls"], ps["itam"])
        qk = ghost_chip("kinase?", ORANGE, 28).move_to([0, -3.0, 0])
        self.at("where is the kinase")
        self.play(FadeOut(VGroup(lbl, ps["lbls"], ps["itam"], ps["frames"], st["pep_lbl"])),
                  FadeIn(qk, shift=UP * 0.15), run_time=0.7)

        base, hook = hook_pieces()
        co_lbl = T("co-receptor", 26, GREY).move_to([X_CO - 0.3 - 0.95, 1.75, 0])
        self.at("borrowed from")
        self.play(GrowFromEdge(base, DOWN), run_time=0.7)
        self.play(FadeIn(co_lbl), run_time=0.4)
        self.at("grips the display")
        self.play(Create(hook), run_time=1.2)

        co_tail = Line([X_CO, YT - 0.6, 0], [X_CO, -0.65, 0], color=GREY, stroke_width=7)
        lck = bchip("Lck", ORANGE, 30).move_to([X_CO, -1.05, 0])
        self.at("A share of")
        self.play(ReplacementTransform(qk, lck), Create(co_tail), run_time=1.3, path_arc=1.2)
        self.at("beside the")
        tether = always_redraw(lambda: Line([X_CO, -0.65, 0], lck.get_left() + [0.12, 0.15, 0], color=GREY, stroke_width=6))
        self.add(tether)
        self.play(lck.animate.move_to([-2.95, -0.8, 0]), run_time=0.8)

        # zoom: the nearest tail turns sideways and fills the frame
        big_m, bt, bys = big_membrane(), big_tail(), big_ys()
        lck_b = lck_big()
        wide_tail, wide_ys = ps["tails"][0], ps["ys"][0]
        rest = VGroup(st["tm"], st["pm"], st["pm_lbl"], st["tm_lbl"], st["mhc"], st["pep"], st["tcr"], ps["chains"],
                      ps["tails"][1], ps["tails"][2], ps["ys"][1], ps["ys"][2], base, hook, co_lbl, co_tail)
        self.at("partner tails")
        self.remove(tether)
        self.play(FadeOut(rest), FadeIn(big_m),
                  ReplacementTransform(wide_tail, bt),
                  ReplacementTransform(wide_ys[0], bys[0]), ReplacementTransform(wide_ys[1], bys[1]),
                  ReplacementTransform(lck, lck_b), run_time=1.2)
        pbs = big_ps()
        start = lck_b.get_bottom() + DOWN * 0.32
        p1, p2 = pbs[0].copy().move_to(start), pbs[1].copy().move_to(start)
        self.at("a phosphate")
        self.add(p1)
        self.play(p1.animate.move_to(pbs[0].get_center()), run_time=0.7)
        self.at("both tyrosines")
        self.add(p2)
        self.play(p2.animate.move_to(pbs[1].get_center()), run_time=0.7)
        self.finish()


# =============================================================================================
def big_base():
    return big_membrane(), big_tail(), big_ys(), big_ps()


class S04Reader(SpokenScene):
    """ZAP-70: two SH2 cups spaced like the two tyrosines. One phosphate: weak. Two: tight."""

    def construct(self):
        bm, bt, bys, bps = big_base()
        lck = lck_big()
        self.add(bm, bt, bys, bps, lck)
        self.play(FadeOut(lck), run_time=0.5)

        z = Zap(OPEN, OPEN)
        z.parts.shift(UP * 0.5)
        self.at("reader arrives")
        self.play(FadeIn(z.parts, shift=DOWN * 0.5), run_time=0.9)

        sh_l = T("SH2", 26, ORANGE).move_to(z.cups[0].get_left() + [-0.55, 0, 0])
        sh_r = T("SH2", 26, ORANGE).move_to(z.cups[1].get_right() + [0.55, 0, 0])
        self.at("domains")
        self.play(FadeIn(sh_l), FadeIn(sh_r), Indicate(z.cups[0], color=ORANGE, scale_factor=1.12),
                  Indicate(z.cups[1], color=ORANGE, scale_factor=1.12), run_time=0.9)

        self.at("Each domain")
        self.play(Indicate(bps[0], color=GOLD, scale_factor=1.35), run_time=0.5)
        self.play(Indicate(bps[1], color=GOLD, scale_factor=1.35), run_time=0.5)

        dim_t = DoubleArrow([BYX[0], TY - 0.85, 0], [BYX[1], TY - 0.85, 0], color=GREY, stroke_width=4, buff=0,
                            tip_length=0.18)
        dim_c = DoubleArrow([BYX[0], 1.3, 0], [BYX[1], 1.3, 0], color=ORANGE, stroke_width=4, buff=0, tip_length=0.18)
        self.at("spaced to fit")
        self.play(GrowFromCenter(dim_t), GrowFromCenter(dim_c), run_time=0.7)
        self.play(z.parts.animate.shift(DOWN * 0.5), sh_l.animate.shift(DOWN * 0.5), sh_r.animate.shift(DOWN * 0.5), run_time=0.9)
        self.play(FadeOut(dim_t), FadeOut(dim_c), run_time=0.4)

        weak = T("one phosphate: weak binding", 30, RED).move_to([0, -2.6, 0])
        self.at("With one phosphate")
        self.play(bps[1].animate.set_opacity(0.18), run_time=0.5)
        self.at("binds weakly")
        self.play(Transform(z.cups[0], cup(BYX[0], SHUT)), FadeIn(weak), run_time=0.6)
        self.play(Wiggle(z.parts, scale_value=1.0, rotation_angle=0.025 * TAU), run_time=0.8)

        tight = T("two phosphates: tight binding", 30, GREEN).move_to([0, -2.6, 0])
        self.at("binds tightly")
        self.play(bps[1].animate.set_opacity(1), run_time=0.4)
        self.play(Transform(z.cups[1], cup(BYX[1], SHUT)), ReplacementTransform(weak, tight), run_time=0.7)
        self.at("both tyrosines")
        self.play(Indicate(bys, color=PURPLE, scale_factor=1.25), run_time=0.8)
        self.finish()


# =============================================================================================
class S05Branches(SpokenScene):
    """ZAP-70 opens, phosphorylates LAT, and three branches leave LAT and meet on a gene."""

    def construct(self):
        bm, bt, bys, bps = big_base()
        z = Zap()
        sh_l = T("SH2", 26, ORANGE).move_to(z.cups[0].get_left() + [-0.55, 0, 0])
        sh_r = T("SH2", 26, ORANGE).move_to(z.cups[1].get_right() + [0.55, 0, 0])
        tight = T("two phosphates: tight binding", 30, GREEN).move_to([0, -2.6, 0])
        self.add(bm, bt, bys, bps, z.parts, sh_l, sh_r, tight)

        self.at("Docking opens")
        self.play(FadeOut(tight), *z.set_color(GREEN), run_time=0.7)

        # ZAP-70 and LAT meet in the middle, then slide left to make room for the branches
        chip_z = bchip("ZAP-70", GREEN, 30).move_to([-2.5, 0.0, 0])
        lat = RoundedRectangle(corner_radius=0.14, width=0.5, height=3.2, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.35).move_to([0.2, 0.0, 0])
        lat_lbl = T("LAT", 32, TEXT, weight=BOLD).move_to([0.2, 2.1, 0])
        self.at("phosphorylates")
        self.play(FadeOut(VGroup(bm, bt, bys, bps, sh_l, sh_r, *z.legs, *z.cups)),
                  ReplacementTransform(z.bar, chip_z), FadeIn(lat, shift=RIGHT * 0.2), FadeIn(lat_lbl), run_time=1.1)
        p = pbadge(0.26, 22).move_to(chip_z.get_right() + [0.35, 0.3, 0])
        self.at("LAT")
        self.play(FadeIn(p, scale=0.5), run_time=0.2)
        self.play(p.animate.move_to(lat.get_left() + [0.0, 0.3, 0]), run_time=0.6)
        self.at("scaffold")
        self.play(Indicate(lat, color=TEXT, scale_factor=1.05), run_time=0.7)

        left = VGroup(chip_z, lat, lat_lbl, p)
        rows = [2.1, 0.0, -2.1]
        mids = ["calcium", "DAG, PKC", "Ras, ERK"]
        tfs = ["NFAT", "NF-κB", "AP-1"]
        mid_x, tf_x = -0.2, 2.5
        lat_x = -2.9          # where LAT ends up
        mid_chips = [bchip(m, TEXT, 28).move_to([mid_x, y, 0]) for m, y in zip(mids, rows)]
        tf_chips = [bchip(t, PINK, 28).move_to([tf_x, y, 0]) for t, y in zip(tfs, rows)]
        lat_right = lat_x + 0.25
        a_lat = [arr([lat_right + 0.02, y * 0.45, 0], [mc.get_left()[0], y, 0], GREY, 4, 0.2) for y, mc in zip(rows, mid_chips)]
        a_tf = [arr(mc.get_right(), tc.get_left(), GREY, 4, 0.2) for mc, tc in zip(mid_chips, tf_chips)]

        self.at("one branch")
        self.play(left.animate.shift(LEFT * (0.2 - lat_x)), GrowArrow(a_lat[0]), run_time=0.6)
        self.at("raises calcium")
        self.play(FadeIn(mid_chips[0], shift=RIGHT * 0.2), run_time=0.5)
        self.at("enters the")
        self.play(GrowArrow(a_tf[0]), FadeIn(tf_chips[0], shift=RIGHT * 0.2), run_time=0.6)

        self.at("A second")
        self.play(GrowArrow(a_lat[1]), run_time=0.4)
        self.at("protein kinase")
        self.play(FadeIn(mid_chips[1], shift=RIGHT * 0.2), run_time=0.5)
        self.at("C to")
        self.play(GrowArrow(a_tf[1]), FadeIn(tf_chips[1], shift=RIGHT * 0.2), run_time=0.6)

        self.at("A third")
        self.play(GrowArrow(a_lat[2]), run_time=0.4)
        self.at("loads Ras")
        self.play(FadeIn(mid_chips[2], shift=RIGHT * 0.2), run_time=0.5)
        self.at("helps build")
        self.play(GrowArrow(a_tf[2]), FadeIn(tf_chips[2], shift=RIGHT * 0.2), run_time=0.6)

        gene = RoundedRectangle(corner_radius=0.14, width=0.5, height=3.2, stroke_color=TEXT, stroke_width=3,
                                fill_color=TEXT, fill_opacity=0.2).move_to([5.3, 0.0, 0])
        gene_lbl = T("interleukin-2\ngene", 26, TEXT, line_spacing=0.8).move_to([5.3, -2.5, 0])
        a_gene = [arr(tc.get_right(), [gene.get_left()[0], y * 0.45, 0], PINK, 4, 0.2) for tc, y in zip(tf_chips, rows)]
        self.at("The three meet")
        self.play(FadeIn(gene, shift=LEFT * 0.2), run_time=0.5)
        self.play(LaggedStart(*[GrowArrow(a) for a in a_gene], lag_ratio=0.2), run_time=0.9)
        self.at("interleukin")
        self.play(FadeIn(gene_lbl), run_time=0.5)
        self.finish()


# =============================================================================================
class S06Two(SpokenScene):
    """signal one alone leaves the cell anergic; CD28 binding B7 is signal two; two phosphates and two signals."""

    def construct(self):
        XR = -3.4   # receptor column
        XC = 1.9    # CD28 / B7 column
        x0, x1 = -5.8, 3.7
        pm, tm = mem_h(YP, x0, x1), mem_h(YT, x0, x1)
        pm_lbl = T("presenting cell", 26, GREY).move_to([5.15, YP, 0])
        tm_lbl = T("T cell", 26, GREY).move_to([5.15, YT, 0])
        body = RoundedRectangle(corner_radius=0.3, width=x1 - x0, height=YT - 0.16 + 3.3, stroke_color=GREY,
                                stroke_width=3).move_to([(x0 + x1) / 2, (YT - 0.16 - 3.3) / 2, 0])
        mh, pep, rec = mhc(XR, 3.2), peptide(XR), tcr(XR)
        pep_lbl = T("own peptide", 26, YELLOW).move_to([XR + 0.35 + 1.15, 2.02, 0])
        sig1 = T("signal 1", 30, YELLOW, weight=BOLD).move_to([XR, -0.75, 0])
        slot = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=1.1, height=1.5), num_dashes=36).set_color(GREY)
        slot.move_to([XC, 1.95, 0])
        slot_q = T("?", 48, GREY, weight=BOLD).move_to(slot)

        self.at("Even this")
        self.play(Create(pm), Create(tm), FadeIn(pm_lbl), FadeIn(tm_lbl), Create(body), run_time=0.9)
        self.play(FadeIn(mh, shift=DOWN * 0.2), FadeIn(pep, shift=DOWN * 0.2), FadeIn(rec, shift=UP * 0.2),
                  FadeIn(sig1), run_time=0.8)
        self.play(Create(slot), FadeIn(slot_q), run_time=0.6)

        self.at("vary almost")
        self.play(Wiggle(rec, scale_value=1.0, rotation_angle=0.04 * TAU), run_time=0.9)
        self.at("own peptides")
        self.play(FadeIn(pep_lbl), Indicate(pep, color=YELLOW, scale_factor=1.6), run_time=0.8)

        cx = (x0 + x1) / 2
        worse = T("worse than nothing", 40, RED, weight=BOLD).move_to([cx, -2.0, 0])
        self.at("alone did worse")
        self.play(body.animate.set_stroke(RED, 5), FadeIn(worse, shift=UP * 0.15), run_time=0.7)
        anergy = T("anergy", 56, RED, weight=BOLD).move_to([cx, -1.85, 0])
        sub = T("a lasting unresponsive state", 28, RED).move_to([cx, -2.75, 0])
        self.at("lasting unresponsive")
        self.play(ReplacementTransform(worse, anergy), FadeIn(sub), run_time=0.8)

        # signal two: B7 on the presenting cell, CD28 on the T cell, each with a round head
        def b7_pic():
            return VGroup(chain(XC, 2.9, 2.3, TEAL, 24), Dot([XC, 2.25, 0], radius=0.24, color=TEAL))

        def cd28_pic(top):
            return VGroup(chain(XC, YT - 0.55, top - 0.05, TEAL, 24), Dot([XC, top, 0], radius=0.24, color=TEAL))

        b7, cd28 = b7_pic(), cd28_pic(1.3)
        b7_lbl = T("B7", 26, TEAL).move_to([XC + 0.75, 2.6, 0])
        cd28_lbl = T("CD28", 26, TEAL).move_to([XC + 0.95, 1.5, 0])
        self.at("second signal needs")
        fresh = T("a fresh T cell, both signals", 28, TEXT, weight=BOLD).move_to([cx, -2.85, 0])
        self.play(FadeOut(VGroup(anergy, sub, pep_lbl, slot, slot_q)), body.animate.set_stroke(GREY, 3), run_time=0.5)
        self.play(FadeIn(fresh, shift=UP * 0.15), FadeIn(b7, shift=DOWN * 0.2), FadeIn(cd28, shift=UP * 0.2),
                  FadeIn(b7_lbl), FadeIn(cd28_lbl), run_time=0.9)
        sig2 = T("signal 2", 30, TEAL, weight=BOLD).move_to([XC, -0.75, 0])
        on = T("switched on", 56, GREEN, weight=BOLD).move_to([cx, -1.85, 0])
        self.at("to bind")
        self.play(Transform(cd28, cd28_pic(1.8)), FadeIn(sig2), run_time=0.8)
        self.play(body.animate.set_stroke(GREEN, 5), FadeIn(on, shift=UP * 0.15), run_time=0.8)

        p1, p2 = pbadge(0.24, 22).move_to([XR - 0.32, -0.1, 0]), pbadge(0.24, 22).move_to([XR + 0.32, -0.1, 0])
        self.at("two phosphates")
        self.play(FadeIn(p1, scale=0.4), FadeIn(p2, scale=0.4), Indicate(sig1, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.at("two signals")
        self.play(Indicate(sig1, color=YELLOW, scale_factor=1.2), Indicate(sig2, color=TEAL, scale_factor=1.2), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "A T cell needs two phosphates and two signals."
