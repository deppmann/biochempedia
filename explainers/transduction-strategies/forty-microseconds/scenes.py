"""Chapter 2; final narration and word timings are unchanged.
COLOR MAP: YELLOW tissue latency / stimulus; BLUE channel / activation;
PURPLE enzymes / molecular gain; ORANGE behavioural latency; TEAL recording;
GREEN messenger / model products; RED exclusions; GREY preparation / axes.
Every trace is computed from the explicitly labelled illustrative model.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
CAPTION = '#C3CAD5'


def heading(text, color=TEXT):
    return T(text, 33, color, font=TITLE_FONT).move_to([0, 3.3, 0])


def note(text, y=-3.35, color=CAPTION):
    return T(text, 31, color).move_to([0, y, 0])


def arr(a, b, color=GREY):
    return Arrow(a, b, buff=.10, color=color, stroke_width=4, tip_length=.18)


def mapper(ox, oy, w, h, xmax=150, ymax=1):
    return lambda t, v: np.array([ox + w*t/xmax, oy + h*v/ymax, 0.])


def trace(f, t0, t1, mp, color, n=501, width=5):
    g = VMobject(stroke_color=color, stroke_width=width)
    g.set_points_as_corners([mp(t, f(t)) for t in np.linspace(t0, t1, n)])
    return g


def step_trace(mp, color=YELLOW, xmax=150):
    return VMobject(stroke_color=color, stroke_width=5).set_points_as_corners(
        [mp(0, 0), mp(40, 0), mp(40, 1), mp(xmax, 1)])


def plot_axes(x=-5.35, y=-1.85, w=10.8, h=4.35, xmax=150,
              ticks=(0, 50, 100, 150), ylabel='response'):
    mp = mapper(x, y, w, h, xmax)
    axes = VGroup(Line(mp(0, 0), mp(xmax, 0), color=GREY),
                  Line(mp(0, 0), mp(0, 1.07), color=GREY))
    for t in ticks:
        axes.add(Line(mp(t, 0)+DOWN*.08, mp(t, 0)+UP*.08, color=GREY),
                 M(str(t), 26, CAPTION).move_to(mp(t, 0)+DOWN*.36))
    axes.add(T('time (μs)', 27, CAPTION).move_to([x+w/2, y-.87, 0]),
             T(ylabel, 27, CAPTION).rotate(PI/2).move_to([x-.55, y+h/2, 0]))
    return axes, mp


def bracket(mp, end, y, label, color):
    a, b = mp(0, 0), mp(end, 0)
    a[1] = b[1] = y
    return VGroup(Line(a, b, color=color, stroke_width=3),
                  Line(a+UP*.09, a+DOWN*.09, color=color),
                  Line(b+UP*.09, b+DOWN*.09, color=color),
                  T(label, 26, color).next_to((a+b)/2, UP, buff=.13))


def hair_cell(s=1., chan=True):
    body = RoundedRectangle(corner_radius=.25*s, width=1.4*s, height=1.6*s,
                            stroke_color=GREY, fill_color=GREY, fill_opacity=.15)
    top = body.get_top()
    xs, hs = [-.4, 0, .4], [.65, 1., 1.35]
    cil = VGroup(*[Line(top+RIGHT*x*s, top+RIGHT*x*s+UP*h*s,
                       color=TEXT, stroke_width=5) for x, h in zip(xs, hs)])
    links = VGroup(*[Line(top+RIGHT*xs[i]*s+UP*hs[i]*s,
                         top+RIGHT*xs[i+1]*s+UP*(hs[i]+.22)*s,
                         color=GREY) for i in range(2)])
    channels = VGroup(*[Rectangle(width=.22*s, height=.16*s, color=BLUE,
                                  fill_opacity=1).move_to(l.get_center()) for l in links]) if chan else VGroup()
    g = VGroup(body, cil, links, channels)
    g.body, g.bundle = body, VGroup(cil, links, channels)
    return g


def sheet():
    cells = VGroup(*[hair_cell(1.).move_to([x, -.3, 0]) for x in [-2.7, -.9, .9, 2.7]])
    tray = VGroup(Line([-4.5, -1.45, 0], [-4.1, -2.05, 0], color=GREY),
                  Line([-4.1, -2.05, 0], [4.1, -2.05, 0], color=GREY),
                  Line([4.1, -2.05, 0], [4.5, -1.45, 0], color=GREY),
                  Line([-4.35, -1.65, 0], [4.35, -1.65, 0], color=TEAL, stroke_opacity=.65))
    tip = cells[2].bundle.get_top()
    probe = VGroup(Line([3.6, 2.45, 0], tip, color=TEAL, stroke_width=4),
                   Line([3.9, 2.45, 0], tip, color=TEAL, stroke_width=3))
    g = VGroup(cells, tray, probe)
    g.cells, g.tray, g.probe = cells, tray, probe
    return g


def pore(x=0, y=0, label=True):
    walls = VGroup(*[RoundedRectangle(width=.3, height=1.8, corner_radius=.08,
                                      color=BLUE, fill_color=BLUE, fill_opacity=.25)
                    .move_to([x+d, y, 0]) for d in [-.5, .5]])
    gate = Line([x-.35, y, 0], [x+.35, y, 0], color=BLUE, stroke_width=7)
    g = VGroup(walls, gate)
    if label:
        g.add(T('channel', 28, BLUE).move_to([x, y-1.25, 0]))
    g.gate = gate
    return g


def clock():
    face = Circle(radius=1.8, color=YELLOW, stroke_width=5)
    top = Rectangle(width=.65, height=.27, color=YELLOW).move_to([0, 2.0, 0])
    return VGroup(face, top, M('40 μs', 52, YELLOW))


def prediction():
    bundle = hair_cell(1.).move_to([-5.1, -.45, 0])
    enzyme = chip('enzyme', PURPLE, 30, pad=.3).move_to([-2.35, -.45, 0])
    messenger = chip('messenger', GREEN, 28, pad=.3).move_to([.8, -.45, 0])
    channel = pore(4.4, -.45)
    arrows = VGroup(arr([-4.25, 0, 0], [-3.5, 0, 0]),
                    arr([-1.2, 0, 0], [-.55, 0, 0]),
                    arr([2.2, 0, 0], [3.35, 0, 0]))
    q = T('Enzyme step inside 40 μs?', 36, YELLOW).move_to([0, -2.65, 0])
    timer = clock().scale(.52).move_to([5.45, 1.9, 0])
    main = VGroup(bundle, enzyme, messenger, channel, arrows).scale(1.08, about_point=ORIGIN)
    arrows.shift(DOWN*.45)
    timer.scale(1.35).move_to([4.9, 1.85, 0])
    return VGroup(bundle, enzyme, messenger, channel, arrows, q, timer)


CARD_TITLES = ['Tissue response\nlatency', 'Channel\nactivation\ntime constant',
               'Molecular\ngain', 'Behavioural\nlatency']
CARD_COLORS = [YELLOW, BLUE, PURPLE, ORANGE]
DEFINITIONS = ['Delay of a whole\npopulation\nof cells', 'How fast current\nrises in a patch\nor cell',
               'Output events\nper input event', 'Stimulus to\nmovement']
EXAMPLES = ['40 μs\nbullfrog sacculus', 'about 50 μs\nturtle hair cells',
            '≈ 12–14 effective\ncomplexes per\nactivated rhodopsin\n(mouse rods,\nGcaps-null)',
            'Conduction\nspinal circuits\nmuscle']


def card_icon(i, x):
    c = CARD_COLORS[i]
    if i == 0:
        return VGroup(*[hair_cell(.32).move_to([x+d, .65, 0]) for d in [-.7, 0, .7]])
    if i == 1:
        cell = hair_cell(.33).move_to([x-.25, .65, 0])
        pip = VGroup(Line([x+.9, 1.25, 0], cell.body.get_right(), color=TEAL),
                     Line([x+1.1, 1.15, 0], cell.body.get_right(), color=TEAL))
        return VGroup(cell, pip)
    if i == 2:
        source = Dot([x-.95, .65, 0], radius=.11, color=c)
        outputs = VGroup(*[Dot([x+.9, yy, 0], radius=.07, color=c) for yy in [.15, .4, .65, .9, 1.15]])
        return VGroup(source, *[arr(source.get_center(), d.get_center(), c) for d in outputs], outputs)
    return VGroup(Ellipse(width=1.05, height=.5, color=c, fill_opacity=.25).move_to([x-.1, .65, 0]),
                  Circle(radius=.2, color=c).move_to([x+.55, .75, 0]),
                  Circle(radius=.11, color=c).move_to([x+.45, 1., 0]),
                  Line([x-.62, .65, 0], [x-1, 1., 0], color=c),
                  Line([x-.35, .4, 0], [x-.6, .15, 0], color=c),
                  Line([x+.2, .4, 0], [x+.55, .15, 0], color=c))


def cards(n, defined=True):
    result = VGroup()
    for i, x in enumerate([-4.8, -1.6, 1.6, 4.8]):
        c = CARD_COLORS[i] if i < n else GREY
        box = RoundedRectangle(width=3.05, height=5.95, corner_radius=.15,
                               color=c, fill_color=c, fill_opacity=.07).move_to([x, -.05, 0])
        g = VGroup(box)
        if i < n:
            # All card text shares the same left inset and explicit line breaks.
            left = x-1.27
            title = T(CARD_TITLES[i], 24, c).move_to([left, 2.05, 0], aligned_edge=LEFT)
            definition = T(DEFINITIONS[i], 24, TEXT).move_to([left, -.55, 0], aligned_edge=LEFT)
            example = T(EXAMPLES[i], 23, c).move_to([left, -2.0, 0], aligned_edge=LEFT)
            for label in (title, definition, example):
                if label.width > 2.48:
                    label.scale_to_fit_width(2.48).align_to(title, LEFT)
            if not defined and i == n-1:
                definition.set_opacity(0)
            g.add(title, card_icon(i, x), definition, example)
        result.add(g)
    return result


class S00Title(TitleCard):
    LESSON = 'Five Ways to Turn a Stimulus into a Current'
    TITLE = 'Forty Microseconds: What a Fast Number Measures'
    def construct(self):
        brand = T('BIOCHEMISTRYPEDIA', 26, TEAL)
        lesson = T(self.LESSON, 28, CAPTION)
        title = VGroup(T('Forty Microseconds:', 44, font=TITLE_FONT),
                       T('What a Fast Number Measures', 44, font=TITLE_FONT)).arrange(DOWN, buff=.35)
        rule = Line(LEFT*1.4, RIGHT*1.4, color=YELLOW, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=.5).move_to(ORIGIN)
        self.add(brand, lesson, rule)
        self.play(FadeIn(title), run_time=.6)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        c = clock().scale(1.28).move_to([0, .15, 0])
        enzyme = chip('enzyme?', PURPLE, 32).move_to([-4.25, -.65, 0])
        self.add(c, enzyme, note('Could an enzyme fit in here?', -3.0, YELLOW))
        self.at('could an enzyme')
        self.play(enzyme.animate.move_to([0, -.8, 0]), run_time=.8)
        self.play(Circumscribe(enzyme, color=YELLOW), run_time=.5)
        self.at('first')
        self.play(FadeIn(heading('What does the number measure?')), run_time=.35)
        self.finish()


class S02Setup(SpokenScene):
    def construct(self):
        s = sheet()
        self.add(s.cells, s.tray, heading('Corey and Hudspeth, 1979'),
                 note('Bullfrog sacculus • in a dish', -2.9))
        self.at('moved the hair')
        self.play(Create(s.probe), run_time=.3)
        self.play(*[c.bundle.animate.rotate(-.28, about_point=c.body.get_top()) for c in s.cells],
                  s.probe.animate.shift(RIGHT*.3+DOWN*.1), run_time=.65)
        self.finish()


class S03Record(SpokenScene):
    def construct(self):
        s = sheet().scale(.72).move_to([-1.65, .05, 0])
        for c in s.cells:
            c.bundle.rotate(-.28, about_point=c.body.get_top())
        s.probe.shift(RIGHT*.26+DOWN*.086)
        self.add(s, heading('Summed electrical response across the sheet'),
                 note('Transepithelial microphonic', 2.55, TEAL))
        # Tapered tips contact opposite surfaces; independent leads reach the box.
        contact = s.cells[0].bundle[0][2].get_end()
        upper = Polygon(contact, contact+UP*.65+LEFT*.17, contact+UP*.65+RIGHT*.17,
                        color=TEAL, fill_color=TEAL, fill_opacity=.65)
        below = s.cells[0].body.get_bottom()
        lower = Polygon(below, below+DOWN*.65+LEFT*.17, below+DOWN*.65+RIGHT*.17,
                        color=TEAL, fill_color=TEAL, fill_opacity=.65)
        box = chip('summed response\nof the sheet', TEAL, 32, pad=.3).move_to([4.05, -.15, 0])
        wires = VGroup(VMobject(color=TEAL).set_points_as_corners(
            [contact+UP*.65, [contact[0], 1.9, 0], [4.05, 1.9, 0], [4.05, .6, 0]]),
            VMobject(color=TEAL).set_points_as_corners(
            [below+DOWN*.65, [below[0], -2.25, 0], [4.05, -2.25, 0], [4.05, -.9, 0]]))
        labels = VGroup(T('electrode above', 28, TEAL).move_to([-4.5, 2.2, 0]),
                        T('electrode below', 28, TEAL).move_to([-3.65, -2.8, 0]))
        self.at('they recorded')
        self.play(Create(upper), Create(lower), Create(wires), FadeIn(labels), FadeIn(box), run_time=.6)
        self.at('summed electrical response')
        self.play(Indicate(box, scale_factor=1.04), run_time=.6)
        self.finish()


# Illustrative RC: step at 40 us, tau=80 us. To show a recorded onset,
# read the onset at a 30% detection threshold on the filtered response.
# This threshold is a teaching choice, not a reconstruction of the experiment.
RC_TAU = 80.
DETECTION = .30
RECORDED_ONSET = 40 - RC_TAU*np.log(1-DETECTION)


def correction_picture():
    axes, mp = plot_axes(x=-5.3, y=-1.55, w=10.6, h=3.7, xmax=240,
                         ticks=(0, 40, 100, 200))
    raw = trace(lambda t: 1-np.exp(-max(0, t-40)/RC_TAU),
                0, 240, mp, TEAL)
    corrected = step_trace(mp, xmax=240)
    labels = VGroup(T('corrected step', 28, YELLOW).move_to([-1.5, 2.45, 0]),
                    T('recorded signal', 28, TEAL).move_to([3.8, .75, 0]))
    delays = VGroup(bracket(mp, 40, .7, 'true delay', YELLOW),
                    bracket(mp, RECORDED_ONSET, -.8, 'recorded delay', TEAL))
    delays[1][-1].become(T('recorded\ndelay', 26, TEAL).move_to([-4.42, -.1, 0]))
    onset = T('40 μs', 27, YELLOW).next_to(mp(40, 1), LEFT, buff=.18)
    return axes, mp, raw, corrected, labels, delays, onset


class S04Slow(SpokenScene):
    def construct(self):
        axes, mp, raw, cor, labels, delays, onset = correction_picture()
        self.add(axes, heading('Electrical filtering delays the recorded onset'),
                 note('Illustrative, not measured traces', -3.4),
                 note('RC filter • illustrative 30% detection threshold', -2.95))
        threshold = VGroup(
            DashedLine(mp(0, DETECTION), mp(RECORDED_ONSET, DETECTION),
                       color=CAPTION, stroke_width=2, stroke_opacity=.6),
            DashedLine(mp(RECORDED_ONSET, 0), mp(RECORDED_ONSET, DETECTION),
                       color=TEAL, stroke_width=2),
            Dot(mp(RECORDED_ONSET, DETECTION), radius=.07, color=TEAL),
            T('30%', 27, CAPTION).next_to(mp(RECORDED_ONSET, DETECTION), RIGHT, buff=.18).shift(DOWN*.22))
        self.at("the epithelium's own")
        self.play(Create(raw), FadeIn(labels[1]), FadeIn(threshold), run_time=.7)
        self.at('slows that signal')
        self.play(FadeIn(delays[1]), run_time=.4)
        self.at('so the recorded')
        self.play(Create(cor), FadeIn(labels[0]), FadeIn(onset), run_time=.6)
        self.at('longer than')
        self.play(FadeIn(delays[0]), run_time=.4)
        self.finish()


class S05Corrected(SpokenScene):
    def construct(self):
        axes, mp, raw, cor, labels, delays, onset = correction_picture()
        old = VGroup(axes, cor, labels[0], onset)
        self.add(old, heading('Corrected tissue delay', YELLOW),
                 note('22 degrees C • bullfrog sacculus', -3.05))
        c = clock().scale(1.15).move_to([0, .0, 0])
        self.at('after correcting')
        self.play(ReplacementTransform(old, c), run_time=1.1)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        p = prediction()
        self.add(p[0], p[3], p[6], heading('Predict'))
        self.at('suppose an enzyme')
        self.play(FadeIn(p[1]), GrowArrow(p[4][0]), run_time=.5)
        self.at('chemical messenger')
        self.play(FadeIn(p[2]), GrowArrow(p[4][1]), run_time=.5)
        self.at('between the bundle')
        self.play(GrowArrow(p[4][2]), run_time=.4)
        self.at('could the response')
        self.play(FadeIn(p[5]), run_time=.4)
        self.finish()


class S07Pause(Scene):
    def construct(self):
        self.camera.background_color = BG
        p = prediction()
        self.add(p, heading('Pause and predict'))
        # A depleting ring makes the silent five-second thinking interval visible.
        ring = Circle(radius=1.0, color=YELLOW, stroke_width=8).move_to(p[6][0].get_center())
        self.add(ring)
        self.play(Uncreate(ring), run_time=5, rate_func=linear)


class S08Reveal1(SpokenScene):
    def construct(self):
        self.add(heading('Illustrative free diffusion'))
        origin = np.array([-1.6, -.1, 0])
        # 100 nm per unit: the 30 nm gap is inside the RMS radius at 40 us.
        # The gate centre is the target; its H icon is schematic, not to scale.
        channel = pore(label=False).scale(.22)
        channel.shift(origin + RIGHT*(30/110 + .65*.22))
        source = Dot(origin, radius=.07, color=GREEN)
        self.add(source, channel,
                 T('source', 27, GREEN).move_to([-4.2, -.1, 0]),
                 Line([-3.5, -.1, 0], origin+LEFT*.12, color=GREEN),
                 T('channel (icon not to scale)\n30 nm from source to near rail', 27, BLUE).move_to([3.5, .5, 0]),
                 Line([1.8, .02, 0], channel.get_center(), color=BLUE))
        verdict = note('Only with great difficulty', -3.25, YELLOW)
        self.add(verdict)
        def cloud(t):
            radius = np.sqrt(6*300*t)*1000/110  # micrometres -> nm / 100
            return VGroup(*[Circle(radius=max(.02, k*radius), color=GREEN,
                                  stroke_opacity=.75, fill_color=GREEN, fill_opacity=.035)
                          .move_to(origin) for k in [.33, .67, 1.]])
        cl = cloud(1e-7)
        self.at('over a gap')
        self.play(FadeOut(verdict), FadeIn(cl), run_time=.3)
        self.at('free diffusion')
        self.play(Transform(cl, cloud(40e-6)), run_time=1.0)
        radius = np.sqrt(6*300*40e-6)*1000/110
        radius_line = Line(origin, origin+DL*radius/np.sqrt(2), color=GREEN)
        rlabel = T('Rings: spread at 40 μs • RMS ≈ 270 nm', 28, GREEN).move_to([-1.7, -2.85, 0])
        scale = VGroup(Line([3.2, -1.5, 0], [3.2+100/110, -1.5, 0], color=TEXT, stroke_width=5),
                       T('100 nm', 26).move_to([3.7, -1.92, 0]))
        self.add(radius_line, rlabel, scale,
                 note('D = 300 μm²/s • RMS = √(6Dt) • t = 40 μs', 2.7, GREEN))
        self.at('but that alone')
        self.play(Indicate(channel, color=BLUE), run_time=.4)
        self.at('finds and binds')
        self.play(FadeIn(T('Spread is not time\nto find and bind', 29, BLUE).move_to([3.7, -.55, 0])),
                  run_time=.4)
        self.add(note('Too slow? A later interpretation; not a claim of the 1979 abstract', -3.4))
        self.finish()


class S09Reveal2(SpokenScene):
    def construct(self):
        self.add(heading('Making a messenger in 40 μs'),
                 note('Constant-rate Poisson model', 2.6))
        enzyme = chip('one active\nenzyme', PURPLE, 30, pad=.3).move_to([-4.2, 1.3, 0])
        t = ValueTracker(0)
        timer = always_redraw(lambda: M(f'{t.get_value():.0f} μs', 46, YELLOW).move_to([3.8, 1.3, 0]))
        counter = always_redraw(lambda: M(f'{4000*t.get_value()*1e-6:.2f}', 44, GREEN).move_to([0, 1.3, 0]))
        self.add(enzyme, timer, counter, T('expected products', 27, GREEN).move_to([0, .58, 0]))
        line = Line([-5.4, -.25, 0], [5.4, -.25, 0], color=YELLOW, stroke_width=5)
        ticks = VGroup(*[VGroup(Line([x, -.37, 0], [x, -.13, 0], color=YELLOW),
                               M(str(v), 26, YELLOW).move_to([x, -.7, 0]))
                        for x, v in zip(np.linspace(-5.4, 5.4, 5), [0, 10, 20, 30, 40])])
        cursor = always_redraw(lambda: Dot([-5.4+10.8*t.get_value()/40, -.25, 0], color=GREEN, radius=.13))
        self.add(line, ticks, cursor, T('μs', 26, YELLOW).move_to([6.1, -.7, 0]))
        self.at('one enzyme')
        rate = T('4,000 turnovers / s', 26, PURPLE).move_to([-3.9, .1, 0])
        # Rate label belongs beside the enzyme, above the time bar.
        rate.move_to([-4.0, .3, 0])
        self.play(FadeIn(rate), run_time=.3)
        self.at('turnovers a second')
        self.play(t.animate.set_value(40), run_time=1.25, rate_func=linear)
        self.at('on average')
        self.play(FadeIn(M('4,000 per s × 0.00004 s = 0.16', 30, GREEN).move_to([0, -1.35, 0])), run_time=.4)
        self.at('only')
        self.play(Indicate(counter, scale_factor=1.1), run_time=.4)
        self.at('that is about')
        p = 1-np.exp(-4000*40e-6)
        bar = Rectangle(width=10.8, height=.46, color=GREY).move_to([0, -2.25, 0])
        fill = Rectangle(width=10.8*p, height=.46, stroke_width=0, fill_color=GREEN,
                         fill_opacity=1).align_to(bar, LEFT).set_y(-2.25)
        ends = VGroup(M('0%', 26).move_to([-5.4, -2.85, 0]), M('100%', 26).move_to([5.4, -2.85, 0]))
        self.play(Create(bar), FadeIn(fill), FadeIn(ends),
                  FadeIn(note('P(at least one product) = 1 − exp(−0.16) ≈ 15%', -3.4, GREEN)), run_time=.6)
        self.finish()


class S10Interp(SpokenScene):
    def construct(self):
        p = pore(-3.1, 0, label=False).scale(1.25)
        enz = VGroup(*[chip('enzyme', PURPLE, 28, pad=.25).move_to(pos)
                      for pos in [[-5, 1.7, 0], [-1.4, 1.7, 0], [-5, -1.7, 0], [-1.4, -1.7, 0]]])
        channel_label = T('channel', 28, BLUE).move_to([-3.1, -2.55, 0])
        arrangement = VGroup(p, enz, channel_label).scale(1.15).move_to([0, -.1, 0])
        self.add(arrangement, heading('Hypothetical arrangement', PURPLE))
        glows = VGroup(*[e[0].copy().set_stroke(PURPLE, width=15, opacity=.22)
                         .set_fill(PURPLE, opacity=.25) for e in enz])
        self.at('many enzymes')
        self.play(FadeIn(glows), *[e[0].animate.set_fill(PURPLE, opacity=.4) for e in enz], run_time=.5)
        self.at('to test')
        self.play(arrangement.animate.scale(.87).move_to([-3.5, -.1, 0]),
                  glows.animate.scale(.87).shift(LEFT*3.5), run_time=.6)
        cues = [('enzyme numbers', 'enzyme numbers'),
                ('activation and binding', 'activation and\nbinding rates'),
                ('geometry', 'geometry'),
                ('messenger level', 'messenger level → current')]
        for (cue, text), y in zip(cues, [1.8, .65, -.65, -1.7]):
            lab = T(text, 32, TEXT).move_to([.25, y, 0], aligned_edge=LEFT)
            self.at(cue)
            self.play(FadeIn(lab, shift=RIGHT*.12), run_time=.35)
        self.at('this is a model')
        self.play(FadeIn(note('A model check, not a result of the 1979 experiment', -3.25, YELLOW)), run_time=.4)
        self.finish()


class S11Isnot(SpokenScene):
    def construct(self):
        s = sheet().scale(.86).move_to([-1.3, .4, 0])
        self.add(s, heading('40 μs: tissue response latency', YELLOW))
        h = pore(4.5, .55, label=False).scale(1.25)
        dashed = VGroup(*[DashedVMobject(part, num_dashes=16) for part in h.family_members_with_points()])
        self.add(dashed, T('?', 40, BLUE).move_to([4.5, 1.95, 0]),
                 T('one channel', 28, BLUE).move_to([4.5, -1.0, 0]),
                 DashedLine([2, .3, 0], [3.6, .3, 0], color=BLUE))
        a = VGroup(T('×', 52, '#FF6B78', weight=BOLD), T("one channel's opening time", 30)).arrange(RIGHT, buff=.3).move_to([0, -2.3, 0])
        b = VGroup(T('×', 52, '#FF6B78', weight=BOLD), T('a mouse number', 30)).arrange(RIGHT, buff=.3).move_to([0, -3.05, 0])
        self.at('it is not')
        self.play(FadeIn(a), run_time=.4)
        self.at('and it is')
        self.play(FadeIn(b), run_time=.4)
        self.finish()


class S12Ricci(SpokenScene):
    def construct(self):
        self.add(heading('Direct channel activation measurement'),
                 note('Ricci and colleagues, 2005', 2.65),
                 note('Exponential model, illustrative: I/Imax = 1 − exp(−t / 50 μs)', -3.4))
        cell = hair_cell(.85).move_to([-4.9, -.15, 0])
        touch = cell.body.get_left()
        pip = VGroup(Line([-6.2, 1.8, 0], touch, color=TEAL, stroke_width=4),
                     Line([-6.5, 1.7, 0], touch, color=TEAL, stroke_width=4))
        self.add(cell, pip, T('turtle\nhair cell', 28, BLUE).move_to([-4.8, -2.4, 0]))
        axes, mp = plot_axes(x=-2.5, y=-1.8, w=8.4, h=3.9, xmax=150, ylabel='current / final')
        self.add(axes)
        curve = trace(lambda t: 1-np.exp(-t/50), 0, 150, mp, BLUE)
        self.at('channel speed')
        self.play(Create(curve), run_time=.9)
        self.at('time constants')
        v = 1-np.exp(-1)
        guides = VGroup(DashedLine(mp(50, 0), mp(50, v), color=BLUE),
                        Dot(mp(50, v), color=BLUE, radius=.09),
                        T('63% at 50 μs', 28, BLUE).move_to([2.9, -.1, 0]),
                        Line([1.65, .02, 0], mp(50, v), color=BLUE))
        self.play(FadeIn(guides), run_time=.5)
        self.finish()


class S13Same(SpokenScene):
    def construct(self):
        self.add(heading('Similar time scale; different measurements'))
        axes, mp = plot_axes(x=-5.1, y=-1.5, w=10.5, h=3.6, xmax=110, ticks=(0, 50, 100))
        tissue = step_trace(mp, xmax=110)
        channel = trace(lambda t: 1-np.exp(-t/50), 0, 110, mp, BLUE)
        self.add(axes, tissue, channel,
                 T('tissue latency', 28, YELLOW).move_to([2.65, 2.4, 0]),
                 T('channel time constant', 28, BLUE).move_to([3.1, -.1, 0]),
                 note('Illustrative response models', -3.4))
        forty = VGroup(Line(mp(40, 0)+DOWN*.09, mp(40, 0)+UP*.09, color=YELLOW),
                       M('40', 26, YELLOW).move_to(mp(40, 0)+DOWN*.38))
        point = mp(50, 1-np.exp(-1))
        fifty = VGroup(DashedLine(mp(50, 0), point, color=BLUE), Dot(point, color=BLUE),
                       T('50 μs: 63%', 27, BLUE).move_to([3.3, .7, 0]),
                       Line([1.8, .7, 0], point, color=BLUE))
        self.add(forty, fifty)
        # Legend definitions sit below the plot, away from ticks and traces.
        self.add(T('delay of a whole sheet', 27, YELLOW).move_to([-3, -2.95, 0]),
                 T('rise of channel current', 27, BLUE).move_to([3.1, -2.95, 0]))
        self.at('so in turtle')
        self.play(Indicate(channel, scale_factor=1.01), run_time=.6)
        self.at('number simply')
        self.play(Indicate(tissue, scale_factor=1.01), run_time=.5)
        self.finish()


class S14Four(SpokenScene):
    def construct(self):
        c = cards(0)
        self.add(c, heading('Four kinds of number'))
        self.at('a tissue response')
        self.play(Transform(c, cards(1, defined=False)), run_time=.5)
        self.at('the delay of')
        self.play(Transform(c, cards(1)), run_time=.4)
        self.finish()


class S15Channel(SpokenScene):
    def construct(self):
        c = cards(1)
        self.add(c, heading('Four kinds of number'))
        self.at('a channel activation')
        self.play(Transform(c, cards(2, defined=False)), run_time=.5)
        self.at('how fast current')
        self.play(Transform(c, cards(2)), run_time=.4)
        self.finish()


class S16Gain(SpokenScene):
    def construct(self):
        c = cards(2)
        self.add(c, heading('Four kinds of number'))
        self.at('a molecular gain')
        self.play(Transform(c, cards(3, defined=False)), run_time=.45)
        self.at('output events')
        self.play(Transform(c, cards(3)), run_time=.35)
        self.finish()


class S17Behav(SpokenScene):
    def construct(self):
        c = cards(3)
        self.add(c, heading('Four kinds of number'))
        self.at('and a')
        self.play(Transform(c, cards(4, defined=False)), run_time=.5)
        self.at('stimulus to movement')
        self.play(Transform(c, cards(4)), run_time=.4)
        self.at('through conduction')
        self.play(Indicate(c[3][4], color=ORANGE, scale_factor=1.02), run_time=.5)
        self.at('and muscle')
        self.play(FadeIn(note('No channel time constant stands in for it', -3.45, ORANGE)), run_time=.3)
        self.finish()


class S18Speed(SpokenScene):
    def construct(self):
        p = pore(0, .5).scale(1.65)
        self.add(p, heading('Candidate channel', BLUE))
        a = T('40 μs tissue latency\nsimilar scale,\ndifferent measurement', 28, YELLOW, should_center=True).move_to([-4.0, .6, 0])
        b = T('✓ 50 μs\nchannel time constant', 30, BLUE).move_to([3.8, .6, 0])
        self.at('speed can be')
        self.play(FadeIn(a), FadeIn(b), run_time=.5)
        self.add(note('Compatible time scale', -2.0, BLUE))
        self.at('but speed alone')
        self.play(FadeIn(T('Speed alone does not identify the channel', 32, TEXT)
                         .move_to([0, -3.05, 0])), run_time=.5)
        self.finish()


class S19Take(SpokenScene):
    def construct(self):
        boxes = VGroup()
        for title, c, pos in zip(CARD_TITLES, CARD_COLORS,
                                 [[-3.2, 2, 0], [3.2, 2, 0], [-3.2, .25, 0], [3.2, .25, 0]]):
            box = RoundedRectangle(width=5.6, height=1.35, corner_radius=.14,
                                   color=c, fill_color=c, fill_opacity=.12)
            lines = title.replace('Channel\nactivation\ntime constant',
                                  'Channel activation\ntime constant').split('\n')
            label = VGroup(*[T(line, 28, c) for line in lines]).arrange(DOWN, buff=.08)
            if label.width > 5.1:
                label.scale_to_fit_width(5.1)
            boxes.add(VGroup(box, label.move_to(box)).move_to(pos))
        self.add(boxes)
        self.at('before you compare')
        self.play(boxes[0].animate.move_to([-3.2, -.65, 0]),
                  boxes[1].animate.move_to([3.2, -.65, 0]),
                  boxes[2].animate.move_to([-3.2, 1.65, 0]),
                  boxes[3].animate.move_to([3.2, 1.65, 0]),
                  FadeIn(T('?', 44, YELLOW).move_to([0, -.65, 0])), run_time=.7)
        self.at('ask whether')
        self.play(FadeIn(T('Same kind of number?', 36, YELLOW, font=TITLE_FONT)
                         .move_to([0, -2.55, 0])), run_time=.4)

        self.finish()


class S20End(EndCard):
    LINE = 'Ask whether they are the same kind of number.'
