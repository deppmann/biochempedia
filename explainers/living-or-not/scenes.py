"""Who Can Act Alone? — Living or Not? Viruses and Bacteria.

COLOR MAP
  GREEN  bacterium / living-cell action
  BLUE   virus / virus parts
  PINK   host cell and mature red blood cell
  PURPLE genes
  GOLD   energy, carbon, and other building material
  TEXT   neutral labels and host machinery

The builders below are the film's carried world.  Every return uses the same coordinates.
"""
from bp_parts import *

PINK = "#F06C9B"
PURPLE = "#B58CD9"


def arrow(a, b, color=TEXT, dashed=False, width=5):
    cls = DashedLine if dashed else Arrow
    kw = {"dash_length": 0.16} if dashed else {"tip_length": 0.22}
    return cls(a, b, color=color, stroke_width=width, **kw)


def genes_block(text="genes", scale=1.0):
    # A purple instruction block is legible at every carried scale; nearby labels name it when spoken.
    return RoundedRectangle(corner_radius=0.08, width=1.15, height=0.52,
                            stroke_color=PURPLE, stroke_width=3,
                            fill_color=PURPLE, fill_opacity=0.68).scale(scale)


def virus_picture(radius=0.72, at=ORIGIN, genes=True):
    """A labelled-cartoon virus: protein shell plus one genes block, never a molecule."""
    shell = Circle(radius=radius, stroke_color=BLUE, stroke_width=6,
                   fill_color=BLUE, fill_opacity=0.14)
    ridges = VGroup(*[
        Line(shell.point_at_angle(a), shell.point_at_angle(a) + 0.13 * np.array([np.cos(a), np.sin(a), 0]),
             color=BLUE, stroke_width=5)
        for a in np.linspace(0, TAU, 8, endpoint=False)
    ])
    g = VGroup(shell, ridges)
    if genes:
        core = genes_block("genes", 0.58).move_to(shell)
        g.add(core)
        g.core = core
    g.shell = shell
    return g.move_to(at)


def ribosome(at, scale=1.0):
    top = RoundedRectangle(corner_radius=0.12, width=0.82, height=0.34,
                           stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.20)
    base = RoundedRectangle(corner_radius=0.10, width=1.05, height=0.28,
                            stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.10)
    base.next_to(top, DOWN, buff=0.02)
    return VGroup(top, base).scale(scale).move_to(at)


def host_cell(at=(3.75, -0.15, 0), width=5.3, height=5.3):
    membrane = RoundedRectangle(corner_radius=0.9, width=width, height=height,
                                stroke_color=PINK, stroke_width=6,
                                fill_color=PINK, fill_opacity=0.18).move_to(at)
    ribs = VGroup(ribosome(np.array(at) + d, 0.62) for d in
                  [(-1.05, 1.15, 0), (0.75, 1.20, 0), (-0.45, -0.65, 0), (1.05, -1.05, 0)])
    g = VGroup(membrane, ribs)
    g.membrane, g.ribs = membrane, ribs
    return g


def switch_picture(at=(-4.65, -0.25, 0)):
    plate = RoundedRectangle(corner_radius=0.28, width=2.8, height=4.6,
                             stroke_color=TEXT, stroke_width=5, fill_color=TEXT, fill_opacity=0.07)
    lever = RoundedRectangle(corner_radius=0.16, width=0.85, height=1.75,
                             stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.20)
    lever.rotate(-0.12)
    return VGroup(plate, lever).move_to(at)


def bacterium_picture(at=(-2.7, 0, 0), width=5.3, height=2.5, internals=True):
    membrane = RoundedRectangle(corner_radius=height / 2 - 0.03, width=width, height=height,
                                stroke_color=GREEN, stroke_width=6,
                                fill_color=GREEN, fill_opacity=0.19).move_to(at)
    g = VGroup(membrane)
    g.membrane = membrane
    if internals:
        gene = genes_block("genes", 0.78).move_to(np.array(at) + LEFT * 0.65)
        ribs = VGroup(ribosome(np.array(at) + d, 0.48) for d in
                      [(0.95, 0.55, 0), (1.30, -0.50, 0), (0.15, -0.62, 0)])
        g.add(gene, ribs)
        g.gene, g.ribs = gene, ribs
    return g


def hook_world():
    switch = switch_picture()
    v = virus_picture(0.55, (-4.65, 2.55, 0))
    host = host_cell()
    return VGroup(switch, v, host), switch, v, host


def predict_world():
    host = host_cell((3.65, 0.35, 0), 5.55, 4.75)
    v = virus_picture(0.62, (-4.75, 0.75, 0))
    path_a = chip("virus gains machinery", BLUE, size=28).move_to([-2.45, 2.55, 0])
    path_b = chip("host supplies what is missing", PINK, size=28).move_to([-2.15, -1.05, 0])
    a1 = arrow(v.get_right(), path_a.get_left(), BLUE)
    a2 = arrow(v.get_right() + DOWN * 0.2, path_b.get_left(), PINK)
    return VGroup(host, v, path_a, path_b, a1, a2)


class S01Hook(SpokenScene):
    def construct(self):
        world, switch, v, host = hook_world()
        self.play(FadeIn(switch), FadeIn(v, shift=DOWN * 0.2), run_time=0.8)
        bob(v, amp=0.05, speed=1.5)
        self.at("then reaches a cell")
        self.play(FadeIn(host), run_time=0.7)
        v.clear_updaters()
        self.play(v.animate.move_to(host.membrane.get_left() + RIGHT * 0.65), run_time=1.3)
        self.at("makes new copies")
        copies = VGroup(*[virus_picture(0.32, p) for p in
                          [(2.65, 0.8, 0), (4.0, 0.0, 0), (4.75, 1.15, 0)]])
        self.play(LaggedStart(*[FadeIn(x, scale=0.35) for x in copies], lag_ratio=0.22), run_time=1.1)
        for r in host.ribs:
            bob(r, amp=0.05, speed=1.7)
        self.at("Was the virus alive")
        q = fit_text("Alive on the switch?", max_w=5.6, size=46, color=GOLD).move_to([-2.55, -2.85, 0])
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.6)
        self.at("Watch what each object")
        self.play(Indicate(switch, color=TEXT), Indicate(host.membrane, color=PINK), run_time=1.0)
        self.at("who supplies the work")
        self.play(Indicate(host.ribs, color=GOLD), run_time=0.9)
        self.finish()


class S02Title(NarratedScene):
    def construct(self):
        world, switch, v, host = hook_world()
        world.set_opacity(0.42)
        title = fit_text("Who Can Act Alone?", max_w=4.1, size=50, color=TEXT, font=TITLE_FONT)
        lesson = T("LIVING OR NOT? VIRUSES AND BACTERIA", 22, TEAL)
        lesson.layout_ok = True
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        card = VGroup(lesson, title, rule).arrange(DOWN, buff=0.30).move_to([-1.05, 0.0, 0])
        self.add(world)
        self.play(v.animate.shift(RIGHT * 1.5), Rotate(host.ribs, 0.18, about_point=host.get_center()),
                  FadeIn(card), run_time=1.2)
        self.play(v.animate.shift(RIGHT * 0.65), Rotate(host.ribs, 0.12, about_point=host.get_center()),
                  run_time=0.8)
        self.finish()


class S03Evidence(SpokenScene):
    def construct(self):
        host = host_cell((0, 0, 0), 2.6, 2.6)
        host.ribs.set_opacity(0.45)
        self.play(FadeIn(host), run_time=0.8)
        self.at("characteristics of life")
        labels = ["cell", "energy", "grow", "respond", "steady", "reproduce", "evolve"]
        colors = [PINK, GOLD, GREEN, TEXT, TEAL, BLUE, PURPLE]
        icons = VGroup()
        for i, (lab, col) in enumerate(zip(labels, colors)):
            a = PI / 2 - i * TAU / 7
            pos = np.array([4.35 * np.cos(a), 2.4 * np.sin(a), 0])
            icons.add(chip(lab, col, size=28, pad=0.15).move_to(pos))
        self.play(LaggedStart(*[FadeIn(x, scale=0.75) for x in icons], lag_ratio=0.10), run_time=2.0)
        for i, icon in enumerate(icons):
            bob(icon, amp=0.065, speed=1.25, seed=i)
        self.at("The list guides")
        self.play(Indicate(icons, color=GOLD, scale_factor=1.01), run_time=1.6)
        self.at("not a score")
        one = chip("✓", GREEN, size=42, pad=0.22).move_to([0, 0, 0])
        self.play(FadeIn(one, scale=0.5), FadeOut(host), run_time=0.5)
        self.play(one.animate.scale(1.45), run_time=0.45, rate_func=there_and_back)
        note = T("Not enough alone", 36, GOLD, weight=BOLD).move_to([0, -1.0, 0])
        self.play(FadeIn(note, shift=UP * 0.15), run_time=0.5)
        self.at("individual tick wins")
        self.play(Indicate(icons, color=TEXT, scale_factor=1.01), run_time=1.1)
        self.finish()


class S04Bacterium(SpokenScene):
    def construct(self):
        b = bacterium_picture((0, 0.1, 0), 9.0, 3.55)
        self.play(FadeIn(b.membrane, scale=0.9), run_time=0.8)
        self.at("single cell with")
        flow = VGroup(*[
            Dot([x, y, 0], radius=0.12, color=TEXT).set_opacity(0.44)
            for y in (-1.0, -0.35, 0.35, 1.0) for x in np.linspace(-3.8, 3.8, 7)
        ]).set_z_index(-1)

        def drift_cytoplasm(mob, dt):
            for i, dot in enumerate(mob):
                dot.shift(RIGHT * (0.46 + 0.055 * (i % 4)) * dt)
                if dot.get_x() > 4.0:
                    dot.shift(LEFT * 7.9)

        flow.add_updater(drift_cytoplasm)
        self.play(FadeIn(flow), FadeIn(b.gene),
                  LaggedStart(*[FadeIn(r) for r in b.ribs], lag_ratio=0.2), run_time=1.0)
        pulse(b.membrane, base=6.0, amp=1.2, speed=2.0)
        b.ribs.add_updater(lambda m, dt: m.rotate(0.16 * dt, about_point=b.get_center()))
        parts = VGroup(
            T("membrane", 28, GREEN).move_to([-4.5, 2.5, 0]),
            T("cytoplasm", 28, TEXT).move_to([-1.45, 2.5, 0]),
            T("genes", 28, PURPLE).move_to([1.1, 2.5, 0]),
            T("ribosomes", 28, TEXT).move_to([4.1, 2.5, 0]),
        )
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.15) for x in parts], lag_ratio=0.12), run_time=1.2)
        self.at("This prokaryote")
        pro = caption("Prokaryote: no nucleus; typically no membrane-covered organelles", size=28, color=GREEN)
        self.play(FadeOut(parts), FadeIn(pro), run_time=0.6)
        self.at("In suitable conditions")
        blocks = VGroup(*[Square(0.28, color=GOLD, fill_color=GOLD, fill_opacity=0.85).move_to([-5.7, y, 0])
                          for y in (-0.85, 0.15, 1.05)])
        self.play(FadeIn(blocks), run_time=0.4)
        self.at("materials cross its membrane")
        self.play(*[x.animate.shift(RIGHT * (2.0 + i * 0.25)) for i, x in enumerate(blocks)], run_time=1.2)
        self.at("ribosomes build proteins")
        protein = chip("protein", TEXT, size=28).move_to([3.0, 0.1, 0])
        self.play(b.ribs.animate.shift(RIGHT * 0.55), FadeIn(protein, scale=0.5), FadeOut(pro), run_time=1.0)
        self.at("It uses energy")
        action = VGroup(*[chip(x, c, size=28, pad=0.13) for x, c in
                          [("energy", GOLD), ("grows", GREEN), ("responds", TEXT), ("divides", GREEN)]])
        action.arrange(RIGHT, buff=0.28).move_to([0, -2.7, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.15) for x in action], lag_ratio=0.18), run_time=1.5)
        self.at("and divides")
        b1 = bacterium_picture((-2.7, 0.1, 0), 4.15, 2.7, False)
        b2 = bacterium_picture((2.7, 0.1, 0), 4.15, 2.7, False)
        self.play(FadeOut(VGroup(blocks, protein, flow, b.gene, b.ribs)),
                  ReplacementTransform(b.membrane, VGroup(b1, b2)), run_time=1.5)
        self.finish()


class S05VirusOutside(SpokenScene):
    def construct(self):
        bacterium = bacterium_picture((-4.5, 1.55, 0), 3.6, 1.7, False)
        bacterium.add(T("cell", 28, GREEN).move_to([-4.5, 1.55, 0]))
        v = virus_picture(1.55, (1.5, 0.3, 0))
        self.play(FadeIn(bacterium), FadeIn(v, scale=0.75), run_time=0.9)
        v[1].add_updater(lambda m, dt: m.rotate(0.48 * dt, about_point=v.get_center()))
        bob(bacterium, amp=0.075, speed=1.35)
        self.at("genes inside a protein capsid")
        caplab = T("protein capsid", 32, BLUE).move_to([1.5, 2.65, 0])
        self.play(FadeIn(caplab), Indicate(v.core, color=PURPLE), run_time=0.9)
        self.at("not a cell")
        ncell = chip("not a cell", BLUE, size=32).move_to([-4.5, -0.15, 0])
        self.play(FadeIn(ncell), run_time=0.5)
        self.at("capsid protects the genes")
        self.play(v.shell.animate.scale(1.08), run_time=0.45, rate_func=there_and_back)
        self.at("fatty envelope")
        envelope = Circle(radius=1.9, stroke_color=TEAL, stroke_width=4).move_to(v)
        envlab = T("some: fatty envelope", 28, TEAL).move_to([1.5, -2.05, 0])
        self.play(Create(envelope), FadeIn(envlab), run_time=0.7)
        self.at("no cytoplasm or ribosomes")
        empty = VGroup(chip("no cytoplasm", TEXT, 28), chip("no ribosomes", TEXT, 28))
        empty.arrange(DOWN, buff=0.25).move_to([4.9, -0.2, 0])
        self.play(FadeOut(envlab), FadeIn(empty), run_time=0.8)
        self.at("Outside a host")
        gold = VGroup(*[Square(0.24, color=GOLD, fill_color=GOLD, fill_opacity=0.85).move_to([-6.0, y, 0])
                        for y in (-2.35, -2.8, -3.2)])
        self.add(gold)
        self.play(gold.animate.shift(RIGHT * 11.2), run_time=2.2, rate_func=linear)
        self.at("use energy, or grow")
        still = T("no food in • no energy use • no growth", 30, GOLD).move_to([0, -3.25, 0])
        self.play(FadeIn(still), run_time=0.6)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        world = predict_world()
        host, v, path_a, path_b, a1, a2 = world
        self.play(FadeIn(host), FadeIn(v), run_time=0.8)
        for r in host.ribs:
            bob(r, amp=0.045, speed=1.6)
        self.at("Does the virus gain")
        self.play(GrowArrow(a1), FadeIn(path_a), run_time=0.7)
        self.at("or does the host supply")
        self.play(GrowArrow(a2), FadeIn(path_b), run_time=0.7)
        self.at("Keep your eye")
        self.play(Indicate(host.ribs, color=GOLD), run_time=0.8)
        pred = T("PREDICT", 42, GOLD, weight=BOLD).move_to([-4.6, -2.25, 0])
        q = question_card("Who supplies the missing machinery?", y=-3.15, size=30, max_w=8.8)
        self.play(FadeIn(pred), FadeIn(q), run_time=0.6)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Who supplies the missing machinery?"
    SECONDS = 4.5
    CARD = {"y": -3.15, "size": 30, "max_w": 8.8}

    def backdrop(self):
        return predict_world()


class S08Host(SpokenScene):
    def construct(self):
        host = host_cell((1.0, 0.15, 0), 10.7, 5.25)
        v = virus_picture(0.72, (-5.35, 1.45, 0))
        answer = chip("HOST SUPPLIES IT", PINK, 32).move_to([-3.6, 3.35, 0])
        self.play(FadeIn(host), FadeIn(v), FadeIn(answer), run_time=0.9)
        host.ribs.add_updater(lambda m, dt: m.rotate(0.32 * dt, about_point=host.get_center()))
        self.at("provides ribosomes, energy")
        gold = VGroup(*[Square(0.26, color=GOLD, fill_color=GOLD, fill_opacity=0.9).move_to([-4.8, y, 0])
                        for y in (-1.2, -0.45, 0.3)])
        self.play(Indicate(host.ribs, color=GOLD), FadeIn(gold), run_time=0.8)
        self.at("Viral genes use them")
        target = np.array([-1.8, 0.55, 0])
        core = v.core.copy()
        self.play(v.animate.move_to([-3.45, 1.15, 0]), run_time=0.8)
        self.play(FadeOut(v.shell), FadeOut(v[1]), core.animate.move_to(target), run_time=0.7)
        self.play(gold.animate.move_to([-0.2, -0.35, 0]), host.ribs.animate.shift(LEFT * 0.35), run_time=1.0)
        self.at("make virus parts")
        parts = VGroup(*[Arc(radius=0.38, start_angle=a, angle=1.15, color=BLUE, stroke_width=7).move_to(p)
                         for a, p in zip((0, 2, 4), [(1.4, 1.25, 0), (2.2, 0.3, 0), (1.25, -0.75, 0)])])
        self.play(LaggedStart(*[Create(p) for p in parts], lag_ratio=0.2), run_time=1.0)
        self.at("Host enzymes or viral enzymes")
        enzyme = chip("host or viral enzyme", TEXT, 28).move_to([-3.0, -1.65, 0])
        core2 = core.copy().shift(RIGHT * 2.6)
        self.play(FadeIn(enzyme), core.animate.move_to([-2.6, -0.35, 0]), FadeIn(core2), run_time=1.0)
        self.at("parts assemble around")
        new1 = virus_picture(0.6, (1.8, 0.65, 0))
        new2 = virus_picture(0.6, (3.7, -0.75, 0))
        self.play(FadeOut(parts), FadeIn(new1, scale=0.45), FadeIn(new2, scale=0.45), run_time=1.2)
        self.at("never gains its own metabolism")
        rule = caption("Virus: no metabolism of its own", 32, BLUE)
        self.play(FadeOut(answer), FadeIn(rule), run_time=0.7)
        self.finish()


class S09EdgeCases(SpokenScene):
    def construct(self):
        panels = TwoPanel("mature red blood cell", "crystal", colors=(PINK, TEXT))
        self.play(FadeIn(panels), run_time=0.8)
        tube = VGroup(Line([-5.9, 0.7, 0], [-0.7, 0.7, 0], color=PINK, stroke_width=4),
                      Line([-5.9, -0.7, 0], [-0.7, -0.7, 0], color=PINK, stroke_width=4))
        rbc = Annulus(inner_radius=0.48, outer_radius=1.05, color=PINK, fill_opacity=0.35, stroke_width=4).move_to([-5.1, 0, 0])
        self.at("mature red blood cell")
        self.play(FadeIn(tube), FadeIn(rbc), run_time=0.6)
        self.at("cannot divide")
        nodiv = chip("cell • no division", PINK, 30).move_to([-3.25, -1.75, 0])
        self.play(rbc.animate.stretch(0.55, 1).move_to([-1.55, 0, 0]), FadeIn(nodiv), run_time=1.4)
        self.at("A crystal gets bigger")
        blocks = VGroup(*[Square(0.72, color=TEXT, fill_color=TEXT, fill_opacity=0.16).move_to(p)
                          for p in [(2.3, 0.6, 0), (3.05, 0.6, 0), (2.3, -0.15, 0),
                                    (3.05, -0.15, 0), (3.8, 0.6, 0), (3.8, -0.15, 0), (3.05, 1.35, 0)]])
        self.play(LaggedStart(*[FadeIn(x, scale=0.2) for x in blocks], lag_ratio=0.12), run_time=1.5)
        self.at("no cells and no metabolism")
        no = chip("bigger • no cell", TEXT, 30).move_to([3.25, -1.75, 0])
        self.play(FadeIn(no), run_time=0.6)
        self.at("Growth alone")
        cap = caption("One checked box cannot decide alone.", 34, GOLD)
        self.play(FadeIn(cap), run_time=0.6)
        self.finish()


class S10Scope(SpokenScene):
    def construct(self):
        path = VMobject(stroke_color=PURPLE, stroke_width=6)
        path.set_points_smoothly([[-6.0, 1.2, 0], [-4.7, 1.8, 0], [-3.6, 1.1, 0], [-2.2, 2.0, 0], [-1.0, 1.35, 0]])
        branch = VGroup(path,
                        Line([-3.6, 1.1, 0], [-2.4, 0.1, 0], color=PURPLE, stroke_width=5),
                        Line([-2.2, 2.0, 0], [-1.2, 2.75, 0], color=PURPLE, stroke_width=5))
        viruses = VGroup(*[virus_picture(0.32, p) for p in
                           [(-5.7, 1.25, 0), (-4.5, 1.65, 0), (-3.4, 1.1, 0), (-2.25, 1.9, 0), (-1.25, 1.4, 0)]])
        self.play(Create(branch), LaggedStart(*[FadeIn(v) for v in viruses], lag_ratio=0.15), run_time=1.5)
        for i, vir in enumerate(viruses):
            vir[1].add_updater(lambda m, dt, vir=vir: m.rotate(0.65 * dt, about_point=vir.get_center()))
            bob(vir, amp=0.075, speed=1.25, seed=i)
        self.at("carry genes and evolve")
        ev = T("genes • evolves", 30, PURPLE).move_to([-3.4, 3.0, 0])
        self.play(FadeIn(ev), viruses.animate.shift(RIGHT * 0.35), run_time=0.8)
        self.at("Virginia biology classes")
        title = T("VIRGINIA BIOLOGY", 30, GOLD, weight=BOLD).move_to([3.45, 2.75, 0])
        bracket = Brace(Line([0.15, 2.2, 0], [0.15, -2.2, 0]), RIGHT, color=GOLD)
        self.play(FadeIn(title), GrowFromCenter(bracket), run_time=0.7)
        rows = VGroup(chip("cell  —  no", TEXT, 30), chip("own metabolism  —  no", GOLD, 30),
                      chip("host dependence  —  yes", PINK, 30)).arrange(DOWN, buff=0.35).move_to([3.55, 0.1, 0])
        self.at("not cells")
        self.play(FadeIn(rows[0]), run_time=0.45)
        self.at("no metabolism of their own")
        self.play(FadeIn(rows[1]), run_time=0.5)
        self.at("depend on a host cell")
        self.play(FadeIn(rows[2]), run_time=0.5)
        tag = scope_tag("course classification", 24, GOLD)
        self.play(FadeIn(tag), viruses.animate.shift(RIGHT * 0.25), run_time=0.9)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        world, switch, v, host = hook_world()
        b = bacterium_picture((-1.65, -1.65, 0), 4.15, 1.8)
        self.play(FadeIn(switch), FadeIn(v), FadeIn(host), FadeIn(b), run_time=1.0)
        bob(v, amp=0.045, speed=1.4)
        host.ribs.add_updater(lambda m, dt: m.rotate(0.34 * dt, about_point=host.get_center()))
        b.ribs.add_updater(lambda m, dt: m.rotate(0.55 * dt, about_point=b.get_center()))
        self.at("later be copied")
        dep = arrow(v.get_right() + DOWN * 0.2, host.membrane.get_left() + UP * 0.8, BLUE, dashed=True)
        self.play(Create(dep), run_time=0.9)
        self.at("waiting is not living")
        waiting = T("waiting ≠ living", 34, BLUE, weight=BOLD).move_to([-4.45, -3.0, 0])
        self.play(FadeIn(waiting), run_time=0.5)
        self.at("host cell supplies")
        self.play(Indicate(host.ribs, color=GOLD), run_time=0.8)
        self.at("bacterium carries its own")
        loop = Arc(radius=0.58, start_angle=0.3, angle=5.3, color=GREEN, stroke_width=6,
                   arc_center=b.get_center())
        tip = Arrow(loop.get_end() - 0.22 * LEFT, loop.get_end(), buff=0, color=GREEN, tip_length=0.2)
        self.play(Create(loop), GrowArrow(tip), run_time=0.9)
        blocks = VGroup(*[Square(0.22, color=GOLD, fill_color=GOLD, fill_opacity=0.9).move_to([-4.2 + i * 0.35, -1.65, 0]) for i in range(3)])
        self.play(FadeIn(blocks), blocks.animate.shift(RIGHT * 1.0), run_time=1.2)
        self.at("conditions suit it")
        self.play(b.membrane.animate.stretch(1.16, 0), Rotate(loop, 0.5, about_point=b.get_center()), run_time=1.0)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        panels = TwoPanel("bacterium", "virus", colors=(GREEN, BLUE), bottom=-2.15)
        b = bacterium_picture((-3.25, 0.45, 0), 4.2, 2.15)
        v = virus_picture(0.95, (3.25, 0.6, 0))
        host = RoundedRectangle(corner_radius=0.35, width=2.0, height=1.3, color=PINK,
                                fill_color=PINK, fill_opacity=0.08).move_to([5.0, -1.1, 0])
        dep = arrow(v.get_bottom() + DOWN * 0.05, host.get_left() + LEFT * 0.05, BLUE, dashed=True)
        self.play(FadeIn(panels), FadeIn(b), FadeIn(v), FadeIn(host), Create(dep), run_time=1.0)
        self.at("Is it a cell")
        q1 = chip("cell?", TEXT, 30).move_to([-3.25, -1.55, 0])
        self.play(FadeIn(q1), Indicate(b.membrane, color=GREEN), run_time=0.7)
        self.at("own ribosomes and metabolism")
        q2 = chip("own machinery?", GOLD, 26).move_to([2.2, -1.55, 0])
        self.play(FadeIn(q2), Indicate(b.ribs, color=GOLD), run_time=0.8)
        loop = Arc(radius=0.50, start_angle=0.2, angle=5.4, color=GREEN, stroke_width=6,
                   arc_center=b.get_center())
        self.play(Create(loop), run_time=0.7)
        self.at("course rule")
        rule = caption("Bacteria are living cells; viruses are not cells and are classed nonliving.", 31, GOLD)
        self.play(FadeIn(rule), run_time=0.8)
        self.at("viruses are not cells")
        self.play(Indicate(v, color=BLUE), Indicate(dep, color=PINK), Rotate(loop, 0.55, about_point=b.get_center()), run_time=1.2)
        self.finish()


class S13End(EndCard):
    LINE = "Bacteria are living cells; viruses are not cells and are classed nonliving."
