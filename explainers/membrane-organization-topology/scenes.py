"""Membrane organization and topology: a membrane's faces never swap  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  GREY   = membranes (walls, bilayer bars) and neutral labels; the cytosol side has no tint
  TEAL   = lumen / outside of the cell (the exoplasmic side), tinted
  BLUE   = the membrane-spanning segment of the protein
  YELLOW = the N terminus (and its N-terminal domain)
  GREEN  = the C terminus
  ORANGE = the sugar (glycan)
  PURPLE = a lipid
  RED    = blocked / not allowed (a crossing that does not happen)
Rule of the drawing: in every picture the N end of the protein points to the teal side.
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
LUM = TEAL
R = 1.5          # vesicle radius
PS = 1.0         # protein scale inside vesicles
WALL_W = 7
HW = R * math.sin(math.radians(20))      # half width of the fusion gap
DOCK = R * math.cos(math.radians(20))    # centre sits this far below the wall when docked


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def P(x, y):
    return np.array([x, y, 0.0])


def corners(pts, color=GREY, w=WALL_W):
    m = VMobject()
    m.set_points_as_corners([P(*p) for p in pts])
    m.set_stroke(color, w)
    m.set_fill(opacity=0)
    return m


class Comp:
    """A compartment (or the outside of the cell) lying above a wall at y=yb. Lumen is teal."""

    def __init__(self, x0, x1, yb, yt, gx, boxed=True):
        self.gx, self.yb = gx, yb
        self.fill = Rectangle(width=x1 - x0, height=yt - yb, stroke_width=0, fill_color=LUM,
                              fill_opacity=0.16).move_to(P((x0 + x1) / 2, (yb + yt) / 2))
        if boxed:
            self.outline = corners([(gx - HW, yb), (x0, yb), (x0, yt), (x1, yt), (x1, yb), (gx + HW, yb)])
        else:
            self.outline = VGroup(corners([(x0, yb), (gx - HW, yb)]), corners([(gx + HW, yb), (x1, yb)]))
        self.cap = corners([(gx - HW, yb), (gx + HW, yb)])
        self.base = VGroup(self.fill, self.outline, self.cap)


def protein(c, s=1.0, sugar=True):
    """N end up (toward the teal side), C end down. c is where the spanning bar crosses the wall."""
    c = np.array(c, float)
    fs = max(22, int(26 * s))
    bar = Line(c + DOWN * 0.75 * s, c + UP * 0.7 * s, color=BLUE, stroke_width=14 * s)
    ccap = Circle(radius=0.27 * s, stroke_width=0, fill_color=GREEN, fill_opacity=1).move_to(c + DOWN * 0.95 * s)
    ctxt = T("C", fs, BG, weight=BOLD).move_to(ccap)
    nbl = Circle(radius=0.33 * s, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to(c + UP * 0.95 * s)
    ntxt = T("N", fs, BG, weight=BOLD).move_to(nbl)
    g = VGroup(bar, ccap, ctxt, nbl, ntxt)
    g.bar, g.C, g.N = bar, VGroup(ccap, ctxt), VGroup(nbl, ntxt)
    if sugar:
        o = nbl.get_center()
        stem = Line(o + np.array([0.2 * s, 0.26 * s, 0]), o + np.array([0.55 * s, 0.62 * s, 0]), color=ORANGE, stroke_width=5)
        sq = Square(side_length=0.3 * s, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to(o + np.array([0.7 * s, 0.77 * s, 0]))
        g.S = VGroup(stem, sq)
        g.add(stem, sq)
    return g


def vesicle(cx, cy, s=PS):
    c = P(cx, cy)
    v = VGroup()
    v.fill = Circle(radius=R, stroke_width=0, fill_color=LUM, fill_opacity=0.16).move_to(c)
    v.bot = Arc(radius=R, start_angle=110 * DEGREES, angle=320 * DEGREES, arc_center=c, color=GREY, stroke_width=WALL_W)
    v.top = Arc(radius=R, start_angle=70 * DEGREES, angle=40 * DEGREES, arc_center=c, color=GREY, stroke_width=WALL_W)
    v.prot = protein(P(cx, cy - R), s)
    v.add(v.fill, v.bot, v.top, v.prot)
    return v


def key_item(text, color, pos, size=24):
    dot = Circle(radius=0.12, stroke_width=0, fill_color=color, fill_opacity=1)
    lab = T(text, size, color)
    g = VGroup(dot, lab).arrange(RIGHT, buff=0.15)
    g.move_to(pos)
    g.shift(RIGHT * (pos[0] - g.get_left()[0]))   # pos[0] is the LEFT edge
    return g


def cross(center, size=0.3, color=RED):
    c = np.array(center, float)
    return VGroup(Line(c + P(-size, -size), c + P(size, size), color=color, stroke_width=8),
                  Line(c + P(-size, size), c + P(size, -size), color=color, stroke_width=8))


def pulse(m, color=None, s=1.25):
    if color:
        return Indicate(m, scale_factor=s, color=color)
    start = m.copy()
    return UpdateFromAlphaFunc(m, lambda mob, a: mob.become(start.copy().scale(1 + (s - 1) * math.sin(math.pi * a))))


YB, YT = 1.6, 3.6
CY0 = -0.5                   # vesicle centre while it travels
DOWN_TRAVEL = (YB - DOCK) - CY0   # from docked to travelling


class S00Title(TitleCard):
    LESSON = "Membrane organization and topology"
    TITLE = "A membrane's faces never swap"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        yb, yt = 0.0, 3.3
        er = Comp(-6.2, -0.7, yb, yt, -3.45)
        er_l = T("ER lumen", 24, TEAL).move_to(P(-5.0, 2.9))
        p = protein(P(-3.45, yb), 1.4)
        self.at("A sugar is added")
        self.play(FadeIn(er.base), FadeIn(er_l), run_time=0.6)
        self.play(FadeIn(p.bar), FadeIn(p.C), FadeIn(p.N), run_time=0.5)
        self.play(FadeIn(p.S, shift=DOWN * 0.15), run_time=0.5)
        self.play(pulse(p.S, ORANGE, 1.4), run_time=0.6)
        self.at("cultured mammalian cell")
        cm = T("cultured mammalian cell", 24, GREY).move_to(P(0, -3.1))
        self.play(FadeIn(cm), run_time=0.5)

        self.at("Later")
        pm = Comp(0.7, 6.3, yb, yt, 3.45, boxed=False)
        out_l = T("outside the cell", 24, TEAL).move_to(P(4.6, 1.2))
        pm_l = T("plasma membrane", 22, GREY).move_to(P(4.9, -0.45))
        self.play(FadeIn(pm.base), FadeIn(out_l), FadeIn(pm_l), run_time=0.7)
        self.at("sits on the outside")
        osq = Square(side_length=0.4, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to(P(3.0, 2.4))
        olab = T("sugar", 26, ORANGE).move_to(P(4.0, 2.4))
        self.play(FadeIn(osq, scale=0.5), FadeIn(olab), run_time=0.6)
        d1 = DashedLine(P(-2.2, 2.55), P(-0.35, 2.45), color=GREY, stroke_width=4)
        d2 = DashedLine(P(0.85, 2.42), P(2.7, 2.4), color=GREY, stroke_width=4)
        q = chip("?", TEXT, size=34).move_to(P(0.25, 2.45))
        self.play(Create(d1), run_time=0.5)
        self.play(FadeIn(q, scale=0.6), Create(d2), run_time=0.5)

        self.at("never crossed a membrane")
        x = cross(P(-0.7, 2.5), 0.3)
        self.play(GrowFromCenter(x), run_time=0.45)
        self.at("how does a sugar")
        self.play(pulse(q, TEXT, 1.3), run_time=0.8)

        self.at("The answer is one rule")
        bars = VGroup(
            RoundedRectangle(corner_radius=0.1, width=0.36, height=6.4, stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.35).move_to(P(-0.2, 0)),
            RoundedRectangle(corner_radius=0.1, width=0.36, height=6.4, stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.35).move_to(P(0.2, 0)))
        everything = VGroup(er.base, er_l, p, cm, pm.base, out_l, pm_l, osq, olab, d1, d2, q, x)
        self.play(FadeOut(everything), run_time=0.6)
        self.play(GrowFromCenter(bars), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Faces(SpokenScene):
    def construct(self):
        left = RoundedRectangle(corner_radius=0.1, width=0.36, height=6.4, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.35).move_to(P(-0.2, 0))
        right = left.copy().move_to(P(0.2, 0))
        self.add(left, right)

        self.at("two sheets of lipid")
        self.play(pulse(left, None, 1.06), run_time=0.5)
        self.play(pulse(right, None, 1.06), run_time=0.5)
        self.at("called a leaflet")
        ll = T("leaflet", 26, GREY).move_to(P(-1.8, 2.7))
        lr = T("leaflet", 26, GREY).move_to(P(1.8, 2.7))
        ln1 = Line(P(-1.15, 2.7), P(-0.5, 2.7), color=GREY, stroke_width=3)
        ln2 = Line(P(1.15, 2.7), P(0.5, 2.7), color=GREY, stroke_width=3)
        self.play(FadeIn(ll), FadeIn(lr), Create(ln1), Create(ln2), run_time=0.7)

        self.at("two faces")
        fl = T("face", 26, TEXT).move_to(P(-1.8, 2.7))
        fr = T("face", 26, TEXT).move_to(P(1.8, 2.7))
        self.play(FadeOut(ll), FadeOut(lr), run_time=0.3)
        self.play(FadeIn(fl), FadeIn(fr), run_time=0.4)

        self.at("One face looks at the cytosol")
        cyt = chip("cytosol", GREY, size=26).move_to(P(-3.6, 1.8))
        a1 = Arrow(P(-2.55, 1.8), P(-0.6, 1.8), buff=0, color=GREY, stroke_width=5, tip_length=0.22)
        self.play(FadeIn(cyt), GrowArrow(a1), run_time=0.7)
        self.at("the fluid that fills")
        rng = np.random.RandomState(3)
        dots = VGroup(*[Circle(radius=0.07, stroke_width=0, fill_color=GREY, fill_opacity=0.7).move_to(
            P(rng.uniform(-6.0, -1.2), rng.uniform(-3.0, 0.9))) for _ in range(26)])
        self.play(FadeIn(dots, lag_ratio=0.05), run_time=1.2)
        self.play(*[d.animate.shift(P(rng.uniform(-0.4, 0.4), rng.uniform(-0.4, 0.4))) for d in dots], run_time=2.0)

        self.at("The other faces")
        tint = Rectangle(width=5.95, height=7.0, stroke_width=0, fill_color=LUM, fill_opacity=0.14).move_to(P(3.375, 0))
        outc = chip("outside the cell", TEAL, size=26).move_to(P(3.6, 1.8))
        orr = T("or", 24, GREY).move_to(P(3.6, 0.95))
        lum = chip("lumen (ER)", TEAL, size=26).move_to(P(3.6, 0.1))
        a2 = Arrow(P(2.2, 1.8), P(0.6, 1.8), buff=0, color=TEAL, stroke_width=5, tip_length=0.22)
        self.play(FadeIn(tint), FadeIn(outc), FadeIn(a2), run_time=0.7)
        self.play(FadeIn(orr), FadeIn(lum), run_time=0.5)

        self.at("slide sideways")
        self.play(FadeOut(dots), run_time=0.4)
        dot = Circle(radius=0.2, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to(P(0.2, -1.6))
        prot = RoundedRectangle(corner_radius=0.12, width=1.2, height=0.3, stroke_color=BLUE, stroke_width=3,
                                fill_color=BLUE, fill_opacity=0.9).move_to(P(0, 0.6))
        dl = T("lipid", 24, PURPLE).move_to(P(1.2, -1.6))
        pl = T("protein", 24, BLUE).move_to(P(-1.7, 0.6))
        self.play(FadeIn(dot), FadeIn(prot), FadeIn(dl), FadeIn(pl), run_time=0.5)
        self.play(dot.animate.move_to(P(0.2, -2.6)), dl.animate.move_to(P(1.2, -2.6)),
                  prot.animate.move_to(P(0, -0.5)), pl.animate.move_to(P(-1.7, -0.5)), run_time=0.7)
        self.play(dot.animate.move_to(P(0.2, -1.2)), dl.animate.move_to(P(1.2, -1.2)),
                  prot.animate.move_to(P(0, 0.9)), pl.animate.move_to(P(-1.7, 0.9)), run_time=0.7)

        self.at("cannot easily flip")
        jump = Arrow(P(0.2 + 0.25, -1.2), P(-1.0, -1.2), buff=0, color=RED, stroke_width=5, tip_length=0.22)
        x = cross(P(0.0, -1.2), 0.26)
        self.play(GrowArrow(jump), run_time=0.5)
        self.play(GrowFromCenter(x), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Protein(SpokenScene):
    def construct(self):
        yb, S = 0.0, 1.8
        er = Comp(-6.2, 6.2, yb, 3.65, 0.0)
        er_l = T("ER lumen", 26, TEAL).move_to(P(-4.9, 3.15))
        cy_l = T("cytosol", 26, GREY).move_to(P(-4.9, -3.0))
        p = protein(P(0, yb), S)
        self.add(er.base, er_l, cy_l)
        ny, cyy = 0.95 * S, -0.95 * S

        self.at("Take a protein")
        seg = T("membrane-spanning segment", 24, BLUE).move_to(P(-3.0, -0.45))
        self.play(Create(p.bar), FadeIn(seg), run_time=0.9)
        self.at("is in the lumen")
        nl = T("N terminus", 28, YELLOW).move_to(P(-2.9, ny))
        self.play(FadeIn(p.N, shift=DOWN * 0.3), FadeIn(nl), run_time=0.8)
        self.at("is in the cytosol")
        cl = T("C terminus", 28, GREEN).move_to(P(-2.9, cyy))
        self.play(FadeIn(p.C, shift=UP * 0.3), FadeIn(cl), run_time=0.8)
        self.at("makes it a")
        tc = chip("single-pass type I", BLUE, size=26).move_to(P(4.1, -2.0))
        self.play(FadeIn(tc), FadeOut(seg), run_time=0.6)
        self.at("carries a sugar")
        sl = T("sugar", 28, ORANGE).move_to(P(2.9, 3.1))
        self.play(FadeIn(p.S, shift=DOWN * 0.2), FadeIn(sl), run_time=0.6)
        self.play(pulse(p.S, ORANGE, 1.3), run_time=0.6)
        self.at("set once")
        self.play(pulse(VGroup(p.bar, p.N, p.C), None, 1.06), run_time=0.7)
        self.at("when the protein enters")
        tr = RoundedRectangle(corner_radius=0.2, width=2.0, height=1.2, stroke_color=GOLD, stroke_width=4).move_to(P(0, yb))
        trl = T("translocon", 26, GOLD).move_to(P(3.0, -0.5))
        trline = Line(P(1.75, -0.45), P(1.0, -0.15), color=GOLD, stroke_width=3)
        self.play(Create(tr), FadeIn(trl), Create(trline), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def bud(scene, wall_cap, ves, prot, run=1.0):
    """The wall bulges into a cup below it, carrying the protein to the cup's bottom."""
    ves.top.set_opacity(0)
    scene.play(FadeOut(wall_cap), Create(ves.bot), FadeIn(ves.fill), prot.animate.shift(DOWN * (R + DOCK)), run_time=run)


class S04Rule(SpokenScene):
    def construct(self):
        er = Comp(-6.2, -0.7, YB, YT, -3.45)
        go = Comp(0.7, 6.2, YB, YT, 3.45)
        er_l = T("ER lumen", 24, TEAL).move_to(P(-5.0, 3.15))
        go_l = T("Golgi lumen", 24, TEAL).move_to(P(5.0, 3.15))
        p = protein(P(-3.45, YB), PS)
        self.add(er.base, go.base, er_l, go_l, p)

        self.at("Here is the rule")
        b1 = chip("lumen", TEAL, size=28)
        eq = M("=", 36, TEXT)
        b2 = chip("outside the cell", TEAL, size=28)
        banner = VGroup(b1, eq, b2).arrange(RIGHT, buff=0.35).move_to(P(0, -1.0))
        self.play(FadeIn(b1), run_time=0.5)
        self.at("equivalent to")
        self.play(FadeIn(eq), FadeIn(b2, shift=LEFT * 0.2), run_time=0.7)

        self.at("A transport vesicle buds")
        v = vesicle(-3.45, YB - DOCK)
        v.remove(v.prot)
        v.prot = p
        self.play(FadeOut(banner), run_time=0.3)
        bud(self, er.cap, v, p, run=1.0)
        v.top.set_opacity(1)
        grp = VGroup(v.fill, v.bot, v.top, p)
        self.play(FadeIn(v.top), FadeIn(er.cap), run_time=0.3)
        self.play(grp.animate.shift(DOWN * DOWN_TRAVEL), run_time=0.5)
        self.play(grp.animate.shift(RIGHT * 6.9), run_time=1.0)
        self.play(grp.animate.shift(UP * DOWN_TRAVEL), run_time=0.5)
        self.play(FadeOut(go.cap), FadeOut(v.top), run_time=0.5)

        self.at("the donor lumen")
        self.play(pulse(er_l, TEAL, 1.2), run_time=0.7)
        self.at("and then with the target")
        self.play(pulse(go_l, TEAL, 1.2), run_time=0.7)

        self.at("Nothing crosses a membrane")
        ar = Arrow(P(4.2, -0.3), P(4.2, -2.0), buff=0, color=RED, stroke_width=5, tip_length=0.22)
        x = cross(P(4.2, -1.11), 0.25)
        self.play(GrowArrow(ar), run_time=0.5)
        self.play(GrowFromCenter(x), run_time=0.4)
        self.at("The face that pointed")
        self.play(FadeOut(ar), FadeOut(x), run_time=0.4)
        fl = T("faces the cytosol", 24, GREEN).move_to(P(1.2, -2.4))
        self.play(FadeIn(fl), pulse(p.C, GREEN, 1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Surface(SpokenScene):
    def construct(self):
        go = Comp(-6.2, -0.7, YB, YT, -3.45)
        pm = Comp(0.2, 6.3, YB, YT, 2.1, boxed=False)
        go_l = T("Golgi lumen", 24, TEAL).move_to(P(-5.0, 3.15))
        out_l = T("outside the cell", 24, TEAL).move_to(P(2.6, 3.15))
        pm_l = T("plasma membrane", 22, GREY).move_to(P(4.9, 2.0))
        self.add(go.base, pm.base, go_l, out_l, pm_l)

        v = vesicle(-3.45, YB - DOCK)
        self.at("Follow the protein")
        self.play(FadeIn(v), run_time=0.5)
        self.at("by vesicles")
        self.play(v.animate.shift(DOWN * DOWN_TRAVEL), run_time=0.35)
        self.play(v.animate.shift(RIGHT * 5.55), run_time=0.9)
        self.at("face stays")
        self.play(pulse(v.fill, TEAL, 1.06), pulse(v.prot.N, None, 1.3), run_time=0.8)
        self.at("A secretory vesicle")
        self.play(v.animate.shift(UP * DOWN_TRAVEL), run_time=0.7)
        self.at("Its lumen opens")
        self.play(FadeOut(pm.cap), FadeOut(v.top), pulse(out_l, TEAL, 1.15), run_time=0.9)

        self.at("the sugar now face")
        ecf = T("extracellular fluid", 24, TEAL).move_to(out_l)
        k1 = key_item("N terminus", YELLOW, P(4.3, 0.4))
        k2 = key_item("sugar", ORANGE, P(4.3, -0.3))
        self.play(FadeOut(out_l), run_time=0.25)
        self.play(FadeIn(ecf), FadeIn(k1), FadeIn(k2), run_time=0.6)
        self.play(pulse(v.prot.N, None, 1.3), pulse(v.prot.S, ORANGE, 1.3), run_time=0.8)
        self.at("stays in the cytosol")
        k3 = key_item("C terminus", GREEN, P(4.3, -1.0))
        cy = T("cytosol", 24, GREY).move_to(P(5.0, -2.2))
        self.play(FadeIn(k3), FadeIn(cy), pulse(v.prot.C, GREEN, 1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Endo(SpokenScene):
    def construct(self):
        px = -2.0
        pm = Comp(-6.3, 6.3, YB, YT, px, boxed=False)
        out_l = T("outside the cell", 24, TEAL).move_to(P(3.5, 3.15))
        cy = T("cytosol", 24, GREY).move_to(P(5.2, 1.0))
        p = protein(P(px, YB), PS)
        self.add(pm.base, out_l, cy, p)

        v = vesicle(px, YB - DOCK)
        v.remove(v.prot)
        v.prot = p
        self.at("Endocytosis pinches")
        bud(self, pm.cap, v, p, run=1.3)
        self.at("becomes the lumen")
        v.top.set_opacity(1)
        grp = VGroup(v.fill, v.bot, v.top, p)
        el = T("endosome lumen", 24, TEAL).move_to(P(0.0, -0.5)); el.shift(RIGHT * (-0.1 - el.get_left()[0]))
        self.play(FadeIn(v.top), FadeIn(pm.cap), run_time=0.4)
        self.play(grp.animate.shift(DOWN * (YB - DOCK - (-0.5))), FadeIn(el), run_time=0.9)

        self.at("face that lumen")
        k1 = key_item("N terminus", YELLOW, P(3.0, 0.4))
        k2 = key_item("sugar", ORANGE, P(3.0, -0.3))
        self.play(FadeIn(k1), FadeIn(k2), run_time=0.5)
        self.play(pulse(p.N, None, 1.3), pulse(p.S, ORANGE, 1.3), run_time=0.8)
        self.at("still faces the cytosol")
        k3 = key_item("C terminus", GREEN, P(3.0, -1.0))
        self.play(FadeIn(k3), pulse(p.C, GREEN, 1.3), run_time=0.8)
        self.at("At no step")
        nb = chip("always in the cytosol", GREEN, size=24).move_to(P(3.9, -2.1))
        self.play(FadeIn(nb), pulse(p.C, GREEN, 1.3), run_time=0.8)

        self.at("That is how")
        self.play(FadeOut(VGroup(pm.base, out_l, cy, grp, el, k1, k2, k3, nb)), run_time=0.6)
        names = ["ER lumen", "Golgi lumen", "outside the cell", "endosome lumen"]
        chips = [chip(n, TEAL, size=26) for n in names]
        row = VGroup(*chips).arrange(RIGHT, buff=0.7).move_to(P(0, -0.3))
        fit(row, max_w=12.4)
        arrows = [Arrow(chips[i].get_right(), chips[i + 1].get_left(), buff=0.05, color=GREY, stroke_width=4, tip_length=0.18)
                  for i in range(3)]
        sqs = [Square(side_length=0.36, stroke_width=0, fill_color=ORANGE, fill_opacity=1).next_to(c, UP, buff=0.35) for c in chips]
        lbl = T("sugar", 26, ORANGE).next_to(sqs[0], UP, buff=0.15)
        self.play(LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.25), run_time=1.2)
        self.play(*[GrowArrow(a) for a in arrows], run_time=0.5)
        self.play(*[FadeIn(s, scale=0.5) for s in sqs], FadeIn(lbl), run_time=0.6)

        self.at("Keep the rule")
        self.play(FadeOut(VGroup(*chips, *arrows, *sqs, lbl)), run_time=0.5)
        wall = corners([(-3.2, 0.0), (3.2, 0.0)])
        up = Rectangle(width=6.4, height=2.2, stroke_width=0, fill_color=LUM, fill_opacity=0.16).move_to(P(0, 1.1))
        pr = protein(P(0, 0.0), 1.3)
        l1 = T("Orientation is set once, at the ER", 40, font=TITLE_FONT).move_to(P(0, 3.0))
        self.play(FadeIn(up), FadeIn(wall), FadeIn(pr), run_time=0.6)
        self.play(FadeIn(l1, shift=DOWN * 0.1), run_time=0.7)
        self.at("never flips it")
        l2 = T("Traffic never flips it", 40, font=TITLE_FONT).move_to(P(0, -2.9))
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Orientation is set once at the ER. Traffic never flips it."
