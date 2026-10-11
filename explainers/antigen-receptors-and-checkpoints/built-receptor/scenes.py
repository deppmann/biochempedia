"""Antigen receptors and checkpoints, section film: building a receptor from parts  (Biochemistrypedia)

COLOR MAP (one color per concept, whole video)
  BLUE   = the T-cell receptor's own chains: constant regions and its own tips
  ORANGE = antibody parts (variable regions, antibody fragment)
  PURPLE = the zeta tail inside the cell
  YELLOW = the peptide
  PINK   = the antibody's target, a whole folded protein (schematic)
  GREEN  = the T cell responds
  RED    = crossed out / not needed
  GOLD   = the one highlight: the name CAR
  GREY   = membranes, MHC, quiet labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
TEAL_P = "#E58FB5"

TM_Y = -1.3     # T-cell membrane
CM_Y = 2.95     # membrane of the other cell


def mem(y, x0, x1, color=GREY):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=0.32, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def rods(x, color=BLUE):
    g = VGroup()
    for dx in (-0.3, 0.3):
        g.add(Line([x + dx, TM_Y + 0.15, 0], [x + dx, 0.95, 0], color=color, stroke_width=20,
                   cap_style=CapStyleType.ROUND))
    return g


def tips(x, color=BLUE):
    g = VGroup()
    for dx in (-0.3, 0.3):
        g.add(RoundedRectangle(corner_radius=0.16, width=0.5, height=0.55, stroke_color=color, stroke_width=3,
                               fill_color=color, fill_opacity=0.85).move_to([x + dx, 1.3, 0]))
    return g


def mhc(x, w=2.2):
    blk = RoundedRectangle(corner_radius=0.16, width=w, height=0.64, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.3).move_to([x, 2.42, 0])
    return VGroup(blk, T("MHC", 26, GREY).move_to(blk))


def peptide(x):
    return Circle(radius=0.15, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=1).move_to([x, 2.0, 0])


def blob(x, y=2.3):
    g = VGroup()
    for dx, dy, r in ((-0.4, 0.0, 0.42), (0.1, 0.12, 0.45), (0.5, -0.05, 0.36)):
        g.add(Circle(radius=r, stroke_color=TEAL_P, stroke_width=3, fill_color=TEAL_P, fill_opacity=0.4)
              .move_to([x + dx, y + dy, 0]))
    return g


def ghost_chip(text, color, size=26):
    c = chip(text, color, size=size)
    box = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height), num_dashes=36)
    box.set_color(color).move_to(c[0])
    return VGroup(box, c[1])


def cross(mob, color=RED):
    a = mob.get_corner(UL) + 0.05 * (RIGHT + DOWN)
    b = mob.get_corner(DR) + 0.05 * (LEFT + UP)
    c = mob.get_corner(UR) + 0.05 * (LEFT + DOWN)
    d = mob.get_corner(DL) + 0.05 * (RIGHT + UP)
    return VGroup(Line(a, b, color=color, stroke_width=6), Line(c, d, color=color, stroke_width=6))


def zeta_tail(x, y0, y1):
    return ParametricFunction(lambda t: np.array([x + 0.12 * np.sin(3.2 * t), y0 - t, 0.0]),
                              t_range=[0, y0 - y1], color=PURPLE, stroke_width=8)


XR = -1.5   # x of the receptor in scenes 1 and 2


class S00Title(TitleCard):
    LESSON = "Antigen receptors and checkpoints"
    TITLE = "Antibody outside, zeta tail inside"


class S01Gap(SpokenScene):
    def construct(self):
        cm = mem(CM_Y, -5.2, 2.6)
        tm = mem(TM_Y, -5.2, 2.6)
        cl = T("tumour cell", 26, GREY).move_to([4.3, CM_Y, 0])
        tl = T("T cell", 26, GREY).move_to([4.3, TM_Y, 0])
        m = mhc(XR)
        p = peptide(XR)
        pl = T("peptide", 24, YELLOW).move_to([XR + 1.0, 1.8, 0], aligned_edge=LEFT)
        pl.next_to(p, RIGHT, buff=1.3).shift(DOWN * 0.15)
        r_rods, r_tips = rods(XR), tips(XR)
        self.play(FadeIn(cm), FadeIn(tm), FadeIn(cl), FadeIn(tl), run_time=0.5)
        self.play(FadeIn(m), FadeIn(p), FadeIn(r_rods), FadeIn(r_tips), run_time=0.5)
        self.at("reads a short peptide")
        self.play(r_tips.animate.shift(UP * 0.12), FadeIn(pl), run_time=0.5)
        note = T("helps only if T cells already\nrecognise the tumour", 28, TEXT, line_spacing=0.9).move_to([3.0, 0.1, 0])
        fit(note, max_w=5.4)
        note.move_to([3.0, 0.1, 0])
        self.at("helps only if")
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.at("The other approach")
        q = ghost_chip("?", ORANGE, size=60)
        q.move_to([XR, 0.2, 0])
        self.play(FadeOut(VGroup(r_rods, r_tips, pl, note)), run_time=0.5)
        self.play(FadeIn(q, scale=0.8), run_time=0.5)
        lab = T("a new receptor", 28, ORANGE).next_to(q, RIGHT, buff=0.5)
        self.play(FadeIn(lab), run_time=0.4)
        self.at("build one from parts")
        parts = T("built from parts", 28, ORANGE).move_to(lab)
        self.play(Transform(lab, parts), run_time=0.5)
        self.finish()


class S02Swap(SpokenScene):
    def construct(self):
        tm = mem(TM_Y, -5.2, 2.6)
        tl = T("T cell", 26, GREY).move_to([4.3, TM_Y, 0])
        r_rods, r_tips = rods(XR), tips(XR)
        rl = T("T cell receptor\nchains", 24, BLUE, line_spacing=0.9).move_to([-4.2, 0.2, 0])
        self.add(tm, tl, r_rods, r_tips)
        self.play(FadeIn(rl), run_time=0.3)
        self.at("joined the variable regions")
        credit1 = T("Gross, Waks and Eshhar, 1989", 28, TEXT).move_to([-0.3, -2.35, 0])
        ab_tips = tips(XR + 3.4, ORANGE).shift(UP * 0.5)
        abl = T("antibody\nvariable regions", 24, ORANGE, line_spacing=0.9).next_to(ab_tips, RIGHT, buff=0.4)
        abl.shift(UP * 0.0)
        self.play(FadeIn(credit1, shift=UP * 0.1), FadeIn(ab_tips, shift=UP * 0.2), FadeIn(abl), run_time=0.7)
        self.play(r_tips.animate.shift(UP * 1.0).set_opacity(0), run_time=0.7)
        self.play(ab_tips.animate.move_to(r_tips.get_center() + DOWN * 1.0), abl.animate.shift(LEFT * 0.0),
                  run_time=0.9)
        self.at("constant regions")
        self.play(Indicate(r_rods, color=BLUE, scale_factor=1.05), run_time=0.7)
        hyb = T("hybrid", 28, TEXT).move_to([-4.2, 1.3, 0])
        self.at("carrying the hybrid")
        self.play(FadeIn(hyb), FadeOut(abl), run_time=0.4)
        self.at("responded to")
        cm = mem(CM_Y, -5.2, 2.6)
        tgt = blob(XR)
        tgl = T("target", 26, TEAL_P).next_to(tgt, RIGHT, buff=0.6)
        self.play(FadeIn(cm), FadeIn(tgt, shift=DOWN * 0.2), FadeIn(tgl), run_time=0.7)
        resp = T("responds", 28, GREEN, weight=BOLD).move_to([4.3, 0.1, 0])
        self.play(tm.animate.set_color(GREEN), FadeIn(resp), run_time=0.5)
        self.at("published the same kind")
        credit2 = T("Kuwana and colleagues, 1987:\nthe same kind of construct", 26, GREY, line_spacing=0.9).move_to([-0.3, -3.1, 0])
        self.play(FadeIn(credit2), run_time=0.6)
        self.finish()


class S03Direct(SpokenScene):
    def construct(self):
        # left panel: the receptor's own tips read peptide on MHC
        LX, RX = -3.2, 3.2
        lcm, ltm = mem(CM_Y, -5.9, -0.6), mem(TM_Y, -5.9, -0.6)
        lm, lp = mhc(LX), peptide(LX)
        lr, lt = rods(LX), tips(LX)
        lcap = T("peptide held on MHC", 26, YELLOW).move_to([LX, -2.4, 0])
        left = VGroup(lcm, ltm, lm, lp, lr, lt)
        self.at("receptor's own tips")
        self.play(FadeIn(left), run_time=0.6)
        self.play(FadeIn(lcap), lt.animate.shift(UP * 0.12), run_time=0.5)
        # right panel
        rcm, rtm = mem(CM_Y, 0.6, 5.9), mem(TM_Y, 0.6, 5.9)
        rr, rt = rods(RX), tips(RX, ORANGE)
        rb = blob(RX)
        rcap = T("whole folded protein", 26, TEAL_P).move_to([RX, -2.4, 0])
        self.at("An antibody is different")
        self.play(left.animate.set_opacity(0.3), lcap.animate.set_opacity(0.3), run_time=0.5)
        self.play(FadeIn(VGroup(rcm, rtm, rr, rt)), run_time=0.6)
        self.at("grips a whole folded")
        self.play(FadeIn(rb, shift=DOWN * 0.2), FadeIn(rcap), rt.animate.shift(UP * 0.12), run_time=0.7)
        gp = ghost_chip("peptide", RED, size=24).move_to([5.2, 2.3, 0])
        gm = ghost_chip("MHC", RED, size=24).move_to([1.3, 2.3, 0])
        self.at("needs no peptide")
        self.play(FadeIn(gp), run_time=0.4)
        self.play(Create(cross(gp)), run_time=0.4)
        self.at("and no")
        self.play(FadeIn(gm), run_time=0.4)
        self.play(Create(cross(gm)), run_time=0.4)
        self.finish()


class S04Car(SpokenScene):
    def construct(self):
        MY = 0.3
        tm = mem(MY, -5.5, 3.0)
        out_l = T("outside the cell", 26, GREY).move_to([4.5, 1.1, 0])
        in_l = T("inside the cell", 26, GREY).move_to([4.5, -0.5, 0])
        # carried over: the two-chain hybrid (orange tips on blue chains), now drawn across this membrane
        X = -1.5
        rd = VGroup(*[Line([X + dx, MY - 0.9, 0], [X + dx, MY + 1.5, 0], color=BLUE, stroke_width=20,
                           cap_style=CapStyleType.ROUND) for dx in (-0.3, 0.3)])
        tp = VGroup(*[RoundedRectangle(corner_radius=0.16, width=0.5, height=0.55, stroke_color=ORANGE, stroke_width=3,
                                       fill_color=ORANGE, fill_opacity=0.85).move_to([X + dx, MY + 1.85, 0])
                      for dx in (-0.3, 0.3)])
        self.add(tm, rd, tp)
        self.add(out_l, in_l)
        note = T("later designs:\nEshhar's laboratory\nand others", 24, GREY, line_spacing=0.9).move_to([-4.3, 2.3, 0])
        self.at("were single chains")
        # one chain: antibody fragment, a line across the membrane, zeta tail
        frag = RoundedRectangle(corner_radius=0.22, width=1.1, height=0.8, stroke_color=ORANGE, stroke_width=3,
                                fill_color=ORANGE, fill_opacity=0.85).move_to([X, MY + 2.4, 0])
        stem = Line([X, MY + 2.0, 0], [X, MY - 0.3, 0], color=GREY, stroke_width=14, cap_style=CapStyleType.ROUND)
        self.play(ReplacementTransform(tp, frag), ReplacementTransform(rd, stem), FadeIn(note), run_time=1.0)
        fl = T("antibody fragment", 26, ORANGE).next_to(frag, RIGHT, buff=0.5)
        self.at("antibody fragment outside")
        self.play(FadeIn(fl), run_time=0.4)
        self.at("the zeta tail inside")
        tail = zeta_tail(X, MY - 0.3, -3.1)
        self.play(Create(tail), run_time=0.9)
        tl = T("zeta tail", 26, PURPLE).move_to([X + 1.7, -1.8, 0])
        self.play(FadeIn(tl), run_time=0.3)
        self.at("chimeric antigen receptor")
        car = T("chimeric\nantigen receptor:\nCAR", 28, GOLD, weight=BOLD, line_spacing=0.9).move_to([-4.0, -1.9, 0])
        self.play(FadeIn(car, shift=UP * 0.1), run_time=0.6)
        sch = T("schematic, not to scale", 22, GREY).move_to([4.2, -3.1, 0])
        self.add(sch)
        self.at("Remember the plan")
        self.play(Indicate(frag, color=ORANGE, scale_factor=1.15), Indicate(tail, color=PURPLE), run_time=1.2)
        self.finish()


class S05End(EndCard):
    LINE = "A CAR: antibody outside, zeta tail inside."
