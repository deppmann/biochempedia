"""PET imaging, timed to the recorded narration.

Colour map from the methods series: GREY = anatomy and membranes, BLUE =
scanner and imaging apparatus, PURPLE = enzymes and protein deposits,
YELLOW = glucose, tracer and measured signal, ORANGE = added compounds,
TEAL = oxygen and sodium, GREEN = retained products, RED = inhibition or a
limit of interpretation, GOLD = dates and the take-home rule.
"""
from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
BODY = np.array([-4.15, 0.22, 0])
ZOOM = np.array([2.30, 0.22, 0])
CHEST = BODY + np.array([0.62, -0.20, 0])
BRAIN = BODY + UP * 1.83
WINDOW_RADIUS = 2.8
QUESTION = "Does a bright spot prove a tumor?"
DRUG_CHANGE, PLACEBO_CHANGE = 11.6, 19.3


def p(x, y):
    return np.array([x, y, 0.0])


def outline(points, center, color=GREY, fill=0.44, width=3):
    shape = VMobject(stroke_color=color, stroke_width=width,
                     fill_color=color, fill_opacity=fill)
    shape.set_points_smoothly([center + p(*point) for point in [*points, points[0]]])
    return shape


def body():
    torso = outline([
        (0, 2.42), (0.70, 2.08), (0.68, 1.45), (0.55, 1.13),
        (0.70, 0.91), (1.48, 0.64), (1.84, -0.17), (1.90, -1.45),
        (1.81, -2.40), (1.35, -2.42), (1.19, -1.17), (1.13, -2.57),
        (-1.13, -2.57), (-1.19, -1.17), (-1.35, -2.42), (-1.81, -2.40),
        (-1.90, -1.45), (-1.84, -0.17), (-1.48, 0.64), (-0.70, 0.91),
        (-0.55, 1.13), (-0.68, 1.45), (-0.70, 2.08)
    ], BODY, fill=0.48, width=4)
    brain = outline([
        (-0.45, -0.07), (-0.48, 0.14), (-0.30, 0.34), (-0.06, 0.35),
        (0.12, 0.36), (0.33, 0.30), (0.48, 0.16), (0.43, -0.10),
        (0.22, -0.22), (-0.03, -0.24), (-0.26, -0.20)
    ], BRAIN, fill=0.33, width=2.5)
    midline = ArcBetweenPoints(BRAIN + UP * 0.31, BRAIN + DOWN * 0.20,
                               angle=0.38, color=GREY, stroke_width=2)
    return VGroup(torso, brain, midline)


def window():
    return Circle(radius=WINDOW_RADIUS, stroke_color=BLUE, stroke_width=3,
                  fill_color=BLUE, fill_opacity=0.26).move_to(ZOOM)


def link(source):
    end = ZOOM + WINDOW_RADIUS * normalize(source - ZOOM)
    return Line(source, end, color=BLUE, stroke_width=3, stroke_opacity=0.68)


def glow(center, color=YELLOW, strength=1):
    return VGroup(*[
        Dot(center, radius=r, color=color, fill_opacity=o * strength)
        for r, o in [(0.56, 0.16), (0.36, 0.28), (0.20, 0.54), (0.095, 1)]
    ])


def breathing_glow(center, strength=1):
    light = glow(center, strength=strength)
    light.age, light.magnification = 0.0, 1.0

    def breathe(m, dt):
        m.age += dt
        magnification = 1.0 + 0.14 * (1 - np.cos(m.age * TAU / 3.5))
        m.scale(magnification / m.magnification, about_point=center)
        m.magnification = magnification

    return light.add_updater(breathe)


def neck_hotspots():
    return VGroup(*[breathing_glow(BODY + p(x, 0.73)) for x in [-0.78, 0.78]])


def cell(center=ZOOM, scale=1):
    membrane = outline([
        (-1.77, 0), (-1.62, 0.65), (-1.00, 1.17), (-0.10, 1.29),
        (0.92, 1.11), (1.60, 0.62), (1.78, -0.11), (1.49, -0.76),
        (0.72, -1.16), (-0.24, -1.31), (-1.14, -1.06), (-1.65, -0.60)
    ], ZOOM, fill=0.32, width=4).scale(scale).move_to(center)
    nucleus = Ellipse(width=0.78 * scale, height=0.60 * scale, color=GREY,
                      stroke_width=2, fill_opacity=0.30)
    nucleus.move_to(center + scale * p(0.73, 0.42))
    return VGroup(membrane, nucleus)


def ring():
    scanner = Ellipse(width=4.39, height=1.04, stroke_color=BLUE, stroke_width=9,
                      fill_opacity=0).move_to(CHEST + LEFT * 0.62)
    modules = VGroup(*[
        RoundedRectangle(width=0.26, height=0.18, corner_radius=0.05,
                         stroke_width=0, fill_color=BLUE, fill_opacity=1)
        .move_to(scanner.point_at_angle(a))
        for a in np.linspace(0, TAU, 12, endpoint=False)
    ])
    return VGroup(scanner, modules)


def cluster(center=ZOOM):
    return VGroup(cell(center + p(-0.87, 0.54), 0.49),
                  cell(center + p(0.85, 0.45), 0.48),
                  cell(center + p(0.02, -0.68), 0.53))


def flux(start, end, color=YELLOW, count=3, period=3.0, radius=0.23, bend=0.20):
    """A stream of schematic tokens along a defined route, with soft entry and exit."""
    path = end - start
    normal = normalize(np.cross(OUT, path))
    particles = VGroup()
    for i in range(count):
        dot = Dot(radius=radius, color=color, stroke_width=0)
        dot.phase = i / count
        dot.lane = (i - (count - 1) / 2) * bend

        def drift(mob, dt):
            mob.phase = (mob.phase + dt / period) % 1
            q = mob.phase
            mob.move_to(start + q * path + mob.lane * np.sin(PI * q) * normal)
            mob.set_fill(opacity=min(1, q * 8, (1 - q) * 8))

        dot.add_updater(drift, call_updater=True)
        particles.add(dot)
    return particles


def trapped(center=ZOOM, scale=1, count=6):
    slots = [(-1.12, -0.30), (0.68, -0.58), (-0.33, 0.56),
             (0.12, -0.38), (-0.70, -0.74), (1.08, -0.31)]
    return VGroup(*[
        bob(Dot(center + scale * p(*pos), radius=0.13 if scale < 0.6 else 0.20, color=YELLOW),
            amp=0.11 * scale, speed=2.4, seed=i)
        for i, pos in enumerate(slots[:count])
    ])


def bottom(text, color=TEXT, size=32):
    return caption(text, size=size, color=color, y=-3.28)


def label(text, x, y, color=TEXT, size=30, width=6.1):
    return fit_text(text, max_w=width, size=size, min_size=28, color=color).move_to(p(x, y))


def jaw_pair(center=ZOOM, opened=True):
    offset = 0.73 if opened else 0.53
    upper = ArcBetweenPoints(center + p(-1.0, offset - 0.23), center + p(1.0, offset - 0.23),
                             angle=-1.36, color=PURPLE, stroke_width=24)
    lower = ArcBetweenPoints(center + p(-1.0, -offset + 0.23), center + p(1.0, -offset + 0.23),
                             angle=1.36, color=PURPLE, stroke_width=24)
    return VGroup(upper, lower)


def isotope_token():
    badge = Dot(radius=0.49, color=YELLOW)
    isotope = T("¹⁸F", 34, BG).move_to(badge)
    return VGroup(badge, isotope)


def question_world():
    return body(), ring(), link(CHEST), glow(CHEST), window(), cluster()


def question_label():
    return question_card(QUESTION, size=34, y=-3.25).shift(RIGHT * 2.60)


def hotspot_label():
    return label("FDG-PET hotspot", -4.13, -3.06, YELLOW, width=4.0)


def question_scope():
    return scope_tag(size=28, color=TEXT).move_to(p(-4.15, 3.20))


class S01Hook(SpokenScene, TitleCard):
    # The script's first card is a narrated hook. Its title is revealed in s02.
    TITLE = "Lighting Up Living Chemistry With PET"
    LESSON = "Positron Emission Tomography (PET)"

    def construct(self):
        self.at("how can you")
        light = breathing_glow(CHEST, 0.57)
        self.add(body(), link(CHEST), light)
        view, tissue = window(), cell()
        self.play(FadeIn(view), run_time=0.70)
        self.play(FadeIn(tissue), run_time=0.65)
        stream = flux(ZOOM + p(-2.35, -0.26), ZOOM + p(0.86, -0.22))
        self.add(stream)
        self.at("positron emission tomography")
        name = bottom("Positron emission tomography (PET)", BLUE)
        self.play(FadeIn(name), run_time=0.5)
        self.at("tracks radioactive tracers")
        tracer_name = label("Radioactive tracer", 2.30, 2.10, YELLOW, width=4.0)
        self.play(FadeIn(tracer_name), run_time=0.48)
        self.at("map activity")
        light.clear_updaters()
        self.play(Transform(light, glow(CHEST)), run_time=0.78)
        self.finish()


class S02Title(TitleCard):
    TITLE = S01Hook.TITLE
    LESSON = S01Hook.LESSON

    def construct(self):
        self.add(body(), breathing_glow(CHEST, 0.57))
        title = T(self.TITLE.replace("Living Chemistry", "Living\nChemistry"), 46, font=TITLE_FONT,
                  line_spacing=0.9).move_to(p(2.15, 0.33))
        self.play(FadeIn(title), run_time=0.22)
        self.wait(1.06)
        self.play(FadeOut(title), run_time=0.22)


class S03Trap(SpokenScene):
    def construct(self):
        self.at("zoom into")
        self.add(body(), link(CHEST), glow(CHEST, strength=0.57), window())
        self.play(FadeIn(cell()), run_time=0.64)
        view_tag = scope_tag(size=28, color=TEXT)
        glucose = Dot(ZOOM + p(-2.08, -0.37), color=YELLOW, radius=0.51)
        self.play(FadeIn(view_tag), FadeIn(glucose), run_time=0.46)
        self.play(glucose.animate.move_to(ZOOM + p(0, -0.07)), run_time=4.0)
        self.at("breakdown of glucose")
        glucose_name = label("Glucose", 2.30, 1.98, YELLOW)
        self.play(FadeIn(glucose_name), run_time=0.45)
        self.at("step one is a trap")
        pocket = jaw_pair(ZOOM + DOWN * 0.07)
        self.play(Create(pocket), run_time=1.58)
        self.at("the enzyme")
        hexo = label("Hexokinase", 2.30, 1.98, PURPLE)
        self.play(swap(glucose_name, hexo, 0.60), Transform(pocket, jaw_pair(ZOOM + DOWN * 0.07, False)),
                  run_time=0.60)
        atp = chip("ATP", ORANGE, size=28, pad=0.17).move_to(ZOOM + p(0.74, -1.78))
        badge = Dot(radius=0.23, color=BG, stroke_width=0).move_to(p(atp.get_left()[0] - 0.30, -1.56))
        charge = VGroup(badge, T("−", 34, GREEN).move_to(badge))
        self.at("moves a phosphate")
        self.play(FadeIn(atp, shift=UP * 0.35), FadeIn(charge, shift=UP * 0.35), run_time=0.86)
        self.at("onto glucose")
        self.play(FadeOut(pocket), run_time=0.25)
        self.play(charge.animate.move_to(glucose.get_center()), FadeOut(atp),
                  run_time=0.61)
        self.at("negative charge")
        carbon = label("Phosphate at carbon 6", 2.30, 1.76, GREEN, width=4.35)
        self.play(swap(hexo, carbon, 0.62))
        tagged = VGroup(glucose, charge)
        self.play(tagged.animate.shift(LEFT * 1.15 + DOWN * 0.05), run_time=1.0)
        self.play(tagged.animate.shift(RIGHT * 2.13 + DOWN * 0.10), run_time=1.12)
        self.play(tagged.animate.shift(LEFT * 0.85 + DOWN * 0.11), run_time=1.40)
        self.finish()


class S04Fdg(SpokenScene):
    def construct(self):
        self.at("fdg pet uses")
        tissue = cell()
        self.add(body(), link(CHEST), window(), tissue, glow(CHEST, strength=0.57))
        token = Dot(ZOOM + p(-2.25, -0.40), radius=0.49, color=YELLOW)
        self.play(FadeIn(token), run_time=0.42)
        self.play(token.animate.move_to(ZOOM + p(-0.62, -0.12)), run_time=2.18)
        analog = label("Glucose analog", 2.30, 1.98, YELLOW)
        self.play(FadeIn(analog), run_time=0.44)
        self.at("radioactive fluorine")
        fluorine = label("Radioactive fluorine-18", 2.30, 1.76, YELLOW, width=4.30)
        decoy = isotope_token().move_to(ZOOM + DOWN * 0.20)
        self.play(swap(analog, fluorine), Transform(token, decoy[0]), run_time=0.87)
        self.play(FadeIn(decoy[1]), run_time=0.28)
        self.at("it is trapped")
        pocket = jaw_pair(ZOOM + DOWN * 0.20, False)
        self.play(Create(pocket), FadeOut(fluorine), run_time=1.72)
        self.at("the scanner detects")
        detector = ring()
        self.play(FadeIn(detector), FadeOut(pocket), run_time=0.70)
        flashes = flux(CHEST, BODY + p(-1.86, -0.44), count=2, period=1.38, radius=0.24)
        view_tracer = flux(ZOOM + p(-0.67, -0.66), ZOOM + p(-1.94, 0.68),
                           count=2, period=1.75, radius=0.23)
        beam = link(CHEST)
        detector_signal = flux(beam.get_end(), beam.get_start(), color=GOLD, count=2,
                               period=2.05, radius=0.23, bend=0)
        self.add(flashes, view_tracer, detector_signal)
        self.at("light up")
        self.play(FadeIn(breathing_glow(CHEST)), run_time=0.75)
        self.at("many tumors")
        self.play(FadeOut(tissue), FadeOut(token), FadeOut(decoy[1]), FadeOut(view_tracer),
                  run_time=0.32)
        tumor = cluster()
        self.play(FadeIn(tumor), run_time=0.56)
        accumulation = VGroup(*[trapped(m.get_center(), 0.46, count=4) for m in tumor])
        tumor_name = label("Tumor (schematic)", 2.30, 2.05, TEXT)
        self.play(FadeIn(accumulation), FadeIn(tumor_name), run_time=0.60)
        self.at("with oxygen present")
        oxygen = flux(ZOOM + p(-1.63, -1.69), ZOOM + p(0.89, -1.72), TEAL,
                      count=3, period=2.5, bend=0.02)
        self.add(oxygen)
        self.play(FadeIn(label("Oxygen", 2.30, -2.16, TEAL, width=1.7)), run_time=0.42)
        self.at("the warburg effect")
        self.play(FadeIn(bottom("Warburg effect", GOLD)), run_time=0.43)
        self.finish()


class S05PredictQ(SpokenScene):
    def construct(self):
        self.at("picture a bright spot")
        self.add(*question_world(), hotspot_label(), question_scope())
        flow = flux(ZOOM + p(-2.49, 0.33), ZOOM + p(0.98, 0.40), period=2.15)
        self.add(flow)
        self.at("those cells are pulling")
        retained = trapped(ZOOM + p(0.02, -0.68), 0.48, count=4)
        self.play(FadeIn(retained), run_time=0.70)
        self.at("predict")
        self.play(FadeIn(question_label()), run_time=0.55)
        settling = self.narration_s - self.elapsed() - 0.30
        self.wait(settling)
        self.play(FadeOut(flow), FadeOut(retained), FadeIn(pause_tokens()), run_time=0.62)
        self.finish()


def pause_tokens():
    return VGroup(*[
        Dot(ZOOM + p(x, y), color=YELLOW, radius=0.13)
        for x, y in [(-1.91, 0.34), (-0.77, 0.40), (0.93, 0.33),
                     (-0.38, -0.66), (0.20, -0.93)]
    ])


class S06PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(*question_world(), hotspot_label(), question_scope(),
                 pause_tokens(), question_label())
        self.wait(4.5)


class S07FdgLimits(SpokenScene):
    def construct(self):
        self.at("no fdg pet")
        torso, detector, beam, spot, view, cells = question_world()
        scope = question_scope()
        hotspot = hotspot_label()
        tokens = pause_tokens()
        self.add(torso, detector, beam, spot, view, cells, hotspot, scope, tokens)
        prompt = question_label()
        self.add(prompt)
        answer = bottom("No: fast glucose uptake", GOLD).shift(RIGHT * 3.0)
        uptake = flux(ZOOM + p(-2.40, 0.32), ZOOM + p(1.18, 0.47), period=1.74)
        self.remove(tokens)
        self.add(uptake)
        self.play(swap(prompt, answer, 0.75), run_time=0.75)
        self.at("reports glucose uptake")
        retained = trapped(ZOOM + p(0.02, -0.68), 0.48, count=4)
        self.play(FadeIn(retained), run_time=0.55)
        self.at("enflamed tissue")
        self.play(FadeOut(cells), FadeOut(retained), FadeOut(uptake), run_time=0.35)
        inflamed = cell(ZOOM + p(-1.24, 0), 0.61)
        brown = cell(ZOOM + p(1.25, 0), 0.61)
        divider = Line(ZOOM + DOWN * 1.86, ZOOM + UP * 1.77, color=BLUE, stroke_width=3)
        self.play(FadeIn(inflamed), Create(divider), run_time=0.54)
        inflammation = label("Inflamed\ntissue", 1.03, 1.51, TEXT, width=2.1)
        inflamed_flow = flux(ZOOM + p(-2.56, -0.35), ZOOM + p(-0.69, -0.33), period=1.85)
        self.add(inflamed_flow)
        self.play(FadeIn(inflammation), run_time=0.42)
        self.at("in a cold adult")
        self.play(FadeIn(brown), run_time=0.59)
        cold = label("Brown fat\nin cold", 3.58, 1.51, TEXT, width=2.12)
        brown_flow = flux(ZOOM + p(0.30, -0.32), ZOOM + p(2.37, -0.38), period=1.85)
        neck = neck_hotspots()
        self.add(brown_flow)
        self.play(FadeIn(cold), run_time=0.44)
        self.at("can light up")
        petct = label("PET-CT", -4.13, -3.06, BLUE)
        self.play(FadeIn(neck), swap(hotspot, petct, 0.66), FadeOut(spot),
                  Transform(beam, link(BODY + p(0.78, 0.73))), FadeOut(detector),
                  run_time=0.68)
        self.finish()


def synapse():
    upper = outline([(-2.15, 0.47), (-1.28, 0.78), (0, 0.81), (1.28, 0.78),
                     (2.15, 0.47), (1.30, 0.10), (0, 0.05), (-1.30, 0.10)],
                    ZOOM, fill=0.40, width=3)
    lower = outline([(-2.15, -1.78), (-1.20, -1.47), (0, -1.42), (1.20, -1.47),
                     (2.15, -1.78), (1.36, -2.09), (0, -2.33), (-1.36, -2.09)],
                    ZOOM, fill=0.40, width=3)
    enzyme = VGroup(*[
        Arc(radius=0.25, start_angle=0.36, angle=TAU - 0.72, color=PURPLE,
            stroke_width=9).move_to(ZOOM + p(x, -0.68))
        for x in [-0.92, 0.0, 0.92]
    ])
    return VGroup(upper, lower), enzyme


class S08MechanismAndGuide(SpokenScene):
    def construct(self):
        self.at("other pet tracers")
        anatomy, beam, spot, view = body(), link(BODY + p(0.78, 0.73)), glow(BRAIN), window()
        neck = neck_hotspots()
        self.add(anatomy, neck, beam, view)
        self.play(Transform(beam, link(BRAIN)), FadeIn(spot), FadeOut(neck), run_time=0.75)
        membranes, enzymes = synapse()
        self.play(FadeIn(membranes), run_time=0.30)
        self.at("track enzymes")
        self.play(FadeIn(enzymes), run_time=0.54)
        activity = flux(ZOOM + p(-1.85, -0.94), ZOOM + p(1.77, -0.93),
                        count=4, period=2.52)
        self.add(activity)
        scope = scope_tag(size=28, color=TEXT)
        self.add(scope)
        self.at("protein deposits")
        types = label("Enzymes or protein deposits", 2.30, 1.79, PURPLE, width=4.20)
        self.play(FadeIn(types), run_time=0.46)
        self.at("in patients with probable")
        case = bottom("Probable Alzheimer disease")
        self.play(FadeOut(types), FadeIn(case), run_time=0.50)
        self.at("the drug")
        drug = chip("Donepezil", ORANGE, size=28).move_to(p(2.30, 2.05))
        plugs = VGroup(*[
            RoundedRectangle(width=0.24, height=0.37, corner_radius=0.075,
                             stroke_width=0, fill_color=ORANGE, fill_opacity=1)
            .move_to(ZOOM + p(x + 0.22, -0.68))
            for x in [-0.92, 0.0, 0.92]
        ])
        self.play(FadeIn(drug), run_time=0.60)
        self.at("cutting cortical")
        self.play(LaggedStart(*[FadeIn(block, shift=DOWN * 0.24) for block in plugs],
                              lag_ratio=0.35),
                  activity.animate.set_opacity(0), run_time=1.27)
        self.remove(activity)
        enzyme_name = label("Acetylcholinesterase", 2.30, 1.34, PURPLE, width=3.95)
        self.play(FadeIn(enzyme_name), Transform(spot, glow(BRAIN, strength=0.33)), run_time=0.54)
        self.at("that enzyme breaks")
        acetylcholine = flux(ZOOM + p(-1.54, -0.36), ZOOM + p(1.48, -0.35),
                             color=GREEN, count=4, period=4.1, radius=0.31, bend=0.20)
        self.add(acetylcholine)
        retained_name = bottom("Acetylcholine lingers", GREEN)
        self.play(swap(case, retained_name), run_time=0.74)
        self.at("that measures mechanism")
        mechanism = label("Mechanism", -4.20, -3.15, GOLD)
        clinical = label("Not clinical benefit", 1.95, -3.15, RED)
        split = Line(p(-1.31, -3.50), p(-1.31, -2.79), color=GREY, stroke_width=3)
        self.play(FadeOut(retained_name), run_time=0.28)
        self.play(FadeIn(mechanism), Create(split), run_time=0.52)
        self.at("not clinical benefit")
        self.play(FadeIn(clinical), run_time=0.46)
        self.at("the guiding idea")
        guide = label("Maps living chemistry", -4.12, -3.15, GOLD, width=4.7)
        self.play(swap(mechanism, guide, 0.84), FadeOut(drug), run_time=0.84)
        self.finish()


def cortex_map():
    target_center = ZOOM + p(-0.13, 1.22)
    target = VGroup(*[
        Circle(radius=r, color=GREY, stroke_width=2.5, fill_opacity=0.27)
        .move_to(target_center)
        for r in [0.86, 0.63, 0.39, 0.16]
    ])
    cortex = outline([
        (-2.02, -0.68), (-1.41, -0.64), (-0.63, -0.20), (0, -0.03),
        (0.64, -0.20), (1.43, -0.65), (2.02, -0.69), (2.02, -1.07),
        (1.18, -1.12), (0.62, -1.45), (0, -1.69), (-0.62, -1.43),
        (-1.35, -1.11), (-2.02, -1.07)
    ], ZOOM, fill=0.56, width=4)
    return target, cortex, target_center


class S09UnlockedV1(SpokenScene):
    def construct(self):
        self.at("the glucose analog")
        self.add(body(), link(BRAIN), breathing_glow(BRAIN), window(),
                 scope_tag(size=28, color=TEXT))
        target, cortex, center = cortex_map()
        self.play(Create(target), run_time=1.2)
        self.play(FadeIn(cortex), run_time=1.05)
        probe = VGroup(glow(center).scale(0.86), Dot(center, color=YELLOW, radius=0.22))
        self.play(FadeIn(probe), run_time=0.45)
        self.at("in 1988")
        study = bottom("Tootell and colleagues · 1988", GOLD)
        self.play(FadeIn(study), probe.animate.shift(LEFT * 0.62 + DOWN * 0.16),
                  run_time=1.90)
        self.at("mapped macaque visual cortex")
        v1 = label("Macaque V1 cortex", 2.30, 3.31, TEXT, width=4.0)
        self.play(FadeIn(v1), probe.animate.move_to(center + p(0.55, -0.34)),
                  run_time=1.55)
        self.at("with 2d oxyglucose")
        tracer = bottom("2-deoxyglucose", YELLOW)
        self.play(swap(study, tracer), run_time=0.73)
        self.at("marks active cells")
        point = Dot(ZOOM + p(1.25, -0.86), color=YELLOW, radius=0.25)
        self.play(FadeIn(point), probe.animate.shift(LEFT * 0.28), run_time=0.75)
        self.at("near the fovea")
        fovea = label("Fovea", 3.71, 1.61, YELLOW, width=1.3)
        self.play(probe.animate.move_to(center), FadeIn(fovea), run_time=0.9)
        mapping = Line(center + DOWN * 0.15, ZOOM + DOWN * 0.08,
                       color=YELLOW, stroke_width=3, stroke_opacity=0.65)
        self.play(point.animate.move_to(ZOOM + DOWN * 0.81), Create(mapping), run_time=1.0)
        self.at("about 15 millimeters", lead=0.6)
        center_bar = Line(ZOOM + p(0, -0.18), ZOOM + p(0, -1.49), color=YELLOW,
                          stroke_width=22)
        amount = bottom("≈15 mm of cortex per degree", YELLOW)
        self.play(GrowFromCenter(center_bar), FadeOut(point), swap(tracer, amount, 1.0),
                  run_time=1.0)
        self.at("estimates vary")
        comparison = Line(ZOOM + p(-1.54, -0.74), ZOOM + p(-1.54, -1.00),
                          color=YELLOW, stroke_width=8)
        self.play(FadeIn(comparison), probe.animate.shift(LEFT * 0.54),
                  cortex.animate.set_fill(opacity=0.94), run_time=1.38)
        self.at("is a macaque value")
        limit = bottom("≈15 mm per degree in macaques", YELLOW)
        self.play(swap(amount, limit, 0.65), probe.animate.move_to(center),
                  cortex.animate.set_fill(opacity=0.56), run_time=1.65)
        self.finish()


def glial_world():
    astro = outline([(-1.9, -0.22), (-1.53, 0.33), (-1.31, 0.95),
                     (-0.87, 0.66), (-0.32, 0.82), (-0.24, 0.25),
                     (0.34, -0.04), (-0.22, -0.44), (-0.29, -1.19),
                     (-0.86, -0.88), (-1.45, -1.20), (-1.52, -0.59)],
                    ZOOM, fill=0.54, width=4)
    neuron = outline([(0.69, -0.33), (0.96, -0.04), (1.22, 0.08),
                      (1.45, 0.87), (1.58, 0.38), (1.76, -0.09),
                      (2.16, -0.51), (1.63, -0.68), (1.23, -1.29),
                      (1.34, -0.71), (0.96, -0.63)],
                     ZOOM, fill=0.45, width=3)
    return astro, neuron


class S10UnlockedGlia(SpokenScene):
    def construct(self):
        self.at("in 1994")
        self.add(body(), link(BRAIN), breathing_glow(BRAIN, 0.58), window(),
                 scope_tag(size=28, color=TEXT))
        astro, neuron = glial_world()
        self.play(GrowFromCenter(astro), run_time=1.22)
        study = bottom("Pellerin and Magistretti · 1994", GOLD)
        self.play(FadeIn(study), run_time=0.45)
        self.at("gave glutamate")
        glutamate = flux(ZOOM + p(-1.96, 1.43), ZOOM + p(-0.73, 0.16), ORANGE,
                         period=2.25, count=3, radius=0.32)
        self.add(glutamate)
        glutamate_name = label("Glutamate", 2.30, 2.28, ORANGE)
        self.play(FadeIn(glutamate_name), run_time=0.45)
        self.at("astrocytes glial cells")
        astro_name = label("Astrocyte", 1.26, -1.54, TEXT)
        self.play(FadeIn(astro_name), run_time=0.46)
        self.at("the cells took up")
        uptake = flux(ZOOM + p(-2.47, -0.46), ZOOM + p(-0.74, -0.15), YELLOW,
                      period=1.65, count=3)
        self.add(uptake)
        uptake_name = bottom("2-deoxyglucose uptake rises", YELLOW)
        self.play(swap(study, uptake_name), run_time=0.66)
        self.at("released more lactate")
        released = flux(ZOOM + p(-0.53, -0.46), ZOOM + p(1.72, -0.37), GREEN,
                        period=1.65, count=4)
        self.add(released)
        lactate_name = label("Lactate", 3.96, 1.36, GREEN)
        self.play(FadeIn(lactate_name), run_time=0.42)
        self.at("blocking the sodium pump")
        pump = RoundedRectangle(width=0.68, height=0.40, corner_radius=0.13,
                                stroke_color=PURPLE, stroke_width=3,
                                fill_color=PURPLE, fill_opacity=0.78)
        pump.move_to(ZOOM + p(-0.49, 0.61))
        blocker = RoundedRectangle(width=0.80, height=0.22, corner_radius=0.08,
                                   stroke_width=0, fill_color=RED, fill_opacity=1)
        blocker.move_to(pump.get_center())
        self.play(FadeIn(pump), run_time=0.48)
        stop = bottom("Ouabain blocks the sodium pump", RED)
        self.play(FadeIn(blocker, shift=DOWN * 0.35), swap(uptake_name, stop, 0.75),
                  run_time=0.75)
        self.play(FadeOut(uptake), FadeOut(released), FadeOut(lactate_name),
                  run_time=0.36)
        self.at("their explanation")
        sodium = flux(ZOOM + p(-1.47, 1.53), ZOOM + p(-0.34, 0.17), TEAL,
                      period=2.4, count=3)
        self.play(FadeOut(blocker), FadeOut(stop), run_time=0.38)
        self.add(sodium)
        sodium_name = label("Na⁺", 3.51, 1.71, TEAL)
        self.play(FadeIn(sodium_name), run_time=0.44)
        self.at("pumping it out")
        outward = flux(ZOOM + p(-0.54, 0.57), ZOOM + p(0.68, 1.65),
                       TEAL, count=2, period=1.6)
        self.add(outward)
        chain = bottom("Na⁺ in  →  pump uses ATP  →  glycolysis", GOLD)
        self.play(FadeIn(chain), run_time=0.63)
        self.at("they proposed")
        self.play(FadeIn(neuron), FadeOut(glutamate_name), FadeOut(sodium_name),
                  run_time=0.65)
        lactate_to_neuron = flux(ZOOM + p(-0.49, -0.46), ZOOM + p(1.48, -0.47),
                                 GREEN, period=1.6, count=4)
        self.add(lactate_to_neuron)
        self.play(FadeIn(label("Neuron", 3.50, -1.48)),
                  FadeIn(label("Lactate", 3.96, 1.36, GREEN)),
                  swap(chain, bottom("Proposed fuel for active neurons", GOLD), 0.8),
                  run_time=0.80)
        self.finish()


def amyloid_world():
    return body(), link(BRAIN), breathing_glow(BRAIN)


def trial_chart():
    plot = Plot(box=(0.0, 6.33, -1.65, 2.30), xr=(0, 3), yr=(0, 22),
                yticks=[0, 10, 20], ylabel="Change in centiloids", size=28,
                label_size=30, color=TEXT)
    names = VGroup(label("Solanezumab", plot.pt(0.86, 0)[0], -2.10, BLUE, width=2.40),
                   label("Placebo", plot.pt(2.14, 0)[0], -2.10, ORANGE, width=2.35))
    time = label("Over 240 weeks", 3.15, -2.64, TEXT)
    return plot, names, time


def trial_bar(plot, x, value, color):
    start = plot.pt(x, 0)
    top = plot.pt(x, value)
    bar = Rectangle(width=1.19, height=top[1] - start[1], stroke_color=color,
                    stroke_width=2.5, fill_color=color, fill_opacity=0.85)
    return bar.move_to((start + top) / 2)


def trial_values(plot):
    return VGroup(label(f"+{DRUG_CHANGE:.1f}", plot.pt(0.86, 0)[0], plot.pt(0.86, DRUG_CHANGE)[1] + 0.29, BLUE),
                  label(f"+{PLACEBO_CHANGE:.1f}", plot.pt(2.14, 0)[0], plot.pt(2.14, PLACEBO_CHANGE)[1] + 0.29, ORANGE))


class S11UnlockedAmyloid(SpokenScene):
    def construct(self):
        self.at("finally the")
        anatomy, beam, glow_brain = amyloid_world()
        self.add(anatomy, beam, glow_brain)
        view = window()
        self.play(FadeIn(view), run_time=0.53)
        study = bottom("A4 study · 2023", GOLD)
        self.play(FadeIn(study), run_time=0.47)
        self.at("tracked amyloid")
        plaques = VGroup(*[
            outline([(-0.54, -0.01), (-0.37, 0.34), (-0.11, 0.29), (0.17, 0.48),
                     (0.44, 0.28), (0.58, -0.05), (0.32, -0.31),
                     (0.04, -0.26), (-0.25, -0.36), (-0.43, -0.24)],
                    ZOOM + p(x, y), color=PURPLE, fill=0.57, width=3)
            for x, y in [(-0.99, -0.43), (0.33, 0.47), (0.99, -0.86)]
        ])
        self.play(LaggedStart(*[FadeIn(patch) for patch in plaques], lag_ratio=0.40),
                  run_time=0.96)
        tracer = flux(ZOOM + p(-1.9, 0.51), ZOOM + p(1.19, -0.51),
                      count=4, period=2.3)
        self.add(tracer)
        plaque = label("Amyloid plaques", 2.30, 2.12, PURPLE)
        self.play(FadeIn(plaque), run_time=0.53)
        self.at("for 240 weeks")
        period = bottom("A4 study · 240 weeks", GOLD)
        self.play(swap(study, period, 0.78))
        self.at("got an antibody")
        drug = label("Solanezumab", 1.39, -1.24, BLUE, width=2.35)
        self.play(FadeIn(drug), run_time=0.58)
        self.at("or placebo")
        control = label("Placebo", 3.75, -1.24, ORANGE, width=1.48)
        self.play(FadeIn(control, shift=UP * 0.18), run_time=0.54)
        self.at("uses centalloids")
        self.play(*[FadeOut(m) for m in [view, beam, plaques, tracer, plaque, drug, control, period]],
                  run_time=0.40)
        scale = Plot(box=(0.10, 6.18, -1.95, 2.08), xr=(0, 100), yr=(0, 1), color=TEXT)
        track = Line(scale.pt(0, 0.53), scale.pt(100, 0.53), color=BLUE, stroke_width=28)
        self.play(Create(track), run_time=0.75)
        title = label("Amyloid PET · Centiloids", 3.02, 2.40, TEXT, width=5.65)
        self.play(FadeIn(title), run_time=0.43)
        self.at("0 is the average")
        young = label("Plaque-free\nyoung adults\n(average)", 1.07, -0.73, TEXT, width=2.25)
        left_value = label("0", 0.20, 0.83, BLUE, 35)
        left_anchor = Line(scale.pt(0, 0.48), scale.pt(0, 0.58),
                           color=TEXT, stroke_width=10)
        self.play(FadeIn(young), FadeIn(left_value), GrowFromCenter(left_anchor),
                  run_time=0.75)
        self.at("100 is typical")
        typical = label("Typical Alzheimer\ndementia\n(average)", 4.83, -0.73, TEXT, width=3.04)
        right_value = label("100", 6.00, 0.83, BLUE, 35)
        right_anchor = Line(scale.pt(100, 0.48), scale.pt(100, 0.58),
                            color=TEXT, stroke_width=10)
        self.play(FadeIn(typical), FadeIn(right_value), GrowFromCenter(right_anchor),
                  run_time=0.75)
        self.at("amyloid rose", lead=0.78)
        plot, names, duration = trial_chart()
        self.play(*[FadeOut(m) for m in [track, title, young, left_value, typical, right_value,
                                         left_anchor, right_anchor]], run_time=0.32)
        self.play(FadeIn(plot), FadeIn(names), FadeIn(duration), run_time=0.51)
        a = trial_bar(plot, 0.86, DRUG_CHANGE, BLUE)
        b = trial_bar(plot, 2.14, PLACEBO_CHANGE, ORANGE)
        values = trial_values(plot)
        self.at("11 .6 centalloids", lead=0.9)
        self.play(Transform(a.copy().stretch(0, dim=1, about_edge=DOWN), a),
                  FadeIn(values[0]), run_time=0.75)
        self.at("19 .3 with placebo", lead=1.0)
        self.play(Transform(b.copy().stretch(0, dim=1, about_edge=DOWN), b),
                  FadeIn(values[1]), run_time=0.75)
        self.finish()


class S12MathAndReturn(SpokenScene):
    def construct(self):
        self.at("subtract 11")
        anatomy, _, glow_brain = amyloid_world()
        plot, names, duration = trial_chart()
        bars = VGroup(trial_bar(plot, 0.86, DRUG_CHANGE, BLUE),
                      trial_bar(plot, 2.14, PLACEBO_CHANGE, ORANGE))
        values = trial_values(plot)
        self.add(anatomy, glow_brain, plot, names, duration, bars, *values)
        subtraction = label("(19.3 − 11.6)", -1.70, -3.26, TEXT, 34)
        denominator = label("/ 19.3", 0.75, -3.26, TEXT, 34)
        result = label(f"≈ {(PLACEBO_CHANGE - DRUG_CHANGE) / PLACEBO_CHANGE:.2f}",
                       2.61, -3.26, YELLOW, 34)
        self.play(FadeIn(subtraction), bars[0].animate.set_fill(opacity=0.35),
                  run_time=1.18)
        self.at("then divide by")
        self.play(FadeIn(denominator), bars[1].animate.set_fill(opacity=1),
                  run_time=1.17)
        self.at("that equals about")
        self.play(FadeIn(result), bars[0].animate.set_fill(opacity=0.85),
                  bars[1].animate.set_fill(opacity=0.85), run_time=1.02)
        self.at("40 slower buildup")
        equation = VGroup(subtraction, denominator, result)
        percent = (PLACEBO_CHANGE - DRUG_CHANGE) / PLACEBO_CHANGE
        percent_text = bottom(f"≈{percent:.0%} slower amyloid buildup", YELLOW, size=35)
        self.play(swap(equation, percent_text), bars[0].animate.set_fill(opacity=0.49),
                  run_time=1.05)
        self.at("yet a slower rising")
        rule = bottom("Slower amyloid rise ≠ slower decline", GOLD, size=35)
        self.play(swap(percent_text, rule, 0.81),
                  bars[1].animate.set_fill(opacity=0.42), run_time=1.0)
        self.at("decline in the person")
        glow_brain.clear_updaters()
        self.play(FadeOut(plot), FadeOut(names), FadeOut(duration), FadeOut(bars),
                  *[FadeOut(value) for value in values],
                  Transform(glow_brain, glow(CHEST)),
                  run_time=1.42)
        self.at("petmap's chemistry")
        self.play(FadeIn(window()), FadeIn(link(CHEST)), run_time=0.50)
        self.play(FadeIn(cell()), run_time=0.55)
        self.play(swap(rule, bottom("PET maps living chemistry", GOLD), 0.81))
        self.add(flux(ZOOM + p(-2.35, -0.26), ZOOM + p(0.86, -0.22), period=2.2),
                 scope_tag(size=28, color=TEXT))
        self.finish()


class S13End(EndCard):
    LINE = "PET maps living chemistry with radioactive tracers, not clinical benefit."
