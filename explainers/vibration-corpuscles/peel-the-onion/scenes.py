"""Word-timed repair of Peel the Onion.
COLOR MAP: INDIGO #9B8CF2 outer core; TEAL #3FB8C0 inner core;
YELLOW #F5D547 axon/spikes; GREEN #83C167 terminal voltage/current;
ORANGE #F29E4C stimulus; BLUE fluid; GREY reference/axes; RED interpretation.
All response shapes are exponential step responses or the reference AP template;
tuning is a Gaussian schematic, never presented as measured data.
"""
import numpy as np
from bp_style import *
INDIGO='#9B8CF2'
ORANGE='#F29E4C'

# Keep rendering side effects out of the chapter's existing sync.log.
class Timed(SpokenScene):
    def at(self, phrase, lead=.2, nth=0):
        rest=self.t_of(phrase,nth)-lead-self.elapsed()
        if rest>.02:self.wait(rest)


def label(s,x=0,y=3,color=TEXT,size=28):
    return T(s,size,color).move_to([x,y,0])


def poly(pts,color=GREEN,sw=5):
    return VMobject(stroke_color=color,stroke_width=sw).set_points_as_corners([[x,y,0] for x,y in pts])


def key():
    return VGroup(label('outer core',-4.4,3.45,INDIGO,26),label('inner core',0,3.45,TEAL,26),label('ending / axon',4.2,3.45,YELLOW,26))


def corpuscle(pressed=False,relaxed=False):
    outer=VGroup(*[Ellipse(width=6.6-.65*i,height=5.4-.55*i,color=INDIGO,stroke_width=3,fill_color=INDIGO,fill_opacity=.025) for i in range(4)])
    inner=VGroup(*[Ellipse(width=w,height=h,color=TEAL,stroke_width=4,fill_color=TEAL,fill_opacity=.07) for w,h in [(3.2,2.4),(2.5,1.7)]])
    axon=Line([-4.8,0,0],[-.6,0,0],color=YELLOW,stroke_width=8)
    term=RoundedRectangle(width=1.9,height=.65,corner_radius=.2,color=YELLOW,fill_color=YELLOW,fill_opacity=.5)
    if pressed:
        outer.stretch(.58,1)
        if not relaxed:inner.stretch(.5,1);term.stretch(.6,1)
    g=VGroup(outer,inner,axon,term)
    g.outer,g.inner,g.axon,g.term=outer,inner,axon,term
    return g


def suspects(active=()):
    return VGroup(*[label(s,x,-2.95,c if i in active else GREY,26) for i,(s,x,c) in enumerate([
        ('1. capsule',-4.7,INDIGO),('2. terminal channels',-.2,GREEN),('3. spike generator',4.4,YELLOW)])])


def leader(s,x,y,target,color=TEXT):
    t=label(s,x,y,color,26)
    start=t.get_left()+LEFT*.18 if x>target[0] else t.get_right()+RIGHT*.18
    return VGroup(t,Line(start,target,color=color,stroke_width=2))


def probe(down=False):
    return VGroup(RoundedRectangle(width=1.5,height=.45,corner_radius=.08,color=ORANGE,fill_color=ORANGE,fill_opacity=.3).move_to([0,1.85 if down else 2.9,0]),label('probe pressing the skin',3.9,2.65,ORANGE,26))


def stimulus(y=2.25,x0=-5.4,x1=5.5):
    a=x0+.17*(x1-x0);b=x0+.8*(x1-x0)
    return VGroup(poly([(x0,y),(a,y),(a,y+.45),(b,y+.45),(b,y),(x1,y)],ORANGE,4),
      label('press',a-.6,y+.85,ORANGE,26),label('hold',(a+b)/2,y+.85,ORANGE,26),label('release',b+.6,y+.85,ORANGE,26))


def base(y,x0=-5.4,x1=5.5):return Line([x0,y,0],[x1,y,0],color=GREY,stroke_width=2)


def axis(y,title,x0=-5.4,x1=5.5,height=2):
    return VGroup(base(y,x0,x1),Arrow([x0,y,0],[x0,y+height,0],buff=0,color=GREY,stroke_width=2,max_tip_length_to_length_ratio=.08),
      label(title,(x0+x1)/2,y+height+.35,GREEN,26),label('time →',x1-.6,y-.48,GREY,26))


def decay(y,tau=.45,amp=1.8,x0=-5.4,x1=5.5,inward=False,color=GREEN):
    a=x0+.17*(x1-x0);b=x0+.8*(x1-x0)
    xs=np.unique(np.r_[np.linspace(x0,x1,600),a-.001,a,b-.001,b])
    return poly([(x,y+((-1 if inward else 1)*amp*np.exp(-(x-a)/tau) if a<=x<b else 0)) for x in xs],color)


def impulses(y,positions=None,x0=-5.4,x1=5.5,amp=1.8):
    if positions is None:positions=[-3.547,-3.24,3.32,3.63]
    pts=[(x0,y)]
    for x in positions:pts += [(x-.12,y),(x-.035,y),(x,y+amp),(x+.05,y-.15),(x+.15,y)]
    return poly(pts+[(x1,y)],YELLOW)


def silence(y=-2.6):
    return VGroup(Line([-2.8,y,0],[3.1,y,0],color=YELLOW),Line([-2.8,y,0],[-2.8,y+.18,0],color=YELLOW),Line([3.1,y,0],[3.1,y+.18,0],color=YELLOW),label('silent through the whole hold',.15,y-.4,YELLOW,26))


def cat_stage(potential=False,spikes=False,question=False,caveat=False):
    g=VGroup(label('Cat · mainly under intense compression' if caveat else 'Isolated cat corpuscle · outer layers removed',y=3.45,size=28),stimulus(y=2.05),
        axis(.1,'generator potential · voltage',height=1.2),axis(-2.15,'impulses · voltage',height=1.65))
    if potential:
        g.add(DashedVMobject(decay(.1,.45,1.25,color=GREY)),decay(.1,6,1.25),label('intact',-2.5,.55,GREY,26),label('peeled',2.7,.95,GREEN,26))
    if spikes:g.add(impulses(-2.15,[-3.547],amp=1.65),silence(-2.65))
    if question:g.add(label('What lasts through the hold?',y=-3.05,size=30))
    return g


def tuning_plot():
    xs=np.linspace(1.6,5.8,240)
    before=[(x,-1.7+2.25*np.exp(-((x-3.7)/.8)**2)) for x in xs]
    after=[(x,-1.7+2.2*np.exp(-((x-3.76)/.82)**2)) for x in xs]
    return VGroup(base(-1.7,1.6,5.8),Line([1.6,-1.7,0],[1.6,.8,0],color=GREY),poly(before,GREY,7),poly(after,YELLOW,3),
      label('sensitivity',3.7,1.15,size=26),label('frequency →',3.7,-2.2,GREY,26),label('before',4.9,.65,GREY,26),
      label('after outer core removed',3.7,-2.85,YELLOW,26))


def duck_current(big=False):return decay(.7,.20,3.15 if big else 2.05,x0=-5.5,x1=.5,inward=True)


def current_stage(question=False,trace=False,big=False,tuning=False):
    g=VGroup(label('Duck · outer core removed · inner core kept',y=3.45,size=28),stimulus(2.05,-5.5,.5),
      base(.7,-5.5,.5),label('current (inward)',-2.5,1.35,GREEN,28),Line([-5.5,.7,0],[-5.5,-2.6,0],color=GREY,stroke_width=2),
      label('time (ms) →',-.55,.3,TEXT,24),label('schematic response shapes',x=-2.7,y=-3.05,color=TEXT,size=26))
    if trace:g.add(duck_current(big))
    if tuning:g.add(tuning_plot())
    if question:g.add(label('Slow and sustained,',3.6,.7,size=28),label('or still fast?',3.6,.1,size=28),label('And the tuning?',3.6,-1,size=28),label('Pause and predict',3.6,2.4,GOLD,30))
    return g


def timeline(active):
    return VGroup(*[label(s,x,-3.1,TEXT if i==active else GREY,26) for i,(s,x) in enumerate([('1965 cat',-4.5),('1966 model',0),('2025 duck',4.4)])])


def pipette():
    return VGroup(Polygon([4.5,2.35,0],[4.9,1.95,0],[.65,.15,0],color=GREY,fill_color=GREY,fill_opacity=.2),label('patch pipette',4.7,2.8,size=26))


class S00Title(TitleCard):
    TITLE='Peel the Onion'
    LESSON='Meissner and Pacinian Corpuscles: Flutter and Vibration'
    def construct(self):
        self.add(label('Meissner and Pacinian Corpuscles',y=1,color=GREY),label('Flutter and Vibration',y=.4,color=GREY),label(self.TITLE,y=-.65,size=54),Line([-1.5,-1.5,0],[1.5,-1.5,0],color=GOLD));self.finish()

class S01Q(Timed):
    def construct(self):
        self.add(stimulus(),axis(-1.45,'membrane potential · voltage',height=2.65))
        self.at('at the press');self.play(Create(impulses(-1.45,[-3.547,-3.24],x1=-2.9,amp=2.65)),run_time=.55)
        self.at('at the release',nth=0);self.play(Create(impulses(-1.45,[3.32,3.63],x0=-2.9,amp=2.65)),run_time=.5)
        self.at('In between');self.play(FadeIn(silence(-2.0)),run_time=.35)
        self.at('Where does');self.play(FadeIn(label('Where does that brevity come from?',y=-3.25,color=TEXT,size=32)),run_time=.4);self.finish()

class S02Three(Timed):
    def construct(self):
        c=corpuscle().shift(LEFT*1.1);self.add(c,key(),leader('outer core (the onion)',3.9,2,[1.4,1.9,0],INDIGO),leader('inner core (lamellar cells)',4.5,1,[.3,.7,0],TEAL),leader('nerve ending',3.9,-.6,[-.15,0,0],YELLOW),leader('axon',-4.6,-1.3,[-4.6,0,0],YELLOW));self.finish()

class S03Capsule(Timed):
    def construct(self):
        c=corpuscle();self.add(c,key(),suspects([0]))
        self.at('Its onion');self.play(c.outer.animate.set_stroke(width=6),run_time=.4)
        self.at('could absorb');p=probe();self.add(p);self.play(p[0].animate.shift(DOWN),c.outer.animate.stretch(.65,1),run_time=.8);self.finish()

class S04Channels(Timed):
    def construct(self):
        # A pressed skin inset links to the enlarged membrane below.
        skin=Line([-1.3,2.25,0],[1.3,2.25,0],color=YELLOW,stroke_width=5)
        press=RoundedRectangle(width=.8,height=.4,corner_radius=.06,color=ORANGE,fill_color=ORANGE,fill_opacity=.4).move_to([0,2.65,0])
        self.add(suspects([1]),skin,press,label('probe pressing skin',3.6,2.6,ORANGE,26),
            DashedLine([-1.3,2.25,0],[-5,1,0],color=GREY),DashedLine([1.3,2.25,0],[5,1,0],color=GREY),
            RoundedRectangle(width=10,height=2.8,corner_radius=.6,color=YELLOW,fill_color=YELLOW,fill_opacity=.08).shift(DOWN*.4),label('enlarged nerve ending',y=-2.2,color=YELLOW))
        def gate(x,closed=False):
            return VGroup(Line([x-.55,-.65,0],[x-.55,.65,0],color=GREEN,stroke_width=7),
                Line([x+.55,-.65,0],[x+.55,.65,0],color=GREEN,stroke_width=7),
                Line([x-.55,.15,0],[x if closed else x-.4, .15 if closed else .65,0],color=GREEN,stroke_width=7),
                Line([x+.55,.15,0],[x if closed else x+.4,.15 if closed else .65,0],color=GREEN,stroke_width=7))
        gates=VGroup(gate(-2),gate(2))
        self.at("the ending's channels");self.play(FadeIn(gates),run_time=.4)
        self.at('They could open');state=label('open',y=1.45,color=GREEN);self.play(FadeIn(state),press.animate.shift(DOWN*.2),run_time=.4)
        self.at('then close');self.play(Transform(state,label('closed · press still held',y=1.45,color=GREEN)),Transform(gates,VGroup(gate(-2,True),gate(2,True))),run_time=.5);self.finish()

class S05Spike(Timed):
    def construct(self):
        c=corpuscle();self.add(c,key(),suspects([2]))
        seg=Line([-3.1,0,0],[-1,0,0],color=YELLOW,stroke_width=20)
        self.at('the spike generator');self.play(Create(seg),run_time=.4)
        s=impulses(.2,[-2.6,-2],x0=-3.1,x1=-1,amp=.8)
        self.at('It could stop');self.play(Create(s),c.term.animate.set_fill(GREEN,1),run_time=.45);self.play(FadeOut(s,shift=LEFT),run_time=.4)
        self.add(leader('spike generator:',-4.5,-1.9,[-2,0,0],YELLOW),label('stopped firing',-4.5,-2.4,YELLOW,26))
        self.at('even while');self.play(FadeIn(VGroup(leader('ending: still',4.7,1.5,[.8,0,0],GREEN),label('depolarized',4.7,.95,GREEN,26))),run_time=.4);self.finish()

class S06Terms(Timed):
    def construct(self):
        self.add(stimulus(),axis(-1.4,'voltage',height=2.8))
        self.at('Two terms');self.play(Create(decay(-1.4,2,2.8)),run_time=.7)
        self.at('generator potential');self.play(FadeIn(label('generator potential',y=-2.05,color=GREEN,size=32)),run_time=.3)
        self.at('graded depolarization');self.play(FadeIn(label('graded depolarization',y=-2.6,color=GREEN)),run_time=.3)
        self.at('transduction current');self.play(FadeIn(label('driven by transduction current',y=-3.1,color=GREEN)),run_time=.3);self.finish()

class S07Imp(Timed):
    def construct(self):
        self.add(stimulus(2.05),axis(.05,'generator potential · voltage',height=1.3),decay(.05,2,1.3),axis(-2.15,'impulses · voltage',height=1.35))
        self.at('Impulses are');self.play(Create(impulses(-2.15,amp=1.35)),run_time=.8)
        self.at('action potentials');self.play(FadeIn(label('all-or-none action potentials',y=-3.1,color=YELLOW)),run_time=.3);self.finish()

class S08Model(Timed):
    def construct(self):
        locator=corpuscle().scale(.34).move_to([-5.1,0,0]);self.add(key(),timeline(1),locator,Line([-3.8,1.25,0],[-3.8,-1.25,0],color=INDIGO),Line([-3.8,1.25,0],[-3.45,1.65,0],color=INDIGO),Line([-3.8,-1.25,0],[-3.45,-1.65,0],color=INDIGO))
        layers=VGroup()
        for y in [1.8,0,-1.8]:
            xs=np.linspace(-3.6,3.6,25)
            layers.add(poly([(x,y+(.22 if i%2 else -.22)) for i,x in enumerate(xs)],INDIGO,6))
        fluid=VGroup(*[Rectangle(width=7.2,height=.9,color=BLUE,stroke_opacity=0,fill_color=BLUE,fill_opacity=.15).move_to([0,y,0]) for y in [.9,-.9]])
        self.add(layers,fluid,label('elastic layers',4.9,-1.8,INDIGO),label('fluid',4.8,.9,BLUE),label('fluid',4.8,-.9,BLUE))
        self.at('Loewenstein',lead=.35);self.play(FadeIn(label('Loewenstein and Skalak · 1966',y=2.8,size=30)),run_time=.35)
        self.at('fluid between');self.play(fluid.animate.set_fill(opacity=.35),run_time=.4)
        self.at('elastic layers');self.play(layers.animate.stretch(.8,1),run_time=.5);self.finish()

def capsule_model(pressed=False,relaxed=False):
    c=corpuscle(pressed,relaxed)
    if pressed:c.outer.stretch(1.65,1)
    return c.scale(1.15).shift(RIGHT*.45)


def fluid_dots(pressed=False):
    dots=VGroup()
    for rx,ry in [(3.0,2.4),(2.4,1.9),(1.85,1.4)]:
        for theta in np.linspace(0,2*np.pi,20,endpoint=False):
            dots.add(Dot([.45+1.15*rx*np.cos(theta),1.15*ry*np.sin(theta)*(.957 if pressed else 1),0],radius=.045,color=BLUE))
    return dots


class S09Press(Timed):
    def construct(self):
        c=capsule_model();p=probe();p[1].move_to([4.3,3.55,0]);p[0].move_to([.45,3.55,0]);dots=fluid_dots()
        footer=label('Classical capsule model',y=-3.5,color=INDIGO)
        self.add(c,p,dots,footer)
        self.at('At the instant');self.play(Transform(c,capsule_model(True)),p[0].animate.move_to([.45,3.2,0]),Transform(dots,fluid_dots(True)),FadeOut(footer),run_time=.55)
        self.at('fluid cannot move');self.play(FadeIn(label('fluid briefly trapped',y=-3.5,color=BLUE)),run_time=.3)
        self.at('ending is squeezed');self.play(c.term.animate.set_fill(GREEN,1),run_time=.35);self.finish()

class S10Hold(Timed):
    def construct(self):
        c=capsule_model(True);p=probe(True);p[0].move_to([.45,3.2,0]);p[1].move_to([4.3,3.55,0]);self.add(c,p)
        dots=fluid_dots(True);self.add(dots)
        self.at('the fluid flows');self.play(*[d.animate.shift(RIGHT*np.sign(d.get_x()-.45)*.55) for d in dots],FadeIn(label('← fluid flows sideways →',y=-3.5,color=BLUE)),run_time=1.1)
        self.at('stretched layers');self.play(c.outer.animate.set_stroke(width=5),run_time=.4)
        self.at('core relaxes');self.play(Transform(c,capsule_model(True,True)),run_time=.7);self.finish()

class S11Release(Timed):
    def construct(self):
        c=capsule_model(True,True);p=probe(True);p[0].move_to([.45,3.2,0]);p[1].move_to([4.3,3.55,0]);self.add(c,p)
        self.at('At the release');self.play(p[0].animate.move_to([.45,3.55,0]),run_time=.35)
        self.at('layers spring back');self.play(Transform(c,capsule_model()),run_time=.45)
        self.at('jolt the core');self.play(c.term.animate.set_fill(GREEN,1),c.inner.animate.set_stroke(width=7),FadeIn(label('second jolt',0,-3.5,GREEN)),run_time=.3);self.finish()

class S12Filter(Timed):
    def construct(self):
        self.add(label('Classical capsule model',y=3.4,color=INDIGO),stimulus(1.65),axis(-.8,'force reaching the ending (model)',height=1.1))
        xs=np.unique(np.r_[np.linspace(-5.4,5.5,600),-3.548,-3.547,3.319,3.32])
        response=poly([(x,-.8+(1.5*np.exp(-(x+3.547)/.35) if x>=-3.547 else 0)-(1.5*np.exp(-(x-3.32)/.35) if x>=3.32 else 0)) for x in xs],INDIGO)
        self.at('in this model');self.play(Create(response),run_time=.6)
        self.at('That is');self.play(FadeIn(label('high-pass filter',y=2.95,size=30)),FadeIn(label('passes fast change, blocks the steady part',y=-3.05,size=26)),run_time=.35);self.finish()

class S13Peel(Timed):
    def construct(self):
        c=corpuscle();self.add(c,key(),timeline(0),label('Isolated cat corpuscle · Loewenstein and Mendelson',y=2.9,size=26))
        self.at('peeled most layers');self.play(LaggedStart(*[FadeOut(e,shift=UP*.5+RIGHT*.8) for e in c.outer],lag_ratio=.55),run_time=2.7)
        self.add(label('outer layers removed',3.9,1.65,INDIGO))
        self.at('Then they');p=probe();p[1].move_to([3.9,2.25,0]);self.add(p);self.at('pressed',lead=.3);self.play(p[0].animate.move_to([0,.95,0]),c.inner.animate.stretch(.65,1),run_time=.3);self.wait(2);self.finish()

class S14Predict(Timed):
    def construct(self):
        self.add(cat_stage())
        prompt=label('Predict',y=-3.05,color=GOLD)
        self.at('Predict');self.play(FadeIn(prompt),run_time=.25)
        self.at('what should now');self.play(ReplacementTransform(prompt,label('What lasts through the hold?',y=-3.05,size=30)),run_time=.3);self.finish()

class S15Pause(Scene):
    def construct(self):self.camera.background_color=BG;self.add(cat_stage(question=True));self.wait(5)

class S16Reveal1(Timed):
    def construct(self):
        self.add(cat_stage())
        self.at('Only half');self.play(FadeIn(label('Only half of it',y=-3.05,color=GOLD)),run_time=.3)
        self.at('generator potential');self.add(DashedVMobject(decay(.1,.45,1.25,color=GREY)),label('intact',-2.5,.55,GREY,26))
        self.at('decayed much more slowly');self.play(Create(decay(.1,6,1.25)),FadeIn(label('peeled',2.7,.95,GREEN,26)),run_time=.8)
        self.at('mainly under');self.play(Transform(self.mobjects[0][0],label('Cat · mainly under intense compression',y=3.45,size=28)),run_time=.3);self.finish()

class S17Reveal2(Timed):
    def construct(self):
        self.add(cat_stage(potential=True,caveat=True))
        self.at('But the impulses');self.play(Create(impulses(-2.15,[-3.547],amp=1.65)),FadeIn(silence(-2.65)),run_time=.6)
        self.at('a single spike');self.play(Create(DashedLine([1.8,.1+1.25*np.exp(-(1.8+3.547)/6),0],[1.8,-2.15,0],color=GREEN)),run_time=.3);self.finish()

class S18Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(label('Peeled cat corpuscle: slow voltage, brief firing',y=3.45,size=30),
          stimulus(2.05,-5.8,-.6),stimulus(2.05,.6,5.8),
          axis(-1.5,'generator potential',-5.8,-.6,2.4),
          axis(-1.5,'impulses',.6,5.8,2.4),
          DashedVMobject(decay(-1.5,.21,2.4,-5.8,-.6,color=GREY)),
          decay(-1.5,2.86,2.4,-5.8,-.6),
          impulses(-1.5,[1.484],.6,5.8,2.4),
          label('voltage stays elevated',-3.2,-2.65,GREEN,26),
          label('single spike; then silent',3.2,-2.65,YELLOW,26),
          label('mainly under intense compression',y=-3.1,color=GREY,size=26))
        self.wait(3)

class S19Two(Timed):
    def construct(self):
        c=corpuscle();s=suspects();self.add(c,s)
        self.at('two stages');self.play(FadeIn(label('Two stages of brevity',y=3.35,size=32)),run_time=.3)
        self.at('One is');self.play(Transform(s,suspects([0])),FadeIn(VGroup(label('stage 1:',4.8,1.7,INDIGO,26),label('mechanics',4.8,1.15,INDIGO,26))),c.outer.animate.set_stroke(width=6),run_time=.45)
        self.at('The other');self.play(Transform(s,suspects([0,2])),FadeIn(VGroup(label('stage 2:',-4.7,-1.5,YELLOW,26),label('spike membrane',-4.7,-2,YELLOW,26))),run_time=.45);self.finish()

class S20Duck(Timed):
    def construct(self):
        head=VMobject(color=TEAL,fill_color=TEAL,fill_opacity=.35,stroke_width=4)
        head.set_points_smoothly([[-4,-2,0],[-4.1,-.5,0],[-4.2,1.1,0],[-3.7,2.0,0],[-2.7,2.3,0],[-1.7,1.85,0],[-1.35,1.0,0],[-1.25,.5,0],[-1.5,-.35,0],[-2.4,-.7,0],[-2.6,-2,0]])
        bill=VMobject(color=ORANGE,fill_color=ORANGE,fill_opacity=.6,stroke_width=4)
        bill.set_points_smoothly([[-1.45,.65,0],[-.3,.45,0],[1.7,.42,0],[2.15,.12,0],[2.1,-.25,0],[1.5,-.48,0],[-.5,-.45,0],[-1.5,-.1,0],[-1.45,.65,0]])
        duck=VGroup(head,bill,Dot([-2.15,1.15,0],radius=.13,color=TEXT),Dot([.1,.22,0],radius=.055,color=ORANGE),Line([-1.25,-.07,0],[1.9,-.07,0],color=ORANGE))
        bill_label=label('duck bill skin',2.4,-1,ORANGE);strip=timeline(2)
        self.add(duck,bill_label,label('Duck Herbst corpuscle · 2025',y=3.35,size=30),strip)
        self.at('researchers recorded');circle=Circle(radius=.4,color=TEXT).move_to([.8,.05,0]);self.play(Create(circle),run_time=.25);self.wait(.35)
        c=corpuscle().scale(.92).shift(UP*.3)
        self.play(Transform(circle,c.outer[0].copy()),FadeIn(c),FadeOut(duck),FadeOut(bill_label),FadeOut(strip),run_time=.8);self.remove(circle);self.add(pipette().shift(UP*.3))
        self.at('They used');self.play(FadeIn(label('ex vivo: skin removed from the animal',y=-2.55,size=26)),FadeIn(label('and kept alive in a dish',y=-3.05,size=26)),run_time=.35);self.finish()

class S21Strip(Timed):
    def construct(self):
        c=corpuscle();p=pipette();self.add(c,p,key(),label('Duck · outer core removed',y=-3.1,color=INDIGO))
        self.at('They removed');self.play(LaggedStart(*[FadeOut(e,shift=UP*.7+RIGHT*.6) for e in c.outer],lag_ratio=.25),run_time=1.3)
        self.at('kept the inner cells');self.play(c.inner.animate.scale(1.65),FadeIn(leader('inner core kept',4.6,-1.6,[2.2,-1,0],TEAL)),run_time=.6);self.finish()

class S22Predict2(Timed):
    def construct(self):
        self.add(current_stage())
        self.at('Predict');self.play(FadeIn(label('Pause and predict',3.6,2.4,GOLD,30)),run_time=.25)
        self.at('what should happen');self.play(FadeIn(label('Slow and sustained,',3.6,.7)),FadeIn(label('or still fast?',3.6,.1)),FadeIn(label('And the tuning?',3.6,-1)),run_time=.4);self.finish()

class S23Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(current_stage(question=True))
        ring=Circle(radius=.5,color=GOLD).move_to([3.6,-2.25,0]);self.add(ring)
        for n in range(5,0,-1):
            count=label(str(n),3.6,-2.25,GOLD,28);self.add(count);self.play(Transform(ring,Arc(radius=.5,start_angle=PI/2,angle=TAU*max(.001,(n-1)/5),color=GOLD).move_arc_center_to([3.6,-2.25,0])),run_time=1,rate_func=linear);self.remove(count)
        self.add(label('0',3.6,-2.25,GOLD,28))

class S24Reveal(Timed):
    def construct(self):
        self.add(current_stage())
        self.at('It stayed fast');self.play(Create(duck_current()),run_time=.6)
        self.at('frequency tuning');self.play(Create(tuning_plot()),run_time=.55)
        self.at('did not change');self.play(FadeIn(label('no significant change',3.6,2.25,size=26)),run_time=.3);self.finish()

class S25Bigger(Timed):
    def construct(self):
        self.add(current_stage(tuning=True),duck_current().set_color(GREY))
        self.at('did grow larger');self.play(Create(duck_current(True)),run_time=.6);self.add(label('before',-2.9,-1.35,TEXT,26),label('after',-2.9,-2.45,GREEN,26),Line([-4.48,-1.35,0],[-3.7,-1.35,0],color=GREY,stroke_width=2),Line([-4.48,-2.45,0],[-3.7,-2.45,0],color=GREEN,stroke_width=2))
        self.at('may still damp');self.play(FadeIn(label('outer core may damp',x=3.65,y=2.45,color=ORANGE,size=26),label('arriving force',x=3.65,y=1.9,color=ORANGE,size=26)),run_time=.3);self.finish()

class S26Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(current_stage(trace=True,big=True,tuning=True),duck_current().set_color(GREY),label('before',-2.9,-1.35,TEXT,26),label('after',-2.9,-2.45,GREEN,26),Line([-4.48,-1.35,0],[-3.7,-1.35,0],color=GREY,stroke_width=2),Line([-4.48,-2.45,0],[-3.7,-2.45,0],color=GREEN,stroke_width=2),label('outer core may damp',x=3.65,y=2.45,color=ORANGE,size=26),label('arriving force',x=3.65,y=1.9,color=ORANGE,size=26));self.wait(3)


def deterioration():
    g=VGroup(label('Time since dissection',y=3.35,size=32),Arrow([-4.8,2.4,0],[4.8,2.4,0],color=GREY,buff=0),label('early',-3.3,2.85),label('late',3.3,2.85),
        label('current (inward)',-3.3,.35,GREEN,26),label('current (inward)',3.3,.35,GREEN,26),base(-.2,-5.8,-.7),base(-.2,.7,5.8),label('time (ms) →',-3.3,-2.2,GREY,26),label('time (ms) →',3.3,-2.2,GREY,26),decay(-.2,.16,1.7,-5.8,-.7,True))
    for x in [-3.3,3.3]:
        ending=corpuscle();ending.outer.set_opacity(0);ending.scale(.5).move_to([x,1.3,0]);g.add(ending)
    return g

class S27Reconcile(Timed):
    def construct(self):
        g=deterioration();self.add(g)
        self.at('only as');self.play(Create(decay(-.2,1.5,1.7,.7,5.8,True)),g[-1].inner.animate.set_stroke(opacity=.25).set_fill(opacity=.02),g[-1].term.animate.set_opacity(.25),g[-1].axon.animate.set_opacity(.25),FadeIn(label('slow only after deterioration',y=-3.05,size=30)),run_time=.8);self.finish()

class S28Dying(Timed):
    def construct(self):
        self.add(label('Similar slow traces, different explanations',y=3.35,size=30),label('damaged ending',-3.3,2.55,GREY),label('filter lost?',3.3,2.55,INDIGO))
        left=corpuscle();left.outer.set_opacity(0);left.scale(.55).move_to([-3.3,.8,0]);left.inner.set_stroke(opacity=.3).set_fill(opacity=.02);left.term.set_opacity(.3);left.axon.set_opacity(.3)
        right=corpuscle();right.outer.set_stroke(opacity=.1).set_fill(opacity=0);right.scale(.55).move_to([3.3,.8,0])
        self.add(left,right,base(-1,-5.8,-.7),base(-1,.7,5.8),decay(-1,1.5,1.3,-5.8,-.7,True),label('time (ms) →',-3.3,-2.55,GREY,26),label('time (ms) →',3.3,-2.55,GREY,26))
        self.at('can look like');self.play(Create(decay(-1,1.5,1.3,.7,5.8,True)),run_time=.6)
        self.at('one reading');self.play(FadeIn(label('One reading · not shown directly',y=-3.1,color=RED)),run_time=.3);self.finish()

class S29Take(Timed):
    def construct(self):
        c=corpuscle();c.outer.set_stroke(opacity=.1).set_fill(opacity=0);c.scale(.85).shift(UP*.5);c.outer.stretch(.8,1)
        framework=VGroup(label('1. capsule',-4.7,-2.7,GREY,26),label('2. terminal channels',-.2,-2.7,GREEN,26),label('3. spike generator',4.4,-2.7,GREY,26))
        self.add(c,key(),framework,label('In this duck preparation',y=2.95,size=32),label('inner core kept',4.7,1.4,TEAL,26),label('cat result; not tested in duck',4.3,-3.1,GREY,26))
        self.at('ending stayed fast');self.play(c.term.animate.set_fill(GREEN,1),run_time=.4)
        self.at('without the outer core');self.play(FadeIn(label('Outer core removed · inner core retained',y=-1.65,size=28)),run_time=.35)
        self.at('fast adaptation does not need');self.play(FadeIn(label('Fast adaptation persists in this preparation',y=-2.15,color=GREEN,size=26)),run_time=.35);self.finish()

class S30End(EndCard):
    LINE='In this duck preparation, the ending stayed fast without the outer core.'
    def construct(self):
        self.add(label('In this duck preparation,',y=.9,size=38),label('the ending stayed fast',y=.1,size=38),label('without the outer core.',y=-.7,size=38),label('biochemistrypedia.com',y=-1.8,color=TEAL,size=26));self.finish()
