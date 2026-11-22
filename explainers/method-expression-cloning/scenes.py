"""Finding a Gene by What It Does, paced to the supplied narration."""
from bp_parts import *
from bp_style import EndCard

# Patch-clamp palette: BLUE apparatus, GREY anatomy, PURPLE channels,
# YELLOW calcium/current, GREEN control, RED loss, ORANGE stimulus,
# TEAL expressed genes, GOLD dates and the take-home rule.
PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
WELL_BLUE = "#284957"
CELL_BLUE = "#477283"
CELL_LIGHT = "#6894A2"
POOL_COLORS = ("#62D2CA", "#39AEB4", "#8DE3D1", "#288F99", "#59BBA8", "#A1DBE3")
WELL_X = (-4.05, 0, 4.05)
TOP_Y = 2.10
WELL_Y = -0.65
QUESTION = "Does an intact animal need this gene?"
QUESTION_STYLE = dict(y=2.95, size=40, max_w=11)


def pt(x, y):
    return np.array([x, y, 0.0])


def bubble(width, height, at, color, *, fill=None, opacity=1, line=3):
    return Ellipse(width=width, height=height, color=color, stroke_width=line,
                   fill_color=fill or color, fill_opacity=opacity).move_to(at)


def ribbon(i):
    color = POOL_COLORS[i]
    strip = RoundedRectangle(width=0.69, height=0.27, corner_radius=0.12,
                             stroke_width=0, fill_color=color, fill_opacity=1)
    seam = RoundedRectangle(width=0.23, height=0.063, corner_radius=0.027,
                            stroke_width=0, fill_color=BG, fill_opacity=0.58)
    return VGroup(strip, seam.shift(LEFT * 0.13))


GENES = ((0, 1, 2), (3, 4, 5), (0, 2, 4))


def pool(portions, at):
    return VGroup(*(ribbon(i) for i in portions)).arrange(RIGHT, buff=0.12).move_to(at)


def pool_row(portions=GENES, y=TOP_Y, xs=WELL_X):
    return VGroup(*(pool(genes, pt(x, y)) for x, genes in zip(xs, portions)))


def gene_cloud(row=False):
    offsets = [(-1.80, 0.54), (-0.40, -0.34), (1.46, 1.21),
               (-1.35, -1.12), (0.10, 1.32), (1.87, -0.58)]
    genes = VGroup(*(ribbon(i) for i in range(6)))
    if row:
        genes.arrange(RIGHT, buff=0.18).move_to(pt(0, TOP_Y))
    else:
        for i, (gene, (x, y)) in enumerate(zip(genes, offsets)):
            gene.scale(1.55).rotate((i % 3 - 1) * 0.28).move_to(pt(x, y))
    return genes


def library_grid(at):
    genes = VGroup(*(ribbon(i).scale(2.15) for i in range(6)))
    return genes.arrange_in_grid(rows=3, cols=2, buff=(0.41, 0.55)).move_to(at)


def cell(at=ORIGIN, size=1, active=False):
    shell = bubble(2.26, 2.02, ORIGIN, BLUE, fill=CELL_BLUE, line=3.6)
    interior = bubble(1.67, 1.35, pt(-0.10, 0.06), CELL_LIGHT, line=0)
    core = bubble(0.84, 0.69, pt(-0.25, -0.08), WELL_BLUE, opacity=0.85, line=0)
    body = VGroup(shell, interior, core).scale(size).move_to(at)
    if active:
        light_cell(body)
    return body


def light_cell(body, animated=False):
    fill = body[0].animate if animated else body[0]
    glow = body[1].animate if animated else body[1]
    core = body[2].animate if animated else body[2]
    return (fill.set_fill("#94611F").set_stroke(YELLOW, width=4.5),
            glow.set_fill("#DCA835"), core.set_fill(YELLOW, opacity=0.95))


def living(body, speed=1.8, seed=0):
    # Keep the membrane fixed while the layered interior drifts.
    bob(body[1], amp=0.16, speed=speed, seed=seed)
    bob(body[2], amp=0.23, speed=speed * 1.14, seed=seed + 2)


def response_glow(body, emphasize=False):
    """Keep the active cell visibly luminous while the stimulus result is discussed."""
    phase = 0.0
    dim = ManimColor("#74441B")
    bright = ManimColor("#BD8729")

    def breathe(shell, dt):
        nonlocal phase
        phase += dt
        intensity = 0.5 + 0.5 * np.sin(2.6 * phase)
        shell.set_fill(interpolate_color(dim, bright, intensity))

    body[0].add_updater(breathe)
    if emphasize:
        dim_inside = ManimColor("#9B6526")
        bright_inside = ManimColor("#FFD45C")

        def shimmer_interior(interior):
            intensity = 0.5 + 0.5 * np.sin(2.6 * phase)
            interior.set_fill(interpolate_color(dim_inside, bright_inside, intensity))

        body[1].add_updater(shimmer_interior)


def well(x, active=False, proteins=False):
    at = pt(x, WELL_Y)
    rim = bubble(3.65, 3.91, at, BLUE, fill=WELL_BLUE, line=3)
    inset = bubble(3.38, 3.64, at, CELL_LIGHT, fill="#233A49", line=2)
    body = cell(at, 1.14, active)
    result = VGroup(rim, inset, body)
    if proteins:
        result.add(channels(body))
    return result


def tray(active=None, proteins=False, xs=WELL_X):
    return VGroup(*(well(x, active=(i == active), proteins=proteins) for i, x in enumerate(xs)))


def channels(body):
    center = body.get_center()
    return VGroup(*(RoundedRectangle(width=0.16, height=0.31, corner_radius=0.066,
                                     color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.68)
                    .rotate(angle).move_to(center + pt(x, y))
                    for x, y, angle in [(-0.73, 0.89, -0.55), (0, 1.12, 0), (0.74, 0.89, 0.55)]))


def single_well(x=0, active=True):
    return well(x, active=active, proteins=True)


def droplet(at, size=0.43):
    drop = VMobject(color=ORANGE, stroke_width=2.3, fill_color=ORANGE, fill_opacity=0.68)
    drop.start_new_path(pt(0, 0.51))
    drop.add_cubic_bezier_curve_to(pt(-0.07, 0.20), pt(-0.43, -0.07), pt(-0.37, -0.30))
    drop.add_cubic_bezier_curve_to(pt(-0.27, -0.68), pt(0.29, -0.68), pt(0.37, -0.30))
    drop.add_cubic_bezier_curve_to(pt(0.43, -0.07), pt(0.07, 0.20), pt(0, 0.51))
    return drop.scale_to_fit_height(size).move_to(at)


def dose(scene, xs, start=TOP_Y - 0.23, end=WELL_Y + 1.17, pace=1, drop_size=0.43, *, label=None):
    drops = VGroup(*(droplet(pt(x, start), size=drop_size) for x in xs))
    annotations = (label,) if label is not None else ()
    scene.play(FadeIn(drops, shift=DOWN * 0.15), *(FadeIn(mob) for mob in annotations),
               run_time=0.35 * pace)
    scene.play(drops.animate.shift(DOWN * (start - end)), run_time=1.12 * pace,
               rate_func=rate_functions.ease_in_quad)
    scene.play(FadeOut(drops, *annotations), run_time=0.28 * pace)


def calcium(x, y=WELL_Y, scale=1):
    specks = VGroup()
    for dx, dy, radius in [(-0.69, 0.48, 0.12), (0, 0.30, 0.13), (0.65, 0.44, 0.10),
                           (-0.47, -0.43, 0.13), (0.52, -0.35, 0.12)]:
        specks.add(Dot(pt(x + dx * scale, y + dy * scale), radius=radius * scale, color=YELLOW))
    return specks


def shimmer(specks):
    for i, dot in enumerate(specks):
        bob(dot, amp=0.12, speed=2.05, seed=i)


def heat_waves(at):
    waves = VGroup()
    for dx in (-0.45, 0, 0.45):
        wave = VMobject(stroke_color=ORANGE, stroke_width=4)
        wave.set_points_smoothly([at + pt(dx + 0.105 * np.sin(2 * np.pi * t), 0.57 * t)
                                  for t in np.linspace(0, 1, 13)])
        waves.add(wave)
    return waves


def nerve_ending():
    membrane = VMobject(color=BLUE, stroke_width=4.5, fill_color=CELL_BLUE, fill_opacity=1)
    membrane.start_new_path(pt(-1.1, -2.7))
    for handles in (
        ((-1.19, -2.13), (-0.86, -1.47), (-1.79, -0.94)),
        ((-3.3, -0.15), (-3.05, 1.38), (-2.58, 1.84)),
        ((-2.02, 2.42), (-1.78, 1.19), (-1.08, 1.40)),
        ((-0.37, 1.58), (-0.56, 2.63), (0.11, 2.57)),
        ((0.81, 2.58), (0.64, 1.54), (1.24, 1.33)),
        ((1.86, 1.05), (2.16, 2.18), (2.72, 1.68)),
        ((3.35, 1.19), (3.31, -0.04), (1.65, -0.96)),
        ((0.87, -1.45), (1.29, -2.07), (1.10, -2.7)),
        ((0.52, -2.76), (-0.54, -2.76), (-1.1, -2.7)),
    ):
        membrane.add_cubic_bezier_curve_to(*(pt(*xy) for xy in handles))
    inner = bubble(3.42, 1.66, pt(-0.1, 0.1), CELL_LIGHT, line=0)
    return VGroup(membrane, inner)


def zoomed_cell():
    return bubble(10.50, 5.52, pt(0, -0.02), BLUE, fill=WELL_BLUE, line=3.5)


def mouse():
    body = bubble(3.24, 2.11, pt(0.12, -0.32), GREY, fill="#687C89", line=3)
    head = bubble(1.70, 1.12, pt(-1.28, -0.22), GREY, fill="#687C89", line=3).rotate(0.25)
    ear = bubble(0.79, 0.89, pt(-0.87, 0.53), GREY, fill="#7E92A0", line=2)
    nose = Dot(pt(-2.06, -0.40), color=TEXT, radius=0.07)
    eye = Dot(pt(-1.49, -0.11), color=BG, radius=0.095)
    tail = VMobject(color=GREY, stroke_width=5)
    tail.set_points_smoothly([pt(1.59, -0.56), pt(2.11, -0.28), pt(2.36, 0.26), pt(2.14, 0.55)])
    return VGroup(tail, body, head, ear, nose, eye).move_to(pt(3.40, 0))


def prediction_stage():
    dish = single_well(x=-3.72)
    ions = calcium(-3.72)
    animal = mouse()
    mark = T("?", size=76, color=GOLD, weight=BOLD).move_to(pt(-0.44, 0.14))
    return dish, ions, animal, mark


class S01Hook(SpokenScene):
    def construct(self):
        nerve = nerve_ending()
        self.add(nerve, scope_tag(size=28))
        pulse(nerve[0], base=4.5, amp=1.0, speed=2.3)
        bob(nerve[1], amp=0.15, speed=2.1)
        self.at("responds to capsaicin")
        capsaicin = T("Capsaicin", 30, ORANGE).move_to(pt(-3.94, 3.06))
        dose(self, (-2.34, 0.11, 2.55), start=3.2, end=2.15, label=capsaicin)
        self.play(nerve[0].animate.set_fill("#9A6327"), nerve[1].animate.set_fill(YELLOW), run_time=0.95)
        self.at("which gene", lead=1.78)
        question = T("?", 82, GOLD, weight=BOLD).move_to(pt(5.94, 0.52))
        self.play(FadeIn(question), run_time=0.45)
        self.at("that cell expresses")
        nerve[0].clear_updaters()
        nerve[1].clear_updaters()
        membrane = zoomed_cell()
        genes = gene_cloud()
        self.play(ReplacementTransform(nerve[0], membrane), FadeOut(nerve[1]),
                  LaggedStart(*(FadeIn(gene, scale=0.55) for gene in genes), lag_ratio=0.17), run_time=2.3)
        inside_question = T("?", 82, GOLD, weight=BOLD).move_to(pt(3.30, 0.74))
        self.play(swap(question, inside_question, run_time=0.62))
        for i, gene in enumerate(genes):
            bob(gene, amp=0.14, speed=1.63 + 0.09 * i, seed=i)
        self.at("you cannot spot")
        genes[2][0].set_stroke(POOL_COLORS[2], width=3, opacity=0.45)
        pulse(genes[2][0], base=3, amp=2, speed=2.7)
        self.at("find the gene")
        self.play(FadeOut(inside_question), run_time=0.65)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Finding a Gene by What It Does"
    LESSON = "Expression cloning"

    def construct(self):
        membrane, genes = zoomed_cell(), gene_cloud()
        # Leave the middle open for the standard lesson and title typography.
        row = gene_cloud(row=True)
        title = fit(T(self.TITLE, 54, TEXT, font=TITLE_FONT), max_w=11.4)
        lesson = T(self.LESSON.upper(), 28, TEAL, weight=BOLD).move_to(pt(0, 0.82))
        rule = Line(pt(-1.1, -0.83), pt(1.1, -0.83), color=GOLD, stroke_width=4)
        self.add(membrane, genes, scope_tag(size=28))
        self.play(Transform(genes, row), FadeOut(membrane), run_time=0.55)
        self.play(FadeIn(title), FadeIn(lesson), GrowFromCenter(rule), run_time=0.35)
        self.wait(0.65)
        self.play(FadeOut(title), FadeOut(lesson), FadeOut(rule), run_time=0.40)


class S03Library(SpokenScene):
    def construct(self):
        genes = gene_cloud(row=True)
        self.add(genes, scope_tag(size=28))
        self.at("first make")
        self.play(Transform(genes, library_grid(pt(-2.5, 0.04))), run_time=1.45)
        self.at("copies of the", lead=0.05)
        copies = library_grid(pt(2.5, 0.04))
        self.play(TransformFromCopy(genes, copies), run_time=1.25)
        expressed = T("Expressed genes", 30, TEAL).move_to(pt(-2.5, -2.06))
        self.play(FadeIn(expressed), run_time=0.43)
        self.at("called cdna")
        cdna = T("cDNA copies", 32, TEAL).move_to(pt(2.5, -2.06))
        self.play(FadeIn(cdna), run_time=0.40)
        for i, gene in enumerate(copies):
            bob(gene, amp=0.11, speed=2, seed=i)
        self.at("divide them into")
        for gene in copies:
            gene.clear_updaters()
        pools = pool_row()
        self.play(FadeOut(genes), FadeOut(expressed), FadeOut(cdna),
                  ReplacementTransform(copies, pools), run_time=1.60)
        pool_label = T("cDNA pools", 30, TEAL).move_to(pt(0, 2.88))
        self.play(FadeIn(pool_label), run_time=0.40)
        dishes = tray()
        self.at("pick foreign cells", lead=1.05)
        self.play(LaggedStart(*(FadeIn(dish, shift=UP * 0.25) for dish in dishes), lag_ratio=0.15), run_time=1.75)
        for i, dish in enumerate(dishes):
            living(dish[2], seed=i)
        self.at("293")
        cells = caption("HEK293 cells", color=BLUE)
        self.play(FadeIn(cells), run_time=0.5)
        self.at("respond to capsaicin", lead=0.75)
        dose(self, WELL_X, start=1.55)
        self.at("gene into foreign")
        gene = pools[1][1].copy()
        self.add(gene)
        assay = caption("Heterologous expression", color=TEAL)
        self.play(gene.animate.move_to(dishes[1][2].get_center()), run_time=1.32)
        self.at("is heterologous")
        self.play(FadeOut(gene, shift=DOWN * 0.18), swap(cells, assay), run_time=0.65)
        self.finish()


class S04Screen(SpokenScene):
    def construct(self):
        pools, dishes = pool_row(), tray()
        pool_label = T("cDNA pools", 30, TEAL).move_to(pt(0, 2.88))
        self.add(pools, dishes, pool_label, scope_tag(size=28))
        for i, dish in enumerate(dishes):
            living(dish[2], seed=i)
        self.at("put one pool")
        self.play(FadeOut(pool_label),
                  LaggedStart(*(genes.animate.move_to(pt(x, 0.76)) for genes, x in zip(pools, WELL_X)),
                              lag_ratio=0.22), run_time=2.0)
        self.play(FadeOut(pools, shift=DOWN * 0.3), run_time=0.55)
        self.at("make the encoded", lead=0.92)
        blocks = VGroup(*(channels(dish[2]) for dish in dishes))
        self.play(LaggedStart(*(FadeIn(channel, scale=0.5) for group in blocks for channel in group),
                              lag_ratio=0.23), run_time=2.35)
        self.at("then add capsaicin")
        dose(self, WELL_X)
        self.at("calcium flowing", lead=0.07)
        ions = calcium(0)
        self.play(LaggedStart(*(FadeIn(ion, shift=DOWN * 0.64) for ion in ions), lag_ratio=0.32),
                  *light_cell(dishes[1][2], animated=True), run_time=2.25)
        response_glow(dishes[1][2])
        shimmer(ions)
        calcium_label = caption("Calcium influx", color=YELLOW)
        self.play(FadeIn(calcium_label), run_time=0.45)
        self.at("most dishes stay dark")
        self.play(FadeOut(calcium_label), run_time=0.55)
        self.at("marking the winning")
        winner = pool(GENES[1], pt(0, TOP_Y))
        winner_label = place_label(T("Winning pool", 30, GOLD), winner, dirs=(UP,), buff=0.28)
        self.play(FadeIn(winner, shift=UP * 0.25), run_time=0.48)
        self.play(FadeIn(winner_label), run_time=0.45)
        self.finish()


class S05Sib(SpokenScene):
    def construct(self):
        dishes = tray(active=1, proteins=True)
        winner = pool(GENES[1], pt(0, TOP_Y))
        ions = calcium(0)
        winning_label = place_label(T("Winning pool", 30, GOLD), winner, dirs=(UP,), buff=0.28)
        self.add(dishes, winner, winning_label, ions, scope_tag(size=28))
        shimmer(ions)
        response_glow(dishes[1][2])
        for i, dish in enumerate(dishes):
            living(dish[2], seed=i)
        self.at("whole pool of genes")
        self.play(winner.animate.scale(1.22), FadeOut(winning_label), run_time=1.24)
        self.at("split the winning pool", lead=0.56)
        sides = (-2.1, 2.1)
        subsets = pool_row(((3,), (4, 5)), xs=sides)
        fresh = tray(xs=sides)
        self.play(ReplacementTransform(winner, subsets), FadeOut(ions), FadeOut(dishes),
                  run_time=0.84)
        self.play(FadeIn(fresh), run_time=0.46)
        self.at("test fresh silent cells", lead=1.61)
        self.play(*(genes.animate.shift(DOWN * 1.23) for genes in subsets), run_time=0.55)
        proteins = VGroup(*(channels(dish[2]) for dish in fresh))
        self.play(FadeOut(subsets, shift=DOWN * 0.35), FadeIn(proteins), run_time=0.30)
        dose(self, sides, pace=0.60)
        smaller_glow = calcium(2.1)
        self.play(*light_cell(fresh[1][2], animated=True), FadeIn(smaller_glow), run_time=0.44)
        shimmer(smaller_glow)
        self.wait(1.6)
        self.at("repeat this narrowing")
        finalists = pool_row(((4,), (5,)), xs=sides)
        single_clone_wells = tray(xs=sides)
        self.play(FadeIn(finalists, shift=UP * 0.30), FadeOut(fresh), FadeOut(smaller_glow),
                  FadeOut(proteins), run_time=0.57)
        self.play(FadeIn(single_clone_wells), run_time=0.47)
        self.play(finalists.animate.shift(DOWN * 1.15), run_time=0.56)
        proteins = VGroup(*(channels(dish[2]) for dish in single_clone_wells))
        self.play(FadeOut(finalists, shift=DOWN * 0.32), FadeIn(proteins), run_time=0.27)
        dose(self, sides, pace=0.52)
        ions = calcium(2.1)
        final_dish = single_clone_wells[1]
        self.play(FadeIn(ions, shift=DOWN * 0.36), *light_cell(final_dish[2], animated=True), run_time=0.48)
        clone = pool((5,), pt(0, TOP_Y))
        self.play(FadeOut(single_clone_wells[0]), FadeOut(proteins[0]),
                  final_dish.animate.shift(LEFT * 2.1), proteins[1].animate.shift(LEFT * 2.1),
                  ions.animate.shift(LEFT * 2.1), FadeIn(clone, shift=UP * 0.25), run_time=0.71)
        shimmer(ions)
        living(final_dish[2])
        response_glow(final_dish[2])
        self.at("that is expression cloning")
        rule = caption("Expression cloning", color=TEAL, size=34)
        self.play(FadeIn(rule), run_time=0.65)
        self.at("one alone creates")
        clone[0][0].set_stroke(TEAL, width=5)
        pulse(clone[0][0], base=4, amp=2.3, speed=2.7)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        dish = single_well()
        clone = pool((5,), pt(0, TOP_Y))
        ions = calcium(0)
        self.add(dish, clone, ions, scope_tag(size=28))
        response_glow(dish[2], emphasize=True)
        living(dish[2])
        shimmer(ions)
        self.at("respond to capsaicin", lead=0.75)
        self.play(FadeOut(clone), run_time=0.36)
        dose(self, (0,), start=2.29, drop_size=0.72)
        self.at("noxious heat")
        waves = heat_waves(pt(0, 1.53)).scale(1.55)
        self.play(LaggedStart(*(Create(wave) for wave in waves), lag_ratio=0.19), run_time=0.76)
        self.play(waves.animate.shift(UP * 0.35), run_time=0.52)
        self.play(FadeOut(waves), run_time=0.43)
        self.at("pause and think")
        _, _, animal, mark = prediction_stage()
        for layer in dish[2]:
            layer.clear_updaters()
        for ion in ions:
            ion.clear_updaters()
        self.play(dish.animate.shift(LEFT * 3.72), ions.animate.shift(LEFT * 3.72),
                  FadeIn(animal, shift=LEFT * 0.22), run_time=1.7)
        response_glow(dish[2], emphasize=True)
        self.play(FadeIn(mark), run_time=0.47)
        self.at("does that prove")
        question = question_card(QUESTION, **QUESTION_STYLE)
        self.play(FadeIn(question), run_time=0.57)
        living(dish[2])
        shimmer(ions)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        dish, ions, animal, mark = prediction_stage()
        question = question_card(QUESTION, **QUESTION_STYLE)
        self.add(dish, ions, animal, mark, question, scope_tag(size=28))
        response_glow(dish[2], emphasize=True)
        shimmer(ions)
        self.wait(self.narration_s)


def circuits():
    paths = VGroup()
    labels = VGroup()
    for y, name in zip((1.2, 0.06, -1.08), ("TRPV1", "TRPM3", "TRPA1")):
        # Channel names occupy their own column. Each route feeds the same output.
        labels.add(T(name, 30, PURPLE, weight=BOLD).move_to(pt(1.04, y)))
        start = pt(2.04, y)
        block = RoundedRectangle(width=0.55, height=0.45, corner_radius=0.12,
                                 color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.72)
        block.move_to(pt(2.97, y))
        incoming = Line(start, block.get_left(), color=PURPLE, stroke_width=5)
        outgoing = VMobject(color=PURPLE, stroke_width=5)
        outgoing.set_points_as_corners([block.get_right(), pt(4.22, y), pt(4.84, 0.06)])
        paths.add(VGroup(incoming, block, outgoing))
    return paths, labels


def cut(at):
    return VGroup(Line(at + pt(-0.17, -0.17), at + pt(0.17, 0.17), color=RED, stroke_width=5),
                  Line(at + pt(-0.17, 0.17), at + pt(0.17, -0.17), color=RED, stroke_width=5))


def disable_route(route):
    incoming, channel, outgoing = route
    return (incoming.animate.set_stroke(opacity=0.22),
            channel.animate.set_stroke(opacity=0.22).set_fill(opacity=0.18),
            outgoing.animate.set_stroke(opacity=0.22))


class S08Limits(SpokenScene):
    def construct(self):
        dish, ions, animal, mark = prediction_stage()
        question = question_card(QUESTION, **QUESTION_STYLE)
        self.add(dish, ions, animal, mark, question, scope_tag(size=28))
        living(dish[2])
        response_glow(dish[2], emphasize=True)
        shimmer(ions)
        bob(animal, amp=0.07, speed=1.9)
        self.at("cloning shows")
        self.play(FadeOut(question), FadeOut(mark), run_time=0.55)
        sufficient = boxed_label("Sufficient", color=YELLOW, size=32).move_to(pt(-3.72, 2.18))
        self.play(FadeIn(sufficient), run_time=0.55)
        self.at("does not prove")
        animal.clear_updaters()
        self.play(animal.animate.shift(UP * 0.58), run_time=1.66)
        self.at("testing need")
        self.play(animal.animate.scale(0.4).move_to(pt(3.58, 2.53)), run_time=1.55)
        paths, labels = circuits()
        study = T("Vandewauw, 2018", 28, GOLD).move_to(pt(3.30, -2.12))
        self.at("in 2018")
        self.play(FadeIn(study), run_time=0.50)
        self.at("three heat channels", lead=1.35)
        self.play(LaggedStart(*(FadeIn(path, shift=RIGHT * 0.15) for path in paths), lag_ratio=0.24),
                  run_time=1.23)
        self.play(FadeIn(labels), run_time=0.53)
        output = Arrow(pt(4.89, 0.06), pt(6.27, 0.06), buff=0, color=YELLOW, stroke_width=9)
        withdraw = place_label(T("Withdrawal", 28, YELLOW), output, dirs=(UP,), buff=0.23)
        withdraw.shift(RIGHT * 0.17)
        self.play(GrowArrow(output), FadeIn(withdraw), run_time=0.62)
        self.at("single removals")
        first_cut = cut(paths[0][1].get_center())
        self.play(*disable_route(paths[0]), FadeIn(first_cut),
                  Indicate(output, color=YELLOW, scale_factor=1.09), run_time=1.02)
        self.at("losing all three")
        other_cuts = VGroup(*(cut(path[1].get_center()) for path in paths[1:]))
        self.play(*disable_route(paths[1]), *disable_route(paths[2]), FadeIn(other_cuts),
                  output.animate.set_color(GREY).set_opacity(0.30),
                  withdraw.animate.set_color(GREY), run_time=1.18)
        self.finish()


def comparison_wells():
    return VGroup(well(-2.45), well(2.45, active=True, proteins=True))


def pore():
    bars = VGroup()
    for x in (-3.88, -1.94):
        bars.add(RoundedRectangle(width=1.59, height=0.59, corner_radius=0.17,
                                  color=GREY, stroke_width=4, fill_color=CELL_BLUE, fill_opacity=1)
                 .move_to(pt(x, 0.02)))
    outline = VGroup(*(RoundedRectangle(width=0.47, height=1.50, corner_radius=0.18, color=GREY,
                                        stroke_width=3, fill_color=CELL_LIGHT, fill_opacity=0.9)
                       .move_to(pt(x, 0.02)) for x in (-3.34, -2.48)))
    return VGroup(bars, outline)


class S09Controls(SpokenScene):
    def construct(self):
        wells = comparison_wells()
        ions = calcium(2.45)
        self.add(wells, ions, scope_tag(size=28))
        living(wells[0][2], seed=1)
        living(wells[1][2], seed=3)
        response_glow(wells[1][2])
        shimmer(ions)
        self.at("controls for expression")
        tags = VGroup(T("Procedure alone", 30, GREEN).move_to(pt(-2.45, 1.91)),
                      T("Expressed gene", 30, TEAL).move_to(pt(2.45, 1.91)))
        self.play(FadeIn(tags), run_time=0.60)
        self.at("did not cause")
        self.play(Indicate(wells[0][0], color=GREEN, scale_factor=1.05), run_time=1.17)
        self.at("removing a gene")
        animal = mouse().scale(1.58).move_to(pt(-2.4, 0.1))
        original = Arrow(pt(1.42, 0.88), pt(5.42, 0.06), buff=0, color=PURPLE, stroke_width=7)
        alternate = Arrow(pt(1.42, -0.96), pt(5.42, -0.12), buff=0, color=GREEN, stroke_width=7)
        alternate.set_opacity(0.27)
        knockout = cut(original.get_center()).scale(2.15)
        self.play(FadeOut(wells), FadeOut(tags), FadeOut(ions), run_time=0.31)
        self.play(FadeIn(animal), FadeIn(original), FadeIn(alternate), run_time=0.51)
        self.play(FadeIn(knockout), original.animate.set_opacity(0.28), run_time=0.55)
        self.at("development compensate")
        compensation = caption("Development can compensate", color=GREEN)
        self.play(FadeIn(compensation), alternate.animate.set_opacity(1), run_time=0.52)
        self.at("cell pass current", lead=1.0)
        membrane = pore().scale(1.17, about_point=pt(-2.91, 0.02))
        self.play(FadeOut(animal, original, alternate, knockout, compensation),
                  FadeIn(membrane, scale=0.72), run_time=0.78)
        flow = VGroup(*(Dot(pt(-2.91, y), radius=0.145, color=YELLOW)
                        for y in (-1.72, -0.96, -0.2, 0.56, 1.32)))
        self.play(FadeIn(flow), run_time=0.35)
        self.at("never proves")
        uncertainty = T("?", 68, GOLD, weight=BOLD).move_to(pt(-0.78, 1.17))
        self.play(FadeIn(uncertainty), run_time=0.44)
        self.play(flow.animate.shift(DOWN * 1.13), membrane.animate.scale(1.19, about_point=pt(-2.91, 0.02)),
                  run_time=1.90, rate_func=linear)
        self.play(FadeOut(flow[0]), FadeOut(flow[1]), run_time=0.37)
        incoming = VGroup(Dot(pt(-2.91, 1.86), radius=0.145, color=YELLOW),
                          Dot(pt(-2.91, 1.10), radius=0.145, color=YELLOW))
        self.play(FadeIn(incoming, shift=DOWN * 0.36), run_time=0.55)
        self.at("necessity sufficiency")
        claims = VGroup(boxed_label("Necessary", GREEN, 32),
                        boxed_label("Sufficient", YELLOW, 32),
                        boxed_label("Lines the pore", PURPLE, 32)).arrange(DOWN, buff=0.38).move_to(pt(2.64, 0.04))
        self.play(LaggedStart(*(FadeIn(claim, shift=LEFT * 0.20) for claim in claims), lag_ratio=0.79),
                  run_time=3.10)
        self.finish()


def embryo():
    shell = bubble(4.66, 4.55, pt(0, -0.36), BLUE, fill=CELL_BLUE, line=4.5)
    inner = bubble(3.54, 3.45, pt(-0.19, -0.44), CELL_LIGHT, line=0)
    # Keep the base fixed and leave room above the rim for the RNA pools to bob.
    return VGroup(shell, inner).stretch(0.93, 1, about_point=shell.get_bottom())


def dorsal_ridge(shell):
    center = shell.get_center()
    radius_x, radius_y = shell.width / 2, shell.height / 2
    tip_x = 0.65
    tip_y = np.sqrt(1 - tip_x**2)

    def point(x, y):
        return center + pt(x * radius_x, y * radius_y)

    left, right = point(-tip_x, tip_y), point(tip_x, tip_y)
    ridge = VMobject(color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.75)
    ridge.start_new_path(left)
    ridge.add_cubic_bezier_curve_to(point(-0.34, 1.06), point(0.34, 1.06), right)
    ridge.add_cubic_bezier_curve_to(point(0.33, 0.83), point(-0.33, 0.83), left)
    return ridge


def cue_tag():
    cue = Triangle(color=ORANGE, fill_color=ORANGE, fill_opacity=0.90, stroke_width=2).scale(0.27)
    marker = Dot(cue.get_corner(UL) + pt(-0.06, 0.02), radius=0.10, color=YELLOW)
    return VGroup(cue, marker)


class S10UnlockedA(SpokenScene):
    def construct(self):
        pools = pool_row()
        wells = tray()
        self.add(pools, wells, scope_tag(size=28))
        for i, dish in enumerate(wells):
            living(dish[2], seed=i)
        for i, each in enumerate(pools):
            bob(each, amp=0.16, speed=1.7, seed=i)
        self.at("unlocked landmark")
        sample = embryo()
        self.play(FadeOut(wells[0]), FadeOut(wells[2]), ReplacementTransform(wells[1], sample),
                  run_time=1.65)
        bob(sample[1], amp=0.14, speed=2.3)
        self.at("in 1992")
        rna = T("RNA pools", 30, TEAL).move_to(pt(0, 2.93))
        self.play(FadeIn(rna), run_time=0.60)
        self.at("harland injected")
        for each in pools:
            each.clear_updaters()
        self.bring_to_front(pools)
        injection_y = sample[0].get_top()[1] - 0.45
        self.play(*(each.animate.move_to(pt((i - 1) * 0.55, injection_y)).scale(0.55)
                    for i, each in enumerate(pools)), run_time=2.24)
        self.play(FadeOut(pools, shift=DOWN * 0.65), FadeOut(rna), run_time=0.68)
        self.at("lacking dorsal structures")
        self.play(Indicate(sample[0], color=BLUE, scale_factor=1.05), run_time=1.05)
        self.at("narrowing the pools")
        subset = pool((3, 4, 5), pt(0, TOP_Y + 0.27))
        self.play(FadeIn(subset, shift=DOWN * 0.12), run_time=0.34)
        discarded = VGroup(subset[0], subset[2])
        clone = subset[1]
        self.play(FadeOut(discarded, scale=0.65), run_time=0.43)
        sample[1].clear_updaters()
        self.play(clone.animate.move_to(pt(0, 1.19)),
                  sample.animate.scale(1.08, about_point=sample[0].get_bottom()), run_time=0.46)
        bob(sample[1], amp=0.14, speed=2.3)
        ridge = dorsal_ridge(sample[0])
        noggin = caption("Noggin, 1992", color=GOLD, size=34)
        self.play(GrowFromCenter(ridge, run_time=0.93), FadeOut(clone, shift=DOWN * 0.26),
                  FadeIn(noggin, run_time=0.48))
        self.at("in 1997")
        wells = tray(proteins=True)
        pools = pool_row()
        self.play(FadeOut(sample), FadeOut(ridge), FadeOut(noggin), run_time=0.57)
        self.play(FadeIn(wells), FadeIn(pools), run_time=0.75)
        for i, dish in enumerate(wells):
            living(dish[2], seed=i)
        self.at("screened")
        self.play(FadeOut(pools, shift=DOWN * 0.47), run_time=0.72)
        self.at("binding a tagged", lead=0.80)
        cues = VGroup(*(cue_tag().move_to(pt(x, 2.05)) for x in WELL_X))
        self.play(FadeIn(cues), run_time=0.45)
        self.play(cues.animate.shift(DOWN * 1.45), run_time=1.05)
        self.play(FadeOut(cues[0], shift=UP * 0.58), FadeOut(cues[2], shift=UP * 0.58), run_time=0.55)
        self.at("they found")
        neuropilin = caption("Neuropilin, 1997", color=GOLD, size=34)
        self.play(wells[1][2][0].animate.set_stroke(ORANGE, width=6),
                  wells[1][2][1].animate.set_fill("#CB9143"), run_time=0.65)
        self.play(FadeIn(neuropilin), run_time=0.55)
        self.at("the receiver of")
        sema = T("Sema3A", 30, ORANGE).move_to(pt(0, 2.16))
        self.play(FadeIn(sema), run_time=0.55)
        self.finish()


class S11UnlockedB(SpokenScene):
    def construct(self):
        wells = tray(proteins=True)
        pools = pool_row()
        self.add(wells, pools, scope_tag(size=28))
        for i, dish in enumerate(wells):
            living(dish[2], seed=i)
        for i, each in enumerate(pools):
            bob(each, amp=0.13, speed=1.8, seed=i)
        self.at("also in 1997")
        lineage = T("Sensory-neuron cDNA", 32, TEAL).move_to(pt(0, 2.97))
        self.at("answered our opening")
        self.play(FadeIn(lineage), run_time=0.7)
        self.at("they screened")
        for each in pools:
            each.clear_updaters()
        self.play(LaggedStart(*(each.animate.shift(DOWN * 0.88) for each in pools), lag_ratio=0.25),
                  run_time=1.85)
        self.play(FadeOut(pools), run_time=0.56)
        self.at("for capsaicin")
        dose(self, WELL_X)
        self.at("calcium influx")
        ions = calcium(0)
        self.play(FadeIn(ions, shift=DOWN * 0.48), *light_cell(wells[1][2], animated=True), run_time=1.25)
        shimmer(ions)
        response_glow(wells[1][2])
        self.at("clone they recovered", lead=0.4)
        self.play(FadeOut(wells[0]), FadeOut(wells[2]), FadeOut(lineage), run_time=0.66)
        clone = pool((5,), pt(0, TOP_Y))
        self.play(FadeIn(clone, scale=1.32), run_time=0.65)
        self.at("trpv1")
        trpv1 = caption("TRPV1, 1997", color=GOLD, size=34)
        self.play(FadeIn(trpv1), run_time=0.50)
        self.at("noxious heating", lead=0.64)
        waves = heat_waves(pt(0, 1.29))
        self.play(FadeOut(clone), Create(waves), run_time=0.79)
        self.play(waves.animate.shift(UP * 0.57), run_time=0.74)
        self.play(FadeOut(waves), run_time=0.41)
        self.at("response hides its gene")
        pools = pool_row(y=2.22)
        self.play(FadeIn(pools, shift=DOWN * 0.19), FadeOut(trpv1), run_time=0.75)
        self.at("narrow expressed pools")
        self.play(ReplacementTransform(pools, clone), run_time=1.16)
        self.play(clone.animate.shift(DOWN * 0.52), run_time=0.64)
        self.finish()


class S12End(EndCard):
    LINE = "Split pools of expressed genes until one alone creates the response."
