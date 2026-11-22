"""Counting and painting chromosomes, timed to the supplied narration.

GREY is nuclear structure, purple is stained chromatin, TEAL and ORANGE
distinguish painted chromosome identities, RED marks the mutant version,
and GOLD marks dates and count changes. All chromosome shapes are schematic.
"""

from bp_parts import *

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
STAIN = "#C3A9D8"
BAND = "#6D537F"
FIELD = "#394258"
NUCLEAR_FILL = "#343449"
QUESTION = "46 chromosomes: normal DNA and genes?"
CENTRE = np.array([0.0, -0.24, 0.0])
PAINT = {40: TEAL, 41: TEAL, 42: ORANGE, 43: ORANGE}


def point(x, y):
    return np.array([x, y, 0.0])


def nuclear_membrane():
    return Ellipse(width=9.7, height=5.64, fill_color=NUCLEAR_FILL, fill_opacity=1,
                   stroke_color=GREY, stroke_width=3).move_to(CENTRE)


def slide_field():
    return RoundedRectangle(width=12.45, height=5.55, corner_radius=1.08,
                            fill_color=FIELD, fill_opacity=1, stroke_color=GREY,
                            stroke_width=2).move_to(CENTRE)


def heading(text, color=TEXT):
    return fit_text(text, max_w=11.1, size=34, min_size=28, color=color,
                    weight=BOLD).move_to(point(0, 3.22))


def footer(text, color=TEXT):
    return caption(text, size=30, color=color, y=-3.45).set_x(0)


def schematic():
    return scope_tag(size=28, color=TEXT)


def count_label(value, y=3.22):
    label = counter("{:.0f} chromosomes", value, point(0, y), size=34, color=GOLD)
    redraw = label.get_updaters()[0]
    displayed = round(value.get_value())

    def update_count(mob):
        nonlocal displayed
        current = round(value.get_value())
        if current != displayed:
            redraw(mob)
            displayed = current

    return label.clear_updaters().add_updater(update_count)


def thread(centre, radius, phase, color=PURPLE, opacity=0.78, width=5):
    """Loose schematic chromatin curled around its own centre."""
    t = np.linspace(0, 2 * PI, 41)
    x = radius * (0.66 * np.cos(2 * t + phase) + 0.33 * np.cos(5 * t))
    y = radius * (0.73 * np.sin(3 * t) + 0.29 * np.sin(t + phase))
    curve = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    curve.set_points_smoothly([centre + point(a, b) for a, b in zip(x, y)])
    return curve


def crowded_strands():
    rng = np.random.default_rng(63)
    strands = VGroup()
    for i in range(46):
        angle = i * 2.39996
        radius = np.sqrt((i + 0.5) / 46)
        centre = CENTRE + point(3.98 * radius * np.cos(angle), 2.16 * radius * np.sin(angle))
        strands.add(thread(centre, rng.uniform(0.35, 0.69), rng.uniform(0, TAU),
                           color=[PURPLE, STAIN, GREY][i % 3], opacity=0.78))
    return strands


def rod(pair, color=STAIN, height=None):
    """A pinched mitotic chromosome silhouette with matching bands on homologs."""
    h = height if height is not None else 1.30 - 0.024 * (pair - 1)
    w = 0.24 * (h / 1.3) ** 0.35
    contour = [(-.5, -.40), (-.38, -.49), (.38, -.49), (.5, -.40),
               (.47, -.10), (.32, .03), (.49, .18), (.5, .40),
               (.36, .49), (-.36, .49), (-.5, .40), (-.49, .18),
               (-.32, .03), (-.47, -.10)]
    body = Polygon(*[point(x * w, y * h) for x, y in contour], stroke_width=0,
                   fill_color=color, fill_opacity=1)
    stripe = BAND if color == STAIN else interpolate_color(ManimColor(color), ManimColor(BG), .48)
    bands = VGroup()
    for y, thickness in [(-.31, .12), (-.14, .06 + .02 * (pair % 3)),
                         (.045, .065), (.20 + .035 * (pair % 4), .10)]:
        if abs(y - .045) < .01:
            width = w * .64
        elif y < -.25 or y > .25:
            width = w * .96
        else:
            width = w * .88
        bands.add(Rectangle(width=width, height=h * thickness,
                            fill_color=stripe, fill_opacity=1, stroke_width=0).move_to(UP * y * h))
    return VGroup(body, *bands)


def pair_spot(pair):
    row, column = divmod(pair - 1, 8)
    return point(1.47 * (column - (3 if row == 2 else 3.5)), 1.39 - 1.65 * row)


def spread_rods(paint=None, sample=False):
    """The same 23 landmarks are used whenever the spread is ordered."""
    paint = paint or {}
    rng = np.random.default_rng(98)
    result = VGroup()
    for index in range(46):
        pair, homolog = divmod(index, 2)
        pair += 1
        chromosome = rod(pair, paint.get(index, STAIN))
        if sample:
            slot = (index * 17) % 48
            row, column = divmod(slot, 12)
            position = point((column - 5.5) * .98, (1.5 - row) * 1.18 - .24)
            chromosome.scale(.79).rotate(rng.uniform(-.56, .56))
            position += point(*rng.uniform(-.09, .09, size=2))
        else:
            position = pair_spot(pair) + RIGHT * (.22 if homolog else -.22)
        chromosome.move_to(position)
        result.add(chromosome)
    return result


def spread(paint=None):
    return slide_field(), spread_rods(paint)


def drift_group(group, amp=.10, speed=1.2, rotate=.026):
    """Keep the diagram alive without shifting its frame or its labels."""
    base = group.get_center().copy()
    clock = 0.0
    angle = 0.0

    def drift(mob, dt):
        nonlocal clock, angle
        clock += dt
        next_angle = rotate * np.sin(speed * clock)
        mob.rotate(next_angle - angle, about_point=mob.get_center())
        mob.move_to(base + point(amp * np.sin(speed * clock), .53 * amp * np.sin(1.37 * speed * clock)))
        angle = next_angle

    return group.add_updater(drift)


def highlight(pair, color=GOLD):
    return Ellipse(width=1.12, height=1.24, stroke_color=color,
                   stroke_width=4).move_to(pair_spot(pair))


def territory(centre, color, seed, scale=1):
    """A soft paint patch and cords packed into a small, distinct region."""
    rng = np.random.default_rng(seed)
    outline = VMobject(stroke_width=0, fill_color=color, fill_opacity=.25)
    angles = np.linspace(0, TAU, 19)
    points = [centre + scale * point((1.08 + .12 * np.cos(3*t)) * np.cos(t),
                                      (.79 + .13 * np.sin(4*t)) * np.sin(t)) for t in angles]
    outline.set_points_smoothly(points)
    outline.close_path()
    cords = VGroup()
    for _ in range(6):
        offset = point(*rng.uniform([-.42, -.36], [.42, .36]))
        cords.add(thread(centre + scale * offset, scale * rng.uniform(.36, .67),
                         rng.uniform(0, TAU), color=color, opacity=.83, width=4))
    return VGroup(outline, cords)


def painted_contents():
    """Four visible painted territories amid unpainted chromatin."""
    contents = crowded_strands().set_stroke(opacity=.25)
    patches = VGroup(
        territory(CENTRE + point(-2.38, .66), TEAL, 20),
        territory(CENTRE + point(.01, .79), ORANGE, 31),
        territory(CENTRE + point(2.36, -.54), TEAL, 44),
        territory(CENTRE + point(-.55, -.91), ORANGE, 52),
    )
    return VGroup(contents, patches)


def painted_nucleus():
    return nuclear_membrane(), painted_contents()


def paint_drift(contents):
    for seed, patch in enumerate(contents[1]):
        drift_group(patch[1], amp=.17, speed=1.18 + .11 * seed, rotate=.18)


def probes_at(x):
    """Fluorescent spots moving across the stained slide."""
    spots = VGroup()
    for i in range(12):
        centre = point(x + .29 * np.sin(i * 2.4), (i - 5.5) * .41 - .24)
        color = TEAL if i % 2 else ORANGE
        spots.add(Dot(centre, radius=.19, color=color, fill_opacity=.27),
                  Dot(centre, radius=.066 + .014 * (i % 3), color=color))
    return spots


def predict_card():
    return question_card(QUESTION, y=3.22, size=32, max_w=11).set_x(0)


def predict_world():
    field, rods = spread()
    number = count_label(ValueTracker(46), y=-3.45).clear_updaters()
    return field, rods, number, highlight(21)


def focused_rod(pair, x, color=STAIN, height=3.77):
    return rod(pair, color, height=height).stretch(1.45, 0).move_to(point(x, -.24))


def tip(color, rod_picture, length=.52):
    cap = RoundedRectangle(width=rod_picture.width * .95, height=length, corner_radius=.095,
                           stroke_width=0, fill_color=color, fill_opacity=1)
    return cap.move_to(rod_picture.get_top() + DOWN * (length / 2))


def locus(color, rod_picture, y):
    return RoundedRectangle(width=rod_picture.width * 1.1, height=.14, corner_radius=.04,
                            stroke_width=0, fill_color=color, fill_opacity=1).move_to(point(rod_picture.get_x(), y))


def orbit(mob, amp=.13):
    drift_group(mob, amp=amp, speed=1.65, rotate=.018)


class S01Hook(SpokenScene, TitleCard):
    LESSON = "Karyotyping and chromosome FISH"
    TITLE = "Counting and Painting Chromosomes"

    def construct(self):
        membrane = nuclear_membrane()
        strands = crowded_strands()
        self.add(membrane, strands)
        for i, strand in enumerate(strands):
            bob(strand, amp=.16, speed=1.1 + .12 * (i % 4), seed=i)
        self.at("crowded nucleus")
        title = fit_text(self.TITLE, max_w=11.7, size=42, min_size=32, font=TITLE_FONT).move_to(point(0, 3.23))
        self.play(FadeIn(title), run_time=.45)
        self.at("Chromosomes live there")
        self.play(FadeOut(title), run_time=.32)

        parent_pair = VGroup(rod(1).scale(1.45).move_to(point(-.55, -.24)),
                             rod(1).scale(1.45).move_to(point(.55, -.24)))
        pair_outline = Ellipse(width=2.25, height=2.57, stroke_color=PURPLE, stroke_width=3).move_to(CENTRE)
        self.play(FadeIn(parent_pair), Create(pair_outline),
                  strands.animate.set_stroke(opacity=.31), run_time=.75)
        bob(parent_pair, amp=.14, speed=1.5)
        self.at("from each parent")
        name = footer("Homologous chromosome pair")
        self.play(FadeIn(name), run_time=.4)
        self.at("uses stain spreads")
        parent_pair.clear_updaters()
        left = parent_pair.copy().move_to(point(-2.15, -.24))
        right = VGroup(rod(1).scale(1.45).move_to(point(1.75, -.24)),
                       rod(1).scale(1.45).move_to(point(2.55, -.24)))
        stain_text = footer("Karyotyping").set_x(-2.15)
        self.play(Transform(parent_pair, left), FadeOut(pair_outline), FadeOut(name), run_time=.8)
        self.play(FadeIn(stain_text), run_time=.45)
        bob(parent_pair, amp=.15, speed=1.3)
        self.at("Fluorescent DNA probes")
        spots = VGroup(*[Dot(point(3.55, -.9 + i * .22), radius=.065, color=TEAL) for i in range(7)])
        self.play(FadeIn(right), FadeIn(spots), run_time=.7)
        bright = VGroup(rod(1, TEAL).scale(1.45).move_to(point(1.75, -.24)),
                        rod(1, TEAL).scale(1.45).move_to(point(2.55, -.24)))
        self.at("bind matching sequences")
        self.play(LaggedStart(*[dot.animate.move_to(point(2.55 if i % 2 else 1.75, -.9 + i * .22))
                                for i, dot in enumerate(spots)], lag_ratio=.12), run_time=1.1)
        self.at("method called FISH")
        fish_text = footer("FISH", TEAL).set_x(2.15)
        self.play(Transform(right, bright), FadeOut(spots), FadeIn(fish_text), run_time=.65)
        bob(right, amp=.14, speed=1.6)
        self.at("chromosomes glow", lead=-1.0)
        self.play(FadeOut(parent_pair), FadeOut(right), FadeOut(stain_text), FadeOut(fish_text),
                  strands.animate.set_stroke(opacity=.78), run_time=.75)
        self.finish()


class S02Karyotype(SpokenScene):
    def construct(self):
        membrane, strands = nuclear_membrane(), crowded_strands()
        self.add(membrane, strands)
        for i, strand in enumerate(strands):
            bob(strand, amp=.12, speed=1.37, seed=i)
        self.at("dividing cell")
        stage = heading("Mitosis")
        self.play(FadeIn(stage), run_time=.48)
        self.at("each chromosome packs", lead=.55)
        strands.clear_updaters(recursive=True)
        compact = VGroup()
        for i, strand in enumerate(crowded_strands()):
            compact.add(rod(i // 2 + 1).scale(.67).rotate(.28 * np.sin(i)).move_to(strand))
        self.play(LaggedStart(*[ReplacementTransform(a, b) for a, b in zip(strands, compact)],
                              lag_ratio=.032), run_time=2.65)
        self.remove(*compact)
        self.add(compact)

        self.at("Spreading and staining")
        field, scattered = slide_field(), spread_rods(sample=True)
        self.play(Transform(membrane, field), ReplacementTransform(compact, scattered),
                  FadeOut(stage), run_time=2.1)
        self.at("count every chromosome", lead=.12)
        total = ValueTracker(0)
        number = count_label(total)
        active = VGroup(*[Dot(a.get_top() + UP * .09, radius=.057, color=GOLD).set_opacity(0)
                          for a in scattered])
        self.play(scattered.animate.set_fill(opacity=.39), FadeIn(number), run_time=.25)
        self.add(active)
        order = sorted(range(46), key=lambda i: (i * 17) % 48)
        shown = 0

        def mark_count(picture):
            nonlocal shown
            current = round(total.get_value())
            for i in order[shown:current]:
                picture[i].set_fill(opacity=1)
                active[i].set_opacity(1)
            shown = current

        scattered.add_updater(mark_count)
        self.play(total.animate.set_value(46), rate_func=linear, run_time=4.15)
        scattered.clear_updaters()
        number.clear_updaters()
        self.at("The stain leaves stripes")
        bands = footer("Stain reveals bands")
        self.play(FadeOut(active), FadeIn(bands), run_time=.64)
        drift_group(scattered, amp=.09, speed=1.7)
        self.at("Sorting rods by size")
        scattered.clear_updaters()
        ordered = spread_rods()
        self.play(ReplacementTransform(scattered, ordered), FadeOut(number), FadeOut(bands), run_time=3.25)
        self.at("forming a karyotype")
        self.play(FadeIn(heading("Karyotype (schematic)")), run_time=.6)
        self.finish()


class S03Fish(SpokenScene):
    def construct(self):
        field, rods = spread()
        self.add(field, rods)
        drift_group(rods, amp=.14, speed=1.48)
        label = heading("Karyotype (schematic)")
        self.add(label)
        self.at("track one chromosome")
        target = highlight(21, TEAL)
        self.play(Create(target), run_time=.8)
        self.at("add fluorescent DNA probes")
        markers = probes_at(-5.55)
        dna_probes = heading("Fluorescent DNA probes")
        self.play(swap(label, dna_probes), FadeIn(markers), run_time=.64)
        self.play(markers.animate.shift(RIGHT * 8.13), rate_func=smooth, run_time=2.14)
        coloured = spread_rods(PAINT)
        self.at("matching sequence")
        rods.clear_updaters()
        self.play(*[Transform(rods[i], coloured[i]) for i in (40, 41)],
                  FadeOut(target), FadeOut(markers), run_time=1.35)
        self.at("Labeling whole chromosomes")
        second = probes_at(-4.5)
        self.play(FadeIn(second), run_time=.30)
        self.play(second.animate.shift(RIGHT * 8.8), run_time=1.1)
        self.play(*[Transform(rods[i], coloured[i]) for i in (42, 43)], FadeOut(second), run_time=.9)
        self.at("chromosome painting")
        painting = heading("Chromosome painting")
        self.play(swap(dna_probes, painting), run_time=.67)
        for i in PAINT:
            bob(rods[i], amp=.105, speed=1.5, seed=i)

        self.at("After mitosis")
        rods.clear_updaters(recursive=True)
        membrane, contents = painted_nucleus()
        patches = contents[1]
        nuclei_threads = contents[0]
        painted_indices = [40, 42, 41, 43]
        self.play(Transform(field, membrane), FadeOut(painting),
                  *[rods[i].animate.move_to(patches[j]) for j, i in enumerate(painted_indices)],
                  *[FadeOut(r) for i, r in enumerate(rods) if i not in PAINT],
                  FadeIn(nuclei_threads), run_time=1.56)
        self.at("chromosome partly unpacks")
        unpacking = [ReplacementTransform(rods[i], patch) for i, patch in zip(painted_indices, patches)]
        self.play(LaggedStart(*unpacking, lag_ratio=.13), run_time=2.83)
        self.remove(nuclei_threads, *patches)
        self.add(contents)
        paint_drift(contents)
        self.at("a chromosome territory")
        territories = heading("Chromosome territories (schematic)")
        self.play(FadeIn(territories), run_time=.55)
        self.at("countable pairs")
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        membrane, contents = painted_nucleus()
        territories = heading("Chromosome territories (schematic)")
        self.add(membrane, contents, territories)
        paint_drift(contents)
        self.at("what a chromosome count")
        field, rods, count, choice = predict_world()
        self.play(Transform(membrane, field), ReplacementTransform(contents, rods),
                  FadeOut(territories), run_time=2.58)
        drift_group(rods, amp=.11, speed=1.43)
        self.at("spread shows 46")
        self.play(FadeIn(count), run_time=.55)
        self.at("the usual count")
        self.play(Create(choice), run_time=.65)
        pulse(choice, base=4, amp=1.3, speed=2)
        self.at("Does that normal count")
        self.play(FadeIn(predict_card()), run_time=.65)
        self.at("extra chromosome 21")
        self.at("disrupted gene", lead=-.16)
        rods.clear_updaters()
        choice.clear_updaters()
        self.play(Transform(rods, spread_rods()), Transform(choice, highlight(21)), run_time=.43)
        self.finish()


class S05Pause(Scene):
    """Rebuild the question and hold it still for the supplied silent clip."""

    def construct(self):
        self.camera.background_color = BG
        field, rods, count, choice = predict_world()
        wash = VGroup(Ellipse(width=2.40, height=4.76, stroke_width=0, fill_color=TEXT),
                      Ellipse(width=1.72, height=4.25, stroke_width=0, fill_color=TEXT))
        elapsed = 0.0

        def sweep(light, dt):
            nonlocal elapsed
            elapsed = min(4.5, elapsed + dt)
            fraction = elapsed / 4.5
            envelope = np.sin(PI * fraction) ** .65
            light.move_to(point(-4.85 + 9.7 * fraction, -.24))
            light[0].set_fill(opacity=.16 * envelope)
            light[1].set_fill(opacity=.085 * envelope)

        wash.add_updater(sweep, call_updater=True)
        self.add(field, wash, rods, count, choice, predict_card())
        self.wait(4.5)


class S06Limits(SpokenScene):
    def construct(self):
        field, rods, count, choice = predict_world()
        question = predict_card()
        self.add(field, rods, count, choice, question)
        self.at("No count is only", lead=.05)
        self.play(FadeOut(question), run_time=.45)
        pulse(choice, base=4, amp=1.6, speed=1.4)
        self.at("A cell with 46")
        recipient = focused_rod(10, .65)
        donors = VGroup(focused_rod(21, -2.86, height=2.67),
                        focused_rod(21, -1.86, height=2.67))
        focus = VGroup(donors, recipient)
        choice.clear_updaters()
        self.play(rods.animate.set_opacity(.10), FadeOut(choice), FadeIn(focus, scale=.6),
                  FadeOut(count), run_time=.62)
        count = count_label(ValueTracker(46)).clear_updaters()
        scope = schematic()
        self.play(FadeIn(count), FadeIn(scope), run_time=.52)
        orbit(focus, amp=.23)
        self.at("hold extra chromosome")
        focus.clear_updaters()
        extra = tip(TEAL, donors[1], .59)
        self.play(FadeIn(extra), run_time=.75)
        self.at("attached to another chromosome", lead=.47)
        # The extra segment joins the recipient while both original homologs stay intact.
        longer = focused_rod(10, .65, height=4.04).shift(DOWN * .12)
        self.play(extra.animate.move_to(longer.get_top() + DOWN * extra.height / 2),
                  Transform(recipient, longer), run_time=1.33)
        extra_caption = footer("Extra chromosome 21 DNA", TEAL)
        self.play(FadeIn(extra_caption), run_time=.45)

        self.at("A swap called")
        left, right = focused_rod(5, -1.68), focused_rod(9, 1.68)
        left_tip, right_tip = tip(ORANGE, left), tip(TEAL, right)
        left_destination, right_destination = right_tip.get_center(), left_tip.get_center()
        gene = Dot(left_tip.get_bottom() + UP * .11, radius=.072, color=TEXT)
        carried_tip = VGroup(left_tip, gene)
        control = locus(GOLD, right, 1.00)
        translocation = heading("Translocation")
        old_case = VGroup(focus, extra)
        self.play(FadeOut(old_case), FadeOut(extra_caption), FadeOut(count), run_time=.42)
        self.play(FadeIn(VGroup(left, right, carried_tip, right_tip, control)), run_time=.44)
        self.play(carried_tip.animate(path_arc=-.67).shift(left_destination - left_tip.get_center()),
                  right_tip.animate(path_arc=.67).move_to(right_destination),
                  FadeIn(translocation), run_time=1.20)
        self.at("place a gene beside")
        junction = probe_hit(right.get_x(), 1.10, TEXT)
        control_note = footer("Strong control region", GOLD)
        self.play(Create(junction), FadeIn(control_note), run_time=.58)
        swapped = VGroup(left, right, carried_tip, right_tip, control, junction)
        orbit(swapped, amp=.32)
        self.at("without changing total DNA")
        equal_note = footer("Total DNA unchanged")
        self.play(swap(control_note, equal_note), run_time=.7)

        self.at("a tumor's two copies")
        swapped.clear_updaters()
        copies = VGroup(focused_rod(13, -.87), focused_rod(13, .87))
        self.play(FadeOut(swapped), FadeOut(equal_note), FadeOut(translocation),
                  FadeIn(copies, scale=.65), run_time=.92)
        thirteen = heading("Chromosome 13")
        self.at("chromosome 13")
        self.play(FadeIn(thirteen), run_time=.53)
        self.at("both carry one mutant")
        altered = VGroup(*[focused_rod(13, x, RED) for x in (-.87, .87)])
        self.play(LaggedStart(*[Transform(a, b) for a, b in zip(copies, altered)], lag_ratio=.32),
                  run_time=1.34)
        orbit(copies, amp=.26)
        self.at("leaving no normal copy")
        self.play(FadeIn(footer("No normal gene copy", RED)), run_time=.47)
        self.finish()


def probe_hit(x, y, color):
    center = point(x, y)
    return VGroup(Circle(radius=.40, stroke_color=color, stroke_width=3).move_to(center),
                  Circle(radius=.23, stroke_color=color, stroke_width=3).move_to(center),
                  Dot(center, radius=.085, color=color))


def edge_view():
    """Two enlarged territories, with a few strands crossing their soft border."""
    left = territory(point(-1.92, -.24), TEAL, 20, scale=2.05)
    right = territory(point(1.92, -.24), ORANGE, 31, scale=2.05)
    loose = VGroup(
        thread(point(-.29, .36), .81, 1.4, TEAL, opacity=1, width=6),
        thread(point(.32, -.66), .86, 4.8, ORANGE, opacity=1, width=6),
    )
    return VGroup(left, right, loose)


class S07Guards(SpokenScene):
    def construct(self):
        field, rods = spread()
        rods.set_opacity(.10)
        copies = VGroup(*[focused_rod(13, x, RED) for x in (-.87, .87)])
        old_title, old_note = heading("Chromosome 13"), footer("No normal gene copy", RED)
        scope = schematic()
        self.add(field, rods, copies, old_title, old_note, scope)
        self.at("experimenters do not judge")
        self.play(FadeOut(copies), FadeOut(old_title), FadeOut(old_note), FadeOut(scope),
                  rods.animate.set_opacity(1), run_time=2.05)
        drift_group(rods, amp=.15, speed=1.45)
        self.at("They check what DNA")
        check = footer("DNA gained or lost", TEAL)
        gain_pair = VGroup(rods[40], rods[41])
        gain = highlight(21, TEAL).add_updater(lambda ring: ring.move_to(gain_pair), call_updater=True)
        self.play(Create(gain, suspend_mobject_updating=False), FadeIn(check), run_time=.67)
        self.at("trace breaks with probes")
        focus = rods[42].get_center()
        breaking = probe_hit(focus[0], focus[1] + .30, ORANGE)
        breaking.add_updater(lambda marker: marker.move_to(rods[42].get_center() + UP * .30))
        break_note = footer("Breaks", ORANGE)
        self.play(FadeOut(gain, suspend_mobject_updating=False),
                  Create(breaking, suspend_mobject_updating=False), swap(check, break_note), run_time=.71)
        self.at("test which gene versions")
        gene_note = footer("Gene versions", RED)
        versions = VGroup(*[probe_hit(rods[i].get_x(), rods[i].get_y() + .22, RED) for i in (24, 25)])
        versions[0].add_updater(lambda marker: marker.move_to(rods[24].get_center() + UP * .22))
        versions[1].add_updater(lambda marker: marker.move_to(rods[25].get_center() + UP * .22))
        self.play(FadeOut(breaking, suspend_mobject_updating=False),
                  FadeIn(versions, suspend_mobject_updating=False), swap(break_note, gene_note), run_time=.8)

        self.at("Chromosome painting has a limit")
        membrane, contents = painted_nucleus()
        versions.clear_updaters(recursive=True)
        rods.clear_updaters()
        self.play(Transform(field, membrane), ReplacementTransform(rods, contents),
                  FadeOut(versions), FadeOut(gene_note), run_time=2.72)
        paint_drift(contents)
        self.at("Painted territories press together")
        close = edge_view()
        contents.clear_updaters(recursive=True)
        self.play(ReplacementTransform(contents, VGroup(close[0], close[1])),
                  run_time=2.4)
        self.at("loose loops poking")
        self.play(LaggedStart(*[Create(loop) for loop in close[2]], lag_ratio=.32), run_time=1.5)
        for i, zone in enumerate(close):
            drift_group(zone, amp=.19, speed=1.32 + .21 * i, rotate=.051)
        self.at("Whole nucleus painting")
        limit = heading("Whole-nucleus painting")
        self.play(FadeIn(limit), run_time=.55)
        self.at("whether edges mix", lead=.60)
        self.play(FadeIn(footer("Edges unresolved (schematic)")), run_time=.54)
        self.finish()


class S08UnlockedDown(SpokenScene):
    def construct(self):
        membrane = nuclear_membrane()
        close = edge_view()
        old_title, old_note = heading("Whole-nucleus painting"), footer("Edges unresolved (schematic)")
        self.add(membrane, close, old_title, old_note)
        self.at("These methods unlocked")
        field, rods = spread()
        self.play(Transform(membrane, field), ReplacementTransform(close, rods),
                  FadeOut(old_title), FadeOut(old_note), run_time=2.85)
        drift_group(rods, amp=.09, speed=1.42)
        self.at("In 1959")
        date = heading("1959", GOLD).set_x(-4.93)
        total = ValueTracker(46)
        number = count_label(total)
        self.play(FadeIn(date), run_time=.55)
        self.at("counted chromosomes")
        self.play(FadeIn(number), run_time=.65)
        self.at("with Down syndrome")
        name = footer("Down syndrome")
        self.play(FadeIn(name), run_time=.60)
        self.at("cultured cells held", lead=.36)
        rods.clear_updaters()
        # End its ambient drift at the original grid landmarks before adding the third homolog.
        self.play(Transform(rods, spread_rods()), run_time=.38)
        spot = pair_spot(21)
        new = rod(21, TEAL).move_to(spot + point(.55, -.51))
        self.play(FadeIn(new, shift=DOWN * .31), run_time=.65)
        self.play(new.animate(run_time=1.25).move_to(spot + RIGHT * .58),
                  total.animate(run_time=.35).set_value(47))
        observed = VGroup(rods, new)
        landmark = observed.get_center().copy()
        self.remove(rods, new)
        self.add(observed)
        drift_group(observed, amp=.18, speed=1.48, rotate=0)
        self.at("That extra chromosome")
        halo = Ellipse(width=.40, height=1.15, stroke_color=TEAL, stroke_width=4).move_to(new)
        self.play(Create(halo), run_time=.72)
        pulse(halo, base=4, amp=1.6, speed=1.8)
        halo.add_updater(lambda ring: ring.move_to(new))
        self.at("later number 21")
        self.play(swap(name, footer("Extra chromosome 21", TEAL)), run_time=.68)
        self.at("to the condition")
        observed.clear_updaters()
        self.play(observed.animate.move_to(landmark), run_time=1.1)
        self.finish()


class S09UnlockedCml(SpokenScene):
    def construct(self):
        field, rods = spread()
        extra = rod(21, TEAL).move_to(pair_spot(21) + RIGHT * .58)
        old = VGroup(heading("1959", GOLD).set_x(-4.93), count_label(ValueTracker(47)),
                     footer("Extra chromosome 21", TEAL),
                     Ellipse(width=.40, height=1.15, stroke_color=TEAL, stroke_width=4).move_to(extra))
        self.add(field, rods, extra, old)
        self.at("In 1960")
        self.play(FadeOut(old), FadeOut(extra), run_time=.45)
        date = heading("1960", GOLD)
        self.play(FadeIn(date), run_time=.50)
        self.at("saw a small chromosome", lead=.46)
        small = focused_rod(22, -1.45, height=2.44)
        focus = rods[43].copy()
        self.add(focus)
        self.play(rods.animate.set_opacity(.13), Transform(focus, small), run_time=1.62)
        self.at("chronic myeloid leukemia")
        cml = footer("Chronic myeloid leukaemia")
        self.play(FadeIn(cml), run_time=.50)
        orbit(focus, amp=.19)
        self.at("In 1973")
        date2 = heading("1973", GOLD)
        self.play(swap(date, date2), run_time=.7)
        recipient = focused_rod(9, 1.45)
        self.play(FadeIn(recipient, scale=.68), run_time=1.14)
        orbit(recipient, amp=.18)
        self.at("was chromosome 22")
        id22 = T("22", 30, TEXT, weight=BOLD).move_to(point(-1.45, -2.55))
        id9 = T("9", 30, TEXT, weight=BOLD).move_to(point(1.45, -2.55))
        self.play(FadeIn(id22), run_time=.48)
        self.at("its missing piece attached", lead=.32)
        focus.clear_updaters()
        recipient.clear_updaters()
        gap = focus.get_top()
        piece = tip(ORANGE, recipient, .59).move_to(gap + UP * .33)
        self.play(FadeIn(piece), run_time=.42)
        self.play(piece.animate(path_arc=-.62).move_to(recipient.get_top() + UP * .25),
                  FadeIn(id9), run_time=1.34)
        orbit(focus, amp=.19)
        orbit(recipient, amp=.20)
        piece.add_updater(lambda cap: cap.move_to(recipient.get_top() + UP * .25))
        self.at("work tied that join")
        junction = probe_hit(recipient.get_x(), recipient.get_top()[1], TEAL)
        self.play(Create(junction), FadeOut(date2), run_time=.62)
        pulse(junction[0], base=3, amp=1.25, speed=1.8)
        junction.add_updater(lambda spot: spot.move_to(recipient.get_top()))
        self.at("fusion of two genes")
        self.play(swap(cml, footer("BCR–ABL fusion (schematic)", TEAL)), run_time=.7)
        self.finish()


def marker_cell(center, scale=1):
    boundary = Ellipse(width=2.7, height=2.45, fill_color=NUCLEAR_FILL, fill_opacity=1,
                       stroke_color=GREY, stroke_width=3).move_to(center)
    chromatin = VGroup(*[thread(center + point(.52 * np.cos(t), .58 * np.sin(t)), .38,
                                i, STAIN, opacity=.42, width=3)
                         for i, t in enumerate(np.linspace(0, TAU, 7, endpoint=False))])
    marker = rod(4, height=1.22)
    marker.apply_function(lambda p: point(p[0] + .33 * max(0, p[1]) ** 1.2, p[1])).rotate(-.37)
    marker.move_to(center)
    return VGroup(boundary, chromatin, marker).scale(scale, about_point=center)


def clone_layout(positions, scale):
    return VGroup(*[marker_cell(point(x, y), scale) for x, y in positions])


class S10UnlockedClone(SpokenScene):
    def construct(self):
        field = slide_field()
        date = heading("1963", GOLD)
        cell = marker_cell(CENTRE, 2.10)
        self.add(field, cell)
        self.at("In 1963")
        self.play(FadeIn(date), run_time=.55)
        drift_group(cell[1], amp=.16, rotate=.19)
        drift_group(cell, amp=.13, speed=1.23, rotate=.023)
        self.at("tracked marrow cells")
        marrow = footer("Marrow cell")
        self.play(FadeIn(marrow), run_time=.60)
        daughters = clone_layout([(-1.95, -.24), (1.95, -.24)], 1.15)
        self.at("Chromosome markers showed", lead=.9)
        cell.clear_updaters(recursive=True)
        self.play(FadeOut(marrow), Transform(cell, daughters[0]), run_time=.83)
        self.play(TransformFromCopy(cell, daughters[1]), run_time=.98)
        self.at("each spleen colony")
        cluster = clone_layout([(-1.55, .83), (1.55, .83), (-1.55, -1.41), (1.55, -1.41)], .86)
        self.play(Transform(cell, cluster[0]), Transform(daughters[1], cluster[1]),
                  TransformFromCopy(cell, cluster[2]), TransformFromCopy(daughters[1], cluster[3]),
                  run_time=1.26)
        self.at("grown from one cell")
        clone_note = footer("One cell, one clone (schematic)")
        self.play(FadeIn(clone_note), run_time=.54)
        for picture in (cell, daughters[1], cluster[2], cluster[3]):
            drift_group(picture[1], amp=.10, rotate=.12)

        self.at("Counting banding and painting")
        lineage = VGroup(cell, daughters[1], cluster[2], cluster[3])
        lineage.clear_updaters(recursive=True)
        all_rods = spread_rods(PAINT).scale(.42).move_to(point(-3.75, -.23))
        membrane, contents = painted_nucleus()
        painted = VGroup(membrane, contents).scale(.43).move_to(point(3.80, -.23))
        joined = focused_rod(9, 0, height=2.2)
        attached = tip(ORANGE, joined, .39).shift(UP * .29)
        self.play(swap(date, heading("Counting, banding and painting")),
                  FadeOut(clone_note), lineage.animate.scale(.42).move_to(point(0, -1.52)),
                  FadeIn(all_rods, scale=.85), FadeIn(painted, scale=.83), run_time=2.15)
        self.at("rearrangements", lead=.46)
        self.play(FadeIn(VGroup(joined, attached).move_to(point(0, 1.41)).scale(.7)), run_time=.68)
        paint_drift(contents)
        for picture in lineage:
            drift_group(picture[1], amp=.07, rotate=.12)
        self.finish()


class S11End(EndCard):
    LINE = "Stained spreads and fluorescent probes expose\nchromosome number, rearrangements, and territories."
