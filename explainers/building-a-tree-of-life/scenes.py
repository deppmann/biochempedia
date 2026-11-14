"""Which Similarities Reveal Relatives? — animated teaching film.

COLOR MAP
  BLUE = whale
  GREEN = hippo
  GREY = tuna, swimming-shape/function evidence
  TEAL = inherited evidence and derived traits
  GOLD = common ancestors and branch points

All animals, embryos, fossils, limbs, and trees are schematic teaching drawings.
"""
from bp_parts import *


# --------------------------------------------------------------------------------------
# One world, rebuilt from the same builders wherever it returns.

def animal(kind, color, scale=1.0):
    """Simple labelled silhouette; intentionally schematic, not anatomical."""
    if kind == "whale":
        body = Ellipse(3.2, 1.25, color=color, stroke_width=5, fill_color=color, fill_opacity=0.18)
        nose = ArcBetweenPoints([-1.55, 0.08, 0], [-1.35, -0.38, 0], angle=-1.0, color=color, stroke_width=5)
        tail = VGroup(Polygon([1.45, 0, 0], [2.05, 0.55, 0], [1.92, 0, 0], color=color,
                              fill_color=color, fill_opacity=0.18),
                      Polygon([1.45, 0, 0], [2.05, -0.55, 0], [1.92, 0, 0], color=color,
                              fill_color=color, fill_opacity=0.18))
        fin = Polygon([-0.1, -0.35, 0], [0.75, -0.95, 0], [0.5, -0.2, 0], color=color,
                      fill_color=color, fill_opacity=0.2)
        eye = Dot([-1.12, 0.22, 0], radius=0.055, color=TEXT)
        shape = VGroup(body, nose, tail, fin, eye)
    elif kind == "tuna":
        body = Ellipse(2.55, 1.05, color=color, stroke_width=5, fill_color=color, fill_opacity=0.18)
        tail = Polygon([1.18, 0, 0], [1.8, 0.62, 0], [1.62, 0, 0], [1.8, -0.62, 0],
                       color=color, fill_color=color, fill_opacity=0.18)
        fin = Polygon([-0.2, 0.38, 0], [0.15, 0.88, 0], [0.42, 0.34, 0], color=color,
                      fill_color=color, fill_opacity=0.18)
        eye = Dot([-0.86, 0.17, 0], radius=0.05, color=TEXT)
        shape = VGroup(body, tail, fin, eye)
    else:
        body = RoundedRectangle(corner_radius=0.45, width=2.55, height=1.22, color=color,
                                stroke_width=5, fill_color=color, fill_opacity=0.18)
        head = Circle(radius=0.52, color=color, stroke_width=5, fill_color=color, fill_opacity=0.18).shift(LEFT * 1.35)
        legs = VGroup(*[Line([x, -0.42, 0], [x - 0.08, -1.02, 0], color=color, stroke_width=7)
                        for x in (-0.72, 0.0, 0.72)])
        ears = VGroup(Triangle(color=color, fill_color=color, fill_opacity=0.18).scale(0.16).move_to([-1.52, 0.48, 0]),
                      Triangle(color=color, fill_color=color, fill_opacity=0.18).scale(0.16).move_to([-1.17, 0.48, 0]))
        eye = Dot([-1.55, 0.12, 0], radius=0.05, color=TEXT)
        shape = VGroup(body, head, legs, ears, eye)
    label = T(kind, 30, color).next_to(shape, DOWN, buff=0.12)
    g = VGroup(shape, label).scale(scale)
    g.layout_ok = True
    return g


def water_world(dim=False):
    water = RoundedRectangle(corner_radius=0.2, width=12.4, height=5.65, stroke_color=BLUE,
                             stroke_width=2, fill_color=BLUE, fill_opacity=0.10).move_to([0, 0.15, 0])
    river = RoundedRectangle(corner_radius=0.18, width=3.35, height=5.15, stroke_color=GREEN,
                             stroke_width=2, fill_color=GREEN, fill_opacity=0.09).move_to([4.45, 0.15, 0])
    waves = VGroup(*[Arc(radius=0.42, start_angle=0, angle=PI, color=BLUE, stroke_width=2)
                     .move_to([-5.6 + i * 0.72, 2.55, 0]) for i in range(16)]).set_opacity(0.35)
    bubbles = VGroup(*[Circle(radius=0.05 + 0.018 * (i % 3), color=BLUE, stroke_width=2)
                       .move_to([-5.7 + (i * 1.37) % 9.4, -2.2 + (i * 0.83) % 4.2, 0]) for i in range(12)])
    whale = animal("whale", BLUE, 0.92).move_to([-2.65, 0.75, 0])
    tuna = animal("tuna", GREY, 0.84).move_to([-2.9, -1.35, 0])
    hippo = animal("hippo", GREEN, 0.78).move_to([4.45, -0.25, 0])
    # These are deliberately behind the labels and silhouettes as environmental texture.
    water.layout_ok = river.layout_ok = waves.layout_ok = bubbles.layout_ok = True
    g = VGroup(water, river, waves, bubbles, whale, tuna, hippo)
    if dim:
        g.set_opacity(0.24)
    return g


def animate_world(world):
    bob(world[4], amp=0.17, speed=1.15)
    bob(world[5], amp=0.15, speed=1.35, seed=2)
    bob(world[6], amp=0.11, speed=0.85, seed=4)
    for i, b in enumerate(world[3]):
        bob(b, amp=0.16, speed=0.7 + 0.06 * i, seed=i)


def tree_picture(with_labels=True, water=False):
    """The carried tree: all scenes use these exact landmarks."""
    root = np.array([-4.9, -2.15, 0])
    n1, n2 = np.array([-2.5, -0.65, 0]), np.array([0.25, 0.35, 0])
    tuna_p, pig_p, cow_p = np.array([-3.45, 2.25, 0]), np.array([-0.75, 2.25, 0]), np.array([1.15, 2.25, 0])
    whale_p, hippo_p = np.array([3.25, 2.25, 0]), np.array([5.05, 2.25, 0])
    lines = VGroup(Line(root, n1, color=GREY, stroke_width=7), Line(n1, tuna_p, color=GREY, stroke_width=6),
                   Line(n1, n2, color=GREY, stroke_width=7), Line(n2, pig_p, color=GREY, stroke_width=5),
                   Line(n2, cow_p, color=GREY, stroke_width=5), Line(n2, whale_p, color=TEAL, stroke_width=7),
                   Line(n2, hippo_p, color=TEAL, stroke_width=7))
    nodes = VGroup(Dot(n1, radius=0.13, color=GOLD), Dot(n2, radius=0.17, color=GOLD))
    tips = VGroup(Dot(tuna_p, radius=0.1, color=GREY), Dot(pig_p, radius=0.1, color=GREY),
                  Dot(cow_p, radius=0.1, color=GREY), Dot(whale_p, radius=0.11, color=BLUE),
                  Dot(hippo_p, radius=0.11, color=GREEN))
    g = VGroup(lines, nodes, tips)
    crown = Polygon(n2 + [-0.62, -0.5, 0], whale_p + [-0.62, 0.05, 0],
                    whale_p + [0.55, 0.55, 0], hippo_p + [0.55, 0.55, 0],
                    hippo_p + [-0.55, 0.05, 0], n2 + [0.62, -0.5, 0],
                    stroke_opacity=0, fill_color=TEAL, fill_opacity=0.19)
    trunk = Polygon(root + [-0.28, -0.28, 0], n1 + [-0.28, 0.3, 0], n2 + [-0.28, 0.3, 0],
                    n2 + [0.28, -0.3, 0], n1 + [0.28, -0.3, 0], root + [0.28, 0.28, 0],
                    stroke_opacity=0, fill_color=TEAL, fill_opacity=0.17)
    clade_band = VGroup(crown, trunk).set_z_index(-2)
    clade_band.layout_ok = True
    g.add(clade_band)
    if with_labels:
        labels = VGroup(T("tuna", 28, GREY).next_to(tuna_p, UP, buff=0.13),
                        T("pig", 28, GREY).next_to(pig_p, UP, buff=0.13),
                        T("cow", 28, GREY).next_to(cow_p, UP, buff=0.13),
                        T("whale", 28, BLUE).next_to(whale_p, UP, buff=0.13),
                        T("hippo", 28, GREEN).next_to(hippo_p, UP, buff=0.13))
        labels.layout_ok = True
        g.add(labels)
    if water:
        bg = VGroup(*[Arc(radius=0.5, start_angle=0, angle=PI, color=BLUE, stroke_width=2)
                      .move_to([-6.1 + i * 0.85, -2.65, 0]) for i in range(15)]).set_opacity(0.24)
        field = RoundedRectangle(corner_radius=0.2, width=12.5, height=5.65, stroke_opacity=0,
                                 fill_color=BLUE, fill_opacity=0.075).move_to([0, 0.05, 0])
        field.layout_ok = bg.layout_ok = True
        g.add_to_back(field, bg)
    return g


def traveling_dots(points, color=TEAL, count=9, speed=0.12):
    """Evidence markers continuously follow a schematic route, including during narration holds."""
    pts = [np.array(p, dtype=float) for p in points]
    seg = np.array([np.linalg.norm(b - a) for a, b in zip(pts[:-1], pts[1:])])
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    total = max(cum[-1], 1e-6)
    group = VGroup()
    for i in range(count):
        d = Dot(pts[0], radius=0.055 + 0.012 * (i % 3), color=color).set_opacity(0.45 + 0.05 * (i % 4))
        d._travel_t = i / count

        def move(m, dt, pts=pts, cum=cum, total=total):
            m._travel_t = (m._travel_t + speed * dt) % 1.0
            s = m._travel_t * total
            j = min(np.searchsorted(cum, s, side="right") - 1, len(pts) - 2)
            a = (s - cum[j]) / max(cum[j + 1] - cum[j], 1e-6)
            m.move_to(interpolate(pts[j], pts[j + 1], a))
        d.add_updater(move)
        group.add(d)
    group.layout_ok = True
    return group


def trail_picture(question=True):
    fork = Dot([-4.65, 0.2, 0], radius=0.17, color=BLUE)
    start = Line([-6.15, 0.2, 0], [-4.65, 0.2, 0], color=BLUE, stroke_width=9)
    grey = VMobject(color=GREY, stroke_width=10).set_points_as_corners([
        [-4.65, 0.2, 0], [-2.4, 1.95, 0], [1.55, 1.95, 0], [5.2, 1.0, 0]])
    teal = VMobject(color=TEAL, stroke_width=10).set_points_as_corners([
        [-4.65, 0.2, 0], [-2.4, -1.55, 0], [1.55, -1.55, 0], [5.2, -0.65, 0]])
    labs = VGroup(T("outside shape", 32, GREY).move_to([-0.5, 2.5, 0]),
                  T("inherited features", 32, TEAL).move_to([-0.4, -2.15, 0]))
    covers = VGroup(RoundedRectangle(corner_radius=0.18, width=2.2, height=1.35, color=GREY,
                                     fill_color=BG, fill_opacity=1).move_to([5.2, 1.0, 0]),
                    RoundedRectangle(corner_radius=0.18, width=2.2, height=1.35, color=TEAL,
                                     fill_color=BG, fill_opacity=1).move_to([5.2, -0.65, 0]))
    covers.layout_ok = True  # question marks are deliberately centred on these covered outcomes
    g = VGroup(start, fork, grey, teal, labs, covers)
    if question:
        qs = VGroup(T("?", 58, GOLD, weight=BOLD).move_to([5.2, 1.0, 0]),
                    T("?", 58, GOLD, weight=BOLD).move_to([5.2, -0.65, 0]))
        qs.layout_ok = True
        g.add(qs)
    g.layout_ok = True
    return g


def limb_pattern():
    cols = [TEAL, BLUE, GREEN, GOLD]
    names = ["upper arm", "forearm pair", "wrist", "fingers"]
    widths = [1.55, 1.95, 1.05, 1.55]
    blocks = VGroup()
    x = -3.25
    for name, col, w in zip(names, cols, widths):
        block = RoundedRectangle(corner_radius=0.14, width=w, height=0.78, color=col, stroke_width=4,
                                 fill_color=col, fill_opacity=0.2)
        lab = fit_text(name, max_w=w - 0.16, size=34, min_size=28, max_lines=2, color=TEXT).move_to(block)
        labelled = VGroup(block, lab).move_to([x, 0, 0])
        labelled.layout_ok = True  # each bone-set label intentionally sits inside its own block
        blocks.add(labelled)
        x += w + 0.22
    return blocks


def limb_row(label, y, outline):
    blocks = limb_pattern().scale(0.82).move_to([0.55, y, 0])
    name = T(label, 30, TEXT).move_to([-5.55, y, 0])
    shell = RoundedRectangle(corner_radius=outline[0], width=7.25, height=outline[2], color=TEAL,
                             stroke_width=3).move_to([0.55, y, 0])
    return VGroup(name, shell, blocks)


def embryo(stage="early"):
    colors = [BLUE, GREEN, GREY]
    xs = [-3.8, 0, 3.8]
    g = VGroup()
    for i, (x, col) in enumerate(zip(xs, colors)):
        w = 2.05 + (0.3 * i if stage == "late" else 0)
        h = 3.05 - (0.35 * i if stage == "late" else 0)
        fill = Ellipse(w, h, color=col, stroke_opacity=0, fill_color=col, fill_opacity=0.18).move_to([x, 0.35, 0])
        body = Arc(radius=1.25, start_angle=-PI * 0.35, angle=PI * 1.55, color=col, stroke_width=10)
        body.stretch_to_fit_width(w).stretch_to_fit_height(h).move_to([x, 0.35, 0])
        tail = ArcBetweenPoints([x + 0.55, -0.65, 0], [x + 1.15, -1.15, 0], angle=-0.65,
                               color=TEAL, stroke_width=7)
        arches = VGroup(*[Arc(radius=0.28 + j * 0.08, start_angle=-1.0, angle=1.8,
                              color=TEAL, stroke_width=5).move_to([x - 0.45 + j * 0.12, 0.75, 0])
                           for j in range(3)])
        g.add(VGroup(fill, body, tail, arches))
    g.layout_ok = True
    return g


def fossil_timeline():
    axis = Arrow([-5.7, -1.55, 0], [5.75, -1.55, 0], buff=0, color=GREY, stroke_width=5,
                 tip_length=0.22)
    labels = VGroup(T("past", 30, GREY).next_to(axis.get_start(), DOWN, buff=0.15),
                    T("present", 30, TEXT).next_to(axis.get_end(), DOWN, buff=0.15))
    layers = VGroup(*[Rectangle(width=11.3, height=0.62, stroke_color=GOLD, stroke_width=2,
                                fill_color=GOLD, fill_opacity=0.10 + 0.025 * (i % 2))
                       .move_to([0, -0.85 + i * 0.62, 0]) for i in range(4)])
    layers.set_z_index(-2)
    fossil = animal("hippo", GOLD, 0.65).move_to([-3.1, 0.65, 0])
    fossil[1].become(T("fossil whale", 28, GOLD).next_to(fossil[0], DOWN, buff=0.12))
    modern = animal("whale", BLUE, 0.72).move_to([3.25, 0.65, 0])
    node = Dot([0.25, -0.05, 0], radius=0.15, color=GOLD)
    branches = VGroup(Line(node, fossil.get_bottom() + DOWN * 0.05, color=GOLD, stroke_width=5),
                      Line(node, modern.get_bottom() + DOWN * 0.05, color=GOLD, stroke_width=5))
    g = VGroup(axis, labels, layers, branches, node, fossil, modern, scope_tag("schematic"))
    g.layout_ok = True
    return g


def sequence_strips():
    names = [("whale", BLUE), ("hippo", GREEN), ("pig", GREY), ("cow", GREY), ("outgroup", GREY)]
    ys = [2.35, 1.25, 0.15, -0.95, -2.05]
    g = VGroup()
    for (name, col), y in zip(names, ys):
        lane = RoundedRectangle(corner_radius=0.12, width=11.9, height=0.94, stroke_opacity=0,
                                fill_color=col, fill_opacity=0.16).move_to([0, y, 0])
        lane.layout_ok = True
        lab = T(name, 28, col).move_to([-5.5, y, 0])
        line = Line([-4.45, y, 0], [5.65, y, 0], color=col, stroke_width=7)
        ticks = VGroup(*[Line([x, y - 0.12, 0], [x, y + 0.12, 0], color=BG, stroke_width=3)
                         for x in np.linspace(-4.0, 5.2, 14)])
        g.add(VGroup(lane, lab, line, ticks))
    g.layout_ok = True
    return g


# --------------------------------------------------------------------------------------

class S00Hook(SpokenScene):
    def construct(self):
        world = water_world()
        animate_world(world)
        self.at("A whale looks")
        self.play(FadeIn(world[0:4]), FadeIn(world[4], shift=RIGHT * 0.3), run_time=0.8)
        self.play(FadeIn(world[5], shift=RIGHT * 0.3), FadeIn(world[6], shift=LEFT * 0.2), run_time=0.8)
        self.at("So why does")
        shape_link = DashedLine(world[4].get_bottom(), world[5].get_top(), color=GREY, stroke_width=5)
        shape_lab = T("similar shape", 30, GREY).next_to(shape_link, LEFT, buff=0.18)
        q = T("?", 68, GOLD, weight=BOLD).move_to([1.35, 0.45, 0])
        pulse(q, base=1.5, amp=1.1, speed=2.2)
        self.play(Create(shape_link), FadeIn(shape_lab), FadeIn(q, scale=0.6), run_time=1.2)
        self.at("Shape offers")
        self.play(Indicate(shape_link, color=GREY, scale_factor=1.04), run_time=1.0)
        self.at("but ancestry")
        branch = VGroup(Line([0.55, -0.25, 0], [1.35, 0.45, 0], color=GOLD, stroke_width=5),
                        Line([1.35, 0.45, 0], [2.35, -0.35, 0], color=GOLD, stroke_width=5))
        self.play(ReplacementTransform(q, branch), run_time=1.1)
        self.at("Watch which features")
        dots = VGroup(*[Dot([-0.15 + i * 0.43, -0.83 + i * 0.11, 0], radius=0.09, color=TEAL) for i in range(6)])
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.14), run_time=1.4)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Building a Tree of Life"
    TITLE = "Which Similarities Reveal Relatives?"

    def construct(self):
        world = water_world(dim=True)
        animate_world(world)
        title = fit_text(self.TITLE, max_w=11.4, size=50, min_size=36, font=TITLE_FONT).move_to([0, 0.5, 0])
        lesson = T(self.LESSON.upper(), 24, GREY).next_to(title, UP, buff=0.35)
        rule = Line([-2.6, -0.25, 0], [2.6, -0.25, 0], color=GOLD, stroke_width=5)
        self.add(world)
        self.play(FadeIn(lesson), Write(title), GrowFromCenter(rule), run_time=0.9)
        branch = VGroup(Line([-2.6, -0.25, 0], [0, -0.25, 0], color=GOLD, stroke_width=5),
                        Line([0, -0.25, 0], [2.6, 0.15, 0], color=GOLD, stroke_width=5))
        self.play(FadeOut(lesson), FadeOut(title), ReplacementTransform(rule, branch), run_time=0.75)
        self.finish()


class S02SameJob(SpokenScene):
    def construct(self):
        world = water_world()
        animate_world(world)
        self.add(world)
        self.at("Whales and tuna")
        flow = VGroup(*[Arrow([-5.8, y, 0], [0.0, y, 0], buff=0, color=BLUE, stroke_width=2,
                                   tip_length=0.16) for y in (1.25, 0.65, -0.85, -1.45)])
        self.play(LaggedStart(*[GrowArrow(a) for a in flow], lag_ratio=0.12), run_time=1.4)
        self.at("A smooth body")
        outline = DashedVMobject(SurroundingRectangle(VGroup(world[4], world[5]), buff=0.18,
                                                         color=GREY, corner_radius=0.25), num_dashes=24)
        lab = T("swimming shape", 32, GREY).move_to([-0.15, -3.3, 0])
        self.play(Create(outline), FadeIn(lab), run_time=1.2)
        self.at("Similar conditions")
        card = chip("same job", GREY, size=32).move_to([1.15, 2.25, 0])
        self.play(ReplacementTransform(outline.copy(), card), FadeOut(flow), run_time=1.3)
        self.at("even in groups")
        self.play(card.animate.shift(RIGHT * 0.4), world[4].animate.shift(LEFT * 0.12),
                  world[5].animate.shift(RIGHT * 0.12), run_time=1.0)
        self.at("Scientists therefore")
        beam = AnnularSector(inner_radius=0.15, outer_radius=5.4, angle=0.22, start_angle=-0.11,
                             color=TEAL, fill_opacity=0.16, stroke_opacity=0).rotate(PI).move_to([5.6, 0.1, 0])
        self.play(FadeOut(lab), FadeIn(beam), run_time=1.1)
        self.play(Rotate(beam, angle=0.42, about_point=[5.6, 0.1, 0]), run_time=1.2)
        self.at("Which similarities")
        ask = T("inherited together?", 38, TEAL, weight=BOLD).move_to([-0.55, -2.55, 0])
        self.play(FadeOut(beam), FadeOut(card), FadeIn(ask, shift=UP * 0.15), run_time=1.1)
        self.finish()


class S03Predict(SpokenScene):
    def construct(self):
        trail = trail_picture()
        whale = animal("whale", BLUE, 0.48).move_to([-5.55, 1.15, 0])
        self.at("Suppose you could")
        self.play(Create(trail[0]), FadeIn(trail[1]), FadeIn(whale), run_time=1.0)
        self.at("Would you choose")
        self.play(Create(trail[2]), FadeIn(trail[4][0]), run_time=1.0)
        self.play(Create(trail[3]), FadeIn(trail[4][1]), run_time=1.0)
        self.play(FadeIn(trail[5:]), run_time=0.7)
        self.at("Hold your answer")
        dots = VGroup(Dot(trail[2].get_start(), color=GREY), Dot(trail[3].get_start(), color=TEAL))
        dots.layout_ok = True
        self.add(dots)
        self.play(MoveAlongPath(dots[0], trail[2]), MoveAlongPath(dots[1], trail[3]), run_time=1.8, rate_func=linear)
        self.at("The useful trail")
        q = question_card("Outside shape—or features passed through generations?", y=-3.15,
                          size=32, color=GOLD, max_w=11.0)
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.9)
        self.at("not just one")
        self.play(Indicate(VGroup(trail[5], trail[6]), color=GOLD, scale_factor=1.03), run_time=1.0)
        self.finish()


class S04Pause(PredictPause):
    QUESTION = "Outside shape—or features passed through generations?"
    SECONDS = 4.5
    CARD = {"y": -3.15, "size": 32, "color": GOLD, "max_w": 11.0}

    def backdrop(self):
        g = trail_picture()
        whale = animal("whale", BLUE, 0.48).move_to([-5.55, 1.15, 0])
        bob(whale, amp=0.08, speed=1.4)
        d1, d2 = Dot(g[2].get_start(), color=GREY), Dot(g[3].get_start(), color=TEAL)
        d1.add_updater(lambda m, dt: m.rotate(0.55 * dt, about_point=[0, 0, 0]))
        d2.add_updater(lambda m, dt: m.rotate(-0.42 * dt, about_point=[0, 0, 0]))
        return VGroup(g, whale, d1, d2)


class S05BodyParts(SpokenScene):
    def construct(self):
        pattern = limb_pattern().move_to([0, 0.35, 0])
        self.at("Start inside")
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in pattern], lag_ratio=0.16), run_time=1.5)
        self.at("A human hand")
        hand = limb_row("human hand", 1.65, (0.18, 7.8, 1.15))
        bat = limb_row("bat wing", 0.05, (0.45, 8.7, 1.2))
        flipper = limb_row("whale flipper", -1.55, (0.58, 7.9, 1.25))
        self.play(ReplacementTransform(pattern, hand[2]), FadeIn(hand[0:2]), run_time=1.0)
        self.play(TransformFromCopy(hand[2], bat[2]), FadeIn(bat[0:2]), run_time=0.9)
        self.play(TransformFromCopy(hand[2], flipper[2]), FadeIn(flipper[0:2]), run_time=0.9)
        rows = VGroup(hand, bat, flipper)
        rows.layout_ok = True
        self.at("Yet each keeps")
        self.play(LaggedStart(*[Indicate(r[2], color=TEAL, scale_factor=1.02) for r in rows], lag_ratio=0.18), run_time=1.5)
        self.at("Matching parts shift")
        self.play(hand[1].animate.stretch(0.91, 0), bat[1].animate.stretch(1.06, 0),
                  flipper[1].animate.stretch(0.94, 0), run_time=1.8)
        self.at("That pattern is")
        node = Dot([5.45, -2.65, 0], radius=0.16, color=GOLD)
        paths = VGroup(*[Line(node, r[1].get_right() + RIGHT * 0.02, color=GOLD, stroke_width=4) for r in rows])
        cap = T("homologous structure", 36, TEAL, weight=BOLD).move_to([0, 3.15, 0])
        self.play(Create(paths), FadeIn(node), FadeIn(cap), run_time=1.4)
        self.at("inherited from")
        self.play(Indicate(node, color=GOLD, scale_factor=1.7), run_time=1.1)
        self.finish()


class S06DevelopmentFossils(SpokenScene):
    def construct(self):
        early = embryo("early")
        tag = scope_tag("schematic")
        self.at("Development and fossils")
        self.play(FadeIn(early), FadeIn(tag), run_time=1.2)
        pulse(early, base=8.5, amp=2.2, speed=0.9)
        self.at("Vertebrate embryos")
        self.play(LaggedStart(*[Indicate(e[1:], color=TEAL, scale_factor=1.05) for e in early], lag_ratio=0.18), run_time=1.5)
        self.at("then follow different")
        late = embryo("late")
        self.play(Transform(early, late), run_time=1.5)
        self.at("Fossils place")
        timeline = fossil_timeline()
        flow = traveling_dots([[-5.5, -1.55, 0], [5.45, -1.55, 0]], GOLD, count=12, speed=0.075)
        self.play(FadeOut(early), FadeOut(tag), FadeIn(timeline[0:3], shift=UP * 0.15), run_time=1.2)
        self.play(FadeIn(timeline[3:]), FadeIn(flow), run_time=1.0)
        pulse(timeline[2], base=2.5, amp=1.5, speed=0.8)
        self.at("Whale embryos begin")
        bud = VGroup(Line([2.45, 0.0, 0], [2.1, -0.55, 0], color=TEAL, stroke_width=8),
                     Line([2.9, 0.0, 0], [3.25, -0.55, 0], color=TEAL, stroke_width=8))
        self.play(GrowFromCenter(bud), run_time=0.9)
        self.at("and fossil whales")
        self.play(Indicate(timeline[5], color=GOLD, scale_factor=1.05), FadeOut(bud), run_time=1.1)
        self.at("Neither clue")
        adult_shape = DashedVMobject(SurroundingRectangle(timeline[6], color=GREY, buff=0.14), num_dashes=18)
        x = VGroup(Line(adult_shape.get_corner(DL), adult_shape.get_corner(UR), color=GREY, stroke_width=4),
                   Line(adult_shape.get_corner(UL), adult_shape.get_corner(DR), color=GREY, stroke_width=4))
        self.play(Create(adult_shape), Create(x), run_time=1.0)
        self.play(FadeOut(adult_shape), FadeOut(x), Indicate(timeline[4], color=GOLD), run_time=0.9)
        self.finish()


class S07Dna(SpokenScene):
    def construct(self):
        strips = sequence_strips()
        self.at("DNA supplies")
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in strips], lag_ratio=0.1), run_time=1.4)
        strip_lines = VGroup(*[s[2] for s in strips])
        pulse(strip_lines, base=7.5, amp=4.0, speed=3.0)
        self.at("Scientists compare")
        scan = Line([-4.2, 2.75, 0], [-4.2, -2.45, 0], color=TEAL, stroke_width=5)
        self.play(FadeIn(scan), scan.animate.shift(RIGHT * 8.8), run_time=2.1, rate_func=linear)
        self.at("Shared insertions")
        blocks = VGroup()
        for y in (2.35, 1.25):
            for x in (-2.5, 0.4, 3.2):
                blocks.add(RoundedRectangle(corner_radius=0.06, width=0.42, height=0.48, color=TEAL,
                                            fill_color=TEAL, fill_opacity=0.85).move_to([x, y, 0]))
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.25) for b in blocks], lag_ratio=0.1), run_time=1.8)
        self.at("Several such clues")
        pair = SurroundingRectangle(VGroup(strips[0], strips[1]), color=GOLD, buff=0.16, corner_radius=0.15)
        self.play(Create(pair), run_time=1.0)
        tree = tree_picture()
        self.play(FadeOut(scan), FadeOut(pair), ReplacementTransform(VGroup(strips, blocks), tree), run_time=1.8)
        pulse(tree[0], base=9.0, amp=6.0, speed=3.0)
        self.at("When body")
        icons = VGroup(chip("body", TEAL, 26), chip("embryo", TEAL, 26), chip("fossil", TEAL, 26), chip("DNA", TEAL, 26))
        icons.arrange(RIGHT, buff=0.2).move_to([0.2, -2.65, 0])
        self.play(LaggedStart(*[FadeIn(i, shift=UP * 0.15) for i in icons], lag_ratio=0.18), run_time=1.4)
        self.at("the grouping becomes")
        ring = Circle(radius=0.46, color=TEAL, stroke_width=8).move_to([0.25, 0.35, 0])
        self.play(LaggedStart(*[i.animate.move_to(ring.get_center()).scale(0.15).set_opacity(0) for i in icons],
                              lag_ratio=0.12), Create(ring), run_time=1.5)
        self.finish()


class S08Rule(SpokenScene):
    def construct(self):
        tree = tree_picture()
        self.at("One clue can")
        self.play(Create(tree[0]), FadeIn(tree[1:]), run_time=1.5)
        pulse(tree[0], base=9.0, amp=6.0, speed=3.0)
        flow = traveling_dots([[3.25, 2.25, 0], [0.25, 0.35, 0], [-2.5, -0.65, 0], [-4.9, -2.15, 0]],
                              TEAL, count=11, speed=0.075)
        self.add(flow)
        self.at("so scientists compare")
        sources = [("body", [-5.3, 1.2, 0]), ("development", [-5.0, 0.35, 0]),
                   ("fossils", [-4.7, -0.5, 0]), ("DNA", [-4.3, -1.35, 0])]
        icons = VGroup(*[chip(name, TEAL, 25).move_to(pos) for name, pos in sources])
        self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in icons], lag_ratio=0.14), run_time=1.3)
        self.at("Body structures")
        node = tree[1][1]
        paths = VGroup(*[Arrow(i.get_right(), node.get_center(), buff=0.15, color=TEAL, stroke_width=3,
                                    tip_length=0.16) for i in icons])
        self.play(LaggedStart(*[GrowArrow(p) for p in paths], lag_ratio=0.15), run_time=2.0)
        self.at("When they agree")
        ring = Circle(radius=0.48, color=TEAL, stroke_width=8).move_to(node)
        self.play(Create(ring), FadeOut(icons), FadeOut(paths), run_time=1.2)
        self.at("The useful traits")
        tile = chip("derived trait", TEAL, 30).move_to([-1.05, -0.12, 0])
        tile.layout_ok = True  # the tile intentionally sits on the branch it marks
        self.play(FadeIn(tile, shift=UP * 0.15), run_time=1.0)
        self.at("A derived trait")
        definition = fit_text("first in one ancestor → passed to descendants", max_w=7.5, size=31,
                              min_size=28, color=TEAL).move_to([0.7, -2.65, 0])
        self.play(FadeIn(definition), Indicate(tree[1][1], color=GOLD, scale_factor=1.5), run_time=1.4)
        self.at("shared derived")
        tracer = Dot([3.25, 2.25, 0], radius=0.14, color=TEAL)
        path = VMobject().set_points_as_corners([[3.25, 2.25, 0], [0.25, 0.35, 0], [-2.5, -0.65, 0]])
        self.add(tracer)
        self.play(MoveAlongPath(tracer, path), run_time=2.0, rate_func=linear)
        rule = caption("Trace shared derived traits to branch points.", size=32, color=TEXT)
        self.play(FadeOut(definition), FadeIn(rule), run_time=1.0)
        self.finish()


def ambient(scene):
        halo = Circle(radius=0.3, color=GOLD, stroke_width=5).move_to([0.25, 0.35, 0])
        halo._t = 0.0

        def breathe(m, dt):
            m._t += dt
            k = (m._t * 0.8) % 1.0
            m.set_width(0.5 + 1.6 * k)
            m.move_to([0.25, 0.35, 0])
            m.set_stroke(opacity=0.9 * (1 - k))
        halo.add_updater(breathe)
        scene.add(halo)
        sweep = Line([-4.9, -2.15, 0], [0.25, 0.35, 0], color=GOLD, stroke_width=11)
        sweep._t = 0.0

        def glow(m, dt):
            m._t += dt
            k = (m._t * 0.35) % 1.0
            a = np.array([-4.9, -2.15, 0]); b = np.array([0.25, 0.35, 0])
            m.put_start_and_end_on(a + (b - a) * max(0, k - 0.18), a + (b - a) * k)
            m.set_stroke(opacity=0.8)
        sweep.add_updater(glow)
        scene.add(sweep)


class S09Answer(SpokenScene):
    def construct(self):
        world = water_world(dim=True)
        animate_world(world)
        self.add(world)
        self.at("Now the first")
        shape_link = DashedLine(world[4].get_bottom(), world[5].get_top(), color=GREY, stroke_width=5)
        lab = T("function", 30, GREY).next_to(shape_link, LEFT, buff=0.15)
        self.play(Create(shape_link), FadeIn(lab), run_time=1.0)
        self.at("The whale's swimming")
        self.play(Indicate(shape_link, color=GREY, scale_factor=1.03), run_time=1.0)
        self.at("Its lungs")
        land = VGroup(*[chip(x, TEAL, 26) for x in ("lungs", "limb bones", "embryos")]).arrange(RIGHT, buff=0.25)
        land.move_to([0, -2.55, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.12) for x in land], lag_ratio=0.18), run_time=1.4)
        self.at("Its milk")
        mammals = VGroup(*[chip(x, TEAL, 26) for x in ("milk", "fossils", "DNA")]).arrange(RIGHT, buff=0.25)
        mammals.move_to([0, -2.55, 0])
        self.play(FadeOut(land), LaggedStart(*[FadeIn(x, shift=UP * 0.12) for x in mammals], lag_ratio=0.18), run_time=1.4)
        self.at("Within living mammals")
        tree = tree_picture(water=True)
        self.play(FadeOut(VGroup(world, shape_link, lab, mammals)), FadeIn(tree), run_time=1.8)
        ambient(self)
        pulse(tree[0], base=9.0, amp=6.0, speed=3.0)
        flow = traveling_dots([[3.25, 2.25, 0], [0.25, 0.35, 0], [-2.5, -0.65, 0], [-4.9, -2.15, 0]],
                              TEAL, count=12, speed=0.085)
        self.add(flow)
        marks = VGroup(*[Dot([-1.4 + i * 0.42, -0.18 + i * 0.08, 0], radius=0.09, color=TEAL) for i in range(5)])
        self.play(LaggedStart(*[FadeIn(m, scale=0.3) for m in marks], lag_ratio=0.12), run_time=1.1)
        self.at("The tree records")
        rule = caption("Ancestry, not overall appearance", size=34, color=TEAL)
        self.play(FadeIn(rule), Indicate(tree[1][1], color=GOLD, scale_factor=1.5), run_time=1.2)
        self.finish()


class S10Return(SpokenScene):
    def construct(self):
        tree = tree_picture(water=True)
        self.add(tree)
        pulse(tree[0], base=9.0, amp=6.0, speed=3.0)
        flow = traveling_dots([[3.25, 2.25, 0], [0.25, 0.35, 0], [-2.5, -0.65, 0], [-4.9, -2.15, 0]],
                              TEAL, count=12, speed=0.085)
        self.add(flow)
        shape = chip("shape: same job", GREY, 28).move_to([-4.6, 3.3, 0])
        ambient(self)
        self.at("Looks still matter")
        self.play(FadeIn(shape), Indicate(tree[0][5:7], color=TEAL, scale_factor=1.02), run_time=1.2)
        self.at("They mislead")
        self.play(shape.animate.scale(0.78).set_opacity(0.55).shift(LEFT * 0.35), run_time=1.1)
        self.at("So begin with")
        steps = VGroup(chip("traits", TEAL, 27), chip("independent evidence", TEAL, 27),
                       chip("shared ancestor", GOLD, 27)).arrange(RIGHT, buff=0.3).move_to([0.65, -2.65, 0])
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in steps], lag_ratio=0.18), run_time=1.5)
        self.at("test them with")
        self.play(Indicate(steps[1], color=TEAL, scale_factor=1.06), run_time=1.0)
        self.at("and follow their")
        tracer = Dot([3.25, 2.25, 0], radius=0.15, color=TEAL)
        path = VMobject().set_points_as_corners([[3.25, 2.25, 0], [0.25, 0.35, 0]])
        self.add(tracer)
        self.play(MoveAlongPath(tracer, path), run_time=2.0, rate_func=linear)
        self.at("That turns")
        claim = caption("A resemblance becomes a testable claim.", size=34, color=TEXT)
        self.play(FadeOut(steps), FadeIn(claim), Indicate(tree[1][1], color=GOLD, scale_factor=1.6), run_time=1.2)
        self.finish()


class S11End(EndCard):
    LINE = "Trace shared derived traits to branch points to find the closest relatives."
