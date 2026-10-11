"""Section film: give one kinase an ATP of its own (detecting-a-signal, section 'Which kinase?')

COLOR MAP (one colour per concept, whole film)
  BLUE   = the kinase (block; the ATP pocket is a notch in it)
  YELLOW = ATP, and the open question marks
  ORANGE = the gatekeeper residue (a block inside the pocket) and what replaces it
  PURPLE = the bulky group added to ATP
  GREEN  = a phosphate badge "P"
  TEAL   = a protein whose level or state changed when the kinase is removed
  RED    = what fails: a crossed-out kinase, a misfit
  GREY   = other proteins, membranes, labels
No molecular structures: kinase = block with a notch, ATP = chip with a tab, groups = squares.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CE0"
DARK = "#0f1117"


def V(x=0.0, y=0.0):
    return np.array([x, y, 0.0])


def badge(p, txt="P", col=GREEN):
    c = Circle(radius=0.25, color=col, stroke_width=3, fill_color=col, fill_opacity=0.9).move_to(p)
    return VGroup(c, T(txt, size=24, color=DARK, weight=BOLD).move_to(c))


def dchip(text, color=GREY, size=28, pad=0.2):
    lab = T(text, size=size, color=color)
    w, h = lab.width + 2 * pad, lab.height + 2 * pad
    box = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color,
                                          stroke_width=2.5), num_dashes=36)
    return VGroup(box, lab.move_to(box))


def arrow(a, b, col=GREY, sw=4):
    return Arrow(a, b, buff=0.08, color=col, stroke_width=sw, max_tip_length_to_length_ratio=0.25)


# ---------- the kinase and its ATP (all in local coordinates, scaled and placed by c, s) ----------
def W(c, s, x, y):
    return c + s * V(x, y)


def kinase_body(c, s):
    pts = [(-2.4, -1.7), (2.4, -1.7), (2.4, 1.7), (1.2, 1.7), (1.2, 0.1), (-1.2, 0.1), (-1.2, 1.7), (-2.4, 1.7)]
    return Polygon(*[W(c, s, *p) for p in pts], color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.22)


def rect(c, s, x0, x1, y0, y1, col, fo=0.55, sw=3):
    r = Rectangle(width=s * (x1 - x0), height=s * (y1 - y0), color=col, stroke_width=sw,
                  fill_color=col, fill_opacity=fo)
    return r.move_to(W(c, s, (x0 + x1) / 2, (y0 + y1) / 2))


def gate_big(c, s):
    return rect(c, s, 0.55, 1.2, 0.1, 1.0, ORANGE)


def gate_small(c, s):
    return rect(c, s, 1.0, 1.2, 0.1, 0.55, ORANGE)


def hole(c, s):
    r = Rectangle(width=s * 0.65, height=s * 0.9, color=ORANGE, stroke_width=2.5).move_to(W(c, s, 0.875, 0.55))
    return DashedVMobject(r, num_dashes=24)


def atp(c, s, bulky=False, fs=26):
    """ATP chip seated in the pocket at local (-0.5, 0.5); tab or purple bulky square on its right."""
    body = RoundedRectangle(corner_radius=0.1, width=s * 1.3, height=s * 0.7, color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=0.28).move_to(W(c, s, -0.5, 0.5))
    lab = T("ATP", size=fs, color=YELLOW).move_to(body)
    if bulky:
        ext = rect(c, s, 0.15, 0.85, 0.15, 0.85, PURPLE, fo=0.6)
    else:
        ext = rect(c, s, 0.15, 0.45, 0.35, 0.65, YELLOW, fo=0.5)
    return VGroup(body, lab, ext)


class S00Title(TitleCard):
    LESSON = "Detecting a Signal"
    TITLE = "Give One Kinase an ATP of Its Own"


def protein_panel(cx, title, n_p, tube):
    """panel with a kinase on top and five proteins; n_p of them get a phosphate badge (idealised)."""
    cy = -0.1
    if tube:
        fr = VMobject(color=GREY, stroke_width=6)
        fr.set_points_as_corners([V(cx - 2.6, 2.3), V(cx - 2.6, -2.5), V(cx + 2.6, -2.5), V(cx + 2.6, 2.3)])
    else:
        fr = RoundedRectangle(corner_radius=0.7, width=5.2, height=4.9, color=GREY, stroke_width=6).move_to(V(cx, cy))
    ttl = T(title, size=28, color=GREY).move_to(V(cx, 2.85))
    k = chip("kinase", BLUE, 26).move_to(V(cx, 1.5))
    pos = [(-1.5, 0.3), (0, 0.3), (1.5, 0.3), (-0.75, -1.1), (0.75, -1.1)]
    names = "ABCDE"
    ps = VGroup(*[chip(names[i], GREY, 26, pad=0.22).move_to(V(cx + x, y)) for i, (x, y) in enumerate(pos)])
    bs = VGroup(*[badge(ps[i].get_corner(UR) + V(0.08, 0.08)) for i in n_p])
    return fr, ttl, k, ps, bs


class S01Tube(SpokenScene):
    def construct(self):
        kin = chip("kinase", BLUE, 44).move_to(V(-4.2, 0.2))
        qs = VGroup(*[chip("?", YELLOW, 44).move_to(V(0.8, y)) for y in (1.9, 0.2, -1.5)])
        arrs = VGroup(*[arrow(kin.get_right(), q.get_left()) for q in qs])
        qlab = T("which proteins?", size=34, color=YELLOW).move_to(V(3.9, 0.2))
        self.at("have a kinase")
        self.play(FadeIn(kin, scale=0.7), run_time=0.6)
        self.at("do not know")
        self.play(LaggedStart(*[Create(a) for a in arrs], lag_ratio=0.25),
                  LaggedStart(*[FadeIn(q, scale=0.6) for q in qs], lag_ratio=0.25), FadeIn(qlab), run_time=1.0)
        # panels
        tf, tt, tk, tp, tb = protein_panel(-3.2, "test tube", range(5), True)
        cf, ct, ck, cp, cb = protein_panel(3.2, "in a cell", [0, 3], False)
        note = T("idealised: counts are for illustration", size=22, color=GREY).move_to(V(0, -3.15))
        self.at("A purified kinase")
        self.play(FadeOut(kin), FadeOut(qs), FadeOut(arrs), FadeOut(qlab), run_time=0.3)
        self.play(Create(tf), FadeIn(tt), FadeIn(tk), FadeIn(tp, lag_ratio=0.1), FadeIn(note), run_time=0.8)
        self.at("what it can phosphorylate")
        self.play(LaggedStart(*[FadeIn(b, scale=0.4) for b in tb], lag_ratio=0.2), run_time=1.4)
        self.at("more than it does in a cell")
        self.play(Create(cf), FadeIn(ct), FadeIn(ck), FadeIn(cp, lag_ratio=0.1), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(b, scale=0.4) for b in cb], lag_ratio=0.3), run_time=0.8)
        # prediction
        sq = chip("sequence", GREY, 40).move_to(V(-4.0, 0.2))
        cands = VGroup(*[dchip(n, GREY, 40).move_to(V(0.6, y)) for n, y in zip("ABC", (1.6, 0.2, -1.2))])
        ar2 = VGroup(*[arrow(sq.get_right(), c.get_left()) for c in cands])
        clab = T("candidates", size=40, color=YELLOW).move_to(V(3.9, 0.2))
        self.at("Prediction from sequence")
        self.play(*[FadeOut(m) for m in (tf, tt, tk, tp, tb, cf, ct, ck, cp, cb, note)], run_time=0.5)
        self.play(FadeIn(sq, scale=0.7), LaggedStart(*[Create(a) for a in ar2], lag_ratio=0.2),
                  LaggedStart(*[FadeIn(c) for c in cands], lag_ratio=0.2), run_time=1.0)
        self.at("gives candidates")
        self.play(FadeIn(clab, shift=LEFT * 0.2), run_time=0.5)
        self.finish()


class S02Limits(SpokenScene):
    def construct(self):
        k = chip("kinase", BLUE, 56).move_to(V(-3.6, 0.8))
        p = chip("protein", GREY, 56).move_to(V(3.6, 0.8))
        self.at("Finding the kinase")
        self.play(FadeIn(k, scale=0.7), FadeIn(p, scale=0.7), run_time=0.8)
        self.at("bound to a protein")
        self.play(k.animate.move_to(V(-1.9, 0.8)), p.animate.move_to(V(2.0, 0.8)), run_time=1.0)
        con = T("contact", size=44, color=TEXT).move_to(V(0.1, -0.9))
        self.at("shows contact")
        self.play(FadeIn(con, shift=UP * 0.15), run_time=0.5)
        q = badge(p.get_corner(UR) + V(0.12, 0.12), "?", YELLOW)
        cat = T("contact is not catalysis", size=44, color=RED).move_to(V(0.1, -0.9))
        self.at("not catalysis")
        self.play(FadeOut(con), FadeIn(cat), FadeIn(q, scale=0.4), run_time=0.7)
        self.wait(self.beat(0.04))
        # chain
        self.at("Removing the kinase")
        kk = chip("kinase", BLUE, 36).move_to(V(-5.0, 0.2))
        xs = [-2.3, 0.2, 2.7, 5.2]
        chain = VGroup(*[chip(n, GREY, 40, pad=0.26).move_to(V(x, 0.2)) for n, x in zip("ABCD", xs)])
        ars = VGroup(arrow(kk.get_right(), chain[0].get_left()),
                     *[arrow(chain[i].get_right(), chain[i + 1].get_left()) for i in range(3)])
        ex = T("for example", size=24, color=GREY).move_to(V(0, -3.15))
        dl = T("direct substrate", size=26, color=GREY).move_to(V(-2.3, -0.95))
        dn = T("three steps\ndownstream", size=26, color=GREY, line_spacing=0.8).move_to(V(4.6, -1.1))
        self.play(FadeOut(k), FadeOut(p), FadeOut(cat), FadeOut(q), run_time=0.3)
        self.play(FadeIn(kk, scale=0.7), LaggedStart(*[FadeIn(c) for c in chain], lag_ratio=0.1),
                  LaggedStart(*[Create(a) for a in ars], lag_ratio=0.1), FadeIn(ex), FadeIn(dl), FadeIn(dn),
                  run_time=1.0)
        lst = T("inhibitor  /  RNA interference  /  knockout", size=32, color=TEXT).move_to(V(0, 2.6))
        self.at("with an inhibitor")
        self.play(FadeIn(lst, shift=DOWN * 0.15), run_time=0.5)
        cross = VGroup(*[Line(kk.get_center() + d * 0.5, kk.get_center() - d * 0.5, color=RED, stroke_width=8)
                         for d in (V(1.3, 0.8), V(1.3, -0.8))])
        self.play(Create(cross), kk.animate.set_opacity(0.4), run_time=0.6)
        self.at("changes many proteins")
        self.play(*[c.animate.set_color(TEAL) for c in chain],
                  *[a.animate.set_color(TEAL) for a in ars[1:]], run_time=0.9)
        chl = T("all changed", size=32, color=TEAL).move_to(V(0.7, 1.45))
        self.play(FadeIn(chl), run_time=0.4)
        self.at("look the same")
        same = T("look the same", size=36, color=TEAL).move_to(V(0.7, -2.1))
        self.play(Indicate(chain[0], color=TEAL), Indicate(chain[3], color=TEAL), FadeIn(same), run_time=1.0)
        self.finish()


class S03Gate(SpokenScene):
    def construct(self):
        c, s = V(0, -0.7), 1.3
        body = kinase_body(c, s)
        klab = T("kinase", size=34, color=BLUE).move_to(W(c, s, 0, -0.9))
        shok = T("Shokat laboratory", size=34, color=TEXT).move_to(V(0, 3.15))
        quote = T("organic chemistry meets protein manipulation", size=32, color=GOLD).move_to(V(0, 2.4))
        self.at("laboratory found a way")
        self.play(FadeIn(shok, shift=DOWN * 0.15), run_time=0.6)
        self.at("organic chemistry")
        self.play(FadeIn(quote, shift=DOWN * 0.1), run_time=0.7)
        self.at("share an")
        self.play(FadeOut(quote), FadeIn(body), FadeIn(klab), run_time=0.8)
        plab = T("ATP pocket", size=30, color=YELLOW).move_to(V(-2.0, 2.3))
        parr = arrow(V(-0.9, 1.95), W(c, s, -0.5, 1.0), col=YELLOW)
        self.at("pocket")
        self.play(FadeIn(plab), Create(parr), run_time=0.6)
        gate = gate_big(c, s)
        self.at("bulky residue")
        self.play(FadeIn(gate, scale=0.5), run_time=0.6)
        glab = T("gatekeeper", size=30, color=ORANGE).move_to(V(2.4, 2.3))
        garr = arrow(V(1.3, 1.95), W(c, s, 0.9, 1.0), col=ORANGE)
        self.at("the gatekeeper")
        self.play(FadeIn(glab), Create(garr), run_time=0.5)
        a = atp(c, s)
        a.shift(UP * 2.4).set_opacity(0)
        self.at("limits what fits")
        self.play(FadeOut(parr), a.animate.shift(DOWN * 2.4).set_opacity(1), run_time=1.0)
        # replace
        small = gate_small(c, s)
        hl = hole(c, s)
        glab2 = T("glycine or alanine", size=30, color=ORANGE).move_to(V(2.9, 2.3))
        self.at("Replace the gatekeeper")
        self.play(FadeOut(a, shift=UP * 0.6), run_time=0.5)
        self.at("glycine or alanine")
        self.play(Transform(gate, small), FadeIn(hl), Transform(glab, glab2), run_time=0.9)
        hole_txt = T("the pocket gains a hole", size=30, color=TEXT).move_to(V(0, -3.3))
        self.at("gains a hole")
        self.play(FadeIn(hole_txt), hl.animate.set_color(TEXT), run_time=0.7)
        self.finish()


class S04Analog(SpokenScene):
    def construct(self):
        # carried over: the enlarged kinase, rebuilt at the same place, then slid right
        c0, s0 = V(0, -0.7), 1.3
        s = 1.0
        cL, cR = V(-3.4, -0.6), V(3.4, -0.6)
        bodyR = kinase_body(c0, s0)
        gateR = gate_small(c0, s0)
        holeR = hole(c0, s0)
        self.add(bodyR, gateR, holeR)
        holeR.set_color(TEXT)
        newbody = kinase_body(cR, s)
        newgate, newhole = gate_small(cR, s), hole(cR, s)
        newhole.set_color(TEXT)
        bodyL = kinase_body(cL, s)
        gateL = gate_big(cL, s)
        labL = T("normal kinase", size=30, color=GREY).move_to(V(-3.4, -2.75))
        labR = T("enlarged pocket", size=30, color=ORANGE).move_to(V(3.4, -2.75))
        self.play(Transform(bodyR, newbody), Transform(gateR, newgate), Transform(holeR, newhole),
                  FadeIn(bodyL), FadeIn(gateL), FadeIn(labL), FadeIn(labR), run_time=0.7)
        # analog ATP above, centre
        top = V(-3.4, 2.75)
        an = atp(cR, s, bulky=True, fs=24).shift(top)
        blab = T("bulky group", size=24, color=PURPLE).next_to(an[2], RIGHT, buff=0.2)
        self.at("with a bulky group")
        self.play(FadeIn(an, shift=DOWN * 0.3), FadeIn(blab), run_time=0.8)
        self.at("fits the enlarged pocket")
        an2 = an.copy()
        self.add(an2)
        self.play(FadeOut(blab), an.animate.shift(-top), run_time=1.0)
        fit_ok = T("fits", size=32, color=GREEN).move_to(V(3.4, 1.65))
        self.play(FadeIn(fit_ok), run_time=0.3)
        # the copy comes down on a normal kinase and stops at the gatekeeper
        self.at("normal kinases poorly")
        self.play(an2.animate.shift(V(-3.4, -2.75 + 0.85 * s)), run_time=1.0)
        xmark = VGroup(*[Line(V(-3.0, 1.75) + d * 0.22, V(-3.0, 1.75) - d * 0.22, color=RED, stroke_width=8)
                         for d in (V(1, 1), V(1, -1))])
        fits_poor = T("fits poorly", size=32, color=RED).move_to(V(-3.4, 2.35))
        xmark.shift(V(0, 0))
        self.play(FadeIn(xmark), FadeIn(fits_poor), run_time=0.4)
        # name
        self.at("is called")
        asl = T("analog-sensitive", size=32, color=YELLOW).move_to(V(3.4, -2.75))
        self.play(Transform(labR, asl), FadeOut(fit_ok), run_time=0.7)
        # 1997 and v-Src
        y97 = chip("1997", GOLD, 34).move_to(V(-1.6, 3.0))
        vs = chip("tyrosine kinase v-Src", BLUE, 30).move_to(V(2.4, 3.0))
        lnk = arrow(y97.get_right(), vs.get_left(), col=GREY)
        self.at("introduced the approach")
        self.play(FadeOut(fits_poor), FadeIn(y97, scale=0.7), run_time=0.6)
        self.at("tyrosine kinase")
        self.play(Create(lnk), FadeIn(vs, shift=LEFT * 0.3), run_time=0.7)
        self.finish()


class S05End(EndCard):
    LINE = "Enlarge one kinase's pocket and give it an ATP of its own."
