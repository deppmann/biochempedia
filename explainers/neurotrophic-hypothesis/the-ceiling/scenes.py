"""Chapter 5 fix round.
COLOR MAP: BLUE control/undecided neuron; GREEN survival/extra NGF group;
YELLOW NGF/support; RED death; TEAL cohort ceiling; PURPLE TrkA;
LIGHT axes/tissue/annotations. Biological counts are schematic, not data.
Allocation traces: min(N, floor(F/q)); shortfall example: N=900, q=1.5.
"""
import numpy as np
from bp_style import *
PURPLE='#B58CD9'
LIGHT='#C0C6D0'
LTEAL='#8FE8EE'
# Keep pipeline-generated timing logs outside the deliverable directory.
class TimedScene(SpokenScene):
    def at(self, phrase, lead=.2, nth=0):
        target=self.t_of(phrase,nth)-lead
        rest=target-self.elapsed()
        if rest>.02: self.wait(rest)

def txt(s,x=0,y=0,size=30,color=TEXT):
    return T(s,size,color).move_to([x,y,0])
def heading(s,color=TEXT): return txt(s,y=3.15,size=34,color=color)
def foot(s,color=LIGHT,y=-3.15,size=27): return txt(s,y=y,size=size,color=color)
def countdown(scene,n=5,pos=(5.9,2.6)):
    for k in range(n,0,-1):
        ring=Circle(radius=.55,color=YELLOW,stroke_width=6).move_to([pos[0],pos[1],0]); num=txt(str(k),pos[0],pos[1],46,YELLOW)
        scene.add(ring,num); scene.wait(1); scene.remove(ring,num)
def dot(p,color=BLUE,r=.5,op=.8):
    return Circle(radius=r,stroke_color=color,stroke_width=3,fill_color=color,fill_opacity=op).move_to(p)
def state(c,color,op=.8): return c.animate.set_stroke(color,opacity=1).set_fill(color,opacity=op)
def arr(a,b,color=LIGHT,buff=.12): return Arrow(a,b,buff=buff,color=color,stroke_width=4)
def cells(center=(0,0),color=BLUE,op=.8):
    return VGroup(*[dot([center[0]+x,center[1]+y,0],color,.62,op) for y in [1.1,-1.1] for x in [-2,0,2]])
def options():
    return VGroup(*[VGroup(RoundedRectangle(width=5.5,height=1.9,corner_radius=.15,color=LIGHT),txt(s,size=30)).move_to([x,y,0]) for s,x,y in [('No change',-3,1.3),('More survive',3,1.3),('New ganglia\nin wrong places',-3,-1.15),('Fibres invade\nevery tissue',3,-1.15)]])
def comparison():
    a=cells((-3.2,-.05)).scale(.72); b=cells((3.2,-.05),GREEN).scale(.72)
    for i in [1,3,5]: a[i].set_fill(RED,opacity=.12).set_stroke(RED)
    b[5].set_fill(RED,opacity=.12).set_stroke(RED)
    labs=VGroup(txt('Control',-3.2,2.15,color=BLUE),txt('Extra NGF',3.2,2.15,color=GREEN))
    return a,b,labs

def count_chart(stages=3,result=False):
    ax=Axes(x_range=[0,3,1],y_range=[0,100,50],x_length=9.3,y_length=4.7,tips=False,axis_config={'color':LIGHT,'include_ticks':False}).move_to([.6,0,0])
    g=VGroup(txt('Chick dorsal root ganglia',y=3.4,size=34),ax,txt('neurons per ganglion (schematic)',-5.75,0,26).rotate(PI/2),txt('blue = control    green = extra NGF',y=2.85,size=27),foot('NGF reduced the normal death' if result else 'Schematic counts • not experimental values',GREEN if result else LIGHT,y=-3.5))
    for v in [0,50,100]: g.add(txt(str(v),*ax.c2p(0,v)[:2]+np.array([-.4,0]),size=26))
    groups=[]
    for j,(stage,vals) in enumerate(zip(['Before','During','After'],[(100,100),(65,90),(40,80)])):
        x=j+.5; bars=VGroup()
        for dx,val,col in [(-.13,vals[0],BLUE),(.13,vals[1],GREEN)]:
            a=ax.c2p(x+dx,0); b=ax.c2p(x+dx,val)
            bars.add(Rectangle(width=.62,height=b[1]-a[1],stroke_width=0,fill_color=col,fill_opacity=.8).move_to((a+b)/2))
        bars.add(txt(stage,*ax.c2p(x,0)[:2]+np.array([0,-.42]),size=28))
        if j==1:
            for dx,n in [(-.13,5),(.13,1)]:
                for k in range(n):
                    p=ax.c2p(x+dx,12+k*12)
                    bars.add(Line(p+LEFT*.12+DOWN*.08,p+RIGHT*.12+UP*.08,color=RED,stroke_width=5))
        groups.append(bars)
        if j<stages:g.add(bars)
    g.add(txt('red marks: dying nuclei',x=3.9,y=2.0,size=26,color=RED))
    return g,groups

def checklist(n=1):
    g=VGroup(heading('Saved, or newly born?'))
    for i,s in enumerate(['1   Count neurons + dying nuclei','2   Mark dividing cells','3   Check usual cell identity'][:n]):
        cy=[2.0,.4,-1.85][i]; h=[1.3,1.3,2.5][i]
        card=RoundedRectangle(width=11.4,height=h,corner_radius=.15,color=[BLUE,YELLOW,GREEN][i]).move_to([0,cy,0])
        item=VGroup(card,txt(s,y=cy+(.55 if i==2 else 0),size=31))
        if i==2: item.add(txt('e.g. tyrosine hydroxylase in sympathetic neurons',y=-1.95,size=26,color=GREEN),txt('enzyme for noradrenaline',y=-2.5,size=26,color=LIGHT))
        g.add(item)
    return g

def division():
    body=RoundedRectangle(width=9.4,height=5.2,corner_radius=.8,color=LIGHT).move_to([-1.4,-.25,0])
    xs=[-4.4,-1.4,1.6]
    c=VGroup(*[dot([x,1.0,0],BLUE,.8) for x in xs])
    pairs=VGroup(*[VGroup(dot([x-.5,-1.3,0],YELLOW,.5),dot([x+.5,-1.3,0],YELLOW,.5),arr([x,.1,0],[x,-.65,0],YELLOW)) for x in xs])
    return body,c,pairs

def source(): return chip('500 units/day',YELLOW,30).move_to([0,2,0])
def sharing(question=False):
    c=VGroup(*[dot([x,y,0],YELLOW,.9,.45) for y in [.35,-1.6] for x in [-3.6,0,3.6]])
    for d in c:
        d.set_fill(YELLOW,opacity=.15)
        half=Sector(radius=.9,start_angle=PI,angle=PI,fill_color=YELLOW,fill_opacity=.65,stroke_width=0).move_arc_center_to(d.get_center())
        d.add(half)
    h=txt('Every neuron gets half. How many survive?' if question else 'Equal sharing',y=3.45,size=34)
    src=chip('500 units/day',YELLOW,32).move_to([0,2.45,0])
    flow=VGroup(*[arr([0,2.0,0],d.get_top()+UP*.05,YELLOW,.03) for d in c[:3]])
    g=VGroup(h,src,flow,c,foot('500 ÷ 1,000 = 0.5 each • each dot = many neurons',y=-2.95,size=27),foot('Pause and predict' if question else 'Needs 1 unit per neuron per day',YELLOW if question else LIGHT,y=-3.5,size=34 if question else 27))
    return g,c

def dials(fast=False):
    g=VGroup()
    for x,title,right in [(-3.4,'Commitment',fast),(3.4,'Sharing',not fast)]:
        g.add(txt(title,x,2.75,34))
        g.add(Arc(radius=2.2,start_angle=0,angle=PI,color=LIGHT,stroke_width=5).shift([x,-.2,0]))
        a=PI*(.22 if right else .78)
        g.add(Line([x,-.2,0],[x+2.0*np.cos(a),-.2+2.0*np.sin(a),0],color=RED if title=='Commitment' else YELLOW,stroke_width=9))
        g.add(txt('Slow',x-1.65,-.65,28,LIGHT),txt('Fast',x+1.65,-.65,28,LIGHT))
    return g

def timing_frame(fast=False,caption=False):
    c=VGroup(*[dot([x,-1.95,0],GREEN if i in ([0] if fast else [0,2,4]) else RED,.65,.3 if fast else .8) for i,x in enumerate(np.linspace(-5.0,5.0,6))])
    for i in range(6):
        if i not in ([0] if fast else [0,2,4]):c[i].set_fill(RED,opacity=.12)
    return VGroup(txt('The count depends on timing',y=3.5,size=34),dials(fast),c,foot('Far fewer • depends on timing' if fast else 'About half left (about 500) • illustrative',GREEN if not fast else LIGHT,y=-3.0,size=34),foot('Equal sharing alone does not say how many survive.' if caption else 'Illustrative timing outcomes',y=-3.55)),c

RC=1.6; LC=np.array([-3.4,-.25,0]); RN=np.array([3.4,-.25,0])
def race(winner=False):
    return dot(LC,GREEN if winner else BLUE,RC,.85 if winner else .3),dot(RN,BLUE,RC,.3)
def rec_at(center,deg,color=PURPLE):
    a=deg*DEGREES; p=center+RC*np.array([np.cos(a),np.sin(a),0])
    return RoundedRectangle(width=.36,height=.64,corner_radius=.08,color=color,fill_color=color,fill_opacity=.7).move_to(p).rotate(a-PI/2)
def receptors(): return VGroup(*[rec_at(LC,d) for d in [120,90,150,60,30,180]])
def p75_parts():
    r=rec_at(RN,40,LIGHT); lab=chip('p75',LIGHT,30).move_to([5.9,1.95,0])
    return r,lab,Line(lab.get_bottom(),r.get_center()+UP*.1+RIGHT*.1,color=LIGHT,stroke_width=3)
def competition(winner=True):
    a,b=race(winner); g=VGroup(heading('Mouse sympathetic neurons'),a,b)
    if winner:
        r=receptors(); g.add(r,txt('TrkA',-5.8,2.15,32,PURPLE),Line([-5.35,1.9,0],r[0].get_center()+LEFT*.1,color=PURPLE),txt('weak NGF signal',3.4,-2.2,30,LIGHT))
    return g,a,b

class S00Title(TitleCard):
    LESSON='The Neurotrophic Hypothesis Tested'
    TITLE='The Ceiling, and the Sharing Puzzle'
class S01Q(TimedScene):
    def construct(self):
        c=cells().scale(1.25).shift(DOWN*.2)
        self.add(heading('Can extra NGF enlarge it without limit?'),c,foot('Ganglion • schematic',BLUE))
        self.at('can extra'); self.play(GrowArrow(arr([4,-1.9,0],[4,1.7,0],YELLOW)),FadeIn(txt('?',5,0,64,YELLOW)),run_time=.6); self.finish()
class S02Setup(TimedScene):
    def construct(self):
        # Egg with a curled chick embryo inside; daily NGF drops across a death-period band.
        egg=Ellipse(width=3.0,height=3.7,color=LIGHT,stroke_width=4,fill_color=LIGHT,fill_opacity=.12).move_to([-4.4,.85,0])
        body=Arc(radius=.85,start_angle=-PI*.55,angle=PI*1.5,color=BLUE,stroke_width=26).move_to([-4.4,.75,0])
        head=dot([-4.95,1.55,0],BLUE,.45); eye=dot([-5.1,1.65,0],TEXT,.06)
        beak=Triangle(color=BLUE,fill_color=BLUE,fill_opacity=.8).scale(.17).rotate(PI/2).move_to([-5.5,1.5,0])
        bud=Ellipse(width=.6,height=.28,color=BLUE,fill_color=BLUE,fill_opacity=.5).move_to([-3.6,.5,0])
        self.add(heading('NGF across the death period'),egg,body,head,eye,beak,bud,txt('Chick embryo',-1.0,.5,34))
        self.at('extra'); ngf=chip('NGF, daily',YELLOW,36).move_to([1.4,1.6,0]); self.play(FadeIn(ngf),run_time=.3)
        self.at('every day'); self.play(Create(arr([1.4,1.2,0],[1.4,-.95,0],YELLOW)),run_time=.2); axis=Line([-6.2,-2.45,0],[6.2,-2.45,0],color=LIGHT,stroke_width=4); self.play(Create(axis),run_time=.2)
        for i,x in enumerate(np.linspace(-5.4,5.4,7)):
            self.add(txt(str(i+1),x,-2.9,28,LIGHT)); p=dot([x,-1.5,0],YELLOW,.2); self.play(FadeIn(p,shift=DOWN*.25),run_time=.08)
        self.add(txt('Day (schematic)',y=-3.5,size=28))
        self.at('through the period'); self.play(FadeIn(Rectangle(width=12.4,height=1.2,color=RED,fill_opacity=.14).move_to([0,-1.85,0])),FadeIn(txt('Normal death period',4.5,-.5,34,RED)),run_time=.4); self.finish()
class S03Predict(TimedScene):
    def construct(self):
        self.add(heading('Predict')); c=options()
        for cue,card in zip(['No','More survivors','New ganglia','invading every'],c): self.at(cue); self.play(FadeIn(card),run_time=.3)
        self.finish()
class S04Pause(Scene):
    def construct(self): self.camera.background_color=BG; self.add(heading('Predict'),options(),foot('Pause and predict',YELLOW,y=-3.3,size=34)); countdown(self,5,(6.0,3.15))
class S05Reveal(TimedScene):
    def construct(self):
        cards=options(); self.add(heading('Result'),cards)
        self.at('More of'); self.play(cards[1][0].animate.set_stroke(GREEN).set_fill(GREEN,opacity=.3),*[cards[i].animate.set_opacity(.28) for i in [0,2,3]],run_time=.2); self.wait(1)
        a,b,l=comparison(); self.play(FadeOut(cards),FadeIn(VGroup(a,b,l,foot('blue = control    green = extra NGF',size=28))),run_time=.35); self.finish()
class S06More(TimedScene):
    def construct(self):
        a,b,l=comparison(); l.shift(UP*.4); self.add(a,b,l,heading('Survivors grow and branch'),txt('control: unchanged',-3.2,-2.25,27,BLUE))
        self.at('grow larger'); self.play(*[b[i].animate.scale(1.32) for i in range(5)],run_time=.5)
        self.at('sprout more'); branches=VGroup()
        for i in [0,2,3]:
            p=b[i].get_center(); end=p+UP*.95
            branches.add(Line(p+UP*.58,end,color=GREEN),Line(end,end+LEFT*.45+UP*.3,color=GREEN),Line(end,end+RIGHT*.45+UP*.3,color=GREEN))
        self.play(Create(branches),run_time=.5)
        self.at('no neuron'); card=chip('Type change',LIGHT,40).move_to([1.1,-2.65,0]); self.play(FadeIn(card),run_time=.2); self.play(Create(Line(card.get_left()+RIGHT*.15,card.get_right()+LEFT*.15,color=RED,stroke_width=2)),run_time=.25); self.finish()
class S071981(TimedScene):
    def construct(self):
        credit=VGroup(heading('Counting across time'),txt('Hamburger, Brunso-Bechtold and Yip',y=1,size=31),txt('1981',y=0,size=38,color=TEAL),foot('Chick dorsal root ganglia'))
        self.add(credit)
        self.at('counted chick'); g,stages=count_chart(1); self.play(FadeOut(credit),FadeIn(g),run_time=.4)
        self.at('across the death'); self.play(FadeIn(stages[1]),run_time=.45); self.play(FadeIn(stages[2]),run_time=.45); self.finish()
class S08Found(TimedScene):
    def construct(self):
        g,_=count_chart(); self.add(g)
        self.at('the normal death'); self.play(Transform(g[4],foot('NGF reduced the normal death',GREEN,y=-3.5)),run_time=.4); self.finish()
class S09Beat(Scene):
    def construct(self): self.camera.background_color=BG; self.add(count_chart(result=True)[0]); self.wait(3)
class S10How(TimedScene):
    def construct(self):
        gang=VGroup()
        for x in [-4.6,0,4.6]:
            box=RoundedRectangle(width=3.5,height=2.7,corner_radius=.5,color=LIGHT).move_to([x,-.55,0])
            dts=VGroup(*[dot([x+dx,-.55+dy,0],BLUE,.4,.8) for dy in [.55,-.55] for dx in [-1,0,1]])
            gang.add(VGroup(box,dts))
        tl=VGroup(arr([-2.8,-.55,0],[-1.8,-.55,0],LIGHT,.05),arr([1.8,-.55,0],[2.8,-.55,0],LIGHT,.05))
        lab=txt('Follow the same ganglia across time',y=-2.65,size=34,color=BLUE)
        self.add(heading('Saved, or newly born?'),gang,tl,lab)
        self.at('Count neurons'); self.play(FadeIn(checklist()[1]),run_time=.3); self.finish()
class S11Mark(TimedScene):
    def construct(self):
        c=checklist(3); self.add(*c[:2]); self.at('Mark dividing'); self.play(FadeIn(c[2]),run_time=.35)
        self.at('Then check'); self.play(FadeIn(c[3]),run_time=.35); self.finish()
class S12Div(TimedScene):
    def construct(self):
        body,c,pairs=division(); self.add(heading('Early chick embryo'),body,c,foot('Primary sympathetic ganglion',y=-3.45))
        self.at('extra'); ng=chip('Extra NGF',YELLOW,30).move_to([5.75,-.3,0]); self.play(FadeIn(ng),Create(arr([4.6,-.3,0],[2.75,-.3,0],YELLOW)),run_time=.4)
        self.at('increase division'); self.play(*[Transform(c[i].copy(),pairs[i]) for i in range(3)],run_time=.7); self.finish()
class S13Div2(TimedScene):
    def construct(self):
        c=VGroup(*[dot([-4,y,0],BLUE,.45) for y in [1.25,0,-1.25]])
        marks=VGroup(*[VGroup(dot([-5.4,y+.15,0],YELLOW,.23),dot([-4.95,y-.15,0],YELLOW,.23)) for y in [1.25,0,-1.25]])
        target=RoundedRectangle(width=1.6,height=3.8,corner_radius=.2,color=LIGHT).move_to([5,0,0])
        self.add(heading('Division and death are separate counts'),c,marks,target,txt('Target',5,2.35,28))
        self.at('before sympathetic axons'); fibres=VGroup(*[Line(d.get_right(),[2.7,d.get_y(),0],color=BLUE,stroke_width=4) for d in c]); self.play(Create(fibres),FadeIn(txt('axons not yet at target',.1,2.1,28,BLUE)),run_time=.5)
        self.at('The extra division'); self.play(FadeIn(txt('dividing: up',-3.1,-2.25,29,YELLOW)),FadeIn(txt('dying: slightly down',2.1,-2.25,29,RED)),run_time=.35)
        self.at('other than'); self.play(FadeIn(foot('The checks tell them apart • a little less death')),run_time=.35); self.finish()
class S14Limit(TimedScene):
    def construct(self):
        c=VGroup(*[dot([x,-.2,0],BLUE,.95) for x in [-5.4,-2.7,0,2.7]])
        empty=DashedVMobject(Circle(radius=.95,color=LIGHT,stroke_width=5).move_to([5.4,-.2,0]),num_dashes=16)
        self.add(heading('Only existing neurons can be saved'),c,empty,txt('Existing neurons',-2.7,-1.9,34,LTEAL),txt('Never made',5.4,-1.9,34,WHITE))
        self.at('A survival factor'); self.play(FadeIn(chip('Survival factor',YELLOW,34).move_to([0,2.2,0])),Create(arr([-6,1.3,0],[4.2,1.3,0],YELLOW)),Create(Line([4.45,.9,0],[4.45,1.7,0],color=RED,stroke_width=6)),run_time=.5)
        self.at('never made'); self.play(FadeIn(foot('No neuron exists here to rescue',LTEAL,y=-3.2,size=34)),run_time=.4); self.finish()
class S15Table(TimedScene):
    def construct(self):
        self.add(heading('Ideal allocation model'),foot('Illustrative • no new neurons or immigration'))
        self.at('Take a ganglion'); self.play(FadeIn(chip('N = 1,000 neurons already made',TEAL,34).move_to([0,1.65,0])),run_time=.35)
        self.at('Each needs'); self.play(FadeIn(chip('q = 1 unit per survivor per day',YELLOW,32).move_to([0,.1,0])),run_time=.35)
        self.at('shared supply'); self.play(FadeIn(chip('F (shared supply) = 500 / 1,000 / 3,000 units per day',YELLOW,29).move_to([0,-1.55,0])),run_time=.35); self.finish()
class S16Rows(TimedScene):
    def construct(self):
        self.add(heading('Ideal allocation model'),foot('N = 1,000 • q = 1 unit/day • illustrative',y=-3.2))
        self.add(*[txt(s,x,2.2,29,LIGHT) for s,x in [('Supply / day',-4),('At most survive',0),('Limit',4)]])
        rows=VGroup(*[VGroup(txt(f'{f:,}',-4,y,36,YELLOW),txt(f'{min(1000,f):,}',0,y,36,GREEN),txt(l,4,y,30,TEAL if f>=1000 else YELLOW)) for f,y,l in [(500,1,'Target'),(1000,-.45,'Both'),(3000,-1.9,'Number made')]])
        self.add(rows); highlight=RoundedRectangle(width=11.7,height=1.1,corner_radius=.1,color=YELLOW).move_to([0,1,0])
        self.at('With'); self.play(Create(highlight),run_time=.3)
        self.at('With three'); self.play(highlight.animate.move_to([0,-2.15,0]).set_color(TEAL),run_time=.5); self.finish()
class S17Ceiling(TimedScene):
    def construct(self):
        rule=VGroup(M('S ≤ min(',42),M('N',42,TEAL),M(', floor(',42),M('F/q',42,YELLOW),M('))',42)).arrange(RIGHT,buff=.06).move_to([0,1.65,0])
        self.add(heading('Ideal allocation model'),rule,txt('N: neurons made',-3,.35,30,TEAL),txt('F/q: support available',3,.35,30,YELLOW),txt('F: supply per day',y=-.65,size=29,color=YELLOW),txt('q: units one survivor needs',y=-1.35,size=29,color=YELLOW))
        self.at('smaller of'); self.play(Circumscribe(rule[3],color=YELLOW),run_time=.6)
        self.add(txt('e.g. min(1,000, 500) = 500',y=-2.1,size=30,color=GREEN))
        self.at('budget bound'); self.play(FadeIn(foot('Support-budget bound; not a law for injected NGF dose',y=-3.05,size=27)),run_time=.35); self.finish()
class S18First(TimedScene):
    def construct(self):
        ax=Axes(x_range=[0,3000,1000],y_range=[0,1200,500],x_length=9.7,y_length=5.0,tips=False,axis_config={'color':LIGHT,'include_ticks':False}).move_to([.45,-.1,0])
        cap=DashedLine(ax.c2p(0,1000),ax.c2p(3000,1000),color=TEAL)
        bound=ax.plot(lambda f:min(1000,np.floor(f)),x_range=[0,3000,10],color=YELLOW,use_smoothing=False)
        short=DashedVMobject(ax.plot(lambda f:min(900,np.floor(f/1.5)),x_range=[0,3000,10],color=GREEN,use_smoothing=False),num_dashes=35)
        self.add(heading('S ≤ min(N, floor(F/q))'),ax,cap,txt('Survivors',-6.05,.4,27).rotate(PI/2),txt('N = 1,000',-4.9,2,26,TEAL),foot('Shared supply F (units/day); q = 1',y=-3.5,size=27))
        for f in [500,1000,3000]:self.add(txt(f'{f:,}',*ax.c2p(f,0)[:2]+[0,-.3],size=26))
        self.add(txt('0',*ax.c2p(0,0)[:2]+[-.25,-.3],size=26),txt('500',*ax.c2p(0,500)[:2]+[-.43,0],size=26))
        self.at('Extra factor'); self.play(Create(bound),run_time=.6)
        self.add(txt('F/q: supply limits',1,-.7,27,YELLOW),Line([-.6,-.65,0],ax.c2p(650,650),color=YELLOW),txt('N: number made limits',2.2,2.4,27,TEAL))
        for f in [500,1000,3000]:self.add(dot(ax.c2p(f,min(1000,f)),YELLOW,.07))
        self.add(txt('F/q = 1,000 (units/day)',-2.5,2.6,26,YELLOW),Line([-1.16,2.35,0],ax.c2p(1000,1000),color=LIGHT))
        self.at('Acting as a survival factor'); self.play(Create(short),FadeIn(txt('real survival can fall short',2.1,.8,26,GREEN)),FadeIn(txt('(illustrative)',2.7,.3,26,GREEN)),run_time=.6); self.finish()
class S19Puzzle(TimedScene):
    def construct(self):
        g,c=sharing(); self.add(g[0],g[1],g[3],g[4],g[5])
        self.at('Spread those'); self.play(Create(g[2]),*[Indicate(d,color=YELLOW,scale_factor=1.07) for d in c],run_time=.8); self.finish()
class S20Predict(TimedScene):
    def construct(self):
        g,c=sharing(True); self.add(g); self.at('Predict'); self.play(Indicate(g[0],scale_factor=1.025),run_time=.5); self.finish()
class S21Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; g,_=sharing(True); self.add(g); countdown(self,5,(5.9,2.6))
class S22Reveal(TimedScene):
    def construct(self):
        g,c=sharing(True); self.add(g)
        self.at('It depends'); self.play(Transform(g[0],txt('It depends',y=3.45,size=34)),FadeOut(g[-1]),run_time=.35)
        for d in c: d.save_state()
        events=[('equally short','Every neuron is equally short',LIGHT),('all are at risk','All are at risk together',RED)]; cur=None
        while self.narration_s-self.elapsed()>1.3:
            self.play(*[d.animate.set_opacity(.3) for d in c],run_time=.5)
            extra=[]
            if events and self.elapsed()>self.t_of(events[0][0])-.3:
                e=events.pop(0); new=foot(e[1],e[2],y=-3.5,size=34)
                if cur is None: cur=new; extra=[FadeIn(cur)]
                else: extra=[Transform(cur,new)]
            self.play(*[Restore(d) for d in c],*extra,run_time=.5)
        self.finish()
class S23Model(TimedScene):
    def construct(self):
        xs=[-5.2,-2.6,0,2.6,5.2]
        c=VGroup(*[dot([x,-.8,0],BLUE,.9,.8) for x in xs])
        supply=chip('Continuing supply',YELLOW,34).move_to([0,2.35,0]); streams=VGroup(*[arr([0,1.9,0],d.get_top(),YELLOW) for d in c])
        self.add(heading('Sharing after a death'),c,supply,streams,foot('Schematic • assumes supply can be redirected',y=-3.3,size=27))
        self.at('Each death'); self.play(state(c[1],RED,.08),FadeOut(streams[1]),run_time=.9)
        ps=VGroup(*[dot(c[1].get_top(),YELLOW,.18) for _ in range(2)]); self.add(ps)
        self.play(ps[0].animate.move_to(c[0].get_top()),ps[1].animate.move_to(c[2].get_top()),state(c[0],GREEN),state(c[2],GREEN),run_time=.7); self.remove(*ps,ps)
        self.at('already committed')
        stub=arr([0,1.9,0],[1.95,.7,0],YELLOW); block_bar=Line([1.7,.38,0],[2.3,1.06,0],color=RED,stroke_width=10)
        self.play(state(c[3],RED,.3),FadeOut(streams[3]),FadeIn(stub),FadeIn(block_bar),FadeIn(chip('LOCK: committed',RED,30).move_to([2.6,-2.4,0])),run_time=.4)
        self.at('cannot use it'); p=dot([2.0,1.3,0],YELLOW,.2); self.add(p)
        self.play(p.animate.move_to([4.0,1.3,0]),Create(arr([2.3,1.3,0],[4.0,1.3,0],YELLOW)),run_time=.4); self.play(p.animate.move_to(c[4].get_top()),state(c[4],GREEN),run_time=.4); self.remove(p); self.finish()
class S23Model2(TimedScene):
    def construct(self):
        g,c=timing_frame(); neutral=c.copy().set_stroke(BLUE).set_fill(BLUE,opacity=.5); self.add(g[:2],neutral)
        self.at('Slow commitment'); self.play(Transform(neutral,c),FadeIn(g[3:]),run_time=.5); self.finish()
class S23Model3(TimedScene):
    def construct(self):
        g,c=timing_frame(); new,_=timing_frame(True); self.add(g)
        self.at('Fast commitment'); self.play(Transform(g,new),run_time=.7)
        self.at('Equal sharing alone'); self.play(Transform(g[-1],foot('Equal sharing alone does not say how many survive.',y=-3.55)),run_time=.4); self.finish()
class S24Beat(Scene):
    def construct(self): self.camera.background_color=BG; self.add(timing_frame(True,True)[0]); self.wait(3)
class S25Win(TimedScene):
    def construct(self):
        c=cells(color=YELLOW,op=.5).scale(1.2); self.add(heading('When supply is short'),c)
        self.at('When supply'); self.play(*[state(c[i],GREEN) for i in [0,2,4]],*[state(c[i],RED,.12) for i in [1,3,5]],run_time=.65)
        self.at('factor ends up'); self.play(FadeIn(foot('Factor ends up with some neurons',YELLOW)),run_time=.3); self.finish()
class S25Win2(TimedScene):
    def construct(self):
        a=cells((-3.2,0)).scale(.72); b=cells((3.2,0)).scale(.72)
        self.add(heading('Same result, two routes'),a,b,txt('Slow random loss',-3.2,-2.3,29),txt('Early competition',3.2,-2.3,29))
        self.at('Slow random'); self.play(*[state(a[i],GREEN) for i in [0,2,4]],*[state(a[i],RED,.12) for i in [1,3,5]],run_time=.6)
        self.at('Competition that'); self.play(*[state(b[i],GREEN) for i in [0,2,4]],*[state(b[i],RED,.12) for i in [1,3,5]],run_time=.6); self.finish()
class S26Model(TimedScene):
    def construct(self):
        g,a,b=competition(False); self.add(g)
        self.at('evidence supports'); self.play(FadeIn(foot('Active competition • a supported model',size=32,y=-3.0)),run_time=.35); self.finish()
class S27Trka(TimedScene):
    def construct(self):
        g,a,b=competition(False); r=receptors(); nchip=chip('NGF',YELLOW,36).move_to([0,2.3,0]); self.add(g,nchip)
        start=nchip.get_bottom()
        def fly(pts,run=.8,extra=()):
            ps=VGroup(*[dot(start,YELLOW,.2,.95) for _ in pts]); self.add(ps)
            self.play(AnimationGroup(*[p.animate.move_to(t) for p,t in zip(ps,pts)],lag_ratio=.15),*extra,run_time=run); self.remove(*ps,ps)
        rim=lambda C,deg: C+RC*np.array([np.cos(deg*DEGREES),np.sin(deg*DEGREES),0])
        self.at('raises its own'); fly([rim(LC,105),rim(LC,135),rim(RN,80),rim(RN,50)],.9)
        self.at('receptor'); self.play(FadeIn(r[0]),run_time=.3)
        self.at('track A'); self.play(FadeIn(txt('TrkA',-5.8,2.15,32,PURPLE)),Create(Line([-5.35,1.9,0],r[0].get_center()+LEFT*.1,color=PURPLE)),run_time=.3)
        self.at('gets a little more'); fly([r[0].get_center(),r[1].get_center()],.6,[state(a,GREEN,.5)])
        self.play(FadeIn(r[1:3]),run_time=.3)
        self.at('take up'); fb=foot('more NGF → more TrkA → more uptake',YELLOW,y=-3.0,size=34)
        self.play(FadeIn(r[3:]),FadeIn(fb),run_time=.3)
        fly([r[i].get_center() for i in range(6)],.9,[state(a,GREEN)]); self.finish()
class S28Bdnf(TimedScene):
    def construct(self):
        g,a,b=competition(); self.add(g)
        self.at('release two related'); self.play(Create(arr([-1.75,.3,0],[1.75,.3,0],RED)),Create(arr([-1.75,-.75,0],[1.75,-.75,0],RED)),run_time=.4)
        self.at('factors',lead=-.4); self.play(FadeIn(txt('BDNF',0,.8,30,RED)),run_time=.25)
        self.at('and'); self.play(FadeIn(txt('NT-4',0,-1.25,30,RED)),run_time=.25)
        self.at('another receptor'); r,lab,ld=p75_parts(); self.play(FadeIn(r),FadeIn(lab),Create(ld),run_time=.3); self.finish()
class S29Push(TimedScene):
    def construct(self):
        g,a,b=competition(); r,lab,ld=p75_parts(); self.add(g,arr([-1.75,-.25,0],[1.75,-.25,0],RED),txt('BDNF + NT-4',0,.3,28,RED),r,lab,ld)
        self.at('toward death'); self.play(state(b,RED,.12),Create(Cross(b,stroke_color=RED,stroke_width=4)),run_time=.6)
        self.at('Winners are'); self.play(FadeIn(txt('Winners amplified',-3.4,-2.95,30,GREEN)),run_time=.3)
        self.at('losers are'); self.play(FadeIn(txt('Losers punished',3.4,-2.95,30,RED)),FadeIn(foot('Deppmann and colleagues, 2008',GOLD,y=-3.62,size=28)),run_time=.3); self.finish()
class S30Motor(TimedScene):
    def construct(self):
        self.add(heading('The population matters'))
        panels=VGroup(*[RoundedRectangle(width=6.0,height=5.4,corner_radius=.2,color=LIGHT).move_to([x,-.2,0]) for x in [-3.3,3.3]])
        ptxt=txt('Limb motor neurons (chick)',3.3,2.05,30)
        panels[1].set_stroke(opacity=.3); ptxt.set_opacity(.3)
        self.add(panels[0],panels[1],ptxt,txt('Sympathetic neurons',-3.3,2.05,30))
        self.add(DashedLine([-6.1,1.15,0],[-.5,1.15,0],color=LTEAL),txt('Cohort ceiling',-3.3,1.55,28,LTEAL))
        neuron=dot([-5.0,-1.0,0],BLUE,.85,.5)
        lock=chip('TrkA',PURPLE,30).move_to([-3.2,-1.1,0]); slot=Rectangle(width=.36,height=.22,color=PURPLE,fill_color=BG,fill_opacity=1).move_to(lock.get_top()+DOWN*.05)
        key=chip('NGF',YELLOW,30).move_to([-3.2,.3,0]); teeth=Rectangle(width=.28,height=.28,color=YELLOW,fill_color=YELLOW,fill_opacity=.9).move_to(key.get_bottom()+DOWN*.12); key.add(teeth)
        self.add(neuron,lock,slot,key)
        self.at('population measured'); self.play(key.animate.shift(DOWN*.6),run_time=.5); self.add(foot('The ceiling holds only for the population measured.',LTEAL,y=-3.4,size=30))
        self.at('Limb motor neurons'); motor=dot([4.9,-.3,0],BLUE,.85,.7); ngf=chip('NGF',YELLOW,30).move_to([2.2,-.3,0]); ngf.add(Rectangle(width=.28,height=.28,color=YELLOW,fill_color=YELLOW,fill_opacity=.9).next_to(ngf,RIGHT,buff=0))
        other=txt('Other factors each reduce\npart of the death',3.3,-1.95,28,LIGHT)
        self.play(panels[1].animate.set_stroke(opacity=1),ptxt.animate.set_opacity(1),FadeIn(motor),FadeIn(ngf),FadeIn(other),run_time=.4)
        self.at('do not depend'); self.play(Create(Line([3.55,-.9,0],[3.55,.3,0],color=RED,stroke_width=7)),FadeIn(txt('Not NGF-dependent',3.3,1.0,30)),run_time=.4); self.finish()
class S31Take(TimedScene):
    def construct(self):
        c=VGroup(*[dot([x,-.55,0],BLUE,.65,.4) for x in [-4.8,-2.4,0,2.4,4.8]])
        self.add(heading('Extra NGF saves neurons'),c,DashedLine([-5.8,1.45,0],[5.8,1.45,0],color=TEAL),txt('Number made: the ceiling',y=2.05,size=30,color=TEAL))
        self.at('extra'); self.play(*[c[i].animate.set_fill(GREEN,opacity=.85).set_stroke(GREEN).shift(UP*1.1) for i in [0,2,4]],*[state(c[i],RED,.12) for i in [1,3]],run_time=.6)
        self.at('never more'); self.play(FadeIn(txt('Never more than were made',y=-2.05,size=34,color=TEAL)),run_time=.35)
        self.at('how the factor'); self.play(FadeIn(foot('Sharing decides how many',YELLOW,size=32)),run_time=.35); self.finish()
class S32End(EndCard):
    LINE='Extra NGF saves neurons, never more than were made. Sharing decides how many.'
    def construct(self):
        line=T('Extra NGF saves neurons,\nnever more than were made.\nSharing decides how many.',38,font=TITLE_FONT,line_spacing=1.25)
        self.add(line,foot('biochemistrypedia.com',TEAL,y=-2.5)); self.finish()
