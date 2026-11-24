"""Measuring a Forest's Breath, timed to audio/words.json.

Colors follow the reference film's roles: BLUE for apparatus and measurements,
GREY for structure, YELLOW for transported CO₂, GREEN for fixation, ORANGE for
respiration, TEAL for carbonyl sulfide, and GOLD for questions and dates.
"""
from bp_parts import *
from bp_style import EndCard

ORANGE = "#F29E4C"
PINE = ("#315E54", "#407661", "#548465")
SKY_DAY = "#172735"
SKY_NIGHT = "#101726"
QUESTION = "Forest stores carbon: positive or negative NEE?"
TOWER_X = -2.46
SCHEMATIC_RECO_LENGTH = 1.17
EXAMPLE_NEE = -300
GAUGE_LIMIT = 400
GAUGE_EXTENT = 1.49


def point(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=32):
    return T(text, size, color).move_to(point(x, y))


def slab(w, h, x, y, color, radius=0.2):
    return RoundedRectangle(width=w, height=h, corner_radius=radius,
                            stroke_width=0, fill_color=color, fill_opacity=1).move_to(point(x, y))


def arr(a, b, color=GREY, w=5, tip=0.2):
    """Arrow geometry from the reference film."""
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pine(x, y, h, w, color):
    trunk = slab(w * 0.11, h * 0.77, x, y + h * 0.385, "#765C52", 0.02)
    layers = VGroup()
    for base, peak, width in [(0.14, 0.69, 1), (0.33, 0.85, 0.84), (0.54, 1, 0.65)]:
        layers.add(Polygon(
            point(x - w * width / 2, y + base * h),
            point(x, y + peak * h),
            point(x + w * width / 2, y + base * h),
            stroke_width=0, fill_color=color, fill_opacity=1,
        ))
    return VGroup(trunk, layers)


def tower(x=TOWER_X, bottom=-2.17, height=4.44, simple=False):
    def p(side, fraction):
        return point(x + side * (0.50 - 0.29 * fraction) * height / 4.44,
                     bottom + height * fraction)

    mast = VGroup(*(Line(p(side, 0), p(side, 1), color=BLUE, stroke_width=4)
                    for side in (-1, 1)))
    sections = np.linspace(0, 1, 4 if simple else 9)
    for lo, hi in zip(sections[:-1], sections[1:]):
        mast.add(Line(p(-1, hi), p(1, hi), color=BLUE, stroke_width=2))
        for side in (-1, 1):
            mast.add(Line(p(side, lo), p(-side, hi), color=BLUE, stroke_width=1.35,
                          stroke_opacity=0.64))
    head = VGroup(Line(p(0, 1), p(0, 1.10), color=BLUE, stroke_width=3.5),
                  Line(p(-1.9, 1.10), p(1.9, 1.10), color=BLUE, stroke_width=3.5),
                  Dot(p(-1.9, 1.10), radius=height * 0.016, color=BLUE),
                  Dot(p(1.9, 1.10), radius=height * 0.016, color=BLUE))
    return VGroup(mast, head)


def forest():
    """The carried cross-section with fixed canopy and sensor coordinates."""
    sky = slab(8.40, 5.63, -2.40, 0.27, SKY_DAY)
    ground = Polygon(
        point(-6.60, -2.55), point(1.80, -2.55), point(1.80, -1.69),
        point(0.25, -1.87), point(-1.55, -1.69), point(-3.78, -1.82),
        point(-5.28, -1.58), point(-6.60, -1.78),
        stroke_width=0, fill_color="#554742", fill_opacity=1,
    )
    far = VGroup(*(pine(x, -1.89, h, 1.12, PINE[0]) for x, h in
                   [(-5.98, 2.86), (-5.21, 2.59), (-4.25, 2.83), (-3.48, 2.41),
                    (-2.76, 2.45), (-1.44, 2.72), (-0.55, 2.54), (0.41, 2.68), (1.22, 2.53)]))
    near = VGroup(*(pine(x, -2.28, h, w, PINE[i % 2 + 1]) for i, (x, h, w) in enumerate(
        [(-5.83, 2.49, 1.38), (-4.72, 3.10, 1.48), (-3.67, 2.61, 1.10),
         (-1.46, 2.69, 1.18), (-0.33, 3.06, 1.48), (0.97, 2.67, 1.23)])))
    return sky, VGroup(ground, far, near), tower()


def add_forest(scene, with_tower=True):
    sky, trees, mast = forest()
    scene.add(sky, trees)
    if with_tower:
        scene.add(mast)
    return sky, trees, mast


def tag():
    return scope_tag(size=28, color=GREY)


def wind(y_levels=(1.48, 2.30), x_left=-5.76, width=6.75):
    """Curled gusts and CO₂ passing the sensor head from left to right."""
    gusts = VGroup()
    for lane, level in enumerate(y_levels):
        for i in range(3):
            envelope = Ellipse(width=1.5, height=0.43, stroke_width=0,
                               fill_color=BLUE, fill_opacity=0.47)
            trace = Arc(angle=2.0, radius=0.16, color=BLUE, stroke_width=3)
            trace.rotate(1.03).shift(LEFT * 0.42)
            grains = VGroup(*[Dot(point(dx, dy), radius=0.079, color=YELLOW)
                              for dx, dy in [(-0.12, -0.05), (0.12, 0.10), (0.35, -0.03)]])
            gust = VGroup(envelope, trace, grains)
            opacities = (0.47, 0.95, 1.0)
            phase = (i + lane * 0.43) / 3

            gust.clock = 0.0

            def drift(mob, dt, phase=phase, lane=lane, level=level):
                mob.clock += dt
                f = (phase + mob.clock * (0.22 + 0.025 * lane)) % 1
                mob.move_to(point(x_left + width * f, level + 0.13 * np.sin(2 * PI * f)))
                fade = min(1, 10 * f, 10 * (1 - f))
                for part, opacity in zip(mob, opacities):
                    part.set_opacity(fade * opacity)

            drift(gust, 0)
            gust.add_updater(drift)
            gusts.add(gust)
    return gusts


def stream(x, start, end, color, count, speed=0.57, width=0.92):
    """One moving cloud of tracer dots. Density encodes concentration qualitatively."""
    dots = VGroup()
    for i in range(count):
        offset = (i * 0.61803399) % 1
        lane = ((i * 0.41421356) % 1 - 0.5) * width
        dot = Dot(radius=0.111 if i % 3 else 0.147, color=color)
        dot.clock = 0.0

        def tick(mob, dt, offset=offset, lane=lane):
            mob.clock += dt
            f = (offset + speed * mob.clock) % 1
            mob.move_to(point(x + lane + 0.15 * np.sin(2 * PI * f),
                              interpolate(start, end, f)))
            mob.set_opacity(min(1, 11 * f, 11 * (1 - f)))

        tick(dot, 0)
        dot.add_updater(tick)
        dots.add(dot)
    return dots


def vertical_gust(up):
    x = 0.3 if up else -4.92
    a, b = (0.27, 2.54) if up else (2.54, 0.27)
    arrow = arr(point(x, a), point(x, b), BLUE, w=6, tip=0.28)
    return arrow, stream(x + 0.38, a, b, YELLOW, 7 if up else 16)


def gauge_heading():
    return label("NEE (net exchange)", 4.23, 2.55, BLUE, 34)


def gauge_signs():
    return (label("+", 3.72, GAUGE_EXTENT, TEXT, 36),
            label("−", 3.72, -GAUGE_EXTENT, TEXT, 36))


def release_label():
    return label("Release to air", 5.76, GAUGE_EXTENT, TEXT, 24)


def gauge(value, *, signed=True):
    """Vertical balance. The needle and the measured fill share the same value."""
    x = 4.45
    extent = GAUGE_EXTENT
    slot = slab(0.38, 2 * extent, x, 0, "#284050", 0.16)
    zero = label("0", 3.72, 0, TEXT, 30)
    tick = Line(point(x - 0.34, 0), point(x + 0.34, 0), stroke_width=2, color=GREY)

    def fill():
        y = extent * value.get_value() / GAUGE_LIMIT
        return Rectangle(width=0.28, height=max(0.001, abs(y)), stroke_width=0,
                         fill_color=BLUE, fill_opacity=0.78).move_to(point(x, y / 2))

    marker = Triangle(fill_color=BLUE, fill_opacity=1, stroke_width=0).scale(0.155).rotate(PI / 2)
    marker.add_updater(lambda m: m.move_to(point(x + 0.48, extent * value.get_value() / GAUGE_LIMIT)))
    marker.update(0)
    meter = VGroup(slot, tick, always_redraw(fill), marker, zero)
    if signed:
        meter.add(*gauge_signs())
    return meter


def measurement():
    return M("−300 g C m⁻² yr⁻¹", 32, BLUE).move_to(point(4.35, -2.32))


def flux_arrow(x, length, rising, color, model=False):
    bottom = point(x, 0.05)
    top = point(x, length + 0.05)
    a, b = (bottom, top) if rising else (top, bottom)
    if model:
        return DashedLine(a, b, color=color, stroke_width=8,
                          dash_length=0.14, dashed_ratio=0.62).add_tip(tip_length=0.23)
    return arr(a, b, color, w=9, tip=0.29)


def flux_pair(fixation_length=SCHEMATIC_RECO_LENGTH, model=False, reco_length=SCHEMATIC_RECO_LENGTH):
    gpp = flux_arrow(-4.87, fixation_length, False, GREEN, model)
    reco = flux_arrow(0.27, reco_length, True, ORANGE, model)
    gpp_label = label("GPP (fixation)", -4.67, 2.58, GREEN)
    reco_label = label("Reco (respiration)", -0.12, 2.58, ORANGE, 30)
    return gpp, reco, gpp_label, reco_label


def flux_motion():
    return VGroup(stream(-4.47, 2.11, 0.21, YELLOW, 11, width=0.68),
                  stream(0.70, 0.15, 1.53, YELLOW, 9, speed=0.53, width=0.67))


def tower_gusts():
    return wind(y_levels=(1.39, 1.89), x_left=-3.69, width=2.67)


def question():
    return question_card(QUESTION, y=-3.12, left=-6.2, size=34, max_w=10)


class S01Hook(SpokenScene):
    def construct(self):
        sky, trees, mast = forest()
        landscape = VGroup(sky, trees)
        wide = landscape.copy().stretch_to_fit_width(13.20, about_edge=LEFT)
        self.add(wide, tag())
        tree_x = -6.60 + (1.88 * 13.20 / 8.40)
        jar = RoundedRectangle(width=2.52, height=3.32, corner_radius=0.27,
                               color=BLUE, stroke_width=4, stroke_opacity=0.76,
                               fill_color=BLUE, fill_opacity=0.12)
        jar.move_to(point(tree_x, -0.60))
        lid = Line(point(tree_x - 0.94, 1.08), point(tree_x + 0.94, 1.08),
                   color=BLUE, stroke_width=5)
        glass = VGroup(jar, lid)
        self.at("measure a", lead=0.36)
        self.play(Create(jar), run_time=2.40)
        self.at("without sealing", lead=0.4)
        self.play(FadeIn(lid, shift=DOWN * 0.16), run_time=1.0)
        self.at("instead", lead=0.45)
        self.play(FadeOut(glass, shift=UP * 0.32), Transform(wide, landscape), run_time=1.10)
        self.play(GrowFromEdge(mast, DOWN), run_time=1.03)
        self.at("watch carbon", lead=0.45)
        self.add(wind())
        self.at("that method is")
        self.play(FadeIn(label("Eddy covariance", 4.24, 0.56, TEXT, 42)), run_time=0.55)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Measuring a Forest's Breath"
    LESSON = "Eddy Covariance"

    def construct(self):
        add_forest(self)
        self.add(wind(), tag())
        title = T(self.TITLE, 44, TEXT, font=TITLE_FONT)
        title.move_to(point(-2.40, 3.50))
        self.play(FadeIn(title), run_time=0.27)
        self.wait(1.32)
        self.play(FadeOut(title), run_time=0.33)


class S03Tower(SpokenScene):
    def construct(self):
        landscape = VGroup(*forest())
        self.add(landscape, tag())
        wide = landscape.copy()
        intake = wind()
        self.add(intake)
        halo = Circle(radius=0.54, color=BLUE, stroke_width=3).move_to(point(TOWER_X, 2.56))
        self.play(Create(halo), landscape.animate.scale(1.045, about_point=point(TOWER_X, 2.70)),
                  run_time=0.65)
        pulse(halo, base=3, amp=1.1, speed=2.5)
        self.at("track vertical wind", lead=0.42)
        wind_label = label("Vertical wind", 4.24, 1.47, BLUE, 36)
        self.play(FadeIn(wind_label), run_time=0.55)
        self.at("and co2 concentration", lead=0.36)
        co2_label = label("CO₂ concentration", 4.24, 0.78, YELLOW, 36)
        self.play(FadeIn(co2_label), run_time=0.60)
        self.at("sinking gusts", lead=0.7)
        down, down_cloud = vertical_gust(False)
        self.play(FadeOut(VGroup(intake, halo, wind_label, co2_label)),
                  Transform(landscape, wide), GrowArrow(down), run_time=0.65)
        self.add(down_cloud, tower_gusts())
        self.at("rising gusts lift", lead=0.55)
        up, up_cloud = vertical_gust(True)
        self.play(GrowArrow(up), run_time=0.60)
        self.add(up_cloud)
        self.at("the forest takes")
        self.play(FadeIn(caption("Net carbon uptake", color=GREEN, size=34)), run_time=0.7)
        self.at("averaged yearly", lead=0.65)
        balance = ValueTracker(0)
        self.play(FadeIn(gauge(balance, signed=False)), run_time=0.66)
        self.at("net ecosystem exchange", lead=0.18)
        self.play(FadeIn(gauge_heading()), run_time=0.53)
        self.finish()


class S04SignPredict(SpokenScene):
    def construct(self):
        add_forest(self)
        balance = ValueTracker(0)
        gusts = tower_gusts()
        self.add(gauge(balance, signed=False), gauge_heading(), tag(), gusts)
        gpp, reco, gpp_label, reco_label = flux_pair()
        self.at("gross primary production", lead=0.78)
        self.play(GrowArrow(gpp), run_time=0.64)
        self.play(FadeIn(gpp_label), run_time=0.55)
        down = stream(-4.51, 1.49, 0.28, YELLOW, 8, width=0.44)
        self.add(down)
        self.at("ecosystem respiration", lead=0.78)
        self.play(GrowArrow(reco), run_time=0.64)
        self.play(FadeIn(reco_label), run_time=0.55)
        up = stream(0.63, 0.27, 1.48, YELLOW, 7, speed=0.39, width=0.43)
        self.add(up)
        self.at("suppose the tower", lead=0)
        self.play(FadeIn(VGroup(*gauge_signs(), release_label())), run_time=0.50)
        self.at("if a forest stores", lead=0.15)
        self.play(FadeIn(question()), run_time=0.66)
        self.at("negative", lead=0)
        self.wait(1.13)
        self.play(FadeOut(VGroup(down, up, gusts)), run_time=0.29)
        self.finish()


def predict_backdrop():
    return VGroup(*forest(), gauge(ValueTracker(0)), gauge_heading(),
                  release_label(), tag(), *flux_pair())


class S05Pause(PredictPause):
    QUESTION = QUESTION
    SECONDS = 4.5

    def construct(self):
        self.add(predict_backdrop(), question())
        self.wait(self.SECONDS, frozen_frame=True)


class S06AnswerMath(SpokenScene):
    def construct(self):
        add_forest(self)
        balance = ValueTracker(0)
        gpp, reco, gpp_label, reco_label = flux_pair()
        q = question()
        release = release_label()
        self.add(gauge(balance), gauge_heading(), release, tag(), gpp, reco, gpp_label, reco_label, q,
                 tower_gusts())
        self.at("negative")
        result = caption("Negative NEE", color=BLUE, size=35)
        self.play(swap(q, result, run_time=0.65))
        flow = flux_motion()
        self.add(flow)
        self.at("nee equals", lead=0.32)
        equation = M("NEE = Reco − GPP", 37).move_to(point(-2.4, 3.39))
        self.play(FadeIn(equation), run_time=0.64)
        self.at("fixes more than", lead=0.46)
        long_gpp = flux_pair(2.13)[0]
        self.play(Transform(gpp, long_gpp), run_time=1.75)
        self.at("falls below zero", lead=0.48)
        self.play(balance.animate.set_value(-105), run_time=1.30)
        self.at("say a tower reads", lead=0.18)
        self.play(FadeOut(release), balance.animate.set_value(EXAMPLE_NEE), run_time=1.03)
        self.at("minus 300", lead=0.02)
        number = measurement()
        self.play(FadeIn(number), run_time=0.42)
        self.at("uptake beat release", lead=0.2)
        self.play(swap(result, caption("Net sink", color=GREEN, size=36)), run_time=0.77)
        self.finish()


def model_equation():
    return M("GPP = modelled Reco + 300", 35).move_to(point(-2.42, 3.39))


def day_models():
    # Lengths are schematic. Only the excess, above modelled respiration, is fixed by the example.
    length_per_carbon = 0.0025
    reco_length = 1.38
    fixation_length = reco_length + (-EXAMPLE_NEE) * length_per_carbon
    return flux_pair(fixation_length, model=True, reco_length=reco_length)


class S07Partition(SpokenScene):
    def construct(self):
        sky, trees, _ = add_forest(self)
        gpp, reco, gpp_label, reco_label = flux_pair(2.13)
        balance = ValueTracker(EXAMPLE_NEE)
        number = measurement()
        equation = M("NEE = Reco − GPP", 37).move_to(point(-2.4, 3.39))
        result = caption("Net sink", color=GREEN, size=36)
        flow = flux_motion()
        self.add(gauge(balance), gauge_heading(), tag(), number, equation, result,
                 gpp, reco, gpp_label, reco_label, flow, tower_gusts())
        self.at("300 is net exchange")
        self.play(FadeOut(result), Indicate(number, color=BLUE, scale_factor=1.08), run_time=0.9)
        self.at("a flux tower measures")
        self.play(Indicate(number, color=BLUE, scale_factor=1.05), run_time=1.0)
        self.at("a partitioning model")
        self.play(FadeOut(equation), run_time=0.60)
        self.at("at night", lead=0.76)
        night = label("Night", -2.42, 3.39, TEXT, 38)
        self.play(sky.animate.set_fill(SKY_NIGHT), trees.animate.set_opacity(0.64),
                  FadeOut(VGroup(gpp, gpp_label, flow[0], number)), run_time=1.20)
        self.play(FadeIn(night), balance.animate.set_value(130), run_time=0.72)
        self.at("tower records respiration", lead=0.35)
        night_nee = label("NEE = Reco", 4.35, -2.32, BLUE, 34)
        self.play(FadeIn(night_nee), run_time=0.67)
        self.at("models extend nighttime", lead=0.48)
        gpp_day, reco_day, _, _ = day_models()
        self.play(sky.animate.set_fill(SKY_DAY), trees.animate.set_opacity(1),
                  FadeOut(VGroup(night, night_nee)), balance.animate.set_value(EXAMPLE_NEE),
                  ReplacementTransform(reco, reco_day), run_time=1.55)
        self.play(FadeIn(number), run_time=0.53)
        self.at("adding modeled respiration", lead=0.40)
        self.play(Create(gpp_day), run_time=1.15)
        self.add(flow[0])
        self.play(FadeIn(gpp_label), FadeIn(model_equation()), run_time=0.75)
        self.finish()


class S08Limits(SpokenScene):
    def construct(self):
        add_forest(self)
        gpp, reco, gpp_label, reco_label = day_models()
        number = measurement()
        balance = ValueTracker(EXAMPLE_NEE)
        meter = gauge(balance)
        equation = model_equation()
        self.add(meter, gauge_heading(), tag(), number, gpp, reco, gpp_label, reco_label,
                 equation, flux_motion(), tower_gusts())
        self.at("check the sign convention", lead=0.35)
        sign = label("Check sign convention", -2.42, 3.39, GOLD, 36)
        self.play(swap(equation, sign, run_time=0.65),
                  Indicate(meter[-2], scale_factor=1.18, color=GOLD),
                  Indicate(meter[-1], scale_factor=1.18, color=GOLD), run_time=0.80)
        self.at("reversing it flips", lead=0.3)
        # Show what the wrong interpretation would say while leaving the measured bar fixed.
        wrong = label("Uptake ↔ release", 4.31, -1.83, GOLD, 29)
        self.play(FadeIn(wrong), run_time=0.58)
        self.at("second no method", lead=0.35)
        model_title = label("Modelled GPP", -2.42, 3.39, GREEN, 37)
        self.play(FadeOut(wrong), swap(sign, model_title, run_time=0.7))
        self.at("besides nighttime", lead=0.35)
        method = caption("Night-time fit", color=GREEN, size=34)
        self.play(FadeIn(method), run_time=0.62)
        outline1 = flux_arrow(-5.19, 1.77, False, GREEN, True).set_opacity(0.45)
        outline2 = flux_arrow(-4.58, 2.20, False, GREEN, True).set_opacity(0.45)
        self.at("light response fits", lead=0.28)
        new_method = caption("Light-response", color=GREEN, size=34)
        self.play(Create(outline1), swap(method, new_method, run_time=0.72))
        self.at("neural networks", lead=0.24)
        final_method = caption("Neural network", color=GREEN, size=34)
        self.play(Create(outline2), swap(new_method, final_method, run_time=0.75))
        self.at("every gpp estimate", lead=0.22)
        self.play(Indicate(final_method, color=GREEN, scale_factor=1.05), run_time=0.95)
        self.finish()


def network():
    """All 36 study sites are represented. The blue bar motion is schematic."""
    sites = VGroup()
    for i in range(36):
        row, col = divmod(i, 6)
        x, y = -6.06 + 1.22 * col, 2.83 - 0.88 * row
        icon = tower(x, bottom=y - 0.48, height=0.50, simple=True)
        icon.set_stroke(width=1.5)
        baseline = Line(point(x + 0.15, y - 0.48), point(x + 0.64, y - 0.48),
                        color=GREY, stroke_width=1, stroke_opacity=0.65)
        bar = slab(0.10, 0.32, x + 0.27, y - 0.31, BLUE, 0.01)
        bar.clock = 0.0

        def tick(mob, dt, x=x, y=y, i=i):
            mob.clock += dt
            h = 0.19 + 0.15 * (1 + np.sin(2.1 * mob.clock + i * 0.72))
            mob.stretch_to_fit_height(h).move_to(point(x + 0.27, y - 0.46 + h / 2))

        bar.add_updater(tick)
        tick(bar, 0)
        sites.add(VGroup(icon, baseline, bar))
    return sites


def agreement_plot():
    plot = Plot(box=(2.40, 6.51, -1.98, 1.74), xr=(0, 1), yr=(0, 1.1),
                xlabel="Time", color=GREY, label_size=29)
    t = ValueTracker(0.02)

    def estimate(time, respiration):
        # NEE = Reco − GPP. Compare two respiration assumptions using
        # the same illustrative net uptake profile, in arbitrary units.
        daylight = 4 * time * (1 - time)
        nee = -0.82 * daylight
        return respiration * daylight - nee

    a = lambda time: estimate(time, 0.10)
    b = lambda time: estimate(time, 0.17)
    curves = VGroup(plot.live_curve(a, t, color=GREEN, width=5),
                    plot.live_curve(b, t, color="#C9DB8F", width=4),
                    plot.dot(t.get_value, lambda: a(t.get_value()), color=GREEN))
    return plot, curves, t


def distant_view(landscape):
    return landscape.copy().scale(0.16).move_to(point(-2.4, -2.72))


class S09UnlockedNetworks(SpokenScene):
    def construct(self):
        sky, trees, mast = add_forest(self)
        gpp, reco, gpp_label, reco_label = day_models()
        flow = flux_motion()
        balance = ValueTracker(EXAMPLE_NEE)
        meter = VGroup(gauge(balance), gauge_heading(), measurement())
        old = VGroup(gpp, reco, gpp_label, reco_label, meter,
                     label("Modelled GPP", -2.42, 3.39, GREEN, 37),
                     caption("Neural network", color=GREEN, size=34), flow)
        self.add(old, tag())
        self.at("towers now span")
        self.play(FadeOut(old), run_time=0.48)
        landscape = VGroup(sky, trees, mast)
        # The original terrain remains visible below the expanded network.
        self.play(Transform(landscape, distant_view(landscape)), run_time=1.14)
        sites = network()
        self.play(LaggedStart(*(FadeIn(row, shift=UP * 0.10) for row in sites), lag_ratio=0.06),
                  run_time=2.15)
        self.at("a neural network method", lead=0.35)
        method = label("Neural network", 4.42, 0.98, GREEN, 36)
        self.play(FadeIn(method), run_time=0.66)
        self.at("36 fluxnet 2015", lead=0.28)
        count = label("36 FLUXNET2015 sites (2020)", -2.39, 3.42, GOLD, 35)
        self.play(FadeIn(count), run_time=0.68)
        self.at("split each tower's", lead=0.32)
        plot, curves, cursor = agreement_plot()
        graph_title = label("Modelled GPP", 4.42, 2.57, GREEN, 34)
        self.play(FadeOut(method), run_time=0.35)
        self.play(Create(plot), FadeIn(graph_title), run_time=0.78)
        self.add(curves)
        self.play(cursor.animate.set_value(1), run_time=2.92, rate_func=linear)
        self.at("without being right", lead=0.06)
        warning = caption("Agreement is not independent validation", color=GOLD, size=34, y=-3.45)
        self.play(FadeIn(warning), run_time=0.65)
        self.finish()


SLOT_X = (2.60, 3.76, 4.92, 6.08)
BAR_FLOOR = -1.70
BAR_WIDTH = 0.78
BAR_UNIT = 2.46
STUDY_TAG = "Hyytiälä, Finland · 2013–2017 · Kohonen et al. 2022"


def slots():
    outlines = VGroup()
    names = VGroup()
    for i, x in enumerate(SLOT_X):
        color = YELLOW if i < 2 else TEAL
        names.add(label("CO₂" if i < 2 else "COS", x, -2.14, color, 29))
        outlines.add(RoundedRectangle(width=BAR_WIDTH, height=0.62, corner_radius=0.09,
                                      stroke_color=color, stroke_width=3, fill_opacity=0)
                        .move_to(point(x, BAR_FLOOR + 0.31)))
    return outlines, names


def gas_flows():
    return (stream(-4.42, 2.47, 0.58, YELLOW, 12, speed=0.43, width=1.46),
            stream(-0.41, 2.47, 0.51, TEAL, 12, speed=0.34, width=1.52))


def study_title():
    return label(STUDY_TAG, -1.40, 3.39, GOLD, 32)


def gas_labels():
    return (label("CO₂", -4.45, 2.78, YELLOW, 32),
            label("Carbonyl sulfide", -0.35, 2.78, TEAL, 30))


class S10UnlockedHyytiala(SpokenScene):
    def construct(self):
        landscape = VGroup(*forest())
        distant = distant_view(landscape)
        self.add(distant, tag())
        co2, cos = gas_flows()
        co2_label, cos_label = gas_labels()
        outlines, names = slots()
        self.at("in 2022")
        self.play(Transform(distant, landscape), run_time=1.22)
        wind_field = wind()
        self.add(wind_field)
        self.at("compared four gpp", lead=0.38)
        comparison = label("Four GPP estimates", 4.30, 1.61, TEXT, 35)
        self.play(FadeIn(comparison), run_time=0.60)
        self.at("hayatila finland", lead=0.18)
        place = label("Hyytiälä, Finland · Kohonen et al. 2022", -1.74, 3.41, GOLD, 33)
        self.play(FadeIn(place), run_time=0.60)
        self.at("scots pine forest", lead=0.35)
        pines = label("Scots pine", -2.40, -3.12, TEXT, 32)
        self.play(FadeIn(pines), run_time=0.55)
        self.at("2013 to 2017", lead=0.25)
        self.play(swap(place, study_title(), run_time=0.68))
        self.at("methods used co2", lead=0.72)
        self.play(FadeOut(VGroup(wind_field, pines)), run_time=0.45)
        self.add(tower_gusts())
        self.add(co2)
        self.play(FadeIn(VGroup(co2_label, *outlines[:2], *names[:2])), run_time=0.61)
        self.at("two used carbonyl", lead=0.62)
        self.add(cos)
        self.play(FadeIn(VGroup(cos_label, *outlines[2:], *names[2:])), run_time=0.74)
        self.at("a second route", lead=0.32)
        self.play(Indicate(outlines[2:], color=TEAL, scale_factor=1.04), run_time=1.10)
        self.finish()


def relative_bar(i, ratio):
    height = BAR_UNIT * ratio
    return slab(BAR_WIDTH, height, SLOT_X[i], BAR_FLOOR + height / 2,
                YELLOW if i < 2 else TEAL, 0.08)


class S11Return(SpokenScene):
    def construct(self):
        add_forest(self)
        co2, cos = gas_flows()
        co2_label, cos_label = gas_labels()
        outlines, names = slots()
        title = study_title()
        comparison = label("Four GPP estimates", 4.30, 1.61, TEXT, 35)
        self.add(title, comparison, tag(), tower_gusts(), co2, cos, co2_label, cos_label, outlines, names)
        self.at("daily carbonyl sulfide")
        top = label("Daily GPP estimates", 4.33, 2.72, TEXT, 34)
        reference = relative_bar(0, 1)
        self.play(swap(comparison, top, run_time=0.69), ReplacementTransform(outlines[0], reference),
                  run_time=1.35)
        ref_line = DashedLine(point(3.10, BAR_FLOOR + BAR_UNIT), point(6.53, BAR_FLOOR + BAR_UNIT),
                              dash_length=0.11, color=GREY, stroke_width=2)
        ref_label = label("Ref.", SLOT_X[0], 1.14, YELLOW, 28)
        self.play(Create(ref_line), FadeIn(ref_label), run_time=0.63)
        self.at("7 or 23", lead=0.6)
        low, high = relative_bar(2, 1.07), relative_bar(3, 1.23)
        self.play(ReplacementTransform(outlines[2], low), run_time=0.73)
        seven = label("+7%", SLOT_X[2], 1.36, TEAL, 31)
        self.play(FadeIn(seven), ReplacementTransform(outlines[3], high), run_time=0.75)
        twenty_three = label("+23%", SLOT_X[3], 1.72, TEAL, 31)
        self.play(FadeIn(twenty_three), run_time=0.48)
        self.at("model of the two gases", lead=0.25)
        ratio = caption("Model of the two gases’ uptake ratio", color=TEAL, size=32)
        self.play(FadeIn(ratio), run_time=0.64)
        self.at("which estimate is true", lead=0.37)
        questions = VGroup(label("?", SLOT_X[2], 1.90, GOLD, 33),
                           label("?", SLOT_X[3], 2.24, GOLD, 33))
        self.play(FadeIn(questions), run_time=0.56)
        self.at("trust a flux tower", lead=0.47)
        chart = VGroup(top, reference, outlines[1], names, low, high, ref_line,
                       ref_label, seven, twenty_three, questions)
        self.play(FadeOut(VGroup(chart, title, ratio, co2, cos, co2_label, cos_label)), run_time=0.72)
        balance = ValueTracker(EXAMPLE_NEE)
        self.play(FadeIn(VGroup(gauge(balance), gauge_heading(), measurement())), run_time=0.96)
        self.at("always name the model", lead=0.38)
        gpp, _, _, _ = day_models()
        self.play(Create(gpp), run_time=0.75)
        self.play(FadeIn(label("Modelled GPP", -4.67, 2.58, GREEN, 32)), run_time=0.51)
        self.add(flux_motion()[0])
        for dash in gpp:
            if isinstance(dash, VMobject) and dash is not gpp.tip:
                pulse(dash, base=8, amp=1.8, speed=2.8)
        self.finish()


class S12End(EndCard):
    LINE = "A flux tower measures net exchange; models split photosynthesis from respiration."
