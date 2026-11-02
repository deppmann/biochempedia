"""Rebuilt stretch-reflex chapter, locked to the existing narration.
COLOR MAP: BLUE neurons/axons; GREEN excitation; RED inhibition/antagonist;
YELLOW stretch and ALL spikes; TEAL spindle; GREY resting muscle/structure;
GOLD Golgi tendon organ. Labels are white unless they carry a concept colour.

Bars use the lesson's passive conductance model: V=(gL*EL+gI*EI+I)/(gL+gI).
Rasters use an explicit illustrative leaky integrate-and-fire model (not data):
20 ms membrane time constant, -70 mV rest/reset, -60 mV threshold, 3 ms refractory.
Sensor drive is proportional to positive thread tension / tendon pull. No
hand-drawn voltage curves, event times or sensor-specific spike colours.
"""
import numpy as np
from bp_style import *


def P(x,y): return np.array([x,y,0.])

def label(s,x,y,color=TEXT,size=28):
    t=T(s,size,color).move_to(P(x,y))
    t.add_background_rectangle(color=BG,opacity=1,buff=.055)
    return t

def heading(s): return label(s,0,3.12,size=34)

def poly(pts,color=BLUE,w=7):
    m=VMobject(stroke_color=color,stroke_width=w)
    m.set_points_as_corners([P(*p) for p in pts]); return m

def capsule(w,h,color=GREY):
    return RoundedRectangle(width=w,height=h,corner_radius=min(.3,h/2),stroke_color=color,
                            stroke_width=4,fill_color=color,fill_opacity=.12)

def leader(text,x,y,end,color=TEXT,size=28):
    t=label(text,x,y,color,size)
    start=t.get_left() if end[0]<x else t.get_right()
    return VGroup(Line(start,end,color=color,stroke_width=2),t)

def excite(a,b):
    a,b=np.array(a),np.array(b); d=b-a
    tip=Triangle(color=GREEN,fill_color=GREEN,fill_opacity=1,stroke_width=0).scale(.23)
    tip.rotate(np.arctan2(d[1],d[0])-PI/2).move_to(b)
    return VGroup(Line(a,b,color=BLUE,stroke_width=7),tip)

def inhibit(a,b):
    a,b=np.array(a),np.array(b); d=(b-a)/np.linalg.norm(b-a); n=np.array([-d[1],d[0],0])
    return VGroup(Line(a,b,color=RED,stroke_width=8),Line(b-.35*n,b+.35*n,color=RED,stroke_width=10))

def pulses(scene,path,n=3,duration=.9):
    if not path.has_points(): path=path[0]
    dots=VGroup(*[Dot(radius=.14,color=YELLOW) for _ in range(n)])
    scene.add(dots)
    scene.play(LaggedStart(*[MoveAlongPath(d,path,rate_func=linear) for d in dots],lag_ratio=.25),run_time=duration)
    scene.remove(*dots,dots)


def spindle(width=8,slack=False,contracted=False):
    shell=capsule(width,1.3,TEAL)
    a=width/2-.16
    thread=poly([(-a,0),(-.8,0),(0,-.48 if slack else 0),(.8,0),(a,0)],TEAL,6)
    length=width*.26*(.45 if contracted else 1)
    c=a-length/2
    ends=VGroup(capsule(length,.45,BLUE).move_to(P(-c,0)),capsule(length,.45,BLUE).move_to(P(c,0)))
    return VGroup(shell,thread,ends)

def coil():
    # Projected helix around the centre of a fibre; geometric anatomy, not a trace.
    return ParametricFunction(lambda t:P(1.35*(t/(10*PI)-.5),.3*np.sin(t)),t_range=[0,10*PI,.04],color=BLUE,stroke_width=5)

def muscle(width=10,height=4.7):
    body=capsule(width,height,GREY)
    fibres=VGroup(*[Line(P(-width/2+.25,y),P(width/2-.25,y),color=GREY,stroke_width=10)
                    for y in [-1.85,-1.22,-.86,.86,1.22,1.85]])
    return VGroup(body,fibres)


def voltage(current=4.,gi=0.): return (.5*-70+gi*-80+current)/(.5+gi)

def events(drive,duration=1.):
    dt=.0005; v=-70.; refractory=0.; times=[]
    for t in np.arange(0,duration,dt):
        if refractory>0: refractory-=dt; continue
        v+=dt/.02*(-70+2*drive-v)
        if v>=-60:
            times.append(t);v=-70;refractory=.003
    return times

def raster(active=True,y=-2.6,x=0,width=9,height=1.,drive=7.,name=True):
    base=Line(P(x-width/2,y),P(x+width/2,y),color=GREY,stroke_width=2)
    # Event times, including the quiet case, are computed by the same model.
    ticks=VGroup(*[Line(P(x-width/2+t*width,y),P(x-width/2+t*width,y+height),color=YELLOW,stroke_width=4)
                   for t in events(drive if active else 0)])
    text=label('spikes, over time →',x,y-.4,size=26) if name else VGroup()
    return VGroup(base,ticks,text)

def meter(x=4.7,y=0,current=4.,gi=0.,color=BLUE,show_model=True):
    # Map -80..-50 mV into the 2.4-unit schematic bar; threshold is -60 mV.
    bottom=y-1.2; h=max(.05,(voltage(current,gi)+80)/30*2.4)
    box=Rectangle(width=1.15,height=2.4,color=GREY).move_to(P(x,y))
    fill=Rectangle(width=.99,height=h,stroke_width=0,fill_color=color,fill_opacity=.7).move_to(P(x,bottom+h/2))
    threshold=DashedLine(P(x-.75,bottom+1.6),P(x+.75,bottom+1.6),color=YELLOW)
    texts=VGroup(label('membrane',x,y+2.6,size=26),label('voltage',x,y+2.17,size=26),
                 label('threshold',x,y+1.5,YELLOW,26),label('illustrative model',x,y-1.62,size=26).set_opacity(1 if show_model else 0))
    return VGroup(box,fill,threshold,texts)


def leg(answer=False):
    # Large seated profile; the labels belong to the thigh, the shin pivots at knee.
    thigh=capsule(5.5,2.15,GREY).move_to(P(-1.3,1.65))
    quad=capsule(4.6,.62,GREEN if answer else GREY).move_to(P(-1.3,2.19))
    ham=capsule(4.6,.62,RED if answer else GREY).move_to(P(-1.3,1.08))
    knee=Circle(.4,color=GREY).move_to(P(1.6,1.65))
    shin=VGroup(Line(P(1.6,1.65),P(1.6,-2.95),color=GREY,stroke_width=25),
                Line(P(1.6,-2.95),P(2.9,-2.95),color=GREY,stroke_width=17))
    labels=VGroup(label('Quadriceps',-1.3,2.2,size=30),label('Hamstrings',-1.3,1.08,size=30))
    return VGroup(thigh,quad,ham,knee,shin,labels)


def cord(x=0,r=3.6):
    outline=Circle(r,color=GREY,fill_color=GREY,fill_opacity=.05).move_to(P(x,0))
    # Symmetric butterfly: narrow dorsal horns above, broad ventral horns below.
    pts=[(-.3,1.5),(-1.2,2.65),(-1.6,2.3),(-1.15,.55),(-2.2,-1.5),(-1.45,-2.35),
         (-.35,-1.2),(.35,-1.2),(1.45,-2.35),(2.2,-1.5),(1.15,.55),(1.6,2.3),(1.2,2.65),(.3,1.5)]
    butterfly=Polygon(*[P(x+a*r/3.6,b*r/3.6) for a,b in pts],stroke_color=GREY,stroke_width=2,fill_color=GREY,fill_opacity=.1)
    mid=DashedLine(P(x,-r*.97),P(x,r*.97),color=GREY,stroke_width=2)
    return VGroup(outline,butterfly,mid)


class Circuit:
    def __init__(self,stage=3):
        self.cord=cord()
        self.tint=Sector(radius=3.55,start_angle=PI/2,angle=PI,fill_color=BLUE,fill_opacity=.07,stroke_width=0)
        self.aff=poly([(-5.9,2.5),(-2.65,2.5),(-2.65,1.9)])
        self.br1=excite(P(-2.65,1.9),P(-2.1,-.35))
        self.br2=excite(P(-2.65,1.9),P(-1.65,1.2))
        self.quad=Circle(.48,color=BLUE,stroke_width=5,fill_color=GREEN,fill_opacity=.2).move_to(P(-2.1,-.95))
        self.inter=Circle(.44,color=RED,stroke_width=5,fill_color=RED,fill_opacity=.2).move_to(P(-1.1,.95))
        self.ham=Circle(.48,color=BLUE,stroke_width=5,fill_color=RED,fill_opacity=.18).move_to(P(-.9,-2.25))
        self.inh=inhibit(P(-1.1,.51),P(-.9,-1.62))
        self.ql=leader('quadriceps',.35,-.95,P(-1.6,-.95),size=28)
        self.hl=leader('hamstring',1.45,-2.25,P(-.4,-2.25),size=28)
        self.il=leader('Ia inhibitory\ninterneuron',2.4,1.12,P(-.64,.95),RED,28)
        self.tag=label('same side as the spindle',-3.15,-3.25,size=26)
        self.sensor=capsule(1.4,.55,TEAL).move_to(P(-5.9,2.5))
        self.names=VGroup(label('dorsal',.1,3.13,size=26),label('ventral',.1,-3.13,size=26))
        self.base=VGroup(self.cord,self.tint,self.names,self.sensor,self.aff,self.br1,self.quad,self.ql,self.ham,self.hl)
        self.g=VGroup(self.base)
        if stage>=2:self.g.add(self.br2,self.inter,self.il)
        if stage>=3:self.g.add(self.inh)


def question():
    return VGroup(heading('The Ia fibre only excites.'),label('How can it',0,.9,size=48),
                  label('inhibit anything?',0,-.05,size=48),label('?',0,-2,YELLOW,84))


def sensors(tall=False):
    # Full-height panels. Each organ is a SERIES link between one fibre bundle and tendon.
    left=VGroup(muscle(5.3),spindle(4.4)).move_to(P(-3.2,.25))
    right=VGroup()
    tendon=Rectangle(width=.75,height=4.7,color=GREY,fill_color=GREY,fill_opacity=.2).move_to(P(5.5,.25))
    for i,y in enumerate([1.65,.25,-1.15]):
        ox=[3.35,3.85,3.35][i]
        fibres=VGroup(*[Line(P(.45,y+d),P(ox-.5,y+d),color=GREY,stroke_width=7) for d in [-.17,0,.17]])
        organ=capsule(1.,.65,GOLD).move_to(P(ox,y))
        link=Line(P(ox+.5,y),P(5.1,y),color=GREY,stroke_width=8)
        right.add(VGroup(fibres,organ,link))
    right.add(tendon)
    if tall:
        left.stretch(6./4.7,1).move_to(P(-3.2,-.25))
        right=VGroup()
        for ox,y in zip([2.,3.25,4.35],[1.8,-.25,-2.3]):
            fibres=VGroup(*[Line(P(.45,y+d),P(ox-.5,y+d),color=GREY,stroke_width=7) for d in [-.17,0,.17]])
            organ=capsule(1.,.75,GOLD).move_to(P(ox,y))
            link=Line(P(ox+.5,y),P(5.1,y),color=GREY,stroke_width=8)
            right.add(VGroup(fibres,organ,link))
        right.add(Rectangle(width=.75,height=6.,color=GREY,fill_color=GREY,fill_opacity=.2).move_to(P(5.5,-.25)))
    return VGroup(left,right)

def sensor_labels(tall=False):
    if tall:
        return VGroup(label('Muscle spindle',-3.2,3.3,TEAL,30),label('Golgi tendon organ',3.15,3.3,GOLD,30),
                      label('Muscle',1.05,2.55,size=32),label('Tendon',5.45,-3.55,size=32))
    return VGroup(label('Muscle spindle',-3.2,3.12,TEAL,30),label('Golgi tendon organ',3.15,3.12,GOLD,30),
                  label('Muscle',1.1,2.38,size=26),label('Tendon',5.25,-2.6,size=26))


def gamma_axon():
    cell=Circle(.32,color=BLUE,fill_color=BLUE,fill_opacity=.25).move_to(P(-4.6,2.55))
    left=poly([(-4.28,2.55),(-3.4,2.55),(-3.4,.85),(-2.65,.2)])
    right=poly([(-3.4,2.55),(3.7,2.55),(3.7,.85),(2.65,.2)])
    terminals=VGroup(Dot(P(-2.65,.2),radius=.13,color=BLUE),Dot(P(2.65,.2),radius=.13,color=BLUE))
    return VGroup(cell,left,right,terminals)

def gamma_context(slack=True,contracted=False):
    return VGroup(muscle(8.5).stretch(.87,1),spindle(6.2,slack,contracted),raster(not slack,y=-2.9,width=8.4,height=.55),
                  label('gamma motor neuron',-2.7,3.12,BLUE,30))


def takeaway(gamma=False):
    title=heading('Which pools go up, which down?')
    a=VGroup(label('Own muscle: pool up',0,1.65,GREEN,38),label('1 synapse',0,.9,GREEN,34))
    b=VGroup(label('Antagonist: pool down',0,-.25,RED,38),label('2 synapses',0,-1,RED,34))
    c=VGroup(label('Gamma drive keeps the spindle signalling',0,-2.35,TEAL,30),
             label('while the muscle shortens',0,-2.95,TEAL,30))
    return VGroup(title,a,b,c)


class S00Title(TitleCard):
    TITLE='One Stretch, Two Opposite Commands'
    LESSON='Motor Units, Reflexes and Locomotion'
    def construct(self):
        self.add(VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28),
                        T('One Stretch,',50,font=TITLE_FONT),T('Two Opposite Commands',50,font=TITLE_FONT)).arrange(DOWN,buff=.35))
        self.finish()

class S01Question(SpokenScene):
    def construct(self):
        l=leg().scale(1.12).shift(DOWN*.18)
        # The entire profile fills 80% of the frame height, including the resting shin.
        l[5][1].shift(LEFT*.55)
        self.add(l)
        knee=l[3].get_center();tap=knee+DOWN*.62
        hammer=VGroup(Line(tap+P(1.8,-1.05),tap+RIGHT*.75,color=TEXT,stroke_width=12),
                      capsule(.75,.38,TEXT).set_fill(TEXT,opacity=1).move_to(tap+RIGHT*.75))
        self.at('Tap the tendon');self.play(FadeIn(hammer),run_time=.2)
        self.play(hammer.animate.shift(LEFT*.75),run_time=.4)
        self.play(hammer.animate.shift(RIGHT*.9+DOWN*.1),run_time=.5)
        self.play(FadeOut(hammer),run_time=.3)
        self.at('your leg kicks')
        # Swing through the question, instead of freezing in the kicked pose.
        self.play(Rotate(l[4],PI/8,about_point=knee),run_time=1.5,rate_func=smooth)
        self.at('What happens')
        q=label('?',.5,1.03,YELLOW,44)
        self.play(FadeIn(q),l[2].animate.set_stroke(YELLOW,width=5),
                  Rotate(l[4],PI/8,about_point=knee),run_time=2.3,rate_func=smooth)
        self.finish()

class S02Spindle(SpokenScene):
    def construct(self):
        l=leg();m=muscle();q=heading('Quadriceps');s=spindle();self.add(l)
        self.at('The tap');self.play(l[1].animate.set_color(GREEN),run_time=.3)
        # Remove rasterised text before the zoom; bring the sensor in with its muscle.
        self.play(FadeOut(l[5]),run_time=.2);l.remove(l[5])
        self.play(ReplacementTransform(l,m),FadeIn(q),FadeIn(s),run_time=.8)
        self.play(m.animate.stretch(1.05,0),s.animate.stretch(1.05,0),run_time=.6)
        self.at('Inside it');self.play(Indicate(s[0],color=TEAL,scale_factor=1.03),run_time=.55)
        self.at('called muscle');self.play(FadeIn(leader('Muscle spindle',0,-2.95,P(0,-.7),TEAL,30)),run_time=.4)
        self.finish()

class S03Alongside(SpokenScene):
    def construct(self):
        m=muscle();s=spindle();self.add(m,s,heading('Quadriceps'),label('Muscle spindle',0,-2.95,TEAL,30))
        self.at('the force making');self.play(FadeIn(label('force-making fibres',0,2.62,size=28)),run_time=.35)
        ghost=VGroup(m.copy(),s.copy()).set_opacity(.16)
        self.at('It lengthens');self.add(ghost)
        arrows=VGroup(Arrow(P(-4,-2.5),P(-5.55,-2.5),color=YELLOW,buff=0),Arrow(P(4,-2.5),P(5.55,-2.5),color=YELLOW,buff=0))
        self.play(m.animate.stretch(1.1,0),s.animate.stretch(1.1,0),FadeIn(arrows),run_time=1.1)
        self.at('reports stretch');self.play(Transform(self.mobjects[3],label('Muscle spindle: senses stretch',0,-2.95,TEAL,32)),run_time=.35)
        self.finish()

class S04Afferent(SpokenScene):
    def construct(self):
        s=VGroup(muscle(4.8),spindle(4)).scale(.9).move_to(P(-3.7,-.1))
        c=cord(4.8,1.9).move_to(P(4.8,-.1))
        ax=poly([(-1.8,-.1),(-.9,-.1),(-.9,1.65),(4.,1.65),(4.,.65)],w=16)
        self.add(s,c)
        self.at('Its sensory axons');self.play(Create(ax),run_time=.8)
        aff=VGroup(label('afferent: sensory axon',0,3.12,BLUE,32),
                   label('carrying signals into the cord',0,2.5,size=30),
                   Line(P(.6,2.22),P(.6,1.65),color=BLUE,stroke_width=2))
        self.at('or afferents');self.play(FadeIn(aff),run_time=.4)
        self.at('carry signals');pulses(self,ax,3,.8)
        ia=VGroup(label('Ia fibre (said one-A)',1.05,.65,BLUE,26),
                  Line(P(1.05,.95),P(1.05,1.65),color=BLUE,stroke_width=2))
        self.at('The main ones');self.play(FadeIn(ia),run_time=.35)
        note=VGroup(label('Old numbering by thickness',1.,-1.6,size=26),
                    label('Among the thickest, fastest',1.,-2.2,size=26),
                    poly([(-.5,-1.3),(-.5,-.5),(-.9,-.1)],BLUE,2))
        self.play(FadeIn(note),run_time=.4)
        self.finish()

class S05Enter(SpokenScene):
    def construct(self):
        c=Circuit(1);self.add(c.cord,c.names,c.sensor,c.aff)
        self.at('The tap');pulses(self,c.aff,4,1.3)
        self.at('through the dorsal');self.play(FadeIn(leader('Dorsal root',-4.8,1.25,P(-2.65,2.5),size=30)),run_time=.4)
        branches=VGroup(poly([(-2.65,1.9),(-2.1,-.35)]),poly([(-2.65,1.9),(-1.65,1.2)]))
        self.at('they branch');self.play(Create(branches),run_time=.45)
        self.finish()

class S06Mono(SpokenScene):
    def construct(self):
        # Cord-to-muscle chain, with a large persistent leg panel and output axon.
        l=leg(True).scale(.58).move_to(P(-4.65,-.25))
        for t in l[5]: t.scale(1/.58)
        c=Circuit(1);cg=VGroup(c.cord,c.names,c.aff,c.br1,c.quad).scale(.58).move_to(P(.65,.35))
        neuron=c.quad
        qend=l[1].get_right()
        outpts=[(neuron.get_center()[0]-.25,neuron.get_center()[1]),(-1.8,-.8),(-1.8,qend[1]),tuple(qend[:2])]
        out=poly(outpts,w=7)
        self.add(l,c.cord,c.aff)
        self.at('One branch');self.play(Create(c.br1),FadeIn(neuron),run_time=.6)
        self.at('quadriceps motor');self.play(FadeIn(leader('Quadriceps\nmotor neuron',1.6,-.85,neuron.get_right(),BLUE,28)),Create(out),run_time=.6)
        self.at('directly');pulses(self,c.br1,1,.4)
        self.at('one synapse');self.play(FadeIn(heading('Synapses: 1')),run_time=.3)
        b=meter(current=4);self.add(b,label('quadriceps',4.7,3.25,BLUE,28))
        self.at('The pool goes');self.play(Transform(b,meter(current=8,color=GREEN)),run_time=.3)
        # Audio has only one second between pool and kick: preserve a two-second high hold.
        self.wait(2)
        self.at('the leg kicks');pulses(self,out,1,.35)
        self.play(l[1].animate.stretch(.78,0),Rotate(l[4],PI/6,about_point=l[3].get_center()),
            Transform(out,poly(outpts[:-1]+[(qend[0]-.11*l[1].width,qend[1])],w=7)),run_time=1.1)
        self.wait(2.2);self.finish()

class S07Predict(SpokenScene):
    def construct(self):
        c=Circuit(1);small=VGroup(c.cord,c.aff,c.br1,c.quad,c.ham).scale(.56).move_to(P(-3.85,.4));self.add(small,leader('hamstring',-3.65,-1.65,c.ham.get_bottom(),size=28))
        b=meter(x=-.4,y=-.15,current=7,show_model=False);r=raster(y=-2.4,x=3.1,width=5.4,height=3.9)
        self.add(b,r,heading('Hamstring motor neurons'),label('illustrative model',3.1,2.15,size=26))
        self.at('are held back');self.play(Transform(b,meter(x=-.4,y=-.15,current=2,color=RED,show_model=False)),
            Transform(r,raster(y=-2.4,x=3.1,width=5.4,height=3.9,drive=5.15)),run_time=3)
        self.wait(.35)
        self.at('only ever excites');self.remove(*self.mobjects);self.add(question()[0])
        self.at('How can it');self.play(FadeIn(question()[1:]),run_time=.4)
        self.finish()

class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(question());self.wait(5)

class S09Reveal(SpokenScene):
    def construct(self):
        c=Circuit(1);self.add(c.g)
        self.at('Its second branch');self.play(Create(c.br2),run_time=.65)
        self.at('excites an inhibitory');self.play(FadeIn(c.inter),FadeIn(c.il),run_time=.6)
        self.at('same side');self.play(FadeIn(c.tag),run_time=.4)
        self.finish()

class S10Inhib(SpokenScene):
    def construct(self):
        c=Circuit(2);c.base.remove(c.hl);self.add(c.g,c.tag)
        self.at('That interneuron');self.play(Create(c.inh),run_time=.65)
        self.at('hamstring motor');self.play(Indicate(c.ham,color=RED,scale_factor=1.1),run_time=.45)
        b=meter(current=7,show_model=False)
        owner=leader('hamstring\nmotor neuron',1.45,-2.05,c.ham.get_right(),BLUE,26)
        bridge=poly([(2.62,-2.05),(3.7,-2.05),(4.12,-1.1)],BLUE,2)
        self.add(b,owner,bridge)
        self.at('Their pool');self.play(Transform(b,meter(current=7,gi=.3,color=RED,show_model=False)),run_time=.8)
        self.at('two synapses');self.play(FadeIn(label('Synapses: 2',4.7,-3.1,size=30)),run_time=.35)
        self.finish()

class S11Rule(SpokenScene):
    def construct(self):
        # Three central steps double as the corresponding circuit elements.
        self.add(capsule(12.1,6.9,GREY).set_fill(opacity=0))
        first=VGroup(Circle(.42,color=BLUE).move_to(P(-3.3,2.25)),label('Ia afferent (+)',.1,2.25,GREEN,38))
        middle=VGroup(Circle(.45,color=RED,fill_color=RED,fill_opacity=.2).move_to(P(-3.3,.1)),
                      label('inhibitory interneuron',.55,.1,RED,34))
        last=VGroup(Circle(.45,color=BLUE,fill_color=RED,fill_opacity=.15).move_to(P(-3.3,-2.1)),
                    label('(−) antagonist motor neurons',.7,-2.1,RED,32))
        plus=excite(P(-3.3,1.8),P(-3.3,.75));minus=inhibit(P(-3.3,-.35),P(-3.3,-1.5))
        self.add(first)
        self.at('In this pathway');self.wait(.1)
        self.at('the excitatory');self.play(Create(plus),FadeIn(middle),FadeIn(label('excites (+)',1,1.16,GREEN,28)),run_time=.65)
        self.at('inhibits the antagonist');self.play(Create(minus),FadeIn(last),FadeIn(label('inhibits (−)',1,-1.05,RED,28)),run_time=.65)
        self.at('through an inhibitory');self.play(Indicate(middle[0],color=RED,scale_factor=1.15),run_time=.7)
        self.finish()

class S12Sherrington(SpokenScene):
    def construct(self):
        c=Circuit(3);self.add(c.g,c.tag)
        a=label('↑ pool up',5.05,-.95,GREEN,32);b=label('↓ pool down',5.05,-2.25,RED,32)
        self.at('One stretch');pulses(self,c.aff,2,.6)
        self.at('two commands');self.play(FadeIn(a),FadeIn(b),run_time=.5)
        self.at('Sherrington called');self.play(FadeIn(label('Reciprocal innervation\n(Sherrington)',4.7,2.9,size=26)),run_time=.5)
        self.finish()

class S13Tendon(SpokenScene):
    def construct(self):
        s=sensors(tall=True);labs=sensor_labels(tall=True);self.add(s[0],labs[0])
        self.at('A second sensor');self.play(FadeIn(s[1]),FadeIn(labs[1:]),run_time=.65)
        self.at('Golgi tendon organ');self.play(Indicate(s[1][1][1],color=GOLD,scale_factor=1.1),run_time=.5)
        self.at('muscle meets tendon');self.play(Indicate(s[1][3],color=GREY,scale_factor=1.04),run_time=.55)
        self.finish()

class S14Force(SpokenScene):
    def construct(self):
        s=sensors(tall=True);self.add(s,sensor_labels(tall=True))
        self.at('in line with');self.play(Indicate(s[1][1],color=GOLD,scale_factor=1.025),run_time=.6)
        arrows=VGroup(*[Arrow(P(.7,y+.43),P(4.9,y+.43),color=YELLOW,buff=0,stroke_width=5) for y in [1.8,-.25,-2.3]])
        self.at('senses their pull');self.play(FadeIn(arrows),run_time=.45)
        self.at('signal force');self.play(FadeIn(label('force',3.2,-3.55,GOLD,38)),run_time=.35)
        self.at('not length');self.play(FadeIn(label('length',-3.2,-3.55,TEAL,38)),run_time=.35)
        self.wait(1.5);self.finish()

class S15Twitch(SpokenScene):
    def construct(self):
        s=sensors();s.stretch(.82,1).shift(UP*.35)
        self.add(s,label('Muscle spindle',-3.2,3.12,TEAL,30),label('Golgi tendon organ',3.15,3.12,GOLD,30))
        r1=raster(False,y=-2.75,x=3.1,width=5,height=.7);r2=raster(y=-2.75,x=-3.2,width=5,height=.7)
        self.add(r1,r2)
        self.at('A unit');self.play(s[1][1][0].animate.set_color(GREEN),run_time=.35)
        self.at('twitches');self.play(s[1][1][0].animate.stretch(.8,0,about_edge=RIGHT),run_time=.45)
        self.at('that organ fires');self.play(Transform(r1,raster(y=-2.75,x=3.1,width=5,height=.7,drive=9)),run_time=.45)
        self.at('The shortened spindle');self.play(s[0][0].animate.stretch(.8,0),Transform(s[0][1],spindle(3.5,slack=True).stretch(.82,1).move_to(s[0][1])),run_time=.6)
        self.at('go quiet');self.play(Transform(r2,raster(False,y=-2.75,x=-3.2,width=5,height=.7)),run_time=.35)
        self.finish()

class S16Problem(SpokenScene):
    def construct(self):
        m=muscle(10,4.5);s=spindle();r=raster(y=-2.9,height=.55)
        self.add(m,s,r,heading('Muscle spindle'))
        self.at('That slack spindle');self.play(m.animate.stretch(.8,0),Transform(s,spindle(6.2,slack=True)),Transform(r,raster(False,y=-2.9,height=.55)),run_time=.8)
        self.at('Gamma motor neurons');self.play(Transform(self.mobjects[3],heading('Gamma motor neurons')),run_time=.4)
        self.finish()

class S17Gamma(SpokenScene):
    def construct(self):
        g=gamma_context();self.add(g);ax=gamma_axon()
        self.at('They supply only');self.play(Create(ax),FadeIn(leader('pole ending',-2.65,-.48,P(-2.65,.2),BLUE,24)),FadeIn(leader('pole ending',2.65,-.48,P(2.65,.2),BLUE,24)),run_time=.75)
        arr=VGroup(Arrow(P(-1.9,.7),P(-2.9,.7),color=BLUE,buff=0),Arrow(P(1.9,.7),P(2.9,.7),color=BLUE,buff=0))
        self.at('contract its');self.play(Transform(g[1][2],spindle(6.2,slack=True,contracted=True)[2]),FadeIn(arr),run_time=.75)
        self.finish()

class S18Taut(SpokenScene):
    def construct(self):
        g=gamma_context(True,True);self.add(g,gamma_axon())
        self.at('That pulls');self.play(Transform(g[1],spindle(6.2,contracted=True)),run_time=.9)
        self.at('taut again');self.play(Transform(g[2],raster(y=-2.9,width=8.4,height=.55)),run_time=.4)
        self.at('endings wrap');self.play(Create(coil().stretch(1.3,1).set_stroke(width=7)),FadeIn(leader('Ia ending',0,-.95,P(0,-.4),BLUE,28)),run_time=.45)
        self.finish()

class S19Tape(SpokenScene):
    def construct(self):
        case=capsule(1.8,2.1,TEAL).move_to(P(-4.7,.7))
        dial=Circle(.45,color=GREY).move_to(case)
        def tape(end):
            start=-3.8
            strip=Rectangle(width=end-start,height=.65,stroke_width=2,color=YELLOW,fill_color=YELLOW,fill_opacity=.25).move_to(P((end+start)/2,.7))
            ticks=VGroup(*[Line(P(x,.38),P(x,.38+(.3 if i%5==0 else .16)),color=YELLOW,stroke_width=3) for i,x in enumerate(np.arange(start+.1,end,.22))])
            hook=poly([(end,1.18),(end,.26),(end-.22,.26)],GREY,7)
            return VGroup(strip,ticks,hook)
        strip=tape(5.35)
        ends=VGroup(Dot(P(-4.7,-1.6),radius=.16,color=GREY),Dot(P(5.35,-1.6),radius=.16,color=GREY),Line(P(-4.7,-1.6),P(5.35,-1.6),color=GREY,stroke_width=10))
        self.add(case,dial,strip,ends,label('muscle ends',0,-2.25,size=28))
        title=heading('Tape measure')
        self.at('a tape measure');self.play(FadeIn(title),run_time=.3)
        target=VGroup(Dot(P(-4.7,-1.6),radius=.16,color=GREY),Dot(P(1.5,-1.6),radius=.16,color=GREY),Line(P(-4.7,-1.6),P(1.5,-1.6),color=GREY,stroke_width=10))
        self.at('winds itself in');self.play(Transform(strip,tape(1.5)),Transform(ends,target),Rotate(dial,PI),FadeOut(title),run_time=1.15)
        self.at('never goes loose');self.play(FadeIn(label('stays taut',0,2.05,TEAL,40)),run_time=.3)
        self.finish()

class S20Coactivation(SpokenScene):
    def construct(self):
        m=muscle(9).stretch(.66,1);s=spindle(7.6);r=raster(y=-2.95,width=8.5,height=.6)
        self.add(m,s,r)
        alpha=VGroup(Circle(.3,color=BLUE).move_to(P(-5.6,2.55)),poly([(-5.3,2.55),(-4.8,2.55),(-4.8,1.22),(-2.9,1.22)]),Dot(P(-2.9,1.22),radius=.15,color=BLUE))
        gamma=VGroup(Circle(.3,color=BLUE).move_to(P(5.6,2.55)),poly([(5.3,2.55),(4.5,2.55),(4.5,.5),(3.1,0)]),poly([(4.5,2.15),(-2.8,2.15),(-2.8,0)]))
        self.at('alpha and gamma');self.play(Create(alpha),Create(gamma),FadeIn(label('alpha motor neuron',-3.4,3.2,BLUE,28)),FadeIn(label('gamma motor neuron',3.4,3.2,BLUE,28)),run_time=.65)
        self.at('fire together');self.play(FadeIn(label('Alpha–gamma coactivation',0,-2.05,BLUE,36)),run_time=.2)
        dots=VGroup(Dot(radius=.14,color=YELLOW),Dot(radius=.14,color=YELLOW))
        self.add(dots);self.play(MoveAlongPath(dots[0],alpha[1]),MoveAlongPath(dots[1],gamma[1]),run_time=.7);self.remove(*dots,dots)
        self.at('the spindle can');self.play(m.animate.stretch(.7,0),Transform(s,spindle(5.32,contracted=True)),
            Transform(alpha[1],poly([(-5.3,2.55),(-4.8,2.55),(-4.8,1.22),(-2.,1.22)])),
            alpha[2].animate.move_to(P(-2.,1.22)),
            Transform(gamma[1],poly([(5.3,2.55),(4.5,2.55),(4.5,.5),(2.2,0)])),
            Transform(gamma[2],poly([(4.5,2.15),(-2.2,2.15),(-2.2,0)])),run_time=1.1)
        self.at('during a contraction');self.play(Transform(r,raster(y=-2.95,width=8.5,height=.6)),run_time=.4)
        self.finish()

class S21Takeaway(SpokenScene):
    def construct(self):
        t=takeaway();q=label('?',0,0,YELLOW,86);self.add(t[0],q)
        self.at('So ask');self.wait(.1)
        self.at('A stretch');self.play(FadeOut(q),FadeIn(t[1]),run_time=.55)
        self.at('and its antagonists');self.play(FadeIn(t[2]),run_time=.55)
        self.finish()

class S21bGamma(SpokenScene):
    def construct(self):
        t=takeaway();self.add(*t[:3])
        self.at('gamma drive keeps');self.play(FadeIn(t[3]),run_time=.55)
        self.at('while the muscle');self.play(Indicate(t[3],color=TEAL,scale_factor=1.02),run_time=.6)
        self.finish()

class S22End(EndCard):
    LINE="A stretch pushes its own pool up and its antagonist's down."
    def construct(self):
        a=VGroup(T('A stretch pushes its own pool up',38,font=TITLE_FONT),T("and its antagonist’s down.",38,font=TITLE_FONT)).arrange(DOWN,buff=.35)
        self.add(a,label('biochemistrypedia.com',0,-1.65,TEAL,28));self.finish()
