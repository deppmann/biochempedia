"""Neuron doctrine: a touch is not a fusion  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = neuron one (the branch and cell on the left)
  YELLOW = neuron two (the branch and cell on the right)
  RED    = the limit of the light microscope (the blind spot)
  ORANGE = Golgi's reading: the branches are joined
  GREEN  = Cajal's reading and the verdict: separate cells, each with its own membrane
  TEAL   = what passes through gap junctions (ions, small molecules, the signal)
  GREY   = tissue, outlines, stain tangle, de-emphasised things
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def smooth(points, color, w=9, opacity=1.0):
    m = VMobject()
    m.set_points_smoothly([np.array([x, y, 0.0]) for x, y in points])
    m.set_stroke(color, w, opacity=opacity)
    m.set_fill(opacity=0)
    return m


def branch(side, color):
    """a stylised nerve branch coming in from one side to the junction at the centre."""
    s = 1 if side == "R" else -1
    pts = [(-6.0, -2.3), (-4.5, -0.9), (-2.9, -1.1), (-1.5, 0.45), (-0.2, 0.04)]
    twigs = [[(-4.5, -0.9), (-5.2, 0.9), (-5.7, 1.9)],
             [(-2.9, -1.1), (-2.6, -1.9), (-2.4, -2.5)],
             [(-1.5, 0.45), (-1.9, 1.3), (-2.0, 2.2)]]
    g = VGroup(smooth(pts, color, 10))
    for t in twigs:
        g.add(smooth(t, color, 6))
    if s == 1:  # mirror through the origin
        g.apply_matrix(np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]]))
    return g


def tip(color, side, length=2.2, w=12, gap=0.3, y=0.0):
    """a blunt branch ending, for the close-up panels. side L comes from the left."""
    s = -1 if side == "L" else 1
    return Line([s * (gap / 2 + length), y, 0], [s * gap / 2, y, 0], color=color, stroke_width=w)


def disc(radius, center, fill=0.0, dashed=True):
    c = Circle(radius=radius, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=fill).move_to(center)
    return DashedVMobject(c, num_dashes=28) if dashed and fill == 0 else c


def cell_pair(gap, h=4.4, yc=0.35, w=4.9):
    """two big cell outlines facing each other across `gap`; returns left, right, left-edge, right-edge."""
    xl = -(gap / 2 + w / 2)
    xr = gap / 2 + w / 2
    L = RoundedRectangle(corner_radius=0.5, width=w, height=h, stroke_color=BLUE, stroke_width=4,
                         fill_color=BLUE, fill_opacity=0.12).move_to([xl, yc, 0])
    R = RoundedRectangle(corner_radius=0.5, width=w, height=h, stroke_color=YELLOW, stroke_width=4,
                         fill_color=YELLOW, fill_opacity=0.12).move_to([xr, yc, 0])
    el = Line([-gap / 2, yc - h / 2 + 0.5, 0], [-gap / 2, yc + h / 2 - 0.5, 0], color=GREEN, stroke_width=9)
    er = Line([gap / 2, yc - h / 2 + 0.5, 0], [gap / 2, yc + h / 2 - 0.5, 0], color=GREEN, stroke_width=9)
    return L, R, el, er


def channel(y, gap, color=TEAL):
    return RoundedRectangle(corner_radius=0.08, width=gap + 0.2, height=0.5, stroke_color=color, stroke_width=4,
                            fill_color=BG, fill_opacity=1).move_to([0, y, 0])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def label(text, color=TEXT, size=26):
    return T(text, size, color)


class S00Title(TitleCard):
    LESSON = "Seeing neurons: Golgi, Cajal and the neuron doctrine"
    TITLE = "A Touch Is Not a Fusion"


# A single continuous contour encloses soma, dendrites and axon.
def neuron(color=BLUE):
    pts = [(-2.1,1.15),(-1.3,.65),(-1.05,.35),(-.85,.43),(-1.0,1.25),
           (-.78,1.25),(-.55,.48),(-.25,.3),(.05,.13),(1.7,.13),
           (2.1,.6),(2.23,.48),(1.86,0),(2.23,-.48),(2.1,-.6),
           (1.7,-.13),(.05,-.13),(-.25,-.3),(-.55,-.48),(-.78,-1.25),
           (-1.0,-1.25),(-.85,-.43),(-1.05,-.35),(-1.3,-.65),
           (-2.1,-1.15),(-2.23,-.98),(-1.55,-.42),(-1.24,0),
           (-1.55,.42),(-2.23,.98)]
    return Polygon(*[[x,y,0] for x,y in pts], stroke_color=color,
                   stroke_width=3, fill_color=color, fill_opacity=.15).round_corners(.07)


def circuit():
    cells = VGroup(*[neuron(c).scale(.8).move_to([x,0,0])
                    for x,c in [(-4.05,BLUE),(0,YELLOW),(4.05,BLUE)]])
    arrows = VGroup(*[arr([x,-1.65,0],[x+2.4,-1.65,0],TEAL)
                      for x in [-4.8,-.9,3.0]])
    return cells, arrows


class S01Meet(SpokenScene):
    def construct(self):
        a = neuron(BLUE).move_to([-2.4,0,0])
        b = neuron(YELLOW).move_to([2.4,0,0])
        answer = label('Separate cells', GREEN, 34).move_to([0,3.05,0])
        self.at('In the vertebrate')
        self.play(Create(a), Create(b), FadeIn(answer), run_time=1.4)
        own = label('Each has its own membrane', GREEN, 26).move_to([0,-2.8,0])
        self.at('Each has its own')
        self.play(Indicate(a,scale_factor=1),Indicate(b,scale_factor=1),FadeIn(own),run_time=.8)
        contact = Circle(radius=.33,color=TEAL).move_to([0,0,0])
        ct = label('specialized contact',TEAL,26).move_to([0,1.95,0])
        self.at('specialized contacts')
        self.play(Create(contact),FadeIn(ct),run_time=.7)
        self.at('neuron doctrine')
        self.play(Transform(answer,label('Neuron doctrine',GREEN,34).move_to(answer)),run_time=.6)
        cells, arrows = circuit()
        self.at('wire cells together')
        self.play(FadeOut(VGroup(a,b,contact,ct,own)),FadeIn(cells),run_time=1)
        self.at('direction of signal flow')
        self.play(LaggedStart(*[GrowArrow(x) for x in arrows],lag_ratio=.3),run_time=1.5)
        branches = VGroup(branch('L',BLUE),branch('R',YELLOW)).scale(.85)
        self.at('Two fine nerve branches')
        self.play(FadeOut(cells),FadeOut(arrows),Create(branches),run_time=1.2)
        self.at('Their contact connects')
        self.play(Create(Circle(radius=.4,color=TEAL)),
                  Transform(answer,label('Contact connects separate cells',GREEN,32).move_to(answer)),run_time=.7)
        self.finish()


class S03Growth(SpokenScene):
    def construct(self):
        head = label('Developmental evidence',TEXT,32).move_to([0,3.05,0])
        cell = Circle(radius=.65,color=BLUE,fill_color=BLUE,fill_opacity=.15).move_to([-4,0,0])
        name = label('one neuroblast',BLUE,28).move_to([-4,-1.35,0])
        scheme = label('His: schematic outgrowth',GREY,26).move_to([0,2.2,0])
        self.at('Development gave evidence')
        self.play(FadeIn(head),FadeIn(cell),run_time=.8)
        fibre = smooth([(-3.35,0),(-1.8,.1),(0,-.15),(2,.25),(4,.2)],BLUE,9)
        self.at('grows out from')
        self.play(Create(fibre),FadeIn(scheme),run_time=1.5)
        self.at('a neuroblast')
        self.play(FadeIn(name),run_time=.5)
        # These are separate fixed drawings; no cone travels along an axon.
        def specimen(x,fringe=False):
            shaft = tip(BLUE,'L',2.0,9,.15).shift([x+.75,0,0])
            cone = Polygon([x-.1,-.14,0],[x+.75,-.52,0],[x+1.15,0,0],
                           [x+.75,.52,0],[x-.1,.14,0],color=BLUE,fill_color=BLUE,fill_opacity=.25)
            g = VGroup(shaft,cone)
            if fringe:
                for y in [-.5,0,.5]:
                    g.add(smooth([(x+.75,y),(x+1.2,y*1.5),(x+1.5,y*1.6)],BLUE,3))
            return g
        stills = VGroup(specimen(-2.8),specimen(2.5,True)).scale(1.3)
        fixed = label('Chick-embryo axon tips • fixed specimens',GREY,28).move_to([0,2.2,0])
        self.at('described growth cones')
        self.play(FadeOut(VGroup(cell,fibre,name,scheme)),FadeIn(stills),FadeIn(fixed),run_time=.8)
        inference = label('Advancing ends? An interpretation of still shapes',GREEN,26).move_to([0,-2.3,0])
        self.at('He read them')
        self.play(FadeIn(inference),run_time=.7)
        dead = chip('Fixed and dead',GREY,26).move_to([0,-1.2,0])
        self.at('fixed and dead')
        self.play(FadeIn(dead),run_time=.6)
        self.at('Movement was an inference')
        self.play(Indicate(stills[0],scale_factor=1.04),run_time=.6)
        self.play(Indicate(stills[1],scale_factor=1.04),run_time=.6)
        self.finish()


class S03Polarity(SpokenScene):
    def construct(self):
        n = neuron(BLUE).scale(1.7).move_to([0,0,0])
        head = label('Usual direction of signal flow',TEAL,32).move_to([0,3.1,0])
        self.at('Separate cells also')
        self.play(Create(n),FadeIn(head),run_time=1)
        labels = VGroup(label('dendrites',BLUE,26).move_to([-3.3,-2.75,0]),
                        label('cell body',BLUE,26).move_to([-1.3,-2.75,0]),
                        label('axon',BLUE,26).move_to([2.8,-2.75,0]))
        entry = arr([-3.8,.7,0],[-1.2,0,0],TEAL)
        exit_ = arr([-.4,0,0],[3.5,0,0],TEAL)
        self.at('Signals enter through')
        self.play(FadeIn(labels[:2]),GrowArrow(entry),run_time=1)
        self.at('leave through the axon')
        self.play(FadeIn(labels[2]),GrowArrow(exit_),run_time=.7)
        self.at('dynamic polarization')
        self.play(Transform(head,label('Dynamic polarization',TEAL,32).move_to(head)),run_time=.6)
        cells, arrows = circuit()
        self.at('through a chain')
        self.play(FadeOut(VGroup(n,labels,entry,exit_)),FadeIn(cells),run_time=.7)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=.2),run_time=.8)
        self.at('a useful generalization')
        self.play(Transform(head,label('A useful generalization',TEAL,32).move_to(head)),run_time=.6)
        # Mirrored neurons meet at their dendritic ends, with a small gap.
        a = neuron(BLUE).scale(.95).rotate(PI).move_to([-2.3,0,0])
        b = neuron(YELLOW).scale(.95).move_to([2.3,0,0])
        exception = label('Exception: dendrite-to-dendrite synapse',GREEN,28).move_to([0,-2.5,0])
        self.at('including synapses between dendrites')
        self.play(FadeOut(cells),FadeOut(arrows),FadeIn(VGroup(a,b)),FadeIn(exception),
                  Create(Circle(radius=.38,color=GREEN)),run_time=.8)
        self.finish()


class S03Camps(SpokenScene):
    def construct(self):
        tissue = VGroup(*[neuron(GREY).scale(.65).move_to([x,y,0])
                          for x,y in [(-3.7,1.15),(0,1.15),(3.7,1.15),(-3.7,-1.15),(0,-1.15),(3.7,-1.15)]])
        head = label('Crowded tissue',GREY,32).move_to([0,3.1,0])
        edge = Rectangle(width=12,height=4.6,color=GREY,stroke_width=2)
        self.at('How could anyone')
        self.play(FadeIn(tissue),FadeIn(head),Create(edge),run_time=.9)
        self.at('black reaction fills')
        self.play(*[t.animate.set_opacity(.12) for i,t in enumerate(tissue) if i not in [0,4]],
                  tissue[0].animate.set_color(TEXT).set_fill(TEXT,opacity=.65),
                  tissue[4].animate.set_color(TEXT).set_fill(TEXT,opacity=.65),
                  Transform(head,label('Black reaction: a few cells, completely',TEXT,30).move_to(head)),run_time=1)
        self.at('A single cell')
        self.play(Indicate(tissue[0],color=TEXT,scale_factor=1.05),run_time=.9)
        cuts = VGroup(*[Line([x-.12,y-.15,0],[x+.12,y+.15,0],color=RED,stroke_width=4)
                       for x,y in [(-5.08,1.8),(-5.08,.5)]])
        cutlabel = label('Section edge: branches cut off',GREY,26).move_to([0,-3.1,0])
        # Place the section boundary through the leftmost dendritic branches.
        boundary = DashedLine([-5.08,-2.3,0],[-5.08,2.3,0],color=GREY)
        self.at('branches leaving the section')
        cropped = tissue[0].copy().apply_function(lambda p: np.array([max(p[0],-5.08),p[1],p[2]]))
        self.play(Transform(tissue[0],cropped),Create(boundary),Create(cuts),FadeIn(cutlabel),run_time=.7)
        left = VGroup(branch('L',ORANGE),branch('R',ORANGE),
                      Line([-.2,.04,0],[.2,-.04,0],color=ORANGE,stroke_width=10)).scale(.44).move_to([-3.1,0,0])
        right = VGroup(branch('L',BLUE),branch('R',YELLOW)).scale(.44).move_to([3.1,0,0])
        golgi = label('Golgi: continuous axon net',ORANGE,26).move_to([-3.1,1.6,0])
        cajal = label('Cajal: free endings',GREEN,26).move_to([3.1,1.6,0])
        interp = label('Interpretations of stained tissue',GREY,30).move_to([0,3.1,0])
        self.at('axon branches as')
        self.play(FadeOut(VGroup(tissue,edge,boundary,cuts,cutlabel)),Transform(head,interp),
                  Create(left),FadeIn(golgi),run_time=.7)
        self.at('Cajal found branches')
        self.play(Create(right),FadeIn(cajal),run_time=.8)
        sep = label('near other cells • without joining',GREEN,26).move_to([3.1,-1.6,0])
        self.at('without joining them')
        self.play(FadeIn(sep),run_time=.6)
        self.finish()


class S02Blur(SpokenScene):
    def construct(self):
        ctr = np.array([-3.2,.4,0])
        junction = VGroup(tip(BLUE,'L',2.6,14,.18),tip(YELLOW,'R',2.6,14,.18)).shift(ctr)
        blind = VGroup(disc(1.6,ctr),disc(1.6,ctr,fill=.3,dashed=False))
        head = label('Historical light microscope: unresolved',RED,30).move_to([0,3.2,0])
        self.at('The light microscope')
        self.play(Create(junction),FadeIn(blind),FadeIn(head),run_time=.9)
        self.at('Fine branches touching')
        touching = label('touching branches',TEXT,26).move_to([-3.2,2.35,0])
        self.play(FadeIn(touching),run_time=.5)
        slab = Rectangle(width=5.2,height=2.2,color=GREY,fill_color=GREY,fill_opacity=.1).move_to([3.3,.6,0])
        a = Line([.9,1.2,0],[3.8,1.2,0],color=BLUE,stroke_width=12)
        b = Line([2.8,0,0],[5.7,0,0],color=YELLOW,stroke_width=12)
        depth = label('different depths',GREY,26).move_to([3.3,2.35,0])
        self.at('different depths')
        self.play(FadeIn(slab),Create(a),Create(b),FadeIn(depth),run_time=.7)
        projected = VGroup(Line([.9,-1.7,0],[3.8,-1.7,0],color=BLUE,stroke_width=12),
                           Line([2.8,-1.7,0],[5.7,-1.7,0],color=YELLOW,stroke_width=12),
                           disc(.7,[3.3,-1.7,0],fill=.32,dashed=False))
        self.at('could look the same')
        self.play(FadeIn(projected),run_time=.6)
        verdict = label('Contact or fusion? Unresolved.',RED,30).move_to([0,-3.1,0])
        self.at('The image could not tell')
        self.play(FadeIn(verdict),run_time=.7)
        self.finish()


class S04Cleft(SpokenScene):
    def construct(self):
        blur = VGroup(tip(BLUE,'L',1.2,14,.3),tip(YELLOW,'R',1.2,14,.3),
                      disc(1.2,ORIGIN),disc(1.2,ORIGIN,fill=.3,dashed=False))
        head = label('The direct test • 1950s',GREY,32).move_to([0,3.2,0])
        self.at('The direct test')
        self.play(FadeIn(blur),FadeIn(head),run_time=.8)
        L,R,el,er = cell_pair(2.1,h=4.1,yc=.1,w=4.7)
        self.at('Electron microscopy')
        self.play(blur.animate.scale(3).set_opacity(0),FadeIn(L),FadeIn(R),
                  Transform(head,label('Electron microscopy • chemical synapse',TEXT,30).move_to(head)),run_time=1)
        self.remove(blur)
        self.at('two separate membranes')
        self.play(Create(el),Create(er),run_time=.8)
        gap = VGroup(DoubleArrow([-1.05,.1,0],[1.05,.1,0],buff=0,color=TEXT,tip_length=.18),
                     label('cleft',TEXT,28).move_to([0,.75,0]))
        self.at('a narrow cleft')
        self.play(FadeIn(gap),run_time=.7)
        ves = VGroup(*[Circle(radius=.18,color=BLUE,fill_color=BLUE,fill_opacity=.45).move_to([x,y,0])
                       for x,y in [(-2,1.4),(-2.9,.7),(-2,-.5),(-3.7,1.3)]])
        vlabel = label('vesicles',BLUE,26).move_to([-3.3,-2.65,0])
        self.at('small vesicles')
        self.play(FadeIn(ves),FadeIn(vlabel),run_time=.7)
        self.at('The gap was visible')
        self.play(Indicate(VGroup(el,er),color=GREEN,scale_factor=1),run_time=.7)
        cells,arrows = circuit()
        self.at('Separate cells form circuits')
        self.play(FadeOut(VGroup(L,R,el,er,gap,ves,vlabel)),FadeIn(cells),
                  Transform(head,label('Separate cells • specialized contacts',GREEN,32).move_to(head)),run_time=.9)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=.2),run_time=.7)
        self.finish()


class S05Gap(SpokenScene):
    def construct(self):
        L,R,el,er = cell_pair(.8,h=4.3,yc=0,w=5.1)
        head = label('A smaller point: electrical coupling',TEAL,30).move_to([0,3.15,0])
        self.at('A smaller')
        self.play(FadeIn(VGroup(L,R,el,er)),FadeIn(head),run_time=.8)
        chans = VGroup(*[channel(y,.8) for y in [1.2,0,-1.2]])
        self.at('through channels')
        self.play(FadeIn(chans),run_time=.6)
        dots = VGroup(*[Dot([-1.7,y,0],radius=.12,color=TEAL) for y in [1.2,0,-1.2]])
        small = label('ions and small molecules',TEAL,26).move_to([0,-2.9,0])
        self.at('ions and small molecules')
        self.play(FadeIn(dots),FadeIn(small),run_time=.3)
        self.play(dots.animate.shift(RIGHT*3.4),run_time=1.3,rate_func=linear)
        shut = VGroup(*[Line([0,y-.22,0],[0,y+.22,0],color=RED,stroke_width=8) for y in [1.2,0,-1.2]])
        self.at('The channels can close')
        self.play(FadeOut(dots),Create(shut),Transform(small,label('Channels can close',RED,26).move_to(small)),run_time=.7)
        self.at('Each neuron still keeps')
        self.play(Indicate(VGroup(el,er),color=GREEN,scale_factor=1),
                  Transform(small,label('Each keeps its own membrane',GREEN,28).move_to(small)),run_time=.8)
        self.finish()


class S07End(EndCard):
    LINE = "In vertebrates, separate cells form circuits through specialized contacts."
