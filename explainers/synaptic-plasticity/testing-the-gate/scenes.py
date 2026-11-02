"""Testing the Gate: review revision.
COLOR MAP: YELLOW glutamate; BLUE everyday EPSP; PURPLE NMDA;
ORANGE Mg²⁺; TEAL Ca²⁺; PINK voltage/current; GREEN LTP;
RED failure; TEXT input/APV/EGTA; GOLD questions; GREY context.
All curves are models, never historical recordings. Outcome model:
R(t)=1+A H(t-t_train), A=0 (failed induction), A=1 (LTP illustration).
EPSP model: f(t)=-u exp(1-u), u=max(0,(t-1)/1.6).
Agonist response uses the same alpha-function envelope, positive polarity;
APV multiplies its amplitude by zero. No fitted kinetics or invented units.
Stimulus ticks and current steps are discrete event/rectangular command models.
"""
import json
import os
from pathlib import Path
import numpy as np
from bp_style import *

PURPLE='#B58CD9'
ORANGE='#F29E4C'
PINK='#E58FC0'


class SpokenScene(SpokenScene):
    """Use actual cue start times; shared sync.log logs BEFORE waiting.
    Keep the pipeline untouched and remove its cumulative 0.4 s scene tails.
    Frame rounding contributes at most one 15-fps frame per scene.
    """
    def at(self, phrase, lead=0, nth=0):
        target=self.t_of(phrase,nth)-lead
        if target-self.elapsed() > .001:
            self.wait(target-self.elapsed())
        lateness=self.elapsed()-target
        if lateness > .15:
            raise ValueError(f'Late cue {phrase}: {lateness:.3f}s')
    def finish(self):
        if self.narration_s > self.elapsed():
            self.wait(self.narration_s-self.elapsed())


def lab(s,x=0,y=3.15,c=TEXT,size=30):
    return T(s,size,c).move_to([x,y,0])


def appear(scene,*mobs,rt=.35):
    scene.play(*[FadeIn(m) for m in mobs],run_time=rt)


def check(x,y,k=1):
    return VMobject(color=GREEN,stroke_width=7).set_points_as_corners(
        [[x-.25*k,y,0],[x-.05*k,y-.2*k,0],[x+.35*k,y+.3*k,0]])


def ticks(x,y,n=12,gap=.25,h=.35):
    return VGroup(*[Line([x+(i-(n-1)/2)*gap,y-h/2,0],
                        [x+(i-(n-1)/2)*gap,y+h/2,0],color=TEXT,stroke_width=3) for i in range(n)])


def formula():
    return VGroup(chip('glutamate',YELLOW,30),T('+',32),chip('depolarization',PINK,30),
                  T('→',34),chip('Ca²⁺ entry',TEAL,30)).arrange(RIGHT,buff=.2)


def electrode(x,y,c=TEXT):
    # Tapered electrode; the tip is the first vertex and touches its target.
    return Polygon([x,y,0],[x+.65,y+1.45,0],[x+.95,y+1.45,0],
                   color=c,fill_color=BG,fill_opacity=1,stroke_width=4)


def slice_dish(electrodes=False):
    dish=VGroup(Ellipse(width=11.6,height=5.35,color=GREY,fill_opacity=.04),
                VMobject(color=GREY).set_points_as_corners([[5.8*np.cos(t),2.675*np.sin(t)-.16,0] for t in np.linspace(PI,2*PI,101)]))
    tissue=RoundedRectangle(width=9.2,height=3.7,corner_radius=.9,color=GREY,fill_opacity=.1)
    ca3=chip('CA3',GREY,34).move_to([-3.35,-.35,0])
    ca1=chip('CA1',GREY,34).move_to([3.25,-.35,0])
    path=Arrow(ca3.get_right(),ca1.get_left(),color=TEXT,buff=.1,stroke_width=6)
    name=lab('Schaffer collaterals',0,-1.35,TEXT,28)
    g=VGroup(dish,tissue,ca3,ca1,path,name)
    if electrodes:
        g.add(electrode(-1.7,-.35),lab('stimulate',-2.1,2.18,TEXT,26),
              electrode(3.25,.03,TEAL),lab('record',4.8,2.18,TEAL,26))
    return g


def cell(x=-3.3,y=-.25,w=3.8,h=3.4,c=GREY):
    body=RoundedRectangle(width=w,height=h,corner_radius=.75,color=c,fill_opacity=.08).move_to([x,y,0])
    return VGroup(body,lab('CA1 cell',x,y-h/2+.5,GREY,28))


def meter(x,y,name='soma',value='−90 mV',w=3.2):
    box=RoundedRectangle(width=w,height=1.45,corner_radius=.16,color=PINK,fill_opacity=.07).move_to([x,y,0])
    rail=Line([x-w/2+.25,y-.4,0],[x+w/2-.25,y-.4,0],color=GREY,stroke_width=5)
    needle=Line([x-w/2+.45,y-.57,0],[x-w/2+.45,y-.23,0],color=PINK,stroke_width=6)
    return VGroup(box,lab(name,x,y+.38,PINK,26),lab(value,x,y-.02,PINK,28),rail,needle)


def held_cell():
    return VGroup(cell(),electrode(-3.6,.1,PINK),meter(-3.3,2.2))


def outcome(x=0,y=-.25,w=10.6,h=4.65,up=False,event='train',base_name='baseline',labels=True):
    # Coordinates are a literal evaluation of R(t)=1+A H(t-0.32).
    left=x-w/2; bottom=y-h/2
    def p(t,r): return np.array([left+w*t,bottom+h*r/2.6,0])
    axes=VGroup(Line(p(0,0),p(1,0),color=GREY),Line(p(0,0),p(0,2.6),color=GREY))
    trace=VMobject(color=GREEN if up else TEXT,stroke_width=6).set_points_as_corners(
        [p(t,1+(1 if up and t>=.32 else 0)) for t in (0,.31999,.32,1)])
    baseline=DashedLine(p(0,1),p(1,1),color=GREY,stroke_opacity=.6)
    mark=DashedLine(p(.32,0),p(.32,2.4),color=GREY,stroke_opacity=.5)
    text=VGroup()
    if labels:
        yl=lab('synaptic response (normalised)',left+3,y+h/2+.3,GREY,26)
        text.add(yl,lab('1',left-.27,p(0,1)[1],GREY,26),
                 lab(base_name,left+w-.95,p(0,1)[1]+.35,GREY,26),
                 lab(event,left+w*.32,bottom-.35,TEXT,26),
                 lab('time →',left+w-.55,bottom-.35,GREY,26))
    return VGroup(axes,baseline,mark,text),trace


def prediction():
    a,tr=outcome(2.5,-.2,6.4,3.65)
    # Compact panel gets a concise y label next to its axis.
    a[3][0].become(lab('normalised response',1.85,1.95,GREY,26))
    return VGroup(held_cell(),a,lab('?',2.5,.15,GOLD,86),
                  lab('Will that cell’s input potentiate?',0,-3.1,GOLD,44))


def pulse_steps(x=-2.8,y=0,w=5.6):
    # Sparse ticks fall within each rectangular depolarizing command.
    centers=np.linspace(x-w/2+.5,x+w/2-.5,4)
    tk=VGroup(*[Line([a,y+.6,0],[a,y+1.1,0],color=TEXT,stroke_width=4) for a in centers])
    st=VMobject(color=PINK,stroke_width=5)
    pts=[[x-w/2,y-.7,0]]
    for a in centers:
        pts.extend([[a-.35,y-.7,0],[a-.35,y,0],[a+.35,y,0],[a+.35,y-.7,0]])
    pts.append([x+w/2,y-.7,0]);st.set_points_as_corners(pts)
    return tk,st


def reverse_stage():
    c=cell(3.7,-.3,3.6,3.6)
    pip=electrode(3.2,.25,PINK)
    tk,st=pulse_steps()
    path=Arrow([-5.9,.85,0],[1.8,.85,0],buff=0,color=GREY,stroke_width=3)
    return c,pip,tk,st,path


def choice():
    cards=[]
    for x,title in [(-3.15,'frequency'),(3.15,'coincidence')]:
        box=RoundedRectangle(width=5.8,height=4.9,corner_radius=.22,color=GREY).move_to([x,-.25,0])
        title_m=lab(title,x,1.65,TEXT,34)
        tk=ticks(x,.65,14 if x<0 else 4,.29 if x<0 else 1.05,.5)
        if x<0:
            step=Line([x-2,-.8,0],[x+2,-.8,0],color=GREY)
            caption=lab('fast input',x,-1.8,TEXT,28)
        else:
            step=VMobject(color=PINK,stroke_width=5).set_points_as_corners(
                [[x-2.2,-.9,0],[x-1.9,-.9,0],[x-1.9,-.05,0],[x+1.9,-.05,0],[x+1.9,-.9,0],[x+2.2,-.9,0]])
            caption=lab('input during depolarization',x,-1.8,PINK,26)
            # Faint guides visually connect the input events to the depolarizing window.
            for tick in tk:
                tick.add(Line(tick.get_bottom(),[tick.get_x(),-.05,0],color=PINK,stroke_opacity=.35))
        cards.append(VGroup(box,title_m,tk,step,caption))
    q=lab('Fast input, or depolarization\nat the moment of input?',0,3.0,GOLD,44)
    return *cards,q


def spine():
    # One connected channel block with a visible dark pore, not two floating bars.
    body=RoundedRectangle(width=5.25,height=4.35,corner_radius=1,color=GREY,fill_opacity=.08).move_to([-3.1,-.6,0])
    mem=VGroup(Line([-5.72,1.45,0],[-3.85,1.45,0],color=GREY,stroke_width=12),
               Line([-2.35,1.45,0],[-.48,1.45,0],color=GREY,stroke_width=12))
    channel=RoundedRectangle(width=1.5,height=1.05,corner_radius=.18,color=PURPLE,fill_opacity=.35).move_to([-3.1,1.45,0])
    pore=Rectangle(width=.34,height=1.04,stroke_width=0,fill_color=BG,fill_opacity=1).move_to(channel)
    nm=lab('NMDA',-4.75,.45,PURPLE,28)
    leader=Line(nm.get_right(),[-3.8,1,0],color=PURPLE)
    return VGroup(body,mem,channel,pore,nm,leader,lab('active spine',-3.1,-2.2,GREY,28))


def alpha(t):
    u=max(0,(t-1)/1.6)
    return u*np.exp(1-u)


def evoked_panel(kind='field',x=0,y=-.2,w=10.2,h=4.3):
    # Plot origin at the left edge, independently of deflection polarity.
    left=x-w/2; bottom=y-h/2
    zero=bottom+h*.8 if kind=='field' else bottom+h*.18
    sign=-1 if kind=='field' else 1
    def p(t,v): return [left+w*t/10,zero+sign*h*.65*v,0]
    ax=VGroup(Line([left,bottom,0],[left,bottom+h,0],color=GREY),
              Line(p(0,0),p(10,0),color=GREY),lab('response',left+1,bottom+h+.25,GREY,28),
              lab('time →',left+w-.6,bottom-.3,GREY,28))
    pts=[p(t,alpha(t)) for t in np.linspace(0,10,301)]
    before=VMobject(color=GREY,stroke_width=10).set_points_as_corners(pts)
    after=VMobject(color=BLUE if kind=='field' else PURPLE,stroke_width=4).set_points_as_corners(
        pts if kind=='field' else [p(t,0) for t in np.linspace(0,10,101)])
    legends=VGroup(VGroup(Line(LEFT*.3,RIGHT*.3,color=GREY,stroke_width=9),T('before APV',28,GREY)).arrange(RIGHT,buff=.2),
                   VGroup(Line(LEFT*.3,RIGHT*.3,color=BLUE if kind=='field' else PURPLE,stroke_width=4),T('after APV',28,BLUE if kind=='field' else PURPLE)).arrange(RIGHT,buff=.2)).arrange(RIGHT,buff=.8).move_to([x,2.35 if h>3 else y+h/2+.65,0])
    return ax,before,after,legends


class S00Title(TitleCard):
    LESSON='Synaptic Plasticity'
    TITLE='Testing the Gate'
    def construct(self):
        self.add(lab('BIOCHEMISTRYPEDIA',0,1.6,TEAL,26),lab(self.LESSON.upper(),0,.85,GREY,28))
        self.play(FadeIn(lab(self.TITLE,0,-.15,TEXT,54)),Create(Line([-1.2,-1,0],[1.2,-1,0],color=GOLD)),run_time=.8)
        self.wait(max(.01,self.narration_s-self.elapsed()))


class S01Question(SpokenScene):
    def construct(self):
        f=formula().move_to([0,.45,0])
        box=RoundedRectangle(width=12.1,height=1.9,corner_radius=.2,color=GOLD).move_to(f)
        self.add(box,f)
        self.at('predicts experiments')
        bench=VGroup(Line([-6,-1.45,0],[6,-1.45,0],color=GREY,stroke_width=8),
                     Line([-5,-1.45,0],[-5,-3.2,0],color=GREY,stroke_width=6),
                     Line([5,-1.45,0],[5,-3.2,0],color=GREY,stroke_width=6),
                     Ellipse(width=4.8,height=1,color=GREY,fill_opacity=.12).move_to([0,-1.1,0]),
                     RoundedRectangle(width=3.3,height=.5,corner_radius=.2,color=GREY).move_to([0,-1.05,0]))
        appear(self,bench)
        self.at('How would you test');appear(self,lab('How would you test the two-signal gate?',0,2.7,GOLD,36))
        self.finish()


class S02Slice(SpokenScene):
    def construct(self):
        g=slice_dish();self.add(g.copy().scale(.42).move_to([0,-1.1,0]))
        self.at('Work in a slice');self.play(Transform(self.mobjects[0],g),run_time=.8)
        self.at('rat hippocampus');appear(self,lab('Rat hippocampal slice'))
        self.at('Stimulate the');appear(self,electrode(-1.7,-.35),lab('stimulate',-2.1,2.18,TEXT,26))
        self.play(ShowPassingFlash(g[4].copy().set_color(YELLOW),time_width=.6),run_time=.65)
        self.at('record from');appear(self,electrode(3.25,.03,TEAL),lab('record',4.8,2.18,TEAL,26));self.finish()


class S03Setup(SpokenScene):
    def construct(self):
        d=slice_dish(True);self.add(d)
        self.at('Give the input')
        c=cell();outline=slice_dish()[1].copy().set_opacity(.18).stretch_to_fit_width(12).stretch_to_fit_height(5.4)
        self.play(FadeOut(d),FadeIn(outline),FadeIn(c),run_time=.65)
        self.at('usual fast train')
        tk=ticks(1.8,.4,20,.27,.5);path=Arrow([4.8,.4,0],[-1.3,.4,0],color=GREY,buff=0)
        appear(self,tk,path,rt=.25)
        flashes=[ShowPassingFlash(Line([4.7,.4,0],[-1.5,.4,0],color=TEXT,stroke_width=5),time_width=.12) for _ in range(20)]
        self.play(LaggedStart(*flashes,lag_ratio=.06),run_time=.95)
        self.at('pulses per second');appear(self,lab('100 pulses per second',2.1,1.4,TEXT,30))
        self.at('But hold');appear(self,electrode(-3.6,.1,PINK))
        self.at('very negative');appear(self,meter(-3.3,2.2));self.play(c[0].animate.set_stroke(PINK),run_time=.3)
        self.at('near minus');self.play(Indicate(self.mobjects[-1],color=PINK),run_time=.5);self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        p=prediction();self.add(p[0],p[1])
        self.at('input potentiate');appear(self,p[2],p[3]);self.finish()


class S05Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(prediction());self.wait(5)


class S06Reveal(SpokenScene):
    def construct(self):
        g=spine();self.add(g)
        self.at('if the current');appear(self,meter(3.3,2.75,'soma','−90 mV',4.5).scale(.85))
        self.at('active spines negative');appear(self,meter(3.3,1.35,'active spine','strongly negative',4.5).scale(.85),
             lab('Assume effective hyperpolarization\nat the active spines',0,-3.25,TEXT,26))
        self.at('magnesium block')
        mg=Dot([-3.1,1.5,0],radius=.18,color=ORANGE)
        mgl=lab('Mg²⁺',-1.15,2.3,ORANGE,28)
        appear(self,mg,mgl,Line(mgl.get_left(),mg.get_center()+RIGHT*.2,color=ORANGE))
        self.at('glutamate arrives')
        dot=Dot([-5.2,2.6,0],radius=.16,color=YELLOW);gl=lab('glutamate',-4.8,3.2,YELLOW,28)
        self.add(dot);appear(self,gl,rt=.2);self.play(dot.animate.move_to([-3.55,2.13,0]),run_time=.5)
        self.at('without the second')
        ax,tr=outcome(3.3,-1.5,6.0,2.65,labels=False)
        ax.add(lab('synaptic response (normalised)',3.3,.24,GREY,26),
               lab('1',.05,-1.81,GREY,26),lab('time →',5.65,-3.08,GREY,26),
               lab('No LTP',3.4,-.8,RED,36))
        appear(self,ax,tr);self.finish()


class S07Malinow(SpokenScene):
    def construct(self):
        ax,tr=outcome(1.6,-.3,8.5,4.65)
        self.add(ax,cell(-4.8,.1,2.7,2.65),meter(-4.8,2.25,'soma','−90 mV',2.7))
        self.at('In');year=lab('1986',1.3,3.2,TEXT,32);appear(self,year)
        self.at('found that');self.play(Transform(year,lab('Malinow and Miller · 1986',1.3,3.2,TEXT,32)),run_time=.25)
        self.at('hyperpolarizing the cell')
        tk=ticks(-4.8,-1.75,8,.27);appear(self,tk)
        self.play(Indicate(self.mobjects[2],color=PINK),run_time=.4)
        self.at('prevented');self.play(Create(tr),run_time=.65)
        appear(self,lab('No LTP under their conditions',1.8,.7,RED,28));self.finish()


class S08Reverse(SpokenScene):
    def construct(self):
        c,pip,tk,st,path=reverse_stage()
        self.add(c,pip,path,lab('Reverse the test',0,3.15,TEXT,36))
        self.at('Slow input');appear(self,tk,lab('slow input',-2.8,1.9,TEXT,28))
        dot=Dot([-5.6,.85,0],color=YELLOW);self.add(dot)
        self.play(dot.animate.move_to([1.85,.85,0]),run_time=.3);self.remove(dot)
        self.at('too weak');alone=lab('alone: no potentiation',-2.8,-1.7,GREY,28);appear(self,alone)
        self.at('was paired with current');self.play(FadeOut(alone),Create(st),GrowArrow(Arrow([0,-.7,0],[3.2,.25,0],color=PINK,buff=.05,stroke_width=4)),run_time=.65)
        self.at('depolarized the cell');appear(self,lab('depolarizing current',0,-2.9,PINK,30))
        self.play(c[0].animate.set_stroke(PINK).set_fill(PINK,.12),run_time=.4);self.finish()


class S09Reverse2(SpokenScene):
    def construct(self):
        tk,st=pulse_steps(0,2,6)
        self.add(tk,st,lab('paired input + depolarizing current',0,3.55,PINK,26))
        ax,tr=outcome(0,-.55,10.7,3,up=True,event='pairing')
        ax[3][0].become(lab('normalised response',-3.2,.95,GREY,26))
        self.add(ax)
        self.at('produced');self.play(Create(tr),run_time=.6)
        appear(self,lab('LTP',4.4,.65,GREEN,32),rt=.25)
        self.at('Two groups reported')
        appear(self,lab('Kelso, Ganong and Brown · 1986',0,-3.2,TEXT,26),
               lab('Wigström and colleagues · 1986',0,-3.65,TEXT,26),rt=.3);self.finish()


class S10Predict2(SpokenScene):
    def construct(self):
        a,b,q=choice();self.add(a[0],b[0])
        self.at('which matters');appear(self,q)
        self.at('How fast the input');appear(self,VGroup(*a[1:]))
        self.at('whether the cell');appear(self,VGroup(*b[1:]));self.finish()


class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(*choice());self.wait(5)


class S12Reveal2(SpokenScene):
    def construct(self):
        a,b,q=choice();self.add(a,b,q)
        self.at('Coincidence');self.play(b[0].animate.set_stroke(GREEN,width=6).set_fill(GREEN,.08),run_time=.5)
        self.at('High frequency');appear(self,lab('high frequency not required',0,-3.35,GREEN,28))
        self.at('A fast train')
        # Leaky summation model: dV/dt=-V/tau + sum(delta(t-ti)).
        ts=np.linspace(0,10,301); events=np.linspace(1,7,14)
        v=np.array([sum(np.exp(-(t-ti)/1.4) for ti in events if t>=ti) for t in ts])
        v=.85*v/max(v)
        bump=VMobject(color=PINK,stroke_width=5).set_points_as_corners(
            [[-5.35+4.4*t/10,-.8+vv,0] for t,vv in zip(ts,v)])
        self.play(Transform(a[3],bump),Transform(a[4],lab('supplies depolarization',-3.15,-1.8,PINK,26)),run_time=1)
        self.finish()


class S13TwoMore(SpokenScene):
    def construct(self):
        rows=VGroup(*[VGroup(Square(.7,color=c),T(s,38,c)).arrange(RIGHT,buff=.5) for s,c in
            [('block the receptor',PURPLE),('block the calcium',TEAL),('withhold depolarization',PINK)]]).arrange(DOWN,aligned_edge=LEFT,buff=1.1).move_to([0,-.2,0])
        ck=check(*rows[2][0].get_center()[:2])
        self.add(rows,ck,lab('Test the gate',0,3.2,TEXT,38))
        self.at('You have just seen');self.play(Indicate(VGroup(rows[2],ck),color=GREEN),run_time=.6);self.finish()


class S14Apv(SpokenScene):
    def construct(self):
        d=slice_dish(True)
        d[1].stretch_to_fit_height(3.1)  # Leave a clear bath margin for the wash-in.
        d[5].shift(UP*.2)
        self.add(d)
        self.at('block the receptor');appear(self,lab('Block the NMDA receptor',0,3.2,PURPLE,34))
        self.at('In');year=lab('1983',0,-3.25,TEXT,28);appear(self,year)
        self.at('Collingridge');self.play(Transform(year,lab('Collingridge, Kehl and McLennan · 1983',0,-3.25,TEXT,28)),run_time=.3)
        self.at('applied the')
        drops=VGroup(*[chip('APV',TEXT,26).move_to([x,-2.95,0]) for x in (-1.7,0,1.7)])
        self.add(drops);self.play(*[m.animate.move_to([x,-2.1,0]) for m,x in zip(drops,(-1.7,0,1.7))],run_time=.85)
        self.at('antagonist');self.play(drops.animate.set_opacity(.6),d[1].animate.set_fill(PURPLE,.18),run_time=.4);self.finish()


class S15Apv2(SpokenScene):
    def construct(self):
        ax,bef,aft,legend=evoked_panel('agonist')
        title=lab('NMDA agonist response',0,3.25,PURPLE,34)
        self.add(ax,bef,legend[0],title)
        self.at('abolished responses');self.play(Create(aft),FadeIn(legend[1]),run_time=.6)
        fail=lab('abolished',3,.5,RED,32);appear(self,fail)
        self.at('The baseline')
        ax2,bef2,aft2,leg2=evoked_panel('field')
        self.play(FadeOut(VGroup(ax,bef,aft,legend,fail)),Transform(title,lab('field EPSP',0,3.25,BLUE,34)),run_time=.2)
        self.play(FadeIn(ax2),Create(bef2),FadeIn(leg2[0]),run_time=.4)
        self.at('was unaffected');self.play(Create(aft2),FadeIn(leg2[1]),FadeIn(lab('identical traces · model illustration',0,-3.3,TEXT,26)),run_time=.35);self.finish()


class S16Apv3(SpokenScene):
    def construct(self):
        ax,tr=outcome(-1.35,-.25,8.4,4.8,base_name='pre-train level')
        self.add(ax,lab('APV present',4.5,3.3,TEXT,34))
        # Same field EPSP parameters, overlaid before/after APV.
        mini=VGroup();left=3.25;zero=-.1
        mini.add(Line([left,-1.8,0],[left,.2,0],color=GREY),Line([left,zero,0],[6.2,zero,0],color=GREY))
        pts=[[left+2.95*t/10,zero-1.4*alpha(t),0] for t in np.linspace(0,10,201)]
        mini.add(VMobject(color=GREY,stroke_width=9).set_points_as_corners(pts),VMobject(color=BLUE,stroke_width=4).set_points_as_corners(pts),
                 lab('field EPSP',4.7,-2.1,BLUE,26),lab('before / after APV',4.7,-2.65,TEXT,26),lab('time →',5.65,-1.5,GREY,26))
        self.add(mini)
        self.at('a fast train');tk=ticks(-2.85,3.1,20,.22);appear(self,tk,rt=.25)
        self.at('no longer produced');self.play(Create(tr),run_time=.65)
        no=lab('No LTP',-.3,.4,RED,32);appear(self,no)
        self.at('needed to start');appear(self,lab('induction needs\nNMDA receptors',4.5,1.6,PURPLE,28))
        self.at('everyday response')
        everyday=lab('everyday response:\nunchanged by APV',4.65,-2.5,BLUE,28)
        self.play(ReplacementTransform(VGroup(mini[4],mini[5]),everyday),
                  Indicate(VGroup(*mini[:4]),color=BLUE,scale_factor=1.03),run_time=.35);self.finish()


class S17Egta(SpokenScene):
    def construct(self):
        c=cell(0,-.25,8.6,5.3);self.add(c)
        self.at('block the calcium');appear(self,lab('Block the calcium rise',0,3.3,TEAL,36))
        ca=VGroup(*[Dot(p,radius=.16,color=TEAL) for p in [(-2,-.2,0),(1.8,-.4,0),(1,-1.4,0)]])
        cal=lab('Ca²⁺',-2.9,-.2,TEAL,30)
        appear(self,ca,cal)
        self.at('The same year');year=lab('1983',0,-3.3,TEXT,28);appear(self,year)
        self.at('Lynch and colleagues');self.play(Transform(year,lab('Lynch and colleagues · 1983',0,-3.3,TEXT,28)),run_time=.25)
        self.at('injected the');pip=electrode(-.8,.65,TEAL);appear(self,pip,rt=.35)
        self.at('calcium buffer');buf=chip('EGTA',TEXT,28).move_to([-.8,.65,0])
        tag=lab('Ca²⁺ buffer',.1,-.65,TEAL,28)
        appear(self,buf,rt=.25)
        self.play(buf.animate.move_to([0,0,0]),run_time=.4)
        self.at('EGTA');appear(self,tag,rt=.25)
        self.at('into')
        buffers=VGroup(*[chip('EGTA',TEXT,26).move_to([-.8,.65,0]) for _ in range(2)])
        self.add(buffers);self.play(buffers[0].animate.move_to([-2,-1.2,0]),buffers[1].animate.move_to([2,.1,0]),run_time=.3)
        # Show calcium converging on the labelled buffers before it disappears.
        self.play(ca[0].animate.move_to([-2,-1.2,0]),ca[1].animate.move_to([2,.1,0]),
                  ca[2].animate.move_to([0,0,0]),run_time=.35)
        self.play(FadeOut(ca),FadeOut(cal),run_time=.3);self.finish()


class S18Egta2(SpokenScene):
    def construct(self):
        a,ta=outcome(-3.25,-.25,5.35,4.7,labels=False)
        b,tb=outcome(3.25,-.25,5.35,4.7,up=True,labels=False)
        self.add(a,lab('EGTA-filled cell',-3.25,2.8,TEAL,32),lab('normalised response',-3.25,2.2,GREY,26),lab('baseline',-1.7,-.42,GREY,26),lab('time →',-1.3,-2.95,GREY,26),lab('pairing',-4.2,-2.95,TEXT,26))
        self.at('failed at');self.play(Create(ta),run_time=.5)
        self.at('So induction needs')
        appear(self,b,lab('control cell (illustration)',3.25,2.8,GREY,28),lab('normalised response',3.25,2.2,GREY,26),
               lab('time →',5.2,-2.95,GREY,26),lab('pairing',2.2,-2.95,TEXT,26),rt=.3)
        self.play(Create(tb),run_time=.6)
        appear(self,lab('Induction needs a postsynaptic Ca²⁺ rise',0,-3.55,TEAL,30));self.finish()


class S19Trigger(SpokenScene):
    def construct(self):
        g=spine();self.add(g,lab('model illustration',-3.1,-3.3,TEXT,28))
        # A compact, explicit APV recap replaces the unsupported empty chip.
        rax,rtr=outcome(3.45,-.3,5.0,3.5,labels=False)
        recap=VGroup(rax,rtr,lab('APV: no induction',3.45,2.7,PURPLE,32),
                     lab('normalised response',3.45,1.8,GREY,26),
                     lab('post-train response\nstays at baseline',3.45,.55,TEXT,28),
                     lab('time →',5.3,-2.4,GREY,26))
        self.at('With the');appear(self,recap)
        glu=Dot([-5.1,2.65,0],radius=.16,color=YELLOW)
        self.add(glu,lab('glutamate',-4.9,3.25,YELLOW,28))
        self.play(glu.animate.move_to([-3.55,2.13,0]),run_time=.65)
        self.at('calcium entering')
        ca=VGroup(*[Dot([-3.1,2.4,0],radius=.14,color=TEAL) for _ in range(5)])
        self.add(ca,lab('Ca²⁺ entry',-1.55,.75,TEAL,28))
        flow=Line([-3.1,2.6,0],[-3.1,.35,0],color=TEAL,stroke_width=12)
        self.play(ca.animate.move_to([-3.1,.4,0]),
                  ShowPassingFlash(flow,time_width=.7),
                  Flash([-3.1,1.45,0],color=TEAL,flash_radius=.45),run_time=.8)
        dest=[[-4.8,-.6,0],[-3.9,-1.3,0],[-2.8,-1.4,0],[-1.7,-.7,0],[-3.1,-.5,0]]
        self.play(*[d.animate.move_to(p) for d,p in zip(ca,dest)],g[0].animate.set_fill(TEAL,.22),run_time=.65)
        self.at('active spines');appear(self,lab('Ca²⁺ rise',-3.1,-.05,TEAL,32));self.finish()


class S20Scope(SpokenScene):
    def construct(self):
        outline=RoundedRectangle(width=12,height=5.7,corner_radius=1,color=GREY,fill_opacity=.04).move_to([0,-.15,0])
        dg=chip('dentate\ngyrus',GREY,36).move_to([-4.5,0,0])
        ca3=chip('CA3',GREY,44).move_to([-.4,0,0]);ca1=chip('CA1',GREY,44).move_to([4.5,0,0])
        sch=Arrow(ca3.get_right(),ca1.get_left(),color=PURPLE,buff=.15,stroke_width=7)
        self.add(outline,ca3,ca1,sch,lab('Schaffer collaterals',2.1,1.1,PURPLE,30),
                 lab('NMDA-dependent\n(this film)',2.1,-1.15,PURPLE,30))
        self.at('One caution');appear(self,lab('Scope matters',0,3.25,GOLD,38))
        self.at('Not every');appear(self,dg)
        self.at('Mossy fiber')
        moss=Arrow(dg.get_right(),ca3.get_left(),buff=.15,color=GREEN,stroke_width=8)
        self.play(GrowArrow(moss),run_time=.5);appear(self,lab('mossy fibres',-2.5,1.1,GREEN,30))
        self.at('Guinea pig');appear(self,lab('guinea-pig hippocampus · in slices',0,-3.3,TEXT,26))
        self.at('needed no');appear(self,lab('NMDA-independent\nLTP',-2.5,-1.2,GREEN,32));self.finish()


class S21Takeaway(SpokenScene):
    def construct(self):
        self.add(lab('At Schaffer–CA1 synapses',0,3.3,TEXT,36))
        chips=VGroup(*[chip(s,c,30).move_to([x,1.95,0]) for s,c,x in
            [('NMDA receptor',PURPLE,-4.3),('Ca²⁺ rise',TEAL,0),('depolarization',PINK,4.3)]])
        self.add(*chips)
        self.at('block the');appear(self,lab('blocked',-4.3,1.05,RED,28))
        self.at('the calcium');appear(self,lab('blocked',0,1.05,RED,28))
        self.at('or the depolarization');appear(self,lab('blocked',4.3,1.05,RED,28))
        self.at('LTP fails');appear(self,lab('at these synapses: any block → no LTP',0,.05,RED,34))
        self.at('Pair glutamate');f=formula().scale(1.15).move_to([0,-1.3,0]);appear(self,f,rt=.2)
        self.at('and it appears');appear(self,check(-1.3,-2.75,1.3),lab('LTP',.3,-2.75,GREEN,42));self.finish()


class S22End(EndCard):
    LINE='Block receptor, calcium or depolarization: LTP fails. Pair signals: LTP appears.'
    def construct(self):
        self.add(lab('At Schaffer–CA1 synapses',0,2.35,TEXT,30))
        self.play(FadeIn(lab('Block receptor, calcium or depolarization:\nLTP fails. Pair signals: LTP appears.',0,.3,TEXT,38)),run_time=.5)
        self.add(lab('biochemistrypedia.com',0,-1.7,TEAL,26))
        self.wait(max(.01,self.narration_s-self.elapsed()))
