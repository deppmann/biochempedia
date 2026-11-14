"""Reading a Pathway Backward — complementation and pathways, chapter 2.

Every continuing pathway is rebuilt by ``pathway_world`` so its scale and landmarks do not drift.

COLOR MAP (carried exactly from chapter 1)
  BLUE   = one function / early supplied material
  YELLOW = a distinct function / later supplied material (the chapter-one gold step colour)
  GREEN  = observed rescue and growth
  RED    = a tested block or failed rescue
  GREY   = inactive context and neutral structure
  TEXT   = active neutral material
"""
from bp_parts import *  # noqa: F401,F403


STEP_COLORS = (BLUE, YELLOW, BLUE, YELLOW)
NODE_X = (-5.25, -2.05, 1.95, 5.3)
PATH_Y = 0.55


def dark_chip(text, color=BLUE, size=28, **kwargs):
    """Chapter-one chip with an opaque ground, so paths never show through its label."""
    c = chip(text, color=color, size=size, **kwargs)
    back = RoundedRectangle(
        corner_radius=0.14, width=c[0].width, height=c[0].height,
        stroke_width=0, fill_color=BG, fill_opacity=1,
    ).move_to(c[0])
    return VGroup(back, *c)


def path_arrow(a, b, color=GREY, width=5, opacity=1.0):
    return Arrow(
        a, b, buff=0, color=color, stroke_width=width, stroke_opacity=opacity,
        tip_length=0.22, max_tip_length_to_length_ratio=0.45,
        max_stroke_width_to_length_ratio=14,
    )


def barrier(x, y=PATH_Y):
    bar = Line([x, y - 0.68, 0], [x, y + 0.68, 0], color=RED, stroke_width=12)
    cap1 = Line([x - 0.22, y + 0.68, 0], [x + 0.22, y + 0.68, 0], color=RED, stroke_width=8)
    cap2 = Line([x - 0.22, y - 0.68, 0], [x + 0.22, y - 0.68, 0], color=RED, stroke_width=8)
    return VGroup(bar, cap1, cap2)


def flow_dots(x0, x1, y=PATH_Y, color=TEXT, n=3, speed=0.22, radius=0.075):
    """Continuously moving schematic material; the only motion is along the shown path."""
    dots = VGroup()
    span = x1 - x0
    for i in range(n):
        d = Dot([x0 + span * i / n, y, 0], radius=radius, color=color)
        d._flow_t = i / n

        def drift(mob, dt, x0=x0, span=span, y=y, speed=speed):
            mob._flow_t = (mob._flow_t + speed * dt) % 1.0
            mob.move_to([x0 + span * mob._flow_t, y, 0])

        d.add_updater(drift)
        dots.add(d)
    return dots


def pathway_world(*, blocks=(), product_color=YELLOW, gauge_value=0.0, dim_after=None,
                  functions=False, pile=False, flow=None, cell=True):
    """The carried pathway picture used at the same size and place throughout the chapter."""
    g = VGroup()
    if cell:
        shell = RoundedRectangle(
            corner_radius=1.6, width=13.0, height=4.6, stroke_color=GREY,
            stroke_width=4, fill_color=GREY, fill_opacity=0.04,
        ).move_to([0, 0.25, 0])
        texture = VGroup(*[
            Dot([x, y, 0], radius=0.11, color=GREY).set_opacity(0.42)
            for y, offset in ((2.00, 0.0), (2.28, 0.28))
            for x in np.linspace(-5.7 + offset, 5.7 + offset, 12)
        ]).set_z_index(-3)
        shell_group = VGroup(shell, texture)
        g.add(shell_group)
        g.shell = shell_group

    names = ("precursor", "early intermediate", "late intermediate", "product")
    nodes = VGroup(*[
        dark_chip(name, STEP_COLORS[i], 24).move_to([NODE_X[i], PATH_Y, 0])
        for i, name in enumerate(names)
    ])
    nodes[3][1].set_stroke(product_color).set_fill(product_color, 0.16)
    nodes[3][2].set_color(product_color)
    arrows = VGroup()
    for i in range(3):
        left = nodes[i].get_right() + RIGHT * 0.1
        right = nodes[i + 1].get_left() + LEFT * 0.1
        opacity = 0.22 if dim_after is not None and i >= dim_after else 1.0
        arrows.add(path_arrow(left, right, GREY, opacity=opacity))
    g.add(arrows, nodes)
    g.nodes, g.arrows = nodes, arrows

    if functions:
        badges = VGroup()
        for i, ar in enumerate(arrows):
            badges.add(dark_chip(f"function {i + 1}", BLUE if i % 2 == 0 else YELLOW, 24)
                       .move_to([ar.get_center()[0], 1.58, 0]))
        g.add(badges)
        g.badges = badges

    bars = VGroup(*[barrier(arrows[i].get_center()[0]) for i in blocks])
    g.add(bars)
    g.bars = bars

    if pile and blocks:
        bx = arrows[blocks[0]].get_center()[0] - 0.32
        heap = VGroup(*[
            Dot([bx - 0.18 * (i % 3), PATH_Y - 0.82 + 0.18 * (i // 3), 0], radius=0.09, color=BLUE)
            for i in range(6)
        ])
        heap_label = T("may accumulate", 24, BLUE).move_to([arrows[blocks[0]].get_center()[0] + 0.45, -0.75, 0])
        g.add(heap, heap_label)
        g.heap, g.heap_label = heap, heap_label

    if flow is not None:
        _x0, _x1, col = flow
        moving = VGroup(*[
            flow_dots(ar.get_start()[0] + 0.08, ar.get_end()[0] - 0.08,
                      color=col, n=1, speed=0.32)
            for ar in arrows
        ])
        moving.set_z_index(-1)
        g.add(moving)
        # Material travels behind the opaque pathway blocks, never through their lettering.
        g.remove(nodes)
        g.add(nodes)
        g.flow = moving

    gv = ValueTracker(gauge_value)
    gauge = dial(gv, center=[4.75, -1.35, 0], radius=0.78, label="growth",
                 color=GREEN, fmt="{:.0f}%", size=30)
    g.add(gauge)
    g.gauge, g.gauge_tracker = gauge, gv
    return g


def candidate_pair(world, drifting=False):
    early = dark_chip("early intermediate", BLUE, 26).move_to([-2.3, -1.55, 0])
    final = dark_chip("final product", GREEN, 26).move_to([2.35, -1.55, 0])
    if drifting:
        bob(early, amp=0.07, speed=1.7, seed=0)
        bob(final, amp=0.07, speed=1.7, seed=2)
    return VGroup(early, final)


def predict_backdrop(drifting=False):
    world = pathway_world(blocks=(2,), product_color=GREY, gauge_value=0.0, dim_after=2)
    candidates = candidate_pair(world, drifting=drifting)
    return VGroup(world, candidates)


def mini_path(y, block_index, results):
    """Compact carried geometry for the nested-rescue comparison."""
    xs = (-4.6, -1.55, 1.45, 4.45)
    nodes = VGroup(*[
        RoundedRectangle(corner_radius=0.12, width=1.35, height=0.48,
                         stroke_color=STEP_COLORS[i], stroke_width=3,
                         fill_color=STEP_COLORS[i], fill_opacity=0.12).move_to([x, y, 0])
        for i, x in enumerate(xs)
    ])
    arrows = VGroup(*[
        path_arrow(nodes[i].get_right() + RIGHT * 0.08,
                   nodes[i + 1].get_left() + LEFT * 0.08, GREY, width=4)
        for i in range(3)
    ])
    bar = barrier(arrows[block_index].get_center()[0], y).scale(0.55)
    marks = VGroup(*[
        Circle(radius=0.16, stroke_color=GREEN if ok else GREY, stroke_width=3,
               fill_color=GREEN if ok else BG, fill_opacity=0.45 if ok else 0.0)
        .move_to([xs[i], y - 0.53, 0])
        for i, ok in enumerate(results)
    ])
    return VGroup(arrows, nodes, bar, marks)


class S01Hook(TitleCard, SpokenScene):
    """The required first TitleCard scene uses its spoken time for the script's hook picture."""
    LESSON = "Complementation and gene function"
    TITLE = "Reading a Pathway Backward"

    def construct(self):
        world = pathway_world(gauge_value=0.7, flow=(NODE_X[0], NODE_X[3], TEXT))
        tag = scope_tag("schematic")
        self.play(FadeIn(world.shell), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(n, shift=RIGHT * 0.12) for n in world.nodes], lag_ratio=0.18),
                  LaggedStart(*[GrowArrow(a) for a in world.arrows], lag_ratio=0.22), run_time=1.7)
        self.add(world.flow)
        self.at("Can a supplied compound")
        question = T("Can a supply reveal the block?", 34, YELLOW, weight=BOLD).move_to([0, 3.2, 0])
        self.play(FadeIn(question, shift=DOWN * 0.15), run_time=0.65)
        self.at("Watch one cell build")
        self.play(FadeIn(world.nodes[3]), FadeIn(world.gauge), FadeIn(tag),
                  Indicate(world.nodes[3], color=GREEN, scale_factor=1.08), run_time=1.0)
        self.finish()


class S02Block(SpokenScene):
    def construct(self):
        world = pathway_world(blocks=(), product_color=YELLOW, gauge_value=0.72,
                              functions=True, flow=(NODE_X[0], NODE_X[3], TEXT))
        self.add(world.shell, world.arrows, world.nodes, world.gauge, world.flow, scope_tag("schematic"))
        self.at("Each arrow needs")
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.12) for b in world.badges], lag_ratio=0.25), run_time=1.6)
        self.at("A damaging mutation")
        block = barrier(world.arrows[1].get_center()[0])
        self.play(FadeIn(block, shift=DOWN * 0.5), run_time=0.7)
        world.flow.clear_updaters()
        self.play(FadeOut(world.flow), run_time=0.35)
        ready = flow_dots(world.arrows[2].get_start()[0] + 0.08,
                          world.arrows[2].get_end()[0] - 0.08,
                          color=GREY, n=3, speed=0.24, radius=0.11).set_z_index(-1)
        self.add(ready)
        heap_world = pathway_world(blocks=(1,), product_color=GREY, gauge_value=0.0,
                                   functions=True, pile=True, dim_after=1, cell=True)
        self.play(FadeIn(heap_world.heap), FadeIn(heap_world.heap_label),
                  world.nodes[3][1].animate.set_stroke(GREY).set_fill(GREY, 0.1),
                  world.nodes[3][2].animate.set_color(GREY), run_time=0.8)
        self.play(world.animate.scale(1.018), run_time=0.75, rate_func=there_and_back)
        self.at("The cell then lacks")
        self.play(world.gauge_tracker.animate.set_value(0.0), run_time=0.8)
        self.play(world.animate.scale(1.018), run_time=0.75, rate_func=there_and_back)
        self.at("every step after")
        for a in world.arrows[2:]:
            pulse(a, base=3.0, amp=1.2, speed=2.0)
        self.play(Indicate(world.arrows[2], color=GREY, scale_factor=1.03), run_time=0.7)
        self.play(world.animate.scale(1.018), run_time=0.75, rate_func=there_and_back)
        self.finish()


def dish(label, at, color=GREY, growth=False):
    rim = Ellipse(width=3.45, height=1.85, stroke_color=color, stroke_width=4,
                  fill_color=color, fill_opacity=0.08).move_to(at)
    broth = Ellipse(width=3.0, height=1.2, stroke_width=0,
                    fill_color=GREEN if growth else GREY, fill_opacity=0.3).move_to(at + DOWN * 0.12)
    lab = T(label, 28, color).next_to(rim, UP, buff=0.18)
    dots = VGroup(*[
        Dot(at + np.array([-0.9 + 0.3 * (i % 7), -0.35 + 0.28 * (i // 7), 0]),
            radius=0.06, color=GREEN)
        for i in range(14)
    ]) if growth else VGroup()
    return VGroup(rim, broth, dots, lab)


class S02Screen(SpokenScene):
    def construct(self):
        hidden = barrier(0, 1.8).scale(0.8)
        cover = dark_chip("mutant", RED, 30).move_to([0, 1.8, 0])
        self.play(FadeIn(hidden), FadeIn(cover), run_time=0.6)
        self.at("screen makes that hidden block visible")
        self.play(cover.animate.shift(UP * 1.0).set_opacity(0.25), Indicate(hidden, color=RED), run_time=0.8)
        complete = dish("complete medium", [-4.35, -0.35, 0], GREEN, True)
        minimal = dish("minimal medium", [0, -0.35, 0], GREY, False)
        candidate = dish("minimal + supply", [4.35, -0.35, 0], YELLOW, False)
        self.at("Keep each mutant alive")
        self.play(FadeOut(hidden), FadeOut(cover), FadeIn(complete, shift=UP * 0.2), run_time=0.85)
        self.at("then test minimal medium")
        self.play(FadeIn(minimal, shift=UP * 0.2), run_time=0.85)
        self.at("Adding candidate compounds separately")
        supply = dark_chip("candidate", YELLOW, 26).move_to([4.35, 2.25, 0])
        self.play(FadeIn(candidate, shift=UP * 0.2), FadeIn(supply), run_time=0.7)
        self.play(supply.animate.move_to([4.35, 0.05, 0]), run_time=1.1)
        unresolved = T("?", 46, TEXT).move_to([4.35, -0.3, 0])
        self.play(ReplacementTransform(supply, unresolved), run_time=0.45)
        dishes = VGroup(complete, minimal, candidate, unresolved)
        self.play(dishes.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        self.play(dishes.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        self.finish()


class S03Upstream(SpokenScene):
    def construct(self):
        world = pathway_world(blocks=(1,), product_color=GREY, gauge_value=0.0,
                              pile=True, dim_after=1)
        self.add(world, scope_tag("schematic"))
        supply = dark_chip("upstream supply", BLUE, 28).move_to([-4.35, -1.35, 0])
        self.at("Add an upstream intermediate")
        self.play(FadeIn(supply, shift=UP * 0.2), run_time=0.6)
        self.play(world.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        self.at("It enters before")
        self.play(supply.animate.move_to(world.nodes[1].get_center() + DOWN * 0.72), run_time=0.7)
        moving = Dot(world.nodes[1].get_right() + RIGHT * 0.14, radius=0.13, color=BLUE).set_z_index(-1)
        self.play(ReplacementTransform(supply, moving), run_time=0.3)
        self.play(moving.animate.move_to(world.bars[0].get_center() + LEFT * 0.48), run_time=0.9)
        self.play(world.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        self.at("Nothing arrives downstream")
        self.play(FadeOut(moving), Indicate(world.nodes[2], color=GREY, scale_factor=1.05), run_time=0.7)
        self.at("growth gauge stays dark")
        no = dark_chip("no growth", RED, 30).move_to([0, -1.55, 0])
        self.play(FadeIn(no), Indicate(world.gauge, color=RED), run_time=0.65)
        self.at("Failure to rescue")
        conclusion = caption("This supply did not bypass the block.", color=RED)
        self.play(swap(no, conclusion), run_time=0.75)
        self.play(world.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        self.play(world.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        self.finish()


class S04Downstream(SpokenScene):
    def construct(self):
        world = pathway_world(blocks=(1,), product_color=GREY, gauge_value=0.0, dim_after=1)
        self.add(world, scope_tag("schematic"))
        supply = dark_chip("downstream supply", YELLOW, 28).move_to([1.65, -1.45, 0])
        self.at("Now add a downstream intermediate")
        self.play(FadeIn(supply, shift=UP * 0.2), run_time=0.6)
        bob(supply, amp=0.08, speed=1.8)
        self.at("It enters beyond")
        supply.clear_updaters()
        self.play(supply.animate.move_to(world.nodes[2].get_center() + DOWN * 0.72), run_time=0.8)
        moving = RoundedRectangle(corner_radius=0.08, width=0.46, height=0.46,
                                  stroke_color=YELLOW, stroke_width=3,
                                  fill_color=YELLOW, fill_opacity=0.65)
        moving.move_to(world.nodes[2].get_right() + RIGHT * 0.14).set_z_index(-1)
        self.play(ReplacementTransform(supply, moving), run_time=0.3)
        self.play(world.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        self.at("later functions convert")
        self.play(moving.animate.move_to(world.nodes[3].get_left() + LEFT * 0.35), run_time=1.0)
        self.play(world.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        self.play(FadeOut(moving), world.nodes[3][1].animate.set_stroke(GREEN).set_fill(GREEN, 0.18),
                  world.nodes[3][2].animate.set_color(GREEN), run_time=0.5)
        self.at("growth returns")
        self.play(world.gauge_tracker.animate.set_value(0.82), run_time=0.9)
        self.play(world.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        self.at("Rescue places the block")
        bracket = Brace(Line([NODE_X[0], -0.65, 0], [NODE_X[2], -0.65, 0]), DOWN, color=RED)
        label = T("block lies before here", 28, RED).next_to(bracket, DOWN, buff=0.12)
        self.play(GrowFromCenter(bracket), FadeIn(label), run_time=0.75)
        self.play(world.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        back = predict_backdrop()
        world, candidates = back
        self.add(world, scope_tag("schematic"))
        self.at("new mutant blocks the last arrow")
        self.play(FadeIn(world.bars[0], shift=DOWN * 0.4), run_time=0.65)
        self.at("Which supply can restore growth")
        self.play(FadeIn(candidates[0], shift=UP * 0.15), FadeIn(candidates[1], shift=UP * 0.15), run_time=0.7)
        q = question_card("Which restores growth?")
        self.play(FadeIn(q.question), run_time=0.65)
        self.at("Trace each root")
        self.play(Indicate(candidates[0], color=BLUE), Indicate(candidates[1], color=GREEN), run_time=0.8)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Which restores growth?"
    OPTIONS = []
    SECONDS = 4.5

    def backdrop(self):
        return predict_backdrop(drifting=True)


class S06Reveal(SpokenScene):
    def construct(self):
        world = pathway_world(blocks=(2,), product_color=GREY, gauge_value=0.0, dim_after=2)
        self.add(world, scope_tag("schematic"))
        early = dark_chip("early intermediate", BLUE, 27).move_to([-2.3, -1.45, 0])
        final = dark_chip("final product", GREEN, 27).move_to([2.35, -1.45, 0])
        self.add(early, final)
        self.at("early intermediate still meets")
        self.play(early.animate.move_to(world.nodes[1].get_center() + DOWN * 0.7), run_time=0.5)
        bead = Dot(world.nodes[1].get_right() + RIGHT * 0.14, radius=0.13, color=BLUE).set_z_index(-1)
        self.play(ReplacementTransform(early, bead), run_time=0.25)
        self.play(bead.animate.move_to(world.bars[0].get_center() + LEFT * 0.28), run_time=0.85)
        self.at("cannot rescue")
        no = dark_chip("no growth", RED, 28).move_to([0, -1.5, 0])
        self.play(FadeOut(bead), FadeIn(no), run_time=0.5)
        self.at("final product needs no remaining conversion")
        self.play(FadeOut(no), final.animate.move_to(world.nodes[3].get_center() + DOWN * 1.0 + LEFT * 0.5), run_time=0.9)
        self.at("restores growth")
        self.play(FadeOut(final),
                  world.nodes[3][1].animate.set_stroke(GREEN).set_fill(GREEN, 0.18),
                  world.nodes[3][2].animate.set_color(GREEN),
                  world.gauge_tracker.animate.set_value(0.85), run_time=0.9)
        self.play(world.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        self.at("entered after every block step")
        entry = SurroundingRectangle(world.nodes[3], color=GREEN, buff=0.14, stroke_width=5)
        label = T("after the block", 28, GREEN).move_to([4.6, 3.12, 0])
        self.play(Create(entry), FadeIn(label), run_time=0.65)
        self.play(world.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        self.finish()


class S07Rows(SpokenScene):
    def construct(self):
        heading = T("supplies enter →", 30, TEXT).move_to([0, 3.2, 0])
        self.play(FadeIn(heading), run_time=0.45)
        early = mini_path(1.75, 0, (False, True, True, True))
        middle = mini_path(0.0, 1, (False, False, True, True))
        late = mini_path(-1.75, 2, (False, False, False, True))
        labels = [T("early block", 28, BLUE), T("middle block", 28, YELLOW), T("late block", 28, RED)]
        for lab, row in zip(labels, (early, middle, late)):
            lab.move_to([-5.25, row.get_center()[1] + 0.68, 0])
        self.at("Compare several mutants")
        self.play(FadeIn(early[:-1]), FadeIn(labels[0]), run_time=0.65)
        self.at("early block is rescued")
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in early[-1]], lag_ratio=0.15), run_time=0.8)
        self.play(early.animate.scale(1.025), run_time=0.7, rate_func=there_and_back)
        self.at("middle block has fewer options")
        self.play(FadeIn(middle[:-1]), FadeIn(labels[1]),
                  LaggedStart(*[FadeIn(m, scale=0.5) for m in middle[-1]], lag_ratio=0.15), run_time=0.9)
        self.at("late block may accept only")
        self.play(FadeIn(late[:-1]), FadeIn(labels[2]),
                  LaggedStart(*[FadeIn(m, scale=0.5) for m in late[-1]], lag_ratio=0.15), run_time=0.9)
        self.at("Nested rescue patterns")
        rule = caption("more rescue = earlier block", color=GREEN)
        self.play(FadeIn(rule), run_time=0.65)
        self.play(Indicate(VGroup(early[-1], middle[-1], late[-1]), color=GREEN, scale_factor=1.04), run_time=0.8)
        self.finish()


class S08Limits(SpokenScene):
    def construct(self):
        world = pathway_world(gauge_value=0.0, cell=True)
        self.add(world.shell, world.arrows, world.nodes, scope_tag("schematic"))
        assumptions = T("assumptions", 34, TEXT, weight=BOLD).move_to([0, 3.15, 0])
        self.play(FadeIn(assumptions), run_time=0.5)
        gate_x = world.shell.get_left()[0] + 0.5
        gate = VGroup(Line([gate_x, -0.65, 0], [gate_x, 0.1, 0], color=BLUE, stroke_width=9),
                      Line([gate_x, 0.85, 0], [gate_x, 1.55, 0], color=BLUE, stroke_width=9))
        supply = dark_chip("usable supply", BLUE, 26).move_to([-4.35, -1.25, 0])
        self.at("supplied compound must enter")
        self.play(FadeIn(gate), FadeIn(supply), run_time=0.55)
        self.play(supply.animate.move_to([-4.55, -1.25, 0]), run_time=0.8)
        self.at("pathway must behave like the tested chain")
        caution = RoundedRectangle(corner_radius=0.16, width=3.4, height=1.45,
                                   stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08)
        caution.move_to([3.9, -1.35, 0])
        branch = VGroup(Line([3.05, -1.62, 0], [3.75, -1.38, 0], color=GREY),
                        Line([3.05, -1.62, 0], [3.75, -1.86, 0], color=GREY))
        diff = T("different model", 26, GREY).move_to([3.9, -0.95, 0])
        self.play(FadeOut(world.gauge), run_time=0.3)
        self.play(FadeIn(caution), Create(branch), FadeIn(diff), run_time=0.55)
        self.at("rescue class can contain several genes")
        self.play(FadeOut(caution), FadeOut(branch), FadeOut(diff), FadeOut(supply), run_time=0.35)
        badges = VGroup(*[dark_chip(f"function {i + 1}", BLUE if i % 2 == 0 else YELLOW, 24)
                          for i in range(3)]).arrange(RIGHT, buff=0.2).move_to([0, -1.25, 0])
        bracket = Brace(badges, DOWN, color=TEXT)
        label = T("one rescue class", 28, TEXT).next_to(bracket, DOWN, buff=0.1)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.12) for b in badges], lag_ratio=0.25), run_time=1.0)
        self.play(GrowFromCenter(bracket), FadeIn(label), run_time=0.6)
        final_group = VGroup(world.shell, world.arrows, world.nodes, badges, bracket, label)
        self.play(final_group.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        self.play(final_group.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        self.finish()


class S08DoubleBlock(SpokenScene):
    def construct(self):
        world = pathway_world(blocks=(0, 2), product_color=GREY, gauge_value=0.0, dim_after=0)
        self.add(world, scope_tag("schematic"))
        self.at("more than one block")
        self.play(Indicate(world.bars, color=RED, scale_factor=1.05), run_time=0.65)
        self.play(world.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        supply = dark_chip("early supply", BLUE, 28).move_to([-1.8, -1.45, 0])
        self.at("early supply may bypass the first barrier")
        self.play(FadeIn(supply), supply.animate.move_to(world.nodes[1].get_center() + DOWN * 0.7), run_time=0.75)
        self.play(world.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        bead = Dot(world.nodes[1].get_right() + RIGHT * 0.14, radius=0.13, color=BLUE).set_z_index(-1)
        self.play(ReplacementTransform(supply, bead), run_time=0.25)
        self.at("stop at a later one")
        self.play(bead.animate.move_to(world.bars[1].get_center() + LEFT * 0.28), run_time=0.85)
        self.play(FadeOut(bead), Indicate(world.gauge, color=RED), run_time=0.45)
        self.at("Growth returns only when")
        product = dark_chip("final product", GREEN, 28).move_to([2.4, -1.45, 0])
        self.play(FadeIn(product), run_time=0.4)
        self.at("enters after every remaining block")
        self.play(product.animate.move_to(world.nodes[3].get_center() + DOWN * 1.0 + LEFT * 0.5),
                  world.gauge_tracker.animate.set_value(0.88), run_time=1.0)
        self.play(FadeOut(product),
                  world.nodes[3][1].animate.set_stroke(GREEN).set_fill(GREEN, 0.18),
                  world.nodes[3][2].animate.set_color(GREEN), run_time=0.35)
        self.finish()


def chromosome_panel():
    bars = VGroup(
        RoundedRectangle(corner_radius=0.18, width=4.8, height=0.45, stroke_color=GREY,
                         fill_color=GREY, fill_opacity=0.25).move_to([0, 0.65, 0]),
        RoundedRectangle(corner_radius=0.18, width=4.8, height=0.45, stroke_color=GREY,
                         fill_color=GREY, fill_opacity=0.25).move_to([0, -0.65, 0]),
    )
    dots = VGroup(*[
        Dot([x, y, 0], radius=0.2, color=c)
        for x, y, c in ((-1.25, 0.65, BLUE), (-0.7, -0.65, BLUE),
                        (0.85, 0.65, YELLOW), (1.35, -0.65, YELLOW))
    ])
    groups = VGroup(
        DashedVMobject(Ellipse(width=2.15, height=2.05, color=BLUE, stroke_width=4), num_dashes=30).move_to([-0.95, 0, 0]),
        DashedVMobject(Ellipse(width=2.15, height=2.05, color=YELLOW, stroke_width=4), num_dashes=30).move_to([1.1, 0, 0]),
    )
    return VGroup(bars, dots, groups)


def staircase_panel():
    rows = VGroup(mini_path(0.95, 0, (False, True, True, True)),
                  mini_path(0.0, 1, (False, False, True, True)),
                  mini_path(-0.95, 2, (False, False, False, True)))
    rows.scale(0.48)
    return rows


class S09Bridge(SpokenScene):
    def construct(self):
        heading = T("rescue questions", 34, TEXT, weight=BOLD).move_to([0, 3.35, 0])
        panels = TwoPanel("complementation groups", "rescue classes", colors=(BLUE, YELLOW), top=2.85)
        left, right = chromosome_panel(), staircase_panel()
        panels.put(left, "left")
        panels.put(right, "right")
        self.at("related rescue questions")
        self.play(FadeIn(heading), FadeIn(panels), run_time=0.8)
        self.at("their groups differ")
        self.play(FadeIn(left), FadeIn(right), run_time=0.8)
        self.at("sort mutations by shared function")
        ll = T("shared function", 28, BLUE).move_to([-3.25, -2.05, 0])
        self.play(FadeIn(ll), Indicate(left[2], color=BLUE, scale_factor=1.05), run_time=0.8)
        self.at("sort blocks by pathway position")
        rr = T("pathway position", 28, YELLOW).move_to([3.25, -2.05, 0])
        self.play(FadeIn(rr), Indicate(right, color=YELLOW, scale_factor=1.03), run_time=0.8)
        self.at("Keeping those readouts separate")
        divider = Line([0, -2.45, 0], [0, 2.65, 0], color=TEXT, stroke_width=4)
        self.play(Create(divider), run_time=0.55)
        self.play(VGroup(panels, left, right, ll, rr, divider).animate.scale(1.012),
                  run_time=1.0, rate_func=there_and_back)
        self.play(VGroup(panels, left, right, ll, rr, divider).animate.scale(1.012),
                  run_time=1.0, rate_func=there_and_back)
        self.play(VGroup(panels, left, right, ll, rr, divider).animate.scale(1.012),
                  run_time=1.0, rate_func=there_and_back)
        self.finish()


class S09Measurement(SpokenScene):
    def construct(self):
        world = pathway_world(product_color=GREY, gauge_value=0.0, dim_after=1)
        self.add(world.shell, world.arrows, world.nodes, scope_tag("schematic"))
        broad = Brace(Line([-1.0, -0.65, 0], [3.3, -0.65, 0]), DOWN, color=RED)
        broad_lab = T("possible block region", 28, RED).next_to(broad, DOWN, buff=0.12)
        self.at("Rescue narrows the possibilities")
        self.play(GrowFromCenter(broad), FadeIn(broad_lab), run_time=0.7)
        self.play(world.animate.scale(1.018), run_time=0.7, rate_func=there_and_back)
        self.at("does not expose the broken reaction directly")
        scan = RoundedRectangle(corner_radius=0.08, width=0.34, height=1.25,
                                stroke_color=RED, stroke_width=3,
                                fill_color=RED, fill_opacity=0.22).move_to([-0.75, 1.55, 0])
        self.play(FadeIn(scan), run_time=0.25)
        self.play(scan.animate.move_to([3.0, 1.55, 0]),
                  world.animate.scale(1.018), run_time=1.55, rate_func=there_and_back)
        self.play(scan.animate.move_to([3.0, 1.55, 0]),
                  world.animate.scale(1.018), run_time=1.55, rate_func=there_and_back)
        self.play(FadeOut(scan), run_time=0.25)
        self.at("test more intermediates")
        entry = dark_chip("new supply", YELLOW, 26).move_to([1.65, 2.05, 0])
        self.play(FadeIn(entry), entry.animate.move_to([1.65, 1.25, 0]), run_time=0.75)
        narrow = Brace(Line([0.15, -0.65, 0], [2.9, -0.65, 0]), DOWN, color=RED)
        narrow_lab = T("still a region", 28, RED).next_to(narrow, DOWN, buff=0.12).shift(RIGHT * 0.3)
        self.play(ReplacementTransform(broad, narrow), swap(broad_lab, narrow_lab), run_time=0.8)
        self.at("Measure accumulated compounds")
        tube = VGroup(
            RoundedRectangle(corner_radius=0.18, width=0.85, height=2.0,
                             stroke_color=TEXT, stroke_width=4),
            Rectangle(width=0.72, height=0.65, stroke_width=0,
                      fill_color=BLUE, fill_opacity=0.45).shift(DOWN * 0.55),
        ).move_to([-4.05, -0.95, 0])
        tube_lab = T("measure accumulation", 28, TEXT).next_to(tube, RIGHT, buff=0.25)
        self.play(FadeIn(tube, shift=UP * 0.15), FadeIn(tube_lab), run_time=0.7)
        bob(tube, amp=0.04, speed=2)
        self.finish()


class S10End(EndCard):
    LINE = "A usable supplement rescues only by entering after the blocked step."
