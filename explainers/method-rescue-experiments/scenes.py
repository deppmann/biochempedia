"""Rescue experiments, timed to the supplied narration.

GREY / TEAL: cell boundaries and their normal activity.
PURPLE: original genes and the messages copied from them.
ORANGE: material added in a rescue, including the rescue copy.
RED: silencing guide or persistent defect. GREEN: protein and restored function.
BLUE: apparatus or measurement. YELLOW / GOLD: target emphasis, dates and questions.
All cellular pictures and blot lanes are schematic.
"""
from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
QUESTION = "How can rescue escape the shRNA?"
CELL_CENTER = np.array([-0.7, -0.32, 0.0])
CELL_W, CELL_H = 8.8, 5.45
ORIGINAL = np.array([-1.05, 1.16, 0.0])
RESCUE = np.array([-1.05, 1.16, 0.0])
MESSAGE = np.array([-0.85, -0.07, 0.0])
GUIDE_HOLD = np.array([0.28, 0.58, 0.0])
TARGET = 4
TESTED, RESTORED = 414, 176
FRACTION = RESTORED / TESTED


def at_xy(x, y):
    return np.array([x, y, 0.0])


def block(w, h, color, center, fill=0.72, stroke=2.5, radius=0.12):
    return RoundedRectangle(width=w, height=h, corner_radius=radius, stroke_color=color,
                            stroke_width=stroke, fill_color=color, fill_opacity=fill).move_to(center)


def cell(state="healthy", center=CELL_CENTER, width=CELL_W, height=CELL_H):
    """The same membrane under every version of the cell diagram."""
    edge, fill = {
        "healthy": (TEAL, 0.33),
        "stalled": (GREY, 0.25),
        "crowded": (RED, 0.27),
    }[state]
    return Ellipse(width=width, height=height, stroke_color=edge, stroke_width=6,
                   fill_color=edge, fill_opacity=fill).move_to(center)


def breathe(membrane, fill=0.33):
    """Animate the membrane itself so activity reads even with the protein dots held."""
    pulse(membrane, base=6, amp=2.7, speed=2.6)
    membrane.breath_time = 0.0

    def tint(mob, dt):
        mob.breath_time += dt
        mob.set_fill(opacity=fill + 0.085 * np.sin(2.6 * mob.breath_time))

    membrane.add_updater(tint)


def gene(center=ORIGINAL, color=PURPLE, broken=False, width=2.95):
    if not broken:
        return block(width, 0.5, color, center)
    halves = VGroup(
        block(width * 0.43, 0.5, color, center + LEFT * width * 0.28),
        block(width * 0.43, 0.5, color, center + RIGHT * width * 0.28),
    )
    fault = Line(center + UL * 0.15, center + DR * 0.15, color=RED, stroke_width=8)
    return VGroup(halves, fault)


def message(center=MESSAGE, changed=False):
    colors = [PURPLE, PURPLE, ORANGE, PURPLE, YELLOW, ORANGE, PURPLE]
    if changed:
        colors[3:6] = [YELLOW, ORANGE, PURPLE]
    ribbon = VGroup(*[block(0.55, 0.38, color, ORIGIN, radius=0.07) for color in colors])
    return ribbon.arrange(RIGHT, buff=0.065).move_to(center)


def guide(center=GUIDE_HOLD):
    """A clamp with its opening facing the matching message."""
    hook = VMobject().set_points_as_corners([
        at_xy(-0.89, -0.23), at_xy(-0.89, 0.10), at_xy(-0.72, 0.23),
        at_xy(0.72, 0.23), at_xy(0.89, 0.10), at_xy(0.89, -0.23),
    ])
    hook.set_stroke(RED, width=10)
    teeth = VGroup(*[
        Line(at_xy(x, 0.20), at_xy(x, 0.02), color=RED, stroke_width=6)
        for x in (-0.60, 0, 0.60)
    ])
    return VGroup(hook, teeth).move_to(center)


def target_frame(ribbon):
    segment = VGroup(*ribbon[3:6])
    return block(segment.width + 0.24, segment.height + 0.22, YELLOW, segment.get_center(),
                 fill=0, stroke=3, radius=0.1)


def protein(center, radius=0.20, color=GREEN):
    return Dot(center, radius=radius, color=color, fill_opacity=0.92)


def proteins(center=CELL_CENTER, scale=1.0):
    positions = [(-2.48, -0.90), (-1.72, -1.55), (-0.77, -0.91), (0.23, -1.62),
                 (1.28, -0.88), (2.30, -1.34), (2.95, -0.32)]
    return VGroup(*[protein(center + at_xy(x, y) * scale, 0.22 * scale) for x, y in positions])


def drift_dots(dots):
    for i, dot in enumerate(dots):
        bob(dot, amp=0.13, speed=1.9 + 0.13 * i, seed=i)


def stop_drift(dots):
    for dot in dots:
        dot.clear_updaters()


def flow_in(dots, shift=DOWN * 0.48, run_time=1.8):
    return LaggedStart(*(FadeIn(dot, shift=shift) for dot in dots),
                       lag_ratio=0.22, run_time=run_time)


def label(text, x, y, color=TEXT, size=32):
    return T(text, size, color).move_to(at_xy(x, y))


def diagram_tag():
    return scope_tag(size=28, color=TEXT)


def prediction_card():
    return question_card(QUESTION, y=3.31, size=39)


def prediction_world():
    """Rebuild the last spoken question frame for both the pause and answer."""
    membrane = cell("stalled")
    copy = gene(RESCUE, ORANGE)
    ribbon = message()
    return membrane, copy, ribbon, guide(), target_frame(ribbon)


class S01Hook(TitleCard, SpokenScene):
    TITLE = "Putting the Gene Back to Prove Cause"
    LESSON = "Rescue experiments"

    def construct(self):
        membrane = cell(center=at_xy(-1.8, -0.32))
        working = gene(at_xy(-1.85, 0.60))
        gene_name = label("Gene", -1.85, 1.30, PURPLE)
        self.add(membrane, working, gene_name, diagram_tag())
        breathe(membrane)
        self.at("silence a gene")
        wedge = Triangle(color=RED, stroke_width=0, fill_opacity=0.95).scale(0.40).rotate(PI)
        wedge.move_to(at_xy(-1.85, 2.45))
        self.play(FadeOut(gene_name), FadeIn(wedge, shift=DOWN * 0.35), run_time=0.32)
        self.play(wedge.animate.move_to(at_xy(-1.85, 1.14)), run_time=0.43)
        self.at("cell breaks")
        membrane.clear_updaters()
        self.play(Transform(membrane, cell("stalled", center=membrane.get_center())),
                  working.animate.set_opacity(0.25), run_time=0.58)
        self.at("did losing it")
        question = label("?", 4.36, -0.10, GOLD, size=122)
        self.play(GrowFromCenter(question), run_time=1.05)
        bob(question, amp=0.12, speed=2.1)
        self.at("maybe not")
        question.clear_updaters()
        title = T(self.TITLE, 38, TEXT, font=TITLE_FONT).move_to(at_xy(-0.70, 3.06))
        lesson = label(self.LESSON, -0.70, 3.59, GOLD, 28)
        title_card = VGroup(lesson, title)
        self.play(FadeIn(title_card), run_time=0.27)
        self.wait(0.94)
        self.play(FadeOut(title_card), run_time=0.27)
        wrong_target = gene(at_xy(0.48, 0.88), width=1.55)
        self.at("silencing tool can")
        self.play(FadeIn(wrong_target), run_time=0.43)
        self.at("hit the wrong")
        self.play(wedge.animate.move_to(at_xy(0.48, 1.56)), run_time=1.05)
        self.play(wrong_target.animate.set_opacity(0.28), run_time=0.45)
        self.at("rescue experiment")
        self.play(FadeOut(wedge), FadeOut(question), FadeOut(wrong_target),
                  membrane.animate.move_to(CELL_CENTER), run_time=0.9)
        self.at("putting a working")
        copy = gene(RESCUE, ORANGE)
        self.play(FadeOut(working), FadeIn(copy, shift=LEFT * 3.0), run_time=1.2)
        self.finish()


class S02HowRescueWorks(SpokenScene):
    def construct(self):
        membrane = cell()
        original = gene()
        ribbon = message()
        dots = proteins()
        guide_piece = guide(at_xy(2.01, 0.83))
        self.add(membrane, original, diagram_tag())
        breathe(membrane)
        self.at("gene makes")
        self.play(LaggedStart(*(FadeIn(b, shift=DOWN * 0.55) for b in ribbon),
                              lag_ratio=0.14), run_time=1.1)
        mrna_name = label("mRNA", -4.02, -0.07, PURPLE)
        self.play(FadeIn(mrna_name), run_time=0.30)
        self.at("to build")
        self.play(flow_in(dots, run_time=1.65))
        drift_dots(dots)
        protein_name = label("Protein", -0.7, -2.65, GREEN)
        self.play(FadeIn(protein_name), run_time=0.32)
        self.at("silencing guide")
        self.play(FadeIn(guide_piece, shift=LEFT * 0.9), run_time=0.85)
        guide_name = label("shRNA", 2.48, 0.35, RED)
        self.play(FadeIn(guide_name), run_time=0.4)
        self.at("pairs with that")
        landing = ribbon[TARGET].get_center() + UP * 0.17
        self.play(FadeOut(guide_name), run_time=0.25)
        self.play(guide_piece.animate.move_to(landing), run_time=1.10)
        self.at("protein vanishes")
        stop_drift(dots)
        self.play(LaggedStart(*(FadeOut(d) for d in dots), lag_ratio=0.20),
                  FadeOut(protein_name), run_time=1.2)
        self.at("the cell breaks")
        membrane.clear_updaters()
        self.play(Transform(membrane, cell("stalled")),
                  FadeOut(mrna_name), FadeOut(ribbon), FadeOut(guide_piece), run_time=0.65)
        self.at("if losing it caused")
        panels = TwoPanel("On-target", "Off-target", colors=(GREEN, RED),
                          top=2.82, bottom=-2.65, size=36)
        left_center = panels.area("left")[0]
        right_center = panels.area("right")[0]
        left = cell("stalled", left_center, 4.92, 3.72)
        right = cell("stalled", right_center, 4.92, 3.72)
        self.play(Transform(membrane, left), FadeIn(right, shift=RIGHT * 0.35),
                  FadeIn(panels), FadeOut(original), run_time=1.25)
        self.at("adding a working")
        copies = [gene(c + UP * 0.95, ORANGE, width=1.95) for c in (left_center, right_center)]
        self.play(*(FadeIn(copy, shift=LEFT * 0.7) for copy in copies), run_time=0.8)
        left_dots = proteins(left_center, 0.60)
        right_dots = proteins(right_center, 0.60)
        self.at("should cure it")
        self.play(Transform(membrane, cell("healthy", left_center, 4.92, 3.72)),
                  flow_in(left_dots, run_time=1.25), run_time=1.25)
        breathe(membrane)
        drift_dots(left_dots)
        self.at("off target hit")
        self.play(flow_in(right_dots, run_time=1.45),
                  right.animate.set_stroke(RED, width=6), run_time=1.45)
        self.at("the defect stays")
        right_note = label("Defect stays", 3.30, -3.18, RED)
        self.play(FadeIn(right_note), run_time=0.50)
        self.finish()


class S03PredictQ(SpokenScene):
    def construct(self):
        membrane, copy, ribbon, clamp, outline = prediction_world()
        entry_guide = guide(at_xy(2.01, 0.83))
        self.add(membrane, entry_guide, diagram_tag())
        self.at("there is a catch")
        self.play(FadeIn(copy, shift=LEFT * 2.65), run_time=1.8)
        self.at("shrna is")
        self.play(LaggedStart(*(FadeIn(b, shift=DOWN * 0.62) for b in ribbon),
                              lag_ratio=0.18), run_time=1.65)
        self.at("ready to silence")
        self.play(Transform(entry_guide, clamp), run_time=0.99)
        self.at("matching message")
        self.play(Create(outline), run_time=0.64)
        self.at("so predict")
        self.play(FadeIn(prediction_card(), shift=UP * 0.15), run_time=0.78)
        world = VGroup(membrane, copy, ribbon, entry_guide, outline)
        self.at("rescue copy make")
        self.play(world.animate.scale(1.09, about_point=at_xy(0, 0.05)), run_time=2.35)
        self.at("escape that guide")
        self.play(world.animate.scale(1 / 1.09, about_point=at_xy(0, 0.05)), run_time=2.10)
        self.finish()


class S04PredictPause(PredictPause):
    QUESTION = QUESTION
    SECONDS = 4.5

    def construct(self):
        membrane, copy, ribbon, clamp, outline = prediction_world()
        self.add(membrane, copy, ribbon, clamp, outline, prediction_card(), diagram_tag())
        origin = clamp.get_center()
        phase = ValueTracker(0)
        clamp.add_updater(lambda mob: mob.move_to(origin + RIGHT * 0.30 * np.sin(phase.get_value())))
        outline.add_updater(lambda mob: mob.set_fill(opacity=0.37 * np.sin(phase.get_value() / 2)**2))
        pulse(outline, base=3.5, amp=1.5, speed=2.4)
        self.play(phase.animate.set_value(TAU), run_time=self.narration_s, rate_func=linear)


class S05PredictAnswer(SpokenScene):
    def construct(self):
        membrane, copy, ribbon, clamp, outline = prediction_world()
        question = prediction_card()
        self.add(membrane, copy, ribbon, clamp, outline, question, diagram_tag())
        self.at("change the codons")
        zoom = 1.19
        spotlight = at_xy(0, 0.05)
        world = VGroup(membrane, copy, ribbon, clamp, outline)
        self.play(FadeOut(question), world.animate.scale(zoom, about_point=spotlight), run_time=1.1)
        alternative = message(changed=True).scale(zoom, about_point=spotlight)
        self.at("target site")
        self.play(LaggedStart(*(Transform(ribbon[i], alternative[i]) for i in range(3, 6)),
                              lag_ratio=0.34), run_time=0.90)
        codon_name = label("Synonymous codons", 0, 3.35, YELLOW, 37)
        self.at("synonymous codons")
        self.play(FadeIn(codon_name), run_time=0.58)
        self.at("different codes")
        # Identical output shapes under the old and new versions of the target.
        output = VGroup(*[protein(ribbon[i].get_center() + DOWN * 1.05, 0.24) for i in range(3, 6)])
        self.play(flow_in(output, run_time=1.0))
        output_name = label("Same amino acids", 0.10, -2.0, GREEN)
        self.at("same amino acid")
        self.play(FadeIn(output_name), run_time=0.65)
        self.at("silent mutations")
        self.play(world.animate.shift(RIGHT * 0.62),
                  VGroup(output, output_name).animate.shift(RIGHT * 0.62), run_time=1.50)
        self.at("the guide no longer")
        self.play(clamp.animate.shift(RIGHT * 2.42 + DOWN * 0.18), run_time=2.02)
        self.at("yet the amino")
        self.play(world.animate.scale(1 / zoom, about_point=spotlight),
                  Indicate(output, color=GREEN, scale_factor=1.15), run_time=1.5)
        self.at("the protein returns")
        dots = proteins()
        membrane_target = cell()
        self.play(FadeOut(output_name), FadeOut(codon_name), run_time=0.30)
        self.play(Transform(membrane, membrane_target), FadeOut(copy), FadeOut(ribbon),
                  FadeOut(clamp), FadeOut(outline), FadeOut(output),
                  flow_in(dots, run_time=1.60), run_time=1.60)
        breathe(membrane)
        drift_dots(dots)
        self.finish()


def blot():
    center = at_xy(3.77, -0.20)
    plate = block(5.38, 4.5, BLUE, center, fill=0.33, stroke=3.2, radius=0.23)
    xs = [2.06, 3.75, 5.44]
    bands = VGroup()
    for x, thickness, opacity in zip(xs, (0.24, 0.12, 0.53), (0.88, 0.40, 1.0)):
        bands.add(block(1.13, thickness, TEXT, at_xy(x, -0.27), fill=opacity,
                        stroke=0, radius=0.045))
    labels = VGroup(*[label(word, x, -1.64, TEXT, 28)
                      for word, x in zip(("Normal", "Too low", "Too high"), xs)])
    return plate, bands, labels


class S06ControlLevel(SpokenScene):
    def construct(self):
        membrane = cell()
        dots = proteins()
        side = at_xy(-3.38, -0.32)
        side_dots = proteins(side, 0.60)
        tag = diagram_tag()
        self.add(membrane, dots, tag)
        self.at("a rescue can mislead")
        self.play(Transform(membrane, cell(center=side, width=6.12, height=5.45)),
                  Transform(dots, side_dots), run_time=1.55)
        plate, bands, names = blot()
        self.at("levels are wrong")
        self.play(FadeIn(plate, shift=LEFT * 0.25), FadeIn(bands[0]), run_time=0.9)
        self.play(FadeIn(names[0]), run_time=0.30)
        self.at("a failed rescue")
        keep = dots[1]
        self.play(FadeOut(VGroup(*[dot for dot in dots if dot is not keep])),
                  Transform(membrane, cell("stalled", side, 6.12, 5.45)), FadeIn(bands[1]),
                  run_time=1.35)
        self.play(FadeIn(names[1]), run_time=0.35)
        self.at("folded placed")
        misfolded = Ellipse(width=0.47, height=0.17, stroke_width=0,
                            fill_color=GREEN, fill_opacity=0.63).rotate(0.62)
        misfolded.move_to(keep.get_center() + UP * 2.15 + RIGHT * 1.05)
        self.play(Transform(keep, misfolded), membrane.animate.set_fill(opacity=0.17), run_time=1.20)
        self.at("near normal levels")
        self.play(Indicate(bands[0], color=BLUE, scale_factor=1.08), run_time=1.65)
        self.at("far too much")
        crowd = VGroup(*[protein(side + at_xy(x, y), radius=0.19)
                        for x, y in [(-1.9, -0.55), (-1.55, 0.45), (-1.20, -1.25),
                                     (-1.15, 1.25), (-0.89, -0.14), (-0.56, -0.78),
                                     (-0.56, 0.65), (-0.09, 1.34), (0.04, -1.43),
                                     (0.19, 0.05), (0.61, -0.70), (0.67, 0.88),
                                     (1.23, 1.29), (1.26, -1.26), (1.45, 0.20),
                                     (2.0, -0.46), (2.05, 0.73)]])
        self.play(flow_in(crowd, run_time=1.93), FadeOut(keep), FadeIn(bands[2]),
                  Transform(membrane, cell("crowded", side, 6.12, 5.45)), run_time=1.93)
        drift_dots(crowd)
        self.at("effects of its own")
        self.play(FadeIn(names[2]), Indicate(bands[2], color=RED, scale_factor=1.12), run_time=1.55)
        self.at("an immunoblot")
        heading = label("Immunoblot", 3.77, 2.57, BLUE, 36)
        self.play(FadeIn(heading), run_time=0.72)
        self.at("an antibody test")
        stop_drift(crowd)
        matched = proteins(side, 0.60)
        self.play(FadeOut(crowd), Transform(membrane, cell(center=side, width=6.12, height=5.45)),
                  flow_in(matched, run_time=1.35), Indicate(bands[0], color=BLUE, scale_factor=1.13),
                  run_time=1.35)
        breathe(membrane)
        drift_dots(matched)
        self.finish()


def apg_locus():
    return gene(at_xy(-1.35, 0.97), PURPLE, broken=True)


class S07LimitSuppressor(SpokenScene):
    def construct(self):
        side = at_xy(-3.38, -0.32)
        membrane = cell(center=side, width=6.12, height=5.45)
        dots = proteins(side, 0.60)
        self.add(membrane, dots, diagram_tag())
        locus = apg_locus()
        self.at("even a working rescue")
        self.play(Transform(membrane, cell()), Transform(dots, proteins()), run_time=1.55)
        self.play(Transform(membrane, cell("stalled")), FadeOut(dots), FadeIn(locus), run_time=1.15)
        self.at("extra copies")
        extra = VGroup(*[gene(at_xy(1.25 + i * 0.40, 0.25 - i * 0.51),
                               ORANGE, width=1.70) for i in range(3)])
        self.play(LaggedStart(*(FadeIn(g, shift=LEFT * 0.80) for g in extra),
                              lag_ratio=0.54), run_time=1.55)
        self.at("can suppress")
        bypass = ArcBetweenPoints(at_xy(3.02, -0.73), at_xy(-1.6, -1.24), angle=-0.82)
        bypass.set_stroke(GREEN, width=5, opacity=0.72)
        self.play(Create(bypass), run_time=1.3)
        self.at("overexpressed")
        apg1 = label("Extra APG1", 1.64, 1.04, ORANGE, 32)
        apg13 = label("Broken apg13", -1.35, 1.73, PURPLE, 32)
        self.play(extra.animate.shift(RIGHT * 0.36 + DOWN * 0.20), run_time=0.68)
        self.play(FadeIn(apg1), FadeIn(apg13), run_time=0.48)
        passing = VGroup(*[protein(bypass.get_start(), 0.19) for _ in range(3)])
        self.at("rescues")
        self.play(LaggedStart(*(MoveAlongPath(p, bypass) for p in passing), lag_ratio=0.33),
                  run_time=1.65)
        revived = proteins()
        self.play(FadeOut(passing), flow_in(revived, run_time=0.90),
                  Transform(membrane, cell()), run_time=0.9)
        breathe(membrane)
        drift_dots(revived)
        self.at("sequencing the mutant")
        checks = Ledger([("Sequence", "Mutant allele", BLUE),
                         ("Remake", "Use a clean strain", BLUE)],
                        top_left=(-3.75, 0.78), key_w=2.95, width=9.1, row_h=1.10, size=34)
        scan = Rectangle(width=0.15, height=0.80, stroke_width=0,
                         fill_color=BLUE, fill_opacity=0.84).move_to(locus.get_left())
        self.play(FadeOut(apg1), FadeOut(extra), FadeOut(bypass), FadeIn(scan), run_time=0.35)
        self.play(scan.animate.move_to(locus.get_right()), run_time=0.85)
        self.play(FadeOut(scan), FadeOut(locus), FadeOut(apg13), run_time=0.28)
        self.play(checks.reveal(0), run_time=0.30)
        self.at("remaking the mutation")
        membrane.clear_updaters()
        stop_drift(revived)
        self.play(Transform(membrane, cell("stalled")), FadeOut(revived),
                  checks.reveal(1), run_time=0.85)
        fresh_locus = gene(at_xy(0.65, -1.08), PURPLE, broken=True)
        self.play(FadeIn(fresh_locus, shift=DOWN * 0.28), run_time=0.65)
        self.at("rules out")
        self.play(Indicate(fresh_locus, color=YELLOW, scale_factor=1.10), run_time=1.20)
        self.finish()


def yeast_rod(center=CELL_CENTER):
    return block(10.15, 3.16, GREY, center, fill=0.30, stroke=6, radius=1.48)


def yeast_daughters():
    return VGroup(*[block(4.8, 3.16, TEAL, CELL_CENTER + RIGHT * x,
                          fill=0.34, stroke=6, radius=1.48) for x in (-2.68, 2.68)])


def split_yeast(scene, rod):
    daughters = yeast_daughters()
    center = rod.get_center()
    furrow = Line(center + UP * 1.49, center + DOWN * 1.49, color=GREEN, stroke_width=7)
    scene.play(GrowFromCenter(furrow), run_time=0.65)
    scene.play(ReplacementTransform(rod, daughters), FadeOut(furrow), run_time=1.1)
    return daughters


class S08UnlockedYeast(SpokenScene):
    def construct(self):
        membrane = cell("stalled")
        old_locus = gene(at_xy(0.65, -1.08), PURPLE, broken=True)
        self.add(membrane, old_locus, diagram_tag())
        self.at("used carefully")
        self.play(Transform(membrane, yeast_rod()), FadeOut(old_locus), run_time=2.55)
        self.at("across species")
        self.play(membrane.animate.set_fill(opacity=0.40), run_time=1.65)
        self.at("in 1982")
        date = label("1982", -4.92, 2.75, GOLD, 41)
        self.play(FadeIn(date), run_time=0.6)
        self.at("david beach")
        investigators = label("David Beach · Barbara Durkacz · Paul Nurse", 0.0, -2.92, TEXT, 31)
        self.play(FadeIn(investigators), membrane.animate.set_fill(opacity=0.29), run_time=0.9)
        self.at("fission yeast")
        mutant = label("cdc2 mutant", -0.70, 0.12, PURPLE, 40)
        self.play(FadeIn(mutant), membrane.animate.set_fill(opacity=0.45), run_time=1.4)
        self.at("they added")
        donor = gene(at_xy(1.81, 1.83), ORANGE, width=2.55)
        self.play(FadeIn(donor, shift=LEFT * 2.0), FadeOut(investigators),
                  membrane.animate.set_fill(opacity=0.30), run_time=1.30)
        donor_name = label("Budding yeast · CDC28", 1.96, 2.53, ORANGE, 34)
        self.at("carrying cdc28")
        self.play(FadeIn(donor_name), donor.animate.shift(DOWN * 1.09), run_time=0.86)
        self.at("two distant yeasts")
        self.play(FadeOut(mutant), run_time=0.32)
        daughters = split_yeast(self, membrane)
        self.at("in 1987")
        new_date = label("1987", -4.92, 2.75, GOLD, 41)
        rod = yeast_rod()
        self.play(ReplacementTransform(daughters, rod), FadeOut(donor), FadeOut(donor_name),
                  FadeIn(mutant), swap(date, new_date, run_time=0.95), run_time=1.1)
        self.at("a human gene")
        donor = gene(at_xy(1.81, 0.74), ORANGE, width=2.55)
        human = label("Human gene", 1.96, 2.53, ORANGE, 34)
        self.play(FadeIn(donor, shift=LEFT * 1.5), FadeIn(human), run_time=0.70)
        self.at("that same mutant")
        self.play(FadeOut(mutant), run_time=0.23)
        split_yeast(self, rod)
        self.play(FadeOut(donor), FadeOut(human), FadeOut(new_date), run_time=0.30)
        self.finish()


def budding_yeast():
    return VGroup(cell(center=at_xy(-1.02, -0.26), width=5.25, height=5.0),
                  cell(center=at_xy(2.17, 1.06), width=2.27, height=2.34))


def assay_bar():
    center = at_xy(0, -0.06)
    return block(11.7, 2.37, GREY, center, fill=0.32, stroke=4.0, radius=0.23)


def assay_fill(bar, fraction):
    """Map the reported fraction to the width inside the full 414-gene bar."""
    inset = 0.12
    width = (bar.width - 2 * inset) * fraction
    center = bar.get_left() + RIGHT * (inset + width / 2)
    return block(width, bar.height - 2 * inset, GREEN, center, fill=0.79,
                 stroke=0, radius=0.13)


def reveal_bar_segment(segment):
    """Reveal a bar segment along its measured dimension, keeping its height fixed."""
    collapsed = segment.copy().stretch_to_fit_width(0.02, about_point=segment.get_left())
    return TransformFromCopy(collapsed, segment)


class S09UnlockedOrthologs(SpokenScene):
    def construct(self):
        daughters = yeast_daughters()
        self.add(daughters, diagram_tag())
        bud = budding_yeast()
        self.at("in 2015")
        self.play(ReplacementTransform(daughters, bud), run_time=1.25)
        date = label("2015", -4.92, 2.75, GOLD, 41)
        self.play(FadeIn(date), run_time=0.6)
        byline = label("Aashiq Kachroo · Edward Marcotte", -0.42, -3.18, TEXT, 32)
        self.play(FadeIn(byline), run_time=1.0)
        self.at("tested matching")
        yeast_gene = gene(at_xy(-1.13, -0.30), PURPLE)
        human_gene = gene(at_xy(-1.13, -0.30), ORANGE)
        self.play(FadeIn(yeast_gene), run_time=0.68)
        self.at("human genes in place")
        self.play(FadeOut(yeast_gene), run_time=0.45)
        self.play(FadeIn(human_gene, shift=LEFT * 1.45), run_time=1.5)
        self.at("414 genes yeast")
        bar = assay_bar()
        self.play(ReplacementTransform(bud, bar), FadeOut(human_gene), FadeOut(date), FadeOut(byline),
                  run_time=1.50)
        total = label(f"{TESTED} genes yeast needs", 0, 1.98, TEXT, 39)
        self.play(FadeIn(total), run_time=0.65)
        self.at("176 restored growth")
        fill = assay_fill(bar, FRACTION)
        self.play(reveal_bar_segment(fill), run_time=2.1)
        inside = label(f"{RESTORED} restored growth", fill.get_x(), fill.get_y(), BG, 34)
        self.play(FadeIn(inside), run_time=0.57)
        self.at("dividing 176")
        formula = VGroup(M(f"{RESTORED}", 42, GREEN), M("/", 42),
                         M(f"{TESTED}", 42), M(f"≈ {FRACTION:.0%}", 42, GREEN))
        formula.arrange(RIGHT, buff=0.30).move_to(at_xy(-2.15, -2.25))
        self.play(FadeIn(formula[0]), fill.animate.set_fill(opacity=0.98), run_time=0.65)
        self.at("by 414")
        self.play(FadeIn(VGroup(formula[1], formula[2])),
                  bar.animate.set_fill(opacity=0.48), run_time=0.76)
        self.at("43 percent")
        self.play(FadeIn(formula[3]), fill.animate.set_fill(opacity=0.79), run_time=0.70)
        self.at("47 percent")
        # This published summary includes earlier cases and has a different denominator.
        x = bar.get_left()[0] + 0.12 + (bar.width - 0.24) * 0.47
        tick = Line(at_xy(x, 1.12), at_xy(x, 2.49), color=GOLD, stroke_width=5)
        earlier = label("47% with earlier cases", 2.55, 2.90, GOLD, 34)
        marker_scope = label("schematic", 2.55, 2.33, TEXT, 28)
        self.play(FadeOut(total), run_time=0.28)
        self.play(GrowFromEdge(tick, DOWN), run_time=0.62)
        self.play(FadeIn(earlier), FadeIn(marker_scope), run_time=0.63)
        self.at("failed swaps")
        remainder = block(bar.get_right()[0] - fill.get_right()[0] - 0.24, 2.13, GREY,
                          at_xy((bar.get_right()[0] + fill.get_right()[0]) / 2, -0.06),
                          fill=0.29, stroke=0, radius=0.12)
        self.play(reveal_bar_segment(remainder), run_time=1.5)
        self.at("failure has several")
        note = label("Failure has several causes", 2.52, -0.06, TEXT, 34)
        self.play(FadeIn(note), run_time=0.85)
        self.finish()


EMBRYO_ANGLE = -0.10


def embryo(center, width=7.25, height=4.9):
    """A whole-embryo profile with the dorsalized state shaded uniformly."""
    outline = Ellipse(width=width, height=height, stroke_color=GREY, stroke_width=6,
                      fill_color=PURPLE, fill_opacity=0.35).rotate(EMBRYO_ANGLE).move_to(center)
    outline.semi_axes = (width / 2, height / 2)
    return outline


def embryo_edges(shell, x):
    """Give the lower and upper membrane positions at a given horizontal coordinate."""
    a, b = shell.semi_axes
    c, s = np.cos(EMBRYO_ANGLE), np.sin(EMBRYO_ANGLE)
    span = np.hypot(a * c, b * s)
    phase = np.arctan2(-b * s, a * c)
    offset = np.arccos((x - shell.get_x()) / span)
    angles = phase + np.array([-offset, offset])
    return shell.get_y() + a * s * np.cos(angles) + b * c * np.sin(angles)


def injection_site(shell, x):
    return at_xy(x, embryo_edges(shell, x)[0])


def ventral_band(shell, x):
    """The ventralmost domain grows from the exact entry site on the membrane."""
    offsets = np.linspace(-1.0, 1.0, 17)
    xs = x + 0.63 * offsets
    bottom, top = np.array([embryo_edges(shell, xi) for xi in xs]).T
    profile = 0.66 * np.sqrt(np.maximum(0, 1 - offsets**2))
    upper = bottom + (top - bottom) * profile
    edge = [at_xy(xi, y) for xi, y in zip(xs, upper)]
    edge.extend(at_xy(xi, y) for xi, y in zip(xs[::-1], bottom[::-1]))
    return Polygon(*edge, stroke_color=ORANGE, stroke_width=3.5,
                   fill_color=ORANGE, fill_opacity=0.76)


def needle(tip):
    tail = tip + at_xy(-1.05, -1.0)
    return VGroup(
        Line(tail, tip + at_xy(-0.18, -0.17), color=BLUE, stroke_width=10),
        Line(tip + at_xy(-0.23, -0.21), tip, color=TEXT, stroke_width=4),
        Line(tail + at_xy(-0.16, 0.16), tail + at_xy(0.16, -0.16), color=BLUE, stroke_width=7),
    )


class S10UnlockedFly(SpokenScene):
    def construct(self):
        first = embryo(at_xy(-0.70, 0.08))
        bar = assay_bar()
        chart = VGroup(bar, assay_fill(bar, FRACTION))
        self.add(chart, diagram_tag())
        self.at("rescue can also")
        self.play(ReplacementTransform(chart, first), run_time=2.6)
        self.at("in 1985")
        heading = label("1985 · Toll mutant mother", -1.00, 3.24, GOLD, 37)
        self.play(FadeIn(heading), run_time=0.70)
        self.at("anderson and colleagues")
        researcher = label("Kathryn Anderson and colleagues", -0.7, -3.0, TEXT, 33)
        self.play(FadeIn(researcher), run_time=0.65)
        self.at("fly embryos from")
        self.play(first.animate.set_fill(opacity=0.50), run_time=1.85)
        self.at("those dorsalized embryos")
        dorsal = label("Dorsalized embryo", -0.7, 0.12, TEXT, 39)
        self.play(FadeOut(researcher), FadeIn(dorsal), run_time=0.70)
        self.at("lack ventral")
        self.play(first.animate.set_fill(opacity=0.35), run_time=1.92)
        self.at("injected wild type")
        x_left = -2.55
        entry = injection_site(first, x_left)
        syringe = needle(entry)
        sample = label("Wild-type cytoplasm", 2.68, -2.9, ORANGE, 34)
        self.play(FadeOut(dorsal), FadeIn(syringe, shift=at_xy(0.62, 0.56)), run_time=0.94)
        self.play(FadeIn(sample), run_time=0.45)
        self.at("ventral most part")
        band = ventral_band(first, x_left)
        self.play(GrowFromEdge(band, DOWN), FadeOut(syringe), run_time=1.28)
        self.at("pattern form")
        first_small = embryo(at_xy(-3.30, 0.05), 5.74, 4.12)
        second = embryo(at_xy(3.30, 0.05), 5.74, 4.12)
        moved_band = ventral_band(first_small, -4.76)
        self.play(Transform(first, first_small), Transform(band, moved_band),
                  FadeOut(sample), FadeIn(second), run_time=0.99)
        x_right = 4.55
        second_needle = needle(injection_site(second, x_right))
        self.play(FadeIn(second_needle, shift=at_xy(0.50, 0.49)), run_time=0.58)
        self.at("needle went in")
        second_band = ventral_band(second, x_right)
        self.play(GrowFromEdge(second_band, DOWN), FadeOut(second_needle), run_time=1.22)
        self.at("putting the missing")
        self.play(first.animate.set_fill(opacity=0.23), second.animate.set_fill(opacity=0.23),
                  band.animate.set_fill(opacity=0.94), second_band.animate.set_fill(opacity=0.94),
                  run_time=1.65)
        self.finish()


class S11End(EndCard):
    LINE = "If losing a gene breaks function, putting it back should restore it."
