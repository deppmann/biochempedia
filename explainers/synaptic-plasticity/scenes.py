"""A Synapse That Could Learn — chapter 1.

COLOR MAP (shared with scenes.old.py; CHAPTERS.md is read-only for this task):
YELLOW glutamate; BLUE AMPA; PURPLE NMDA; ORANGE magnesium;
TEAL calcium; PINK postsynaptic depolarization; GREEN increase/LTP;
RED decrease/LTD; TEXT stimuli; GOLD questions; GREY structure/baseline.
Plots below are computed schematic models, never reconstructed experimental data.
Field EPSP: delayed alpha function -u exp(1-u); spike: negative Gaussian.
Time course: normalized step, with no invented experimental magnitude or time axis.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
PINK = '#E58FC0'


def heading(text, color=TEXT):
    return T(text, 34, color).move_to([0, 3.05, 0])


def neuron(x, y=0, color=GREY, pyramidal=False):
    body = (Triangle().scale(.58) if pyramidal else Circle(radius=.6)).set_stroke(color, 4).set_fill(color, .12).move_to([x,y,0])
    branches = VGroup(*[Line([x-.45,y+d*.25,0],[x-1.05,y+d*.72,0],color=color,stroke_width=3) for d in (-1,1)])
    return VGroup(body, branches)


def pair(thick=False):
    a,b=neuron(-4,0),neuron(4,0)
    a.stretch(3.3,1);b.stretch(3.3,1)
    wire=Line([-3.4,0,0],[3.4,0,0],color=GREY,stroke_width=5)
    syn=RoundedRectangle(width=.9,height=1.3,corner_radius=.15,color=GREEN if thick else GOLD,stroke_width=10 if thick else 4,fill_color=GOLD,fill_opacity=.2)
    labs=VGroup(T('Cell A',28).move_to([-4,-2.6,0]),T('Cell B',28).move_to([4,-2.6,0]))
    return VGroup(a,b,wire,syn,labs)


def checklist():
    title=VGroup(heading('Design specification'),T('Strengthen when two things happen together',28,GOLD).move_to([0,2.25,0]))
    boxes=VGroup(*[Square(.5,color=GREY).move_to([-5.5,y,0]) for y in (.7,-1.4)])
    return title,boxes


def spec_pair():
    p=pair().scale(.48).stretch(1.8,1).move_to([3.1,-.7,0])
    p.remove(p[4])
    p.add(VGroup(T('Cell A',26).move_to([1.2,-3.05,0]),T('Cell B',26).move_to([5,-3.05,0])))
    return p


def check(box):
    c=box.get_center()
    return VMobject(color=GREEN,stroke_width=6).set_points_as_corners([c+[-.17,0,0],c+[-.03,-.15,0],c+[.22,.18,0]])


# Closed schematic hippocampal contour; not an anatomical measurement.
def map_outline():
    outline=VMobject(color=GREY,stroke_width=3).set_stroke(opacity=.6)
    outline.start_new_path(np.array([-6.3,1.7,0]))
    for c1,c2,end in [
        ([-6.2,2.7,0],[-3,2.5,0],[0,2.5,0]),
        ([3,2.5,0],[6.3,2.6,0],[6.3,1,0]),
        ([6.7,-2.4,0],[4.5,-3.25,0],[1,-3.25,0]),
        ([-2,-3.25,0],[-4.8,-3.3,0],[-5.5,-3.1,0]),
        ([-6.7,-2.9,0],[-6.7,-.9,0],[-5.5,-.9,0]),
        ([-4.7,-.9,0],[-4.7,-2,0],[-5.5,-2,0]),
        ([-5.8,-2,0],[-5.8,-1.5,0],[-5.5,-1.5,0]),
        ([-5.1,-1.5,0],[-5.1,-1.2,0],[-5.5,-1.2,0]),
        ([-6.1,-1.2,0],[-6.1,-2.6,0],[-5.3,-2.6,0]),
        ([-4.4,-2.6,0],[-4.4,-.5,0],[-5.6,-.5,0]),
        ([-6.5,-.5,0],[-6.5,.7,0],[-6.3,1.7,0]),
    ]:
        outline.add_cubic_bezier_curve_to(*[np.array(v) for v in (c1,c2,end)])
    outline.close_path()
    return outline


MAP_POS=[[-4.1,1,0],[-3,-1.05,0],[.9,-1.05,0],[4.1,1,0]]

def station(i):
    p=np.array(MAP_POS[i]);names=['Entorhinal cortex','Dentate gyrus','CA3','CA1']
    cell=neuron(*p[:2],pyramidal=i>1).scale(.65,about_point=p)
    name=T(names[i],26).move_to(p+(DOWN*.8 if i in (1,2) else UP*.85))
    sub=T('granule cells' if i==1 else 'pyramidal cells',26,GREY).move_to(p+(DOWN*1.3 if i in (1,2) else RIGHT*.6+DOWN*1.05)) if i else VGroup()
    name.set_background_stroke(color=BG,width=5)
    sub.set_background_stroke(color=BG,width=5)
    return VGroup(cell,name,sub)

def relay(i):
    a=np.array(MAP_POS[i]);b=np.array(MAP_POS[i+1]);mid=(a+b)/2
    arrow=Arrow(a,b,buff=.65,color=TEXT,stroke_width=4,max_tip_length_to_length_ratio=.10)
    positions=[[-5.1,.15,0],[-1.05,-.25,0],[3.65,-.75,0]]
    label=T(['perforant\npath','mossy fibres','Schaffer\ncollaterals'][i],26).move_to(positions[i])
    leader=Line(label.get_right() if i==0 else label.get_bottom() if i==1 else label.get_top(),mid,color=GREY,stroke_width=1.5)
    return VGroup(arrow,VGroup(label,leader))


def circuit(n=3,dots=False):
    g=VGroup(map_outline(),heading('Hippocampus'))
    for i in range(n+1):g.add(station(i))
    for i in range(n):g.add(relay(i))
    if dots:
        for i in range(3):
            p=(np.array(MAP_POS[i])+np.array(MAP_POS[i+1]))/2
            offset=[RIGHT*.45+UP*.12,DOWN*.55,LEFT*.5+UP*.35][i]
            g.add(VGroup(Circle(.23,color=GOLD,fill_color=BG,fill_opacity=1).move_to(p+offset),T(str(i+1),26,GOLD).move_to(p+offset)))
    return g


def electrode(p,color=TEXT,recording=False):
    p=np.array(p)
    if recording:
        # Hollow tapered pipette: its point lies in extracellular space.
        return Polygon(p,p+[.32,1.6,0],p+[.75,1.75,0],color=color,
                       fill_color=color,fill_opacity=.2,stroke_width=3)
    return VGroup(*[Polygon(p+[dx,0,0],p+[dx-.12,1.6,0],p+[dx+.12,1.6,0],
                            color=color,fill_color=color,fill_opacity=.6,stroke_width=2)
                   for dx in (-.25,.25)])


def method():
    path=Arrow([-6,-.2,0],[-.8,-.2,0],buff=0,color=TEXT,stroke_width=5)
    cells=VGroup(*[Circle(.72,color=GREY,fill_color=GREY,fill_opacity=.13).move_to([x,y,0]) for x,y in [(0,-1.5),(2.2,-1.5),(4.4,-1.5),(.6,1),(3.6,1)]])
    labs=VGroup(T('perforant path',28).move_to([-3.7,-1.2,0]),T('dentate gyrus · granule cells',28).move_to([2,-2.9,0]))
    stim=VGroup(electrode([-3.8,-.15,0]),T('stimulating electrode',28).move_to([-3.8,2.2,0]))
    rec=VGroup(electrode([2.1,.1,0],TEAL,True),T('recording electrode',28,TEAL).move_to([3,2.7,0]))
    return VGroup(path,cells,labs,stim,rec)


def bar(x, base, h, color, w=0.6, op=0.85):
    # Reused from scenes.old.py.
    return Rectangle(width=w, height=max(h, 0.02), stroke_color=color, stroke_width=2,
                     fill_color=color, fill_opacity=op).move_to([x, base+max(h,0.02)/2, 0])


def field(t,spike=0):
    u=max(0,(t-1)/1.6)
    return -u*np.exp(1-u)-spike*np.exp(-((t-2.8)/.13)**2)


def scope(spike=0,color=TEXT):
    ax=Axes(x_range=[0,10,2],y_range=[-2,.5,.5],x_length=11,y_length=5.1,axis_config={'color':GREY,'include_ticks':False,'include_tip':False}).move_to([.25,.05,0])
    tr=ax.plot(lambda t:field(t,spike),x_range=[0,10,.015],color=color,stroke_width=5,use_smoothing=False)
    labs=VGroup(T('time →',26,GREY).move_to([4.7,-2.95,0]),T('voltage',26,GREY).rotate(PI/2).move_to([-6.1,0,0]),T('Schematic · no calibrated scale',26,GREY).move_to([2.5,2.25,0]))
    return ax,tr,labs


def slope_marker(ax,label=True):
    seg=ax.plot(lambda t:field(t),x_range=[1.12,1.85,.01],color=GREEN,stroke_width=9,use_smoothing=False)
    lab=T('field EPSP slope = synaptic strength',28,GREEN).move_to([0,-2.85,0])
    lead=Line(lab.get_top()+LEFT*2,ax.c2p(1.55,field(1.55)),color=GREEN,stroke_width=2)
    return VGroup(seg,lab,lead) if label else seg


def course(control=False):
    # Normalized schematic step, finite observation window; not a measured magnitude.
    ax=Axes(x_range=[0,12,2],y_range=[0,2.3,.5],x_length=10.7,y_length=5.4,axis_config={'include_ticks':False,'include_tip':False,'color':GREY}).move_to([.4,-.15,0])
    before=VGroup(Line(ax.c2p(0,1),ax.c2p(3,1),color=GREY,stroke_width=4),*[Dot(ax.c2p(x,1),radius=.055,color=TEXT) for x in (.5,1.4,2.3)])
    after=VGroup(ax.plot(lambda x:1.65,x_range=[3,11,.05],color=GREEN,stroke_width=5),Line(ax.c2p(3,1),ax.c2p(3,1.65),color=GREEN,stroke_width=5),*[Dot(ax.c2p(x,1.65),radius=.055,color=GREEN) for x in (3.8,5,6.5,8,9.5,11)])
    train=VGroup(Arrow(ax.c2p(3,.08),ax.c2p(3,.85),buff=0,color=TEXT),T('train',26).move_to(ax.c2p(3,-.18)))
    labels=VGroup(T('response',26).rotate(PI/2).move_to([-6.2,1.9,0]),T('100%',26,GREY).move_to(ax.c2p(0,1)+LEFT*.6),T('time →',26,GREY).move_to([4.9,-3.25,0]))
    flat=DashedLine(ax.c2p(3,1.04),ax.c2p(11,1.04),color=GREY,stroke_width=4,dash_length=.15)
    return VGroup(ax,before,after,train,labels,flat if control else VGroup())


def duration_bracket(ax):
    left=ax.c2p(3.4,1.9);right=ax.c2p(11,1.9)
    return VGroup(Line(left,right,color=GREEN),Line(left,left+DOWN*.15,color=GREEN),Line(right,right+DOWN*.15,color=GREEN),T('30 min to 10 h',28,GREEN).move_to((left+right)/2+UP*.3),T('10 h',26,GREY).move_to(ax.c2p(11,.2)))


def pathways():
    cell=Circle(.6,color=GREY,fill_color=GREY,fill_opacity=.15).move_to([4.8,2.05,0])
    a=Arrow([-.3,2.55,0],[4.15,2.25,0],buff=0,color=GREEN,max_tip_length_to_length_ratio=.07)
    b=Arrow([-.3,1.55,0],[4.15,1.85,0],buff=0,color=GREY,max_tip_length_to_length_ratio=.07)
    return VGroup(cell,a,b,T('trained',26,GREEN).move_to([1,2.8,0]),T('untrained',26,GREY).move_to([1,1.95,0]),T('same\ncells',22,line_spacing=.8).move_to([4.8,2.05,0]))


def prediction():
    title=heading('Made-up recording',GREY)
    a=VGroup(bar(-3.9,-2.1,2.4,GREEN,w=1.2),T('EPSP slope',30).move_to([-3.9,-2.65,0]),M('160%',36,GREEN).move_to([-3.9,.9,0]))
    b=VGroup(bar(-.9,-2.1,3.75,TEXT,w=1.2),T('Spike',30).move_to([-.9,-2.65,0]),M('250%',36).move_to([-.9,2.2,0]))
    q=VGroup(T('?',68,GOLD).move_to([3.3,1.1,0]),T('Is the synapse\n2½ times stronger?',32,GOLD,line_spacing=.9).move_to([3.5,-.8,0]))
    note=T('Percent of baseline',26,GREY).move_to([-2.4,-3.35,0]);title.add(note)
    return VGroup(title,a,b,q)


class S00Title(TitleCard):
    LESSON='Synaptic Plasticity'
    TITLE='A Synapse That Could Learn'

    def construct(self):
        brand=T('BIOCHEMISTRYPEDIA',22,TEAL,weight=BOLD)
        lesson=T(self.LESSON.upper(),22,GREY)
        title=T(self.TITLE,54,font=TITLE_FONT)
        fit(title,max_w=11.5)
        rule=Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)
        g=VGroup(brand,lesson,title,rule).arrange(DOWN,buff=.32)
        self.play(FadeIn(brand),FadeIn(lesson),run_time=self.beat(.25))
        self.play(Write(title),GrowFromCenter(rule),run_time=self.beat(.35))
        self.wait(self.beat(.2))
        self.play(FadeOut(g),run_time=self.beat(.2))
        self.finish()

class S01Question(SpokenScene):
    def construct(self):
        p=pair();q=heading('What would a synapse need to store an association?',GOLD);fit(q,max_w=12.5);mark=T('?',42,GOLD)
        self.add(p,q,mark)
        self.at('a synapse need');self.play(Indicate(p[3],color=GOLD,scale_factor=1.2),run_time=.55)
        self.at('to store');self.play(Flash(p[3],color=GOLD,flash_radius=.9),run_time=.6);self.finish()

class S02Hebb(SpokenScene):
    def construct(self):
        p=pair();self.add(p,heading('Donald Hebb · 1949'))
        self.at('When one cell')
        # Persistent bright fills make the A→B delay visible between frames.
        for pulse in range(3):
            self.play(p[0][0].animate.set_fill(TEAL,.9).set_stroke(TEAL,6),run_time=.15)
            self.wait(.25)
            self.play(p[1][0].animate.set_fill(PINK,.9).set_stroke(PINK,6),run_time=.15)
            self.wait(.15)
            if pulse < 2:
                self.play(p[0][0].animate.set_fill(GREY,.12).set_stroke(GREY,4),p[1][0].animate.set_fill(GREY,.12).set_stroke(GREY,4),run_time=.1)
        self.at('grows')
        self.play(p[3].animate.scale(1.25).set_stroke(GREEN,12),FadeIn(T('connection grows',28,GREEN).move_to([0,-1.5,0])),run_time=.6);self.finish()

class S03Spec(SpokenScene):
    def construct(self):
        title,boxes=checklist();p=spec_pair();self.add(title,boxes,p)
        blanks=VGroup(*[Line([-4.9,y,0],[-.2,y,0],color=GREY) for y in (.7,-1.4)])
        self.add(blanks)
        self.at('design specification');self.play(Indicate(p[3],color=GOLD),run_time=.5)
        self.at('two things happen');self.play(Indicate(boxes,color=GOLD),run_time=.6);self.finish()

class S04Two(SpokenScene):
    def construct(self):
        title,boxes=checklist();p=spec_pair();self.add(title,boxes,p)
        self.at('Its own input')
        self.play(p[3].animate.set_fill(TEAL,.9).set_stroke(TEAL,7),p[0][0].animate.set_fill(TEAL,.8),Create(check(boxes[0])),FadeIn(T('input active',30).align_to(boxes[0],LEFT).shift(RIGHT*.7).set_y(.7)),run_time=.65)
        self.at('And the cell')
        self.play(p[1][0].animate.set_fill(PINK,.85).set_stroke(PINK,6),Create(check(boxes[1])),FadeIn(T('postsynaptic cell active\n(depolarized)',28,PINK,line_spacing=.9).align_to(boxes[1],LEFT).shift(RIGHT*.7).set_y(-1.4)),run_time=.7);self.finish()

class S05MapIntro(SpokenScene):
    def construct(self):
        p=pair(True);self.add(p)
        self.at('evidence that synapses')
        self.play(Indicate(p[3],color=GREEN),run_time=.65)
        self.at('Most of it')
        self.play(FadeOut(p),Create(map_outline()),run_time=.8)
        self.at('so here is')
        self.play(FadeIn(heading('Hippocampus')),run_time=.5)
        self.finish()

class S06Loop1(SpokenScene):
    def construct(self):
        self.add(circuit(0)[0:2])
        self.at('Input arrives')
        self.play(FadeIn(station(0)),run_time=.6)
        self.at('Its axons')
        r=relay(0);self.play(GrowArrow(r[0]),run_time=.7)
        self.at('the perforant path')
        self.play(FadeIn(r[1]),run_time=.45)
        self.at('reach the dentate')
        s=station(1);self.play(FadeIn(s),run_time=.65)
        self.at('granule cells')
        self.play(Indicate(s[0],color=TEXT),run_time=.5)
        self.finish()

class S07Loop2(SpokenScene):
    def construct(self):
        self.add(circuit(1))
        self.at('The granule')
        r=relay(1);self.play(GrowArrow(r[0]),run_time=.6)
        self.at('the mossy')
        self.play(FadeIn(r[1]),run_time=.5)
        self.at('reach the pyramidal')
        self.play(FadeIn(station(2)),run_time=.7)
        self.finish()

class S08Loop3(SpokenScene):
    def construct(self):
        self.add(circuit(2))
        self.at('Their axons')
        r=relay(2);self.play(GrowArrow(r[0]),run_time=.6)
        self.at('the Schaffer')
        self.play(FadeIn(r[1]),run_time=.5)
        self.at('reach the pyramidal')
        self.play(FadeIn(station(3)),run_time=.6)
        self.at('Most of this story')
        dots=VGroup(*list(circuit(3,True))[-3:]);self.play(FadeIn(dots),run_time=.5)
        self.at('that last relay')
        self.play(Indicate(dots[2],color=GOLD),FadeIn(Circle(.64,color=GOLD,stroke_width=6).move_to(MAP_POS[3])),run_time=.6)
        self.finish()

class S09FirstSite(SpokenScene):
    def construct(self):
        g=circuit(3,True);self.add(g)
        self.at('three synapses')
        self.play(Indicate(VGroup(*list(g)[-3:]),color=GOLD,scale_factor=1.08),run_time=.7)
        self.at('The first is')
        self.play(Indicate(g[-3],color=GOLD,scale_factor=1.5),run_time=1)
        self.finish()

class S10Bliss(SpokenScene):
    def construct(self):
        self.add(M('1973',70,GOLD).move_to([0,1.7,0]),T('Tim Bliss & Terje Lømo',42))
        self.at('reported it');self.play(Indicate(self.mobjects[0],color=GOLD),run_time=.4)
        self.at('in anesthetized rabbits');self.play(FadeIn(T('Anaesthetized rabbits',32,GREY).move_to([0,-1.7,0])),run_time=.5);self.finish()

class S11Method(SpokenScene):
    def construct(self):
        m=method();self.add(*m[:3])
        self.at('They stimulated')
        self.play(Create(m[3]),run_time=.6)
        self.at('recorded from')
        self.play(Create(m[4]),run_time=.6)
        self.at('outside the cells')
        self.play(FadeIn(T('tip outside all cells',26,TEAL).move_to([4.6,-.2,0])),Create(Line([3.15,-.2,0],[2.18,.08,0],color=TEAL,stroke_width=2)),run_time=.7)
        self.finish()

class S12Field(SpokenScene):
    def construct(self):
        cells=VGroup(*[Circle(.48,color=GREY,fill_color=GREY,fill_opacity=.15).move_to([x,y,0]) for x,y in [(-5.3,1.6),(-3.5,1.6),(-5.3,0),(-3.5,0),(-5.3,-1.6),(-3.5,-1.6)]])
        self.add(cells,heading('Many cells → one field potential',TEAL))
        self.at('That electrode records')
        self.play(LaggedStart(*[c.animate.set_stroke(TEAL,4).set_fill(TEAL,.35) for c in cells],lag_ratio=.12),run_time=1)
        self.at('an extracellular voltage')
        currents=VGroup(*[Dot(c.get_right(),radius=.1,color=TEAL) for c in cells])
        self.add(currents)
        self.play(*[d.animate.shift(RIGHT*.8) for d in currents],run_time=.7)
        self.play(*[d.animate.shift(RIGHT*.4).set_opacity(.3) for d in currents],run_time=.7)
        self.at('summed currents')
        pulses=VGroup(*[Arrow(c.get_right(),[.5,0,0],buff=.1,color=TEAL,stroke_width=2,max_tip_length_to_length_ratio=.035) for c in cells])
        flat=Line([.5,0,0],[5.8,0,0],color=TEAL,stroke_width=5)
        self.play(FadeOut(currents),LaggedStart(*[GrowArrow(a) for a in pulses],lag_ratio=.1),run_time=.8)
        self.play(Create(flat),FadeIn(T('summed cell currents',28,TEAL).move_to([2.9,-1.4,0])),run_time=.5);self.finish()

class S13Epsp(SpokenScene):
    def construct(self):
        ax,tr,labs=scope();self.add(ax,labs)
        self.at('A test pulse');self.play(Create(Line(ax.c2p(1,0),ax.c2p(1,.3),color=TEXT,stroke_width=5)),run_time=.3)
        self.at('A slow wave');self.play(Create(tr),run_time=.7)
        self.at('the population');self.play(FadeIn(heading('Population EPSP')),run_time=.4)
        self.at('measures synaptic strength');self.play(Create(slope_marker(ax)),run_time=.5);self.finish()

class S14Spike(SpokenScene):
    def construct(self):
        ax,tr,labs=scope();self.add(ax,tr,labs,slope_marker(ax))
        self.at('A sharp spike')
        target=ax.plot(lambda t:field(t,.65),x_range=[0,10,.015],color=TEXT,stroke_width=5,use_smoothing=False)
        self.play(Transform(tr,target),run_time=.5)
        self.at('shows how many')
        lab=T('Population spike =\nhow many cells fire,\nand how together',28).move_to([2.6,-1.35,0])
        pointer=Arrow(lab.get_left(),ax.c2p(2.8,field(2.8,.65)),color=TEXT,buff=.1,stroke_width=2)
        self.play(FadeIn(lab),GrowArrow(pointer),run_time=.5);self.finish()

class S15Tetanus(SpokenScene):
    def construct(self):
        base=Line([-5.8,-1.3,0],[5.8,-1.3,0],color=GREY)
        tests=VGroup(*[Line([x,-1.3,0],[x,1.8,0],color=TEXT,stroke_width=4) for x in (-5.5,-4.3,4.3,5.5)])
        self.add(base,tests,T('test pulses',28).move_to([-4.8,2.4,0]),T('time →',26,GREY).move_to([4.8,-2,0]))
        self.at('brief high')
        ticks=VGroup(*[Line([x,-1.3,0],[x,1.8,0],color=TEXT,stroke_width=2) for x in np.linspace(-2.4,2.4,61)])
        self.play(LaggedStart(*[Create(t) for t in ticks],lag_ratio=.01),run_time=.8)
        self.at('called a tetanus');self.play(FadeIn(heading('Tetanus')),run_time=.4)
        self.at('One regimen was');self.play(FadeIn(T('100 per second',32).move_to([0,2.3,0])),run_time=.4)
        self.at('for');self.play(Create(BraceBetweenPoints([-2.4,-1.6,0],[2.4,-1.6,0],direction=DOWN)),FadeIn(T('3 to 4 s',30).move_to([0,-2.8,0])),run_time=.45);self.finish()

class S16Result(SpokenScene):
    def construct(self):
        g=course();self.add(g[0],g[1],g[3],g[4])
        self.at('the same test pulse');self.play(Indicate(g[3]),run_time=.4)
        self.at('a larger response');self.play(Create(g[2]),run_time=.6)
        self.at('in');self.play(FadeIn(T('15 of 18 rabbits',28).move_to([.5,.5,0])),run_time=.4)
        self.at('It lasted');self.play(Create(duration_bracket(g[0])),run_time=.5);self.finish()

class S17Ltp(SpokenScene):
    def construct(self):
        g=course();self.add(g)
        self.at('This lasting rise')
        self.play(Indicate(g[2],color=GREEN,scale_factor=1.03),run_time=.6)
        self.at('is long')
        self.play(FadeIn(T('Long-term potentiation (LTP)',34,GREEN).move_to([0,3.25,0])),run_time=.7)
        self.finish()

class S18Control(SpokenScene):
    def construct(self):
        g=course();self.add(g)
        self.at('How do you know');self.play(FadeIn(heading('Does the change belong to this input?',GOLD).set_y(3.35)),run_time=.4)
        self.at('Record a second pathway');self.play(FadeIn(pathways()),run_time=.6)
        self.at('leave it untrained');self.play(Create(course(True)[5]),run_time=.6);self.finish()

class S19Control2(SpokenScene):
    def construct(self):
        g=course(True);self.add(g,pathways())
        self.at('If the preparation')
        drift=DashedVMobject(g[0].plot(lambda x:1+.065*(x-3),x_range=[3,11,.1],color=GREY),num_dashes=25)
        lab=T('if drifting',28,GREY).move_to([4,0,0])
        self.play(g[5].animate.set_opacity(.15),Create(drift),FadeIn(lab),run_time=.6)
        self.at('If it stays flat');self.play(FadeOut(drift),FadeOut(lab),g[5].animate.set_opacity(1),run_time=.5)
        self.at('one rises');self.play(Indicate(g[2],color=GREEN,scale_factor=1.02),run_time=.5)
        self.at('the change is');self.play(FadeIn(heading('Input specific',GREEN)),run_time=.5);self.finish()

class S20Predict(SpokenScene):
    def construct(self):
        p=prediction();self.add(p[0])
        self.at('the slope rose')
        self.play(FadeIn(p[1]),run_time=.65)
        self.at('The spike rose')
        self.play(FadeIn(p[2]),run_time=.65)
        self.at('Is the synapse')
        self.play(FadeIn(p[3]),run_time=.65)
        self.finish()

class S21Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(prediction());self.wait(5)

class S22Reveal(SpokenScene):
    def construct(self):
        p=prediction();self.add(p)
        # Transcript misrecognizes the opening "No" as "Now"; cue the next intact phrase.
        self.at('synaptic strength')
        self.play(FadeOut(p[3]),p[2].animate.set_opacity(.35),Circumscribe(p[1],color=GREEN),run_time=.75)
        self.at('read from the slope')
        self.play(FadeIn(T('Read synaptic strength\nfrom the slope',28,GREEN).move_to([3.6,-1.3,0])),run_time=.6)
        self.finish()

class S23Threshold(SpokenScene):
    def construct(self):
        xs=np.linspace(-5,-.2,6);base=-2.2;hs=np.array([2.6,2.52,2.4,2.3,1.5,1.4]);threshold=2.5
        tracker=ValueTracker(1)
        bars=always_redraw(lambda:VGroup(*[bar(x,base,h*tracker.get_value(),GREEN if h*tracker.get_value()>threshold else GREY,w=.48) for x,h in zip(xs,hs)]))
        cells=always_redraw(lambda:VGroup(*[Circle(.18,color=GREEN if h*tracker.get_value()>threshold else GREY,fill_color=GREEN if h*tracker.get_value()>threshold else GREY,fill_opacity=.8).move_to([x,2.35,0]) for x,h in zip(xs,hs)]))
        state=T('before',32).move_to([-2.5,3.15,0]);sp=bar(4,-2.2,1.2,TEXT,w=1)
        self.add(bars,cells,state,sp,T('EPSP in each cell',28).move_to([-2.5,-2.85,0]),T('population spike',28).move_to([4,-2.85,0]),T('100%',28).move_to([4,-.55,0]))
        self.at('Firing has a threshold');self.play(Create(DashedLine([-5.7,.3,0],[.5,.3,0],color=GOLD)),FadeIn(T('firing\nthreshold',26,GOLD).move_to([1.6,.3,0])),run_time=.5)
        self.at('A modest rise');self.play(tracker.animate.set_value(1.6),Transform(state,T('after · EPSP ×1.6',30).move_to([-2.5,3.15,0])),run_time=1)
        self.at('many more cells');self.play(Indicate(cells,color=GREEN,scale_factor=1.02),run_time=.4)
        self.at('So the spike');self.play(Transform(sp,bar(4,-2.2,3,TEXT,w=1)),Transform(self.mobjects[6],T('250%',28).move_to([4,1.3,0])),run_time=.6);self.finish()

class S24Matched(SpokenScene):
    def construct(self):
        ax,before,labs=scope(0,GREY);_,after,_=scope(0,TEXT)
        self.add(ax,before,after,labs,slope_marker(ax),heading('Same EPSP: does the spike change?',GOLD))
        self.add(T('before train',28,GREY).move_to([3.8,.8,0]),T('after train',28).move_to([3.8,.25,0]))
        self.at('To test whether');self.play(Indicate(slope_marker(ax,False),color=GREEN),run_time=.5)
        self.at('compare spike size')
        bt=ax.plot(lambda t:field(t,.3),x_range=[0,10,.015],color=GREY,stroke_width=8,use_smoothing=False)
        at=ax.plot(lambda t:field(t,.7),x_range=[0,10,.015],color=TEXT,stroke_width=4,use_smoothing=False)
        self.play(Transform(before,bt),Transform(after,at),run_time=.6)
        self.at('at matched');self.play(FadeIn(T('Bigger spike at the same EPSP: coupling rose',28,GOLD).move_to([1,-2.25,0])),run_time=.45);self.finish()

class S25Puzzles(SpokenScene):
    def construct(self):
        self.add(heading('Three puzzles'))
        for cue,txt,y in [('How can a synapse','1   How does a synapse detect activity together?',1.7),('What decides','2   What decides whether strength goes up or down?',-.2),('And does memory','3   Does memory use this change?',-2.4)]:
            self.at(cue)
            card=VGroup(RoundedRectangle(width=12,height=1.4,corner_radius=.15,color=GOLD),T(txt,28,GOLD).move_to([0,0,0])).move_to([0,y,0])
            self.play(FadeIn(card),run_time=.4)
        self.wait(max(0,self._words()[-1][0]+3.5-self.elapsed()))
        self.finish()

class S26Takeaway(SpokenScene):
    def construct(self):
        membrane=VGroup(Line([-5.8,-.3,0],[-.65,-.3,0],color=GREY,stroke_width=12),Line([.65,-.3,0],[5.8,-.3,0],color=GREY,stroke_width=12),Arc(radius=3.5,start_angle=PI,angle=PI,color=GREY).stretch(.4,1,about_point=ORIGIN).shift(DOWN*.3))
        pore=VGroup(*[Rectangle(width=.28,height=1.2,color=PURPLE,fill_color=PURPLE,fill_opacity=.8).move_to([x,-.3,0]) for x in (-.52,.52)])
        mg=chip('Mg²⁺',ORANGE,28).move_to([0,-.3,0])
        model=T('What sets the direction is a model',26,GOLD).move_to([0,2.3,0])
        self.add(membrane,pore,T('NMDA receptor',30,PURPLE).move_to([0,1,0]),T('spine',26,GREY).move_to([-4.1,-1.4,0]),heading('How does coincidence open the gate?',GOLD))
        self.at('offers a model');self.play(FadeIn(model),run_time=.5)
        self.at('At');self.play(Transform(model,T('Schaffer collateral → CA1',28).move_to([0,2.3,0])),run_time=.5)
        self.at('with normal magnesium');self.play(FadeIn(mg),Transform(model,T('CA1 · normal Mg²⁺ · co-agonist present',26,ORANGE).move_to([0,2.3,0])),run_time=.6)
        glu=chip('glutamate',YELLOW,26).move_to([-4,1.1,0])
        self.play(FadeIn(glu),run_time=.5)
        self.at('is triggered by')
        ca=chip('Ca²⁺ entry → LTP',TEAL,28).move_to([0,-2.5,0])
        status=T('gate closed',26,TEAL).move_to([3.8,-1.7,0])
        self.play(FadeIn(ca.set_opacity(.35)),FadeIn(status),run_time=.5)
        # Glutamate approaches while Mg still blocks the pore.
        self.at('calcium entering')
        self.play(glu.animate.shift(RIGHT*.45+DOWN*.25),run_time=1)
        self.at('Substantial entry needs');self.play(Indicate(mg,color=ORANGE),run_time=.5)
        self.at('glutamate and')
        ga=Arrow(glu.get_right(),[-.8,-.1,0],color=YELLOW,buff=.12)
        self.play(GrowArrow(ga),run_time=.6)
        self.at('enough local depolarization')
        dep=chip('local depolarization',PINK,26).move_to([3.7,1,0]);da=Arrow(dep.get_bottom(),[.8,-.3,0],color=PINK,buff=.15)
        self.play(FadeIn(dep),GrowArrow(da),mg.animate.move_to([5,-2.5,0]),membrane.animate.set_color(PINK),run_time=.7)
        self.at('together')
        ions=VGroup(*[Dot([0,y,0],radius=.1,color=TEAL) for y in (.35,0,-.35)])
        self.add(ions)
        self.play(Transform(status,T('gate open',26,GREEN).move_to([3.8,-1.7,0])),Transform(ca,chip('Ca²⁺ entry → LTP',TEAL,28).move_to([0,-2.5,0])),ions.animate.shift(DOWN*.8),GrowArrow(Arrow([0,-.9,0],ca.get_top(),color=TEAL,buff=.1)),Circumscribe(ca,color=GREEN),run_time=.6)
        self.wait(2)
        self.finish()

class S27End(EndCard):
    LINE='NMDA receptors let in much calcium only when\nglutamate and depolarization coincide.'
