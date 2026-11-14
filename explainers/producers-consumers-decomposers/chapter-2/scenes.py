"""Weighing the Drain — chapter 2 of Producers, consumers and decomposers.

COLOR MAP (kept from chapter 1)
  GREEN  = producers
  BLUE   = consumers; brighter BLUE also marks the higher-site data
  PURPLE = decomposers and detritivores
  TAN    = dead leaves
  ORANGE = nutrients
  YELLOW = energy
  GOLD   = measured matter / measurement emphasis
  GREY   = soil, water, air, and apparatus outlines

Every recurring world is rebuilt by the builders below at the same coordinates.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
TAN = "#B8946A"
DATA = "#5DADE2"
PALE = "#8FA9B8"

MONTHS = np.array([0.0, 1.0, 8.0, 12.0, 20.0, 24.0])
MASS = np.array([100.0, 72.0, 68.9, 59.7, 55.8, 47.8])


def arrow(a, b, color=GREY, width=5, tip=0.2, buff=0.06):
    return Arrow(a, b, color=color, stroke_width=width, tip_length=tip, buff=buff,
                 max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=10)


def leaf_shape(center=ORIGIN, width=2.5, color=TAN):
    """One large, readable dead-leaf silhouette; no biological detail is implied."""
    body = Ellipse(width=width, height=0.46 * width, color=color, stroke_width=4,
                   fill_color=color, fill_opacity=0.55).rotate(0.12).move_to(center)
    stem = Line(body.get_left() + LEFT * 0.12, body.get_left() + LEFT * 0.48,
                color=color, stroke_width=5)
    vein = Line(body.get_left() + RIGHT * 0.2, body.get_right() + LEFT * 0.2,
                color=color, stroke_width=2).rotate(0.12, about_point=body.get_center())
    return VGroup(body, stem, vein)


def small_leaves(n=6, center=ORIGIN, spread=(1.7, 0.65), seed=4):
    rng = np.random.default_rng(seed)
    g = VGroup()
    for _ in range(n):
        p = np.array(center, float) + [rng.uniform(-spread[0], spread[0]),
                                      rng.uniform(-spread[1], spread[1]), 0]
        g.add(Ellipse(width=0.52, height=0.23, color=TAN, stroke_width=2,
                      fill_color=TAN, fill_opacity=0.72).rotate(rng.uniform(-0.5, 0.5)).move_to(p))
    return g


def mesh_bag(center=ORIGIN, scale=1.0, leaf_count=6, highlight=False):
    """The measured mesh bag, shared by the method and limitation scenes."""
    c = np.array(center, float)
    outline = RoundedRectangle(corner_radius=0.18, width=3.4, height=2.25,
                               stroke_color=DATA if highlight else PALE, stroke_width=4,
                               fill_color=GREY, fill_opacity=0.07).move_to(c)
    mesh = VGroup()
    for x in np.linspace(-1.35, 1.35, 7):
        mesh.add(Line(c + [x, -0.88, 0], c + [x, 0.88, 0], color=PALE, stroke_width=1.2).set_opacity(0.5))
    for y in np.linspace(-0.72, 0.72, 5):
        mesh.add(Line(c + [-1.48, y, 0], c + [1.48, y, 0], color=PALE, stroke_width=1.2).set_opacity(0.5))
    leaves = small_leaves(leaf_count, c + DOWN * 0.15, (1.1, 0.55), seed=leaf_count + 10)
    tie = VGroup(Line(c + [-0.35, 1.12, 0], c + [0, 0.85, 0], color=PALE, stroke_width=4),
                 Line(c + [0.35, 1.12, 0], c + [0, 0.85, 0], color=PALE, stroke_width=4))
    g = VGroup(outline, leaves, mesh, tie).scale(scale)
    g.outline, g.leaves = outline, leaves
    return g


def balance(center=ORIGIN, reading="100%", color=GOLD, scale=1.0):
    c = np.array(center, float)
    beam = Line(c + [-1.25, 0.45, 0], c + [1.25, 0.45, 0], color=GREY, stroke_width=6)
    post = Line(c + [0, -0.85, 0], c + [0, 0.48, 0], color=GREY, stroke_width=6)
    base = Line(c + [-0.72, -0.87, 0], c + [0.72, -0.87, 0], color=GREY, stroke_width=6)
    pan = Arc(radius=0.75, start_angle=PI, angle=PI, arc_center=c + [0, 0.02, 0],
              color=GREY, stroke_width=5)
    read = M(reading, 34, color).move_to(c + [0, -1.25, 0])
    return VGroup(beam, post, base, pan, read).scale(scale)


def bathtub(center=(0, -0.15, 0), width=8.8, height=4.6, pile=0.55, drain=True):
    """The chapter-one schematic bathtub, always rebuilt at the same scale."""
    c = np.array(center, float)
    left, right = c[0] - width / 2, c[0] + width / 2
    bottom, top = c[1] - height / 2, c[1] + height / 2
    back = Rectangle(width=width, height=height, stroke_width=0, fill_color=PALE,
                     fill_opacity=.14).move_to(c)
    tub = VGroup(back,
                 Line([left, top, 0], [left, bottom, 0], color=PALE, stroke_width=7),
                 Line([left, bottom, 0], [right, bottom, 0], color=PALE, stroke_width=7),
                 Line([right, bottom, 0], [right, top, 0], color=PALE, stroke_width=7))
    layers = VGroup()
    count = max(1, int(round(6 * pile)))
    for k in range(count):
        w = width * (0.62 - 0.035 * k)
        layers.add(RoundedRectangle(corner_radius=0.08, width=w, height=0.35,
                                    stroke_color=TAN, stroke_width=2, fill_color=TAN,
                                    fill_opacity=0.55).move_to([c[0] - 0.55, bottom + 0.25 + 0.38 * k, 0]))
    drain_m = VGroup()
    if drain:
        hole = Circle(radius=0.28, color=PURPLE, stroke_width=5).move_to([right - 0.7, bottom, 0])
        out = arrow([right - 0.7, bottom - 0.05, 0], [right - 0.7, bottom - 1.0, 0], PURPLE, 7)
        drain_m.add(hole, out)
    g = VGroup(tub, layers, drain_m)
    g.tub, g.layers, g.drain = tub, layers, drain_m
    return g


def hillside_world(show_labels=True, bags=True):
    """The Weimer Run hillside, fixed across the field-method scenes."""
    slope = Polygon([-6.2, 2.35, 0], [5.9, -1.65, 0], [5.9, -3.0, 0], [-6.2, -3.0, 0],
                    color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.13)
    stream = VGroup(*[Arc(radius=0.55 + 0.18 * i, start_angle=-0.1, angle=PI,
                          color=DATA, stroke_width=4).move_to([5.15 + 0.12 * i, -2.45, 0]) for i in range(3)])
    trees = VGroup()
    for x, y, s in [(-5.3, 1.7, .9), (-3.2, .98, .75), (-.6, .1, .8), (2.1, -.75, .7)]:
        trunk = Line([x, y - .55 * s, 0], [x, y + .25 * s, 0], color=GREY, stroke_width=5)
        crown = Circle(radius=.55 * s, color=GREEN, stroke_width=3,
                       fill_color=GREEN, fill_opacity=.26).move_to([x, y + .56 * s, 0])
        trees.add(VGroup(trunk, crown))
    bag_pos = [(-3.8, .2, 0), (-.45, -.9, 0), (2.8, -1.9, 0)]  # higher, middle, lower
    bag_group = VGroup(*[mesh_bag(p, .32, 4, highlight=(i == 0)) for i, p in enumerate(bag_pos)]) if bags else VGroup()
    labels = VGroup()
    if show_labels:
        label_pos = [(-5.7, .25, 0), (-.45, -.15, 0), (2.8, -1.15, 0)]
        for text, p, col in [("higher", label_pos[0], DATA), ("middle", label_pos[1], TEXT), ("lower", label_pos[2], TEXT)]:
            lab = T(text, 28, col).move_to(p)
            lab.layout_ok = True  # site labels deliberately sit on the schematic hillside fill
            labels.add(lab)
    g = VGroup(slope, trees, stream, bag_group, labels)
    g.bags, g.labels, g.stream, g.trees = bag_group, labels, stream, trees
    return g


def higher_plot(points_through=6, line=False, small=False):
    """Measured higher-site data. The line is piecewise interpolation of those data."""
    if small:
        P = Plot(box=(0.65, 5.9, -1.65, 2.15), xr=(0, 24), yr=(0, 105),
                 xticks=[0, 12, 24], yticks=[(0, "0"), (50, "50"), (100, "100")],
                 xlabel="months", ylabel="mass left (%)", size=27, label_size=28)
    else:
        P = Plot(box=(-5.55, 5.65, -2.35, 2.35), xr=(0, 24), yr=(0, 105),
                 xticks=[0, 1, 8, 12, 20, 24], yticks=[(0, "0"), (50, "50"), (100, "100")],
                 xlabel="months", ylabel="mass left (%)", size=22, label_size=28)
    back = RoundedRectangle(corner_radius=.12, width=P.x1-P.x0-.7, height=P.y1-P.y0-.7,
                            stroke_width=0, fill_color=DATA, fill_opacity=.30)
    back.move_to([(P.x0+P.x1)/2, (P.y0+P.y1)/2, 0])
    P.add(back)
    P.submobjects.insert(0, P.submobjects.pop())
    P.backplate = back
    dots = VGroup(*[Dot(P.pt(x, y), radius=.13 if not small else .1, color=DATA,
                        stroke_color=TEXT, stroke_width=2) for x, y in zip(MONTHS[:points_through], MASS[:points_through])])
    curve = VGroup()
    if line and points_through > 1:
        pts = [P.pt(x, y) for x, y in zip(MONTHS[:points_through], MASS[:points_through])]
        curve = VMobject(stroke_color=DATA, stroke_width=6, fill_opacity=0).set_points_as_corners(pts)
    return P, dots, curve


def measured_graph_backdrop(points=6, line=True):
    P, dots, curve = higher_plot(points, line)
    title = T("higher site · Weimer Run", 32, DATA, weight=BOLD).move_to([0, 3.28, 0])
    return VGroup(P, curve, dots, title)


def scan_band(P, x, color=DATA):
    """A broad attention guide that keeps a plot visibly active while it is introduced."""
    return Rectangle(width=1.05, height=P.y1-P.y0, stroke_width=0, fill_color=color,
                     fill_opacity=.75).move_to([(P.pt(x, 0)[0]), (P.y0+P.y1)/2, 0])


def worm(center=(-2.3, 0, 0), scale=.75):
    c = np.array(center, float)
    pts = [c + [i * .33, .18 * np.sin(i * 1.4), 0] for i in range(7)]
    w = VMobject(stroke_color=PURPLE, stroke_width=13, fill_opacity=0).set_points_smoothly(pts)
    eye = Dot(pts[-1] + UP * .04, radius=.035, color=TEXT)
    return VGroup(w, eye).scale(scale)


def millipede(center=(2.0, 0, 0), scale=.75):
    c = np.array(center, float)
    body = VGroup(*[Circle(radius=.16, color=PURPLE, stroke_width=3,
                           fill_color=PURPLE, fill_opacity=.45).move_to(c + [i * .28, 0, 0]) for i in range(8)])
    legs = VGroup(*[Line(c + [i * .28, -.1, 0], c + [i * .28 - .08, -.3, 0], color=PURPLE, stroke_width=3)
                    for i in range(8)],
                  *[Line(c + [i * .28, .1, 0], c + [i * .28 + .08, .3, 0], color=PURPLE, stroke_width=3)
                    for i in range(8)])
    return VGroup(body, legs).scale(scale)


def mesh_question_backdrop(question=True):
    bag = mesh_bag((0, .65, 0), 1.28, 8)
    w = worm((-5.25, .55, 0), 1.0)
    m = millipede((3.75, .55, 0), 1.0)
    left_stop = arrow(w.get_right(), bag.get_left() + LEFT * .06, PURPLE, 5)
    right_stop = arrow(m.get_left(), bag.get_right() + RIGHT * .06, PURPLE, 5)
    bars = VGroup(Line(bag.get_left() + UP * .75, bag.get_left() + DOWN * .75, color=PALE, stroke_width=7),
                  Line(bag.get_right() + UP * .75, bag.get_right() + DOWN * .75, color=PALE, stroke_width=7))
    g = VGroup(bag, w, m, left_stop, right_stop, bars)
    if question:
        g.add(question_card("Faster or slower without the mesh?", y=-3.05, max_w=10.2))
    return g


class S00Title(TitleCard):
    LESSON = "Producers, consumers and decomposers"
    TITLE = "Weighing the Drain"


class S01Link(SpokenScene):
    def construct(self):
        tub = bathtub(pile=.72)
        tag = scope_tag("schematic")
        self.at("first film showed")
        self.play(Create(tub.tub), FadeIn(tub.layers, shift=DOWN * .15), run_time=1.25)
        bob(tub.layers, amp=.11, speed=1.05)
        self.play(FadeIn(tub.drain), run_time=.55)
        dots = VGroup(*[Dot([-2.2 + .55 * i, -.5 + .14 * (i % 2), 0], radius=.1, color=GOLD) for i in range(7)])
        co2 = T("carbon dioxide", 28, GREY).move_to([4.55, 2.45, 0])
        out = arrow([2.9, -.5, 0], [4.25, 1.95, 0], GREY, 5)
        self.play(FadeIn(dots), run_time=.45)
        self.play(dots[:3].animate.shift(RIGHT * 5 + UP * 2.2), GrowArrow(out), FadeIn(co2), run_time=1.0)
        self.at("how fast")
        clock = Circle(radius=.78, color=GOLD, stroke_width=5).move_to([4.6, -.8, 0])
        hands = VGroup(Line(clock.get_center(), clock.get_center() + UP * .48, color=TEXT, stroke_width=5),
                       Line(clock.get_center(), clock.get_center() + RIGHT * .35, color=TEXT, stroke_width=5))
        how = T("how fast?", 38, GOLD, weight=BOLD).move_to([2.15, -3.12, 0])
        self.play(Create(clock), Create(hands), FadeIn(how), FadeIn(tag), run_time=1.1)
        self.at("measure matter")
        pulse(tub.drain[0], base=5, amp=2)
        self.play(Rotate(hands[0], -TAU * .75, about_point=clock.get_center()),
                  run_time=1.7, rate_func=linear)
        self.finish()


class S02Place(SpokenScene):
    def construct(self):
        va = Polygon([-5.3, -1.8, 0], [-4.1, 2.35, 0], [-1.0, 2.0, 0], [.6, .35, 0],
                     [-.2, -1.8, 0], color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.08)
        wv = Polygon([-2.45, .65, 0], [-1.75, 1.8, 0], [-.65, 1.45, 0], [-.4, .25, 0],
                     [-1.45, -.15, 0], color=DATA, stroke_width=5, fill_color=DATA, fill_opacity=.18)
        va_l = T("Virginia", 30, GREY).move_to([-2.2, -2.35, 0])
        wv_l = T("West Virginia", 30, DATA).move_to([1.8, 1.8, 0])
        davis = T("Davis", 28, GOLD).move_to([.25, .45, 0])
        davis.layout_ok = True  # map labels intentionally sit over the schematic state polygons
        pin = VGroup(Dot([-1.25, .65, 0], radius=.18, color=GOLD), davis)
        date = chip("October 2011", GOLD, 32).move_to([3.65, -1.8, 0])
        self.at("Researchers in West Virginia")
        self.play(FadeIn(va), FadeIn(va_l), run_time=.8)
        self.play(FadeIn(wv), FadeIn(wv_l), run_time=.8)
        self.at("October")
        self.play(FadeIn(date, shift=UP * .2), run_time=.7)
        self.at("worked in the")
        self.play(FadeIn(pin, shift=UP * .15), run_time=.7)
        watershed = T("Weimer Run watershed", 32, DATA, weight=BOLD).move_to([2.65, -.15, 0])
        watershed.layout_ok = True  # map label intentionally sits over the schematic state polygon
        self.play(FadeIn(watershed), run_time=.6)
        self.at("near the town")
        hill = hillside_world(show_labels=False, bags=False)
        self.play(FadeOut(VGroup(va, va_l, wv, wv_l, pin, date, watershed)), FadeIn(hill), run_time=.65)
        self.play(hill.trees.animate.shift(UP * .08), rate_func=there_and_back, run_time=.75)
        self.finish()


class S03Bags(SpokenScene):
    def construct(self):
        loose = small_leaves(7, (-3.8, .25, 0), (1.25, .7), seed=21)
        bag = mesh_bag((-3.8, .25, 0), .95, 7)
        bag.leaves.set_opacity(0)
        self.at("sealed dried yellow")
        self.play(FadeIn(loose, lag_ratio=.08), run_time=.65)
        self.play(Create(bag.outline), FadeIn(VGroup(*bag[2:])),
                  ReplacementTransform(loose, bag.leaves.copy().set_opacity(1)), run_time=1.15)
        scale = balance((2.3, -.15, 0), "100%", GOLD, 1.15)
        self.at("weighed the leaves")
        self.play(FadeIn(scale, shift=UP * .15), bag.animate.move_to([2.3, 1.25, 0]).scale(.68), run_time=.85)
        self.play(Rotate(scale[0], .04, about_point=scale[0].get_center()), rate_func=there_and_back, run_time=.55)
        self.at("Then they set")
        hill = hillside_world(show_labels=False, bags=False)
        self.play(FadeOut(VGroup(bag, scale)), FadeIn(hill), run_time=.65)
        self.at("three heights")
        full = hillside_world(show_labels=True, bags=True)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * .18) for b in full.bags], lag_ratio=.25), run_time=1.05)
        self.play(LaggedStart(*[FadeIn(l) for l in full.labels], lag_ratio=.25), run_time=.75)
        self.finish()


class S04Return(SpokenScene):
    def construct(self):
        hill = hillside_world(show_labels=True, bags=True)
        months = [1, 8, 12, 20, 24]
        xvals = np.linspace(-4.8, 3.7, 5)
        line = Line([-5.6, -3.0, 0], [4.5, -3.0, 0], color=GREY, stroke_width=4)
        ticks = VGroup(*[Line([x, -3.15, 0], [x, -2.85, 0], color=GOLD, stroke_width=4) for x in xvals])
        labs = VGroup(*[M(str(m), 24, GOLD).move_to([x, -3.43, 0]) for x, m in zip(xvals, months)])
        unit = T("months", 24, GREY).move_to([5.45, -3.45, 0])
        self.add(hill)
        self.at("Five times")
        self.play(Create(line), LaggedStart(*[Create(t) for t in ticks], lag_ratio=.12), run_time=.85)
        self.play(LaggedStart(*[FadeIn(l) for l in labs], lag_ratio=.1), FadeIn(unit), run_time=.7)
        self.at("brought some bags back")
        selected = hill.bags[0].copy()
        self.play(selected.animate.move_to([4.8, 1.9, 0]).scale(1.7), run_time=.9)
        self.at("Different bags")
        echoes = VGroup(*[mesh_bag([x, 2.45, 0], .24, max(2, 6-i), highlight=True) for i, x in enumerate(xvals)])
        self.play(LaggedStart(*[FadeIn(b, shift=UP * .2) for b in echoes], lag_ratio=.14),
                  FadeOut(selected), run_time=1.15)
        self.at("dried the leaves")
        dry_text = T("dry", 32, ORANGE)
        dry_text.layout_ok = True  # deliberate label centred inside the drying-oven icon
        oven = VGroup(RoundedRectangle(corner_radius=.16, width=2.0, height=1.55, color=ORANGE,
                                       stroke_width=4, fill_color=ORANGE, fill_opacity=.1),
                      dry_text).move_to([2.9, .6, 0])
        scale = balance([5.25, .2, 0], "mass", GOLD, .78)
        self.play(FadeOut(echoes), FadeIn(oven), run_time=.55)
        self.play(hill.bags[1].copy().animate.move_to(oven.get_center()).scale(1.35), run_time=.55)
        self.at("weighed them again")
        self.play(FadeIn(scale), oven.animate.set_opacity(.45), run_time=.65)
        self.finish()


class S05Dry(SpokenScene):
    def construct(self):
        panels = TwoPanel("wet leaves", "dried leaves", colors=(DATA, GOLD), top=3.1, bottom=-2.45)
        panels.left_frame.set_fill(DATA, .14)
        panels.right_frame.set_fill(GOLD, .14)
        wet = leaf_shape([-3.2, .75, 0], 3.0)
        dry = leaf_shape([3.2, .75, 0], 3.0)
        drops = VGroup(*[Circle(radius=.13, color=DATA, fill_color=DATA, fill_opacity=.65)
                         .move_to([-4.2 + .5*i, 1.75 + .12*(i%2), 0]) for i in range(5)])
        sw = balance([-3.2, -.95, 0], "heavier", DATA, .8)
        sd = balance([3.2, -.95, 0], "dry mass", GOLD, .8)
        self.at("Why dry")
        self.play(FadeIn(panels), FadeIn(wet), FadeIn(dry), run_time=.8)
        self.play(FadeIn(drops, lag_ratio=.1), run_time=.6)
        self.at("Wet leaves")
        self.play(FadeIn(sw), sw[0].animate.rotate(.07), wet.animate.shift(DOWN * .32), run_time=.75)
        self.at("Drying them")
        self.play(drops.animate.shift(UP * 1.1).set_opacity(0), dry.animate.set_fill(TAN, .28), run_time=1.0)
        self.play(FadeIn(sd), run_time=.55)
        rule = caption("✓ weigh only dry leaves", 34, GOLD)
        self.at("water in the leaves")
        self.play(FadeIn(rule, shift=UP * .15), run_time=.7)
        self.play(Indicate(sd, color=GOLD, scale_factor=1.04), run_time=1.15)
        self.finish()


class S06Graph(SpokenScene):
    def construct(self):
        P, _, _ = higher_plot(0, False)
        title = T("higher site · Weimer Run", 32, DATA, weight=BOLD).move_to([0, 3.28, 0])
        self.at("follow the higher site")
        self.play(FadeIn(title, shift=DOWN * .15), run_time=.75)
        self.at("graph shows")
        self.play(Create(P), run_time=1.3)
        sweep = scan_band(P, 0)
        self.add(sweep)
        self.play(sweep.animate.move_to([P.pt(24, 0)[0], (P.y0+P.y1)/2, 0]),
                  run_time=2.25, rate_func=linear)
        self.remove(sweep)
        start = Dot(P.pt(0, 100), radius=.15, color=DATA, stroke_color=TEXT, stroke_width=2)
        start_l = T("start", 28, GOLD).next_to(start, RIGHT, buff=.18)
        self.at("Every bag started")
        self.play(FadeIn(start, scale=.6), FadeIn(start_l), run_time=.7)
        self.play(Indicate(start, color=DATA, scale_factor=1.35), run_time=.8)
        avg = chip("each dot: average of 8 or 9 bags", PALE, 28).move_to([2.25, 1.35, 0])
        self.at("Each later dot")
        self.play(FadeIn(avg, shift=LEFT * .15), run_time=.8)
        samples = VGroup(*[Circle(radius=.11, color=DATA, fill_color=DATA, fill_opacity=.35)
                           .move_to([.25 + .32*(i%5), .15 + .32*(i//5), 0]) for i in range(9)])
        self.play(FadeIn(samples, lag_ratio=.08), run_time=.8)
        one = Dot(P.pt(1, 72), radius=.16, color=DATA, stroke_color=TEXT, stroke_width=2)
        value = M("72.0%", 38, DATA).next_to(one, RIGHT, buff=.25)
        self.at("After one month")
        self.play(FadeOut(VGroup(avg, samples)), FadeIn(one, shift=UP * .7), run_time=.8)
        self.at("about 72")
        self.play(FadeIn(value, shift=LEFT * .15), run_time=.75)
        self.play(Indicate(VGroup(one, value), color=DATA, scale_factor=1.08), run_time=.65)
        self.finish()


class S07Leaching(SpokenScene):
    def construct(self):
        leaf = leaf_shape([0, .3, 0], 5.1)
        soil = Rectangle(width=12.3, height=1.55, stroke_color=GREY, stroke_width=3,
                         fill_color=GREY, fill_opacity=.16).move_to([0, -2.15, 0])
        rain = VGroup(*[Line([-4.5 + i*1.0, 3.1, 0], [-4.7 + i*1.0, 2.35, 0],
                                 color=DATA, stroke_width=5) for i in range(10)])
        self.at("first drop was fast")
        self.play(FadeIn(soil), FadeIn(leaf), run_time=.75)
        bob(leaf, amp=.10, speed=1.15)
        fast = arrow([-5.5, 2.1, 0], [-5.5, -.3, 0], DATA, 7)
        self.play(GrowArrow(fast), run_time=.65)
        self.at("probably rain")
        self.play(LaggedStart(*[Create(r) for r in rain], lag_ratio=.06), run_time=.9)
        specks = VGroup(*[Dot([-1.5 + .5*i, -.05 + .1*(i%2), 0], radius=.11, color=PALE) for i in range(7)])
        self.at("washing sugars")
        self.play(FadeIn(specks), run_time=.45)
        self.play(*[d.animate.move_to([-2.2 + .7*i, -2.15 - .08*(i%2), 0]) for i, d in enumerate(specks)],
                  run_time=1.45)
        sugar = T("dissolved sugars", 30, PALE).move_to([4.35, -.95, 0])
        self.play(FadeIn(sugar), run_time=.55)
        label = chip("leaching", DATA, 38).move_to([3.9, 2.05, 0])
        self.at("called leaching")
        self.play(FadeIn(label, scale=.85), FadeOut(fast), run_time=.75)
        dim = chip("decomposers", PURPLE, 28, fill_opacity=.04).set_opacity(.3).move_to([-3.9, 1.85, 0])
        no = T("not needed", 28, GREY).next_to(dim, DOWN, buff=.18)
        self.at("does not need")
        self.play(FadeIn(dim), FadeIn(no), run_time=.65)
        self.play(rain.animate.shift(DOWN * .25), rate_func=there_and_back, run_time=1.0)
        self.finish()


class S08Year(SpokenScene):
    def construct(self):
        P, dots2, line2 = higher_plot(2, True)
        title = T("higher site · Weimer Run", 32, DATA, weight=BOLD).move_to([0, 3.28, 0])
        self.add(P, line2, dots2, title)
        self.at("jump to 12")
        sweep = scan_band(P, 0, GOLD)
        self.add(sweep)
        self.play(sweep.animate.move_to([P.pt(12, 0)[0], (P.y0+P.y1)/2, 0]),
                  run_time=1.0, rate_func=linear)
        self.remove(sweep)
        p8 = Dot(P.pt(8, 68.9), radius=.13, color=DATA, stroke_color=TEXT, stroke_width=2)
        p12 = Dot(P.pt(12, 59.7), radius=.16, color=DATA, stroke_color=TEXT, stroke_width=2)
        seg = VMobject(stroke_color=DATA, stroke_width=6).set_points_as_corners([P.pt(1,72), P.pt(8,68.9), P.pt(12,59.7)])
        self.play(FadeIn(p8), Create(seg), run_time=.75)
        self.play(FadeIn(p12, shift=UP * .5), run_time=.55)
        val = chip("59.7% left", DATA, 36, fill_opacity=.28).next_to(p12, RIGHT, buff=.2)
        self.at("About 60")
        self.play(FadeIn(val), run_time=.65)
        area = Polygon(P.pt(0,100), P.pt(12,100), P.pt(12,59.7), P.pt(0,100),
                       color=GOLD, stroke_width=0, fill_color=GOLD, fill_opacity=.16)
        bracket = BraceBetweenPoints(P.pt(12,100), P.pt(12,59.7), direction=RIGHT, color=GOLD)
        self.at("about 40")
        calc = M("100 − 59.7 = 40.3% gone", 28, GOLD)
        calc.move_to([P.pt(12,100)[0] + .35 + calc.width / 2, 2.2, 0])
        self.play(FadeIn(area), GrowFromCenter(bracket), FadeIn(calc), run_time=1.0)
        gone = T("gone in 1 year", 28, GOLD).next_to(bracket, RIGHT, buff=.18)
        self.play(FadeIn(gone), run_time=.65)
        self.finish()


class S09Two(SpokenScene):
    def construct(self):
        P, dots4, line4 = higher_plot(4, True)
        title = T("higher site · Weimer Run", 32, DATA, weight=BOLD).move_to([0, 3.28, 0])
        half = P.hline(50, "50%", GREY, 26, True)
        self.add(P, line4, dots4, title)
        self.at("At 24 months")
        sweep = scan_band(P, 12, GOLD)
        self.add(sweep)
        self.play(sweep.animate.move_to([P.pt(24, 0)[0], (P.y0+P.y1)/2, 0]),
                  run_time=.8, rate_func=linear)
        self.remove(sweep)
        self.play(FadeIn(half), run_time=.55)
        p20 = Dot(P.pt(20,55.8), radius=.13, color=DATA, stroke_color=TEXT, stroke_width=2)
        p24 = Dot(P.pt(24,47.8), radius=.16, color=DATA, stroke_color=TEXT, stroke_width=2)
        seg = VMobject(stroke_color=DATA, stroke_width=6).set_points_as_corners([P.pt(12,59.7), P.pt(20,55.8), P.pt(24,47.8)])
        self.play(FadeIn(p20), Create(seg), FadeIn(p24), run_time=.95)
        val = chip("47.8% left", DATA, 34, fill_opacity=.28).move_to([4.35, -.72, 0])
        self.play(FadeIn(val), run_time=.55)
        self.at("still losing mass")
        moving = Dot(P.pt(12,59.7), radius=.09, color=GOLD)
        self.play(MoveAlongPath(moving, seg.copy()), run_time=1.4, rate_func=linear)
        self.at("more slowly")
        slow = T("slower", 32, GOLD, weight=BOLD).move_to(P.pt(18, 70))
        year2 = Line(P.pt(12,59.7), P.pt(24,47.8), color=GOLD, stroke_width=9).set_opacity(.35)
        self.play(Create(year2), FadeIn(slow), run_time=.75)
        self.play(Indicate(VGroup(year2, slow), color=GOLD, scale_factor=1.04), run_time=.8)
        self.finish()


class S10Predict(SpokenScene):
    def construct(self):
        bag = mesh_bag((0, .65, 0), 1.28, 8)
        w = worm((-5.25, .55, 0), 1.0)
        m = millipede((3.75, .55, 0), 1.0)
        self.at("One more thing")
        self.play(FadeIn(bag), run_time=.7)
        bob(bag, amp=.11, speed=1.2)
        self.at("mesh kept")
        self.play(FadeIn(w, shift=RIGHT * .25), FadeIn(m, shift=LEFT * .25), run_time=.7)
        stops = VGroup(Line(bag.get_left() + UP * .75, bag.get_left() + DOWN * .75, color=PALE, stroke_width=7),
                       Line(bag.get_right() + UP * .75, bag.get_right() + DOWN * .75, color=PALE, stroke_width=7))
        self.play(w.animate.shift(RIGHT * 1.2), m.animate.shift(LEFT * 1.2), FadeIn(stops), run_time=.75, rate_func=there_and_back)
        self.at("On an open")
        q = question_card("Faster or slower without the mesh?", y=-3.05, max_w=10.2)
        self.play(FadeIn(q.question, shift=UP * .15), run_time=.75)
        self.at("faster or slower")
        self.play(Indicate(q.question, color=GOLD, scale_factor=1.04), run_time=1.25)
        self.finish()


class S11Pause(PredictPause):
    QUESTION = "Faster or slower without the mesh?"
    SECONDS = 5.0
    CARD = {"y": -3.05, "max_w": 10.2}

    def backdrop(self):
        return mesh_question_backdrop(False)

    def construct(self):
        self.add(self.backdrop())
        self.add(question_card(self.QUESTION, y=-3.05, max_w=10.2))
        remaining = ValueTracker(5.0)
        center = np.array([5.7, -2.85, 0])
        ring = Circle(radius=.9, color=GREY, stroke_width=6).move_to(center)
        arc = always_redraw(lambda: Arc(radius=.9, start_angle=PI/2,
                                         angle=max(remaining.get_value()/5, .001)*TAU,
                                         color=GOLD, stroke_width=11, arc_center=center))
        number = always_redraw(lambda: M(str(max(1, int(np.ceil(remaining.get_value())))),
                                         54, GOLD).move_to(center))
        self.add(ring, arc, number)
        self.play(remaining.animate.set_value(0), run_time=5, rate_func=linear)
        self.finish()


class S12Reveal(SpokenScene):
    def construct(self):
        big = leaf_shape([-2.25, .45, 0], 4.0)
        w = worm((-5.3, 1.2, 0), .9)
        m = millipede((-1.0, 1.4, 0), .75)
        answer = chip("probably faster", GOLD, 38).move_to([3.7, 2.65, 0])
        self.at("Probably faster")
        self.play(FadeIn(big), FadeIn(w), FadeIn(m), FadeIn(answer, scale=.85), run_time=.9)
        self.at("tear dead")
        bits = VGroup(*[RoundedRectangle(corner_radius=.06, width=.65, height=.38, color=TAN,
                                         stroke_width=2, fill_color=TAN, fill_opacity=.6)
                        .move_to([-3.8 + .75*(i%5), -.35 + .55*(i//5), 0]) for i in range(15)])
        self.play(w.animate.shift(RIGHT * 1.25), m.animate.shift(LEFT * .8), run_time=.55)
        self.play(ReplacementTransform(big, bits), run_time=.85)
        self.at("Smaller bits")
        self.play(*[b.animate.shift([.12*(i%3-1), .09*((i+1)%3-1), 0]) for i,b in enumerate(bits)], run_time=.6)
        threads = VGroup(*[ArcBetweenPoints([-4.1 + .65*i, -.9, 0], [-3.75 + .65*i, .95, 0],
                                             angle=(-1)**i*.65, color=PURPLE, stroke_width=4) for i in range(7)])
        fungi = T("fungi + bacteria", 30, PURPLE).move_to([-2.25, -1.7, 0])
        surface = T("more surface", 32, GOLD, weight=BOLD).move_to([-2.25, -2.35, 0])
        self.at("fungi and bacteria")
        self.play(LaggedStart(*[Create(t) for t in threads], lag_ratio=.08), FadeIn(fungi), run_time=1.15)
        self.at("more surface")
        self.play(FadeIn(surface), run_time=.6)
        P, dots, line = higher_plot(6, True, small=False)
        ghost_pts = [P.pt(x, max(4, y - (x/24)*18)) for x,y in zip(MONTHS, MASS)]
        ghost = DashedVMobject(VMobject(stroke_color=GOLD, stroke_width=5).set_points_as_corners(ghost_pts), num_dashes=18)
        glab = fit_text("open floor: probably faster", 5.5, 28, GOLD).move_to([2.65, -1.6, 0])
        self.at("bags probably show")
        self.play(FadeOut(VGroup(w,m,threads,fungi,surface,bits,answer)), FadeIn(P), FadeIn(line), FadeIn(dots), run_time=.75)
        self.play(Create(ghost), FadeIn(glab), FadeIn(scope_tag("schematic, not measured")), run_time=1.1)
        self.finish()


class S13Tub(SpokenScene):
    def construct(self):
        tub = bathtub(pile=.55)
        title = T("bathtub model", 34, PALE, weight=BOLD).move_to([0, 3.2, 0])
        model = scope_tag("schematic model")
        self.at("In these bags")
        self.play(Create(tub.tub), FadeIn(tub.layers), FadeIn(tub.drain), FadeIn(title), FadeIn(model), run_time=1.0)
        bob(tub.layers, amp=.10, speed=1.0)
        stat = fit_text("about 40% gone in year 1 · about half in 2 years", 10.4, 30, DATA).move_to([0, 2.45, 0])
        self.at("about 40")
        self.play(FadeIn(stat, shift=DOWN * .1), run_time=.75)
        matter = VGroup(*[Dot([-2.8 + .55*i, -.4 + .13*(i%2), 0], radius=.1, color=GOLD) for i in range(10)])
        self.play(FadeIn(matter), matter[:4].animate.shift(RIGHT * 5 + DOWN * 1.4).set_opacity(0), run_time=.9)
        self.at("Suppose a model")
        premise = chip("40% of whole pile leaves each year", PURPLE, 30).move_to([0, 1.55, 0])
        self.play(FadeOut(stat), FadeIn(premise, shift=DOWN * .15), run_time=.75)
        tracker = ValueTracker(.35)
        gauge_dial = dial(tracker, [5.15, .75, 0], radius=.85, label="", color=PURPLE, size=30)
        gauge_label = T("annual drain", 26, PURPLE).move_to([5.55, -.45, 0])
        gauge = VGroup(gauge_dial, gauge_label)
        self.play(FadeIn(gauge), run_time=.55)
        self.play(tracker.animate.set_value(.40), run_time=.75)
        self.at("pile would level")
        calc = M("1 ÷ 0.40 ≈ 2.5 autumns", 32, GOLD).move_to([0, -2.85, 0])
        extra = VGroup(*[RoundedRectangle(corner_radius=.07, width=4.2-.16*k, height=.32,
                                          color=TAN, stroke_width=2, fill_color=TAN, fill_opacity=.55)
                         .move_to([-.55, -.15 + .34*k, 0]) for k in range(4)])
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN*.18) for x in extra], lag_ratio=.16), FadeIn(calc), run_time=1.4)
        plateau = T("model only", 24, GOLD).move_to([-3.45, .85, 0])
        self.play(FadeIn(plateau), run_time=.5)
        self.at("But these bags")
        self.play(FadeOut(VGroup(premise, gauge, calc, plateau, matter, extra, tub, title, model)), run_time=.55)
        graph = measured_graph_backdrop()
        self.play(FadeIn(graph), run_time=.7)
        slow = chip("year 2: slower", GOLD, 30).move_to([2.1, 1.3, 0])
        self.at("more slowly in year two")
        self.play(FadeIn(slow, shift=LEFT*.15), run_time=.7)
        self.play(Indicate(graph[1], color=GOLD, scale_factor=1.02), run_time=.8)
        self.at("cannot tell us")
        q = T("real pile height: ?", 38, GOLD, weight=BOLD).move_to([0, -1.15, 0])
        self.play(FadeIn(q, scale=.85), run_time=.65)
        self.play(q.animate.shift(UP*.12), rate_func=there_and_back, run_time=.7)
        self.finish()


class S14Takehome(SpokenScene):
    def construct(self):
        panels = TwoPanel("measured mass loss", "bathtub drain", colors=(DATA, PURPLE), top=3.1, bottom=-2.45)
        panels.left_frame.set_fill(DATA, .14)
        panels.right_frame.set_fill(PURPLE, .14)
        P, dots, line = higher_plot(6, True, small=True)
        graph = VGroup(P, line, dots).scale(.83).move_to([-3.25, .05, 0])
        tub = bathtub(center=(3.25, -.05, 0), width=4.2, height=3.0, pile=.55)
        link = arrow([-1.0, .3, 0], [1.0, .3, 0], GOLD, 6)
        self.at("early loss")
        self.play(FadeIn(panels), FadeIn(graph), FadeIn(tub), GrowArrow(link), run_time=1.0)
        causes = VGroup(chip("decomposers", PURPLE, 28), chip("leaching", DATA, 28),
                        chip("bits through mesh", TAN, 28)).arrange(DOWN, buff=.18).move_to([3.25, .55, 0])
        self.play(FadeOut(tub.layers), FadeIn(causes[1]), FadeIn(causes[0]), run_time=.8)
        self.at("all the loss together")
        all_loss = T("all causes together", 32, GOLD, weight=BOLD).move_to([0, -2.85, 0])
        self.play(FadeIn(causes[2]), FadeIn(all_loss), run_time=.8)
        self.at("cannot split")
        brace = Brace(causes, LEFT, color=GOLD)
        unknown = T("cannot split", 24, GOLD).move_to([1.4, -1.75, 0])
        self.play(GrowFromCenter(brace), FadeIn(unknown), run_time=.75)
        self.play(LaggedStart(*[Indicate(c, scale_factor=1.04) for c in causes], lag_ratio=.2), run_time=1.25)
        self.at("one kind of leaf")
        sample_bag = mesh_bag((-3.25, -.15, 0), .72, 6, highlight=True)
        scope = chip("yellow birch · fine mesh bags", TAN, 28).move_to([-3.25, 1.55, 0])
        self.play(FadeOut(graph), FadeIn(sample_bag), FadeIn(scope, shift=DOWN*.15), run_time=.75)
        notwhole = T("not a whole forest floor", 28, GREY).move_to([-3.25, -1.7, 0])
        self.at("not a whole")
        self.play(FadeIn(notwhole), run_time=.65)
        self.at("Weighing leaf bags")
        rule = fit_text("Weighing leaf bags measures how fast leaves lose mass.", 11.8, 38, GOLD,
                        min_size=32, max_lines=1).move_to([0, 0, 0])
        self.play(FadeOut(VGroup(panels, sample_bag, tub, link, causes, all_loss, brace, unknown, scope, notwhole)),
                  FadeIn(rule, scale=.92), run_time=1.0)
        underline = Line(rule.get_corner(DL)+DOWN*.16, rule.get_corner(DR)+DOWN*.16, color=GOLD, stroke_width=5)
        self.play(Create(underline), run_time=.8)
        self.finish()


class S15End(EndCard):
    LINE = "Weighing leaf bags measures how fast leaves lose mass."
