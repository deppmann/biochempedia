"""Chapter 1 repair: schematic anatomy, continuous developmental geometry.
COLOR MAP: PURPLE forebrain; GREEN midbrain; ORANGE hindbrain; TAN cord/tube
wall; BLUE canal and sensory; RED motor; YELLOW directions; PINK section
planes; GREY body. Anatomical contours are schematics, not quantitative traces.
"""
import numpy as np
from bp_style import *
from bp_style import SpokenScene as _SpokenScene
PURPLE='#AC8CDE'
ORANGE='#F29E4C'
TAN='#CCA982'
PINK='#EE8FBE'

class SpokenScene(_SpokenScene):
    # The standard sync log's negative 'late' is time WAITED, not early display.
    # Use zero lead and record actual reveal times after waiting for the transcript.
    def at(self, phrase, lead=0, nth=0):
        target=self.t_of(phrase,nth)
        if target>self.elapsed(): self.wait(np.ceil((target-self.elapsed())*config.frame_rate)/config.frame_rate)
        with open('/tmp/nervous-map-cue-audit.txt','a') as f:
            f.write(f'{os.environ["KX_SCENE_ID"]} {phrase!r}: target={target:.3f} actual={self.elapsed():.3f}\n')

def pt(x,y): return np.array([x,y,0.])
def label(s,x,y,color=TEXT,size=28):
    return T(s,size=size,color=color,line_spacing=1.2).move_to(pt(x,y))
def heading(s): return label(s,0,3.35,size=30)
def path(ps,c,w=5): return VMobject().set_points_as_corners([pt(*p) for p in ps]).set_stroke(c,w)
def blob(ps,c,opacity=.3):
    return VMobject().set_points_smoothly([pt(*p) for p in ps+[ps[0]]]).set_stroke(c,2.5).set_fill(c,opacity)
def callout(s,x,y,target,color=TEXT,size=28):
    t=label(s,x,y,color,size)
    edge=t.get_right() if x<target[0] else t.get_left()
    elbow=pt(edge[0]+(.18 if x<target[0] else -.18),y)
    return VGroup(path([tuple(edge[:2]),tuple(elbow[:2]),target],color,2),Dot(pt(*target),radius=.035,color=color),t)
def arrow(a,b,c=YELLOW): return Arrow(pt(*a),pt(*b),buff=0,color=c,stroke_width=5,max_tip_length_to_length_ratio=.18)

def tube(bent=True):
    ps=[(-3.7,1.45),(.55,1.45),(.55,-2.8)] if bent else [(-4.5,0),(4.5,0)]
    return VGroup(path(ps,TAN,85),path(ps,BLUE,22))
def rule(): return label('A working picture: one hollow tube, bent once',0,3.3,size=28)

def vesicles(five=False):
    # One continuous wall follows the same bent centreline; bulges never cross it.
    g=VGroup(path([(-4.7,1.45),(.55,1.45),(.55,-2.8)],TAN,55))
    specs=[(-3.7,1.45,2.0,2.3,PURPLE),(-1.25,1.45,1.5,1.7,GREEN),(.55,.65,1.9,2.4,ORANGE)]
    if five: specs=[(-4.2,1.45,1.25,2.3,PURPLE),(-2.8,1.45,1.25,1.9,PURPLE),(-1.25,1.45,1.15,1.6,GREEN),(.55,1.25,1.8,1.55,ORANGE),(.55,-.45,1.55,1.55,ORANGE)]
    for x,y,w,h,c in specs:g.add(Ellipse(width=w,height=h,color=c,fill_opacity=.94).move_to(pt(x,y)))
    g.add(path([(-4.7,1.45),(.55,1.45),(.55,-2.8)],BLUE,12).set_z_index(2))
    return g

def adult(level=0):
    # Same lateral hemisphere contour throughout opening and developmental scenes.
    hemi=blob([(-3.5,.1),(-3.7,1.1),(-3,2.2),(-1.7,2.85),(.1,2.8),(1.7,2.2),(2.1,1.2),(1.7,.25),(.6,-.25),(-.4,-.8),(-1.8,-.7),(-2.6,-.4)],PURPLE)
    far=hemi.copy().scale(.96).shift(UP*.32+RIGHT*.3).set_fill(PURPLE,.12).set_stroke(PURPLE,2)
    th=Ellipse(width=1.3,height=.6,color=PURPLE,fill_opacity=.8).move_to(pt(-.35,.35))
    hy=blob([(-1,-.15),(-.35,-.05),(.1,-.4),(-.5,-.65),(-1,-.4)],PURPLE,.85)
    mid=blob([(-.15,-.4),(.65,-.25),(.9,-1.05),(.25,-1.25)],GREEN,.6)
    hind=blob([(.25,-1.1),(.8,-1),(.95,-1.8),(.85,-2.7),(.4,-2.95),(.15,-2),(-.2,-1.65)],ORANGE,.4)
    pons=blob([(.2,-1.2),(-.2,-1.3),(-.35,-1.7),(.1,-2),(.7,-1.9),(.8,-1.35)],ORANGE,.65)
    med=blob([(.25,-2),(.85,-1.9),(.9,-2.7),(.4,-3)],ORANGE,.65)
    cord=path([(.6,-2.85),(.6,-3.25)],TAN,30)
    cb=blob([(.8,-1.2),(1,-.65),(1.65,-.55),(2.45,-.95),(2.5,-1.8),(1.95,-2.25),(1.15,-2.1),(1.35,-1.65)],ORANGE,.65)
    wall=VGroup(far,hemi,th,hy,mid,hind,pons,med,cord)
    water=VGroup()
    if level>=1:
        water.add(blob([(-2.8,1.25),(-2.35,1.65),(-1.25,1.45),(-.5,.7),(-1.35,1.15),(-2.3,1.3)],BLUE,.75),blob([(-2.65,1.9),(-2.1,2.25),(-1.05,1.95),(-.5,.7),(-1.25,1.65),(-2.05,1.92)],BLUE,.55))
    if level>=2:water.add(path([(-.5,.7),(-.5,-.4)],BLUE,9))
    if level>=3:water.add(path([(-.5,-.4),(.4,-.8),(.6,-1.25)],BLUE,7))
    if level>=4:water.add(Polygon(pt(.6,-1.25),pt(1.35,-1.65),pt(.65,-2.25),color=BLUE,fill_opacity=.75,stroke_width=2))
    return wall,water,cb

def adult_scene(s,level=0,cb=False):
    w,a,c=adult(level);s.add(w)
    if cb:s.add(c)
    s.add(a)
    return w,a,c

def section():
    outer=Circle(radius=2.85,color=TAN,fill_opacity=.12)
    canal=Circle(radius=.25,color=BLUE,fill_opacity=.7)
    d=AnnularSector(inner_radius=.45,outer_radius=2.65,angle=PI,start_angle=0,color=BLUE,fill_opacity=.38,stroke_width=0)
    v=AnnularSector(inner_radius=.45,outer_radius=2.65,angle=PI,start_angle=PI,color=RED,fill_opacity=.38,stroke_width=0)
    return VGroup(outer,canal),d,v

def human(bent=True):
    # Rounded skull, brow, short nose, lips and chin in one human profile.
    head=blob([(-1.3,1.3),(-1.9,1.45),(-2.16,1.7),(-2.2,1.98),(-2.34,2.04),(-2.25,2.13),(-2.36,2.2),(-2.28,2.33),(-2.52,2.37),(-2.32,2.61),(-2.28,2.84),(-1.97,3.08),(-1.45,3.15),(-.97,2.88),(-.78,2.45),(-.82,1.9)],GREY,.12)
    nose=VMobject()  # Preserve the shared figure's subobject indices.
    torso=blob([(-1.65,1.3),(-.7,1.3),(0,.6),(.15,-1.3),(-.55,-1.8),(-1.8,-1.6),(-2.15,-.7)],GREY,.12)
    legs=VGroup(path([(-1.6,-1.6),(-1.8,-3.1)],GREY,13),path([(-.5,-1.7),(-.1,-3.1)],GREY,13))
    fore=path([(-2.25,2.25),(-1.2,2.25)],PURPLE,28) if bent else path([(-1.2,2.25),(-1.2,2.9)],PURPLE,28)
    brainstem=VGroup(path([(-1.2,2.25),(-1.1,1.75)],GREEN,28),path([(-1.1,1.75),(-1,1.25)],ORANGE,28))
    cord=path([(-1,1.25),(-1,-1.6)],TAN,25)
    return VGroup(head,nose,torso,legs,fore,brainstem,cord)

def rat():
    body=blob([(-2.9,.25),(-2,1.3),(.3,1.55),(2.7,1),(3,.1),(2.3,-.9),(-1.8,-1),(-2.9,-.5)],GREY,.13)
    head=blob([(-2.9,.6),(-3.65,.85),(-4.9,.1),(-4.4,-.5),(-3,-.6)],GREY,.13)
    ear=Circle(radius=.4,color=GREY,fill_opacity=.15).move_to(pt(-3.15,.8))
    feet=VGroup(*[path([(x,-.7),(x-.3,-2.25),(x-.9,-2.25)],GREY,8) for x in [-2,-.8,1.4,2.3]])
    tail=path([(2.8,.1),(4.2,-.4),(5.6,-1.4)],GREY,7)
    return VGroup(body,head,ear,feet,tail,path([(-4,.15),(-2.8,.15)],PURPLE,30),path([(-2.8,.15),(-1.5,.15)],ORANGE,30),path([(-1.5,.15),(2.6,.15)],TAN,30))

def q1():return VGroup(human(),label('Spinal cord:\nwhich way is dorsal?',3,2.45,size=30),label('?',.2,-.4,YELLOW,70))
def slab(kind):
    ps={'s':[(-2.7,1.2),(-.6,1.45),(-.6,3.15),(-2.7,2.9)],'c':[(-1.5,1),(-.55,1.5),(-.55,3.1),(-1.5,2.6)],'h':[(-3.1,1.65),(.2,1.65),(.9,2.25),(-2.4,2.25)]}[kind]
    top=Polygon(*[pt(*p) for p in ps],color=PINK,fill_opacity=.2,stroke_width=3)
    face=Polygon(pt(*ps[0]),pt(*ps[1]),pt(*ps[1])+DOWN*.12,pt(*ps[0])+DOWN*.12,color=PINK,fill_opacity=.5,stroke_width=1)
    return VGroup(top,face)
def horizontal():
    # A finite-thickness horizontal slab crosses the upper brainstem below the bend.
    return VGroup(human(),slab('h'),arrow((-1.2,2.05),(-2.45,2.05)),label('Horizontal',3,2.8,PINK,30))
def q2():return VGroup(horizontal(),label('Through the brainstem?',2.6,.7,size=28),label('?',-.4,1.5,YELLOW,60))

class S00Title(TitleCard):
    LESSON='The Map: How the Nervous System Is Organized'
    TITLE='One Tube, Bent Once'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,1.7,TEAL,26),label(self.LESSON,0,.8,GREY,26))
        self.play(FadeIn(label(self.TITLE,0,-.3,size=48)),run_time=.8);self.finish()

class S01Question(SpokenScene):
    def construct(self):
        w,a,c=adult();VGroup(w,c).scale(1.06).move_to(pt(-.35,0));self.add(w,c)
        # Explicitly an inventory of names, rather than a regional map.
        left=['Frontal','Temporal','Insula','Thalamus','Hypothalamus','Amygdala']
        right=['Parietal','Occipital','Cerebellum','Midbrain','Pons','Medulla']
        names=VGroup(*[label(n,x,2.6-i*.92,TEXT,28) for ns,x in [(left,-5.25),(right,4.9)] for i,n in enumerate(ns)])
        inventory=label('A list of names',0,3.55,GREY,26)
        self.at('Your brain');self.play(FadeIn(names),FadeIn(inventory),run_time=.3)
        self.at('is one shape');self.play(FadeOut(names),FadeOut(inventory),FadeIn(label('?',-.8,.9,YELLOW,85)),run_time=.4);self.finish()

class S02Tube(SpokenScene):
    def construct(self):
        # Identical 101 points throughout: sheet edges lift and close without a swap.
        def fold(theta):
            u=np.linspace(-theta,theta,101);r=3
            return VMobject().set_points_as_corners([pt(-2.8+r*np.sin(v),-2.8+r*(1-np.cos(v))) for v in u]).set_stroke(TAN,25)
        sheet=Line(pt(-5.8,-2.8),pt(.2,-2.8),color=TAN,stroke_width=25);self.add(sheet)
        self.at('Most neurons');self.play(Transform(sheet,fold(PI*.52)),run_time=1.2)
        self.at('brain and spinal');self.play(Transform(sheet,fold(PI*.82)),run_time=.8)
        self.at('come from the wall');self.play(Transform(sheet,Circle(radius=3,color=TAN,stroke_width=25).move_to(pt(-2.8,.2))),run_time=.8)
        self.at('one tube');self.play(FadeIn(Circle(radius=2.7,color=BLUE,fill_opacity=.15).move_to(pt(-2.8,.2))),FadeIn(VGroup(path([(1,-.4),(5.3,-.4)],TAN,75),path([(1,-.4),(5.3,-.4)],BLUE,22))),run_time=.4)
        self.at('It forms');self.play(FadeIn(label('Along the embryo’s back',2.8,-1.55,size=26)),FadeIn(label('Open ends close: about 4 weeks\nafter fertilization\n(about 6 weeks of pregnancy)',3.2,2.05,GREY,26)),run_time=.35);self.finish()

class S03Rule1(SpokenScene):
    def construct(self):
        t=tube(False);self.add(t)
        self.at('The one idea');self.play(FadeIn(label('A working picture',0,3.3,size=28)),run_time=.3)
        self.at('one hollow tube');self.play(Indicate(t[1],color=BLUE),run_time=.4)
        self.at('bent once');self.play(Transform(t,tube()),FadeOut(self.mobjects[1]),FadeIn(rule()),run_time=.4);self.finish()
class S04Rule2(SpokenScene):
    def construct(self):
        t=tube();self.add(t,rule())
        self.at('Its walls');self.play(FadeIn(callout('Walls → brain parts\nand spinal cord',3.8,1.2,(.55,-.2),TAN,28)),run_time=.35)
        self.at('Its canal');self.play(FadeIn(callout('Canal → ventricles',3.8,-1.8,(.55,-2),BLUE,28)),run_time=.35);self.finish()
class S05Rule3(SpokenScene):
    def construct(self):
        self.add(tube(),rule())
        axis=VGroup(path([(.55,-2.65),(.55,1.45),(-3.2,1.45)],YELLOW,8),arrow((-3.2,1.45),(-3.9,1.45))).set_z_index(4)
        self.at('own long axis');self.play(Create(axis),run_time=.4)
        dirs=VGroup(label('Rostral',-4.9,1.45,YELLOW,26),label('Caudal',1.8,-2.9,YELLOW,26),arrow((-2,1.95),(-2,2.65)),label('Dorsal',-3.5,2.65,YELLOW,26),arrow((-2,.95),(-2,.15)),label('Ventral',-3.5,.15,YELLOW,26),arrow((1.05,-.4),(2.2,-.4)),label('Dorsal',3.1,-.4,YELLOW,26),arrow((.05,-1.8),(-1.05,-1.8)),label('Ventral',-2.1,-1.8,YELLOW,26))
        self.at('direction words');self.play(FadeIn(dirs),run_time=.3);self.finish()
class S06Swell3(SpokenScene):
    def construct(self):
        t=tube();t[1].set_z_index(2);self.add(t)
        self.at('the front end');v=vesicles();self.play(Transform(t[0],v[0]),Transform(t[1],v[-1]),*[GrowFromCenter(m) for m in v[1:-1]],run_time=1)
        self.at('brain');self.play(FadeIn(label('Forebrain',-3.7,3,PURPLE)),run_time=.2)
        self.at('midbrain');self.play(FadeIn(label('Midbrain',-1.2,2.7,GREEN)),run_time=.2)
        self.at('hindbrain');self.play(FadeIn(callout('Hindbrain',3.2,.6,(1.35,.6),ORANGE)),run_time=.2);self.finish();self.wait(.8)
class S07Swell5(SpokenScene):
    def construct(self):
        v=vesicles();self.add(v,label('Forebrain',-3.7,3,PURPLE),label('Midbrain',-1.2,2.7,GREEN),callout('Hindbrain',3.2,.6,(1.35,.6),ORANGE))
        self.at('each divide');new=vesicles(True);self.play(FadeOut(VGroup(*v[1:-1])),*[GrowFromCenter(m) for m in new[1:-1]],run_time=.6)
        self.at('The rest becomes');self.play(FadeIn(callout('Spinal cord',3.4,-2.5,(.55,-2.5),TAN)),run_time=.3);self.finish()
class S08Cerebrum(SpokenScene):
    def construct(self):
        v=vesicles(True);self.add(v);w,a,c=adult(1)
        self.at('buds out');self.play(FadeOut(v),*[GrowFromPoint(m,pt(-2.8,1.45)) for m in w],run_time=.65)
        inset=VGroup(Ellipse(width=1.1,height=1.5,color=PURPLE,fill_opacity=.3).move_to(pt(3.7,1.3)),Ellipse(width=1.1,height=1.5,color=PURPLE,fill_opacity=.3).move_to(pt(4.95,1.3)))
        both=VGroup(label('Two cerebral hemispheres',4.25,2.7,PURPLE,26),path([(4.25,2.4),(4.25,2.2),(3.7,2.05)],PURPLE,2),path([(4.25,2.2),(4.95,2.05)],PURPLE,2),label('Front view',4.3,.25,GREY,24))
        self.at('cerebral hemispheres');self.play(FadeIn(inset),FadeIn(both),run_time=.3)
        self.at('Their canals');self.play(Create(a),run_time=.4)
        self.at('lateral ventricles');self.play(FadeIn(callout('Two lateral\nventricles',-5.1,1,(-2.3,1.6),BLUE)),run_time=.25);self.finish()
class S09Dien(SpokenScene):
    def construct(self):
        w,a,c=adult_scene(self,1)
        self.at('thalamus');self.play(Indicate(w[2]),FadeIn(callout('Thalamus',4.5,1,(.1,.4),PURPLE)),run_time=.25)
        self.at('hypothalamus');self.play(Indicate(w[3]),FadeIn(callout('Hypothalamus',-4.8,-1.3,(-.5,-.4),PURPLE)),run_time=.25)
        self.at('third ventricle');self.play(FadeIn(adult(2)[1][-1]),FadeIn(callout('Third ventricle',4.6,-.4,(-.5,.1),BLUE)),run_time=.25);self.finish()
class S10Aqueduct(SpokenScene):
    def construct(self):
        w,a,c=adult_scene(self,2)
        self.at('The midbrain');self.play(FadeIn(callout('Midbrain',4.6,.7,(.5,-.65),GREEN)),run_time=.25)
        self.at('a narrow canal');self.play(Create(adult(3)[1][-1]),run_time=.3)
        self.at('cerebral aqueduct');self.play(FadeIn(callout('Cerebral\naqueduct',4.7,-1.6,(.3,-.75),BLUE)),run_time=.25);self.finish()
class S11Hind(SpokenScene):
    def construct(self):
        w,a,c=adult_scene(self,3)
        self.at('pons and medulla');self.play(FadeIn(callout('Pons',-4.8,-1.35,(0,-1.6),ORANGE)),FadeIn(callout('Medulla',-4.8,-2.6,(.5,-2.5),ORANGE)),run_time=.3)
        self.at('fourth ventricle');self.play(FadeIn(adult(4)[1][-1]),FadeIn(callout('Fourth ventricle',4.7,-2.3,(1,-1.7),BLUE)),run_time=.25);self.finish()
class S12Cerebellum(SpokenScene):
    def construct(self):
        w,a,c=adult_scene(self,4);self.add(callout('Fourth ventricle',4.7,-2.3,(1,-1.7),BLUE))
        self.at('cerebellum grows');self.play(GrowFromPoint(c,pt(1.1,-1.55)),run_time=.6);self.bring_to_front(a)
        self.at('dorsal side');self.play(FadeIn(callout('Cerebellum',4.8,-.4,(2,-1.3),ORANGE)),GrowArrow(arrow((.9,-1.55),(1.9,-.95))),FadeIn(label('Dorsal',2.2,.35,YELLOW,26)),run_time=.3)
        self.at('fourth ventricle');self.play(Indicate(a[-1]),run_time=.4);self.finish()
class S13Plan(SpokenScene):
    def construct(self):
        r,d,v=section();self.add(r,heading('Embryonic spinal cord · cross-section'))
        self.add(arrow((3.5,-1),(3.5,1)),label('Dorsal',4.6,1,YELLOW,26),label('Ventral',4.6,-1,YELLOW,26))
        self.at('receive sensory signals');self.play(FadeIn(d),FadeIn(callout('Receives sensory\nsignals',-4.8,1.3,(-2,1.2),BLUE,26)),run_time=.35)
        self.at('motor neurons');self.play(FadeIn(v),FadeIn(callout('Motor neurons',-4.8,-1.5,(-2,-1.2),RED,26)),run_time=.35)
        self.at('Sensory fibers');self.play(GrowArrow(arrow((.8,1.6),(.8,-1.6),BLUE)),FadeIn(label('Sensory fibres also reach ventral neurons',0,-3.35,BLUE,26)),run_time=.4);self.finish()
class S14Roots(SpokenScene):
    def construct(self):
        r,d,v=section();self.add(r,d,v,heading('Spinal roots'),label('Dorsal',0,2.35,BLUE,26),label('Ventral',0,-2.35,RED,26))
        fibre=path([(-5.6,1.5),(-3.6,1.5),(-2.5,1.2),(-1.3,.9)],BLUE,9)
        gang=Ellipse(width=1,height=.6,color=BLUE,fill_opacity=.45).move_to(pt(-3.8,1.5));cell=Dot(pt(-3.8,1.5),radius=.13,color=YELLOW)
        self.at('sensory fibers');self.play(Create(fibre),FadeIn(gang),FadeIn(cell),run_time=.4)
        self.at('dorsal roots');self.play(FadeIn(callout('Dorsal root',-4.8,2.55,(-5,1.5),BLUE,26)),FadeIn(callout('Ganglion\n(cell body)',-4.7,-.2,(-3.8,1.5),BLUE,26)),MoveAlongPath(Dot(radius=.09,color=TEXT),fibre),run_time=.5)
        out=path([(1.1,-1),(2.5,-1.25),(4,-1.5),(5.6,-1.5)],RED,9)
        self.at('motor axons');self.play(Create(out),run_time=.35)
        self.at('ventral roots');self.play(FadeIn(callout('Ventral root',4.8,-2.4,(4,-1.5),RED,26)),MoveAlongPath(Dot(radius=.09,color=TEXT),out),run_time=.5);self.finish()
class S15Scope(SpokenScene):
    def construct(self):
        bowl=Polygon(pt(-5.3,1.5),pt(-3.5,.5),pt(-1.7,1.5),pt(-2,-2.5),pt(-5,-2.5),color=TAN,fill_opacity=.16)
        cavity=Polygon(pt(-5.3,1.5),pt(-3.5,.5),pt(-1.7,1.5),color=BLUE,fill_opacity=.3)
        m=VGroup(*[RoundedRectangle(width=.4,height=2.2,corner_radius=.15,color=RED,fill_opacity=.6).move_to(pt(x,-.8)) for x in [-3.9,-3.1]])
        s=VGroup(*[RoundedRectangle(width=.55,height=2.2,corner_radius=.15,color=BLUE,fill_opacity=.6).move_to(pt(x,-.8)) for x in [-4.65,-2.35]])
        self.add(bowl,cavity,m,heading('A plan for where neurons develop'),label('Brainstem',-3.5,2.6,size=30),label('Dorsal',-3.5,1.95,YELLOW,26),label('Ventral',-3.5,-2.9,YELLOW,26))
        self.at('keeps this plan');self.play(FadeIn(label('Motor: medial',.1,-1.1,RED,26)),run_time=.25)
        self.at('sensory nuclei');self.play(FadeIn(s),run_time=.25)
        self.at('to the side');self.play(FadeIn(label('Sensory: lateral',.1,0,BLUE,26)),FadeIn(label('✓',-1.3,2.4,GREEN,48)),run_time=.25)
        w,a,c=adult();fore=VGroup(w[0],w[1]).scale(.48).move_to(pt(4,.5))
        self.at('forebrain does not');self.play(FadeIn(fore),FadeIn(Cross(fore,stroke_color=RED,stroke_width=7)),FadeIn(label('Forebrain',4,2.4,PURPLE,30)),run_time=.35);self.finish()
class S16Rat(SpokenScene):
    def construct(self):
        self.add(rat())
        self.at('nearly straight');self.play(GrowArrow(arrow((-2,.4),(-4.3,.4))),GrowArrow(arrow((1,.4),(3.1,.4))),FadeIn(label('Rostral',-4.2,1.65,YELLOW,26)),FadeIn(label('Caudal',3.2,1.65,YELLOW,26)),run_time=.35)
        self.at('Dorsal is');self.play(GrowArrow(arrow((0,1.55),(0,2.6))),FadeIn(label('Dorsal → back',0,3,YELLOW,28)),GrowArrow(arrow((0,-1),(0,-2.3))),FadeIn(label('Ventral',0,-2.85,YELLOW,26)),run_time=.3);self.finish()
class S17Stand(SpokenScene):
    def construct(self):
        r=rat();ba=arrow((1,1.4),(1,2.4));fa=arrow((-3.7,.5),(-3.7,1.5))
        bl=label('Dorsal',1,2.85,YELLOW,26);fl=label('Dorsal',-3.7,2,YELLOW,26)
        self.add(r,ba,fa,bl,fl)
        self.at('Stand the rat up');self.play(FadeOut(bl),FadeOut(fl),run_time=.2)
        target=r.copy().scale(.78).rotate(-PI/6)
        x,y=target[5].get_center()[:2]
        self.play(Transform(r,target),ba.animate.rotate(-PI/6,about_point=ORIGIN),Transform(fa,arrow((x,y+.25),(x,y+1.25))),run_time=.45)
        self.at('face pointing forward')
        # Transform one figure into the next: no overlapping transparent silhouettes.
        h=human(False)
        self.play(Transform(r,h),Transform(ba,arrow((-.8,.2),(.7,.2))),Transform(fa,arrow((-1.2,2.9),(-1.2,3.5))),run_time=.6)
        self.at('body cord and brainstem');self.play(FadeIn(label('Dorsal · cord / brainstem',3,.2,YELLOW,26)),run_time=.3)
        self.at('only the forebrain');self.play(FadeIn(label('Dorsal · forebrain',3,3.1,YELLOW,26)),run_time=.3);self.finish()
class S18Bend(SpokenScene):
    def construct(self):
        def enlarged(bent=True):return human(bent).scale(1.07,about_point=ORIGIN).shift(RIGHT*1.3+DOWN*.1)
        h=enlarged(False);self.add(h)
        self.at('tube bends');self.play(Transform(h,enlarged()),run_time=.5)
        mark=path([(-.42,2.31),(-.42,1.88),(.02,1.88)],YELLOW,4)
        self.at('a right angle');self.play(Create(mark),FadeIn(label('Roughly a right angle',3.8,3.25,YELLOW,26)),run_time=.3)
        self.at('midbrain meets');self.play(FadeIn(callout('Midbrain',-4.5,1.1,(.1,1.95),GREEN,26)),FadeIn(callout('Diencephalon',-4.5,2.8,(-.55,2.31),PURPLE,26)),run_time=.3)
        inset=path([(3.1,-2.3),(3.1,-1.1),(3.85,-.35),(4.6,-1.1),(5.55,-.15)],TAN,18)
        self.at('embryo bends');self.play(Create(inset),FadeIn(label('Embryo · three bends',4.4,1.2,size=26)),run_time=.35)
        self.at('three places');self.play(FadeIn(VGroup(Dot(pt(3.1,-1.1),color=GREY),Dot(pt(3.85,-.35),color=GREY),Dot(pt(4.6,-1.1),color=GREEN))),FadeIn(callout('Cervical',2.9,-2.85,(3.1,-1.1),GREY,24)),FadeIn(VGroup(label('Pontine',3.7,.35,GREY,24),path([(3.7,.12),(3.85,-.35)],GREY,2))),FadeIn(callout('Midbrain',5.6,-2,(4.6,-1.1),GREEN,24)),Create(path([(4.39,-.89),(4.6,-.68),(4.81,-.89)],YELLOW,3)),run_time=.35)
        self.at('This one matters');self.play(Indicate(inset,color=YELLOW),FadeIn(label('This bend sets the naming frame',3.5,-3.45,YELLOW,24)),run_time=.3);self.finish()
class S19Predict2(SpokenScene):
    def construct(self):
        q=q1();self.add(q[0]);self.at('In your spinal cord');self.play(FadeIn(q[1]),run_time=.25);self.at('which way');self.play(FadeIn(q[2]),run_time=.25);self.finish()
class S20Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(q1())
        for n in range(5,0,-1):
            t=label(f'Think · {n}',3,-2,YELLOW,30);self.add(t);self.wait(1);self.remove(t)
class S21Reveal2(SpokenScene):
    def construct(self):
        q=q1();self.add(q)
        self.at('your back');self.play(FadeOut(q[1]),FadeOut(q[2]),GrowArrow(arrow((-.8,-.5),(1,-.5))),FadeIn(label('Cord · dorsal: back',3.4,-.5,YELLOW,26)),run_time=.3)
        self.at('brainstem uses');self.play(GrowArrow(arrow((-1.02,1.7),(.55,2.014))),FadeIn(label('Brainstem · dorsal: back',3.5,1.45,YELLOW,26)),run_time=.3)
        self.at('dorsal points');self.play(GrowArrow(arrow((-1.8,2.39),(-1.8,3.5))),FadeIn(label('Forebrain · dorsal: top',2.9,3.15,YELLOW,26)),run_time=.3);self.finish()
class S22Planes(SpokenScene):
    def construct(self):
        self.add(human())
        for cue,k,txt,y in [('sagittal','s','Sagittal · left / right',2.7),('coronal','c','Coronal · front / back',1),('horizontal','h','Horizontal · top / bottom',-.7)]:
            self.at(cue);self.play(FadeIn(slab(k),shift=RIGHT*.5),FadeIn(label(txt,3.1,y,PINK,28)),run_time=.25)
        self.finish();self.wait(1)
class S23Predict3(SpokenScene):
    def construct(self):
        q=q2();self.add(q[0][0]);self.at('A horizontal cut');self.play(FadeIn(q[0][1]),FadeIn(q[0][3]),run_time=.3)
        self.at('along the');self.play(GrowArrow(q[0][2]),run_time=.25)
        self.at('How does it');self.play(FadeIn(q[1]),FadeIn(q[2]),run_time=.25);self.finish()
class S24Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(q2())
        for n in range(5,0,-1):
            t=label(f'Think · {n}',3,-2,YELLOW,30);self.add(t);self.wait(1);self.remove(t)
class S25Reveal3(SpokenScene):
    def construct(self):
        q=q2();self.add(q)
        self.at('roughly across it');self.play(FadeOut(q[1]),FadeOut(q[2]),FadeIn(label('Roughly transverse',3,.7,PINK,28)),Create(path([(-1.1,1.68),(-.75,1.68),(-.75,2.03)],YELLOW,4)),run_time=.3)
        self.at('axis runs');self.play(GrowArrow(arrow((-1.05,1),(-1.05,2.45))),FadeIn(label('≈ 90°',.5,1.5,YELLOW,28)),run_time=.3);self.finish()
class S26Close(SpokenScene):
    def construct(self):
        # Turn the same bent tube so its tail points away from the mapping lanes.
        t=vesicles(True).rotate(-PI/2).scale(.78).move_to(pt(-3.5,0))
        w,a,c=adult(4);b=VGroup(w,c,a).scale(.78).move_to(pt(2.5,-.1));self.add(t,b)
        fore=t[2].get_right();mid=t[3].get_right();hind=t[4].get_right()
        fore_target=w[1].get_left()
        mid_target=w[4].get_center()+LEFT*.22+DOWN*.12
        hind_target=w[7].get_left()
        ties=VGroup(path([tuple(fore[:2]),(-.2,fore[1]),(-.2,fore_target[1]),tuple(fore_target[:2])],PURPLE,3),path([tuple(mid[:2]),(-.4,mid[1]),(-.4,mid_target[1]),tuple(mid_target[:2])],GREEN,3),path([tuple(hind[:2]),(-.6,hind[1]),(-.6,hind_target[1]),tuple(hind_target[:2])],ORANGE,3))
        names=VGroup(callout('Forebrain',-4.8,2.75,tuple(t[1].get_left()[:2]),PURPLE,24),callout('Midbrain',-4.8,-.35,tuple(t[3].get_left()[:2]),GREEN,24),callout('Hindbrain',-4.8,-2.85,tuple(t[5].get_bottom()[:2]),ORANGE,24))
        self.at('tube tells you');self.play(FadeIn(heading('The tube tells you where things are.')),Create(ties),FadeIn(names),run_time=.4)
        self.at('What each place does');self.play(FadeIn(label('What each place does?',0,-3.35,TEAL,32)),run_time=.3);self.finish()
class S27End(EndCard):
    LINE='The tube tells you where things are.'
    def construct(self):
        self.play(FadeIn(label(self.LINE,0,.35,size=40)),run_time=.6)
        self.play(FadeIn(label('biochemistrypedia.com',0,-.6,TEAL,26)),run_time=.3);self.finish()
