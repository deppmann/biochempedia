"""Chapter 2 revision. COLOR MAP: BLUE #7C9CFF P2ry1/protection;
YELLOW Npy2r; GREEN PIEZO2/stretch; RED suppressed inspiration;
TEAL light; PINK prediction; GREY anatomy. All traces are model-generated,
qualitative schematics, never experimental recordings or quantitative counts.
"""
import numpy as np
from bp_style import *
BLUE = '#7C9CFF'
PINK = '#E58BC4'
GREY = '#D2D7E0'


def label(s,x=0,y=3.1,color=TEXT,size=30):
    return T(s,size=size,color=color,line_spacing=0.8).move_to([x,y,0])


def left(s,x,y,c=TEXT,size=26):
    return label(s,0,y,c,size).align_to([x,y,0],LEFT)


def arr(a,b,c=GREY):
    return Arrow(a,b,buff=.12,color=c,stroke_width=5,max_tip_length_to_length_ratio=.16)


def cell(c=GREY,r=.42,pos=(0,0)):
    return Circle(radius=r,color=c,stroke_width=4,fill_color=c,fill_opacity=.12).move_to([*pos,0])


def breathing(x,w,y,rapid=False,halt=True,cutshort=False,amp=.55):
    # Integrated phase oscillator from the reference film. For inflation the
    # rising half-cycle is terminated early and relaxes exponentially; rhythm
    # subsequently resumes. This is a qualitative model, not recorded data.
    pts=[]
    for t in np.linspace(0,8,641):
        z=amp*np.sin(np.pi*t)
        if cutshort:
            onset=2.25
            if onset<=t<4:
                z=amp*np.sin(np.pi*onset)*np.exp(-7*(t-onset))
            elif t>=4:
                z=amp*np.sin(np.pi*(t-4))
        elif t>=4:
            z=.22*np.sin(2*np.pi*(t-4)/.8) if rapid else (0 if halt else z)
        pts.append([x+w*t/8,y+z,0])
    return VMobject(stroke_color=YELLOW if rapid else RED if halt or cutshort else GREY,stroke_width=5).set_points_as_corners(pts)


def stimulus(x,w,y,on=4,c=TEAL,text='light on'):
    start=x+w*on/8
    return VGroup(Line([start,y,0],[x+w,y,0],color=c,stroke_width=8),label(text,(start+x+w)/2,y-.36,c,34))


def lungs(x=0,y=0,scale=1):
    g=VGroup(*[Ellipse(width=1.25,height=2.7,color=GREY,fill_color=GREEN,fill_opacity=.10).move_to([d,0,0]) for d in [-.73,.73]],
      Line([0,2,0],[0,.8,0],color=GREY,stroke_width=8),
      Line([0,.8,0],[-.65,.3,0],color=GREY,stroke_width=6),Line([0,.8,0],[.65,.3,0],color=GREY,stroke_width=6))
    return g.scale(scale).move_to([x,y,0])


def opt_panel(x,c,name,result=False,rapid=False):
    nerve=RoundedRectangle(width=5.7,height=1.65,corner_radius=.35,color=GREY,fill_opacity=.07).move_to([x,.95,0])
    axons=VGroup(*[Line([x-2.6,.95+d,0],[x+2.6,.95+d,0],color=c,stroke_width=6) for d in [-.48,0,.48]])
    beam=VGroup(Line([x,2.6,0],[x,1.95,0],color=TEAL,stroke_width=9),Polygon([x,1.95,0],[x-.9,.2,0],[x+.9,.2,0],stroke_width=0,fill_color=TEAL,fill_opacity=.2),
       label('light',x+1.15,2.25,TEAL,34),Line([x+.65,2.12,0],[x+.1,1.95,0],color=TEAL))
    g=VGroup(label(name,x,2.95,c,28),nerve,axons,beam)
    if result:
        g.add(breathing(x-2.65,5.3,-1.1,rapid=rapid),stimulus(x-2.65,5.3,-2.05),
          label('rapid, shallow' if rapid else 'breathing suppressed',x,-2.95,YELLOW if rapid else RED,27))
    return g


def opt_title():
    return label('First: compare populations with light drive',0,3.55,TEXT,30)


def both_opt():
    return VGroup(opt_title(),opt_panel(-3.25,BLUE,'P2ry1 afferents',True),opt_panel(3.25,YELLOW,'Npy2r afferents',True,True),label('Anaesthetized mice • schematic breathing vs time →',0,-3.55,GREY,34))


def fibres(names=True):
    g=VGroup(label('Independent nerve recordings',0,3.4,TEXT,32))
    for x,c,my in [(-3.3,BLUE,True),(3.3,YELLOW,False)]:
        ax=RoundedRectangle(width=5.4,height=.5,corner_radius=.2,color=c,fill_color=c,fill_opacity=.4).move_to([x,.7,0])
        if my:
            sheath=VGroup(*[RoundedRectangle(width=.75,height=1.25,corner_radius=.18,color=GREY,fill_color=GREY,fill_opacity=.4).move_to([x+d,.7,0]) for d in [-1.9,-.95,0,.95,1.9]])
        else: sheath=VGroup()
        electrode=VGroup(Line([x+.45,2.2,0],[x+.45,1.45,0],color=TEXT,stroke_width=4),arr([x+.45,1.45,0],[x+.15,.7,0]),label('electrode',x+1.3,2.3,GREY,34))
        g.add(VGroup(ax,sheath,electrode))
        if names:
            g.add(label('A fibre • myelinated' if my else 'C fibre • unmyelinated',x,-.55,c,27),label('P2ry1: largely A' if my else 'Npy2r: largely C',x,2.9,c,27))
    g.add(label('conduction speed (schematic; no numeric scale)',0,-2.5,GREY,34))
    return g


def speed(x,c,fast):
    w=4.8 if fast else 1.4
    return VGroup(Line([x-2.5,-1.4,0],[x+2.5,-1.4,0],color=GREY),Rectangle(width=w,height=.32,fill_color=c,fill_opacity=1,stroke_width=0).move_to([x-2.5+w/2,-1.4,0]),label('fast' if fast else 'slow',x,-1.98,c,34))


def program():
    rows=VGroup()
    for y,s in [(1.35,'apnoea'),(.25,'vocal folds close'),(-.85,'swallowing'),(-1.95,'expiratory reflexes')]:
        rows.add(VGroup(left(s,-1.65,y,BLUE,30)))
    rows[0].add(Line([-4.8,1.35,0],[-2.8,1.35,0],color=RED,stroke_width=6))
    for x,d in [(-4.5,1),(-3.1,-1)]:
        rows[1].add(Polygon([x,.65,0],[x,-.15,0],[x+d*.6,.25,0],color=BLUE,fill_color=BLUE,fill_opacity=.5))
    rows[2].add(Arc(radius=.45,start_angle=PI/2,angle=PI,color=BLUE).move_to([-4,-.8,0]),arr([-3.6,-.45,0],[-3.6,-1.25,0],BLUE))
    rows[3].add(arr([-4.6,-1.95,0],[-3,-1.95,0],BLUE),*[Arc(radius=r,start_angle=-PI/4,angle=PI/2,color=BLUE).move_to([-2.7+r*.25,-1.95,0]) for r in [.22,.42]])
    return rows


# Fixed blue rings always mean P2RY1 labelling. Counts are illustrative only.
POS=[(-3,1.25),(0,1.25),(3,1.25),(-3,-.85),(0,-.85),(3,-.85)]
LABELLED=[1,2,5]
RESPONDERS=[0,1,3,4]

def field():
    boundary=RoundedRectangle(width=10.8,height=5.5,corner_radius=.55,color=GREY).move_to([0,.25,0])
    cells=VGroup(*[cell(GREY,.52,p) for p in POS])
    rings=VGroup(*[Circle(radius=.65,color=BLUE,stroke_width=5).move_to([*POS[i],0]) for i in LABELLED])
    return VGroup(boundary,cells,rings)


def key():
    return VGroup(Circle(radius=.16,color=BLUE,stroke_width=4).move_to([-5.6,-2.87,0]),left('P2RY1 label',-5.25,-2.87,BLUE,34),
       Dot([.4,-2.87,0],radius=.15,color=GREEN),left('responds to inflation',.75,-2.87,GREEN,34),label('Schematic cells • counts are illustrative',0,-3.5,GREY,34))


def predicted():
    return VGroup(*[DashedVMobject(Circle(radius=.42,color=PINK).move_to([*POS[i],0]),num_dashes=12) for i in LABELLED])


def observed():
    f=field()
    for i in RESPONDERS: f[1][i].set_fill(GREEN,.8).set_stroke(GREEN)
    tags=VGroup(*[label('PIEZO2+',*([POS[i][0],POS[i][1]-.88]),GREEN,34) for i in RESPONDERS])
    return VGroup(f,tags,key(),label('Most responders: PIEZO2+ / P2RY1−',0,3.35,GREEN,31))


def prediction():
    # Smaller neutral field leaves room for airway cuff, but no answer is shown.
    f=field(); f.remove(f[2]); f.scale(.65).move_to([1.8,.35,0])
    l=lungs(-4.5,.4,.95)
    cuff=Rectangle(width=.8,height=.3,color=GREEN,stroke_width=6).move_to([-4.5,2,0])
    return VGroup(label('Predict: inflation imaging',0,3.35,PINK,32),f,l,cuff,label('inflation cuff',-4.5,-1.9,GREEN,34),label('Which cells light up?',0,-2.65,PINK,30),label('What label do they carry?',0,-3.3,PINK,30))


class S00Title(TitleCard):
    LESSON='Vagal Sensory Neurons: The Body Reports to the Brain'
    TITLE='Two Ways to Stop Breathing'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.6,TEAL,34),label('Vagal Sensory Neurons',0,1.5,GREY,32),label(self.TITLE,0,0,TEXT,48),Line([-2,-1,0],[2,-1,0],color=GOLD),label('Inflation • airway protection',0,-2,GREY,30))
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        self.add(label('Two Ways to Stop Breathing',0,3.35,TEXT,36))
        starts=VGroup(chip('Inflation',GREEN,32).move_to([-4.2,1.65,0]),chip('Laryngeal irritant',BLUE,30).move_to([-4.2,-1.3,0]))
        self.add(starts,label('First: light-drive contrast   →   Then: inflation vs protection',0,-3.6,GREY,28))
        self.at('end with')
        self.play(Create(VGroup(arr([-2.6,1.65,0],[-.5,.1,0],GREEN),arr([-2.1,-1.3,0],[-.5,.1,0],BLUE))),Create(breathing(0,5.7,0,amp=.85)),run_time=.6)
        self.add(label('inspiration halted',2.9,-1.7,RED,30))
        self.at('same line')
        self.play(FadeIn(label('Same line, used twice?',0,-3,PINK,34)),FadeIn(label('?',.2,1.8,PINK,64)),run_time=.35)
        self.finish()


class S02Opt1(SpokenScene):
    def construct(self):
        # Full-width preparation initially; matched panels for direct comparison.
        p=opt_panel(0,BLUE,'P2ry1 afferents')
        p[1].stretch(2,0); p[2].stretch(2,0)
        self.add(opt_title(),p[0],p[1],p[2],label('breathing',-4.85,-.2,GREY,34),Line([-5.9,-1.8,0],[5.9,-1.8,0],color=GREY),label('Anaesthetized mice • schematic breathing vs time →',0,-3.55,GREY,34))
        self.at('light on')
        self.play(FadeIn(p[3]),run_time=.4)
        self.at('suppressed breathing')
        self.play(Create(breathing(-5.9,11.8,-1.1)),FadeIn(stimulus(-5.9,11.8,-2.05)),FadeIn(label('breathing suppressed',0,-2.95,RED,27)),run_time=.55)
        self.finish()


class S03Opt2(SpokenScene):
    def construct(self):
        p=opt_panel(3.25,YELLOW,'Npy2r afferents')
        self.add(opt_title(),opt_panel(-3.25,BLUE,'P2ry1 afferents',True),p,label('Anaesthetized mice • schematic breathing vs time →',0,-3.55,GREY,34))
        self.at('light on')
        self.play(Indicate(p[3],color=TEAL),run_time=.4)
        self.at('rapid shallow')
        self.play(Create(breathing(.6,5.3,-1.1,rapid=True)),FadeIn(stimulus(.6,5.3,-2.05)),FadeIn(label('rapid, shallow',3.25,-2.95,YELLOW,27)),run_time=.6)
        self.finish()


class S04Beat1(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(both_opt()); self.wait(3)


class S05Logic(SpokenScene):
    def construct(self):
        g=both_opt(); self.add(g)
        self.at('this is sufficiency')
        self.play(Transform(g[0],label('Sufficiency: what light drive can do',0,3.55,TEAL,30)),run_time=.4)
        self.at('it says')
        self.play(Transform(g[-1],label('?  Natural stimulus: unknown here',0,-3.55,PINK,29)),run_time=.4)
        self.finish()


class S06Fibres(SpokenScene):
    def construct(self):
        self.add(fibres(False))
        self.at('one population')
        self.play(GrowFromEdge(speed(-3.3,BLUE,True),LEFT),run_time=.5)
        self.at('the other')
        self.play(GrowFromEdge(speed(3.3,YELLOW,False),LEFT),run_time=.5)
        self.finish()


class S07Fibres2(SpokenScene):
    def construct(self):
        self.add(fibres(False))
        self.at('a fibers')
        self.play(FadeIn(label('A fibre • myelinated',-3.3,-.55,BLUE,27)),FadeIn(label('P2ry1: largely A',-3.3,2.9,BLUE,27)),run_time=.4)
        self.at('conduct quickly')
        self.play(GrowFromEdge(speed(-3.3,BLUE,True),LEFT),run_time=.4)
        self.at('c fibers')
        self.play(FadeIn(label('C fibre • unmyelinated',3.3,-.55,YELLOW,27)),FadeIn(label('Npy2r: largely C',3.3,2.9,YELLOW,27)),run_time=.4)
        self.at('conduct slowly')
        self.play(GrowFromEdge(speed(3.3,YELLOW,False),LEFT),run_time=.4)
        self.finish()


class S08Fibres3(SpokenScene):
    def construct(self):
        a,b=speed(-3.3,BLUE,True),speed(3.3,YELLOW,False)
        self.add(fibres(),a,b)
        self.at('most of one')
        self.play(Indicate(a,color=BLUE),run_time=.5)
        self.at('most of the other')
        self.play(Indicate(b,color=YELLOW),run_time=.5)
        self.at('not proof')
        self.play(FadeIn(label('Predominant types; complete separation unproven',0,-3.3,PINK,28)),run_time=.4)
        self.finish()
        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)),run_time=.25)
        self.add(label('Keep P2ry1 in mind.',0,1,BLUE,38),label('Now: two routes that both halt inspiration.',0,-.5,TEXT,34))
        self.wait(3)


class S09Inflation(SpokenScene):
    def construct(self):
        l=lungs(-3.6,.3,1.25)
        self.add(label('Two routes to one output: inflation',0,3.35,TEXT,32),l,label('lungs',-3.6,-2.45,GREY,28),label('schematic breathing',2.5,2.35,GREY,28),Line([-.4,-1.3,0],[6,-1.3,0],color=GREY),label('time →',3,-2.5,GREY,34))
        self.at('first inflation')
        self.play(FadeIn(arr([-5.9,-1,0],[-5.9,1.6,0],GREEN)),FadeIn(label('volume ↑',-4.8,2.9,GREEN,28)),run_time=.4)
        self.at('when the lungs')
        self.play(l.animate.stretch(1.4,0),run_time=.7)
        self.at('further inspiration')
        tr=breathing(-.4,6.4,.2,cutshort=True,amp=1)
        self.play(Create(tr),FadeIn(stimulus(-.4,6.4,-1.55,2.25,GREEN,'inflation on')),run_time=.55)
        self.add(label('inspiration cut short',2.7,1.65,RED,29),arr([1.4,1.4,0],[1.5,.75,0],RED))
        self.finish()


def hb_panel(x):
    l=lungs(x,1.05,.86)
    vagi=VGroup(*[Line([x+d,2.45,0],[x+d,.05,0],color=GREEN,stroke_width=7) for d in [-1.8,1.8]])
    g=VGroup(l,vagi,label('vagus',x-2.05,-.3,GREEN,34),label('vagus',x+2.05,-.3,GREEN,34),label('intact input',x,2.85,TEXT,28),breathing(x-2.6,5.2,-1.3,cutshort=True,amp=.5),stimulus(x-2.6,5.2,-2.1,2.25,GREEN,'inflation on'),label('inspiration interrupted',x,-3,RED,27))
    return g


class S10Hb(SpokenScene):
    def construct(self):
        a,b=hb_panel(-3.25),hb_panel(3.25)
        self.add(label('Hering–Breuer inflation reflex',0,3.55,TEXT,32),a,b)
        self.at('cut both',lead=2.2)
        cuts=VGroup(*[Line([3.25+d-.25,.8,0],[3.25+d+.25,1.5,0],color=RED,stroke_width=9) for d in [-1.8,1.8]])
        self.play(Create(cuts),Transform(b[4],label('both vagi interrupted',3.25,2.85,TEXT,28)),FadeOut(b[5]),FadeOut(b[7]),run_time=.5)
        self.play(Create(breathing(.65,5.2,-1.3,halt=False,amp=.5).set_color(RED)),FadeIn(label('feedback absent',3.25,-3,TEXT,34)),run_time=.4)
        self.finish()


class S11Protect(SpokenScene):
    def construct(self):
        airway=VGroup(RoundedRectangle(width=3.5,height=5.1,corner_radius=1,color=GREY,fill_opacity=.04).move_to([0,.2,0]),Ellipse(width=2.7,height=3.6,color=GREY).move_to([0,.2,0]))
        folds=VGroup(Polygon([-1.3,1,0],[-1.3,-1,0],[-.3,-.1,0],color=BLUE,fill_color=BLUE,fill_opacity=.55),Polygon([1.3,1,0],[1.3,-1,0],[.3,-.1,0],color=BLUE,fill_color=BLUE,fill_opacity=.55))
        self.add(label('Protection: laryngeal irritant',0,3.35,BLUE,34),airway,folds,label('larynx',3.7,.6,GREY,30),Line([2.7,.6,0],[1.75,.6,0],color=GREY),label('not lung stretch',3.9,-1.6,GREEN,28))
        self.at('water or acid')
        drops=VGroup(cell(TEAL,.23,(-.5,1.7)),cell(YELLOW,.23,(.5,1.7)))
        water_line=Line([-3,2,0],[-.75,1.7,0],color=TEAL)
        acid_line=Line([3.3,2,0],[.75,1.7,0],color=YELLOW)
        self.play(FadeIn(drops),FadeIn(label('water',-4,2,TEAL,28)),Create(water_line),FadeIn(label('acid',4,2,YELLOW,28)),Create(acid_line),run_time=.4)
        self.play(drops.animate.shift(DOWN*1.1),water_line.animate.put_start_and_end_on([-3,2,0],[-.75,.6,0]),acid_line.animate.put_start_and_end_on([3.3,2,0],[.75,.6,0]),run_time=.6)
        self.at('protective reflexes')
        self.play(folds[0].animate.shift(RIGHT*.3),folds[1].animate.shift(LEFT*.3),run_time=.5)
        self.at('keep the airway')
        self.play(FadeIn(label('Which afferents sense it?',0,-2.8,PINK,30)),FadeIn(label('A separate measurement',0,-3.45,GREY,27)),run_time=.35)
        self.finish()


class S12Program(SpokenScene):
    def construct(self):
        self.add(label('P2ry1 afferents • light drive',0,3.35,BLUE,32))
        driver=VGroup(*[cell(BLUE,.6,(x,.4)) for x in [-2,0,2]])
        lamp=VGroup(chip('light',TEAL,34).move_to([0,2.6,0]),Polygon([-.2,2.2,0],[-3,-.3,0],[3,-.3,0],[.2,2.2,0],stroke_width=0,fill_color=TEAL,fill_opacity=.18))
        source=VGroup(driver,lamp,label('P2ry1 afferents',0,-1.1,BLUE,34))
        self.add(source)
        self.at('with lite')
        self.play(driver.animate.set_fill(BLUE,.8),run_time=.3)
        rows=program()
        # Crossfade directly to the program: no empty frame between the views.
        # Begin at light drive and let successive rows build across the last 3 s.
        self.play(FadeOut(source),FadeIn(rows[0]),run_time=.45)
        for row in rows[1:]:
            self.play(FadeIn(row,shift=DOWN*.15),run_time=.6)
        self.at('not apnea alone')
        self.play(Indicate(rows[0],color=RED,scale_factor=1.03),run_time=.35)
        self.finish(); self.wait(2)


class S13Necessity(SpokenScene):
    def construct(self):
        rows=program().shift(DOWN*.2)
        for i in [0,1,3]:
            rows[i].set_color(GREY)
            rows[i].add(left('not tested',3.5,rows[i][0].get_y(),GREY,34))
        cells=VGroup(*[cell(BLUE,.23,(x,2.3)) for x in [-.7,0,.7]])
        self.add(label('Cell ablation: one tested reflex',0,3.4,TEXT,32),label('P2ry1',3.2,2.3,BLUE,28),Line([1.45,2.3,0],[2.5,2.3,0],color=BLUE),Ellipse(width=2.9,height=1.1,color=GREY).move_to([0,2.3,0]),cells,rows)
        self.at('ablating those cells')
        # Briefly show the labelled starting state even though the verb begins at t=0.
        self.wait(.25)
        self.play(FadeOut(cells),run_time=.65)
        self.at('impaired swallowing')
        self.play(rows[2].animate.set_color(GREY),FadeIn(left('impaired',3.5,-1.05,BLUE,34)),FadeIn(label('Laryngeal water / acid',0,-2.8,BLUE,27)),run_time=.4)
        self.at('that is necessity')
        self.play(FadeIn(label('Necessity • that assay, age and driver',0,-3.4,PINK,28)),run_time=.4)
        self.finish()


class S14Predict(SpokenScene):
    def construct(self):
        # Preview the empty field while the prior result is recalled, so the
        # prediction question never competes with the previous answer list.
        pred=prediction()
        self.add(pred)
        self.at('needs them',lead=0)
        # Predict is missing from the forced alignment; its spoken interval is
        # in the pause before If (7.10 s). The field is already ready to inspect.
        self.wait(max(0,5.5-self.elapsed()))
        self.play(Indicate(pred[0],color=PINK,scale_factor=1.03),run_time=.4)
        self.at('what would inflation')
        self.play(Indicate(pred[-2],color=PINK,scale_factor=1.03),run_time=.4)
        self.finish()


class S15Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        p=prediction(); p[0].become(label('Pause and predict',0,3.35,PINK,32))
        self.add(p)
        for remaining in range(5,0,-1):
            count=label(str(remaining),5.65,2.25,PINK,48)
            self.add(count); self.wait(1); self.remove(count)


class S16Reveal1(SpokenScene):
    def construct(self):
        self.add(field(),key(),label('Prediction: one population does both?',0,3.35,PINK,32))
        self.at('the inflation responders')
        self.play(Create(predicted()),run_time=.5)
        self.at('inside the labeled set')
        self.play(FadeIn(label('Dashed pink = predicted responders',0,2.5,PINK,34)),run_time=.4)
        self.finish()


class S17Reveal2(SpokenScene):
    def construct(self):
        f=field(); d=predicted()
        title=label('Prediction: one population does both?',0,3.35,PINK,32)
        self.add(f,d,key(),title)
        self.at('they did not')
        self.play(FadeOut(d),Transform(title,label('Observed: inflation responses',0,3.35,TEXT,32)),*[f[1][i].animate.set_fill(GREEN,.8).set_stroke(GREEN) for i in RESPONDERS],run_time=.55)
        self.at('most stretch responsive neurons')
        self.play(Transform(title,label('Most responders: PIEZO2+ / P2RY1−',0,3.35,GREEN,31)),run_time=.4)
        self.at('were')
        self.play(FadeIn(VGroup(*[label('PIEZO2+',POS[i][0],POS[i][1]-.88,GREEN,34) for i in RESPONDERS])),run_time=.4)
        self.finish()


class S18Beat2(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(observed()); self.wait(3)


class S19Caveat(SpokenScene):
    def construct(self):
        gang=Ellipse(width=3.3,height=5.1,color=GREY).move_to([-1,0,0])
        cells=VGroup(*[cell(GREY,.34,(-1+d,y)) for d in [-.6,.6] for y in [-1,0,1]])
        l=lungs(4.3,.2,1.28)
        nerve=Line([.65,0,0],[l[0].get_left()[0],0,0],color=GREY,stroke_width=7)
        nerve.add_updater(lambda m: m.put_start_and_end_on([.65,0,0],[l[0].get_left()[0],0,0]))
        self.add(label('Imaging preparation',0,3.4,TEXT,34),gang,cells,l,label('ganglion imaged',-1,-2.9,GREY,28),Line([-6,0,0],[-2.65,0,0],color=GREY,stroke_width=7),nerve,label('to brainstem',-4.5,-.65,GREY,34),label('from\nlungs',1.6,-.95,GREY,34))
        self.at('central connections severed')
        self.play(Create(Line([-4.7,-.4,0],[-4.1,.4,0],color=RED,stroke_width=8)),FadeIn(label('central\nconnections cut',-4.6,1.25,RED,27)),run_time=.45)
        self.at('under')
        self.play(FadeIn(label('under isoflurane',-1,-3.4,GREY,28)),run_time=.4)
        self.at('with the airway')
        self.play(l.animate.stretch(1.25,0),FadeIn(label('inflation in vivo',4.35,-2.65,GREEN,27)),run_time=.6)
        self.finish()


def comparison():
    # Wider gutter gives row names air. The secondary caveat is 22 pt. All cell content is text, not burned-in narration.
    headers=VGroup(label('Protection afferents',-1.6,3.35,BLUE,30),label('Stretch afferents',3.65,3.35,GREEN,30))
    rows=VGroup()
    data=[
      ('CHALLENGE',2.15,'Laryngeal water / acid','Lung inflation\nResponsive afferents imaged'),
      ('HANDLE',.95,'P2ry1-labelled cells','PIEZO2-positive,\nP2RY1-negative'),
      ('OUTPUT\n(driven)',-.18,'Apnoea + airway defence','Apnoea: broader Piezo2-\nlabelled population;\nseparate experiment'),
      ('CELL\nABLATION',-1.4,'Water / acid swallowing\nimpaired','No matched ablation of this\nexact subset specified here'),
      ('CHANNEL\nLOSS /\nSCOPE',-2.75,'P2X2/P2X3 double loss:\nsome laryngeal swallowing ↓\nnot P2ry1-cell-specific','Adult sensory-neuron\nPiezo2 deletion impairs\ninflation reflex')]
    def compact(s,x,y,c):
        return T(s,size=26,color=c,line_spacing=.45).move_to([0,y,0]).align_to([x,y,0],LEFT)
    for name,y,a,b in data:
        row=VGroup(compact(name,-6.5,y,GREY),compact(a,-3.8,y,BLUE),compact(b,1.35,y,GREEN))
        if name=='CHALLENGE':
            row[1].set_y(2.6)
            row.add(left('Ablation: reflex contribution;\nnot direct transduction',-3.8,1.88,'#AEB6C4',22))
        rows.add(row)
    rules=VGroup(Line([1,3,0],[1,-3.45,0],color=GREY,stroke_width=1),*[Line([-6.2,y,0],[6.3,y,0],color=GREY,stroke_opacity=.3) for y in [1.45,.43,-.86,-2.02]])
    return VGroup(headers,rows,rules)


class S20Table(SpokenScene):
    def construct(self):
        g=comparison(); self.add(g[0],g[2])
        self.at('two challenges')
        self.play(FadeIn(g[1][0]),FadeIn(g[1][1]),run_time=.45)
        self.at('one shared output')
        self.play(FadeIn(g[1][2]),run_time=.4)
        self.at('the table')
        self.play(FadeIn(g[1][3]),FadeIn(g[1][4]),run_time=.4)
        self.finish(); self.wait(12)


class S21Take(SpokenScene):
    def construct(self):
        self.add(label('Same output, different pathways',0,3.4,TEXT,36),label('Laryngeal challenge',-3.35,2.5,BLUE,30),label('Lung inflation',3.35,2.5,GREEN,30))
        a=VGroup(cell(BLUE,.7,(-3.35,.7)),label('P2ry1-labelled',-3.35,-.4,BLUE,30))
        b=VGroup(cell(GREEN,.7,(3.35,.7)),label('PIEZO2-positive',3.35,-.4,GREEN,30))
        self.add(a,b)
        self.at('an output alone')
        self.play(Create(arr([-3.35,-.9,0],[-1,-2,0],BLUE)),Create(arr([3.35,-.9,0],[1,-2,0],GREEN)),FadeIn(chip('apnoea',RED,32).move_to([0,-2,0])),run_time=.5)
        self.add(label('Output of light drive • separate experiments',0,-2.9,GREY,27))
        self.at('measure stimulus')
        self.play(FadeIn(label('Measure stimulus and output separately.',0,-3.55,TEXT,29)),run_time=.4)
        self.finish()


class S22End(EndCard):
    LINE='An output alone does not identify which pathway produced it.'
    def construct(self):
        self.add(label('An output alone does not identify',0,.6,TEXT,38),label('which pathway produced it.',0,-.3,TEXT,38),label('biochemistrypedia.com',0,-1.6,TEAL,34))
        self.finish()
