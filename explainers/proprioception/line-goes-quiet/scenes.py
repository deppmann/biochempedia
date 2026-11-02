"""Chapter 3: When the Line Goes Quiet.
COLOR MAP: BLUE stretch input / sensory neurons; YELLOW joint limits / effort;
RED deletion / deficit; GREY anatomy / inactive input; WHITE vision;
ORANGE position estimate. Anatomical silhouettes and reach paths are schematic.
Reach paths use a deterministic motor-error model, not measured patient data.
"""
import numpy as np
from bp_style import *
ORANGE = '#F29E4C'

class TimedScene(SpokenScene):
    def at(self, phrase, lead=0, nth=0):
        super().at(phrase, lead=lead, nth=nth)

def heading(s):
    return T(s, 34, font=TITLE_FONT).move_to([0, 3.1, 0])

def eye(closed=False):
    if closed:
        return VGroup(Line([-.8,0,0],[.8,0,0],color=TEXT,stroke_width=6))
    return VGroup(Ellipse(width=1.6,height=.85,color=TEXT,stroke_width=4),Dot(radius=.24,color=TEXT))

def arm(end=(2.65,-.65,0)):
    return VGroup(Line([-5,-1.7,0],[-2,-1.7,0],color=GREY,stroke_width=24),
        Line([-2,-1.7,0],end,color=GREY,stroke_width=24),
        Circle(radius=.23,color=TEXT,fill_color=BG,fill_opacity=1).move_to([-2,-1.7,0]),
        Circle(radius=.28,color=TEXT,fill_color=GREY,fill_opacity=.5).move_to(end))

def cup():
    return VGroup(Polygon([2.9,-.4,0],[4.2,-.4,0],[4.05,-1.9,0],[3.05,-1.9,0],color=TEXT,fill_color=TEXT,fill_opacity=.12,stroke_width=4),
        Rectangle(width=.5,height=.7,color=TEXT).move_to([4.4,-.95,0]))

def stretch():
    return VMobject(color=GREY,stroke_width=6).set_points_as_corners([[-5,-1.3,0],[-2,-1.3,0],[2.4,-.3,0]])

def room(miss=False,dark=False):
    border=Rectangle(width=12,height=6.2,color=GREY,fill_color='#020309' if dark else '#27251E',fill_opacity=1).move_to([0,0,0])
    glow=Circle(radius=1.25,color=YELLOW,stroke_opacity=0,fill_color=YELLOW,fill_opacity=.02 if dark else .12).move_to([0,1.7,0])
    lamp=VGroup(Line([0,3.1,0],[0,2.2,0],color=GREY),Polygon([-.5,1.7,0],[.5,1.7,0],[.25,2.2,0],[-.25,2.2,0],color=GREY if dark else YELLOW,fill_color=YELLOW,fill_opacity=.05 if dark else .7))
    c=cup(); a=arm((5,.2,0) if miss else (2.65,-.65,0)); w=stretch()
    if dark: c.set_opacity(.25); a.set_opacity(.3); w.set_stroke(opacity=.25)
    return VGroup(border,glow,lamp,c,a,w)

def question():
    backdrop=VGroup(arm(),eye().move_to([-3,1.6,0])).set_opacity(.18)
    q=VGroup(T('What does most of the work',40,font=TITLE_FONT),T('for the silent line?',40,font=TITLE_FONT)).arrange(DOWN,buff=.3).move_to([0,.2,0])
    return VGroup(backdrop,q,T('Think',28,YELLOW).move_to([0,-2.55,0]),Line([-3,-3.05,0],[3,-3.05,0],color=YELLOW,stroke_width=3))

def person():
    head=Circle(radius=.4,color=GREY).move_to([0,2.1,0])
    torso=RoundedRectangle(width=1.05,height=1.65,corner_radius=.2,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([0,.8,0])
    limbs=VGroup(*[Line(a,b,color=GREY,stroke_width=12) for a,b in [([-.5,1.4,0],[-.95,-.3,0]),([.5,1.4,0],[.95,-.3,0]),([-.27,0,0],[-.48,-2,0]),([.27,0,0],[.48,-2,0])]])
    return VGroup(head,VGroup(torso,limbs))

def spine(curved=False,x=0,height=4.7):
    # Qualitative single-C silhouette; not a CT reconstruction or quantitative trace.
    verts=VGroup()
    for u in np.linspace(-1,1,18):
        dx=.85*(1-u*u) if curved else 0
        verts.add(RoundedRectangle(width=.6,height=height/21,corner_radius=.04,color=GREY,fill_color=GREY,fill_opacity=.75,stroke_width=1).move_to([x+dx,u*height/2,0]))
    return verts

def neuron():
    return VGroup(Circle(radius=.8,color=BLUE,fill_color=BLUE,fill_opacity=.2),
        Line([.8,0,0],[2.1,0,0],color=BLUE,stroke_width=7),
        *[Line([-.6,y/3,0],[-1.3,y,0],color=BLUE,stroke_width=6) for y in (-1,1)]).move_to([-3.2,.1,0])

def nonauto():
    n=neuron().stretch_to_fit_height(3.9).stretch_to_fit_width(4.4).move_to([-2.6,.1,0])
    s=spine(True,1.65,height=4.4).shift(UP*.1)
    link=Arrow([-.2,.1,0],[1.3,.1,0],color=GREY,buff=.05,stroke_width=4)
    return VGroup(n,s,link,chip('Piezo2 lost',RED,28).move_to([-2.6,2.35,0]),
        T('Parvalbumin-labelled neurons',26,BLUE).move_to([-2.6,-2.15,0]),
        T('Skeleton',28).move_to([4.15,.1,0]))

def definition_card():
    return chip('Defect appears in the skeleton\nGene lost in parvalbumin-labelled neurons',TEXT,26,
                fill_opacity=.04).move_to([0,-3.05,0])

class S00Title(TitleCard):
    LESSON="Proprioception: Sensing the Body's Own Position"
    TITLE='When the Line Goes Quiet'
    def construct(self):
        self.play(FadeIn(T('BIOCHEMISTRYPEDIA',26,TEAL).move_to([0,2.3,0])),run_time=.35)
        self.play(FadeIn(T('Proprioception:\nSensing the Body’s Own Position',28,GREY).move_to([0,1,0])),run_time=.45)
        self.play(FadeIn(T(self.TITLE,46,font=TITLE_FONT).move_to([0,-.8,0])),Create(Line([-1.2,-1.7,0],[1.2,-1.7,0],color=GOLD)),run_time=.7)
        self.finish()

class S01Q(TimedScene):
    def construct(self):
        w=Line([-5,-2.3,0],[5,-2.3,0],color=BLUE,stroke_width=12)
        self.add(heading('When the Line Goes Quiet'),person().scale(.4).move_to([0,-.95,0]).set_opacity(.25))
        self.at('what happens')
        self.play(FadeIn(T('What happens to a person when\nproprioceptive input is lost?',38,font=TITLE_FONT).move_to([0,.8,0])),Create(w),run_time=.6)
        self.at('input is lost')
        self.play(w.animate.set_color(GREY),run_time=.4)
        self.finish()

class S02Dark(TimedScene):
    def construct(self):
        r=room()
        # Raise and enlarge the reach; retain the lit-room context.
        target=arm().scale(1.2).shift(UP*.9)
        r[4].become(arm((-.4,0,0)).scale(1.2).shift(UP*.9))
        r[3].scale(1.2).shift(UP*.9)
        wire=stretch().scale(1.2).shift(UP*.9).set_stroke(GREY,width=12)
        r[5].become(wire)
        self.add(r)
        self.at('picture reaching')
        self.play(Transform(r[4],target),run_time=1.1)
        self.at('stretch lines silent')
        self.play(Indicate(r[5],color=GREY),
                  FadeIn(T('Stretch line: silent',32,GREY).move_to([-1.8,-2.45,0])),run_time=.45)
        self.finish()

class S03Predict(TimedScene):
    def construct(self):
        q=question(); self.add(q[0])
        self.at('predict')
        self.play(FadeIn(q[2]),run_time=.3)
        self.at('what would you')
        self.play(FadeIn(q[1]),Create(q[3]),run_time=.5)
        self.finish()

class S04Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question()); self.wait(5)

class S05Reveal(TimedScene):
    def construct(self):
        r=room(); e=eye().move_to([-3.7,1.4,0]); self.add(r)
        self.at('mainly your eyes')
        self.play(FadeIn(e),run_time=.5)
        self.at('vision does much')
        self.play(FadeIn(T('Vision',30).move_to([-3.7,2.25,0])),run_time=.35)
        self.at('take it away')
        dark=room(dark=True)
        self.play(Transform(r,dark),Transform(e,eye(True).move_to(e)),run_time=.6)
        self.at('reaching becomes')
        self.play(Transform(r[4],arm((5,.2,0)).set_opacity(.3)),run_time=.8)
        self.at('less accurate')
        self.play(FadeIn(T('×',46,RED).move_to([5,.65,0])),FadeIn(T('Misses the cup',28,RED).move_to([3.8,1.4,0])),run_time=.35)
        self.finish()

class S06Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(room(True,True),eye(True).move_to([-3.7,1.4,0]),T('Vision',30).move_to([-3.7,2.25,0]),T('×',46,RED).move_to([5,.65,0]),T('Misses the cup',28,RED).move_to([3.8,1.4,0])); self.wait(2)

class S07Chesler(TimedScene):
    def construct(self):
        self.add(heading('Chesler and colleagues · 2016'))
        p=VGroup(person().move_to([-3,0,0]),person().move_to([3,0,0]))
        self.add(p.set_opacity(.22))
        self.at('two unrelated young people')
        self.play(p.animate.set_opacity(1),run_time=.6)
        self.at('inactivating variants')
        self.play(p.animate.set_color(RED),run_time=.4)
        self.at('both copies')
        self.play(FadeIn(VGroup(*[chip('PIEZO2: both copies\ninactivating variants',RED,26).move_to([x,-2.9,0]) for x in (-3,3)])),run_time=.45)
        self.finish()

# Reaching model: forward progress plus a decaying transverse motor error.
# Sight reduces error gain; blocked sight increases it and adds endpoint bias.
def reach_path(y,blocked=False):
    t=np.linspace(0,1,161); gain=1.0 if blocked else .12
    x=-5+9.4*t+(1.0*t*t if blocked else 0)
    z=y+gain*np.sin(5*np.pi*t)*np.sin(np.pi*t/2)+(1.1*t*t if blocked else 0)
    return VMobject(color=RED if blocked else TEXT,stroke_width=6).set_points_as_corners(np.column_stack([x,z,np.zeros_like(t)]))

class S08Tests(TimedScene):
    def construct(self):
        self.add(heading('Reaching with and without sight'),T('Schematic motor-error model',26,GREY).move_to([0,-3.15,0]))
        good=reach_path(1.25); bad=reach_path(-1.6,True)
        targets=VGroup(*[Circle(radius=.3,color=TEXT,stroke_width=4).move_to([4.4,y,0]) for y in (1.25,-1.6)])
        self.add(targets,Dot([-5,1.25,0],color=GREY),Dot([-5,-1.6,0],color=GREY))
        self.at('with and without sight')
        self.play(Create(good),run_time=.6)
        self.play(FadeIn(T('With sight',28).move_to([-3.5,1.95,0])),run_time=.3)
        self.at('without vision')
        self.play(Create(bad),run_time=.9)
        self.at('uncoordinated movements')
        self.play(FadeIn(T('Sight blocked · Ataxia',28,RED).move_to([-2.9,-.4,0])),FadeIn(T('Uncoordinated movement',26,RED).move_to([-2.9,-2.5,0])),run_time=.4)
        self.at('misjudged reaches')
        end=bad.get_end()
        bracket=VGroup(Line([4.4,-1.6,0],[5.4,-1.6,0],color=RED),Line([5.4,-1.6,0],end,color=RED),Dot(end,color=RED))
        self.play(Create(bracket),FadeIn(T('Dysmetria:\nmisjudged reach',26,RED).move_to([2.6,-2.55,0])),run_time=.45)
        self.finish()

class S09Still(TimedScene):
    def construct(self):
        walk=person().move_to([-4,0,0])
        talk=VGroup(RoundedRectangle(width=2.7,height=2.1,corner_radius=.25,color=GREY),Polygon([-.8,-1.05,0],[-1.2,-1.6,0],[-.1,-1.05,0],color=GREY)).move_to([0,.2,0])
        write=VGroup(Rectangle(width=2.4,height=2.7,color=GREY),Line([-.6,-.7,0],[.8,.8,0],color=TEXT,stroke_width=15)).move_to([4,0,0])
        self.add(walk.set_opacity(.3))
        self.at('still walk')
        self.play(walk.animate.set_opacity(1),FadeIn(T('Walk',30).move_to([-4,2.7,0])),run_time=.3)
        self.at('talk and write')
        self.play(FadeIn(talk),FadeIn(write),FadeIn(T('Talk',30).move_to([0,2.7,0])),FadeIn(T('Write',30).move_to([4,2.7,0])),run_time=.5)
        self.at('only with support')
        cane=VGroup(Arc(radius=.25,start_angle=0,angle=PI,color=TEXT).move_to([-2.9,-.2,0]),Line([-2.65,-.2,0],[-2.65,-2.1,0],color=TEXT,stroke_width=6),Line([-3.1,.1,0],[-2.9,-.2,0],color=GREY,stroke_width=9))
        self.play(Create(cane),FadeIn(T('One walked only with support',28).move_to([0,-2.95,0])),run_time=.4)
        self.finish()

class S10Iw(TimedScene):
    def construct(self):
        p=person().scale(1.25).move_to([3.6,0,0]); self.add(p)
        self.at('an older case')
        self.play(FadeIn(T('I.W.\nCole and Sedgwick\n1992',36,font=TITLE_FONT).move_to([-2.8,1,0])),run_time=.5)
        self.at('had lost')
        self.play(p[1].animate.set_color(RED),run_time=.6)
        self.at('below the neck')
        lab=T('Large-fibre sensation\nlost below the neck',30,RED).move_to([-2.7,-1.3,0])
        self.play(FadeIn(lab),Create(Line([.3,-1.3,0],[2.9,-.7,0],color=RED)),run_time=.45)
        self.finish()

class S11Kept(TimedScene):
    def construct(self):
        self.add(*[RoundedRectangle(width=5.3,height=5.4,color=c,fill_color=c,fill_opacity=.06).move_to([x,0,0]) for x,c in ((-3,RED),(3,TEXT))],T('Lost',34,RED).move_to([-3,2,0]),T('Kept',34).move_to([3,2,0]))
        for cue,label,x,y,c in [('light touch','Light touch',-3,.7,RED),('position sense','Position sense',-3,-.5,RED),('he kept pain','Pain',3,.7,TEXT),('temperature','Heat and cold',3,-.5,TEXT),('muscle fatigue','Muscle fatigue',3,-1.7,TEXT)]:
            self.at(cue); self.play(FadeIn(T(label,30,c).move_to([x,y,0])),run_time=.3)
        self.finish()

class S12Watch(TimedScene):
    def construct(self):
        a=arm((-.4,.2,0)).scale(1.1).shift(UP*.4); e=eye().move_to([-.4,2.1,0])
        link=DashedLine([-.4,1.7,0],[-.4,.7,0],color=TEXT)
        self.add(a,e,link)
        self.at('in testing')
        self.play(Transform(a,arm((2.3,-.6,0)).scale(1.1).shift(UP*.4)),e.animate.shift(RIGHT*2.7),link.animate.shift(RIGHT*2.7),run_time=1.6)
        self.at('no new movement')
        self.play(Transform(e,eye(True).move_to(e)),FadeOut(link),run_time=.15)
        self.at('without watching it')
        self.play(FadeIn(T('New movement needs vision',34).move_to([0,-2.2,0])),FadeIn(T('Can hold a posture or repeat a simple movement',26).move_to([0,-3,0])),run_time=.4)
        self.at('every new movement')
        self.play(Transform(e,eye().move_to(e)),run_time=.2)
        self.play(Transform(a,arm((.5,.6,0)).scale(1.1).shift(UP*.4)),e.animate.shift(LEFT*1.8),run_time=.9)
        self.finish()

class S13Rule(TimedScene):
    def construct(self):
        self.add(heading('The guiding idea · two parts'))
        first=VGroup(RoundedRectangle(width=11.8,height=1.4,color=GREY,fill_opacity=0),T('Stretch line signals limb position',30,GREY)).move_to([0,1.7,0])
        box=RoundedRectangle(width=11.8,height=3.25,color=GREY,fill_color=TEXT,fill_opacity=.03).move_to([0,-.9,0])
        e=eye().scale(1.5).move_to([-4,-.9,0]); self.add(first,box,e)
        self.at('second half')
        self.play(box.animate.set_stroke(YELLOW,width=4),run_time=.4)
        self.at('proprioceptive input lost')
        self.play(FadeIn(T('With proprioceptive input lost',30,RED).move_to([1.1,0,0])),run_time=.4)
        self.at('accurate movement')
        self.play(FadeIn(T('Accurate movement',34).move_to([1.1,-.85,0])),run_time=.4)
        self.at('depends heavily on vision')
        self.play(FadeIn(T('depends heavily on vision',32).move_to([1.1,-1.65,0])),Indicate(e,color=TEXT),run_time=.5)
        self.at('neither case silences')
        self.play(FadeIn(T('Neither case silences spindles alone',26).move_to([0,-2.95,0])),run_time=.35)
        self.at('touch was affected')
        self.play(FadeIn(T('Touch was affected too',26).move_to([0,-3.5,0])),run_time=.3)
        self.finish()

class S14Skeleton(TimedScene):
    def construct(self):
        spindle=VGroup(RoundedRectangle(width=3.7,height=2,corner_radius=.8,color=GREY),Ellipse(width=.65,height=1.9,color=BLUE,stroke_width=7),Line([0,.9,0],[1.4,1.5,0],color=BLUE,stroke_width=6)).move_to([-3.6,.2,0])
        s=spine(False,3,height=5.2)
        self.add(spindle,heading('In mice'))
        self.at('the line turned')
        self.play(FadeIn(T('Spindle:\nthe stretch line',30,BLUE).move_to([-3.6,-2,0])),run_time=.4)
        self.at('the skeleton too')
        self.play(FadeIn(s),Create(DashedLine([-1.4,.3,0],[2.3,.3,0],color=GREY)),FadeIn(T('?',42).move_to([.4,1,0])),FadeIn(T('Spine',28).move_to([4.4,-1.9,0])),run_time=.5)
        self.finish()

class S15Curve(TimedScene):
    def construct(self):
        left=spine(False,-2.8); right=spine(False,2.2)
        self.add(left,right,T('Control',30).move_to([-2.8,3,0]),T('Schematic silhouettes',26,GREY).move_to([-3.4,-3.45,0]))
        self.at('deleting')
        self.play(FadeIn(T('Pvalb-Cre\nPiezo2 deletion',28,RED).move_to([2.6,3,0])),run_time=.5)
        self.at('curved the spine')
        self.play(Transform(right,spine(True,2.2)),run_time=.85)
        self.at('some mice')
        self.play(FadeIn(T('Some animals',26,RED).move_to([3,-2.85,0])),run_time=.35)
        self.at('postnatal day')
        self.play(FadeIn(T('P60',30).move_to([.12,-2.9,0])),run_time=.35)
        self.finish()

class S16Collagen(TimedScene):
    def construct(self):
        left=spine(False,-4.7,height=3.8).shift(DOWN*.6)
        right=spine(True,4,height=3.8).shift(DOWN*.6)
        middle=spine(False,0,height=3.8).shift(DOWN*.6)
        self.add(left,right,T('Control',28).move_to([-4.7,2.65,0]),T('Pvalb-Cre\nPiezo2 deletion',26,RED).move_to([4.5,2.65,0]),T('Schematic\nsilhouettes',26,GREY).move_to([-4.7,-3.15,0]))
        self.at('deleting it')
        self.play(FadeIn(T('Col1a1-Cre / Col2a1-Cre',26).move_to([0,3.15,0])),FadeIn(middle),run_time=.4)
        self.at('bone and cartilage')
        self.play(FadeIn(T('Piezo2 deletion in bone\nand cartilage lineages',26,RED).move_to([0,2.25,0])),run_time=.4)
        self.at('did not curve')
        self.play(FadeIn(T('No spinal curve',28).move_to([0,-2.95,0])),run_time=.4)
        self.at('at the ages tested')
        self.play(FadeIn(T('At the ages tested',26).move_to([0,-3.5,0])),run_time=.35)
        self.finish()

class S17Nonauto(TimedScene):
    def construct(self):
        g=nonauto(); neutral=spine(False,1.65,height=4.4).shift(UP*.1)
        self.add(heading('The authors’ interpretation'),g[0],g[3],neutral)
        self.at('this as')
        self.play(FadeIn(T('Non-autonomous',30,YELLOW).move_to([2.7,2.65,0])),run_time=.4)
        self.at('curve shows in the skeleton')
        self.play(Create(g[2]),Transform(neutral,g[1]),FadeIn(g[5]),FadeIn(definition_card()[0]),
                  FadeIn(T('Defect appears in the skeleton',26).move_to([0,-2.8,0])),run_time=.7)
        self.at('the gene was lost')
        self.play(Indicate(g[3],color=RED),run_time=.5)
        self.at('parvalbumin')
        self.play(FadeIn(g[4]),FadeIn(T('Gene lost in parvalbumin-labelled neurons',26).move_to([0,-3.3,0])),run_time=.45)
        self.finish()

class S18Open(TimedScene):
    def construct(self):
        g=nonauto(); self.add(g,heading('The authors’ interpretation'))
        self.at('how the signal')
        self.play(Transform(g[2],DashedLine([-.2,.1,0],[1.3,.1,0],color=GREY,stroke_width=4).add_tip(tip_length=.18)),FadeIn(T('?',110,YELLOW).move_to([.55,1.15,0])),run_time=.4)
        self.at('not known')
        self.play(FadeIn(chip('How the signal reaches the skeleton: not known',TEXT,28,fill_opacity=.04).move_to([0,-3.05,0])),run_time=.4)
        self.finish()

class S19Limits(TimedScene):
    def construct(self):
        self.add(heading('Limits of the stretch rule'))
        left=RoundedRectangle(width=5.6,height=5.4,color=GREY).move_to([-3,-.3,0])
        joint=VGroup(
            Line([-5.25,-1.15,0],[-3.15,-1.15,0],color=GREY,stroke_width=30),
            Line([-3.15,-1.15,0],[-3.65,1.05,0],color=GREY,stroke_width=30),
            Circle(radius=.32,color=YELLOW,stroke_width=4).move_to([-3.15,-1.15,0]),
            *[Arc(radius=r,start_angle=.1,angle=1.4,color=YELLOW,stroke_width=3)
              .move_arc_center_to([-3.15,-1.15,0]) for r in (.75,1.0,1.25)],
            # Short transverse marks show stretched skin over the bent joint.
            *[Line([-3.65+dx,-.65+dy,0],[-3.4+dx,-.52+dy,0],color=TEXT,stroke_width=4)
              for dx,dy in ((0,0),(-.07,.3),(-.14,.6))])
        self.add(left,joint)
        self.at('near a joints limits')
        self.play(FadeIn(T('Joint limits',30,YELLOW).move_to([-3,1.8,0])),FadeIn(T('Joint and skin\nafferents',26).move_to([-3,-2.2,0])),run_time=.45)
        self.at('feeling of effort')
        right=left.copy().move_to([3,-.3,0])
        weight=VGroup(
            RoundedRectangle(width=1.65,height=1.25,corner_radius=.12,color=TEXT,
                             fill_color=GREY,fill_opacity=.3).move_to([3.7,-.9,0]),
            Arc(radius=.4,start_angle=0,angle=PI,color=TEXT,stroke_width=5).move_arc_center_to([3.7,-.27,0]),
            T('Weight',26).move_to([3.7,-.9,0])).shift(UP*.25)
        # A bent arm ends in a palm, thumb and curled fingers gripping the handle.
        hand=VGroup(
            Line([.9,-1.2,0],[2.15,-1.2,0],color=GREY,stroke_width=28),
            Line([2.15,-1.2,0],[2.65,.55,0],color=GREY,stroke_width=28),
            Circle(radius=.22,color=TEXT,fill_color=BG,fill_opacity=1).move_to([2.15,-1.2,0]),
            RoundedRectangle(width=1.05,height=.48,corner_radius=.2,color=TEXT,
                             fill_color=GREY,fill_opacity=.7).move_to([3.15,.55,0]),
            Line([3.05,.72,0],[3.55,.95,0],color=TEXT,stroke_width=9),
            *[Arc(radius=.12,start_angle=PI,angle=PI,color=TEXT,stroke_width=5)
              .move_arc_center_to([x,.39,0]) for x in (3.3,3.52,3.74)])
        self.play(FadeIn(right),FadeIn(weight),Create(hand),FadeIn(T('Force and effort',30,YELLOW).move_to([3,1.8,0])),run_time=.5)
        self.play(weight.animate.shift(UP*.2),hand.animate.shift(UP*.2),FadeIn(T('Tendon organs\nand effort',26).move_to([3,-2.2,0])),run_time=.4)
        self.finish()

class S20Takeaway(TimedScene):
    def construct(self):
        # Empty opening; input and estimate are assembled on their named beats.
        est=chip('Limb position\nis an estimate',ORANGE,40,pad=.4).move_to([3.1,0,0])
        w=Line([-5.7,1.5,0],[-2,1.5,0],color=BLUE,stroke_width=12)
        a=Arrow([-1.75,1.5,0],[.75,.45,0],color=BLUE,buff=.1,stroke_width=7)
        e=eye().scale(1.9).move_to([-3.85,-1.5,0])
        v=Arrow([-1.75,-1.5,0],[.75,-.45,0],color=TEXT,buff=.1,stroke_width=7)
        self.at('limb position')
        self.play(Create(w),run_time=.3)
        self.at('is an estimate')
        self.play(GrowArrow(a),run_time=.3)
        # Keep the estimate completely absent until the word itself is spoken.
        self.at('estimate')
        self.play(FadeIn(est),run_time=.3)
        self.at('mainly from the stretch line')
        self.play(FadeIn(T('Stretch line',34,BLUE).move_to([-3.85,2.6,0])),run_time=.3)
        self.at('lose that input')
        self.play(w.animate.set_color(GREY),a.animate.set_color(GREY).set_opacity(.35),FadeIn(e),run_time=.6)
        self.at('vision does much')
        self.play(GrowArrow(v),FadeIn(T('Vision',34).move_to([-3.85,-2.85,0])),run_time=.5)
        self.finish()

class S21End(EndCard):
    LINE='With stretch input lost, vision does much of the work.'
