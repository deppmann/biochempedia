"""Chapter 1, reviewer fix round.
COLOR MAP: YELLOW stimulus; TEAL graded potential / fluctuation;
GREEN spikes / firing rate; BLUE comparison; GREY structures / axes;
RED inhibition; PURPLE smell receptor proteins (unused in this chapter).
Models: Gaussian tuning 50 exp(-.5*((theta-45)/22.5)^2);
V = -65/(1+g); passive attenuation exp(-x/lambda).
Rasters are illustrative integrate-and-fire reconstructions, not measured data:
spike times are crossings of integrated rate, with exponential adaptation.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'


def train(xs, y, h=.8, color=GREEN, w=5):
    return VGroup(*[Line([x,y,0],[x,y+h,0],color=color,stroke_width=w) for x in xs])


def baseline(x0,x1,y,color=GREY):
    return Line([x0,y,0],[x1,y,0],color=color,stroke_width=2)


def firing(duration, initial, steady=None, tau=2):
    """Deterministic phase crossings of r(t)=steady+(initial-steady)e^-t/tau."""
    steady=initial if steady is None else steady
    t=np.linspace(0,duration,12001)
    phase=steady*t+(initial-steady)*tau*(1-np.exp(-t/tau))
    return np.interp(np.arange(.35,phase[-1],1),phase,t)


def heading(s,color=TEXT):
    return T(s,34,color).move_to([0,3.15,0])


def tag(s):
    return T(s,26,GREY).move_to([0,-3.22,0])


def brain():
    outline=Union(Circle(.8).shift(LEFT*.5),Circle(.9).shift(RIGHT*.5),Circle(.65).shift(UP*.5),color=GREY,fill_opacity=.13)
    return VGroup(outline,T('brain',28).move_to([0,-.15,0]))


def sense(kind):
    if kind=='eye':
        return VGroup(Ellipse(width=1.35,height=.8,color=GREY),Circle(.25,color=GREY))
    if kind=='fingertip':
        return VGroup(RoundedRectangle(width=.8,height=1.1,corner_radius=.35,color=GREY),RoundedRectangle(width=.44,height=.36,corner_radius=.12,color=GREY).shift(UP*.18))
    if kind=='tongue':
        return VGroup(VMobject(color=YELLOW,fill_opacity=.13).set_points_smoothly([[-.6,.45,0],[-.57,-.2,0],[-.38,-.6,0],[0,-.72,0],[.38,-.6,0],[.57,-.2,0],[.6,.45,0]]),Line([0,.25,0],[0,-.4,0],color=YELLOW))
    return VGroup(VMobject(color=GREY).set_points_smoothly([[-.2,.65,0],[-.05,.2,0],[.48,-.2,0],[.35,-.4,0],[.05,-.42,0],[-.12,-.25,0],[-.4,-.45,0],[-.57,-.3,0]]),Arc(radius=.16,start_angle=0,angle=PI,color=GREY).shift(RIGHT*.02+DOWN*.37))


def muscle_stage():
    muscle=RoundedRectangle(width=1.65,height=3.7,corner_radius=.65,color=GREY,fill_opacity=.13).move_to([-4,.4,0])
    fibres=VGroup(*[Line([-4+dx,-1.1,0],[-4+dx,1.9,0],color=GREY,stroke_opacity=.45) for dx in [-.48,.48]])
    receptor=VGroup(Ellipse(width=.55,height=1.15,color=TEAL,stroke_width=5).move_to([-4,.4,0]),T('one stretch receptor',28,TEAL).move_to([-.3,-1.25,0]),Line([-3.75,.05,0],[-1.6,-.9,0],color=TEAL))
    nerve=VGroup(Line([-3.72,.4,0],[2.2,.4,0],color=GREY,stroke_width=5),T('one nerve fibre',28,GREY).move_to([-.5,.85,0]))
    electrode=VGroup(Line([2.2,1.6,0],[2.2,.35,0],color=TEXT,stroke_width=6),T('electrode',28).move_to([3.55,1.55,0]),baseline(2.1,5.7,-.5),train(2.2+firing(1,4)*3.4,-.5,.8))
    weight=VGroup(Line([-4,-1.45,0],[-4,-2,0],color=YELLOW),Rectangle(width=1.6,height=.8,color=YELLOW,fill_opacity=.15).move_to([-4,-2.4,0]),T('weight',28,YELLOW).move_to([-2.35,-2.4,0]))
    return VGroup(muscle,fibres,receptor,nerve,electrode),weight


def prediction():
    title=heading('Heavier weight: bigger spikes, or more spikes?',YELLOW)
    setups=VGroup()
    for x,h,name,w in [(-3.1,1.8,'light weight',1.2),(3.1,2.6,'heavier weight',1.8)]:
        top=2.5
        m=RoundedRectangle(width=1.45,height=h,corner_radius=.4,color=GREY,fill_opacity=.12).move_to([x,top-h/2,0])
        r=Ellipse(width=.55,height=h*.7,color=TEAL).move_to(m)
        wt=Rectangle(width=w,height=.45,color=YELLOW,fill_opacity=.15).move_to([x,top-h-.45,0])
        setups.add(VGroup(m,r,Line([x,top-h,0],wt.get_top(),color=YELLOW),wt,T(name,28,YELLOW).move_to([x+(-1.75 if x<0 else 2.05),1.4,0])))
    left=VGroup(baseline(-5.8,-.5,-2.15),train(-5.6+firing(1,4)*4.9,-2.15,1.35,GREY),T('bigger?',30,GREY).move_to([-3.15,-2.7,0])).set_opacity(.55)
    right=VGroup(baseline(.5,5.8,-2.15),train(.7+firing(1,9)*4.9,-2.15,.85,GREY),T('more often?',30,GREY).move_to([3.15,-2.7,0])).set_opacity(.55)
    return title,setups,left,right,tag('candidate traces • reconstruction')


def idea_box():
    border=RoundedRectangle(width=12.1,height=6.7,corner_radius=.2,color=GREY).move_to([0,.1,0])
    title=T('RATE CODE • fixed counting window',28,GREY).move_to([0,2.75,0])
    eq=VGroup(T('rate',32,GREEN),T('= tuning curve(stimulus)',32),T('+ fluctuation',32,TEAL)).arrange(RIGHT,buff=.15).move_to([0,1.85,0])
    noise=VGroup(T('noise = standard deviation of the fluctuation',28,TEAL).move_to([0,.95,0]),T('average fluctuation = 0',28,TEAL).move_to([0,.05,0]))
    ident=VGroup(T('neuron identities + relative rates',30,GREEN).move_to([0,-.85,0]),T('what • where • how much',30,YELLOW).move_to([0,-1.75,0]))
    small=VGroup(T('A small change is easiest to see where the mean rate',26,BLUE),T('changes a lot compared with the noise.',26,BLUE)).arrange(DOWN,buff=.17).move_to([0,-2.65,0])
    small.add(Line([-4,-2.12,0],[4,-2.12,0],color=GREY,stroke_opacity=.4))
    return border,title,eq,noise,ident,small


def count_window(compact=False):
    if compact:
        return VGroup(Rectangle(width=9.5,height=1.25,color=GREY).move_to([0,-1.9,0]),train(-4.3+firing(1,7)*8.6,-2.4,.9),T('spike count: 7 in a fixed 1 s window',28,GREEN).move_to([0,-.95,0]),T('0 s',26,GREY).move_to([-4.45,-2.8,0]),T('1 s',26,GREY).move_to([4.45,-2.8,0]))
    return VGroup(Rectangle(width=9.5,height=1.65,color=GREY).move_to([0,.4,0]),train(-4.3+firing(1,7)*8.6,-.1,.95),T('spike count in a fixed window',30).move_to([0,1.85,0]),T('0 s',26,GREY).move_to([-4.45,-.75,0]),T('1 s',26,GREY).move_to([4.45,-.75,0]),T('7 spikes in 1 second',32,GREEN).move_to([0,-1.65,0]))


def channel(x, opened=False, resting=False):
    color=GREY if resting or not opened else TEAL
    walls=VGroup(*[Line([x+dx,-1.4,0],[x+dx,1.5,0],color=color,stroke_width=5) for dx in [-.23,.23]])
    if opened:
        gate=VGroup(Line([x-.23,.15,0],[x-.23,.65,0],color=color,stroke_width=9),Line([x+.23,-.15,0],[x+.23,.35,0],color=color,stroke_width=9))
        if not resting:
            walls.add(Line([x,-1.3,0],[x,1.4,0],color=TEAL,stroke_width=12,stroke_opacity=.22))
    else:
        gate=Line([x-.23,.25,0],[x+.23,.25,0],color=color,stroke_width=7)
    return VGroup(walls,gate)


def voltage(g):
    return -65/(1+g)


def voltage_stage(g=0):
    mem=VGroup(Line([-6.3,1.75,0],[-.65,1.75,0],color=GREY,stroke_width=5),Line([-6.3,-1.65,0],[-.65,-1.65,0],color=GREY,stroke_width=5))
    resting=VGroup(channel(-5.55,True,True),channel(-4.8,True,True),T('resting channels',22,GREY).move_to([-5,-2.02,0]))
    channels=VGroup(*[channel(x,i<g) for i,x in enumerate([-3.85,-3.05,-2.25,-1.45])])
    count=T(f'{g} open transduction '+('channel' if g==1 else 'channels'),26,TEAL).move_to([-3.4,-2.55,0])
    scale=NumberLine(x_range=[-65,0,13],length=5.4,include_numbers=False,color=GREY).move_to([3,.05,0])
    labels=VGroup(T('−65 mV',26,GREY).move_to([.35,-.65,0]),T('0 mV',26,GREY).move_to([5.7,-.65,0]),T('balance point',28,TEAL).move_to([3,2.15,0]),Line([5.7,-.25,0],[5.7,.8,0],color=TEXT,stroke_width=5))
    marker=Triangle(color=TEAL,fill_opacity=1).scale(.16).rotate(PI).move_to(scale.n2p(voltage(g))+UP*.3)
    readout=T(f'{voltage(g):g} mV',30,TEAL).move_to([scale.n2p(voltage(g))[0],1.05,0])
    mem.add(T('closed: bar across • open: clear gap',22,GREY).move_to([-3.4,-3.05,0]))
    return mem,resting,channels,count,scale,labels,marker,readout


class S00Title(TitleCard):
    TITLE='What a Spike Means'
    LESSON='Principles of Sensory Coding'
    def construct(self):
        group=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON.upper(),26,GREY),T(self.TITLE,54,font=TITLE_FONT),Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.4)
        self.play(FadeIn(group),run_time=.6)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        title=heading('What a Spike Means')
        rows=VGroup()
        ys=[2,.55,-.9,-2.35]
        for kind,y in zip(['fingertip','eye','tongue','nose'],ys):
            icon=sense(kind).scale(1.15).move_to([-5.55,y,0])
            label=T(kind,26,GREY).move_to([-3.75,y,0])
            rows.add(VGroup(icon,label,baseline(-2.5,2.45,y)))
        b=brain().scale(1.3).move_to([4.4,-.1,0])
        self.at('Every sense')
        self.add(title,rows,b)
        self.at('spikes that look alike')
        ticks=VGroup(*[train(-2.41+firing(1,4)*1.5,y,.5) for y in ys])
        self.play(FadeIn(ticks),run_time=.25)
        self.play(ticks.animate.shift(RIGHT*3.3),run_time=1.15,rate_func=linear)
        self.at('So how does')
        self.play(Transform(title,heading('what?    where?    how hard?',YELLOW)),run_time=.45)
        self.finish()


class S02Adrian(SpokenScene):
    def construct(self):
        s,w=muscle_stage()
        self.at('In')
        self.add(heading('Adrian and Zotterman • 1926'),s[0],s[1],tag('reconstruction • frog muscle'))
        self.at('recorded one stretch receptor')
        self.play(FadeIn(s[2]),Create(s[3]),FadeIn(s[4]),run_time=.8)
        self.at('Then they hung weights')
        self.play(FadeIn(w,shift=DOWN*.25),run_time=.65)
        self.finish()


class S03Predict(SpokenScene):
    def construct(self):
        title,setups,l,r,n=prediction()
        s,w=muscle_stage()
        old=VGroup(s,w)
        self.add(heading('Adrian and Zotterman • 1926'),old,tag('reconstruction • frog muscle'))
        self.at('A heavier weight')
        self.play(FadeOut(old),FadeIn(setups),FadeIn(l),FadeIn(r),run_time=.7)
        self.at('Will its spikes')
        self.play(Transform(self.mobjects[0],title),Indicate(l,color=GREY,scale_factor=1.02),run_time=.4)
        self.at('or will they')
        self.play(Indicate(r,color=GREY,scale_factor=1.02),run_time=.4)
        self.finish()


class S04Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        title,setups,l,r,n=prediction()
        self.add(title,setups,l,r,tag('reconstruction • frog muscle'))
        self.wait(5)


class S05Reveal(SpokenScene):
    def construct(self):
        title=heading('reconstruction',GREY)
        rows=VGroup()
        for rate,y,name in [(4,1.45,'light'),(7,-.4,'medium'),(11,-2.25,'heavy')]:
            xs=-2.8+firing(1,rate)*8.4
            rows.add(VGroup(T(name+' load',28,YELLOW).move_to([-4.55,y+.45,0]),baseline(-3,5.8,y),train(xs,y,.95),DashedLine([-3,y+.95,0],[5.8,y+.95,0],color=GREY,stroke_width=1)))
        self.at('They come more often')
        self.add(title)
        self.play(LaggedStart(*[FadeIn(r) for r in rows],lag_ratio=.12),run_time=.85)
        record_note=tag('illustrative spike records • time →')
        self.add(record_note)
        self.at('Every spike stays')
        self.play(Transform(title,heading('rate coding • same spike size',GREEN)),run_time=.4)
        self.at('while a weight is held')
        self.play(FadeOut(rows),FadeOut(record_note),run_time=.25)
        held=T('heavy load held',30,YELLOW).move_to([0,2.15,0])
        axis=VGroup(baseline(-5.6,5.6,-1.3),T('0',26,GREY).move_to([-5.6,-1.7,0]),T('time →',28,GREY).move_to([4.9,-1.7,0]))
        self.play(FadeIn(held),Create(axis),run_time=.4)
        self.at('the firing slowly falls')
        label=T('adaptation • gaps widen during a held load',30,TEAL).move_to([0,-2.65,0])
        # Fixed spike positions; reveal forward in time, never rearrange existing events.
        xs=-5.4+firing(5,4,1.2,tau=1.8)*2.15
        spikes=train(xs,-1.3,1.9)
        self.add(label)
        cursor=ValueTracker(-5.6)
        growing=always_redraw(lambda: VGroup(
            Line([-5.6,1.25,0],[-5.6,1.75,0],color=YELLOW),
            Line([-5.6,1.75,0],[max(-5.599,cursor.get_value()),1.75,0],color=YELLOW),
            Line([cursor.get_value(),1.75,0],[cursor.get_value(),1.25,0],color=YELLOW)))
        for spike in spikes:
            spike.set_opacity(0)
            spike.add_updater(lambda m: m.set_opacity(float(m.get_x() <= cursor.get_value())))
        self.add(growing,spikes)
        self.play(cursor.animate.set_value(5.6),run_time=2.2,rate_func=linear)
        growing.clear_updaters()
        spikes.clear_updaters()
        self.wait(.8)
        self.finish()


class S06Rate(SpokenScene):
    def construct(self):
        meter=Rectangle(width=1.5,height=4.4,color=GREY).move_to([-2.5,.1,0])
        bundle=VGroup(*[Line([.3,y,0],[5.4,y,0],color=GREY,stroke_width=7) for y in [1.7,.9,.1,-.7,-1.5]])
        load_labels=VGroup(*[T(s,28,YELLOW).move_to([-5,y,0]) for s,y in [('light',-1.6),('medium',0),('heavy',1.6)]])
        count=T('1 / 5',32,GREEN).move_to([2.8,2.45,0])
        fill=Rectangle(width=1.35,height=.9,color=GREEN,fill_opacity=.8).align_to(meter,DOWN).set_x(-2.5)
        pointer=Arrow([-4.2,-1.6,0],[-3.4,-1.6,0],color=YELLOW,buff=0)
        self.at('So the rate')
        self.add(heading('how much?',YELLOW),meter,fill,bundle,load_labels,pointer,count,T('load',28,YELLOW).move_to([-5,2.45,0]),T('firing rate',28,GREEN).move_to([-2.5,-2.65,0]),T('number of active fibres',28,GREEN).move_to([2.8,-2.65,0]))
        bundle[0].set_color(GREEN)
        self.wait(1.35)
        for n,h,y in [(3,2.7,0),(5,4.25,1.6)]:
            target=Rectangle(width=1.35,height=h,color=GREEN,fill_opacity=.8).align_to(meter,DOWN).set_x(-2.5)
            self.play(Transform(fill,target),pointer.animate.set_y(y),*[bundle[j].animate.set_color(GREEN) for j in range(n)],Transform(count,T(f'{n} / 5',32,GREEN).move_to(count)),run_time=.45)
            self.wait(1.2)
        self.finish()


class S07Line(SpokenScene):
    def construct(self):
        eye=VGroup(Ellipse(width=3.1,height=4.8,color=GREY,fill_opacity=.08),Arc(radius=1.35,start_angle=PI+.18,angle=PI-.36,color=GREY).stretch(.35,1).shift(UP*.35),Arc(radius=1.2,start_angle=-.7,angle=1.4,color=TEAL).shift(RIGHT*.15)).move_to([-4.45,.15,0])
        nerve=Line([-2.9,-.15,0],[2.25,-.15,0],color=GREY,stroke_width=8)
        b=brain().scale(1.7).move_to([4.05,-.35,0])
        b[0].stretch_to_fit_height(4.7).set_y(-.1)
        b[1].move_to([4.05,-1.4,0])
        self.at('Now the what')
        eye_label=T('closed eye',28,GREY).move_to([-4.45,-2.55,0])
        self.add(heading('what?',YELLOW),eye,nerve,b,eye_label)
        finger=RoundedRectangle(width=.85,height=1.3,corner_radius=.35,color=YELLOW,fill_opacity=.15).move_to([-4.45,3.0,0])
        flab=T('pressing finger',28,YELLOW).move_to([-1.2,2.35,0])
        leader=Line([-3.95,2.8,0],flab.get_left()+LEFT*.15,color=YELLOW)
        self.at('Pressure on the closed eye')
        self.play(FadeIn(finger),FadeIn(flab),Create(leader),run_time=.3)
        self.play(finger.animate.shift(DOWN*.45),run_time=.45)
        flash=VGroup(*[Line([4.05+np.cos(a)*.35,.8+np.sin(a)*.35,0],[4.05+np.cos(a)*.7,.8+np.sin(a)*.7,0],color=YELLOW,stroke_width=4) for a in np.linspace(0,TAU,9)[:-1]])
        self.at('seen as light')
        self.play(Create(flash),FadeIn(T('seen as light',28,YELLOW).move_to([4.05,2.35,0])),run_time=.4)
        self.at('Activity in the optic nerve')
        self.add(T('optic nerve',28,GREEN).move_to([-.1,.75,0]))
        self.play(nerve.animate.set_color(GREEN),run_time=.35)
        activity=train(-2.85+firing(1,3)*1.3,-.15,.55)
        self.play(FadeIn(activity),run_time=.2)
        self.play(activity.animate.shift(RIGHT*3.7),run_time=1.1,rate_func=linear)
        self.play(FadeOut(activity),run_time=.2)
        self.at('So the kind of sense')
        touch=VGroup(Circle(.35,color=YELLOW).move_to([-4.45,-2.65,0]),T('finger touch',28,YELLOW).move_to([-4.45,-3.18,0]),VMobject(color=GREEN,stroke_width=5).set_points_as_corners([[-4.1,-2.65,0],[1.7,-2.65,0],[2.8,-1.15,0]]),Dot([2.8,-1.15,0],radius=.14,color=YELLOW),T('touch afferent → touch',28,GREEN).move_to([.2,-3.05,0]))
        self.play(FadeOut(eye_label),FadeIn(touch),run_time=.45)
        self.at('the line')
        self.play(FadeOut(flab),FadeOut(leader),FadeIn(T('labelled line',32,GREEN).move_to([.3,-1.3,0])),run_time=.35)
        self.add(tag('Müller’s law of specific nerve energies • classic example').set_y(-3.55))
        self.at('Whether every quality')
        self.play(FadeIn(T('Every quality? Still argued.',26,GREY).move_to([-.5,2.35,0])),run_time=.4)
        self.finish()


class S08Terms(SpokenScene):
    def construct(self):
        # Positive orientation coordinates keep the vertical axis at the left edge.
        ax=Axes(x_range=[0,90,15],y_range=[0,60,20],x_length=9.7,y_length=4.6,tips=False,axis_config={'color':GREY}).move_to([-.25,.1,0])
        rate=lambda x:50*np.exp(-.5*((x-45)/22.5)**2)
        curve=ax.plot(rate,x_range=[0,90],color=GREEN)
        ticks=VGroup(*[T(str(x)+'°',26,GREY).next_to(ax.c2p(x,0),DOWN,buff=.15) for x in [0,45,90]],*[T(str(y),26,GREY).next_to(ax.c2p(0,y),LEFT,buff=.15) for y in [0,20,40,60]])
        caption=tag('illustrative Gaussian tuning').set_y(-3.55)
        self.at('A tuning curve')
        self.add(ax,ticks,heading('bar orientation → mean firing rate'),caption,T('orientation',28,YELLOW).move_to([0,-2.95,0]),T('spikes/s',28,GREEN).rotate(PI/2).move_to([-6.2,.4,0]))
        self.play(Create(curve),run_time=1.1)
        self.at('mean firing rate')
        self.play(FadeIn(T('tuning curve',28,GREEN).move_to([-2.7,2.05,0])),run_time=.35)
        self.at('The count varies')
        points=VGroup(*[Dot(ax.c2p(x,rate(x)),radius=.055,color=TEAL) for x in [15,30,45,60,75]])
        self.play(FadeIn(points),run_time=.4)
        self.at('That spread is noise')
        bars=VGroup()
        for x in [15,30,45,60,75]:
            low=ax.c2p(x,rate(x)-5); high=ax.c2p(x,rate(x)+5)
            bars.add(VGroup(Line(low,high,color=TEAL),Line(low+LEFT*.12,low+RIGHT*.12,color=TEAL),Line(high+LEFT*.12,high+RIGHT*.12,color=TEAL)))
        noise=VGroup(T('noise:',28,TEAL),T('trial-to-trial',26,TEAL),T('spread',26,TEAL)).arrange(DOWN,buff=.12).move_to([4.85,1.65,0])
        self.play(FadeOut(caption),run_time=.18)
        self.play(LaggedStart(*[Create(b) for b in bars],lag_ratio=.4),FadeIn(noise),FadeIn(tag('illustrative Gaussian tuning • equal noise').set_y(-3.55)),run_time=1.1)
        self.wait(1.2)
        self.finish()


class S09Idea(SpokenScene):
    def construct(self):
        b,t,e,n,_,_=idea_box()
        # The window is already explicit while the opening sentence is spoken.
        window=count_window()
        self.at('Here is the one idea')
        self.add(b,t,window)
        self.at('for spikes counted')
        self.play(Indicate(window[0],color=GREEN,scale_factor=1.02),run_time=.5)
        self.at('On each trial')
        self.play(ReplacementTransform(window,count_window(True)),FadeIn(e[0],shift=LEFT*.3),run_time=.45)
        self.at('is its tuning curve')
        self.play(FadeIn(e[1],shift=LEFT*.3),run_time=.45)
        self.at('plus a fluctuation')
        self.play(FadeIn(e[2],shift=LEFT*.3),run_time=.45)
        self.at('averages to zero')
        self.play(FadeIn(n),run_time=.45)
        self.finish()


class S10Reading(SpokenScene):
    def construct(self):
        b,t,e,n,i,_=idea_box()
        window=count_window(True)
        self.add(b,t,e,n,window)
        self.at('Which neurons respond')
        self.play(FadeOut(window),FadeIn(i[0]),run_time=.6)
        self.at('together tell you')
        self.play(FadeIn(i[1]),run_time=.5)
        self.finish()


class S11Small(SpokenScene):
    def construct(self):
        b,t,e,n,i,s=idea_box()
        self.add(b,t,e,n,i)
        self.at('A small change')
        self.play(FadeIn(s),run_time=.55)
        self.at('Spike timing can')
        self.play(FadeIn(tag('Spike timing can carry information too.').set_y(-3.55)),run_time=.5)
        self.finish()


class S12Transduction(SpokenScene):
    def construct(self):
        mem,rest,chs,count,scale,labels,marker,readout=voltage_stage(0)
        self.at('How is the rate')
        self.add(heading('How is the rate set?'),mem,rest,chs,count,scale,labels,marker,readout,T('nerve ending membrane',28,GREY).move_to([-3.4,2.5,0]))
        self.at('force opens channels')
        force=Arrow([-3.85,2.15,0],[-3.85,1.65,0],color=YELLOW,buff=0)
        self.play(GrowArrow(force),run_time=.35)
        self.play(FadeOut(count),FadeOut(readout),run_time=.15)
        count=T('1 open transduction channel',26,TEAL).move_to(count)
        readout=T('−32.5 mV',30,TEAL).move_to([scale.n2p(voltage(1))[0],1.05,0])
        self.play(Transform(chs[0],channel(-3.85,True)),marker.animate.move_to(scale.n2p(voltage(1))+UP*.3),FadeIn(count),FadeIn(readout),run_time=.45)
        self.at('In a simple model')
        self.add(tag('toy passive model • no injected current • settled voltages').set_y(-3.6))
        self.play(Indicate(scale,color=TEAL,scale_factor=1.02),run_time=.5)
        self.add(T('resting reversal: −65 mV',26,GREY).move_to([3,-1.65,0]))
        self.at('each open channel')
        self.play(Indicate(chs[0],color=TEAL,scale_factor=1.03),Indicate(readout,color=TEAL,scale_factor=1.03),run_time=.8)
        self.finish()


class S13Graded(SpokenScene):
    def construct(self):
        mem,rest,chs,count,scale,labels,marker,readout=voltage_stage(1)
        self.add(mem,rest,chs,count,scale,labels,marker,readout,tag('toy passive model • no injected current • settled voltages').set_y(-3.6),T('resting reversal: −65 mV',26,GREY).move_to([3,-1.65,0]))
        self.at('So the receptor potential')
        self.add(heading('graded receptor potential',TEAL))
        self.at('Each extra channel')
        for g in [2,3,4]:
            if g==3:
                self.at('as the voltage')
            previous=voltage(g-1); value=voltage(g)
            label={2:'−22 mV',3:'−16 mV',4:'−13 mV'}[g]
            p0=scale.n2p(previous)+DOWN*1.1; p1=scale.n2p(value)+DOWN*1.1
            bracket=VGroup(Line(p0,p1,color=TEAL),Line(p0+UP*.1,p0+DOWN*.1,color=TEAL),Line(p1+UP*.1,p1+DOWN*.1,color=TEAL),T({2:'about 11 mV',3:'about 5 mV',4:'about 3 mV'}[g],26,TEAL).move_to([3,-2.35,0]))
            self.play(FadeOut(count),FadeOut(readout),run_time=.15)
            count=T(f'{g} open transduction channels',26,TEAL).move_to(count)
            readout=T(label,30,TEAL).move_to([scale.n2p(value)[0],1.05,0])
            self.play(Transform(chs[g-1],channel([-3.85,-3.05,-2.25,-1.45][g-1],True)),marker.animate.move_to(scale.n2p(value)+UP*.3),FadeIn(count),FadeIn(readout),FadeIn(bracket),run_time=.45)
            self.wait(1.15)
            self.play(FadeOut(bracket),run_time=.15)
        self.add(T('smaller steps → saturation',28,TEAL).move_to([3,-2.35,0]))
        self.wait(1.2)
        self.finish()


class S14Spikes(SpokenScene):
    def construct(self):
        title=heading('a graded potential fades',TEAL)
        axon=RoundedRectangle(width=10.6,height=4.6,corner_radius=.65,color=GREY,fill_opacity=.05).move_to([-.7,.1,0])
        # x=0 and x=lambda included explicitly: the second bar is exactly exp(-1).
        lam=3.8
        xs=np.array([-5.6,-1.8,.1,2,3.9])
        bars=VGroup(*[Line([x,-.8,0],[x,-.8+2.6*np.exp(-(x+5.6)/lam),0],color=TEAL,stroke_width=9) for x in xs])
        bracket=VGroup(Line([-5.6,-1.6,0],[-1.8,-1.6,0],color=TEAL),Line([-5.6,-1.45,0],[-5.6,-1.75,0],color=TEAL),Line([-1.8,-1.45,0],[-1.8,-1.75,0],color=TEAL))
        note=VGroup(T('one length constant',26,TEAL),T('falls to about 1/3',26,TEAL)).arrange(DOWN,buff=.12).move_to([-3.7,-2.25,0])
        values=VGroup(T('100%',26,TEAL).move_to([-5.3,2.05,0]),T('37%',26,TEAL).move_to([-1.8,.65,0]))
        self.add(title,axon,bars[0],values[0])
        self.at('a graded potential fades')
        self.play(LaggedStart(*[GrowFromEdge(b,DOWN) for b in bars[1:]],lag_ratio=.16),FadeIn(bracket),FadeIn(note),FadeIn(values[1]),run_time=1)
        self.at('To reach the spinal cord')
        cord=chip('spinal\ncord',GREY,28).move_to([5.45,-.2,0])
        connector=Line([4.6,-.2,0],cord.get_left(),color=GREY,stroke_width=5)
        self.play(FadeIn(cord),Create(connector),run_time=.4)
        self.at('it must become spikes')
        self.play(FadeOut(bracket),FadeOut(note),FadeOut(values),run_time=.25)
        self.at('which regenerate')
        spikes=train(xs,-.8,2.6)
        self.play(Transform(title,heading('spikes regenerate',GREEN)),ReplacementTransform(bars,spikes),FadeIn(T('same spike height along the axon',28,GREEN).move_to([-.6,-2.7,0])),run_time=.6)
        self.wait(1.2)
        self.finish()


class S15Where(SpokenScene):
    def construct(self):
        # Smooth, joined silhouette: four fingers and a thumb on a rounded palm.
        hand=VMobject(color=GREY,fill_opacity=.1)
        hand.start_new_path(np.array([-4.8,-2.3,0]))
        def curve(c1,c2,end):
            hand.add_cubic_bezier_curve_to(np.array([*c1,0]),np.array([*c2,0]),np.array([*end,0]))
        def edge(x,y):
            hand.add_line_to(np.array([x,y,0]))
        curve((-4.8,-1.4),(-5.25,-.65),(-5.72,.02))
        curve((-6.05,.55),(-5.55,.7),(-5.28,.25))
        edge(-4.95,-.25); edge(-5.08,1.8)
        curve((-5.08,2.35),(-4.5,2.35),(-4.5,1.8))
        edge(-4.48,.25); edge(-4.44,2.12)
        curve((-4.44,2.7),(-3.83,2.7),(-3.83,2.12))
        edge(-3.8,.3); edge(-3.78,1.95)
        curve((-3.78,2.52),(-3.16,2.52),(-3.16,1.95))
        edge(-3.12,.15); edge(-3.08,1.35)
        curve((-3.08,1.92),(-2.53,1.92),(-2.53,1.35))
        edge(-2.5,-.8)
        curve((-2.48,-1.5),(-2.95,-1.65),(-3,-2.3))
        edge(-4.8,-2.3); hand.close_path()
        back=RoundedRectangle(width=3.6,height=4.9,corner_radius=.8,color=GREY,fill_opacity=.1).move_to([3.4,.05,0])
        first=Ellipse(width=.46,height=.65,color=YELLOW,stroke_width=5).move_to([-4.12,1.96,0])
        leader=Line([-3.85,2.05,0],[-1.95,2.35,0],color=YELLOW)
        firstlabel=T('receptive field',28,YELLOW).move_to([-.45,2.4,0])
        self.at('Receptive fields help')
        self.add(heading('where?',YELLOW),hand,back,first,leader,firstlabel,T('hand',28,GREY).move_to([-4,-2.85,0]),T('back',28,GREY).move_to([3.4,-2.85,0]))
        self.at('small fields on a fingertip')
        small=VGroup(*[Ellipse(width=.44,height=.6,color=YELLOW,stroke_width=4).move_to([x,y,0]) for x,y in [(-4.78,1.8),(-3.46,1.8),(-4.12,1.25)]])
        self.play(FadeOut(firstlabel),run_time=.15)
        firstlabel=T('small-field\ntouch afferents',26,YELLOW).move_to([-.35,1.4,0])
        self.play(Create(small),Transform(leader,Line([-3.25,1.8,0],firstlabel.get_left()+LEFT*.1,color=YELLOW)),FadeIn(firstlabel),run_time=.5)
        self.at('larger ones elsewhere')
        large=VGroup(*[Ellipse(width=2.25,height=1.3,color=YELLOW,stroke_width=4).move_to([x,y,0]) for x,y in [(3.1,1.55),(3.6,0),(3.1,-1.55)]])
        self.play(Create(large),FadeIn(T('larger fields elsewhere',26,YELLOW).move_to([3.4,2.85,0])),run_time=.5)
        self.at('Field size also depends')
        broad=DashedVMobject(Ellipse(width=2.7,height=2.5,color=BLUE).move_to([-3.95,-.8,0]),num_dashes=24)
        pac=VGroup(T('Pacinian afferents',26,BLUE),T('much broader',26,BLUE),T('fields',26,BLUE)).arrange(DOWN,buff=.14).move_to([-.1,-1.5,0])
        self.play(Create(broad),FadeIn(pac),Create(Line([-2.6,-.8,0],[-1.85,-1.15,0],color=BLUE)),run_time=.5)
        self.finish()


class S16When(SpokenScene):
    def construct(self):
        # All three rows share x; the probe spans the onset-to-offset hold.
        x0,x1=-3.6,3.5
        skin=Line([-4.1,2.02,0],[4,2.02,0],color=GREY,stroke_width=5)
        probe=Rectangle(width=x1-x0,height=.4,color=YELLOW,fill_opacity=.2).move_to([(x0+x1)/2,2.5,0])
        step=VMobject(color=YELLOW,stroke_width=4).set_points_as_corners([[-5.8,1.1,0],[x0,1.1,0],[x0,1.85,0],[x1,1.85,0],[x1,1.1,0],[5.8,1.1,0]])
        marks=VGroup(*[DashedLine([x,1.1,0],[x,-3,0],color=GREY,stroke_opacity=.4) for x in [x0,x1]])
        self.at('Endings are tuned')
        self.add(heading('tuned in time'),skin,probe,step,T('probe',26,YELLOW).move_to([-5.15,2.5,0]),T('skin',26,GREY).move_to([5,2.02,0]),T('pressure on skin',28,YELLOW).move_to([0,1.48,0]),T('onset',26,YELLOW).move_to([x0,.8,0]),T('offset',26,YELLOW).move_to([x1,.8,0]),marks,tag('illustrative rasters • shared time axis →').set_y(-3.55))
        self.play(probe.animate.shift(DOWN*.18),run_time=.35)
        self.at('Rapidly adapting endings')
        # Rate proportional to the onset/offset transient: exponential bursts.
        burst=firing(.7,9,.1,tau=.2)
        ra_x=np.concatenate([x0+burst*.9,x1+burst*.9])
        ra=VGroup(baseline(-5.8,5.8,-1.05),train(ra_x,-1.05,1.25),T('rapidly adapting • change',28,GREEN).move_to([0,.5,0]))
        self.play(Create(ra),run_time=.6)
        self.at('Slowly adapting endings')
        times=firing(6,3.5,1.7,tau=2)
        sa_x=x0+times/6*(x1-x0)
        sa=VGroup(baseline(-5.8,5.8,-3),train(sa_x,-3,1.25),T('slowly adapting • held stimulus',28,GREEN).move_to([0,-1.45,0]))
        self.play(Create(sa),run_time=.7)
        self.at('keep firing')
        self.play(Indicate(sa[1],color=GREEN,scale_factor=1.02),run_time=.5)
        self.finish()


class S17Takeaway(SpokenScene):
    def construct(self):
        b,t,e,n,_,_=idea_box()
        box=VGroup(b,t,e,n)
        self.at('So a spike means')
        self.add(box)
        self.wait(2)
        line=VGroup(T('A spike means what',40),T('its neuron is tuned to.',40,GREEN)).arrange(DOWN,buff=.2).move_to([0,1.75,0])
        self.play(FadeOut(box),FadeIn(line),run_time=.45)
        self.at('Next')
        # Overlapping receptive fields, explicitly labelled as neighbours.
        units=VGroup()
        for x,label in [(-2.1,'A'),(0,'B'),(2.1,'C')]:
            units.add(VGroup(Circle(1.25,color=BLUE,fill_opacity=.07).move_to([x,-.8,0]),chip(label,GREY,28).move_to([x,-.8,0]),Line([x,-2.05,0],[x,-2.4,0],color=GREY)))
        self.play(FadeIn(units),run_time=.4)
        self.at('neighbors compare')
        self.play(FadeIn(T('Next: neighbours compare',30,BLUE).move_to([0,-3.15,0])),run_time=.4)
        self.wait(2.4)
        self.finish()


class S18End(EndCard):
    LINE='A spike means what its neuron is tuned to.'
