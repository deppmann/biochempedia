"""Slicing Thick Tissue With Light. All diagrams are schematic.

Color map (shared patch-clamp palette):
BLUE   microscope glass and the second eye's fluorescence
GREY   tissue support, barriers and reference lines
GREEN  labelled cells and their optical sections
RED    the first eye's fluorescence, including the out-of-plane speck
YELLOW illumination, measured signal and stimulation
PURPLE digestive compartments and junctions
GOLD   study credits and the prediction cue
"""
from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
TISSUE_TOP = "#304555"
TISSUE_FACE = "#263747"
TISSUE_EDGE = "#566B80"
QUESTION = "How does the stack show the speck is outside?"

# All views share the same specimen coordinates. z is height within the specimen.
OPEN = (0.0, -0.44, 1.14)
OPTICAL = (-1.62, -1.28, 0.83)
DETAIL = (0.0, 0.03, 1.0)
PIN_X = OPTICAL[0]
LENS_Y, PIN_Y, DETECTOR_Y = 1.73, 2.51, 3.25
FOCUS_Z = -0.04
SPECK = (0.08, 0.06, 0.56)
BRANCHES = (
    ((-0.36, 0.02, 0.02), (-1.33, 0.43, 0.13), (-2.43, 1.16, 0.37), (-3.19, 1.46, 0.78)),
    ((-1.33, 0.43, 0.13), (-1.96, 1.46, 0.56), (-1.96, 2.02, 0.93)),
    ((-2.43, 1.16, 0.37), (-2.84, 0.76, 0.53), (-3.47, 0.59, 0.69)),
    ((-0.30, -0.30, -0.08), (-1.40, -0.92, -0.29), (-2.04, -1.75, -0.39), (-2.89, -1.90, -0.23)),
    ((-1.40, -0.92, -0.29), (-2.22, -0.52, -0.80), (-3.40, -0.38, -0.96)),
    ((0.36, 0.24, 0.03), (1.49, 0.71, 0.18), (2.18, 1.17, 0.41), (3.25, 1.75, 0.62)),
    ((1.49, 0.71, 0.18), (1.94, 1.65, -0.45), (2.36, 1.95, -0.63)),
    ((2.18, 1.17, 0.41), (2.96, 1.38, 0.93), (3.43, 1.24, 1.13)),
    ((0.30, -0.35, -0.10), (1.24, -1.17, -0.39), (2.06, -1.66, -0.50), (3.28, -1.66, -0.22)),
    ((1.24, -1.17, -0.39), (1.67, -1.99, -0.89), (2.30, -2.01, -1.07)),
    ((2.06, -1.66, -0.50), (2.84, -1.26, -1.07), (3.48, -0.94, -1.14)),
)
OUTER = (
    (SPECK, RED, 0.12), ((-3.6, -1.4, 1.12), BLUE, 0.11), ((-2.5, 1.6, 1.23), RED, 0.13),
    ((-1.28, -1.35, 0.91), BLUE, 0.08), ((1.42, 1.69, 1.23), BLUE, 0.13),
    ((2.68, -1.31, 1.19), RED, 0.12), ((3.37, 1.02, -0.02), BLUE, 0.11),
    ((-3.50, 1.60, -0.68), BLUE, 0.08), ((-2.42, -1.47, -1.32), RED, 0.12),
    ((-0.65, 1.49, -1.18), RED, 0.09), ((0.63, -1.70, -1.21), BLUE, 0.11),
    ((2.43, 1.10, -1.24), RED, 0.12), ((3.42, -1.38, -1.02), BLUE, 0.09),
    ((-2.86, 0.49, 0.01), RED, 0.08), ((2.90, 0.28, -0.10), BLUE, 0.09),
)
INNER = (
    ((-0.42, 0.11, -0.09), RED, 0.08), ((-0.17, 0.28, 0.05), RED, 0.075),
    ((-0.08, -0.17, -0.11), BLUE, 0.075), ((0.31, -0.24, 0.07), RED, 0.07),
    ((0.57, -0.02, -0.04), RED, 0.075), ((0.39, 0.19, 0.17), BLUE, 0.07),
)


def xy(x, y):
    return np.array([x, y, 0.0])


def project(point, view, angle=0.0, top=False):
    x, y, z = point
    c, s = np.cos(angle), np.sin(angle)
    u, v = c * x - s * y, s * x + c * y
    cx, cy, scale = view
    return xy(cx + scale * (u + (0 if top else 0.37 * v)),
              cy + scale * (v if top else 0.49 * v + z))


def face(points, color, opacity=1, stroke=TISSUE_EDGE, width=1.7):
    return Polygon(*points, stroke_color=stroke, stroke_width=width,
                   fill_color=color, fill_opacity=opacity)


def filament(points, color, width=4, opacity=1):
    path = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    path.set_points_as_corners(points)
    return path


def light_path(points, color, width=3, opacity=1):
    return VGroup(filament(points, color, width * 3.5, opacity * 0.16),
                  filament(points, color, width, opacity))


def speck(point, color, radius=0.10, power=1.0):
    return VGroup(
        Dot(point, radius=radius * 2.6, color=color, fill_opacity=power * 0.10),
        Dot(point, radius=radius * 1.65, color=color, fill_opacity=power * 0.26),
        Dot(point, radius=radius, color=color, fill_opacity=power),
    )


def plane_corners(view, z, angle=0):
    return [project(p, view, angle) for p in
            [(-4.0, -2.12, z), (4.0, -2.12, z), (4.0, 2.12, z), (-4.0, 2.12, z)]]


def tissue_shell(view):
    a, b, c, d = plane_corners(view, 1.49)
    e, f, g, h = plane_corners(view, -1.49)
    return VGroup(
        face([e, f, b, a], TISSUE_FACE, 0.90),
        face([f, g, c, b], "#334b59", 0.9),
        face([a, b, c, d], TISSUE_TOP, 0.75),
        Line(e, h, color=TISSUE_EDGE, stroke_width=1.4),
        Line(h, g, color=TISSUE_EDGE, stroke_width=1.4),
        Line(d, h, color=TISSUE_EDGE, stroke_width=1.4),
    )


def cell(view, angle=0, top=False, intensity=1):
    point = lambda p: project(p, view, angle, top)
    scale = view[2]
    body = Ellipse(width=1.65 * scale, height=(1.34 if top else 0.96) * scale,
                   stroke_color=GREEN, stroke_width=2.5, stroke_opacity=intensity,
                   fill_color=GREEN, fill_opacity=0.60 * intensity).move_to(point((0, 0, 0)))
    body_glow = body.copy().scale(1.22).set_stroke(width=0).set_fill(GREEN, 0.15 * intensity)
    branches = VGroup()
    for branch in BRANCHES:
        for index, (p, q) in enumerate(zip(branch, branch[1:])):
            width = (13 if abs(branch[0][0]) < 0.5 else 7)
            width = max(2.7, width * (0.64 ** index)) * scale
            branches.add(light_path([point(p), point(q)], GREEN, width, 0.90 * intensity))
    return VGroup(branches, body_glow, body)


def emitters(view, items=OUTER, angle=0, top=False, power=1.0):
    return VGroup(*(speck(project(p, view, angle, top), c, r * view[2], power)
                    for p, c, r in items))


def specimen(view):
    return VGroup(tissue_shell(view), cell(view), emitters(view))


def label(text, x, y, color=TEXT, size=30):
    return T(text, size, color).move_to(xy(x, y))


def haze(view, radius, strength):
    """Defocus spreads each emitter's light across a wider disk."""
    scatter = VGroup()
    for p, color, r in OUTER[1:13]:
        pos = project((p[0] * 0.85, p[1] * 0.55, p[2] * 0.55), view)
        for factor, alpha in [(1.0, 0.044), (0.8, 0.047), (0.57, 0.059), (0.36, 0.079), (0.19, 0.13)]:
            scatter.add(Dot(pos, radius=radius * factor * (0.92 + r), color=color,
                            fill_opacity=alpha * strength))
    return scatter


def objective(x, y):
    return VGroup(
        Ellipse(width=3.05, height=0.44, fill_color=BLUE, fill_opacity=0.29,
                stroke_color=BLUE, stroke_width=2.6).move_to(xy(x, y)),
        Line(xy(x - 1.24, y), xy(x + 1.24, y), stroke_color=BLUE,
             stroke_width=1.4, stroke_opacity=0.5),
    )


def aperture():
    bars = VGroup()
    for sign in (-1, 1):
        bars.add(RoundedRectangle(width=2.21, height=0.27, corner_radius=0.055,
                                  stroke_color=GREY, stroke_width=1.8,
                                  fill_color="#546579", fill_opacity=1)
                 .move_to(xy(PIN_X + sign * 1.23, PIN_Y)))
    detector = RoundedRectangle(width=1.22, height=0.36, corner_radius=0.08,
                                stroke_color=BLUE, stroke_width=2,
                                fill_color=BLUE, fill_opacity=0.20).move_to(xy(PIN_X, DETECTOR_Y))
    return VGroup(bars, detector)


def section(view, z, sharp=True):
    """A plane and the labelled material that intersects this z slice."""
    pane = face(plane_corners(view, z), "#34736b", 0.57,
                stroke=TEAL, width=2.8)
    if not sharp:
        return pane
    signal = VGroup()
    step = 0.19
    for branch in BRANCHES:
        for a, b in zip(branch, branch[1:]):
            a, b = np.array(a), np.array(b)
            delta = b[2] - a[2]
            if abs(delta) < 1e-6:
                if abs(a[2] - z) <= step:
                    signal.add(light_path([project(a, view), project(b, view)], GREEN, 5))
                continue
            lo, hi = sorted(((z - step - a[2]) / delta, (z + step - a[2]) / delta))
            lo, hi = max(0, lo), min(1, hi)
            if hi > lo:
                a2, b2 = a + (b - a) * lo, a + (b - a) * hi
                a2[2] = b2[2] = z
                signal.add(light_path([project(a2, view), project(b2, view)], GREEN, 5))
    if abs(z) < 0.48:
        width = 1.47 * np.sqrt(1 - (z / 0.48) ** 2)
        signal.add(Ellipse(width=width * view[2], height=width * 0.53 * view[2],
                           stroke_color=GREEN, stroke_width=2, fill_color=GREEN,
                           fill_opacity=0.78).move_to(project((0, 0, z), view)))
    for point, color, radius in OUTER + INNER:
        distance = abs(z - point[2])
        if distance < 0.19:
            signal.add(speck(project((*point[:2], z), view), color, radius * view[2],
                             power=1 - 2.4 * distance))
    return VGroup(pane, signal)


def illumination(x, z):
    focal = project((x, 0, z), OPTICAL)
    left, right = xy(PIN_X - 0.65, LENS_Y), xy(PIN_X + 0.65, LENS_Y)
    source = xy(-5.91, 2.18)
    return VGroup(
        light_path([source, xy(PIN_X - 0.22, LENS_Y + 0.07), focal], YELLOW, 2.5),
        face([left, right, focal], YELLOW, 0.10, stroke=YELLOW, width=0.9),
        speck(focal, YELLOW, 0.12),
    )


def focused_return(x, z):
    focal = project((x, 0, z), OPTICAL)
    pin = xy(PIN_X, PIN_Y)
    rays = [light_path([focal, xy(PIN_X + dx, LENS_Y), pin,
                        xy(PIN_X - 0.33 * dx, DETECTOR_Y)], GREEN, 2.2)
            for dx in (-0.83, 0.83)]
    return VGroup(*rays, speck(xy(PIN_X, DETECTOR_Y), GREEN, 0.10))


def rejected_return():
    rays = VGroup()
    for index, spread in [(2, -1), (10, 1)]:
        point, color, _ = OUTER[index]
        focal = project(point, OPTICAL)
        launch = xy(PIN_X + spread * 0.93, LENS_Y)
        near = xy(PIN_X + spread * 0.49, PIN_Y - 0.145)
        far = xy(PIN_X + spread * 2.17, PIN_Y - 0.145)
        rays.add(face([focal, launch, far, near], color, 0.10, stroke=color, width=1.15))
        for k in (0.12, 0.49, 0.87):
            rays.add(light_path([focal, launch + RIGHT * (k - 0.5) * 0.34,
                                  interpolate(near, far, k)], color, 2, 0.67))
    return rays


def optical_world():
    return VGroup(specimen(OPTICAL), objective(PIN_X, LENS_Y), aperture())


def return_labels():
    return VGroup(label("Pinhole", 1.76, PIN_Y, BLUE),
                  label("Detector", 0.42, DETECTOR_Y, BLUE),
                  label("Out-of-focus light", 2.79, 1.60, RED))


def reconstructed(view, angle=0, outer=True):
    return VGroup(cell(view, angle), emitters(view, INNER, angle),
                  emitters(view, OUTER if outer else (), angle, power=0.85))


def prediction_world():
    world = VGroup(tissue_shell(DETAIL), section(DETAIL, -1.26, False),
                   section(DETAIL, FOCUS_Z, False), cell(DETAIL),
                   emitters(DETAIL, OUTER[:1]))
    return world


def compartments(view, color=PURPLE, fill=0.58):
    return VGroup(*(Ellipse(width=w * view[2], height=h * view[2], stroke_width=3,
                             stroke_color=color, fill_color=color, fill_opacity=fill)
                    .move_to(project(p, view)) for p, w, h in [
        ((-0.27, 0.10, -0.045), 0.58, 0.37), ((0.43, -0.04, 0.025), 0.51, 0.34),
    ]))


class S01Hook(SpokenScene):
    def construct(self):
        block = specimen(OPEN)
        tag = scope_tag(size=28, color=TEXT)
        self.add(block, tag)
        self.at("glowing speck")
        marker = Circle(radius=0.38, color=RED, stroke_width=3).move_to(project(SPECK, OPEN))
        close_view = (0.43, -0.13, 1.21)
        self.play(Create(marker), run_time=0.40)
        self.play(Transform(block, specimen(close_view)),
                  marker.animate.move_to(project(SPECK, close_view)), run_time=1.20)
        self.at("just sitting behind")
        self.play(Transform(block, specimen(OPEN)),
                  marker.animate.scale(0.76).move_to(project(SPECK, OPEN)), run_time=1.66)
        self.at("under an ordinary")
        lens = objective(0, 3.12)
        self.play(FadeOut(marker), FadeIn(lens, shift=DOWN * 0.18), run_time=0.72)
        self.at("thick glowing tissue")
        mist = haze(OPEN, 1.12, 1.22)
        self.play(FadeIn(mist, scale=0.72), run_time=2.28)
        self.at("from layers above")
        rays = VGroup(*(light_path([project(p, OPEN), xy(end, 2.92)], c, 1.9, 0.66)
                        for (p, c, _), end in zip([OUTER[i] for i in (2, 4, 8, 11)], (-0.9, 0.6, -0.52, 0.95))))
        self.play(LaggedStart(*[Create(ray) for ray in rays], lag_ratio=0.20), run_time=2.12)
        self.at("collapsing depth")
        blur = haze(OPEN, 1.70, 1.5)
        self.play(FadeOut(rays), Transform(mist, blur), run_time=1.58)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Confocal Microscopy"
    TITLE = "Slicing Thick Tissue With Light"

    def construct(self):
        backdrop = VGroup(specimen(OPEN), objective(0, 3.12), haze(OPEN, 1.70, 1.5))
        dimmed = backdrop.copy().fade(0.65)
        shade = Rectangle(width=11.5, height=1.83, stroke_width=0,
                          fill_color=BG, fill_opacity=1).move_to(xy(0, 0.18))
        title = T(self.TITLE, 49, font=TITLE_FONT).move_to(xy(0, 0.31))
        rule = Line(xy(-0.61, -0.27), xy(0.61, -0.27), stroke_color=GOLD, stroke_width=3)
        self.add(backdrop)
        self.play(Transform(backdrop, dimmed), FadeIn(shade), run_time=0.27)
        self.play(FadeIn(title), GrowFromCenter(rule), run_time=0.40)
        self.wait(0.80)
        self.play(FadeOut(title), FadeOut(rule), run_time=0.27)
        self.play(FadeOut(shade), Transform(backdrop, VGroup(specimen(OPEN), objective(0, 3.12),
                                                              haze(OPEN, 1.70, 1.5))),
                  run_time=0.26)


class S03Pinhole(SpokenScene):
    def construct(self):
        block = specimen(OPEN)
        mist = haze(OPEN, 1.70, 1.5)
        lens = objective(0, 3.12)
        self.add(block, mist, lens, scope_tag(size=28, color=TEXT))
        self.at("a confocal microscope")
        self.play(Transform(block, specimen(OPTICAL)), Transform(lens, objective(PIN_X, LENS_Y)),
                  FadeOut(mist), run_time=1.53)
        pin = aperture()
        labels = return_labels()
        self.at("clears that blur")
        self.play(FadeIn(pin, shift=DOWN * 0.13), run_time=0.82)
        self.at("with a pinhole")
        self.play(FadeIn(labels[0]), run_time=0.48)
        self.at("fluorescent dyes")
        chosen = emitters(OPTICAL, OUTER[-2:], power=1)
        self.play(FadeIn(chosen, scale=0.65), run_time=0.70)
        self.play(Indicate(block[1], color=GREEN, scale_factor=1.025), run_time=2.15)
        self.at("a focused laser")
        x = ValueTracker(-2.8)
        pane = section(OPTICAL, FOCUS_Z, False)
        beam = always_redraw(lambda: illumination(x.get_value(), FOCUS_Z))
        laser_label = label("Laser", -5.45, 2.61, YELLOW)
        self.play(FadeIn(pane), FadeIn(beam), FadeIn(laser_label), run_time=0.65)
        signal = always_redraw(lambda: VGroup(*(
            speck(project(p, OPTICAL), color, 1.4 * radius,
                  power=np.exp(-((p[0] - x.get_value()) / 0.56) ** 2))
            for p, color, radius in [*OUTER[-2:], ((0, 0, FOCUS_Z), GREEN, 0.19)]
        )))
        self.add(beam, signal)
        self.play(x.animate.set_value(2.36), FadeOut(chosen), run_time=2.77, rate_func=linear)
        self.remove(signal)
        self.at("light from the focal spot")
        accepted = always_redraw(lambda: focused_return(x.get_value(), FOCUS_Z))
        self.play(FadeIn(accepted), FadeOut(laser_label), run_time=0.72)
        self.play(x.animate.set_value(0), run_time=1.49, rate_func=smooth)
        self.at("right at the pinhole")
        self.play(FadeIn(labels[1]), run_time=0.51)
        self.at("light from other depths")
        rejected = rejected_return()
        self.play(LaggedStart(*[Create(ray) for ray in rejected], lag_ratio=0.12), run_time=2.40)
        self.at("most hits the barrier")
        self.play(FadeIn(labels[2]), Indicate(pin[0], color=GREY, scale_factor=1.035),
                  run_time=1.1)
        self.finish()


class S04Stack(SpokenScene):
    def construct(self):
        world = optical_world()
        tags = return_labels()
        rejected = rejected_return()
        beam = illumination(0, FOCUS_Z)
        accepted = focused_return(0, FOCUS_Z)
        pane = section(OPTICAL, FOCUS_Z, False)
        self.add(world, pane, beam, accepted, rejected, tags, scope_tag(size=28, color=TEXT))
        self.at("rejecting out of focus")
        self.play(FadeOut(rejected), FadeOut(tags[2]),
                  pane.animate.set_fill("#246c59", opacity=0.86), run_time=1.60)
        sharp = section(OPTICAL, FOCUS_Z)
        self.at("yields a sharp")
        self.play(FadeIn(sharp), FadeOut(pane), run_time=0.96)
        optical = label("Optical section", 3.95, 2.03, GREEN)
        self.at("optical section")
        self.play(FadeIn(optical), sharp[0].animate.set_fill("#4c9782", opacity=0.88),
                  run_time=0.72)
        self.play(sharp[0].animate.set_fill("#34736b", opacity=0.57), run_time=1.08)

        stack_view = (4.48, -0.50, 0.41)
        slices = []
        self.at("it slices thick tissue")
        first_view = (stack_view[0], stack_view[1] + 1.63 * 0.64 - FOCUS_Z * stack_view[2], stack_view[2])
        first = section(first_view, FOCUS_Z)
        self.play(TransformFromCopy(sharp, first), run_time=2.7)
        slices.append(first)
        self.at("step the focus deeper")
        stack = label("Optical stack", 3.95, 2.03, GREEN)
        self.play(swap(optical, stack, 0.64), FadeOut(tags), FadeOut(accepted), run_time=0.64)
        for depth, height in ((-0.43, 0.56), (-0.84, -0.51), (-1.27, -1.58)):
            self.play(Transform(sharp, section(OPTICAL, depth)), Transform(beam, illumination(0, depth)),
                      run_time=0.78)
            # Move the actual fluorescent section into the reconstruction stack.
            duplicate = sharp.copy()
            target_view = (stack_view[0], stack_view[1] + height * 0.64 - depth * stack_view[2], stack_view[2])
            self.play(Transform(duplicate, section(target_view, depth)), run_time=0.92)
            slices.append(duplicate)

        self.at("software rebuilds")
        model_label = label("3D reconstruction", 0, 2.95, GREEN)
        right_view = (3.70, -0.43, 0.62)
        model = reconstructed(right_view)
        self.play(FadeOut(world), FadeOut(beam), FadeOut(sharp), FadeOut(stack),
                  *[sheet.animate.move_to(xy(3.70, -0.43)).set_opacity(0)
                    for sheet in slices], FadeIn(model), run_time=1.18)
        theta = ValueTracker(0)
        live = always_redraw(lambda: reconstructed((3.70 * (1 - theta.get_value() / 0.46),
                                                     -0.43, 0.62 + 1.17 * theta.get_value()),
                                                    angle=theta.get_value()))
        self.remove(model, *slices)
        self.add(live)
        self.play(FadeIn(model_label), theta.animate.set_value(0.46), run_time=2.55)
        self.finish()


class S05PredictQ(SpokenScene):
    def construct(self):
        model = reconstructed((0, -0.43, 1.1582), angle=0.46)
        heading = label("3D reconstruction", 0, 2.95, GREEN)
        tag = scope_tag(size=28, color=TEXT)
        self.add(model, heading, tag)
        world = prediction_world()
        self.at("test that on")
        self.play(FadeIn(world, shift=UP * 0.12), FadeOut(model), FadeOut(heading), run_time=1.80)
        self.at("a red speck")
        locator = Circle(radius=0.32, color=RED, stroke_width=2.8).move_to(project(SPECK, DETAIL))
        halo = section(DETAIL, SPECK[2], False).set_fill("#385e72", opacity=0.70)
        self.play(Create(locator), FadeIn(halo, shift=UP * 0.23), run_time=1.28)
        self.bring_to_front(world[-1], locator)
        self.at("touching its outside")
        self.play(Indicate(world[-1], color=RED, scale_factor=1.20),
                  halo.animate.set_fill("#5a3c53", opacity=0.42),
                  locator.animate.scale(1.10), run_time=1.47)
        self.at("in a flat image")
        flat_view = (0, 0.05, 1.10)
        flat = VGroup(
            face([xy(-5.28, -2.48), xy(5.28, -2.48), xy(5.28, 2.48), xy(-5.28, 2.48)], TISSUE_FACE),
            cell(flat_view, top=True), emitters(flat_view, OUTER[:1], top=True))
        flat_label = label("Flat image", 0, 3.06)
        self.play(FadeOut(locator), FadeOut(halo), FadeOut(world), FadeIn(flat, scale=0.94), run_time=1.04)
        self.play(FadeIn(flat_label), Indicate(flat[-1], color=RED, scale_factor=1.23), run_time=1.1)
        self.at("when you step")
        self.play(FadeOut(flat), FadeOut(flat_label), FadeIn(world, scale=1.03), run_time=1.27)
        self.at("how can you tell")
        self.play(FadeOut(tag), FadeIn(question_card(QUESTION, size=33), shift=UP * 0.15),
                  world[0][0].animate.set_fill("#547888", opacity=0.91), run_time=0.72)
        self.play(world[0][0].animate.set_fill(TISSUE_FACE, opacity=0.90),
                  run_time=2.08, rate_func=linear)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = {"size": 33}
    SECONDS = 4.5

    def backdrop(self):
        return prediction_world()

    def finish(self):
        # The ring uses the exact silent track length.
        pass


def filled_cell(scale):
    """Both cell volumes contain the same schematic label fraction."""
    body = Ellipse(width=4.5 * scale, height=3.15 * scale,
                   stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.45)
    labels = VGroup(*(speck(xy(x * scale, y * scale), RED, 0.16 * scale)
                      for x, y in [(-0.98, 0.3), (-0.51, -0.53), (0.02, 0.56),
                                   (0.27, -0.11), (0.95, 0.36), (0.85, -0.54)]))
    return VGroup(body, labels)


class S07Controls(SpokenScene):
    def construct(self):
        shell, lower, base_plane, green_cell, outside = prediction_world()
        q = question_card(QUESTION, size=33)
        self.add(shell, lower, base_plane, green_cell, outside, q)
        level = ValueTracker(FOCUS_Z)
        scanning = always_redraw(lambda: section(DETAIL, level.get_value(), False)
                                 .set_fill("#477e7b", opacity=0.82))
        slice_label = label("Higher slice", 0, 3.12, RED)
        self.at("the spec peaks")
        self.remove(base_plane)
        self.add(scanning, outside)
        self.play(FadeOut(q), level.animate.set_value(SPECK[2]),
                  Succession(Wait(0.78), FadeIn(slice_label, run_time=0.42), Wait(0.36)),
                  run_time=1.56)
        self.at("outside the rebuilt")
        self.play(Indicate(outside, color=RED, scale_factor=1.32), run_time=0.92)
        mask = label("3D cell mask", 0, 3.12, GREEN)
        self.at("software removes")
        keep = emitters(DETAIL, INNER)
        self.play(FadeOut(outside, scale=0.40), FadeIn(keep), FadeOut(scanning),
                  swap(slice_label, mask, 0.94), run_time=1.08)

        self.at("raw volume misleads")
        panels = TwoPanel("Small cell", "Large cell", colors=(GREEN, GREEN),
                          top=2.85, bottom=-2.36, width=12.35)
        small, big = filled_cell(0.59), filled_cell(1)
        panels.put(small, "left")
        panels.put(big, "right")
        panel_frames = VGroup(panels.left_frame, panels.right_frame)
        panel_labels = VGroup(panels.left_head, panels.right_head)
        self.play(FadeOut(mask), run_time=0.28)
        self.play(FadeOut(shell), FadeOut(lower), FadeOut(green_cell), FadeOut(keep),
                  FadeIn(panel_frames), FadeIn(small, scale=0.70), FadeIn(big, scale=0.70),
                  run_time=1.31)
        self.play(FadeIn(panel_labels), run_time=0.50)
        self.at("large cells hold more")
        self.play(Indicate(small[1], color=RED, scale_factor=1.10),
                  Indicate(big[1], color=RED, scale_factor=1.10),
                  small[0].animate.set_fill(GREEN, opacity=0.27),
                  big[0].animate.set_fill(GREEN, opacity=0.27), run_time=1.85)
        self.at("researchers divide")
        formula = VGroup(T("Label volume inside", 32, RED), T("÷", 35), T("cell volume", 32, GREEN))
        formula.arrange(RIGHT, buff=0.26).move_to(xy(0, -3.07))
        self.play(FadeIn(formula[0]), run_time=0.82)
        self.at("by cell volume")
        self.play(FadeIn(formula[1]), FadeIn(formula[2]),
                  small[0].animate.set_fill(GREEN, opacity=0.57),
                  big[0].animate.set_fill(GREEN, opacity=0.57), run_time=0.50)

        self.at("independent checks")
        internal = reconstructed(DETAIL, outer=False)
        shell = tissue_shell(DETAIL)
        self.play(FadeOut(panel_labels), FadeOut(formula), run_time=0.30)
        self.play(FadeOut(panel_frames), FadeOut(small), FadeOut(big), FadeIn(shell),
                  FadeIn(internal, scale=0.88), run_time=1.18)
        stained = compartments(DETAIL)
        self.at("label overlaps")
        self.play(LaggedStart(*[GrowFromCenter(a) for a in stained], lag_ratio=0.4),
                  shell[0].animate.set_fill("#4b4260", opacity=0.92),
                  run_time=1.10)
        self.bring_to_front(internal[1])
        compartment_label = label("Digestive compartments", 0, 3.10, PURPLE)
        self.at("digestive compartments")
        self.play(FadeIn(compartment_label), run_time=0.65)
        self.at("dye that glows")
        acid_label = label("Acid-activated dye", 0, 3.10, YELLOW)
        glow = compartments(DETAIL, YELLOW, 0.78)
        self.play(Transform(stained, glow), swap(compartment_label, acid_label, 1.30),
                  shell[0].animate.set_fill(TISSUE_FACE, opacity=0.90), run_time=2.12)
        self.finish()


def follicle_scene():
    """One continuous axon tree with three follicle contacts."""
    shell = face([xy(-5.78, -2.71), xy(5.76, -2.71), xy(5.76, 2.35), xy(-5.78, 2.35)],
                 TISSUE_FACE, 0.93)
    roots, endings, follicles = VGroup(), VGroup(), VGroup()
    trunk = light_path([xy(-4.89, -1.91), xy(-3.69, -1.69), xy(-2.20, -1.17),
                        xy(-0.85, -0.95), xy(0.50, -0.57), xy(1.46, -0.45)], GREEN, 8)
    for index, x in enumerate((-2.91, 0, 3.15)):
        tube = Ellipse(width=0.95, height=2.27, stroke_width=3, stroke_color=GREY,
                       fill_color=TISSUE_TOP, fill_opacity=0.95).rotate(-0.15)
        tube.move_to(xy(x, 0.62))
        shaft = Line(xy(x - 0.02, 0.01), xy(x + 0.28, 2.04), color=GREY, stroke_width=5)
        follicles.add(VGroup(tube, shaft))
        start = [xy(-3.69, -1.69), xy(-0.85, -0.95), xy(1.46, -0.45)][index]
        roots.add(light_path([start, xy(x - 0.58, -0.55), xy(x - 0.54, 0.45)], GREEN, 5))
        for j in range(2):
            ends = [xy(x + 0.56 * np.cos(a), 0.48 + 0.39 * j + 0.18 * np.sin(a))
                    for a in np.linspace(PI, -0.88 * PI, 34)]
            endings.add(light_path(ends, GREEN, 4))
    return VGroup(shell, follicles, trunk, roots, endings)


class S08Limits(SpokenScene):
    def construct(self):
        shell = tissue_shell(DETAIL)
        model = reconstructed(DETAIL, outer=False)
        stained = compartments(DETAIL, YELLOW, 0.78)
        prior = label("Acid-activated dye", 0, 3.10, YELLOW)
        self.add(shell, model, stained, prior)
        self.at("two limits remain")
        self.play(FadeOut(prior), FadeOut(stained), FadeIn(emitters(DETAIL)),
                  run_time=1.20)
        self.at("fixed tissue")
        snapshot = label("Fixed snapshot", 0, 3.10, GOLD)
        expose = section(DETAIL, 1.45, False)
        self.play(Create(expose), run_time=1.20)
        self.at("one frozen moment")
        self.play(FadeOut(expose), FadeIn(snapshot), run_time=0.81)

        self.at("seeing a structure")
        paths = VGroup(*(DashedVMobject(Arrow(xy(side * 2.68, 1.78), xy(side * 1.80, 1.40),
                                              path_arc=side * 0.55, buff=0, color=YELLOW,
                                              stroke_width=3, tip_length=0.16), num_dashes=6)
                         for side in (-1, 1)))
        self.play(Create(paths), shell[0].animate.set_fill("#393e58", opacity=0.93),
                  run_time=1.24)
        marks = VGroup(*(label("?", side * 1.80, 1.40, YELLOW, 38) for side in (-1, 1)))
        self.at("how it works")
        self.play(swap(paths, marks, 0.85),
                  shell[0].animate.set_fill(TISSUE_FACE, opacity=0.90), run_time=0.85)

        skin, follicles, trunk, roots, endings = follicle_scene()
        self.at("counting stained branches")
        self.play(FadeOut(marks), run_time=0.27)
        self.play(Transform(shell, skin), FadeOut(model), FadeOut(snapshot),
                  *[FadeOut(m) for m in self.mobjects if m not in (shell, model, snapshot)],
                  run_time=1.07)
        self.play(FadeIn(follicles, shift=UP * 0.09), FadeIn(trunk), run_time=1.20)
        self.at("one nerve cell")
        self.play(LaggedStart(*[Create(r) for r in roots], lag_ratio=0.25), run_time=1.45)
        self.at("counting endings")
        self.play(LaggedStart(*[Create(r) for r in endings], lag_ratio=0.15), run_time=1.27)
        one = label("One neuron", -4.52, -3.12, GREEN)
        many = label("Multiple endings", 2.42, -3.12, GREEN)
        self.play(FadeIn(one), FadeIn(many), Indicate(trunk, color=GREEN, scale_factor=1.045),
                  run_time=1.13)
        self.finish()


def pyramidal_slice():
    corners = [xy(-6.25, -1.67), xy(-1.22, -1.67), xy(-0.59, 1.93), xy(-5.62, 1.93)]
    plane = face(corners, TISSUE_FACE, 0.95)
    soma = face([xy(-3.46, 0.45), xy(-3.96, -0.61), xy(-2.91, -0.61)],
                GREEN, 0.69, stroke=GREEN, width=2.5)
    branches = (
        ((-3.46, 0.29), (-3.32, 1.09), (-3.23, 1.65), (-3.39, 2.16)),
        ((-3.31, 1.13), (-3.87, 1.48), (-4.68, 1.80)),
        ((-3.23, 1.65), (-2.80, 1.84), (-2.41, 2.15)),
        ((-3.83, -0.25), (-4.39, -0.15), (-5.10, 0.12), (-5.62, 0.47)),
        ((-4.38, -0.15), (-4.99, -0.59), (-5.59, -0.82)),
        ((-5.08, 0.12), (-5.21, 0.56), (-5.48, 0.92)),
        ((-3.16, -0.36), (-2.60, -0.20), (-1.87, 0.23), (-1.27, 0.35)),
        ((-1.87, 0.23), (-1.77, 0.60), (-1.36, 0.94)),
        ((-2.60, -0.20), (-2.21, -0.62), (-1.67, -0.81)),
        ((-3.44, -0.54), (-3.38, -1.16), (-3.44, -1.85)),
    )
    paths = VGroup(*(light_path([xy(*p) for p in path], GREEN, 5.2 if i in (0, 3, 6) else 3.4)
                     for i, path in enumerate(branches)))
    return VGroup(plane, paths, soma)


def nearby_response(x):
    """Schematic sigmoid anchored to the 3.3 mV threshold and 246% enhancement
    reported by Polsky et al. (doi:10.1038/nn1253, pp. 622–623). The threshold
    criterion is y/x = 1.25. A smooth step toward the response scale 3.46 × 3.3
    illustrates saturation with the low-input linear limit.
    """
    threshold = 3.3
    plateau = threshold * 3.46
    fraction = (0.25 * threshold) / (plateau - threshold)
    slope = 2.0 / threshold
    decay = np.exp(slope * threshold)
    threshold_odds = fraction * decay / (decay - 1 - fraction * decay)
    midpoint = threshold - np.log(threshold_odds) / slope
    fraction_at_zero = 1 / (1 + np.exp(slope * midpoint))
    step = 1 / (1 + np.exp(-slope * (x - midpoint)))
    blend = max(0, (step - fraction_at_zero) / (1 - fraction_at_zero))
    return x + (plateau - x) * blend


class S09Polsky(SpokenScene):
    def construct(self):
        skin, follicles, trunk, roots, endings = follicle_scene()
        snapshot = VGroup(skin, follicles, trunk, roots, endings)
        self.add(snapshot, label("One neuron", -4.52, -3.12, GREEN),
                 label("Multiple endings", 2.42, -3.12, GREEN))
        sheet, dendrites, soma = pyramidal_slice()
        self.at("confocal imaging open")
        self.play(*[FadeOut(m) for m in self.mobjects],
                  FadeIn(sheet, scale=1.08), run_time=1.63)
        scan = Line(xy(-5.91, 1.87), xy(-1.05, 1.87), color=TEAL, stroke_width=4)
        self.add(scan)
        citation = label("Polsky, Mel & Schiller 2004", -3.15, 3.17, GOLD)
        self.at("in 2004")
        self.play(scan.animate.shift(DOWN * 3.33), FadeIn(citation),
                  LaggedStart(FadeIn(soma), Create(dendrites), lag_ratio=0.25),
                  run_time=2.48)
        self.at("thin dendrites")
        branch = light_path([xy(-3.16, -0.36), xy(-2.60, -0.20), xy(-1.87, 0.23),
                             xy(-1.27, 0.35)], YELLOW, 4.4)
        self.play(FadeOut(scan), Create(branch),
                  sheet.animate.set_fill("#394f54", opacity=0.94), run_time=1.35)
        self.at("in rat neocortex")
        tissue = label("Rat neocortex slice", -3.50, -2.66)
        self.play(FadeIn(tissue), sheet.animate.set_fill(TISSUE_TOP, 0.9), run_time=1.17)

        self.at("stimulated two sites")
        specimen_parts = VGroup(sheet, dendrites, soma, branch)
        anchor = xy(-6.20, 0)
        magnification = 1.27
        offset = RIGHT * 0.30
        original_sites = (xy(-2.45, -0.11), xy(-1.87, 0.23))
        zoomed_sites = [anchor + (p - anchor) * magnification + offset for p in original_sites]
        a, b = [speck(p, YELLOW, 0.12) for p in zoomed_sites]
        self.play(specimen_parts.animate.scale(magnification, about_point=anchor).shift(offset),
                  FadeIn(a), FadeIn(b), run_time=1.04)
        self.at("sites alone")
        self.play(Succession(Indicate(a, color=YELLOW, scale_factor=2.25),
                             Indicate(b, color=YELLOW, scale_factor=2.25)), run_time=1.30)
        self.at("then together")
        self.play(Indicate(a, color=YELLOW, scale_factor=2.25),
                  Indicate(b, color=YELLOW, scale_factor=2.25), run_time=0.83)
        self.play(specimen_parts.animate.shift(-offset).scale(1 / magnification, about_point=anchor),
                  a.animate.scale(1 / magnification).move_to(original_sites[0]),
                  b.animate.scale(1 / magnification).move_to(original_sites[1]), run_time=0.64)

        plot = Plot(box=(1.79, 6.02, -2.00, 2.23), xr=(0, 13), yr=(0, 13),
                    xlabel="Sum of separate responses", label_size=28)
        y_label = T("Response to both together", 28, TEXT).rotate(PI / 2)
        y_label.move_to(xy(1.19, 0.13))
        diagonal = DashedLine(plot.pt(0, 0), plot.pt(13, 13), color=GREY, stroke_width=3,
                              dash_length=0.17)
        tag = scope_tag(size=28, color=TEXT)
        self.at("on one branch")
        self.play(Create(plot.axes), FadeIn(plot.xlabel), FadeIn(y_label), FadeIn(tag), run_time=0.80)
        self.play(Create(diagonal), run_time=0.62)
        self.at("in an s shape")
        t = ValueTracker(0.02)
        trace = plot.live_curve(nearby_response, t, color=YELLOW, width=5)
        dot = plot.dot(t.get_value, lambda: nearby_response(t.get_value()),
                       color=YELLOW, ring=YELLOW, radius=0.08)
        key = label("Nearby", 2.99, 2.82, YELLOW, 28)
        self.add(trace, dot)
        self.play(FadeIn(key), t.animate.set_value(3.3), run_time=1.28, rate_func=linear)
        self.at("then steep")
        self.play(t.animate.set_value(8.35), run_time=0.87, rate_func=linear)
        self.play(t.animate.set_value(12.9), run_time=1.10, rate_func=linear)
        self.at("distant inputs")
        distant = label("Distant", 4.97, 2.82, BLUE, 28)
        points = VGroup(*(Dot(plot.pt(v, v), color=BLUE, radius=0.095)
                          for v in (2.2, 4.1, 6.0, 8.8, 11.4)))
        self.play(FadeOut(dot), FadeOut(branch), b.animate.move_to(xy(-5.10, 0.12)),
                  sheet.animate.set_fill("#385f64", opacity=0.95), FadeIn(distant),
                  LaggedStart(*[FadeIn(p, scale=0.4) for p in points], lag_ratio=0.28),
                  run_time=1.48)
        self.at("thin branches as separate")
        other = light_path([xy(-3.83, -0.25), xy(-4.39, -0.15), xy(-5.10, 0.12),
                            xy(-5.62, 0.47)], BLUE, 4.2)
        self.play(Create(other), Indicate(a, color=YELLOW, scale_factor=1.45), run_time=1.01)
        self.finish()


def tracheal_mount():
    sheet = face([xy(-6.15, -2.48), xy(5.40, -2.48), xy(6.12, 2.42), xy(-5.43, 2.42)],
                 TISSUE_FACE, 0.94)
    texture = VGroup()
    for j, x in enumerate(np.linspace(-5.25, 4.95, 15)):
        y = -1.72 + (j % 3) * 0.20
        texture.add(Ellipse(width=0.62, height=0.30, stroke_color=TISSUE_EDGE, stroke_width=1.2,
                            fill_color=TISSUE_TOP, fill_opacity=0.9).rotate(0.25).move_to(xy(x, y)))
    return VGroup(sheet, texture)


def lymphatics():
    left = [(-5.38, -0.28), (-5.30, 0.46), (-4.68, 0.94), (-3.79, 1.05),
            (-2.97, 0.78), (-2.0, 0.72), (-0.35, 0.56), (0.19, 0.70),
            (0.92, 1.18), (2.05, 1.50), (5.36, 1.47), (5.36, -0.62),
            (2.05, -0.65), (0.92, -0.35), (0.19, 0.03), (-0.35, 0.10),
            (-2.05, -0.30), (-2.96, -0.55), (-3.88, -0.95), (-4.79, -0.89)]
    wall = face([xy(*p) for p in left], GREEN, 0.23, stroke=GREEN, width=2.7)
    flaps, buttons = VGroup(), VGroup()
    for x, y, height_scale in ((-4.72, -0.04, 1), (-3.84, 0.005, 1), (-2.96, 0.05, 0.87),
                               (-2.08, 0.15, 0.62), (-1.20, 0.22, 0.40)):
        def flap_point(dx, dy):
            return xy(x + dx, y + height_scale * dy)

        # Junction segments sit along flap sides, leaving the tips free.
        flaps.add(face([flap_point(-.46, .25), flap_point(.10, .59), flap_point(.57, .27),
                        flap_point(.29, -.08), flap_point(-.19, -.03)],
                       GREEN, 0.31, stroke=GREEN, width=1.9))
        flaps.add(face([flap_point(-.43, -.34), flap_point(-.07, .07), flap_point(.21, .03),
                        flap_point(.45, -.35), flap_point(.01, -.59)],
                       GREEN, 0.20, stroke=GREEN, width=1.9))
        p, q = flap_point(-.40, -.30), flap_point(-.22, -.11)
        buttons.add(light_path([p, q], PURPLE, 6.4))
        p, q = flap_point(.31, .31), flap_point(.47, .43)
        buttons.add(light_path([p, q], PURPLE, 6.4))
    zipper_points = [(0.73, .40), (1.45, .57), (2.10, .44), (2.82, .57),
                     (3.49, .44), (4.18, .57), (5.35, .46)]
    zipper = light_path([xy(*p) for p in zipper_points], PURPLE, 6)
    return wall, flaps, buttons, zipper


class S10Baluk(SpokenScene):
    def construct(self):
        mount = tracheal_mount()
        tag = scope_tag(size=28, color=TEXT)
        self.add(mount, tag)
        self.at("in 2007")
        scan = Line(xy(-5.24, 2.27), xy(-4.60, -2.29), color=TEAL, stroke_width=5)
        self.add(scan)
        cite = label("Baluk et al. 2007", -4.36, 3.13, GOLD)
        self.play(FadeIn(cite), scan.animate.shift(RIGHT * 2.6), run_time=2.27)
        site = label("Mouse trachea whole mount", 1.59, 3.13)
        self.at("intact sheets")
        self.play(FadeIn(site), scan.animate.shift(RIGHT * 4.6), run_time=2.40)
        wall, flaps, buttons, zipper = lymphatics()
        self.at("how fluid enters")
        self.play(FadeIn(wall), scan.animate.shift(RIGHT * 2.65), run_time=1.9)
        self.play(FadeOut(scan), run_time=0.49)

        self.at("in the first")
        initial = label("Blind-ended vessel", -3.45, 1.91, GREEN)
        self.play(FadeIn(initial), GrowFromCenter(flaps),
                  wall.animate.set_fill(GREEN, opacity=0.37), run_time=1.37)
        self.at("joined by short")
        self.play(LaggedStart(*[Create(b) for b in buttons], lag_ratio=0.16),
                  wall.animate.set_fill(GREEN, opacity=0.21), run_time=1.51)
        length = label("About 3.2 µm", -3.48, -2.16, PURPLE)
        self.at("about 3 .2 micrometers")
        self.play(FadeIn(length), Indicate(buttons, color=PURPLE, scale_factor=1.02),
                  mount[0].animate.set_fill("#374e59", opacity=0.94), run_time=1.46)

        self.at("loose flaps")
        loose = label("Loose flaps", -3.48, -2.16, GREEN)
        self.play(swap(length, loose, 0.88), Indicate(flaps, color=GREEN, scale_factor=1.012),
                  mount[0].animate.set_fill(TISSUE_FACE, opacity=0.94), run_time=1.46)

        self.at("larger collecting vessels")
        collecting = label("Collecting vessel", 3.32, 1.93, GREEN)
        self.play(FadeIn(collecting), run_time=0.62)
        self.at("had continuous")
        self.play(Create(zipper), wall.animate.set_fill(GREEN, opacity=0.37), run_time=1.45)
        continuous = label("Continuous junction", 3.00, -2.16, PURPLE)
        self.play(FadeIn(continuous), run_time=0.58)

        self.at("from that structure alone")
        inference = label("Inferred from structure", 0.04, -3.08, GOLD)
        self.play(FadeOut(loose), FadeIn(inference),
                  wall.animate.set_fill(GREEN, opacity=0.23), run_time=0.85)
        arrows = VGroup()
        for x in (-4.42, -3.54, -2.65):
            arrow = Arrow(xy(x - .25, -1.48), xy(x, -.19), buff=0, color=YELLOW,
                          stroke_width=4, tip_length=0.16)
            arrows.add(DashedVMobject(arrow, num_dashes=8))
        self.at("proposed fluid enters")
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.28), run_time=1.85)
        self.finish()


class S11Schafer(SpokenScene):
    def construct(self):
        thalamus_view = (0, -0.05, 1.05)
        shell = tissue_shell(thalamus_view)
        colours = emitters(thalamus_view)
        tag = scope_tag(size=28, color=TEXT)
        credit = label("Schafer et al. 2012", -3.96, 3.16, GOLD)
        thalamus = label("Mouse visual thalamus", 2.54, 3.16)
        self.add(shell, tag)
        self.at("in 2012")
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in colours], lag_ratio=0.09),
                  FadeIn(credit), shell[2].animate.set_fill("#4f435b", opacity=0.89),
                  run_time=2.68)
        self.at("nerve endings")
        red = VGroup(*[p for p, entry in zip(colours, OUTER) if entry[1] == RED])
        blue = VGroup(*[p for p, entry in zip(colours, OUTER) if entry[1] == BLUE])
        left_eye = label("One eye", -4.46, -3.18, RED)
        other_eye = label("Other eye", -1.54, -3.18, BLUE)
        self.play(Indicate(red, color=RED, scale_factor=1.025), FadeIn(left_eye),
                  shell[2].animate.set_fill("#614251", opacity=0.89), run_time=1.03)
        self.play(Indicate(blue, color=BLUE, scale_factor=1.025), FadeIn(other_eye),
                  shell[2].animate.set_fill(TISSUE_TOP, opacity=0.75), run_time=1.19)

        self.at("they rebuilt green")
        layers = VGroup(*(section(thalamus_view, height) for height in (-0.94, -0.41, 0.12, 0.76)))
        model = reconstructed(thalamus_view, outer=False)
        self.play(LaggedStart(*[FadeIn(p) for p in layers], lag_ratio=0.25), run_time=1.95)
        self.play(FadeIn(model), FadeOut(layers),
                  LaggedStart(*[FadeOut(p, scale=0.5) for p in colours], lag_ratio=0.09),
                  run_time=1.46)
        self.at("visual thalamus")
        micro = label("Microglia", 0.28, 1.43, GREEN)
        self.play(FadeIn(thalamus), FadeIn(micro), run_time=0.68)

        stained = compartments(thalamus_view)
        self.at("pieces of those endings")
        self.play(LaggedStart(*[GrowFromCenter(a) for a in stained], lag_ratio=0.5),
                  shell[0].animate.set_fill("#4f465c", opacity=0.91), run_time=1.64)
        model[1].set_z_index(1)
        digestive = label("Digestive compartments", 3.20, -3.18, PURPLE)
        self.at("inside digestive")
        self.play(swap(tag, digestive, 1.04), Indicate(stained, color=PURPLE, scale_factor=1.04),
                  shell[0].animate.set_fill(TISSUE_FACE, opacity=0.90), run_time=1.29)
        self.at("relatively more")
        quiet = label("Silenced eye", -4.46, -3.18, RED)
        kept = [p for p, entry in zip(model[1], INNER) if entry[1] == RED]
        self.play(swap(left_eye, quiet, 0.55), *[p.animate.scale(1.19) for p in kept],
                  shell[0].animate.set_fill("#4d3a4d", opacity=0.91), run_time=0.80)
        self.at("by rejecting blur")
        restored = specimen(OPTICAL)
        self.play(FadeOut(credit), FadeOut(thalamus), FadeOut(micro), FadeOut(digestive),
                  FadeOut(other_eye), FadeOut(quiet), run_time=0.27)
        self.play(FadeOut(stained), FadeOut(model), Transform(shell, restored[0]),
                  FadeIn(restored[1]), FadeIn(restored[2]), run_time=0.85)
        lens = objective(PIN_X, LENS_Y)
        beam = illumination(0, FOCUS_Z)
        accepted = focused_return(0, FOCUS_Z)
        self.at("one pinhole")
        self.play(FadeIn(lens), FadeIn(aperture()), FadeIn(beam), Create(accepted), run_time=1.14)
        optical_slices = VGroup(*(section(OPTICAL, z) for z in (-1.02, -0.54, FOCUS_Z, 0.51)))
        self.at("crowded tissue")
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.07) for p in optical_slices], lag_ratio=0.40),
                  run_time=1.70)
        self.at("space", lead=-0.86)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.75)
        self.finish()


class S12End(EndCard):
    LINE = "A pinhole rejects blur to slice thick tissue in three dimensions."
