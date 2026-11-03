"""Chapter 1: The Map and the Puzzle.
COLOR MAP: YELLOW netrin/UNC-6; BLUE axon/growth cone; TEAL DCC;
PURPLE UNC5; ORANGE cAMP and extracellular matrix; GREEN attraction;
RED repulsion; GREY anatomy. Migrating worm cells use TEAL.
All paths are anatomical schematics, not quantitative model traces.
The current lesson (map glossary and 1995 Colamarino paragraph) supports trochlear axons.
"""
import numpy as np
from bp_style import *

PURPLE='#B58CD9'
ORANGE='#F29E4C'

class Timed(SpokenScene):
    # Exact anchors, no anticipatory lead. Avoid writing the pipeline's diagnostic log.
    def at(self, phrase, lead=0, nth=0):
        rest=self.t_of(phrase,nth)-self.elapsed()
        if rest>.001:self.wait(rest)
    def finish(self):
        # Match each audio segment exactly; no accumulating 0.4-second scene padding.
        rest=self.narration_s-self.elapsed()
        if rest>.001:self.wait(rest)

def label(s,x,y,color=TEXT,size=28):
    return T(s,size=size,color=color).move_to([x,y,0])

def heading(s):return label(s,0,3.25,size=32)

def smooth(points,color=BLUE,width=6):
    return VMobject().set_points_smoothly([np.array(p,float) for p in points]).set_stroke(color,width)

def callout(s,pos,target,color=TEXT,size=28):
    t=label(s,*pos,color,size)
    edge=t.get_left() if target[0]<pos[0] else t.get_right()
    return VGroup(Line(edge+(.12*LEFT if target[0]<pos[0] else .12*RIGHT),target,color=color,stroke_width=2),t)

def cord(center=(0,0,0),scale=1.36,level=0,crossed=False,axes=True):
    c=np.array(center,float)
    def p(x,y):return c+scale*np.array([x,y,0])
    outline=Ellipse(width=4.5*scale,height=4.5*scale,color=GREY,stroke_width=3).move_to(c)
    canal=Ellipse(width=.45*scale,height=1.15*scale,color=GREY,fill_color=BG,fill_opacity=1).move_to(p(0,.4))
    fp=VGroup(*[Polygon(p(x-.17,-2.12),p(x+.17,-2.12),p(x+.12,-1.78),p(x-.12,-1.78),color=ORANGE,fill_color=ORANGE,fill_opacity=.8,stroke_width=2) for x in [-.32,0,.32]])
    vz=VGroup(Ellipse(width=1.2*scale,height=1.95*scale,stroke_width=0,fill_color=TEAL,fill_opacity=.12).move_to(p(0,.4)))
    for a in np.linspace(0,TAU,16,endpoint=False):
        cell=Ellipse(width=.18*scale,height=.36*scale,color=TEAL,fill_color=TEAL,fill_opacity=.35,stroke_width=2)
        cell.rotate(-a).move_to(p(.45*np.sin(a),.4+.8*np.cos(a)));vz.add(cell)
    fibres=VGroup(*[Line(p(.5*np.sin(a),.4+.82*np.cos(a)),p(2.15*np.sin(a),2.15*np.cos(a)),color=GREY,stroke_width=2) for a in np.linspace(0,TAU,10,endpoint=False)])
    rim=outline.copy().scale(1.025).set_stroke(ORANGE,5)
    soma=Dot(p(-.95,1.45),radius=.15*scale,color=BLUE)
    route=smooth([p(x,y) for x,y in [(-.95,1.45),(-1.6,.85),(-1.92,.0),(-1.55,-1.05),(-.85,-1.55)]])
    crossing=smooth([p(x,y) for x,y in [(-.85,-1.55),(-.4,-1.9),(0,-1.96),(.65,-1.8),(1.6,-.85)]])
    ticks=VGroup(label('dorsal',c[0],c[1]+2.48*scale,size=26),label('ventral',c[0],c[1]-2.48*scale,size=26)) if axes else VGroup()
    g=VGroup(outline,canal)
    if level>=1:g.add(fp)
    if level>=2:g.add(vz)
    if level>=3:g.add(fibres.set_opacity(.25 if level>=5 else .7))
    if level>=4:g.add(rim)
    if level>=5:g.add(soma,route)
    if crossed:g.add(crossing)
    if axes:g.add(ticks)
    return g,dict(outline=outline,canal=canal,fp=fp,vz=vz,fibres=fibres,rim=rim,soma=soma,route=route,crossing=crossing,p=p)

def growth(center=(0,0,0),scale=1):
    c=np.array(center,float)
    fan=Polygon(*[c+scale*np.array(p) for p in [(-.8,0,0),(.2,.8,0),(.65,.55,0),(.85,0,0),(.65,-.55,0),(.2,-.8,0)]],color=BLUE,fill_color=BLUE,fill_opacity=.2,stroke_width=4)
    fil=VGroup(*[Line(c+scale*np.array([.55,y,0]),c+scale*np.array([1.25,y*1.65,0]),color=BLUE,stroke_width=3) for y in [-.6,-.3,0,.3,.6]])
    return VGroup(fan,fil)

def cups(center,angles,color,scale=1):
    c=np.array(center,float);g=VGroup()
    for deg in angles:
        phi=np.radians(deg);q=c+scale*np.array([np.cos(phi),np.sin(phi),0])
        g.add(Arc(radius=.25*scale,start_angle=phi+PI/2,angle=PI,arc_center=q,stroke_color=color,stroke_width=6))
    return g

def boxes(filled=0):
    names=['What crosses?','Two answers?','Gradient or path?']
    g=VGroup()
    for i,x in enumerate([-4.25,0,4.25]):
        g.add(VGroup(RoundedRectangle(width=4.05,height=.85,corner_radius=.12,color=YELLOW if i<filled else GREY,fill_color=YELLOW,fill_opacity=.07 if i<filled else 0).move_to([x,-3.12,0]),label(f'{i+1}  '+(names[i] if i<filled else '?'),x,-3.12,YELLOW if i<filled else TEXT,26)))
    return g

def dual(y=.15,scale=1.17):
    left,dl=cord((-3.45,y,0),scale,5,True,axes=False)
    right,dr=cord((3.45,y,0),scale,4,axes=False)
    p=dr['p'];path=smooth([p(x,z) for x,z in [(.5,-1.55),(1.5,-1.05),(1.9,.1),(1.25,1.65)]],RED)
    soma=Dot(p(.5,-1.55),radius=.16,color=RED)
    labs=VGroup(label('spinal cord',-3.45,3.25,size=28),label('midbrain–hindbrain',3.45,3.25,size=28),callout('floor plate',(-3.4,-2.87),dl['p'](0,-1.96),ORANGE,26),callout('floor plate',(3.45,-2.87),dr['p'](0,-1.96),ORANGE,26))
    return VGroup(left,right),path,soma,labs,dl,dr

def worm():
    cuticle=VGroup(Ellipse(width=8.7,height=6.25,color=GREY,stroke_width=5),Ellipse(width=8.35,height=5.9,color=GREY,stroke_width=2))
    gut=Dot([0,.15,0],radius=.34,color=GREY,fill_opacity=.6)
    nerve=Ellipse(width=1.0,height=.42,color=GREY,fill_color=GREY,fill_opacity=.8,stroke_width=2).move_to([0,-2.35,0])
    return VGroup(cuticle,gut,nerve,label('C. elegans · cross-section',0,3.45,size=28),label('dorsal',0,2.6,size=26),label('ventral',0,-2.85,size=26))

def pause_track():
    return Line([-5.9,-1.85,0],[5.9,-1.85,0],color=GREY,stroke_width=12)

def choices():
    return VGroup(*[VGroup(RoundedRectangle(width=5.3,height=3.3,color=GREY).move_to([x,.25,0]),label(s,x,.25,size=28)) for x,s in [(-3.25,'direction in the cue'),(3.25,'direction in the reader')]],label('?',0,.25,size=40),label('Pause and guess',0,2.75,size=30))

def rule():
    return VGroup(label('Netrin marks a place.',0,1.2,YELLOW,40),label('The growth cone decides',0,-.1,BLUE,38),label('what to do there.',0,-1.15,BLUE,38))

def rulecard(n, where='source · slope · surface', sign='receptors'):
    rows=[('WHERE',where,YELLOW),('SIGN',sign,BLUE),('STATE','internal state\n(in some cells)',ORANGE)]
    g=VGroup(RoundedRectangle(width=12.4,height=1.85,corner_radius=.15,color=GREY,fill_color=BG,fill_opacity=1).move_to([0,-2.65,0]))
    for i,(a,b,col) in enumerate(rows[:n]):
        x=-4.1+i*4.1
        g.add(label(a,x,-2.15,col,28),label(b,x,-2.85,TEXT,26 if i<2 else 26))
    return g

class S00Title(TitleCard):
    LESSON='Netrin and DCC: One Cue, Two Answers'
    TITLE='The Map and the Puzzle'

class S01Question(Timed):
    def construct(self):
        mid=Line([2.6,-2.25,0],[2.6,2.7,0],color=YELLOW,stroke_width=9)
        self.add(mid,label('netrin · midline',3.9,-2.7,YELLOW,28),Dot([-1.5,0,0],radius=.16,color=BLUE))
        toward=smooth([[-1.5,0,0],[-.5,1,0],[1,1.6,0],[2.35,1.5,0]],BLUE,9)
        away=smooth([[-1.5,0,0],[-2.4,-.5,0],[-3.8,-1.3,0],[-5.4,-1,0]],BLUE,9)
        self.at('pulls some');self.play(Create(toward),run_time=1.3)
        self.add(Arrow([.1,2.3,0],[2.1,2.3,0],color=GREEN,buff=0),label('pull',1.1,2.8,GREEN,28))
        self.at('it pushes');self.play(Create(away),run_time=.8)
        self.add(Arrow([-3,-2.1,0],[-5,-2.1,0],color=RED,buff=0),label('push',-4,-2.6,RED,28))
        self.at('what decides');self.play(FadeIn(label('What decides?',0,3.4,size=38)),run_time=.3);self.finish()

class S02Growthcone(Timed):
    def construct(self):
        ax=Line([-5.8,0,0],[-1.6,0,0],color=BLUE,stroke_width=12);g=growth(scale=2.25)
        self.add(ax,g)
        self.at('its growth');self.play(FadeIn(callout('growth cone',(3.9,2.9),[1.2,1.3,0],BLUE,32)),run_time=.3)
        self.at('the moving');self.play(g.animate.shift(RIGHT*.45),ax.animate.put_start_and_end_on([-5.8,0,0],[-1.15,0,0]),run_time=.7);self.finish()

class S03Slice(Timed):
    def construct(self):
        back=Ellipse(width=2.6,height=5.8,color=GREY).move_to([-2,0,0]);front=back.copy().shift(RIGHT*4)
        tube=VGroup(back,front,Line([-2,2.9,0],[2,2.9,0],color=GREY),Line([-2,-2.9,0],[2,-2.9,0],color=GREY));self.add(tube)
        plane=Polygon([-.65,-3,0],[.65,-2.5,0],[.65,3,0],[-.65,2.5,0],color=TEXT,fill_opacity=.2)
        self.at('cut crosswise');self.play(FadeIn(plane),run_time=.35)
        self.at('like a slice');self.play(FadeOut(tube),plane.animate.stretch(.18,0),run_time=.3)
        section,d=cord(axes=False)
        self.play(ReplacementTransform(plane,section),FadeIn(callout('transverse section',(4.5,1.8),[2.8,1.4,0])),FadeIn(callout('central canal',(4.4,.2),[.32,.5,0],size=26)),run_time=.55);self.finish()

class S04Floorplate(Timed):
    def construct(self):
        g,d=cord();self.add(g)
        self.at('floor plate');self.play(FadeIn(d['fp']),FadeIn(callout('floor plate',(4.5,-1.8),d['p'](0,-1.96),ORANGE)),run_time=.4)
        self.play(Indicate(d['fp'],color=ORANGE,scale_factor=1.18),run_time=.6)
        self.at('ventral midline');self.play(FadeIn(callout('ventral midline',(-4.6,-2.4),d['p'](0,-2.12),size=26)),run_time=.3);self.finish()

class S05Vz(Timed):
    def construct(self):
        g,d=cord(level=1);self.add(g)
        self.at('ventricular zone');self.play(FadeIn(d['vz']),FadeIn(callout('ventricular zone',(-4.65,1.4),d['p'](-.5,.8),TEAL,26)),run_time=.4)
        self.at('central canal');self.play(FadeIn(callout('central canal',(4.7,1.0),d['p'](.22,.4),size=26)),run_time=.3)
        self.at('progenitors');self.play(FadeIn(callout('progenitors',(4.6,-.3),d['p'](.5,-.1),TEAL,28)),run_time=.3)
        neuron=VGroup(Dot([3.85,-1.5,0],color=BLUE,radius=.18),Line([3.85,-1.5,0],[4.3,-1.5,0],color=BLUE,stroke_width=4))
        glia=Ellipse(width=.42,height=.56,color=GREY,fill_color=GREY,fill_opacity=.65).move_to([3.85,-2.35,0])
        # Explicit daughter objects persist after the division animation.
        split=VGroup(Line(d['p'](.5,-.1),[3.25,-1.9,0],color=TEAL,stroke_width=2),Line([3.25,-1.9,0],[3.6,-1.5,0],color=BLUE,stroke_width=2))
        self.at('make neurons');self.play(Create(split),FadeIn(neuron),FadeIn(label('neuron',5.15,-1.5,BLUE,26)),run_time=.3)
        self.at('and glia');self.play(Create(Line([3.25,-1.9,0],[3.6,-2.35,0],color=GREY,stroke_width=2)),FadeIn(glia),FadeIn(label('glia',5,-2.35,size=26)),run_time=.3);self.finish()

class S06Fibres(Timed):
    def construct(self):
        g,d=cord(level=2);self.add(g,callout('progenitors',(4.6,1.2),d['p'](.5,.9),TEAL))
        self.at('sends a long');self.play(Create(d['fibres']),run_time=1.2)
        self.at('to the edge');self.play(FadeIn(callout('radial fibre',(4.7,-.9),d['p'](1.8,-.6),size=26)),run_time=.3);self.finish()

class S07Pia(Timed):
    def construct(self):
        g,d=cord(level=3);self.add(g)
        self.at('outer edge');self.play(Create(d['rim']),run_time=.5)
        self.at('is the');self.play(FadeIn(callout('pial surface',(4.7,1.7),d['p'](1.85,1.3),ORANGE)),run_time=.3)
        self.at('basement membrane');self.play(FadeIn(callout('basement\nmembrane',(-4.8,-1.5),d['p'](-2.1,-.85),ORANGE,26)),run_time=.3)
        self.at('thin sheet');self.play(FadeIn(callout('extracellular\nmatrix sheet',(-4.8,-2.5),d['p'](-1.9,-1.3),ORANGE,26)),run_time=.3);self.finish()

class S08Commissural(Timed):
    def construct(self):
        g,d=cord(level=4);d['fibres'].set_opacity(.2);self.add(g)
        self.at('dorsal cord');self.play(FadeIn(d['soma']),FadeIn(callout('commissural neuron',(-4.6,2.0),d['p'](-.95,1.45),BLUE,26)),run_time=.4)
        self.at('their axons');self.play(Create(d['route']),run_time=1.2)
        self.at('close to');self.play(FadeIn(callout('near the pia',(-4.7,-1.4),d['p'](-1.7,-.8),BLUE,26)),run_time=.3);self.finish()

class S09Cross(Timed):
    def construct(self):
        g,d=cord(level=5);self.add(g,callout('floor plate',(4.6,-2.1),d['p'](0,-1.96),ORANGE))
        self.at('they turn inward');self.play(Create(d['crossing']),run_time=1.5)
        self.at('other side');self.play(FadeIn(callout('cross the midline',(4.7,-.7),d['p'](.8,-1.6),BLUE,26)),run_time=.3);self.finish()

class S10Trochlear(Timed):
    def construct(self):
        old,_=cord(level=5,crossed=True);self.add(old)
        maps,path,soma,labs,dl,dr=dual()
        self.at('on its own');self.play(ReplacementTransform(old,maps[0]),run_time=.5)
        self.at('neural tube');self.play(FadeIn(maps[1]),FadeIn(labs),run_time=.5)
        self.at('trochlear motor');self.play(FadeIn(soma),FadeIn(label('trochlear motor axon',3.5,-3.4,RED,26)),FadeIn(label('commissural axon',-3.5,-3.4,BLUE,26)),run_time=.3)
        self.at('grow dorsally');self.play(Create(path),run_time=1.0)
        self.add(label('dorsal ↑',3.6,2.6,size=26));self.finish()

class S11Worm(Timed):
    def construct(self):
        self.add(worm())
        cell=Dot([-1.8,1.1,0],radius=.25,color=TEAL)
        ax=smooth([[1.8,-1.2,0],[2,-.3,0],[1.5,1.25,0]],BLUE,7)
        cell_label=callout('migrating cell',(-4.6,1.5),[-1.8,1.1,0],TEAL,26)
        self.at('cells and');self.play(FadeIn(cell),FadeIn(cell_label),run_time=.3)
        self.at('pioneer axons');self.play(FadeIn(VGroup(label('pioneer axon',4.6,1.85,BLUE,26),Line([3.25,1.6,0],[1.7,.65,0],color=BLUE,stroke_width=2))),run_time=.3)
        self.at('migrate between');self.play(cell.animate.shift(DOWN*2.3),Transform(cell_label,callout('migrating cell',(-4.8,-1.4),[-1.8,-1.2,0],TEAL,26)),Create(ax),GrowArrow(Arrow([-2.5,.8,0],[-2.5,-1.3,0],color=TEAL,buff=0)),GrowArrow(Arrow([2.6,-1.1,0],[2.6,1.2,0],color=BLUE,buff=0)),run_time=1.1);self.finish()

class S12Unc6(Timed):
    def construct(self):
        self.add(worm(),Dot([-1.8,-1.2,0],radius=.25,color=TEAL),smooth([[1.8,-1.2,0],[2,-.3,0],[1.5,1.25,0]],BLUE,7))
        band=Arc(radius=3.1,start_angle=225*DEGREES,angle=90*DEGREES,color=YELLOW,stroke_width=13).stretch(1.4,0)
        self.at("the worm's netrin");self.play(Create(band),run_time=.4)
        self.at('called');self.play(FadeIn(callout('UNC-6',(-4.9,-2.2),[-2.1,-2.6,0],YELLOW,28)),run_time=.3)
        self.at('is made');self.play(FadeIn(callout('made ventrally',(1.2,-3.55),[1.25,-2.96,0],YELLOW,26)),run_time=.3);self.finish()

class S13P1(Timed):
    def construct(self):
        slots=boxes();initial,_=cord((0,.3,0),1.1,5,True,axes=False)
        self.add(slots,heading('Three puzzles'),initial)
        dish=RoundedRectangle(width=11.8,height=4.8,corner_radius=.3,color=GREY,fill_color=GREY,fill_opacity=.06).move_to([0,.2,0])
        a=RoundedRectangle(width=1.4,height=2.4,corner_radius=.2,color=GREY,fill_opacity=.3).move_to([-4,.1,0]);b=a.copy().move_to([4,.1,0])
        self.at('a floor plate');self.play(FadeOut(initial),FadeIn(dish),FadeIn(a),FadeIn(b),FadeIn(label('collagen gel',0,2.2,size=28)),FadeIn(label('floor plate',4,-1.6,ORANGE,28)),run_time=.4)
        dots=VGroup(*[Dot([x,y,0],radius=.035,color=YELLOW).set_opacity(.08+.08*(x+2)) for x in np.linspace(-1.6,3.1,15) for y in [-.8,-.3,.3,.8]])
        paths=VGroup(*[smooth([[-3.3,y,0],[-2,y*.9+.2,0],[-.3,y*.4+.1,0],[1.7,y*.25,0]]) for y in [-.65,0,.65]])
        self.at('draws axons');self.play(Create(paths),FadeIn(dots),FadeIn(label('dorsal cord',-4,-1.6,BLUE,28)),run_time=.8)
        self.at('without touching');self.play(FadeIn(label('no contact',2.35,-1.08,size=26)),run_time=.3)
        self.at('what crosses');self.play(FadeIn(label('?',2.5,.55,YELLOW,44)),run_time=.2)
        stamp=slots[0][0].copy();self.play(TransformFromCopy(VGroup(dish,a,b,paths),stamp),Transform(slots,boxes(1)),run_time=.5);self.remove(stamp);self.finish()

class S14P2(Timed):
    def construct(self):
        slots=boxes(1);self.add(slots)
        maps,path,soma,labs,dl,dr=dual(y=.45,scale=1.02)
        # Same anatomical parts on both maps; glow behind, never over, floor plate.
        self.add(maps,labs[:2])
        self.at('one cue');self.play(FadeIn(VGroup(*[Dot(d['p'](0,-1.96),radius=.75,color=YELLOW,fill_opacity=.12).set_z_index(-1) for d in [dl,dr]])),run_time=.3)
        self.at('pull commissural');self.play(Indicate(dl['crossing'],color=GREEN),FadeIn(label('toward',-3.45,-2.25,GREEN,28)),run_time=.6)
        self.at('push trochlear');self.play(FadeIn(soma),Create(path),FadeIn(label('away',3.45,-2.25,RED,28)),run_time=.6)
        stamp=slots[1][0].copy();self.play(TransformFromCopy(VGroup(maps,path,soma),stamp),Transform(slots,boxes(2)),run_time=.45);self.remove(stamp);self.finish()

class S15P3(Timed):
    def construct(self):
        slots=boxes(2);self.add(slots)
        a,da=cord((-3.45,.35,0),1.12,4,axes=False);b,db=cord((3.45,.35,0),1.12,4,axes=False);self.add(a,b)
        self.add(label('dorsal',-3.45,3.3,size=26),label('dorsal',3.45,3.3,size=26),label('ventral',-3.45,-2.4,size=26),label('ventral',3.45,-2.4,size=26))
        # Hypothesis diagram: opacity decreases with distance from the ventral source.
        shading=VGroup(*[Line(da['p'](-1.35,y),da['p'](1.35,y),color=YELLOW,stroke_width=16).set_opacity(.4*np.exp(-(y+1.8)/1.1)) for y in np.linspace(-1.8,1.5,14)])
        self.at('a gradient');self.play(FadeIn(shading),run_time=.4)
        deposits=VGroup(*[Dot(db['outline'].point_from_proportion(t),radius=.07,color=YELLOW) for t in np.linspace(.05,.95,35)])
        self.at('or laid along');self.play(FadeIn(deposits),run_time=.4)
        stamp=slots[2][0].copy();self.play(TransformFromCopy(VGroup(a,b,shading,deposits),stamp),Transform(slots,boxes(3)),run_time=.45);self.remove(stamp);self.finish()

class S16Predict(Timed):
    def construct(self):
        cards=choices();self.add(cards[0][0],cards[1][0],cards[2],cards[3],pause_track())
        self.at('direction written');self.play(FadeIn(cards[0][1]),run_time=.4)
        self.at('or does');self.play(FadeIn(cards[1][1]),run_time=.4);self.finish()

class S17Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(choices())
        self.add(pause_track())
        bar=Line([-5.9,-1.85,0],[-5.88,-1.85,0],color=BLUE,stroke_width=14);self.add(bar)
        self.play(bar.animate.put_start_and_end_on([-5.9,-1.85,0],[5.9,-1.85,0]),run_time=5,rate_func=linear)

class S18Reveal(Timed):
    def construct(self):
        cards=choices();self.add(cards)
        self.at('the second');self.play(cards[1][0].animate.set_stroke(BLUE,width=5),run_time=.4)
        r=rule();self.at('marks a place');self.play(FadeOut(cards),FadeIn(r[0]),run_time=.4)
        self.at('the growth cone');self.play(FadeIn(r[1:]),run_time=.4);self.finish()

class S19Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(rule());self.wait(2.5)

class S20Where(Timed):
    def construct(self):
        card=rulecard(0);g,d=cord((0,1,0),1.03,4,axes=False);self.add(card,g)
        # Build each text object once. Never morph between overlapping glyph layers.
        self.at('supplies the');self.play(FadeIn(label('WHERE',-4.1,-2.15,YELLOW,28)),run_time=.3)
        terms=VGroup(*[label(t,0,0,size=26) for t in ['source',' · slope',' · surface']]).arrange(RIGHT,buff=.02).move_to([-4.1,-2.85,0])
        self.at('its source');self.play(FadeIn(terms[0]),FadeIn(Dot(d['p'](0,-1.95),radius=.7,color=YELLOW,fill_opacity=.16).set_z_index(-1)),FadeIn(callout('source',(4,-.8),d['p'](0,-1.95),YELLOW)),run_time=.3)
        gradient=VGroup(*[Line(d['p'](-.7,y),d['p'](.7,y),color=YELLOW,stroke_width=16).set_opacity(.4*np.exp(-(y+1.7)/1.0)) for y in np.linspace(-1.7,1.3,12)])
        self.at('its slope');self.play(FadeIn(terms[1]),FadeIn(gradient),FadeIn(callout('slope',(-4.1,1.5),d['p'](-.6,.5),YELLOW)),run_time=.3)
        self.at('the surface');self.play(FadeIn(terms[2]),d['rim'].animate.set_color(YELLOW),FadeIn(callout('surface',(4,2.3),d['p'](1.8,1.3),YELLOW)),run_time=.3);self.finish()

class S21Sign(Timed):
    def construct(self):
        card=rulecard(1);self.add(card)
        l=growth((-3.8,.9,0),2.1);r=growth((3.8,.9,0),2.1).rotate(PI,about_point=[3.8,.9,0])
        self.add(l,r,Dot([0,1.3,0],radius=.38,color=YELLOW),label('netrin',0,2.05,YELLOW,28))
        self.at('supplies the sign');self.play(FadeIn(label('SIGN',0,-2.15,BLUE,28)),run_time=.3)
        lc=cups((-3.8,.9,0),[0,45,-45],TEAL,1.8);rc=cups((3.8,.9,0),[140,180,220],PURPLE,1.8)
        self.at('its receptors');self.play(FadeIn(label('receptors',0,-2.85,TEXT,26)),FadeIn(lc),FadeIn(rc),run_time=.4)
        self.at('usually draws');self.play(FadeIn(label('DCC · usually',-3.8,3.25,TEAL,28)),Create(CurvedArrow([-4.4,-1.3,0],[-1.2,-.1,0],angle=PI/3,color=GREEN)),VGroup(l,lc).animate.rotate(.12,about_point=[-3.8,.9,0]),run_time=.7)
        self.at('receptors add');self.play(FadeIn(label('UNC5',3.8,3.25,PURPLE,28)),Create(CurvedArrow([3,-.3,0],[5.8,-1.2,0],angle=-PI/3,color=RED)),VGroup(r,rc).animate.rotate(.18,about_point=[3.8,.9,0]),run_time=.7)
        self.at('sometimes with');self.play(FadeIn(cups((3.8,.9,0),[120],TEAL,1.8)),FadeIn(label('+ DCC sometimes',3.8,2.65,TEAL,26)),run_time=.4);self.finish()

class S22State(Timed):
    def construct(self):
        card=rulecard(2);g=growth((0,1,0),2.6);self.add(card,g)
        self.at('its internal');self.play(FadeIn(VGroup(*list(rulecard(3))[5:])),run_time=.4)
        inside=VGroup(label('cAMP',.35,1.45,ORANGE,30),label('calcium',.35,.65,size=28))
        self.at('such as');self.play(FadeIn(inside[0]),run_time=.3)
        self.at('or calcium');self.play(FadeIn(inside[1]),run_time=.3)
        surface=Line([-4.8,-1.08,0],[4.8,-1.08,0],color=ORANGE,stroke_width=6)
        self.at('a matrix protein');self.play(Create(surface),FadeIn(label('laminin',-3.8,-1.48,ORANGE,28)),run_time=.4)
        self.at('can change');self.play(GrowArrow(Arrow([0,-1.08,0],[0,-.1,0],color=ORANGE,buff=0)),inside[0].animate.set_opacity(.35),FadeIn(label('can change state',4.65,-.6,ORANGE,26)),FadeIn(label('Example: frog retinal growth cone',-1.7,3.5,size=26)),run_time=.5);self.finish()

class S23Limits(Timed):
    def construct(self):
        self.add(rulecard(3),label('The rule has limits',0,2.8,size=34))
        self.at('not always');self.play(FadeIn(chip('not always a long-range gradient',YELLOW,size=32).move_to([0,1.2,0])),run_time=.4)
        self.at('does more');self.play(FadeIn(chip('does more than steer',BLUE,size=32).move_to([0,-.45,0])),run_time=.2)
        # A three-second hold also captures both tags in the review sampling.
        self.wait(3);self.finish()

class S24Takeaway(Timed):
    def construct(self):
        g,d=cord((-2.65,.5,0),1.0,5,True,axes=False)
        inset,e=cord((3.8,.5,0),.84,1,axes=False)
        p=e['p'];path=smooth([p(x,y) for x,y in [(.5,-1.55),(1.5,-1.05),(1.9,.1),(1.25,1.65)]],RED)
        slots=boxes(3)
        self.add(g,inset,path,Dot(p(.5,-1.55),radius=.13,color=RED),slots,
                 label('spinal cord',-2.65,3.3,size=28),label('midbrain–hindbrain',3.8,3.3,size=26),
                 callout('dorsal neuron',(-5.15,2.65),d['p'](-.95,1.45),BLUE,26),
                 callout('floor plate',(-2.65,-2.25),d['p'](0,-1.96),ORANGE,26),
                 callout('ventricular zone',(.25,1.65),d['p'](.5,.9),TEAL,26),
                 callout('pial surface',(-5.15,-1.5),d['p'](-2.1,-.6),ORANGE,26),
                 label('trochlear axon',3.8,-1.9,RED,26))
        self.at('each chapter');self.play(Indicate(slots,scale_factor=1.02,color=YELLOW),run_time=.5);self.finish()

class S25End(EndCard):
    LINE='Netrin marks a place;\nthe growth cone decides what to do there.'
