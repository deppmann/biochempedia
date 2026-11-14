"""How DNA Became Readable (Biochemistrypedia explainer, chapter 2).

COLOR MAP (kept from chapter 1)
  BLUE   = DNA base blocks and sequence strips
  GREY   = backbones, outlines, lanes and structure
  YELLOW = the question lens and differences
  GREEN  = features a model shows / correct order
  ORANGE = features omitted, covers and chain-stopping blocks
  PURPLE = evidence, copying machinery and project contributions
  GOLD   = title rule only

All DNA pictures are labelled blocks, bars, lanes and rulers. No molecular structure is drawn.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
BASES = "ATGCCGTAACGT"


def diagram_field():
    """Shared chapter-one diagram ground; decorative, behind every teaching object."""
    field = RoundedRectangle(corner_radius=0.28, width=13.0, height=6.75,
                             stroke_color=GREY, stroke_width=2,
                             fill_color=GREY, fill_opacity=0.20)
    field.set_z_index(-20)
    field.layout_ok = True
    return field


def scan_band(width, height, color, start, axis="x", span=10.0, seconds=8.0):
    """A slow diagram highlight used where the narrated process continues running."""
    band = Rectangle(width=width, height=height, stroke_width=0,
                     fill_color=color, fill_opacity=0.36).move_to(start)
    band.set_z_index(-5)
    band.layout_ok = True
    band._clock = 0.0
    origin = np.array(start, dtype=float)
    def drift(mob, dt):
        mob._clock = (mob._clock + dt / seconds) % 1.0
        offset = (mob._clock - 0.5) * span
        mob.move_to(origin + (RIGHT if axis == "x" else DOWN) * offset)
    band.add_updater(drift)
    return band


class FilmScene(SpokenScene):
    def setup(self):
        super().setup()
        self.add(diagram_field())


def base_block(letter="", w=0.66, h=0.58, size=28, color=BLUE):
    """The shared base tile. Text deliberately sits inside its own labelled block."""
    box = RoundedRectangle(corner_radius=0.09, width=w, height=h, stroke_color=color,
                           stroke_width=3, fill_color=color, fill_opacity=0.22)
    if not letter:
        return VGroup(box)
    label = T(letter, size, TEXT, weight=BOLD).move_to(box)
    label.layout_ok = True
    return VGroup(box, label)


def labelled_box(text, color=GREY, width=2.3, height=0.72, size=28, fill=0.12):
    box = RoundedRectangle(corner_radius=0.14, width=width, height=height,
                           stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=fill)
    label = fit_text(text, max_w=width - 0.3, size=size, color=color, max_lines=2).move_to(box)
    label.layout_ok = True
    return VGroup(box, label)


def strip(n, end="", color=BLUE, block_w=0.42, block_h=0.34, gap=0.025):
    blocks = VGroup(*[base_block("", w=block_w, h=block_h, color=color) for _ in range(n)])
    blocks.arrange(RIGHT, buff=gap)
    if end:
        cap = base_block(end, w=block_w, h=block_h, size=22, color=ORANGE)
        blocks.add(cap)
        blocks.arrange(RIGHT, buff=gap)
    return blocks


def letter_strip(text=BASES, block_w=0.72, block_h=0.62, size=28, color=BLUE):
    g = VGroup(*[base_block(ch, w=block_w, h=block_h, size=size, color=color) for ch in text])
    return g.arrange(RIGHT, buff=0.055)


def model_tag(text, color, size=26):
    return labelled_box(text, color=color, width=max(2.0, 0.16 * len(text) + 0.65),
                        height=0.62, size=size)


def question_world(focus="shape", comparison=False):
    """The carried chapter-one world, rebuilt at fixed coordinates."""
    sample = labelled_box("DNA sample", PURPLE, width=2.1, height=1.0, size=26).move_to([-5.8, 0.0, 0])
    q = T("Which view answers the question?", 34, YELLOW, weight=BOLD).move_to([0.8, 3.25, 0])
    names = ["pairing", "shape", "order", "occupied space"]
    if comparison:
        names = ["shape", "order", "comparison"]
        positions = [(-2.8, 0.45), (0.65, 0.45), (4.1, 0.45)]
    else:
        positions = [(-2.5, 1.25), (2.2, 1.25), (-2.5, -1.55), (2.2, -1.55)]
    frames = VGroup()
    for name, (x, y) in zip(names, positions):
        frame = RoundedRectangle(corner_radius=0.18, width=4.15 if not comparison else 3.1,
                                 height=2.15, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.065).move_to([x, y, 0])
        lab = T(name, 28, GREY, weight=BOLD).move_to(frame.get_top() + DOWN * 0.34)
        frames.add(VGroup(frame, lab))
    target_names = names
    idx = target_names.index(focus) if focus in target_names else 0
    lens = SurroundingRectangle(frames[idx][0], color=YELLOW, stroke_width=7, buff=0.08,
                                corner_radius=0.22)
    schem = scope_tag("schematic")
    return VGroup(sample, q, frames, lens, schem), sample, frames, lens


def order_contents(frame, bright=True):
    g = letter_strip("ATGCC", block_w=0.52, block_h=0.5, size=24)
    g.move_to(frame.get_center() + DOWN * 0.18)
    if not bright:
        g.set_opacity(0.25)
    return g


def shape_contents(frame):
    card = RoundedRectangle(corner_radius=0.2, width=2.35, height=0.85,
                            stroke_color=GREY, stroke_width=5,
                            fill_color=GREY, fill_opacity=0.16)
    card.move_to(frame.get_center() + DOWN * 0.18)
    return card


def copying_world(copy_count=0):
    template = VGroup(*[base_block("?", w=0.69, h=0.58, size=27) for _ in range(14)])
    template.arrange(RIGHT, buff=0.06).move_to([0, 1.15, 0])
    rail = Line([-5.75, 1.64, 0], [5.75, 1.64, 0], color=GREY, stroke_width=7)
    lab = T("template", 30, GREY, weight=BOLD).move_to([-5.0, 2.3, 0])
    copy = VGroup(*[base_block("", w=0.69, h=0.58) for _ in range(copy_count)])
    if copy_count:
        copy.arrange(RIGHT, buff=0.06).move_to(template[:copy_count]).shift(DOWN * 1.5)
    enzyme = labelled_box("copying enzyme", PURPLE, width=2.55, height=0.82, size=28, fill=0.22)
    ex = template[max(0, min(copy_count, 13))].get_x()
    enzyme.move_to([ex, 0.35, 0])
    cover = labelled_box("readout covered", ORANGE, width=2.5, height=0.72, size=25, fill=0.32)
    cover.move_to([4.75, -2.3, 0])
    return VGroup(rail, template, lab, copy, enzyme, cover, scope_tag("schematic")), template, copy, enzyme, cover


def reaction_trays(with_mixture=True):
    trays = VGroup()
    for j, letter in enumerate("ATGC"):
        x = -4.8 + j * 3.2
        frame = RoundedRectangle(corner_radius=0.18, width=2.7, height=5.25,
                                 stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.11).move_to([x, -0.05, 0])
        lab = T(letter, 36, BLUE, weight=BOLD).move_to([x, 2.9, 0])
        contents = VGroup()
        if with_mixture:
            for k, n in enumerate((3 + (j % 2), 6 - (j % 2), 4 + ((j + 1) % 3))):
                s = strip(n, letter, block_w=0.25, block_h=0.25)
                s.move_to([x + (-0.12, 0.13, -0.08)[k], 1.25 - 1.22 * k, 0])
                contents.add(s)
        trays.add(VGroup(frame, lab, contents))
    return trays


def sorting_world(include_pair=False):
    lanes = VGroup()
    entrance = VGroup()
    for j, letter in enumerate("ATGC"):
        x = -4.65 + j * 3.1
        lane = RoundedRectangle(corner_radius=0.12, width=2.45, height=5.45,
                                stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.10).move_to([x, -0.05, 0])
        lab = T(letter, 32, BLUE, weight=BOLD).move_to([x, 3.08, 0])
        lanes.add(VGroup(lane, lab))
        for k, n in enumerate((3 + j % 2, 5 + (j + 1) % 2)):
            s = strip(n, letter, block_w=0.22, block_h=0.22)
            s.move_to([x + (-0.32 if k == 0 else 0.32), 2.1 - 0.38 * k, 0])
            entrance.add(s)
    pair = VGroup()
    if include_pair:
        short = strip(3, "A", block_w=0.31, block_h=0.3).move_to([-1.3, 2.1, 0])
        long = strip(8, "A", block_w=0.31, block_h=0.3).move_to([1.45, 2.1, 0])
        pair = VGroup(short, long)
    return VGroup(lanes, entrance, pair, scope_tag("schematic")), lanes, entrance, pair


def reference_world(rows=3):
    ref = letter_strip(BASES, block_w=0.7, block_h=0.62, size=27).move_to([0, 1.65, 0])
    ruler = VGroup(ref, T("reference sequence", 32, BLUE, weight=BOLD).next_to(ref, UP, buff=0.3))
    seqs = VGroup()
    variants = [BASES[1:10], "TGCCGGTAAC", "GCCGTAACGT"]
    for i, text in enumerate(variants[:rows]):
        s = letter_strip(text, block_w=0.58, block_h=0.5, size=23)
        s.move_to([-0.3 + i * 0.25, 0.45 - i * 0.9, 0])
        seqs.add(s)
    tag = model_tag("comparison standard", GREEN, 27).move_to([0, -2.75, 0])
    return VGroup(ruler, seqs, tag, scope_tag("schematic")), ruler, seqs, tag


COST_DATA = [
    (2001.75, 95263072), (2003.83, 40157554), (2007.83, 7147571),
    (2008.00, 3063820), (2010.00, 46774), (2012.25, 5901),
    (2015.50, 1363), (2019.33, 606), (2021.58, 562), (2022.33, 525),
]


def cost_plot(box=(-5.85, 5.75, -2.35, 2.35)):
    p = Plot(box=box, xr=(2001.75, 2022.33), yr=(2.0, 8.15),
             xticks=[(2001.75, "2001"), (2022.33, "2022")], yticks=[],
             xlabel="year", ylabel="estimated production cost, log scale", label_size=28)
    pts = [p.pt(year, np.log10(cost)) for year, cost in COST_DATA]
    curve = VMobject(stroke_color=BLUE, stroke_width=7, fill_opacity=0).set_points_as_corners(pts)
    floor = p.pt(2001.75, 2.0)
    floor_r = p.pt(2022.33, 2.0)
    area = Polygon(floor, *pts, floor_r, stroke_width=0, fill_color=BLUE, fill_opacity=0.10)
    return p, curve, pts, area


class S00LinkHook(FilmScene):
    def construct(self):
        world, sample, frames, lens = question_world("shape")
        shape = shape_contents(frames[1][0])
        order = order_contents(frames[2][0], bright=False)
        self.add(world, shape, order)
        self.at("double helix revealed")
        self.play(Indicate(shape, color=GREEN, scale_factor=1.05), run_time=1.0)
        mask = RoundedRectangle(corner_radius=0.2, width=shape.width + 0.35, height=shape.height + 0.25,
                                stroke_width=0, fill_color=ORANGE, fill_opacity=0.30).move_to(shape)
        self.at("how can scientists read")
        self.play(FadeIn(mask), order.animate.set_opacity(1.0), run_time=1.2)
        new_lens = SurroundingRectangle(frames[2][0], color=YELLOW, stroke_width=7, buff=0.08,
                                        corner_radius=0.22)
        self.at("yellow lens to order")
        self.play(ReplacementTransform(lens, new_lens), run_time=1.3)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Discovering DNA structure"
    TITLE = "How DNA Became Readable"


class S02Copying(FilmScene):
    def construct(self):
        world, template, copy, enzyme, cover = copying_world(0)
        self.add(scan_band(0.62, 3.6, PURPLE, [0, 0.15, 0], span=11.5, seconds=7.0))
        self.at("Start with one template")
        self.play(FadeIn(VGroup(world[0], template, world[2])), run_time=0.8)
        self.at("copying enzyme moves")
        self.play(FadeIn(enzyme, shift=RIGHT * 0.2), run_time=0.5)
        copies = VGroup(*[base_block("", w=0.69, h=0.58).move_to(b).shift(DOWN * 1.5) for b in template[:11]])
        self.at("adding matching base blocks")
        self.play(enzyme.animate.move_to([3.65, 0.35, 0]),
                  LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in copies], lag_ratio=0.09),
                  run_time=2.2, rate_func=linear)
        self.at("Ordinary blocks")
        extra = VGroup(*[base_block("", w=0.69, h=0.58).move_to(b).shift(DOWN * 1.5) for b in template[11:]])
        self.play(enzyme.animate.move_to([5.15, 0.35, 0]),
                  LaggedStart(*[FadeIn(b) for b in extra], lag_ratio=0.16), run_time=1.2)
        self.at("letters are still hidden")
        self.play(FadeIn(cover, shift=LEFT * 0.15), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S03StopBlocks(FilmScene):
    def construct(self):
        trays = reaction_trays(False)
        self.add(scan_band(0.65, 5.3, PURPLE, [0, -0.05, 0], span=12.2, seconds=7.5))
        self.at("original method ran")
        self.play(LaggedStart(*[FadeIn(VGroup(t[0], t[1]), shift=UP * 0.15) for t in trays], lag_ratio=0.12), run_time=1.2)
        for tray in trays:
            pulse(tray[0], base=3.0, amp=0.8, speed=1.4)
        ordinary = base_block("", w=0.5, h=0.45).move_to([-5.65, 3.6, 0])
        stop = base_block("A", w=0.5, h=0.45, size=23, color=ORANGE).move_to([5.65, 3.6, 0])
        mixlab = T("mostly ordinary   +   a few stop blocks", 28, TEXT).move_to([0, 3.6, 0])
        self.at("mixed ordinary blocks")
        self.play(FadeIn(mixlab), FadeIn(ordinary), FadeIn(stop), run_time=0.8)
        built = VGroup()
        for j, tray in enumerate(trays):
            for k, n in enumerate((3 + j % 2, 6 - j % 2, 4 + (j + 1) % 3)):
                s = strip(n, "ATGC"[j], block_w=0.25, block_h=0.25)
                s.move_to([tray[0].get_x() + (-0.12, 0.13, -0.08)[k], 1.25 - 1.22 * k, 0])
                built.add(s)
        self.at("stop block joins")
        self.play(LaggedStart(*[GrowFromEdge(s, LEFT) for s in built], lag_ratio=0.05), run_time=2.0)
        self.at("cannot grow farther")
        self.play(Indicate(VGroup(*[s[-1] for s in built]), color=ORANGE, scale_factor=1.12), run_time=0.9)
        self.at("Many copies grow")
        self.play(LaggedStart(*[s.animate.shift(DOWN * 0.16).shift(UP * 0.16) for s in built], lag_ratio=0.04), run_time=1.7)
        self.at("different matching positions")
        self.play(LaggedStart(*[Indicate(s, color=BLUE, scale_factor=1.03) for s in built], lag_ratio=0.04), run_time=1.5)
        inset = RoundedRectangle(corner_radius=0.16, width=5.0, height=1.35, stroke_color=PURPLE,
                                 stroke_width=3, fill_color=BG, fill_opacity=0.95).move_to([0, -2.65, 0])
        ilab = T("later versions: one reaction", 25, PURPLE).move_to([0, -2.25, 0])
        colors = [BLUE, GREEN, YELLOW, PURPLE]
        stops = VGroup(*[base_block(ch, w=0.48, h=0.42, size=22, color=c)
                         for ch, c in zip("ATGC", colors)]).arrange(RIGHT, buff=0.18).move_to([0, -2.85, 0])
        for b in stops:
            b[1].layout_ok = True
        self.at("Later versions")
        self.play(FadeOut(VGroup(mixlab, ordinary, stop)), FadeIn(inset), FadeIn(ilab),
                  LaggedStart(*[FadeIn(b, scale=0.8) for b in stops], lag_ratio=0.15), run_time=1.4)
        self.add(scope_tag("schematic"))
        self.finish()


class S04Mixture(FilmScene):
    def construct(self):
        trays = reaction_trays(True)
        self.add(trays, scope_tag("schematic"))
        self.at("holds a mixture")
        self.play(*[t[2].animate.shift(RIGHT * (0.08 if i % 2 else -0.08)) for i, t in enumerate(trays)],
                  run_time=0.45, rate_func=there_and_back)
        self.play(*[t[2].animate.shift(UP * 0.08) for t in trays], run_time=0.45, rate_func=there_and_back)
        self.at("Each copy ends")
        caps = VGroup(*[s[-1] for t in trays for s in t[2]])
        self.play(Indicate(caps, color=ORANGE, scale_factor=1.1), run_time=0.9)
        lanes_world, lanes, entrance, pair = sorting_world(False)
        self.at("Sorting lanes")
        self.play(ReplacementTransform(trays, VGroup(lanes, entrance)), run_time=1.7)
        cover = labelled_box("readout covered", ORANGE, width=2.4, height=0.65, size=24, fill=0.3)
        cover.move_to([0, -3.35, 0])
        self.play(FadeIn(cover, shift=UP * 0.1), run_time=0.6)
        bob(entrance, amp=0.035, speed=2.0)
        self.finish()


def predict_backdrop(include_field=True):
    world, lanes, entrance, pair = sorting_world(True)
    qmark = T("?", 60, YELLOW, weight=BOLD).move_to([0, 1.1, 0])
    for lane in lanes:
        pulse(lane[0], base=3.0, amp=1.0, speed=1.3)
    bob(qmark, amp=0.08, speed=1.5)
    shimmer = scan_band(12.2, 0.48, BLUE, [0, 0, 0], axis="y", span=5.2, seconds=5.5)
    items = [diagram_field()] if include_field else []
    return VGroup(*items, shimmer, lanes, entrance, pair, qmark), qmark


class S05Predict(FilmScene):
    def construct(self):
        back, qmark = predict_backdrop(False)
        self.add(*back[:-1])
        self.at("Predict before")
        self.play(FadeIn(back[1], scale=0.8), run_time=0.6)
        self.at("Which copy reaches")
        q = question_card("Which reaches the bottom first?", y=-3.15, size=30)
        self.play(FadeIn(q.question), run_time=1.0)
        self.at("Hold the picture")
        self.play(Indicate(qmark, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Which reaches the bottom first?"
    OPTIONS = []
    SECONDS = 4.5
    CARD = {"y": -3.15, "size": 30, "chip_size": 26}

    def backdrop(self):
        return predict_backdrop()[0]


class S07Reveal(FilmScene):
    def construct(self):
        world, lanes, entrance, pair = sorting_world(False)
        shimmer = scan_band(12.2, 0.48, BLUE, [0, 0, 0], axis="y", span=5.2, seconds=5.5)
        self.add(shimmer, lanes)
        moving = VGroup()
        lengths = [3, 5, 4, 6, 5, 7, 6, 8]
        for i, (letter, n) in enumerate(zip("ATGCATGC", lengths)):
            lane_i = i // 2
            x = -4.65 + lane_i * 3.1 + (-0.3 if i % 2 == 0 else 0.3)
            s = strip(n, letter, block_w=0.22, block_h=0.22).move_to([x, 2.05 - 0.35 * (i % 2), 0])
            moving.add(s)
        self.add(moving)
        self.at("copies start moving together")
        animations = []
        for s, n in zip(moving, lengths):
            target_y = -2.35 + 0.31 * (n - min(lengths))
            animations.append(s.animate.move_to([s.get_x(), target_y, 0]))
        self.play(*animations, run_time=3.2, rate_func=linear)
        shortest = moving[lengths.index(min(lengths))]
        self.at("shortest reaches")
        self.play(Indicate(shortest, color=GREEN, scale_factor=1.12), run_time=0.7)
        ordered = sorted(range(len(lengths)), key=lambda i: lengths[i])
        self.at("longer copies follow")
        self.play(LaggedStart(*[Indicate(moving[i], color=GREEN, scale_factor=1.05)
                                for i in ordered[1:]], lag_ratio=0.12), run_time=1.5)
        cover = Rectangle(width=11.4, height=1.15, stroke_color=ORANGE, stroke_width=3,
                          fill_color=BG, fill_opacity=1).move_to([0, -2.85, 0])
        self.add(cover)
        letters = letter_strip("ATGCCGTA", block_w=0.62, block_h=0.54, size=25).move_to([0, -2.85, 0])
        self.at("Reading each stop base")
        self.play(FadeOut(lanes), cover.animate.shift(DOWN * 1.25),
                  LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in letters], lag_ratio=0.1), run_time=2.3)
        checks = VGroup(*[T("✓", 26, GREEN, weight=BOLD).next_to(b, UP, buff=0.08) for b in letters])
        self.at("one position after another")
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in checks], lag_ratio=0.1), run_time=1.2)
        self.finish()


class S08SequenceModel(FilmScene):
    def construct(self):
        letters = letter_strip(BASES, block_w=0.72, block_h=0.62, size=27).move_to([0, 0.7, 0])
        shape = labelled_box("coiled shape", GREY, width=3.2, height=1.15, size=32).move_to([-4.5, 2.65, 0])
        self.at("Sequencing changes")
        self.play(FadeIn(shape, shift=DOWN * 0.15), run_time=0.6)
        self.at("becomes a letter string")
        self.play(ReplacementTransform(shape, letters), run_time=1.5)
        shows = VGroup(model_tag("identity", GREEN, 28), model_tag("order", GREEN, 28)).arrange(RIGHT, buff=0.35)
        shows.move_to([0, -0.5, 0])
        self.at("shows identity and order")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in shows], lag_ratio=0.2), run_time=1.0)
        hidden = VGroup(*[T(x, 28, ORANGE) for x in ("shape", "size", "partner strand")]).arrange(RIGHT, buff=0.65)
        hidden.move_to([0, -2.0, 0])
        curtain = Rectangle(width=hidden.width + 0.5, height=0.85, stroke_color=ORANGE, stroke_width=3,
                            fill_color=ORANGE, fill_opacity=0.28).move_to(hidden)
        self.at("while hiding")
        self.play(FadeIn(hidden), run_time=0.6)
        self.play(FadeIn(curtain, shift=DOWN * 0.15), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S09Reference(FilmScene):
    def construct(self):
        genome = labelled_box("one chromosome set", PURPLE, width=4.2, height=1.15, size=32).move_to([0, 0.5, 0])
        self.at("genome is all")
        self.play(FadeIn(genome, shift=UP * 0.15), run_time=0.8)
        world, ruler, seqs, standard = reference_world(3)
        self.at("reference sequence acts")
        self.play(ReplacementTransform(genome, ruler), run_time=1.3)
        self.at("New sequence strips")
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.4) for s in seqs], lag_ratio=0.22), run_time=1.7)
        matches = VGroup()
        diffs = VGroup()
        for i, s in enumerate(seqs):
            if len(s):
                matches.add(SurroundingRectangle(s[min(2, len(s)-1)], color=GREEN, stroke_width=4, buff=0.02))
                diffs.add(SurroundingRectangle(s[min(5, len(s)-1)], color=YELLOW, stroke_width=4, buff=0.02))
        self.at("differences easier")
        self.play(FadeIn(matches), FadeIn(diffs), FadeIn(standard, shift=UP * 0.1), run_time=1.1)
        self.add(scope_tag("schematic"))
        self.finish()


class S10Project(FilmScene):
    def construct(self):
        ref_box = RoundedRectangle(corner_radius=0.12, width=11.6, height=1.0,
                                   stroke_color=BLUE, stroke_width=4,
                                   fill_color=BLUE, fill_opacity=0.08).move_to([0, 1.45, 0])
        title = T("human reference", 32, BLUE, weight=BOLD).move_to([0, 2.3, 0])
        donors = VGroup()
        self.add(scan_band(0.65, 5.0, GREEN, [0, 0.0, 0], span=11.0, seconds=7.0))
        widths = [4.0, 2.2, 2.0, 1.7]
        x = -5.45
        for w in widths:
            seg = labelled_box("donor", PURPLE, width=w, height=0.72, size=24, fill=0.2)
            seg.move_to([x + w / 2, 1.45, 0])
            donors.add(seg)
            x += w + 0.35
        self.at("Human Genome Project")
        self.play(FadeIn(title), Create(ref_box), run_time=0.8)
        self.at("build a human reference")
        self.play(LaggedStart(*[FadeIn(d, shift=RIGHT * 0.25) for d in donors], lag_ratio=0.18), run_time=1.6)
        gaps = VGroup(*[Rectangle(width=0.25, height=0.8, stroke_width=0, fill_color=BG, fill_opacity=1)
                        .move_to([d.get_right()[0] + 0.17, 1.45, 0]) for d in donors[:-1]])
        self.at("several donors")
        self.play(LaggedStart(*[Indicate(d, color=PURPLE, scale_factor=1.03) for d in donors], lag_ratio=0.14), run_time=1.1)
        self.at("still left gaps")
        self.play(FadeIn(gaps), run_time=0.7)
        axis = Line([-5.6, -1.3, 0], [5.6, -1.3, 0], color=GREY, stroke_width=5)
        dates = [("1990", -5.2), ("2003", -1.8), ("2022", 2.3), ("2023", 5.2)]
        ticks = VGroup(*[VGroup(Line([x, -1.48, 0], [x, -1.12, 0], color=GREY, stroke_width=4),
                                T(year, 26, GREY).move_to([x, -1.8, 0])) for year, x in dates])
        bridges = VGroup(*[Rectangle(width=0.38, height=0.68, stroke_color=GREEN, stroke_width=3,
                                     fill_color=GREEN, fill_opacity=0.28).move_to(g) for g in gaps])
        varied = VGroup(*[strip(8 + i, "", block_w=0.28, block_h=0.25).move_to([0.25 * i, -2.55 - 0.35 * i, 0])
                          for i in range(3)])
        self.at("Later projects")
        self.play(Create(axis), FadeIn(ticks), FadeIn(bridges), run_time=1.2)
        self.at("added variation")
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.25) for s in varied], lag_ratio=0.18), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S11CostCurve(FilmScene):
    def construct(self):
        ref = letter_strip(BASES, block_w=0.72, block_h=0.58, size=26).move_to([0, -2.35, 0])
        self.at("became far less costly")
        self.play(FadeIn(ref, shift=UP * 0.15), run_time=0.7)
        p, curve, pts, area = cost_plot()
        self.at("production cost estimates")
        self.play(ReplacementTransform(ref, p.axes[0]), FadeIn(VGroup(p.axes[1], p.ticks, p.tick_labels,
                                                                      p.xlabel, p.ylabel)), run_time=1.4)
        self.at("logarithmic scale")
        dots = VGroup(*[Dot(pt, radius=0.08, color=BLUE) for pt in pts])
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.08), run_time=1.0)
        self.at("curve plunges")
        self.play(FadeIn(area), Create(curve), run_time=2.2, rate_func=linear)
        self.at("then flattens")
        self.play(Indicate(VGroup(*dots[-3:]), color=GREEN, scale_factor=1.2), run_time=0.8)
        self.finish()


class S12Limits(FilmScene):
    def construct(self):
        p, curve, pts, area = cost_plot(box=(-5.85, 5.75, -1.9, 2.25))
        left_zone = Rectangle(width=4.1, height=4.15, stroke_width=0, fill_color=PURPLE,
                              fill_opacity=0.16).move_to([-3.8, 0.18, 0])
        right_zone = Rectangle(width=7.5, height=4.15, stroke_width=0, fill_color=BLUE,
                               fill_opacity=0.12).move_to([1.85, 0.18, 0])
        p.remove(p.ylabel)
        ylab = T("estimated production cost, log scale", 24, GREY).rotate(PI / 2).move_to([-6.45, 0.18, 0])
        early = T("build without reference", 26, PURPLE).move_to([-3.75, 2.7, 0])
        late = T("re-sequence against reference", 26, BLUE).move_to([2.25, 2.7, 0])
        self.add(left_zone, right_zone, area, p, ylab, curve, early, late)
        pulse(curve, base=7, amp=1.5, speed=2.0)
        travel = Dot(pts[0], radius=0.11, color=YELLOW)
        travel._clock = 0.0
        def follow_data(mob, dt):
            mob._clock = (mob._clock + dt / 15.5) % 1.0
            u = mob._clock * (len(pts) - 1)
            i = min(int(u), len(pts) - 2)
            mob.move_to(interpolate(pts[i], pts[i + 1], u - i))
        travel.add_updater(follow_data)
        scan = scan_band(0.5, 4.2, YELLOW, [0, 0.18, 0], span=11.0, seconds=8.0)
        self.add(scan, travel)
        self.at("curve needs limits")
        self.play(Indicate(curve, color=BLUE, scale_factor=1.01), run_time=0.8)
        tags = VGroup(model_tag("production estimate", ORANGE, 25),
                      model_tag("not a customer price", ORANGE, 25),
                      model_tag("interpretation excluded", ORANGE, 25)).arrange(RIGHT, buff=0.35)
        fit(tags, max_w=12.0).move_to([0, -3.05, 0])
        self.at("production estimates")
        self.play(FadeIn(tags[0], shift=UP * 0.1), run_time=0.6)
        self.at("not prices paid")
        self.play(FadeIn(tags[1], shift=UP * 0.1), run_time=0.6)
        self.at("Later estimates")
        self.play(Indicate(right_zone, color=BLUE, scale_factor=1.01), run_time=0.8)
        self.at("Earlier estimates")
        self.play(Indicate(left_zone, color=PURPLE, scale_factor=1.01), run_time=0.8)
        self.at("Interpretation costs")
        self.play(FadeIn(tags[2], shift=UP * 0.1), run_time=0.6)
        self.finish()


class S13ScaleUp(FilmScene):
    def construct(self):
        p, curve, pts, area = cost_plot(box=(-5.9, -1.5, 0.8, 3.0))
        mini = VGroup(area, p, curve).scale(0.93)
        budget = labelled_box("fixed budget", PURPLE, width=2.5, height=1.05, size=30, fill=0.24).move_to([4.8, 2.2, 0])
        self.add(scan_band(0.55, 4.2, GREEN, [0, -1.0, 0], span=10.5, seconds=7.0))
        self.at("Lower cost")
        self.play(FadeIn(mini), FadeIn(budget), run_time=0.9)
        ref = letter_strip(BASES, block_w=0.68, block_h=0.54, size=25).move_to([0.2, -0.78, 0])
        reflab = T("one reference", 28, BLUE, weight=BOLD).next_to(ref, UP, buff=0.25)
        self.at("fixed budget")
        self.play(FadeIn(ref), FadeIn(reflab), run_time=0.7)
        seqs = VGroup()
        for i in range(5):
            s = strip(8 + (i % 3), "", block_w=0.31, block_h=0.25)
            s.move_to([-1.3 + 0.5 * (i % 2), -1.45 - 0.42 * i, 0])
            seqs.add(s)
        self.at("read more genomes")
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.3) for s in seqs], lag_ratio=0.14), run_time=1.7)
        diffs = VGroup(*[SurroundingRectangle(s[min(2 + i % 3, len(s)-1)], color=GREEN,
                                              stroke_width=4, buff=0.02) for i, s in enumerate(seqs)])
        self.at("compare many people")
        self.play(LaggedStart(*[FadeIn(d) for d in diffs], lag_ratio=0.12), run_time=1.2)
        limit = model_tag("leaves out variation", ORANGE, 25).move_to([4.25, -0.78, 0])
        self.at("model with limits")
        self.play(FadeIn(limit, shift=LEFT * 0.15), run_time=0.8)
        self.finish()


class S14ReturnRule(FilmScene):
    def construct(self):
        world, sample, frames, lens = question_world("shape", comparison=True)
        self.add(world)
        shape = shape_contents(frames[0][0])
        letters = order_contents(frames[1][0])
        ruler = letter_strip("ATGCC", block_w=0.43, block_h=0.42, size=22).move_to(frames[2][0].get_center() + DOWN * 0.18)
        tabs = VGroup(*[model_tag("leaves out", ORANGE, 22).scale(0.8).next_to(obj, DOWN, buff=0.12)
                        for obj in (shape, letters, ruler)])
        self.at("Shape required")
        self.play(FadeIn(shape, shift=UP * 0.15), FadeIn(tabs[0]), run_time=0.8)
        lens2 = SurroundingRectangle(frames[1][0], color=YELLOW, stroke_width=7, buff=0.08, corner_radius=0.22)
        self.at("Order required")
        self.play(ReplacementTransform(lens, lens2), FadeIn(letters, shift=UP * 0.15), FadeIn(tabs[1]), run_time=0.9)
        lens3 = SurroundingRectangle(frames[2][0], color=YELLOW, stroke_width=7, buff=0.08, corner_radius=0.22)
        self.at("Comparison required")
        self.play(ReplacementTransform(lens2, lens3), FadeIn(ruler, shift=UP * 0.15), FadeIn(tabs[2]), run_time=0.9)
        qlens = SurroundingRectangle(world[1], color=YELLOW, stroke_width=6, buff=0.12, corner_radius=0.18)
        self.at("models by the question")
        self.play(ReplacementTransform(lens3, qlens), run_time=1.1)
        self.at("every model leaves")
        self.play(LaggedStart(*[Indicate(t, color=ORANGE, scale_factor=1.06) for t in tabs], lag_ratio=0.18), run_time=1.2)
        self.finish()


class S15End(EndCard):
    LINE = "Choose DNA models by the question; every model leaves features out."
