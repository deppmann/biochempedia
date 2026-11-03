"""Chapter 3 — revised, word-aligned schematic experiments.
COLOR MAP: INDIGO #9B8CF2 capsule; TEAL lamellar cells; YELLOW nerve/spikes;
GREEN current/Piezo2; ORANGE force; BLUE light; RED absence; light GREY labels.
Orange and magenta distinguish the two genetically labelled Meissner afferents.
Curves: sine input, shifted sine output, exponential adapting current model.
Latency dots and spike rasters are explicitly schematic, never sampled trial data.
"""
import importlib.util
from pathlib import Path
import numpy as np
from bp_style import *
from bp_style import SpokenScene as BaseSpokenScene
_spec=importlib.util.spec_from_file_location('reference',Path(__file__).resolve().parent.parent/'scenes.old.py')
_old=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_old)
ORANGE,INDIGO=_old.ORANGE,_old.INDIGO
GREY='#C2C8D2'; MAGENTA='#EE78C6'

class Scene(Scene):
    def setup(self):
        super().setup()
        self.camera.background_color=BG
poly,mouse=_old.poly,_old.mouse

class SpokenScene(BaseSpokenScene):
    # Same word alignment without writing an unrequested sync.log artifact.
    def at(self,phrase,lead=.2,nth=0):
        rest=self.t_of(phrase,nth)-lead-self.elapsed()
        if rest>.02: self.wait(rest)

def heading(s): return T(s,34,font=TITLE_FONT).move_to([0,3.12,0])
def tag(s,color=GREY,y=-3.5): return T(s,28,color).move_to([0,y,0])
def label(s,p,q,color=GREY,size=28):
    t=T(s,size,color).move_to(p)
    direction=np.array(q)-t.get_center()
    start=t.get_boundary_point(direction)+.12*direction/np.linalg.norm(direction)
    return VGroup(Line(start,q,color=color,stroke_width=2),t)
def core(x=-2.8,y=-.1):
    # Enlarged wrapping-cell cross section. Cell inner faces touch axon membrane.
    term=RoundedRectangle(width=3.8,height=.7,corner_radius=.25,color=YELLOW,fill_opacity=.25).move_to([x,y,0])
    top=RoundedRectangle(width=4.65,height=2.25,corner_radius=.55,color=TEAL,fill_opacity=.2).move_to([x,y+1.475,0])
    bot=top.copy().move_to([x,y-1.475,0])
    axon=Line([x-3,y,0],[x-1.9,y,0],color=YELLOW,stroke_width=8)
    g=VGroup(top,bot,term,axon); g.top,g.bot,g.term,g.axon=top,bot,term,axon
    return g.scale(1.12,about_point=[x,y,0])

def anatomy_labels():
    return VGroup(label('lamellar cells',[3,1.25,0],[-.65,1.2,0],TEAL),label('nerve ending',[3,-.6,0],[-.9,-.1,0],YELLOW))
def force(): return Arrow([-3.8,2.8,0],[-3.8,2.2,0],buff=0,color=ORANGE,stroke_width=7)
def channels():
    return VGroup(*[VGroup(Line([x-.18,-.04,0],[x-.18,.65,0],color=GREEN,stroke_width=9),Line([x+.18,-.04,0],[x+.18,.65,0],color=GREEN,stroke_width=9)) for x in (-3.7,-2)])
def raster(xs,y=-1.6,x0=.6,x1=5.8):
    return VGroup(Line([x0,y,0],[x1,y,0],color=GREY),*[Line([x,y,0],[x,y+.65,0],color=YELLOW,stroke_width=5) for x in xs])
def clear(s): s.play(*[FadeOut(m) for m in list(s.mobjects)],run_time=.3)
def replace_all(s,g):
    s.remove(*list(s.mobjects));s.add(g);s.wait(.2)

def delay_panel():
    # Log position is proportional to log(time); only endpoints are measured bounds.
    x=lambda ms:-5.5+11*np.log10(ms/5)/np.log10(9000/5)
    title=T('Duck Grandry: delay after depolarizing\none wrapping cell',32,TEAL).move_to([0,2.75,0])
    axis=Line([-5.5,-1.7,0],[5.5,-1.7,0],color=GREY)
    ticks=VGroup()
    for v,txt in [(5,'5 ms'),(50,'50 ms'),(500,'500 ms'),(5000,'5 s')]:
        ticks.add(Line([x(v),-1.8,0],[x(v),-1.6,0],color=GREY),M(txt,28,GREY).move_to([x(v),-2.15,0]))
    points=VGroup(*[Dot([x(v),y,0],radius=.11,color=TEAL) for v,y in zip(np.geomspace(20,9000,8),[.9,.35,1.2,.1,.65,1.35,.3,.95])])
    ends=VGroup(M('20 ms',28,TEAL).move_to([x(20),1.65,0]),M('~9 s',28,TEAL).move_to([x(9000),1.65,0]))
    ref=VGroup(Line([-5.5,-1.4,0],[-5.5,-.75,0],color=ORANGE,stroke_width=5),T('one cycle',28,ORANGE).move_to([-4.7,-.4,0]))
    return VGroup(title,axis,ticks,points,ends,ref,tag('reported range, schematic · logarithmic time axis'))

def clock():
    ax=Axes(x_range=[0,5,1],y_range=[-1,1,1],x_length=10.5,y_length=4.5,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([0,.1,0])
    c=ax.plot(lambda t:np.sin(2*np.pi*200*t/1000),x_range=[0,5,.015],color=ORANGE)
    return VGroup(heading('200 Hz vibration'),ax,c,M('0',28).move_to([-5.25,-2.5,0]),M('5 ms',30,ORANGE).move_to([5.1,-2.5,0]),tag('time → · one complete cycle = 5 ms',ORANGE))
def question():
    return VGroup(heading('Predict'),T('One signal per cycle?',46,GOLD).move_to([0,1.25,0]),
        chip('5 ms cycle',ORANGE,32).move_to([-3,-.2,0]),chip('20 ms to about 9 s',TEAL,32).move_to([2.6,-.2,0]),
        T('Delay after electrical activation\nof one duck Grandry wrapping cell',30,TEAL).move_to([0,-1.7,0]),tag('Could the wrapping cells pass on each cycle?'))

def threshold(factor=1,touch=False):
    maxv=20 if touch else 5; control=10 if touch else 1
    base=-2.15; height=3.6
    axis=VGroup(Line([-4.8,base,0],[5.5,base,0],color=GREY),Line([-4.8,base,0],[-4.8,1.6,0],color=GREY))
    for v in ([0,10,20] if touch else [0,1,3,5]):
        yy=base+height*v/maxv
        axis.add(Line([-4.9,yy,0],[-4.7,yy,0],color=GREY),M(str(v),28,GREY).move_to([-5.3,yy,0]))
    a=Rectangle(width=1.5,height=height*control/maxv,color=ORANGE,fill_opacity=.65).move_to([-2.4,base+height*control/maxv/2,0])
    b=Rectangle(width=1.5,height=height*control*factor/maxv,color=ORANGE,fill_opacity=.65).move_to([2.2,base+height*control*factor/maxv/2,0])
    labs=VGroup(T('control' if touch else 'cells active',28).move_to([-2.4,-2.55,0]),T('without corpuscles' if touch else 'cells silenced',28).move_to([2.2,-2.55,0]))
    nums=VGroup(M('~10 mN' if touch else '1×',30,ORANGE).next_to(a,UP,buff=.15),M(('~20 mN' if factor==2 else '~10 mN') if touch else ('~5×' if factor==5 else '1×'),30,ORANGE).next_to(b,UP,buff=.15))
    unit=T('force (mN)' if touch else 'vibration size needed to detect\n(relative to control)',28,GREY).move_to([0,2.3,0])
    return VGroup(axis,a,b,labs,nums,unit)
def sensitivity_note(): return tag('higher bar = needs more force = less sensitive',ORANGE)
def detected(): return label('still detected\nat about 20 mN',[4.7,2.05,0],[2.95,1.45,0],YELLOW,26)

def meissner(two=False):
    # Two parallel fibres occupy the central corridor between lamellar bodies.
    cx=-1.8
    cells=VGroup(*[RoundedRectangle(width=1.7,height=.7,corner_radius=.33,color=TEAL,fill_opacity=.2).move_to([cx+side*1.3,y,0]) for y in (-1.75,-.6,.6,1.75) for side in (-1,1)])
    def nerve(dx,col):
        ys=np.linspace(-2.6,2.25,150)
        return poly([(cx+dx+.10*np.sin(2*y),y) for y in ys],col,7)
    a=nerve(-.23,ORANGE if two else YELLOW); b=nerve(.23,MAGENTA)
    pap=RoundedRectangle(width=5.1,height=5.8,corner_radius=1.3,color=GREY,fill_opacity=.04).move_to([cx,-.1,0])
    g=VGroup(pap,cells,a)
    if two:g.add(b)
    g.cells,g.a,g.b=cells,a,b
    return g

def branch_scene():
    b=RoundedRectangle(width=12,height=.55,corner_radius=.18,color='#AC7954',fill_opacity=.7).move_to([0,-1.05,0])
    grain=VGroup(*[Line([-5.7,y,0],[5.7,y+.06,0],color='#D5A777',stroke_width=2) for y in (-1.18,-.98)])
    a=mouse().scale(3.1).move_to([2.6,.5,0])
    return VGroup(b,grain),a

class S00Title(TitleCard):
    LESSON='Meissner and Pacinian Corpuscles: Flutter and Vibration'
    TITLE='The Cells That Help It Feel'
    def construct(self):
        self.add(T('BIOCHEMISTRYPEDIA',28,TEAL).move_to([0,2.35,0]),T('Meissner and Pacinian Corpuscles:\nFlutter and Vibration',30,GREY).move_to([0,1.1,0]))
        self.play(FadeIn(T(self.TITLE,44,font=TITLE_FONT).move_to([0,-.4,0])),run_time=.7);self.finish()
class S01Q(SpokenScene):
    def construct(self):
        g=core(0).scale(.98); outer=VGroup(*[Ellipse(width=5.5+i*.45,height=4.4+i*.4,color=INDIGO) for i in range(3)])
        self.add(g,outer,heading('The inner core'))
        self.at('Peel away the onion');self.wait(1.9)
        self.play(FadeOut(outer,shift=UP*.4),run_time=1)
        self.at('nerve ending');self.play(Indicate(g.top,scale_factor=1.03),Indicate(g.bot,scale_factor=1.03),run_time=.5)
        self.play(FadeIn(T('What do they add?',42,GOLD).move_to([0,-3.5,0])),run_time=.3)
        self.finish();self.wait(1.2)
class S02Piezo(SpokenScene):
    def construct(self):
        g=core();c=channels();self.add(g,heading('Force becomes current'),anatomy_labels())
        self.at('First the settled step');self.play(FadeIn(c),run_time=.4)
        self.at('In mice');self.play(FadeIn(tag('mouse · sensory axon')),run_time=.3)
        self.at('force opens a channel');self.play(GrowArrow(force()),*[v[0].animate.shift(LEFT*.12) for v in c],*[v[1].animate.shift(RIGHT*.12) for v in c],run_time=.5)
        self.at('called');self.play(FadeIn(VGroup(T('Piezo2',32,GREEN).move_to([1.4,2.15,0]),poly([(.6,2.15),(-.8,2.15),(-1.5,1.8),(-2,.65)],GREEN,2))),run_time=.3)
        ions=VGroup(*[Dot([x,.8,0],radius=.09,color=GREEN) for x in (-3.7,-2)])
        self.add(ions);self.play(ions.animate.shift(DOWN*.95),FadeIn(T('ion current into axon',28,GREEN).move_to([2.8,-1.8,0])),run_time=.9);self.finish()
class S03Delete(SpokenScene):
    def construct(self):
        g=core();self.add(g,channels(),heading('Wrapping-cell Piezo2 deletion'),tag('mouse · non-neuronal deletion'))
        gene=chip('Piezo2 gene',TEAL,28).move_to([-2.8,1.15,0]);self.add(gene)
        self.at('Delete it from the wrapping cells');self.play(Create(Cross(Square(side_length=.5).move_to([-4.65,1.15,0]),stroke_color=RED,stroke_width=5)),run_time=.65)
        self.at('touch responses stay');self.play(GrowArrow(force()),Create(raster([1,1.7,2.9,4.3],y=-.65)),FadeIn(T('axon still fires',32,GREEN).move_to([3,1,0])),run_time=.7)
        self.finish();self.wait(1)
class S04Feel(SpokenScene):
    def construct(self):
        g=core();self.add(g,heading('Wrapping cells feel force too'))
        pip=poly([(-.8,2.1),(-2,1.25),(-1.7,1.8),(-.7,2.45)],GREY,4)
        self.at('the wrapping cells');self.play(Create(pip),FadeIn(label('recording electrode',[3,2.1,0],[-1,2.1,0])),run_time=.4)
        self.at('feel force too');self.play(GrowArrow(force()),g.top.animate.set_fill(TEAL,.5),run_time=.4)
        self.at('In duck bill');self.play(FadeIn(tag('duck bill skin · normalized adapting-current model',y=-3.4)),run_time=.3)
        ax=Axes(x_range=[0,1,.2],y_range=[-1.1,0,.5],x_length=5,y_length=3.4,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([3,-.45,0])
        # Single schematic inward transient on onset; no offset kinetics attributed to the cell.
        def current(t):return -(np.exp(-(t-.15)/.055) if t>=.15 else 0)
        cur=ax.plot(current,x_range=[0,1,.002],color=GREEN,use_smoothing=False)
        stim=poly([( .5,-2.5),(1.25,-2.5),(1.25,-2.2),(4,-2.2),(4,-2.5),(5.5,-2.5)],ORANGE,4)
        self.at('their own mechanically activated currents');self.play(Create(ax),Create(cur),Create(stim),FadeIn(T('inward current ↓',28,GREEN).move_to([3,1.65,0])),run_time=.8)
        self.add(T('press on / off · time →',28,ORANGE).move_to([3,-2.8,0]));self.finish()
class S05Drive(SpokenScene):
    def construct(self):
        g=core();self.add(g,heading('Duck Grandry · Meissner type'),tag('schematic electrical activation and first spikes'))
        self.at('depolarizing one wrapping cell');self.play(FadeIn(VGroup(Line([.6,-2.25,0],[5.8,-2.25,0],color=GREY),T('time →',28).move_to([5.2,-2.65,0]))),GrowArrow(Arrow([-.2,2.3,0],[-2,1.1,0],buff=0,color=TEAL)),g.top.animate.set_fill(TEAL,.7),FadeIn(T('current injected',28,TEAL).move_to([2.4,2.25,0])),run_time=.5)
        rows=VGroup()
        for y,gap,xs in [( .35,1.5,[2.3,3.5,5.1]),(-.95,2.5,[3.3,4.8]),(-2.25,3.4,[4.2,5.5])]:
            row=VGroup(raster(xs,y=y),Line([.8,y-.1,0],[.8,y+.6,0],color=TEAL),DoubleArrow([.85,y+.85,0],[.8+gap,y+.85,0],buff=0,color=TEAL,tip_length=.12))
            rows.add(row)
        self.at('could make its fiber fire');self.play(Create(rows[0]),run_time=.8)
        self.at('after a variable delay');self.play(Create(rows[1]),run_time=.65);self.play(Create(rows[2]),run_time=.65)
        self.add(T('variable delay',28,TEAL).move_to([2.6,1.65,0]));self.finish();self.wait(1.8)
class S06Mouse(SpokenScene):
    def construct(self):
        g=core();self.add(g,heading('Mouse Pacinian wrapping cells'),T('optogenetic activation',28,BLUE).move_to([3,2,0]),raster([],y=-1.3))
        light=Arrow([-3,2.5,0],[-3,1.8,0],color=BLUE,buff=0)
        self.at('on with light');self.add(T('blue light',30,BLUE).move_to([3,.95,0]))
        for i in range(3):
            self.play(FadeIn(light),g.top.animate.set_fill(TEAL,.65),run_time=.18)
            self.play(Create(Line([1.3+i*1.6,-1.3,0],[1.3+i*1.6,-.55,0],color=YELLOW,stroke_width=5)),FadeOut(light),g.top.animate.set_fill(TEAL,.2),run_time=.23)
        self.at('drove the fiber');self.add(tag('Chen and colleagues, 2025'));self.finish();self.wait(1)
class S07Off(SpokenScene):
    def construct(self):
        c=threshold();c[2].set_opacity(0);c[4][1].set_opacity(0)
        self.add(heading('Vibration detection threshold'),c,tag('awake mice · hindpaw vibration'))
        self.at('Switching them off');self.play(Indicate(c[3][1],color=TEAL),run_time=.4)
        self.at('about five times larger');self.play(Transform(c,threshold(5)),run_time=.9);self.finish()
class S08Beat(Scene):
    def construct(self):
        self.add(heading('Vibration detection threshold'),threshold(5),tag('awake mice · optogenetic silencing of lamellar cells'))
        self.play(FadeIn(T('about five times larger',30,ORANGE).move_to([-1.15,.65,0])),run_time=.4);self.wait(2.6)
class S09Caveat(SpokenScene):
    def construct(self):
        g=core();self.add(g,heading('What the experiments establish'))
        self.at('these cells contribute');self.play(Indicate(g.top,scale_factor=1.03),FadeIn(label('contributes to detection',[3,1.3,0],[-.5,1.2,0],TEAL)),run_time=.5)
        self.at('How they normally do it');self.play(FadeIn(T('?',60,GOLD).move_to([-2.8,1.15,0])),FadeIn(label('normal mechanism\nunknown',[3,-.8,0],[-.5,.9,0],GOLD)),run_time=.5);self.finish()
class S10Clock(SpokenScene):
    def construct(self):
        self.add(clock());self.at('delays ran from');replace_all(self,delay_panel());self.finish()
class S11Predict(SpokenScene):
    def construct(self):
        self.add(delay_panel());self.at('Could those cells');replace_all(self,question());self.finish()
class S12Pause(Scene):
    def construct(self):self.add(question());self.wait(5)
class S13Reveal(SpokenScene):
    def construct(self):
        self.add(heading('A steady delay keeps every cycle, just later'))
        x=np.linspace(-5.5,5.5,500)
        a=poly([(v,1+ .65*np.sin(2*np.pi*3*(v+5.5)/11)) for v in x],ORANGE,4)
        b=poly([(v,-1+.65*np.sin(2*np.pi*3*(v+5.5)/11-np.pi/2)) for v in x],TEAL,4)
        self.add(a,T('input',28,ORANGE).move_to([-4.6,2.2,0]))
        self.at('A steady delay');self.play(Create(b),FadeIn(T('output, delayed copy',28,TEAL).move_to([3,-2.2,0])),run_time=.5)
        self.at('shift every cycle');self.play(FadeIn(VGroup(DoubleArrow([-4.58,.05,0],[-3.66,.05,0],buff=0,color=GOLD,tip_length=.12),T('same delay every cycle',30,GOLD).move_to([1,.05,0]))),run_time=.4)
        self.at('But the slow scattered firing');p=delay_panel();replace_all(self,p)
        # Five actual cycle boundaries positioned on the same logarithmic scale.
        tick_x=lambda ms:-5.5+11*np.log10(ms/5)/np.log10(9000/5)
        comb=VGroup(*[Line([tick_x(ms),-1.25,0],[tick_x(ms),-.8,0],color=ORANGE) for ms in (5,10,15,20,25)])
        self.play(Create(comb),FadeIn(T('5 ms cycles',28,ORANGE).move_to([-.8,-1.05,0])),run_time=.4)
        self.at('suggests a supporting role');self.play(Transform(p[-1],tag('slow, variable first spikes: supporting role suggested',GOLD)),run_time=.4);self.finish()
class S13bOpen(SpokenScene):
    def construct(self):
        g=core();h=heading('Duck Grandry · Meissner type');self.add(g,h)
        chain=VGroup(T('electrical depolarization\nof one wrapping cell',30,TEAL).move_to([3,1.65,0]),Arrow([3,1,0],[3,.45,0],buff=0,color=GREY),T('variable first-spike delay',28,TEAL).move_to([3,.05,0]),Arrow([3,-.35,0],[3,-.9,0],buff=0,color=GREY),T('cycle following:\nnot measured',30,GOLD).move_to([3,-1.6,0]))
        self.at('Those delays followed electrical depolarization');self.play(FadeIn(chain[0]),g.top.animate.set_fill(TEAL,.65),run_time=.5)
        self.at('not vibration');self.play(FadeIn(chain[1:3]),FadeIn(tag('electrical activation · not a vibration-response test')),run_time=.5)
        self.at('Passing each cycle needs');self.play(FadeIn(chain[3:]),run_time=.5)
        self.at('wrapping cells',nth=0)
        p=_old.corpuscle().scale(1.8).stretch(.9,0).move_to([-2.7,0,0])
        replace_all(self,VGroup(p,heading('Pacinian wrapping cells: question open'),label('?', [2.8,.8,0],[-1.9,.6,0],GOLD,72),T('direct cycle-following\ntest still needed',30,GOLD).move_to([3.2,-1.3,0])));self.finish()
class S14Meissner(SpokenScene):
    def construct(self):
        m=meissner(True);m.b.set_stroke(opacity=0);self.add(m,heading('Mouse Meissner · most corpuscles'),tag('dermal papilla · two distinct afferents'))
        self.at('hold a surprise too');self.play(Indicate(m.cells),run_time=.5)
        self.at('two molecularly distinct nerve fibers');self.play(m.b.animate.set_stroke(opacity=1),run_time=.7)
        self.at('told apart by genetic labels');self.play(FadeIn(VGroup(T('Ret label',32,ORANGE).move_to([3.4,1.8,0]),poly([(2.35,1.8),(.95,2.65),(-2.1,2.65),(-2.1,2.2)],ORANGE,2))),FadeIn(VGroup(T('TrkB-lineage label',30,MAGENTA).move_to([3.65,-1.8,0]),poly([(1.8,-1.8),(.95,-2.7),(-1.5,-2.7),(-1.5,-2.3)],MAGENTA,2))),run_time=.5);self.finish()
class S15Double(SpokenScene):
    def construct(self):
        m=meissner(True);self.add(m,heading('TrkB absent from sensory neurons'),tag('developmental deletion'))
        self.at('from development');self.play(Indicate(m.a,color=RED),run_time=.4)
        self.at('grew up without');self.play(FadeOut(m.cells,scale=.1),FadeOut(m.a,scale=.1),FadeOut(m.b,scale=.1),run_time=.65)
        self.play(FadeIn(T('Meissner corpuscles\nabsent',32,RED).move_to([-1.8,.6,0])),run_time=.3)
        self.at('They needed');c=threshold(touch=True);c[2].set_opacity(0);c[4][1].set_opacity(0);replace_all(self,VGroup(heading('Touch detection threshold'),c,tag('developmental deletion')))
        self.at('about twice the push');self.play(Transform(c,threshold(2,True)),run_time=.8);self.finish()
class S16Contrib(SpokenScene):
    def construct(self):
        c=threshold(2,True);self.add(heading('Touch detection threshold'),c,tag('developmental deletion'))
        self.at('They still detected stronger pushes');self.play(FadeIn(detected()),run_time=.5)
        self.at('help set sensitivity');self.remove(self.mobjects[2]);self.add(sensitivity_note());self.play(Indicate(c[2],color=ORANGE,scale_factor=1.03),run_time=.5)
        self.at('detection survived without them');self.play(Indicate(c[2],color=YELLOW,scale_factor=1.03),run_time=.6);self.finish()
class S17Beat(Scene):
    def construct(self):self.add(heading('Touch detection threshold'),threshold(2,True),sensitivity_note(),detected());self.wait(3)
class S18Wild(SpokenScene):
    def construct(self):
        b,a=branch_scene();a.shift(LEFT*.8);self.add(b,a,heading('Single Pacinian neuron · awake mouse'),tag('DRG recording · Turecek and Ginty, 2024'),T('schematic spike raster',28,YELLOW).move_to([-3.4,1.9,0]),raster([],y=1,x0=-5.8,x1=-1.6))
        self.at('In freely moving mice');self.play(a.animate.shift(RIGHT*.6),run_time=1)
        self.at('fired during')
        for x in (-5.4,-4.6,-3.8,-2.7,-2):
            self.play(a.animate.shift(RIGHT*.12),Create(Line([x,1,0],[x,1.65,0],color=YELLOW,stroke_width=5)),run_time=.27)
        self.finish()
class S19Tap(SpokenScene):
    def construct(self):
        b,a=branch_scene();self.add(b,a,heading('The most sensitive Pacinian neurons'),T('schematic, not to scale in time',28,GREY).move_to([0,-3.25,0]))
        measure=VGroup(DoubleArrow([-5.3,-1.95,0],[2.6,-1.95,0],buff=0,color=GREY),M('2.5 m · furthest point tested',30,ORANGE).move_to([-.5,-2.6,0]))
        self.at('The most sensitive');self.play(FadeIn(measure),run_time=.4)
        self.at('a tap on the branch');self.play(GrowArrow(Arrow([-5.3,1.7,0],[-5.3,-.75,0],buff=0,color=ORANGE)),run_time=.3)
        # Local wave packet travels slowly for legibility; no measured velocity implied.
        center=ValueTracker(-5.3)
        pulse=always_redraw(lambda:poly([(x,-1.02+.22*np.exp(-((x-center.get_value())/.5)**2)*np.sin(16*(x-center.get_value()))) for x in np.linspace(-5.7,3,360)],ORANGE,5))
        self.add(pulse);self.play(center.animate.set_value(2.6),run_time=2.1,rate_func=linear)
        self.play(Create(raster([-4.4,-3.7,-2.3],y=1.5,x0=-4.8,x1=-1)),FadeIn(T('neuron fires',28,YELLOW).move_to([-2.7,2.45,0])),run_time=.35);self.finish();self.wait(1)
class S20Take(SpokenScene):
    def construct(self):
        a=VGroup(*[AnnularSector(inner_radius=.9,outer_radius=1.28,angle=PI,start_angle=angle,color=TEAL,fill_opacity=.23,stroke_width=3).stretch(1.6,0).move_to([-3.2,dy,0]) for angle,dy in [(0,.65),(PI,-.65)]],RoundedRectangle(width=2.5,height=.55,corner_radius=.22,color=YELLOW,fill_opacity=.25).move_to([-3.2,0,0]),Line([-5.6,0,0],[-4.45,0,0],color=YELLOW,stroke_width=7));b=_old.corpuscle().scale(1.35).move_to([3.2,0,0]);self.add(a,b,heading('Two detectors of change'),T('Meissner',30).move_to([-3.2,2.5,0]),T('Pacinian',30).move_to([3.2,2.5,0]))
        self.at('each a nerve ending');self.play(FadeIn(label('nerve ending',[-3.2,-2.55,0],[-2.6,-.25,0],YELLOW)),FadeIn(label('nerve ending',[3.2,-2.55,0],[3.2,0,0],YELLOW)),run_time=.4)
        self.at('the cells that help it feel');self.play(FadeIn(label('lamellar cells',[-3.2,-3.25,0],[-4.5,-1.1,0],TEAL)),FadeIn(VGroup(T('lamellar cells',28,TEAL).move_to([3.2,-3.25,0]),poly([(4.5,-3.25),(5.8,-3.25),(5.8,-1.25),(4,-.7)],TEAL,2))),run_time=.4);self.finish();self.wait(1)
class S21End(EndCard):
    LINE='Wrapping cells contribute to detection. Their normal mechanism remains open.'
    def construct(self):
        self.play(FadeIn(T('Wrapping cells contribute to detection.\nTheir normal mechanism remains open.',38,font=TITLE_FONT).move_to([0,.3,0])),run_time=.6)
        self.add(T('biochemistrypedia.com',28,TEAL).move_to([0,-1.4,0]));self.finish()
