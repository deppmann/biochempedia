"""Who Puts the Potassium Back — revised word-timed teaching film.

COLOR MAP: YELLOW neurons; BLUE/teal potassium and its equilibrium potential;
GREEN astrocytes and Kir4.1; ORANGE oligodendrocytes; RED deletion/knockout;
PURPLE gap junctions; GOLD sodium-potassium pumps; PINK electrical current;
GREY axes, electrodes and membranes. Current arrows never represent ion tracks.

All traces are evaluated from models, not sketched or digitized recordings:
Nernst E = 61.5 log10(Ko/140); equal release impulses with exp(-t/2 s)
clearance. Uptake curves are explicitly qualitative normalized models. Their
arbitrary amplitudes and different kinetics do not estimate experimental effects.
"""
import numpy as np
from bp_style import *

NEUR, KC, ASTRO, OLIG, BAD = YELLOW, BLUE, GREEN, '#F29E4C', RED
PUMP, JUNCTION, CURRENT = GOLD, '#B69BE8', '#F495CA'
EK = lambda k: 61.5 * np.log10(np.asarray(k) / 140.)


def solid_chip(text, color=KC, size=28):
    g = chip(text, color, size=size)
    g[0].set_fill(BG, opacity=1)
    return g


def heading(s, color=TEXT):
    return T(s, 34, color).move_to([0, 3.15, 0])


def blob(cx, cy, w, h, color, label=None):
    e = Ellipse(width=w, height=h, stroke_color=color, stroke_width=4,
                fill_color=color, fill_opacity=.12).move_to([cx, cy, 0])
    return VGroup(e, *([T(label, 28, color).move_to(e)] if label else []))


def kdot(p):
    return Dot([p[0], p[1], 0], radius=.09, color=KC)


def scatter(n, xr, yr, seed):
    rng = np.random.default_rng(seed)
    pts = []
    while len(pts) < n:
        p = np.array([rng.uniform(*xr), rng.uniform(*yr)])
        if all(np.linalg.norm(p-q) > .23 for q in pts):
            pts.append(p)
    return VGroup(*[kdot(p) for p in pts])


def arr(a, b, color=KC):
    return Arrow(a, b, buff=0, color=color, stroke_width=5, tip_length=.18)


def cross(p, r=.22):
    p = np.array(p)
    return VGroup(Line(p+[-r,-r,0],p+[r,r,0],color=BAD,stroke_width=6),
                  Line(p+[-r,r,0],p+[r,-r,0],color=BAD,stroke_width=6))


def ek_label(size=28):
    # Separate Text objects give a true visual subscript without LaTeX.
    e, k = T('E',size,KC), T('K',26,KC)
    k.next_to(e, RIGHT, buff=.015).shift(DOWN*.12)
    return VGroup(e,k)


def trace(fn, x0=-4.7, width=10.2, base=-2.25, gain=.17, end=10, color=ASTRO):
    ts = np.linspace(0,end,801)
    return VMobject(color=color,stroke_width=4).set_points_as_corners(
        [[x0+width*t/end,base+gain*float(fn(t)),0] for t in ts])


def release(t, duration=3., rate=3.):
    return sum(.32*np.exp(-(t-s)/2.) for s in np.arange(1,1+duration,1/rate) if t>=s)


def record_base():
    return VGroup(heading('Glial voltage'),
        T('axon impulses',26,NEUR).move_to([-3.8,2.42,0]),
        Line([-4.7,1.6,0],[5.5,1.6,0],color=GREY),
        arr([-4.7,-2.25,0],[-4.7,1.0,0],GREY),
        T('more positive ↑',26,GREY).move_to([-2.8,.85,0]),
        T('very negative',26,GREY).move_to([-3.3,-2.7,0]),
        arr([-4.7,-2.25,0],[5.8,-2.25,0],GREY),
        T('time',26,GREY).move_to([5.2,-2.7,0]),
        T('illustrative model • not a recording',26,GREY).move_to([0,-3.3,0]))


def train(duration=3,rate=3,x0=-4.7,width=10.2,end=10,y=1.6):
    return VGroup(*[Line([x0+width*s/end,y,0],[x0+width*s/end,y+.46,0],color=NEUR,stroke_width=3)
                    for s in np.arange(1,1+duration,1/rate)])


def glial_trace(duration=3,rate=3,**kw):
    return trace(lambda t: EK(3+release(t,duration,rate))-EK(3),**kw)


def outside():
    return VGroup(RoundedRectangle(width=11.5,height=.53,corner_radius=.12,
        stroke_color=GREY,stroke_width=1.2,fill_color=GREY,fill_opacity=.06).move_to([0,.97,0]),
        T('outside',26,GREY).move_to([5.0,1.5,0]))


def cluster():
    return VGroup(*[kdot([-4.7+(i%6)*.27,.85+(i//6)*.23]) for i in range(12)])


def network(tall=False):
    cy,h = (-.7,3.9) if tall else (-1.,3.2)
    cells = VGroup(*[blob(x,cy,3.65,h,ASTRO) for x in (-4,0,4)])
    joins = VGroup(*[RoundedRectangle(width=.38,height=.75,corner_radius=.07,
              color=JUNCTION,fill_color=JUNCTION,fill_opacity=.8).move_to([x,cy,0]) for x in (-2,2)])
    labels = VGroup(*[T('astrocyte',26,ASTRO).move_to([x,-2.95,0]) for x in (-4,0,4)])
    return VGroup(cells,joins,labels)


def junction_labels(y=-1.):
    groups=VGroup()
    for x in (-2,2):
        label=T('gap junction',26,JUNCTION).move_to([x,y-1.07,0])
        backing=Rectangle(width=label.width+.14,height=label.height+.12,
            stroke_width=0,fill_color=BG,fill_opacity=1).move_to(label)
        groups.add(VGroup(Line([x,y-.4,0],[x,y-.8,0],color=JUNCTION),backing,label))
    return groups


def voltage_panel(high=False,raised=False):
    ks=np.array([4.,3.,3.]) if high else np.array([3.15,3.,2.9])
    es=EK(ks); v=float(es.mean()) if raised else float(EK(3.))
    y=lambda z: 1.7+(z-float(EK(3)))*.075
    scales=VGroup(*[VGroup(Line([x,1.4,0],[x,2.5,0],color=GREY),
        *[Line([x-.07,z,0],[x+.07,z,0],color=GREY) for z in (1.45,1.95,2.45)]) for x in (-4,0,4)])
    line=VGroup(Line([-5.65,y(v),0],[5.65,y(v),0],color=ASTRO,stroke_width=4),
        T('network voltage',26,ASTRO).move_to([-2,1.45,0]))
    ticks=VGroup(*[VGroup(Line([x-.22,y(e),0],[x+.22,y(e),0],color=KC,stroke_width=5),
        ek_label().move_to([x+.57,2.43,0]),
        Line([x+.38,2.29,0],[x+.18,y(e)+.08,0],color=KC,stroke_width=1.5)) for x,e in zip((-4,0,4),es)])
    axis=VGroup(arr([-6.05,1.4,0],[-6.05,2.65,0],GREY),
        T('more positive',26,GREY).move_to([-4.65,2.74,0]))
    return VGroup(scales,line,ticks,axis)


def channels():
    # Label beside a membrane pore; the arrow crosses the pore, never the text.
    return VGroup(*[VGroup(RoundedRectangle(width=.32,height=.48,corner_radius=.05,
         color=ASTRO,fill_color=BG,fill_opacity=1).move_to([x,.6,0]),
         T('Kir4.1',26,ASTRO).move_to([x+1.35,.55,0]),
         Line([x+.2,.6,0],[x+.8,.55,0],color=ASTRO)) for x in (-4,0,4)])


def flows(color=KC):
    return VGroup(arr([-4,1.25,0],[-4,-.3,0],color),
                  arr([0,-.3,0],[0,1.25,0],color),arr([4,-.3,0],[4,1.25,0],color))


def flow_labels(inout=False):
    return VGroup(*[T(s,26,KC).move_to([x,-.72,0]) for x,s in zip((-4,0,4),
        ('in here','out there','out there') if inout else ('K+ in','K+ out','K+ out'))])


def prediction_one():
    curve=glial_trace()
    evidence=VGroup(record_base(),curve,train()).set_opacity(.22)
    curve.set_fill(opacity=0)
    plate=RoundedRectangle(width=11.5,height=1.6,corner_radius=.2,
        fill_color=BG,fill_opacity=.97,stroke_opacity=0).move_to([0,.25,0])
    return VGroup(evidence,plate,T('Pause. What is the glial cell sensing?',36).move_to([0,.25,0]))


def knockout_chip(x,y,color=ASTRO):
    c=solid_chip('Kir4.1',color,28).move_to([x,y,0])
    return VGroup(c,cross([x-c.width/2-.35,y,0]))


def prediction_two():
    return VGroup(heading('Pause. What else might fail?'),
        blob(0,-.65,7,4.2,ASTRO,'astrocyte'),
        knockout_chip(-2.2,1.85),solid_chip('glutamate transporter',GREY,28).move_to([1.4,1.85,0]),
        T('?',48).move_to([1.4,2.55,0]))


def countdown(scene):
    ring=Circle(radius=.33,color=GREY,stroke_width=2).move_to([6.05,-3.15,0])
    arc=Arc(radius=.33,start_angle=PI/2,angle=TAU,color=GOLD,stroke_width=6).move_arc_center_to([6.05,-3.15,0])
    left=ValueTracker(1)
    arc.add_updater(lambda a:a.become(Arc(radius=.33,start_angle=PI/2,
        angle=max(.001,TAU*left.get_value()),color=GOLD,stroke_width=6).move_arc_center_to([6.05,-3.15,0])))
    scene.add(ring,arc)
    scene.play(left.animate.set_value(0),run_time=5,rate_func=linear)
    arc.clear_updaters()


def uptake_panel(glutamate=False):
    title='Glutamate uptake' if glutamate else 'Potassium uptake'
    ylabel='glutamate uptake' if glutamate else 'potassium uptake (relative)'
    base=VGroup(heading(title),
        arr([-4.95,-2.15,0],[5.7,-2.15,0],GREY),arr([-4.95,-2.15,0],[-4.95,1.9,0],GREY),
        T(ylabel,26,GREY).move_to([-2.5,2.12,0]),
        T('time after stimulus',26,GREY).move_to([1,-2.62,0]),
        T('qualitative model • not measured data',26,GREY).move_to([0,-3.3,0]))
    # Distinct normalized kinetic examples; neither encodes a measured ratio.
    tau=3.8 if glutamate else 2.4
    f=lambda t: (1-np.exp(-t/.35))*np.exp(-t/tau)
    reduced=.68 if glutamate else .50
    end=5.0
    control=trace(f,x0=-4.95,width=7.8,base=-2.15,gain=5.0,end=end)
    ko=trace(lambda t:reduced*f(t),x0=-4.95,width=7.8,base=-2.15,gain=5.0,end=end,color=BAD)
    labels=VGroup(T('control',26,ASTRO).move_to([4.55,-2.15+5*f(end)+.23,0]),
        T('Kir4.1 knockout',26,BAD).move_to([4.55,-2.15+5*reduced*f(end)+.03,0]))
    direct=VGroup()
    for text,amp in zip(labels,(1,reduced)):
        start=[2.85,-2.15+5*amp*f(end),0]
        endp=text.get_left()+LEFT*.12
        direct.add(VGroup(Line(start,endp,color=text.color,stroke_width=1.5),text))
    return base,VGroup(control,ko),direct


def voltage_meter(negative=True):
    y=-1.5 if negative else .65
    return VGroup(Line([1.7,-2.25,0],[1.7,1.8,0],color=GREY),
        T('voltage',28).move_to([3.1,2.1,0]),
        T('less negative',26,GREY).move_to([3.75,1.12,0]),
        T('negative',26,GREY).move_to([3.5,-1.95,0]),
        Line([-.35,-.55,0],[.6,-.55,0],color=GREY),
        Line([.6,-.55,0],[.6,y,0],color=GREY),
        arr([.6,y,0],[2.05,y,0],ASTRO))


def meter_cell():
    return blob(-3,-.65,5.3,3.7,ASTRO,'astrocyte')


def limits(oligo=True):
    g=VGroup(heading('Deletion began in development'),
        arr([-5.5,2.12,0],[5.5,2.12,0],GREY),
        T('early',26,GREY).move_to([-5.15,2.57,0]),T('later',26,GREY).move_to([5.05,2.57,0]),
        Line([-3.8,1.95,0],[-3.8,2.3,0],color=BAD,stroke_width=5),
        T('deletion starts',26,BAD).move_to([-2.45,2.55,0]),
        blob(-3,-.55,5.2,3.8,ASTRO,'astrocyte'),knockout_chip(-3,1.25))
    if not oligo:
        # Keep the lone cell centred until the second cell is named.
        g[-2:].shift(RIGHT*3)
    if oligo:
        g.add(blob(3,-.55,5.2,3.8,OLIG,'oligodendrocyte'),knockout_chip(3,1.25,OLIG),
            T('also deleted here',26,BAD).move_to([3,-1.65,0]))
    return g


class S00Title(TitleCard):
    TITLE='Who Puts the Potassium Back'
    LESSON='Neurons and Glia at Work'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON.upper(),26,GREY),
                 T('Who Puts the\nPotassium Back',46,font=TITLE_FONT),
                 Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.3)
        self.play(FadeIn(g),run_time=.6); self.finish()


class S01Question(SpokenScene):
    def construct(self):
        cells=VGroup(blob(-3.3,-.4,5.4,5.1,NEUR,'neuron'),blob(3.3,-.4,5.4,5.1,NEUR,'neuron'))
        dots=scatter(18,(-.4,.4),(-2.4,1.7),3)
        labs=VGroup(T('extracellular space',26,GREY).move_to([0,-3.2,0]),
            T('K+',28,KC).move_to([0,2.1,0]))
        self.add(cells,dots,labs)
        self.at('Who does it')
        self.play(FadeIn(heading('Who clears the potassium outside neurons, and how?')),run_time=.4)
        self.finish()


class S02Who(SpokenScene):
    def construct(self):
        date=T('1966',96,GOLD)
        self.add(date)
        # Transcript spells these surnames differently: cue on stable first names.
        for cue,name,y in [('Stephen','Stephen Kuffler',1.5),('John','John Nicholls',0),('and Richard','Richard Orkand',-1.5)]:
            self.at(cue)
            if cue=='Stephen':
                self.play(date.animate.scale(34/96).move_to([0,3.15,0]),run_time=.25)
                self.play(FadeIn(T(name,40).move_to([0,y,0]),shift=RIGHT*.2),run_time=.2)
            else:
                self.play(FadeIn(T(name,40).move_to([0,y,0]),shift=RIGHT*.2),run_time=.35)
        self.at('recorded from')
        self.play(FadeIn(T('recording from glial cells',30,ASTRO).move_to([0,-2.85,0])),run_time=.4)
        self.finish()


class S03Prep(SpokenScene):
    def construct(self):
        axons=VGroup(*[RoundedRectangle(width=11.5,height=.75,corner_radius=.25,color=NEUR,
                    fill_color=NEUR,fill_opacity=.1).move_to([0,y,0]) for y in (-2.15,1.95)])
        self.add(heading('Mudpuppy optic nerve • Necturus'),axons,
            *[T('axon',28,NEUR).move_to([-4.7,y,0]) for y in (-2.15,1.95)],
            blob(-1,-.1,4.3,2.65,ASTRO,'glial cell'))
        electrode=VGroup(Line([5.5,1.0,0],[.35,.3,0],color=GREY,stroke_width=5),
            T('microelectrode',28,GREY).move_to([3.5,-.35,0]),
            Line([2.4,-.15,0],[1.25,.37,0],color=GREY))
        self.at('worked in'); self.play(Create(electrode[0]),FadeIn(electrode[1:]),run_time=.6)
        self.finish()


class S04Trace(SpokenScene):
    def construct(self):
        self.add(record_base())
        self.at('Read the record')
        self.play(Create(trace(lambda t:0)),run_time=1.1,rate_func=linear)
        self.at('sits steady')
        tick=VGroup(Line([-4.7,-2.4,0],[-4.7,-2.0,0],color=ASTRO),
            T('recording begins',26,ASTRO).move_to([-2.9,-1.7,0]))
        self.play(FadeIn(tick),run_time=.4); self.finish()


class S05Train(SpokenScene):
    def construct(self):
        self.add(record_base())
        clock=ValueTracker(0)
        line=trace(lambda t:0,end=.001,width=.00102)
        spikes=train()
        event_times=np.arange(1,4,1/3)
        for spike in spikes:
            spike.set_stroke(opacity=0)
        line.add_updater(lambda m:m.become(glial_trace(end=max(.001,clock.get_value()),
            width=1.02*max(.001,clock.get_value()))))
        spikes.add_updater(lambda g:[spike.set_stroke(opacity=float(clock.get_value()>=t))
            for spike,t in zip(g,event_times)])
        self.add(line,spikes)
        self.at('neighboring axons')
        # One model clock drives both event marks and voltage samples. This
        # avoids Create's path-length interpolation delaying the first rise.
        self.play(clock.animate.set_value(4),run_time=4.6,rate_func=linear)
        line.clear_updaters(); spikes.clear_updaters()
        self.finish()


class S06More(SpokenScene):
    def construct(self):
        base=record_base(); base.remove(base[1],base[2],base[4])
        def raster(d,r,y):
            return train(d,r,y=y).stretch(.55,1,about_point=np.array([0,y,0]))
        self.add(base,glial_trace(end=4,width=4.08).set_stroke(opacity=.5),raster(3,3,1.4),
            *[Line([-4.7,y,0],[5.5,y,0],color=GREY,stroke_width=1) for y in (1.4,1.9,2.4)],
            *[T(s,26,NEUR).move_to([-5.65,y+.1,0]) for s,y in [('train',1.4),('longer',1.9),('faster',2.4)]])
        self.add(T('glial voltage (more positive up)',26,GREY).move_to([2.7,1.1,0]))
        longer=glial_trace(5,3,end=6,width=6.12,color='#D6E9CE')
        faster=glial_trace(3,6,end=4,width=4.08,color=ASTRO)
        self.at('Longer and')
        self.play(Create(longer),Create(raster(5,3,1.9)),
            FadeIn(T('longer',26,'#D6E9CE').move_to([3.8,.32,0])),run_time=.65)
        self.at('faster trains')
        self.play(Create(faster),Create(raster(3,6,2.4)),FadeIn(T('faster',26,ASTRO).move_to([3.8,-.3,0])),run_time=1.1)
        self.at('When the axons stop')
        recovery=VGroup()
        for d,r,begin,c,opacity in [(3,3,4,ASTRO,.5),(5,3,6,'#D6E9CE',1),(3,6,4,ASTRO,1)]:
            ts=np.linspace(begin,10,401)
            recovery.add(VMobject(color=c,stroke_width=4,stroke_opacity=opacity).set_points_as_corners(
                [[-4.7+1.02*t,-2.25+.17*float(EK(3+release(t,d,r))-EK(3)),0] for t in ts]))
        self.play(*[Create(c) for c in recovery],run_time=1.35,rate_func=linear)
        self.at('recovers over seconds')
        bar=VGroup(Line([-.4,-2.75,0],[1.64,-2.75,0],color=GREY,stroke_width=4),
            Line([-.4,-2.65,0],[-.4,-2.85,0],color=GREY),Line([1.64,-2.65,0],[1.64,-2.85,0],color=GREY),
            T('seconds',26,GREY).move_to([2.6,-2.75,0]))
        self.play(FadeIn(bar),run_time=.4); self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        self.add(prediction_one()); self.at('What is'); self.finish()


class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction_one()); countdown(self)


class S09Reveal(SpokenScene):
    def construct(self):
        bath=RoundedRectangle(width=3.2,height=4.6,corner_radius=.25,color=KC,
            fill_color=KC,fill_opacity=.07).move_to([-4.55,-.1,0])
        self.add(heading('Potassium electrode • Nernst model',KC),bath,
            blob(-4.55,-.85,2.7,2.2,ASTRO,'glial cell'),T('bath K+',28,KC).move_to([-4.55,1.75,0]))
        base=-2.05; x0=-2.35; width=8.1
        self.add(arr([x0,base,0],[6,base,0],GREY),arr([x0,base,0],[x0,2.25,0],GREY),
            T('glial voltage ↑',26,GREY).move_to([-.55,2.43,0]),
            T('bath K+ raised in steps →',26,GREY).move_to([1.8,-2.65,0]))
        # Qualitative concentration levels, computed Nernst heights, no invented data.
        step=lambda t:EK(3 if t<3 else 4 if t<6 else 6)-EK(3)
        curve=trace(step,x0=x0,width=width,base=base,gain=.20,end=9)
        levels=VGroup(*[T(s,26,KC).move_to([x,base+.20*float(EK(k)-EK(3))+.43,0])
            for x,k,s in [(-1.1,3,'low K+'),(1.6,4,'higher K+'),(4.3,6,'highest K+')]])
        dots=scatter(4,(-5.55,-3.55),(.45,1.24),4); self.add(dots)
        self.at('in the bath')
        extra=VGroup(*[kdot([-5.5+(i%5)*.43,.55+(i//5)*.35]) for i in range(10)])
        self.play(AnimationGroup(Create(curve,run_time=2.1),
            LaggedStart(*[FadeIn(l) for l in levels],lag_ratio=1.5,run_time=2.1),
            Succession(Wait(.65),FadeIn(extra[:5],run_time=.35),Wait(.4),FadeIn(extra[5:],run_time=.35)),
            bath.animate.set_fill(KC,.2)),run_time=2.1,rate_func=linear)
        self.at('as a potassium')
        self.play(FadeIn(T('behaves like a potassium electrode',28).move_to([0,-3.3,0])),run_time=.4)
        self.finish()


class S10Reveal2(SpokenScene):
    def construct(self):
        self.add(heading('Glia sense released K+',KC),blob(-3,1.65,5.3,1.15,NEUR,'active axons'),
            blob(-3,-1.1,5.3,2.8,ASTRO,'glial cell'))
        line=trace(lambda t:0,x0=.6,width=5,base=-2.1,gain=.16); self.add(line,
            arr([.6,-2.1,0],[5.8,-2.1,0],GREY),arr([.6,-2.1,0],[.6,1.8,0],GREY),
            T('glial voltage',26,GREY).move_to([3,2.1,0]),T('time →',26,GREY).move_to([4.8,-2.6,0]))
        dots=scatter(12,(-5.1,-.9),(.15,.75),8)
        self.at('the axons released')
        self.play(LaggedStart(*[FadeIn(d,shift=DOWN*.4) for d in dots],lag_ratio=.03),run_time=.55)
        self.at('as it built up')
        self.play(Transform(line,glial_trace(5,4,x0=.6,width=5,base=-2.1,gain=.16)),run_time=.7)
        self.add(T('illustrative model',26,GREY).move_to([3,-3.3,0])); self.finish()


class S11Network(SpokenScene):
    def construct(self):
        net=network(tall=True); self.add(heading('Astrocyte network',ASTRO),net[0],net[2])
        self.at('joined by gap junctions')
        self.play(FadeIn(net[1]),FadeIn(junction_labels(-.7)),run_time=.6)
        self.at('link the insides')
        self.play(*[Indicate(j,color=JUNCTION) for j in net[1]],run_time=.6)
        self.at('almost purely permeable')
        self.play(FadeIn(T('membranes almost purely permeable to K+',28,KC).move_to([0,2.2,0])),
            FadeIn(T('K+',28,KC).move_to([-4,.4,0])),run_time=.5); self.finish()


class S12Voltage(SpokenScene):
    def construct(self):
        self.add(network(),heading('Nearly shared voltage',ASTRO))
        p=voltage_panel()
        self.at('strongly coupled network'); self.add(p[0],p[3]); self.play(Create(p[1]),run_time=.65)
        self.at('What differs'); self.play(FadeIn(p[2]),run_time=.6)
        self.at('set by the local potassium')
        note=VGroup(T('local',26,KC),ek_label(),T('depends on local K+',26,KC)).arrange(RIGHT,buff=.14).move_to([0,-3.4,0])
        self.play(FadeIn(note),run_time=.4); self.finish()


class S13High(SpokenScene):
    def construct(self):
        p=voltage_panel(); self.add(network(),outside(),p,heading('One active spot'))
        self.at('one spot fire hard')
        self.play(FadeIn(cluster()),FadeIn(VGroup(T('high K+ outside',26,KC).move_to([-1.65,.98,0]), Line([-2.9,.98,0],[-3.2,.98,0],color=KC))),run_time=.5)
        self.at('more positive'); self.play(Transform(p,voltage_panel(True,False)),run_time=.65); self.finish()


class S14In(SpokenScene):
    def construct(self):
        self.add(network(),outside(),cluster(),voltage_panel(True,False),heading('K+ enters at the high-K+ site',KC))
        self.at('potassium flows in')
        self.play(GrowArrow(flows()[0]),FadeIn(flow_labels()[0]),run_time=.55)
        self.at('it enters through'); self.play(FadeIn(channels()[0]),run_time=.45); self.finish()


class S15Out(SpokenScene):
    def construct(self):
        p=voltage_panel(True,False)
        self.add(network(),outside(),cluster(),p,channels()[0],flows()[0],flow_labels()[0],
            heading('Entry depolarizes the network slightly',ASTRO))
        self.at('depolarizes the network slightly'); self.play(Transform(p,voltage_panel(True,True)),run_time=.65)
        self.at('potassium now flows out')
        self.play(FadeIn(channels()[1:]),*[GrowArrow(a) for a in flows()[1:]],FadeIn(flow_labels()[1:]),run_time=.65)
        self.finish()


class S16Loop(SpokenScene):
    def construct(self):
        # Rounded current circuit returns through the same extracellular strip.
        # Both distal exits share the inside leg; no moving potassium tracks.
        net=network()
        title=heading('Spatial buffering',ASTRO)
        self.add(net,outside(),title,junction_labels())
        pores=VGroup(*[VGroup(RoundedRectangle(width=.32,height=.48,corner_radius=.05,
            color=ASTRO,fill_color=BG,fill_opacity=1).move_to([x,.6,0]),
            T('Kir4.1',26,ASTRO).move_to([x+.85,-.12,0])) for x in (-4,0,4)])
        self.add(pores,T('current loop',30,CURRENT).move_to([0,2.6,0]))
        limbs=VGroup(arr([-4,.45,0],[-4,-.3,0],CURRENT),
            arr([0,-.3,0],[0,.45,0],CURRENT),arr([4,-.3,0],[4,.45,0],CURRENT))
        self.at('at the same time')
        self.play(*[GrowArrow(a) for a in limbs],run_time=.5)
        self.at('one loop of current')
        ring=Polygon([-4,.97,0],[-4,-.7,0],[4,-.7,0],[4,.97,0],
            color=CURRENT,stroke_width=5,fill_opacity=0).round_corners(.25)
        branch=VMobject(color=CURRENT,stroke_width=5).start_new_path(np.array([0,-.7,0]))
        branch.add_line_to(np.array([0,.72,0]))
        branch.add_cubic_bezier_curve_to(np.array([0,.86,0]),np.array([-.11,.97,0]),np.array([-.25,.97,0]))
        paths=VGroup(ring,branch,arr([-2,-.7,0],[-1,-.7,0],CURRENT),
            arr([1,-.7,0],[2,-.7,0],CURRENT),arr([2,.97,0],[1,.97,0],CURRENT),
            arr([-1,.97,0],[-2,.97,0],CURRENT))
        self.play(Create(paths),FadeIn(T('K+ leaves far away; it need not be the same K+ that entered',26,KC).move_to([0,-3.45,0])),run_time=.6)
        self.at('spatial buffering')
        self.play(Indicate(title,color=ASTRO,scale_factor=1.03),run_time=.4)
        self.finish()


class S17Spread(SpokenScene):
    def construct(self):
        dots=cluster(); self.add(network(),outside(),channels(),flows(),flow_labels(True),dots,
            heading('Redistribution: in here, out there',ASTRO))
        self.at('where it is high')
        targets=[[-5.25+i*.94,.97,0] for i in range(12)]
        self.play(*[d.animate.move_to(p) for d,p in zip(dots,targets)],run_time=2.1,rate_func=smooth)
        self.at('On balance')
        self.play(FadeIn(T('On balance: still outside, spread thinner',30,KC).move_to([0,-3.4,0])),run_time=.45); self.finish()


class S18Pumps(SpokenScene):
    def construct(self):
        self.add(heading('Uptake: back inside',PUMP),blob(-3,-.9,5.2,3.6,ASTRO),blob(3,-.9,5.2,3.6,NEUR),
            T('astrocyte',28,ASTRO).move_to([-3,-2.25,0]),T('neuron',28,NEUR).move_to([3,-2.25,0]))
        dots=VGroup(*[kdot([x+dx,2.05]) for x in (-3,3) for dx in (-.22,0,.22)])
        self.add(dots,T('K+ outside',26,KC).move_to([0,2.4,0]))
        self.at('Sodium potassium pumps')
        pumps=VGroup(*[VGroup(RoundedRectangle(width=.55,height=.55,corner_radius=.08,
            color=PUMP,fill_color=BG,fill_opacity=1).move_to([x,.9,0]),
            T('Na+/K+ pump',28,PUMP).move_to([x+.4,1.65,0],aligned_edge=LEFT),
            Line([x+.28,1.15,0],[x+.55,1.45,0],color=PUMP)) for x in (-3,3)])
        self.play(FadeIn(pumps),run_time=.55)
        self.at('take potassium up')
        arrows=VGroup(*[arr([x,1.8,0],[x,-1.6,0],KC) for x in (-3,3)])
        self.play(*[GrowArrow(a) for a in arrows],run_time=.3)
        self.play(*[d.animate.shift(DOWN*3.65) for d in dots],run_time=.9,rate_func=linear); self.finish()


class S19Debate(SpokenScene):
    def construct(self):
        self.add(heading('How much does each contribute?'))
        # Large balance with two mechanisms as its pans; no proposed proportion.
        beam=VGroup(Line([-4.4,1.05,0],[4.4,1.05,0],color=GREY,stroke_width=5),
            Line([0,1.05,0],[0,-2.2,0],color=GREY,stroke_width=5),
            Line([-1,-2.2,0],[1,-2.2,0],color=GREY,stroke_width=5))
        pans=VGroup(*[VGroup(Line([x,1.05,0],[x,-.45,0],color=GREY),
            solid_chip(s,c,32).move_to([x,-.85,0])) for x,s,c in [(-3.4,'Redistribution',ASTRO),(3.4,'Uptake',PUMP)]])
        self.add(beam,pans)
        self.at('each mechanism contributes'); self.play(FadeIn(T('?',64).move_to([0,1.9,0])),run_time=.4)
        self.at('still debated'); self.play(Indicate(beam,color=GREY,scale_factor=1.02),run_time=.4); self.finish()


class S20Ko(SpokenScene):
    def construct(self):
        self.add(heading('Glial Kir4.1 knockout',BAD),blob(2,-.6,6.5,4.2,ASTRO,'glial cell'))
        # Recognisable filled silhouette: body, head, two ears, nose, feet, tail.
        mouse=VGroup(Ellipse(width=2.5,height=1.45,stroke_width=0,fill_color=GREY,fill_opacity=1),
            Circle(radius=.58,stroke_width=0,fill_color=GREY,fill_opacity=1).shift(RIGHT*1.1+UP*.3),
            *[Circle(radius=.35,stroke_width=0,fill_color=GREY,fill_opacity=1).shift(RIGHT*x+UP*.9) for x in (.7,1.3)],
            Dot([1.7,.3,0],radius=.13,color=GREY),Dot([1.3,.47,0],radius=.055,color=BG),
            Line([-1.1,-.15,0],[-2.1,.3,0],color=GREY,stroke_width=8),
            *[Ellipse(width=.65,height=.23,stroke_width=0,fill_color=GREY,fill_opacity=1).shift(RIGHT*x+DOWN*.7) for x in (-.6,.6)])
        mouse.move_to([-3.8,-.6,0]); self.add(mouse,T('mouse',28,GREY).move_to([-3.8,-2.1,0]),
            T('Ken McCarthy’s laboratory',28,GREY).move_to([0,2.45,0]))
        c=solid_chip('Kir4.1',ASTRO,30).move_to([2,1.5,0]); self.add(c)
        self.at('laboratory deleted'); self.play(Create(cross([.7,1.5,0])),run_time=.5); self.finish()


class S21Ko2(SpokenScene):
    def construct(self):
        base,curves,labels=uptake_panel(); self.add(base,
            T('CA1 astrocytes • mice 15–20 days old',26,GREY).move_to([0,2.62,0]))
        self.at('In hippocampal slices')
        self.play(Create(curves[0]),FadeIn(labels[0]),run_time=1.0)
        self.at('took up potassium poorly')
        self.play(Create(curves[1]),FadeIn(labels[1]),run_time=1.15); self.finish()


class S22Predict(SpokenScene):
    def construct(self):
        self.add(prediction_two()); self.at('What else'); self.finish()


class S23Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction_two()); countdown(self)


class S24Reveal(SpokenScene):
    def construct(self):
        base,curves,labels=uptake_panel(True); self.add(base)
        self.at('Glutamate uptake'); self.play(Create(curves),FadeIn(labels),run_time=.8)
        self.at('does not mean')
        note=T('Kir4.1 does not carry glutamate',28).move_to([0,2.65,0])
        self.play(FadeIn(note),run_time=.4)
        self.at('Glutamate transport')
        # Preserve the clarification through the voltage explanation.
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not note],run_time=.25)
        note.move_to([0,-3.15,0])
        meter=voltage_meter(True)
        self.add(meter,meter_cell(),knockout_chip(-3,1.2),heading('Glutamate transport depends on voltage'))
        self.at('depends on'); self.play(Transform(meter,voltage_meter(False)),run_time=.75); self.finish()


class S25Reveal2(SpokenScene):
    def construct(self):
        meter=voltage_meter(False); knocked=knockout_chip(-3,1.2)
        self.add(meter_cell(),meter,knocked,heading('Kir4.1 helps hold voltage negative',ASTRO))
        self.at('And')
        self.play(FadeOut(knocked[1]),run_time=.5)
        self.at('helps hold'); self.play(Transform(meter,voltage_meter(True)),run_time=.7); self.finish()


class S26Limit(SpokenScene):
    def construct(self):
        initial=limits(False); self.add(initial)
        self.at('deletion began in development'); self.play(Indicate(initial[5],color=BAD),run_time=.45)
        self.at('also reached oligodendrocytes')
        full=limits(); self.play(initial[-2:].animate.shift(LEFT*3),FadeIn(full[-3:]),run_time=.6); self.finish()


class S27Limit2(SpokenScene):
    def construct(self):
        self.add(limits())
        self.at('cannot be pinned')
        self.play(FadeIn(T('Cannot be pinned on mature astrocytes alone',32).move_to([0,-3.15,0])),run_time=.5); self.finish()


class S28Takeaway(SpokenScene):
    def construct(self):
        self.add(heading('What the film showed'))
        rows=[]
        texts=['Glia sense the potassium that firing releases',
            'Spatial buffering spreads it through the network',
            'Pumps in astrocytes and neurons\ntake it back inside cells']
        colors=[ASTRO,ASTRO,PUMP]
        for y,s,c in zip((1.65,-.05,-1.95),texts,colors):
            border=RoundedRectangle(width=12,height=1.4,corner_radius=.15,color=c,stroke_width=2)
            border.move_to([0,y,0])
            if y==1.65:
                icon=VGroup(Ellipse(width=.65,height=.8,color=ASTRO),Line([-.4,.5,0],[.4,.5,0],color=KC)).move_to([-5.2,y,0])
            elif y==-.05:
                icon=VGroup(*[Ellipse(width=.36,height=.65,color=ASTRO).shift(RIGHT*x) for x in (-.4,0,.4)]).move_to([-5.2,y,0])
            else:
                icon=VGroup(Rectangle(width=.6,height=.65,color=PUMP),arr([0,.6,0],[0,-.6,0],PUMP)).move_to([-5.2,y,0])
            text=T(s,28,c).move_to([-4.35,y,0],aligned_edge=LEFT)
            rows.append(VGroup(border,icon,text))
        self.at('sense the potassium'); self.play(FadeIn(rows[0]),run_time=.45)
        self.at('They spread it'); self.play(FadeIn(rows[1]),run_time=.45)
        self.at('and pumps take'); self.play(FadeIn(rows[2]),run_time=.5); self.finish()


class S29End(EndCard):
    LINE='Glia sense and spread potassium; pumps take it back inside cells.'
    def construct(self):
        line=T('Glia sense and spread potassium;\npumps take it back inside cells.',38,font=TITLE_FONT)
        self.add(T('biochemistrypedia.com',26,TEAL).move_to([0,-1.7,0]))
        self.play(FadeIn(line),run_time=.6); self.finish()
