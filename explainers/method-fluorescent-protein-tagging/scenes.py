"""Word-synced schematics for What a Fluorescent Tag Can Tell You.

Color map from the methods films: GREY for cell structures and untagged
proteins, GREEN for GFP and GFP-tagged spots, BLUE for the cyan end, YELLOW
for the yellow end, PURPLE for calcium and ORANGE for a targeting address.
A distinct violet-blue represents excitation; TEAL identifies the marker.
"""
from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
EXCITATION = "#7985FF"
CELL = "#314953"
CELL_INNER = "#18272D"
LINK = "#8495A4"
PREDICTION = "What happens to the ratio?"
PREDICT_CARD = {"y": -3.18, "size": 37}
PROTEIN_HOME = np.array([-3.35, -0.65, 0])
PEROXISOME_AT = np.array([3.2, 0.1, 0])


def point(x, y):
    return np.array([x, y, 0.0])


def shape(coords, color, edge=None, opacity=1):
    """A filled, rounded silhouette made from a short list of outline anchors."""
    vertices = [point(x, y) for x, y in coords]
    return (VMobject().set_points_smoothly([*vertices, vertices[0]])
            .set_fill(color, opacity).set_stroke(edge or color, 2.5 if edge else 0))


def block(w, h, color, center, fill=0.8):
    return RoundedRectangle(width=w, height=h, corner_radius=min(w, h) * 0.22,
                            stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=fill).move_to(center)


def heading(text, color=TEXT, x=0, y=3.27, size=34):
    return T(text, size, color).move_to(point(x, y))


def light_spot(at, r=0.14, color=GREEN):
    halo = Circle(radius=r * 1.95, stroke_width=0, fill_color=color, fill_opacity=0.17)
    rim = Circle(radius=r * 1.38, stroke_width=0, fill_color=color, fill_opacity=0.25)
    return VGroup(halo, rim, Dot(radius=r, color=color),
                  Dot(radius=r * 0.39, color=interpolate_color(ManimColor(color), WHITE, 0.57))).move_to(at)


def flow(mob, distance, phase=0.0):
    """Drift a patch of cytoplasm around a fixed center."""
    center = mob.get_center().copy()
    clock = 0.0

    def advance(patch, dt):
        nonlocal clock
        clock += dt
        dx = np.sin(1.53 * clock + phase) - np.sin(phase)
        dy = np.sin(2.09 * clock + phase) - np.sin(phase)
        patch.move_to(center + point(distance * dx, distance * 0.58 * dy))

    mob.add_updater(advance)
    return mob


def intracellular_field():
    body = shape([(-6.55, -0.38), (-5.5, 1.7), (-3.45, 2.6), (0.4, 2.45),
                  (3.5, 1.9), (6.05, 0.85), (6.35, -0.65), (4.5, -2.35),
                  (1.5, -2.73), (-2.2, -2.58), (-5.0, -2.0)], CELL)
    stream = shape([(-5.43, -0.57), (-4.6, 0.72), (-2.4, 1.46), (0.5, 1.23),
                    (3.75, 0.6), (5.27, -0.04), (4.5, -1.4), (1.82, -1.83),
                    (-1.34, -1.64), (-4.05, -1.4)], CELL_INNER)
    flow(stream, 0.58)
    return VGroup(body, stream).set_z_index(-5)


def branch_world(close=False, glow=True, floating=False):
    """Wide nerve branch with contact-linked puncta, or the large central contact."""
    if close:
        membrane = shape([(-6.58, 0.45), (-4.8, 0.68), (-2.6, 0.73),
                          (0, 0.74), (3.0, 0.86), (6.5, 0.87), (6.48, -0.08),
                          (3.0, -0.24), (-0.3, -0.23), (-3.3, -0.42),
                          (-6.57, -0.53)], LINK)
        interior = shape([(-6.55, -0.05), (-3.8, 0.04), (-0.4, 0.17), (3.6, 0.24),
                          (6.49, 0.36), (6.45, -1.9), (5.22, -2.47), (2.73, -2.72),
                          (-1.4, -2.76), (-4.7, -2.63), (-6.5, -2.12)], CELL)
        current = shape([(-5.75, -1.17), (-3.96, -0.96), (-1.06, -0.74), (1.84, -0.62),
                         (4.72, -0.50), (5.8, -0.87), (3.82, -1.85), (0.97, -2.18),
                         (-2.43, -2.18), (-4.95, -1.94)], CELL_INNER)
        return VGroup(membrane, interior, flow(current, 0.39)).stretch(0.95, 0, about_point=ORIGIN)
    # Two lobes of the same branching extension join the thick incoming trunk.
    main = shape([(-6.58, -1.16), (-4.9, -0.62), (-3.5, 0.09), (-1.5, 0.68),
                  (1.0, 0.84), (3.3, 1.24), (6.24, 1.98), (6.46, 1.35),
                  (3.5, 0.44), (1.12, -0.32), (-1.63, -0.52),
                  (-3.52, -1.23), (-4.9, -1.98), (-6.52, -2.55)], CELL)
    upper = shape([(-4.52, -0.76), (-3.1, 0.45), (-2.06, 1.25), (-1.12, 1.91),
                   (0.48, 2.43), (1.1, 2.61), (0.96, 2.92), (0.15, 2.86),
                   (-1.49, 2.53), (-2.66, 1.86), (-3.65, 1.03), (-4.73, 0.05)], CELL)
    lower = shape([(-2.5, -0.36), (-0.68, -0.54), (0.96, -1.04), (2.52, -1.54),
                   (4.9, -2.32), (5.27, -2.42), (5.16, -2.79), (4.69, -2.73),
                   (2.29, -2.17), (0.66, -1.69), (-0.9, -1.41), (-2.42, -1.16)], CELL)
    ridge = shape([(-6.45, -1.54), (-4.7, -0.95), (-2.45, 0.04), (-0.5, 0.46),
                   (1.62, 0.62), (4.05, 1.15), (6.21, 1.72), (6.25, 1.54),
                   (4.12, 0.88), (1.56, 0.26), (-0.92, 0.1), (-2.86, -0.39),
                   (-4.72, -1.45), (-6.44, -1.94)], "#587687")
    positions = [(-5.55, -1.42), (-4.47, -0.95), (-3.32, -0.5), (-2.32, -0.19),
                 (-1.1, 0.17), (0, 0.27), (1.18, 0.38), (2.32, 0.58), (3.42, 0.9),
                 (4.6, 1.2), (5.62, 1.52), (-3.05, 1.08), (-2.27, 1.65),
                 (-1.38, 2.23), (-0.28, 2.55), (0.65, -1.34), (1.73, -1.65),
                 (2.82, -1.98), (4.07, -2.29)]
    contacts = VGroup(*[block(0.38, 0.24, LINK, point(x, y + 0.07), fill=0.36).rotate(0.18)
                        for x, y in positions])
    dots = VGroup(*[light_spot(point(x, y), 0.09 + 0.023 * (i % 3))
                    for i, (x, y) in enumerate(positions)])
    if floating:
        for i, dot in enumerate(dots):
            dot.shift(point(0.19 * np.sin(i * 2), 0.29 * np.cos(i * 1.7)))
    if not glow:
        for halo, rim, core, gleam in dots:
            halo.set_fill(opacity=0)
            rim.set_fill(opacity=0.06)
            core.set_fill(opacity=0.48)
            gleam.set_fill(opacity=0.29)
    branch = VGroup(main, upper, lower, ridge, contacts, dots).stretch(0.96, 0, about_point=ORIGIN)
    wave = 0.0

    def light_drift(mob, dt):
        nonlocal wave
        wave += dt
        for part, phase in zip(mob[:4], (0.0, 0.48, 0.96, 1.6)):
            part.set_fill(opacity=0.80 + 0.19 * np.cos(1.92 * wave + phase))

    light_drift(branch, 0.0)
    return branch.add_updater(light_drift)


def scaffold(at, glowing=False):
    body = shape([(-1.48, 0.28), (-0.9, 0.51), (-0.5, 0.32), (-0.1, 0.43),
                  (0.8, 0.44), (1.26, 0.16), (1.25, -0.27), (0.68, -0.4),
                  (0.16, -0.29), (-0.32, -0.48), (-0.9, -0.49), (-1.47, -0.24)],
                 GREY, TEXT)
    tag = block(0.85, 0.72, GREEN, point(1.55, 0.05), fill=0.57)
    glow = light_spot(tag.get_center(), 0.52).set_opacity(0.5 if glowing else 0)
    model = VGroup(glow, body, tag).shift(at)
    return model, tag, glow


def excitation(at=ORIGIN, width=5.2, height=2.2):
    x, y, _ = at
    return Polygon(point(x - width / 2, y + height / 2), point(x + width / 2, y + height / 2),
                   point(x + width * 0.43, y - height / 2), point(x - width * 0.43, y - height / 2),
                   stroke_width=0, fill_color=EXCITATION, fill_opacity=0.23)


def calcium_cloud():
    positions = [(-5.64, 0.15), (-4.75, -1.55), (-4.13, -2.06), (-2.89, -2.27),
                 (-1.58, -1.82), (-0.2, -1.72), (1.15, -1.52), (1.8, 0.04)]
    return VGroup(*[Dot(point(x, y), radius=0.10 + 0.03 * (i % 3), color=PURPLE)
                    for i, (x, y) in enumerate(positions)])


def bound_calcium(cup_at):
    return VGroup(*[Dot(cup_at + point(dx, dy), radius=0.13, color=PURPLE)
                    for dx, dy in [(-0.52, 0.20), (0.51, -0.35)]])


def high_calcium():
    return VGroup(calcium_cloud()[2:], bound_calcium(point(-1.96, -0.60)))


def sensor(grip, balance, emphasis=None):
    """Same unscaled four-part sensor. Grip sets geometry and balance sets the light."""
    links = VGroup(*[CubicBezier(ORIGIN, LEFT, RIGHT, UP, color=LINK, stroke_width=13)
                     for _ in range(3)])
    cyan = block(1.65, 1.35, BLUE, ORIGIN)
    yellow = block(1.65, 1.35, YELLOW, ORIGIN)
    cup = shape([(-1.0, -0.61), (-1.2, 0.06), (-0.92, 0.57), (-0.52, 0.6),
                 (-0.48, 0.13), (-0.18, -0.12), (0.35, -0.09), (0.48, 0.19),
                 (0.48, 0.47), (0.81, 0.33), (0.91, -0.22), (0.54, -0.63),
                 (-0.20, -0.77)], GREY, LINK)
    peptide = block(0.78, 0.46, TEXT, ORIGIN, fill=0.67)
    blue_halo = Ellipse(width=2.5, height=2.05, color=BLUE, fill_opacity=0.16, stroke_width=0)
    yellow_halo = Ellipse(width=2.5, height=2.05, color=YELLOW, fill_opacity=0.16, stroke_width=0)
    group = VGroup(blue_halo, yellow_halo, links, cup, peptide, cyan, yellow)

    def pose():
        closed = grip.get_value()
        endpoints = [point(-4.9 + 2.34 * closed, 1.15 + 0.16 * closed),
                     point(1.04 - 0.84 * closed, 1.15 + 0.16 * closed)]
        cup_at = point(-3.54 + 1.58 * closed, -0.92 + 0.32 * closed)
        short_at = point(-0.32 - 1.46 * closed, -0.86 + 0.74 * closed)
        return *endpoints, cup_at, short_at

    def refresh(_):
        a, b, c, d = pose()
        cyan.move_to(a)
        yellow.move_to(b)
        cup.move_to(c)
        peptide.move_to(d)
        strength = balance.get_value()
        cyan.set_fill(BLUE, 0.94 - 0.52 * strength)
        yellow.set_fill(YELLOW, 0.29 + 0.66 * strength)
        blue_halo.move_to(a).set_fill(BLUE, 0.25 * (1 - strength))
        yellow_halo.move_to(b).set_fill(YELLOW, 0.24 * strength)
        cup.set_fill(GREY, 1)
        if emphasis is not None:
            cup.set_stroke(interpolate_color(ManimColor(LINK), ManimColor(TEXT), emphasis.get_value()), 2.5)
        for cord, p, q, bend in zip(links, (a, c, d), (c, d, b), (-0.72, -0.21, 0.55)):
            cord.set_points(CubicBezier(p, p + point(bend, -0.86),
                                        q + point(bend, -0.62), q).get_points())

    refresh(group)
    group.add_updater(refresh)
    return group, pose, cup, peptide


def ratio_display(indicator, show_tip=True):
    """Fraction with a qualitative scale. It deliberately displays no values."""
    panel = block(4.55, 2.55, LINK, point(4.2, 0.14), fill=0.07)
    top = T("Yellow brightness", 31, YELLOW).move_to(point(3.91, 0.73))
    bottom = T("Cyan brightness", 31, BLUE).move_to(point(3.91, -0.40))
    rule = Line(point(2.47, 0.18), point(5.35, 0.18), color=TEXT, stroke_width=2.5)
    track_x = 5.95
    track = Line(point(track_x, -0.73), point(track_x, 1.00), color=LINK, stroke_width=3)
    tip = Triangle(color=TEXT, stroke_width=0, fill_opacity=1).rotate(PI / 2).scale(0.125)

    def update_tip(mob):
        mob.move_to(point(track_x + 0.21, -0.73 + 1.73 * indicator.get_value()))

    update_tip(tip)
    tip.add_updater(update_tip)
    group = VGroup(panel, top, rule, bottom, track, tip)
    if not show_tip:
        track.set_opacity(0)
        tip.set_opacity(0)
    return group, top, rule, bottom, track, tip


def close_sensor_world():
    grip, balance, indicator = ValueTracker(1), ValueTracker(0.80), ValueTracker(0.84)
    model, _, _, _ = sensor(grip, balance)
    display, *_ = ratio_display(indicator)
    return intracellular_field(), model, high_calcium(), display


def targeted_protein(masked=True):
    """The same tip and green tag return at the start of the control scene."""
    center = PROTEIN_HOME
    body = shape([(-1.25, -0.25), (-1.17, 0.42), (-0.69, 0.64), (-0.23, 0.46),
                  (0.53, 0.45), (0.98, 0.25), (1.13, -0.12), (0.82, -0.44),
                  (0.37, -0.52), (-0.36, -0.45), (-0.91, -0.58)], GREY, TEXT).shift(center)
    address = block(0.48, 0.59, ORANGE, center + point(1.09, 0.01))
    tag = block(0.87, 0.85, GREEN, center + point(1.27 if masked else -0.64, 0.02),
                fill=1 if masked else 0.80)
    return body, address, tag


def compartment(at=PEROXISOME_AT, w=4.3, h=4.65):
    return (Ellipse(width=w, height=h, color=GREY, stroke_width=3)
            .set_fill("#405963", opacity=1).rotate(0.22).move_to(at))


def marker_field():
    centers = [point(-3.8, 0.94), point(-0.32, -0.58), point(3.43, 0.65)]
    compartments = VGroup(*[compartment(c, 1.72, 1.54) for c in centers])
    markers = VGroup(*[Ellipse(width=1.42, height=1.22, color=TEAL, stroke_width=6)
                       .rotate(0.22).move_to(c) for c in centers])
    return compartments, markers


def comparison_cell(at, w, h):
    body = shape([(-0.50, 0.03), (-0.41, 0.34), (-0.17, 0.47), (0.18, 0.46),
                  (0.44, 0.29), (0.51, 0.01), (0.39, -0.32), (0.14, -0.48),
                  (-0.19, -0.43), (-0.45, -0.24)], "#405963", GREY)
    body.stretch_to_fit_width(w).stretch_to_fit_height(h).move_to(at)
    return body


def large_cell():
    return comparison_cell(point(3.0, -0.05), 5.25, 5.02)


def whi5_spots(at, w, h):
    # Both sets have the same count; the drawn positions have no experimental scale.
    positions = [(-0.52, 0.22), (0.38, -0.39), (-0.15, 0.56), (0.58, -0.16),
                 (0.04, -0.06), (-0.46, -0.42), (0.42, 0.47), (0.01, -0.63),
                 (-0.60, -0.08), (0.22, 0.20), (-0.24, -0.24), (0.19, 0.67)]
    dots = VGroup(*[light_spot(at + point(x * w * 0.46, y * h * 0.46), 0.106)
                    for x, y in positions])
    return dots


class FilmScene(SpokenScene):
    """Leave a short moving beat after the supplied audio for the picture to settle."""

    def setup(self):
        super().setup()
        self.narration_s += 0.80
        self.add(scope_tag(size=28))


class S01Hook(FilmScene, TitleCard):
    TITLE = "What a Fluorescent Tag Can Tell You"
    LESSON = "Fluorescent Protein Tagging"

    def construct(self):
        branch = branch_world(glow=False, floating=True)
        question = question_card("Where does it go?", y=3.25, size=43)
        question.shift(LEFT * 3.1)
        self.add(branch, question)
        self.at("where does a protein")
        settled = branch_world()[-1]
        self.play(LaggedStart(*[dot.animate.move_to(target)
                                for dot, target in zip(branch[-1], settled)], lag_ratio=0.07),
                  run_time=3.2)
        self.at("look at this branch")
        self.play(branch[-2].animate.set_fill(opacity=0.64), run_time=1.3)
        self.at("those green dots")
        self.play(Transform(branch[-1], settled), run_time=2.9)
        self.at("its own fluorescent tag")
        title = heading(self.TITLE, x=-0.8, size=42)
        lesson = heading(self.LESSON, TEAL, x=-1.5, y=-2.10, size=29)
        self.play(FadeOut(question), run_time=0.22)
        self.play(FadeIn(title), FadeIn(lesson), run_time=0.28)
        self.wait(1.0)
        self.play(FadeOut(title), FadeOut(lesson), run_time=0.28)
        self.finish()


class S02Tag(FilmScene):
    def construct(self):
        branch = branch_world()
        branch[-2].set_fill(opacity=0.64)
        close = branch_world(close=True)
        tag = block(1.08, 0.81, GREEN, point(0, -1.22), fill=0.56).set_z_index(2)
        self.add(branch)
        self.at("green fluorescent protein", lead=0)
        self.play(FadeOut(branch), FadeIn(close, scale=0.88),
                  FadeIn(tag, shift=UP * 0.2), run_time=1.32)
        self.at("or gfp")
        name = place_label(T("GFP", 34, GREEN), tag, dirs=(DOWN,), buff=0.54)
        self.play(FadeIn(name), run_time=0.4)
        self.at("gives off green")
        beam = excitation(point(0, -0.1), width=2.34, height=2.48)
        shine = light_spot(tag.get_center(), 0.39).set_z_index(1)
        self.play(FadeIn(beam, shift=DOWN * 0.4), run_time=1.05)
        self.play(FadeIn(shine), tag.animate.set_fill(GREEN, opacity=1), run_time=0.5)
        self.at("blue light shines")
        self.play(beam.animate.set_fill(EXCITATION, 0.34), run_time=0.85)
        self.at("join its gene")
        self.play(FadeOut(name), FadeOut(beam), FadeOut(shine), FadeOut(tag), run_time=0.34)
        other = block(3.55, 0.55, GREY, point(-3.32, -1.12))
        gene = block(1.66, 0.55, GREEN, point(3.55, -1.12))
        self.play(FadeIn(other, shift=RIGHT * 0.45), FadeIn(gene, shift=LEFT * 0.45), run_time=0.55)
        self.play(other.animate.shift(RIGHT * 2.25), gene.animate.shift(LEFT * 2.02), run_time=1.65)
        self.at("the cell makes")
        product, attached_tag, shine = scaffold(point(0, -1.16))
        self.play(ReplacementTransform(VGroup(other, gene), product), run_time=1.35)
        self.at("with gfp attached")
        final_beam = excitation(point(attached_tag.get_x(), 0.43), width=2.48, height=3.22)
        self.play(FadeIn(final_beam, shift=DOWN * 0.32), run_time=1.10)
        self.at("so green light marks")
        self.play(shine.animate.set_opacity(0.50), run_time=1.30)
        self.play(FadeOut(final_beam), run_time=0.55)
        self.finish()


class S03Location(FilmScene):
    def construct(self):
        branch = branch_world(close=True)
        sample, _, _ = scaffold(point(0, -1.16), glowing=True)
        contact = shape([(-1.32, 1.05), (-1.61, 1.62), (-1.2, 2.34), (-0.77, 2.78),
                         (0.61, 2.79), (1.04, 2.35), (1.53, 1.68), (1.35, 1.12),
                         (0.78, 0.82), (-0.48, 0.83)], "#4C6672", GREY)
        self.add(branch, sample)
        self.at("here the tagged protein")
        label = heading("Gephyrin", x=0, y=-2.31, size=35)
        self.play(FadeIn(label), run_time=0.56)
        self.at("it forms a scaffold")
        self.play(FadeIn(contact, shift=DOWN * 0.55), sample.animate.shift(UP * 0.48), run_time=1.36)
        self.at("inhibitory synapses")
        synapse_label = place_label(T("Inhibitory synapse", 32), contact, dirs=(RIGHT,), buff=0.50)
        self.play(FadeIn(synapse_label), run_time=0.44)
        self.at("where one cell")
        self.play(contact.animate.shift(DOWN * 0.08), run_time=1.48)
        self.at("pull back")
        self.play(FadeOut(label), FadeOut(synapse_label), run_time=0.35)
        broad = branch_world()
        bright = broad[-1]
        broad.remove(bright)
        self.play(FadeOut(branch, scale=0.65), FadeOut(contact, scale=0.40),
                  FadeOut(sample, scale=0.35), FadeIn(broad, scale=0.92), run_time=1.36)
        self.at("rows of bright dots")
        self.play(LaggedStart(*[FadeIn(dot, scale=0.4) for dot in bright], lag_ratio=0.13),
                  run_time=2.55)
        self.finish()


class S04Sensor(FilmScene):
    def construct(self):
        branch = branch_world()
        self.add(branch)
        self.at("show where something is")
        self.play(branch[-1][5][0].animate.scale(1.5), run_time=0.9)
        self.at("report a signal")
        field = intracellular_field()
        focus = branch[-1][5]
        branch[-1].remove(focus)
        self.add(focus)
        self.play(FadeOut(branch), FadeIn(field, scale=0.86),
                  focus.animate.scale(3.2).shift(LEFT * 0.58), run_time=1.65)
        self.at("calcium acts")
        ions = calcium_cloud()
        ion_label = heading("Calcium", PURPLE, x=-3.7)
        self.play(FadeOut(focus, scale=1.32),
                  LaggedStart(*[FadeIn(dot, shift=point(0.35, 0.17)) for dot in ions],
                              lag_ratio=0.10), run_time=1.1)
        self.play(FadeIn(ion_label), run_time=0.40)
        self.at("one calcium sensor")
        grip, strength, emphasis = ValueTracker(0), ValueTracker(0.18), ValueTracker(0)
        model, pose, cup, peptide = sensor(grip, strength, emphasis)
        self.play(FadeOut(ion_label), FadeOut(ions, shift=LEFT * 0.38), run_time=0.38)
        self.play(FadeIn(model), run_time=1.2)
        a, b, _, _ = pose()
        cyan_label = heading("Cyan", BLUE, x=a[0], y=2.63)
        yellow_label = heading("Yellow", YELLOW, x=b[0], y=2.63)
        self.at("cyan and yellow")
        self.play(FadeIn(cyan_label), FadeIn(yellow_label), run_time=0.48)
        self.at("between them sit")
        self.play(FadeOut(cyan_label), FadeOut(yellow_label),
                  emphasis.animate.set_value(1), run_time=0.52)
        calmodulin = place_label(T("Calmodulin", 32), cup, dirs=(DOWN,), buff=0.32)
        self.at("called calmodulin")
        self.play(FadeIn(calmodulin), run_time=0.39)
        self.at("a short piece")
        binder = place_label(T("Short piece", 32), peptide, dirs=(DOWN,), buff=0.48)
        self.play(FadeIn(binder), run_time=0.40)
        self.wait(1.34)
        self.play(FadeOut(calmodulin), FadeOut(binder), emphasis.animate.set_value(0), run_time=0.43)
        self.finish()


class S05Transfer(FilmScene):
    def construct(self):
        grip, balance = ValueTracker(0), ValueTracker(0.18)
        model, pose, _, _ = sensor(grip, balance)
        self.add(intracellular_field(), model)
        ions = calcium_cloud()
        self.at("when calcium rises")
        self.play(LaggedStart(*[FadeIn(dot, shift=point(0.42, 0.20)) for dot in ions],
                              lag_ratio=0.08), run_time=1.36)
        self.at("it binds calmodulin")
        _, _, cup_at, _ = pose()
        bound = bound_calcium(cup_at)
        self.play(ReplacementTransform(ions[0], bound[0]),
                  ReplacementTransform(ions[1], bound[1]), run_time=0.87)
        self.at("which grips")
        self.play(grip.animate.set_value(1), bound.animate.shift(point(1.58, 0.32)), run_time=2.68)
        self.at("shine light")
        wash = excitation(point(-1.20, 0.97), width=6.36, height=3.65).set_z_index(-1)
        self.play(FadeIn(wash, shift=DOWN * 0.28), balance.animate.set_value(0.04), run_time=1.50)
        self.at("with yellow close")
        a, b, _, _ = pose()
        path = CubicBezier(a + point(0.82, 0.05), a + point(1.1, 0.60),
                           b + point(-1.1, 0.60), b + point(-0.82, 0.05))
        pulse_dot = light_spot(path.get_start(), 0.13, color=YELLOW)
        self.at("some energy passes")
        self.play(FadeIn(pulse_dot, scale=0.5), run_time=0.26)
        self.play(MoveAlongPath(pulse_dot, path, rate_func=linear), run_time=1.75)
        self.at("making yellow brighter")
        self.play(FadeOut(pulse_dot), balance.animate.set_value(0.80), run_time=1.55)
        self.play(FadeOut(wash), run_time=0.50)
        self.finish()


class S06Predict(FilmScene):
    def construct(self):
        grip, balance, indicator = ValueTracker(1), ValueTracker(0.80), ValueTracker(0.22)
        model, _, _, _ = sensor(grip, balance)
        self.add(intracellular_field(), model, high_calcium())
        display, top, rule, bottom, track, tip = ratio_display(indicator)
        self.at("to track the change")
        self.play(FadeIn(display[0], shift=RIGHT * 0.34), run_time=0.92)
        self.at("divide the yellow")
        self.play(FadeIn(top), FadeIn(rule), run_time=0.55)
        self.at("the cyan brightness")
        self.play(FadeIn(bottom), run_time=0.42)
        self.at("this ratio rises")
        self.play(FadeIn(track), FadeIn(tip), run_time=0.55)
        self.play(indicator.animate.set_value(0.84), run_time=2.05)
        self.at("if calcium drops")
        question = question_card(PREDICTION, **PREDICT_CARD)
        self.at("what should happen", lead=0.45)
        self.play(FadeIn(question), run_time=0.55)
        self.finish()


class S07Think(PredictPause):
    QUESTION = PREDICTION
    CARD = PREDICT_CARD
    SECONDS = 4.5

    def backdrop(self):
        return VGroup(*close_sensor_world(), scope_tag(size=28))

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        self.wait(self.SECONDS)


class S08Reveal(FilmScene):
    def construct(self):
        grip, balance, indicator = ValueTracker(1), ValueTracker(0.80), ValueTracker(0.84)
        model, pose, _, _ = sensor(grip, balance)
        display, *_ = ratio_display(indicator)
        question = question_card(PREDICTION, **PREDICT_CARD)
        ions, bound = high_calcium()
        self.add(intracellular_field(), model, ions, bound, display, question)
        self.at("as calcium drops")
        self.play(FadeOut(question), FadeOut(ions, shift=LEFT * 0.46), run_time=1.17)
        self.at("the grip loosens")
        self.play(grip.animate.set_value(0.14), FadeOut(bound, shift=DOWN * 0.50), run_time=2.50)
        self.at("less energy passes")
        a, b, _, _ = pose()
        remnant = light_spot(a + point(0.8, 0.05), 0.095, YELLOW).set_opacity(0.53)
        self.play(FadeIn(remnant), run_time=0.30)
        self.play(FadeOut(remnant, shift=(b - a) * 0.32), grip.animate.set_value(0), run_time=1.35)
        self.at("yellow gives off less")
        self.play(balance.animate.set_value(0.46), indicator.animate.set_value(0.53), run_time=2.12)
        self.at("brightness falls", lead=0.65)
        self.play(balance.animate.set_value(0.18), indicator.animate.set_value(0.22), run_time=1.95)
        self.at("the readout follows")
        self.play(grip.animate.set_value(0.23), balance.animate.set_value(0.30),
                  indicator.animate.set_value(0.34), run_time=1.55)
        self.play(grip.animate.set_value(0), balance.animate.set_value(0.18),
                  indicator.animate.set_value(0.22), run_time=1.72)
        self.finish()


class S09Pitfall(FilmScene):
    def construct(self):
        model, _, _, _ = sensor(ValueTracker(0), ValueTracker(0.18))
        ratio, *_, tip = ratio_display(ValueTracker(0.22))
        self.add(intracellular_field(), model, ratio)
        body, address, tag = targeted_protein(masked=False)
        tag.move_to(point(-3.75, 1.26))
        self.at("for a location measurement")
        tip.clear_updaters()
        self.play(FadeOut(ratio, scale=0.35, shift=RIGHT * 0.32), FadeOut(model), run_time=0.90)
        self.play(FadeIn(body, shift=RIGHT * 0.34), FadeIn(tag, shift=RIGHT * 0.34), run_time=0.78)
        self.at("the tag itself")
        self.play(tag.animate.shift(UP * 0.12), run_time=0.86)
        self.at("some proteins carry")
        self.play(FadeIn(address, shift=LEFT * 0.14), run_time=0.75)
        name = place_label(T("Tip address", 32, ORANGE), address, dirs=(UP,), buff=0.51)
        self.at("at their very end")
        self.play(FadeIn(name), run_time=0.45)
        self.at("that address sends")
        organelle = compartment()
        self.play(FadeOut(name), FadeIn(organelle, scale=0.91), run_time=0.60)
        sample = VGroup(body, address)
        self.play(sample.animate.shift(RIGHT * 3.75), run_time=1.35)
        organelle_name = heading("Peroxisome", TEXT, x=3.2, y=2.95)
        self.at("called peroxisomes")
        self.play(FadeIn(organelle_name), run_time=0.44)
        self.play(sample.animate.shift(LEFT * 3.75), run_time=1.25)
        self.at("a tag placed after it")
        tag.set_z_index(2)
        self.play(Transform(tag, targeted_protein()[2]), run_time=1.42)
        self.finish()


class S10Guard(FilmScene):
    def construct(self):
        field = intracellular_field()
        body, address, tag = targeted_protein()
        organelle = compartment()
        name = heading("Peroxisome", TEXT, x=3.2, y=2.95)
        self.add(field, body, address, organelle, tag, name)
        self.at("put the tag where")
        self.play(Transform(tag, targeted_protein(masked=False)[2]), run_time=1.33)
        self.at("stays exposed")
        self.play(address.animate.set_fill(ORANGE, 1), run_time=0.74)
        self.at("then use a marker")
        self.play(FadeOut(name), run_time=0.26)
        compartments, markers = marker_field()
        self.play(FadeOut(body, scale=0.44), FadeOut(address, scale=0.44),
                  FadeOut(tag, scale=0.44), ReplacementTransform(organelle, compartments[2]),
                  FadeIn(compartments[:2], scale=0.85), run_time=1.30)
        self.at("shows where the peroxisomes are")
        self.play(LaggedStart(*[Create(marker) for marker in markers], lag_ratio=0.20), run_time=1.1)
        marker_label = heading("Peroxisome marker", TEAL, x=-2.95)
        self.play(FadeIn(marker_label), run_time=0.40)
        self.at("check whether")
        check = question_card("Do the signals overlap?", **PREDICT_CARD)
        self.play(FadeIn(check), run_time=0.45)
        # Sample positions illustrate a comparison without assigning a result.
        green = VGroup(light_spot(compartments[0].get_center(), 0.18),
                       light_spot(compartments[2].get_center() + point(-1.0, -1.25), 0.18))
        green_label = heading("Tagged protein", GREEN, x=2.9, y=2.92, size=32)
        self.play(FadeIn(green, scale=0.65), run_time=0.48)
        self.play(FadeIn(green_label), run_time=0.32)
        self.play(LaggedStart(*[Indicate(marker, color=TEAL, scale_factor=1.13) for marker in markers],
                              lag_ratio=0.50), run_time=2.05)
        self.play(FadeOut(check), FadeOut(marker_label), FadeOut(green_label),
                  FadeOut(green), run_time=0.30)
        self.finish()


class S11Cameleon(FilmScene):
    def construct(self):
        compartments, markers = marker_field()
        field = intracellular_field()
        self.add(field, compartments, markers)
        grip, balance, indicator = ValueTracker(0), ValueTracker(0.18), ValueTracker(0.22)
        model, _, _, _ = sensor(grip, balance)
        self.at("miyawaki")
        self.play(FadeOut(compartments, scale=1.24), FadeOut(markers, scale=1.24),
                  FadeIn(model, scale=0.88), run_time=1.45)
        credit = heading("Miyawaki, Tsien and colleagues", size=32, x=-1.9)
        self.play(FadeIn(credit), run_time=0.52)
        self.at("called chameleon")
        name = heading("Cameleon", size=37, x=-1.90)
        self.play(swap(credit, name, run_time=0.78))
        self.at("1997")
        year = heading("1997", GOLD, x=3.98, y=2.83, size=32)
        self.play(FadeIn(year), run_time=0.38)
        self.at("its shifting balance")
        ratio, *_, tip = ratio_display(indicator)
        self.play(FadeIn(ratio, shift=RIGHT * 0.28), run_time=0.72)
        self.play(grip.animate.set_value(1), balance.animate.set_value(0.80),
                  indicator.animate.set_value(0.84), run_time=3.15)
        self.at("follow calcium")
        self.play(FadeOut(year), FadeOut(name), run_time=0.60)
        self.at("fluorescent tags can also")
        cell = large_cell()
        tip.clear_updaters()
        self.play(FadeOut(model, scale=0.50), FadeOut(ratio, scale=0.65), run_time=0.64)
        self.play(FadeOut(field), FadeIn(cell, scale=0.73), run_time=1.95)
        # Keep the same frame timing as the animated hold before the field was removed.
        self.always_update_mobjects = True
        self.finish()


class S12Whi5(FilmScene):
    def construct(self):
        large = large_cell()
        little = comparison_cell(point(-3.10, -0.48), 3.38, 3.44)
        large_home = large.get_center()
        self.add(flow(large, 0.36))
        self.at("in 2015")
        credit = heading("Schmoller, Skotheim and colleagues", size=32, x=-0.5)
        year = heading("2015", GOLD, x=-3.68, y=2.45, size=33)
        self.play(FadeIn(credit), FadeIn(year), run_time=0.65)
        self.at("tagged a protein")
        large.clear_updaters()
        bigger_dots = whi5_spots(large_home, large.width, large.height)
        for i, spot in enumerate(bigger_dots):
            bob(spot, amp=0.15, speed=1.2, seed=i)
        self.play(large.animate.move_to(large_home),
                  LaggedStart(*[FadeIn(spot, scale=0.6) for spot in bigger_dots], lag_ratio=0.12),
                  run_time=0.90)
        self.at("called y5")
        whi = heading("Tagged Whi5", GREEN, x=-0.5, size=37)
        self.play(swap(credit, whi, run_time=0.62), FadeOut(year), run_time=0.62)
        self.at("they measured it")
        self.play(large.animate.set_stroke(GREY, 4.3), run_time=1.4)
        self.at("at birth")
        self.play(FadeIn(little, scale=0.73), run_time=0.85)
        small_label = heading("Small daughter cell", y=2.15, x=-3.12, size=32)
        big_label = heading("Larger cell", y=2.82, x=3, size=32)
        self.play(FadeIn(small_label), FadeIn(big_label), run_time=0.48)
        self.at("about as many")
        smaller_dots = whi5_spots(little.get_center(), little.width, little.height)
        for i, spot in enumerate(smaller_dots):
            bob(spot, amp=0.10, speed=1.35, seed=i + 3)
        self.play(LaggedStart(*[FadeIn(spot, scale=0.58) for spot in smaller_dots], lag_ratio=0.09),
                  run_time=1.7)
        self.at("in less space")
        self.play(little.animate.set_stroke(GREEN, 4.2), run_time=1.16)
        self.at("more concentrated")
        self.play(FadeIn(caption("More concentrated", size=33, color=GREEN, y=-3.16)
                         .shift(LEFT * 2.24)), run_time=0.55)
        self.finish()


class S13End(EndCard):
    LINE = "Fluorescent tags reveal where proteins go and when signals change."
