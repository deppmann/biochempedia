"""Hox genes and the hindbrain: a gradient writes the address  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  ORANGE = retinoic acid (the drug, the drops, the gradient, the dose)
  GREEN  = made / switched on (Raldh2, a gene that is on, the right dose)
  RED    = destroyed / harmful (Cyp26, the wrong dose)
  BLUE   = the retinoic acid receptors (RAR, RXR)
  PURPLE = Hox genes and the Hox code (four shades = four gene groups; seven abstract shades = each rhombomere's mix)
  GOLD   = the short DNA stretch the receptor pair binds
  TEAL   = trigeminal identity (jaw, chewing)
  YELLOW = facial identity (face, facial expression)
  GREY   = bulges, DNA, nucleus, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
HOX = ["#DCC8F4", "#C39EE6", "#A573CF", "#8650B8"]   # four Hox gene groups, 3' to 5'

# one shared hindbrain strip, same place in every scene that shows it
SX = [-4.8 + 1.6 * i for i in range(7)]   # bulge centres
SY, SH, SW = 0.0, 3.0, 1.5
TAGY = -2.3


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def recolor(c, color):
    return [c[1].animate.set_stroke(color).set_fill(color, 0.16), c[2].animate.set_color(color)]


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bulge(i, fill=GREY, op=0.15, h=SH, y=SY):
    return RoundedRectangle(corner_radius=0.3, width=SW, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=fill, fill_opacity=op).move_to([SX[i], y, 0])


def strip(op=0.15, h=SH, y=SY):
    return VGroup(*[bulge(i, op=op, h=h, y=y) for i in range(7)])


def rlabels(bs, size=24):
    return VGroup(*[T(f"r{i + 1}", size, GREY).move_to(b.get_top() + DOWN * 0.38) for i, b in enumerate(bs)])


def front_back(y):
    f = T("front", 24, GREY).move_to([SX[0], y, 0])
    b = T("back", 24, GREY).move_to([SX[6], y, 0])
    return VGroup(f, b)


def tag(i, y=TAGY, pat=None):
    box = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=1.15, height=0.8, stroke_color=GREY, stroke_width=2.5),
                         num_dashes=30)
    g = VGroup(box)
    if pat is None:
        g.add(T("?", 34, GREY))
    else:
        for j, on in enumerate(pat):
            sq = Square(0.24, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.9 if on else 0.0)
            g.add(sq.move_to([-0.34 + 0.34 * j, 0, 0]))
    return g.move_to([SX[i], y, 0])


# Abstract "mix" tags: each rhombomere gets its own purple shade. The shades stand for
# "a different combination", not for any particular set of Hox genes.
MIX = ["#EDE2FA", "#D7C1F0", "#C1A0E6", "#AB80DB", "#9461CC", "#7C46B5", "#64339A"]


def pat_tag(i, shade_of=None, y=TAGY):
    k = i if shade_of is None else shade_of
    box = RoundedRectangle(corner_radius=0.12, width=1.15, height=0.8, stroke_color=PURPLE, stroke_width=2.5,
                           fill_color=MIX[k], fill_opacity=0.9)
    return box.move_to([SX[i], y, 0])


def drop(color=ORANGE, r=0.14):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1)


def curve_pts(x0=-5.55, x1=5.55, base=1.9, peak=3.3, power=1.8, n=40):
    xs = np.linspace(x0, x1, n)
    t = (xs - x0) / (x1 - x0)
    return [np.array([x, base + (peak - base) * tt ** power, 0]) for x, tt in zip(xs, t)]


def curve_mobs(pts, base=1.9):
    line = VMobject(stroke_color=ORANGE, stroke_width=6)
    line.set_points_smoothly(pts)
    poly = Polygon(*([np.array([pts[0][0], base, 0])] + pts + [np.array([pts[-1][0], base, 0])]),
                   stroke_width=0, fill_color=ORANGE, fill_opacity=0.22)
    return line, poly


class S00Title(TitleCard):
    LESSON = "Hox genes and the hindbrain"
    TITLE = "A Hox Code Gives Each Segment Its Identity"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", 22, TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), 22, GREY)
        title = T(self.TITLE, 54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), run_time=self.beat(0.25))
        self.play(Write(title), GrowFromCenter(rule), run_time=self.beat(0.35))
        self.wait(self.beat(0.2))
        self.play(FadeOut(g), run_time=self.beat(0.2))
        self.finish()



# Shared schematic elements. Marks denote combinations, not measured expression.
def code_marks(i, y=-0.3):
    pats = [(), (0,), (0, 1), (0, 2), (0, 1, 2), (0, 2, 3), (0, 1, 3)]
    return VGroup(*[Square(0.22, stroke_width=2, stroke_color=HOX[k],
                          fill_color=HOX[k], fill_opacity=0.9)
                   .move_to([SX[i] - 0.3 + j * 0.3, y, 0])
                   for j, k in enumerate(pats[i])])


def identity_map():
    bs = strip(h=2.6)
    labs = rlabels(bs)
    marks = VGroup(*[code_marks(i) for i in range(7)])
    return bs, labs, marks


def neuron(color=YELLOW):
    return VGroup(Circle(0.16, color=color, fill_color=color, fill_opacity=1),
                  Line([0.16, 0, 0], [0.6, 0, 0], color=color, stroke_width=4))


def header(text, color=TEXT):
    return T(text, 30, color, weight=BOLD).move_to([0, 3.1, 0])


def motor_key():
    jaw = VGroup(Line([-0.4, 0.18, 0], [-0.22, -0.22, 0], color=TEAL, stroke_width=4),
                 Line([-0.22, -0.22, 0], [0.22, -0.22, 0], color=TEAL, stroke_width=4),
                 Line([0.22, -0.22, 0], [0.4, 0.18, 0], color=TEAL, stroke_width=4)).move_to([-5.2, -2.7, 0])
    face = VGroup(Circle(0.35, color=YELLOW),
                  Dot([-0.12, 0.08, 0], radius=0.035, color=YELLOW),
                  Dot([0.12, 0.08, 0], radius=0.035, color=YELLOW),
                  Arc(radius=0.17, start_angle=PI*1.2, angle=PI*0.6, color=YELLOW)
                  .shift(DOWN*0.04)).move_to([4.6, -2.7, 0])
    return VGroup(jaw, T("trigeminal → jaw", 26, TEAL).move_to([-2.9, -2.7, 0]),
                  T("facial → face", 26, YELLOW).move_to([2.3, -2.7, 0]), face)


class S01Pill(SpokenScene):
    def construct(self):
        bs, labs, marks = identity_map()
        self.add(bs)
        question = header("Similar segments — different neurons?")
        self.at("Why do")
        self.play(FadeIn(question), run_time=0.5)
        code = T("Hox combinations · schematic", 26, PURPLE).move_to([0, 2.1, 0])
        self.at("Each segment carries")
        self.play(FadeIn(marks), FadeIn(code), run_time=0.7)
        krox = bchip("Krox20 + segment genes", GREY, 26).move_to([0, -2.15, 0])
        self.at("working with segment genes")
        self.play(FadeIn(krox), run_time=0.6)
        nt = neuron(TEAL).move_to([SX[1], 0.35, 0])
        nf = neuron(YELLOW).move_to([SX[3], 0.35, 0])
        paths = VGroup(arr([SX[1], 0.5, 0], [-2.4, 1.6, 0], TEAL),
                       arr([SX[3], 0.5, 0], [1.0, 1.6, 0], YELLOW))
        self.at("which neurons it makes")
        self.play(FadeIn(nt), FadeIn(nf), run_time=0.5)
        self.at("where their axons go")
        self.play(*[GrowArrow(a) for a in paths], run_time=0.6)
        key = motor_key()
        self.at("jaw and face movement")
        self.play(FadeOut(krox), run_time=0.3)
        self.play(FadeIn(key), run_time=0.3)
        rh = header("Rhombomeres")
        self.at("The small bulges")
        self.play(Transform(question, rh), FadeIn(labs), FadeOut(paths), run_time=0.6)
        chick = T("chick", 24, GREY).move_to([5.3, 2.1, 0])
        self.at("In chick")
        self.play(FadeIn(chick), run_time=0.4)
        self.at("make trigeminal motor neurons")
        self.play(*[bs[i].animate.set_stroke(TEAL, 5).set_fill(TEAL, 0.22) for i in (1, 2)],
                  FadeIn(neuron(TEAL).move_to([SX[2], 0.35, 0])), run_time=0.7)
        self.at("make facial motor neurons")
        self.play(*[bs[i].animate.set_stroke(YELLOW, 5).set_fill(YELLOW, 0.22) for i in (3, 4)],
                  FadeIn(neuron(YELLOW).move_to([SX[4], 0.35, 0])), run_time=0.7)
        self.finish()


class S05Code(SpokenScene):
    def construct(self):
        title = header("Mouse · Hoxb1 knockout")
        self.add(title)
        # Three segments in each comparison row; segment outlines always survive.
        def row(y):
            boxes = VGroup(*[RoundedRectangle(width=2.6, height=1.35, corner_radius=0.2,
                          stroke_color=GREY, fill_color=GREY, fill_opacity=0.1)
                          .move_to([x, y, 0]) for x in (-2.6, 0.2, 3.0)])
            labels = VGroup(*[T(f"r{k}", 24, GREY).move_to([x, y + 0.4, 0])
                              for k, x in zip((4, 5, 6), (-2.6, 0.2, 3.0))])
            return VGroup(boxes, labels)
        normal, mutant = row(1.35), row(-1.1)
        nl = T("normal", 24, GREY).move_to([-5.0, 1.35, 0])
        ml = T("knockout", 24, GREY).move_to([-5.0, -1.1, 0])
        hox = bchip("Hoxb1", PURPLE, 26).move_to([5.6, 2.55, 0])
        self.at("Test that address")
        self.play(FadeIn(hox), run_time=0.4)
        self.at("removing")
        self.play(hox.animate.set_opacity(0.3), Create(Cross(hox, stroke_color=RED)), run_time=0.5)
        n = neuron().move_to([-2.6, 1.1, 0])
        self.at("Normally")
        self.play(FadeIn(normal), FadeIn(nl), FadeIn(n), run_time=0.6)
        self.at("migrate back")
        self.play(n.animate.move_to([3.0, 1.1, 0]), run_time=1.1)
        nucleus = Ellipse(width=1.3, height=0.65, color=YELLOW).move_to([3.0, 1.1, 0])
        self.play(Create(nucleus), run_time=0.3)
        m = VGroup(neuron().move_to([-2.9, -1.35, 0]), neuron().move_to([-2.1, -1.35, 0]))
        mark = Square(0.22, color=PURPLE, fill_color=PURPLE, fill_opacity=0.9).move_to([-3.4, -1.05, 0])
        self.at("Without")
        self.play(FadeIn(mutant), FadeIn(ml), FadeIn(m), FadeIn(mark), run_time=0.6)
        self.at("loses parts")
        partial = T("r4 code → partly r2-like", 24, PURPLE).move_to([-2.5, -2.2, 0])
        self.play(mark.animate.set_fill(HOX[0]).set_stroke(HOX[0]), FadeIn(partial), run_time=0.6)
        self.at("fail to form or migrate normally")
        self.play(m[0].animate.shift(RIGHT * 1.8 + DOWN * 0.1), run_time=0.8)
        note = T("related mutant outcomes · schematic", 24, GREY).move_to([0, -2.8, 0])
        self.at("Some behave")
        self.play(m[1].animate.set_color(TEAL), FadeIn(note), run_time=0.6)
        failed = T("facial nucleus: abnormal", 24, RED).move_to([2.8, -2.0, 0])
        self.at("The facial motor nucleus")
        self.play(FadeIn(failed), run_time=0.6)
        self.at("The segment is still there")
        self.play(Indicate(mutant[0][0], color=GREY, scale_factor=1.04), run_time=0.8)
        self.at("What changes")
        self.play(Indicate(m, color=TEAL, scale_factor=1.1), run_time=0.7)
        self.finish()


class S08Compartments(SpokenScene):
    def construct(self):
        title = header("Chick · lineage tracing")
        sub = T("schematic clones · later observations", 24, GREY).move_to([0, 2.4, 0])
        self.add(title, sub)
        def panel(x, label):
            frame = RoundedRectangle(width=5.2, height=2.5, corner_radius=0.2, stroke_color=GREY).move_to([x, 0.4, 0])
            border = DashedLine([x, -0.85, 0], [x, 1.65, 0], color=GREY)
            lab = T(label, 25, TEXT).move_to([x, -1.6, 0])
            return VGroup(frame, border, lab)
        before, after = panel(-3.0, "label before boundaries"), panel(3.0, "label after boundaries")
        left = VGroup(*[Dot([-3 + dx, y, 0], radius=0.13, color=PURPLE)
                        for dx, y in [(-0.9, 0.3), (-0.45, 0.8), (0.3, 0.2), (0.7, 0.9)]])
        right = VGroup(*[Dot([3 + dx, y, 0], radius=0.13, color=PURPLE)
                         for dx, y in [(-1.5, 0.3), (-0.8, 0.8), (-1.2, 0.0), (-0.5, 0.2)]])
        self.at("compartments")
        self.play(FadeIn(before), FadeIn(after), run_time=0.6)
        seed = Dot([-3.7, 0.5, 0], radius=0.14, color=PURPLE)
        self.at("descendants of a cell")
        self.play(FadeIn(seed), run_time=0.4)
        self.at("can span")
        self.play(ReplacementTransform(seed, left), run_time=0.8)
        seed2 = Dot([1.8, 0.5, 0], radius=0.14, color=PURPLE)
        self.at("Label a cell after")
        self.play(FadeIn(seed2), run_time=0.4)
        self.at("stay within one")
        self.play(ReplacementTransform(seed2, right), run_time=0.8)
        self.at("Cell sorting")
        self.play(before[1].animate.set_stroke(TEXT, 5), after[1].animate.set_stroke(TEXT, 5), run_time=0.6)
        self.at("In fish and frog")
        self.play(FadeOut(VGroup(before, after, left, right, sub)),
                  Transform(title, header("Fish / frog · contact sorting")), run_time=0.6)
        ca = Circle(0.7, color=GREY, fill_color=GREY, fill_opacity=0.12).move_to([-1.0, 0.3, 0])
        cb = ca.copy().move_to([1.0, 0.3, 0])
        receptor = bchip("EphA4", BLUE, 28).move_to([-3.5, 1.9, 0])
        ligand = bchip("ephrin-B", BLUE, 28).move_to([3.5, 1.9, 0])
        badgea = Square(0.25, color=BLUE, fill_color=BLUE, fill_opacity=0.5).move_to([-0.3, 0.3, 0])
        badgeb = Circle(0.14, color=BLUE, fill_color=BLUE, fill_opacity=0.8).move_to([0.3, 0.3, 0])
        cells = VGroup(ca, cb, badgea, badgeb)
        self.at("receptors")
        self.play(FadeIn(cells), FadeIn(receptor), run_time=0.5)
        self.at("ligands")
        self.play(FadeIn(ligand), run_time=0.5)
        self.at("sorting at contact")
        self.play(VGroup(ca, badgea).animate.shift(RIGHT * 0.15), VGroup(cb, badgeb).animate.shift(LEFT * 0.15), run_time=0.5)
        self.play(VGroup(ca, badgea).animate.shift(LEFT * 1.0), VGroup(cb, badgeb).animate.shift(RIGHT * 1.0), run_time=0.7)
        restrict = T("progenitors: restricted mixing", 28, GREY).move_to([0, -1.4, 0])
        self.at("These borders restrict")
        self.play(FadeIn(restrict), run_time=0.6)
        self.at("Later neurons")
        self.play(FadeOut(VGroup(cells, receptor, ligand)),
                  Transform(title, header("Later facial motor neurons can migrate")), run_time=0.5)
        boxes = VGroup(*[RoundedRectangle(width=2.7, height=1.8, corner_radius=0.2, stroke_color=GREY)
                         .move_to([x, 0.4, 0]) for x in (-2.8, 0, 2.8)])
        labs = VGroup(*[T(f"r{i}", 24, GREY).move_to([x, 1.0, 0]) for i,x in zip((4,5,6),(-2.8,0,2.8))])
        n = neuron().move_to([-2.8, 0.1, 0])
        self.at("can still migrate")
        self.play(FadeIn(boxes), FadeIn(labs), FadeIn(n), run_time=0.4)
        self.play(n.animate.move_to([2.8, 0.1, 0]), run_time=1.0)
        self.finish()


class S02Bath(SpokenScene):
    def construct(self):
        bs = strip(h=2.2, y=-0.1)
        labs = rlabels(bs)
        code = T("Hox code + segment regulators", 26, PURPLE).move_to([0, -1.7, 0])
        fb = front_back(1.3)
        self.add(bs, labs, code, fb)
        ra = header("retinoic acid · from vitamin A", ORANGE)
        self.at("Retinoic acid")
        self.play(FadeIn(ra), run_time=0.6)
        tap = bchip("Raldh2 · makes", GREEN, 26).move_to([3.5, -3.1, 0])
        meso = T("adjacent mesoderm", 24, GREY).move_to([3.5, -2.55, 0])
        up = arr([5.5, -2.7, 0], [5.5, -1.1, 0], GREEN)
        self.at("makes it in mesoderm")
        self.play(FadeIn(tap), FadeIn(meso), GrowArrow(up), run_time=0.7)
        drain = bchip("Cyp26 · destroys", RED, 26).move_to([-3.5, -3.1, 0])
        dn = arr([-3.5, -1.1, 0], [-3.5, -2.7, 0], RED)
        self.at("enzymes destroy it")
        self.play(FadeIn(drain), GrowArrow(dn), run_time=0.6)
        anterior = T("Cyp26a1 · anterior", 26, RED).move_to([-2.0, 1.55, 0])
        self.at("strongly expressed toward the front")
        self.play(FadeIn(anterior), run_time=0.6)
        self.at("tap and drain")
        d = drop(r=0.18).move_to([4.8, 0, 0])
        self.play(FadeIn(d), run_time=0.2)
        self.play(d.animate.move_to([-4.8, 0, 0]), run_time=1.0)
        self.play(FadeOut(d), run_time=0.2)
        line, poly = curve_mobs(curve_pts(base=1.95, peak=2.8), base=1.95)
        self.at("more signal at the back")
        self.play(Create(line), FadeIn(poly),
                  *[bs[i].animate.set_fill(ORANGE, 0.05 + 0.07 * i) for i in range(7)], run_time=0.8)
        self.at("less at the front")
        self.play(Indicate(bs[0], color=ORANGE, scale_factor=1.03), run_time=0.5)
        self.finish()


class S03Read(SpokenScene):
    def construct(self):
        nuc = Ellipse(width=11.6, height=5.9, stroke_color=GREY, stroke_width=4,
                      fill_color=GREY, fill_opacity=0.08)
        nlab = T("nucleus", 24, GREY).move_to([0, -2.55, 0])
        self.add(nuc, nlab)
        d = drop(r=0.26).move_to([-5.7, 2.9, 0])
        self.at("Retinoic acid reaches")
        self.play(FadeIn(d), run_time=0.2)
        self.play(d.animate.move_to([-3.4, 1.4, 0]), run_time=0.6)
        rar = bchip("RAR", BLUE, 30).move_to([-1.5, 1.4, 0])
        self.at("binds")
        self.play(FadeIn(rar), d.animate.move_to([-2.4, 1.4, 0]), run_time=0.5)
        rxr = bchip("RXR", BLUE, 30).next_to(rar, RIGHT, buff=0.12)
        self.at("This receptor works")
        self.play(FadeIn(rxr), run_time=0.6)
        dna = Line([-4.9, -0.7, 0], [4.9, -0.7, 0], color=GREY, stroke_width=6)
        sites = VGroup(*[Rectangle(width=0.7, height=0.3, stroke_color=GOLD,
                    fill_color=GOLD, fill_opacity=0.9).move_to([x, -0.7, 0]) for x in (-3.1, 1.7)])
        response = T("retinoic acid response elements", 26, GOLD).move_to([0, -1.65, 0])
        self.at("on short DNA sequences")
        self.play(Create(dna), FadeIn(sites), run_time=0.6)
        self.at("called retinoic acid response elements")
        self.play(FadeIn(response), VGroup(d, rar, rxr).animate.move_to([-2.7, 0.05, 0]), run_time=0.7)
        genes = VGroup(bchip("Hoxa1", PURPLE, 28).move_to([-1.4, -0.7, 0]),
                       bchip("Hoxb1", PURPLE, 28).move_to([3.4, -0.7, 0]))
        self.at("HoxA1 and HoxB1")
        self.play(FadeIn(genes), run_time=0.5)
        self.at("helps switch on")
        self.play(*[a for g in genes for a in recolor(g, GREEN)], run_time=0.7)
        parallel = VGroup(bchip("FGF", GREY, 26).move_to([1.6, 1.15, 0]),
                          bchip("Wnt", GREY, 26).move_to([3.7, 1.15, 0]))
        arrows = VGroup(arr([1.6, 0.75, 0], [1.6, -0.4, 0]), arr([3.7, 0.75, 0], [3.7, -0.4, 0]))
        self.at("working alongside")
        self.play(FadeIn(parallel), *[GrowArrow(a) for a in arrows], run_time=0.6)
        self.finish()


class S06Dose(SpokenScene):
    def construct(self):
        bs, labs, marks = identity_map()
        self.add(bs, labs, marks)
        title = header("Hox combinations · schematic", PURPLE)
        self.add(title)
        self.at("Change this input")
        self.play(Indicate(marks, color=PURPLE, scale_factor=1.03), run_time=0.7)
        experiment = T("mouse embryos · early excess retinoic acid", 28, ORANGE).move_to([0, 2.2, 0])
        self.at("In mouse embryos")
        self.play(FadeIn(experiment), run_time=0.6)
        extra = VGroup(*[drop(r=0.15).move_to([x, 1.6, 0]) for x in (-4, -2, 0, 2, 4)])
        self.at("extra retinoic acid early")
        self.play(FadeIn(extra), run_time=0.6)
        self.at("Hox domains changed")
        self.play(Transform(marks[1], code_marks(3).move_to(marks[1])),
                  Transform(marks[2], code_marks(4).move_to(marks[2])), run_time=0.8)
        shifts = VGroup(T("r2 → r4-like", 28, PURPLE).move_to([-2.9, -2.3, 0]),
                        T("r3 → r5-like", 28, PURPLE).move_to([2.3, -2.3, 0]))
        self.at("shifted toward the identity")
        self.play(FadeIn(shifts), bs[1].animate.set_stroke(YELLOW, 5), bs[2].animate.set_stroke(YELLOW, 5), run_time=0.7)
        self.at("The signal helps")
        self.play(Transform(title, header("Signal helps set regional identity", PURPLE)), FadeOut(extra), run_time=0.6)
        self.finish()


class S04Order(SpokenScene):
    def construct(self):
        cy = 2.3
        chrom = Line([-5.6, cy, 0], [5.6, cy, 0], color=GREY, stroke_width=5)
        ends = VGroup(T("3′", 30, GREY).move_to([-6.0, cy, 0]), T("5′", 30, GREY).move_to([6.0, cy, 0]))
        xs = [-3.9, -1.3, 1.3, 3.9]
        genes = VGroup(*[Square(0.5, color=c, fill_color=c, fill_opacity=0.9).move_to([x, cy, 0]) for x,c in zip(xs,HOX)])
        title = header("Hox cluster · schematic", PURPLE)
        self.at("The chromosome carries")
        self.play(Create(chrom), FadeIn(ends), FadeIn(genes), FadeIn(title), run_time=0.7)
        axis = arr([-5.4, 0.95, 0], [5.5, 0.95, 0])
        fb = front_back(1.4)
        edges = [-4.4, -2.0, 0.4, 2.8]
        bars = VGroup(*[Rectangle(width=5.3-x, height=0.4, stroke_width=0, fill_color=HOX[k], fill_opacity=0.9)
                  .move_to([(x+5.3)/2, 0.3-k*0.65, 0]) for k,x in enumerate(edges)])
        self.at("farthest forward")
        self.play(GrowArrow(axis), FadeIn(fb), GrowFromEdge(bars[0], LEFT), run_time=0.7)
        self.at("front edges farther back")
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars[1:]], lag_ratio=0.2), run_time=1.0)
        timing = T("mouse + chick · activation time", 26, GREY).move_to([0, -0.5, 0])
        timeline = arr([-4.8, -1.7, 0], [4.8, -1.7, 0])
        timewords = VGroup(T("first · 3′", 26, HOX[0]).move_to([-4.0, -2.5, 0]),
                          T("later · 5′", 26, HOX[3]).move_to([4.0, -2.5, 0]))
        lights = VGroup(*[Square(0.5, color=HOX[k], fill_color=HOX[k], fill_opacity=0.15)
                            .move_to([xs[k], -1.7, 0]) for k in range(4)])
        self.at("In mouse and chick")
        self.play(FadeOut(VGroup(axis, fb, bars)), FadeIn(timing), GrowArrow(timeline), FadeIn(lights), run_time=0.7)
        self.at("switch on first")
        self.play(lights[0].animate.set_fill(HOX[0], 1), FadeIn(timewords[0]), run_time=0.6)
        self.at("genes later")
        self.play(LaggedStart(*[s.animate.set_fill(HOX[k], 1) for k,s in enumerate(lights) if k], lag_ratio=0.2),
                  FadeIn(timewords[1]), run_time=0.9)
        self.at("This is")
        self.play(Transform(title, header("Colinearity · position and timing", PURPLE)), run_time=0.6)
        self.at("along the growing body")
        self.play(FadeOut(VGroup(chrom, ends, genes, timing, timeline, timewords, lights)), run_time=0.4)
        bs, labs, marks = identity_map()
        for i in (1,2):
            bs[i].set_stroke(TEAL, 4)
        for i in (3,4):
            bs[i].set_stroke(YELLOW, 4)
        self.play(FadeIn(bs), FadeIn(labs), FadeIn(marks), FadeIn(motor_key()), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "A Hox code gives each segment its identity."

    def construct(self):
        bs, labs, marks = identity_map()
        for i in (1, 2):
            bs[i].set_stroke(TEAL, 4)
        for i in (3, 4):
            bs[i].set_stroke(YELLOW, 4)
        self.add(bs, labs, marks, motor_key())
        line = T(self.LINE, size=36, font=TITLE_FONT).move_to([0, 3.1, 0])
        fit(line, max_w=12.6)
        self.play(FadeIn(line), run_time=self.beat(0.3))
        self.finish()
