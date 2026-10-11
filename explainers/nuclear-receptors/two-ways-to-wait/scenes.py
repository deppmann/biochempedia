"""Nuclear receptors, section film: two ways to wait for a hormone  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the hormone receptor (a block with a pocket notch and a small DNA grip)
  YELLOW = the hormone (a dot)
  PURPLE = the chaperones (Hsp90 chips)
  ORANGE = RXR, the partner
  GOLD   = response elements / half-sites on the DNA
  RED    = co-repressors, "off", and whatever is blocked or kept away
  GREEN  = co-activator and "on"
  GREY   = membranes, nucleus outline, DNA, labels

No molecular structures: a receptor is a rounded block with a round notch (the pocket) and a small tab (the
DNA grip). Hormone is a dot, DNA is a line, half-sites are arrows, bases in a gap are small squares.
Not to scale: half-sites, gap squares and the activity bars are marked on screen where they are idealised.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SW = 3


def bchip(text, color=BLUE, size=22, pad=0.18):
    c = chip(text, color, size=size, pad=pad)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def rec(k, color=BLUE, pocket=True):
    """A receptor at scale k, body centred on the origin. Parts: body, grip, pocket."""
    body = RoundedRectangle(corner_radius=0.18 * k, width=0.9 * k, height=1.3 * k, stroke_color=color,
                            stroke_width=SW, fill_color=color, fill_opacity=0.22)
    grip = Rectangle(width=0.5 * k, height=0.22 * k, stroke_color=color, stroke_width=SW,
                     fill_color=color, fill_opacity=0.5).move_to([0, -(0.65 + 0.11) * k, 0])
    parts = [body, grip]
    g = VGroup(*parts)
    g.body, g.grip, g.k = body, grip, k
    if pocket:
        pk = Circle(radius=0.2 * k, stroke_color=color, stroke_width=SW, fill_color=BG, fill_opacity=1)
        pk.move_to([0, 0.65 * k - 0.07 * k, 0])
        g.add(pk)
        g.pocket = pk
    return g


def drop(k):
    return 0.87 * k      # body centre to the bottom of the grip


def hormone(r=0.13):
    return Dot(radius=r, color=YELLOW)


def arrow(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12)


def strike(c, s=0.22, color=RED):
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=7),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=7))


def move_to_body(grp, body, target, k_from, k_to):
    c = body.get_center()
    return grp.animate.scale(k_to / k_from, about_point=c).shift(np.array(target) - c)


def make_gene(w=1.8, h=0.7, color=GREY, label="gene"):
    box = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=SW,
                           fill_color=color, fill_opacity=0.25)
    return VGroup(box, T(label, 22, TEXT).move_to(box))


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Nuclear Receptors: Receptors That Are Transcription Factors"
    TITLE = "A Receptor Waits Off DNA or On It"


# ---------------------------------------------------------------------------------------------
class S01Chaperone(SpokenScene):
    def construct(self):
        hdr = T("Answer 1: wait with a chaperone", 28, TEXT).move_to([0, 3.2, 0])
        cell = RoundedRectangle(corner_radius=0.5, width=11.8, height=5.85, stroke_color=GREY, stroke_width=3
                                ).move_to([0, -0.275, 0])
        nuc = RoundedRectangle(corner_radius=0.4, width=4.6, height=4.9, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.08).move_to([3.2, -0.25, 0])
        l_nuc = T("nucleus", 22, GREY).move_to([3.2, 1.85, 0])
        l_cyt = T("cytoplasm", 22, GREY).move_to([-3.2, -2.85, 0])
        dna = Line([1.3, -2.0, 0], [5.2, -2.0, 0], color=GREY, stroke_width=5)
        res = [Rectangle(width=0.9, height=0.22, stroke_color=GOLD, stroke_width=SW, fill_color=GOLD,
                         fill_opacity=0.6).move_to([x, -2.0, 0]) for x in (2.75, 3.75)]
        l_re = T("response elements", 22, GOLD).move_to([3.25, -2.4, 0])
        l_dna = T("DNA", 22, GREY).move_to([1.7, -1.7, 0])

        R = rec(1.6)
        R.move_to([-3.2, 0, 0])
        q = T("?", 64, GREY).move_to([-3.2, 1.75, 0])
        l_name = T("glucocorticoid and\nandrogen receptors", 22, BLUE, line_spacing=0.8).move_to([-3.2, -1.7, 0])
        cl = bchip("Hsp90", PURPLE).next_to(R.body, LEFT, buff=0.02)
        cr = bchip("Hsp90", PURPLE).next_to(R.body, RIGHT, buff=0.02)

        self.at("What does a receptor")
        self.play(Create(cell), Create(nuc), FadeIn(l_nuc), FadeIn(l_cyt), Create(dna), FadeIn(l_dna),
                  *[FadeIn(r) for r in res], run_time=1.0)
        self.play(FadeIn(R, shift=UP * 0.2), FadeIn(q), run_time=0.7)
        self.at("two answers")
        self.play(FadeOut(q), run_time=0.3)
        self.at("The first is")
        self.play(FadeIn(hdr, shift=DOWN * 0.1), run_time=0.5)
        self.at("wait mostly in the cytoplasm")
        self.play(FadeIn(l_name), Indicate(l_cyt, color=TEXT, scale_factor=1.2), run_time=0.8)
        self.at("held by chaperones")
        self.play(FadeIn(cl, shift=RIGHT * 0.4), FadeIn(cr, shift=LEFT * 0.4), run_time=0.8)
        self.at("A chaperone is a protein")
        self.play(cl.animate(rate_func=there_and_back).scale(1.15), cr.animate(rate_func=there_and_back).scale(1.15),
                  run_time=0.9)
        self.at("keeps the pocket ready")
        self.play(Indicate(R.pocket, color=YELLOW, scale_factor=1.5), run_time=0.9)
        self.at("keeps the receptor off")
        ar = arrow([-0.9, 1.2, 0], [0.7, 1.2, 0], GREY, 5)
        x = strike(ar.get_center())
        l_off = T("off DNA", 24, RED).move_to([-0.1, 1.65, 0])
        self.play(GrowArrow(ar), run_time=0.4)
        self.play(Create(x), FadeIn(l_off), run_time=0.4)
        self.at("When hormone binds")
        h = hormone().move_to([-4.6, 3.05, 0])
        lh = T("hormone", 22, YELLOW).next_to(h, LEFT, buff=0.15)
        self.add(h)
        self.play(FadeIn(lh), run_time=0.2)
        tgt = R.pocket.get_center()
        self.play(h.animate.move_to(tgt), FadeOut(lh), run_time=1.1)
        self.play(FadeOut(ar), FadeOut(x), FadeOut(l_off), FadeOut(l_name), run_time=0.4)
        self.at("is released")
        self.play(cl.animate.shift(LEFT * 0.5).set_opacity(0), cr.animate.shift(RIGHT * 0.5).set_opacity(0),
                  run_time=0.8)
        self.at("moves into the nucleus")
        grp = VGroup(R, h)
        self.play(move_to_body(grp, R.body, [2.75, -0.1, 0], 1.6, 1.1), run_time=1.6)
        self.at("second copy of itself")
        R2 = rec(1.1)
        R2.move_to([3.75, -0.1, 0])
        copy = VGroup(R2)
        self.play(FadeIn(copy, shift=LEFT * 0.5), run_time=0.8)
        self.at("response elements", nth=0)
        dy = -(1.02 + 0.1)
        self.play(grp.animate.shift(DOWN * 0.9), copy.animate.shift(DOWN * 0.9), FadeIn(l_re), run_time=1.0)
        self.play(*[Indicate(r, color=TEXT, scale_factor=1.15) for r in res], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Partner(SpokenScene):
    def construct(self):
        hdr = T("Answer 2: wait on the DNA", 28, TEXT).move_to([0, 3.2, 0])
        nuc = RoundedRectangle(corner_radius=0.4, width=12.0, height=5.9, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.06).move_to([0, -0.2, 0])
        l_nuc = T("nucleus", 22, GREY).move_to([-5.2, 2.45, 0])
        # rows in spoken order: thyroid hormone (4), retinoic acid (5), vitamin D (3), PPAR (1)
        rows = [("thyroid hormone", 4), ("retinoic acid", 5), ("vitamin D", 3), ("PPAR", 1)]
        ys = [1.45, 0.3, -0.85, -2.0]
        unit = 0.4
        x0 = -0.7
        names, rxrs, dnas, arrs, gaps, nums = [], [], [], [], [], []
        for (nm, n), y in zip(rows, ys):
            t = T(nm, 28, BLUE)
            t.move_to([-5.7 + t.width / 2, y, 0])
            names.append(t)
            r = T("+ RXR", 28, ORANGE)
            r.move_to([-2.3 + r.width / 2, y, 0])
            rxrs.append(r)
            d = Line([-1.1, y, 0], [3.8, y, 0], color=GREY, stroke_width=5)
            dnas.append(d)
            a1 = arrow([x0, y + 0.3, 0], [x0 + 1.2, y + 0.3, 0], GOLD, 8)
            xs = x0 + 1.2 + n * unit
            a2 = arrow([xs, y + 0.3, 0], [xs + 1.2, y + 0.3, 0], GOLD, 8)
            arrs.append(VGroup(a1, a2))
            sq = VGroup(*[Square(0.28, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.25
                                 ).move_to([x0 + 1.2 + unit * (i + 0.5), y, 0]) for i in range(n)])
            gaps.append(sq)
            lab = T(f"{n} base" + ("" if n == 1 else "s"), 26, TEXT)
            lab.move_to([4.0 + lab.width / 2, y, 0])
            nums.append(lab)
        note = T("half-sites and bases not to scale", 20, GREY).move_to([0, -2.75, 0])

        self.at("The second answer")
        self.play(FadeIn(hdr, shift=DOWN * 0.1), run_time=0.5)
        self.at("The receptors for")
        self.play(Create(nuc), FadeIn(l_nuc), run_time=0.7)
        self.at("thyroid hormone")
        self.play(FadeIn(names[0], shift=RIGHT * 0.2), run_time=0.4)
        self.at("retinoic acid")
        self.play(FadeIn(names[1], shift=RIGHT * 0.2), run_time=0.4)
        self.at("vitamin D")
        self.play(FadeIn(names[2], shift=RIGHT * 0.2), run_time=0.4)
        self.at("stay in the nucleus")
        self.play(Indicate(l_nuc, color=TEXT, scale_factor=1.3), run_time=0.7)
        self.at("so do the")
        self.play(FadeIn(names[3], shift=RIGHT * 0.2), run_time=0.4)
        self.at("They bind")
        self.play(*[Create(d) for d in dnas], run_time=0.8)
        self.at("paired with a partner")
        self.play(*[FadeIn(r, shift=LEFT * 0.2) for r in rxrs], run_time=0.8)
        self.at("point the same way")
        self.play(*[FadeIn(a, shift=RIGHT * 0.2) for a in arrs], FadeIn(note), run_time=1.0)
        self.at("The gap between them")
        self.play(*[FadeIn(g) for g in gaps], run_time=0.8)
        order = [3, 2, 0, 1]
        for key, idx in zip(["one base for", "three for", "four for", "five for"], order):
            self.at(key)
            self.play(FadeIn(nums[idx], shift=LEFT * 0.2), Indicate(gaps[idx], color=TEXT, scale_factor=1.1),
                      run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Swap(SpokenScene):
    def construct(self):
        yd = -2.1
        dna = Line([-5.8, yd, 0], [5.8, yd, 0], color=GREY, stroke_width=5)
        k = 1.8
        cy = yd + drop(k) + 0.02
        R = rec(k)
        R.move_to([-1.0, cy, 0])
        P = rec(k, ORANGE, pocket=False)
        P.move_to([0.0 + 0.0, cy, 0])
        P.shift(RIGHT * 0.0)
        P.move_to([-1.0 + 0.9 * k + 0.0, cy, 0])
        sites = [Rectangle(width=1.4, height=0.22, stroke_color=GOLD, stroke_width=SW, fill_color=GOLD,
                           fill_opacity=0.6).move_to([x, yd, 0]) for x in (R.body.get_center()[0], P.body.get_center()[0])]
        l_rxr = T("RXR", 24, ORANGE).move_to(P.body)
        l_rec = T("receptor", 22, BLUE).move_to(R.body.get_center() + [0, -0.25, 0])
        gene = make_gene(2.6, 0.8).move_to([4.0, yd + 0.4 + 0.02, 0])
        l_state = T("", 30, RED)
        l_lab = T("thyroid hormone or retinoic acid receptor, with its partner RXR", 22, GREY).move_to([0, -2.95, 0])
        l_no = T("no hormone", 24, GREY).move_to([-4.3, 1.2, 0])
        corep = bchip("co-repressor", RED, 24).move_to([-0.1, cy + 1.5 + 0.35, 0])
        coact = bchip("co-activator", GREEN, 24).move_to(corep.get_center())
        off = T("gene off", 28, RED).move_to([4.0, -0.9, 0])
        on = T("gene on", 28, GREEN).move_to([4.0, -0.9, 0])
        stem = Line(corep.get_bottom(), [-0.1, cy + 0.75, 0], color=RED, stroke_width=4)
        stem2 = Line(coact.get_bottom(), [-0.1, cy + 0.75, 0], color=GREEN, stroke_width=4)

        self.at("Without hormone")
        self.play(Create(dna), *[FadeIn(s) for s in sites], FadeIn(R), FadeIn(P), FadeIn(l_rxr), FadeIn(l_rec),
                  FadeIn(l_lab), FadeIn(l_no), FadeIn(gene), run_time=1.2)
        self.at("receptors hold")
        self.play(FadeIn(corep, shift=DOWN * 0.3), Create(stem), run_time=0.8)
        self.at("keep the gene off")
        self.play(gene[0].animate.set_stroke(RED).set_fill(RED, 0.3), FadeIn(off), run_time=0.7)
        self.at("Hormone releases")
        h = hormone(0.16).move_to([-4.4, 2.2, 0])
        self.play(FadeOut(l_no), run_time=0.2)
        self.add(h)
        self.play(h.animate.move_to(R.pocket.get_center()), run_time=1.0)
        self.play(FadeOut(corep, shift=UP * 0.6), FadeOut(stem), run_time=0.8)
        self.at("brings in its place")
        self.play(FadeIn(coact, shift=DOWN * 0.6), Create(stem2), run_time=0.8)
        self.at("switch the gene on")
        self.play(gene[0].animate.set_stroke(GREEN).set_fill(GREEN, 0.3), FadeOut(off), FadeIn(on), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Rule(SpokenScene):
    def construct(self):
        # ---- part 1: two genes and a bar for how active each is (idealised)
        hdr = T("gene activity (idealised, not to scale)", 24, GREY).move_to([2.9, 2.9, 0])
        yb1, yb2 = 0.35, -2.25
        d1 = Line([-3.0, yb1, 0], [1.9, yb1, 0], color=GREY, stroke_width=5)
        g1 = make_gene(1.5, 0.7).move_to([1.0, yb1 + 0.37, 0])
        l1 = T("no receptor", 28, TEXT).move_to([-4.9 + 0.0, yb1 + 0.5, 0])
        l1.move_to([-5.8 + l1.width / 2, yb1 + 0.5, 0])
        d2 = Line([-3.0, yb2, 0], [1.9, yb2, 0], color=GREY, stroke_width=5)
        g2 = make_gene(1.5, 0.7).move_to([1.0, yb2 + 0.37, 0])
        k = 0.8
        R = rec(k)
        R.move_to([-1.9, yb2 + drop(k) + 0.02, 0])
        P = rec(k, ORANGE, pocket=False)
        P.move_to([-1.9 + 0.9 * k, yb2 + drop(k) + 0.02, 0])
        co = bchip("co-repressor", RED, 22).move_to([-1.55, yb2 + 2.15, 0])
        stem = Line(co.get_bottom(), [-1.55, yb2 + 1.25, 0], color=RED, stroke_width=4)
        l2 = T("empty thyroid\nhormone receptor", 28, TEXT, line_spacing=0.8)
        l2.move_to([-5.8 + l2.width / 2, yb2 + 1.0, 0])
        base = Line([3.4, 2.1, 0], [3.4, -2.5, 0], color=GREY, stroke_width=3)
        bar1 = Rectangle(width=2.6, height=0.55, stroke_color=GREY, stroke_width=SW, fill_color=GREY,
                         fill_opacity=0.5).move_to([3.4 + 1.3, yb1 + 0.37, 0])
        bar2 = Rectangle(width=0.95, height=0.55, stroke_color=RED, stroke_width=SW, fill_color=RED,
                         fill_opacity=0.5).move_to([3.4 + 0.475, yb2 + 0.37, 0])
        # ---- part 2: the two ways to wait
        kk = 1.2
        yd = -1.7
        dl = Line([-5.8, yd, 0], [-0.7, yd, 0], color=GREY, stroke_width=5)
        dr = Line([0.7, yd, 0], [5.8, yd, 0], color=GREY, stroke_width=5)
        RL = rec(kk).move_to([-3.25, 0.7, 0])
        chl = bchip("Hsp90", PURPLE).next_to(RL.body, LEFT, buff=0.02)
        chr_ = bchip("Hsp90", PURPLE).next_to(RL.body, RIGHT, buff=0.02)
        RR = rec(kk).move_to([3.25 - 0.45 * kk, yd + drop(kk) + 0.02, 0])
        PR = rec(kk, ORANGE, pocket=False).move_to([3.25 + 0.45 * kk, yd + drop(kk) + 0.02, 0])
        wl = T("off the DNA", 30, TEXT).move_to([-3.25, -2.6, 0])
        wr = T("on the DNA", 30, TEXT).move_to([3.25, -2.6, 0])

        self.at("An empty receptor")
        self.play(Create(d1), FadeIn(g1), FadeIn(l1), Create(d2), FadeIn(g2), FadeIn(R), FadeIn(P), FadeIn(co),
                  Create(stem), FadeIn(l2), run_time=0.9)
        self.at("of this kind")
        self.play(co.animate(rate_func=there_and_back).scale(1.15), run_time=0.8)
        self.at("A gene carrying")
        self.play(Create(base), FadeIn(hdr), run_time=0.5)
        self.at("quieter than")
        self.play(GrowFromEdge(bar2, LEFT), run_time=0.8)
        self.at("same gene with no receptor")
        self.play(GrowFromEdge(bar1, LEFT), run_time=1.0)
        self.at("So a receptor can wait")
        self.play(*[FadeOut(m) for m in (hdr, d1, g1, l1, d2, g2, R, P, co, stem, l2, base, bar1, bar2)],
                  Create(dl), Create(dr), FadeIn(RL), FadeIn(RR), FadeIn(PR), run_time=0.7)
        self.at("wait off the")
        self.play(FadeIn(chl, shift=RIGHT * 0.3), FadeIn(chr_, shift=LEFT * 0.3), FadeIn(wl, shift=UP * 0.1),
                  run_time=0.6)
        self.at("wait on it")
        self.play(FadeIn(wr, shift=UP * 0.1), Indicate(RR, color=TEXT, scale_factor=1.1),
                  Indicate(PR, color=TEXT, scale_factor=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05End(EndCard):
    LINE = "A receptor can wait off the DNA, or wait on it."
