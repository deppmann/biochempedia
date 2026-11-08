"""Reporters of Change — reviewed chapter 1.
COLOR MAP: INDIGO #9B8CF2 capsule; TEAL #3FB8C0 lamellar cells;
YELLOW #F5D547 nerve endings/spikes; GREEN #83C167 graded response;
ORANGE #F29E4C mechanical stimulus; GREY axes; TEXT labels.
All response traces are calculated: event rasters from thresholded positive
changes of a step input (release is the explicitly typical example); vibration
spikes from sine peaks with one deterministic skipped cycle; adaptation from
 dy/dt = dx/dt - y/tau. Species curves are illustrative log-Gaussians at the
narrated peak data, not experimental fits. No molecular structures.
"""
import numpy as np
from bp_style import *
ORANGE = '#F29E4C'
INDIGO = '#9B8CF2'
LIGHT = '#C4CAD5'


def label(s, x=0, y=3.15, size=30, color=TEXT):
    return T(s, size=size, color=color, line_spacing=.8).move_to([x,y,0])


def poly(points, color=ORANGE, sw=4):
    return VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners([np.array([x,y,0]) for x,y in points])


def leader(text, x, y, target, color=TEXT, size=28):
    t=label(text,x,y,size,color)
    start=t.get_left() if target[0]<x else t.get_right()
    ln=Line(start, target, buff=.12, color=color, stroke_width=3)
    return VGroup(ln,t)


def corpuscle(cut=False):
    # Anatomical lamellae, not molecular rings. A wedge exposes the inner core.
    outer=VGroup()
    for i in range(5):
        w,h=4.1-.38*i,3.7-.34*i
        if cut:
            angles=np.linspace(.52,2*PI-.52,180)
            outer.add(poly([(w/2*np.cos(a),h/2*np.sin(a)) for a in angles],INDIGO,3))
        else:
            outer.add(Ellipse(width=w,height=h,color=INDIGO,fill_color=INDIGO,fill_opacity=.035))
    inner=VGroup(*[Ellipse(width=w,height=h,color=TEAL,fill_color=TEAL,fill_opacity=.1) for w,h in [(2.05,1.65),(1.5,1.15)]])
    axon=Line([-2.65,0,0],[-.5,0,0],color=YELLOW,stroke_width=7)
    term=RoundedRectangle(width=1.25,height=.52,corner_radius=.24,color=YELLOW,fill_color=BG,fill_opacity=1,stroke_width=4)
    g=VGroup(outer,inner,axon,term)
    g.outer,g.inner,g.axon,g.term=outer,inner,axon,term
    return g


def meissner():
    cells=VGroup(*[Ellipse(width=1.6,height=.37,color=TEAL,fill_color=TEAL,fill_opacity=.18).move_to([0,y,0]) for y in [-.8,-.27,.27,.8]])
    # Cross the gaps horizontally; all vertical runs clear the disc edges.
    nerve=poly([(-1.1,-1.15),(.98,-1.15),(.98,-.535),(-.98,-.535),(-.98,0),(.98,0),(.98,.535),(-.98,.535),(-.98,1.12),(.3,1.12)],YELLOW,5)
    return VGroup(cells,nerve)


def finger(w=3.4,h=1.3):
    return RoundedRectangle(width=w,height=h,corner_radius=min(.55,h/2-.02),color=ORANGE,fill_color=ORANGE,fill_opacity=.16,stroke_width=4)


def vibration_arcs(x,y,scale=1):
    return VGroup(*[Arc(radius=r*scale,start_angle=-.8,angle=1.6,color=ORANGE,stroke_width=3).move_arc_center_to([x,y,0]) for r in [.65,.95]],*[Arc(radius=r*scale,start_angle=PI-.8,angle=1.6,color=ORANGE,stroke_width=3).move_arc_center_to([x,y,0]) for r in [.65,.95]])


def probe_skin(x=-4.9,y=2.45,scale=.55,pressed=False):
    # One continuous deforming skin surface; dimple follows probe indentation.
    depth=.4 if pressed else 0
    skin=poly([(x+scale*u,y+scale*v) for u,v in [(-1.5,0),(-.65,0),(-.38,-depth),(.38,-depth),(.65,0),(1.5,0)]],LIGHT,4)
    probe=RoundedRectangle(width=.8*scale,height=1.2*scale,corner_radius=.12*scale,color=ORANGE,fill_color=ORANGE,fill_opacity=.25).move_to([x,y+scale*(.6-depth),0])
    block=poly([(x-1.5*scale,y),(x-1.5*scale,y-.65*scale),(x+1.5*scale,y-.65*scale),(x+1.5*scale,y)],LIGHT,2)
    return VGroup(block,skin,probe)


X0,X1,ON,OFF=-2.5,6.1,-1.8,4.4
RY,SY=.75,-1.65

def ticks(xs,y,height=.95,color=YELLOW):
    return VGroup(*[Line([x,y,0],[x,y+height,0],color=color,stroke_width=3) for x in xs])


def burst_times(t0):
    # Integrate a decaying firing rate r(t)=24 exp(-t/.32).
    # One tick per unit of integrated rate, half-event phase at the edge.
    tau=.32
    counts=np.arange(7)+.5
    return t0-tau*np.log(1-counts/(24*tau))


def sa_times():
    return np.arange(ON+.08,OFF,.37)


def row_name(upper=True):
    return label('Meissner or\nPacinian fibre' if upper else 'slowly adapting\nfibre',-4.65,RY+.35 if upper else SY+.25,28,YELLOW)


def typical_label():
    # Attach the qualifier to the upper row, with a small gap below its name.
    return label('typical example',-4.65,.46,22,YELLOW)


def hold_shade():
    return Rectangle(width=OFF-ON,height=3.75,stroke_width=0,fill_color=BLUE,fill_opacity=.09).move_to([(ON+OFF)/2,-.05,0]).set_z_index(-2)


def raster(sa=False,ra=False,names=False,typical=False,dim_sa=False):
    g=VGroup(label('Press → hold → lift',1.2,3.2,34),probe_skin(),
       Line([X0,RY,0],[X1,RY,0],color=GREY),
       Line([X0,SY,0],[X1,SY,0],color=GREY),
       poly([(X0,-3),(ON,-3),(ON,-2.35),(OFF,-2.35),(OFF,-3),(X1,-3)]),
       label('skin\nindentation',-4.65,-2.7,28,ORANGE),label('time →',5.3,-3.45,28,LIGHT))
    if names:g.add(row_name())
    if typical:g.add(typical_label())
    if sa:
        lower=VGroup(row_name(False),ticks(sa_times(),SY))
        if dim_sa:lower.set_opacity(.23)
        g.add(lower)
    if ra:g.add(ticks(burst_times(ON),RY),ticks(burst_times(OFF),RY))
    return g


def questions():
    return VGroup(label('During the hold?',1.0,2.35,30),label('At the lift?',4.8,2.35,30))


def release_note():
    return leader('Release burst:\ncommon, not required',3.8,-.13,[4.8,.95,0],LIGHT,28)


def answered():
    return VGroup(hold_shade(),raster(True,True,True,True))


class S00Title(TitleCard):
    TITLE='Reporters of Change'
    LESSON='Meissner and Pacinian Corpuscles: Flutter and Vibration'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',y=2.2,size=28,color=TEAL))
        self.play(FadeIn(label(self.TITLE,y=.5,size=50)),FadeIn(label('Meissner and Pacinian Corpuscles\nFlutter and Vibration',y=-1.2,size=28,color=LIGHT)),run_time=.7)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        cloth=VGroup(*[Line([-6.2,y,0],[-.9,y,0],color=GREY) for y in np.linspace(-1.5,-.4,6)],*[Line([x,-1.5,0],[x,-.4,0],color=GREY) for x in np.linspace(-6.2,-.9,15)])
        f=finger(4,2).move_to([-4.2,.6,0])
        self.add(cloth,f,label('Across cloth',-3.6,2.6,32))
        self.at('Slide a fingertip')
        self.play(f.animate.shift(RIGHT*.95),run_time=1.3)
        phone=RoundedRectangle(width=2.1,height=3.9,corner_radius=.25,color=LIGHT,fill_color=GREY,fill_opacity=.12).move_to([3,.3,0])
        screen=RoundedRectangle(width=1.7,height=2.65,corner_radius=.12,color=GREY).move_to([3,.65,0])
        grip=finger(.8,2.5).move_to([4.45,-.3,0])
        arcs=VGroup(*[Arc(radius=r,start_angle=-.65,angle=1.3,color=ORANGE,stroke_width=3).move_arc_center_to([3,.3,0]) for r in [2.15,2.5]],*[Arc(radius=r,start_angle=PI-.65,angle=1.3,color=ORANGE,stroke_width=3).move_arc_center_to([3,.3,0]) for r in [1.5,1.85]])
        self.at('hold a buzzing')
        self.play(FadeIn(VGroup(phone,screen,grip,arcs)),FadeIn(label('Buzzing phone',3.1,3.05,32)),run_time=.4)
        self.play(Wiggle(VGroup(phone,screen,grip),scale_value=1.035,rotation_angle=.05),Indicate(arcs),run_time=.9)
        self.at('Two kinds')
        self.play(Indicate(f,color=ORANGE),Indicate(phone,color=ORANGE),run_time=.6)
        self.at('What are they')
        self.play(FadeIn(label('What are they reporting?',y=-2.9,size=40)),run_time=.5)
        self.finish()


class S02Names(SpokenScene):
    def construct(self):
        a=meissner().scale(1.8).move_to([-3.5,.15,0]); b=corpuscle().scale(1.17).move_to([3,.05,0])
        b.outer.set_fill(opacity=0).set_stroke(opacity=.22)
        self.add(a,b)
        self.at('They are the')
        self.play(FadeIn(label('Meissner',-3.5,3.2,34)),run_time=.4)
        self.at('and')
        self.play(FadeIn(label('Pacinian',3,3.2,34)),run_time=.4)
        self.at('nerve ending')
        self.play(Indicate(a[1]),Indicate(b.term),FadeIn(leader('nerve ending',-5.0,2.45,a[1].get_end(),YELLOW)),FadeIn(leader('nerve ending',3.8,-2.55,b.term.get_bottom(),YELLOW)),run_time=.6)
        self.at('the cells that')
        self.play(Indicate(a[0]),Indicate(b.inner),FadeIn(leader('lamellar cells',-3.5,-2.55,a[0][0].get_bottom(),TEAL)),FadeIn(leader('lamellar cells',3,2.45,[3.85,.65,0],TEAL)),run_time=.6)
        self.finish()


class S03Press(SpokenScene):
    def construct(self):
        p=probe_skin(-3.5,.85,1.65)
        self.add(label('Press, hold, then lift',y=3.25,size=36),p,
          Line([.15,.75,0],[6.1,.75,0],color=GREY),Line([.15,-.7,0],[6.1,-.7,0],color=GREY),
          label('spike rows',3.1,1.65,28,LIGHT),label('skin indentation',0,-3.4,28,ORANGE),label('time →',5.1,-3.4,28,LIGHT))
        self.at('Push a probe')
        self.play(Transform(p,probe_skin(-3.5,.85,1.65,True)),Create(poly([(-5.9,-2.7),(-3.6,-2.7),(-3.6,-1.8)])),run_time=.8)
        self.at('hold it still')
        self.play(Create(poly([(-3.6,-1.8),(3.5,-1.8)])),run_time=.65)
        self.at('then lift it')
        self.play(Transform(p,probe_skin(-3.5,.85,1.65)),Create(poly([(3.5,-1.8),(3.5,-2.7),(6,-2.7)])),run_time=.65)
        self.finish()


class S04Sa(SpokenScene):
    def construct(self):
        self.add(raster())
        self.at('called slowly adapting')
        self.play(FadeIn(row_name(False)),run_time=.45)
        self.at('keeps firing')
        self.play(Create(ticks(sa_times(),SY)),run_time=1.2)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        self.add(raster(True))
        self.at('Predict')
        self.play(FadeIn(row_name()),run_time=.4)
        q=questions()
        self.at('while the press')
        self.play(FadeIn(q[0]),run_time=.45)
        self.at('And when the probe')
        self.play(FadeIn(q[1]),run_time=.45)
        self.finish()


class S06Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        g=raster(True,names=True);g[0].become(label('Pause and predict',1.2,3.2,34,TEAL))
        self.add(g,questions())
        self.wait(5)


class S07Reveal(SpokenScene):
    def construct(self):
        self.add(raster(True,names=True))
        self.at('Typically')
        self.play(FadeIn(typical_label()),run_time=.3)
        self.at('fires a burst')
        self.play(Create(ticks(burst_times(ON),RY)),run_time=.6)
        self.at('goes quiet')
        self.play(FadeIn(hold_shade()),FadeIn(label('Quiet during the hold',1.35,2.35,30,LIGHT)),run_time=.5)
        self.at('fires again')
        self.play(Create(ticks(burst_times(OFF),RY)),run_time=.6)
        self.finish()


class S08Name(SpokenScene):
    def construct(self):
        g=answered();self.add(g)
        self.at('That is rapidly')
        self.play(Transform(g[1][0],label('Rapidly adapting',1.2,3.2,36)),run_time=.5)
        self.at('The firing dies')
        self.play(FadeIn(label('Firing dies away during the hold',1.7,2.35,30,LIGHT)),run_time=.5)
        self.at('common not required')
        self.play(FadeIn(release_note()),run_time=.5)
        self.finish()


class S09Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        g=raster(True,False,True,True,True);g[0].become(label('Rapidly adapting: replay',1.2,3.2,34))
        self.add(hold_shade(),g)
        scan=Line([ON,-3.05,0],[ON,1.85,0],color=ORANGE,stroke_width=2)
        self.add(scan,ticks(burst_times(ON),RY))
        self.play(scan.animate.set_x(OFF),run_time=1.5,rate_func=linear)
        self.play(Create(ticks(burst_times(OFF),RY)),run_time=.5)
        self.play(FadeOut(scan),run_time=.3)
        self.wait(.7)


def action_panel(x,y,name,kind):
    box=RoundedRectangle(width=5.8,height=2.55,corner_radius=.15,color=GREY,stroke_width=2).move_to([x,y,0])
    skin=Rectangle(width=4.6,height=.3,color=LIGHT,stroke_width=2,fill_color=LIGHT,fill_opacity=.08).move_to([x,y-.2,0])
    f=finger(2.5,.65).move_to([x,y+.28,0])
    row=Line([x-2.3,y-.9,0],[x+2.3,y-.9,0],color=GREY)
    # Sliding over texture gives three separated transient bursts.
    slide_events=np.concatenate([x+offset+.85*burst_times(0) for offset in [-1.95,-.55,1.05]])
    events=[] if kind=='steady' else (slide_events if kind=='slide' else x-.45+1.65*burst_times(0))
    spikes=ticks(events,y-.9,.55)
    title=label(name,x,y+1.0,28,LIGHT)
    return VGroup(box,skin,f,row,spikes,title)


class S10Idea(SpokenScene):
    def construct(self):
        self.add(label('Reports change, not level',y=3.25,size=36))
        panels=[action_panel(-3.1,1.15,'press begins','begin'),action_panel(3.1,1.15,'press ends','end'),action_panel(-3.1,-1.7,'finger slides','slide'),action_panel(3.1,-1.7,'level: silent','steady')]
        for p in panels:p[4].set_opacity(.12)
        self.add(*panels)
        self.at('report change')
        self.play(panels[3][0].animate.set_color(LIGHT),Indicate(panels[3][3],color=LIGHT),run_time=.55)
        # Each case is bright only during its own spoken phrase.
        for panel,phrase,end_phrase,tail,motion in [
            (panels[0],'starts to move','move',.30,DOWN*.14),
            (panels[1],'stops','stops',.22,UP*.17),
            (panels[2],'keeps moving','moving',.32,RIGHT*.65),
        ]:
            self.at(phrase,lead=0)
            panel[0].set_color(ORANGE)
            panel[5].set_color(ORANGE)
            panel[4].set_opacity(1)
            self.play(panel[2].animate.shift(motion),run_time=.2)
            self.wait(max(.01,self.t_of(end_phrase)+tail-self.elapsed()))
            panel[0].set_color(GREY)
            panel[5].set_color(LIGHT)
            panel[4].set_opacity(.12)
        self.finish()


class S11Vib(SpokenScene):
    def construct(self):
        self.add(label('Meissner or Pacinian fibre (schematic)',y=3.2,size=32),label('schematic phase locking',y=2.5,size=28,color=LIGHT),
          Line([-5.8,1,0],[5.8,1,0],color=GREY),label('skin vibration',-4.2,-3.35,28,ORANGE),label('time →',5.1,-3.35,28,LIGHT))
        # A single shared phase drives the waveform sweep and the event raster.
        n=6; a,b=-5.8,5.8
        points=[(x,-1.35+1.15*np.sin(2*PI*n*(x-a)/(b-a))) for x in np.linspace(a,b,601)]
        peaks=[a+(k+.25)*(b-a)/n for k in range(n)]
        wave=poly(points)
        self.at('Vibration is change')
        duration=max(1.8,self.t_of('So it drives')-self.elapsed()-.2)
        spikes=ticks([p for k,p in enumerate(peaks) if k!=3],1,1.0)
        event_positions=[p for k,p in enumerate(peaks) if k!=3]
        def reveal(mob,alpha):
            for tick,p in zip(mob,event_positions):
                tick.set_opacity(1 if alpha >= (p-a)/(b-a) else 0)
        spikes.set_opacity(0);self.add(spikes)
        self.play(Create(wave,rate_func=linear),UpdateFromAlphaFunc(spikes,reveal,rate_func=linear),run_time=duration)
        self.at('So it drives')
        self.play(Indicate(spikes,color=YELLOW),run_time=.5)
        self.finish()


class S12Talbot(SpokenScene):
    def construct(self):
        f=finger(4.2,2.5).rotate(PI/2).move_to([-2,1.05,0])
        # The bottom of this fingertip contacts the probe's top.
        p=RoundedRectangle(width=1.4,height=1.7,corner_radius=.16,color=ORANGE,fill_color=ORANGE,fill_opacity=.25).move_to([-2,-1.9,0])
        arcs=vibration_arcs(-2,-1.05,1.75)
        self.add(f,p,label('Fingertip on a vibrating probe',y=3.55,size=32))
        self.at('In')
        self.play(FadeIn(label('Talbot and colleagues\n1968',3,1.4,32)),FadeIn(label('human volunteers',3,.2,30,LIGHT)),run_time=.5)
        self.at('vibrated')
        self.play(FadeIn(arcs),Wiggle(p,scale_value=1.04,rotation_angle=.055),run_time=1)
        self.finish()


def dial(hum=False,flutter=True):
    # Linear frequency scale gives the 60–80 transition enough label space.
    def px(f):return -5.8+11.6*f/200
    g=VGroup(label('Human volunteers: perceived vibration',y=3.15,size=34),Line([-5.8,-1.35,0],[5.8,-1.35,0],color=LIGHT))
    for f in [5,40,60,80,200]:
        x=px(f); ty=-1.95 if f!=60 else -2.55
        g.add(Line([x,-1.2,0],[x,-1.55,0],color=LIGHT),label(str(f),x,ty,28,LIGHT))
    g.add(label('frequency (Hz) →',3.5,-2.8,28,LIGHT))
    if flutter:
        band=RoundedRectangle(width=px(40)-px(5),height=.9,corner_radius=.15,stroke_width=0,fill_color=ORANGE,fill_opacity=.32).move_to([(px(5)+px(40))/2,.2,0])
        g.add(band,label('flutter',(px(5)+px(40))/2,.2,28,ORANGE),label('about 5 to 40 Hz',-3.35,1.85,32,ORANGE))
    if hum:
        fade=VGroup(*[Rectangle(width=(px(80)-px(60))/24+.008,height=.9,stroke_width=0,fill_color=ORANGE,fill_opacity=.35*(i+1)/24).move_to([px(60)+(i+.5)*(px(80)-px(60))/24,.2,0]) for i in range(24)])
        band=Rectangle(width=px(200)-px(80),height=.9,stroke_width=0,fill_color=ORANGE,fill_opacity=.35).move_to([(px(80)+px(200))/2,.2,0])
        g.add(fade,band,label('hum',px(140),.2,34,ORANGE),label('from around 60 to 80 Hz upward',0,2.15,30,ORANGE))
    return g,px


class S13Flutter(SpokenScene):
    def construct(self):
        base,px=dial(flutter=False);self.add(base)
        pointer=Triangle(color=ORANGE,fill_color=ORANGE,fill_opacity=1).scale(.2).rotate(PI).move_to([px(5),1.05,0])
        self.at('From about')
        self.add(pointer)
        self.play(pointer.animate.set_x(px(40)),run_time=1.6)
        full,_=dial()
        self.at('light flutter')
        self.play(FadeOut(pointer),FadeIn(full[-3:]),run_time=.4)
        self.wait(1.8)
        self.finish()


class S14Hum(SpokenScene):
    def construct(self):
        d,px=dial();self.add(d)
        pointer=Triangle(color=ORANGE,fill_color=ORANGE,fill_opacity=1).scale(.2).rotate(PI).move_to([px(60),1.05,0])
        self.at('From around')
        # Clear the first range's annotation before displaying the second range.
        self.play(FadeOut(d[-1]),FadeIn(pointer),run_time=.2)
        self.play(pointer.animate.set_x(px(100)),run_time=1.5)
        full,_=dial(True)
        self.at('deeper hum')
        self.play(FadeOut(pointer),FadeIn(full[-4:]),run_time=.4)
        self.wait(1.8)
        self.finish()


class S15Monkey(SpokenScene):
    def construct(self):
        self.add(label('Talbot and colleagues · 1968',y=3.25,size=34),label('Human perception',-4.4,2.3,30,LIGHT),label('flutter',-4.4,.55,34,ORANGE),label('hum',-4.4,-1.65,34,ORANGE))
        panel=RoundedRectangle(width=8.1,height=5.55,corner_radius=.2,color=GREY).move_to([2,-.3,0])
        heading=label('anaesthetized rhesus monkey:\nsingle-fibre recordings',2,1.95,30,LIGHT)
        separate=label('Separate preparation',2,.9,28,LIGHT)
        self.at('The same study')
        self.play(Create(panel),FadeIn(heading),FadeIn(separate),run_time=.7)
        self.at('single fibers in monkeys')
        self.play(Indicate(heading,color=LIGHT),run_time=.5)
        self.at('Flutter matched')
        a=meissner().scale(.49).move_to([.7,-.15,0])
        self.play(GrowArrow(Arrow([-3.2,.55,0],[-.25,-.15,0],buff=.1,color=LIGHT)),FadeIn(a),FadeIn(label('Meissner-type\nfibres',3.7,-.1,30,YELLOW)),run_time=.6)
        self.at('The hum matched')
        b=corpuscle().scale(.36).move_to([.7,-1.65,0])
        self.play(GrowArrow(Arrow([-3.2,-1.65,0],[-.35,-1.65,0],buff=.1,color=LIGHT)),FadeIn(b),FadeIn(label('Pacinian fibres',3.7,-1.65,30,YELLOW)),run_time=.6)
        self.finish()


class S16Species(SpokenScene):
    def construct(self):
        self.add(label('Frequency preference depends on species',y=3.3,size=32))
        def xx(f):return -5.25+11.05*np.log10(f/30)/np.log10(10000/30)
        def curve(peak,col):return poly([(xx(f),-2.0+3.95*np.exp(-.5*(np.log(f/peak)/.43)**2)) for f in np.geomspace(30,10000,600)],col)
        self.add(Line([-5.25,-2,0],[5.8,-2,0],color=LIGHT),Line([-5.25,-2,0],[-5.25,2.3,0],color=LIGHT),label('relative sensitivity',-6.15,.15,28,LIGHT).rotate(PI/2),label('frequency (Hz; log scale)',0,-2.95,28,LIGHT),label('Prsa et al., 2021 · curve shapes illustrative',0,-3.55,28,LIGHT))
        for f in [100,1000,10000]:
            x=xx(f);self.add(Line([x,-2,0],[x,-2.15,0],color=LIGHT),label(str(f),x,-2.48,28,LIGHT))
        self.at('The best frequency')
        self.wait(.25)
        self.at('sensitivity peaked near')
        self.play(Create(curve(240,TEXT)),FadeIn(label('human fingertip · 240 Hz',-2.5,2.55,28)),run_time=.9)
        self.at('and near')
        self.play(Create(curve(1000,TEAL)),FadeIn(label('mouse forepaw · 1000 Hz',2.7,2.55,28,TEAL)),run_time=.8)
        self.finish()


class S17Idea2(SpokenScene):
    def construct(self):
        self.add(label('Same push size; different speed',y=3.35,size=34),label('illustrative model · no hard cut-off',y=-3.45,size=28,color=LIGHT))
        # Two decay rates, tau 1.6 and .6, with a shared linear response scale.
        t=np.linspace(0,5,601)
        def xx(t,x):return x+4.65*t/5
        def resp(t,tau,ramp):
            if ramp:
                return np.where(t<.5,0,np.where(t<=2.5,tau/2*(1-np.exp(-np.maximum(t-.5,0)/tau)),tau/2*(1-np.exp(-2/tau))*np.exp(-np.maximum(t-2.5,0)/tau)))
            return np.where(t<.5,0,np.exp(-np.maximum(t-.5,0)/tau))
        pushes=VGroup();responses=VGroup()
        for x,name,ramp in [(-4.4,'slow ramp',True),(1.4,'sudden push',False)]:
            self.add(label(name,x+2.3,2.6,30,ORANGE))
            push=np.clip((t-.5)/2,0,1) if ramp else (t>=.5).astype(float)
            pushes.add(poly([(xx(tt,x),1.15+.9*vv) for tt,vv in zip(t,push)]))
            for base,tau in [(-.45,1.6),(-2.25,.6)]:
                self.add(Line([x,base,0],[x+4.65,base,0],color=GREY))
                responses.add(poly([(xx(tt,x),base+1.45*vv) for tt,vv in zip(t,resp(t,tau,ramp))],GREEN))
            self.add(label('time →',x+3.8,-2.8,28,LIGHT))
        self.add(label('push',-5.8,1.55,28,ORANGE),label('response\nslower\ndecay',-5.7,.05,28,GREEN),label('response\nfaster\ndecay',-5.7,-1.75,28,GREEN))
        self.at('Here is the idea')
        self.play(Create(pushes),run_time=.9)
        self.at('Compare pushes')
        self.play(Indicate(pushes,color=ORANGE),run_time=.5)
        self.at('The faster the response')
        self.play(Create(responses),run_time=1.1)
        self.at('discounts slow change')
        self.play(Indicate(responses[1],color=GREEN),Indicate(responses[0],color=GREEN),run_time=.7)
        self.finish()


class S18Three(SpokenScene):
    def construct(self):
        c=corpuscle(cut=True).scale(1.65).move_to([-1.95,0,0])
        # Channel cartoons straddle the terminal membrane; their centres follow it.
        top=c.term.get_top()[1]
        ch=VGroup(*[RoundedRectangle(width=.22,height=.5,corner_radius=.035,color=GREEN,fill_color=GREEN,fill_opacity=.5).move_to([c.term.get_center()[0]+dx,top,0]) for dx in [-.45,.45]])
        gen=RoundedRectangle(width=.65,height=.62,corner_radius=.12,color=YELLOW,fill_color=YELLOW,fill_opacity=.3).move_to([c.term.get_left()[0]+.4,-.1,0])
        self.add(c)
        self.at('That dying away')
        self.play(FadeIn(label('Three possible sites of dying-away',y=3.5,size=32)),run_time=.5)
        self.at('capsule')
        self.play(Indicate(c.outer,color=INDIGO),FadeIn(leader('capsule',4.5,2.1,[.4,2.1,0],INDIGO,30)),run_time=.5)
        self.at('the endings channels')
        self.play(FadeIn(ch),FadeIn(leader('terminal channels',4.7,.55,ch.get_right(),GREEN,28)),run_time=.5)
        self.at('the spike generator')
        self.play(FadeIn(gen),FadeIn(leader('spike generator',2.4,-1.15,gen.get_bottom(),YELLOW,28)),run_time=.5)
        self.finish()


class S19Take(SpokenScene):
    def construct(self):
        # Dedicated result: upper raster enlarged; comparison recedes.
        self.add(label('Meissner or Pacinian fibre',y=2.6,size=32,color=YELLOW),Line([-5.9,.15,0],[5.9,.15,0],color=GREY),ticks(-5.2+2.3*burst_times(0),.15,1.65),ticks(3.8+2.3*burst_times(0),.15,1.65),label('burst',-4.5,-.4,30,YELLOW),label('silence during hold',0,-.4,30,LIGHT),label('burst',4.5,-.4,30,YELLOW))
        sa=VGroup(Line([-5.9,-1.8,0],[5.9,-1.8,0],color=GREY),ticks(np.arange(-5.2,5.2,.55),-1.8,.65),label('slowly adapting comparison',0,-2.5,28,LIGHT)).set_opacity(.22)
        self.add(sa)
        self.at('Keep this')
        title=label('Keep this',y=3.5,size=32,color=LIGHT)
        self.play(FadeIn(title),run_time=.35)
        self.at('These corpuscles report')
        self.play(Transform(title,label('Reports change',y=3.5,size=38)),run_time=.5)
        self.finish()


class S20End(EndCard):
    LINE='These corpuscles report change, not level.'
