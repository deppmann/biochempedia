"""Mass spectrometry, from the sample inlet to a sequence read from mass gaps.

Colour map (as in the patch-clamp film): BLUE apparatus, GREY neutral material
and context, PURPLE electric field, YELLOW measured signal, GREEN agreement,
RED interference, TEAL and ORANGE contrasting sample identities, GOLD the
highlighted target. Peptide colours identify bead tokens, never structure.
"""
from bp_parts import *  # noqa: F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
CABINET = "#233C54"
SCREEN = "#172A3C"
WINDOW = "#1E3045"
METAL = "#56768E"
QUESTION = "Same peak — how to tell them apart?"
QUESTION_STYLE = dict(y=2.85, size=42)
SHARED = (68, 0.80, YELLOW)
ION_DATA = ((40, 2, .79, TEAL), (68, 1, .63, GOLD))
RESIDUES = (("Lys", 128.09496, GOLD), ("Gly", 57.02146, TEAL),
            ("Ser", 87.03203, PURPLE), ("Ala", 71.03711, ORANGE))


def xy(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, size=34, color=TEXT):
    return T(text, size, color).move_to(xy(x, y))


def panel(x, y, w, h, fill=CABINET, edge=METAL, radius=.24, stroke=2.5):
    return RoundedRectangle(width=w, height=h, corner_radius=radius,
                            stroke_color=edge, stroke_width=stroke, fill_color=fill,
                            fill_opacity=1).move_to(xy(x, y))


def arrow(a, b, color=BLUE):
    return Arrow(xy(*a), xy(*b), buff=0, color=color, stroke_width=4,
                 tip_length=.16, max_tip_length_to_length_ratio=.45)


def sphere(x, y, r=.19, color=GOLD, ring=False):
    disk = Circle(radius=r, stroke_color=color, stroke_width=2.5,
                  fill_color=color, fill_opacity=.85)
    glint = Dot(point=xy(-.24 * r, .27 * r), radius=.22 * r, color=TEXT).set_opacity(.6)
    bead = VGroup(disk, glint)
    if ring:
        bead.add(Circle(radius=r + .09, stroke_color=TEXT, stroke_width=3))
    return bead.move_to(xy(x, y))


def tube(x, y, w, h, liquid=.55):
    shell = panel(x, y, w, h, WINDOW, BLUE, min(.25, w / 3))
    level = Rectangle(width=w - .14, height=h * liquid, stroke_width=0,
                      fill_color=BLUE, fill_opacity=.23)
    level.move_to(xy(x, y - h / 2 + .075 + level.height / 2))
    rim = Line(xy(x - w * .39, y + h / 2 - .16), xy(x + w * .39, y + h / 2 - .16),
               color=BLUE, stroke_width=3)
    return VGroup(shell, level, rim)


def bench():
    """One bench, with the inlet, field chamber and detector fixed in frame."""
    chassis = panel(0, -.12, 12.96, 4.92)
    inlet = panel(-5.47, .05, 1.40, 3.85, WINDOW, radius=.16, stroke=0)
    chamber = panel(-2.63, .05, 3.90, 3.85, WINDOW, radius=.16, stroke=0)
    detector = panel(3.18, -.03, 6.06, 4.07, SCREEN, radius=.18)
    base = Line(xy(-6.15, -2.27), xy(6.15, -2.27), color=METAL, stroke_width=3)
    return VGroup(chassis, inlet, chamber, detector, base)


def stages():
    """Ion gate, collision opening and second analyzer in the same chamber."""
    rails = []
    for x, w, color in [(-4.34, .94, BLUE), (-3.08, 1.06, PURPLE), (-1.68, .84, BLUE)]:
        # Open-sided rails leave the flight path and fragment fan free.
        for y, flip in [(1.26, -1), (-1.29, 1)]:
            rails.append(VMobject(stroke_color=color, stroke_width=4).set_points_as_corners([
                xy(x, y + flip * .22), xy(x, y), xy(x + w, y), xy(x + w, y + flip * .22)]))
    return VGroup(*rails)


def lc_column():
    return tube(-5.47, .05, .72, 3.02, .82)


def spectrum(xr=(0, 100), axis="Mass / charge"):
    plot = Plot(box=(.57, 5.89, -1.35, 1.57), xr=xr, yr=(0, 1),
                xlabel=axis, color=GREY, label_size=28)
    plot.xlabel.shift(DOWN * .08)
    return plot


def peaks(plot, values, width=7):
    """Sticks use (m/z, relative height, color); intensities here are schematic."""
    return VGroup(*(Line(plot.pt(mz, 0), plot.pt(mz, h), stroke_color=c,
                         stroke_width=width) for mz, h, c in values))


def threshold(plot):
    return DashedLine(plot.pt(plot.xr[0] + 2, .45), plot.pt(plot.xr[1], .45),
                      dash_length=.13, dashed_ratio=.55, stroke_color=TEXT, stroke_width=2.5)


def scope(text="Schematic"):
    return scope_tag(text, size=28, color=TEXT).move_to(xy(4.67, -3.24))


def drifting_cloud(n, box, colors, seed, radii=(.12, .22)):
    rng = np.random.default_rng(seed)
    x, y, half_w, half_h = box
    cloud = VGroup()
    for i in range(n):
        phase = rng.uniform(0, TAU)
        px = x + rng.uniform(-half_w + .22, half_w - .22)
        py = y + rng.uniform(-half_h + .22, half_h - .22)
        bead = sphere(px, py, rng.uniform(*radii), colors[i % len(colors)])
        # Alternate clocks keep the drift legible without moving the apparatus.
        bob(bead, amp=.18 + .04 * (i % 3), speed=.8 + .18 * (i % 4), seed=phase)
        cloud.add(bead)
    return cloud


def flight(color=GOLD, count=5, start=-5.40, stop=-.94, y=.03, speed=1.2):
    """Keep the moving sample in the flight path while the labels settle."""
    beam = VGroup()
    for i in range(count):
        obj = sphere(0, 0, .15 + .035 * (i % 3), color)
        offset = .38 + i / count * (stop - start)
        obj.clock = 0.0

        def travel(mob, dt, offset=offset, i=i):
            mob.clock += dt
            d = (offset + mob.clock * speed) % (stop - start)
            mob.move_to(xy(start + d, y + .14 * np.sin(mob.clock * 2 + i)))
            # Fade through the launch and arrival apertures.
            mob.set_opacity(min(1, 2.5 * d, 2.5 * (stop - start - d)))

        obj.add_updater(travel, call_updater=True)
        beam.add(obj)
    return beam


def charged(kind, x, y, charge=1, r=.37):
    color = {"hex": TEAL, "diamond": ORANGE, "light": TEAL, "heavy": GOLD}[kind]
    if kind == "hex":
        shape = RegularPolygon(n=6, radius=r, color=color, fill_opacity=.85)
    elif kind == "diamond":
        shape = Square(side_length=r * 1.74, color=color, fill_opacity=.85).rotate(PI / 4)
    else:
        shape = sphere(0, 0, r, color)
    # The marks sit on the filled middle, away from the outline.
    sign = T("+" * charge, 29, BG, weight=BOLD).move_to(shape)
    return VGroup(shape, sign).move_to(xy(x, y))


def predict_world():
    p = spectrum()
    traces = peaks(p, [SHARED], 23)
    pair = VGroup(charged("hex", 3.73, 1.12), charged("diamond", 4.63, 1.12))
    mass = label("Same mass and charge", -2.88, -3.07, 30)
    return p, traces, pair, mass


def bead_chain(colors, r=.20, gap=.08):
    return VGroup(*(sphere(0, 0, r, c) for c in colors)).arrange(RIGHT, buff=gap)


def grow_peaks(scene, plot, values, seconds=1.2, width=7):
    bars = peaks(plot, values, width)
    scene.play(LaggedStart(*(Create(b) for b in bars), lag_ratio=.24),
               run_time=seconds)
    return bars


class S01Hook(SpokenScene):
    def construct(self):
        sample = tube(-2.30, -.10, 4.24, 5.06, .78)
        cloud = drifting_cloud(29, (-2.30, -.53, 1.85, 1.69), [TEAL, BLUE, GREY, PURPLE, ORANGE], 8)
        target = sphere(-2.10, .55, .40)
        bob(target, .19, 1.9)
        pulse(target[0], 4, 2.5, 2.6)
        question = label("?", -2.10, 2.95, 71, GOLD)
        self.add(sample, cloud, target, scope())

        self.at("so how do")
        self.play(FadeIn(question), run_time=.4)
        self.at("an enzyme assay")
        level = ValueTracker(.08)
        activity = dial(level, xy(3.38, -.20), radius=1.36, color=GREEN,
                        label="Activity", fmt="{:.0f}%", size=34)
        activity[3].clear_updaters().set_opacity(0)
        self.play(FadeIn(activity), run_time=.38)
        self.play(level.animate.set_value(.65), rate_func=linear, run_time=1.68)

        self.at("a gel sorts")
        self.play(FadeOut(activity), run_time=.3)
        gel = panel(3.39, -.22, 2.64, 4.34, WINDOW, BLUE)
        bands = VGroup(*(RoundedRectangle(width=w, height=.16, corner_radius=.05,
                        stroke_width=0, fill_color=c, fill_opacity=1).move_to(xy(3.39, 1.12 - i * .26))
                        for i, (w, c) in enumerate([(1.17, BLUE), (1.90, PURPLE), (1.49, GOLD), (.94, TEAL)])))
        self.play(FadeIn(gel), FadeIn(bands), run_time=.4)
        self.play(*(b.animate.move_to(xy(3.39, y)) for b, y in zip(bands, [1.1, .42, -.52, -1.47])),
                  run_time=1.7)
        self.at("Neither names")
        gel_question = label("?", 5.39, -.52, 66, GOLD)
        self.play(swap(question, gel_question, run_time=.58))
        pulse(bands[2], 2.5, 1.3, 2.8).set_stroke(GOLD, opacity=.9)

        self.at("Mass spectrometry")
        cloud.clear_updaters(recursive=True)
        target.clear_updaters(recursive=True)
        instrument = bench()
        target.set_z_index(1)
        self.play(FadeOut(gel_question), run_time=.22)
        self.play(FadeOut(cloud), FadeOut(bands), FadeOut(sample),
                  FadeIn(instrument), gel.animate.stretch_to_fit_width(1.24).move_to(xy(-5.47, .05)),
                  target.animate.move_to(xy(-5.47, .55)).scale(.63), run_time=1.15)
        self.remove(gel)
        self.play(target.animate.move_to(xy(-4.99, .05)), run_time=1.2)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Mass Spectrometry"
    TITLE = "Weighing Molecules to Name Them"

    def construct(self):
        instrument = bench()
        moving = flight(start=-5.55, stop=-4.47, count=1)
        title = label(self.TITLE, 0, 2.91, 49)
        lesson = label(self.LESSON, 0, -3.13, 32, BLUE)
        base = instrument.copy().set_opacity(.44)
        self.add(base, moving)
        self.play(FadeIn(title), FadeIn(lesson), run_time=.36)
        self.wait(.81)
        self.play(FadeOut(title), FadeOut(lesson), Transform(base, instrument), run_time=.64)
        self.wait(max(.07, self.narration_s - self.elapsed()))


class S03IonizeWeigh(SpokenScene):
    def construct(self):
        p = spectrum()
        plates = VGroup(*(Line(xy(-4.29, y), xy(-.95, y), stroke_color=PURPLE,
                              stroke_width=8) for y in (-1.43, 1.47)))
        for plate in plates:
            pulse(plate, 8, 2, 2.4)
        neutral = flight(GREY, 4, start=-4.28, stop=-.97, speed=1.42)
        self.add(bench(), p, plates, neutral, scope())
        self.at("adds a charge")
        a = charged("light", -4.04, -.28, 2, .35)
        b = charged("heavy", -4.04, .53, 1, .35)
        neutral.clear_updaters(recursive=True)
        self.play(FadeOut(neutral), run_time=.22)
        self.play(FadeIn(a), FadeIn(b), run_time=.40)
        ions = label("Ions", -2.66, 2.89, 36, BLUE)
        self.at("make ions")
        self.play(FadeIn(ions), run_time=.4)
        field = VGroup(*(arrow((x, 1.37), (x, .95), PURPLE) for x in (-2.78, -1.79)))
        self.at("More charge")
        self.play(FadeIn(field), run_time=.3)
        # Constant field: for equal transit time the transverse deflection is
        # proportional to q/m. Show greater deflection for the lighter double ion.
        def track(x, y, mass, charge, span):
            return ParametricFunction(lambda t: xy(x + span*t, y - 5.5*charge/mass*t*t),
                                      t_range=[0, 1], color=PURPLE)
        self.play(MoveAlongPath(a, track(-4.04, -.28, 40, 2, 2.04)),
                  run_time=1.75, rate_func=linear)
        self.at("while more mass")
        self.play(MoveAlongPath(b, track(-4.04, .53, 68, 1, 2.04)),
                  run_time=2.05, rate_func=linear)
        self.at("analyzer sorts ions")
        plates.clear_updaters(recursive=True)
        self.play(FadeOut(field), FadeOut(plates), FadeIn(stages()), run_time=.52)
        self.at("mass divided by")
        formula = label("mass / charge", -2.65, 2.89, 37, BLUE)
        self.play(swap(ions, formula, run_time=.65))
        self.play(a.animate.move_to(xy(-1.17, -.51)), b.animate.move_to(xy(-1.17, .41)), run_time=1.46)
        self.at("Each ratio produces")
        signal = peaks(p, [(m / q, h, c) for m, q, h, c in ION_DATA], width=28)
        self.play(FadeOut(a), FadeOut(b), run_time=.20)
        self.play(LaggedStart(*(Create(bar) for bar in signal), lag_ratio=.24),
                  swap(formula, label("Schematic spectrum", 3.18, 2.89), run_time=.67),
                  run_time=1.90, rate_func=linear)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        p, trace, pair, mass = predict_world()
        previous = peaks(p, [(m / q, h, c) for m, q, h, c in ION_DATA], width=28)
        previous_title = label("Schematic spectrum", 3.18, 2.89)
        self.add(bench(), stages(), p, previous, previous_title, scope())
        self.at("One peak is")
        self.play(FadeOut(previous), FadeOut(previous_title), run_time=.35)
        self.play(Create(trace[0]), run_time=2.35, rate_func=linear)
        pulse(trace[0], 23, 5, 2.1)
        a, b = pair
        ends = [m.get_center().copy() for m in pair]
        a.move_to(xy(-4, .47))
        b.move_to(xy(-4, -.47))
        self.at("Suppose two different")
        self.play(FadeIn(pair), run_time=.38)
        self.play(pair.animate.shift(RIGHT * 1.35), run_time=1.60)
        self.at("same mass and charge")
        self.play(FadeIn(mass), pair.animate.shift(RIGHT * 1.70), run_time=2.10)
        self.at("Both land on")
        self.play(FadeOut(pair, shift=RIGHT*.41), run_time=.46)
        a.move_to(ends[0])
        b.move_to(ends[1])
        self.play(FadeIn(pair, shift=DOWN*.14), run_time=.66)
        trace[0].clear_updaters().set_stroke(width=23)
        self.at("How can a mass")
        self.play(FadeIn(question_card(QUESTION, **QUESTION_STYLE)), run_time=.56)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    SECONDS = 4.5

    def backdrop(self):
        return VGroup(bench(), stages(), *predict_world(), scope())

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        timer = Rectangle(width=8.8, height=.22, fill_color=GOLD, fill_opacity=1,
                          stroke_width=0).move_to(xy(-1, -3.59))
        left = timer.get_left()
        timer.stretch(.005, 0, about_point=left)
        self.play(timer.animate.stretch(200, 0, about_point=left),
                  run_time=self.SECONDS, rate_func=linear)


class S06Tandem(SpokenScene):
    def construct(self):
        p, shared, pair, mass = predict_world()
        q = question_card(QUESTION, **QUESTION_STYLE)
        apparatus = stages()
        self.add(bench(), apparatus, p, shared, pair, mass, q, scope())
        self.at("Break them apart")
        self.play(FadeOut(q), FadeOut(mass), FadeOut(shared),
                  FadeOut(pair), run_time=.45)
        pair[0].move_to(xy(-4.03, .41))
        pair[1].move_to(xy(-4.03, -.44))
        self.play(FadeIn(pair, shift=LEFT*.40), run_time=.60)
        self.play(pair.animate.shift(RIGHT*.37), run_time=1.76, rate_func=linear)
        self.at("In tandem mass")
        title = label("Tandem MS", 0, 2.83, 42, BLUE)
        self.play(FadeIn(title), run_time=.5)

        self.at("first stage isolates")
        others = VGroup(sphere(-4.04, -.77, .12, GREY), sphere(-4.1, .77, .12, GREY))
        gate = Line(xy(-3.11, -.90), xy(-3.11, .89), stroke_color=PURPLE, stroke_width=5)
        stage1 = label("Stage 1", -3.95, -3.03, 31, BLUE)
        self.play(FadeIn(others), Create(gate), FadeIn(stage1), run_time=.45)
        self.play(FadeOut(others), FadeOut(gate), run_time=.30)
        self.play(pair.animate.shift(RIGHT * 1.08), run_time=.87)
        self.at("shatters its ions")
        flash = Circle(radius=.86, color=PURPLE, stroke_width=5).move_to(xy(-2.59, 0))
        glow = Circle(radius=.80, color=PURPLE, fill_opacity=.35,
                      stroke_width=4).move_to(flash)
        collision = label("Collision cell", -2.66, -3.03, 31, PURPLE)
        self.play(FadeIn(glow), ShowPassingFlash(flash, time_width=.74),
                  swap(stage1, collision, run_time=.85), run_time=.85)
        data = [(13, .51, TEAL), (25, .79, TEAL), (35, .61, TEAL), (47, .68, ORANGE), (62, .82, ORANGE)]
        fragments = VGroup(*(Triangle(color=c, fill_opacity=.92).rotate(i*.9).scale(.26 + .015*i)
                             .move_to(xy(-2.60, .28 if c == TEAL else -.40))
                             for i, (_, _, c) in enumerate(data)))
        self.play(FadeOut(pair), run_time=.23)
        self.play(FadeIn(fragments), run_time=.34)
        self.at("Different molecules usually")
        exits = [xy(x, y) for x, y in [(-2.22, .62), (-1.72, .16), (-1.12, .59),
                                      (-1.66, -.35), (-.99, -.64)]]
        paths = VGroup(*(Line(f.get_center(), end, color=color, stroke_width=15,
                              stroke_opacity=.76)
                         for f, end, (_, _, color) in zip(fragments, exits, data)))
        self.play(FadeOut(glow, scale=1.14), *(Create(path) for path in paths),
                  *(f.animate.move_to(end) for f, end in zip(fragments, exits)),
                  run_time=2.64, rate_func=linear)

        self.at("second stage weighs")
        stage2 = label("Stage 2", -1.27, -3.03, 31, BLUE)
        self.play(swap(collision, stage2, run_time=.65), FadeOut(paths),
                  *(f.animate.move_to(xy(-.53, .80 - .40*i)).scale(.60)
                    for i, f in enumerate(fragments)), run_time=1.03)
        self.play(FadeOut(fragments), run_time=.28)
        spec_title = label("Schematic fragment spectra", 3.17, 2.88, 31)
        self.play(swap(title, spec_title, run_time=.55))
        bars = grow_peaks(self, p, data, 1.75, width=28)
        self.at("identifies molecules")
        for i, bar in enumerate(bars):
            pulse(bar, 28, 7, 1.7 + .37*i)
        self.play(LaggedStart(*(bar.animate(rate_func=there_and_back)
                                .scale(1.30, about_point=bar.get_start()) for bar in bars),
                              lag_ratio=.48), run_time=3.85)
        self.finish()


class S07Sequencing(SpokenScene):
    def construct(self):
        # Singly protonated y ions: cumulative residue masses plus H2O and H+.
        # Residue masses from Medzihradszky & Chalkley, PMC4367481, Table 1.
        masses = np.cumsum([m for _, m, _ in RESIDUES]) + 19.01784
        colors = [c for _, _, c in RESIDUES]
        p = spectrum((112, 380))
        peptide = bead_chain(colors[::-1])
        tail = bead_chain([BLUE, GREY, TEAL, PURPLE])
        head = bead_chain([PURPLE, BLUE, GREY])
        chain = VGroup(head, peptide, tail).arrange(RIGHT, buff=.08).move_to(xy(-3.04, .53))
        self.add(bench(), p, chain, scope())
        self.at("the enzyme trypsin")
        snip = label("Trypsin", -3.60, 2.88, 35, BLUE)
        blades = VGroup()
        for edge in [head.get_right()[0]+.04, peptide.get_right()[0]+.04]:
            blades.add(VGroup(*(Line(xy(edge + dx, 1.27), xy(edge, .82), color=TEXT, stroke_width=4)
                                for dx in (-.15, .15))))
        self.play(FadeIn(blades), FadeIn(snip), run_time=.5)
        self.at("cuts it into")
        self.play(blades.animate.shift(DOWN * .32), run_time=.43)
        self.play(FadeOut(blades), head.animate.shift(UP * .56),
                  tail.animate.shift(DOWN * .71), run_time=.55)
        tag = label("Peptides", -3.60, 2.88, 35, BLUE)
        self.play(swap(snip, tag, run_time=.64))

        self.at("first stage selects")
        self.play(FadeOut(head), FadeOut(tail), FadeOut(tag),
                  peptide.animate.move_to(xy(-4.16, .04)), run_time=.76)
        self.play(FadeIn(stages()), peptide.animate.move_to(xy(-2.65, .04)), run_time=1.43)
        self.at("breaks it into")
        ladder = VGroup(*(bead_chain(colors[:n][::-1], r=.16) for n in (4, 3, 2, 1)))
        ladder.arrange(DOWN, buff=.22, aligned_edge=RIGHT).move_to(xy(-2.52, -.03))
        self.play(FadeOut(peptide), LaggedStart(*(FadeIn(f, shift=RIGHT*.3) for f in ladder),
                                                lag_ratio=.42), run_time=1.63)
        self.at("each one amino acid shorter")
        bar_data = list(zip(masses, (.58, .63, .72, .78), [YELLOW]*4))
        self.play(ladder.animate.shift(RIGHT*.63), run_time=1.13)
        bars = grow_peaks(self, p, bar_data, 1.42)

        self.at("Subtracting neighboring masses")
        formula = label("Mass gap = one amino acid’s mass", 1.04, 2.87, 35)
        self.play(FadeIn(formula), run_time=.42)
        annotations = VGroup()
        for i in range(3):
            x1, x2 = [p.pt(masses[j], 1)[0] for j in (i, i+1)]
            bracket = VMobject(stroke_color=colors[i+1], stroke_width=3).set_points_as_corners([
                xy(x1, .99), xy(x1, 1.13), xy(x2, 1.13), xy(x2, .99)])
            annotations.add(bracket)
        self.play(LaggedStart(*(Create(bracket) for bracket in annotations), lag_ratio=.37),
                  run_time=1.37)
        self.at("each amino acid in order")
        names = VGroup(*(label(RESIDUES[i+1][0], annotations[i].get_x(), 1.48,
                                29, colors[i+1]) for i in range(3)))
        self.play(LaggedStart(*(FadeIn(n, shift=UP*.09) for n in names), lag_ratio=.5), run_time=1.48)

        self.at("Two amino acids")
        same_mass = label("Same mass", -3.04, 2.87, 36, GOLD)
        self.play(FadeOut(ladder), FadeOut(bars), FadeOut(annotations), FadeOut(names),
                  swap(formula, same_mass, run_time=.62), run_time=.62)
        twins = VGroup(sphere(-3.72, .31, .39, TEAL), sphere(-1.89, .31, .39, ORANGE))
        tags = VGroup(label("Leucine", -3.72, -.38, 29, TEAL),
                      label("Isoleucine", -1.89, -.38, 29, ORANGE))
        self.play(FadeIn(twins), run_time=.4)
        self.at("weigh exactly")
        self.play(FadeIn(tags), *(Indicate(b, scale_factor=1.15, color=c)
                                  for b, c in zip(twins, [TEAL, ORANGE])), run_time=1.03)
        self.finish()


class S08Separation(SpokenScene):
    def construct(self):
        p = spectrum()
        target = sphere(-5.35, .08, .24, GOLD)
        bob(target, .13, 2.0)
        albumin = drifting_cloud(23, (-3.27, .05, 1.15, 1.37), [GREY], 21, (.12, .21))
        self.add(bench(), p, albumin, target, scope())
        self.at("Fasting blood holds")
        insulin = label("Insulin", -5.37, 2.86, 33, GOLD)
        self.play(FadeIn(insulin), run_time=.45)
        concentration = label("A few tens of picomolar", -3.92, -3.08, 30, GOLD)
        self.play(FadeIn(concentration), run_time=.52)

        self.at("Albumin outnumbers")
        tag = label("Albumin", -2.32, 2.86, 33, GREY)
        ratio = label("Roughly 10 million to 1", -3.77, -3.08, 32)
        self.play(FadeIn(tag), swap(concentration, ratio, run_time=.64), run_time=.64)

        self.at("drown its signal")
        albumin.clear_updaters(recursive=True)
        target.clear_updaters(recursive=True)
        self.play(FadeOut(albumin, shift=RIGHT*.8), FadeOut(target, shift=RIGHT*.8), run_time=.65)
        interference = grow_peaks(self, p, [(65, .95, GREY), (54, .036, GOLD)], 1.18, width=12)

        self.at("liquid chromatography")
        col = lc_column()
        title = label("Liquid chromatography", -3.18, 2.86, 37, BLUE)
        self.play(FadeOut(insulin), FadeOut(tag), FadeOut(ratio), FadeOut(interference),
                  FadeIn(col, shift=UP*.3), run_time=.56)
        self.play(FadeIn(title), run_time=.45)
        first = VGroup(*(sphere(-5.47, y, .18, GREY) for y in (.62, .19, -.23)))
        later = sphere(-5.47, 1.08, .23, GOLD)
        self.play(FadeIn(first), FadeIn(later), run_time=.35)
        self.play(first.animate.shift(DOWN*.75), later.animate.shift(DOWN*.28), run_time=1)
        self.at("feeding compounds in", lead=.76)
        self.play(first.animate.arrange(RIGHT, buff=.30).move_to(xy(-3.43, .03)),
                  later.animate.shift(DOWN*1.29), run_time=.43)
        grey = peaks(p, [(65, .86, GREY)], width=24)
        self.play(Create(grey[0]), FadeOut(first, shift=RIGHT*.76), run_time=.27)
        self.play(FadeOut(grey), later.animate.move_to(xy(-2.3, .02)).scale(1.40), run_time=.36)
        self.play(FadeOut(later, shift=RIGHT*.35), run_time=.22)
        self.play(Create(peaks(p, [(54, .76, GOLD)], width=31)[0]),
                  FadeIn(label("Insulin", 3.18, 2.86, 33, GOLD)), run_time=.56)
        self.finish()


def limit_world():
    p = spectrum()
    return p, threshold(p)


class S09LimitsControl(SpokenScene):
    def construct(self):
        p, floor = limit_world()
        violet = label("Detection limit", 3.21, 2.87, 41)
        signal = peaks(p, [(62, .20, GOLD)], width=10)
        dots = flight(GOLD, 3, start=-5.35, stop=-.91, speed=1.04)
        apparatus = stages()
        last = peaks(p, [(54, .76, GOLD)], width=31)
        insulin = label("Insulin", 3.18, 2.86, 33, GOLD)
        self.add(bench(), lc_column(), apparatus, p, dots, last, insulin, scope())
        self.at("A missing peak")
        self.play(FadeOut(last), FadeOut(insulin), run_time=.65)
        self.play(Create(signal[0]), run_time=1.05)
        self.at("Every instrument has")
        self.play(Create(floor), run_time=1.06)
        self.at("detection limit")
        self.play(FadeIn(violet), run_time=.48)
        pulse(signal[0], 9, 3.3, 2.4)
        self.at("Not detected means")
        below = label("Below limit, not zero", 2.81, -.33, 33, GOLD)
        self.play(FadeIn(below), run_time=.54)
        signal[0].clear_updaters()
        self.play(FadeOut(signal), run_time=2.25)
        self.at("studies report their")
        self.play(FadeOut(below), floor.animate.set_stroke(width=4), run_time=.79)

        self.at("Strong claims also")
        dots.clear_updaters(recursive=True)
        self.play(FadeOut(dots), FadeOut(apparatus), FadeOut(violet), run_time=.42)
        control_value = ValueTracker(.12)
        control = dial(control_value, xy(-2.64, -.25), radius=1.35, color=GREEN,
                       label="Second method", fmt="{:.0f}", scale=1.0, size=31)
        # The needle is the schematic readout. The narration gives no numerical reading.
        control[3].clear_updaters().set_opacity(0)
        self.play(FadeIn(control, shift=UP*.30), run_time=.54)
        self.at("two methods")
        bars = peaks(p, [(62, .79, GREEN)], 23)
        self.play(control_value.animate.set_value(.77), Create(bars[0]),
                  run_time=1.60, rate_func=linear)
        self.at("agree")
        agree = label("Agreement", -.72, -3.04, 34, GREEN)
        self.play(FadeIn(agree), Indicate(bars[0], color=GREEN, scale_factor=1.04), run_time=.82)
        self.finish()


def vial(color=GOLD):
    body = tube(0, 0, .48, 1.07, .44)
    cap = RoundedRectangle(width=.47, height=.19, corner_radius=.05,
                           fill_color=BLUE, fill_opacity=1, stroke_width=0).move_to(xy(0, .48))
    bead = sphere(0, -.26, .12, color)
    return VGroup(body, cap, bead).move_to(xy(-5.47, .16))


class S10UnlockedDrug(SpokenScene):
    def construct(self):
        p, floor = limit_world()
        col = lc_column()
        lc = label("Liquid chromatography", -3.40, 2.89, 36, BLUE)
        dose = label("Isoguvacine", 3.18, .91, 42, GOLD)
        amount = label("20 mg/kg", 3.18, -.61, 36)
        self.add(bench(), col, p, floor, scope())
        sample = vial()
        sample.scale(1.8).move_to(xy(-3.00, .13))
        self.play(FadeIn(sample, shift=UP*.44), run_time=.74)
        self.at("Male mice received")
        self.play(FadeIn(dose), run_time=.51)
        self.at("20 milligrams per")
        self.play(FadeIn(amount), sample.animate.scale(.71), run_time=1.52)
        self.at("Liquid chromatography")
        self.play(FadeOut(dose), FadeOut(amount), FadeOut(sample), run_time=.43)
        self.play(FadeIn(lc), FadeIn(stages()), run_time=.43)
        stream = flight(GREY, 4, start=-5.35, stop=-.86)
        self.add(stream)

        def load_sample(name, color, label_y, signal=None):
            container = vial(color).scale(.60).move_to(xy(-6.02, 1.95))
            tag = label(name, 3.15, label_y, 31, color)
            self.play(FadeIn(container), FadeIn(tag), run_time=.18)
            self.play(container.animate.move_to(xy(-5.47, 1.84)).scale(.70), run_time=.30)
            feed = sphere(-5.47, 1.47, .11, color)
            self.add(feed)
            readout = [Create(signal)] if signal is not None else []
            self.play(FadeOut(container), FadeOut(feed, shift=DOWN*.67), *readout, run_time=.24)
            return tag

        detected = peaks(p, [(63, .84, GOLD)], width=10)[0]
        undetected = Line(p.pt(4, .045), p.pt(99, .045), color=GREY, stroke_width=4)
        self.at("in blood")
        blood = load_sample("Blood", GOLD, 3.22, detected)
        self.at("liver")
        liver = load_sample("Liver", GOLD, 2.71)
        self.at("not detected", lead=.10)
        self.play(FadeOut(blood), FadeOut(liver), FadeOut(detected), run_time=.24)
        self.at("in brain")
        brain = load_sample("Brain", TEXT, 3.22, undetected)
        self.at("or cerebrospinal")
        fluid = load_sample("Cerebrospinal fluid", TEXT, 2.71)
        self.at("Detection limits were")
        self.play(FadeOut(brain), FadeOut(fluid), FadeOut(undetected), run_time=.37)
        limit = label("Detection limits", 3.16, 2.88, 36)
        self.play(FadeIn(limit), run_time=.45)
        flu = label("640 picomolar (fluids)", 3.38, .45, 32, BLUE)
        tis = label("16 nanomolar (tissue)", 3.38, 1.19, 32, BLUE)
        self.at("640 picomolar")
        self.play(FadeIn(flu), run_time=.55)
        self.at("16 nanomolar")
        self.play(FadeIn(tis), run_time=.55)
        self.finish()


def heel_drop():
    drop = VMobject(stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=.95)
    drop.start_new_path(xy(0, .98))
    drop.add_cubic_bezier_curve_to(xy(-.22, .62), xy(-.74, .08), xy(-.68, -.28))
    drop.add_cubic_bezier_curve_to(xy(-.61, -1.02), xy(.61, -1.02), xy(.68, -.28))
    drop.add_cubic_bezier_curve_to(xy(.74, .08), xy(.22, .62), xy(0, .98))
    glint = Dot(xy(-.28, -.15), radius=.11, color=TEXT).set_opacity(.74)
    return VGroup(drop, glint).move_to(xy(-3.51, .37))


def clock_gauge(x, y):
    radius = .86
    center = xy(x, y)
    rim = Circle(radius=radius, stroke_color=BLUE, stroke_width=5).move_to(center)
    ticks = VGroup(*(Line(center + .74*v, center + .82*v, stroke_color=GREY, stroke_width=4)
                     for v in [UP, DOWN, LEFT, RIGHT]))
    minute = Line(center, center + UP*.61, stroke_color=GOLD, stroke_width=4)
    hour = Line(center, center + RIGHT*.41 + UP*.11, stroke_color=TEXT, stroke_width=5)
    return VGroup(rim, ticks, hour, minute), minute


class S11UnlockedMcad(SpokenScene):
    def construct(self):
        p = spectrum()
        apparatus = stages()
        drop = heel_drop().scale(.78).move_to(xy(-3.28, .03))
        bob(drop, .12, 1.54)
        drop.add_updater(lambda mob: mob.shift(RIGHT * .63 * np.sin(1.2 * self.time)))
        self.add(bench(), apparatus, p, drop, scope())
        self.at("serves newborn screening")
        newborn = label("Newborn heel prick", -3.21, 2.88, 36, GOLD)
        self.play(FadeIn(newborn), run_time=.50)
        self.at("MCAD deficiency")
        mcad = label("MCAD deficiency", 3.22, 2.88, 36, TEAL)
        self.play(FadeIn(mcad), run_time=.52)
        self.at("a missing fat")
        self.play(Indicate(drop, color=GOLD, scale_factor=1.14), run_time=1.35)
        self.at("affects roughly")
        frequency = label("1 in 10,000–20,000 births", -3.43, -3.12, 33)
        self.play(FadeIn(frequency), run_time=.62)
        self.at("A heel prick read")
        drop.clear_updaters(recursive=True)
        self.play(FadeOut(frequency), FadeOut(newborn),
                  drop.animate.move_to(xy(-5.47, .04)).scale(.43), run_time=.67)
        self.play(drop.animate.move_to(xy(-3.02, .04)).scale(.64), run_time=1.07)
        trace = [(28, .24, TEAL), (48, .39, TEAL), (69, .83, GOLD), (86, .31, TEAL)]
        children = VGroup(*(sphere(-3.0, .03, .16, c) for _, _, c in trace))
        self.play(FadeOut(drop), FadeIn(children), run_time=.27)
        self.play(*(m.animate.move_to(xy(-.92, .73-i*.48)) for i, m in enumerate(children)),
                  run_time=.94)
        self.play(FadeOut(children), run_time=.22)
        bars = grow_peaks(self, p, trace, .89)
        self.play(swap(mcad, label("Flags MCAD deficiency", 3.20, 2.88, 34, GOLD), run_time=.59))
        self.at("A few babies")
        timer, hand = clock_gauge(-2.64, .06)
        self.play(FadeOut(apparatus), FadeIn(timer), run_time=.54)
        self.play(Rotate(hand, angle=-TAU*.84, about_point=xy(-2.64, .06)), run_time=2.78, rate_func=linear)
        pulse(bars[2], 8.5, 2, 2.1)
        self.finish()


class S12UnlockedTurnover(SpokenScene):
    def construct(self):
        p = spectrum()
        normal = sphere(-4.06, .26, .52, GREY)
        heavy = sphere(-1.77, .26, .53, GOLD, ring=True)
        bob(normal, .36, 1.49)
        bob(heavy, .36, 1.21, seed=2)
        normal_tag = label("Normal nitrogen", -4.38, 2.87, 31, GREY)
        heavy_tag = label("Heavy nitrogen tag", -.19, 2.87, 32, GOLD)
        ordinary = peaks(p, [(42, .72, GREY)], 9)
        # 15N and 14N differ in mass. The horizontal shift is enlarged in
        # this schematic, which has no numeric m/z ticks.
        tagged = peaks(p, [(52, .72, GOLD)], 9)
        self.add(bench(), p, normal, heavy, scope())
        self.at("Heavy nitrogen weighs")
        self.play(FadeIn(normal_tag), FadeIn(heavy_tag), run_time=.54)
        self.at("weighing tracks it")
        self.play(Create(ordinary[0]), run_time=.8)
        self.play(Create(tagged[0]), run_time=1.14)

        self.at("In the 1930s")
        history = label("Schoenheimer, 1930s", -3.53, 2.86, 37)
        normal.clear_updaters(recursive=True)
        heavy.clear_updaters(recursive=True)
        self.play(FadeOut(normal), FadeOut(normal_tag),
                  swap(heavy_tag, history, run_time=.79), run_time=.79)
        self.at("fed rats nitrogen")
        self.play(heavy.animate.move_to(xy(-5.43, .07)).scale(.62), run_time=1.82)
        self.at("heavy tag entered")
        chains = VGroup(*(bead_chain([TEAL, PURPLE, BLUE, GREY], r=.22)
                          .move_to(xy(-2.61, y)) for y in (.95, .02, -.91)))
        self.play(FadeIn(chains, shift=RIGHT*.25), run_time=.50)
        tags = VGroup(*(heavy.copy() for _ in range(3)))
        self.remove(heavy)
        self.add(tags)
        self.play(LaggedStart(*(tag.animate.move_to(chain.get_left() + LEFT*.49)
                                for tag, chain in zip(tags, chains)), lag_ratio=.39),
                  run_time=2.13)
        self.at("dynamic state of")
        self.play(LaggedStart(*(row.animate.shift(RIGHT*dx)
                                for row, dx in zip([VGroup(c, t) for c, t in zip(chains, tags)],
                                                   (.62, .44, .70))), lag_ratio=.33),
                  run_time=2.29)
        self.at("turns hidden mixtures")
        self.play(FadeOut(history), FadeOut(chains), FadeOut(tags), FadeOut(ordinary),
                  FadeIn(stages()), FadeIn(lc_column()), run_time=.53)
        stream = flight(GOLD, 5, speed=1.48)
        self.add(stream)
        grow_peaks(self, p, [(27, .42, TEAL), (66, .53, ORANGE), (88, .81, PURPLE)], 1.14)
        sequence = bead_chain([ORANGE, PURPLE, TEAL, GOLD], r=.23).move_to(xy(-2.85, -3.10))
        self.play(FadeIn(sequence, shift=RIGHT*.25), run_time=.54)
        self.finish()


class S13End(EndCard):
    LINE = "Weighing charged ions and fragments identifies molecules\nand reads protein sequences."
