"""Forward Is the Default — secretory-pathway teaching film.

COLOR MAP (kept constant throughout)
  BLUE   membranes and secretory-pathway compartments
  GOLD   the pulse-labelled cargo cohort
  GREY   unlabelled protein and secondary structure
  TEAL   ER chaperones, KDEL, and the retrieval route
  WHITE  KDEL receptor and questions
  RED    the mannosidase-II threshold
  SAND   constitutive carriers
  GREEN  mannose circles
  BLUE   glucose circles and GlcNAc squares (shape distinguishes them)
  YELLOW galactose circles
  PURPLE sialic-acid diamonds

All glycans are explicitly schematic symbol trees, never molecular structures.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58AE6"
SAND = "#D9C3A0"
INK = "#202531"

# The shared world.  These coordinates never drift between whole-world scenes.
ER_X, ERGIC_X = -5.15, -3.48
GOLGI_X = (-2.15, -1.18, -0.21)
TGN_X, MEM_X = 1.18, 5.75
WORLD_Y = 0.0


def label(text, p, color=TEXT, size=28):
    return T(text, size=size, color=color).move_to(p)


def cell_outline():
    return RoundedRectangle(width=12.5, height=5.65, corner_radius=0.75,
                            stroke_color=BLUE, stroke_width=4, fill_opacity=0).move_to([0, -0.05, 0])


def er_stack(scale=1.0, center=np.array([ER_X, WORLD_Y, 0.0])):
    bars = VGroup(*[
        RoundedRectangle(width=1.55, height=0.43, corner_radius=0.18,
                         stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.14)
        .move_to(center + UP * y)
        for y in (0.72, 0.0, -0.72)
    ])
    ribosomes = VGroup(*[
        Dot(center + np.array([-0.58 + 0.29 * k, y + 0.27, 0]), radius=0.045, color=GREY)
        for y in (0.72, 0.0, -0.72) for k in range(5)
    ])
    return VGroup(bars, ribosomes).scale(scale, about_point=center)


def ergic():
    return VGroup(*[
        Circle(radius=0.27, stroke_color=BLUE, stroke_width=3,
               fill_color=BLUE, fill_opacity=0.12).move_to([ERGIC_X, y, 0])
        for y in (0.65, 0, -0.65)
    ])


def golgi():
    return VGroup(*[
        RoundedRectangle(width=0.58, height=2.35, corner_radius=0.25,
                         stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.13)
        .move_to([x, 0, 0]) for x in GOLGI_X
    ])


def tgn():
    return VGroup(
        Arc(radius=0.66, start_angle=-PI / 2, angle=PI, color=BLUE, stroke_width=4).move_to([TGN_X, 0.35, 0]),
        Arc(radius=0.55, start_angle=PI / 2, angle=PI, color=BLUE, stroke_width=4).move_to([TGN_X, -0.45, 0]),
        Line([TGN_X, -0.95, 0], [TGN_X + 0.25, -1.25, 0], color=BLUE, stroke_width=4),
    )


def membrane():
    # Two bars leave a visible secretion door at y=1.0.
    return VGroup(
        Line([MEM_X, -2.65, 0], [MEM_X, 0.55, 0], color=BLUE, stroke_width=8),
        Line([MEM_X, 1.45, 0], [MEM_X, 2.65, 0], color=BLUE, stroke_width=8),
    )


def shelf():
    line = Line([2.25, -1.55, 0], [5.25, -1.55, 0], color=GREY, stroke_width=4)
    gs = VGroup(*[
        Circle(radius=0.31, stroke_color=BLUE, stroke_width=3, fill_color=INK, fill_opacity=0.55)
        .move_to([2.65 + 0.62 * i, -1.13, 0]) for i in range(5)
    ])
    return VGroup(line, gs)


def routes():
    return VGroup(
        VMobject(color=GREY, stroke_width=3).set_points_smoothly([
            [TGN_X + 0.35, 0.35, 0], [2.7, 1.05, 0], [4.3, 1.0, 0], [MEM_X - 0.15, 1.0, 0]]),
        VMobject(color=GREY, stroke_width=3).set_points_smoothly([
            [TGN_X + 0.3, -0.3, 0], [2.0, -0.75, 0], [2.45, -1.1, 0]]),
    )


def flow_arrow():
    base = Arrow([-5.5, -2.15, 0], [4.9, -2.15, 0], buff=0, color=GREY,
                 stroke_width=2.5, tip_length=0.18).set_opacity(0.65)
    chevs = VGroup(*[
        VGroup(Line([-0.25, 0.16, 0], [0, 0, 0]), Line([0, 0, 0], [-0.25, -0.16, 0]))
        .set_stroke(GREY, 4).move_to([-4.7 + i * 1.05, -2.15, 0]) for i in range(10)
    ])
    # The flow is part of the scientific picture, not decorative ambient motion.
    # It keeps travelling during narrated holds and wraps seamlessly.
    for chev in chevs:
        def move_right(m, dt):
            m.shift(RIGHT * 1.8 * dt)
            if m.get_x() > 5.1:
                m.shift(LEFT * 10.5)
        chev.add_updater(move_right)
    return VGroup(base, chevs)


def world(with_clock=True, with_gel=False):
    organelles = VGroup(cell_outline(), er_stack(), ergic(), golgi(), tgn(), membrane(), shelf(), routes(), flow_arrow())
    extras = VGroup()
    if with_clock:
        extras.add(clock(0))
    if with_gel:
        extras.add(gel_panel(small=True))
    return VGroup(organelles, extras)


def station_labels():
    return VGroup(
        label("rough ER", [ER_X, -1.38, 0], BLUE),
        label("ERGIC", [ERGIC_X, -1.38, 0], BLUE),
        label("Golgi stack", [GOLGI_X[1], -1.55, 0], BLUE),
        label("TGN", [TGN_X, -1.55, 0], BLUE),
    )


def clock(minutes):
    box = RoundedRectangle(width=1.45, height=0.58, corner_radius=0.12,
                           stroke_color=TEXT, stroke_width=2, fill_color=INK, fill_opacity=0.85)
    txt = M(f"min {minutes}", size=28).move_to(box)
    return VGroup(box, txt).move_to([-5.55, 3.18, 0])


def gel_panel(small=False):
    w, h = (2.35, 1.45) if small else (5.4, 4.15)
    panel = RoundedRectangle(width=w, height=h, corner_radius=0.12,
                             stroke_color=GREY, stroke_width=2, fill_color=INK, fill_opacity=0.82)
    lanes = VGroup()
    xs = np.linspace(-0.72 * w / 2, 0.72 * w / 2, 4)
    for i, x in enumerate(xs):
        lanes.add(Line([x, -0.28 * h, 0], [x, 0.27 * h, 0], color=GREY, stroke_width=1.2).set_opacity(0.35))
        lanes.add(M(str((0, 15, 30, 60)[i]), size=22 if small else 28, color=TEXT).move_to([x, 0.38 * h, 0]))
    g = VGroup(panel, lanes)
    if small:
        g.scale(0.82).move_to([4.35, -2.75, 0])
    return g


def cargo_dot(p, color=GOLD, r=0.105):
    return Dot(p, radius=r, color=color)


def cargo_cloud(center, spread=0.55, n=11, color=GOLD):
    offsets = [(-0.9, .1), (-.65, -.3), (-.45, .38), (-.25, -.12), (0, .05),
               (.18, .35), (.35, -.25), (.55, .15), (.75, -.38), (.92, .28), (1.1, 0)]
    return VGroup(*[cargo_dot(np.array(center) + [x * spread, y * spread, 0], color, .07 + .035 * (1 - min(abs(x), 1)))
                    for x, y in offsets[:n]])


def protein_blob(p, color=GOLD, scale=1.0):
    return RoundedRectangle(width=0.72 * scale, height=0.42 * scale, corner_radius=0.19 * scale,
                            stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.35).move_to(p)


def glycan_tree(center=np.array([0., 0., 0.]), scale=1.0, late=False):
    """A labelled-symbol tree; lines are only hierarchy connectors, not chemical bonds."""
    c = np.array(center, float)
    pts = [c + scale * np.array(v) for v in (
        (0, 0, 0), (-.24, .32, 0), (.24, .32, 0),
        (-.46, .65, 0), (-.14, .68, 0), (.14, .68, 0), (.46, .65, 0),
        (-.55, .98, 0), (-.28, 1.02, 0), (0, 1.0, 0), (.28, 1.02, 0), (.55, .98, 0)
    )]
    links = VGroup(*[Line(pts[a], pts[b], color=GREY, stroke_width=2) for a, b in
                     ((0,1),(0,2),(1,3),(1,4),(2,5),(2,6),(3,7),(4,8),(5,9),(6,10),(6,11))])
    nodes = VGroup(Square(side_length=.17 * scale, color=BLUE, fill_opacity=.9).move_to(pts[0]),
                   Square(side_length=.17 * scale, color=BLUE, fill_opacity=.9).move_to(pts[1]))
    for p in pts[2:10]:
        nodes.add(Circle(radius=.085 * scale, color=GREEN, fill_opacity=.9).move_to(p))
    tips = VGroup(*[Circle(radius=.08 * scale, color=BLUE, fill_opacity=.9).move_to(p) for p in pts[9:12]])
    tree = VGroup(links, nodes, tips)
    if late:
        tree.add(Circle(radius=.08 * scale, color=YELLOW, fill_opacity=.9).move_to(pts[7] + LEFT * .18 * scale),
                 Square(side_length=.13 * scale, color=PURPLE, fill_opacity=.9).rotate(PI/4).move_to(pts[11] + RIGHT * .2 * scale))
    return tree


def drift_chevrons(scene, flow, seconds, distance=0.8):
    """Visible, slow rightward motion tied to pathway direction."""
    scene.play(flow[1].animate.shift(RIGHT * distance), rate_func=linear, run_time=max(.2, seconds))


class S00Hook(SpokenScene):
    def construct(self):
        w = world()
        self.play(FadeIn(w[0]), run_time=.8)
        pulse = label("pulse", [-4.05, 1.45, 0], GOLD)
        gold = cargo_cloud([ER_X, 0, 0], .62, 9)
        self.at("Label the new proteins")
        self.add(pulse)
        self.play(LaggedStart(*[FadeIn(d, scale=.2) for d in gold], lag_ratio=.08), run_time=2.4)
        self.at("hours later")
        c60 = clock(60)
        smear = cargo_cloud([-1.0, 0.1, 0], 2.4, 11)
        self.remove(pulse)
        self.play(ReplacementTransform(w[1][0], c60), ReplacementTransform(gold, smear), run_time=1.2)
        q = T("?", size=92, color=TEXT).move_to([0, .9, 0])
        self.at("where are they")
        self.play(FadeIn(q, scale=.4), smear.animate.shift(RIGHT * .45), run_time=.8)
        bubble = Circle(radius=.78, color=TEXT, stroke_width=3).move_to([2.4, .65, 0])
        tree = glycan_tree([2.4, .15, 0], .62)
        treeq = T("?", size=40).move_to([2.4, 1.85, 0])
        question = T("Where are they?  Can they tell you?", size=34).move_to([0, 3.18, 0])
        self.at("proteins themselves")
        self.play(FadeOut(q), Create(bubble), FadeIn(tree), FadeIn(treeq), run_time=1.0)
        self.at("how far")
        self.play(FadeIn(question), smear.animate.shift(RIGHT * .4), run_time=.8)
        self.finish()


class S01Title(Scene):
    def construct(self):
        # Keep the hook's world visible: this is a title overlay, not a cut to an empty card.
        w = world()
        title = T("Forward Is the Default", size=54, font=TITLE_FONT)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        backing = RoundedRectangle(width=8.0, height=1.65, corner_radius=.2,
                                   stroke_width=0, fill_color=INK, fill_opacity=.94)
        card = VGroup(backing, title, rule)
        title.move_to([0, .28, 0])
        rule.move_to([0, -.42, 0])
        self.add(w)
        self.play(FadeIn(card), run_time=.35)
        self.wait(1.3)
        self.play(FadeOut(card), run_time=.35)


class S02Pulse(SpokenScene):
    def construct(self):
        w = world()
        self.add(w)
        pulse = label("pulse", [-4.05, 1.55, 0], GOLD, 40)
        gold = cargo_cloud([ER_X, 0, 0], .62, 9).scale(1.65, about_point=[ER_X,0,0])
        self.at("pulse chase")
        self.add(pulse)
        self.play(LaggedStart(*[FadeIn(d, scale=.2) for d in gold], lag_ratio=.08), run_time=2.0)
        chase = label("chase", [-4.05, 1.55, 0], GREY, 40)
        grey = cargo_cloud([ER_X - .15, -.15, 0], .75, 11, GREY).scale(1.55, about_point=[ER_X,0,0])
        self.at("then a flood")
        self.remove(pulse)
        self.add(chase)
        self.play(gold.animate.shift(RIGHT * .55),
                  LaggedStart(*[FadeIn(d, scale=.2) for d in grey], lag_ratio=.06), run_time=2.2)
        cohort = label("cohort", [ER_X, 1.55, 0], GOLD)
        self.at("Only the batch")
        self.play(Indicate(gold, color=GOLD), grey.animate.shift(RIGHT * .18), run_time=1.0)
        self.at("the cohort")
        self.remove(chase)
        self.play(FadeIn(cohort), gold.animate.shift(RIGHT * .3), run_time=.7)
        self.finish()


class S03Grains(SpokenScene):
    def construct(self):
        w = world(with_gel=False)
        self.add(w)
        credit = label("Lucien Caro & George Palade, 1964", [0, 3.2, 0], TEXT, 28)
        self.at("Caro and Pallade")
        self.play(FadeIn(credit), run_time=.8)
        layer = RoundedRectangle(width=12.15, height=5.25, corner_radius=.65, stroke_color=TEXT,
                                 stroke_width=2, fill_color=TEXT, fill_opacity=.035).move_to([0, -.05, 0])
        layerlab = label("photographic layer", [2.4, 2.25, 0], TEXT)
        grains = VGroup(*[Dot([-5.7 + .22*i, (-.38, .05, .55)[i%3], 0], radius=.105, color=TEXT) for i in range(8)])
        self.at("Silver grains")
        self.play(FadeIn(layer), FadeIn(layerlab), LaggedStart(*[FadeIn(g) for g in grains], lag_ratio=.08), run_time=1.8)
        note = label("grain positions: schematic", [0, -3.4, 0], TEXT, 28)
        self.play(FadeIn(note), grains.animate.shift(RIGHT * .35), run_time=.7)
        c5 = clock(5)
        self.at("five minutes")
        self.play(ReplacementTransform(w[1][0], c5), grains.animate.shift(RIGHT * .25), run_time=1.0)
        golgi_grains = VGroup(*[Dot([-2.6 + .23*i, (-.7, -.25, .2, .65)[i%4], 0], radius=.105, color=TEXT) for i in range(10)])
        c20 = clock(20)
        self.at("about 20")
        self.play(ReplacementTransform(grains, golgi_grains), ReplacementTransform(c5, c20), run_time=1.25)
        gran_grains = VGroup(*[Dot([2.5 + .35*(i%8), -1.08 + .14*(i%3), 0], radius=.095, color=TEXT) for i in range(15)])
        fills = VGroup(*[cargo_dot([2.65 + .62*i, -1.13, 0], GOLD, .18) for i in range(5)])
        c60 = clock(60)
        self.at("an hour")
        self.play(ReplacementTransform(golgi_grains, gran_grains), ReplacementTransform(c20, c60), FadeIn(fills), run_time=1.4)
        self.play(gran_grains.animate.shift(RIGHT * .15), run_time=.6)
        self.finish()


class S04Route(SpokenScene):
    def construct(self):
        w = world(with_gel=False)
        self.add(w)
        cloud = cargo_cloud([ER_X, 0, 0], .55, 11)
        self.add(cloud)
        labs = station_labels()
        self.at("peak moves forward")
        self.play(cloud.animate.move_to([ERGIC_X, 0, 0]), FadeIn(labs[0]), run_time=1.4)
        wide = cargo_cloud([GOLGI_X[0], 0, 0], 1.1, 11)
        self.at("spreads out")
        self.play(ReplacementTransform(cloud, wide), FadeIn(labs[1]), run_time=1.1)
        self.at("The ER")
        self.play(Indicate(w[0][1], color=GOLD), wide.animate.shift(RIGHT * .3), run_time=.7)
        self.at("sorting dock")
        self.play(Indicate(w[0][2], color=GOLD), FadeIn(labs[2]), wide.animate.move_to([-1.1, 0, 0]), run_time=1.0)
        self.at("Golgi stack")
        self.play(Indicate(w[0][3], color=GOLD), wide.animate.shift(RIGHT * .55), run_time=.8)
        self.at("routes split")
        self.play(FadeIn(labs[3]), Indicate(w[0][7], color=GOLD), wide.animate.move_to([1.2, 0, 0]), run_time=.8)
        self.finish()


def focused_processing_world():
    er = RoundedRectangle(width=2.35, height=4.4, corner_radius=.3, color=BLUE,
                          fill_color=BLUE, fill_opacity=.1).move_to([-5.15, 0, 0])
    sacs = VGroup(*[RoundedRectangle(width=1.25, height=4.4, corner_radius=.32, color=BLUE,
                                     fill_color=BLUE, fill_opacity=.1).move_to([x, 0, 0]) for x in (-2.0, 0, 2.0)])
    labels = VGroup(label("ER", [-5.15, -2.65, 0], BLUE), label("cis", [-2, -2.65, 0], BLUE),
                    label("medial", [0, -2.65, 0], BLUE), label("trans", [2, -2.65, 0], BLUE))
    return VGroup(er, sacs, labels)


class S05Tree(SpokenScene):
    def construct(self):
        stage = focused_processing_world()
        self.add(stage)
        p = protein_blob([-5.15, -1.2, 0], GOLD, 1.25)
        self.at("follow one protein")
        self.play(FadeIn(p, scale=.5), run_time=.9)
        tree = glycan_tree([-5.15, -.75, 0], .9)
        schematic = label("14-sugar core • schematic", [-3.9, 2.8, 0], TEXT, 28)
        self.at("ready made tree")
        self.add(schematic)
        self.play(FadeIn(tree, shift=DOWN*.3), run_time=1.3)
        folding = label("folding", [-5.15, -1.8, 0], GOLD)
        self.at("trimmed as it folds")
        self.play(FadeOut(tree[2], shift=UP*.35), p.animate.stretch(.68, 0), FadeIn(folding), run_time=1.25)
        self.at("In the Golgi")
        unit = VGroup(p, tree)
        self.remove(schematic)
        self.play(FadeOut(folding), unit.animate.shift(RIGHT * 3.15), run_time=1.15)
        washes = VGroup(*[RoundedRectangle(width=2.5, height=4.65, corner_radius=.35, stroke_width=0,
                                           fill_color=c, fill_opacity=.10).move_to([x, 0, 0])
                           for x, c in ((-2, GREEN), (0, BLUE), (2, PURPLE))])
        self.at("enzymes in successive")
        self.play(FadeIn(washes), unit.animate.shift(RIGHT * 1.8), run_time=1.15)
        newtree = glycan_tree([0, -.75, 0], .82, late=True)
        self.at("cut and rebuild")
        self.play(Transform(tree, newtree), p.animate.move_to([0, -1.2, 0]), run_time=1.0)
        redline = DashedLine([0, -2.3, 0], [0, 2.3, 0], color=RED, stroke_width=5)
        redlab = label("mannosidase II", [.05, 2.75, 0], RED)
        self.at("Manicidase II")
        self.play(Create(redline), FadeIn(redlab), run_time=.8)
        late_tree = glycan_tree([2, -.75, 0], .82, late=True)
        self.at("red line")
        self.play(Transform(tree, late_tree), p.animate.move_to([2, -1.2, 0]), run_time=1.05)
        self.finish()


class S06Odometer(SpokenScene):
    def construct(self):
        stage = focused_processing_world()
        self.add(stage)
        washes = VGroup(*[RoundedRectangle(width=3.0, height=4.55, corner_radius=.35, stroke_width=0,
                                           fill_color=c, fill_opacity=.12).move_to([x, 0, 0])
                           for x, c in ((-1.6, GREEN), (0, BLUE), (1.6, PURPLE))])
        p = protein_blob([0, -1.2, 0])
        tree = glycan_tree([0, -.75, 0], .82, late=True)
        self.at("enzymes overlap")
        self.play(FadeIn(washes), washes.animate.shift(RIGHT*.3), run_time=1.4)
        which = label("which sac?", [0, 2.75, 0], TEXT, 34)
        self.at("cannot say which sac")
        self.play(FadeIn(which), VGroup(p, tree).animate.shift(RIGHT*.65), washes.animate.shift(LEFT*.2), run_time=1.1)
        self.play(FadeOut(which), VGroup(p, tree).animate.shift(LEFT*.65), run_time=.6)
        early_steps = label("glucoses off  •  mannoses off  •  GlcNAc on", [0, 3.28, 0], TEXT, 28)
        late_steps = label("mannosidase II  •  galactose  •  sialic acid", [0, 2.73, 0], TEXT, 28)
        self.at("records the enzymes")
        self.play(FadeIn(early_steps), VGroup(p, tree).animate.shift(UP*.25), run_time=1.0)
        self.at("it has met")
        self.play(FadeIn(late_steps), Indicate(VGroup(early_steps, late_steps), color=GOLD), run_time=1.3)
        verdict = label("enzymes met — not an address", [0, 3.2, 0], TEXT, 32)
        self.at("rough odometer")
        self.play(FadeOut(early_steps), FadeOut(late_steps), FadeIn(verdict), washes.animate.shift(RIGHT*.25), run_time=.8)
        self.finish()


class S07Gel(SpokenScene):
    def construct(self):
        # Sampling world above, large readable gel below/right.
        cell = RoundedRectangle(width=6.2, height=2.6, corner_radius=.45, color=BLUE,
                                fill_color=BLUE, fill_opacity=.04).move_to([-3.25, 1.45, 0])
        samples = VGroup(*[RoundedRectangle(width=1.02, height=1.42, corner_radius=.15, color=TEXT,
                                            fill_color=INK, fill_opacity=.9).move_to([-5.05 + i*1.28, -.78, 0])
                           for i in range(4)])
        nums = VGroup(*[M(str(t), size=30).next_to(samples[i], DOWN, buff=.14) for i,t in enumerate((0,15,30,60))])
        pip = VGroup(Line([0,.35,0],[0,-.4,0], color=TEXT, stroke_width=5),
                     Triangle(color=TEXT, fill_opacity=.3).scale(.16).rotate(PI).move_to([0,-.48,0])).move_to([-5.0, 1.65, 0])
        cell_cargo = cargo_cloud([-3.25, 1.45, 0], 1.7, 11)
        for dot_ in cell_cargo:
            def stream(m, dt):
                m.shift(RIGHT * 1.45 * dt)
                if m.get_x() > -.55:
                    m.shift(LEFT * 5.35)
            dot_.add_updater(stream)
        self.add(cell, cell_cargo)
        self.at("sample at each")
        self.play(FadeIn(samples), FadeIn(nums), FadeIn(pip), run_time=1.1)
        sample_dots = VGroup()
        for i in range(4):
            aliquot = cargo_dot(samples[i].get_center() + DOWN*.42, GOLD, .11)
            sample_dots.add(aliquot)
            self.play(pip.animate.move_to(samples[i].get_top()+UP*.55),
                      FadeIn(aliquot), run_time=.55)
        scissors = VGroup(Circle(radius=.16, color=TEAL), Circle(radius=.16, color=TEAL),
                           Line([-.08,-.05,0],[.34,-.43,0], color=TEAL, stroke_width=4),
                           Line([.08,-.05,0],[-.34,-.43,0], color=TEAL, stroke_width=4))
        scissors.scale(.58).move_to(samples[3].get_center() + UP*.25)
        endoh = label("Endo H", [.12, -.60, 0], TEAL, 30)
        self.at("endoH")
        self.play(FadeIn(scissors), FadeIn(endoh), run_time=.9)
        mannose_box = RoundedRectangle(width=2.0, height=.85, corner_radius=.15, color=GREEN,
                                       fill_color=INK, fill_opacity=.94).move_to([-2.05, 2.12, 0])
        mannose = VGroup(*[Circle(radius=.1, color=GREEN, fill_opacity=.9).move_to([-2.42+.25*i, 2.12,0]) for i in range(4)])
        resistant_box = RoundedRectangle(width=2.0, height=.85, corner_radius=.15, color=BLUE,
                                         fill_color=INK, fill_opacity=.94).move_to([1.0,2.12,0])
        resistant = VGroup(Square(side_length=.2, color=BLUE, fill_opacity=.9),
                           Circle(radius=.1, color=YELLOW, fill_opacity=.9)).arrange(RIGHT,buff=.18).move_to([1.0,2.12,0])
        self.at("cuts chains still")
        self.play(FadeIn(mannose_box), FadeIn(mannose), Indicate(scissors, color=TEAL), run_time=.8)
        self.at("not those rebuilt")
        self.play(mannose.animate.shift(DOWN*.18).set_opacity(.25),
                  FadeIn(resistant_box), FadeIn(resistant), run_time=1.0)
        self.play(Indicate(resistant, color=TEXT), run_time=.6)
        self.at("Cut protein loses sugar")
        sample_group = VGroup(samples, nums, sample_dots)
        self.play(FadeOut(cell), FadeOut(cell_cargo), FadeOut(pip), FadeOut(scissors), FadeOut(endoh),
                  FadeOut(mannose_box), FadeOut(mannose), FadeOut(resistant_box), FadeOut(resistant),
                  sample_group.animate.scale(.78).to_edge(LEFT,buff=.4).shift(UP*.2), run_time=.9)
        panel = RoundedRectangle(width=7.2, height=5.5, corner_radius=.15, color=GREY,
                                 fill_color=INK, fill_opacity=.92).move_to([2.25,0,0])
        xs = [.85, 2.05, 3.25, 4.45]
        heads = VGroup(*[M(str(t), size=32).move_to([x,2.1,0]) for x,t in zip(xs,(0,15,30,60))])
        cut_vals, uncut_vals = (1.0,.67,.45,.20), (.07,.33,.55,.80)
        cuts = VGroup(*[Line([x,-1.0,0],[x+.88,-1.0,0], color=GOLD, stroke_width=18).set_opacity(1.0) for x in xs])
        uncuts = VGroup(*[Line([x,.55,0],[x+.88,.55,0], color=GOLD, stroke_width=18).set_opacity(.07) for x in xs])
        labs = VGroup(label("uncut", [-.55,.55,0], TEXT, 30), label("cut: faster", [-.35,-1,0], TEXT, 28),
                      label("illustrative data", [2.25,-2.25,0], TEXT, 28))
        self.play(FadeIn(panel), FadeIn(heads), FadeIn(labs), FadeIn(cuts), run_time=1.0)
        self.at("runs faster")
        fast = Arrow([5.55,.4,0],[5.55,-1.3,0], color=TEXT, stroke_width=4, tip_length=.18)
        self.play(GrowArrow(fast), cuts.animate.set_stroke(width=13), run_time=.8)
        self.at("Over the chase")
        shift = AnimationGroup(
            *[b.animate.set_opacity(v) for b, v in zip(cuts, cut_vals)],
            *[b.animate.set_opacity(v) for b, v in zip(uncuts, uncut_vals)],
            lag_ratio=.08,
        )
        self.play(shift, run_time=1.45)
        self.at("gives way")
        self.play(LaggedStart(*[Indicate(b,color=GOLD) for b in cuts], *[Indicate(b,color=GOLD) for b in uncuts], lag_ratio=.08), run_time=1.5)
        self.finish()


def chaperone(p, tagged=True):
    body = RoundedRectangle(width=1.0, height=.56, corner_radius=.24, color=TEAL,
                            fill_color=TEAL, fill_opacity=.25).move_to(p)
    parts = VGroup(body)
    if tagged:
        tail = Line(body.get_right(), body.get_right()+RIGHT*.45, color=TEAL, stroke_width=5)
        tag = label("KDEL", body.get_right()+RIGHT*.82, TEAL, 28)
        parts.add(tail,tag)
    return parts


class S08Kdel(SpokenScene):
    def construct(self):
        w = world(with_gel=False)
        self.add(w)
        chap_start = np.array([-4.95, 1.5, 0.0])
        chap = chaperone(chap_start).scale(1.28, about_point=chap_start)
        helper = label("ER chaperone", [-4.1,2.3,0], TEAL)
        self.at("ER chaperones")
        self.play(FadeIn(chap), FadeIn(helper), run_time=.8)
        self.at("leak forward")
        self.play(chap.animate.shift(RIGHT*1.15), FadeOut(helper), run_time=1.1)
        self.at("end in a tag")
        self.play(Indicate(chap[2], color=TEAL), chap.animate.shift(RIGHT*.35), run_time=.8)
        acidic = label("acidic compartment: KDEL receptor", [0, 3.12,0], TEXT, 28)
        target = np.array([-3.15,1.55,0.0])
        tail_c = chap.copy().move_to(target)[1].get_center()
        receptor = VGroup(Arc(radius=.34,start_angle=PI,angle=PI,color=TEXT,stroke_width=6),
                           Line([0,-.34,0],[0,-.75,0],color=TEXT,stroke_width=6)).scale(.55)
        receptor.move_to(tail_c + LEFT*.24 + DOWN*(receptor.height/2))
        self.at("slightly acidic")
        self.play(FadeIn(acidic), FadeIn(receptor), chap.animate.move_to(target), run_time=1.2)
        self.at("receptor grabs")
        self.play(Indicate(receptor,color=TEXT), Indicate(chap[2],color=TEXT), run_time=.8)
        ves = DashedVMobject(Circle(radius=.7,color=BLUE,stroke_width=4).move_to(chap[1].get_center()+LEFT*.45+DOWN*.05),num_dashes=18)
        cop = label("COPI vesicle", ves.get_center()+UP*.95+RIGHT*.6, BLUE)
        ret = CurvedArrow([-2.8,-1.5,0],[-4.75,-1.45,0],angle=-.35,color=TEAL,stroke_width=4)
        self.at("vesicle carries both")
        self.remove(acidic)
        self.play(FadeIn(ves), FadeIn(cop), Create(ret), run_time=.8)
        complex_ = VGroup(chap,receptor,ves)
        self.play(complex_.animate.shift(LEFT*.6), run_time=1.15)
        neutral = label("near neutral", [-3.7,2.35,0], TEXT)
        self.at("near neutral")
        self.play(FadeOut(cop), FadeIn(neutral), FadeOut(ves),
                  chap.animate.shift(LEFT*.2), receptor.animate.shift(RIGHT*.25), run_time=.85)
        self.at("receptor lets go")
        self.play(chap.animate.shift(LEFT*.2), receptor.animate.shift(RIGHT*.8+DOWN*.3), ret.animate.set_opacity(.35), run_time=.8)
        self.finish()


class S09Predict(SpokenScene):
    def construct(self):
        w = world(with_gel=False)
        self.add(w)
        chap_start = np.array([-4.95, 1.45, 0.0])
        chap = chaperone(chap_start).scale(1.25, about_point=chap_start)
        name = label("grp78", [-4.95,2.2,0], TEAL)
        self.add(chap,name)
        scissors = VGroup(Line([-.25,.25,0],[.25,-.25,0],color=TEXT,stroke_width=5),
                          Line([.25,.25,0],[-.25,-.25,0],color=TEXT,stroke_width=5)).move_to([-3.55,1.45,0])
        self.at("snip the tag")
        self.play(FadeIn(scissors), chap[1:].animate.shift(RIGHT*.45).set_opacity(0), run_time=.9)
        deleted = label("grp78 • KDEL deleted", [-3.7,2.2,0], TEAL)
        self.play(ReplacementTransform(name,deleted), FadeOut(scissors), run_time=.55)
        credit = label("Munro & Pelham, 1987 • COS cells", [0,3.15,0], TEXT,28)
        self.at("Sean Munro")
        self.play(FadeIn(credit), chap[0].animate.shift(RIGHT*.35), run_time=1.0)
        self.at("cultured monkey cells")
        self.play(chap[0].animate.shift(RIGHT*.45), run_time=.85)
        q = label("Where does it end up?", [0,2.15,0], TEXT,38)
        self.at("Where does it")
        self.play(FadeOut(credit), FadeOut(deleted), FadeIn(q), chap[0].animate.shift(RIGHT*.35), run_time=.8)
        self.finish()


class S10Think(Scene):
    def construct(self):
        w = world(with_gel=False)
        q = label("Where does it end up?", [0,2.15,0], TEXT,38)
        chap_start = np.array([ER_X+.8, 1.05, 0.0])
        chap = chaperone(chap_start,tagged=False).scale(1.55, about_point=chap_start)
        receptors = VGroup(*[VGroup(Arc(radius=.25,start_angle=PI,angle=PI,color=TEXT,stroke_width=5),
                                      Line([0,-.25,0],[0,-.62,0],color=TEXT,stroke_width=5)).move_to([ERGIC_X,y,0])
                             for y in (.55,-.55)])
        self.add(w,q,chap,receptors)
        self.play(chap.animate.shift(UP*.45+RIGHT*.35), w[0][8][1].animate.shift(RIGHT*.65), rate_func=there_and_back, run_time=2.2)
        self.play(chap.animate.shift(DOWN*.45+RIGHT*.35), w[0][8][1].animate.shift(RIGHT*.65), rate_func=there_and_back, run_time=2.2)


class S11Rule(SpokenScene):
    def construct(self):
        w = world(with_gel=False)
        self.add(w)
        chap = chaperone([ER_X+.8,0,0],tagged=False)
        cargo = cargo_cloud([ER_X+.35,.2,0],.42,7)
        q = label("Where does it end up?", [0,2.15,0], TEXT,38)
        self.add(chap,cargo,q)
        self.at("secreted with the cargo")
        self.play(FadeOut(q), VGroup(chap,cargo).animate.move_to([ERGIC_X,0,0]), run_time=1.0)
        receptors = VGroup(*[VGroup(Arc(radius=.25,start_angle=PI,angle=PI,color=TEXT,stroke_width=5),
                                      Line([0,-.25,0],[0,-.62,0],color=TEXT,stroke_width=5)).move_to([ERGIC_X,y,0])
                             for y in (.55,-.55)])
        self.play(FadeIn(receptors), VGroup(chap,cargo).animate.move_to([-1.1,.2,0]), run_time=1.2)
        self.play(VGroup(chap,cargo).animate.move_to([2.4,1.0,0]), run_time=1.1)
        self.play(VGroup(chap,cargo).animate.move_to([6.0,1.0,0]), run_time=1.1)
        secreted = label("secreted", [4.4,1.75,0], TEAL)
        self.play(FadeIn(secreted), run_time=.45)
        rule = label("Forward is the default", [0,3.18,0], TEXT,40)
        self.at("forward is the default")
        self.play(FadeIn(rule), w[0][8][1].animate.shift(RIGHT*.6), run_time=.8)
        held = VGroup(protein_blob([ER_X,.1,0],GOLD), label("held: not folded",[-4.25,1.75,0],GOLD,28))
        ret = CurvedArrow([-2.7,-1.75,0],[-4.75,-1.65,0],angle=-.3,color=TEAL,stroke_width=5)
        self.at("protein is held")
        self.play(FadeIn(held), FadeOut(secreted), FadeOut(VGroup(chap,cargo)), run_time=.55)
        self.at("fetched back")
        self.play(Create(ret), run_time=.55)
        self.at("sorted out")
        self.play(Indicate(w[0][6],color=GOLD), run_time=.55)
        self.finish()


class S12Fork(SpokenScene):
    def construct(self):
        # Same right-hand world, enlarged without changing landmark relationships.
        t = tgn().scale(1.45).move_to([-4.4,.2,0])
        mem = VGroup(Line([5.45,-3.0,0],[5.45,.45,0],color=BLUE,stroke_width=10),
                     Line([5.45,1.55,0],[5.45,3.0,0],color=BLUE,stroke_width=10))
        upper = VMobject(color=GREY,stroke_width=4).set_points_smoothly([[-3.7,.45,0],[-1.2,1.1,0],[2.0,1.0,0],[5.3,1.0,0]])
        lower = VMobject(color=GREY,stroke_width=4).set_points_smoothly([[-3.7,-.25,0],[-1.7,-1.4,0],[.3,-1.65,0]])
        shelfline = Line([-.2,-2.0,0],[4.8,-2.0,0],color=GREY,stroke_width=5)
        self.add(t,mem,upper,lower,shelfline)
        self.at("split the roots")
        self.play(Indicate(VGroup(upper,lower),color=TEXT), run_time=1.0)
        carriers = VGroup(*[Circle(radius=.33,color=SAND,fill_color=SAND,fill_opacity=.18).move_to([-3.2+.45*i,.65+.08*i,0]) for i in range(4)])
        self.at("Some carriers")
        self.play(LaggedStart(*[FadeIn(c,scale=.4) for c in carriers],lag_ratio=.12), run_time=.8)
        self.at("straight to the surface")
        self.play(carriers.animate.move_to([3.9,1.0,0]), run_time=1.7)
        door = label("constitutive: the door", [2.8,2.15,0], SAND)
        self.at("default door")
        self.play(FadeIn(door), carriers.animate.shift(RIGHT*2).set_opacity(0), run_time=.9)
        grans = VGroup(*[Circle(radius=.43,color=BLUE,fill_color=INK,fill_opacity=.85).move_to([.5+i*.82,-1.52,0]) for i in range(5)])
        fill = VGroup(*[VGroup(*[cargo_dot([.35+i*.82+.14*(j%3),-1.65+.17*(j//3),0],GOLD,.07) for j in range(6)]) for i in range(5)])
        self.at("digestive enzymes")
        self.play(LaggedStart(*[FadeIn(x) for x in fill],lag_ratio=.08), FadeIn(grans), run_time=1.2)
        regulated = label("regulated: the shelf", [2.1,-2.65,0], GOLD)
        self.at("regulated secretion")
        self.play(FadeIn(regulated), grans.animate.shift(RIGHT*.2), fill.animate.shift(RIGHT*.2), run_time=.8)
        self.at("wait on a shelf")
        self.play(VGroup(grans,fill).animate.shift(LEFT*.2), run_time=1.0)
        ring = Circle(radius=.35,color=TEXT,stroke_width=5).move_to([5.8,-.8,0])
        stim = label("stimulus", [3.8,.6,0], TEXT)
        self.at("a stimulus")
        self.play(FadeIn(stim), Create(ring), ring.animate.scale(3.5).set_opacity(0), run_time=1.0)
        self.play(VGroup(grans,fill).animate.move_to([4.5,-.45,0]), run_time=1.2)
        self.play(grans.animate.set_opacity(0), fill.animate.shift(RIGHT*.8).set_opacity(0), run_time=.8)
        q = label("Speed up the line?", [-1.1,2.8,0], TEXT,36)
        self.at("speed up the line")
        self.play(FadeIn(q), Indicate(t,color=TEXT), run_time=.8)
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        w = world(with_gel=False)
        self.add(w)
        q = label("Where are they?  Can they tell you?", [0,3.18,0], TEXT,34)
        self.add(q)
        self.at("hour later")
        self.play(ReplacementTransform(w[1][0], clock(60)), w[0][8][1].animate.shift(RIGHT*.6), run_time=.9)
        packed = VGroup(*[cargo_dot([2.65+.62*i,-1.13,0],GOLD,.19) for i in range(5)])
        tail = cargo_cloud([.2,-.1,0],1.1,8,GOLD).set_opacity(.35)
        grey = cargo_cloud([-2.7,.2,0],1.2,9,GREY)
        self.at("Mostly in storage")
        self.play(FadeIn(packed), FadeIn(tail), FadeIn(grey), run_time=1.0)
        tree = glycan_tree([3.0,-.1,0],.75,late=True)
        rec = label("enzymes met", [3.0,1.75,0],TEXT,28)
        self.at("sugar record")
        self.play(FadeIn(tree), FadeIn(rec), tail.animate.shift(RIGHT*.25), run_time=1.0)
        default = label("GOING ON", [-.5,2.2,0], GOLD,32)
        self.at("going on is")
        self.play(FadeIn(default), w[0][8][1].animate.shift(RIGHT*.65), run_time=.9)
        held = protein_blob([ER_X,.1,0],GOLD)
        ret = CurvedArrow([-2.7,-1.75,0],[-4.75,-1.65,0],angle=-.3,color=TEAL,stroke_width=5)
        self.at("Staying means")
        self.play(FadeIn(held), Create(ret), run_time=1.0)
        self.at("fetched back")
        self.play(Indicate(ret,color=TEAL), grey.animate.shift(RIGHT*.25), run_time=.75)
        self.at("Storing means")
        self.play(Indicate(w[0][6],color=GOLD), packed.animate.scale(1.12), run_time=.8)
        self.at("ways still argued")
        self.remove(q)
        self.play(packed.animate.scale(1/1.12), w[0][8][1].animate.shift(RIGHT*.55), run_time=.9)
        self.finish()


class S14End(EndCard):
    LINE = "Forward is the default unless cargo is held, retrieved, or sorted."
