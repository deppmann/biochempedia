"""Nerve injury and axotomy, timed to the supplied Kokoro word alignment.

Colors follow the patch-clamp map: grey anatomy, blue apparatus, yellow signal,
green regrowth or intact function, red damage or pain, purple named proteins
and cell identity, teal the nerve's own tissue, and gold dates and questions.
All anatomy, elapsed-time indicators and threshold gauges are schematic.
"""
from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
TISSUE = "#354957"
NERVE = "#3A636B"
CORD = "#485367"
HORN = "#6A667E"
PAW = "#6D565D"
REFLEX_LIFT = 0.52
LABEL_Y = 2.97
QUESTION = "What can that paw lift NOT tell you?"
CREDIT_P = "Peirs and colleagues, 2015"
CREDIT_J = "Petitjean and colleagues, 2015"


def pt(x, y):
    return np.array([x, y, 0.0])


def spline(points, color, width):
    path = VMobject(stroke_color=color, stroke_width=width)
    path.set_points_smoothly([pt(*p) for p in points])
    return path


def tissue(points, fill, edge=GREY, width=2.5):
    shape = spline([*points, points[0]], edge, width)
    shape.set_fill(fill, 1)
    return shape


def heading(text, color=TEXT):
    return fit_text(text, max_w=10.0, size=36, min_size=28, color=color).move_to(pt(-0.3, LABEL_Y))


def tag(text, at, color=TEXT, size=30):
    return T(text, size, color).move_to(pt(*at))


def schematic():
    return scope_tag("schematic", size=28, color=TEXT).move_to(pt(5.54, -3.4))


def soma(x, y, radius, color=TEAL, fill=NERVE):
    centre = pt(x, y)
    outline = Circle(radius=radius, stroke_color=color, stroke_width=3,
                     fill_color=fill, fill_opacity=1).move_to(centre)
    nucleus = Circle(radius=radius * 0.34, stroke_width=1.7, stroke_color=color,
                     fill_color=color, fill_opacity=0.38).move_to(centre + UP * radius * 0.10)
    return VGroup(outline, nucleus)


def paw(centre, scale=1, raised=0):
    """The same hind paw, with the toes at the far left, at every magnification."""
    shape = tissue([
        (-1.23, -0.39), (-1.67, -0.34), (-1.70, -0.17), (-1.26, -0.02),
        (-1.68, 0.02), (-1.73, 0.19), (-1.18, 0.32), (-1.57, 0.41),
        (-1.52, 0.59), (-0.78, 0.63), (-0.33, 0.90), (0.16, 1.54),
        (0.73, 1.67), (0.99, 1.41), (0.65, 0.77), (0.70, 0.20),
        (0.44, -0.28), (-0.34, -0.43),
    ], PAW)
    pad = Ellipse(width=0.76, height=0.27, stroke_width=2, stroke_color="#D49B9A",
                  fill_color="#AA777B", fill_opacity=1).rotate(0.06).move_to(pt(-0.67, -0.19)).set_z_index(1)
    g = VGroup(shape, pad).scale(scale, about_point=ORIGIN).shift(pt(*centre))
    return g.shift(UP * raised)


def cord(centre, scale=1):
    """Section through the cord, with the dorsal side at the top."""
    outline = tissue([
        (0.0, 1.91), (-0.67, 2.03), (-1.36, 1.62), (-1.76, 0.86),
        (-1.78, -0.19), (-1.39, -1.18), (-0.61, -1.79), (-0.16, -1.63),
        (0, -1.36), (0.18, -1.65), (0.72, -1.72), (1.47, -1.12),
        (1.80, -0.23), (1.72, 0.93), (1.34, 1.62), (0.65, 1.99),
    ], CORD)
    horns = tissue([
        (0, 0.36), (-0.4, 0.58), (-0.75, 1.26), (-1.14, 1.48),
        (-1.05, 0.86), (-0.78, 0.26), (-0.63, -0.20), (-1.13, -0.96),
        (-0.83, -1.16), (-0.24, -0.76), (0, -0.45), (0.24, -0.76),
        (0.83, -1.16), (1.13, -0.96), (0.63, -0.20), (0.78, 0.26),
        (1.05, 0.86), (1.14, 1.48), (0.75, 1.26), (0.4, 0.58),
    ], HORN, "#9C92AC", 2)
    return VGroup(outline, horns).scale(scale, about_point=ORIGIN).shift(pt(*centre))


def brain():
    """The diagram's separate brain circuit, kept clear of the corner brand mark."""
    return tissue([
        (-0.94, 0.01), (-0.88, 0.36), (-0.57, 0.53), (-0.23, 0.54),
        (0.05, 0.66), (0.43, 0.52), (0.78, 0.47), (0.95, 0.14),
        (0.79, -0.17), (0.49, -0.21), (0.40, -0.47), (0.23, -0.47),
        (0.16, -0.18), (-0.26, -0.26), (-0.70, -0.24),
    ], CORD).scale(0.85, about_point=ORIGIN).shift(pt(3.65, 3.05))


# One geometry for the overview. Its close-ups reuse the paw and cord shapes.
LIMB = [(-5.20, -0.95), (-4.42, -0.59), (-3.51, 0.00), (-2.68, 0.20),
        (-1.8, 0.30), (-0.8, 0.61), (0.36, 0.86), (1.08, 0.78), (2.29, 0.62), (3.35, 0.74)]
BRANCHES = [
    [(-5.64, -0.45), (-4.71, -0.23), (-4.14, -0.22), (-3.51, 0.00)],
    [(-5.48, -1.37), (-4.87, -1.18), (-4.23, -0.59), (-3.51, 0.00)],
]


def part(path, a, b, color, width):
    section = path.copy()
    section.pointwise_become_partial(path, a, max(a + 0.0001, b))
    return section.set_fill(opacity=0).set_stroke(color, width)


def overview(*, spared=False, limb_gap=False, cord_gap=False, lift=0, lit=False, brain_view=False):
    animal = paw((-4.8, -1.06), scale=1.16, raised=lift)
    spinal = cord((4.27, -0.19), 1.24)
    # The branch junction moves with the paw. Bend into the stationary trunk.
    limb_points = [(x, y + lift * weight)
                   for (x, y), weight in zip(LIMB, (1, 1, 1, 0.45, 0, 0, 0, 0, 0, 0))]
    nerve = spline(limb_points, TEAL, 6)
    cell = soma(0.13, 1.71, 0.84)
    root = spline([(0.13, 1.05), (0.27, 0.90), (0.36, 0.86)], TEAL, 7)
    branches = VGroup()
    for points in BRANCHES:
        branch = spline([(x, y + lift) for x, y in points], TEAL, 5)
        if spared:
            branches.add(part(branch, 0, 0.37, TEAL, 5), part(branch, 0.56, 1, TEAL, 5))
        else:
            branches.add(branch)
    central = spline([(3.35, 0.74), (3.76, 0.94), (4.04, 1.16), (4.15, 1.02)], TEAL, 8)
    if limb_gap:
        sheath = VGroup(part(nerve, 0, 0.35, NERVE, 38), part(nerve, 0.49, 1, NERVE, 38))
        limb = VGroup(part(nerve, 0, 0.35, TEAL, 6), part(nerve, 0.49, 1, TEAL, 6))
    else:
        limb = nerve.copy()
        sheath = nerve.copy().set_stroke(NERVE, 38)
    if cord_gap:
        central_display = VGroup(part(central, 0, 0.45, TEAL, 8), part(central, 0.61, 1, TEAL, 8))
    else:
        central_display = central.copy()
    reflex = soma(4.15, 1.02, 0.33, RED if lit else PURPLE, "#9A535B" if lit else HORN)
    wiring = VGroup(branches, sheath, limb)
    g = VGroup(spinal, animal, wiring, root, cell, central_display, reflex)
    g.animal, g.nerve, g.central, g.cell, g.reflex = animal, nerve, central, cell, reflex
    g.wiring, g.limb, g.sheath, g.horns = wiring, limb, sheath, spinal[1]
    if brain_view:
        g.brain = brain()
        g.add(g.brain)
    return g


def wave(scene, path, start, end, seconds, color=YELLOW, width=15, during=()):
    """A traveling impulse rides its axon, with a soft leading glow."""
    progress = ValueTracker(start)
    length = 0.21 if end >= start else -0.21

    def band():
        v = progress.get_value()
        a, b = sorted([np.clip(v - length, 0, 1), v])
        a, b = min(a, 0.9999), max(b, 0.0001)
        dot = Dot(path.point_from_proportion(v), color=color, radius=0.19)
        aura = part(path, a, b, color, width + 34).set_stroke(opacity=0.43)
        return VGroup(aura, part(path, a, b, color, width), dot)
    moving = always_redraw(band)
    scene.add(moving)
    scene.play(progress.animate.set_value(end), *during, rate_func=linear, run_time=seconds)
    moving.clear_updaters()
    scene.play(FadeOut(moving), run_time=0.22)


def axon(*, broken=False, debris=False, central=False):
    """One magnified axon with the connected soma on the proximal side."""
    channel = tissue([
        (-5.92, 0.30), (-5.62, 1.48), (-4.14, 1.80), (-1.77, 1.57),
        (0.88, 1.90), (3.07, 1.99), (4.30, 1.40), (4.76, 0.50),
        (4.28, -0.59), (2.92, -1.08), (0.57, -0.86), (-2.25, -1.13),
        (-4.78, -1.00), (-5.72, -0.64),
    ], CORD if central else TISSUE, width=2.2)
    path = spline([(-5.54, 0.18), (-4.25, 0.27), (-2.83, 0.53), (-1.32, 0.39),
                   (0.12, 0.30), (1.43, 0.48), (2.83, 0.59), (4.04, 0.56)], TEAL, 29)
    left = part(path, 0, 0.424, TEAL, 29)
    right = part(path, 0.543, 1, TEAL, 29)
    cell = soma(4.54, 0.61, 1.70)
    collar = spline([(3.05, 0.58), (3.39, 0.52), (3.93, 0.54)], TEAL, 29)
    fragments = VGroup()
    for i, a in enumerate(np.linspace(0.013, 0.387, 10)):
        tint = RED if i % 3 == 0 else TEAL
        fragment = part(path, a, a + (0.014 if i % 2 else 0.024), tint, 10 + i % 4 * 3)
        fragment.shift(UP * (0.24 + i % 4 * 0.16) * (-1 if i % 2 else 1))
        fragment.rotate((-1 if i % 2 else 1) * 0.39)
        fragments.add(fragment)
    g = VGroup(channel, collar, cell)
    if broken:
        g.add(right, fragments if debris else left)
    else:
        g.add(path.copy())
    g.path, g.left, g.right, g.fragments, g.cell = path, left, right, fragments, cell
    return g


def growing(path, tracker, start=0.545):
    def tip():
        value = tracker.get_value()
        return VGroup(part(path, value, start, GREEN, 21),
                      Dot(path.point_from_proportion(value), radius=0.22, color=GREEN))
    return always_redraw(tip)


def scrubber(progress, left, right):
    """An elapsed-time band whose endpoints are stated time windows."""
    x0, x1, y = -4.95, 3.67, -2.03
    track = Line(pt(x0, y), pt(x1, y), stroke_color=GREY, stroke_width=5)
    ticks = VGroup(*[Line(pt(x, y - 0.13), pt(x, y + 0.13), color=GREY, stroke_width=3) for x in (x0, x1)])

    def elapsed_bar():
        width = max(0.001, (x1 - x0) * progress.get_value())
        return Rectangle(width=width, height=0.18, stroke_width=0,
                         fill_color=GOLD, fill_opacity=0.80).move_to(pt(x0 + width / 2, y))

    fill = always_redraw(elapsed_bar)
    marker = always_redraw(lambda: Dot(pt(interpolate(x0, x1, progress.get_value()), y),
                                       radius=0.13, color=GOLD))
    a = tag(left, (x0, -2.66), size=28)
    b = tag(right, (x1, -2.66), size=28)
    return VGroup(track, ticks, fill, marker, a, b)


def brake(at, opacity=1):
    x, y = at
    stop = VGroup(Line(pt(x, y + 0.55), pt(x, y), color=PURPLE, stroke_width=8),
                  Line(pt(x - 0.32, y), pt(x + 0.32, y), color=PURPLE, stroke_width=8))
    return stop.set_opacity(opacity)


def circuit_frame(*, raised=False, activated=False, brain_view=False):
    lift = REFLEX_LIFT if raised else 0
    g = overview(spared=True, lift=lift, lit=activated, brain_view=brain_view)
    g.stop = brake((3.72, 0.77), 0.3 if activated else 1)
    if activated:
        g.horns.set_fill("#795868")
    g.probe = filament(-5.82, -1.60 + lift, slim=True, height=1.15)
    g.add(g.stop, g.probe)
    return g


def threshold_dial(value, centre=(3.80, -1.13), radius=1.56):
    g = dial(value, center=pt(*centre), radius=radius, color=BLUE, label="")
    g.remove(g[3])  # The narration gives no force values.
    sector = always_redraw(lambda: Sector(radius=radius - 0.10, start_angle=PI,
                                            angle=-PI * value.get_value(), arc_center=pt(*centre),
                                            stroke_width=0, fill_color=BLUE, fill_opacity=0.54))
    label = tag("Withdrawal threshold", (centre[0], centre[1] - 0.47), TEXT, size=29)
    return VGroup(sector, g, label)


def filament(x, tip, *, slim=True, height=2.0):
    color = BLUE
    return VGroup(spline([(x, tip - height), (x, tip - height * 0.58), (x + 0.06, tip - 0.18),
                          (x + 0.15, tip)], color, 3 if slim else 7),
                  RoundedRectangle(width=0.29 if slim else 0.43, height=0.32,
                                   corner_radius=0.09, stroke_color=BLUE, stroke_width=2,
                                   fill_color=NERVE, fill_opacity=1).move_to(pt(x, tip - height)))


def paw_assay(*, cut=True):
    animal = paw((-3.48, -0.33), 1.52)
    rear = spline([(-5.62, 0.30), (-4.92, 0.30), (-4.04, 0.58), (-3.04, 1.44), (-2.25, 1.78), (-0.76, 1.76)],
                  NERVE, 27)
    tracks = [
        [(-5.68, 0.47), (-4.86, 0.47), (-4.11, 0.73), (-3.08, 1.48)],
        [(-5.50, 0.13), (-4.70, 0.15), (-3.97, 0.57), (-3.08, 1.48)],
        [(-5.26, -0.14), (-4.73, -0.13), (-4.00, 0.29), (-3.08, 1.48)],
    ]
    nerves = [spline(points, TEAL, 7) for points in tracks]
    visible = VGroup(*nerves) if not cut else VGroup(
        *[VGroup(part(path, 0, 0.31, TEAL, 7), part(path, 0.52, 1, TEAL, 7)) for path in nerves[:2]],
        nerves[2].copy().set_stroke(GREEN, 8))
    trunk = spline([(-3.08, 1.48), (-2.24, 1.76), (-1.14, 1.76)], TEAL, 8)
    grid = VGroup(*[Line(pt(-6.12 + i * 0.40, -1.12), pt(-5.80 + i * 0.40, -0.93),
                         color=GREY, stroke_width=2) for i in range(13)],
                  Line(pt(-6.10, -1.12), pt(-1.25, -1.12), color=GREY, stroke_width=2.8),
                  Line(pt(-5.80, -0.93), pt(-0.96, -0.93), color=GREY, stroke_width=2.8))
    g = VGroup(grid, animal, rear, trunk, visible).shift(DOWN * 0.20)
    g.animal, g.rear, g.visible, g.nerves = animal, rear, visible, nerves
    g.trunk = trunk
    return g


GANGLION_POINTS = [(-0.97, 0.90), (0.73, 0.99), (-1.17, -0.87), (0.63, -0.78), (1.71, 0.04)]
IDENTITY_COLORS = [PURPLE, ORANGE, BLUE, PURPLE, ORANGE]


def ganglion(*, marks=True, cut=True):
    shell = tissue([
        (-2.47, 0.17), (-1.95, 1.38), (-0.96, 2.11), (0.49, 2.20),
        (1.77, 1.64), (2.49, 0.38), (2.49, -0.79), (1.62, -1.86),
        (0.32, -2.26), (-1.21, -1.90), (-2.33, -0.96),
    ], TISSUE)
    left = spline([(-6.03, -0.40), (-5.39, -0.46), (-4.55, -0.45), (-4.36, -0.44)], TEAL, 12)
    right = spline([(-3.60, -0.43), (-3.01, -0.50), (-2.54, -0.43), (-1.92, -0.25)], TEAL, 12)
    output = spline([(2.02, -0.17), (3.07, -0.37), (4.38, -0.33), (5.86, 0.10)], NERVE, 25)
    tiny_paw = paw((-5.68, -0.55), 0.57)
    cells, dots, rings = VGroup(), VGroup(), VGroup()
    for (x, y), color in zip(GANGLION_POINTS, IDENTITY_COLORS):
        tint = interpolate_color(ManimColor(NERVE), ManimColor(color), 0.47) if marks else NERVE
        cells.add(soma(x, y, 0.62, fill=tint))
        dots.add(Dot(pt(x, y + 0.055), radius=0.21, color=color).set_z_index(2))
    for i in (0, 3):
        x, y = GANGLION_POINTS[i]
        rings.add(Circle(radius=0.69, stroke_color=GOLD, stroke_width=5).move_to(pt(x, y)))
    dots.set_opacity(1 if marks else 0.13)
    stem = spline([(-3.63, -0.43), (-4.42, -0.48), (-5.20, -0.50), (-5.65, -0.45)], GREEN, 13)
    g = VGroup(tiny_paw, left, right, output, shell, cells, dots)
    bridge = spline([(-4.38, -0.44), (-3.98, -0.44), (-3.57, -0.43)], TEAL, 12)
    if not cut:
        g.add(bridge)
    g.cells, g.dots, g.rings, g.stem, g.shell, g.bridge = cells, dots, rings, stem, shell, bridge
    return g


def dorsal_horn(*, vglut=False, activated=False):
    """The same local circuit for the dorsal-horn experiments and their reversal."""
    section = cord((-2.07, -0.11), 1.31)
    afferent = spline([(-6.15, 0.94), (-5.63, 1.02), (-4.85, 0.89), (-4.14, 0.57),
                       (-3.59, 0.48), (-2.41, 0.57), (-1.28, 0.30)], TEAL, 9)
    receiver = soma(-1.18, 0.26, 0.57, TEAL, NERVE)
    pv_cell = soma(-2.29, 1.52, 0.50, GREEN if activated else PURPLE, HORN)
    stop = brake((-1.57, 0.78))
    pv_link = spline([(-1.89, 1.36), (-1.63, 1.27), (-1.57, 1.19)], PURPLE, 6)
    if activated:
        pv_cell[0].set_fill(GREEN, 0.5)
        stop.set_color(GREEN)
        pv_link.set_color(GREEN)
    paw_icon = paw((3.82, 0.93), 0.90)
    probe = filament(3.10, 0.57, slim=True, height=0.86)
    g = VGroup(section, afferent, receiver, paw_icon, probe, pv_cell, pv_link, stop)
    if vglut:
        g.vglut = boxed_label("VGLUT3", PURPLE, size=28, min_size=28).move_to(pt(-4.82, -2.62))
        g.add(g.vglut)
    g.pv, g.link, g.stop, g.afferent, g.receiver = pv_cell, pv_link, stop, afferent, receiver
    g.animal, g.probe, g.horns = paw_icon, probe, section[1]
    return g


class S01Hook(SpokenScene):
    def construct(self):
        g = overview(limb_gap=True, cord_gap=True)
        self.add(g, schematic())
        extension = ValueTracker(0.487)
        tip = growing(g.nerve, extension, start=0.49)
        self.at("cut limb nerve", lead=0.6)
        self.add(tip)
        self.play(extension.animate.set_value(0.36), run_time=1.56)
        self.at("spinal axons mostly stall", lead=0.05)
        stopped = Dot(g.central.point_from_proportion(0.45), color=RED, radius=0.18)
        self.play(FadeIn(stopped, scale=0.6), run_time=0.55)
        self.play(g.horns.animate.set_fill("#986475"), run_time=1.57)
        self.at("light touch", lead=0.60)
        touch = Circle(radius=0.25, color=YELLOW, stroke_width=5).move_to(pt(-5.61, -1.55))
        raised = overview(limb_gap=True, cord_gap=True, lift=0.38)
        resting_wiring = g.wiring.copy()
        self.play(FadeIn(touch, scale=0.45), Transform(g.animal, raised.animal),
                  Transform(g.wiring, raised.wiring), run_time=0.45)
        self.play(FadeOut(touch), g.animal.animate.shift(DOWN * 0.38),
                  Transform(g.wiring, resting_wiring), run_time=0.35)
        wave(self, g.nerve, 0.03, 0.97, 2.05, RED)
        self.at("labs cut or crush", lead=0.25)
        tip.clear_updaters()
        self.play(FadeOut(tip), FadeOut(stopped), g.horns.animate.set_fill(HORN), run_time=0.65)
        self.play(g.limb[0].animate.shift(LEFT * 0.20), g.sheath[0].animate.shift(LEFT * 0.20),
                  g.cell[0].animate.set_fill("#538590"), run_time=1.55)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Axotomy and nerve injury models"
    TITLE = "Cutting a Nerve to Watch Repair and Pain"

    def construct(self):
        g = overview().scale(0.86, about_point=ORIGIN).shift(DOWN * 0.95).fade(0.62)
        name = fit_text(self.TITLE, max_w=12.0, size=52, min_size=40, color=TEXT).move_to(pt(0, 2.23))
        lesson = tag(self.LESSON, (0, 1.51), GOLD, 29)
        path = g.nerve.copy().scale(0.86, about_point=ORIGIN).shift(DOWN * 0.95)
        self.add(g)
        self.play(FadeIn(name, shift=UP * 0.10), FadeIn(lesson), run_time=0.43)
        wave(self, path, 0.03, 0.98, 1.25, TEAL, 8)
        self.wait(0.10)


class S03Axotomy(SpokenScene):
    def construct(self):
        g = axon()
        self.add(g, schematic())
        whole = g[-1]
        self.at("cutting an axon")
        self.play(Circumscribe(part(g.path, 0.46, 0.52, TEAL, 29), color=RED, shape=Circle), run_time=1.02)
        cut = heading("Axotomy", RED)
        self.play(FadeIn(cut), run_time=0.50)
        self.at("severe crush splits", lead=0.6)
        self.play(ReplacementTransform(whole, VGroup(g.left, g.right)), run_time=0.84)
        prox = tag("Proximal", (1.75, 1.17), TEAL)
        dist = tag("Distal", (-3.43, 1.14), TEAL)
        self.at("the proximal piece", lead=0.23)
        self.play(FadeIn(prox), Indicate(g.cell[0], color=TEAL, scale_factor=1.05), run_time=1.62)
        self.at("the distal piece separates")
        self.play(FadeIn(dist), g.left.animate.shift(LEFT * 0.17), run_time=1.12)
        phase = heading("Mouse sciatic nerve")
        self.at("in mouse sciatic")
        self.play(swap(cut, phase, run_time=0.70), FadeOut(prox), FadeOut(dist), run_time=0.70)
        progress = ValueTracker(0)
        timebar = scrubber(progress, "Injury", "1½–2 days")
        self.play(FadeIn(timebar), run_time=0.57)
        latent = heading("Latent phase", GOLD)
        self.at("it looks normal", lead=0.0)
        self.play(swap(phase, latent, run_time=0.54), run_time=0.54)
        self.play(progress.animate.set_value(1), run_time=4.20, rate_func=linear)
        self.at("it breaks apart", lead=0.30)
        self.play(FadeOut(latent), run_time=0.28)
        self.play(FadeIn(heading("Distal breakdown", RED), run_time=0.43),
                  FadeOut(g.left, run_time=0.92),
                  LaggedStart(*[FadeIn(f, shift=f.get_center()[1] * UP * 0.22)
                                for f in g.fragments], lag_ratio=0.12, run_time=1.40))
        self.finish()


class S04RegrowVsStall(SpokenScene):
    def construct(self):
        g = axon(broken=True, debris=True)
        scope = schematic()
        peripheral = heading("Peripheral nerve", TEAL)
        progress = ValueTracker(0)
        timebar = scrubber(progress, "Days", "Weeks")
        self.add(g, scope, peripheral)
        self.at("debris clears")
        self.play(FadeIn(timebar), run_time=0.44)
        self.play(LaggedStart(*[FadeOut(f, shift=UP * (0.12 + 0.07 * (i % 3))) for i, f in enumerate(g.fragments)],
                              lag_ratio=0.18),
                  progress.animate.set_value(1), run_time=2.16)
        self.at("the proximal tip")
        growth = ValueTracker(0.539)
        tip = growing(g.path, growth)
        self.add(tip)
        self.play(growth.animate.set_value(0.40), rate_func=linear, run_time=2.17)
        self.at("human regrowth often", lead=0.55)
        human = heading("Humans · around 1 mm/day", GREEN)
        months = scrubber(progress, "Weeks", "Months")
        self.play(swap(peripheral, human, run_time=0.8), FadeOut(timebar), run_time=0.80)
        progress.set_value(0)
        self.play(FadeIn(months), run_time=0.44)
        self.play(progress.animate.set_value(1), growth.animate.set_value(0.065), rate_func=linear, run_time=3.30)
        self.at("in the spinal cord", lead=0.25)
        tip.clear_updaters()
        central = axon(broken=True, central=True)
        spinal = heading("Spinal cord", TEAL)
        self.play(FadeOut(g), FadeOut(tip), FadeOut(months), swap(human, spinal, run_time=0.75),
                  FadeIn(central), run_time=0.75)
        self.at("distal axons break")
        self.play(FadeOut(central.left, scale=0.84),
                  LaggedStart(*[FadeIn(f, scale=0.40) for f in central.fragments], lag_ratio=0.15),
                  central[0].animate.set_fill("#61697B"), run_time=2.50)
        self.at("clearing is slower")
        self.play(*[FadeOut(central.fragments[i], shift=UP * 0.15) for i in (1, 8)],
                  *[f.animate.shift(UP * (0.12 if i % 2 else -0.12))
                    for i, f in enumerate(central.fragments) if i not in (1, 8)],
                  central[0].animate.set_fill("#485367"), run_time=2.75)
        self.at("many central axons", lead=0.4)
        stall = Dot(central.path.point_from_proportion(0.543), color=RED, radius=0.20)
        self.play(FadeIn(stall, scale=0.4), run_time=0.62)
        self.play(Indicate(stall, color=RED, scale_factor=1.65),
                  central.cell[0].animate.set_fill("#617D88"), run_time=1.85)
        self.at("the fault in the neurons", lead=0.35)
        neuron = tag("Neuron?", (4.35, -1.86), TEAL)
        surroundings = tag("Surroundings?", (-2.99, -1.87), GOLD)
        self.play(FadeIn(neuron), Indicate(central.cell[0], color=TEAL, scale_factor=1.04), run_time=1.16)
        self.play(FadeIn(surroundings), central[0].animate.set_fill("#56637C"), run_time=2.12)
        self.at("controlled nerve injury", lead=0.25)
        closed = overview(limb_gap=True, cord_gap=True, lit=True)
        self.play(FadeOut(spinal), FadeOut(neuron), FadeOut(surroundings), run_time=0.25)
        residue = VGroup(*[f for i, f in enumerate(central.fragments) if i not in (1, 8)])
        self.play(FadeOut(central), FadeOut(residue), FadeOut(stall), FadeIn(closed), run_time=0.6)
        self.play(Create(part(closed.nerve, 0.38, 0.49, GREEN, 12)), run_time=1.25)
        wave(self, closed.central, 0.63, 0.99, 1.28, RED)
        self.finish()


class S05SparedNerveInjury(SpokenScene):
    def construct(self):
        g = paw_assay(cut=False)
        cut_view = paw_assay()
        title = heading("Spared nerve injury", TEAL)
        wide = overview(limb_gap=True, cord_gap=True, lit=True)
        self.add(wide, schematic())
        self.at("for lasting pain", lead=0)
        self.play(FadeOut(wide, shift=RIGHT * 0.32, scale=0.85), FadeIn(g, shift=LEFT * 0.48, scale=0.72),
                  run_time=1.42)
        self.at("labs use spared", lead=0.31)
        self.play(FadeIn(title), run_time=0.58)
        self.play(LaggedStart(*[Indicate(n, scale_factor=1.04, color=BLUE) for n in g.nerves],
                              lag_ratio=0.38), run_time=1.34)
        self.at("two branches to", lead=0.18)
        self.play(Indicate(g.nerves[0], color=RED, scale_factor=1.02),
                  Indicate(g.nerves[1], color=RED, scale_factor=1.02), run_time=1.0)
        self.at("are cut one", lead=0.42)
        selected = VGroup(*[part(n, 0.53, 0.65, RED, 15) for n in g.nerves[:2]])
        self.play(ReplacementTransform(g.visible, cut_view.visible), FadeIn(selected, scale=0.9),
                  g.animal[0].animate.set_fill("#B87881"), run_time=0.82)
        spared = tag("Spared", (-1.67, -0.35), GREEN)
        leader = Line(spared.get_left() + LEFT * 0.14, cut_view.visible[-1].point_from_proportion(0.68),
                      color=GREEN, stroke_width=3)
        self.at("one is spared", lead=0.40)
        self.play(FadeIn(spared), Create(leader), FadeOut(selected, scale=0.3),
                  g.animal[0].animate.set_fill(PAW), run_time=0.44)
        first = filament(-4.78, -1.60, height=1.58)
        second = filament(-4.78, -1.60, slim=False, height=1.58)
        self.at("calibrated von frei", lead=0.40)
        vf = heading("Calibrated von Frey filaments", BLUE)
        self.play(swap(title, vf, run_time=0.69), FadeOut(spared, run_time=0.35),
                  FadeOut(leader, run_time=0.35), FadeIn(first, shift=UP * 0.45), run_time=0.69)
        self.play(first.animate.shift(UP * 0.49), g.animal[1].animate.set_fill("#F6A3A2"),
                  rate_func=there_and_back, run_time=1.55)
        self.play(ReplacementTransform(first, second), run_time=0.58)
        self.play(second.animate.shift(UP * 0.49), g.animal[1].animate.set_fill("#F6A3A2"),
                  rate_func=there_and_back, run_time=1.45)
        self.at("many labs take")
        intensity = ValueTracker(0.76)
        gauge = threshold_dial(intensity)
        trials = tag("Paw lifts half the time", (3.78, -2.30), size=29)
        self.play(FadeIn(gauge), run_time=0.70)
        self.play(second.animate.shift(UP * 0.54), run_time=0.55)
        self.at("lifting the paw", lead=0.38)
        # At the threshold, show one lifted and one unlifted touch.
        moving_paw = (g.animal, g.rear, g.trunk, cut_view.visible)
        lift = UP * 0.35
        self.play(*(piece.animate.shift(lift) for piece in (*moving_paw, second)),
                  rate_func=there_and_back, run_time=1.08)
        self.play(second.animate.shift(DOWN * 0.54), run_time=0.44)
        self.play(second.animate.shift(UP * 0.54), rate_func=there_and_back, run_time=1.02)
        self.play(FadeIn(trials), run_time=0.60)
        self.at("days later it drops", lead=0.33)
        days = heading("Days after injury", GOLD)
        fine = filament(-4.78, -1.60, height=1.58)
        self.play(swap(vf, days, run_time=0.8), ReplacementTransform(second, fine),
                  intensity.animate.set_value(0.24), run_time=1.61)
        self.at("sign of allodynia", lead=0.3)
        allo = heading("Mechanical allodynia", RED)
        self.play(swap(days, allo, run_time=0.85), fine.animate.shift(UP * 0.53), run_time=0.85)
        self.play(*(piece.animate.shift(lift) for piece in (*moving_paw, fine)),
                  rate_func=there_and_back, run_time=1.12)
        self.play(fine.animate.shift(DOWN * 0.53), run_time=0.45)
        self.play(fine.animate.shift(UP * 0.53), rate_func=there_and_back, run_time=1.03)
        self.finish()


def predict_backdrop(*, raised=True):
    g = circuit_frame(raised=raised, activated=True, brain_view=True)
    g.brain.set_opacity(0.70)
    return g


def predict_question():
    return question_card(QUESTION, y=-3.19, size=34, max_w=10.05, left=-6.24).question


class S06PredictQuestion(SpokenScene):
    def construct(self):
        g = circuit_frame()
        scope = schematic()
        self.add(g, scope)
        self.at("after injury")
        wave(self, g.nerve, 0.55, 0.98, 1.25, RED,
             during=(g.cell[0].animate.set_fill("#7B6575"),))
        self.at("sensory neurons can fire", lead=0.10)
        wave(self, g.nerve, 0.73, 0.98, 1.06, RED)
        spontaneous = tag("Spontaneous firing", (0.1, -1.88), RED)
        self.play(FadeIn(spontaneous), run_time=0.52)
        wave(self, g.nerve, 0.47, 0.94, 1.25, RED,
             during=(g.cell[0].animate.set_fill(NERVE),))
        self.at("in one model", lead=0.08)
        model = tag("Model", (0.13, -1.88), GOLD)
        self.play(swap(spontaneous, model, run_time=0.60),
                  g.horns.animate.set_fill("#9383A4"), run_time=1.65)
        horn = tag("Dorsal horn", (4.27, 2.85), PURPLE)
        self.at("the dorsal horn", lead=0.37)
        self.play(FadeIn(horn), run_time=0.51)
        self.at("loses inhibition", lead=0.29)
        self.play(g.stop.animate.set_opacity(0.3), g.horns.animate.set_fill("#795868"), run_time=1.9)
        self.at("a light touch", lead=0.44)
        self.play(g.probe.animate.shift(UP * 0.19), FadeOut(horn), run_time=0.37)
        wave(self, g.nerve, 0.02, 0.99, 1.10)
        wave(self, g.central, 0.0, 0.99, 0.65, RED)
        end = predict_backdrop()
        end.brain.set_opacity(0.39)
        halfway = overview(spared=True, lift=REFLEX_LIFT / 2)
        self.play(Transform(g.animal, halfway.animal), Transform(g.wiring, halfway.wiring),
                  g.probe.animate.shift(UP * 0.07),
                  Transform(g.reflex, end.reflex), FadeIn(end.brain), run_time=0.65)
        self.at("pause and think", lead=0.23)
        self.play(FadeOut(model), FadeIn(predict_question()),
                  g.animal[0].animate.set_fill("#BE8790"), run_time=0.75)
        self.play(Transform(g.animal, end.animal), Transform(g.wiring, end.wiring),
                  Transform(g.probe, end.probe),
                  end.brain.animate.set_opacity(0.70), rate_func=lambda t: t**1.7,
                  run_time=self.narration_s + 0.38 - self.elapsed())
        self.finish()


class S07PredictPause(NarratedScene):
    def construct(self):
        self.add(predict_backdrop(), schematic(), predict_question())
        self.wait(self.narration_s)


class S08ControlsLimits(SpokenScene):
    def construct(self):
        g = predict_backdrop()
        resting = predict_backdrop(raised=False)
        raised_wiring = g.wiring.copy()
        self.add(g, schematic())
        self.at("a rat cannot", lead=0)
        self.play(Transform(g.animal, resting.animal), Transform(g.wiring, resting.wiring),
                  Transform(g.probe, resting.probe), run_time=0.63)
        self.at("a paw lift is", lead=0.45)
        self.play(g.animal.animate.shift(UP * REFLEX_LIFT), Transform(g.wiring, raised_wiring),
                  g.probe.animate.shift(UP * REFLEX_LIFT), run_time=0.85)
        stand = tag("Withdrawal reflex", (-3.77, -2.60), YELLOW)
        self.play(FadeIn(stand), run_time=0.55)
        self.at("separate brain circuits", lead=0.25)
        self.play(g.brain.animate.set_opacity(1).set_fill("#9D7DA9"), run_time=1.09)
        unpleasant = tag("Unpleasantness", (0.98, 3.11), PURPLE, size=29)
        leader = Line(unpleasant.get_right() + RIGHT * 0.13, pt(2.89, 3.11),
                      color=PURPLE, stroke_width=3)
        self.play(FadeIn(unpleasant), Create(leader), run_time=0.54)
        self.at("and spontaneous pain", lead=0.24)
        unknown = tag("?", (-2.43, 1.18), RED, size=44)
        self.play(FadeIn(unknown), run_time=0.55)
        wave(self, g.nerve, 0.55, 0.88, 1.95, RED,
             during=(g.cell[0].animate.set_fill("#6B535F"),))
        self.at("recovery over time", lead=0.55)
        ganglia = ganglion(marks=False)
        survival = heading("Which injured neurons survived?", GOLD)
        self.play(FadeOut(stand), FadeOut(unknown), FadeOut(unpleasant), FadeOut(leader), run_time=0.27)
        self.play(FadeOut(g), FadeIn(ganglia), run_time=0.66)
        self.play(FadeIn(survival), run_time=0.62)
        i = 2
        self.play(FadeOut(ganglia.cells[i], scale=0.62), FadeOut(ganglia.dots[i]), run_time=1.05)
        self.at("labs trace injured", lead=0.35)
        tracing = heading("Trace injured cells", GOLD)
        self.play(swap(survival, tracing, run_time=0.65), run_time=0.65)
        self.play(LaggedStart(*[Create(r) for r in ganglia.rings], lag_ratio=0.34),
                  *[ganglia.cells[i][0].animate.set_fill("#827249") for i in (0, 3)], run_time=1.70)
        self.at("differ with sex", lead=0.65)
        limits = heading("Sex and injury type")
        junction = pt(3.26, -0.38)
        routes = VGroup(
            Arrow(junction, pt(5.45, 0.87), buff=0, color=TEAL, stroke_width=5),
            Arrow(junction, pt(5.45, -1.50), buff=0, color=TEAL, stroke_width=5),
        )
        self.play(swap(tracing, limits, run_time=0.75), run_time=0.75)
        self.play(LaggedStart(*[GrowArrow(route) for route in routes], lag_ratio=0.27),
                  ganglia.shell.animate.set_fill("#536676"), run_time=1.32)
        self.at("injury mechanisms may", lead=0.20)
        disease = heading("Disease may differ")
        uncertain_route = DashedVMobject(spline([(3.26, -0.38), (4.09, 0.32),
                                                (4.80, 0.92), (5.58, 1.02)], GOLD, 5), num_dashes=8)
        uncertain_end = tag("?", (5.95, 1.02), GOLD, size=36)
        self.play(swap(limits, disease, run_time=0.85), routes.animate.set_opacity(0.32), run_time=0.85)
        self.play(Create(uncertain_route), ganglia.shell.animate.set_fill(TISSUE), run_time=0.88)
        self.play(FadeIn(uncertain_end), run_time=0.42)
        self.finish()


class S09UnlockedReprogramming(SpokenScene):
    def construct(self):
        g = ganglion(cut=False)
        self.add(g, schematic())
        attribution = heading("Renthal and colleagues, 2020", GOLD)
        self.at("first in 2020")
        self.play(FadeIn(attribution), g.shell.animate.set_fill("#4F6473"), run_time=1.18)
        self.at("colleagues cut or", lead=0.38)
        marker = Line(pt(-3.98, -0.78), pt(-3.98, -0.11), stroke_color=RED, stroke_width=7)
        self.play(Create(marker), FadeOut(g.bridge), run_time=0.56)
        self.play(FadeOut(marker), g.shell.animate.set_fill(TISSUE), run_time=1.56)
        self.at("then sequenced single", lead=0.3)
        nuclei = VGroup(*[Circle(radius=0.33, color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.51).move_to(c[1]).set_z_index(3) for c in g.cells])
        self.play(LaggedStart(*[Create(r) for r in nuclei], lag_ratio=0.26), run_time=1.32)
        drg = heading("Sensory ganglion (DRG)", TEAL)
        self.at("from sensory ganglia", lead=0.22)
        self.play(swap(attribution, drg, run_time=0.65), run_time=0.65)
        self.play(FadeOut(nuclei), run_time=0.75)
        self.at("injuries suppressed", lead=0.22)
        types = tag("Subtype markers", (4.42, 1.29), PURPLE)
        self.play(FadeIn(types), run_time=0.55)
        suppression = [AnimationGroup(dot.animate.set_opacity(0.13), cell[0].animate.set_fill(NERVE))
                       for dot, cell in zip(g.dots, g.cells)]
        self.play(LaggedStart(*suppression, lag_ratio=0.22), run_time=2.54)
        self.at("was required for full", lead=1.0)
        atf = boxed_label("Atf3", PURPLE, size=33, min_size=28).move_to(pt(4.45, 1.29))
        self.play(swap(types, atf, run_time=0.70), run_time=0.70)
        self.play(Indicate(atf, color=PURPLE, scale_factor=1.13),
                  g.shell.animate.set_fill("#4F4B67"), run_time=1.85)
        self.finish()


class S09bIdentityReturns(SpokenScene):
    def construct(self):
        g = ganglion(marks=False)
        g.shell.set_fill("#4F4B67")
        self.add(g, schematic())
        self.at("identity re")
        identity = heading("Subtype identity returns", PURPLE)
        self.play(FadeIn(identity), run_time=0.55)
        progress = ValueTracker(0.001)
        fiber = always_redraw(lambda: VGroup(part(g.stem, 0, progress.get_value(), GREEN, 13),
                                              Dot(g.stem.point_from_proportion(progress.get_value()),
                                                  radius=0.13, color=GREEN)))
        self.add(fiber)
        recovery = [AnimationGroup(dot.animate.set_opacity(1),
                                   cell[0].animate.set_fill(interpolate_color(ManimColor(NERVE), ManimColor(color), 0.47)))
                    for dot, cell, color in zip(g.dots, g.cells, IDENTITY_COLORS)]
        self.play(LaggedStart(*recovery, lag_ratio=0.21), g.shell.animate.set_fill(TISSUE),
                  progress.animate.set_value(0.88), run_time=2.88, rate_func=linear)
        self.at("with regrowth", lead=-0.20)
        assoc = heading("Associated with regrowth", GREEN)
        self.play(swap(identity, assoc, run_time=0.70), run_time=0.70)
        self.at("reporter's share held", lead=1.12)
        share = tag("Atf3 reporter share", (4.45, 1.76), GOLD, size=29)
        bar = RoundedRectangle(width=2.91, height=0.38, corner_radius=0.12,
                               stroke_width=2.5, stroke_color=GOLD).move_to(pt(4.45, 0.91))
        fill = RoundedRectangle(width=1.26, height=0.23, corner_radius=0.075,
                                stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to(pt(3.74, 0.91))
        self.play(FadeIn(share), FadeIn(bar), FadeIn(fill), FadeIn(g.rings), run_time=0.7)
        self.at("from one week", lead=0.42)
        week = tag("1 week", (4.45, -1.12), size=29)
        months = tag("2 months", (4.45, -1.12), size=29)
        self.play(FadeIn(week), run_time=0.62)
        self.at("to two months", lead=0.16)
        self.play(swap(week, months, run_time=0.69), Indicate(g.rings, color=GOLD, scale_factor=1.045),
                  run_time=1.42)
        self.at("against selective death", lead=0.1)
        finding = heading("Evidence against selective death", GOLD)
        self.play(swap(assoc, finding, run_time=0.75), run_time=0.75)
        self.finish()


class S10UnlockedPain(SpokenScene):
    def construct(self):
        g = dorsal_horn(vglut=True)
        intensity = ValueTracker(0.26)
        gauge = threshold_dial(intensity, centre=(4.35, -1.87), radius=1.42)
        credit = heading(CREDIT_P, GOLD)
        self.add(g, schematic())
        self.at("in 2015 pears")
        self.play(FadeIn(credit), g.horns.animate.set_fill("#8E7FA3"), run_time=1.59)
        self.at("colleagues deleted vglut3", lead=0.0)
        self.play(Indicate(g.receiver, color=PURPLE, scale_factor=1.07), run_time=0.57)
        self.play(FadeOut(g.vglut, shift=DOWN * 0.20), g.horns.animate.set_fill(HORN), run_time=1.39)
        horn = tag("Dorsal horn", (-4.82, -2.62), PURPLE)
        self.at("mouse dorsal horn", lead=0.2)
        self.play(FadeIn(horn), run_time=0.67)
        self.at("withdrawal thresholds rose", lead=0.46)
        self.play(FadeIn(gauge), run_time=0.57)
        self.play(intensity.animate.set_value(0.71), run_time=2.22, rate_func=linear)
        self.at("stronger touch was needed", lead=0.3)
        thick = filament(3.10, 0.57, slim=False, height=0.86)
        self.play(ReplacementTransform(g.probe, thick), run_time=0.55)
        self.play(thick.animate.shift(UP * 0.26), g.animal.animate.shift(UP * 0.21),
                  rate_func=there_and_back, run_time=1.42)
        self.at("also in 2015", lead=0.32)
        next_credit = heading(CREDIT_J, GOLD)
        males = tag("Male mice", (-4.82, -2.62), TEXT)
        self.play(swap(credit, next_credit, run_time=0.79), swap(horn, males, run_time=0.79),
                  FadeOut(gauge), FadeOut(thick), run_time=0.79)
        pv_name = tag("Parvalbumin\nneuron", (-5.16, 2.42), PURPLE, size=29)
        self.play(FadeIn(pv_name), run_time=0.69)
        self.at("removed spinal parvalbumin", lead=0.13)
        self.play(FadeOut(g.pv, scale=0.32), FadeOut(g.link), g.stop.animate.set_opacity(0.58),
                  g.horns.animate.set_fill("#8E7189"), run_time=2.18)
        self.play(FadeOut(pv_name), run_time=0.46)
        self.at("caused mechanical allodynia", lead=0.35)
        thin = filament(3.10, 0.57, slim=True, height=0.86)
        allo = tag("Mechanical allodynia", (3.80, -1.83), RED, size=29)
        self.play(FadeIn(thin), FadeIn(allo), run_time=0.64)
        self.play(thin.animate.shift(UP * 0.50), g.animal.animate.shift(UP * 0.50),
                  rate_func=there_and_back, run_time=1.26)
        self.at("lifting inhibition on", lead=0.27)
        self.play(FadeOut(g.stop, shift=UP * 0.27), run_time=0.78)
        pkc = tag("PKC-gamma interneuron", (-1.23, -2.92), PURPLE, size=28)
        self.play(FadeIn(pkc), run_time=0.61)
        wave(self, g.afferent, 0.06, 1.0, 1.74, RED,
             during=(g.horns.animate.set_fill("#965E70"),))
        self.play(g.receiver[0].animate.set_stroke(RED, 3).set_fill("#955451"), run_time=0.45)
        self.finish()


class S11Closing(SpokenScene):
    def construct(self):
        g = dorsal_horn()
        activated = dorsal_horn(activated=True)
        intensity = ValueTracker(0.22)
        gauge = threshold_dial(intensity, centre=(4.35, -1.87), radius=1.42)
        credit = heading(CREDIT_J, GOLD)
        males = tag("Male mice", (-4.82, -2.62))
        active = tag("Activated", (-5.05, 2.34), GREEN)
        scope = schematic()
        self.add(g, credit, males, gauge, scope)
        self.at("activating parvalbumin")
        self.play(Transform(g.pv, activated.pv), Transform(g.link, activated.link),
                  Transform(g.stop, activated.stop), run_time=1.18)
        self.play(FadeIn(active), run_time=0.55)
        self.at("neurons eased", lead=0.04)
        self.play(intensity.animate.set_value(0.58), g.horns.animate.set_fill("#6B837C"),
                  rate_func=linear, run_time=3.25)
        self.at("whether an axon regrows", lead=0.54)
        whole = overview(spared=True, limb_gap=True, cord_gap=True)
        probe = filament(-5.82, -1.60, height=1.15)
        whole.add(probe)
        tracer = Circle(radius=0.95, color=GOLD, stroke_width=5).move_to(whole.cell)
        self.play(FadeOut(credit), FadeOut(males), FadeOut(gauge), FadeOut(active), run_time=0.26)
        self.play(FadeOut(g), FadeIn(whole), run_time=0.62)
        extension = ValueTracker(0.489)
        tip = growing(whole.nerve, extension, start=0.49)
        self.add(tip)
        self.play(extension.animate.set_value(0.35), run_time=1.32)
        self.at("stalls or rewires", lead=0.05)
        stall = Dot(whole.central.point_from_proportion(0.45), color=RED, radius=0.15)
        self.play(FadeIn(stall), run_time=0.55)
        self.play(FadeOut(stall), probe.animate.shift(UP * 0.20), run_time=0.56)
        raised = overview(spared=True, limb_gap=True, cord_gap=True, lift=0.33)
        wave(self, whole.nerve, 0.06, 0.99, 1.15, RED,
             during=(Transform(whole.animal, raised.animal), Transform(whole.wiring, raised.wiring),
                     probe.animate.shift(UP * 0.22)))
        self.at("a controlled break", lead=0.28)
        self.play(Create(tracer), whole.cell[0].animate.set_fill("#927A4C"), run_time=1.12)
        wave(self, whole.central, 0.03, 0.43, 1.07, RED,
             during=(whole.horns.animate.set_fill("#9B6880"),))
        self.finish()


class S12End(EndCard):
    LINE = "Controlled nerve injury isolates axon breakdown, regrowth, and altered pain circuits."
