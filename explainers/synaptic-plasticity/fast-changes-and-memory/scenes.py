"""Chapter 6: fast changes and the road to memory.
COLOR MAP: YELLOW glutamate/light cue; BLUE AMPA; PURPLE NMDA;
ORANGE magnesium; TEAL calcium; PINK postsynaptic depolarization;
GREEN increase/LTP; RED decrease/LTD; TEXT stimuli/blocker;
GOLD questions; GREY membranes, vesicles, outlines, baseline.
Response bars are schematic amplitudes, explicitly labelled, except depletion:
R1=F*N*i, R2=F*(1-F)*N*i. LTP curves are computed illustrative models:
control(t)=100+50*(1-exp(-max(t,0)/3)); AP5(t)=100, never experimental data.
The opening blip is a Gaussian, exp(-((t-2)/.25)**2).
"""
import numpy as np
from bp_style import *
PURPLE='#B58CD9'
ORANGE='#F29E4C'
PINK='#E58FC0'

def label(s,x=0,y=0,size=28,color=TEXT):
    return T(s,size,color).move_to([x,y,0])
def heading(s):
    return label(s,y=3.18,size=32)
def bar(x,base,h,col=GREY,w=.85):
    return Rectangle(width=w,height=max(.02,h),stroke_color=col,fill_color=col,fill_opacity=.75).move_to([x,base+h/2,0])
def response_pair(x=0,y=-2.05,ratio=1,col=GREEN,scale=1):
    h=3.25*scale
    b=VGroup(bar(x-.95,y,h,GREY),bar(x+.95,y,h*ratio,col))
    base=Line([x-1.8,y,0],[x+1.8,y,0],color=GREY)
    names=VGroup(label('first',x-.95,y-.38,26),label('second',x+.95,y-.38,26))
    return VGroup(base,b,names)
def terminal():
    outline=RoundedRectangle(width=10.4,height=4.7,corner_radius=.6,stroke_color=GREY,fill_color=GREY,fill_opacity=.04).move_to([0,.15,0])
    ves=VGroup(*[Circle(radius=.27,color=GREY,fill_color=GREY,fill_opacity=.22).move_to([x,y,0]) for y in (-.9,.25) for x in (-3.6,-1.8,0,1.8,3.6)])
    membrane=Line([-4.6,-2.05,0],[4.6,-2.05,0],color=GREY,stroke_width=6)
    return VGroup(outline,ves,membrane)
def calcium():
    return VGroup(*[Dot([x,y,0],radius=.13,color=TEAL) for x,y in [(-3.6,1.3),(-2.5,1.1),(-1.3,1.4),(.1,1.25),(1.4,1.4)]])
def spike(n=1):
    return VGroup(label('Spike '+str(n),-5.25,2.7,28),Arrow([-5.15,2.3,0],[-4.4,1.7,0],color=TEXT,buff=.05))

def depletion_frame(question=True,full=False):
    # A single quantitative model, including the reservoir pictogram (ten units).
    title=heading('Simple depletion model')
    rules=label('No refilling · no facilitation · same current per vesicle',y=2.5,size=26)
    definition=label('F = fraction of pool released per pulse = 0.40',y=1.95,size=26)
    p=response_pair(2.5,-2.35,.6,RED,1.15)
    if question: p[1][1].set_opacity(0)
    q=label('?',3.45,-.45,65,GOLD) if question else label('ratio = 1 − F = 0.60',2.5,-3.2,30,RED)
    ask=label('Second response: larger or smaller?',y=-3.2,size=30,color=GOLD) if question else VGroup()
    dots=VGroup(*[Circle(radius=.3,color=TEXT,fill_color=GREY,fill_opacity=.35).move_to([-5.3+(i%3)*.85,-1.6+(i//3)*.8,0]) for i in range(10)])
    if not full:
        for v in list(dots)[:4]: v.set_stroke(opacity=.2).set_fill(opacity=0)
    pool=VGroup(dots,label('Vesicle pool',-4.35,-2.35,28))
    remain=VGroup(label('60% remains',-4.1,1.4,28,TEAL),Arrow([-4.1,1.1,0],[-4.1,.35,0],color=TEAL,buff=.07))
    if full: remain.set_opacity(0)
    return VGroup(title,rules,definition,p,q,ask,pool,remain)

def evidence_icon(kind,x,y):
    if kind=='maze':
        return VGroup(Circle(radius=.34,color=TEXT).move_to([x,y,0]),Square(.14,color=GOLD).move_to([x+.12,y-.08,0]))
    return VGroup(Line([x-.34,y,0],[x+.34,y,0],color=GREEN,stroke_width=6),Dot([x,y,0],color=YELLOW,radius=.13))
def ladder(active=None,question=False,studies=2):
    rails=VGroup(*[Line([x,-2.35,0],[x,2.4,0],color=GREY) for x in (-3.8,-2.3)])
    rows=VGroup()
    for i,(name,y) in enumerate([('Correlation',-1.7),('Necessity',0),('Sufficiency',1.7)]):
        c=GOLD if i==active else TEXT
        rows.add(VGroup(Line([-3.8,y,0],[-2.3,y,0],color=c,stroke_width=9),label(name+(' ?' if question and i==2 else ''),.6,y,42,c)))
    icons=VGroup()
    if studies>=1:
        icons.add(evidence_icon('maze',4.7,.15),label('Morris',4.7,-.5,26))
    if studies>=2:
        icons.add(evidence_icon('light',4.7,1.85),label('Nabavi',4.7,1.2,26))
    return VGroup(rails,rows,icons)
def memory_question():
    return VGroup(ladder(2,True),label('Is LTP alone enough\nto create this memory?',y=-3,size=30,color=GOLD))

def rat(x=-2.8,y=-.65,frozen=False):
    body=Ellipse(width=4.6,height=2.45,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([x,y,0])
    head=Ellipse(width=1.3,height=1.35,color=TEXT,fill_color=BG,fill_opacity=1).move_to([x+2.3,y+.55,0])
    ear=Circle(radius=.34,color=GREY).move_to([x+1.95,y+1.24,0])
    eye=Dot([x+2.6,y+.78,0],radius=.075,color=TEXT)
    tail=VMobject(color=GREY,stroke_width=4).set_points_smoothly([[x-2.2,y,0],[x-3,y+.3,0],[x-3.3,y+1,0]])
    hind=Line([x-1,y-1,0],[x-.1,y-1.3,0],color=GREY,stroke_width=6)
    if frozen:
        body.stretch(.93,0).stretch(1.08,1)
        VGroup(head,ear,eye).shift(LEFT*.22+UP*.16)
    return VGroup(body,head,ear,eye,tail,hind)
def input_inset(mode='normal'):
    c=RED if mode=='LTD' else GREEN if mode=='LTP' else GREY
    w=2 if mode=='LTD' else 9 if mode=='LTP' else 5
    box=RoundedRectangle(width=3.9,height=3.8,corner_radius=.2,color=GREY).move_to([4.25,.6,0])
    target=Ellipse(width=1.55,height=1.25,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([4.8,.1,0])
    paths=VGroup(*[Arrow([2.7,y,0],[4.05,.1,0],color=c,stroke_width=w,buff=.05,max_tip_length_to_length_ratio=.15) for y in (-.4,.2,.8)])
    return VGroup(box,target,paths,label('Auditory inputs',4.25,1.95,26),label('Lateral amygdala',4.25,-.95,26),label('Optical '+mode if mode!='normal' else 'Same pathway',4.25,1.3,28,c if mode!='normal' else TEXT))
def lever_stage(on=False,mode='normal'):
    r=rat()
    post=Line([1.45,-2.1,0],[1.45,-.8,0],color=GREY,stroke_width=7)
    handle=Line([.15,-.5,0],[1.45,-.8,0],color=TEXT,stroke_width=9)
    paw=Line([-1,-.9,0],[.15,-.5,0],color=TEXT,stroke_width=7)
    lamp=Circle(radius=.27,color=YELLOW,fill_color=YELLOW,fill_opacity=1 if on else 0).move_to([-4.7,2.25,0])
    l=label('Light cue: ON' if on else 'Light cue: OFF',-2.5,2.25,28,YELLOW if on else TEXT)
    return VGroup(r,post,handle,paw,lamp,l,input_inset(mode))
def posture(stage,frozen):
    endpoint=[-.65,-1.45,0] if frozen else [.15,-.5,0]
    return (Transform(stage[0],rat(frozen=frozen)),
            stage[3].animate.put_start_and_end_on([-1,-.9,0],endpoint))

def switch_light(scene,stage,on):
    scene.play(stage[4].animate.set_fill(YELLOW,1 if on else 0),Transform(stage[5],label('Light cue: ON' if on else 'Light cue: OFF',-2.5,2.25,28,YELLOW if on else TEXT)),run_time=.3)
def tally(n=0):
    return label('Press tally: '+str(n),4.25,-1.95,30)
def press(scene,stage,count,start=0,n=2):
    for i in range(n):
        scene.play(stage[0].animate.shift(DOWN*.10+RIGHT*.06),stage[2].animate.put_start_and_end_on([.15,-1.15,0],[1.45,-.8,0]),stage[3].animate.put_start_and_end_on([-1,-.9,0],[.15,-1.15,0]),Transform(count,tally(start+i+1)),run_time=.22)
        scene.play(stage[0].animate.shift(UP*.10+LEFT*.06),stage[2].animate.put_start_and_end_on([.15,-.5,0],[1.45,-.8,0]),stage[3].animate.put_start_and_end_on([-1,-.9,0],[.15,-.5,0]),run_time=.22)
def shock_symbol():
    bolt=VMobject(color=TEXT,stroke_width=7).set_points_as_corners([[-4.9,-1.9,0],[-5.25,-2.35,0],[-4.8,-2.35,0],[-5.15,-2.85,0]])
    return VGroup(bolt,label('Shock',-3.8,-2.6,28))

class S00Title(TitleCard):
    LESSON='Synaptic Plasticity'
    TITLE='Fast Changes, and the Road to Memory'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',y=1.7,size=26,color=TEAL),label(self.LESSON.upper(),y=.95,size=26))
        self.play(FadeIn(label('Fast Changes,\nand the Road to Memory',y=-.3,size=47)),Create(Line([-1.2,-1.7,0],[1.2,-1.7,0],color=GOLD)),run_time=.65)
        self.finish()

class S01Question(SpokenScene):
    def construct(self):
        axes=VGroup()
        for y,values,unit in [(1.35,(0,5,10),'ms'),(-1.05,(0,1,2),'h')]:
            axis=VGroup(Arrow([-5.4,y,0],[5.6,y,0],buff=0,color=GREY))
            for x,v in zip((-5,0,5),values):
                axis.add(Line([x,y-.12,0],[x,y+.12,0],color=TEXT),label(str(v)+' '+unit,x,y-.45,28))
            axes.add(axis)
        self.add(axes)
        self.at('milliseconds')
        blip=ParametricFunction(lambda t:np.array([-5+t,1.35+.75*np.exp(-((t-2)/.25)**2),0]),t_range=[0,10,.02],color=TEAL)
        self.play(Create(blip),FadeIn(label('milliseconds',y=2.65,size=34,color=TEAL)),run_time=.45)
        self.at('hours')
        self.play(Create(Line([-5,-.7,0],[5,-.7,0],color=GREEN,stroke_width=12)),FadeIn(label('hours',y=-.05,size=34,color=GREEN)),run_time=.4)
        self.at('Do they follow')
        self.play(FadeIn(label('The same rule?',y=-2.8,size=40,color=GOLD)),run_time=.4)
        self.finish()

class S02Different(SpokenScene):
    def construct(self):
        t=terminal().scale(.72).move_to([0,1,0])
        pre=label('Presynaptic terminal',y=2.95,size=30)
        spine=RoundedRectangle(width=7.5,height=1.6,corner_radius=.4,color=PINK).move_to([0,-1.8,0])
        post=label('Postsynaptic spine',y=-1.8,size=30,color=PINK)
        self.add(t,pre,spine,post)
        self.at('different machine')
        self.play(t[1][0].animate.shift(DOWN*.4),t[1][1].animate.shift(DOWN*.4),run_time=.6)
        self.at('They need no')
        no=label('No postsynaptic coincidence',y=-3.05,size=30)
        self.play(FadeIn(no),run_time=.4)
        self.at('they work mainly')
        self.play(FadeOut(spine),FadeOut(post),run_time=.3)
        self.play(Transform(t,terminal()),Transform(pre,heading('Presynaptic terminal')),run_time=.6)
        self.play(t[1][1].animate.shift(DOWN*.55),t[1][3].animate.shift(DOWN*.55),run_time=.7)
        self.at('also includes')
        self.play(Transform(no,label('Other short-term mechanisms also exist',y=-3.05,size=28)),run_time=.4)
        self.finish()

class S03Ppr(SpokenScene):
    def construct(self):
        p=response_pair(y=-2.15,ratio=1,col=GREEN,scale=1.15)
        self.add(p[0],p[2],heading('Paired responses · schematic'),label('response size',-4.6,.4,30).rotate(PI/2))
        self.at('Give two pulses')
        ticks=VGroup(*[Line([x,2.05,0],[x,2.65,0],color=TEXT,stroke_width=5) for x in (-.95,.95)])
        self.play(Create(ticks),GrowFromEdge(p[1][0],DOWN),GrowFromEdge(p[1][1],DOWN),run_time=.65)
        self.at('Divide the second')
        eq=label('second / first = 1.00 / 1.00',y=-3.15,size=30)
        self.play(FadeIn(eq),run_time=.4)
        self.at('paired pulse ratio')
        self.play(Transform(eq,label('Paired-pulse ratio = 1.00',y=-3.15,size=32)),run_time=.45)
        self.finish()

class S04Ppr2(SpokenScene):
    def construct(self):
        a=response_pair(-3,-2.15,1,GREEN,.88); b=response_pair(3,-2.15,1,RED,.88)
        self.add(a,b,heading('Response size · schematic'))
        self.at('Above one')
        self.play(Transform(a[1][1],bar(-2.05,-2.15,3.25*.88*1.45,GREEN)),FadeIn(label('ratio = 1.45',-3,2.45,30,GREEN)),run_time=.35)
        self.at('facilitation')
        self.play(FadeIn(label('Facilitation',-3,-3.05,32,GREEN)),run_time=.25)
        self.at('Below one')
        self.play(Transform(b[1][1],bar(3.95,-2.15,3.25*.88*.55,RED)),FadeIn(label('ratio = 0.55',3,2.45,30,RED)),run_time=.35)
        self.at('depression')
        self.play(FadeIn(label('Depression',3,-3.05,32,RED)),run_time=.25)
        self.finish()

class S05Fac(SpokenScene):
    def construct(self):
        t=terminal(); ca=calcium(); s=spike()
        self.add(t,heading('Facilitation · residual calcium'))
        self.at('classic explanation')
        self.play(FadeIn(s),Flash([-4.4,1.7,0],color=TEXT,flash_radius=.35),run_time=.35)
        self.play(FadeIn(ca,shift=DOWN*.5),t[1][0].animate.move_to([-3.6,-2.05,0]),run_time=.4)
        self.play(t[1][0].animate.shift(DOWN*.7).set_opacity(0),run_time=.3)
        self.at('residual calcium')
        left=label('Left over from spike 1',y=-3.1,size=30,color=TEAL)
        self.play(FadeIn(left),ca.animate.set_opacity(.65),run_time=.45)
        self.at('first spike')
        self.play(Transform(s,spike(2)),Flash([-4.4,1.7,0],color=TEXT,flash_radius=.35),run_time=.3)
        more=calcium().shift(RIGHT*.45+DOWN*.4)
        self.play(FadeIn(more),run_time=.3)
        release=VGroup(t[1][1],t[1][2],t[1][3])
        self.play(release.animate.set_y(-2.05),run_time=.35)
        self.play(release.animate.shift(DOWN*.65).set_opacity(0),FadeIn(label('Larger second release',2.8,1.95,28,GREEN)),run_time=.35)
        self.finish()

class S06Syt(SpokenScene):
    def construct(self):
        p=response_pair(1,-1.8,1.5,GREEN,.72)
        terminal_icon=RoundedRectangle(width=3.5,height=2.5,corner_radius=.4,color=GREY).move_to([-4,.3,0])
        ca=VGroup(*[Dot([-5+(i%3)*.8,.0+(i//3)*.7,0],color=TEAL,radius=.13) for i in range(6)])
        state=label('Normal',1,2.25,30,GREEN)
        self.add(p,terminal_icon,ca,state,label('Ca²⁺ in terminal',-4,-1.5,26,TEAL),label('Response size · schematic',1,-2.95,26))
        self.at('In')
        self.play(FadeIn(heading('Jackman, Regehr and colleagues · 2016')),run_time=.35)
        self.at('deleted')
        self.play(Transform(state,label('Synaptotagmin 7 deleted',1,2.25,29)),
                  Transform(p[1][1],bar(1.95,-1.8,3.25*.72,GREY)),run_time=.4)
        self.at('Facilitation was lost')
        self.play(Indicate(p[1],color=TEXT,scale_factor=1.02),run_time=.5)
        self.at('at the synapses tested')
        self.play(FadeIn(label('At the synapses tested',y=-3.55,size=26)),run_time=.35)
        self.at('residual calcium')
        self.play(FadeIn(label('Unchanged',-4,1.9,30,TEAL)),Indicate(ca,color=TEAL),run_time=.5)
        self.finish()

class S07Syt2(SpokenScene):
    def construct(self):
        outline=terminal()[0]
        ca=calcium()
        sensor=RoundedRectangle(width=5,height=1.8,corner_radius=.35,color=TEAL,fill_color=TEAL,fill_opacity=.05).move_to([0,-.55,0])
        self.add(outline,ca,sensor,heading('At the synapses tested'))
        self.at('a sensor')
        self.play(FadeIn(label('Synaptotagmin 7',0,-.55,36,TEAL)),run_time=.4)
        self.at('reads the leftover')
        glow=sensor.copy().set_stroke(TEAL,18,opacity=.25)
        self.play(*[d.animate.move_to([-1.9+i*.85,.48,0]) for i,d in enumerate(ca)],sensor.animate.set_fill(TEAL,.4),FadeIn(glow),run_time=.7)
        self.play(FadeIn(label('Reads leftover Ca²⁺',y=-3.05,size=34,color=TEAL)),run_time=.35)
        self.finish()

class S08Dep(SpokenScene):
    def construct(self):
        t=terminal(); self.add(t,heading('Depression · a depletion candidate'))
        self.at('first spike')
        s=spike()
        self.play(FadeIn(s),Flash([-4.4,1.7,0],color=TEXT,flash_radius=.35),run_time=.35)
        release=VGroup(*list(t[1])[:4])
        self.play(*[v.animate.move_to([x,-2.05,0]).stretch(.45,1) for v,x in zip(release,(-3.6,-1.8,0,1.8))],run_time=.5)
        self.at('uses up vesicles')
        used=label('40% used',y=-3.15,size=32,color=RED)
        self.play(release.animate.shift(DOWN*.7),FadeIn(used),run_time=.35)
        self.play(FadeOut(release),Transform(used,label('60% remain · illustrative pool',y=-3.15,size=30,color=TEAL)),run_time=.4)
        self.finish()

class S09Predict(SpokenScene):
    def construct(self):
        f=depletion_frame(full=True)
        self.add(f[0],f[3][0],f[3][2],f[6])
        self.at('no refilling')
        self.play(FadeIn(f[1]),run_time=.35)
        self.at('first pulse releases')
        depleted=depletion_frame()
        self.play(FadeIn(f[2]),GrowFromEdge(f[3][1][0],DOWN),Transform(f[6],depleted[6]),FadeIn(depleted[7]),run_time=.6)
        self.at('Will the second')
        self.play(FadeIn(f[4]),FadeIn(f[5]),run_time=.4)
        self.finish()

class S10Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(depletion_frame()); self.wait(5)

class S11Reveal(SpokenScene):
    def construct(self):
        f=depletion_frame();self.add(f)
        self.at('Smaller')
        self.play(FadeOut(f[4]),FadeOut(f[5]),f[3][1][1].animate.set_opacity(1),run_time=.45)
        self.at('of the pool')
        self.play(Indicate(f[7],color=TEAL,scale_factor=1.06),run_time=.4)
        self.at('so the second')
        self.play(FadeIn(label('ratio = 1 − F = 0.60',2.5,-3.2,30,RED)),run_time=.4)
        self.finish()

class S12Limit(SpokenScene):
    def construct(self):
        f=depletion_frame(False)
        self.add(f)
        self.at('does not prove')
        self.play(FadeOut(f[0]),FadeOut(f[1]),FadeOut(f[2]),FadeOut(f[7]),FadeIn(heading('A ratio does not prove depletion')),run_time=.4)
        mark=label('Cause ?',4.05,2.35,34,GOLD)
        self.play(FadeIn(mark),run_time=.3)
        self.at('Other processes')
        candidates=VGroup(*[RoundedRectangle(width=1.1,height=.7,corner_radius=.12,color=GOLD).move_to([x,.9,0]) for x in (2.7,4.05,5.4)])
        candidates.set_y(1.3)
        arrows=VGroup(*[Arrow([x,.93,0],[target,-.08,0],color=GOLD,buff=.04,
                                 max_tip_length_to_length_ratio=.18)
                         for x,target in zip((2.7,4.05,5.4),(3.12,3.45,3.78))])
        self.play(Create(candidates),Create(arrows),run_time=.6)
        self.finish()

class S13Memory(SpokenScene):
    def construct(self):
        # Chapter 1's Cell A -> Cell B connection cartoon, without a central midline.
        self.add(heading('Donald Hebb · 1949'))
        self.at('back to Hebb')
        cells=VGroup(*[Circle(radius=.55,color=TEXT).move_to([x,.9,0]) for x in (-4,4)])
        wire=Line([-3.4,.9,0],[3.4,.9,0],color=GREY)
        syn=RoundedRectangle(width=.9,height=1.15,corner_radius=.15,color=GOLD,fill_color=GOLD,fill_opacity=.2).move_to([0,.9,0])
        self.play(FadeIn(cells),Create(wire),FadeIn(syn),FadeIn(label('Cell A',-4,-.05,28)),FadeIn(label('Cell B',4,-.05,28)),run_time=.4)
        wording=label('When one cell repeatedly helps fire another,\nthe connection between them grows.',y=-1.25,size=30)
        self.play(FadeIn(wording),syn.animate.set_stroke(GREEN,8),run_time=.4)
        self.at('Does memory')
        self.play(FadeIn(label('Does memory use LTP?',y=-2.9,size=38,color=GOLD)),run_time=.4)
        self.finish()

class S14Corr(SpokenScene):
    def construct(self):
        l=ladder(studies=0);self.add(l)
        self.at('A correlation')
        self.play(Transform(l,ladder(0,studies=0)),run_time=.3)
        self.at('learning alongside')
        self.play(FadeIn(label('Learning alongside potentiation',y=-2.75,size=30)),run_time=.35)
        self.at('is not proof')
        self.play(FadeIn(label('≠ proof',4.7,-1.7,30,GOLD)),run_time=.3)
        self.finish()

def maze_panel():
    pool=Circle(radius=1.62,color=TEXT).move_to([-3.9,.5,0])
    platform=DashedVMobject(Circle(radius=.22,color=GOLD).move_to([-3.3,.9,0]))
    hidden=label('Hidden platform',-3.8,2.45,27,GOLD)
    leader=Line([-3.6,2.15,0],[-3.3,1.16,0],color=GOLD)
    direct=Line([-4.8,.0,0],[-3.3,.9,0],color=GREEN,stroke_width=5)
    wander=VMobject(color=RED,stroke_width=5).set_points_smoothly([[-4.8,0,0],[-4.5,-.25,0],[-3.2,-.15,0],[-3,.65,0],[-4,1.45,0],[-4.75,.85,0],[-3.9,-.4,0],[-3.5,-.2,0]])
    return VGroup(pool,platform,hidden,leader,direct,wander)
def ltp_plot():
    # Explicit model and schematic label: no invented experimental measurements.
    ax=Axes(x_range=[-5,15,5],y_range=[50,175,50],x_length=5.2,y_length=3.75,axis_config={'color':GREY,'include_tip':False}).move_to([3,.05,0])
    ticks=VGroup(*[label(str(t),*ax.c2p(t,50)[:2]+np.array([0,-.3]),26) for t in (-5,0,5,10,15)],*[label(str(y),*ax.c2p(-5,y)[:2]+np.array([-.45,0]),26) for y in (50,100,150)])
    control=ax.plot(lambda t:100+50*(1-np.exp(-max(t,0)/3)),x_range=[-5,15,.1],color=GREEN)
    blocked=ax.plot(lambda t:100,x_range=[-5,15,.1],color=RED)
    tet=VGroup(Arrow(ax.c2p(0,70),ax.c2p(0,95),color=TEXT,buff=.02),label('tetanus',2.95,-1.28,26))
    labs=VGroup(label('minutes',3,-2.5,28),label('response, % of baseline',3,2.55,26),label('Control · schematic',3.8,1.62,26,GREEN),label('AP5',5.2,-.85,28,RED))
    return VGroup(ax,ticks,control,blocked,tet,labs)

class S15Morris(SpokenScene):
    def construct(self):
        maze=maze_panel();plot=ltp_plot()
        self.add(maze[0],maze[1],maze[2],maze[3],plot[0],plot[1],plot[4],plot[5][0],plot[5][1],heading('Morris and colleagues · 1986'))
        swimmer=rat(-4.8,0).scale(.15,about_point=[-4.8,0,0])
        self.add(swimmer,label('Control path',-4,-1.5,26,GREEN),Line([-5.6,-1.5,0],[-5.1,-1.5,0],color=GREEN,stroke_width=5))
        self.at('infused')
        syringe=VGroup(Line([-4.25,1.5,0],[-4.45,.15,0],color=TEXT,stroke_width=5),Line([-4.55,1.5,0],[-3.95,1.5,0],color=TEXT,stroke_width=5))
        infusion=label('AP5 infused · NMDA blocker',3,1.2,28)
        self.play(FadeIn(infusion),Create(syringe),run_time=.45)
        self.at('Place learning was impaired')
        self.play(FadeOut(syringe),Create(maze[4]),Create(maze[5]),MoveAlongPath(swimmer,maze[5]),FadeIn(label('AP5: place learning impaired',-3.7,-1.95,26,RED)),run_time=.8)
        self.at('visual task was spared')
        # Direct visual discrimination route, labelled; a separate task, not a visible-platform claim.
        visual=VGroup(label('Visual discrimination',-3.7,-2.5,26),Square(.25,color=TEXT).move_to([-5.2,-3,0]),Triangle(color=TEXT).scale(.16).move_to([-2.4,-3,0]),Arrow([-4.8,-3,0],[-2.8,-3,0],color=GREEN,buff=.02),label('learned normally',-3.7,-3.5,26,GREEN))
        self.play(FadeIn(visual),run_time=.5)
        self.at('hippocampal')
        self.play(FadeOut(infusion),run_time=.15)
        self.play(Create(plot[2]),Create(plot[3]),FadeIn(plot[5][2]),FadeIn(plot[5][3]),
                  FadeIn(label('Hippocampal LTP suppressed',3,-3.3,26,RED)),run_time=.7)
        self.finish()

class S16Morris2(SpokenScene):
    def construct(self):
        l=ladder(studies=1);self.add(l)
        self.at('drug reached many synapses')
        self.play(FadeIn(label('Drug reached many synapses',y=-2.7,size=30,color=GOLD)),run_time=.4)
        self.at('receptors were needed')
        self.play(Transform(l,ladder(1,studies=1)),FadeIn(heading('Receptors needed for both')),run_time=.4)
        self.at('not that the learning')
        self.play(FadeIn(label('Not shown: that learning is LTP',y=-3.4,size=32,color=GOLD)),run_time=.4)
        self.finish()

class S17Nabavi(SpokenScene):
    def construct(self):
        target=Ellipse(width=5,height=4.8,color=GREY,fill_color=GREY,fill_opacity=.08).move_to([3,-.3,0])
        inputs=VGroup(*[Arrow([-5.8,y,0],[.55,-.3+y*.3,0],buff=.02,color=GREY,stroke_width=6) for y in (-1.8,-.3,1.2)])
        self.add(target,inputs,heading('Nabavi, Malinow and colleagues · 2014'),
                 label('Auditory inputs',-3.6,.25,30),label('Lateral\namygdala',3,-.3,36))
        self.at('used light')
        lamp=VGroup(Circle(radius=.28,color=YELLOW,fill_color=YELLOW,fill_opacity=1).move_to([-3.5,2.25,0]),Arrow([-3.5,1.9,0],[-3.5,1.35,0],color=YELLOW,buff=.05),label('Light',-4.5,2.25,28,YELLOW))
        channels=VGroup(*[RoundedRectangle(width=.35,height=.55,corner_radius=.08,color=YELLOW).move_to([-1.25,y,0]) for y in (-1.2,-.3,.6)])
        channel_label=label('light-gated channels',-1.2,-2.55,27,YELLOW)
        leader=Line([-1.2,-2.23,0],[-1.25,-1.52,0],color=YELLOW)
        self.play(FadeIn(lamp),Create(channels),FadeIn(channel_label),Create(leader),inputs.animate.set_color(YELLOW),run_time=.5)
        self.at('auditory inputs')
        self.play(Indicate(inputs,color=YELLOW,scale_factor=1.02),run_time=.4)
        self.at('lateral amygdala')
        self.play(Indicate(target,color=TEXT,scale_factor=1.02),run_time=.4)
        self.at('a cue')
        self.play(FadeIn(label('Light is the cue',y=-3.4,size=30,color=YELLOW)),run_time=.35)
        self.finish()

class S18Nabavi2(SpokenScene):
    def construct(self):
        stage=lever_stage();count=tally();result=label('Normal pressing',-2,-3.15,32)
        self.add(stage,count,result)
        self.at('After light')
        press(self,stage,count,0,2)
        self.at('paired with shock')
        switch_light(self,stage,True)
        shock=shock_symbol()
        self.play(FadeIn(shock),Flash([-5,-2.4,0],color=TEXT,flash_radius=.4),FadeIn(heading('Light paired with shock')),run_time=.35)
        self.at('light suppressed')
        self.play(FadeOut(shock),*posture(stage,True),Transform(result,label('Freezing · pressing suppressed',-1.6,-3.15,32,RED)),run_time=.35)
        self.at('Optical')
        self.play(Transform(stage[6],input_inset('LTD')),run_time=.4)
        self.at('removed the response')
        self.play(*posture(stage,False),Transform(result,label('Pressing resumes with light ON',-1.6,-3.15,30)),run_time=.3)
        press(self,stage,count,2,3)
        self.finish()

class S19Nabavi3(SpokenScene):
    def construct(self):
        stage=lever_stage(True,'LTD');count=tally(5);result=label('Pressing resumes with light ON',-1.6,-3.15,30)
        self.add(stage,count,result)
        self.at('Optical')
        self.play(Transform(stage[6],input_inset('LTP')),FadeIn(heading('Optical LTP afterwards')),
                  *posture(stage,True),Transform(result,label('Freezing · pressing suppressed again',-1,-3.15,30,RED)),run_time=.35)
        self.at('restored it')
        self.wait(.35)
        self.finish()

class S20Predict2(SpokenScene):
    def construct(self):
        l=ladder();self.add(l)
        self.at('at these inputs')
        self.play(Transform(l,ladder(2,True)),run_time=.35)
        self.at('on its own')
        self.play(FadeIn(memory_question()[1]),run_time=.35)
        self.finish()

class S21Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(memory_question());self.wait(5)

class S22Reveal2(SpokenScene):
    def construct(self):
        stage=lever_stage(False);count=tally();self.add(stage,count)
        self.at('in rats never')
        self.play(FadeIn(heading('Never given light–shock pairing')),run_time=.4)
        press(self,stage,count,0,2)
        self.at('at these inputs')
        self.play(Transform(stage[6],input_inset('LTP')),run_time=.4)
        self.at('no response')
        switch_light(self,stage,True)
        result=label('Light ON: pressing continues',-1.6,-2.75,30)
        self.play(FadeIn(result),run_time=.3)
        press(self,stage,count,2,2)
        self.at('Something set up')
        scope=label('Something set up by the pairing was needed',y=-3.45,size=28,color=GOLD)
        self.play(FadeIn(scope),run_time=.4)
        press(self,stage,count,4,2)
        self.at('That holds for')
        self.play(Transform(scope,label('This pathway · rats · this task',y=-3.45,size=30)),run_time=.4)
        press(self,stage,count,6,2)
        self.finish()

class S23Takeaway(SpokenScene):
    def construct(self):
        divider=Line([0,-2.6,0],[0,3.2,0],color=GREY)
        t=terminal().scale(.59).move_to([-3.3,1.05,0])
        self.add(t,divider)
        self.at('fast changes')
        self.play(FadeIn(label('Fast changes here',-3.3,3.1,32)),run_time=.4)
        self.at('presynaptic machine')
        left=VGroup(label('Presynaptic examples',-3.3,-.75,28),label('No pre/post coincidence',-3.3,-1.55,27),label('Other mechanisms exist',-3.3,-2.35,27))
        self.play(FadeIn(left),run_time=.4)
        necessity=chip('Necessity',GOLD,size=34).move_to([3.25,1.6,0])
        sufficiency=chip('Sufficiency',GOLD,size=34).move_to([3.25,.3,0])
        correlation=label('Correlation alone is not enough',y=-3.2,size=32,color=TEXT)
        right=VGroup(label('LTP → memory',3.25,3.1,34),necessity,sufficiency,
                     label('This pathway\nRats · this task',3.25,-1.45,29),correlation)
        self.at('And linking')
        self.play(FadeIn(right),run_time=.35)
        self.at('tests of necessity')
        self.play(Indicate(necessity,color=GOLD,scale_factor=1.04),run_time=.35)
        self.at('and sufficiency')
        self.play(Indicate(sufficiency,color=GOLD,scale_factor=1.04),run_time=.35)
        self.at('not correlation alone')
        self.play(Indicate(correlation,color=TEXT,scale_factor=1.02),run_time=.35)
        self.finish()

class S24End(EndCard):
    LINE='Fast changes here are presynaptic; LTP–memory links need necessity and sufficiency.'
    def construct(self):
        self.add(label('KEEP THE DISTINCTION',y=2.5,size=28,color=TEAL))
        self.play(FadeIn(label('Fast changes here are presynaptic;\nLTP–memory links need\nnecessity and sufficiency.',y=.3,size=40)),run_time=.6)
        self.play(FadeIn(label('biochemistrypedia.com',y=-2.3,size=26,color=TEAL)),run_time=.3)
        self.finish()
