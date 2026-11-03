"""Chapter 1: A Gain That Death Erases.
COLOR MAP: BLUE = outer hair cells / prestin; GREEN = contraction / NLC;
YELLOW = stimulus / energy; TEAL = returning sound; GREY = passive structure;
RED = absent; GOLD = living response / gain.
Curves: continuous schematic, soft slope 1, middle .25, loud convergence.
Spatial envelopes: analytic asymmetric Gaussian schematics, not measured data.
"""
import numpy as np
import os
from pathlib import Path
from bp_style import *

LESSON = 'The Cochlear Amplifier and Otoacoustic Emissions'
GREY = '#B7BFCC'

class Timed(SpokenScene):
    def at(self, phrase, lead=0, nth=0):
        target = self.t_of(phrase, nth)
        if target > self.elapsed() + .02:
            self.wait(target-self.elapsed())
        with open(Path(os.environ['KX_SCRIPT']).parent/'sync.log','a') as f:
            f.write(f"{os.environ['KX_SCENE_ID']} {phrase!r} target={target:.3f} actual={self.elapsed():.3f} offset={self.elapsed()-target:+.3f}\n")

def head(text,color=TEXT):
    return T(text,32,color).move_to([0,3.25,0])

def note(text,y=1.5,color=GOLD):
    return T(text,27,color).move_to([3.65,y,0])

def living(x):
    return x+45 if x<=20 else 65+.25*(x-20) if x<=80 else x

def graph():
    # .056 world units per dB on BOTH axes: slope 1 is exactly 45 degrees.
    ax=Axes(x_range=[0,100,10],y_range=[0,110,10],x_length=5.6,y_length=6.16,
        tips=False,axis_config={'color':GREY,'include_ticks':True,'tick_size':.065,'stroke_width':2}).move_to([-1.55,.05,0])
    lab=VGroup(T('Basilar-membrane motion (dB)',26).rotate(PI/2).move_to([-5.15,.05,0]),
        T('Sound level (dB)',26).move_to([-1.55,-3.5,0]),
        T('Schematic · basal site',26,GREY).move_to([3.65,3.3,0]))
    return ax,lab

def curve(ax,fn,xr,color,w=5):
    return VMobject(color=color,stroke_width=w).set_points_as_corners([ax.c2p(x,fn(x)) for x in np.linspace(*xr,301)])
def dead(ax):return curve(ax,lambda x:x,(0,100),GREY)
def live(ax,end=100,start=0):return curve(ax,living,(start,end),GOLD)
def shade(ax):
    xs=np.linspace(0,100,301)
    return Polygon(*([ax.c2p(x,living(x)) for x in xs]+[ax.c2p(x,x) for x in xs[::-1]]),stroke_width=0,fill_color=GOLD,fill_opacity=.2)
def plot_state(end=None,filled=False):
    ax,lab=graph();g=VGroup(ax,lab)
    if filled:g.add(shade(ax))
    g.add(dead(ax))
    if end is not None:g.add(live(ax,end))
    return g,ax

def cell(x=0,y=0,h=1.6):
    return RoundedRectangle(width=h*.34,height=h,corner_radius=h*.17,color=BLUE,stroke_width=4,fill_color=BLUE,fill_opacity=.18).move_to([x,y,0])

def envelope(x,active=True):
    p=6.25 if active else 5.65
    return (4.3 if active else 4.3/3)*np.exp(-.5*((x-p)/((1.3 if active else 2.25) if x<p else (.42 if active else 1.5)))**2)

def spatial(active=True,carrier=False,phase=0,front=10):
    xs=np.linspace(0,10,600)
    return VMobject(color=GOLD if active else GREY,stroke_width=5).set_points_as_corners(
        [[-5.8+1.16*x,-1.65+envelope(x,active)*((1+np.cos(2*PI*1.3*(x-6.25)-phase))/2 if carrier else 1)*min(1,max(0,(front-x)*3)),0] for x in xs])

def strip(active=True,oscillate=False):
    base=VGroup(Line([-5.8,-1.65,0],[5.8,-1.65,0],color=GREY,stroke_width=3),
        *[Line([x,-1.73,0],[x,-1.57,0],color=GREY) for x in np.linspace(-5.8,5.8,11)])
    labels=VGroup(T('Base · high frequency',26,GREY).move_to([-4,-2.1,0]),T('Basilar membrane',26,GREY).move_to([0,-2.1,0]),T('Apex · low frequency',26,GREY).move_to([4,-2.1,0]))
    return VGroup(base,labels,spatial(active,oscillate))

def prediction():
    g,ax=plot_state()
    q=VGroup(T('Predict',32,YELLOW),T('Where is the difference',26),T('largest: living vs dead?',26)).arrange(DOWN,buff=.14).move_to([3.65,1.9,0])
    a=VGroup(T('Soft ?',32,YELLOW).move_to([3.65,-1.65,0]),Arrow([2.3,-1.65,0],ax.c2p(10,10),color=YELLOW,buff=.12))
    b=VGroup(T('Loud ?',32,YELLOW).move_to([3.65,.15,0]),Arrow([2.3,.15,0],ax.c2p(94,94),color=YELLOW,buff=.12))
    return g,q,a,b

class S00Title(TitleCard):
    LESSON=LESSON
    TITLE='A Gain That Death Erases'
    def construct(self):
        self.add(T('BIOCHEMISTRYPEDIA',26,TEAL).move_to([0,2.2,0]),VGroup(T('The Cochlear Amplifier',28,GREY),T('and Otoacoustic Emissions',28,GREY)).arrange(DOWN,buff=.12).move_to([0,1.1,0]))
        self.play(FadeIn(T(self.TITLE,48,font=TITLE_FONT).move_to([0,-.4,0])),Create(Line([-1.2,-1.2,0],[1.2,-1.2,0],color=GOLD)),run_time=.8);self.finish()

class S01Q(Timed):
    def construct(self):
        # A tapering canal, a sealed probe, and a connected inner-ear spiral.
        canal=Polygon([-4.5,2.2,0],[-1,1.1,0],[2.5,.75,0],[2.5,-.75,0],[-1,-1.1,0],[-4.5,-2.2,0],color=GREY,fill_color=GREY,fill_opacity=.07)
        plug=RoundedRectangle(width=.55,height=4.8,corner_radius=.15,color=GREY,fill_color=GREY,fill_opacity=.4).move_to([-4.65,0,0])
        mic=RoundedRectangle(width=.45,height=.7,corner_radius=.08,color=TEAL,fill_color=TEAL,fill_opacity=.4).move_to([-4.22,0,0])
        t=np.linspace(0,4.5*PI,300);spiral=VMobject(color=GREY,stroke_width=5).set_points_as_corners([[4.05+.09*a*np.cos(a),.09*a*np.sin(a),0] for a in t])
        link=Line([2.5,0,0],[4.05,0,0],color=GREY,stroke_width=3)
        self.add(head('A Gain That Death Erases'),canal,plug,mic,spiral,link)
        self.at('a microphone');self.play(FadeIn(T('Microphone',28,TEAL).move_to([-4.25,2.75,0])),run_time=.3)
        self.at('healthy ear canal');self.play(FadeIn(T('Healthy · sealed ear canal',28,GREY).move_to([-.5,-2.65,0])),run_time=.35)
        # A long, faint ripple leaves the cochlea and reaches the probe.
        pulse=VMobject(color=TEAL,stroke_width=4,stroke_opacity=.65).set_points_as_corners([[x,.22*np.sin(9*(x-4.05)),0] for x in np.linspace(4.05,5.85,180)])
        self.at('record sound');self.play(Create(pulse),run_time=.2)
        self.play(pulse.animate.shift(LEFT*3.4),run_time=.55,rate_func=linear)
        self.at('cochlea itself');self.play(FadeIn(T('Cochlea',28,GREY).move_to([4.05,-1.6,0])),pulse.animate.shift(LEFT*4.87),run_time=.85,rate_func=linear);self.play(FadeOut(pulse),run_time=.15)
        self.at('where does it');self.play(FadeIn(T('Where does that sound come from?',32,TEAL).move_to([0,-3.3,0])),run_time=.3);self.finish()

class S02Wave(Timed):
    def construct(self):
        t=np.linspace(0,4*PI,320);spiral=VMobject(color=GREY,stroke_width=5).set_points_as_corners([[.18*(1+a)*np.cos(a),.18*(1+a)*np.sin(a),0] for a in t])
        self.add(head('A cochlea without help',GREY),T('Motion magnitude · schematic',26,GREY).move_to([0,-3.2,0]))
        self.at('start with');self.play(Create(spiral),run_time=.6)
        st=strip(False);self.wait(.3);self.play(ReplacementTransform(spiral,st[0]),FadeIn(st[1]),run_time=1.2)
        phase=ValueTracker(0);front=ValueTracker(0)
        moving=always_redraw(lambda:spatial(False,True,phase.get_value(),front.get_value()))
        self.at('sound sets up');self.add(moving);self.play(front.animate.set_value(10.5),phase.animate.set_value(3*PI),run_time=2.6,rate_func=linear);self.finish()

class S03Cf(Timed):
    def construct(self):
        st=strip(False);self.add(st[0],st[1],head('Living · soft levels',GOLD))
        phase=ValueTracker(0);moving=always_redraw(lambda:spatial(True,True,phase.get_value()));self.add(moving)
        self.at('in a living');self.play(phase.animate.set_value(4*PI),run_time=2.4,rate_func=linear)
        freq=VGroup(*[T(t,26,GREY).move_to([x,-2.65,0]) for x,t in [(-5,'High'),(0,'Middle'),(5,'Low')]],T('Frequency along the cochlea · schematic',26,GREY).move_to([0,-3.2,0]))
        self.at('each place moves');self.play(FadeIn(freq),phase.animate.set_value(7*PI),run_time=1.8,rate_func=linear)
        self.at('its characteristic frequency');self.play(phase.animate.set_value(9*PI),run_time=1.1,rate_func=linear)
        self.play(FadeIn(VGroup(T('Characteristic frequency',28,GOLD),T('(living, soft levels)',26,GOLD)).arrange(DOWN,buff=.1).move_to([4.3,1.9,0])),Create(Line([1.45,2.65,0],[2.05,2.1,0],color=GOLD)),run_time=.4)
        self.at('the wave peaks');moving.clear_updaters();self.play(FadeOut(moving),Create(spatial(True)),run_time=.8);self.finish()

class S04Passive(Timed):
    def construct(self):
        st=strip(True);title=head('Living · soft levels',GOLD);self.add(st,title)
        ghost=spatial(True).set_stroke(opacity=.75,width=4)
        self.at('after death');self.add(ghost);self.play(Transform(title,head('Passive · after death',GREY)),st[2].animate.set_color(GREY),run_time=.4)
        self.at('but weak');self.play(Transform(st[2],spatial(False)),run_time=.7)
        ticks=VGroup(*[Line([x,-1.78,0],[x,-1.47,0],color=col,stroke_width=4) for x,col in [(.754,GREY),(1.45,GOLD)]])
        self.at('peak can shift');self.play(Create(ticks),Create(DoubleArrow([.754,-1.3,0],[1.45,-1.3,0],buff=0,color=GREY,tip_length=.12)),FadeIn(T('Peak can shift',28,GREY).move_to([1.1,-2.8,0])),run_time=.4);self.finish()

class S05Exp(Timed):
    def construct(self):
        st=strip(False);self.add(st)
        site=Dot([-4.4,-1.65,0],radius=.12,color=YELLOW)
        self.at('now pick one');self.play(FadeIn(site),FadeIn(T('One site near the base',28,YELLOW).move_to([-3.5,-2.8,0])),Create(Line([-4.4,-1.85,0],[-4.4,-2.45,0],color=YELLOW)),run_time=.35)
        self.at('play a tone');self.play(FadeIn(head('Tone at this site’s characteristic frequency',YELLOW)),run_time=.35)
        # Establish the measuring apparatus before the stepped input is named.
        self.wait(1);ax,lab=graph()
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.25)
        self.play(FadeIn(ax),FadeIn(lab),run_time=.35)
        marker=Dot(ax.c2p(10,0),color=YELLOW,radius=.11)
        self.at('raise the level');self.add(marker)
        for x in (20,30,40):self.play(marker.animate.move_to(ax.c2p(x,0)),run_time=.27)
        self.play(FadeIn(note('10 dB steps',-.5,YELLOW)),run_time=.2);self.finish()

class S06Dead(Timed):
    def construct(self):
        ax,lab=graph();self.add(ax,lab)
        self.at('after death');self.play(Create(dead(ax)),run_time=.7)
        self.at('more sound');self.play(Create(Line(ax.c2p(30,30),ax.c2p(40,30),color=YELLOW,stroke_width=7)),FadeIn(T('+10 dB in',26,YELLOW).next_to(ax.c2p(35,30),DOWN,buff=.2).shift(RIGHT*.2+DOWN*.2)),run_time=.35)
        self.at('more motion');self.play(Create(Line(ax.c2p(40,30),ax.c2p(40,40),color=GREY,stroke_width=7)),FadeIn(T('+10 dB out',26,GREY).next_to(ax.c2p(40,35),RIGHT,buff=.2)),run_time=.35)
        self.at('that straight line');self.play(FadeIn(note('After death',1.6,GREY)),FadeIn(note('Linear · slope 1',1,GREY)),run_time=.35);self.finish()

class S07Predict(Timed):
    def construct(self):
        g,q,a,b=prediction();self.add(g)
        self.at('predict');self.play(FadeIn(q),run_time=.3)
        self.at('at soft levels');self.play(FadeIn(a),run_time=.3)
        self.at('loud ones');self.play(FadeIn(b),run_time=.3);self.finish()
class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(*prediction(),T('Pause and decide',28,YELLOW).move_to([3.65,-2.9,0]));self.wait(5)
class S09R1(Timed):
    def construct(self):
        g,ax=plot_state();self.add(g)
        self.at('at soft levels');self.play(Create(live(ax,20)),run_time=.7)
        self.at('living membrane');self.play(FadeIn(note('Living',1.6)),run_time=.3)
        self.at('tens of decibels');self.play(GrowFromCenter(DoubleArrow(ax.c2p(8,8),ax.c2p(8,living(8)),buff=0,color=GOLD)),FadeIn(VGroup(T('Tens',26,GOLD),T('of dB',26,GOLD)).arrange(DOWN,buff=.08).move_to([-3,-.6,0])),run_time=.4);self.finish()
class S10R2(Timed):
    def construct(self):
        g,ax=plot_state(20);self.add(g)
        self.at('as the tone');self.play(Create(live(ax,80,20)),run_time=1.1)
        self.at('grows slowly');self.play(FadeIn(note('Grows slowly',1.6)),run_time=.3)
        self.at('often');self.play(FadeIn(VGroup(T('Often 2–5 dB motion',27,GOLD),T('per 10 dB sound',27,GOLD)).arrange(DOWN,buff=.18).move_to([3.65,.3,0])),run_time=.4);self.finish()
class S11R3(Timed):
    def construct(self):
        g,ax=plot_state(80);self.add(g)
        self.at('at the loudest');self.play(Create(live(ax,100,80)),run_time=.6)
        self.at('come close together');self.play(FadeIn(VGroup(T('Close together',27,GOLD),T('at loud levels',27,GOLD)).arrange(DOWN).move_to([3.65,.5,0])),run_time=.3);self.finish()
class S12Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;g,_=plot_state(100);self.add(g,note('Close at loud levels',.5));self.wait(2.5)
class S13Gain(Timed):
    def construct(self):
        g,ax=plot_state(100);self.add(g)
        self.at('the gap between');self.play(FadeIn(shade(ax)),run_time=.5)
        self.at('cochlear amplifier');self.play(FadeIn(VGroup(T('Gain =',28,GOLD),T('the cochlear amplifier',27,GOLD)).arrange(DOWN).move_to([3.65,2.5,0])),run_time=.35)
        c=cell(2.15,.8,1.5)
        # The gap closes at (80,80): leave its right tip horizontally.
        link=Line(ax.c2p(80,80),[1.9,ax.c2p(80,80)[1],0],color=BLUE,stroke_width=3)
        label=VGroup(T('Outer hair',26,BLUE),T('cell',26,BLUE)).arrange(DOWN,buff=.1).move_to([4.1,.8,0])
        self.at('outer hair cells');self.play(FadeIn(c),Create(link),FadeIn(label),run_time=.4);self.finish()
class S14Sharp(Timed):
    def construct(self):
        st=strip(False);self.add(st,head('Gain near the characteristic frequency',GOLD))
        self.at('the gain is');self.play(Create(spatial(True)),run_time=.7)
        legend=VGroup(T('Living',27,GOLD),T('Passive',27,GREY)).arrange(DOWN,aligned_edge=LEFT,buff=.2).move_to([4.3,1.5,0])
        self.at('sharpens the peak');self.play(FadeIn(T('Taller and narrower',28,GOLD).move_to([-2,2.2,0])),FadeIn(legend),run_time=.35);self.finish()
class S15Idea1(Timed):
    def construct(self):
        st=strip(True);st[1][1].move_to([-3.5,-.4,0]);title=head('The one idea');self.add(st,title)
        # Lay out once so all glyphs share their typographic baseline.
        tokens=['Outer','hair','cells','add','energy','near','the','peak']
        sentence=T(' '.join(tokens),28,YELLOW,disable_ligatures=True).move_to([0,3.25,0])
        words=[];start=0
        for token in tokens:
            words.append(VGroup(*sentence[start:start+len(token)]));start+=len(token)+1
        cells=VGroup(*[cell(x,-2.8,1.2) for x in [.4,1.1,1.8]])
        self.at('outer hair cells');self.remove(title);self.play(FadeIn(cells),FadeIn(T('Outer hair cell',26,BLUE).move_to([-1.4,-2.85,0])),run_time=.15)
        for i,cue in enumerate(['outer','hair','cells','add','energy','near','its','peak']):
            self.at(cue);self.play(FadeIn(words[i]),run_time=.1)
            if i==4:self.play(*[GrowArrow(Arrow([x,-2.15,0],[x,-1.4,0],color=YELLOW,buff=.02)) for x in [.4,1.1,1.8]],run_time=.2)
        self.finish()
class S16Idea2(Timed):
    def construct(self):
        self.add(head('Gain = living compared with dead',GOLD),Line([-5.7,-2,0],[5.7,-2,0],color=GREY))
        def bar(x,h):return Rectangle(width=1.6,height=h,fill_color=GOLD,fill_opacity=.5,stroke_color=GOLD).move_to([x,-2+h/2,0])
        self.at('large for soft');self.play(GrowFromEdge(bar(-3.9,4.3),DOWN),FadeIn(T('Soft',28).move_to([-3.9,-2.6,0])),run_time=.5)
        self.at('small for loud');self.play(GrowFromEdge(bar(0,4.3*(living(78)-78)/45),DOWN),FadeIn(T('Loud',28).move_to([0,-2.6,0])),run_time=.4)
        self.at('gone after death');self.play(FadeIn(T('0',36,GREY).move_to([3.9,-1.65,0])),FadeIn(T('After death',28,GREY).move_to([3.9,-2.6,0])),run_time=.4);self.finish()
class S17Idea3(Timed):
    def construct(self):
        g,ax=plot_state(100,True);g[1][2].set_opacity(0);self.add(g)
        # Dashed teal identifies a diagram leader, distinct from both data curves.
        bracket=VGroup(DashedLine(ax.c2p(15,40),[1.55,.2,0],color=TEAL,dash_length=.09,stroke_width=2.5),Line([1.55,-1.6,0],[1.55,2.3,0],color=TEAL,stroke_width=2.5))
        self.add(bracket)
        entries=[('sensitivity',['Sensitivity'],2.3,GOLD),('sharp tuning',['Sharp tuning'],1,GOLD),('compressive growth',['Compressive growth','of motion'],-.3,GOLD),('returning sound',['Emissions','(returning sound)'],-1.6,TEAL)]
        for cue,lines,y,col in entries:
            text=VGroup(*[T(t,26,col) for t in lines]).arrange(DOWN,buff=.08).move_to([4.5,y,0])
            self.at(cue);self.play(GrowArrow(Arrow([1.55,y,0],[2.55,y,0],buff=0,color=col)),FadeIn(text),run_time=.3)
        self.play(FadeIn(VGroup(T('Microphone sound:',26,TEAL),T('a clue to cochlear gain',26,TEAL)).arrange(DOWN,buff=.12).move_to([3.8,-2.85,0])),run_time=.3);self.finish()
class S18Floor(Timed):
    def construct(self):
        g,ax=plot_state(100,True);self.add(g)
        self.at('at the very softest');self.play(Create(live(ax,20).set_stroke(width=10)),run_time=.5)
        self.at('gain stops rising');self.play(Create(curve(ax,lambda x:x,(0,20),GREY,10)),FadeIn(note('As the tone gets softer',1.7)),run_time=.4)
        self.at('it levels off');self.play(FadeIn(T('Plateau',27,GOLD).move_to([-3,1.2,0])),Create(Line([-3.45,.92,0],ax.c2p(10,55),color=GOLD)),Create(DoubleArrow(ax.c2p(5,5),ax.c2p(5,50),buff=0,color=GOLD)),FadeIn(VGroup(T('Plateau at the soft end',27,GOLD),T('Gain at its maximum',27,GOLD),T('Linear again',27,GREY)).arrange(DOWN,buff=.2).move_to([3.65,.15,0])),run_time=.4);self.finish()
class S19Why(Timed):
    def construct(self):
        g,ax=plot_state(100);self.add(g)
        self.at('why want');self.play(FadeIn(VGroup(T('Why want a gain',27,GOLD),T('that shrinks?',27,GOLD)).arrange(DOWN).move_to([3.65,1.7,0])),run_time=.3)
        self.at('suppose the response');self.play(Create(live(ax,80,20).set_stroke(width=10)),run_time=.6)
        self.at('grows');self.play(FadeIn(VGroup(T('2.5 dB per 10 dB',27,GOLD),T('Slope 0.25',27,GOLD)).arrange(DOWN).move_to([3.65,-.2,0])),run_time=.3);self.finish()

def squeeze_state():
    a=Rectangle(width=10,height=1,color=YELLOW,fill_color=YELLOW,fill_opacity=.25).move_to([0,1.4,0])
    b=Rectangle(width=2.5,height=1,color=GOLD,fill_color=GOLD,fill_opacity=.25).move_to([0,-1.15,0])
    f=VGroup(Line([-5,.9,0],[-1.25,-.65,0],color=GREY),Line([5,.9,0],[1.25,-.65,0],color=GREY))
    return a,b,f
class S20Squeeze(Timed):
    def construct(self):
        a,b,f=squeeze_state();self.add(head('An illustrative constant slope'),T('Slope 0.25 · assumed constant',27,GREY).move_to([0,-3.2,0]))
        self.at('if that slope');self.play(FadeIn(a),FadeIn(T('60 dB input',29,YELLOW).move_to([0,2.35,0])),run_time=.4)
        self.at('a quiet room');self.play(FadeIn(T('Quiet room → shout',27,YELLOW).move_to([0,1.4,0])),run_time=.3)
        self.at('would fit into');self.play(Create(f),TransformFromCopy(a,b),FadeIn(T('15 dB motion',28,GOLD).move_to([0,-2,0])),FadeIn(M('60 × 0.25 = 15 dB',28).move_to([0,-2.6,0])),run_time=.4);self.finish()
class S21Benefit(Timed):
    def construct(self):
        a,b,f=squeeze_state();self.add(a,b,f,head('The same range, expressed as ratios'),T('Slope 0.25 · assumed constant',27,GREY).move_to([0,-3.2,0]))
        self.at('thousandfold range');self.play(FadeIn(T('60 dB = 1000× in pressure',30,YELLOW).move_to([0,2.35,0])),run_time=.4)
        self.at('fitted into');self.play(FadeIn(T('15 dB = under 6× in motion',30,GOLD).move_to([0,-2.2,0])),Indicate(b,scale_factor=1.03),run_time=.4);self.finish()
class S22Bridge(Timed):
    def construct(self):
        c=cell(0,-.05,5.1);self.add(c)
        self.at('outer hair cells');self.play(FadeIn(head('Outer hair cell',BLUE)),run_time=.3)
        motors=VGroup(*[Dot([x,y,0],radius=.09,color=BLUE) for x in [-.85,.85] for y in np.linspace(-1.8,1.7,9)])
        self.at('motor protein');self.play(FadeIn(motors),run_time=.4)
        self.at('called');self.play(FadeIn(T('Prestin',32,BLUE).move_to([3,.8,0])),Create(Line([.95,.8,0],[2.25,.8,0],color=BLUE)),run_time=.4)
        self.at('how does a cell');self.play(FadeIn(VGroup(T('How does a cell',32,TEAL),T('push that fast?',32,TEAL)).arrange(DOWN,buff=.2).move_to([3.7,-1,0])),run_time=.35)
        self.add(T('The returning-sound question continues in chapter 3',26,TEAL).move_to([0,-3.25,0]));self.finish()
class S23Take(Timed):
    def construct(self):
        g,ax=plot_state(100,True);self.add(g)
        self.at('take this with you');self.play(FadeIn(note('Take this with you',2)),run_time=.3)
        self.at('large for soft sounds');self.play(Indicate(g[2],color=GOLD,scale_factor=1.01),FadeIn(VGroup(T('A gain for',29,GOLD),T('soft sounds',29,GOLD)).arrange(DOWN).move_to([3.65,.6,0])),run_time=.4)
        self.at('death erases it');self.play(FadeOut(g[2]),FadeOut(g[4]),FadeIn(VGroup(T('Death erases',29,GREY),T('the gain',29,GREY)).arrange(DOWN).move_to([3.65,-1.4,0])),run_time=.4);self.finish()
class S24End(EndCard):
    LINE='The living cochlea adds gain for soft sounds; death erases it.'
    def construct(self):
        lines=VGroup(T('The living cochlea adds gain for soft sounds;',34,font=TITLE_FONT),T('death erases it.',34,font=TITLE_FONT)).arrange(DOWN,buff=.28)
        self.play(FadeIn(lines),run_time=.7);self.play(FadeIn(T('biochemistrypedia.com',26,TEAL).move_to([0,-1.7,0])),run_time=.35);self.finish()
