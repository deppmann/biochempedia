"""Count the Water — Biochemistrypedia explainer.

COLOR MAP (constant throughout):
  BLUE   = freely moving bulk water
  TEAL   = the slightly stiffer interfacial water layer
  YELLOW = oily/nonpolar groups
  GREEN  = polar beads and favourable bonds/packing
  RED    = chain-freedom cost / a problem
  GOLD   = totals and the take-home idea

Only beads, blobs, dots, bars, and labelled cartoons are used; no molecular
structure is drawn.  Ledger lengths are computed from the narrated values.
"""
import math
import random

from bp_style import *  # noqa: F401,F403


ORANGE = "#FF8A5B"
GLASS_X0, GLASS_X1 = -6.35, 6.35
GLASS_Y0, GLASS_Y1 = -3.35, 3.35


def glass_world(opacity=1.0, gauge_level=0.72, seed=17, include_gauge=True):
    """The carried world: filled glass, 140 gently Brownian water dots, and gauge."""
    water_fill = Rectangle(
        width=12.7, height=6.7, stroke_color=BLUE, stroke_width=2.2,
        fill_color=BLUE, fill_opacity=0.11 * opacity,
    )
    water_fill.set_stroke(opacity=0.65 * opacity)
    depth_fill = Rectangle(
        width=12.66, height=3.22, stroke_width=0,
        fill_color=BLUE, fill_opacity=0.15 * opacity,
    ).move_to(DOWN * 1.69)
    water_fill.set_z_index(-2)
    depth_fill.set_z_index(-1)

    rng = random.Random(seed)
    dots = VGroup()
    for i in range(140):
        x = rng.uniform(-6.05, 5.0)
        y = rng.uniform(-3.08, 3.08)
        d = Dot([x, y, 0], radius=rng.uniform(0.038, 0.070), color=BLUE)
        d.set_opacity(rng.uniform(0.35, 0.78) * opacity)
        d.v = np.array([rng.uniform(-0.38, 0.38), rng.uniform(-0.32, 0.32), 0.0])
        d.phase = rng.uniform(0, TAU)
        d.age = 0.0

        def drift(m, dt, i=i):
            m.age += dt
            kick = np.array([
                0.075 * math.sin(2.1 * m.age + m.phase),
                0.065 * math.cos(1.7 * m.age + 1.4 * m.phase), 0.0,
            ])
            m.shift((m.v + kick) * dt)
            if m.get_x() < -6.08 or m.get_x() > 5.02:
                m.v[0] *= -1
                m.set_x(np.clip(m.get_x(), -6.08, 5.02))
            if m.get_y() < -3.08 or m.get_y() > 3.08:
                m.v[1] *= -1
                m.set_y(np.clip(m.get_y(), -3.08, 3.08))

        d.add_updater(drift)
        dots.add(d)

    world = VGroup(water_fill, dots, depth_fill)
    tracker = ValueTracker(gauge_level)
    if not include_gauge:
        return world, None, None

    gx, gy, gh, gw = 5.78, 0.18, 3.5, 0.48
    gauge_box = RoundedRectangle(
        width=gw, height=gh, corner_radius=0.12,
        stroke_color=BLUE, stroke_width=2.4,
        fill_color=BG, fill_opacity=0.82,
    ).move_to([gx, gy, 0])

    def gauge_fill():
        level = np.clip(tracker.get_value(), 0.05, 1.0)
        h = (gh - 0.16) * level
        return Rectangle(
            width=gw - 0.14, height=h, stroke_width=0,
            fill_color=BLUE, fill_opacity=0.85,
        ).move_to([gx, gy - (gh - 0.16) / 2 + h / 2, 0])

    fill = always_redraw(gauge_fill)
    gauge_label = T("water's\nfreedom", 30, BLUE, line_spacing=0.82).next_to(gauge_box, LEFT, buff=0.18)
    gauge_label.shift(UP * 0.45)
    schematic = T("schematic", 28, TEXT).next_to(gauge_box, DOWN, buff=0.16)
    gauge = VGroup(gauge_box, fill, gauge_label, schematic)
    world.add(gauge)
    return world, tracker, gauge


def chain_open(scale=1.0, center=ORIGIN):
    """Fourteen-bead floppy chain: eight polar, six oily."""
    pts = [
        (-3.0, 0.15), (-2.55, 0.78), (-2.0, 0.4), (-1.55, -0.35),
        (-0.95, -0.72), (-0.35, -0.25), (0.1, 0.55), (0.7, 0.88),
        (1.3, 0.35), (1.72, -0.42), (2.25, -0.72), (2.72, -0.15),
        (2.45, 0.62), (3.05, 0.85),
    ]
    pts = [center + scale * np.array([x, y, 0.0]) for x, y in pts]
    colors = [GREEN, YELLOW, GREEN, GREEN, YELLOW, GREEN, YELLOW,
              GREEN, GREEN, YELLOW, GREEN, YELLOW, GREEN, YELLOW]
    links = VGroup(*[Line(a, b, color=TEXT, stroke_width=3) for a, b in zip(pts, pts[1:])])
    beads = VGroup(*[
        Circle(radius=(0.22 if c == GREEN else 0.27) * scale,
               stroke_color=c, stroke_width=2.5, fill_color=c, fill_opacity=0.9).move_to(p)
        for p, c in zip(pts, colors)
    ])
    g = VGroup(links, beads)
    g.phase = 0.0

    def breathe(m, dt):
        m.phase += dt
        m.scale(1 + 0.0007 * math.sin(2.0 * m.phase), about_point=center)

    g.add_updater(breathe)
    return g


def chain_folded(scale=1.0, center=ORIGIN):
    oily = [(-0.45, 0.15), (0.0, 0.35), (0.42, 0.08),
            (-0.3, -0.35), (0.22, -0.4), (0.0, -0.05)]
    polar = [(0.0, 1.02), (0.72, 0.75), (1.0, 0.05), (0.7, -0.72),
             (0.0, -1.0), (-0.72, -0.72), (-1.0, 0.02), (-0.72, 0.72)]
    yellow = VGroup(*[
        Circle(radius=0.28 * scale, stroke_color=YELLOW, stroke_width=2.5,
               fill_color=YELLOW, fill_opacity=0.95).move_to(center + scale * np.array([x, y, 0]))
        for x, y in oily
    ])
    green = VGroup(*[
        Circle(radius=0.22 * scale, stroke_color=GREEN, stroke_width=2.5,
               fill_color=GREEN, fill_opacity=0.95).move_to(center + scale * np.array([x, y, 0]))
        for x, y in polar
    ])
    outline = Circle(radius=1.18 * scale, stroke_color=TEXT, stroke_width=2.5,
                     fill_color=BG, fill_opacity=0.05).move_to(center)
    g = VGroup(outline, yellow, green)
    g.phase = 0.0

    def breathe(m, dt):
        m.phase += dt
        m.scale(1 + 0.0008 * math.sin(2.4 * m.phase), about_point=center)

    g.add_updater(breathe)
    return g


SCATTER_POS = [(-3.55, 1.55), (-1.45, 1.85), (1.0, 1.45),
               (-3.15, -1.25), (-0.7, -1.55), (1.65, -1.1)]


def oily_scatter(with_layer=True):
    blobs, rings, layer_dots = VGroup(), VGroup(), VGroup()
    for j, (x, y) in enumerate(SCATTER_POS):
        p = np.array([x, y, 0.0])
        blobs.add(Circle(radius=0.38, stroke_color=YELLOW, stroke_width=2.5,
                         fill_color=YELLOW, fill_opacity=0.92).move_to(p))
        if with_layer:
            rings.add(Circle(radius=0.62, stroke_color=TEAL, stroke_width=3,
                             fill_opacity=0).move_to(p))
            for k in range(5):
                a = TAU * k / 5 + 0.2 * j
                d = Dot(p + 0.57 * np.array([math.cos(a), math.sin(a), 0]), radius=0.055, color=TEAL)
                d.phase = a
                d.t = 0.0

                def constrained(m, dt, p=p):
                    m.t += dt
                    a2 = m.phase + 0.06 * math.sin(1.4 * m.t + m.phase)
                    m.move_to(p + (0.57 + 0.015 * math.sin(2.0 * m.t)) * np.array([math.cos(a2), math.sin(a2), 0]))

                d.add_updater(constrained)
                layer_dots.add(d)
    return blobs, rings, layer_dots


def oily_cluster(center=np.array([-0.6, 0.0, 0.0])):
    offsets = [(-0.48, 0.42), (0.0, 0.5), (0.5, 0.35),
               (-0.45, -0.35), (0.08, -0.42), (0.52, -0.22)]
    blobs = VGroup(*[
        Circle(radius=0.42, stroke_color=YELLOW, stroke_width=2.5,
               fill_color=YELLOW, fill_opacity=0.95).move_to(center + np.array([x, y, 0]))
        for x, y in offsets
    ])
    ring = Circle(radius=1.28, stroke_color=TEAL, stroke_width=4).move_to(center)
    layer = VGroup()
    for k in range(12):
        a = TAU * k / 12
        p = center + 1.2 * np.array([math.cos(a), math.sin(a), 0])
        layer.add(Dot(p, radius=0.06, color=TEAL))
    return blobs, ring, layer


def question_card():
    q = T("Water's entropy: up or down?", 36, GOLD)
    box = RoundedRectangle(width=q.width + 0.55, height=q.height + 0.38,
                           corner_radius=0.16, stroke_color=GOLD, stroke_width=2.5,
                           fill_color=BG, fill_opacity=0.9)
    card = VGroup(box, q.move_to(box)).move_to(UP * 2.78 + LEFT * 0.45)
    arrows = VGroup(T("↑", 52, GOLD), T("↓", 52, GOLD)).arrange(RIGHT, buff=0.25)
    arrows.next_to(card, DOWN, buff=0.12)
    arrows.phase = 0.0

    def pulse(m, dt):
        m.phase += dt
        m.set_opacity(0.72 + 0.25 * (0.5 + 0.5 * math.sin(2.2 * m.phase)))

    arrows.add_updater(pulse)
    return card, arrows


def heat_waves(start, end, count=3, color=ORANGE):
    waves = VGroup()
    for j in range(count):
        yoff = (j - (count - 1) / 2) * 0.28
        pts = []
        for k in range(25):
            u = k / 24
            p = interpolate(np.array(start), np.array(end), u)
            p[1] += yoff + 0.08 * math.sin(6 * PI * u)
            pts.append(p)
        waves.add(VMobject(stroke_color=color, stroke_width=3).set_points_smoothly(pts))
    return waves


def small_glass_and_folded():
    box = Rectangle(width=2.65, height=5.4, stroke_color=BLUE, stroke_width=2.2,
                    fill_color=BLUE, fill_opacity=0.065).move_to(LEFT * 4.85)
    folded = chain_folded(0.72, LEFT * 4.85)
    dots = VGroup()
    rng = random.Random(51)
    for i in range(45):
        d = Dot([rng.uniform(-5.95, -3.75), rng.uniform(-2.4, 2.4), 0], radius=0.060, color=BLUE)
        d.set_opacity(0.65)
        d.t, d.ph = 0.0, rng.uniform(0, TAU)
        d.v = np.array([rng.uniform(-0.52, 0.52), rng.uniform(-0.46, 0.46), 0])

        def small_drift(m, dt):
            m.t += dt
            m.shift((m.v + np.array([0.05 * math.sin(m.t + m.ph),
                                     0.04 * math.cos(1.4*m.t + m.ph), 0])) * dt)
            if m.get_x() < -5.98 or m.get_x() > -3.72:
                m.v[0] *= -1
            if m.get_y() < -2.42 or m.get_y() > 2.42:
                m.v[1] *= -1

        d.add_updater(small_drift)
        dots.add(d)
    return VGroup(box, dots), folded


def ledger_geometry(water=-500, packing=-90, entropy_mode=False):
    """Cumulative ledger using 0.008 scene units per kJ/mol."""
    zero_x, scale = -1.05, 0.008
    chain = 550
    start_red, end_red = zero_x, zero_x + chain * scale
    end_water = end_red + water * scale
    end_pack = end_water + packing * scale
    red = Line([start_red, 1.15, 0], [end_red, 1.15, 0], color=RED, stroke_width=20)
    blue = Line([end_red, 0.0, 0], [end_water, 0.0, 0], color=BLUE, stroke_width=20)
    green = Line([end_water, -1.15, 0], [end_pack, -1.15, 0], color=GREEN, stroke_width=20)
    connectors = VGroup(
        DashedLine([end_red, 0.93, 0], [end_red, 0.22, 0], color=GREY, dash_length=0.08),
        DashedLine([end_water, -0.22, 0], [end_water, -0.93, 0], color=GREY, dash_length=0.08),
    )
    axis = Line([zero_x, -2.05, 0], [zero_x, 2.1, 0], color=TEXT, stroke_width=3)
    return dict(zero=zero_x, scale=scale, red=red, blue=blue, green=green,
                connectors=connectors, axis=axis, end=end_pack,
                end_red=end_red, end_water=end_water)


class S00Hook(SpokenScene):
    def construct(self):
        world, tracker, gauge = glass_world(include_gauge=True)
        world.remove(gauge)
        chain = chain_open(0.85, LEFT * 0.45)
        self.add(world, chain)
        self.at("folds itself")
        folded = chain_folded(1.15, LEFT * 0.45)
        self.play(ReplacementTransform(chain, folded), run_time=2.0)
        self.at("second loss")
        law = chip("second law: disorder wins?", RED, 32).move_to(UP * 2.55 + LEFT * 0.55)
        mark = T("?", 52, RED).next_to(folded, RIGHT, buff=0.5)
        self.play(FadeIn(law, shift=DOWN * 0.25), GrowFromCenter(mark), run_time=0.7)
        self.play(mark.animate.scale(1.18), rate_func=there_and_back, run_time=0.65)
        self.at("Watch the water")
        open_again = chain_open(0.92, LEFT * 0.45)
        self.play(ReplacementTransform(folded, open_again), FadeOut(law), FadeOut(mark),
                  FadeIn(gauge), run_time=1.2)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Water & weak bonds"
    TITLE = "Count the Water"

    def construct(self):
        world, _, _ = glass_world(opacity=0.25, include_gauge=False)
        full_world, _, _ = glass_world(opacity=1.0, include_gauge=False)
        chain = chain_open(0.85, LEFT * 0.45).set_opacity(0.25)
        brand = T("BIOCHEMISTRYPEDIA", 20, TEAL, weight=BOLD)
        title = T(self.TITLE, 54, font=TITLE_FONT)
        rule = Line(LEFT * 1.3, RIGHT * 1.3, color=GOLD, stroke_width=4)
        card = VGroup(brand, title, rule).arrange(DOWN, buff=0.38)
        self.add(world, chain)
        self.play(FadeIn(card), run_time=0.45)
        self.wait(1.1)
        full_chain = chain_open(0.85, LEFT * 0.45)
        self.play(FadeOut(card), FadeOut(world), FadeOut(chain), FadeIn(full_world),
                  FadeIn(full_chain), run_time=0.4)
        self.finish()


class S02Count(SpokenScene):
    def construct(self):
        world, _, _ = glass_world(gauge_level=0.72)
        chain = chain_open(0.72, LEFT * 0.8)
        self.add(world, chain)
        self.at("total entropy")
        brace = BraceBetweenPoints(LEFT * 4.8 + UP * 2.75, RIGHT * 4.55 + UP * 2.75,
                                   direction=DOWN, color=GOLD)
        total = T("total entropy", 32, GOLD).next_to(brace, UP, buff=0.12)
        self.play(GrowFromCenter(brace), FadeIn(total), run_time=0.7)
        self.at("the protein")
        protein = chip("protein", GREEN, 32).move_to(LEFT * 1.0 + UP * 1.3)
        self.play(FadeIn(protein, shift=DOWN * 0.2), run_time=0.55)
        self.at("the water around")
        water = chip("water", BLUE, 32).move_to(LEFT * 3.85 + DOWN * 1.7)
        self.play(FadeIn(water, shift=UP * 0.2), world[1].animate.set_opacity(1), run_time=0.7)
        self.at("heat they trade")
        surround = chip("surroundings", ORANGE, 30).move_to(RIGHT * 4.2 + DOWN * 1.65)
        waves = heat_waves([1.7, -1.0, 0], [3.35, -1.45, 0], 2)
        heat = T("heat", 32, ORANGE).next_to(waves, UP, buff=0.05)
        self.play(Create(waves), FadeIn(heat), FadeIn(surround), run_time=0.9)
        self.at("Count the water")
        rule = T("Count the water", 42, GOLD).move_to(DOWN * 2.65 + LEFT * 0.6)
        self.play(
            FadeOut(VGroup(protein, surround, waves, heat)),
            water.animate.scale(1.25), Write(rule), run_time=0.9,
        )
        self.play(FadeOut(water), run_time=0.35)
        self.finish()


class S03Layer(SpokenScene):
    def construct(self):
        world, tracker, _ = glass_world(gauge_level=0.72, seed=23)
        blob = Circle(radius=1.35, stroke_color=YELLOW, stroke_width=4,
                      fill_color=YELLOW, fill_opacity=0.9).move_to(LEFT * 0.55)
        label = T("methyl group\n(oily)", 30, BG, weight=BOLD, line_spacing=0.82).move_to(blob)
        self.add(world, blob, label)
        self.at("cannot hydrogen bond")
        test = DashedLine(LEFT * 3.2 + UP * 0.8, blob.get_left() + UP * 0.35,
                          color=TEXT, stroke_width=4, dash_length=0.12)
        cross = T("×", 48, RED).move_to(blob.get_left() + LEFT * 0.25 + UP * 0.35)
        self.play(Create(test), run_time=0.45)
        self.play(FadeOut(test), GrowFromCenter(cross), run_time=0.4)
        self.at("points its bonds")
        layer, ticks = VGroup(), VGroup()
        for k in range(16):
            a = TAU * k / 16
            p = blob.get_center() + 1.63 * np.array([math.cos(a), math.sin(a), 0])
            d = Dot(p, radius=0.075, color=TEAL)
            tangent = np.array([-math.sin(a), math.cos(a), 0])
            tick = Line(p - 0.13 * tangent, p + 0.13 * tangent, color=TEXT, stroke_width=3)
            d.t, d.a = 0.0, a
            d.add_updater(lambda m, dt, c=blob.get_center(): (setattr(m, "t", m.t + dt), m.move_to(c + (1.63 + 0.018*math.sin(1.5*m.t+m.a))*np.array([math.cos(m.a), math.sin(m.a), 0])))[-1])
            layer.add(d); ticks.add(tick)
        self.play(FadeOut(cross), LaggedStart(*[FadeIn(d) for d in layer], lag_ratio=0.03),
                  LaggedStart(*[GrowFromCenter(t) for t in ticks], lag_ratio=0.03), run_time=1.2)
        self.at("fewer ways to arrange")
        stiff = T("stiffer layer", 32, TEAL).move_to(RIGHT * 3.5 + UP * 1.7)
        pointer = Arrow(stiff.get_left(), blob.get_center() + RIGHT * 1.6 + UP * 0.75,
                        buff=0.12, color=TEAL, stroke_width=4)
        self.play(FadeIn(stiff), GrowArrow(pointer), run_time=0.65)
        self.at("lower entropy")
        self.play(tracker.animate.set_value(0.58), run_time=0.8)
        self.finish()


class S04NotCage(SpokenScene):
    def construct(self):
        world, tracker, _ = glass_world(gauge_level=0.58, seed=23)
        blob = Circle(radius=1.35, stroke_color=YELLOW, stroke_width=4,
                      fill_color=YELLOW, fill_opacity=0.9).move_to(LEFT * 0.55)
        layer = Circle(radius=1.65, stroke_color=TEAL, stroke_width=4).move_to(blob)
        self.add(world, blob, layer)
        self.at("ice cage")
        cage = RegularPolygon(8, radius=1.82, color=TEXT, stroke_width=5).move_to(blob)
        cage_lab = T("textbook ice cage", 30, TEXT).move_to(LEFT * 3.9 + UP * 2.25)
        self.play(Create(cage), FadeIn(cage_lab), run_time=0.75)
        self.at("overstates it")
        strike = Line(cage.get_corner(DL), cage.get_corner(UR), color=RED, stroke_width=9)
        self.play(Create(strike), run_time=0.35)
        self.play(FadeOut(cage), FadeOut(cage_lab), FadeOut(strike), run_time=0.45)
        self.at("slightly stiffer")
        bulk_bar = Rectangle(width=0.75, height=1.4, stroke_color=BLUE, fill_color=BLUE,
                             fill_opacity=0.75).move_to(RIGHT * 2.1 + DOWN * 1.35)
        layer_bar = Rectangle(width=0.75, height=1.65, stroke_color=TEAL, fill_color=TEAL,
                              fill_opacity=0.75).next_to(bulk_bar, RIGHT, buff=0.35).align_to(bulk_bar, DOWN)
        labs = VGroup(T("bulk", 28, BLUE).next_to(bulk_bar, DOWN, buff=0.1),
                      T("layer", 28, TEAL).next_to(layer_bar, DOWN, buff=0.1),
                      T("schematic", 28, TEXT).next_to(VGroup(bulk_bar, layer_bar), UP, buff=0.12))
        self.play(GrowFromEdge(bulk_bar, DOWN), GrowFromEdge(layer_bar, DOWN), FadeIn(labs), run_time=0.8)
        self.at("many oily groups")
        blobs, rings, ldots = oily_scatter()
        close = VGroup(blob, layer, bulk_bar, layer_bar, labs)
        self.play(FadeOut(close), FadeIn(blobs), FadeIn(rings), FadeIn(ldots), run_time=0.8)
        for level, ring in zip([0.53, 0.49, 0.45, 0.41, 0.37, 0.32], rings):
            self.play(Flash(ring, color=TEAL, line_length=0.12, flash_radius=0.72),
                      tracker.animate.set_value(level), run_time=0.35)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        world, tracker, _ = glass_world(gauge_level=0.32, seed=17)
        blobs, rings, ldots = oily_scatter()
        self.add(world, blobs, rings, ldots)
        self.at("gather the scattered")
        target = np.array([-0.6, 0.0, 0])
        arrows = VGroup(*[
            DashedLine(b.get_center(), target, color=GOLD, stroke_width=2.5,
                       dash_length=0.12).set_opacity(0.55)
            for b in blobs
        ])
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.08), run_time=0.9)
        self.at("water's entropy")
        card, choices = question_card()
        self.play(FadeIn(card), FadeIn(choices), run_time=0.6)
        self.at("Up or down")
        self.play(tracker.animate.set_value(0.35), rate_func=there_and_back, run_time=0.8)
        self.finish()


class S06Think(Scene):
    def construct(self):
        world, tracker, _ = glass_world(gauge_level=0.32, seed=17)
        blobs, rings, ldots = oily_scatter()
        target = np.array([-0.6, 0.0, 0])
        arrows = VGroup(*[
            DashedLine(b.get_center(), target, color=GOLD, stroke_width=2.5,
                       dash_length=0.12).set_opacity(0.55)
            for b in blobs
        ])
        card, choices = question_card()
        self.add(world, blobs, rings, ldots, arrows, card, choices)
        self.wait(4.5)


class S07Release(SpokenScene):
    def construct(self):
        world, tracker, _ = glass_world(gauge_level=0.32, seed=17)
        blobs, rings, ldots = oily_scatter()
        target = np.array([-0.6, 0.0, 0])
        arrows = VGroup(*[DashedLine(b.get_center(), target, color=GOLD, stroke_width=2.5,
                                    dash_length=0.12).set_opacity(0.55) for b in blobs])
        card, choices = question_card()
        self.add(world, blobs, rings, ldots, arrows, card, choices)
        self.at("It goes up")
        up = T("↑", 80, GOLD).move_to(UP * 2.5 + LEFT * 0.5)
        self.play(FadeOut(card), FadeOut(choices), GrowFromCenter(up), run_time=0.5)
        self.play(up.animate.scale(1.2), rate_func=there_and_back, run_time=0.45)
        self.at("less surface")
        cblobs, cring, clayer = oily_cluster(target)
        self.play(ReplacementTransform(blobs, cblobs), ReplacementTransform(rings, cring),
                  ReplacementTransform(ldots, clayer), FadeOut(arrows), FadeOut(up), run_time=1.35)
        less = T("less surface", 32, TEAL).move_to(LEFT * 3.45 + UP * 1.55)
        ptr = Arrow(less.get_right(), cring.get_left() + UP * 0.6, color=TEAL, buff=0.12)
        self.play(FadeIn(less), GrowArrow(ptr), run_time=0.5)
        self.at("freed water")
        freed = VGroup(*[Dot(target + 1.2*np.array([math.cos(TAU*k/12), math.sin(TAU*k/12), 0]),
                                  radius=0.065, color=TEAL) for k in range(12)])
        self.add(freed)
        destinations = [target + np.array([2.2*math.cos(TAU*k/12), 2.35*math.sin(TAU*k/12), 0]) for k in range(12)]
        self.play(*[d.animate.set_color(BLUE).move_to(p) for d, p in zip(freed, destinations)],
                  tracker.animate.set_value(0.78), run_time=1.3)
        self.at("mainly because the water")
        gain = T("water gains freedom", 32, BLUE).move_to(RIGHT * 2.55 + UP * 1.75)
        gain_arr = Arrow(gain.get_right(), [5.45, 1.35, 0], color=BLUE, buff=0.1)
        self.play(FadeOut(VGroup(less, ptr)), FadeIn(gain), GrowArrow(gain_arr), run_time=0.65)
        self.at("not because they attract")
        weak = T("weak attraction", 30, YELLOW).move_to(DOWN * 2.35 + LEFT * 0.55)
        weak_link = Line(target + LEFT * 0.5, target + RIGHT * 0.5, color=YELLOW,
                         stroke_width=3)
        self.play(FadeOut(VGroup(gain, gain_arr)), FadeIn(weak), Create(weak_link), run_time=0.55)
        self.finish()


class S08Name(SpokenScene):
    def construct(self):
        world, _, _ = glass_world(gauge_level=0.78, seed=17)
        blobs, ring, layer = oily_cluster(np.array([0.55, -0.35, 0]))
        self.add(world, blobs, ring, layer)
        self.at("hydrophobic effect")
        title = chip("hydrophobic effect", GOLD, 40).move_to(UP * 2.55 + RIGHT * 0.5)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.65)
        self.at("almost all entropy")
        bar_box = Rectangle(width=1.25, height=3.35, stroke_color=TEXT, stroke_width=2).move_to(LEFT * 3.8 + DOWN * 0.25)
        entropy = Rectangle(width=1.15, height=2.85, stroke_width=0, fill_color=BLUE,
                            fill_opacity=0.88).move_to(bar_box).align_to(bar_box, DOWN).shift(UP * 0.05)
        enthalpy = Rectangle(width=1.15, height=0.38, stroke_width=0, fill_color=ORANGE,
                             fill_opacity=0.9).next_to(entropy, UP, buff=0)
        entropy_lab = T("entropy", 30, TEXT).move_to(entropy)
        enthalpy_lab = T("enthalpy", 30, ORANGE).next_to(bar_box, RIGHT, buff=0.15).align_to(enthalpy, UP)
        schematic = T("schematic", 28, TEXT).next_to(bar_box, DOWN, buff=0.12)
        self.remove(title)
        self.play(Create(bar_box), GrowFromEdge(entropy, DOWN), GrowFromEdge(enthalpy, DOWN),
                  FadeIn(entropy_lab), FadeIn(enthalpy_lab), FadeIn(schematic), run_time=1.0)
        self.at("higher temperatures")
        thermo = VGroup(Line(LEFT*0.0, UP*1.4, color=ORANGE, stroke_width=8),
                        Circle(radius=0.18, fill_color=ORANGE, fill_opacity=1, stroke_color=ORANGE)).arrange(DOWN, buff=-0.05)
        thermo.move_to(LEFT * 2.35 + DOWN * 0.35)
        hot = Rectangle(width=1.15, height=1.05, stroke_width=0, fill_color=ORANGE, fill_opacity=0.9).move_to(bar_box).align_to(bar_box, UP).shift(DOWN*0.05)
        cool = Rectangle(width=1.15, height=2.18, stroke_width=0, fill_color=BLUE, fill_opacity=0.88).move_to(bar_box).align_to(bar_box, DOWN).shift(UP*0.05)
        self.play(FadeIn(thermo), Transform(enthalpy, hot), Transform(entropy, cool), run_time=1.0)
        self.at("large flat surfaces")
        slab = RoundedRectangle(width=3.8, height=0.85, corner_radius=0.35,
                                stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                                fill_opacity=0.9).move_to(RIGHT * 0.55 + DOWN * 0.35)
        self.play(ReplacementTransform(VGroup(blobs, ring, layer), slab), run_time=0.8)
        self.play(ReplacementTransform(slab, VGroup(*oily_cluster(np.array([0.55, -0.35, 0])))), run_time=0.8)
        self.finish()


class S09Ledger(SpokenScene):
    def construct(self):
        glass, folded = small_glass_and_folded()
        open_chain = chain_open(0.34, LEFT * 4.85)
        self.add(glass, open_chain)
        self.at("Fold a small protein")
        self.play(ReplacementTransform(open_chain, folded), run_time=1.2)
        geo = ledger_geometry()
        header = T("100 residues, ~25 °C, rounded", 28, TEXT).move_to(RIGHT * 1.25 + UP * 2.85)
        key = T("+ opposes, − favors", 28, TEXT).move_to(RIGHT * 2.6 + DOWN * 2.75)
        units = T("kJ/mol", 28, TEXT).move_to(LEFT * 0.2 + DOWN * 2.75)
        zero = T("0", 28, TEXT).next_to(geo["axis"], DOWN, buff=0.05)
        self.at("hundred residues")
        self.play(FadeIn(header), run_time=0.45)
        self.at("round numbers")
        self.play(Create(geo["axis"]), FadeIn(zero), FadeIn(key), FadeIn(units), run_time=0.75)
        self.at("lost freedom costs")
        lr = T("chain's lost freedom  +550", 30, RED).next_to(geo["red"], UP, buff=0.12)
        self.play(Create(geo["red"]), FadeIn(lr), run_time=1.0)
        self.at("Freed water")
        lb = T("freed water  −500", 30, BLUE).next_to(geo["blue"], UP, buff=0.12)
        self.play(Create(geo["connectors"][0]), Create(geo["blue"]), FadeIn(lb), run_time=1.0)
        self.at("Bonds and packing")
        lg = T("bonds, packing  −90", 30, GREEN).next_to(geo["green"], UP, buff=0.12)
        self.play(Create(geo["connectors"][1]), Create(geo["green"]), FadeIn(lg), run_time=0.9)
        self.finish()


class S10Margin(SpokenScene):
    def construct(self):
        glass, folded = small_glass_and_folded()
        geo = ledger_geometry()
        labels = VGroup(
            T("chain  +550", 30, RED).next_to(geo["red"], UP, buff=0.12),
            T("water  −500", 30, BLUE).next_to(geo["blue"], UP, buff=0.12),
            T("packing  −90", 30, GREEN).next_to(geo["green"], UP, buff=0.12),
        )
        self.add(glass, folded, geo["axis"], geo["connectors"], geo["red"], geo["blue"], geo["green"], labels)
        self.at("total is")
        total = Line([geo["zero"], -2.0, 0], [geo["end"], -2.0, 0], color=GOLD, stroke_width=16)
        total_lab = T("total about −40", 32, GOLD).move_to([0.35, -2.0, 0])
        self.play(Create(total), FadeIn(total_lab), run_time=0.65)
        self.at("small difference")
        big = BraceBetweenPoints([geo["zero"], 1.95, 0], [geo["end_red"], 1.95, 0], direction=UP, color=GOLD)
        big_lab = T("big numbers", 30, GOLD).next_to(big, UP, buff=0.08)
        self.play(GrowFromCenter(big), FadeIn(big_lab), run_time=0.65)
        self.at("10 percent")
        changed = ledger_geometry(water=-450)
        old = DashedLine(geo["blue"].get_start(), geo["blue"].get_end(), color=BLUE,
                         stroke_width=3, dash_length=0.1).set_opacity(0.45)
        new_total = Line([changed["zero"], -2.0, 0], [changed["end"], -2.0, 0], color=RED, stroke_width=16)
        new_lab = T("total +10", 32, RED).move_to([0.35, -2.0, 0])
        self.add(old)
        self.play(Transform(geo["blue"], changed["blue"]), Transform(geo["green"], changed["green"]),
                  Transform(total, new_total), Transform(total_lab, new_lab), run_time=1.0)
        self.at("more than its own size")
        self.play(
            Indicate(VGroup(geo["blue"], labels[1]), color=RED, scale_factor=1.03),
            Indicate(VGroup(total, total_lab), color=RED, scale_factor=1.08),
            run_time=0.75,
        )
        self.at("one bad mutation")
        open_chain = chain_open(0.34, LEFT * 4.85)
        self.play(ReplacementTransform(folded, open_chain), run_time=0.75)
        restored = ledger_geometry()
        restored_total = Line([restored["zero"], -2.0, 0], [restored["end"], -2.0, 0], color=GOLD, stroke_width=16)
        restored_lab = T("total about −40", 32, GOLD).move_to([0.35, -2.0, 0])
        self.play(Transform(geo["blue"], restored["blue"]), Transform(geo["green"], restored["green"]),
                  Transform(total, restored_total), Transform(total_lab, restored_lab), FadeOut(old),
                  ReplacementTransform(open_chain, chain_folded(0.72, LEFT * 4.85)), run_time=1.0)
        self.finish()


class S11SecondLaw(SpokenScene):
    def construct(self):
        glass, folded = small_glass_and_folded()
        geo = ledger_geometry(water=-480, packing=0)
        header = T("near 25 °C, round numbers", 28, TEXT).move_to(RIGHT * 0.9 + UP * 2.85)
        red_lab = T("chain entropy cost  +550", 30, RED).next_to(geo["red"], UP, buff=0.12)
        blue_lab = T("water entropy gain  −480", 30, BLUE).next_to(geo["blue"], UP, buff=0.12)
        gap = Line([geo["end_water"], -0.72, 0], [geo["zero"], -0.72, 0], color=RED, stroke_width=10)
        gap_lab = T("a little short", 30, RED).next_to(gap, UP, buff=0.12)
        self.add(glass, folded, header, geo["axis"], geo["red"], red_lab)
        self.at("water's entropy gain")
        self.play(Create(geo["connectors"][0]), Create(geo["blue"]), FadeIn(blue_lab), run_time=1.35)
        self.at("most of the chain's loss")
        self.play(Indicate(geo["red"], color=RED, scale_factor=1.02),
                  Indicate(geo["blue"], color=BLUE, scale_factor=1.02), run_time=1.0)
        self.at("not quite all")
        self.play(Create(gap), FadeIn(gap_lab), run_time=0.75)
        self.at("bonds inside release heat")
        surround = chip("surroundings", ORANGE, 30).move_to(RIGHT * 4.6 + DOWN * 2.25)
        waves = heat_waves([-3.65, -1.65, 0], [3.65, -2.15, 0], 3)
        self.play(Create(waves), FadeIn(surround), run_time=1.0)
        self.at("raises the entropy")
        gold_start = geo["end_water"]
        gold_end = gold_start - 0.85
        surroundings = Line([gold_start, -1.45, 0], [gold_end, -1.45, 0], color=GOLD, stroke_width=18)
        surroundings_lab = T("surroundings", 30, GOLD).next_to(surroundings, RIGHT, buff=0.25)
        self.remove(gap_lab, waves, surround)
        self.play(Create(surroundings), FadeIn(surroundings_lab), run_time=0.8)
        self.at("total entropy rises")
        brace = BraceBetweenPoints(LEFT * 5.8 + UP * 3.15, RIGHT * 5.25 + UP * 3.15,
                                   direction=DOWN, color=GOLD)
        total = T("total entropy  ↑", 36, GOLD).next_to(brace, DOWN, buff=0.1)
        self.play(FadeOut(header), GrowFromCenter(brace), FadeIn(total), run_time=0.75)
        self.finish()


class S12Return(SpokenScene):
    def construct(self):
        world, tracker, _ = glass_world(gauge_level=0.78, seed=17)
        folded = chain_folded(1.35, LEFT * 0.65)
        ring = Circle(radius=1.72, stroke_color=TEAL, stroke_width=3).move_to(LEFT * 0.65)
        brace = BraceBetweenPoints(LEFT * 4.8 + UP * 2.8, RIGHT * 4.55 + UP * 2.8,
                                   direction=DOWN, color=GOLD)
        total = T("total entropy  ↑", 34, GOLD).next_to(brace, DOWN, buff=0.1)
        self.add(world, folded, ring, brace, total)
        self.at("not broken")
        self.play(Indicate(total, color=GOLD, scale_factor=1.12), run_time=0.75)
        self.at("order is not free")
        cost = T("order has a cost", 32, RED).move_to(LEFT * 3.9 + DOWN * 2.45)
        self.play(FadeIn(cost), run_time=0.55)
        self.at("pays most of the bill")
        water_bar = Rectangle(width=2.2, height=0.38, stroke_width=0, fill_color=BLUE,
                              fill_opacity=0.9).move_to(RIGHT * 2.8 + DOWN * 0.65)
        packing_bar = Rectangle(width=0.75, height=0.38, stroke_width=0, fill_color=GREEN,
                                fill_opacity=0.9).next_to(water_bar, DOWN, buff=0.22).align_to(water_bar, LEFT)
        bill = T("most of the bill", 30, BLUE).next_to(water_bar, UP, buff=0.12)
        self.play(GrowFromEdge(water_bar, LEFT), GrowFromEdge(packing_bar, LEFT), FadeIn(bill),
                  FadeOut(cost), run_time=0.9)
        self.at("oily surfaces hide")
        self.play(folded.animate.scale(1.12), ring.animate.scale(1.08), tracker.animate.set_value(0.88),
                  FadeOut(VGroup(water_bar, packing_bar, bill)), run_time=0.9)
        self.finish()


class S13End(EndCard):
    LINE = "In this ledger, water pays most of the bill."

    def construct(self):
        world, _, _ = glass_world(opacity=0.30, include_gauge=False)
        line = T(self.LINE, 40, GOLD, font=TITLE_FONT).shift(UP * 0.45)
        fit(line, max_w=11.5)
        sub = T("biochemistrypedia.com", 24, TEAL).next_to(line, DOWN, buff=0.45)
        self.add(world)
        self.play(FadeIn(line, shift=UP * 0.15), FadeIn(sub, shift=UP * 0.1), run_time=0.65)
        self.finish()
