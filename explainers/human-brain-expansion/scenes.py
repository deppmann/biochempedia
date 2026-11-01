"""Human brain expansion: more columns, not a thicker cortex  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = classical radial glia / founder progenitors (the units)
  YELLOW = neurons, and the columns they stack into
  GREEN  = area: the number of units, symmetric (doubling) divisions
  PURPLE = thickness: neurons per unit, asymmetric (adding) divisions
  PINK   = outer radial glia
  ORANGE = a gene or protein that is added, changed or removed
  RED    = not tested / no contact / missing
  GREY   = ventricle, brain surface, labels, de-emphasized
  GOLD   = the question mark and the final rule
"""


import numpy as np


from bp_style import *


PURPLE = "#B58CD9"


ORANGE = "#F29E4C"


PINK = "#E58BB8"


def btext(text, size=24, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.12, stroke_width=0, fill_color=BG,
                     fill_opacity=1).move_to(t)
    return VGroup(back, t)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.04, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def darr(a, b, color=GREY, w=5, tip=0.2):
    return DoubleArrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                       max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bar(x0, x1, y, color=GREY, h=0.24):
    return RoundedRectangle(corner_radius=0.08, width=x1 - x0, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def dot(x, y, color, r=0.16):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.9).move_to([x, y, 0])


def sq(x, bottom, side, color):
    return Rectangle(width=side, height=side, stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=0.3).move_to([x, bottom + side / 2, 0])


class S00Title(TitleCard):
    LESSON = "What makes the human brain big"
    TITLE = "More Progenitors, More Cortical Area"


UX = [-4.5 + 1.8 * i for i in range(6)]


VEN_Y = -2.7


def unit_parts(x):
    patch = Ellipse(width=0.9, height=0.32, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                    fill_opacity=0.5).move_to([x, -2.42, 0])
    fibre = Line([x, -2.26, 0], [x, 2.55, 0], color=BLUE, stroke_width=3).set_opacity(0.55)
    return patch, fibre


def column_rect(x):
    return RoundedRectangle(corner_radius=0.12, width=0.62, height=2.1, stroke_color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=0.12).move_to([x, 1.4, 0])


STACK_Y = [0.7, 1.15, 1.6, 2.05]


LX, RX = -3.2, 3.3


BY = -1.75


COL_B, COL_H = -1.3, 2.7


def founders(cx, n, span=5.6):
    """n founder circles plus n columns, spread over `span` centred at cx."""
    sp = span / n if n > 1 else 0
    g = VGroup()
    for i in range(n):
        x = cx + (i - (n - 1) / 2) * sp
        w = min(0.5, sp * 0.72) if n > 1 else 0.5
        c = dot(x, BY + 0.25, BLUE, r=0.17)
        r = Rectangle(width=w, height=COL_H, stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW,
                      fill_opacity=0.18).move_to([x, COL_B + COL_H / 2, 0])
        g.add(c, r)
    return g


def blob(a, b, eps, cx=0.0, cy=0.0):
    return ParametricFunction(
        lambda th: np.array([cx + a * (1 + eps * np.sin(11 * th)) * np.cos(th),
                             cy + b * (1 + eps * np.sin(11 * th)) * np.sin(th), 0]),
        t_range=[0, TAU, 0.02], stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.14)


def ring_dots(cx, cy, a, b, n, color=BLUE, r=0.1):
    g = VGroup()
    for k in range(n):
        th = TAU * k / n
        g.add(dot(cx + 0.78 * a * np.cos(th), cy + 0.78 * b * np.sin(th), color, r=r))
    return g


class S07End(EndCard):
    LINE = "More progenitors, more cortical area"

    def construct(self):
        line = T(self.LINE, 40, GOLD, font=TITLE_FONT).move_to([0, 2.9, 0])
        fit(line, max_w=12)
        surface = Line([-5.5, 1.8, 0], [5.5, 1.8, 0], color=GREY)
        parent = org_cell(-4, 0, top=1.8)
        ip = dot(0, 0, BLUE, .26)
        neurons = VGroup(dot(3.6, .2, YELLOW), dot(4.4, .2, YELLOW))
        labels = VGroup(T('outer radial glia', 24, PINK).move_to([-4, -.85, 0]),
                        T('intermediate progenitor', 24, BLUE).move_to([0, -.85, 0]),
                        T('neurons', 24, YELLOW).move_to([4, -.85, 0]))
        links = VGroup(arr([-3.5, 0, 0], [-.5, 0, 0], BLUE),
                       arr([.5, 0, 0], [3.1, 0, 0], YELLOW))
        sub = T('biochemistrypedia.com', 22, TEAL).move_to([0, -2.7, 0])
        self.play(FadeIn(line), FadeIn(VGroup(surface, parent, ip, neurons, labels, links)),
                  FadeIn(sub), run_time=self.beat(.3))
        self.finish()

# Intermediate progenitors use blue; outer radial glia retain pink.
# All tissues, cells and scaling relationships below are schematic.
def heading(text, color=TEXT):
    return T(text, 30, color, font=TITLE_FONT).move_to([0, 3.25, 0])


def org_cell(x, y, topx=None, top=2.35):
    """Classic outer radial glial example: basal fibre, no apical process."""
    if topx is None:
        topx = x
    return VGroup(Line([x, y + .24, 0], [topx, top, 0], color=PINK, stroke_width=3),
                  dot(x, y, PINK, .24))


def outer_stage():
    surface = VGroup(Line([-6, 2.35, 0], [6, 2.35, 0], color=GREY),
                     T('brain surface', 22, GREY).move_to([4.7, 2.7, 0]))
    ventricle = VGroup(bar(-6, 6, -2.55), T('ventricle', 24, GREY).move_to([4.9, -3.05, 0]))
    zone = VGroup(Rectangle(width=12, height=2.3, stroke_width=0, fill_color=PINK,
                           fill_opacity=.055).move_to([0, -.2, 0]),
                  btext('outer subventricular zone', 24, PINK).move_to([-3.5, 1.55, 0]).set_z_index(3))
    return VGroup(surface, ventricle, zone)


class S01Puzzle(SpokenScene):
    def construct(self):
        title = heading('A sheet that grows in area')
        thick = VGroup(T('wall thickness', 28, PURPLE).move_to([-3.3, 2.4, 0]),
                       Rectangle(width=.9, height=1, color=PURPLE, fill_opacity=.3).move_to([-4.3, .1, 0]),
                       Rectangle(width=.9, height=2, color=PURPLE, fill_opacity=.3).move_to([-2.3, .6, 0]),
                       T('mouse', 24, GREY).move_to([-4.3, -.8, 0]),
                       T('human', 24, GREY).move_to([-2.3, -.8, 0]))
        ratio = T('about twice the thickness', 26, PURPLE).move_to([-3.3, -1.6, 0])
        area = VGroup(T('surface area', 28, GREEN).move_to([3.3, 2.4, 0]),
                      sq(1.7, -.4, .5, GREEN), sq(4.4, -.4, 2.3, GREEN),
                      T('mouse', 24, GREY).move_to([1.7, -.8, 0]),
                      T('human', 24, GREY).move_to([4.4, -.8, 0]))
        area_ratio = T('roughly 1,000× the area', 26, GREEN).move_to([3.3, -1.6, 0])
        note = T('schematic sheets • not to scale', 22, GREY).move_to([0, -2.65, 0])
        self.at('Your cortex')
        self.play(FadeIn(title), FadeIn(thick), FadeIn(note), run_time=.65)
        self.at('twice as thick')
        self.play(FadeIn(ratio), run_time=.5)
        self.at('its surface')
        self.play(FadeIn(area), run_time=.6)
        self.at('a thousand times larger')
        self.play(FadeIn(area_ratio), run_time=.6)
        self.at('A leading explanation')
        stage = outer_stage()
        stage[0][0].put_start_and_end_on([-4, 2.35, 0], [4, 2.35, 0])
        stage[0][1].move_to([4.7, 2.85, 0])
        stage[2][1].become(btext('outer subventricular\nzone', 22, PINK).move_to([-5, 1.1, 0]))
        head = heading('A leading explanation', GOLD)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(stage), FadeIn(head), run_time=.65)
        parent = org_cell(-3, -.35)
        parent_label = T('outer radial glia', 24, PINK).move_to([-3, -1.2, 0])
        self.at('Outer radial glia')
        self.play(FadeIn(parent), FadeIn(parent_label), run_time=.5)
        self.at('renew themselves')
        renewed = org_cell(-1.2, -.35)
        self.play(TransformFromCopy(parent, renewed), run_time=.65)
        self.at('Their daughters can become')
        ip = VGroup(dot(1.3, -.35, BLUE, .26), T('intermediate\nprogenitor', 24, BLUE).move_to([1.3, -1.25, 0]))
        link = arr([-.75, -.35, 0], [.9, -.35, 0], BLUE)
        self.play(TransformFromCopy(renewed[1], ip[0]), FadeIn(ip[1]), GrowArrow(link), run_time=.7)
        self.at('divide into neurons')
        neurons = VGroup(dot(3.7, -.05, YELLOW), dot(4.5, -.05, YELLOW),
                         T('neurons', 24, YELLOW).move_to([4.1, -.8, 0]))
        self.play(FadeOut(link), TransformFromCopy(ip[0], neurons[:2]), FadeIn(neurons[2]), run_time=.75)
        self.at('amplify neuron production')
        self.play(Indicate(neurons, color=YELLOW, scale_factor=1.1), run_time=.65)
        self.at('a larger cortical sheet')
        sheet = bar(-6, 6, 2.35, GREEN, .35)
        self.play(Transform(stage[0][0], sheet), neurons[:2].animate.move_to([3.5, 1.8, 0]), run_time=.9)
        self.finish()


class S05Orgs(SpokenScene):
    def construct(self):
        stage = outer_stage()
        head = heading('Living human fetal cortical slice')
        parent = org_cell(-3, -.35)
        self.at('In living slices')
        self.play(FadeIn(stage), FadeIn(head), FadeIn(parent), run_time=.65)
        self.at('filmed these cells dividing')
        daughter = org_cell(-1.6, -.35)
        self.play(TransformFromCopy(parent, daughter), parent.animate.shift(LEFT * .5), run_time=.7)
        classic = T('classic example', 24, PINK).move_to([-3.5, -.95, 0])
        self.at('The classic outer')
        self.play(FadeOut(daughter), FadeIn(classic), run_time=.5)
        self.at('keeps a fiber')
        self.play(Indicate(parent[0], color=PINK, scale_factor=1.03), run_time=.65)
        gap = DashedLine([-3.5, -1.2, 0], [-3.5, -2.3, 0], color=RED)
        no = T('no ventricular contact', 24, RED).move_to([0, -2, 0])
        self.at('no contact with the ventricle')
        self.play(Create(gap), FadeIn(no), run_time=.6)
        self.at('Daughters could divide again')
        renewed = org_cell(-1.5, -.35)
        self.play(FadeOut(gap), FadeOut(no), FadeOut(classic), TransformFromCopy(parent, renewed), run_time=.7)
        self.at('or become intermediate progenitors')
        ip = VGroup(dot(1.2, -.35, BLUE, .25), T('intermediate\nprogenitor', 24, BLUE).move_to([1.2, -1.25, 0]))
        neurons = VGroup(dot(3.5, .1, YELLOW), dot(4.3, .1, YELLOW))
        self.play(TransformFromCopy(renewed[1], ip[0]), FadeIn(ip[1]), run_time=.5)
        self.play(TransformFromCopy(ip[0], neurons), run_time=.5)
        self.at('abundant in primates and ferret')
        abundance = T('primates + ferret: abundant', 26, PINK).move_to([0, -3.1, 0])
        self.play(FadeOut(stage[1][1]), FadeIn(abundance), run_time=.5)
        self.at('rare in mouse')
        abundance2 = T('primates + ferret: abundant   •   mouse: rare', 26, PINK).move_to([0, -3.1, 0])
        self.play(ReplacementTransform(abundance, abundance2), run_time=.5)
        self.at('Their fibers fan')
        fan = VGroup(org_cell(-3.5, -.35, -5.1), org_cell(-1.5, -.35, -.3), org_cell(.5, -.35, 3))
        self.play(FadeOut(ip), FadeOut(neurons), ReplacementTransform(VGroup(parent, renewed), fan), run_time=.8)
        self.at('growth in area')
        wide = darr([-5.2, 1.9, 0], [3.2, 1.9, 0], GREEN)
        self.play(GrowFromCenter(wide), run_time=.6)
        self.at('The nearly smooth marmoset')
        marmoset = VGroup(blob(1.3, .65, 0, 3.7, -.8),
                          T('marmoset • nearly smooth', 22, TEXT).move_to([3.7, -1.85, 0]))
        self.play(FadeIn(marmoset), run_time=.65)
        self.at('do not guarantee folding')
        caveat = T('outer radial glia do not guarantee folding', 28, GOLD).move_to([0, -3.1, 0])
        self.play(ReplacementTransform(abundance2, caveat), run_time=.6)
        self.finish()


class S02Unit(SpokenScene):
    def construct(self):
        head = heading('Early founders at the ventricle')
        ven = VGroup(bar(-6, 6, VEN_Y), T('ventricle', 24, GREY).move_to([4.8, -3.2, 0]))
        units = VGroup(*[VGroup(*unit_parts(x)) for x in (-3.6, 0, 3.6)])
        self.at('Early founders')
        self.play(FadeIn(head), FadeIn(ven), FadeIn(VGroup(*[u[0] for u in units])), run_time=.65)
        newhead = heading('Radial unit hypothesis')
        source = T('Pasko Rakic • fetal rhesus monkey work', 24, GREY).move_to([0, -3.2, 0])
        self.at('the radial unit hypothesis')
        self.play(ReplacementTransform(head, newhead), ReplacementTransform(ven[1], source), run_time=.6)
        self.at('In this simplified model')
        model = btext('simplified model', 24, GOLD).move_to([4.9, -1.7, 0]).set_z_index(3)
        self.play(FadeIn(model), run_time=.4)
        cols = VGroup(*[VGroup(column_rect(x), *[dot(x, y, YELLOW) for y in STACK_Y]) for x in (-3.6, 0, 3.6)])
        self.at('each patch of progenitors')
        self.play(*[Create(u[1]) for u in units], run_time=.5)
        self.at('makes a column')
        self.play(FadeIn(cols, shift=UP * .35), run_time=.65)
        area = VGroup(darr([-4.2, 2.8, 0], [4.2, 2.8, 0], GREEN), btext('area', 26, GREEN).move_to([0, 2.8, 0]))
        self.at('number of units sets area')
        self.play(FadeIn(area), run_time=.6)
        thickness = VGroup(darr([-4.65, .4, 0], [-4.65, 2.4, 0], PURPLE),
                           T('thickness', 24, PURPLE).rotate(PI/2).move_to([-5.3, 1.4, 0]))
        self.at('neuron output sets thickness')
        self.play(FadeIn(thickness), run_time=.6)
        self.at('spread sideways')
        self.play(cols[1][2].animate.shift(LEFT * .8), cols[1][3].animate.shift(RIGHT * .8), run_time=.8)
        self.finish()


class S03Arithmetic(SpokenScene):
    def construct(self):
        head = heading('Arithmetic in the simplified radial-unit model', GOLD)
        left_title = T('symmetric founders', 26, GREEN).move_to([LX, 2.5, 0])
        right_title = T('direct asymmetric divisions', 26, PURPLE).move_to([RX, 2.5, 0])
        cur = founders(LX, 1)
        self.at('While founders divide symmetrically')
        self.play(FadeIn(head), FadeIn(left_title), FadeIn(cur), run_time=.65)
        self.at('the pool doubles each round')
        eq = M('1', 30, GREEN).move_to([LX, -2.4, 0])
        self.play(FadeIn(eq), run_time=.4)
        self.at('three extra rounds give')
        for n in (2, 4, 8):
            nxt = founders(LX, n)
            neweq = M(' → '.join(map(str, (1, 2, 4, 8)[:(1, 2, 4, 8).index(n)+1])), 30, GREEN).move_to(eq)
            self.play(ReplacementTransform(cur, nxt), ReplacementTransform(eq, neweq), run_time=.38)
            cur, eq = nxt, neweq
        self.at('eight times as many units')
        self.play(Indicate(cur, color=GREEN, scale_factor=1.03), run_time=.5)
        self.at('Three extra direct asymmetric divisions')
        right = founders(RX, 1)
        right[1].stretch_to_fit_height(1.5).move_to([RX, COL_B + .75, 0])
        self.play(FadeIn(right_title), FadeIn(right), run_time=.55)
        extra = VGroup(*[dot(RX, .45 + i * .4, YELLOW, .14) for i in range(3)])
        result = T('+3 neurons per column', 26, PURPLE).move_to([RX, -2.4, 0])
        self.at('add just three neurons')
        self.play(LaggedStart(*[FadeIn(d, shift=UP*.3) for d in extra], lag_ratio=.3), FadeIn(result), run_time=.9)
        self.at('In mice')
        tag = heading('Mouse progenitors: stabilized β-catenin', ORANGE)
        normal = blob(1.8, 1.25, 0, -3.2, -.05)
        changed = blob(1.8, 1.25, 0, 3.2, -.05)
        labels = VGroup(T('comparison', 24, GREY).move_to([-3.2, -2.25, 0]),
                        T('stabilized β-catenin', 24, ORANGE).move_to([3.2, -2.25, 0]))
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(tag), FadeIn(normal), FadeIn(changed), FadeIn(labels), run_time=.65)
        cells = ring_dots(3.2, -.05, 1.8, 1.25, 4)
        self.at('kept more progenitor cycling')
        cycling = T('more progenitors cycling', 26, BLUE).move_to([0, 2.45, 0])
        self.play(FadeIn(cells), FadeIn(cycling), run_time=.6)
        self.play(Transform(cells, ring_dots(3.2, -.05, 1.8, 1.25, 8)), run_time=.6)
        self.at('cortex enlarged and buckled')
        vent = blob(1.3, .85, 0, 3.2, -.05).set_color(GREY).set_fill(opacity=0)
        self.add(vent)
        self.play(Transform(changed, blob(2.6, 1.7, .07, 3.2, -.05)),
                  Transform(vent, blob(1.9, 1.2, .07, 3.2, -.05).set_color(GREY).set_fill(opacity=0)),
                  Transform(cells, ring_dots(3.2, -.05, 2.6, 1.7, 8)), run_time=.9)
        self.at('did not reproduce primate cortical growth')
        caveat = T('Mouse expansion did not reproduce primate cortical growth', 26, GOLD).move_to([0, -3.15, 0])
        self.play(FadeIn(caveat), run_time=.6)
        self.finish()


class S06Genes(SpokenScene):
    def construct(self):
        head = heading('Human-specific gene copies: evidence by system')
        headers = VGroup(T('gene / intervention', 24, ORANGE).move_to([-4.75, 2.5, 0]),
                         T('experimental system', 24, GREY).move_to([-.7, 2.5, 0]),
                         T('observed result', 24, TEXT).move_to([3.9, 2.5, 0]))
        records = [
            ('ARHGAP11B', 'mouse embryos', 'more basal progenitors'),
            ('ARHGAP11B', 'marmoset fetuses', 'larger neocortex'),
            ('NOTCH2NL', 'mouse cortex', 'continued division'),
            ('NOTCH2NL deleted', 'human organoids', 'early differentiation'),
            ('ARHGAP11B blocked', 'cultured human\nfetal slices', 'fewer basal progenitors'),
        ]
        rows = VGroup()
        for i, (gene, system, result) in enumerate(records):
            y = 1.65 - .86 * i
            row = VGroup(T(gene, 23, ORANGE).move_to([-4.75, y, 0]),
                         T(system, 23, GREY).move_to([-.7, y, 0]),
                         T(result, 23, TEXT).move_to([3.9, y, 0]),
                         Line([-6.3, y-.39, 0], [6.3, y-.39, 0], color=GREY, stroke_width=1).set_opacity(.3))
            rows.add(row)
        self.at('gene copies act')
        self.play(FadeIn(head), FadeIn(headers), run_time=.6)
        self.at('increased basal progenitors')
        self.play(FadeIn(rows[0], shift=RIGHT*.15), run_time=.6)
        self.at('enlarged the neocortex')
        self.play(FadeIn(rows[1], shift=RIGHT*.15), run_time=.6)
        self.at('kept progenitors dividing')
        self.play(FadeIn(rows[2], shift=RIGHT*.15), run_time=.6)
        self.at('Deleting it made')
        self.play(FadeIn(rows[3], shift=RIGHT*.15), run_time=.6)
        self.at('In cultured human fetal slices')
        # Show the experimental system first; the result arrives only when spoken.
        self.play(FadeIn(rows[4][1]), FadeIn(rows[4][3]), run_time=.5)
        self.at('blocking')
        self.play(FadeIn(rows[4][0]), run_time=.5)
        self.at('reduced basal progenitors')
        self.play(FadeIn(rows[4][2]), run_time=.6)
        self.at('These tests support contributions')
        summary = T('progenitor amplification + continued division', 26, BLUE).move_to([0, -2.85, 0])
        self.play(FadeIn(summary), run_time=.6)
        self.at('None shows that one gene')
        caution = T('Contributions to expansion • no single-gene explanation', 26, GOLD).move_to([0, -3.4, 0])
        self.play(FadeIn(caution), run_time=.6)
        self.finish()


class S08Time(SpokenScene):
    def construct(self):
        head = heading('Time for producing neurons')
        note = T('schematic durations • no numerical scale', 22, GREY).move_to([0, -3.1, 0])
        rows = VGroup()
        for label, length, y in [('mouse', 2, 1.6), ('rhesus', 4, .5), ('human', 7, -.6)]:
            rows.add(VGroup(T(label, 26, GREY).move_to([-4.9, y, 0]), bar(-3.5, -3.5+length, y, BLUE, .38)))
        self.at('Time matters too')
        self.play(FadeIn(head), FadeIn(note), run_time=.5)
        self.at('Human cortical neurogenesis')
        self.play(FadeIn(rows), run_time=.65)
        self.at('more time to divide')
        cycle = VGroup(dot(4.5, -.6, BLUE, .22),
                       Arc(radius=.6, start_angle=.3, angle=5.5, color=BLUE).add_tip(tip_length=.15).move_to([4.5, -.6, 0]))
        cycle.shift(RIGHT * .4)
        self.play(FadeIn(cycle), run_time=.55)
        self.play(Rotate(cycle[1], angle=TAU), run_time=.65)
        self.at('Output also depends')
        factors = T('output: duration • cell-cycle length • division type', 26, BLUE).move_to([0, -2.05, 0])
        self.play(FadeIn(factors), run_time=.6)
        self.at('Human neurons mature slowly')
        newhead = heading('After production: neuron maturation', YELLOW)
        timeline = VGroup(arr([-5.7, -1.8, 0], [5.7, -1.8, 0], GREY),
                          T('postmitotic maturation →', 26, YELLOW).move_to([0, -2.4, 0]))
        neuron = dot(-4.6, .3, YELLOW, .25)
        label = T('human neuron', 26, YELLOW).move_to([-4.6, 1.35, 0])
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(newhead), FadeIn(timeline), FadeIn(neuron), FadeIn(label), run_time=.65)
        host = VGroup(RoundedRectangle(width=5.6, height=2.3, corner_radius=.2, color=GREY).move_to([2.6, .3, 0]),
                      T('newborn mouse cortex', 26, GREY).move_to([2.6, 1.9, 0]))
        self.at('Transplanted into newborn mouse cortex')
        self.play(FadeIn(host), neuron.animate.move_to([.7, .3, 0]), FadeOut(label), run_time=.8)
        pace = T('largely human pace', 28, YELLOW).move_to([0, -3.1, 0])
        # Symbolic maturation track, spatially separate from all production diagrams.
        self.at('they kept a largely human pace')
        track = Line([-5, -1.8, 0], [4.6, -1.8, 0], color=YELLOW, stroke_width=6)
        self.play(Create(track), neuron.animate.move_to([4.3, .3, 0]).scale(1.25), FadeIn(pace), run_time=1.1)
        self.at('distinct from producing neurons')
        distinction = T('Maturation is distinct from producing neurons', 28, GOLD).move_to([0, -3.1, 0])
        self.play(ReplacementTransform(pace, distinction), run_time=.6)
        self.finish()


class S09Scaling(SpokenScene):
    def construct(self):
        head = heading('Broadly consistent with primate scaling')
        axes = VGroup(arr([-4.3, -1.9, 0], [4.6, -1.9, 0]), arr([-4.3, -1.9, 0], [-4.3, 2.1, 0]),
                      T('brain size →', 24, GREY).move_to([.2, -2.45, 0]),
                      T('neuron number', 24, GREY).rotate(PI/2).move_to([-5.1, .2, 0]))
        trend = Line([-3.7, -1.5, 0], [3.7, 1.8, 0], color=GREEN, stroke_width=4)
        schematic = T('schematic relationship • no data values', 22, GREY).move_to([0, -3.15, 0])
        self.at('The result broadly fits')
        self.play(FadeIn(head), FadeIn(axes), Create(trend), FadeIn(schematic), run_time=.65)
        human = VGroup(dot(2.8, 1.4, YELLOW, .16), T('human', 26, YELLOW).move_to([4.1, 1.5, 0]))
        self.at('A human brain holds')
        self.play(FadeIn(human), run_time=.6)
        self.at('predicted for a primate brain')
        self.play(Indicate(human, color=YELLOW, scale_factor=1.1), run_time=.6)
        self.at('Mass alone misses')
        final_head = heading('Where neurons sit matters', GOLD)
        regions = VGroup(chip('cerebral cortex', YELLOW, 28).move_to([-3.2, .3, 0]),
                         chip('cerebellum', YELLOW, 28).move_to([3.2, .3, 0]))
        allocation = T('regional neuron allocation', 30, YELLOW).move_to([0, -1.2, 0])
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(final_head), FadeIn(regions), FadeIn(allocation), run_time=.65)
        self.finish()
