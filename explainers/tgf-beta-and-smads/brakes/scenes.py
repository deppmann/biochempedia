"""Three brakes on a strong signal (TGF-beta and Smads, section film)

COLOR MAP (one color per concept, whole video)
  YELLOW = the ligand (TGF-beta)
  BLUE   = receptor (type I / BMP type I)
  GREEN  = ON / active (active receptor, switched-on gene)
  RED    = a brake (wrapper, Smad7, the blocked path)
  PURPLE = Smads (R-Smad, Smad4)
  TEAL   = Smurfs (ubiquitin ligases)
  GOLD   = ubiquitin tag (Ub)
  ORANGE = release agents in scene 1 (integrin, protease) and the "what breaks" cards
  PINK   = muscle / bone tissue in the cards
  GREY   = membranes, matrix, DNA, outlines
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB4"


def bchip(text, color=BLUE, size=28, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def recolor(c, color):
    return [c[1].animate.set_stroke(color).set_fill(color, 0.16), c[2].animate.set_color(color)]


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.24, b - perp * 0.24, color=color, stroke_width=w + 1))


def membrane_h(y, x0=-6.3, x1=6.3, h=0.32):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def ubadge(r=0.27):
    c = Circle(radius=r, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("Ub", 22, BG, weight=BOLD).move_to(c))


def brake_tag(text):
    return chip(text, RED, size=28).to_corner(UL, buff=0.45)


def cross(mob, color=RED, pad=0.1):
    w, h = mob.width, mob.height
    a = Line(mob.get_corner(UL) + [pad, -pad, 0], mob.get_corner(DR) + [-pad, pad, 0], color=color, stroke_width=7)
    b = Line(mob.get_corner(DL) + [pad, pad, 0], mob.get_corner(UR) + [-pad, -pad, 0], color=color, stroke_width=7)
    return VGroup(a, b)


class S00Title(TitleCard):
    LESSON = "TGF-β and Smads"
    TITLE = "Three brakes on a strong signal"


# ---------------------------------------------------------------------------------------------
class S01Locked(SpokenScene):
    def construct(self):
        mem = membrane_h(2.0)
        rec = RoundedRectangle(corner_radius=0.2, width=0.6, height=1.1, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.3).move_to([0, 1.45, 0])
        rec_l = T("receptor", 26, BLUE).move_to([1.5, 1.25, 0])
        self.play(FadeIn(mem), FadeIn(rec), FadeIn(rec_l), run_time=0.3)

        self.at("First")
        tag = brake_tag("Brake 1: stored locked")
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.5)

        lig = bchip("TGF-β", YELLOW, 32).move_to([0, -0.9, 0])
        self.at("secreted")
        self.play(FadeIn(lig, shift=UP * 0.3), run_time=0.6)
        wrap = RoundedRectangle(corner_radius=0.3, width=4.0, height=2.1, stroke_color=RED, stroke_width=5,
                                fill_color=RED, fill_opacity=0.14).move_to([0, -0.6, 0])
        wl = T("wrapper", 26, RED).move_to([0, 0.15, 0])
        self.at("wrapped")
        self.play(Create(wrap), FadeIn(wl), run_time=0.9)

        # the wrapper covers the surfaces the receptor needs
        blk = DashedLine([0, 0.45, 0], [0, 0.9, 0], color=GREY, stroke_width=4)
        barr = Line([-0.3, 0.68, 0], [0.3, 0.68, 0], color=RED, stroke_width=8)
        self.at("covers the surfaces")
        self.play(Create(blk), FadeIn(barr), run_time=0.5)

        # tethered to the matrix
        mat = Rectangle(width=12.6, height=0.8, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                        fill_opacity=0.22).move_to([0, -3.1, 0])
        hatch = VGroup(*[Line([x, -3.5, 0], [x + 0.4, -2.7, 0], color=GREY, stroke_width=2).set_opacity(0.6)
                         for x in np.arange(-6.2, 5.9, 0.6)])
        mat_l = bchip("extracellular matrix", GREY, 24, fill_opacity=0.0).move_to([0, -3.1, 0])
        tether = Line([0, -1.65, 0], [0, -2.7, 0], color=GREY, stroke_width=5)
        self.at("tethered")
        self.play(Create(tether), run_time=0.6)
        self.at("extracellular matrix")
        self.play(FadeIn(mat), FadeIn(hatch), FadeIn(mat_l), run_time=0.8)

        # integrin pulls / protease cuts (examples)
        integ = bchip("integrin", ORANGE, 26).move_to([-3.5, 2.0, 0])
        pull = arr([-2.4, 1.9, 0], [-2.05, -0.05, 0], ORANGE)
        eg1 = T("for example", 22, GREY).next_to(integ, DOWN, buff=0.12)
        self.at("integrins")
        self.play(FadeIn(integ), GrowArrow(pull), FadeIn(eg1), run_time=0.8)
        prot = bchip("protease", ORANGE, 26).move_to([4.6, -0.4, 0])
        eg2 = T("for example", 22, GREY).next_to(prot, DOWN, buff=0.12)
        slash = Line([2.3, 0.2, 0], [1.7, -0.4, 0], color=ORANGE, stroke_width=8)
        self.at("protease")
        self.play(FadeIn(prot), FadeIn(eg2), run_time=0.5)
        self.play(Create(slash), run_time=0.3)

        # release
        act = T("active TGF-β", 26, YELLOW).move_to([2.4, 0.5, 0])
        self.at("released")
        self.play(FadeOut(barr), FadeOut(blk), FadeOut(slash), FadeOut(pull), FadeOut(integ), FadeOut(eg1),
                  FadeOut(prot), FadeOut(eg2),
                  VGroup(wrap, wl).animate.shift(DOWN * 0.9).set_opacity(0.3),
                  tether.animate.put_start_and_end_on([0, -2.55, 0], [0, -2.7, 0]),
                  lig.animate.move_to([0, 0.5, 0]), run_time=1.3)
        self.play(FadeIn(act), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Feedback(SpokenScene):
    def construct(self):
        mem = membrane_h(2.0)
        rx = 3.3
        rec = bchip("active type I", GREEN, 28).move_to([rx, 2.0, 0])
        rsm = bchip("R-Smad", PURPLE, 28).move_to([rx, 0.7, 0])
        dock = Line([rx, 1.6, 0], [rx, 1.1, 0], color=GREEN, stroke_width=4)
        dna = Line([-6.0, -2.6, 0], [-0.4, -2.6, 0], color=GREY, stroke_width=5)
        gene = bchip("Smad7 gene", GREY, 28).move_to([-3.4, -2.6, 0])
        self.play(FadeIn(mem), FadeIn(dna), FadeIn(gene), FadeIn(rec), FadeIn(rsm), Create(dock), run_time=0.3)
        tag = brake_tag("Brake 2: feedback")
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.5)

        self.at("genes")
        p1 = arr([rx - 0.9, 0.45, 0], [-2.55, -0.95, 0], PURPLE, 4)
        self.play(FadeOut(dock), rsm.animate.move_to([-3.4, -1.2, 0]), GrowArrow(p1), run_time=0.9)
        self.at("switch on")
        self.play(*recolor(gene, GREEN), run_time=0.4)
        s7 = bchip("Smad7", RED, 28).move_to([-0.9, -2.6, 0])
        self.at("encodes")
        self.play(FadeIn(s7, shift=RIGHT * 0.3), run_time=0.5)
        p2 = arr([-0.9, -2.15, 0], [rx - 0.7, 0.35, 0], RED, 4)
        self.at("binds the active")
        self.play(s7.animate.move_to([rx, 0.7, 0]), GrowArrow(p2), run_time=1.5)
        lnk = Line([rx, 1.6, 0], [rx, 1.1, 0], color=RED, stroke_width=4)
        self.play(Create(lnk), run_time=0.3)

        r2 = bchip("R-Smad", PURPLE, 28).move_to([5.4, -0.7, 0])
        self.at("keeps")
        self.play(FadeIn(r2), run_time=0.4)
        self.play(r2.animate.move_to([5.4, 0.2, 0]), run_time=0.5)
        blk = inhib([5.2, 0.45, 0], [4.15, 0.7, 0], RED)
        self.play(Create(blk), run_time=0.4)
        self.play(r2.animate.set_opacity(0.5), run_time=0.3)

        nf = T("negative feedback", 34, RED, weight=BOLD).move_to([-1.3, 1.4, 0])
        self.at("negative feedback")
        self.play(Write(nf), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Destroy(SpokenScene):
    def construct(self):
        mem = membrane_h(2.0)
        rx = -3.8
        rec = bchip("active type I", GREEN, 30).move_to([rx, 2.0, 0])
        s7 = bchip("Smad7", RED, 30).move_to([rx, -0.5, 0])
        l1 = Line([rx, 1.6, 0], [rx, -0.05, 0], color=RED, stroke_width=4)
        self.play(FadeIn(mem), FadeIn(rec), FadeIn(s7), Create(l1), run_time=0.3)
        tag = brake_tag("Brake 3: destroyed")
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.5)

        smurf = bchip("Smurfs", TEAL, 30).move_to([-0.2, -0.5, 0])
        sl = T("ubiquitin ligases", 24, TEAL).next_to(smurf, DOWN, buff=0.2)
        l2 = Line([rx + 0.95, -0.5, 0], [-0.2 - 0.85, -0.5, 0], color=TEAL, stroke_width=4)
        self.at("brings")
        self.play(FadeIn(smurf, shift=LEFT * 0.4), Create(l2), run_time=0.8)
        self.at("ligases")
        self.play(FadeIn(sl), run_time=0.4)

        sm = bchip("some Smads", PURPLE, 30).move_to([4.0, -0.5, 0])
        legend = VGroup(ubadge(), T("Ub = ubiquitin tag", 26, GOLD)).arrange(RIGHT, buff=0.3).move_to([0, -2.6, 0])
        self.at("to the receptor")
        self.play(FadeIn(sm), FadeIn(legend), run_time=0.6)

        self.at("tag the receptor")
        ub1 = [ubadge().move_to([-0.2, 0.1, 0]) for _ in range(2)]
        ends = [[-2.9, 1.35, 0], [-4.7, 1.35, 0]]
        self.play(*[FadeIn(u) for u in ub1], run_time=0.2)
        self.play(*[u.animate.move_to(e) for u, e in zip(ub1, ends)], run_time=1.0)
        self.at("some")
        ub2 = [ubadge().move_to([0.9, -0.2, 0]) for _ in range(2)]
        e2 = [[2.45, -0.8, 0], [2.45, -0.2, 0]]
        self.play(*[FadeIn(u) for u in ub2], run_time=0.2)
        self.play(*[u.animate.move_to(e) for u, e in zip(ub2, e2)], run_time=1.0)

        self.at("destruction")
        x1 = cross(rec, RED); x2 = cross(sm, RED)
        self.play(Create(x1), Create(x2), run_time=0.5)
        self.play(VGroup(rec, x1, *ub1).animate.set_opacity(0.15), VGroup(sm, x2, *ub2).animate.set_opacity(0.15),
                  run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def lines(txt, size=22, color=TEXT):
    return VGroup(*[T(l, size, color) for l in txt.split("\n")]).arrange(DOWN, buff=0.1)


def card_frame(title, sub):
    box = RoundedRectangle(corner_radius=0.25, width=4.0, height=6.0, stroke_color=ORANGE, stroke_width=3,
                           fill_color=ORANGE, fill_opacity=0.06)
    t = T(title, 30, TEXT, weight=BOLD).move_to([0, 2.5, 0])
    sub.move_to([0, 1.8, 0])
    return box, t, sub


class S04Breaks(SpokenScene):
    def construct(self):
        XS = [-4.2, 0.0, 4.2]

        # ---- card 1: Smad4, pancreatic cancer (local coordinates, card centred on the origin) ----
        b1, t1, s1 = card_frame("Smad4", lines("Scott Kern's\nlaboratory", 22, GREY))
        sm4 = bchip("Smad4", PURPLE, 36).move_to([0, 0.5, 0])
        x1 = cross(sm4, RED)
        bar = Rectangle(width=3.2, height=0.45, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([0, -0.7, 0])
        half = Rectangle(width=1.6, height=0.45, stroke_width=0, fill_color=RED, fill_opacity=0.85).move_to([-0.8, -0.7, 0])
        f1 = lines("inactivated in about half\nof pancreatic cancers", 22).move_to([0, -2.1, 0])
        c1 = VGroup(b1, t1, s1, sm4, x1, bar, half, f1)
        self.at("found")
        self.play(FadeIn(b1), FadeIn(t1), FadeIn(s1), FadeIn(sm4), run_time=0.9)
        self.at("inactivated")
        self.play(Create(x1), run_time=0.5)
        self.at("about half")
        self.play(FadeIn(bar), FadeIn(half), FadeIn(f1), run_time=0.7)

        # ---- card 2: myostatin ----
        b2, t2, s2 = card_frame("Myostatin", lines("Se-Jin Lee's\nlaboratory", 22, GREY))
        base = Line([-1.5, -0.9, 0], [1.5, -0.9, 0], color=GREY, stroke_width=3)
        bn = Rectangle(width=0.9, height=0.5, stroke_width=0, fill_color=PINK, fill_opacity=0.8).move_to([-0.8, -0.65, 0])
        bm = Rectangle(width=0.9, height=1.1, stroke_width=0, fill_color=PINK, fill_opacity=0.8).move_to([0.8, -0.35, 0])
        em = DashedVMobject(Rectangle(width=0.9, height=1.65, stroke_color=PINK, stroke_width=3), num_dashes=36).move_to([0.8, -0.075, 0])
        ln = T("normal", 22, GREY).move_to([-0.95, -1.2, 0])
        lm = T("no myostatin", 22, PINK).move_to([0.75, -1.2, 0])
        ideal = T("bars idealised", 22, GREY).move_to([0, 0.95, 0])
        f2 = lines("muscles 2 to 3 times\nthe normal weight", 22).move_to([0, -2.1, 0])
        c2 = VGroup(b2, t2, s2, base, bn, bm, em, ln, lm, ideal, f2)

        # ---- card 3: FOP ----
        b3, t3, s3 = card_frame("FOP", lines("fibrodysplasia\nossificans progressiva", 22, GREY))
        mem3 = Rectangle(width=3.4, height=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to([0, 0.2, 0])
        rec3 = RoundedRectangle(corner_radius=0.15, width=0.6, height=1.6, stroke_color=BLUE, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.3).move_to([0, -0.15, 0])
        gs = Rectangle(width=0.6, height=0.4, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.6).move_to([0, -0.35, 0])
        gsl = T("GS domain", 22, ORANGE).move_to([1.05, -0.35, 0])
        dot = Circle(radius=0.11, stroke_width=0, fill_color=RED, fill_opacity=1).move_to([0.0, -0.35, 0])
        chg = T("same one amino\nacid change", 22, RED).move_to([-1.3, 0.3, 0])
        chg = lines("same one\namino acid\nchange", 22, RED).move_to([-1.2, -0.62, 0])
        rl = T("BMP type I receptor", 22, BLUE).move_to([0, -1.5, 0])
        f3 = lines("muscle and connective\ntissue turn to bone", 22, PINK).move_to([0, -2.1, 0])
        c3 = VGroup(b3, t3, s3, mem3, rec3, gs, gsl, dot, chg, rl, f3)

        # layout: card 1 starts large in the middle and slides left when card 2 arrives
        c1.move_to([0, 0, 0])
        for c, x in ((c2, XS[1]), (c3, XS[2])):
            c.move_to([x, 0, 0])
        self.at("pancreatic cancers")
        self.play(c1.animate.move_to([XS[0], 0, 0]), run_time=0.8)
        self.at("Mice made")
        self.play(FadeIn(b2), FadeIn(t2), FadeIn(s2), run_time=0.4)
        self.at("without the")
        self.play(FadeIn(base), FadeIn(bn), FadeIn(ln), FadeIn(ideal), run_time=0.5)
        self.at("have muscles")
        self.play(FadeIn(bm), Create(em), FadeIn(lm), FadeIn(f2), run_time=0.9)

        self.at("ossificans")
        self.play(FadeIn(b3), FadeIn(t3), FadeIn(s3), run_time=0.7)
        self.at("turn to bone")
        self.play(FadeIn(f3), run_time=0.6)
        self.at("amino acid change")
        self.play(FadeIn(mem3), FadeIn(rec3), FadeIn(rl), run_time=0.6)
        self.at("domain of")
        self.play(FadeIn(gs), FadeIn(gsl), run_time=0.5)
        self.play(FadeIn(dot), FadeIn(chg), run_time=0.5)
        self.finish()


class S05End(EndCard):
    LINE = "A signal this strong has to be kept off most of the time."
