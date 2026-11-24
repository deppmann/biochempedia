"""ELISA and immunoassays. Timings come from the locked Kokoro transcript.

BLUE: antibody; GOLD: target antigen; TEAL: sample and infusion;
GREEN: developed signal; RED: red cells; PURPLE: memory B cells;
GREY: glass, membrane, and other material.
"""
from bp_parts import *

PURPLE = "#B58CD9"
LIQUID = "#244C59"
DEVELOPED = "#416E45"
GLASS = "#182730"
QUESTION = "How confirm true viral proteins?"
QUESTION_CARD = {"y": 2.72, "size": 36}
SAMPLE_CENTER = (0, -0.18)
SAMPLE_SIZE = (12.0, 4.65)


def point(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=32):
    return T(text, size, color, weight=MEDIUM).move_to(point(x, y))


def plate(w, h, x=0, y=0, fill=LIQUID, phase=0, moving=False):
    """The open glass well shared by the sample, ELISA and clumping diagrams."""
    def xy(u, v):
        return point(x + w * u, y + h * v)

    def surface(t):
        return [xy(u, 0.23 + 0.025 * np.sin(13 * u + t))
                for u in np.linspace(-0.457, 0.457, 35)]

    glass = Polygon(xy(-0.5, 0.5), xy(-0.34, -0.5), xy(0.34, -0.5), xy(0.5, 0.5),
                    stroke_width=0, fill_color=GLASS, fill_opacity=1)
    liquid = Polygon(xy(-0.34, -0.5), xy(0.34, -0.5), *reversed(surface(phase)),
                     stroke_width=0, fill_color=fill, fill_opacity=1)
    rim = VMobject(stroke_color=GREY, stroke_width=3.5)
    rim.set_points_as_corners([xy(-0.5, 0.5), xy(-0.34, -0.5), xy(0.34, -0.5), xy(0.5, 0.5)])
    meniscus = VMobject(stroke_color=TEAL, stroke_width=2.5)
    meniscus.set_points_as_corners(surface(phase))
    rim.set_z_index(1)
    meniscus.set_z_index(1)
    if moving:
        def flow(mob, dt):
            mob.clock += dt
            top = surface(phase + 1.65 * mob.clock)
            meniscus.set_points_as_corners(top)
            boundary = [xy(-0.34, -0.5), xy(0.34, -0.5), *reversed(top)]
            mob.set_points_as_corners([*boundary, boundary[0]])

        liquid.clock = 0
        liquid.add_updater(flow)
    return VGroup(glass, liquid, meniscus, rim)


def reagent(x, y, scale=1, angle=0):
    """Rounded Y cartoon with cupped tips. Local origin is the branch joint."""
    branches = VGroup()
    for sign in (-1, 1):
        arm = VMobject(stroke_color=BLUE, stroke_width=10 * scale)
        arm.set_points_as_corners([point(0, 0), point(sign * 0.48, 0.51),
                                  point(sign * 0.73, 0.62), point(sign * 0.88, 0.84)])
        arm.set_cap_style(CapStyleType.ROUND)
        branches.add(arm)
    stem = Line(point(0, -0.9), ORIGIN, color=BLUE, stroke_width=12 * scale)
    stem.set_cap_style(CapStyleType.ROUND)
    return VGroup(stem, *branches).scale(scale, about_point=ORIGIN).rotate(
        angle, about_point=ORIGIN).shift(point(x, y)).set_z_index(3)


def target(x, y, r, opacity=1):
    body = Circle(radius=r, stroke_color=YELLOW, stroke_width=2.5, fill_color=GOLD,
                  fill_opacity=0.82 * opacity, stroke_opacity=opacity)
    return body.move_to(point(x, y)).set_z_index(4)


def unknown(x, y, r, form):
    shape = RegularPolygon(n=form, radius=r, stroke_color=GREY, stroke_width=1.2,
                           fill_color=GREY, fill_opacity=0.42, stroke_opacity=0.72)
    return shape.rotate(0.25).move_to(point(x, y)).set_z_index(2)


def swirl(particles, radius=0.34, speed=1.65):
    """Circulation belongs to the solution. Each particle follows a bounded orbit."""
    homes = [particle.get_center().copy() for particle in particles]
    particles.clock = 0

    def update(group, dt):
        group.clock += dt
        for i, (particle, home) in enumerate(zip(group, homes)):
            angle = speed * group.clock * (0.82 + 0.067 * (i % 6)) + i * 2.4
            particle.move_to(home + point(radius * np.sin(angle), radius * 0.55 * np.cos(angle)))

    particles.add_updater(update)
    return particles


def opening_sample():
    well = plate(*SAMPLE_SIZE, *SAMPLE_CENTER, moving=True)
    coords = [(-4.3, 0.2), (-3.75, -0.55), (-3.1, -1.45), (-2.75, 0.36),
              (-2, -0.5), (-1.5, -1.75), (-0.9, 0.44), (-0.20, -1.3),
              (0.6, -0.4), (1.1, -1.72), (1.8, 0.35), (2.45, -1.25),
              (3.35, -0.66), (4.43, 0.54), (2.95, 0.48), (-3.72, -1.32)]
    particles = VGroup(*[unknown(x, y, 0.13 + 0.036 * (i % 4), 3 + i % 3)
                         for i, (x, y) in enumerate(coords)],
                       target(-2.75, -0.87, 0.23, 0.62),
                       target(3.25, -0.25, 0.29, 0.78))
    return well, particles


def sample_tag():
    return scope_tag(size=28, color=TEXT)


class S01Hook(SpokenScene, TitleCard):
    LESSON = "ELISA and Immunoassays"
    TITLE = "Catching One Molecule With an Antibody"

    def construct(self):
        well, particles = opening_sample()
        query = label("?", 4.40, -0.56, YELLOW, size=58)
        title = fit_text(self.TITLE, max_w=11.6, size=42, min_size=33, font=TITLE_FONT)
        title.move_to(point(0, 2.87))
        lesson = label(self.LESSON, 0, 3.52, BLUE, size=28)
        self.add(well, swirl(particles), query, title, lesson, sample_tag())
        self.at("invisible molecule", lead=0.15)
        self.play(FadeOut(title), FadeOut(lesson), run_time=0.65)

        self.at("an enzyme reveals")
        substrate = unknown(-2.4, 1.85, 0.28, 4)
        partner = unknown(-3.8, 1.4, 0.26, 3)
        flash = Circle(radius=0.52, stroke_color=GREEN, stroke_width=5,
                       fill_color=GREEN, fill_opacity=0.18).move_to(point(-3.06, 1.66))
        self.play(FadeIn(substrate), FadeIn(partner), run_time=0.4)
        self.play(substrate.animate.move_to(flash), partner.animate.move_to(flash), run_time=0.65)
        self.play(FadeIn(flash, scale=0.65), run_time=0.35)
        self.play(FadeOut(flash, scale=1.55), FadeOut(partner), FadeOut(substrate), run_time=0.65)

        self.at("but a hormone")
        self.play(FadeOut(query), run_time=0.65)

        self.at("to measure a silent")
        antibody = reagent(0, 0.06, 1.5)
        self.play(FadeIn(antibody, shift=DOWN * 1.7), run_time=2.5)
        self.at("test called an immunoassay")
        self.play(FadeIn(label("Immunoassay", -3.55, 2.82, BLUE, 39)), run_time=0.55)
        self.finish()


class S02Antibody(SpokenScene):
    def construct(self):
        well, old_particles = opening_sample()
        antibody = reagent(0, 0.06, 1.5)
        self.add(well, antibody, swirl(old_particles), sample_tag())
        self.at("every immunoassay")
        self.play(FadeOut(old_particles), Transform(antibody, reagent(0, -0.12, 2.2)),
                  run_time=1.45)

        self.at("with an antibody")
        self.play(FadeIn(label("Antibody", -4.25, 2.78, BLUE, 38)), run_time=0.6)

        self.at("its two arm tips")
        tips = VGroup(*[Circle(radius=0.37, stroke_color=BLUE, stroke_width=4)
                         .move_to(point(sign * 1.7, 1.47)) for sign in (-1, 1)])
        antigen = target(4.15, 1.18, 0.34)
        self.play(FadeIn(tips), FadeIn(antigen), run_time=0.52)
        self.play(antigen.animate.move_to(point(1.54, 1.64)), run_time=1.7)
        self.play(FadeOut(tips), run_time=0.45)

        self.at("called an antigen")
        self.play(FadeIn(label("Antigen", 3.55, 2.55, YELLOW, 36)), run_time=0.52)
        bound_pair = VGroup(antibody, antigen)
        self.play(bound_pair.animate.shift(RIGHT * 0.63 + DOWN * 0.07), run_time=1.16)

        self.at("other molecules in")
        rejects = VGroup(unknown(-4.32, 0.73, 0.68, 3), unknown(-3.88, -0.91, 0.63, 4))
        for molecule in rejects:
            molecule.set_fill(GREY, opacity=0.97)
        self.play(FadeIn(rejects, shift=RIGHT * 0.40), run_time=0.58)
        self.play(rejects[0].animate.move_to(point(-1.77, 1.08)).rotate(0.47),
                  rejects[1].animate.move_to(point(-1.92, 0.11)).rotate(-0.54),
                  bound_pair.animate.shift(RIGHT * 0.48), run_time=1.35)
        self.play(rejects[0].animate.shift(LEFT * 1.05 + DOWN * 0.69).rotate(0.70),
                  rejects[1].animate.shift(RIGHT * 0.60 + DOWN * 1.00).rotate(-0.65),
                  bound_pair.animate.shift(LEFT * 0.48), run_time=0.90)
        self.play(FadeOut(rejects, shift=LEFT * 1.35 + DOWN * 0.22), run_time=1.27)

        self.at("once caught")
        halo = Circle(radius=0.41, stroke_color=GOLD, stroke_opacity=0.65,
                      stroke_width=4).move_to(antigen)
        readout_question = label("?", 3.0, 0.42, YELLOW, size=52)
        self.play(FadeIn(halo), FadeIn(readout_question), run_time=0.65)
        in_solution = VGroup(antibody, antigen, halo)
        self.play(in_solution.animate.shift(LEFT * 0.70 + DOWN * 0.14).rotate(
            -0.13, about_point=antibody[0].get_end()), run_time=2.4)
        self.finish()


def sandwich(xs, joint_y, scale):
    capture = VGroup(*[reagent(x, joint_y, scale) for x in xs])
    bound = VGroup(*[target(x + 0.69 * scale, joint_y + 0.85 * scale, 0.24 * scale)
                     for x in xs])
    detection = VGroup()
    for x in xs:
        center = x + 1.38 * scale
        upper = joint_y + 1.7 * scale
        antibody = reagent(center, upper, scale, PI)
        enzyme = RoundedRectangle(width=0.55 * scale, height=0.37 * scale, corner_radius=0.11 * scale,
                                  stroke_width=2, stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.8)
        enzyme.move_to(point(center, upper + 0.90 * scale)).set_z_index(4)
        detection.add(VGroup(antibody, enzyme))
    return capture, bound, detection


class S03Elisa(SpokenScene):
    def construct(self):
        well = plate(*SAMPLE_SIZE, *SAMPLE_CENTER, moving=True)
        capture, bound, detection = sandwich([-2.65, -0.65, 1.35], -1.77, 0.82)
        unbound = VGroup(*[unknown(x, y, r, n) for x, y, r, n in [
            (-3.8, 0.45, 0.26, 3), (-2.7, -0.13, 0.20, 4), (-1.3, 0.43, 0.23, 5),
            (0.25, -0.32, 0.19, 3), (1.42, 0.51, 0.28, 4), (2.82, -0.25, 0.23, 4),
            (3.68, 0.51, 0.19, 3), (3.25, -1.13, 0.23, 5)]])
        self.add(well, swirl(unbound, 0.24), sample_tag())
        self.at("a plate test")
        heading = label("ELISA", -4.83, 2.83, BLUE, 38)
        self.play(FadeIn(heading), run_time=0.58)
        self.play(LaggedStart(*(FadeIn(a, shift=DOWN * 0.18) for a in capture),
                              lag_ratio=0.27), run_time=1.35)
        self.at("and hold the target")
        self.play(LaggedStart(*(FadeIn(b, shift=DOWN * 0.68) for b in bound),
                              lag_ratio=0.23), run_time=1.30)

        self.at("unbound molecules wash")
        unbound.clear_updaters()
        self.play(FadeOut(unbound, shift=UP * 1.3 + RIGHT * 1.9), run_time=1.75)
        self.at("a second enzyme linked")
        self.play(LaggedStart(*(FadeIn(a, shift=DOWN * 1.8) for a in detection),
                              lag_ratio=0.25), run_time=2.65)

        self.at("its enzyme creates")
        self.play(well[1].animate.set_fill(DEVELOPED), well[2].animate.set_stroke(GREEN),
                  run_time=1.55)
        self.at("converted to concentration")
        well[1].clear_updaters()
        sample = VGroup(well, capture, bound, detection)
        self.play(sample.animate.scale(0.46).move_to(point(-3.55, -0.10)), run_time=0.68)

        standard = Plot(box=(0.12, 6.24, -2.35, 2.1), xr=(0, 1), yr=(0, 1),
                        xlabel="Known concentration", ylabel="Colour signal", label_size=29)
        # Beer–Lambert proportionality in a normalized illustrative linear working range.
        response = lambda concentration: 0.86 * concentration
        trace = standard.curve(response, color=GREEN)
        standards = VGroup(*[Dot(standard.pt(c, response(c)), radius=0.078, color=GREEN)
                             for c in np.linspace(0.17, 0.94, 5)])
        self.play(FadeIn(standard), run_time=0.45)
        self.at("a standard curve")
        self.play(Create(trace), FadeIn(standards), run_time=0.70)
        c = 0.62
        foot, level, result = standard.pt(c, 0), standard.pt(0, response(c)), standard.pt(c, response(c))
        guide = VGroup(DashedLine(level, result, color=GOLD, stroke_width=3, dash_length=0.12),
                       DashedLine(result, foot, color=GOLD, stroke_width=3, dash_length=0.12))
        sample_dot = Dot(result, radius=0.10, color=GOLD)
        self.play(Create(guide), FadeIn(sample_dot), run_time=1.05)
        self.finish()


def red_cell(x, y, radius, peg_angle=None):
    outer = Ellipse(width=2 * radius, height=1.46 * radius, stroke_color=RED, stroke_width=3,
                    fill_color="#843D43", fill_opacity=1).move_to(point(x, y))
    inner = Ellipse(width=1.12 * radius, height=0.72 * radius, stroke_color=RED, stroke_width=1.5,
                    stroke_opacity=0.65, fill_color="#422833", fill_opacity=1).move_to(outer)
    cell = VGroup(outer, inner).set_z_index(2)
    if peg_angle is not None:
        cell.add(target(x + radius * np.cos(peg_angle), y + 0.73 * radius * np.sin(peg_angle),
                        0.13 * radius + 0.04))
    return cell


def clump_well(x, y, width, height, density):
    dish = plate(width, height, x, y)
    if density == 0:
        offsets = [(-0.22, 0.07), (0.03, 0.08), (0.25, -0.06),
                   (-0.06, -0.22), (0.15, -0.30)]
    elif density == 1:
        offsets = [(-0.23, -0.04), (0.24, 0.06), (-0.05, -0.24),
                   (0.07, -0.27), (0.02, -0.10)]
    else:
        offsets = [(-0.12, -0.11), (0.07, -0.09), (0.00, -0.23),
                   (0.17, -0.23), (-0.14, -0.29)]
    cells = VGroup(*[red_cell(x + dx * width, y + dy * height, width * 0.094)
                     for dx, dy in offsets])
    return dish, cells


class S04Agglutination(SpokenScene):
    def construct(self):
        well = plate(*SAMPLE_SIZE, *SAMPLE_CENTER, moving=True)
        left = red_cell(-3.25, 0.1, 1.23)
        right = red_cell(3.25, 0.1, 1.23)
        self.add(well, left, right, sample_tag())
        self.at("when targets sit")
        peg_l = target(-2.02, 0.1, 0.19)
        peg_r = target(2.02, 0.1, 0.19)
        self.play(FadeIn(peg_l, scale=0.4), FadeIn(peg_r, scale=0.4), run_time=0.70)
        self.play(VGroup(left, peg_l).animate.shift(RIGHT * 0.34 + UP * 0.23),
                  VGroup(right, peg_r).animate.shift(LEFT * 0.34 + UP * 0.23), run_time=1.50)

        self.at("antibodies need no")
        linker = reagent(0, -1.04, 1.47)
        self.play(FadeIn(linker, shift=DOWN * 0.85), run_time=2.28)
        self.at("two arms link")
        self.play(VGroup(left, peg_l).animate.shift(RIGHT * 0.54 + DOWN * 0.34),
                  VGroup(right, peg_r).animate.shift(LEFT * 0.54 + DOWN * 0.34),
                  run_time=1.12)
        cluster = VGroup(left, right, peg_l, peg_r, linker)
        self.play(cluster.animate.shift(UP * 0.25), run_time=0.65)

        self.at("called agglutination")
        heading = label("Agglutination", 0, 2.75, RED, 39)
        self.play(FadeIn(heading), run_time=0.58)
        bob(cluster, amp=0.12, speed=1.8)

        self.at("diluting serum in")
        cluster.clear_updaters()
        well[1].clear_updaters()
        self.play(FadeOut(cluster), FadeOut(well), FadeOut(heading), run_time=0.44)
        row = [clump_well(x, -0.14, 2.67, 2.78, level)
               for x, level in zip((-4.62, -1.55, 1.55, 4.62), (3, 2, 1, 0))]
        dilution = label("Increasing serum dilution  →", -0.25, 2.18, TEXT, 34)
        self.play(FadeIn(dilution), LaggedStart(*(FadeIn(p) for p, _ in row), lag_ratio=0.19),
                  run_time=0.60)
        self.play(LaggedStart(*(FadeIn(c, shift=UP * 0.40) for _, c in row), lag_ratio=0.23),
                  run_time=0.92)
        for i, (_, cells) in enumerate(row):
            sway = 0.06 if i < 3 else 0.11
            swirl(cells, radius=sway, speed=1.9)

        self.at("highest dilution that")
        dish, cells = row[2]
        outline = SurroundingRectangle(dish, buff=0.12, color=GOLD, stroke_width=3.5,
                                       corner_radius=0.18)
        titer = label("Titer", 1.55, -2.07, YELLOW, 34)
        self.play(Create(outline), run_time=0.62)
        self.play(FadeIn(titer), run_time=0.60)

        self.at("more antibody survives")
        transfer = Arrow(point(-1.48, 1.61), point(1.38, 1.61), buff=0.04,
                         color=GOLD, stroke_width=4, tip_length=0.18)
        self.play(GrowArrow(transfer), run_time=1.6)

        self.at("a relative measure")
        summary = caption("Higher titer = more antibody (relative)", size=33, y=-3.1)
        self.play(FadeIn(summary), run_time=0.56)
        self.finish()


def protein(x, y, lookalike=False):
    points = [(-0.48, -0.20), (-0.32, 0.14), (-0.10, 0.19), (0.02, 0.48),
              (0.22, 0.39), (0.45, 0.19), (0.36, -0.19), (0.08, -0.30)]
    if lookalike:
        points[2:7] = [(-0.27, 0.48), (0.00, 0.66), (0.18, 0.22),
                       (0.60, 0.48), (0.55, -0.13)]
    return Polygon(*(point(x + 1.22 * a, y + 1.08 * b) for a, b in points), stroke_color=YELLOW,
                   stroke_width=3, fill_color=GOLD, fill_opacity=0.86).set_z_index(4)


def positive_well(colour=DEVELOPED, moving=True, bound=True, annotated=True):
    well = plate(10.1, 4.12, 0, -0.53, fill=colour, moving=moving)
    pair = VGroup(reagent(-0.63, -1.22, 1.44), protein(0.38, -0.17))
    if annotated:
        heading = label("Positive ELISA screen", 0, 1.89, GREEN, 38)
    else:
        heading = VGroup()
    world = VGroup(well, heading, sample_tag())
    if bound:
        world.add(pair)
    return world, pair


class S05Predict(SpokenScene):
    def construct(self):
        world, pair = positive_well(colour=LIQUID, bound=False, annotated=False)
        well = world[0]
        antibody, silhouette = pair
        self.add(world)
        self.at("one signal can")
        self.play(well[1].animate.set_fill("#355C4D"), run_time=2.3)

        self.at("an ELISA screen")
        self.play(FadeIn(antibody, shift=DOWN * 0.7), run_time=1.42)
        self.play(FadeIn(silhouette, shift=UP * 0.75), run_time=1.46)

        self.at("turns positive")
        self.play(well[1].animate.set_fill("#3B6345"), run_time=1.36)
        self.play(FadeIn(label("Positive ELISA screen", 0, 1.89, GREEN, 38)), run_time=0.55)

        self.at("sensitive but less")
        self.play(Transform(silhouette, protein(1.03, -0.17, lookalike=True)),
                  antibody.animate.shift(RIGHT * 0.65), run_time=1.8)
        self.at("cannot show which")
        self.play(Transform(silhouette, protein(0.09, -0.17)),
                  antibody.animate.shift(LEFT * 0.94), run_time=1.28)
        self.play(Transform(silhouette, protein(0.66, -0.17, lookalike=True)),
                  antibody.animate.shift(RIGHT * 0.57), run_time=0.92)
        self.play(Transform(silhouette, protein(0.38, -0.17)),
                  antibody.animate.shift(LEFT * 0.28), run_time=0.93)

        self.at("how can the lab")
        card = question_card(QUESTION, **QUESTION_CARD)
        self.play(FadeIn(card), run_time=0.78)
        self.play(well[1].animate.set_fill(DEVELOPED), run_time=3.65, rate_func=linear)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_CARD
    SECONDS = 4.5

    def backdrop(self):
        world, _ = positive_well()
        liquid = world[0][1]

        def shimmer(water, dt):
            phase = np.clip(water.clock / self.SECONDS, 0, 1)
            shine = 0.5 * np.sin(PI * phase)
            water.set_fill(interpolate_color(ManimColor(DEVELOPED), ManimColor("#588B53"), shine))

        liquid.add_updater(shimmer)
        return world

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        self.wait(self.SECONDS)


def blot_panel(x, colour):
    return RoundedRectangle(width=4.22, height=5.14, corner_radius=0.20,
                            stroke_color=colour, stroke_width=3,
                            fill_color="#253D4C", fill_opacity=1).move_to(point(x, -0.23))


def band(x, y, width, color=GREY):
    return RoundedRectangle(width=width, height=0.23, corner_radius=0.075, stroke_width=0,
                            fill_color=color, fill_opacity=0.9).move_to(point(x, y)).set_z_index(2)


class S07Confirm(SpokenScene):
    def construct(self):
        world, _ = positive_well()
        card = question_card(QUESTION, **QUESTION_CARD)
        self.add(world, card)
        self.at("classic HIV testing")
        self.play(FadeOut(card), run_time=0.43)
        well, well_heading, tag, pair = world
        well[1].clear_updaters()
        sample = VGroup(well, pair)
        self.play(sample.animate.scale(0.44).move_to(point(-3.28, -0.22)),
                  FadeOut(well_heading), run_time=0.98)

        gel = blot_panel(2.71, BLUE)
        ladder_x = 1.40
        ladder = VGroup(*[band(ladder_x, y, 0.52) for y in (1.74, 1.10, 0.48, -0.2, -1.0, -2.07)])
        gel_name = label("Gel", 2.71, 2.81, BLUE, 36)
        self.at("positives with a western")
        self.play(FadeIn(gel), run_time=0.55)
        loaded = VGroup(*[band(3.34 + dx, 1.77, width, GOLD)
                          for dx, width in [(-0.36, 0.35), (0, 0.36), (0.40, 0.40)]])
        self.play(FadeIn(ladder), FadeIn(gel_name),
                  TransformFromCopy(pair[1], loaded), run_time=1.15)

        self.at("a gel separates")
        ends = (1.35, -0.23, -1.71)
        self.play(LaggedStart(*(b.animate.move_to(point(3.31, y)).stretch_to_fit_width(1.10)
                                for b, y in zip(loaded, ends)), lag_ratio=0.23), run_time=2.60)

        self.at("then they move onto")
        membrane = blot_panel(-3.26, GREY).set_fill("#36424D")
        film_name = label("Membrane", -3.26, 2.81, TEXT, 36)
        self.play(FadeOut(sample), run_time=0.40)
        self.play(FadeIn(membrane), FadeIn(film_name), run_time=0.54)
        copied = VGroup(*[band(-3.26, y, 1.42, GOLD) for y in ends])
        self.play(TransformFromCopy(loaded, copied), run_time=1.42)

        self.at("the patient's antibodies")
        antibodies = VGroup(*[reagent(-3.83, y - 0.48, 0.60) for y in (ends[0], ends[2])])
        patient = label("Patient's antibodies", 0.40, 3.35, BLUE, 30)
        self.play(FadeIn(patient), LaggedStart(*(FadeIn(a, shift=RIGHT * 0.75) for a in antibodies),
                                               lag_ratio=0.32),
                  gel.animate.set_fill("#1C2834"), run_time=2.55)

        self.at("a true positive lights")
        self.play(FadeOut(patient), run_time=0.42)
        developed = VGroup(*[band(-3.26, y, 1.74, GREEN) for y in (ends[0], ends[2])])
        self.play(FadeOut(copied), LaggedStart(*(FadeIn(b, scale=0.45) for b in developed),
                                              lag_ratio=0.36),
                  membrane.animate.set_fill("#394E50"), run_time=1.38)
        for signal in developed:
            signal.set_fill("#669A5A")

        self.play(swap(film_name, label("Western blot", -3.26, 2.81, GREEN, 37)), run_time=0.66)

        self.at("expected sizes of")
        highlights = VGroup(*[Line(point(-2.22, y), point(-1.58, y), color=GREEN, stroke_width=4)
                              for y in (ends[0], ends[2])])
        self.play(LaggedStart(*(Create(h) for h in highlights), lag_ratio=0.3),
                  *(b.animate.set_fill(GREEN, opacity=1).stretch_to_fit_height(0.42)
                    for b in developed), membrane.animate.set_fill("#40595B"),
                  run_time=1.92)
        self.finish()


def memory_cell(x, y, r=0.37):
    outer = Circle(radius=r, stroke_color=PURPLE, stroke_width=3,
                   fill_color="#503B62", fill_opacity=1).move_to(point(x, y))
    nucleus = Circle(radius=r * 0.49, stroke_color=PURPLE, stroke_width=1.2,
                     fill_color=PURPLE, fill_opacity=0.44).move_to(point(x - r * 0.08, y))
    return VGroup(outer, nucleus)


class S08ReadoutLimit(SpokenScene):
    def construct(self):
        world, _ = positive_well(annotated=False)
        self.add(world)
        well, _, tag, pair = world
        self.at("test only measures")
        self.play(Indicate(pair[1], color=YELLOW, scale_factor=1.18), run_time=1.35)
        self.play(well[1].animate.set_fill("#355C4D"), run_time=1.35)

        self.at("ELISA tracks antibody")
        well[1].clear_updaters()
        sample = VGroup(well, pair)
        self.play(sample.animate.scale(0.44).move_to(point(-3.23, 1.06)), run_time=0.80)
        plasma = label("Plasma antibody", -3.22, 2.73, BLUE, 36)
        trend = Plot(box=(-5.95, -0.52, -2.23, -0.18), xr=(0, 1), yr=(0, 1),
                     xlabel="Time", label_size=28)
        clock = ValueTracker(0)
        # Normalized schematic of falling plasma antibody. There is no absolute scale.
        falling = lambda t: 0.87 * np.exp(-1.30 * t)
        curve = trend.live_curve(falling, clock, color=BLUE)
        dot = trend.dot(clock.get_value, lambda: falling(clock.get_value()), color=BLUE)
        self.play(FadeIn(plasma), FadeIn(trend), run_time=0.62)
        self.add(curve, dot)
        self.play(clock.animate.set_value(0.30), rate_func=linear, run_time=1.03)

        self.at("memory B cells held")
        chamber = RoundedRectangle(width=5.75, height=4.54, corner_radius=0.27,
                                   stroke_color=PURPLE, stroke_width=3, fill_color="#372D47",
                                   fill_opacity=1).move_to(point(3.21, -0.01))
        reserve = VGroup(*[memory_cell(x, y, r) for x, y, r in [
            (1.67, -0.95, 0.42), (2.96, -0.70, 0.43), (4.30, -0.86, 0.47),
            (4.78, 0.45, 0.40), (2.08, 0.57, 0.46)]])
        self.play(FadeIn(chamber), FadeIn(reserve, shift=UP * 0.27), run_time=0.82)
        self.play(FadeIn(label("Memory B cells", 3.21, 2.73, PURPLE, 36)),
                  clock.animate.set_value(0.48), run_time=1.05)
        swirl(reserve, radius=0.20, speed=1.65)

        self.at("can persist or even")
        additions = VGroup(memory_cell(3.34, 1.02), memory_cell(5.04, -1.41))
        self.play(clock.animate.set_value(0.69), run_time=1.55, rate_func=linear)
        self.play(clock.animate.set_value(1), LaggedStart(*(FadeIn(c, scale=0.45) for c in additions),
                                                          lag_ratio=0.5), run_time=2.50,
                  rate_func=linear)
        swirl(additions, radius=0.12)

        self.at("neither readout measures")
        lock_box = boxed_label("Protection", color=GOLD, size=33, pad=0.24, fill_opacity=0.17)
        lock_box.move_to(point(-1.72, -3.24))
        lock_body = RoundedRectangle(width=0.35, height=0.28, corner_radius=0.05,
                                     fill_color=GOLD, fill_opacity=0.95, stroke_width=0)
        lock_body.move_to(point(-3.38, -3.28))
        shackle = Arc(radius=0.12, start_angle=0, angle=PI, arc_center=point(-3.38, -3.17),
                      stroke_width=3, stroke_color=GOLD)
        lock = VGroup(lock_body, shackle)
        self.play(FadeIn(lock_box), FadeIn(lock, shift=DOWN * 0.12), run_time=0.70)
        self.at("needs its own endpoint")
        endpoint = label("Needs own endpoint", 1.72, -3.24, TEXT, 31)
        self.play(FadeIn(endpoint), run_time=0.68)
        self.at("like reinfection rates")
        self.play(swap(endpoint, label("Reinfection rates", 1.72, -3.24, TEXT, 31)), run_time=0.76)
        self.finish()


def bird(x, y, bursa):
    body = Ellipse(width=1.40, height=0.91, fill_color="#544336", fill_opacity=1,
                   stroke_color=GREY, stroke_width=2).move_to(point(x, y))
    head = Circle(radius=0.30, stroke_color=GREY, stroke_width=2, fill_color="#544336",
                  fill_opacity=1).move_to(point(x + 0.51, y + 0.56))
    beak = Polygon(point(x + 0.77, y + 0.63), point(x + 0.99, y + 0.49),
                   point(x + 0.76, y + 0.43), stroke_width=0, fill_color=GOLD, fill_opacity=1)
    tail = Polygon(point(x - 0.63, y + 0.12), point(x - 1.00, y + 0.48),
                   point(x - 0.50, y + 0.35), stroke_color=GREY, stroke_width=2,
                   fill_color="#544336", fill_opacity=1)
    eye = Dot(point(x + 0.59, y + 0.65), radius=0.039, color=TEXT)
    feet = VGroup(*[Line(point(x + dx, y - 0.43), point(x + dx + 0.06, y - 0.61),
                         color=GOLD, stroke_width=2) for dx in (-0.21, 0.19)])
    pouch = Ellipse(width=0.28, height=0.34, fill_color=PURPLE, fill_opacity=int(bursa),
                    stroke_width=2, stroke_opacity=int(bursa), stroke_color=PURPLE)
    pouch.move_to(point(x - 0.41, y - 0.14)).set_z_index(2)
    return VGroup(tail, feet, body, head, beak, eye), pouch


class S09UnlockedClumping(SpokenScene):
    def construct(self):
        panels = TwoPanel("Landsteiner 1901", "Glick, Chang & Jaap 1956", colors=(RED, PURPLE),
                          top=3.12, bottom=-2.73, width=12.86, size=30)
        panels.left_frame.set_fill("#222833", opacity=1)
        panels.right_frame.set_fill("#222833", opacity=1)
        self.add(sample_tag(), panels.left_frame)
        xs = (-4.24, -2.78, -1.31)
        tests = [(x, y, density) for y, pattern in [(0.75, (3, 0, 0)), (-0.85, (0, 3, 0))]
                 for x, density in zip(xs, pattern)]
        specimens = [clump_well(x, y, 1.31, 1.46, 0) for x, y, _ in tests]
        sera = VGroup(label("Serum\nB", -5.61, 0.78, TEAL, 28),
                      label("Serum\nA", -5.61, -0.82, BLUE, 28))
        self.at("clumping tests made")
        self.play(LaggedStart(*(FadeIn(p) for p, _ in specimens), lag_ratio=0.37),
                  run_time=2.42)

        self.at("in 1901")
        self.play(FadeIn(panels.left_head), run_time=0.52)
        self.play(FadeIn(sera), run_time=0.56)
        aliquots = VGroup(*[Dot(point(x, y + 0.57), radius=0.12, color=TEAL if y > 0 else BLUE)
                            for x, y, _ in tests])
        self.play(LaggedStart(*(FadeIn(d) for d in aliquots), lag_ratio=0.3), run_time=0.62)
        self.at("mixed serum and")
        self.play(LaggedStart(*(FadeOut(d, shift=DOWN * 0.47) for d in aliquots),
                              lag_ratio=0.37), run_time=0.94)
        self.play(LaggedStart(*(FadeIn(c, shift=UP * 0.19) for _, c in specimens),
                              lag_ratio=0.24), run_time=1.18)
        self.at("clumping sorted people")
        clusters = [(cells, clump_well(x, y, 1.31, 1.46, density)[1])
                    for (_, cells), (x, y, density) in zip(specimens, tests) if density]
        self.play(LaggedStart(*(Transform(c, packed) for c, packed in clusters),
                              lag_ratio=0.32), run_time=1.05)
        a = label("A", xs[0], -2.02, TEXT, 33)
        b = label("B", xs[1], -2.02, TEXT, 33)
        c = label("C", xs[2], -2.02, TEXT, 33)
        self.play(LaggedStart(FadeIn(a), FadeIn(b), FadeIn(c), lag_ratio=0.50), run_time=1.24)
        for _, cells in specimens:
            swirl(cells, radius=0.06, speed=1.6)
        self.at("now called O")
        self.play(swap(c, label("C (now O)", xs[2], -2.02, TEXT, 30)), run_time=0.73)

        self.at("in 1956")
        self.play(FadeIn(panels.right_frame), FadeIn(panels.right_head), run_time=0.84)
        intact, bursa = bird(2.02, 0.56, True)
        removed, _ = bird(4.90, 0.56, False)
        self.play(FadeIn(intact, shift=LEFT * 0.42), FadeIn(removed, shift=RIGHT * 0.42),
                  run_time=1.55)
        self.at("studied the bursa")
        self.play(FadeIn(bursa, scale=0.48), run_time=0.70)
        self.play(Indicate(bursa, color=PURPLE, scale_factor=1.5), run_time=0.84)
        self.play(VGroup(intact, bursa).animate.shift(DOWN * 0.22),
                  removed.animate.shift(DOWN * 0.22), run_time=0.88)

        self.at("immunized birds with")
        statuses = VGroup(label("Intact", 2.02, 1.85, TEXT, 32), label("Bursa removed", 4.90, 1.85, TEXT, 30))
        dose = VGroup(*[target(x, 1.47, 0.12) for x in (2.02, 4.90)])
        self.play(FadeIn(statuses), FadeIn(dose), run_time=0.56)
        self.play(dose.animate.shift(DOWN * 1.01).scale(1.8), run_time=0.88)
        self.play(FadeOut(dose, scale=0.35), run_time=0.53)

        self.at("clumping titers showed")
        p, clumped = clump_well(2.02, -1.31, 2.40, 1.67, 3)
        q, smooth = clump_well(4.90, -1.31, 2.40, 1.67, 0)
        self.play(FadeIn(p), FadeIn(q), run_time=0.57)
        dispersed = clump_well(2.02, -1.31, 2.40, 1.67, 0)[1]
        self.play(FadeIn(dispersed, shift=UP * 0.32), run_time=0.65)
        self.play(Transform(dispersed, clumped), run_time=1.63)
        self.at("made little or")
        self.play(FadeIn(smooth, shift=UP * 0.26), run_time=0.83)
        swirl(smooth, radius=0.085, speed=1.9)
        self.finish()


def storage(x, y, w, h, tint):
    return RoundedRectangle(width=w, height=h, corner_radius=0.22, stroke_color=GREY,
                            stroke_width=2, fill_color=tint, fill_opacity=1).move_to(point(x, y))


def hormone_pulse(t):
    """Schematic trace at Walker et al.'s reported mean rate (0.89 pulses/h)."""
    return 0.13 + 0.70 * ((1 - np.cos(TAU * 0.89 * t)) / 2) ** 2


def advancing_area(plot, fn, time, color):
    """Shade the region between the same computed trace and its time axis."""
    def region():
        start = plot.xr[0]
        end = max(start + 0.0001, time.get_value())
        samples = np.linspace(start, end, max(2, int((end - start) * 45)))
        points = [plot.pt(t, fn(t)) for t in samples]
        return Polygon(plot.pt(start, 0), *points, plot.pt(end, 0), stroke_width=0,
                       fill_color=color, fill_opacity=1)

    return always_redraw(region)


class S10UnlockedHormone(SpokenScene):
    def construct(self):
        study = label("Walker et al. 2012", -3.75, 3.26, TEXT, 35)
        plot = Plot(box=(-5.63, 5.99, -1.67, 0.61), xr=(0, 3.5), yr=(0, 1),
                    xlabel="Time", ylabel="Corticosterone", label_size=30)
        h_panel = storage(0, -0.39, 12.57, 3.76, "#222E38")
        self.add(h_panel, plot, sample_tag())
        self.at("Walker and colleagues")
        self.play(FadeIn(study), run_time=0.70)
        self.at("the hourly pulses")
        preview_time = ValueTracker(0)
        preview_area = advancing_area(plot, hormone_pulse, preview_time, "#354F45")
        initial = plot.live_curve(hormone_pulse, preview_time, color=GREEN)
        self.add(preview_area, initial)
        self.play(preview_time.animate.set_value(3.5), run_time=3.55, rate_func=linear)

        self.at("a natural guess")
        header = label("Guess: CRH burst → pulse", -3.00, 2.77, TEAL, 34)
        input_panel = storage(0, 1.83, 12.57, 1.08, "#253E49")
        input_plot = Plot(box=(-5.63, 5.99, 1.42, 2.13), xr=(0, 3.5), yr=(0, 1))
        burst = lambda t: 0.14 + 0.72 * ((1 - np.cos(TAU * 0.89 * (t + 0.11))) / 2) ** 4
        guess_time = ValueTracker(0)
        guess_area = advancing_area(input_plot, burst, guess_time, "#377481")
        guess = input_plot.live_curve(burst, guess_time, color=TEAL, width=5)
        self.play(FadeIn(header), FadeIn(input_panel), run_time=0.64)
        self.at("follows a burst")
        self.add(guess_area, guess)
        self.play(guess_time.animate.set_value(3.5), run_time=3.05, rate_func=linear)

        self.at("they dripped in")
        rejected = VGroup(Line(point(-1.65, 1.48), point(1.65, 2.20), color=RED, stroke_width=5),
                          Line(point(-1.65, 2.20), point(1.65, 1.48), color=RED, stroke_width=5))
        self.play(Create(rejected), run_time=0.46)
        self.play(FadeOut(rejected), FadeOut(guess), FadeOut(guess_area), FadeOut(initial),
                  FadeOut(preview_area), FadeOut(header), run_time=0.5)
        steady = input_plot.curve(lambda t: 0.51, color=TEAL, width=5)
        self.at("a low steady")
        self.play(Create(steady), run_time=1.05)
        infusion = label("CRH infusion (0.5 µg/h)", -3.22, 2.77, TEAL, 32)
        self.play(FadeIn(infusion), run_time=0.61)

        self.at("measuring corticosterone")
        row = VGroup(*[plate(1.03, 0.61, x, -2.72, fill=DEVELOPED)
                       for x in np.linspace(-5.62, 2.33, 8)])
        continuation = label("…", 3.37, -2.72, TEXT, 34)
        cadence = label("Samples every 5 min", -3.81, -3.44, TEXT, 29)
        self.play(LaggedStart(*(FadeIn(w, shift=DOWN * 0.13) for w in row), lag_ratio=0.27),
                  run_time=2.38)
        self.at("by immunoassay")
        self.play(FadeIn(cadence), FadeIn(continuation), run_time=0.50)
        clock = ValueTracker(0)
        waveform = plot.live_curve(hormone_pulse, clock, color=GREEN)
        spot = plot.dot(clock.get_value, lambda: hormone_pulse(clock.get_value()), color=GREEN)
        waveform_area = advancing_area(plot, hormone_pulse, clock, "#354F45")
        self.add(waveform_area, waveform, spot)
        self.play(clock.animate.set_value(0.61), run_time=1.17, rate_func=linear)

        self.at("it still pulsed")
        mean = label("Mean 0.89 pulses/h", 3.66, 0.95, GREEN, 31)
        self.play(FadeIn(mean), clock.animate.set_value(3.5), run_time=3.04, rate_func=linear)

        self.at("a pituitary adrenal")
        self.play(FadeOut(row), FadeOut(cadence), FadeOut(continuation), FadeOut(h_panel),
                  FadeOut(plot), FadeOut(waveform_area), FadeOut(waveform), FadeOut(spot),
                  FadeOut(mean), run_time=0.49)
        pituitary = boxed_label("Pituitary", color=BLUE, size=38, pad=0.32).move_to(point(-3.21, -0.42))
        adrenal = boxed_label("Adrenal", color=BLUE, size=38, pad=0.32).move_to(point(3.21, -0.42))
        outward = CurvedArrow(point(-2.51, 0.21), point(2.51, 0.21), angle=-0.57,
                              color=BLUE, stroke_width=4.6)
        back = CurvedArrow(point(2.51, -1.05), point(-2.51, -1.05), angle=-0.63,
                           color=GREEN, stroke_width=4.6)
        self.play(FadeIn(pituitary), FadeIn(adrenal), run_time=0.48)
        self.play(Create(outward), Create(back), run_time=0.79)
        self.at("make its own rhythm")
        self.play(FadeIn(caption("Loop makes its own rhythm", size=35)), run_time=0.59)
        self.finish()


class S11End(EndCard):
    LINE = "Antibodies bind one target, turning invisible molecules into measurable signals."
