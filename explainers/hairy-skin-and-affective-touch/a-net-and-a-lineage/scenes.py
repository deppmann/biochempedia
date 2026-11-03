"""Chapter 3 repair.
COLOR MAP: shared reference GREEN human CT, PURPLE #B58CD9 ratings,
BLUE recording, YELLOW stimulus, ORANGE #F29E4C field-LTMR / mouse outcomes,
RED removal / unsupported link, GREY anatomy. Distinct mouse subtypes:
TH #70B7F0 (sky blue), MRG #ED86B3 (rose), FIELD #F29E4C (orange).
Reference bell is computed from scenes.old.py. Other traces are explicit
illustrative models, never fitted data: event kernel, force threshold and
integrate-and-fire summation. Model amplitudes/time units are not measurements.
"""
import numpy as np
from bp_style import *
PURPLE='#B58CD9'
ORANGE=FIELD='#F29E4C'
TH='#70B7F0'
MRG='#ED86B3'
LESSON='Hairy Skin, Stroking and Affective Touch'

def label(s,x=0,y=3.1,size=30,color=TEXT):
    return T(s,size=size,color=color).move_to([x,y,0])

def path(points,color=GREY,width=4):
    return VMobject(color=color,stroke_width=width).set_points_as_corners([np.array([*p,0]) for p in points])

def skin_bar(x0,x1,y,h=.4):
    return RoundedRectangle(corner_radius=.1,width=x1-x0,height=h,color=GREY,fill_opacity=.24).move_to([(x0+x1)/2,y,0])

def hair(x,y,h=1.2):
    return Line([x,y,0],[x,y+h,0],color=GREY,stroke_width=5)

def brush(x,y,w=1):
    return VGroup(Line([x,y+.85,0],[x,y+.25,0],color=YELLOW,stroke_width=7),
        Rectangle(width=w,height=.22,color=YELLOW,fill_opacity=.5).move_to([x,y+.18,0]),
        *[Line([x+dx,y+.07,0],[x+dx,y-.12,0],color=YELLOW,stroke_width=3) for dx in np.linspace(-w*.45,w*.45,13)])

def mouse():
    return VGroup(Ellipse(width=2.8,height=1.4,color=GREY,fill_opacity=.3),
        Ellipse(width=1,height=.9,color=GREY,fill_opacity=.3).move_to([1.35,.15,0]),
        Circle(.3,color=GREY,fill_opacity=.5).move_to([1,.8,0]),Dot([1.65,.3,0],radius=.05,color=TEXT),
        path([(-1.4,0),(-2,.3),(-2.4,.8)],GREY,5),
        Line([-.8,-.55,0],[-.5,-.9,0],color=GREY,stroke_width=5),
        Line([.6,-.55,0],[1,-.9,0],color=GREY,stroke_width=5))

def follicle(x=-4.4):
    return VGroup(skin_bar(x-1.6,x+1.6,1.4),hair(x,1.6,1.3),
        RoundedRectangle(corner_radius=.28,width=.65,height=2.8,color=GREY,fill_opacity=.2).move_to([x,-.15,0]))

def ending(kind='field',x=-4.4):
    c={'th':TH,'mrg':MRG,'field':FIELD}[kind]
    base=VGroup(Circle(.34,color=c,fill_opacity=.3).move_to([x,-2.8,0]))
    if kind=='mrg':
        base.add(path([(x,-2.45),(x-1.1,-1.8),(x-1.1,.65),(x-.8,1.05)],c,4))
        tips=VGroup(path([(x-1.1,.1),(x-1.45,.55),(x-1.3,1.05)],c),Dot([x-.8,1.05,0],color=c,radius=.07))
    elif kind=='th':
        base.add(path([(x,-2.45),(x-.95,-1.8),(x-.48,-1.3)],c,4),path([(x-.95,-1.8),(x+.75,-1.8),(x+.75,-1.4),(x+.48,-1.3)],c,4))
        tips=VGroup(*[Line([x+s*.48,-1.3,0],[x+s*.48,1.05,0],color=c,stroke_width=5) for s in [-1,1]])
    else:
        base.add(path([(x,-2.45),(x-1,-1.9),(x-1,.3)],c,9))
        for y in [-1.6,-.9,-.2]:
            base.add(RoundedRectangle(width=.3,height=.43,corner_radius=.1,color=c,fill_opacity=.65).move_to([x-1,y,0]))
        tips=VGroup(*[Ellipse(width=1.45,height=.35,color=c,stroke_width=6).move_to([x,y,0]) for y in [-1,-.35,.3]])
        base.add(Line([x-1,.3,0],[x-.72,.3,0],color=c,stroke_width=6))
    return base,tips

def scoreboard(n=0,active=-1):
    rows=VGroup()
    specs=[('TH C-LTMR','marker: tyrosine hydroxylase (TH)','lanceolate · unmyelinated',TH),
           ('MrgprB4 neurons','marker: MrgprB4 receptor','free endings · unmyelinated',MRG),
           ('Aβ field-LTMR','class: Aβ field afferent','circumferential · myelinated',FIELD)]
    for i,(name,marker,shape,c) in enumerate(specs):
        y=1.95-i*1.7
        box=RoundedRectangle(width=7.4,height=1.65,corner_radius=.12,color=c,stroke_opacity=1 if i==active else .45,fill_color=c,fill_opacity=.12 if i==active else .03).move_to([2.05,y-.12,0])
        row=VGroup(box,label(name,.1,y+.35,30,c).align_to(box,LEFT).shift(RIGHT*.25))
        if i<n:
            row.add(label(marker,2.05,y-.2,26),label(shape,2.05,y-.7,26,c))

        rows.add(row)
    return VGroup(label('Three mouse candidates',2,3.35,30),rows)

def comparison_anatomy(kind=None):
    f=follicle()
    f[2].stretch(1.65,1,about_edge=UP)
    anatomy=VGroup(f)
    if kind:
        b,t=ending(kind); anatomy.add(b,t)
    # Enlarge only the anatomy; keep the comparison's typography unchanged.
    return anatomy.stretch(1.12,1).shift(DOWN*.05)

def class_scene(scene,kind,n,phrase):
    board=scoreboard(n,n-1); anatomy=comparison_anatomy(kind)
    scene.add(anatomy,board)
    scene.at(phrase); scene.play(Indicate(anatomy[-1],scale_factor=1.015),run_time=.65)
    return board

def net():
    trunk=VGroup(Circle(.3,color=FIELD,fill_opacity=.4).move_to([0,-1.65,0]),
        Line([0,-1.35,0],[0,-.85,0],color=FIELD,stroke_width=6),Line([-5.4,-.85,0],[5.4,-.85,0],color=FIELD,stroke_width=4))
    follicles=VGroup(); branches=VGroup()
    for x in np.linspace(-5.4,5.4,7):
        follicles.add(VGroup(hair(x,1.1,.95),RoundedRectangle(corner_radius=.12,width=.3,height=.85,color=GREY,fill_opacity=.2).move_to([x,.6,0])))
        branches.add(VGroup(Line([x,-.85,0],[x,.35,0],color=FIELD,stroke_width=3),Ellipse(width=.65,height=.24,color=FIELD,stroke_width=4).move_to([x,.65,0])))
    return VGroup(skin_bar(-6,6,1.1,.23),follicles,trunk,branches)

def trace_axis(x=-2.5,y=-2.7,w=5):
    return VGroup(Line([x,y,0],[x+w,y,0],color=GREY),label('spikes',x-1,y+.15,26,FIELD),label('time →',x+w+.7,y,26,GREY))

def spike_model(drive=0,n=800):
    # Leaky integrate-and-fire: summed drive above 2.5 gives repetitive spikes.
    ts=np.linspace(0,1,n); voltage=0.; events=[]
    for t in ts:
        voltage+=max(0,drive-2.5)/n*8
        if voltage>=1: events.append(t); voltage=0
    return events

def spikes(drive,x=-2.5,y=-2.7,w=5):
    return VGroup(*[Line([x+t*w,y,0],[x+t*w,y+.55,0],color=FIELD,stroke_width=4) for t in spike_model(drive)])

def prediction():
    return VGroup(net(),brush(0,2.3,10.5),label('PREDICT',y=3.45,size=36,color=YELLOW),
        Arrow([-5,2.08,0],[5,2.08,0],color=YELLOW,buff=0),trace_axis(),label('?',0,-2.35,40,FIELD),
        label('Gentle sweep across the whole field: fires or silent?',y=-3.65,size=28))

def net_card():
    # Keep vertical scale of the receptive field. Compress only its horizontal span.
    lever=follicle(0).shift(LEFT*4.5+UP*.25); b,t=ending('th',0); aff=VGroup(b,t).shift(LEFT*4.5+UP*.25)
    n=net(); n.stretch(.65,0).shift(RIGHT*2.15+DOWN*.1)
    return VGroup(lever,aff,n,label('A single hair is a lever',-3.9,-3.25,29),label('A field afferent is a net',3,-3.25,29,FIELD))

def chamber():
    boxes=VGroup(Rectangle(width=3.9,height=5.1,color=GREY).move_to([-4,0,0]),Rectangle(width=3.9,height=5.1,color=MRG,fill_opacity=.13).move_to([0,0,0]))
    return VGroup(boxes,mouse().scale(.68).move_to([0,0,0]),label('unpaired',-4,-2.9,26,GREY),label('activation-paired',0,-2.9,26,MRG),Rectangle(width=.24,height=1.25,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([-2,0,0]))

def time_bars():
    # Direction only; illustrative occupancy fractions, not reported values.
    g=VGroup(Line([2.7,-2.3,0],[6.2,-2.3,0],color=GREY),
        Arrow([2.7,-2.3,0],[2.7,1.8,0],color=GREY,buff=0),
        label('time in chamber',4.5,2.3,26),label('(schematic)',4.5,1.85,24,GREY),
        label('unpaired',3.55,-2.7,22,GREY),label('paired',5.25,-2.7,22,MRG),label('0',2.4,-2.3,22,GREY))
    for x,h,c in [(3.55,1.2,GREY),(5.25,3,MRG)]:
        g.add(Rectangle(width=.85,height=h,color=c,fill_opacity=.6).move_to([x,-2.3+h/2,0]))
    return g

def bell(x): return float(np.exp(-((x-.5)/.62)**2))

def human_plot():
    ox,oy,w,h=-5,-2.5,10,5.15
    def p(x,y=0): return np.array([ox+(x+1)/3*w,oy+y*h*.9,0])
    band=Rectangle(width=w/3,height=h,stroke_width=0,fill_color=YELLOW,fill_opacity=.1).move_to([p(.5)[0],oy+h/2,0])
    axes=VGroup(band,Line(p(-1),p(2),color=GREY),Line(p(-1),p(-1,1.1),color=GREY),
        *[label(s,p(x)[0],-2.87,26) for s,x in [('0.1',-1),('1',0),('10',1),('100',2)]],
        label('stroke speed · cm/s (log scale)',y=-3.15,size=26),
        label('normalized response / rating',-5.9,.1,26).rotate(PI/2),
        label('Human CT firing',-2.9,3.45,28,GREEN),label('pleasantness ratings',2.7,3.45,28,PURPLE),
        label('1–10 cm/s',.1,2.95,26,YELLOW))
    ct=ParametricFunction(lambda t:p(t,bell(t)),t_range=[-1,2,.015],color=GREEN,stroke_width=7)
    # Same model, separate purple point symbols rather than an obscuring overlap.
    ratings=VGroup(*[Circle(radius=.105,color=PURPLE,stroke_width=4,fill_color=BG,fill_opacity=1).move_to(p(x,bell(x))) for x in np.linspace(-.8,1.8,15)])
    caption=label('Normalized reference model · separate groups, different people',y=-3.65,size=26,color=GREY)
    return axes,ct,ratings,caption

def event_kernel(t):
    # Unit peak causal gamma kernel. Time and amplitudes chosen for illustration.
    return 0 if t<=0 else float((t/.22)**2*np.exp(2-2*t/.22))

def photometry():
    g=VGroup(label('Nucleus accumbens · fibre photometry',y=3.45,size=30),
        label('dopamine-sensor signal, arbitrary units',-6,.1,26).rotate(PI/2),
        label('Illustrative model · timing and amplitudes are not data',y=-3.5,size=26,color=GREY))
    curves=[]
    for y,amp,name in [(1.05,1,'Control females · larger'),(-1.65,.32,'Lineage ablated · reduced')]:
        g.add(Line([-4.8,y,0],[5.8,y,0],color=GREY),Line([-4.8,y,0],[-4.8,y+1.8,0],color=GREY),
              label(name,.8,y+1.95,28,MRG),DashedLine([-2.7,y,0],[-2.7,y+1.65,0],color=YELLOW),label('0',-5.15,y,26,GREY))
        curves.append(ParametricFunction(lambda t,y=y,amp=amp:[-4.8+t*10.6,y+1.65*amp*event_kernel(t-.2),0],t_range=[0,1,.005],color=MRG,stroke_width=5))
    g.add(label('mounting begins',-2.7,-2.25,26,YELLOW),label('time →',4.6,-2.25,26,GREY))
    return g,VGroup(*curves)

class S00Title(TitleCard):
    LESSON=LESSON
    TITLE='A Net, a Lineage and a Mouse That Cannot Say'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',y=2.7,size=26,color=TEAL),label(self.LESSON,y=1.9,size=28,color=GREY))
        title=VGroup(*[T(s,size=44,font=TITLE_FONT) for s in ['A Net, a Lineage','and a Mouse That Cannot Say']]).arrange(DOWN,buff=.25)
        self.play(FadeIn(title),run_time=.6); self.finish()

class S01Q(SpokenScene):
    def construct(self):
        m=mouse().scale(2.1).move_to([0,-.8,0]); b=brush(-.5,1.1)
        bubble=VGroup(RoundedRectangle(width=3.5,height=.8,corner_radius=.2,color=GREY).move_to([3.8,2.05,0]),
            path([(3.3,1.65),(3.65,1.05),(4,1.65)],GREY,3),label('feels nice',3.8,2.05,30),
            Line([2.2,1.8,0],[5.4,2.3,0],color=RED,stroke_width=5))
        self.add(m,b,bubble,label('Which cells?',-3.2,3.2,36,FIELD),label('and what outcome?',2.6,3.2,36,YELLOW))
        self.at('A mouse'); self.play(b.animate.shift(RIGHT*1.2),run_time=.65)
        self.at('Which of its cells'); self.play(Indicate(self.mobjects[-2],scale_factor=1.03),run_time=.25)
        self.at('what can we measure'); self.play(Indicate(self.mobjects[-1],scale_factor=1.03),run_time=.25)
        self.finish()

class S02Three(SpokenScene):
    def construct(self):
        self.add(comparison_anatomy(),scoreboard())
        self.at('at least three'); self.play(Indicate(scoreboard()[1],scale_factor=1.01),run_time=.6)
        self.finish()

class S03Th(SpokenScene):
    def construct(self):
        self.add(label('C-LTMR: C-fibre low-threshold mechanoreceptor',x=1.5,y=-3.6,size=24,color=TH))
        class_scene(self,'th',1,'Their endings')
        self.finish()

class S04Mrgpr(SpokenScene):
    def construct(self):
        # Put both skin types in the anatomy column, beside the follicle.
        anatomy=comparison_anatomy('mrg').shift(LEFT*.35)
        anatomy[0][0].stretch(.62,0).shift(LEFT*.35)
        self.add(anatomy,scoreboard(2,1))
        patch=VGroup(skin_bar(-3.9,-2,1.52,.4),label('glabrous',-2.95,2.05,24,GREY),
            label('hairy',-5.3,2.05,24,GREY),label('no fibre',-2.95,.95,24,GREY),
            label('hairy skin only',-3.05,-1.8,24,MRG))
        self.at('Their'); self.play(FadeIn(patch),run_time=.3)
        self.finish()

class S05Field(SpokenScene):
    def construct(self):
        class_scene(self,'field',3,'their endings')
        self.wait(1)
        self.add(label('LTMR: low-threshold mechanoreceptor',y=-3.6,size=26,color=FIELD))
        self.finish()

class S06Ignore(SpokenScene):
    def construct(self):
        f=follicle(); b,t=ending(); self.add(f,b,t,label('High indentation threshold',2.4,3.2,30,YELLOW))
        ax=VGroup(Line([-.8,-1.5,0],[5.8,-1.5,0],color=GREY),label('schematic firing',2.5,-2.25,26,FIELD),label('time →',4.6,-1.95,26,GREY))
        self.add(ax,label('force',2.5,1.9,28,YELLOW))
        self.at('ignores any single hair'); self.play(Rotate(f[1],-.35,about_point=f[1].get_start()),run_time=.4)
        self.at('Indenting the skin')
        self.remove(f[0])
        probe=Rectangle(width=.6,height=1.3,color=YELLOW,fill_opacity=.6).move_to([-3.25,2.35,0]); self.add(probe)
        for i,name in enumerate(['low','medium','high']):
            if i==2: self.at('high force')
            bar=Rectangle(width=1.1*(i+1),height=.35,color=YELLOW,fill_opacity=.6).move_to([2.5,1.25,0])
            txt=label(name,2.5,.55,32,YELLOW)
            depth=[.1,.3,.8][i]
            deform=path([(-6,1.6),(-3.7,1.6),(-3.55,1.6-depth),(-2.95,1.6-depth),(-2.8,1.6)],GREY,6)
            if i: self.remove(prevbar,prevtxt,prevdef)
            self.add(bar,txt,deform)
            self.play(probe.animate.move_to([-3.25,2.25-depth,0]),run_time=.35)
            if i<2: self.wait(.3)
            else:
                self.play(Create(spikes(4,-.8,-1.5,6.6)),run_time=.4)
                self.wait(2.5)
            prevbar,prevtxt,prevdef=bar,txt,deform
        self.finish()

class S07Endings(SpokenScene):
    def construct(self):
        self.add(label('Up to 180 endings · one neuron',y=3.35,size=36,color=FIELD),label('Representative subset · … ×180',y=-3.3,size=28,color=GREY))
        f=follicle(); b,t=ending(); original=VGroup(f,b,t); self.add(original)
        self.at('one neuron'); self.play(ReplacementTransform(original,net()),run_time=.9); self.finish()

class S08Predict(SpokenScene):
    def construct(self):
        self.add(prediction()); self.at('Predict'); self.play(Indicate(self.mobjects[0][2],scale_factor=1.04),run_time=.4); self.finish()

class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction(),label('Pause the video to decide',y=-3.12,size=26,color=YELLOW)); self.wait(5)

class S10Reveal(SpokenScene):
    def construct(self):
        p=prediction(); p.remove(p[2],p[5],p[6]); self.add(p)
        p[1].shift(LEFT*4.5); p[1].stretch(.3,0)
        self.at('It fires')
        for i,branch in enumerate(p[0][3]):
            anim=[p[1].animate.move_to([-4.8+i*1.6,2.65,0]),branch.animate.set_color(YELLOW).set_stroke(width=7)]
            if i==3: anim.append(Create(spikes(5)))
            self.play(*anim,run_time=.3,rate_func=linear)
        self.at('The authors proposed'); self.play(FadeIn(label('Summation across endings · proposed',y=3.45,size=32,color=FIELD)),run_time=.3)
        self.at('sums many'); self.play(Indicate(p[0][2],color=YELLOW,scale_factor=1.05),run_time=.4)
        self.add(label('Illustrative threshold model',y=-3.5,size=26,color=GREY)); self.finish()

class S11Net(SpokenScene):
    def construct(self):
        c=net_card(); self.add(c)
        self.at('A single hair'); self.play(Rotate(c[0][1],-.3,about_point=c[0][1].get_start()),run_time=.4)
        self.at('A field afferent'); self.play(Indicate(c[2],color=FIELD,scale_factor=1.02),run_time=.4)
        self.play(Rotate(c[0][1],.3,about_point=c[0][1].get_start()),run_time=.2); self.finish()

class S12Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(net_card()); self.wait(2.5)

class S13Cpp(SpokenScene):
    def construct(self):
        c=chamber(); door=c[4]; c.remove(door)
        phase=label('1 · Conditioning: confined to paired side',y=3.35,size=30,color=MRG)
        self.add(c,phase)
        barrier=Line([-2,-2.55,0],[-2,2.55,0],color=MRG,stroke_width=8); self.add(barrier)
        self.at('Activating'); chem=label('MrgprB4\nchemogenetic\nactivation\n(DREADD)',4.3,.5,26,MRG)
        self.play(FadeIn(chem),Indicate(c[0][1],color=MRG,scale_factor=1.01),run_time=.4)
        self.at('young male mice'); self.add(label('Vrontou et al., 2013 · males about one month old',y=-3.6,size=26,color=GREY))
        self.at('a place preference'); self.remove(phase,chem)
        self.add(label('2 · Test: free choice, more time on paired side',y=3.35,size=30,color=MRG))
        self.play(FadeOut(barrier),FadeIn(door),c[1].animate.move_to([-4,0,0]),run_time=.6)
        self.play(c[1].animate.move_to([0,0,0]),FadeIn(time_bars()),run_time=.9)
        self.wait(1.5); self.finish()

class S14Read(SpokenScene):
    def construct(self):
        c=chamber(); self.add(c,time_bars(),label('Place preference: two interpretations',y=3.35,size=32))
        self.at('positive reinforcement'); self.play(c[1].animate.move_to([-4,0,0]),run_time=.6)
        self.remove(self.mobjects[1])
        self.add(label('positive\nreinforcement',4.3,1.5,27,MRG))
        self.at('reduced anxiety'); self.play(c[1].animate.move_to([0,0,0]),FadeIn(label('reduced\nanxiety',4.3,-.5,27,MRG)),run_time=.6)
        self.at('or both'); self.play(FadeIn(label('both kept open',y=-3.6,size=30,color=TEXT)),run_time=.3); self.finish()

class S15Elias(SpokenScene):
    def construct(self):
        self.add(label('Ablation in development → testing in adult',y=3.4,size=30,color=MRG),label('Elias et al., 2023 · adult females',y=-3.6,size=26,color=GREY))
        fibres=[]; names=[]
        for x,name in [(-3.3,'Control female'),(3.3,'Lineage ablated')]:
            m=mouse().scale(1.1).move_to([x,1.1,0]); f=VGroup(*[path([(x+dx-.2,.8),(x+dx,1.1),(x+dx,1.6)],MRG,5) for dx in [-.8,0,.8]])
            nm=label(name,x,2.6,30,MRG); self.add(m,f,nm); fibres.append(f); names.append(nm)
        self.add(label('Mrgprb4 lineage: permanently labelled fibres',y=-.5,size=28,color=MRG),Line([-5,-2.6,0],[5,-2.6,0],color=GREY),label('sexual receptivity',y=-3.05,size=28))
        bars=VGroup(Rectangle(width=1.5,height=1.4,color=MRG,fill_opacity=.6).move_to([-3.3,-1.9,0]),Rectangle(width=1.5,height=1.4,color=MRG,fill_opacity=.6).move_to([3.3,-1.9,0]))
        self.at('removed during development'); self.play(fibres[1].animate.set_color(GREY),names[1].animate.set_color(GREY),run_time=.4)
        self.at('less sexually receptive'); target=Rectangle(width=1.5,height=.55,color=MRG,fill_opacity=.6).move_to([3.3,-2.325,0])
        bars[1].become(target)
        self.play(FadeIn(bars),FadeIn(label('lower',4.8,-1.9,28,MRG)),run_time=.4)
        self.add(label('directional comparison · no numerical scale',y=-.95,size=26,color=GREY)); self.wait(3.2); self.finish()

class S16Lineage(SpokenScene):
    def construct(self):
        self.add(label('Permanent label marks past Mrgprb4 expression',y=3.45,size=30,color=MRG))
        def cells(y): return VGroup(*[VGroup(Circle(.73,color=MRG,stroke_width=7),Dot(radius=.4,color=MRG)).move_to([x,y,0]) for x in [-2.6,0,2.6]])
        early=cells(1.55); adult=cells(-1.15)
        self.add(early,label('Early',-4.8,1.55,30),label('Adult',-4.8,-1.15,30),adult,
            label('ring = permanent label · centre = current expression',y=-3.35,size=26,color=GREY))
        self.at('once expressed the gene'); self.play(Indicate(early,scale_factor=1.02,color=MRG),run_time=.35)
        self.at('including some'); self.play(FadeOut(adult[0][1]),FadeOut(adult[2][1]),run_time=.35)
        self.add(label('label stays on; Mrgprb4 expression off in some',y=-2.55,size=28,color=MRG))
        self.wait(3.2); self.finish()

class S17Dopamine(SpokenScene):
    def construct(self):
        g,c=photometry(); self.add(g)
        self.at('dopamine sensor signal'); self.play(Create(c[0]),run_time=.65)
        self.at('was reduced'); self.play(Create(c[1]),run_time=.55)
        self.wait(3.2); self.finish()

class S18Outcome(SpokenScene):
    def construct(self):
        icons=[]
        c=VGroup(Rectangle(width=1.7,height=3.3,color=GREY).move_to([-5.2,.65,0]),Rectangle(width=1.7,height=3.3,color=MRG,fill_opacity=.13).move_to([-3.45,.65,0]),mouse().scale(.32).move_to([-3.45,.65,0]),Rectangle(width=.15,height=.6,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([-4.325,.65,0]))
        m=VGroup(mouse().scale(.72),Arrow([-.5,-1.6,0],[-.5,1.6,0],color=MRG),label('posture',0,-1.9,26,MRG)).move_to([0,.7,0])
        tr=VGroup(Line([2.7,-1,0],[5.9,-1,0],color=GREY),Line([2.7,-1,0],[2.7,2.4,0],color=GREY),ParametricFunction(lambda t:[2.7+t*3.2,-1+3*event_kernel(t-.15),0],t_range=[0,1,.005],color=MRG,stroke_width=5))
        for x,obj,txt in [(-4.3,c,'chamber preference'),(0,m,'mating behaviour'),(4.3,tr,'dopamine signal')]:
            obj.stretch_to_fit_height(4.7).move_to([x,.4,0])
            panel=RoundedRectangle(width=4,height=5.2,corner_radius=.15,color=GREY,stroke_opacity=.45).move_to([x,.4,0]); self.add(panel)
            icons.append(VGroup(obj,label(txt,x,-2.6,27,MRG)))
        self.add(icons[0])
        self.at('A chamber preference'); self.play(Indicate(icons[0],scale_factor=1.015,color=MRG),run_time=.3)
        self.at('a mating'); self.play(FadeIn(icons[1]),run_time=.3)
        self.at('a dopamine signal'); self.play(FadeIn(icons[2]),run_time=.3)
        self.add(label('time →',4.3,-1.55,22,GREY),label('sensor (a.u.)',4.3,3.15,22,MRG))
        self.at('Each is an outcome'); self.play(FadeIn(label('OUTCOME',y=3.45,size=38)),run_time=.25)
        self.at('not a feeling'); f=label('feeling',y=-3.2,size=36,color=GREY); self.play(FadeIn(f),Create(Line([-1.2,-3.2,0],[1.2,-3.2,0],color=RED,stroke_width=5)),run_time=.25); self.finish()

class S19Idea(SpokenScene):
    def construct(self):
        a,c,r,cap=human_plot(); legend=a[10]; a.remove(legend); self.add(a,c,cap)
        self.at('pleasantness follows'); self.play(FadeIn(legend),FadeIn(r),run_time=.5); self.wait(3.2); self.finish()

class S20Open(SpokenScene):
    def construct(self):
        # Full-height human reference, beside the three unresolved mouse candidates.
        def p(x,y): return [-5.8+(x+1)/3*5.3,-2.5+y*4.8,0]
        c=ParametricFunction(lambda t:p(t,bell(t)),t_range=[-1,2,.015],color=GREEN,stroke_width=7)
        r=VGroup(*[Circle(radius=.09,color=PURPLE,stroke_width=3,fill_color=BG,fill_opacity=1).move_to(p(x,bell(x))) for x in np.linspace(-.8,1.8,15)])
        unsettled=label('Unsettled',3.5,-2.7,32,RED)
        self.add(c,r,Line(p(-1,0),p(2,0),color=GREY),Line(p(-1,0),p(-1,1.08),color=GREY),
            label('Human CT + ratings',-3.2,2.9,28,GREEN),label('stroke speed (log)',-3.2,-2.95,26),
            label('Normalized reference model · separate groups',y=-3.6,size=26,color=GREY),
            label('Which mouse cell, if any, matches the human fibre?',y=3.5,size=29),
            unsettled)
        for i,(txt,col) in enumerate([('TH C-LTMR',TH),('MrgprB4',MRG),('Aβ field-LTMR',FIELD)]):
            y=1.75-i*1.65
            self.add(chip(txt,col,28).move_to([3.9,y,0]),Arrow([2.2,y,0],[.5,y,0],color=col,buff=.1),label('?',.1,y,36,col))
        self.at('still unsettled'); self.play(Indicate(unsettled,scale_factor=1.03,color=RED),run_time=.3); self.finish()

class S21Take(SpokenScene):
    def construct(self):
        left=VGroup(RoundedRectangle(width=5.6,height=4.8,corner_radius=.2,color=GREEN),label('Human candidate',0,1.5,34,GREEN),label('CT afferent',0,0,32,GREEN),label('recorded firing',0,-1.5,28,GREEN)).move_to([-3.25,.4,0])
        right=VGroup(RoundedRectangle(width=5.6,height=4.8,corner_radius=.2,color=FIELD),label('Mouse outcomes',0,1.5,34,FIELD),label('place preference',0,.4,28,FIELD),label('sexual receptivity',0,-.5,28,FIELD),label('dopamine signal',0,-1.4,28,FIELD)).move_to([3.25,.4,0])
        self.add(left)
        self.at('and the mouse'); self.play(FadeIn(right),run_time=.3)
        self.at('apart until'); self.play(Create(DashedLine([0,3.1,0],[0,-2.4,0],color=GREY)),run_time=.3)
        self.at('a match is made'); self.play(FadeIn(label('Keep them apart until a match is made.',y=-3.2,size=34)),run_time=.3); self.finish()

class S22End(EndCard):
    LINE='Keep the human candidate and the mouse outcomes apart until a match is made.'
    def construct(self):
        lines=VGroup(*[T(s,size=40,font=TITLE_FONT) for s in ['Keep the human candidate','and the mouse outcomes apart','until a match is made.']]).arrange(DOWN,buff=.35)
        self.add(lines,label('biochemistrypedia.com',y=-2.2,size=26,color=TEAL)); self.finish()
