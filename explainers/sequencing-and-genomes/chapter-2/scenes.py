"""When Reads Become a Genome — chapter 2 explainer.

COLOR MAP (kept throughout both chapters)
  BLUE  = genome and reference paths
  GOLD  = reads
  RED   = repeats
  TEAL  = reversible or adjustable features
  GREEN = confirmed placement or signal
  GREY  = uncertainty and de-emphasis
"""
from bp_parts import *  # noqa: F401,F403


# Shared geometry. Every continuing scene rebuilds these exact coordinates.
RIBBON_Y = -0.35
RIBBON_X0, RIBBON_X1 = -5.9, 5.9
REPEAT_CENTERS = (-3.0, 2.25)
REPEAT_W = 1.55


def stage_panel():
    """Shared landscape ground; its quiet shimmer keeps the carried world alive."""
    panel = RoundedRectangle(corner_radius=0.28, width=12.55, height=6.35,
                             stroke_width=0, fill_color=GREY, fill_opacity=0.18)
    panel.move_to([0, -0.05, 0]).set_z_index(-8)
    panel._phase = 0.0

    def shimmer(mob, dt):
        mob._phase += dt
        mob.set_fill(opacity=0.18 + 0.04 * np.sin(5.0 * mob._phase))
    panel.add_updater(shimmer)
    return panel


def read_bar(width=1.1, height=0.30, color=GOLD):
    return RoundedRectangle(
        corner_radius=0.09, width=width, height=height,
        stroke_color=color, stroke_width=2.5,
        fill_color=color, fill_opacity=0.78,
    )


def cartoon_tag(text="schematic"):
    """A fixed tag that also leaves the encode-time Hex mark clear."""
    return T(text, 24, GREY).move_to([-5.75, -3.42, 0], aligned_edge=LEFT)


def genome_world(y=RIBBON_Y):
    ribbon = RoundedRectangle(corner_radius=0.18, width=RIBBON_X1 - RIBBON_X0,
                              height=0.62, stroke_color=BLUE, stroke_width=3,
                              fill_color=BLUE, fill_opacity=0.82).move_to([0, y, 0])
    return ribbon


def repeat_world(with_questions=False, waiting=False, y=RIBBON_Y):
    """The carried exact-repeat picture used in s05–s08."""
    ribbon = genome_world(y)
    repeats = VGroup(*[
        RoundedRectangle(corner_radius=0.08, width=REPEAT_W, height=1.05,
                         stroke_color=RED, stroke_width=4,
                         fill_color=RED, fill_opacity=0.72).move_to([x, y, 0])
        for x in REPEAT_CENTERS
    ])
    world = VGroup(ribbon, repeats)
    world.ribbon, world.repeats = ribbon, repeats
    if with_questions:
        qs = VGroup(
            T("?", 54, GREY, weight=BOLD).move_to([-1.35, y + 0.9, 0]),
            T("?", 54, GREY, weight=BOLD).move_to([0.62, y + 0.9, 0]),
        )
        world.add(qs)
        world.questions = qs
    if waiting:
        pile = VGroup(*[read_bar(0.95).move_to([0, 1.05 + 0.34 * i, 0]) for i in range(5)])
        world.add(pile)
        world.pile = pile
    return world


def reference_graph(extra_branch=True, many=False):
    """The carried reference/pangenome graph used in s09–s11."""
    left = Line([-5.8, 0.15, 0], [-2.2, 0.15, 0], color=BLUE, stroke_width=24)
    right = Line([2.2, 0.15, 0], [5.8, 0.15, 0], color=BLUE, stroke_width=24)
    main = Line([-2.2, 0.15, 0], [2.2, 0.15, 0], color=BLUE, stroke_width=24)
    paths = VGroup(left, main, right)
    upper = VMobject(color=BLUE, stroke_width=20)
    upper.set_points_smoothly([[-2.2, 0.15, 0], [-1.35, 1.45, 0], [1.25, 1.45, 0], [2.2, 0.15, 0]])
    if extra_branch:
        paths.add(upper)
    lower = None
    if many:
        lower = VMobject(color=BLUE, stroke_width=18)
        lower.set_points_smoothly([[-2.2, 0.15, 0], [-1.3, -1.1, 0], [1.2, -1.1, 0], [2.2, 0.15, 0]])
        paths.add(lower)
    paths.main, paths.upper, paths.lower = main, upper, lower
    return paths


def waiting_prediction_world():
    world = repeat_world(with_questions=True, waiting=True)
    bob(world.pile, amp=0.08, speed=1.5, seed=2)
    pulse(world.repeats[0], base=4.0, amp=1.2, speed=2.5)
    pulse(world.repeats[1], base=4.0, amp=1.2, speed=2.5)
    group = VGroup(stage_panel(), world, cartoon_tag())
    group.world = world
    return group


class S01Hook(SpokenScene):
    def construct(self):
        self.add(stage_panel())
        ribbon = genome_world()
        tag = cartoon_tag()
        self.play(Create(ribbon), FadeIn(tag), run_time=0.8)

        starts = [-5.0, -3.55, -1.8, 0.25, 2.0, 4.25]
        reads = VGroup(*[read_bar(1.18).move_to([x, 3.0 + 0.18 * (i % 2), 0])
                         for i, x in enumerate(starts)])
        targets = [np.array([x, RIBBON_Y + 0.42 + 0.32 * (i % 2), 0]) for i, x in enumerate(starts)]
        self.play(*[r.animate.move_to(p) for r, p in zip(reads, targets)],
                  run_time=2.4, rate_func=linear)

        self.at("How do millions")
        question = fit_text("How do reads become one genome?", max_w=10.5, size=46,
                            color=TEXT, min_size=32).move_to([0, 2.65, 0])
        self.play(FadeIn(question, shift=UP * 0.12), run_time=0.55)

        self.at("Some overlap unique")
        settled = VGroup(*[SurroundingRectangle(reads[i], color=GREEN, buff=0.08,
                                                corner_radius=0.08, stroke_width=4)
                           for i in (0, 1, 4)])
        self.play(FadeIn(settled), run_time=0.55)

        self.at("Others seem to fit")
        ambiguous = read_bar(1.15).move_to([0.5, 1.35, 0])
        qmarks = VGroup(T("?", 54, GREY).move_to([-0.9, 1.0, 0]),
                        T("?", 54, GREY).move_to([2.0, 1.0, 0]))
        self.play(FadeIn(ambiguous), FadeIn(qmarks), run_time=0.55)
        bob(ambiguous, amp=0.09, speed=1.7)

        self.at("The computer must separate")
        missing = boxed_label("missing evidence", GREY, size=28).move_to([-3.55, -2.0, 0])
        unplaced = boxed_label("cannot be placed", GREY, size=28).move_to([3.3, -2.0, 0])
        self.play(FadeOut(question), FadeIn(missing), FadeIn(unplaced), run_time=0.7)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Sequencing and Genomes"
    TITLE = "When Reads Become a Genome"

    def construct(self):
        self.add(stage_panel())
        ribbon = genome_world()
        reads = VGroup(*[read_bar(1.1).move_to([x, RIBBON_Y + 0.45 + 0.28 * (i % 2), 0])
                         for i, x in enumerate([-5.0, -3.5, -1.8, 0.25, 2.0, 4.2])])
        bob(reads, amp=0.05, speed=1.4)
        veil = Rectangle(width=12.5, height=3.0, stroke_width=0,
                         fill_color=BG, fill_opacity=0.82).move_to([0, 1.2, 0])
        title = T(self.TITLE, 52, font=TITLE_FONT)
        fit(title, max_w=11.3)
        lesson = T(self.LESSON.upper(), 22, GREY)
        rule = Line(LEFT * 1.3, RIGHT * 1.3, color=GOLD, stroke_width=4)
        card = VGroup(lesson, title, rule).arrange(DOWN, buff=0.32).move_to([0, 1.25, 0])
        self.add(ribbon, reads, cartoon_tag())
        self.play(FadeIn(veil), FadeIn(lesson), Write(title), GrowFromCenter(rule), run_time=0.75)
        self.wait(0.55)
        self.play(FadeOut(VGroup(veil, card)), run_time=0.45)
        self.finish()


class S03Coverage(SpokenScene):
    def construct(self):
        self.add(stage_panel())
        y = -2.35
        ribbon = genome_world(y)
        tag = cartoon_tag()
        self.play(Create(ribbon), FadeIn(tag), run_time=0.7)

        xs = [-5.25, -4.55, -3.8, -3.1, -2.35, -1.6, -0.85,
              0.65, 1.4, 2.15, 2.9, 3.65, 4.4, 5.1]
        heights = [2, 4, 3, 6, 2, 5, 3, 1, 5, 3, 6, 2, 4, 3]
        stacks = VGroup()
        for x, n in zip(xs, heights):
            for lane in range(n):
                stacks.add(read_bar(0.64, 0.19).move_to([x, y + 0.32 + lane * 0.27, 0]))
        for r in stacks:
            r.save_state()
            r.shift(UP * (4.8 + 0.25 * (int(abs(r.get_x()) * 10) % 3)))

        self.at("Coverage is the mean")
        mean = T("mean coverage", 34, GOLD).move_to([0, 2.9, 0])
        self.play(FadeIn(mean), run_time=0.4)

        self.at("As more gold reads")
        self.play(FadeOut(mean), run_time=0.25)
        self.play(LaggedStart(*[Restore(r) for r in stacks], lag_ratio=0.018),
                  run_time=4.0, rate_func=linear)

        self.at("blue gaps shrink")
        gap = VGroup(
            DashedLine([-0.12, y - 0.35, 0], [-0.12, 1.85, 0], color=GREY, stroke_width=3),
            T("uncovered", 28, GREY).move_to([-0.12, 2.15, 0]),
        )
        self.play(FadeIn(gap), FadeIn(mean), run_time=0.5)

        self.at("The mean does not")
        unequal = T("not uniform coverage", 30, GREY).move_to([3.8, 2.8, 0])
        self.play(FadeIn(unequal), run_time=0.45)

        self.at("many reads")
        many = T("many", 28, GOLD).move_to([-3.1, -3.05, 0])
        self.play(FadeIn(many), Indicate(stacks, color=GOLD, scale_factor=1.0), run_time=0.7)
        self.at("few reads")
        few = T("few", 28, GOLD).move_to([0.65, -3.05, 0])
        self.play(FadeIn(few), run_time=0.35)
        self.at("or none")
        none = T("none", 28, GREY).move_to([-0.12, -3.05, 0])
        self.play(FadeOut(few), FadeIn(none), run_time=0.35)
        pulse(ribbon, base=18, amp=1.2, speed=1.8)
        self.finish()


class S04Random(SpokenScene):
    def construct(self):
        self.add(stage_panel())
        fn = lambda c: float(np.exp(-c))
        plot = Plot(box=(-5.55, 2.4, -2.05, 2.35), xr=(0, 6), yr=(0, 1),
                    xticks=[0, 2, 4, 6], yticks=[(0, "0"), (0.5, "0.5"), (1, "1")],
                    xlabel="mean coverage", ylabel="fraction unread", label_size=28)
        c = ValueTracker(0.3)
        curve = plot.live_curve(fn, c, color=GREY, width=7)
        dot = plot.dot(lambda: c.get_value(), lambda: fn(c.get_value()), color=GOLD, ring=GOLD)
        readout = Readout([
            ("coverage", lambda: c.get_value(), "{:4.1f}", GOLD),
            ("unread", lambda: fn(c.get_value()), "{:5.3f}", GREY),
        ], at=[4.15, 0.15, 0], widest=[6.0, 1.0], title="ideal sampling", size=25, pad=0.22)
        self.play(Create(plot), run_time=0.8)
        self.add(curve, dot, cartoon_tag("computed"))

        self.at("the unread fraction")
        self.play(FadeIn(readout), c.animate.set_value(3.0), run_time=3.3, rate_func=linear)

        self.at("Adding reads")
        self.play(c.animate.set_value(5.8), run_time=2.5, rate_func=linear)

        self.at("It makes an unseen")
        low = T("less likely", 34, GREY).move_to([4.15, -1.75, 0])
        self.play(FadeIn(low, shift=DOWN * 0.1), run_time=0.5)

        self.at("although real libraries")
        xs = np.linspace(0, 6, 80)
        top = [plot.pt(x, min(1, fn(x) + 0.09 + 0.02 * x)) for x in xs]
        bottom = [plot.pt(x, max(0, fn(x) - 0.05)) for x in xs[::-1]]
        band = Polygon(*(top + bottom), stroke_width=0, fill_color=GREY, fill_opacity=0.18)
        badge = boxed_label("real libraries: less even", GREY, size=26).move_to([4.55, 2.55, 0])
        self.play(FadeIn(band), FadeIn(badge), run_time=0.65)
        pulse(band, base=0.1, amp=0.05, speed=1.5)
        self.finish()


class S05Repeat(SpokenScene):
    def construct(self):
        self.add(stage_panel())
        world = repeat_world()
        self.play(Create(world.ribbon), FadeIn(cartoon_tag("exact-repeat model · schematic")), run_time=0.7)

        self.at("the same red repeat")
        self.play(FadeIn(world.repeats[0]), FadeIn(world.repeats[1]), run_time=0.8)

        self.at("A short gold read")
        short = read_bar(0.92, 0.28).move_to([0, 2.15, 0])
        self.play(FadeIn(short, shift=DOWN * 0.2), run_time=0.45)

        self.at("matches both places")
        left = short.copy().move_to([REPEAT_CENTERS[0], RIBBON_Y + 0.58, 0])
        right = short.copy().move_to([REPEAT_CENTERS[1], RIBBON_Y + 0.58, 0])
        glows = VGroup(*[SurroundingRectangle(r, color=GREEN, buff=0.1,
                                             corner_radius=0.08, stroke_width=5)
                         for r in world.repeats])
        self.play(ReplacementTransform(short, left), FadeIn(right), FadeIn(glows), run_time=1.0)
        pulse(glows[0], base=5, amp=1.3, speed=2.0)
        pulse(glows[1], base=5, amp=1.3, speed=2.0)

        self.at("Its bases may be accurate")
        accurate = boxed_label("accurate bases", GOLD, size=28).move_to([0, 2.2, 0])
        self.play(FadeIn(accurate), run_time=0.45)
        self.at("address is ambiguous")
        ambiguous = boxed_label("ambiguous address", GREY, size=28).move_to([0, 1.35, 0])
        self.play(FadeIn(ambiguous), run_time=0.45)

        self.at("More copies")
        copies = VGroup(*[read_bar(0.92, 0.2).move_to([0, 2.55 + 0.27 * i, 0]) for i in range(3)])
        self.play(FadeOut(accurate), run_time=0.25)
        self.play(FadeIn(copies, lag_ratio=0.12), run_time=0.65)
        bob(copies, amp=0.05, speed=1.5)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        world = waiting_prediction_world()
        self.add(world)
        self.at("Another pile")
        self.play(LaggedStart(*[Indicate(r, color=GOLD, scale_factor=1.05)
                                for r in world.world.pile], lag_ratio=0.08), run_time=1.8)
        self.at("Will a deeper pile")
        question = question_card("Will a deeper pile tell which flanking regions belong together?",
                                 size=30, max_w=10.6)
        self.play(FadeIn(question.question), run_time=0.6)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Will a deeper pile tell which flanking regions belong together?"
    SECONDS = 4.5

    def backdrop(self):
        return waiting_prediction_world()


class S08Span(SpokenScene):
    def construct(self):
        self.add(stage_panel())
        world = repeat_world(with_questions=True, waiting=True)
        self.add(world, cartoon_tag())
        bob(world.pile, amp=0.06, speed=1.5)

        self.at("The pile grows")
        extra = VGroup(*[read_bar(0.95).move_to([0, 2.75 + 0.28 * i, 0]) for i in range(2)])
        self.play(FadeIn(extra, lag_ratio=0.15), run_time=0.7)

        self.at("both placements remain")
        placed_l = world.pile.copy().arrange(DOWN, buff=0.1).move_to([REPEAT_CENTERS[0], 1.35, 0])
        placed_r = world.pile.copy().arrange(DOWN, buff=0.1).move_to([REPEAT_CENTERS[1], 1.35, 0])
        glow_l = SurroundingRectangle(world.repeats[0], color=GREEN, buff=0.1, corner_radius=0.08)
        glow_r = SurroundingRectangle(world.repeats[1], color=GREEN, buff=0.1, corner_radius=0.08)
        self.play(FadeOut(world.questions), run_time=0.25)
        self.play(FadeOut(VGroup(world.pile, extra)), FadeIn(placed_l), FadeIn(placed_r),
                  FadeIn(glow_l), FadeIn(glow_r), run_time=1.1)

        self.at("More reeds fill")
        sampling = T("sampling gaps", 30, GREY).move_to([-4.55, 2.75, 0])
        self.play(FadeIn(sampling), run_time=0.4)

        self.at("reeds that span")
        spanning = T("span the repeat", 32, GOLD).move_to([-4.55, 2.75, 0])
        self.play(swap(sampling, spanning), run_time=0.6)

        self.at("one long gold")
        long_read = read_bar(4.25, 0.3).move_to([REPEAT_CENTERS[0], RIBBON_Y + 0.82, 0])
        self.play(FadeOut(VGroup(placed_l, placed_r, glow_l, glow_r)),
                  FadeIn(long_read, shift=DOWN * 0.2), run_time=0.9)

        self.at("reaches blue unique")
        flank_l = SurroundingRectangle(
            Rectangle(width=1.25, height=0.55).move_to([-4.4, RIBBON_Y, 0]),
            color=GREEN, buff=0.03, stroke_width=5)
        flank_r = SurroundingRectangle(
            Rectangle(width=1.25, height=0.55).move_to([-1.6, RIBBON_Y, 0]),
            color=GREEN, buff=0.03, stroke_width=5)
        self.play(Create(flank_l), Create(flank_r), run_time=0.8)

        self.at("That span links")
        confirmed = boxed_label("repeat linked to its flanks", GREEN, size=28).move_to([0, -2.1, 0])
        self.play(FadeIn(confirmed), Indicate(long_read, color=GOLD, scale_factor=1.0), run_time=0.7)
        pulse(long_read, base=2.5, amp=0.8, speed=2.0)
        self.finish()


class S09Reference(SpokenScene):
    def construct(self):
        self.add(stage_panel())
        ribbon = genome_world()
        repeat = RoundedRectangle(corner_radius=0.08, width=REPEAT_W, height=1.05,
                                  stroke_color=RED, stroke_width=4, fill_color=RED,
                                  fill_opacity=0.72).move_to([REPEAT_CENTERS[0], RIBBON_Y, 0])
        span = read_bar(4.25, 0.3).move_to([REPEAT_CENTERS[0], RIBBON_Y + 0.82, 0])
        self.add(ribbon, repeat, span, cartoon_tag("graph · schematic"))

        self.at("De novo assembly")
        contigs = VGroup(*[read_bar(2.2).move_to([-3.9 + 2.05 * i, 0.2 + 0.36 * (i % 2), 0])
                           for i in range(5)])
        de_novo = T("de novo assembly", 32, GOLD).move_to([0, 2.8, 0])
        self.play(FadeOut(VGroup(ribbon, repeat, span)), FadeIn(contigs), FadeIn(de_novo), run_time=0.9)

        self.at("producing contigs")
        assembled = genome_world(0.15)
        self.play(contigs.animate.arrange(RIGHT, buff=-0.32).move_to([0, 0.55, 0]),
                  Create(assembled), run_time=1.5)

        self.at("Reference alignment")
        ref_label = T("reference alignment", 32, BLUE).move_to([0, 2.8, 0])
        ref_reads = VGroup(*[read_bar(1.35).move_to([x, 0.65 + 0.32 * (i % 2), 0])
                             for i, x in enumerate([-4.7, -2.8, -0.8, 1.2, 3.2, 4.7])])
        self.play(swap(de_novo, ref_label), FadeOut(contigs), FadeIn(ref_reads), run_time=0.9)

        self.at("Now the reference branches")
        graph = reference_graph(extra_branch=True)
        self.play(ReplacementTransform(assembled, graph), run_time=1.3)

        self.at("A read missing")
        hovering = read_bar(1.45).move_to([0, 2.25, 0])
        self.play(FadeIn(hovering), run_time=0.45)
        self.at("fit another")
        self.play(hovering.animate.move_to([0, 1.72, 0]), run_time=0.8)

        self.at("reported difference")
        marker = Triangle(color=GREEN, fill_color=GREEN, fill_opacity=1).scale(0.13).rotate(PI)
        marker.move_to([0.75, -0.1, 0])
        self.play(FadeIn(marker), graph.main.animate.set_stroke(opacity=0.35),
                  graph.upper.animate.set_stroke(opacity=1.0), run_time=0.7)
        self.play(marker.animate.move_to([0.75, 1.18, 0]), run_time=1.2)
        bob(ref_reads, amp=0.035, speed=1.4)
        self.finish()


class S10Human(SpokenScene):
    def construct(self):
        self.add(stage_panel())
        left = Line([-5.8, 0.15, 0], [-0.65, 0.15, 0], color=BLUE, stroke_width=24)
        right = Line([0.65, 0.15, 0], [5.8, 0.15, 0], color=BLUE, stroke_width=24)
        gap = DashedLine([-0.6, 0.15, 0], [0.6, 0.15, 0], color=GREY, stroke_width=8)
        self.add(left, right, gap, cartoon_tag("history diagram · schematic"))

        self.at("Long accurate reads")
        long_reads = VGroup(
            read_bar(4.1).move_to([-1.05, 1.15, 0]),
            read_bar(4.7).move_to([1.15, -0.85, 0]),
        )
        self.play(FadeIn(long_reads[0], shift=LEFT * 0.4), run_time=1.0)
        self.at("ultra long spans")
        self.play(FadeIn(long_reads[1], shift=RIGHT * 0.4), run_time=1.0)

        self.at("difficult gaps")
        bridge = Line([-0.65, 0.15, 0], [0.65, 0.15, 0], color=BLUE, stroke_width=24)
        completeness = T("completeness", 40, BLUE).move_to([0, 2.8, 0])
        self.play(FadeOut(gap), Create(bridge), FadeIn(completeness), run_time=0.9)

        self.at("A pangenome")
        graph = reference_graph(extra_branch=True, many=True)
        representation = T("representation", 40, TEAL).move_to([0, -2.35, 0])
        self.play(FadeOut(long_reads), ReplacementTransform(VGroup(left, bridge, right), graph),
                  FadeIn(representation), run_time=1.4)

        self.at("many chromosome copies")
        traversals = VGroup(
            read_bar(2.2).move_to([0, 1.78, 0]),
            read_bar(2.2).move_to([0, 0.5, 0]),
            read_bar(2.2).move_to([0, -1.42, 0]),
        )
        self.play(FadeIn(traversals, lag_ratio=0.18), run_time=1.2)

        self.at("Completeness asks")
        self.play(Indicate(completeness, color=BLUE, scale_factor=1.03), run_time=0.6)
        self.at("Representation asks")
        self.play(Indicate(representation, color=TEAL, scale_factor=1.03), run_time=0.6)
        bob(traversals, amp=0.035, speed=1.3)
        self.finish()


class S11Variants(SpokenScene):
    def construct(self):
        self.add(stage_panel())
        graph = reference_graph(extra_branch=True)
        tag = T("graph · schematic", 24, GREY).move_to([-5.85, 3.35, 0], aligned_edge=LEFT)
        self.add(graph, tag)
        active = T("chosen reference", 32, BLUE).move_to([0, 2.75, 0])
        self.play(FadeIn(active), run_time=0.5)

        self.at("First")
        read = read_bar(2.0, 0.3).move_to([0, 1.75, 0])
        poor = read.copy().set_opacity(0.28).move_to([0, 0.58, 0])
        self.play(FadeIn(read), FadeIn(poor), run_time=0.7)

        self.at("close place")
        clean = boxed_label("close alignment", GREEN, size=28).move_to([3.85, 1.72, 0])
        self.play(FadeIn(clean), graph.upper.animate.set_stroke(opacity=1.0),
                  graph.main.animate.set_stroke(opacity=0.32), run_time=0.7)

        self.at("Then it changes")
        marker = Triangle(color=GREEN, fill_color=GREEN, fill_opacity=1).scale(0.14).rotate(PI)
        marker.move_to([0.7, 1.18, 0])
        self.play(FadeIn(marker), run_time=0.4)
        self.at("labeled different")
        self.play(marker.animate.move_to([0.7, -0.1, 0]),
                  graph.upper.animate.set_stroke(opacity=0.32),
                  graph.main.animate.set_stroke(opacity=1.0), run_time=1.1)

        self.at("A variant call")
        comparison = boxed_label("variant call = comparison", GREEN, size=30).move_to([0, -2.05, 0])
        self.play(FadeOut(VGroup(clean, poor)), FadeIn(comparison), run_time=0.7)

        self.at("not a claim")
        unknowns = VGroup(*[boxed_label(f"{name}  ?", GREY, size=26)
                            for name in ("rarity", "selection", "health")])
        unknowns.arrange(RIGHT, buff=0.35).move_to([0, -3.0, 0])
        self.play(FadeIn(unknowns, lag_ratio=0.15), run_time=0.9)
        bob(read, amp=0.04, speed=1.3)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        self.add(stage_panel())
        panels = TwoPanel("sampled", "placed", colors=(BLUE, GREEN), top=3.0, bottom=-2.35)
        self.play(FadeIn(panels), run_time=0.7)

        left_ribbon = Line([-2.5, 0, 0], [2.5, 0, 0], color=BLUE, stroke_width=14)
        left_gap = Rectangle(width=0.85, height=0.5, stroke_width=0,
                             fill_color=BG, fill_opacity=1).move_to([0, 0, 0])
        left_pic = VGroup(left_ribbon, left_gap)
        panels.put(left_pic, "left")

        right_ribbon = Line([-2.5, 0, 0], [2.5, 0, 0], color=BLUE, stroke_width=14)
        right_repeat = RoundedRectangle(corner_radius=0.07, width=1.45, height=0.62,
                                        stroke_color=RED, stroke_width=4, fill_color=RED,
                                        fill_opacity=0.72).move_to([0, 0, 0])
        right_pic = VGroup(right_ribbon, right_repeat)
        panels.put(right_pic, "right")
        self.play(FadeIn(left_pic), FadeIn(right_pic), FadeIn(cartoon_tag()), run_time=0.7)

        self.at("Was the region sampled")
        left_q = T("?", 58, GREY).move_to([panels.area("left")[0][0], 1.65, 0])
        right_q = T("?", 58, GREY).move_to([panels.area("right")[0][0], 1.65, 0])
        self.play(FadeIn(left_q), FadeIn(right_q), run_time=0.6)

        self.at("Extra reads")
        cx, cy = left_pic.get_center()[:2]
        fill_reads = VGroup(*[read_bar(0.8, 0.2).move_to([cx - 1.65 + i * 0.55,
                                                          cy + 0.45 + 0.26 * (i % 3), 0])
                              for i in range(7)])
        self.play(FadeOut(left_q), run_time=0.2)
        self.play(FadeIn(fill_reads, lag_ratio=0.08), FadeOut(left_gap), run_time=1.0)

        self.at("Reads that span")
        long_read = read_bar(4.0, 0.28).move_to(right_pic.get_center() + UP * 0.72)
        self.play(FadeOut(right_q), run_time=0.2)
        self.play(FadeIn(long_read, shift=DOWN * 0.15), run_time=0.8)

        self.at("A richer reference")
        branch = ArcBetweenPoints(right_pic.get_left() + RIGHT * 0.45,
                                  right_pic.get_right() + LEFT * 0.45,
                                  angle=-PI / 2.2, color=TEAL, stroke_width=7)
        self.play(Create(branch), run_time=1.1)

        self.at("Those are different limits")
        checks = VGroup(T("✓", 118, GREEN), T("✓", 118, GREEN))
        checks[0].move_to(panels.area("left")[0])
        checks[1].move_to(panels.area("right")[0])
        self.play(FadeOut(VGroup(left_pic, right_pic, fill_reads, long_read, branch)), run_time=0.5)
        self.play(FadeIn(checks), run_time=0.55)
        self.at("different fixes")
        self.play(Indicate(checks, color=GREEN, scale_factor=1.03), run_time=0.8)
        pulse(checks[0], base=1.0, amp=0.2, speed=1.7)
        pulse(checks[1], base=1.0, amp=0.2, speed=1.7)
        self.finish()


class S13End(EndCard):
    LINE = "More reads fill sampling gaps; reads that span a repeat place it."
