"""Light microscopy: a carried bench and camera view, timed to the recorded narration.

COLOR MAP: blue = optics and glass, grey = specimen structure, purple = motors,
yellow = motion or measured separation, green = fluorescence and controls,
red = degraded response, orange = treatments, teal = camera, gold = dates and prompts.
"""
from bp_parts import *
from scipy.special import j1

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
WAVELENGTH = 520
NM = 0.0065
OIL_NA, OTHER_NA = 1.40, 1.00
OIL_LIMIT = 0.61 * WAVELENGTH / OIL_NA
OTHER_LIMIT = 0.61 * WAVELENGTH / OTHER_NA
BENCH, CAM = -3.37, 3.37
STAGE, LIP, IMAGE_Y = -1.43, 1.02, -0.05
QUESTION = "Smaller, same, or wider?"
QUESTION_STYLE = {"y": 0.30, "max_w": 5.0, "size": 34}
CAM_RGB = np.array([18, 31, 43])
AIRY_RGB = np.array([170, 249, 139])


def p(x, y):
    return np.array([x, y, 0.0])


def block(width, height, x, y, fill, stroke=None, corner=0.12, opacity=1):
    return RoundedRectangle(
        width=width, height=height, corner_radius=corner, fill_color=fill,
        fill_opacity=opacity, stroke_color=stroke or fill, stroke_width=2 if stroke else 0,
    ).move_to(p(x, y))


def label(text, x=CAM, y=-2.29, size=30, color=TEXT):
    return T(text, size, color).move_to(p(x, y))


def glass():
    return VGroup(
        block(4.78, 0.36, BENCH, STAGE - 0.27, "#294D64", BLUE),
        Line(p(BENCH - 2.22, STAGE - 0.14), p(BENCH + 2.22, STAGE - 0.14),
             stroke_width=3, color="#AFDDE9"),
    )


def objective(na):
    wide = na == OIL_NA
    aperture = 1.40 if wide else 0.94
    body = Polygon(
        p(BENCH - 1.43, 2.37), p(BENCH + 1.43, 2.37),
        p(BENCH + 1.48, 1.55), p(BENCH + aperture, LIP),
        p(BENCH - aperture, LIP), p(BENCH - 1.48, 1.55),
        fill_color="#315B78" if wide else "#3B526D", fill_opacity=1,
        color=BLUE, stroke_width=3,
    )
    return VGroup(
        body, block(2.99, 0.29, BENCH, 2.24, "#44728D", BLUE),
        Ellipse(width=2 * aperture, height=0.32, fill_color="#78C9DA", fill_opacity=0.90,
                color=BLUE, stroke_width=2).move_to(p(BENCH, LIP)),
    )


def cone_half_width(na):
    # Cone angles are schematic, since the immersion refractive index is unspecified.
    return 0.60 + 0.76 * (na - OTHER_NA) / (OIL_NA - OTHER_NA)


def cone(na, animated=True):
    half = cone_half_width(na)
    tip = p(BENCH, STAGE + 0.09)
    top = LIP - 0.1
    edges = VGroup(
        Polygon(tip, p(BENCH - half, top), p(BENCH + half, top),
                fill_color="#426E37", fill_opacity=0.75, stroke_width=0),
        *[Line(tip, p(BENCH + side * half, top), color=GREEN, stroke_width=2.7)
          for side in (-1, 1)],
    )
    rays = VGroup(*[Line(tip, p(BENCH + f * half, top), color=GREEN, stroke_width=1.8)
                    .set_opacity(0.32) for f in (-0.77, -0.38, 0, 0.38, 0.77)])
    # Fronts travel from the emitting specimen toward the lens while the cone stays fixed.
    fronts = VGroup(*[Line(LEFT, RIGHT, color="#C8FDAE", stroke_width=11) for _ in range(3)])
    phase = 0.0

    def advance(group, dt):
        nonlocal phase
        phase += dt * 0.56
        for index, front in enumerate(group):
            frac = (phase + index / len(group) + 0.14) % 1
            y = interpolate(tip[1], top, frac)
            front.put_start_and_end_on(p(BENCH - frac * half, y), p(BENCH + frac * half, y))
            front.set_stroke(width=6 + 10 * frac, opacity=0.78 * np.sin(np.pi * frac))
        edges[0].set_fill(opacity=0.68 + 0.20 * np.sin(TAU * phase))

    advance(fronts, 0)
    if animated:
        fronts.add_updater(advance)
    return VGroup(edges, rays, fronts)


def bench_world(na=OIL_NA, rays=True):
    panel = TwoPanel("Microscope bench", "Camera view", colors=(BLUE, TEAL),
                     top=3.2, bottom=-2.75, width=13.15, gap=0.42, size=32)
    fields = VGroup(
        block(6.28, 5.77, BENCH, 0.225, "#253A4E"),
        block(6.28, 5.77, CAM, 0.225, "#121F2B"),
    )
    lens = objective(na)
    light = cone(na)
    cover = glass()
    frame = Group(fields, panel, cover)
    group = Group(frame, light, lens) if rays else Group(frame, lens)
    return group, light, lens


def scope():
    return scope_tag("Schematic", size=28, color=TEXT)


def bench_points(spacing, count=2):
    offsets = (0,) if count == 1 else (-spacing / 2, spacing / 2)
    return VGroup(*[
        VGroup(Dot(p(BENCH + dx, STAGE + 0.10), radius=0.19, color=GREEN).set_opacity(0.23),
               Dot(p(BENCH + dx, STAGE + 0.10), radius=0.078, color="#D6FFC5"))
        for dx in offsets
    ])


# Ideal circular-aperture PSF: [2 J1(u)/u]², with u = 3.831706 r / r_first_min.
# Add intensities for mutually incoherent emitters, then apply a display gamma to reveal dim rings.
VIEW_W, VIEW_H = 5.98, 3.78
X, Y = np.meshgrid(np.linspace(-VIEW_W / 2, VIEW_W / 2, 270),
                   np.linspace(VIEW_H / 2, -VIEW_H / 2, 171))
RADIAL = np.linspace(0, 55, 8193)
AIRY = np.ones_like(RADIAL)
AIRY[1:] = (2 * j1(RADIAL[1:]) / RADIAL[1:]) ** 2


def diffraction_pixels(radius, centers, distortion, brightness):
    intensity = np.zeros_like(X)
    for center, weight in centers:
        dx = X - center
        xx = dx / (1 + 0.56 * distortion)
        yy = (Y + distortion * (0.18 - 0.22 * dx)) / (1 + 0.24 * distortion)
        rad = np.hypot(xx, yy) * 3.83170597 / max(radius, 0.04)
        ideal = np.interp(rad, RADIAL, AIRY)
        # Illustrative asymmetric ghost contribution, not a measured instrument PSF.
        ghost = np.exp(-(((dx - 0.81) / 1.25) ** 2 + ((Y + 0.38) / 0.56) ** 2))
        intensity += weight * (ideal + 0.13 * distortion * ghost)
    light = (intensity * brightness / (0.45 + intensity * brightness)) ** 0.65
    rgb = (CAM_RGB + light[:, :, None] * (AIRY_RGB - CAM_RGB)).astype(np.uint8)
    return np.dstack((rgb, np.full_like(rgb[:, :, 0], 255)))


def camera_airy(radius, centers, distortion=lambda: 0.0, moving=True):
    def pixels(brightness):
        return diffraction_pixels(radius(), centers(), distortion(), brightness)

    image = ImageMobject(pixels(1)).set_width(VIEW_W).move_to(p(CAM, IMAGE_Y))
    if moving:
        elapsed = 0.0

        def refresh(mob, dt):
            nonlocal elapsed
            elapsed += dt
            # Mild exposure shimmer lets a held diffraction pattern retain its geometry.
            mob.pixel_array[:, :, :3] = pixels(1 + 0.18 * np.sin(3.4 * elapsed))[:, :, :3]

        image.add_updater(refresh)
    return image


def pair(separation):
    return ((-separation / 2, 1), (separation / 2, 1))


def gap_bar(x, width, y=-1.44, color=YELLOW):
    left, right = x - width / 2, x + width / 2
    return VGroup(
        Line(p(left, y), p(right, y), color=color, stroke_width=3.5),
        *[Line(p(end, y - 0.09), p(end, y + 0.09), color=color, stroke_width=3.5)
          for end in (left, right)],
    )


def pixel_grid():
    step = 100 * NM
    return VGroup(
        *[Line(p(CAM + j * step, IMAGE_Y - 1.82), p(CAM + j * step, IMAGE_Y + 1.82),
               color=BLUE, stroke_width=1.5, stroke_opacity=0.37) for j in range(-4, 5)],
        *[Line(p(CAM - 2.86, IMAGE_Y + j * step), p(CAM + 2.86, IMAGE_Y + j * step),
               color=BLUE, stroke_width=1.5, stroke_opacity=0.37) for j in range(-2, 3)],
    )


def point_scene(na=OIL_NA):
    world, light, lens = bench_world(na)
    return world, light, lens, bench_points(0.78)


def na_label(na):
    return label(f"NA {na:.2f}", BENCH + 1.90, -0.76, 34, BLUE)


def emission_label():
    return label("λ = 520 nm", BENCH, -2.31, 32, GREEN)


def predict_picture_label():
    return question_card(QUESTION, **QUESTION_STYLE).shift(RIGHT * (CAM + 0.5))


def predict_mask():
    return block(6.03, 4.63, CAM, -0.04, "#223544")


def predict_backdrop():
    world, _, _, points = point_scene(OTHER_NA)
    return Group(world, points, emission_label(), na_label(OTHER_NA), predict_mask(), scope())


class S01Hook(SpokenScene):
    def construct(self):
        world, _, _ = bench_world()
        distance = ValueTracker(2.9)
        radius = OIL_LIMIT * NM
        points = always_redraw(lambda: bench_points(0.52 * distance.get_value()))
        image = camera_airy(lambda: radius, lambda: pair(distance.get_value()))
        question = question_card("When do two points blur into one?", size=31, y=-3.25)
        self.add(world, points, image, scope())
        self.at("how close")
        mark = bob(label("?", CAM, 2.0, 45, GOLD), amp=0.07, speed=3)
        self.play(FadeIn(question), FadeIn(mark), run_time=0.30)
        self.play(distance.animate.set_value(0.38), run_time=3.2)
        self.at("inside cells")
        self.play(distance.animate.set_value(2.55), run_time=3.5)
        self.at("tiny motors step")
        self.play(distance.animate.set_value(1.7), run_time=2.1)
        self.at("light microscopy lets")
        self.play(distance.animate.set_value(0.38), run_time=3.8)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Light Microscopy"
    TITLE = "Seeing Tiny Motion at the Limit of Light"

    def construct(self):
        world, _, _ = bench_world()
        radius = OIL_LIMIT * NM
        self.add(world, bench_points(0.52 * 0.38), scope(),
                 camera_airy(lambda: radius, lambda: pair(0.38)))
        name = fit_text(self.TITLE, max_w=11.7, size=46, font=TITLE_FONT, max_lines=2)
        name.move_to(p(0, 0.08))
        title_panel = block(12.4, 1.96, 0, 0.14, "#1B2A3A", BLUE)
        lesson = label(self.LESSON, 0, 0.79, 28, BLUE)
        rule = Line(p(-1.0, -0.49), p(1.0, -0.49), color=GOLD, stroke_width=3)
        self.add(title_panel)
        self.play(FadeIn(Group(lesson, name, rule)), run_time=0.46)
        self.wait(1.54)


class S03AiryRayleigh(SpokenScene):
    def construct(self):
        world, _, _ = bench_world()
        limit = OIL_LIMIT * NM
        radius, spacing, second = ValueTracker(0.18), ValueTracker(2.8), ValueTracker(0)
        def centers():
            d = spacing.get_value() / 2
            x = interpolate(0, -d, second.get_value())
            return ((x, 1), (d, second.get_value()))

        image = camera_airy(radius.get_value, centers)
        point = bench_points(0, 1)
        self.add(world, point, image, scope())
        self.at("a lens")
        self.play(radius.animate.set_value(limit), run_time=4.4)
        self.at("bright center with rings")
        ring = Circle(radius=limit, color=GREEN, stroke_width=2.3).move_to(p(CAM, IMAGE_Y))
        ring.set_stroke(opacity=0.8)
        self.play(Create(ring), run_time=0.8)
        self.at("airy pattern")
        airy = label("Airy pattern", color=GREEN)
        self.play(FadeIn(airy), run_time=0.46)
        self.at("under the rayleigh")
        criterion = label("Rayleigh criterion", color=GOLD)
        self.play(swap(airy, criterion), FadeOut(ring), run_time=0.63)
        self.at("two points resolve")
        self.play(second.animate.set_value(1), FadeIn(bench_points(0.78)),
                  FadeOut(point), run_time=1.1)
        self.at("one center falls")
        self.play(spacing.animate.set_value(limit), run_time=1.7)
        self.at("first dark ring")
        ring.move_to(p(CAM - limit / 2, IMAGE_Y))
        centre = Dot(p(CAM + limit / 2, IMAGE_Y), radius=0.054, color=YELLOW)
        self.play(Create(ring), FadeIn(centre), run_time=0.65)
        self.at("that smallest separation")
        self.play(Create(gap_bar(CAM, limit)), swap(criterion, label("Resolution", color=YELLOW)),
                  run_time=0.8)
        self.finish()


class S04WavelengthNa(SpokenScene):
    def construct(self):
        world, _, _, points = point_scene()
        distance = OIL_LIMIT * NM
        image = camera_airy(lambda: distance, lambda: pair(distance))
        resolution = label("Resolution", color=YELLOW)
        mark = gap_bar(CAM, distance)
        self.add(world, points, image, mark, resolution, scope())
        self.at("emission wavelength")
        wave = label("Emission wavelength  λ", BENCH, -2.29, 30, GREEN)
        self.play(FadeIn(wave), run_time=0.65)
        wavefront = Line(p(BENCH - 0.28, -0.85), p(BENCH + 0.28, -0.85),
                         stroke_width=10, color="#E4FFD7")
        self.play(FadeIn(wavefront), run_time=0.24)
        self.play(wavefront.animate.put_start_and_end_on(p(BENCH - 1.22, 0.82), p(BENCH + 1.22, 0.82)),
                  run_time=2.2, rate_func=linear)
        self.play(FadeOut(wavefront), run_time=0.24)
        self.at("numerical aperture")
        aperture = label("Numerical\naperture", BENCH + 1.90, -0.70, 30, BLUE)
        self.play(FadeIn(aperture), run_time=0.75)
        self.at("describes the cone")
        outline = VGroup(*[Line(p(BENCH, STAGE + 0.09),
                                p(BENCH + side * cone_half_width(OIL_NA), LIP - 0.10),
                                color="#B6F29B", stroke_width=5) for side in (-1, 1)])
        self.play(ShowPassingFlash(outline, time_width=0.5), run_time=2.0)
        self.at("ideal setup")
        grid = pixel_grid().set_z_index(2)
        self.play(FadeOut(mark), FadeIn(grid), run_time=1.0)
        self.at("green label emits")
        self.play(swap(wave, emission_label()), run_time=1.0)
        self.at("oil objective")
        self.play(swap(aperture, na_label(OIL_NA)), run_time=0.85)
        self.at("resolves 227")
        self.play(FadeIn(mark.set_z_index(3)),
                  swap(resolution, label("227 nm", color=YELLOW)), run_time=0.65)
        self.play(FadeIn(label("100 nm per pixel", CAM, 2.03, 28, TEXT).set_z_index(3)), run_time=0.5)
        self.finish()


class S05PredictQuestion(SpokenScene):
    def construct(self):
        world, light, lens, points = point_scene()
        d = OIL_LIMIT * NM
        image = camera_airy(lambda: d, lambda: pair(d))
        grid = pixel_grid().set_z_index(2)
        result = VGroup(label("227 nm", color=YELLOW), gap_bar(CAM, d),
                        label("100 nm per pixel", CAM, 2.03, 28)).set_z_index(3)
        wide = na_label(OIL_NA)
        self.add(world, points, image, grid, result, wide, emission_label(), scope())
        self.at("swap objectives")
        new_lens = objective(OTHER_NA)
        screen = predict_mask()
        self.play(FadeIn(screen), FadeOut(result), FadeOut(grid), FadeOut(wide), run_time=0.48)
        self.remove(image)
        light.clear_updaters(recursive=True)
        self.play(FadeOut(lens, shift=LEFT * 0.68), FadeOut(light), run_time=0.52)
        self.play(FadeIn(new_lens, shift=RIGHT * 0.70), run_time=1.15)
        self.at("drop na")
        narrow_light = cone(OTHER_NA)
        new_lens.set_z_index(1)
        aperture = ValueTracker(1.94)
        source = p(CAM, -1.30)

        def comparison_cone():
            half = aperture.get_value()
            return Polygon(source, p(CAM - half, 1.34), p(CAM + half, 1.34),
                           fill_color="#527D41", fill_opacity=1, stroke_color=GREEN, stroke_width=3)

        profile = always_redraw(comparison_cone)
        self.play(FadeIn(narrow_light), FadeIn(na_label(OTHER_NA)),
                  FadeIn(profile), run_time=0.66)
        self.play(aperture.animate.set_value(0.86), run_time=1.65)
        self.at("losing 0")
        change = label("−0.40 NA", CAM, -2.05, 35, BLUE)
        former = VGroup(
            *[DashedLine(source, p(CAM + side * 1.94, 1.34), color=BLUE, stroke_width=4)
              for side in (-1, 1)],
            DashedLine(p(CAM - 1.94, 1.34), p(CAM + 1.94, 1.34), color=BLUE, stroke_width=4),
        )
        self.play(FadeIn(change), Create(former), run_time=1.6)
        self.at("collects a narrower")
        front = Line(p(CAM - 0.15, -0.84), p(CAM + 0.15, -0.84),
                     color="#CAFDB5", stroke_width=15)
        self.play(FadeIn(front), run_time=0.22)
        self.play(front.animate.put_start_and_end_on(p(CAM - 0.82, 1.23), p(CAM + 0.82, 1.23)),
                  run_time=1.8, rate_func=linear)
        self.play(FadeOut(front), run_time=0.24)
        self.at("will the smallest")
        self.play(FadeOut(change), FadeOut(profile), FadeOut(former), FadeOut(screen), run_time=0.55)
        self.play(GrowFromCenter(predict_mask()), run_time=1.65)
        self.play(FadeIn(predict_picture_label()), run_time=0.48)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    RING_AT = (CAM, -0.83, 0)
    SECONDS = 4.5

    def backdrop(self):
        return predict_backdrop()

    def construct(self):
        self.add(self.backdrop(), predict_picture_label())
        ring, advance = countdown(self.SECONDS, center=self.RING_AT, radius=0.77)
        remaining = advance.mobject
        sweep = always_redraw(lambda: Sector(
            radius=0.73, arc_center=np.array(self.RING_AT), start_angle=PI / 2,
            angle=max(0.001, TAU * remaining.get_value()), color=GOLD,
            fill_opacity=0.64, stroke_width=0,
        ))
        self.add(sweep, ring)
        self.play(advance)


class S07PredictAnswer(SpokenScene):
    def construct(self):
        base = predict_backdrop()
        mask = base[4]
        q = predict_picture_label()
        radius = ValueTracker(OIL_LIMIT * NM)
        d = ValueTracker(radius.get_value())
        image = camera_airy(radius.get_value, lambda: pair(d.get_value()))
        self.add(*base[:4], image, mask, q, base[5])
        self.at("it grows wider")
        self.play(FadeOut(q), FadeOut(mask, shift=UP * 0.33), run_time=0.7)
        self.play(radius.animate.set_value(OTHER_LIMIT * NM), run_time=1.5)
        self.at("a narrower cone")
        # The ghost outline is the former wide cone, drawn around the current narrower cone.
        wide = VGroup(*[DashedLine(p(BENCH, STAGE + 0.09),
                                   p(BENCH + side * cone_half_width(OIL_NA), LIP - 0.10),
                                   color=BLUE, stroke_width=3, dash_length=0.12)
                        for side in (-1, 1)])
        old_na = label("NA 1.40", BENCH - 1.91, -0.31, 28, BLUE)
        self.play(Create(wide), FadeIn(old_na), d.animate.set_value(OTHER_LIMIT * NM),
                  run_time=2.7)
        self.at("pushing resolution")
        self.play(FadeOut(wide), FadeOut(old_na),
                  Create(gap_bar(CAM, OTHER_LIMIT * NM)), run_time=0.75)
        self.at("317 .2")
        self.play(FadeIn(label(f"{OTHER_LIMIT:.1f} nm", color=YELLOW)), run_time=0.68)
        self.at("subtract 227")
        equation = caption(f"{OTHER_LIMIT:.1f} nm − {OIL_LIMIT:.0f} nm",
                           size=32, color=TEXT, y=-3.28)
        expression = VGroup(equation, T(f"≈ {OTHER_LIMIT - round(OIL_LIMIT):.0f} nm lost", 32, YELLOW))
        expression.arrange(RIGHT, buff=0.28).move_to(p(-0.55, -3.25))
        self.play(FadeIn(expression[0]), run_time=0.7)
        self.at("about 90")
        self.play(FadeIn(expression[1]), run_time=0.8)
        self.finish()


def cilium_cross_section():
    center = p(CAM, 0)
    rim = Circle(radius=1.72, stroke_color=GREY, stroke_width=3,
                 fill_color="#26303B", fill_opacity=1).move_to(center)
    sections, arms = VGroup(), VGroup()
    for n in range(9):
        theta = n * TAU / 9
        radial = np.array([np.cos(theta), np.sin(theta), 0.0])
        tangent = np.array([-np.sin(theta), np.cos(theta), 0.0])
        a = center + 1.19 * radial
        b = a + 0.26 * tangent
        sections.add(Circle(radius=0.17, color=TEXT, stroke_width=2.4).move_to(a),
                     Circle(radius=0.13, color=GREY, stroke_width=2.1).move_to(b))
        if n != 1:
            arms.add(Line(a + 0.14 * radial, a + 0.14 * radial - 0.24 * tangent,
                          color="#B7BCC6", stroke_width=5))
    centre_pair = VGroup(*[Circle(radius=0.15, color=TEXT, stroke_width=2.2)
                           .move_to(center + dx * RIGHT) for dx in (-0.19, 0.19)])
    missing = Circle(radius=0.18, color=RED, stroke_width=3).move_to(p(CAM + 1.24, 0.73))
    return VGroup(rim, sections, arms, centre_pair), missing


class S08Limits(SpokenScene):
    def construct(self):
        world, _, _, _ = point_scene(OTHER_NA)
        width = OTHER_LIMIT * NM
        second, warp = ValueTracker(1), ValueTracker(0)
        image = camera_airy(lambda: width, lambda: ((-width / 2 * second.get_value(), 1),
                            (width / 2, second.get_value())), warp.get_value)
        ideal = label("Ideal values", color=YELLOW)
        self.add(world, bench_points(0, 1), image, ideal, scope())
        self.at("these are ideal")
        self.play(second.animate.set_value(0), run_time=2.2)
        self.at("real response to")
        psf = label("Point-spread function", color=GREEN)
        self.play(swap(ideal, psf), run_time=1.0)
        self.at("can be worse")
        sample = block(2.9, 0.62, BENCH, STAGE + 0.23, "#405970", GREY, opacity=0.86)
        self.play(FadeIn(sample, shift=RIGHT * 0.67), warp.animate.set_value(1), run_time=3.25)
        self.at("suspected missing motor")
        section, missing = cilium_cross_section()
        self.play(FadeOut(image), FadeOut(psf), run_time=0.45)
        self.play(FadeIn(section), run_time=0.40)
        self.play(Create(missing), run_time=0.48)
        self.play(section.animate.scale(1.12),
                  missing.animate.shift(p(1.24 * 0.12, 0.73 * 0.12)), run_time=1.25)
        self.at("confirmed by electron")
        self.play(FadeIn(label("Electron microscopy", color=TEXT)), run_time=0.65)
        pulse(missing, base=3.5, amp=1.6, speed=3)
        self.finish()


def motor_stalk(x, y, height):
    tail = block(0.32, 0.16, x, y + 0.08, PURPLE, corner=0.05)
    stalk = Line(p(x, y + 0.12), p(x + 0.14, y + height), color=PURPLE, stroke_width=5)
    head = Ellipse(width=0.34, height=0.19, color=PURPLE, fill_color=PURPLE,
                   fill_opacity=1, stroke_width=0).move_to(stalk.get_end())
    return VGroup(tail, stalk, head)


def filament(x, y, length):
    return VGroup(
        Line(p(x - length / 2, y), p(x + length / 2, y), color=GREEN,
             stroke_width=15, stroke_opacity=0.29),
        Line(p(x - length / 2, y), p(x + length / 2, y), color="#BCF9A8", stroke_width=5),
        *[Dot(p(x + length * f, y), radius=0.046, color="#E4FFD7") for f in (-0.36, -0.08, 0.19, 0.36)],
    )


class S09Controls(SpokenScene):
    def construct(self):
        world, _, _ = bench_world(OTHER_NA)
        small_motors = VGroup(*[motor_stalk(BENCH + x, STAGE, 0.43) for x in (-1.0, 0, 1.0)])
        small_filament = filament(BENCH, STAGE + 0.48, 2.8)
        floor = block(5.40, 0.30, CAM, -1.32, "#294D64", BLUE)
        rear_floor = Polygon(p(CAM - 2.70, -1.17), p(CAM + 2.70, -1.17),
                             p(CAM + 2.30, -0.37), p(CAM - 2.30, -0.37),
                             color=BLUE, stroke_width=2, fill_color="#36566C", fill_opacity=1)
        motors = VGroup(*[motor_stalk(CAM + x, -1.17, 1.51) for x in (-2.0, -1, 0, 1, 2)])
        back_motors = VGroup(*[motor_stalk(CAM + x, -0.37, 1.52) for x in (-1.75, -0.75, 0.25, 1.25)])
        streaks = VGroup(filament(CAM - 0.91, 0.47, 2.46), filament(CAM - 1.23, 1.25, 1.91))
        self.add(world, scope(), rear_floor, back_motors, floor)
        self.at("seeing motion")
        back_motors.set_opacity(0)
        self.play(FadeIn(small_motors), FadeIn(motors, shift=UP * 0.45),
                  back_motors.animate.set_opacity(1), run_time=2.5)
        self.at("in a gliding assay")
        assay = label("Gliding assay", CAM, 2.04, 31, TEXT)
        self.play(FadeIn(assay), run_time=0.55)
        self.play(GrowFromEdge(small_filament, LEFT), run_time=0.68)
        self.at("motors stick by")
        tails = VGroup(*[Dot(p(CAM + x, -1.09), radius=0.105, color=PURPLE)
                         for x in (-2.0, -1, 0, 1, 2)])
        self.play(LaggedStart(*[Indicate(tail, color=TEXT, scale_factor=1.6) for tail in tails],
                              lag_ratio=0.23), run_time=1.65)
        self.at("under fluorescent filaments")
        self.play(LaggedStart(*[GrowFromEdge(f, LEFT) for f in streaks], lag_ratio=0.26), run_time=1.85)
        self.at("without a tp")
        no_atp = label("No ATP", color=GREEN)
        self.play(FadeIn(no_atp), run_time=0.52)
        head_highlights = VGroup(*[Circle(radius=0.13, color=GREEN, stroke_width=4)
                                  .move_to(p(CAM + x + 0.14, 0.34)) for x in (-2, -1, 0)])
        self.play(LaggedStart(*[ShowPassingFlash(h, time_width=0.75) for h in head_highlights],
                              lag_ratio=0.46), run_time=1.42)
        self.at("add a tp")
        with_atp = label("ATP added", color=ORANGE)
        self.play(swap(no_atp, with_atp), run_time=0.63)
        self.at("and filaments move")
        self.play(streaks.animate.shift(RIGHT * 1.15),
                  small_filament.animate.shift(RIGHT * 0.29), run_time=2.12, rate_func=linear)
        self.at("and purified systems")
        self.play(swap(with_atp, label("Purified vs. cell", color=TEXT)),
                  streaks.animate.shift(RIGHT * 0.34), run_time=0.83, rate_func=linear)
        self.play(streaks.animate.shift(RIGHT * 0.65),
                  small_filament.animate.shift(RIGHT * 0.32), run_time=4.0, rate_func=linear)
        self.finish()


def tubule(x0, x1, y, thickness=0.32, color=GREEN):
    body = block(x1 - x0, thickness, (x0 + x1) / 2, y, "#476C4E", color,
                 corner=min(thickness / 2.2, (x1 - x0) / 4))
    seam = Line(p(x0 + 0.10, y), p(x1 - 0.10, y), color="#C0F5B1", stroke_width=2)
    return VGroup(body, seam)


class S10UnlockedMicrotubules(SpokenScene):
    def construct(self):
        world, _, _ = bench_world(OTHER_NA)
        starts = (-2.02, -2.39, -1.62, -2.22, -1.62)
        ends = (1.08, 1.73, 2.34, 1.05, 2.19)
        population = VGroup(*[tubule(CAM + a, CAM + b, y, 0.27)
                              for a, b, y in zip(starts, ends, (1.43, 0.73, 0.03, -0.67, -1.37))])
        bench_sample = VGroup(*[filament(BENCH + i * 0.55, STAGE + 0.16 + 0.16 * (i % 2),
                                        1 + 0.20 * (i % 3)) for i in range(-2, 3)])
        self.add(world, scope())
        self.at("light microscopy then")
        self.play(FadeIn(bench_sample), LaggedStart(*[GrowFromCenter(t) for t in population],
                                                   lag_ratio=0.29), run_time=3.35)
        self.at("in 1984")
        historical = label("Mitchison and Kirschner, 1984", CAM, 2.13, 28, GOLD)
        self.play(FadeIn(historical), run_time=0.7)
        self.at("inferred dynamic")
        inferred = label("Inferred from populations", color=TEXT)
        self.play(FadeIn(inferred), run_time=0.65)
        self.at("ends switching between")
        altered = VGroup(*[tubule(CAM + a + da, CAM + b + db, y, 0.27)
                            for a, b, da, db, y in zip(starts, ends, (0.5, 0.1, -0.63, 0.43, -0.4),
                                                       (-0.3, 0.64, 0.28, -0.68, 0.33),
                                                       (1.43, 0.73, 0.03, -0.67, -1.37))])
        self.play(Transform(population, altered), run_time=3.85)
        self.at("microscopy of single ends")
        left, right = ValueTracker(-1.54), ValueTracker(1.35)
        single = always_redraw(lambda: tubule(CAM + left.get_value(), CAM + right.get_value(), 0.08, 0.62))
        direct = label("Switching seen directly", color=TEXT)
        self.play(FadeOut(population), FadeOut(historical), run_time=0.52)
        self.play(FadeIn(single), swap(inferred, direct), run_time=0.63)
        self.at("showed switching directly")
        self.play(left.animate.set_value(-2.52), right.animate.set_value(2.48),
                  run_time=1.65, rate_func=linear)
        self.at("both ends")
        self.play(left.animate.set_value(-1.01), right.animate.set_value(1.03),
                  run_time=1.28, rate_func=linear)
        self.play(left.animate.set_value(-1.72), right.animate.set_value(1.95),
                  run_time=1.12, rate_func=linear)
        self.finish()


def doublet(y, x0=-1.65, x1=1.65):
    return VGroup(
        *[Line(p(CAM + x0, y + dy), p(CAM + x1, y + dy), stroke_width=15,
               color=GREEN, stroke_opacity=0.35) for dy in (-0.105, 0.105)],
        *[Line(p(CAM + x0, y + dy), p(CAM + x1, y + dy), stroke_width=6.0,
               color="#C8F9B9") for dy in (-0.105, 0.105)],
    )


class S11UnlockedCilia(SpokenScene):
    def construct(self):
        world, _, _ = bench_world(OTHER_NA)
        positions = (1.11, 0.41, -0.29, -0.99)
        rows = VGroup(*[doublet(y) for y in positions])
        links = VGroup(*[Line(p(CAM + x, y - 0.14), p(CAM + x, y - 0.55),
                              color=PURPLE, stroke_width=7)
                         for y in positions[:-1] for x in (-0.92, -0.37, 0.37, 0.92)])
        bench_bundle = VGroup(*[filament(BENCH, STAGE + 0.10 + 0.10 * i, 2.70)
                                for i in range(3)])
        field = block(6.03, 5.04, CAM, -0.02, "#080A0D")
        name = label("Summers and Gibbons", CAM, 2.19, 29, GOLD)
        self.add(world, field, scope())
        self.at("summers and gibbons")
        self.play(FadeIn(bench_bundle), FadeIn(name),
                  LaggedStart(*[Create(row) for row in rows], lag_ratio=0.22), run_time=3.45)
        self.at("bundles of paired")
        self.play(FadeIn(links), run_time=0.75)
        self.at("called doublets")
        pairs = label("Microtubule doublets", color=GREEN)
        group_brace = gap_bar(CAM, 3.3, y=-1.56, color=GREEN)
        self.play(FadeIn(pairs), Create(group_brace), run_time=0.62)
        self.at("did the motor")
        prompt = label("Slide or shorten?", color=GOLD)
        self.play(swap(pairs, prompt), FadeOut(group_brace), run_time=0.75)
        self.at("slide doublets")
        possible_slide = Arrow(p(CAM - 1.48, -1.62), p(CAM + 1.63, -1.62),
                               buff=0, color=YELLOW, stroke_width=7)
        self.play(GrowArrow(possible_slide), Indicate(rows[1], color=YELLOW, scale_factor=1),
                  run_time=1.05)
        self.at("or shorten microtubules")
        arrows_in = VGroup(*[Arrow(p(CAM + side * 1.63, -1.62), p(CAM + side * 0.17, -1.62),
                                   buff=0, color=YELLOW, stroke_width=7) for side in (-1, 1)])
        self.play(FadeOut(possible_slide), run_time=0.24)
        self.play(*[GrowArrow(arrow) for arrow in arrows_in], run_time=1.16)
        self.at("briefly treated axonemes")
        trypsin = label("Trypsin", color=ORANGE)
        self.play(swap(prompt, trypsin), FadeOut(arrows_in), run_time=0.7)
        treatment = VGroup(*[Dot(link.get_center(), radius=0.11, color=ORANGE) for link in links])
        self.play(LaggedStart(*[FadeIn(dot, scale=0.35) for dot in treatment], lag_ratio=0.18),
                  run_time=2.68)
        self.at("breaking structures")
        self.play(LaggedStart(*[AnimationGroup(FadeOut(link, scale=0.25), FadeOut(dot, scale=1.45))
                                for link, dot in zip(links, treatment)], lag_ratio=0.19),
                  run_time=3.6)
        self.at("adding 0 .1")
        atp = label("0.1 mM ATP", color=ORANGE)
        added_atp = VGroup(*[Dot(p(CAM + side * (2.52 - 0.12 * (i % 2)), y), radius=0.20,
                                  color=ORANGE)
                            for side in (-1, 1) for i, y in enumerate((1.16, 0.48, -0.22, -0.92))])
        self.play(swap(trypsin, atp),
                  LaggedStart(*[FadeIn(dot, scale=0.40) for dot in added_atp], lag_ratio=0.19),
                  run_time=1.35)
        self.play(*[dot.animate.shift((0.43 if i < 4 else -0.43) * RIGHT)
                    for i, dot in enumerate(added_atp)], run_time=1.55, rate_func=linear)
        self.at("doublets sliding out")
        self.play(*[row.animate.shift(dx * RIGHT) for row, dx in zip(rows, (-1.30, -0.47, 0.49, 1.29))],
                  FadeOut(added_atp), run_time=3.0, rate_func=smooth)
        self.at("answer sliding")
        self.play(swap(atp, label("Doublets slide", color=YELLOW)), run_time=0.58)
        self.finish()


STEP = 0.80
TRACK_Y = -0.92


def motor_track():
    track = tubule(CAM - 2.78, CAM + 2.78, TRACK_Y, 0.55)
    marks = VGroup(*[Line(p(CAM + i * STEP, TRACK_Y - 0.22), p(CAM + i * STEP, TRACK_Y + 0.27),
                           color="#D1F7C6", stroke_width=2.4) for i in range(-3, 4)])
    return VGroup(track, marks)


def walking_motor(head_a, head_b, swing_a, swing_b, dye=True):
    a = p(CAM + head_a, TRACK_Y + 0.36 + swing_a)
    b = p(CAM + head_b, TRACK_Y + 0.36 + swing_b)
    cargo = p(CAM + (head_a + head_b) / 2, 1.17)
    joint = p(cargo[0], 0.36)
    limbs = VGroup(Line(a, joint, color=PURPLE, stroke_width=8),
                   Line(b, joint, color=PURPLE, stroke_width=8),
                   Line(joint, cargo, color=PURPLE, stroke_width=8))
    cargo_body = block(0.93, 0.66, cargo[0], cargo[1], "#684D88", PURPLE, corner=0.20)
    heads = VGroup(*[block(0.38, 0.27, pos[0], pos[1], PURPLE, corner=0.10) for pos in (a, b)])
    group = VGroup(limbs, cargo_body, heads)
    if dye:
        group.add(Dot(a, radius=0.135, color=GREEN).set_opacity(0.49),
                  Dot(a, radius=0.067, color="#E0FFD4"))
    return group


class S12UnlockedMotors(SpokenScene):
    def construct(self):
        world, _, _ = bench_world(OTHER_NA)
        step_a, step_b = ValueTracker(-1), ValueTracker(0)
        track = motor_track()
        small_track = filament(BENCH, STAGE + 0.11, 3.43)
        motor = always_redraw(lambda: walking_motor(
            2 * step_a.get_value() * STEP, (-1 + 2 * step_b.get_value()) * STEP,
            0.94 * abs(np.sin(PI * step_a.get_value())), 0.94 * np.sin(PI * step_b.get_value()),
        ))
        self.add(world, scope(), small_track, track)
        self.at("tracking one dye")
        self.play(FadeIn(motor, shift=UP * 0.24), run_time=0.95)
        head_glow = Circle(radius=0.23, color=GREEN, stroke_width=5).move_to(p(CAM - 2 * STEP, TRACK_Y + 0.36))
        self.play(Create(head_glow), run_time=0.75)
        self.play(FadeOut(head_glow), run_time=0.56)
        self.at("walks hand over")
        name = label("Kinesin-1", CAM, 2.09, 31, PURPLE)
        self.play(FadeIn(name), step_a.animate.set_value(0), run_time=2.25)
        self.at("sites 8 nanometers")
        spacing = VGroup(gap_bar(CAM - STEP / 2, STEP, y=-1.66),
                         label("8 nm between sites", color=YELLOW))
        self.play(Create(spacing[0]), FadeIn(spacing[1]), run_time=0.72)
        ticks = VGroup(*[Circle(radius=0.15, color=YELLOW, stroke_width=4)
                         .move_to(p(CAM + x, TRACK_Y)) for x in (-STEP, 0)])
        self.play(LaggedStart(*[Indicate(tick, color=YELLOW) for tick in ticks],
                              lag_ratio=0.50), run_time=1.35)
        self.remove(*ticks, ticks)
        self.at("its cargo moves")
        cargo_gap = gap_bar(CAM, STEP, y=1.72)
        cargo_step = label("Cargo step: 8 nm", color=YELLOW)
        self.play(FadeOut(spacing[0]), swap(spacing[1], cargo_step),
                  Create(cargo_gap), step_b.animate.set_value(1), run_time=2.18)
        self.at("rear head swings")
        self.play(FadeOut(cargo_gap), step_a.animate.set_value(1), run_time=2.7)
        self.at("two times eight")
        head_gap = gap_bar(CAM + STEP, 2 * STEP, y=-1.66)
        equation = label("2 × 8 = 16 nm", color=YELLOW)
        self.play(swap(cargo_step, equation), Create(head_gap), run_time=0.76)
        self.at("2004 imaging study")
        study = label("2004 imaging study", CAM, 2.09, 30, GOLD)
        self.play(swap(name, study), FadeOut(head_gap), FadeOut(equation), run_time=0.8)
        # The study's measured displacement is shown as an optical readout.
        measured = 17 / 8 * STEP
        dye_x = ValueTracker(-measured / 2)
        dye = camera_airy(lambda: 0.85, lambda: ((dye_x.get_value(), 1),))
        self.play(FadeOut(motor), FadeOut(track), FadeIn(dye), run_time=1.35)
        self.at("dye on one head")
        start = Circle(radius=0.19, color=GREEN, stroke_width=2.7).move_to(p(CAM - measured / 2, IMAGE_Y))
        self.play(FadeIn(start), dye_x.animate.set_value(measured / 2), run_time=1.05)
        self.at("about 17")
        self.play(Create(gap_bar(CAM, measured, y=-0.72)),
                  FadeIn(label("≈ 17 nm measured", color=YELLOW)), run_time=0.72)
        self.finish()


class S13End(EndCard):
    LINE = "Wavelength and numerical aperture set resolution; controls test what you see."
