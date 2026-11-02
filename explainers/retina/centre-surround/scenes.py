"""Centre Minus Surround — chapter 3.

COLOR MAP (shared with scenes.old.py; CHAPTERS.md is not editable in this task):
YELLOW light; BLUE photoreceptors / inward cations; TEAL glutamate;
PURPLE cGMP; ORANGE phototransduction / G protein; GREEN ON pathway;
PINK OFF pathway; RED inhibitory T-bars; GOLD ganglion output; GREY structure.
M/L/S spectral plots use BLUE photoreceptor curves with letter labels.

Models: spot area weighting from CentreSurroundSpot.astro: 20+40*c-15*s,
c=min(r,1)^2, s=max(0,min(r,2)^2-1)/3. Edge uses the script's symmetric
linear DoG: 40*Phi(x/.45)-15*Phi(x/1.25), relative to uniform dark.
Spectra: lesson's Govardovskii A1 alpha+beta template, peaks 420/530/560 nm.
No curves are freehand. Spike ticks are schematic, not experimental recordings.
"""
import importlib.util
from pathlib import Path
from math import erf, sqrt
import numpy as np
from bp_style import *

_spec = importlib.util.spec_from_file_location('retina_reference', Path(__file__).parent.parent / 'scenes.old.py')
_old = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_old)
PURPLE, ORANGE, PINK = _old.PURPLE, _old.ORANGE, _old.PINK
arr, tbar, spikes, bip_cell = _old.arr, _old.tbar, _old.spikes, _old.bip_cell


def pigment(w,p):
    w=np.asarray(w); x=p/w
    a=.8795+.0459*np.exp(-(p-300)**2/11940)
    alpha=1/(np.exp(69.7*(a-x))+np.exp(28*(.922-x))+np.exp(-14.9*(1.104-x))+.674)
    beta=.26*np.exp(-((w-(189+.315*p))/(-40.5+.195*p))**2)
    return alpha+beta



# Keep cue timing without mutating the pipeline's sync.log (task output scope).
_BaseSpokenScene = SpokenScene
class SpokenScene(_BaseSpokenScene):
    def at(self, phrase, lead=.2, nth=0):
        rest=self.t_of(phrase,nth)-lead-self.elapsed()
        if rest>.02: self.wait(rest)


def lab(s,x=0,y=3.25,c=TEXT,size=30):
    return T(s,size=size,color=c).move_to([x,y,0])


def field(x=-3.3,y=.15,r=2.7,mode='none',signs=False,off=False):
    col=PINK if off else GREEN
    ring=Annulus(inner_radius=r*.5,outer_radius=r,color=GREY,fill_opacity=.12,stroke_width=2).move_to([x,y,0])
    centre=Circle(radius=r*.5,color=col,fill_opacity=.13,stroke_width=3).move_to([x,y,0])
    if mode in ('ring','full'): ring.set_fill(YELLOW,.5)
    if mode in ('spot','full'): centre.set_fill(YELLOW,.8)
    g=VGroup(ring,centre)
    if signs:
        g.add(lab('−' if off else '+',x,y,col,52))
        for dx,dy in ((0,.75),(0,-.75),(.75,0),(-.75,0)):
            g.add(lab('+' if off else '−',x+dx*r,y+dy*r,PINK if off else RED,38))
    return g


def train(rate=20,x0=.1,x1=6.2,y=0,h=2.1):
    # Explicit common 0.4 s schematic window: no Transform between unequal tick counts.
    n=max(0,round(rate*.4)); base=y-h/2
    return VGroup(Line([x0,base,0],[x1,base,0],color=GREY,stroke_width=2),
        *[Line([x,base,0],[x,base+h,0],color=GOLD,stroke_width=3) for x in np.linspace(x0+.12,x1-.12,n)])


def replace(scene,old,new,rt=.25):
    scene.play(FadeOut(old),FadeIn(new),run_time=rt)
    return new


def spotrate(r):
    return 20+40*min(r,1)**2-15*max(0,min(r,2)**2-1)/3


def question():
    return VGroup(field(mode='full'),lab('Whole field lit',-3.3,3.25,YELLOW),
        lab('More than the best spot?',3.1,1.4,size=28),lab('Fewer?',3.1,.1,size=28),
        lab('No change from background?',3.1,-1.2,size=28),lab('Predict the spike rate',0,-3.25,GOLD,32))


def paired():
    return VGroup(field(-3.35,.4,2.25,'spot'),field(3.35,.4,2.25,'full'),
        lab('Small spot',-3.35,3.15,YELLOW),lab('Full field',3.35,3.15,YELLOW))


def circuit():
    # Match each spatial part of the receptive field to its circuit path.
    rf=VGroup(field(-4.65,1.5,1.6),lab('receptive field',-4.65,3.35,size=27),
        lab('centre',-4.65,1.5,GREEN,26),lab('surround',-4.65,.25,RED,26))
    cones=VGroup(*[chip('cones: '+t,BLUE,22).move_to([x,2.45,0]) for x,t in ((-.9,'surround'),(2,'centre'),(4.9,'surround'))])
    bips=VGroup(*[bip_cell(x,.25,.55,.75,GREEN) for x in (1.5,2.5)])
    direct=VGroup(*[arr(cones[1].get_bottom(),[x,.72,0],GREEN) for x in (1.5,2.5)],
        *[arr([x,-.15,0],[2,-1.85,0],GREEN) for x in (1.5,2.5)],lab('bipolar cells',3.9,.25,GREEN,26))
    gang=chip('ganglion cell',GOLD,28).move_to([2,-2.3,0])
    side=chip('sideways cells',RED,26).move_to([-.6,1.15,0])
    # Exact contacts: arrowheads and inhibitory bars touch box edges.
    feedback_end=cones[1].get_left()
    feedback=VGroup(Line(side.get_right(),feedback_end,color=RED,stroke_width=4),
        Line(feedback_end+UP*.2,feedback_end+DOWN*.2,color=RED,stroke_width=5))
    lateral=VGroup(side,
        Arrow(cones[0].get_bottom(),side.get_top(),buff=0,color=RED,tip_length=.17),
        Arrow(cones[2].get_bottom(),side.get_right(),buff=0,color=RED,tip_length=.2),feedback,
        DashedLine([-3.12,2,0],side.get_left(),color=RED,stroke_width=3))
    return rf,cones,bips,direct,gang,lateral


def edge_stage(model=False):
    # Separate circular windows sample the same straight edge; display spacing is expanded.
    xs=np.array([-4.8,-2.4,0,2.4,4.8]); offsets=np.array([-3,-.88,0,.88,3])
    fs=VGroup(); bg=VGroup(lab('dark side',-4.7,2.95,size=26),lab('light side',4.7,2.95,YELLOW,26))
    for x,d in zip(xs,offsets):
        f=field(x,1.5,1.05)
        lit=Intersection(Circle(1.05).move_to([x,1.5,0]),Rectangle(width=10,height=4).move_to([x-d*.7+5,1.5,0]),fill_color=YELLOW,fill_opacity=.3,stroke_width=0)
        f.add_to_back(lit)
        fs.add(f)
    yy=-2.35; scale=.085
    vals=np.array([40*(1+erf(d/.45/sqrt(2)))/2-15*(1+erf(d/1.25/sqrt(2)))/2 for d in offsets])
    bs=VGroup(*[Rectangle(width=.85,height=max(.015,abs(v)*scale),fill_color=GOLD,fill_opacity=.85,stroke_width=0).move_to([x,yy+v*scale/2,0]) for x,v in zip(xs,vals)])
    ax=VGroup(Line([-5.5,yy,0],[5.6,yy,0],color=GREY),
        DashedLine([-5.5,yy+25*scale,0],[5.6,yy+25*scale,0],color=GREY),
        *[lab(str(v),-6,yy+v*scale,GREY,26) for v in (0,12.5,25)],
        lab('Change from uniform-dark firing (spikes/s)',0,-3.05,size=26),
        lab('Field spacing expanded; model differences exaggerated',0,-3.55,GREY,26),
        *[DashedLine([x,.4,0],[x,max(yy+v*scale,yy)+.08,0],color=GREY,stroke_opacity=.4) for x,v in zip(xs,vals)])
    title=lab('Model: symmetric centre and surround' if model else 'ON-centre cells across an edge',0,3.5,GREEN,30)
    return bg,fs,bs,ax,title


def spectral(peaks=(530,560),ratio=False):
    ymax=2.2 if ratio else 1.15
    ax=Axes(x_range=[400,700,100],y_range=[0,ymax,.5],x_length=10.6,y_length=4.1,tips=False,
        axis_config={'color':GREY,'include_ticks':False}).move_to([.25,.75,0])
    cs=VGroup()
    for p in peaks:
        fn=(lambda w:pigment(w,530)/pigment(w,560)) if ratio else (lambda w,p=p:pigment(w,p))
        cs.add(VMobject(color=BLUE,stroke_width=5).set_points_as_corners([ax.c2p(w,fn(w)) for w in np.linspace(400,700,401)]))
    ls=VGroup(lab('M/L ratio' if ratio else 'relative sensitivity',-3.9,3.35,BLUE,28),
        lab('wavelength (nm)',.25,-2.3,size=26),
        *[lab(str(w),ax.c2p(w,0)[0],-1.6,GREY,26) for w in (400,500,600,700)],
        *[lab(str(v),-5.65,ax.c2p(400,v)[1]+(.18 if v==0 else 0),GREY,26) for v in (0,1)])
    return ax,cs,ls


class S00Title(TitleCard):
    LESSON='The Retina'
    TITLE='Centre Minus Surround'


class S01Question(SpokenScene):
    def construct(self):
        p=paired(); self.add(p,lab('Why does a ganglion cell prefer a small spot\nto light over the whole retina?',0,-3.3,size=28))
        self.at('a ganglion cell')
        self.play(FadeIn(lab('ganglion cell spikes',-3.35,-2.05,GOLD,26)), FadeIn(lab('ganglion cell spikes',3.35,-2.05,GOLD,26)),run_time=.25)
        self.at('a small spot')
        self.play(FadeIn(train(80,-5.8,-.9,-2.45,.45)),run_time=.3)
        self.at('light spread')
        self.play(FadeIn(train(25,.9,5.8,-2.45,.45)),run_time=.3)
        self.finish()


class S02Kuffler(SpokenScene):
    def construct(self):
        retina=Ellipse(width=10.5,height=6.1,color=GREY,fill_opacity=.1).move_to([0,0,0])
        cell=bip_cell(.6,-.7,1.2,.9,GOLD)
        dend=VGroup(*[Line([.6,-.3,0],[x,.65,0],color=GOLD,stroke_width=3) for x in (-1,.6,2)])
        self.add(retina,cell,dend,lab('cat retina',-2.5,-1.9,size=28),lab('Kuffler, 1953',-3.1,3.45,size=32),lab('dendrites',-.8,1.1,GOLD,26))
        self.at('recorded single')
        electrode=Line([4.3,2.2,0],[1.15,-.6,0],color=TEXT,stroke_width=5)
        self.play(Create(electrode),FadeIn(lab('electrode',4.6,2.65,size=27)),
            FadeIn(lab('ganglion cell',2.7,-1.2,GOLD,28)),run_time=.5)
        self.at('small spots')
        spot=Circle(radius=.42,color=YELLOW,fill_opacity=.8).move_to([-2.8,.3,0])
        self.play(FadeIn(spot),run_time=.2)
        for pos in ((-3.2,1.2,0),(-1.8,1.9,0),(-2.8,-.6,0)):
            self.play(spot.animate.move_to(pos),run_time=.45)
        self.finish()


class S03Centre(SpokenScene):
    def construct(self):
        f=field(); tr=train(); tag=lab('baseline',3.1,-1.6,GOLD)
        self.add(f,tr,tag,lab('ganglion cell spikes',3.1,2.3,GOLD),lab('receptive field',-3.3,3.3))
        self.at('A spot'); self.play(Transform(f,field(mode='spot')),run_time=.35)
        self.at('fire faster')
        replace(self,tr,train(60)); replace(self,tag,lab('centre light on',3.1,-1.6,YELLOW))
        self.finish()


class S04Surround(SpokenScene):
    def construct(self):
        f=field(); tr=train(); tag=lab('baseline',3.1,-1.65,GOLD)
        self.add(f,tr,tag,lab('ganglion cell spikes',3.1,2.3,GOLD),lab('receptive field',-3.3,3.3))
        self.at('a ring')
        self.play(Transform(f,field(mode='ring')),run_time=.35)
        tr=replace(self,tr,train(0)); tag=replace(self,tag,lab('annulus on · silent',3.1,-1.65,YELLOW))
        self.at('fall silent'); self.play(Indicate(tr,color=GREY),run_time=.3)
        self.at('light went off')
        self.play(Transform(f,field()),run_time=.2)
        tag=replace(self,tag,lab('light off · burst',3.1,-1.65,GOLD),.2)
        self.at('it fired'); replace(self,tr,train(75),.2)
        self.finish()


class S05Types(SpokenScene):
    def construct(self):
        a=field(-3.35,.1,2.65,signs=True); self.add(a,lab('ON-centre',-3.35,3.3,GREEN,34))
        self.at('An off')
        self.play(FadeIn(field(3.35,.1,2.65,signs=True,off=True)),FadeIn(lab('OFF-centre',3.35,3.3,PINK,34)),run_time=.45)
        self.at('mirror image'); self.play(FadeIn(lab('Opposite responses to centre and surround light',0,-3.25,size=28)),run_time=.3)
        self.finish()


class S06Source(SpokenScene):
    def construct(self):
        rf,cones,bips,direct,gang,lat=circuit(); self.add(rf,cones,gang,lab('photoreceptor input',2,3.45,BLUE,26))
        links=VGroup(DashedLine([-3.85,1.5,0],[-2.7,.25,0],color=GREEN),
            *[DashedLine([-2.7,.25,0],b.get_left(),color=GREEN,stroke_width=2) for b in bips])
        self.at('bipolar cells'); self.play(FadeIn(bips),Create(direct),Create(links),run_time=.55)
        self.at('contact the ganglion'); self.play(Indicate(gang),run_time=.4)
        self.at('The surround'); self.play(rf[0][0].animate.set_stroke(RED,width=4),Create(lat[4]),run_time=.4)
        self.at('act sideways'); self.play(FadeIn(VGroup(*lat[:4])),run_time=.6)
        self.finish()


class S07Lateral(SpokenScene):
    def construct(self):
        rf,cones,bips,direct,gang,lat=circuit()
        bands=VGroup(Rectangle(width=8.7,height=2.35,stroke_width=0,fill_color=BLUE,fill_opacity=.045).move_to([2,1.95,0]),
            Rectangle(width=8.7,height=3.45,stroke_width=0,fill_color=GOLD,fill_opacity=.035).move_to([2,-1.05,0]),
            lab('outer retina',2,3.25,TEXT,24),lab('inner retina',-.9,-.65,TEXT,24))
        self.add(bands,rf,cones,bips,direct,gang)
        self.at('Horizontal cells')
        lat[0][1].become(T('horizontal',size=26,color=RED).move_to(lat[0][1]))
        self.play(FadeIn(lat),run_time=.45)
        self.at('outer retina')
        self.play(FadeIn(lab('Feedback mechanism still debated',0,-3.4,TEXT,28)),run_time=.3)
        self.at('add more')
        ama=chip('amacrine',RED,26).move_to([4.8,-1.1,0])
        contact=gang.get_right()
        path=VGroup(VMobject(color=RED,stroke_width=4).set_points_as_corners([cones[2].get_right(),[6.45,2.45,0],[6.45,-1.1,0]]),
            Arrow([6.45,-1.1,0],ama.get_right(),buff=0,color=RED,tip_length=.18),
            Line(ama.get_bottom(),contact,color=RED,stroke_width=4),
            Line(contact+UP*.23,contact+DOWN*.23,color=RED,stroke_width=5))
        self.play(FadeIn(ama),Create(path),run_time=.5)
        self.at('opposite way')
        light=VGroup(*[Circle(.25,color=YELLOW,fill_opacity=.8).move_to([x,3.25,0]) for x in (-.9,4.9)])
        signs=VGroup(lab('+',.65,-1.55,GREEN,44),lab('−',4.65,-2.3,RED,44),
            arr([.6,-.7,0],[.6,-1.3,0],GREEN),Arrow([5.7,-1.65,0],[5.1,-2.3,0],buff=0,color=RED,tip_length=.18))
        self.play(FadeIn(light),Create(signs),run_time=.6)
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        q=question(); self.add(q[0],q[5])
        for phrase,i in (('whole field',1),('More spikes',2),('fewer',3),('no change',4)):
            self.at(phrase); self.play(FadeIn(q[i]),run_time=.25)
        self.finish()


class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question()); self.wait(5)


class S10Reveal(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,2.5,1],y_range=[0,70,20],x_length=7.6,y_length=4.9,tips=False,
            axis_config={'color':GREY,'include_ticks':False}).move_to([-1.85,.15,0])
        def tick(v): return lab(str(v),-6.1,ax.c2p(0,v)[1],GREY,26)
        base=DashedLine(ax.c2p(0,20),ax.c2p(2.5,20),color=GREY)
        self.add(ax,base,tick(0),tick(20),lab("Worked example: this example's weights",0,3.45,size=30),
            lab('spikes/s',-4.8,2.9,GOLD,26),lab('background 20',-.5,-1.35,GREY,26),
            lab('spot radius (centre edge = 1)',-1.8,-3.0,size=26),
            *[lab(str(v),ax.c2p(v,0)[0],-2.6,GREY,26) for v in (0,1,2)])
        self.at('fewer')
        curve=VMobject(color=GOLD,stroke_width=5).set_points_as_corners([ax.c2p(r,spotrate(r)) for r in np.linspace(0,2.5,301)])
        self.play(Create(curve),run_time=.45)
        self.at('spikes a second')
        full=VGroup(tick(45),Dot(ax.c2p(2.3,45),color=GOLD),lab('full field 45',.8,.25,GOLD,26),
            lab('Full field · 45',4.4,.05,GOLD,28),train(45,2.8,6.1,-1.1,1.1))
        self.play(FadeIn(full),run_time=.3)
        self.at('instead of')
        best=VGroup(tick(60),Dot(ax.c2p(1,60),color=GOLD),lab('best spot 60',-1.8,2.7,GOLD,26),
            lab('Best spot · 60',4.4,2.65,GOLD,28),train(60,2.8,6.1,1.45,1.1))
        self.play(FadeIn(best),run_time=.3)
        self.at('Its surround')
        plus=BraceBetweenPoints(ax.c2p(1,20),ax.c2p(1,60),direction=LEFT,color=GREEN)
        minus=BraceBetweenPoints(ax.c2p(2,60),ax.c2p(2,45),direction=RIGHT,color=RED)
        braces=VGroup(plus,T('+40',size=26,color=GREEN).next_to(plus,LEFT,buff=.12),
            minus,T('−15',size=26,color=RED).next_to(minus,RIGHT,buff=.12))
        self.play(FadeIn(braces),FadeIn(lab('20 + 40 − 15 = 45',3.9,-2.75,size=28)),run_time=.4)
        self.finish()


class S11Contrast(SpokenScene):
    def construct(self):
        p=paired(); self.add(p,lab('Spot 60 spikes/s',-3.35,-2.35,GOLD),lab('Uniform 45 spikes/s',3.35,-2.35,GOLD),lab('Contrast more than brightness',0,-3.3,size=32))
        self.at('reports contrast'); self.play(Indicate(p[0][1],color=YELLOW),run_time=.5)
        self.at('more than overall'); self.play(Indicate(p[1],color=GREY,scale_factor=1.03),run_time=.5)
        self.finish()


class S12Edge(SpokenScene):
    def construct(self):
        bg,fs,bs,ax,title=edge_stage(); self.add(bg,title,ax)
        self.at('line up a row'); self.play(LaggedStart(*[FadeIn(f) for f in fs],lag_ratio=.1),run_time=.6)
        self.at('light meets dark'); self.play(FadeIn(bs),run_time=.5)
        self.finish()


class S13Bright(SpokenScene):
    def construct(self):
        bg,fs,bs,ax,title=edge_stage(); self.add(bg,fs,bs,ax,title)
        self.at('right on the edge')
        self.play(fs[2].animate.set_stroke(TEXT,width=5),bs[2].animate.set_color(TEXT),FadeIn(lab('about half',.4,-1.0,size=26)),run_time=.35)
        self.at('In this model')
        title=replace(self,title,lab('Model: symmetric centre and surround',0,3.45,GREEN,30),.18)
        self.at('bright side fire most')
        self.play(fs[3].animate.set_stroke(GOLD,width=5),bs[3].animate.set_color(YELLOW),run_time=.4)
        self.at('surrounds reach')
        # Only the dark-side segment of this annulus is tinted.
        patch=Intersection(Annulus(inner_radius=.525,outer_radius=1.05).move_to([2.4,1.5,0]),
            Rectangle(width=10,height=6).move_to([-3.216,1.5,0]),color=RED,fill_opacity=.7,stroke_width=0)
        # Graphic circle spacing is expanded; map model-space dark overlap to visible cap.
        self.play(FadeIn(patch),FadeIn(lab('subtracts less',4.4,.23,RED,26)),run_time=.4)
        self.finish()


class S14Dark(SpokenScene):
    def construct(self):
        bg,fs,bs,ax,title=edge_stage(True); self.add(bg,fs,bs,ax,title)
        self.at('just on the dark')
        self.play(fs[1].animate.set_stroke(RED,width=5),bs[1].animate.set_color(RED),run_time=.4)
        self.play(FadeIn(lab('undershoot',-3.9,-1.4,RED,26)),FadeIn(lab('overshoot',1.05,-.8,GOLD,26)),run_time=.3)
        self.play(Create(Arrow([-3.9,-1.7,0],bs[1].get_bottom(),buff=0,color=RED,tip_length=.18)),
            Create(Arrow([1.4,-.5,0],bs[3].get_top(),buff=0,color=GOLD,tip_length=.18)),run_time=.3)
        self.at('edge stands out')
        takeaway=lab('The edge stands out across the population',0,3.45,GOLD,30)
        replace(self,title,takeaway,.2)
        self.play(Indicate(bs[1],color=RED),Indicate(bs[3],color=GOLD),run_time=.6)
        self.finish()


class S15Colour(SpokenScene):
    def construct(self):
        ax,cs,ls=spectral((560,)); plot=VGroup(ax,cs,ls).scale(.67).move_to([-2.7,.55,0])
        for label in ls: label.scale(1/.67)
        # Position typography after scaling so ticks, origin and title have distinct rows.
        ls[1].move_to([-2.7,-2.15,0])
        for label,w in zip(ls[2:6],(400,500,600,700)):
            label.move_to([ax.c2p(w,0)[0],-1.65,0])
        ls[6].move_to([ax.c2p(400,0)[0]-.4,ax.c2p(400,0)[1]+.18,0])
        self.add(plot,lab('one cone',-1,2.9,BLUE,30),lab('One cone cannot separate wavelength from intensity',0,-3.4,size=29))
        self.at('One cone')
        self.play(Indicate(cs[0],scale_factor=1.02),run_time=.35)
        factor=float(pigment(560,560)/pigment(620,560))
        points=VGroup(*[Dot(ax.c2p(w,pigment(w,560)),color=YELLOW) for w in (560,620)])
        tags=VGroup(lab('dim, 560 nm',3.9,2.65,YELLOW,28),lab('intensity 1.00',3.9,2.15,size=26),
            lab('bright, 620 nm',3.9,.25,YELLOW,28),lab('intensity %.2f'%factor,3.9,-.25,size=26))
        leaders=VGroup(Line(points[0].get_center(),[2.35,2.65,0],color=YELLOW),
            Line(points[1].get_center(),[2.35,.25,0],color=YELLOW))
        self.at('change in wavelength'); self.play(FadeIn(points),FadeIn(tags),Create(leaders),run_time=.35)
        self.at('change in intensity')
        responses=VGroup(*[VGroup(Rectangle(width=1.3,height=.65,color=BLUE,fill_opacity=.55),
            T('1.00',size=26)).move_to([3.9,y,0]) for y in (1.45,-.95)],
            Line([3.9,1.85,0],[3.9,1.775,0],color=BLUE),Line([3.9,-.55,0],[3.9,-.625,0],color=BLUE),
            Line([4.65,1.45,0],[5.8,1.45,0],color=GOLD),Line([5.8,1.45,0],[5.8,.55,0],color=GOLD),Line([5.8,-.05,0],[5.8,-.95,0],color=GOLD),
            Line([5.8,-.95,0],[4.65,-.95,0],color=GOLD),lab('=',5.8,.25,GOLD,30),
            lab('same mean response',3.9,-1.85,GOLD,26),lab('same timing and adaptation',0,-2.75,TEXT,28))
        self.play(FadeIn(responses),run_time=.35)
        self.finish()


class S16Ratio(SpokenScene):
    def construct(self):
        ax,cs,ls=spectral(); m=lab('M',-1,2.9,BLUE,30); l=lab('L',1.2,2.9,BLUE,30)
        self.add(ax,cs[0],ls,m)
        self.at('two cones'); self.play(Create(cs[1]),FadeIn(l),run_time=.4)
        w=ValueTracker(530); intensity=ValueTracker(1)
        marker=always_redraw(lambda: VGroup(DashedLine(ax.c2p(w.get_value(),0),ax.c2p(w.get_value(),1.05),color=YELLOW),lab('%.0f nm'%w.get_value(),3.9,3.35,YELLOW,28)))
        read=always_redraw(lambda: lab('M/L = %.2f'%(pigment(w.get_value(),530)/pigment(w.get_value(),560)),3.9,-2.6,GOLD,30))
        catches=always_redraw(lambda: lab('M catch %.3f      L catch %.3f'%(intensity.get_value()*pigment(w.get_value(),530),intensity.get_value()*pigment(w.get_value(),560)),0,-3.3,BLUE,28))
        self.at('their ratio changes'); self.add(marker,read,catches)
        self.wait(.35); self.play(w.animate.set_value(600),run_time=1.1,rate_func=linear)
        self.at('Turn the light up')
        slider=VGroup(lab('light intensity',-3.8,-2.55,YELLOW,26),Line([-2,-2.55,0],[0,-2.55,0],color=YELLOW))
        knob=Dot([-2,-2.55,0],color=YELLOW)
        self.add(slider,knob)
        self.play(intensity.animate.set_value(2),knob.animate.shift(RIGHT*2),run_time=1.1)
        self.at('the ratio holds'); self.play(FadeIn(lab('ratio unchanged',3.9,-1.95,GOLD,26)),run_time=.25)
        self.finish()


class S17Tie(SpokenScene):
    def construct(self):
        w1=427.; target=float(pigment(w1,530)/pigment(w1,560)); lo,hi=510.,550.
        for _ in range(50):
            mid=(lo+hi)/2
            if pigment(mid,530)/pigment(mid,560)>target: lo=mid
            else: hi=mid
        w2=(lo+hi)/2
        ax,cs,ls=spectral((530,),True); model=lab('Pigment-template model',2,3.35,TEXT,30)
        self.add(ax,cs,ls,model)
        self.at('ratio can repeat')
        marks=VGroup(*[Dot(ax.c2p(w,target),color=YELLOW,radius=.1) for w in (w1,w2)],
            DashedLine(ax.c2p(w1,target),ax.c2p(w2,target),color=GOLD),
            lab('427 nm: M/L = %.1f'%target,-3,-2.8,GOLD,28),lab('≈529 nm: M/L = %.1f'%target,3,-2.8,GOLD,28))
        self.play(FadeIn(marks),run_time=.35)
        self.at('Set two wavelengths')
        self.play(FadeOut(VGroup(ax,cs,ls,model,marks)),run_time=.15)
        head=lab('Intensities scaled for equal L catch',0,3.35,size=30)
        columns=VGroup(lab('427 nm',-2.5,2.65,YELLOW,30),lab('≈529 nm',2.5,2.65,YELLOW,30))
        def catchbars(name,v,xoffset):
            return VGroup(*[VGroup(Rectangle(width=.8,height=3.5*v,color=BLUE,fill_opacity=.6).move_to([x+xoffset,-2.1+3.5*v/2,0]),
                lab('%s %.2f'%(name,v),x+xoffset,-2.65,BLUE,28)) for x in (-2.5,2.5)])
        lb=catchbars('L',1,-.65); mb=catchbars('M',target,.65)
        self.play(FadeIn(head),FadeIn(columns),GrowFromEdge(lb,DOWN),run_time=.35)
        self.at('their M catches'); self.play(GrowFromEdge(mb,DOWN),run_time=.4)
        self.at('The S cone')
        self.play(FadeOut(VGroup(head,columns,lb,mb)),run_time=.15)
        sa,sc,sl=spectral((420,)); self.add(sa,sl,lab('What the S cone adds',2.5,3.35,BLUE,30))
        self.play(Create(sc),run_time=.45)
        sv=[float(pigment(w,420)/pigment(w,560)) for w in (w1,w2)]
        sm=VGroup(*[VGroup(DashedLine(sa.c2p(w,0),sa.c2p(w,pigment(w,420)),color=YELLOW),Dot(sa.c2p(w,pigment(w,420)),color=YELLOW)) for w in (w1,w2)])
        self.at('far more'); self.play(FadeIn(sm),FadeIn(lab('427 nm: S/L %.1f'%sv[0],-3,-2.75,GOLD,28)),FadeIn(lab('≈529 nm: S/L %.3f'%sv[1],3,-2.75,GOLD,28)),run_time=.4)
        self.at('tells them apart'); self.play(Indicate(sm[0],color=YELLOW),FadeIn(lab('Equal L and M catches; different S catch',0,-3.45,size=28)),run_time=.4)
        self.finish()


class S18Rule(SpokenScene):
    def construct(self):
        a=chip('cone A',BLUE,32).move_to([-3,1.8,0]); b=chip('cone B',BLUE,32).move_to([3,1.8,0]); node=chip('comparison',GOLD,34).move_to([0,-.5,0])
        self.add(a,b,node,arr([-3,1.25,0],[-.8,0,0],BLUE),arr([3,1.25,0],[.8,0,0],BLUE))
        self.at('One receptor cannot')
        self.play(FadeIn(lab('One receptor cannot separate wavelength from intensity',0,3.3,size=29)),run_time=.25)
        self.at('wavelength from intensity')
        self.play(FadeIn(lab('wavelength from intensity',0,-1.7,YELLOW,34)),run_time=.25)
        self.at('The circuit compares')
        self.play(FadeIn(lab('The circuit compares.',0,-2.9,GOLD,40)),run_time=.2)
        self.wait(2); self.finish()


class S19Takeaway(SpokenScene):
    def construct(self):
        g=chip('ganglion cells\ncontrast + colour',GOLD,26).move_to([-4.35,0,0]); brain=Ellipse(width=2.8,height=4.6,color=GREY,fill_opacity=.15).move_to([4.6,0,0])
        path=Line([-2.5,0,0],[3.1,0,0],color=GOLD,stroke_width=5)
        icons=VGroup(field(-4.35,1.9,.75,mode='spot'),lab('contrast',-4.35,3, GREEN,28),
            chip('M / L / S',BLUE,28).move_to([-4.35,-1.8,0]),lab('colour',-4.35,-2.65,BLUE,28))
        self.add(g,brain,lab('brain',4.6,0,size=32),path,icons,lab('optic nerve',.2,-1.55,GOLD,30))
        self.at('ganglion cells send')
        phase=ValueTracker(0)
        packets=always_redraw(lambda: VGroup(*[Line([x,-.6,0],[x,.6,0],color=GOLD,stroke_width=4) for x in [-2.25+((j*1.73+phase.get_value())%6.0) for j in range(3)]]))
        self.add(packets)
        self.play(phase.animate.set_value(13.7),run_time=max(1,self.narration_s-self.elapsed()),rate_func=linear)
        self.finish()


class S20End(EndCard):
    LINE='Ganglion cells compare centre and surround, then send spikes to brain.'
    def construct(self):
        self.add(lab('Centre minus surround',0,1.8,GOLD,44),
            lab('Edges and colour come from comparison.',0,.2,size=36),
            lab('Ganglion cells send the result as spikes.',0,-1.1,size=32),
            lab('biochemistrypedia.com',0,-2.8,TEAL,26))
        self.finish()
