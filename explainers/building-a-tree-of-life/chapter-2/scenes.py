"""Read the Branch Point — chapter 2 of Building a Tree of Life.

COLOR MAP (shared with chapter 1)
  BLUE = whale and its tracer
  GREEN = hippo and its tracer
  GREY = tuna, neutral structure, and uncertainty
  TEAL = inherited evidence / shared derived traits
  GOLD = common ancestral populations / branch points

The tree is rebuilt only through ``relationship_tree`` so carried geometry never drifts.
Animal drawings are deliberately schematic labelled silhouettes, not anatomical claims.
"""
from bp_parts import *  # noqa: F401,F403


TREE_CENTRE = np.array([0.0, 0.15, 0.0])


def diagram_surface():
    """The shared moving diagram paper: visual texture, not biological content."""
    paper = RoundedRectangle(corner_radius=0.28, width=13.15, height=7.15,
                             stroke_color="#30414A", stroke_width=2,
                             fill_color="#17242B", fill_opacity=1.0)
    paper.set_z_index(-30)
    grid = VGroup(
        *[Line([x, -3.45, 0], [x, 3.45, 0], color="#36515C",
               stroke_width=5).set_opacity(0.45) for x in np.arange(-6.0, 6.1, 1.0)],
        *[Line([-6.4, y, 0], [6.4, y, 0], color="#36515C",
               stroke_width=5).set_opacity(0.45) for y in np.arange(-3.0, 3.1, 1.0)],
    )
    grid.set_z_index(-29.5)
    for line in grid:
        line.layout_ok = True  # intentional diagram-paper ruling behind text
    bands = VGroup()
    for x, opacity in ((-5.2, 0.22), (-0.8, 0.22), (3.7, 0.22)):
        band = Rectangle(width=1.15, height=7.0, stroke_width=0,
                         fill_color=TEAL, fill_opacity=opacity).move_to([x, 0, 0])
        band.set_z_index(-29)

        def drift(mob, dt):
            mob.shift(RIGHT * 0.30 * dt)
            if mob.get_left()[0] > 6.65:
                mob.shift(LEFT * 13.9)
        band.add_updater(drift)
        bands.add(band)
    surface = VGroup(paper, grid, bands)
    surface.layout_ok = True  # intentional full-frame background behind all labels
    return surface


class DiagramScene(SpokenScene):
    """Spoken scene on the chapter's continuously moving diagram surface."""
    def setup(self):
        super().setup()
        self.add(diagram_surface())


def animal_icon(name, color, at, scale=1.0):
    """A consistent schematic animal marker: coloured silhouette plus an upright label."""
    body = Ellipse(width=0.72 * scale, height=0.42 * scale, color=color,
                   stroke_width=3, fill_color=color, fill_opacity=0.22)
    head = Circle(radius=0.16 * scale, color=color, stroke_width=3,
                  fill_color=color, fill_opacity=0.22).next_to(body, RIGHT, buff=-0.03 * scale)
    tail = Triangle(color=color, stroke_width=3, fill_color=color, fill_opacity=0.22)
    tail.set_height(0.28 * scale).rotate(PI / 2).next_to(body, LEFT, buff=-0.04 * scale)
    picture = VGroup(tail, body, head).move_to(at)
    label = T(name, 28, color, weight=BOLD).next_to(picture, RIGHT, buff=0.18)
    g = VGroup(picture, label)
    g.picture, g.label = picture, label
    return g


def relationship_tree(swapped=False, labels=True, trait=True, dim=False):
    """The chapter's one carried tree, always at the same scale and coordinates."""
    root = np.array([-3.2, -0.35, 0.0])
    early = np.array([-1.95, -0.35, 0.0])
    shared = np.array([0.0, 0.55, 0.0])
    tuna_tip = np.array([2.9, -2.05, 0.0])
    whale_tip = np.array([2.9, 2.05 if not swapped else 0.45, 0.0])
    hippo_tip = np.array([2.9, 0.45 if not swapped else 2.05, 0.0])

    trunk = VGroup(
        Line(root, early, color=GREY, stroke_width=7),
        Line(early, shared, color=GREY, stroke_width=7),
    )
    tuna_branch = VGroup(
        Line(early, [early[0], tuna_tip[1], 0], color=GREY, stroke_width=7),
        Line([early[0], tuna_tip[1], 0], tuna_tip, color=GREY, stroke_width=7),
    )
    whale_branch = VGroup(
        Line(shared, [shared[0], whale_tip[1], 0], color=BLUE, stroke_width=7),
        Line([shared[0], whale_tip[1], 0], whale_tip, color=BLUE, stroke_width=7),
    )
    hippo_branch = VGroup(
        Line(shared, [shared[0], hippo_tip[1], 0], color=GREEN, stroke_width=7),
        Line([shared[0], hippo_tip[1], 0], hippo_tip, color=GREEN, stroke_width=7),
    )
    early_node = Dot(early, radius=0.14, color=GOLD)
    shared_node = Dot(shared, radius=0.17, color=GOLD)
    root_dot = Dot(root, radius=0.08, color=GREY)
    whale = animal_icon("whale", BLUE, whale_tip + RIGHT * 0.35, 0.78)
    hippo = animal_icon("hippo", GREEN, hippo_tip + RIGHT * 0.35, 0.78)
    tuna = animal_icon("tuna", GREY, tuna_tip + RIGHT * 0.35, 0.78)
    tips = VGroup(whale, hippo, tuna)
    if not labels:
        for icon in tips:
            icon.remove(icon.label)

    trait_mark = VGroup(
        Line([-1.35, 0.0, 0], [-1.07, -0.52, 0], color=TEAL, stroke_width=8),
        T("shared derived\ntrait", 26, TEAL, weight=BOLD,
          line_spacing=0.8).move_to([-2.25, 0.92, 0]),
    )
    pieces = [trunk, tuna_branch, whale_branch, hippo_branch,
              early_node, shared_node, root_dot, tips]
    if trait:
        pieces.append(trait_mark)
    g = VGroup(*pieces)
    if dim:
        g.set_opacity(0.35)
    g.root, g.early, g.shared = root, early, shared
    g.tuna_tip, g.whale_tip, g.hippo_tip = tuna_tip, whale_tip, hippo_tip
    g.trunk, g.tuna_branch = trunk, tuna_branch
    g.whale_branch, g.hippo_branch = whale_branch, hippo_branch
    g.early_node, g.shared_node = early_node, shared_node
    g.whale, g.hippo, g.tuna, g.tips = whale, hippo, tuna, tips
    g.trait_mark = trait_mark
    return g


def trace_path(tree, tip, node):
    """A tip-to-node polyline that follows the drawn right-angle branch."""
    return VMobject().set_points_as_corners([
        tip, np.array([node[0], tip[1], 0.0]), node
    ])


def matrix_picture(show_checks=True):
    """The schematic trait table used in s02 and rebuilt at the start of s03."""
    x0, y0 = -3.9, 1.75
    row_y = [1.25, 0.0, -1.25]
    col_x = [-0.9, 1.0, 2.9]
    rows = VGroup(*[animal_icon(n, c, [x0, y, 0], 0.7)
                    for n, c, y in zip(("whale", "hippo", "tuna"),
                                       (BLUE, GREEN, GREY), row_y)])
    heads = VGroup(*[T(t, 28, TEAL).move_to([x, y0 + 0.55, 0])
                     for x, t in zip(col_x, ("trait A", "trait B", "trait C"))])
    hlines = VGroup(*[Line([-4.9, y - 0.52, 0], [3.8, y - 0.52, 0], color=GREY,
                               stroke_width=2).set_opacity(0.45) for y in row_y])
    vlines = VGroup(*[Line([x - 0.7, 2.55, 0], [x - 0.7, -1.85, 0], color=GREY,
                               stroke_width=2).set_opacity(0.45) for x in col_x])
    checks = VGroup()
    patterns = ((0, 1, 2), (0, 1), (0,))
    columns = []
    for x, inds in zip(col_x, patterns):
        col = VGroup()
        for i in inds:
            mark = T("✓", 46, TEAL, weight=BOLD).move_to([x, row_y[i], 0])
            col.add(mark)
            checks.add(mark)
        columns.append(col)
    g = VGroup(rows, heads, hlines, vlines)
    if show_checks:
        g.add(checks)
    g.rows, g.heads, g.checks, g.columns = rows, heads, checks, columns
    g.col_x, g.row_y = col_x, row_y
    return g


def rotated_question_backdrop():
    tree = relationship_tree(swapped=True)
    q = question_card("Did the relationship change, or only the drawing?", y=-3.18,
                      size=30, max_w=11.2)
    return tree, q


class S00Hook(DiagramScene):
    def construct(self):
        tree = relationship_tree()
        self.at("The first film")
        self.play(LaggedStart(Create(tree.trunk), Create(tree.tuna_branch),
                              Create(tree.whale_branch), Create(tree.hippo_branch),
                              FadeIn(tree.tips), FadeIn(tree.early_node),
                              FadeIn(tree.shared_node), lag_ratio=0.12), run_time=2.2)
        self.play(FadeIn(tree.trait_mark), run_time=0.7)
        pulse(tree.whale.picture, base=3, amp=1.2, speed=2.5)
        pulse(tree.hippo.picture, base=3, amp=1.2, speed=2.5)
        self.add(tree.whale.picture, tree.hippo.picture)

        self.at("Once evidence is scored")
        near = DoubleArrow([3.25, 1.68, 0], [3.25, -1.67, 0], buff=0.1,
                           color=GREY, stroke_width=4, tip_length=0.18)
        wrong = T("nearest tips?", 30, GREY).next_to(near, RIGHT, buff=0.2)
        self.play(GrowArrow(near), FadeIn(wrong), run_time=1.0)

        self.at("The answer is not")
        self.play(FadeOut(near), FadeOut(wrong), run_time=0.5)
        p1 = trace_path(tree, tree.whale_tip, tree.shared + [-0.32, 0.22, 0])
        p2 = trace_path(tree, tree.hippo_tip, tree.shared + [0.32, -0.22, 0])
        q1 = T("?", 32, BLUE).move_to(tree.whale_tip)
        q2 = T("?", 32, GREEN).move_to(tree.hippo_tip)
        # Deliberate: these question marks ride directly on the branch paths they question.
        q1.layout_ok = q2.layout_ok = True
        self.play(MoveAlongPath(q1, p1), MoveAlongPath(q2, p2), run_time=2.0, rate_func=linear)
        self.at("shared branch point")
        self.play(FadeOut(q1), FadeOut(q2),
                  Indicate(tree.shared_node, color=GOLD, scale_factor=2.0), run_time=0.9)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Building a Tree of Life"
    TITLE = "Read the Branch Point"


class S02Scores(DiagramScene):
    def construct(self):
        table = matrix_picture(show_checks=False)
        self.at("Begin with a trait table")
        self.play(FadeIn(table.rows), Create(table[2]), Create(table[3]), run_time=1.5)
        self.play(FadeIn(table.heads), run_time=0.7)

        self.at("Each row is an organism")
        self.play(LaggedStart(*[Indicate(r.picture, scale_factor=1.08) for r in table.rows],
                              lag_ratio=0.22), run_time=1.2)
        self.at("each column")
        self.play(LaggedStart(*[Indicate(h, color=TEAL, scale_factor=1.08) for h in table.heads],
                              lag_ratio=0.22), run_time=1.1)

        self.at("A present mark")
        self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in table.columns[0]],
                              lag_ratio=0.18), run_time=1.0)
        self.at("When the same marks")
        self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in table.columns[1]],
                              lag_ratio=0.18), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in table.columns[2]],
                              lag_ratio=0.18), run_time=0.6)

        all_box = SurroundingRectangle(VGroup(table.rows[0], table.rows[1], table.rows[2]),
                                       color=TEAL, buff=0.12, corner_radius=0.14)
        pair_box = SurroundingRectangle(VGroup(table.rows[0], table.rows[1]),
                                        color=TEAL, buff=0.08, corner_radius=0.14)
        one_box = SurroundingRectangle(table.rows[0], color=TEAL, buff=0.06, corner_radius=0.14)
        self.play(Create(all_box), run_time=0.6)
        self.play(Create(pair_box), run_time=0.6)
        self.play(Create(one_box), run_time=0.5)
        self.at("the groups are nested")
        brackets = VGroup(Brace(all_box, RIGHT, color=TEAL),
                          Brace(pair_box, RIGHT, color=TEAL),
                          Brace(one_box, RIGHT, color=TEAL))
        self.play(FadeOut(VGroup(all_box, pair_box, one_box)), FadeIn(brackets), run_time=0.8)
        self.at("A tree can show")
        self.play(brackets.animate.shift(LEFT * 1.0), run_time=1.0)
        self.finish()


class S03Derived(DiagramScene):
    def construct(self):
        table = matrix_picture(show_checks=True)
        self.add(table)
        trait_tile = chip("shared derived trait", TEAL, 28).move_to([4.65, 2.8, 0])
        self.at("A useful marker")
        self.play(FadeIn(trait_tile, shift=DOWN * 0.15), run_time=0.8)
        self.at("It first appeared")
        ancestor = Dot([-3.2, -0.25, 0], radius=0.20, color=GOLD)
        descendants = VGroup(*[Dot(p, radius=0.14, color=TEAL)
                               for p in ([1.6, 1.8, 0], [2.1, -0.15, 0], [1.6, -2.0, 0])])
        rays = VGroup(*[Line(ancestor.get_center(), d.get_center(), color=TEAL,
                             stroke_width=4) for d in descendants])
        self.play(FadeOut(table), FadeIn(ancestor), LaggedStart(*[Create(r) for r in rays], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(d) for d in descendants], lag_ratio=0.15), run_time=1.5)

        self.at("Move its mark")
        tree = relationship_tree(trait=False)
        self.play(FadeOut(VGroup(ancestor, descendants, rays)),
                  LaggedStart(Create(tree.trunk), Create(tree.tuna_branch),
                              Create(tree.whale_branch), Create(tree.hippo_branch),
                              FadeIn(tree.tips), FadeIn(tree.early_node),
                              FadeIn(tree.shared_node), lag_ratio=0.1), run_time=1.7)
        travel = VMobject().set_points_as_corners([
            trait_tile.get_center(), [4.65, 3.25, 0], [-2.25, 3.25, 0], [-2.25, 0.92, 0]
        ])
        self.play(MoveAlongPath(trait_tile, travel), run_time=1.2, rate_func=smooth)
        final_label = tree.trait_mark[1].copy()
        tick = tree.trait_mark[0].copy()
        self.play(FadeOut(trait_tile), FadeIn(final_label), Create(tick), run_time=0.7)

        self.at("Every tip beyond")
        glow1 = tree.whale_branch.copy().set_color(TEAL).set_stroke(width=11)
        glow2 = tree.hippo_branch.copy().set_color(TEAL).set_stroke(width=11)
        self.play(Create(glow1), Create(glow2), run_time=1.5)
        self.play(Indicate(tree.whale.picture, color=TEAL), Indicate(tree.hippo.picture, color=TEAL),
                  run_time=0.9)
        self.add(scope_tag("schematic"))
        self.finish()


class S04Nodes(DiagramScene):
    def construct(self):
        tree = relationship_tree()
        self.add(tree, scope_tag("schematic"))
        self.at("A branch point")
        node_label = fit_text("common ancestral population", max_w=3.0, size=30,
                              color=GOLD, max_lines=2).move_to([0.0, -0.85, 0])
        self.play(Indicate(tree.shared_node, color=GOLD, scale_factor=2.2), run_time=0.8)
        self.play(FadeIn(node_label, shift=DOWN * 0.12), run_time=0.7)

        self.at("Start at two tips")
        blue_path = trace_path(tree, tree.whale_tip, tree.shared)
        green_path = trace_path(tree, tree.hippo_tip, tree.shared)
        blue_trace = blue_path.copy().set_stroke(BLUE, 12)
        green_trace = green_path.copy().set_stroke(GREEN, 12)
        self.play(Create(blue_trace), Create(green_trace), run_time=2.1, rate_func=linear)
        self.at("Stop at the first node")
        pulse(tree.shared_node, base=2, amp=3, speed=3)
        self.add(tree.shared_node)
        self.play(Indicate(tree.shared_node, color=GOLD, scale_factor=2.0), run_time=0.9)

        self.at("A pair sharing a later node")
        grey_path = VMobject().set_points_as_corners([
            tree.tuna_tip, [-1.95, tree.tuna_tip[1], 0], tree.early
        ]).set_stroke(GREY, 11)
        earlier = T("earlier node", 28, GOLD).move_to([-4.0, -0.85, 0])
        self.play(Create(grey_path), run_time=1.4, rate_func=linear)
        self.play(Indicate(tree.early_node, color=GOLD, scale_factor=2.0), FadeIn(earlier), run_time=0.8)

        self.at("Trace shared derived traits")
        self.play(FadeOut(node_label), FadeOut(earlier), run_time=0.4)
        rule = caption("Trace traits to branch points to find the closest relatives.",
                       size=30, color=TEAL, y=-3.15)
        self.play(FadeIn(rule, shift=UP * 0.12), run_time=0.9)
        self.finish()


class S05Predict(DiagramScene):
    def construct(self):
        before = relationship_tree()
        self.add(before)
        self.at("Now spin")
        after = relationship_tree(swapped=True)
        self.play(Transform(before.whale_branch, after.whale_branch),
                  Transform(before.hippo_branch, after.hippo_branch),
                  Transform(before.whale, after.whale),
                  Transform(before.hippo, after.hippo), run_time=2.8, rate_func=smooth)
        self.at("The tips trade places")
        self.play(Indicate(before.whale.picture, color=BLUE),
                  Indicate(before.hippo.picture, color=GREEN), run_time=0.9)
        self.at("Did the relationship change")
        q = question_card("Did the relationship change, or only the drawing?", y=-3.18,
                          size=30, max_w=11.2)
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.8)
        self.at("Follow both paths")
        p1 = trace_path(after, after.whale_tip, after.shared)
        p2 = trace_path(after, after.hippo_tip, after.shared)
        d1, d2 = Dot(after.whale_tip, radius=0.10, color=BLUE), Dot(after.hippo_tip, radius=0.10, color=GREEN)
        self.play(MoveAlongPath(d1, p1), MoveAlongPath(d2, p2), run_time=1.8, rate_func=linear)
        self.finish()


class S06Pause(Scene):
    def construct(self):
        tree, q = rotated_question_backdrop()
        self.add(diagram_surface(), tree, q)
        ring, ring_run = countdown(4.5, center=[6.0, -3.05, 0], radius=0.38)
        self.add(ring)
        p1 = trace_path(tree, tree.whale_tip, tree.shared)
        p2 = trace_path(tree, tree.hippo_tip, tree.shared)
        d1, d2 = Dot(tree.whale_tip, radius=0.10, color=BLUE), Dot(tree.hippo_tip, radius=0.10, color=GREEN)
        motion = AnimationGroup(MoveAlongPath(d1, p1), MoveAlongPath(d2, p2),
                                run_time=4.5, rate_func=linear)
        self.play(ring_run, motion)


class S07RotationReveal(DiagramScene):
    def construct(self):
        tree = relationship_tree(swapped=True)
        self.add(tree)
        self.at("Only the drawing moved")
        same = chip("same relationship", GOLD, 28).move_to([0.0, -1.0, 0])
        self.play(FadeIn(same, scale=0.8), Indicate(tree.shared_node, color=GOLD), run_time=0.9)

        self.at("Both paths still meet")
        p1 = trace_path(tree, tree.whale_tip, tree.shared).set_stroke(BLUE, 11)
        p2 = trace_path(tree, tree.hippo_tip, tree.shared).set_stroke(GREEN, 11)
        self.play(Create(p1), Create(p2), run_time=1.6)
        self.play(Indicate(tree.shared_node, color=GOLD, scale_factor=2.0), run_time=0.7)

        self.at("Tip order cannot")
        self.play(FadeOut(VGroup(same, p1, p2)), run_time=0.4)
        labels = VGroup(tree.whale.label, tree.hippo.label, tree.tuna.label, tree.trait_mark[1])
        self.play(FadeOut(labels), run_time=0.3)
        topology = VGroup(tree.trunk, tree.tuna_branch, tree.whale_branch, tree.hippo_branch,
                          tree.early_node, tree.shared_node,
                          tree.whale.picture, tree.hippo.picture, tree.tuna.picture)
        self.play(Rotate(topology, PI / 2, about_point=TREE_CENTRE), run_time=1.4)
        self.play(Rotate(topology, PI / 2, about_point=TREE_CENTRE), run_time=1.4)

        self.at("no top or goal")
        no_top = T("no top • no goal", 34, GOLD, weight=BOLD).move_to([0, -3.05, 0])
        self.play(FadeIn(no_top), run_time=0.6)
        self.play(Rotate(topology, -PI, about_point=TREE_CENTRE), run_time=1.5)
        self.play(FadeIn(labels), run_time=0.4)

        self.at("Every living tip")
        pulse(tree.whale.picture, base=3, amp=1.5, speed=3)
        pulse(tree.hippo.picture, base=3, amp=1.5, speed=3)
        pulse(tree.tuna.picture, base=3, amp=1.5, speed=3)
        self.add(tree.whale.picture, tree.hippo.picture, tree.tuna.picture)
        self.play(FadeOut(no_top), run_time=0.4)
        self.wait(2.0)
        self.finish()


def panel_tree(origin, stretch=False):
    """Compact tree for the branch-length comparison (topology is identical)."""
    ox, oy = origin[0], origin[1]
    r, a, b = np.array([ox - 2.0, oy, 0]), np.array([ox - 1.0, oy, 0]), np.array([ox, oy + 0.45, 0])
    upper_x = ox + (2.25 if stretch else 1.65)
    lower_x = ox + 1.65
    lines = VGroup(
        Line(r, a, color=GREY, stroke_width=6), Line(a, b, color=GREY, stroke_width=6),
        Line(a, [a[0], oy - 1.25, 0], color=GREY, stroke_width=6),
        Line([a[0], oy - 1.25, 0], [lower_x, oy - 1.25, 0], color=GREY, stroke_width=6),
        Line(b, [b[0], oy + 1.2, 0], color=BLUE, stroke_width=6),
        Line([b[0], oy + 1.2, 0], [upper_x, oy + 1.2, 0], color=BLUE, stroke_width=6),
        Line(b, [b[0], oy - 0.25, 0], color=GREEN, stroke_width=6),
        Line([b[0], oy - 0.25, 0], [lower_x, oy - 0.25, 0], color=GREEN, stroke_width=6),
    )
    nodes = VGroup(Dot(a, radius=0.11, color=GOLD), Dot(b, radius=0.12, color=GOLD))
    tips = VGroup(Dot([upper_x, oy + 1.2, 0], radius=0.13, color=BLUE),
                  Dot([lower_x, oy - 0.25, 0], radius=0.13, color=GREEN),
                  Dot([lower_x, oy - 1.25, 0], radius=0.13, color=GREY))
    return VGroup(lines, nodes, tips)


class S08Lengths(DiagramScene):
    def construct(self):
        panels = TwoPanel("plain cladogram: length unscaled (schematic)",
                          "tree with a time scale (schematic)",
                          colors=(GREY, GOLD), size=29)
        left_short = panel_tree([-3.3, 0.25, 0], stretch=False)
        left_long = panel_tree([-3.3, 0.25, 0], stretch=True)
        right = panel_tree([3.2, 0.25, 0], stretch=False)
        self.at("Branch length needs a key")
        self.play(FadeIn(panels), run_time=1.0)
        self.play(Create(left_short), run_time=1.1)

        self.at("a long line")
        self.play(Transform(left_short, left_long), run_time=1.8)
        empty = T("layout space", 28, GREY).move_to([-3.1, -1.65, 0])
        self.play(FadeIn(empty), run_time=0.5)
        self.at("does not automatically")
        not_equal = T("≠ time or change", 28, GREY, weight=BOLD).move_to([-3.25, -2.2, 0])
        self.play(FadeIn(not_equal), run_time=0.8)

        self.at("Some trees add a scale")
        self.play(Create(right), run_time=1.1)
        ruler = VGroup(Line([1.8, -1.72, 0], [5.0, -1.72, 0], color=GOLD, stroke_width=5),
                       *[Line([x, -1.87, 0], [x, -1.57, 0], color=GOLD, stroke_width=4)
                         for x in np.linspace(1.8, 5.0, 5)],
                       T("time scale", 28, GOLD).move_to([3.4, -2.18, 0]))
        self.play(Create(ruler[0]), LaggedStart(*[Create(t) for t in ruler[1:6]], lag_ratio=0.1),
                  FadeIn(ruler[6]), run_time=1.3)
        self.at("Read that scale")
        self.play(Indicate(ruler, color=GOLD, scale_factor=1.03), run_time=0.9)
        self.finish()


class S09Limits(DiagramScene):
    def construct(self):
        tree = relationship_tree(labels=False, trait=False)
        tree.scale(0.72).move_to([0.0, -0.1, 0])
        frame = RoundedRectangle(corner_radius=0.2, width=7.2, height=5.2, color=GREY,
                                 stroke_width=3).move_to([0, -0.1, 0])
        heading = fit_text("organisms and evidence included", max_w=6.6, size=30,
                           color=TEXT).move_to([0, 2.78, 0])
        self.at("A tree can only use")
        self.play(Create(frame), FadeIn(heading), Create(tree), run_time=1.7)

        fossil = chip("fossil", GOLD, 28).move_to([-5.25, 1.65, 0])
        sequence = VGroup(RoundedRectangle(corner_radius=0.08, width=1.8, height=0.7,
                                           color=TEAL, fill_color=TEAL, fill_opacity=0.12),
                          T("sequence", 26, TEAL)).move_to([-5.25, 0.0, 0])
        trait = chip("trait", TEAL, 28).move_to([-5.25, -1.65, 0])
        self.at("New fossils")
        self.play(FadeIn(fossil, shift=RIGHT * 0.2), run_time=0.6)
        self.at("sequences")
        self.play(FadeIn(sequence, shift=RIGHT * 0.2), run_time=0.6)
        self.at("or traits")
        self.play(FadeIn(trait, shift=RIGHT * 0.2), run_time=0.6)
        paths = VGroup(DashedLine(fossil.get_right(), [-1.9, 1.25, 0], color=GOLD),
                       DashedLine(sequence.get_right(), [-1.9, 0.3, 0], color=TEAL),
                       DashedLine(trait.get_right(), [-1.9, -0.8, 0], color=TEAL))
        self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.2), run_time=1.2)

        self.at("Different evidence may disagree")
        alt = DashedLine([0.25, 0.2, 0], [2.7, 1.55, 0], color=GREY, stroke_width=5)
        test = chip("test", GREY, 26).move_to([4.85, 1.55, 0])
        uncertain = T("?", 44, GREY).next_to(test, DOWN, buff=0.15)
        self.play(Create(alt), FadeIn(test), FadeIn(uncertain), run_time=1.0)

        self.at("treat the tree as a supported model")
        model = chip("supported\nmodel", TEAL, 28).move_to([4.85, -0.6, 0])
        converge = VGroup(*[Arrow(p.get_end(), model.get_left(), buff=0.1,
                                 color=TEAL, stroke_width=4, tip_length=0.16) for p in paths])
        self.play(FadeIn(model), LaggedStart(*[GrowArrow(a) for a in converge], lag_ratio=0.15), run_time=1.4)

        self.at("Scientists can update")
        self.play(Indicate(tree.shared_node, color=GOLD, scale_factor=1.8),
                  Indicate(alt, color=GREY, scale_factor=1.05), run_time=1.0)
        self.at("The clean classroom table")
        note = caption("A starting case — not every case.", size=30, color=GREY, y=-3.2)
        self.play(FadeIn(note, shift=UP * 0.12), run_time=0.8)
        bob(uncertain, amp=0.05, speed=2.0)
        self.add(uncertain)
        self.finish()


class S10Return(DiagramScene):
    def construct(self):
        tree = relationship_tree()
        self.add(tree, scope_tag("schematic"))
        self.at("do not read across")
        across = DoubleArrow(tree.whale_tip + [0.15, -0.25, 0],
                             tree.tuna_tip + [0.15, 0.25, 0], color=GREY,
                             stroke_width=4, tip_length=0.16)
        cross = VGroup(Line(across.get_corner(DL), across.get_corner(UR), color=RED, stroke_width=6),
                       Line(across.get_corner(UL), across.get_corner(DR), color=RED, stroke_width=6))
        self.play(GrowArrow(across), Create(cross), run_time=0.9)
        self.at("Trace backward")
        self.play(FadeOut(across), FadeOut(cross), run_time=0.3)
        p1 = trace_path(tree, tree.whale_tip, tree.shared).set_stroke(BLUE, 12)
        p2 = trace_path(tree, tree.hippo_tip, tree.shared).set_stroke(GREEN, 12)
        self.play(Create(p1), Create(p2), run_time=1.6, rate_func=linear)

        self.at("Find the first node")
        self.play(Indicate(tree.shared_node, color=GOLD, scale_factor=2.2), run_time=0.8)
        self.at("shared derived trait")
        self.play(Indicate(tree.trait_mark, color=TEAL, scale_factor=1.08), run_time=0.9)

        self.at("Rotation changes the picture")
        rot_icon = VGroup(Arc(radius=0.35, start_angle=0.3, angle=1.7 * PI, color=GREY,
                              stroke_width=4), Triangle(color=GREY, fill_opacity=1).set_height(0.18))
        rot_icon[1].move_to(rot_icon[0].get_end()).rotate(-0.5)
        rot_icon.move_to([-5.6, 2.5, 0])
        scale_icon = VGroup(Line([-0.55, 0, 0], [0.55, 0, 0], color=GREY, stroke_width=4),
                            *[Line([x, -0.14, 0], [x, 0.14, 0], color=GREY, stroke_width=3)
                              for x in np.linspace(-0.55, 0.55, 5)]).move_to([5.5, 2.5, 0])
        self.play(FadeIn(rot_icon), FadeIn(scale_icon), run_time=0.8)
        self.at("The branching order")
        self.play(FadeOut(VGroup(rot_icon, scale_icon, p1, p2)),
                  Indicate(VGroup(tree.trunk, tree.whale_branch, tree.hippo_branch),
                           color=GOLD, scale_factor=1.02), run_time=1.1)
        self.finish()


class S11End(EndCard):
    LINE = "Trace shared derived traits to branch points to find the closest relatives."
