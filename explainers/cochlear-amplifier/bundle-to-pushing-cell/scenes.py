"""From a Bent Bundle to a Pushing Cell.
COLOR MAP: BLUE = cell / expanded prestin / bundle; GREEN = contracted prestin / NLC;
YELLOW = voltage / current / charge; TEAL = sound; RED = exclusions;
GREY = structures (secondary text uses bright #C3CBD6).
All traces are sampled equations; schematic motion has no implied physical scale.
"""
import os
from pathlib import Path
import numpy as np
from bp_style import *

VH, Z, KTE = -112., .70, 25.42
SECONDARY = '#C3CBD6'
LESSON_NAME = 'The Cochlear Amplifier and Otoacoustic Emissions'

def occ(v,z=Z):
    return 1/(1+np.exp(-z*(v-VH)/KTE))
def nlc(v,z=Z):
    f=occ(v,z)
    return 4*f*(1-f)
def label(s,x,y,size=28,color=TEXT):
    return T(s,size,color).move_to([x,y,0])
def header(s,color=TEXT):
    return label(s,0,3.16,32,color)
def model_note():
    # Fixed corner throughout s09–s17, above rather than below plot captions.
    return label('Two-state equilibrium model · 295 K',3.3,3.52,26,SECONDARY)
def axes(w=10.4,h=4.7,xr=(-260,36),yr=(0,1.08),center=(.3,0)):
    a=Axes(x_range=[*xr,1],y_range=[*yr,1],x_length=w,y_length=h,tips=False,
           axis_config={'include_ticks':False,'color':SECONDARY,'stroke_width':2})
    a.y_axis.set_stroke(opacity=0)
    a.add(Line(a.c2p(xr[0],yr[0]),a.c2p(xr[0],yr[1]),color=SECONDARY,stroke_width=2))
    return a.move_to([*center,0])
def curve(a,fn,xr=(-260,36),color=GREEN,w=5):
    xs=np.linspace(*xr,400)
    m=VMobject(color=color,stroke_width=w)
    m.set_points_as_corners([a.c2p(float(x),float(fn(x))) for x in xs])
    return m

def cell(x=0,y=-.8,h=3.5,w=1.8):
    return RoundedRectangle(width=w,height=h,corner_radius=.45,color=BLUE,
        fill_color=BLUE,fill_opacity=.17,stroke_width=5).move_to([x,y,0])
def bundle(x=0,base=.95,tilt=0,opening=0):
    b=VGroup()
    for i,h in enumerate([.85,1.25,1.65]):
        xx=x+(i-1)*.62
        tip=np.array([xx+tilt*h,base+h,0])
        b.add(Line([xx,base,0],tip,color=BLUE,stroke_width=13))
        # Enlarged green gates, all in one open/closed colour.
        b.add(Line(tip+LEFT*.22,tip+LEFT*.05+UP*.17*opening,color=GREEN,stroke_width=7),
              Line(tip+RIGHT*.22,tip+RIGHT*.05+DOWN*.17*opening,color=GREEN,stroke_width=7))
    return b

def chain(active=0):
    return VGroup(*[label(f'{i+1}  {s}',-5.1,1.7-i*.82,28,YELLOW if active==i+1 else SECONDARY)
                   for i,s in enumerate(['bundle','channel','voltage','prestin','push'])])
def motor(x=0,y=0,f=0,scale=1):
    return RoundedRectangle(width=(1.25+.27*f)*scale,height=(2.2-.5*f)*scale,
           corner_radius=.22,color=interpolate_color(ManimColor(BLUE),ManimColor(GREEN),f),fill_opacity=.6,
           fill_color=interpolate_color(ManimColor(BLUE),ManimColor(GREEN),f),stroke_width=4).move_to([x,y,0])
def wave(a,phase=0,cycles=3,amp=1):
    return curve(a,lambda t:amp*np.sin(2*PI*cycles*t+phase),(0,1),YELLOW)

class TimedScene(SpokenScene):
    """Log the actual post-wait cue time, not the pre-wait clock in bp_style.
    Quantized 15 fps waits lead speech by at most 0.12 s; no accumulated tail.
    """
    def at(self,phrase,lead=.12,nth=0):
        target=self.t_of(phrase,nth)
        rest=max(0,target-lead-self.elapsed())
        if rest>.001:
            self.wait(rest)
        with open(Path(__file__).parent/'frames'/'sync.log','a') as f:
            f.write(f'{os.environ["KX_SCENE_ID"]} | {phrase} | word={target:.3f} visual={self.elapsed():.3f}\n')
    def finish(self):
        if self.narration_s>self.elapsed():
            self.wait(self.narration_s-self.elapsed())

def pair_plots():
    a=axes(10.3,2.05,center=(.6,1.70))
    b=axes(10.3,2.05,center=(.6,-1.35))
    labs=VGroup(label('charge',-5.5,2.64,26,YELLOW),label('NLC',-5.7,-.21,26,GREEN),
        label('membrane voltage',.6,-2.72,26,YELLOW),
        label('Nonlinear component · normalized to its own peak',0,-3.19,26,SECONDARY))
    return a,b,curve(a,occ,color=YELLOW),curve(b,nlc),labs

def predict():
    g=VGroup(header('Predict: wider or narrower?').shift(DOWN*.35),model_note())
    for x,z in [(-3.1,.7),(3.1,1.4)]:
        g.add(RoundedRectangle(width=5.35,height=3.9,corner_radius=.15,color=SECONDARY).move_to([x,.1,0]),
              label(f'z = {z:.2f}',x,2.4,32,YELLOW),label('?',x,.1,76,GREEN))
    g.add(label('If z doubles, what happens to the bell?',0,-2.6,28))
    return g

def reveal():
    a,b,s,c,l=pair_plots()
    s.set_color(SECONDARY);c.set_color(SECONDARY)
    g=VGroup(a,b,s,c,l,model_note(),curve(a,lambda v:occ(v,1.4),color=GREEN),curve(b,lambda v:nlc(v,1.4)),
        label('width ∝ 1/z',-3.95,3.2,28),
        label('z = 0.70',3.85,1.05,26,SECONDARY),label('z = 1.40',3.85,1.72,26,GREEN))
    # Both brackets mark the actual half-height crossings; labels stay local.
    for z,col in [(.7,SECONDARY),(1.4,GREEN)]:
        width=4*KTE*np.arccosh(np.sqrt(2))/z
        x1,x2=VH-width/2,VH+width/2
        p1,p2=b.c2p(x1,.5),b.c2p(x2,.5)
        g.add(Line(p1,p2,color=col,stroke_width=4))
        for p in [p1,p2]:
            g.add(Line(p+UP*.10,p+DOWN*.10,color=col))
        txt=label(f'{round(width)} mV',0,0,26,col)
        if z==.7:
            txt.next_to(p1,LEFT,buff=.16)
        else:
            txt.next_to((p1+p2)/2,DOWN,buff=.16)
        g.add(txt)
    g.add(label('z = 0.70',-3.8,-.47,26,SECONDARY),label('z = 1.40',3.9,-.47,26,GREEN))
    p=b.c2p(-240,.06); q=b.c2p(-190,.06)
    g.add(Line(p,q,color=TEXT,stroke_width=4),label('50 mV',float((p[0]+q[0])/2),-2.65,26))
    return g

def worked_axes():
    a=axes(10.3,4.1,center=(.45,.1))
    g=VGroup(a,curve(a,nlc),model_note(),label('normalized NLC',-4.85,2.64,26,GREEN),
        label('membrane voltage',.45,-2.78,26,YELLOW),
        label('Linear capacitance excluded',-3.8,-3.27,26,SECONDARY))
    for y in [1,.64]:
        p=a.c2p(-260,y)
        g.add(Line(p+LEFT*.1,p+RIGHT*.1,color=TEXT),label('1.0' if y==1 else '0.64',p[0]-.5,p[1],26))
    g.add(DashedLine(a.c2p(VH,0),a.c2p(VH,1),color=SECONDARY),
        label('Vh = −112 mV',-2,-2.32,26,SECONDARY))
    return a,g

class S00Title(TitleCard):
    LESSON=LESSON_NAME
    TITLE='From a Bent Bundle to a Pushing Cell'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.5,28,TEAL),label(self.LESSON,0,1.5,27,SECONDARY))
        self.play(FadeIn(label('From a Bent Bundle\nto a Pushing Cell',0,-.15,48)),run_time=.6)
        self.wait(2.4)

class S01Q(TimedScene):
    def construct(self):
        t=ValueTracker(0)
        c=always_redraw(lambda:cell(-3.6,-.45,3.8-.45*np.sin(t.get_value())))
        b=always_redraw(lambda:bundle(-3.6,1.45-.225*np.sin(t.get_value())).scale(.6,about_point=[-3.6,1.45-.225*np.sin(t.get_value()),0]))
        a=axes(6,4.6,(0,1),(-1.1,1.1),(2.5,-.1))
        w=always_redraw(lambda:wave(a,t.get_value(),4))
        self.add(c,b,a,w,header('Many thousands of pushes a second?',YELLOW))
        self.at('How does one')
        self.play(t.animate.set_value(4*PI),run_time=4.1,rate_func=linear)
        self.finish()

class S02C1(TimedScene):
    def construct(self):
        u=ValueTracker(0); opened=ValueTracker(0)
        b=always_redraw(lambda:bundle(1,.9,u.get_value(),opened.get_value()))
        count=always_redraw(lambda:VGroup(Rectangle(width=3,height=.28,color=GREEN).move_to([4.1,-.6,0]),
            Rectangle(width=max(.05,3*(u.get_value()+.5)),height=.28,stroke_width=0,fill_color=GREEN,fill_opacity=1).align_to(Rectangle(width=3,height=.28).move_to([4.1,-.6,0]),LEFT).set_y(-.6)))
        c=chain()
        self.add(c,cell(1,-.85,3.5,2.5),b,header('Five links: bundle → push'))
        self.at('Sound bends')
        self.play(Transform(c,chain(1)),u.animate.set_value(.42),run_time=.6)
        self.play(u.animate.set_value(-.42),run_time=.6)
        self.at('Bending toward the tallest')
        self.add(label('toward tallest →',4,2.3,27,BLUE))
        self.play(u.animate.set_value(.42),run_time=.6)
        self.at('opens more')
        more=label('more channels open',4.05,1.25,26,GREEN)
        self.add(count,more,label('open channels',4.1,-1.2,26,GREEN))
        self.play(Transform(c,chain(2)),opened.animate.set_value(1),run_time=.4)
        self.play(u.animate.set_value(-.42),opened.animate.set_value(0),Transform(more,label('fewer channels open',4.05,1.25,26,GREEN)),run_time=.55)
        self.play(u.animate.set_value(.42),opened.animate.set_value(1),Transform(more,label('more channels open',4.05,1.25,26,GREEN)),run_time=.55)
        self.finish()

class S03C2(TimedScene):
    def construct(self):
        ch=chain(2)
        self.add(ch,cell(-1.6,-.85),bundle(-1.6,.9,.3,1))
        self.at('Current flows in')
        self.play(GrowArrow(Arrow([.05,2.4,0],[-.9,.65,0],color=YELLOW,buff=.1)),Transform(ch,chain(3)),run_time=.4)
        self.at('so the voltage')
        a=axes(5.8,3.7,(0,1),(-1.1,1.1),(3.3,.2));self.add(a,label('voltage',3.3,2.5,28,YELLOW))
        self.play(Create(wave(a,cycles=2)),run_time=1.3)
        self.at('The voltage moves charge')
        m=motor(-.7,-.8,scale=.55)
        self.play(FadeIn(m),FadeIn(label('prestin',.8,-1.9,28,BLUE)),Create(Line([.3,-1.65,0],[-.6,-1,0],color=BLUE)),Transform(ch,chain(4)),run_time=.4)
        q=Dot(m.get_top()+DOWN*.25,color=YELLOW,radius=.12)
        self.add(q);self.play(q.animate.shift(DOWN*.45),run_time=.5)
        self.at('which changes shape')
        self.play(Transform(m,motor(-.7,-.8,1,.55)),run_time=.6)
        self.finish()

class S04C3(TimedScene):
    def construct(self):
        u=ValueTracker(0);ch=chain(5)
        c=always_redraw(lambda:cell(-1.6,-.65-u.get_value()/2,3.8-u.get_value()))
        # Plates flank the cell body; omit the bundle so it cannot stand on a plate.
        top=always_redraw(lambda:Line([-3,1.25-u.get_value(),0],[-.2,1.25-u.get_value(),0],color=SECONDARY,stroke_width=12))
        bottom=Line([-3,-2.55,0],[-.2,-2.55,0],color=SECONDARY,stroke_width=12)
        a=axes(4.7,3.1,(0,1),(-1.1,1.1),(3.7,.1))
        d=always_redraw(lambda:Dot(a.c2p(.75+u.get_value()/1.6,np.sin(2*PI*(.75+u.get_value()/1.6))),color=YELLOW,radius=.12))
        self.add(ch,c,top,bottom,a,wave(a,cycles=1),d,label('voltage',3.6,2.2,28,YELLOW))
        self.at('The cell shortens')
        cue=label('↓ shorten',3.6,-2,28,BLUE);self.add(cue)
        self.play(u.animate.set_value(.8),run_time=.8)
        self.at('and lengthens')
        self.play(u.animate.set_value(0),Transform(cue,label('↑ lengthen',3.6,-2,28,BLUE)),run_time=.7)
        self.at('and pushes')
        self.add(label('organ of Corti',-.7,2.6,28,SECONDARY),Line([-.7,2.3,0],[-1.3,1.4,0],color=SECONDARY),
            Arrow([-.1,.8,0],[-.1,1.8,0],color=BLUE,buff=.05),Arrow([-.1,-1.8,0],[-.1,-2.9,0],color=BLUE,buff=.05))
        self.play(u.animate.set_value(.6),run_time=.5);self.play(u.animate.set_value(0),run_time=.5)
        self.finish()

class S05Speed(TimedScene):
    def construct(self):
        self.add(header('Why voltage?'))
        a=axes(11.6,4.35,(0,150),(-1.1,1.1),(0,-.05))
        w=curve(a,lambda t:np.sin(2*PI*t/50),(0,150),YELLOW)
        self.add(a,w,label('time (µs)',4.8,-3.45,28,YELLOW))
        for t in [0,50,100,150]:
            tick=a.c2p(t,-1.1)
            self.add(Line(tick,tick+DOWN*.12,color=SECONDARY),label(str(t),tick[0],tick[1]-.30,26))
        self.at('20 kilohertz')
        self.add(label('20 kHz',-4.6,2.6,32,YELLOW))
        theta=ValueTracker(0)
        clock=Circle(radius=.78,color=YELLOW).move_to([4.8,2.7,0])
        hand=always_redraw(lambda:Line(clock.get_center(),clock.get_center()+.69*np.array([np.sin(theta.get_value()),np.cos(theta.get_value()),0]),color=YELLOW))
        self.add(clock,hand)
        self.at('completes a cycle')
        dot=Dot(a.c2p(0,0),color=YELLOW)
        self.add(dot)
        self.play(MoveAlongPath(dot,curve(a,lambda t:np.sin(2*PI*t/50),(0,50),YELLOW)),theta.animate.set_value(2*PI),run_time=.9,rate_func=linear)
        self.at('every 50')
        p,q=a.c2p(0,-1.55),a.c2p(50,-1.55)
        self.add(Line(p,q,color=YELLOW),Line(p+UP*.12,p+DOWN*.12,color=YELLOW),Line(q+UP*.12,q+DOWN*.12,color=YELLOW),
            label('one cycle = 50 µs',0,-3.45,34,YELLOW))
        self.finish()

class S06Atp(TimedScene):
    def construct(self):
        t=ValueTracker(0)
        a=axes(11.4,2.7,(0,1),(-1.1,1.1),(0,1.35))
        w=always_redraw(lambda:wave(a,t.get_value(),4))
        p=always_redraw(lambda:motor(-3,-1.55,(1+np.sin(t.get_value()))/2,1.05))
        dot=always_redraw(lambda:Dot(a.c2p(.25,np.sin(t.get_value())),color=YELLOW,radius=.13))
        self.add(a,w,p,dot,label('voltage',-5,3.1,28,YELLOW),label('prestin',-3,-3.1,30,BLUE))
        self.at('An amplifier working')
        self.play(t.animate.set_value(4*PI),run_time=2.05,rate_func=linear)
        self.at('cannot wait')
        slow=chip('slow chemical step',SECONDARY,28).move_to([2.5,-1.2,0])
        self.add(slow)
        lag=Dot([.5,-2.1,0],color=SECONDARY,radius=.14);self.add(lag)
        self.play(t.animate.set_value(8*PI),lag.animate.shift(RIGHT*.5),run_time=2.3,rate_func=linear)
        self.at('such as')
        self.add(label('ATP hydrolysis',2.5,-2.55,28,SECONDARY),label('×',5.7,-1.2,64,RED))
        self.play(t.animate.set_value(10*PI),run_time=1.2,rate_func=linear)
        self.finish()

class S07Rc(TimedScene):
    def construct(self):
        self.add(header('Membrane resistance + capacitance',YELLOW))
        # Passive RC response: f/fc = r, |H|=1/sqrt(1+r²); no invented absolute cutoff.
        panels=[]
        for x,r,name in [(-4.2,.3,'low'),(0,1.2,'higher'),(4.2,4,'highest')]:
            a=axes(3.6,4,(0,4),(-1.1,1.1),(x,.3))
            g=VGroup(a,label(f'{name}: f/fc = {r:g}',x,2.65,26,YELLOW),label('time',x,-2,26,SECONDARY))
            for y in [-1,1]:g.add(DashedLine(a.c2p(0,y),a.c2p(4,y),color=SECONDARY,stroke_opacity=.6))
            tr=curve(a,lambda t,r=r:np.sin(2*PI*r*t)/np.sqrt(1+r*r),(0,4),YELLOW)
            panels.append((g,tr))
        self.add(*[g for g,tr in panels],panels[0][1])
        self.at('The membrane smooths')
        self.add(label('f = input frequency · fc = membrane cutoff',0,-2.55,27,SECONDARY))
        self.play(Create(panels[1][1]),run_time=1.2)
        self.at('In simple estimates')
        self.play(Create(panels[2][1]),run_time=1.2)
        self.at('far below')
        msg=label('Simple cutoff estimate: far below high basal frequencies',0,-3.25,27)
        self.add(msg)
        self.at('How much that limits')
        self.play(FadeOut(msg),FadeIn(label('Impact still argued · Altoè & Shera, 2023',0,-3.25,28,RED)),run_time=.35)
        self.finish()

class S08Q2(TimedScene):
    def construct(self):
        a=axes(7.2,4.8,center=(2,.0))
        c=cell(-4.55,-.25,4.5)
        pip=Polygon([-2.6,2.8,0],[-2.2,2.4,0],[-3.65,1,0],color=YELLOW,fill_color=YELLOW,fill_opacity=.25)
        self.add(c,pip,a,label('charge',-.7,2.65,28,YELLOW),label('membrane voltage',2,-2.85,28,YELLOW),
            label('voltage clamp:',-4.3,-2.85,26,YELLOW),label('hold at chosen voltages',-4.3,-3.3,26,SECONDARY))
        self.at('How can you watch')
        # Measured samples represented by the same two-state equation used in the next scene.
        dots=VGroup(*[Dot(a.c2p(v,occ(v)),color=YELLOW,radius=.09) for v in [-230,-180,-130,-80,-30,20]])
        # Command voltage is separate from the cell and the measured charge.
        steps=VGroup()
        for i in range(6):
            x=-2.9+i*.35; y=2.8+i*.10
            steps.add(Line([x,y,0],[x+.35,y,0],color=YELLOW,stroke_width=4))
            if i<5:
                steps[-1].add(Line([x+.35,y,0],[x+.35,y+.10,0],color=YELLOW,stroke_width=4))
        self.add(label('voltage steps',-2,3.55,26,YELLOW))
        self.at('Measure capacitance')
        self.play(FadeIn(label('C = dQ/dV',2.6,3.15,38,GREEN)),run_time=.35)
        for step,dot in zip(steps,dots):
            self.play(Create(step),FadeIn(dot),run_time=.25)
        self.finish()

class S09S(TimedScene):
    def construct(self):
        a=axes(7.5,4.65,center=(2,-.05));v=ValueTracker(-250);x=ValueTracker(0)
        self.add(model_note())
        p=always_redraw(lambda:motor(x.get_value(),.5,occ(v.get_value()),1.45+.3*x.get_value()/4.6))
        name=label('prestin',0,2.65,30,BLUE)
        self.at('In the simplest model')
        self.add(p,name)
        self.at('flips between two states')
        states=VGroup(motor(-3.7,.5,0,.75),label('expanded',-3.7,-.7,28,BLUE),
                      motor(3.7,.5,1,.75),label('contracted',3.7,-.7,28,GREEN))
        self.add(states)
        self.play(v.animate.set_value(30),run_time=.45)
        self.play(v.animate.set_value(-250),run_time=.45)
        self.at('voltage tilts the odds')
        self.play(x.animate.set_value(-4.6),name.animate.move_to([-4.6,2.65,0]),FadeOut(states),run_time=.3)
        self.add(motor(-5.55,-1.1,0,.38),label('expanded',-5.55,-1.8,22,BLUE),
                 motor(-3.7,-1.1,1,.38),label('contracted',-3.7,-1.8,22,GREEN))
        slider=Line([-6.15,-2.5,0],[-2.95,-2.5,0],color=YELLOW,stroke_width=5)
        d=always_redraw(lambda:Dot(slider.point_from_proportion(np.clip((v.get_value()+260)/296,0,1)),color=YELLOW))
        bar=always_redraw(lambda:Rectangle(width=max(.02,3.2*occ(v.get_value())),height=.42,fill_color=GREEN,fill_opacity=1,stroke_width=0).move_to([-6.15+1.6*occ(v.get_value()),-3.2,0]))
        self.add(slider,d,Rectangle(width=3.2,height=.42,color=GREEN).move_to([-4.55,-3.2,0]),bar,
                 label('voltage',-4.55,-2.12,24,YELLOW),label('contracted occupancy',-4.55,-3.7,24,GREEN))
        self.play(v.animate.set_value(30),run_time=.8)
        self.at('So its charge moves')
        self.add(a,label('charge',-1.6,2.55,28,YELLOW),label('membrane voltage',2,-2.85,28,YELLOW))
        self.play(v.animate.set_value(-250),run_time=.2)
        tr=always_redraw(lambda:curve(a,occ,(-260,max(-259,v.get_value())),YELLOW))
        dot=always_redraw(lambda:Dot(a.c2p(v.get_value(),occ(v.get_value())),color=YELLOW))
        self.add(tr,dot)
        self.play(v.animate.set_value(36),run_time=2.2,rate_func=linear)
        self.at('mostly near its midpoint')
        shade=Polygon(a.c2p(VH-30,0),a.c2p(VH+30,0),a.c2p(VH+30,1.05),a.c2p(VH-30,1.05),stroke_width=0,fill_color=YELLOW,fill_opacity=.12)
        self.add(shade,DashedLine(a.c2p(VH,0),a.c2p(VH,1.05),color=SECONDARY),label('midpoint',4.4,-.4,26,SECONDARY),
            Line([3.65,-.4,0],a.c2p(VH,.5),color=SECONDARY,stroke_width=2))
        self.finish()

class S10Bell(TimedScene):
    def construct(self):
        a,b,s,c,l=pair_plots();v=ValueTracker(-255)
        self.add(a,b,s,l,model_note())
        tangent=always_redraw(lambda:Line(a.c2p(v.get_value()-36,occ(v.get_value())-36*Z/KTE*occ(v.get_value())*(1-occ(v.get_value()))),a.c2p(v.get_value()+36,occ(v.get_value())+36*Z/KTE*occ(v.get_value())*(1-occ(v.get_value()))),color=TEXT,stroke_width=5))
        self.at('The slope of')
        self.add(tangent)
        self.play(v.animate.set_value(VH),run_time=1.9,rate_func=linear)
        self.at('So the extra')
        # Name the plotted quantity before constructing it; formal name arrives on its own cue.
        nlc_title=label('Nonlinear capacitance (NLC)',.6,.08,28,GREEN)
        self.add(nlc_title)
        partial=always_redraw(lambda:curve(b,nlc,(-260,max(-259,v.get_value())),GREEN))
        v.set_value(-255);self.add(partial)
        self.play(v.animate.set_value(30),run_time=1.8,rate_func=linear)
        self.remove(partial)
        self.add(c)
        self.play(v.animate.set_value(VH),run_time=.4)
        self.at('called nonlinear')
        self.play(Indicate(nlc_title,scale_factor=1.03),run_time=.35)
        self.finish()

class S11Z(TimedScene):
    def construct(self):
        a,b,s,c,l=pair_plots();self.add(a,b,s,c,l,model_note())
        self.at('Its steepness')
        slope=Line(a.c2p(VH-25,.5-25*Z/KTE*.25),a.c2p(VH+25,.5+25*Z/KTE*.25),color=TEXT,stroke_width=8)
        self.play(Create(slope),Indicate(s,color=YELLOW,scale_factor=1.025),run_time=1)
        self.at('the effective charge')
        self.add(label('z = effective charge moved per prestin',-.7,3.05,28,YELLOW))
        self.play(Indicate(slope,scale_factor=1.2),run_time=.9)
        self.finish()

class S12Predict(TimedScene):
    def construct(self):
        self.add(predict());self.at('Predict');self.finish()
class S13Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(predict())
        for i in range(5,0,-1):
            t=label(f'Pause and think · {i}',0,-3.15,28,TEAL)
            self.add(t);self.wait(1);self.remove(t)
class S14Reveal(TimedScene):
    def construct(self):
        a,b,s,c,l=pair_plots();self.add(a,b,s,c,l,model_note())
        self.at('Nervower');self.add(label('Narrower',-4.5,3.15,30,GREEN))
        self.at('A larger')
        self.play(s.animate.set_color(SECONDARY),c.animate.set_color(SECONDARY),Create(curve(a,lambda v:occ(v,1.4),color=GREEN)),Create(curve(b,lambda v:nlc(v,1.4))),run_time=1.2)
        self.at('The width of');self.clear();self.add(reveal());self.finish()
class S15Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(reveal());self.wait(2)

class S16Worked(TimedScene):
    def construct(self):
        a,g=worked_axes();self.add(g)
        self.at('Take the gerbil fit')
        self.add(label('Gerbil fit · z = 0.70',-3.9,3.16,30))
        self.at('At 50 millivolts')
        p=Dot(a.c2p(-62,nlc(-62)),color=YELLOW,radius=.13)
        self.add(p,DashedLine(a.c2p(-62,0),p.get_center(),color=YELLOW),label('−62 mV',1.9,-2.32,26,YELLOW))
        p1,p2=a.c2p(VH,1.06),a.c2p(-62,1.06)
        self.add(Line(p1,p2,color=YELLOW),Line(p1+UP*.1,p1+DOWN*.1,color=YELLOW),Line(p2+UP*.1,p2+DOWN*.1,color=YELLOW),
            label('+50 mV',.9,2.65,28,YELLOW))
        self.at('about 80')
        self.add(label('f = 0.798 (about 80 %)',3.9,1.1,28,GREEN),label('contracted',4.2,.55,26,GREEN))
        self.at('The bell there')
        self.add(DashedLine(a.c2p(-260,nlc(-62)),p.get_center(),color=GREEN),label('NLC = 4f(1 − f) = 0.64 of peak',2.8,-3.27,27,GREEN))
        self.finish()
class S17Limit(TimedScene):
    def construct(self):
        a,g=worked_axes();self.add(g)
        self.at('This reads charge movement')
        self.add(label('✓',2.35,1.9,46,GREEN),label('charge movement',2.8,1.9,29,GREEN).align_to([2.8,1.9,0],LEFT))
        self.at('not the force')
        self.add(label('×',2.35,.95,48,RED),label('force / power',2.8,.95,29,SECONDARY).align_to([2.8,.95,0],LEFT))
        self.finish()

class S18Struct(TimedScene):
    def construct(self):
        self.add(header('Purified prestin · schematic dimer',BLUE),label('membrane',0,-2.2,28,SECONDARY),label('not to scale',-4.7,2.25,28,SECONDARY))
        membrane=Rectangle(width=12.3,height=5.25,color=SECONDARY,fill_color=SECONDARY,fill_opacity=.1)
        self.add(membrane)
        def dimer(x=0,w=1.65):
            return VGroup(*[RoundedRectangle(width=w,height=3.5,corner_radius=.25,color=BLUE,fill_color=BLUE,fill_opacity=.5).move_to([x+dx,0,0]) for dx in [-w*.55,w*.55]])
        d=dimer();self.add(d)
        self.at('Structures of purified')
        self.play(Transform(d,dimer(w=1.8)),run_time=.8);self.play(Transform(d,dimer()),run_time=.8)
        self.at('suggest an area motor')
        self.play(Transform(d,dimer(w=1.8)),run_time=.7);self.play(Transform(d,dimer()),run_time=.7)
        self.at('But each is')
        self.play(Transform(d,dimer(-2.9,1.4)),FadeIn(dimer(2.9,1.52)),run_time=.5)
        self.add(label('chloride · contracted',-2.9,-2.95,27,SECONDARY),label('salicylate · expanded',2.9,-2.95,27,SECONDARY))
        self.at('not a working')
        self.add(label('End states, not a movie',0,-3.6,31,RED));self.finish()

class S19Need(TimedScene):
    def construct(self):
        self.add(header('Is the motor needed?'))
        c=cell(-4.1,-.05,4.8,2.1)
        self.add(c,bundle(-4.1,2.35).scale(.5,about_point=[-4.1,2.35,0]),label('outer hair cell',-4.1,-2.85,28,BLUE))
        self.at('In a')
        self.add(label('prestin knock-in mouse',1.3,2.35,32,BLUE))
        self.at('transduction and')
        self.add(label('✓',-1.45,1.15,48,GREEN),label('transduction normal',2,1.15,30,GREEN))
        self.at('cell mechanics')
        self.add(label('✓',-1.45,.15,48,GREEN),label('cell mechanics normal',2,.15,30,GREEN))
        self.at('Yet amplification')
        self.add(label('×',-1.45,-1.1,54,RED),label('amplification lost',2,-1.1,32,RED),label('much as in a knockout',2,-1.85,28,SECONDARY))
        self.finish()

class S20Need2(TimedScene):
    def construct(self):
        self.add(header('Two preparations, different evidence'))
        u=ValueTracker(0)
        c=always_redraw(lambda:cell(0,-.35,3.8-.45*np.sin(u.get_value()),2.3))
        self.add(c,label('Cell-body motility is necessary',0,-3,30,BLUE),label('Dallos and colleagues, 2008',0,2.45,28,SECONDARY))
        self.at('So the cell')
        self.play(u.animate.set_value(4*PI),run_time=2.5,rate_func=linear)
        self.at('In an excised frog organ')
        self.remove(c);self.clear()
        frogtitle=header('Excised bullfrog sacculus',YELLOW)
        self.add(frogtitle,label('excised preparation',0,-3.15,29,SECONDARY))
        tilt=ValueTracker(0)
        self.add(cell(0,-1.35,2.6,3),always_redraw(lambda:bundle(0,-.05,tilt.get_value(),.6)))
        self.play(tilt.animate.set_value(.28),run_time=.45);self.play(tilt.animate.set_value(-.28),run_time=.45)
        self.at('can also add')
        self.play(Transform(frogtitle,header('In excised bullfrog: bundle can add energy',YELLOW)),run_time=.25)
        self.add(Arrow([2.1,.5,0],[3.9,.5,0],color=YELLOW),label('energy out',4,1.2,28,YELLOW))
        self.play(tilt.animate.set_value(.28),run_time=.4);self.play(tilt.animate.set_value(-.28),run_time=.4)
        self.finish()

class S21Split(TimedScene):
    def construct(self):
        self.add(header('Work in mammalian hair cells'))
        self.add(cell(2.5,-.4,4.5,2.7),bundle(2.5,1.85).scale(.45,about_point=[2.5,1.85,0]),
            cell(-3.9,-1.3,1.6,1.8),bundle(-3.9,-.5).scale(.8,about_point=[-3.9,-.5,0]),
            label('bundle: possible partner',-3.8,-2.98,28,BLUE),label('cell-body motor',2.6,-2.98,28,BLUE),
            label('prestin motility is necessary',2.6,-3.55,28,GREEN))
        self.at('How the work is split')
        self.at('has not been established')
        self.play(Transform(self.mobjects[0],header('Split in mammals: not established',RED)),run_time=.35)
        self.finish()

class S22Take(TimedScene):
    def construct(self):
        self.add(header('Take this with you'))
        row=VGroup(*[chip(s,SECONDARY,28) for s in ['bundle','channel','voltage','prestin','push']]).arrange(RIGHT,buff=.5).move_to([0,1.8,0])
        self.add(row)
        arrows=VGroup(*[Arrow(row[i].get_right(),row[i+1].get_left(),buff=.04,color=SECONDARY,stroke_width=3,max_tip_length_to_length_ratio=.3) for i in range(4)])
        self.add(arrows)
        for i,phrase in enumerate(['bundle','channel','voltage','Preston','push']):
            self.at(phrase)
            self.play(row[i].animate.set_color(YELLOW),run_time=.13)
            self.play(row[i].animate.set_color(SECONDARY),run_time=.13)
        self.at('the bell')
        a=axes(10.4,3.6,center=(.4,-.8))
        self.add(a,label('normalized NLC',-4.3,1.15,26,GREEN),label('membrane voltage',.4,-2.95,28,YELLOW))
        self.play(Create(curve(a,nlc)),run_time=1.2)
        self.at('electrical fingerprint')
        self.add(label('The bell is the motor’s electrical fingerprint.',0,-3.5,28,GREEN))
        self.finish()

class S23End(EndCard):
    LINE='The bell is the motor’s electrical fingerprint.'
    def construct(self):
        self.add(label(self.LINE,0,.3,36),label('biochemistrypedia.com',0,-.6,28,TEAL))
        self.wait(self.narration_s)
