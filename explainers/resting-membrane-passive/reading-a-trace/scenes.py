"""Reading a Trace, Predicting a Drug.
COLOR MAP: BLUE K+; ORANGE Na+; YELLOW voltage; GREEN chloride only;
TEAL injected current; GREY structure / before; RED non-ideal dynamics;
TEXT neutral headings, cautions and rules. No molecular structures.
Model: EK=-95, ENa=60.6 mV; gK=8.47, gNa=1.53 nS; C=200 pF.
RC: ΔV=I/g*(1-exp(-tg/C)); cable: V(x)=V(0)*exp(-x/lambda).
HCN illustrative model: C V'=I-gL(V-EL)-gh*h*(V-Eh),
h'=(1/(1+exp((V+82)/7))-h)/100 ms.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares
from bp_style import *
ORANGE='#F29E4C'
KC,NAC,VC=BLUE,ORANGE,YELLOW
EK,ENA,GK,GNA,CAP=-95.,60.6,8.47,1.53,200.
REST=(GK*EK+GNA*ENA)/(GK+GNA)
def label(s,y=3.1,color=TEXT,size=32): return T(s,size,color).move_to([0,y,0])
def rc(t,i=100,g=10,c=CAP): return i/g*(1-np.exp(-max(t,0)*g/c))
def graph(x=-5.2,y=-2.4,w=10.4,h=4.6,xmin=0,xmax=120,ymin=0,ymax=12):
    ax=Axes(x_range=[xmin,xmax,(xmax-xmin)/4],y_range=[ymin,ymax,(ymax-ymin)/3],x_length=w,y_length=h,tips=False,axis_config={'color':GREY,'include_ticks':False})
    ax.shift(np.array([x,y,0])-ax.c2p(xmin,ymin)); return ax

def curve(ax,func,a=0,b=120,color=VC):
    return ax.plot(func,x_range=[a,b,(b-a)/240],color=color,stroke_width=4,use_smoothing=False)
def card(lines,pos=(0,-3.05,0),size=29,color=TEXT):
    words=VGroup(*[T(s,size,color) for s in lines]).arrange(DOWN,buff=.22)
    box=RoundedRectangle(width=words.width+.55,height=words.height+.5,corner_radius=.15,color=color,fill_color=BG,fill_opacity=.96)
    return VGroup(box,words).move_to(pos)
def dim(m,opacity):
    # Preserve open paths: set_opacity would also fill every plotted curve.
    for sm in m.family_members_with_points():
        sm.set_fill(opacity=sm.get_fill_opacity()*opacity,family=False)
        sm.set_stroke(opacity=sm.get_stroke_opacity()*opacity,family=False)
    return m

def upper_rope(m):
    # Keep the larger rope drawing above the comparison inset, with readable type.
    m.stretch(.65,1,about_point=ORIGIN).shift(UP*1.05)
    for sm in m.get_family():
        if isinstance(sm,Text): sm.stretch(1/.65,1)
    return m

def slots(n=0):
    vals=['Rin = ΔV / I','τ = time to 63%','C = τ / Rin']
    return VGroup(*[chip(vals[k] if k<n else ['Rin   ···','τ   ···','C   ···'][k],VC if k<n else GREY,size=27).move_to([4.15,1.55-k*1.6,0]) for k in range(3)])
def measurement(n=0,wide=False):
    w=10.5 if wide else 6.6
    ax=graph(x=-5.2,y=-2.35,w=w,h=3.9)
    tr=curve(ax,lambda t:rc(t-12))
    p=lambda t,y:ax.c2p(t,0)+UP*y
    step=VMobject(color=TEAL,stroke_width=4).set_points_as_corners([p(0,4.6),p(12,4.6),p(12,5.2),p(120,5.2)])
    labs=VGroup(T('current',28,TEAL).move_to([-4.4,3.25,0]),T('ΔV (mV)',27,VC).rotate(PI/2).move_to([-5.9,-.35,0]),T('time (ms)',27,GREY).move_to([ax.c2p(110,0)[0],-2.9,0]))
    return VGroup(ax,tr,step,labs,slots(n))
def plateau(m): return DashedLine(m[0].c2p(0,10),m[0].c2p(120,10),color=GREY)
def rin_marks(m):
    ax=m[0]; x=103
    dv=DoubleArrow(ax.c2p(x,0),ax.c2p(x,10),buff=0,color=VC,tip_length=.15)
    dl=T('ΔV',27,VC).next_to(dv,RIGHT,buff=.12)
    a=ax.c2p(12,0)+UP*4.6; b=a+UP*.6
    br=VGroup(Line(a+LEFT*.22,b+LEFT*.22,color=TEAL),Line(a+LEFT*.35,a+LEFT*.08,color=TEAL),Line(b+LEFT*.35,b+LEFT*.08,color=TEAL),T('I',30,TEAL).move_to(a+LEFT*.65+UP*.3))
    return VGroup(plateau(m),dv,dl,br)
def tau_marks(m):
    ax=m[0]; p=ax.c2p(32,rc(20)); y=ax.c2p(0,0)[1]-.28
    span=DoubleArrow([ax.c2p(12,0)[0],y,0],[p[0],y,0],buff=0,color=VC,tip_length=.10)
    return VGroup(DashedLine(ax.c2p(0,rc(20)),p,color=VC),DashedLine(ax.c2p(32,0),p,color=VC),Dot(p,color=VC),T('63%',27,VC).move_to(p+LEFT*.55+UP*.4),Line(p,p+LEFT*.3+UP*.2,color=VC),span,T('τ',30,VC).move_to([span.get_center()[0],y-.42,0]))
def down_step(x=-5.2,y=2.8,w=10.4):
    return VGroup(VMobject(color=TEAL,stroke_width=4).set_points_as_corners([[x,y,0],[x+.65,y,0],[x+.65,y-.42,0],[x+w,y-.42,0]]),T('current: −200 pA',27,TEAL).move_to([3.65,y+.35,0]))
def step_onset(end): return end*.65/10.4
def step_curve(ax,func,end,color=VC):
    return curve(ax,lambda t:func(max(0,t-step_onset(end))),b=end,color=color)
def trace_stage(end=300):
    ax=graph(y=-2.25,h=4.3,ymin=-25,ymax=0,xmax=end)
    names=VGroup(T('ΔV (mV)',27,VC).rotate(PI/2).move_to([-5.9,-.1,0]),T('time (ms)',27,GREY).move_to([4.45,1.15,0]),down_step(),*[T(str(t),26,GREY).move_to(ax.c2p(t,0)+DOWN*.3+(LEFT*.35 if t==0 else ORIGIN)) for t in [0,end//2,end]])
    return ax,names

def hinf(v): return 1/(1+np.exp((v+82)/7))
EH,GH,VL=-35.,8.,-65.
EL=VL+GH*hinf(VL)*(VL-EH)/10
_H=solve_ivp(lambda t,z:[(-200-10*(z[0]-EL)-GH*z[1]*(z[0]-EH))/CAP,(hinf(z[0])-z[1])/100],[0,300],[VL,hinf(VL)],dense_output=True,max_step=1)
def sag(t): return float(_H.sol(max(t,0))[0]-VL)
def hsteady(i): return brentq(lambda v:i-10*(v-EL)-GH*hinf(v)*(v-EH),-120,-30)-VL
_F=least_squares(lambda p:np.array([p[0]*(1-np.exp(-t/p[1]))-sag(t) for t in np.linspace(0,300,301)]),[-13,15],bounds=([-30,1],[0,200])).x

def vi(extended=False):
    end=250 if extended else 70
    ax=graph(x=-4.7,y=-2.45,w=6.7,h=4.9,xmax=end,ymax=end/10)
    labs=VGroup(T('|I| (pA)',28,TEAL).move_to([-1.35,-3.35,0]),T('|ΔV| (mV)',28,VC).move_to([-4.5,3.05,0]))
    for v in ([0,100,200] if extended else [0,20,40,60]): labs.add(T(str(v),26,GREY).move_to(ax.c2p(v,0)+DOWN*.3))
    for v in ([5,15,25] if extended else [2,4,6]): labs.add(T(str(v),26,GREY).move_to(ax.c2p(0,v)+LEFT*.35))
    return ax,labs,curve(ax,lambda i:i/10,b=end*.93)
def vi_points(ax): return VGroup(*[Dot(ax.c2p(i,i/10),color=c,radius=.09) for i,c in zip([20,40,60],[VC,TEXT,TEAL])])
def slope(ax):
    a,b,c=ax.c2p(20,2),ax.c2p(60,2),ax.c2p(60,6)
    end=c+normalize(c-a)*.75
    return VGroup(DashedLine(a,b,color=GREY),DashedLine(b,c,color=GREY),
                  T('I',28,TEAL).next_to(Line(a,b),DOWN,buff=.14),
                  T('ΔV',28,VC).next_to(Line(b,c),RIGHT,buff=.16),
                  T('slope = Rin',28,VC).next_to(VectorizedPoint(end),RIGHT,buff=.18),
                  Line(a,end,color=VC,stroke_width=4))
# The marker is ON the voltage scale. Arched ropes are a schematic of
# conductance, not geometric length; the Cl endpoints share one voltage.
def scale_base():
    def px(v): return -5.5+(v+100)/170*11
    axis=Line([px(-100),-1.05,0],[px(70),-1.05,0],color=GREY)
    refs=VGroup(*[VGroup(Line([px(v),-1.22,0],[px(v),-.88,0],color=c,stroke_width=4),T(s,28,c).move_to([px(v),-1.65,0])) for v,c,s in [(EK,KC,'EK'),(ENA,NAC,'ENa')]])
    return VGroup(axis,refs),px

def ropes(gk=GK,gna=GNA,gcl=0,v=None):
    if v is None: v=(gk*EK+gna*ENA+gcl*REST)/(gk+gna+gcl)
    base,px=scale_base(); a=np.array([px(v),-1.05,0])
    k=VMobject(color=KC,stroke_width=gk*.85).set_points_smoothly([[px(EK),-1.05,0],[px(EK)-.25,1.55,0],[px(v),2.85,0],a])
    na=VMobject(color=NAC,stroke_width=3).set_points_smoothly([[px(ENA),-1.05,0],[2.8,1.65,0],[0,2.25,0],a])
    dot=Dot(a,radius=.14,color=VC); vm=T('Vm',28,VC).move_to(a+UP*.9+LEFT*.65)
    names=VGroup(T('K+ leak',29,KC).move_to([-5.35,3.35,0]),T('Na+ leak',29,NAC).move_to([2.5,2.95,0]))
    group=VGroup(base,k,na,dot,vm,names)
    if gcl:
        cl=VMobject(color=GREEN,stroke_width=6).set_points_smoothly([[px(REST),-1.05,0],[px(REST)+.4,-2.25,0],[px(REST)+1.1,-1.85,0],a])
        refs=VGroup(DashedLine([px(REST),-1.05,0],[px(REST),-2.2,0],color=GREEN),T('ECl = rest',27,GREEN).move_to([px(REST),-2.5,0]),T('Cl− leak',28,GREEN).move_to([-.2,-1.9,0]),Line([px(REST)+.9,-1.9,0],[-1.3,-1.9,0],color=GREEN))
        group.add(cl,refs)
    return group

def ghost(v=REST):
    _,px=scale_base(); p=[px(v),-1.05,0]
    return VGroup(Circle(.17,color=GREY).move_to(p),DashedLine(p,[px(v),-1.8,0],color=GREY),T('old rest',26,GREY).move_to([px(v)+1,-2.2,0]))
def question():
    return VGroup(label('Pause · Predict',3.0,TEXT,36),label('A drug opens more K+ leak channels.',1.5,KC,33),label('Nothing else changes.',.5,GREY,28),VGroup(*[chip(s,VC,size=34) for s in ['Rest?','Rin?','τ?']]).arrange(RIGHT,buff=.7).move_to([0,-1,0]))
def comparison(g0=10,g1=18.47,small=False):
    x,y,w,h=(-.2,-3.0,5.8,1.45) if small else (-5.2,-2.3,10.4,4.3)
    ax=graph(x=x,y=y,w=w,h=h,ymin=-18,ymax=0)
    onset=(.55-x)/w*120 if small else step_onset(120)
    a=curve(ax,lambda t:rc(t-onset,i=-100,g=g0),color=GREY); b=curve(ax,lambda t:rc(t-onset,i=-100,g=g1),color=VC)
    if small:
        labs=VGroup(T('ΔV',26,VC).move_to([-.75,-2.3,0]),T('time',26,GREY).move_to([5.4,-3.4,0]))
        ly=-1.08; sx=.2
        step=VMobject(color=TEAL,stroke_width=3).set_points_as_corners([[.1,-.65,0],[.55,-.65,0],[.55,-.9,0],[5.7,-.9,0]])
    else:
        labs=VGroup(T('ΔV (mV)',27,VC).rotate(PI/2).move_to([-5.9,-.15,0]),T('time (ms)',27,GREY).move_to([4.4,1.68,0]))
        ly=3.15; sx=-1.2
        step=VMobject(color=TEAL,stroke_width=4).set_points_as_corners([[-5.2,2.8,0],[-4.55,2.8,0],[-4.55,2.4,0],[5.2,2.4,0]])
        labs.add(T('test: −100 pA',27,TEAL).move_to([-3.9,3.2,0]))
    for k,(s,c) in enumerate([('before',GREY),('after',VC)]):
        xx=sx+k*2.85
        labs.add(Line([xx,ly,0],[xx+.45,ly,0],color=c,stroke_width=4),T(s,26,c).move_to([xx+1.2,ly,0]))
    return ax,a,b,VGroup(labs,step)

class S00Title(TitleCard):
    LESSON='The Resting Membrane and Passive Signals'
    TITLE='Reading a Trace, Predicting a Drug'
class S01Question(SpokenScene):
    def construct(self):
        m=measurement(wide=True); self.add(m[0],m[3]); self.at('one small step'); self.play(Create(m[2]),run_time=.65)
        self.at('one voltage trace'); self.play(Create(m[1]),run_time=.85)
        self.at('what can it'); self.play(FadeIn(label('What can this tell us?',3.25,TEXT,32)),FadeOut(m[3][0]),run_time=.4); self.finish()
class S02Three(SpokenScene):
    def construct(self):
        m=measurement(wide=True); self.add(m[:4]); self.at('compact passive cell'); self.play(FadeIn(label('compact · passive',3.3,GREY,28)),FadeOut(m[3][0]),run_time=.35)
        self.at('it gives three'); new=measurement(); self.play(Transform(m[:4],new[:4]),FadeIn(new[4]),run_time=.7); self.finish()
class S03Rin(SpokenScene):
    def construct(self):
        m=measurement(); self.add(m); self.at('input resistance'); self.play(Indicate(m[1],color=VC),run_time=.4)
        self.at('the plateau divided'); self.play(Create(rin_marks(m)),Transform(m[4],slots(1)),run_time=.85); self.finish()
class S04Tau(SpokenScene):
    def construct(self):
        m=measurement(1); self.add(m,plateau(m)); self.at('the time constant'); self.play(Create(tau_marks(m)),run_time=.65)
        self.at('the time to reach'); self.play(Transform(m[4],slots(2)),run_time=.5); self.finish()
class S05Cap(SpokenScene):
    def construct(self):
        m=measurement(2); self.add(m,plateau(m),tau_marks(m)); self.at('capacitance'); self.play(Indicate(m[4][:2]),run_time=.4)
        self.at('the time constant divided'); tau=T('τ',34,VC).move_to(m[4][1]); rin=T('Rin',30,VC).move_to(m[4][0]); self.add(tau,rin)
        target=m[4][2].get_center(); self.play(FadeOut(m[4][2]),tau.animate.move_to(target+UP*.25),rin.animate.move_to(target+DOWN*.25),run_time=.65)
        bar=Line(target+LEFT*.4,target+RIGHT*.4,color=VC); self.play(Create(bar),run_time=.3)
        self.play(FadeOut(tau),FadeOut(rin),FadeOut(bar),Transform(m[4],slots(3)),Transform(m[:4],dim(m[:4].copy(),.25)),run_time=.6); self.finish()
class S06Compact(SpokenScene):
    def construct(self):
        def branch(start,end,width):
            start,end=np.array(start,dtype=float),np.array(end,dtype=float)
            normal=normalize(rotate_vector(end-start,PI/2))*width/2
            return Polygon(start+normal,end+normal*.12,end-normal*.12,start-normal,
                           stroke_width=0,fill_color=GREY,fill_opacity=1)
        compact=VGroup(Circle(.85,color=GREY,fill_opacity=.1).move_to([-3.4,.1,0]))
        for sx in [-1,1]:
            for sy in [-1,1]:
                start=[-3.4+sx*.62,.1+sy*.55,0]; tip=[-3.4+sx*1.35,.1+sy*1.1,0]
                compact.add(branch(start,tip,.14),branch([-3.4+sx*.98,.1+sy*.82,0],[-3.4+sx*1.4,.1+sy*.65,0],.08))
        compact.scale(2.2).move_to(ORIGIN); ct=T('compact cell',31).move_to([0,3.1,0]); self.add(compact,ct); self.at('compact matters'); self.play(Indicate(compact),run_time=.5)
        self.at('big dendrites'); soma=Circle(.85,color=GREY,fill_opacity=.1).move_to([2.7,.1,0]); branches=VGroup(soma)
        for sx in [-1,1]:
            for sy in [-1,1]:
                start=np.array([2.7+sx*.6,.1+sy*.55,0]); mid=np.array([2.7+sx*1.15,sy*1.05,0]); end=np.array([2.7+sx*1.65,sy*2.15,0])
                branches.add(branch(start,mid,.19),branch(mid,end,.12))
                for d in [-.4,.4]:
                    tip=mid+np.array([sx*(.7+d),sy*(.7-d),0])
                    branches.add(branch(mid,tip,.09))
        self.play(compact.animate.scale(1/2.2).move_to([-3.4,.1,0]),ct.animate.move_to([-3.4,2.9,0]),Create(branches),FadeIn(T('big dendrites',31).move_to([2.7,2.9,0])),run_time=.9)
        self.at('that last step'); tag=card(['τ / Rin','underestimates C'],(2.7,-2.95,0),27); self.play(FadeIn(tag),run_time=.5); self.finish()
class S07Vi(SpokenScene):
    def construct(self):
        ax,labs,ln=vi(); ta=graph(x=-4.7,y=-2.35,w=9.3,h=4.6,ymin=-7,ymax=0)
        self.add(ta,T('ΔV (mV)',28,VC).rotate(PI/2).move_to([-5.5,-.1,0]),T('time (ms)',27,GREY).move_to([4.3,2.6,0]))
        self.at('several small steps'); cs=[VC,TEXT,TEAL]; traces=VGroup(*[curve(ta,lambda t,i=i:rc(t-8,i=-i),color=c) for i,c in zip([20,40,60],cs)])
        tags=VGroup(*[T(f'−{i} pA → −{i//10} mV',27,c).move_to([2.7,1.25-k*1.32,0]) for k,(i,c) in enumerate(zip([20,40,60],cs))])
        # Each trace is a response to the labelled downward current step.
        steps=VGroup()
        for k,(i,c) in enumerate(zip([20,40,60],cs)):
            xx=-4.8+k*3.2
            step=VMobject(color=c,stroke_width=3).set_points_as_corners([[xx,3.15,0],[xx+.4,3.15,0],[xx+.4,3.15-i*.008,0],[xx+1.5,3.15-i*.008,0]])
            steps.add(step,T(f'−{i} pA',26,c).move_to([xx+.75,3.6,0]))
        self.play(Create(traces),FadeIn(tags),Create(steps),run_time=.8)
        dots=VGroup(*[Dot(ta.c2p(116,rc(108,i=-i)),color=c) for i,c in zip([20,40,60],cs)]); self.add(dots)
        self.at('plot each plateau'); old=Group(*[m for m in self.mobjects if m is not dots and m is not tags]); self.play(FadeOut(old),FadeIn(ax),FadeIn(labs),run_time=.4)
        pts=vi_points(ax)
        for k in range(3): self.play(Transform(dots[k],pts[k]),Transform(tags[k],T(f'−{[20,40,60][k]} pA',26,cs[k]).next_to(pts[k],UP+LEFT,buff=.12)),run_time=.35)
        self.play(Create(ln),run_time=.5); self.at('the slope is'); self.play(Create(slope(ax)),run_time=.5); self.finish()
class S08Line(SpokenScene):
    def construct(self):
        ax,labs,ln=vi(); self.add(ax,labs,ln,vi_points(ax)); self.at('fits a passive'); ca=card(['Straight line','fits a passive membrane'],(4.1,1.2,0),26); self.play(FadeIn(ca),run_time=.4)
        self.at('does not prove'); self.play(Transform(ca,card(['Straight line','fits a passive membrane','does not prove one'],(4.1,.8,0),26)),run_time=.4); self.finish()
class S09Shape(SpokenScene):
    def construct(self):
        ax,names=trace_stage(end=120); self.add(ax,names,T('hyperpolarizing step',28).move_to([-2.8,3.45,0])); self.at('check the'); self.play(Create(step_curve(ax,lambda t:rc(t,i=-200),120)),run_time=1)
        self.at('a pure resistor'); self.play(FadeIn(T('pure RC',32,VC).move_to([2.8,-2.7,0])),run_time=.4); self.finish()
class S10Sag(SpokenScene):
    def construct(self):
        ax,names=trace_stage(); ref=DashedVMobject(step_curve(ax,lambda t:rc(t,i=-200),300,color=GREY),num_dashes=50); self.add(ax,names,ref,T('passive RC',27,GREY).move_to([3.8,-1.8,0]))
        self.at('voltage overshoots'); self.play(Create(step_curve(ax,sag,300,color=RED)),run_time=1.1)
        ts=np.linspace(0,300,601); tp=ts[np.argmin([sag(t) for t in ts])]; p=ax.c2p(tp+step_onset(300),sag(tp)); q=ax.c2p(285,sag(285-step_onset(300)))
        marks=VGroup(Dot(p,color=RED),T('peak',27,RED).move_to([-3.5,-2.15,0]),Line(p,[-3.5,-1.88,0],color=RED),Dot(q,color=RED),T('steady level',27,RED).next_to(q,UP,buff=.15))
        self.at('sags back'); ar=DoubleArrow(ax.c2p(180,sag(tp)),ax.c2p(180,sag(285-step_onset(300))),color=RED,buff=0,tip_length=.12); self.play(FadeIn(marks),GrowArrow(ar),FadeIn(T('sag',28,RED).next_to(ar,RIGHT,buff=.12)),run_time=.5)
        self.at('conductance is turning'); self.play(FadeIn(label('conductance turns on with voltage',-3.35,RED,28)),run_time=.4); self.finish()
class S11Hcn(SpokenScene):
    def construct(self):
        ax,names=trace_stage(); tr=step_curve(ax,sag,300,color=RED); self.add(ax,names,tr); self.at('often'); title=T('HCN current (often)',30,RED).move_to([-2.8,3.45,0]); self.play(FadeIn(title),run_time=.4)
        self.at('plot of plateau'); va,vl,ln=vi(extended=True); self.play(FadeOut(VGroup(ax,names,tr,title)),FadeIn(va),FadeIn(vl),Create(DashedVMobject(ln,num_dashes=32).set_color(GREY)),FadeIn(T('passive prediction',27,GREY).move_to([3.9,2.5,0])),run_time=.6)
        # A model-computed nonlinear example; no channel attribution on this plot.
        self.at('bends'); bent=curve(va,lambda i:-hsteady(-i),b=232.5,color=RED); self.play(Create(bent),run_time=.7)
        self.at('input resistance depends'); self.play(FadeIn(T('Rin depends\non voltage',30,RED).move_to([4.1,.3,0])),run_time=.5); self.finish()
class S12Mislead(SpokenScene):
    def construct(self):
        ax,names=trace_stage(); self.add(ax,names,step_curve(ax,sag,300,color=RED)); self.at('a single resistor')
        f=lambda t:_F[0]*(1-np.exp(-max(0,t)/_F[1])); fitcurve=DashedVMobject(step_curve(ax,f,300,color=TEXT),num_dashes=45)
        gap=Polygon(*[ax.c2p(t,sag(max(0,t-step_onset(300)))) for t in np.linspace(0,300,100)],*[ax.c2p(t,f(t-step_onset(300))) for t in np.linspace(300,0,100)],stroke_width=0,fill_color=RED,fill_opacity=.2)
        self.play(Create(fitcurve),FadeIn(gap),run_time=1.5); self.play(FadeIn(label('single RC fit misleads',-3.35,RED,31)),run_time=.35); self.at('will mislead'); self.finish()
class S13Rule(SpokenScene):
    def construct(self):
        self.add(ropes()); self.at('ask two questions'); self.play(FadeIn(label('Predict a drug',3.45,TEXT,34)),run_time=.4)
        self.at('conductance changed'); c=card(['1 · Which conductance? Which way?'],(0,-3.05,0)); self.play(FadeIn(c),run_time=.5)
        self.at('that moves rest'); self.play(Transform(c,card(['1 · Which conductance? Which way?','→ rest'],(0,-3.05,0))),run_time=.4); self.finish()
class S14Rule2(SpokenScene):
    def construct(self):
        self.add(ropes(),label('Predict a drug',3.45,TEXT,34)); self.at('total conductance'); c=card(['2 · Total conductance up or down?'],(0,-3.05,0)); self.play(FadeIn(c),run_time=.5)
        self.at('that moves input'); self.play(Transform(c,card(['2 · Total conductance up or down?','→ Rin and τ'],(0,-3.05,0))),run_time=.4); self.finish()
class S15Predict(SpokenScene):
    def construct(self):
        q=question(); self.add(q[0]); self.at('a drug opens'); self.play(FadeIn(q[1:3]),run_time=.7); self.at('what happens'); self.play(FadeIn(q[3]),run_time=.5); self.finish()
class S16Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question()); back=Line([-3,-2.6,0],[3,-2.6,0],color=GREY,stroke_width=8); bar=back.copy().set_color(TEXT); self.add(back,bar,T('Predict all three',28).move_to([0,-3.2,0])); self.play(bar.animate.stretch(.001,0,about_edge=LEFT),run_time=8,rate_func=linear)
class S17Reveal(SpokenScene):
    def construct(self):
        r=ropes(); self.add(r,ghost()); self.at("potassium's rope"); self.play(Transform(r,ropes(gk=2*GK,v=REST)),FadeIn(label('more K+ conductance',3.45,KC,31)),run_time=.8)
        self.at('so rest moves'); _,px=scale_base(); new=(2*GK*EK+GNA*ENA)/(2*GK+GNA); ar=VGroup(DashedLine([px(REST),-1.05,0],[px(REST),-.7,0],color=GREY),Arrow([px(REST)+1,-.7,0],[px(new),-.7,0],buff=0,color=VC,tip_length=.18))
        self.play(Transform(r,ropes(gk=2*GK)),Create(ar),run_time=1.1)
        self.at('the cell hyperpolarizes'); self.play(FadeIn(card(['hyperpolarizes'],(0,-3.05,0),36)),run_time=.5); self.finish()
class S18Reveal2(SpokenScene):
    def construct(self):
        ax,a,b,labs=comparison(); self.add(ax,a,labs); self.at('total conductance rises'); self.play(Create(b),run_time=.85)
        self.at('input resistance falls'); result=label('Rin ↓',-3.5,VC,30); self.play(FadeIn(result),run_time=.35)
        self.at('time constant shortens'); self.play(Transform(result,label('Rin ↓     τ ↓',-3.5,VC,30)),run_time=.4); self.finish()
class S19Close(SpokenScene):
    def construct(self):
        r=upper_rope(ropes()); self.add(r,upper_rope(ghost())); self.at('closing a leak'); self.play(Transform(r,upper_rope(ropes(gk=GK/2,v=REST))),FadeIn(label('K+ leak closed',3.45,KC,31)),run_time=.8)
        self.at('input resistance and'); ax,a,b,labs=comparison(g1=GK/2+GNA,small=True); self.play(FadeIn(VGroup(ax,a,b,labs)),FadeIn(T('Rin ↑\nτ ↑',30,VC).move_to([-4.9,-2.8,0])),run_time=.7)
        self.at('rest moves away'); _,px=scale_base(); new=(GK/2*EK+GNA*ENA)/(GK/2+GNA); ar=upper_rope(VGroup(DashedLine([px(REST),-1.05,0],[px(REST),-.7,0],color=GREY),Arrow([px(REST)-.7,-.7,0],[px(new),-.7,0],buff=0,color=VC,tip_length=.18))); self.play(Transform(r,upper_rope(ropes(gk=GK/2))),Create(ar),run_time=1); self.finish()
class S20Shunt(SpokenScene):
    def construct(self):
        self.add(dim(ropes(),.35)); self.at('one case'); self.play(FadeIn(label('Shunting',3.45,TEXT,38)),run_time=.5)
        self.at('new channels reverse'); _,px=scale_base(); tick=VGroup(Line([px(REST),-1.25,0],[px(REST),-.85,0],color=GREEN,stroke_width=5),DashedLine([px(REST),-1.2,0],[px(REST),-2.1,0],color=GREEN),card(['channel reversal = Vm'],(0,-2.7,0),31,GREEN)); self.play(Create(tick),run_time=.65); self.finish()
class S21Shunt2(SpokenScene):
    def construct(self):
        r=ropes(); self.add(r); self.at('chloride channels'); self.play(FadeIn(label('Cl− at equilibrium',3.45,GREEN,32)),run_time=.5)
        self.at('their rope is anchored'); self.play(Transform(r,ropes(gcl=10)),run_time=.8); self.finish()
class S22Shunt3(SpokenScene):
    def construct(self):
        self.add(ropes(gcl=10),label('Cl− at equilibrium',3.45,GREEN,32)); self.at('not stretched'); c=card(['no stretch → no pull'],(0,-3.15,0),30); self.play(FadeIn(c),run_time=.5)
        self.at('rest does not move'); self.play(FadeOut(c),FadeIn(card(['no stretch → no pull · same rest'],(0,-3.15,0),30)),run_time=.4); self.finish()
class S23Shunt4(SpokenScene):
    def construct(self):
        r=upper_rope(ropes(gcl=10)); self.add(r); self.at('marker is now harder'); self.play(FadeIn(label('same current · added Cl− conductance',3.45,TEXT,29)),run_time=.5)
        self.at('any other current'); _,px=scale_base(); push=Arrow([px(REST)+2,.3675,0],[px(REST)+.3,.3675,0],color=TEXT,buff=0,stroke_width=7); self.play(GrowArrow(push),run_time=.4)
        # Show the no-shunt displacement as a ghost before the smaller actual displacement.
        no=Circle(.16,color=GREY).move_to([px(REST-100/10),.3675,0]); self.play(FadeIn(no),run_time=.3)
        self.at('shifts the voltage less'); self.play(Transform(r,upper_rope(ropes(gcl=10,v=REST-100/20))),run_time=.5)
        ax,a,b,labs=comparison(g1=20,small=True)
        # Magnified displacement comparison; arrow lengths remain I/g, same scale.
        dis=VGroup(T('shift (magnified)',24,TEXT).move_to([-4.25,-1.8,0]))
        for yy,d,s,c in [(-2.45,(100/10)*(11/170)*4,'before',GREY),(-3.25,(100/20)*(11/170)*4,'after',VC)]:
            dis.add(Arrow([-2.9,yy,0],[-2.9-d,yy,0],buff=0,color=c),T(s,26,c).move_to([-1.8,yy,0]))
        self.play(FadeIn(VGroup(ax,a,b,labs,dis)),run_time=.5); self.finish()
class S24Shunt5(SpokenScene):
    def construct(self):
        self.add(ropes(gcl=10)); self.at('that is shunting'); c=card(['shunting'],(0,-3.15,0),31); self.play(FadeIn(c),run_time=.4)
        self.at('lowers input resistance'); c2=card(['shunting = lower Rin'],(0,-3.15,0),31); self.play(FadeOut(c),run_time=.15); self.play(FadeIn(c2),run_time=.25)
        self.at('without moving'); self.play(FadeOut(c2),run_time=.15); self.play(FadeIn(card(['shunting = lower Rin, same Vm'],(0,-3.15,0),31)),run_time=.25); self.finish()
class S25Whole(SpokenScene):
    def construct(self):
        self.add(ropes(gcl=10)); self.at('our passive model'); top=label('passive model',3.45,GREY,27); self.play(FadeIn(top),run_time=.35)
        self.at('with no injected current'); self.play(Transform(top,label('passive model · no injected current',3.45,GREY,27)),run_time=.35)
        self.at("pump's own current"); self.play(FadeIn(label('pump’s direct current set aside',-2.95,GREY,26)),run_time=.35)
        self.at('rest is where'); self.play(FadeIn(label('Rest is where the leaks balance.',-3.55,TEXT,32)),run_time=.4); self.finish()
class S26Takeaway(SpokenScene):
    def construct(self):
        self.add(label('Rest is where the leaks balance.',3.35,TEXT,32)); self.at('the leak with capacitance')
        sentence=VGroup(T('Leak, capacitance and the core decide',29),T('how big, how fast and how far a nudge goes.',29)).arrange(DOWN,buff=.16).move_to([0,2.6,0]); self.play(FadeIn(sentence),run_time=.5)
        ax=graph(x=-5.15,y=-2.6,w=4.2,h=3.55,ymin=-12,ymax=0); tr=curve(ax,lambda t:rc(t-(.4/4.2*120),i=-100)); self.add(ax,T('ΔV',28,VC).move_to([-5.8,.65,0]),T('time',28,GREY).move_to([-1.5,.55,0]),T('test: −100 pA',26,TEAL).move_to([-3.1,1.8,0]))
        step=VMobject(color=TEAL,stroke_width=3).set_points_as_corners([[-5.15,1.6,0],[-4.75,1.6,0],[-4.75,1.35,0],[-1,1.35,0]]); self.add(step)
        self.at('how big'); self.play(Create(tr),FadeIn(T('how big',28,VC).move_to([-3.1,-3.15,0])),run_time=.4)
        self.at('how fast'); self.play(FadeIn(T('how fast',28,VC).move_to([-3.1,-3.6,0])),run_time=.3)
        bx=graph(x=1.05,y=-2.6,w=4.2,h=3.55,xmax=1.5,ymax=1.1); space=curve(bx,lambda x:np.exp(-x/.5),b=1.5)
        tube=RoundedRectangle(width=3.4,height=.5,corner_radius=.2,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([3.2,.95,0]); tube.add(T('core',24,TEXT).move_to(tube)); self.at('how far'); self.play(FadeIn(VGroup(bx,tube,T('along a dendrite',27,GREY).move_to([3.2,1.45,0]),T('distance (mm)',27,GREY).move_to([3.2,-3.2,0]),T('V / V₀',27,VC).rotate(PI/2).move_to([.45,-.65,0]))),Create(space),run_time=.5); self.finish()
class S27End(EndCard):
    LINE='Leak decides rest; leak and capacitance decide the response.'
