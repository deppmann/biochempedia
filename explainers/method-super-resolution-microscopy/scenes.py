"""Super-resolution microscopy, timed to the supplied narration.

Blue: microscope and camera. Grey: membranes and image field. Green: fluorescence
and localized emitters. Purple: violet activation, depletion and patterned light.
Yellow: measured distances and localization. Gold: dates and prediction.
Red: image limits. Teal and orange: ordered and disordered probes, respectively.
"""
from bp_parts import *
from scipy.special import j1

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
FIELD = "#364654"
MEMBRANE = "#526576"
CENTER = np.array([-2.65, 0.1, 0])
VESICLE_CENTER = CENTER + DOWN * 0.52
VESICLE_RADII = np.array([2.15, 1.72])
PROTEINS = (CENTER + [-0.22, 0.46, 0], CENTER + [0.22, 0.46, 0])
QUESTION = "Can the microscope separate them?"
CARD = dict(y=-3.05, size=36)
WAVELENGTH = 520
RAYLEIGH = 0.61 * WAVELENGTH
HIGH_NA = 1.4
LOW_NA = 1.0
MAX_PIXEL_ZOOM = 1.85
PHOTOACTIVATION_SITES = np.array([
    [-1.52, -0.08], [1.49, -0.06], [-0.18, 1.39], [-0.70, -1.29], [0.86, 1.24],
    [-1.28, 0.84], [0.42, -1.45], [1.62, 0.62], [-1.56, -0.76], [1.35, -1.04],
    [-0.94, 1.25], [0.18, 1.53], [-1.07, -1.12], [1.10, -1.28], [-0.07, -1.55],
    [0.24, 0.54], [-0.27, 0.54], [0.50, 1.49], [-1.61, 0.39], [1.49, -0.66],
    [-1.20, -1.05], [-0.54, 1.42], [0.68, -1.42], [1.19, 0.98],
])


def p(x, y):
    return np.array([x, y, 0])


def membrane_site(direction):
    radial = direction / VESICLE_RADII
    return VESICLE_CENTER + p(*(direction / np.linalg.norm(radial)))


def side(text, y=0, color=TEXT, size=34):
    return fit_text(text, max_w=5.55, size=size, min_size=28, color=color, weight=BOLD).move_to(p(3.62, y))


def microscope_field(center=CENTER, radius=2.54):
    return Circle(radius=radius, color=GREY, stroke_width=2, fill_color=FIELD,
                  fill_opacity=1).move_to(center)


def vesicle():
    body = Ellipse(width=2 * VESICLE_RADII[0], height=2 * VESICLE_RADII[1], color=GREY, stroke_width=3,
                   fill_color=MEMBRANE, fill_opacity=1).move_to(VESICLE_CENTER)
    inner = body.copy().scale(0.93).set_fill(opacity=0).set_stroke(GREY, 1.1, opacity=0.55)
    return VGroup(body, inner)


def breathe_exposure(field, membrane=None):
    """Keep the specimen fixed while the live field gains and loses illumination."""
    clock = 0.0
    dark = ManimColor("#293945")
    lit = ManimColor("#4A5C6B")
    dark_membrane = ManimColor("#405365")
    lit_membrane = ManimColor("#697C8C")

    def update(image, dt):
        nonlocal clock
        clock += dt
        fraction = 0.5 + 0.5 * np.sin(1.74 * clock)
        image.set_fill(interpolate_color(dark, lit, fraction))
        if membrane is not None:
            membrane[0].set_fill(interpolate_color(dark_membrane, lit_membrane, fraction))

    field.add_updater(update)


def objective():
    body = RoundedRectangle(width=2.44, height=0.60, corner_radius=0.15, color=BLUE,
                            fill_color="#254352", fill_opacity=1, stroke_width=3)
    glass = ArcBetweenPoints(p(-0.78, -0.20), p(0.78, -0.20), angle=0.42)
    glass.set_stroke(BLUE, width=5)
    return VGroup(body, glass).move_to(CENTER + UP * 1.83)


def light_cone(na, center=p(3.62, 1.55)):
    # The angle is illustrative. At fixed n, NA is proportional to sin(half-angle).
    width = 1.6 * np.tan(np.arcsin(na / 1.52))
    width /= np.tan(np.arcsin(HIGH_NA / 1.52))
    tip = center + DOWN * 0.73
    left, right = center + p(-width, 0.73), center + p(width, 0.73)
    cone = Polygon(left, right, tip, color=GREEN, stroke_width=2,
                   fill_color=GREEN, fill_opacity=0.23)
    lens = ArcBetweenPoints(left, right, angle=0.24).set_stroke(BLUE, 5)
    return VGroup(cone, lens)


def signal_image(intensity, location, width, color=GREEN):
    """Render a computed intensity field as an alpha mask over the microscope view."""
    rgba = np.empty((*intensity.shape, 4), dtype=np.uint8)
    rgba[:, :, :3] = ManimColor(color).to_int_rgb()
    rgba[:, :, 3] = np.rint(255 * np.clip(intensity, 0, 1))
    return ImageMobject(rgba).set_width(width).move_to(location)


def sample_grid(radius, samples=161):
    axis = np.linspace(-radius, radius, samples)
    return np.meshgrid(axis, -axis)


def gaussian_blurs(centers, sigma, extent, color=GREEN, location=CENTER):
    x, y = sample_grid(extent)
    intensity = sum(np.exp(-((x - px) ** 2 + (y - py) ** 2) / (2 * sigma ** 2))
                    for px, py in centers)
    taper = np.clip((extent - np.hypot(x, y)) / (extent * 0.13), 0, 1)
    return signal_image((1 - np.exp(-1.6 * intensity)) * taper, location, 2 * extent, color)


def merged_smudge():
    return gaussian_blurs([(-0.22, 0.46), (0.22, 0.46)], 0.67, 2.32)


def airy(displacement=0, both=False):
    """Incoherent Airy intensities add. Gamma lifts faint rings for projection."""
    x, y = sample_grid(2.46, 241)
    first_minimum = 0.91

    def pattern(cx):
        z = 3.83170597 * np.hypot(x - cx, y) / first_minimum
        amplitude = np.divide(2 * j1(z), z, out=np.ones_like(z), where=z != 0)
        return amplitude ** 2

    intensity = pattern(-first_minimum / 2)
    if both:
        intensity += pattern(-first_minimum / 2 + displacement)
    taper = np.clip((2.46 - np.hypot(x, y)) / 0.29, 0, 1)
    return signal_image(np.minimum(intensity, 1) ** 0.48 * taper, CENTER, 4.92)


def crosshair(center, radius=0.24):
    return VGroup(*[
        Line(center + direction * radius * 0.56, center + direction * radius,
             color=YELLOW, stroke_width=2.5)
        for direction in (LEFT, RIGHT, UP, DOWN)
    ])


def measure(length, center, color=YELLOW):
    left = center + LEFT * length / 2
    right = center + RIGHT * length / 2
    return VGroup(Line(left, right, color=color, stroke_width=4),
                  *[Line(q + DOWN * 0.095, q + UP * 0.095, color=color, stroke_width=3)
                    for q in (left, right)])


def distance_bar(na):
    return measure(4.3 / na, p(3.62, -1.03))


def optical_readings(na):
    return VGroup(side("520 nm", 2.89, GREEN), side(f"NA {na:.2f}", 0.36, BLUE),
                  side(f"{RAYLEIGH / na:.1f} nm", -1.62, YELLOW))


def prediction_picture():
    field = microscope_field()
    membrane = vesicle()
    spots = VGroup(*[Dot(pos, radius=0.085, color=GREEN) for pos in PROTEINS])
    spacing = measure(0.44, CENTER + UP * 0.82)
    gap = side("50 nm apart", -0.92, YELLOW)
    cone = light_cone(HIGH_NA)
    lights = VGroup(*optical_readings(HIGH_NA)[:2])
    return VGroup(field, membrane, spots, spacing, gap, cone, lights,
                  scope_tag(size=26, color=TEXT))


def prediction_progress(fraction=0):
    """A quiet timer in the free space below the optical readings."""
    track = RoundedRectangle(width=5.04, height=0.26, corner_radius=0.10,
                             color=GREY, stroke_width=1.4, fill_color=FIELD,
                             fill_opacity=1).move_to(p(3.62, -2.07))
    length = 4.92 * max(fraction, 0.001)
    fill = Rectangle(width=length, height=0.19, stroke_width=0,
                     fill_color=GOLD, fill_opacity=1)
    fill.move_to(p(3.62 - 4.92 / 2 + length / 2, -2.07))
    return VGroup(track, fill)


def green_dot(location, radius=0.067):
    return Dot(location, radius=radius, color=GREEN)


def localized_map():
    return VGroup(*[green_dot(membrane_site(q)) for q in PHOTOACTIVATION_SITES])


def activation_glow(location, sigma, color=GREEN):
    offset = (location - CENTER)[:2]
    return gaussian_blurs([offset], sigma, 2.52, color)


def target_ring(radius=1.02, center=CENTER):
    return Circle(radius=radius, color=YELLOW, stroke_width=3).move_to(center)


def pixel_image(centers, tiles=14):
    x, y = sample_grid(1.0, tiles)
    brightness = sum(np.exp(-((x - a) ** 2 + (y - b) ** 2) / (2 * 0.32 ** 2))
                     for a, b in centers)
    # Broadcast one computed colour per sensor pixel, with the grid baked in.
    level = 0.9 * (1 - np.exp(-brightness))
    base = np.array(ManimColor(FIELD).to_int_rgb())
    signal = np.array(ManimColor(GREEN).to_int_rgb())
    rgb = np.uint8(base + level[:, :, None] * (signal - base))
    pitch = 12
    grid = np.repeat(np.repeat(rgb, pitch, axis=0), pitch, axis=1)
    grid[::pitch] = base
    grid[:, ::pitch] = base
    return ImageMobject(grid).set_width(1.89)


def camera_zoom():
    box = Square(side_length=1.91, color=BLUE, stroke_width=2.5)
    return Group(pixel_image([(-0.10, 0), (0.10, 0)]), box).move_to(CENTER)



def shimmer(mob, amount=0.16, speed=2.8):
    """Vary the emission, keeping emitter coordinates and specimen geometry fixed."""
    clock = 0.0

    def update(image, dt):
        nonlocal clock
        clock += dt
        image.set_opacity(1 - amount * (0.5 - 0.5 * np.cos(speed * clock)))

    mob.add_updater(update)
    return mob


def sim_exposures():
    """Noise-free 1-D SIM example under a hard frequency cutoff.

    Phase-stepped striping shifts neighboring frequency bands into the passband.
    Demodulate the three phases and move the recovered bands back before inversion.
    The picture repeats the stripes in y because this example reconstructs one direction.
    """
    n = 161
    axis = np.arange(n) / n
    specimen = sum(np.exp(-((axis - x) / 0.025) ** 2 / 2) for x in (0.405, 0.595))
    cutoff, stripe = 3, 3
    band = np.arange(-cutoff, cutoff + 1)
    phases = 2 * np.pi * np.arange(3) / 3
    lighting = 1 + np.cos(2 * np.pi * stripe * axis[None, :] + phases[:, None])
    exposures = np.fft.fft(lighting * specimen, axis=1)[:, band]
    recovered = np.zeros(n, dtype=complex)
    for shift in (-1, 0, 1):
        coefficient = np.mean(exposures * np.exp(-1j * shift * phases[:, None]), axis=0)
        recovered[band - shift * stripe] = coefficient * (2 if shift else 1)
    widefield = np.zeros(n, dtype=complex)
    widefield[band] = np.fft.fft(specimen)[band]
    return np.fft.ifft(widefield).real, np.fft.ifft(recovered).real


def sim_image(profile):
    x, y = sample_grid(1.0)
    taper = np.clip((1 - np.hypot(x, y)) / 0.17, 0, 1)
    intensity = np.maximum(profile, 0)[None, :] * np.exp(-7 * y ** 2) * taper
    return signal_image(intensity, CENTER, 4.85)


def stripes():
    x, y = sample_grid(1.0)
    taper = np.clip((1 - np.hypot(x, y)) / 0.12, 0, 1)
    return signal_image((0.52 + 0.42 * np.cos(3 * np.pi * x)) * taper, CENTER, 4.59, PURPLE)


RECEPTORS = [(-0.39, 0.04), (-0.12, 0.24), (0.12, 0.06), (0.39, -0.14),
             (-0.25, -0.25), (0.11, -0.29), (0.37, 0.23)]
ORDERED = [(-0.67, 0.15), (-0.49, 0.45), (-0.08, 0.53), (0.35, 0.57), (0.58, 0.21),
           (0.61, -0.32), (0.29, -0.53), (-0.16, -0.54), (-0.52, -0.40)]
DISORDERED = [(-1.28, -0.14), (-1.01, 0.80), (-0.25, 1.22), (0.79, 1.0), (1.28, 0.30),
              (1.19, -0.63), (0.50, -1.09), (-0.73, -1.01)]


def probe_marks(offsets, center, scale, color, radius, angle=0):
    marks = VGroup(*[Dot(center + p(*offset) * scale, radius=radius * scale, color=color)
                     for offset in offsets])
    return marks.rotate(angle, about_point=center)


def cell_field(center, radius=1.74, angle=0):
    scale = radius / 1.74
    field = microscope_field(center, radius)
    receptor = probe_marks(RECEPTORS, center, scale, PURPLE, 0.104, angle)
    ordered = probe_marks(ORDERED, center, scale, TEAL, 0.077, angle)
    disordered = probe_marks(DISORDERED, center, scale, ORANGE, 0.077, angle)
    return VGroup(field, receptor, ordered, disordered)


def preparations():
    return [cell_field(p(x, -0.06), angle=a) for x, a in
            [(-4.35, 0.24), (0, -0.25), (4.35, 0.45)]]


def preparation_labels():
    return VGroup(*[T(name, 31, TEXT, weight=BOLD).move_to(p(x, 2.21))
                    for x, name in zip((-4.35, 0, 4.35),
                                       ("Live CH27", "Fixed CH27", "Fixed primary B cells"))])


class S01Hook(SpokenScene):
    def construct(self):
        field, membrane, spots, spacing, gap, _, _, scope = prediction_picture()
        self.add(field, membrane, spots, scope)
        breathe_exposure(field, membrane)
        self.at("50 nanometers")
        self.play(GrowFromCenter(spacing), FadeIn(gap), run_time=0.7)
        lens = objective()
        self.at("Through a standard lens")
        self.play(FadeIn(lens, shift=UP * 0.42), FadeOut(spacing), FadeOut(gap), run_time=1.1)
        self.at("each glowing label")
        individual = [gaussian_blurs([(0, 0)], 0.38, 1.32, location=pos) for pos in PROTEINS]
        self.play(*[FadeIn(blur, scale=0.17) for blur in individual], FadeOut(spots), run_time=2.0)
        self.at("both blurs merge")
        merged = merged_smudge()
        self.play(*[FadeOut(blur) for blur in individual], FadeIn(merged, scale=0.72), run_time=1.15)
        shimmer(merged)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Seeing Past Light's Blur"
    LESSON = "Super-resolution microscopy"

    def construct(self):
        # The title interlude leaves the microscope image and its smudge in place.
        merged = merged_smudge()
        self.add(microscope_field(), vesicle(), objective(), merged, scope_tag(size=26, color=TEXT))
        shimmer(merged, amount=0.24)
        title = fit_text(self.TITLE.replace("Past ", "Past\n"), max_w=5.55, size=52, min_size=44,
                         font=TITLE_FONT).move_to(p(3.62, 0.18))
        lesson = side(self.LESSON, -1.38, BLUE, 28)
        self.play(FadeIn(title), FadeIn(lesson), run_time=0.37)
        self.wait(1.27)
        self.play(FadeOut(title), FadeOut(lesson), run_time=0.36)


class S03Diffraction(SpokenScene):
    def construct(self):
        merged = merged_smudge()
        membrane, lens = vesicle(), objective()
        field = microscope_field()
        self.add(field, membrane, lens, merged, scope_tag(size=26, color=TEXT))
        breathe_exposure(field)
        first = airy()
        self.at("Each glowing point")
        self.play(FadeOut(membrane), FadeOut(lens), FadeOut(merged), FadeIn(first, scale=0.75),
                  run_time=1.42)
        self.at("bright center")
        airy_label = side("Airy pattern", 0.28, GREEN)
        self.play(FadeIn(airy_label), run_time=0.5)
        ring = DashedVMobject(target_ring(0.91, CENTER + LEFT * 0.455), num_dashes=32)
        self.play(Create(ring), run_time=1.25)
        self.at("Two spots resolve")
        gap = ValueTracker(0.18)
        pair = always_redraw(lambda: airy(gap.get_value(), both=True))
        right_center = always_redraw(lambda: crosshair(CENTER + RIGHT * (gap.get_value() - 0.455)))
        self.remove(first)
        self.add(pair, right_center)
        self.play(gap.animate.set_value(0.91), run_time=3.58)
        self.at("Emission wavelength")
        self.play(FadeOut(airy_label), run_time=0.35)
        cone = light_cone(0.78)
        self.at("the lens's light cone")
        self.play(FadeIn(cone, scale=0.65), run_time=0.74)
        criterion = side("Rayleigh distance", -0.5)
        bracket = measure(0.91, CENTER + DOWN * 1.03)
        self.at("that Rayleigh distance")
        self.play(Create(bracket), FadeIn(criterion), run_time=1.1)
        wavelength, na, result = optical_readings(1)
        self.at("520 nanometer")
        self.play(FadeIn(wavelength), run_time=0.53)
        self.at("numerical aperture 1")
        self.play(Transform(cone, light_cone(1)), FadeIn(na), run_time=1.15)
        self.at("317 .2")
        self.play(GrowFromCenter(distance_bar(1)), FadeIn(result), run_time=1.44)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        field, membrane, spots, spacing, separation, _, labels, scope = prediction_picture()
        pattern = airy(0.91, both=True)
        ring = DashedVMobject(target_ring(0.91, CENTER + LEFT * 0.455), num_dashes=32)
        center = crosshair(CENTER + RIGHT * 0.455)
        bracket = measure(0.91, CENTER + DOWN * 1.03)
        criterion = side("Rayleigh distance", -0.5)
        na = ValueTracker(HIGH_NA)
        live_na = counter("NA {:.2f}", na, p(3.62, 0.36), size=31, color=BLUE, mono=False)
        cone = always_redraw(lambda: light_cone(na.get_value()))
        rayleigh_bar = always_redraw(lambda: distance_bar(na.get_value()))
        wave, aperture = labels
        self.add(field, pattern, ring, center, bracket, cone, rayleigh_bar, wave, live_na, criterion, scope)
        breathe_exposure(field)
        self.at("Losing")
        self.play(na.animate.set_value(LOW_NA), run_time=3.25)
        rayleigh_bar.clear_updaters()
        change = side("About 90 nm wider", -2.29, YELLOW, 29)
        self.at("about 90 nanometers")
        self.play(FadeIn(change), run_time=0.58)
        self.at("Predict two")
        field.clear_updaters()
        self.play(field.animate.set_fill(FIELD), FadeOut(pattern), FadeOut(ring), FadeOut(center), FadeOut(bracket),
                  FadeOut(rayleigh_bar), FadeOut(criterion), FadeOut(change),
                  FadeIn(membrane), run_time=0.67)
        breathe_exposure(field, membrane)
        sample = side("GFP-tagged proteins", -1.62, GREEN, 30)
        self.at("GFP")
        self.play(FadeIn(spots, scale=0.65), FadeIn(sample), run_time=0.70)
        self.at("50 nanometers apart")
        self.play(GrowFromCenter(spacing), FadeIn(separation), run_time=0.68)
        self.at("With numerical aperture")
        self.play(na.animate.set_value(HIGH_NA), FadeOut(sample), run_time=1.68)
        cone.clear_updaters()
        self.remove(live_na)
        self.add(aperture)
        self.at("can a standard microscope")
        self.play(FadeIn(question_card(QUESTION, **CARD)), FadeIn(prediction_progress()),
                  run_time=0.63)
        self.wait(1.1)
        field.clear_updaters()
        self.play(field.animate.set_fill(FIELD), membrane[0].animate.set_fill(MEMBRANE),
                  run_time=0.31)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = QUESTION
    CARD = CARD
    SECONDS = 4.5

    def construct(self):
        # The prediction frame holds at its original scale while its time bar fills.
        progress = ValueTracker(0)
        timer = always_redraw(lambda: prediction_progress(progress.get_value()))
        self.add(prediction_picture(), question_card(self.QUESTION, **self.CARD), timer)
        self.play(progress.animate.set_value(1), run_time=self.SECONDS, rate_func=linear)


class S06GuidingIdea(SpokenScene):
    def construct(self):
        field, membrane, spots, spacing, separation, cone, light, scope = prediction_picture()
        question = question_card(QUESTION, **CARD)
        timer = prediction_progress(1)
        self.add(field, membrane, spots, spacing, separation, cone, light, scope, question, timer)
        breathe_exposure(field, membrane)
        self.at("Now")
        self.play(FadeOut(question), FadeOut(cone), FadeOut(light), FadeOut(separation),
                  FadeOut(timer), run_time=0.65)
        answer = side("One smudge", 2.79, RED)
        a = side("317.2 nm", 1.42, YELLOW)
        self.at("317 .2")
        self.play(Write(a), run_time=0.9)
        self.at("about 90 leaves")
        minus = side("− about 90 nm", 0.61, YELLOW)
        self.play(Write(minus), run_time=0.88)
        merged = gaussian_blurs([(-0.22, 0.46), (0.22, 0.46)], 0.62, 2.32)
        self.at("230 nanometers")
        result = side("≈ 230 nm", -0.27, YELLOW)
        self.play(Write(result), FadeOut(spots), FadeOut(spacing), FadeIn(merged, scale=0.45),
                  run_time=1.5)
        self.play(FadeIn(answer), run_time=0.42)
        self.at("That limit is")
        comparison = VGroup(measure(3.85, p(3.62, -1.08)),
                            measure(3.85 * 50 / 230, p(3.62, -1.78), GREEN),
                            side("50 nm", -2.30, GREEN, 29))
        self.play(LaggedStart(*[GrowFromCenter(mob) for mob in comparison], lag_ratio=0.23), run_time=1.98)
        self.at("Zooming only enlarges")
        zoom = camera_zoom()
        self.play(FadeOut(merged), FadeOut(membrane), FadeIn(zoom, scale=0.55), FadeOut(a), FadeOut(minus),
                  FadeOut(result), FadeOut(comparison), FadeOut(answer), run_time=1.28)
        first_zoom = 1.66
        self.play(zoom.animate.scale(first_zoom), run_time=1.31)
        self.at("Magnification without resolution")
        empty = side("Empty magnification", 0.08, RED)
        self.play(FadeIn(empty), run_time=0.6)
        self.play(zoom.animate.scale(MAX_PIXEL_ZOOM / first_zoom), run_time=2.1)
        self.at("Super resolution changes")
        self.play(FadeOut(zoom), FadeOut(empty), FadeIn(membrane), run_time=0.75)
        self.at("controlling when and where")
        switching = side("One at a time", 0.14, GREEN)
        first, second = [gaussian_blurs([(0, 0)], 0.45, 1.28, location=q) for q in PROTEINS]
        self.play(FadeIn(first, scale=0.60), FadeIn(switching), run_time=0.75)
        self.play(FadeOut(first), run_time=0.63)
        self.play(FadeIn(second, scale=0.60), run_time=0.75)
        self.at("blurs separate")
        self.play(FadeOut(second), run_time=0.63)
        self.finish()


class S07PalmStorm(SpokenScene):
    def construct(self):
        field, membrane = microscope_field(), vesicle()
        self.add(field, membrane, scope_tag(size=26, color=TEXT))
        breathe_exposure(field, membrane)
        dark_sites = localized_map().set_color("#43655E").set_opacity(0.68)
        self.at("In 2002")
        self.play(LaggedStart(*[FadeIn(mob) for mob in dark_sites], lag_ratio=0.11), run_time=2.75)
        credit = side("2002 · Photoactivatable GFP", 1.15, GOLD)
        person = side("George Patterson", 0.24, TEXT, 29)
        lab = side("Lippincott-Schwartz lab", -0.43, TEXT, 28)
        self.at("photoactivatable GFP")
        self.play(FadeIn(credit), FadeIn(person), run_time=0.6)
        self.at("in Jennifer")
        self.play(FadeIn(lab), run_time=0.7)
        first_site = membrane_site(PHOTOACTIVATION_SITES[0])
        dark_focus = crosshair(first_site, 0.27)
        self.at("It starts dark")
        self.play(Create(dark_focus), run_time=0.7)
        violet = activation_glow(first_site, 0.46, PURPLE)
        one = activation_glow(first_site, 0.30)
        self.at("violet light")
        self.play(FadeIn(violet), FadeOut(dark_focus), run_time=0.38)
        self.play(FadeOut(violet), FadeIn(one), run_time=0.55)
        self.at("In 2006")
        self.play(FadeOut(VGroup(credit, person, lab)), run_time=0.38)
        shimmer(one, amount=0.32)
        year = side("2006", 2.16, GOLD, 36)
        self.play(FadeIn(year), run_time=0.45)
        palm = side("PALM", 1.22, GREEN)
        storm = side("STORM", 0.35, GREEN)
        fpalm = side("FPALM", -0.52, GREEN)
        self.at("published Palm")
        self.play(FadeIn(palm), run_time=0.55)
        self.at("Zhuang's Storm")
        self.play(FadeIn(storm), run_time=0.5)
        self.at("F -Palm")
        self.play(FadeIn(fpalm), run_time=0.5)
        self.at("Switch on a sparse few")
        one.clear_updaters()
        self.play(FadeOut(year), FadeOut(palm), FadeOut(storm), FadeOut(fpalm),
                  FadeOut(one), run_time=0.42)
        batch = [membrane_site(q) for q in PHOTOACTIVATION_SITES[:3]]
        sources = [activation_glow(q, 0.33) for q in batch]
        self.play(LaggedStart(*[FadeIn(spot) for spot in sources], lag_ratio=0.36),
                  run_time=1.54)
        for glow in sources:
            shimmer(glow)
        sparse = side("Sparse activation", 0.48, GREEN)
        self.play(FadeIn(sparse), run_time=0.56)
        self.at("Locate each center")
        hairs = VGroup(*[crosshair(q) for q in batch])
        located = side("Locate each center", 0.48, YELLOW)
        self.play(LaggedStart(*[Create(mob) for mob in hairs], lag_ratio=0.25),
                  swap(sparse, located), run_time=1.06)
        self.at("then let them bleach")
        for glow in sources:
            glow.clear_updaters()
        centers = localized_map()
        bleach = side("Bleach the active spots", 0.48, TEXT)
        self.play(*[FadeOut(glow) for glow in sources], swap(located, bleach), run_time=1.32)
        self.play(FadeOut(hairs), LaggedStart(*[FadeIn(mob) for mob in centers[:3]], lag_ratio=0.2),
                  run_time=0.72)
        self.at("Repeat thousands of times")
        self.play(FadeOut(dark_sites), FadeOut(bleach), run_time=0.33)
        for first, last in ((3, 6), (6, 10), (10, 14), (14, 17), (17, 21), (21, 24)):
            flash = VGroup(*[green_dot(membrane_site(q), radius=0.19).set_opacity(0.7)
                             for q in PHOTOACTIVATION_SITES[first:last]])
            self.play(FadeIn(flash, scale=0.8), run_time=0.12)
            self.play(FadeOut(flash), FadeIn(centers[first:last]), run_time=0.21)
        self.finish()


class S08Math(SpokenScene):
    def construct(self):
        membrane, sites = vesicle(), localized_map()
        self.add(microscope_field(), membrane, sites, scope_tag(size=26, color=TEXT))
        blur = gaussian_blurs([(0, 0)], 1.02, 2.42)
        self.at("One lone blur")
        self.play(FadeOut(membrane), FadeOut(sites), FadeIn(blur, scale=0.22), run_time=1.46)
        shimmer(blur, amount=0.18)
        self.at("more sharply")
        cross = crosshair(CENTER, 0.23)
        self.play(Create(cross), run_time=0.75)
        self.at("shot noise approximation")
        title = side("Shot-noise approximation", 2.1, TEXT, 29)
        self.play(FadeIn(title), run_time=0.52)
        self.at("uncertainty equals")
        formula = side("Center uncertainty ≈", 1.16, YELLOW, 30)
        numerator = side("Blur standard deviation", 0.48, YELLOW, 29)
        denominator = side("√photon count", -0.63, YELLOW, 29)
        line = Line(p(1.35, -0.07), p(5.89, -0.07), color=YELLOW, stroke_width=2)
        self.play(Write(formula), run_time=0.62)
        self.at("blur standard deviation")
        self.play(Write(numerator), Create(line), run_time=0.86)
        self.at("square root of photons")
        self.play(Write(denominator), run_time=0.82)
        self.at("Take a 100 nanometer")
        bar = measure(1.02, CENTER + DOWN * 1.6)
        width = T("σ = 100 nm", 30, YELLOW).move_to(CENTER + DOWN * 2.02)
        ring = target_ring()
        self.play(Create(bar), FadeIn(width), Create(ring), run_time=1.05)
        self.at("giving 100 photons", lead=0.65)
        n = ValueTracker(0)
        photons = counter("{:.0f} photons", n, p(3.62, -1.75), size=34, color=GREEN)
        self.add(photons)
        spark_positions = [p(1.88, 0.64), p(-1.04, 1.57), p(1.3, 1.34), p(-1.85, 0.51),
                           p(1.63, -1.18), p(-1.75, -0.62), p(0.46, 1.86)]
        travel = [Dot(CENTER + pos, radius=0.074, color=GREEN) for pos in spark_positions]
        photons_in = [Succession(FadeIn(dot, run_time=0.19),
                                dot.animate(run_time=0.39).move_to(CENTER),
                                FadeOut(dot, run_time=0.12))
                      for dot in travel]
        self.play(n.animate(run_time=0.75, rate_func=linear).set_value(100),
                  LaggedStart(*photons_in, lag_ratio=0.32, run_time=1.72, rate_func=linear))
        self.at("The square root of 100")
        formula_group = VGroup(title, formula, numerator, line, denominator)
        root = side("√100 = 10", 1.06, YELLOW, 39)
        self.play(swap(formula_group, root), run_time=0.93)
        self.at("100 over 10")
        final = side("100 nm ÷ 10", 0.29, YELLOW, 35)
        self.play(Write(final), run_time=0.77)
        self.at("gives")
        estimate = side("≈ 10 nm", -0.56, YELLOW, 42)
        self.play(Transform(ring, target_ring(0.102)), FadeOut(cross), Write(estimate),
                  run_time=0.7)
        self.finish()


class S09OtherRoutes(SpokenScene):
    def construct(self):
        blur = gaussian_blurs([(0, 0)], 1.02, 2.42)
        self.add(microscope_field(), blur, scope_tag(size=26, color=TEXT))
        shimmer(blur, amount=0.34, speed=2.1)
        self.at("Switching sparse molecules")
        self.wait(1.5)
        self.at("Stefan Hell proposed")
        sted = side("STED", 1.37, PURPLE, 45)
        stefan = side("Stefan Hell", 0.59)
        self.play(FadeIn(sted), FadeIn(stefan), run_time=0.62)
        self.at("1994")
        proposed = side("Proposed in 1994", -0.16, GOLD, 29)
        self.play(FadeIn(proposed), run_time=0.59)
        self.at("showed it in")
        shown = side("Shown in 1999", -0.84, GOLD, 29)
        self.play(FadeIn(shown), run_time=0.64)
        x, y = sample_grid(2.35)
        r = np.hypot(x, y)
        ring = signal_image(np.exp(-0.5 * ((r - 1.08) / 0.35) ** 2) * 0.79,
                            CENTER + LEFT * 0.57, 4.7, PURPLE)
        self.at("A ring beam")
        self.play(FadeIn(ring, scale=0.68), run_time=0.42)
        blur.clear_updaters()
        small = gaussian_blurs([(0, 0)], 0.16, 2.42)
        core = gaussian_blurs([(0, 0)], 0.098, 2.42)
        self.play(ring.animate.move_to(CENTER), Transform(blur, small), run_time=2.17)
        self.at("leaving a tiny glowing center")
        self.play(FadeOut(ring), Transform(blur, core), run_time=1.39)
        self.at("Structured illumination")
        wide, recovered = sim_exposures()
        conventional, restored = sim_image(wide), sim_image(recovered)
        illumination = stripes()
        name = side("Structured illumination", 1.13, PURPLE)
        self.play(FadeOut(VGroup(sted, stefan, proposed, shown)), FadeOut(blur),
                  FadeIn(conventional), run_time=0.49)
        self.play(FadeIn(illumination), FadeIn(name), run_time=0.54)
        self.play(Rotate(illumination, angle=PI * 0.68), run_time=1.4, rate_func=linear)
        result = side("Reconstructed detail", -0.18, GREEN, 30)
        self.play(Transform(conventional, restored), FadeOut(illumination), FadeIn(result),
                  run_time=0.9)
        self.finish()


class S10Limits(SpokenScene):
    def construct(self):
        _, recovered = sim_exposures()
        field = microscope_field()
        last = sim_image(recovered)
        self.add(field, last, scope_tag(size=26, color=TEXT))
        initial = target_ring(0.102)
        isolated = gaussian_blurs([(0, 0)], 0.48, 2.42)
        self.at("That shot noise formula")
        self.play(FadeOut(last), FadeIn(isolated), FadeIn(initial), run_time=1.07)
        haze = gaussian_blurs([(-0.8, -0.48), (0.71, 0.59)], 0.89, 2.46, GREY)
        haze.set_opacity(0.50)
        isolated.set_z_index(1)
        initial.set_z_index(2)
        self.at("neglects background")
        bg = side("Background + pixel size", 1.0, RED, 32)
        self.play(FadeIn(haze), FadeIn(bg), run_time=1.17)
        haze.set_opacity(0.50)
        self.at("crowded molecules")
        crowded = gaussian_blurs([(-0.36, -0.19), (-0.24, 0.31), (0.26, 0.32),
                                  (0.42, -0.15)], 0.51, 2.42)
        warning = side("Overlapping blurs", -0.04, RED, 32)
        self.play(Transform(isolated, crowded), Transform(initial, target_ring(1.06)),
                  FadeIn(warning), run_time=1.7)
        self.at("Once a camera samples")
        pixels = camera_zoom()
        self.play(FadeOut(haze), FadeOut(isolated), FadeOut(initial), FadeOut(bg),
                  FadeOut(warning), FadeIn(pixels), run_time=1.14)
        self.at("further zoom adds")
        zoom = side("Same pixels, larger", 0.5, BLUE)
        self.play(pixels.animate.scale(MAX_PIXEL_ZOOM), FadeIn(zoom), run_time=1.85)
        self.at("Comparing live fixed")
        cells, labels = preparations(), preparation_labels()
        example = VGroup(*[T(name, 31, TEXT, weight=BOLD).move_to(label)
                           for name, label in zip(("Live cells", "Fixed cells", "Primary cells"), labels)])
        self.play(FadeOut(field), FadeOut(pixels), FadeOut(zoom), run_time=0.43)
        self.play(LaggedStart(*[FadeIn(cell[0], scale=0.85) for cell in cells], lag_ratio=0.22),
                  run_time=0.72)
        self.play(LaggedStart(*[FadeIn(mob) for mob in example], lag_ratio=0.29), run_time=1.1)
        self.at("tests whether a pattern")
        self.play(LaggedStart(*[FadeIn(cell[1:], scale=0.76) for cell in cells], lag_ratio=0.26),
                  run_time=1.43)
        self.at("without claiming every")
        caution = caption("Compare the preparations tested", size=31, color=GOLD, y=-2.95)
        self.play(FadeIn(caution), run_time=0.5)
        for cell in cells:
            pulse(cell[0], base=2.4, amp=1.8, speed=3)
        self.finish()


class S11Unlocked(SpokenScene):
    def construct(self):
        cells, labels = preparations(), preparation_labels()
        scope = scope_tag(size=26, color=TEXT)
        self.add(*cells, scope)
        for cell in cells:
            breathe_exposure(cell[0])
        milestones = T("STED · 1999   |   PALM, STORM, FPALM · 2006", 34, GOLD).move_to(p(0, 2.9))
        self.at("Palm")
        self.play(FadeIn(milestones), run_time=0.51)
        self.at("reach tens of nanometers")
        detail = caption("Tens of nanometers", color=YELLOW, y=-2.95)
        highlight = [Circle(radius=0.79, color=YELLOW, stroke_width=2.3)
                     .move_to(cell[0]) for cell in cells]
        self.play(FadeIn(detail), LaggedStart(*[Create(ring) for ring in highlight], lag_ratio=0.27),
                  run_time=1.34)
        self.at("Stone and colleagues")
        for cell in cells:
            cell[0].clear_updaters()
        self.play(FadeOut(VGroup(milestones, detail, *highlight)),
                  *[cell[0].animate.set_fill(FIELD) for cell in cells], run_time=0.64)
        name = T("Stone and colleagues", 31, GOLD).move_to(p(0, -2.84))
        self.play(FadeIn(name), run_time=0.55)
        self.at("CH27 mouse")
        self.play(FadeIn(labels[0]), FadeIn(labels[1]), run_time=1.03)
        self.at("Fixed primary mouse")
        self.play(FadeIn(labels[2]), run_time=0.61)
        self.play(Indicate(cells[2][0], color=BLUE, scale_factor=1.065), run_time=1.47)
        hero = cell_field(CENTER, radius=2.54, angle=0.24)
        self.at("A peptide probe")
        self.play(FadeOut(cells[1]), FadeOut(cells[2]), FadeOut(labels), FadeOut(name),
                  FadeOut(cells[0][2:]), run_time=0.34)
        field, receptors = cells[0][:2]
        self.play(Transform(VGroup(field, receptors), hero[:2]), run_time=0.72)
        bcr = side("B-cell receptors", 1.35, PURPLE)
        self.play(FadeIn(bcr), run_time=0.62)
        self.at("gathered near")
        ordered = hero[2]
        ordered_label = side("Ordered-membrane probe", 0.39, TEAL, 29)
        arrivals = ordered.copy()
        for dot, end in zip(arrivals, ordered):
            dot.move_to(CENTER + 2.35 * (end.get_center() - CENTER))
        self.add(arrivals)
        self.play(Transform(arrivals, ordered), FadeIn(ordered_label), run_time=1.74)
        self.at("A disordered membrane probe")
        disordered = hero[3]
        disordered_label = side("Disordered-membrane probe", -0.52, ORANGE, 29)
        margin = disordered.copy()
        for dot, end in zip(margin, disordered):
            dot.move_to(CENTER + 0.79 * (end.get_center() - CENTER))
        self.play(FadeIn(margin), FadeIn(disordered_label), run_time=0.58)
        self.play(Transform(margin, disordered), run_time=1.31)
        self.at("That supports phase")
        caution = side("Phase-like sorting\nin this system", -1.79, GOLD, 34)
        self.play(FadeIn(caution), run_time=0.6)
        outline = Circle(radius=1.20, color=TEAL, stroke_width=2.4).move_to(CENTER)
        self.play(Create(outline), run_time=1.20)
        pulse(outline, base=2.7, amp=1.7, speed=3.6)
        self.at("Controlling")
        rule = side("Resolved membrane map", 0.15, GREEN, 33)
        legend = VGroup(bcr, ordered_label, disordered_label, caution)
        localized = VGroup(receptors, arrivals, margin)
        positions = [[(dot.get_center() - CENTER)[:2] for dot in marks] for marks in localized]
        colors = (PURPLE, TEAL, ORANGE)
        glows = [gaussian_blurs(points, 0.34, 2.46, color) for points, color in zip(positions, colors)]
        focused = [gaussian_blurs(points, 0.13, 2.46, color) for points, color in zip(positions, colors)]
        outline.clear_updaters()
        self.play(FadeOut(outline), FadeOut(legend), FadeOut(localized),
                  *[FadeIn(glow) for glow in glows], run_time=0.75)
        self.at("which molecules glow")
        self.play(LaggedStart(*[glow.animate(rate_func=there_and_back).set_opacity(0.58)
                                for glow in glows], lag_ratio=0.4), run_time=1.2)
        self.at("overlapping blurs")
        self.play(*[Transform(glow, focus) for glow, focus in zip(glows, focused)], run_time=1.02)
        self.at("into maps")
        self.play(*[FadeOut(glow) for glow in glows], FadeIn(localized), FadeIn(rule), run_time=0.64)
        self.finish()


class S12End(EndCard):
    LINE = "Control when and where molecules glow to separate overlapping light blurs."
