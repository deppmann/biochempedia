"""Sugar chains record the route: the secretory pathway  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = membranes and compartments: the cell outline, ER, ERGIC, Golgi cisternae, granules
  YELLOW = the radioactively labelled protein (the cohort, the protein we follow)
  ORANGE = a high-mannose sugar chain: the one Endo H cuts (sensitive)
  GREEN  = a complex sugar chain: the one Endo H does not cut (resistant)
  PURPLE = the late sugars, galactose and sialic acid
  TEAL   = Endo H, the enzyme that reads the stamp
  RED    = a cut, a blocked step
  TEXT   = the half-time marker and neutral highlights
  GREY   = labels, axes, unlabelled protein, not-the-subject
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58AE6"
LANE = "#1a1d27"

CY = 0.1                       # vertical centre of the cell
ER_X = -5.2
ERGIC_X = -3.55
GX = [-2.3, -1.3, -0.3]        # cis, medial, trans
ER_Y = [CY + 0.85, CY, CY - 0.85]
LABEL_Y = -1.8


# ---------------------------------------------------------------------------------------------
# the cell
# ---------------------------------------------------------------------------------------------
def cell_outline():
    return RoundedRectangle(corner_radius=0.7, width=12.4, height=5.0, stroke_color=BLUE, stroke_width=5,
                            fill_opacity=0).move_to([0, CY, 0])


def er_stack():
    bars = VGroup(*[RoundedRectangle(corner_radius=0.25, width=1.7, height=0.5, stroke_color=BLUE, stroke_width=3,
                                     fill_color=BLUE, fill_opacity=0.12).move_to([ER_X, y, 0]) for y in ER_Y])
    ribo = VGroup()
    for y in ER_Y:
        for k in range(5):
            ribo.add(Dot([ER_X - 0.64 + k * 0.32, y + 0.31, 0], radius=0.04, color=GREY))
    return VGroup(bars, ribo)


def golgi_stack():
    return VGroup(*[RoundedRectangle(corner_radius=0.3, width=0.7, height=2.6, stroke_color=BLUE, stroke_width=3,
                                     fill_color=BLUE, fill_opacity=0.12).move_to([x, CY, 0]) for x in GX])


def ergic():
    return VGroup(*[Circle(radius=0.3, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.1)
                    .move_to([ERGIC_X, y, 0]) for y in (CY + 0.8, CY, CY - 0.8)])


GRAN_P = [np.array([x, y, 0.0]) for y in (0.75, -0.55) for x in (3.0, 4.2, 5.4)]


def granules():
    return VGroup(*[Circle(radius=0.38, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.12)
                    .move_to(p) for p in GRAN_P])


def lab(text, x, y=LABEL_Y, color=GREY, size=22):
    return T(text, size, color).move_to([x, y, 0])


ER_ROW = [np.array([ER_X - 0.6 + k * 0.24, CY, 0.0]) for k in range(6)]
GOLGI_ROW = [np.array([-1.3 - 0.6 + k * 0.24 + 0.12, CY, 0.0]) for k in range(6)]


def dot(p, color=YELLOW, r=0.1):
    return Dot(np.array(p, float), radius=r, color=color)


# ---------------------------------------------------------------------------------------------
# the protein and its sugar chain (a schematic knob, never a structure)
# ---------------------------------------------------------------------------------------------
def glycan(kind, p, s=1.0):
    """Sugar-chain stand-in drawn above the point p. kind: core, complex, tips."""
    p = np.array(p, float)
    col = ORANGE if kind == "core" else GREEN
    stalk = Line(p + UP * 0.12 * s, p + UP * 0.36 * s, color=col, stroke_width=4 * s)
    knob = Circle(radius=0.12 * s, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.55) \
        .move_to(p + UP * 0.48 * s)
    g = VGroup(stalk, knob)
    if kind in ("complex", "tips"):
        for sx in (-1, 1):
            b = Circle(radius=0.085 * s, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.55) \
                .move_to(p + UP * 0.6 * s + RIGHT * sx * 0.2 * s)
            g.add(b)
    if kind == "tips":
        for sx in (-1, 1):
            t = Circle(radius=0.06 * s, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.9) \
                .move_to(p + UP * 0.7 * s + RIGHT * sx * 0.34 * s)
            g.add(t)
    return g


def protein(kind, p, s=1.0, r=0.12):
    p = np.array(p, float)
    body = Dot(p, radius=r * s, color=YELLOW)
    g = VGroup(body, glycan(kind, p, s))
    g.kind, g.s = kind, s
    return g


def step(prot, p, kind=None):
    """Animations moving the protein body to p and (re)drawing its chain there (as kind)."""
    p = np.array(p, float)
    kind = kind or prot.kind
    prot.kind = kind
    return [prot[0].animate.move_to(p), Transform(prot[1], glycan(kind, p, prot.s))]


def stage_static(scene, with_gran=True, ergic_on=False, labels=("rough ER", "Golgi", "granules")):
    """Rebuild the standing cell for scenes that continue the story (no animation)."""
    parts = [cell_outline(), er_stack(), golgi_stack()]
    if with_gran:
        parts.append(granules())
    if ergic_on:
        parts.append(ergic())
    labs = []
    if "rough ER" in labels:
        labs.append(lab("rough ER", ER_X))
    if "Golgi" in labels:
        labs.append(lab("Golgi", GX[1]))
    if "granules" in labels and with_gran:
        labs.append(lab("granules", 4.2))
    scene.add(*parts, *labs)
    return parts, labs


class Plot:
    """Tiny axes with no LaTeX: maps data (x, y) onto the frame."""

    def __init__(self, origin, w, h, xmax, ymax):
        self.o = np.array([origin[0], origin[1], 0.0]); self.w, self.h, self.xm, self.ym = w, h, xmax, ymax

    def p(self, x, y):
        return self.o + np.array([x / self.xm * self.w, y / self.ym * self.h, 0.0])

    def axes(self):
        return VGroup(Line(self.o, self.o + RIGHT * self.w, color=GREY, stroke_width=3),
                      Line(self.o, self.o + UP * self.h, color=GREY, stroke_width=3))

    def curve(self, f, x0, x1, color, n=120, width=6):
        m = VMobject(color=color, stroke_width=width)
        m.set_points_smoothly([self.p(x, f(x)) for x in np.linspace(x0, x1, n)])
        return m

    def xtick(self, x, label, size=22):
        t = T(label, size, GREY).next_to(self.p(x, 0), DOWN, buff=0.14)
        k = Line(self.p(x, 0), self.p(x, 0) + DOWN * 0.1, color=GREY, stroke_width=3)
        return VGroup(k, t)

    def ytick(self, y, label, size=22):
        t = M(label, size, GREY).next_to(self.p(0, y), LEFT, buff=0.14)
        k = Line(self.p(0, y), self.p(0, y) + LEFT * 0.1, color=GREY, stroke_width=3)
        return VGroup(k, t)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "The secretory pathway"
    TITLE = "Sugar chains record the route"


# ---------------------------------------------------------------------------------------------
class S01Timetable(SpokenScene):
    """The puzzle: label the new proteins, then see where the label sits at 5, 20 and 60 minutes."""

    def construct(self):
        head = T("Guinea-pig pancreas cell after radioactive leucine", 30, font=TITLE_FONT).move_to([0, 3.2, 0])
        cell = cell_outline()
        er, gol, gran = er_stack(), golgi_stack(), granules()
        l_er, l_gol, l_gran = lab("rough ER", ER_X), lab("Golgi", GX[1]), lab("granules", 4.2)

        def tx(t):
            return -5.2 + t / 60 * 10.4
        axis = Line([-5.2, -2.95, 0], [5.2, -2.95, 0], color=GREY, stroke_width=3)
        ticks = VGroup()
        for t, name in ((5, "about 5 min"), (20, "about 20 min"), (60, "about 1 hour")):
            ticks.add(VGroup(Line([tx(t), -2.95, 0], [tx(t), -2.82, 0], color=GREY, stroke_width=3),
                             T(name, 22, GREY).move_to([tx(t), -3.3, 0])))
        mark = Triangle(color=YELLOW, fill_color=YELLOW, fill_opacity=1).scale(0.11).rotate(PI) \
            .move_to([tx(0), -2.82, 0])

        self.play(Write(head), FadeIn(cell), run_time=1.0)
        self.play(FadeIn(er), FadeIn(gol), FadeIn(gran), FadeIn(l_er), FadeIn(l_gol), FadeIn(l_gran),
                  Create(axis), run_time=1.2)
        self.at("Within about five")
        cohort = VGroup(*[dot(p) for p in ER_ROW])
        self.play(FadeIn(cohort, scale=0.5), FadeIn(ticks[0]), FadeIn(mark), mark.animate.move_to([tx(5), -2.82, 0]),
                  run_time=0.9)
        self.at("the label lies")
        self.play(LaggedStart(*[c.animate.move_to(p) for c, p in zip(cohort, GOLGI_ROW)], lag_ratio=0.05),
                  mark.animate.move_to([tx(20), -2.82, 0]), FadeIn(ticks[1]), run_time=1.6)
        self.at("By an hour")
        self.play(LaggedStart(*[c.animate.move_to(p) for c, p in zip(cohort, GRAN_P)], lag_ratio=0.05),
                  mark.animate.move_to([tx(60), -2.82, 0]), FadeIn(ticks[2]), run_time=2.0)
        self.at("How do we know")
        q1 = T("?", 64, TEXT, weight=BOLD).move_to([-3.1, CY + 1.3, 0])
        q2 = T("?", 64, TEXT, weight=BOLD).move_to([1.2, CY + 1.3, 0])
        a1 = Arrow([-4.2, CY + 0.7, 0], [-2.9, CY + 0.7, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
        a2 = Arrow([0.4, CY + 0.7, 0], [2.4, CY + 0.7, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
        self.play(FadeOut(cohort), FadeIn(a1), FadeIn(a2), FadeIn(q1, scale=0.5), FadeIn(q2, scale=0.5), run_time=0.7)
        self.at("how fast")
        hf = T("how fast?", 36, YELLOW, weight=BOLD).move_to([0, 2.1, 0])
        self.play(FadeIn(hf, shift=DOWN * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Cohort(SpokenScene):
    """Pulse, chase, cohort."""

    def construct(self):
        stage_static(self)
        pulse = chip("pulse: radioactive amino acid", YELLOW, size=22, pad=0.16).move_to([-2.6, 3.1, 0])
        feed = Arrow([-5.75, 2.78, 0], [-5.75, 1.45, 0], buff=0, color=YELLOW, stroke_width=5, tip_length=0.22)
        self.at("method is called")
        title = T("pulse-chase", 34, font=TITLE_FONT).move_to([3.7, 3.1, 0])
        self.play(Write(title), run_time=0.8)
        self.at("short pulse")
        self.play(FadeIn(pulse, shift=DOWN * 0.1), GrowArrow(feed), run_time=0.6)
        cohort = VGroup(*[dot(p) for p in ER_ROW])
        self.play(LaggedStart(*[FadeIn(c, scale=0.3) for c in cohort], lag_ratio=0.1), run_time=1.0)
        self.at("Then comes the chase")
        chase = chip("chase: unlabelled amino acid", GREY, size=22, pad=0.16).move_to([-2.6, 3.1, 0])
        feed2 = Arrow([-5.75, 2.78, 0], [-5.75, 1.45, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.22)
        self.play(ReplacementTransform(pulse, chase), ReplacementTransform(feed, feed2), run_time=0.7)
        grey = VGroup()
        for y in (ER_Y[0], ER_Y[2]):
            for k in range(6):
                grey.add(dot([ER_X - 0.6 + k * 0.24, y, 0], GREY))
        self.at("flood")
        self.play(LaggedStart(*[FadeIn(g, scale=0.3) for g in grey], lag_ratio=0.06), run_time=1.3)
        self.at("carries label")
        l1 = VGroup(dot([0, 0, 0], YELLOW, 0.13), T("labelled", 26, YELLOW)).arrange(RIGHT, buff=0.25)
        l2 = VGroup(dot([0, 0, 0], GREY, 0.13), T("unlabelled", 26, GREY)).arrange(RIGHT, buff=0.25)
        leg = VGroup(l1, l2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([1.9, 1.85, 0])
        self.play(FadeIn(leg, shift=LEFT * 0.2), run_time=0.6)
        self.at("labeled group is a cohort")
        br = RoundedRectangle(corner_radius=0.2, width=1.75, height=0.52, stroke_color=YELLOW, stroke_width=3) \
            .move_to([ER_X, CY, 0])
        br = DashedVMobject(br, num_dashes=28)
        cl = T("cohort", 30, YELLOW, weight=BOLD).move_to([-3.2, CY + 0.0, 0])
        cl.move_to([-3.6, CY, 0])
        self.play(Create(br), FadeIn(cl), run_time=0.8)
        self.at("follow it")
        grp = VGroup(cohort, br, cl)
        self.play(FadeOut(leg), run_time=0.3)
        self.play(*[c.animate.move_to(p) for c, p in zip(cohort, GOLGI_ROW)],
                  br.animate.move_to([GX[1], CY, 0]), cl.animate.move_to([GX[1], CY + 1.7, 0]), run_time=2.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Stamp(SpokenScene):
    """One protein, one sugar chain, rebuilt at the Golgi."""

    def construct(self):
        stage_static(self, with_gran=False, labels=("rough ER",))
        # the panel on the right keeps the three states of the chain
        PX = 1.9
        rows = [("core: 14 sugars", "core", 1.55), ("rebuilt: complex", "complex", 0.35),
                ("+ galactose,\nsialic acid", "tips", -0.85)]
        panel = []
        for text, kind, y in rows:
            ic = glycan(kind, [PX, y - 0.3, 0], 1.4)
            tx = T(text, 24, TEXT if kind != "core" else ORANGE, line_spacing=0.7).move_to([PX + 2.0, y, 0])
            panel.append(VGroup(ic, tx))
        panel[1][1].set_color(GREEN)
        panel[2][1].set_color(PURPLE)
        for p_ in panel:
            p_[1].align_to([PX + 0.75, 0, 0], LEFT)
        base = [ER_X, CY - 0.2, 0]
        self.at("In the")
        lum = lab("lumen", ER_X, CY + 1.65)
        lum.set_color(GREY)
        pr = protein("core", base, 0.9)
        self.play(FadeIn(pr, scale=0.5), FadeIn(lum), run_time=0.7)
        self.at("core of")
        self.play(FadeIn(panel[0], shift=LEFT * 0.2), run_time=0.7)
        self.at("It passes")
        eg = ergic()
        lerg = lab("ERGIC", ERGIC_X)
        self.play(FadeOut(lum), FadeIn(eg), FadeIn(lerg), *step(pr, [ERGIC_X, CY - 0.2, 0]), run_time=1.2)
        self.at("enters the Golgi")
        cis = lab("cis", GX[0], CY + 1.65)
        self.play(FadeIn(cis), *step(pr, [GX[0], CY - 0.2, 0]), run_time=1.0)
        self.at("Golgi enzymes then rebuild")
        med = lab("medial", GX[1], CY + 1.65)
        tr = lab("trans", GX[2], CY + 1.65)
        self.play(FadeIn(med), FadeIn(tr), run_time=0.4)
        self.at("rebuild the sugar")
        self.play(*step(pr, [GX[1], CY - 0.2, 0], "complex"), FadeIn(panel[1], shift=LEFT * 0.2), run_time=1.1)
        self.at("crosses to")
        self.play(*step(pr, [GX[2], CY - 0.2, 0]), run_time=0.9)
        self.at("Early enzymes act first")
        self.play(Indicate(panel[1], color=GREEN, scale_factor=1.06), run_time=0.9)
        self.at("added later")
        self.play(*step(pr, [GX[2], CY - 0.2, 0], "tips"), FadeIn(panel[2], shift=LEFT * 0.2), run_time=0.9)
        self.at("So the chain")
        box = SurroundingRectangle(VGroup(*panel), color=YELLOW, buff=0.22, corner_radius=0.18, stroke_width=3)
        st = T("the stamp: how far it has come", 24, YELLOW).move_to([PX + 1.7, -1.85, 0])
        self.play(Create(box), FadeIn(st), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Endoh(SpokenScene):
    """Endo H cuts the orange chain, not the green one; cut protein runs faster; the resistant band counts arrivals."""

    def construct(self):
        s = 2.4
        p1 = np.array([-5.0, -0.5, 0.0]); p2 = np.array([-2.4, -0.5, 0.0])
        pr1 = protein("core", p1, s)
        pr2 = protein("complex", p2, s)
        l1 = T("high-mannose", 24, ORANGE).move_to([p1[0], -1.35, 0])
        l2 = T("complex", 24, GREEN).move_to([p2[0], -1.35, 0])
        self.play(FadeIn(pr1, scale=0.6), FadeIn(pr2, scale=0.6), FadeIn(l1), FadeIn(l2), run_time=0.9)
        endo = chip("Endo H", TEAL, size=30, pad=0.2).move_to([-3.7, 2.9, 0])
        self.at("reads that")
        self.play(FadeIn(endo, shift=DOWN * 0.15), run_time=0.6)
        self.at("It cuts")
        k1 = pr1[1][1].get_center()
        self.play(endo.animate.next_to(pr1[1][1], RIGHT, buff=0.3), run_time=0.7)
        slash = Line(k1 + np.array([-0.4, -0.45, 0]), k1 + np.array([0.4, -0.15, 0]), color=RED, stroke_width=6)
        self.play(Create(slash), run_time=0.2)
        self.play(VGroup(pr1[1][1:]).animate.shift(UP * 0.5 + LEFT * 0.4).set_opacity(0), FadeOut(slash), run_time=0.7)
        self.at("does not cut")
        self.play(endo.animate.next_to(pr2[1][1], RIGHT, buff=0.55), run_time=0.8)
        self.play(endo.animate.shift(RIGHT * 0.12), run_time=0.1)
        self.play(endo.animate.shift(LEFT * 0.24), run_time=0.1)
        self.play(endo.animate.shift(RIGHT * 0.12), run_time=0.1)
        nc = T("not cut", 24, GREY).next_to(endo, DOWN, buff=0.2)
        self.play(FadeIn(nc), run_time=0.3)
        # gel
        self.at("Cut protein")
        lx = [2.9, 4.9]
        w = 1.6
        lanes = VGroup(*[Rectangle(width=w, height=4.4, fill_color=LANE, fill_opacity=1, stroke_color=GREY,
                                   stroke_width=2).move_to([x, -0.1, 0]) for x in lx])
        lt = [T("no Endo H", 22, GREY).move_to([lx[0], 2.4, 0]), T("Endo H", 22, TEAL).move_to([lx[1], 2.4, 0])]
        hw = (w - 0.3) / 2
        BH = 0.4

        def band(x, y, c, half):
            r = Rectangle(width=hw, height=BH, stroke_width=0, fill_color=c, fill_opacity=0.75)
            return r.move_to([x + half * hw / 2, y, 0])
        yt = 0.9
        a_o = band(lx[0], yt, ORANGE, -1); a_g = band(lx[0], yt, GREEN, 1)
        b_o = band(lx[1], yt, ORANGE, -1); b_g = band(lx[1], yt, GREEN, 1)
        self.play(FadeOut(endo), FadeOut(nc), FadeIn(lanes), *[FadeIn(t) for t in lt], FadeIn(a_o), FadeIn(a_g),
                  FadeIn(b_o), FadeIn(b_g), run_time=0.6)
        self.at("runs faster")
        ghost = DashedVMobject(Rectangle(width=hw, height=BH, stroke_color=ORANGE, stroke_width=2)
                               .move_to(b_o.get_center()), num_dashes=16)
        dn = Arrow([lx[1] - 1.0, yt - 0.3, 0], [lx[1] - 1.0, -1.1, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(ghost), b_o.animate.move_to([lx[1] - hw / 2, -0.8, 0]), GrowArrow(dn), run_time=1.3)
        self.at("resistant band counts")
        br = SurroundingRectangle(b_g, color=GREEN, buff=0.08, stroke_width=4)
        cap = T("reached those enzymes", 24, GREEN).move_to([4.2, -2.75, 0])
        self.play(Create(br), FadeIn(cap), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
TIMES = [0, 15, 30, 60]
RES = [0, 330, 550, 800]
SEN = [1000, 670, 450, 200]


class S05Numbers(SpokenScene):
    """The illustrative time course and the rate constant."""

    def construct(self):
        lx = [-4.2, -2.9, -1.6, -0.3]
        w = 1.15
        yt, yb = 0.85, -0.75
        lanes = VGroup(*[Rectangle(width=w, height=4.2, fill_color=LANE, fill_opacity=1, stroke_color=GREY,
                                   stroke_width=2).move_to([x, 0.2, 0]) for x in lx])
        labs = VGroup(*[M(str(t), 24, TEXT).move_to([x, 2.65, 0]) for x, t in zip(lx, TIMES)])
        ttl = T("chase time (min)", 24, GREY).move_to([-2.45, 3.15, 0])
        ill = T("illustrative data", 22, GREY).move_to([-2.45, -3.35, 0])
        rl = T("resistant", 22, GREEN).move_to([-5.6, yt, 0])
        sl = T("sensitive", 22, ORANGE).move_to([-5.6, yb, 0])
        self.at("illustrative time course")
        self.play(FadeIn(lanes), FadeIn(labs), FadeIn(ttl), FadeIn(rl), FadeIn(sl), FadeIn(ill), run_time=1.0)
        self.at("At each chase time")

        def band(x, y, c, n):
            if n == 0:
                return VGroup()
            r = Rectangle(width=w - 0.2, height=0.42, stroke_width=0, fill_color=c,
                          fill_opacity=0.2 + 0.7 * n / 1000).move_to([x, y, 0])
            t = M(f"{n:,}", 22, TEXT).move_to(r)
            return VGroup(r, t)
        bands = [(band(x, yt, GREEN, r), band(x, yb, ORANGE, s)) for x, r, s in zip(lx, RES, SEN)]
        self.play(LaggedStart(*[AnimationGroup(FadeIn(a), FadeIn(b)) for a, b in bands], lag_ratio=0.25), run_time=1.6)
        self.at("add up to")
        tot = VGroup(*[M("1,000", 22, GREY).move_to([x, -2.35, 0]) for x in lx])
        tl = T("total", 22, GREY).move_to([-5.6, -2.35, 0])
        self.play(FadeIn(tot, shift=UP * 0.1), FadeIn(tl), run_time=0.7)
        self.at("share is")
        pc = VGroup(*[M(f"{p}%", 22, GREEN).move_to([x, -2.85, 0]) for x, p in zip(lx, (0, 33, 55, 80))])
        pl = T("share", 22, GREEN).move_to([-5.6, -2.85, 0])
        self.play(FadeIn(pc, shift=UP * 0.1), FadeIn(pl), run_time=0.8)
        # right side
        self.at("rate constant")
        f1 = M("k = −ln S / t", 34, YELLOW, weight=BOLD).move_to([3.4, 2.5, 0])
        f2 = T("S = share still sensitive", 24, ORANGE).move_to([3.4, 1.8, 0])
        self.play(FadeIn(f1, shift=DOWN * 0.1), FadeIn(f2), run_time=0.8)
        rows = []
        data = [("−ln(0.67) / 15", "0.0267"), ("−ln(0.45) / 30", "0.0266"), ("−ln(0.20) / 60", "0.0268")]
        for i, (a, b) in enumerate(data):
            r = VGroup(M(a, 24, TEXT), M("=", 24, GREY), M(b, 24, GREEN, weight=BOLD)).arrange(RIGHT, buff=0.2)
            r.move_to([3.4, 0.8 - i * 0.75, 0])
            rows.append(r)
        self.at("comes out near")
        self.play(FadeIn(rows[0], shift=RIGHT * 0.15), run_time=0.6)
        self.at("per minute")
        self.play(FadeIn(rows[1], shift=RIGHT * 0.15), run_time=0.6)
        self.at("minutes")
        self.play(FadeIn(rows[2], shift=RIGHT * 0.15), run_time=0.6)
        pm = T("per minute", 22, GREY).move_to([3.4, -1.55, 0])
        self.play(FadeIn(pm), run_time=0.3)
        self.at("The three agree")
        sb = SurroundingRectangle(VGroup(*[r[2] for r in rows]), color=GREEN, buff=0.12, corner_radius=0.1)
        self.play(Create(sb), run_time=0.7)
        self.at("so one first")
        fo = chip("one first-order step", GREEN, size=26, pad=0.16).move_to([3.4, -2.55, 0])
        self.play(FadeIn(fo, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Halftime(SpokenScene):
    """Half-time, what it covers, the threshold, and the rule."""

    def construct(self):
        P = Plot([-5.3, -2.1], 7.0, 4.3, 60, 1.0)
        ax = P.axes()
        xt = VGroup(*[P.xtick(t, str(t)) for t in (0, 15, 30, 60)])
        yt = VGroup(*[P.ytick(v, lbl) for v, lbl in ((0, "0"), (0.5, "0.5"), (1, "1"))])
        xl = T("chase time (min)", 24, GREY).move_to(P.p(30, 0) + DOWN * 0.95)
        yl = T("share still sensitive, S", 24, ORANGE).move_to(P.p(0, 1.0) + UP * 0.45 + RIGHT * 2.0)
        curve = P.curve(lambda t: math.exp(-0.0267 * t), 0, 60, ORANGE)
        pts = VGroup(*[Dot(P.p(t, s / 1000), radius=0.1, color=ORANGE) for t, s in zip(TIMES, SEN)])
        self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), run_time=0.8)
        self.play(FadeIn(pts, scale=0.5), Create(curve), run_time=1.2)
        self.at("divided by")
        f1 = M("t½ = ln 2 / k", 30, TEXT).move_to([4.2, 2.4, 0])
        f2 = M("= 0.693 / 0.0267", 30, TEXT).move_to([4.2, 1.7, 0])
        half = DashedLine(P.p(0, 0.5), P.p(26, 0.5), color=TEXT, stroke_width=3)
        drop = DashedLine(P.p(26, 0.5), P.p(26, 0), color=TEXT, stroke_width=3)
        hd = Dot(P.p(26, 0.5), radius=0.13, color=TEXT)
        self.play(FadeIn(f1, shift=DOWN * 0.1), Create(half), run_time=0.8)
        self.play(FadeIn(f2, shift=DOWN * 0.1), Create(drop), FadeIn(hd, scale=0.4), run_time=0.8)
        f3 = M("= 26 min", 34, TEXT, weight=BOLD).move_to([4.2, 0.95, 0])
        self.play(FadeIn(f3, shift=DOWN * 0.1), run_time=0.5)
        self.at("That covers")
        bra = BraceBetweenPoints(P.p(0, 0) + DOWN * 0.95 + LEFT * 0.0, P.p(26, 0) + DOWN * 0.95, direction=DOWN, color=BLUE)
        bra.shift(DOWN * 0.0)
        cov = T("ER exit plus the trip\nto the Golgi enzymes", 24, BLUE, line_spacing=0.8).move_to([4.2, -0.2, 0])
        cov2 = T("(26 min)", 24, BLUE)
        # brace sits below the tick labels: move the axis title out of the way first
        self.play(FadeOut(xl), run_time=0.2)
        bra = Brace(Line(P.p(0, 0), P.p(26, 0)), direction=DOWN, color=BLUE, buff=0.55)
        self.play(GrowFromCenter(bra), FadeIn(cov, shift=UP * 0.1), run_time=0.9)
        self.at("upper bound")
        ub = T("an upper bound for\nER exit alone", 24, YELLOW, line_spacing=0.8).move_to([4.2, -1.45, 0])
        self.play(FadeIn(ub, shift=UP * 0.1), run_time=0.7)
        # threshold scene
        self.at("Resistance is")
        everything = VGroup(ax, xt, yt, yl, curve, pts, f1, f2, f3, half, drop, hd, bra, cov, ub)
        self.play(FadeOut(everything), run_time=0.4)
        route_y = 0.5
        xs, xe, xth, xc = -5.2, 5.2, -0.4, -2.6
        seg1 = Line([xs, route_y, 0], [xth, route_y, 0], color=ORANGE, stroke_width=14)
        seg2 = Line([xth, route_y, 0], [xe, route_y, 0], color=GREEN, stroke_width=14)
        er_l = T("ER", 30, BLUE, weight=BOLD).move_to([xs, route_y - 0.7, 0])
        go_l = T("end of Golgi", 30, BLUE, weight=BOLD).move_to([xe - 0.4, route_y - 0.7, 0])
        cis_l = T("cis Golgi", 30, BLUE, weight=BOLD).move_to([xc, route_y - 0.7, 0])
        cis_k = Line([xc, route_y - 0.25, 0], [xc, route_y + 0.25, 0], color=BLUE, stroke_width=4)
        self.play(Create(seg1), FadeIn(er_l), FadeIn(go_l), FadeIn(cis_l), FadeIn(cis_k), run_time=0.4)
        self.at("a threshold")
        seg2.set_opacity(1)
        tick = DashedLine([xth, route_y - 0.9, 0], [xth, route_y + 1.4, 0], color=TEXT, stroke_width=3)
        tl = T("early Golgi enzymes have acted", 26, TEXT).move_to([xth, route_y + 1.8, 0])
        lo = T("sensitive", 26, ORANGE).move_to([-3.4, route_y + 1.1, 0])
        hi = T("resistant", 26, GREEN).move_to([3.0, route_y + 1.1, 0])
        self.play(Create(seg2), Create(tick), FadeIn(tl), FadeIn(lo), FadeIn(hi), run_time=1.1)
        self.at("not a switch")
        nt = T("not this:", 28, RED, weight=BOLD).move_to([-5.3, -1.9, 0])
        w1 = chip("ER: sensitive", ORANGE, size=24).move_to([-2.9, -1.9, 0])
        w2 = chip("Golgi: resistant", GREEN, size=24).move_to([1.1, -1.9, 0])
        arr = Arrow(w1.get_right() + RIGHT * 0.05, w2.get_left() + LEFT * 0.05, buff=0, color=GREY, stroke_width=4,
                    tip_length=0.2)
        mx = (w1.get_right()[0] + w2.get_left()[0]) / 2
        cross = VGroup(Line([mx - 0.25, -1.65, 0], [mx + 0.25, -2.15, 0], color=RED, stroke_width=7),
                       Line([mx - 0.25, -2.15, 0], [mx + 0.25, -1.65, 0], color=RED, stroke_width=7))
        self.play(FadeIn(nt), FadeIn(w1), FadeIn(w2), GrowArrow(arr), run_time=0.7)
        self.play(Create(cross), run_time=0.5)
        # the rule
        self.at("Keep the rule")
        self.play(FadeOut(VGroup(nt, w1, w2, arr, cross)), run_time=0.4)
        pr = protein("core", [xs + 0.3, route_y + 0.0, 0], 0.9)
        self.play(FadeIn(pr, scale=0.5), run_time=0.4)
        self.at("records how far")
        self.play(*step(pr, [xth + 1.6, route_y, 0], "complex"), run_time=1.5)
        self.play(*step(pr, [xe - 0.6, route_y, 0], "tips"), run_time=1.3)
        rule = T("The sugar chain records how far the protein has come.", 34, YELLOW, font=TITLE_FONT)
        fit(rule, max_w=11.8)
        rule.move_to([0, -2.1, 0])
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "The sugar chain records how far the protein has come."
