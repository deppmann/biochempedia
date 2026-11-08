"""Chapter 1: One More Rope.
COLOR MAP: BLUE neuron; GREEN AMPA/excitation; RED GABA/inhibition;
GREY leak/structure; YELLOW Vm; TEAL threshold. Ropes are schematic.
Model: C=200 pF, gL=10 nS, EL=-65 mV, EE=0 mV.
All voltage traces solve C dV/dt = sum(g*(E-V)).
"""
import numpy as np
from bp_style import *

EL, EE, THR, C = -65., 0., -50., 200.

def vss(gL, gE, gI, EI=-65.):
    return (gL*EL+gE*EE+gI*EI)/(gL+gE+gI)

def step(t, start=-65., ge=2., gi=0., ei=-65.):
    total=10+ge+gi
    end=vss(10,ge,gi,ei)
    return end+(start-end)*np.exp(-np.asarray(t)*total/C)

def xvolt(v):
    return -5.6+(v+80)*11.2/90

def header(s):
    return T(s,32).move_to([0,3.35,0])

class Rail:
    def __init__(self,v=-65,plot=False):
        self.v=ValueTracker(v)
        self.y=1.0 if plot else -.8
        self.top=2.25 if plot else 1.65
        y=self.y
        self.axis=VGroup(Line([-5.6,y,0],[5.6,y,0],color=GREY,stroke_width=3))
        for n in [-80,-65,-50,0,10]:
            self.axis.add(Line([xvolt(n),y-.19,0],[xvolt(n),y+.19,0],color=GREY,stroke_width=3),M(str(n).replace('-','−'),26,GREY).move_to([xvolt(n),y-.65,0]))
        self.axis.add(T('mV',26,GREY).move_to([6.15,y,0]))
        self.threshold=VGroup(DashedLine([xvolt(THR),y+.32,0],[xvolt(THR),self.top-.25,0],color=TEAL),T('threshold',26,TEAL).move_to([xvolt(THR)+.4,self.top+.45,0]))
        self.dot=always_redraw(lambda:Dot([xvolt(self.v.get_value()),y,0],radius=.41,color=YELLOW))
        # Marker tag stays below tick labels, clear of all rope lanes.
        self.vm=always_redraw(lambda:T('Vm',26,YELLOW).move_to([xvolt(self.v.get_value()),y-1.1,0]))
        self.base=VGroup(self.axis,self.threshold,self.dot,self.vm)
    def rope(self,e,color,label,width=14):
        y,top=self.y,self.top
        # A slight lateral schematic offset makes the leak visible even at rest.
        end=np.array([xvolt(e)+.35,top,0])
        peg=VGroup(Line([xvolt(e),y+.25,0],end,color=color,stroke_width=3),Dot(end,color=color,radius=.12))
        rope=always_redraw(lambda:Line([xvolt(self.v.get_value()),y,0],end,color=color,stroke_width=max(14,width)))
        if color==GREY and e==-65:
            pos=[-2.05,top+.05,0]
        elif e < -60:
            pos=[-5.05,top+.43,0]
        else:
            pos=[3.9,top+.43,0]
        lab=T(label,26,color).move_to(pos)
        return VGroup(peg,rope,lab)
    def leak(self):
        return self.rope(-65,GREY,'leak 10 nS',12)
    def ampa(self):
        return self.rope(0,GREEN,'AMPA 2 nS',9)
    def rest(self):
        return VGroup(Line([xvolt(-65)-.28,self.y-.22,0],[-4.9,self.y-1.2,0],color=YELLOW),T('rest −65 mV',30,YELLOW).move_to([-4.9,self.y-1.65,0]))

class Plot:
    def __init__(self,box=(-4.9,5.7,-2.8,-.45),duration=80,lo=-77,hi=-43,threshold=True):
        self.box,self.duration=box,duration
        x0,x1,y0,y1=box
        self.px=lambda t:x0+(x1-x0)*np.asarray(t)/duration
        self.py=lambda v:y0+(y1-y0)*(np.asarray(v)-lo)/(hi-lo)
        self.axes=VGroup(Line([x0,y0,0],[x1,y0,0],color=GREY),Line([x0,y0,0],[x0,y1,0],color=GREY))
        for v in [-65,-50]:
            yy=float(self.py(v))
            self.axes.add(Line([x0-.1,yy,0],[x0,yy,0],color=GREY),M(f'−{abs(v)}',26,GREY).move_to([x0-.49,yy,0]))
        self.axes.add(T('mV',26,YELLOW).move_to([x0-.4,y1+.35,0]))
        for t in [0,20,duration]:
            if t==20 and duration==20: continue
            self.axes.add(T(f'{int(t)}'+(' ms' if t==duration else ''),26,GREY).move_to([float(self.px(t)),y0-.36,0]))
        if threshold:
            yy=float(self.py(THR))
            self.axes.add(DashedLine([x0,yy,0],[x1,yy,0],color=TEAL,stroke_width=2),T('threshold',26,TEAL).move_to([(x0+x1)/2,yy+.23,0]))
    def curve(self,fn,end=None,color=YELLOW,dashed=False):
        ts=np.linspace(0,self.duration if end is None else max(.001,end),260)
        vs=fn(ts)
        cu=VMobject(color=color,stroke_width=5).set_points_as_corners([[float(self.px(t)),float(self.py(v)),0] for t,v in zip(ts,vs)])
        return DashedVMobject(cu,num_dashes=35) if dashed else cu

def formula():
    num=VGroup(M('gL × EL',34,GREY),M('+',32),M('gE × EE',34,GREEN),M('+',32),M('gI × EI',34,RED)).arrange(RIGHT,buff=.24).move_to([.7,1.8,0])
    den=VGroup(M('gL',34,GREY),M('+',32),M('gE',34,GREEN),M('+',32),M('gI',34,RED)).arrange(RIGHT,buff=.35).move_to([.7,.65,0])
    return VGroup(M('Vss =',36,YELLOW).move_to([-5.1,1.23,0]),num,Line([-3.65,1.23,0],[5.5,1.23,0],color=TEXT),den)

def scope():
    return T('Passive cell • one voltage everywhere',30,GREY).move_to([0,-.45,0])

def prediction(plot=False):
    r=Rail(plot=plot)
    ro=r.rope(-75,RED,'GABA 10 nS',12)
    q=header('Which way does the marker move?')
    rest=r.rest()
    prompt=T('Pause and predict: down, up or no change?',34,TEAL).move_to([0,-2.9,0])
    return r,ro,q,rest,prompt

def definitions():
    cards=[]
    for x,name,col,msg in [(-3.25,'EPSP',GREEN,'more likely to fire'),(3.25,'IPSP',RED,'less likely to fire')]:
        card=VGroup(RoundedRectangle(width=5.9,height=4.8,corner_radius=.2,color=col,fill_color=col,fill_opacity=.07).move_to([x,0,0]),T(name,48,col).move_to([x,1.45,0]),T(msg,32).move_to([x,.35,0]))
        cards.append(card)
    return cards

class S00Title(TitleCard):
    LESSON='Integration, Inhibition and Neuromodulation'
    TITLE='One More Rope'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,26,GREY),T(self.TITLE,54,font=TITLE_FONT),Line(LEFT*1.2,RIGHT*1.2,color=GOLD)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.6);self.finish()

class S01Question(SpokenScene):
    def construct(self):
        self.add(header('How can inhibition stop firing?'))
        p=Plot((-5.1,-.9,-2.6,1.8));q=Plot((1.8,6,-2.6,1.8))
        self.add(p.axes,q.axes,T('inhibitory input on',28,RED).move_to([-3,2.5,0]),T('excitatory input',28,GREEN).move_to([3.9,2.5,0]))
        flat=p.curve(lambda t:step(t,ge=0,gi=10))
        ref=q.curve(lambda t:step(t,ge=5),color=GREY,dashed=True)
        # Excitation starts first; the shunt opens at 8 ms, visibly bending the rise.
        def stopped(t):
            v8=float(step(8,ge=5))
            return np.where(t<=8,step(t,ge=5),step(np.maximum(t-8,0),start=v8,ge=5,gi=10))
        cut=q.curve(stopped)
        self.at('inhibitory input');self.play(Create(flat),run_time=.7)
        self.at('stop a cell');self.play(Create(ref),Create(cut),run_time=1.2)
        self.play(FadeIn(T('+ inhibition',28,RED).move_to([4,-.25,0])),run_time=.3)
        self.at('resting voltage unchanged');self.play(FadeIn(T('rest stays flat',30,YELLOW).move_to([-3,0,0])),FadeIn(T('held below threshold',28,YELLOW).move_to([3.9,-1.15,0])),run_time=.4)
        self.finish()

class S02Recall(SpokenScene):
    def construct(self):
        r=Rail();self.add(header('The balance point'),r.axis,r.threshold,r.dot,r.vm)
        target=Circle(radius=.49,color=YELLOW).move_to(r.dot)
        self.at('balance point');self.play(Create(target),run_time=.5)
        self.at('the cell settles');self.play(FadeIn(T('Where voltage settles',34,YELLOW).move_to([1,1.1,0])),run_time=.5)
        self.at('open channels stay');self.play(FadeIn(T('if the open channels stay as they are',30,GREY).move_to([0,-3.15,0])),run_time=.5)
        self.at('A marker');self.play(Indicate(r.dot),FadeIn(r.rest()),run_time=.5)
        self.finish()

class S03Ropes(SpokenScene):
    def construct(self):
        r=Rail();self.add(header('Channels pull toward their reversal potential'),r.base)
        ro=r.rope(0,GREY,'E: reversal potential')
        self.at('open channel');self.play(Create(ro[0]),Create(ro[1]),run_time=.65)
        self.at('reversal potential');self.play(FadeIn(ro[2]),run_time=.4)
        note=T('zero current at E',28,GREY).move_to([2.5,.2,0])
        lead=Line([3.6,.45,0],ro[0][1].get_center()+DOWN*.15,color=GREY)
        self.at('Each rope pulls');self.play(GrowArrow(Arrow([-2.9,-2.2,0],[1.5,-2.2,0],color=GREY)),FadeIn(note),Create(lead),run_time=.6)
        self.add(T('toward its end',30,GREY).move_to([0,-2.95,0]));self.finish()

class S04Pull(SpokenScene):
    def construct(self):
        self.add(header('How hard does a rope pull?'))
        # Compact marker-and-peg diagram links the current equation to the rope.
        self.add(Line([-4,1.35,0],[4,1.35,0],color=GREY),Dot([-3,1.35,0],radius=.25,color=YELLOW),Dot([3,2.5,0],radius=.12,color=GREY),Line([-3,1.35,0],[3,2.5,0],color=GREY,stroke_width=10),T('Vm',28,YELLOW).move_to([-3.6,1.9,0]),T('E',28,GREY).move_to([3.6,2.5,0]))
        eq=VGroup(M('I',52,YELLOW),M('=',46),M('g',52,GREY),M('×',46),M('(Vm − E)',52,YELLOW)).arrange(RIGHT,buff=.35).move_to([0,-.35,0])
        self.at('How hard');self.play(FadeIn(eq),run_time=.4)
        self.at('its current');self.play(FadeIn(T('current',28,YELLOW).next_to(eq[0],DOWN,buff=.5)),run_time=.3)
        self.at('conductance');self.play(FadeIn(T('conductance',26,GREY).move_to([eq[2].get_x(),-2,0])),run_time=.3)
        b=Brace(eq[4],DOWN,buff=.15)
        self.at('driving force');self.play(Create(b),FadeIn(T('driving force',28,YELLOW).next_to(b,DOWN,buff=.2)),run_time=.4)
        self.finish()

class S05Terms(SpokenScene):
    def construct(self):
        r=Rail();ro=r.rope(0,GREY,'E: reversal potential');self.add(header('Conductance and driving force'),r.base,ro,T('zero current at E',28,GREY).move_to([2.5,.2,0]))
        ro[1].clear_updaters()
        a,b=ro[1].get_start(),ro[1].get_end()
        icons=VGroup(*[RoundedRectangle(width=.38,height=.55,corner_radius=.06,color=GREY,fill_color=BG,fill_opacity=1,stroke_width=4).move_to(a+(b-a)*f) for f in [.2,.4,.6,.8]])
        self.at('Conductance');self.play(FadeIn(icons[0]),run_time=.4)
        self.at('how many channels');self.play(FadeIn(VGroup(*icons[1:])),ro[1].animate.set_stroke(width=17),run_time=.7)
        gap=VGroup(Line([xvolt(-65),-2.5,0],[xvolt(0),-2.5,0],color=YELLOW),*[Line([xvolt(v),-2.3,0],[xvolt(v),-2.7,0],color=YELLOW) for v in [-65,0]])
        self.at('Driving force');self.play(FadeOut(icons),Create(gap),run_time=.5)
        self.at('the gap');self.play(FadeIn(T('driving force: Vm − E',32,YELLOW).move_to([0,-3.2,0])),run_time=.4)
        self.finish()

class S06Leak(SpokenScene):
    def construct(self):
        r=Rail();self.add(header('The rope already open at rest'),r.base)
        ro=r.leak()
        self.at('one rope');self.play(Create(ro[0]),Create(ro[1]),run_time=.5)
        self.at('the leak');self.play(FadeIn(ro[2]),run_time=.4)
        self.at('It is');self.play(Indicate(ro[2]),run_time=.5)
        self.at('tied at');self.play(FadeIn(r.rest()),run_time=.4)
        self.finish()

class S07Ampa(SpokenScene):
    def construct(self):
        r=Rail();self.add(header('A synapse adds one more rope'),r.base,r.leak(),r.rest())
        ro=r.ampa()
        self.at('synapse fires');self.play(Create(ro[0]),Create(ro[1]),run_time=.6)
        self.at('receptors add');self.play(FadeIn(ro[2]),run_time=.4)
        self.at('tied near');self.play(Indicate(ro[0]),run_time=.5)
        self.finish()

class S08Settle(SpokenScene):
    def construct(self):
        r=Rail(plot=True);p=Plot(duration=160);t=ValueTracker(0)
        cu=always_redraw(lambda:p.curve(lambda ts:step(ts),end=t.get_value()))
        self.add(header('The leak holds the marker back'),r.base,r.leak(),r.ampa(),p.axes,cu)
        self.add(r.v)
        r.v.add_updater(lambda v:v.set_value(float(step(t.get_value()))))
        self.at('The marker');self.play(t.animate.set_value(80),run_time=2.5,rate_func=linear)
        self.at('So it settles');self.play(FadeIn(T('−54.2 mV',30,YELLOW).move_to([3.5,-1.65,0])),run_time=.4)
        self.finish()

class S09Psp(SpokenScene):
    def construct(self):
        # Continue the same physical rise, then append its decay without redrawing history.
        r=Rail(float(step(80)),plot=True);p=Plot(duration=160)
        p.axes[-1].move_to([4.2,-.72,0])
        ro=r.ampa();t=ValueTracker(80)
        grid=np.linspace(0,160,6401)
        values=np.empty_like(grid);values[0]=EL
        for i,dt in enumerate(np.diff(grid)):
            u=np.clip((grid[i]+dt/2-80)/10,0,1)
            ge=2*(1-3*u*u+2*u*u*u)
            total=10+ge; equilibrium=vss(10,ge,0)
            values[i+1]=equilibrium+(values[i]-equilibrium)*np.exp(-dt*total/C)
        def pulse(ts):
            return np.interp(ts,grid,values)
        cu=always_redraw(lambda:p.curve(pulse,end=t.get_value()))
        self.add(header('A postsynaptic potential'),r.base,r.leak(),ro,p.axes,cu)
        self.at('That rise');self.play(FadeIn(T('postsynaptic potential',28,YELLOW).move_to([.4,-.45,0])),run_time=.4)
        self.at('channels close');ro[1].clear_updaters()
        a,b=ro[1].get_start(),ro[1].get_end()
        slack=VMobject(color=GREEN,stroke_width=9).set_points_smoothly([a,a*.65+b*.35+DOWN*.65,a*.3+b*.7+DOWN*.7,b])
        self.play(Transform(ro[1],slack),run_time=.5)
        self.at('goes slack');self.play(FadeOut(ro),run_time=.4)
        self.add(r.v)
        r.v.add_updater(lambda v:v.set_value(float(pulse(np.array([t.get_value()]))[0])))
        self.at('drifts back');self.play(t.animate.set_value(160),run_time=1.7,rate_func=linear)
        self.finish()

class S10GabaRope(SpokenScene):
    def construct(self):
        r=Rail();self.add(header('GABA_A: chloride channels'),r.base,r.leak())
        peg=ValueTracker(-70)
        # GABA remains red, matching the chapter COLOR MAP. No nested redraws.
        def sliding_rope():
            end=np.array([xvolt(peg.get_value())+.35,r.top,0])
            return VGroup(Line([xvolt(-65),r.y,0],end,color=RED,stroke_width=14),Line([xvolt(peg.get_value()),r.y+.25,0],end,color=RED,stroke_width=3),Dot(end,color=RED,radius=.12),T('GABA 10 nS',26,RED).move_to([-5.05,r.top+.43,0]))
        ro=always_redraw(sliding_rope)
        tag=always_redraw(lambda:T('E_GABA',28,RED).move_to([xvolt(peg.get_value()),-2.1,0]))
        self.at('receptors are');self.play(FadeIn(T('set by the chloride gradient',32,RED).move_to([0,-2.7,0])),run_time=.4)
        self.at('their rope');self.play(FadeIn(ro),FadeIn(tag),run_time=.5)
        self.at('depends on');self.play(peg.animate.set_value(-78),run_time=.65);self.play(peg.animate.set_value(-75),run_time=.5)
        self.finish()

class S11Predict(SpokenScene):
    def construct(self):
        r,ro,q,rest,prompt=prediction();self.add(r.base,r.leak(),q)
        self.at('rope is tied');self.play(FadeIn(ro),FadeIn(T('E_GABA = −75 mV',30,RED).move_to([2,-1.7,0])),run_time=.5)
        self.at('The cell rests');self.play(FadeIn(rest),run_time=.4)
        self.at('Which way');self.play(FadeIn(prompt),run_time=.4)
        self.finish()

class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        r,ro,q,rest,prompt=prediction();self.add(r.base,r.leak(),ro,q,rest,prompt,T('E_GABA = −75 mV',30,RED).move_to([2,-1.7,0]));self.wait(5)

class S13Reveal(SpokenScene):
    def construct(self):
        r=Rail(plot=True);ro=r.rope(-75,RED,'GABA 10 nS',12);p=Plot();t=ValueTracker(0)
        cu=always_redraw(lambda:p.curve(lambda ts:step(ts,ge=0,gi=10,ei=-75),end=t.get_value()))
        self.add(header('IPSP: the balance point drops below rest'),r.base,r.leak(),ro,p.axes,cu)
        self.add(r.v)
        r.v.add_updater(lambda v:v.set_value(float(step(t.get_value(),ge=0,gi=10,ei=-75))))
        self.at('Down');self.play(Indicate(ro[1],color=RED),t.animate.set_value(80),run_time=1.8,rate_func=linear)
        self.at('balance point drops');self.play(FadeIn(T('−70 mV: between the two ropes',28,YELLOW).move_to([1.6,-1.45,0])),run_time=.4)
        self.at('the textbook');self.play(Indicate(cu,color=RED),run_time=.5)
        self.finish()

class S14Define(SpokenScene):
    def construct(self):
        a,b=definitions();self.add(header('Defined by the effect on firing'),a[0],b[0])
        self.at('An');self.play(FadeIn(a[1]),run_time=.3)
        self.at('more likely');self.play(FadeIn(a[2]),run_time=.4)
        self.at('makes firing');self.play(FadeIn(b[1]),run_time=.4)
        self.at('less likely');self.play(FadeIn(b[2]),run_time=.4)
        self.finish()

class S15Firing(SpokenScene):
    def construct(self):
        a,b=definitions();self.add(header('Firing outcome defines the name'),a,b)
        # Counterexample: a depolarizing inhibitory response, compared with a typical EPSP.
        # No invented downward EPSP: the model supplies an upward IPSP instead.
        p=Plot((-5.2,-1.15,-1.9,-.35),threshold=False);q=Plot((1.3,5.35,-1.9,-.35),threshold=False)
        traces=VGroup(p.curve(lambda t:step(t,ge=2),color=GREEN),q.curve(lambda t:step(t,ge=0,gi=10,ei=-55),color=RED))
        self.at('about firing');self.play(Create(traces),run_time=.6)
        self.at('not about');self.play(FadeIn(T('Vm can rise in either case',32,YELLOW).move_to([0,-3.05,0])),run_time=.5)
        self.add(T('upward EPSP',26,GREEN).move_to([-3.25,-2.05,0]),T('upward IPSP',26,RED).move_to([3.25,-2.05,0]));self.finish()

class S16Promise(SpokenScene):
    def construct(self):
        self.add(header('Both can hold back excitation'))
        p=Plot((-5.1,-.9,-2.15,1.65));q=Plot((1.8,6,-2.15,1.65))
        self.add(p.axes,q.axes,T('GABA: no change at rest',27,RED).move_to([-3,2.45,0]),T('GABA: Vm moves up',27,RED).move_to([3.9,2.45,0]))
        self.add(p.curve(lambda t:step(t,ge=0,gi=10),color=RED),q.curve(lambda t:step(t,ge=0,gi=30,ei=-55),color=RED))
        self.at('this lesson');self.play(Indicate(p.axes),run_time=.5)
        self.at('voltage unchanged');self.play(FadeIn(T('excitation alone',24,GREY).move_to([-3,-3,0])),FadeIn(T('excitation + GABA',24,GREEN).move_to([-3,-3.5,0])),FadeIn(p.curve(lambda t:step(t,ge=5),color=GREY,dashed=True)),FadeIn(p.curve(lambda t:step(t,ge=5,gi=10),color=GREEN)),run_time=.6)
        self.at('input that moves');self.play(Indicate(q.axes),run_time=.5)
        self.at('yet can still');self.play(FadeIn(T('excitation alone',24,GREY).move_to([3.9,-3,0])),FadeIn(T('excitation + GABA',24,GREEN).move_to([3.9,-3.5,0])),FadeIn(q.curve(lambda t:step(t,ge=5),color=GREY,dashed=True)),FadeIn(q.curve(lambda t:step(t,ge=5,gi=30,ei=-55),color=GREEN)),run_time=.6)
        self.finish()

class S17Formula(SpokenScene):
    def construct(self):
        f=formula();f[0].scale(1.15);f[1].scale(1.25);f[3].scale(1.25)
        f.shift(DOWN*.8)
        self.add(header('A weighted average of the ropes’ ends'))
        self.at('Written out');self.play(FadeIn(f),run_time=.6)
        self.at('an average');self.play(Indicate(f[1],scale_factor=1.04),run_time=.5)
        self.at('passive cell');self.play(FadeIn(scope().move_to([0,-1.35,0])),run_time=.5)
        self.add(T('Each end contributes through its conductance',32,YELLOW).move_to([0,-2.05,0]));self.finish()

class S18Weights(SpokenScene):
    def construct(self):
        f=formula();self.add(header('Each rope has a share'),f)
        self.at('Each end')
        for term,col in [(f[1][0],GREY),(f[1][2],GREEN),(f[1][4],RED)]:
            self.play(Indicate(term,color=col,scale_factor=1.12),run_time=.28)
        self.at('weighted by');self.play(FadeIn(M('share = g / (gL + gE + gI)',28).move_to([0,-.3,0])),run_time=.3)
        self.play(FadeIn(T('leak 10 nS at −65 mV • AMPA 2 nS at 0 mV • gI = 0',26).move_to([0,-1.15,0])),run_time=.35)
        self.at('total conductance');self.play(FadeIn(chip('leak 5/6',GREY,28).move_to([-2,-1.95,0])),FadeIn(chip('AMPA 1/6',GREEN,28).move_to([2,-1.95,0])),run_time=.35)
        self.play(FadeIn(M('Vss = −54.2 mV',34,YELLOW).move_to([0,-2.95,0])),run_time=.35)
        self.wait(2)
        self.finish()

class S18bScope(SpokenScene):
    def construct(self):
        self.add(header('When this balance rule applies'),formula(),scope())
        self.at('no current injected');self.play(FadeIn(T('No injected current',30,GREY).move_to([0,-1.25,0])),run_time=.4)
        self.at('do not change');self.play(FadeIn(T('Conductances fixed with voltage',30,GREY).move_to([0,-2.05,0])),run_time=.4)
        y=-2.95;v=ValueTracker(-65);target=vss(10,2,0)
        axis=Line([-5.6,y,0],[5.6,y,0],color=GREY)
        ghost=Circle(radius=.28,color=YELLOW,stroke_opacity=.5).move_to([xvolt(target),y,0])
        marker=always_redraw(lambda:Dot([xvolt(v.get_value()),y,0],radius=.18,color=YELLOW))
        labels=VGroup(always_redraw(lambda:T('Vm',24,YELLOW).move_to([xvolt(v.get_value()),y-.4,0])),T('Vss',24,YELLOW).move_to([xvolt(target),y+.4,0]))
        self.at('The marker then');self.play(Create(axis),FadeIn(ghost),FadeIn(marker),FadeIn(labels),run_time=.35)
        self.play(v.animate.set_value(target-.25),run_time=1.1,rate_func=rate_functions.ease_out_cubic)
        self.finish()

class S19TwoJobs(SpokenScene):
    def construct(self):
        f=formula();self.add(header('A new synapse does two jobs'),f)
        y=-2.15;t=ValueTracker(-65)
        dot=always_redraw(lambda:Dot([xvolt(t.get_value()),y,0],radius=.25,color=YELLOW))
        end=np.array([xvolt(0),-1.35,0]);ro=always_redraw(lambda:Line(dot.get_center(),end,color=GREEN,stroke_width=9))
        self.add(Line([-5.6,y,0],[5.6,y,0],color=GREY),dot,T('−65 mV',26,GREY).move_to([xvolt(-65),-2.8,0]),T('0 mV',26,GREEN).move_to([xvolt(0),-2.8,0]))
        leakend=np.array([xvolt(-65)+.35,-1.1,0])
        leak=always_redraw(lambda:Line(dot.get_center(),leakend,color=GREY,stroke_width=12))
        self.add(leak,Dot(leakend,color=GREY),T('leak 10 nS',26,GREY).move_to([-3.65,-.75,0]))
        self.at('two jobs');self.play(Indicate(f[1]),run_time=.4)
        self.at('First');self.play(FadeIn(T('1  Pull toward the new rope’s end',30,GREEN).move_to([0,-.4,0])),Create(ro),FadeIn(Dot(end,color=GREEN)),FadeIn(T('AMPA 2 nS',26,GREEN).move_to([4,-.85,0])),run_time=.5)
        self.at('toward its own');self.play(t.animate.set_value(vss(10,2,0)),run_time=1.4,rate_func=linear)
        self.finish()

class S20Bottom(SpokenScene):
    def construct(self):
        f=formula();self.add(header('2  Add to total conductance'),f)
        g=ValueTracker(0)
        # Fixed-width bar, absolute rope widths unchanged as shares change.
        def shares():
            vals=[10,2,g.get_value()];cols=[GREY,GREEN,RED];x=-5.5;pieces=VGroup()
            for val,col in zip(vals,cols):
                w=11*max(.001,val)/sum(vals)
                pieces.add(Rectangle(width=w,height=.55,fill_color=col,fill_opacity=1,stroke_width=0).move_to([x+w/2,-2.25,0]));x+=w
            return pieces
        bar=always_redraw(shares)
        legend=VGroup(T('leak',26,GREY).move_to([-3.7,-1.55,0]),T('AMPA',26,GREEN).move_to([0,-1.55,0]),T('new rope',26,RED).move_to([3.7,-1.55,0]))
        old=VGroup(Line([-4.6,-1,0],[-2.8,-1,0],color=GREY,stroke_width=12),Line([-.9,-1,0],[.9,-1,0],color=GREEN,stroke_width=9))
        new=Line([2.8,-1,0],[4.6,-1,0],color=RED,stroke_width=12)
        self.add(T('gL = 10 nS • gE = 2 nS • new gI: 0 → 10 nS',28).move_to([0,-.4,0]),legend,old,bar,T('share of total conductance',28).move_to([0,-3.05,0]))
        self.at('Second');self.play(Indicate(f[3]),Create(new),run_time=.5)
        self.at('Every other rope');self.play(g.animate.set_value(10),run_time=1.4)
        self.at('counts for less');self.play(Indicate(bar),run_time=.5)
        self.finish()

class S21Settles(SpokenScene):
    def construct(self):
        self.add(header('More conductance: faster settling'))
        # Same starting displacement; opening a shunt tied at rest halves tau.
        p=Plot((-5.1,-.9,-2.0,1.75));q=Plot((1.8,6,-2.0,1.75))
        self.add(p.axes,q.axes,T('leak 10 nS',30,GREY).move_to([-3,2.5,0]),T('+ GABA 10 nS at rest',28,RED).move_to([3.9,2.5,0]))
        self.add(T('after a brief depolarisation',28,YELLOW).move_to([0,-3,0]))
        self.at('In this passive cell');self.play(Create(p.curve(lambda t:step(t,start=-55,ge=0))),run_time=.8)
        self.at('settles faster');self.play(Create(q.curve(lambda t:step(t,start=-55,ge=0,gi=10))),run_time=.8)
        self.add(T('settles in about 60 ms',24,YELLOW).move_to([-3,-1.75,0]),T('about 30 ms',24,YELLOW).move_to([3.9,-1.75,0]))
        self.at('next chapter');self.play(FadeIn(T('Next: time and distance',32,TEAL).move_to([0,-3.55,0])),run_time=.4)
        self.wait(1.5)
        self.finish()

class S22Takeaway(SpokenScene):
    def construct(self):
        r=Rail(vss(10,2,0));self.add(header('A synapse is one more rope'),r.base,r.leak(),r.ampa())
        self.at('A synapse');self.play(Indicate(r.ampa()[0]),run_time=.5)
        self.at('Conductances add');self.play(FadeIn(T('Conductances add.',40).move_to([0,-2.5,0])),run_time=.4)
        self.at('their weighted average');self.play(FadeIn(T('Balance point = weighted average',36,YELLOW).move_to([0,-3.25,0])),run_time=.4)
        self.finish()

class S23End(EndCard):
    LINE='One more rope: conductances add; the balance point is their weighted average.'
    def construct(self):
        # Twelve-word rule, wrapped to preserve readable type.
        g=VGroup(T('One more rope: conductances add.',40,font=TITLE_FONT),T('The balance point is their weighted average.',36,YELLOW,font=TITLE_FONT),T('biochemistrypedia.com',26,TEAL)).arrange(DOWN,buff=.6)
        self.play(FadeIn(g),run_time=.6);self.finish()
