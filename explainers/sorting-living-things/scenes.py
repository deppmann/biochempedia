"""Sorting living things: one name for every living thing  (grade 7 Life Science explainer)

COLOR MAP (one color per concept, whole film)
  YELLOW = the common name "buzzard" (the mix-up)
  BLUE   = scientific names and the genus word
  ORANGE = a species and the species word
  TEAL   = the eight levels of classification
  PURPLE = the dichotomous key
  GREEN  = "same living thing", the answer, pair that shares more levels
  RED    = the question, limits, "does not show"
  GREY   = panels, outlines, neutral structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"


def Ti(text, size=40, color=BLUE, **kw):
    return T(text, size, color, slant=ITALIC, **kw)


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def panel(w, h, x, y, color=GREY):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.05).move_to([x, y, 0])


def box(w, h, color, x=0, y=0, op=0.14):
    return RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=op).move_to([x, y, 0])


NAME_Y = 0.95


def name_boxes():
    b1 = box(5.2, 1.8, BLUE)
    b2 = box(4.6, 1.8, ORANGE)
    g = VGroup(b1, b2).arrange(RIGHT, buff=0.3).move_to([0, NAME_Y, 0])
    return g


class S00Title(TitleCard):
    LESSON = "Sorting living things"
    TITLE = "One name for every living thing"


# ---------------------------------------------------------------------------------------------
class S01Buzzard(SpokenScene):
    def construct(self):
        pv = panel(5.9, 5.4, -3.4, 0.1)
        pb = panel(5.9, 5.4, 3.4, 0.1)
        tv = T("In Virginia", 40, TEXT, weight=BOLD).move_to([-3.4, 2.05, 0])
        tb = T("In Britain", 40, TEXT, weight=BOLD).move_to([3.4, 2.05, 0])
        wv = chip("buzzard", YELLOW, size=44).move_to([-3.4, 0.85, 0])
        wb = chip("buzzard", YELLOW, size=44).move_to([3.4, 0.85, 0])
        sv = T("some people call a", 30, GREY).move_to([-3.4, -0.2, 0])
        sb = T("is a kind of", 30, GREY).move_to([3.4, -0.2, 0])
        av = arr([-3.4, -0.55, 0], [-3.4, -1.15, 0], YELLOW)
        ab = arr([3.4, -0.55, 0], [3.4, -1.15, 0], YELLOW)
        bv = chip("vulture", BLUE, size=44).move_to([-3.4, -1.85, 0])
        bb = chip("hawk", BLUE, size=44).move_to([3.4, -1.85, 0])
        self.at("In Virginia")
        self.play(FadeIn(pv), FadeIn(tv), FadeIn(wv), run_time=0.7)
        self.at("some people call")
        self.play(FadeIn(sv), GrowArrow(av), FadeIn(bv), run_time=0.8)
        self.at("In Britain")
        self.play(FadeIn(pb), FadeIn(tb), FadeIn(wb), run_time=0.7)
        self.at("kind of hawk")
        self.play(FadeIn(sb), GrowArrow(ab), FadeIn(bb), run_time=0.8)
        q = T("?", 110, RED, weight=BOLD).move_to([0, 0.3, 0])
        self.at("which bird")
        self.play(FadeIn(q, scale=1.4), run_time=0.5)
        self.play(Indicate(q, color=RED, scale_factor=1.2), run_time=0.8)
        note = T("one name, different birds", 36, YELLOW).move_to([0, -3.25, 0])
        self.at("different birds")
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Species(SpokenScene):
    def construct(self):
        one = chip("one name for each kind of living thing", BLUE, size=38).move_to([0, 3.0, 0])
        self.at("one name for each")
        self.play(FadeIn(one, shift=DOWN * 0.15), run_time=0.7)
        sp = T("species", 60, ORANGE, weight=BOLD).move_to([-4.5, 0.4, 0])
        c1 = chip("similar-looking organisms", ORANGE, size=36)
        c2 = chip("can mate in nature", ORANGE, size=36)
        c3 = chip("young that can also reproduce", ORANGE, size=36)
        col = VGroup(c1, c2, c3).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([2.4, 0.35, 0])
        self.at("A species")
        self.play(Write(sp), run_time=0.7)
        self.at("looking organisms")
        self.play(FadeIn(c1, shift=RIGHT * 0.2), run_time=0.6)
        self.at("can mate in nature")
        self.play(FadeIn(c2, shift=RIGHT * 0.2), run_time=0.6)
        self.at("young that can also")
        self.play(FadeIn(c3, shift=RIGHT * 0.2), run_time=0.6)
        lim = chip("it has limits", RED, size=34).move_to([-4.6, -2.5, 0])
        l1 = T("not for organisms that reproduce without sex", 26, GREY).move_to([1.9, -2.2, 0])
        l2 = T("some different species do sometimes mate in nature", 26, GREY).move_to([1.9, -3.0, 0])
        self.at("It does not fit")
        self.play(FadeIn(lim, scale=1.2), FadeIn(l1), run_time=0.6)
        self.at("some different species")
        self.play(FadeIn(l2), run_time=0.6)
        # clear, then bring in the two empty name boxes
        self.at("scientific name")
        self.play(*[FadeOut(m) for m in (one, sp, c1, c2, c3, lim, l1, l2)], run_time=0.5)
        nb = name_boxes()
        w1 = T("first word", 36, BLUE).move_to(nb[0])
        w2 = T("second word", 36, ORANGE).move_to(nb[1])
        cap = T("binomial nomenclature", 44, TEXT, weight=BOLD).move_to([0, -0.9, 0])
        self.play(FadeIn(nb), FadeIn(w1), FadeIn(w2), run_time=0.7)
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Names(SpokenScene):
    def construct(self):
        nb = name_boxes()
        w1 = T("first word", 36, BLUE).move_to(nb[0])
        w2 = T("second word", 36, ORANGE).move_to(nb[1])
        cap = T("binomial nomenclature", 44, TEXT, weight=BOLD).move_to([0, -0.9, 0])
        self.add(nb, w1, w2, cap)
        self.at("first word of the name")
        g_lbl = T("genus", 46, BLUE, weight=BOLD).move_to([nb[0].get_center()[0], 2.4, 0])
        g_def = T("a small group of closely related species", 34, BLUE).move_to([0, -0.5, 0])
        self.play(FadeOut(cap), FadeIn(g_lbl, shift=DOWN * 0.1), run_time=0.6)
        self.play(Indicate(nb[0], color=BLUE, scale_factor=1.06), FadeIn(g_def), run_time=0.8)
        s_lbl = T("species", 46, ORANGE, weight=BOLD).move_to([nb[1].get_center()[0], 2.4, 0])
        s_def = T("one species in that genus", 34, ORANGE).move_to([0, -1.15, 0])
        self.at("second word names")
        self.play(FadeIn(s_lbl, shift=DOWN * 0.1), Indicate(nb[1], color=ORANGE, scale_factor=1.06),
                  FadeIn(s_def), run_time=0.8)

        def fill(a, b):
            ta = Ti(a, 66, BLUE).move_to(nb[0])
            tb = Ti(b, 66, ORANGE).move_to(nb[1])
            return ta, tb

        ta, tb = fill("Cathartes", "aura")
        lab = T("turkey vulture", 44, TEXT).move_to([0, -0.95, 0])
        self.at("The turkey vulture is")
        self.play(FadeOut(w1), FadeOut(w2), FadeOut(g_def), FadeOut(s_def), run_time=0.4)
        self.play(FadeIn(lab), Write(ta), run_time=0.7)
        self.play(Write(tb), run_time=0.5)
        ta2, tb2 = fill("Coragyps", "atratus")
        lab2 = T("black vulture", 44, TEXT).move_to([0, -0.95, 0])
        self.at("The black vulture is")
        self.play(Transform(ta, ta2), Transform(tb, tb2), Transform(lab, lab2), run_time=0.8)
        self.at("capital letter")
        ca = SurroundingRectangle(ta[0], color=YELLOW, buff=0.06, stroke_width=4)
        self.play(Create(ca), run_time=0.4)
        self.at("second word is lowercase")
        cb = SurroundingRectangle(tb[0], color=YELLOW, buff=0.1, stroke_width=4)
        self.play(ReplacementTransform(ca, cb), run_time=0.5)
        ta3, tb3 = fill("Cathartes", "aura")
        lab3 = T("turkey vulture", 44, TEXT).move_to([0, -0.95, 0])
        self.at("A scientist in Japan")
        self.play(FadeOut(cb), Transform(ta, ta3), Transform(tb, tb3), Transform(lab, lab3), run_time=0.7)
        jp = chip("a scientist in Japan", TEXT, size=30).move_to([-4.1, -2.9, 0])
        va = chip("you in Virginia", TEXT, size=30).move_to([4.1, -2.9, 0])
        aj = arr([-4.1, -2.4, 0], [-2.9, -0.15, 0], TEXT)
        av = arr([4.1, -2.4, 0], [2.9, -0.15, 0], TEXT)
        self.play(FadeIn(jp), GrowArrow(aj), run_time=0.6)
        self.at("means the same bird")
        self.play(FadeIn(va), GrowArrow(av), run_time=0.6)
        same = T("same bird", 44, GREEN, weight=BOLD).move_to([0, -2.9, 0])
        self.play(FadeIn(same, scale=1.2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
LEVELS = ["domain", "kingdom", "phylum", "class", "order", "family", "genus", "species"]


class S04Levels(SpokenScene):
    def construct(self):
        step = 0.78
        top = 2.4
        rows = []
        for i, n in enumerate(LEVELS):
            c = chip(n, TEAL, size=32)
            c.move_to([-5.4 + c.width / 2 + 0.4 * i, top - step * i, 0])
            rows.append(c)
        hi = T("most general", 30, GREY).move_to([-4.2, 3.3, 0])
        lo = T("most specific", 30, GREY).move_to([2.6, top - step * 7, 0])
        loa = arr([rows[7].get_right()[0] + 0.1, top - step * 7, 0], [lo.get_left()[0] - 0.15, top - step * 7, 0], GREY)
        ph = VGroup(*[box(r.width, r.height, GREY, x=r.get_center()[0], y=r.get_center()[1], op=0.04) for r in rows])
        self.at("eight levels")
        self.play(FadeIn(hi), LaggedStart(*[FadeIn(p) for p in ph], lag_ratio=0.12), run_time=1.2)
        nth = {"species": 1}
        for i, c in enumerate(rows):
            self.at(LEVELS[i], lead=0.15, nth=nth.get(LEVELS[i], 0))
            self.play(FadeOut(ph[i]), FadeIn(c, shift=RIGHT * 0.2), run_time=0.3)
        self.play(GrowArrow(loa), FadeIn(lo), run_time=0.5)
        dom = VGroup(*[chip(n, TEAL, size=30) for n in ("Archaea", "Bacteria", "Eukarya")]).arrange(RIGHT, buff=0.25)
        dom.move_to([0, top, 0]).set_x(-1.6 + dom.width / 2)
        da = arr([rows[0].get_right()[0] + 0.1, top, 0], [dom.get_left()[0] - 0.1, top, 0], TEAL)
        kg = VGroup(chip("plants", TEAL, size=30), chip("animals", TEAL, size=30)).arrange(RIGHT, buff=0.3)
        kg.move_to([0, top - step, 0]).set_x(-1.6 + kg.width / 2)
        ka = arr([rows[1].get_right()[0] + 0.1, top - step, 0], [kg.get_left()[0] - 0.1, top - step, 0], TEAL)
        self.at("A domain is the largest")
        self.play(Indicate(rows[0], color=TEAL, scale_factor=1.15), run_time=0.6)
        self.at("There are three")
        self.play(GrowArrow(da), LaggedStart(*[FadeIn(d, shift=LEFT * 0.2) for d in dom], lag_ratio=0.3), run_time=1.2)
        self.at("Plants and animals")
        self.play(Indicate(rows[1], color=TEAL, scale_factor=1.15), GrowArrow(ka), FadeIn(kg), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Share(SpokenScene):
    def construct(self):
        cy = -0.1
        ws = [5.2, 4.2, 3.2, 2.2]
        addr_names = ["country", "state", "city", "street"]
        ab = VGroup()
        for w, n in zip(ws, addr_names):
            b = box(w, 0.85, GREY, op=0.1)
            t = T(n, 34, TEXT).move_to(b)
            ab.add(VGroup(b, t))
        ab.arrange(DOWN, buff=0.3).move_to([-3.4, cy, 0])
        ah = T("mailing address", 38, GREY, weight=BOLD).move_to([-3.4, 3.0, 0])
        self.at("mailing address")
        self.play(FadeIn(ah), run_time=0.5)
        for i, n in enumerate(addr_names):
            self.at(n, lead=0.15)
            self.play(FadeIn(ab[i], scale=0.9), run_time=0.35)
        wl = np.linspace(5.4, 1.8, 8)
        cb = VGroup()
        for w, n in zip(wl, LEVELS):
            b = box(w, 0.52, TEAL, op=0.12)
            t = T(n, 26, TEXT).move_to(b)
            cb.add(VGroup(b, t))
        cb.arrange(DOWN, buff=0.1).move_to([3.4, cy, 0])
        ch = T("levels of classification", 36, TEAL, weight=BOLD).move_to([3.4, 3.0, 0])
        self.at("levels of classification")
        self.play(FadeIn(ch), LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in cb], lag_ratio=0.12), run_time=1.6)
        self.at("Organisms that share")
        self.play(*[FadeOut(m) for m in (ab, ah, cb, ch)], run_time=0.4)

        def pair(x, shared, label, color, note):
            rows = VGroup()
            for r in range(2):
                sq = VGroup()
                for k in range(8):
                    on = k < shared
                    sq.add(Square(0.5, stroke_color=TEAL if on else GREY, stroke_width=3,
                                  fill_color=TEAL if on else GREY, fill_opacity=0.55 if on else 0.05))
                sq.arrange(RIGHT, buff=0.08)
                rows.add(sq)
            rows.arrange(DOWN, buff=0.2).move_to([x, 1.25, 0])
            lb = T(label, 40, TEXT, weight=BOLD).move_to([x, 2.7, 0])
            nt = T(note, 30, color).move_to([x, -0.15, 0])
            return rows, lb, nt

        rA, lA, nA = pair(-3.4, 5, "pair A", GREEN, "share more levels")
        rB, lB, nB = pair(3.4, 2, "pair B", GREY, "share fewer levels")
        mu = T("made-up example", 30, YELLOW).move_to([0, 3.3, 0])
        self.play(FadeIn(mu), FadeIn(lA), FadeIn(rA), FadeIn(lB), FadeIn(rB), FadeIn(nA), FadeIn(nB), run_time=0.7)
        gc = T("grouped more closely", 38, GREEN, weight=BOLD).move_to([-3.4, -0.9, 0])
        self.at("grouped more closely")
        self.play(FadeIn(gc, shift=UP * 0.1), Indicate(rA, color=GREEN, scale_factor=1.05), run_time=0.8)
        ev = VGroup(chip("body parts", BLUE, size=34), chip("what organisms do", BLUE, size=34),
                    chip("DNA", BLUE, size=34)).arrange(RIGHT, buff=0.35).move_to([0, -2.2, 0])
        self.at("body parts")
        self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.15) for e in ev], lag_ratio=0.35), run_time=1.6)
        chg = T("names can still change", 32, GREY).move_to([0, -3.3, 0])
        self.at("Names can still change")
        self.play(FadeIn(chg), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        kt = T("dichotomous key", 46, PURPLE, weight=BOLD).move_to([-3.4, 3.0, 0])
        q = chip("step 1: has fins?", PURPLE, size=36).move_to([-3.6, 1.0, 0])
        yes = chip("brook trout", PURPLE, size=36).move_to([3.6, 1.8, 0])
        no = chip("go to step 2", PURPLE, size=36).move_to([3.6, 0.2, 0])
        a1 = arr(q.get_right() + RIGHT * 0.05, yes.get_left() + LEFT * 0.05, PURPLE)
        a2 = arr(q.get_right() + RIGHT * 0.05, no.get_left() + LEFT * 0.05, PURPLE)
        l1 = T("fins", 28, GREY).move_to([0.1, 1.85, 0])
        l2 = T("no fins", 28, GREY).move_to([0.1, 0.15, 0])
        self.at("A dichotomous key")
        self.play(FadeIn(kt), run_time=0.5)
        self.at("traits you can see")
        self.play(FadeIn(q), run_time=0.5)
        self.at("choice step")
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(l1), FadeIn(l2), run_time=0.7)
        self.play(FadeIn(yes), FadeIn(no), run_time=0.5)
        nr = chip("does not show who is related", RED, size=38).move_to([0, -2.0, 0])
        self.at("does not show")
        self.play(FadeIn(nr, shift=UP * 0.1), run_time=0.6)
        key = VGroup(kt, q, yes, no, a1, a2, l1, l2, nr)
        qq = T("Same living thing?", 54, TEXT, weight=BOLD).move_to([0, 2.9, 0])
        self.at("how do scientists know")
        self.play(FadeOut(key), run_time=0.4)
        self.play(FadeIn(qq, shift=DOWN * 0.1), run_time=0.5)
        sn = chip("scientific name, shared in every country", BLUE, size=38).move_to([0, 1.3, 0])
        lv = chip("place in the eight levels", TEAL, size=38).move_to([0, -0.3, 0])
        self.at("scientific name")
        self.play(FadeIn(sn, shift=UP * 0.15), run_time=0.6)
        self.at("its place in the")
        self.play(FadeIn(lv, shift=UP * 0.15), run_time=0.6)
        ans = T("same living thing", 56, GREEN, weight=BOLD).move_to([0, -2.6, 0])
        a3 = arr([0, -1.0, 0], [0, -2.0, 0], GREEN)
        self.play(GrowArrow(a3), FadeIn(ans), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Use its scientific name and its place in the eight levels."
