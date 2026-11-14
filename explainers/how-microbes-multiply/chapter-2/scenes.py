"""Built Now, or Carried Along — chapter 2 of How microbes multiply.

COLOR MAP (shared by both chapters)
  CELL_GREEN = bacterial cell, a pale green rounded rod
  BLUE       = bacterial chromosome
  ORANGE     = phage DNA, phage heads, and phage parts
  GREY       = phage tails, apparatus, and de-emphasised structure
  YELLOW     = questions, switching, and the item to notice

All biological drawings are schematic cartoons.  Builder functions below are reused wherever a
picture carries between scenes so scale and position stay exact.
"""
from bp_parts import *  # noqa: F401,F403


ORANGE = "#F29E4C"
CELL_GREEN = "#A8D5BA"
CHARCOAL = "#252A32"
BROWN = "#9A6B4F"


def rod(width=6.0, height=2.7, center=ORIGIN, chromosome=True, prophage=False, grey=False):
    """The film's bacterial cell: pale green rod and one blue chromosome loop."""
    col = GREY if grey else CELL_GREEN
    body = RoundedRectangle(corner_radius=height * 0.46, width=width, height=height,
                            stroke_color=col, stroke_width=5, fill_color=col,
                            fill_opacity=0.13).move_to(center)
    g = VGroup(body)
    if chromosome:
        loop = Ellipse(width=width * 0.48, height=height * 0.48, color=BLUE,
                       stroke_width=7).move_to(center)
        g.add(loop)
        g.chromosome = loop
        if prophage:
            cx, cy = np.array(center, dtype=float)[:2]
            rx, ry = width * 0.24, height * 0.24
            seg = ParametricFunction(lambda t: [cx + rx * np.cos(t), cy + ry * np.sin(t), 0],
                                     t_range=[-0.35, 0.40], color=ORANGE, stroke_width=9)
            g.add(seg)
            g.prophage = seg
    g.body = body
    return g


def phage(scale=1.0, center=ORIGIN):
    """Orange hexagon head, short grey tail and legs."""
    head = RegularPolygon(6, radius=0.43 * scale, color=ORANGE, stroke_width=4,
                          fill_color=ORANGE, fill_opacity=0.28)
    tail = Line(head.get_bottom(), head.get_bottom() + DOWN * 0.65 * scale,
                color=GREY, stroke_width=5)
    foot = tail.get_end()
    legs = VGroup(Line(foot, foot + LEFT * 0.34 * scale + DOWN * 0.25 * scale,
                       color=GREY, stroke_width=4),
                  Line(foot, foot + RIGHT * 0.34 * scale + DOWN * 0.25 * scale,
                       color=GREY, stroke_width=4))
    g = VGroup(head, tail, legs).move_to(center)
    g.head, g.tail, g.legs = head, tail, legs
    return g


def dna_strand(width=2.0, center=ORIGIN):
    return ArcBetweenPoints(np.array(center) + LEFT * width / 2,
                            np.array(center) + RIGHT * width / 2,
                            angle=0.45, color=ORANGE, stroke_width=7)


def ellipse_arc(width, height, start_angle, angle, color, stroke_width, center=ORIGIN):
    """An Arc reshaped into an ellipse (Manim's Arc has no width/height constructor args)."""
    a = Arc(radius=1.0, start_angle=start_angle, angle=angle, color=color,
            stroke_width=stroke_width)
    a.stretch_to_fit_width(width).stretch_to_fit_height(height).move_to(center)
    return a


def part_set(center=ORIGIN, spread=1.0):
    """Loose phage heads, tails and DNA—the experiment's early material."""
    c = np.array(center, dtype=float)
    heads = VGroup(*[RegularPolygon(6, radius=0.34, color=ORANGE, stroke_width=4,
                                    fill_color=ORANGE, fill_opacity=0.25).move_to(c + q * spread)
                     for q in (LEFT * 1.45 + UP * 0.55, RIGHT * 0.15 + UP * 0.7)])
    tails = VGroup(*[Line(c + q * spread, c + (q + DOWN * 0.75) * spread,
                              color=GREY, stroke_width=5)
                     for q in (LEFT * 0.45 + DOWN * 0.2, RIGHT * 1.3 + DOWN * 0.05)])
    strands = VGroup(dna_strand(1.2, c + LEFT * 1.2 + DOWN * 0.75),
                     dna_strand(1.2, c + RIGHT * 0.7 + DOWN * 0.8))
    return VGroup(heads, tails, strands)


def readout_box(label, value, center, value_color=TEXT, width=3.0):
    txt = M(f"{label}: {value}", 28, value_color)
    width = max(width, txt.width + 0.6)
    box = RoundedRectangle(corner_radius=0.16, width=width, height=0.72,
                           stroke_color=GREY, stroke_width=2.5,
                           fill_color=CHARCOAL, fill_opacity=0.96).move_to(center)
    txt.move_to(box)
    txt.layout_ok = True  # intended text inside its own charcoal readout
    return VGroup(box, txt)


def schematic_tag():
    return scope_tag("schematic")


def question_mark(moving=False):
    q = T("?", 76, YELLOW, weight=BOLD).move_to([4.8, 0.0, 0])
    if moving:
        q._pulse_t, q._base_h = 0.0, q.height

        def breathe(mob, dt):
            mob._pulse_t += dt
            mob.set_height(mob._base_h * (1 + 0.16 * np.sin(2.3 * mob._pulse_t)))
        q.add_updater(breathe)
    return q


def early_cell(question=False):
    c = rod(7.2, 4.1, [0, 0.25, 0], chromosome=False)
    parts = part_set([0, 0.3, 0], 1.25)
    g = VGroup(c, parts, readout_box("whole phages", "?" if question else "0",
                                    [4.8, 2.8, 0], YELLOW if question else TEXT, 3.2))
    return g


def lysogenic_cell(width=5.6, height=2.5, center=ORIGIN):
    return rod(width, height, center, chromosome=True, prophage=True)


def mini_family(rows=2, cols=4, center=[0, -0.2, 0], width=2.5, height=1.15, pitch=1.45):
    cells = VGroup()
    for r in range(rows):
        for c in range(cols):
            x = (c - (cols - 1) / 2) * 2.9
            y = ((rows - 1) / 2 - r) * pitch
            cells.add(lysogenic_cell(width, height, np.array(center) + [x, y, 0]))
    return cells


def lytic_cycle_diagram(center=ORIGIN, scale=1.0):
    c = np.array(center, dtype=float)
    pts = [c + UP * 1.75 * scale, c + RIGHT * 2.45 * scale,
           c + DOWN * 1.75 * scale, c + LEFT * 2.45 * scale]
    labels = ["inject DNA", "parts built", "assembled", "burst"]
    icons = VGroup(phage(0.42 * scale, pts[0]), part_set(pts[1], 0.28 * scale),
                   VGroup(*[phage(0.28 * scale) for _ in range(3)]).arrange(RIGHT, buff=0.15).move_to(pts[2]),
                   VGroup(Line(pts[3] + UL * 0.38, pts[3] + DR * 0.38, color=RED, stroke_width=7),
                          Line(pts[3] + DL * 0.38, pts[3] + UR * 0.38, color=RED, stroke_width=7)))
    offsets = (LEFT * 1.45, RIGHT * 1.45, RIGHT * 1.45, UP * 0.85)
    labs = VGroup(*[T(t, 28, ORANGE if i < 3 else RED).move_to(p + offsets[i] * scale)
                    for i, (t, p) in enumerate(zip(labels, pts))])
    arrows = VGroup(*[CurvedArrow(pts[i] + (pts[(i+1) % 4] - pts[i]) * 0.28,
                                        pts[(i+1) % 4] - (pts[(i+1) % 4] - pts[i]) * 0.28,
                                        angle=-0.45, color=GREY, stroke_width=4,
                                        tip_length=0.18)
                          for i in range(4)])
    return VGroup(arrows, icons, labs)


class S00Title(TitleCard):
    LESSON = "How microbes multiply"
    TITLE = "Built Now, or Carried Along"

    def construct(self):
        cell = rod(7.2, 2.6, [0, -0.35, 0], chromosome=False)
        parts = part_set([0, -0.25, 0], 0.9)
        title = T(self.TITLE, 48, TEXT, font=TITLE_FONT).move_to([0, 2.7, 0])
        lesson = T(self.LESSON.upper(), 22, GREY).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(cell, scale=0.94), run_time=self.beat(0.22))
        self.play(LaggedStart(*[FadeIn(p, scale=0.6) for p in parts], lag_ratio=0.08),
                  Write(title), FadeIn(lesson), run_time=self.beat(0.48))
        self.wait(self.beat(0.15))
        self.play(FadeOut(VGroup(cell, parts, title, lesson)), run_time=self.beat(0.15))
        self.finish()


class S01Link(SpokenScene):
    def construct(self):
        cell = rod(8.4, 4.2, [0, 0.15, 0], chromosome=False)
        strand = dna_strand(2.4, [-1.7, 0.7, 0])
        self.play(FadeIn(cell), Create(strand), run_time=0.7)
        self.at("cell building")
        parts = part_set([1.35, 0.2, 0], 0.8)
        self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in parts], lag_ratio=0.08), run_time=0.8)
        count = readout_box("new phages", "0", [4.75, 2.85, 0], TEXT, 3.25)
        self.play(FadeIn(count), run_time=0.4)
        self.at("So how")
        q = question_card("One phage never divides. How does it become many?", y=-3.0,
                          size=32, max_w=10.6)
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.7)
        pulse(cell.body, base=5, amp=1.2, speed=2)
        self.add(schematic_tag())
        self.finish()


class S02Test(SpokenScene):
    def construct(self):
        title = T("open cells at different times", 36, TEXT).move_to([0, 3.25, 0])
        line = Arrow([-5.4, -1.25, 0], [5.5, -1.25, 0], color=GREY, stroke_width=5, tip_length=0.25)
        times = VGroup(*[chip(t, col, 30) for t, col in zip(("early", "middle", "late"),
                                                            (YELLOW, ORANGE, RED))])
        times.arrange(RIGHT, buff=1.45).move_to([0, -2.0, 0])
        tubes = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.12, width=1.35, height=2.4,
                                                color=GREY, stroke_width=4),
                                      rod(0.9, 0.42, chromosome=False)).arrange(DOWN, buff=-1.45)
                         for _ in range(3)])
        tubes.arrange(RIGHT, buff=2.0).move_to([0, 0.6, 0])
        self.at("Scientists tested")
        self.play(FadeIn(title), run_time=0.5)
        self.at("infected bacteria")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in tubes], lag_ratio=0.16),
                  Create(line), FadeIn(times), run_time=1.1)
        crack = VGroup(Line([-4.15, 1.1, 0], [-3.7, 0.55, 0], color=YELLOW, stroke_width=7),
                       Line([-3.7, 0.55, 0], [-4.05, 0.05, 0], color=YELLOW, stroke_width=7))
        self.at("broke some cells open")
        spill = part_set([-3.8, 0.75, 0], 0.52)
        self.play(Create(crack), tubes[0].animate.set_stroke(opacity=0.35), FadeIn(spill), run_time=0.6)
        self.play(spill.animate.move_to([4.25, 2.25, 0]), run_time=2.2, rate_func=linear)
        dish = Ellipse(width=3.2, height=0.8, color=GREY, stroke_width=4).move_to([4.25, 2.25, 0])
        dish_label = T("look for whole phages", 28, TEXT).next_to(dish, LEFT, buff=0.2)
        self.at("looked for whole")
        self.play(FadeIn(dish), FadeIn(dish_label), run_time=0.6)
        self.add(schematic_tag())
        self.finish()


class S03Predict(SpokenScene):
    def construct(self):
        world = early_cell(question=True)
        self.play(FadeIn(world[0]), run_time=0.5)
        self.at("plenty of phage material")
        self.play(LaggedStart(*[FadeIn(x, scale=0.7) for x in world[1]], lag_ratio=0.08), run_time=0.8)
        self.play(FadeIn(world[2]), run_time=0.4)
        self.at("How many whole")
        q = question_card("How many whole phages are inside?", y=-3.05, size=34)
        mark = question_mark()
        self.play(FadeIn(q.question, shift=UP * 0.1), FadeIn(mark), run_time=0.6)
        self.add(schematic_tag())
        self.finish()


class S04Pause(PredictPause):
    QUESTION = "How many whole phages are inside?"
    SECONDS = 5.0
    RING_AT = (-6.0, -3.0, 0)

    def backdrop(self):
        return VGroup(early_cell(question=True), question_mark(moving=True), schematic_tag())


class S05Reveal(SpokenScene):
    def construct(self):
        world = early_cell(question=False)
        self.add(world, schematic_tag())
        self.at("None")
        self.play(Indicate(world[2], color=YELLOW, scale_factor=1.08), run_time=0.7)
        self.at("phage parts")
        heads, tails, strands = world[1]
        targets = [[-3.4, -0.2, 0], [0, -0.2, 0], [3.35, -0.2, 0]]
        self.play(heads.animate.arrange(DOWN, buff=0.18).move_to(targets[0]),
                  tails.animate.arrange(RIGHT, buff=0.25).move_to(targets[1]),
                  strands.animate.arrange(DOWN, buff=0.2).move_to(targets[2]), run_time=1.0)
        labs = VGroup(T("heads", 30, ORANGE).move_to([-3.4, -2.35, 0]),
                      T("tails", 30, GREY).move_to([0, -2.35, 0]),
                      T("DNA", 30, ORANGE).move_to([3.35, -2.35, 0]))
        self.play(FadeIn(labs), run_time=0.5)
        self.at("not split")
        split = chip("split from a parent", GREY, 28).move_to([0, 2.85, 0])
        strike = Line(split.get_left(), split.get_right(), color=RED, stroke_width=7)
        strike.layout_ok = True  # deliberate strike-through
        self.play(FadeIn(split), Create(strike), run_time=0.6)
        self.at("built from parts")
        rule = caption("BUILT FROM PARTS", 36, ORANGE)
        self.play(FadeOut(VGroup(split, strike)), FadeIn(rule, shift=UP * 0.12), run_time=0.7)
        self.finish()


class S06Lytic(SpokenScene):
    def construct(self):
        cell = rod(8.6, 4.8, [0, 0.15, 0], chromosome=False)
        parts = part_set([0, 0.3, 0], 1.2)
        self.add(cell, parts, schematic_tag())
        self.at("put together")
        complete = VGroup(*[phage(0.72) for _ in range(8)]).arrange_in_grid(2, 4, buff=0.42).move_to([0, 0.25, 0])
        self.play(ReplacementTransform(parts, complete), run_time=1.2)
        self.at("cell bursts")
        left_wall = ellipse_arc(8.6, 4.8, PI/2, PI-0.35, RED, 6, [0, 0.15, 0])
        right_wall = ellipse_arc(8.6, 4.8, -PI/2, PI-0.35, RED, 6, [0, 0.15, 0])
        self.play(FadeOut(cell.body), FadeIn(left_wall), FadeIn(right_wall), run_time=0.7)
        self.at("phages escape")
        exits = [[-5.3, 2.2, 0], [-4.7, 0.2, 0], [-5.2, -2.0, 0], [5.3, 2.1, 0],
                 [4.7, 0.3, 0], [5.25, -2.0, 0], [-1.4, 2.7, 0], [1.6, -2.55, 0]]
        self.play(*[p.animate.move_to(q) for p, q in zip(complete, exits)], run_time=1.1)
        self.at("host cell dies")
        dies = T("host cell dies", 34, RED, weight=BOLD).move_to([0, 0.2, 0])
        count = readout_box("new phages", "many", [4.65, 3.0, 0], ORANGE, 3.6)
        self.play(FadeIn(dies), FadeIn(count), left_wall.animate.set_stroke(GREY),
                  right_wall.animate.set_stroke(GREY), run_time=0.7)
        self.finish()


class S07LyticName(SpokenScene):
    def construct(self):
        cyc = lytic_cycle_diagram([0, -0.1, 0], 1.08)
        self.play(Create(cyc[0]), run_time=0.8)
        self.at("lytic cycle")
        title = T("LYTIC CYCLE", 42, ORANGE, weight=BOLD).move_to([0, 3.2, 0])
        self.play(FadeIn(title), run_time=0.5)
        self.at("takes over now")
        self.play(FadeIn(cyc[1][0]), FadeIn(cyc[2][0]), run_time=0.6)
        self.at("host builds")
        self.play(LaggedStart(FadeIn(cyc[1][1]), FadeIn(cyc[2][1]),
                              FadeIn(cyc[1][2]), FadeIn(cyc[2][2]), lag_ratio=0.18), run_time=1.0)
        self.at("cell bursts")
        self.play(FadeIn(cyc[1][3]), FadeIn(cyc[2][3]), run_time=0.6)
        self.add(schematic_tag())
        self.finish()


class S08Fork(SpokenScene):
    def construct(self):
        host = rod(6.1, 3.0, [-2.3, 0.25, 0])
        virus = phage(0.9, [-5.8, 0.8, 0]).rotate(-PI/2)
        self.at("second path")
        self.play(FadeIn(host), FadeIn(virus), run_time=0.7)
        self.at("phage lambda")
        lab = chip("lambda", ORANGE, 28).move_to([-5.45, 2.4, 0])
        self.play(FadeIn(lab), virus.animate.move_to([-4.95, 0.8, 0]), run_time=0.7)
        self.at("infects E")
        ecoli = T("E. coli", 30, CELL_GREEN).move_to([-2.3, -1.75, 0])
        strand = dna_strand(1.55, [-2.5, 1.0, 0])
        self.play(FadeIn(ecoli), Create(strand), run_time=0.7)
        self.at("does not have")
        fork = VGroup(Arrow([1.15, 0.3, 0], [3.0, 1.55, 0], color=ORANGE, stroke_width=5),
                      Arrow([1.15, 0.3, 0], [3.0, -1.15, 0], color=BLUE, stroke_width=5))
        labels = VGroup(chip("build now · lytic", ORANGE, 28).move_to([4.55, 1.65, 0]),
                        chip("carry along · lysogenic", BLUE, 28).move_to([4.6, -1.3, 0]))
        self.play(Create(fork), FadeIn(labels), run_time=0.9)
        self.play(Indicate(labels[1], color=YELLOW, scale_factor=1.05), run_time=0.5)
        self.add(schematic_tag())
        self.finish()


class S09Prophage(SpokenScene):
    def construct(self):
        host = rod(8.2, 4.4, [0, 0.05, 0])
        strand = dna_strand(2.0, [-3.2, 1.7, 0])
        self.add(host, strand, schematic_tag())
        self.play(host.body.animate.set_fill(CELL_GREEN, opacity=0.30), run_time=1.25)
        self.at("slips into")
        opening = ellipse_arc(3.95, 2.1, 0.45, TAU-0.9, BLUE, 7, [0, 0.05, 0])
        self.play(ReplacementTransform(host.chromosome, opening),
                  strand.animate.move_to([1.55, 0.35, 0]).scale(0.7), run_time=1.0)
        self.at("becomes part")
        joined = lysogenic_cell(8.2, 4.4, [0, 0.05, 0])
        self.play(ReplacementTransform(VGroup(host.body, opening, strand), joined), run_time=1.0)
        self.play(joined.body.animate.set_fill(CELL_GREEN, opacity=0.28), run_time=1.1)
        self.at("Stored viral")
        self.play(Indicate(joined.prophage, color=YELLOW, scale_factor=1.2), run_time=0.75)
        self.at("called a prophage")
        label = T("prophage", 36, ORANGE, weight=BOLD).move_to([2.7, 2.7, 0])
        pointer = Arrow(label.get_bottom(), [1.7, 0.85, 0], buff=0.15, color=ORANGE,
                        stroke_width=5, tip_length=0.2)
        self.play(FadeIn(label), GrowArrow(pointer), run_time=0.7)
        self.finish()


class S10Divide(SpokenScene):
    def construct(self):
        one = lysogenic_cell(6.2, 3.0, [0, 0, 0])
        count1 = readout_box("cells", "1", [4.9, 2.85, 0], TEXT, 2.5)
        self.add(one, count1, schematic_tag())
        self.play(one.animate.scale(1.03), run_time=0.8)
        self.at("keeps dividing")
        self.play(one.animate.stretch(1.32, 0), run_time=0.8)
        self.at("copies its chromosome")
        copy_loop = one.chromosome.copy().shift(UP * 0.65)
        copy_seg = one.prophage.copy().shift(UP * 0.65)
        self.play(one.chromosome.animate.shift(DOWN * 0.65), one.prophage.animate.shift(DOWN * 0.65),
                  TransformFromCopy(one.chromosome, copy_loop), TransformFromCopy(one.prophage, copy_seg), run_time=1.0)
        self.at("Both new cells")
        daughters = VGroup(lysogenic_cell(5.0, 2.5, [-2.75, 0, 0]),
                           lysogenic_cell(5.0, 2.5, [2.75, 0, 0]))
        count2 = readout_box("cells", "2", [4.9, 2.85, 0], TEXT, 2.5)
        self.play(ReplacementTransform(VGroup(one, copy_loop, copy_seg), daughters),
                  ReplacementTransform(count1, count2), run_time=1.0)
        self.play(Indicate(daughters[0].prophage, color=YELLOW),
                  Indicate(daughters[1].prophage, color=YELLOW), run_time=0.7)
        self.finish()


class S11Counter(SpokenScene):
    def construct(self):
        cells = VGroup(lysogenic_cell(4.2, 1.8, [0, 0, 0]))
        cbox = readout_box("cells", "1", [4.9, 3.4, 0], TEXT, 2.7)
        pbox = readout_box("new phages", "0", [4.65, 2.55, 0], TEXT, 3.25)
        self.add(cells, cbox, pbox, schematic_tag())
        self.at("1 cell")
        layouts = [
            VGroup(*[lysogenic_cell(3.5, 1.55, [x, 0, 0]) for x in (-2.0, 2.0)]),
            VGroup(*[lysogenic_cell(2.7, 1.25, [x, y, 0]) for x in (-3.0, 0, 3.0) for y in (-0.85, 0.85)])[:4],
            mini_family(2, 4, [0, -0.15, 0], 2.45, 1.05),
            mini_family(4, 4, [0, -0.4, 0], 2.25, 0.9, 1.2),
        ]
        values = ["2", "4", "8", "16"]
        cues = ["2", "4", "8", "16"]
        for layout, val, cue in zip(layouts, values, cues):
            self.at(cue)
            newbox = readout_box("cells", val, [4.9, 3.4, 0], TEXT, 2.7)
            self.play(ReplacementTransform(cells, layout), ReplacementTransform(cbox, newbox), run_time=0.5)
            cells, cbox = layout, newbox
        self.at("carrying the orange")
        self.play(LaggedStart(*[Indicate(c.prophage, color=YELLOW, scale_factor=1.15)
                                for c in cells], lag_ratio=0.03), run_time=1.0)
        self.finish()


class S12Zero(SpokenScene):
    def construct(self):
        family = mini_family(4, 4, [0, -0.4, 0], 2.25, 0.9, 1.2)
        cells = readout_box("cells", "16", [4.9, 3.4, 0], TEXT, 2.8)
        phages = readout_box("new phages", "0", [4.65, 2.55, 0], TEXT, 3.3)
        self.add(family, cells, phages, schematic_tag())
        self.at("look at the second")
        halo = SurroundingRectangle(phages, color=YELLOW, buff=0.12, stroke_width=6)
        self.play(Create(halo), run_time=0.6)
        self.at("New phages")
        self.play(Indicate(phages, color=YELLOW, scale_factor=1.08), run_time=0.7)
        self.at("viral")
        self.play(FadeOut(halo), LaggedStart(*[Indicate(c.prophage, color=ORANGE, scale_factor=1.12)
                                               for c in family], lag_ratio=0.025), run_time=1.2)
        self.at("host's doubling")
        dna_count = readout_box("viral DNA copies", "16", [-4.3, 3.4, 0], ORANGE, 4.0)
        self.play(FadeIn(dna_count), Indicate(cells, color=YELLOW), run_time=0.7)
        self.at("lysogenic cycle")
        rule = caption("LYSOGENIC CYCLE · COPIED WITH THE HOST", 32, BLUE)
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S13Switch(SpokenScene):
    def construct(self):
        family = mini_family(2, 4, [0, -0.25, 0], 2.65, 1.15)
        self.add(family, schematic_tag())
        generations = T("many generations", 34, BLUE).move_to([0, 3.15, 0])
        self.at("many generations")
        self.play(FadeIn(generations), family.animate.shift(RIGHT * 0.08), run_time=0.7)
        struck = family[2]
        self.at("damage to the")
        bolt = Polygon([-1.0, 1.0, 0], [-0.35, 0.65, 0], [-0.62, 0.05, 0],
                       [0.25, 0.45, 0], [-0.25, -0.65, 0], color=YELLOW,
                       fill_color=YELLOW, fill_opacity=0.8).scale(0.75).move_to(struck)
        damage = chip("DNA damage", YELLOW, 28).move_to([-3.9, 2.45, 0])
        self.play(FadeIn(bolt), FadeIn(damage), struck.body.animate.set_stroke(YELLOW), run_time=0.7)
        self.at("switch it into")
        loose = dna_strand(1.25, struck.get_center() + UP * 0.65)
        fork = chip("BUILD NOW · LYTIC", ORANGE, 30).move_to([3.8, 2.55, 0])
        self.play(ReplacementTransform(struck.prophage, loose), FadeIn(fork), FadeOut(generations), run_time=0.8)
        self.play(loose.animate.shift(UP * 0.45), Indicate(fork, color=YELLOW), run_time=0.6)
        self.finish()


class S14Burst(SpokenScene):
    def construct(self):
        family = mini_family(2, 4, [0, -0.25, 0], 2.65, 1.15)
        target = family[2]
        zero = readout_box("new phages", "0", [4.65, 3.0, 0], TEXT, 3.3)
        self.add(family, schematic_tag(), zero)
        self.at("host now builds")
        parts = part_set(target.get_center(), 0.28)
        self.play(FadeOut(VGroup(target.chromosome, target.prophage)), FadeIn(parts), run_time=0.8)
        assembled = VGroup(*[phage(0.3) for _ in range(4)]).arrange_in_grid(2, 2, buff=0.12).move_to(target)
        self.play(ReplacementTransform(parts, assembled), run_time=0.7)
        self.at("cell bursts")
        dead = VGroup(Line(target.get_center()+UL*0.55, target.get_center()+DR*0.55, color=RED, stroke_width=7),
                      Line(target.get_center()+DL*0.55, target.get_center()+UR*0.55, color=RED, stroke_width=7))
        self.play(FadeOut(target.body), FadeIn(dead),
                  *[p.animate.shift(d) for p, d in zip(assembled, (UL, UR, DL, DR))], run_time=0.8)
        many = readout_box("new phages", "many", [4.65, 3.0, 0], ORANGE, 3.7)
        self.play(ReplacementTransform(zero, many), run_time=0.5)
        self.at("other cells carry")
        survivors = VGroup(*[c for i, c in enumerate(family) if i != 2])
        bob(survivors, amp=0.035, speed=1.7)
        carry = caption("the other cells carry on · prophage and all", 30, BLUE)
        self.play(FadeIn(carry), Indicate(survivors, color=BLUE, scale_factor=1.02), run_time=0.8)
        self.finish()


class S15Close(SpokenScene):
    def construct(self):
        panels = TwoPanel("LYTIC", "LYSOGENIC", colors=(ORANGE, BLUE), top=3.35, bottom=-2.5)
        self.at("two paths")
        self.play(FadeIn(panels), run_time=0.7)
        cycle = lytic_cycle_diagram([-3.25, -0.05, 0], 0.62)
        cycle_picture = VGroup(cycle[0], cycle[1])
        family_start = VGroup(lysogenic_cell(2.15, 0.95, [2.0, -0.1, 0]),
                              lysogenic_cell(2.15, 0.95, [4.45, -0.1, 0]))
        family = mini_family(2, 2, [3.25, -0.1, 0], 2.15, 0.95)
        self.at("builds new phages now")
        left_rule = T("builds phages now", 30, ORANGE).move_to([-3.25, -2.05, 0])
        self.play(FadeIn(cycle_picture), FadeIn(left_rule), run_time=1.0)
        self.at("copies only")
        right_rule = T("copies phage DNA only", 30, BLUE).move_to([3.25, -2.05, 0])
        zero = readout_box("new phages", "0", [3.25, 2.15, 0], TEXT, 3.2)
        self.play(FadeIn(family_start), FadeIn(right_rule), FadeIn(zero), run_time=1.0)
        self.at("many generations")
        self.play(ReplacementTransform(family_start, family), run_time=1.0)
        self.play(LaggedStart(*[Indicate(c.prophage, color=ORANGE) for c in family], lag_ratio=0.12), run_time=0.8)
        self.at("only if it switches")
        traveler = family[0].copy()
        self.add(traveler)
        switch = DashedLine([2.2, -2.55, 0], [-2.15, -2.55, 0], color=YELLOW,
                            stroke_width=5, dash_length=0.18)
        tip = Triangle(color=YELLOW, fill_color=YELLOW, fill_opacity=1).scale(0.12).rotate(PI/2)
        tip.move_to(switch.get_end())
        switch_lab = T("only if it switches", 28, YELLOW).next_to(switch, DOWN, buff=0.08)
        self.play(Create(switch), FadeIn(tip), FadeIn(switch_lab),
                  traveler.animate.move_to([-3.25, -0.1, 0]).set_stroke(ORANGE),
                  run_time=1.4)
        self.play(FadeOut(traveler), run_time=0.35)
        self.at("may never happen")
        maybe = T("may never happen", 28, GREY).move_to([3.25, -3.25, 0])
        self.play(FadeIn(maybe), run_time=0.6)
        self.add(schematic_tag())
        self.finish()


class S16Takehome(SpokenScene):
    def construct(self):
        host = rod(9.0, 5.1, [0, 0.2, 0], chromosome=False)
        virus = phage(1.35, [0, 0.5, 0])
        self.play(FadeIn(host), FadeIn(virus, scale=0.8), run_time=0.8)
        self.at("rule to keep")
        heading = T("THE RULE TO KEEP", 34, GOLD, weight=BOLD).move_to([0, 3.25, 0])
        self.play(FadeIn(heading), run_time=0.5)
        self.at("virus never builds itself")
        no_self = VGroup(Line([-1.05, 1.45, 0], [1.05, -0.45, 0], color=RED, stroke_width=8),
                         Line([-1.05, -0.45, 0], [1.05, 1.45, 0], color=RED, stroke_width=8))
        parts = part_set([0, 0.25, 0], 1.0)
        self.play(Create(no_self), host.body.animate.set_fill(CELL_GREEN, opacity=0.32),
                  run_time=1.8)
        self.play(FadeOut(no_self), ReplacementTransform(virus, parts), run_time=0.7)
        self.at("host cell builds")
        rebuilt = VGroup(*[phage(0.62) for _ in range(6)]).arrange_in_grid(2, 3, buff=0.45).move_to([0, 0.25, 0])
        self.play(ReplacementTransform(parts, rebuilt), host.body.animate.set_fill(CELL_GREEN, opacity=0.18),
                  run_time=1.0)
        self.at("only on the lytic")
        rule = caption("A HOST BUILDS NEW PHAGES ONLY ON THE LYTIC PATH", 34, ORANGE)
        self.play(FadeIn(rule, shift=UP * 0.12), run_time=0.7)
        self.add(schematic_tag())
        self.finish()


class S17End(EndCard):
    LINE = "In lambda, a host builds new phages only on the lytic path."
