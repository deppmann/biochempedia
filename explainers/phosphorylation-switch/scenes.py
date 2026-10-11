"""Phosphorylation: a charge you can add and remove  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the target protein (its copies, its side chains)
  PURPLE = the kinase, the writer of the phosphate
  RED    = the phosphatase, the eraser (and an inhibited protein, a blocked route)
  GOLD   = a phosphate (the round "P" badge) and the share of protein that carries one (the gauge)
  ORANGE = an electric charge (the minus and plus marks)
  PINK   = ATP and ADP
  GREEN  = working / activated (an active protein, a signal that activates)
  YELLOW = an outside signal
  GREY   = structure, labels, water, parts not yet doing anything

No molecular structures: a protein is a round blob with a mouth that opens and shuts (two
arrangements), a kinase and a phosphatase are labelled chips, a phosphate is a "P" badge, a charge is
a small circle with a minus or plus, and ATP is a chip.

Pictures carried from scene to scene (rebuilt in the same place at the start of the next scene):
  scenes 2 -> 3  the protein with its phosphate and two charges (right of centre, then grown to fill the frame)
  scenes 5 -> 6  the tank of twelve copies, the kinase above (the tap) and the phosphatase below (the drain)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F08BB4"

SHUT, GAPE = 0.30, 1.35        # the mouth of a protein copy, in radians: two arrangements
SITE = 140                      # where on the rim a phosphate lands, in degrees


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.24, b - perp * 0.24, color=color, stroke_width=w + 1))


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


def pbadge(k=1.0):
    """a phosphate."""
    c = Circle(radius=0.18 * k, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22 * k, BG, weight=BOLD).move_to(c))


def cmark(sign="-", k=1.0):
    """one electric charge: a small circle with a minus or a plus."""
    r = 0.13 * k
    parts = [Circle(radius=r, stroke_color=ORANGE, stroke_width=3, fill_color=BG, fill_opacity=1),
             Line(LEFT * 0.075 * k, RIGHT * 0.075 * k, color=ORANGE, stroke_width=3.5)]
    if sign == "+":
        parts.append(Line(DOWN * 0.075 * k, UP * 0.075 * k, color=ORANGE, stroke_width=3.5))
    return VGroup(*parts)


def pop(m, s=1.35):
    """swell and settle, without recolouring (Indicate would hide the P on a badge)."""
    return m.animate(rate_func=there_and_back).scale(s)


def glow(*mobs, s=1.1, color=TEXT):
    """flash each mobject in place, one animation each."""
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def body(c, r, open_=False, color=BLUE, sw=4.0, fo=0.30):
    """a protein copy: a round blob with a mouth. Shut and open are two arrangements of the same protein."""
    m = GAPE if open_ else SHUT
    return Sector(radius=r, start_angle=m / 2, angle=TAU - m, arc_center=np.array(c, float),
                  stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=fo)


def rim(c, r, deg=SITE):
    a = np.radians(deg)
    return np.array(c, float) + r * np.array([np.cos(a), np.sin(a), 0])


def recolor(b, color, fo=0.30):
    return b.animate.set_stroke(color).set_fill(color, fo)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Phosphorylation: Kinases and Phosphatases"
    TITLE = "A charge you can add and remove"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """about 518 kinases, one reaction; why a phosphate?"""

    def construct(self):
        GX, GY = -3.5, -0.35
        # the count of kinase genes
        about = T("about", 30, GREY).move_to([-4.6, 2.95, 0])

        def numtxt(n):
            return M(str(n), 66, PURPLE, weight=BOLD).move_to([-3.85, 3.0, 0], aligned_edge=LEFT)
        num = numtxt(0)
        sub = T("genes for protein kinases", 28, PURPLE).move_to([GX, 2.28, 0])

        def count(m, a):
            m.become(numtxt(int(round(518 * a))))

        pills, dots = VGroup(), VGroup()
        for r_ in range(6):
            for c_ in range(7):
                pos = [GX + (c_ - 3) * 0.82, GY + (2.5 - r_) * 0.7, 0]
                pills.add(RoundedRectangle(corner_radius=0.11, width=0.66, height=0.38, stroke_color=PURPLE, stroke_width=2.5,
                                           fill_color=PURPLE, fill_opacity=0.3).move_to(pos))
                dots.add(Circle(radius=0.08, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to([pos[0] + 0.2, pos[1], 0]))

        # the one reaction they all run
        PC1 = np.array([4.1, 1.45, 0])
        prot = body(PC1, 1.2, color=BLUE)
        prot_lbl = T("protein", 28, BLUE).move_to([4.1, 3.05, 0])
        atp = bchip("ATP", PINK, 34, pad=0.28).move_to([4.1, -1.75, 0])
        ph = pbadge(1.5).move_to(atp.get_corner(UR) + [-0.05, 0.1, 0])
        site = rim(PC1, 1.2, 270)
        flow = arr([-0.2, -0.35, 0], [2.65, -0.35, 0], GREY, w=6)
        same = T("the same reaction", 26, GREY).move_to([1.2, 0.2, 0])

        self.add(about, num)
        self.play(UpdateFromAlphaFunc(num, count), run_time=1.9, rate_func=linear)
        self.at("genes for")
        self.play(FadeIn(sub), LaggedStart(*[FadeIn(p, scale=0.6) for p in pills], lag_ratio=0.03), run_time=1.3)
        self.at("same reaction")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.02), run_time=0.8)
        self.play(GrowArrow(flow), FadeIn(same), FadeIn(prot), FadeIn(prot_lbl), FadeIn(atp), FadeIn(ph, scale=0.5), run_time=0.8)
        self.at("takes a")
        self.play(pop(ph, 1.4), run_time=0.5)
        self.at("fastens it")
        self.play(ph.animate.move_to(site + [0, 0.02, 0]), run_time=1.0)
        self.play(atp[1].animate.set_stroke(opacity=0.5).set_fill(opacity=0.08), atp[2].animate.set_opacity(0.5), run_time=0.3)
        q = T("?", 72, TEXT, weight=BOLD).move_to([5.75, 0.55, 0])
        self.at("Why would")
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.at("small chemical")
        self.play(pop(ph, 1.8), pop(q, 1.2), run_time=0.8)
        good = T("a good switch?", 44, TEXT, font=TITLE_FONT).move_to([0.6, -3.15, 0])
        self.at("a good switch")
        self.play(FadeIn(good, shift=UP * 0.15), pop(ph, 1.6), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# scene 2 geometry (also the start of scene 3)
PC, PR = np.array([3.5, 0.2, 0]), 1.75                 # the protein: centre and radius
MC = np.array([0.0, 0.2, 0])                            # where it sits at the end of scene 2 and in scene 3
BK = 1.9                                                # size of the phosphate and the charges beside it


def site_marks(c, r=PR, k=BK):
    """where the phosphate lands on a protein at c, and where its two charges sit."""
    site = rim(c, r, SITE)
    u = np.array([np.cos(np.radians(SITE)), np.sin(np.radians(SITE)), 0])
    p = np.array([-u[1], u[0], 0])
    return site, site + u * 0.4 * k + p * 0.2 * k, site + u * 0.4 * k - p * 0.2 * k


class S02Write(SpokenScene):
    """ATP is plentiful; the kinase moves the end phosphate onto a hydroxyl on the protein; it brings two charges."""

    def construct(self):
        PSITE, CH1, CH2 = site_marks(PC)
        kin = bchip("kinase", PURPLE, 40, pad=0.4).move_to([-1.0, 0.45, 0])
        spots = [(-5.7, 2.5), (-4.2, 3.0), (-5.5, 1.3), (-5.5, -0.6), (-4.0, -1.0), (-5.7, -2.1), (-4.2, -2.5), (-2.6, -2.2), (-2.8, 2.8)]
        swarm = VGroup(*[bchip("ATP", PINK, 28, pad=0.18).move_to([x, y, 0]) for x, y in spots])
        main = bchip("ATP", PINK, 30, pad=0.2).move_to([-4.6, 0.45, 0])
        mol = T("millimolar", 28, GREY).move_to([-1.0, -2.4, 0])
        prot = body(PC, PR, color=BLUE)
        self.add(kin, prot)
        self.play(FadeIn(swarm, lag_ratio=0.1), FadeIn(main), run_time=0.9)
        self.at("millimolar")
        self.play(FadeIn(mol, shift=UP * 0.1), LaggedStart(*[pop(c, 1.12) for c in swarm], lag_ratio=0.08), run_time=1.0)
        self.at("never waits")
        self.play(main.animate.move_to([kin[1].get_left()[0] - main.width / 2 - 0.02, 0.45, 0]), FadeOut(mol), run_time=0.8)
        self.play(pop(kin, 1.06), run_time=0.4)

        ph = pbadge(BK).move_to(main.get_corner(UR) + [0.05, 0.22, 0]).set_z_index(3)
        self.at("end phosphate")
        self.play(FadeIn(ph, scale=0.4), run_time=0.4)
        self.at("off")
        hover = np.array([-1.0, 2.0, 0])
        self.play(ph.animate.move_to(hover), run_time=0.7)
        adp = bchip("ADP", PINK, 30, pad=0.2).move_to(main)
        self.at("leaving")
        self.play(ReplacementTransform(main, adp), run_time=0.5)
        self.play(adp.animate.shift(DOWN * 0.9 + LEFT * 0.4).set_opacity(0.0), run_time=0.9)
        self.remove(adp)

        # the protein and its hydroxyl site
        site = Circle(radius=0.13, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.9).move_to(PSITE).set_z_index(2)
        self.at("In animals")
        self.play(FadeIn(site, scale=0.4), Indicate(prot, color=BLUE, scale_factor=1.04), run_time=0.7)
        self.at("fastens that")
        self.play(ph.animate.move_to(PSITE), run_time=0.9)
        self.remove(site)
        lbl = T("side chain", 30, GREY).move_to([2.7, 3.05, 0])
        ptr = Line([2.5, 2.77, 0], PSITE + [0.05, 0.3, 0], color=GREY, stroke_width=3)
        self.at("side chain")
        self.play(FadeIn(lbl, shift=DOWN * 0.1), Create(ptr), run_time=0.5)
        lbl2 = T("hydroxyl group", 30, GREY).move_to([2.7, 3.05, 0])
        self.at("hydroxyl")
        self.play(ReplacementTransform(lbl, lbl2), pop(ph, 1.2), run_time=0.6)

        # the three residues that carry it
        names = VGroup(*[bchip(n, BLUE, 28, pad=0.18) for n in ("serine", "threonine", "tyrosine")]).arrange(RIGHT, buff=0.25)
        names.move_to([PC[0], -2.85, 0])
        self.at("That means")
        self.play(FadeOut(lbl2), FadeOut(ptr), LaggedStart(*[FadeIn(n, shift=UP * 0.12) for n in names], lag_ratio=0.4), run_time=1.9)

        # the charge: the protein comes to the middle of the frame
        self.at("Near")
        mv = MC - PC
        self.play(FadeOut(kin), FadeOut(swarm), prot.animate.shift(mv), ph.animate.shift(mv), names.animate.shift(mv), run_time=0.9)
        PSITE, CH1, CH2 = site_marks(MC)
        m1, m2 = cmark("-", 1.5).move_to(CH1).set_z_index(4), cmark("-", 1.5).move_to(CH2).set_z_index(4)
        two = T("two negative charges", 30, ORANGE).move_to([-4.2, 2.95, 0])
        none = T("on a spot that had none", 28, GREY).next_to(two, DOWN, buff=0.18, aligned_edge=RIGHT)
        self.at("two negative")
        self.play(FadeIn(m1, scale=0.4), FadeIn(m2, scale=0.4), FadeIn(two, shift=DOWN * 0.1), run_time=0.7)
        self.at("on a spot")
        self.play(FadeIn(none, shift=DOWN * 0.1), pop(ph, 1.3), run_time=0.7)

        # hand over to scene 3: the labels and the residues go, the protein and its phosphate stay
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        self.play(FadeOut(two), FadeOut(none), FadeOut(names), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
POOL_R = 1.0
POOL = [np.array([x, y, 0]) for y in (1.1, -1.4) for x in (-4.2, -1.4, 1.4, 4.2)]


class S03Shape(SpokenScene):
    """the charge holds a protein in shape; a phosphate shifts which arrangement its copies sit in."""

    def construct(self):
        # the protein from scene 2, where scene 2 left it
        BC, BR = MC, PR
        PSITE, CH1, CH2 = site_marks(BC)
        prot = body(BC, BR, color=BLUE)
        ph = pbadge(BK).move_to(PSITE).set_z_index(3)
        m1, m2 = cmark("-", 1.5).move_to(CH1).set_z_index(4), cmark("-", 1.5).move_to(CH2).set_z_index(4)
        self.add(prot, ph, m1, m2)
        self.at("That charge")
        self.play(*[Indicate(x, color=ORANGE, scale_factor=1.3) for x in (m1, m2)], run_time=0.8)

        # charges inside hold it in shape
        marks, lines = VGroup(), VGroup()
        spec = [("+", 100, 1.05), ("-", 150, 1.05), ("+", 215, 1.05), ("-", 265, 1.05), ("+", 325, 1.05), ("-", 30, 1.05)]
        for s, a, rr in spec:
            marks.add(cmark(s, 1.3).move_to(rim(BC, rr, a)).set_z_index(2))
        for i in (0, 2, 4):
            lines.add(DashedLine(marks[i].get_center(), marks[i + 1].get_center(), color=GREY, stroke_width=3, dash_length=0.1))
        lines.set_z_index(-1)
        rep_a, rep_b = cmark("+", 1.3).move_to([-0.3, -0.15, 0]), cmark("+", 1.3).move_to([0.3, -0.15, 0])
        push = VGroup(arr([-0.45, -0.15, 0], [-1.0, -0.15, 0], GREY, w=4, tip=0.16), arr([0.45, -0.15, 0], [1.0, -0.15, 0], GREY, w=4, tip=0.16))
        self.at("held in shape")
        self.play(LaggedStart(*[FadeIn(m, scale=0.4) for m in (*marks, rep_a, rep_b)], lag_ratio=0.1), run_time=1.1)
        self.at("attract")
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.25), run_time=0.9)
        self.at("repel")
        self.play(*[GrowArrow(a) for a in push], LaggedStart(*[Indicate(m, color=ORANGE, scale_factor=1.35) for m in marks], lag_ratio=0.1), run_time=1.0)

        # a small change, a big disturbance
        shift = [np.array(v) for v in ([0.15, 0.2, 0], [-0.25, 0.1, 0], [-0.2, -0.15, 0], [0.1, -0.25, 0], [0.25, -0.1, 0], [0.2, 0.2, 0])]
        self.at("disturb")
        self.play(Transform(prot, body(BC, BR, open_=True, color=BLUE)),
                  *[m.animate.shift(v) for m, v in zip(marks, shift)], FadeOut(lines), FadeOut(push),
                  *[Indicate(x, color=ORANGE, scale_factor=1.25) for x in (m1, m2)], run_time=0.9)

        # one copy becomes a pool of copies that flicker between two arrangements
        pool = [body(p, POOL_R, open_=(i in (0, 5))) for i, p in enumerate(POOL)]
        self.at("Every copy")
        self.play(FadeOut(marks), FadeOut(rep_a), FadeOut(rep_b), FadeOut(ph), FadeOut(m1), FadeOut(m2),
                  Transform(prot, body(POOL[0], POOL_R, open_=True)), run_time=0.7)
        pool[0] = prot
        self.play(LaggedStart(*[FadeIn(b, scale=0.7) for b in pool[1:]], lag_ratio=0.1), run_time=0.7)
        openset = {0, 5}

        def flick(toggle, rt=0.35):
            anims = []
            for i in toggle:
                openset.symmetric_difference_update({i})
                anims.append(Transform(pool[i], body(POOL[i], POOL_R, open_=i in openset)))
            self.play(*anims, run_time=rt)

        self.at("flickers")
        flick([0, 2]); self.wait(0.15)
        flick([5, 7, 3]); self.wait(0.15)
        flick([2, 6])                      # 3 of 8 open
        self.at("some working")
        flick([1, 6]); self.wait(0.1)
        flick([1, 6])

        # the phosphates land: the pool tips toward the open arrangement
        badges = [pbadge(1.15).move_to(rim(p, POOL_R, SITE)).set_z_index(3) for p in POOL]
        self.at("A phosphate makes")
        self.play(LaggedStart(*[FadeIn(b, scale=0.4, shift=DOWN * 0.3) for b in badges], lag_ratio=0.1), run_time=1.0)
        self.at("suit its charge")
        self.play(*[pop(b, 1.4) for b in badges], run_time=0.6)
        self.at("cheaper")
        flick([0, 2, 5], 0.4)
        self.wait(0.12)
        flick([4, 1], 0.3)
        self.wait(0.1)
        flick([4, 1], 0.3)                 # 6 of 8 open, 1 and 4 shut
        self.at("more copies")
        self.play(*[Indicate(pool[i], color=TEXT, scale_factor=1.12) for i in sorted(openset)], run_time=0.8)

        # the same shift works one protein on and another off
        title = T("glycogen phosphorylase", 34, TEXT).move_to([0, 3.0, 0])
        act = T("toward its active form", 32, GREEN).move_to([0, -3.1, 0])
        shut = [i for i in range(8) if i not in openset]
        self.at("In glycogen")
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.5)
        self.at("shifts")
        self.play(*[recolor(pool[i], GREEN) for i in sorted(openset)], *[recolor(pool[i], GREY) for i in shut], run_time=0.7)
        self.at("toward its")
        self.play(FadeIn(act, shift=UP * 0.1), run_time=0.5)
        title2 = T("glycogen synthase", 34, TEXT).move_to([0, 3.0, 0])
        inh = T("inhibited", 32, RED).move_to([0, -3.1, 0])
        self.at("inhibits")
        self.play(ReplacementTransform(title, title2), ReplacementTransform(act, inh),
                  *[recolor(pool[i], RED) for i in sorted(openset)], *[recolor(pool[i], GREEN) for i in shut], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Erase(SpokenScene):
    """a phosphatase takes the phosphate off with water; a separate lane from the kinase's; one ATP per round trip."""

    def construct(self):
        XL, XR = -4.5, 4.5
        R = 1.05
        copy_at = lambda x: np.array([x, 0.0, 0])
        cb = body(copy_at(XR), R, color=BLUE)
        pb = pbadge(1.3).move_to(rim(copy_at(XR), R, SITE)).set_z_index(3)
        copy = VGroup(cb, pb)

        # lower lane: the phosphatase
        phos = bchip("phosphatase", RED, 36, pad=0.3).move_to([0, -3.0, 0])
        a_low = arr([3.4, -2.15, 0], [-3.4, -2.15, 0], RED, w=7)
        wat = T("water", 30, GREY).move_to([1.6, -1.6, 0])
        # upper lane: the kinase
        kin = bchip("kinase", PURPLE, 36, pad=0.3).move_to([0, 3.0, 0])
        a_up = arr([-3.4, 2.15, 0], [3.4, 2.15, 0], PURPLE, w=7)
        atp_t, adp_t = T("ATP", 30, PINK), T("ADP", 30, PINK)
        rx_arrow = arr([0, 0, 0], [0.8, 0, 0], PINK, w=4, tip=0.18)
        rx = VGroup(atp_t, rx_arrow, adp_t).arrange(RIGHT, buff=0.25).move_to([-1.0, 1.6, 0])

        self.add(copy, phos, a_low)
        self.at("takes the phosphate")
        self.play(copy.animate.shift(LEFT * 4.5), run_time=0.9)
        copy.remove(pb)
        self.at("with water")
        self.play(FadeIn(wat, shift=UP * 0.1), pb.animate.shift(DOWN * 0.8 + LEFT * 0.3).set_opacity(0), run_time=0.8)
        self.remove(pb)
        self.play(copy.animate.shift(LEFT * 4.5), run_time=0.8)
        asis = T("as it was", 30, GREY).move_to([XL, -1.6, 0])
        self.at("exactly as it was")
        self.play(FadeIn(asis, shift=UP * 0.1), pop(cb, 1.12), run_time=0.7)

        # the kinase has its own lane
        self.at("kinase reaction")
        self.play(FadeOut(asis), FadeIn(kin, shift=DOWN * 0.15), GrowArrow(a_up), FadeIn(rx), run_time=0.8)
        a_rev = arr([3.4, 2.15, 0], [-3.4, 2.15, 0], RED, w=7)
        xmark = Line([-0.35, 1.8, 0], [0.35, 2.5, 0], color=RED, stroke_width=8)
        self.at("backwards")
        self.play(Transform(a_up, a_rev), Create(xmark), run_time=0.5)
        self.wait(0.35)
        self.play(Transform(a_up, arr([-3.4, 2.15, 0], [3.4, 2.15, 0], PURPLE, w=7)), FadeOut(xmark), run_time=0.4)
        self.at("different reaction")
        self.play(*glow(phos[1], phos[2], s=1.1), pop(wat, 1.2), Indicate(a_low, color=TEXT, scale_factor=1.0), run_time=0.8)

        # both go downhill
        def slope(y):
            return VGroup(arr([3.7, y + 0.3, 0], [4.4, y - 0.25, 0], GREY, w=4, tip=0.16),
                          T("downhill", 28, GREY).move_to([5.4, y, 0]))
        sl_up, sl_dn = slope(2.15), slope(-2.15)
        self.at("downhill")
        self.play(FadeIn(sl_up, shift=DOWN * 0.1), FadeIn(sl_dn, shift=DOWN * 0.1), run_time=0.7)

        # the marker and the eraser
        mk = T("marker", 30, GREY).move_to([2.6, 3.0, 0])
        er = T("eraser", 30, GREY).move_to([2.6, -3.0, 0])
        self.at("marker")
        self.play(FadeIn(mk, shift=RIGHT * 0.1), run_time=0.4)
        self.at("eraser")
        self.play(FadeIn(er, shift=RIGHT * 0.1), run_time=0.4)
        self.at("different tools")
        self.play(*glow(kin[1], kin[2], phos[1], phos[2], s=1.08), run_time=0.7)

        # one round trip: adding with the kinase, removing with the phosphatase
        self.at("likewise")
        self.play(copy.animate.shift(RIGHT * 3.2), run_time=0.5)
        pb2 = pbadge(1.3).move_to(atp_t.get_center()).set_z_index(3)
        self.play(FadeIn(pb2, scale=0.5), Indicate(atp_t, color=TEXT, scale_factor=1.25), run_time=0.3)
        self.play(pb2.animate.move_to(rim(copy_at(XL + 3.2), R, SITE)), run_time=0.4)
        copy.add(pb2)
        self.play(copy.animate.shift(RIGHT * 5.8), run_time=0.7)
        self.at("removing")
        self.play(copy.animate.shift(LEFT * 4.5), run_time=0.7)
        copy.remove(pb2)
        self.play(pb2.animate.shift(DOWN * 0.8).set_opacity(0), run_time=0.4)
        self.remove(pb2)
        self.play(copy.animate.shift(LEFT * 4.5), run_time=0.7)
        one = T("one ATP per round trip", 36, PINK).move_to([0.4, 0.0, 0])
        self.at("round trip")
        self.play(FadeIn(one, scale=0.9), Indicate(atp_t, color=TEXT, scale_factor=1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# the tank (scenes 5 and 6)
TC, TW, TH = np.array([-1.7, 0.0, 0]), 5.8, 3.7
COPY_R = 0.42
CELLS = [TC + np.array([x, y, 0]) for y in (1.15, 0.0, -1.15) for x in (-2.025, -0.675, 0.675, 2.025)]
G_X, G_W = 2.65, 0.7
G_BOT, G_TOP = TC[1] - TH / 2, TC[1] + TH / 2


def gauge_fill(n, color=GOLD):
    h = max(n / 12 * TH, 0.02)
    return Rectangle(width=G_W - 0.08, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([G_X, G_BOT + h / 2, 0])


class Tank:
    """twelve copies of a protein in a tank; the kinase is the tap above, the phosphatase the drain below."""

    def __init__(self, marked):
        self.tank = RoundedRectangle(corner_radius=0.2, width=TW, height=TH, stroke_color=GREY, stroke_width=3).move_to(TC)
        self.copies = [body(c, COPY_R, open_=False, sw=3.5) for c in CELLS]
        self.badges = [pbadge(1.0).move_to(rim(c, COPY_R, SITE)).set_z_index(3) for c in CELLS]
        self.on = set(marked)
        self.kin = bchip("kinase", PURPLE, 28, pad=0.22).move_to([TC[0], 2.85, 0])
        self.pho = bchip("phosphatase", RED, 28, pad=0.22).move_to([TC[0], -2.85, 0])
        self.a_in = arr([TC[0], 2.45, 0], [TC[0], G_TOP + 0.02, 0], PURPLE, w=6)
        self.a_out = arr([TC[0], G_BOT - 0.02, 0], [TC[0], -2.45, 0], RED, w=6)
        self.g_out = Rectangle(width=G_W, height=TH, stroke_color=GREY, stroke_width=3).move_to([G_X, TC[1], 0])
        self.g_fill = gauge_fill(len(self.on))

    def base(self):
        return [self.tank, *self.copies, self.kin, self.pho, self.a_in, self.a_out, self.g_out, self.g_fill]

    def shown(self):
        return [self.badges[i] for i in sorted(self.on)]

    def flip(self, on=(), off=()):
        """animations that add a phosphate to the copies in `on` and take one off the copies in `off`; returns them."""
        anims = []
        for i in on:
            if i not in self.on:
                self.on.add(i)
                anims.append(FadeIn(self.badges[i], scale=0.4, shift=DOWN * 0.15))
        for i in off:
            if i in self.on:
                self.on.discard(i)
                anims.append(FadeOut(self.badges[i], scale=0.6, shift=DOWN * 0.15))
        anims.append(Transform(self.g_fill, gauge_fill(len(self.on))))
        return anims


BASE = {0, 2, 5, 6, 9, 11}


class S05Balance(SpokenScene):
    """the share of protein carrying a phosphate is set by both enzymes: a sink with a tap and a drain."""

    def construct(self):
        T_ = Tank(BASE)
        lvl = T("level", 32, GOLD, weight=BOLD).move_to([5.0, 0.55, 0])
        lvl2 = VGroup(T("share carrying", 24, GREY), T("a phosphate", 24, GREY)).arrange(DOWN, buff=0.08).move_to([5.0, -0.2, 0])

        self.add(T_.tank, *T_.copies, *T_.shown())
        self.at("phosphatases")
        self.play(FadeIn(T_.pho, shift=UP * 0.15), run_time=0.5)
        tap = T("tap", 24, GREY).move_to([TC[0] + 0.55, 2.2, 0])
        drain = T("drain", 24, GREY).move_to([TC[0] + 0.65, -2.2, 0])
        self.at("a sink")
        self.play(FadeIn(T_.kin, shift=DOWN * 0.15), run_time=0.5)
        self.at("tap")
        self.play(GrowArrow(T_.a_in), FadeIn(tap), run_time=0.5)
        self.at("drain")
        self.play(GrowArrow(T_.a_out), FadeIn(drain), run_time=0.5)
        self.at("water level")
        self.play(FadeIn(T_.g_out), FadeIn(T_.g_fill), FadeIn(lvl, shift=LEFT * 0.1), run_time=0.7)
        # phosphates keep coming on and going off; the level holds still
        self.play(*T_.flip(on=[1], off=[2]), pop(T_.kin, 1.04), run_time=0.45)
        self.play(*T_.flip(on=[2], off=[9]), pop(T_.pho, 1.04), run_time=0.45)
        self.at("same way")
        self.play(FadeIn(lvl2, shift=UP * 0.1), *T_.flip(on=[9], off=[0]), run_time=0.5)
        self.at("carrying")
        self.play(*T_.flip(on=[7], off=[5]), pop(T_.kin, 1.04), run_time=0.45)
        self.at("both enzymes")
        self.play(*T_.flip(on=[5], off=[1]), *glow(T_.kin[1], T_.kin[2], T_.pho[1], T_.pho[2], s=1.08), run_time=0.6)

        # a signal turns the kinase up
        sig1 = bchip("signal", YELLOW, 28, pad=0.2).move_to([-5.45, 2.85, 0])
        act = arr([-4.55, 2.85, 0], [T_.kin.get_left()[0] - 0.05, 2.85, 0], GREEN, w=6)
        act_l = T("activates", 24, GREEN).move_to([-3.65, 3.3, 0])
        self.at("A signal")
        self.play(FadeIn(sig1, shift=RIGHT * 0.15), run_time=0.5)
        self.at("activating")
        self.play(GrowArrow(act), FadeIn(act_l), Transform(T_.a_in, arr([TC[0], 2.45, 0], [TC[0], G_TOP + 0.02, 0], PURPLE, w=13, tip=0.3)),
                  *glow(T_.kin[1], T_.kin[2], s=1.08), run_time=0.6)
        self.play(*T_.flip(on=[3, 8], off=[]), run_time=0.45)

        # or turns the phosphatase down
        sig2 = bchip("signal", YELLOW, 28, pad=0.2).move_to([-5.45, -2.85, 0])
        blk = inhib([-4.55, -2.85, 0], [T_.pho.get_left()[0] - 0.12, -2.85, 0], RED, w=6)
        blk_l = T("inhibits", 24, RED).move_to([-3.65, -3.3, 0])
        self.at("or by")
        self.play(FadeIn(sig2, shift=RIGHT * 0.15), run_time=0.5)
        self.at("inhibiting")
        self.play(Create(blk), FadeIn(blk_l), Transform(T_.a_out, arr([TC[0], G_BOT - 0.02, 0], [TC[0], -2.45, 0], RED, w=2.5, tip=0.12)),
                  run_time=0.6)
        self.play(*T_.flip(on=[4, 10], off=[]), run_time=0.45)
        self.at("Cells do")
        self.play(*glow(sig1[1], sig1[2], sig2[1], sig2[2], s=1.08), pop(T_.kin, 1.04), pop(T_.pho, 1.04), run_time=0.7)

        # hand over to scene 6: the signals go, the arrows return to normal, the tank settles back
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        back = T_.flip(on=sorted(BASE - T_.on), off=sorted(T_.on - BASE))
        self.play(FadeOut(VGroup(sig1, sig2, act, act_l, blk, blk_l, tap, drain, lvl, lvl2)),
                  Transform(T_.a_in, arr([TC[0], 2.45, 0], [TC[0], G_TOP + 0.02, 0], PURPLE, w=6)),
                  Transform(T_.a_out, arr([TC[0], G_BOT - 0.02, 0], [TC[0], -2.45, 0], RED, w=6)), *back, run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """four reasons it is a good switch, then the rule: writer, eraser, level."""

    def construct(self):
        T_ = Tank(BASE)
        self.add(*T_.base(), *T_.shown())
        items = [("1", "charge", ORANGE), ("2", "stays on", GOLD), ("3", "two enzymes", PINK), ("4", "ATP supply", PINK)]
        rows = VGroup(*[VGroup(T(n, 26, GREY, weight=BOLD), T(t, 26, c)).arrange(RIGHT, buff=0.25) for n, t, c in items])
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([4.75, 0.0, 0])
        rows[2][1].set_color(TEXT)

        self.at("four reasons")
        self.play(Indicate(T_.tank, color=TEXT, scale_factor=1.02), run_time=0.7)
        # 1: the charge
        i0 = 0
        mk1, mk2 = cmark("-", 1.1), cmark("-", 1.1)
        c0 = rim(CELLS[i0], COPY_R, SITE)
        mk1.move_to(c0 + np.array([-0.33, 0.3, 0])); mk2.move_to(c0 + np.array([-0.4, -0.08, 0]))
        self.at("adds charge")
        self.play(FadeIn(rows[0], shift=LEFT * 0.1), FadeIn(mk1, scale=0.4), FadeIn(mk2, scale=0.4), *glow(T_.badges[i0], s=1.5), run_time=0.8)
        # 2: it stays
        ring = Circle(radius=0.62, stroke_color=GOLD, stroke_width=3).move_to(CELLS[i0])
        self.at("stays")
        self.play(FadeIn(rows[1], shift=LEFT * 0.1), Create(ring), run_time=0.7)
        self.at("removes it")
        self.play(*glow(T_.pho[1], T_.pho[2], s=1.12), run_time=0.7)
        # 3: two enzymes
        self.at("Different enzymes")
        self.play(FadeIn(rows[2], shift=LEFT * 0.1), *glow(T_.kin[1], T_.kin[2], s=1.12), run_time=0.7)
        self.at("remove it")
        self.play(*glow(T_.pho[1], T_.pho[2], s=1.12), run_time=0.7)
        # 4: ATP keeps the kinase supplied
        atps = VGroup(*[bchip("ATP", PINK, 24, pad=0.16).move_to([x, y, 0]) for x, y in ((-5.5, 2.85), (-4.2, 3.3), (-4.2, 2.4))])
        feed = arr([-3.55, 2.85, 0], [T_.kin.get_left()[0] - 0.05, 2.85, 0], PINK, w=5)
        self.at("keeps the kinase")
        self.play(FadeIn(rows[3], shift=LEFT * 0.1), LaggedStart(*[FadeIn(a, shift=RIGHT * 0.15) for a in atps], lag_ratio=0.2),
                  GrowArrow(feed), run_time=0.9)

        # the rule
        self.at("keep this")
        self.play(FadeOut(rows), FadeOut(atps), FadeOut(feed), FadeOut(mk1), FadeOut(mk2), FadeOut(ring), run_time=0.7)
        writes = T("writes", 32, PURPLE, weight=BOLD).move_to([T_.kin.get_right()[0] + 1.0, 2.85, 0])
        erases = T("erases", 32, RED, weight=BOLD).move_to([T_.pho.get_right()[0] + 1.0, -2.85, 0])
        self.at("writes")
        self.play(FadeIn(writes, shift=LEFT * 0.1), *glow(T_.kin[1], T_.kin[2], s=1.12), run_time=0.7)
        self.at("erases")
        self.play(FadeIn(erases, shift=LEFT * 0.1), *glow(T_.pho[1], T_.pho[2], s=1.12), run_time=0.7)
        self.at("balance")
        self.play(*glow(T_.kin[1], T_.kin[2], T_.pho[1], T_.pho[2], s=1.1), run_time=0.7)
        lvl = T("level", 32, GOLD, weight=BOLD).move_to([5.0, 0.2, 0])
        self.at("sets the")
        self.play(FadeIn(lvl, shift=LEFT * 0.1), Indicate(T_.g_out, color=GOLD, scale_factor=1.04), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "A kinase writes, a phosphatase erases, and the balance sets the level."
