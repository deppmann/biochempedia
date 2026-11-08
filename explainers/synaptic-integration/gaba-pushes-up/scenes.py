"""When GABA Pushes Up — chapter 5, review revision.
COLOR MAP: BLUE neuron/chloride compartment; GREEN excitation; RED GABA;
GREY leak, ghosts and structure; YELLOW Vm; TEAL threshold.
All voltage traces solve C*dV/dt=gL(EL-V)+gE(EE-V)+gG(EG-V).
Study spike marks are explicitly qualitative symbols, not measured traces.
"""
import numpy as np
from bp_style import *
from bp_style import SpokenScene as BaseSpokenScene

EL, EG, EE, THR, C = -65., -55., 0., -50., 200.

def vss(gl=10, ge=0, gg=10):
    return (gl*EL+ge*EE+gg*EG)/(gl+ge+gg)

def step(t, start=EL, ge=0, gg=10):
    end=vss(10,ge,gg)
    return end+(start-end)*np.exp(-np.asarray(t)*(10+ge+gg)/C)

def model(gg=0, start=EL, onset=0, duration=45, gfun=None, efun=None):
    ts=np.arange(0,duration+.01,.01); vs=np.empty(len(ts)); vs[0]=start
    def f(t,v):
        u=max(0,t-onset); ge=(19*u*np.exp(1-u) if t>=onset else 0) if efun is None else efun(t)
        gi=gg if gfun is None else gfun(t)
        return (10*(EL-v)+ge*(EE-v)+gi*(EG-v))/C
    for i,t in enumerate(ts[:-1]):
        v=vs[i]; h=.01
        a=f(t,v); b=f(t+h/2,v+h*a/2); c=f(t+h/2,v+h*b/2); d=f(t+h,v+h*c)
        vs[i+1]=v+h*(a+2*b+2*c+d)/6
    return ts,vs

FAST0=model(); FASTG=model(10,-60)
# A separate illustrative pulse for the timing comparison: same excitation in both cases.
# GABA coincident: 30 nS during the 20 ms pulse. Earlier GABA is closed before the pulse.
PULSE=lambda t:4.5 if t<20 else 0
COMPARE0=model(efun=PULSE)
COINC=model(gfun=lambda t:30 if t<20 else 0,efun=PULSE)
COMPAREG=model(start=-60,efun=PULSE)

class SpokenScene(BaseSpokenScene):
    # Keep the immutable audio schedule; no per-scene 0.4-second drift or extra log file.
    def at(self,phrase,lead=.2,nth=0):
        rest=self.t_of(phrase,nth)-lead-self.elapsed()
        if rest>.02:self.wait(rest)
    def finish(self):
        rest=self.narration_s-self.elapsed()
        if rest>0:self.wait(rest)

def label(s,x=0,y=3.3,size=30,color=TEXT):
    return T(s,size,color).move_to([x,y,0])
def head(s):return label(s)
def foot(s,color=TEXT):return label(s,0,-3.45,26,color)
def backed(s,x,y,size=26,color=TEXT):
    t=label(s,x,y,size,color)
    return VGroup(BackgroundRectangle(t,color=BG,fill_opacity=.95,buff=.09),t).set_z_index(10)
def xv(v):return -5.7+(v+68)*11.4/20

def hgap(r,y=1.95,col=TEAL):
    return always_redraw(lambda:VGroup(Line([xv(r.v.get_value()),y,0],[xv(THR),y,0],color=col),Line([xv(r.v.get_value()),y-.12,0],[xv(r.v.get_value()),y+.12,0],color=col),Line([xv(THR),y-.12,0],[xv(THR),y+.12,0],color=col)))

class Rail:
    def __init__(self,v=-65,eg=-55):
        self.v=ValueTracker(v);self.eg=ValueTracker(eg)
        self.axis=VGroup(Line([-5.7,.5,0],[5.7,.5,0],color=GREY,stroke_width=3))
        for val in [-65,-60,-55,-50]:
            self.axis.add(Line([xv(val),.38,0],[xv(val),.65,0],color=GREY),label(str(val).replace('-','−'),xv(val),1.05,28,GREY))
        self.axis.add(label('mV',6.12,1.05,26,GREY))
        self.th=VGroup(DashedLine([xv(THR),1.4,0],[xv(THR),2.5,0],color=TEAL),label('threshold',4.5,2.8,26,TEAL))
        self.dot=always_redraw(lambda:Dot([xv(self.v.get_value()),.5,0],radius=.18,color=YELLOW).set_z_index(5))
        self.vm=always_redraw(lambda:backed('Vm',xv(self.v.get_value()),.02,26,YELLOW))
        self.base=VGroup(self.axis,self.th,self.dot,self.vm)
        self.leak=VGroup(always_redraw(lambda:Line([xv(self.v.get_value()),.5,0],[xv(-65),-1.45,0],color=GREY,stroke_width=6)),Dot([xv(-65),-1.45,0],color=GREY),label('Leak: 10 nS',-4,-2.05,28,GREY),label('E = −65 mV',-4,-2.65,26,GREY))
        self.rope=always_redraw(lambda:VGroup(Line([xv(self.v.get_value()),.5,0],[xv(self.eg.get_value()),-1.45,0],color=RED,stroke_width=7),Dot([xv(self.eg.get_value()),-1.45,0],radius=.15,color=RED)))
        self.glab=label('GABA: 10 nS',1.8,-2.05,28,RED)
        self.elab=label('E_GABA = −55 mV',1.8,-2.65,26,RED)
        self.gaba=VGroup(self.rope,self.glab,self.elab)
    def excitation(self):
        return VGroup(Arrow([xv(self.v.get_value()),1.75,0],[5.5,1.75,0],color=GREEN,buff=.04,stroke_width=7),label('excitation: E = 0 mV, pulls up',-.8,2.4,26,GREEN))
    def zones(self):
        return VGroup(*[Rectangle(width=b-a,height=2.3,stroke_width=0,fill_color=col,fill_opacity=.12).move_to([(a+b)/2,.45,0]).set_z_index(-3) for a,b,col in [(-5.7,xv(-55),RED),(xv(-55),5.7,BLUE)]],VGroup(DashedLine([xv(-55),-1,0],[xv(-55),.3,0],color=RED),DashedLine([xv(-55),1.35,0],[xv(-55),1.65,0],color=RED)))

class Plot:
    def __init__(self,box=(-5.35,5.7,-2.05,2.4),duration=45,lo=-66,hi=-48,threshold=True,numeric=True,compact=False):
        self.x0,self.x1,self.y0,self.y1=box;self.duration=duration;self.lo=lo;self.hi=hi
        self.axes=VGroup(Line(self.p(0,lo),self.p(duration,lo),color=GREY),Line(self.p(0,lo),self.p(0,hi),color=GREY),label('Vm (mV)',self.x0+.6,self.y1+.42,26,YELLOW),label('time (ms)',(self.x0+self.x1)/2,self.y0-.88,26,GREY))
        vals=[-65,-60,-55] if lo<-60 else [-56,-54,-52,-50,-48]
        if numeric:
            for val in vals:
                if lo<=val<=hi:self.axes.add(label(str(val).replace('-','−'),self.x0-.5,self.p(0,val)[1],26,GREY))
        for t in range(0,int(duration)+1,10):
            self.axes.add(Line(self.p(t,lo),self.p(t,lo)+DOWN*.1,color=GREY),label(str(t),self.p(t,lo)[0],self.y0-.37,26,GREY))
        self.th=VGroup(DashedLine(self.p(0,THR),self.p(duration,THR),color=TEAL),backed('−50 threshold',self.x1-1.4,self.p(0,THR)[1]+.25,26,TEAL)) if threshold else VGroup()
    def p(self,t,v):return np.array([self.x0+(self.x1-self.x0)*t/self.duration,self.y0+(self.y1-self.y0)*(v-self.lo)/(self.hi-self.lo),0])
    def curve(self,t,v,color=YELLOW,opacity=1):
        # Intersect line segments with the plot bounds; never turn clipped values into a fake plateau.
        stride=max(1,len(t)//800);ts=t[::stride];vs=v[::stride]
        curve=VMobject(color=color,stroke_width=4,stroke_opacity=opacity)
        previous=None
        for ta,tb,va,vb in zip(ts[:-1],ts[1:],vs[:-1],vs[1:]):
            low,high=0.,1.
            for a,b,mn,mx in [(ta,tb,0,self.duration),(va,vb,self.lo,self.hi)]:
                if abs(b-a)<1e-12:
                    if not mn<=a<=mx:low,high=1.,0.
                else:
                    u,w=sorted(((mn-a)/(b-a),(mx-a)/(b-a)));low=max(low,u);high=min(high,w)
            if low>high:previous=None;continue
            aa=self.p(ta+(tb-ta)*low,va+(vb-va)*low);bb=self.p(ta+(tb-ta)*high,va+(vb-va)*high)
            if previous is None or np.linalg.norm(previous-aa)>1e-5:curve.start_new_path(aa)
            curve.add_line_to(bb);previous=bb
        return curve
    def peak(self,data,col,text,offset):
        t,v=data;i=np.argmax(v);point=self.p(t[i],v[i]);anchor=point+np.array(offset)
        return VGroup(Dot(point,radius=.07,color=col),Line(point,anchor,color=col),backed(text,anchor[0],anchor[1],26,col))

def bracket(p,t,low,high,text,col,dx=.9):
    a=p.p(t,low);b=p.p(t,high)
    return VGroup(Line(a,b,color=col,stroke_width=3),Line(a+LEFT*.12,a+RIGHT*.12,color=col),Line(b+LEFT*.12,b+RIGHT*.12,color=col),backed(text,a[0]+dx,(a[1]+b[1])/2,26,col))

def queued():
    return VGroup(Arrow([-.8,2.05,0],[2.7,2.05,0],color=GREEN,buff=.05),label('excitation arrives in a few ms',-.6,2.65,26,GREEN))

def prediction(n):
    r=Rail(-65 if n==1 else (-52 if n==2 else float(step(4,-60,gg=0))))
    question={1:'Where does the marker settle?',2:'Which way does the GABA rope pull?',3:'Nearer threshold or farther?'}[n]
    g=VGroup(r.base,r.leak,head(question),foot('Pause',TEAL))
    if n!=3:g.add(r.gaba)
    if n==2:g.add(r.excitation())
    if n==3:g.add(queued(),hgap(r,1.55))
    return r,g

class S00Title(TitleCard):
    TITLE='When GABA Pushes Up'; LESSON='Integration, Inhibition and Neuromodulation'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,26,GREY),T(self.TITLE,54,font=TITLE_FONT),Line(LEFT*1.2,RIGHT*1.2,color=GOLD)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.6);self.wait(max(.01,self.narration_s-self.renderer.time))

class S01Question(SpokenScene):
    def construct(self):
        self.add(label('Can one GABA input hold back excitation,',0,3.4,30),label('and then help it a few milliseconds later?',0,2.88,30))
        p=Plot(box=(-5.35,-.65,-2.05,1.85),duration=40);q=Plot(box=(1.1,5.8,-2.05,1.85),duration=40)
        p.th[1].move_to([-2.05,2.27,0]);q.th[1].move_to([4.4,2.27,0])
        self.add(p.axes,q.axes,p.th,q.th,p.curve(*COMPARE0,GREY,.7),q.curve(*COMPARE0,GREY,.7),label('Illustrative 20 ms input',0,-2.98,26,GREY),foot('Grey: EPSP alone   ·   yellow: with GABA',GREY))
        self.at('hold back excitation');self.play(Create(p.curve(*COINC)),FadeIn(backed('GABA coincident',-2.9,-1.4,26,RED)),run_time=.6)
        self.at('then help it');self.play(Create(q.curve(*COMPAREG)),FadeIn(backed('GABA earlier',3.5,-1.4,26,RED)),run_time=.6);self.finish()

class S02Moves(SpokenScene):
    def construct(self):
        r=Rail(eg=-65);peglabel=label('GABA rope: E = −65 mV (the shunt)',-2,-2.15,28,RED);self.add(r.base,r.rope,head('The rope’s end can move'),peglabel)
        gradient=ValueTracker(0)
        def gradient_icon():
            x=xv(r.eg.get_value())+1.5;u=gradient.get_value()
            return VGroup(Rectangle(width=.55,height=1.1-.4*u,color=BLUE,fill_opacity=.65).move_to([x-.6,-1.9,0]),Rectangle(width=.55,height=.35+.42*u,color=BLUE,fill_opacity=.65).move_to([x+.6,-1.9,0]),label('Cl− outside',x-.7,-2.75,26,BLUE),label('inside',x+.95,-2.75,26,BLUE),label('chloride gradient',x,-3.35,28,BLUE))
        icon=always_redraw(gradient_icon)
        self.at('tied exactly at rest');self.play(Indicate(r.rope,color=RED),run_time=.4)
        self.at('depends on the chloride gradient');self.play(FadeOut(peglabel),FadeIn(icon),run_time=.3)
        self.play(gradient.animate.set_value(1),r.eg.animate.set_value(-55),run_time=1.3);self.finish()

class S03Between(SpokenScene):
    def construct(self):
        r=Rail();self.add(r.base,r.rope,head('Above rest. Below threshold.'))
        self.at('Suppose it is tied');self.play(FadeIn(r.elab),run_time=.4)
        self.at('above rest');self.play(FadeIn(label('rest: −65 mV',-4,-2.25,28,GREY)),run_time=.4)
        self.at('below threshold');self.play(Indicate(r.th,color=TEAL),run_time=.5);self.finish()

class S04Predict1(SpokenScene):
    def construct(self):
        r,g=prediction(1);self.add(r.base,r.leak,head('Where does the marker settle?'),foot('Pause',TEAL))
        self.at('rope opens');self.play(FadeIn(r.gaba),run_time=.6);self.finish()

class Countdown(Scene):
    CASE=1
    def __init__(self,*args,**kwargs):
        config.background_color=BG
        super().__init__(*args,**kwargs)
    def construct(self):
        config.background_color=BG;r,g=prediction(self.CASE);self.add(g)
        # A progress line below Pause, with an explicit duration.
        self.add(label('5 seconds',4.7,-3.45,26,GREY))
        bar=Line([-1.7,-3.75,0],[1.7,-3.75,0],color=TEAL,stroke_width=5)
        self.add(bar);self.play(bar.animate.stretch(.001,0,about_edge=LEFT),run_time=5,rate_func=linear)
class S05Pause(Countdown):CASE=1
class S08Pause(Countdown):CASE=2
class S11Pause(Countdown):CASE=3

class S06Reveal1(SpokenScene):
    def construct(self):
        r=Rail();title=head('Equal conductances → halfway');self.add(r.base,r.leak,r.gaba,title)
        self.at('at minus');self.play(r.v.animate.set_value(vss()),run_time=.85)
        p=Plot(duration=60,lo=-66,hi=-53,threshold=False);t=np.linspace(0,60,601)
        plot=VGroup(p.axes,head('GABA depolarizes: −65 to −60 mV'),DashedLine(p.p(0,EG),p.p(60,EG),color=RED),backed('E_GABA = −55 mV',3.6,p.p(0,EG)[1]+.3,26,RED))
        self.at('This');self.play(*[FadeOut(m) for m in list(self.mobjects)],FadeIn(plot),run_time=.35)
        self.play(Create(p.curve(t,step(t))),run_time=.8);self.finish()

class S07Predict2(SpokenScene):
    def construct(self):
        r=Rail(-60);self.add(r.base,r.leak,r.gaba,head('Which way does the GABA rope pull?'),foot('Pause',TEAL))
        self.at('strong excitation');self.play(FadeIn(r.excitation()),run_time=.4)
        self.play(r.v.animate.set_value(-52),run_time=1.1);self.finish()

class S09Reveal2(SpokenScene):
    def construct(self):
        r=Rail(-52);self.add(r.base,r.leak,r.rope,Line([xv(-52),.5,0],[5.5,1.75,0],color=GREEN,stroke_width=5),r.excitation(),label('GABA: 10 nS',3.7,-1.45,28,RED),head('GABA opposes further depolarization'))
        # Keep all three pulls; the red direction alone changes.
        self.at('Down');a=Arrow([xv(-52)+.42,.5,0],[xv(-55)+.42,-1.45,0],color=RED,buff=.12,stroke_width=7);self.play(GrowArrow(a),run_time=.45)
        self.at('conductance enlarges')
        self.remove(r.leak[2],r.leak[3])
        def subterm(base,sub,color=TEXT):
            term=T(base,27,color);subscript=T(sub,22,color).next_to(term,RIGHT,buff=.015).align_to(term,DOWN).shift(DOWN*.10)
            return VGroup(term,subscript)
        numerator=VGroup(subterm('g','L'),T('·',27),subterm('E','L'),T('+',27),subterm('g','E'),T('·',27),subterm('E','E'),T('+',27),subterm('g','GABA',RED),T('·',27),subterm('E','GABA',RED)).arrange(RIGHT,buff=.09).move_to([0,-2.15,0])
        den=VGroup(subterm('g','L'),T('+',27),subterm('g','E'),T('+',27),subterm('g','GABA',RED)).arrange(RIGHT,buff=.15).move_to([0,-3.0,0])
        frac=VGroup(numerator,Line([-3.8,-2.6,0],[3.8,-2.6,0],color=TEXT),den,label('V∞ =',-5,-2.6,28,YELLOW))
        self.play(FadeIn(frac),run_time=.6);self.finish()

class S10Predict3(SpokenScene):
    def construct(self):
        r=Rail(-60);self.add(r.base,r.leak,r.gaba,head('Nearer threshold or farther?'),foot('Pause',TEAL),hgap(r,1.55))
        self.at('conductance closes');self.play(FadeOut(r.gaba),run_time=.6)
        self.at('arrives a few');self.play(FadeIn(queued()),r.v.animate.set_value(float(step(4,-60,gg=0))),run_time=.9);self.finish()

class S12Reveal3(SpokenScene):
    def construct(self):
        p=Plot();t,v=model(0,-60,onset=6);u,w=model(0,-65,onset=6);tail=step(t,-60,gg=0)
        self.add(p.axes,p.th,p.curve(t,tail,YELLOW,.6),foot('GABA closes at 0 ms · residual voltage decays: τ = 20 ms',YELLOW))
        self.at('Nearer');self.play(FadeIn(head('Nearer threshold')),run_time=.3)
        close=VGroup(Line(p.p(0,-60)+UP*.15,p.p(0,-60)+UP*.65,color=RED))
        self.add(close)
        self.play(Create(p.curve(u,w,GREY)),Create(p.curve(t,v)),run_time=.5)
        start=float(step(6,-60,gg=0))
        self.add(Dot(p.p(6,-65),color=GREY),Dot(p.p(6,start),color=YELLOW),bracket(p,6,-65,start,'head start',YELLOW,-1.1),label('EPSP on the tail',3,1.55,26,YELLOW),label('EPSP from rest (ghost)',3,.95,26,GREY));self.finish()


class S13Rule(SpokenScene):
    def construct(self):
        r=Rail(-63);self.add(r.base,r.rope,head('An open synapse pulls Vm toward its reversal potential'),label('E (reversal potential)',1.8,-2.15,30,RED))
        a=Arrow([xv(-63),1.9,0],[xv(-55),1.9,0],color=RED,buff=.05,stroke_width=7)
        self.at('an open synapse');self.play(GrowArrow(a),r.v.animate.set_value(-58),run_time=1);self.finish()

class S14HelpHurt(SpokenScene):
    def construct(self):
        r=Rail(-62);self.add(r.zones(),r.base,r.rope,r.elab)
        title=head('Below −55 mV: depolarizing GABA current');self.add(title)
        a=Arrow([xv(-62),1.9,0],[xv(-55),1.9,0],color=RED,buff=.05)
        self.at('depolarizes while');self.play(GrowArrow(a),run_time=.5)
        self.at('It hyperpolarizes');self.play(FadeOut(a),Transform(title,head('Above −55 mV: hyperpolarizing GABA current')),r.v.animate.set_value(-52),run_time=.7)
        self.play(GrowArrow(Arrow([xv(-52),1.9,0],[xv(-55),1.9,0],color=RED,buff=.05)),run_time=.4);self.finish()

class S14bFiring(SpokenScene):
    def construct(self):
        p=Plot();a=p.curve(*COMPARE0,GREY);b=p.curve(*COINC)
        p.axes[3].become(label('time (ms) · illustrative 20 ms input',.175,-2.93,24,GREY))
        self.add(p.axes,p.th,a,head('Judge by the whole response'))
        legend=VGroup(T('without GABA',26,GREY),T('with GABA',26,YELLOW)).arrange(RIGHT,buff=.6).move_to([0,-3.45,0]);self.add(legend)
        cap=backed('GABA coincident: smaller response',1.8,2.82,28,RED)
        self.at('Current direction alone');self.play(Create(b),FadeIn(cap),run_time=.6)
        self.at('compare the whole response');self.play(Transform(b,p.curve(*COMPAREG)),Transform(cap,backed('GABA earlier: closer to threshold',1.8,2.82,28,RED)),run_time=.8)
        self.add(backed('Earlier GABA closed before EPSP',2.4,-1.25,26,RED));self.finish()

class S15Steady(SpokenScene):
    def construct(self):
        old=vss(10,2.3,0);new=vss(10,2.3,10);r=Rail(old)
        ghost=Dot([xv(old),1.05,0],radius=.22,color=GREY)
        ghost_stem=DashedLine([xv(old),.52,0],[xv(old),.83,0],color=GREY,stroke_width=1.5)
        ex=r.excitation();self.add(r.base,r.leak,r.rope,r.elab,ex,head('Steady inputs: the balance stays below threshold'),foot('New balance stays between the old balance and E_GABA'))
        tag=backed('balance without GABA',-2.3,1.9,26,GREY)
        self.add(ghost,ghost_stem,DashedLine(ghost.get_center(),[-2.3,1.7,0],color=TEAL,stroke_width=1.5),tag,hgap(r,1.5),label('−55 mV limit',1.8,-2.05,28,RED))
        self.at('new balance point');self.play(r.v.animate.set_value(new),run_time=1.2);self.finish()

class S16Fast(SpokenScene):
    def construct(self):
        p=Plot();self.add(p.axes,p.th,head('Brief inputs are different'),foot('Model of this lesson’s cell',GREY))
        self.at('Brief inputs');self.play(Create(p.curve(*FAST0)),run_time=.7)
        t,v=FAST0;i=np.argmax(v)
        self.at('stopped just short');self.add(bracket(p,t[i],v[i],THR,'just short',TEAL,1.2),backed('EPSP alone',1.8,-1.15,26,YELLOW));self.finish()

class S17Fast2(SpokenScene):
    def construct(self):
        p=Plot(box=(-5.35,5.7,-2.05,0));self.add(p.axes,p.th,p.curve(*FAST0,GREY),head('GABA already open: peak zoom (first 10 ms)'))
        z=Plot(box=(-4.4,-1,1.1,2.5),duration=10,lo=-53.5,hi=-49.5,threshold=False)
        za=VGroup(Rectangle(width=3.4,height=1.4,color=GREY,stroke_width=1).move_to([-2.7,1.8,0]),DashedLine(z.p(0,THR),z.p(10,THR),color=TEAL))
        for val in [-53,-52,-51,-50]:za.add(label(str(val).replace('-','−'),-4.95,z.p(0,val)[1],24,GREY))
        for tm in [0,5,10]:za.add(Line(z.p(tm,z.lo),z.p(tm,z.lo)+DOWN*.08,color=GREY),label(str(tm),z.p(tm,z.lo)[0],.82,22,GREY))
        za.add(label('ms',-.5,.82,22,GREY))
        def peak_dot(data,col):
            t,v=data;i=np.argmax(v);return Dot(z.p(t[i],v[i]),radius=.055,color=col)
        grey_dot=peak_dot(FAST0,GREY)
        self.add(za,z.curve(*FAST0,GREY),grey_dot,Line(grey_dot.get_center(),[-.55,grey_dot.get_y(),0],color=GREY,stroke_width=1.5),label('alone: −52.7 mV',1,1.37,24,GREY),foot('Same passive model; GABA remains open',GREY))
        self.at('conductance already open');self.play(Create(p.curve(*FASTG)),Create(z.curve(*FASTG,YELLOW)),run_time=.7)
        yellow_dot=peak_dot(FASTG,YELLOW)
        self.add(yellow_dot,Line(yellow_dot.get_center(),[-1.15,yellow_dot.get_y(),0],color=YELLOW,stroke_width=1.5),label('GABA open: −49.9 mV',.8,2.35,24,YELLOW),label('GABA still open → −60 mV',3.4,-2.98,24,RED))
        # A second, explicitly scaled zoom makes the tiny crossing visible.
        self.at('just crossed')
        m=Plot(box=(3.6,6.2,1.25,2.4),duration=2,lo=-50.08,hi=-49.9,threshold=False)
        t,v=FASTG;mask=(t>=3)&(t<=5)
        self.add(Rectangle(width=2.6,height=1.15,color=GREY,stroke_width=1).move_to([4.9,1.825,0]),DashedLine(m.p(0,THR),m.p(2,THR),color=TEAL),m.curve(t[mask]-3,v[mask]),label('−50',3.2,m.p(0,THR)[1],22,TEAL),label('3–5 ms · zoom',4.9,.87,22,GREY),label('Crossing: +0.061 mV',4.65,2.85,24,TEAL));self.finish()

class S18Fast3(SpokenScene):
    def construct(self):
        p=Plot(box=(-5.35,5.7,-2.05,.85));self.add(p.axes,p.th,p.curve(*FAST0,GREY),p.curve(*FASTG),head('Smaller EPSP; a 5 mV head start'),foot('gE peaks at 1 ms; Vm peaks at 4–5 ms',GREEN))
        # The conductance panel shares exactly the Vm time transform.
        gy=1.65;gh=.9;t=np.linspace(0,45,901);ge=19*t*np.exp(1-t)
        gp=VMobject(color=GREEN,stroke_width=4).set_points_as_corners([[p.p(x,EL)[0],gy+y/19*gh,0] for x,y in zip(t,ge)])
        panel=VGroup(Line([p.x0,gy,0],[p.x1,gy,0],color=GREY),Line([p.x0,gy,0],[p.x0,gy+gh,0],color=GREY),label('gE (nS)',-4.4,2.85,26,GREEN),label('19',-5.9,2.55,26,GREEN),gp,label('1 ms',-3.9,2.4,26,GREEN))
        self.add(panel,Dot([p.p(1,EL)[0],gy+gh,0],radius=.06,color=GREEN))
        for tm,col in [(1,GREEN),(float(FAST0[0][np.argmax(FAST0[1])]),GREY),(float(FASTG[0][np.argmax(FASTG[1])]),YELLOW)]:
            x=p.p(tm,EL)[0];self.add(DashedLine([x,-2.05,0],[x,2.55,0],color=col,stroke_opacity=.4))
        ta=FAST0[0][np.argmax(FAST0[1])];tb=FASTG[0][np.argmax(FASTG[1])]
        yb=bracket(p,tb,-60,max(FASTG[1]),'10.1 mV',YELLOW,-1.05)
        yb[-1].move_to([p.p(tb,-60)[0]-.95,.65,0])
        self.at('made the');self.play(FadeIn(bracket(p,ta,-65,max(FAST0[1]),'12.3 mV',GREY,1.05)),FadeIn(yb),run_time=.6)
        self.at('five millivolt');self.add(bracket(p,25,-65,-60,'5 mV head start',YELLOW,1.8));self.finish()

# One reusable layer-5 cell drawing, with soma and apical dendrite anchored consistently.
def neuron(x=0,y=0,scale=1):
    soma=Polygon([-.42,-.35,0],[.42,-.35,0],[0,.45,0],color=BLUE,fill_opacity=.25,stroke_width=4)
    branches=VGroup(Line([0,.45,0],[0,2,0],color=BLUE,stroke_width=5),Line([0,1.3,0],[-.8,2,0],color=BLUE,stroke_width=4),Line([0,1.3,0],[.8,2,0],color=BLUE,stroke_width=4),Line([-.35,-.25,0],[-1.1,-.7,0],color=BLUE,stroke_width=4),Line([.35,-.25,0],[1.1,-.7,0],color=BLUE,stroke_width=4),Line([0,-.35,0],[0,-1.15,0],color=BLUE,stroke_width=4))
    return VGroup(soma,branches).scale(scale,about_point=ORIGIN).shift([x,y,0])

def cell_labels(x,y,sc=1):
    soma=label('soma',x+1.45*sc,y-.3*sc,26,BLUE)
    apical=label('apical dendrite',x+1.75*sc,y+1.65*sc,26,BLUE)
    return VGroup(soma,Line([x+.3*sc,y-.12*sc,0],soma.get_left()+LEFT*.08,color=BLUE),apical,Line([x,y+1.65*sc,0],apical.get_left()+LEFT*.08,color=BLUE))

def pulse(x,y,late=False,dend=False):
    # Symbolic timelines, not voltage recordings; ms positions are illustrative.
    g=VGroup(Line([x-1.45,y,0],[x+1.45,y,0],color=GREY),label('0',x-1.1,y-.3,26,GREY),label('10 ms',x+.8,y-.3,26,GREY))
    g.add(Line([x-1.1,y,0],[x-1.1,y+.4,0],color=RED,stroke_width=8))
    xx=x+.8 if late else x-.95
    g.add(Line([xx,y,0],[xx,y+.65,0],color=GREEN,stroke_width=6))
    return g

def spikes(x,y,n,col=YELLOW):
    return VGroup(*[Line([x+(i-(n-1)/2)*.35,y,0],[x+(i-(n-1)/2)*.35,y+.38,0],color=col,stroke_width=4) for i in range(n)])

def timing_panel(x,late=False,small=False,dend=False):
    sc=.65 if small else 1.05;cy=.65 if small else .3
    n=neuron(x,cy,sc)
    g=VGroup(n,label('Dendrite' if dend else ('Soma · later' if late else 'Soma · same time'),x,2.65,28,BLUE))
    target=np.array([x,cy+1.15*sc if dend else cy,0])
    g.add(Arrow([x-1.5,target[1],0],target+LEFT*.15,color=RED,buff=.02),Arrow([x+1.5,cy-.25,0],[x+.35,cy-.25,0],color=GREEN,buff=.02))
    g.add(label('dendrite',x+1.35 if not small else x+.8,1.25 if not small else 2.22,24,BLUE),label('soma',x+1.45 if not small else x+.85,cy-.9*sc,24,BLUE))
    if dend:
        for yy,latecase,word in [(-.95,False,'same'),(-2.25,True,'later')]:
            row=pulse(x,yy,latecase);row.remove(row[1],row[2])
            g.add(row,label(word,x+.1,yy+.35,24,GREY),spikes(x-.8,yy-.62,3),label('more spikes',x+.75,yy-.5,24,YELLOW))
    else:
        g.add(pulse(x,-1.3,late),spikes(x,-2.4,3 if late else 1),label('more likely to fire' if late else 'fewer spikes',x,-2.85,26,YELLOW))
    return g

class S19Evidence(SpokenScene):
    def construct(self):
        n=neuron(-3.8,-.2,1.3);self.add(n,cell_labels(-3.8,-.2,1.3),head('Gulledge & Stuart · Neuron (2003)'))
        # Slice schematic: labelled cortical bands; cell body highlighted in layer 5.
        layers=VGroup()
        for i,name in enumerate(['1','2/3','4','5','6']):
            yy=1.6-i*.65;layers.add(Rectangle(width=2.5,height=.65,color=GREY,fill_color=BLUE,fill_opacity=.18 if name=='5' else .04).move_to([2.15,yy,0]),label(name,3.8,yy,26,BLUE if name=='5' else GREY))
        self.at('pyramidal neurons');self.play(FadeIn(layers),FadeIn(label('Layer 5',1.6,-2.05,30,BLUE)),run_time=.5)
        self.at('cortex slices');self.add(label('Rat somatosensory cortex slice',1.4,-2.7,28))
        self.at('weeks old');self.add(foot('3–4 weeks old',GREY));self.finish()

class S20Found(SpokenScene):
    def construct(self):
        p=Plot(duration=60,numeric=False);self.add(p.axes,p.th,head('Depolarizing from rest'),foot('Qualitative model illustration · illustrative voltages',GREY))
        t=np.linspace(0,60,601)
        self.at('responses depolarized');self.play(Create(p.curve(t,step(t))),run_time=.8)
        self.at('below threshold');self.play(Create(DashedLine(p.p(0,EG),p.p(60,EG),color=RED)),FadeIn(backed('E_GABA',-4.2,p.p(0,EG)[1]+.25,26,RED)),run_time=.5);self.finish()

class S21Timing(SpokenScene):
    def construct(self):
        a=timing_panel(-3.15);b=timing_panel(3.15,True)
        self.add(head('Layer 5 · somatic GABA: timing matters'),foot('Qualitative spike marks · red GABA, green excitation',GREY),a[0],a[1],b[0],b[1],*b[2:-2])
        self.at('at the cell body');self.play(FadeIn(VGroup(*a[2:-2])),run_time=.5)
        self.at('inhibited excitation');self.play(FadeIn(VGroup(*a[-2:])),run_time=.4)
        self.at('later excitation');self.play(FadeIn(VGroup(*b[-2:])),run_time=.6);self.finish()

class S22Site(SpokenScene):
    def construct(self):
        self.add(head('Site matters too'),timing_panel(-4.4,small=True),timing_panel(0,True,small=True),foot('At every timing tested in this preparation · qualitative',GREY))
        d=timing_panel(4.4,small=True,dend=True)
        self.add(d[0],d[1])
        self.at('on the dendrites');self.play(FadeIn(VGroup(*d[2:])),run_time=.55);self.finish()

class S23Reading(SpokenScene):
    def construct(self):
        r=Rail(float(step(4,-60,gg=0)));self.add(r.base,r.leak,head('A likely reading · somatic timing only'),foot('Conductance gone; voltage still above rest',YELLOW),hgap(r,1.6))
        self.add(label('distance to threshold (smaller)',0,1.95,26,TEAL),label('Later input',-.8,2.75,28,GREEN),Arrow([-.8,2.25,0],[2.8,2.25,0],color=GREEN,buff=.05))
        restgap=VGroup(Line([xv(-65),-2.95,0],[xv(THR),-2.95,0],color=GREY),Line([xv(-65),-3.05,0],[xv(-65),-2.85,0],color=GREY),Line([xv(THR),-3.05,0],[xv(THR),-2.85,0],color=GREY),label('rest to threshold (larger)',0,-2.45,26,GREY));self.add(restgap)
        self.at('depolarization remained');self.play(Indicate(r.dot,color=YELLOW),run_time=.6);self.finish()

class S24Caveat(SpokenScene):
    def construct(self):
        self.add(neuron(-4,-.3,1.3),cell_labels(-4,-.3,1.3),head('One preparation'),label('Applied GABA',2.5,1.9,34,RED),label('Rat somatosensory',2.5,1.05,30),label('cortex slices',2.5,.5,30))
        self.at('adult cortex in general');self.add(label('Does not show GABA is excitatory',1.8,-.65,28),label('in adult cortex generally',1.8,-1.2,28))
        self.at('depended on timing');self.add(foot('Sign depended on timing and site',RED));self.finish()

class S25Chloride(SpokenScene):
    def construct(self):
        membrane=Rectangle(width=11.7,height=.2,color=GREY,fill_opacity=.4).move_to([0,.6,0])
        ga=chip('GABA_A',RED,28).move_to([-3.2,1.6,0]);kcc=chip('KCC2',GREY,28).move_to([2.8,1.6,0])
        self.add(head('The reversal potential can move'),membrane,ga,kcc,label('outside',-5.2,2.45,26,GREY),label('inside',-5.2,-.4,26,GREY),Line([-3.2,1.2,0],[-2.1,.72,0],color=RED),Line([2.8,1.2,0],[1.6,.72,0],color=GREY),Rectangle(width=.5,height=.4,color=RED,fill_color=BG,fill_opacity=1).move_to([-2.1,.6,0]),Rectangle(width=.5,height=.4,color=GREY,fill_color=BG,fill_opacity=1).move_to([1.6,.6,0]))
        incoming=Arrow([-2.1,2.1,0],[-2.1,-.65,0],color=BLUE,buff=.02,stroke_width=12)
        outgoing=Arrow([1.6,-.65,0],[1.6,2.1,0],color=GREY,buff=.02,stroke_width=3)
        self.at('chloride enters faster');self.play(GrowArrow(incoming),GrowArrow(outgoing),run_time=.45)
        self.add(label('Cl− in',-3.3,-.2,28,BLUE),label('K+ and Cl−',3.7,-.1,26),label('out together',3.7,-.6,26))
        dots=VGroup(*[chip('Cl−',BLUE,26).move_to([-.8+i*1.2,-1.25,0]) for i in range(4)])
        counter=label('Cl− inside: 0',-3.8,-1.3,26,BLUE);self.add(counter)
        for i,ion in enumerate(dots):self.play(FadeIn(ion,shift=DOWN*.3),Transform(counter,label(f'Cl− inside: {i+1}',-3.8,-1.3,26,BLUE)),run_time=.25)
        self.at('reversal potential creeps')
        y=-2.7;axis=VGroup(Line([-5.7,y,0],[5.7,y,0],color=GREY))
        for val in [-65,-60,-55,-50]:axis.add(label(str(val).replace('-','−'),xv(val),y-.4,26,GREY))
        axis.add(label('mV',6.1,y-.4,26,GREY),label('E_GABA creeps up',0,-2.05,30,RED))
        peg=Dot([xv(-55),y,0],radius=.17,color=RED);self.add(axis,peg);self.play(peg.animate.move_to([xv(-52),y,0]),run_time=1);self.finish()

class S26Takeaway(SpokenScene):
    def construct(self):
        r=Rail(-62);self.add(r.zones(),r.base,r.rope,r.elab,head('GABA pulls Vm toward E_GABA'))
        self.at('pulls the voltage');self.play(r.v.animate.set_value(-58),run_time=.6)
        self.at('helps or hinders firing');self.add(label('depolarizing',-3.3,-2.05,28,RED),label('hyperpolarizing',4,-2.05,28,BLUE))
        self.at('depends on timing');self.add(label('Firing depends on timing, site and the other inputs',0,-3.45,30));self.finish()

class S27End(EndCard):
    LINE='GABA pulls toward its reversal potential; whether that helps or hinders firing depends on timing, site and the other inputs.'
    def construct(self):
        lines=VGroup(T('GABA pulls toward its reversal potential;',34,font=TITLE_FONT),T('whether that helps or hinders firing depends on',32,font=TITLE_FONT),T('timing, site and the other inputs.',34,font=TITLE_FONT)).arrange(DOWN,buff=.35)
        self.add(lines,label('biochemistrypedia.com',0,-2.3,26,TEAL));self.wait(self.narration_s)
