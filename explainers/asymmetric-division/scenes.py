"""Chapter 1: Two Jobs, One Division.

COLOR MAP (from scenes.old.py; shared across the chapter series)
YELLOW = Numb / inherited determinant; TEAL = Notch signal / hears Notch;
RED = inhibition / failed control; VIOLET = inner bristle fates (neuron, sheath);
ORANGE = outer bristle fates (hair, socket); GREY = neutral cells / unknown;
BLUE = neuroblast / self-renewal; GREEN = differentiating neural output;
GOLD = apical polarity; TEXT = other cargo / general labels.
Cell, crescent, arrow, and spindle geometry reuse the reference film's helpers.
No quantitative plots occur in this chapter; all curves below are cell schematics.
"""
import numpy as np
from bp_style import *

ORANGE = '#F29E4C'
VIOLET = '#A98BE0'
LESSON_TITLE = 'Asymmetric Division: Numb and the Neuroblast'


SOFT = '#BAC1CD'   # secondary-label grey, about 9:1 against BG (GREY itself stays the Notch-off colour)


def label(text, color=TEXT, x=0, y=0, size=28):
    if color == GREY:
        color = SOFT
    return T(text, size=max(26, size), color=color, line_spacing=1.15).move_to([x, y, 0])


def head(text):
    return label(text, TEXT, 0, 3.25, 32)


def cell(c, r, color=GREY, op=.22):
    return Circle(radius=r, stroke_color=color, stroke_width=4,
                  fill_color=color, fill_opacity=op).move_to(c)


def crescent(center, r, span=2, w=14):
    return Arc(radius=r, start_angle=PI-span/2, angle=span,
               arc_center=center, color=YELLOW, stroke_width=w)


def arr(a, b, color=GREY, w=4):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=.22,
                 max_tip_length_to_length_ratio=.5)


def callout(text, pos, target, color=TEXT, size=28):
    # Consistent fine leader, ending at the named feature rather than crossing it.
    t = label(text, color, *pos, size)
    end = np.array(target, float)
    start = t.get_boundary_point(end-t.get_center())
    line = Line(start, end, buff=.12, color=color, stroke_width=2)
    return VGroup(line, t)


def spindle(center=(0, 0, 0)):
    c = np.array(center, float)
    p, q = c+RIGHT*1.35, c- RIGHT*1.35
    return VGroup(*[VGroup(Line(p, c+UP*d, color=TEXT, stroke_width=4),
                           Line(c+UP*d, q, color=TEXT, stroke_width=4))
                    for d in (-.55, 0, .55)],
                  Dot(p, radius=.09, color=TEXT), Dot(q, radius=.09, color=TEXT))


def furrow():
    # A continuous membrane pinches toward the spindle midpoint from top and bottom.
    # Parametric cartoon geometry, not a measured trace or molecular structure.
    theta = np.linspace(0, TAU, 161)
    x = 2.25*np.cos(theta)
    y = 2.25*np.sin(theta)*(1-.92*np.exp(-(x/.7)**2))
    outline = VMobject(stroke_color=BLUE, stroke_width=4,
                       fill_color=BLUE, fill_opacity=.22)
    outline.set_points_smoothly(np.column_stack((x, y, np.zeros_like(x))))
    outline.close_path()
    return outline


def pair(y=.2, radius=1.55, colors=(BLUE, BLUE)):
    return VGroup(cell([-2.2, y, 0], radius, colors[0]),
                  cell([2.2, y, 0], radius, colors[1]))


def mother_rig():
    return cell([0, 0, 0], 2.25, BLUE), crescent([0, 0, 0], 2.08)


def neural_pair():
    return cell([0, 1, 0], 1.5, BLUE), cell([0, -1.8, 0], .8, GREEN)


def node(text, x, y, color=GREY, size=28):
    return chip(text, color, size=max(26, size)).move_to([x, y, 0])


def glial_note():
    return label('Adult lineage also makes a glial cell.', GREY, 0, -3.15, 26)


def tree():
    root = node('SOP', 0, 2.1, size=34)
    mids = VGroup(node('outer precursor (pIIa)', -3.15, .5),
                  node('inner precursor (pIIb)', 3.15, .5))
    e1 = VGroup(arr([-.4, 1.65, 0], [-3.15, .95, 0]),
                arr([.4, 1.65, 0], [3.15, .95, 0]))
    leaves = VGroup(node('hair cell', -4.7, -1.6, ORANGE),
                    node('socket cell', -1.6, -1.6, ORANGE),
                    node('neuron', 1.6, -1.6, VIOLET),
                    node('sheath cell', 4.7, -1.6, VIOLET))
    e2 = VGroup(*[arr([px, .05, 0], [x, -1.18, 0])
                   for px, x in [(-3.15, -4.7), (-3.15, -1.6), (3.15, 1.6), (3.15, 4.7)]])
    return root, mids, e1, leaves, e2


def tree_stage(level=3):
    r, m, e, l, e2 = tree()
    g = VGroup(r)
    if level >= 1:
        g.add(m, e)
    if level >= 2:
        g.add(l[:2], e2[:2])
    if level >= 3:
        g.add(l[2:], e2[2:])
    return g


def bristle():
    skin = VGroup(Line([-5.3, -.35, 0], [-1.3, -.35, 0], color=GREY, stroke_width=7),
                  Line([1.3, -.35, 0], [5.3, -.35, 0], color=GREY, stroke_width=7))
    shaft = Polygon([-.36, -.35, 0], [.4, -.35, 0], [1.1, 2.8, 0],
                    stroke_color=ORANGE, fill_color=ORANGE, fill_opacity=.45)
    socket = Ellipse(width=2.5, height=.75, color=ORANGE).move_to([0, -.35, 0])
    return VGroup(skin, shaft, socket)


def questions(n):
    texts = ['How can sisters born side by side differ?',
             'What does the inherited protein do?',
             'How does the mother put it on one side?',
             'What happens when the sorting fails?']
    rows = VGroup()
    for i, text in enumerate(texts[:n]):
        y = -.45-i*.87
        t = label(text, TEXT, 0, y, 28).align_to([-4.65, y, 0], LEFT)
        rows.add(VGroup(label(str(i+1), YELLOW, -5.25, y, 28), t))
    return rows


def mini_maps(scale=1.0, center=None):
    # Two thumbnail maps, each labelled; scaled about its own centre and placed side by side.
    sop = cell([-3.25, 2.7, 0], .28)
    a = VGroup(sop,
               *[Line([-3.25, 2.42, 0], [x, 1.98, 0], color=GREY) for x in (-4.2, -2.3)],
               *[cell([x, 1.8, 0], .23) for x in (-4.2, -2.3)],
               *[Line([px, 1.57, 0], [x, 1.04, 0], color=GREY)
                 for px, x in [(-4.2, -4.75), (-4.2, -3.65), (-2.3, -2.85), (-2.3, -1.75)]],
               *[cell([x, .8, 0], .25, ORANGE if x < -3.25 else VIOLET)
                 for x in (-4.75, -3.65, -2.85, -1.75)])
    nb = cell([3.2, 2.1, 0], .8, BLUE)
    gm = cell([3.2, .65, 0], .38, GREEN)
    b = VGroup(nb, gm)
    ta = VGroup(label('Bristle', GREY, -3.25, 3.4, 28))
    tb = VGroup(label('Neuroblast', BLUE, 3.2, 3.4, 28))
    # small tags beside the nodes they name
    tags_a = VGroup(label('SOP', GREY, -2.45, 2.7, 26),
                    label('pIIa', GREY, -5.1, 1.8, 26),
                    label('pIIb', GREY, -1.45, 1.8, 26))
    tags_b = VGroup(label('GMC', GREEN, 4.35, .65, 26))
    ga = VGroup(a, ta, tags_a)
    gb = VGroup(b, tb, tags_b)
    out = VGroup(ga, gb)
    if center is not None:
        for g, cx in ((ga, -3.3), (gb, 3.1)):
            g.scale(scale)
            g.move_to([cx, center, 0])
    return out


class S00Title(TitleCard):
    LESSON = LESSON_TITLE
    TITLE = 'Two Jobs, One Division'

    def construct(self):
        g = VGroup(T('BIOCHEMISTRYPEDIA', 26, TEAL),
                   T(self.LESSON, 26, GREY),
                   T(self.TITLE, 50, TEXT, font=TITLE_FONT),
                   Line(LEFT*1.3, RIGHT*1.3, color=GOLD, stroke_width=4)).arrange(DOWN, buff=.4)
        self.play(FadeIn(g), run_time=.6)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        m = cell([-3, .4, 0], 1.8, BLUE)
        self.at('A stem cell')
        self.play(FadeIn(m), FadeIn(label('stem cell', BLUE, -3, .4, 32)), run_time=.5)
        self.at('stay a stem cell')
        self.play(GrowArrow(arr([-1.1, .95, 0], [.65, 1.3, 0], BLUE)),
                  FadeIn(node('stay a stem cell', 3, 1.3, BLUE, 30)), run_time=.4)
        self.at('make cells that differentiate')
        self.play(GrowArrow(arr([-1.1, -.2, 0], [.65, -.8, 0], GREEN)),
                  FadeIn(node('make cells that\ndifferentiate', 3, -.8, GREEN, 28)), run_time=.4)
        self.at('How can one division')
        self.play(FadeIn(label('How can one division do both?', TEXT, 0, -2.7, 32)), run_time=.5)
        self.finish()


class S02Symmetric(SpokenScene):
    def construct(self):
        m = cell([0, .2, 0], 1.8, BLUE)
        self.add(m, head('Symmetric'))
        self.at('In a symmetric division')
        # Separate daughters start small and grow without crossing outlines.
        p = pair()
        self.play(m.animate.stretch(.55, 0), run_time=.35)
        self.play(FadeOut(m), run_time=.15)
        self.play(GrowFromCenter(p[0]), GrowFromCenter(p[1]), run_time=.7)
        self.at('the daughters are alike')
        self.play(Indicate(p, color=BLUE, scale_factor=1.02), run_time=.4)
        self.finish()
        self.wait(1)


class S03GrowSpend(SpokenScene):
    def construct(self):
        lm = cell([-3.2, 0, 0], 1.3, BLUE)
        rm = cell([3.2, 0, 0], 1.3, BLUE)
        lc = label('Progenitor pool: 1', BLUE, -3.2, -2.2, 28)
        rc = label('Progenitor pool: 1', BLUE, 3.2, -2.2, 28)
        self.add(lm, rm, lc, rc)
        self.at('Two progenitors')
        left = VGroup(cell([-4.65, 0, 0], 1.25, BLUE), cell([-1.85, 0, 0], 1.25, BLUE))
        self.play(ReplacementTransform(lm, left), FadeIn(label('Progenitors', BLUE, -3.2, 2.2, 30)), run_time=.7)
        self.at('enlarge the pool')
        self.play(Transform(lc, label('Progenitor pool: 1 → 2', BLUE, -3.2, -2.2, 28)), run_time=.4)
        self.at('Two differentiating cells')
        right = VGroup(cell([1.85, 0, 0], 1.25, GREEN), cell([4.65, 0, 0], 1.25, GREEN))
        self.play(ReplacementTransform(rm, right), FadeIn(label('Differentiating cells', GREEN, 3.2, 2.2, 28)), run_time=.7)
        self.at('spend it')
        self.play(Transform(rc, label('Progenitor pool: 1 → 0', GREEN, 3.2, -2.2, 28)), run_time=.4)
        self.finish()


class S04Asymmetric(SpokenScene):
    def construct(self):
        m = cell([0, .4, 0], 1.8, BLUE)
        self.add(m)
        self.at('In an asymmetric division')
        p = pair(radius=1.3)
        self.play(ReplacementTransform(m, p), run_time=.8)
        self.at('different fates')
        self.play(p[1].animate.set_stroke(GREEN).set_fill(GREEN, .3), FadeIn(head('Asymmetric')), run_time=.5)
        self.at('one stays a progenitor')
        self.play(FadeIn(label('progenitor', BLUE, -2.2, -1.65, 28)), run_time=.4)
        self.at('the other moves')
        self.play(p[1].animate.shift(RIGHT*1.65),
                  GrowArrow(arr([1.8, -1.65, 0], [3.85, -1.65, 0], GREEN)),
                  FadeIn(label('toward a fate', GREEN, 3.85, -2.2, 28)), run_time=.8)
        self.play(FadeIn(label('Progenitor pool: 1 → 1', BLUE, 0, -3.1, 28)), run_time=.3)
        self.finish()


class S05Inside(SpokenScene):
    def construct(self):
        m, c = mother_rig()
        self.add(m, head('From inside'))
        self.at('can be built from inside')
        self.play(FadeIn(label('mother cell', BLUE, 0, -2.9, 28)), run_time=.4)
        patches = VGroup(*[Dot([2.05*np.cos(a), 2.05*np.sin(a), 0], radius=.12, color=YELLOW)
                           for a in np.linspace(0, 2*PI, 7, endpoint=False)])
        self.at('The mother gathers a protein')
        self.play(FadeIn(patches),
                  FadeIn(callout('cortex', (-3.7, 1.1), [-2.05, .65, 0])),
                  FadeIn(label('layer just under\nthe membrane', TEXT, .15, -.3, 28)), run_time=.35)
        self.at('on one side')
        self.play(*[d.animate.move_to([2.08*np.cos(a), 2.08*np.sin(a), 0])
                    for d, a in zip(patches, np.linspace(PI-1, PI+1, 7))], run_time=.6)
        self.play(FadeOut(patches), Create(c), run_time=.25)
        self.finish()


class S06Determinant(SpokenScene):
    def construct(self):
        m, c = mother_rig()
        self.add(m, c)
        self.at('That protein is called a determinant')
        d = callout('determinant', (-4, 1.5), [-1.85, 1, 0], YELLOW)
        self.play(FadeIn(d), run_time=.4)
        self.at('The mother lines its spindle up')
        sp = spindle().rotate(PI/3)
        sl = callout('spindle', (3.45, 1.1), [1.15, .15, 0])
        self.play(Create(sp), run_time=.3)
        self.play(Rotate(sp, -PI/3), FadeIn(sl), run_time=.65)
        self.at('so only one daughter')
        self.play(Transform(m, furrow()), run_time=.45)
        p = pair(radius=1.45)
        self.play(FadeOut(sp), FadeOut(sl), ReplacementTransform(m, p),
                  Transform(c, crescent([-2.2, .2, 0], 1.3)),
                  Transform(d, callout('determinant', (-4.5, 2), [-3.15, 1, 0], YELLOW)), run_time=.65)
        self.at('inherits it')
        self.play(FadeIn(label('inherits it', YELLOW, -2.2, -1.9, 28)), run_time=.35)
        self.finish()


class S07Outside(SpokenScene):
    def construct(self):
        niche = VGroup(*[RoundedRectangle(width=1.5, height=.9, corner_radius=.18,
                           color=GREY, fill_color=GREY, fill_opacity=.22).move_to([x, 1.95, 0])
                         for x in (-4, -2.4, -.8)])
        p = VGroup(cell([-2.4, .25, 0], 1.25, BLUE), cell([.25, .25, 0], 1.25, BLUE))
        self.at('it can come from outside')
        self.play(FadeIn(niche), FadeIn(p), FadeIn(head('From outside')), run_time=.5)
        self.at('Only one daughter stays touching')
        self.play(p[1].animate.move_to([3.6, -.7, 0]).set_stroke(GREEN).set_fill(GREEN, .3),
                  FadeIn(callout('stem cell', (-3.9, -1.75), [-2.8, -.8, 0], BLUE)),
                  FadeIn(callout('differentiate', (3.6, -2.5), [3.6, -1.95, 0], GREEN)), run_time=.85)
        self.at('a niche')
        self.play(FadeIn(callout('niche', (-5.4, 2.65), [-4.35, 2.35, 0], GREY)), run_time=.3)
        self.at('cells that signal it')
        self.play(GrowArrow(arr([-1.4, 1.55, 0], [-1.8, 1.15, 0], BLUE)),
                  FadeIn(callout('signal: stay a stem cell', (2.7, 1.7), [-1.5, 1.35, 0], BLUE, 26)), run_time=.4)
        self.finish()


class S08Map1(SpokenScene):
    def construct(self):
        self.at('Our first map')
        self.play(FadeIn(bristle()), run_time=.55)
        self.at('a fly bristle')
        self.play(FadeIn(head('Map 1 · Fly bristle')), run_time=.4)
        self.at('a small sense organ')
        self.play(FadeIn(label('four cells', TEXT, 0, -2.4, 30)), run_time=.4)
        self.finish()


class S09Cells(SpokenScene):
    def construct(self):
        self.add(bristle())
        neuron = cell([0, -2, 0], .62, VIOLET)
        sheath = Ellipse(width=2.6, height=2.05, color=VIOLET, stroke_width=4,
                         fill_color=VIOLET, fill_opacity=.12).move_to([0, -2, 0])
        self.at('neuron')
        self.play(FadeIn(neuron), FadeIn(callout('neuron', (-2.6, -2.55), [-.6, -2.25, 0], VIOLET)), run_time=.35)
        self.at('a sheath cell')
        self.play(Create(sheath), FadeIn(callout('sheath cell', (2.8, -2.2), [1.3, -2, 0], VIOLET)), run_time=.45)
        self.at('two outer cells')
        hair = cell([-1.1, 1.2, 0], .57, ORANGE)
        socket = cell([1.9, .45, 0], .57, ORANGE)
        self.play(FadeIn(hair), FadeIn(socket),
                  Create(Line(hair.get_right(), [.25, 1.2, 0], color=ORANGE, stroke_width=2)),
                  Create(Line([1.5, .05, 0], [.9, -.15, 0], color=ORANGE, stroke_width=2)), run_time=.35)
        self.at('build the hair')
        self.play(FadeIn(callout('hair cell', (-3.1, 1.6), [-1.65, 1.35, 0], ORANGE)), run_time=.25)
        self.at('and socket')
        self.play(FadeIn(callout('socket cell', (4, .9), [2.45, .6, 0], ORANGE)), run_time=.25)
        self.finish()
        self.wait(.9)


class S10Sop(SpokenScene):
    def construct(self):
        r = tree()[0].scale(1.5)
        self.add(r, head('Classic simplified map'), glial_note())
        self.at('all four come from one')
        self.play(Indicate(r, scale_factor=1.1), run_time=.5)
        self.at('sensory organ precursor')
        self.play(FadeIn(label('sensory organ precursor', TEXT, 0, .9, 30)), run_time=.4)
        self.at('in three divisions')
        self.play(FadeIn(label('three divisions', TEXT, 0, -.5, 30)), run_time=.4)
        self.finish()


class S11Branches(SpokenScene):
    def construct(self):
        r, m, e, l, e2 = tree()
        self.add(head('Classic simplified map'), r, glial_note())
        self.at('The precursor makes an outer precursor')
        self.play(GrowArrow(e[0]), FadeIn(m[0]), run_time=.6)
        self.at('and an inner precursor')
        self.play(GrowArrow(e[1]), FadeIn(m[1]), run_time=.6)
        self.at('The outer one makes')
        self.play(Create(e2[:2]), run_time=.45)
        self.at('the hair cell')
        self.play(FadeIn(l[0]), run_time=.35)
        self.at('and the socket cell')
        self.play(FadeIn(l[1]), run_time=.35)
        self.finish()


class S12Inner(SpokenScene):
    def construct(self):
        self.add(head('Classic simplified map'), tree_stage(2), glial_note())
        r, m, e, l, e2 = tree()
        self.at('The inner one makes')
        self.play(Create(e2[2:]), run_time=.4)
        self.at('the neuron')
        self.play(FadeIn(l[2]), run_time=.3)
        self.at('and the sheath cell')
        self.play(FadeIn(l[3]), run_time=.3)
        self.finish()


class S13NotchLabels(SpokenScene):
    def construct(self):
        g = tree_stage()
        h = head('Hears Notch?')
        self.add(g, glial_note().move_to([0, -3.35, 0]))
        self.at('At each division')
        self.play(FadeIn(h), run_time=.3)
        # Sister ties below each row: each blank belongs to the tie, not a node.
        ties = VGroup()
        for x1, x2, y in [(-1.5, 1.5, -.1), (-4.7, -1.6, -2.2), (1.6, 4.7, -2.2)]:
            tie = VMobject(color=GREY, stroke_width=2).set_points_as_corners(
                [[x1, y+.13, 0], [x1, y, 0], [x2, y, 0], [x2, y+.13, 0]])
            t = node('hears Notch?', (x1+x2)/2, y-.38, GREY, 26)
            # Opaque background keeps the upper tie's caption clear of descending edges.
            t[0].set_fill(BG, 1)
            ties.add(tie, t)
        self.at('one sister hears a signal')
        self.play(FadeIn(ties), run_time=.45)
        self.at('and the other does not')
        k1 = label('Key:  Notch-on', TEAL, 0, 0, 26).move_to([4.7, 3.0, 0], aligned_edge=RIGHT)
        k2 = label('Notch-off', GREY, 0, 0, 26)
        k1.to_corner(UR, buff=.45).shift(DOWN*.05)
        k2.next_to(k1, DOWN, buff=.15, aligned_edge=RIGHT)
        self.play(FadeIn(k1), FadeIn(k2), run_time=.4)
        self.at('Which is which')
        self.play(Transform(h, head('Which is which?')), run_time=.4)
        self.finish()


class S14Map2(SpokenScene):
    def construct(self):
        sheet = VGroup(*[RoundedRectangle(width=1.45, height=1.25, corner_radius=.12,
                          color=GREY, fill_color=GREY, fill_opacity=.15).move_to([x, 1.6, 0])
                        for x in (-4.8, -3.2, -1.6, 1.6, 3.2, 4.8)])
        nb = cell([0, 1.6, 0], .62, BLUE)
        self.at('Our second map')
        self.play(FadeIn(sheet), FadeIn(nb), FadeIn(head('Map 2 · Neuroblast')),
                  FadeIn(label('epithelium (sheet of cells)', GREY, 0, 2.65, 26)), run_time=.4)
        self.at('is a neuroblast')
        nl = label('neuroblast', BLUE, -3.0, -.8, 32)
        nline = Line([-1.95, -.8, 0], [-1.3, -.8, 0], color=BLUE, stroke_width=2)
        self.play(nb.animate.move_to([0, -.8, 0]).scale(1.9), FadeIn(nl, shift=RIGHT*.3),
                  FadeIn(nline), run_time=1)
        self.at('a stem cell')
        self.play(FadeIn(callout('stem cell', (2.7, -.8), [1.3, -.8, 0], BLUE, 30)), run_time=.4)
        self.at('central nervous system')
        self.play(FadeIn(label('fly central nervous system', GREY, 0, -2.8, 28)), run_time=.4)
        self.finish()


class S15Type1(SpokenScene):
    def construct(self):
        m = cell([0, 0, 0], 2.05, BLUE)
        self.add(m)
        self.at('In most neuroblasts')
        self.play(FadeIn(head('Most neuroblasts')), run_time=.3)
        self.at('each division is unequal')
        nb, gmc = neural_pair()
        self.play(ReplacementTransform(m, nb), FadeIn(gmc, shift=DOWN*.4), run_time=.85)
        self.play(FadeIn(callout('apical (top)', (-3, 2.1), [-.85, 2.2, 0], GREY)),
                  FadeIn(callout('basal (bottom)', (-3, -2.3), [-.75, -2, 0], GREY)), run_time=.3)
        self.at('The large top daughter')
        self.play(FadeIn(callout('neuroblast', (3, 1), [1.5, 1, 0], BLUE, 32)), run_time=.4)
        self.finish()


class S16Gmc(SpokenScene):
    def construct(self):
        nb, gmc = neural_pair()
        self.add(nb, gmc, callout('neuroblast', (3, 1), [1.5, 1, 0], BLUE, 32))
        self.at('The small bottom daughter')
        gl = callout('ganglion mother cell\n(GMC)', (3.4, -1.8), [.8, -1.8, 0], GREEN, 28)
        self.play(FadeIn(gl), run_time=.45)
        self.at('It divides once more')
        ds = VGroup(cell([-.95, -1.85, 0], .7, GREEN), cell([.95, -1.85, 0], .7, GREEN))
        self.play(Transform(gl, callout('GMC divides once', (3.7, -1.5), [1.6, -1.7, 0], GREEN, 26)),
                  ReplacementTransform(gmc, ds), run_time=.9)
        self.at('into two neurons or glia')
        self.play(FadeIn(label('neuron or glia', GREEN, 0, -3, 28)), run_time=.4)
        self.finish()


class S17Counter(SpokenScene):
    def construct(self):
        nb = cell([0, 1.55, 0], 1.12, BLUE)
        count = label('Neuroblasts: 1', BLUE, 0, 3.15, 28)
        gc = label('Cumulative GMCs produced: 0', GREEN, 0, -3.25, 28)
        self.add(nb, count, gc)

        def division(i, x):
            # 1.5 s per neuroblast division, then a separately paced GMC division.
            g = cell([0, .5, 0], .2, GREEN)
            self.play(nb.animate.stretch(1.06, 1), GrowFromCenter(g), run_time=.5)
            link = Line([0, .45, 0], [0, .45, 0], color=GREEN, stroke_width=3)
            self.add(link)
            tag = label('GMC', GREEN, x, -2.35, 26)
            end = [x, -.2, 0]
            self.play(g.animate.scale(4.25).move_to([x, -1.05, 0]),
                      link.animate.put_start_and_end_on([0, .45, 0], end),
                      nb.animate.stretch(1/1.06, 1), run_time=.6)
            self.play(Transform(count, label('Neuroblasts: '+' → '.join(['1']*(i+2)), BLUE, 0, 3.15, 28)),
                      Transform(gc, label(f'Cumulative GMCs produced: {i+1}', GREEN, 0, -3.25, 28)),
                      FadeIn(tag), run_time=.4)
            return g, tag, x, link

        def gmc_divides(g, tag, x, link):
            ds = VGroup(cell([x-.85, -1.3, 0], .72, GREEN), cell([x+.85, -1.3, 0], .72, GREEN))
            self.play(ReplacementTransform(g, ds),
                      link.animate.put_start_and_end_on([0, .45, 0], [x, -.58, 0]),
                      Transform(tag, label('GMC → two cells', GREEN, x, -2.35, 26)), run_time=.65)

        self.at('Division after division')
        first = division(0, -3.5)
        self.at('the neuroblast stays one neuroblast')
        gmc_divides(*first)
        second = division(1, 0)
        self.at('Each division adds one')
        gmc_divides(*second)
        third = division(2, 3.5)
        self.at('which divides once')
        gmc_divides(*third)
        self.finish()


class S18Puzzles(SpokenScene):
    def construct(self):
        self.at('These maps raise four puzzles')
        self.play(FadeIn(mini_maps(1.4, 1.2)), run_time=.45)
        self.at('How can two sisters')
        self.play(FadeIn(questions(1).shift(DOWN*1.95)), run_time=.5)
        self.finish()


class S19Puzzles2(SpokenScene):
    def construct(self):
        big = mini_maps(1.4, 1.2)
        q1 = questions(1).shift(DOWN*1.95)
        self.add(big, q1)
        qs = questions(4)
        # The maps settle upward and the first puzzle rises with them to make room for the list.
        self.play(Transform(big, mini_maps(1.15, 1.8)), q1.animate.shift(UP*1.95), run_time=.6)
        self.at('What does the inherited protein do')
        self.play(FadeIn(qs[1]), run_time=.45)
        self.at('How does the mother')
        self.play(FadeIn(qs[2]), run_time=.45)
        self.at('And what happens')
        self.play(FadeIn(qs[3]), run_time=.45)
        self.finish()


class S20Rule(SpokenScene):
    def construct(self):
        m, c = mother_rig()
        self.add(m)
        self.at('Here is the idea to carry')
        self.play(FadeIn(head('The idea to carry')), run_time=.4)
        self.at('mother puts a protein')
        self.play(Create(c), run_time=.6)
        self.at('called numb')
        self.play(FadeIn(callout('Numb', (-3.8, 1.2), [-1.9, .8, 0], YELLOW, 32)), run_time=.4)
        self.at('and aims')
        sp = spindle().rotate(PI/3)
        self.play(Create(sp), run_time=.3)
        self.play(Rotate(sp, -PI/3), FadeIn(callout('spindle', (3.5, 1.1), [1.15, .15, 0])), run_time=.7)
        self.finish()


def notch_result():
    p = pair(radius=1.45, colors=(GREY, TEAL))
    p[0].set_fill(GREY, .4)
    p[1].set_fill(TEAL, .3)
    c = crescent([-2.2, .2, 0], 1.3)
    return p, c


class S21Rule2(SpokenScene):
    def construct(self):
        m, c = mother_rig()
        sp = spindle()
        self.add(m, c, sp)
        self.at('The daughter that inherits numb')
        p = pair(radius=1.45, colors=(BLUE, BLUE))
        self.play(FadeOut(sp), ReplacementTransform(m, p),
                  Transform(c, crescent([-2.2, .2, 0], 1.3)), run_time=.7)
        nl = callout('Numb', (-2.1, .1), [-3.45, .2, 0], YELLOW, 28)
        self.play(FadeIn(nl), run_time=.25)
        self.at('cannot hear notch')
        # Signal from the Numb sister to the unblocked sister, across the intercell gap.
        outward = arr([-.7, .8, 0], [.95, .8, 0], TEAL)
        # Reciprocal signal from the sister loops above the cells to the Numb crescent on the far left.
        route = VMobject(color=TEAL, stroke_width=4).set_points_as_corners(
            [[2.2, 1.7, 0], [2.2, 2.5, 0], [-5.0, 2.5, 0], [-5.0, .2, 0]])
        incoming = arr([-5.0, .2, 0], [-4.15, .2, 0], TEAL)
        # Thick red bar sits on the membrane directly outside the Numb crescent.
        block = Line([-3.9, -.55, 0], [-3.9, .95, 0], color=RED, stroke_width=26)
        bl = callout('blocked by Numb', (-3.1, 2.0), [-3.9, 1.05, 0], RED, 26)
        self.play(Create(route), GrowArrow(incoming), GrowArrow(outward),
                  FadeIn(label('Notch', TEAL, 0, 1.35, 28)),
                  FadeIn(label('Notch signal', TEAL, -1.4, 2.95, 28)),
                  FadeIn(label('When a Notch signal is on offer', GREY, 0, -3.25, 26)), run_time=.45)
        self.play(Create(block), FadeIn(bl), run_time=.3)
        self.play(p[0].animate.set_stroke(GREY).set_fill(GREY, .4), p[1].animate.set_stroke(TEAL).set_fill(TEAL, .3),
                  FadeIn(label('cannot hear Notch', GREY, -2.2, -1.8, 28)),
                  FadeIn(label('hears Notch', TEAL, 2.2, -1.8, 28)), run_time=.35)
        self.at('So it takes')
        self.play(FadeIn(label('Notch-off fate', GREY, -2.2, -2.55, 28)), run_time=.4)
        self.at('This holds where')
        self.play(Indicate(route, color=TEAL, scale_factor=1), run_time=.4)
        self.finish()


def takeaway_steps():
    m = cell([-4.5, .5, 0], 1.15, BLUE, .3)
    c = crescent([-4.5, .5, 0], 1.02)
    m2 = cell([-.9, .5, 0], 1.15, BLUE, .3)
    c2 = crescent([-.9, .5, 0], 1.02)
    sp = spindle([-.9, .5, 0]).scale(.7, about_point=[-.9, .5, 0])
    ds = VGroup(cell([2.4, .5, 0], .85, GREY, .4), cell([4.8, .5, 0], .85, TEAL, .3),
                crescent([2.4, .5, 0], .73))
    return VGroup(m, c), VGroup(m2, c2, sp), ds


def takeaway():
    a, b, c = takeaway_steps()
    return VGroup(head('One division can do both jobs.'), a, b, c,
                  arr([-3.05, .5, 0], [-2.35, .5, 0]), arr([.55, .5, 0], [1.25, .5, 0]),
                  label('mark a side', YELLOW, -4.5, -1.15, 28),
                  label('aim spindle', TEXT, -.9, -1.15, 28),
                  label('inherits Numb', YELLOW, 2.4, -1.15, 26),
                  label('does not', TEXT, 4.8, -1.15, 26),
                  label('One daughter inherits the determinant.', TEXT, 0, -2.55, 30))


class S22Takeaway(SpokenScene):
    def construct(self):
        p, c = notch_result()
        inheritance = VGroup(label('inherits Numb', YELLOW, -2.2, -1.85, 28),
                             label('does not', TEXT, 2.2, -1.85, 28))
        self.add(p, c, inheritance)
        self.at('One division can do both jobs')
        self.play(FadeIn(head('One division can do both jobs.')), run_time=.4)
        self.at('if the mother marks a side')
        a, b, ds = takeaway_steps()
        self.play(FadeOut(p), FadeOut(c), FadeOut(inheritance), FadeIn(a),
                  FadeIn(label('mark a side', YELLOW, -4.5, -1.15, 28)), run_time=.4)
        self.play(GrowArrow(arr([-3.05, .5, 0], [-2.35, .5, 0])), FadeIn(b),
                  FadeIn(label('aim spindle', TEXT, -.9, -1.15, 28)), run_time=.5)
        self.at('only one daughter inherits it')
        self.play(GrowArrow(arr([.55, .5, 0], [1.25, .5, 0])), FadeIn(ds),
                  FadeIn(label('inherits Numb', YELLOW, 2.4, -1.15, 26)),
                  FadeIn(label('does not', TEXT, 4.8, -1.15, 26)),
                  FadeIn(label('One daughter inherits the determinant.', TEXT, 0, -2.55, 30)), run_time=.5)
        self.finish()


class S23End(EndCard):
    LINE = 'One division can do both jobs.'

    def construct(self):
        self.add(takeaway())
        self.finish()
