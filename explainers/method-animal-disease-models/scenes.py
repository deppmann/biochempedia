"""Animal disease models, synchronized to the supplied Kokoro word timings.

COLOR MAP (shared with the methods series)
  GREY    anatomical outlines and structural connections
  BLUE    the animal model and its circuit
  TEAL    the human comparator
  PURPLE  proteins, gene switches, receptors and synapses
  YELLOW  propagating signals and the isolated feature
  GREEN   functioning output, rescue and a passing test
  RED     loss, symptoms and the limits of the comparison
  ORANGE  experimental inputs
  GOLD    the prediction question and study milestones
"""
from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
MODEL_FILL = "#234658"
HUMAN_FILL = "#24494B"
TISSUE_FILL = "#293449"
FEATURE_FILL = "#303F5B"

TITLE = "Recreating Disease to Test Its Cause"
QUESTION = "Which two late tests separate them?"


def p(x, y):
    return np.array([x, y, 0.0])


def outline(points, color, fill, stroke=3):
    shape = VMobject(stroke_color=color, stroke_width=stroke, fill_color=fill, fill_opacity=1)
    verts = [p(x, y) for x, y in points]
    shape.set_points_smoothly([*verts, verts[0]])
    return shape


def oval(width, height, x, y, color, fill, stroke=3):
    return Ellipse(width=width, height=height, stroke_color=color, stroke_width=stroke,
                   fill_color=fill, fill_opacity=1).move_to(p(x, y))


def rod(a, b, color=GREY, width=5):
    return Line(p(*a), p(*b), color=color, stroke_width=width).set_cap_style(CapStyleType.ROUND)


def path(points, color=GREY, width=5):
    line = VMobject(stroke_color=color, stroke_width=width)
    line.set_points_as_corners([p(*point) for point in points])
    return line.set_cap_style(CapStyleType.ROUND)


def arrow(a, b, color=YELLOW):
    return Arrow(p(*a), p(*b), buff=0, color=color, stroke_width=5, tip_length=0.22)


def movement_arrow(x, y, color, height=1.36):
    stem, head = 0.20, 0.44
    return Polygon(p(x - stem, y), p(x + stem, y),
                   p(x + stem, y + height - 0.42), p(x + head, y + height - 0.42),
                   p(x, y + height), p(x - head, y + height - 0.42),
                   p(x - stem, y + height - 0.42),
                   fill_color=color, fill_opacity=0.89, stroke_width=0)


def label(value, x, y, color=TEXT, size=31):
    return T(value, size, color).move_to(p(x, y))


def badge(value, x, y, color=PURPLE):
    return boxed_label(value, color, size=28, pad=0.18).move_to(p(x, y))


def bead(x, y, color, radius=0.16):
    return Dot(p(x, y), radius=radius, color=color)


def wave(scene, route, color=YELLOW, seconds=2.0, radius=0.15, broken=False):
    """Send a visible signal along a connection while the narration holds the view."""
    signal = Dot(radius=radius, color=color).move_to(route.get_start())

    def travel(mob, dt):
        mob.phase = (mob.phase + dt / seconds) % 1
        mob.move_to(route.point_from_proportion(mob.phase))
        amplitude = np.sin(PI * mob.phase)
        if broken:
            amplitude *= 0.72 + 0.28 * np.cos(3 * TAU * mob.phase)
        mob.set_opacity(0.27 + 0.73 * amplitude)

    signal.phase = 0
    signal.add_updater(travel)
    scene.add(signal)
    return signal


def patient():
    body = outline(
        [(-0.49, 1.10), (-1.08, 0.80), (-1.39, -0.34), (-1.42, -0.83),
         (-1.03, -0.90), (-0.73, -0.02), (-0.72, -0.90), (-0.70, -1.98),
         (-0.19, -2.05), (0, -0.86), (0.19, -2.05), (0.70, -1.98),
         (0.72, -0.90), (0.73, -0.02), (1.03, -0.90), (1.42, -0.83),
         (1.39, -0.34), (1.08, 0.80), (0.49, 1.10)],
        TEAL, HUMAN_FILL)
    return VGroup(body, oval(1.02, 1.06, 0, 1.68, TEAL, HUMAN_FILL))


def mouse():
    tail = CubicBezier(p(1.87, -0.68), p(3.00, -0.91), p(3.13, 0.31), p(2.38, 0.38))
    tail.set_stroke(BLUE, 4)
    body = outline(
        [(-2.39, -0.42), (-1.84, -0.13), (-1.43, 0.47), (-0.63, 1.29),
         (0.45, 1.67), (1.51, 1.23), (2.09, 0.29), (1.96, -0.78),
         (1.62, -1.23), (0.93, -1.22), (1.00, -0.97), (-0.55, -0.99),
         (-1.15, -1.29), (-1.67, -1.24), (-1.52, -0.98), (-2.05, -0.75)],
        BLUE, MODEL_FILL)
    ear = oval(0.85, 0.89, -1.29, 0.56, BLUE, MODEL_FILL)
    eye = bead(-1.82, -0.29, BLUE, 0.072)
    return VGroup(tail, body, ear, eye)


def comparator():
    """The bridge always leads from the same patient to the same model."""
    panels = TwoPanel("Human", "Animal", colors=(TEAL, BLUE), top=2.94,
                      bottom=-2.64, gap=0.55, width=12.65, size=33)
    human = patient().scale(0.93).move_to(p(-3.30, -0.18))
    animal = mouse().move_to(p(3.30, -0.46))
    bridge = arrow((-3.25, -3.02), (3.20, -3.02), BLUE)
    reticle = Circle(radius=0.84, color=YELLOW, stroke_width=5).move_to(p(3.55, -0.22))
    return panels, human, animal, bridge, reticle


def workbench(center=1.0, width=9.5):
    """A single close-up field for the test inside the animal."""
    return oval(width, 5.38, center, 0.00, BLUE, MODEL_FILL, 3)


def mouse_route():
    return path([(2.29, -0.51), (2.87, 0.19), (3.55, -0.22), (4.18, 0.48), (4.81, -0.23)], BLUE, 5)


def junction(x=1.18, y=0.0, scale=1.0, receptors=6):
    """A nerve terminal above a receiving muscle strip."""
    terminal = outline(
        [(-1.49, 0.52), (-0.69, 0.99), (-0.24, 1.75), (-0.23, 2.15),
         (0.23, 2.15), (0.24, 1.75), (0.69, 0.99), (1.49, 0.52),
         (1.41, 0.18), (0.0, 0.13), (-1.41, 0.18)], BLUE, FEATURE_FILL)
    muscle = RoundedRectangle(width=4.08, height=1.0, corner_radius=0.3,
                              stroke_color=GREY, stroke_width=3, fill_color=TISSUE_FILL,
                              fill_opacity=1).move_to(p(0, -1.02))
    slots = VGroup(*[
        RoundedRectangle(width=0.21, height=0.33, corner_radius=0.075, stroke_width=0,
                         fill_color=PURPLE, fill_opacity=1).move_to(p(pos, -0.46))
        for pos in np.linspace(-1.21, 1.21, receptors)
    ])
    return tuple(m.scale(scale, about_point=ORIGIN).shift(p(x, y)) for m in (terminal, muscle, slots))


def brain_nodes(x, y, scale=1.0, healthy=True):
    """A schematic of paths through a circuit, without a recorded trace."""
    coords = [(-2.12, 0.0), (-1.13, 0.60), (0.0, 0.21), (1.08, 0.53), (2.12, 0)]
    positions = [(x + scale * u, y + scale * v) for u, v in coords]
    route = path(positions, GREY, 6)
    lower = path([positions[0], (x - scale, y - 0.63 * scale),
                  (x + scale, y - 0.63 * scale), positions[-1]], GREY, 3)
    nodes = VGroup(*[bead(u, v, BLUE, 0.23 * scale) for u, v in positions[:-1]],
                   bead(*positions[-1], GREEN if healthy else RED, 0.28 * scale))
    shell = oval(5.48 * scale, 2.63 * scale, x, y + 0.02, BLUE, FEATURE_FILL)
    return VGroup(shell, lower, route, nodes), route, nodes[-1]


def sensory_field(x=0.40, y=0.0, scale=1.0):
    """One inner-ear location with a schematic count of ribbon synapses."""
    tissue = outline(
        [(-2.35, 0.30), (-1.60, 1.84), (-0.10, 2.13), (1.68, 1.61),
         (2.33, 0.78), (1.98, -0.51), (0.90, -1.20), (-1.21, -1.06), (-2.13, -0.64)],
        BLUE, FEATURE_FILL).scale(scale, about_point=ORIGIN).shift(p(x, y))
    ribbons = VGroup(*[bead(x + scale * pos, y - 1.28 * scale, PURPLE, 0.14 * scale)
                       for pos in np.linspace(-1.93, 1.93, 10)])
    return tissue, ribbons


def stimulus_waves(x, y, color=ORANGE):
    return VGroup(*[
        Arc(radius=r, start_angle=-PI / 3, angle=2 * PI / 3,
            arc_center=p(x, y), color=color, stroke_width=4)
        for r in (0.36, 0.66, 0.96)
    ])


def drop(x, y):
    return outline([(0, 0.43), (-0.29, -0.08), (-0.19, -0.32),
                    (0.18, -0.32), (0.29, -0.08)], ORANGE, ORANGE, 2).move_to(p(x, y))


def antibody(x, y):
    return VGroup(rod((x, y - 0.29), (x, y + 0.03), ORANGE, 7),
                  rod((x, y + 0.03), (x - 0.22, y + 0.27), ORANGE, 7),
                  rod((x, y + 0.03), (x + 0.22, y + 0.27), ORANGE, 7))


def feature_panels(scene):
    panels, human, animal, bridge, ring = comparator()
    scene.add(panels, human, animal, bridge, scope_tag(size=28))
    return panels, human, animal, bridge, ring


class S01Hook(SpokenScene):
    def construct(self):
        panels, human, animal, bridge, ring = comparator()
        knot = path([(-4.10, -0.23), (-2.80, 0.43), (-3.77, 0.55),
                     (-3.06, -0.70), (-3.87, -0.54), (-3.52, 0.58), (-2.69, -0.05)], GREY, 4)
        symptom = Circle(radius=0.23, color=RED, stroke_width=5).move_to(knot.get_end())
        barrier = RoundedRectangle(width=0.18, height=3.57, corner_radius=0.08,
                                   stroke_width=0, fill_color=RED, fill_opacity=0.6).move_to(p(-0.65, -0.23))
        stop = label("Cannot test here", -3.30, -3.48, RED, 29)
        model_route = mouse_route()
        self.add(panels.left_frame, panels.left_head, human, knot, symptom, scope_tag(size=28))
        pulse(symptom, base=6, amp=3, speed=3)
        symptom_signal = wave(self, knot, RED, seconds=2.25, radius=0.35, broken=True)
        self.at("without experimenting")
        self.play(FadeIn(barrier), run_time=0.55)
        self.at("on patients")
        self.play(FadeIn(stop), run_time=0.5)
        self.at("watching patients", lead=0.72)
        self.play(FadeIn(panels.right_frame), FadeIn(animal), GrowArrow(bridge), run_time=0.90)
        self.play(FadeIn(panels.right_head), Create(model_route), run_time=0.68)
        self.at("which broken part")
        self.play(knot.animate.set_stroke(width=7), run_time=0.9)
        self.at("to test cause directly", lead=0.6)
        self.play(FadeOut(stop), FadeOut(barrier), run_time=0.43)
        bridge_signal = wave(self, bridge, BLUE, seconds=1.95, radius=0.28)
        self.at("one disease feature")
        self.play(Create(ring), FadeOut(knot), FadeOut(symptom), FadeOut(symptom_signal),
                  FadeOut(bridge_signal), run_time=0.72)
        wave(self, model_route, seconds=1.8, radius=0.25)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Animal models of disease"
    TITLE = TITLE

    def construct(self):
        # The hook hands off the same bridge and animal to this two-second card.
        panels, human, animal, bridge, ring = comparator()
        title = fit_text(self.TITLE, max_w=12.0, size=46, min_size=40, font=TITLE_FONT).move_to(p(0, 3.40))
        route = mouse_route()
        self.add(panels.left_frame, panels.right_frame, human, animal, bridge, ring, route, scope_tag(size=28))
        wave(self, route, seconds=1.9, radius=0.22)
        pulse(ring, base=5, amp=2.4)
        self.play(FadeIn(title), run_time=0.38)
        self.wait(1.08)
        self.play(FadeOut(title), FadeOut(panels.left_frame), FadeOut(human), FadeOut(bridge), run_time=0.46)


class S03Build(SpokenScene):
    def construct(self):
        panels, _, animal, _, ring = comparator()
        field = workbench(1.46, 8.70)
        terminal, muscle, slots = junction(1.46)
        inputs = [
            badge(word, -4.78, y, ORANGE) for word, y in
            zip(("Genes", "Toxins", "Injury", "Antibodies"), (1.69, 0.56, -0.57, -1.70))
        ]
        icons = (
            RoundedRectangle(width=0.41, height=0.27, corner_radius=0.07, stroke_width=3,
                             stroke_color=ORANGE).move_to(p(-6.17, 1.69)),
            drop(-6.17, 0.56).scale(0.54),
            stimulus_waves(-6.17, -0.57).scale(0.36).move_to(p(-6.17, -0.57)),
            antibody(-6.17, -1.70).scale(0.76),
        )
        route_in_mouse = mouse_route()
        self.add(panels.right_frame, animal, ring, route_in_mouse, scope_tag(size=28))
        self.at("they build that")
        self.play(FadeOut(panels.right_frame), FadeOut(animal), FadeOut(route_in_mouse),
                  ReplacementTransform(ring, field), run_time=0.85)
        tracks = [arrow((-3.15, y), (-1.25, 0.12), ORANGE) for y in (1.69, 0.56, -0.57, -1.70)]
        for phrase, source, icon, track in zip(("genes", "toxins", "injury", "patient antibodies"), inputs, icons, tracks):
            self.at(phrase)
            self.play(FadeIn(source), FadeIn(icon), GrowArrow(track), run_time=0.50)
        self.play(LaggedStart(*(FadeOut(track) for track in tracks), lag_ratio=0.17), run_time=1.0)
        self.at("deleting the muscle protein", lead=0.65)
        tag = badge("MuSK", -3.60, 0.52)
        self.play(*(FadeOut(source) for source in (*inputs, *icons)),
                  FadeIn(terminal), FadeIn(muscle), FadeIn(slots), run_time=0.65)
        self.play(FadeIn(tag), run_time=0.38)
        self.at("stops nerve")
        self.play(FadeOut(tag, shift=UP * 0.30), terminal.animate.shift(UP * 0.34).set_opacity(0.46),
                  slots.animate.set_opacity(0.20), run_time=1.20)
        off = label("Junction fails to form", 0.48, -3.03, RED)
        self.play(FadeIn(off), run_time=0.42)
        self.at("in newborn mice")
        self.play(muscle.animate.set_stroke(color=RED, width=4), run_time=0.8)
        toxins = drop(-3.5, 0.55)
        brain, route, output = brain_nodes(1.46, -0.15)
        self.at("toxins kill", lead=0.9)
        self.play(FadeOut(terminal), FadeOut(muscle), FadeOut(slots), FadeOut(off),
                  FadeIn(brain), FadeIn(toxins), run_time=0.63)
        self.play(toxins.animate.move_to(p(0.23, 0.6)), brain[-1][1:3].animate.set_opacity(0.21), run_time=1.35)
        ear, ribbons = sensory_field(1.46, -0.18)
        waves = stimulus_waves(-3.05, 0.0)
        self.at("loud noise", lead=0.54)
        self.play(FadeOut(brain), FadeOut(toxins), FadeIn(ear), FadeIn(ribbons), run_time=0.54)
        self.play(Create(waves), run_time=0.40)
        self.play(waves.animate.shift(RIGHT * 1.35), ribbons[1::2].animate.set_opacity(0.21), run_time=1.05)
        self.finish()


def junction_chain():
    coords = [(-1.15, 0.31), (0.22, -0.43), (1.59, 0.42), (2.96, -0.35), (4.37, 0.34)]
    links = VGroup(*[oval(0.96, 0.78, x, y, PURPLE, TISSUE_FILL) for x, y in coords[:-1]])
    segments = VGroup(*[rod(a, b, PURPLE, 7) for a, b in zip(coords, coords[1:])])
    output = oval(1.20, 1.07, *coords[-1], GREEN, GREEN, 5).set_fill(opacity=0.73)
    return VGroup(segments, links, output), links, segments, output, path(coords)


class S04Intervene(SpokenScene):
    def construct(self):
        field = workbench(1.46, 8.70)
        ear, ribbons = sensory_field(1.46, -0.18)
        ribbons[1::2].set_opacity(0.21)
        self.add(field, ear, ribbons, scope_tag(size=28))
        terminal, muscle, slots = junction(1.46, -0.05, 0.92)
        anatomy = VGroup(terminal, muscle, slots)
        self.at("inside a living animal")
        self.play(FadeOut(ear), FadeOut(ribbons), FadeIn(anatomy), run_time=0.9)
        self.at("researchers can intervene")
        chain, links, segments, out, route = junction_chain()
        lever = badge("Intervention", -4.55, 0.02, ORANGE)
        self.play(FadeOut(anatomy), FadeIn(chain), run_time=0.8)
        self.play(FadeIn(lever), run_time=0.45)
        current = wave(self, route, seconds=1.46, radius=0.34)
        self.at("removing one link")
        self.play(links[1].animate.shift(DOWN * 0.88).set_opacity(0.35),
                  segments[:2].animate.set_opacity(0.14),
                  out.animate.set_fill(RED, opacity=0.19).set_stroke(RED, width=5),
                  FadeOut(current), run_time=1.15)
        self.at("reveals each protein's job")
        self.play(links[1].animate.shift(UP * 0.88).set_opacity(1),
                  segments[:2].animate.set_opacity(1),
                  out.animate.set_fill(GREEN, opacity=0.73).set_stroke(GREEN), run_time=0.6)
        self.play(links[2].animate.shift(UP * 0.86).set_opacity(0.35),
                  segments[1:3].animate.set_opacity(0.14),
                  out.animate.set_fill(RED, opacity=0.19).set_stroke(RED, width=3), run_time=0.9)
        panels, human, animal, bridge, ring = comparator()
        self.at("an animal model recreates")
        self.play(FadeOut(chain), FadeOut(lever), ReplacementTransform(field, ring),
                  FadeIn(animal), FadeIn(panels.right_frame), run_time=1.0)
        self.play(FadeIn(panels.right_head), run_time=0.5)
        self.at("one disease feature")
        pulse(ring, base=5, amp=3)
        self.play(FadeIn(human), FadeIn(panels.left_frame), GrowArrow(bridge), run_time=0.9)
        self.at("a whole human")
        self.play(FadeIn(panels.left_head), run_time=0.5)
        wave(self, bridge, BLUE, radius=0.16)
        self.finish()


def age_rail():
    rail = arrow((-4.86, -2.19), (4.96, -2.19), GREY)
    landmarks = VGroup(bead(-4.22, -2.19, BLUE, 0.14), bead(4.18, -2.19, RED, 0.16))
    birth = label("Birth", -4.22, -2.69)
    adult = label("Young adulthood", 4.18, -2.69)
    return rail, landmarks, birth, adult


def hypotheses():
    early = badge("Built wrong early", -3.25, 1.93, GOLD)
    late = badge("Built fine, cannot run", 3.25, 1.93, GOLD)
    forks = VGroup(path([(-1.04, 0.97), (-2.04, 1.28), (-3.25, 1.42)], GOLD, 4),
                   path([(1.04, 0.97), (2.04, 1.28), (3.25, 1.42)], GOLD, 4))
    return early, late, forks


def predict_world():
    field = oval(11.98, 5.38, 0, 0, BLUE, MODEL_FILL, stroke=0)
    circuit, route, output = brain_nodes(0, 0.19, 1.07, healthy=False)
    rail, landmarks, birth, adult = age_rail()
    gene = badge("Mecp2", 0, -1.66)
    switch = badge("OFF", 4.03, -1.10, RED)
    early, late, forks = hypotheses()
    q = question_card(QUESTION, y=3.26, size=36).move_to(p(0, 3.23))
    return field, circuit, route, output, rail, landmarks, birth, adult, gene, switch, early, late, forks, q


class S05Predict(SpokenScene):
    def construct(self):
        panels, human, animal, bridge, ring = comparator()
        field, circuit, route, output, rail, landmarks, birth, adult, gene, switch, early, late, forks, q = predict_world()
        schem = scope_tag(size=28)
        self.add(panels, human, animal, bridge, ring, schem)
        output.set_color(GREY)
        self.at("now picture a mouse")
        self.play(FadeOut(panels), FadeOut(human), FadeOut(bridge), FadeOut(animal),
                  ReplacementTransform(ring, field), run_time=1.0)
        self.play(FadeIn(circuit), GrowArrow(rail), FadeIn(landmarks[0]), run_time=1.1)
        self.play(FadeIn(birth), run_time=0.44)
        self.at("its gene is")
        self.play(FadeIn(gene), run_time=0.48)
        self.play(FadeIn(switch), run_time=0.52)
        age_path = rod((-4.22, -2.19), (0.28, -2.19), BLUE, 16)
        age = bead(-4.22, -2.19, BLUE, 0.22)
        self.add(age)
        rett = label("Rett syndrome", 0, 3.13, TEAL)
        self.at("the mouse version", lead=0.85)
        self.play(Create(age_path), age.animate.shift(RIGHT * 4.5), run_time=1.96, rate_func=linear)
        self.at("mutated in rett")
        self.play(FadeIn(rett, run_time=0.44), age_path.animate.put_start_and_end_on(p(-4.22, -2.19), p(4.18, -2.19)),
                  age.animate.move_to(landmarks[1]), run_time=1.52, rate_func=linear)
        self.at("by young adulthood")
        self.play(FadeOut(rett), FadeOut(age), FadeOut(age_path), FadeIn(landmarks[1]), FadeIn(adult), run_time=0.58)
        self.at("it has symptoms")
        self.play(output.animate.set_color(RED), run_time=0.47)
        signal = wave(self, route, RED, seconds=1.95, radius=0.35, broken=True)
        self.at("two histories fit")
        self.play(Create(forks), run_time=0.76)
        self.at("either the circuit")
        self.play(FadeIn(early), run_time=0.65)
        self.at("it simply cannot run")
        self.play(FadeIn(late), run_time=0.65)
        self.at("switching that gene")
        self.play(Indicate(switch, color=RED, scale_factor=1.15), run_time=0.85)
        self.at("which two tests")
        self.play(FadeIn(q), FadeOut(signal), run_time=0.53)
        # The symptom alert completes a pulse as the picture settles into the still pause.
        halo = Circle(radius=1.28, stroke_color=RED, stroke_width=5, fill_color=RED,
                      fill_opacity=0.58).move_to(output)
        self.play(FadeIn(halo, scale=0.35), run_time=0.66)
        self.play(FadeOut(halo, scale=1.12), run_time=1.09, rate_func=linear)
        self.finish()


class S06PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        field, circuit, _, _, rail, landmarks, birth, adult, gene, switch, early, late, forks, q = predict_world()
        self.add(field, circuit, rail, landmarks, birth, adult, gene, switch, forks, early, late, q, scope_tag(size=28))
        self.wait(float(os.environ.get("KX_DURATION", "4.5")))


class S07Answer(SpokenScene):
    def construct(self):
        field, circuit, route, output, rail, landmarks, birth, adult, gene, switch, early, late, forks, q = predict_world()
        self.add(field, circuit, rail, landmarks, birth, adult, gene, switch, forks, early, late, q, scope_tag(size=28))
        self.at("first put the gene")
        self.play(FadeOut(early), FadeOut(late), FadeOut(forks), FadeOut(q),
                  field.animate.stretch(0.87, 0), run_time=0.51, rate_func=linear)
        first = label("Restore after symptoms", 0, 2.98, GOLD)
        self.play(FadeIn(first), run_time=0.38)
        on = badge("ON", 4.03, -1.10, GREEN)
        signal = wave(self, route, RED, seconds=2.05, radius=0.20, broken=True)
        self.at("after symptoms begin")
        self.play(swap(switch, on, run_time=0.66), run_time=0.66)
        self.at("and watch")
        self.play(output.animate.set_color(GREEN), FadeOut(signal), run_time=0.74)
        signal = wave(self, route, GREEN, seconds=1.55, radius=0.19)

        self.at("second take it")
        panels = TwoPanel("Restore after symptoms", "Remove after development",
                          colors=(BLUE, BLUE), top=2.72, bottom=-2.63, size=30)
        rescue, rescue_route, _ = brain_nodes(-3.32, -0.10, 0.96)
        loss, loss_route, loss_output = brain_nodes(3.32, -0.10, 0.96)
        rescue_on = badge("Mecp2 ON", -3.32, -1.93, GREEN)
        loss_on = badge("Mecp2 ON", 3.32, -1.93, GREEN)
        loss_off = badge("Mecp2 OFF", 3.32, -1.93, RED)
        self.play(FadeOut(field), FadeOut(rail), FadeOut(landmarks), FadeOut(birth), FadeOut(adult),
                  FadeOut(gene), FadeOut(on), FadeOut(first), FadeOut(signal),
                  ReplacementTransform(circuit, rescue), run_time=0.78)
        self.play(FadeIn(panels.left_frame), FadeIn(panels.left_head), FadeIn(rescue_on), FadeIn(panels.right_frame),
                  FadeIn(loss), run_time=0.62)
        self.play(FadeIn(panels.right_head), FadeIn(loss_on), run_time=0.43)
        wave(self, rescue_route, GREEN, seconds=1.80, radius=0.18)
        healthy = wave(self, loss_route, GREEN, seconds=1.8, radius=0.18)
        self.at("after its circuit")
        self.play(swap(loss_on, loss_off, run_time=0.78), run_time=0.78)
        self.play(FadeOut(healthy), loss_output.animate.set_color(RED), run_time=0.55)
        wave(self, loss_route, RED, seconds=2.0, radius=0.20, broken=True)
        self.at("symptoms fade on return")
        self.play(panels.left_frame.animate.set_stroke(GREEN, width=5), run_time=0.66)
        self.at("appear on late loss")
        self.play(panels.right_frame.animate.set_stroke(RED, width=5), run_time=0.65)
        self.at("the protein runs")
        self.play(FadeIn(label("Built fine, cannot run", 0, 3.24, GOLD, 34)), run_time=0.55)
        self.finish()


def protein_outputs():
    protein = RoundedRectangle(width=2.65, height=1.39, corner_radius=0.28,
                               stroke_color=PURPLE, stroke_width=4, fill_color=TISSUE_FILL,
                               fill_opacity=1).move_to(p(-0.88, 0.0))
    outputs = VGroup(*[bead(3.61, y, GREEN, 0.35) for y in (1.40, 0.0, -1.40)])
    routes = VGroup(*[rod((0.46, 0.0), (3.25, y), GREY, 5) for y in (1.4, 0.0, -1.4)])
    return protein, outputs, routes


class S08Controls(SpokenScene):
    def construct(self):
        field = workbench(0.36, 10.8)
        protein, outputs, routes = protein_outputs()
        protein_label = label("Protein", -0.88, 0, PURPLE)
        self.add(field, routes, protein, outputs, scope_tag(size=28))
        self.at("clean tests need")
        self.play(FadeIn(protein_label), run_time=0.5)
        signals = [wave(self, route, GREEN, seconds=1.4 + i * 0.34, radius=0.28)
                   for i, route in enumerate(routes)]
        knockout = label("Knockout", 0, 3.12, PURPLE, 35)
        self.at("knockout deletes")
        self.play(FadeIn(knockout), run_time=0.44)
        self.play(FadeOut(protein, shift=UP * 0.55), FadeOut(protein_label, shift=UP * 0.55),
                  *(FadeOut(s) for s in signals), run_time=0.82)
        self.at("removing every job")
        self.play(LaggedStart(*(m.animate.set_color(RED).set_opacity(0.34) for m in outputs),
                              lag_ratio=0.27), run_time=1.25)
        knockin = label("Knock-in", 0, 3.12, PURPLE, 35)
        self.at("edits one site", lead=0.95)
        self.play(swap(knockout, knockin, run_time=0.62), run_time=0.62)
        self.play(FadeIn(protein), FadeIn(protein_label), outputs.animate.set_color(GREEN).set_opacity(1),
                  run_time=0.58)
        edit = bead(-1.86, 0.24, YELLOW, 0.18)
        self.play(FadeIn(edit, scale=0.5), run_time=0.44)
        self.at("to test one role")
        self.play(outputs[1].animate.set_color(YELLOW), run_time=0.65)
        signal = wave(self, routes[1], seconds=1.68, radius=0.33)
        ear, ribbons = sensory_field(0.92, 0.04, 1.0)
        self.at("measurements can mislead")
        self.play(FadeOut(protein), FadeOut(protein_label), FadeOut(edit), FadeOut(outputs),
                  FadeOut(routes), FadeOut(signal), FadeOut(knockin), run_time=0.4)
        self.play(FadeIn(ear), FadeIn(ribbons), run_time=0.48)
        waves = stimulus_waves(-3.90, 0.28).scale(1.5).set_stroke(width=11)
        self.at("after loud noise")
        self.play(Create(waves), run_time=0.38)
        self.play(waves.animate.shift(RIGHT * 1.65), ear.animate.set_fill("#3E506D"), run_time=0.63)
        self.play(FadeOut(waves), run_time=0.27)
        hearing = ValueTracker(0.18)
        g = dial(hearing, p(-3.30, 0.1), radius=1.25, label="Hearing test", color=GREEN,
                 fmt="Pass", scale=1, size=32)
        self.at("pass its hearing test", lead=0.55)
        passing = g[3]
        g.remove(passing)
        self.play(FadeIn(g), run_time=0.53)
        self.play(hearing.animate.set_value(0.88), run_time=1.09)
        self.play(FadeIn(passing), run_time=0.36)
        self.at("lose about half")
        self.play(LaggedStart(*(m.animate.set_opacity(0.16) for m in ribbons[1::2]), lag_ratio=0.22),
                  ear.animate.set_fill(FEATURE_FILL), run_time=1.75)
        ribbon_label = label("Ribbon synapses", 0.90, -1.94, PURPLE, 28)
        self.at("at one")
        self.play(FadeIn(ribbon_label), run_time=0.52)
        self.finish()


def lungs(x, y, color):
    left = outline([(-0.19, 0.87), (-0.70, 1.35), (-1.20, 0.57), (-1.26, -0.89),
                    (-0.60, -1.11), (-0.19, -0.64)], color, TISSUE_FILL).shift(p(x, y))
    right = left.copy().flip(UP, about_point=p(x, y))
    airway = path([(x, y + 1.45), (x, y + 0.55), (x + 0.59, y + 0.08)], color, 6)
    branch = rod((x, y + 0.55), (x - 0.59, y + 0.08), color, 6)
    tumour = oval(0.97, 0.90, x + 0.72, y - 0.49, RED, "#BA5051", 4)
    anatomy = VGroup(left, right, airway, branch)
    for obj in (anatomy, tumour):
        obj.scale(1.26, about_point=p(x, y))
    return anatomy, tumour


class S09Limits(SpokenScene):
    def construct(self):
        panels, human, animal, bridge, ring = feature_panels(self)
        pulse(ring, base=5, amp=3)
        signal = wave(self, bridge, BLUE, radius=0.18)
        self.add(ring)
        warning = badge("Check in people", 0, -3.15, RED)
        self.at("face species limits")
        self.play(FadeOut(bridge), FadeOut(signal), run_time=0.31)
        self.play(FadeIn(warning), run_time=0.41)
        self.at("one mouse strain", lead=0.52)
        detail = [label(word, 1.55, y, color=TEXT, size=28) for word, y in
                  zip(("Strain", "Sex", "Age", "Exposure"), (1.22, 0.42, -0.38, -1.18))]
        self.play(animal.animate.scale(0.63).move_to(p(4.20, -0.44)), FadeOut(ring), run_time=0.55)
        for phrase, item in zip(("strain", "sex", "age", "exposure"), detail):
            self.at(phrase, lead=0.08)
            self.play(FadeIn(item), run_time=0.33)
        self.at("holds in people")
        self.play(panels.left_frame.animate.set_stroke(RED, width=5), run_time=0.7)
        rl, rt = lungs(3.30, -0.27, BLUE)
        treatment = label("Cetuximab", 3.30, -2.18, ORANGE)
        self.at("the antibody", lead=0.8)
        self.play(FadeOut(animal), *(FadeOut(t) for t in detail), run_time=0.35)
        self.play(FadeIn(rl), FadeIn(rt), run_time=0.47)
        self.play(FadeIn(treatment), run_time=0.43)
        self.at("shrank mouse lung")
        self.play(rt.animate.scale(0.41), run_time=1.72)
        pulse(rt, base=4, amp=2)
        self.at("driven by a mutant")
        receptor = bead(2.49, 0.82, PURPLE, 0.32)
        self.play(GrowFromCenter(receptor), rl.animate.set_stroke(BLUE, width=4), run_time=0.60)
        self.play(FadeOut(receptor), run_time=0.58)
        ll, lt = lungs(-3.30, -0.27, TEAL)
        combo = label("Cetuximab + afatinib", -3.30, -2.18, ORANGE, 29)
        self.at("yet in patients")
        self.play(FadeOut(human), FadeIn(ll), FadeIn(lt), run_time=0.79)
        self.at("adding it to")
        medicine = VGroup(bead(-4.47, 1.01, ORANGE, 0.34), bead(-3.85, 1.01, ORANGE, 0.28))
        self.play(FadeIn(combo), FadeIn(medicine), run_time=0.59)
        self.play(medicine.animate.shift(RIGHT * 1.28 + DOWN * 0.95), run_time=1.04)
        self.play(FadeOut(medicine), run_time=0.55)
        pulse(lt, base=5, amp=3)
        self.at("did not help")
        self.play(swap(combo, label("No added benefit", -3.30, -2.18, RED), run_time=0.75), run_time=0.75)
        self.finish()


class S10Unlocked1(SpokenScene):
    def construct(self):
        panels, human, animal, bridge, ring = comparator()
        warning = badge("Check in people", 0, -3.15, RED)
        self.add(panels, human, animal, warning, scope_tag(size=28))
        self.at("within those limits")
        self.play(FadeOut(warning), run_time=0.32)
        self.play(GrowArrow(bridge), run_time=0.60)
        wave_dot = wave(self, bridge, BLUE, seconds=2.2, radius=0.32)
        self.at("unlocked major causes")
        self.play(Create(ring), run_time=1.0)
        pulse(ring, base=5, amp=3)
        milestone = label("1975 · Toyka & colleagues", 0, 3.33, GOLD, 33)
        self.at("in 1975")
        self.play(FadeIn(milestone), run_time=0.63)
        transfer = VGroup(*[antibody(x, -1.11) for x in (-4.34, -3.48, -2.62)])
        antibody_label = label("Patient antibodies", -3.30, -3.08, ORANGE, 30)
        self.at("transferred antibodies", lead=0.67)
        self.play(FadeIn(transfer), FadeOut(wave_dot), FadeOut(bridge), run_time=0.55)
        self.play(FadeIn(antibody_label), run_time=0.48)
        self.at("from patients")
        self.play(FadeOut(antibody_label), run_time=0.28)
        self.play(transfer.animate.shift(DOWN * 1.80), GrowArrow(bridge), run_time=0.61)
        self.play(transfer.animate.shift(RIGHT * 6.67), run_time=2.47, rate_func=linear)
        self.at("into mice")
        self.play(transfer.animate.shift(UP * 1.69), run_time=0.65)
        field = workbench(0.42, 10.45)
        terminal, muscle, slots = junction(0.65, -0.18, 1.04)
        self.play(FadeOut(panels), FadeOut(human), FadeOut(bridge), FadeOut(animal), FadeOut(transfer),
                  ReplacementTransform(ring, field), FadeIn(terminal), FadeIn(muscle), FadeIn(slots), run_time=0.80)
        signal_route = rod((0.65, 1.74), (0.65, -0.61))
        current = wave(self, signal_route, seconds=1.6, radius=0.32)
        receptor_label = label("Muscle junction receptors", 0.30, -3.09, PURPLE, 30)
        self.at("lost muscle junction")
        self.play(FadeIn(receptor_label), run_time=0.43)
        self.play(LaggedStart(*(FadeOut(slot) for slot in slots[1::2]), lag_ratio=0.2), run_time=0.95)
        self.at("smaller unit signals")
        pending = oval(2.07, 0.63, 0.65, -1.18, YELLOW, YELLOW).set_fill(opacity=0.75)
        self.play(GrowFromCenter(pending), FadeOut(current), run_time=0.52)
        self.play(pending.animate.scale(0.44), run_time=0.69)
        miniatures = label("Miniatures", 0.30, -3.09, YELLOW, 31)
        self.at("called miniatures")
        self.play(swap(receptor_label, miniatures, run_time=0.58), run_time=0.58)
        pulse(pending, base=5, amp=3)
        self.finish()


def primate():
    # Front view, so the movement on the other side is visible against the same body.
    torso = outline(
        [(-1.03, 0.77), (-1.87, 0.41), (-2.25, -0.72), (-2.01, -1.55),
         (-1.71, -1.38), (-1.63, -0.46), (-1.02, -0.34), (-1.13, -1.82),
         (-0.81, -2.08), (-0.36, -1.84), (0, -1.27), (0.36, -1.84),
         (0.81, -2.08), (1.13, -1.82), (1.02, -0.34), (1.63, -0.46),
         (1.71, -1.38), (2.01, -1.55), (2.25, -0.72), (1.87, 0.41), (1.03, 0.77)],
        BLUE, "#365A72")
    head = oval(2.26, 1.66, 0, 1.30, BLUE, "#365A72")
    ears = VGroup(oval(0.48, 0.74, -1.16, 1.22, BLUE, "#365A72"),
                  oval(0.48, 0.74, 1.16, 1.22, BLUE, "#365A72"))
    return VGroup(torso, ears, head).shift(p(0.50, 0.05))


class S11Unlocked2(SpokenScene):
    def construct(self):
        field = workbench(0.42, 10.45)
        monkey = primate()
        self.add(field, monkey, scope_tag(size=28))
        milestone = label("1990 · Bergman, Wichmann & DeLong", 0, 3.24, GOLD, 32)
        self.at("in 1990")
        self.play(FadeIn(milestone), run_time=0.57)
        brain = oval(1.83, 0.88, 0.50, 1.52, BLUE, FEATURE_FILL)
        neurons = VGroup(*[bead(x, y, BLUE, 0.15) for x, y in
                           [(-0.08, 1.59), (0.13, 1.73), (0.34, 1.54), (0.60, 1.73), (0.90, 1.66), (1.06, 1.47)]])
        route = path([(-0.23, 1.41), (0.0, 0.21), (1.02, -0.19),
                      (1.97, -0.65), (2.62, -1.27)], GREY, 4)
        self.at("tested a brain")
        self.play(FadeIn(brain), FadeIn(neurons), Create(route), run_time=0.95)
        transfer = wave(self, route, seconds=2.4, radius=0.33)
        toxin = drop(-3.36, 0.82)
        toxin_label = label("MPTP", -3.36, 0.04, ORANGE)
        self.at("they used the toxin", lead=0.45)
        self.play(FadeIn(toxin), run_time=0.44)
        self.play(FadeIn(toxin_label), run_time=0.39)
        self.at("kill dopamine neurons")
        self.play(toxin.animate.move_to(p(-1.35, 1.45)),
                  neurons.animate.set_opacity(0.23), brain.animate.set_fill(TISSUE_FILL).set_stroke(RED),
                  FadeOut(transfer), run_time=1.45)
        self.at("model parkinson's disease")
        arrows = VGroup(movement_arrow(3.32, -1.08, RED),
                        movement_arrow(4.30, -0.78, RED, height=1.19))
        arm = path([(1.48, 0.49), (2.18, -0.17), (2.38, -1.04)], RED, 27)
        self.play(FadeOut(toxin), FadeOut(toxin_label), FadeIn(arrows), run_time=0.82)
        self.play(Create(arm), run_time=0.48)
        bob(arrows, amp=0.55, speed=2.15)
        lesion = Circle(radius=0.31, color=RED, stroke_width=6).move_to(p(-0.07, 1.39))
        stn = label("STN", -2.97, 1.43, PURPLE, 34)
        pointer = rod((-2.30, 1.43), (-0.42, 1.40), PURPLE, 3)
        self.at("a lesion in")
        self.play(Create(lesion), Create(pointer), brain.animate.set_fill("#533844"), run_time=0.62)
        self.play(FadeIn(stn), run_time=0.46)
        self.at("eased opposite")
        arrows.clear_updaters()
        self.play(arrows.animate.stretch(1.34, 1).set_color(GREEN), arm.animate.set_color(GREEN),
                  brain.animate.set_fill(FEATURE_FILL), run_time=1.07)
        bob(arrows, amp=0.62, speed=2.2)
        wave(self, route, GREEN, seconds=2.1, radius=0.33)
        self.at("that result made")
        surgical = label("Surgical target", -3.00, 0.64, GOLD, 30)
        self.play(FadeIn(surgical), lesion.animate.set_stroke(GOLD, width=6), run_time=0.77)
        self.finish()


class S12Unlocked3(SpokenScene):
    def construct(self):
        field = workbench(0.42, 10.45)
        tissue, _ = sensory_field(0.28, -0.10, 1.12)
        self.add(field, tissue, scope_tag(size=28))
        milestone = label("2017 · Michalski & colleagues", 0, 3.27, GOLD, 32)
        self.at("in 2017")
        self.play(FadeIn(milestone), run_time=0.6)
        protein = RoundedRectangle(width=2.18, height=0.72, corner_radius=0.26,
                                   fill_color=PURPLE, fill_opacity=0.34, stroke_color=PURPLE,
                                   stroke_width=4).move_to(p(0.28, -0.45))
        name = label("Otoferlin", 0.28, -1.97, PURPLE, 32)
        self.at("used a knock")
        self.play(FadeIn(protein), run_time=0.6)
        route = path([(0.28, 1.77), (0.28, 0.81), (0.28, 0.04)], BLUE, 5)
        self.play(Create(route), run_time=0.54)
        calcium = wave(self, route, BLUE, seconds=1.60, radius=0.32)
        self.at("inner ear protein")
        self.play(FadeIn(name), run_time=0.60)
        release = rod((1.43, -0.47), (3.85, -0.47), GREY, 4)
        self.play(Create(release), run_time=0.52)
        pulses = [wave(self, release, YELLOW, seconds=1.28 + i * 0.52, radius=0.28)
                  for i in range(3)]
        edit = bead(0.84, -0.45, YELLOW, 0.21)
        edit_label = label("Calcium-binding domain", -2.78, -3.08, YELLOW, 29)
        self.at("changing one calcium")
        self.play(FadeIn(edit, scale=0.5), run_time=0.55)
        self.play(FadeIn(edit_label), run_time=0.56)
        self.at("kept the protein present")
        self.play(protein.animate.set_stroke(PURPLE, width=7), run_time=0.88)
        self.at("lowered the calcium")
        self.play(FadeOut(pulses[0]), FadeOut(pulses[1]), run_time=1.08)
        released = label("Less release", 3.69, -1.05, YELLOW, 30)
        self.at("sensitivity of release")
        self.play(FadeIn(released), run_time=0.65)
        panels, human, animal, bridge, ring = comparator()
        self.at("each model isolated", lead=0.47)
        self.play(FadeOut(name), FadeOut(edit_label), FadeOut(released), run_time=0.31)
        self.play(FadeOut(milestone), FadeOut(tissue), FadeOut(protein), FadeOut(edit),
                  FadeOut(route), FadeOut(release), FadeOut(calcium),
                  FadeOut(pulses[2]), ReplacementTransform(field, ring),
                  FadeIn(animal), FadeIn(panels.right_frame), run_time=1.1)
        self.play(FadeIn(panels.right_head), run_time=0.65)
        pulse(ring, base=5, amp=3)
        self.at("human studies confirm")
        self.play(FadeIn(human), FadeIn(panels.left_frame), GrowArrow(bridge), run_time=0.77)
        self.play(FadeIn(panels.left_head), run_time=0.40)
        wave(self, bridge, BLUE, radius=0.18)
        self.finish()


class S13End(EndCard):
    LINE = "Animal models recreate disease features to test cause, not copy people."
