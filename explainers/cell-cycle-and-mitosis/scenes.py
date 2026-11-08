"""Copy first, then divide: the cell cycle and mitosis  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = DNA / chromosomes / sister chromatids (labelled bars, never a molecule)
  DNA2   = darker DNA blue for the second model chromosome
  GOLD   = the centromere (little dot joining two sister chromatids)
  PURPLE = nuclear envelope / nucleus
  YELLOW = spindle fibers and the pinching ring (what moves things)
  GREEN  = new cells, new wall (cell plate), new tissue
  TEAL   = things that cross the cell membrane (oxygen, food, wastes)
  RED    = the problem: less membrane for the inside (falling ratio), "not a rest"
  ORANGE = an open question
  GREY   = membranes, cell outlines, tissue, de-emphasized
  TEXT   = stage names (prophase, ...), neutral labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bar(h=1.3, w=0.18, color=BLUE):
    return RoundedRectangle(corner_radius=min(0.07, w / 2.5), width=w, height=h, stroke_color=color,
                            stroke_width=2, fill_color=color, fill_opacity=0.85)


def chrom(center, copied=True, h=1.3, w=0.18, gap=0.08, dot_r=0.09):
    """A chromosome as labelled blocks: one bar, or two sister-chromatid bars joined by a gold dot."""
    cx, cy = center[0], center[1]
    if copied:
        off = (w + gap) / 2
        l = bar(h, w).move_to([cx - off, cy, 0])
        r = bar(h, w).move_to([cx + off, cy, 0])
        dot = Dot([cx, cy, 0], radius=dot_r, color=GOLD).set_z_index(3)
        g = VGroup(l, r, dot)
        g.l, g.r, g.dot = l, r, dot
    else:
        l = bar(h, w).move_to([cx, cy, 0])
        g = VGroup(l)
        g.l, g.r, g.dot = l, None, None
    g.set_z_index(2)
    return g


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cell_shape(w, h, center, color=GREY):
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color,
                   fill_opacity=0.07).move_to(center)


def nucleus(r, center, dashed=False):
    c = Circle(radius=r, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.10).move_to(center)
    return c


def stage_chip(text):
    return chip(text, TEXT, size=32).move_to([0, 3.0, 0])


# Two shades of the DNA blue distinguish the two model chromosomes throughout.
DNA2 = "#3485B4"


def model_pair(x=0, y=-0.4, copied=True, h=1.3):
    a = chrom([x - 0.65, y, 0], copied, h, 0.20)
    b = chrom([x + 0.65, y, 0], copied, h * 0.72, 0.20)
    b.l.set_color(DNA2)
    if copied:
        b.r.set_color(DNA2)
    return VGroup(a, b)


def daughter(x, y=0.0):
    outline = cell_shape(2.2, 2.7, [x, y, 0], GREEN)
    n = nucleus(0.72, [x, y, 0])
    dna = model_pair(x, y, False, 0.75)
    # Compact matching complete sets inside each nucleus.
    dna[0].move_to([x - 0.24, y, 0])
    dna[1].move_to([x + 0.24, y, 0])
    return VGroup(outline, n, dna)


def book(center):
    cover = RoundedRectangle(width=1.5, height=1.9, corner_radius=0.1,
                              color=BLUE, fill_color=BLUE, fill_opacity=0.15)
    lines = VGroup(*[Line([-0.5, y, 0], [0.5, y, 0], color=TEXT, stroke_width=3)
                     for y in (0.5, 0.15, -0.2, -0.55)])
    return VGroup(cover, lines).move_to(center)


class S00Title(TitleCard):
    LESSON = "The Cell Cycle and Mitosis"
    TITLE = "Copy First, Then Divide"

    def construct(self):
        title = T(self.TITLE, 48, font=TITLE_FONT).move_to([0, 2.5, 0])
        skin = VGroup(*[Square(0.45, color=GREEN, fill_opacity=0.2)
                        .move_to([-3.8 + i * 0.5, 0.3, 0]) for i in range(3)])
        root = RoundedRectangle(width=0.7, height=1.5, corner_radius=0.3,
                                color=GREY).move_to([3.2, 0.3, 0])
        labels = VGroup(T("skin repair", 24).move_to([-3.3, -1.0, 0]),
                        T("onion root", 24).move_to([3.2, -1.0, 0]))
        model = VGroup(cell_shape(2.5, 2, [0, 0, 0]), nucleus(0.7, ORIGIN),
                       model_pair(0, 0, False, 0.65).scale(0.65))
        self.play(FadeIn(title), FadeIn(skin), FadeIn(root), FadeIn(labels), run_time=0.7)
        self.play(FadeOut(skin), FadeOut(root), FadeOut(labels), FadeIn(model, scale=0.6), run_time=0.8)
        self.play(model.animate.scale(1.5), run_time=0.8)
        self.finish()


class S03Copy(SpokenScene):
    def construct(self):
        cell = cell_shape(6.4, 3.6, [0, -0.4, 0])
        nuc = nucleus(1.4, [0, -0.4, 0])
        dna = model_pair(copied=False)
        heading = T("DNA: copy before mitosis", 34, BLUE).move_to([0, 2.8, 0])
        self.at("A cell copies")
        self.play(FadeIn(cell), FadeIn(nuc), FadeIn(dna), FadeIn(heading), run_time=0.6)
        copies = model_pair()
        self.at("its DNA")
        self.play(ReplacementTransform(dna, copies), run_time=1.2)
        outcome = T("A complete set for each new cell", 30).move_to([0, -2.8, 0])
        self.at("a full set")
        self.play(FadeIn(outcome), run_time=0.6)
        self.at("Copy first")
        self.play(Indicate(copies, color=BLUE), run_time=0.7)

        analogy = T("ANALOGY: two groups need every recipe", 30).move_to([0, 2.8, 0])
        groups = VGroup(T("group 1", 26).move_to([-3, -2.1, 0]),
                        T("group 2", 26).move_to([3, -2.1, 0]))
        whole = book([0, 0, 0])
        self.at("Picture two groups")
        self.play(*[FadeOut(m) for m in (cell, nuc, copies, heading, outcome)],
                  FadeIn(analogy), FadeIn(groups), FadeIn(whole), run_time=0.7)
        halves = VGroup(*[VGroup(Rectangle(width=1.5, height=0.92, color=BLUE,
                         fill_opacity=0.15), T("½ recipes", 24)).move_to([x, 0, 0]) for x in (-3, 3)])
        self.at("Tearing a book")
        self.play(ReplacementTransform(whole, halves), run_time=1.2)
        fulls = VGroup(book([-3, 0, 0]), book([3, 0, 0]))
        self.at("Copying it first")
        self.play(ReplacementTransform(halves, fulls), run_time=1.0)
        caveat = T("Cells do not decide", 32, GREY).move_to([0, -3, 0])
        self.at("The comparison breaks")
        self.play(FadeIn(caveat), run_time=0.7)
        protein = chip("proteins copy and share DNA", BLUE, 30).move_to([0, 2.8, 0])
        singles = model_pair(copied=False)
        self.at("Proteins copy")
        self.play(*[FadeOut(m) for m in (analogy, groups, fulls, caveat)],
                  FadeIn(protein), FadeIn(cell), FadeIn(nuc), FadeIn(singles), run_time=0.7)
        inter = T("interphase", 32).move_to([0, 3.25, 0])
        g1 = chip("G1: growth", GREEN, 26).move_to([-3.8, 2.3, 0])
        s = chip("S: DNA copying", BLUE, 26).move_to([0, 2.3, 0])
        g2 = chip("G2: preparation", TEXT, 26).move_to([3.8, 2.3, 0])
        self.at("In interphase")
        self.play(FadeOut(protein), FadeIn(inter), run_time=0.4)
        self.at("G1 is growth")
        self.play(FadeIn(g1), cell.animate.scale(1.06), run_time=0.6)
        self.at("S phase")
        copies = model_pair()
        self.play(FadeIn(s), ReplacementTransform(singles, copies), run_time=1.1)
        self.at("G2 is preparation")
        self.play(FadeIn(g2), run_time=0.6)
        big = chrom([0, -0.5, 0], True, 2.0, 0.45, 0.35, 0.16)
        self.at("Each copied chromosome")
        self.play(*[FadeOut(m) for m in (cell, nuc, copies, inter, g1, s, g2)], FadeIn(big), run_time=0.7)
        sisters = T("two identical sister chromatids", 30, BLUE).move_to([0, 1.6, 0])
        self.at("two identical sister chromatids")
        self.play(FadeIn(sisters), run_time=0.6)
        cent = T("centromere", 28, GOLD).move_to([3.1, -0.5, 0])
        pointer = arr([1.8, -0.5, 0], [0.25, -0.5, 0], GOLD, w=3)
        self.at("joined at the centromere")
        self.play(FadeIn(cent), GrowArrow(pointer), run_time=0.7)
        self.finish()


class S04Mitosis(SpokenScene):
    def construct(self):
        cy = -0.4
        cell = cell_shape(8.2, 5, [0, cy, 0])
        nuc = nucleus(1.5, [0, cy, 0])
        dna = model_pair()
        c1, c2 = dna
        stage = stage_chip("mitosis: nuclear division")
        note = T("model cell: two chromosomes shown", 24, GREY).move_to([0, -3.35, 0])
        self.at("Mitosis shares")
        self.play(FadeIn(cell), FadeIn(nuc), FadeIn(dna), FadeIn(stage), FadeIn(note), run_time=0.7)
        # Introduce a schematic fiber separately before showing spindle attachment.
        legend = VGroup(Line([-4, -3.25, 0], [-2, -3.25, 0], color=YELLOW, stroke_width=4),
                        T("spindle: protein fibers", 26, YELLOW).move_to([1, -3.25, 0]))
        self.at("Spindle fibers are")
        self.play(FadeOut(note), FadeIn(legend), run_time=0.6)
        self.at("In prophase")
        newstage = stage_chip("prophase")
        self.play(ReplacementTransform(stage, newstage), FadeOut(legend), FadeIn(note), run_time=0.4)
        stage = newstage
        self.at("coil up")
        self.play(c1.animate.stretch(0.7, 1).stretch(1.3, 0),
                  c2.animate.stretch(0.7, 1).stretch(1.3, 0), run_time=0.7)
        self.at("nuclear envelope breaks down")
        self.play(FadeOut(nuc), run_time=0.8)
        self.at("In metaphase")
        newstage = stage_chip("metaphase")
        self.play(ReplacementTransform(stage, newstage), run_time=0.4)
        stage = newstage
        def fiber(edge, target):
            f = Line(edge, target.get_center(), color=YELLOW, stroke_width=3).set_z_index(0)
            f.add_updater(lambda m: m.put_start_and_end_on(edge, target.get_center()))
            return f
        fibers = VGroup(*[fiber(np.array([x, cy, 0]), part)
                          for c in dna for x, part in ((-4, c.l), (4, c.r))])
        self.at("spindle fibers line")
        middle = DashedLine([0, -2.5, 0], [0, 1.8, 0], color=GREY).set_z_index(-1)
        self.play(FadeIn(fibers), FadeIn(middle), c1.animate.move_to([0, 0.45, 0]),
                  c2.animate.move_to([0, -1.2, 0]), run_time=1.6)
        self.at("In anaphase")
        newstage = stage_chip("anaphase")
        self.play(ReplacementTransform(stage, newstage), FadeOut(middle), run_time=0.4)
        stage = newstage
        self.at("sister chromatids separate")
        self.play(FadeOut(c1.dot), FadeOut(c2.dot),
                  *[p.animate.shift(direction * 0.45) for c in dna
                    for p, direction in ((c.l, LEFT), (c.r, RIGHT))], run_time=0.7)
        self.at("move to opposite ends")
        self.play(*[p.animate.move_to([x, y, 0]) for c, y in ((c1, 0.35), (c2, -1.1))
                    for p, x in ((c.l, -2.7), (c.r, 2.7))], run_time=1.6)
        self.at("In telophase")
        newstage = stage_chip("telophase")
        self.play(ReplacementTransform(stage, newstage), FadeOut(fibers), run_time=0.4)
        stage = newstage
        self.at("a full set reaches")
        self.play(Indicate(VGroup(c1.l, c2.l), color=BLUE),
                  Indicate(VGroup(c1.r, c2.r), color=BLUE), run_time=0.7)
        envs = VGroup(*[Ellipse(width=1.65, height=2.8, color=PURPLE,
                               fill_opacity=0.1).move_to([x, cy, 0]) for x in (-2.7, 2.7)])
        label = T("one complete set in each nucleus", 26, PURPLE).move_to([0, -3.25, 0])
        self.at("new nuclear envelope")
        self.play(FadeIn(envs), FadeOut(note), FadeIn(label), run_time=1.0)
        self.finish()


class S05Split(SpokenScene):
    def construct(self):
        p = ValueTracker(0)
        def body():
            def f(t):
                x = 2.6 * np.cos(t)
                y = 1.7 * np.sin(t) * (1 - p.get_value() * np.exp(-(x / 0.99) ** 2))
                return [x - 3.3, y, 0]
            return ParametricFunction(f, t_range=[0, TAU], color=GREY, stroke_width=4,
                                      fill_color=GREY, fill_opacity=0.07)
        animal = always_redraw(body)
        left, right = daughter(-4.45), daughter(-2.15)
        nuclear = VGroup(left[1:], right[1:])
        head = T("cytokinesis: cytoplasmic division", 32).move_to([0, 3.1, 0])
        sub = T("mitosis: nuclear division", 26, PURPLE).move_to([0, 2.35, 0])
        a_label = T("animal cell", 28).move_to([-3.3, -2.3, 0])
        self.at("Cytokinesis divides")
        self.play(FadeIn(head), FadeIn(sub), FadeIn(animal), FadeIn(nuclear), FadeIn(a_label), run_time=0.8)
        self.at("It often starts")
        self.play(p.animate.set_value(0.22), run_time=1.2)
        self.at("In an animal cell")
        self.play(Indicate(animal, scale_factor=1.02), run_time=0.6)
        ring = VGroup(arr([-3.3, 2, 0], [-3.3, 0.9, 0], YELLOW),
                      arr([-3.3, -2, 0], [-3.3, -0.9, 0], YELLOW))
        self.at("a ring pinches")
        self.play(FadeIn(ring), p.animate.set_value(0.7), run_time=1.2)
        self.at("The furrow deepens")
        self.play(p.animate.set_value(0.98), run_time=0.9)
        outlines = VGroup(left[0], right[0])
        self.at("the cell splits")
        self.play(FadeOut(animal), FadeOut(ring), FadeIn(outlines), run_time=0.6)
        wall = RoundedRectangle(width=5, height=3.4, corner_radius=0.12, color=GREY,
                                fill_color=GREY, fill_opacity=0.07).move_to([3.3, 0, 0])
        pd1, pd2 = daughter(2.15), daughter(4.45)
        pn = VGroup(pd1[1:], pd2[1:])
        p_label = T("plant cell: stiff wall", 28).move_to([3.3, -2.3, 0])
        self.at("A plant cell has")
        self.play(FadeIn(wall), FadeIn(pn), FadeIn(p_label), run_time=0.7)
        self.at("cannot pinch")
        self.play(Indicate(wall, scale_factor=1.01), run_time=0.5)
        plate = Line([3.3, -0.05, 0], [3.3, 0.05, 0], color=GREEN, stroke_width=8)
        plate_label = T("cell plate", 26, GREEN).move_to([3.3, -3.0, 0])
        self.at("A cell plate forms")
        self.play(Create(plate), FadeIn(plate_label), run_time=0.6)
        self.at("grows outward")
        self.play(Transform(plate, Line([3.3, -1.7, 0], [3.3, 1.7, 0],
                                      color=GREEN, stroke_width=8)), run_time=1.1)
        self.at("The two new cells")
        same = T("same complete DNA set, usually", 28, BLUE).move_to([0, -3.05, 0])
        self.play(FadeOut(plate_label), FadeIn(same), run_time=0.7)
        self.finish()


class S01Cut(SpokenScene):
    def construct(self):
        head = T("growth • repair • replacement", 34).move_to([0, 3, 0])
        cells = VGroup(daughter(-1.3), daughter(1.3))
        self.at("These new cells")
        self.play(FadeIn(head), FadeIn(cells), run_time=0.8)
        skin = RoundedRectangle(width=6, height=2.5, corner_radius=0.12, color=GREY,
                                fill_color=GREY, fill_opacity=0.2).move_to([-3, 0, 0])
        wound = Rectangle(width=1.4, height=1, color=RED, fill_color=BG,
                          fill_opacity=1).move_to([-3, 0.75, 0])
        dividing = VGroup(*[Square(0.5, color=GREEN, fill_opacity=0.3)
                            .move_to([-3.4 + i * 0.8, -0.6, 0]) for i in range(2)])
        skin_label = T("skin: division behind the wound", 24).move_to([-3, -1.8, 0])
        self.at("Skin cells divide")
        self.play(FadeOut(cells), FadeIn(skin), FadeIn(wound), FadeIn(dividing), FadeIn(skin_label), run_time=0.7)
        added = VGroup(*[Square(0.35, color=GREEN, fill_opacity=0.5)
                         .move_to([-3.5 + i * 0.34, -0.6, 0]) for i in range(4)])
        self.play(ReplacementTransform(dividing, added), run_time=0.6)
        self.at("replace cells that")
        self.play(added.animate.move_to(wound), wound.animate.set_opacity(0.25), run_time=1)
        self.at("Near an onion root tip")
        self.play(*[FadeOut(m) for m in (skin, wound, added, skin_label)], run_time=0.4)
        root = RoundedRectangle(width=1.6, height=4.2, corner_radius=0.6,
                                color=GREY, fill_opacity=0.1).move_to([-1.8, -0.1, 0])
        division = VGroup(*[Square(0.38, color=GREEN, fill_opacity=0.4)
                            .move_to([-2.1 + i * 0.6, -1.3 + j * 0.45, 0])
                            for i in range(2) for j in range(2)])
        dlab = T("division zone", 26, GREEN).move_to([1.4, -1.2, 0])
        self.play(FadeIn(root), FadeIn(division), FadeIn(dlab), run_time=0.5)
        self.at("tip cells divide")
        divided = VGroup(*[Rectangle(width=0.38, height=0.2, color=GREEN, fill_opacity=0.4)
                            .move_to([-2.1 + i * 0.6, -1.5 + j * 0.24, 0])
                            for i in range(2) for j in range(4)])
        self.play(ReplacementTransform(division, divided), run_time=0.5)
        division = divided
        elong = VGroup(*[Rectangle(width=0.5, height=0.5, color=GREEN, fill_opacity=0.2)
                         .move_to([-2.1 + i * 0.6, 0.35, 0]) for i in range(2)])
        elab = T("elongation zone", 26, GREEN).move_to([1.5, 0.6, 0])
        self.at("Behind that zone")
        self.play(FadeIn(elong), FadeIn(elab), run_time=0.5)
        self.at("new cells stretch")
        self.play(elong.animate.stretch(2.8, 1), run_time=0.8)
        down = arr([-3.2, -0.5, 0], [-3.2, -2.5, 0], YELLOW)
        self.at("pushing the root")
        self.play(root.animate.stretch(1.1, 1, about_edge=UP), division.animate.shift(DOWN * 0.35),
                  GrowArrow(down), run_time=0.8)
        self.at("For a single")
        self.play(*[FadeOut(m) for m in (head, root, division, dlab, elong, elab, down)], run_time=0.5)
        amoeba = cell_shape(3.4, 2.5, [0, 0, 0], GREEN)
        label = T("amoeba: one cell, one organism", 30).move_to([0, 2.7, 0])
        self.play(FadeIn(amoeba), FadeIn(label), run_time=0.5)
        self.at("division can make")
        self.play(Transform(amoeba, cell_shape(2.3, 2.5, [-1.5, 0, 0], GREEN)),
                  FadeIn(cell_shape(2.3, 2.5, [1.5, 0, 0], GREEN), shift=RIGHT), run_time=1)
        self.finish()


def cube_model(side, center):
    face = Square(side, color=GREY, fill_color=GREY, fill_opacity=0.15)
    shift = np.array([0.32 * side, 0.25 * side, 0])
    top = Polygon(face.get_corner(UL), face.get_corner(UR), face.get_corner(UR) + shift,
                  face.get_corner(UL) + shift, color=GREY, fill_color=GREY, fill_opacity=0.08)
    right = Polygon(face.get_corner(UR), face.get_corner(DR), face.get_corner(DR) + shift,
                    face.get_corner(UR) + shift, color=GREY, fill_color=GREY, fill_opacity=0.2)
    return VGroup(face, top, right).move_to(center)


class S02Small(SpokenScene):
    def construct(self):
        head = T("A smaller point: cell size", 34).move_to([0, 3.1, 0])
        cell = cell_shape(2.6, 2.6, ORIGIN)
        self.at("A smaller point")
        self.play(FadeIn(head), FadeIn(cell), run_time=0.7)
        flow = VGroup(arr([-3, 0.7, 0], [-0.8, 0.7, 0], TEAL),
                      arr([0.8, -0.5, 0], [3, -0.5, 0], TEAL),
                      T("oxygen + food", 26, TEAL).move_to([-4.5, 0.7, 0]),
                      T("wastes", 26, TEAL).move_to([4, -0.5, 0]))
        self.at("Oxygen food")
        self.play(FadeIn(flow), run_time=0.7)
        self.at("In a cube model")
        small, large = cube_model(1.3, [-3.2, 0, 0]), cube_model(1.3, [2.7, 0.4, 0])
        model = T("geometry model", 26, GREY).move_to([0, 2.3, 0])
        self.play(FadeOut(cell), FadeOut(flow), FadeIn(small), FadeIn(large), FadeIn(model), run_time=0.6)
        self.at("a cell gets bigger")
        self.play(large.animate.scale(1.9), run_time=0.8)
        growth = T("inside grows faster than surface", 30, TEXT).move_to([0, -2.1, 0])
        self.at("its volume grows faster")
        self.play(FadeIn(growth), large[0].animate.set_fill(GREY, opacity=0.45), run_time=0.7)
        ratio = T("less membrane for each bit inside", 30, RED).move_to([0, -2.9, 0])
        self.at("less membrane")
        self.play(FadeIn(ratio), run_time=0.6)
        shapes = VGroup(cell_shape(2, 2, [-3.5, 0, 0]), cell_shape(1.5, 3.2, [0, 0, 0]),
                        cell_shape(3, 1.3, [3.5, 0, 0]))
        self.at("Real cells are not cubes")
        self.play(*[FadeOut(m) for m in (small, large, model, growth, ratio)], FadeIn(shapes), run_time=0.7)
        control = T("cells also control their size", 28).move_to([0, -2.3, 0])
        self.at("Cells also control")
        self.play(FadeIn(control), run_time=0.6)
        limit = T("surface area: one limit among several", 30, RED).move_to([0, -3.1, 0])
        self.at("surface area is one limit")
        self.play(FadeIn(limit), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Cells copy their DNA first, so each new cell gets a full set."