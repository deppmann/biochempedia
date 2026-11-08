"""Chapter 3: Which Channel, and What the Test Can Prove.
COLOR MAP (shared): GREEN #83C167 Piezo/stretch/function; RED #FC6255 lost
reflex/apnoea; TEAL #3FB8C0 light; PINK #E58BC4 hypothesis/questions;
GREY #8B93A1 anatomy/control; BLUE #7C9CFF protection; YELLOW Npy2r;
ORANGE #F29E4C light-gated channel. No molecular structures.
Quantitative curve: exact lesson F(x). Bars: reported means and SEM.
Other traces are computed schematic models, explicitly labelled.
"""
import numpy as np
from bp_style import *
import kx_manim
# Audio already includes its pauses. Avoid cumulative 0.4 s scene-start drift.
kx_manim.TAIL = 0.0
PINK = '#E58BC4'
BLUE = '#7C9CFF'
ORANGE = '#F29E4C'


def lab(s,x=0,y=3.15,c=TEXT,n=30):
    return T(s,size=n,color=c,line_spacing=.85).move_to([x,y,0])


def arr(a,b,color=GREY,w=5):
    return Arrow(a,b,buff=.08,color=color,stroke_width=w,tip_length=.2,
                 max_tip_length_to_length_ratio=.3)


def cell(color=GREY,r=.85,pos=(0,0)):
    return Circle(radius=r,stroke_color=color,stroke_width=4,
        fill_color=color,fill_opacity=.12).move_to([*pos,0])


def box(x,y,w,h,color=GREY):
    return RoundedRectangle(width=w,height=h,corner_radius=.16,
        color=color,fill_color=color,fill_opacity=.07).move_to([x,y,0])


def patch(opened=False,y=.5):
    # Membrane stops before the pore in both states; no overlapping bars.
    walls=VGroup(*[box(x,y,4.35,.6) for x in [-3.8,3.8]])
    gates=VGroup(*[box(x,y,.42,2.2,GREEN) for x in ([-.8,.8] if opened else [-.22,.22])])
    return VGroup(walls,gates)


def lung(x=-4.5,y=.1):
    return VGroup(*[Ellipse(width=1.55,height=3.5,color=GREY,
        fill_color=GREY,fill_opacity=.12).move_to([x+d,y,0]) for d in [-.85,.85]],
        Line([x,y+2.5,0],[x,y+.8,0],color=GREY,stroke_width=8),
        *[Line([x,y+.8,0],[x+d,y+.2,0],color=GREY,stroke_width=6) for d in [-.8,.8]])


def wave(ax,amp=.8,color=GREY,flat_after=99):
    # Computed oscillator, used only for labelled qualitative schematics.
    return ax.plot(lambda t: amp*np.sin(2*np.pi*t/2) if t<flat_after else 0,
                   x_range=[0,8,.025],color=color,stroke_width=4)


def questions(y=1.6):
    return VGroup(*[VGroup(box(x,y,3.7,1.3,GREEN if i==1 else GREY),
        lab(t,x,y,GREEN if i==1 else GREY,32)) for i,(x,t) in
        enumerate([(-4.35,'What stimulus?'),(0,'What channel?'),(4.35,'What output?')])])


def table(stage=2,result=True):
    g=VGroup(lab('Drug-evoked baroreflex',0,3.15,n=34),
        lab('Deletion in nodose and petrosal neurons',0,2.45,GREY,28),
        lab('Genotype',-4.35,1.55,GREY,28),
        lab('Result against littermate controls',1.75,1.55,GREY,28))
    rows=[('Control','reference'),('Piezo1 knockout','no statistically detectable difference'),
        ('Piezo2 knockout','no statistically detectable difference'),('Double knockout','essentially abolished')]
    for i in range(stage+1):
        y=.75-i*.91
        g.add(lab(rows[i][0],-4.3,y,GREEN if i else GREY,28))
        if i<stage or result:
            g.add(lab(rows[i][1],1.65,y,RED if i==3 else TEXT,28))
    g.add(lab('Single deletions: no statistically detectable difference in the reported assay',0,-3.15,GREY,26))
    return g


def model(x):
    return 5*(1+.35**2)*x*x/(.35**2+x*x)


def ticks(ax,xs,ys):
    return VGroup(*[T(str(v),size=28,color=GREY).next_to(ax.c2p(v,0),DOWN,buff=.12) for v in xs],
        *[T(str(v),size=28,color=GREY).next_to(ax.c2p(0,v),LEFT,buff=.15) for v in ys])


def curve_panel(compact=False,hedge=True):
    ax=Axes(x_range=[0,1,.5],y_range=[0,5,1],x_length=5 if compact else 9.8,
        y_length=4.3,tips=False,axis_config={'color':GREY}).move_to([-3.3 if compact else -.15,-.05,0])
    c=ax.plot(model,x_range=[0,1,.005],color=PINK,stroke_width=5)
    labs=VGroup(ticks(ax,[0,.5,1],[0,1,3,5]),
        lab('Hypothetical model' if compact else 'Illustrative model • not measured',-3.3 if compact else 0,3.2,PINK,32),
        lab('Magnitude (bpm/mmHg)',-3.3 if compact else 0,2.55,GREY,28),
        lab('Input fraction' if compact else 'Hypothetical fraction of control sensory input',-3.3 if compact else 0,-2.8,GREY,28))
    if hedge: labs.add(lab('Neither deletion’s effect on current was measured',0,-3.4,PINK,28))
    return ax,c,labs


def measured(compact=False):
    cx=3.7 if compact else .2
    w=4.2 if compact else 9.4
    ax=Axes(x_range=[0,3,1],y_range=[-6,0,1],x_length=w,y_length=4.4,
        tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([cx,-.15,0])
    g=VGroup(ax,lab('Measured',cx,3.2,n=32),lab('Sensitivity (bpm/mmHg)',cx,2.55,GREY,28))
    for v in [0,-1,-3,-5,-6]:
        g.add(T(str(v),size=28,color=GREY).next_to(ax.c2p(0,v),LEFT,buff=.12))
    for x,v,sem,name,col in [(1,-5,.5,'Control',GREY),(2.35,-.6,.4,'Double KO',GREEN)]:
        top=ax.c2p(x,0); end=ax.c2p(x,v)
        g.add(Rectangle(width=.65 if compact else 1.3,height=abs(end[1]-top[1]),
            color=col,fill_color=col,fill_opacity=.6).move_to((top+end)/2))
        g.add(Line(ax.c2p(x,v-sem),ax.c2p(x,v+sem),color=TEXT))
        for vv in [v-sem,v+sem]:
            pos=ax.c2p(x,vv);g.add(Line(pos+LEFT*.17,pos+RIGHT*.17,color=TEXT))
        g.add(lab(name,top[0],-2.95,col,28),lab(f'−{abs(v):.1f} ± {sem:.1f}',top[0],-2.35 if v==-5 else .9,col,28))
    g.add(lab('Mean ± SEM',cx,-3.5,GREY,28))
    return g


def evidence():
    g=VGroup(lab('Reported assay',3.95,2.6,GREY,28))
    for y,name,res in [(1.25,'Piezo1 KO','no statistically\ndetectable difference'),(-.35,'Piezo2 KO','no statistically\ndetectable difference'),(-1.95,'Double KO','essentially abolished')]:
        g.add(lab(name,3.95,y+.55,GREEN,28),lab(res,3.95,y-.12,RED if name=='Double KO' else TEXT,28))
    g.add(lab('(reported assay)',3.95,-3.15,GREY,28))
    return g


def choices(state=0):
    # state 0: intact; 1: P1 deleted; 2: P2 deleted; 3: both deleted.
    g=VGroup(lab('Both in each cell',-3.55,2.6,PINK,30),
        lab('Separate cell groups',-3.55,-.25,PINK,30))
    paths=[]
    for separate,y in [(False,1.3),(True,-1.6)]:
        positions=[(-4.9,y),(-2.8,y)] if separate else [(-4.15,y)]
        for pos in positions: g.add(cell(GREY,.86,pos))
        for j,name in enumerate(['Piezo1','Piezo2']):
            x=positions[j][0] if separate else -4.15
            yy=y if separate else y+(.36 if j==0 else -.36)
            label=lab(name,x,yy,GREEN,28); g.add(label)
            deleted=state==3 or state==j+1
            if deleted:
                g.add(Line(label.get_corner(UL),label.get_corner(DR),color=RED,stroke_width=5),
                    Line(label.get_corner(DL),label.get_corner(UR),color=RED,stroke_width=5))
            else:
                start=[x+.88,yy,0] if separate else [-3.25,yy,0]
                end=[-.6,y,0]
                if separate and j==0:
                    pts=[[x,y-.87,0],[x,-2.7,0],[-.6,-2.7,0],[-.6,y,0]]
                    route=VMobject(color=GREEN,stroke_width=4).set_points_as_corners(pts)
                    path=VGroup(route,arr([-.6,-2.15,0],end,GREEN))
                    motion=route.copy()
                else:
                    path=arr(start,end,GREEN);motion=Line(start,end)
                path.set_stroke(opacity=.55 if state else 1)
                g.add(path); paths.append(motion)
        g.add(lab('No input' if state==3 else ('Reflex retained' if state else 'Input'),-.4,y+.6,RED if state==3 else GREEN,28))
    return g,paths


def bracket(x,y1,y2,color=PINK):
    return VGroup(Line([x,y1,0],[x,y2,0],color=color,stroke_width=4),
        *[Line([x-.13,y,0],[x+.13,y,0],color=color,stroke_width=4) for y in [y1,y2]])


class S00Title(TitleCard):
    TITLE='Which Channel, and What the Test Can Prove'
    LESSON='Vagal Sensory Neurons: The Body Reports to the Brain'

    def construct(self):
        brand=lab('BIOCHEMISTRYPEDIA',0,2.3,TEAL,22)
        lesson=lab(self.LESSON,0,1.55,GREY,24)
        title=T('Which Channel,\nand What the Test Can Prove',size=46,font=TITLE_FONT).move_to([0,-.1,0])
        rule=Line([-1.2,-1.6,0],[1.2,-1.6,0],color=GOLD,stroke_width=4)
        self.play(FadeIn(brand),FadeIn(lesson),run_time=.4)
        self.play(FadeIn(title),GrowFromCenter(rule),run_time=.65)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        p=patch(); self.add(p,lab('Which channel turns stretch into current?',0,3.15,PINK,34),
            lab('membrane',-4,1.25,GREY,30),lab('Force-gated channel (closed)',0,-1.25,GREEN,32),lab('?',0,.5,PINK,56))
        self.at('stretch has to')
        self.play(GrowArrow(arr([-2.3,2,0],[-5.5,2,0])),GrowArrow(arr([2.3,2,0],[5.5,2,0])),FadeIn(lab('stretch',0,2.05,GREY,30)),run_time=.5)
        self.at('electrical current somewhere')
        self.play(FadeIn(lab('Force → electrical current?',0,-2.2,PINK,34)),run_time=.4)
        self.at('how would a deletion')
        self.play(FadeIn(lab('What would deletion prove?',0,-3.2,n=32)),run_time=.4)
        self.finish()


class S02Channel(SpokenScene):
    def construct(self):
        q=questions(1.7); self.add(q,lab('Three experimental questions',0,3.2,n=34))
        self.at('this is the second')
        self.play(q[0].animate.set_opacity(.35),q[2].animate.set_opacity(.35),q[1][0].animate.set_fill(GREEN,opacity=.3),run_time=.4)
        self.at('deleting a channel')
        a=VGroup(arr([-.8,1,0],[-3,-.1,0],GREEN),box(-3,-1.45,5.4,2.5,GREEN),lab('Deletion',-3,-.8,GREEN,32),lab('Tests requirement',-3,-1.65,n=30))
        self.play(FadeIn(a),run_time=.4)
        self.at('showing that it converts')
        b=VGroup(arr([.8,1,0],[3,-.1,0],GREEN),box(3,-1.45,5.4,2.5,GREEN),lab('Current recordings',3,-.8,GREEN,32),lab('Test transduction',3,-1.65,n=30),lab('Force → current',3,-2.3,GREY,28))
        self.play(FadeIn(b),run_time=.5)
        self.finish()


class S03Open(SpokenScene):
    def construct(self):
        p=patch(y=1.3);self.add(p,lab('Force-gated channel',0,3.25,GREEN,32),
            lab('outside',-4,2.5,GREY,28),lab('inside',-4,.2,GREY,28))
        self.at('force can open')
        self.play(Transform(p,patch(True,1.3)),GrowArrow(arr([-2,2.6,0],[-3.1,2.6,0])),
            GrowArrow(arr([2,2.6,0],[3.1,2.6,0])),FadeIn(lab('stretch',0,2.6,GREY,28)),run_time=.45)
        self.at('inward current')
        ions=VGroup(*[Dot([x,2.2,0],radius=.09,color=GREEN) for x in [-.25,0,.25]])
        self.add(ions)
        self.play(ions.animate.shift(DOWN*2.2),FadeIn(lab('Inward current (Na+/Ca2+)',3.6,.15,GREEN,28)),GrowArrow(arr([0,1,0],[0,-.5,0],GREEN)),run_time=.5)
        ax=Axes(x_range=[0,1,.5],y_range=[0,1,1],x_length=4.2,y_length=1.65,tips=False,axis_config={'include_ticks':False,'color':GREY}).move_to([-3.6,-1.8,0])
        bx=ax.copy().move_to([3.4,-1.8,0])
        self.add(ax,bx,lab('Membrane potential',-3.6,-.65,GREY,28),lab('Membrane potential',3.4,-.65,GREY,28),lab('Time →',-3.6,-3,GREY,28),lab('Time →',3.4,-3,GREY,28))
        self.at('depolarizes the terminal')
        self.play(Create(ax.plot(lambda t:.8*(1-np.exp(-4*t)),x_range=[0,1,.01],color=GREEN)),run_time=.4)
        self.at('if it reaches threshold')
        self.play(Create(DashedLine(ax.c2p(0,.6),ax.c2p(1,.6),color=PINK)),FadeIn(lab('threshold',-.3,-1.25,PINK,28)),run_time=.3)
        self.at('the afferent fires')
        self.play(GrowArrow(arr([-1.2,-2.25,0],[.8,-2.25,0],GREEN)),Create(bx.plot(lambda t:.9*sum(np.exp(-((t-m)/.018)**2) for m in [.2,.5,.8]),x_range=[0,1,.004],color=GREEN)),FadeIn(lab('Schematic excitation',0,-3.5,GREY,28)),run_time=.4)
        self.finish()


class S04Lung(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,8,2],y_range=[-1,1,1],x_length=6.9,y_length=2.8,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([2,.1,0])
        control=wave(ax,amp=.85)
        self.add(lung(),ax,control,lab('Lung inflation reflex',0,3.2,n=34),lab('Control: inflation reflex',2,1.9,GREY,30),lab('Schematic reflex response',2,-1.75,GREY,28),lab('Time →',2,-2.4,GREY,28))
        self.at('deleting')
        self.play(FadeIn(lab('Piezo2 deleted',-4.5,-2.4,GREEN,30)),run_time=.35)
        self.at('in adult mouse sensory neurons')
        self.play(FadeIn(lab('Adult mouse sensory neurons',0,-3.3,GREEN,30)),run_time=.35)
        self.at('impaired the lung')
        self.play(control.animate.set_stroke(opacity=.3),Create(wave(ax,amp=.14,color=RED)),FadeIn(lab('Deleted: reflex impaired',2,2.55,RED,30)),run_time=.45)
        self.finish()


class S05Lung2(SpokenScene):
    def construct(self):
        self.add(box(-3.35,0,5.65,6.7),box(3.1,0,6.05,6.7),lab('Deletion: requirement',-3.35,2.85,GREEN,30),lab('Light: activation',3.1,2.85,TEAL,30),lung(-3.35,.15).scale(.65),lab('Piezo2 required for',-3.35,-1.6,GREEN,28),lab('inflation reflex',-3.35,-2.15,GREEN,28),lab('Adult sensory neurons',-3.35,-2.9,GREY,28))
        cells=VGroup(*[cell(GREEN,.68,(x,.9)) for x in [1.5,3.1,4.7]])
        ax=Axes(x_range=[0,8,2],y_range=[-1,1,1],x_length=4.7,y_length=1.1,tips=False,axis_config={'include_ticks':False,'color':GREY}).move_to([3.1,-1.4,0])
        tr=wave(ax,.8,GREEN)
        self.add(cells,ax,tr,lab('Piezo2-positive vagal neurons',3.1,-.15,GREEN,28))
        self.at('and driving')
        self.play(Create(Line([3.1,2.4,0],[3.1,1.75,0],color=TEAL,stroke_width=10)),run_time=.25)
        self.at('with light')
        self.play(*[GrowArrow(arr([x,1.9,0],[x,1.45,0],TEAL)) for x in [1.5,3.1,4.7]],run_time=.3)
        self.at('caused apnea')
        self.play(Transform(tr,wave(ax,0,RED)),FadeIn(lab('Apnoea',3.1,-2.15,RED,32)),run_time=.35)
        self.at('that uses')
        self.play(FadeIn(lab('Population-activation sufficiency',3.1,-2.85,GREY,28)),FadeIn(lab('Genetic handle',4.6,2.2,PINK,28)),run_time=.35)
        self.finish()


class S06Artery(SpokenScene):
    def construct(self):
        vessel=VGroup(box(0,1.1,11.1,1.65),box(0,1.1,11.1,1.2,RED))
        theta=np.linspace(0,2*np.pi,240)
        heart=VMobject(color=RED,fill_color=RED,fill_opacity=.4).set_points_as_corners([
            [16*np.sin(t)**3/16,(13*np.cos(t)-5*np.cos(2*t)-2*np.cos(3*t)-np.cos(4*t))/16,0] for t in theta]).close_path().move_to([-4.5,-1.9,0])
        self.add(vessel,heart,lab('Artery',0,3.25,n=34),lab('Heart',-4.5,-3.25,GREY,30),lab('Schematic baroreflex',2,-.9,GREY,28),lab('Schematic',2,-2.4,GREY,28))
        rate=ValueTracker(2.4);phase=[0.];previous=[1.]
        def pulse(mob,dt):
            phase[0]+=dt*rate.get_value()*2*np.pi
            scale=1+.16*np.sin(phase[0])
            mob.scale(scale/previous[0]);previous[0]=scale
            mob.set_fill(opacity=.45+.3*max(0,np.sin(phase[0])))
        heart.add_updater(pulse)
        self.at('the reflex by which')
        self.play(FadeIn(lab('Baroreflex',0,2.9,GREEN,32)),run_time=.3)
        self.at('a rise in blood pressure')
        self.play(vessel.animate.stretch(1.55,1),FadeIn(lab('Pressure rises',0,1.1,RED,34)),GrowArrow(arr([-.6,-.22,0],[-3.35,-1.7,0],GREEN)),run_time=.4)
        self.at('slows the heart')
        self.play(rate.animate.set_value(.7),FadeIn(lab('Heart rate falls',2,-3.1,GREEN,34)),run_time=.3)
        self.finish()


class S07Setup(SpokenScene):
    def construct(self):
        self.add(lab('Drug-evoked baroreflex assay',0,3.2,n=34),cell(GREY,.9,(-4.4,1.5)),cell(GREY,.9,(-1.8,1.5)),lab('Nodose',-4.4,1.5,n=28),lab('Petrosal',-1.8,1.5,n=28))
        axes=[]
        for x,name in [(-3.5,'Pressure'),(3.5,'Heart rate')]:
            a=Axes(x_range=[0,1,.5],y_range=[0,1,.5],x_length=4.5,y_length=1.7,tips=False,axis_config={'include_ticks':False,'color':GREY}).move_to([x,-1.6,0]);axes.append(a)
            self.add(a,lab(name,x,-.4,GREY,28),lab('Time →',x,-2.85,GREY,28))
        self.at('channels were deleted')
        # Deletion is a gene manipulation; ganglion names remain intact.
        deletion=lab('Piezo1 / Piezo2 gene deletion',-3.1,.05,GREEN,28)
        self.play(FadeIn(deletion),run_time=.4)
        self.at('blood pressure was raised')
        syringe=VGroup(Rectangle(width=1.6,height=.65,color=GREY).move_to([3.4,1.5,0]),Line([4.2,1.5,0],[5.3,1.5,0],color=GREY),Line([2.6,1.5,0],[2,1.5,0],color=GREY),Line([2,1.15,0],[2,1.85,0],color=GREY),lab('Drug injection',3.4,2.6,GREY,28))
        self.play(FadeIn(syringe),FadeIn(lab('Raises blood pressure',3.4,.45,GREEN,28)),run_time=.4)
        self.at('with a drug')
        self.add(lab('Control mouse • schematic assay response',0,-3.5,TEXT,28))
        self.play(Create(axes[0].plot(lambda t:.1+.8*t,x_range=[0,1,.02],color=GREEN)),Create(axes[1].plot(lambda t:.9-.8*t,x_range=[0,1,.02],color=GREEN)),run_time=.5)
        self.at('in anesthetized mice')
        self.play(FadeIn(lab('Anaesthetized mice',0,-3.05,GREY,24)),run_time=.3)
        self.finish()


class S08Single1(SpokenScene):
    def construct(self):
        self.add(table(1,False))
        self.at('no statistically detectable difference')
        self.play(FadeIn(lab('no statistically detectable difference',1.65,-.16,n=28)),run_time=.25)
        self.finish()


class S09Single2(SpokenScene):
    def construct(self):
        self.add(table(2,False))
        self.at('no statistically detectable difference')
        self.play(FadeIn(lab('no statistically detectable difference',1.65,-1.07,n=28)),run_time=.25)
        self.finish()


class S10Beat1(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(table());self.wait(3)


class S11Double(SpokenScene):
    def construct(self):
        tb=table(3,False);self.add(tb)
        self.at('essentially abolished')
        result=lab('essentially abolished',1.65,-1.98,RED,28)
        self.play(FadeIn(result),run_time=.25)
        self.at('the magnitude of its sensitivity')
        self.play(FadeOut(tb),FadeOut(result),run_time=.15)
        self.play(FadeIn(measured()),FadeIn(lab('Zeng and colleagues • Science 2018',0,3.65,GREY,28)),run_time=.35)
        self.finish()


class S12Conscious(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,1,.5],y_range=[80,120,20],x_length=9.9,y_length=4.4,tips=False,axis_config={'color':GREY}).move_to([-.45,-.1,0])
        self.add(ax,lab('Conscious mice • telemetry',0,3.25,n=34),lab('Mean arterial pressure (mmHg)',0,2.55,GREY,28),lab('Time across one day →',0,-2.9,GREY,28),lab('Schematic day trace; labels give reported active-period means',0,-3.5,GREY,28))
        for v in [80,100,120]:self.add(T(str(v),size=28,color=GREY).next_to(ax.c2p(0,v),LEFT,buff=.13))
        # Synthetic illustration anchored at reported active-period means.
        # No clock-hour assignment or invented recorded telemetry is implied.
        control=ax.plot(lambda t:95+1.8*np.sin(4*np.pi*t)+.6*np.sin(18*np.pi*t),x_range=[0,1,.004],color=GREY,stroke_width=4)
        ko=ax.plot(lambda t:112+1.8*np.sin(4*np.pi*t)+.6*np.sin(18*np.pi*t),x_range=[0,1,.004],color=GREEN,stroke_width=4)
        self.add(control,lab('95 mmHg',.5,ax.c2p(.6,95)[1]+.35,GREY,28),lab('Control',-3.8,-.05,GREY,28))
        self.at('in conscious double knockouts')
        self.play(Create(ko),FadeIn(lab('112 mmHg',.5,ax.c2p(.6,112)[1]+.35,GREEN,28)),FadeIn(lab('Double KO',-3.5,1.8,GREEN,28)),run_time=.4)
        self.at('the active period')
        shade=Polygon(ax.c2p(.4,80),ax.c2p(.8,80),ax.c2p(.8,120),ax.c2p(.4,120),fill_color=PINK,fill_opacity=.12,stroke_width=0).set_z_index(-1)
        self.play(FadeIn(shade),FadeIn(lab('active-period',.5,-1.3,PINK,28)),FadeIn(lab('means',.5,-1.85,PINK,28)),run_time=.4)
        self.finish()


class S13Predict(SpokenScene):
    def construct(self):
        a,_=choices();self.add(a,evidence(),lab('Do the data choose a cellular picture?',0,3.4,PINK,32))
        self.at('carries both channels')
        self.play(Circumscribe(a[2],color=PINK),run_time=.4)
        self.at('predict')
        self.play(FadeIn(lab('Predict: which picture?',-3.1,-3.2,PINK,30)),run_time=.3)
        self.finish()


class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;a,_=choices();self.add(a,evidence(),lab('Pause. Which picture do the data choose?',0,3.4,PINK,32))
        rail=Line([-5.8,-3.3,0],[.7,-3.3,0],color=GREY,stroke_width=8)
        progress=Line([-5.8,-3.3,0],[-5.79,-3.3,0],color=PINK,stroke_width=8)
        self.add(rail,progress);self.play(Transform(progress,Line([-5.8,-3.3,0],[.7,-3.3,0],color=PINK,stroke_width=8)),run_time=5,rate_func=linear)


class S15Reveal1(SpokenScene):
    def construct(self):
        a,_=choices();self.add(a,evidence(),lab('Compatible with both • requires an input assumption',0,3.4,PINK,30))
        self.at('it does not follow')
        label=lab('Piezo1 deleted',-3.25,-3.25,GREEN,30)
        b,paths=choices(1);self.play(Transform(a,b),FadeIn(label),run_time=.2)
        dots=VGroup(*[Dot(p.get_start(),radius=.09,color=GREEN) for p in paths]);self.add(dots)
        self.play(*[MoveAlongPath(d,p) for d,p in zip(dots,paths)],run_time=.6);self.remove(dots)
        self.at('either picture could fit')
        b,paths=choices(2);self.play(Transform(a,b),Transform(label,lab('Piezo2 deleted',-3.25,-3.25,GREEN,30)),run_time=.2)
        dots=VGroup(*[Dot(p.get_start(),radius=.09,color=GREEN) for p in paths]);self.add(dots)
        self.play(*[MoveAlongPath(d,p) for d,p in zip(dots,paths)],run_time=.6);self.remove(dots)
        self.at('if the input that remains')
        self.play(Transform(label,lab('Remaining input could sustain reflex',-3.1,-3.25,GREEN,28)),run_time=.3)
        self.wait(.6)
        b,_=choices(3);self.play(Transform(a,b),Transform(label,lab('Both deleted: no input remains',-3.1,-3.25,RED,28)),run_time=.4)
        self.finish()


class S16Saturate(SpokenScene):
    def construct(self):
        ax,c,l=curve_panel();self.add(ax,l)
        self.at('a nonlinear relation')
        self.play(Create(c),run_time=1.1)
        self.at('this curve is a hypothesis')
        self.play(Indicate(l[1],color=PINK),run_time=.4)
        self.finish()


class S17Half(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,1,.5],y_range=[0,5,1],x_length=7.3,y_length=4.3,tips=False,axis_config={'color':GREY}).move_to([-2,-.05,0])
        c=ax.plot(model,x_range=[0,1,.005],color=PINK,stroke_width=5)
        l=VGroup(ticks(ax,[0,.5,1],[0,1,3,5]),lab('Illustrative model • not measured',0,3.2,PINK,32),lab('Magnitude (bpm/mmHg)',-2,2.55,GREY,28),lab('Hypothetical input fraction',-2,-2.8,GREY,28))
        self.add(ax,c,l,lab('Neither establishes detectability in the published single KOs',0,-3.5,PINK,28))
        self.at('on this chosen curve')
        d=Dot(ax.c2p(1,5),color=PINK);self.add(d)
        self.at('the input costs')
        self.play(d.animate.move_to(ax.c2p(.5,model(.5))),Create(DashedLine(ax.c2p(.5,0),ax.c2p(.5,model(.5)),color=PINK)),run_time=.4)
        y5=ax.c2p(1,5)[1]; yh=ax.c2p(.5,model(.5))[1]
        drop_label=T('1.23 drop',size=28,color=PINK).next_to([2.15,(y5+yh)/2,0],RIGHT,buff=.28)
        self.play(Create(bracket(2.15,y5,yh)),FadeIn(drop_label),
            FadeIn(lab('5.00',1.2,y5+.25,PINK,28)),
            FadeIn(lab('3.77',1.2,yh-.25,PINK,28)),run_time=.3)
        self.at('an illustrative cutoff')
        cutoff=2*np.sqrt(.5**2+.5**2);dy=cutoff*ax.y_length/5
        cutoff_top=.2
        cutoff_label=T('1.41\n(illustrative cutoff)',size=28,color=GOLD,line_spacing=.85).next_to([2.15,cutoff_top-dy/2,0],RIGHT,buff=.28)
        note=Paragraph('Hypothetical groups', 'Independent • SEM 0.5 each',
            'Cutoff: 2 standard errors',alignment='left',font=FONT,font_size=25,
            color=GREY,line_spacing=.7).move_to([4.35,-2.25,0])
        self.play(Create(bracket(2.15,cutoff_top,cutoff_top-dy,GOLD)),
            FadeIn(cutoff_label),FadeIn(note),run_time=.4)
        self.finish()


class S18All(SpokenScene):
    def construct(self):
        ax,c,l=curve_panel(hedge=False);self.add(ax,c,l)
        self.at('losing all of it')
        d=Dot(ax.c2p(1,5),color=PINK);self.add(d)
        self.play(MoveAlongPath(d,c.copy().reverse_points()),run_time=.9)
        self.at('the measured drop')
        ax2,c2,l2=curve_panel(compact=True,hedge=False)
        self.play(Transform(ax,ax2),Transform(c,c2),Transform(l,l2),d.animate.move_to(ax2.c2p(0,0)),FadeIn(measured(True)),run_time=.45)
        self.finish()


class S19Beat2(Scene):
    def construct(self):
        self.camera.background_color=BG;ax,c,l=curve_panel(True,False)
        self.add(ax,c,l,Dot(ax.c2p(0,0),color=PINK),measured(True));self.wait(3.5)


class S20Sum(SpokenScene):
    def construct(self):
        a,_=choices();self.add(a,evidence(),lab('Collective channel requirement',0,3.4,GREEN,34))
        self.at('it does not measure')
        self.play(Create(VMobject(color=PINK).set_points_as_corners([[-5.9,-2.8,0],[-5.9,-2.95,0],[.4,-2.95,0],[.4,-2.8,0]])),run_time=.3)
        self.at('or prove')
        self.play(FadeIn(lab('Both still need further tests',-3,-3.45,PINK,30)),run_time=.3)
        self.finish()


class S21Next(SpokenScene):
    def construct(self):
        self.add(lab('Tests that separate the cellular pictures',0,3.3,n=34),box(-3.25,-.15,5.7,5.9),box(3.25,-.15,5.7,5.9),lab('Per-cell measurement',-3.25,2.3,GREEN,30),lab('Delivered force',3.25,2.3,PINK,30))
        c=cell(GREY,.72,(-3.25,.45));target=cell(GREY,.72,(3.25,.45))
        self.add(c,target,lab('Identified baroreceptor',-3.25,1.6,GREY,28),
            lab('Identified baroreceptor',3.25,-.65,GREY,28))
        # A single aligned checklist keeps the three measurements grouped.
        def item(text,y,color):
            lines=VGroup(*[T(line,size=26,color=color) for line in text.split('\n')])
            lines.arrange(DOWN,aligned_edge=LEFT,buff=.12)
            lines.move_to([-5.4,y,0],aligned_edge=LEFT)
            return VGroup(Dot([-5.65,lines[0].get_y(),0],radius=.05,color=color),lines)
        self.at('measure channel expression')
        self.play(FadeIn(item('Channel expression',-.9,GREEN)),
            FadeIn(item('Verified single-channel\ndeletion',-1.65,GREY)),run_time=.35)
        self.at('and mechanosensitive current')
        # Pipette tip terminates exactly on the upper-right cell membrane.
        tip=c.get_center()+np.array([.72/np.sqrt(2),.72/np.sqrt(2),0])
        pipette=VGroup(Line(tip,[-1.1,1.3,0],color=GREEN,stroke_width=5),
            Line(tip,[-1.1,1.05,0],color=GREEN,stroke_width=5))
        self.play(Create(pipette),FadeIn(item('Current recording',-2.4,GREEN)),run_time=.4)
        self.at('under controlled mechanical stimulation')
        # No arrow buffer: applied force visibly reaches the membrane.
        force=Arrow([3.25,1.95,0],target.get_top(),buff=0,color=PINK,stroke_width=5,tip_length=.2)
        self.play(GrowArrow(force),FadeIn(lab('Controlled force',3.25,-1.65,PINK,30)),run_time=.5)
        self.finish()


class S22Take(SpokenScene):
    def construct(self):
        self.add(lab('What the reflex tests establish',0,3.35,n=34))
        # Question chips on the right; evidence connects directly to its question.
        for y,name in [(2,'Stimulus'),(.5,'Channel'),(-1,'Output')]:
            self.add(chip(name,PINK,30).move_to([4.9,y,0]))
        lungtext=VGroup(lab('Lung: Piezo2 required',-2.8,2.15,GREEN,30),lab('Inflation reflex • adult sensory neurons',-2.8,1.45,GREY,28))
        artery=VGroup(lab('Artery: Piezo1 and Piezo2 together',-2.3,-.3,GREEN,30),lab('Required collectively in targeted population',-2.3,-1,GREY,28))
        self.at('the channels are required collectively')
        self.play(FadeIn(lungtext),FadeIn(artery),run_time=.35)
        lung_start=lungtext[0].get_right()+RIGHT*.12
        artery_start=artery[0].get_right()+RIGHT*.12
        junction=np.array([2.5,lung_start[1],0])
        self.play(Create(Line(lung_start,junction,color=GREEN,stroke_width=5)),
            GrowArrow(arr(junction,[3.65,.65,0],GREEN)),
            GrowArrow(arr(junction,[3.9,-.85,0],GREEN)),
            GrowArrow(arr(artery_start,[3.65,.35,0],GREEN)),run_time=.35)
        self.at('the result does not show')
        self.play(FadeIn(lab('Both in each neuron? Further tests needed.',-1,-2,GREY,30)),run_time=.3)
        self.at('that each neuron carries both')
        handle=VGroup(Arc(radius=.28,start_angle=0,angle=PI,color=PINK),Line([-.28,0,0],[-.28,-.3,0],color=PINK),Line([.28,0,0],[.28,-.3,0],color=PINK)).move_to([3.05,-3,0])
        handle.set_stroke(PINK,width=5,opacity=1)
        handle_label=lab('Genetic handle',.65,-3,PINK,30).set_opacity(1)
        handle_note=lab('× touches none',5.15,-3,PINK,30).set_opacity(1)
        self.add(handle,handle_label,handle_note)
        self.finish()


class S23End(EndCard):
    LINE='These channels are required collectively in the targeted population.'

    def construct(self):
        self.add(lab('These channels are required collectively\nin the targeted population.',0,.45,n=40),lab('biochemistrypedia.com',0,-1,TEAL,28))
        self.finish()
