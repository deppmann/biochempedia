"""Neuromuscular junction: agrin protects what the muscle starts  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = acetylcholine receptors and their clusters
  PURPLE = the motor neuron: axon and nerve terminal
  YELLOW = agrin (the nerve's clustering signal)
  TEAL   = Lrp4 (the agrin receptor on the muscle)
  GREEN  = MuSK, Dok7 and "protect / facilitate" (the shield)
  ORANGE = rapsyn (the scaffold under the receptors)
  RED    = acetylcholine, dispersal, "not there / not needed / lost"
  GREY   = muscle membrane and fibre, basal lamina, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

NERVE, RECEPTOR, AGRIN, LRP4, MUSK, RAPSYN, ACH = PURPLE, BLUE, YELLOW, TEAL, GREEN, ORANGE, RED


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def cdim(c, o=0.45):
    """animations that fade a bchip without filling it (never use set_opacity on a bchip)"""
    return [c[1].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[2].animate.set_opacity(o)]


def undim(c):
    return [c[1].animate.set_stroke(opacity=1).set_fill(opacity=0.16), c[2].animate.set_opacity(1)]


def cluster(x, y, s=1.0, color=RECEPTOR):
    """A receptor cluster: a tight clump of three dots."""
    r = 0.10 * s
    off = 0.17 * s
    pts = [(-off, -off * 0.6), (off, -off * 0.6), (0, off * 0.9)]
    g = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([x + a, y + b, 0])
                 for a, b in pts])
    return g


def grid_points(n, x0, x1, y0, y1, seed=1):
    rng = np.random.RandomState(seed)
    rows = max(1, int(round(np.sqrt(n * (y1 - y0) / (x1 - x0)))))
    cols = int(np.ceil(n / rows))
    cw, ch = (x1 - x0) / cols, (y1 - y0) / rows
    pts = []
    for r in range(rows):
        for c in range(cols):
            pts.append((x0 + (c + 0.5) * cw + rng.uniform(-0.2, 0.2) * cw,
                        y0 + (r + 0.5) * ch + rng.uniform(-0.2, 0.2) * ch))
    idx = rng.permutation(len(pts))[:n]
    return [pts[i] for i in sorted(idx)]


def muscle(w=12.4, top=0.5, h=2.8):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.12).move_to([0, top - h / 2, 0])


def axon(x=0.0, top=3.7, bulb_y=0.95):
    line = Line([x, top, 0], [x, bulb_y + 0.3, 0], color=NERVE, stroke_width=14)
    bulb = Ellipse(width=1.9, height=0.7, stroke_color=NERVE, stroke_width=3, fill_color=NERVE,
                   fill_opacity=0.55).move_to([x, bulb_y, 0])
    return VGroup(line, bulb)


def cross(mob, color=RED, w=7):
    r = 0.55 * max(mob.width, mob.height) / 2 + 0.05
    r = min(r, 0.55)
    c = mob.get_center()
    return VGroup(Line(c + np.array([-r, -r, 0]), c + np.array([r, r, 0]), color=color, stroke_width=w),
                  Line(c + np.array([-r, r, 0]), c + np.array([r, -r, 0]), color=color, stroke_width=w))


def strike(chp, color=RED):
    """a red slash across a whole chip"""
    w, h = chp.width, chp.height
    c = chp.get_center()
    return Line(c + np.array([-w / 2, -h / 2, 0]), c + np.array([w / 2, h / 2, 0]), color=color, stroke_width=7)


def arr(a, b, color=GREY, w=7, tip=0.28):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


class S00Title(TitleCard):
    LESSON = "Building the neuromuscular junction"
    TITLE = "Agrin protects what muscle starts"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """MuSK missing: axon arrives, no junction. Then a healthy junction: receptors under the terminal. Who tells them?"""

    def construct(self):
        mus = muscle()
        mlbl = T("diaphragm", 26, GREY).move_to([-5.0, -2.75, 0])
        self.at("newborn mouse")
        self.play(FadeIn(mus), FadeIn(mlbl), run_time=0.8)
        musk = bchip("MuSK", MUSK, 30).move_to([-4.6, 2.4, 0])
        self.at("lacks the muscle kinase")
        self.play(FadeIn(musk, shift=DOWN * 0.2), run_time=0.5)
        bar = strike(musk)
        self.at("cannot breathe")
        self.play(Create(bar), *cdim(musk), run_time=0.5)
        ax = axon(0.0)
        axl = T("motor axon", 26, NERVE).move_to([2.0, 2.7, 0])
        self.at("motor axons")
        self.play(Create(ax[0]), run_time=1.0)
        self.play(FadeIn(ax[1], scale=0.8), FadeIn(axl), run_time=0.5)
        nj = T("no junction", 32, RED, weight=BOLD).move_to([3.0, 0.95, 0])
        self.at("but no")
        self.play(FadeIn(nj, shift=LEFT * 0.2), run_time=0.5)
        # healthy junction
        packed = VGroup(*[cluster(x, y, 1.0) for x, y in
                          [(-0.55, 0.2), (0.0, 0.2), (0.55, 0.2), (-0.55, -0.25), (0.0, -0.25), (0.55, -0.25)]])
        sparse = VGroup(*[cluster(x, y, 1.1) for x, y in [(-4.6, -0.6), (-2.5, -1.7), (3.4, -1.1), (4.9, -0.2), (-3.4, 0.0)]])
        rlbl = T("acetylcholine receptors", 26, RECEPTOR).move_to([3.2, -2.75, 0])
        self.at("healthy junction")
        self.play(FadeOut(nj), FadeOut(musk), FadeOut(bar), run_time=0.5)
        self.at("packs its")
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in packed], lag_ratio=0.12), run_time=1.0)
        self.play(FadeIn(sparse), FadeIn(rlbl), run_time=0.7)
        self.at("Where do the receptors go")
        self.play(Indicate(packed, color=RECEPTOR, scale_factor=1.2), run_time=0.9)
        q = T("?", 110, YELLOW, weight=BOLD).move_to([-2.8, 1.8, 0])
        self.at("who tells them")
        self.play(FadeIn(q, scale=1.4), run_time=0.5)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Prepattern(SpokenScene):
    """No nerve: a central band of clusters forms. Needs MuSK, not agrin. The nerve arrives and the band narrows."""

    def construct(self):
        mus = muscle()
        mlbl = T("diaphragm", 26, GREY).move_to([-5.0, -2.75, 0])
        self.add(mus, mlbl)
        nm = T("no motor neurons", 30, NERVE).move_to([0, 2.9, 0])
        ncross = cross(nm)  # placed to the left of text
        ncross.next_to(nm, LEFT, buff=0.3).scale(0.5)
        self.at("job alone")
        self.play(FadeIn(nm), Create(ncross), run_time=0.7)
        pts = grid_points(12, -2.3, 2.3, -1.95, 0.15, seed=4)
        band = VGroup(*[cluster(x, y, 1.15) for x, y in pts])
        blbl = T("band of receptor clusters", 28, RECEPTOR).move_to([0, 1.7, 0])
        self.at("builds a band")
        self.play(FadeIn(blbl), LaggedStart(*[FadeIn(c, scale=0.4) for c in band], lag_ratio=0.06), run_time=2.0)
        frame = RoundedRectangle(corner_radius=0.15, width=5.4, height=2.5, stroke_color=RECEPTOR, stroke_width=3,
                                 fill_opacity=0).move_to([0, -0.9, 0])
        pre = T("prepattern", 34, RECEPTOR, weight=BOLD).move_to([0, 1.7, 0])
        self.at("laid down")
        self.play(Create(frame), ReplacementTransform(blbl, pre), run_time=0.9)
        mk = bchip("MuSK", MUSK, 30).move_to([-4.5, 2.0, 0])
        ag = bchip("agrin", AGRIN, 30).move_to([4.5, 2.0, 0])
        self.at("needs MuSK")
        self.play(FadeIn(mk, shift=RIGHT * 0.2), run_time=0.5)
        self.at("does not need agrin")
        self.play(FadeIn(ag, shift=LEFT * 0.2), run_time=0.5)
        sag = strike(ag)
        self.play(Create(sag), run_time=0.4)
        # the nerve arrives
        ax = axon(0.0)
        axl = T("motor axon", 26, NERVE).move_to([2.0, 2.9, 0])
        self.at("nerve does arrive")
        self.play(FadeOut(nm), FadeOut(ncross), FadeOut(mk), FadeOut(ag), FadeOut(pre), FadeOut(frame), FadeOut(sag), run_time=0.4)
        self.play(Create(ax[0]), run_time=0.5)
        self.play(FadeIn(ax[1], scale=0.8), FadeIn(axl), run_time=0.3)
        self.at("band narrows")
        self.play(*[c.animate.shift(RIGHT * (-c.get_center()[0] * 0.4)) for c in band], run_time=1.4)
        keep = VGroup(*[c for c in band if c.get_center()[1] > -0.45])
        gone = VGroup(*[c for c in band if c.get_center()[1] <= -0.45])
        bl = T("beneath the terminal", 26, RECEPTOR).move_to([0, -2.75, 0])
        self.at("beneath the terminal")
        self.play(FadeOut(gone), FadeIn(bl), run_time=0.9)
        self.play(Indicate(keep, color=RECEPTOR, scale_factor=1.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Relay(SpokenScene):
    """cross-section: agrin -> Lrp4 -> MuSK (+Dok7) -> rapsyn gathers receptors"""

    def construct(self):
        DY = -0.8

        def P(x, y):
            return [x, y + DY, 0]

        term = RoundedRectangle(corner_radius=0.3, width=7.0, height=1.1, stroke_color=NERVE, stroke_width=3,
                                fill_color=NERVE, fill_opacity=0.35).move_to(P(-2.4, 3.4))
        tl = T("nerve terminal", 28, NERVE).move_to(term)
        mem = RoundedRectangle(corner_radius=0.1, width=12.4, height=0.34, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.4).move_to(P(0, 0))
        mlab = T("muscle membrane", 24, GREY).move_to(P(-4.8, -0.65))
        self.at("adds its own signal")
        self.play(FadeIn(term), FadeIn(tl), FadeIn(mem), FadeIn(mlab), run_time=0.8)
        ag = Circle(radius=0.27, stroke_color=AGRIN, stroke_width=3, fill_color=AGRIN, fill_opacity=0.95).move_to(P(-4.2, 2.45))
        agl = T("agrin", 28, AGRIN).next_to(ag, LEFT, buff=0.2)
        self.at("protein called agrin")
        self.play(FadeIn(ag, scale=0.4), FadeIn(agl), run_time=0.5)
        lam = DashedLine(P(-6.3, 2.0), P(6.3, 2.0), color=GREY, stroke_width=3, dash_length=0.18)
        laml = T("basal lamina", 24, GREY).move_to(P(4.9, 2.4))
        self.at("basal lamina")
        self.play(Create(lam), FadeIn(laml), ag.animate.move_to(P(-4.2, 2.0)), agl.animate.move_to(P(-4.2, 2.55)), run_time=0.9)
        # muscle surface proteins
        lrp = RoundedRectangle(corner_radius=0.12, width=0.5, height=1.7, stroke_color=LRP4, stroke_width=3,
                               fill_color=LRP4, fill_opacity=0.45).move_to(P(-4.2, 0.95))
        lrpl = T("Lrp4", 28, LRP4).move_to(P(-5.0, 1.0))
        musk = RoundedRectangle(corner_radius=0.12, width=0.5, height=1.5, stroke_color=MUSK, stroke_width=3,
                                fill_color=MUSK, fill_opacity=0.25).move_to(P(-1.5, 0.0))
        muskl = T("MuSK", 28, MUSK).move_to(P(-0.8, 1.25))
        rx = [1.2, 3.0, 4.8]
        recs = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.5, height=0.9, stroke_color=RECEPTOR, stroke_width=3,
                                         fill_color=RECEPTOR, fill_opacity=0.5).move_to(P(x, 0)) for x in rx])
        recl = T("receptors", 26, RECEPTOR).move_to(P(3.0, 0.95))
        self.at("thin layer")
        self.play(FadeIn(lrp), FadeIn(lrpl), FadeIn(musk), FadeIn(muskl), FadeIn(recs), FadeIn(recl), run_time=0.9)
        self.at("Agrin binds")
        self.play(Indicate(ag, color=AGRIN, scale_factor=1.4), run_time=0.7)
        # Lrp4 (carrying agrin) joins MuSK
        self.at("forms a complex")
        self.play(lrp.animate.move_to(P(-2.15, 0.95)), lrpl.animate.move_to(P(-3.0, 1.0)),
                  ag.animate.move_to(P(-2.15, 2.0)), agl.animate.move_to(P(-2.15, 2.55)), run_time=1.0)
        dok = bchip("Dok7", MUSK, 26).move_to(P(-1.5, -1.45))
        self.at("inside the muscle")
        self.play(FadeIn(dok, shift=UP * 0.2), run_time=0.5)
        self.at("boosts")
        self.play(musk.animate.set_fill(MUSK, 0.85), Indicate(musk, color=MUSK, scale_factor=1.2), run_time=0.8)
        # rapsyn gathers receptors
        rap = RoundedRectangle(corner_radius=0.1, width=3.2, height=0.3, stroke_color=RAPSYN, stroke_width=3,
                               fill_color=RAPSYN, fill_opacity=0.6).move_to(P(3.7, -0.75))
        rapl = T("rapsyn", 28, RAPSYN).move_to(P(3.7, -1.4))
        sig = arr(P(-0.9, -0.85), P(2.0, -0.78), MUSK)
        self.at("Downstream")
        self.play(GrowArrow(sig), run_time=0.5)
        self.play(FadeIn(rap, shift=UP * 0.2), FadeIn(rapl), run_time=0.5)
        self.at("holds the receptors")
        new_x = [2.6, 3.7, 4.8]
        self.play(*[r.animate.move_to(P(x, 0)) for r, x in zip(recs, new_x)], recl.animate.move_to(P(3.7, 0.95)),
                  run_time=1.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
def _ach_dots(x, y, n=5, seed=2):
    rng = np.random.RandomState(seed)
    return VGroup(*[Circle(radius=0.09, stroke_width=0, fill_color=ACH, fill_opacity=0.95)
                    .move_to([x + rng.uniform(-0.6, 0.6), y + rng.uniform(-0.1, 0.1), 0]) for _ in range(n)])


class S04Second(SpokenScene):
    """agrin not needed for clusters, yet agrin-null mice lose most; ACh disperses unprotected clusters."""

    def construct(self):
        mus = muscle()
        self.add(mus)
        pts = grid_points(10, -5.4, 5.4, -2.0, 0.2, seed=7)
        cl = [cluster(x, y, 1.15) for x, y in pts]
        self.at("Here is the puzzle")
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in cl], lag_ratio=0.08), run_time=1.2)
        ag = bchip("agrin", AGRIN, 30).move_to([4.6, 2.5, 0])
        self.at("no agrin at all")
        self.play(FadeIn(ag), run_time=0.4)
        sl = strike(ag)
        self.play(Create(sl), run_time=0.4)
        lost = T("most clusters lost", 30, RED).move_to([0, 1.7, 0])
        order = list(range(10))
        keepi = [order[2], order[7]]
        fade = [cl[i] for i in order if i not in keepi]
        self.at("lose most")
        self.play(FadeIn(lost), *[FadeOut(c) for c in fade], run_time=1.2)
        # reset for the next case
        left = [cl[i] for i in keepi]
        ax = axon(0.0)
        axl = T("motor axon", 26, NERVE).move_to([2.0, 2.9, 0])
        A = cluster(-3.2, -0.7, 2.0)
        B = cluster(3.2, -0.7, 2.0)
        self.at("second signal")
        self.play(FadeOut(ag), FadeOut(sl), FadeOut(lost), *[FadeOut(c) for c in left], Create(ax[0]), run_time=0.5)
        self.play(FadeIn(ax[1], scale=0.8), FadeIn(axl), FadeIn(A, scale=0.6), FadeIn(B, scale=0.6), run_time=0.5)
        shield = Arc(radius=1.2, start_angle=0.0, angle=PI, color=MUSK, stroke_width=9).move_to([3.2, -0.65, 0])
        agb = T("agrin", 28, AGRIN).move_to([3.2, 0.85, 0])
        ua = T("unprotected", 26, GREY).move_to([-3.2, -1.95, 0])
        pb = T("protected", 26, MUSK).move_to([3.2, -1.95, 0])
        ach_l = T("acetylcholine", 28, ACH).move_to([-2.4, 2.1, 0])
        self.at("Acetylcholine")
        dots = _ach_dots(0.0, 0.5, 6)
        self.play(FadeIn(dots), FadeIn(ach_l), run_time=0.5)
        self.play(Create(shield), FadeIn(agb), FadeIn(ua), FadeIn(pb), run_time=0.7)
        self.at("disperses")
        d_left = VGroup(*dots[:3])
        d_right = VGroup(*dots[3:])
        # stream toward each cluster
        self.play(*[d.animate.move_to([-3.2 + (i - 1) * 0.3, 0.2, 0]) for i, d in enumerate(d_left)],
                  *[d.animate.move_to([3.2 + (i - 1) * 0.5, 0.9, 0]) for i, d in enumerate(d_right)], run_time=0.9)
        rng = np.random.RandomState(5)
        scat = [d.animate.shift([rng.uniform(-1.6, 1.6), rng.uniform(-0.9, 0.9), 0]).set_opacity(0.35) for d in A]
        self.play(*scat, FadeOut(d_right), FadeOut(d_left), run_time=1.3)
        self.play(Indicate(B, color=RECEPTOR, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Mutants(SpokenScene):
    """four cases on one strip: normal, no agrin, no ACh, both removed."""

    def construct(self):
        mus = muscle()
        ax = axon(0.0)
        self.add(mus, ax)

        def sw():
            a = bchip("agrin", AGRIN, 28).move_to([4.7, 3.2, 0])
            b = bchip("acetylcholine", ACH, 28).move_to([4.7, 2.3, 0])
            return a, b
        a, b = sw()
        sa, sb = strike(a), strike(b)
        lab = T("Normal", 38, TEXT, font=TITLE_FONT).move_to([-3.6, 3.1, 0])
        cap_pos = [0, -3.05, 0]
        # ACh puffs under the terminal when acetylcholine is present
        puff = _ach_dots(0.0, 0.3, 4, seed=9)
        normal = VGroup(*[cluster(x, y, 1.0) for x, y in [(-0.8, -0.1), (0.0, -0.1), (0.8, -0.1), (-0.4, -0.65), (0.4, -0.65)]]).shift(RIGHT * 0.0)
        note = T("illustrative counts", 22, GREY).move_to([-4.8, -3.05, 0])
        self.at("Test it with mutant")
        self.play(FadeIn(lab), FadeIn(a), FadeIn(b), FadeIn(normal), FadeIn(puff), FadeIn(note), run_time=0.9)
        # case 2: no agrin
        lab2 = T("No agrin", 38, TEXT, font=TITLE_FONT).move_to([-3.6, 3.1, 0])
        two = VGroup(*[cluster(x, y, 1.0) for x, y in [(-0.6, -0.1), (0.5, -0.55), (1.5, -0.1)]]).set_opacity(0.4)
        cap2 = T("most clusters lost", 30, RED).move_to(cap_pos)
        self.at("Remove agrin")
        self.play(ReplacementTransform(lab, lab2), Create(sa), *cdim(a), FadeOut(normal), FadeIn(two), run_time=0.8)
        self.at("most are lost")
        self.play(FadeIn(cap2), run_time=0.7)
        # case 3: no ACh
        lab3 = T("No acetylcholine", 38, TEXT, font=TITLE_FONT).move_to([-3.6, 3.1, 0])
        wide = VGroup(*[cluster(x, y, 1.0) for x, y in grid_points(16, -4.6, 4.6, -2.0, 0.2, seed=11)])
        cap3 = T("more clusters, wider band", 30, GREEN).move_to(cap_pos)
        self.at("Remove the enzyme")
        self.play(ReplacementTransform(lab2, lab3), FadeOut(sa), *undim(a), Create(sb),
                  *cdim(b), FadeOut(puff), FadeOut(two), FadeOut(cap2),
                  LaggedStart(*[FadeIn(c, scale=0.4) for c in wide], lag_ratio=0.04), run_time=1.3)
        self.at("wider band")
        self.play(FadeIn(cap3), run_time=0.6)
        # case 4: both
        lab4 = T("Double knockout", 38, TEXT, font=TITLE_FONT).move_to([-3.6, 3.1, 0])
        back = VGroup(*[cluster(x, y, 1.0) for x, y in grid_points(16, -4.6, 4.6, -2.0, 0.2, seed=11)])
        cap4 = T("clusters return", 30, GREEN).move_to(cap_pos)
        sa2 = strike(a)
        mp = bchip("muscle's MuSK program", MUSK, 26).move_to([-3.2, 2.3, 0])
        self.at("Now remove both")
        self.play(ReplacementTransform(lab3, lab4), Create(sa2), *cdim(a),
                  FadeOut(wide), FadeOut(cap3), run_time=0.9)
        self.at("Clusters return")
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in back], lag_ratio=0.08), FadeIn(cap4), run_time=1.4)
        self.at("MuSK program")
        self.play(FadeIn(mp, shift=DOWN * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """double mutant is telling; agrin protects; two forces."""

    def construct(self):
        floor = RoundedRectangle(corner_radius=0.1, width=12.4, height=0.34, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.4).move_to([0, -2.3, 0])
        self.add(floor)
        lab = T("Double knockout", 38, TEXT, font=TITLE_FONT).move_to([0, 3.2, 0])
        cl = cluster(0, -1.55, 3.0)
        ag = bchip("agrin", AGRIN, 30).move_to([-5.0, -0.3, 0])
        ach = bchip("acetylcholine", ACH, 28).move_to([4.9, -0.3, 0])
        sa, sb = strike(ag), strike(ach)
        self.at("double mutant")
        self.play(*cdim(ag, 0.5), *cdim(ach, 0.5), run_time=0.01)
        self.play(FadeIn(lab), FadeIn(cl, scale=0.5), FadeIn(ag), FadeIn(ach), FadeIn(sa), FadeIn(sb), run_time=0.8)
        # hypothesis: agrin starts clusters
        ghost = cluster(0, -1.1, 3.0, color=GREY).set_opacity(0.0)
        hyp = arr([-3.6, -0.4, 0], [-1.7, -0.9, 0], AGRIN)
        hl = T("start?", 30, AGRIN).move_to([-2.5, 0.35, 0])
        self.at("start clusters")
        self.play(FadeOut(lab), FadeOut(sa), *undim(ag), GrowArrow(hyp), FadeIn(hl), run_time=0.7)
        hx = cross(VGroup(hyp), RED).move_to(hyp.get_center())
        self.at("bring them back")
        self.play(Create(hx), hyp.animate.set_opacity(0.4), hl.animate.set_opacity(0.4), run_time=0.6)
        # reality: protect
        shield = Arc(radius=1.9, start_angle=0.0, angle=PI, color=MUSK, stroke_width=10).move_to([0, -1.15, 0])
        pl = T("protect", 32, MUSK, weight=BOLD).move_to([0, 0.2, 0])
        ach_arrows = VGroup(*[arr([3.4, y, 0], [xe, y, 0], ACH, w=6) for y, xe in [(-0.75, 1.5), (-1.2, 1.85), (-1.7, 2.0)]])
        self.at("protect clusters")
        self.play(FadeOut(hyp), FadeOut(hl), FadeOut(hx), run_time=0.4)
        self.play(Create(shield), FadeIn(pl), run_time=0.8)
        self.at("dispersal")
        self.play(FadeOut(sb), *undim(ach), run_time=0.3)
        self.play(FadeIn(ach_arrows, shift=LEFT * 0.3), run_time=0.6)
        # two forces
        fac = T("facilitate", 34, MUSK, weight=BOLD).move_to([-4.9, 0.7, 0])
        inh = T("inhibit", 34, ACH, weight=BOLD).move_to([4.9, 0.7, 0])
        self.at("Agrin and MuSK facilitate")
        self.play(FadeIn(fac), Indicate(shield, color=MUSK, scale_factor=1.08), run_time=0.7)
        self.at("inhibits")
        self.play(FadeIn(inh), Indicate(ach_arrows, color=ACH, scale_factor=1.1), run_time=0.7)
        self.at("muscle starts clusters")
        self.play(Indicate(cl, color=RECEPTOR, scale_factor=1.2), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "The muscle starts clusters; agrin protects them from acetylcholine."
