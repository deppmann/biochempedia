"""Chapter 6. COLOR MAP shared with scenes.old.py / CHAPTERS.md:
YELLOW light, clock/pupil outputs, questions; BLUE rod/cone relay;
GREEN ipRGC and melanopsin; PURPLE brain targets; RED removal/loss;
GREY outlines/de-emphasis; TEXT results. Reference GREEN cells are preserved
rather than replacing the series concept colour with gold.
CHAPTERS.md remains untouched under TASK.md's edit-only restriction.
Reference arr/cell/clock/eye helpers reused below. Spectrum uses the series'
Govardovskii alpha-band template at the lesson's human 480 nm peak. It is a
model, not fabricated participant data. Other experiments use qualitative
icons (no invented quantitative traces). Rhythm: sine phase schematic only.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'

def arr(a,b,color=GREY,w=5,tip=.22):
    return Arrow(a,b,buff=.06,color=color,stroke_width=w,tip_length=tip,
                 max_tip_length_to_length_ratio=.45,max_stroke_width_to_length_ratio=12)
def cell(cx,cy,w=2.5,h=1.7,color=GREEN,fill=.18):
    return Ellipse(width=w,height=h,stroke_color=color,stroke_width=4,fill_color=color,fill_opacity=fill).move_to([cx,cy,0])
def lab(s,x,y,size=28,color=TEXT): return T(s,size,color).move_to([x,y,0])
def head(s): return lab(s,0,3.12,32)
def foot(s): return lab(s,0,-3.15,28,GREY)
def box(s,x,y,color=PURPLE,size=28): return chip(s,color,size).move_to([x,y,0])
def body(x,y): return VGroup(cell(x,y),lab('ipRGC',x,y,28,GREEN))
def cross(c,s=.35):
    c=np.array(c,float)
    return VGroup(Line(c+[-s,-s,0],c+[s,s,0],color=RED,stroke_width=6),Line(c+[-s,s,0],c+[s,-s,0],color=RED,stroke_width=6))
def clock_icon(cx,cy,r=.55):
    c=np.array([cx,cy,0.]); ring=Circle(radius=r,color=YELLOW,stroke_width=4).move_to(c)
    h1=Line(c,c+[0,r*.7,0],color=YELLOW,stroke_width=4)
    h2=Line(c,c+[r*.62*np.cos(PI/6),r*.62*np.sin(PI/6),0],color=YELLOW,stroke_width=4)
    g=VGroup(ring,h1,h2); g.h2=h2; g.c=c; return g

def eye_icon(cx,cy,w=1.5):
    eye=Ellipse(width=w,height=w*.57,color=YELLOW,stroke_width=4).move_to([cx,cy,0])
    iris=Circle(radius=w*.24,stroke_width=0,fill_color=GREY,fill_opacity=.6).move_to(eye)
    pup=Circle(radius=w*.16,stroke_width=0,fill_color=BG,fill_opacity=1).move_to(eye)
    g=VGroup(eye,iris,pup); g.pup=pup; return g

def mouse(x,y):
    return VGroup(Ellipse(width=2.6,height=1.4,color=GREY,fill_opacity=.15).move_to([x,y,0]),
       Circle(radius=.43,color=GREY,fill_opacity=.15).move_to([x+.8,y+.62,0]),
       Dot([x+1.05,y+.15,0],radius=.07,color=TEXT),
       Line([x-1.3,y,0],[x-1.9,y+.35,0],color=GREY,stroke_width=4))
def person(x,y):
    return VGroup(Circle(radius=.4,color=GREY,stroke_width=4).move_to([x,y+1.25,0]),
       RoundedRectangle(width=1.5,height=1.8,corner_radius=.3,color=GREY,fill_opacity=.12).move_to([x,y-.05,0]),
       Line([x-.45,y-.95,0],[x-.45,y-1.8,0],color=GREY,stroke_width=6),
       Line([x+.45,y-.95,0],[x+.45,y-1.8,0],color=GREY,stroke_width=6))
def grating(x,y,w=4,h=2.6,n=4,contrast=1):
    # Equal-area light/dark bands: luminance .5 +/- .5*contrast, mean .5.
    colors=[rgb_to_color([.5+sign*.5*contrast]*3) for sign in [-1,1]]
    bands=VGroup(*[Rectangle(width=w/(2*n),height=h,stroke_width=0,fill_color=colors[i%2],fill_opacity=1)
                    .move_to([x-w/2+(i+.5)*w/(2*n),y,0]) for i in range(2*n)])
    return VGroup(bands,Rectangle(width=w,height=h,color=GREY,stroke_width=2).move_to([x,y,0]))

def spectrum(w):
    # Same alpha-band nomogram as chapter 2; peak set to human lens-corrected estimate.
    p=480.; x=p/np.asarray(w); a=.8795+.0459*np.exp(-(p-300)**2/11940)
    return 1/(np.exp(69.7*(a-x))+np.exp(28*(.922-x))+np.exp(-14.9*(1.104-x))+.674)


def panel(x,y,w,h):
    return RoundedRectangle(width=w,height=h,corner_radius=.18,color=GREY,stroke_width=2).move_to([x,y,0])
def arrow_between(a,b,color=GREEN):
    return arr(a.get_right(),b.get_left(),color,6)
def prediction():
    c=body(-4.6,0); l=box('learning',3.7,1.7); m=box('mood',3.7,-1.7)
    return VGroup(head('Same output, or different outputs?'),c,l,m,
        arr(c.get_right(),l.get_left(),GREY),arr(c.get_right(),m.get_left(),GREY),lab('?',0,0,80,YELLOW))
def routes():
    c=body(-4.7,0); scn=box('SCN',0,1.65); learn=box('learning',4.5,1.65)
    phb=box('PHb',0,-1.65); mood=box('mood',4.5,-1.65)
    a=VGroup(Line(c.get_right(),[-2.8,0,0],color=GREEN,stroke_width=6),
        arr([-2.8,0,0],scn.get_left(),GREEN,6))
    b=arr([-2.8,0,0],phb.get_left(),GREEN,6)
    return VGroup(c,scn,learn,phb,mood,a,b,arrow_between(scn,learn,PURPLE),arrow_between(phb,mood,PURPLE))
def result_base(normal=False):
    m=mouse(-3.5,.55)
    if not normal:
        # A flat back and dropped muzzle distinguish immobility from the upright control.
        m=VGroup(Ellipse(width=2.8,height=.65,color=GREY,fill_opacity=.15).move_to([-3.6,.25,0]),
            Ellipse(width=.85,height=.6,color=GREY,fill_opacity=.15).move_to([-2.25,.02,0]),
            Circle(radius=.22,color=GREY,fill_opacity=.15).move_to([-2.5,.4,0]),
            Dot([-1.98,.02,0],radius=.06,color=TEXT),
            Line([-5,.25,0],[-5.5,.15,0],color=GREY,stroke_width=4),
            Line([-4.6,-.1,0],[-2,-.1,0],color=GREY,stroke_width=3))
    else: m.rotate(.22)
    g=VGroup(panel(-3.3,-.15,5.7,5.5),panel(3.15,-.15,5.9,5.5),
        lab('mouse behaviour',-3.3,2.1,30),lab('hippocampal potentiation',3.15,2.1,28),m,
        lab('qualitative comparison',3.15,-3.1,28,GREY))
    # Ordinal bars only: heights are symbolic, never measured effect sizes.
    g.add(Line([.7,-1.5,0],[5.6,-1.5,0],color=GREY),
          lab('control',1.9,-1.95,28,GREY),lab('T7',4.2,-1.95,28,YELLOW))
    control=Rectangle(width=1.15,height=2.4,color=GREY,fill_opacity=.35).move_to([1.9,-.3,0])
    result=Rectangle(width=1.15,height=2.4 if normal else 1.0,color=GREEN if normal else RED,fill_opacity=.4)
    result.move_to([4.2,-1.5+result.height/2,0])
    return g,control,result

class S00Title(TitleCard):
    LESSON='Melanopsin Cells: Light for the Clock and the Pupil'
    TITLE='Beyond the Clock: Mood, Learning, Seeing and People'
    def construct(self):
        self.add(lab('BIOCHEMISTRYPEDIA',0,2.8,28,TEAL),lab('Melanopsin Cells: Light for the Clock and the Pupil',0,1.8,28,GREY))
        self.play(FadeIn(lab('Beyond the Clock:\nMood, Learning,\nSeeing and People',0,-.5,48)),run_time=.6); self.finish()

class S01Q(SpokenScene):
    def construct(self):
        c=body(-4.7,0); ck=clock_icon(-.3,1.6,.7); eye=eye_icon(-.3,-1.6,1.8)
        self.add(head('Apart from sleep?'),c,ck,eye,lab('pupil',-.3,-2.5,28,YELLOW))
        self.at('Light sets'); self.play(GrowArrow(arr(c.get_right(),[-1.2,1.6,0],GREEN)),GrowArrow(arr(c.get_right(),[-1.3,-1.6,0],GREEN)),run_time=.6)
        a=box('? mood',4.5,1.6); b=box('? learning',4.5,-1.6)
        self.at('can it'); self.play(FadeIn(a),FadeIn(b),
            GrowArrow(arr(c.get_right()+UP*.25,a.get_left(),PURPLE)),
            GrowArrow(arr(c.get_right()+DOWN*.25,b.get_left(),PURPLE)),run_time=.6); self.finish()

class S02T7(SpokenScene):
    def construct(self):
        self.add(head('LeGates and colleagues • 2012'),mouse(-3.5,0),lab('mice',-3.5,-1.7,30),clock_icon(2,0,2.4))
        self.at('with a'); self.play(FadeIn(lab('T7: a repeating 7-hour cycle',0,-3,32,YELLOW)),run_time=.4); self.finish()

class S03T7b(SpokenScene):
    def construct(self):
        center=np.array([0,.25,0]); r=2.6
        wedges=VGroup()
        for i in range(7):
            hours=min(3.5,24-3.5*i); angle=TAU*hours/24
            wedges.add(Sector(radius=r,start_angle=PI/2-TAU*3.5*i/24-angle,angle=angle,
                color=YELLOW if i%2==0 else GREY,fill_opacity=.4 if i%2==0 else .18,stroke_width=2).move_arc_center_to(center))
        hand=Line(center,center+[0,r*.94,0],color=TEXT,stroke_width=5)
        self.add(head('T7 repeated across a 24-hour dial'),wedges,hand)
        self.at('hours of light'); self.play(FadeIn(lab('3.5 h\nlight',.9,1.95,28,YELLOW)),run_time=.35)
        self.at('hours of dark'); self.play(FadeIn(lab('3.5 h\ndark',1.85,.55,28)),run_time=.35)
        self.at('again and again'); self.play(Rotate(hand,-TAU,about_point=center),FadeIn(lab('24 / 7 ≈ 3.4 cycles per day',0,-3,34,YELLOW)),run_time=1); self.finish()

class S04Result(SpokenScene):
    def construct(self):
        g,control,result=result_base(); self.add(head('T7 mice'),g,control)
        self.at('depression'); self.play(FadeIn(lab('depression-like',-3.3,-1.45,32,RED)),run_time=.4)
        self.at('potentiation in'); self.play(FadeIn(result),run_time=.5)
        self.at('was impaired'); self.play(FadeIn(lab('smaller',4.2,1.3,28,RED)),run_time=.35); self.finish()

class S05Ablate(SpokenScene):
    def construct(self):
        g,control,result=result_base(True); c=VGroup(cell(-3.3,-1.65,1.7,.75),lab('ipRGC',-3.3,-1.65,28,GREEN))
        self.add(head('T7 mice • ipRGCs ablated'),g,control,c,cross([-4.15,-1.65,0],.25))
        self.at('did not show'); self.play(FadeIn(result),FadeIn(lab('no T7 change',-3.3,-.7,30,GREEN)),FadeIn(lab('preserved',4.2,1.3,28,GREEN)),run_time=.5); self.finish()

class S06Controls(SpokenScene):
    def construct(self):
        self.add(head('Control 1 of 2: total sleep'),lab('total sleep',-4.5,1,30,BLUE))
        for x,name in [(-1.3,'control'),(3.2,'T7')]:
            self.add(Rectangle(width=2,height=3.7,color=BLUE,fill_opacity=.35).move_to([x,.2,0]),lab(name,x,-2.2,32))
        self.add(foot('Equal schematic bars • earlier work'))
        self.at('preserved'); self.play(FadeIn(lab('preserved',0,2.6,32,BLUE)),run_time=.4); self.finish()

class S07Controls2(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,2.3,.5],y_range=[-1.2,1.2,1],x_length=10.5,y_length=4.1,tips=False,axis_config={'include_ticks':False,'color':GREY}).move_to([.4,-.25,0])
        normal=ax.plot(lambda t:np.sin(TAU*t),x_range=[0,2.3,.01],color=GREY,use_smoothing=False)
        longer=ax.plot(lambda t:np.sin(TAU*t/1.07),x_range=[0,2.3,.01],color=YELLOW,use_smoothing=False)
        self.add(head('Control 2 of 2: clock'),ax,normal,lab('clock output',-4.6,2.5,28,GREY),lab('time →',5,-2.8,28),foot('Phase schematic • modest stretch, not measured size'))
        self.at('clock stayed'); self.play(Create(longer),run_time=.6)
        self.at('period lengthened')
        for y,p,name,color in [(1.6,1,'control period',GREY),(2.2,1.07,'T7 period',YELLOW)]:
            a=ax.c2p(.25,0); b=ax.c2p(.25+p,0); a[1]=b[1]=y
            self.add(Line(a,b,color=color),Line(a+DOWN*.1,a+UP*.1,color=color),Line(b+DOWN*.1,b+UP*.1,color=color),lab(name,3.6,y,28,color))
        self.finish()

class S08Limit(SpokenScene):
    def construct(self):
        pigment=box('melanopsin',3.2,.65,GREEN,32)
        self.add(head('What the experiment establishes'),panel(-3.2,.65,6,4.2),panel(3.2,.65,6,4.2),
            lab('cells (ablation)',-3.2,2.15,32),lab('pigment (knockout)',3.2,2.15,32),
            body(-3.2,.65),pigment)
        self.at('any ablation'); self.play(Create(cross([-3.2,.65,0],.65)),run_time=.4)
        self.at('not the pigment'); self.play(Create(cross(pigment.get_center(),.55)),
            FadeIn(lab('pigment removed',3.2,-.55,28,RED)),
            FadeIn(lab('cells, not pigment',-3.2,-.55,30,YELLOW)),run_time=.4)
        self.at('mouse assay'); self.play(FadeIn(VGroup(panel(0,-2.5,12.4,1.65),mouse(-4.5,-2.5).scale(.55),person(4.8,-2.5).scale(.38),lab('?',5.7,-2.5,38,YELLOW),lab('mouse assay ≠ diagnosis',0,-2.5,32))),run_time=.4); self.finish()

class S09Predict(SpokenScene):
    def construct(self):
        self.add(prediction()); self.at('Predict'); self.play(Indicate(self.mobjects[0][-1]),run_time=.5); self.finish()
class S10Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction(),lab('Pause and predict',0,-3.05,38,YELLOW))
        n=lab('5',0,-1.9,48,YELLOW); self.add(Circle(radius=.62,color=YELLOW,stroke_width=4).move_to(n),n)
        for i in range(5,0,-1):
            n.become(lab(str(i),0,-1.9,48,YELLOW)); self.wait(1)

class S11Reveal(SpokenScene):
    def construct(self):
        g=routes().scale(1.08).shift(DOWN*.25)
        # Match the following scene's one-cell branching layout; enlarge the active targets.
        g[1].scale(1.2); g[2].scale(1.15)
        g[7]=arrow_between(g[1],g[2],PURPLE)
        self.add(head('Fernandez and colleagues • 2018'),g[0],g[1],g[5])
        other=box('other targets',.4,-2.1,GREY,32)
        hedge=VGroup(DashedLine(g[5][0].get_end(),other.get_left(),color=GREY),other,
            lab('minor projections\nnot excluded',3.9,-2.1,32,TEXT))
        self.at('Cells projecting'); self.play(FadeIn(hedge),run_time=.4)
        self.at('were sufficient'); self.play(Create(g[7]),FadeIn(g[2]),run_time=.6)
        self.finish()

class S12Phb(SpokenScene):
    def construct(self):
        g=routes()
        g[6]=VGroup(Line([-2.8,0,0],[-2.8,-1.65,0],color=GREEN,stroke_width=6),arr([-2.8,-1.65,0],g[3].get_left(),GREEN,6))
        self.add(head('One ipRGC schematic • two paths'),g[0],g[1],g[2],g[5],g[7])
        self.at('A separate path'); self.play(Create(g[6]),FadeIn(g[3]),run_time=.5)
        self.at('region next'); self.play(FadeIn(lab('perihabenular region',0,-.95,28,PURPLE)),FadeIn(VGroup(Ellipse(width=2.4,height=.85,color=GREY,fill_opacity=.12).move_to([0,-2.8,0]),lab('habenula',0,-2.8,28,GREY),Line([0,-2.02,0],[0,-2.37,0],color=GREY,stroke_width=2))),run_time=.5)
        self.at('carried the mood'); self.play(Create(g[8]),FadeIn(g[4]),run_time=.5); self.finish()

class S13Phb2(SpokenScene):
    def construct(self):
        a=box('PHb',-3.6,1.15,PURPLE,50); b=box('normal mood',3,1.15,PURPLE,38)
        route=arrow_between(a,b,PURPLE)
        self.add(head('In the tested paradigms'),a,b,route)
        self.at('silencing this region'); self.play(FadeIn(box('silenced',-3.6,2.3,RED,34)),Create(Line(a.get_left()+DOWN*.35,a.get_right()+UP*.35,color=RED,stroke_width=10)),run_time=.4)
        self.at('prevented'); new_b=box('change prevented',3,1.15,PURPLE,38)
        self.play(Transform(b,new_b),Transform(route,arrow_between(a,new_b,PURPLE)),run_time=.4)
        c=box('PHb',-3.6,-2.25,PURPLE,50); d=box('mood-like change',3,-2.25,PURPLE,38)
        self.at('Activating'); self.play(FadeIn(c),FadeIn(lab('activated',-3.6,-1.1,34,PURPLE)),run_time=.4)
        self.at('enough to produce'); self.play(GrowArrow(arrow_between(c,d,PURPLE)),FadeIn(d),run_time=.5); self.finish()

class S14HumanQ(SpokenScene):
    def construct(self):
        p=person(-4.3,0).scale(1.25); a=box('PHb',-.9,.5,GREY,36); b=box('mood',4,.5,GREY,36)
        self.add(head('Matching human circuit?'),p,a,b,DashedLine(a.get_right(),b.get_left(),color=GREY),lab('? • not tested',1.7,-1,38,YELLOW),foot('Human circuit not tested')); self.finish()

class S15Vision(SpokenScene):
    def construct(self):
        a=VGroup(cell(-4,1.6,3.3,1.7),lab('M5 ipRGC',-4,1.6,32,GREEN)); b=VGroup(cell(-4,-1.6,3.3,1.7),lab('M6 ipRGC',-4,-1.6,32,GREEN)); d=box('dLGN',3.5,0,PURPLE,48)
        self.add(head('Seeing patterns'),a,b,d,arr(a.get_right(),d.get_left(),GREEN,7),arr(b.get_right(),d.get_left(),GREEN,7))
        self.at('thalamic visual relay'); self.play(FadeIn(lab('thalamic visual relay',3.2,-2,30,PURPLE)),run_time=.5); self.wait(1.2); self.finish()

class S16Grating(SpokenScene):
    def construct(self):
        self.add(head('Rod and cone signalling removed'),grating(-4.1,1.1,3.1,2.2,2),grating(0,1.1,3.1,2.2,9),Rectangle(width=3.1,height=2.2,color=GREY,fill_color=rgb_to_color([.5]*3),fill_opacity=1).move_to([4.1,1.1,0]),lab('coarse stripes',-4.1,-.4,28),lab('fine stripes',0,-.4,28),lab('grey',4.1,-.4,28))
        self.at('could tell'); self.play(FadeIn(lab('discriminated',-4.1,2.65,28,GREEN)),run_time=.4)
        self.at('only very coarse'); self.play(FadeIn(lab('not discriminated',0,2.65,28,RED)),run_time=.4)
        self.add(lab('Finest grating told from grey (cycles/degree)',0,-1.35,28))
        for y,value,name,col in [(-2.05,.16,'rod/cone signals\nremoved',YELLOW),(-2.85,.55,'normal mice (wild type)',GREY)]:
            self.add(lab(name,-3.5,y,28,col),Line([-.4,y,0],[5.3,y,0],color=GREY),Dot([-.4+5.7*value/.6,y,0],color=col,radius=.09),lab(str(value),-.4+5.7*value/.6,y+.32,28,col))
        self.finish()

class S17Contrast(SpokenScene):
    def construct(self):
        a=grating(-3.25,.8,5.3,3.4,6,.65); b=grating(3.25,.8,5.3,3.4,6,.65)
        self.add(head('Contrast sensitivity'),a,b,lab('normal mice',-3.25,-1.3,30),lab('melanopsin-less',3.25,-1.3,30),foot('Contrast icon • no measured threshold'))
        self.at('showed deficits'); self.play(Transform(b,grating(3.25,.8,5.3,3.4,6,.18)),
            FadeIn(lab('small deficit',3.25,-2,32,RED)),run_time=.6)
        self.at('secondary role'); self.play(FadeIn(lab('Secondary role',-3.25,-2,34,YELLOW)),run_time=.4); self.finish()

class S18People(SpokenScene):
    def construct(self):
        self.add(head('Zaidi and colleagues • 2007'),person(-3,0).scale(1.2),person(3,0).scale(1.2),lab('participant 1',-3,2.5,30),lab('participant 2',3,2.5,30))
        self.at('two blind adults'); self.play(FadeIn(lab('two profoundly blind adults',0,-2.6,32)),run_time=.4)
        self.at('without functional'); self.play(FadeIn(foot('Without functional rods or cones')),run_time=.4); self.finish()

class S19Woman(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[380,650,50],y_range=[0,1.1,.5],x_length=10.4,y_length=4.5,tips=False,axis_config={'include_ticks':True,'color':GREY}).move_to([.5,0,0])
        self.add(head('One woman • pupil sensitivity'),ax,lab('relative pupil sensitivity',-3.5,2.55,28,GREY),lab('wavelength (nm)',1,-3.2,28,GREY),box('illustrative template',3.65,2.35,GREEN,24))
        for w in [400,500,600]: self.add(lab(str(w),ax.c2p(w,0)[0],-2.7,28,GREY))
        for v in [0,.5,1]: self.add(lab(str(v),-5.2,ax.c2p(380,v)[1],28,GREY))
        curve=ax.plot(lambda w:float(spectrum(w)),x_range=[380,650,1],color=GREEN,use_smoothing=False,stroke_width=6)
        self.at('the pupil',lead=0); self.play(Create(curve),run_time=1.25)
        self.at('480 nanometers'); pt=ax.c2p(480,float(spectrum(480)))
        self.play(FadeIn(Dot(pt,color=YELLOW)),FadeIn(lab('480 nm\nafter lens correction',2.9,1.3,28,YELLOW)),Create(Line(pt,[1.1,1.3,0],color=YELLOW)),run_time=.5); self.finish()

class S20Woman2(SpokenScene):
    def construct(self):
        self.add(head('Same woman • forced-choice test'),lab('Two alternatives, one has light',0,2.35,30),box('A',-3.5,1.25,YELLOW,32),box('B',3.5,1.25,GREY,32),lab('no light',3.5,.55,28,GREY),lab('% correct',-5.4,.1,28),Line([-4,-2.4,0],[-4,.4,0],color=GREY),Line([-4,-2.4,0],[4.6,-2.4,0],color=GREY),foot('Qualitative result • no accuracy value implied'))
        self.at('detected a light'); self.play(FadeIn(lab('light',-3.5,.55,28,YELLOW)),run_time=.35)
        self.at('above chance'); self.play(Create(DashedLine([-4,-1.5,0],[4.6,-1.5,0],color=GREY)),FadeIn(lab('chance',-5,-1.5,28,GREY)),Create(Line([-3.5,-1.5,0],[-3.5,-.45,0],color=GREEN,stroke_width=5)),FadeIn(Dot([-3.5,-.45,0],color=GREEN,radius=.16)),FadeIn(lab('above chance',-1.55,-.45,30,GREEN)),run_time=.45); self.finish()

class S21Man(SpokenScene):
    def construct(self):
        base=Rectangle(width=1.5,height=3.7,color=PURPLE,fill_opacity=.4).move_to([1,-.15,0]); outline=base.copy().set_fill(opacity=0).set_stroke(opacity=.5)
        self.add(head('One man'),person(-3.7,-.2).scale(1.2),base,outline,lab('melatonin',2.5,2.5,32,PURPLE),Line([-.2,-2,0],[4.5,-2,0],color=GREY),lab('dark/dim baseline',3.8,1.7,28,GREY),foot('Qualitative suppression • not to scale'))
        self.at('light of'); self.play(FadeIn(box('460 nm',-3.7,2.5,YELLOW,32)),FadeIn(Dot([-5.7,1.7,0],color=YELLOW,radius=.14)),Create(Polygon([-5.7,1.7,0],[-4.2,.8,0],[-2.8,.8,0],color=YELLOW,fill_opacity=.18)),run_time=.4)
        self.at('suppressed melatonin'); self.play(base.animate.stretch_to_fit_height(1.5).move_to([1,-1.25,0]),FadeIn(lab('with 460 nm light',3.8,-.6,28,YELLOW)),run_time=.5); self.finish()

class S22Existence(SpokenScene):
    def construct(self):
        self.add(head('Two people • keep the results separate'),person(-3.3,0),person(3.3,0),lab('woman',-3.3,2.3,32),lab('man',3.3,2.3,32),lab('pupil + detection',-3.3,-2.2,30),lab('melatonin',3.3,-2.2,30),Line([0,-2.4,0],[0,1.9,0],color=GREY))
        self.at('existence proof'); self.play(FadeIn(lab('Existence proof • not a population result',0,-3,32,YELLOW)),run_time=.4); self.finish()

def readers():
    tablet=VGroup(RoundedRectangle(width=2.7,height=3.3,corner_radius=.2,color=GREY),Rectangle(width=2.3,height=2.8,stroke_width=0,fill_color=TEXT,fill_opacity=.95)).move_to([-3,0,0])
    book=VGroup(Rectangle(width=3.5,height=2.8,color=GREY,fill_opacity=.12),Line([0,-1.4,0],[0,1.4,0],color=GREY))
    for x in [-1.25,.35]:
        for y in [-.7,-.3,.1,.5,.9]: book.add(Line([x,y,0],[x+.9,y,0],color=GREY,stroke_width=2))
    book.move_to([3,0,0]); return VGroup(tablet,book)
class S23Screens(SpokenScene):
    def construct(self):
        self.add(head('One evening-reading protocol'),readers(),lab('maximum brightness',-3,-2,28,YELLOW),lab('printed book',3,-2,30))
        self.at('about four hours'); self.play(FadeIn(lab('About 4 hours on each of 5 evenings',0,-3.2,30)),run_time=.4)
        for i in range(5): self.add(Line([-1.6+i*.8,2.15,0],[-1.6+i*.8,2.4,0],color=YELLOW),lab(str(i+1),-1.6+i*.8,2.65,28,YELLOW))
        self.finish()

class S24Screens2(SpokenScene):
    def construct(self):
        self.add(head('Melatonin: device vs comparison'))
        # Taller panels fill the stage; caveats occupy their own bottom strip.
        left=VGroup(panel(-3.2,.4,6,4.8),lab('melatonin',-3.2,2.25,32,PURPLE),
            Line([-5.8,-.65,0],[-.6,-.65,0],color=GREY),Line([-5.8,-.65,0],[-5.8,1.85,0],color=GREY))
        for x,h,col in [(-4.6,2.1,GREY),(-1.9,1.5,PURPLE)]:
            left.add(Rectangle(width=1.25,height=h,color=col,fill_opacity=.4).move_to([x,-.65+h/2,0]))
        left.add(lab('dim-light test',-4.6,-1.12,26),lab('device',-1.9,-1.12,28,PURPLE),lab('illustrative, not to scale',-3.2,-1.7,26,GREY))
        self.add(left,panel(3.2,.4,6,4.8),lab('melatonin starts rising',3.2,2.25,28))
        self.at('rise came later'); self.play(GrowArrow(arr([.7,.3,0],[5.9,.3,0],GREY)),run_time=.4)
        for x,name,col in [(1.6,'print',GREY),(4.9,'device',PURPLE)]: self.add(Line([x,.05,0],[x,.55,0],color=col),lab(name,x,1.05,30,col))
        self.add(lab('evening →',3.2,-1.1,30,GREY))
        self.at('But the study'); self.play(FadeIn(lab('Spectrum and brightness not separated\nNo ipRGC manipulation • Link inferred',0,-2.8,30,YELLOW)),run_time=.4); self.finish()

class S25Take(SpokenScene):
    def construct(self):
        self.add(head('Across these mouse results'),lab('two inputs → one cell',-.8,2.45,28))
        cells=[]; targets=[]; inputs=[]
        for y,name in zip([1.55,.3,-.95,-2.2],['clock','pupil','learning','mood']):
            c=VGroup(cell(-.8,y,2,.85),lab('ipRGC',-.8,y,28,GREEN)); t=box(name,4.4,y,YELLOW if name in ['clock','pupil'] else PURPLE,28)
            cells.append(c); targets.append(VGroup(arrow_between(c,t),t))
            inputs.append(VGroup(arr([-4.9,y+.25,0],[-1.85,y+.12,0],BLUE,4),arr([-3.4,y-.25,0],[-1.85,y-.12,0],GREEN,4)))
        self.add(*cells,*targets,*inputs,
            lab('rod/cone signal',-4.7,2.1,24,BLUE),lab('melanopsin',-4.7,1.3,24,GREEN))
        self.at('two light signals'); self.play(Indicate(inputs[0]),run_time=.5)
        c=box('M5/M6',-4.8,-2.95,GREEN,24); t=lab('visual relay: not covered by this picture',1.7,-2.95,24,GREY)
        self.at('does not explain'); self.play(FadeIn(c),Create(DashedLine(c.get_right(),t.get_left(),color=GREY,buff=.15)),FadeIn(t),run_time=.5)
        self.at('cannot test necessity'); self.play(FadeIn(lab('Cannot test necessity in people',0,-3.5,26,YELLOW)),run_time=.4); self.finish()

class S26End(EndCard):
    LINE='In mice, each cell pools two light signals,\nand different cells reach different targets.'
    def construct(self):
        self.add(lab('In mice',0,2.3,36,YELLOW),lab('Each cell pools two light signals.',0,.7,38),lab('Different cells reach different targets.',0,-.5,38),lab('biochemistrypedia.com',0,-2.3,28,TEAL)); self.finish()
