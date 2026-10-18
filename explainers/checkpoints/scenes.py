"""Checkpoints: make cells wait, then commit  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = DNA and chromosomes (the thing being copied, repaired, pulled apart)
  ORANGE = damage and radiation (broken DNA); also separase (the protease)
  RED    = wait / stop: the gate, the drug block, the checkpoint complex (MCC, Mad2, BubR1, Bub3)
  GREEN  = go / done / repaired
  TEAL   = Cdc20 (the activator)
  BLUE   = APC/C (the ubiquitin ligase)
  PURPLE = securin
  PINK   = cyclin B
  GOLD   = ubiquitin badge, the phosphate badge, the question mark, half-life marks
  TEXT   = kinetochores, laser
  GREY   = cell outlines, spindle microtubules, axes, de-emphasized
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E58FB5"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def dna(x, y, w=0.8, broken=True):
    """A chromosome fragment as a plain line; broken = two pieces with an orange break between."""
    if broken:
        a = Line([x - w / 2, y, 0], [x - 0.1, y, 0], color=YELLOW, stroke_width=6)
        b = Line([x + 0.1, y, 0], [x + w / 2, y, 0], color=YELLOW, stroke_width=6)
        k1 = Line([x - 0.06, y + 0.16, 0], [x + 0.06, y - 0.16, 0], color=ORANGE, stroke_width=4)
        k2 = Line([x + 0.06, y + 0.16, 0], [x - 0.06, y - 0.16, 0], color=ORANGE, stroke_width=4)
        return VGroup(a, b, k1, k2)
    return VGroup(Line([x - w / 2, y, 0], [x + w / 2, y, 0], color=YELLOW, stroke_width=6))


def ycell(x, y, r=0.5, broken=True):
    c = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([x, y, 0])
    return VGroup(c, dna(x, y, w=r * 1.3, broken=broken))


def cross(x, y, s=0.3, color=RED):
    return VGroup(Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=6),
                  Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=6))


def prog(x, y, w, frac, color=BLUE, h=0.4):
    """Progress bar fill anchored at the left edge."""
    return Rectangle(width=max(w * frac, 0.01), height=h, stroke_width=0, fill_color=color,
                     fill_opacity=0.7).move_to([x - w / 2 + max(w * frac, 0.01) / 2, y, 0])


def badge(text, color, r=0.26, size=22):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=1)
    return VGroup(c, T(text, size, BG, weight=BOLD).move_to(c))


class S00Title(TitleCard):
    LESSON = "Checkpoints and irreversible transitions"
    TITLE = "Checkpoints make cells wait, then commit"


# ---------------------------------------------------------------------------------------------
class S01Rad9(SpokenScene):
    """irradiated rad9 cell divides on and dies; the same cell held by a drug repairs; what was the gene for?"""

    def construct(self):
        y1, y2 = 1.6, -1.95
        head1 = T("Budding yeast without RAD9, irradiated", 28, GREY).move_to([0, 3.2, 0])
        c1 = ycell(-4.3, y1, 0.75)
        rad = VGroup(*[arr([-6.25, y1 + d + 0.6, 0], [-5.15, y1 + d * 0.6, 0], ORANGE, w=4, tip=0.16) for d in (0.5, 0.0, -0.5)])
        radl = T("radiation", 24, ORANGE).move_to([-5.6, y1 - 1.2, 0])
        self.at("Irradiate a budding")
        self.play(FadeIn(head1), FadeIn(c1), run_time=0.7)
        self.play(LaggedStart(*[GrowArrow(a) for a in rad], lag_ratio=0.2), FadeIn(radl), run_time=1.0)

        self.at("It keeps dividing")
        a1 = arr([-3.35, y1, 0], [-2.75, y1, 0], GREY)
        c2a, c2b = ycell(-1.95, y1, 0.6), ycell(-0.55, y1, 0.6)
        self.play(GrowArrow(a1), TransformFromCopy(c1, c2a), TransformFromCopy(c1, c2b), run_time=0.9)
        a2 = arr([0.3, y1, 0], [0.9, y1, 0], GREY)
        xs = [1.7, 2.8, 3.9, 5.0]
        c3 = [ycell(x, y1, 0.5) for x in xs]
        self.play(GrowArrow(a2), TransformFromCopy(c2a, c3[0]), TransformFromCopy(c2a, c3[1]),
                  TransformFromCopy(c2b, c3[2]), TransformFromCopy(c2b, c3[3]), run_time=0.9)
        gen = T("several generations", 26, GREY).move_to([0.3, y1 - 1.2, 0])
        self.play(FadeIn(gen), run_time=0.4)

        self.at("and it dies")
        xx = VGroup(*[cross(x, y1, 0.34) for x in xs])
        dies = T("dies", 36, RED, weight=BOLD).move_to([3.9, y1 - 1.2, 0])
        self.play(Create(xx), FadeIn(dies), *[c.animate.set_opacity(0.35) for c in c3], run_time=0.8)

        self.at("Hold the same cell")
        head2 = T("The same cell, held back with a drug", 28, GREY).move_to([0, y2 + 1.55, 0])
        d = ycell(-4.3, y2, 0.75)
        wall = Line([-3.1, y2 - 0.9, 0], [-3.1, y2 + 0.9, 0], color=RED, stroke_width=12)
        wl = T("drug", 26, RED).move_to([-3.1, y2 - 1.25, 0])
        self.play(FadeIn(head2), FadeIn(d), run_time=0.6)
        self.play(Create(wall), FadeIn(wl), run_time=0.6)

        self.at("repairs the damage")
        fixed = dna(-4.3, y2, w=0.75 * 1.3, broken=False)
        okl = T("repaired", 36, GREEN, weight=BOLD).move_to([-1.3, y2, 0])
        self.play(ReplacementTransform(d[1], fixed), run_time=0.7)
        self.play(FadeIn(okl, shift=RIGHT * 0.2), run_time=0.4)

        self.at("So what was the gene")
        gene = chip("RAD9", GOLD, size=36).move_to([1.5, y2, 0])
        q = T("?", 100, GOLD, weight=BOLD).move_to([3.1, y2, 0])
        ql = T("what was it for?", 28, GOLD).move_to([5.0, y2, 0])
        self.play(FadeIn(gene, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(q, scale=0.5), FadeIn(ql), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Wait(SpokenScene):
    """repair fills a bar; a red gate holds division until it is full; remove the gate and division goes on time."""

    def construct(self):
        yc = 1.1
        A = chip("repair", TEXT, size=40).move_to([-4.2, yc, 0])
        B = chip("division", TEXT, size=40).move_to([4.2, yc, 0])
        path = arr([-2.65, yc, 0], [2.4, yc, 0], GREY, w=7, tip=0.3)
        bw = 4.2
        by = -0.45
        outline = Rectangle(width=bw, height=0.55, stroke_color=GREY, stroke_width=3).move_to([-4.2, by, 0])
        fillr = prog(-4.2, by, bw, 0.0, h=0.55)
        self.at("not a repair gene")
        self.play(FadeIn(A, shift=RIGHT * 0.2), FadeIn(outline), FadeIn(B, shift=LEFT * 0.2), GrowArrow(path), run_time=0.9)
        gate = Rectangle(width=0.4, height=2.1, stroke_width=0, fill_color=RED, fill_opacity=0.95).move_to([0, yc, 0])
        wait = T("wait", 40, RED, weight=BOLD).move_to([0, yc + 1.6, 0])
        self.at("a gene for waiting")
        self.play(FadeIn(gate, scale=1.3), FadeIn(wait), path.animate.set_color(RED), run_time=0.7)

        self.at("named such a control")
        ck = T("checkpoint", 40, RED, weight=BOLD).move_to([0, yc + 1.6, 0])
        self.play(ReplacementTransform(wait, ck), run_time=0.5)

        self.at("makes one cell cycle event wait")
        ea = T("earlier event", 26, GREY).move_to([-4.2, yc + 0.95, 0])
        eb = T("later event", 26, GREY).move_to([4.2, yc + 0.95, 0])
        self.play(FadeIn(ea), FadeIn(eb), run_time=0.4)
        cur = fillr
        self.add(cur)
        for f in [0.3, 0.6, 1.0]:
            nxt = prog(-4.2, by, bw, f, color=GREEN if f == 1.0 else BLUE, h=0.55)
            self.play(Transform(cur, nxt), run_time=0.6)
        cap1 = T("B starts when A is done", 38, GREEN).move_to([0, -2.4, 0])
        self.play(gate.animate.set_opacity(0.0), path.animate.set_color(GREEN), FadeOut(ck),
                  *[B[0].animate.set_stroke(GREEN).set_fill(GREEN, 0.25), B[1].animate.set_color(GREEN)],
                  FadeIn(cap1), run_time=0.6)

        # reset to the neutral state while the new case begins
        self.at("Remove it")
        nog = T("no checkpoint", 40, RED).move_to([0, yc + 1.6, 0])
        self.play(FadeOut(cap1), FadeOut(gate),
                  Transform(cur, prog(-4.2, by, bw, 0.4, color=BLUE, h=0.55)),
                  path.animate.set_color(GREY),
                  *[B[0].animate.set_stroke(TEXT).set_fill(TEXT, 0.16), B[1].animate.set_color(TEXT)],
                  FadeIn(nog), run_time=0.7)
        self.at("on time instead")
        cap2 = T("B starts on time, A unfinished", 38, RED).move_to([0, -2.4, 0])
        self.play(path.animate.set_color(RED),
                  *[B[0].animate.set_stroke(RED).set_fill(RED, 0.25), B[1].animate.set_color(RED)],
                  FadeIn(cap2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Kinetochore(SpokenScene):
    """spindle: attached chromosomes, one unattached kinetochore, laser, anaphase after ~20 min, signal source."""

    def construct(self):
        P_L, P_R = np.array([-5.0, -0.1, 0]), np.array([5.0, -0.1, 0])
        cellb = Ellipse(width=11.6, height=5.2, stroke_color=GREY, stroke_width=4, fill_color=GREY,
                        fill_opacity=0.08).move_to([0, -0.1, 0])
        pl = Dot(P_L, radius=0.16, color=GREY)
        pr = Dot(P_R, radius=0.16, color=GREY)
        plab = T("pole", 24, GREY).move_to([-5.0, -3.1, 0])
        prlab = T("pole", 24, GREY).move_to([5.0, -3.1, 0])

        chroms = []
        ys = [1.5, -0.1, -1.7]
        mts = VGroup()
        for y in ys:
            lb = RoundedRectangle(corner_radius=0.08, width=0.2, height=0.7, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([-0.2, y, 0])
            rb = lb.copy().move_to([0.2, y, 0])
            lk = Dot([-0.36, y, 0], radius=0.1, color=TEXT)
            rk = Dot([0.36, y, 0], radius=0.1, color=TEXT)
            ml = always_redraw(lambda lk=lk: Line(P_L, lk.get_center(), color=GREY, stroke_width=2).set_opacity(0.7))
            mr = always_redraw(lambda rk=rk: Line(P_R, rk.get_center(), color=GREY, stroke_width=2).set_opacity(0.7))
            chroms.append((lb, rb, lk, rk, ml, mr))
        self.at("Before anaphase")
        self.play(FadeIn(cellb), FadeIn(pl), FadeIn(pr), FadeIn(plab), FadeIn(prlab), run_time=0.8)
        for lb, rb, lk, rk, ml, mr in chroms:
            self.add(ml, mr)
        self.play(*[FadeIn(m) for c in chroms for m in (c[0], c[1], c[2], c[3])], run_time=0.8)

        self.at("called the kinetochore")
        klab = T("kinetochore", 28, TEXT).move_to([2.0, -3.15, 0])
        ka = arr([1.5, -2.9, 0], [0.5, -1.9, 0], TEXT, w=3, tip=0.16)
        self.play(FadeIn(klab), GrowArrow(ka), run_time=0.6)

        # the odd chromosome
        ox, oy = -3.3, 1.15
        olb = RoundedRectangle(corner_radius=0.08, width=0.2, height=0.7, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([ox - 0.17, oy, 0])
        orb = olb.copy().move_to([ox + 0.17, oy, 0])
        olk = Dot([ox - 0.33, oy, 0], radius=0.1, color=TEXT)
        ork = Dot([ox + 0.33, oy, 0], radius=0.1, color=TEXT)
        ring = Circle(radius=0.22, stroke_color=RED, stroke_width=4).move_to(ork)
        oml = always_redraw(lambda: Line(P_L, olk.get_center(), color=GREY, stroke_width=2).set_opacity(0.7))
        ulab = T("unattached kinetochore", 28, RED).move_to([-2.2, 3.0, 0])
        ua = arr([-2.8, 2.7, 0], [-2.95, 1.55, 0], RED, w=3, tip=0.16)
        self.at("only one pole")
        self.add(oml)
        self.play(FadeIn(olb), FadeIn(orb), FadeIn(olk), FadeIn(ork), FadeOut(klab), FadeOut(ka), run_time=0.7)
        self.play(Create(ring), FadeIn(ulab), GrowArrow(ua), run_time=0.7)

        self.at("destroyed its unattached")
        laser = Line([-6.2, 2.0, 0], ork.get_center() + np.array([-0.1, 0.05, 0]), color=TEXT, stroke_width=7)
        ll = T("laser", 24, TEXT).move_to([-5.9, 2.4, 0])
        self.play(Create(laser), FadeIn(ll), run_time=0.5)
        self.play(Flash(ork, color=TEXT, line_length=0.3, flash_radius=0.4), FadeOut(ork), FadeOut(ring),
                  FadeOut(ulab), FadeOut(ua), run_time=0.6)
        self.play(FadeOut(laser), FadeOut(ll), run_time=0.3)

        self.at("anaphase followed")
        tm = M("20 ± 2.5 min", 34, GREEN).move_to([4.3, 3.05, 0])
        self.play(FadeIn(tm), run_time=0.4)
        anims = []
        for lb, rb, lk, rk, ml, mr in chroms:
            anims += [lb.animate.shift(LEFT * 1.6), lk.animate.shift(LEFT * 1.6),
                      rb.animate.shift(RIGHT * 1.6), rk.animate.shift(RIGHT * 1.6)]
        self.play(*anims, run_time=1.6)

        self.at("never reached the middle")
        mid = DashedLine([0, -2.6, 0], [0, 2.5, 0], color=GREY, stroke_width=3)
        midl = T("middle", 24, GREY).move_to([0, 3.0, 0])
        self.play(Create(mid), FadeIn(midl), Indicate(VGroup(olb, orb, olk), color=YELLOW, scale_factor=1.2), run_time=1.0)

        self.at("signal comes from")
        ghost = DashedVMobject(Circle(radius=0.22, stroke_color=RED, stroke_width=4), num_dashes=16).move_to(ork.get_center())
        rip = [Circle(radius=0.25, stroke_color=RED, stroke_width=4).move_to(ork.get_center()) for _ in range(3)]
        sl = T("wait signal", 32, RED, weight=BOLD).move_to([-2.2, 3.0, 0])
        self.play(FadeIn(ghost), FadeIn(sl), FadeOut(midl), run_time=0.5)
        for r in rip:
            self.play(r.animate.scale(3.2).set_stroke(opacity=0), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def cup_pts(s=1.1):
    return [(0, 0), (2.0, 0), (2.0, .9), (1.75, .9), (1.75, .45), (1.45, .45), (1.45, .9), (0, .9)]


def key_pts():
    return [(1.1, 1.45), (2.1, 1.45), (2.1, .95), (1.73, .95), (1.73, .47), (1.47, .47), (1.47, .95), (1.1, .95)]


def mk_poly(pts, color, s, origin):
    p = Polygon(*[np.array([x * s + origin[0], y * s + origin[1], 0]) for x, y in pts], stroke_color=color,
                stroke_width=3, fill_color=color, fill_opacity=0.3)
    return p


def mk_apc(show_key=True):
    """APC/C blob with the Cdc20 cup on top; optionally the BubR1 key sitting in the slot."""
    s = 1.1
    blob = RoundedRectangle(corner_radius=0.6, width=7.0, height=1.8, stroke_color=BLUE, stroke_width=4,
                            fill_color=BLUE, fill_opacity=0.16).move_to([0, -1.3, 0])
    lab = T("APC/C", 32, BLUE, weight=BOLD).move_to([1.6, -1.3, 0])
    cup = mk_poly(cup_pts(), TEAL, s, (-2.3, -0.4))
    cl = T("Cdc20", 24, TEAL).move_to([-2.3 + 0.72 * s, -0.4 + 0.45 * s * 0.9 + 0.05, 0])
    key = mk_poly(key_pts(), RED, s, (-2.3, -0.4))
    kl = T("BubR1", 22, RED).move_to([-2.3 + 1.6 * s, -0.4 + 1.2 * s, 0])
    g = VGroup(blob, lab, cup, cl)
    k = VGroup(key, kl)
    return g, k


class S04Mcc(SpokenScene):
    """kinetochore -> four chips gather into the MCC; Cdc20 cup on APC/C; the BubR1 key sits in the slot."""

    def construct(self):
        ky = 2.45
        kin = VGroup(Circle(radius=0.2, stroke_color=RED, stroke_width=4), Dot(radius=0.1, color=TEXT)).move_to([-5.3, ky, 0])
        kl = T("unattached\nkinetochore", 22, TEXT, line_spacing=0.8).move_to([-5.3, ky - 0.85, 0])
        ar = arr([-4.85, ky, 0], [-3.95, ky, 0], RED)
        names = [("Mad2", RED, -2.7), ("Cdc20", TEAL, -0.75), ("BubR1", RED, 1.35), ("Bub3", RED, 3.25)]
        chips = [chip(n, c, size=28).move_to([x, ky + 0.0, 0]) for n, c, x in names]
        box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=8.1, height=1.25, stroke_color=RED, stroke_width=3), num_dashes=70).move_to([0.25, ky, 0])
        mlab = T("mitotic checkpoint complex (MCC)", 24, RED).move_to([0.25, ky + 0.95, 0])
        self.at("Unattached kinetochores promote")
        self.play(FadeIn(kin), FadeIn(kl), run_time=0.5)
        self.play(GrowArrow(ar), run_time=0.4)
        self.at("mitotic checkpoint complex")
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in chips], lag_ratio=0.25), run_time=1.4)
        self.play(Create(box), FadeIn(mlab), run_time=0.7)

        apc, key = mk_apc()
        self.at("is the activator")
        self.play(FadeIn(apc[0]), FadeIn(apc[1]), run_time=0.6)
        self.play(TransformFromCopy(chips[1], VGroup(apc[2], apc[3])), run_time=0.9)

        self.at("sit in the binding sites")
        self.play(TransformFromCopy(chips[2], key), run_time=1.1)

        self.at("broken off in the lock")
        held = T("APC/C with Cdc20 is held back", 32, RED).move_to([0, -3.1, 0])
        self.play(Indicate(key[0], color=RED, scale_factor=1.15), FadeIn(held), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Destroy(SpokenScene):
    """the key lifts out; securin and cyclin B are tagged and destroyed; separase wakes and cuts the cohesin link."""

    def construct(self):
        apc, key = mk_apc()
        self.add(apc, key)
        lastk = chip("last kinetochore attached", GREEN, size=28).move_to([-3.0, 2.6, 0])
        self.at("When the last kinetochore")
        self.play(FadeIn(lastk), run_time=0.5)

        self.at("releases its grip")
        self.play(key.animate.shift(UP * 1.1).set_opacity(0), run_time=0.8)
        self.play(Indicate(apc[2], color=GREEN, scale_factor=1.12), FadeOut(lastk), run_time=0.7)

        sec = chip("securin", PURPLE, size=30).move_to([0.5, 1.9, 0])
        cyc = chip("cyclin B", PINK, size=30).move_to([2.9, 1.9, 0])
        prot = RoundedRectangle(corner_radius=0.3, width=2.0, height=2.0, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.14).move_to([5.3, -1.3, 0])
        plab = T("proteasome", 24, GREY).move_to([5.3, -1.9, 0])
        a1 = arr([0.5, -0.4, 0], [0.5, 1.45, 0], GOLD, w=5)
        a2 = arr([2.9, -0.4, 0], [2.9, 1.45, 0], GOLD, w=5)
        self.at("ubiquitinates securin")
        self.play(FadeIn(sec), FadeIn(cyc), GrowArrow(a1), GrowArrow(a2), run_time=0.8)
        ub1 = badge("Ub", GOLD, r=0.3, size=24).move_to(sec.get_corner(UR))
        ub2 = badge("Ub", GOLD, r=0.3, size=24).move_to(cyc.get_corner(UR))
        self.play(FadeIn(ub1, scale=0.5), FadeIn(ub2, scale=0.5), run_time=0.5)
        self.at("proteasome destroys")
        self.play(FadeIn(prot), FadeIn(plab), FadeOut(a1), FadeOut(a2), run_time=0.5)
        g1, g2 = VGroup(sec, ub1), VGroup(cyc, ub2)
        self.play(g1.animate.scale(0.3).move_to(prot.get_center()).set_opacity(0),
                  g2.animate.scale(0.3).move_to(prot.get_center()).set_opacity(0), run_time=1.1)

        self.at("Securin had held separase")
        self.play(FadeOut(VGroup(apc, prot, plab)), run_time=0.5)
        sep = chip("separase", ORANGE, size=36).move_to([-3.6, 0.9, 0])
        clamp = chip("securin", PURPLE, size=30).move_to([-3.6, 1.6, 0])
        inact = T("inactive", 28, GREY).move_to([-3.6, 0.1, 0])
        sep_dim = [sep[0].animate.set_stroke(opacity=0.45).set_fill(opacity=0.07), sep[1].animate.set_opacity(0.55)]
        self.play(FadeIn(sep), FadeIn(clamp), FadeIn(inact), run_time=0.6)
        self.play(*sep_dim, run_time=0.4)

        self.at("Freed")
        lb = RoundedRectangle(corner_radius=0.1, width=0.4, height=1.8, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([0.5, -2.0, 0])
        rb = lb.copy().move_to([1.5, -2.0, 0])
        link = Line([0.7, -2.0, 0], [1.3, -2.0, 0], color=TEXT, stroke_width=12)
        self.play(FadeOut(clamp), FadeOut(inact),
                  sep[0].animate.set_stroke(opacity=1).set_fill(opacity=0.16), sep[1].animate.set_opacity(1),
                  FadeIn(lb), FadeIn(rb), FadeIn(link), run_time=0.8)

        self.at("cuts")
        self.play(sep.animate.move_to([1.0, -0.4, 0]), run_time=0.8)
        lab = T("Scc1, the cohesin", 28, TEXT).move_to([1.0, -3.3, 0])
        self.play(FadeIn(lab), Flash(link, color=ORANGE, line_length=0.3, flash_radius=0.5), FadeOut(link), run_time=0.6)

        self.at("Anaphase begins")
        ag = arr([-0.2, -2.0, 0], [-1.8, -2.0, 0], GREEN, w=7, tip=0.3)
        bg = arr([2.2, -2.0, 0], [3.8, -2.0, 0], GREEN, w=7, tip=0.3)
        self.play(lb.animate.shift(LEFT * 1.8), rb.animate.shift(RIGHT * 1.8), FadeOut(sep), FadeOut(lab), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Oneway(SpokenScene):
    """securin time course (100,71,50,35,25), half-life 10 min, poison at 10 min; phosphate vs destruction; wait + one way."""

    def construct(self):
        ox, oy, W, H, XM = -5.6, -2.5, 10.8, 4.9, 30.0

        def P(t, v):
            return np.array([ox + t / XM * W, oy + v / 100.0 * H, 0])

        xa = Line(P(0, 0), P(30, 0), color=GREY, stroke_width=3)
        ya = Line(P(0, 0), P(0, 100), color=GREY, stroke_width=3)
        ticks = VGroup()
        for t in (0, 10, 20, 30):
            ticks.add(M(str(t), 22, GREY).move_to(P(t, 0) + DOWN * 0.35))
        for v in (0, 50, 100):
            ticks.add(M(str(v), 22, GREY).move_to(P(0, v) + LEFT * 0.45))
        xt = T("minutes after metaphase", 26, GREY).move_to([ox + W / 2, -3.3, 0])
        yt = T("securin, % of metaphase value", 26, GREY).move_to([-3.3, 3.1, 0])
        tag = T("made-up data", 24, GREY).move_to([5.0, 3.1, 0])
        self.at("made up time course")
        self.play(Create(xa), Create(ya), FadeIn(ticks), FadeIn(xt), FadeIn(yt), FadeIn(tag), run_time=1.0)

        data = [(0, 100), (5, 71), (10, 50), (15, 35), (20, 25)]
        dots = VGroup(*[Dot(P(t, v), radius=0.11, color=PURPLE) for t, v in data])
        curve = VMobject(color=PURPLE, stroke_width=5)
        curve.set_points_smoothly([P(t, 100 * math.exp(-0.0693 * t)) for t in np.linspace(0, 20, 21)])
        self.at("falls from")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.25), run_time=1.5)
        self.play(Create(curve), run_time=0.8)

        self.at("half life")
        hl_h = DashedLine(P(0, 50), P(10, 50), color=GOLD, stroke_width=3)
        hl_v = DashedLine(P(10, 50), P(10, 0), color=GOLD, stroke_width=3)
        hl = T("half-life: 10 min", 30, GOLD).move_to([1.6, 0.9, 0])
        self.play(Create(hl_h), Create(hl_v), FadeIn(hl), run_time=1.0)

        self.at("Add a spindle poison")
        pv = DashedLine(P(10, 0), P(10, 100), color=RED, stroke_width=4)
        pl = T("spindle poison", 30, RED).move_to([0.0, 2.6, 0])
        self.play(FadeOut(hl), Create(pv), FadeIn(pl), run_time=0.8)
        flat = Line(P(10, 50), P(30, 50), color=PURPLE, stroke_width=5)
        stays = T("stays near 50", 30, PURPLE).move_to([2.6, 0.25, 0])
        self.play(dots[3].animate.set_opacity(0.2), dots[4].animate.set_opacity(0.2),
                  curve.animate.set_stroke(opacity=0.25), run_time=0.4)
        self.play(Create(flat), FadeIn(stays), run_time=0.9)

        # --- phosphate versus destruction ---------------------------------------------------
        self.at("A phosphate")
        self.play(FadeOut(VGroup(xa, ya, ticks, xt, yt, tag, dots, curve, hl_h, hl_v, pv, pl, flat, stays)), run_time=0.7)
        p1 = chip("protein", PURPLE, size=40).move_to([-3.4, 1.6, 0])
        pb = badge("P", GOLD, r=0.32, size=26).move_to(p1.get_corner(UR))
        t1 = T("phosphate: removed in seconds", 36, GOLD).move_to([2.2, 1.6, 0])
        self.play(FadeIn(p1), FadeIn(pb, scale=0.5), run_time=0.6)
        self.play(pb.animate.shift([1.0, 0.9, 0]).set_opacity(0), FadeIn(t1), run_time=0.8)

        self.at("a destroyed protein")
        p2 = chip("protein", PURPLE, size=40).move_to([-3.4, -0.6, 0])
        self.play(FadeIn(p2), run_time=0.4)
        self.play(p2.animate.scale(0.2).set_opacity(0), run_time=0.7)
        t2 = T("destroyed: must be made again", 36, RED).move_to([2.2, -0.6, 0])
        p3 = chip("new protein", PURPLE, size=40).move_to([-3.4, -2.4, 0])
        self.play(FadeIn(t2), run_time=0.4)
        self.play(FadeIn(p3, shift=UP * 0.2), run_time=0.7)

        self.at("So a checkpoint makes")
        self.play(FadeOut(VGroup(p1, pb, t1, p3, t2)), run_time=0.6)
        gate = Rectangle(width=0.45, height=2.4, stroke_width=0, fill_color=RED, fill_opacity=0.95).move_to([-3.4, 0.9, 0])
        gl = T("checkpoint: wait", 40, RED, weight=BOLD).move_to([-3.4, -0.9, 0])
        self.play(FadeIn(gate, scale=1.3), FadeIn(gl), run_time=0.7)
        self.at("destruction makes")
        go = arr([1.2, 1.1, 0], [5.4, 1.1, 0], GREEN, w=12, tip=0.5)
        back = arr([4.8, -0.1, 0], [2.0, -0.1, 0], RED, w=7).set_opacity(0.5)
        bx = cross(3.4, -0.1, 0.4)
        dl = T("destruction: one way", 40, GREEN, weight=BOLD).move_to([3.3, -1.3, 0])
        self.play(GrowArrow(go), FadeIn(dl), run_time=0.7)
        self.play(FadeIn(back), Create(bx), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Checkpoints make events wait; destruction makes them one-way."
