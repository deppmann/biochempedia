"""Finding One Band in a Smear.

BLUE = gel apparatus and unprobed DNA; TEAL = RNA and capillary flow;
GREY = membrane and reference structure; YELLOW = probe and detected band;
GREEN = assay controls; RED = absent signal; GOLD = dates and teaching cues.
All bands, example loads, and signal ratios are schematic.
"""
from bp_parts import *  # noqa: F403


CENTER = -1.65
WIDTH = 8.2
TOP, BOTTOM = 2.48, -2.72
LADDER, NORMAL, TUMOR, CONTROL = -4.65, -2.65, -0.65, 1.35
LONG, SHORT = 0.87, -1.03
RIGHT_X = 4.58
QUESTION = "What will the tumor lane show?"
LADDER_ROWS = (1.63, LONG, 0.2, SHORT, -1.62, -2.16)
GEL_ROWS = (1.47, LONG, 0.21, -0.39, SHORT, -1.67, -2.17)
GEL_WIDTHS = (1.33, 1.22, 1.09, 0.96, 0.82, 0.72, 0.62)


def at_xy(x, y):
    return np.array([x, y, 0.0])


def rect(x, y, width, height, color, opacity=1, radius=0.05):
    return RoundedRectangle(
        width=width, height=height, corner_radius=min(radius, height * 0.45),
        stroke_width=0, fill_color=color, fill_opacity=opacity,
    ).move_to(at_xy(x, y))


def panel(membrane=False):
    """The gel and its membrane share dimensions and lane coordinates."""
    color, fill = (GREY, "#293441") if membrane else (BLUE, "#213944")
    return RoundedRectangle(
        width=WIDTH, height=TOP - BOTTOM, corner_radius=0.18, stroke_color=color,
        stroke_width=2.5, fill_color=fill, fill_opacity=1,
    ).move_to(at_xy(CENTER, (TOP + BOTTOM) / 2))


def lane(x, width=1.55, mouth=False):
    track = rect(x, -0.12, width, 4.74, "#141E2A", 0.72, 0.10)
    if mouth:
        well = rect(x, 2.03, width * 0.89, 0.20, BLUE, 0.32)
        return VGroup(track, well)
    return track


def signal(x, y, width=1.22, color=YELLOW, strength=1, height=0.13):
    """A schematic band, with the halo following the same intensity as its core."""
    halo = rect(x, y, width + 0.12, height * 2.3, color, 0.16 * strength)
    core = rect(x, y, width, height, color, strength)
    return VGroup(halo, core)


def size_ladder(x=LADDER):
    return VGroup(*[signal(x, y, 0.96, BLUE, 0.72, 0.094) for y in LADDER_ROWS])


def lane_name(text, x, color=TEXT):
    return T(text, 28, color).move_to(at_xy(x, 2.86))


def side(text, y=0, color=TEXT, size=34):
    return fit_text(text, max_w=3.75, size=size, min_size=28,
                    color=color).move_to(at_xy(RIGHT_X, y))


def tag():
    return scope_tag(size=28, color=TEXT)


def migration_arrow(x, y0, y1, color=BLUE):
    return Arrow(at_xy(x, y0), at_xy(x, y1), buff=0, color=color,
                 stroke_width=5, tip_length=0.18)


def smear(x=NORMAL):
    rng = np.random.default_rng(19)
    rows = np.linspace(-2.12, 1.71, 53)
    segments = VGroup()
    for y in rows:
        segments.add(rect(x + rng.uniform(-0.10, 0.10), y,
                          rng.uniform(0.52, 1.45), rng.uniform(0.045, 0.10),
                          BLUE, rng.uniform(0.14, 0.56)))
    return segments


def smear_stage():
    return panel(), lane(NORMAL, 1.9), smear()


def smear_drift(segments):
    centers = [part.get_center().copy() for part in segments]
    clock = ValueTracker(0)

    def drift(group, dt):
        clock.increment_value(dt)
        t = clock.get_value()
        for i, (part, center) in enumerate(zip(group, centers)):
            part.move_to(center + DOWN * (0.22 * np.sin(1.35 * t + i * 0.29)))
            part.set_fill(opacity=0.40 + 0.20 * np.sin(2.4 * t + i * 0.56))

    segments.add_updater(drift)


def gel_stage():
    slab = panel()
    rails = VGroup(lane(LADDER, mouth=True), lane(NORMAL, mouth=True))
    return slab, rails


def gel_fragments(double=True):
    parts = VGroup()
    for y, width in zip(GEL_ROWS, GEL_WIDTHS):
        if double:
            band = VGroup(rect(NORMAL, y + 0.052, width, 0.075, BLUE, 0.9),
                          rect(NORMAL, y - 0.052, width, 0.075, BLUE, 0.73))
        else:
            band = rect(NORMAL, y, width, 0.062, BLUE, 0.80)
        parts.add(band)
    return parts


def film_bands():
    return signal(NORMAL, LONG, GEL_WIDTHS[1])


def southern_result():
    return VGroup(panel(True), lane(LADDER), lane(NORMAL), size_ladder(), film_bands())


def southern_name():
    return side("Southern · DNA", 0.95, TEXT, 34)


def flow_front():
    return rect(CENTER, -2.48, WIDTH - 0.45, 0.26, TEAL, 0.40)


def probe_cloud():
    probes = VGroup()
    for x, y, width in ((-4.86, 1.65, 0.49), (-4.45, LONG - 0.13, 0.76),
                        (-4.08, 0.13, 0.56), (-4.73, -0.64, 0.63),
                        (-4.93, -1.32, 0.50), (-4.20, -2.02, 0.69)):
        probes.add(signal(x, y, width, YELLOW, 0.93, 0.061))
    return probes


def allele_stage():
    """One Southern blot used for the prediction, controls, and 1983 result."""
    return VGroup(panel(True), lane(LADDER), lane(NORMAL), lane(TUMOR), size_ladder(),
                  lane_name("Ladder", LADDER), lane_name("Normal", NORMAL),
                  lane_name("Tumor", TUMOR), tag())


def normal_bands():
    return VGroup(signal(NORMAL, LONG), signal(NORMAL, SHORT, 0.94))


def tumor_band():
    return signal(TUMOR, LONG)


def unknown():
    return T("?", 80, GOLD).move_to(at_xy(TUMOR, -0.10)).set_z_index(1)


def prediction():
    text = question_card(QUESTION, y=-3.26, size=34)
    paper = rect(-0.5, -3.26, 7.40, 0.67, GOLD, 0.19, 0.12)
    return VGroup(paper, text)


def scan(x, width=1.42, y=1.65, color=YELLOW):
    """A soft inspection light that traverses a lane without moving its bands."""
    return VGroup(rect(x, y, width, 1.02, color, 0.18, 0.12),
                  rect(x, y, width * 0.96, 0.72, color, 0.32, 0.12),
                  rect(x, y, width * 0.88, 0.22, color, 0.31, 0.10))


class S01Hook(SpokenScene):
    def construct(self):
        slab, track, blur = smear_stage()
        hint = T("?", 112, GOLD).move_to(at_xy(0.25, LONG))
        ring = RoundedRectangle(width=1.7, height=0.40, corner_radius=0.10,
                                stroke_color=GOLD, stroke_width=3).move_to(at_xy(NORMAL, LONG))
        self.add(slab, track, blur)
        self.at("find one gene")
        self.play(FadeIn(hint), run_time=0.72)
        self.at("hides in a smear")
        self.play(Create(ring), run_time=0.75)
        pulse(ring, base=3, amp=1.6, speed=4)
        smear_drift(blur)
        self.at("cut genomic DNA")
        blur.clear_updaters()
        cutter = side("Restriction\nenzyme", 1.28, BLUE)
        strand = rect(RIGHT_X, 0.46, 2.80, 0.13, BLUE)
        self.play(FadeOut(hint), FadeOut(ring), GrowFromCenter(strand), run_time=0.7)
        smear_drift(blur)
        split = VGroup(rect(3.88, 0.46, 1.12, 0.13, BLUE),
                       rect(5.44, 0.46, 1.35, 0.13, BLUE))
        self.play(FadeIn(cutter), Transform(strand, split), run_time=1.35)
        self.at("sequence specific cutter")
        self.play(strand[0].animate.shift(LEFT * 0.20),
                  strand[1].animate.shift(RIGHT * 0.25), run_time=1.25)
        self.at("a gel shows")
        self.play(FadeOut(strand), FadeOut(cutter), run_time=0.65)
        self.at("to spot one")
        size = side("Size", 0.73, BLUE, 41)
        identity = side("Identity", -0.42, YELLOW, 41)
        self.play(FadeIn(size), run_time=0.85)
        self.at("its identity")
        self.play(FadeIn(identity), run_time=0.65)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Finding One Band in a Smear"
    LESSON = "Southern and northern blots"

    def construct(self):
        slab, track, blur = smear_stage()
        smear_drift(blur)
        shade = panel().set_fill(BG, opacity=0.23).set_stroke(width=0)
        title = fit_text(self.TITLE, max_w=11.2, size=50, font=TITLE_FONT)
        title.move_to(at_xy(-0.65, 3.27))
        lesson = side(self.LESSON, 0.12, TEXT, 32)
        self.add(slab, track, blur, shade)
        self.play(FadeIn(title), FadeIn(lesson), run_time=0.53)
        self.wait(1.40)


class S03Gel(SpokenScene):
    def construct(self):
        slab, rails = gel_stage()
        bands = gel_fragments()
        staged = [at_xy(NORMAL, 2.02 - i * 0.023) for i in range(len(bands))]
        parked = [band.get_center().copy() for band in bands]
        for band, pos in zip(bands, staged):
            band.move_to(pos)
        self.add(slab, rails, tag())
        self.at("load the cut")
        sample = signal(NORMAL, 2.02, 1.36, BLUE, 0.91, 0.25)
        self.play(FadeIn(sample, shift=DOWN * 0.20), run_time=1.3)
        gel = side("Agarose gel", 1.58, BLUE)
        self.play(FadeIn(gel), run_time=0.65)
        self.at("negatively charged backbone")
        minus = T("−", 48, BLUE).move_to(at_xy(-4.95, 2.95))
        plus = T("+", 48, BLUE).move_to(at_xy(-4.95, -3.18))
        electrodes = VGroup(rect(CENTER, 2.32, 7.46, 0.13, BLUE, 0.75),
                            rect(CENTER, -2.52, 7.46, 0.13, BLUE, 0.75))
        field = migration_arrow(0.76, 1.70, -2.19)
        self.play(FadeIn(minus), FadeIn(plus), GrowArrow(field),
                  LaggedStart(*[GrowFromCenter(plate) for plate in electrodes], lag_ratio=0.35),
                  sample.animate.set_y(1.72), run_time=1.0)
        self.at("moves toward")
        for band in bands:
            band.shift(DOWN * 0.30)
        self.play(FadeIn(bands), FadeOut(sample), run_time=0.42)
        self.play(*[band.animate.move_to(a + 0.47 * (b - a))
                    for band, a, b in zip(bands, staged, parked)], run_time=3.32, rate_func=linear)
        self.at("smaller fragments")
        mesh = VGroup(*[Line(at_xy(a, 1.67), at_xy(a, -2.30), color=BLUE,
                             stroke_width=1, stroke_opacity=0.15)
                        for a in np.linspace(NORMAL - 0.65, NORMAL + 0.65, 8)])
        mesh.set_z_index(-1)
        slab.set_z_index(-3)
        rails.set_z_index(-2)
        self.play(FadeIn(mesh), *[band.animate.move_to(b) for band, b in zip(bands, parked)],
                  run_time=3.18, rate_func=linear)
        self.at("a size ladder")
        ladder = size_ladder()
        self.play(LaggedStart(*[FadeIn(row) for row in ladder], lag_ratio=0.34),
                  FadeOut(minus), FadeOut(plus), FadeOut(field), FadeOut(electrodes), run_time=1.8)
        ladder_name = lane_name("Ladder", LADDER)
        guide = DashedLine(at_xy(LADDER + 0.57, LONG), at_xy(NORMAL - 0.70, LONG),
                           color=BLUE, stroke_width=3, dash_length=0.11)
        self.at("turns position")
        reader = scan(LADDER, y=1.72, color=BLUE)
        self.play(FadeIn(ladder_name), Create(guide), FadeIn(reader), run_time=0.68)
        self.play(reader.animate.set_y(LONG), run_time=1.50, rate_func=linear)
        self.at("still a right sized band")
        bracket = RoundedRectangle(width=1.51, height=0.39, corner_radius=0.09,
                                   stroke_color=GOLD, stroke_width=3).move_to(at_xy(NORMAL, LONG))
        self.play(Create(bracket), reader.animate.set_x(NORMAL), run_time=0.72)
        pulse(bracket, base=3.4, amp=1.7)
        size = side("Size only", 1.58, GOLD)
        self.play(swap(gel, size), FadeOut(reader), run_time=0.90)
        self.finish()


class S04Southern(SpokenScene):
    def construct(self):
        slab, rails = gel_stage()
        bands = gel_fragments()
        ladder = size_ladder()
        self.add(slab, rails, ladder, bands, tag())
        self.at("in 1975")
        date = side("1975", 1.83, GOLD, 45)
        self.play(FadeIn(date), run_time=0.78)
        self.at("Edwin Southern")
        southern = southern_name()
        reading = scan(NORMAL, color=BLUE)
        self.play(FadeIn(southern), FadeIn(reading), run_time=0.65)
        self.play(reading.animate.set_y(-2.05), run_time=3.65, rate_func=linear)
        self.play(FadeOut(reading), run_time=0.35)
        self.at("is denatured")
        self.play(FadeOut(date), LaggedStart(*[
            AnimationGroup(pair[0].animate.shift(UP * 0.093), pair[1].animate.shift(DOWN * 0.093))
            for pair in bands
        ], lag_ratio=0.25), run_time=2.03)
        strands = side("Single strands", -0.22, BLUE)
        self.play(FadeIn(strands), run_time=0.72)
        self.at("capillary flow")
        front = flow_front()
        membrane = panel(True)
        paper = side("Cellulose nitrate\nmembrane", -0.45, TEXT, 30)
        layer = rect(CENTER, -2.65, WIDTH - 0.44, 0.10, GREY, 0.94)
        self.play(FadeIn(front), FadeIn(layer), FadeOut(strands), run_time=0.48)
        self.play(front.animate.set_y(2.12), layer.animate.set_y(2.27),
                  run_time=2.86, rate_func=linear)
        self.at("cellulose nitrate membrane")
        self.play(Transform(slab, membrane), Transform(rails, VGroup(lane(LADDER), lane(NORMAL))),
                  FadeOut(front), FadeOut(layer),
                  FadeIn(paper), run_time=1.35)
        self.at("a labeled probe")
        incoming = probe_cloud()
        self.play(FadeIn(incoming, shift=RIGHT * 0.32), FadeOut(paper), run_time=0.7)
        matching = incoming[1]
        others = VGroup(*[item for i, item in enumerate(incoming) if i != 1])
        probe = side("Labeled probe", -0.37, YELLOW)
        self.play(FadeIn(probe), matching.animate.move_to(at_xy(NORMAL, LONG - 0.04)),
                  others.animate.shift(RIGHT * 1.46), run_time=1.91, rate_func=linear)
        self.at("only to matching")
        wash = scan(NORMAL, y=1.91, color=TEAL)
        self.add(wash)
        self.play(FadeOut(others, shift=RIGHT * 1.14), wash.animate.set_y(-2.10),
                  *[part.animate.set_opacity(0.16) for part in bands], run_time=2.58)
        result = film_bands()
        self.at("the gel sorts")
        self.play(FadeOut(bands), FadeOut(matching), FadeOut(wash),
                  FadeIn(result), run_time=1.22)
        self.at("pairing with the probe")
        hybrid = side("Hybridization", -0.37, YELLOW)
        expose = scan(NORMAL, y=1.72)
        self.play(swap(probe, hybrid), FadeIn(expose), run_time=0.73)
        self.play(expose.animate.set_y(LONG), run_time=1.73, rate_func=linear)
        self.play(FadeOut(expose), run_time=0.67)
        self.finish()


class S05Northern(SpokenScene):
    def construct(self):
        previous = southern_result()
        old = southern_name()
        self.add(*previous, old, tag())
        self.at("in 1977")
        date = side("1977", 1.83, GOLD, 45)
        authors = side("Alwine, Kemp\nand Stark", -1.0, TEXT, 31)
        self.play(FadeIn(date), run_time=0.75)
        self.at("James Alwine")
        study = scan(NORMAL, y=1.82)
        self.play(FadeIn(authors), FadeIn(study), run_time=0.64)
        self.play(study.animate.set_y(-1.86), run_time=1.98, rate_func=linear)
        slab, old_ladder_lane, old_sample_lane, ladder, result = previous
        self.at("adapted transfer")
        self.play(Transform(slab, panel()), FadeOut(old_ladder_lane),
                  Transform(old_sample_lane, lane(NORMAL, mouth=True)),
                  FadeIn(lane(TUMOR, mouth=True)), FadeOut(ladder), FadeOut(result), FadeOut(study),
                  run_time=1.88)
        self.at("its name")
        northern = side("Northern · RNA", 0.95, TEAL, 35)
        compass = migration_arrow(RIGHT_X, -0.47, 0.41, TEAL)
        self.play(FadeOut(authors), GrowArrow(compass), run_time=0.7)
        self.at("northern blot")
        self.play(swap(old, northern), run_time=0.87)
        self.play(FadeOut(date), FadeOut(compass), run_time=0.68)
        final = [(x, y, w) for x in (NORMAL, TUMOR)
                 for y, w in ((1.38, 1.28), (LONG, 1.08), (-0.20, 0.85), (-1.38, 0.60))]
        fragments = VGroup(*[rect(x, 2.01 - (i % 4) * 0.06, w, 0.083, TEAL)
                             for i, (x, _, w) in enumerate(final)])
        self.play(FadeIn(fragments), run_time=0.70)
        self.at("RNA separates")
        self.play(*[part.animate.move_to(at_xy(x, y))
                    for part, (x, y, _) in zip(fragments, final)], run_time=1.66)
        self.at("transfers to a membrane")
        flow = flow_front()
        self.add(flow)
        self.play(flow.animate.set_y(2.15), Transform(slab, panel(True)), run_time=1.57)
        self.remove(flow)
        self.at("binds a labeled DNA probe")
        probes = VGroup(signal(NORMAL - 1.45, LONG - 0.12, 0.70, height=0.06),
                        signal(TUMOR - 1.39, LONG - 0.12, 0.70, height=0.06))
        self.add(probes)
        self.play(probes.animate.shift(RIGHT * 1.40),
                  *[f.animate.set_opacity(0.24) for f in fragments], run_time=2.38)
        self.at("band intensity")
        faint = signal(NORMAL, LONG, 1.10, strength=0.33)
        bright = signal(TUMOR, LONG, 1.10, strength=1)
        self.play(FadeOut(probes), FadeOut(fragments), FadeIn(faint), FadeIn(bright), run_time=1.0)
        less = lane_name("Less", NORMAL)
        more = lane_name("More", TUMOR)
        amount = side("mRNA amount", -0.24, TEXT, 32)
        self.at("how much messenger RNA")
        light = scan(TUMOR, width=1.40)
        self.play(FadeIn(less), FadeIn(more), FadeIn(amount), FadeIn(light), run_time=0.6)
        self.play(light.animate.set_y(-1.77), run_time=2.25, rate_func=linear)
        self.play(FadeOut(light), run_time=0.38)
        self.finish()


class S06PredictQ(SpokenScene):
    def construct(self):
        stage = allele_stage()
        self.add(*stage[:2], *stage[2:5], stage[-1])
        self.at("a chromosome's two copies")
        heads = VGroup(rect(NORMAL, 1.84, 1.46, 0.35, BLUE),
                       rect(NORMAL, 0.03, 1.46, 0.35, BLUE))
        heads.set_z_index(1)
        header = lane_name("Two copies", NORMAL, BLUE)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in heads], lag_ratio=0.6),
                  run_time=1.18)
        self.play(FadeIn(header), run_time=0.55)
        self.at("an enzyme cuts")
        top = VGroup(rect(NORMAL - 0.23, 1.84, 1.00, 0.35, BLUE),
                     rect(NORMAL + 0.60, 1.84, 0.38, 0.35, BLUE, 0.33))
        low = VGroup(rect(NORMAL - 0.51, 0.03, 0.45, 0.35, BLUE),
                     rect(NORMAL + 0.31, 0.03, 0.82, 0.35, BLUE, 0.33))
        active_cut = rect(NORMAL, 1.07, 1.51, 2.37, BLUE, 0.47, 0.12)
        self.play(FadeIn(active_cut), run_time=0.72)
        self.play(Transform(heads[0], top.set_z_index(1)),
                  active_cut.animate.set_y(1.22), run_time=1.12)
        self.play(FadeOut(active_cut), run_time=0.73)
        self.at("into a long piece")
        long_label = side("Long fragment", 1.30, TEXT, 30)
        self.play(FadeIn(long_label), heads[0][0].animate.shift(DOWN * 0.49), run_time=1.27)
        self.at("into a short piece")
        self.play(Transform(heads[1], low.set_z_index(1)), run_time=0.72)
        short_label = side("Short fragment", -0.37, TEXT, 30)
        self.play(FadeIn(short_label), heads[1][0].animate.shift(DOWN * 0.54), run_time=1.28)
        self.at("normal tissue shows")
        bands = normal_bands()
        self.play(TransformFromCopy(heads[0][0], bands[0]), swap(header, stage[6]), run_time=1.08)
        self.play(TransformFromCopy(heads[1][0], bands[1]), FadeIn(stage[5]), run_time=1.20)
        self.add(*bands)
        self.play(FadeOut(heads), FadeOut(long_label), FadeOut(short_label),
                  run_time=0.65)
        self.at("if a tumor cell")
        outlook = scan(TUMOR, width=1.53, y=1.83, color=BLUE)
        self.play(FadeIn(stage[7]), FadeIn(outlook), run_time=0.68)
        self.play(outlook.animate.set_y(0.49), run_time=1.48, rate_func=linear)
        self.at("what will its lane")
        card = prediction()
        card[0].set_fill(opacity=0.36)
        self.play(FadeIn(card, shift=LEFT * 0.54), FadeIn(unknown()),
                  outlook.animate.set_y(-1.87), run_time=1.48, rate_func=linear)
        self.play(FadeOut(outlook, shift=UP * 0.78), card[0].animate.set_fill(opacity=0.19),
                  run_time=0.57, rate_func=linear)
        self.finish()


class S07PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(allele_stage(), normal_bands(), unknown(), prediction())
        self.wait(4.5)


class S08Controls(SpokenScene):
    def construct(self):
        stage = allele_stage()
        bands = normal_bands()
        q, mark = prediction(), unknown()
        self.add(stage, bands, q, mark)
        self.at("only one band")
        band = tumor_band()
        ghost = DashedVMobject(
            RoundedRectangle(width=0.94, height=0.18, corner_radius=0.07,
                             stroke_color=RED, stroke_width=2.5).move_to(at_xy(TUMOR, SHORT)),
            num_dashes=12,
        )
        compare = scan(TUMOR, y=1.79)
        self.play(FadeOut(q), FadeOut(mark), FadeIn(band), FadeIn(compare), run_time=0.34)
        self.play(compare.animate.set_y(LONG), run_time=1.1, rate_func=linear)
        self.at("the tumor lost")
        self.play(Create(ghost), compare.animate.set_y(SHORT), run_time=1.65)
        self.play(FadeOut(compare), run_time=0.65)
        self.at("brightness alone")
        warning = side("Uneven loading", 1.08, RED)
        loaded = scan(TUMOR, width=1.50, y=1.82)
        self.play(FadeOut(ghost), FadeIn(warning), FadeIn(loaded), run_time=0.85)
        self.play(loaded.animate.set_y(LONG), run_time=0.92, rate_func=linear)
        self.at("uneven loading shifts")
        self.play(Transform(band, signal(TUMOR, LONG, strength=0.22, height=0.08)),
                  FadeOut(loaded, shift=DOWN * 0.75), run_time=2.35)
        self.at("a size ladder")
        ladder_glow = scan(LADDER, color=BLUE)
        self.play(FadeOut(warning), FadeIn(ladder_glow),
                  Transform(band, tumor_band()), run_time=0.52)
        self.play(ladder_glow.animate.set_y(-1.88), run_time=1.57, rate_func=linear)
        self.at("a positive control")
        positive = lane(CONTROL)
        label = lane_name("Positive", CONTROL, GREEN)
        known = signal(CONTROL, LONG, color=GREEN)
        self.play(FadeOut(ladder_glow), FadeIn(positive), FadeIn(known), run_time=0.6)
        self.play(FadeIn(label), run_time=0.65)
        check = rect(CONTROL, 1.39, 1.47, 1.65, GREEN, 0.45, 0.12)
        self.add(check)
        self.play(check.animate.set_y(-1.53), run_time=1.9, rate_func=linear)
        self.play(FadeOut(check), run_time=0.36)
        self.at("a loading control")
        strip = VGroup(*[signal(x, -2.02, 0.97, GREEN, 0.85)
                         for x in (NORMAL, TUMOR, CONTROL)])
        self.play(LaggedStart(*[GrowFromCenter(m) for m in strip], lag_ratio=0.46),
                  run_time=1.2)
        loading = caption("Loading control", size=32, color=GREEN, y=-3.18)
        self.play(FadeIn(loading), run_time=0.75)
        lower = VGroup(*[scan(x, width=1.45, y=-2.02, color=GREEN)
                         for x in (NORMAL, TUMOR, CONTROL)])
        self.play(FadeIn(lower), run_time=0.72)
        self.play(FadeOut(lower), run_time=1.68)
        self.at("supports comparison")
        plot = Plot(box=(3.27, 6.23, -1.44, 0.91), xr=(0, 1), yr=(0, 1),
                    xlabel="Amount", color=TEXT, label_size=28)
        ylabel = side("Brightness", 1.43, TEXT, 30)
        value = ValueTracker(0)
        response = lambda amount: min(1.7 * amount, 0.82)
        curve = plot.live_curve(response, value, GREEN, width=5)
        dot = plot.dot(value.get_value, lambda: response(value.get_value()), GREEN, TEXT, radius=0.082)
        self.play(FadeIn(plot), FadeIn(ylabel), run_time=0.65)
        self.add(curve, dot)
        self.at("brightness still tracks")
        self.play(value.animate.set_value(1), run_time=1.8, rate_func=linear)
        limit = side("Signal saturates", -2.41, GOLD, 30)
        self.play(FadeIn(limit), run_time=0.48)
        self.finish()


class S09UnlockedDna(SpokenScene):
    def construct(self):
        stage = allele_stage()
        normal = normal_bands()
        present = tumor_band()
        missing = DashedVMobject(
            RoundedRectangle(width=0.95, height=0.19, corner_radius=0.07,
                             stroke_color=RED, stroke_width=2.7).move_to(at_xy(TUMOR, SHORT)),
            num_dashes=12,
        )
        self.add(stage, normal)
        self.at("in 1983")
        date = side("1983", 1.84, GOLD, 45)
        people = side("Cavenee, Dryja\net al.", 0.90, TEXT, 30)
        self.play(FadeIn(date), run_time=0.75)
        self.at("Webster")
        normal_light = scan(NORMAL, y=1.80)
        self.play(FadeIn(people), FadeIn(normal_light), run_time=0.64)
        self.play(normal_light.animate.set_y(-1.87), run_time=2.09, rate_func=linear)
        self.at("compared normal and tumor")
        self.play(FadeOut(normal_light), run_time=0.56)
        disease = side("Retinoblastoma", -0.53, BLUE, 30)
        self.at("in retinoblastoma")
        reader = scan(TUMOR, y=1.6)
        self.play(FadeIn(disease), FadeIn(reader), run_time=0.64)
        self.play(reader.animate.set_y(LONG), run_time=2.39, rate_func=linear)
        self.at("the tumor showed")
        self.play(FadeIn(present), reader.animate.set_y(SHORT), run_time=1.47)
        self.at("chromosome 13 alleles")
        key = caption("Chromosome 13 alleles", 32, y=-3.18)
        self.play(FadeIn(key), Create(missing), run_time=0.78)
        self.play(FadeOut(reader), FadeOut(missing), run_time=1.36)
        self.finish()


def her2_stage():
    positions = np.linspace(-5.19, 1.9, 10)
    rails = VGroup(*[lane(x, 0.64) for x in positions])
    elevated = {2, 5, 8}
    reference, strong = 0.43, 0.98
    control = VGroup(*[signal(x, -0.65, 0.51, GREEN, reference, 0.14) for x in positions])
    targets = VGroup(*[signal(x, 1.03, 0.51, YELLOW,
                              strong if i in elevated else reference, 0.14)
                       for i, x in enumerate(positions)])
    bars = VGroup()
    for i, x in enumerate(positions):
        intensity = strong if i in elevated else reference
        height = 0.50 * intensity / reference
        bars.add(rect(x, -2.34 + height / 2, 0.37, height, YELLOW, 0.92))
    return positions, rails, targets, control, bars


class S09bUnlockedHer2(SpokenScene):
    def construct(self):
        positions, rails, targets, controls, bars = her2_stage()
        self.add(panel(True), rails, tag())
        self.at("in 1987")
        date = side("1987", 1.91, GOLD, 44)
        authors = side("Slamon et al.", 1.16, TEXT, 32)
        self.play(FadeIn(date), run_time=0.65)
        self.at("Dennis")
        self.play(FadeIn(authors), run_time=0.65)
        self.at("probed 189")
        probe_pass = scan(CENTER, width=7.37, y=1.91)
        self.play(FadeIn(probe_pass), run_time=0.58)
        self.play(probe_pass.animate.set_y(1.03),
                  LaggedStart(*[GrowFromCenter(m) for m in targets], lag_ratio=0.22),
                  run_time=2.30, rate_func=linear)
        self.play(FadeOut(probe_pass), run_time=0.45)
        count = side("189 breast\ncancers", -0.24, TEXT, 31)
        self.play(FadeIn(count), run_time=0.60)
        self.at("strength against")
        self.play(FadeOut(count), FadeOut(authors), FadeOut(date), run_time=0.43)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in controls], lag_ratio=0.45), run_time=1.36)
        target_label = side("HER2", 1.03, YELLOW, 40)
        control_label = side("Control gene", -0.65, GREEN, 32)
        self.play(FadeIn(target_label), FadeIn(control_label), run_time=0.73)
        self.at("reported HER2 copies")
        ratio = side("HER2 ÷ control", -2.11, TEXT, 30)
        self.play(LaggedStart(*[GrowFromEdge(m, DOWN) for m in bars], lag_ratio=0.38),
                  FadeIn(ratio), run_time=2.58)
        self.at("about 30")
        elevated = VGroup(*[scan(positions[i], width=0.64, y=1.60) for i in (2, 5, 8)])
        stat = side("About 30%\nextra copies", 2.01, GOLD, 34)
        self.play(FadeIn(elevated), FadeIn(stat), run_time=0.68)
        self.play(elevated.animate.shift(DOWN * 3.35), run_time=2.1, rate_func=linear)
        self.at("women relapsed")
        outcome = caption("Earlier relapse and death", size=31, y=-3.19)
        self.play(FadeIn(outcome), elevated.animate.set_y(-1.78), run_time=0.76)
        self.play(FadeOut(elevated), run_time=2.15)
        self.at("with lymph node spread")
        emphasis = caption("Clearest with lymph-node spread", size=31, y=-3.19)
        self.play(swap(outcome, emphasis), run_time=0.93)
        self.finish()


GENES = (("VEGF", 1.27), ("PDGF-B", 0.0), ("GLUT1", -1.27))


def rna_lane(x, strength):
    return VGroup(*[signal(x, y, 1.12, YELLOW, strength, 0.15) for _, y in GENES])


def gene_label(i):
    name, height = GENES[i]
    return side(name, height, YELLOW, 34)


def rna_study():
    return VGroup(panel(True), lane(NORMAL), lane(TUMOR), tag())


def tissue_label():
    return caption("Kidney-cancer cells · Northern blot", size=31, y=-3.18)


class S10UnlockedRna(SpokenScene):
    def construct(self):
        self.add(rna_study())
        self.at("in 1996")
        date = side("1996", 2.03, GOLD, 40)
        team = side("Kaelin et al.", 1.28, TEXT, 30)
        tissue = tissue_label()
        self.play(FadeIn(date), run_time=0.65)
        self.at("William")
        self.play(FadeIn(team), run_time=0.68)
        self.at("northern blots")
        reader = scan(NORMAL, y=1.88, color=TEAL)
        self.play(FadeIn(tissue), FadeIn(reader), run_time=0.6)
        self.play(reader.animate.set_y(-1.85), run_time=2.14, rate_func=linear)
        self.at("some lacked")
        absent = lane_name("−VHL", NORMAL)
        restored = lane_name("+VHL", TUMOR)
        self.play(FadeIn(absent), FadeOut(reader), run_time=0.7)
        self.at("others had it restored")
        check = scan(TUMOR, y=1.75, color=TEAL)
        self.play(FadeIn(restored), FadeOut(team), FadeOut(date),
                  FadeIn(check), run_time=0.82)
        self.play(check.animate.set_y(-1.90), run_time=2.04, rate_func=linear)
        self.play(FadeOut(check), run_time=0.33)
        dark = rna_lane(NORMAL, 1)
        faint = rna_lane(TUMOR, 0.35)
        self.at("VEGF")
        self.play(GrowFromCenter(dark[0]), GrowFromCenter(faint[0]),
                  FadeIn(gene_label(0)), run_time=0.79)
        self.at("PDGFB")
        self.play(GrowFromCenter(dark[1]), GrowFromCenter(faint[1]),
                  FadeIn(gene_label(1)), run_time=0.88)
        self.at("stayed high")
        light = scan(NORMAL, y=1.74)
        self.add(light)
        self.play(light.animate.set_y(-0.60), run_time=1.17, rate_func=linear)
        self.at("so did GLUT1")
        self.play(GrowFromCenter(dark[2]), GrowFromCenter(faint[2]),
                  FadeIn(gene_label(2)), FadeOut(light), run_time=0.81)
        self.finish()


class S10bClose(SpokenScene):
    def construct(self):
        left, right = lane_name("−VHL", NORMAL), lane_name("+VHL", TUMOR)
        tissue = tissue_label()
        self.add(rna_study(), rna_lane(NORMAL, 1), rna_lane(TUMOR, 0.35), left, right,
                 tissue, *[gene_label(i) for i in range(3)])
        self.at("held at 21")
        # Both 1% and 21% are schematic conditions, with each pair using the
        # same three RNA rows and the same band geometry as the preceding scene.
        conditions = VGroup(*[lane_name(text, x) for text, x in
                              zip(("1% O₂", "21% O₂", "21% O₂", "1% O₂"),
                                  (LADDER, NORMAL, TUMOR, CONTROL))])
        self.play(left.animate.move_to(at_xy((LADDER + NORMAL) / 2, 3.40)),
                  right.animate.move_to(at_xy((TUMOR + CONTROL) / 2, 3.40)),
                  FadeOut(tissue), run_time=0.52)
        self.play(FadeIn(conditions[1]), FadeIn(conditions[2]), run_time=0.30)
        self.at("and 1")
        self.play(FadeIn(lane(LADDER)), FadeIn(lane(CONTROL)),
                  FadeIn(conditions[0]), FadeIn(conditions[3]), run_time=0.72)
        self.play(FadeIn(rna_lane(LADDER, 1)), FadeIn(rna_lane(CONTROL, 0.94)), run_time=0.92)
        self.at("VHL is needed")
        light = VGroup(scan(TUMOR, y=1.76), scan(CONTROL, y=1.76))
        self.play(FadeIn(light), run_time=0.30)
        self.play(light.animate.shift(DOWN * 3.2), run_time=2.41, rate_func=linear)
        self.play(FadeOut(light), run_time=0.40)
        self.at("sorts the smear")
        self.clear()
        slab, track, blur = smear_stage()
        self.add(slab, track, blur, tag())
        smear_drift(blur)
        size = side("Size separates", 0.57, BLUE, 33)
        self.play(FadeIn(size), run_time=0.65)
        self.at("a probe names")
        identity = side("Probe identifies", -0.57, YELLOW, 33)
        self.play(Transform(slab, panel(True)), FadeOut(blur), FadeIn(film_bands()),
                  FadeIn(identity), run_time=1.02)
        self.finish()


class S11End(EndCard):
    LINE = "Gels sort DNA and RNA by size; probes reveal sequence identity."
