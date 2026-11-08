"""Cancer as a genetic disease: acquired changes and clonal evolution  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  RED    = the broken (mutant) copy of RB1, a hit
  GREEN  = the working copy of RB1
  YELLOW = the second hit as an event (the thing that strikes)
  ORANGE = a tumor: a tumor cell, a tumor in an eye, an affected person
  TEAL   = a probability with no tumor / numbers that are computed
  BLUE   = a pre-existing treatment-resistant subline
  GREY   = outlines, axes, healthy cells, labels; passenger markers
"""
import numpy as np
from math import exp, factorial
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def cell(center, s=1.0, l=RED, r=GREEN, outline=GREY, fill=0.0):
    """A cell as a rounded square holding the two copies of RB1 as two small bars."""
    center = np.array(center, float)
    box = RoundedRectangle(corner_radius=0.12 * s, width=s, height=s, stroke_color=outline, stroke_width=3,
                           fill_color=outline, fill_opacity=fill).move_to(center)
    lb = RoundedRectangle(corner_radius=0.05 * s, width=0.14 * s, height=0.58 * s, stroke_width=0,
                          fill_color=l, fill_opacity=1).move_to(center + LEFT * 0.17 * s)
    rb = RoundedRectangle(corner_radius=0.05 * s, width=0.14 * s, height=0.58 * s, stroke_width=0,
                          fill_color=r, fill_opacity=1).move_to(center + RIGHT * 0.17 * s)
    g = VGroup(box, lb, rb)
    g.box, g.lb, g.rb = box, lb, rb
    return g


def tumorize(c):
    """animations: the working copy is hit, the cell becomes a tumor cell."""
    return [c.rb.animate.set_fill(RED, 1), c.box.animate.set_stroke(ORANGE).set_fill(ORANGE, 0.4)]


def grid_cells(rows=4, cols=9, pitch=1.3, cy=-0.3, s=1.0):
    cells = []
    for i in range(rows):
        for j in range(cols):
            x = (j - (cols - 1) / 2) * pitch
            y = cy + ((rows - 1) / 2 - i) * pitch
            cells.append(cell([x, y, 0], s))
    return cells


def legend(y=-3.42):
    a = RoundedRectangle(corner_radius=0.03, width=0.11, height=0.4, stroke_width=0, fill_color=RED, fill_opacity=1)
    ta = T("broken copy", 22, RED)
    b = RoundedRectangle(corner_radius=0.03, width=0.11, height=0.4, stroke_width=0, fill_color=GREEN, fill_opacity=1)
    tb = T("working copy", 22, GREEN)
    sq = RoundedRectangle(corner_radius=0.06, width=0.4, height=0.4, stroke_color=ORANGE, stroke_width=3,
                          fill_color=ORANGE, fill_opacity=0.4)
    tc = T("tumor cell", 22, ORANGE)
    g = VGroup(VGroup(a, ta).arrange(RIGHT, buff=0.15), VGroup(b, tb).arrange(RIGHT, buff=0.15),
               VGroup(sq, tc).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.8)
    return g.move_to([0, y, 0])


def hit_dot():
    return Circle(radius=0.14, stroke_width=0, fill_color=YELLOW, fill_opacity=1)


def eye(center, tumor=False, s=1.0):
    center = np.array(center, float)
    body = Ellipse(width=1.3 * s, height=0.78 * s, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(center)
    iris = Circle(radius=0.2 * s, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to(center)
    g = VGroup(body, iris)
    if tumor:
        dot = Circle(radius=0.14 * s, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to(center + RIGHT * 0.38 * s + DOWN * 0.03 * s)
        g.add(dot)
    return g


def eyes(center, tl, tr, s=1.0):
    center = np.array(center, float)
    return VGroup(eye(center + LEFT * 0.85 * s, tl, s), eye(center + RIGHT * 0.85 * s, tr, s))


def bracket(x0, x1, y, color, tick=0.18):
    return VGroup(Line([x0, y - tick, 0], [x0, y, 0], color=color, stroke_width=4),
                  Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=4),
                  Line([x1, y, 0], [x1, y - tick, 0], color=color, stroke_width=4))


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pedigree():
    S = 0.62

    def sym(x, y, sq, aff):
        col = ORANGE if aff else GREY
        if sq:
            s = Square(side_length=S, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.9 if aff else 0)
        else:
            s = Circle(radius=S / 2, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.9 if aff else 0)
        return s.move_to([x, y, 0])

    yI, yII, yIII = 2.3, 0.5, -1.4
    f = sym(-4.6, yI, True, True)
    mo = sym(-2.9, yI, False, False)
    m1 = Line(f.get_right(), mo.get_left(), color=GREY, stroke_width=3)
    mid1 = (f.get_right() + mo.get_left()) / 2
    kx = [-5.8, -4.3, -2.8]
    ks = [sym(kx[0], yII, True, True), sym(kx[1], yII, False, False), sym(kx[2], yII, False, True)]
    sib = Line([kx[0], yII + 0.95, 0], [kx[2], yII + 0.95, 0], color=GREY, stroke_width=3)
    d1 = Line(mid1, [mid1[0], yII + 0.95, 0], color=GREY, stroke_width=3)
    drops = VGroup(*[Line([x, yII + 0.95, 0], [x, yII + 0.31, 0], color=GREY, stroke_width=3) for x in kx])
    p = sym(-1.3, yII, True, False)
    m2 = Line(ks[2].get_right(), p.get_left(), color=GREY, stroke_width=3)
    mid2 = (ks[2].get_right() + p.get_left()) / 2
    gx = [-2.8, -1.3]
    gk = [sym(gx[0], yIII, False, True), sym(gx[1], yIII, True, False)]
    sib2 = Line([gx[0], yIII + 0.95, 0], [gx[1], yIII + 0.95, 0], color=GREY, stroke_width=3)
    d2 = Line(mid2, [mid2[0], yIII + 0.95, 0], color=GREY, stroke_width=3)
    drops2 = VGroup(*[Line([x, yIII + 0.95, 0], [x, yIII + 0.31, 0], color=GREY, stroke_width=3) for x in gx])
    ped = VGroup(f, mo, m1, d1, sib, drops, *ks, p, m2, d2, sib2, drops2, *gk)
    return ped

def heading(text, color=TEXT):
    return T(text, 34, color, font=TITLE_FONT).move_to([0, 3.15, 0])


def copy_key(y=-3.1):
    return VGroup(chip("altered copy", RED, 24), chip("working copy", GREEN, 24)).arrange(RIGHT, buff=0.6).move_to([0, y, 0])


def lineage():
    """Seven schematic body cells; bars represent DNA regions, not molecules."""
    pts = [(-4.8, 0), (-1.8, 1.35), (-1.8, -1.35), (1.7, 2), (1.7, 0.65), (1.7, -0.65), (1.7, -2)]
    nodes = VGroup(*[cell([x, y, 0], 0.95, RED, GREEN, ORANGE, 0.12) for x, y in pts])
    links = VGroup(*[arr(nodes[a].get_right(), nodes[b].get_left(), GREY, 3)
                     for a, b in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]])
    return nodes, links


def chromosome_pair(mode="normal"):
    """Abstract chromosome bars with a labelled RB1 region; no molecular geometry."""
    pair = VGroup()
    for x, col in [(-0.45, RED), (0.45, GREEN)]:
        stem = RoundedRectangle(width=0.24, height=2.2, corner_radius=0.08,
                                stroke_color=GREY, fill_color=GREY, fill_opacity=0.3).move_to([x, 0, 0])
        region = Rectangle(width=0.34, height=0.55, stroke_width=0, fill_color=col, fill_opacity=1).move_to([x, 0.35, 0])
        pair.add(VGroup(stem, region))
    if mode == "deletion":
        pair[1][0].become(VGroup(
            RoundedRectangle(width=0.24, height=1.17, corner_radius=0.04,
                             stroke_color=GREY, fill_color=GREY, fill_opacity=0.3).move_to([0.45, -0.515, 0]),
            RoundedRectangle(width=0.24, height=0.47, corner_radius=0.04,
                             stroke_color=GREY, fill_color=GREY, fill_opacity=0.3).move_to([0.45, 0.865, 0])))
        pair[1][1].set_opacity(0)
        pair.add(DashedLine([0.45, 0.07, 0], [0.45, 0.63, 0], color=YELLOW, stroke_width=4))
    elif mode == "loss":
        pair[1].set_opacity(0)
    elif mode == "recombination":
        pair[1][1].set_fill(RED, 1)
    return pair


class S00Title(TitleCard):
    LESSON = "Cancer as a genetic disease"
    TITLE = "Cancer as a Genetic Disease"

    def construct(self):
        title = T(self.TITLE, 46, font=TITLE_FONT).move_to([0, 2.3, 0])
        brand = T("BIOCHEMISTRYPEDIA", 22, TEAL).move_to([0, 3.2, 0])
        nodes = VGroup(cell([-3, -0.8, 0], 1.1, GREEN, GREEN),
                       cell([0, -0.8, 0], 1.1, RED, GREEN),
                       cell([3, -0.8, 0], 1.1, RED, GREEN))
        links = VGroup(arr(nodes[0].get_right(), nodes[1].get_left()), arr(nodes[1].get_right(), nodes[2].get_left()))
        label = T("acquired DNA change → daughter cells", 26, GREY).move_to([0, -2.4, 0])
        self.play(FadeIn(brand), Write(title), run_time=0.8)
        self.play(FadeIn(nodes[0]), run_time=0.3)
        self.play(GrowArrow(links[0]), FadeIn(nodes[1]), run_time=0.5)
        self.play(GrowArrow(links[1]), FadeIn(nodes[2]), FadeIn(label), run_time=0.5)
        self.finish()


class S08Acquired(SpokenScene):
    def construct(self):
        c = cell([0, 0, 0], 2.6, GREEN, GREEN)
        head = heading("Altered DNA in a body cell")
        self.at("Cancer is a genetic disease")
        self.play(FadeIn(head), FadeIn(c), run_time=0.6)
        self.at("most changes")
        note = T("most tumor changes are acquired", 28, GREY).move_to([0, -2.5, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.at("They arise")
        somatic = T("somatic: arises during life", 28, RED).move_to([0, -2.5, 0])
        self.play(c.lb.animate.set_fill(RED, 1), ReplacementTransform(note, somatic), run_time=0.7)
        self.at("Some changes switch on")
        on = chip("growth drive: ON", RED, 28).move_to([-3.7, 0.3, 0])
        self.play(c.animate.move_to([0, 0.3, 0]).scale(0.65), FadeIn(on), run_time=0.6)
        self.at("Others switch off")
        off = chip("restraint: OFF", RED, 28).move_to([3.7, 0.3, 0])
        self.play(FadeIn(off), run_time=0.6)
        self.at("cells divide more")
        self.play(FadeOut(on), FadeOut(off), c.animate.move_to([0, 1.4, 0]), run_time=0.6)
        self.at("their descendants expand")
        daughters = VGroup(*[cell([x, -0.8, 0], 1.25, RED, GREEN) for x in (-3, 0, 3)])
        arrows = VGroup(*[arr(c.get_bottom(), d.get_top()) for d in daughters])
        inheritance = T("daughter cells receive the altered DNA", 28, RED).move_to([0, -2.6, 0])
        self.play(FadeOut(somatic), *[GrowArrow(a) for a in arrows],
                  *[TransformFromCopy(c, d) for d in daughters], FadeIn(inheritance), run_time=0.8)
        self.finish()


class S09GeneClasses(SpokenScene):
    def construct(self):
        left = cell([-3.4, 0.5, 0], 2.2, RED, GREEN)
        right = cell([3.4, 0.5, 0], 2.2, RED, GREEN)
        lh = T("oncogene", 32, RED).move_to([-3.4, 2.4, 0])
        rh = T("tumor suppressor", 32, GREEN).move_to([3.4, 2.4, 0])
        accelerator = arr([-4.5, -1.3, 0], [-2.3, -1.3, 0], RED)
        state_l = T("accelerator stuck ON", 26, RED).move_to([-3.4, -2.1, 0])
        self.at("An oncogene")
        self.play(FadeIn(lh), FadeIn(left), GrowArrow(accelerator), FadeIn(state_l), run_time=0.7)
        self.at("One altered copy")
        enough = T("usually: one altered copy suffices", 24, RED).move_to(state_l)
        self.play(Indicate(left.lb, color=RED), ReplacementTransform(state_l, enough), run_time=0.6)
        self.at("A tumor suppressor")
        brake = Line([2.3, -1.3, 0], [4.5, -1.3, 0], color=GREEN, stroke_width=10)
        state_r = T("usually: one working holds", 26, GREEN).move_to([3.4, -2.1, 0])
        self.play(FadeIn(rh), FadeIn(right), Create(brake), run_time=0.6)
        self.at("One working copy")
        self.play(FadeIn(state_r), Indicate(right.rb, color=GREEN), run_time=0.6)
        self.at("both copies normally")
        failed = T("normally: both lose function", 26, RED).move_to(state_r)
        self.play(right.rb.animate.set_fill(RED, 1), FadeOut(brake), ReplacementTransform(state_r, failed), run_time=0.7)
        self.at("These are useful rules")
        qualifier = T("Usually — these rules have exceptions", 28, YELLOW).move_to([0, -3.15, 0])
        self.play(FadeIn(qualifier), run_time=0.5)
        self.finish()


class S10Selection(SpokenScene):
    def construct(self):
        nodes, links = lineage()
        VGroup(nodes, links).shift(RIGHT * 1.55)
        head = heading("Usually a clone: one cell's descendants")
        self.at("A tumor is usually")
        self.play(FadeIn(head), FadeIn(nodes[0]), run_time=0.5)
        self.at("the descendants")
        self.play(Create(links), FadeIn(nodes[1:]), run_time=0.8)
        self.at("More changes accumulate")
        self.play(nodes[1].rb.animate.set_fill(RED, 1), run_time=0.5)
        self.at("A driver gives")
        driver = T("driver: selective advantage", 26, RED).move_to([0, -2.9, 0])
        driver_marks = VGroup(*[Dot(nodes[i].get_center() + UP * 0.44, radius=0.13, color=RED)
                               for i in (1, 3, 4)])
        for i in (3, 4):
            nodes[i].rb.set_fill(RED, 1)
        self.play(FadeIn(driver), FadeIn(driver_marks),
                  *[nodes[i].animate.scale(1.12) for i in (3, 4)], run_time=0.7)
        self.at("A passenger gives")
        passenger = T("passenger: no advantage; carried along", 26, GREY).move_to(driver)
        marks = VGroup(*[Dot(nodes[i].get_center() + DOWN * 0.29, radius=0.07, color=GREY) for i in (1, 3, 4)])
        self.play(ReplacementTransform(driver, passenger), FadeIn(marks), run_time=0.6)
        self.at("clone expands")
        self.play(Indicate(driver_marks, color=RED, scale_factor=1.12), run_time=0.6)
        self.at("Mutation supplies variants")
        variant = T("different sublines", 28, TEXT).move_to(passenger)
        resistant = T("resistant subline", 24, BLUE).next_to(nodes[6], RIGHT, buff=0.25)
        self.play(ReplacementTransform(passenger, variant), nodes[6].box.animate.set_stroke(BLUE),
                  FadeIn(resistant), run_time=0.6)
        self.at("Selection favors")
        favored = T("divide more or die less", 28, ORANGE).move_to(variant)
        self.play(ReplacementTransform(variant, favored), Indicate(nodes[3:5], color=ORANGE), run_time=0.6)
        self.at("A resistant subline")
        self.play(Indicate(nodes[6], color=BLUE), run_time=0.5)
        self.at("survive treatment")
        treatment = heading("Treatment selects a surviving subline", BLUE)
        self.play(ReplacementTransform(head, treatment), FadeOut(marks), FadeOut(driver_marks),
                  *[FadeOut(nodes[i]) for i in range(6)], FadeOut(links), run_time=0.7)
        self.at("and expand")
        survivors = VGroup(*[cell([x, y, 0], 0.95, RED, GREEN, BLUE, 0.2)
                              for x, y in [(1.6, -0.2), (3.25, 0.5), (4.9, -0.2)]])
        expansion_links = VGroup(*[arr(nodes[6].get_top(), c.get_bottom(), BLUE, 3) for c in survivors])
        self.play(*[TransformFromCopy(nodes[6], c) for c in survivors],
                  *[GrowArrow(a) for a in expansion_links], FadeOut(resistant),
                  FadeOut(favored), run_time=0.7)
        self.at("so treatment can fail")
        self.play(FadeIn(T("the resistant subline expands", 28, BLUE).move_to([0, -3, 0])), run_time=0.5)
        self.finish()


class S01Puzzle(SpokenScene):
    def construct(self):
        big = cell([0, 0.2, 0], 2.6)
        head = heading("RB1: inherited risk")
        self.at("shows how inherited risk")
        self.play(FadeIn(head), FadeIn(big), run_time=0.6)
        self.at("A child inherits")
        cells = VGroup(*grid_cells(rows=2, cols=3, pitch=2.2, cy=0.15, s=1.4))
        self.play(ReplacementTransform(big, cells), FadeIn(copy_key()), run_time=0.8)
        self.at("only a few retinal cells")
        candidate = SurroundingRectangle(cells[1], color=YELLOW, buff=0.12)
        question = T("a few retinal cells: later second hit?", 28, YELLOW).move_to([0, -2.1, 0])
        self.play(Create(candidate), FadeIn(question), run_time=0.6)
        self.at("One working copy")
        brake = heading("RB1: one working copy usually provides the brake", GREEN)
        self.play(ReplacementTransform(head, brake), Indicate(cells[1].rb, color=GREEN), run_time=0.7)
        self.finish()


class S02Second(SpokenScene):
    def construct(self):
        cells = VGroup(*grid_cells(rows=2, cols=3, pitch=2.2, cy=0.15, s=1.4))
        head = heading("RB1: inherited first hit")
        self.add(cells, head, copy_key())
        self.at("The inherited change")
        self.play(Indicate(cells[1].lb, color=RED), run_time=0.5)
        self.at("A rare second hit")
        dot = hit_dot().move_to(cells[1].rb.get_center() + UP * 0.9)
        self.play(FadeIn(dot), run_time=0.2)
        self.play(dot.animate.move_to(cells[1].rb), run_time=0.4)
        self.at("removes the working")
        self.play(*tumorize(cells[1]), FadeOut(dot), run_time=0.6)
        self.at("Often this is")
        pair = chromosome_pair().move_to([0, 0.2, 0])
        loh = heading("RB1: loss of heterozygosity")
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not head],
                  ReplacementTransform(head, loh), FadeIn(pair), run_time=0.7)
        self.at("keeps only the mutant")
        label = T("working allele lost; mutant allele retained", 28, RED).move_to([0, -2.7, 0])
        self.play(Transform(pair, chromosome_pair("loss").move_to(pair)), FadeIn(label), run_time=0.5)
        # Each route begins from the original heterozygote: they are alternatives.
        self.at("Deletion")
        deletion = chromosome_pair("deletion").move_to([-4.2, 0.1, 0])
        dl = T("deletion", 26, YELLOW).move_to([-4.2, -1.6, 0])
        deletion_start = chromosome_pair().move_to([-4.2, 0.1, 0])
        routes = T("alternative second-hit routes", 26, GREY).move_to([0, 2.2, 0])
        self.play(ReplacementTransform(pair, deletion_start), FadeIn(dl), FadeIn(routes), FadeOut(label), run_time=0.2)
        self.play(Transform(deletion_start, deletion), run_time=0.3)
        self.at("chromosome loss")
        loss = chromosome_pair("loss").move_to([0, 0.1, 0])
        ll = T("chromosome loss", 26, YELLOW).move_to([0, -1.6, 0])
        before_loss = chromosome_pair().move_to(loss)
        self.play(FadeIn(before_loss), FadeIn(ll), run_time=0.2)
        self.play(Transform(before_loss, loss), run_time=0.4)
        self.at("mitotic recombination")
        recomb = chromosome_pair().move_to([4.2, 0.1, 0])
        rl = T("mitotic recombination", 24, YELLOW).move_to([4.2, -1.6, 0])
        self.play(FadeIn(recomb), FadeIn(rl), run_time=0.3)
        self.play(Transform(recomb, chromosome_pair("recombination").move_to(recomb)), run_time=0.5)
        note = T("two mutant regions\nboth chromosomes retained", 22, RED).move_to([4.2, -2.5, 0])
        self.at("can supply that")
        self.play(FadeIn(note), run_time=0.4)
        self.finish()


class S05Sporadic(SpokenScene):
    def construct(self):
        self.add(heading("RB1: two pathways to loss of the brake"))
        inherited = VGroup(cell([-1.8, 1.4, 0], 1.1), cell([2.2, 1.4, 0], 1.1, RED, RED, ORANGE, 0.3))
        ia = arr(inherited[0].get_right(), inherited[1].get_left(), YELLOW)
        il = T("inherited first hit", 24, RED).move_to([-4.4, 1.4, 0])
        self.add(inherited, ia, il)
        normal = cell([-1.8, -0.7, 0], 1.1, GREEN, GREEN)
        nl = T("nonhereditary", 24, GREY).move_to([-4.4, -0.7, 0])
        self.at("Without a germline")
        self.play(FadeIn(normal), FadeIn(nl), run_time=0.5)
        self.at("both hits must arise")
        middle = cell([0.2, -0.7, 0], 1.1)
        end = cell([2.2, -0.7, 0], 1.1, RED, RED, ORANGE, 0.3)
        aa = arr(normal.get_right(), middle.get_left(), YELLOW)
        ab = arr(middle.get_right(), end.get_left(), YELLOW)
        self.play(GrowArrow(aa), TransformFromCopy(normal, middle), run_time=0.5)
        self.play(GrowArrow(ab), TransformFromCopy(middle, end), run_time=0.5)
        self.at("same body cell")
        self.play(Indicate(VGroup(normal, middle, end), color=YELLOW), run_time=0.6)
        self.at("These tumors tend")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.3)
        ee = eyes([0, 1.1, 0], True, False, 2)
        label = T("tend to be single and one-sided", 32, ORANGE).move_to([0, -0.5, 0])
        self.play(FadeIn(ee), FadeIn(label), run_time=0.5)
        self.at("diagnosed later")
        timeline = arr([-4.5, -2, 0], [4.5, -2, 0])
        later = T("later diagnosis", 28, GREY).move_to([3, -2.7, 0])
        self.play(GrowArrow(timeline), FadeIn(later), run_time=0.6)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        ped = pedigree()
        # Retain the old pedigree geometry; use muted red fills to mean inherited
        # allele/risk, rather than imply every carrier has a tumor.
        for shape in ped.family_members_with_points():
            if isinstance(shape, (Square, Circle)) and shape.get_fill_opacity() > 0:
                shape.set_fill(RED, 0.4).set_stroke(RED)
        c = cell([3.6, 0.7, 0], 2.6)
        self.add(heading("RB1: family risk and cell function"))
        pl = T("family: inherited risk", 28, RED).move_to([-3.4, -2.4, 0])
        dom = T("dominant", 28, RED).move_to([-3.4, -3.1, 0])
        self.at("the inherited allele")
        self.play(FadeIn(ped), FadeIn(pl), run_time=0.6)
        self.at("dominant in a family")
        self.play(FadeIn(dom), run_time=0.5)
        cl = T("cell: recessive", 28, GREEN).move_to([3.6, -1.2, 0])
        self.at("recessive in the cell")
        self.play(FadeIn(c), FadeIn(cl), run_time=0.6)
        self.at("A pedigree tracks risk")
        self.play(Indicate(ped, color=RED, scale_factor=1.03), run_time=0.6)
        self.at("A cell needs")
        disabled = T("both RB1 copies disabled", 26, RED).move_to([3.6, -2.4, 0])
        self.play(c.rb.animate.set_fill(RED, 1), FadeIn(disabled), run_time=0.7)
        self.finish()


class S11Instability(SpokenScene):
    def construct(self):
        head = heading("Genome instability adds variation")
        self.at("Genome instability")
        self.play(FadeIn(head), run_time=0.5)
        repair = chip("faulty DNA repair", RED, 28).move_to([-3.6, 1.9, 0])
        seq = VGroup(*[chip(letter, GREY, 26) for letter in "ACGT"]).arrange(RIGHT, buff=0.16).move_to([-3.6, 0.5, 0])
        self.at("Faulty")
        self.play(FadeIn(repair), FadeIn(seq), run_time=0.6)
        self.at("can increase mutations")
        self.play(Transform(seq[1], chip("T", RED, 26).move_to(seq[1])),
                  Transform(seq[3], chip("A", RED, 26).move_to(seq[3])), run_time=0.7)
        segregation = chip("faulty segregation", RED, 28).move_to([3.6, 1.9, 0])
        # Bars are whole chromosome counts, not molecular structures.
        def count_bars(n, x):
            return VGroup(*[RoundedRectangle(width=0.18, height=1.1, corner_radius=0.06,
                         stroke_color=GREY, fill_color=GREY, fill_opacity=0.7)
                         for _ in range(n)]).arrange(RIGHT, buff=0.22).move_to([x, 0.3, 0])
        source = count_bars(4, 3.6)
        self.at("Faulty chromosome segregation")
        self.play(FadeIn(segregation), FadeIn(source), run_time=0.6)
        self.at("produces chromosome gains")
        gains, losses = count_bars(3, 2.4), count_bars(1, 4.8)
        labels = VGroup(T("gain", 24, YELLOW).move_to([2.4, -0.7, 0]), T("loss", 24, YELLOW).move_to([4.8, -0.7, 0]))
        self.play(ReplacementTransform(source, VGroup(gains, losses)), FadeIn(labels), run_time=0.8)
        self.at("That variation supplies")
        root = cell([0, -1.3, 0], 0.8, RED, GREEN, ORANGE, 0.2)
        branches = VGroup(*[cell([x, -2.7, 0], 0.8, RED, RED if x > 0 else GREEN, ORANGE, 0.2) for x in (-2, 2)])
        inputs = VGroup(arr([-3.6, -0.2, 0], root.get_left()), arr([3.6, -1, 0], root.get_right()))
        outputs = VGroup(*[arr(root.get_bottom(), b.get_top()) for b in branches])
        self.play(Create(inputs), FadeIn(root), Create(outputs), FadeIn(branches), run_time=0.7)
        self.at("material for selection")
        self.play(Indicate(branches, color=YELLOW), run_time=0.6)
        self.finish()


class S12Sequencing(SpokenScene):
    def construct(self):
        head = heading("Compare tumor and matched normal")
        normal = chip("matched normal", GREY, 30).move_to([-3.5, 2, 0])
        tumor = chip("tumor sample", ORANGE, 30).move_to([3.5, 2, 0])
        self.at("Sequencing a tumor")
        samples = VGroup(cell([-3.5, 0, 0], 1.8, GREEN, GREEN),
                         cell([3.5, 0, 0], 1.8, RED, GREEN, ORANGE, 0.2))
        self.play(FadeIn(head), FadeIn(normal), FadeIn(tumor), FadeIn(samples), run_time=0.7)
        shared = VGroup(chip("variant A", RED, 26).move_to([-3.5, 0.6, 0]),
                        chip("variant A", RED, 26).move_to([3.5, 0.6, 0]))
        germ = T("shared → usually germline", 28, TEXT).move_to([0, -0.35, 0])
        self.at("Variants in both")
        self.play(FadeOut(samples), FadeIn(shared), FadeIn(germ), run_time=0.7)
        som = T("tumor only → usually somatic", 28, TEXT).move_to([0, -2.5, 0])
        only = chip("variant B", RED, 26).move_to([3.5, -1.4, 0])
        self.at("Variants only in the tumor")
        self.play(FadeIn(only), FadeIn(som), run_time=0.6)
        self.at("The tumor sample also")
        self.play(FadeOut(shared), FadeOut(germ), FadeOut(only), FadeOut(som), FadeOut(normal),
                  tumor.animate.move_to([0, 2, 0]), run_time=0.5)
        mixed = VGroup(cell([-2.7, 0, 0], 1.15, RED, GREEN, ORANGE, 0.3),
                       cell([-0.9, 0, 0], 1.15, RED, GREEN, ORANGE, 0.3),
                       cell([0.9, 0, 0], 1.15, GREEN, GREEN), cell([2.7, 0, 0], 1.15, GREEN, GREEN))
        mixlabels = VGroup(T("tumor cells", 24, ORANGE).move_to([-1.8, -1, 0]),
                           T("normal cells", 24, GREY).move_to([1.8, -1, 0]))
        self.at("contains normal cells")
        self.play(FadeIn(mixed), FadeIn(mixlabels), run_time=0.6)
        purity = T("purity = fraction of tumor cells", 30, ORANGE).move_to([0, -2.1, 0])
        effect = T("purity matters for variant fractions", 26, GREY).move_to([0, -3, 0])
        self.at("its purity matters")
        self.play(FadeIn(purity), FadeIn(effect), run_time=0.6)
        # Hold the purity definition through the last spoken sentence, then
        # return to the acquired-change lineage to connect to the end card.
        self.at("variant fractions")
        self.wait(0.5)
        nodes, links = lineage()
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(nodes), Create(links), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Cancer grows from acquired DNA changes selected in a clone."

    def construct(self):
        nodes, links = lineage()
        VGroup(nodes, links).shift(DOWN * 0.3)
        self.add(nodes, links)
        first, second = self.LINE.split(" selected", 1)
        line = VGroup(T(first, 34, font=TITLE_FONT), T("selected" + second, 34, font=TITLE_FONT))
        line.arrange(DOWN, buff=0.15).move_to([0, 3.15, 0])
        sub = T("biochemistrypedia.com", 22, TEAL).move_to([0, -3.1, 0])
        self.play(FadeIn(line), FadeIn(sub), run_time=0.6)
        self.finish()
