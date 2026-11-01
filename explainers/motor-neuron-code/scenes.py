"""A motor neuron is a combination  (Developmental Neuroscience explainer, motor-neuron-code)

COLOR MAP (one colour per concept, whole film)
  BLUE   = Lhx3
  YELLOW = Isl1
  PURPLE = NLI (the cofactor)
  ORANGE = V2 interneuron and its genes
  GREEN  = motor neuron and its genes
  PINK   = Mnx1
  TEAL   = Sonic hedgehog
  RED    = absent / deleted / crossed out
  GREY   = cells, tissue, structure, labels
  WHITE  = rings that point at the shared binding site
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58AB5"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(center, w=1.0, h=0.7, color=RED, sw=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-w / 2, h / 2, 0], c + [w / 2, -h / 2, 0], color=color, stroke_width=sw),
                  Line(c + [-w / 2, -h / 2, 0], c + [w / 2, h / 2, 0], color=color, stroke_width=sw))


R0 = 1.5


def lhx(c, k=1.0):
    """Lhx3 drawn as a cup: a round body with a round socket bitten out of its right side."""
    R = R0 * k
    cx, cy = c[0], c[1]
    circ = Circle(radius=R).move_to([cx, cy, 0])
    cut = Circle(radius=0.44 * k).move_to([cx + 0.95 * R, cy, 0])
    body = Difference(circ, cut, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3)
    lab = T("Lhx3", int(round(34 * k)), BLUE, weight=BOLD).move_to([cx - 0.2 * R, cy, 0])
    return VGroup(body, lab)


def notch(c, k=1.0):
    return np.array([c[0] + 0.95 * R0 * k, c[1], 0])


def nli(peg, k=1.0, color=PURPLE):
    """NLI: a block with a round peg that fits the socket."""
    p = Circle(radius=0.40 * k, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.5).move_to([peg[0], peg[1], 0])
    b = RoundedRectangle(corner_radius=0.16, width=1.5 * k, height=1.1 * k, stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=0.3).move_to([peg[0] + 1.15 * k, peg[1], 0])
    lab = T("NLI", int(round(32 * k)), color, weight=BOLD).move_to(b)
    return VGroup(p, b, lab)


def isl(peg, k=1.0, color=YELLOW):
    """Isl1: a block with a long tail that ends in the same kind of peg."""
    p = Circle(radius=0.40 * k, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.5).move_to([peg[0], peg[1], 0])
    tail = Line([peg[0] + 0.4 * k, peg[1], 0], [peg[0] + 2.0 * k, peg[1], 0], color=color, stroke_width=7)
    b = RoundedRectangle(corner_radius=0.2, width=2.0 * k, height=1.2 * k, stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=0.3).move_to([peg[0] + 3.0 * k, peg[1], 0])
    lab = T("Isl1", int(round(34 * k)), color, weight=BOLD).move_to(b)
    return VGroup(p, tail, b, lab)


def nli_down(peg, k=1.0, color=PURPLE):
    """NLI bound beneath Isl1: the same peg and block, the block hanging below the peg."""
    p = Circle(radius=0.40 * k, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.5).move_to([peg[0], peg[1], 0])
    b = RoundedRectangle(corner_radius=0.16, width=1.5 * k, height=1.1 * k, stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=0.3).move_to([peg[0], peg[1] - 0.95 * k, 0])
    lab = T("NLI", int(round(32 * k)), color, weight=BOLD).move_to(b)
    return VGroup(p, b, lab)


def isl_dock(s, k=1.0):
    """Where NLI binds on Isl1: under the middle of the Isl1 block."""
    blk = s[2]
    return np.array([blk.get_center()[0], blk.get_bottom()[1] - 0.25 * k, 0])


def ghost_isl(center, k=1.0):
    box = RoundedRectangle(corner_radius=0.2, width=2.0 * k, height=1.2 * k).move_to(center)
    d = DashedVMobject(box, num_dashes=26).set_stroke(RED, 4, opacity=0.9)
    lab = T("no Isl1", int(round(30 * k)), RED, weight=BOLD).move_to(box)
    return VGroup(d, lab)


def tag(text, pos):
    return T(text, 24, GREY).move_to(pos)


class S00Title(TitleCard):
    LESSON = "Transcription Factor Codes: Building a Motor Neuron"
    TITLE = "A Motor Neuron Is a Combination"


# Extra schematic helpers. Structural binding helpers above are retained from the old film,
# but the new chick comparison deliberately uses only chips.
# Additional colours: GOLD = Olig2 / Hox positional information; TEAL also = guidance context.
def neuron(pos, radius=0.7, color=GREEN):
    body = Circle(radius=radius, color=color, stroke_width=4, fill_color=color, fill_opacity=0.14).move_to(pos)
    branches = VGroup(*[Line(body.get_center() + radius * np.array([np.cos(a), np.sin(a), 0]),
                              body.get_center() + radius * 1.5 * np.array([np.cos(a), np.sin(a), 0]),
                              color=color, stroke_width=3) for a in (2.3, 3.1, 3.9)])
    return VGroup(body, branches)


def tube():
    bands = VGroup(*[Rectangle(width=2.8, height=0.78, stroke_color=GREY, stroke_width=2,
                               fill_color=GREY, fill_opacity=0.10 + 0.08 * (i % 2)) for i in range(7)])
    return bands.arrange(DOWN, buff=0).move_to([-2.8, 0, 0])


def muscle(pos, label="muscle", width=2.1):
    box = RoundedRectangle(width=width, height=1, corner_radius=0.3, color=GREY,
                           fill_color=GREY, fill_opacity=0.16).move_to(pos)
    return VGroup(box, T(label, 26, GREY).move_to(box))


class S01Puzzle(SpokenScene):
    def construct(self):
        n = neuron([-3, 0, 0], 1.1)
        factors = VGroup(chip("factor", YELLOW, 26), chip("factor", BLUE, 26), chip("factor", PINK, 26)).arrange(RIGHT, buff=0.25).move_to([0, 2.3, 0])
        self.at("A motor neuron")
        self.play(FadeIn(n), run_time=0.5)
        self.at("combinations of transcription factors")
        self.play(FadeIn(factors), run_time=0.6)
        stages = VGroup(*[T(t, 24, GREY) for t in ("progenitor stripe", "motor neuron", "column / pool", "axon route", "muscle")]).arrange(RIGHT, buff=0.5).move_to([0, -2.4, 0])
        self.at("acting in stages")
        self.play(FadeIn(stages), run_time=0.5)
        self.at("first makes")
        identity = VGroup(chip("Isl1 / Isl2", YELLOW, 26), chip("Lhx3", BLUE, 26), chip("Mnx1", PINK, 26)).arrange(RIGHT, buff=0.25).move_to(factors)
        self.play(Indicate(n, color=GREEN), Transform(factors, identity), stages[1].animate.set_color(GREEN), run_time=0.6)
        target = muscle([4.6, 0, 0])
        axon = VMobject(color=GREEN, stroke_width=5).set_points_smoothly([[-1.9, 0, 0], [0, -0.5, 0], [2, 0.3, 0], [3.55, 0, 0]])
        self.at("Then it helps decide")
        positional = VGroup(chip("Hox", GOLD, 28), chip("FoxP1", TEXT, 28)).arrange(RIGHT, buff=0.3).move_to([1, 2.3, 0])
        self.play(FadeIn(target), Transform(factors, positional), stages[2].animate.set_color(GREEN), run_time=0.6)
        self.at("its axon will reach")
        route_code = VGroup(chip("Lhx1", TEXT, 28), T("+ guidance cues", 26, TEAL)).arrange(RIGHT, buff=0.3).move_to([1, 2.3, 0])
        self.play(Create(axon), Transform(factors, route_code), stages[3:].animate.set_color(GREEN), run_time=1)
        self.at("only part of the story")
        self.play(Indicate(VGroup(axon, target), color=GREEN), run_time=0.7)
        self.at("Follow the code")
        self.play(LaggedStart(*[Indicate(t, color=GREEN) for t in stages], lag_ratio=0.3), run_time=2)
        self.finish()


class S08Progenitors(SpokenScene):
    def construct(self):
        bands = tube()
        bar = VGroup(*[Rectangle(width=0.45, height=5.46 / 16, stroke_width=0, fill_color=TEAL,
                                 fill_opacity=0.06 + 0.85 * (i / 15) ** 1.5) for i in range(16)]).arrange(DOWN, buff=0).move_to([-5, 0, 0])
        shh = T("Sonic hedgehog", 26, TEAL).rotate(PI / 2).move_to([-5.8, 0, 0])
        self.at("Sonic Hedgehog")
        self.play(FadeIn(bar), FadeIn(shh), FadeIn(bands), run_time=0.7)
        self.at("read their position")
        self.play(LaggedStart(*[Indicate(b, color=TEAL) for b in bands], lag_ratio=0.1), run_time=0.9)
        pmn = bands[5]
        lab = T("pMN", 30, GREEN).move_to([-0.5, pmn.get_y(), 0])
        self.at("One stripe")
        self.play(pmn.animate.set_fill(GREEN, 0.5).set_stroke(GREEN), FadeIn(lab), run_time=0.6)
        cell = Circle(radius=0.9, color=GREY, fill_color=GREY, fill_opacity=0.14).move_to([3.5, 0, 0])
        olig = chip("Olig2", GOLD, 28).move_to(cell)
        self.at("Its dividing cells")
        self.play(TransformFromCopy(pmn, cell), FadeIn(olig), run_time=0.7)
        daughter = Circle(radius=0.65, color=GREY, fill_color=GREY, fill_opacity=0.14).move_to([2.3, 0.6, 0])
        other = daughter.copy().move_to([4.7, -0.6, 0])
        self.at("Around the final division")
        self.play(ReplacementTransform(cell, VGroup(daughter, other)), FadeOut(olig), run_time=0.7)
        new = neuron([2.3, 0.6, 0], 0.65)
        code = chip("new factor set", GREEN, 26).move_to([3.5, -2.2, 0])
        self.at("turns on a new set")
        self.play(ReplacementTransform(daughter, new), FadeIn(code), other.animate.set_opacity(0.3), run_time=0.6)
        self.finish()


class S02Markers(SpokenScene):
    def construct(self):
        lc, rc = np.array([-3.4, 0.2, 0]), np.array([3.4, 0.2, 0])
        cell_l = Circle(radius=2.2, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.12).move_to(lc)
        lab_l = T("new motor neuron", 30, GREEN).move_to([-3.4, -2.5, 0])
        isl_chip = chip("Isl1 or Isl2", YELLOW, 28).move_to(lc + [0, 1, 0])
        lhx_chip = chip("Lhx3", BLUE, 30).move_to(lc)
        mnx_chip = chip("Mnx1", PINK, 30).move_to(lc + [0, -1, 0])
        self.at("ILAT")
        self.play(FadeIn(cell_l), FadeIn(lab_l), FadeIn(isl_chip), run_time=0.6)
        self.at("LHX 3")
        self.play(FadeIn(lhx_chip), run_time=0.5)
        self.at("and MNX 1")
        self.play(FadeIn(mnx_chip), run_time=0.5)
        self.at("not a unique label")
        self.play(Indicate(lhx_chip, color=BLUE), run_time=0.6)
        cell_r = Circle(radius=2.2, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.12).move_to(rc)
        lab_r = T("V2 interneuron", 30, ORANGE).move_to([3.4, -2.5, 0])
        lhx2 = chip("Lhx3", BLUE, 30).move_to(rc)
        self.at("also appears")
        self.play(FadeIn(cell_r), FadeIn(lab_r), TransformFromCopy(lhx_chip, lhx2), run_time=0.8)
        self.at("Its partners")
        self.play(Indicate(isl_chip, color=YELLOW), Indicate(lhx2, color=BLUE), run_time=0.8)
        self.finish()


class S03Nli(SpokenScene):
    def construct(self):
        sp = tag("chick • factor addition", [0, 3.1, 0])
        lh = chip("Lhx3", BLUE, 32).move_to([-3, 0.7, 0])
        nl = chip("NLI", PURPLE, 32).move_to([0, 0.7, 0])
        absent = T("without Isl1", 28, GREY).move_to([3.5, 0.7, 0])
        self.at("In CHIC")
        self.play(FadeIn(sp), FadeIn(lh), FadeIn(absent), run_time=0.6)
        self.at("binds NLI")
        nl.shift(LEFT * 0.8)
        self.play(FadeIn(nl, shift=LEFT * 0.3), lh.animate.shift(RIGHT * 0.8), run_time=0.6)
        out = chip("V2 interneuron genes", ORANGE, 30).move_to([0, -2, 0])
        a = arr([0, -0.1, 0], [0, -1.4, 0], ORANGE)
        self.at("and promotes")
        self.play(GrowArrow(a), FadeIn(out), run_time=0.6)
        is1 = chip("Isl1", YELLOW, 32).move_to([2.2, 0.7, 0])
        self.at("Add islet 1")
        self.play(FadeOut(out), FadeOut(a), FadeOut(absent), FadeIn(is1), run_time=0.5)
        self.at("a different complex")
        self.play(lh.animate.move_to([-1.7, 0.7, 0]), nl.animate.move_to([0, 0.7, 0]), is1.animate.move_to([1.7, 0.7, 0]), run_time=0.6)
        new = chip("motor-neuron genes", GREEN, 30).move_to([0, -2, 0])
        a2 = arr([0, -0.1, 0], [0, -1.4, 0], GREEN)
        self.at("promotes motor neuron")
        self.play(GrowArrow(a2), FadeIn(new), run_time=0.6)
        self.at("The combination matters")
        self.play(Indicate(VGroup(lh, nl, is1), color=GREEN), run_time=0.7)
        self.finish()


class S06Tests(SpokenScene):
    def construct(self):
        sp = tag("mouse • gene deletions", [0, 3.1, 0])
        i = chip("delete Isl1", RED, 30).move_to([-4.5, 1.5, 0])
        m = chip("delete Mnx1", RED, 30).move_to([-4.5, -1.1, 0])
        a1 = arr([-2.9, 1.5, 0], [-1.7, 1.5, 0], GREY)
        no = T("motor neurons\nnot generated", 30, RED).move_to([1.5, 1.5, 0])
        self.at("Delete islet 1")
        self.play(FadeIn(sp), FadeIn(i), run_time=0.5)
        self.at("not generated")
        self.play(GrowArrow(a1), FadeIn(no), run_time=0.6)
        self.at("Delete MNX1")
        self.play(FadeIn(m), run_time=0.5)
        ns = VGroup(*[neuron([x, -1, 0], 0.35) for x in (-0.8, 0.3, 1.4)])
        self.at("and they form")
        self.play(FadeIn(ns), run_time=0.5)
        state = T("transient V2 features", 26, ORANGE).move_to([1.8, -2.2, 0])
        self.at("transiently show")
        self.play(FadeIn(state), ns.animate.set_color(ORANGE), run_time=0.5)
        scattered = [(-1.1, -0.6, 0), (0.4, -1.3, 0), (1.9, -0.7, 0)]
        paths = VGroup(*[arr(a, b, GREEN, w=3) for a, b in (
            ((-1.1, -0.95, 0), (-0.4, -1.8, 0)),
            ((0.4, -1.65, 0), (-0.3, -1.9, 0)),
            ((2.25, -0.7, 0), (3.2, -1.6, 0)),
        )])
        disorder = T("disordered columns / projections", 26, ORANGE).move_to([1.3, -3.1, 0])
        self.at("disordered columns and axons")
        self.play(*[n.animate.move_to(p) for n, p in zip(ns, scattered)], Create(paths), FadeIn(disorder), run_time=0.6)
        self.at("Making a cell")
        self.play(Indicate(no, color=RED), run_time=0.6)
        self.at("maintaining its identity")
        self.play(Indicate(VGroup(ns, state), color=GREEN), run_time=0.6)
        self.finish()


class S09Hox(SpokenScene):
    def construct(self):
        cord = RoundedRectangle(width=1.5, height=5.3, corner_radius=0.3, color=GREY).move_to([-4.7, 0, 0])
        profiles = VGroup(*[Rectangle(width=0.4, height=h, color=GOLD, fill_color=GOLD, fill_opacity=op).move_to([-5.1 + i * 0.4, y, 0]) for i, (h, y, op) in enumerate(((2.6, 1.2, 0.3), (3.2, 0, 0.6), (2.4, -1.3, 0.9)))])
        ho = T("Hox profiles", 28, GOLD).move_to([-4.7, 3.1, 0])
        self.at("Now which motor neuron")
        self.play(FadeIn(cord), run_time=0.5)
        self.at("Hox proteins")
        self.play(FadeIn(profiles), FadeIn(ho), run_time=0.6)
        fox = chip("FoxP1", TEXT, 30).move_to([-1.7, 2.3, 0])
        column = RoundedRectangle(width=2.6, height=3.8, corner_radius=0.2, color=GREEN).move_to([-0.7, -0.4, 0])
        pools = VGroup(*[VGroup(*[Dot([x, y, 0], color=GREEN, radius=0.13) for x in (-1.2, -0.7, -0.2)]) for y in (0.4, -1.2)])
        self.at("With FOXP1")
        self.play(FadeIn(fox), run_time=0.5)
        self.at("columns and pools")
        self.play(Create(column), FadeIn(pools), run_time=0.6)
        lmc = T("lateral motor\ncolumn", 26, GREEN).move_to([-0.7, -2.9, 0])
        limb = muscle([4.5, 0.2, 0], "limb muscles", width=3.2)
        route = arr([0.7, 0.2, 0], [2.85, 0.2, 0], GREEN)
        self.at("The lateral motor column")
        self.play(FadeIn(lmc), FadeIn(limb), GrowArrow(route), run_time=0.6)
        one = muscle([4.5, -1.9, 0], "one muscle", width=3.2)
        pool_route = arr([0, -1.2, 0], [2.85, -1.9, 0], GREEN)
        self.at("A pool supplies")
        self.play(FadeOut(route), FadeIn(one), GrowArrow(pool_route), Indicate(pools[1], color=GREEN), run_time=0.6)
        deletion = chip("mouse: delete Foxp1", RED, 28).move_to([0, 2.6, 0])
        self.at("Delete FOXP1")
        self.play(*[FadeOut(o) for o in (fox, ho, cord, profiles, lmc, column, limb, one, pool_route)], FadeIn(deletion), pools.animate.move_to([-3.7, 0, 0]), run_time=0.6)
        retained = T("motor neurons still form", 28, GREEN).move_to([-3.6, -2.1, 0])
        self.at("still form")
        self.play(FadeIn(retained), run_time=0.5)
        failed = T("limb / autonomic\ncolumn identities fail", 28, RED).move_to([3.1, 1.3, 0])
        self.at("identities fail")
        self.play(FadeIn(failed), run_time=0.5)
        targets = VGroup(muscle([4.6, -0.4, 0], "muscle A"), muscle([4.6, -2.2, 0], "muscle B"))
        tangled = VGroup(*[VMobject(color=GREEN, stroke_width=3).set_points_smoothly([[-3.2, y, 0], [-1, y + dy, 0], [1, z + dy, 0], [3.5, z, 0]]) for y, dy, z in ((0.8, -1, -2.2), (-0.8, 0.8, -0.4), (0.8, -1.8, -0.4))])
        self.at("axons appear to choose")
        self.play(FadeIn(targets), Create(tangled), run_time=1)
        qual = T("apparently random\nlimb targeting", 24, GREY).move_to([4.6, -3.25, 0])
        self.at("at random")
        self.play(FadeIn(qual), run_time=0.5)
        self.finish()


class S10Limb(SpokenScene):
    def construct(self):
        n = neuron([-4.5, 0, 0], 0.8)
        nl = T("lateral LMC cells", 28, GREEN).move_to([-4.5, 2.2, 0])
        lh = chip("Lhx1", TEXT, 28).move_to([-4.5, -1.7, 0])
        limb = RoundedRectangle(width=5.3, height=4.4, corner_radius=0.7, color=GREY).move_to([3.4, 0, 0])
        labels = VGroup(T("dorsal limb", 28, GREY).move_to([3.5, 1.6, 0]), T("ventral limb", 28, GREY).move_to([3.5, -1.6, 0]))
        dorsal = VMobject(color=GREEN, stroke_width=6).set_points_smoothly([[-3.7, 0, 0], [-1, 0, 0], [1.3, 0.9, 0], [4.4, 0.9, 0]])
        self.at("The code also")
        self.play(FadeIn(n), FadeIn(limb), FadeIn(labels), run_time=0.6)
        self.at("Lateral cells")
        self.play(FadeIn(nl), run_time=0.5)
        self.at("express LHX1")
        self.play(FadeIn(lh), run_time=0.5)
        self.at("ensures a dorsal trajectory")
        self.play(Create(dorsal), run_time=1)
        loss = chip("without Lhx1", RED, 28).move_to(lh)
        neutral = T("dorsal preference lost", 28, RED).move_to([0, -3, 0])
        ventral = VMobject(color=GREEN, stroke_width=4).set_points_smoothly([[-3.7, 0, 0], [-1, 0, 0], [1.3, -0.9, 0], [4.4, -0.9, 0]])
        self.at("Without it")
        self.play(ReplacementTransform(lh, loss), FadeOut(dorsal), run_time=0.5)
        self.at("lose that preference")
        self.play(Create(dorsal.copy().set_stroke(width=4)), Create(ventral), FadeIn(neutral), run_time=0.7)
        machinery = VGroup(chip("Eph receptors / ephrins", TEAL, 26), T("part of the guidance machinery", 24, GREY)).arrange(DOWN, buff=0.2).move_to([0, 2.9, 0])
        self.at("F receptors")
        self.play(FadeOut(nl), FadeIn(machinery), run_time=0.6)
        self.at("Identity helps")
        self.play(Indicate(n, color=GREEN), run_time=0.7)
        self.finish()


class S11Dish(SpokenScene):
    def construct(self):
        dish = Ellipse(width=11.5, height=3.5, color=GREY, stroke_width=4).move_to([0, -0.7, 0])
        cells = VGroup(*[Circle(radius=0.35, color=GREY, fill_color=GREY, fill_opacity=0.2).move_to([x, -0.7 + y, 0]) for x, y in ((-1, 0.1), (0, -0.2), (1, 0.2))])
        stage = T("mouse embryonic stem cells", 30, GREY).move_to([0, -3, 0])
        self.at("Use that developmental logic")
        self.play(Create(dish), FadeIn(cells), FadeIn(stage), run_time=0.7)
        ra = VGroup(chip("retinoic acid", GOLD, 28), T("rostral hindbrain / cervical", 24, GOLD)).arrange(DOWN, buff=0.2).move_to([-3.1, 2.3, 0])
        self.at("retinoic acid")
        self.play(FadeIn(ra), run_time=0.5)
        spinal = T("spinal progenitors", 30, GREY).move_to(stage)
        self.at("promotes spinal character")
        self.play(ReplacementTransform(stage, spinal), cells.animate.set_stroke(GOLD), run_time=0.6)
        hh = VGroup(chip("Hedgehog agonist", TEAL, 28), T("ventral / pMN", 24, TEAL)).arrange(DOWN, buff=0.2).move_to([3.1, 2.3, 0])
        self.at("A hedgehog agonist")
        self.play(FadeIn(hh), run_time=0.5)
        pmn = T("pMN progenitors", 30, GREEN).move_to(spinal)
        self.at("toward PMN")
        self.play(ReplacementTransform(spinal, pmn), cells.animate.set_stroke(GREEN), run_time=0.5)
        neurons = VGroup(*[neuron(c.get_center(), 0.35) for c in cells])
        mn = T("Mnx1-positive motor neurons", 30, GREEN).move_to(pmn)
        self.at("Motor neurons follow")
        self.play(ReplacementTransform(cells, neurons), ReplacementTransform(pmn, mn), run_time=0.6)
        bias = T("mostly medial motor column", 28, GREEN).move_to([0, -1.7, 0])
        self.at("mostly medial motor column")
        self.play(FadeIn(bias), run_time=0.6)
        unresolved = chip("one named pool?", GREY, 30).move_to([0, 2.3, 0])
        self.at("Making one named pool")
        self.play(FadeOut(ra), FadeOut(hh), FadeIn(unresolved), run_time=0.6)
        self.at("fine detail is still incomplete")
        self.play(Indicate(unresolved, color=GREY), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "A staged transcription-factor code builds identity and helps specify connections."
