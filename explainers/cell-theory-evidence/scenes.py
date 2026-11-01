"""Cell theory: cellular unity, division and the evidence supporting them.

COLOR MAP (retained from the original film)
  BLUE = cells, cell walls and tissues
  ORANGE = DNA (labelled blocks, never molecular structures)
  PINK = metabolism
  TEAL = tools and their resolving ability
  PURPLE = stain and the nucleus it reveals
  YELLOW = highlights and ideas being named
  GREEN = visible / resolved / supported by evidence
  RED = unresolved detail / rejected model
  GREY = context and de-emphasized outlines
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E58FB0"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def btext(text, size=24, color=GREY, **kw):
    t = T(text, size, color, **kw)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.12, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    return VGroup(back, t)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cellc(r=0.4, color=BLUE, op=0.15, sw=3.5):
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op)


def dna_block(w=1.3):
    """DNA as a plain labelled block (no structure drawn)."""
    box = RoundedRectangle(corner_radius=0.1, width=w, height=0.6, stroke_color=ORANGE, stroke_width=3,
                           fill_color=ORANGE, fill_opacity=0.25)
    lab = T("DNA", 26, ORANGE, weight=BOLD).move_to(box)
    return VGroup(box, lab)


def tissue(plant=True):
    # Reuse the old cork rectangles and tissue-cell circles, with six cells.
    cells = VGroup()
    for r in range(2):
        for c in range(3):
            shape = (Rectangle(width=0.85, height=0.72, stroke_color=BLUE,
                               stroke_width=3, fill_color=BLUE, fill_opacity=0.13)
                     if plant else cellc(0.38))
            cells.add(shape.move_to([(c-1)*0.88, (0.5-r)*0.76, 0]))
    return cells


def microbe(archaeon=False):
    if archaeon:
        return Ellipse(width=1.8, height=1.35, stroke_color=BLUE,
                       stroke_width=4, fill_color=BLUE, fill_opacity=0.15)
    return RoundedRectangle(width=2.1, height=0.95, corner_radius=0.45,
                            stroke_color=BLUE, stroke_width=4,
                            fill_color=BLUE, fill_opacity=0.15)


def examples(y=0):
    shapes = [tissue(True), tissue(False), microbe(), microbe(True)]
    labels = ['plant', 'animal', 'bacterium', 'archaeon']
    return VGroup(*[VGroup(s.move_to([x, y, 0]),
                           T(l, 26, BLUE).move_to([x, y-1.25, 0]))
                    for s, l, x in zip(shapes, labels, [-4.8, -1.6, 1.6, 4.8])])


def daughters():
    return VGroup(cellc(1.25, sw=5).move_to([-1.8, 0, 0]),
                  cellc(1.25, sw=5).move_to([1.8, 0, 0]))


def clear(scene):
    scene.play(*[FadeOut(m) for m in list(scene.mobjects)], run_time=0.45)


class S00Title(TitleCard):
    LESSON = "The cell theory and its evidence"
    TITLE = "Cells: The Basic Units of Life"

    def construct(self):
        title = T(self.TITLE, 44, font=TITLE_FONT).move_to([0, 2.65, 0])
        rule = Line([-1.2, 2.05, 0], [1.2, 2.05, 0], color=GOLD, stroke_width=4)
        # Simple organism silhouettes with highlighted cellular patches.
        stem = Line([-4, -0.9, 0], [-4, 1.1, 0], color=GREY, stroke_width=5)
        leaves = VGroup(*[Ellipse(width=1.0, height=0.4, color=GREY).rotate(a).move_to([x,y,0])
                          for x,y,a in [(-4.4,0.6,-0.5),(-3.6,0.2,0.5)]])
        plant = VGroup(stem, leaves, tissue(True).scale(0.45).move_to([-4,-1.2,0]),
                       T('plant',26,BLUE).move_to([-4,-2.2,0]))
        animal = VGroup(Ellipse(width=1.9,height=1.0,color=GREY).move_to([0,0,0]),
                        Circle(radius=0.42,color=GREY).move_to([0.95,0.6,0]),
                        tissue(False).scale(0.45).move_to([0,-1.2,0]),
                        T('animal',26,BLUE).move_to([0,-2.2,0]))
        bacterium = VGroup(microbe().move_to([4,0,0]), T('bacterium',26,BLUE).move_to([4,-2.2,0]))
        self.play(FadeIn(title), Create(rule), FadeIn(plant), FadeIn(animal), FadeIn(bacterium), run_time=1.0)
        self.play(Indicate(plant[2],color=YELLOW), Indicate(animal[2],color=YELLOW),
                  Indicate(bacterium[0],color=YELLOW),run_time=0.7)
        self.finish()


class S01Cork(SpokenScene):
    def construct(self):
        headline = T('All living organisms are made of cells', 36, font=TITLE_FONT).move_to([0,2.8,0])
        ex = examples()
        self.at('Every living organism')
        self.play(FadeIn(headline), FadeIn(ex[:2]), run_time=0.8)
        self.at('Cells are the basic unit')
        one = cellc(1.45, sw=5)
        rule = T('Cells are the basic unit of life', 34, YELLOW).move_to([0,-2.7,0])
        self.play(FadeOut(ex[:2]), GrowFromCenter(one), FadeIn(rule), run_time=0.9)
        self.at('the processes of life')
        self.play(Indicate(one, color=YELLOW), run_time=0.7)
        self.at('This connects living things')
        self.play(FadeOut(one), FadeIn(ex[:2]), run_time=0.8)
        self.at('Plants and animals')
        self.play(Indicate(ex[0][0],color=YELLOW),Indicate(ex[1][0],color=YELLOW),run_time=0.8)
        self.at('So are bacteria')
        self.play(FadeIn(ex[2:]), run_time=0.8)
        self.at('Their cells differ')
        self.play(*[Indicate(e[0], color=YELLOW, scale_factor=1.08) for e in ex], run_time=1.0)
        self.at('but cells are what')
        self.play(*[e[0].animate.set_stroke(BLUE,5) for e in ex],run_time=0.6)
        self.finish()


class S02Division(SpokenScene):
    def construct(self):
        title = T('New cells arise from existing cells',36,font=TITLE_FONT).move_to([0,2.8,0])
        cell = cellc(1.6,sw=5)
        label = T('existing cell',28,BLUE).move_to([0,-2.3,0])
        self.at('Every new cell')
        self.play(FadeIn(title),GrowFromCenter(cell),FadeIn(label),run_time=0.8)
        self.at('New cells form')
        elongated = Ellipse(width=4.1,height=2.5,stroke_color=BLUE,stroke_width=5,fill_color=BLUE,fill_opacity=0.15)
        self.play(Transform(cell,elongated),run_time=0.65)
        self.at('existing cells divide')
        pair = daughters()
        self.play(ReplacementTransform(cell,pair),Transform(label,T('cell division',28,BLUE).move_to(label)),run_time=1.0)
        self.at('connects living things')
        self.play(Indicate(pair,color=YELLOW,scale_factor=1.06),run_time=0.8)
        self.finish()


class S02Six(SpokenScene):
    def construct(self):
        title = T('The cell theory: six ideas',36,YELLOW,font=TITLE_FONT).move_to([0,2.9,0])
        pair = daughters()
        established = T('Organisms contain cells  •  Basic units of life  •  Cells divide',24,GREY).move_to([0,-2.9,0])
        self.at('The cell theory')
        self.play(FadeIn(title),FadeIn(pair),FadeIn(established),run_time=0.7)
        self.at('The other three')
        cell = cellc(2.15,sw=5).move_to([0,-0.1,0])
        self.play(ReplacementTransform(pair,cell),run_time=0.8)
        self.at('Metabolism happens inside')
        met = T('Metabolism inside cells',32,PINK).move_to([0,2.9,0])
        self.play(Transform(title,met),run_time=0.5)
        self.at('breaking down sugar')
        sugar = bchip('sugar',PINK,26).move_to([0,0.65,0])
        self.play(FadeIn(sugar),run_time=0.5)
        self.at('to release energy')
        energy = bchip('energy for cell use',PINK,26).move_to([0,-0.9,0])
        arrow = arr([0,0.2,0],[0,-0.4,0],PINK)
        self.play(GrowArrow(arrow),FadeIn(energy),run_time=0.8)
        self.at('carries hereditary information')
        dna = dna_block().move_to(cell)
        self.play(FadeOut(sugar),FadeOut(arrow),FadeOut(energy),FadeIn(dna),
                  Transform(title,T('DNA carries hereditary information',32,ORANGE).move_to(title)),run_time=0.7)
        self.at('When a cell divides')
        dna2 = dna.copy().shift(RIGHT*0.75)
        self.play(dna.animate.shift(LEFT*0.75),FadeIn(dna2),run_time=0.7)
        self.at('each new cell gets')
        pair = daughters()
        self.play(ReplacementTransform(cell,pair),dna.animate.move_to(pair[0]),dna2.animate.move_to(pair[1]),run_time=1.0)
        self.at('Cells also share')
        self.play(FadeOut(dna),FadeOut(dna2),FadeOut(established),
                  Transform(title,T('Shared molecular categories',34,YELLOW).move_to(title)),
                  Transform(pair[0],cellc(1.65,sw=5).move_to([-3.4,0,0])),
                  Transform(pair[1],RoundedRectangle(width=3.8,height=2.5,corner_radius=0.35,
                            stroke_color=BLUE,stroke_width=5,fill_color=BLUE,fill_opacity=0.15).move_to([3.4,0,0])),run_time=0.8)
        # Matching category names do not claim equal amounts or identical details.
        cats = ['proteins','lipids','carbohydrates','nucleic acids']
        category_labels = VGroup()
        for name, cue, y in zip(cats,cats,[0.9,0.3,-0.3,-0.9]):
            self.at(cue)
            row = VGroup(*[T(name,24,TEXT).move_to([x,y,0]) for x in [-3.4,3.4]])
            category_labels.add(row)
            self.play(FadeIn(row),run_time=0.3)
        self.at('The details differ')
        note = T('Details differ; basic composition is shared',28,GREY).move_to([0,-2.25,0])
        self.play(FadeIn(note),run_time=0.6)
        self.at('but the basic composition')
        clear(self)
        labels = ['1  Organisms contain cells','2  Cells are life’s basic units','3  New cells come from cells',
                  '4  Metabolism is inside cells','5  DNA passes to new cells','6  Basic composition is shared']
        summary = VGroup(*[T(s,28,BLUE if i<3 else YELLOW).move_to([0,2.5-i,0]) for i,s in enumerate(labels)])
        self.play(FadeIn(summary),run_time=0.7)
        self.finish()


class S05Revised(SpokenScene):
    def construct(self):
        title = T('What evidence supports cell theory?',36,font=TITLE_FONT).move_to([0,2.9,0])
        self.at('How did scientists')
        self.play(FadeIn(title),run_time=0.6)
        self.at('showed walls of dead cells')
        cork = tissue(True).scale(1.55)
        label = T('Hooke’s cork: walls of dead cells\none plant material',28,GREY).move_to([0,-2.2,0])
        self.play(Create(cork),FadeIn(label),run_time=0.8)
        self.at('compare many plant')
        plant = tissue(True).scale(1.3).move_to([-3.2,0.3,0])
        animal = tissue(False).scale(1.3).move_to([3.2,0.3,0])
        labels = VGroup(T('plant tissue samples',28,BLUE).move_to([-3.2,-1.4,0]),
                        T('animal tissue samples',28,BLUE).move_to([3.2,-1.4,0]))
        self.play(ReplacementTransform(cork,plant),FadeIn(animal),FadeOut(label),FadeIn(labels),run_time=0.8)
        # Cycle the samples' cell proportions while preserving their cellular plan.
        self.play(plant.animate.stretch(0.75, 1), animal.animate.stretch(1.13, 0), run_time=0.6)
        self.play(plant.animate.stretch(1.2, 0), animal.animate.stretch(0.8, 1), run_time=0.6)
        self.at('the shared cellular plan')
        self.play(Indicate(plant,color=YELLOW),Indicate(animal,color=YELLOW),run_time=0.8)
        self.at('They also corrected')
        clear(self)
        title = T('A rejected model',36,RED).move_to([0,2.9,0])
        fluid = RoundedRectangle(width=4.3,height=2.5,corner_radius=0.2,stroke_color=RED,
                                 fill_color=RED,fill_opacity=0.1).move_to([-2.6,0.1,0])
        label = T('structureless fluid',28,RED).move_to([-2.6,-1.8,0])
        self.play(FadeIn(title),FadeIn(fluid),FadeIn(label),run_time=0.6)
        self.at('new cells could form')
        falsecell = cellc(0.7).move_to(fluid)
        self.play(GrowFromCenter(falsecell),run_time=0.6)
        self.at('inside a structureless fluid')
        cross = VGroup(Line([-4.5,-1,0],[-0.7,1.2,0],color=RED,stroke_width=8),
                       Line([-4.5,1.2,0],[-0.7,-1,0],color=RED,stroke_width=8))
        self.play(Create(cross),run_time=0.6)
        self.at('published evidence')
        clear(self)
        title = T('Remak: evidence of division',36,GREEN).move_to([0,2.9,0])
        cell = cellc(1.6,sw=5)
        self.play(FadeIn(title),FadeIn(cell),run_time=0.6)
        self.at('existing cells divide')
        pair = daughters()
        self.play(ReplacementTransform(cell,pair),run_time=0.9)
        self.at('spread the idea')
        statement = T('Virchow: every cell comes from a cell',30,GREEN).move_to([0,-2.4,0])
        self.play(FadeIn(statement),run_time=0.7)
        self.at('A scientific theory')
        clear(self)
        theory = bchip('Theory: a well-tested explanation',GREEN,34).move_to([0,1.0,0])
        self.play(FadeIn(theory),run_time=0.7)
        self.at('many lines of evidence')
        sources = VGroup(*[bchip(t,BLUE,24).move_to([x,-1.2,0]) for x,t in zip([-4.3,0,4.3],['observations','comparisons','cell division'])])
        arrows = VGroup(*[arr([x,-0.65,0],[x*0.45,0.45,0],GREEN) for x in [-4.3,0,4.3]])
        self.play(FadeIn(sources),*[GrowArrow(a) for a in arrows],run_time=0.8)
        self.at('It can change')
        update = T('New evidence can revise the explanation',28,YELLOW).move_to([0,-2.8,0])
        self.play(FadeIn(update),Indicate(theory,color=YELLOW,scale_factor=1.04),run_time=0.8)
        self.finish()


class S03Resolve(SpokenScene):
    def construct(self):
        # Overlapping soft halos only: no crisp points inside an unresolved image.
        def blur():
            return VGroup(*[Circle(radius=r,stroke_width=0,fill_color=BLUE,fill_opacity=op)
                            .stretch(1.3,0) for r,op in [(0.8,0.08),(0.65,0.13),(0.5,0.2)]])
        title = T('Microscopes reveal evidence',36,TEAL,font=TITLE_FONT).move_to([0,2.9,0])
        blurred = blur().move_to([0,0.2,0])
        label = T('unresolved pair',28,GREY).move_to([0,-2.3,0])
        self.at('Microscopes helped')
        self.play(FadeIn(title),FadeIn(blurred),FadeIn(label),run_time=0.6)
        self.at('Magnification makes')
        self.play(Transform(title,T('Magnification: a bigger image',36,YELLOW).move_to(title)),
                  blurred.animate.scale(1.7),run_time=0.8)
        self.at('Resolution decides')
        resolved = VGroup(*[cellc(0.22,GREEN,0.9).move_to([x,0.2,0]) for x in [-0.85,0.85]])
        self.play(Transform(title,T('Resolution: separate details',36,GREEN).move_to(title)),
                  ReplacementTransform(blurred,resolved),Transform(label,T('two points resolved',28,GREEN).move_to(label)),run_time=0.8)
        self.at('Enlarging a blur')
        blurred = blur().scale(1.7).move_to([-3.2,0.2,0])
        self.play(resolved.animate.shift(RIGHT*3.2),FadeIn(blurred),
                  Transform(label,T('Bigger blur                     Resolved pair',28,GREY).move_to(label)),run_time=0.7)
        self.at('Many cells are almost clear')
        clear(self)
        cell = cellc(2.15,BLUE,0.04,4).set_stroke(opacity=0.5).move_to([0,0.1,0])
        nuc = Circle(radius=0.7,stroke_color=PURPLE,stroke_width=3,fill_color=PURPLE,
                     fill_opacity=0.0).set_stroke(opacity=0.12).move_to([0.2,0.3,0])
        label = T('almost clear cell',30,GREY).move_to([0,-2.7,0])
        title = T('Contrast',36,PURPLE).move_to([0,2.9,0])
        self.play(FadeIn(cell),FadeIn(nuc),FadeIn(label),FadeIn(title),run_time=0.7)
        self.at('Stains add contrast')
        dye = bchip('stain',PURPLE,28).move_to([-4.6,1.5,0])
        self.play(FadeIn(dye),run_time=0.4)
        self.at('sticking to some parts')
        nlab = T('nucleus',28,PURPLE).move_to([3.9,1.5,0])
        pointer = arr([3.1,1.3,0],[0.9,0.6,0],PURPLE)
        self.play(dye.animate.move_to([-2.9,0.3,0]),nuc.animate.set_stroke(PURPLE,5,opacity=1).set_fill(PURPLE,0.55),
                  FadeIn(nlab),GrowArrow(pointer),Transform(label,T('stain makes parts stand out',30,PURPLE).move_to(label)),run_time=0.8)
        self.finish()


class S04Limits(SpokenScene):
    def construct(self):
        title = T('Ordinary light microscope',36,TEAL).move_to([0,2.9,0])
        cell = VGroup(cellc(1.0).stretch(1.25,0),cellc(0.3,PURPLE,0.4)).move_to([-3.3,0.4,0])
        bacterium = microbe().move_to([3.3,0.4,0])
        labels = VGroup(T('cheek cell',28,BLUE).move_to([-3.3,-1.2,0]),
                        T('bacterium',28,BLUE).move_to([3.3,-1.2,0]))
        self.at('An ordinary light microscope')
        self.play(FadeIn(title),run_time=0.5)
        self.at('a cheek cell')
        self.play(FadeIn(cell),FadeIn(labels[0]),run_time=0.5)
        self.at('or a bacterium')
        self.play(FadeIn(bacterium),FadeIn(labels[1]),run_time=0.5)
        self.at('Ribosomes are too small')
        limit = T('Ribosomes: too small to resolve',30,RED).move_to([0,-2.7,0])
        self.play(FadeIn(limit),run_time=0.6)
        self.at('Electron microscopes')
        # Replace the whole tool view, never zoom the light image to show a ribosome.
        clear(self)
        title = T('Electron microscope',36,TEAL).move_to([0,2.9,0])
        field = RoundedRectangle(width=8.6,height=3.5,corner_radius=0.2,stroke_color=GREY,stroke_width=3)
        self.play(FadeIn(title),Create(field),run_time=0.5)
        self.at('including ribosomes')
        dots = VGroup(*[Dot([x,y,0],radius=0.16,color=GREEN) for x,y in [(-2,0.6),(0,-0.4),(2,0.6)]])
        label = T('ribosomes resolved • schematic view',28,GREEN).move_to([0,-2.6,0])
        self.play(FadeIn(dots),FadeIn(label),run_time=0.6)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        observation = bchip('microscope\nobservations',TEAL,28).move_to([-4.3,1.2,0])
        comparison = tissue(True).move_to([0,1.1,0])
        division = daughters().scale(0.55).move_to([4.3,1.1,0])
        labels = VGroup(T('comparisons',26,BLUE).move_to([0,-0.5,0]),
                        T('division evidence',26,GREEN).move_to([4.3,-0.5,0]))
        self.at('Tools made observations')
        self.play(FadeIn(observation),run_time=0.7)
        self.at('Comparisons and evidence')
        self.play(FadeIn(comparison),FadeIn(division),FadeIn(labels),run_time=0.7)
        self.at('supported and corrected')
        theory = T('cell theory',34,GREEN).move_to([0,-2.3,0])
        arrows = VGroup(*[arr([x,-0.9,0],[x*0.2,-1.9,0],GREEN) for x in [-4.3,0,4.3]])
        self.play(*[GrowArrow(a) for a in arrows],FadeIn(theory),run_time=0.8)
        self.at('Its central idea')
        clear(self)
        ex = examples()
        self.play(FadeIn(ex),run_time=0.7)
        self.at('cells are the basic units')
        line = T('Cells are the basic units of life',38,YELLOW,font=TITLE_FONT).move_to([0,2.8,0])
        self.play(FadeIn(line),*[Indicate(e[0],color=YELLOW,scale_factor=1.06) for e in ex],run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "All living things are made of cells, and cells come from cells."
    def construct(self):
        ex = examples()
        line = T(self.LINE,38,YELLOW,font=TITLE_FONT).move_to([0,2.8,0])
        fit(line, max_w=12.5)
        self.add(ex,line)
        self.wait(2.3)
        self.play(FadeOut(ex),FadeOut(line),run_time=0.8)
        self.finish()
