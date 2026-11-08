"""Smell lines: revised teaching animation.
COLOR MAP: cyan/blue = receptor identity; yellow = odorant/concentration;
green = measured response schematic or toy ON; red = receptor removal;
white/bright grey = structure. Other receptor identities use smell-only muted
teal, steel, olive, and coral; no taste palette. DATA is the exact supplied toy
binary model. Research squares are qualitative, explicitly not measured values.
"""
import numpy as np
from bp_style import *

RECEPTOR, ODORANT, ON, GONE = BLUE, YELLOW, GREEN, RED
MUTED = '#C6CED8'
SMELL = [BLUE, '#6EC6B8', '#B5BF77', '#D48B75']
IDENTITIES = [BLUE, SMELL[1], BLUE, SMELL[2], SMELL[3], BLUE, SMELL[1], BLUE]
DATA = np.array([[1,1,0,0],[0,1,1,0],[1,1,1,0],[0,0,0,1]])
XX = [-1.9,-.45,1,2.45]
YY = [1.45,.15,-1.15,-2.45]


def label(s,x=0,y=3.3,size=30,color=TEXT):
    return T(s,size,color).move_to([x,y,0])


def neuron(x,color,y=-.35):
    # Cilia face the nasal lumen below; axons face the bulb above throughout.
    soma=Circle(.3,color=color,fill_opacity=.22).move_to([x,y,0])
    dend=Line([x,y-.3,0],[x,y-1.5,0],color=color,stroke_width=3)
    cilia=VGroup(*[Line([x,y-1.5,0],[x+dx,y-1.95,0],color=color,stroke_width=3) for dx in [-.3,0,.3]])
    axon=Line([x,y+.3,0],[x,y+2.35,0],color=color,stroke_width=3)
    return VGroup(soma,dend,cilia,axon)


def epithelium(many=False):
    cols=IDENTITIES if not many else [BLUE,'#6EC6B8','#B5BF77','#D48B75','#92A7C8','#C4AA77','#7DB58A','#C47F88',BLUE,'#6EC6B8','#B5BF77','#D48B75']
    cells=VGroup(*[neuron(x,c) for x,c in zip(np.linspace(-5.7,5.7,len(cols)),cols)])
    bar=Rectangle(width=12.3,height=.4,color=MUTED,fill_opacity=.08).move_to([0,-.35,0])
    return VGroup(bar,cells,label('olfactory epithelium',y=-3.15,color=MUTED))


def line_stage():
    g=epithelium()
    for i,n in enumerate(g[1]):
        if IDENTITIES[i]!=BLUE:n.set_opacity(.2)
    return g


def line_bracket():
    return VGroup(Line([-5.7,2.3,0],[5.7,2.3,0],color=BLUE),*[Line([x,2.1,0],[x,2.3,0],color=BLUE) for x in np.linspace(-5.7,5.7,8)[[0,2,5,7]]])


def converge_stage(wires=True):
    bulb=Ellipse(width=8.5,height=2.05,color=MUTED,fill_opacity=.08).move_to([0,1.8,0])
    gl=VGroup(*[Circle(.38,color=BLUE,fill_opacity=.7).move_to([x,1.7,0]) for x in [-2.4,2.4]])
    cells=VGroup(*[neuron(x,BLUE,y=-1.35) for x in [-5,-2.7,1.6,4.8]])
    for n in cells:n[3].set_opacity(0)
    epi=Rectangle(width=11.5,height=.35,color=MUTED,fill_opacity=.1).move_to([0,-1.35,0])
    paths=VGroup()
    # Four scattered axons gather centrally. Each continues to ONE terminal;
    # the population ends at the two glomeruli, not one bifurcating neuron.
    for i,n in enumerate(cells):
        end=gl[0 if i<2 else 1].get_bottom()+RIGHT*(-.08 if i%2==0 else .08)
        mid=np.array([-.18+.12*i,.05,0])
        upper=mid+UP*.6
        p=VMobject(color=BLUE,stroke_width=4)
        p.set_points(CubicBezier(n[0].get_top(),[n[0].get_x(),-.4,0],[mid[0],-.15,0],mid).get_points())
        p.append_points(Line(mid,upper).get_points())
        p.append_points(CubicBezier(upper,[upper[0],.95,0],[end[0],.95,0],end).get_points())
        paths.add(p)
    g=VGroup(bulb,gl,epi,cells,paths if wires else VGroup(),label('same receptor, scattered cells',y=3.35,color=BLUE),label('one side shown · each side has its own bulb',y=-3.6,size=28,color=MUTED),label('olfactory bulb',y=2.35,size=28,color=MUTED),label('epithelium',x=-.5,y=-1.35,size=28,color=MUTED))
    return g,paths


def bulb_map():
    outline=RoundedRectangle(width=11.8,height=5.4,corner_radius=1,color=MUTED,fill_opacity=.05).move_to([0,.15,0])
    rng=np.random.default_rng(17)
    positions=[]
    for r in range(7):
        for c in range(11):
            positions.append([-4.9+c*.98+rng.uniform(-.12,.12),2.35-r*.73+rng.uniform(-.08,.08),0])
    # Exactly two of each teaching identity; all remaining tiles use other colours.
    special={4:0,73:0,17:1,69:1,31:2,54:2,9:3,46:3}
    tiles=VGroup()
    for i,pos in enumerate(positions):
        col=SMELL[special[i]] if i in special else ManimColor.from_hsv([rng.uniform(.12,.95),.16,.42])
        tiles.add(Circle(.26,color=col,fill_opacity=.8).move_to(pos))
    return VGroup(outline,tiles,label('mouse olfactory bulb',y=3.35),label('~1,800 glomeruli per bulb · schematic, not to scale',y=-3.3,size=28,color=MUTED))


def lab_cells(respond=True,tags=False):
    cells=VGroup()
    for i,x in enumerate([-4,0,4]):
        c=ON if respond and i<2 else MUTED
        soma=Circle(1.25,color=c,fill_opacity=.45 if i<2 and respond else .09).move_to([x,-.15,0])
        nucleus=Circle(.34,color=c,fill_opacity=.12).move_to(soma)
        # Short radial processes meet, rather than cross, the membrane.
        neurites=VGroup(*[Line(soma.get_center()+1.25*np.array([np.cos(a),np.sin(a),0]),soma.get_center()+1.8*np.array([np.cos(a),np.sin(a),0]),color=c) for a in [-np.pi/2,np.pi/4,3*np.pi/4]])
        cells.add(VGroup(soma,nucleus,neurites))
    g=VGroup(cells,label('calcium imaging · single mouse neurons · schematic',y=-3.3,size=28,color=MUTED))
    if tags:g.add(VGroup(chip('receptor Rα',BLUE,size=30).move_to([-4,-2.35,0]),chip('receptor Rβ',BLUE,size=30).move_to([0,-2.35,0]),label('no response',4,-2.35,30,MUTED)))
    return g


def odorant_dots():
    return VGroup(*[Dot([x+dx,2.2+.18*j,0],radius=.1,color=ODORANT) for x in [-4,0,4] for j,dx in enumerate([-.35,.1,.4])])


def research_grid():
    # Same orientation as the toy: receptors across, odorants down.
    boxes=VGroup(*[Square(1.1,color=MUTED,stroke_width=2).move_to([-1.5+1.65*c,1.45-1.6*r,0]) for r in range(3) for c in range(3)])
    heads=VGroup(*[label(s,-1.5+1.65*c,2.65,30,BLUE) for c,s in enumerate(['Rα','Rβ','Rγ'])])
    rows=VGroup(*[label('odorant '+str(r+1),-4.3,1.45-1.6*r,30,ODORANT) for r in range(3)])
    return VGroup(boxes,heads,rows,label('schematic of findings · not measured values',y=-3.3,size=28,color=MUTED),label('receptors',y=3.4,color=BLUE))


def activate(box):return box.animate.set_fill(ON,.9).set_stroke(ON)


def slider(high=True):
    rail=Line([4.5,-1.5,0],[4.5,1.45,0],color=MUTED,stroke_width=5)
    knob=Dot([4.5,1.45 if high else -1.5,0],radius=.16,color=ODORANT)
    return VGroup(rail,knob,label('odorant 1',5.5,.95 if high else -2,26,ODORANT),label('10×',5.4,1.45,30,ODORANT),label('1×',5.4,-1.5,30,ODORANT))


def matrix(data=DATA,headers=True,removed=False,high=False,question=False,dim=False):
    boxes=VGroup(*[Square(.9,color=ON if data[r,c] else MUTED,fill_color=ON,fill_opacity=.9 if data[r,c] else 0,stroke_width=3).move_to([XX[c],YY[r],0]) for r in range(4) for c in range(4)])
    heads=VGroup(*[chip(s,BLUE,size=32).move_to([x,2.6,0]) for s,x in zip('ABCD',XX)]) if headers else VGroup()
    rows=VGroup(*[label('odorant '+str(r+1),-4.35,YY[r],30,ODORANT) for r in range(4)])
    g=VGroup(boxes,heads,rows,label('invented for illustration',y=3.45,size=30,color=MUTED))
    if removed:
        heads[0].set_opacity(.25)
        for r in range(4):boxes[r*4].set_fill(opacity=0).set_stroke(MUTED,opacity=.2)
        g.add(VGroup(Line([-2.3,2.2,0],[-1.5,3,0],color=GONE,stroke_width=5),Line([-2.3,3,0],[-1.5,2.2,0],color=GONE,stroke_width=5)))
    if high:g.add(slider())
    if question:
        boxes[2].set_fill(opacity=0).set_stroke(MUTED)
        g.add(label('?',XX[2],YY[0],40,ODORANT))
    if dim:
        for i,b in enumerate(boxes):
            b.set_stroke(opacity=.3)
            b.set_fill(opacity=.18 if data[i//4,i%4] and not (removed and i%4==0) else 0)
    return g


def legend():
    return VGroup(label('green:',4.85,.7,28,ON),label('responds',4.85,.2,28,ON),label('empty:',4.85,-.7,28,MUTED),label('no response',4.85,-1.2,28,MUTED))


def remove_question():return label('Which two odorants give the same pattern?',y=-3.5,size=30)
def high_question():return label('What happens to odorant 1’s pattern?',y=-3.5,size=30)
def pause_tag():return VGroup(label('Pause and',4.85,1.5,28,ODORANT),label('predict',4.85,.95,30,ODORANT))
def row_outline(r):return RoundedRectangle(width=8.5,height=1.15,corner_radius=.1,color=ODORANT,stroke_width=3).move_to([-1.1,YY[r],0])


def countdown(scene):
    track=Rectangle(width=2,height=.2,color=MUTED).move_to([4.8,-.5,0])
    fill=Rectangle(width=1.96,height=.16,color=ODORANT,fill_opacity=1).move_to(track)
    scene.add(track,fill)
    scene.play(fill.animate.stretch(.001,0,about_point=fill.get_left()),run_time=5,rate_func=linear)


class S00Title(TitleCard):
    LESSON='Smell and Taste'
    TITLE='Smell Keeps Its Lines Apart'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',y=1.8,size=28,color=TEAL),label(self.LESSON.upper(),y=.9,size=30,color=MUTED))
        self.play(FadeIn(label(self.TITLE,y=-.15,size=46)),Create(Line([-1.4,-1.2,0],[1.4,-1.2,0],color=GOLD)),run_time=.8)
        self.finish()

class S01Question(SpokenScene):
    def construct(self):
        g=epithelium(True)
        q=VGroup(label('How does the nose keep a thousand',y=3.45,size=32),label('receptor types on separate lines?',y=2.85,size=32))
        self.add(g,q,label('~1,000 receptor types in a mouse · colours = receptor types',y=-3.6,size=28,color=MUTED))
        self.at('receptor types')
        self.play(LaggedStart(*[Indicate(n[0],scale_factor=1.2) for n in g[1]],lag_ratio=.06),run_time=1)
        self.finish()

class S02OneGene(SpokenScene):
    def construct(self):
        # Enlarged soma, with both processes ending exactly at its membrane.
        soma=Circle(.95,color=BLUE,fill_opacity=.22).move_to([0,.45,0])
        n=VGroup(soma,Line(soma.get_bottom(),[0,-1.55,0],color=BLUE,stroke_width=4),VGroup(*[Line([0,-1.55,0],[dx,-2.15,0],color=BLUE,stroke_width=4) for dx in [-.35,0,.35]]),Line(soma.get_top(),[0,2.8,0],color=BLUE,stroke_width=4))
        self.add(n,label('most mature mouse neurons',y=3.45,color=MUTED))
        self.at('one receptor gene')
        nucleus=Circle(.58,color=MUTED).move_to(n[0])
        genes=VGroup(*[Square(.2,color=BLUE if i==0 else MUTED,fill_opacity=1 if i==0 else .15).move_to([-.17+(i%2)*.34,.28+(i//2)*.34,0]) for i in range(4)])
        txt=label('one receptor gene on',-3.7,.25,30,BLUE)
        self.play(FadeIn(nucleus),FadeIn(genes),FadeIn(txt),Create(Line(txt.get_right(),n[0].get_left(),color=MUTED)),run_time=.5)
        self.at('high abundance')
        self.play(n[0].animate.set_fill(BLUE,.65),run_time=.5)
        self.at('can still bind')
        rec=RoundedRectangle(width=.95,height=.35,corner_radius=.1,color=BLUE,fill_opacity=.7).move_to([0,-2.15,0])
        dots=VGroup(*[Dot([x,-2.9,0],radius=.12,color=ODORANT) for x in [-.28,0,.28]])
        rlabel=label('receptor',-3,-1.8,30,BLUE)
        self.play(FadeIn(rec),FadeIn(rlabel),Create(Line(rlabel.get_right(),rec.get_left(),color=BLUE)),FadeIn(dots),run_time=.4)
        self.at('many odorants')
        many=label('many odorants',3.65,-2.6,30,ODORANT)
        self.play(dots.animate.move_to([0,-2.445,0]),FadeIn(many),GrowArrow(Arrow(many.get_left(),[.55,-2.445,0],color=ODORANT)),run_time=.5)
        self.finish()

class S03OneLine(SpokenScene):
    def construct(self):
        g=epithelium();self.add(g,label('one receptor type → one line',y=3.25,size=36,color=BLUE),line_bracket())
        self.at('all the neurons')
        self.play(*[n.animate.set_opacity(.18) for i,n in enumerate(g[1]) if IDENTITIES[i]!=BLUE],*[n[0].animate.set_fill(BLUE,.9) for i,n in enumerate(g[1]) if IDENTITIES[i]==BLUE],run_time=.7)
        self.finish()

class S04Mombaerts(SpokenScene):
    def construct(self):
        g=line_stage();self.add(g)
        q=label('Where do their axons go?',y=3.4,size=34);self.add(q,Ellipse(width=12.1,height=.55,color=MUTED).move_to([0,2.65,0]))
        for n in g[1]:n[3].set_color(MUTED)
        self.at('and colleagues made')
        self.play(Transform(q,label('Mombaerts and colleagues, 1996',y=3.4,size=30)),run_time=.4)
        self.at('fill their axons')
        marks=VGroup(*[Line(n[0].get_center(),[n.get_x(),2.7,0],color=BLUE,stroke_width=8) for i,n in enumerate(g[1]) if IDENTITIES[i]==BLUE])
        self.play(*[n[0].animate.set_fill(BLUE,1) for i,n in enumerate(g[1]) if IDENTITIES[i]==BLUE],LaggedStart(*[Create(p) for p in marks],lag_ratio=.08),FadeIn(label('marker',4.4,2.3,30,BLUE)),run_time=.8)
        self.add(label('animated schematic',y=-3.6,size=28,color=MUTED))
        self.finish()

class S05Converge(SpokenScene):
    def construct(self):
        g,paths=converge_stage(False);self.add(g)
        self.at('cells were scattered')
        self.play(Indicate(g[3],scale_factor=1.04),run_time=.6)
        self.at('Their axons gathered')
        self.play(*[Create(p) for p in paths],run_time=1.4)
        self.at('two fixed glomeruli')
        self.play(Indicate(g[1],color=BLUE,scale_factor=1.15),Transform(g[7],label('two glomeruli · one bulb',y=2.35,size=28,color=BLUE)),run_time=.6)
        self.finish()

class S06Glomeruli(SpokenScene):
    def construct(self):
        g=bulb_map();self.add(g)
        self.at('Each glomerulus')
        self.play(Indicate(g[1][4],color=BLUE,scale_factor=1.35),run_time=.6)
        self.at('mainly from neurons')
        self.play(Transform(g[2],label('mainly one receptor type per glomerulus',y=3.35,size=30,color=BLUE)),run_time=.5)
        self.finish()

class S07Map(SpokenScene):
    def construct(self):
        g=bulb_map();self.add(g[0],g[1],label('a map of lines',y=3.35,size=36,color=BLUE))
        sw=VGroup(Square(.32,color=BLUE,fill_opacity=1),T('receptor identity',30,BLUE)).arrange(RIGHT,buff=.2)
        box=RoundedRectangle(width=sw.width+.45,height=.7,corner_radius=.14,color=BLUE,fill_opacity=.12)
        sw=VGroup(box,sw).move_to([2,-3.25,0])
        target=g[1][73]
        arrow=Arrow(sw.get_top(),target.get_bottom(),color=BLUE,buff=.04,stroke_width=5,max_tip_length_to_length_ratio=.5)
        self.add(sw,arrow)
        self.at('glomerular layer')
        self.play(Indicate(target,color=BLUE,scale_factor=1.4),run_time=.7)
        self.at('a map of lines')
        self.play(FadeIn(label('identity → position',-3.7,-3.25,28,BLUE)),run_time=.4)
        self.finish()

class S08Malnic(SpokenScene):
    def construct(self):
        g=lab_cells(False);dots=odorant_dots();self.add(g,dots,label('odorant',x=2,y=2.6,color=ODORANT))
        q=label('What does each line detect?',y=3.45,size=32);self.add(q)
        self.at('and colleagues imaged')
        self.play(Transform(q,label('Malnic, Hirono, Sato and Buck, 1999',y=3.45,size=30)),run_time=.5)
        self.play(dots.animate.shift(DOWN*1.35),run_time=2.3,rate_func=linear)
        self.at('odorants were applied')
        self.play(*[c.animate.set_color(ON) for c in g[0][:2]],run_time=.45)
        self.play(*[c[0].animate.set_fill(ON,.55) for c in g[0][:2]],run_time=.3)
        self.finish()

class S09Method(SpokenScene):
    def construct(self):
        g=lab_cells(True,True);self.add(g,label('identify each responding cell’s receptor',y=3.4,size=32))
        self.at('each responding cell')
        self.play(*[Indicate(c[0],color=ON,scale_factor=1.08) for c in g[0][:2]],run_time=.6)
        self.finish()

class S10Findings(SpokenScene):
    def construct(self):
        g=research_grid();self.add(g)
        self.at('One receptor recognized')
        self.play(*[activate(g[0][i]) for i in [0,3,6]],run_time=.7)
        self.at('One odorant was recognized')
        self.play(*[activate(g[0][i]) for i in [1,2]],run_time=.7)
        self.finish()

class S11Conc(SpokenScene):
    def construct(self):
        g=research_grid()
        for i in [0,3,6,1,2]:g[0][i].set_fill(ON,.9).set_stroke(ON)
        low=VGroup(label('odorant 2',4.75,2.2,32,ODORANT),label('low',4.75,1.55,32,ODORANT),label('concentration',4.75,.9,30,ODORANT));self.add(g,low)
        self.at('odorant activated')
        self.play(Transform(low[1],label('high',4.75,1.55,32,ODORANT)),activate(g[0][4]),Create(Square(1.22,color=ODORANT).move_to(g[0][4])),run_time=.5)
        self.play(Indicate(g[0][4],color=ODORANT,scale_factor=1.1),run_time=.5)
        self.at('combinatorial code')
        self.play(Transform(g[4],label('combinatorial code',y=3.4,size=34,color=BLUE)),run_time=.5)
        self.finish()

class S12Toy(SpokenScene):
    def construct(self):
        key=legend();self.add(matrix(np.zeros((4,4)),headers=False),key)
        self.at('Now practice reading')
        self.play(Indicate(key,scale_factor=1.03),run_time=.5)
        self.finish()

class S13Rules(SpokenScene):
    def construct(self):
        g=matrix(np.zeros((4,4)));self.add(g,legend(),label('real responses are graded and noisy',y=-3.5,size=30,color=MUTED))
        self.at('Four receptors')
        self.play(Indicate(g[1],scale_factor=1.05),run_time=.6)
        self.finish()

class S14Matrix(SpokenScene):
    def construct(self):
        g=matrix(np.zeros((4,4)));note=label('real responses are graded and noisy',y=-3.5,size=30,color=MUTED);self.add(g,note,legend())
        for r,cue in enumerate(['turns on','Odint 2','Odint 3','D alone']):
            self.at(cue)
            self.play(*[activate(g[0][4*r+c]) for c in range(4) if DATA[r,c]],run_time=.5)
        self.finish()

class S15Predict(SpokenScene):
    def construct(self):
        g=matrix(dim=True);self.add(g,pause_tag(),remove_question())
        self.at('Remove receptor')
        new=matrix(removed=True,dim=True)
        self.play(Transform(g[0],new[0]),Transform(g[1],new[1]),FadeIn(new[4]),run_time=.6)
        self.finish()

class S16Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(matrix(removed=True,dim=True),remove_question(),pause_tag());countdown(self)

class S17Reveal(SpokenScene):
    def construct(self):
        g=matrix(removed=True);self.add(g,label('same pattern',y=-3.5,size=34),row_outline(1),row_outline(2))
        self.at('Both now read')
        self.play(FadeIn(label('B C',4.9,YY[1],38)),FadeIn(label('B C',4.9,YY[2],38)),run_time=.5)
        self.finish()

class S18Raise(SpokenScene):
    def construct(self):
        g=matrix(removed=True);sl=slider(False);self.add(g,sl)
        self.at('put receptor A back')
        new=matrix();self.play(Transform(g[0],new[0]),Transform(g[1],new[1]),FadeOut(g[4]),run_time=.6)
        self.at('raise odorant')
        self.play(sl[1].animate.move_to([4.5,1.45,0]),sl[2].animate.move_to([5.5,.95,0]),run_time=3.2,rate_func=linear)
        self.at('Receptor C has')
        self.play(Indicate(g[1][2],color=ODORANT,scale_factor=1.25),run_time=.5)
        self.at('lower affinity')
        note=label('C: lower affinity',1,3.35,26,BLUE)
        self.remove(g[3])
        self.play(FadeIn(note),run_time=.5)
        self.at('higher concentration')
        self.play(Indicate(sl[1],color=ODORANT,scale_factor=1.4),run_time=.5)
        self.finish()

class S19Predict(SpokenScene):
    def construct(self):
        self.add(matrix(high=True,question=True),high_question())
        self.at('What happens')
        self.play(Indicate(label('?',XX[2],YY[0],40,ODORANT),scale_factor=1.2),run_time=.5)
        self.finish()

class S20Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(matrix(high=True,question=True),high_question(),label('Pause and predict',y=-2.1,x=4.85,size=28,color=ODORANT))
        # Bar sits below the retained concentration slider.
        track=Rectangle(width=2,height=.2,color=MUTED).move_to([4.8,-2.8,0]);fill=Rectangle(width=1.96,height=.16,color=ODORANT,fill_opacity=1).move_to(track)
        self.add(track,fill);self.play(fill.animate.stretch(.001,0,about_point=fill.get_left()),run_time=5,rate_func=linear)

class S21Reveal(SpokenScene):
    def construct(self):
        g=matrix(high=True,question=True);self.add(g)
        self.at('C is recruited')
        self.remove(g[-1]);self.play(g[0][2].animate.set_fill(ON,.3).set_stroke(ON),run_time=.35);self.play(activate(g[0][2]),run_time=.45)
        self.at('now reads')
        self.play(Create(row_outline(0)),run_time=.45)
        self.at('the pattern of')
        self.play(Create(row_outline(2)),FadeIn(label('same pattern: A B C',y=-3.5,size=32)),run_time=.5)
        self.finish()

class S22Quality(SpokenScene):
    def construct(self):
        d=DATA.copy();d[0,2]=1
        self.add(matrix(d,high=True),row_outline(0),row_outline(2))
        n=VGroup(label('Odorant 1 at 10×: model predicts it',y=-3.15,size=28),label('could be mistaken for odorant 3',y=-3.6,size=28));self.add(n)
        self.at('Quality can change')
        self.play(Transform(n,VGroup(label('In the model, the pattern changes',y=-3.15,size=28),label('with concentration',y=-3.6,size=28))),run_time=.5)
        self.finish()

class S23Caution(SpokenScene):
    def construct(self):
        card=RoundedRectangle(width=10.2,height=3.8,corner_radius=.3,color=MUTED,fill_opacity=.06)
        self.add(card,label('TOY MODEL',y=1.25,size=40,color=BLUE),label('patterns are not a count of smells',y=.35,size=34))
        self.at('What a mouse can')
        third=VGroup(label('What a mouse can tell apart:',y=-.6,size=32,color=ODORANT),label('behavioural test',y=-1.3,size=36,color=ODORANT))
        self.play(FadeIn(third),run_time=.45)
        self.finish()

class S24Takeaway(SpokenScene):
    def construct(self):
        self.add(label('An odour is read as a pattern',y=3.35,size=38),label('across many lines.',y=2.65,size=38))
        groups=VGroup()
        for k,(cx,col) in enumerate(zip([-4.8,-1.6,1.6,4.8],SMELL)):
            cells=VGroup(*[neuron(cx+dx,col,y=-1).scale(.48,about_point=[cx+dx,-1,0]) for dx in [-.8,-.28,.28,.8]])
            pairs=VGroup(*[Circle(.25,color=col,fill_opacity=.7).move_to([cx+dx,1.45,0]) for dx in [-.45,.45]])
            paths=VGroup()
            for i,n in enumerate(cells):
                n[3].set_opacity(0)
                p=VMobject(color=col,stroke_width=3).set_points_smoothly([n[0].get_top(),[cx+(-.45 if i<2 else .45)+(i%2-.5)*.08,.4,0],pairs[0 if i<2 else 1].get_bottom()]);paths.add(p)
            grp=VGroup(cells,pairs,paths)
            if k>1:
                for m in grp.family_members_with_points():
                    m.set_fill(opacity=m.get_fill_opacity()*.2)
                    m.set_stroke(opacity=m.get_stroke_opacity()*.2)
            groups.add(grp)
        self.add(groups,label('one odour = a pattern across lines',x=-3.2,y=-2.25,size=26,color=ODORANT),label('~2 glomeruli per receptor type per bulb',y=-2.65,size=28,color=MUTED),label('most mature neurons: one receptor gene',y=-3.2,size=28,color=MUTED))
        self.at('a pattern across')
        self.play(*[Indicate(groups[k][1],color=SMELL[k],scale_factor=1.2) for k in [0,1]],run_time=.6)
        self.finish()

class S25End(EndCard):
    LINE='An odour is read as a pattern across many lines.'
    def construct(self):
        self.add(label('An odour is read as a pattern',y=.7,size=40),label('across many lines.',y=-.1,size=40),label('biochemistrypedia.com',y=-1.4,size=28,color=TEAL))
        self.finish()
