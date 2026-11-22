"""Testing One Kinase Outside the Cell.

Colour map from the patch-clamp film: blue apparatus, grey structure,
purple kinases/receptors, yellow phosphate/signal, green controls/activity,
red inhibition, orange additions, teal sample/fluid, gold history and rule.
"""
from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
GLASS = "#234657"
READER = "#182433"
PAPER = "#BCCBD6"
BAND = "#19273A"
L, R = -3.24, 3.24
QUESTION = "Does a darker band prove more phosphate?"


def p(x, y):
    return np.array([x, y, 0.0])


def label(words, x, y, color=TEXT, size=31, width=5.55):
    return fit_text(words, max_w=width, size=size, min_size=28,
                    color=color, max_lines=2).move_to(p(x, y))


def tile(x, y, w, h, color, border=None, radius=0.17):
    return RoundedRectangle(width=w, height=h, corner_radius=radius,
                            stroke_color=border or color, stroke_width=2 if border else 0,
                            fill_color=color, fill_opacity=1).move_to(p(x, y))


def phosphate(x, y, r=0.17):
    return VGroup(Dot(p(x, y), radius=1.55 * r, color=YELLOW, fill_opacity=0.17),
                  Dot(p(x, y), radius=r, color=YELLOW))


def kinase(x, y, scale=1):
    body = VGroup(
        Ellipse(width=1.68, height=1.16, stroke_width=2, stroke_color=PURPLE,
                fill_color="#75568E", fill_opacity=1).rotate(0.26).move_to(p(-0.36, 0.22)),
        Ellipse(width=1.54, height=0.96, stroke_width=2, stroke_color=PURPLE,
                fill_color="#594474", fill_opacity=1).rotate(-0.31).move_to(p(0.39, -0.31)),
    )
    return body.scale(scale).move_to(p(x, y))


def substrate(x, y, w=3.75):
    return VGroup(tile(x, y, w, 0.52, "#237782", TEAL),
                  Dot(p(x + 0.73, y), radius=0.14, color=BG, stroke_color=TEAL, stroke_width=2))


def antibody(x, y, scale=1):
    branches = VGroup(Line(p(0, -0.75), p(0, 0.1)),
                      Line(p(0, 0.1), p(-0.59, 0.72)),
                      Line(p(0, 0.1), p(0.59, 0.72)))
    return branches.set_stroke(ORANGE, 12 * scale).scale(scale).move_to(p(x, y))


def atp(x, y, labelled=True):
    dark = "#9D6036"
    body = VGroup(Line(p(x - .39, y), p(x, y), stroke_width=9, color=dark),
                  Dot(p(x - .39, y), radius=.16, color=ORANGE),
                  Dot(p(x, y), radius=.16, color=ORANGE))
    if not labelled:
        return body
    return body, Line(p(x + .13, y), p(x + .47, y), stroke_width=8, color=dark), phosphate(x + .61, y)


def drifting(mob, base, amp, speed, seed=0):
    # Elliptical convection stays inside the reserve assigned to each object.
    def move(shape, dt):
        shape.phase += dt * speed
        shape.move_to(base + p(amp * np.sin(shape.phase),
                               amp * 0.53 * np.sin(1.4 * shape.phase)))
    mob.phase = seed
    return mob.add_updater(move)


def stage():
    panels = TwoPanel("Reaction chamber", "Readout", colors=(BLUE, GREY),
                      top=3.02, bottom=-2.52, width=12.72, gap=.24, size=32)
    panels.left_frame.set_fill(GLASS, 1)
    panels.right_frame.set_fill(READER, 1)
    return panels


def fluid(live=True):
    bubbles = VGroup()
    for i, (x, y, r) in enumerate([
        (-5.52, 1.49, .22), (-4.78, 1.56, .15), (-1.05, 1.38, .20),
        (-5.49, .35, .22), (-1.01, .44, .15), (-5.23, -.56, .21),
        (-1.02, -.37, .24), (-5.51, -1.66, .23), (-4.7, -1.95, .16),
        (-1.63, -1.42, .17), (-1.93, 1.59, .13), (-1.04, -1.86, .24),
        (-5.58, -2.03, .16), (-1.71, -.91, .15)
    ]):
        bubble = Dot(p(x, y), radius=r, color="#749EA9", fill_opacity=.64)
        if live:
            drifting(bubble, p(x, y), .35, 1.57 + .15 * (i % 3), i)
        bubbles.add(bubble)
    return bubbles


def chamber(scene, readout=False, live=True):
    world = stage()
    scene.add(world.left_frame, world.left_head, fluid(live))
    if readout:
        scene.add(world.right_frame, world.right_head)
    return world


def reaction(marked=False):
    enzyme = kinase(L, .52, 1.18)
    protein = substrate(L, -1.12, 4.08)
    mark = phosphate(L + .73, -1.12)
    return VGroup(enzyme, protein, mark) if marked else VGroup(enzyme, protein)


def cell():
    membrane = Ellipse(width=12.35, height=6.15, stroke_color=TEAL,
                       stroke_width=3, fill_color="#224451", fill_opacity=1)
    return membrane.shift(DOWN * .1)


def crowd(live=True, reserve_candidate=False):
    enzymes = VGroup()
    for ring, (n, a, b) in enumerate([(12, 3.15, 1.36), (19, 5.38, 2.37)]):
        for i in range(n):
            angle = TAU * (i + ring * .36) / n
            pos = p(a * np.cos(angle), b * np.sin(angle) - .1)
            if abs(pos[0]) < 1.1 and 0 < pos[1] < 1.65:
                continue
            if reserve_candidate and ring == 0 and i == 5:
                continue
            shape = kinase(*pos[:2], scale=.36 + .045 * (i % 3)).rotate(.55 * np.sin(i))
            if live:
                drifting(shape, pos, .24 + .025 * (i % 4), 1.1 + .07 * (i % 4), i)
            enzymes.add(shape)
    return enzymes


class S01Hook(SpokenScene):
    def construct(self):
        enzymes = crowd()
        target = substrate(0, -.08, 3.25)
        dot = phosphate(-.23, 1.02, .21)
        self.add(cell(), enzymes, target)
        self.at("A phosphate just landed")
        self.add(dot)
        self.play(dot.animate.move_to(p(.73, -.08)), run_time=1.35, rate_func=rate_functions.ease_in_out_cubic)
        self.at("which enzyme put")
        question = label("?", 0, .69, YELLOW, 60)
        self.play(FadeIn(question, shift=UP * .23), run_time=.55)
        self.at("your genome holds")
        total = ValueTracker(0)
        count = counter("{:.0f}", total, p(-1.62, -3.53), size=41, color=TEXT)
        words = label("protein kinases", .75, -3.53, TEXT, 32)
        self.play(FadeOut(question), run_time=.26)
        self.add(count)
        self.play(total.animate.set_value(518), run_time=.72, rate_func=rate_functions.ease_out_cubic)
        self.play(FadeIn(words), run_time=.36)
        self.at("in a living cell")
        self.play(FadeOut(count), FadeOut(words), FadeIn(question), run_time=.5)
        self.finish()


class S02Title(TitleCard):
    LESSON = "In Vitro Kinase Assay"
    TITLE = "Testing One Kinase Outside the Cell"

    def construct(self):
        background = VGroup(cell(), crowd(False, reserve_candidate=True))
        question = label("?", 0, .69, YELLOW, 60)
        candidate = kinase(-2.73, .58, .45)
        target = substrate(0, -.08, 3.25)
        dot = phosphate(.73, -.08, .21)
        world = stage()
        prepared = reaction()
        self.add(background, candidate, target, dot, question)
        self.play(FadeOut(question), run_time=.16)
        self.play(FadeOut(background), FadeOut(dot), FadeIn(world.left_frame.set_z_index(-1)),
                  Transform(candidate, prepared[0]), Transform(target, prepared[1]),
                  run_time=.55)
        self.add(fluid(False).set_z_index(-.5))
        title = fit_text(self.TITLE, max_w=5.55, size=44, min_size=32, max_lines=2,
                         font=TITLE_FONT).move_to(p(R, .30))
        lesson = label(self.LESSON, R, 1.63, BLUE, 29)
        rule = Line(p(2.3, -1.08), p(4.2, -1.08), color=GOLD, stroke_width=4)
        self.play(FadeIn(title), FadeIn(lesson), GrowFromCenter(rule),
                  FadeIn(world.left_head), run_time=.38)
        self.wait(.59)
        self.play(FadeOut(title), FadeOut(lesson), FadeOut(rule), run_time=.30)


class S03Reaction(SpokenScene):
    def construct(self):
        world = chamber(self)
        kit = reaction()
        enzyme, protein = kit
        drifting(enzyme, enzyme.get_center(), .24, 1.64)
        self.add(kit)
        tag = scope_tag(size=28, color=TEXT)
        self.add(tag)
        self.at("isolate one suspect")
        focus = Circle(radius=1.65, color=PURPLE, stroke_width=3).move_to(p(L, .5))
        self.play(Create(focus), run_time=1.3)
        self.play(FadeOut(focus), run_time=.6)
        self.at("assay mixes")
        k = label("Purified kinase", L, 2.01, PURPLE, 32)
        self.play(FadeIn(k), run_time=.42)
        self.at("a substrate")
        s = label("Substrate", L, -1.81, BLUE, 31)
        self.play(FadeIn(s), run_time=.32)
        self.at("a tp with")
        self.play(FadeIn(world.right_frame), FadeIn(world.right_head), run_time=.48)
        body, bridge, end = atp(-2.28, -.28)
        packet = VGroup(body, bridge, end)
        self.play(FadeIn(packet, shift=LEFT * .19), run_time=.42)
        supply = label("Labelled ATP", R, .85, ORANGE, 39)
        supply_icon = VGroup(*atp(R - .1, -.2)).scale(1.95)
        self.play(FadeIn(supply_icon), run_time=.36)
        self.play(FadeIn(supply), run_time=.4)
        self.at("the kinase moves")
        gamma = label("Gamma phosphate", R, .85, YELLOW, 37)
        self.play(swap(supply, gamma, run_time=.72), run_time=.72)
        self.play(FadeOut(bridge), end.animate.move_to(p(L + .58, -.55)), run_time=1.35)
        self.at("onto serine")
        self.play(end.animate.move_to(p(L + .73, -1.12)),
                  body.animate.shift(p(-1.58, -.08)), FadeOut(supply_icon), run_time=.7)
        sites = label("Serine, threonine or tyrosine", R, -.66, TEAL, 34)
        self.play(FadeIn(sites), run_time=.6)
        adp = label("ADP", -4.97, -.36, ORANGE, 29)
        self.play(FadeIn(adp), run_time=.35)
        self.at("near ph 7")
        neg = label("Near pH 7", R, .85, TEXT, 35)
        self.play(swap(gamma, neg, run_time=.75), FadeOut(sites),
                  FadeOut(adp), FadeOut(body), run_time=.75)
        glow = Circle(radius=.37, color=YELLOW, stroke_width=4).move_to(end)
        self.add(pulse(glow, base=5, amp=2.8, speed=3.5))
        self.at("phosphate adds close")
        charge = label("About two negative charges", R, -.44, YELLOW, 36)
        self.play(FadeIn(charge), run_time=.75)
        self.wait(.7)
        self.play(FadeOut(glow), FadeOut(k), FadeOut(s), run_time=.45)
        self.finish()


def blot(x=R, y=-.15, opacity=.92, width=3.8, height=2.48):
    sheet = tile(x, y, width, height, PAPER)
    band = tile(x, y, width * .66, .43, BAND, radius=.12).set_fill(BAND, opacity)
    return sheet, band


def scissors(x, y):
    return VGroup(
        Line(p(x - .29, y + .24), p(x + .45, y - .41)),
        Line(p(x + .29, y + .24), p(x - .45, y - .41)),
        Circle(.14).move_to(p(x - .3, y + .29)),
        Circle(.14).move_to(p(x + .3, y + .29)),
    ).set_stroke(TEXT, 4)


class S04Detect(SpokenScene):
    def construct(self):
        chamber(self, True)
        self.add(reaction(True), scope_tag(size=28, color=TEXT))
        self.at("detect the transferred")
        sample = substrate(R, -.35, 4.52)
        mark = phosphate(R + .73, -.35, .22)
        self.play(FadeIn(sample, shift=LEFT * .48), FadeIn(mark, shift=LEFT * .48), run_time=1.35)
        self.at("track its label")
        direct = label("Label on substrate", R, 1.38, YELLOW, 34)
        halo = Circle(radius=.48, color=YELLOW, stroke_width=4).move_to(mark)
        self.play(FadeIn(direct), Create(halo), run_time=.55)
        pulse(halo, base=5, amp=3, speed=3.5)
        self.at("or use a phosphospecific")
        self.play(FadeOut(direct), FadeOut(halo), run_time=.4)
        y = antibody(R + .4, .66, .75).rotate(PI).shift(LEFT * .35)
        self.play(FadeIn(y, shift=UP * .35), run_time=.46)
        immune = label("Phosphospecific antibody", R, 1.77, ORANGE, 32)
        self.play(FadeIn(immune), run_time=.45)
        self.at("binds only")
        paper, band = blot(y=-1.5, height=.98, opacity=.12)
        self.play(y.animate.shift(RIGHT * .24 + DOWN * .24), FadeIn(paper), FadeIn(band), run_time=1.05)
        self.play(band.animate.set_fill(BAND, .94), run_time=1.45)
        self.at("to find unexpected sites")
        self.play(FadeOut(y), FadeOut(paper), FadeOut(band), FadeOut(immune), run_time=.58)
        self.at("the enzyme trypsin")
        blades = scissors(R - .67, .72)
        self.play(FadeIn(blades, shift=DOWN * .25), run_time=.43)
        trypsin = label("Trypsin", R, 1.65, TEXT, 34)
        self.play(FadeIn(trypsin), run_time=.36)
        self.at("cuts the protein")
        pieces = VGroup(*(tile(x, -.35, w, h, "#237782", TEAL)
                          for x, w, h in [(1.62, 1.2, .51), (3.47, 1.8, .74), (5.12, 1.12, .51)]))
        self.play(blades.animate.shift(DOWN * .42),
                  ReplacementTransform(sample, pieces), run_time=.73)
        peptides = label("Peptides", R, 1.65, TEAL, 34)
        self.play(FadeOut(blades), swap(trypsin, peptides),
                  mark.animate.shift(DOWN * .23),
                  *[piece.animate.shift(DOWN * (.23 + .18 * (i != 1))) for i, piece in enumerate(pieces)],
                  run_time=1.15)
        self.at("mass spectrometry weighs")
        # Unimod:21 gives +79.966331 Da. The baseline is the unmodified peptide's mass.
        plot = Plot(box=(.81, 5.83, -1.58, .83), xr=(-18, 113), yr=(0, 1),
                    xlabel="Mass shift", ylabel="Mass spectrometry", label_size=29, color=TEXT)
        baseline = Line(plot.pt(0, 0), plot.pt(0, .69), color=TEAL, stroke_width=6)
        delta = 79.966331
        peak = Line(plot.pt(delta, 0), plot.pt(delta, .69), color=YELLOW, stroke_width=6)
        self.play(FadeOut(peptides), FadeOut(pieces[0]), FadeOut(pieces[2]),
                  Create(plot), run_time=.55)
        moving_peptide = VGroup(pieces[1], mark)
        self.play(moving_peptide.animate.move_to(plot.pt(0, .40)).scale(.48), run_time=.52)
        self.play(FadeOut(moving_peptide), GrowFromEdge(baseline, DOWN), run_time=.44)
        self.at("one phosphate shows")
        self.play(TransformFromCopy(baseline, peak), run_time=.42)
        self.play(FadeIn(label("+1 phosphate", plot.pt(delta, 0)[0], .44, YELLOW, 32)), run_time=.28)
        self.finish()


def prediction():
    paper, band = blot()
    arrow = Arrow(p(R, 1.52), p(R, 1.20), color=YELLOW, buff=0,
                  tip_length=.15, stroke_width=4)
    signal = label("Signal", R, 1.81, YELLOW, 33)
    return paper, band, arrow, signal


def predict_card():
    return question_card(QUESTION, y=-3.17, size=36, max_w=11.7).shift(RIGHT * .5)


class S05Predict(SpokenScene):
    def construct(self):
        chamber(self, True)
        self.add(reaction(True))
        paper, band, arrow, signal = prediction()
        paper.scale(.75)
        band.scale(.75).set_fill(BAND, .17)
        self.at("suppose a signal")
        self.play(FadeIn(paper), FadeIn(band), run_time=.55)
        self.play(FadeIn(signal), GrowArrow(arrow), run_time=.64)
        self.at("band turns much")
        self.play(paper.animate.scale(1 / .75),
                  band.animate.scale(1 / .75).set_fill(BAND, .76), run_time=2.07)
        self.at("does that prove")
        self.play(FadeIn(predict_card()), run_time=.65)
        self.at("think of two")
        self.play(band.animate.set_fill(BAND, .92), run_time=2.25)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = QUESTION
    SECONDS = 4.5

    def construct(self):
        chamber(self, True, live=False)
        self.add(reaction(True), *prediction(), predict_card())
        start, end = p(-3.2, -3.61), p(3.2, -3.61)
        track = Line(start, end, color=READER, stroke_width=8)
        progress = Line(start, end, color=GOLD, stroke_width=8)
        self.add(track)
        self.play(Create(progress), rate_func=linear, run_time=self.SECONDS)


def lane_sheet():
    layout = tile(R, -.22, 5.03, 3.39, PAPER)
    slots = VGroup(*(tile(x, -.42, 1.23, 2.52, "#A7B9C7") for x in [1.56, R, 4.92]))
    return layout, slots


def lane_band(x, y, opacity):
    return tile(x, y, .94, .29, BAND, radius=.1).set_fill(BAND, opacity)


class S07Controls(SpokenScene):
    def construct(self):
        chamber(self, True)
        self.add(reaction(True))
        paper, original, arrow, signal = prediction()
        question = predict_card()
        self.add(paper, original, arrow, signal, question)
        self.at("the sample may hold")
        sheet, slots = lane_sheet()
        self.play(FadeOut(question), FadeOut(arrow), FadeOut(signal), run_time=.36)
        weak = lane_band(1.56, .38, .20).set_z_index(2)
        strong = lane_band(R, .38, .92).set_z_index(2)
        original.set_z_index(2)
        self.play(ReplacementTransform(paper, sheet), FadeIn(slots),
                  ReplacementTransform(original, strong), FadeIn(weak), run_time=1.38)
        phospho = label("Phosphate signal", R, 1.83, YELLOW, 30)
        self.play(FadeIn(phospho), run_time=.5)
        self.at("blot the same samples")
        whole = label("Whole protein", R, -2.2, GREEN, 29)
        amount_a, amount_b = lane_band(1.56, -.92, .18), lane_band(R, -.92, .18)
        self.play(FadeIn(amount_a), FadeIn(amount_b), run_time=.48)
        self.play(FadeIn(whole), run_time=.45)
        self.play(amount_a.animate.set_fill(BAND, .46), amount_b.animate.set_fill(BAND, .96), run_time=1.8)
        self.at("an antibody can bind")
        possible = lane_band(4.92, .38, .18)
        off_target = antibody(4.92, -.55, .49)
        self.play(FadeIn(off_target, shift=UP * .27), FadeIn(possible), run_time=1.12)
        self.at("run a control")
        self.play(FadeOut(off_target), FadeOut(possible), run_time=1.06)
        control = label("Control", 4.92, -2.2, GREEN, 29)
        whole_left = label("Whole protein", 2.35, -2.2, GREEN, 29)
        self.play(swap(whole, whole_left), FadeIn(control), run_time=.8)
        self.at("with those checks")
        statement = caption("A purified kinase shows what it can phosphorylate directly.",
                            size=33, color=GOLD, y=-3.12).shift(RIGHT * .9)
        self.play(FadeIn(statement), run_time=.7)
        self.finish()


def unknown_gauge():
    # Unknown occupancy has no assigned numeric value or needle position.
    g = Arc(radius=.69, start_angle=0, angle=PI, color=GREY,
            stroke_width=7).move_to(p(R, -1.07))
    return VGroup(g, label("?", R, -1.19, TEXT, 35),
                  label("Fraction unknown", R, -2.04, TEXT, 29))


class S08Limits(SpokenScene):
    def construct(self):
        world = chamber(self, True)
        parts = reaction(True)
        self.add(parts)
        sheet, slots = lane_sheet()
        previous = VGroup(sheet, slots, lane_band(1.56, .38, .20), lane_band(R, .38, .92),
                 lane_band(1.56, -.92, .46), lane_band(R, -.92, .96),
                 label("Phosphate signal", R, 1.83, YELLOW, 30),
                 label("Whole protein", 2.35, -2.2, GREEN, 29),
                 label("Control", 4.92, -2.2, GREEN, 29),
                 caption("A purified kinase shows what it can phosphorylate directly.",
                         size=33, color=GOLD, y=-3.12).shift(RIGHT * .9))
        self.add(previous)
        self.at("three limits remain")
        self.play(FadeOut(previous), world.left_frame.animate.set_fill("#1D3645", 1), run_time=.62)
        target = substrate(R, .39, 4.45)
        site = phosphate(R + .73, .39)
        other_site = phosphate(R - 1.03, .39)
        self.play(FadeIn(target), FadeIn(site), FadeIn(other_site), run_time=.74)
        self.at("an antibody misses")
        probe = antibody(R + .42, 1.24, .57).rotate(PI)
        self.play(FadeIn(probe, shift=UP * .25), run_time=.65)
        self.play(probe.animate.shift(RIGHT * .06 + DOWN * .15), run_time=.8)
        self.at("what fraction")
        gauge = unknown_gauge()
        self.play(FadeIn(gauge, shift=UP * .2), run_time=1.07)
        self.at("sites predicted")
        self.play(FadeOut(VGroup(target, site, other_site, probe, gauge)), run_time=.3)
        sequence = VGroup(*(tile(1.31 + .64 * i, .03, .52, .75,
                                  "#237782" if i != 4 else READER, TEAL)
                            for i in range(7)))
        self.play(LaggedStart(*(FadeIn(b, shift=RIGHT * .1) for b in sequence),
                              lag_ratio=.09), run_time=.34)
        self.at("tools like scansite")
        guess = label("Scansite guess", R, 1.36, GOLD, 34)
        self.play(FadeIn(guess), run_time=.52)
        self.at("someone finds the phosphate")
        empty = Circle(radius=.39, stroke_width=4, color=YELLOW).move_to(sequence[4])
        self.play(Create(empty), run_time=.72)
        self.at("and a cell free mix")
        self.play(FadeOut(VGroup(sequence, guess, empty)), run_time=.46)
        outline = Ellipse(width=5.05, height=3.39, color=TEAL, stroke_width=3,
                          fill_color="#224451", fill_opacity=1).move_to(p(R, -.03))
        in_cell = VGroup(kinase(1.85, .66, .47), substrate(4.06, -.89, 2.25))
        phosphatase = tile(4.35, .55, .92, .66, "#527146", GREEN)
        self.play(FadeIn(outline), FadeIn(in_cell), FadeIn(phosphatase), run_time=.9)
        ph_label = label("Phosphatase", 4.21, -.04, GREEN, 28)
        cell_label = label("Inside cells", R, 1.98, TEAL, 31)
        self.play(FadeIn(ph_label), FadeIn(cell_label), run_time=.55)
        self.at("kinase may mark targets")
        mark = parts[2]
        self.remove(parts)
        self.add(parts[0], parts[1])
        new_mark = phosphate(-3.34, .07)
        self.add(new_mark)
        self.play(new_mark.animate.move_to(mark), run_time=1.45)
        self.finish()


def receptor(x, y):
    return VGroup(tile(x, y + .23, .35, 1.13, "#75568E", PURPLE),
                  tile(x, y - .55, .68, .43, "#75568E", PURPLE),
                  VGroup(Dot(p(x - .21, y + .73), .28, color=PURPLE),
                         Dot(p(x + .21, y + .73), .28, color=PURPLE)))


def membranes():
    rail = VGroup(tile(L, -.39, 5.12, .20, GREY), tile(L, -.72, 5.12, .20, GREY))
    receptors = VGroup(*(receptor(x, -.56) for x in [-4.75, L, -1.72]))
    return rail, receptors


class S09UnlockedEgf(SpokenScene):
    def construct(self):
        chamber(self, True)
        base = reaction(True)
        self.add(base)
        rail, receptors = membranes()
        self.at("assay unlocked major")
        self.play(FadeOut(base), FadeIn(rail, shift=UP * .36), run_time=1.4)
        self.play(LaggedStart(*(FadeIn(r, shift=UP * .32) for r in receptors),
                              lag_ratio=.26), run_time=1.4)
        self.at("end of the 1970s")
        date = label("End of the 1970s", R, 1.67, GOLD, 36)
        self.play(FadeIn(date), run_time=.57)
        self.at("cohen's lab")
        institute = label("Vanderbilt University", R, .97, GOLD, 32)
        cohen = label("Cohen", R, .1, TEXT, 33)
        self.play(FadeIn(institute), run_time=.53)
        self.play(FadeIn(cohen), run_time=.46)
        self.at("membranes from")
        sample = label("A-431 tumor-cell membranes", L, 1.97, TEXT, 32)
        self.play(FadeIn(sample), run_time=.61)
        self.at("rich in receptors")
        signal = Dot(p(L, 1.03), radius=.25, color=ORANGE)
        self.play(GrowFromCenter(signal), run_time=.62)
        drifting(signal, signal.get_center(), .20, 2.44)
        self.at("growth factor egf")
        ligand_label = label("EGF", -2.15, .97, ORANGE, 29)
        self.play(FadeIn(ligand_label), run_time=.43)
        self.at("with graham carpenter")
        carpenter = label("Graham Carpenter", R, -.65, TEXT, 33)
        self.play(FadeIn(carpenter), run_time=.6)
        self.at("adding egf")
        signal.clear_updaters()
        self.play(FadeOut(ligand_label), signal.animate.move_to(p(L, .43)), run_time=.78)
        marks = VGroup(*(phosphate(x, -1.11, .14) for x in [-4.75, L, -1.72]))
        self.play(LaggedStart(*(FadeIn(dot, shift=DOWN * .3) for dot in marks),
                              lag_ratio=.24), run_time=1.71)
        self.at("hiroshi")
        ushiro = label("Hiroshi Ushiro", R, -1.37, TEXT, 33)
        self.play(FadeIn(ushiro), run_time=.53)
        self.at("landed on tyrosine")
        tyr = label("Tyrosine", R, -2.04, YELLOW, 34)
        self.play(FadeIn(tyr, shift=UP * .16), run_time=.51)
        self.finish()


def cam_ring():
    center = p(L, -.16)
    nodes = VGroup()
    for i in range(8):
        angle = TAU * i / 8
        pos = center + p(1.46 * np.cos(angle), 1.32 * np.sin(angle))
        nodes.add(kinase(*pos[:2], scale=.41).rotate(angle + PI / 2))
    return nodes


def calcium_wave():
    wave = Circle(radius=.28, color=TEAL, stroke_width=7).move_to(p(L, -.16))
    return Succession(GrowFromCenter(wave, run_time=.24),
                      wave.animate(run_time=.42).scale(5.45).set_stroke(opacity=.13),
                      FadeOut(wave, run_time=.14))


class S10UnlockedCamkii(SpokenScene):
    def construct(self):
        chamber(self, True)
        self.add(*membranes())
        old = VGroup(*self.mobjects[-2:])
        new = cam_ring()
        self.at("in 1998")
        self.play(FadeOut(old), FadeIn(new), run_time=1.16)
        author = label("De Koninck and Schulman", R, 1.89, GOLD, 31)
        year = label("1998", R, 1.32, GOLD, 30)
        self.play(FadeIn(author), FadeIn(year), run_time=.66)
        self.at("tested purified")
        name = label("CaM kinase II", L, 1.83, PURPLE, 34)
        self.play(FadeIn(name), run_time=.6)
        self.at("which calcium switches")
        calcium = label("Calcium pulses", L, -2.04, BLUE, 29)
        self.play(FadeIn(calcium), calcium_wave(), run_time=.86)
        self.wait(.86)
        self.play(calcium_wave(), run_time=.86)
        self.at("protein calmodulin")
        cams = VGroup(*(tile(x, y, .52, .27, ORANGE) for x, y in
                        [(-1.68, .10), (-2.14, .98)]))
        cam = label("Calmodulin", R, -.24, ORANGE, 34)
        self.play(FadeIn(cams[0], shift=LEFT * .3), run_time=.6)
        self.play(FadeIn(cam), run_time=.48)
        self.at("when two neighboring")
        self.play(calcium_wave(), run_time=.62)
        self.play(calcium_wave(), FadeIn(cams[1], shift=DOWN * .25), run_time=.62)
        self.play(calcium_wave(), run_time=.62)
        self.at("one can phosphorylate")
        mark = phosphate(-1.99, -.24, .14)
        self.play(FadeIn(mark), run_time=.45)
        self.play(mark.animate.move_to(p(-2.22, .60)), run_time=1.06)
        self.at("activity can persist")
        self.play(FadeOut(cams), FadeOut(cam), FadeOut(calcium), run_time=.75)
        # Approximate points from De Koninck & Schulman, Science 279 (1998), Fig. 3B.
        # Plot residual activity measured after stimulation, over increasing
        # numbers of 4 Hz or 1 Hz pulses. Interpolate only between sampled points.
        plot = Plot(box=(1.21, 5.88, -1.39, .96), xr=(0, 104), yr=(0, 70),
                    xlabel="Number of pulses", ylabel="Activity after pulses (%)",
                    size=28, label_size=28, color=TEXT)
        plot.ylabel.move_to(p(R + .06, 1.28))
        self.play(FadeOut(year), run_time=.28)
        self.play(Create(plot), run_time=.77)
        progress = ValueTracker(0)
        slow = lambda n: np.interp(n, [0, 10, 20, 40, 60, 80, 100], [0, 1, 3, 2, 4, 8, 7])
        fast = lambda n: np.interp(n, [0, 8, 16, 20, 32, 40, 80, 100], [0, 5, 10, 15, 27, 39, 55, 63])
        a = plot.live_curve(slow, progress, color=BLUE)
        b = plot.live_curve(fast, progress, color=GREEN)
        self.add(a, b, plot.dot(progress.get_value, lambda: fast(progress.get_value()), ring=GREEN, radius=.085))
        self.at("showed that lasting activity")
        self.play(progress.animate.set_value(100), run_time=2.1, rate_func=linear)
        self.play(FadeIn(label("Fast pulses", 3.82, .68, GREEN, 28)),
                  FadeIn(label("Slow pulses", 4.70, -.72, BLUE, 28)), run_time=.55)
        self.finish()


def pocket_enzyme():
    # Simplify the ATP pocket to the space between these two lobes.
    shell = VGroup(tile(L - .77, .12, 1.82, 2.38, "#75568E", PURPLE, radius=.58),
                   tile(L + .63, -.62, 1.81, .9, "#594474", PURPLE, radius=.35))
    return shell


class S11UnlockedImatinib(SpokenScene):
    def construct(self):
        chamber(self, True)
        self.add(cam_ring(), label("CaM kinase II", L, 1.83, PURPLE, 34))
        old = VGroup(*self.mobjects[-2:])
        enzyme = pocket_enzyme()
        self.at("around 1990")
        self.play(FadeOut(old), FadeIn(enzyme), run_time=1.05)
        blocker = tile(L + .86, 1.38, .78, .39, ORANGE).rotate(.18)
        self.at("a drug for")
        self.play(FadeIn(blocker, shift=DOWN * .33), run_time=.52)
        self.at("tp pocket")
        self.play(blocker.animate.move_to(p(L + .61, .09)), run_time=1.02)
        pocket = label("ATP pocket", L, -1.7, PURPLE, 34)
        self.play(FadeIn(pocket), run_time=.45)
        self.at("that pocket looks alike")
        comparison = VGroup(*(pocket_enzyme().scale(.47).move_to(p(x, -.06))
                              for x in [1.54, R, 4.94]))
        self.play(LaggedStart(*(FadeIn(k, shift=UP * .22) for k in comparison),
                              lag_ratio=.36), run_time=1.36)
        self.at("in basel")
        basel = label("Basel", R, 1.83, GOLD, 35)
        self.play(FadeIn(basel), run_time=.58)
        researcher = label("Juerg Zimmermann", R, 1.20, TEXT, 32)
        self.play(FadeIn(researcher), run_time=.5)
        self.at("added one methyl")
        self.play(FadeOut(comparison), blocker.animate.move_to(p(L + .86, .73)), run_time=.66)
        methyl = Dot(p(L + 1.25, .86), radius=.17, color=ORANGE, stroke_color=TEXT, stroke_width=2)
        tag = label("Methyl", -2.28, 1.73, ORANGE, 29)
        self.play(FadeIn(methyl, shift=LEFT * .17), run_time=.44)
        self.play(FadeIn(tag), run_time=.34)
        self.at("removing activity against")
        grid = Ledger([("Protein kinase C", "Active", GREEN), ("ABL", "Blocked", RED)],
                      top_left=(.69, .21), key_w=3.82, width=5.34, row_h=1.17, size=29)
        self.play(grid.reveal(0), run_time=.7)
        line1 = Line(p(.74, -.27), p(5.79, -.27), stroke_width=3, color=GREEN)
        self.play(Create(line1), run_time=1.24)
        self.at("it still blocked")
        self.play(grid.reveal(1), run_time=.68)
        line2 = Line(p(.74, -1.43), p(5.79, -1.43), stroke_width=3, color=RED)
        self.play(Create(line2), VGroup(blocker, methyl).animate.shift(LEFT * .25 + DOWN * .62),
                  FadeOut(tag), run_time=1.14)
        self.at("compound became imatinib")
        imatinib = label("Imatinib", R, 1.79, ORANGE, 36)
        self.play(swap(basel, imatinib), run_time=.8)
        self.at("one purified kinase")
        scope = caption("One purified kinase", size=34, color=GOLD, y=-3.13).shift(RIGHT * .9)
        self.play(FadeIn(scope), run_time=.68)
        self.finish()


class S12End(EndCard):
    LINE = "A purified kinase plus labelled ATP shows what it can phosphorylate directly."
