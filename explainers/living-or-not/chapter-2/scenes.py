"""Parts Reveal the Difference — Living or Not?, chapter 2.

COLOR MAP (carried exactly from chapter 1)
  BLUE   = cells: bacterium and host cell
  YELLOW = virus, capsid and virus parts
  ORANGE = genetic material (DNA or RNA)
  TEAL   = ribosomes / protein-building workbenches
  PURPLE = material inputs (nutrients, carbon compounds, CO2, sulfur compounds)
  GOLD   = energy and the central teaching rule
  GREEN  = living / a working cell
  RED    = absent / noncellular
  GREY   = outlines, water and de-emphasized structure
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"


def arrow(a, b, color=GREY, width=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=width, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=10)


def gene_block(text="genes", at=ORIGIN, scale=1.0):
    g = chip(text, ORANGE, 28).scale(scale).move_to(at)
    return g


def ribosome(at=ORIGIN, scale=1.0):
    """A schematic protein-building workbench, not a molecular structure."""
    base = RoundedRectangle(corner_radius=0.13, width=1.05, height=0.48,
                            stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                            fill_opacity=0.22)
    slot = Line(LEFT * 0.28, RIGHT * 0.28, color=TEAL, stroke_width=5).move_to(base)
    g = VGroup(base, slot).scale(scale).move_to(at)
    return g


def bacterium(at=(-2.9, 0.15, 0), width=5.4, height=3.35, details=True):
    """The carried bacterium picture. Every continuing scene calls this builder."""
    body = RoundedRectangle(corner_radius=height / 2 - 0.04, width=width, height=height,
                            stroke_color=BLUE, stroke_width=7, fill_color=BLUE,
                            fill_opacity=0.20).move_to(at)
    g = VGroup(body)
    g.body = body
    if details:
        zone = Ellipse(width=2.15, height=1.35, stroke_color=ORANGE, stroke_width=2.5,
                       fill_color=ORANGE, fill_opacity=0.05).move_to(body.get_center() + LEFT * 0.55)
        dna = Arc(radius=0.48, start_angle=0.15, angle=TAU * 0.86, color=ORANGE,
                  stroke_width=7).move_to(zone)
        ribs = VGroup(ribosome(body.get_center() + np.array([1.15, 0.70, 0]), 0.72),
                      ribosome(body.get_center() + np.array([1.30, -0.45, 0]), 0.72),
                      ribosome(body.get_center() + np.array([-0.20, -0.88, 0]), 0.65))
        g.add(zone, dna, ribs)
        g.zone, g.dna, g.ribs = zone, dna, ribs
    return g


def virus(at=(3.65, 0.15, 0), radius=1.55, envelope=False, labelled=True):
    """The carried virus picture: capsid plus one genetic-material block."""
    cap = RegularPolygon(6, radius=radius, stroke_color=YELLOW, stroke_width=7,
                         fill_color=YELLOW, fill_opacity=0.22).move_to(at)
    if labelled:
        core = chip("DNA or RNA" if radius >= 1.35 else "genes", ORANGE, 24, pad=0.12).move_to(at)
    else:
        core = RoundedRectangle(corner_radius=0.05, width=radius * 0.9, height=radius * 0.42,
                                stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                                fill_opacity=0.65).move_to(at)
    g = VGroup(cap, core)
    if envelope:
        env = Circle(radius=radius * 1.23, stroke_color=BLUE, stroke_width=4,
                     fill_color=BLUE, fill_opacity=0.05).move_to(at)
        g.add_to_back(env)
        g.envelope = env
    g.cap, g.core = cap, core
    return g


def host_cell(at=(3.3, 0.0, 0), width=6.3, height=5.4):
    body = RoundedRectangle(corner_radius=0.75, width=width, height=height,
                            stroke_color=BLUE, stroke_width=6, fill_color=BLUE,
                            fill_opacity=0.16).move_to(at)
    ribs = VGroup(ribosome(np.array(at) + [-1.3, 0.6, 0], 0.72),
                  ribosome(np.array(at) + [0.3, 1.1, 0], 0.72),
                  ribosome(np.array(at) + [1.25, -0.45, 0], 0.72))
    g = VGroup(body, ribs)
    g.body, g.ribs = body, ribs
    return g


def working_bacterium(at=(0, 0.2, 0), width=5.2, height=3.2):
    b = bacterium(at, width, height, True)
    pulse(b.body, base=7, amp=1.2, speed=2.2)
    bob(b, amp=0.11, speed=1.25)
    return b


def input_lanes(b_at=(1.9, 0.2, 0)):
    energy = arrow([-2.8, 1.25, 0], [b_at[0] - 2.7, 1.25, 0], GOLD, 7)
    carbon = arrow([-2.8, -0.75, 0], [b_at[0] - 2.7, -0.75, 0], PURPLE, 7)
    e_lab = T("energy", 32, GOLD, weight=BOLD).move_to([-5.1, 1.75, 0])
    c_lab = T("carbon", 32, PURPLE, weight=BOLD).move_to([-5.1, -1.28, 0])
    return VGroup(energy, carbon, e_lab, c_lab)


def spring_world(with_names=True):
    water = RoundedRectangle(corner_radius=0.2, width=13.0, height=5.8,
                             stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                             fill_opacity=0.12).move_to([0, 0.15, 0])
    floor = Polygon([-6.5, -2.2, 0], [-4.8, -1.55, 0], [-2.6, -2.15, 0],
                    [-0.3, -1.55, 0], [2.0, -2.2, 0], [4.3, -1.5, 0],
                    [6.5, -2.15, 0], [6.5, -2.75, 0], [-6.5, -2.75, 0],
                    stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18)
    b = working_bacterium([0.5, 0.2, 0], 4.2, 2.6)
    sulfur = chip("sulfur compounds", PURPLE, 27).move_to([-4.65, 1.15, 0])
    co2 = chip("carbon dioxide", PURPLE, 27).move_to([-4.65, -0.65, 0])
    sulfur[1].layout_ok = True  # chip text intentionally lies within the spring's water field
    co2[1].layout_ok = True
    a1 = arrow([-3.1, 1.12, 0], [-1.72, 0.88, 0], GOLD, 6)
    a2 = arrow([-3.1, -0.65, 0], [-1.72, -0.55, 0], PURPLE, 6)
    g = VGroup(water, floor, b, sulfur, co2, a1, a2)
    g.bacterium, g.sulfur, g.co2 = b, sulfur, co2
    if with_names:
        names = VGroup(chip("heterotroph", TEXT, 25), chip("photoautotroph", TEXT, 25),
                       chip("chemoautotroph", TEXT, 25)).arrange(DOWN, buff=0.18).move_to([4.85, 0.25, 0])
        g.add(names)
        g.names = names
    return g


class S01Hook(SpokenScene):
    def construct(self):
        b = bacterium([-3.35, 0.25, 0], 5.3, 3.25, False)
        v = virus([3.7, 0.25, 0], 1.55)
        self.play(FadeIn(b), FadeIn(v), run_time=0.8)
        # Show the shared genes before naming either object.
        bg = gene_block("genes", [-3.35, 0.25, 0], 0.82)
        self.play(FadeIn(bg), run_time=0.45)
        pulse(b.body, base=7, amp=1.5, speed=2.4)
        self.at("bacteria and viruses")
        labs = VGroup(T("bacterium", 34, BLUE, weight=BOLD).next_to(b, UP, buff=0.2),
                      T("virus", 34, YELLOW, weight=BOLD).next_to(v, UP, buff=0.2))
        self.play(FadeIn(labs), run_time=0.45)
        self.at("If both carry genes")
        self.play(Indicate(bg, color=ORANGE), Indicate(v.core, color=ORANGE), run_time=0.7)
        self.at("why can a bacterium grow")
        self.play(b.animate.scale(1.10), run_time=0.8)
        self.at("while a virus waits")
        wait_mark = T("waits", 32, GREY).next_to(v, DOWN, buff=0.25)
        self.play(FadeIn(wait_mark), run_time=0.4)
        self.at("Open them")
        q = T("Same genes, different lives?", 45, GOLD, font=TITLE_FONT).move_to([0, -3.15, 0])
        self.play(FadeOut(wait_mark), FadeIn(q, shift=UP * 0.15), run_time=0.6)
        self.play(b.body.animate.set_fill(opacity=0.04), v.cap.animate.set_fill(opacity=0.04), run_time=0.8)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Living or Not? Viruses and Bacteria"
    TITLE = "Parts Reveal the Difference"


class S03BacteriumParts(SpokenScene):
    def construct(self):
        b = bacterium([0, 0.05, 0], 10.9, 5.75, False)
        self.play(FadeIn(b), run_time=0.6)
        self.at("the bacterium")
        title = T("bacterium · prokaryotic cell", 38, BLUE, weight=BOLD).move_to([0, 3.28, 0])
        self.play(FadeIn(title), run_time=0.45)
        self.at("Its membrane controls")
        gate = VGroup(Line([-5.45, 0.65, 0], [-5.45, -0.65, 0], color=BG, stroke_width=12),
                      Line([-5.45, 0.65, 0], [-5.45, -0.1, 0], color=BLUE, stroke_width=7),
                      Line([-5.45, 0.1, 0], [-5.45, -0.65, 0], color=BLUE, stroke_width=7))
        blocks = VGroup(*[Square(0.32, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.7)
                          .move_to([-6.1, y, 0]) for y in (-0.35, 0.35)])
        memlab = T("cell membrane", 30, BLUE).move_to([-1.9, -2.1, 0])
        memlab.layout_ok = True  # deliberately labels the cell boundary from inside
        self.play(FadeIn(gate), FadeIn(blocks), run_time=0.4)
        self.play(blocks.animate.shift(RIGHT * 1.45), FadeIn(memlab), run_time=0.85)
        self.at("Cytoplasm fills")
        cyto = b.body.copy().set_stroke(opacity=0).set_fill(BLUE, opacity=0.18)
        cytolab = T("cytoplasm", 31, BLUE).move_to([2.2, -2.05, 0])
        cytolab.layout_ok = True  # deliberately labels the filled cell interior
        self.play(FadeIn(cyto), FadeIn(cytolab), run_time=0.65)
        self.at("Ribosomes build proteins")
        ribs = VGroup(ribosome([-0.1, 1.2, 0]), ribosome([1.5, 0.25, 0]), ribosome([3.2, 1.25, 0]))
        dna = gene_block("DNA instructions", [-2.1, 0.65, 0], 0.9)
        feed = arrow(dna.get_right() + RIGHT * 0.12, ribs[0].get_left(), ORANGE, 5)
        riblab = T("ribosomes build proteins", 30, TEAL).move_to([1.7, 2.25, 0])
        self.play(FadeIn(dna), run_time=0.35)
        self.play(FadeIn(ribs), GrowArrow(feed), FadeIn(riblab), run_time=0.75)
        bob(ribs, amp=0.055, speed=2.0)
        self.at("That DNA sits in a nucleoid")
        zone = Ellipse(width=3.25, height=2.0, stroke_color=ORANGE, stroke_width=3,
                       fill_color=ORANGE, fill_opacity=0.05).move_to([-2.1, 0.65, 0])
        nlab = T("nucleoid · no membrane", 30, ORANGE).move_to([-2.0, -1.0, 0])
        self.play(Create(zone), FadeIn(nlab), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S04MoreParts(SpokenScene):
    def construct(self):
        b = working_bacterium([0, 0.1, 0], 8.2, 4.35)
        self.add(b)
        self.at("cell wall")
        wall = RoundedRectangle(corner_radius=2.25, width=8.6, height=4.75, stroke_color=GOLD,
                                stroke_width=8, fill_opacity=0).move_to([0, 0.1, 0])
        water = VGroup(*[arrow(p, q, BLUE, 5) for p, q in [([-5.8, 1.4, 0], [-4.55, 1.0, 0]),
                                                            ([-5.8, -1.2, 0], [-4.55, -0.8, 0]),
                                                            ([5.8, 1.4, 0], [4.55, 1.0, 0]),
                                                            ([5.8, -1.2, 0], [4.55, -0.8, 0])]])
        lab = T("often: cell wall braces the cell", 32, GOLD).move_to([0, 3.2, 0])
        self.play(FadeIn(water), Create(wall), FadeIn(lab), run_time=0.8)
        self.at("when water enters")
        self.play(*[a.animate.shift(0.25 * (RIGHT if a.get_center()[0] < 0 else LEFT)) for a in water],
                  run_time=0.8)
        self.at("Some have a capsule")
        capsule = RoundedRectangle(corner_radius=2.55, width=9.15, height=5.25, stroke_color=TEAL,
                                   stroke_width=4, fill_color=TEAL, fill_opacity=0.05).move_to([0, 0.1, 0])
        caplab = T("sometimes: capsule", 30, TEAL).move_to([3.7, -2.75, 0])
        self.play(FadeOut(water), FadeIn(capsule), FadeIn(caplab), run_time=0.65)
        self.at("Some have flagella")
        flag = ParametricFunction(lambda t: np.array([4.15 + 0.42 * t, 0.1 + 0.38 * np.sin(4.2 * t), 0]),
                                  t_range=[0, 5.4], color=GREY, stroke_width=6)
        flab = T("sometimes: spinning flagellum", 30, TEXT).move_to([3.5, 2.8, 0])
        self.play(FadeOut(capsule), FadeOut(caplab), Create(flag), FadeIn(flab), run_time=0.75)
        self.play(Rotate(flag, angle=TAU, axis=RIGHT, about_point=flag.get_start()),
                  VGroup(b, wall, flag).animate.shift(RIGHT * 0.75), run_time=1.6, rate_func=linear)
        self.at("These parts vary")
        self.play(FadeOut(flag), FadeOut(flab), FadeOut(wall), run_time=0.5)
        rule = T("the working cell remains", 40, GREEN, weight=BOLD).move_to([0, -2.85, 0])
        self.play(FadeIn(rule), Indicate(b.ribs, color=TEAL), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S05VirusParts(SpokenScene):
    def construct(self):
        b = bacterium([-4.75, 0.6, 0], 3.8, 2.5, True)
        bob(b.ribs, amp=0.04, speed=2.0)
        v = virus([2.1, 0.2, 0], 2.25)
        self.add(b)
        self.play(FadeIn(v), run_time=0.7)
        self.at("open the virus")
        self.play(v.cap.animate.scale(1.18), run_time=0.65)
        self.at("DNA or RNA")
        self.play(Indicate(v.core, color=ORANGE), run_time=0.6)
        self.at("protein capsid")
        clab = T("protein capsid", 32, YELLOW, weight=BOLD).move_to([2.1, 3.45, 0])
        self.play(FadeIn(clab), Indicate(v.cap, color=YELLOW), run_time=0.6)
        self.at("Some viruses add a lipid envelope")
        env = Circle(radius=2.75, stroke_color=BLUE, stroke_width=5, fill_color=BLUE,
                     fill_opacity=0.04).move_to([2.1, 0.2, 0])
        elab = T("some: envelope", 30, BLUE).move_to([5.0, -2.7, 0])
        self.play(FadeIn(env), FadeIn(elab), run_time=0.65)
        self.at("There is no cytoplasm")
        no1 = chip("no cytoplasm", RED, 30).move_to([-1.05, -2.65, 0])
        self.play(FadeIn(no1), run_time=0.45)
        self.at("and no ribosome workbench")
        absent = ribosome([2.1, -0.5, 0], 1.1)
        x = VGroup(Line(absent.get_corner(UL), absent.get_corner(DR), color=RED, stroke_width=8),
                   Line(absent.get_corner(DL), absent.get_corner(UR), color=RED, stroke_width=8))
        no2 = T("no ribosomes", 30, RED).move_to([2.1, -1.55, 0])
        self.play(FadeIn(absent), Create(x), FadeIn(no2), run_time=0.65)
        self.at("A host cell must build")
        route = arrow(v.core.get_left(), b.ribs.get_right(), ORANGE, 5)
        self.play(GrowArrow(route), Indicate(b.ribs, color=TEAL), run_time=0.85)
        self.add(scope_tag("schematic"))
        self.finish()


class S06SharedGenes(SpokenScene):
    def construct(self):
        b = bacterium([-3.7, 0.25, 0], 5.2, 3.25, True)
        v = virus([3.7, 0.25, 0], 1.55)
        bob(b, amp=0.11, speed=1.25)
        self.add(b, v)
        self.at("Genes are the shared part")
        self.play(b.dna.animate.move_to([-1.2, 2.5, 0]), v.core.animate.move_to([1.2, 2.5, 0]), run_time=0.8)
        shared = T("shared: genes", 36, ORANGE, weight=BOLD).move_to([0, 3.25, 0])
        self.play(FadeIn(shared), run_time=0.4)
        self.at("not proof that both are cells")
        cell_lab = T("cell", 34, GREEN, weight=BOLD).move_to([-3.7, -1.95, 0])
        non_lab = T("not a cell", 34, RED, weight=BOLD).move_to([3.7, -2.05, 0])
        self.play(FadeIn(cell_lab), FadeIn(non_lab), run_time=0.55)
        self.at("with its own ribosomes")
        path_b = arrow([-2.9, 0.8, 0], b.ribs.get_center(), ORANGE, 5)
        self.play(GrowArrow(path_b), Indicate(b.ribs, color=TEAL), run_time=0.7)
        self.at("only after they reach")
        host = host_cell([5.35, 0.25, 0], 2.45, 4.7)
        dotted = DashedLine([2.65, -1.45, 0], host.ribs.get_center(), color=ORANGE,
                            stroke_width=5, dash_length=0.18)
        self.play(FadeOut(cell_lab), FadeOut(non_lab), v.animate.move_to([2.65, 0.2, 0]), FadeIn(host), run_time=0.65)
        self.play(Create(dotted), Indicate(host.ribs, color=TEAL), run_time=0.75)
        self.finish()


class S07EnergyCarbon(SpokenScene):
    def construct(self):
        b = working_bacterium([2.0, 0.2, 0], 5.3, 3.3)
        self.add(b)
        self.at("needs energy and carbon")
        lanes = input_lanes([2.0, 0.2, 0])
        self.play(GrowArrow(lanes[0]), GrowArrow(lanes[1]), run_time=0.8)
        self.play(FadeIn(lanes[2:]), run_time=0.4)
        self.at("Energy powers the work")
        self.play(Indicate(lanes[0], color=GOLD), Indicate(b.ribs, color=TEAL), run_time=0.75)
        self.at("Carbon supplies material")
        parts = VGroup(*[Square(0.26, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.8)
                         .move_to([0.25 + i * 0.38, -0.75, 0]) for i in range(4)])
        self.play(FadeIn(parts), parts.animate.shift(RIGHT * 2.2), run_time=0.85)
        self.at("sort bacteria into common patterns")
        header = T("three common patterns", 40, GOLD, font=TITLE_FONT).move_to([0, 3.25, 0])
        forks = VGroup(*[CurvedArrow([-4.0, y, 0], [-1.1, yy, 0], angle=a, color=GREY,
                                     stroke_width=3, tip_length=0.18)
                         for y, yy, a in [(1.25, 2.05, 0.22), (0.25, 0.4, 0.0), (-0.75, -1.35, -0.22)]])
        self.play(FadeIn(header), LaggedStart(*[Create(x) for x in forks], lag_ratio=0.2), run_time=1.0)
        self.finish()


class S08Patterns(SpokenScene):
    def construct(self):
        b = working_bacterium([2.3, 0.1, 0], 5.0, 3.05)
        lanes = input_lanes([2.3, 0.1, 0])
        self.add(b, lanes[0], lanes[1])
        name = T("HETEROTROPH", 38, GOLD, weight=BOLD).move_to([0, 3.25, 0])
        food1 = chip("carbon compounds", PURPLE, 28).move_to([-4.6, 1.2, 0])
        food2 = food1.copy().move_to([-4.6, -0.8, 0])
        self.at("Heterotrophs take in")
        self.play(FadeIn(name), FadeIn(food1), FadeIn(food2), run_time=0.55)
        self.play(food1.animate.shift(RIGHT * 0.15), food2.animate.shift(RIGHT * 0.15), run_time=0.8)
        self.at("Photoautotrophs use light")
        photo = T("PHOTOAUTOTROPH", 38, GOLD, weight=BOLD).move_to(name)
        beam = VGroup(*[Line([-5.7, 2.0 - i * 0.28, 0], [-3.0, 1.3 - i * 0.18, 0],
                                 color=GOLD, stroke_width=7) for i in range(3)])
        co2 = chip("carbon dioxide", PURPLE, 28).move_to([-4.6, -0.8, 0])
        self.play(swap(name, photo), FadeOut(food1), FadeOut(food2), FadeIn(beam), FadeIn(co2), run_time=0.75)
        self.play(beam.animate.shift(RIGHT * 0.35), co2.animate.shift(RIGHT * 0.15), run_time=0.75)
        self.at("Chemoautotrophs use chemicals")
        chemo = T("CHEMOAUTOTROPH", 38, GOLD, weight=BOLD).move_to(name)
        sulfur = chip("sulfur compounds", PURPLE, 28).move_to([-4.6, 1.2, 0])
        co2b = chip("carbon dioxide", PURPLE, 28).move_to([-4.6, -0.8, 0])
        self.play(swap(photo, chemo), FadeOut(beam), FadeOut(co2), FadeIn(sulfur), FadeIn(co2b), run_time=0.75)
        self.play(sulfur.animate.shift(RIGHT * 0.15), co2b.animate.shift(RIGHT * 0.15), run_time=0.8)
        self.finish()


class S09Predict(SpokenScene):
    def construct(self):
        world = spring_world(True)
        self.play(FadeIn(world[0]), FadeIn(world[1]), run_time=0.55)
        self.at("dark spring")
        self.play(FadeIn(world.bacterium), run_time=0.55)
        dark = T("dark spring · no light", 34, TEXT, weight=BOLD).move_to([0, 3.35, 0])
        self.play(FadeIn(dark), run_time=0.4)
        self.at("uses sulfur compounds")
        self.play(FadeIn(world.sulfur), GrowArrow(world[5]), run_time=0.6)
        self.play(Indicate(world.sulfur, color=GOLD), run_time=0.55)
        self.at("carbon dioxide for carbon")
        self.play(FadeIn(world.co2), GrowArrow(world[6]), run_time=0.6)
        self.play(Indicate(world.co2, color=PURPLE), run_time=0.55)
        self.at("Which name fits")
        self.play(FadeIn(world.names), run_time=0.6)
        q = question_card("Which name fits — and which input tells you?", y=-3.25, size=29)
        self.play(FadeIn(q), run_time=0.45)
        self.finish()


class S10Pause(PredictPause):
    QUESTION = "Which name fits — and which input tells you?"
    SECONDS = 4.5
    CARD = {"y": -3.25, "size": 29}

    def backdrop(self):
        world = spring_world(True)
        world.add(T("dark spring · no light", 34, TEXT, weight=BOLD).move_to([0, 3.35, 0]))
        bob(world.sulfur, amp=0.045, speed=1.7)
        bob(world.co2, amp=0.045, speed=1.7, seed=3)
        return world


class S11Reveal(SpokenScene):
    def construct(self):
        world = spring_world(False)
        bob(world.sulfur, amp=0.13, speed=1.35)
        bob(world.co2, amp=0.13, speed=1.35, seed=3)
        self.add(world)
        self.at("Chemo autotroph fits")
        answer = T("CHEMOAUTOTROPH", 40, GOLD, weight=BOLD).move_to([2.9, 2.3, 0])
        self.play(FadeIn(answer, shift=DOWN * 0.2), run_time=0.6)
        self.at("Chemical energy selects chemo")
        chemo = T("CHEMO", 34, GOLD, weight=BOLD).move_to([-3.1, 2.35, 0])
        self.play(ReplacementTransform(answer.copy(), chemo), Indicate(world.sulfur, color=GOLD), run_time=0.75)
        self.at("carbon dioxide supplies the carbon")
        auto = T("AUTOTROPH", 34, PURPLE, weight=BOLD).move_to([4.25, 1.25, 0])
        self.play(ReplacementTransform(answer.copy(), auto), Indicate(world.co2, color=PURPLE), run_time=0.75)
        self.at("The model is a simplification")
        simp = scope_tag("useful simplification", 25, GREY)
        self.play(FadeIn(simp), run_time=0.45)
        self.at("separate questions")
        divider = Line([-1.25, 2.0, 0], [-1.25, -1.45, 0], color=GREY, stroke_width=3)
        self.play(Create(divider), world.sulfur.animate.shift(UP * 0.25), world.co2.animate.shift(DOWN * 0.25), run_time=0.7)
        self.at("a few bacteria mix the patterns")
        mixed = VGroup(DashedLine([-3.7, 0.85, 0], [-1.7, -0.45, 0], color=GREY, stroke_width=3),
                       DashedLine([-3.7, -0.7, 0], [-1.7, 0.6, 0], color=GREY, stroke_width=3))
        self.play(Create(mixed), run_time=0.75)
        self.finish()


class S12Dependence(SpokenScene):
    def construct(self):
        host = host_cell([0, 0.0, 0], 11.7, 6.1)
        question = T("DOES DEPENDENCE DECIDE?", 40, GOLD, font=TITLE_FONT).move_to([0, 3.5, 0])
        self.play(FadeIn(host.body), FadeIn(question), run_time=0.6)
        self.at("Some bacteria grow only inside")
        b = bacterium([-2.7, 0.1, 0], 3.7, 2.35, True)
        self.play(FadeIn(b), run_time=0.55)
        dep = T("dependent cell", 32, GREEN, weight=BOLD).move_to([-2.7, -1.75, 0])
        self.play(FadeIn(dep), run_time=0.4)
        self.at("keep ribosomes and metabolism")
        energy = arrow([-4.55, 1.15, 0], [-3.95, 0.85, 0], GOLD, 5)
        self.play(GrowArrow(energy), Indicate(b.ribs, color=TEAL), run_time=0.75)
        bob(b.ribs, amp=0.045, speed=2.0)
        self.at("Viruses remain different")
        v = virus([3.0, 0.2, 0], 1.1)
        self.play(FadeIn(v), run_time=0.55)
        non = T("noncellular virus", 32, RED, weight=BOLD).move_to([3.0, -1.75, 0])
        self.play(FadeIn(non), run_time=0.4)
        self.at("no ribosomes of their own")
        route = DashedLine(v.core.get_left(), host.ribs[2].get_center(), color=ORANGE,
                           stroke_width=5, dash_length=0.16)
        self.play(Create(route), Indicate(host.ribs[2], color=TEAL), run_time=0.75)
        rule = caption("Dependence does not decide it; cell parts do.", color=GOLD, y=-3.4)
        self.play(FadeIn(rule), run_time=0.5)
        self.finish()


class S13Size(SpokenScene):
    def construct(self):
        track = Line([-5.8, 0, 0], [5.8, 0, 0], color=GREY, stroke_width=5)
        question = T("DOES SIZE DECIDE?", 46, GOLD, font=TITLE_FONT).move_to([0, 3.05, 0])
        typical_v = virus([-3.9, 0.85, 0], 0.55, labelled=False)
        typical_b = bacterium([1.2, 0.85, 0], 3.3, 1.45, False)
        self.play(Create(track), FadeIn(question), FadeIn(typical_v), FadeIn(typical_b), run_time=0.75)
        self.at("Most viruses are smaller")
        labs = VGroup(T("typical virus", 30, YELLOW).next_to(typical_v, UP, buff=0.18),
                      T("typical bacterium", 30, BLUE).next_to(typical_b, UP, buff=0.18))
        self.play(FadeIn(labs), run_time=0.55)
        self.at("some giant viruses")
        giant = virus([-4.2, -1.45, 0], 1.1, labelled=False)
        small_b = bacterium([1.2, -1.45, 0], 1.8, 0.92, False)
        self.play(FadeIn(giant), FadeIn(small_b), run_time=0.55)
        self.at("longer than small bacteria")
        self.play(giant.animate.move_to([2.1, -1.45, 0]), small_b.animate.move_to([-1.15, -1.45, 0]), run_time=0.9)
        self.at("that shortcut breaks")
        test = T("SIZE TEST", 38, GREY, weight=BOLD).move_to([0, 3.05, 0])
        test.layout_ok = True  # the crack is an intentional strike-through
        crack = VGroup(Line([-0.35, 3.35, 0], [0.15, 2.75, 0], color=RED, stroke_width=7),
                       Line([0.15, 2.75, 0], [0.45, 3.15, 0], color=RED, stroke_width=7))
        self.play(ReplacementTransform(question, test), Create(crack), run_time=0.55)
        self.at("Parts in work matter")
        rule = T("PARTS + WORK", 46, GOLD, weight=BOLD).move_to([0, -3.15, 0])
        self.play(FadeIn(rule), FadeOut(test), FadeOut(crack), run_time=0.65)
        self.finish()


class S14Rule(SpokenScene):
    def construct(self):
        b = bacterium([-3.55, 0.25, 0], 5.3, 3.3, True)
        v = virus([3.75, 0.25, 0], 1.45)
        self.play(FadeIn(b), FadeIn(v), run_time=0.65)
        self.at("Bacterial parts let the cell")
        inputs = VGroup(*[Square(0.3, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.8)
                          .move_to([-6.1, y, 0]) for y in (-0.4, 0.4)])
        self.play(FadeIn(inputs), inputs.animate.shift(RIGHT * 1.2), run_time=0.75)
        self.at("build proteins")
        bob(b.ribs, amp=0.055, speed=2.0)
        proteins = VGroup(*[Square(0.24, stroke_color=TEAL, fill_color=TEAL, fill_opacity=0.75)
                            .move_to([-2.2 + 0.38 * i, -1.0, 0]) for i in range(4)])
        self.play(Indicate(b.ribs, color=TEAL), FadeIn(proteins), run_time=0.75)
        self.at("Viral parts carry genes")
        host = host_cell([5.35, 0.2, 0], 2.0, 4.4)
        v.core[1].layout_ok = True  # the gene label intentionally enters the host-cell outline
        self.play(FadeIn(host), v.animate.move_to([3.0, 0.25, 0]), run_time=0.75)
        self.play(Indicate(v.core, color=ORANGE), run_time=0.45)
        self.at("Bacteria are living cells")
        left = T("living cell", 36, GREEN, weight=BOLD).move_to([-3.55, -2.35, 0])
        self.play(FadeIn(left), run_time=0.45)
        self.at("Viruses are not cells")
        right = T("not a cell · classed nonliving", 32, RED, weight=BOLD).move_to([3.25, -2.35, 0])
        self.play(FadeIn(right), run_time=0.45)
        rule = T("PARTS EXPLAIN THE DIFFERENCE", 40, GOLD, font=TITLE_FONT).move_to([0, 3.25, 0])
        self.play(FadeIn(rule), run_time=0.6)
        self.finish()


class S15End(EndCard):
    LINE = "Bacteria are living cells; viruses are not cells and are classed nonliving."
