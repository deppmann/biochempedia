"""Sugar chains record the route: the secretory pathway  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = membranes and compartments: the cell outline, ER, ERGIC, Golgi cisternae, granules
  YELLOW = the radioactively labelled protein (the cohort, the protein we follow)
  ORANGE = high-mannose / hybrid sugar chains: Endo H sensitive
  GREEN  = a complex sugar chain: the one Endo H does not cut (resistant)
  PURPLE = the late sugars, galactose and sialic acid
  TEAL   = Endo H, the enzyme that reads the stamp
  RED    = a cut, a blocked step
  TEXT   = ER residents, receptors, and neutral highlights
  GOLD   = early Golgi resident-enzyme markers
  PURPLE also marks late Golgi resident enzymes (distinct from cargo)
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
    TITLE = "The Secretory Pathway"


def heading(text):
    return T(text, 34, font=TITLE_FONT).move_to([0, 3.15, 0])


def arrow(a, b, color=GREY):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=4, tip_length=0.18)


def route_diagram():
    """The old organelle shapes, with a compact pair of exits on the right."""
    er = VGroup(er_stack(), lab("rough ER", ER_X))
    intermediate = VGroup(ergic(), lab("ERGIC", ERGIC_X))
    golgi = VGroup(golgi_stack(), lab("Golgi", GX[1]))
    surface = VGroup(Line([6.0, -2.3, 0], [6.0, 2.3, 0], color=BLUE, stroke_width=6),
                     T("surface", 22, BLUE).move_to([5.8, 2.7, 0]))
    gran = VGroup(Circle(radius=0.48, color=BLUE, fill_color=BLUE, fill_opacity=0.12)
                 .move_to([3.5, -0.8, 0]), lab("granule", 3.5, -1.8))
    forward = VGroup(arrow([-4.2, 0.1, 0], [-3.9, 0.1, 0]),
                     arrow([-3.15, 0.1, 0], [-2.75, 0.1, 0]),
                     arrow([0.25, 0.1, 0], [5.8, 1.3, 0]),
                     arrow([0.25, 0.1, 0], [2.95, -0.8, 0]),
                     arrow([4.05, -0.8, 0], [5.8, -0.8, 0]))
    return VGroup(er, intermediate, golgi, surface, gran, forward)


def recycling():
    return VGroup(arrow([-0.2, -2.55, 0], [-5.1, -2.55, 0], BLUE),
                  arrow([-0.3, 2.0, 0], [-2.3, 2.0, 0], BLUE))


class S01Timetable(SpokenScene):
    def construct(self):
        cell = cell_outline()
        cargo = dot([5.6, 0.6, 0], r=0.15)
        self.at("Cells send")
        self.play(FadeIn(cell), FadeIn(cargo), run_time=0.7)
        self.at("release them outside")
        self.play(cargo.animate.move_to([6.6, 0.6, 0]), run_time=0.7)
        examples = T("Examples: digestive enzymes • hormones", 28, YELLOW).move_to([0, 3.1, 0])
        self.at("Think of")
        self.play(FadeIn(examples), run_time=0.6)
        route = route_diagram()
        self.at("The conventional route")
        self.play(FadeOut(cell), FadeOut(cargo), FadeIn(route[0]), run_time=0.6)
        cargo = dot([ER_X, CY, 0], r=0.15)
        self.at("rough endoplasmic reticulum")
        self.play(FadeIn(cargo), Indicate(route[0][0], color=BLUE), run_time=0.8)
        self.at("Cargo travels")
        self.play(FadeIn(route[1]), FadeIn(route[2]), FadeIn(route[5][:2]),
                  cargo.animate.move_to([ERGIC_X, CY, 0]), run_time=0.65)
        self.play(cargo.animate.move_to([GX[0], CY, 0]), run_time=0.65)
        self.at("processed and sorted")
        self.play(cargo.animate.move_to([GX[-1], CY, 0]), run_time=0.7)
        self.at("This pathway connects")
        self.play(FadeIn(route[3]), FadeIn(route[4]), FadeIn(route[5][2:]), run_time=0.7)
        stored = dot([GX[-1], CY, 0], r=0.13)
        self.at("straight away")
        self.play(FadeIn(stored), cargo.animate.move_to([6.5, 1.3, 0]), run_time=0.75)
        self.at("after storage")
        self.play(stored.animate.move_to([3.5, -0.8, 0]), run_time=0.75)
        self.finish()


class S02Cohort(SpokenScene):
    def construct(self):
        parts, labels = stage_static(self)
        title = heading("How do we know the order?")
        self.at("How do we")
        self.play(FadeIn(title), run_time=0.6)
        yellow = VGroup(*[dot(p) for p in ER_ROW])
        pulse = T("PULSE: labelled proteins", 28, YELLOW).move_to([0, 1.95, 0])
        self.at("A pulse chase")
        self.play(FadeIn(yellow, scale=0.5), FadeIn(pulse), run_time=0.7)
        grey = VGroup(*[dot(p + DOWN * 0.8, GREY) for p in ER_ROW])
        chase = T("CHASE: unlabelled proteins", 28, GREY).move_to([0, 1.95, 0])
        self.at("then supplies")
        self.play(ReplacementTransform(pulse, chase), FadeIn(grey, scale=0.5), run_time=0.7)
        pancreas = heading("Guinea-pig pancreas")
        self.at("In guinea pig pancreas")
        self.play(ReplacementTransform(title, pancreas), run_time=0.6)
        self.at("rough ER")
        self.play(Indicate(parts[1], color=YELLOW), run_time=0.6)
        self.at("to Golgi")
        self.play(*[c.animate.move_to(p) for c,p in zip(yellow, GOLGI_ROW)],
                  Indicate(parts[2], color=YELLOW), run_time=0.6)
        self.at("to granules")
        self.play(*[c.animate.move_to(p) for c,p in zip(yellow, GRAN_P)],
                  Indicate(parts[3], color=YELLOW), run_time=0.8)
        self.at("The experiment establishes")
        self.finish()


class S03Stamp(SpokenScene):
    def construct(self):
        er = RoundedRectangle(width=4.5, height=3.8, corner_radius=0.25,
                              color=BLUE, fill_color=BLUE, fill_opacity=0.12).move_to([0, 0, 0])
        erlab = lab("ER lumen", 0, -2.6, BLUE, 28)
        cargo = protein("core", [0, -0.6, 0], 2.3)
        cargo[0].stretch(2, 0)
        self.at("Processing starts")
        self.play(FadeIn(er), FadeIn(erlab), FadeIn(cargo[0]), run_time=0.7)
        corelab = T("core sugar chain", 30, ORANGE).move_to([0, 2.3, 0])
        tips = VGroup(*[Square(side_length=0.13, color=ORANGE, fill_opacity=1)
                        .move_to([-0.22+i*0.22, 0.95, 0]) for i in range(3)])
        self.at("A core sugar chain")
        self.play(FadeIn(cargo[1]), FadeIn(tips), FadeIn(corelab), run_time=0.7)
        folded = T("glucoses trimmed • cargo folds", 26, TEXT).move_to([0, 3.15, 0])
        self.at("glucoses are trimmed")
        self.play(tips.animate.shift(UP*0.6).set_opacity(0),
                  cargo[0].animate.stretch(0.5, 0), FadeIn(folded), run_time=1.0)
        intermediate = VGroup(Circle(radius=0.65, color=BLUE, fill_opacity=0.1),
                              lab("ERGIC", 0, -2.0)).move_to([-2.4, -0.5, 0])
        # Keep the compartment centre on the cargo route, its label below it.
        intermediate[0].move_to([-2.4, 0, 0]); intermediate[1].move_to([-2.4, -2.0, 0])
        sacs = VGroup(*[RoundedRectangle(width=0.7, height=2.8, corner_radius=0.3,
                          color=BLUE, fill_color=BLUE, fill_opacity=0.12).move_to([x, 0, 0])
                          for x in (0, 2, 4)])
        labs = VGroup(*[lab(t, x, -2.0, BLUE, 24) for t,x in zip(("cis Golgi", "medial", "trans"), (0,2,4))])
        regions = VGroup(*[RoundedRectangle(width=3.0, height=3.2, corner_radius=0.4,
                            stroke_width=0, fill_color=c, fill_opacity=0.10).move_to([x, 0, 0])
                            for x,c in zip((0,2,4), (ORANGE,GREEN,PURPLE))])
        self.at("Folded cargo passes")
        cargo.s = 1.6
        small_er = RoundedRectangle(width=2.7, height=2.8, corner_radius=0.25,
                                   color=BLUE, fill_color=BLUE, fill_opacity=0.12).move_to([-4.8,0,0])
        self.play(FadeOut(folded), FadeOut(corelab), run_time=0.25)
        self.play(FadeIn(intermediate[0]), Transform(er, small_er),
                  erlab.animate.move_to([-4.8,-2.0,0]),
                  cargo[0].animate.scale(1.6/2.3).move_to([-2.4,-0.6,0]),
                  Transform(cargo[1],glycan("core",[-2.4,-0.6,0],1.6)),run_time=0.65)
        self.play(FadeIn(intermediate[1]), FadeIn(heading("Processing along the route")), run_time=0.25)
        self.at("to the cis")
        self.play(FadeIn(sacs), FadeIn(labs), *step(cargo, [0,-0.6,0]), run_time=0.9)
        self.at("enzymes rebuild")
        regions.set_z_index(-1)
        self.play(FadeIn(regions), *step(cargo, [2,-0.6,0], "complex"), run_time=1.2)
        late = T("galactose", 26, PURPLE).move_to([2, -2.9, 0])
        self.at("adding galactose")
        self.play(*step(cargo, [4,-0.6,0], "tips"), FadeIn(late), run_time=0.8)
        sialic = T("sialic acid", 26, PURPLE).move_to([5.0, -2.9, 0])
        cap = RoundedRectangle(width=0.24, height=0.16, corner_radius=0.05,
                               color=PURPLE, fill_opacity=1).move_to([4, 0.75, 0])
        self.at("sialic acid")
        self.play(FadeIn(sialic), FadeIn(cap), run_time=0.6)
        self.finish()


class S04Retrieval(SpokenScene):
    def construct(self):
        er = RoundedRectangle(width=3.0, height=2.8, corner_radius=0.3, color=BLUE,
                              fill_color=BLUE, fill_opacity=0.12).move_to([-4.4,0,0])
        later = RoundedRectangle(width=4.4, height=2.8, corner_radius=0.3, color=BLUE,
                                 fill_color=BLUE, fill_opacity=0.12).move_to([2.6,0,0])
        labels = VGroup(lab("ER",-4.4,-2.0,BLUE,28), lab("ERGIC / Golgi",2.6,-2.0,BLUE,28))
        resident = VGroup(Square(side_length=0.35, color=TEXT, fill_opacity=0.7),
                          T("ER resident",22,TEXT).move_to([0,-0.65,0])).move_to([-4.4,0,0])
        cargo = dot([-4.4,0.75,0], r=0.14)
        self.at("ER residents")
        self.play(FadeIn(er), FadeIn(later), FadeIn(labels), FadeIn(resident), FadeIn(cargo), run_time=0.6)
        self.at("escape with cargo")
        self.play(resident.animate.move_to([2.2,0,0]), cargo.animate.move_to([4.25,-0.85,0]), run_time=1.0)
        tag = chip("KDEL", TEXT, size=24, pad=0.1).move_to([2.2,0.65,0])
        taglabel = heading("KDEL: return to sender")
        self.at("The KDEL tag")
        self.play(FadeIn(tag), FadeIn(taglabel), run_time=0.6)
        # A cup on the lumenal face of a schematic membrane receptor.
        receptor = VGroup(Arc(radius=0.38, start_angle=PI, angle=PI, color=TEXT, stroke_width=6),
                           Line([0,-0.38,0],[0,-0.8,0],color=TEXT,stroke_width=6)).move_to([3.45,0.05,0])
        self.at("Its receptor binds")
        self.play(FadeIn(receptor), resident[0].animate.move_to([3.45,0.15,0]),
                  resident[1].animate.move_to([1.6,0.15,0]),
                  tag.animate.move_to([3.45,0.8,0]), run_time=0.8)
        ph = T("slightly acidic: binds",26,TEXT).move_to([2.6,-2.8,0])
        self.at("slightly acidic")
        self.play(FadeIn(ph),run_time=0.6)
        coat = DashedVMobject(Circle(radius=1.0,color=BLUE,stroke_width=5).move_to([3.45,0.2,0]), num_dashes=20)
        cop = T("COPI return vesicle",26,BLUE).move_to([0,2.25,0])
        self.at("COP1 vesicles")
        self.play(FadeIn(coat), FadeIn(cop), FadeOut(resident[1]), run_time=0.5)
        complex_ = VGroup(resident[0],tag,receptor,coat)
        self.play(complex_.animate.shift(LEFT*7.85), run_time=1.2)
        neutral = T("near-neutral: releases",26,TEXT).move_to([-4.4,-2.8,0])
        self.at("conditions let them go")
        self.play(FadeOut(coat), resident[0].animate.shift(LEFT*0.65),
                  tag.animate.shift(LEFT*0.65), FadeIn(neutral), run_time=0.6)
        inset = VGroup(golgi_stack()).scale(0.6).move_to([2.6,0,0])
        back = VGroup(arrow([3.4,0.4,0],[2.7,0.4,0],BLUE),
                      arrow([2.5,-0.4,0],[1.8,-0.4,0],BLUE))
        enzyme = Square(side_length=0.16,color=PURPLE,fill_opacity=1).move_to([3.4,0.6,0])
        model = T("One model: enzyme recycling",26,TEXT).move_to([2.3,2.2,0])
        self.at("In one model")
        self.play(FadeOut(taglabel),FadeOut(cop),FadeOut(ph),FadeOut(cargo),
                  FadeOut(later),FadeIn(inset),FadeIn(model),run_time=0.6)
        self.at("Golgi enzymes also")
        self.play(FadeIn(back),FadeIn(enzyme),run_time=0.4)
        self.at("recycle backward")
        self.play(enzyme.animate.shift(LEFT*1.5),run_time=0.8)
        self.finish()


class S05Maturation(SpokenScene):
    def construct(self):
        title=heading("Cisternal maturation")
        sac=RoundedRectangle(width=4.0,height=2.4,corner_radius=0.4,color=BLUE,
                             fill_color=BLUE,fill_opacity=0.12).move_to([-2.8,0.3,0])
        cargo=VGroup(*[dot([-3.35+i*0.55,0.3,0],r=0.12) for i in range(3)])
        early=VGroup(*[Square(side_length=0.2,color=GOLD,fill_opacity=1)
                       .move_to([-3.5+i*0.7,0.8,0]) for i in range(3)])
        key=T("early enzymes",26,GOLD).move_to([-2.8,-1.5,0])
        self.at("In cisternal maturation")
        self.play(FadeIn(title),FadeIn(sac),run_time=0.8)
        self.at("carries cargo")
        self.play(FadeIn(cargo),run_time=0.6)
        self.at("resident enzymes change")
        self.play(FadeIn(early),FadeIn(key),run_time=0.6)
        back=arrow([-1.8,1.8,0],[-5.4,1.8,0],BLUE)
        self.at("Enzymes recycle backward")
        self.play(GrowArrow(back),early.animate.shift(LEFT*2).set_opacity(0),run_time=1.0)
        late=VGroup(*[Square(side_length=0.2,color=PURPLE,fill_opacity=1)
                      .move_to([0.5+i*0.7,0.8,0]) for i in range(3)])
        self.at("sac changes")
        self.play(sac.animate.shift(RIGHT*4),cargo.animate.shift(RIGHT*4),FadeIn(late),
                  Transform(key,T("late enzymes",26,PURPLE).move_to([1.2,-1.5,0])),run_time=1.2)
        yeast=heading("Budding yeast: direct imaging evidence")
        scattered=VGroup(*[RoundedRectangle(width=1.2,height=0.55,corner_radius=0.2,color=BLUE,
                         fill_color=BLUE,fill_opacity=0.1).move_to(p)
                         for p in ([-4.5,-1.6,0],[4.6,1.4,0])])
        self.at("In budding yeast")
        self.play(ReplacementTransform(title,yeast),FadeOut(back),FadeIn(scattered),
                  late.animate.set_color(GOLD),
                  Transform(key,T("early marker",26,GOLD).move_to([1.2,-1.5,0])),run_time=0.7)
        self.at("imaging shows this change")
        self.play(late.animate.set_color(PURPLE),
                  Transform(key,T("late marker",26,PURPLE).move_to([1.2,-1.5,0])),run_time=1.2)
        self.at("cargo staying inside")
        self.play(Indicate(cargo,color=YELLOW),run_time=0.8)
        caveat=T("Mammalian Golgi\nNo single model explains every observation",26,TEXT,
                  line_spacing=0.8).move_to([-1.0,-2.65,0])
        stack=golgi_stack().scale(0.45).move_to([4.7,-2.65,0])
        self.at("Maturation is a leading framework")
        self.play(FadeOut(scattered),FadeOut(key),
                  Transform(yeast,heading("Maturation: a leading framework")),run_time=0.5)
        self.at("no single model")
        self.play(FadeIn(caveat),FadeIn(stack),run_time=0.8)
        self.finish()


class S06Exits(SpokenScene):
    def construct(self):
        tgn=chip("trans-Golgi\nnetwork",BLUE,size=28).move_to([-4.7,0,0])
        surface=VGroup(Line([5.2,-2.4,0],[5.2,2.4,0],color=BLUE,stroke_width=6),
                       T("cell surface",24,BLUE).move_to([5.1,3.0,0]))
        branches=VGroup(arrow([-3.2,0.1,0],[4.9,1.4,0]),arrow([-3.2,-0.1,0],[0.6,-1.4,0]))
        self.at("At the")
        self.play(FadeIn(tgn),FadeIn(surface),run_time=0.6)
        self.at("split")
        self.play(Create(branches),run_time=0.7)
        direct=T("constitutive secretion",28,YELLOW).move_to([0.3,2.65,0])
        flow=VGroup(*[dot([-2.6+i*1.9,0.3+i*0.3,0],r=0.13) for i in range(3)])
        self.at("Constitutive secretion")
        self.play(FadeIn(direct),FadeIn(flow),run_time=0.5)
        self.at("as fast as")
        self.play(*[d.animate.move_to([5.8,1.1+i*0.3,0]) for i,d in enumerate(flow)],run_time=1.2)
        nearly=T("nearly every eukaryotic cell",24,GREY).move_to([0.2,3.35,0])
        self.at("Nearly every")
        self.play(FadeIn(nearly),run_time=0.6)
        gran=Circle(radius=0.65,color=BLUE,fill_color=BLUE,fill_opacity=0.12).move_to([1.4,-1.4,0])
        packed=VGroup(*[dot([1.15+i*0.25,-1.5+j*0.25,0],r=0.09) for j in range(2) for i in range(3)])
        store=T("specialized cells: storage",26,GREY).move_to([0.5,-3.25,0])
        reg=T("regulated secretion",28,YELLOW).move_to([0.5,-2.6,0])
        self.at("Specialized cells")
        self.play(FadeOut(flow),FadeIn(gran),FadeIn(packed),FadeIn(store),FadeIn(reg),run_time=0.5)
        self.at("store cargo")
        self.play(Indicate(packed,color=YELLOW),run_time=0.7)
        stim=chip("stimulus",TEXT,size=26).move_to([2.8,0,0])
        self.at("a stimulus triggers")
        self.play(FadeIn(stim),gran.animate.move_to([4.35,-1.4,0]),packed.animate.shift(RIGHT*2.95),run_time=0.6)
        self.play(FadeOut(gran),*[d.animate.move_to([5.8+i*0.05,-1.8+i*0.15,0]) for i,d in enumerate(packed)],run_time=0.65)
        self.at("That is regulated secretion")
        self.play(FadeOut(store),FadeOut(stim),Indicate(reg,color=YELLOW),run_time=0.5)
        # A separate inset returns to the immature stage when sorting is mentioned.
        self.at("Sorting can continue")
        self.play(FadeOut(packed),FadeOut(branches),FadeOut(tgn),FadeOut(direct),FadeOut(nearly),
                  FadeOut(surface),FadeOut(reg),run_time=0.35)
        immature=VGroup(Circle(radius=0.62,color=BLUE,fill_opacity=0.12),
                       *[dot([-0.25+i*0.25,0,0],r=0.1) for i in range(3)]).move_to([0,0.6,0])
        sortlabel=T("immature granule: sorting continues",26,TEXT).move_to([0,2.5,0])
        self.play(FadeIn(immature),FadeIn(sortlabel),run_time=0.35)
        self.play(immature[3].animate.shift(RIGHT*1.2),run_time=0.45)
        whole=route_diagram(); back=recycling()
        self.play(FadeOut(immature),FadeOut(sortlabel),FadeIn(whole),FadeIn(back),run_time=0.7)
        self.finish()


class S04Endoh(SpokenScene):
    def construct(self):
        route=route_diagram().set_opacity(0.5)
        # Keep the route visible without competing background text in the assay inset.
        for i in (0,1,2,3,4):
            route[i][1].set_opacity(0)
        back=recycling().set_opacity(0.5)
        self.add(route,back)
        panel=RoundedRectangle(width=12.5,height=5.1,corner_radius=0.25,
                               stroke_color=GREY,fill_color=BG,fill_opacity=0.8).move_to([0,0,0])
        title=heading("Smaller point: Endo H assay")
        proteins=VGroup(*[protein(k,[x,-0.4,0],1.8) for k,x in zip(("core","core","complex"),(-4,0,4))])
        labels=VGroup(*[T(t,26,c).move_to([x,-1.5,0]) for t,c,x in
                       (("high-mannose",ORANGE,-4),("hybrid",ORANGE,0),("complex",GREEN,4))])
        # These are the same schematic sugar-chain knobs used throughout the old film.
        self.at("A smaller point")
        self.play(FadeIn(panel),FadeIn(title),FadeIn(proteins),FadeIn(labels),run_time=0.8)
        scissors=VGroup(Line([-0.25,-0.2,0],[0.25,0.2,0],color=TEAL,stroke_width=5),
                        Line([-0.25,0.2,0],[0.25,-0.2,0],color=TEAL,stroke_width=5),
                        Circle(radius=0.12,color=TEAL).move_to([-0.34,-0.26,0]),
                        Circle(radius=0.12,color=TEAL).move_to([-0.34,0.26,0])).move_to([-4,-0.05,0])
        self.at("It cuts")
        self.play(FadeIn(scissors),run_time=0.25)
        self.play(proteins[0][1].animate.shift(UP*0.6).set_opacity(0),run_time=0.45)
        self.at("and hybrid")
        self.play(scissors.animate.move_to([0,-0.05,0]),run_time=0.3)
        self.play(proteins[1][1].animate.shift(UP*0.6).set_opacity(0),run_time=0.45)
        spared=T("not cut",26,GREEN).move_to([4,1.5,0])
        self.at("but not complex")
        self.play(scissors.animate.move_to([4.8,-0.05,0]),FadeIn(spared),run_time=0.7)
        history=T("Past: relevant Golgi enzymes have acted",28,GREEN).move_to([0,-2.9,0])
        self.at("Resistance records passage")
        self.play(FadeOut(scissors),FadeIn(history),Indicate(proteins[2][1],color=GREEN),run_time=0.8)
        location=T("Current location?",30,TEXT).move_to([0,2.05,0])
        self.at("It does not tell")
        self.play(FadeIn(location),run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Cargo moves ER to Golgi to release, at once or after storage."
