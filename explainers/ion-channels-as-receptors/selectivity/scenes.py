"""A Pore That Pays for Potassium  (Biochemistrypedia section film, Ion channels as receptors lesson)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the channel protein (its walls)
  TEAL   = potassium ions
  ORANGE = sodium ions
  PURPLE = the oxygen lining of the filter (the pay-back)
  RED    = the cost of leaving water, gaps, and what is ruled out
  GREEN  = what the pore pays back
  PINK   = the repulsion between potassium ions
  GOLD   = the laboratory and the year
  GREY   = water coats, labels

No molecular structures: the channel is two blue wall blocks around a pore; ions are sized discs
(radii in the ratio of the lesson's 0.95 and 1.33); the oxygen lining is a plain purple strip; cost and
pay-back are idealised bars. Every drawing is marked "schematic, not to scale".
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#F08BB4"
TEALK = TEAL

CX = -3.6
TOPY, FILT_BOT, BOTY = 2.0, 0.0, -3.0
PW, CAVH = 1.0, 1.0           # filter passage width, cavity half width
RK, RNA = 0.42, 0.30          # radii in the ratio 1.33 : 0.95
XL = 0.45                     # left edge of the right-hand panel text


def ion(color, r, plus=True):
    c = Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.35)
    g = VGroup(c)
    if plus:
        g.add(Line([-r * .45, 0, 0], [r * .45, 0, 0], color=color, stroke_width=3),
              Line([0, -r * .45, 0], [0, r * .45, 0], color=color, stroke_width=3))
    return g


def kion(x=CX, y=0.0):
    return ion(TEAL, RK).move_to([x, y, 0])


def naion(x=CX, y=0.0):
    return ion(ORANGE, RNA).move_to([x, y, 0])


def wall(side):
    s = side
    pts = [(CX + s * 1.9, TOPY), (CX + s * PW / 2, TOPY), (CX + s * PW / 2, FILT_BOT), (CX + s * CAVH, FILT_BOT - 0.55),
           (CX + s * CAVH, BOTY), (CX + s * 1.9, BOTY)]
    back = Polygon(*[[x, y, 0] for x, y in pts], stroke_width=0, fill_color=BG, fill_opacity=1)
    body = Polygon(*[[x, y, 0] for x, y in pts], stroke_color=BLUE, stroke_width=3.5, fill_color=BLUE, fill_opacity=0.4)
    return VGroup(back, body)


def channel():
    g = VGroup(wall(-1), wall(1))
    return g


def lining():
    h = TOPY - FILT_BOT
    return VGroup(*[Rectangle(width=0.1, height=h, stroke_width=0, fill_color=PURPLE, fill_opacity=0.95)
                    .move_to([CX + s * (PW / 2 - 0.05), (TOPY + FILT_BOT) / 2, 0]) for s in (-1, 1)])


def sides():
    o = T("outside", 22, GREY).move_to([-5.85, 3.0, 0])
    i = T("inside", 22, GREY).move_to([-5.9, -3.2, 0])
    sc = T("schematic, not to scale", 22, GREY).move_to([4.75, 3.4, 0])
    return o, i, sc


def halo(x, y, r=0.6):
    return DashedVMobject(Circle(radius=r, stroke_width=3, color=GREY).move_to([x, y, 0]), num_dashes=22)


def bar(y, length, color):
    return Rectangle(width=length, height=0.32, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to([XL + length / 2, y, 0])


def bar_label(text, y, color):
    t = T(text, 24, color)
    return t.move_to([XL + t.width / 2, y, 0])


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


def static_base(scene, lin=False):
    ch = channel()
    o, i, sc = sides()
    scene.add(ch, o, i, sc)
    li = None
    if lin:
        li = lining()
        scene.add(li)
    return ch, li


class S00Title(TitleCard):
    LESSON = "Ion Channels as Receptors"
    TITLE = "A Pore That Pays for Potassium"


class S01Sieve(SpokenScene):
    def construct(self):
        ch = channel()
        o, i, sc = sides()
        self.play(FadeIn(ch), FadeIn(o), FadeIn(i), FadeIn(sc), run_time=1.0)
        self.at("hundred million")
        kchip = chip("K+  up to about 100 million a second", TEAL, size=24).move_to([2.7, 2.4, 0])
        ks = [kion(CX + dx, 3.1) for dx in (0, 0, 0, 0, 0, 0)]
        runs = [Succession(FadeIn(k, run_time=0.15), k.animate(run_time=1.5, rate_func=linear).move_to([CX, -3.2, 0]),
                           FadeOut(k, run_time=0.1)) for k in ks]
        self.play(FadeIn(kchip, shift=LEFT * 0.2), LaggedStart(*runs, lag_ratio=0.4), run_time=4.0)
        self.at("fewer than one sodium")
        nchip = chip("Na+  fewer than 1 for every 1,000 K+", ORANGE, size=24).move_to([2.7, 1.4, 0])
        n1, n2 = naion(CX - 0.1, 3.1), naion(CX + 0.1, 3.1)
        turn = [Succession(FadeIn(n, run_time=0.15), n.animate(run_time=0.5).move_to([CX + dx, TOPY + RNA + 0.08, 0]),
                           n.animate(run_time=0.5).move_to([CX + dx * 4, 3.1, 0]), FadeOut(n, run_time=0.15))
                for n, dx in ((n1, -0.08), (n2, 0.08))]
        self.play(FadeIn(nchip, shift=LEFT * 0.2), LaggedStart(*turn, lag_ratio=0.5), run_time=2.4)
        self.at("smaller ion")
        na = naion(1.3, -0.5)
        k = kion(3.9, -0.5)
        nl = T("Na+  0.95 Å", 24, ORANGE).move_to([1.3, -1.35, 0])
        kl = T("K+  1.33 Å", 24, TEAL).move_to([3.9, -1.35, 0])
        rad = T("radius", 22, GREY).move_to([2.6, 0.35, 0])
        self.play(FadeIn(na, scale=0.5), FadeIn(k, scale=0.5), FadeIn(rad), FadeIn(nl), FadeIn(kl), run_time=1.0)
        self.at("simple sieve")
        sv = chip("a simple sieve", RED, size=28).move_to([2.6, -2.5, 0])
        self.play(FadeIn(sv, shift=UP * 0.15), run_time=0.6)
        self.play(Create(strike(sv)), run_time=0.6)
        self.finish()


class S02Trade(SpokenScene):
    def construct(self):
        ch, _ = static_base(self)
        self.at("Think of it as a trade")
        k = kion(CX, 2.9)
        h = halo(CX, 2.9)
        wl = T("water coat", 22, GREY).move_to([CX + 2.0, 2.9, 0])
        self.play(FadeIn(k), FadeIn(h), FadeIn(wl), run_time=0.8)
        self.at("stripping that coat costs")
        cl = bar_label("cost of stripping the coat", 1.7, RED)
        cb = bar(1.25, 4.0, RED)
        self.play(h.animate.scale(1.5).set_stroke(opacity=0), FadeOut(wl), FadeIn(cl), GrowFromEdge(cb, LEFT), run_time=1.4)
        self.at("narrow pore")
        self.play(k.animate.move_to([CX, TOPY + RK + 0.12, 0]), run_time=0.8)
        self.at("pays the cost back")
        pl = bar_label("paid back by the pore", 0.4, GREEN)
        pb = bar(-0.05, 4.0, GREEN)
        note = T("idealised", 22, GREY).move_to([XL + 0.6, -0.75, 0])
        self.play(FadeIn(pl), GrowFromEdge(pb, LEFT), k.animate.move_to([CX, 1.0, 0]), FadeIn(note), run_time=1.6)
        self.at("Roderick")
        self.play(*[FadeOut(m) for m in (cl, cb, pl, pb, note)], run_time=0.6)
        who = chip("1998 · Roderick MacKinnon's laboratory", GOLD, size=24).move_to([2.2, 1.9, 0])
        self.play(FadeIn(who, shift=LEFT * 0.2), run_time=0.7)
        self.at("structure of")
        kc = chip("KcsA", BLUE, size=32).move_to([0.6, 0.5, 0])
        ar = Arrow(kc.get_left(), [CX + 1.95, -0.6, 0], buff=0.1, color=BLUE, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(kc, scale=0.8), GrowArrow(ar), run_time=0.8)
        self.at("soil bacterium")
        sb = T("a potassium channel from a soil bacterium", 24, TEXT).move_to([2.6, -0.7, 0])
        self.play(FadeIn(sb, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S03Filter(SpokenScene):
    def construct(self):
        ch, _ = static_base(self)
        self.at("Four identical subunits")
        sub = chip("4 identical subunits, 1 pore", BLUE, size=24).move_to([1.8, 2.65, 0])
        sar = Arrow(sub.get_left(), [CX + 1.5, 2.08, 0], buff=0.1, color=BLUE, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(sub, shift=LEFT * 0.2), GrowArrow(sar), run_time=0.9)
        self.at("selectivity filter")
        br = DoubleArrow([CX + 2.15, TOPY, 0], [CX + 2.15, FILT_BOT, 0], buff=0, color=TEXT, stroke_width=4, tip_length=0.18)
        fc = chip("selectivity filter, 12 Å long", TEXT, size=24).move_to([2.55, 1.45, 0])
        # keep the chip clear of the bracket
        fc.next_to(br, RIGHT, buff=0.2)
        self.play(GrowFromCenter(br), FadeIn(fc, shift=LEFT * 0.2), run_time=0.9)
        self.at("too tight for an ion")
        k = kion(CX, 2.9)
        h = halo(CX, 2.9)
        self.play(FadeIn(k), FadeIn(h), run_time=0.6)
        self.play(k.animate.move_to([CX, TOPY + RK + 0.12, 0]), h.animate.move_to([CX, TOPY + RK + 0.12, 0]), run_time=0.7)
        self.at("keep its water")
        self.play(h.animate.scale(1.5).set_stroke(opacity=0), run_time=0.8)
        self.at("carbonyl oxygen atoms")
        li = lining()
        oc = chip("carbonyl oxygens of the backbone", PURPLE, size=22).move_to([2.2, -0.1, 0])
        oc.shift(RIGHT * 0.0)
        oar = Arrow(oc.get_left(), [CX + 0.5, 0.8, 0], buff=0.1, color=PURPLE, stroke_width=4, tip_length=0.2)
        self.play(GrowFromEdge(li[0], DOWN), GrowFromEdge(li[1], DOWN), FadeIn(oc, shift=LEFT * 0.2), GrowArrow(oar), run_time=1.2)
        self.at("surround a potassium ion")
        self.play(k.animate.move_to([CX, 1.0, 0]), run_time=1.2)
        self.at("swaps water for protein")
        cl = bar_label("water coat lost", -0.95, RED)
        cb = bar(-1.35, 4.0, RED)
        pl = bar_label("paid back by the oxygens", -2.0, GREEN)
        pb = bar(-2.4, 3.8, GREEN)
        self.play(FadeIn(cl), GrowFromEdge(cb, LEFT), FadeIn(pl), GrowFromEdge(pb, LEFT), run_time=1.6)
        self.at("loses almost nothing")
        net = T("net loss: almost nothing", 24, TEAL).move_to([XL + 2.1, -3.05, 0])
        self.play(FadeIn(net, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S04Sodium(SpokenScene):
    def construct(self):
        ch, li = static_base(self, lin=True)
        self.at("Sodium is too small")
        ghost = DashedVMobject(Circle(radius=RNA, stroke_width=3, color=ORANGE).move_to([CX, 1.0, 0]), num_dashes=14)
        c1 = chip("if sodium entered the filter", ORANGE, size=24).move_to([1.8, 2.4, 0])
        self.play(FadeIn(ghost, scale=2.0), FadeIn(c1, shift=LEFT * 0.2), run_time=0.9)
        self.at("touch all the oxygens")
        gl = [Line([CX + s * RNA, 1.0, 0], [CX + s * PW / 2, 1.0, 0], color=RED, stroke_width=7) for s in (-1, 1)]
        c2 = chip("gaps: it cannot touch every oxygen", RED, size=22).move_to([1.8, 1.3, 0])
        self.play(*[Create(g) for g in gl], FadeIn(c2, shift=LEFT * 0.2), run_time=0.9)
        self.at("held too stiffly")
        c3 = chip("filter held stiff, does not close in", PURPLE, size=22).move_to([1.8, 0.2, 0])
        self.play(FadeIn(c3, shift=LEFT * 0.2), run_time=0.8)
        self.at("leaving water costs")
        na = naion(CX, 2.9)
        h = halo(CX, 2.9)
        cl = bar_label("cost of leaving water", -1.0, RED)
        cb = bar(-1.4, 4.0, RED)
        self.play(*[FadeOut(m) for m in (ghost, c1, c2, c3, *gl)], FadeIn(na), FadeIn(h), FadeIn(cl), GrowFromEdge(cb, LEFT), run_time=1.2)
        self.at("more than the filter repays")
        pl = bar_label("paid back by the filter", -2.0, GREEN)
        pb = bar(-2.4, 1.6, GREEN)
        self.play(FadeIn(pl), GrowFromEdge(pb, LEFT), run_time=1.0)
        self.at("stays outside")
        so = chip("sodium stays outside", ORANGE, size=26).move_to([1.8, 1.7, 0])
        self.play(FadeIn(so, shift=LEFT * 0.2), na.animate.shift(UP * 0.0).set_run_time(0.4), run_time=0.8)
        self.at("Two potassium ions")
        self.play(*[FadeOut(m) for m in (na, h, cl, cb, pl, pb, so)], run_time=0.7)
        k1, k2 = kion(CX, 0.5), kion(CX, 1.5)
        sf = chip("single file", TEAL, size=26).move_to([1.8, 1.6, 0])
        self.play(FadeIn(k1, scale=0.5), FadeIn(k2, scale=0.5), FadeIn(sf, shift=LEFT * 0.2), run_time=0.8)
        self.at("repulsion between them")
        k3 = kion(CX, 3.0)
        self.add(k3)
        rc = chip("repulsion", PINK, size=26).move_to([1.8, 0.4, 0])
        pa = [DoubleArrow([CX, 1.97, 0], [CX, 2.53, 0], buff=0, color=PINK, stroke_width=6, tip_length=0.15)]
        self.play(FadeIn(rc, shift=LEFT * 0.2), *[GrowArrow(a) for a in pa], run_time=0.8)
        self.at("pushes one out")
        self.play(*[FadeOut(a) for a in pa], k1.animate.move_to([CX, -1.0, 0]).set_opacity(0),
                  k2.animate.move_to([CX, 0.5, 0]), k3.animate.move_to([CX, 1.5, 0]), run_time=1.4)
        self.at("answer for potassium channels")
        self.play(FadeOut(rc), FadeOut(sf), run_time=0.4)
        oth = chip("sodium and calcium channels: different filters", GREY, size=24).move_to([2.9, 1.0, 0])
        self.play(FadeIn(oth, shift=LEFT * 0.2), run_time=0.8)
        self.finish()


class S05End(EndCard):
    LINE = "An ion enters a pore only if the pore pays the cost back."
