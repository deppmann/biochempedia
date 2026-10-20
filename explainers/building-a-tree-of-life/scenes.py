"""Building a tree of life: relatives are found by inherited traits  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = whale, and the mammal branch it sits on
  ORANGE = hippo
  PURPLE = tuna / fish
  YELLOW = lines of evidence (body parts, embryos, fossils, DNA)
  GOLD   = common ancestor / branch point
  GREEN  = a shared derived characteristic (lungs and milk, hair) and "agree"
  RED    = crossed out / ruled out
  PINK   = pharyngeal arches (s04)
  SAND   = embryo tail (s04)
  GREY   = outlines, labels, de-emphasised
  s03 only: bone colours TEAL (upper arm), PINK2 (forearm), SAND2 (wrist), LIME (finger)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB5"
SAND = "#C8A27A"
LIME = "#A8D672"
TEALB = "#3FB8C0"


def block(w, h, color, text=None, size=22, op=0.3):
    r = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=op)
    if text:
        return VGroup(r, T(text, size, TEXT).move_to(r))
    return VGroup(r)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def ln(a, b, color=GREY, w=5):
    return Line([a[0], a[1], 0], [b[0], b[1], 0], color=color, stroke_width=w)


def cross(c, color=RED):
    return Line(c.get_corner(DL) + [-0.1, -0.1, 0], c.get_corner(UR) + [0.1, 0.1, 0], color=color, stroke_width=6)


class S00Title(TitleCard):
    LESSON = "Building a Tree of Life"
    TITLE = "Relatives are found by inherited traits"


# ---------------------------------------------------------------------------------------------
class S01Whale(SpokenScene):
    def construct(self):
        whale = chip("whale", BLUE, size=54).move_to([0, 1.0, 0])
        tuna = chip("tuna", PURPLE, size=46).move_to([-4.7, 1.0, 0])
        hippo = chip("hippo", ORANGE, size=46).move_to([4.7, 1.0, 0])
        self.at("A whale swims")
        self.play(FadeIn(whale, scale=0.8), run_time=0.7)
        self.at("shaped like a fish")
        link1 = DashedLine(tuna.get_right() + [0.1, 0, 0], whale.get_left() - [0.1, 0, 0], color=GREY, stroke_width=4)
        lab1 = T("same body\nshape", 24, GREY, line_spacing=0.8).next_to(link1, UP, buff=0.12)
        self.play(FadeIn(tuna, shift=RIGHT * 0.3), Create(link1), FadeIn(lab1), run_time=0.9)
        lungs = chip("lungs: breathes air", BLUE, size=32).move_to([-2.5, -0.7, 0])
        milk = chip("milk for young", BLUE, size=32).move_to([2.6, -0.7, 0])
        self.at("breathes air")
        self.play(FadeIn(lungs, shift=UP * 0.2), run_time=0.6)
        self.at("milk")
        self.play(FadeIn(milk, shift=UP * 0.2), run_time=0.6)
        self.at("closest living relatives")
        link2 = Line(whale.get_right() + [0.1, 0, 0], hippo.get_left() - [0.1, 0, 0], color=GREEN, stroke_width=5)
        lab2 = T("closest living\nrelatives", 24, GREEN, line_spacing=0.8).next_to(link2, UP, buff=0.12)
        self.play(FadeIn(hippo, shift=LEFT * 0.3), Create(link2), FadeIn(lab2), run_time=0.9)
        q = T("Who is related to whom?", 52, font=TITLE_FONT).move_to([0, -2.5, 0])
        self.at("how do scientists")
        self.play(Write(q), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Evidence(SpokenScene):
    def construct(self):
        head = T("Classification", 44, font=TITLE_FONT).move_to([0, 2.9, 0])
        sub = T("grouping living things by how they are related", 26, GREY).next_to(head, DOWN, buff=0.15)
        self.at("Scientists group")
        self.play(Write(head), FadeIn(sub), run_time=1.0)
        no = [chip("looks", GREY, 40), chip("home", GREY, 40), chip("diet", GREY, 40)]
        VGroup(*no).arrange(RIGHT, buff=0.9).move_to([0, 0.9, 0])
        self.at("looks")
        self.play(FadeIn(no[0], shift=UP * 0.2), run_time=0.4)
        self.at("home")
        self.play(FadeIn(no[1], shift=UP * 0.2), run_time=0.4)
        self.at("diet")
        self.play(FadeIn(no[2], shift=UP * 0.2), run_time=0.4)
        self.at("Those can match")
        note = T("can match in animals that are not close relatives", 30, GREY).move_to([0, -0.2, 0])
        crs = [cross(c) for c in no]
        self.play(*[Create(x) for x in crs], FadeIn(note), run_time=0.8)
        self.at("Instead")
        insp = T("compare inherited evidence", 40, YELLOW, weight=BOLD).move_to([0, 0.4, 0])
        self.play(FadeOut(VGroup(*no, *crs)), FadeOut(note), run_time=0.4)
        self.play(FadeIn(insp, shift=UP * 0.15), run_time=0.5)
        ev = [chip("body parts", YELLOW, 34), chip("embryos", YELLOW, 34), chip("fossils", YELLOW, 34), chip("DNA", YELLOW, 34)]
        VGroup(*ev).arrange(RIGHT, buff=0.35).move_to([0, -1.4, 0])
        self.at("body parts")
        self.play(FadeIn(ev[0], shift=UP * 0.2), run_time=0.4)
        self.at("embryos")
        self.play(FadeIn(ev[1], shift=UP * 0.2), run_time=0.4)
        self.at("fossils")
        self.play(FadeIn(ev[2], shift=UP * 0.2), run_time=0.4)
        self.at("DNA")
        self.play(FadeIn(ev[3], shift=UP * 0.2), run_time=0.4)
        self.at("agree")
        evg = VGroup(*ev)
        br = Brace(evg, DOWN, color=GREEN, buff=0.15)
        agree = T("agree", 40, GREEN, weight=BOLD).next_to(br, DOWN, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(agree), evg.animate.set_color(GREEN), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Limbs(SpokenScene):
    """three forelimbs as labelled blocks, matching blocks the same colour."""

    def limb(self, x):
        up = block(0.9, 0.8, TEALB)
        fa = VGroup(block(0.42, 0.8, PINK, op=0.3), block(0.42, 0.8, PINK, op=0.3)).arrange(RIGHT, buff=0.06)
        wr = block(0.9, 0.4, SAND)
        fi = block(0.9, 0.7, LIME)
        g = VGroup(up, fa, wr, fi).arrange(DOWN, buff=0.08)
        g.scale(1.2).move_to([x, 1.4, 0])
        g.parts = (up, fa, wr, fi)
        return g

    def construct(self):
        xs = [-2.0, 1.4, 4.8]
        names = ["human", "bat", "whale"]
        funcs = ["hand grasps", "wing flies", "flipper steers"]
        limbs, nlabs, flabs = [], [], []
        for x, n, f in zip(xs, names, funcs):
            limbs.append(self.limb(x))
            nlabs.append(T(n, 28, TEXT, weight=BOLD).move_to([x, -0.78, 0]))
            flabs.append(T(f, 24, GREY).move_to([x, -1.25, 0]))
        self.at("front limb")
        self.play(FadeIn(limbs[0], shift=UP * 0.2), FadeIn(nlabs[0]), run_time=0.6)
        self.at("bat")
        self.play(FadeIn(limbs[1], shift=UP * 0.2), FadeIn(nlabs[1]), run_time=0.6)
        self.at("whale")
        self.play(FadeIn(limbs[2], shift=UP * 0.2), FadeIn(nlabs[2]), run_time=0.6)
        for i, w in enumerate(["grasps", "flies", "steers"]):
            self.at(w)
            self.play(FadeIn(flabs[i]), run_time=0.4)
        bone_names = [("upper arm bone", TEALB, 0), ("two forearm bones", PINK, 1), ("wrist bones", SAND, 2), ("finger bones", LIME, 3)]
        cues = ["upper arm bone", "two forearm bones", "wrist bones", "finger bones"]
        labs = []
        for (txt, col, k), cue in zip(bone_names, cues):
            ref = limbs[0].parts[k]
            lab = T(txt, 22, col).move_to([-4.65, ref.get_center()[1], 0])
            lab.align_to([-6.25, 0, 0], LEFT)
            labs.append(lab)
            self.at(cue)
            self.play(FadeIn(lab, shift=RIGHT * 0.2),
                      *[Indicate(l.parts[k], color=col, scale_factor=1.12) for l in limbs], run_time=0.8)
        self.at("homologous structures")
        br = Brace(VGroup(*flabs), DOWN, color=YELLOW, buff=0.15)
        hom = T("homologous structures", 32, YELLOW, weight=BOLD).next_to(br, DOWN, buff=0.12)
        self.play(GrowFromCenter(br), FadeIn(hom), run_time=0.8)
        self.at("common ancestor")
        anc = chip("common ancestor", GOLD, size=28).move_to([1.4, -3.15, 0])
        ar = arr(anc.get_top(), hom.get_bottom(), GOLD, tip=0.18)
        self.play(FadeIn(anc, shift=UP * 0.2), GrowArrow(ar), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Embryos(SpokenScene):
    def row(self, y, name):
        body = RoundedRectangle(corner_radius=0.5, width=4.0, height=1.2, stroke_color=GREY, stroke_width=3).move_to([-2.6, y, 0])
        nm = T(name, 30, TEXT, weight=BOLD).move_to([-5.6, y, 0])
        arch = block(1.1, 0.8, PINK).move_to([-4.0, y, 0])
        tail = block(0.8, 0.3, SAND).move_to([-0.2, y, 0])
        return body, nm, arch, tail

    def construct(self):
        head = T("Embryos", 40, font=TITLE_FONT).move_to([-4.2, 3.05, 0])
        rows = {"fish": self.row(1.9, "fish"), "chick": self.row(0.4, "chick"), "human": self.row(-1.1, "human")}
        self.at("Embryos can share")
        self.play(Write(head), run_time=0.7)
        self.at("Early fish")
        self.play(*[FadeIn(m) for m in rows["fish"][:2]], run_time=0.5)
        self.at("chick")
        self.play(*[FadeIn(m) for m in rows["chick"][:2]], run_time=0.5)
        self.at("human embryos", nth=0)
        self.play(*[FadeIn(m) for m in rows["human"][:2]], run_time=0.5)
        self.at("a tail")
        tl = T("tail", 24, SAND)
        self.play(*[FadeIn(r[3], shift=LEFT * 0.2) for r in rows.values()], run_time=0.7)
        tl.move_to([-0.2, -2.0, 0])
        self.play(FadeIn(tl), run_time=0.3)
        self.at("pharyngeal arches")
        self.play(*[FadeIn(r[2]) for r in rows.values()], run_time=0.7)
        al = T("pharyngeal arches", 24, PINK).move_to([-4.0, -2.0, 0])
        self.play(FadeIn(al), run_time=0.3)
        fish_out = chip("several arches support gills", PINK, size=24).move_to([3.5, 1.9, 0])
        hum_out = chip("arches become jaw, ear, throat", PINK, size=24).move_to([3.4, -1.1, 0])
        cp1 = rows["fish"][2].copy()
        self.at("support gills")
        self.play(cp1.animate.move_to(fish_out.get_left() + [0.5, 0, 0]), run_time=0.7)
        self.play(FadeOut(cp1), FadeIn(fish_out), run_time=0.3)
        cp2 = rows["human"][2].copy()
        self.at("jaw")
        self.play(cp2.animate.move_to(hum_out.get_left() + [0.5, 0, 0]), run_time=0.7)
        self.play(FadeOut(cp2), FadeIn(hum_out), run_time=0.3)
        no = T("Human embryos do not turn into fish first.", 34, RED).move_to([0, -3.1, 0])
        self.at("do not turn into fish")
        self.play(FadeIn(no, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Cladogram(SpokenScene):
    def construct(self):
        head = T("Cladogram", 44, font=TITLE_FONT).move_to([-4.6, 3.0, 0])
        self.at("A cladogram")
        self.play(Write(head), run_time=0.7)
        nx = -2.0
        root = ln([-5.6, 0], [nx, 0])
        v = ln([nx, 1.6], [nx, -1.8])
        up = ln([nx, 1.6], [2.4, 1.6])
        dn = ln([nx, -1.8], [2.4, -1.8])
        dn2 = ln([nx, -0.3], [2.4, -0.3])
        self.at("branching diagram")
        self.play(Create(root), run_time=0.6)
        self.at("order in which groups split")
        self.play(Create(v), run_time=0.5)
        self.play(Create(up), Create(dn), Create(dn2), run_time=0.7)
        node = Dot([nx, 0, 0], radius=0.16, color=GOLD)
        nlab = T("branch point:\ncommon ancestor", 24, GOLD, line_spacing=0.8).move_to([-3.85, 0.65, 0])
        self.at("common ancestors")
        self.play(FadeIn(node, scale=2), FadeIn(nlab), run_time=0.6)
        sdc = T("shared derived characteristic", 32, GREEN, weight=BOLD).move_to([0, -3.0, 0])
        self.at("shared derived characteristics")
        self.play(FadeIn(sdc, shift=UP * 0.15), run_time=0.7)
        self.at("first appeared in one ancestor")
        self.play(Indicate(node, color=GOLD, scale_factor=2.0), run_time=0.8)
        tick = Line([0.0, 1.35, 0], [0.0, 1.85, 0], color=GREEN, stroke_width=8)
        hair = T("hair", 30, GREEN, weight=BOLD).move_to([0.0, 2.25, 0])
        self.at("Hair is one")
        self.play(Create(tick), FadeIn(hair, shift=DOWN * 0.15), run_time=0.7)
        mam = chip("mammals", BLUE, size=36).move_to([4.2, 1.6, 0])
        self.at("Mammals share it")
        self.play(FadeIn(mam, shift=LEFT * 0.3), run_time=0.7)
        nohair = VGroup(chip("frogs", GREY, size=34).move_to([4.2, -0.3, 0]), chip("fish", GREY, size=34).move_to([4.2, -1.8, 0]))
        nh_lab = T("no hair", 30, GREY, weight=BOLD).move_to([0.0, -1.05, 0])
        self.at("fish and frogs")
        self.play(FadeIn(nohair, shift=LEFT * 0.3), FadeIn(nh_lab), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        ax = -4.6
        root = ln([-6.0, 0.0], [ax, 0.0])
        va = ln([ax, -1.9], [ax, 1.0])
        low = ln([ax, -1.9], [2.5, -1.9], PURPLE)
        upl = ln([ax, 1.0], [-1.5, 1.0], BLUE)
        tuna = chip("tuna", PURPLE, size=32).move_to([3.9, -1.9, 0])
        whale = chip("whale", BLUE, size=32).move_to([3.9, 1.0, 0])
        qmark = T("?", 40, GREY).move_to([5.6, 1.0, 0])
        self.at("Now place")
        self.play(Create(root), Create(va), Create(low), Create(upl), FadeIn(tuna, shift=LEFT * 0.2), FadeIn(whale, shift=LEFT * 0.2), FadeIn(qmark), run_time=1.0)
        tick = Line([-3.3, 0.75, 0], [-3.3, 1.25, 0], color=GREEN, stroke_width=8)
        trait = T("lungs, milk", 28, GREEN, weight=BOLD).move_to([-3.3, 1.65, 0])
        self.at("Lungs and milk")
        self.play(Create(tick), FadeIn(trait, shift=DOWN * 0.15), run_time=0.7)
        vb = ln([-1.5, 0.2], [-1.5, 1.8], BLUE)
        upw = ln([-1.5, 1.8], [2.5, 1.8], BLUE)
        node = Dot([-1.5, 1.0, 0], radius=0.16, color=GOLD)
        nlab = T("common\nancestor", 24, GOLD, line_spacing=0.8).move_to([-2.45, 0.2, 0])
        hippo = chip("hippo", ORANGE, size=32).move_to([3.9, 0.2, 0])
        hl = ln([-1.5, 0.2], [2.5, 0.2], ORANGE)
        self.at("mammals")
        self.play(Create(vb), FadeOut(qmark), whale.animate.move_to([3.9, 1.8, 0]), Create(upw), Create(hl),
                  FadeIn(hippo, shift=LEFT * 0.2), FadeIn(node, scale=2), FadeIn(nlab), run_time=0.9)
        ev = [chip("fossils", YELLOW, 24), chip("embryos", YELLOW, 24), chip("DNA", YELLOW, 24)]
        VGroup(*ev).arrange(RIGHT, buff=0.3).move_to([-0.3, 3.0, 0])
        self.at("Fossil whales")
        self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.15) for e in ev], lag_ratio=0.4), run_time=1.0)
        self.at("point the same way")
        agree = T("agree", 30, GREEN, weight=BOLD).next_to(VGroup(*ev), RIGHT, buff=0.4)
        self.play(FadeIn(agree), run_time=0.5)
        shape = T("fishlike shape: fits life in water", 26, GREY).move_to([-0.1, -0.85, 0])
        self.at("shape fits life")
        self.play(FadeIn(shape), run_time=0.7)
        rule = T("Judge relatives by inherited traits, not by looks.", 32, font=TITLE_FONT)
        fit(rule, max_w=11.8)
        rule.move_to([0, -3.1, 0])
        self.at("Keep this rule")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Judge relatives by inherited traits, not by looks."
