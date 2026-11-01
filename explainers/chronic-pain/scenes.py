"""A reflex is not the pain  (Biochemistrypedia explainer for 'When Pain Persists')

COLOR MAP (one color per concept, whole video)
  PURPLE = the basolateral amygdala ensemble (outline = identified, filled = active)
  BLUE   = withdrawal reflex (the measured endpoint)
  ORANGE = escape and avoidance (the affective-motivational endpoint)
  YELLOW = noxious stimulus
  TEAL   = innocuous stimulus
  GOLD   = the genetic tag
  RED    = silenced / not shown
  GREY   = other cells, frames, labels and neutral pathway schematics
  TEXT   = neuronal signals / processing (new scenes); old endpoint colours retained
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

# cells are a schematic; positions are unit-box layout, not data
POS = [(-3.2, 1.4), (-1.6, 1.2), (0.0, 1.5), (1.6, 1.3), (3.2, 1.4),
       (-3.1, 0.0), (-1.7, -0.2), (0.0, 0.1), (1.7, -0.1), (3.0, 0.2),
       (-3.2, -1.4), (-1.5, -1.5), (0.1, -1.3), (1.5, -1.5), (3.1, -1.4)]
ENS = [1, 4, 6, 9, 12, 14]
BOXW, BOXH = 8.0, 4.8


def cell(p):
    soma = Circle(radius=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12)
    stubs = VGroup(*[Line(ORIGIN, 0.26 * np.array([np.cos(a), np.sin(a), 0]), color=GREY, stroke_width=3)
                     .shift(0.3 * np.array([np.cos(a), np.sin(a), 0])) for a in (0.5, 2.4, 4.2)])
    g = VGroup(soma, stubs)
    g.move_to([p[0], p[1] - 0.3, 0])
    return g


def make_box(center, scale=1.0):
    frame = RoundedRectangle(corner_radius=0.3, width=BOXW, height=BOXH, stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.05).move_to([0, -0.3, 0])
    cells = [cell(p) for p in POS]
    g = VGroup(frame, *cells)
    g.scale(scale).move_to(center)
    g.frame, g.cells = frame, cells
    return g


def style(c, state):
    """state: grey | ident | lit | silent"""
    soma, stubs = c[0], c[1]
    if state == "grey":
        return [soma.animate.set_stroke(GREY).set_fill(GREY, 0.12), stubs.animate.set_color(GREY)]
    if state == "ident":
        return [soma.animate.set_stroke(PURPLE).set_fill(PURPLE, 0.1), stubs.animate.set_color(PURPLE)]
    if state == "lit":
        return [soma.animate.set_stroke(PURPLE).set_fill(PURPLE, 0.95), stubs.animate.set_color(PURPLE)]
    if state == "silent":
        return [soma.animate.set_stroke(PURPLE, opacity=0.5).set_fill(PURPLE, 0.0), stubs.animate.set_color(PURPLE).set_opacity(0.4)]


def setstyle(c, state):
    soma, stubs = c[0], c[1]
    if state == "grey":
        soma.set_stroke(GREY).set_fill(GREY, 0.12); stubs.set_color(GREY)
    elif state == "ident":
        soma.set_stroke(PURPLE).set_fill(PURPLE, 0.1); stubs.set_color(PURPLE)
    elif state == "lit":
        soma.set_stroke(PURPLE).set_fill(PURPLE, 0.95); stubs.set_color(PURPLE)


def ring(c, color=GOLD):
    return Circle(radius=c[0].width / 2 + 0.12, stroke_color=color, stroke_width=4).move_to(c[0])


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


MY0 = -2.2  # meter bottom
MH = 3.3


def meter_fill(x, color, level, w=1.1):
    r = Rectangle(width=w - 0.1, height=max(0.02, MH * level), stroke_width=0, fill_color=color, fill_opacity=0.85)
    r.move_to([x, MY0 + max(0.02, MH * level) / 2, 0])
    return r


def meter(x, color, label, level, w=1.1):
    frame = Rectangle(width=w, height=MH + 0.1, stroke_color=color, stroke_width=3).move_to([x, MY0 + MH / 2 - 0.0 + 0.0, 0])
    frame.move_to([x, MY0 + (MH + 0.1) / 2 - 0.05, 0])
    fill = meter_fill(x, color, level, w)
    lab = T(label, 24, color).next_to(frame, DOWN, buff=0.18)
    return VGroup(frame, fill, lab)


class S00Title(TitleCard):
    LESSON = "When pain persists"
    TITLE = "Why pain persists after nerve injury"


DASH_X = 4.7
BM_X = 1.9
CL_C = [-3.2, -0.2, 0]
CL_S = 0.75


def dashed_q():
    box = RoundedRectangle(corner_radius=0.25, width=1.7, height=MH + 0.1, stroke_color=ORANGE, stroke_width=3)
    box = DashedVMobject(box, num_dashes=36)
    qm = T("?", 90, ORANGE, weight=BOLD)
    cy = MY0 + (MH + 0.1) / 2 - 0.05
    box.move_to([DASH_X, cy, 0])
    qm.move_to(box.get_center())
    lab = T("unpleasant\nexperience", 24, ORANGE).next_to(box, DOWN, buff=0.18)
    return VGroup(box, qm, lab)


# New narration: neutral schematics preserve the original endpoint colour map.
# All pulse positions and event counts illustrate mechanisms, never measured data.
def neuron(center, scale=1.0):
    c = cell((0, 0)).scale(2.0).move_to(ORIGIN)
    axon = Line([0.6, 0, 0], [2.8, 0, 0], color=GREY, stroke_width=4)
    return VGroup(c, axon).scale(scale).move_to(center)


def pulse_along(scene, start, end, color=TEXT, seconds=0.8):
    d = Dot(start, radius=0.10, color=color)
    scene.add(d)
    scene.play(d.animate.move_to(end), run_time=seconds, rate_func=linear)
    scene.remove(d)


def heading(text, y=3.15, color=TEXT):
    return T(text, 30, color, font=TITLE_FONT).move_to([0, y, 0])


def panel(text, x):
    frame = RoundedRectangle(width=4.05, height=4.05, corner_radius=0.25,
                             stroke_color=GREY, fill_color=GREY, fill_opacity=0.05)
    label = T(text, 30).move_to([0, 1.2, 0])
    return VGroup(frame, label).move_to([x, -0.15, 0])


def event_row(dense=False):
    # Schematic event marks, without numerical axes or a fabricated recording.
    xs = [-2.7, -0.6, 1.7] if not dense else [-2.7, -2.0, -1.2, -0.6, 0.2, 1.0, 1.7, 2.5]
    base = Line([-3.2, -0.7, 0], [3.2, -0.7, 0], color=GREY)
    marks = VGroup(*[Line([x, -0.7, 0], [x, 0.0, 0], color=TEXT, stroke_width=4) for x in xs])
    return VGroup(base, marks)


def processing_map():
    labels = [('sensory\nneuron', [-4.5, 0.8, 0]), ('spinal\ncord', [0, 0.8, 0]),
              ('immune\ncells', [0, -1.1, 0]), ('brain\ncircuits', [4.5, 0.8, 0])]
    nodes = [chip(name, GREY, size=36, pad=0.3).move_to(pos) for name, pos in labels]
    links = VGroup(arr(nodes[0].get_right(), nodes[1].get_left()),
                   arr(nodes[1].get_right(), nodes[3].get_left()),
                   arr(nodes[2].get_top(), nodes[1].get_bottom()))
    return VGroup(links, *nodes)


class S01Processing(SpokenScene):
    def construct(self):
        scope = chip('after nerve injury', GREY, size=24).move_to([0, 3.15, 0])
        self.at('After a nerve injury')
        self.play(FadeIn(scope), run_time=0.6)
        head = heading('The nervous system itself can change', 2.25)
        self.at('the nervous system')
        self.play(FadeIn(head), run_time=0.7)
        p1, p2, p3 = [panel(t, x) for t, x in [('sensory neuron', -4.25), ('spinal cord', 0), ('immune cells', 4.25)]]
        n = neuron([-4.25, 0.05, 0], 0.8)
        no = T('no applied\nstimulus', 35, GREY).move_to([-4.25, -1.3, 0])
        self.at('Sensory neurons can fire')
        self.play(FadeIn(p1), FadeIn(n), FadeIn(no), run_time=0.6)
        pulse_along(self, n[1].get_start(), n[1].get_end())
        self.at('The spinal cord')
        target = cell((0, 0)).scale(1.5).move_to([0.8, -0.05, 0])
        inputs = VGroup(*[arr([-1.4, y, 0], [0.25, -0.05, 0], TEXT, 3) for y in (0.55, -0.05, -0.65)])
        cord = VGroup(p2, target, inputs, T('more\nexcitation', 35).move_to([0, -1.35, 0]))
        self.play(FadeIn(cord), run_time=0.6)
        self.play(LaggedStart(*[ShowPassingFlash(a.copy().set_color(TEXT), time_width=0.4) for a in inputs], lag_ratio=0.2), run_time=1)
        self.at('Immune cells can')
        immune = cell((0, 0)).scale(1.5).move_to([3.5, 0, 0])
        recipient = cell((0, 0)).move_to([5.2, 0, 0])
        signal = arr([4.0, 0, 0], [4.85, 0, 0], TEXT, 3)
        im = VGroup(p3, immune, recipient, signal, T('sustain\nsensitivity', 35).move_to([4.25, -1.35, 0]))
        self.play(FadeIn(im), run_time=0.6)
        pulse_along(self, signal.get_start(), signal.get_end(), seconds=0.6)
        self.at('persistent pain can reflect')
        new = heading('Persistent pain can reflect changed processing', 2.25)
        self.play(Transform(head, new), run_time=0.7)
        self.at('at several levels')
        self.play(*[Indicate(p[0], color=TEXT, scale_factor=1.02) for p in (p1, p2, p3)], run_time=0.8)
        self.at('more than an acute warning')
        note = T('more than a continuing acute warning', 24, GREY).move_to([0, -2.5, 0])
        self.play(FadeIn(note), run_time=0.6)
        self.at('Each experiment measures')
        self.play(Transform(note, T('Each preparation measures a particular change', 26).move_to(note)), run_time=0.7)
        self.finish()


class S02Periphery(SpokenScene):
    def construct(self):
        h = heading('Start with the first neuron')
        n = neuron([-1.8, 0, 0], 1.3)
        self.at('Start with the first neuron')
        self.play(FadeIn(h), FadeIn(n), run_time=0.7)
        prep = T('Human DRG neurons in culture\nfrom tumour-surgery donors', 27, GREY).move_to([0, 2.05, 0])
        dish = Ellipse(width=6.2, height=2.8, color=GREY).move_to(n)
        self.at('Cultured human sensory neurons')
        self.play(Transform(h, heading('Human sensory neurons')), FadeIn(prep), Create(dish), run_time=0.7)
        note = T('sometimes: spontaneous firing\nwithout an applied stimulus', 24).move_to([3.8, -0.2, 0])
        self.at('sometimes fired spontaneously')
        self.play(FadeIn(note), run_time=0.5)
        pulse_along(self, n[1].get_start(), n[1].get_end())
        assoc = T('Associated with donor radicular / neuropathic pain', 26).move_to([0, -2.1, 0])
        self.at('was associated with')
        self.play(FadeIn(assoc), run_time=0.7)
        caveat = chip('association in culture', GREY, size=25).move_to([0, -3.05, 0])
        self.at('This is an association')
        self.play(FadeIn(caveat), run_time=0.6)
        self.at('Rat studies also show')
        ratprep = T('Rat afferents after nerve injury\nuninjured neighbouring neurons', 27, GREY).move_to([0, 2.05, 0])
        self.play(FadeOut(dish), FadeOut(assoc), FadeOut(caveat),
                  Transform(h, heading('A separate rat preparation')), Transform(prep, ratprep),
                  Transform(note, T('spontaneous firing\nwithout an applied stimulus', 24).move_to(note)), run_time=0.6)
        self.at('spontaneous firing')
        pulse_along(self, n[1].get_start(), n[1].get_end())
        self.at('In other rat recordings')
        events = event_row()
        recording = T('Spinal recordings in anaesthetized rats', 27, GREY).move_to([0, 2.05, 0])
        schema = T('qualitative schematic — not a recording', 22, GREY).move_to([0, -1.5, 0])
        self.play(FadeOut(n), FadeOut(note), Transform(h, heading('Another rat preparation')),
                  Transform(prep, recording), FadeIn(events), FadeIn(schema), run_time=0.7)
        self.at('more frequent excitatory synaptic events')
        self.play(Transform(events, event_row(True)), run_time=1.0)
        self.at('That measures input')
        inp = T('excitatory synaptic input', 27).move_to([0, 0.9, 0])
        self.play(FadeIn(inp), run_time=0.6)
        self.at('It does not measure')
        distinction = T('Synaptic input ≠ unpleasantness', 32, font=TITLE_FONT).move_to([0, -2.65, 0])
        self.play(FadeIn(distinction), run_time=0.7)
        self.finish()


class S03Immune(SpokenScene):
    def construct(self):
        head = heading('Immune cells can change neuronal signalling')
        self.at('immune cells can change')
        self.play(FadeIn(head), run_time=0.6)
        scope = chip('Study 1 · nerve-injured rats', GREY, size=25).move_to([0, 2.1, 0])
        micro = cell((0, 0)).scale(3).move_to([-3.5, 0, 0])
        ml = T('reactive spinal\nmicroglia', 26, GREY).move_to([-3.5, -1.65, 0])
        receptor = chip('P2X4 ↑', GREY, size=26).move_to([-1.2, 0.65, 0])
        self.at('In nerve')
        self.play(FadeIn(scope), FadeIn(micro), FadeIn(ml), FadeIn(receptor), run_time=0.6)
        result = chip('touch hypersensitivity', GREY, size=26).move_to([3, 0.4, 0])
        self.at('lowering P2X4 receptors')
        self.play(Transform(receptor, chip('P2X4 ↓', GREY, size=26).move_to(receptor)), FadeIn(result), run_time=0.6)
        self.at('reduced touch hypersensitivity')
        reduction = T('reduced', 30).move_to([3, -0.75, 0])
        self.play(FadeIn(reduction, shift=DOWN * 0.3), run_time=0.6)
        self.at('A separate rat study')
        self.play(FadeOut(VGroup(micro, ml, receptor, result, reduction)),
                  Transform(scope, chip('Study 2 · rats', GREY, size=25).move_to(scope)),
                  Transform(head, heading('A separate study links microglia to neurons')), run_time=0.6)
        mg = VGroup(cell((0, 0)).scale(2).move_to([-4.7, 0.5, 0]),
                    T('microglia', 25, GREY).move_to([-4.7, -0.55, 0])).scale(1.3, about_point=[-4.7, 0.5, 0])
        atp = chip('ATP', GREY, size=33).move_to([-4.7, 2.3, 0])
        bdnf = chip('BDNF', GREY, size=35).move_to([-0.8, 0.5, 0])
        release = arr([-3.5, 0.5, 0], bdnf.get_left(), TEXT)
        self.at('stimulated with')
        self.play(FadeIn(mg), FadeIn(atp), run_time=0.5)
        self.at('released BDNF')
        self.play(FadeIn(bdnf, shift=RIGHT * 0.3), GrowArrow(release), run_time=0.7)
        neuron_group = VGroup(cell((0, 0)).scale(2.6).move_to([4.6, 0.5, 0]),
                             T('lamina I neuron', 33, GREY).move_to([4.6, -0.95, 0]),
                             chip('TrkB', GREY, size=31).move_to([2.4, 0.5, 0]))
        link = arr(bdnf.get_right(), neuron_group[2].get_left(), TEXT)
        axis = Line([-1.5, -1.55, 0], [4.6, -1.55, 0], color=GREY)
        dot = Dot([-0.7, -1.55, 0], color=TEXT, radius=0.13)
        shiftlabel = T('anion reversal potential\nshift in depolarizing direction →', 33).move_to([1.5, -2.65, 0])
        potential = VGroup(axis, dot, shiftlabel)
        self.at('That shifted the anion reversal potential')
        self.play(FadeIn(neuron_group), GrowArrow(link), FadeIn(potential), run_time=0.6)
        self.play(dot.animate.move_to([3.5, -1.55, 0]), run_time=0.8)
        self.at('Blocking BDNF')
        cross = Cross(link, stroke_color=RED, stroke_width=6)
        self.play(Create(cross), run_time=0.6)
        self.at('reversed both the shift')
        self.play(dot.animate.move_to([-0.7, -1.55, 0]),
                  Transform(shiftlabel, T('shift reversed\nhypersensitivity reversed', 33).move_to(shiftlabel)), run_time=0.8)
        self.at('These are links')
        self.play(Indicate(scope[0], color=TEXT, scale_factor=1.05), run_time=0.7)
        self.finish()


class S01Reflex(SpokenScene):
    def construct(self):
        brain = chip('brain circuits', GREY, size=30).move_to([0, 1.7, 0])
        cord = chip('spinal cord', GREY, size=30).move_to([0, -1.4, 0])
        self.at('Now the brain')
        self.play(FadeIn(brain), run_time=0.6)
        affect = chip('unpleasant side\nof pain', ORANGE, size=26).move_to([-4.3, 1.7, 0])
        self.at('Brain circuits shape')
        self.play(FadeIn(affect), run_time=0.6)
        down = arr([1.1, 1.15, 0], [1.1, -0.85, 0], TEXT)
        self.at('send signals back down')
        self.play(FadeIn(cord), GrowArrow(down), run_time=0.7)
        scope = chip('rodent experiments', GREY, size=24).move_to([0, 3.15, 0])
        self.at('In rodent experiments')
        self.play(FadeIn(scope), run_time=0.6)
        acc = chip('anterior cingulate\ncortex', GREY, size=27).move_to(brain)
        self.at('stimulating the anterior cingulate cortex')
        self.play(Transform(brain, acc), run_time=0.6)
        self.at('strengthened spinal excitatory transmission')
        self.play(ShowPassingFlash(down.copy().set_color(TEXT), time_width=0.7), run_time=0.6)
        excitation = T('stronger excitatory\ntransmission', 25).move_to([4.1, -1.4, 0])
        self.play(FadeIn(excitation), Indicate(cord, color=TEXT, scale_factor=1.08), run_time=0.6)
        self.at('Descending control can facilitate')
        self.play(ShowPassingFlash(down.copy().set_color(TEXT), time_width=0.7), run_time=0.8)
        self.at('Keep the measurements apart')
        self.play(FadeOut(VGroup(brain, cord, affect, down, excitation, scope)), run_time=0.5)
        # Reuse the original meter frame and dashed question; no heights equate endpoints.
        m = meter(-3.2, BLUE, 'withdrawal\nreflex', 0.0, w=2.3)
        m.remove(m[1])
        m.shift(UP * 0.6)
        paw = T('paw pulls\naway', 26, BLUE).move_to(m[0])
        q = dashed_q().shift(LEFT * 1.8 + UP * 0.6)
        self.at('A withdrawal reflex')
        self.play(FadeIn(m), FadeIn(paw), FadeIn(q), run_time=0.7)
        distinct = T('separate measurements', 28, font=TITLE_FONT).move_to([0, 2.6, 0])
        self.play(FadeIn(distinct), run_time=0.5)
        self.at('More synaptic events cannot tell us')
        note = T('Synaptic input ≠ unpleasantness', 30).move_to([0, -3.3, 0])
        self.play(FadeIn(note), run_time=0.7)
        self.finish()


class S06Scope(SpokenScene):
    def construct(self):
        head = heading('The immune route depends on context')
        self.at('the immune route depends')
        self.play(FadeIn(head), run_time=0.6)
        male = chip('male mice', GREY, size=27).move_to([-3.3, 1.6, 0])
        female = chip('female mice', GREY, size=27).move_to([3.3, 1.6, 0])
        tested = T('tested conditions after nerve injury', 23, GREY).move_to([0, 2.5, 0])
        self.at('In the tested mice')
        self.play(FadeIn(male), FadeIn(female), FadeIn(tested), run_time=0.5)
        inhibitor = chip('microglial inhibitor', GREY, size=26).move_to([0, 0.4, 0])
        self.at('a microglial inhibitor')
        self.play(FadeIn(inhibitor), run_time=0.5)
        mr = T('hypersensitivity\nreversed', 27).move_to([-3.3, -0.9, 0])
        fr = T('hypersensitivity\nnot reversed', 27).move_to([3.3, -0.9, 0])
        self.at('in males')
        self.play(FadeIn(mr, shift=DOWN * 0.2), run_time=0.4)
        self.at('but not females')
        self.play(FadeIn(fr), run_time=0.5)
        adaptive = T('females: adaptive immune cells appeared to contribute', 24, GREY).move_to([0, -2.3, 0])
        self.at('Females appeared to use')
        self.play(FadeIn(adaptive), run_time=0.6)
        self.at('Without those cells')
        # Reset the result during the condition change, before revealing the new result.
        self.play(FadeOut(VGroup(male, mr, fr, adaptive)),
                  Transform(female, chip('female mice\nwithout adaptive immune cells', GREY, size=26).move_to([0, 1.6, 0])), run_time=0.6)
        worked = T('hypersensitivity reversed', 29).move_to([0, -0.9, 0])
        self.at('the inhibitor worked')
        self.play(FadeIn(worked, shift=DOWN * 0.2), run_time=0.5)
        conditional = T('conditional route — it can switch', 28, font=TITLE_FONT).move_to([0, -2.3, 0])
        self.at('The route could switch')
        self.play(FadeIn(conditional), run_time=0.6)
        self.at('Compartment matters too')
        self.play(FadeOut(VGroup(female, inhibitor, worked, tested, conditional)),
                  Transform(head, heading('Compartment matters too · mice')), run_time=0.6)
        macrophages = chip('systemic macrophage depletion', GREY, size=28).move_to([0, 1.7, 0])
        both = T('hypersensitivity reduced\nin both sexes', 29).move_to([0, 0.35, 0])
        self.at('Depleting macrophages')
        self.play(FadeIn(macrophages), run_time=0.5)
        self.at('reduced hypersensitivity in both sexes')
        self.play(FadeIn(both, shift=DOWN * 0.2), run_time=0.6)
        ganglion = chip('ganglion macrophages\nfavoured by the authors', GREY, size=34, pad=0.32).move_to([-3.3, -1.4, 0])
        skin = chip('skin dendritic cells\ncould not be excluded', GREY, size=34, pad=0.32).move_to([3.3, -1.4, 0])
        self.at('The authors favored')
        self.play(FadeIn(ganglion), run_time=0.6)
        self.at('but could not exclude')
        self.play(FadeIn(skin), run_time=0.6)
        self.at('These animal findings')
        mapping = processing_map()
        caveat = T('Animal findings do not establish\na fixed human sex rule', 30, font=TITLE_FONT).move_to([0, -2.8, 0])
        self.play(FadeOut(VGroup(macrophages, both, ganglion, skin)),
                  Transform(head, heading('After nerve injury · preparation-specific findings')),
                  FadeIn(mapping), FadeIn(caveat), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Persistent pain after nerve injury can reflect altered processing at several levels."
