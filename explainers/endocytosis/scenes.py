"""Endocytosis: the receptor makes a round trip  (Biochemistrypedia explainer)

COLOR MAP (one colour per concept, whole film)
  YELLOW = LDL, the cargo (and the cholesterol it releases)
  BLUE   = LDL receptor
  TEAL   = adaptors (AP2)
  PURPLE = clathrin coat
  PINK   = dynamin
  ORANGE = acid (the endosome lumen, pH roughly 6)
  GOLD   = Rab identity (Rab5, Rab7; the outline turns gold while a Rab is named)
  GREEN  = a step that works / a step done
  RED    = a step that fails / things that cannot happen
  GREY   = membranes, compartments, labels
  TEXT   = the chaperone
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#E86FA5"
ORANGE = "#F29E4C"
PI = np.pi


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def rect_at(p, n, w=0.2, h=0.62, color=BLUE):
    """a receptor: rounded bar centred on p, long axis along the unit normal n."""
    ang = np.arctan2(n[1], n[0]) - PI / 2
    r = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.55)
    return r.rotate(ang).move_to([p[0], p[1], 0])


def ldl_dot(p, r=0.17):
    return Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to([p[0], p[1], 0])


def lbl(text, color=GREY, size=26):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.16, height=t.height + 0.1, stroke_width=0, fill_color=BG, fill_opacity=0.85).move_to(t)
    return VGroup(back, t)


def bchip(text, color=BLUE, size=26):
    c = chip(text, color, size=size)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def membrane_h(y, x0=-6.2, x1=6.2, w=9):
    return Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=w)


class S00Title(TitleCard):
    LESSON = "Endocytosis, recycling and degradation"
    TITLE = "The receptor makes a round trip"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        MY = 0.5
        mem = membrane_h(MY)
        out_l = T("outside", 26, GREY).move_to([-5.4, MY + 0.5, 0])
        in_l = T("inside the cell", 26, GREY).move_to([-5.2, MY - 0.5, 0])
        xs = [-3.6, 0.0, 3.6]
        recs = VGroup(*[rect_at([x, MY], UP, 0.36, 1.5) for x in xs])
        ldls = VGroup(*[ldl_dot([x, MY + 1.2], 0.45) for x in xs])
        self.at("Cells from one patient")
        self.play(Create(mem), FadeIn(out_l), FadeIn(in_l), FadeIn(recs, shift=UP * 0.2), run_time=1.0)
        self.at("receptors")
        self.play(Indicate(recs, color=BLUE, scale_factor=1.12), run_time=0.7)
        self.play(FadeIn(ldls, shift=DOWN * 0.8), run_time=0.01)
        for l, x in zip(ldls, xs):
            l.move_to([x, MY + 2.4, 0])
        self.at("grip")
        self.play(*[l.animate.move_to([x, MY + 1.15, 0]) for l, x in zip(ldls, xs)], run_time=0.8)
        ldl_t = T("LDL", 26, YELLOW).next_to(ldls[1], RIGHT, buff=0.25)
        rec_t = T("receptor", 26, BLUE).next_to(recs[1], RIGHT, buff=0.3).shift(DOWN * 0.1)
        self.play(FadeIn(ldl_t), FadeIn(rec_t), run_time=0.5)
        # the crossed-out arrow: LDL does not enter
        self.at("stays outside")
        dash = DashedLine([0.95, MY + 0.9, 0], [0.95, MY - 1.7, 0], color=GREY, stroke_width=5, dash_length=0.18)
        tip = Triangle(color=GREY, fill_color=GREY, fill_opacity=1, stroke_width=0).scale(0.16).rotate(PI).move_to([0.95, MY - 1.85, 0])
        x_mark = T("×", 80, RED, weight=BOLD).move_to([0.95, MY, 0])
        self.play(Create(dash), FadeIn(tip), run_time=0.5)
        self.play(FadeIn(x_mark, scale=1.6), run_time=0.4)
        self.at("A receptor has to do more")
        self.play(FadeOut(VGroup(ldl_t, rec_t, dash, tip, x_mark)), run_time=0.5)
        # chips
        names = ["bind", "gather", "enter", "release", "return"]
        chips = VGroup(*[bchip(n, GREY, 28) for n in names]).arrange(RIGHT, buff=0.55).move_to([0, -2.9, 0])
        arrows = VGroup(*[arr(chips[i].get_right(), chips[i + 1].get_left(), GREY, 3, 0.15) for i in range(4)])
        self.at("more than bind")
        self.play(FadeIn(chips[0]), run_time=0.4)
        self.play(chips[0].animate.scale(1.12), run_time=0.25)
        self.play(chips[0].animate.scale(1 / 1.12), run_time=0.25)
        self.at("gathered into")
        self.play(FadeIn(chips[1]), GrowArrow(arrows[0]),
                  recs[0].animate.move_to([-1.1, MY, 0]), ldls[0].animate.move_to([-1.1, MY + 1.15, 0]),
                  recs[2].animate.move_to([1.1, MY, 0]), ldls[2].animate.move_to([1.1, MY + 1.15, 0]), run_time=1.1)
        self.at("carried inside")
        self.play(FadeIn(chips[2]), GrowArrow(arrows[1]), Indicate(chips[2], color=YELLOW), run_time=0.6)
        self.at("let go")
        self.play(FadeIn(chips[3]), GrowArrow(arrows[2]), Indicate(chips[3], color=YELLOW), run_time=0.6)
        self.at("come back")
        self.play(FadeIn(chips[4]), GrowArrow(arrows[3]), Indicate(chips[4], color=BLUE), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
R_V = 1.5
Y0 = 2.3


class Pit:
    """A membrane that bends into a pit, grows a neck, and pinches off a vesicle."""

    def __init__(self):
        self.C = ValueTracker(-0.9)   # bulb centre height above the neck circle (cap -> bulb)
        self.S = ValueTracker(0.0)    # neck stem length
        self.SEP = ValueTracker(0.0)  # how far the free vesicle has moved down
        self.AD = ValueTracker(0.0)   # adaptor opacity
        self.COAT = ValueTracker(0.0)  # how much of the arc the coat covers
        self.DYN = ValueTracker(0.0)  # dynamin opacity
        self.TAIL = ValueTracker(0.0)

    def geom(self):
        c = self.C.get_value()
        n = float(np.sqrt(max(R_V ** 2 - c ** 2, 1e-4)))
        s, sep = self.S.get_value(), self.SEP.get_value()
        cen = np.array([0, Y0 - s - c - sep, 0])
        pl = np.arctan2(c, -n) % (2 * PI)
        pr = np.arctan2(c, n) % (2 * PI)
        if pr <= pl:
            pr += 2 * PI
        return n, s, sep, cen, pl, pr

    def pt(self, f, off=0.0):
        n, s, sep, cen, pl, pr = self.geom()
        phi = pl + f * (pr - pl)
        d = np.array([np.cos(phi), np.sin(phi), 0])
        return cen + (R_V + off) * d, d

    def membrane(self):
        n, s, sep, cen, pl, pr = self.geom()
        g = VGroup()
        if sep > 0.01:
            g.add(membrane_h(Y0))
            ph = np.linspace(pl, pl + 2 * PI, 90)
        else:
            g.add(membrane_h(Y0, -6.2, -n), membrane_h(Y0, n, 6.2))
            if s > 0.02:
                g.add(Line([-n, Y0, 0], [-n, Y0 - s, 0], color=GREY, stroke_width=9),
                      Line([n, Y0, 0], [n, Y0 - s, 0], color=GREY, stroke_width=9))
            ph = np.linspace(pl, pr, 90)
        pts = [cen + R_V * np.array([np.cos(p), np.sin(p), 0]) for p in ph]
        arc = VMobject(color=GREY, stroke_width=9, fill_opacity=0)
        arc.set_points_as_corners(pts)
        g.add(arc)
        return g

    def receptors(self, fs):
        return [always_redraw(lambda f=f: rect_at(self.pt(f)[0], self.pt(f)[1])) for f in fs]

    def ldls(self, fs):
        return [always_redraw(lambda f=f: ldl_dot(self.pt(f, -0.52)[0])) for f in fs]

    def adaptors(self, fs):
        def mk(f):
            a = self.AD.get_value()
            p, d = self.pt(f, 0.5 + (1 - a) * 0.9)
            m = rect_at(p, d, 0.42, 0.24, TEAL)
            m.set_opacity(a)
            m.set_stroke(opacity=a)
            return m
        return [always_redraw(lambda f=f: mk(f)) for f in fs]

    def tails(self, fs):
        def mk(f):
            p, d = self.pt(f, 0.5)
            q, _ = self.pt(f, 0.36)
            a = self.AD.get_value()
            return Line(q, p, color=BLUE, stroke_width=3, stroke_opacity=a)
        return [always_redraw(lambda f=f: mk(f)) for f in fs]

    def coat(self):
        def mk():
            e = self.COAT.get_value()
            if e < 0.02:
                return VGroup()
            lo, hi = 0.5 - 0.46 * e, 0.5 + 0.46 * e
            fs = np.linspace(lo, hi, max(3, int(24 * e)))
            pts = [self.pt(f, 0.98)[0] for f in fs]
            line = VMobject(color=PURPLE, stroke_width=5, fill_opacity=0)
            line.set_points_as_corners(pts)
            beads = VGroup(*[Dot(p, radius=0.07, color=PURPLE) for p in pts[::2]])
            return VGroup(line, beads)
        return always_redraw(mk)

    def rungs(self, fs):
        def mk(f):
            e = self.COAT.get_value()
            if not (0.5 - 0.46 * e <= f <= 0.5 + 0.46 * e) or e < 0.02:
                return VGroup()
            return Line(self.pt(f, 0.64)[0], self.pt(f, 0.94)[0], color=PURPLE, stroke_width=3)
        return [always_redraw(lambda f=f: mk(f)) for f in fs]

    def dynamin(self):
        def mk():
            a = self.DYN.get_value()
            if a < 0.02:
                return VGroup()
            n, s, sep, cen, pl, pr = self.geom()
            g = VGroup()
            for k in (0.18, 0.5, 0.82):
                for sx in (-1, 1):
                    b = RoundedRectangle(corner_radius=0.06, width=0.32, height=0.15, stroke_color=PINK, stroke_width=3,
                                         fill_color=PINK, fill_opacity=0.8 * a).move_to([sx * (n + 0.22), Y0 - s * k - sep * 0, 0])
                    b.set_stroke(opacity=a)
                    g.add(b)
            return g
        return always_redraw(mk)


class S02Coat(SpokenScene):
    def construct(self):
        P = Pit()
        P.C.set_value(-0.55)
        fs = [0.2, 0.4, 0.6, 0.8]
        mem = always_redraw(P.membrane)
        recs = P.receptors(fs)
        ldls = P.ldls(fs)
        tails = P.tails(fs)
        ads = P.adaptors(fs)
        coat = P.coat()
        rungs = P.rungs(fs)
        dyn = P.dynamin()
        out_l = T("outside", 26, GREY).move_to([-5.5, Y0 + 0.6, 0])
        cyt_l = T("cytosol", 26, GREY).move_to([-5.5, Y0 - 0.6, 0])
        self.add(mem, *recs, *ldls, out_l, cyt_l)
        self.add(*tails, *ads, coat, *rungs, dyn)
        self.wait(0.2)

        # clathrin cannot touch membrane or cargo
        self.at("Clathrin builds the coat")
        clat = bchip("clathrin", PURPLE, 28).move_to([0, -0.6, 0])
        self.play(FadeIn(clat, shift=UP * 0.3), run_time=0.6)
        self.at("binds neither membrane nor cargo")
        d1 = DashedLine(clat.get_top() + LEFT * 0.4, [-0.6, Y0 - 1.0, 0], color=GREY, stroke_width=4, dash_length=0.15)
        d2 = DashedLine(clat.get_top() + RIGHT * 0.4, [0.6, Y0 - 1.0, 0], color=GREY, stroke_width=4, dash_length=0.15)
        x1 = T("×", 56, RED, weight=BOLD).move_to(d1.get_center() + LEFT * 0.0)
        x2 = T("×", 56, RED, weight=BOLD).move_to(d2.get_center())
        self.play(Create(d1), Create(d2), run_time=0.5)
        self.play(FadeIn(x1, scale=1.5), FadeIn(x2, scale=1.5), run_time=0.4)
        # adaptors bridge
        self.at("Adapters do that")
        self.play(FadeOut(VGroup(d1, d2, x1, x2)), run_time=0.3)
        self.at("An adapter called")
        self.play(P.AD.animate.set_value(1.0), run_time=0.9)
        ad_l = bchip("AP2 adaptor", TEAL, 26).move_to([-4.3, 0.5, 0])
        ad_ld = always_redraw(lambda: Line(ad_l.get_right(), P.pt(0.2, 0.55)[0] + [-0.2, 0, 0], color=TEAL, stroke_width=2.5))
        self.play(FadeIn(ad_l), FadeIn(ad_ld), run_time=0.5)
        self.at("inner leaflet")
        self.play(Indicate(ad_l, color=TEAL), run_time=0.6)
        self.at("sorting motifs")
        self.play(*[Indicate(t, color=BLUE, scale_factor=1.4) for t in tails], run_time=0.8)
        # clathrin joins
        self.at("recruit clathrin")
        self.play(ReplacementTransform(clat, clat.copy().scale(0.01).move_to(P.pt(0.5, 0.98)[0])), run_time=0.4)
        self.play(P.COAT.animate.set_value(0.55), run_time=1.1)
        cl_l = bchip("clathrin", PURPLE, 26).move_to([4.6, 0.6, 0])
        cl_ld = always_redraw(lambda: Line(cl_l.get_left(), P.pt(0.75, 0.98)[0], color=PURPLE, stroke_width=2.5))
        self.play(FadeIn(cl_l), FadeIn(cl_ld), run_time=0.4)
        self.at("The lattice grows")
        self.play(P.COAT.animate.set_value(1.0), run_time=0.8)
        self.at("curves into a pit")
        self.play(P.C.animate.set_value(1.2), P.S.animate.set_value(0.3), run_time=1.6)
        self.play(P.C.animate.set_value(1.32), P.S.animate.set_value(0.95), run_time=1.0)
        # dynamin
        self.at("Dynamin forms a collar")
        dy_l = bchip("dynamin", PINK, 26).move_to([4.5, 1.5, 0])
        dy_ld = always_redraw(lambda: Line(dy_l.get_left(), [P.geom()[0] + 0.45, Y0 - 0.5 * P.S.get_value(), 0], color=PINK, stroke_width=2.5))
        self.play(P.DYN.animate.set_value(1.0), FadeIn(dy_l), FadeIn(dy_ld), run_time=0.8)
        self.at("drives the membrane")
        self.play(P.C.animate.set_value(1.46), run_time=0.9)
        self.at("to split")
        self.play(P.SEP.animate.set_value(0.6), P.DYN.animate.set_value(0.0), FadeOut(dy_l), FadeOut(dy_ld), run_time=1.0)
        self.at("A chaperone")
        ch_l = bchip("chaperone", TEXT, 26).move_to([4.6, -2.3, 0])
        ch_ld = always_redraw(lambda: Line(ch_l.get_left(), P.pt(0.62, 0.98)[0], color=TEXT, stroke_width=2.5))
        self.play(FadeIn(ch_l), FadeIn(ch_ld), FadeOut(cl_l), FadeOut(cl_ld), run_time=0.5)
        self.at("pulls the lattice")
        self.play(P.COAT.animate.set_value(0.0), P.AD.animate.set_value(0.0), FadeOut(ad_l), FadeOut(ad_ld), run_time=1.4)
        self.play(FadeOut(ch_l), FadeOut(ch_ld), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
EC = np.array([-1.0, 0.1, 0])
EA, EB = 3.4, 2.3


def ell_pt(t_deg, off=0.0):
    t = np.radians(t_deg)
    p = EC + np.array([EA * np.cos(t), EB * np.sin(t), 0])
    n = np.array([np.cos(t) / EA, np.sin(t) / EB, 0])
    n = n / np.linalg.norm(n)
    return p + n * off, n


def make_endo(tint=0.0, color=GREY):
    return Ellipse(width=2 * EA, height=2 * EB, stroke_color=color, stroke_width=8,
                   fill_color=ORANGE, fill_opacity=tint).move_to(EC)


REC_T = [-150, -105, -45, 45, 105, 150]


class S03Acid(SpokenScene):
    def construct(self):
        vc = np.array([5.0, 0.1, 0])
        vr = 1.0
        ves = Circle(radius=vr, stroke_color=GREY, stroke_width=8).move_to(vc)
        vts = [0, 60, 120, 180, 240, 300]
        v_rec, v_ldl = [], []
        for t in vts:
            d = np.array([np.cos(np.radians(t)), np.sin(np.radians(t)), 0])
            v_rec.append(rect_at(vc + d * vr, d))
            v_ldl.append(ldl_dot(vc + d * (vr - 0.5)))
        v_lbl = T("vesicle", 26, GREY).move_to(vc + DOWN * 1.55)
        self.play(FadeIn(ves), *[FadeIn(r) for r in v_rec], *[FadeIn(l) for l in v_ldl], FadeIn(v_lbl), run_time=0.8)
        self.at("fuses with an early endosome")
        endo = make_endo()
        e_lbl = T("early endosome", 28, GREY).move_to([EC[0], EC[1] + EB + 0.75, 0])
        self.play(FadeIn(endo), FadeIn(e_lbl), FadeOut(v_lbl), run_time=0.7)
        vgrp = VGroup(ves, *v_rec, *v_ldl)
        self.play(vgrp.animate.shift(LEFT * 1.4), run_time=0.7)
        e_rec, e_ldl = [], []
        for t in REC_T:
            p, n = ell_pt(t)
            e_rec.append(rect_at(p, n))
            e_ldl.append(ldl_dot(p - n * 0.52))
        self.play(FadeOut(ves), *[ReplacementTransform(a, b) for a, b in zip(v_rec, e_rec)],
                  *[ReplacementTransform(a, b) for a, b in zip(v_ldl, e_ldl)], run_time=1.0)
        self.at("mildly acid")
        ph = T("lumen: roughly pH 6", 30, ORANGE).move_to([EC[0], EC[1] - EB - 0.75, 0])
        self.play(endo.animate.set_fill(ORANGE, 0.14), FadeIn(ph, shift=UP * 0.15), run_time=0.9)
        self.at("acid is the sorting signal")
        self.play(Indicate(ph, color=ORANGE, scale_factor=1.12), run_time=0.8)
        self.at("comes off its receptor")
        tgt = []
        for i, l in enumerate(e_ldl):
            c = l.get_center()
            tgt.append(c + (EC - c) * 0.42)
        self.play(*[l.animate.move_to(p) for l, p in zip(e_ldl, tgt)], run_time=1.3)
        self.at("Receptor and cargo")
        rl = bchip("receptor", BLUE, 26).move_to([-5.3, -1.9, 0])
        rld = Line(rl.get_top(), e_rec[0].get_center() + DOWN * 0.1 + LEFT * 0.0, color=BLUE, stroke_width=2.5)
        ll = bchip("LDL", YELLOW, 26).move_to([EC[0], EC[1] + 0.0, 0])
        self.play(FadeIn(rl), Create(rld), FadeIn(ll), run_time=0.7)
        self.finish()


class S04Return(SpokenScene):
    def construct(self):
        endo = make_endo(0.14)
        e_lbl = T("early endosome", 28, GREY).move_to([EC[0], EC[1] + EB + 0.75, 0])
        ph = T("lumen: roughly pH 6", 30, ORANGE).move_to([EC[0], EC[1] - EB - 0.75, 0])
        recs = []
        for t in REC_T:
            p, n = ell_pt(t)
            recs.append(rect_at(p, n))
        lpos = []
        for i in range(6):
            a = np.radians(60 * i + 20)
            lpos.append(EC + np.array([0.75 * np.cos(a), 0.55 * np.sin(a), 0]))
        ldls = [ldl_dot(p) for p in lpos]
        self.add(endo, e_lbl, ph, *recs, *ldls)
        self.wait(0.3)
        self.at("Empty receptors collect")
        # gather receptors to the right side, then a tubule grows from there
        gt = [-48, -32, -16, 16, 32, 48]
        moves = []
        for r, t in zip(recs, gt):
            p, n = ell_pt(t)
            moves.append(r.animate.become(rect_at(p, n)))
        self.play(*moves, run_time=1.2)
        tube = RoundedRectangle(corner_radius=0.2, width=2.4, height=0.5, stroke_color=GREY, stroke_width=6,
                                fill_color=BG, fill_opacity=1).move_to([EC[0] + EA + 0.9, EC[1], 0])
        self.play(GrowFromEdge(tube, LEFT), run_time=0.6)
        marks = []
        for k, r in enumerate(recs):
            m = rect_at([EC[0] + EA + 0.35 + 0.38 * k, EC[1]], UP, 0.12, 0.3)
            marks.append(m)
        self.play(*[ReplacementTransform(r, m) for r, m in zip(recs, marks)], run_time=0.9)
        tv = VGroup(tube, *marks)
        self.at("pinch off")
        self.play(tv.animate.shift(RIGHT * 0.6), run_time=0.6)
        self.at("plasma membrane")
        pm = Line([6.0, -2.9, 0], [6.0, 2.8, 0], color=GREY, stroke_width=9)
        pm_l = T("plasma membrane", 24, GREY).move_to([4.9, 3.25, 0])
        self.play(Create(pm), FadeIn(pm_l), run_time=0.7)
        self.play(tv.animate.shift(RIGHT * 0.75), run_time=1.0)
        pm_r = [rect_at([6.0, 0.1 + 0.55 * (k - 2.5)], RIGHT, 0.2, 0.62) for k in range(6)]
        self.play(FadeOut(tube), *[ReplacementTransform(m, r) for m, r in zip(marks, pm_r)], run_time=0.8)
        # LDL stays in the lumen
        self.at("stays in the lumen")
        self.play(*[Indicate(l, color=YELLOW, scale_factor=1.5) for l in ldls], run_time=0.9)
        # Rab conversion
        self.at("In human A431 cells")
        rab = bchip("Rab5", GOLD, 28).move_to([-4.6, 2.5, 0])
        self.play(FadeIn(rab), endo.animate.set_stroke(GOLD), run_time=0.7)
        self.at("replaced by")
        rab7 = bchip("Rab7", GOLD, 28).move_to(rab)
        self.play(ReplacementTransform(rab, rab7), run_time=0.8)
        self.at("the compartment maturing")
        late = T("late endosome", 28, GREY).move_to(e_lbl)
        self.play(ReplacementTransform(e_lbl, late), FadeOut(ph), run_time=0.8)
        # to the lysosome
        self.at("goes on to the lysosome")
        lys = Circle(radius=1.35, stroke_color=GREY, stroke_width=8).move_to([4.1, -0.1, 0])
        lys_l = T("lysosome", 26, GREY).move_to([4.1, -1.9, 0])
        self.play(FadeOut(VGroup(pm_l, pm, *pm_r, rab7, late, endo, *ldls)), FadeIn(lys), FadeIn(lys_l), run_time=0.8)
        ldls = [ldl_dot([4.1 + 0.55 * np.cos(np.radians(60 * i + 20)), -0.1 + 0.4 * np.sin(np.radians(60 * i + 20)), 0]) for i in range(6)]
        self.play(*[FadeIn(l, scale=0.6) for l in ldls], run_time=0.8)
        self.at("enzymes digest it")
        en = T("enzymes", 26, TEXT).move_to([4.1, 1.9, 0])
        self.play(FadeIn(en, shift=DOWN * 0.15), run_time=0.5)
        self.play(*[l.animate.scale(0.3).set_opacity(0) for l in ldls], run_time=0.8)
        self.at("release cholesterol")
        ch = T("cholesterol", 26, YELLOW).move_to([4.1, -0.1, 0])
        self.play(FadeIn(ch, scale=0.7), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Numbers(SpokenScene):
    def construct(self):
        base, sc = -2.0, 0.1  # y of zero, units per value
        xs = [-3.6, 0.2, 4.0]
        names = ["Normal", "Strain X", "Strain Y"]
        axis = Line([-5.6, base, 0], [-5.6, base + 40 * sc, 0], color=GREY, stroke_width=3)
        ticks = VGroup(*[VGroup(Line([-5.7, base + v * sc, 0], [-5.5, base + v * sc, 0], color=GREY, stroke_width=3),
                                M(str(v), 22, GREY).move_to([-6.1, base + v * sc, 0])) for v in (0, 10, 20, 30, 40)])
        floor = Line([-5.6, base, 0], [6.0, base, 0], color=GREY, stroke_width=3)
        ytitle = T("ng LDL per mg cell protein", 22, GREY).rotate(PI / 2).move_to([-6.7, base + 20 * sc, 0])
        nm = VGroup(*[T(n, 28, TEXT).move_to([x, base - 0.4, 0]) for n, x in zip(names, xs)])
        self.play(FadeIn(VGroup(axis, ticks, floor)), FadeIn(ytitle), FadeIn(nm), run_time=0.9)
        self.at("made up for practice")
        pr = T("made-up practice numbers", 24, GREY).move_to([0.2, 3.35, 0])
        self.play(FadeIn(pr), run_time=0.4)

        def bar(x, v0, v1, color, solid):
            h = (v1 - v0) * sc
            r = Rectangle(width=1.5, height=max(h, 0.02), stroke_color=color, stroke_width=3,
                          fill_color=color, fill_opacity=0.85 if solid else 0.0)
            r.move_to([x, base + v0 * sc + h / 2, 0])
            return r
        bound = [40, 1.0, 38]
        self.at("bind labeled")
        bars = [bar(x, 0, v, YELLOW, False) for x, v in zip(xs, bound)]
        leg = T("bound at 4 °C", 24, YELLOW).move_to([0.2, 2.75, 0])
        vals = [M(str(v), 24, YELLOW).next_to(b, UP, buff=0.12) for b, v in zip(bars, ["40", "1.0", "38"])]
        self.play(*[GrowFromEdge(b, DOWN) for b in bars], FadeIn(leg), run_time=1.0)
        self.play(*[FadeIn(v) for v in vals], run_time=0.4)
        self.at("warm up")
        # normal: 10 surface + 30 internal ; strain Y: 35 surface + 3 internal
        n_int = bar(xs[0], 0, 30, YELLOW, True)
        y_int = bar(xs[2], 0, 3, YELLOW, True)
        leg2 = T("solid: inside after warming", 24, YELLOW).move_to([0.2, 2.75, 0])
        self.play(FadeIn(n_int), FadeIn(y_int), ReplacementTransform(leg, leg2), run_time=1.0)
        i30 = M("30", 24, YELLOW).move_to([xs[0], base + 15 * sc, 0]); i30.set_color(BG)
        i3 = M("3", 24, YELLOW).next_to(y_int, RIGHT, buff=0.12)
        self.play(FadeIn(i30), FadeIn(i3), run_time=0.5)
        self.at("Normal cells bound")
        self.play(Indicate(vals[0], color=YELLOW, scale_factor=1.4), run_time=0.6)
        self.at("that is 75")
        p75 = bchip("30 / 40 = 75%", GREEN, 26).move_to([-3.6, 3.0, 0])
        self.play(FadeIn(p75), run_time=0.6)
        self.at("Strain X bound only")
        self.play(Indicate(bars[1], color=YELLOW, scale_factor=1.4), run_time=0.9)
        self.at("which is 2")
        x25 = bchip("1.0 / 40 = 2.5%", RED, 24).move_to([0.2, 0.9, 0])
        self.play(FadeIn(x25), run_time=0.5)
        self.at("binding defect")
        bd = bchip("binding defect", RED, 26).move_to([0.2, -3.05, 0])
        self.play(FadeIn(bd), run_time=0.5)
        self.at("Strain Y bound")
        self.play(Indicate(vals[2], color=YELLOW, scale_factor=1.4), run_time=0.6)
        self.at("that is 7")
        p79 = bchip("3 / 38 = 7.9%", RED, 26).move_to([4.0, 3.0, 0])
        self.play(FadeIn(p79), FadeOut(leg2), run_time=0.6)
        self.at("entry defect")
        ed = bchip("entry defect", RED, 26).move_to([4.0, -3.05, 0])
        self.play(FadeIn(ed), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Trip(SpokenScene):
    def construct(self):
        pos = {"bind": np.array([-4.3, 0.0, 0]), "enter": np.array([0.0, 2.4, 0]),
               "release": np.array([4.3, 0.0, 0]), "return": np.array([0.0, -2.4, 0])}
        place = {"bind": "cell surface", "enter": "coated vesicle", "release": "acid endosome", "return": "recycling tubule"}
        chips = {k: bchip(k, GREY, 30).move_to(p) for k, p in pos.items()}
        places = {k: T(place[k], 22, GREY) for k in pos}
        places["bind"].next_to(chips["bind"], DOWN, buff=0.25)
        places["enter"].next_to(chips["enter"], UP, buff=0.2)
        places["release"].next_to(chips["release"], DOWN, buff=0.25)
        places["return"].next_to(chips["return"], DOWN, buff=0.2)
        order = ["bind", "enter", "release", "return"]
        arrs = VGroup(arr(chips["bind"].get_corner(UR) + [0.1, 0.0, 0], chips["enter"].get_left() + [-0.1, -0.1, 0], GREY, 4),
                      arr(chips["enter"].get_right() + [0.1, -0.1, 0], chips["release"].get_corner(UL) + [-0.1, 0.0, 0], GREY, 4),
                      arr(chips["release"].get_corner(DL) + [-0.1, -0.0, 0], chips["return"].get_right() + [0.1, 0.1, 0], GREY, 4),
                      arr(chips["return"].get_left() + [-0.1, 0.1, 0], chips["bind"].get_corner(DR) + [0.1, -0.0, 0], GREY, 4))

        def good(k):
            c = chips[k]
            return [c[1].animate.set_stroke(GREEN).set_fill(GREEN, 0.16), c[2].animate.set_color(GREEN)]

        def paint(k, col, fo=0.16):
            c = chips[k]
            return [c[1].animate.set_stroke(col).set_fill(col, fo), c[2].animate.set_color(col)]

        self.at("round trip")
        self.play(*[FadeIn(c) for c in chips.values()], *[FadeIn(p) for p in places.values()],
                  *[GrowArrow(a) for a in arrs], run_time=1.4)
        rec = rect_at(pos["bind"] + [0, 1.1, 0], UP, 0.3, 0.9)
        ldl = ldl_dot(pos["bind"] + [0, 1.1 + 0.68, 0], 0.26)
        self.at("binds at the surface")
        self.play(FadeIn(rec), FadeIn(ldl), *good("bind"), run_time=0.8)
        self.at("enters in a")
        tp = pos["enter"] + [0, -1.15, 0]
        self.play(rec.animate.move_to(tp), ldl.animate.move_to(tp + [0, 0.68, 0]), *good("enter"), run_time=1.2)
        self.at("lets go of")
        rp = pos["release"] + [0, 1.1, 0]
        self.play(rec.animate.move_to(rp), ldl.animate.move_to(rp + [0, 0.68, 0]), *good("release"), run_time=1.0)
        lys = Circle(radius=0.6, stroke_color=GREY, stroke_width=6).move_to([5.7, 2.0, 0])
        lys_l = T("lysosome", 22, GREY).next_to(lys, UP, buff=0.12)
        self.play(FadeIn(lys), FadeIn(lys_l), run_time=0.4)
        self.play(ldl.animate.move_to(lys.get_center()), run_time=0.8)
        self.at("and returns")
        bp = pos["return"] + [0, 1.15, 0]
        self.play(rec.animate.move_to(bp), *good("return"), run_time=1.0)
        self.play(rec.animate.move_to(pos["bind"] + [0, 1.1, 0]), run_time=1.0)
        self.at("travels one way")
        self.play(Indicate(lys, color=YELLOW, scale_factor=1.2), run_time=0.8)
        self.at("break different steps")
        self.play(*[x for k in order for x in paint(k, GREY, 0.0)], run_time=0.4)
        for k in order:
            self.play(*paint(k, RED), run_time=0.3)
            self.play(*paint(k, GREY, 0.0), run_time=0.25)
        self.at("Keep this rule")
        self.play(*[x for k in order for x in good(k)], run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "A receptor must bind, enter, release, and return."
