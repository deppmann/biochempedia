"""Growing Mini-Organs in a Dish, timed to audio/words.json.

BLUE is glass, TEAL is the culture medium and lumen, GREY is structure.
PURPLE is stem cells and progenitors, GREEN is neurons or confirming evidence,
RED is viral harm or a limitation, ORANGE is an added cue, YELLOW is a
released signal or a highlighted cell, and GOLD is context and key questions.
"""
from bp_parts import *
from bp_style import EndCard, TitleCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
DISH = np.array([-2.25, -0.28, 0.0])
CENTER = DISH + UP * 0.19
SIDE = 4.17
QUESTION = "What can organoids prove—and miss?"


def p(x, y):
    return np.array([x, y, 0.])


def silhouette(points, color, opacity=0.38, stroke=2.5):
    shape = VMobject()
    vertices = [p(*xy) for xy in points]
    shape.set_points_smoothly([*vertices, vertices[0]])
    return shape.set_fill(color, opacity).set_stroke(color, stroke)


def plate():
    """Fixed vessel and focal point shared by the whole film."""
    floor = Ellipse(width=7.58, height=4.92).move_to(DISH + DOWN * 0.16)
    floor.set_fill(BLUE, 0.26).set_stroke(BLUE, 2.5, 0.48)
    bath = Ellipse(width=7.12, height=4.48).move_to(DISH + UP * 0.04)
    bath.set_fill(TEAL, 0.24).set_stroke(width=0)
    rim = Ellipse(width=7.60, height=4.96).move_to(DISH + UP * 0.05)
    rim.set_stroke(BLUE, 3.1, 0.88)
    glint = Arc(radius=1, start_angle=PI * 1.15, angle=PI * 0.51)
    glint.stretch(3.52, 0, about_point=ORIGIN).stretch(2.25, 1, about_point=ORIGIN)
    glint.shift(DISH + UP * 0.03).set_stroke(TEXT, 2, 0.56)
    stream = VGroup(
        Ellipse(width=2.68, height=0.91).move_to(DISH + p(-1.69, 0.61)),
        Ellipse(width=2.33, height=0.73).move_to(DISH + p(1.85, -0.78)),
    ).set_fill(BLUE, 0.23).set_stroke(width=0)
    motes = VGroup(*(
        Dot(DISH + p(x, y), radius=r, color=BLUE).set_opacity(0.48)
        for x, y, r in [(-3.2, -.35, .055), (-2.65, .93, .042), (-2., -1.33, .069),
                        (-.85, 1.68, .052), (.85, -1.69, .049), (2.15, 1.32, .06),
                        (2.83, .53, .043), (3.13, -.68, .061)]
    ))
    return VGroup(floor, bath, rim, glint, stream, motes)


def float_in(scene, mob, amount=0.14, speed=1.6, phase=0.0):
    """Drift around a fixed landmark and settle back at the cut."""
    home = mob.get_center().copy()
    start = scene.elapsed()

    def drift(obj, dt):
        t = scene.elapsed()
        age = t - start
        settle = np.clip((scene.narration_s - t) / 0.65, 0, 1)
        enter = np.clip(age / 0.45, 0, 1)
        offset = p(np.sin(speed * age + phase) * 0.42, np.sin(0.77 * speed * age + phase))
        obj.move_to(home + amount * settle * enter * offset)

    mob.add_updater(drift)
    return mob


def show_plate(scene, still=False, tag=True):
    world = plate()
    scene.add(world)
    if not still:
        float_in(scene, world[-2][0], 0.46, 2.1)
        float_in(scene, world[-2][1], 0.39, 2.35, 2)
        for i, mote in enumerate(world[-1]):
            float_in(scene, mote, 0.15, 1.4, i)
    if tag:
        scene.add(scope_tag("Schematic", size=28, color=TEXT))
    return world


def label(text, color=TEXT, x=SIDE, y=0.1, width=4.45):
    return fit_text(text, max_w=width, size=33, min_size=28, color=color).move_to(p(x, y))


def heading(text, color=TEXT):
    return label(text, color, x=DISH[0], y=3.03, width=9.2)


def cell(color=PURPLE, radius=0.43, at=CENTER, flat=False):
    membrane = Circle(radius=radius, stroke_color=color, stroke_width=2.4,
                      fill_color=color, fill_opacity=0.59)
    nucleus = Dot(p(-0.14, 0.14) * radius, radius=radius * 0.32, color=color)
    unit = VGroup(membrane, nucleus)
    if flat:
        unit.stretch(1.55, 0).stretch(0.58, 1)
    return unit.move_to(at)


def cluster(at=CENTER, size=1.0, color=PURPLE):
    positions = [(0, .63), (.55, .43), (.75, -.13), (.4, -.62), (-.2, -.65),
                 (-.7, -.27), (-.62, .3), (.07, -.03)]
    return VGroup(*(cell(color, (0.34 + 0.035 * (i % 3)) * size, at + p(x, y) * size)
                    for i, (x, y) in enumerate(positions)))


def brain():
    mass = silhouette([(-2, -.24), (-2.08, .39), (-1.6, 1.02), (-.81, 1.34),
                       (.12, 1.38), (.98, 1.13), (1.69, .7), (1.93, .08),
                       (1.66, -.43), (.99, -.59), (.58, -1.03), (.28, -.66),
                       (-.59, -.77), (-1.38, -.58)], GREY, 0.31, 2)
    folds = VGroup(*(
        VMobject().set_points_smoothly([p(*q) for q in pts]).set_stroke(GREY, 2.1, 0.69)
        for pts in [[(-1.57, -.13), (-1.25, .46), (-.6, .62)],
                    [(-.9, 1.03), (-.46, .78), (-.27, .16), (-.62, -.25)],
                    [( .24, 1.08), (.69, .74), (.62, .19), (.31, -.14)],
                    [(1.29, .67), (1.15, .25), (1.56, .08)]]
    ))
    return VGroup(mass, folds)


def neuron(at, angle):
    u = p(np.cos(angle), np.sin(angle))
    v = p(-u[1], u[0])
    soma = cell(GREEN, 0.185, at)
    root, tip = at + .12 * u, at + .43 * u
    branches = VGroup(Line(root, tip), Line(at + .27 * u, tip + .14 * v),
                      Line(at + .30 * u, tip - .12 * v)).set_stroke(GREEN, 2.8)
    return VGroup(branches, soma)


def cortex(stage="layered", size=1.0):
    """The same concentric landmarks in self-organization, cortex and Zika scenes."""
    perimeter = [(2.34, .18), (1.69, 1.36), (.24, 1.7), (-1.25, 1.52), (-2.28, .7),
                 (-2.31, -.43), (-1.42, -1.28), (.05, -1.56), (1.6, -1.2)]
    shell = silhouette(perimeter, PURPLE, .28, 2.2).shift(CENTER)
    lumen = Ellipse(width=2.45, height=1.42, stroke_color=TEAL, stroke_width=2.8,
                    fill_color=TEAL, fill_opacity=.30).move_to(CENTER)
    angles = np.linspace(0, TAU, 13, endpoint=False)
    inner = VGroup(*(cell(PURPLE, .218, CENTER + p(1.39*np.cos(t), .89*np.sin(t))) for t in angles))
    outer = VGroup(*(neuron(CENTER + p(1.93*np.cos(t), 1.28*np.sin(t)), t)
                     if stage == "layered" else cell(GREY, .19, CENTER + p(1.93*np.cos(t), 1.28*np.sin(t)))
                     for t in angles + .14))
    return VGroup(shell, lumen, inner, outer).scale(size, about_point=CENTER)


def gut():
    """Continuous gut lining, with the same rare-cell location in dish and native tissue."""
    angles = np.linspace(0, TAU, 24, endpoint=False)
    ring = [p((1.99 + .31*np.cos(3*t))*np.cos(t),
              (1.27 + .23*np.cos(3*t))*np.sin(t)) for t in angles]
    envelope = silhouette([(x, y) for x, y, _ in ring], TEAL, .24, 2.6).shift(CENTER)
    lumen = envelope.copy().scale(.64, about_point=CENTER).set_fill(BG, .58).set_stroke(TEAL, 2, .62)
    palette = [BLUE, TEAL, PURPLE]
    lining = VGroup(*(cell(palette[(i // 3) % 3], .225, CENTER + x * .86)
                      for i, x in enumerate(ring)))
    return VGroup(envelope, lumen, lining)


def gut_strip(tagged=False):
    bed = RoundedRectangle(width=3.7, height=1.45, corner_radius=.23, stroke_color=TEAL,
                           stroke_width=2.7, fill_color=TEAL, fill_opacity=.25)
    rows = VGroup()
    for row in range(2):
        for i in range(7):
            color = YELLOW if tagged and row == 0 and i == 4 else [BLUE, TEAL, PURPLE][(i + row) % 3]
            rows.add(cell(color, .18, p((i-3)*.46, .30-row*.58), flat=True))
    return VGroup(bed, rows).move_to(p(SIDE, -.43))


def body(pregnant=False):
    left = [(-.19, 1.42), (-.66, 1.21), (-1.02, .03), (-.82, -.09),
            (-.48, .72), (-.43, -.1), (-.38, -1.50), (-.09, -1.49)]
    if pregnant:
        right = [(.17, -1.5), (.46, -1.5), (.54, -.32), (1.00, .22),
                 (.67, .97), (.44, 1.27), (.19, 1.42)]
    else:
        right = [(-x, y) for x, y in reversed(left)]
    path = silhouette([*left, (0, -.38), *right], GREY, .12, 2)
    outline = DashedVMobject(path.copy().set_fill(opacity=0).set_stroke(GREY, 2.7, .8), num_dashes=44)
    head = DashedVMobject(Circle(radius=.35, color=GREY, stroke_width=2.7).move_to(p(0, 1.88)),
                         num_dashes=15)
    return VGroup(path.set_stroke(width=0), outline, head).move_to(p(SIDE, .20))


def mouse():
    torso = Ellipse(width=2.1, height=1.16, stroke_width=2.7, color=GREY, fill_opacity=.24)
    head = Ellipse(width=.92, height=.71, stroke_width=2.5, color=GREY, fill_opacity=.34)
    head.move_to(p(.99, .14)).rotate(-.20)
    ear = Dot(p(.71, .48), radius=.20, color=GREY)
    eye = Dot(p(1.14, .25), radius=.048, color=TEXT)
    tail = VMobject().set_points_smoothly([p(-.87, -.03), p(-1.40, -.29), p(-1.79, -.16),
                                           p(-1.98, .09)]).set_stroke(GREY, 3)
    belly = Ellipse(width=.76, height=.50, color=GREY, stroke_width=2).move_to(p(-.13, -.19))
    return VGroup(tail, torso, head, ear, eye, belly).move_to(p(SIDE, -.32))


def beads(coords, color, radius=.13):
    return VGroup(*(Dot(CENTER + p(x, y), color=color, radius=radius * (1 - .12*(i % 3)))
                    for i, (x, y) in enumerate(coords)))


def mark(at, good=True):
    vertices = [(-.25, 0), (-.06, -.18), (.30, .23)]
    if good:
        icon = VMobject().set_points_as_corners([p(*xy) for xy in vertices]).set_stroke(GREEN, 6)
    else:
        icon = Cross(stroke_color=RED, stroke_width=6).scale(.28)
    return icon.move_to(at)


def glutamate():
    return beads([(-1.86, .73), (-2.23, .99), (-2.44, .65), (-2.74, .88), (-2.92, 1.17)], YELLOW)


def predict_question():
    return question_card(QUESTION, y=3.02, size=37).move_to(p(DISH[0], 3.02))


def predict_picture():
    loop = gut()
    signal = glutamate()
    whole = body()
    return loop, signal, whole


class S01Hook(SpokenScene):
    def construct(self):
        show_plate(self)
        sketch = brain().scale(.93).move_to(CENTER + UP * 1.36)
        query = label("?", GOLD, x=SIDE, y=1.13).scale(1.55)
        self.add(sketch)
        float_in(self, sketch, .37, 2.1)
        self.at("can you test")
        self.play(FadeIn(query, shift=UP*.16), run_time=.62)
        pulse_sketch = sketch[0]
        pulse(pulse_sketch, base=2.1, amp=1.0, speed=2.5)
        float_in(self, query, .16, 2.1)
        self.at("cannot experiment")
        pulse_sketch.clear_updaters()
        self.play(sketch[0].animate.set_fill(opacity=.14).set_stroke(opacity=.47),
                  sketch[1].animate.set_stroke(opacity=.31), run_time=1.35)
        self.at("instead")
        self.play(FadeOut(query), FadeOut(sketch), run_time=.48)
        microtissues = VGroup(cluster(CENTER+p(-1.96, -.19), 1.12),
                             cluster(CENTER+p(.05, .54), .98, TEAL),
                             cluster(CENTER+p(1.86, -.42), 1.14))
        self.play(LaggedStart(*(GrowFromCenter(c) for c in microtissues), lag_ratio=.26), run_time=1.48)
        for i, group in enumerate(microtissues):
            float_in(self, group, .19, 2.0, i*1.5)
        self.at("called organoids")
        self.play(FadeIn(label("Organoids", PURPLE)), run_time=.40)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Growing Mini-Organs in a Dish"
    LESSON = "iPS cells and organoids"

    def construct(self):
        show_plate(self, tag=False)
        first, last = self.TITLE.rsplit(" in ", 1)
        title = VGroup(T(first, size=46, font=TITLE_FONT),
                       T("in " + last, size=46, font=TITLE_FONT)).arrange(DOWN, buff=.12)
        lesson = T(self.LESSON, size=29, color=TEXT)
        card = VGroup(title, lesson).arrange(DOWN, buff=.30).move_to(CENTER)
        self.play(FadeIn(card), run_time=.32)
        self.wait(1.30)
        self.play(FadeOut(card), run_time=.32)


class S03Reset(SpokenScene):
    def construct(self):
        show_plate(self)
        subject = cell(GREY, 1.00, CENTER + LEFT*1.22, flat=True)
        self.add(subject)
        self.at("start with")
        self.play(subject.animate.move_to(CENTER), run_time=1.13)
        skin = label("Skin cell")
        self.play(FadeIn(skin), run_time=.30)
        self.at("a few proteins")
        signals = beads([(-2.95, .91), (-2.53, 1.5), (2.55, .94), (2.97, -.61)], ORANGE, .18)
        self.play(FadeIn(signals, shift=UP*.15), run_time=.48)
        factors = label("Transcription factors", ORANGE)
        self.at("called transcription factors")
        self.play(swap(skin, factors), run_time=.66)
        self.at("reset its identity")
        destinations = [(-1.17, .17), (-.59, .58), (1.01, .29), (1.19, -.22)]
        self.play(*(dot.animate.move_to(CENTER + p(*xy)) for dot, xy in zip(signals, destinations)),
                  run_time=1.02)
        self.play(Transform(subject, cell(PURPLE, 1.02)), FadeOut(signals), FadeOut(factors), run_time=1.22)
        float_in(self, subject, .26, 1.9)
        self.at("induced pluripotent")
        ips = label("iPS cell", PURPLE)
        self.play(FadeIn(ips), run_time=.62)
        self.at("pluripotent means")
        sketches = VGroup(brain().scale(.28).move_to(CENTER + p(-2.47, .53)),
                          gut().scale(.27).move_to(CENTER + p(2.19, .79)),
                          VGroup(*(Ellipse(width=1.19, height=.16, color=GREY, fill_opacity=.28)
                                   .shift(UP*y) for y in [-.22, 0, .22]))
                          .rotate(.53).move_to(CENTER + p(2.08, -.94)))
        branches = VGroup(*(Line(CENTER+u*.99, c.get_center()-u*.63, color=GREY, stroke_width=2.6)
                            for c in sketches for u in [(c.get_center()-CENTER)/np.linalg.norm(c.get_center()-CENTER)]))
        plural = label("Pluripotent", PURPLE)
        self.play(swap(ips, plural), LaggedStart(*[FadeIn(c, shift=RIGHT*.18) for c in sketches], lag_ratio=.45),
                  Create(branches), run_time=2.00)
        self.at("and it carries")
        self.play(FadeOut(sketches), FadeOut(branches), FadeOut(plural), run_time=.56)
        self.play(FadeIn(boxed_label("Patient genome", PURPLE, size=30).move_to(p(SIDE, .1))),
                  subject[1].animate.set_color(YELLOW), run_time=.64)
        self.finish()


class S04Selforg(SpokenScene):
    def construct(self):
        show_plate(self)
        seed = cell(PURPLE, 1.02)
        seed[1].set_color(YELLOW)
        self.add(seed)
        self.at("stem cells clump")
        floating = cluster(size=1.43)
        self.play(ReplacementTransform(seed, floating), run_time=1.40)
        float_in(self, floating, .19)
        self.at("yet they sort")
        selforg = heading("Self-organization", GOLD)
        self.play(FadeIn(selforg), run_time=.55)
        self.at("they form a polarized sheet", lead=.82)
        floating.clear_updaters()
        layers = cortex("sheet")
        self.play(ReplacementTransform(floating, layers), run_time=2.20)
        for i, c in enumerate(layers[2]):
            float_in(self, c, .094, 2.2, i*.48)
        self.at("dividing precursors called")
        progenitors = label("Progenitors", PURPLE, y=.13)
        self.play(FadeIn(progenitors), run_time=.64)
        for i, c in enumerate(layers[2]):
            pulse(c[0], base=2.7, amp=1.6, speed=1.9 + .2*(i % 3))
        self.at("fluid")
        cavity = label("Fluid-filled cavity", TEAL, y=.93)
        self.play(FadeIn(cavity), run_time=.60)
        self.at("while young neurons", lead=.55)
        young = label("Young neurons", GREEN, y=-.67)
        self.play(Transform(layers[3], cortex()[3]), run_time=.93)
        self.play(FadeIn(young), run_time=.45)
        float_in(self, layers, .10, 1.7)
        self.finish()


class S05Niche(SpokenScene):
    def construct(self):
        show_plate(self)
        loop = gut()
        self.add(loop)
        whole = body()
        float_in(self, loop, .18, 2.1)
        self.at("start from adult")
        loop.clear_updaters()
        adult = cell(PURPLE, .98)
        self.play(FadeOut(loop), run_time=.46)
        self.play(GrowFromCenter(adult), run_time=.84)
        stem = label("Adult gut stem cell", PURPLE)
        self.play(FadeIn(stem), run_time=.55)
        float_in(self, adult, .23, 2.15)
        self.at("they are multipotent")
        examples = VGroup(*(cell(color, .35, CENTER + p(x, y)) for x, y, color in
                            [(-1.69, -.24, BLUE), (0, 1.52, TEAL), (1.70, -.24, PURPLE)]))
        multi = label("Multipotent", PURPLE)
        self.play(swap(stem, multi), LaggedStart(*(GrowFromCenter(c) for c in examples), lag_ratio=.5),
                  run_time=2.03)
        for i, c in enumerate(examples):
            float_in(self, c, .08 if i == 1 else .20, 1.9, i)
        self.at("within one tissue")
        self.play(FadeOut(examples), FadeOut(multi), run_time=.69)
        self.at("and colleagues grew")
        gel = Ellipse(width=6.72, height=3.57, color=TEAL, stroke_width=2.6, fill_opacity=.37).move_to(CENTER)
        adult.set_z_index(1)
        # The gel sits above the dish floor and below all cells.
        self.play(GrowFromCenter(gel), run_time=.75)
        pulse(gel, base=2.6, amp=1.3, speed=2.3)
        matrigel = label("Matrigel", TEAL)
        self.at("in matrigel")
        self.play(FadeIn(matrigel), run_time=.45)
        year = heading("Sato et al. · 2009", GOLD)
        self.play(FadeIn(year), run_time=.40)
        self.at("added growth factors")
        cues = beads([(-2.85, .82), (-2.58, .35), (-2.81, -.12), (-2.32, -.6), (-2.95, -.81)], ORANGE)
        growth = label("Growth factors", ORANGE)
        self.play(FadeIn(cues, shift=LEFT*.21), swap(matrigel, growth),
                  run_time=.70)
        self.play(cues.animate.shift(RIGHT*1.54), run_time=1.2)
        self.at("cells dividing")
        adult.clear_updaters()
        intestine = gut()
        intestine.set_z_index(1)
        self.play(ReplacementTransform(adult, intestine), FadeOut(cues), FadeOut(year), FadeOut(growth),
                  run_time=2.36)
        float_in(self, intestine, .14)
        self.at("stem cells self")
        self.play(FadeOut(gel), run_time=.36)
        self.at("that model tissue")
        self.play(FadeIn(whole), run_time=1.02)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        show_plate(self)
        starting = gut()
        whole = body()
        self.add(starting, whole)
        self.at("suppose a virus")
        self.play(FadeOut(whole), FadeOut(starting), run_time=.36)
        brain_organoid = cortex(size=.76)
        self.play(GrowFromCenter(brain_organoid), run_time=.55)
        viral = beads([(-2.15, .71), (-1.82, 1.37), (-.70, 1.65), (.38, 1.7)], RED, .115)
        self.play(FadeIn(viral), run_time=.61)
        self.play(viral.animate.shift(p(.83, -.74)), brain_organoid.animate.scale(.75, about_point=CENTER),
                  run_time=.88)
        self.at("or sugar makes")
        self.play(FadeOut(viral), FadeOut(brain_organoid), run_time=.30)
        loop, signal, whole = predict_picture()
        self.play(FadeIn(loop, scale=.89), run_time=.66)
        sugar = beads([(2.98, .69), (2.68, .98), (3.02, .23)], ORANGE, .125)
        sugar_label = label("Sugar", ORANGE)
        self.play(FadeIn(sugar), FadeIn(sugar_label), run_time=.40)
        self.play(sugar.animate.shift(LEFT*1.18), run_time=.83)
        self.at("release glutamate")
        signal_label = label("Glutamate", YELLOW)
        self.play(LaggedStart(*(GrowFromCenter(d) for d in signal), lag_ratio=.33),
                  swap(sugar_label, signal_label), FadeOut(sugar), run_time=.90)
        self.add(signal)
        self.at("what do those experiments")
        self.play(FadeOut(signal_label), run_time=.28)
        self.play(FadeIn(whole), run_time=.45)
        self.play(FadeIn(predict_question(), shift=UP*.19), run_time=.64)
        float_in(self, loop, .16, 1.8)
        float_in(self, signal, .14, 1.9)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        show_plate(self, still=True)
        loop, signal, whole = predict_picture()
        self.add(loop, signal, whole, predict_question())
        self.wait(self.narration_s)


class S08Limits(SpokenScene):
    def construct(self):
        show_plate(self)
        loop, signal, whole = predict_picture()
        self.add(loop, signal, whole)
        self.at("organoids show")
        layers = cortex()
        harm = beads([(-.72, .02), (-.82, .29), (-1.32, .71)], RED, .135)
        self.play(FadeOut(loop), FadeOut(signal), run_time=.34)
        self.play(FadeIn(layers, scale=.91), run_time=.49)
        check = mark(CENTER + p(-2.92, .17))
        self.play(FadeIn(harm), Create(check), run_time=.73)
        float_in(self, layers, .18, 2.08)
        self.at("pregnancy risk")
        pregnant = body(pregnant=True)
        risk = mark(p(SIDE+1.22, .51), good=False)
        risk_label = label("Pregnancy risk", TEXT, y=-2.04)
        self.play(ReplacementTransform(whole, pregnant), Create(risk), FadeIn(risk_label), run_time=.73)
        self.at("old lab virus strain")
        old = heading("Old lab strain", GREY)
        self.play(FadeOut(pregnant), FadeOut(risk), FadeOut(risk_label), FadeOut(check), run_time=.32)
        self.play(FadeIn(old), run_time=.30)
        float_in(self, harm, .24, 2.6)
        self.at("retest epidemic strains")
        field = heading("Epidemic strains", RED)
        epidemic_harm = beads([(.57, -.07), (.83, .31), (1.35, .62)], RED, .135)
        harm.clear_updaters()
        self.play(swap(old, field), FadeOut(harm), run_time=.76)
        self.play(FadeIn(epidemic_harm), Create(check), run_time=.50)
        float_in(self, epidemic_harm, .24, 2.6)
        self.at("and pregnant mice")
        rodent = mouse()
        ml = label("Pregnant mice", TEXT, y=-1.62)
        self.play(FadeIn(rodent, shift=LEFT*.23), run_time=.55)
        self.play(FadeIn(ml), run_time=.47)
        float_in(self, rodent, .23, 2.15)
        self.at("in 2022")
        self.play(*(FadeOut(obj) for obj in (rodent, ml, field, epidemic_harm, check, layers)), run_time=.49)
        donor = gut()
        self.play(FadeIn(donor, scale=.91), run_time=.81)
        source = heading("Buchanan et al. · 2022", GOLD)
        self.play(FadeIn(source), run_time=.51)
        self.at("saw glutamate release")
        released = glutamate()
        self.play(LaggedStart(*(GrowFromCenter(d) for d in released), lag_ratio=.38), run_time=1.10)
        self.add(released)
        who = label("One donor", TEXT)
        self.at("one donor's gut")
        self.play(FadeIn(who), run_time=.57)
        float_in(self, donor, .16, 1.9)
        float_in(self, released, .22, 2.0)
        self.at("not human behavior")
        caution = label("Human behavior", TEXT, y=-1.66)
        caution_mark = mark(ORIGIN, good=False).next_to(caution, LEFT, buff=.28)
        self.play(FadeIn(caution), Create(caution_mark), run_time=.62)
        self.at("so checks in")
        self.play(FadeOut(who), FadeOut(caution), FadeOut(caution_mark), run_time=.37)
        native = gut_strip()
        connector = Arrow(p(.07, -.48), p(2.09, -.48), color=GREEN, buff=0, stroke_width=3.4)
        self.play(FadeIn(native), GrowArrow(connector), run_time=.85)
        self.play(FadeIn(label("Native tissue", GREEN, y=-1.83)), run_time=.45)
        self.finish()


class S09UnlockCortex(SpokenScene):
    def construct(self):
        show_plate(self)
        paired = VGroup(cluster(CENTER+p(-1.43, .28), 1.10), cluster(CENTER+p(1.38, -.21), 1.08))
        self.add(paired)
        for i, c in enumerate(paired):
            float_in(self, c, .22, 1.7, i*1.7)
        self.at("first in")
        first = heading("Eiraku and Sasai · 2008", GOLD)
        self.play(FadeIn(first), run_time=.68)
        self.at("colleagues floated")
        stem = label("Embryonic stem cells", PURPLE, y=.61)
        self.play(FadeIn(stem), run_time=.61)
        self.at("are pluripotent cells")
        embryo = label("Pluripotent", PURPLE, y=-.26)
        self.play(FadeIn(embryo), run_time=.54)
        self.at("their clumps built", lead=.82)
        for c in paired:
            c.clear_updaters()
        sheet = cortex()
        incoming = [*paired[0], *paired[1]]
        destinations = [*sheet[2], *sheet[3][:3]]
        # Send each cell toward the closest unoccupied site on the developing rim.
        moves = []
        for precursor in incoming:
            target = min(destinations, key=lambda c: np.linalg.norm(c.get_center()-precursor.get_center()))
            destinations.remove(target)
            moves.append(precursor.animate.scale(.63).move_to(target.get_center()))
        self.play(LaggedStart(*moves, lag_ratio=.049), run_time=1.53)
        self.play(FadeOut(paired), FadeIn(sheet), run_time=.64)
        self.at("a definite inside")
        inside = label("Inside · progenitors", PURPLE, y=.58)
        outside = label("Outside · young neurons", GREEN, y=-.39)
        self.play(swap(stem, inside), FadeOut(embryo), run_time=.70)
        self.play(FadeIn(outside), run_time=.48)
        float_in(self, sheet, .11)
        self.finish()


class S10UnlockZika(SpokenScene):
    def construct(self):
        show_plate(self)
        sheet = cortex()
        self.add(sheet)
        float_in(self, sheet, .13, 1.74)
        self.at("zika virus harms")
        virus = beads([(-2.45,.95), (-2.10,1.30), (-1.65,1.50), (-1.3,1.52),
                       (.95,1.63), (1.65,1.54), (2.48,.95), (2.57,.49),
                       (2.36,-.42), (1.78,-1.18), (-2.65,-.97)], RED, .11)
        self.play(FadeIn(virus), run_time=.75)
        float_in(self, virus, .21, 1.9)
        self.at("in march")
        year = heading("Zika · 2016", RED)
        authors = label("Ming, Song and Tang", GOLD, y=1.01)
        self.play(FadeIn(year), run_time=.54)
        self.play(FadeIn(authors), run_time=.48)
        self.at("tracked zika")
        sheet.clear_updaters()
        sheet.move_to(cortex().get_center())
        virus.clear_updaters()
        marked = [0, 1, 2, 3, 4, 6, 7, 8, 9, 11]
        sites = [sheet[2][i].get_center() + p(.09, .13) for i in marked]
        sites.append(sheet[3][0].get_center())
        self.play(LaggedStart(*(d.animate.move_to(site) for d, site in zip(virus, sites)),
                              lag_ratio=.10), run_time=3.25)
        for i, d in enumerate(virus):
            float_in(self, d, .13, 2.3, i*.75)
        for i in marked:
            float_in(self, sheet[2][i], .085, 2.12, i*.72)
        self.at("infected progenitors far")
        progenitors = label("Progenitors", PURPLE, y=.14)
        self.play(FadeIn(progenitors), run_time=.52)
        for i in marked:
            pulse(sheet[2][i][0], base=2.2, amp=1.05, speed=1.55)
        self.at("or immature neurons")
        young = label("Young neurons", GREEN, y=-.70)
        self.play(FadeIn(young), run_time=.53)
        self.at("killing some")
        lost = [1, 3, 6, 8, 11]
        for i in marked:
            sheet[2][i][0].clear_updaters()
        self.play(LaggedStart(*(sheet[2][i].animate.set_opacity(0) for i in lost), lag_ratio=.35),
                  run_time=1.7)
        self.at("group showed", lead=.9)
        for d in virus:
            d.clear_updaters()
        for c in sheet[2]:
            c.clear_updaters()
        outline = DashedVMobject(cortex()[0].set_fill(opacity=0).set_stroke(TEXT, 2.8, .75), num_dashes=42)
        control = label("Uninfected control", TEXT, y=-.44)
        rehen = label("Rehen’s group", GOLD, y=1.01)
        self.play(FadeIn(outline), FadeOut(progenitors), FadeOut(young), swap(authors, rehen), run_time=.62)
        self.play(sheet.animate.scale(.70, about_point=CENTER), virus.animate.scale(.70, about_point=CENTER),
                  FadeIn(control), run_time=2.44)
        self.finish()


def bound_bar(text, bound, lower, y, color):
    """Show the stated bound on a common 0–100% scale."""
    width = 3.75
    center = p(SIDE, y)
    track = RoundedRectangle(width=width, height=.30, corner_radius=.10,
                             color=GREY, stroke_width=1.8, fill_opacity=.12).move_to(center)
    if lower:
        fill = Rectangle(width=width*bound-.065, height=.17, stroke_width=0,
                         fill_color=color, fill_opacity=.86)
        fill.move_to(center + LEFT * (width - fill.width) / 2 + RIGHT * .032)
        bars = VGroup(track, fill)
    else:
        # At this scale the first 1% is narrower than the track's corner.
        # A marker at the exact threshold shows the bound without exaggerating the fill.
        x = center[0] - width/2 + width*bound
        marker = Line(p(x, y-.16), p(x, y+.16), color=color, stroke_width=3.7)
        bars = VGroup(track, marker)
    return VGroup(bars, label(text, color, y=y+.52))


class S11UnlockGut(SpokenScene):
    def construct(self):
        show_plate(self)
        tissue = gut()
        self.add(tissue)
        float_in(self, tissue, .17, 1.85)
        self.at("enterochromaffin cells", lead=.48)
        rare = tissue[2][3]
        self.play(rare.animate.set_color(YELLOW), run_time=.64)
        highlight = label("Enterochromaffin cell", YELLOW, y=1.48)
        self.play(FadeIn(highlight), run_time=.49)
        pulse(rare[0], base=3.4, amp=2.5, speed=2.4)
        self.at("are under 1")
        cells = bound_bar("<1% of lining cells", .01, False, -.16, BLUE)
        self.play(FadeIn(cells), run_time=.70)
        self.at("90 % of")
        serotonin = bound_bar(">90% of serotonin", .90, True, -1.38, YELLOW)
        self.play(FadeIn(serotonin), run_time=.70)
        self.at("2017 bellono")
        source = heading("Bellono et al. · 2017", GOLD)
        self.play(FadeIn(source), run_time=.62)
        self.at("genetically tagged them")
        tissue.clear_updaters()
        rare[0].clear_updaters()
        badge = SurroundingRectangle(rare, color=YELLOW, stroke_width=2.5, corner_radius=.10, buff=.08)
        self.play(Create(badge), run_time=.74)
        float_in(self, badge, .025, 2.2)
        self.at("mouse intestinal organoids")
        organoid_heading = label("Mouse intestinal organoid", BLUE, x=DISH[0], y=-3.36, width=6.0)
        self.play(FadeOut(cells), FadeOut(serotonin), swap(highlight, organoid_heading), run_time=.81)
        self.at("checked native tissue")
        native = gut_strip(tagged=True)
        link = Arrow(p(.07, -.48), p(2.08, -.48), color=GREEN, buff=0, stroke_width=3.4)
        self.play(FadeIn(native), GrowArrow(link), run_time=.73)
        native_label = label("Native tissue", GREEN, y=-1.84)
        self.play(FadeIn(native_label), run_time=.43)
        self.at("across organs")
        self.play(FadeOut(native), FadeOut(link), FadeOut(native_label), FadeOut(badge),
                  FadeOut(organoid_heading), FadeOut(source), run_time=.54)
        whole = body()
        self.play(FadeIn(whole, shift=RIGHT*.17), run_time=.95)
        float_in(self, tissue, .16, 1.9)
        self.at("tissue rules")
        self.play(FadeIn(heading("Tissue behavior", GOLD)), run_time=.62)
        self.at("whole body")
        self.play(FadeIn(label("Whole body", GREY, y=-2.12)), run_time=.53)
        self.finish()


class S12End(EndCard):
    LINE = "Reprogrammed stem cells self-organize into mini-organs\nthat test tissue, not whole bodies."
