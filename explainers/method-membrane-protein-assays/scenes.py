"""Word-synced teaching film about membrane protein extraction and topology."""

from bp_parts import *
from bp_style import EndCard

# Patch-clamp palette: GREY membrane, PURPLE protein, TEAL lumen, ORANGE added
# reagents, GREEN control evidence, RED caution. GOLD and BLUE distinguish tags.
PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
LUMEN = "#194A55"
LUMEN_LIT = "#2B6572"
BILAYER = "#424A5C"
GEL = "#252E41"
CENTER = np.array([-2.15, -0.32, 0.0])
RX, RY = 3.72, 2.48
PROTEIN_AT = CENTER + UP * (RY - 0.24)
OUT_TAG = PROTEIN_AT + UP * 0.83
IN_TAG = PROTEIN_AT + DOWN * 0.93
QUESTION = "Does surviving protease prove a tag is lumenal?\nWhat control rules out another cause?"
QUESTION_STYLE = dict(y=3.26, max_w=12.1, size=33, color=TEXT)
# The spoken scene's last frame, which the silent scene holds.
PREDICT_END_PHASE = 16.73


def point(x, y):
    return np.array([x, y, 0.0])


def label(words, x, y, color=TEXT, size=32):
    return T(words, size, color).move_to(point(x, y))


def block(width, height, color, at, radius=0.17, opacity=1.0):
    return RoundedRectangle(
        width=width, height=height, corner_radius=radius,
        stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=opacity,
    ).move_to(at)


def rim_point(theta, inset=0):
    return CENTER + point((RX - inset) * np.cos(theta), (RY - inset) * np.sin(theta))


def leaflet(start, extent, inset):
    return (Arc(start_angle=start, angle=extent, radius=1, stroke_color=GREY, stroke_width=3.2)
            .stretch(RX - inset, 0, about_point=ORIGIN)
            .stretch(RY - inset, 1, about_point=ORIGIN)
            .shift(CENTER))


def membrane(opened=False, drifting=True, phase=0.0):
    """Build the same section for every assay. The open section has a gap at right."""
    start = 0.50 if opened else 0
    extent = TAU - 2 * start
    if opened:
        outer = [rim_point(t) for t in np.linspace(start, TAU - start, 100)]
        inner = [rim_point(t, 0.47) for t in np.linspace(TAU - start, start, 100)]
        body = Polygon(*outer, *inner, stroke_width=0, fill_color=BILAYER, fill_opacity=1)
    else:
        body = Ellipse(width=2 * RX, height=2 * RY, stroke_width=0,
                       fill_color=BILAYER, fill_opacity=1).move_to(CENTER)
    lumen = Ellipse(width=2 * (RX - 0.47), height=2 * (RY - 0.47), stroke_width=0,
                    fill_color=LUMEN, fill_opacity=1).move_to(CENTER)
    rims = VGroup(leaflet(start, extent, 0), leaflet(start, extent, 0.47))
    wall = VGroup(body, *([] if opened else [lumen]), rims)
    if opened:
        for end in (start, -start):
            wall.add(Line(rim_point(end), rim_point(end, 0.47), color=GREY, stroke_width=3))
    # Leaflet marks drift sideways, and the fluid compartment catches light as it moves.
    marks = VGroup(*[Dot(radius=0.065, color=GREY) for _ in range(29)])
    clock = phase
    dark, light = ManimColor(LUMEN), ManimColor(LUMEN_LIT)

    def drift(group, dt):
        nonlocal clock
        clock += dt
        for i, mark in enumerate(group):
            theta = start + extent * ((i / len(group) + 0.041 * clock) % 1)
            mark.move_to(rim_point(theta, 0.23))
            mark.set_opacity(0.52 + 0.38 * np.sin(3 * theta - 2.4 * clock) ** 2)
        if not opened:
            glow = 0.5 - 0.5 * np.cos(1.8 * clock)
            lumen.set_fill(interpolate_color(dark, light, glow))

    drift(marks, 0)
    if drifting:
        marks.add_updater(drift)
    wall.add(marks)
    return wall


def spanning():
    return block(0.58, 1.54, PURPLE, PROTEIN_AT, radius=0.22)


def peripheral():
    shoulder = rim_point(0.63) + point(0.27, 0.16)
    return block(0.91, 0.54, PURPLE, shoulder, radius=0.24).rotate(-0.40)


def tag_mark(at, color):
    return block(0.45, 0.28, color, at, radius=0.09)


def gel_band(x, y, color):
    return block(0.98, 0.18, color, point(x, y), radius=0.06)


def protection_gel():
    x = 3.85
    box = block(1.64, 2.63, GEL, point(x, -0.30), opacity=0.90).set_stroke(GREY, 2)
    heading = label("Gel", 4.65, 1.91)
    condition = label("Sealed", x, -1.92, TEAL)
    return VGroup(box, heading, condition), gel_band(x, 0.33, GOLD), gel_band(x, -0.83, BLUE)


def protection_result(drifting=True, phase=0.0):
    wall = membrane(drifting=drifting, phase=phase)
    protein, kept = spanning(), tag_mark(IN_TAG, BLUE)
    gel, _, band = protection_gel()
    return VGroup(wall, protein, kept, gel, band, schematic()), kept, band


def schematic():
    return scope_tag("Schematic", size=28, color=TEXT)


def wash():
    """Moving reagent marks in the outer buffer, following open paths around the section."""
    marks = VGroup(*[Dot(radius=0.09 if i % 3 == 0 else 0.055, color=ORANGE)
                     for i in range(23)])
    clock = 0.0

    def stream(group, dt):
        nonlocal clock
        clock += dt
        for i, mark in enumerate(group):
            p = (i / len(group) + 0.12 * clock) % 1
            x = -6.45 + 8.35 * p
            edge = np.sqrt(max(0, 1 - ((x - CENTER[0]) / (RX + 0.22)) ** 2))
            sign = 1 if i % 2 == 0 else -1
            y = CENTER[1] + sign * (0.47 + (RY + 0.24) * edge + 0.12 * (i % 3))
            mark.move_to(point(x, y))
            mark.set_fill(opacity=0.72 * min(1, p * 20, (1 - p) * 20))
            mark.set_stroke(width=0)

    stream(marks, 0)
    return marks.add_updater(stream)


def scissors(at):
    parts = VGroup()
    for sign in (-1, 1):
        loop = Circle(radius=0.104, color=ORANGE, stroke_width=4)
        loop.move_to(point(0.19, 0.155 * sign))
        blade = Line(point(0.10, 0.12 * sign), point(-0.43, -0.21 * sign),
                     color=ORANGE, stroke_width=5)
        parts.add(loop, blade)
    return parts.shift(at)


def detergent_ring(at, radius=0.24):
    return Circle(radius=radius, color=ORANGE, stroke_width=5).move_to(at)


def detergent_cloud():
    angles = np.linspace(0, TAU, 11, endpoint=False)
    # Leave a gap at the spanning protein on the upper rim.
    angles = np.delete(angles, np.argmin(abs(angles - PI / 2)))
    return VGroup(*[detergent_ring(rim_point(theta) + point(0.32 * np.cos(theta), 0.32 * np.sin(theta)))
                    for theta in angles])


def sugar_mark(at):
    """A tree-shaped glyph for a sugar tag, with no atomic or bond geometry."""
    trunk = Line(point(0, -0.05), point(0, 0.23), color=YELLOW, stroke_width=7)
    fork = VGroup(*[Line(point(0, 0.19), point(sign * 0.23, 0.41),
                         color=YELLOW, stroke_width=7) for sign in (-1, 1)])
    ends = VGroup(*[Dot(point(sign * 0.23, 0.41), radius=0.09, color=YELLOW) for sign in (-1, 1)])
    return VGroup(trunk, fork, ends).shift(at)


def lumen_and_cytosol():
    return (label("Lumen", -2.15, -0.86, TEXT),
            label("Cytosol", 4.15, 0.35, TEXT))


class S01Hook(SpokenScene):
    def construct(self):
        wall, outer, through = membrane(), peripheral(), spanning()
        outside, inside = (label("?", -1.50, 2.74, GOLD, 51),
                           label("?", -1.50, 0.91, GOLD, 51))
        self.add(wall, schematic())
        self.at("how deeply")
        self.play(FadeIn(outer, shift=LEFT * 0.34), FadeIn(through, shift=DOWN * 0.23), run_time=1.25)
        self.at("which way does")
        self.play(FadeIn(outside), FadeIn(inside), run_time=0.65)
        bob(outside, amp=0.13, speed=3)
        bob(inside, amp=0.13, speed=3, seed=2)
        self.at("some proteins cling")
        self.play(Indicate(outer, color=PURPLE, scale_factor=1.13), run_time=1.35)
        self.at("others pierce")
        self.play(Indicate(through, color=PURPLE, scale_factor=1.11), run_time=1.65)
        self.at("on opposite sides")
        lumen, cytosol = lumen_and_cytosol()
        self.play(FadeIn(lumen), FadeIn(cytosol), run_time=0.65)
        self.at("watching an intact")
        self.play(FadeOut(lumen), FadeOut(cytosol), run_time=0.65)
        self.at("two paired assays")
        paired = label("Burial   /   Sidedness", 4.0, 0.33, TEXT, 34)
        self.play(FadeIn(paired), run_time=0.55)
        self.play(FadeOut(outside), FadeOut(inside), run_time=0.75)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Membrane protein extraction and topology assays"
    TITLE = "Mapping How Proteins Sit in Membranes"

    def construct(self):
        wall = VGroup(membrane(drifting=False), peripheral(), spanning())
        self.add(wall)
        shade = Rectangle(width=config.frame_width, height=config.frame_height, stroke_width=0,
                          fill_color=BG, fill_opacity=0.91)
        title = T(self.TITLE, 51, TEXT, font=TITLE_FONT).move_to(UP * 0.30)
        fit(title, max_w=12.0)
        lesson = T(self.LESSON, 29, TEXT).move_to(DOWN * 0.57)
        self.play(FadeIn(shade), run_time=0.20)
        self.play(FadeIn(title), FadeIn(lesson), run_time=0.40)
        self.wait(1.00)
        self.play(FadeOut(title), FadeOut(lesson), run_time=0.20)
        self.play(FadeOut(shade), run_time=0.20)


class S03Extraction(SpokenScene):
    def construct(self):
        wall, outer, through = membrane(), peripheral(), spanning()
        scope = schematic()
        self.add(wall, outer, through, scope)
        self.at("first test burial")
        heading = label("Test burial", 4.20, 2.05, TEXT, 40)
        self.play(FadeIn(heading), run_time=0.45)
        self.at("wash membranes")
        flow = wash()
        self.add(flow)
        wash_label = chip("High salt or high pH", ORANGE, 30).move_to(point(4.14, -0.02))
        self.play(FadeIn(wash_label), run_time=0.55)
        self.at("called alkaline extraction")
        alkaline = label("High pH: alkaline extraction", 4.05, -0.89, TEXT, 28)
        self.play(FadeIn(alkaline), run_time=0.55)
        self.at("loosen proteins held")
        perch = outer.get_center()
        self.play(outer.animate.shift(UR * 0.24), run_time=1.45, rate_func=there_and_back)
        self.at("by contacts at")
        self.play(outer.animate.move_to(perch + UR * 0.31), run_time=1.20)
        self.at("peripheral proteins come")
        self.play(FadeOut(heading), FadeOut(wash_label), FadeOut(alkaline), run_time=0.38)
        self.play(outer.animate.move_to(point(3.86, 1.15)).rotate(0.40), run_time=1.45)
        outer_label = label("Peripheral · in liquid", 4.05, 2.02, PURPLE, 32)
        self.play(FadeIn(outer_label), run_time=0.45)
        bob(outer, amp=0.15, speed=3)
        self.at("integral proteins stay")
        self.play(FadeOut(flow), Indicate(through, color=PURPLE, scale_factor=1.10), run_time=0.85)
        integral = label("Integral · in membrane", 4.10, -0.43, PURPLE, 30)
        self.play(FadeIn(integral), run_time=0.45)
        self.at("are spun down")
        wall.clear_updaters(recursive=True)
        pellet = VGroup(wall, through)
        self.play(pellet.animate.shift(DOWN * 0.66), run_time=1.12)
        pellet_label = label("Membrane pellet", 4.14, -1.43, TEXT, 30)
        self.play(FadeIn(pellet_label), run_time=0.4)
        self.at("only soap")
        self.play(FadeOut(outer), FadeOut(outer_label), FadeOut(integral), FadeOut(pellet_label),
                  run_time=0.4)
        bubbles = detergent_cloud().shift(DOWN * 0.66)
        detergent = label("Detergent", 4.10, 2.0, ORANGE, 35)
        self.play(LaggedStart(*[GrowFromCenter(b) for b in bubbles], lag_ratio=0.08),
                  FadeIn(detergent), run_time=1.05)
        self.at("dissolves the bilayer")
        micelles = VGroup(*[VGroup(detergent_ring(point(x, y), 0.45),
                                    Dot(point(x, y), radius=0.23, color=GREY))
                            for x, y in [(-4.88, 0.98), (-5.02, -1.18), (-3.48, -2.50),
                                         (-2.20, -0.95), (-3.31, 1.65), (-0.45, -2.10),
                                         (0.30, 0.43), (1.28, -0.64), (-0.54, 1.70)]])
        self.play(FadeOut(wall), FadeOut(bubbles), FadeIn(micelles, scale=0.70), run_time=0.95)
        self.at("releases them")
        freed = label("Integral protein released", 4.10, -0.20, PURPLE, 29)
        self.play(through.animate.move_to(point(3.88, 0.83)), FadeIn(freed), run_time=0.9)
        bob(micelles, amp=0.14, speed=2.5)
        self.finish()


class S04Topology(SpokenScene):
    def construct(self):
        wall, protein = membrane(), spanning()
        question = label("Which end faces each side?", 4.13, 1.06, TEXT, 30)
        q_out, q_in = label("?", -1.52, 2.73, GOLD, 47), label("?", -1.52, 0.93, GOLD, 47)
        self.add(wall, protein, schematic())
        self.at("ask its topology")
        self.play(FadeIn(q_out), FadeIn(q_in), run_time=0.58)
        bob(q_out, amp=0.12, speed=2.7)
        bob(q_in, amp=0.12, speed=2.7, seed=3)
        self.at("which end faces")
        self.play(FadeIn(question), run_time=0.50)
        self.at("break cells")
        opened = membrane(opened=True, drifting=False)
        self.play(FadeOut(question), FadeOut(q_out), FadeOut(q_in),
                  FadeOut(wall), FadeIn(opened), run_time=0.9)
        self.at("membranes reseal")
        closed = membrane()
        self.play(FadeOut(opened), FadeIn(closed), run_time=1.2)
        self.bring_to_front(protein)
        self.at("sealed microsomes")
        heading = label("Sealed ER microsome", 4.04, 1.69, TEXT, 32)
        lumen, cytosol = lumen_and_cytosol()
        self.play(FadeIn(heading), run_time=0.48)
        self.at("lumen inside")
        self.play(FadeIn(lumen), FadeIn(cytosol), run_time=0.56)
        self.at("distinct antibody tags")
        outside, inside = tag_mark(OUT_TAG, GOLD), tag_mark(IN_TAG, BLUE)
        self.play(FadeIn(outside, shift=DOWN * 0.13),
                  FadeIn(inside, shift=UP * 0.13), run_time=0.8)
        self.at("then add protein")
        strip, outer_band, inner_band = protection_gel()
        self.play(FadeOut(heading), FadeOut(lumen), FadeOut(cytosol), run_time=0.35)
        cutter = scissors(point(2.25, 1.35))
        self.play(FadeIn(strip), FadeIn(outer_band), FadeIn(inner_band),
                  FadeIn(cutter, shift=LEFT * 0.35), run_time=0.79)
        self.at("protease cannot cross")
        self.play(cutter.animate.move_to(point(1.75, 0.47)), run_time=0.60)
        self.play(cutter.animate.move_to(point(2.52, 1.15)), run_time=0.52)
        self.play(cutter.animate.move_to(point(-0.98, 2.81)), run_time=1.42)
        self.at("removes the cytosolic")
        self.play(cutter.animate.shift(LEFT * 0.64), run_time=0.42)
        self.play(FadeOut(outside, shift=UR * 0.29), FadeOut(outer_band),
                  cutter.animate.shift(UR * 0.41), run_time=0.64)
        self.at("leaving the luminal")
        self.play(FadeOut(cutter), Indicate(inside, color=BLUE, scale_factor=1.22),
                  Indicate(inner_band, color=BLUE, scale_factor=1.14), run_time=1.25)
        self.finish()


def prediction_card():
    return question_card(QUESTION, **QUESTION_STYLE)


def doubt_mark():
    return label("?", -1.50, 0.96, GOLD, 47)


class S05Predict(SpokenScene):
    def construct(self):
        result, tag, band = protection_result()
        question, mark = prediction_card(), doubt_mark()
        self.add(result)
        self.at("pause and test")
        self.play(FadeIn(question), run_time=0.85)
        self.at("one tag survives")
        self.play(Indicate(band, color=BLUE, scale_factor=1.18), run_time=1.35)
        self.at("does survival alone")
        self.play(FadeIn(mark), Indicate(tag, color=BLUE, scale_factor=1.19), run_time=1.15)
        self.at("what else could")
        self.play(Indicate(mark, color=GOLD, scale_factor=1.24), run_time=1.6)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    SECONDS = 4.5

    def backdrop(self):
        result, _, _ = protection_result(drifting=False, phase=PREDICT_END_PHASE)
        return result

    def construct(self):
        mark = doubt_mark()
        clock = 0.0

        def glow(mob, dt):
            nonlocal clock
            clock += dt
            mob.set_opacity(0.86 + 0.14 * np.cos(TAU * clock / self.SECONDS))

        self.add(self.backdrop(), prediction_card(), mark.add_updater(glow))
        self.wait(self.SECONDS)


class S07Controls(SpokenScene):
    def construct(self):
        result, _, _ = protection_result(drifting=False, phase=PREDICT_END_PHASE)
        question, mark = prediction_card(), doubt_mark()
        self.add(result, question, mark)
        self.at("no the tag")
        self.play(FadeOut(question), FadeOut(mark), run_time=0.52)
        resistant = label("Could the tag resist?", 3.8, 2.45, GOLD, 31)
        self.play(FadeIn(resistant), Indicate(result[2], color=BLUE, scale_factor=1.13), run_time=1.0)
        self.at("add detergent first")
        # Begin a fresh aliquot. The sealed lane at left keeps the comparison result.
        wall, protein, inside, _, _, scope = result
        outside = tag_mark(OUT_TAG, GOLD)
        open_lane = block(1.64, 2.63, GEL, point(5.66, -0.30), opacity=0.90).set_stroke(GREY, 2)
        open_label = label("Opened", 5.66, -1.92, ORANGE)
        gold_band, cyan_band = gel_band(5.66, 0.33, GOLD), gel_band(5.66, -0.83, BLUE)
        rings = detergent_cloud()
        treatment = label("Detergent first", 4.05, 2.56, ORANGE, 31)
        self.play(swap(resistant, treatment), FadeIn(outside), FadeIn(rings), run_time=0.68)
        self.at("open the vesicles")
        opened = membrane(opened=True)
        self.play(FadeOut(wall), FadeOut(rings), FadeIn(opened), FadeIn(open_lane),
                  FadeIn(open_label), FadeIn(gold_band), FadeIn(cyan_band), run_time=0.94)
        self.bring_to_front(protein, outside, inside)
        self.at("if both tags vanish")
        cutter_out, cutter_in = scissors(point(-0.63, 2.71)), scissors(point(2.45, -0.33))
        self.play(FadeOut(treatment), FadeIn(cutter_out), FadeIn(cutter_in), run_time=0.35)
        self.play(cutter_out.animate.move_to(point(-1.72, 2.73)),
                  cutter_in.animate.move_to(point(0.65, -0.32)), run_time=0.52)
        self.play(FadeOut(outside, shift=UP * 0.18), FadeOut(gold_band),
                  cutter_in.animate.move_to(point(-1.64, 1.0)), run_time=0.62)
        self.play(FadeOut(inside, shift=RIGHT * 0.17), FadeOut(cyan_band),
                  cutter_out.animate.move_to(point(-2.40, 2.94)),
                  cutter_in.animate.move_to(point(-0.85, 0.73)), run_time=0.55)
        self.at("did the protecting")
        protected = label("The seal protected the tag", 3.87, 2.62, GREEN, 28)
        self.play(FadeIn(protected), Indicate(result[4], color=BLUE, scale_factor=1.13),
                  cutter_out.animate.move_to(point(-4.28, 2.47)),
                  cutter_in.animate.move_to(point(2.34, -0.24)), run_time=1.34)
        self.at("washes test burial", lead=0.65)
        sealed_gel = VGroup(result[3], result[4])
        opened_gel = VGroup(open_lane, open_label)
        intact = membrane()
        self.play(FadeOut(protected), FadeOut(cutter_out), FadeOut(cutter_in),
                  FadeOut(sealed_gel), FadeOut(opened_gel), FadeOut(opened), FadeIn(intact), run_time=0.45)
        self.bring_to_front(protein, scope)
        recap_flow = wash()
        burial = label("Washes test burial", 4.0, 0.33, TEXT, 33)
        self.play(FadeIn(recap_flow), FadeIn(burial), run_time=0.45)
        self.at("protease with and without", lead=0.35)
        sidedness = caption("Protease ± detergent tests sidedness", 33, TEXT, y=-3.30)
        self.play(FadeOut(burial), FadeOut(recap_flow), run_time=0.25)
        self.play(FadeIn(sidedness), FadeOut(intact), FadeIn(opened),
                  FadeIn(sealed_gel), FadeIn(opened_gel), run_time=0.45)
        self.bring_to_front(protein, scope)
        self.at("one extraction catch")
        self.play(FadeOut(sealed_gel), FadeOut(opened_gel),
                  FadeOut(sidedness), FadeOut(opened), FadeIn(intact), run_time=0.75)
        self.bring_to_front(protein, scope)
        self.at("lipid anchored proteins")
        p = rim_point(0.68)
        anchor = block(0.21, 0.72, YELLOW, p, radius=0.09).rotate(-0.68)
        tethered = block(0.89, 0.54, PURPLE, p + point(0.42, 0.37), radius=0.23).rotate(-0.34)
        anchor_name = label("Lipid-anchored protein", 4.03, 1.88, PURPLE, 31)
        self.play(FadeIn(anchor), FadeIn(tethered), run_time=0.71)
        self.play(FadeIn(anchor_name), run_time=0.50)
        self.at("resist washes")
        flow = wash()
        self.add(flow)
        wash_label = label("High salt or high pH", 4.05, -0.20, ORANGE, 30)
        self.play(FadeIn(wash_label), run_time=0.50)
        self.at("lipid tail sits")
        self.play(Indicate(anchor, color=YELLOW, scale_factor=1.19), run_time=1.45)
        self.finish()


def sugar_gel():
    x = 4.16
    box = block(1.80, 2.78, GEL, point(x, -0.38), opacity=0.90).set_stroke(GREY, 2)
    heading = label("Gel", x, 1.52)
    return VGroup(box, heading), gel_band(x, -1.12, PURPLE)


class S08SecondTest(SpokenScene):
    def construct(self):
        wall = membrane()
        segment = block(0.34, 0.91, PURPLE, point(-2.15, 1.01), radius=0.14)
        self.add(wall, spanning(), segment, schematic())
        self.at("a second test")
        heading = label("Sugar mapping", 4.06, 2.15, TEXT, 35)
        self.play(FadeIn(heading), run_time=0.48)
        self.at("cells add")
        sugar = sugar_mark(point(-2.15, 0.49)).rotate(PI)
        sugar.align_to(segment.get_bottom() + UP * 0.03, UP)
        lumen, _ = lumen_and_cytosol()
        lumen.shift(DOWN * 0.48)
        self.play(FadeIn(sugar, shift=DOWN * 0.3), run_time=0.96)
        self.at("only inside")
        self.play(FadeIn(lumen), run_time=0.48)
        self.at("a sugar makes")
        gel, band = sugar_gel()
        self.play(FadeIn(gel), FadeIn(band), FadeOut(heading), run_time=0.66)
        self.at("run higher")
        self.play(band.animate.shift(UP * 1.40).set_color(YELLOW), run_time=0.93)
        self.at("if endoglycosidase")
        enzyme = label("Endoglycosidase H", 4.10, 2.30, ORANGE, 31)
        self.play(FadeIn(enzyme), run_time=0.53)
        self.at("removes that shift")
        self.play(FadeOut(sugar, shift=LEFT * 0.42),
                  band.animate.shift(DOWN * 1.40).set_color(PURPLE), run_time=1.15)
        self.at("the end carrying")
        evidence = label("This end reached the lumen", 4.00, 2.32, GREEN, 28)
        self.play(swap(enzyme, evidence),
                  Indicate(segment, color=BLUE, scale_factor=1.12), run_time=1.05)
        self.at("sites closer than")
        short_zone = BraceBetweenPoints(point(-1.85, 1.62), point(-1.85, 0.85),
                                        direction=RIGHT, color=YELLOW, buff=0)
        residue_count = T("12–14", 29, YELLOW).next_to(short_zone.get_tip(), RIGHT, buff=0.12)
        residue_count.shift(DOWN * 0.12)
        residue_unit = T("residues", 29, YELLOW).next_to(residue_count, DOWN, buff=0.07, aligned_edge=LEFT)
        zone_label = VGroup(residue_count, residue_unit)
        site = Dot(point(-2.15, 1.15), radius=0.11, color=YELLOW)
        self.play(FadeOut(evidence), FadeOut(lumen), FadeIn(short_zone), FadeIn(site), run_time=0.68)
        self.at("12 to 14 residues")
        self.play(FadeIn(zone_label), run_time=0.56)
        self.at("go unused")
        self.play(Indicate(site, color=YELLOW, scale_factor=1.40), run_time=1.15)
        self.at("a missing sugar")
        caution = label("No sugar ≠ cytosol", 4.12, 2.29, RED, 34)
        self.play(FadeIn(caution), Indicate(band, color=PURPLE, scale_factor=1.13), run_time=1.3)
        self.finish()


def channel():
    posts = VGroup(*[block(0.29, 0.79, PURPLE, PROTEIN_AT + RIGHT * sign * 0.38, radius=0.12)
                     for sign in (-1, 1)])
    return posts


def ribosome(at):
    base = block(1.00, 0.34, BLUE, point(0, -0.14), radius=0.15)
    cap = block(0.84, 0.43, BLUE, point(0, 0.16), radius=0.18)
    return VGroup(base, cap).shift(at)


def chain_path(points):
    return VMobject().set_points_smoothly([point(*p) for p in points]).set_stroke(PURPLE, 10)


class S09UnlockedA(SpokenScene):
    def construct(self):
        wall, gate = membrane(), channel()
        self.add(wall, gate, schematic())
        self.at("these assays unlocked")
        intro = label("How proteins enter the ER", 4.00, 0.55, TEXT, 30)
        self.play(FadeIn(intro), run_time=0.70)
        self.at("in 1975")
        name = label("Blobel & Dobberstein", 4.07, 2.18, TEXT, 32)
        year = label("1975", 4.07, 1.64, GOLD, 30)
        self.play(FadeOut(intro), FadeIn(name), FadeIn(year), run_time=0.75)
        self.at("applied protease protection")
        cutter = scissors(point(2.12, 0.50))
        self.play(FadeIn(cutter), run_time=0.45)
        bob(cutter, amp=0.19, speed=2.5)
        self.at("pancreas microsomes")
        source = label("Dog-pancreas microsome", 4.09, -0.91, TEAL, 29)
        ribo = ribosome(point(-2.16, 2.90))
        self.play(FadeIn(source), FadeIn(ribo, shift=DOWN * 0.36), run_time=0.76)
        self.at("a mouse antibody")
        path = chain_path([(-2.16, 2.58), (-2.16, 1.98), (-2.11, 1.43),
                           (-1.58, 0.81), (-1.31, 0.42), (-1.55, 0.02), (-2.16, -0.23)])
        tip = tag_mark(point(-2.39, -0.30), GOLD).rotate(0.2)
        light_chain = label("Mouse antibody light chain", 4.00, -1.71, PURPLE, 28)
        self.play(Create(path), FadeIn(light_chain), run_time=1.3)
        self.play(FadeIn(tip), run_time=0.27)
        self.at("was trimmed")
        self.play(FadeOut(tip, shift=DL * 0.30), run_time=0.59)
        self.at("hidden inside")
        proof = label("Protected from protease", 4.00, -0.27, GREEN, 30)
        self.play(FadeIn(proof), run_time=0.53)
        self.at("present during synthesis")
        during = label("During synthesis", 4.09, -2.54, TEXT, 30)
        self.play(FadeIn(during), run_time=0.57)
        self.at("in 1981")
        name2 = label("Walter & Blobel", 4.07, 2.18, TEXT, 32)
        year2 = label("1981", 4.07, 1.64, GOLD, 30)
        factor = tag_mark(point(-1.42, 2.46), GREEN)
        self.play(swap(name, name2), swap(year, year2),
                  FadeOut(path), FadeOut(cutter), FadeOut(source), FadeOut(light_chain),
                  FadeOut(proof), FadeOut(during), FadeIn(factor), run_time=0.83)
        self.at("washed those membranes")
        stream = wash()
        self.add(stream)
        salt = label("High-salt wash", 4.08, 0.12, ORANGE, 31)
        self.play(FadeIn(salt), run_time=0.56)
        self.at("high salt")
        self.play(factor.animate.move_to(point(2.45, 0.82)), run_time=1.18)
        self.at("ribosome binding vanished")
        undocked = label("Ribosome fails to dock", 4.03, -1.35, TEXT, 30)
        self.play(ribo.animate.shift(LEFT * 1.60 + UP * 0.30),
                  FadeOut(stream), FadeOut(factor), FadeIn(undocked), run_time=1.18)
        self.at("until purified signal")
        restored = label("Signal recognition particle", 4.06, 0.12, GREEN, 29)
        add_back = tag_mark(point(0.30, 2.60), GREEN)
        self.play(swap(salt, restored), FadeOut(undocked), FadeIn(add_back), run_time=0.95)
        self.play(add_back.animate.move_to(point(-1.42, 2.46)), run_time=0.88)
        self.at("particle restored")
        docking = label("Ribosome docks again", 4.03, -1.35, GREEN, 30)
        self.play(ribo.animate.move_to(point(-2.16, 2.90)), FadeIn(docking), run_time=1.15)
        self.finish()


def crossing_gauge(tracker):
    x, y = 4.09, -1.32
    height, width = 0.31, 3.24
    track = block(width, height, GEL, point(x, y), radius=0.08).set_stroke(GREY, 2)
    left = x - width / 2 + 0.07

    def fill_bar():
        filled = (width - 0.14) * tracker.get_value() / 100
        return block(filled, height - 0.12, TEAL, point(left + filled / 2, y), radius=0.055)

    bar = always_redraw(fill_bar)
    reading = counter("≈{:.0f}%", tracker, point(x, -0.68), size=38, color=TEXT)
    title = label("C-terminal crossing", x, 0.02, TEXT, 31)
    return VGroup(track, bar, title, reading)


class S10UnlockedB(SpokenScene):
    def construct(self):
        wall, gate = membrane(), channel()
        path = chain_path([(-3.21, 3.04), (-2.50, 2.65), (-2.16, 2.10),
                           (-2.11, 1.39), (-1.80, 0.83), (-1.36, 0.69)])
        self.add(wall, gate, schematic())
        self.at("in 1999")
        name = label("Goder, Bieri & Spiess", 4.04, 2.27, TEXT, 33)
        year = label("1999", 4.04, 1.68, GOLD, 30)
        self.play(FadeIn(name), FadeIn(year), Create(path), run_time=1.4)
        self.at("combined sugar mapping")
        methods = label("Sugar mapping +\nalkaline extraction", 4.08, 0.20, TEXT, 30)
        self.play(FadeIn(methods), run_time=0.59)
        self.at("cos -1 cells")
        cells = label("COS-1 cells", 4.08, -0.91, TEAL, 31)
        self.play(FadeIn(cells), run_time=0.57)
        self.at("one added sugar site")
        attachment = path.get_end()
        sugar = sugar_mark(attachment + UP * 0.025)
        self.play(FadeIn(sugar, shift=LEFT * 0.24), FadeOut(methods), FadeOut(cells), run_time=0.83)
        self.at("the chain's tail end")
        tail_name = label("C terminus", -0.47, 0.25, TEXT, 31)
        self.play(FadeIn(tail_name), run_time=0.55)
        self.at("its c -terminus")
        crossing = ValueTracker(75)
        gauge = crossing_gauge(crossing)
        self.play(FadeIn(gauge), run_time=0.55)
        gauge.suspend_updating()
        self.at("to 30 percent", lead=0.53)
        gauge.resume_updating()
        self.play(crossing.animate.set_value(30), run_time=0.65)
        gauge.suspend_updating()
        self.at("growing chains can")
        reoriented = chain_path([(-3.21, 3.04), (-2.47, 2.78), (-2.28, 2.44),
                                 (-2.28, 1.93), (-2.27, 1.58), (-2.15, 1.36),
                                 (-2.03, 1.58), (-2.02, 1.94), (-2.02, 2.34),
                                 (-1.94, 2.60), (-1.46, 2.75)])
        # Split at the hairpin tip so the returning leg grows from the attached sugar.
        hairpin = reoriented.get_subcurve(0, 0.5)
        ascending = reoriented.get_subcurve(0.5, 1)
        starting_sugar = sugar.copy()

        def follow_hairpin(mob, alpha):
            mob.become(starting_sugar).rotate(-PI * alpha, about_point=attachment)
            mob.shift(path.get_end() - attachment)

        self.play(FadeOut(tail_name), Transform(path, hairpin),
                  UpdateFromAlphaFunc(sugar, follow_hairpin), run_time=0.80)
        self.play(Create(ascending), run_time=0.53)
        self.at("the entry channel")
        self.play(Indicate(gate, color=PURPLE, scale_factor=1.16), run_time=0.90)
        self.at("strip the surface")
        protein, outer = spanning(), peripheral()
        flow = wash()
        self.play(FadeOut(name), FadeOut(year), FadeOut(gauge), FadeOut(path), FadeOut(ascending),
                  FadeOut(sugar), FadeOut(gate), FadeIn(protein), FadeIn(outer), run_time=0.47)
        kept = tag_mark(IN_TAG, BLUE)
        self.add(flow)
        self.play(FadeIn(kept), outer.animate.shift(RIGHT * 1.33 + DOWN * 0.38), run_time=0.70)
        self.at("open the seal")
        opened = membrane(opened=True)
        detergent = detergent_ring(point(1.46, 0.39))
        cutter = scissors(point(2.30, -0.32))
        self.play(FadeOut(wall), FadeOut(flow), FadeIn(opened), FadeIn(detergent), run_time=0.62)
        self.bring_to_front(protein, kept)
        self.at("the parts reveal")
        self.play(FadeIn(cutter), run_time=0.25)
        self.play(cutter.animate.move_to(point(-1.53, 0.42)), run_time=0.85)
        self.play(FadeOut(kept, shift=UP * 0.25), cutter.animate.shift(DOWN * 0.54), run_time=0.47)
        self.finish()


class S11End(EndCard):
    LINE = "Washes test burial; protease with and without detergent proves each side."
