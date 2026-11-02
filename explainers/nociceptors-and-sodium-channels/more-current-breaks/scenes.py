"""Where More Current Breaks — chapter 4.
COLOR MAP (shared with scenes.old.py): YELLOW SCN9A; ORANGE #F29E4C
Nav1.7; TEAL #3FB8C0 Nav1.8; PURPLE #B58CD9 Nav1.9; RED loss;
GREEN measured residual current only; TEXT control traces; GREY structure.
No changes to CHAPTERS.md: TASK's final file restriction takes precedence.
Curves: lesson Boltzmann h(V); reference PCHIP spike_fn/train model.
Nav1.9 window and separate Nav1.8 curves are explicitly illustrative
Boltzmann shapes, not fitted experimental gating measurements.
"""
import numpy as np
from scipy.interpolate import PchipInterpolator
from bp_style import *

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
TEAL_C = '#3FB8C0'

def heading(s, c=TEXT):
    return T(s,32,c,font=TITLE_FONT).move_to([0,3.05,0])

def lines(ss,c=TEXT,size=28):
    return VGroup(*[T(s,size,c) for s in ss]).arrange(DOWN,buff=.16)

def arr(a,b,c=GREY,w=4):
    return Arrow(a,b,buff=.12,color=c,stroke_width=w,tip_length=.2)

def mem_bar(cx,cy,w,h=.34):
    return RoundedRectangle(width=w,height=h,corner_radius=.1,color=GREY,fill_color=GREY,fill_opacity=.35).move_to([cx,cy,0])

def spike_fn(impaired=False):
    # The reference film's shape-preserving interpolation, not a digitized recording.
    pts = ([(0,0),(.45,.02),(.62,.30),(.78,1),(.95,.74),(1.15,.46),(1.5,.40),(1.85,.02),(2.1,-.14),(2.6,0),(3,0)] if not impaired else
           [(0,0),(.45,.02),(.62,.30),(.78,.68),(.95,.48),(1.15,.28),(1.5,.24),(1.85,0),(2.1,-.10),(2.6,0),(3,0)])
    return PchipInterpolator(*zip(*pts))

def train(impaired,n,gap=3):
    f=spike_fn(impaired); t=np.linspace(0,15,700)
    y=np.zeros_like(t)
    for k in range(n):
        z=t-k*gap
        mask=(z>=0)&(z<=3)
        y[mask]=f(z[mask])
    return t,y

def waveform(cx,cy,w=5,h=1.8,n=4,impaired=False,c=TEXT):
    x,y=train(impaired,n)
    return VMobject(color=c,stroke_width=3.5).set_points_as_corners(
        [[cx-w/2+w*t/15,cy+h*v,0] for t,v in zip(x,y)])

def neuron(cx,cy,r=.65,c=GREY):
    soma=Circle(r,color=c,fill_color=c,fill_opacity=.12).move_to([cx,cy,0])
    branches=VGroup(Line([cx+r,cy,0],[cx+r+1.1,cy,0],color=c,stroke_width=4),
        *[Line([cx-r*.7,cy+d*.45,0],[cx-r- .65,cy+d*.9,0],color=c,stroke_width=3) for d in [-1,1]])
    return VGroup(soma,branches)

# All traces below use the reference PCHIP model; schematic, never recordings.
def h(v,mid=-65): return 1/(1+np.exp((v-mid)/7))

def txt(s,x,y,size=28,c=TEXT): return T(s,size,c).move_to([x,y,0])

def voltage_axes(vmin=-90,vmax=-40,w=10.2,height=4.7,center=(0,0)):
    # Offset coordinates keep the y axis at the LEFT, not at the clamped 0 mV edge.
    ax=Axes(x_range=[0,vmax-vmin,10],y_range=[0,1,.5],x_length=w,y_length=height,
        tips=False,axis_config={'color':GREY,'include_tip':False}).move_to([*center,0])
    ax.vmin=vmin; ax.vmax=vmax
    labels=VGroup(*[T(str(v).replace('-','−'),26,GREY).next_to(ax.c2p(v-vmin,0),DOWN,buff=.12) for v in range(vmin,vmax+1,10)],
        *[T(str(v),26,GREY).next_to(ax.c2p(0,v),LEFT,buff=.15) for v in [0,.5,1]])
    return ax,labels

def point(ax,v,y): return ax.c2p(v-ax.vmin,y)
def curve(ax,fn,c=ORANGE,width=5):
    return ax.plot(lambda x:fn(x+ax.vmin),x_range=[0,ax.vmax-ax.vmin,.15],color=c,stroke_width=width,use_smoothing=False)

def availability():
    ax,labels=voltage_axes(height=4.35,center=(0,-.05))
    return ax,VGroup(ax,labels,curve(ax,h),txt('Available fraction',-3.7,2.5,26,ORANGE),
        txt('Resting voltage (mV)',0,-2.85,26,GREY),txt('Illustrative Nav1.7-like • tetrodotoxin-sensitive',0,-3.4,26,GREY))

def rest_markers(ax):
    g=VGroup()
    for v,c,label,x in [(-60,GREY,'Wild-type −60 mV',-.7),(-48.5,PURPLE,'L1302F −48.5 mV',3.6)]:
        g.add(DashedLine(point(ax,v,0),point(ax,v,.82),color=c),txt(label,x,1.85,26,c).shift(RIGHT*.4 if v==-48.5 else LEFT*.5))
    return g

def mouse():
    body=Ellipse(width=4.5,height=2.7,color=GREY,fill_color=GREY,fill_opacity=.18)
    head=Ellipse(width=1.7,height=1.4,color=GREY,fill_color=BG,fill_opacity=1).move_to([2,.35,0])
    ear=Circle(.42,color=GREY,fill_color=BG,fill_opacity=1).move_to([1.65,1.05,0])
    tail=VMobject(color=GREY,stroke_width=5).set_points_smoothly([[-2.15,-.1,0],[-2.8,-.25,0],[-3.2,.1,0],[-3.6,.15,0]])
    return VGroup(tail,body,head,ear,Dot([2.45,.55,0],radius=.07,color=TEXT))

def paired():
    left=VGroup(txt('R222S • knock-in mouse',-3.45,2,28,PURPLE),waveform(-3.45,-.25,5.3,1.8,5,c=PURPLE),txt('More firing',-3.45,-1,28,PURPLE))
    right=VGroup(txt('L1302F / L811P • rat',3.45,2,28,RED),waveform(3.45,-.25,5.3,1.55,5,True,RED),txt('Impaired firing',3.45,-1,28,RED))
    minority=VGroup(waveform(3.45,-2,5.3,1,0,c=RED),txt('Minority: no firing',3.45,-2.6,28,RED))
    q=txt('Which should you expect?',-2.3,-2.4,30)
    return left,right,minority,q

def variable_items():
    labels=['Size and time course\nof depolarization','Subtype-specific availability',
        'Channel densities','Other conductances','Stimulation']
    items=VGroup(*[T(s,34,TEXT) for s in labels])
    for item,y in zip(items,[1.65,.35,-.65,-1.65,-2.65]):
        item.move_to([-5.8,y,0],aligned_edge=LEFT)
    return items

def question_base():
    # The question and its pause carry exactly the answer's left anchors.
    ax,_=voltage_axes(w=2.6,height=2.8,center=(4.8,0))
    inset=VGroup(ax,curve(ax,h),txt('Availability',4.8,2,26,ORANGE),
        txt('−90',3.5,-1.75,26,GREY),txt('−40 mV',5.75,-1.75,26,GREY))
    return VGroup(heading('What decides the outcome?'),variable_items(),
        txt('Illustrative availability ≠ prediction',0,-3.5,26,ORANGE),inset)

class S00Title(TitleCard):
    LESSON='Nociceptors and the Sodium Channels of Pain'
    TITLE='Where More Current Breaks'
    def construct(self):
        self.add(txt('BIOCHEMISTRYPEDIA',0,1.5,26,TEAL),txt(self.LESSON,0,.7,28,GREY),
            T(self.TITLE,48,TEXT,font=TITLE_FONT).move_to([0,-.35,0]),Line([-2,-1.2,0],[2,-1.2,0],color=GOLD))
        self.finish()

class S01Question(SpokenScene):
    def construct(self):
        self.add(neuron(-3.6,1.1,1.05,PURPLE),neuron(3.2,1.1,1.05,PURPLE),
            txt('Variant A',-3.5,2.7,32,PURPLE),txt('Variant B',3.5,2.7,32,PURPLE),
            chip('Increased channel current',PURPLE,30).move_to([0,-2.9,0]))
        self.at('Two variants'); self.play(Create(waveform(-3.5,-1.65,5.4,1.15,5,c=PURPLE)),Create(waveform(3.5,-1.65,5.4,1.15,0,c=PURPLE)),run_time=.8)
        self.at('Can the neurons'); self.play(FadeIn(txt('Opposite firing outcomes?',0,-.25,32)),run_time=.4); self.finish()

class S02Rule(SpokenScene):
    def construct(self):
        a=chip('More sodium current',PURPLE,36).move_to([-3.6,.2,0]); b=chip('More pain',TEXT,40).move_to([3.9,.2,0])
        for z in [a,b]: z[0].stretch_to_fit_height(3.1)
        self.add(a,b,txt('The tempting rule',0,2.8,36))
        self.at('More sodium current'); self.play(Create(DashedLine(a.get_right(),b.get_left(),color=GREY)),FadeIn(txt('tempting rule',.7,-.55,30,GREY)),run_time=.8); self.finish()

class S03Nine(SpokenScene):
    def construct(self):
        ax,labels=voltage_axes(-90,-30,w=10.6,height=5.35,center=(0,-.15))
        m=lambda v:1/(1+np.exp(-(v+55)/7))
        xs=np.linspace(-90,-30,250)
        shade=Polygon(*[point(ax,v,min(m(v),h(v))) for v in xs],point(ax,-30,0),point(ax,-90,0),stroke_width=0,fill_color=PURPLE,fill_opacity=.6)
        rest=DashedLine(point(ax,-60,0),point(ax,-60,1),color=TEXT)
        window=txt('window',2.7,-1.25,32,PURPLE)
        self.add(heading('Nav1.9 • illustrative gates',PURPLE),ax,labels,
            txt('Fraction',-5.6,2.8,26,GREY),txt('Voltage (mV)',0,-3.55,28,GREY),
            shade,rest,txt('Resting potential',2.1,2.65,26),
            txt('−60 mV',1.8,2.15,26),window,
            Line(window.get_left()+LEFT*.1,point(ax,-60,.25),color=PURPLE))
        self.at('breaks it'); self.play(Create(curve(ax,m,PURPLE)),Create(curve(ax,h,GREY)),run_time=.65)
        self.at('Its activation'); self.play(FadeIn(txt('Activation',3.7,.9,28,PURPLE)),FadeIn(txt('Availability',-3.4,.95,28,GREY)),run_time=.4)
        self.add(Line([3.7,1.12,0],point(ax,-40,m(-40)),color=PURPLE))
        self.at('overlap near rest'); self.play(Indicate(shade,scale_factor=1),Indicate(window,scale_factor=1.05),run_time=.6); self.finish()

class S04Standing(SpokenScene):
    def construct(self):
        self.add(heading('Nav1.9 • near rest',PURPLE),mem_bar(0,.8,12,.65),
            arr([0,.2,0],[0,-2.5,0],PURPLE,12),txt('Inward summed current',3.3,-1,30,PURPLE),
            txt('Window current',3.3,-1.7,32,PURPLE),txt('A population current',3.3,-2.35,28,PURPLE),
            txt('Outside',-4.8,1.9,28,GREY),txt('Inside',-4.8,-.5,28,GREY),txt('Illustrative states • not measured proportions',0,-3.25,26,GREY))
        rng=np.random.default_rng(19)
        def gates():
            states=np.array([0]*6+[1]*5+[2]*5); rng.shuffle(states)
            g=VGroup()
            for x,state in zip(np.linspace(-5.6,5.6,16),states):
                g.add(Line([x-.16,.25,0],[x-.16,1.35,0],color=PURPLE,stroke_width=4),Line([x+.16,.25,0],[x+.16,1.35,0],color=PURPLE,stroke_width=4))
                if state==0: g.add(Line([x-.16,.8,0],[x+.16,.8,0],color=PURPLE,stroke_width=5))
                elif state==2: g.add(Dot([x,.8,0],radius=.12,color=PURPLE))
            return g
        g=gates(); self.add(g,txt('Open now: 5 / 16',0,2.05,30,PURPLE))
        for phrase in ['activation and availability','some channels are open','The population carries']:
            self.at(phrase)
            for _ in range(2):
                new=gates(); self.remove(g); g=new; self.add(g); self.wait(.35)
        self.finish()

class S05Pull(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,10,2],y_range=[0,30,10],x_length=10.2,y_length=4.5,tips=False).move_to([0,-.15,0])
        y=lambda v:ax.c2p(0,v+80)[1]
        self.add(heading('Inward current depolarizes',PURPLE),ax,txt('mV',-6.35,2.85,28,GREY),txt('Time → • schematic',0,-3.1,28,GREY),
            *[txt(str(v).replace('-','−'),-5.8,y(v),26,GREY) for v in [-80,-70,-60,-50]])
        original=DashedLine([-5.1,y(-70),0],[5.1,y(-70),0],color=GREY)
        rest=Line([-5.1,y(-70),0],[5.1,y(-70),0],color=PURPLE,stroke_width=6)
        self.add(original,rest,txt('Original rest',3.7,y(-70)-.4,28,GREY),
            DashedLine([-5.1,y(-52),0],[5.1,y(-52),0],color=TEXT),
            txt('Threshold (schematic)',2.8,y(-52)-.35,26,GREY))
        self.at('a steady depolarizing'); self.play(rest.animate.shift(UP*1.35),GrowArrow(arr([-2,y(-70),0],[-2,y(-70)+1.35,0],PURPLE)),FadeIn(txt('Toward threshold',1.3,.8,30,PURPLE)),run_time=1.6); self.finish()

class S06Okuda(SpokenScene):
    def construct(self):
        self.add(heading('Okuda and colleagues'),mouse().move_to([0,.25,0]),txt('Knock-in mouse',0,2.1,32))
        self.at('carrying the variant'); self.play(FadeIn(chip('Nav1.9 • R222S knock-in allele',PURPLE,32).move_to([0,-2,0])),FadeIn(txt('Found in familial episodic pain',0,-3,28,PURPLE)),run_time=.5); self.finish()

class S07More(SpokenScene):
    def construct(self):
        self.add(heading('Evoked firing • same stimulus'),waveform(0,.3,11.6,1.5,5,c=PURPLE),waveform(.65,-1.85,10.3,1.5,2,c=TEXT),
            txt('R222S knock-in',-3.7,2.05,30,PURPLE),txt('Control',-5.45,-1.1,28),txt('Schematic trace amplitude: a.u. • model time: 0–15 a.u.',0,-3.55,26,GREY))
        # No numerical stimulus amplitude or duration is reported: mark that explicitly.
        stim=VMobject(color=GREY).set_points_as_corners([[-5.8,-3.05,0],[-5,-3.05,0],[-5,-2.7,0],[5,-2.7,0],[5,-3.05,0],[5.8,-3.05,0]])
        self.add(stim,txt('Same step • stimulus amplitude: 1 a.u.',0,-2.3,26,GREY))
        self.at('found in familial'); self.play(FadeIn(txt('Found in familial episodic pain',2.7,2.05,26,PURPLE)),run_time=.35); self.finish()

class S08Huang(SpokenScene):
    def construct(self):
        self.add(heading('Huang and colleagues'),neuron(1.4,.25,1.55),txt('Small dorsal root ganglion neuron',0,-2.6,30),txt('Rat • 4 to 6 weeks',0,-3.2,28,GREY))
        cs=VGroup(chip('L1302F',PURPLE,36).move_to([-4,1.35,0]),chip('L811P',PURPLE,36).move_to([-4,-1.05,0]))
        self.at('expressed two human variants'); self.play(FadeIn(cs),run_time=.35)
        self.at('in small rat'); self.play(*[GrowArrow(arr(c.get_right(),[-.2,.25,0],PURPLE)) for c in cs],run_time=.5); self.finish()

class S09Insens(SpokenScene):
    def construct(self):
        self.add(heading('Human Nav1.9 variants',PURPLE),neuron(1.4,.25,1.55),chip('L1302F',PURPLE,36).move_to([-4,1.35,0]),chip('L811P',PURPLE,36).move_to([-4,-1.05,0]),txt('Small dorsal root ganglion neuron • rat, 4–6 weeks',0,-2.35,26,GREY))
        self.at('associated with'); self.play(FadeIn(chip('Insensitivity to pain',RED,34).move_to([0,-3.1,0])),run_time=.25); self.finish()

class S10Less(SpokenScene):
    def construct(self):
        self.add(heading('Depolarized • impaired firing'),txt('mV',-6,2.3,28,GREY),Line([-5.5,-2.3,0],[-5.5,2.3,0],color=GREY),
            waveform(.4,-1.9,10,1.4,5,c=TEXT),txt('Control',-4.2,-2.6,28),txt('Schematic • voltage offset, not a measured scale',0,-3.35,26,GREY))
        trace=waveform(.4,.2,10,1.6,5,c=PURPLE)
        self.at('Both depolarized'); self.play(FadeIn(trace),FadeIn(txt('L1302F / L811P',-3.5,2.25,30,RED)),
            Create(DashedLine([-5,.2,0],[5.5,.2,0],color=GREY)),FadeIn(txt('Depolarized resting level',2.7,-.25,26,PURPLE)),run_time=.5)
        self.at('impaired action'); self.play(Transform(trace,waveform(.4,.2,10,.85,5,True,RED)),run_time=.55); self.finish()

class S11Shift(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,10,2],y_range=[0,20,5],x_length=10.2,y_length=4.8,tips=False).move_to([0,-.15,0])
        p=lambda v:ax.c2p(0,v+65)
        lo=Line(ax.c2p(0,5),ax.c2p(10,5),color=GREY,stroke_width=5); hi=lo.copy().set_color(PURPLE)
        self.add(heading('Average resting potential'),ax,txt('mV',-5.9,2.6,28,GREY),lo,hi,
            *[T(str(v).replace('-','−'),26,GREY).next_to(p(v),LEFT,buff=.16) for v in [-65,-60,-55,-50,-45]],txt('Wild-type Nav1.9',-1.7,-1.85,30,GREY))
        self.at('shifted the average'); self.play(hi.animate.shift(UP*(11.5*4.8/20)),run_time=.8)
        self.at('by about'); self.play(GrowArrow(DoubleArrow([4.5,p(-60)[1],0],[4.5,p(-48.5)[1],0],buff=0,color=PURPLE)),FadeIn(txt('+11.5 mV',2.8,.1,30,PURPLE)),FadeIn(txt('L1302F • −48.5 mV',-1.4,1.95,30,PURPLE)),run_time=.5); self.finish()

class S12Paradox(SpokenScene):
    def construct(self):
        l,r,m,q=paired(); self.add(heading('Gain of channel function',PURPLE),l[:2],r[:2])
        self.at('One raises firing'); self.play(FadeIn(l[2]),run_time=.35)
        self.at('The other impairs'); self.play(FadeIn(r[2]),run_time=.35)
        self.at('in a minority'); self.play(FadeIn(m),run_time=.35)
        self.at('Which should you expect'); self.play(FadeIn(q),run_time=.35); self.finish()

class S13Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(heading('Gain of channel function',PURPLE),*paired()); self.wait(5)

class S14Need(SpokenScene):
    def construct(self):
        ax,base=availability(); self.add(heading('Current alone cannot answer'),base)
        self.at('You need the availability'); self.play(FadeIn(rest_markers(ax)),run_time=.6); self.finish()

class S15Cost(SpokenScene):
    def construct(self):
        ax,base=availability(); self.add(base,rest_markers(ax),heading('The cost of +11.5 mV'),txt('V½ = −65 mV • k = 7 mV',0,2.95,26,GREY))
        # Heading and parameters share no space: parameters live below the plot instead.
        self.mobjects[-1].move_to([-2.8,-1.35,0])
        dots=VGroup(*[Dot(point(ax,v,h(v)),color=ORANGE,radius=.1) for v in [-60,-48.5]])
        self.at('Put the shift'); self.play(FadeIn(dots),run_time=.4)
        y1=point(ax,-60,h(-60))[1]; y2=point(ax,-48.5,h(-48.5))[1]
        bracket=VGroup(Line(point(ax,-60,h(-60)),[5.7,y1,0],color=ORANGE),Line(point(ax,-48.5,h(-48.5)),[5.7,y2,0],color=ORANGE),DoubleArrow([5.7,y1,0],[5.7,y2,0],buff=0,color=ORANGE))
        self.at('Availability'); self.play(Create(bracket),FadeIn(txt('0.33 → 0.086 • about 4-fold',1.5,2.4,28,ORANGE)),run_time=.5); self.finish()

def range_plot():
    ax,labels=voltage_axes(w=7.5,height=3.7,center=(-1.8,.25))
    band=VGroup(*[curve(ax,lambda v,m=m:h(v,m),ORANGE,2.8).set_stroke(opacity=.7).set_fill(opacity=0) for m in np.linspace(-78,-60,9)])
    g=VGroup(ax,labels,band,txt('Available fraction',-3.8,2.4,26,ORANGE),txt('Voltage (mV)',-1.8,-2.25,26,GREY),txt('V½: −78 to −60 mV • k = 7 mV',0,2.9,26,ORANGE))
    for v in [-60,-48.5]:
        g.add(DashedLine(point(ax,v,0),point(ax,v,.82),color=GREY),*[Dot(point(ax,v,h(v,m)),color=TEXT,radius=.075) for m in [-78,-60]])
    g.add(txt('V½ −78',-4.6,-.3,26,ORANGE),txt('V½ −60',-.5,1.8,26,ORANGE),txt('−48.5',1.2,1.8,26,GREY))
    # Explicit leaders identify the two endpoint curves.
    g.add(Line([-4.4,-.05,0],point(ax,-78,.5),color=ORANGE),Line([-.5,1.55,0],point(ax,-60,.5),color=ORANGE))
    g.add(txt('Midpoint      h(−60) → h(−48.5)      loss',-.6,-2.65,29,GREY))
    for mid,y in [(-78,-3.1),(-60,-3.55)]:
        a,b=h(-60,mid),h(-48.5,mid)
        g.add(txt(f'{mid} mV         {a:.3f} → {b:.3f}         {a/b:.1f}-fold',-.6,y,29,ORANGE))
    return ax,g

class S16Range(SpokenScene):
    def construct(self):
        ax,g=range_plot(); self.add(g)
        self.at('The size depends'); self.play(Indicate(g[2],scale_factor=1),run_time=.5)
        self.at('The direction does not'); self.play(Indicate(g[-2:],scale_factor=1.02),run_time=.5)
        na,lab=voltage_axes(-90,-10,w=2.5,height=2.4,center=(4.65,.45))
        # Inset uses its own marked range so the main comparison never rescales.
        # Avoid crowded inset ticks by showing endpoints only at >=26 pt.
        inset=VGroup(na,curve(na,lambda v:h(v,-30),TEAL_C),txt('Nav1.8',4.65,2.15,30,TEAL_C),txt('−90',3.4,-1.05,26,GREY),txt('−10 mV',5.55,-1.05,26,GREY),txt('Separate curve',4.65,-1.55,26,TEAL_C),txt('Outside calculation',4.65,-2.05,26,TEAL_C))
        self.at('sits on its own curve'); self.play(FadeIn(inset),run_time=.6); self.finish()

class S17Order(SpokenScene):
    def construct(self):
        ax,g=range_plot(); g.set_stroke(opacity=.55); self.add(g)
        self.at('So treat this'); self.play(FadeOut(g[-3:]),FadeIn(chip('Back of envelope • not a measurement',TEXT,30).move_to([0,-2.8,0])),run_time=.5); self.finish()

def excitability(large=False):
    start=-60 if large else -70
    title='Large depolarization: availability collapses' if large else 'Small depolarization: availability to spare'
    ax=Axes(x_range=[0,15,5],y_range=[0,85,20],x_length=8.5,y_length=4.6,tips=False).move_to([-1.3,-.1,0])
    y=lambda v:ax.c2p(0,v+80)[1]
    base=VGroup(heading(title),ax,DashedLine([-5.55,y(start),0],[2.95,y(start),0],color=GREY,stroke_opacity=.5),txt('Start: −60 mV • h ≈ 0.33' if large else 'Start: −70 mV • h ≈ 0.67',-1.3,2.45,26,ORANGE),txt('mV',-6.1,2.45,26,GREY),txt('Time → • schematic',-1.3,-3,26,GREY),txt('Illustrative Nav1.7-like',0,-3.55,26,ORANGE),
        DashedLine([-5.55,y(-40),0],[2.95,y(-40),0],color=GREY),txt('Threshold (schematic)',-.9,1.45,26,GREY),
        *[txt(str(v).replace('-','−'),-6.1,y(v),26,GREY) for v in [-70,-60,-40,0]])
    def state(v,spikes=False):
        frac=h(v)
        rest=waveform(-1.3,y(v),8.5,(2.2 if not large else 2.2*frac/h(start)),5,large,RED if large else PURPLE) if spikes else Line([-5.55,y(v),0],[2.95,y(v),0],color=PURPLE,stroke_width=5)
        meter=VGroup(Rectangle(width=1.05,height=3.5,color=ORANGE).move_to([4.8,-.05,0]),
            Rectangle(width=.93,height=max(.02,3.4*frac),stroke_width=0,fill_color=ORANGE,fill_opacity=.8).move_to([4.8,-1.75+3.4*frac/2,0]),
            txt(f'h = {frac:.3f}',4.8,-2.3,30,ORANGE),txt(f'−{abs(v):g} mV',4.8,-2.9,28,PURPLE),txt('Available',4.8,2.45,28,ORANGE),txt('fraction',4.8,1.95,28,ORANGE))
        return VGroup(rest,meter)
    return base,state,start

class S18Small(SpokenScene):
    def construct(self):
        base,state,start=excitability(); g=state(start); self.add(base,g)
        self.at('A small depolarization'); self.wait(.3)
        self.play(UpdateFromAlphaFunc(g,lambda mob,alpha:mob.become(state(start+3*alpha))),run_time=1.3)
        self.at('closer to threshold'); target=state(-67,True)
        self.play(Transform(g,target),run_time=.7)
        self.add(txt('One possible outcome',-1.3,.85,26,PURPLE))
        self.at('With availability to spare'); self.play(Indicate(g[1],scale_factor=1.02),run_time=.4)
        self.finish()

class S19Large(SpokenScene):
    def construct(self):
        base,state,start=excitability(True); voltage=ValueTracker(start)
        g=always_redraw(lambda:state(voltage.get_value(),True)); self.add(base,g)
        self.at('A larger one'); self.wait(.4); self.play(voltage.animate.set_value(-48.5),run_time=1.5)
        g.clear_updaters()
        self.at('the upstroke'); self.play(Indicate(g[0],scale_factor=1.02),run_time=.4); self.finish()

class S20Fail(SpokenScene):
    def construct(self):
        self.add(heading('Complete failure: only a minority'),txt('Illustrative population • 1 of 8, not a measured proportion',0,-3.5,26,GREY))
        cells=VGroup()
        for i in range(8):
            x=-4.8+(i%4)*3.2; y=1.55-(i//4)*2.8
            cells.add(VGroup(neuron(x,y,.6),waveform(x,y-1.65,2.7,.65,5,c=TEXT)))
        self.add(cells)
        self.at('the cells that depolarized furthest'); self.play(cells[-1][0].animate.set_color(RED),run_time=.4)
        self.at('stopped firing altogether'); self.play(Transform(cells[-1][1],waveform(4.8,-2.9,2.7,.65,0,c=RED)),run_time=.5); self.finish()

class S21WhichSets(SpokenScene):
    def construct(self):
        self.add(question_base()); self.at('what decides the outcome'); self.wait(.2); self.finish()

class S22Pause2(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question_base()); self.wait(5)

class S23Answer(SpokenScene):
    def construct(self):
        q=question_base(); self.add(q); items=q[1]
        cues=['the size and time','subtype specific availability','channel densities','the other conductances','the stimulation']
        self.at('The outcome depends jointly'); self.play(FadeOut(q[3]),run_time=.3)
        for cue,item in zip(cues,items):
            self.at(cue); self.play(Indicate(item,color=ORANGE,scale_factor=1),run_time=.3)
        bracket=VGroup(Line([3.1,2.2,0],[3.1,-2.95,0],color=GREY),Line([2.8,2.2,0],[3.1,2.2,0],color=GREY),Line([2.8,-2.95,0],[3.1,-2.95,0],color=GREY),arr([3.1,-.3,0],[4.1,-.3,0]))
        out=lines(['Firing','outcome'],TEXT,32).move_to([5.2,-.3,0]); box=SurroundingRectangle(out,color=TEXT,buff=.28)
        self.play(Create(bracket),FadeIn(out),Create(box),run_time=.35)
        self.at('The channel gains'); self.wait(max(.05,self.narration_s-self.elapsed()))
        self.play(FadeOut(items),FadeOut(bracket),FadeOut(out),FadeOut(box),FadeOut(q[0]),FadeOut(q[2]),FadeIn(lines(['The channel gains.','The neuron can lose.'],TEXT,44)),run_time=.3); self.wait(2.5); self.finish()

class S24Unmatched(SpokenScene):
    def construct(self):
        self.add(heading('Two different preparations'),mouse().scale(.7).move_to([-3.8,.6,0]),neuron(3.6,.6,1.2,TEAL_C),
            lines(['Knock-in mouse','R222S'],PURPLE,30).move_to([-3.8,-1.65,0]),lines(['Rat DRG neuron','Human channel expressed'],TEAL_C,28).move_to([3.6,-1.65,0]))
        self.at('not measured and matched'); self.play(FadeIn(txt('≠',0,.6,64)),FadeIn(chip('Starting availability: unmatched',TEXT,32).move_to([0,-3,0])),run_time=.45); self.finish()

class S25Account(SpokenScene):
    def construct(self):
        self.add(heading('Reconciling two results'),waveform(-3.5,-1.2,5.2,1.65,5,c=PURPLE),waveform(3.5,-1.2,5.2,1.3,5,True,RED),txt('R222S • knock-in mouse',-3.5,-2,28,PURPLE),txt('L1302F / L811P • rat DRG',3.5,-2,28,RED))
        self.add(*[Rectangle(width=5.5,height=2.5,color=GREY,stroke_opacity=.45).move_to([x,-.5,0]) for x in [-3.5,3.5]])
        bridge=VGroup(Line([-3.5,1.7,0],[3.5,1.7,0],color=GREY),Line([-3.5,.75,0],[-3.5,1.7,0],color=GREY),Line([3.5,.75,0],[3.5,1.7,0],color=GREY))
        self.at('an account that reconciles'); self.play(Create(bridge),FadeIn(txt('Account (reconciles two results)',0,2.25,30)),run_time=.5)
        tag=chip('Measured crossover',GREY,32).move_to([0,-3,0])
        self.at('not as a measured crossover'); self.play(FadeIn(tag),Create(Line(tag.get_left()+RIGHT*.15,tag.get_right()+LEFT*.15,color=RED,stroke_width=5)),run_time=.5); self.finish()

class S26Takeaway(SpokenScene):
    def construct(self):
        self.add(heading('Keep the shape of the argument'))
        a=chip('Channel effect',PURPLE,34).move_to([-4.6,0,0]); b=chip('Neuronal context',TEXT,32).move_to([0,0,0]); c=chip('Firing',TEXT,38).move_to([4.6,0,0])
        for z in [a,b,c]:
            z[0].stretch_to_fit_height(3.8); z[0].stretch_to_fit_width(3.7)
        outlines=VGroup(*[z[0].copy().set_color(GREY).set_opacity(.35) for z in [a,b,c]])
        self.add(outlines)
        self.at('A channel measurement'); self.play(FadeOut(outlines[0]),FadeIn(a),run_time=.4)
        self.at('the neuronal context'); self.play(FadeOut(outlines[1]),FadeIn(b),GrowArrow(arr(a.get_right(),b.get_left())),run_time=.4)
        self.at('determines its effect'); self.play(FadeOut(outlines[2]),FadeIn(c),GrowArrow(arr(b.get_right(),c.get_left())),run_time=.4)
        self.play(FadeIn(txt('Channel measurement',-4.6,-2.6,25,PURPLE)),FadeIn(txt('Neuronal context',0,-2.6,25)),FadeIn(txt('Context → firing',4.6,-2.6,25)),run_time=.3); self.finish()

class S27End(EndCard):
    LINE='A channel measurement tells you the channel effect; the neuronal context decides what it does to firing.'
    def construct(self):
        self.add(lines(['A channel measurement tells you the channel effect;','the neuronal context decides','what it does to firing.'],TEXT,36),txt('biochemistrypedia.com',0,-2.4,26,TEAL))
        self.wait(7)
