"""Phylogenetic inference, animated against the supplied narration.

COLOR MAP
  GREY   tree structure and the schematic scope
  BLUE   sampled tips and sequence data
  TEAL   shared ancestral character states
  GOLD   shared derived states, ancestor tracing and dates
  ORANGE independent gains and character-state pitfalls
  RED    miscalibration and incompatible placements
  GREEN  inference controls and node support
"""
from bp_parts import *


ORANGE = "#F29E4C"  # patch-clamp palette
BRANCH = interpolate_color(ManimColor(BG), ManimColor(GREY), 0.55)
DIM_BRANCH = interpolate_color(ManimColor(BG), ManimColor(GREY), 0.35)
DERIVED_BRANCH = interpolate_color(BRANCH, ManimColor(GOLD), 0.60)
QUESTION = "Closer to shark now?"
QUESTION_STYLE = dict(y=3.53, size=33)


def xy(x, y):
    return np.array([x, y, 0.0])


def heading(text, color=TEXT):
    return T(text, 32, color, weight=BOLD).move_to(xy(0, 3.52))


def note(text, color=TEXT, y=-3.36):
    return caption(text, 32, color, y=y)


def schematic():
    return scope_tag(size=28, color=TEXT)


def branch(a, b, color=BRANCH, width=0.68):
    """A broad ribbon along one topological edge, with a visible centre line."""
    normal = normalize(np.cross(b - a, OUT)) * width / 2
    ribbon = Polygon(a + normal, b + normal, b - normal, a - normal,
                     stroke_width=0, fill_color=color, fill_opacity=1)
    spine = Line(a, b, color=color, stroke_width=4)
    spine.set_color(interpolate_color(ManimColor(color), ManimColor(TEXT), 0.26))
    return VGroup(ribbon, spine)


def edge_color(edge, color):
    return edge[0].animate.set_fill(color)


def joint(position, color=GOLD, radius=0.18):
    return Circle(radius, color=color, stroke_width=4,
                  fill_color=BG, fill_opacity=1).move_to(position).set_z_index(2)


def path(*points):
    return VMobject().set_points_as_corners(points)


def signal(*points, color=GOLD, radius=0.18):
    """Send a visible marker down an existing branch, leaving geometry fixed."""
    bead = VGroup(Dot(radius=radius * 1.9, color=color, fill_opacity=0.24),
                  Dot(radius=radius, color=color)).move_to(points[0]).set_z_index(3)
    route = path(*points)
    glow = route.copy().set_stroke(color, width=44, opacity=0.86)
    travel = AnimationGroup(MoveAlongPath(bead, route, rate_func=linear),
                            ShowPassingFlash(glow, time_width=0.72, rate_func=linear))
    return bead, travel


def tick(a, b, fraction=0.5, color=GOLD, width=0.75):
    center = interpolate(a, b, fraction)
    offset = normalize(np.cross(b - a, OUT)) * width / 2
    return Line(center - offset, center + offset, stroke_width=8,
                color=color).set_z_index(1)


def fish(shark=False):
    if shark:
        outline = [(-1.22, 0.10), (-0.94, 0.32), (-0.46, 0.44), (-0.02, 0.45),
                   (0.30, 0.78), (0.39, 0.41), (0.89, 0.22), (1.12, 0.48),
                   (1.44, 0.68), (1.28, 0.16), (1.40, -0.25), (1.05, -0.04),
                   (0.88, 0.03), (0.10, -0.12), (0.39, -0.49),
                   (-0.09, -0.24), (-0.35, -0.07), (-0.93, -0.06)]
    else:
        outline = [(-1.23, 0.08), (-0.97, 0.34), (-0.48, 0.46), (-0.06, 0.49),
                   (0.21, 0.66), (0.50, 0.52), (0.48, 0.40), (0.89, 0.23),
                   (1.30, 0.46), (1.20, 0.07), (1.30, -0.23), (0.87, -0.07),
                   (0.42, -0.27), (0.28, -0.40), (0.00, -0.29), (-0.47, -0.28),
                   (-0.89, -0.16)]
    body = Polygon(*[xy(*p) for p in outline], stroke_width=0,
                   fill_color=BLUE, fill_opacity=1)
    details = VGroup(Dot(xy(-0.91, 0.13), radius=0.071, color=BG))
    if shark:
        for x in (-0.57, -0.43, -0.29):
            details.add(Line(xy(x, 0.27), xy(x + 0.05, 0.05), color=BG, stroke_width=3))
    else:
        for x, y in [(-0.55, 0.24), (-0.26, 0.33), (0.0, 0.18),
                     (0.29, 0.29), (0.57, 0.16), (-0.41, 0.04), (0.35, 0.04)]:
            details.add(Dot(xy(x, y), radius=0.045, color=BG))
    return VGroup(body, details)


def human():
    head = Circle(0.31, stroke_width=0, fill_color=BLUE, fill_opacity=1).shift(UP * 0.32)
    shoulders = RoundedRectangle(width=1.44, height=0.59, corner_radius=0.27,
                                 stroke_width=0, fill_color=BLUE, fill_opacity=1).shift(DOWN * 0.38)
    neck = Rectangle(width=0.29, height=0.39, stroke_width=0, fill_color=BLUE,
                     fill_opacity=1).shift(DOWN * 0.06)
    return VGroup(head, shoulders, neck)


ROOT = xy(-1.55, -2.72)
OLDER = xy(-0.88, -1.32)
RECENT = xy(2.2, 0.18)
OUTGROUP = xy(-5.13, -1.77)
TIPS = (xy(-4.59, 1.56), xy(0.37, 1.56), xy(4.2, 1.56))
SCALED_TIPS = (xy(-4.59, 0.98), xy(0.52, 1.86), xy(4.65, 1.21))
TIP_NAMES = ("Shark", "Trout", "Human")


def tip_label(name, icon):
    return place_label(T(name, 30, BLUE, weight=BOLD), icon, dirs=(UP,), buff=0.17)


def vertebrates(rotated=False, outgroup=True, dim=False, scaled=False, guess=False,
                show_names=True, highlighted=False):
    """The fixed vertebrate canvas. Styles change without moving ancestral junctions."""
    tips = SCALED_TIPS if scaled else TIPS
    shark, trout, person = (tips[0], tips[2], tips[1]) if not rotated else tips
    root = branch(ROOT, OLDER, width=0.91)
    split = branch(OLDER, RECENT, DERIVED_BRANCH if highlighted else BRANCH, width=0.87)
    shark_edge = branch(OLDER, shark, width=0.81)
    trout_edge = branch(RECENT, trout)
    human_edge = branch(RECENT, person)
    core = VGroup(root, split, shark_edge, trout_edge, human_edge)
    if guess:
        core = VGroup(*[DashedLine(a, b, color=GREY, stroke_width=7, dash_length=0.19)
                        for a, b in [(ROOT, OLDER), (OLDER, RECENT), (OLDER, shark),
                                     (RECENT, trout), (RECENT, person)]])
    out = branch(ROOT, OUTGROUP, DIM_BRANCH if dim else BRANCH, width=0.58)
    out_marker = Dot(OUTGROUP, radius=0.13, color=GREY if dim else BLUE)
    out_picture = VGroup(out, out_marker)
    out_name = T("Outgroup", 29, TEXT).move_to(xy(-5.17, -2.36))
    icons = VGroup(fish(True), fish(), human())
    for icon, end in zip(icons, (shark, trout, person)):
        icon.move_to(end + UP * 0.69)
    names = VGroup(*[tip_label(name, icon) for name, icon in zip(TIP_NAMES, icons)])
    picture = VGroup(core, icons)
    if outgroup:
        picture.add(out_picture)
        if show_names and not dim:
            picture.add(out_name)
    if show_names:
        picture.add(names)
    picture.core, picture.icons, picture.names = core, icons, names
    picture.out, picture.out_name = out_picture, out_name
    return picture


def ancestor_nodes(color=GOLD):
    return VGroup(joint(OLDER, color), joint(RECENT, color))


def predict_world():
    return VGroup(vertebrates(rotated=True, dim=True), ancestor_nodes(), schematic())


def question():
    return question_card(QUESTION, **QUESTION_STYLE)


def pivot(scene, tree, rotated, duration=3.1):
    """Project a half turn about the parent axis. Both children stay attached."""
    names = tree.names
    scene.play(FadeOut(names), run_time=0.30)
    start, end = (TIPS[2], TIPS[1]) if rotated else (TIPS[1], TIPS[2])
    pivot_point = (start + end) / 2
    horizontal = start - pivot_point
    pair = (tree.core[3], tree.core[4])
    icons = (tree.icons[1], tree.icons[2])
    turn = ValueTracker(0)

    def geometry(index):
        side = 1 if index == 0 else -1
        angle = turn.get_value() * PI
        return pivot_point + side * (horizontal * np.cos(angle) + UP * 0.68 * np.sin(angle))

    for i, (edge, icon) in enumerate(zip(pair, icons)):
        edge.add_updater(lambda m, i=i: m.become(branch(RECENT, geometry(i))))
        icon.add_updater(lambda m, i=i: m.move_to(geometry(i) + UP * 0.69))
    scene.play(turn.animate.set_value(1), run_time=duration, rate_func=smooth)
    for edge, icon in zip(pair, icons):
        edge.clear_updaters()
        icon.clear_updaters()
    final_names = VGroup(*[tip_label(name, icon) for name, icon in zip(TIP_NAMES, tree.icons)])
    scene.play(FadeIn(final_names), run_time=0.35)
    tree.names = final_names


def sequence(variants, center, size=0.23):
    """Fictional state strips, with no nucleotide or molecular drawing."""
    strips = VGroup()
    for row in variants:
        blocks = VGroup(*[RoundedRectangle(
            corner_radius=0.035, width=size, height=size * 1.1, stroke_width=0,
            fill_color=(BLUE, TEAL, TEXT, BRANCH)[code], fill_opacity=1) for code in row])
        blocks.arrange(RIGHT, buff=size * 0.19)
        strips.add(blocks)
    return strips.arrange(DOWN, buff=0.11).move_to(center)


ROWS = ((0, 1, 2, 3, 0, 2, 1, 3), (0, 1, 2, 0, 0, 2, 3, 3),
        (0, 1, 3, 0, 0, 2, 3, 1), (0, 2, 3, 0, 1, 2, 3, 1))


class S01Hook(SpokenScene, TitleCard):
    TITLE = "How Phylogenetic Trees Map Relatedness"
    LESSON = "Building and reading phylogenetic trees"

    def construct(self):
        tree = vertebrates(outgroup=False, guess=True, show_names=False)
        mark = T("?", 69, GOLD, weight=BOLD).move_to(xy(-1.7, 1.38))
        self.add(tree, schematic(), bob(mark, amp=0.12, speed=2))
        self.at("Is a trout")
        shimmer, move = signal(RECENT, TIPS[2], color=BLUE, radius=0.21)
        self.play(move, run_time=2.4)
        self.remove(shimmer)
        self.play(FadeIn(tree.names), run_time=0.48)
        self.at("Shark and trout")
        bracket = VGroup(*[BraceBetweenPoints(end + xy(-1.13, 0.15),
                                             end + xy(1.13, 0.15),
                                             direction=DOWN, color=BLUE)
                           for end in (TIPS[0], TIPS[2])])
        self.play(FadeOut(mark), GrowFromCenter(bracket), run_time=0.65)
        self.at("while you look")
        title = fit_text(self.TITLE, max_w=11.9, size=38, min_size=32,
                         font=TITLE_FONT).move_to(xy(0, 3.53))
        self.play(FadeOut(tree.names), run_time=0.32)
        self.play(FadeIn(title), run_time=0.55)
        self.at("Outward looks can")
        self.play(FadeOut(bracket), run_time=0.65)
        self.play(swap(title, tree.names, run_time=0.76))
        self.at("Phylogenetic trees test")
        resolved = vertebrates(outgroup=False)
        self.play(FadeOut(tree.core), FadeIn(resolved.core), run_time=1.8)
        light, move = signal(ROOT, OLDER, RECENT, color=BLUE)
        self.play(move, run_time=2.75)
        self.remove(light)
        self.finish()


class S02Outgroup(SpokenScene):
    def construct(self):
        tree = vertebrates(outgroup=False)
        self.add(tree, schematic())
        traits = VGroup(*[RoundedRectangle(width=0.3, height=0.3, corner_radius=0.07,
                                          color=TEAL, fill_color=TEAL, fill_opacity=0.55)
                          .move_to(xy(x, -0.30)) for x in (-5.45, -4.95, -4.45)])
        seq = sequence(ROWS[:2], xy(-4.95, -0.95), 0.25)
        self.at("compare characters")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.33) for t in traits],
                              lag_ratio=0.27), run_time=1.1)
        self.at("gene sequences across")
        self.play(FadeIn(seq, shift=RIGHT * 0.55), run_time=1.42)
        self.at("First add")
        self.play(FadeOut(traits), FadeOut(seq), run_time=0.38)
        self.play(GrowFromPoint(tree.out, ROOT), run_time=0.72)
        self.play(FadeIn(tree.out_name), run_time=0.45)
        self.at("branched off earlier")
        root_node = joint(ROOT, TEAL)
        self.play(GrowFromCenter(root_node), run_time=0.55)
        bead, move = signal(ROOT, OUTGROUP, color=BLUE)
        self.play(move, run_time=1.48)
        self.remove(bead)
        self.at("Character states matching")
        traces = [signal(*p, color=TEAL, radius=0.20) for p in (
            (ROOT, OUTGROUP), (ROOT, OLDER, TIPS[0]), (ROOT, OLDER, RECENT, TIPS[1]),
            (ROOT, OLDER, RECENT, TIPS[2]))]
        ancient = note("Shared ancestral state", TEAL)
        self.play(*[m for _, m in traces], FadeIn(ancient), run_time=2.95)
        ends = VGroup(*[d for d, _ in traces])
        self.at("Old states cannot")
        inherited = interpolate_color(ManimColor(BRANCH), ManimColor(TEAL), 0.71)
        edges = [*tree.core, tree.out[0]]
        self.play(*[FadeOut(d, scale=1.8) for d in ends], FadeOut(root_node),
                  *[edge_color(e, inherited) for e in edges], run_time=1.13)
        self.play(FadeOut(ancient), *[edge_color(e, BRANCH) for e in edges], run_time=0.92)
        self.at("a new shared")
        derived = tick(OLDER, RECENT)
        self.play(GrowFromCenter(derived), edge_color(tree.core[1], DERIVED_BRANCH), run_time=0.55)
        label = note("Shared derived", GOLD)
        self.play(FadeIn(label), run_time=0.38)
        traces = [signal(interpolate(OLDER, RECENT, 0.5), RECENT, t, radius=0.21) for t in TIPS[1:]]
        self.play(*[m for _, m in traces], run_time=1.75)
        self.play(*[FadeOut(d) for d, _ in traces], FadeOut(label), run_time=0.34)
        self.finish()


class S03Reading(SpokenScene):
    def construct(self):
        tree = vertebrates(dim=True, highlighted=True)
        derived = tick(OLDER, RECENT)
        older, recent = ancestor_nodes()
        self.add(tree, derived, schematic())
        self.at("Every branching point")
        self.play(GrowFromCenter(older), GrowFromCenter(recent),
                  edge_color(tree.core[1], BRANCH), run_time=1.15)
        self.at("marks a common ancestor")
        root_ring = joint(ROOT, GOLD, 0.15)
        self.play(GrowFromCenter(root_ring), run_time=0.65)
        self.at("Characters change along")
        left = tick(OLDER, TIPS[0], 0.45, ORANGE)
        right = tick(RECENT, TIPS[2], 0.48, TEAL)
        for marker, edge, start, end, color in (
                (left, tree.core[2], OLDER, TIPS[0], ORANGE),
                (right, tree.core[3], RECENT, TIPS[2], TEAL)):
            bead, drift = signal(start, interpolate(start, end, 0.57), color=color)
            accent = interpolate_color(ManimColor(BRANCH), ManimColor(color), 0.78)
            self.play(drift, edge_color(edge, accent), run_time=1.13)
            self.remove(bead)
            self.add(marker)
        self.at("Trout is closer")
        self.play(FadeOut(left), FadeOut(right), FadeOut(root_ring),
                  *[edge_color(tree.core[i], BRANCH) for i in (2, 3)], run_time=0.48)
        old_label = T("Older ancestor", 32, GOLD).move_to(xy(1.15, -2.05))
        self.play(FadeIn(old_label), edge_color(tree.core[0], GOLD), run_time=0.6)
        self.at("The ancestor trout shares")
        bead, move = signal(OLDER, RECENT, radius=0.22)
        self.play(move, run_time=1.75)
        self.remove(bead)
        new_label = T("More recent ancestor", 32, GOLD).move_to(xy(4.20, -1.15))
        self.play(FadeIn(new_label), edge_color(tree.core[3], GOLD),
                  edge_color(tree.core[4], GOLD), run_time=0.67)
        self.at("It descends from")
        bead, move = signal(OLDER, RECENT, radius=0.22)
        self.play(move, run_time=1.9)
        self.remove(bead)
        self.play(FadeOut(old_label), FadeOut(new_label), FadeOut(derived),
                  *[edge_color(tree.core[i], BRANCH) for i in (0, 3, 4)],
                  run_time=0.71)
        self.finish()


class S04PredictQ(SpokenScene):
    def construct(self):
        tree = vertebrates(dim=True)
        self.add(tree, ancestor_nodes(), schematic())
        self.at("watch the tree")
        arc = Arc(radius=0.44, start_angle=0.40, angle=-1.24 * PI,
                  arc_center=RECENT, color=GOLD, stroke_width=5).add_tip(tip_length=0.18)
        self.play(Create(arc), run_time=1.25)
        self.at("Suppose we spin")
        pivot(self, tree, rotated=True, duration=3.45)
        self.play(FadeOut(arc), run_time=0.38)
        self.at("Does spinning that node")
        self.play(FadeIn(question()), run_time=0.55)
        brighter = interpolate_color(ManimColor(BRANCH), ManimColor(BLUE), 0.65)
        self.play(*[edge_color(e, brighter) for e in tree.core[2:]],
                  rate_func=there_and_back, run_time=3.0)
        self.finish()


class S05PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        world = predict_world()
        tree, nodes, _ = world
        self.add(world, question())
        # Keep the written question fixed while the whole schematic gently breathes.
        base = ManimColor(BRANCH)
        lifted = ManimColor(BLUE)
        clock = [0.0]

        def breathe(_, dt):
            clock[0] += dt
            phase = TAU * clock[0] / 5
            tint = interpolate_color(base, lifted, 0.29 * (1 - np.cos(phase)))
            for edge in tree.core:
                edge[0].set_fill(tint)
            for index, node in enumerate(nodes):
                node.set_stroke(width=4 + 2.3 * max(0, np.sin(phase - index * PI)))
            for i, icon in enumerate(tree.icons):
                end = TIPS[i]
                icon.move_to(end + UP * (0.69 + 0.055 * np.sin(phase) * (1 if i != 1 else -1)))

        tree.add_updater(breathe)
        self.wait(5)
        tree.remove_updater(breathe)


def sequence_ticks():
    """Marks at equal distance intervals along each edge of the schematic phylogram."""
    edges = [(ROOT, OLDER), (OLDER, RECENT), (OLDER, SCALED_TIPS[0]),
             (RECENT, SCALED_TIPS[1]), (RECENT, SCALED_TIPS[2])]
    return VGroup(*[tick(a, b, d / np.linalg.norm(b - a), BLUE, 0.80)
                    for a, b in edges for d in np.arange(0.58, np.linalg.norm(b - a) - 0.18, 0.58)])


def clock_mark():
    circle = Circle(0.52, color=RED, stroke_width=5)
    hands = path(xy(0, 0.26), ORIGIN, xy(0.23, -0.11)).set_stroke(RED, 5)
    slash = Line(xy(-0.43, -0.43), xy(0.43, 0.43), color=RED, stroke_width=6)
    return VGroup(circle, hands, slash).move_to(xy(-4.94, -0.21))


class S06Reveal(SpokenScene):
    def construct(self):
        world = predict_world()
        tree, nodes, tag = world
        q = question()
        self.add(tree, nodes, tag, q)
        self.at("Now")
        no = heading("No", GOLD).shift(LEFT * 1.62)
        self.play(swap(q, no, run_time=0.64))
        bead, move = signal(OLDER, RECENT)
        self.play(move, run_time=1.0)
        self.remove(bead)
        self.at("rotating a node")
        pivot(self, tree, rotated=False, duration=2.76)
        self.play(FadeOut(no), run_time=0.35)
        self.at("shared ancestor is more recent")
        bead, move = signal(OLDER, RECENT)
        self.play(move, edge_color(tree.core[1], GOLD), run_time=1.65)
        self.remove(bead)
        self.at("Neither tip order")
        twigs = VGroup()
        origins = [interpolate(RECENT, TIPS[1], f) for f in (0.34, 0.69)]
        for p, endpoint in zip(origins, (xy(1.56, 1.97), xy(-0.87, 1.17))):
            twig = branch(p, endpoint, width=0.34)
            twigs.add(VGroup(twig, joint(p, GREY, 0.11)))
        self.play(LaggedStart(*[GrowFromPoint(g, p) for g, p in zip(twigs, origins)],
                              lag_ratio=0.51),
                  edge_color(tree.core[1], BRANCH), run_time=1.5)
        self.at("nodes between tips")
        bead, move = signal(TIPS[2], RECENT, TIPS[1])
        self.play(move, run_time=2.25)
        self.remove(bead)
        self.play(FadeOut(twigs), run_time=0.48)
        self.at("Relatedness lives at")
        self.play(Indicate(nodes[1], color=GOLD, scale_factor=1.57),
                  edge_color(tree.core[3], GOLD), edge_color(tree.core[4], GOLD),
                  run_time=1.38)
        self.at("Change lives on")
        bead, move = signal(OLDER, TIPS[0], color=BLUE)
        self.play(move, edge_color(tree.core[3], BRANCH),
                  edge_color(tree.core[4], BRANCH), run_time=1.38)
        self.remove(bead)
        self.at("scaled molecular trees")
        scaled = vertebrates(dim=True, scaled=True)
        self.play(FadeOut(tree.names), run_time=0.27)
        self.play(Transform(tree.core, scaled.core), Transform(tree.icons, scaled.icons),
                  run_time=1.37)
        self.play(FadeIn(scaled.names), run_time=0.32)
        self.at("branch lengths show")
        self.play(LaggedStart(*[GrowFromCenter(t) for t in sequence_ticks()],
                              lag_ratio=0.10), run_time=1.5)
        change = note("Estimated sequence change", BLUE)
        self.play(FadeIn(change), run_time=0.42)
        self.at("not years")
        clock = clock_mark()
        clock_label = T("Not years", 28, RED).next_to(clock, DOWN, buff=0.15)
        self.play(FadeIn(clock), FadeIn(clock_label), run_time=0.55)
        self.finish()


def extra_outgroups():
    return VGroup(*[
        VGroup(branch(ROOT, p, DIM_BRANCH, width=0.34), Dot(p, radius=0.13, color=GREEN))
        for p in (xy(-5.62, -0.97), xy(-5.21, -2.71))
    ])


def gene_tree_overlay():
    """An alternate gene tree grouped by the same three sampled tips."""
    diverge = xy(-1.45, -0.88)
    closest = xy(-0.72, 0.48)
    endpoints = [(ROOT, diverge), (diverge, closest), (closest, TIPS[0]),
                 (closest, TIPS[2]), (diverge, TIPS[1])]
    return VGroup(*[DashedLine(a, b, color=RED, stroke_width=5, dash_length=0.15)
                    for a, b in endpoints])


class S07ControlsBuild(SpokenScene):
    def construct(self):
        tree = vertebrates(dim=True, scaled=True)
        marks = sequence_ticks()
        nodes = ancestor_nodes()
        self.add(tree, nodes, marks, schematic())
        self.at("Trees are hypotheses")
        regular = vertebrates(dim=True)
        self.play(FadeOut(tree.names), FadeOut(marks), run_time=0.4)
        self.play(Transform(tree.core, regular.core), Transform(tree.icons, regular.icons),
                  run_time=1.3)
        self.play(FadeIn(regular.names), run_time=0.36)
        self.at("Two lineages can gain")
        a = tick(OLDER, TIPS[0], 0.48, ORANGE)
        b = tick(RECENT, TIPS[2], 0.56, ORANGE)
        for patch, start, end in ((a, OLDER, TIPS[0]), (b, RECENT, TIPS[2])):
            bead, move = signal(start, interpolate(start, end, 0.68), color=ORANGE)
            self.play(move, run_time=1.05)
            self.remove(bead)
            self.play(GrowFromCenter(patch), run_time=0.27)
        self.at("called convergence")
        converges = note("Convergence", ORANGE)
        self.play(FadeIn(converges), run_time=0.45)
        self.at("An outgroup can change")
        self.play(FadeOut(a), FadeOut(b), FadeOut(converges), run_time=0.35)
        out_tick = tick(ROOT, OUTGROUP, 0.53, ORANGE)
        self.play(edge_color(tree.out[0], ORANGE), GrowFromCenter(out_tick), run_time=1.05)
        self.at("One gene's tree")
        overlay = gene_tree_overlay()
        gene_note = note("One gene’s tree", RED)
        self.play(FadeOut(out_tick), tree.out[0][0].animate.set_fill(DIM_BRANCH), run_time=0.32)
        self.play(LaggedStart(*[Create(e) for e in overlay], lag_ratio=0.2),
                  *[edge_color(e, DIM_BRANCH) for e in tree.core], run_time=1.42)
        self.play(FadeIn(gene_note), run_time=0.44)
        self.at("So studies compare")
        extra = extra_outgroups()
        self.play(FadeOut(overlay), FadeOut(gene_note),
                  *[edge_color(e, BRANCH) for e in tree.core], run_time=0.48)
        self.play(LaggedStart(*[GrowFromPoint(g, ROOT) for g in extra], lag_ratio=0.46),
                  run_time=1.38)
        self.at("use many genes")
        seq = sequence(ROWS, xy(4.0, -1.6), size=0.22)
        self.play(FadeIn(seq, shift=RIGHT * 0.58), run_time=0.69)
        self.play(FadeOut(seq, shift=xy(-1.5, 0.9), scale=0.28), run_time=0.96)
        self.at("how firmly the data")
        support = VGroup(*[joint(p, GREEN, 0.29) for p in (ROOT, OLDER, RECENT)])
        support_note = note("Node support", GREEN)
        self.play(LaggedStart(*[GrowFromCenter(r) for r in support], lag_ratio=0.35),
                  run_time=0.97)
        self.play(FadeIn(support_note), run_time=0.36)
        self.finish()


def fossil_pin(color=GOLD):
    pin = VGroup(Line(ORIGIN, UP * 0.36, color=color, stroke_width=5),
                 RoundedRectangle(width=0.63, height=0.62, corner_radius=0.12,
                                  fill_color=color, fill_opacity=1, stroke_width=0)
                 .move_to(UP * 0.64))
    shell = Arc(radius=0.17, start_angle=0.02, angle=1.66 * PI,
                arc_center=UP * 0.64, color=BG, stroke_width=4)
    inner = Arc(radius=0.085, start_angle=-0.7, angle=1.4 * PI,
                arc_center=UP * 0.64, color=BG, stroke_width=3)
    return pin.add(shell, inner).set_z_index(3)


def time_ruler(spacing):
    ys = [-2.58, -2.58 + 1.38 * spacing, 0.16 + 0.62 * (spacing - 1), 1.56]
    x = -6.12
    axis = Arrow(xy(x, -2.74), xy(x, 2.07), buff=0, stroke_width=4,
                 color=GOLD, tip_length=0.17)
    ticks = VGroup(*[Line(xy(x, y), xy(x + 0.31, y), color=GOLD, stroke_width=5) for y in ys])
    return VGroup(axis, ticks)


def compact_tree_geometry():
    """Rebuild the same topology at the left of the two-variable plot."""
    def p(point):
        return point * np.array([0.46, 0.78, 1.0]) + xy(-3.38, -0.25)

    core = VGroup(*[branch(p(a), p(b), width=w) for a, b, w in [
        (ROOT, OLDER, 0.75), (OLDER, TIPS[0], 0.59), (OLDER, RECENT, 0.70),
        (RECENT, TIPS[1], 0.56), (RECENT, TIPS[2], 0.56),
    ]])
    icons = VGroup(fish(True), human(), fish())
    for icon, tip in zip(icons, TIPS):
        icon.scale(0.57).move_to(p(tip) + UP * 0.45)
    nodes = VGroup(*[joint(p(n), GOLD, 0.13) for n in (OLDER, RECENT)])
    return VGroup(core, icons, nodes), p


def trait_plot():
    """Compute ordinary and phylogenetic GLS fits from schematic tip data."""
    groups = (
        np.array([(0.8, 1.0), (1.2, 1.3), (1.55, 1.05), (1.96, 1.34)]),
        np.array([(3.02, 3.1), (3.46, 3.30), (3.85, 3.22), (4.23, 3.48)]),
        np.array([(4.96, 5.0), (5.33, 5.18), (5.79, 5.10), (6.14, 5.37)]),
    )
    plot = Plot(box=(0.12, 6.12, -2.10, 2.20), xr=(0, 7), yr=(0, 6.1),
                xlabel="Trait A", ylabel="Trait B", label_size=29, color=TEXT)
    colors = (BLUE, TEAL, GOLD)
    dots = VGroup(*[VGroup(*[Dot(plot.pt(x, y), radius=0.115, color=c) for x, y in g])
                    for g, c in zip(groups, colors)])
    all_points = np.concatenate(groups)
    slope, intercept = np.polyfit(*all_points.T, 1)
    clade = np.repeat(np.arange(len(groups)), [len(group) for group in groups])
    recent_lineage = clade > 0
    # Under Brownian motion, shared path length sets the covariance between tips.
    covariance = (0.12 + 0.21 * np.outer(recent_lineage, recent_lineage)
                  + 0.66 * (clade[:, None] == clade) + 0.025 * np.eye(len(clade)))
    lower = np.linalg.cholesky(covariance)
    design = np.column_stack([np.ones(len(all_points)), all_points[:, 0]])
    adjusted_intercept, adjusted_slope = np.linalg.lstsq(
        np.linalg.solve(lower, design), np.linalg.solve(lower, all_points[:, 1]), rcond=None)[0]
    raw = plot.curve(lambda x: intercept + slope * x, color=GREY, width=5,
                     x0=0.4, x1=6.5)
    adjusted_line = plot.curve(lambda x: adjusted_intercept + adjusted_slope * x,
                               color=GREEN, width=8, x0=0.4, x1=6.5)
    return plot, dots, raw, adjusted_line, groups


class S08ControlsUse(SpokenScene):
    def construct(self):
        tree = vertebrates(dim=True)
        nodes = ancestor_nodes()
        extra = extra_outgroups()
        support = VGroup(*[joint(p, GREEN, 0.29) for p in (ROOT, OLDER, RECENT)])
        tag = schematic()
        self.add(tree, nodes, extra, support, tag)
        self.at("Using trees carries limits")
        self.play(FadeOut(extra), FadeOut(support), run_time=1.07)
        self.at("Turning sequence")
        scaled = vertebrates(dim=True, scaled=True)
        self.play(FadeOut(tree.names), run_time=0.28)
        self.play(Transform(tree.core, scaled.core), Transform(tree.icons, scaled.icons),
                  run_time=1.35)
        self.play(FadeIn(scaled.names), run_time=0.36)
        self.at("needs fossils anchored")
        pin = fossil_pin().shift(OLDER)
        ruler = time_ruler(1)
        time_label = T("Time", 29, GOLD).move_to(xy(-5.51, 0.18)).rotate(PI / 2)
        calibrated = vertebrates(dim=True)
        self.play(FadeIn(pin, shift=DOWN * 0.65), FadeOut(scaled.names), run_time=0.73)
        self.play(Transform(tree.core, calibrated.core), Transform(tree.icons, calibrated.icons),
                  Create(ruler), FadeIn(time_label), run_time=0.98)
        self.play(FadeIn(calibrated.names), run_time=0.38)
        self.at("2012 Parham and colleagues")
        reference = note("Parham and colleagues, 2012", GOLD)
        self.play(FadeIn(reference), run_time=0.5)
        self.at("a misplaced or")
        offset = xy(0.7, 0.65)
        self.play(Transform(pin, fossil_pin(ORANGE).shift(OLDER + offset)), run_time=0.83)
        self.at("fossil carries error")
        warped = time_ruler(1.52)
        warped[1].set_color(RED)
        self.play(Transform(ruler, warped), run_time=1.10)
        self.play(FadeOut(reference), run_time=0.32)
        self.play(Transform(pin, fossil_pin().shift(OLDER)),
                  Transform(ruler, time_ruler(1)), run_time=1.04)
        self.at("Related species are")
        compact, point = compact_tree_geometry()
        self.play(FadeOut(ruler), FadeOut(time_label), FadeOut(pin),
                  FadeOut(calibrated.names), FadeOut(tree.out), run_time=0.43)
        self.play(ReplacementTransform(tree.core, compact[0]),
                  ReplacementTransform(tree.icons, compact[1]),
                  ReplacementTransform(nodes, compact[2]), run_time=0.74)
        plot, dots, raw, adjusted, groups = trait_plot()
        self.play(FadeIn(plot), run_time=0.52)
        endpoints = [point(tip) for tip in TIPS]
        centers = [plot.pt(*group.mean(axis=0)) for group in groups]
        # Curve the Shark link below the shared junction.
        shark_route = ArcBetweenPoints(endpoints[0], centers[0], angle=36 * DEGREES,
                                       color=BLUE, stroke_width=2.5)
        shark_link = DashedVMobject(shark_route, num_dashes=29, dashed_ratio=0.62)
        links = VGroup(shark_link, *[DashedLine(a, b, color=color,
                                    stroke_width=2.5, dash_length=0.15)
                         for a, b, color in zip(endpoints[1:], centers[1:], (TEAL, GOLD))])
        self.play(LaggedStart(*[FadeIn(g) for g in dots], lag_ratio=0.4),
                  LaggedStart(*[Create(link) for link in links], lag_ratio=0.4),
                  run_time=0.72)
        self.at("phylogenetic regression")
        self.play(FadeOut(links), Create(raw), run_time=0.82)
        self.at("accounts for shared ancestry")
        self.play(Transform(raw, adjusted), run_time=1.42)
        self.play(FadeIn(note("Phylogenetic regression", GREEN)), run_time=0.50)
        self.finish()


DEEP_ROOT = xy(0, -2.69)
ARCHAEA = xy(1.91, -0.38)
ASGARD = xy(3.25, 0.95)
DOMAIN_TIPS = (xy(-4.6, 2.26), xy(0, 2.26), xy(4.52, 2.26))


def named_tip(text, p, color=BLUE, size=30, radius=0.18):
    marker = Dot(p, radius=radius, color=color)
    label = place_label(T(text, size, color, weight=BOLD), marker, dirs=(UP,), buff=0.21)
    return VGroup(marker, label)


def domain_edges(modern=False):
    b, a, e = DOMAIN_TIPS
    if modern:
        return VGroup(branch(DEEP_ROOT, b, width=0.85), branch(DEEP_ROOT, ARCHAEA, width=0.89),
                      branch(ARCHAEA, a, width=0.68), branch(ARCHAEA, ASGARD, width=0.68),
                      branch(ASGARD, e, width=0.65),
                      branch(ASGARD, xy(2.32, 1.89), width=0.55))
    return VGroup(*[branch(DEEP_ROOT, p, width=0.79) for p in DOMAIN_TIPS])


def deep_tree():
    domain = domain_edges(modern=True)
    return VGroup(domain, joint(DEEP_ROOT), joint(ARCHAEA), joint(ASGARD))


def domain_names():
    return VGroup(*[named_tip(name, p) for name, p in
                    zip(("Bacteria", "Archaea", "Eukarya"), DOMAIN_TIPS)])


def asgard_tip():
    return VGroup(Dot(xy(2.32, 1.89), radius=0.18, color=BLUE),
                  T("Asgard archaea", 30, BLUE, weight=BOLD).move_to(xy(2.0, 3.23)))


def debated_branch():
    return DashedVMobject(Arc(radius=0.53, start_angle=-1.02, angle=4.8,
                              arc_center=ASGARD, color=ORANGE, stroke_width=4), num_dashes=8)


def early_tree():
    base, split = xy(0, -2.73), xy(0, 0.12)
    return VGroup(branch(base, split, width=0.97),
                  *[branch(split, xy(x, y), width=0.56) for x, y in
                    [(-4.4, 2.06), (-2.1, 2.43), (2.65, 2.28), (4.5, 1.88)]])


class S09UnlockedDomains(SpokenScene):
    def construct(self):
        compact, _ = compact_tree_geometry()
        trunk = early_tree()
        plot, dots, _, adjusted, _ = trait_plot()
        regression = note("Phylogenetic regression", GREEN)
        self.add(compact, plot, dots, adjusted, regression, schematic())
        self.at("With those guards")
        self.play(FadeOut(plot), FadeOut(dots), FadeOut(adjusted), FadeOut(regression),
                  FadeOut(compact[1]), FadeOut(compact[2]), run_time=0.54)
        self.play(ReplacementTransform(compact[0], trunk), run_time=1.58)
        self.at("1977")
        yr = T("1977", 38, GOLD, weight=BOLD).move_to(xy(-4.70, -2.69))
        self.play(FadeIn(yr), run_time=0.42)
        fragments = sequence((ROWS[0][1:6], ROWS[1][1:6], ROWS[2][1:6]),
                             xy(2.52, -1.35), 0.46)
        fragments[0].shift(LEFT * 0.45)
        fragments[2].shift(RIGHT * 0.53)
        self.at("compared short RNA pieces")
        self.play(FadeIn(fragments, shift=RIGHT * 0.36), run_time=0.62)
        self.play(fragments[0].animate.shift(RIGHT * 0.45),
                  fragments[2].animate.shift(LEFT * 0.53), run_time=1.38)
        self.at("1990")
        next_year = T("1990", 38, GOLD, weight=BOLD).move_to(yr)
        self.play(swap(yr, next_year), FadeOut(fragments, shift=LEFT * 1.12), run_time=0.75)
        self.at("proposed three domains")
        old = domain_edges()
        self.play(ReplacementTransform(trunk, old), run_time=1.70)
        labels = domain_names()
        self.at("bacteria archaea")
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.08) for l in labels],
                              lag_ratio=0.50), run_time=1.55)
        self.at("Many gene trees")
        main, root_ring, arch_ring, asgard_ring = deep_tree()
        self.play(FadeOut(next_year), run_time=0.34)
        self.play(ReplacementTransform(old, main), GrowFromCenter(root_ring),
                  GrowFromCenter(arch_ring), run_time=2.37)
        self.at("closest to a group")
        asgard = asgard_tip()
        self.play(GrowFromCenter(asgard_ring), run_time=0.50)
        self.play(FadeIn(asgard), run_time=0.52)
        self.at("though the branch")
        self.play(Create(debated_branch()), FadeIn(note("Exact branch debated", ORANGE)),
                  run_time=0.78)
        self.finish()


def animal_ladder():
    steps = [xy(-6.05, -2.35), xy(-4.28, -2.35), xy(-4.28, -1.00), xy(-0.75, -1.00),
             xy(-0.75, 0.32), xy(3.09, 0.32), xy(3.09, 1.74), xy(5.83, 1.74)]
    return VGroup(*[branch(a, b, width=0.70) for a, b in zip(steps[:-1], steps[1:])])


ANIMAL_ROOT = xy(-1.05, -2.52)
MOULT = xy(1.91, -0.79)
ANIMAL_TIPS = tuple(xy(x, 1.8) for x in (-4.85, -1.64, 1.69, 4.76))


def animal_icon(kind):
    if kind == "arthropod":
        body = VGroup(*[Ellipse(width=w, height=h, color=BLUE, fill_opacity=1, stroke_width=0)
                        .move_to(xy(0, y)) for w, h, y in [(0.33, 0.30, 0.30),
                                                           (0.46, 0.36, 0.025),
                                                           (0.62, 0.51, -0.35)]])
        legs = VGroup(*[path(xy(0, y), xy(s * 0.39, y + dy), xy(s * 0.67, y + dy - 0.12))
                        .set_stroke(BLUE, 5) for s in (-1, 1)
                        for y, dy in [(0.12, 0.24), (-0.03, 0.04), (-0.16, -0.14)]])
        return VGroup(body, legs)
    snake = VMobject()
    snake.set_points_smoothly([xy(-0.70, -0.15), xy(-0.39, 0.24), xy(0.03, 0.16),
                               xy(0.34, -0.18), xy(0.69, 0.14)])
    snake.set_stroke(BLUE, 11 if kind == "annelid" else 6)
    if kind == "annelid":
        rings = VGroup(*[Dot(snake.point_from_proportion(u), color=BG, radius=0.031)
                         for u in np.arange(0.10, 0.98, 0.11)])
        return VGroup(snake, rings)
    return snake


def animal_tips():
    icons = VGroup(*[animal_icon(kind).move_to(p + UP * 0.50)
                    for kind, p in zip(("annelid", "nematode", "arthropod"), ANIMAL_TIPS)])
    labels = VGroup(*[tip_label(name, icon) for name, icon in
                      zip(("Annelids", "Nematodes", "Arthropods"), icons)])
    other = named_tip("Other moulting\nanimals", ANIMAL_TIPS[3], size=28)
    return icons, labels, other


def animal_tree(moulting=True, highlighted=False):
    annelid, nematode, arthropod, others = ANIMAL_TIPS
    stem = branch(ANIMAL_ROOT, MOULT, GOLD if highlighted else BRANCH, width=0.99)
    nem_end = MOULT if moulting else xy(-3.22, -0.66)
    left_end = ANIMAL_ROOT if moulting else nem_end
    left = branch(left_end, annelid, width=0.75)
    return VGroup(stem, left, branch(nem_end, nematode, width=0.73),
                  branch(MOULT, arthropod, width=0.71), branch(MOULT, others, width=0.71),
                  branch(ANIMAL_ROOT, nem_end, width=0.73) if not moulting else
                  joint(ANIMAL_ROOT))


class S10UnlockedAnimals(SpokenScene):
    def construct(self):
        deep = deep_tree()
        tag = schematic()
        labels = VGroup(domain_names(), asgard_tip())
        caution = VGroup(debated_branch(), note("Exact branch debated", ORANGE))
        self.add(deep, labels, caution, tag)
        self.at("Gene trees broke")
        ladder = animal_ladder()
        icons = VGroup(*[animal_icon(kind).move_to(xy(x, y)) for kind, (x, y) in zip(
            ("annelid", "nematode", "arthropod"), [(-5.21, -1.82), (-2.49, -0.43), (4.65, 2.31)])])
        self.play(FadeOut(labels), FadeOut(caution), run_time=0.38)
        self.play(ReplacementTransform(deep, ladder), run_time=1.28)
        self.play(LaggedStart(*[FadeIn(icon) for icon in icons], lag_ratio=0.34), run_time=1.26)
        self.at("1997")
        yr = T("1997", 38, GOLD, weight=BOLD).move_to(xy(3.99, -2.72))
        self.play(FadeIn(yr), run_time=0.48)
        seq = sequence(ROWS[:3], xy(3.92, -1.39), 0.34)
        seq[0].shift(RIGHT * 0.37)
        seq[2].shift(LEFT * 0.37)
        self.play(FadeIn(seq, shift=LEFT * 0.61), run_time=1.3)
        self.at("and colleagues compared")
        self.play(seq[0].animate.shift(LEFT * 0.37),
                  seq[2].animate.shift(RIGHT * 0.37), run_time=0.65)
        seq_name = T("18S ribosomal RNA", 31, BLUE).move_to(xy(3.86, -0.45))
        self.play(FadeIn(seq_name), run_time=0.45)
        old = animal_tree(moulting=False)
        self.at("RNA genes")
        self.play(FadeOut(seq, shift=LEFT * 1.5), FadeOut(seq_name), run_time=0.42)
        self.play(ReplacementTransform(ladder, old),
                  *[icon.animate.move_to(p + UP * 0.50)
                    for icon, p in zip(icons, ANIMAL_TIPS[:3])], run_time=1.43)
        self.at("They grouped nematodes")
        final = animal_tree()
        self.play(Transform(old[1], final[1]), Transform(old[2], final[2]),
                  FadeOut(old[5]), GrowFromCenter(joint(ANIMAL_ROOT)),
                  GrowFromCenter(joint(MOULT)), run_time=1.25)
        _, labels, others = animal_tips()
        self.at("and other molting animals")
        self.play(FadeIn(labels[1]), FadeIn(labels[2]), FadeIn(others), run_time=0.53)
        light, move = signal(ANIMAL_ROOT, MOULT, radius=0.23)
        self.play(move, run_time=0.89)
        self.remove(light)
        self.at("not annelids")
        self.play(FadeIn(labels[0]), edge_color(old[0], GOLD), FadeOut(yr), run_time=0.66)
        self.finish()


PLANT_ROOT = xy(0.17, -2.57)
BRYOPHYTES = xy(-2.56, -0.18)
PLANT_TIPS = tuple(xy(x, 1.92) for x in (-5.14, -2.64, -0.12, 4.01))


def sprout(kind):
    n = 3 if kind == 3 else 2
    stems = VGroup(*[Line(xy(0, -0.34), xy(i * 0.18, 0.28 - 0.06 * abs(i)),
                           color=BLUE, stroke_width=5) for i in range(-n, n + 1)])
    if kind == 2:
        return stems
    leaves = VGroup(*[Ellipse(width=0.27 + 0.09 * kind, height=0.15,
                              fill_color=BLUE, fill_opacity=1, stroke_width=0)
                      .rotate((1 if i < 0 else -1) * 0.58)
                      .move_to(xy(i * 0.24, 0.21 - abs(i) * 0.04))
                      for i in range(-n, n + 1)])
    return VGroup(stems, leaves)


def plants(unresolved=False):
    p = PLANT_ROOT if unresolved else BRYOPHYTES
    first = branch(PLANT_ROOT, PLANT_TIPS[3], width=0.89)
    left = branch(PLANT_ROOT, BRYOPHYTES, width=1.02)
    core = VGroup(first, *[branch(p, t, width=0.70) for t in PLANT_TIPS[:3]], left)
    if unresolved:
        left.set_opacity(0)
    icons = VGroup(*[sprout(i).move_to(t + UP * 0.49) for i, t in enumerate(PLANT_TIPS)])
    labels = VGroup(*[tip_label(n, icon) for n, icon in
                      zip(("Mosses", "Liverworts", "Hornworts", "Vascular plants"), icons)])
    return core, icons, labels


class S11UnlockedPlantsClose(SpokenScene):
    def construct(self):
        animals = animal_tree(highlighted=True)
        animal_icons, animal_names, other = animal_tips()
        animal_moult = joint(MOULT)
        root = joint(PLANT_ROOT)
        plant, icons, labels = plants(unresolved=True)
        self.add(animals, animal_icons, animal_names, other, animal_moult, schematic())
        self.at("Plant trees shifted")
        self.play(FadeOut(animal_icons), FadeOut(animal_names), FadeOut(other),
                  FadeOut(animal_moult), run_time=0.42)
        self.play(ReplacementTransform(animals, plant), run_time=1.24)
        self.play(FadeIn(icons, shift=UP * 0.20), GrowFromCenter(root), run_time=0.70)
        self.at("2019")
        year = T("2019", 38, GOLD, weight=BOLD).move_to(xy(4.87, -2.62))
        self.play(FadeIn(year), run_time=0.45)
        tracks = sequence(ROWS + ROWS[:1], xy(3.94, -0.77), 0.25)
        self.at("Plant Transcriptomes Initiative")
        self.play(LaggedStart(*[FadeIn(s, shift=LEFT * 0.55) for s in tracks],
                              lag_ratio=0.33), run_time=1.92)
        self.at("genes from more")
        count = note("More than 1,100 species", BLUE)
        self.play(FadeIn(count), run_time=0.43)
        self.play(FadeOut(tracks, shift=xy(-2.93, -1.67), scale=0.25), run_time=1.77)
        self.at("Its nuclear gene trees")
        grouped, _, _ = plants()
        bryophytes = joint(BRYOPHYTES)
        self.play(FadeOut(count), FadeOut(year), run_time=0.30)
        self.play(Transform(plant, grouped), GrowFromCenter(bryophytes), run_time=1.67)
        self.at("living mosses")
        self.play(LaggedStart(*[FadeIn(l) for l in labels[:3]], lag_ratio=0.66),
                  run_time=2.51)
        self.at("A living moss")
        self.play(FadeIn(labels[3]), run_time=0.52)
        bead, move = signal(PLANT_TIPS[0], BRYOPHYTES, PLANT_ROOT, PLANT_TIPS[3], radius=0.21)
        self.play(move, run_time=3.29)
        self.remove(bead)
        self.at("Every tree maps descent")
        markers = VGroup(tick(PLANT_ROOT, BRYOPHYTES, 0.53),
                         tick(PLANT_ROOT, PLANT_TIPS[3], 0.56))
        self.play(LaggedStart(GrowFromCenter(markers[0]), GrowFromCenter(markers[1]),
                              lag_ratio=0.48), run_time=1.25)
        self.play(Indicate(root, color=GOLD, scale_factor=1.45),
                  Indicate(bryophytes, color=GOLD, scale_factor=1.45),
                  edge_color(plant[0], GOLD), edge_color(plant[4], GOLD), run_time=1.75)
        self.finish()


class S12End(EndCard):
    LINE = "Build trees from shared derived states; read relatedness at the nodes."
