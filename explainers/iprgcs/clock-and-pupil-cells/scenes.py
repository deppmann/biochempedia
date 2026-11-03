"""Chapter 5. All anatomy is schematic; no molecular structures.
COLOR MAP: GREEN ipRGCs; GREY conventional cells / reference / structure;
YELLOW light and behavioural output; PURPLE brain targets; RED ablated cells.
Pupil traces use a normalized first-order illustrative model, not measured data:
C(t)=A*(1-exp(-max(t-t_on,0)/tau)); A=1 or .18, tau=.35.
Running bars are categorical daily light-locked intervals, not measured records.
"""
import numpy as np
from bp_style import *
PURPLE='#B58CD9'

def label(s,x,y,size=28,color=TEXT):
    return T(s,size,color).move_to([x,y,0])
def heading(s): return label(s,0,3.12,30)
def arr(a,b,color=GREEN,w=4):
    return Arrow(a,b,buff=0,color=color,stroke_width=w,tip_length=.18)
def cell(x,y,w=1.3,h=.85,color=GREEN):
    return Ellipse(width=w,height=h,color=color,stroke_width=4,fill_color=color,fill_opacity=.22).move_to([x,y,0])
def clock_icon(x,y,r=.52):
    c=np.array([x,y,0.]);return VGroup(Circle(radius=r,color=YELLOW).move_to(c),Line(c,c+[0,r*.7,0],color=YELLOW),Line(c,c+[r*.6,r*.2,0],color=YELLOW))
def eye_icon(x,y,w=1.4):
    return VGroup(Ellipse(width=w,height=w*.57,color=YELLOW).move_to([x,y,0]),Circle(radius=w*.17,color=YELLOW,fill_color=YELLOW,fill_opacity=.5).move_to([x,y,0]))
def tagged(x,y,positive=True,grey=False):
    col=GREY if grey else GREEN
    g=VGroup(cell(x,y,color=col))
    if positive:g.add(chip('Brn3b',col,26,pad=.1).move_to([x,y+.68,0]))
    return g

def neuron(x,y,kind=1,scale=1):
    # Plan-view branching sketches; double arbors signify two depth bands.
    r={1:1.05,2:.85,3:1.05,4:1.48,5:.82,6:.82}[kind]*scale
    g=VGroup(Circle(radius=.17*scale,color=GREEN,fill_color=GREEN,fill_opacity=.5).move_to([x,y,0]))
    if kind in (3,6):
        for yy in [y-.42*scale,y+.42*scale]:
            g.add(Line([x,y,0],[x,yy,0],color=GREEN,stroke_width=3),Line([x-r,yy,0],[x+r,yy,0],color=GREEN,stroke_width=3))
            for dx in ([-.8,-.4,.4,.8] if kind==3 else [-.85,-.6,-.3,.3,.6,.85]):
                tip=np.array([x+dx*r+.12*scale,yy+.18*scale,0])
                g.add(Line([x+dx*r,yy,0],tip,color=GREEN,stroke_width=2))
                if kind==6:
                    g.add(Line(tip,tip+[.16*scale,.08*scale,0],color=GREEN,stroke_width=2))
        return g
    levels=[0]
    n={1:5,2:3,3:4,4:7,5:9,6:5}[kind]
    for lev in levels:
        for i in range(n):
            a=TAU*i/n+.13*kind
            p=np.array([x,y,0]);q=p+np.array([np.cos(a)*r,np.sin(a)*r*.65+lev,0])
            g.add(Line(p,q,color=GREEN,stroke_width=3))
            for turn in [-.65,.65]:
                e=q+np.array([np.cos(a+turn),np.sin(a+turn)*.65,0])*r*.32
                g.add(Line(q,e,color=GREEN,stroke_width=2))
                if kind==5:
                    for t in [-.6,.6]:g.add(Line(e,e+np.array([np.cos(a+t),np.sin(a+t),0])*r*.18,color=GREEN,stroke_width=2))
    return g

def type_grid():
    return VGroup(*[VGroup(neuron(x,y,k,1.05),label('M'+str(k),x,y-1.4,28,GREEN)) for k,(x,y) in enumerate([(-4,1.4),(0,1.4),(4,1.4),(-4,-1.5),(0,-1.5),(4,-1.5)],1)])

def route_stage(ghost=False):
    n=tagged(-4.7,1.45,False);p=tagged(-4.7,-1.25)
    nl=label('Brn3b− M1',-4.7,2.25,28,GREEN);pl=label('Brn3b+ ipRGCs',-4.5,-2.2,28,GREEN)
    sc=chip('SCN',PURPLE,30).move_to([.5,1.45,0]);op=chip('OPN',PURPLE,30).move_to([.5,-1.25,0])
    a=arr([-4,1.45,0],sc.get_left());b=arr([-4,-1.25,0],op.get_left())
    ck=VGroup(arr(sc.get_right(),[3.9,1.45,0],PURPLE),clock_icon(4.5,1.45),label('clock',4.5,.5))
    ey=VGroup(arr(op.get_right(),[3.7,-1.25,0],PURPLE),eye_icon(4.5,-1.25),label('pupil',4.5,-2.2))
    g=VGroup(n,nl,p,pl,sc,op,a,b,ck,ey)
    if ghost:
        p.set_color(RED).set_opacity(.65);b.set_opacity(.18)
        g.add(Line([-5.4,-1.7,0],[-4,-.8,0],color=RED,stroke_width=5),Line([-5.4,-.8,0],[-4,-1.7,0],color=RED,stroke_width=5),Line([-2.8,-1.5,0],[-2.4,-1,0],color=RED,stroke_width=5))
    return g

def attribution():return label('Chen, Badea and Hattar · 2011',0,3.15,28)
def target_names():
    return VGroup(label('SCN: suprachiasmatic nucleus',.5,2.35,26,PURPLE),label('OPN: olivary pretectal nucleus',.5,-.35,26,PURPLE))
def predict_routes(ghost=False):
    g=route_stage(ghost)
    for i in [0,1,4,6,8]:g[i].shift(UP*.2)
    for i in [2,3,5,7,9]:g[i].shift(UP*.55)
    if ghost:
        for m in g[10:]:m.shift(UP*.55)
    return g

def conventional():
    return VGroup(tagged(-1.5,.1,True,True),label('other ganglion cells',2,.1,26,GREY))

def prediction():
    g=predict_routes(True)
    qs=VGroup(chip('Pupil reflex: ?',YELLOW,28).move_to([-3,-2.8,0]),chip('Clock entrainment: ?',YELLOW,28).move_to([3,-2.8,0]))
    return VGroup(g,qs,heading('Pause and predict'))

def panels():
    g=VGroup()
    for x,title in [(-3.25,'Pupil light reflex'),(3.25,'Clock entrainment')]:
        g.add(VGroup(RoundedRectangle(width=6.2,height=6.25,corner_radius=.15,color=GREY).move_to([x,-.1,0]),label(title,x,2.5,30)))
    return g

def pupil_plot():
    x0,x1=-5.1,-.65;y0=-1.65
    g=VGroup(Line([x0,y0,0],[x1,y0,0],color=GREY),Line([x0,y0,0],[x0,.8,0],color=GREY),label('pupil constriction',-3.1,1.65,26),label('time, light on',(x0+x1)/2,-2.4,26),label('schematic',-3.2,-2.85,26,GREY))
    onset=x0+.85
    g.add(DashedLine([onset,y0,0],[onset,1.1,0],color=GREY),label('light on',onset,1.3,26))
    t=np.linspace(-.6,2.5,140)
    for amp,col in [(1,GREY),(.18,YELLOW)]:
        response=amp*(1-np.exp(-np.maximum(t,0)/.35))
        pts=[[onset+u*1.18,y0+v*2.25,0] for u,v in zip(t,response)]
        g.add(VMobject(stroke_color=col,stroke_width=5).set_points_as_corners(pts))
    g.add(label('normal',-1.6,.95,28,GREY),label('after removal',-2.15,-.87,28,YELLOW))
    return g

def running_plot():
    g=VGroup(label('schematic running record',3.25,1.9,26,GREY))
    for xx,title,col in [(2.1,'normal',GREY),(4.7,'after removal',YELLOW)]:
        g.add(label(title,xx,1.25,26,col),DashedLine([xx-.35,.55,0],[xx-.35,-1.75,0],color=GREY),label('lights off',xx,-2.15,26))
        for day,y in enumerate([.25,-.55,-1.35],1):
            if xx==2.1:g.add(label('day '+str(day),.85,y,26,GREY))
            g.add(Line([xx-.35,y,0],[xx+.72,y,0],color=col,stroke_width=10))
    g.add(label('running starts at lights-off',3.25,-2.8,26,YELLOW));return g

def layer_base(off=True):
    return VGroup(heading('Inner plexiform layer'),Rectangle(width=8.8,height=.7,color=GREY,fill_opacity=.13).move_to([1,1.2,0]),Rectangle(width=8.8,height=.7,color=GREY,fill_opacity=.13).move_to([1,-.6,0]),label('outer / OFF' if off else 'outer',-4.8,1.2,26,GREY),label('inner',-4.8,-.6,26,GREY))
def strat_cell(x,kind):
    g=VGroup(cell(x,-2.45,.6,.6),label('M'+str(kind),x,-3.05,28,GREEN))
    for d in {1:[1.2],2:[-.6],3:[1.2,-.6]}[kind]:
        g.add(Line([x,-2.15,0],[x,d,0],color=GREEN,stroke_width=4),Line([x-.85,d,0],[x+.85,d,0],color=GREEN,stroke_width=5))
        for dx in [-.7,-.35,.35,.7]:g.add(Line([x+dx,d,0],[x+dx+.12,d+.2,0],color=GREEN,stroke_width=3))
    return g

class S00Title(TitleCard):
    LESSON='Melanopsin Cells: Light for the Clock and the Pupil'
    TITLE='Separate Cells for\nthe Clock and the Pupil'
class S01Q(SpokenScene):
    def construct(self):
        self.add(VGroup(*[cell(-4.7,y,1.6,1.05) for y in [1.5,0,-1.5]]),clock_icon(3.8,1.5,.85),eye_icon(3.8,-1.5,2.2),arr([-3.9,1.5,0],[2.85,1.5,0]),arr([-3.9,-1.5,0],[2.6,-1.5,0]))
        self.at('Do the same cells');self.play(FadeIn(heading('Same cells or separate?')),run_time=.4)
        self.at('Or do separate cells');self.play(Indicate(self.mobjects[0],color=GREEN),run_time=.6);self.finish()
class S02Marker(SpokenScene):
    def construct(self):
        cs=VGroup(*[tagged(x,y,False,grey) for x,y,grey in [(-4,1.2,True),(0,1.2,True),(4,1.2,False),(-4,-1.4,True),(0,-1.4,True),(4,-1.4,False)]])
        for c in cs:c[0].scale(1.35)
        self.add(cs,heading('Mark a set of ganglion cells'))
        sweep=Rectangle(width=.55,height=5.4,stroke_width=0,fill_color=YELLOW,fill_opacity=.25).move_to([-5.6,0,0])
        self.at('a way to mark');self.add(sweep);self.play(sweep.animate.shift(RIGHT*7.5),run_time=1.3);self.remove(sweep)
        tags=VGroup(*[chip('Brn3b',GREY,26,pad=.1).move_to([x,y+.9,0]) for x in [-4,0] for y in [1.2,-1.4]])
        self.at('Here the marker');self.play(FadeIn(tags),run_time=.5);self.finish()
class S03Def(SpokenScene):
    def construct(self):
        cs=VGroup(*[tagged(x,y,True,True) for x,y in [(-4,.45),(0,.45),(4,.45),(-4,-1.8),(4,-1.8)]])
        m=tagged(0,-1.8,False)
        for c in [*cs,m]:c[0].scale(1.45)
        for c in cs:c[1].shift(UP*.22)
        self.add(cs,m,chip('Brn3b',GREY,30).move_to([-4.5,2.65,0]))
        self.at('is a transcription factor');self.play(FadeIn(label('transcription factor: a protein\nthat switches genes on',1.25,2.65,28)),run_time=.5)
        self.at('Most ganglion cells');self.play(Indicate(cs,color=GREY,scale_factor=1.03),run_time=.6)
        self.at('but a subset');self.play(Indicate(m,color=GREEN),FadeIn(label('Brn3b-negative M1',0,-2.95,26,GREEN)),run_time=.6);self.finish()
class S04Chen(SpokenScene):
    def construct(self):
        g=route_stage();self.add(*g[:6],g[8].copy().set_opacity(.2),g[9].copy().set_opacity(.2),attribution());g[4:6].set_opacity(.3)
        self.at('traced where');self.play(Indicate(g[0],color=GREEN),Indicate(g[2],color=GREEN),run_time=.7);self.finish()
class S05Neg(SpokenScene):
    def construct(self):
        g=route_stage();names=target_names();self.add(*g[:4],g[5].copy().set_opacity(.25),attribution())
        self.at('negative');self.play(Indicate(g[0],color=GREEN),run_time=.5)
        self.at('reach the');self.play(GrowArrow(g[6]),FadeIn(g[4]),FadeIn(names[0]),run_time=.65)
        self.at('the clock');self.play(FadeIn(g[8]),run_time=.45);self.finish()
class S06Pos(SpokenScene):
    def construct(self):
        g=route_stage();names=target_names();self.add(*g[:5],g[6],g[8],names[0],attribution())
        self.at('positive');self.play(Indicate(g[2],color=GREEN),run_time=.5)
        self.at('reach the');self.play(GrowArrow(g[7]),FadeIn(g[5]),FadeIn(names[1]),run_time=.65)
        self.at('which drives');self.play(FadeIn(g[9]),run_time=.5);self.finish()
class S07Predict(SpokenScene):
    def construct(self):
        g=predict_routes();ghost=predict_routes(True)
        other=conventional()
        self.add(g,heading('Predict'),other)
        self.at('Kill only');self.play(g[2].animate.set_color(RED).set_opacity(.65),g[7].animate.set_opacity(.18),FadeIn(VGroup(*ghost[10:])),run_time=1.5)
        self.at('leaving other');self.play(Indicate(other,color=GREY),run_time=.6)
        qs=prediction()[1]
        self.at('What happens');self.play(FadeIn(qs[0]),run_time=.45)
        self.at('And to the clock');self.play(FadeIn(qs[1]),run_time=.45);self.finish()
class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(prediction(),conventional())
        bar=Line([-5.7,-3.4,0],[5.7,-3.4,0],color=YELLOW,stroke_width=4);self.add(bar)
        self.play(bar.animate.stretch(.001,0,about_point=bar.get_left()),run_time=5,rate_func=linear)
class S09Reveal(SpokenScene):
    def construct(self):
        self.add(panels())
        self.at('The pupil light reflex');self.play(FadeIn(pupil_plot()),run_time=.45)
        self.at('severely impaired');self.play(FadeIn(label('severely impaired',-3.25,3.45,28,RED)),run_time=.35)
        self.at('But circadian');self.play(FadeIn(running_plot()),run_time=.5)
        self.at('was spared');self.play(FadeIn(label('spared',3.25,3.45,28,GREEN)),run_time=.35);self.finish()
class S10Why(SpokenScene):
    def construct(self):
        g=route_stage(True).shift(DOWN*.35)
        for i in [2,3,5,7,9]:g[i].set_opacity(.22)
        for m in g[10:]:m.set_opacity(.22)
        path=VGroup(g[0],g[1],g[6],g[4],g[8])
        self.add(g,heading('Clock route retained'))
        self.at('negative cells');self.play(Indicate(VGroup(g[0],g[1]),color=GREEN,scale_factor=1.08),run_time=.6)
        self.at('were still there');self.play(Indicate(path,color=YELLOW,scale_factor=1.04),run_time=1);self.finish()
class S11Meaning(SpokenScene):
    def construct(self):
        # Separate into two spacious panels; mixed cells on the pupil branch.
        top=VGroup(tagged(-3,.6,False),arr([-2.3,.6,0],[2.2,.6,0]),clock_icon(3,.6),label('clock route',0,1.5,28),label('Brn3b− M1',-3,1.35,26,GREEN))
        bottom=VGroup(neuron(-3,-.6,2,.45),neuron(-1.6,-.6,5,.5),arr([-.7,-.6,0],[2.1,-.6,0]),eye_icon(3,-.6),label('pupil output set',0,-1.5,28))
        self.add(top,bottom)
        self.at('partly different cells');self.play(FadeIn(heading('Partly different cells: outputs can be pulled apart')),run_time=.5)
        self.at('can be pulled apart');self.play(top.animate.shift(UP*1.15),bottom.animate.shift(DOWN*1.15),run_time=.75);self.finish()
class S12Caution(SpokenScene):
    def construct(self):
        ns=VGroup(*[neuron(x,0,k,.82 if k==4 else .95) for x,k in [(-4.4,1),(-1.5,4),(1.5,5),(4.4,6)]]).shift(DOWN*.45)
        tags=VGroup(*[chip('Brn3b+',GREEN,26,pad=.1).move_to([x,1.25,0]) for x in [-4.4,-1.5,1.5,4.4]])
        bracket=Brace(ns,DOWN,color=GREY)
        self.add(ns,tags,heading('A mixed set of ipRGCs'))
        self.at('marks an');self.play(FadeIn(bracket),FadeIn(label('output set',0,-2.4,30,GREEN)),run_time=.55)
        self.at('not one morphological type');self.play(FadeIn(chip('Not one morphological subtype',TEXT,28).move_to([0,-3.15,0])),run_time=.5);self.finish()
class S13Types(SpokenScene):
    def construct(self):
        g=type_grid();self.add(g,heading('Mouse ipRGCs · schematic dendrite shapes'),label('M3 and M6: dendrites in both bands',0,-3.5,26,GREY))
        self.at('a varied population');self.play(Indicate(g,color=GREEN,scale_factor=1.025),run_time=.6)
        self.at('are named');self.play(Indicate(VGroup(*[n[1] for n in g]),color=YELLOW),run_time=.6);self.finish()
class S14Ipl(SpokenScene):
    def construct(self):
        base=layer_base(False);cs=VGroup(*[strat_cell(x,k) for x,k in [(-2,1),(1,2),(4,3)]])
        contact=label('bipolar cells\ncontact here',-5.25,.3,24,GREY)
        # A single bracket spans both bands, entirely outside the dendrite field.
        leads=VGroup(Line([-3.7,1.55,0],[-3.7,-.95,0],color=GREY),Line([-3.7,1.55,0],[-3.4,1.55,0],color=GREY),Line([-3.7,-.95,0],[-3.4,-.95,0],color=GREY))
        base[3].move_to([-4.7,1.8,0]);base[4].move_to([-4.7,-1.2,0])
        self.add(base,cs,contact,leads)
        self.at('differ in shape');self.play(Indicate(cs,color=GREEN,scale_factor=1.02),run_time=.5)
        self.at('where their dendrites sit');self.play(Indicate(VGroup(base[1],base[2]),color=GREEN,scale_factor=1.015),run_time=.5)
        # Axonal destinations are taught explicitly in the later target scene;
        # no unsupported axon caption is left in this layer-only diagram.
        self.finish()
class S15M1(SpokenScene):
    def construct(self):
        c=strat_cell(1,1);self.add(layer_base(),c,label('outermost stratum',1,2.15,28,GREEN),label('dendrites',4.1,1.95,26,GREEN),Line([3.4,1.8,0],[1.85,1.35,0],color=GREEN),label('cell body',-1.3,-1.6,26,GREEN),Line([-.3,-1.75,0],[.65,-2.3,0],color=GREEN))
        icons=VGroup(clock_icon(-4,-2.55,.45),eye_icon(4.5,-2.55,1.2),label('clock',-4,-3.25,26),label('pupil',4.5,-3.25,26),arr([.7,-2.1,0],[-3.5,-2.35,0]),arr([1.3,-2.1,0],[3.8,-2.35,0]))
        self.at('classic clock and pupil');self.play(FadeIn(icons),run_time=.55)
        self.at('Their dendrites');self.play(Indicate(c[3],color=YELLOW),run_time=.5);self.finish()
class S16Off(SpokenScene):
    def construct(self):
        base=layer_base();base[4].become(label('inner band',-4.8,-.6,26,GREY))
        self.add(base,strat_cell(2.8,1),label('outermost stratum',1,2.3,28,GREEN))
        note=label('OFF = where the dendrites sit',-.9,.4,26)
        leader=VGroup(Line([1.6,.65,0],[1.6,1.2,0],color=GREY),Line([1.6,1.2,0],[1.95,1.2,0],color=GREY))
        self.at('conventionally called off');self.play(FadeIn(note),Create(leader),run_time=.55)
        self.at('not the');self.play(FadeIn(label('not the cell’s own response',-.9,0,26)),run_time=.5);self.finish()
class S17M23(SpokenScene):
    def construct(self):
        a=strat_cell(1,2);b=strat_cell(4,3);ref=strat_cell(-2,1).set_opacity(.4)
        self.add(layer_base(),ref,a,b,label('Dendrites: outer band, inner band or both',0,2.35,26))
        self.at('M2');self.play(Indicate(a,color=YELLOW,scale_factor=1.03),run_time=.5)
        self.at('M3 cells');self.play(Indicate(b,color=YELLOW,scale_factor=1.03),run_time=.6);self.finish()
class S18M4(SpokenScene):
    def construct(self):
        n=neuron(0,-.4,4,1.4);self.add(n,heading('M4 · mouse sustained ON alpha cell'),label('ON: more firing with light increase',0,2.2,28),label('response type',0,1.65,26,GREY))
        self.at('sustained on alpha cell');self.play(Indicate(n,color=GREEN,scale_factor=1.03),run_time=.5)
        light=VGroup(arr([3.5,.75,0],[.3,-.3,0],YELLOW),label('light',3.7,1.15,28,YELLOW),Circle(radius=.4,color=YELLOW,stroke_width=6).move_to([0,-.4,0]))
        self.at('intrinsically photosensitive');self.play(FadeIn(light),FadeIn(label('intrinsically photosensitive',0,-3,28,GREEN)),run_time=.6);self.finish()
class S19M56(SpokenScene):
    def construct(self):
        ns=VGroup(neuron(-3.6,1.25,5,1.8),neuron(-3.6,-1.8,6,1.8))
        target=chip('dLGN\nthalamic relay',PURPLE,30).move_to([3,0,0])
        self.add(ns,label('M5',-6.1,1.25,28,GREEN),label('M6',-6.1,-1.8,28,GREEN),target,heading('Dorsal lateral geniculate nucleus'))
        self.at('send axons');self.play(GrowArrow(arr([-3.6,1.25,0],target[0].get_left()+UP*.25)),GrowArrow(arr([-3.6,-1.8,0],target[0].get_left()+DOWN*.25)),run_time=.7)
        self.at('thalamic relay');self.play(Indicate(target,color=PURPLE),run_time=.5)
        self.at('vision');self.play(FadeIn(label('image-forming vision',3,-2,28)),run_time=.35);self.finish()
class S20Letters(SpokenScene):
    def construct(self):
        self.add(type_grid(),heading('Mouse names, not human types'),label('M3 and M6: dendrites in both bands',0,-3.5,26,GREY))
        self.at('not six matching');self.play(Indicate(self.mobjects[1],color=YELLOW,scale_factor=1.025),run_time=.6);self.finish()
class S21Take(SpokenScene):
    def construct(self):
        simple=VGroup()
        for x,name,icon in [(-3,'clock route',clock_icon(-3,.6)),(3,'pupil route',eye_icon(3,.6))]:
            simple.add(cell(x,1.9),label(name,x,2.6,28),arr([x,1.45,0],[x,1.18,0]),icon)
        row=VGroup(*[VGroup(neuron(x,-1.7,k,.58 if k==4 else .66),label('M'+str(k),x,-2.6,26,TEXT)) for k,x in enumerate(np.linspace(-5,5,6),1)]).set_opacity(.55)
        self.add(simple,heading('Output sets'))
        self.at('can separate');self.play(Indicate(simple,color=GREEN,scale_factor=1.02),run_time=.6)
        self.at('It cannot');self.play(FadeIn(row),FadeIn(label('Which subtype?',0,-.35,28,YELLOW)),FadeIn(label('A marker alone cannot name the subtype.',0,-3.25,28)),run_time=.55);self.finish()
class S22End(EndCard):
    LINE='A marker can separate clock and pupil routes,\nbut cannot by itself name the subtype behind each job.'
    def construct(self):
        # Full caveat takes precedence over the original twelve-word card rule.
        self.add(label('A marker can separate clock and pupil routes,',0,.65,32),label('but cannot by itself name the subtype behind each job.',0,-.15,30),label('biochemistrypedia.com',0,-1.5,26,TEAL));self.finish()
