"""Word-timed schematic anatomy, redrawn after the frame review.
COLOR MAP: BLUE fluid/anatomical routes; TEAL endothelium/seals; RED plexus/plug;
YELLOW protein tracer; WHITE layer emphasis; GREY basement membrane/neutral labels;
TAN astrocyte endfeet/tube wall; PURPLE forebrain; ORANGE hindbrain;
DEPOSIT near-black brown is the tracer's reaction product, distinct from tracer.
Dilution model: dC/dv=-C, C/C0=exp(-v). No sketched data traces.
"""
import numpy as np
from bp_style import *
PURPLE, ORANGE, TAN = '#AC8CDE', '#F29E4C', '#CCA982'
DEPOSIT, DARK_BLUE = '#21130D', '#174EAD'
def p(x,y): return np.array([x,y,0.])
def lab(s,x,y,c=TEXT,size=28): return T(s,size=size,color=c).move_to(p(x,y))
def line(points,c=BLUE,w=5): return VMobject().set_points_as_corners([p(*v) for v in points]).set_stroke(c,w)
def arr(a,b,c=BLUE): return Arrow(p(*a),p(*b),buff=0,stroke_width=5,color=c)
def head(s): return lab(s,0,3.35,size=32)
def leader(s,xy,target,c=TEXT,size=28):
    t=lab(s,*xy,c,size); side=t.get_left() if target[0]<xy[0] else t.get_right()
    return VGroup(Line(side+(.12*LEFT if target[0]<xy[0] else .12*RIGHT),p(*target),color=c,stroke_width=2),t)

# Separated lateral chambers keep both visible in a schematic side projection.
VC=[(-2.4,1.7),(-2.4,.7),(-.2,.6),(1,-1.25)]
def anatomy():
    wall=VGroup(Ellipse(width=7.4,height=4.4,color=PURPLE,fill_opacity=.12).move_to(p(-1.1,.65)),
        Ellipse(width=2.5,height=1.65,color=ORANGE,fill_opacity=.16).move_to(p(1.45,-1.15)),
        Polygon(p(.15,-.6),p(1.1,-.6),p(1.4,-2),p(1,-2.7),p(.7,-3.1),p(.2,-3.1),p(.4,-2),color=TAN,fill_opacity=.22))
    v=VGroup(*[Ellipse(width=2.5,height=.56,color=BLUE,fill_opacity=.8).move_to(p(*q)) for q in VC[:2]],
        Ellipse(width=.42,height=1.25,color=BLUE,fill_opacity=.9).move_to(p(*VC[2])),
        Polygon(p(.65,-.85),p(1.7,-1.3),p(.65,-1.8),color=BLUE,fill_opacity=.85))
    for a in v:
        a.set_stroke(BLUE,3,opacity=.9);a.set_background_stroke(color=BLUE,width=18,opacity=.16)
    links=VGroup(line([(-1.15,1.7),(-.2,1.05)]),line([(-1.15,.7),(-.2,.7)]),line([(-.2,0),(.45,-.35),(.65,-.85)],w=9))
    return wall,v,links

def anatomy_labels():
    return VGroup(leader('Lateral ventricles',(-4.3,2.9),(-2.5,2),BLUE,26),
        leader('Third',(3.9,1.6),(.05,.75),BLUE,26),leader('Aqueduct',(4.1,.15),(.4,-.3),BLUE,26),
        leader('Fourth',(4.1,-1.4),(1.6,-1.3),BLUE,26))
def flow(): return VGroup(arr((-1.5,1.6),(-.35,1.05)),arr((-1.5,.65),(-.35,.65)),arr((-.05,-.05),(.5,-.65)),arr((.8,-.95),(1.3,-1.3)))
def outside():
    outer=VMobject().set_points_smoothly([p(*a) for a in [(-5.1,.6),(-4.2,2.6),(-1,3.05),(2.7,1.5),(3,-1),(2.5,-2.1),(1.3,-2.6),(1,-3.35),(-.05,-3.35),(-.05,-2.4),(-.9,-1.8),(-3.8,-1.6),(-5.1,.6)]])
    outer.set_fill(BLUE,.10).set_stroke(BLUE,4)
    return outer

def plug_question():
    w,v,l=anatomy();plug=Rectangle(width=.72,height=.25,color=RED,fill_opacity=1).move_to(p(.4,-.35))
    return VGroup(w,v,l,plug,lab('Which ventricles swell?',3.7,2.5,size=28),lab('Secretion continues',3.8,-2.6,BLUE,26))

def section(x=-2.6):
    center=p(x,0)
    lumen=Circle(radius=1.55,color=TEXT,stroke_width=2,fill_color='#B9B2A2',fill_opacity=.85).move_to(center)
    cells=VGroup(*[AnnularSector(inner_radius=1.55,outer_radius=2.03,start_angle=a+.018,angle=TAU/4-.036,
        color=TEAL,fill_opacity=.65,stroke_width=2).shift(center) for a in np.arange(4)*TAU/4])
    base=Annulus(inner_radius=2.06,outer_radius=2.29,color=GREY,fill_opacity=.9,stroke_width=0).move_to(center)
    # Scalloped feet share the band's outer edge and wrap continuously around it.
    feet=VGroup()
    for a in np.linspace(0,TAU,10,endpoint=False):
        angles=np.linspace(a+.006,a+TAU/10-.006,16)
        outer=[center+(2.46+.39*np.sin(PI*i/15))*p(np.cos(t),np.sin(t)) for i,t in enumerate(angles)]
        inner=[center+2.29*p(np.cos(t),np.sin(t)) for t in angles[::-1]]
        foot=VMobject().set_points_as_corners(outer+inner+[outer[0]])
        feet.add(foot.set_fill(TAN,.6).set_stroke(TAN,2))
    seams=VGroup(*[Line(center+1.56*p(np.cos(a),np.sin(a)),center+2.04*p(np.cos(a),np.sin(a)),color=TEAL,stroke_width=5) for a in np.arange(4)*PI/2])
    # Fixed fine granular texture suggests EM density, without pretending to be data.
    rng=np.random.default_rng(7)
    texture=VGroup(*[Dot(center+r*p(np.cos(a),np.sin(a)),radius=.017,color=TEXT,fill_opacity=.3) for r,a in zip(rng.uniform(1.62,2,75),rng.uniform(0,TAU,75))])
    return VGroup(lumen,cells,base,feet,seams,texture)
def layer_labels():
    return VGroup(leader('1  Endothelial cells',(3.6,1.85),(-.85,.6),TEAL),
        leader('2  Basement membrane',(3.6,.05),(-.39,.1),GREY,27),
        leader('3  Astrocyte endfeet',(3.6,-1.8),(-.2,-1.3),TAN))
def layer_question(): return VGroup(section(),layer_labels(),head('Which layer stopped the tracer?'))
def deposit_inside(x=-2.6): return Circle(radius=1.52,stroke_color=YELLOW,stroke_width=4,fill_color=DEPOSIT,fill_opacity=1).move_to(p(x,0))
def deposits_outside(x=-2.6):
    return VGroup(*[Dot(p(x+r*np.cos(a),r*np.sin(a)),radius=.105,color=YELLOW) for r in [2.4] for a in np.linspace(0,TAU,20,endpoint=False)],
        *[Dot(p(x+r,0),radius=.11,color=YELLOW) for r in [2.12]])

def vessel(x=0,y=0,leaky=False):
    g=VGroup(Rectangle(width=5.2,height=1.8,stroke_width=0,fill_color=TEAL,fill_opacity=.08).move_to(p(x,y)))
    for yy in [y-.9,y+.9]:
        for i in range(4):
            g.add(RoundedRectangle(width=1.02 if leaky else 1.29,height=.38,corner_radius=.09,color=TEAL,fill_opacity=.65).move_to(p(x-1.95+i*1.3,yy)))
    return g

def tracer(x=0,y=0): return VGroup(*[Dot(p(x+dx,y+dy),radius=.13,color=YELLOW) for dx,dy in [(-1.3,.3),(-.6,-.3),(0,.25),(.7,-.2),(1.3,.3)]])
def glass(v=0,x=-1.7):
    c=np.exp(-v);water=Rectangle(width=2.5,height=5.1,stroke_width=0,fill_color=interpolate_color(ManimColor('#D4EDFA'),ManimColor(DARK_BLUE),c),fill_opacity=1).move_to(p(x,-.35))
    rim=line([(x-1.4,2.25),(x-1.3,-3),(x+1.3,-3),(x+1.4,2.25)],TEXT,5)
    return VGroup(water,rim)
def pouring():
    # A rounded pitcher, open rim, handle and projecting pouring lip.
    body=VMobject().set_points_smoothly([p(*q) for q in [(-5.65,3.15),(-5.55,2.25),(-5.2,1.95),(-4.35,2.0),(-4.0,2.55)]])
    body.set_stroke(TEXT,4).set_fill(BLUE,.18)
    lip=line([(-5.65,3.15),(-4.55,3.15),(-4.15,2.8),(-3.65,2.75),(-4,2.55)],TEXT,4)
    handle=Arc(radius=.48,start_angle=PI/2,angle=PI,color=TEXT,stroke_width=5).stretch(1.15,1).move_to(p(-5.95,2.65))
    jug=VGroup(body,lip,handle)
    stream=VMobject().set_points_smoothly([p(*q) for q in [(-3.68,2.75),(-3.25,2.65),(-2.85,2.25),(-2.6,1.5)]])
    stream.set_stroke('#D4EDFA',22,opacity=.9)
    spoon=VGroup(Line(p(-1.3,2.8),p(-1.3,-1.7),color=GREY,stroke_width=7),Ellipse(width=.4,height=.65,color=GREY,fill_opacity=.8).move_to(p(-1.3,-1.7)))
    sheet=VMobject().set_points_smoothly([p(*q) for q in [(-.3,2.05),(.05,1.9),(.32,1.15),(.45,-.6),(.55,-2.85)]])
    sheet.set_stroke(BLUE,28,opacity=.75)
    spill=VGroup(Line(p(-3.4,-3.15),p(1.35,-3.15),color=GREY,stroke_width=3),sheet,
        Ellipse(width=2.3,height=.28,color=BLUE,fill_opacity=.7,stroke_width=2).move_to(p(.25,-3.05)))
    return jug,stream,spoon,spill

def swirls(): return VGroup(*[Arc(radius=.65,start_angle=i*.6,angle=PI*1.4,color=TEXT,stroke_opacity=.4,stroke_width=3).stretch(.55,1).move_to(p(-1.7,y)) for i,y in enumerate([1,.0,-1.1,-2.1])])
def dye_bar(v=0):
    c=np.exp(-v)
    return VGroup(Rectangle(width=.5,height=4.7,color=GREY).move_to(p(2,-.2)),Rectangle(width=.45,height=max(.02,4.65*c),stroke_width=0,fill_color=DARK_BLUE,fill_opacity=1).move_to(p(2,-2.525+4.65*c/2)),lab('100%',2,2.65,size=26),lab('0%',2,-2.95,size=26),lab(f'{100*c:.0f}% dye left',4.4,1.3,BLUE,28))

def pause(scene,q,targets,highlight=YELLOW):
    scene.camera.background_color=BG
    if len(q)>5: q[5].move_to(p(4.2,-2))
    scene.add(q,lab('Predict',4,-2.7,YELLOW,28))
    bar=Rectangle(width=2.8,height=.13,stroke_width=0,fill_color=YELLOW,fill_opacity=1).move_to(p(4,-3.2));scene.add(bar)
    for i in range(5):
        scene.play(Indicate(targets[i%len(targets)],color=highlight,scale_factor=1.06),bar.animate.stretch(.03 if i==4 else (4-i)/(5-i),0,about_edge=LEFT),run_time=1,rate_func=linear)

class S00Title(TitleCard):
    LESSON='The Map: How the Nervous System Is Organized'
    TITLE='Follow the Fluid, Find the Seal'
    def construct(self):
        self.add(lab('BIOCHEMISTRYPEDIA',0,2,TEAL,26),lab(self.LESSON,0,1,GREY,26))
        self.play(FadeIn(lab('Follow the Fluid,\nFind the Seal',0,-.5,size=48)),run_time=.8);self.finish()
class S01Question(SpokenScene):
    def construct(self):
        w,v,l=anatomy();self.add(w,v,l,anatomy_labels())
        self.at("tube's canal");self.play(Indicate(v,color=BLUE),run_time=.6)
        self.at('Where is it');self.play(FadeIn(lab('Made where?  Goes where?',0,-3.45,YELLOW,30)),run_time=.5);self.finish()
class S02Plexus(SpokenScene):
    def construct(self):
        self.add(*anatomy());fronds=VGroup()
        for x,y in VC:
            f=VGroup(Line(p(x-.4,y),p(x+.4,y),color=RED,stroke_width=4))
            for dx in np.linspace(-.35,.35,7):
                f.add(line([(x+dx-.08,y+.14),(x+dx,y),(x+dx+.08,y-.14)],RED,3))
            fronds.add(f)
        self.at('In each ventricle');self.play(Create(fronds),run_time=.6)
        self.at('the choroid plexus');self.play(FadeIn(leader('Choroid plexus',(3.8,2),(-1.95,1.7),RED)),run_time=.4)
        drops=VGroup(*[Dot(p(x+dx,y),radius=.085,color=BLUE,stroke_color=TEXT,stroke_width=1.5) for x,y in VC for dx in [-.25,0,.25]])
        self.at('secretes cerebrospinal');self.play(LaggedStart(*[FadeIn(d,shift=UP*.12) for d in drops],lag_ratio=.04),run_time=.6);self.play(drops.animate.shift(DOWN*.22),run_time=.5)
        self.at('the main source');self.play(FadeIn(lab('Main source',3.8,.6,BLUE)),run_time=.3)
        self.at('not the only');self.play(FadeIn(lab('Not the only source',3.8,-.3,GREY,26)),run_time=.3);self.finish()
class S03Route(SpokenScene):
    def construct(self):
        self.add(*anatomy(),anatomy_labels());f=flow()
        self.at('The net flow');self.play(FadeIn(lab('Net one-way flow',0,-3.45,BLUE)),run_time=.3)
        self.at('from the lateral');self.play(GrowArrow(f[0]),GrowArrow(f[1]),run_time=.6)
        self.at('then through the');self.play(GrowArrow(f[2]),run_time=.5)
        self.at('into the fourth');self.play(GrowArrow(f[3]),run_time=.4);self.finish()
class S04Exit(SpokenScene):
    def construct(self):
        w,v,l=anatomy();self.add(w,v,l,flow())
        self.at('The exit is');self.play(FadeIn(leader('Hindbrain',(4.4,.2),(2,-1),ORANGE)),run_time=.4)
        self.at('Openings in the');self.play(GrowArrow(arr((1.3,-1.4),(2.4,-2))),FadeIn(leader('Fourth ventricle\nopenings',(4.5,-2),(1.6,-1.5),BLUE,26)),run_time=.6)
        self.at('let fluid out');self.play(Create(outside()),run_time=.8);self.play(FadeIn(leader('Subarachnoid space',(-2,3.5),(-3,2.9),BLUE,26)),run_time=.4);self.finish()
class S05Canal(SpokenScene):
    def construct(self):
        brain=Ellipse(width=4.4,height=1.8,color=PURPLE,fill_opacity=.13).move_to(p(-2,2.25))
        stem=Polygon(p(-2.4,2),p(-1.6,2),p(-1.5,-3),p(-2.5,-3),color=TAN,fill_opacity=.3)
        outer=RoundedRectangle(width=1.7,height=5.7,corner_radius=.45,color=BLUE,fill_opacity=.12).move_to(p(-2,-.3))
        canal=DashedLine(p(-2,1.5),p(-2,-2.8),color=BLUE,dash_length=.15,stroke_width=5)
        self.add(brain,outer,stem,canal,leader('Brainstem',(-4.9,1),(-2.4,1),TAN,26))
        self.at('In most adult');self.play(FadeIn(lab('Adult human spinal cord',2.6,2.4,size=28)),run_time=.4)
        self.at('largely closed');self.play(FadeOut(canal),FadeIn(leader('Central canal:\nlargely closed',(2.5,.5),(-2,0),GREY)),run_time=.6)
        self.at('circulates around');self.play(FadeIn(leader('Fluid around the cord',(2.5,-1.8),(-1.2,-1.7),BLUE,27)),run_time=.5);self.finish()
class S06Turnover(SpokenScene):
    def construct(self):
        center=p(-2.5,0);clock=Circle(radius=1.65,color=GREY).move_to(center)
        hand=Line(center,center+UP*1.4,color=TEXT,stroke_width=5);self.add(clock,hand,lab('1 day',-2.5,-3.15,GREY,28))
        self.at('the fluid is')
        count=lab('0',2.8,.5,BLUE,54);self.add(count)
        for i,r in enumerate([1.9,2.15,2.4]):
            arc=Arc(radius=r,start_angle=PI/2,angle=-TAU,color=BLUE,stroke_width=5).shift(center)
            self.play(Create(arc),Rotate(hand,-TAU,about_point=center),Transform(count,lab(str(i+1),2.8,.5,BLUE,54)),run_time=.52,rate_func=linear)
        self.play(Create(Arc(radius=2.65,start_angle=PI/2,angle=-TAU*.3,color=BLUE,stroke_width=5).shift(center)),Rotate(hand,-TAU*.3,about_point=center),Transform(count,lab('3 and a bit',2.8,.5,BLUE,36)),run_time=.4)
        self.add(lab('About 3.3 turnovers / day',2.8,1.65,BLUE,28))
        self.at('Is it ever');self.play(FadeIn(lab('Completely fresh?',2.8,-1.6,YELLOW,30)),run_time=.4);self.finish()
class S07Glass1(SpokenScene):
    def construct(self):
        self.add(glass());j,s,sp,o=pouring()
        self.at('Picture a glass');self.play(FadeIn(lab('Dyed water',3.5,.7,BLUE,32)),run_time=.4)
        self.at('Pour in clean');self.play(FadeIn(j),Create(s),run_time=.6)
        self.at('stirring as it');self.play(FadeIn(sp),Create(o),Create(swirls()),run_time=.4);self.play(sp.animate.shift(RIGHT*.3),run_time=.3);self.play(sp.animate.shift(LEFT*.3),run_time=.3);self.finish()
class S08Glass2(SpokenScene):
    def construct(self):
        v=ValueTracker(0);g=glass();bar=dye_bar();self.add(g,*pouring(),swirls(),bar)
        g[0].add_updater(lambda m:m.set_fill(interpolate_color(ManimColor('#D4EDFA'),ManimColor(DARK_BLUE),np.exp(-v.get_value()))))
        bar.add_updater(lambda m:m.become(dye_bar(v.get_value())))
        num=lab('0.0 glassfuls',4.3,-.2,size=28);num.add_updater(lambda m:m.become(lab(f'{v.get_value():.1f} glassfuls',4.3,-.2,size=28)));self.add(num)
        self.at('After one full');self.play(v.animate.set_value(1),run_time=2.5,rate_func=linear)
        g[0].clear_updaters();bar.clear_updaters();num.clear_updaters();self.finish()
class S09Glass3(SpokenScene):
    def construct(self):
        bar=dye_bar(1);self.add(glass(1),lab('After 1 glassful',-1.7,2.8,GREY,28),bar)
        self.at('About');self.play(Indicate(bar,scale_factor=1.03),run_time=.5)
        self.at('Replacing a volume');ghost=glass(100,4.6)[1];ghost.set_stroke(opacity=.4)
        self.play(FadeOut(bar[4]),FadeIn(ghost),FadeIn(lab('Piston: empty',4.6,2.8,GREY,28)),run_time=.6);self.finish()
class S10Predict1(SpokenScene):
    def construct(self):
        q=plug_question();self.add(*q[:3]);plug=q[3];plug.shift(UP*1.4)
        self.at('Now plug');self.add(plug);self.play(plug.animate.shift(DOWN*1.4),run_time=.7)
        self.at('while secretion continues');self.play(FadeIn(q[5]),run_time=.4)
        self.at('Which');self.play(FadeIn(q[4]),run_time=.3);self.play(LaggedStart(*[Indicate(q[1][i],color=YELLOW) for i in [0,2,3]],lag_ratio=.1),run_time=.9);self.finish()
class S11Pause(Scene):
    def construct(self):
        q=plug_question();pause(self,q,[q[1][0],q[1][2],q[1][3]])
class S12Reveal1(SpokenScene):
    def construct(self):
        q=plug_question();self.add(*q[:4]);v=q[1]
        self.at('Everything upstream');self.play(v[0].animate.stretch(1.55,1).stretch(1.25,0).shift(UP*.17),v[1].animate.stretch(1.55,1).stretch(1.25,0).shift(DOWN*.17),v[2].animate.stretch(1.7,0),FadeIn(lab('Upstream swells',3.8,2,BLUE,30)),run_time=.8)
        self.at('Not the fourth');self.play(FadeIn(leader('Fourth: unchanged',(4,-2.3),(1.6,-1.45),GREY,27)),Indicate(v[3],color=BLUE),run_time=.6);self.finish()
class S13Hook(SpokenScene):
    def construct(self):
        v=vessel(0,0,True).scale(1.7)
        tissue=RoundedRectangle(width=11.1,height=5.5,corner_radius=.35,stroke_width=0,fill_color=TAN,fill_opacity=.20).move_to(p(0,0))
        self.add(tissue,v)
        self.at('Now the seal');self.play(FadeIn(head('Now the seal')),run_time=.3)
        self.at('In muscle');self.play(FadeIn(lab('Muscle tissue',0,-3,size=30)),run_time=.3)
        t=tracer().scale(1.7)
        # Enter through the open vessel end; keep the leader clear of wall cells.
        tr_label=VGroup(line([(5.0,2.3),(5.15,.51),(2.21,.51)],YELLOW,2),lab('Protein tracer',4.6,2.65,YELLOW))
        self.at('a protein tracer');self.play(FadeIn(t),FadeIn(tr_label),run_time=.5)
        self.at('leaks out');self.play(FadeOut(tr_label[0]),*[MoveAlongPath(d,line([(d.get_x(),d.get_y()),([-2.21,0,2.21,-2.21,2.21][i],.6 if i%2==0 else -.6),([-2.21,0,2.21,-2.21,2.21][i],2.15 if i%2==0 else -2.15)],YELLOW)) for i,d in enumerate(t)],run_time=1)
        stains=VGroup(*[Ellipse(width=1.0+k*.5,height=.35+k*.23,stroke_width=0,fill_color=DEPOSIT,fill_opacity=.12 if k else .8).move_to(d) for d in t for k in range(4, -1, -1)])
        self.play(FadeIn(stains,scale=.5),FadeIn(line([(5,2.3),(4.8,2.15),(2.21,2.15)],YELLOW,2)),run_time=.65);self.bring_to_front(t);self.finish()
class S14Hook2(SpokenScene):
    def construct(self):
        a=vessel(-3.4,0,True);t=tracer(-3.4,0)
        for i,d in enumerate(t):d.move_to(p(-5.4+i,1.7 if i%2==0 else -1.7))
        self.add(a,t,lab('Muscle',-3.4,2.7,size=30),leader('Protein tracer',(-3.4,-2.7),(-2.4,-1.7),YELLOW))
        b=vessel(3.4);tr=tracer(3.4)
        self.at("In the brain's cortex");self.play(FadeIn(b),FadeIn(tr),FadeIn(lab('Brain cortex',3.4,2.7,size=30)),run_time=.6)
        self.at('goes no farther');self.play(tr.animate.shift(RIGHT*.15),FadeIn(leader('Joined lining cells',(3.4,-2.7),(4,-.9),TEAL,26)),run_time=.5);self.finish()
class S15Layers(SpokenScene):
    def construct(self):
        s=section();ls=layer_labels();self.add(s)
        self.at('Three layers');self.play(FadeIn(head('Three possible layers')),run_time=.3)
        self.at('the endothelial cells');self.play(Indicate(s[1],color=TEXT,scale_factor=1.04),FadeIn(ls[0]),run_time=.6)
        self.at('the basement membrane');self.play(Indicate(s[2],color=TEXT,scale_factor=1.04),FadeIn(ls[1]),run_time=.6)
        self.at('and astrocyte');self.play(Indicate(s[3],color=TEXT,scale_factor=1.04),FadeIn(ls[2]),run_time=.6);self.finish()
class S16Method(SpokenScene):
    def construct(self):
        mouse=VGroup(Ellipse(width=5.8,height=3,color=GREY,fill_opacity=.2).move_to(p(-1,-.3)),Ellipse(width=1.8,height=1.6,color=GREY,fill_opacity=.3).move_to(p(-3.8,.25)),Circle(radius=.55,color=GREY,fill_opacity=.3).move_to(p(-3.7,1.2)),Dot(p(-4.2,.5),radius=.08,color=TEXT),line([(1.8,-.4),(3,-.5),(3.6,-1),(4.8,-1.2)],GREY,5))
        vein=line([(-2.6,.2),(-1.5,.7),(-.2,.5),(1,.1)],BLUE,7)
        mouse.stretch(1.3,1);self.add(mouse,vein,leader('Vein',(2.7,1.7),(-.2,.5),BLUE,28))
        self.at('In');self.play(FadeIn(head('Reese and Karnovsky · 1967')),run_time=.4)
        syringe=VGroup(Rectangle(width=1.3,height=.45,color=GREY,fill_opacity=.2),Line(p(.65,0),p(1.5,0),color=YELLOW,stroke_width=4)).rotate(-PI/4).move_to(p(-1.6,2))
        self.at('injected');self.play(FadeIn(syringe),GrowArrow(arr((-1.1,1.5),(-.2,.5),YELLOW)),FadeIn(lab('Horseradish peroxidase',0,-2.5,YELLOW,30)),run_time=.7)
        self.at('Wherever this enzyme');self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.3)
        sample=RoundedRectangle(width=7.5,height=4.7,corner_radius=.2,color=GREY,fill_color='#B9B2A2',fill_opacity=.85).move_to(p(-1,-.2));dots=VGroup(*[Dot(p(x,y),radius=.22,color=YELLOW) for x,y in [(-3,1),(-1.7,-.4),(-.5,1.2),(.6,-1),(-2.8,-1.4)]])
        self.play(FadeIn(sample),FadeIn(dots),FadeIn(lab('Enzyme in tissue',0,3,YELLOW,30)),run_time=.4)
        reagent=chip('Reagent',TEXT,30).move_to(p(4,0))
        self.at('a chemical reaction');self.play(FadeIn(reagent),run_time=.25);self.play(reagent.animate.move_to(p(-1,0)),run_time=.65)
        self.at('a dense deposit');self.play(FadeOut(reagent),*[d.animate.set_color(DEPOSIT).scale(1.6).set_stroke(YELLOW,2) for d in dots],run_time=.45);self.play(FadeIn(leader('Dense deposit',(4.3,-1.7),(.6,-1),TEXT,28)),run_time=.2)
        self.at('an electron microscope');self.wait(.75);self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.2);self.add(section(),lab('Electron microscopy',3.7,1, size=30));self.finish()
class S17Predict2(SpokenScene):
    def construct(self):
        q=layer_question();self.add(q)
        self.at('Which layer');self.play(LaggedStart(*[Indicate(q[0][i],color=TEXT,scale_factor=1.07) for i in [1,2,3]],lag_ratio=.15),run_time=1.5);self.finish()
class S18Pause(Scene):
    def construct(self):
        q=layer_question();pause(self,q,[q[0][i] for i in [1,2,3]],highlight=TEXT)
class S19Reveal2(SpokenScene):
    def construct(self):
        s=section();self.add(s,layer_labels())
        self.at('The endothelial cells');self.play(Indicate(s[1],color=TEXT),run_time=.5)
        d=deposit_inside();self.at('The deposit filled');self.play(GrowFromCenter(d),run_time=1.2)
        self.at('went no farther');self.play(Indicate(s[1],color=TEXT,scale_factor=1.03),FadeIn(head('Deposit stops at the endothelium')),run_time=.5)
        self.at('That holds for');self.play(FadeIn(lab('For this tracer · outer layers clean',2.8,-3.1,GREY,26)),run_time=.4);self.finish()
class S20Junctions(SpokenScene):
    def construct(self):
        inset=VGroup(section(0),deposit_inside(0)).scale(.32).move_to(p(-4.8,1.5))
        cells=VGroup(*[RoundedRectangle(width=2.7,height=5.2,corner_radius=.15,color=TEAL,fill_opacity=.5).move_to(p(x,-.15)) for x in [.2,3.15]])
        seam=VGroup(*[Line(p(1.55,y),p(1.8,y),color=YELLOW,stroke_width=9) for y in [-1.3,-.65,0,.65,1.3]])
        self.add(inset,cells,line([(-3.9,1.5),(-1.5,2.4)],GREY,2),lab('Vessel seam',-4.7,-.2,GREY,26),lab('Endothelial cells',1.7,-3.15,TEAL,28))
        self.at('Tight junctions');self.play(Create(seam),FadeIn(head('Probable block: tight junctions')),run_time=.5)
        t=Dot(p(1.68,2.3),radius=.18,color=YELLOW);self.add(t);self.play(t.animate.move_to(p(1.68,1.55)),run_time=.7)
        self.at('the probable block');self.play(Indicate(seam,color=YELLOW),run_time=.4);self.finish()
class S21Reverse(SpokenScene):
    def construct(self):
        w,v,l=anatomy();self.add(w,v,l)
        self.at('Then');self.play(FadeIn(head('Brightman and Reese')),run_time=.4)
        t=Dot(p(-2.4,2.7),radius=.17,color=YELLOW)
        self.at('put the tracer');self.add(t);self.play(t.animate.move_to(p(*VC[0])),run_time=.6)
        self.at('into the ventricles');self.play(FadeIn(leader('Tracer in ventricular fluid',(3.5,1.4),(-1.5,1.7),YELLOW,26)),run_time=.4);self.finish()
class S22Reverse2(SpokenScene):
    def construct(self):
        s=section();cells=VGroup(*[Ellipse(width=1.1,height=.8,color=GREY,fill_opacity=.2).move_to(p(x,y)) for x,y in [(1.5,1.9),(3.6,1.7),(2.2,.1),(4,-.7),(1.4,-1.9)]])
        source=RoundedRectangle(width=.6,height=1.7,corner_radius=.27,color=BLUE,fill_opacity=.3).move_to(p(5.8,.7))
        self.add(s,cells,source,lab('Neurons and glia',3,2.7,GREY,28),leader('Tracer from ventricle',(3.6,-2.9),(5.8,-.05),YELLOW,25))
        ts=VGroup(*[Dot(p(5.8,.7),radius=.095,color=YELLOW) for _ in range(14)])
        self.add(ts)
        paths=[]
        for i in range(14):
            dy=(i%3-1)*.12
            paths.append(VMobject().set_points_smoothly([p(*q) for q in [(5.8,.7+dy),(4.7,.8+dy),(3.5,.87+dy),(2.2,.95+dy),(1,.7+dy),(.25,.35+dy),(-.48,.02+dy)]]))
        self.at('It spread between')
        self.play(LaggedStart(*[MoveAlongPath(d,path,rate_func=linear) for d,path in zip(ts,paths)],lag_ratio=.09),run_time=3.6)
        self.at('reached the capillaries');self.play(FadeOut(ts),FadeIn(deposits_outside()),run_time=.45)
        # Flash only the outer mouth, leaving the inner seam and lumen empty.
        tick=Line(p(-.58,-.18),p(-.58,.18),color=TEXT,stroke_width=8)
        self.at('stopped at the same');self.play(ShowPassingFlash(tick,time_width=.8),FadeIn(head('From outside · same junctions')),run_time=.65);self.finish()
class S23Same(SpokenScene):
    def construct(self):
        a=VGroup(section(0),deposit_inside(0)).scale(.95).move_to(p(-3.6,0));b=VGroup(section(0),deposits_outside(0)).scale(.95).move_to(p(3.6,0))
        self.add(a,b,lab('From blood',-3.6,3.2,YELLOW,30),lab('From tissue',3.6,3.2,YELLOW,30))
        self.at('Two experiments');self.play(GrowArrow(arr((-3.6,0),(-2.35,0),YELLOW)),GrowArrow(arr((6,0),(5.45,0),YELLOW)),run_time=.6)
        self.at('pointed to the same');self.play(FadeIn(VGroup(leader('Endothelium',(0,-3.2),(-2.35,-1.1),TEAL,32),line([(1,-3.05),(2.35,-1.1)],TEAL,2))),run_time=.5);self.finish()
class S24Second(SpokenScene):
    def construct(self):
        stroma=Polygon(p(-5.8,-3),p(5.8,-3),p(5.8,.55),p(5.15,1.0),p(-5.15,1.0),p(-5.8,.55),color=TAN,fill_opacity=.18)
        ep=VGroup(*[RoundedRectangle(width=1.4,height=1.1,corner_radius=.16,color=TEAL,fill_opacity=.5).move_to(p(-4.35+i*1.45,1.55)) for i in range(7)])
        cap=vessel(0,-1.45,True);tr=VGroup(*[Dot(p(-1.95+(i%4)*1.3,-1.45+(i//4-.5)*.3),radius=.13,color=YELLOW) for i in range(12)])
        self.add(stroma,cap,tr,ep,lab('CSF',-5.7,2.6,BLUE,32),lab('Blood',-3.8,-1.45,YELLOW,28))
        self.at('A second seal');self.play(FadeIn(head('A second seal')),run_time=.3)
        label=leader('Tube lining',(2.9,2.8),(2.9,2.12),TEAL,26)
        self.at('specialized part');self.play(FadeIn(label),run_time=.3)
        self.at('In the');self.play(FadeIn(lab('Choroid plexus',0,-3.4,RED,28)),run_time=.3)
        self.at('leaky capillaries');self.play(FadeIn(lab('Leaky capillary',3.9,-1.45,TEAL,26)),run_time=.35)
        self.play(LaggedStart(*[MoveAlongPath(d,line([(d.get_x(),d.get_y()),(-1.3+(i%3)*1.3,-1.0),(-1.3+(i%3)*1.3,-.35),(-2.9+(i%6)*1.16,.83-(i//6)*.22)],YELLOW),rate_func=linear) for i,d in enumerate(tr)],lag_ratio=.025),run_time=.95)
        seams=VGroup(*[Line(p(-3.625+i*1.45,1.05),p(-3.625+i*1.45,2.05),color=TEAL,stroke_width=6) for i in range(6)])
        self.at('a sealed epithelium');self.play(Create(seams),Transform(label,leader('Blood–CSF barrier',(2.9,2.8),(2.175,2.1),TEAL,26)),run_time=.6);self.finish()
class S25Close(SpokenScene):
    def construct(self):
        self.add(*anatomy(),outside())
        arrows=flow()
        for arrow in arrows: arrow.set_stroke(width=9);arrow.tip.scale(1.65,about_point=arrow.get_end())
        self.at('the net flow');self.play(FadeIn(arrows),FadeIn(lab('Net flow: one way',3.9,2.6,BLUE,28)),run_time=.5)
        vessel_mark=VGroup(RoundedRectangle(width=1.15,height=.43,corner_radius=.18,color=TEAL,fill_opacity=.25).move_to(p(-3.4,-.45)),Line(p(-3.4,-.66),p(-3.4,-.24),color=TEAL,stroke_width=5))
        plex=VGroup(*[Line(p(-2.7+dx,1.5),p(-2.6+dx,1.85),color=RED,stroke_width=5) for dx in [0,.2,.4]])
        self.at('Two main seals');self.play(FadeIn(vessel_mark),FadeIn(plex),FadeIn(leader('Blood–brain:\ncapillary wall',(-4.4,-2.45),(-3.4,-.72),TEAL,27)),FadeIn(leader('Blood–CSF:\nplexus lining',(-3.6,3.45),(-2.5,1.95),TEAL,27)),run_time=.6)
        self.at('both selective');self.play(Indicate(vessel_mark,color=TEXT),Indicate(plex,color=TEXT),run_time=.5)
        self.at('from the blood');self.play(FadeIn(lab('Seals: capillary wall, plexus lining',0,-3.55,size=28)),run_time=.4);self.finish()
class S26End(EndCard):
    LINE='Net flow: one way. Seals: capillary wall, plexus lining.'
    def construct(self):
        self.add(lab('Net flow: one way.',0,1,BLUE,42),lab('Seals: capillary wall, plexus lining.',0,-.3,size=36),lab('biochemistrypedia.com',0,-1.7,TEAL,26));self.finish()
