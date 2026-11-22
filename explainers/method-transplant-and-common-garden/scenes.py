"""Common garden, reciprocal transplant, and cross-fostering.

COLOR MAP: orange/blue = lowland/highland origin (warm/cool also distinguish
finch lineages); green = shared or supporting conditions; red = reduced fitness
and the red monkeyflower; purple = pink-violet monkeyflower; yellow = transfers
and active comparisons; gold/green = genetic/foster parent slopes; gold also
marks questions and take-home rules; grey = structure.
"""
from bp_parts import *
from bp_style import EndCard

ORANGE = "#F29E4C"
PURPLE = "#D6A0E5"
EARTH = "#384544"
RIDGE = "#2B373F"
WATER = "#427583"
BARK = "#88705C"
LEAF = "#719D73"
SITES = ((-4.35, -1.83), (4.25, -0.27))
GARDEN = (0, -1.72)
BIRD_SITES = ((-3.65, -0.38), (3.65, -0.38))
PROMPT = "Genes alone: which slope rises?"


def pt(x, y):
    return np.array([x, y, 0.0])


def solid(points, color, opacity=1):
    return Polygon(*(pt(x, y) for x, y in points), stroke_width=0,
                   fill_color=color, fill_opacity=opacity)


def disk(x, y, radius, color):
    return Dot(pt(x, y), radius=radius, color=color)


def oval(x, y, width, height, color, angle=0):
    return Ellipse(width=width, height=height, stroke_width=0,
                   fill_color=color, fill_opacity=1).rotate(angle).move_to(pt(x, y))


def path(points, color, width=3):
    return VMobject().set_points_smoothly([pt(x, y) for x, y in points]).set_stroke(color, width)


def heading(text, y=3.17, x=0, color=TEXT, size=38):
    return T(text, size, color, weight=BOLD).move_to(pt(x, y))


def field_tag():
    return scope_tag(size=28, color=TEXT).set_z_index(3)


def breeze():
    wisps = VGroup()
    for i in range(11):
        x = -5.9 + (i * 1.47) % 11.5
        y = -2.95 + (i * 0.47) % 3.15
        wisp = oval(x, y, 0.64 + 0.18 * (i % 3), 0.085, WATER, 0.14)
        bob(wisp, amp=0.38, speed=1.26 + 0.14 * (i % 4), seed=i)
        wisps.add(wisp)
    return wisps


def mountain():
    rear = solid([(-6.7, -1.35), (-5.15, -0.58), (-3.85, 0.18), (-2.75, -0.37),
                  (-1.05, 0.75), (0.05, 0.28), (2.33, 2.42), (3.0, 1.99),
                  (4.80, 2.46), (6.7, 0.86), (6.7, -3.64), (-6.7, -3.64)], RIDGE)
    face = solid([(-6.7, -1.92), (-4.25, -1.80), (-2.65, -1.97), (-0.9, -1.51),
                  (1.0, -1.16), (2.98, -0.16), (4.42, -0.23), (6.7, 0.51),
                  (6.7, -3.64), (-6.7, -3.64)], EARTH)
    river = solid([(-6.68, -3.6), (-6.65, -3.17), (-3.55, -2.68), (-1.67, -2.85),
                   (0.34, -2.22), (2.15, -1.75), (3.43, -0.52), (3.76, -0.44),
                   (2.51, -1.94), (0.67, -2.52), (-1.42, -3.34), (-3.26, -3.13),
                   (-4.55, -3.6)], "#405D5B")
    return VGroup(rear, face, river, breeze())


def sprig(x, y, color, height=1.68, broad=True, animate=False, phase=0):
    leaf_width = 0.56 if broad else 0.30
    stem = path([(0, 0), (-0.06, 0.37), (0.03, 0.76), (0.13, 1.05)], LEAF, 5)
    leaves = VGroup()
    for i, (ly, side) in enumerate(((0.2, -1), (0.39, 1), (0.55, -1), (0.73, 1))):
        leaves.add(oval(side * leaf_width * 0.47, ly + 0.12, leaf_width, 0.18,
                        LEAF, side * 0.52))
    petals = VGroup(*[disk(0.13 + 0.13 * np.cos(a), 1.04 + 0.13 * np.sin(a),
                           0.133 if broad else 0.098, color)
                      for a in np.linspace(0, TAU, 5 if broad else 4, endpoint=False)])
    bloom = VGroup(stem, leaves, petals, disk(0.13, 1.04, 0.067, YELLOW))
    bloom.scale_to_fit_height(height)
    bloom.move_to(pt(x, y), aligned_edge=DOWN)
    if animate:
        root = pt(x, y)
        motion = [phase, 0.0]

        def sway(mob, dt):
            motion[0] += dt
            angle = 0.145 * np.sin(1.55 * motion[0])
            mob.rotate(angle - motion[1], about_point=root)
            motion[1] = angle

        bloom.add_updater(sway)
    return bloom


def meadow():
    return VGroup(*[sprig(x + dx, y, color, h, broad, True, i * 1.3)
                    for (x, y), color, broad, heights in
                    [(SITES[0], ORANGE, True, (1.18, 1.68, 1.36)),
                     (SITES[1], BLUE, False, (1.67, 2.36, 1.93))]
                    for i, (dx, h) in enumerate(zip((-0.83, 0, 0.83), heights))])


def bed(x, y, width=2.65, color=GREEN):
    soil = oval(x, y - 0.14, width, 0.52, "#80614E")
    rim = Ellipse(width=width, height=0.48, stroke_color=color, stroke_width=3).move_to(soil)
    furrows = VGroup(*[Line(pt(x + k * width / 8 - 0.16, y - 0.23),
                             pt(x + k * width / 8 + 0.16, y - 0.06),
                             color="#B88D65", stroke_width=3)
                       for k in (-2, -1, 0, 1, 2)])
    return VGroup(soil, rim, furrows)


def shared_plants(look="different", animate=False):
    if look == "different":
        heights, shapes = (1.68, 2.38), (True, False)
    elif look == "alike":
        heights, shapes = (2.06, 2.06), (True, True)
    else:
        heights, shapes = (1.48, 2.27, 1.85), (True, True, True)
        return VGroup(*[sprig(x, GARDEN[1], ORANGE, h, shape, animate, i)
                        for i, (x, h, shape) in enumerate(zip((-1.22, 0, 1.22), heights, shapes))])
    return VGroup(*(sprig(x, GARDEN[1], c, h, shape, animate, i * 1.4)
                    for i, (x, c, h, shape) in enumerate(zip((-0.95, 0.95), (ORANGE, BLUE), heights, shapes))))


def seed(x, y, color):
    return oval(x, y, 0.34, 0.21, color, 0.45)


def curved(a, b, angle, color=YELLOW):
    return CurvedArrow(pt(*a), pt(*b), angle=angle, color=color, stroke_width=5, tip_length=0.22)


def weather():
    sun = disk(-0.82, 1.13, 0.25, YELLOW)
    rays = VGroup(*[Line(sun.get_center() + 0.34 * np.array([np.cos(a), np.sin(a), 0]),
                          sun.get_center() + 0.49 * np.array([np.cos(a), np.sin(a), 0]),
                          color=YELLOW, stroke_width=3)
                    for a in np.linspace(0, TAU, 8, endpoint=False)])
    rain = VGroup(*(oval(0.63 + i * 0.22, 1.31, 0.32, 0.23, BLUE) for i in range(3)),
                  *(oval(0.61 + i * 0.23, 0.97 - 0.08 * (i % 2), 0.071, 0.24, BLUE, -0.28)
                    for i in range(3)))
    return VGroup(bob(VGroup(sun, rays), amp=0.12), bob(rain, amp=0.15, seed=2))


class S01Hook(SpokenScene):
    def construct(self):
        self.at("plants on a mountain")
        self.add(mountain(), meadow(), field_tag())
        arrows = VGroup(curved((-4.25, 0.13), (-2.47, 2.62), -0.33),
                        curved((3.2, 1.95), (2.64, 2.65), 0.33))
        question = heading("Genes or surroundings?", y=3.02, size=47, color=GOLD)
        self.at("are those differences", lead=1.42)
        self.play(LaggedStart(*(Create(a) for a in arrows), lag_ratio=0.22), run_time=0.7)
        self.play(FadeIn(question, shift=0.12 * UP), run_time=0.48)
        self.at("watching them in place")
        self.play(FadeOut(arrows), run_time=0.7)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Common garden and reciprocal transplant experiments"
    TITLE = "Genes or Surroundings? Moving Organisms to Find Out"

    def construct(self):
        self.add(mountain(), meadow())
        title = T(self.TITLE.replace("? ", "?\n"), 48, TEXT, font=TITLE_FONT,
                  line_spacing=0.9).move_to(pt(-1.40, 2.51))
        lesson = T(self.LESSON.replace(" reciprocal", "\nreciprocal"), 28, TEXT,
                   line_spacing=0.9).move_to(pt(-2.65, 1.10))
        self.play(FadeIn(title), run_time=0.52)
        self.play(FadeIn(lesson), run_time=0.30)
        self.wait(self.narration_s - self.elapsed())


class S03CommonGarden(SpokenScene):
    def construct(self):
        home = meadow()
        plot = bed(*GARDEN, 4.7)
        self.add(mountain(), home, field_tag())
        self.at("to separate them")
        sources = (pt(-4.35, -0.05), pt(4.25, 1.87))
        seeds = [seed(*source[:2], c) for source, c in zip(sources, (ORANGE, BLUE))]
        self.play(FadeIn(plot), run_time=0.6)
        self.add(*seeds)
        self.play(*(MoveAlongPath(s, ArcBetweenPoints(src, pt(x, -1.56), angle=a))
                    for s, src, x, a in zip(seeds, sources, (-0.95, 0.95), (-1.02, 0.9))),
                  FadeOut(home), run_time=2.35)
        climate = weather()
        garden_label = heading("Common garden", color=GREEN)
        self.at("common garden")
        self.play(FadeIn(garden_label), FadeIn(climate), run_time=0.63)
        self.at("difference that persists")
        plants = shared_plants()
        for p, s in zip(plants, seeds):
            p.save_state()
            p.scale(0.12, about_point=s.get_center())
        self.add(plants)
        self.play(*(Restore(p) for p in plants), *(FadeOut(s) for s in seeds), run_time=1.35)
        result = caption("Inherited basis", color=ORANGE)
        self.at("inherited basis")
        self.play(FadeIn(result), run_time=0.55)
        self.at("if they grow alike")
        alike = shared_plants("alike")
        self.play(FadeOut(result), Transform(plants, alike), run_time=1.38)
        result = caption("Surroundings", color=BLUE)
        self.at("from surroundings")
        self.play(FadeIn(result), run_time=0.53)
        self.at("inherited variation within")
        self.play(FadeOut(result), FadeOut(climate), Transform(plants, shared_plants("within")), run_time=1.48)
        tag = caption("Within ≠ between populations", color=GOLD)
        self.at("does not show")
        self.play(FadeIn(tag), run_time=0.57)
        self.at("differ genetically", lead=-0.56)
        self.play(Transform(plants, shared_plants("different", True)), run_time=0.82)
        self.play(FadeOut(garden_label), FadeOut(tag), run_time=0.34)
        self.finish()


def home_plots():
    return VGroup(bed(*SITES[0], 3.2), bed(*SITES[1], 3.2))


def home_pairs(animate=False):
    return VGroup(*[sprig(x + offset, y, c, h, broad, animate, i + offset)
                    for i, (x, y) in enumerate(SITES)
                    for offset, c, h, broad in
                    [(-0.65, ORANGE, 1.18, True), (0.65, BLUE, 1.48, False)]])


class S04Reciprocal(SpokenScene):
    def construct(self):
        plot = bed(*GARDEN, 4.7)
        plants = shared_plants()
        sites = home_plots()
        self.add(mountain(), plot, plants, field_tag())
        self.at("next move organisms")
        self.play(ReplacementTransform(plot, sites),
                  plants[0].animate.shift(pt(-4.05, -0.11)).scale(0.7, about_edge=DOWN),
                  plants[1].animate.shift(pt(3.95, 1.45)).scale(0.62, about_edge=DOWN),
                  run_time=1.05)
        pairs = home_pairs()
        arrows = VGroup(curved((-3.58, 0.06), (3.48, 1.43), -0.58),
                        curved((3.50, 0.98), (-3.55, -1.25), -0.49))
        self.at("both ways between")
        self.play(*(Create(a) for a in arrows), run_time=0.65)
        orange = seed(-3.58, 0.06, ORANGE)
        blue = seed(3.50, 0.98, BLUE)
        self.add(orange, blue)
        self.play(MoveAlongPath(orange, arrows[0]), MoveAlongPath(blue, arrows[1]), run_time=1.67)
        method = heading("Reciprocal transplant", color=YELLOW)
        self.at("reciprocal transplant")
        self.play(FadeOut(orange), FadeOut(blue), FadeOut(arrows), FadeIn(method),
                  ReplacementTransform(plants, pairs), run_time=0.82)
        controls = VGroup(T("Home controls", 30, GREEN).move_to(pt(-4.35, -2.61)),
                          T("Home controls", 30, GREEN).move_to(pt(4.25, -1.03)))
        self.at("keeping controls at home")
        self.play(FadeIn(controls), run_time=0.52)
        self.at("then you measure")
        gauges = [ValueTracker(0.02), ValueTracker(0.02)]
        dials = VGroup(*(dial(f, pt(x, y), radius=0.94, size=32, fmt="", color=c)
                         for f, x, y, c in zip(gauges, (-1.5, 1.45), (-0.55, 0.66), (ORANGE, BLUE))))
        performance = T("Performance", 30, TEXT).move_to(pt(0, -1.54))
        self.play(FadeOut(controls), FadeIn(dials), FadeIn(performance), run_time=0.65)
        self.play(gauges[0].animate.set_value(0.73), gauges[1].animate.set_value(0.62),
                  run_time=2.47)
        self.at("the core idea")
        rule = caption("Match or swap environments", color=GOLD, size=34)
        self.play(FadeOut(method), FadeIn(rule), run_time=0.60)
        self.play(FadeOut(dials), FadeOut(performance), run_time=1.1)
        self.finish()


def tree(x, y, mirrored=False):
    side = -1 if mirrored else 1
    trunk = solid([(x - 0.34, -3.62), (x - 0.14, y + 1.42), (x + 0.10, y + 1.39),
                   (x + 0.37, -3.62)], BARK)
    branch = solid([(x, y - 0.45), (x + 1.73 * side, y - 0.67),
                    (x + 2.22 * side, y - 1.54), (x + 1.61 * side, y - 1.07),
                    (x - 0.1 * side, y - 0.83)], BARK)
    crown = VGroup(*[oval(x + dx, y + dy, w, h, LEAF, a)
                     for dx, dy, w, h, a in [(-0.87, 1.03, 1.64, 0.86, 0.23),
                                             (0, 1.34, 1.64, 0.90, 0.12),
                                             (0.89, 1.22, 1.64, 0.90, -0.31)]])
    for i, frond in enumerate(crown):
        frond.set_fill("#415F54", 1)
        bob(frond, amp=0.12, seed=i)
    return VGroup(trunk, branch, crown)


def nest(x, y, scale=1):
    bowl = solid([(-1.18, 0), (-0.96, -0.26), (-0.72, -0.47), (0, -0.56),
                  (0.72, -0.47), (0.96, -0.26), (1.18, 0)], BARK)
    straw = VGroup(*[path([(-1.1 + d, -0.09 - d), (0, -0.31 - d), (1.04 - d, -0.09 - d)],
                           "#BF986D", 3) for d in (0, 0.12, 0.21)])
    rim = oval(0, 0, 2.38, 0.30, "#A57C58")
    return VGroup(bowl, straw, rim).scale(scale).shift(pt(x, y))


def bird(x, y, color, deep=True, face=1, scale=1):
    body = oval(-0.22, -0.14, 1.11, 0.67, color, 0.24)
    head = disk(0.22, 0.17, 0.31, color)
    tail = solid([(-0.53, -0.03), (-1.04, -0.40), (-0.49, -0.27)], color)
    wing = oval(-0.28, -0.14, 0.52, 0.25, RIDGE, 0.31)
    bill = solid([(0.47, 0.32 if deep else 0.245), (0.88, 0.12),
                  (0.47, -0.09 if deep else 0.015)], YELLOW)
    eye = disk(0.29, 0.24, 0.052, BG)
    parts = (tail, body, wing, head, eye) if deep is None else (tail, body, wing, head, bill, eye)
    shape = VGroup(*parts)
    if face < 0:
        shape.flip(UP, about_point=ORIGIN)
    return shape.scale(scale, about_point=ORIGIN).shift(pt(x, y))


def egg(x, y, color, scale=1):
    fill = oval(x, y, 0.34 * scale, 0.46 * scale, color, 0.24)
    glint = oval(x - 0.055 * scale, y + 0.08 * scale, 0.075 * scale, 0.16 * scale, TEXT, -0.25)
    return VGroup(fill, glint)


def grove():
    return VGroup(mountain(), *(tree(x, y, i == 1) for i, (x, y) in enumerate(BIRD_SITES)),
                  *(nest(x, y) for x, y in BIRD_SITES))


def prediction_axes():
    return (
        Plot((-5.8, -0.75, -1.82, 1.74), (0, 1), (-1, 1), xlabel="Genetic parents",
             label_size=32, color=TEXT),
        Plot((0.58, 5.64, -1.82, 1.74), (0, 1), (-1, 1), xlabel="Foster parents",
             label_size=32, color=TEXT),
    )


def plot_land():
    return VGroup(solid([(-6.7, -3.59), (-6.7, 2.22), (6.7, 2.22), (6.7, -3.59)], "#2A333E"),
                  solid([(-6.7, -3.59), (-6.7, -2.64), (-3.2, -2.43), (0, -2.62),
                         (4.1, -2.38), (6.7, -2.59), (6.7, -3.59)], "#354946")).set_z_index(-4)


def graph_backings():
    return VGroup(*(Rectangle(width=5.35, height=3.84, fill_color="#354757", fill_opacity=1,
                              stroke_width=0).move_to(pt(x, -0.04))
                    for x in (-3.27, 3.11))).set_z_index(-3)



def predict_picture():
    axes = prediction_axes()
    marks = VGroup(*(heading("?", 0.14, x, GOLD, 71) for x in (-3.28, 3.10)))
    prompt = question_card(PROMPT, y=-3.06, size=36)
    return axes, marks, prompt


class S05CrossFosterPredict(SpokenScene):
    def construct(self):
        land = mountain()
        plots = home_plots()
        plants = home_pairs()
        self.add(land, plots, plants, field_tag())
        self.at("with animals")
        wooded = grove()
        self.play(FadeOut(plots, shift=DOWN * 0.6), FadeOut(plants, shift=DOWN * 0.9),
                  FadeIn(VGroup(*wooded[1:]), shift=UP * 0.85), run_time=1.20)
        parents = VGroup(*(bird(x + dx, y + 0.57, color, i == 0, face, 0.78)
                           for i, ((x, y), color) in enumerate(zip(BIRD_SITES, (ORANGE, BLUE)))
                           for dx, face in ((-0.79, 1), (0.78, -1))))
        self.play(LaggedStart(*(FadeIn(p, shift=0.25 * DOWN) for p in parents), lag_ratio=0.22),
                  run_time=1.45)
        self.at("method called cross")
        label = heading("Cross-fostering", color=YELLOW)
        self.play(FadeIn(label), run_time=0.52)
        self.at("soon after laying")
        eggs = [egg(x, y + 0.19, c) for (x, y), c in zip(BIRD_SITES, (ORANGE, BLUE))]
        self.play(*(GrowFromCenter(e) for e in eggs), run_time=0.70)
        self.at("swap eggs between")
        left, right = [e.get_center() for e in eggs]
        arcs = [ArcBetweenPoints(left, right, angle=-1.22), ArcBetweenPoints(right, left, angle=0.56)]
        guides = VGroup(*(a.copy().set_stroke(YELLOW, 4) for a in arcs))
        self.play(*(Create(g) for g in guides), run_time=0.68)
        self.play(*(MoveAlongPath(e, a) for e, a in zip(eggs, arcs)), run_time=2.20)
        self.at("leaving other clutches")
        control = VGroup(nest(0, -2.03, 0.83), egg(-0.18, -1.88, ORANGE, 0.75),
                         egg(0.18, -1.88, ORANGE, 0.75), T("Home clutch", 30, GREEN).move_to(pt(0, -2.84)))
        self.play(FadeOut(guides), FadeIn(control), run_time=0.65)
        self.at("measure chicks as adults")
        adults = [bird(x, y + 0.64, c, deep=None, scale=0.68)
                  for (x, y), c in zip(reversed(BIRD_SITES), (ORANGE, BLUE))]
        self.play(*(ReplacementTransform(e, b) for e, b in zip(eggs, adults)),
                  FadeOut(parents), run_time=1.39)
        self.at("predict if genes alone")
        self.play(*(FadeOut(o) for o in (*wooded[1:], *adults, control, label)), run_time=0.40)
        self.play(FadeOut(land), FadeIn(plot_land()), run_time=0.38)
        axes, marks, prompt = predict_picture()
        backs = graph_backings()
        self.play(GrowFromEdge(backs[0], LEFT), Create(axes[0].axes), run_time=1.05)
        self.play(GrowFromEdge(backs[1], LEFT), Create(axes[1].axes), run_time=1.05)
        self.play(*(FadeIn(a.xlabel) for a in axes), FadeIn(prompt), run_time=0.65)
        self.play(*(GrowFromCenter(mark) for mark in marks), run_time=0.74)
        for i, mark in enumerate(marks):
            bob(mark, amp=0.38, speed=2.8, seed=i)
        self.finish()


class S06PredictPause(NarratedScene):
    def construct(self):
        axes, marks, prompt = predict_picture()
        self.add(plot_land(), graph_backings(), *axes, marks, prompt, field_tag())
        # Two even dotted frames leave both plots unanswered while the question stays still.
        locations = [(x, y) for x in (0.18, 0.39, 0.61, 0.82) for y in (-0.54, 0.54)]
        dots = VGroup(*(disk(*a.pt(x, y)[:2], 0.20, "#8197A3").set_opacity(0.72)
                        for a in axes for x, y in locations))
        self.play(FadeIn(dots), run_time=0.8)
        self.play(dots.animate.set_opacity(0.37), run_time=0.8)
        self.play(dots.animate.set_opacity(0.72), run_time=0.8)
        self.play(FadeOut(dots), run_time=0.8)
        self.wait(1.30)


def relationship(plot, slope, color):
    # Dimensionless predictions only. Every displayed line evaluates this schematic model.
    return plot.curve(lambda x: slope * (x - 0.5), x0=0.05, x1=0.96,
                      color=color, width=8, n=40)


def uncertainty(plot, slope, color):
    xs = np.linspace(0.05, 0.96, 30)
    width = lambda x: 0.13 + 0.19 * abs(x - 0.5)
    hi = [plot.pt(x, slope * (x - 0.5) + width(x)) for x in xs]
    lo = [plot.pt(x, slope * (x - 0.5) - width(x)) for x in reversed(xs)]
    return Polygon(*hi, *lo, fill_color=color, fill_opacity=0.27, stroke_width=0)


class S07PredictReveal(SpokenScene):
    def construct(self):
        axes, marks, prompt = predict_picture()
        backs = graph_backings()
        self.add(plot_land(), backs, *axes, marks, prompt, field_tag())
        self.at("if genes alone matter")
        self.play(FadeOut(marks), FadeOut(prompt), run_time=0.38)
        case = heading("Genes only", color=GOLD)
        self.play(FadeIn(case), FadeIn(T("Adult offspring beak depth", 30).move_to(pt(0, 2.48))),
                  run_time=0.55)
        colors = (GOLD, GREEN)
        genetic_highlight, foster_highlight = "#524938", "#3B5140"
        lines = [relationship(a, s, c) for a, s, c in zip(axes, (1.73, 0), colors)]
        self.at("genetic parent slope")
        self.play(Create(lines[0]), backs[0].animate.set_fill(genetic_highlight), run_time=1.42)
        self.at("foster parent slope")
        self.play(Create(lines[1]), backs[1].animate.set_fill(foster_highlight),
                  backs[0].animate.set_fill("#354757"), run_time=1.68)
        self.at("if rearing alone matters")
        new = heading("Rearing only", color=GOLD)
        self.play(FadeOut(case), run_time=0.38)
        self.at("those slopes reverse", lead=0.55)
        reversed_lines = [relationship(a, s, c) for a, s, c in zip(axes, (0, 1.73), colors)]
        self.play(FadeIn(new), *(Transform(line, target) for line, target in zip(lines, reversed_lines)),
                  run_time=0.90)
        self.at("if both contribute")
        case = heading("Both contribute", color=GOLD)
        self.play(FadeOut(new), *(FadeOut(line) for line in lines),
                  backs[1].animate.set_fill("#354757"), run_time=0.44)
        self.play(FadeIn(case), run_time=0.38)
        self.at("both slopes are positive")
        slopes = (1.27, 0.86)
        lines = [relationship(a, s, c) for a, s, c in zip(axes, slopes, colors)]
        self.play(*(Create(line) for line in lines), backs[0].animate.set_fill(genetic_highlight),
                  backs[1].animate.set_fill(foster_highlight), run_time=1.64)
        self.at("with uncertainty")
        bands = [uncertainty(a, s, c) for a, s, c in zip(axes, slopes, colors)]
        self.play(*(GrowFromCenter(b) for b in bands), run_time=1.45)
        self.play(*(b.animate.set_fill(opacity=0.43) for b in bands), run_time=1.10)
        self.finish()


def mouse(x, y, color=GREY, scale=1):
    body = oval(-0.24, -0.10, 1.36, 0.86, color, 0.15)
    face = oval(0.48, 0.04, 0.90, 0.54, color, -0.29)
    ear = disk(0.34, 0.34, 0.20, color)
    tail = path([(-0.79, -0.1), (-1.12, -0.22), (-1.39, -0.10), (-1.48, 0.14)], color, 5)
    eye = disk(0.63, 0.10, 0.049, BG)
    return VGroup(tail, body, face, ear, eye).scale(scale, about_point=ORIGIN).shift(pt(x, y))


class S08ControlsEarly(SpokenScene):
    def construct(self):
        woods = grove()
        large_egg = egg(-3.65, 0.70, ORANGE, 4.2)
        small_egg = egg(3.65, -0.16, BLUE, 1.18)
        self.add(woods, small_egg, field_tag())
        self.at("swaps still have limits")
        self.play(GrowFromCenter(large_egg), run_time=1.55)
        rim = Ellipse(width=1.57, height=2.08, color=YELLOW, stroke_width=6)
        rim.rotate(0.24).move_to(large_egg)
        self.at("bird eggs are swapped")
        self.play(Create(rim), run_time=1.55)
        pulse(rim, base=7, amp=4, speed=2)
        egg_note = heading("Egg effect remains", color=GOLD)
        self.at("effects of the mother")
        self.play(FadeIn(egg_note), run_time=0.62)
        self.at("foster nests still differ")
        food = VGroup(*(seed(x, y, c).scale(1.25)
                        for x, y, c in [(-4.25, 0.84, ORANGE), (-3.90, 0.39, ORANGE),
                                        (-3.02, 0.79, ORANGE), (3.12, 0.66, GREEN),
                                        (3.79, 0.77, GREEN), (4.17, 0.42, GREEN)]))
        territory = heading("Territory & food differ", color=GOLD)
        self.play(FadeOut(rim), FadeOut(large_egg), FadeOut(egg_note), run_time=0.54)
        self.play(LaggedStart(*(FadeIn(item, shift=DOWN * 0.28) for item in food), lag_ratio=0.24),
                  FadeIn(territory), run_time=1.01)
        for i, item in enumerate(food):
            bob(item, amp=0.28, seed=i)
        self.at("in mice cross")
        panel = RoundedRectangle(width=6.4, height=4.27, corner_radius=0.24, color=WATER,
                                 stroke_width=3, fill_color="#273946", fill_opacity=1).move_to(pt(2.94, -0.11))
        pup = mouse(1.35, 0.50, ORANGE, 0.50)
        dam = mouse(4.18, 0.32, BLUE, 1.18)
        self.play(FadeOut(territory), FadeOut(food), FadeOut(woods[2]), FadeOut(woods[4]),
                  FadeOut(small_egg), FadeIn(panel), run_time=0.52)
        self.play(FadeIn(dam), GrowFromCenter(pup), run_time=0.52)
        self.play(MoveAlongPath(pup, ArcBetweenPoints(pup.get_center(), pt(3.40, -0.40), angle=-0.85)),
                  run_time=0.83)
        nursing = T("Controls nursing", 32, TEXT).move_to(pt(2.94, -1.54))
        self.at("controls nursing")
        self.play(FadeIn(nursing), run_time=0.47)
        bob(pup, amp=0.14, speed=2.1)
        self.at("controlling the uterus")
        embryo = disk(1.30, 0.74, 0.19, ORANGE)
        womb = oval(3.96, 0.22, 0.79, 0.50, RIDGE)
        self.play(FadeOut(nursing), FadeOut(pup), FadeIn(womb), GrowFromCenter(embryo), run_time=0.62)
        self.at("transferring embryos")
        self.play(MoveAlongPath(embryo, ArcBetweenPoints(embryo.get_center(), womb.get_center(), angle=-0.8)),
                  run_time=0.94)
        self.play(FadeIn(T("Controls uterus", 32, TEXT).move_to(pt(2.94, -1.54))), run_time=0.48)
        self.finish()


def wind_symbol(x, y):
    return VGroup(*(path([(x - 0.37, y + i * 0.14), (x - 0.04, y + i * 0.14),
                          (x + 0.25, y + i * 0.14), (x + 0.35, y + 0.13 + i * 0.14)],
                         TEXT, 4) for i in (-1, 0, 1)))


def factors():
    thermometer = VGroup(Line(pt(-0.49, -0.19), pt(-0.49, 0.34), color=ORANGE, stroke_width=10),
                         disk(-0.49, -0.19, 0.14, ORANGE))
    rain = VGroup(oval(0.03, 0.15, 0.26, 0.36, BLUE, -0.34),
                  oval(0.24, -0.14, 0.15, 0.28, BLUE, -0.34))
    return VGroup(thermometer, rain, wind_symbol(0.78, 0.02))


class S09ControlsField(SpokenScene):
    def construct(self):
        plots = home_plots()
        self.add(mountain(), plots, field_tag())
        self.at("guard against bias")
        tray = bed(0, -0.85, 3.77)
        starts = [(x, -0.67) for x in np.linspace(-1.35, 1.35, 6)]
        samples = [seed(x, y, GREEN) for x, y in starts]
        self.play(GrowFromCenter(tray), run_time=0.83)
        self.at("start groups under matching")
        self.play(LaggedStart(*(GrowFromCenter(p) for p in samples), lag_ratio=0.22), run_time=0.95)
        self.at("assign them at random")
        matching = heading("Equal start, random split", color=GREEN)
        destinations = [(x + d, y + 0.04) for x, y in SITES for d in (-0.60, 0, 0.60)]
        order = (1, 4, 5, 2, 0, 3)
        self.play(FadeOut(tray), FadeIn(matching),
                  *(MoveAlongPath(s, ArcBetweenPoints(s.get_center(), pt(*destinations[j]), angle=0.62))
                    for s, j in zip(samples, order)), run_time=1.72)
        self.at("a finch swap")
        clutch = VGroup(nest(-0.20, -0.41, 1.08), egg(-0.37, -0.22, ORANGE),
                        bird(-0.99, 0.12, ORANGE, scale=0.75))
        island = heading("One island, one year", color=GOLD)
        self.play(FadeOut(matching), *(FadeOut(s) for s in samples), run_time=0.35)
        self.play(FadeIn(clutch), FadeIn(island), run_time=0.64)
        season = VGroup(seed(-2.2, 1.17, ORANGE), seed(-1.76, 1.38, ORANGE),
                        seed(-1.35, 1.24, ORANGE)).scale(1.65)
        self.play(FadeIn(season), run_time=0.65)
        self.play(season.animate.shift(RIGHT * 1.08 + UP * 0.22), run_time=1.50)
        self.at("different seeds")
        self.play(Transform(season, VGroup(seed(0.89, 1.31, GREEN).scale(1.12),
                                           seed(1.45, 1.47, GREEN).scale(2.25),
                                           seed(2.10, 1.28, GREEN).scale(1.55))), run_time=1.98)
        self.at("elevation changes many")
        climate = factors().move_to(pt(-4.46, -0.67))
        label = heading("Elevation mixes factors", color=GOLD)
        self.play(FadeOut(clutch), FadeOut(season), FadeOut(island), run_time=0.42)
        self.play(FadeIn(climate), FadeIn(label), run_time=0.52)
        self.play(MoveAlongPath(climate, ArcBetweenPoints(climate.get_center(), pt(4.36, 1.14), angle=-0.26)),
                  run_time=2.46)
        self.at("temperature cannot be separated")
        self.play(climate.animate.scale(1.42).shift(LEFT * 0.52 + UP * 0.35), run_time=1.25)
        for i, icon in enumerate(climate):
            bob(icon, amp=0.26, speed=2.8, seed=i)
        self.finish()


def range_flowers():
    return VGroup(sprig(-5.39, SITES[0][1], RED, 2.29, True, True),
                  sprig(4.80, SITES[1][1], PURPLE, 2.18, False, True, 1.1))


def fitness_columns(xs, y, color):
    # These represent qualitative fitness only. Column heights are diagram coordinates.
    bases = VGroup(*(Line(pt(x - 0.36, y), pt(x + 0.36, y), color=TEXT, stroke_width=3) for x in xs))
    columns = VGroup(*(Rectangle(width=0.56, height=h, stroke_width=0, fill_opacity=1,
                                  fill_color=color).move_to(pt(x, y + h / 2))
                       for x, h in zip(xs, (1.45, 0.08))))
    return bases, columns


class S10UnlockedMonkeyflower(SpokenScene):
    def construct(self):
        slope = mountain()
        self.add(slope, home_plots(), field_tag())
        self.at("even with those limits")
        habitat = VGroup(curved((-3.55, -0.8), (-1.58, -0.89), 0.55, RED),
                         curved((3.55, 0.77), (1.52, -0.09), -0.55, PURPLE))
        ranges = VGroup(oval(-3.95, -1.9, 4.15, 0.78, "#75504C", 0.03),
                        oval(4.18, -0.21, 4.16, 0.80, "#635575", 0.11)).set_z_index(-1)
        slope.set_z_index(-2)
        self.play(GrowFromEdge(ranges[0], LEFT), Create(habitat[0]), run_time=1.65)
        self.play(GrowFromEdge(ranges[1], RIGHT), Create(habitat[1]), run_time=1.65)
        self.at("a niche is where")
        self.play(FadeOut(habitat), FadeOut(ranges), run_time=0.55)
        next_n = VGroup(M("N", 44), M("next", 28)).arrange(RIGHT, buff=0.07, aligned_edge=DOWN)
        next_n[1].shift(DOWN * 0.14)
        formula = VGroup(next_n, M("= λ · N + I", 44)).arrange(RIGHT, buff=0.24)
        formula[1].align_to(next_n[0], UP)
        formula.move_to(pt(0, 2.35))
        self.play(Write(formula), run_time=1.03)
        self.at("yearly births and deaths")
        growth = T("λ   Yearly growth factor", 30, GREEN).move_to(pt(0, 1.40))
        self.play(FadeIn(growth), run_time=0.63)
        niche = heading("Niche: long-run λ ≥ 1  (I = 0)", y=0.47, color=GOLD, size=41)
        self.at("stays at least one")
        self.play(FadeIn(niche), run_time=1.15)
        self.at("amy angert")
        credit = heading("Angert & Schemske", y=3.17, size=32)
        self.play(FadeOut(formula), FadeOut(growth), FadeOut(niche), run_time=0.56)
        flowers = range_flowers()
        self.play(FadeIn(credit), run_time=0.57)
        self.at("grew two california")
        self.play(GrowFromEdge(flowers[0], DOWN), run_time=1.10)
        self.at("low elevation mimulus")
        cardinalis = T("Mimulus cardinalis", 30, RED, slant=ITALIC).move_to(pt(-4.46, 1.17))
        self.play(FadeIn(cardinalis), run_time=0.57)
        self.at("high elevation mimulus", lead=0.65)
        self.play(GrowFromEdge(flowers[1], DOWN), run_time=0.69)
        lewisii = T("Mimulus lewisii", 30, PURPLE, slant=ITALIC).move_to(pt(3.92, 2.47))
        self.play(FadeIn(lewisii), run_time=0.57)
        self.at("gardens inside and beyond")
        # Both species have an inside-range garden and a garden beyond its respective limit.
        low_bases, low_bars = fitness_columns((-3.85, 2.84), -1.69, RED)
        high_bases, high_bars = fitness_columns((3.64, -2.82), -0.16, PURPLE)
        garden_rise = high_bases[0].get_y() - low_bases[0].get_y()
        VGroup(low_bases[1], low_bars[1]).shift(UP * garden_rise)
        VGroup(high_bases[1], high_bars[1]).shift(DOWN * garden_rise)
        fitness = heading("Fitness", y=1.53, size=32, color=TEXT)
        self.play(FadeIn(fitness), FadeIn(low_bases), FadeIn(high_bases), run_time=0.62)
        self.play(GrowFromEdge(low_bars[0], DOWN), GrowFromEdge(high_bars[0], DOWN), run_time=1.44)
        self.at("zero or near zero")
        self.play(FadeIn(low_bars[1]), FadeIn(high_bars[1]), run_time=0.57)
        near = caption("Zero or near zero beyond the range", color=GOLD, size=30)
        self.play(FadeIn(near), run_time=0.53)
        self.finish()


META_COLOR = (GREEN, BLUE, ORANGE)
META_SHARES = (46, 26, 23)
META_LABELS = ("Niche limit", "Dispersal limitation", "Elevation sinks")
META_DETAIL = ("Range edge at niche limit", "λ ≥ 1, N = 0", "λ < 1, I > 0")


def meta_background():
    return VGroup(plot_land(), solid([(-6.65, -2.70), (-4.42, -2.50), (-3.10, -2.63),
                                      (-0.62, -2.37), (1.57, -2.55), (4.41, -2.43),
                                      (6.65, -2.70), (6.65, -3.60), (-6.65, -3.60)], EARTH))


def meta_credit():
    return heading("Hargreaves, Samis & Eckert, 2014", size=37)


def meta_scale():
    return Plot((-0.63, 5.72, -2.30, 2.08), (0, 100), (0, 3),
                xticks=((0, "0%"), (25, "25%"), (50, "50%"), (75, "75%"), (100, "100%")),
                size=28, color=TEXT)


def meta_row(scale, index):
    color, percent = META_COLOR[index], META_SHARES[index]
    y = 2.57 - 1.03 * index
    start, stop = scale.pt(0, y), scale.pt(percent, y)
    base = Rectangle(width=scale.pt(100, y)[0] - start[0], height=0.49,
                     fill_color="#405260", fill_opacity=1, stroke_width=0)
    fill = Rectangle(width=stop[0] - start[0], height=0.49, fill_color=color,
                     fill_opacity=1, stroke_width=0)
    base.move_to(start, aligned_edge=LEFT)
    fill.move_to(start, aligned_edge=LEFT)
    amount = M(f"{percent}%", 30, color).next_to(fill, UP, buff=0.12).align_to(fill, RIGHT)
    title = T(META_LABELS[index], 32, color, weight=BOLD).move_to(pt(-3.76, start[1] + 0.13))
    detail = T(META_DETAIL[index], 28, TEXT).move_to(pt(-3.76, start[1] - 0.36))
    return base, fill, amount, title, detail


def grid_tests():
    variants = ("#6AA2AC", "#658B9A", "#5F9A9D", "#739EAC")
    cells = VGroup()
    for i in range(111):
        row, col = divmod(i, 16)
        x, y = -5.56 + col * 0.73, 1.88 - row * 0.59
        fill = RoundedRectangle(width=0.59, height=0.43, corner_radius=0.09,
                                stroke_width=0, fill_opacity=0.91,
                                fill_color=variants[(i * 7 + row) % len(variants)]).move_to(pt(x, y))
        ridge = solid([(x - 0.25, y - 0.14), (x - 0.09, y + 0.03),
                       (x + 0.04, y - 0.02), (x + 0.14, y + 0.10), (x + 0.26, y - 0.14)], RIDGE)
        cells.add(VGroup(fill, ridge))
    return cells


class S11UnlockedMetaA(SpokenScene):
    def construct(self):
        slope = mountain()
        flowers = range_flowers()
        plots = home_plots()
        self.add(slope, plots, flowers)
        self.at("that fits niche limits")
        ground = meta_background()
        self.play(FadeOut(slope, scale=0.32), FadeOut(plots, scale=0.32), FadeOut(flowers, scale=0.32),
                  FadeIn(ground), run_time=1.85)
        self.at("in 2014")
        credit = meta_credit()
        self.play(FadeIn(credit), run_time=0.68)
        grid = grid_tests()
        tiles = [VGroup(*grid[i:i + 16]) for i in range(0, 111, 16)]
        self.play(LaggedStart(*(FadeIn(row, shift=DOWN * 0.18) for row in tiles), lag_ratio=0.37),
                  run_time=3.90)
        self.at("pooled 111 beyond")
        count = caption("111 beyond-range transplant tests", size=32)
        self.play(FadeIn(count), run_time=0.64)
        self.at("in three quarters")
        reduced = sorted(range(111), key=lambda i: (i * 59) % 111)[:round(111 * 0.75)]
        groups = [VGroup(*(grid[i] for i in reduced[j:j + 14])) for j in range(0, len(reduced), 14)]
        self.play(LaggedStart(*(g.animate.shift(DOWN * 0.10).set_opacity(0.28) for g in groups), lag_ratio=0.32),
                  swap(count, caption("75% performed worse beyond the range", size=32), run_time=0.85),
                  run_time=2.68)
        self.at("in 46%", lead=1.55)
        self.play(*(FadeOut(g) for g in self.mobjects if g is not credit and g is not ground), run_time=0.42)
        scale = meta_scale()
        base, fill, number, title, detail = meta_row(scale, 0)
        self.play(FadeIn(scale), FadeIn(base), FadeIn(title), FadeIn(detail), run_time=0.46)
        self.play(GrowFromEdge(fill, LEFT), FadeIn(number), run_time=0.70)
        self.finish()


def meta_focus(row, color):
    return RoundedRectangle(width=12.4, height=1.25, corner_radius=0.17, stroke_width=0,
                            fill_color=color, fill_opacity=1).move_to(
                                pt(-0.23, row.get_y() + 0.04)).set_z_index(-1)



class S12UnlockedMetaB(SpokenScene):
    def construct(self):
        scale = meta_scale()
        self.add(meta_background().set_z_index(-4), meta_credit(), scale, *meta_row(scale, 0))
        base, fill, number, title, detail = meta_row(scale, 1)
        focus = meta_focus(base, "#324E5F")
        self.add(base, focus)
        self.at("26 percent")
        self.play(GrowFromEdge(fill, LEFT), FadeIn(number), run_time=0.78)
        self.at("sustained themselves beyond")
        self.play(FadeIn(detail), focus.animate.set_fill("#48768B"), run_time=1.10)
        self.at("dispersal limitation")
        self.play(FadeIn(title), focus.animate.set_fill("#3B5F71"), run_time=0.88)
        self.at("suitable places never reached")
        suitable = caption("Suitable places never reached", size=31, color=BLUE)
        self.play(FadeIn(suitable, shift=UP * 0.23), focus.animate.set_fill("#324E5F"), run_time=1.30)
        self.at("23 percent", lead=1.45)
        base, fill, number, title, detail = meta_row(scale, 2)
        new_focus = meta_focus(base, "#59473C")
        self.play(FadeOut(suitable), FadeOut(focus), FadeIn(base), FadeIn(new_focus), run_time=0.50)
        self.play(GrowFromEdge(fill, LEFT), FadeIn(number), run_time=0.80)
        self.at("limits were sinks", lead=0.43)
        self.play(FadeIn(title), run_time=0.55)
        self.at("immigrants sustain them")
        self.play(FadeIn(detail), new_focus.animate.set_fill("#705541"), run_time=0.65)
        migrant = disk(5.14, fill.get_y() + 0.01, 0.11, YELLOW)
        self.play(FadeIn(migrant), run_time=0.34)
        self.play(MoveAlongPath(migrant, ArcBetweenPoints(migrant.get_center(),
                                pt(fill.get_right()[0] + 0.17, fill.get_y()), angle=-0.28)), run_time=1.9)
        self.play(FadeOut(migrant), run_time=0.26)
        self.at("the shares do not add")
        note = caption("Shares do not add to 100%", color=GOLD, size=32)
        self.play(FadeIn(note, shift=0.23 * UP), FadeOut(new_focus), run_time=1.15)
        self.at("control or swap environments")
        old = list(self.mobjects)
        self.play(*(FadeOut(m) for m in old), FadeIn(mountain()), run_time=0.55)
        plots = home_plots()
        arc = curved((-3.96, -0.13), (3.94, 0.97), -0.63)
        self.play(FadeIn(plots), Create(arc), run_time=0.65)
        self.play(GrowFromEdge(meadow(), DOWN), run_time=0.85)
        self.play(FadeOut(arc), run_time=0.38)
        self.finish()


class S13End(EndCard):
    LINE = "Share one garden or swap homes to separate genes from surroundings."
