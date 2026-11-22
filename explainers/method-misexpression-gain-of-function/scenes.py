"""Putting a Gene in the Wrong Place.

Colour map: grey tissue, blue glass and electrical pulses, orange DNA,
yellow added factors, purple p3/Nkx2.2, teal pMN/Pax6, green floor plate
and induced floor-plate identity. Gold marks questions, dates, and existing
cell machinery. Red marks cautions.
"""

from bp_parts import *  # noqa: F403
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SLATE = "#354662"
MEMBRANE = "#8294AE"
FLOOR = "#527C51"
P3 = "#745594"
PMN = "#2D6E7A"
INACTIVE = "#39434F"
QUESTION = "What happens to Pax6 and the border?"
OUTER = (0.65, 1.72, 2.46, 2.95, 3.24, 3.37, 3.29, 3.00, 2.50, 1.63, 0.65)
INNER = (0.025, 0.29, 0.63, 0.86, 0.99, 1.03, 0.96, 0.83, 0.64, 0.31, 0.025)
DNA_SEEDS = ((0, 0.47), (-0.29, -0.10), (0.34, -0.42), (-0.18, 0.94),
             (0.45, 0.23), (-0.49, -0.57), (0.14, -0.93))


def point(x, y):
    return np.array([x, y, 0.0])


def row_y(index, close=False):
    return -2.55 + index * (0.716 if close else 0.505)


def cell_tile(points, color, outline=MEMBRANE):
    return Polygon(*points, stroke_color=outline, stroke_width=1.7,
                   fill_color=color, fill_opacity=1).round_corners(0.085)


def cell_color(index, side, stage):
    if stage in ("hook", "moved"):
        return P3 if index in (4, 5) and (side < 0 or stage == "moved") else SLATE
    if stage == "pulsed":
        return "#78682F" if side > 0 else SLATE
    if stage in ("floor", "p3", "pMN", "shifted", "shh", "induced"):
        if index == 0:
            return FLOOR
        if stage == "induced" and side > 0 and index in (6, 7):
            return FLOOR
        if stage in ("p3", "pMN", "shifted"):
            border = 5 if stage == "shifted" and side > 0 else 3
            if index < border:
                return P3
            if stage != "p3" and index <= 5:
                return PMN
    return SLATE


def tube(stage="neutral", close=False):
    """Build matching cell rows with a hollow lumen in both views."""
    walls = VGroup()
    for side in (-1, 1):
        rows = VGroup()
        for index in range(7 if close else 10):
            factor = 1.08 if close else 1.0

            def vertex(edge, fraction):
                x = INNER[edge] + fraction * (OUTER[edge] - INNER[edge])
                return point(side * factor * x, row_y(edge, close))

            row = VGroup()
            for a, b in ((0, 0.48), (0.48, 1)):
                vertices = (vertex(index, a), vertex(index, b),
                            vertex(index + 1, b), vertex(index + 1, a))
                tile = cell_tile(vertices, cell_color(index, side, stage))
                nucleus = Ellipse(width=0.20, height=0.12, stroke_width=0,
                                  fill_color=TEXT, fill_opacity=0.31)
                nucleus.move_to(np.mean(vertices, axis=0)).rotate(side * 0.19)
                row.add(VGroup(tile, nucleus))
            rows.add(row)
        walls.add(rows)
    return walls


def animate_tissue(walls, stage, sides=(0, 1), strength=0.065):
    """A slow light ripple through the existing cell shapes."""
    phase = [0.0]
    tiles = [(column[0], ManimColor(cell_color(index, 2 * side - 1, stage)), index + col * 0.7)
             for side in sides for index, row in enumerate(walls[side])
             for col, column in enumerate(row)]
    light = ManimColor(TEXT)

    def update(_walls, dt):
        phase[0] += dt
        for tile, color, offset in tiles:
            amount = strength * (1.15 + np.sin(2.35 * phase[0] - 0.63 * offset))
            tile.set_fill(interpolate_color(color, light, amount))

    walls.add_updater(update)


def side_label(text, x, y, color=TEXT):
    return fit_text(text, max_w=2.8, size=31, min_size=28, max_lines=3,
                    color=color).move_to(point(x, y))


def factor_dot(color=YELLOW, radius=0.115):
    return VGroup(Dot(radius=radius * 1.7, color=color, fill_opacity=0.24),
                  Dot(radius=radius, color=color))


def dna_cloud():
    return VGroup(*(factor_dot(ORANGE, 0.073).move_to(point(x, y)) for x, y in DNA_SEEDS))


def drift_dna(cloud):
    phase = [0.0]

    def update(group, dt):
        phase[0] += dt
        for i, (dot, (x, y)) in enumerate(zip(group, DNA_SEEDS)):
            t = phase[0] * 1.4 + i * 1.1
            dot.move_to(point(x + 0.14 * (np.sin(t) - np.sin(i * 1.1)),
                              y + 0.19 * (np.cos(t) - np.cos(i * 1.1))))

    cloud.add_updater(update)


def pulse_arc(start, end):
    return ParametricFunction(
        lambda u: interpolate(start, end, u) + UP * 0.16 * np.sin(4 * PI * u),
        t_range=(0, 1, 0.025), color=BLUE, stroke_width=4,
    )


def sweep_pulses(scene, y, seconds=1.1):
    arcs = [pulse_arc(point(-0.87, y + d), point(0.98, y + d)) for d in (-0.22, 0.22)]
    scene.play(LaggedStart(*(Succession(Create(arc), FadeOut(arc)) for arc in arcs),
                           lag_ratio=0.75), run_time=seconds)


def repaint(scene, walls, stage, seconds, close=False):
    walls.clear_updaters()
    scene.play(Transform(walls, tube(stage, close)), run_time=seconds)
    animate_tissue(walls, stage)


def domain_border(side, index=3, color=TEXT):
    scale = 1.08 * side
    return Line(point(INNER[index] * scale, row_y(index, True)),
                point(OUTER[index] * scale, row_y(index, True)),
                color=color, stroke_width=4)


def domain_labels():
    return VGroup(side_label("Floor plate", -5.12, -2.17, GREEN),
                  side_label("p3 · Nkx2.2", -5.12, -1.13, PURPLE),
                  side_label("pMN · Pax6", -5.12, 0.75, TEAL))


def inhibition():
    y = row_y(3, True)
    arrows = VGroup()
    for x, direction, color in ((-2.70, UP, PURPLE), (-1.67, DOWN, TEAL)):
        end = point(x, y) + direction * 0.40
        start = point(x, y) - direction * 0.40
        arrows.add(VGroup(Line(start, end, color=color, stroke_width=4),
                          Line(end + LEFT * 0.13, end + RIGHT * 0.13, color=color, stroke_width=4)))
    return arrows


def right_factor():
    return VGroup(*(factor_dot(PURPLE, 0.105).move_to(point(x, y))
                    for x, y in ((1.58, 0.03), (2.12, 0.33), (1.84, 0.75), (2.72, 0.86))))


def predict_card():
    return question_card(QUESTION, y=3.15, size=36, max_w=10.4)


def tissue_patch(color=INACTIVE, receptor=False):
    """Two adjacent membrane cartoons for a receptor-controlled response."""
    tissue = VGroup()
    for index in range(2):
        x = (index - 0.5) * 1.56
        cell = RoundedRectangle(width=1.49, height=1.65, corner_radius=0.32,
                                stroke_color=MEMBRANE, stroke_width=2.4,
                                fill_color=color, fill_opacity=1).move_to(point(x, 0))
        nucleus = Ellipse(width=0.37, height=0.23, stroke_width=0,
                          fill_color=TEXT, fill_opacity=0.3).move_to(point(x, -0.28))
        nucleus.set_z_index(1)
        body = VGroup(cell, nucleus)
        if receptor:
            notch = VMobject(stroke_color=BLUE, stroke_width=6)
            notch.set_points_as_corners([point(x - 0.21, 0.99), point(x - 0.21, 0.74),
                                        point(x + 0.21, 0.74), point(x + 0.21, 0.99)])
            notch.set_z_index(2)
            body.add(notch)
        tissue.add(body)
    return tissue


class S01Hook(SpokenScene):
    def construct(self):
        walls = tube("hook")
        stripe = VGroup(*(factor_dot(PURPLE, 0.09).move_to(point(-1.76 - 0.31 * i, -0.24 + 0.14 * i))
                          for i in range(4)))
        self.add(walls, stripe, scope_tag())
        animate_tissue(walls, "hook")
        for i, dot in enumerate(stripe):
            bob(dot, amp=0.10, speed=2.1, seed=i)
        self.at("Does it command")
        mark = T("?", 88, GOLD).move_to(point(-4.85, 0.10))
        self.play(FadeIn(mark, shift=UP * 0.22), run_time=0.65)
        self.at("cannot separate")
        cause = side_label("Cause?", -5.10, 0.64, GOLD)
        marker = side_label("Label?", -5.10, -0.55)
        self.play(FadeOut(mark), run_time=0.30)
        self.play(FadeIn(cause, shift=UP * 0.22), FadeIn(marker, shift=DOWN * 0.22), run_time=0.65)
        self.at("To test its power")
        moving = factor_dot(PURPLE).move_to(stripe[2])
        track = CubicBezier(moving.get_center(), point(-1.30, 1.37),
                            point(1.22, 1.37), point(2.00, -0.02))
        self.play(FadeOut(cause), FadeOut(marker), MoveAlongPath(moving, track), run_time=2.0)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Misexpression, electroporation and gain-of-function tests"
    TITLE = "Putting a Gene in the Wrong Place"

    def construct(self):
        walls = tube("hook").set_opacity(0.10)
        lesson = T(self.LESSON, 28, BLUE)
        title = fit_text(self.TITLE, max_w=11.15, size=53, min_size=38, font=TITLE_FONT)
        stack = VGroup(lesson, title).arrange(DOWN, buff=0.24)
        self.add(walls, stack.shift(DOWN * 0.08))
        animate_tissue(walls, "hook")
        self.play(stack.animate.shift(UP * 0.08), run_time=0.40)
        self.wait(1.60)


class S03Misexpression(SpokenScene):
    def construct(self):
        walls = tube("hook")
        signal = factor_dot(PURPLE).move_to(point(2, -0.02))
        self.add(walls, signal)
        bob(signal, amp=0.11)
        self.at("Making a protein")
        repaint(self, walls, "moved", 2.55)
        self.at("is called misexpression")
        term = side_label("Misexpression", 5.04, 0.48, PURPLE)
        self.play(FadeIn(term), run_time=0.50)
        self.at("To test a gene")
        self.play(FadeOut(term), FadeOut(signal), run_time=0.52)
        repaint(self, walls, "neutral", 0.84)
        pipette = Polygon(point(-0.48, 3.48), point(0.03, 3.56), point(0.16, 1.32),
                          point(0.08, 0.83), point(-0.04, 1.30), color=BLUE,
                          stroke_width=2, fill_color=BLUE, fill_opacity=0.30)
        self.at("researchers inject")
        self.play(FadeIn(pipette, shift=DOWN * 0.37), run_time=0.65)
        cloud = dna_cloud()
        self.play(LaggedStart(*(GrowFromPoint(dot, point(0.08, 0.83)) for dot in cloud),
                               lag_ratio=0.15), run_time=1.85)
        self.add(cloud)
        drift_dna(cloud)
        self.at("At first")
        self.play(FadeOut(pipette, shift=UP * 0.19), run_time=0.8)
        label = side_label("DNA in\nthe canal", 5.0, 0.27, ORANGE)
        self.play(FadeIn(label), run_time=0.6)
        self.finish()


class S04Electroporation(SpokenScene):
    def construct(self):
        walls, cloud = tube(), dna_cloud()
        label = side_label("DNA in\nthe canal", 5.0, 0.27, ORANGE)
        self.add(walls, cloud, label)
        drift_dna(cloud)
        animate_tissue(walls, "neutral")
        self.at("brief electric pulses")
        self.play(FadeOut(label), run_time=0.20)
        sweep_pulses(self, -0.05, seconds=0.88)
        self.at("push DNA into")
        cloud.clear_updaters()
        targets = (point(1.49, 0.44), point(1.75, -0.07), point(2.00, -0.45),
                   point(2.04, 0.93), point(2.55, 0.24), point(2.06, -0.71), point(1.49, -0.92))
        self.play(LaggedStart(*(dot.animate.move_to(dest) for dot, dest in zip(cloud, targets)),
                               lag_ratio=0.14), run_time=2.32)
        self.at("That is electroporation")
        term = side_label("Electroporation", 5.03, 0.30, BLUE)
        self.play(FadeIn(term), run_time=0.60)
        self.at("makes the protein")
        self.play(FadeOut(term), FadeOut(cloud), run_time=0.42)
        repaint(self, walls, "pulsed", 1.25)
        pulsed = side_label("Electroporated\nside", 5.14, 0.24, YELLOW)
        control = side_label("Control side", -5.14, 0.24)
        self.play(FadeIn(pulsed), run_time=0.45)
        self.at("untouched control")
        self.play(FadeIn(control), run_time=0.55)
        self.at("Adding a factor elsewhere")
        added = factor_dot().move_to(point(2.12, 0.23))
        self.play(GrowFromCenter(added), run_time=0.62)
        bob(added, amp=0.13)
        self.at("tests sufficiency")
        banner = caption("Tests sufficiency: what it can impose", 32, GOLD, y=-3.15)
        self.play(FadeIn(banner, shift=UP * 0.10), run_time=0.78)
        self.finish()


class S05PredictQ(SpokenScene):
    def construct(self):
        walls = tube("pulsed")
        animate_tissue(walls, "pulsed")
        pulsed = side_label("Electroporated\nside", 5.14, 0.24, YELLOW)
        control = side_label("Control side", -5.14, 0.24)
        banner = caption("Tests sufficiency: what it can impose", 32, GOLD, y=-3.15)
        added = factor_dot().move_to(point(2.12, 0.23))
        self.add(walls, pulsed, control, banner, added)
        self.at("Predict a result")
        walls.clear_updaters()
        self.play(FadeOut(VGroup(pulsed, control, banner, added)), run_time=0.42)
        upper_rows = VGroup(*(row for side in walls for row in side[7:]))
        self.play(FadeOut(upper_rows), run_time=0.52)
        lower_rows = VGroup(*(VGroup(*side[:7]) for side in walls))
        self.remove(walls)
        self.add(lower_rows)
        self.play(Transform(lower_rows, tube("floor", close=True)), run_time=1.42)
        animate_tissue(lower_rows, "floor")
        floor, p3, pmn = domain_labels()
        self.at("the floor plate")
        self.play(FadeIn(floor), run_time=0.5)
        self.at("stripe p3 makes")
        repaint(self, lower_rows, "p3", 1.10, close=True)
        self.play(FadeIn(p3), run_time=0.52)
        self.at("The stripe above")
        repaint(self, lower_rows, "pMN", 1.40, close=True)
        borders = VGroup(domain_border(-1), domain_border(1))
        self.play(Create(borders), run_time=0.60)
        self.at("a low level of")
        self.play(FadeIn(pmn), run_time=0.60)
        self.at("Each factor switches")
        blunt = inhibition()
        self.play(LaggedStart(*(GrowFromCenter(a) for a in blunt), lag_ratio=0.35), run_time=1.36)
        self.at("Now pulse it into")
        self.play(FadeOut(blunt), run_time=0.35)
        sweep_pulses(self, 0.50)
        dots = right_factor()
        self.play(LaggedStart(*(GrowFromPoint(dot, point(0.76, 0.50)) for dot in dots),
                               lag_ratio=0.16), run_time=1.52)
        self.at("What happens to")
        self.play(FadeIn(predict_card()), run_time=0.60)
        self.finish()


class S06PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(tube("pMN", close=True), domain_labels(), domain_border(-1),
                 domain_border(1), right_factor(), predict_card())
        self.wait(float(os.environ["KX_DURATION"]))


class S07PredictAnswer(SpokenScene):
    def construct(self):
        walls = tube("pMN", close=True)
        left, right = domain_border(-1), domain_border(1)
        dots, names, q = right_factor(), domain_labels(), predict_card()
        self.add(walls, names, left, right, dots, q)
        animate_tissue(walls, "pMN", sides=(1,), strength=0.13)
        self.at("On the pulsed right")
        self.play(FadeOut(q), run_time=0.68)
        nk = side_label("Nkx2.2", 5.14, 0.46, PURPLE)
        self.play(FadeIn(nk), run_time=0.55)
        self.at("switches pac")
        walls.clear_updaters()
        muted = walls.copy()
        for row in (3, 4):
            for tile, nucleus in muted[1][row]:
                tile.set_fill(INACTIVE)
        self.play(Transform(walls, muted), FadeOut(dots), run_time=1.65)
        self.at("The border shifts")
        right_shifted = domain_border(1, index=5)
        self.play(Transform(walls, tube("shifted", close=True)),
                  Transform(right, right_shifted), run_time=2.46)
        animate_tissue(walls, "shifted", sides=(1,), strength=0.145)
        self.at("Meanwhile the untouched")
        reference = DashedLine(left.get_start(), domain_border(1).get_end(),
                               dash_length=0.15, color=TEXT, stroke_width=2.4)
        self.play(Create(reference), run_time=1.75)
        control = side_label("Same-embryo\ncontrol", -5.12, 1.70)
        self.at("in the same embryo")
        self.play(FadeIn(control), run_time=0.7)
        self.at("Brisco and colleagues")
        tag = caption("Chick neural tube", 29, GREY, y=-3.12)
        self.play(FadeIn(tag), run_time=0.55)
        pulse(right, base=4.3, amp=1.7, speed=2.5)
        self.finish()


def other_tissue():
    return tissue_patch().scale(1.26).move_to(point(3.59, -0.13))


def context_controls():
    wall = tube("shifted", close=True).scale(0.73).move_to(point(-3.50, -0.12))
    remote = other_tissue()
    signal = factor_dot(PURPLE).move_to(point(4.26, 0.48))
    name = side_label("Other tissue", 3.59, 1.47)
    note = caption("Can impose ≠ normal need", 33, RED, y=-3.15)
    return wall, remote, signal, name, note


class S08LimitsContext(SpokenScene):
    def construct(self):
        walls = tube("shifted", close=True)
        left, right = domain_border(-1), domain_border(1, 5)
        reference = DashedLine(left.get_start(), domain_border(1).get_end(),
                               dash_length=0.15, color=TEXT, stroke_width=2.4)
        names = VGroup(domain_labels(), side_label("Same-embryo\ncontrol", -5.12, 1.70),
                       side_label("Nkx2.2", 5.14, 0.46, PURPLE),
                       caption("Chick neural tube", 29, GREY, y=-3.12))
        inset, remote, transfer, other, note = context_controls()
        self.add(walls, left, right, reference, names)
        self.at("misexpression can mislead")
        self.play(FadeOut(VGroup(names, reference)), run_time=0.55)
        self.play(Transform(walls, inset), FadeOut(left), FadeOut(right), run_time=1.52)
        animate_tissue(walls, "shifted", strength=0.14)
        detail = RoundedRectangle(width=4.36, height=3.38, corner_radius=0.79,
                                  stroke_color=MEMBRANE, stroke_width=3,
                                  fill_color=SLATE, fill_opacity=1).move_to(point(3.59, -0.13))
        helpers = VGroup(
            RoundedRectangle(width=0.53, height=0.25, corner_radius=0.08, stroke_width=0,
                             fill_color=GREY, fill_opacity=0.55).move_to(point(2.65, 0.21)),
            Circle(radius=0.20, stroke_width=0, fill_color=GREY,
                   fill_opacity=0.55).move_to(point(3.77, 0.61)),
            RoundedRectangle(width=0.29, height=0.48, corner_radius=0.08, stroke_width=0,
                             fill_color=GREY, fill_opacity=0.55).move_to(point(4.36, -0.62)),
        )
        signal = factor_dot(PURPLE, 0.19).move_to(point(3.55, -0.30))
        self.at("A factor is sufficient")
        self.play(FadeIn(detail), FadeIn(helpers), run_time=0.84)
        self.play(GrowFromCenter(signal), run_time=0.80)
        bob(signal, amp=0.22, speed=1.65)
        machinery = fit_text("Existing cell machinery", max_w=4.2, size=31,
                             min_size=28, color=GOLD).move_to(point(3.59, 2.12))
        self.at("using their existing")
        self.play(LaggedStart(*(helper.animate.set_fill(GOLD, 1) for helper in helpers),
                              lag_ratio=0.25, run_time=1.4),
                  FadeIn(machinery, run_time=0.60))
        self.at("Shifting a border")
        self.play(FadeOut(machinery), FadeOut(helpers), FadeOut(signal), run_time=0.55)
        self.play(ReplacementTransform(detail, remote), run_time=1.04)
        self.play(FadeIn(other), run_time=0.53)
        start = point(-2.22, 0.19)
        path = CubicBezier(start, point(-0.85, 1.3), point(2.3, 1.14), transfer.get_center())
        transfer.move_to(start)
        self.play(MoveAlongPath(transfer, path), run_time=2.22)
        bob(transfer, amp=0.19, speed=1.7)
        self.at("Nor does it prove")
        caution = T("!", 39, RED, weight=BOLD).move_to(point(-4.05, -3.15))
        self.play(FadeIn(note), FadeIn(caution), run_time=0.7)
        self.finish()


def comparison():
    panels = TwoPanel("Gain and loss", "Pathway test", colors=(GOLD, BLUE),
                      top=2.85, bottom=-2.56, width=12.4)
    x1, x2 = (panels.area(side)[0][0] for side in ("left", "right"))
    gain = tissue_patch(receptor=True).move_to(point(x1 + 0.35, 0.73))
    loss = tissue_patch(receptor=True).move_to(point(x1 + 0.35, -1.40))
    pathway = tissue_patch().scale(1.30).move_to(point(x2, -0.02))
    return panels, gain, loss, pathway


class S09ControlsPathway(SpokenScene):
    def construct(self):
        walls, remote, signal, name, note = context_controls()
        caution = T("!", 39, RED, weight=BOLD).move_to(point(-4.05, -3.15))
        self.add(walls, remote, signal, name, note, caution)
        self.at("Paired controls")
        self.play(FadeOut(VGroup(name, note, caution, signal)), run_time=0.42)
        panels, gain, loss, pathway = comparison()
        self.play(ReplacementTransform(walls, VGroup(gain, loss)),
                  ReplacementTransform(remote, pathway), FadeIn(panels), run_time=1.65)
        self.at("To test necessity")
        add = factor_dot().move_to(point(-3.0, 1.70))
        self.play(FadeIn(add, shift=DOWN * 0.34), run_time=0.58)
        self.play(LaggedStart(*(cell[0].animate.set_fill(FLOOR) for cell in gain),
                               lag_ratio=0.36), run_time=1.10)
        for index, cell in enumerate(gain):
            surface_light(cell[0], rate=1.7 + 0.9 * index, strength=0.42, highlight=GREEN)
        plus = T("+ Gain", 29, GREEN).move_to(point(-5.40, 0.73))
        minus = T("− Loss", 29, RED).move_to(point(-5.36, -1.40))
        self.at("pair gain with loss")
        self.play(FadeIn(plus), FadeIn(minus), run_time=0.72)
        self.at("or block its receptor")
        cap = RoundedRectangle(width=0.64, height=0.22, corner_radius=0.10,
                               fill_color=RED, fill_opacity=1, stroke_width=0)
        cap.move_to(loss[0][2].get_center() + UP * 0.16)
        cap.set_z_index(3)
        self.play(FadeIn(cap, shift=DOWN * 0.45), run_time=0.82)
        self.at("To verify the pathway")
        receptors = tissue_patch(receptor=True).scale(1.30).move_to(pathway)
        notches = VGroup(*(cell[2] for cell in receptors))
        self.play(FadeIn(notches), run_time=0.60)
        self.at("repeat delivery")
        cue = factor_dot().move_to(point(1.37, 1.37))
        travel = CubicBezier(cue.get_center(), point(2.19, 1.67),
                             point(3.82, 1.55), point(4.70, 0.88))
        self.play(FadeOut(notches, shift=UP * 0.18), run_time=0.65)
        self.play(MoveAlongPath(cue, travel), run_time=2.65)
        self.at("If nothing happens there")
        result = T("No receptor, no effect", 31, BLUE).move_to(point(3.15, -1.83))
        self.play(FadeIn(result), run_time=0.68)
        bob(cue, amp=0.24, speed=1.8)
        self.finish()


def silhouette(points, color, outline=MEMBRANE, width=3):
    path = VMobject(fill_color=color, fill_opacity=1, stroke_color=outline, stroke_width=width)
    path.set_points_smoothly([point(x, y) for x, y in [*points, points[0]]])
    return path


def surface_light(surface, rate=2.0, strength=0.22, highlight=MEMBRANE):
    """Gently vary the illumination on a tissue surface during the spoken hold."""
    base = surface.get_fill_color()
    highlight = ManimColor(highlight)
    phase = [0.0]

    def update(mob, dt):
        phase[0] += dt
        amount = strength * (1 - np.cos(rate * phase[0]))
        mob.set_fill(interpolate_color(base, highlight, amount))

    surface.add_updater(update)


BRAIN_CONTOUR = ((-4.5, -0.62), (-4.35, 0.62), (-3.39, 1.51), (-2.3, 1.56),
                 (-1.52, 0.92), (-0.76, 1.50), (0.43, 1.64), (1.51, 0.69),
                 (2.55, 0.26), (4.65, -0.24), (4.73, -1.18), (2.52, -1.25),
                 (0.80, -1.56), (-1.22, -1.40), (-3.05, -1.82), (-4.03, -1.39))
FOLD_START = ((-0.80, 1.19), (-0.60, 1.54), (-0.20, 1.69), (0.27, 1.74),
              (0.73, 1.50), (0.97, 1.24), (0.63, 0.97), (-0.15, 0.87))
FOLD_END = ((-1.48, 0.99), (-1.62, 1.68), (-1.20, 2.16), (-0.70, 1.78),
            (-0.44, 2.47), (0.03, 2.49), (0.40, 1.97), (0.74, 2.55),
            (1.19, 2.37), (1.27, 1.69), (1.77, 1.96), (2.06, 1.40),
            (1.70, 0.76), (0.80, 0.53), (-0.24, 0.51), (-0.98, 0.73))


def brain_tube():
    outline = silhouette(BRAIN_CONTOUR, SLATE)
    inner = silhouette(BRAIN_CONTOUR, BG, MEMBRANE, 1.4).scale(0.79).stretch(0.51, 1)
    inner.shift(point(0.05, -0.33))
    return VGroup(outline, inner)


def brain_fold(folded):
    return silhouette(FOLD_END if folded else FOLD_START, "#8D6E30", YELLOW, 3)


def brain_history():
    return caption("2001 · Midbrain to cerebellum", 33, GOLD, y=-3.09)


class S10UnlockedPattern(SpokenScene):
    def construct(self):
        walls = tube("shh")
        self.add(walls, scope_tag())
        animate_tissue(walls, "shh")
        self.at("In 1993")
        year = caption("1993", 33, GOLD, y=-3.12)
        self.play(FadeIn(year), run_time=0.63)
        self.at("forced sonic hedgehog")
        shh = factor_dot(radius=0.14).move_to(point(2.09, 0.88))
        shh_path = CubicBezier(point(0.05, 1.22), point(0.72, 1.81),
                                 point(1.38, 1.44), shh.get_center())
        shh.move_to(shh_path.get_start())
        self.play(MoveAlongPath(shh, shh_path), run_time=1.42)
        label = side_label("Shh", 5.0, 0.94, YELLOW)
        self.play(FadeIn(label), run_time=0.54)
        bob(shh, amp=0.17, speed=1.8)
        self.at("floor plate genes")
        repaint(self, walls, "induced", 1.36)
        history = caption("1993 · Floor-plate genes", 33, GREEN, y=-3.12)
        self.play(swap(year, history), run_time=0.82)
        self.at("In 2001")
        self.play(FadeOut(VGroup(label, shh)), run_time=0.45)
        tag = caption("2001", 33, GOLD, y=-3.09)
        body = brain_tube()
        walls.clear_updaters()
        self.play(ReplacementTransform(walls, body), swap(history, tag), run_time=2.16)
        surface_light(body[0])
        self.at("misexpressed fgf8b")
        patch = brain_fold(False)
        self.play(GrowFromCenter(patch), run_time=0.90)
        fgf = side_label("FGF8b", 0, 2.55, YELLOW)
        self.play(FadeIn(fgf), run_time=0.65)
        pulse(patch, base=3.3, amp=1.7, speed=2.0)
        self.at("That signal could")
        self.play(FadeOut(fgf), run_time=0.43)
        patch.clear_updaters()
        self.play(Transform(patch, brain_fold(True)), swap(tag, brain_history()), run_time=2.50)
        pulse(patch, base=3.1, amp=1.2, speed=1.8)
        self.finish()


SMOOTH_CORTEX = ((-4.15, -0.12), (-3.74, 0.70), (-2.53, 1.43), (-1.27, 1.80),
                 (0, 1.91), (1.27, 1.80), (2.53, 1.43), (3.74, 0.70), (4.15, -0.12),
                 (3.59, -0.45), (2.51, 0.15), (1.26, 0.48), (0, 0.60), (-1.26, 0.48),
                 (-2.51, 0.15), (-3.59, -0.45))
FOLDED_CORTEX = ((-4.78, -0.19), (-4.25, 0.94), (-3.62, 1.30), (-3.34, 0.72),
                 (-2.77, 0.95), (-2.51, 2.02), (-1.94, 2.40), (-1.36, 1.94),
                 (-1.18, 1.04), (-0.53, 1.27), (-0.35, 2.32), (0.19, 2.58),
                 (0.65, 2.11), (0.85, 1.34), (1.51, 1.28), (1.90, 2.07),
                 (2.54, 2.10), (3.04, 1.63), (3.19, 0.78), (3.72, 0.92),
                 (4.25, 0.79), (4.81, -0.17), (4.40, -0.63), (3.90, 0.08),
                 (3.27, -0.02), (2.59, 0.24), (2.36, 1.38), (1.98, 1.34),
                 (1.63, 0.47), (0.80, 0.40), (0.23, 0.69), (0.13, 1.64),
                 (-0.06, 1.79), (-0.26, 0.72), (-0.80, 0.26), (-1.58, 0.25),
                 (-1.95, 1.47), (-2.16, 1.55), (-2.43, 0.50), (-3.27, -0.12),
                 (-3.91, 0.37), (-4.43, -0.64))


def cortex(folded=False):
    return silhouette(FOLDED_CORTEX if folded else SMOOTH_CORTEX, "#48627D", BLUE)


def progenitor(x, y, radius=0.37):
    cell = Ellipse(width=2 * radius, height=2.4 * radius, stroke_color=MEMBRANE,
                   stroke_width=2.2, fill_color=SLATE, fill_opacity=1)
    nucleus = Dot(radius=0.36 * radius, color=MEMBRANE)
    return VGroup(cell, nucleus).move_to(point(x, y))


class S11UnlockedGrowth(SpokenScene):
    def construct(self):
        brain, fold, history = brain_tube(), brain_fold(True), brain_history()
        scope = scope_tag()
        self.add(brain, fold, history, scope)
        self.at("In 2002")
        sheet = cortex()
        row_curvature = 0.044
        cells = VGroup(*(progenitor(x, -0.86 - row_curvature * x * x)
                         for x in np.linspace(-3.4, 3.4, 7)))
        caption_y = -3.26
        year = caption("2002", 33, GOLD, y=caption_y)
        self.play(ReplacementTransform(VGroup(brain, fold), sheet),
                  FadeIn(cells, shift=UP * 0.22), swap(history, year), run_time=2.35)
        surface_light(sheet)
        self.at("expressed stabilized")
        factor = VGroup(*(factor_dot(radius=0.086).move_to(cell.get_center() + UP * 0.17)
                          for cell in cells[1::2]))
        self.play(LaggedStart(*(GrowFromCenter(dot) for dot in factor), lag_ratio=0.44),
                  run_time=1.7)
        beta = side_label("β-catenin", 5.05, -1.12, YELLOW)
        self.play(FadeIn(beta), run_time=0.5)
        self.at("Stabilized means")
        for i, dot in enumerate(factor):
            bob(dot, amp=0.14, speed=1.7, seed=i)
        stable = T("Stabilized", 30, YELLOW).move_to(point(0, -2.22))
        self.play(FadeIn(stable), run_time=0.65)
        self.at("More of those cells")
        self.play(FadeOut(stable), FadeOut(beta), run_time=0.45)
        daughters = VGroup(*(progenitor(x, -1.86 - row_curvature * x * x + 0.08 * (i % 2), radius=0.285)
                             for i, x in enumerate(np.linspace(-3.80, 3.80, 12))))
        self.play(LaggedStart(*(GrowFromPoint(daughter, cells[min(i // 2, 6)].get_center())
                               for i, daughter in enumerate(daughters)), lag_ratio=0.13),
                  run_time=1.92)
        self.at("enlarging and folding")
        sheet.clear_updaters()
        self.play(Transform(sheet, cortex(True)), run_time=2.42)
        surface_light(sheet, rate=1.7)
        enlarged = caption("2002 · Enlarged, folded cortex", 33, GOLD, y=caption_y)
        self.play(swap(year, enlarged), run_time=0.78)
        pulse(sheet, base=3.3, amp=1.7, speed=1.8)
        self.at("how primate cortex")
        hedge = T("Not how primates grow", 30, RED).move_to(point(0, 3.10))
        self.play(FadeIn(hedge), run_time=0.63)
        self.at("Adding shows")
        self.play(FadeOut(VGroup(enlarged, hedge)), run_time=0.37)
        icons = TwoPanel("+ Add · command", "− Delete · require", colors=(GREEN, RED),
                         top=2.68, bottom=-2.61, width=12.2)
        left = tissue_patch(FLOOR).move_to(point(-3.15, -0.07))
        right = tissue_patch().move_to(point(3.15, -0.07))
        sheet.clear_updaters()
        self.play(FadeOut(sheet, scale=0.68, shift=UP * 0.38),
                  FadeOut(VGroup(cells, daughters, factor), shift=DOWN * 0.28),
                  FadeIn(left, shift=UP * 0.12), FadeIn(right, shift=UP * 0.12),
                  Create(icons.left_frame), Create(icons.right_frame), run_time=0.90)
        add = factor_dot(radius=0.18).move_to(point(-3.15, 1.12))
        self.play(FadeIn(icons.left_head), GrowFromCenter(add), run_time=0.66)
        self.at("Deleting shows")
        absent = DashedVMobject(Circle(radius=0.22).set_stroke(RED, width=2.5), num_dashes=12)
        absent.move_to(point(3.15, 1.12))
        self.play(FadeIn(icons.right_head), Create(absent), run_time=0.66)
        self.finish()


class S12End(EndCard):
    LINE = "Misexpression tests what a factor can impose, not what tissue needs."
