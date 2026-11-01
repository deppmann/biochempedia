"""Reading a neuron's birth year  (Developmental Neuroscience explainer, adult neurogenesis)

COLOR MAP (one color per concept, whole film)
  ORANGE = carbon-14 (the atmospheric curve, the level written into DNA, the carbon-14 estimate)
  BLUE   = neurons (cells, nuclei)
  GREY   = structure, axes, other (non-neuronal) cells, cards
  YELLOW = the birth year marker
  PURPLE = the hippocampus (dentate gyrus outline)
  GREEN  = young neurons seen by a stain
  RED    = a lost marker / missing signal
  TEXT   = the rule and the average
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"


def level(y):
    if y < 1955:
        return 1.0
    if y <= 1963:
        return 1.0 + 0.9 * ((y - 1955) / 8.0) ** 1.6
    return 1.9 - 0.6 * (y - 1963) / 52.0   # schematic: a plain declining line


def make_axes(center, w, h):
    ax = Axes(x_range=[1935, 2015, 10], y_range=[0.0, 2.2, 0.5], x_length=w, y_length=h,
              axis_config={"include_tip": False, "include_numbers": False, "include_ticks": False,
                           "stroke_color": GREY, "stroke_width": 3})
    ax.move_to([center[0], center[1], 0])
    return ax


def year_label(ax, yr, color=GREY, size=22, drop=0.3):
    return M(str(yr), size, color).move_to(ax.c2p(yr, 0.0) + DOWN * drop)


def curve_pieces(ax):
    a = ax.plot(level, x_range=[1935, 1955], color=ORANGE, stroke_width=6)
    b = ax.plot(level, x_range=[1955, 1963], color=ORANGE, stroke_width=6)
    c = ax.plot(level, x_range=[1963, 2015], color=ORANGE, stroke_width=6)
    return a, b, c


def cell(r=0.8, color=BLUE, nuc=0.4):
    body = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.22)
    n = Circle(radius=r * nuc, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5)
    return VGroup(body, n)


def dna_bar(frac, w=1.8, h=0.3):
    out = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=GREY, stroke_width=3,
                           fill_color=BG, fill_opacity=1)
    fill = Rectangle(width=max(0.001, (w - 0.1) * frac), height=h - 0.1, stroke_width=0,
                     fill_color=ORANGE, fill_opacity=0.95)
    fill.move_to(out.get_left() + RIGHT * (0.05 + fill.width / 2))
    return VGroup(out, fill)


def arrow(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def dg_arc(r=1.9, color=PURPLE, n=14, scale_dots=0.13):
    """Dentate gyrus as a thick C-shaped arc with neurons (dots) along it. Returns (group, dots)."""
    arc = Arc(radius=r, start_angle=-0.2 * PI, angle=1.4 * PI, stroke_color=color, stroke_width=26)
    arc.set_stroke(opacity=0.35)
    dots = VGroup()
    for k in range(n):
        t = (k + 0.5) / n
        ang = -0.2 * PI + 1.4 * PI * t
        p = arc.get_arc_center() + r * np.array([np.cos(ang), np.sin(ang), 0])
        dots.add(Dot(p, radius=scale_dots, color=BLUE))
    return VGroup(arc, dots), dots


class S00Title(TitleCard):
    LESSON = "New neurons in the adult brain"
    TITLE = "New Neurons for Adult Circuits"


# Additional schematic helpers; original drawing helpers above are retained.
def neuron(r=0.55):
    c = cell(r)
    branches = VGroup()
    for angle in (0.3, 1.2, 2.2, 3.0):
        d = np.array([np.cos(angle), np.sin(angle), 0])
        tip = d * (r + 0.75)
        branches.add(Line(d * r, tip, color=BLUE, stroke_width=4))
        branches.add(Line(tip, tip + 0.4 * np.array([np.cos(angle + 0.6), np.sin(angle + 0.6), 0]), color=BLUE, stroke_width=3))
    axon = Line(DOWN * r, DOWN * (r + 1.0), color=BLUE, stroke_width=4)
    return VGroup(c, branches, axon)


def astro():
    rays = VGroup(*[Line(0.25 * np.array([np.cos(a), np.sin(a), 0]),
                         0.95 * np.array([np.cos(a), np.sin(a), 0]), color=GREY, stroke_width=5)
                    for a in np.linspace(0, TAU, 7, endpoint=False)])
    return VGroup(rays, cell(0.4, GREY))


def brain_outline():
    # Side view: olfactory bulb is anterior (left); small cerebellar lobe is posterior.
    return VGroup(Ellipse(width=8.4, height=4.4, color=GREY, stroke_width=4,
                         fill_color=GREY, fill_opacity=0.12),
                  Ellipse(width=1.35, height=1.0, color=GREY, fill_color=GREY,
                          fill_opacity=0.12).move_to([-4.4, -0.3, 0]),
                  Ellipse(width=1.6, height=1.3, color=GREY, fill_color=GREY,
                          fill_opacity=0.12).move_to([3.5, -1.25, 0]))


def mouse():
    return VGroup(Ellipse(width=1.2, height=0.6, color=GREY, fill_color=GREY, fill_opacity=0.3),
                  Circle(radius=0.28, color=GREY).move_to([0.6, 0.13, 0]),
                  Circle(radius=0.16, color=GREY).move_to([0.53, 0.43, 0]),
                  Dot([0.72, 0.18, 0], radius=0.04, color=TEXT),
                  Arc(radius=0.5, start_angle=PI / 2, angle=PI, color=GREY).move_to([-0.95, 0, 0]))


class S01TwoNiches(SpokenScene):
    def construct(self):
        brain = brain_outline().move_to([0, -0.2, 0])
        rule = T('Born with them. Keep them.', 34).move_to([0, 3.1, 0])
        self.at('For most of the last century')
        self.play(FadeIn(brain), FadeIn(rule), run_time=0.7)
        cross = Line(rule.get_left() + LEFT * 0.15, rule.get_right() + RIGHT * 0.15, color=RED, stroke_width=6)
        self.at('Adult rodents break')
        self.play(Create(cross), run_time=0.6)
        label = T('adult rodent · schematic', 24, GREY).move_to([0, -3.25, 0])
        self.at('All their lives')
        self.play(FadeOut(rule), FadeOut(cross), FadeIn(label), run_time=0.5)
        vent = Ellipse(width=1.6, height=0.8, color=GREY).move_to([-0.8, 0.6, 0])
        svz = Arc(radius=0.8, start_angle=0.1 * PI, angle=0.8 * PI, color=BLUE, stroke_width=9).stretch(0.5, 1).move_to(vent.get_top())
        sl = T('ventricle wall / SVZ', 26, BLUE).move_to([-2.6, 2.55, 0])
        self.at('One is a thin layer')
        self.play(Create(vent), Create(svz), FadeIn(sl), run_time=0.8)
        bulb = Circle(radius=0.4, color=BLUE).move_to([-4.25, -0.35, 0])
        bl = T('olfactory bulb', 26, BLUE).move_to([-4.3, -1.7, 0])
        path = CubicBezier([-1.3, 0.8, 0], [-2.0, 0.3, 0], [-3.0, -0.4, 0], bulb.get_center())
        dots = VGroup(*[Dot(path.point_from_proportion(t), radius=0.11, color=BLUE) for t in (0, 0.14, 0.28)])
        self.at('Its young neurons travel')
        self.play(FadeIn(bulb), FadeIn(bl), FadeIn(dots), run_time=0.4)
        self.play(*[MoveAlongPath(d, path.get_subcurve(t, t + 0.72), rate_func=linear) for d, t in zip(dots, (0, 0.14, 0.28))], run_time=1.8)
        self.remove(dots)
        self.add(VGroup(*[Dot(bulb.get_center() + [dx, dy, 0], radius=0.09, color=BLUE) for dx, dy in [(-0.15, 0), (0.1, 0.15), (0.1, -0.15)]]))
        dg, dd = dg_arc(0.85, n=3, scale_dots=0.12)
        dg.move_to([1.8, -0.45, 0])
        dl = T('dentate gyrus', 26, PURPLE).move_to([3.5, 2.55, 0])
        self.at('The other is the dentate gyrus')
        self.play(FadeIn(dg[0]), FadeIn(dl), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dd], lag_ratio=0.3), run_time=0.9)
        wires = VGroup(Line(bulb.get_center(), [-3.45, -0.75, 0], color=BLUE),
                       Line(dd[0].get_center(), [2.9, -1.3, 0], color=BLUE))
        self.at('In both places')
        self.play(Create(wires), Indicate(VGroup(bulb, dd), color=BLUE, scale_factor=1.12), run_time=0.9)
        self.finish()


class S02StemCells(SpokenScene):
    def construct(self):
        wall = Line([-6.1, -2.3, 0], [-6.1, 2.3, 0], color=GREY, stroke_width=12)
        head = T('subventricular zone · mouse', 30).move_to([0, 3.1, 0])
        b = astro().move_to([-3.7, 0.3, 0])
        c = cell(0.65, GREY).move_to([0, 0.3, 0])
        a = neuron(0.4).move_to([3.6, 0.3, 0])
        labels = VGroup(T('B · astrocyte-like', 25, GREY).move_to([-3.7, -1.9, 0]),
                        T('C · precursor', 25, GREY).move_to([0, -1.9, 0]),
                        T('A · young neuron', 25, BLUE).move_to([3.6, -1.9, 0]))
        self.at('Which cell makes them')
        self.play(FadeIn(head), Create(wall), FadeIn(b), FadeIn(c), FadeIn(a), FadeIn(labels), run_time=0.7)
        drug = bchip('drug', RED, 28).move_to([1.8, 1.95, 0])
        self.at('a drug killed')
        self.play(FadeIn(drug), c.animate.set_color(RED), a.animate.set_color(RED), run_time=0.45)
        self.play(FadeOut(c), FadeOut(a), run_time=0.65)
        self.at('Cells that look like astrocytes survived')
        self.play(Indicate(b, color=TEXT, scale_factor=1.1), FadeOut(drug), run_time=0.8)
        daughter = b.copy().scale(0.7).move_to([-2.1, 1.35, 0])
        self.at('They began dividing')
        self.play(TransformFromCopy(b, daughter), run_time=0.7)
        self.at('rebuilt the zone')
        c.set_color(GREY)
        a.set_color(BLUE)
        self.play(TransformFromCopy(daughter, c), FadeIn(a), FadeOut(daughter), run_time=0.7)
        self.at('So the stem cell')
        self.play(Indicate(b, color=GREY, scale_factor=1.1), run_time=0.6)
        bc = arrow([-2.55, 0.3, 0], [-0.85, 0.3, 0])
        ca = arrow([0.85, 0.3, 0], [2.3, 0.3, 0], BLUE)
        self.at('It makes fast dividing precursors')
        self.play(GrowArrow(bc), run_time=0.6)
        self.at('which make young neurons')
        self.play(GrowArrow(ca), run_time=0.6)
        self.at('that migrate')
        self.play(a.animate.shift(RIGHT * 0.65), run_time=0.6)
        dest = T('→ olfactory bulb interneuron', 25, BLUE).move_to([2.4, -3.05, 0])
        self.play(FadeIn(dest), run_time=0.3)
        foot = T('dentate stem cells: astrocyte-like too', 26, PURPLE).move_to([0, 2.25, 0])
        self.at('The dentate gyrus has')
        self.play(FadeIn(foot), run_time=0.6)
        self.finish()


class S03HowWeKnow(SpokenScene):
    def construct(self):
        left = cell(1.05).move_to([-3.3, 0.3, 0])
        right = neuron(0.7).move_to([3.1, 0.4, 0])
        labs = VGroup(T('copying DNA', 28, BLUE).move_to([-3.3, 2.65, 0]),
                      T('resting neuron', 28, BLUE).move_to([3.1, 2.65, 0]))
        self.at('How can anyone tell')
        self.play(FadeIn(left), FadeIn(right), FadeIn(labs), run_time=0.7)
        dose = bchip('labelled DNA building block', YELLOW, 28).move_to([0, -2.9, 0])
        self.at('Give a labeled DNA building block')
        self.play(FadeIn(dose), run_time=0.5)
        badge = Dot(dose.get_center(), radius=0.17, color=YELLOW)
        self.at('Only cells copying')
        self.add(badge)
        self.play(badge.animate.move_to(left[1]), left[1].animate.set_fill(YELLOW, 0.85).set_stroke(YELLOW), run_time=1.0)
        self.remove(badge)
        self.at('A neuron that has stopped dividing')
        self.play(Indicate(right, color=BLUE, scale_factor=1.07), run_time=0.6)
        no = T('no label incorporated', 26, GREY).move_to([3.1, -1.9, 0])
        self.at('does not copy its DNA again')
        self.play(FadeIn(no), run_time=0.6)
        later = neuron(0.8).move_to([-2.0, 0.2, 0])
        later[0][1].set_fill(YELLOW, 0.85).set_stroke(YELLOW)
        weeks = T('weeks later', 30).move_to([0, 3.0, 0])
        self.at('So a labeled neuron found weeks later')
        self.play(FadeOut(right), FadeOut(labs), FadeOut(no), FadeOut(dose),
                  ReplacementTransform(left, later), FadeIn(weeks), run_time=0.9)
        inference = T('likely descended from\na dividing cell', 30, YELLOW).move_to([3.1, 0.5, 0])
        self.at('most likely came from')
        self.play(FadeIn(inference), run_time=0.6)
        stain = Circle(radius=0.86, color=GREEN, stroke_width=8).move_to(later[0])
        key = T('second stain: neuron', 28, GREEN).move_to([1.9, -2.5, 0])
        self.at('A second stain')
        self.play(Create(stain), FadeIn(key), run_time=0.8)
        self.finish()


class S04WiringIn(SpokenScene):
    def construct(self):
        dg, dots = dg_arc(1.6, n=3)
        dg.move_to([-3.3, -0.1, 0])
        soma = cell(0.45).move_to([-2.5, -0.5, 0])
        title = T('dentate gyrus', 28, PURPLE).move_to([-3.3, 3.0, 0])
        self.at('A new neuron matters')
        self.play(FadeIn(dg), FadeIn(soma), FadeIn(title), run_time=0.6)
        clock = VGroup(Circle(radius=0.45, color=GREY), Line(ORIGIN, UP * 0.35, color=TEXT)).move_to([0.3, 2.3, 0])
        weeks = T('weeks', 26, GREY).move_to([1.55, 2.3, 0])
        self.at('Over several weeks')
        self.play(FadeIn(clock), FadeIn(weeks), run_time=0.3)
        self.play(Rotate(clock[1], angle=TAU, about_point=clock[0].get_center()), run_time=0.7)
        dendrites = VGroup(*[Line(soma.get_top(), soma.get_top() + [dx, 1.4, 0], color=BLUE, stroke_width=4) for dx in (-0.9, 0, 0.9)])
        self.at('grow dendrites')
        self.play(Create(dendrites), run_time=0.8)
        target = neuron(0.55).move_to([4.0, 0.2, 0])
        axon = CubicBezier(soma.get_bottom(), [-1.4, -2.4, 0], [1.5, -2.4, 0], target[0].get_left(), color=BLUE, stroke_width=5)
        tl = T('hippocampal circuit', 27, BLUE).move_to([3.8, -2.6, 0])
        self.at('send axons')
        self.play(Create(axon), FadeIn(target), FadeIn(tl), run_time=1.1)
        bird = VGroup(Ellipse(width=1.7, height=1.1, color=YELLOW),
                      Circle(radius=0.45, color=YELLOW).move_to([0.65, 0.55, 0]),
                      Polygon([1.05, 0.65, 0], [1.45, 0.5, 0], [1.05, 0.4, 0], color=YELLOW),
                      Dot([0.75, 0.68, 0], radius=0.05, color=TEXT),
                      Line([-0.9, 0, 0], [-1.45, -0.45, 0], color=YELLOW)).move_to([-4.2, -0.2, 0])
        soundcell = neuron(0.65).move_to([3.3, 0.1, 0])
        self.at('In adult canaries')
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(bird),
                  FadeIn(T('adult canary', 30).move_to([-4, 2.8, 0])), run_time=0.6)
        self.at('new neurons in a song nucleus')
        self.play(FadeIn(soundcell), FadeIn(T('new neuron · song nucleus', 26, BLUE).move_to([3, 2.8, 0])), run_time=0.7)
        waves = VGroup(*[Arc(radius=r, start_angle=-PI/4, angle=PI/2, color=TEXT).move_to([-0.7 + 0.5*i, 0.1, 0]) for i, r in enumerate((0.5, 0.8, 1.1))])
        self.at('respond to sound')
        self.play(Create(waves), Indicate(soundcell, color=BLUE, scale_factor=1.15), run_time=0.9)
        self.finish()


class S05WhatFor(SpokenScene):
    def construct(self):
        head = T('What might new neurons do?', 34).move_to([0, 3.1, 0])
        self.at('What are they for')
        self.play(FadeIn(head), run_time=0.6)
        rooms = VGroup()
        for x in (-2.0, 2.0):
            room = VGroup(Rectangle(width=2.8, height=2.5, color=GREY),
                          Square(side_length=0.55, color=TEXT).move_to([0.65, 0.45, 0]),
                          Dot([-0.6, -0.5, 0], color=BLUE, radius=0.17))
            rooms.add(room.move_to([x, 0.6, 0]))
        rooms[1][2].shift(RIGHT * 0.3)
        self.at('In mice young dentate neurons')
        self.play(FadeIn(rooms), run_time=0.7)
        hyp = T('thought to help: pattern separation', 28, PURPLE).move_to([0, -2.5, 0])
        self.at('pattern separation')
        self.play(FadeIn(hyp), run_time=0.6)
        animal = mouse().move_to([0, -1.45, 0])
        self.at('telling apart similar places')
        self.play(rooms[0].animate.shift(LEFT * 1.5), rooms[1].animate.shift(RIGHT * 1.5), FadeIn(animal), run_time=0.8)
        self.play(animal.animate.shift(LEFT * 2.8), run_time=0.6)
        blocked = T('adult neurogenesis blocked', 30, RED).move_to([0, 3.1, 0])
        self.at('Mice in which adult neurogenesis was blocked')
        self.play(ReplacementTransform(head, blocked), FadeOut(animal), FadeOut(hyp), run_time=0.7)
        self.at('did worse at telling apart')
        unsure = T('nearby locations: harder to distinguish', 28, TEXT).move_to([0, -2.5, 0])
        self.play(rooms[0].animate.shift(RIGHT * 1.5), rooms[1].animate.shift(LEFT * 1.5), FadeIn(unsure), run_time=0.7)
        bulb = Circle(radius=1.6, color=GREY).move_to([2.8, 0, 0])
        new = VGroup(*[cell(0.3).move_to([2.2 + i*0.6, 0.2 if i%2 else -0.3, 0]) for i in range(3)])
        cloud = VGroup(*[Circle(radius=r, color=GREY, fill_color=GREY, fill_opacity=0.15).move_to([-3.6+dx, dy, 0]) for r, dx, dy in [(0.6,0,0),(0.5,0.7,0.4),(0.55,0.7,-0.4)]])
        ol = T('olfactory bulb', 30, BLUE).move_to([2.8, 2.5, 0])
        self.at('In the olfactory bulb')
        self.play(FadeOut(rooms), FadeOut(blocked), FadeOut(unsure), FadeIn(bulb), FadeIn(ol), run_time=0.6)
        self.at('new interneurons')
        self.play(FadeIn(new), run_time=0.5)
        self.at('linked to odor learning')
        link = DashedLine([-2,0,0], [0.8,0,0], color=GREY)
        self.play(FadeIn(cloud), Create(link), run_time=0.7)
        output = T('niche signals + experience → output', 30).move_to([0, -2.9, 0])
        self.at('Signals in the niche')
        self.play(FadeIn(output), run_time=0.6)
        wheel = VGroup(Circle(radius=1.65, color=GREY), *[Line(ORIGIN, 1.65*np.array([np.cos(a), np.sin(a), 0]), color=GREY) for a in np.linspace(0, TAU, 6, endpoint=False)]).move_to([-3.3, 0.2, 0])
        runner = mouse().move_to([-3.3, -0.5, 0])
        dg, dots = dg_arc(1.55, n=3)
        dg.move_to([3.2, 0.1, 0])
        self.at('Mice with a running wheel')
        self.play(*[FadeOut(m) for m in (bulb, ol, new, cloud, link, output)], FadeIn(wheel), FadeIn(runner), FadeIn(dg), run_time=0.6)
        self.play(Rotate(wheel, PI/3), run_time=0.6)
        extra = VGroup(*[Dot(dg[0].get_arc_center() + 1.55*np.array([np.cos(a),np.sin(a),0]), radius=0.14, color=BLUE) for a in (-0.3,0.6,1.6)])
        self.at('had more new dentate neurons')
        self.play(FadeIn(extra, scale=0.4), FadeIn(T('more new dentate neurons', 28, BLUE).move_to([2.9, -2.6, 0])), run_time=0.7)
        self.finish()


class S06Humans(SpokenScene):
    def construct(self):
        head = T('What about people?', 34).move_to([0, 3.1, 0])
        self.at('What about people')
        self.play(FadeIn(head), run_time=0.6)
        ax = make_axes([-2.2, 0], 6.5, 3.5)
        curves = VGroup(*curve_pieces(ax))
        al = T('air carbon-14 · schematic', 25, ORANGE).move_to([-2.2, 2.3, 0])
        yrs = VGroup(year_label(ax, 1955), year_label(ax, 1963, drop=0.8), year_label(ax, 2015))
        self.at('Bomb tests')
        self.play(Create(ax), FadeIn(al), FadeIn(yrs), run_time=0.6)
        self.at('put extra carbon')
        self.play(Create(curves), run_time=1.3)
        c = cell(0.8).move_to([4.4, 0.8, 0])
        dna = dna_bar(0.0, 2.0, 0.4).move_to([4.4, -0.6, 0])
        dl = T('DNA · year made', 25, ORANGE).move_to([4.3, -1.5, 0])
        mark = Dot(ax.c2p(1975, level(1975)), radius=0.12, color=YELLOW)
        self.at('and into the DNA')
        self.play(FadeIn(c), FadeIn(dna), FadeIn(dl), FadeIn(mark), run_time=0.5)
        self.play(Transform(dna, dna_bar(0.7, 2.0, 0.4).move_to(dna)), run_time=0.7)
        brain = brain_outline().scale(0.7).move_to([-2.4, 0, 0])
        birth = VGroup(bchip('cortex: birth year', YELLOW, 26).move_to([3.1, 1.4, 0]),
                       bchip('olfactory bulb:\nbirth year', YELLOW, 26).move_to([-4.6, 1.95, 0]))
        cortex = Arc(radius=1.0, start_angle=-PI/3, angle=2*PI/3, color=BLUE, stroke_width=9).move_to([-0.1, 0.3, 0])
        cortex_leader = Line(birth[0].get_left(), cortex.get_right(), buff=0.12,
                             color=YELLOW, stroke_width=3)
        self.at('Neurons at the back of the cortex')
        self.play(*[FadeOut(m) for m in (head, ax, curves, al, yrs, c, dna, dl, mark)], FadeIn(brain), Create(cortex), FadeIn(birth[0]), Create(cortex_leader), run_time=0.7)
        bulb = Dot([-5.35, -0.2, 0], radius=0.2, color=BLUE)
        bulb_leader = Line(birth[1].get_bottom(), bulb.get_top(), buff=0.12,
                           color=YELLOW, stroke_width=3)
        self.at('and in the olfactory bulb')
        self.play(FadeIn(bulb), FadeIn(birth[1]), Create(bulb_leader), run_time=0.6)
        hip, _ = dg_arc(0.65, n=3, scale_dots=0.1)
        hip.move_to([-1.7, -0.4, 0])
        later = bchip('hippocampus: some later', PURPLE, 26).move_to([-1.7, -2.6, 0])
        hip_leader = Line(later.get_top(), hip[0].point_from_proportion(0.95), buff=0.12,
                          color=PURPLE, stroke_width=3)
        self.at('Some hippocampal neurons are younger')
        self.play(FadeIn(hip), FadeIn(later), Create(hip_leader), run_time=0.7)
        panels = VGroup()
        signals = []
        for x in (-3.3, 3.3):
            box = RoundedRectangle(width=4.5, height=3.5, corner_radius=0.2, color=GREY).move_to([x, 0, 0])
            d = VGroup(*[Dot([x + dx, dy, 0], radius=0.2, color=GREEN) for dx, dy in [(-1,0.6),(0,0),(1,0.6),(-0.5,-0.7),(0.7,-0.7)]])
            panels.add(VGroup(box, d)); signals.append(d)
        self.at('Stains for young neurons disagree')
        self.play(*[FadeOut(m) for m in (brain, cortex, birth, bulb, hip, later, cortex_leader, bulb_leader, hip_leader)], FadeIn(panels),
                  FadeIn(T('young-neuron stains · schematic', 30, GREEN).move_to([0, 2.8, 0])), run_time=0.7)
        fade = T('time after death', 28, GREY).move_to([3.3, -2.5, 0])
        self.at('partly because the stain fades')
        self.play(signals[1].animate.set_opacity(0.12), FadeIn(fade), run_time=1.2)
        dg, _ = dg_arc(1.65, n=4)
        dg.move_to([-3.0, 0.2, 0])
        conclusion = T('several methods favour\nsome new neurons', 32).move_to([2.5, 1.0, 0])
        self.at('Recent reviews')
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(dg), FadeIn(conclusion), run_time=0.7)
        self.at('How many and what they do')
        q = T('?', 110, YELLOW).move_to([2.5, -0.8, 0])
        openq = T('number and function: still open', 28, YELLOW).move_to([0, -2.9, 0])
        self.play(FadeIn(q), FadeIn(openq), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Adult rodents make new neurons that join working circuits."
