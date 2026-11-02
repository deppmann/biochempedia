"""Chapter 6 repair. All proteins are schematic chips, not molecular structures.
COLOR MAP: BLUE channel; GREY membrane/control; YELLOW tension;
PURPLE projected area; GREEN sufficiency/retained; RED loss; ORANGE proposed tether.
Traces are sampled analytical toy models (step stimulus, exponential inactivation
and recovery), encoding ordinal observations ONLY, never measured kinetics.
No numerical kinetic constants or qualitative bar heights are empirical estimates.
"""
import numpy as np
from bp_style import *
ORANGE='#F29E4C'
PURPLE='#B58CD9'

def txt(s,x=0,y=0,size=30,color=TEXT):
    return T(s,size,color).move_to([x,y,0])

def channel(x=0,y=0):
    # Same pore icon in every preparation; paralog is identified by nearby text.
    a=RoundedRectangle(width=.85,height=1.0,corner_radius=.15,color=BLUE,fill_color=BG,fill_opacity=1)
    a.add(Line([-.14,-.42,0],[-.14,.42,0],color=BLUE,stroke_width=4),Line([.14,-.42,0],[.14,.42,0],color=BLUE,stroke_width=4))
    return a.move_to([x,y,0])

def membrane(y=.5):
    return VGroup(Line([-5.9,y,0],[-.48,y,0],color=GREY,stroke_width=14),Line([.48,y,0],[5.9,y,0],color=GREY,stroke_width=14),channel(0,y))

def droplets():
    ts=np.linspace(np.pi/3,5*np.pi/3,100)
    pts=[[-1.2+2.4*np.cos(t),2.4*np.sin(t),0] for t in ts]
    left=VMobject(color=GREY,stroke_width=7,fill_color=GREY,fill_opacity=.1).set_points_as_corners(pts+[pts[0]])
    # Two visible outlines represent the lipid coat, without molecular geometry.
    shell=left.copy().scale(.97,about_point=[-1.2,0,0]).set_stroke(YELLOW,2).set_fill(opacity=0)
    l=VGroup(left,shell); r=l.copy().flip(UP,about_point=ORIGIN)
    bil=Line([0,-2.08,0],[0,2.08,0],color=YELLOW,stroke_width=10)
    return VGroup(l,r,bil,channel())

def drop_label():return txt('purified mouse Piezo1',0,3.1,32,BLUE)

def question():
    return VGroup(droplets().shift(DOWN*.1),drop_label(),
        txt('If a tether were required, would this open?',0,-2.75,32),
        txt('What would opening tell us about a cell?',0,-3.35,28))

def model(t,kind):
    t=np.asarray(t);on=(t>=.15)&(t<.82)
    if kind=='force' or kind=='sustained':return on.astype(float)
    if kind=='decay':return on*np.exp(-np.maximum(t-.15,0)/.105)
    if kind=='slow':return on*np.exp(-np.maximum(t-.15,0)/.6)
    if kind=='recover':return 1-np.exp(-t/.16)
    if kind=='recover_wt':return 1-np.exp(-t/.55)
    return np.zeros_like(t)

def curve(x,y,w,h,kind='sustained',color=GREEN,inward=False):
    ts=np.unique(np.r_[np.linspace(0,1,250),.14999,.15,.81999,.82])
    vs=model(ts,kind)
    return VMobject(color=color,stroke_width=5).set_points_as_corners([[x+w*t,y+(-1 if inward else 1)*h*v,0] for t,v in zip(ts,vs)])

def axes(x,y,w,h,xlabel='time',ylabel='current',inward=False,ticks=False):
    s=-1 if inward else 1
    a=VGroup(Line([x,y,0],[x+w,y,0],color=GREY),Line([x,y,0],[x,y+s*h,0],color=GREY))
    for t in [0,.5,1]:
        a.add(Line([x+w*t,y-.07,0],[x+w*t,y+.07,0],color=GREY))
    a.add(txt(xlabel,x+w/2,y+s*h+.4 if inward else y-.48,28))
    lab=txt(ylabel,size=28).rotate(PI/2).move_to([x-.6,y+s*h/2,0]);a.add(lab)
    a.add(txt('0',x-.22,y,26,GREY))
    if ticks:
        a.add(txt('1',x-.22,y+s*h,26,GREY))
    return a

def comparison():
    # Same onset, offset, time window and amplitude; inward current plotted down.
    return VGroup(txt('Piezo1 · same pulse and time axis',0,3.1,32,BLUE),
      txt('whole cell',-3.7,2.35,30,BLUE),axes(-4.9,1.9,10.5,1.55,inward=True),curve(-4.9,1.9,10.5,1.55,'decay',BLUE,True),
      txt('purified bilayer',-3.5,-.5,30,BLUE),axes(-4.9,-.95,10.5,1.55,inward=True),curve(-4.9,-.95,10.5,1.55,'sustained',GREEN,True),
      txt('qualitative model · no measured kinetics',0,-3.35,28,GREY))

def result():
    d=droplets().scale(.93).move_to([-3.1,0,0]).stretch(1.22,1).stretch(.83,0)
    return VGroup(d,txt('purified mouse Piezo1',-3,3.1,30,BLUE),
      axes(.5,1.9,5.1,1.4,inward=True),curve(.5,1.9,5.1,1.4,'sustained',GREEN,True),
      axes(.5,-2.3,5.1,1.3,ylabel='tension'),curve(.5,-2.3,5.1,1.3,'force',YELLOW),
      txt('no inactivation',3.1,-.5,28,GREEN),txt('sufficient in this preparation',0,-3.25,32,GREEN),txt('qualitative model',3.1,3.1,28,GREY))

def tether():
    outline=RoundedRectangle(width=6.0,height=5.6,corner_radius=.65,color=GREY).move_to([-3.1,-.2,0])
    mem=Line([-6.1,1.1,0],[-.1,1.1,0],color=GREY,stroke_width=13)
    ch=VGroup(channel(-4.9,1.1),txt('Piezo1',-4.9,2.05,28,BLUE))
    cad=chip('E-cadherin',ORANGE,28).move_to([-2,1.1,0]);cad[0].set_fill(BG,opacity=1)
    beta=chip('beta-catenin',ORANGE,28).move_to([-2,-.65,0])
    act=VGroup(Line([-5.5,-2.25,0],[-.7,-2.25,0],color=ORANGE,stroke_width=10),txt('actin',-4.65,-1.8,30,ORANGE))
    link=DashedLine([-4.4,1.1,0],[-3.05,1.1,0],color=ORANGE,stroke_width=5)
    b=DashedLine([-2,.7,0],[-2,-.25,0],color=ORANGE,stroke_width=5)
    c=DashedLine([-2,-1.05,0],[-2,-2.25,0],color=ORANGE,stroke_width=5)
    return VGroup(outline,mem,ch,cad,beta,act,link,b,c)

def person(x=0,y=0):
    return VGroup(Circle(.28,color=GREY).move_to([x,y+1.1,0]),
      Line([x,y+.82,0],[x,y-.6,0],color=GREY,stroke_width=7),
      Line([x,y-.6,0],[x-.5,y-1.55,0],color=GREY,stroke_width=7),Line([x,y-.6,0],[x+.5,y-1.55,0],color=GREY,stroke_width=7),
      VMobject(color=GREY,stroke_width=7).set_points_as_corners([[x-.85,y-.15,0],[x-.5,y+.4,0],[x,y+.4,0],[x+.6,y+.05,0],[x+1,y+.45,0]]))

def mouse_icon():
    # A single smooth profile: pointed snout, rounded back, haunch and belly.
    outline=VMobject(color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.16)
    outline.set_points_smoothly([[-1.65,-.35,0],[-1.6,.35,0],[-1,.85,0],[0,.9,0],[.85,.6,0],[1.35,.65,0],[2.05,.1,0],[1.5,-.2,0],[.85,-.55,0],[-.5,-.65,0],[-1.65,-.35,0]])
    ear=Ellipse(width=.6,height=.75,color=GREY,fill_color=BG,fill_opacity=1).move_to([1.05,.75,0])
    inner=Arc(radius=.18,start_angle=-PI/2,angle=PI,color=GREY).move_to([1.06,.76,0])
    eye=Dot([1.55,.35,0],radius=.055,color=TEXT)
    tail=VMobject(color=GREY,stroke_width=4).set_points_smoothly([[-1.6,-.2,0],[-2.05,-.45,0],[-2.65,-.35,0],[-2.8,.15,0],[-2.45,.4,0]])
    legs=VGroup(*[VMobject(color=GREY,stroke_width=4).set_points_as_corners([[x,-.5,0],[x-.15,-.85,0],[x+.25,-.85,0]]) for x in [-.9,.9]])
    whiskers=VGroup(*[Line([1.85,.08,0],[2.35,y,0],color=GREY,stroke_width=2) for y in [-.15,.25]])
    return VGroup(outline,ear,inner,eye,tail,legs,whiskers,Dot([2.05,.1,0],radius=.06,color=TEXT))

class S00Title(TitleCard):
    LESSON='Piezo Channels and the Physics of Force'
    TITLE='Lipid, Tether and People'
    def construct(self):
        self.add(txt('BIOCHEMISTRYPEDIA',0,1.75,28,TEAL),
          txt(self.LESSON,0,.85,30,GREY),txt(self.TITLE,0,-.35,54),
          Line([-1.4,-1.35,0],[1.4,-1.35,0],color=GOLD,stroke_width=4))
        self.finish()

class S01Question(SpokenScene):
    def construct(self):
        self.add(membrane(),txt('Piezo1',2.4,1.35,30,BLUE))
        self.at('Tension pays');self.play(FadeIn(txt('Tension pays for area.',0,3.05,44,YELLOW)),run_time=.45)
        self.at('But how');self.play(FadeIn(txt('How does force reach it?',0,2.25,32)),run_time=.4)
        self.at('Through lipid');self.play(GrowArrow(Arrow([-5.5,.9,0],[-.7,.9,0],buff=0,color=YELLOW)),FadeIn(txt('membrane tension',-3.1,1.5,28,YELLOW)),run_time=.4)
        chain=VGroup(*[chip('protein',ORANGE,28).move_to([0,y,0]) for y in [-2.6,-1.4]])
        link=VGroup(DashedLine([0,-2.25,0],[0,-1.8,0],color=ORANGE),DashedLine([0,-1.05,0],[0,-.15,0],color=ORANGE),Arrow([0,-.6,0],[0,-.1,0],buff=0,color=ORANGE))
        self.at('through a protein');self.play(FadeIn(chain),Create(link),FadeIn(txt('possible direct\ntether force',3,-1.9,30,ORANGE)),run_time=.5);self.finish()

class S02Budget(SpokenScene):
    def construct(self):
        eq=txt('ΔG = ΔG₀ − T × ΔA',-.8,1.55,54,YELLOW)
        self.add(txt('Piezo1 · opening energy budget',0,3.1,32,BLUE))
        self.at('The idea');self.play(FadeIn(eq),run_time=.5)
        self.at('membrane tension');self.play(FadeIn(txt('T = membrane tension     ΔA = area gained on opening',0,.15,30)),FadeIn(txt('ΔG₀ = opening energy without applied force',0,-.6,30,GREY)),run_time=.5)
        self.at('A tether could');self.play(FadeIn(txt('A tether may change T',0,-1.7,34,ORANGE)),run_time=.45)
        self.at('pull on');self.play(FadeIn(txt('or supply direct force',0,-2.45,32,ORANGE)),run_time=.4)
        self.at('That would add');self.play(FadeIn(DashedVMobject(RoundedRectangle(width=2.7,height=1.15,color=ORANGE).move_to([4.4,1.55,0]))),FadeIn(txt('− F × d ?',4.4,1.55,38,ORANGE)),FadeIn(txt('F = force    d = distance',0,-3.2,28,ORANGE)),run_time=.5);self.finish()

class S03Test(SpokenScene):
    def construct(self):
        ch=channel(0,.1);bound=Ellipse(width=11.5,height=5.8,color=GREY)
        labels=VGroup(chip('membrane proteins',GREY,30).move_to([-2.2,1.2,0]),chip('protein partners',GREY,30).move_to([2.5,.6,0]),chip('cytoskeleton',GREY,30).move_to([0,-1.8,0]))
        tag=txt('Piezo1',0,-.85,30,BLUE)
        cell_label=txt('cell',0,3.1,32,GREY);self.add(bound,labels,ch,tag,cell_label)
        self.at('Take everything');
        for ob in labels:self.play(FadeOut(ob),run_time=.22)
        self.play(FadeOut(bound),FadeOut(cell_label),ch.animate.scale(4),tag.animate.move_to([0,2.7,0]),run_time=.45);self.finish()

class S04Droplet(SpokenScene):
    def construct(self):
        ch=channel().scale(4);self.add(ch,drop_label())
        d=droplets();self.at('was placed');self.play(FadeOut(ch),FadeIn(VGroup(*d[:3])),run_time=.35);self.play(FadeIn(d[3]),run_time=.35)
        self.at('no other');self.play(FadeIn(txt('no other cellular components',0,-3.15,30)),run_time=.4);self.finish()

class S05DropletDef(SpokenScene):
    def construct(self):
        d=droplets();d[0].shift(LEFT*.75);d[1].shift(RIGHT*.75)
        self.add(d[0],d[1],drop_label())
        label=txt('droplet bilayer · no cell',3.8,-2.8,28,YELLOW)
        lead=Line([.15,-1.4,0],[2.4,-2.5,0],color=YELLOW)
        self.at('A droplet bilayer');self.play(FadeIn(label),Create(lead),run_time=.4)
        self.at('touch');self.play(d[0].animate.shift(RIGHT*.75),d[1].animate.shift(LEFT*.75),run_time=.45);self.play(Create(d[2]),FadeIn(d[3]),run_time=.3)
        self.at('Nothing from');self.play(FadeIn(txt('lipid coats only · no cell components',-1,-3.4,28)),run_time=.4);self.finish()

class S06Predict(SpokenScene):
    def construct(self):
        q=question();self.add(q[0],q[1])
        self.at('Suppose a tether');self.play(FadeIn(q[2]),run_time=.5)
        self.at('What should');self.play(Indicate(q[0][3],color=BLUE),run_time=.6)
        self.at('And what');self.play(FadeIn(q[3]),run_time=.4);self.finish()

class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(question())
        n=txt('5',5.5,2.5,42,YELLOW);self.add(n)
        for i in range(5,0,-1):
            if i<5:self.remove(n);n=txt(str(i),5.5,2.5,42,YELLOW);self.add(n)
            self.wait(1)

class S08Reveal(SpokenScene):
    def construct(self):
        r=result();d=droplets().scale(.86).move_to([-3.4,0,0]);self.add(d,r[1],r[2],r[4],r[8])
        cur=curve(.5,1.9,5.1,1.4,'silent',GREEN,True);force=curve(.5,-2.3,5.1,1.3,'silent',YELLOW);self.add(cur,force)
        pred=txt('prediction: silent',3.1,2.55,28,GREY);self.at('It should');self.play(FadeIn(pred),run_time=.4)
        self.at('Yet force');self.play(FadeOut(pred),Transform(d,r[0]),Transform(cur,r[3]),Transform(force,r[5]),FadeIn(r[6]),GrowArrow(Arrow([-5.2,-2.1,0],[-5.2,-2.8,0],buff=0,color=YELLOW)),GrowArrow(Arrow([-5.2,2.1,0],[-5.2,2.8,0],buff=0,color=YELLOW)),run_time=.65)
        self.at('protein plus lipid');self.play(FadeIn(r[7]),run_time=.45);self.finish()

class S09Hold(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(result());self.wait(3)

class S10Cell(SpokenScene):
    def construct(self):
        self.add(droplets().scale(.72).move_to([-3.4,0,0]),txt('purified Piezo1',-3.4,2.9,30,BLUE))
        c=VGroup(Ellipse(width=5.5,height=5,color=GREY).move_to([3.1,-.1,0]),channel(3.1,2.4),txt('intact cell · Piezo1',3.1,3.1,30,BLUE))
        self.at('an intact cell');self.play(FadeIn(c),run_time=.45)
        self.at('a second route');self.play(Create(DashedLine([3.1,-1.9,0],[3.1,1.8,0],color=ORANGE,stroke_width=5)),GrowArrow(Arrow([3.1,1.2,0],[3.1,1.85,0],buff=0,color=ORANGE)),FadeIn(txt('?',4.3,.3,64,ORANGE)),FadeIn(txt('second route?',3.1,-3,30,ORANGE)),run_time=.5);self.finish()

class S11Tether(SpokenScene):
    def construct(self):
        # Use the whole cell stage here; the following scene returns to the inset.
        t=tether().stretch(1.75,0,about_point=[-3.1,0,0]).shift(RIGHT*3.1)
        # Rebuild labels without stretching the lettering.
        for i,label in [(3,'E-cadherin'),(4,'beta-catenin')]:
            pos=t[i].get_center();t[i].become(chip(label,ORANGE,32).move_to(pos))
            t[i][0].set_fill(BG,opacity=1)
        for ob,label,color in [(t[2][1],'Piezo1',BLUE),(t[5][1],'actin',ORANGE)]:
            ob.become(txt(label,*ob.get_center()[:2],32,color))
        self.add(*t[:3],txt('proposed · inside a cultured cell',0,3.2,32,ORANGE))
        # The proposed links start building immediately, before the named nodes.
        self.at('A second route');self.play(Create(t[6]),Create(t[7]),Create(t[8]),run_time=.85)
        self.at('and colleagues');self.play(FadeIn(txt('Wang and colleagues, 2022',0,-3.35,28,GREY)),run_time=.3)
        self.at('chain of');self.play(FadeIn(t[3]),run_time=.3)
        self.at('beta catenin');self.play(FadeIn(t[4]),run_time=.3)
        self.at('and actin');self.play(FadeIn(t[5]),run_time=.3);self.finish()

class S12TetherResult(SpokenScene):
    def construct(self):
        t=tether();self.add(t,txt('proposed coupling · cultured cells',0,3.2,32,ORANGE),axes(1,1.1,4.7,2.3,inward=True),txt('cytoskeleton-driven current',3.3,2.15,28,GREEN),txt('qualitative model',3.3,-2.6,28,GREY))
        cur=curve(1,1.1,4.7,2.3,'decay',GREEN,True);self.add(cur)
        self.at('the channels');self.play(FadeOut(t[6]),Create(VGroup(Line([-3.9,.8,0],[-3.4,1.4,0],color=RED,stroke_width=6),Line([-3.9,1.4,0],[-3.4,.8,0],color=RED,stroke_width=6))),run_time=.5)
        self.at('prevented');self.play(Transform(cur,curve(1,1.1,4.7,2.3,'silent',GREEN,True)),run_time=.6)
        self.at('their cultured');self.play(FadeIn(txt('cytoskeleton-dependent gating lost',0,-3.35,30,RED)),run_time=.45);self.finish()

class S13Rivals(SpokenScene):
    def construct(self):
        a=RoundedRectangle(width=5.5,height=4.7,color=YELLOW).move_to([-3.2,.4,0]);b=a.copy().set_color(ORANGE).move_to([3.2,.4,0])
        left=VGroup(a,txt('PURIFIED PIEZO1',-3.2,2.1,30,YELLOW),txt('droplet bilayers',-3.2,1.35,30),txt('Protein + lipid\nare sufficient here',-3.2,-.1,34,GREEN))
        right=VGroup(b,txt('CULTURED CELLS',3.2,2.1,30,ORANGE),txt('A route was proposed',3.2,1.25,30,ORANGE),txt('Reported to be required\nin cytoskeleton-driven\ngating assays',3.2,-.2,28))
        self.add(left,right,txt('Both can be true',0,3.2,36,GREEN))
        self.at('Sufficiency in');self.play(Indicate(a,color=YELLOW),run_time=.6)
        self.at('cannot exclude');self.play(Indicate(b,color=ORANGE),run_time=.6)
        self.at('That is why');self.play(FadeIn(txt('The field has not chosen.',0,-2.85,38)),run_time=.5);self.finish()

class S14Hint(SpokenScene):
    def construct(self):
        c=comparison();self.add(c[0],*c[1:4],c[-1])
        self.at('There is even');self.play(FadeIn(c[4]),FadeIn(c[5]),run_time=.5)
        self.at('The purified channel');self.play(Create(c[6]),run_time=.8)
        self.at('rapid');self.play(Indicate(c[3],color=BLUE,scale_factor=1),run_time=.5);self.finish()

class S15Genetics(SpokenScene):
    def construct(self):
        inset=VGroup(axes(-5.5,1.1,3.2,2.2,inward=True),curve(-5.5,1.1,3.2,2.2,'decay',BLUE,True),curve(-5.5,1.1,3.2,2.2,'sustained',GREEN,True),txt('cell',-4.9,-2,28,BLUE),txt('bilayer',-3,-2,28,GREEN))
        # Continuous hand silhouette with a curled index finger and visible knuckle.
        hand=VMobject(color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.18)
        hand.set_points_smoothly([[.0,-1.5,0],[-.25,-.7,0],[-.85,.1,0],[-1.0,.65,0],[-.8,.8,0],[-.3,.35,0],[-.45,1.65,0],[-.3,1.9,0],[-.12,1.65,0],[.0,.7,0],[.02,2.05,0],[.2,2.23,0],[.37,2.02,0],[.4,.75,0],[.58,1.9,0],[.78,2.03,0],[.94,1.8,0],[.86,.7,0],[1.15,1.25,0],[1.6,1.12,0],[1.65,.65,0],[1.4,.5,0],[1.27,.83,0],[1.15,.75,0],[1.2,-.5,0],[.9,-1.5,0]])
        hand.add(Line([.0,-1.5,0],[.9,-1.5,0],color=GREY),Circle(.14,color=ORANGE,stroke_width=4).move_to([1.55,1.03,0]))
        # Closed foot profile: lower leg, heel, sole, ball and bent-down toes.
        foot=VMobject(color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.18)
        foot.set_points_smoothly([[3.15,2.05,0],[3.05,.25,0],[2.95,-.65,0],[3.15,-1.12,0],[4.3,-1.15,0],[5.25,-1.1,0],[5.65,-1.5,0],[5.95,-1.42,0],[5.85,-.92,0],[5.45,-.5,0],[4.5,-.38,0],[3.95,.18,0],[3.9,2.05,0]])
        foot.add(Line([3.15,2.05,0],[3.9,2.05,0],color=GREY),Circle(.17,color=ORANGE,stroke_width=4).move_to([5.48,-.73,0]),Line([5.45,-.92,0],[5.62,-1.12,0],color=GREY))
        previous=comparison();self.add(previous)
        self.at('Inactivation is');self.play(FadeOut(previous),FadeIn(inset),FadeIn(hand),FadeIn(foot),FadeIn(txt('distal arthrogryposis · Piezo2',0,3.1,36,BLUE)),FadeIn(txt('Piezo1 inactivation',-4,2.05,28,BLUE)),run_time=.7)
        self.at('an inherited');self.play(FadeIn(txt('inherited condition',1.7,2.55,28)),run_time=.4)
        self.at('hands');self.play(FadeIn(txt('hands',.4,-1.95,34)),run_time=.25)
        self.at('feet');self.play(FadeIn(txt('feet',4.45,-1.95,34)),run_time=.25)
        self.at('fixed in bent');self.play(FadeIn(txt('joints fixed in bent positions from birth',0,-2.85,32,ORANGE)),Indicate(hand[-1]),Indicate(foot[-2]),run_time=.5);self.finish()

class S16Variants(SpokenScene):
    def construct(self):
        self.add(txt('Piezo2 variants · human cell line',0,3.35,32,BLUE))
        intro=VGroup(chip('I802F',BLUE,40).move_to([-3,1,0]),chip('E2727del',ORANGE,40).move_to([3,1,0]),txt('compared with wild type',0,-1,34,GREY))
        self.add(intro)
        self.at('were tested');self.play(intro.animate.shift(DOWN*.15),run_time=.4)
        self.at('Both sped recovery');self.play(FadeOut(intro),FadeIn(txt('recovery between pulses',0,2.7,30)),FadeIn(axes(-4.8,.1,7.1,2.05,'interval between pulses','fraction recovered',ticks=True)),Create(curve(-4.8,.1,7.1,2.05,'recover_wt',GREY)),Create(curve(-4.8,.1,7.1,2.05,'recover',BLUE)),run_time=.6)
        self.add(txt('I802F +\nE2727del',4.3,1.95,28,BLUE),txt('both faster',4.3,1.25,28),txt('wild type',4.3,.6,28,GREY),Line([2.7,1.85,0],[3.05,1.85,0],color=BLUE),Line([2.7,.6,0],[3.05,.6,0],color=GREY))
        self.at('Only one slowed');self.play(FadeIn(txt('during the pulse',0,-.8,30)),FadeIn(axes(-4.8,-2.75,7.1,1.45,'time','current')),Create(curve(-4.8,-2.75,7.1,1.45,'decay',GREY)),Create(curve(-4.8,-2.75,7.1,1.45,'slow',ORANGE)),run_time=.6)
        self.add(txt('E2727del',4.3,-1.45,28,ORANGE),txt('I802F tracks\nwild type',4.3,-2.35,28,BLUE),txt('qualitative model\nnot measured',4.3,-3.3,28,GREY));self.finish()

class S17Rule(SpokenScene):
    def construct(self):
        claim=txt('Gain of function always means\nslower inactivation',0,1.3,48)
        self.add(txt('Piezo2 · read each variant',0,3.15,34,BLUE),claim,
          txt('I802F: no slowing during the pulse',0,-.35,36,BLUE),
          txt('Gain of function = increased channel activity',0,-1.35,32,GREY))
        self.at('not a rule');self.play(Create(Cross(claim,stroke_color=RED,stroke_width=6)),run_time=.5)
        self.at('Read each');self.play(FadeIn(txt('Read each variant.',0,-2.7,44,BLUE)),run_time=.45);self.finish()

class S18Mice(SpokenScene):
    def construct(self):
        self.add(txt('MOUSE · Piezo2 loss of function',0,3.2,36,BLUE),
          mouse_icon().scale(1.05).move_to([-3.25,.7,0]),
          axes(.8,-1.9,4.6,3.7,'','light-touch response'),
          Rectangle(width=1,height=3.25,fill_color=GREY,fill_opacity=.7,color=GREY).move_to([2,-.275,0]),
          Rectangle(width=1,height=.1,fill_color=RED,fill_opacity=.8,color=RED).move_to([4.5,-1.85,0]),
          txt('control',2,-2.35,28),txt('deleted',4.5,-2.35,28,RED),
          txt('qualitative assay summary',3.1,2.5,28,GREY))
        self.at('Adult mice');self.play(FadeIn(txt('adult mice',-3.2,2.3,30)),run_time=.4)
        self.at('sensory neurons');self.play(FadeIn(txt('Piezo2 deleted in\nsensory neurons\nand Merkel cells',-3.2,-1.8,30,BLUE)),run_time=.4)
        self.at('lose almost all');self.play(Indicate(self.mobjects[4],color=RED),FadeIn(txt('almost complete light-touch deficit',0,-3.15,32,RED)),run_time=.6);self.wait(1.5);self.finish()

class S19People(SpokenScene):
    def construct(self):
        panel=RoundedRectangle(width=4.3,height=5.5,color=GREY).move_to([-4,.1,0])
        first=person(-4.9,.3)
        second=person(-3.1,.3).stretch(.86,1,about_point=[-3.1,-1.25,0])
        second[-1].become(VMobject(color=GREY,stroke_width=7).set_points_as_corners([[-3.8,-.35,0],[-3.55,.5,0],[-3.1,.5,0],[-2.65,.1,0],[-2.4,.5,0]]))
        # Both conditions are visible from the first frame of the people scene.
        covered=Rectangle(width=1.35,height=3.5,color=ORANGE,fill_color=ORANGE,fill_opacity=.7).move_to([4.2,-.35,0])
        self.add(panel,first,second,txt('PEOPLE · Piezo2',-4,3.2,32,BLUE),
          txt('two individuals',-4,2.25,28),txt('limb-position error',2.5,3.1,32),
          axes(-.6,-2.1,6.3,4.2,'','error'),
          Rectangle(width=1.35,height=1.55,color=ORANGE,fill_color=ORANGE,fill_opacity=.7).move_to([1.1,-1.325,0]),covered,
          txt('eyes open',1.1,-2.55,28),txt('eyes covered',4.2,-2.55,28),
          txt('qualitative comparison',2.6,2.35,28,GREY))
        self.at('impaired discriminative');self.play(FadeIn(txt('discriminative touch\nimpaired',-4,-1.85,28,RED)),run_time=.45)
        self.at('limb position');self.play(FadeIn(txt('profoundly impaired',2.6,-3.25,30,RED)),run_time=.5)
        self.at('worse without');self.play(Indicate(covered,color=ORANGE,scale_factor=1.04),run_time=.5);self.wait(2.5);self.finish()

class S20Selective(SpokenScene):
    def construct(self):
        a=RoundedRectangle(width=5.7,height=5.1,color=GREY).move_to([-3.1,.6,0]);b=a.copy().move_to([3.1,.6,0])
        self.add(channel(-5.4,2.65).scale(.5),channel(5.4,2.65).scale(.5),a,b,txt('ADULT MICE',-3.1,2.65,32,BLUE),txt('PEOPLE',3.1,2.65,32,BLUE),mouse_icon().scale(.65).move_to([-3.1,1.2,0]),txt('Piezo2 deleted',-3.1,.0,30,BLUE),txt('almost complete\nlight-touch deficit',-3.1,-1.1,32,RED))
        self.at('But they kept');self.play(FadeIn(txt('Other abilities\nretained',3.1,1.3,38,GREEN)),run_time=.45)
        self.at('Their deficits');self.play(FadeIn(txt('Selective deficits:\ndiscriminative touch\nand limb position',3.1,-.65,30,RED)),run_time=.45)
        self.at('Keep the mouse');self.play(FadeIn(RoundedRectangle(width=12,height=1.05,color=GOLD).move_to([0,-2.85,0])),FadeIn(txt('Keep the species claims separate.',0,-2.85,34)),run_time=.5);self.finish()

# Fixed arc length cap: projected area = pi * (L sin(theta)/(2 theta))².
# Subunit sectors are labelled schematic blocks, never helix/ribbon drawings.
L_CAP=5.4
TH0=1.239

def cap(theta):
    r=L_CAP/(2*max(theta,.001));parts=VGroup()
    for i in range(3):
        p=np.linspace(-theta+2*theta*i/3+.018*theta,-theta+2*theta*(i+1)/3-.018*theta,40)
        parts.add(VMobject(color=BLUE,stroke_width=20).set_points_as_corners([[1.5*r*np.sin(t),1.5*r*(np.cos(t)-np.cos(theta)),0] for t in p]))
    return parts

def footprint(theta):
    r=L_CAP/(2*max(theta,.001));w=3*r*np.sin(theta)
    return Ellipse(width=w,height=.85,color=PURPLE,stroke_width=5).move_to([0,-1.5,0])

class S21Back(SpokenScene):
    def construct(self):
        th=ValueTracker(TH0);d=always_redraw(lambda:cap(th.get_value()))
        # The initial footprint remains as a dashed reference after flattening.
        before=DashedVMobject(footprint(TH0).set_stroke(GREY,3),num_dashes=36)
        after=footprint(TH0)
        self.add(txt('mouse Piezo2 · schematic',0,3.3,30,BLUE),d,
          Line([-5.8,0,0],[5.8,0,0],color=GREY,stroke_width=5),before)
        self.at('one channel');self.play(FadeIn(txt('Why does one channel need 114 helices?',0,2.65,36)),run_time=.45)
        # Confirmed in lesson.mdx, architecture section: 38 per protomer, 114 per trimer.
        count=txt('3 subunits × 38 helices = 114',0,-.55,30,BLUE);self.add(count)
        self.add(txt('before · curved',0,-1.5,28,GREY))
        self.at('leading model');self.play(FadeIn(txt('leading model, still debated',0,-3.3,30,GREY)),run_time=.4)
        self.at('to collect area');self.play(FadeOut(count),run_time=.15)
        # Separate the comparison rings vertically so both states stay legible.
        self.add(after)
        self.play(th.animate.set_value(.08),Transform(after,footprint(.08).shift(DOWN*.95)),run_time=.65)
        self.add(txt('after · flat',0,-2.45,28,PURPLE))
        old=1.5*(L_CAP/(2*TH0))*np.sin(TH0);new=1.5*(L_CAP/(2*.08))*np.sin(.08)
        self.add(Line([old,-1.5,0],[old,-.55,0],color=GREY),Line([new,-2.45,0],[new,-.55,0],color=PURPLE),
          DoubleArrow([old,-.65,0],[new,-.65,0],buff=0,color=PURPLE,tip_length=.12),txt('ΔA',4.85,-.65,32,PURPLE))
        self.wait(2);self.finish()

class S22Takeaway(SpokenScene):
    def construct(self):
        self.at('Tension pays');self.play(FadeIn(txt('Tension pays for area.',0,1.8,48,YELLOW)),run_time=.5)
        self.at('Whether a tether');self.play(FadeIn(txt('Whether a tether adds its own force\nis a separate question.',0,-.3,36,YELLOW)),run_time=.45);self.finish()

class S23End(EndCard):
    LINE='Tension pays for area.'
    def construct(self):
        self.add(txt(self.LINE,0,1,48,YELLOW),
          txt('Whether a tether adds its own force\nis a separate question.',0,-.35,34,YELLOW),
          txt('biochemistrypedia.com',0,-1.75,28,TEAL))
        self.finish()
