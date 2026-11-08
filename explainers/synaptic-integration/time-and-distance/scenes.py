"""Chapter 2: passive integration, reviewed fix round.
COLOR MAP: BLUE neuron; GREEN input/current; RED inhibitory conductance;
GREY leak/structure; YELLOW local voltage; TEAL filtered soma voltage; GOLD emphasis.
All curves and attenuation bars use RC or passive cable equations. No LaTeX.
"""
import numpy as np
from bp_style import *
C, GL, TAU = 200., 10., 20.

def label(s,x,y,color=TEXT,size=28):
    return T(s,size,color,font='STIX Two Text' if ('τ' in s or 'λ' in s) else FONT).move_to([x,y,0])

def heading(s):
    return label(s,0,3.35,TEXT,32)

def curve(ax,x,y,color=YELLOW,width=5):
    return VMobject(color=color,stroke_width=width,fill_opacity=0).set_points_as_corners(
        [ax.c2p(float(a),float(b)) for a,b in zip(x,y)])

def axes(xr=(0,70,10),yr=(0,5,1),w=10.5,h=5.2,c=(.25,0)):
    return Axes(x_range=xr,y_range=yr,x_length=w,y_length=h,
        axis_config={'color':GREY,'include_tip':False,'include_ticks':False}).move_to([*c,0])

def ticks(ax,xs,ys=(),xunit='ms',ylabel='mV above rest'):
    g=VGroup()
    for x in xs:
        p=ax.c2p(x,0)
        g.add(Line(p+DOWN*.07,p+UP*.07,color=GREY),label(str(x),p[0],p[1]-.3,GREY,26))
    for y in ys:
        p=ax.c2p(0,y)
        g.add(label(str(y),p[0]-.33,p[1],GREY,26))
    if xunit:
        p=ax.c2p(ax.x_range[1],0)
        g.add(label(xunit,p[0]+.55,p[1]-.3,GREY,26))
    if ylabel:
        t=T(ylabel,26,YELLOW).rotate(PI/2)
        t.move_to(ax.c2p(0,(ax.y_range[0]+ax.y_range[1])/2)+LEFT*.85)
        g.add(t)
    return g

def span(a,b,color=GREY):
    delta=np.asarray(b)-np.asarray(a)
    cap=np.array([-delta[1],delta[0],0.]); cap=.1*cap/np.linalg.norm(cap)
    return VGroup(Line(a,b,color=color),Line(a-cap,a+cap,color=color),Line(b-cap,b+cap,color=color))

def epsp(t,onset=5.,tau=20.):
    u=np.maximum(np.asarray(t)-onset,0.)
    return 20*(1-np.exp(-np.minimum(u,3)/tau))*np.exp(-np.maximum(u-3,0)/tau)

def epsp_stage():
    ax=axes((0,70,10),(0,6,1),10.4,4.9,(.25,-.05))
    return ax,VGroup(ax,ticks(ax,[0,10,20,40,60],[0,2,4]))

def pulse_trace(ax,tau,end=28):
    x=np.linspace(0,10,120); z=np.linspace(10,end,150)
    return curve(ax,np.r_[0,0,x[1:],10,z[1:]],np.r_[0,2,2*np.exp(-x[1:]/tau),2+2*np.exp(-10/tau),2*np.exp(-z[1:]/tau)+2*np.exp(-(z[1:]-10)/tau)])

def exp_text(before, exponent, after, x, y, size=30):
    base=T(before+'e',size,YELLOW)
    power=T(exponent,26,YELLOW).next_to(base,RIGHT,buff=.03).shift(UP*.23)
    g=VGroup(base,power)
    if after:
        tail=T(after,size,YELLOW).next_to(power,RIGHT,buff=.08)
        tail.align_to(base,DOWN); g.add(tail)
    return g.move_to([x,y,0])

def formula(tau,x):
    # Unicode superscripts typeset the exponent without caret notation or LaTeX.
    val=2+2*np.exp(-10/tau)
    return exp_text('2 + 2 × ',f'−10/{tau}',f' = {val:.2f} mV',x,-3.3,26)

def panels():
    aa=axes((0,28,10),(0,4,1),4.65,4.6,(-3.25,.05))
    bb=axes((0,28,10),(0,4,1),4.65,4.6,(2.75,.05))
    names=VGroup(label('Cell A: τ = 20 ms',-3.25,2.8,YELLOW),label('Cell B: τ = 10 ms',2.75,2.8,YELLOW))
    marks=VGroup()
    for ax in (aa,bb):
        marks.add(ticks(ax,[0,10,20],[0,2,4],ylabel=''))
        for t in (0,10):
            marks.add(Arrow(ax.c2p(t,3.8),ax.c2p(t,3.1),color=GREEN,buff=0))
    unit=label('mV above rest',-.25,3.38,GREY,26)
    return aa,bb,VGroup(aa,bb,names,marks,unit)

QUESTION='Which is higher just after pulse 2?'

def neuron(branched=False):
    soma=Circle(1.15,color=BLUE,fill_opacity=.12).move_to([4.6,-.65,0])
    wall=Polygon([-5.5,-.1,0],[3.7,.05,0],[3.7,-1.35,0],[-5.5,-1.2,0],color=BLUE,fill_opacity=.08)
    g=VGroup(wall,soma,label('soma',4.6,-2.15,BLUE),label('dendrite',-.6,-2.,BLUE))
    if branched:
        for a,b in [([-3.4,-.15,0],[-3.1,2.5,0]),([-1,-.2,0],[-.2,2.4,0]),([-2,-1.1,0],[-3.4,-3.1,0])]:
            g.add(Line(a,b,color=BLUE,stroke_width=15))
    return g

def synapse(x=-4.5,y=-.1):
    return VGroup(Arrow([x,y+1.15,0],[x,y,0],color=GREEN,buff=0,stroke_width=6),label('synapse',x-1.05,y+1.5,GREEN,26))

class S00Title(TitleCard):
    LESSON='Integration, Inhibition and Neuromodulation'
    TITLE='Adding Inputs in Time and Space'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON.upper(),26,GREY),fit(T(self.TITLE,54,font=TITLE_FONT),11.5),Line(LEFT*1.2,RIGHT*1.2,color=GOLD)).arrange(DOWN,buff=.32)
        self.play(FadeIn(g),run_time=.8); self.finish()

class S01Question(SpokenScene):
    def construct(self):
        ax=axes((0,25,5),(0,5,1),10.5,5.3,(0,-.05))
        self.add(ax,ticks(ax,[0,5,10,15,20],xunit='ms',ylabel=''),curve(ax,[0,25],[0,0]),label('rest: −65 mV',-3.8,-3.25,YELLOW))
        self.at('Two inputs arrive')
        arrows=VGroup(*[Arrow(ax.c2p(t,4.1),ax.c2p(t,.6),color=GREEN,buff=0,stroke_width=8) for t in (5,15)])
        self.play(Create(arrows),run_time=.6)
        self.at('milliseconds apart')
        a,b=ax.c2p(5,4.4),ax.c2p(15,4.4)
        self.play(Create(span(a,b,GREEN)),FadeIn(label('10 ms',(a[0]+b[0])/2,a[1]+.4,GREEN)),run_time=.4)
        self.at('Does the second')
        self.play(FadeIn(label('?',ax.c2p(10,2)[0],-.2,YELLOW,72)),run_time=.4)
        self.at('or from what')
        self.play(FadeIn(heading('Rest, or what the first left behind?')),run_time=.4); self.finish()

class S02Lag(SpokenScene):
    def construct(self):
        y=lambda v:3+v*6/70
        x=1.2; start=np.array([x,y(-65),0]); end=np.array([x,y(-65*10/15),0])
        dot=Dot(start,.16,color=YELLOW); ring=Circle(.27,color=YELLOW).move_to(start)
        self.add(Line([x,-3,0],[x,3,0],color=GREY),dot,ring,*[label(f'{v} mV',-.2,y(v),GREY) for v in (-65,-40,-20,0)],label('voltage marker',3.8,-2.6,YELLOW))
        self.at('When conductances change')
        rope=Line([-4,2.5,0],end,color=GREEN,stroke_width=8)
        self.play(Create(rope),FadeIn(label('conductance opens',-3,3,GREEN)),run_time=.45)
        self.play(ring.animate.move_to(end),run_time=.25)
        self.at('the marker does not')
        self.play(FadeIn(label('balance point',3.85,end[1]+.55,YELLOW)),FadeIn(label('−43.3 mV',3.85,end[1]-.05,YELLOW)),run_time=.3)
        self.at('jump to the new')
        trail=TracedPath(dot.get_center,stroke_color=YELLOW,stroke_opacity=.3,stroke_width=6)
        self.add(trail)
        self.play(dot.animate.move_to(end),run_time=4,rate_func=lambda a:(1-np.exp(-4*a))/(1-np.exp(-4)))
        self.finish()

class S03Charge(SpokenScene):
    def construct(self):
        plates=VGroup(*[Line([x,-2.35,0],[x,2.35,0],color=GREY,stroke_width=12) for x in (-1.8,.3)])
        marker=Dot([3.6,-2.35,0],.16,color=YELLOW)
        self.add(plates,marker,Line([3.6,-2.35,0],[3.6,2.35,0],color=GREY),label('outside',-2.3,2.85),label('inside',.8,2.85),label('C',-.75,0,TEXT,52),label('membrane capacitance',0,-3.2),label('voltage (mV)',4,3.3,YELLOW))
        for v,yy in [(-65,-2.35),(-55,0),(-45,2.35)]:
            self.add(label(str(v),4.5,yy,GREY,26))
        self.at('Changing the voltage')
        charges=VGroup()
        anim=[]
        for i,yy in enumerate(np.linspace(-1.8,1.8,5)):
            pair=VGroup(label('−',-4.5,yy,YELLOW,36),label('+',2,yy,YELLOW,36))
            charges.add(pair)
            anim.append(AnimationGroup(pair[0].animate.move_to([-2.15,yy,0]),pair[1].animate.move_to([.65,yy,0])))
        self.add(charges)
        arrows=VGroup(Arrow([-4,-2.6,0],[-2.3,-2.6,0],color=YELLOW,buff=0),Arrow([1.8,-2.6,0],[.7,-2.6,0],color=YELLOW,buff=0))
        self.add(arrows)
        self.at('moving charge onto')
        self.play(LaggedStart(*anim,lag_ratio=.3),marker.animate.move_to([3.6,2,0]),run_time=4,rate_func=linear)
        self.at('That takes time')
        self.play(FadeOut(charges,shift=LEFT*.7),marker.animate.move_to([3.6,-.8,0]),arrows.animate.rotate(PI),run_time=1)
        self.finish()

class S04Tau(SpokenScene):
    def construct(self):
        ax=axes((0,80,20),(0,1.1,.2),10.3,5.3,(.2,-.05))
        self.add(ax,ticks(ax,[0,20,40,60],[0,1],ylabel='fraction of change'),DashedLine(ax.c2p(0,1),ax.c2p(80,1),color=GREY),label('new level: 100%',3.5,2.9,GREY),label('start',-4.5,-2.2,GREY))
        self.at('The membrane time constant')
        x=np.linspace(0,80,300); self.play(Create(curve(ax,x,1-np.exp(-x/20))),run_time=1.3)
        self.at('tau says how long')
        self.play(FadeIn(label('τ',ax.c2p(20,0)[0],-3.3,YELLOW,42)),run_time=.3)
        self.at('It is the time')
        p=ax.c2p(20,1-np.exp(-1))
        self.play(Create(VGroup(DashedLine(ax.c2p(0,1-np.exp(-1)),p,color=GREY),DashedLine(ax.c2p(20,0),p,color=YELLOW),Dot(p,color=YELLOW))),run_time=.6)
        self.at('of the way')
        self.play(FadeIn(label('63% reached',p[0]+1.5,p[1]-.45,YELLOW)),FadeIn(label('37% still to go',2.6,-1.45,YELLOW,32)),run_time=.4); self.finish()

class S05TauValue(SpokenScene):
    def construct(self):
        self.add(heading('Membrane time constant'),label('C: capacitance',-3.1,1.8,YELLOW,34),label('total g: open conductance',2.2,1.8,GREEN,30))
        top=label('τ = C / total g',0,.3,TEXT,62)
        self.at('Tau equals the capacitance'); self.play(FadeIn(top),run_time=.6)
        self.at('divided by the total'); self.play(Indicate(top,color=YELLOW,scale_factor=1.04),run_time=.5)
        self.at('In our cell')
        self.play(FadeIn(label('200 pF / 10 nS = 20 ms',0,-1.05,YELLOW,40)),FadeIn(label('in our cell: only the leak is open',0,-2.1,GREY)),FadeIn(label('R = 1/gL = 100 MΩ',0,-3,TEXT,34)),run_time=.6); self.finish()

class S06Shortens(SpokenScene):
    def construct(self):
        knot=Dot([-.6,0,0],.22,color=YELLOW)
        leak=Line([-4.6,-2.2,0],[-.6,0,0],color=GREY,stroke_width=12)
        eq=label('τ = 200 / 10 = 20 ms',0,-3.15,YELLOW,34)
        head=heading('τ = C / gL')
        bar=Rectangle(width=4,height=.45,color=YELLOW,fill_opacity=.6).move_to([.8,-.2,0],aligned_edge=LEFT)
        self.add(head,eq,knot,leak,label('gL = 10 nS',-4.4,-2.8,GREY),bar,label('τ',.4,-.2,YELLOW,34))
        for v in (0,10,20): self.add(label(str(v),.8+v/5,-1.1,GREY,26))
        self.add(label('ms',5.6,-1.1,GREY,26))
        self.at('Because tau uses')
        self.at('the total conductance',lead=.3)
        self.play(FadeOut(head),FadeOut(eq),run_time=.15)
        head.become(heading('τ = C / (gL + gE)')); eq.become(label('τ = 200 / (10 + 5) = 13.3 ms',0,-3.15,YELLOW,34))
        self.play(Create(Line([-4.6,2,0],[-.6,0,0],color=GREEN,stroke_width=9)),FadeIn(label('gE = 5 nS',-4.5,2.55,GREEN)),FadeIn(head),FadeIn(eq),bar.animate.stretch_to_fit_width(200/15/5).move_to([.8,-.2,0],aligned_edge=LEFT),run_time=.5)
        self.at('in this passive model',lead=.3)
        self.play(FadeOut(head),FadeOut(eq),run_time=.15)
        head.become(heading('τ = C / (gL + gE + gI)')); eq.become(label('τ = 200 / (10 + 5 + 10) = 8 ms',0,-3.15,YELLOW,32))
        self.play(FadeIn(Line([-4.6,.1,0],[-.6,0,0],color=RED,stroke_width=12)),FadeIn(label('gI = 10 nS',-4.4,.65,RED)),FadeIn(head),FadeIn(eq),bar.animate.stretch_to_fit_width(1.6).move_to([.8,-.2,0],aligned_edge=LEFT),run_time=.5); self.finish()

class S07Shape(SpokenScene):
    def construct(self):
        ax,stage=epsp_stage()
        # Independent current strip, aligned to the voltage plot's millisecond scale.
        x0,x5,x8,x20=[ax.c2p(t,0)[0] for t in (0,5,8,20)]
        pulse=VMobject(color=GREEN,stroke_width=4,fill_opacity=0).set_points_as_corners(
            [[x0,2.8,0],[x5,2.8,0],[x5,3.15,0],[x8,3.15,0],[x8,2.8,0],[x20,2.8,0]])
        a,b=np.array([x5,3.35,0]),np.array([x8,3.35,0])
        self.add(stage,pulse,span(a,b,GREEN),label('3 ms',(x5+x8)/2,3.65,GREEN,26),
                 label('current',-5.8,3.15,GREEN,22),label('synaptic current flows',1.6,3.1,GREEN),label('EPSP',-3.4,-1.9,YELLOW))
        self.at('has a shape')
        x=np.linspace(0,5,30); self.play(Create(curve(ax,x,epsp(x))),run_time=.3)
        self.at('For a brief')
        self.play(FadeIn(label('brief fast input • compact passive cell',0,-3.4,GREY,26)),run_time=.3)
        self.at('it rises while')
        x=np.linspace(5,8,100); cursor=Dot([x5,3.15,0],.07,color=GREEN); self.add(cursor)
        self.play(Create(curve(ax,x,epsp(x))),cursor.animate.move_to([x8,3.15,0]),run_time=2.2,rate_func=linear)
        self.at('over a few'); self.finish()

class S08Decay(SpokenScene):
    def construct(self):
        ax,stage=epsp_stage(); x=np.linspace(0,8,100)
        self.add(stage,curve(ax,x,epsp(x)).set_stroke(opacity=.3),label('current has ended',0,3.3,GREEN))
        self.at('Once that current fades'); self.wait(.2)
        self.at('the voltage decays')
        x=np.linspace(8,70,250); self.play(Create(curve(ax,x,epsp(x))),run_time=1.25)
        self.at('with the resting')
        peak=float(epsp(8)); p=ax.c2p(28,peak/np.e)
        a,b=ax.c2p(8,.3),ax.c2p(28,.3)
        self.play(Create(VGroup(DashedLine(ax.c2p(0,peak/np.e),p,color=GREY),DashedLine(ax.c2p(28,0),p,color=YELLOW),Dot(p,color=YELLOW),span(a,b,YELLOW))),FadeIn(label('37% of peak',p[0]+1.7,p[1]+.35,YELLOW)),FadeIn(label('τ = 20 ms',(a[0]+b[0])/2,-1.85,YELLOW)),run_time=.5)
        self.play(FadeIn(label('Other receptors, dendrites and active channels give other shapes.',0,-3.5,GREY,26)),run_time=.3); self.finish()

class S09Ride(SpokenScene):
    def construct(self):
        ax,stage=epsp_stage(); x=np.linspace(0,70,400)
        self.add(stage,curve(ax,x,epsp(x)).set_stroke(opacity=.35))
        self.at('If a second')
        self.play(Create(VGroup(*[Arrow(ax.c2p(t,5.3),ax.c2p(t,4.25),color=GREEN,buff=0) for t in (5,15)])),Create(span(ax.c2p(5,5.7),ax.c2p(15,5.7),GREEN)),FadeIn(label('10 ms',ax.c2p(10,0)[0],2.55,GREEN)),run_time=.5)
        self.at('it starts from')
        tail=float(epsp(15)); p=ax.c2p(15,tail); q=ax.c2p(18,float(epsp(18)+epsp(18,15)))
        self.play(Create(curve(ax,x,epsp(x)+epsp(x,15))),Create(DashedLine(p,q,color=GREY)),FadeIn(Dot(p,color=YELLOW)),FadeIn(label('starts here (the tail)',2,-.8,YELLOW)),run_time=1.1)
        self.add(Line(p,[-.3,-.8,0],color=TEXT,stroke_width=4))
        self.at('That is temporal summation'); self.play(FadeIn(heading('Temporal summation')),run_time=.4); self.finish()

class S10Predict(SpokenScene):
    def construct(self):
        aa,bb,stage=panels(); self.add(aa,bb,stage[4])
        info=label('Two pulses • 10 ms apart',0,-3.3,GREEN)
        self.at('Two brief'); self.play(FadeIn(stage[3]),FadeIn(info),run_time=.4)
        self.at('Each jumps the voltage'); self.play(Transform(info,label('0.4 pC each → 2 mV jumps',0,-3.3,GREEN)),run_time=.4)
        self.at('Cell A has'); self.play(FadeIn(stage[2][0]),run_time=.3)
        self.at("Cell B's is"); self.play(FadeIn(stage[2][1]),run_time=.3)
        self.at('Which ends higher')
        self.play(FadeOut(info),run_time=.15)
        self.play(FadeIn(label(QUESTION,0,-3.3,TEXT,30)),run_time=.2)
        self.finish()

class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        aa,bb,stage=panels(); self.add(stage,label(QUESTION,0,-3.3,TEXT,30))
        card=RoundedRectangle(width=8.8,height=1.7,fill_color=BG,fill_opacity=.96,stroke_color=TEAL).move_to([0,.2,0])
        self.add(card,label('Pause the video and predict',0,.55,TEAL,38))
        track=Line([-3.7,-.3,0],[3.7,-.3,0],color=GREY,stroke_width=12)
        progress=Line([-3.7,-.3,0],[-3.69,-.3,0],color=TEAL,stroke_width=12)
        self.add(track,progress)
        self.play(progress.animate.put_start_and_end_on([-3.7,-.3,0],[3.7,-.3,0]),run_time=5,rate_func=linear)

class S12RevealA(SpokenScene):
    def construct(self):
        aa,bb,stage=panels(); self.add(stage)
        self.at('Cell A'); self.play(Indicate(stage[2][0],color=YELLOW),run_time=.4)
        self.at('After'); x=np.linspace(0,10,120)
        self.play(Create(curve(aa,np.r_[0,0,x[1:]],np.r_[0,2,2*np.exp(-x[1:]/20)])),run_time=1)
        self.at('has decayed only')
        p=aa.c2p(10,2*np.exp(-.5)); a=aa.c2p(10,0)
        self.play(Create(span(a,p,GREEN).set_stroke(width=2)),FadeIn(label('1.2 mV left',p[0]+1.12,(a[1]+p[1])/2,GREEN,26)),FadeIn(label('61%',-2.2,-.55,YELLOW,30)),run_time=.4)
        self.at('The second lands'); self.play(Create(pulse_trace(aa,20)),FadeIn(formula(20,-3.25)),FadeIn(label('3.21 mV',-2.1,1.8,YELLOW,32)),run_time=.7); self.finish()

class S13RevealB(SpokenScene):
    def construct(self):
        aa,bb,stage=panels(); self.add(stage,pulse_trace(aa,20),formula(20,-3.25),label('3.21 mV',-2.1,1.8,YELLOW,32))
        self.at("Cell B's first"); x=np.linspace(0,10,120)
        self.play(Create(curve(bb,np.r_[0,0,x[1:]],np.r_[0,2,2*np.exp(-x[1:]/10)])),run_time=1)
        self.at('has fallen to about'); self.play(FadeIn(label('37% remains',4,.1,YELLOW,26)),run_time=.4)
        self.at('So cell A ends'); self.play(Create(pulse_trace(bb,10)),FadeIn(formula(10,2.75)),FadeIn(label('2.74 mV',3.45,1.95,YELLOW,32)),run_time=.6)
        self.at('and cell B under')
        p=aa.c2p(10,2+2*np.exp(-.5)); q=bb.c2p(10,2+2*np.exp(-1)); edge=5.65
        self.play(Create(VGroup(DashedLine(p,[edge,p[1],0],color=GREY,stroke_opacity=.5),DashedLine(q,[edge,q[1],0],color=GREY,stroke_opacity=.5),span(np.array([edge,p[1],0]),np.array([edge,q[1],0]),YELLOW))),FadeIn(VGroup(label('0.47 mV',edge-1.1,(p[1]+q[1])/2,YELLOW,26),label('A higher',edge-1.1,(p[1]+q[1])/2-.46,YELLOW,24))),run_time=.5); self.finish()

class S14Rule(SpokenScene):
    def construct(self):
        aa,bb,stage=panels(); self.add(stage,pulse_trace(aa,20),pulse_trace(bb,10))
        card=RoundedRectangle(width=8.8,height=2.45,fill_color=BG,fill_opacity=.98,stroke_color=GREY).move_to([0,-.35,0])
        self.add(card)
        self.at('A longer tau'); self.play(FadeIn(label('longer τ → longer tail',0,.3,YELLOW,36)),run_time=.5)
        self.at('and that means'); self.play(FadeIn(label('→ more summation',0,-.7,YELLOW,36)),run_time=.5)
        self.at('Remember cell B'); self.play(Create(SurroundingRectangle(VGroup(bb,stage[2][1]),color=GOLD,buff=.17).set_z_index(-1)),FadeIn(chip('Remember B',GOLD,32).move_to([3,-3.25,0])),run_time=.5); self.finish()

class S15Space(SpokenScene):
    def construct(self):
        self.add(neuron(True)); head=heading('From dendrite to soma')
        self.at('Now distance'); self.play(FadeIn(head),run_time=.3)
        self.at('Most synapses sit')
        self.play(FadeIn(VGroup(synapse(-4.5),Dot([-.2,2.4,0],.14,color=GREEN),Dot([-3.1,2.5,0],.14,color=GREEN),Dot([4.6,.5,0],.14,color=GREEN))),Transform(head,heading('Most inputs sit on dendrites')),run_time=.6); self.finish()

class S16Leak(SpokenScene):
    def construct(self):
        cell=neuron(True); cell[3].move_to([-.6,-2.55,0])
        self.add(cell,synapse(-4.5))
        self.at('Current entering a dendrite')
        arrows=VGroup(*[Arrow([x,-.65,0],[x+1.3,-.65,0],color=GREEN,buff=0,stroke_width=w,max_tip_length_to_length_ratio=.2) for x,w in [(-4,12),(-1.4,8),(1.2,4)]])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=.35),run_time=1.4)
        self.at('But some leaks out')
        self.play(LaggedStart(*[GrowArrow(Arrow([x,-1.25,0],[x,-1.25-l,0],color=GREEN,buff=0,stroke_width=w)) for x,l,w in [(-3.5,.55,3),(-.5,1,5),(2.3,1.5,8)]],lag_ratio=.25),FadeIn(label('leak across membrane',.4,-3.25,GREEN)),run_time=1); self.finish()

class S17Shrink(SpokenScene):
    def construct(self):
        self.add(neuron(),heading('Long, uniform, passive dendrite'))
        xs=np.linspace(-5,4.6,4)
        self.at('In a long'); self.wait(.4)
        bars=[]
        for i,x in enumerate(xs):
            h=3*np.exp(-i*.5); bars.append(VGroup(Line([x,-.05,0],[x,-.05+h,0],color=YELLOW,stroke_width=13),label(f'{100*np.exp(-i*.5):.0f}%',x,h+.3,YELLOW,30)))
        self.at('a steady voltage change'); self.play(Create(bars[0]),run_time=.5)
        self.at('shrinks by the same fraction'); self.play(LaggedStart(*[Create(b) for b in bars[1:]],lag_ratio=.65),run_time=1.6)
        self.at('over each equal stretch'); self.play(Create(VGroup(*[span(np.array([xs[i],-2.65,0]),np.array([xs[i+1],-2.65,0])) for i in range(3)])),FadeIn(label('equal distance → same fraction left',0,-3.35,YELLOW)),run_time=.5); self.finish()

class S18Lambda(SpokenScene):
    def construct(self):
        ax=axes((0,2,1),(0,1.1,.5),10.2,4.7,(.1,.65))
        self.add(ax,ticks(ax,[0,2],[0,1],xunit='λ',ylabel='voltage / V₀'),Line([-5,-2.6,0],[5.2,-2.6,0],color=BLUE,stroke_width=12),label('synapse',-5,-3, GREEN,26),label('dendrite',0,-3,BLUE,26))
        self.at('The length constant'); x=np.linspace(0,2,200); self.play(Create(curve(ax,x,np.exp(-x))),run_time=.9)
        self.at('is the distance'); p=ax.c2p(1,np.exp(-1))
        self.play(Create(VGroup(DashedLine(ax.c2p(1,0),p,color=YELLOW),DashedLine(ax.c2p(0,np.exp(-1)),p,color=GREY),Dot(p,color=YELLOW))),run_time=.5)
        self.at('it falls to'); self.play(FadeIn(label('37%',p[0]+.65,p[1]+.3,YELLOW,32)),FadeIn(label('1 λ',p[0],-2.05,YELLOW,26)),FadeIn(exp_text('V(x) = V₀ × ','−x/λ','',1.7,2.6,34)),run_time=.4); self.finish()

class S19Example(SpokenScene):
    def construct(self):
        self.add(neuron(),heading('Different example: λ = 500 µm'))
        x=-4.4
        self.at('Put a synapse'); self.play(FadeIn(VGroup(Arrow([-5.8,1.4,0],[x,-.05,0],color=GREEN,buff=0),label('synapse',-5.25,1.85,GREEN,26))),run_time=.4)
        self.at('half a length constant'); self.play(Create(span(np.array([x,-2.7,0]),np.array([4.6,-2.7,0]),GREY)),FadeIn(label('250 µm = 0.5 λ',.2,-3.2,GREY,30)),run_time=.5)
        b1=Line([x,-.05,0],[x,2.15,0],color=YELLOW,stroke_width=14)
        b2=Line([4.6,-.05,0],[4.6,-.05+2.2*np.exp(-.5),0],color=YELLOW,stroke_width=14)
        self.play(Create(b1),run_time=.4)
        self.at('About'); self.play(TransformFromCopy(b1,b2),FadeIn(label('61% steady',4.4,1.8,YELLOW,30)),run_time=.65)
        self.at('of its steady depolarization'); self.play(FadeIn(exp_text('','−0.5',' = 0.61',0,2.45,34)),run_time=.4); self.finish()

def filtered_epsp():
    """Passive cable PDE in normalized units: du/dt = d²u/dx² − u.

    Boundary is the same local brief EPSP; far boundary at 5λ is at rest.
    Explicit finite differences: dx=.05λ, dt=.0008τ (< dx²/2).
    Read out 0.5λ away; this computes attenuation and broadening, no sketched curve.
    """
    dx,dt=.05,.0008
    u=np.zeros(101)
    ts=np.arange(0,5,dt)
    local=epsp(ts*20,5)
    remote=[]
    for v in local:
        u[0]=v
        u[1:-1]+=dt*((u[:-2]-2*u[1:-1]+u[2:])/dx**2-u[1:-1])
        remote.append(u[10])
    return ts*20,local,np.array(remote)


class S20Brief(SpokenScene):
    def construct(self):
        ax=axes((0,100,20),(0,3.3,1),10.5,5,(.25,-.05))
        t,local,remote=filtered_epsp()
        self.add(ax,ticks(ax,[0,20,40,60,80],[0,1,2,3]),heading('Brief EPSP over the same 0.5 λ'),label('Illustrative passive-cable amplitudes',0,-3.4,GREY,26))
        self.at('A brief'); self.play(Create(curve(ax,t[::8],local[::8])),FadeIn(label('at synapse',-2.4,1.8,YELLOW)),run_time=.6)
        self.at('loses more'); r=curve(ax,t[::8],remote[::8],TEAL)
        self.play(Create(r),run_time=.65)
        self.at('because capacitance'); k=np.argmax(remote); p=ax.c2p(t[k],remote[k])
        self.play(FadeIn(label('at soma: smaller, broader',2,-.65,TEAL)),Create(Line(p,[-.9,-.65,0],color=TEAL)),run_time=.4); self.finish()

class S21Spatial(SpokenScene):
    def construct(self):
        soma=Circle(1.2,color=BLUE,fill_opacity=.12).move_to([3.7,0,0])
        ends=[np.array([-5,1.0,0]),np.array([-.8,-2.4,0])]; roots=[np.array([2.6,.65,0]),np.array([3.3,-.65,0])]
        self.add(soma,VGroup(*[Line(a,b,color=BLUE,stroke_width=16) for a,b in zip(ends,roots)]),label('soma',3.7,-1.65,BLUE),label('far',-3.4,2.9,BLUE,32),label('near',.5,-2.45,BLUE,32))
        self.at('Adding inputs at different places')
        self.play(FadeIn(VGroup(*[Dot(a,.16,color=GREEN) for a in ends])),run_time=.3)
        # Equal local heights; attenuate by exp(-distance/lambda) during travel.
        # Yellow is the far contribution; teal identifies the near contribution at soma.
        colors=(YELLOW,TEAL); local_h=2.2
        bumps=VGroup(*[Line(a,a+UP*local_h,color=c,stroke_width=18)
                       for a,c in zip(ends,colors)])
        self.add(bumps)
        mid=[(a+r)/2 for a,r in zip(ends,roots)]
        half=[Line(m,m+UP*local_h*np.exp(-d/2),color=c,stroke_width=18)
              for m,d,c in zip(mid,(1.,.5),colors)]
        self.play(*[Transform(b,h) for b,h in zip(bumps,half)],run_time=1.3,rate_func=linear)
        self.at('is spatial summation')
        arrived=[Line(r,r+UP*local_h*np.exp(-d),color=c,stroke_width=18)
                 for r,d,c in zip(roots,(1.,.5),colors)]
        self.play(FadeIn(heading('Spatial summation')),*[Transform(b,h) for b,h in zip(bumps,arrived)],run_time=1.1,rate_func=linear)
        parts=VGroup(); base=np.array([3.7,-.6,0])
        for b,d,c in zip(bumps,(1.,.5),colors):
            h=local_h*np.exp(-d)
            seg=Rectangle(width=.48,height=h,stroke_width=0,fill_color=c,fill_opacity=.9).move_to(base+UP*h/2)
            self.play(ReplacementTransform(b,seg),run_time=.35); parts.add(seg); base=base+UP*h
        self.add(label('sum',5.25,2.1,TEXT,28),
                 label('far',5.15,-.2,YELLOW,26),label('near',5.15,1.05,TEAL,26),
                 Line([4,-.2,0],[4.65,-.2,0],color=YELLOW),Line([4,1.05,0],[4.65,1.05,0],color=TEAL))
        # Scale is relative to the common local voltage change at each synapse.
        scale_x=3.12
        self.add(Line([scale_x,-.6,0],[scale_x,-.6+local_h,0],color=GREY,stroke_width=2))
        for value in (0,.5,1):
            yy=-.6+local_h*value
            self.add(Line([scale_x-.08,yy,0],[scale_x+.08,yy,0],color=GREY,stroke_width=2),label(str(value),2.65,yy,GREY,22).add_background_rectangle(color=BG,opacity=1,buff=.03))
        self.add(label('× local',3.1,2.1,GREY,22))
        self.at('For the same local change'); self.play(FadeIn(label('same local change • other things equal',0,-3.35,GREY,26)),run_time=.3)
        self.at('inputs near the soma'); self.play(Indicate(parts[1],color=TEAL),run_time=.5)
        self.at('or on dendrites'); self.play(FadeIn(label('longer λ → less loss',-2.8,-.1,YELLOW,30)),run_time=.4); self.finish()

class S22Takeaway(SpokenScene):
    def construct(self):
        a=axes((0,60,20),(0,1,.5),4.7,4.8,(-3.25,.15)); b=axes((0,2,1),(0,1,.5),4.7,4.8,(3,.15))
        self.add(a,b,ticks(a,[0,20,40,60],ylabel='',xunit=''),ticks(b,[0,1,2],ylabel='',xunit=''),label('time (ms)',-3.25,-2.95,GREY),label('distance / λ',3,-2.95,GREY),heading('τ and λ decide how much of each input is left.'))
        self.at('Time and distance decide'); x=np.linspace(0,60,150); z=np.linspace(0,2,150)
        self.play(Create(curve(a,x,np.exp(-x/20))),Create(curve(b,z,np.exp(-z))),run_time=.7)
        self.at('how much of each input'); self.play(FadeIn(label('τ: time',-2.8,2,YELLOW,34)),FadeIn(label('λ: distance',3.5,2,YELLOW,34)),run_time=.4)
        self.at('The balance point decides')
        card=Rectangle(width=12.3,height=1.15,fill_color=BG,fill_opacity=1,stroke_color=GREY).move_to([0,-1.35,0])
        self.play(FadeIn(card),FadeIn(label('The balance point decides what the inputs add up to.',0,-1.35,TEXT,30)),run_time=.5); self.finish()

class S23End(EndCard):
    LINE='The balance point decides what the inputs add up to.'
