"""Seeing Structure, Reading Blood. Diagrams and illustrative data, not scan images."""

from bp_parts import *

# BLUE = scanner, field and electrodes. GREY/TEXT = anatomical structure.
# PURPLE = oxygen-poor blood. RED = oxygen-rich blood.
# Slate = lesions. Muted silver = rejected inference.
# ORANGE = cortical activity and BOLD. YELLOW = neural traces. GREEN = supported inference.
# GOLD = prediction question and study dates. TEAL = comparison region and recovery.
PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
METAL = "#414F61"
SULCUS = "#67758B"
WHITE_MATTER = "#C6CEDD"
CORTEX = "#8F9BAE"
LESION = "#263342"
REJECTED = "#B6B9C3"
SCANNER_AT = np.array([-3.55, 0.05, 0])
PATCH_AT = np.array([-2.86, 0.83, 0])
RIGHT_X = 3.15
QUESTION = "Does BOLD stay high or drop?"
PAUSE_CARD = dict(left=0.0, y=-2.73, size=31, max_w=6.25)


def xy(x, y):
    return np.array([x, y, 0])


def label(s, x=RIGHT_X, y=0, color=TEXT, size=32, width=6.1):
    return fit_text(s, max_w=width, size=size, min_size=28, max_lines=2, color=color).move_to(xy(x, y))


def outline(points, color, fill, stroke=3, opacity=1):
    return VMobject(stroke_color=color, stroke_width=stroke, fill_color=fill, fill_opacity=opacity
                    ).set_points_smoothly([xy(x, y) for x, y in points]).close_path()


def brain_slice(center=SCANNER_AT, scale=1.0):
    """Axial cartoon. The pial outline, white matter and sulci share one registration."""
    hemisphere = [
        (0.04, 1.32), (0.32, 1.47), (0.69, 1.39), (0.96, 1.21),
        (1.13, 0.97), (1.37, 0.66), (1.46, 0.29), (1.39, 0.04),
        (1.46, -0.24), (1.35, -0.55), (1.21, -0.77), (0.95, -1.01),
        (0.66, -1.30), (0.35, -1.34), (0.14, -1.18), (0.06, -0.93),
        (0.10, -0.45), (0.06, 0), (0.12, 0.35), (0.06, 0.77), (0.04, 1.32),
    ]
    shell, white, folds = VGroup(), VGroup(), VGroup()
    for side in (-1, 1):
        shell.add(outline([(side*x, y) for x, y in hemisphere], TEXT, CORTEX))
        white.add(outline([(side*(0.23 + 0.65*x), 0.72*y) for x, y in hemisphere],
                          WHITE_MATTER, WHITE_MATTER, stroke=1.4))
        for path in (
            [(0.55, 1.40), (0.53, 1.16), (0.75, 1.01), (0.86, 0.79)],
            [(1.18, 0.92), (1.03, 0.64), (1.07, 0.43), (0.92, 0.29)],
            [(1.40, 0.13), (1.20, 0.19), (1.08, -0.04), (0.83, -0.12)],
            [(1.28, -0.62), (1.04, -0.60), (0.93, -0.45), (0.69, -0.40)],
            [(0.92, -1.03), (0.77, -0.88), (0.55, -0.92), (0.47, -0.74)],
        ):
            folds.add(VMobject(stroke_color=SULCUS, stroke_width=3.2).set_points_smoothly(
                [xy(side*x, y) for x, y in path]))
    ventricle = outline([(0, 0.18), (0.35, 0.36), (0.50, 0.14), (0.32, -0.17),
                         (0, -0.06), (-0.32, -0.17), (-0.50, 0.14), (-0.35, 0.36),
                         (0, 0.18)], SULCUS, SULCUS, stroke=1.5)
    folds.add(ventricle)
    for layer in (shell, white, folds):
        layer.scale(scale, about_point=ORIGIN).shift(center)
    return VGroup(shell, white, folds)


def scanner():
    """Front view of the same scanner and table, with moving field sweeps inside the bore."""
    c = SCANNER_AT
    housing = Circle(radius=2.78, color=GREY, stroke_width=3, fill_color=METAL, fill_opacity=1).move_to(c)
    bezel = Circle(radius=2.52, color="#77869A", stroke_width=3, fill_color="#273647", fill_opacity=1).move_to(c)
    bore = Circle(radius=2.14, color=BLUE, stroke_width=2.5, fill_color="#172331", fill_opacity=1).move_to(c)
    table = VGroup(
        RoundedRectangle(width=3.25, height=0.22, corner_radius=0.10, color=GREY,
                         fill_color=METAL, fill_opacity=1).move_to(c+DOWN*1.51),
        Polygon(c+xy(-1.20,-1.62), c+xy(1.20,-1.62), c+xy(1.40,-2.55), c+xy(-1.40,-2.55),
                color=GREY, stroke_width=2, fill_color="#53647A", fill_opacity=1),
    )
    sweeps = VGroup(*[
        Arc(radius=r, start_angle=a, angle=span, arc_center=c, color=BLUE, stroke_width=w,
            stroke_opacity=o)
        for r, a, span, w, o in [(1.84, 0.2, 1.45, 6, .75), (1.99, 2.8, 1.1, 5, .68),
                                  (2.02, 5.2, .65, 5, .86), (1.82, 3.9, .55, 4, .47),
                                  (2.34, .55, 1.85, 15, .88), (2.34, 3.53, .74, 10, .60)]
    ])
    return VGroup(housing, bezel, bore, sweeps, table), sweeps


def scan_world(scene, anatomy=True, moving=True):
    housing, sweeps = scanner()
    brain = brain_slice()
    scene.add(housing, brain if anatomy else brain[0])
    if moving:
        sweeps.add_updater(lambda m, dt: m.rotate(dt * 0.71, about_point=SCANNER_AT))
    return brain


def glow(at=PATCH_AT, color=ORANGE, radius=0.49):
    return VGroup(*[
        Ellipse(width=2.2*r, height=1.58*r, stroke_width=0,
                fill_color=color, fill_opacity=opacity).rotate(-.36).move_to(at)
        for r, opacity in [(1.40*radius, .13), (1.13*radius, .23), (.85*radius, .52),
                           (.53*radius, .87)]
    ])


def breathing(mob, period=3.6):
    """Modulate the entire glow while its underlying cortical site stays fixed."""
    initial = mob.copy()
    clock = 0.0

    def update(m, dt):
        nonlocal clock
        clock += dt
        m.become(initial.copy().scale(1 + .21*np.sin(TAU*clock/period), about_point=initial.get_center()))

    return mob.add_updater(update)


def scan_line(brain):
    sweep = Line(brain.get_left(), brain.get_right(), color=BLUE, stroke_width=4)
    sweep.set_y(brain.get_top()[1] - 0.1)
    return sweep


def lesion(deep=False, center=SCANNER_AT, scale=1):
    c = center
    if deep:
        pts = [(0.97, 1.12), (0.79, 1.19), (0.62, 0.98), (0.40, 0.75),
               (0.33, 0.45), (0.47, 0.32), (0.74, 0.51), (0.96, 0.78), (0.97, 1.12)]
    else:
        pts = [(0.97, 1.12), (0.79, 1.19), (0.64, 1.11), (0.66, 0.96),
               (0.83, 0.91), (0.97, 1.12)]
    return outline([(c[0]+scale*x, c[1]+scale*y) for x, y in pts], GREY, LESION, stroke=3)


def scheme():
    return scope_tag("Schematic", size=28, color=TEXT)


class S01Hook(SpokenScene):
    def construct(self):
        brain = scan_world(self, anatomy=False)
        self.at("how can you")
        sweep = scan_line(brain)
        self.add(sweep)
        self.play(sweep.animate.set_y(brain.get_bottom()[1] + .1),
                  Create(brain[1]), run_time=4.0, rate_func=linear)
        self.play(FadeOut(sweep), Create(brain[2]), run_time=1.0)
        self.at("magnetic resonance")
        self.play(FadeIn(label("MRI", y=.5, size=59)), run_time=.65)
        self.at("pictures brain structure")
        self.play(FadeIn(label("Brain structure", y=-.27)), run_time=.55)
        self.at("functional mr")
        patch = glow()
        self.play(GrowFromCenter(patch), run_time=1.05)
        breathing(patch)
        self.at("glowing patches during")
        self.play(FadeIn(label("fMRI", y=-1.48, color=ORANGE, size=51)), run_time=.55)
        self.at("what do those")
        self.play(FadeIn(label("?", x=-.38, y=1.43, color=GOLD, size=62, width=1)), run_time=.55)
        self.finish()


class S02Title(TitleCard):
    LESSON = "MRI and functional MRI"
    TITLE = "Seeing Structure, Reading Blood"

    def construct(self):
        scan_world(self)
        self.add(glow())
        title = fit_text(self.TITLE.replace(", ", ",\n"), max_w=6.25, size=53, min_size=40,
                         max_lines=2, font=TITLE_FONT).move_to(xy(RIGHT_X, .65))
        lesson = label(self.LESSON, y=-.86, color=BLUE, size=29)
        self.play(FadeIn(title), FadeIn(lesson), run_time=.5)
        self.finish()


def bold_response(t):
    """Illustrative delayed onset with a smooth approach to a plateau."""
    u = max(0, (t-2.1)/2.25)
    return .13 + .79*(1 - (1+u)*np.exp(-u))


def mechanism_plot():
    return Plot(box=(.34, 6.15, -2.49, -.75), xr=(0, 10), yr=(0, 1.07),
                xlabel="Time", ylabel="BOLD signal", color=TEXT, label_size=28)


def capillary():
    vessel = RoundedRectangle(width=5.75, height=1.15, corner_radius=.53,
                              stroke_color="#AA5262", stroke_width=3, fill_color="#3E2538",
                              fill_opacity=1).move_to(xy(3.19, 1.52))
    return vessel


def disc(color, x, y):
    outer = Ellipse(width=.46, height=.29, stroke_color=color, stroke_width=2.5,
                    fill_color=color, fill_opacity=.75).rotate(.30).move_to(xy(x,y))
    inner = Ellipse(width=.24, height=.10, stroke_width=0,
                    fill_color="#392538", fill_opacity=.54).rotate(.30).move_to(outer)
    return VGroup(outer, inner)


def blood_flow(scene, oxygenated, speed=.8):
    """Red-cell discs travel along two lanes inside the vessel, wrapping at the lumen ends."""
    cells = VGroup()
    left, span = .63, 5.13
    for i, rich in enumerate(oxygenated):
        x = left + i * span / len(oxygenated)
        y = 1.52 + (1 if i % 2 else -1)*.18
        cell = disc(RED if rich else PURPLE, x, y)

        def advance(m, dt):
            m.set_x(left + (m.get_x() - left + dt*speed) % span)

        cell.add_updater(advance)
        cells.add(cell)
    scene.add(cells)
    return cells


def hemoglobin_transition(cell, start, end):
    """Change the disc's color while its flow updater keeps it moving."""
    start, end = ManimColor(start), ManimColor(end)

    def recolor(outer, alpha):
        color = interpolate_color(start, end, alpha)
        outer.set_fill(color).set_stroke(color)

    return UpdateFromAlphaFunc(cell[0], recolor)


def magnetic_field(strength):
    field = VGroup()
    for i, y in enumerate([.67, .96, 2.07, 2.34]):
        x = np.linspace(.40, 6, 100)
        bend = strength*.16*np.exp(-((x-2.9)/1.35)**2)*np.sin(4*x+i*.32)
        field.add(VMobject(stroke_color=BLUE, stroke_width=2.3, stroke_opacity=.72
                          ).set_points_as_corners([xy(a,b) for a,b in zip(x, y+bend)]))
    return field


def synapses():
    terminals = VGroup()
    for x in (1.1, 2.35, 3.8, 5.12):
        terminals.add(VGroup(
            Line(xy(x-.23, 2.72), xy(x, 2.55), color=YELLOW, stroke_width=3),
            Dot(xy(x, 2.55), radius=.075, color=YELLOW),
            Line(xy(x+.12, 2.51), xy(x+.36, 2.64), color=YELLOW, stroke_width=3),
        ))
    return terminals


class S03HowItWorks(SpokenScene):
    def construct(self):
        brain = scan_world(self)
        self.add(scheme())
        gray = label("Gray matter", y=1.53, color=GREY, size=37)
        white = label("White matter", y=.52, color=WHITE_MATTER, size=37)
        dark = label("Lesions", y=-.49, color=TEXT, size=37)
        self.at("maps gray matter")
        self.play(FadeIn(gray), brain[0].animate.set_fill("#62738B"), run_time=.5)
        self.at("white matter")
        self.play(FadeIn(white), brain[0].animate.set_fill(CORTEX),
                  brain[1].animate.set_fill("#F7F9FF"), run_time=.5)
        self.at("and lesions")
        mark = lesion()
        self.play(FadeIn(mark), brain[1].animate.set_fill(WHITE_MATTER), run_time=.35)
        self.play(FadeIn(dark), run_time=.5)
        self.at("functional mr")
        self.play(FadeOut(VGroup(gray, white, dark, mark)), run_time=.42)
        patch = glow()
        vessel = capillary()
        field = magnetic_field(0)
        self.play(FadeIn(patch), FadeIn(vessel), Create(field), run_time=.85)
        breathing(patch)
        mixed = [False, False, True, False, True]
        cells = blood_flow(self, mixed)
        deoxygenated = [cell for cell, rich in zip(cells, mixed) if not rich]
        self.at("oxygen poor hemoglobin")
        deoxy = label("Deoxyhemoglobin", y=3.09, color=PURPLE, size=31)
        self.play(FadeIn(deoxy), run_time=.55)
        self.at("disturbs the scanner's")
        self.play(Transform(field, magnetic_field(1)), run_time=1.25)
        self.at("oxygen rich hemoglobin")
        oxy = label("Oxygen-rich hemoglobin", y=3.09, color=RED, size=31)
        self.play(swap(deoxy, oxy, run_time=.75), Transform(field, magnetic_field(.08)),
                  *[hemoglobin_transition(cell, PURPLE, RED) for cell in deoxygenated], run_time=.75)
        self.at("active regions receive")
        terminals = synapses()
        self.play(FadeIn(terminals), FadeOut(oxy), Transform(field, magnetic_field(.6)),
                  *[hemoglobin_transition(cell, RED, PURPLE) for cell in deoxygenated], run_time=.55)
        for terminal in terminals:
            pulse(terminal[0], base=3, amp=2.6, speed=5)
        self.at("more oxygenated blood")
        self.remove(cells)
        blood_flow(self, [True, True, True, True, False, True, True], speed=1.65)
        self.play(Transform(field, magnetic_field(.24)), run_time=1.7)
        self.at("that disturbance shrinks")
        self.play(Transform(field, magnetic_field(.08)), run_time=.7)
        self.at("seconds later")
        plot = mechanism_plot()
        self.play(FadeIn(plot), run_time=.55)
        t = ValueTracker(0)
        self.add(plot.live_curve(bold_response, t, color=ORANGE, width=6))
        self.play(t.animate.set_value(2.1), run_time=2.25, rate_func=linear)
        self.play(t.animate.set_value(9.7), run_time=3.04, rate_func=linear)
        self.finish()


def electrode():
    c = SCANNER_AT
    return VGroup(
        Line(c+xy(.84, 2.01), c+xy(.78, 1.23), color=BLUE, stroke_width=8),
        Line(c+xy(.78, 1.23), PATCH_AT+xy(.04, .12), color=TEXT, stroke_width=3),
    )


def smooth_step(x):
    x = np.clip(x, 0, 1)
    return x*x*(3-2*x)


def neural_signals():
    """Qualitative profiles for the stated long-stimulus case, in arbitrary units."""
    def synaptic(t):
        return .13+.72*smooth_step((t-1)/.9)

    def spikes(t):
        dt = max(0, t-1)
        return .13+.75*smooth_step(dt/.54)*np.exp(-max(dt-.54, 0)/1.5)

    def persistent(t):
        return .13+.72*smooth_step((t-2.4)/2.7)

    return synaptic, spikes, persistent


def experiment():
    """Scanner experiment and the three registered traces across the predict sequence."""
    plots = [
        Plot(box=(.12, 6.28, y, y+1.01), xr=(0, 10), yr=(0, 1.05), color=GREY, stroke=2)
        for y in (1.09, -.56, -2.21)
    ]
    funcs = neural_signals()
    colors = (YELLOW, YELLOW, ORANGE)
    names = ("Synaptic currents", "Spiking", "BOLD")
    labels = VGroup(*[label(n, x=1.80, y=y, color=c, size=28, width=3.38)
                      for n, y, c in zip(names, (2.38, .73, -.92), colors)])
    axes = VGroup(*plots)
    traces = VGroup(*[p.curve(f, x1=10 if i < 2 else 5.25, color=c, width=5)
                      for i,(p,f,c) in enumerate(zip(plots, funcs, colors))])
    p = plots[2]
    stim = Line(xy(.74, 3.14), xy(6.28, 3.14), stroke_width=8, color=BLUE)
    stim_label = label("Visual stimulus", x=2.46, y=3.51, color=TEXT, size=28, width=4.5)
    return axes, traces, labels, stim, stim_label


def add_prediction_world(scene, moving=False):
    scan_world(scene, moving=moving)
    probe = electrode()
    scene.add(glow(), probe, scheme())
    return probe


def prediction_question():
    return question_card(QUESTION, **PAUSE_CARD)


def candidate_paths(axes):
    p = axes[2]
    high = neural_signals()[2]
    drop = lambda t: high(5.25) - .66*smooth_step((t-5.25)/3.5)
    return VGroup(*[DashedVMobject(p.curve(fn, x0=5.25, color=ORANGE, width=3, opacity=.44),
                                   num_dashes=13) for fn in (high, drop)])


def bold_question_mark(axes):
    return label("?", x=axes[2].pt(5.25, .85)[0], y=-1.02, color=GOLD, size=38, width=.9)


class S04PredictSetup(SpokenScene):
    def construct(self):
        scan_world(self)
        patch = glow()
        self.add(patch, scheme())
        breathing(patch)
        axes, traces, names, stim, stim_label = experiment()
        self.at("because bold reads")
        link = label("Which neural signal?", y=.72, color=GOLD, size=43)
        self.play(FadeIn(link), run_time=.7)
        self.at("in 2001")
        credit = label("Logothetis et al., 2001", y=-.57, size=32)
        self.play(FadeIn(credit), run_time=.7)
        self.at("recorded with electrodes")
        probe = electrode()
        self.play(FadeIn(probe, shift=UP*.42), run_time=1)
        self.at("monkey visual cortex")
        cortex = label("Monkey visual cortex", x=-3.55, y=-3.20, size=28, width=5.8)
        self.play(FadeIn(cortex), FadeOut(link), FadeOut(credit), run_time=.68)
        self.play(FadeIn(axes), run_time=.65)
        self.at("long visual stimulus")
        self.play(GrowFromEdge(stim, LEFT), FadeIn(stim_label), run_time=.85)
        self.at("synaptic current stayed")
        self.play(FadeIn(names[0]), Create(traces[0]), run_time=1.4, rate_func=linear)
        self.at("while spiking fell")
        self.play(FadeIn(names[1]), Create(traces[1]), run_time=1.4, rate_func=linear)
        self.play(FadeIn(names[2]), Create(traces[2]), run_time=1.05, rate_func=linear)
        self.at("predict did bold")
        self.play(FadeIn(bold_question_mark(axes)), FadeIn(prediction_question()), run_time=.62)
        self.finish()


class S05PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = PAUSE_CARD

    def construct(self):
        # Keep the card and evidence still for the supplied pause; the paths are alternatives.
        add_prediction_world(self)
        axes, traces, names, stim, stim_label = experiment()
        self.add(axes, traces, names, stim, stim_label)
        self.add(label("Monkey visual cortex", x=-3.55, y=-3.20, size=28, width=5.8))
        self.add(bold_question_mark(axes), prediction_question())
        candidates = candidate_paths(axes)
        self.play(FadeIn(candidates), run_time=.48)
        for path in candidates:
            pulse(path, base=4.6, amp=2.1, speed=2.1)
        self.wait(self.narration_s-.48)


class S06PredictAnswer(SpokenScene):
    def construct(self):
        probe = add_prediction_world(self, moving=True)
        axes, traces, names, stim, stim_label = experiment()
        old_q = prediction_question()
        mark = bold_question_mark(axes)
        candidates = candidate_paths(axes)
        cortex = label("Monkey visual cortex", x=-3.55, y=-3.20, size=28, width=5.8)
        self.add(axes, traces, names, stim, stim_label, old_q, mark, candidates, cortex)
        bold = neural_signals()[2]
        complete = axes[2].curve(bold, x0=5.25, color=ORANGE, width=5)
        self.at("bold stayed high")
        self.play(FadeOut(VGroup(old_q, mark, candidates), run_time=.37),
                  Create(complete, run_time=1.30))
        self.at("local field potential")
        lfp = label("Local field potential", x=2.46, y=2.38, color=YELLOW, size=28, width=5.4)
        self.play(swap(names[0], lfp), run_time=.72)
        pulse(traces[0], base=5, amp=2.1, speed=3.1)
        pulse(complete, base=5, amp=2.1, speed=3.1)
        self.at("input and local processing")
        supported = label("✓  Input and processing", y=-2.75, color=GREEN, size=31)
        self.play(FadeIn(supported), run_time=.65)
        self.at("spiking output")
        self.play(traces[1].animate.set_stroke(opacity=.28), names[1].animate.set_opacity(.45),
                  run_time=.72)
        self.at("the rule")
        self.play(FadeOut(VGroup(axes, traces, names[1], names[2], lfp, complete, stim, stim_label,
                                 cortex, supported, probe)), run_time=.72)
        structure = label("MRI · Brain structure", y=1.46, size=39)
        blood = label("fMRI · Delayed blood\noxygenation", y=.15, color=ORANGE, size=37)
        self.at("brain structure")
        self.play(FadeIn(structure), run_time=.64)
        self.at("delayed blood oxygenation")
        self.play(FadeIn(blood), run_time=.7)
        self.at("shows task involvement")
        involvement = label("✓  Task involvement", y=-1.37, color=GREEN, size=32)
        self.play(FadeIn(involvement), run_time=.64)
        self.at("spikes or necessity")
        self.play(FadeIn(label("×  Spikes or necessity", y=-2.21, color=REJECTED, size=32)),
                  run_time=.68)
        self.finish()


def localizers():
    samples = VGroup()
    for center, offset, color in [(xy(1.57,.42), -.36, ORANGE), (xy(4.92,.42), .39, TEAL)]:
        shape = brain_slice(center, .87)
        activity = glow(center+xy(offset,.49), color=color, radius=.37)
        samples.add(VGroup(shape, activity))
    return samples


def overlap_template():
    center = xy(3.25,.42)
    outline_brain = brain_slice(center, 1.27)
    heat = VGroup(glow(center+xy(-.34,.5), radius=.67),
                  glow(center+xy(.38,.5), color=TEAL, radius=.67),
                  glow(center+xy(.01,.5), color=YELLOW, radius=.35))
    return VGroup(outline_brain, heat)


class S07LimitsResolutionBlur(SpokenScene):
    def construct(self):
        scan_world(self)
        active = glow()
        self.add(active, scheme())
        breathing(active)
        self.at("three limits shape")
        intro = label("Three limits", y=2.12, size=42)
        self.play(FadeIn(intro), run_time=.65)
        self.at("activation never shows")
        heading = label("Testing necessity", y=2.12, color=TEXT, size=42)
        glow_label = boxed_label("Activation", ORANGE, size=32).move_to(xy(RIGHT_X,.75))
        self.play(swap(intro, heading, run_time=.58), FadeIn(glow_label), run_time=.58)
        rejected = label("×  Necessity established", y=-.04, color=REJECTED, size=30)
        self.play(FadeIn(rejected), run_time=.65)
        self.at("requires damage or silencing")
        test = boxed_label("Lesion or silencing", BLUE, size=32).move_to(xy(RIGHT_X,-1.05))
        verdict = label("Tests whether it’s needed", y=-1.91, color=GREEN, size=30)
        active.clear_updaters()
        self.play(FadeIn(test), Transform(active, lesion()), run_time=.85)
        self.play(FadeIn(verdict), run_time=.62)
        self.at("averaging scans across")
        self.play(FadeOut(VGroup(heading, glow_label, rejected, test, verdict, active)), run_time=.45)
        samples = localizers()
        self.play(FadeIn(samples), run_time=.75)
        self.at("can blur neighboring")
        midpoint = xy(3.25,.42)
        self.play(*[item.animate.move_to(midpoint) for item in samples], run_time=1.55)
        template = overlap_template()
        self.play(ReplacementTransform(samples, template), run_time=.68)
        self.at("false overlap")
        overlap = label("False overlap", y=-1.78, color=YELLOW, size=36)
        self.play(FadeIn(overlap), run_time=.6)
        self.at("mapping regions inside")
        individuals = localizers()
        self.play(FadeOut(overlap), run_time=.32)
        self.play(ReplacementTransform(template, individuals), run_time=1.7)
        self.play(FadeIn(label("Individual localizers", y=-1.49, size=34)), run_time=.63)
        self.finish()


def example_associations():
    """Synthetic standardized variables with an exactly 0.01 pooled correlation."""
    rng = np.random.default_rng(2022)
    n = 3928
    x, noise = rng.standard_normal((2, n))
    x -= x.mean()
    x /= x.std()
    noise -= noise.mean()
    noise -= np.mean(noise*x)*x
    noise /= noise.std()
    r = .01
    y = r*x + np.sqrt(1-r*r)*noise
    for indices in np.array_split(rng.permutation(n), n//25):
        if len(indices) != 25:
            continue
        slope, _ = np.polyfit(x[indices], y[indices], 1)
        if slope > .26:
            positive = indices
            break
    for indices in rng.permutation(n)[:3900].reshape(-1, 25):
        slope, _ = np.polyfit(x[indices], y[indices], 1)
        if slope < -.26:
            negative = indices
            break
    return x, y, positive, negative


def fitted_line(plot, x, y, color):
    slope, intercept = np.polyfit(x, y, 1)
    return plot.curve(lambda value: slope*value+intercept, x0=-3.7, x1=3.7,
                      color=color, width=5, n=16)


def scatter(plot, x, y, color, radius, opacity):
    return VGroup(*[Dot(plot.pt(a,b), radius=radius, color=color, fill_opacity=opacity)
                    for a,b in zip(x,y)])


def person(color, at):
    head = Dot(xy(0,.31), radius=.17, color=color)
    torso = RoundedRectangle(width=.43, height=.50, corner_radius=.15, stroke_width=0,
                             fill_color=color, fill_opacity=1).move_to(xy(0,-.08))
    return VGroup(head, torso).move_to(at)


def targets():
    rings = VGroup(*[Circle(radius=r, stroke_width=3.5, color=BLUE) for r in (.92,.62,.31)])
    pin = Dot(radius=.15, color=GOLD)
    return rings.move_to(xy(RIGHT_X,1.94)), pin.move_to(xy(RIGHT_X,1.94))


class S08LimitsSamples(SpokenScene):
    def construct(self):
        scan_world(self)
        self.add(scheme())
        plot = Plot(box=(.40, 6.29, -1.75, 2.35), xr=(-4.5,4.5), yr=(-4.5,4.5),
                    xlabel="Brain measure", ylabel="Behaviour", color=TEXT, label_size=28)
        self.at("third brain wide")
        self.play(Create(plot.axes), run_time=.8)
        self.play(FadeIn(plot.xlabel), FadeIn(plot.ylabel), run_time=.65)
        x,y,a,b = example_associations()
        pooled = fitted_line(plot, x, y, TEXT)
        self.at("are usually tiny")
        self.play(Create(pooled), run_time=1.15)
        credit = label("Marek et al., 2022", y=3.08, color=GOLD, size=29)
        self.at("in 2022")
        self.play(FadeIn(credit), run_time=.65)
        median = label("Median association 0.01", x=2.25, y=-2.65, size=30)
        self.at("median association")
        self.play(FadeIn(median), run_time=.65)
        first = scatter(plot, x[a], y[a], ORANGE, .058, .9)
        second = scatter(plot, x[b], y[b], TEAL, .058, .9)
        trend_a = fitted_line(plot, x[a], y[a], ORANGE)
        trend_b = fitted_line(plot, x[b], y[b], TEAL)
        n = label("n = 25 per sample", x=2.25, y=-2.65, size=30)
        self.at("used about 25")
        self.play(FadeOut(pooled), swap(median,n), run_time=.56)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in first], lag_ratio=.075),
                  run_time=1.33)
        self.at("two such sub samples")
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in second], lag_ratio=.06),
                  Create(trend_a), run_time=1.35)
        self.at("opposite conclusions")
        self.play(Create(trend_b), run_time=1.1)
        self.at("replication improved")
        # Cairo draws the point cloud as vector batches, with all 3,928 participants retained.
        batches = VGroup()
        for ids in np.array_split(np.random.default_rng(16).permutation(len(x)), 8):
            dots = scatter(plot, x[ids], y[ids], BLUE, .021, .42)
            batch = VMobject(stroke_width=0, fill_color=BLUE, fill_opacity=.42)
            batch.set_points(np.vstack([dot.get_points() for dot in dots]))
            batches.add(batch)
        size = label("3,928 participants", y=3.08, color=BLUE, size=29)
        self.play(swap(credit,size), LaggedStart(*[FadeIn(part) for part in batches], lag_ratio=.32),
                  FadeOut(VGroup(first, second, trend_a, trend_b, n),
                          rate_func=squish_rate_func(smooth, 0, .4)), run_time=2.03)
        self.play(Create(pooled), FadeIn(median), run_time=.77)
        self.at("fixed targets in advance")
        self.play(FadeOut(VGroup(plot.axes, plot.xlabel, plot.ylabel, batches, pooled, median, size)),
                  run_time=.25)
        target, pin = targets()
        chosen = label("Chosen in advance", y=.68, color=GOLD, size=31)
        self.play(Create(target), GrowFromCenter(pin), FadeIn(chosen), run_time=.5)
        self.at("tests on people")
        people = VGroup(*[person(ORANGE if i < 3 else TEAL, xy(1.65+.62*i,-.58))
                          for i in range(6)])
        self.play(FadeIn(people), run_time=.24)
        train = label("Train", x=1.69, y=-1.40, color=ORANGE, size=29)
        held_out = label("Held-out people", x=4.64, y=-1.40, color=TEAL, size=29)
        self.play(*[p.animate.shift((LEFT if i < 3 else RIGHT)*.58)
                    for i,p in enumerate(people)], FadeIn(train), FadeIn(held_out), run_time=.42)
        self.finish()


def task_comparison():
    tasks = VGroup(
        label("Sentences", y=1.13, color=ORANGE, size=39),
        label("Arithmetic", y=.0, size=29),
        label("Working memory", y=-.69, size=29),
        label("Music", y=-1.38, size=29),
    )
    for item in tasks:
        item.align_to(xy(1.9,0), LEFT)
    return tasks


class S09UnlockedStructureTask(SpokenScene):
    def construct(self):
        brain = scan_world(self)
        self.add(scheme())
        self.at("with those guards")
        sweep = scan_line(brain)
        self.add(sweep)
        self.play(sweep.animate.set_y(brain.get_bottom()[1]+.1), run_time=3.2, rate_func=linear)
        self.play(FadeOut(sweep), run_time=.4)
        self.at("in 2007")
        credit = label("Dronkers et al., 2007", y=2.35, color=GOLD, size=33)
        self.play(FadeIn(credit), run_time=.65)
        self.at("two preserved 1861 brains")
        centers = (xy(1.64,.38), xy(4.62,.38))
        preserved = VGroup(*[brain_slice(at,.77) for at in centers])
        self.play(FadeIn(preserved), run_time=1.3)
        self.at("with mri")
        surface = lesion()
        self.play(FadeIn(surface), run_time=.74)
        self.at("both lesions reached deeper")
        extensions = VGroup(*[lesion(deep=True, center=at, scale=.77) for at in centers])
        self.play(Transform(surface, lesion(deep=True)), FadeIn(extensions), run_time=1.65)
        self.at("into white matter")
        deep = label("Lesions reached white matter", y=-1.74, color=WHITE_MATTER, size=31)
        self.play(FadeIn(deep), run_time=.65)
        self.at("from the surface")
        rim = lesion()
        rim.set_fill(opacity=0).set_stroke(color=TEXT, width=2.5)
        self.play(Create(rim), run_time=.7)
        self.at("in 2011")
        self.play(FadeOut(VGroup(surface,rim,preserved,extensions,deep)), run_time=.6)
        fed = label("Fedorenko et al., 2011", y=2.35, color=GOLD, size=33)
        self.play(swap(credit,fed), run_time=.7)
        self.at("defined each person's")
        sites = VGroup(glow(PATCH_AT, radius=.36), glow(SCANNER_AT+xy(-.79,.08), radius=.28))
        self.play(LaggedStart(*[GrowFromCenter(site) for site in sites], lag_ratio=.6), run_time=1.55)
        self.at("language regions individually")
        tasks = task_comparison()
        self.play(FadeIn(tasks[0]), run_time=.65)
        self.at("responded little to")
        self.play(sites.animate.set_opacity(.075), tasks[0].animate.set_opacity(.65), run_time=.8)
        self.at("arithmetic")
        self.play(FadeIn(tasks[1]), run_time=.50)
        self.at("working memory")
        self.play(FadeIn(tasks[2]), run_time=.50)
        self.at("or music")
        self.play(FadeIn(tasks[3]), run_time=.50)
        self.finish()


def connection():
    p = SCANNER_AT+xy(-.30,.89)
    q = SCANNER_AT+xy(.53,-.32)
    arc = ArcBetweenPoints(p, q, angle=-1.25, color=ORANGE, stroke_width=6)
    return arc, glow(p, radius=.29), glow(q, radius=.29)


def timeline():
    plot = Plot(box=(.46,6.09,-.35,1.76), xr=(0,12), yr=(0,1),
                xticks=((0,"Baseline"),(12,"1 year")), color=BLUE, size=28, stroke=4)
    # A single time rail. The two empty length axes from Plot are unused.
    return plot, VGroup(plot.axes[0],plot.ticks,plot.tick_labels)


class S10UnlockedConnectivity(SpokenScene):
    def construct(self):
        scan_world(self)
        self.add(scheme())
        self.at("in 2012")
        self.play(FadeIn(label("Baliki et al., 2012", y=2.70, color=GOLD, size=34)), run_time=.7)
        plot, rail = timeline()
        self.at("followed adults with")
        self.play(FadeIn(rail), run_time=.64)
        t = ValueTracker(0)
        dot = plot.dot(t.get_value, lambda: 0, color=TEXT, ring=BLUE)
        self.add(dot)
        self.at("recent back pain")
        self.play(t.animate.set_value(12), run_time=2.85, rate_func=linear)
        self.at("stronger baseline connectivity")
        arc, front, deep = connection()
        self.play(Create(arc), GrowFromCenter(front), GrowFromCenter(deep), run_time=1.5)
        breathing(front)
        breathing(deep)
        pulse(arc, base=6, amp=3, speed=TAU/3.6)
        self.at("medial prefrontal cortex")
        frontal = label("Medial prefrontal cortex", y=1.68, color=ORANGE, size=30)
        self.play(FadeIn(frontal), run_time=.65)
        self.at("nucleus accumbens")
        accumbens = label("Nucleus accumbens", y=.89, color=ORANGE, size=30)
        self.play(FadeIn(accumbens), run_time=.65)
        self.at("predicted persistence")
        prediction = label("Predicted persistent pain", y=-1.64, color=GREEN, size=36)
        self.play(FadeIn(prediction), run_time=.7)
        self.at("the roc area")
        roc = boxed_label("ROC area 0.83", GOLD, size=32).move_to(xy(RIGHT_X,-2.61))
        self.play(FadeIn(roc), run_time=.74)
        self.finish()


def pair_plot():
    p = Plot(box=(.43,6.23,-1.89,1.91), xr=(0,7), yr=(0,1), color=TEXT, size=28,
             ylabel="Predicted persistence score", label_size=28, stroke=3)
    return p


def pairs(plot):
    # Seeded synthetic score pairs, with exactly five illustrating the higher rank.
    rng = np.random.default_rng(83)
    low = rng.uniform(.17,.43,size=6)
    high = rng.uniform(.57,.87,size=6)
    illustrative = np.column_stack((high,low))
    illustrative[2] = illustrative[2,::-1]
    return [VGroup(Line(plot.pt(i+.85,a),plot.pt(i+.85,b),color=GREY,stroke_width=2.5),
                   Dot(plot.pt(i+.85,a), radius=.104,color=ORANGE),
                   Dot(plot.pt(i+.85,b), radius=.104,color=TEAL))
            for i,(a,b) in enumerate(illustrative)]


class S10bPairsAndClose(SpokenScene):
    def construct(self):
        scan_world(self)
        arc, front, deep = connection()
        self.add(arc,front,deep,scheme())
        breathing(front)
        breathing(deep)
        pulse(arc, base=6, amp=3, speed=TAU/3.6)
        plot = pair_plot()
        keys = VGroup(label("Persisted", x=1.72, y=1.88, color=ORANGE, size=29),
                      label("Recovered", x=4.84, y=1.88, color=TEAL, size=29))
        self.at("that means in about")
        self.play(Create(plot.axes), FadeIn(plot.ylabel), FadeIn(keys), run_time=.4)
        dots = VGroup(*pairs(plot))
        wins_so_far = ValueTracker(0)
        readout = counter("{:.0f} of 6 rank higher", wins_so_far, at=xy(RIGHT_X,-2.72),
                          size=30, color=GOLD)
        self.add(readout)
        for pair in dots:
            self.play(FadeIn(pair, shift=UP*.15), run_time=.18)
            wins_so_far.increment_value(int(pair[1].get_y() > pair[2].get_y()))
            readout.update(0)
        wins = wins_so_far.get_value()
        result = M(f"{100*wins/len(dots):.0f}% of pairs", 33, GOLD).move_to(readout)
        self.at("of random pairs", lead=.70)
        readout.clear_updaters()
        self.play(swap(readout, result, run_time=.20))
        self.at("prediction is not cause")
        cause = label("Prediction ≠ cause", y=3.07, color=GOLD, size=37)
        self.play(FadeIn(cause), run_time=.66)
        self.at("read structure directly")
        self.play(FadeOut(VGroup(plot.axes,plot.ylabel,result,keys,dots,cause)),
                  FadeOut(VGroup(arc,front,deep)), run_time=.65)
        self.play(FadeIn(label("Brain structure", y=.73, size=40)), run_time=.58)
        self.at("read every glow")
        vessel = capillary().shift(DOWN*2.35)
        self.play(FadeIn(vessel), FadeIn(glow()), run_time=.58)
        cells = blood_flow(self, [True,True,False,True,True], speed=.95)
        cells.shift(DOWN*2.35)
        self.at("delayed blood oxygenation")
        self.play(FadeIn(label("Delayed blood oxygenation", y=-1.85, color=ORANGE, size=32)),
                  run_time=.63)
        self.at("not spikes")
        self.play(FadeIn(label("×  Spikes", y=-2.53, color=REJECTED, size=29)), run_time=.56)
        self.finish()


class S11End(EndCard):
    LINE = "MRI maps structure; fMRI reads blood oxygenation, not spikes or cause."
