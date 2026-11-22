"""FRAP, viewed through a schematic fluorescence microscope.

Colour map (adapted from the patch-clamp film): blue = excitation and laser;
grey = structure and bleached molecules; purple = pores and binding sites;
green = fluorescence; yellow = measurement guides; teal = comparison traces;
gold = questions and study credits.
"""

from math import cos, exp, pi, sin

from bp_parts import *

PURPLE = "#B58CD9"
GLOW = "#C1F6A0"
FIELD = "#38664D"
DARK = "#242C33"
STAGE = (-3.46, 0.18, 0)
SPOT = 1.57
QUESTION = "What happened to the other half?"
QUESTION_STYLE = dict(y=3.22, size=32, left=0.8, max_w=5.9)
BEFORE = -0.25
AFTER = 1.0


def point(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, size=30, color=TEXT):
    return T(text, size, color).move_to(point(x, y))


def border(width, height, at, color=GREY, fill=FIELD):
    return RoundedRectangle(
        corner_radius=0.25, width=width, height=height,
        stroke_color=color, stroke_width=2, fill_color=fill, fill_opacity=1,
    ).move_to(at)


def grain(radius=0.115, color=GLOW):
    core = Dot(radius=radius, color=color)
    halo = Dot(radius=radius * 1.95, color=color, fill_opacity=0.17)
    return VGroup(halo, core)


def tint(particle, color, halo=0.17):
    particle[0].set_fill(color, opacity=halo)
    particle[1].set_fill(color, opacity=1)


def drift(grains, positions, speed=1.3, amplitude=0.16):
    """Independent in-plane motion around each schematic sampling position."""
    phases = np.arange(len(grains)) * 2.399963
    age = 0.0

    def move(group, dt):
        nonlocal age
        age += dt
        for dot, p, phase in zip(group, positions, phases):
            dot.move_to(p + amplitude * point(
                sin(age * speed + phase), cos(age * speed * 0.73 + phase),
            ))

    move(grains, 0)
    grains.add_updater(move)
    return grains


def curve_recovery(t, mobile=1.0):
    """First-order exchange: dF/dt is proportional to the unfilled mobile pool.

    Normalized schematic time is used throughout. Ease the time parameter
    near the far end to hold the asymptotic plateau on screen.
    """
    u = np.clip(t, 0, 0.86) / 0.86
    clock = u if u < 0.7 else u + (u - 0.7) ** 2 * (1 - u) / 0.09
    return mobile * -np.expm1(-5 * clock) / -np.expm1(-5)


class MembraneView(VGroup):
    """A common stage with a circular ROI and fluorescent/bleached particle pairs."""

    def __init__(self, t, mobile=1.0, bleach=0.0, wide=False, tag=1.0, scale=1.0, at=None, title_band=False, swapping=False):
        self.t = t
        self.mobile = mobile
        self.bleach = ValueTracker(bleach)
        self.tag = ValueTracker(tag)
        self.view_scale = scale
        self.title_band = title_band
        self.swapping = swapping
        width = 12.88 if wide else 6.04
        center = point(0, 0.18) if wide else np.array(STAGE)
        self.sheet = border(width, 5.53, center)
        self.spot = Circle(radius=SPOT, stroke_color=GREY, stroke_width=2.5,
                           fill_color=FIELD, fill_opacity=1).move_to(center)
        self.spot.set_stroke(opacity=0)
        self.roi = Circle(radius=SPOT, color=TEXT, stroke_width=2, stroke_opacity=0.72).move_to(center)

        rng = np.random.default_rng(541)
        self.positions = [
            point(x, y) for y in np.linspace(-2.11, 2.11, 8)
            for x in np.linspace(-width / 2 + 0.59, width / 2 - 0.59, 19 if wide else 9)
            if np.hypot(x, y) > 2.00
        ]
        self.positions = [p + point(*rng.uniform(-0.11, 0.11, 2)) for p in self.positions]
        self.outer = VGroup(*(grain(0.103) for _ in self.positions))
        self.partners = list(range(len(self.positions)))
        for i in range(0, len(self.positions) - 1, 2):
            a, b = self.positions[i:i + 2]
            if abs(a[1] - b[1]) < 0.23 and abs(a[0] - b[0]) < 0.92:
                self.partners[i], self.partners[i + 1] = i + 1, i

        angles = np.linspace(0, TAU, 12, endpoint=False) + 0.17
        self.inner_sites = [point(cos(a), sin(a)) * (1.13 if i % 2 == 0 else 0.68)
                            for i, a in enumerate(angles)]
        self.outer_sites = [point(cos(a), sin(a)) * (1.90 + 0.19 * (i % 2))
                            for i, a in enumerate(angles)]
        self.originals = VGroup(*(grain(0.107) for _ in angles))
        self.replacements = VGroup(*(grain(0.107) for _ in angles))
        self.tracks = VGroup(*(
            VMobject(stroke_color=PURPLE, stroke_width=2.7).set_points_smoothly(
                [center + p + point(-0.24, -0.14), center + p, center + p + point(0.25, 0.15)])
            for p in self.inner_sites[1::2]
        )).set_opacity(0)
        super().__init__(self.sheet, self.spot, self.tracks, self.outer, self.originals, self.replacements)
        self.age = 0.0
        self.scale(scale)
        if at is not None:
            self.move_to(at)
            self.roi.scale(scale).move_to(at)
        self.refresh(0)

    def refresh(self, dt):
        self.age += dt
        center = self.sheet.get_center()
        scale = self.view_scale
        t = self.t.get_value()
        bleach = self.bleach.get_value()
        tag = self.tag.get_value()
        replenished = curve_recovery(t, self.mobile)
        field_color = interpolate_color(ManimColor(DARK), ManimColor(FIELD), tag)
        self.sheet.set_fill(field_color)
        self.spot.move_to(center).set_fill(
            interpolate_color(field_color, ManimColor("#182B24"), bleach * (1 - replenished)))
        lit = interpolate_color(ManimColor(GREY), ManimColor(GLOW), tag)
        bleached = interpolate_color(lit, ManimColor("#435152"), bleach)
        for i, (particle, p) in enumerate(zip(self.outer, self.positions)):
            phase = i * 2.399963
            offset = 0.19 * point(sin(1.65 * self.age + phase), cos(1.24 * self.age + phase))
            partner = self.partners[i]
            if self.swapping and partner != i:
                progress = 0.5 - 0.5 * cos(0.84 * self.age + min(i, partner) * 0.29)
                q = self.positions[partner]
                offset += progress * (q - p) + UP * 0.12 * np.sign(q[0] - p[0]) * sin(pi * progress)
            particle.move_to(center + scale * (p + offset))
            tint(particle, lit)
            if self.title_band and abs(particle.get_y() - center[1]) < 0.96:
                particle.set_opacity(0)
        for i, (old, new, inner, outer) in enumerate(zip(
            self.originals, self.replacements, self.inner_sites, self.outer_sites
        )):
            fixed = self.mobile == 0.5 and i % 2 == 1
            slot = i if self.mobile == 1 else i // 2
            count = 12 if self.mobile == 1 else 6
            share = replenished / self.mobile
            progress = smooth(np.clip(share * count * 0.56 - slot * 0.56 + 0.30 * share, 0, 1))
            if fixed:
                progress = 0
            direction = outer - inner
            tangent = point(-direction[1], direction[0])
            bow = 0.26 * sin(pi * progress) * tangent
            wobble = 0.13 * point(sin(1.8 * self.age + i), cos(1.42 * self.age + i))
            old.move_to(center + scale * (interpolate(inner, outer, progress) + bow + (0 * wobble if fixed else wobble)))
            new.move_to(center + scale * (interpolate(outer, inner, progress) - bow - wobble))
            tint(old, bleached, halo=0.17 * (1 - bleach))
            tint(new, lit)
            if self.title_band:
                for dot in (old, new):
                    if abs(dot.get_y() - center[1]) < 0.96:
                        dot.set_opacity(0)

    def moving(self):
        self.add_updater(lambda mob, dt: mob.refresh(dt))
        return self


def recovery_axes():
    return Plot(
        box=(1.43, 6.36, -2.53, 2.25), xr=(BEFORE, AFTER), yr=(0, 1.09),
        xlabel="Time", label_size=29, color=GREY,
        yticks=[(1, "100%"), (0, "0%")], size=28,
    )


def recovery_trace(plot, time, mobile):
    return VGroup(
        plot.curve(lambda _: 1, x0=BEFORE, x1=0, color=GREEN, width=5),
        Line(plot.pt(0, 1), plot.pt(0, 0), color=GREEN, stroke_width=5),
        plot.live_curve(lambda t: curve_recovery(t, mobile), time, color=GREEN, width=5, x0=0),
    )


def recovery_labels():
    return VGroup(
        label("Spot brightness", 3.40, 2.53, 30),
        scope_tag(size=28, color=TEXT).move_to(point(5.49, -3.45)),
    )


def plateau(plot):
    return VGroup(
        DashedLine(plot.pt(BEFORE, 0.5), plot.pt(AFTER, 0.5), color=YELLOW,
                   stroke_width=2.2, dash_length=0.13).set_z_index(-1),
        T("50%", 28, YELLOW).next_to(plot.pt(BEFORE, 0.5), LEFT, buff=0.14),
    )


def laser(at, width=0.92):
    """Focused blue illumination, with a brief highlight at the target."""
    x, y, _ = at
    top = 3.45
    cone = Polygon(point(x - width, top), point(x + width, top), point(x, y),
                   stroke_width=0, fill_color=BLUE, fill_opacity=0.50)
    beam = Line(point(x, top), at, color=BLUE, stroke_width=7)
    focus = Circle(radius=0.29, stroke_color=BLUE, stroke_width=4).move_to(at)
    return VGroup(cone, beam, focus)


def bleach_spot(scene, view):
    beam = laser(view.sheet.get_center())
    scene.play(FadeIn(beam), run_time=0.28)
    scene.play(view.bleach.animate.set_value(1), FadeOut(beam), run_time=0.48)


class S01Hook(SpokenScene):
    def construct(self):
        view = MembraneView(ValueTracker(0), wide=True, swapping=True).moving()
        self.add(view)
        self.at("how can you")
        question = question_card("How can you see it move?", y=-3.36, size=34)
        self.play(FadeIn(question), run_time=0.4)
        self.at("swapping places")
        self.play(FadeOut(question), run_time=0.48)
        self.at("to reveal motion")
        dark_ring = view.roi.copy().set_stroke("#19252A", width=6, opacity=1)
        self.play(Create(dark_ring), run_time=1.25)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Fluorescence Recovery After Photobleaching (FRAP)"
    TITLE = "Watching Molecules Move by Bleaching a Spot"

    def construct(self):
        view = MembraneView(ValueTracker(0), wide=True, title_band=True).moving()
        veil = RoundedRectangle(width=12.88, height=5.53, corner_radius=0.25,
                                stroke_width=0, fill_color=BG, fill_opacity=0.78).move_to(view.sheet)
        title = VGroup(
            T(self.TITLE, size=43, font=TITLE_FONT),
            T(self.LESSON, size=28, color=TEXT),
        ).arrange(DOWN, buff=0.33)
        title.move_to(view.sheet)
        self.add(view, veil)
        self.play(FadeIn(title), run_time=0.36)
        self.wait(1.2)
        self.play(FadeOut(title), run_time=0.38)


class S03Bleach(SpokenScene):
    def construct(self):
        view = MembraneView(ValueTracker(0), wide=True, tag=0).moving()
        self.add(view)
        self.at("tag the target")
        tag_label = label("Fluorescent dye or GFP", 0, -3.35)
        self.play(FadeIn(tag_label), run_time=0.5)
        self.at("absorbs blue light")
        blue = laser(point(-0.42, 0.8), width=1.15)
        excitation = label("Blue light in", -3.7, -3.35, color=BLUE)
        self.play(FadeOut(tag_label), FadeIn(blue), FadeIn(excitation), run_time=0.6)
        self.at("emits green light")
        emission = label("Green light out", 3.55, -3.35, color=GLOW)
        self.play(view.tag.animate.set_value(1), FadeOut(blue), FadeIn(emission), run_time=0.95)
        self.at("carries its own lamp")
        self.play(FadeOut(excitation), FadeOut(emission), run_time=0.45)
        self.at("a focused laser")
        self.play(Create(view.roi), run_time=0.35)
        bleach_spot(self, view)
        self.at("molecules stay")
        self.play(FadeIn(label("Still there, not glowing", 0, -3.35)), run_time=0.45)
        self.finish()


class S04Recover(SpokenScene):
    def construct(self):
        t = ValueTracker(0)
        wide = MembraneView(t, wide=True, bleach=1)
        left = MembraneView(t, bleach=1).moving()
        plot = recovery_axes()
        labels = recovery_labels()
        pre = recovery_trace(plot, t, 1)
        self.add(wide, wide.roi)
        self.at("then unbleached molecules")
        self.play(Transform(wide, left.copy().clear_updaters()), Transform(wide.roi, left.roi),
                  run_time=0.91)
        self.remove(wide, wide.roi)
        self.add(left, left.roi)
        self.play(FadeIn(plot), FadeIn(labels), FadeIn(pre[0]), Create(pre[1]), run_time=0.62)
        self.add(pre[2])
        self.play(t.animate.set_value(0.35), run_time=5.13, rate_func=linear)
        self.at("this is fluorescence")
        term = label("Fluorescence recovery\nafter photobleaching (FRAP)", -3.46, -3.35, 28)
        self.play(FadeIn(term), t.animate.set_value(0.51), run_time=2.2, rate_func=linear)
        self.at("how fast light returns")
        along = 0.12
        y = curve_recovery(along)
        slope = (curve_recovery(along + 0.001) - y) / 0.001
        tangent = Arrow(plot.pt(along - 0.095, y - 0.095 * slope),
                        plot.pt(along + 0.09, y + 0.09 * slope),
                        buff=0, color=YELLOW, stroke_width=4, tip_length=0.15)
        rate = label("Diffusion coefficient", 4.75, -1.27, 30, YELLOW)
        self.play(FadeOut(term), GrowArrow(tangent), run_time=0.56)
        self.at("the diffusion coefficient")
        self.play(FadeIn(rate), t.animate.set_value(0.7), run_time=2.65, rate_func=linear)
        self.at("how completely it")
        x = 6.57
        y0, y1 = plot.pt(0, 0)[1], plot.pt(0, curve_recovery(0.86))[1]
        bracket = VGroup(Line(point(x, y0), point(x, y1)),
                         Line(point(x - 0.12, y0), point(x, y0)),
                         Line(point(x - 0.12, y1), point(x, y1))).set_stroke(YELLOW, 3)
        fraction = label("Mobile fraction", 4.4, -0.65, 30, YELLOW)
        self.play(FadeOut(tangent), FadeOut(rate), t.animate.set_value(0.87),
                  run_time=1.1, rate_func=linear)
        self.play(Create(bracket), run_time=0.40)
        self.at("the mobile fraction")
        self.play(FadeIn(fraction), t.animate.set_value(1), run_time=2.50, rate_func=linear)
        self.at("bleaching one spot")
        self.play(FadeOut(fraction), FadeOut(bracket), run_time=0.65)
        self.finish()


def prediction_world(t, bleach):
    view = MembraneView(t, mobile=0.5, bleach=bleach)
    plot = recovery_axes()
    return view, plot, recovery_labels(), recovery_trace(plot, t, 0.5)


class S05PredictQ(SpokenScene):
    def construct(self):
        t = ValueTracker(0)
        view, plot, labels, trace = prediction_world(t, 0)
        self.add(view.moving(), view.roi, plot, labels, trace[0])
        self.at("second membrane protein")
        second = label("Second membrane protein", -3.46, -3.36, 28)
        self.play(FadeIn(second), run_time=0.5)
        self.at("the same laser")
        bleach_spot(self, view)
        self.play(Create(trace[1]), FadeOut(second), run_time=0.43)
        self.at("spot brightens at first")
        self.add(trace[2])
        self.play(t.animate.set_value(0.86), run_time=1.73, rate_func=linear)
        self.at("stalls at 50")
        self.play(FadeIn(plateau(plot)), t.animate.set_value(1), run_time=1.42, rate_func=linear)
        self.at("what happened to")
        self.play(FadeIn(question_card(QUESTION, **QUESTION_STYLE)), run_time=0.55)
        self.finish()


class S06PredictPause(Scene):
    def construct(self):
        config.background_color = BG
        self.camera.background_color = BG
        view, plot, labels, trace = prediction_world(ValueTracker(1), 1)
        view.refresh(15.4)
        self.add(view, view.roi, plot, labels, trace, plateau(plot))
        self.add(question_card(QUESTION, **QUESTION_STYLE))
        self.wait(float(os.environ.get("KX_DURATION", "4.5")))


class S07PredictAnswer(SpokenScene):
    def construct(self):
        t = ValueTracker(1)
        view, plot, labels, trace = prediction_world(t, 1)
        guide = plateau(plot)
        q = question_card(QUESTION, **QUESTION_STYLE)
        view.refresh(15.4)
        self.add(view.moving(), view.roi, plot, labels, trace, guide, q)
        self.at("starting from dark")
        self.play(FadeOut(q), FadeOut(plot), FadeOut(labels), FadeOut(trace), FadeOut(guide), run_time=0.65)
        formula = label("Mobile fraction =", 3.57, 1.75, 34)
        numerator = label("Recovered brightness", 3.57, 0.65, 32, GLOW)
        denominator = label("Starting brightness", 3.57, -0.59, 32)
        bar = Line(point(1.24, 0.04), point(5.90, 0.04), color=GREY, stroke_width=3)
        self.at("mobile fraction equals")
        self.play(FadeIn(formula), run_time=0.52)
        self.at("recovered brightness")
        self.play(FadeIn(numerator), run_time=0.62)
        self.at("divided by")
        self.play(Create(bar), run_time=0.60)
        self.at("starting brightness")
        self.play(FadeIn(denominator), run_time=0.55)
        self.at("reaching half")
        half = label("Half", 3.57, 0.65, 32, GLOW)
        full = label("Full", 3.57, -0.59, 32)
        self.play(swap(numerator, half), swap(denominator, full), run_time=0.85)
        self.at("gives 50%")
        self.play(FadeIn(label("= 50%", 3.57, -1.76, 42, YELLOW)), run_time=0.45)
        self.at("cannot move")
        pinned = VGroup(*(Circle(radius=0.17, color=YELLOW, stroke_width=2.4).move_to(dot)
                          for dot in view.originals[1::2]))
        self.play(LaggedStart(*(Create(ring) for ring in pinned), lag_ratio=0.15), run_time=1.08)
        self.at("they are anchored")
        self.play(view.tracks.animate.set_opacity(0.95), FadeOut(pinned), run_time=0.62)
        self.at("the cytoskeleton")
        self.play(FadeIn(label("Cytoskeleton", -3.46, -3.34, 29, PURPLE)), run_time=0.48)
        self.finish()


def turnover_examples(t):
    """Two membrane samples at identical scale, with one common recovery clock."""
    top = MembraneView(t, bleach=1, wide=True, scale=0.47, at=point(-3.46, 1.64)).moving()
    bottom = MembraneView(ValueTracker(0), bleach=1, wide=True, scale=0.47, at=point(-3.46, -1.42))
    top_roi, bottom_roi = top.roi, bottom.roi
    bottom_center = bottom.sheet.get_center()
    bottom.remove(bottom.originals, bottom.replacements, bottom.tracks)
    sites = VGroup()
    residents = VGroup()
    arrivals = VGroup()
    for i, x in enumerate((-0.42, -0.14, 0.14, 0.42)):
        y = 0.13 if i % 2 else -0.12
        site = bottom_center + point(x, y)
        cup = Arc(radius=0.105, start_angle=PI, angle=PI, color=PURPLE, stroke_width=4).move_arc_center_to(site)
        old, new = grain(0.063, "#435152").move_to(site), grain(0.063).move_to(site + UP * 0.60)
        sites.add(cup)
        residents.add(old)
        arrivals.add(new)
    return VGroup(top, top_roi), VGroup(bottom, bottom_roi, sites, residents, arrivals)


class S08LimitsTurnover(SpokenScene):
    def construct(self):
        plot = recovery_axes()
        labels = recovery_labels()
        full = ValueTracker(0)
        view = MembraneView(full, bleach=1).moving()
        trace = recovery_trace(plot, full, 1)
        self.add(view, view.roi, plot, labels, trace)
        self.at("even full recovery")
        self.play(full.animate.set_value(1), run_time=3.95, rate_func=linear)
        self.at("frap measures turnover")
        turnover = label("Turnover", 3.86, 3.21, 35, YELLOW)
        self.play(FadeIn(turnover), run_time=0.53)
        self.at("swapping of old")
        exchange = ValueTracker(0)
        free_patch, bound_patch = turnover_examples(exchange)
        stage = VGroup(view, view.roi)
        self.play(FadeOut(stage), FadeIn(free_patch), run_time=0.67)
        self.at("free diffusion")
        free = label("Free diffusion", -3.46, 3.26, 29)
        self.play(FadeIn(free), exchange.animate.set_value(0.78), run_time=1.65, rate_func=linear)
        self.at("binding and unbinding")
        self.play(FadeIn(bound_patch), FadeIn(label("Fixed binding sites", -3.46, -3.10, 29, PURPLE)),
                  run_time=0.74)
        self.play(exchange.animate.set_value(1), run_time=1.8, rate_func=linear)
        self.at("bleached molecules let go")
        _, _, sites, residents, arrivals = bound_patch
        self.play(*[dot.animate.shift(point(0.40, -0.38 if i % 2 else -0.45))
                    for i, dot in enumerate(residents)], run_time=1.4)
        self.at("glowing ones bind")
        stage = bound_patch[0]
        self.play(stage.spot.animate.set_fill(FIELD),
                  *[dot.animate.move_to(site.get_arc_center()) for dot, site in zip(arrivals, sites)],
                  run_time=1.38)
        self.finish()


# For a two-half body and a surrounding reservoir, the difference between halves
# decays at 2*k_mix + k_edge. The body mean and reservoir relax at k_edge*(1+1/3)
# for the illustrative 3:1 volume ratio. This keeps the fluorescence budget fixed.
def body_levels(t):
    equilibrium = 0.35
    difference = exp(-6.9 * t)
    mean = equilibrium + (0.50 - equilibrium) * exp(-0.70 * t)
    return mean - 0.5 * difference, mean + 0.5 * difference, (1.40 - mean) / 3


def body_chart():
    return Plot(box=(0.83, 6.42, -2.39, 2.22), xr=(0, 1), yr=(0, 1.07),
                xlabel="Time", label_size=29)


def sample_disk(radius, count, rng, accept=lambda p: True):
    points = []
    while len(points) < count:
        p = point(*rng.uniform(-radius, radius, 2))
        if np.linalg.norm(p) < radius and accept(p):
            points.append(p)
    return points


def nuclear_body(time, bleached, edge, rebound):
    center = np.array(STAGE)
    stage = border(6.04, 5.53, center, fill="#2C5041")
    r = 1.94
    backdrop = Circle(radius=r, color=GREEN, stroke_width=0, fill_color=FIELD, fill_opacity=1).move_to(center)
    halves = VGroup(*[
        AnnularSector(inner_radius=0, outer_radius=r, angle=PI, start_angle=a,
                      fill_color=FIELD, fill_opacity=1, stroke_width=0).shift(center)
        for a in (PI / 2, -PI / 2)
    ])
    outline = DashedVMobject(Circle(radius=r, color=GREY, stroke_width=3).move_to(center),
                             num_dashes=46, dashed_ratio=0.65)
    rng = np.random.default_rng(804)
    outside = [point(x, y) for x in np.linspace(-2.67, 2.67, 10) for y in np.linspace(-2.28, 2.28, 7)
               if np.hypot(x, y) > r + 0.29]
    bath = drift(VGroup(*(grain(0.085, GREEN) for _ in outside)), [center + p for p in outside], amplitude=0.12)
    spots = sample_disk(1.66, 29, rng)
    moieties = VGroup(*(grain(0.099) for _ in spots))
    cluster_points = [point(-0.5, -0.70), point(-0.18, -0.63), point(-0.35, -0.99),
                      point(-0.05, -0.98), point(0.14, -0.72), point(0.09, -0.44)]
    sites = VGroup(*(Circle(radius=0.14, color=PURPLE, stroke_width=3).move_to(center + p) for p in cluster_points))
    phase = 0.0

    def update(world, dt):
        nonlocal phase
        phase += dt
        t = time.get_value()
        b = bleached.get_value()
        left, right, _ = body_levels(t)
        for half, level in zip(halves, (left, right)):
            half.set_fill(interpolate_color(ManimColor("#1C2D27"), ManimColor("#508963"), 1 - b * (1 - level)))
        outline.set_stroke(opacity=edge.get_value())
        sites.set_stroke(opacity=rebound.get_value() * 0.85)
        for i, (dot, p) in enumerate(zip(moieties, spots)):
            loc = p + 0.19 * point(sin(1.9 * phase + i), cos(1.4 * phase - 2 * i))
            # Particles retain their post-bleach colour as they cross the centre.
            # Mirror selected pairs across the left/right boundary during mixing.
            if i % 3 == 0:
                mix = 1 - exp(-5.7 * t)
                loc[0] = p[0] * (1 - 2 * mix) + 0.14 * sin(2.1 * phase + i)
            if i < len(cluster_points) and rebound.get_value() > 0:
                k = rebound.get_value()
                dock = cluster_points[i] + 0.21 * point(sin(2.4 * phase + i), 1 - cos(2.4 * phase + i))
                loc = interpolate(loc, dock, k)
            dot.move_to(center + loc)
            tint(dot, interpolate_color(ManimColor(GLOW), ManimColor("#4A5654"), b if p[0] < 0 else 0))
        # Two sparse edge crossings appear after the faster internal exchange.
        for i in (0, 1):
            idx = min(range(len(outside)), key=lambda j: np.linalg.norm(outside[j] - point(2.15, 0.55 - i)))
            p = outside[idx]
            approach = 0.53 * (1 - exp(-0.95 * t)) * (1 + 0.45 * (1 - edge.get_value()))
            bath[idx].move_to(center + p * (1 - approach))

    world = VGroup(stage, backdrop, halves, bath, outline, sites, moieties)
    update(world, 0)
    world.add_updater(update)
    return world


class S09LimitsHalfbody(SpokenScene):
    def construct(self):
        time, bleach, edge, rebound = ValueTracker(0), ValueTracker(0), ValueTracker(0.88), ValueTracker(0)
        body = nuclear_body(time, bleach, edge, rebound)
        self.add(body)
        self.at("may be droplets")
        possible = label("Possible liquid droplet", 3.49, 0.15, 35)
        self.play(FadeIn(possible), run_time=0.58)
        self.at("half body frappe")
        half_heading = label("Half-body FRAP", 3.49, 0.15, 35)
        self.play(swap(possible, half_heading, 0.65))
        self.at("bleach one half")
        flash = laser(np.array(STAGE) + LEFT * 0.92, width=0.75)
        self.play(FadeOut(half_heading), FadeIn(flash), run_time=0.23)
        self.play(bleach.animate.set_value(1), FadeOut(flash), run_time=0.40)
        self.at("track both halves")
        plot = body_chart()
        colors = (GREEN, YELLOW, TEAL)
        headings = VGroup(label("Left half", 1.40, 2.79, 28, GREEN),
                          label("Right half", 3.29, 2.79, 28, YELLOW),
                          label("Nucleoplasm", 5.53, 2.79, 28, TEAL))
        curves = VGroup(*(plot.live_curve(lambda t, i=i: body_levels(t)[i], time, c, width=4.5)
                          for i, c in enumerate(colors)))
        self.play(FadeIn(plot), FadeIn(headings), FadeIn(scope_tag(size=28, color=TEXT)), run_time=0.67)
        self.add(curves)
        self.play(time.animate.set_value(0.07), run_time=2.25, rate_func=linear)
        self.at("mixing inside should")
        conclusion = label("Faster mixing inside", -3.46, -3.34, 29, YELLOW)
        self.play(FadeIn(conclusion, run_time=0.5),
                  time.animate(run_time=3.16, rate_func=linear).set_value(0.72))
        self.at("that favors a phase")
        self.play(time.animate.set_value(1), run_time=1.1, rate_func=linear)
        self.at("without proving one")
        caveat = label("A liquid phase is possible", -3.46, -3.34, 29, YELLOW)
        self.play(swap(conclusion, caveat), run_time=0.65)
        self.at("weak edges may")
        self.play(edge.animate.set_value(0.37), run_time=1.85)
        self.at("rebinding in clusters")
        self.play(rebound.animate.set_value(1), FadeOut(caveat), run_time=1.5)
        self.play(FadeIn(label("Rebinding in a cluster", -3.46, -3.34, 29, PURPLE)), run_time=0.5)
        self.finish()


def yeast_cell(bleach, exchange):
    center = np.array(STAGE)
    stage = border(6.04, 5.53, center, fill="#203530")
    base = Ellipse(width=4.30, height=4.78, fill_color=FIELD, fill_opacity=1,
                   stroke_color=GREY, stroke_width=3).move_to(center + LEFT * 0.43 + DOWN * 0.08)
    bud = Circle(radius=1.01, fill_color=FIELD, fill_opacity=1, stroke_color=GREY,
                 stroke_width=3).move_to(center + point(1.57, 1.16))
    nucleus_center = center + point(-0.78, 0.17)
    nuclear_fill = ManimColor("#4F815C")
    equilibrated_fill = ManimColor("#23362F")
    envelope = Circle(radius=1.07, color=GREY, stroke_width=3,
                      fill_color=nuclear_fill, fill_opacity=1).move_to(nucleus_center)
    pore_angles = np.array([0.03, 0.72, 1.50, 2.35, 3.15, 4.00, 4.82, 5.51])
    rays = [point(cos(a), sin(a)) for a in pore_angles]
    pores = VGroup(*(Dot(nucleus_center + ray * 1.07, radius=0.083, color=PURPLE) for ray in rays))
    rng = np.random.default_rng(108)
    cyto_points = [
        p + base.get_center() for p in sample_disk(1.94, 44, rng,
            lambda p: np.linalg.norm(p + base.get_center() - nucleus_center) > 1.26)
    ] + [p + bud.get_center() for p in sample_disk(0.80, 11, rng)]
    cytoplasm = drift(VGroup(*(grain(0.085) for _ in cyto_points)), cyto_points, amplitude=0.105)
    cargo = VGroup(*(grain(0.088 + 0.027 * (i % 3)) for i in range(18)))
    age = 0.0
    cell_center = base.get_center()
    cell_radii = np.array([base.width / 2 - 0.26, base.height / 2 - 0.26])

    def update(world, dt):
        nonlocal age
        age += dt
        b, t = bleach.get_value(), exchange.get_value()
        cytosol = interpolate_color(ManimColor(FIELD), equilibrated_fill, b)
        base.set_fill(cytosol)
        bud.set_fill(cytosol)
        envelope.set_fill(interpolate_color(nuclear_fill, equilibrated_fill, 0.85 * t))
        for dot in cytoplasm:
            tint(dot, interpolate_color(ManimColor(GLOW), ManimColor("#3B4B48"), b), 0.17 * (1 - b))
        for i, dot in enumerate(cargo):
            # Crossing times rise with size. Each exiting path passes one pore.
            size = i % 3
            progress = np.clip((t - 0.054 * (i // 3) - 0.17 * size) / (0.32 + 0.10 * size), 0, 1)
            ray = rays[(i + 2 * (i // 3)) % len(rays)]
            initial_radius = 0.20 + 0.12 * (i // 3)
            departure = smooth(progress)
            cross = interpolate(initial_radius, 1.59, departure)
            # Diffuse throughout the nucleus before converging on a pore.
            # The offset vanishes at the envelope so trajectories use the pore.
            clearance = min(1, abs(cross - 1.07) * 3.3)
            jitter = clearance * point(0.30 * sin(2.18 * age + i * 0.9),
                                       0.39 * cos(1.79 * age + i * 1.7))
            displacement = nucleus_center + ray * cross + jitter - cell_center
            relative_radius = np.linalg.norm(displacement[:2] / cell_radii)
            dot.move_to(cell_center + displacement / max(1.0, relative_radius))

    view = VGroup(stage, base, bud, cytoplasm, envelope, pores, cargo)
    update(view, 0)
    view.add_updater(update)
    return view


class S10UnlockedPores(SpokenScene):
    def construct(self):
        bleach, exchange = ValueTracker(0), ValueTracker(0)
        view = yeast_cell(bleach, exchange)
        self.add(view)
        self.at("tested cell barriers")
        detail = label("Nuclear pores", 3.45, 2.79, 34, PURPLE)
        self.play(FadeIn(detail), run_time=0.52)
        self.at("proposed a sharp")
        wall = DashedLine(point(3.45, -2.33), point(3.45, 1.44),
                          color=PURPLE, stroke_width=8, dash_length=0.19)
        limit = label("40 kDa?", 3.45, 1.90, 39, YELLOW)
        self.play(Create(wall), run_time=0.66)
        self.play(FadeIn(limit), run_time=0.46)
        self.at("timney and colleagues")
        credit = label("Timney et al., 2016", 3.45, 3.29, 29, GOLD)
        self.play(FadeOut(wall), FadeOut(limit), FadeOut(detail), FadeIn(credit), run_time=0.58)
        self.at("bleached cytoplasmic fluorescence")
        flash = laser(np.array(STAGE) + RIGHT * 1.37, width=0.97)
        self.play(FadeIn(flash), run_time=0.32)
        self.play(bleach.animate.set_value(1), FadeOut(flash), run_time=0.65)
        self.at("different sized reporters")
        caption_sizes = label("Different reporter sizes", 3.45, -0.20, 31)
        self.play(FadeIn(caption_sizes), run_time=0.45)
        self.at("leaked out through")
        self.play(exchange.animate.set_value(0.55), run_time=2.54, rate_func=linear)
        self.at("their excess signal")
        self.play(FadeOut(caption_sizes), run_time=0.21)
        plot = Plot(box=(0.75, 6.36, -2.52, 1.88), xr=(0, 1), yr=(0, 1.05),
                    xlabel="Time", label_size=29)
        chart_heading = label("Excess nuclear signal", 3.49, 2.27, 30)
        elapsed = ValueTracker(0)
        # Timney's 27 and 67 kDa time constants, as presented in Nuclear Transport.
        small = plot.live_curve(lambda t: exp(-900 * t / 15), elapsed, GLOW, width=5)
        large = plot.live_curve(lambda t: exp(-900 * t / 413), elapsed, TEAL, width=5)
        self.play(FadeIn(plot), FadeIn(chart_heading), FadeIn(scope_tag(size=28, color=TEXT)), run_time=0.53)
        self.add(small, large)
        self.play(elapsed.animate.set_value(0.58), exchange.animate.set_value(0.84), run_time=2.05, rate_func=linear)
        self.at("slowly for larger")
        small_label = label("Smaller", 2.14, -1.88, 28, GLOW)
        large_label = label("Larger", 4.25, -0.49, 28, TEAL)
        self.play(FadeIn(small_label), FadeIn(large_label), elapsed.animate.set_value(1),
                  exchange.animate.set_value(1), run_time=1.94, rate_func=linear)
        self.at("no sharp cutoff")
        self.play(FadeIn(label("No sharp cutoff", -3.46, -3.34, 30, YELLOW)), run_time=0.45)
        self.finish()


def root_interface(bleach, transfer):
    center = np.array(STAGE)
    def cell(side):
        # Flatten the shared side and round the outer cell shoulders.
        vertices = [point(x * side, y) + center for x, y in
                    ((0.06, -2.62), (2.47, -2.62), (2.94, -2.19),
                     (2.94, 2.19), (2.47, 2.62), (0.06, 2.62))]
        return Polygon(*vertices, fill_color=FIELD, fill_opacity=1,
                       stroke_width=2, stroke_color=GREY).round_corners(0.14)

    left, right = cell(-1), cell(1)
    ys = (-1.60, -0.54, 0.54, 1.60)
    channels = VGroup(*(
        RoundedRectangle(width=0.43, height=0.14, corner_radius=0.055,
                         fill_color=PURPLE, fill_opacity=1, stroke_width=0).move_to(center + UP * y)
        for y in ys
    ))
    rng = np.random.default_rng(101)
    pos = [(side, point(x * side, y) + point(*rng.uniform(-0.10, 0.10, 2)))
           for side in (-1, 1) for x in np.linspace(0.48, 2.40, 5) for y in np.linspace(-2.15, 2.15, 8)]
    particles = VGroup(*(grain(0.094) for _ in pos))
    crossings = VGroup(*(grain(0.106) for _ in ys))
    age = 0.0

    def update(world, dt):
        nonlocal age
        age += dt
        b, t = bleach.get_value(), transfer.get_value()
        brightness = plant_recovery(t, rate=4.1)
        left.set_fill(interpolate_color(ManimColor(FIELD), ManimColor("#23382E"), b * (1 - brightness)))
        for i, (dot, (side, p)) in enumerate(zip(particles, pos)):
            dot.move_to(center + p + 0.13 * point(sin(age * 1.58 + i), cos(age * 1.08 + i * 2)))
            original_dark = b if side == -1 else 0
            # A progressively larger sample of the observed compartment is
            # occupied by unbleached GFP as exchange proceeds.
            refreshed = smooth(np.clip((brightness - ((i * 19) % 43) / 48) * 9, 0, 1))
            tint(dot, interpolate_color(ManimColor(GLOW), ManimColor("#445452"), original_dark * (1 - refreshed)))
        if b > 0:
            for i, (dot, y) in enumerate(zip(crossings, ys)):
                age_since = max(0, age - 17.0 - i * 0.26)
                p = (age_since * (0.60 + 0.10 * i)) % 1
                dot.move_to(center + point(0.96 - 1.94 * p, y + 0.055 * sin(TAU * p)))
                alpha = min(1, 9 * p, 9 * (1 - p)) if t > 0 else 0
                dot[0].set_fill(opacity=0.17 * alpha)
                dot[1].set_fill(opacity=alpha)
        else:
            crossings.set_opacity(0)

    world = VGroup(left, right, channels, particles, crossings)
    update(world, 0)
    world.add_updater(update)
    return world, channels


def plant_recovery(t, rate):
    """Schematic first-order fluorescence recovery comparison."""
    return -np.expm1(-rate * t)


class S11UnlockedPlants(SpokenScene):
    def construct(self):
        bleach, transfer = ValueTracker(0), ValueTracker(0)
        root, channels = root_interface(bleach, transfer)
        credit = label("Dawei Yan et al., 2019", 3.44, 3.29, 29, GOLD)
        scope = scope_tag(size=28, color=TEXT)
        self.add(root, credit, scope)
        self.at("pores joining plant cells")
        pores = label("Plasmodesmata", 3.45, 0.80, 35, PURPLE)
        self.play(FadeIn(pores), channels.animate.set_stroke(PURPLE, width=2), run_time=0.68)
        self.at("arabidopsis root mutant")
        root_label = label("Arabidopsis root mutant", -3.46, -3.34, 29)
        self.play(FadeIn(root_label), run_time=0.56)
        self.at("at one interface")
        a = label("No visible\ncytoplasmic sleeve", 3.44, 0.58, 34)
        self.play(swap(pores, a), run_time=0.76)
        self.at("the open channel")
        self.play(channels.animate.set_fill("#A18AB7").set_stroke(PURPLE, width=3), run_time=0.76)
        self.at("yet frap showed")
        flash = laser(np.array(STAGE) + LEFT * 1.51)
        self.play(FadeIn(flash), FadeOut(a), run_time=0.24)
        self.play(FadeOut(flash), bleach.animate.set_value(1), run_time=0.48)
        self.at("gfp crossing")
        plot = Plot(box=(0.72, 6.32, -2.33, 1.92), xr=(0, 1), yr=(0, 1.07),
                    xlabel="Time", label_size=29)
        self.play(FadeIn(plot), FadeIn(label("GFP recovery", 3.51, 2.62, 30)), run_time=0.51)
        mutant = plot.live_curve(lambda t: plant_recovery(t, 4.1), transfer, GLOW, width=5)
        wild = plot.live_curve(lambda t: plant_recovery(t, 1.45), transfer, TEAL, width=5)
        self.add(mutant, wild)
        self.play(transfer.animate.set_value(0.38), run_time=1.05, rate_func=linear)
        self.at("wild type roots")
        self.play(FadeIn(label("Mutant", 4.96, 1.93, 29, GLOW)),
                  FadeIn(label("Wild type", 4.94, -0.38, 29, TEAL)),
                  transfer.animate.set_value(0.84), run_time=1.55, rate_func=linear)
        self.at("erasing one patch")
        self.play(transfer.animate.set_value(1), run_time=1.26, rate_func=linear)
        self.at("hidden exchange")
        wide = MembraneView(ValueTracker(0), wide=True).moving()
        old_world = Group(*self.mobjects)
        self.play(FadeOut(old_world), run_time=0.36)
        self.play(FadeIn(wide), run_time=0.52)
        self.finish()


class S12End(EndCard):
    LINE = "Bleach a spot dark; the returning glow measures movement and exchange."
