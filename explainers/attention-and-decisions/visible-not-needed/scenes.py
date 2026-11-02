"""Visible Is Not the Same as Needed — chapter 3.

COLOR MAP (shared across chapters): YELLOW = motion evidence; BLUE = MT;
PINK = LIP firing; GOLD = bound / model annotations; GREEN = choices / eyes;
PURPLE = manipulation; RED = impairment; GREY = structure / control.

Ramps: r(t)=min(70,30+s*max(0,t-.2)), s=400,100,25 spikes/s/s.
Psychometrics: P(right)=1/(1+exp(-2*mu*40/(8000/log(9)))),
mu=7.8125*(gain*c+shift). Illustrative stimulation shift=8; silenced
MT gain=.24. LIP intervention overlaps control. These are qualitative
model illustrations, not experimental fits. Bars and landing points are
schematic, without numerical effect estimates. Spike symbols are event
glyphs from a constant-rate 30 spikes/s teaching model (r=0 when silent),
not measured recordings; no invented continuous neural traces.
"""
import numpy as np
from bp_style import *

PINK = '#E58AC0'
PURPLE = '#B58CD9'


def poly(pts, color, w=5):
    return VMobject().set_points_as_corners([np.array([x, y, 0.]) for x, y in pts]).set_stroke(color, w).set_fill(opacity=0)


def label(s, x, y, size=28, color=TEXT):
    return T(s, size, color).move_to([x, y, 0])


def head(s, color=TEXT):
    return label(s, 0, 3.35, 34, color)


def neuron(c, color, s=1):
    c = np.array([*c, 0.])
    g = VGroup(Circle(radius=.32*s, color=color, fill_opacity=.3).move_to(c))
    for a in (110, 160, 210, 250):
        d = np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])
        g.add(Line(c+d*.32*s, c+d*.85*s, color=color, stroke_width=4))
    g.add(Line(c+RIGHT*.32*s, c+RIGHT*s, color=color, stroke_width=4))
    return g


def axes(x0, x1, y0, y1):
    return VGroup(Line([x0,y0,0], [x1,y0,0], color=GREY), Line([x0,y0,0], [x0,y1,0], color=GREY))


def electrode(x=0, tip=-.4, top=2.5):
    return VGroup(Line([x,top,0], [x,tip+.3,0], color=GREY, stroke_width=7),
                  Polygon([x-.09,tip+.3,0], [x+.09,tip+.3,0], [x,tip,0], color=TEXT, fill_opacity=1))


def spikes(x0, x1, y, color=PINK):
    # Six events from a constant-rate teaching model over 0.2 seconds.
    rate=30.0
    event_times=np.arange(int(rate*.2))/rate
    xs=x0+.2+(x1-x0-.4)*event_times/event_times[-1]
    return VGroup(Line([x0,y,0], [x1,y,0], color=GREY),
        *[Line([x,y,0], [x,y+.55,0], color=color, stroke_width=4) for x in xs])


def syringe(x=0, y=1.1):
    return VGroup(Rectangle(width=.65,height=1.15,color=PURPLE,fill_opacity=.18).move_to([x,y,0]),
        Line([x,y+.58,0],[x,y+1.1,0],color=TEXT,stroke_width=5),
        Line([x-.5,y+1.1,0],[x+.5,y+1.1,0],color=TEXT,stroke_width=5),
        Line([x-.55,y+.45,0],[x+.55,y+.45,0],color=PURPLE,stroke_width=5),
        Line([x,y-.58,0],[x,y-1.4,0],color=TEXT,stroke_width=3),
        *[Line([x-.3,y+d,0],[x-.08,y+d,0],color=PURPLE) for d in (-.25,0,.25)])


def brain():
    # Orientation and regions are explicitly schematic, not atlas coordinates.
    outline=Ellipse(width=11.3,height=5.65,color=GREY,stroke_width=4).move_to([0,-.05,0])
    stem=poly([(2.8,-2.3),(3.05,-2.65),(3.3,-2.85)],GREY,12)
    return VGroup(outline,stem,label('front',-5.6,2.5,26),label('back',5.6,2.5,26),
        label('rhesus monkey brain · schematic map',0,-3.4,26,GOLD))


def question():
    cards=VGroup()
    for x,s,c in [(-3.25,'Silence MT',BLUE),(3.25,'Silence LIP',PINK)]:
        box=RoundedRectangle(width=5.5,height=4.1,corner_radius=.2,color=c,fill_opacity=.07).move_to([x,0,0])
        cards.add(VGroup(box,label(s,x,1,38,c),label('?',x,-.7,80,GOLD)))
    return VGroup(head('If LIP is the accumulator…',PINK),*cards)


def psych(x0=-4.8,x1=5.7,y0=-2.2,y1=2.5,gain=1,shift=0,color=GREEN,dashed=False):
    c=np.linspace(-32,32,240)
    mu=7.8125*(gain*c+shift)
    p=1/(1+np.exp(-2*mu*40/(8000/np.log(9))))
    curve=poly([(x0+(x1-x0)*(cc+32)/64,y0+(y1-y0)*v) for cc,v in zip(c,p)],color,6)
    return DashedVMobject(curve,num_dashes=30) if dashed else curve


def psych_frame(x0=-4.8,x1=5.7,y0=-2.2,y1=2.5):
    return VGroup(axes(x0,x1,y0,y1),
        label('rightward choices',x0-1.05,(y0+y1)/2,26,TEXT).rotate(PI/2),
        label('0%',x0-.42,y0,26,GREY),label('100%',x0-.65,y1,26,GREY),
        label('motion strength →',(x0+x1)/2,-2.7,26),
        Line([x0,y0,0],[x0-.1,y0,0],color=GREY),Line([x0,y1,0],[x0-.1,y1,0],color=GREY))


LEFT_PLOT=(-5.35,-.6,-2.15,2.55)
RIGHT_PLOT=(1.5,6.25,-2.15,2.55)


def split_base(right=False):
    g=VGroup(label('MT silenced',-3,3.35,34,BLUE),
        psych_frame(*LEFT_PLOT),label('grey = control',0,-3.13,26,GREY),
        label('qualitative model illustration · not recorded data',0,-3.62,26,GOLD))
    if right:
        g.add(label('LIP silenced',3.8,3.35,34,PINK),psych_frame(*RIGHT_PLOT))
    return g


def mt_result():
    return VGroup(psych(*LEFT_PLOT,color=GREY),psych(*LEFT_PLOT,gain=.24,color=RED),
                  label('impaired',-3.7,2.15,30,RED))


def free_targets():
    return VGroup(head('Free choice: pick either'),
        Circle(radius=1.45,color=GREEN,stroke_width=6).move_to([-3.4,0,0]),
        Circle(radius=1.45,color=GREEN,stroke_width=6).move_to([3.4,0,0]),
        label('+',0,0,48),label('fixation',0,-.7,26,GREY),label('no right answer',0,-2.7,34))


class S00Title(TitleCard):
    LESSON='Attention, Executive Control and Decisions'
    TITLE='Visible Is Not the Same as Needed'

    def construct(self):
        brand=label('BIOCHEMISTRYPEDIA',0,2.1,26,TEAL)
        lesson=label(self.LESSON.upper(),0,1.2,26,GREY)
        title=VGroup(T('Visible Is Not',48,font=TITLE_FONT),T('the Same as Needed',48,font=TITLE_FONT)).arrange(DOWN,buff=.25).move_to([0,-.35,0])
        self.play(FadeIn(brand),FadeIn(lesson),run_time=.35)
        self.play(FadeIn(title),Create(Line([-1.2,-2,0],[1.2,-2,0],color=GOLD,stroke_width=4)),run_time=.5)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        x0,x1,y0,y1=-4.65,5.7,-2.45,2.15
        def point(t,r):
            return (x0+(x1-x0)*t/2,y0+(r-25)/45*(y1-y0))
        ramps=VGroup()
        for slope in (400,100,25):
            t=np.linspace(0,.2+40/slope,160)
            r=np.minimum(70,30+slope*np.maximum(0,t-.2))
            ramps.add(poly([point(tt,rr) for tt,rr in zip(t,r)],PINK))
        bound_y=point(0,70)[1]
        self.at('L I P')
        self.add(axes(x0,x1,y0,y1),ramps,
            label('LIP firing (running total)',-6.05,-.15,28,PINK).rotate(PI/2),
            label('time',.6,-3,28),label('reference model',3.8,-3.5,26,GOLD),
            DashedLine([x0,bound_y,0],[x1,bound_y,0],color=GOLD),label('bound',5.1,2.55,28,GOLD))
        # Labels sit in separate gaps; short leaders touch only their named ramp.
        self.add(label('strong evidence',-3.25,2.65,26,PINK),
            Line([-3.1,2.4,0],[-3.1,2.15,0],color=PINK,stroke_width=2),
            label('medium',-.7,.9,26,PINK),label('evidence',-.7,.4,26,PINK),
            Line([-1.55,.8,0],[-2.23,.8,0],color=PINK,stroke_width=2),
            label('weak evidence',3.2,-.65,26,PINK),
            Line([3.2,-.35,0],[3.2,1.42,0],color=PINK,stroke_width=2))
        self.at('but does')
        self.play(FadeIn(head('Does the decision need LIP?')),run_time=.4)
        self.finish()


class S02Logic(SpokenScene):
    def construct(self):
        n=neuron((-4.35,-.75),PINK,2.8)
        e=electrode(-4.35,tip=-.2,top=2.25)
        trace=VGroup(spikes(-2.9,-.65,1.25),Line([-4.35,1.25,0],[-2.9,1.25,0],color=GREY),
                     label('schematic spikes',-2.1,.7,26,GREY))
        center=np.array([3.35,-.45,0])
        dial=Circle(radius=2,color=PURPLE,stroke_width=6).move_to(center)
        ticks=VGroup(*[Line(center+1.74*np.array([np.cos(a),np.sin(a),0]),
                          center+1.93*np.array([np.cos(a),np.sin(a),0]),color=PURPLE,stroke_width=3)
                      for a in np.linspace(0,TAU,12,endpoint=False)])
        pointer=Line(center,center+UP*1.55,color=PURPLE,stroke_width=7)
        # An outlined hand grips the knob, making the experimenter's action visible.
        hand=poly([(5.75,1.55),(4.8,1.55),(4.05,1.15),(3.45,1.1),
                   (3.25,1.25),(3.4,1.48),(4.0,1.65),(4.45,2.05),
                   (5.0,2.05),(5.75,2.45)],TEXT,5)
        turning=VGroup(pointer,hand)
        self.at('a recording')
        self.add(Line([0,-2.5,0],[0,2.5,0],color=GREY),n,e,
            label('recording',-3.5,3.05,34),dial,ticks,turning,
            label('experimenter',3.35,3.05,30))
        self.at('goes with')
        self.play(Create(trace),FadeIn(label('goes with',-3.4,-3.05,38)),run_time=.4)
        self.at('depends on')
        self.play(Rotate(turning,-PI/4,about_point=center),
                  FadeIn(label('depends on',3.35,-3.05,38)),run_time=.65)
        self.finish()


class S03MtStim(SpokenScene):
    def construct(self):
        centers=[(-3.3,-.05),(0,-.65),(3.3,-.05)]
        ns=VGroup(*[neuron(c,BLUE,3.3) for c in centers])
        arrows=VGroup(*[Arrow([x-.5,y,0],[x+.52,y,0],color=YELLOW,buff=0,stroke_width=5) for x,y in centers])
        self.at('MT')
        self.add(label('MT neurons',0,3.35,34,BLUE),ns,arrows)
        self.at('researchers passed')
        self.play(Create(electrode(0,tip=-.65,top=2.3)),run_time=.45)
        self.at('weak current')
        rings=VGroup(*[Circle(radius=r,color=PURPLE,stroke_width=4).move_to([x,y,0])
                       for x,y in centers for r in (1.12,1.4)])
        current=label('weak current',1.3,1.7,28,PURPLE)
        self.play(FadeIn(current),FadeIn(rings),run_time=.5)
        # Persistent rings remain legible in sampled frames; a pulse travels outward.
        self.at('small clusters')
        self.play(Indicate(rings,color=PURPLE,scale_factor=1.16),run_time=.7)
        self.at('shared a preferred')
        self.play(Indicate(arrows,color=YELLOW,scale_factor=1.12),FadeIn(label('shared preferred direction →',0,-3.6,32,YELLOW)),run_time=.5)
        self.finish()


class S04MtShift(SpokenScene):
    def construct(self):
        base=psych(color=GREY)
        self.at('the monkeys')
        self.add(psych_frame(),base,head('MT stimulation',PURPLE),
            label('no stimulation',3,.1,30,GREY),
            Line([3,.4,0],[3,-2.2+4.7/(1+np.exp(-2*(7.8125*(-32+64*(3+4.8)/10.5))*40/(8000/np.log(9)))),0],color=GREY,stroke_width=2),
            label('qualitative model illustration',0,-3.45,26,GOLD))
        self.at('chose that direction')
        shifted=psych(shift=8,color=GREEN)
        moving=base.copy().set_color(GREEN)
        self.add(moving)
        self.play(Transform(moving,shifted),FadeIn(VGroup(label('stimulated',-2.8,1.2,30,GREEN),Line([-2.1,.95,0],[-1.1,.03,0],color=GREEN,stroke_width=2))),run_time=.8)
        self.at('as if')
        self.play(FadeIn(VGroup(label('as if rightward motion',2.8,-1.15,28,YELLOW),label('were added',2.8,-1.7,28,YELLOW))),run_time=.4)
        self.finish()


class S05Katz(SpokenScene):
    def construct(self):
        mt=chip('MT',BLUE,46).move_to([2.8,-.8,0])
        lip=chip('LIP',PINK,46).move_to([1,1.4,0])
        self.at('cats')
        self.add(brain(),mt,lip,head('Katz, Yates, Pillow & Huk · 2016'))
        self.at('silenced each')
        sil_mt=chip('MT · silenced',PURPLE,38).move_to(mt)
        self.play(Transform(mt,sil_mt),run_time=.3)
        self.at('in rhesus monkeys')
        # Sequential states are held, not subsecond flashes. Reset MT as LIP changes.
        self.play(Transform(mt,chip('MT',BLUE,46).move_to([2.8,-.8,0])),
                  Transform(lip,chip('LIP · silenced',PURPLE,38).move_to([1,1.4,0])),run_time=.3)
        self.wait(1.7)
        self.finish()


class S06Drug(SpokenScene):
    def construct(self):
        ns=VGroup(*[neuron(c,PINK,1.9) for c in [(-3.1,-.6),(0,-1.1),(3.1,-.6)]])
        activity=spikes(-4.3,4.3,-2.8)
        self.at('they used')
        self.add(ns,syringe(0,1.45),activity)
        self.at('muscimol')
        self.play(FadeIn(label('muscimol',2.4,2.6,36,PURPLE)),run_time=.35)
        cloud=Ellipse(width=10.5,height=3.9,color=PURPLE,fill_opacity=.14,stroke_opacity=.65).move_to([0,-.55,0])
        self.at('a drug')
        self.play(GrowFromPoint(cloud,[0,.05,0]),run_time=.55)
        self.at('activates')
        self.play(FadeIn(label('GABA-A receptor agonist',0,-3.5,30,PURPLE)),run_time=.35)
        self.at('quiets nearby')
        flat=Line([-4.3,-2.8,0],[2.7,-2.8,0],color=GREY,stroke_width=4)
        self.play(ns.animate.set_color(GREY).set_opacity(.65),FadeOut(activity),FadeIn(flat),
                  FadeIn(label('silent',3.6,-2.8,30,GREY)),run_time=.6)
        self.finish()


class S07Question(SpokenScene):
    def construct(self):
        q=question()
        self.at('predict each')
        intro=label('Predict each outcome',0,2.95,34)
        self.add(intro,q[1][0],q[1][2],q[2][0],q[2][2])
        self.at('if L I P')
        self.play(ReplacementTransform(intro,q[0]),run_time=.4)
        self.at('what happens')
        self.play(FadeIn(q[1][1]),run_time=.5)
        self.at('and when')
        self.play(FadeIn(q[2][1]),run_time=.5)
        self.finish()


class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(question(),label('pause and predict',-.45,-2.85,30,TEAL))
        center=np.array([2.25,-2.85,0])
        self.add(Circle(radius=.35,color=GREY,stroke_width=4).move_to(center))
        timer=ValueTracker(1)
        arc=always_redraw(lambda: Arc(radius=.35,start_angle=PI/2,angle=TAU*max(.001,timer.get_value()),color=TEAL,stroke_width=7).shift(center))
        self.add(arc)
        self.play(timer.animate.set_value(0),run_time=5,rate_func=linear)


class S09RevealMt(SpokenScene):
    def construct(self):
        base=psych(*LEFT_PLOT,color=GREY)
        self.at('silencing')
        self.add(split_base(),base,base.copy())
        self.at('impaired motion')
        self.play(Transform(base,psych(*LEFT_PLOT,gain=.24,color=RED)),FadeIn(label('impaired',-3.7,2.15,30,RED)),run_time=.6)
        self.finish()


class S10RevealLip(SpokenScene):
    def construct(self):
        self.at('silencing')
        base=split_base(right=True)
        base[2].move_to([-3,-3.13,0])
        self.add(base,mt_result(),psych(*RIGHT_PLOT,color=GREY))
        self.at('no measurable')
        self.play(Create(psych(*RIGHT_PLOT,color=GREEN,dashed=True)),
            FadeIn(VGroup(label('no measurable',3.0,2.25,26,GREEN),label('change in',3.0,1.8,26,GREEN),label('these tasks',3.0,1.35,26,GREEN))),
            FadeIn(label('green dashed = silenced',3.8,-3.13,24,GREEN)),run_time=.6)
        self.finish()


class S11Miss(SpokenScene):
    def construct(self):
        ns=VGroup(*[neuron(c,PINK,1.9) for c in [(-2,-.3),(1.4,-1),(3.5,.4)]])
        site=VGroup(ns,syringe(-2,1.5),label('LIP injection site',1.6,2.1,36,PINK),label('?',-.1,.7,85,GOLD))
        self.at('did the')
        h=head('Did the injection miss?')
        self.add(h,site)
        self.at('the same monkeys')
        self.play(FadeOut(site),FadeOut(h),FadeIn(free_targets()),run_time=.65)
        self.finish()


class S12Control(SpokenScene):
    def construct(self):
        baseline=-2.0
        b0=Rectangle(width=1.5,height=3.9,color=GREEN,fill_opacity=.8).move_to([-.1,baseline+1.95,0])
        b1=Rectangle(width=1.5,height=1.65,color=GREEN,fill_opacity=.8).move_to([3.5,baseline+.825,0])
        targets=VGroup(Circle(radius=.55,color=GREEN).move_to([-5.4,.55,0]),Circle(radius=.55,color=PURPLE).move_to([-3.8,.55,0]),label('+',-4.6,.55,30),
            label('affected side',-4.6,-1.2,26,PURPLE),Arrow([-4.4,-.9,0],[-3.8,.05,0],color=PURPLE,buff=.08))
        self.at('after')
        self.add(head('Free-choice control'),axes(-1.45,5.3,baseline,2.25),
            label('choices into the affected side',-2.15,.1,26,GREEN).rotate(PI/2),targets,
            label('schematic relative heights',0,-3.45,26,GOLD))
        self.at('they chose')
        self.play(GrowFromEdge(b0,DOWN),GrowFromEdge(b1,DOWN),
            FadeIn(label('before',-.1,-2.55,28)),FadeIn(label('after LIP silencing',3.5,-2.55,28,PURPLE)),run_time=.55)
        self.at('less often')
        self.play(Indicate(b1,color=PURPLE,scale_factor=1.04),run_time=.55)
        self.finish()


class S13Landing(SpokenScene):
    def construct(self):
        targets=VGroup(*[VGroup(Circle(radius=1.5,color=GREY),Line([-1.7,0,0],[1.7,0,0],color=GREY),Line([0,-1.7,0],[0,1.7,0],color=GREY)).move_to([x,0,0]) for x in (-3.2,3.2)])
        offsets=np.random.RandomState(4).normal(size=(12,2))*.26
        dots=VGroup(*[Dot([-3.2+dx,dy,0],radius=.09,color=GREEN) for dx,dy in offsets])
        self.at('and their')
        self.add(head('Landing in the affected side of space'),targets,dots,
            label('before',-3.2,2.4,32),label('after LIP silencing',3.2,2.4,32,PURPLE),
            label('schematic target-relative points',0,-3.45,26,GOLD))
        self.at('landed less accurately')
        wide=VGroup(*[Dot([3.2+dx*3.5+.35,dy*3.5+.15,0],radius=.09,color=GREEN) for dx,dy in offsets])
        self.play(FadeIn(wide),FadeIn(label('increased endpoint error',3.2,-2.15,28,RED)),run_time=.6)
        self.at('so the drug')
        self.play(FadeIn(label('the drug acted',3.2,-2.8,32,PURPLE)),run_time=.4)
        self.finish()


class S14Readable(SpokenScene):
    def construct(self):
        a=chip('the control shows the drug acted',PURPLE,38).move_to([0,2.3,0])
        b=VGroup(label('no measurable deficit',0,-.35,40,GREEN),label('in these tasks',0,-1.1,36,GREEN))
        self.at('that control')
        self.add(a)
        self.at('the null result')
        self.play(GrowArrow(Arrow([0,1.65,0],[0,.3,0],color=PURPLE,buff=0)),
                  FadeIn(label('lets us read',2.1,1,32)),FadeIn(b),run_time=.5)
        self.at('cannot rule out')
        self.play(FadeIn(chip('compensation not excluded',GOLD,38).move_to([0,-2.65,0])),run_time=.5)
        self.finish()


class S15Others(SpokenScene):
    def construct(self):
        # Result icons, rather than invented experimental traces.
        control=Rectangle(width=.65,height=3.1,color=GREY,fill_opacity=.7).move_to([-4.8,0,0])
        impaired=Rectangle(width=.65,height=3.1,color=RED,fill_opacity=.8).move_to([-3.7,0,0])
        name=label('Zhou & Freedman · 2019',1.2,1,42)
        result=label('deficits after inactivation',1.2,-.3,36,RED)
        first=VGroup(control,impaired,name,result)
        faded=VGroup(*[Rectangle(width=.4,height=h,color=GREEN,fill_opacity=.8).move_to([-5.1+i*.65,-2.15+h/2,0]) for i,h in enumerate((1.35,.75,.18))])
        foot=label('schematic result icons',0,-3.2,28,GOLD)
        self.at('other studies')
        self.add(head('Other parietal inactivation studies'),control,impaired,name,foot)
        self.at('did find deficits')
        shorter=Rectangle(width=.65,height=1.55,color=RED,fill_opacity=.8).move_to([-3.7,-.775,0])
        self.play(Transform(impaired,shorter),FadeIn(result),run_time=.5)
        self.at('so the result')
        self.play(first.animate.scale(.8).move_to([0,1.35,0]),FadeIn(faded),
            FadeIn(VGroup(label('Jeurissen and colleagues · 2022',.8,-1,32),label('biases that faded',.8,-1.9,32,GREEN))),
            Transform(foot,label('debated · schematic result icons',0,-3.2,28,GOLD)),run_time=.6)
        self.finish()


class S16Faded(SpokenScene):
    def construct(self):
        baseline=-1.65
        def bar(x,h,opacity=1):
            return Rectangle(width=1.1,height=h,color=GREEN,fill_opacity=.8*opacity,stroke_opacity=opacity).move_to([x,baseline+h/2,0])
        bias=bar(-4,3.8)
        timeline=Line([-4.8,-3,0],[5.4,-3,0],color=PURPLE,stroke_width=14)
        self.at('in one study')
        self.add(head('Choice bias fades during inactivation',GREEN),axes(-5.15,5.6,baseline,2.5),
            label('choice bias',-6.05,.35,28,GREEN).rotate(PI/2),bias,
            label('time since inactivation →',.3,-2.2,30),
            timeline,label('schematic',4.6,1.45,26,GOLD),label('area silenced throughout',0,-3.5,28,PURPLE))
        self.at('the biases faded')
        # Schematic magnitudes, no time-course curve or numerical effect estimate.
        self.play(bias.animate.set_fill(opacity=.12),GrowFromEdge(bar(-.5,2.1),DOWN),GrowFromEdge(bar(3.4,.3),DOWN),run_time=1.4)
        self.at('still silenced')
        self.play(Indicate(timeline,color=PURPLE,scale_factor=1.01),run_time=.35)
        self.at('that suggests')
        self.play(FadeIn(label('compensation by other areas?',1.3,2.3,32,GOLD)),run_time=.5)
        self.finish()


class S17Open(SpokenScene):
    def construct(self):
        self.at('which areas')
        map_=brain()
        map_[0].stretch_to_fit_height(6.4).stretch_to_fit_width(12.4)
        map_[4].move_to([0,-3.65,0])
        self.add(map_,head('Where is the decision needed?'))
        nodes=VGroup()
        for text,color,pos in [('LIP ?',PINK,[1.4,1.65,0]),
                               ('frontal eye field ?',TEXT,[-2.25,.35,0]),
                               ('superior colliculus ?',TEXT,[.7,-1.5,0])]:
            box=RoundedRectangle(width=5.6,height=.9,corner_radius=.14,
                                 color=color,fill_opacity=.08)
            nodes.add(VGroup(box,T(text,34,color)).move_to(pos))
        self.add(nodes)
        self.at('open question')
        self.play(Indicate(nodes,color=GOLD,scale_factor=1.02),run_time=.35)
        self.finish()


class S18Takeaway(SpokenScene):
    def construct(self):
        # A computed accumulator is visible during the entire adding sentence.
        ax=axes(-4.4,4.8,-1.7,1.7)
        t=np.linspace(0,1.8,160)
        r=np.minimum(70,30+25*np.maximum(0,t-.2))
        ramp=poly([(-4.4+9.2*tt/1.8,-1.7+(rr-30)/40*3.4) for tt,rr in zip(t,r)],PINK)
        intro=VGroup(head('Adding up evidence'),ax,ramp,label('running total',-1.8,1.7,34,PINK),label('time →',.3,-2.3,28))
        self.at('if a decision')
        self.add(intro)
        places=VGroup(*[chip('area ?',c,36).move_to([x,-.3,0]) for x,c in [(-4,PINK),(0,GOLD),(4,GREY)]],label('perhaps several places',0,2.15,40))
        self.at('perhaps in several')
        self.play(FadeOut(intro),FadeIn(places),run_time=.5)
        visible=VGroup(chip('visible',PINK,64),label('shows the running total',0,-1.05,28,PINK))
        self.at('but a neuron')
        self.play(FadeOut(places),FadeIn(visible),run_time=.4)
        self.at('not always')
        left=chip('visible',PINK,58).move_to([-4.3,.3,0])
        needed=chip('needed',TEXT,58).move_to([4.3,.3,0])
        relation=VGroup(label('does not',0,.65,36,GOLD),label('always mean',0,-.05,36,GOLD))
        self.play(ReplacementTransform(visible[0],left),FadeOut(visible[1]),
                  FadeIn(relation),FadeIn(needed),run_time=.45)
        self.finish()


class S19End(EndCard):
    LINE='A neuron showing the running total is not always needed.'
