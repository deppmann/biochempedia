"""Reading Clues in Shared Sequences, timed to the locked Kokoro narration.

BLUE marks the main sequence or apparatus, TEAL the comparison, GREY the
scaffold, YELLOW a candidate or shared feature, GREEN confirmation, RED a
discarded inference, and GOLD dates and the guiding question.
"""
from bp_parts import *
from bp_style import EndCard


BOARD = "#273642"
TILE = "#385361"
QUESTION = "Closest relatives, or another cause?"
CARD = dict(y=-0.57, size=34)
HUMAN = "VLNAQFTGKD"
MOULD = "VLDAERSGRT"
MATCHES = tuple(i for i, (a, b) in enumerate(zip(HUMAN, MOULD)) if a == b)
TOP, SECOND, THIRD = 2.12, 0.68, -0.76


def pt(x, y):
    return np.array([x, y, 0.0])


def lab(text, x, y, color=TEXT, size=32):
    return T(text, size, color).move_to(pt(x, y))


def panel(w, h, x, y, fill, outline, opacity=1, stroke=2):
    return RoundedRectangle(
        width=w, height=h, corner_radius=0.14, stroke_color=outline,
        stroke_width=stroke, fill_color=fill, fill_opacity=opacity,
    ).move_to(pt(x, y))


def workbench():
    return panel(12.95, 6.75, 0, 0, BOARD, "#465866")


def schematic():
    return scope_tag("Schematic", size=28, color=TEXT).move_to(pt(5.25, -3.02))


def x_at(i):
    return -2.48 + 0.87 * i


def lane(y):
    return panel(8.91, 1.13, 1.435, y, BG, "#627784", stroke=0)


def tile(letter, i, y, color, highlighted=False):
    outline = YELLOW if highlighted else color
    box = panel(0.74, 0.87, x_at(i), y, "#635522" if highlighted else TILE, outline)
    return VGroup(box, M(letter, size=34 if len(letter) == 1 else 28, color=TEXT).move_to(box))


def track(seq, y, color, marks=()):
    return VGroup(*(tile(letter, i, y, color, i in marks) for i, letter in enumerate(seq)))


def track_label(text, y, color):
    return lab(text, -4.73, y, color, 30)


def lanes():
    return VGroup(lane(TOP), lane(SECOND))


def named_pair(top, bottom, marks=()):
    a, name_a = top
    b, name_b = bottom
    return (track(a, TOP, BLUE, marks), track(b, SECOND, TEAL, marks),
            track_label(name_a, TOP, BLUE), track_label(name_b, SECOND, TEAL))


def lis_pair(marks=MATCHES):
    return named_pair((HUMAN, "Human LIS1"), (MOULD, "Mould nudF"), marks)


def highlight(scene, rows, marks, run_time):
    blocks = [row[i] for row in rows for i in marks]
    scene.play(LaggedStart(
        *(recolor(block, "#635522", YELLOW) for block in blocks),
        lag_ratio=0.14,
    ), run_time=run_time)


def recolor(block, fill, outline):
    target = block.copy()
    target[0].set_fill(fill, opacity=1).set_stroke(outline, width=3)
    return Transform(block, target)


def scan(scene, rows, run_time):
    """Pass the inspection light along the strips without moving their landmarks."""
    light = ManimColor("#698791")

    def sweep(row):
        colors = tuple(block[0].get_fill_color() for block in row)

        def update(mob, alpha):
            center = -3 + (len(colors) + 5) * alpha
            for i, (block, base) in enumerate(zip(mob, colors)):
                strength = max(0, 1 - abs(i - center) / 3) ** 0.6
                block[0].set_fill(interpolate_color(base, light, strength * 0.72))

        return UpdateFromAlphaFunc(row, update, rate_func=linear)

    scene.play(*(sweep(row) for row in rows), run_time=run_time)


def trace(a, b, color=GREY, width=5, dashed=False):
    return (DashedLine if dashed else Line)(pt(*a), pt(*b), color=color, stroke_width=width)


def match_bracket():
    return VGroup(
        trace((-2.97, 2.43), (-3.26, 2.43), GOLD),
        trace((-3.26, 2.43), (-3.26, 0.41), GOLD),
        trace((-3.26, 0.41), (-2.97, 0.41), GOLD),
    )


def homology_note():
    plate = panel(8.4, 1.43, 0, -1.28, "#594925", GOLD, stroke=1.5)
    return VGroup(plate, lab("Homology", 0, -0.99, YELLOW, 40),
                  lab("Shared ancestor", 0, -1.60, TEXT))


def meter():
    left, width = -4.77, 9.54
    box = panel(width + 0.24, 0.93, 0, -1.71, BG, GREY)
    value = ValueTracker(0)
    fill = always_redraw(lambda: Rectangle(
        width=max(0.001, width * value.get_value()), height=0.67,
        stroke_width=0, fill_color=YELLOW, fill_opacity=1,
    ).move_to(pt(left + width * value.get_value() / 2, -1.71)))
    return box, fill, value


class S01Hook(SpokenScene):
    def construct(self):
        row = track(HUMAN, TOP - 0.28, BLUE)
        tray = lane(TOP - 0.28)
        query = lab("?", -4.73, 0.21, YELLOW, 128)
        self.add(workbench(), tray, lane(SECOND), schematic(), *row[:2])
        self.at("a string of letters")
        self.play(LaggedStart(*(FadeIn(block, shift=LEFT * 0.26) for block in row[2:]),
                              lag_ratio=0.22), run_time=1.95)
        self.at("unknown protein does")
        self.play(FadeIn(query, shift=UP * 0.12), run_time=0.62)
        bob(query, amp=0.18, speed=2.7)
        scan(self, (row,), 2.35)
        self.at("children with smooth brains")
        self.play(VGroup(tray, row).animate.shift(UP * 0.28), run_time=1.32)
        self.play(FadeIn(track_label("Human LIS1", TOP, BLUE)), run_time=0.75)
        scan(self, (row,), 3.15)
        self.at("its sequence alone")
        self.play(query.animate.set_color(TEXT), run_time=0.65)
        scan(self, (row,), 2.8)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Sequence alignment and homology search"
    TITLE = "Reading Clues in Shared Sequences"

    def construct(self):
        bench = workbench()
        dimmed = VGroup(lanes(), track(HUMAN, TOP, BLUE), track_label("Human LIS1", TOP, BLUE))
        dimmed.fade(0.82)
        title = T(self.TITLE, 54, font=TITLE_FONT).move_to(pt(0, -1.05))
        lesson = lab(self.LESSON, 0, -2.24, TEXT, 29)
        self.add(bench, dimmed)
        self.play(FadeIn(lesson), FadeIn(title, shift=UP * 0.12), run_time=0.38)
        self.wait(1.25)
        self.play(FadeOut(title), FadeOut(lesson), run_time=0.37)


class S03Align(SpokenScene):
    def construct(self):
        upper, lower, name_a, name_b = lis_pair(())
        self.add(workbench(), lanes(), schematic(), upper, name_a)
        self.at("slides two letter strips")
        lower.shift(LEFT * 0.78)
        self.play(FadeIn(lower, shift=RIGHT * 0.38), run_time=0.90)
        self.play(lower.animate.shift(RIGHT * 0.78), run_time=1.7)
        self.at("matching positions")
        highlight(self, (upper, lower), MATCHES, 1.5)
        self.at("clue came from")
        self.play(FadeIn(name_b), run_time=0.65)
        scan(self, (upper, lower), 2.55)
        self.at("1995")
        year = lab("1995", -4.82, -0.72, GOLD)
        self.play(FadeIn(year), run_time=0.7)
        self.at("its protein matched")
        box, fill, value = meter()
        self.play(FadeIn(box), run_time=0.65)
        self.add(fill)
        scan(self, (upper, lower), 1.1)
        match = lab("42% match", 0, -0.75, YELLOW, 38)
        self.play(value.animate.set_value(0.42), FadeIn(match), run_time=0.8)
        self.at("chance rarely matches")
        self.play(FadeOut(year), run_time=0.42)
        scan(self, (upper, lower), 3.45)
        self.at("pointed to homology")
        self.play(FadeOut(box), FadeOut(match), FadeOut(fill), Create(match_bracket()), run_time=0.63)
        note = homology_note()
        self.play(FadeIn(note[0]), FadeIn(note[1]), run_time=0.55)
        self.at("one shared ancestor")
        self.play(FadeIn(note[2]), run_time=0.65)
        self.finish()


def filament():
    cell = panel(10.7, 1.44, 0, -1.35, "#356064", TEAL, stroke=3)
    nuclei = VGroup(*(Dot(pt(x, -1.35 + dy), radius=0.27, color=BLUE)
                      for x, dy in zip((-3.9, -1.45, 1.25, 3.9), (0.27, -0.33, 0.27, -0.33))))
    return cell, nuclei


def rail():
    return VGroup(*(trace((-5.15, y), (5.15, y), GREY, 7) for y in (-2.41, -2.64)))


class S04Clue(SpokenScene):
    def construct(self):
        pair = lis_pair()
        carry = VGroup(match_bracket(), homology_note())
        self.add(workbench(), lanes(), schematic(), *pair, carry)
        self.at("a match lets")
        self.play(FadeOut(carry), run_time=0.57)
        self.at("knowledge from one organism")
        arrow = trace((6.02, 0.83), (6.02, 1.94), YELLOW, dashed=True).add_tip(tip_length=0.2)
        self.play(Create(arrow), run_time=1.15)
        scan(self, pair[:2], 3.64)
        self.at("nuclear distribution")
        cell, nuclei = filament()
        self.play(FadeIn(cell), run_time=0.6)
        self.play(FadeIn(nuclei), run_time=0.62)
        self.at("leave their nuclei bunched")
        self.play(*(n.animate.move_to(pt(-4.65 + 0.56 * i, -1.35 + 0.18 * (-1)**i))
                    for i, n in enumerate(nuclei)), run_time=1.22)
        mutant = lab("nud mutant", 1.62, -1.35, TEXT)
        self.play(FadeIn(mutant), run_time=0.55)
        self.at("other nud genes")
        tracks = rail()
        self.play(FadeOut(cell), FadeOut(nuclei), FadeOut(mutant), Create(tracks), run_time=1.05)
        motor = panel(1.21, 0.75, -4.4, -1.99, "#9a7b2d", YELLOW, stroke=3)
        nucleus = Dot(pt(-4.4, -1.24), radius=0.40, color=BLUE)
        self.play(FadeIn(motor), FadeIn(nucleus), run_time=0.75)
        self.at("a motor that moves")
        dynein = lab("Dynein", -4.4, -0.48, YELLOW)
        self.play(FadeIn(dynein), run_time=0.5)
        self.play(VGroup(motor, nucleus, dynein).animate.shift(RIGHT * 7.2), run_time=2.43)
        self.at("called microtubules")
        self.play(FadeIn(lab("Microtubules", 0, -3.02)), run_time=0.7)
        scan(self, pair[:2], 2.14)
        self.at("cell experiments")
        self.play(FadeOut(arrow), run_time=0.35)
        solid = Arrow(pt(6.02, 0.83), pt(6.02, 1.94), buff=0, stroke_width=5, color=GREEN)
        self.play(GrowArrow(solid), run_time=0.75)
        scan(self, pair[:2], 1.46)
        self.at("binds dining")
        self.play(FadeIn(lab("✓", 6.05, 2.95, GREEN, 42)), run_time=0.62)
        self.finish()


BRANCHES = (
    ((-5.2, -1.98), (-3.25, -1.98)),   # root
    ((-3.25, -1.98), (-3.25, -2.68)),
    ((-3.25, -2.68), (3.25, -2.68)),   # distant tip
    ((-3.25, -1.98), (-0.3, -1.98)),   # shared inner branch
    ((-0.3, -1.98), (-0.3, -1.48)),
    ((-0.3, -1.48), (3.25, -1.48)),    # sister tip 1
    ((-0.3, -1.98), (-0.3, -2.14)),
    ((-0.3, -2.14), (3.25, -2.14)),    # sister tip 2
)
TIP_Y = (-1.48, -2.14, -2.68)
PREDICT_TOP = "VTNALFTGKD"
PREDICT_BOTTOM = "GSQPLINAVR"
SHARED = (4,)


def species_pair(marks=SHARED):
    return named_pair((PREDICT_TOP, "Species one"), (PREDICT_BOTTOM, "Species two"), marks)


def tree():
    branches = VGroup(*(trace(a, b, GREY, 6) for a, b in BRANCHES))
    ends = VGroup(*(Dot(pt(3.25, y), radius=0.11, color=GREY) for y in TIP_Y))
    return VGroup(branches, ends)


def prediction():
    return VGroup(workbench(), lanes(), schematic(), *species_pair(), tree(),
                  lab("?", 4.74, -1.98, YELLOW, 69))


def predict_card():
    card = question_card(QUESTION, color=YELLOW, **CARD)
    plate = panel(card.width + 0.72, 0.69, -0.5, CARD["y"], "#66552a", GOLD, stroke=1.5)
    return VGroup(plate, card)


class S05PredictQ(SpokenScene):
    def construct(self):
        upper, lower, a, b = species_pair(())
        previous = lis_pair()
        self.add(workbench(), lanes(), schematic(), *previous)
        self.at("suppose two species")
        self.play(FadeOut(previous[2]), FadeOut(previous[3]),
                  Transform(previous[0], upper), Transform(previous[1], lower), run_time=0.9)
        self.remove(*previous)
        self.add(upper, lower)
        self.play(FadeIn(a), FadeIn(b), run_time=0.55)
        self.at("share the exact same")
        highlight(self, (upper, lower), SHARED, 0.85)
        scan(self, (upper, lower), 2.05)
        self.at("does that guarantee")
        self.play(Create(tree()), run_time=0.98)
        query = lab("?", 4.74, -1.98, YELLOW, 69)
        self.play(FadeIn(query), run_time=0.44)
        self.at("closest relatives")
        self.play(FadeIn(predict_card()), run_time=0.68)
        scan(self, (upper, lower), 3.68)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = CARD
    SECONDS = 4.5

    def construct(self):
        self.add(prediction(), predict_card())
        self.wait(self.SECONDS)


def tree_paths(indices, color=YELLOW):
    return VGroup(*(trace(*BRANCHES[i], color, 15) for i in indices))


def shared_derived():
    event = (-2.62, -1.98)
    paths = VGroup(trace(event, BRANCHES[3][1], YELLOW, 15), *tree_paths((4, 5, 6, 7)))
    return paths, Dot(pt(*event), radius=0.17, color=YELLOW)


class S07PredictA(SpokenScene):
    def construct(self):
        picture = prediction()
        q = predict_card()
        self.add(picture, q)
        self.at("a match alone")
        self.play(FadeOut(q), FadeOut(picture[-1]), run_time=0.33)
        scan(self, (picture[3], picture[4]), 3.9)
        self.at("two lineages can gain")
        independent = VGroup(
            trace((0.65, -1.48), (3.25, -1.48), YELLOW, 15),
            trace((0.65, -2.68), (3.25, -2.68), YELLOW, 15),
        )
        bursts = VGroup(*(Dot(p.get_start(), radius=0.17, color=YELLOW) for p in independent))
        self.play(LaggedStart(*(GrowFromCenter(dot) for dot in bursts), lag_ratio=0.6), run_time=1.05)
        self.play(LaggedStart(*(Create(path) for path in independent), lag_ratio=0.35), run_time=1.5)
        self.at("called convergence")
        convergence = lab("Convergence", 0, -0.57, YELLOW, 36)
        self.play(FadeIn(convergence), run_time=0.62)
        scan(self, (picture[3], picture[4]), 1.75)
        self.at("both can keep")
        self.play(FadeOut(independent), FadeOut(bursts), FadeOut(convergence), run_time=0.45)
        inherited = tree_paths(range(8))
        self.play(Create(inherited[0]), run_time=0.65)
        ancestral = lab("Ancestral state", 0, -0.57, YELLOW, 36)
        self.play(FadeIn(ancestral), run_time=0.58)
        self.at("present before they split")
        self.play(LaggedStart(*(Create(inherited[i]) for i in (1, 3, 2, 4, 6, 5, 7)),
                              lag_ratio=0.32), run_time=1.99)
        self.at("only a shared derived change")
        self.play(FadeOut(inherited), FadeOut(ancestral), run_time=0.52)
        shared, gain = shared_derived()
        self.play(GrowFromCenter(gain), run_time=0.7)
        self.at("gained once")
        self.play(Create(shared[0]), FadeIn(lab("Shared derived", 0, -0.57, YELLOW, 36)), run_time=1.22)
        self.at("one shared branch")
        self.play(LaggedStart(*(Create(path) for path in shared[1:]), lag_ratio=0.30), run_time=2.35)
        self.finish()


def large_tree_point(x, y):
    return x, (y + 1.98) * 2.5 + 0.55


def large_tree(branches, color=GREY, dashed=False):
    return VGroup(*(trace(large_tree_point(*a), large_tree_point(*b), color, 6, dashed)
                    for a, b in branches))


class S08Limits(SpokenScene):
    def construct(self):
        small = tree()
        sequence = VGroup(lanes(), *species_pair())
        prior = VGroup(*shared_derived(),
                       lab("Shared derived", 0, -0.57, YELLOW, 36))
        self.add(workbench(), schematic(), sequence, small, prior)
        self.at("an outside relative")
        self.play(FadeOut(sequence), FadeOut(prior), FadeOut(small[1]), run_time=0.45)
        self.play(Transform(small[0], large_tree(BRANCHES)), run_time=0.75)
        stem = VGroup(trace((-5.75, 0.55), (-5.75, -2.3), TEAL),
                      trace((-5.75, 0.55), (-5.2, 0.55), TEAL))
        first = trace((-5.75, -2.3), (3.25, -2.3), TEAL, 17)
        self.play(Create(stem), Create(first), run_time=1.28)
        out = lab("Outgroup", 4.74, -2.3, TEAL)
        self.play(FadeIn(out), run_time=0.42)
        self.at("suggests which state")
        state = Dot(pt(3.25, -2.3), radius=0.43, color=TEAL)
        self.play(GrowFromCenter(state), run_time=0.65)
        self.at("its own lineage can change")
        change = Dot(pt(-2.35, -2.3), radius=0.24, color=YELLOW)
        self.play(GrowFromCenter(change), run_time=0.75)
        switched = trace((-2.35, -2.3), (3.25, -2.3), YELLOW, 21)
        self.play(Create(switched), state.animate.set_color(YELLOW), run_time=1.04)
        self.at("studies compare several")
        more = VGroup(trace((-5.75, 0.02), (-3.8, 0.02), TEAL, 6),
                      trace((-3.8, 0.02), (-3.8, -1.69), TEAL, 6),
                      trace((-3.8, -1.69), (3.25, -1.69), TEAL, 9),
                      trace((-5.75, -2.3), (-5.75, -2.88), TEAL, 6),
                      trace((-5.75, -2.88), (3.25, -2.88), TEAL, 9))
        # Keep the additional outgroup paths below the gene-tree tips.
        several = lab("Several outgroups", 0, 2.85, TEAL, 35)
        self.play(Create(more, run_time=1.35), swap(out, several, run_time=0.6))
        self.at("one genes tree")
        overlay_geometry = (
            BRANCHES[0], ((-3.25, -1.98), (-3.25, -1.48)), ((-3.25, -1.48), (3.25, -1.48)),
            ((-3.25, -1.98), (0.85, -1.98)), ((0.85, -1.98), (0.85, -2.68)),
            ((0.85, -2.68), (3.25, -2.68)), ((0.85, -1.98), (0.85, -2.14)),
            ((0.85, -2.14), (3.25, -2.14)),
        )
        overlay = large_tree(overlay_geometry, BLUE, dashed=True).shift(DOWN * 0.20)
        self.play(FadeOut(VGroup(stem, first, more, change, several, state, switched)), run_time=0.5)
        self.play(Create(overlay), run_time=1.6)
        relation = lab("Gene tree vs species tree", 0, 2.85, TEXT, 35)
        self.play(FadeIn(relation), run_time=0.6)
        self.at("tools like scansite")
        row = track("VLNASETGKD", SECOND, BLUE)
        self.play(FadeOut(VGroup(small, overlay, relation)), run_time=0.36)
        self.play(FadeIn(lane(SECOND)), FadeIn(row, shift=LEFT * 0.45), run_time=0.49)
        scansite = track_label("Scansite", SECOND, BLUE)
        query = lab("?", x_at(4), 2.02, YELLOW, 58)
        self.play(FadeIn(scansite), FadeIn(query), run_time=0.47)
        self.at("where a phosphate group")
        highlight(self, (row,), (4,), 0.72)
        self.at("predicted site stays a guess")
        bob(query, amp=0.19, speed=3.5)
        scan(self, (row,), 2.1)
        self.at("experiments find the phosphate")
        query.clear_updaters()
        phosphate = boxed_label("Phosphate", GREEN, size=30).move_to(pt(x_at(4), 1.82))
        self.play(FadeOut(query), run_time=0.32)
        self.play(FadeIn(phosphate), run_time=0.73)
        self.play(recolor(row[4], "#3f5b33", GREEN), run_time=0.55)
        self.finish()


HYDROPHOBIC_BLOCKS = ("VL", "IF", "WA", "LI", "WV", "FL", "IA")
RECEPTOR_A = HYDROPHOBIC_BLOCKS + ("I", "G", "T")
RECEPTOR_B = HYDROPHOBIC_BLOCKS + ("S", "G", "D")
SPAN_COLS = tuple(range(7))


def membrane():
    return VGroup(panel(6.75, 0.27, -0.05, -1.07, "#52616b", GREY),
                  panel(6.75, 0.27, -0.05, -2.23, "#52616b", GREY))


def spans():
    return VGroup(*(panel(0.49, 1.77, x_at(i), -1.65, "#715d25", YELLOW, stroke=3)
                    for i in SPAN_COLS))


def membrane_turns():
    return VGroup(*(ArcBetweenPoints(pt(x_at(i), y), pt(x_at(i + 1), y), angle=angle)
                    .set_stroke(YELLOW, 6)
                    for i in range(len(SPAN_COLS) - 1)
                    for y, angle in [(-0.78, -1.15) if i % 2 == 0 else (-2.52, 1.15)]))


class S09UnlockedOne(SpokenScene):
    def construct(self):
        upper, lower, name_a, name_b = named_pair(
            (RECEPTOR_A, "Beta-adrenergic"), (RECEPTOR_B, "Rhodopsin"))
        self.add(workbench(), lanes(), schematic())
        self.at("1986")
        date = lab("1986", -4.7, -1.62, GOLD, 40)
        self.play(LaggedStart(*(FadeIn(block, shift=LEFT * 0.34) for block in upper),
                              lag_ratio=0.22), FadeIn(date), run_time=4.65)
        self.at("cloned a beta")
        self.play(FadeIn(name_a), run_time=0.85)
        scan(self, (upper,), 1.68)
        self.at("which senses adrenaline")
        adrenaline = lab("Adrenaline", 1.52, 3.02, BLUE, 30)
        self.play(FadeIn(adrenaline), run_time=0.7)
        self.at("its sequence resembled")
        lower.shift(LEFT * 0.72)
        self.play(FadeOut(adrenaline), FadeIn(lower, shift=RIGHT * 0.28), run_time=0.86)
        self.play(lower.animate.shift(RIGHT * 0.72), FadeIn(name_b), run_time=1.35)
        self.at("light catching pigment")
        self.play(FadeIn(membrane()), run_time=0.8)
        self.at("seven water avoiding")
        highlight(self, (upper, lower), SPAN_COLS, 1.25)
        self.play(LaggedStart(*(GrowFromCenter(block) for block in spans()), lag_ratio=0.25),
                  run_time=2.1)
        self.play(Create(membrane_turns()), run_time=1.78)
        self.at("then known used light")
        guess = lab("Light-sensitive only?", 0, -2.98, YELLOW, 34)
        self.play(FadeIn(guess), run_time=0.75)
        scan(self, (upper, lower), 3.80)
        self.at("instead")
        strike = Line(guess.get_left(), guess.get_right(), color=RED, stroke_width=5)
        strike.layout_ok = "covered"  # Deliberate strike-through of the rejected inference.
        self.play(Create(strike), run_time=0.7)
        self.play(FadeOut(VGroup(strike, guess)), FadeOut(date), run_time=0.55)
        self.at("receptors signaling through")
        gpcr = lab("G-protein receptors (1986)", 0, -2.98, GREEN, 33)
        self.play(FadeIn(gpcr), run_time=0.85)
        scan(self, (upper, lower), 1.96)
        self.at("relay proteins inside cells")
        relay = boxed_label("G protein", GREEN, size=28).move_to(pt(5.05, -1.65))
        direction = Arrow(pt(3.30, -1.65), pt(relay.get_left()[0] - 0.12, -1.65),
                          buff=0, color=GREEN, stroke_width=4, tip_length=0.15)
        self.play(FadeIn(relay), GrowArrow(direction), run_time=1.15)
        self.finish()


TAILS = ("QDTYELVRPK", "REKYDIVSAM", "PGNYALINTS")


def immune_tracks(marks=()):
    return [track(seq, y, color, marks)
            for seq, y, color in zip(TAILS, (TOP, SECOND, THIRD), (BLUE, TEAL, BLUE))]


class S10UnlockedTwo(SpokenScene):
    def construct(self):
        row_a, row_b, row_c = immune_tracks()
        bottom = lane(THIRD)
        self.add(workbench(), lanes(), bottom, schematic())
        self.at("1989")
        date = lab("Reth, 1989", 0, -2.13, GOLD, 35)
        self.play(FadeIn(date, shift=UP * 0.2), run_time=1.0)
        self.at("published a letter")
        row_a.shift(LEFT * 0.55)
        self.play(FadeIn(row_a, shift=RIGHT * 0.26), run_time=0.8)
        self.at("with no experiment")
        no_experiment = lab("No new experiment", 0, -2.93, TEXT)
        self.play(FadeIn(no_experiment), run_time=0.9)
        self.at("lined up published tail sequences")
        row_b.shift(LEFT * 0.28)
        self.play(LaggedStart(*(FadeIn(row, shift=RIGHT * 0.36)
                                for row in (row_b, row_c)), lag_ratio=0.56), run_time=1.95)
        self.play(row_a.animate.shift(RIGHT * 0.55), row_b.animate.shift(RIGHT * 0.28), run_time=1.35)
        scan(self, (row_a, row_b, row_c), 2.42)
        self.at("chains from t cells")
        self.play(FadeIn(track_label("T cell", TOP, BLUE)), run_time=0.60)
        self.at("the b cell receptor")
        self.play(FadeIn(track_label("B-cell receptor", SECOND, TEAL)), run_time=0.60)
        self.at("cell receptor all shared")
        self.play(FadeIn(track_label("Mast-cell\nreceptor", THIRD, BLUE)), run_time=0.62)
        self.at("shared one pattern")
        highlight(self, (row_a, row_b, row_c), (3,), 1.2)
        self.finish()


def genome_plot():
    return Plot(box=(-3.5, 4.15, -2.06, 1.78), xr=(0, 3), yr=(0, 3),
                yticks=[(0, "0"), (2, "2×"), (3, "3×")], size=28, stroke=4)


def genome_bar(plot, x, color, ratio):
    base, top = plot.pt(x, 0), plot.pt(x, ratio)
    return Rectangle(
        width=1.82, height=max(0.001, top[1] - base[1]),
        stroke_width=0, fill_color=color, fill_opacity=0.85,
    ).move_to((base + top) / 2)


def genome_baseline(plot):
    rule = DashedLine(plot.pt(0, 1), plot.pt(3, 1), color=TEXT, stroke_width=7, dash_length=0.14)
    note = lab("1×\nInvertebrates", -4.91, plot.pt(0, 1)[1], TEXT, 28)
    return VGroup(rule, note).set_z_index(2)


class S10bUnlockedThree(SpokenScene):
    def construct(self):
        old = VGroup(lanes(), lane(THIRD), *immune_tracks((3,)),
                     track_label("T cell", TOP, BLUE),
                     track_label("B-cell receptor", SECOND, TEAL),
                     track_label("Mast-cell\nreceptor", THIRD, BLUE),
                     lab("Reth, 1989", 0, -2.13, GOLD, 35),
                     lab("No new experiment", 0, -2.93, TEXT), schematic())
        self.add(workbench(), old)
        self.at("2007")
        date = lab("2007", -5.15, 2.78, GOLD, 36)
        head = lab("Human vs four invertebrates", 0.32, 2.83, TEXT, 38)
        plot = genome_plot()
        self.play(FadeOut(old, shift=DOWN * 0.18), FadeIn(date), run_time=0.83)
        self.play(Create(plot.axes.set_z_index(1)), run_time=2.34)
        self.at("compared the human genome")
        chart_plate = panel(7.80, 4.08, 0.40, -0.12, BG, BG, stroke=0)
        self.play(FadeIn(chart_plate, run_time=3.5), FadeIn(head, run_time=1.05),
                  Create(plot.ticks.set_z_index(1), run_time=1.05),
                  FadeIn(plot.tick_labels.set_z_index(1), run_time=1.05))
        self.at("genomes differ in total")
        adjustment = lab("Adjusted for gene number", 0.32, 2.23, TEXT, 29)
        self.play(FadeIn(adjustment), run_time=0.75)
        self.at("total gene number")
        base = genome_baseline(plot)
        self.play(Create(base[0]), FadeIn(base[1]), run_time=2.25)
        a, b = 0.85, 2.15
        tag_a = lab("EGF receptors", plot.pt(a, 0)[0], -2.64, BLUE, 30)
        tag_b = lab("All protein kinases", plot.pt(b, 0)[0], -2.64, TEAL, 30)
        self.at("per gene")
        self.play(FadeIn(tag_a), run_time=0.36)
        bar_a = genome_bar(plot, a, BLUE, 2.5)
        ratio_a = lab("2.5×", plot.pt(a, 0)[0], plot.pt(a, 2.5)[1] + 0.32, BLUE, 37)
        self.play(GrowFromEdge(bar_a, DOWN, run_time=1.1),
                  Succession(Wait(0.75), FadeIn(ratio_a, run_time=0.35)))
        self.at("egf receptors")
        emphasis = interpolate_color(bar_a.get_fill_color(), WHITE, 0.45)
        self.play(bar_a.animate(rate_func=there_and_back).set_fill(emphasis), run_time=1.45)
        self.at("total protein kinases")
        self.play(FadeIn(tag_b), run_time=0.78)
        self.at("were only about")
        bar_b = genome_bar(plot, b, TEAL, 1.2)
        self.play(GrowFromEdge(bar_b, DOWN), run_time=1.63)
        self.at("1 2 times")
        self.play(FadeIn(lab("1.2×", plot.pt(b, 0)[0], plot.pt(b, 1.2)[1] + 0.36, TEAL, 37)),
                  run_time=0.66)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        upper, lower, a, b = lis_pair(())
        pair_a = VGroup(lane(TOP), upper, a)
        pair_b = VGroup(lane(SECOND), lower, b)
        self.add(workbench(), schematic(), pair_a, pair_b)
        self.at("unknown protein to whole genomes")
        scan(self, (upper, lower), 2.72)
        self.at("shared sequences point")
        highlight(self, (upper, lower), MATCHES, 1.65)
        self.at("candidate functions")
        self.play(FadeIn(lab("Candidate function", 0, -0.63, YELLOW, 38)), run_time=0.8)
        self.at("experiments then confirm")
        check = lab("✓", 0, -1.94, GREEN, 84)
        self.play(pair_a.animate.shift(DOWN * 0.14), pair_b.animate.shift(UP * 0.14),
                  GrowFromCenter(check), run_time=0.88)
        bob(check, amp=0.11, speed=2.9)
        self.finish()


class S12End(EndCard):
    LINE = "Shared sequences point to relatives and candidate functions;\nexperiments confirm them."
