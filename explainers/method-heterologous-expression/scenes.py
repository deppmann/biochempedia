"""Heterologous expression, timed to the supplied narration.

Grey: membranes and cell structure. Teal: the added gene and its product.
Blue: glass and water. Purple: chloride channels already in the oocyte.
Yellow: measured responses and current. Green: controls. Red: blocked pores.
Amber: stimuli and PIP2. Gold: dates.
"""

from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
CELL_FILL = "#293A50"
CELL_INNER = "#7792AE"
QUESTION = "Is your protein the chloride channel?"
QUESTION_STYLE = dict(y=-3.32, size=36)
PAIR_X = 3.18


def pt(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=32):
    return T(text, size, color).move_to(pt(x, y))


def block(color=TEAL, width=0.64, height=0.52):
    return RoundedRectangle(
        corner_radius=0.1, width=width, height=height, stroke_color=color,
        stroke_width=3, fill_color=color, fill_opacity=0.72,
    )


def strand(color=TEAL, single=False):
    rows = [0] if single else [-0.075, 0.075]
    body = VGroup(*(Line(pt(-0.53, y), pt(0.53, y), color=color, stroke_width=5) for y in rows))
    return VGroup(
        RoundedRectangle(corner_radius=0.19, width=1.55, height=0.46, color=color,
                         stroke_width=2, fill_color=color, fill_opacity=0.23),
        body,
    )


def cell(x, y, rx, ry, *, crowded=False, motion=True):
    """Membrane, soft interior, and a fixed set of drifting dots."""
    center = pt(x, y)
    outer = Ellipse(width=2 * rx, height=2 * ry, color=GREY, stroke_width=3,
                    fill_color=CELL_FILL, fill_opacity=1).move_to(center)
    inner = Ellipse(width=2 * rx - 0.18, height=2 * ry - 0.18,
                    color=CELL_INNER, stroke_opacity=0.5, stroke_width=1.6).move_to(center)
    drift = VGroup()
    drift_x, drift_y = min(.30, .095 * rx), min(.22, .075 * ry)
    points = [(-.57, .25), (-.36, -.35), (-.05, -.63), (.35, .38), (.62, -.15),
              (.02, .61), (.28, -.37), (-.17, .08), (.55, .15), (-.55, -.15),
              (-.31, .54), (.30, .06), (.10, -.17), (-.21, -.53)]
    for i, (u, v) in enumerate(points):
        anchor = center + pt(rx * u, ry * v)
        dot = Dot(anchor, radius=.135 + .025 * (i % 4), color=CELL_INNER, fill_opacity=.71)
        if motion:
            dot.drift_time = 0.0

            def drift_dot(mob, dt, anchor=anchor, i=i):
                mob.drift_time += dt
                angle = mob.drift_time * (1.19 + .085 * (i % 4)) + i * 1.75
                offset = pt(drift_x * (np.cos(angle) - np.cos(i * 1.75)),
                            drift_y * (np.sin(angle) - np.sin(i * 1.75)))
                mob.move_to(anchor + offset)

            dot.add_updater(drift_dot)
        drift.add(dot)
    crowd = VGroup()
    if crowded:
        for i, a in enumerate(np.linspace(0, TAU, 14, endpoint=False)):
            color = (PURPLE, ORANGE, BLUE, GOLD, GREEN)[i % 5]
            shape = (block(color, .43, .45) if i % 3 else
                     RegularPolygon(6, color=color, fill_opacity=.68, stroke_width=2).scale(.25))
            shape.rotate(a).move_to(center + pt(rx * np.cos(a), ry * np.sin(a)))
            crowd.add(shape)
    picture = VGroup(outer, inner, drift, crowd)
    picture.drift = drift
    return picture


def opening_pair(motion=True):
    return cell(-3.65, 0.25, 2.52, 2.40, crowded=True, motion=motion), host(motion=motion)


def host(x=3.3, y=0.10, motion=True):
    return cell(x, y, 2.55, 2.35, motion=motion)


def host_protein(x=3.3, y=0.10):
    return block().move_to(pt(x + 1.53, y + 1.88)).rotate(-0.60)


def cultured(motion=True):
    return cell(-PAIR_X, .65, 1.62, 1.60, motion=motion)


def oocyte(x, motion=True):
    return cell(x, .65, 1.97, 1.97, motion=motion)


def protein_at_surface(x, color=TEAL):
    return block(color).move_to(pt(x + 1.44, 2.00)).rotate(-0.6)


def gate(x, y, color=TEAL, closed=True, size=1.0):
    """A schematic pore with two sides and a visible plug when closed."""
    sides = VGroup(*(block(color, .32, .94).shift(RIGHT * dx) for dx in (-.39, .39)))
    plug = block(RED, .48, .27).set_opacity(1 if closed else 0)
    g = VGroup(sides, plug).scale(size).move_to(pt(x, y))
    g.plug = plug
    return g


def ions(x, y, length=1.7, *, sideways=False, color=YELLOW):
    """Repeated packets traveling along a single path through the channel."""
    direction = RIGHT if sideways else DOWN
    beads = VGroup()
    for i in range(6):
        dot = Dot(radius=.092, color=color)
        dot.phase = i / 6

        def drift(mob, dt):
            mob.phase = (mob.phase + dt * .47) % 1
            mob.move_to(pt(x, y) + direction * (mob.phase - .5) * length)
            mob.set_opacity(min(1, 8 * mob.phase, 8 * (1 - mob.phase)))

        drift(dot, 0)
        dot.add_updater(drift)
        beads.add(dot)
    return beads


def rise(t):
    return .22 + .60 * (1 - np.exp(-11 * max(0, t - .36)))


def flat(t):
    return .22


def fall(t):
    return 1.04 - rise(t)


def trace(x, fn, color, *, y=-2.62, half_width=1.96, height=.91):
    graph = Plot((x - half_width, x + half_width, y, y + height), (0, 1), (0, 1))
    curve = graph.curve(fn, color=color, width=5)
    return graph, curve


def scheme(x=0, y=-2.92):
    return scope_tag(size=28, color=TEXT).move_to(pt(x, y))


def tube(tip, end):
    """A thin blue glass needle angled away from its target."""
    vector = end - tip
    normal = np.array([-vector[1], vector[0], 0]) / np.linalg.norm(vector)
    return Polygon(tip, end + .15 * normal, end - .15 * normal,
                   stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=.25)


def transfer(mob, start, end, height=.65):
    path = CubicBezier(start, start + UP * height, end + UP * height, end)
    return MoveAlongPath(mob, path, rate_func=smooth)


class S01Hook(SpokenScene):
    def construct(self):
        native, foreign = opening_pair()
        question = caption("How do you test one protein?", 36, y=-3.15).set_x(0)
        gene = strand().move_to(pt(-3.63, .10))
        copy = gene.copy()
        self.add(native, question)
        self.at("inside a crowded")
        self.play(FadeIn(gene), run_time=.8)
        self.at("copy its gene")
        self.play(FadeOut(question), FadeIn(foreign), run_time=.75)
        self.add(copy)
        self.at("put it into", lead=.35)
        self.play(transfer(copy, pt(-3.63, .10), pt(3.3, .10), 2.0), run_time=1.67)
        self.at("let the host")
        protein = host_protein()
        self.play(TransformFromCopy(copy, protein), run_time=.92)
        self.at("watch what response")
        signal = pulse(Arc(radius=.56, start_angle=-.1, angle=1.45, arc_center=pt(4.83, 1.98),
                           color=YELLOW), base=4, amp=1.8, speed=4)
        self.play(Create(signal), run_time=.65)
        self.at("that method is")
        method = caption("Heterologous expression", 36, y=-3.15).set_x(0)
        self.play(FadeIn(method), run_time=.5)
        self.at("heterologous expression", lead=0)
        self.play(FadeOut(signal), run_time=.55)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Testing One Protein in a Foreign Cell"
    LESSON = "Heterologous expression"

    def construct(self):
        foreign = host(motion=False)
        protein = host_protein()
        world = VGroup(foreign, protein)
        title = fit_text(self.TITLE, 12, size=50, min_size=32, font=TITLE_FONT).move_to(pt(0, 3.10))
        self.add(world)
        self.play(world.animate.shift(pt(-3.3, -.63)), run_time=.60)
        self.play(FadeIn(title), run_time=.28)
        self.wait(.70)
        self.play(FadeOut(title), run_time=.32)


class S03HowHosts(SpokenScene):
    def construct(self):
        foreign = host(0, -.53)
        protein = host_protein(0, -.53)
        left, right = cultured(), oocyte(PAIR_X)
        cdna, rna = strand(), strand(single=True)
        cdna.move_to(pt(-1.22, -1.78))
        rna.move_to(pt(1.22, -1.78))
        cl = place_label(T("cDNA", 32, TEAL), cdna, dirs=(DOWN,), buff=.30)
        rl = place_label(T("RNA", 32, TEAL), rna, dirs=(DOWN,), buff=.30)
        self.add(foreign, protein)
        self.at("means foreign")
        original = strand().move_to(pt(0, -.34))
        self.play(FadeIn(original), run_time=.80)
        self.at("you make a")
        self.play(FadeOut(foreign), FadeOut(protein), FadeIn(left), FadeIn(right),
                  TransformFromCopy(original, cdna), run_time=1.68)
        self.at("called cdna")
        self.play(FadeIn(cl), run_time=.42)
        self.at("or you start")
        self.play(ReplacementTransform(original, rna), run_time=1.20)
        self.at("its rna")
        self.play(FadeIn(rl), run_time=.42)
        self.at("deliver those instructions")
        self.play(FadeOut(cl), FadeOut(rl), run_time=.32)
        cdna.set_z_index(1)
        rna.set_z_index(1)
        self.play(transfer(cdna, cdna.get_center(), pt(-PAIR_X, .34)),
                  transfer(rna, rna.get_center(), pt(PAIR_X, .34)), run_time=2.35)
        self.at("common hosts are")
        self.play(FadeIn(label("HEK293", -PAIR_X, 3.15, size=33)), run_time=.58)
        self.at("and frog xenopus")
        self.play(FadeIn(label("Xenopus oocyte", PAIR_X, 3.15, size=33)), run_time=.58)
        self.finish()


class S04HowReadout(SpokenScene):
    def construct(self):
        left, right = oocyte(-PAIR_X), oocyte(PAIR_X)
        rna = strand(single=True).move_to(pt(PAIR_X, .34))
        protein = protein_at_surface(PAIR_X)
        self.add(left, right, rna)
        self.at("host builds the")
        self.play(TransformFromCopy(rna, protein), run_time=1.9)
        self.play(FadeOut(rna), run_time=.52)
        self.at("now add a stimulus")
        stimulus = VGroup(*(ions(x, .03, length=3.2, sideways=True, color=ORANGE)
                            for x in (-PAIR_X, PAIR_X)))
        # Offset their horizontal paths below the cell centres to keep the membrane protein clear.
        self.add(stimulus)
        self.at("compare with an")
        self.play(FadeIn(label("Untransfected control", -PAIR_X, 3.15, GREEN)),
                  FadeIn(label("Test cell", PAIR_X, 3.15, TEAL)), run_time=.65)
        p0, c0 = trace(-PAIR_X, flat, GREEN)
        p1, c1 = trace(PAIR_X, rise, YELLOW)
        self.at("control trace stays")
        self.play(FadeIn(p0), FadeIn(p1), FadeIn(scheme()), run_time=.4)
        self.play(Create(c0), run_time=1.10, rate_func=linear)
        self.at("test cell responds")
        self.play(Create(c1), run_time=1.48, rate_func=linear)
        self.at("heterologous expression tests")
        self.play(FadeIn(label("Molecular sufficiency", 0, -1.40, GOLD, 34)), run_time=.78)
        self.at("whether one protein")
        self.play(Indicate(protein, color=TEAL, scale_factor=1.24), run_time=1.14)
        self.at("produces a response")
        self.play(c1.animate.set_stroke(width=8), run_time=.75)
        self.finish()


def predict_world(motion=False):
    left, right = oocyte(-PAIR_X, motion), oocyte(PAIR_X, motion)
    heads = VGroup(label("Water control", -PAIR_X, 3.16, GREEN),
                   label("RNA-injected", PAIR_X, 3.16, TEAL))
    p0, c0 = trace(-PAIR_X, flat, GREEN)
    p1, c1 = trace(PAIR_X, rise, YELLOW)
    units = label("Chloride current", 0, -.94, YELLOW, 30)
    return left, right, heads, p0, c0, p1, c1, units, scheme(0, -2.43)


class S05PredictQ(SpokenScene):
    def construct(self):
        # Freeze local drift before the cut so the thinking pause carries the same composition.
        left, right, heads, p0, c0, p1, c1, units, note = predict_world(motion=True)
        self.add(left, right)
        t1 = pt(PAIR_X - .9, 1.54)
        t0 = pt(-PAIR_X + .9, 1.54)
        pip1 = tube(t1, pt(1.22, 3.15))
        pip0 = tube(t0, pt(-1.22, 3.15))
        rna = strand(single=True).scale(.61).move_to(pt(1.48, 2.65))
        water = Dot(pt(-1.5, 2.72), radius=.125, color=BLUE)
        self.at("test a classic")
        self.play(FadeIn(pip1, shift=DOWN * .3), run_time=1.5)
        self.at("you inject rna")
        self.play(FadeIn(rna), FadeIn(heads[1]), run_time=.55)
        self.play(rna.animate.move_to(pt(3.11, 1.18)), run_time=2.65)
        self.at("into frog oocytes")
        self.play(FadeOut(pip1), FadeOut(rna), FadeIn(p1), FadeIn(units), FadeIn(note), run_time=.65)
        self.at("chloride current appears")
        self.play(Create(c1), run_time=1.42, rate_func=linear)
        self.at("water injected oocytes")
        self.play(FadeIn(pip0), FadeIn(water), FadeIn(heads[0]), run_time=.55)
        self.play(water.animate.move_to(pt(-3.1, 1.14)), run_time=1.49)
        self.play(FadeOut(pip0), FadeOut(water), FadeIn(p0), run_time=.38)
        self.at("stay flat")
        self.play(Create(c0), run_time=1.25, rate_func=linear)
        self.at("does that prove")
        left.clear_updaters()
        right.clear_updaters()
        frozen_left, frozen_right, *_ = predict_world()
        self.play(FadeIn(question_card(QUESTION, **QUESTION_STYLE)),
                  Transform(left, frozen_left), Transform(right, frozen_right), run_time=.72)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    RING_AT = (5.9, -3.16, 0)
    SECONDS = 4.5

    def backdrop(self):
        return VGroup(*predict_world())

    def finish(self):
        # The script fixes the hold at 4.5 seconds, with the ring as its only motion.
        pass


def bilayer(y=.44):
    # The channel occupies the gap in both membrane leaflets.
    return VGroup(*(Line(pt(a, y + dy), pt(b, y + dy), color=GREY, stroke_width=12)
                    for a, b in ((-5.65, -.73), (.73, 5.65)) for dy in (-.15, .15)))


def surface_gauge(x, tracker, color):
    width = 2.9
    y = -2.20
    border = RoundedRectangle(width=width, height=.43, corner_radius=.08,
                              stroke_width=3, color=GREY).move_to(pt(x, y))

    def fill():
        w = (width - .18) * tracker.get_value()
        return Rectangle(width=w, height=.26, stroke_width=0, fill_color=color,
                         fill_opacity=.88).move_to(pt(x - width / 2 + .09 + w / 2, y))

    return VGroup(border, always_redraw(fill))


class S07Controls(SpokenScene):
    def construct(self):
        previous = predict_world()
        question = question_card(QUESTION, **QUESTION_STYLE)
        right = previous[1]
        self.add(*previous, question)
        detail = cell(0, -1.12, 5.55, 2.52, motion=False)
        native = gate(.35, 1.39, PURPLE, size=1.1)
        foreign = block().move_to(pt(-1.08, 1.34))
        native_label = place_label(T("Oocyte’s own channel", 33, PURPLE), native,
                                   dirs=(UP,), buff=.75)
        self.at("not yet")
        self.play(FadeOut(question), *[FadeOut(m) for m in previous if m is not right],
                  run_time=.44)
        self.play(Transform(right, detail), run_time=1.16)
        self.remove(right)
        right = cell(0, -1.12, 5.55, 2.52)
        self.add(right)
        self.at("oocytes carry chloride")
        self.play(FadeIn(native), run_time=.60)
        self.play(FadeIn(native_label), run_time=.54)
        self.at("and foreign proteins")
        self.play(FadeIn(foreign, shift=UP * .32), run_time=.75)
        self.at("switch them on")
        self.play(native.plug.animate.set_opacity(0), run_time=.5)
        stream = ions(.35, 1.42, 2.35)
        self.add(stream)
        self.at("good experiments include")
        control, test, heads, *_ = predict_world(motion=True)
        self.play(FadeOut(native_label), run_time=.30)
        self.play(FadeOut(right), FadeOut(native),
                  FadeOut(foreign), FadeOut(stream), FadeIn(control), FadeIn(test),
                  FadeIn(heads), run_time=1.03)
        protein = protein_at_surface(PAIR_X)
        self.play(FadeIn(protein), run_time=.60)
        self.at("and match surface")
        # Compare levels only between protein-expressing test conditions.
        self.play(FadeOut(heads), run_time=.30)
        other = protein_at_surface(-PAIR_X)
        lv, rv = ValueTracker(.31), ValueTracker(.73)
        gauges = VGroup(surface_gauge(-PAIR_X, lv, TEAL), surface_gauge(PAIR_X, rv, TEAL))
        surface = label("Surface level", 0, -2.2, TEXT, 30)
        levels = scheme(0, -2.95)
        self.play(FadeIn(other), FadeIn(gauges), FadeIn(surface), FadeIn(levels), run_time=.72)
        self.play(lv.animate.set_value(.73), run_time=2.2)
        self.at("different amounts alone")
        self.play(gauges.animate.set_stroke(width=4), run_time=1.05)
        self.at("to show one protein")
        isolated = block(width=1.42, height=.85).move_to(pt(0, .44))
        membrane = bilayer()
        self.play(FadeOut(control), FadeOut(test), FadeOut(other), FadeOut(gauges),
                  FadeOut(surface), FadeOut(levels), FadeIn(membrane),
                  ReplacementTransform(protein, isolated), run_time=1.45)
        self.at("purify it into")
        pore = gate(0, .44, closed=False, size=1.34)
        self.play(ReplacementTransform(isolated, pore), run_time=.58)
        self.play(FadeIn(label("Lipid bilayer", 0, 3.12, size=34)), run_time=.42)
        self.add(ions(0, .44, 4.5))
        self.finish()


def animal(x, y):
    """A simple animal silhouette for the intact-animal experiment."""
    color = "#8293A7"
    body = Ellipse(width=2.36, height=1.27, fill_opacity=.58, color=color, stroke_width=3)
    head = Circle(radius=.41, color=color, fill_color=color, fill_opacity=.66).shift(pt(1.12, .29))
    ear = Circle(radius=.23, stroke_width=2, color=color, fill_opacity=.75).shift(pt(.94, .64))
    nose = Polygon(pt(1.23, .39), pt(1.66, .13), pt(1.24, .02),
                   color=color, fill_opacity=.72, stroke_width=2)
    tail = CubicBezier(pt(-1.05, -.12), pt(-2.03, -.5), pt(-2.1, .46), pt(-1.77, .45))
    tail.set_stroke(color, 5, opacity=.65)
    return VGroup(tail, body, head, ear, nose).move_to(pt(x, y))


class S08Limits(SpokenScene):
    def construct(self):
        old_mem = bilayer()
        old_gate = gate(0, .44, closed=False, size=1.34)
        old_ions = ions(0, .44, 4.5)
        self.add(old_mem, old_gate, old_ions, label("Lipid bilayer", 0, 3.12, size=34))
        panels = TwoPanel("No current", "Foreign-cell response", colors=(TEXT, TEXT),
                          top=3.38, bottom=-2.75, width=12.6, size=32)
        left = cell(-PAIR_X, .36, 1.9, 1.64)
        p0, c0 = trace(-PAIR_X, flat, GREEN, y=-2.30, half_width=2.01, height=.7)
        self.at("two limits keep")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(left), run_time=1.1)
        self.at("first no current")
        self.play(FadeIn(panels.left_frame), FadeIn(panels.left_head), FadeIn(p0),
                  FadeIn(scheme(0, -3.16)), run_time=.58)
        self.play(Create(c0), run_time=1.38, rate_func=linear)
        self.at("mutant protein may")
        state = label("Absent", -PAIR_X, 2.39, TEAL, 32)
        self.play(FadeIn(state), run_time=.55)
        self.at("mislocalized", lead=.28)
        interior = block().move_to(pt(-PAIR_X + .15, .55))
        misplaced = label("Mislocalized", -PAIR_X, 2.39, TEAL, 32)
        self.play(FadeIn(interior), swap(state, misplaced, .44), run_time=.44)
        self.at("or unable to conduct", lead=.1)
        plugged = gate(-PAIR_X + 1.79, .55, closed=True, size=.7).rotate(PI / 2)
        blocked = label("No conduction", -PAIR_X, 2.39, TEAL, 32)
        self.play(ReplacementTransform(interior, plugged), swap(misplaced, blocked, .68), run_time=.68)
        self.at("second a response")
        right = cell(PAIR_X, .80, 1.78, 1.52)
        protein = block().move_to(
            pt(PAIR_X + 1.78 * np.cos(.75), .80 + 1.52 * np.sin(.75))
        ).rotate(-.6)
        p1, c1 = trace(PAIR_X, rise, YELLOW, y=-2.30, half_width=2.01, height=.7)
        self.play(FadeIn(panels.right_frame), FadeIn(panels.right_head), FadeIn(right),
                  FadeIn(protein), FadeIn(p1), run_time=.85)
        self.play(Create(c1), run_time=1.6, rate_func=linear)
        self.at("testing whether an")
        whole = animal(-PAIR_X, .18)
        marker = strand().scale(.57).move_to(pt(-PAIR_X, .18))
        query = label("?", -PAIR_X, 1.36, GOLD, 45)
        necessity = label("Animal necessity", -3.25, 2.93, size=32)
        self.play(FadeOut(left), FadeOut(plugged), FadeOut(p0), FadeOut(c0),
                  FadeOut(blocked), swap(panels.left_head, necessity, .56), run_time=.56)
        self.play(FadeIn(whole), FadeIn(marker), FadeIn(query), run_time=.75)
        self.at("requires removing it")
        self.play(FadeOut(marker, shift=UP * .5), run_time=.83)
        self.finish()


def pool(x, y, selected=False):
    b = RoundedRectangle(width=.55, height=.86, corner_radius=.11, stroke_width=2.4,
                         color=BLUE, fill_color=CELL_FILL, fill_opacity=.94)
    content = Rectangle(width=.35, height=.32, stroke_width=0, fill_color=TEAL,
                        fill_opacity=1 if selected else .78).shift(DOWN * .16)
    cap = Line(pt(-.32, .40), pt(.32, .40), stroke_width=5, color=BLUE)
    return VGroup(b, content, cap).move_to(pt(x, y))


class S09Unlocked1(SpokenScene):
    def construct(self):
        hek = cultured()
        # Retain the cultured cell's established location and keep plots and equipment on the right.
        date = label("1997", 0, 3.22, GOLD, 35)
        hek_name = label("HEK cells", -PAIR_X, 2.78)
        row = VGroup(*(pool(1.15 + .81 * i, 1.67) for i in range(5)))
        lower = VGroup(*(pool(1.55 + .81 * i, .57) for i in range(4)))
        pools = VGroup(row, lower)
        gene_name = label("cDNA pools", 2.78, 2.69, TEAL)
        pore = gate(-PAIR_X, 2.19, TEAL, closed=True, size=.85)
        self.at("even so the", lead=.2)
        self.play(DrawBorderThenFill(hek), run_time=2.0)
        self.at("in 1997")
        self.play(FadeIn(date), run_time=.54)
        self.at("catarina julius")
        self.play(LaggedStart(*(FadeIn(m, shift=UP * .23) for m in pools), lag_ratio=.4),
                  run_time=1.26)
        self.play(FadeIn(gene_name), run_time=.45)
        self.at("put pools of")
        sample = strand(TEAL).move_to(pt(2.6, -.42))
        self.play(TransformFromCopy(lower[1], sample), run_time=.8)
        self.play(transfer(sample, sample.get_center(), pt(-PAIR_X, .45), 1.18),
                  run_time=1.97)
        self.play(FadeIn(hek_name), run_time=.48)
        self.at("watched for calcium")
        p, c = trace(2.8, rise, YELLOW, y=-2.30, half_width=2.23, height=1.12)
        cal = label("Calcium entry", 2.8, -.78, YELLOW, 30)
        self.play(FadeIn(p), FadeIn(cal), FadeIn(scheme(2.8, -2.88)), run_time=.65)
        self.at("when they added")
        stimulus = Dot(pt(-4.96, 2.18), radius=.18, color=ORANGE)
        cap = label("Capsaicin", -4.45, 3.40, ORANGE, 30)
        entry_x = -3.77
        self.play(FadeIn(stimulus), FadeIn(cap), run_time=.32)
        self.play(stimulus.animate.move_to(pt(entry_x, 1.91)), run_time=.42)
        stream = ions(entry_x, 1.54, 1.95)
        self.add(stream)
        self.play(Create(c), run_time=1.9, rate_func=linear)
        self.at("splitting a responding")
        self.play(FadeOut(stream), FadeOut(stimulus), FadeOut(cap), FadeOut(sample),
                  FadeOut(row), FadeOut(gene_name), run_time=.45)
        picked = pool(2.34, .98, selected=True)
        self.play(ReplacementTransform(lower, picked), run_time=.66)
        selected = strand().move_to(pt(2.34, .98))
        self.play(ReplacementTransform(picked, selected), run_time=.59)
        self.at("trpv1", lead=.35)
        name = label("TRPV1", 2.34, 2.69, TEAL, 35)
        self.play(FadeIn(name), run_time=.45)
        self.play(transfer(selected, selected.get_center(), pt(-PAIR_X, .45), height=.58), run_time=.9)
        self.play(ReplacementTransform(selected, pore), FadeOut(hek_name), run_time=.56)
        self.at("in those foreign cells", lead=-.95)
        temp = ValueTracker(.12)
        gauge = dial(temp, pt(2.75, -.04), radius=1.67, label="Temperature", color=ORANGE,
                     fmt="{:.0f} °C", scale=50, size=33)
        # A schematic temperature cue, not a measured temperature record.
        self.play(FadeOut(p), FadeOut(c), FadeOut(cal), run_time=.3)
        self.play(FadeIn(gauge), run_time=.48)
        self.play(temp.animate(rate_func=linear).set_value(.84), run_time=1.72)
        self.at("43 degrees celsius", lead=.20)
        self.play(temp.animate.set_value(.89), pore.plug.animate.set_opacity(0), run_time=.62)
        self.add(ions(-PAIR_X, 2.18, 1.67))
        self.finish()


def junction_cells(motion=True):
    return cell(-2.55, .28, 2.48, 2.43, motion=motion), cell(2.55, .28, 2.48, 2.43, motion=motion)


class S10Unlocked2(SpokenScene):
    def construct(self):
        expression = cell(-PAIR_X, .56, 2.04, 2.04)
        pore = gate(-PAIR_X, 2.60, size=.79, closed=False)
        markers = VGroup(*(Dot(pt(-PAIR_X + 1.87 * np.cos(a), .56 + 1.87 * np.sin(a)),
                               radius=.112, color=ORANGE)
                          for a in np.linspace(PI + .27, TAU - .27, 9)))
        year = label("2006", 0, 3.15, GOLD, 35)
        k_name = label("KCNQ2/KCNQ3", 2.90, 2.53, TEAL, 34)
        p, c = trace(2.68, fall, YELLOW, y=-1.66, half_width=2.39, height=2.61)
        current = label("Potassium current", 2.68, 1.46, YELLOW, 32)
        note = scheme(2.68, -2.11)
        self.add(expression, year)
        self.at("expressed potassium channels")
        self.play(FadeIn(pore, shift=UP * .16), run_time=.77)
        self.play(FadeIn(k_name), FadeIn(markers), run_time=.65)
        self.at("depleting one membrane")
        lipid = label("PIP2", -PAIR_X, -2.40, ORANGE, 32)
        self.play(FadeIn(lipid), FadeIn(p), FadeIn(current), FadeIn(note), run_time=.55)
        self.play(LaggedStart(*(FadeOut(m, scale=.5) for m in markers), lag_ratio=.24),
                  run_time=2.23)
        self.at("made the current fall")
        self.play(Create(c), pore.plug.animate.set_opacity(1), run_time=2.48, rate_func=linear)
        self.at("in 2020")
        left, right = junction_cells(motion=False)
        right.shift(RIGHT * .65)
        left.shift(LEFT * .65)
        future = label("2020", 0, 3.15, GOLD, 35)
        self.play(*[FadeOut(m) for m in (lipid, k_name, current, note)], run_time=.32)
        self.play(*[FadeOut(m) for m in (expression, pore, p, c)],
                  swap(year, future), FadeIn(left), FadeIn(right), run_time=1.0)
        self.at("paired xenopus oocytes")
        # Rebuild at the destination so their drift anchors also follow the move.
        left.clear_updaters(recursive=True)
        right.clear_updaters(recursive=True)
        self.play(left.animate.shift(RIGHT * .65), right.animate.shift(LEFT * .65), run_time=1.6)
        self.remove(left, right)
        left, right = junction_cells()
        self.add(left, right)
        self.at("two worm junction")
        connector = VGroup(*(Line(pt(-.47, .28 + d), pt(.47, .28 + d), color=TEAL, stroke_width=11)
                             for d in (-.18, .18)))
        self.play(Create(connector), run_time=.62)
        self.play(FadeIn(label("UNC-9", -2.72, -2.65, TEAL, 35)),
                  FadeIn(label("UNC-7b", 2.72, -2.65, TEAL, 35)), run_time=.59)
        self.at("current strongly favored")
        arrow = Arrow(pt(-2.18, .28), pt(2.37, .28), color=YELLOW, buff=0,
                      tip_length=.36, stroke_width=8)
        self.play(GrowArrow(arrow), run_time=.85)
        self.add(ions(.03, .28, 3.9, sideways=True))
        back = Arrow(pt(1.19, -.86), pt(.30, -.86), color=GREY, buff=0, tip_length=.18,
                     stroke_width=3).set_opacity(.65)
        stop = Line(pt(.20, -1.03), pt(.20, -.69), color=RED, stroke_width=5)
        self.play(GrowArrow(back), Create(stop), run_time=.64)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        native = cell(-4.30, .25, 1.75, 1.65, crowded=True)
        foreign = cell(.55, .10, 1.85, 1.75)
        protein = block().move_to(pt(.55 + 1.11, .10 + 1.40)).rotate(-.60)
        gene = strand().move_to(pt(-4.30, .25))
        self.add(native, foreign, gene)
        self.at("moving one gene")
        self.play(transfer(gene, gene.get_center(), pt(.55, .10), 1.40), run_time=1.45)
        self.play(ReplacementTransform(gene, protein), run_time=.67)
        self.at("strips away the crowd")
        self.play(FadeOut(native), run_time=1.10)
        self.at("with careful controls")
        control = cell(-3.91, -.40, 1.43, 1.35)
        ctrl = label("Control", -3.91, 2.97, GREEN, 32)
        p0, c0 = trace(-3.91, flat, GREEN, y=-2.75, half_width=1.43, height=.62)
        self.play(FadeIn(control), FadeIn(ctrl), FadeIn(p0), run_time=.72)
        self.play(Create(c0), run_time=1.19, rate_func=linear)
        self.at("what one protein")
        p1, c1 = trace(.55, rise, YELLOW, y=-3.26, half_width=1.69, height=.74)
        self.play(FadeIn(p1), FadeIn(scheme(3.56, -3.30)), run_time=.42)
        self.play(Create(c1), run_time=1.35, rate_func=linear)
        self.at("whether an intact")
        whole = animal(4.71, .38).scale(.80)
        tail, *silhouette = whole
        tail.set_fill(opacity=0).set_stroke(opacity=.40)
        for part in silhouette:
            part.set_opacity(.62)
        query = label("?", 4.76, 1.71, GOLD, 53)
        self.play(FadeIn(whole, shift=UP * .20), run_time=.72)
        self.play(FadeIn(query), run_time=.63)
        self.finish()


class S12End(EndCard):
    LINE = "A foreign cell tests what one protein can do, not animal need."
