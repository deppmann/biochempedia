"""Chapter 2: Something Crosses the Gel.
COLOR MAP: YELLOW netrin/cue; BLUE axon; TEAL DCC; PURPLE #B58CD9
UNC5; ORANGE #F29E4C cAMP; PINK #E58BD0 anti-DCC; GREEN attraction;
RED repulsion; GREY tissue/apparatus. White is explanatory text.
All trails are schematic, never measurements. Turning paths integrate a
constant-speed heading relaxation toward the source; diffusion particles use
seeded Brownian displacements. No quantitative data or sequence identities
are invented; sequence bars are plain alignment cartoons.
"""
import numpy as np
from bp_style import *
LESSON = 'Netrin and DCC: One Cue, Two Answers'

def label(s,x=0,y=3.2,c=TEXT,size=30):
    return T(s,size=size,color=c).move_to([x,y,0])

def explant(pos,color=BLUE):
    return RoundedRectangle(width=1.5,height=1.8,corner_radius=.2,color=color,
        fill_color=color,fill_opacity=.3).move_to(pos)

def gel():
    # Perspective block, distinct from a dish. Texture stays behind the tissue.
    face=RoundedRectangle(width=11.6,height=5.7,corner_radius=.2,color=GREY,
        fill_color=GREY,fill_opacity=.07).move_to([0,-.1,0])
    edge=VGroup(Line([-5.8,-2.95,0],[-5.35,-3.25,0],color=GREY),
        Line([-5.35,-3.25,0],[6.1,-3.25,0],color=GREY),
        Line([6.1,-3.25,0],[6.1,2.4,0],color=GREY),
        Line([6.1,2.4,0],[5.8,2.75,0],color=GREY),
        Line([5.8,-2.95,0],[6.1,-3.25,0],color=GREY))
    texture=VGroup(*[Line([x,-2.7,0],[x+.5,-2.35,0],color=GREY,
        stroke_width=1,stroke_opacity=.2) for x in np.arange(-5.3,5.2,.7)])
    return VGroup(face,edge,texture)

def assay(pair=False,growth=False,question=False,control=False):
    g=VGroup(gel(),explant([-3.9,0,0]),label('dorsal explant',-3.9,1.45,BLUE,34))
    if pair:g.add(explant([3.9,0,0],GREY),label('floor plate explant',3.6,1.45,TEXT,28))
    if growth:g.add(bundles())
    if question:g.add(label('Alone, what does it do?',size=34))
    if control:g.add(label('Control: few or no axons',0,-2.35,size=32))
    return g

def turning_paths(source=(3.9,0),curved=True):
    # Discrete schematic model: heading relaxes toward source with response .09.
    paths=VGroup()
    for y,angle in [(-.65,-.65),(-.23,-.25),(.23,.25),(.65,.65)]:
        q=np.array([-3.15,y]);h=np.array([np.cos(angle),np.sin(angle)])
        pts=[np.r_[q,0]]
        for _ in range(130):
            aim=np.array(source)+np.array([0,y*.9])-q;aim/=np.linalg.norm(aim)
            if curved:h=.91*h+.09*aim;h/=np.linalg.norm(h)
            q=q+.045*h;pts.append(np.r_[q,0])
        paths.add(VMobject(color=BLUE,stroke_width=5).set_points_as_corners(pts))
    return paths

def bundles():return turning_paths()

def radial(center=ORIGIN,r=2.7,half_size=None):
    p=np.array(center,dtype=float)
    return VGroup(*[Line(p+(min(half_size[0]/max(abs(np.cos(a)),1e-6),
        half_size[1]/max(abs(np.sin(a)),1e-6)) if half_size else .8)*np.array([np.cos(a),np.sin(a),0]),
        p+r*np.array([np.cos(a),np.sin(a),0]),color=BLUE,stroke_width=5)
        for a in np.linspace(0,TAU,12,endpoint=False)])

def radial_stage(question=False,answer=False):
    g=VGroup(explant(ORIGIN).scale(1.5),radial(r=2.95,half_size=(1.125,1.35)))
    if question:g.add(label('Growth, or steering?',size=34),label('Assay scored: outgrowth yes or no',0,-3.4,size=34))
    if answer:g[0:2].shift(LEFT*1.4);g.add(label('Outgrowth is not direction',size=36),scorecard())
    return g

def scorecard(first=True,second=True):
    g=VGroup()
    if first:g.add(label('✓ outgrowth scored',4.25,1.15,GREEN,34))
    if second:g.add(label('direction',4.3,-.2,size=34),label('not scored',4.3,-.7,size=34),
        DashedLine([3.3,-1.45,0],[5.3,-1.45,0],color=GREY),label('?',4.3,-1.9,size=32))
    return g

def cord():
    outline=Ellipse(width=6.3,height=6.5,color=GREY,stroke_width=3)
    canal=Ellipse(width=.65,height=1.6,color=GREY).move_to([0,.7,0])
    zone=Ellipse(width=1.6,height=2.8,color=GREY,fill_color=GREY,fill_opacity=.15).move_to([0,.7,0])
    fp=RoundedRectangle(width=.95,height=.4,corner_radius=.06,color=GREY,
        fill_color=GREY,fill_opacity=.6).move_to([0,-2.92,0])
    neuron=Dot([-2.05,2,0],radius=.22,color=BLUE)
    pts=[[-2.05,2,0],[-2.65,.7,0],[-2.4,-1,0],[-1.3,-2.35,0],[0,-2.92,0],[.65,-2.92,0]]
    path=VMobject(color=BLUE,stroke_width=7).set_points_as_corners(pts)
    b=VGroup(outline,zone,canal,fp,neuron)
    tags=VGroup(label('dorsal cord',-4.55,2.6,BLUE,34),Line([-3.25,2.5,0],[-2.2,2.1,0],color=BLUE),
        label('commissural',-4.55,.5,BLUE,34),label('axon',-4.55,.05,BLUE,34),Line([-3.4,.1,0],[-2.6,-.15,0],color=BLUE),
        label('pial surface',-4.5,-2,TEXT,34),Line([-3.3,-1.9,0],[-2.6,-1.8,0],color=GREY),
        label('ventricular zone',4.65,1.85,size=34),Line([3.1,1.7,0],[.7,1.45,0],color=GREY),
        label('central canal',4.6,.5,size=34),Line([3.3,.4,0],[.32,.4,0],color=GREY),
        label('floor plate',1.9,-3.25,size=34),Line([.8,-3.2,0],[.45,-2.95,0],color=GREY))
    return b,path,tags

def tube(x,y=0):
    return VGroup(RoundedRectangle(width=.8,height=1.5,corner_radius=.15,color=GREY),
        Rectangle(width=.65,height=.5,stroke_width=0,fill_color=YELLOW,fill_opacity=.8).shift(DOWN*.4)).move_to([x,y,0])

def column(x,y=.35):
    return VGroup(Rectangle(width=.9,height=2.7,color=GREY,fill_color=GREY,fill_opacity=.2),
        Rectangle(width=.72,height=1.8,stroke_width=0,fill_color=GREY,fill_opacity=.45),
        Line([0,-1.35,0],[0,-1.65,0],color=GREY)).move_to([x,y,0])

def brain(pos,scale=1):
    # Dorsal-view schematic: separated hemispheres, midline, hindbrain and stalk.
    lobes=VGroup(*[Ellipse(width=.72,height=1.35,color=GREY,
        fill_color=GREY,fill_opacity=.4).move_to([x,.25,0]) for x in [-.43,.43]])
    midline=Line([0,-.3,0],[0,.95,0],color=TEXT,stroke_width=2)
    cerebellum=Ellipse(width=1.1,height=.42,color=GREY,fill_color=GREY,
        fill_opacity=.6).move_to([0,-.6,0])
    stalk=VMobject(color=GREY,stroke_width=3).set_points_as_corners(
        [[-.17,-.78,0],[-.13,-1.12,0],[.13,-1.12,0],[.17,-.78,0]])
    folds=VGroup(*[Line([-.4,y,0],[.4,y,0],color=TEXT,stroke_width=1.5)
        for y in [-.69,-.59,-.49]])
    return VGroup(lobes,midline,cerebellum,stalk,folds).scale(scale).move_to(pos)

def walker(x,y,color=BLUE,facing=-1):
    return VGroup(Circle(radius=.25,color=color).move_to([x,y+.85,0]),
        Dot([x+facing*.22,y+.86,0],radius=.06,color=TEXT),
        Line([x,y+.6,0],[x,y-.35,0],color=color,stroke_width=5),
        Line([x-.45,y-1.1,0],[x,y-.35,0],color=color,stroke_width=5),
        Line([x,y-.35,0],[x+.45,y-1.1,0],color=color,stroke_width=5),
        Line([x-.5,y+.15,0],[x+.5,y+.15,0],color=color,stroke_width=5))

def bakery():
    return VGroup(Rectangle(width=2.4,height=4,color=GREY,fill_color=GREY,fill_opacity=.15).move_to([4.5,.25,0]),
        label('BAKERY',4.5,2.65,size=30),Rectangle(width=.8,height=2,color=GREY).move_to([4.5,-.7,0]))

def scent():
    return VGroup(*[Arrow([3.1,y,0],[-5.3,y,0],color=YELLOW,buff=0,stroke_width=3) for y in [1.65,-.7]])

def diffusion():
    # Sample a truncated exponential concentration profile, not measured data.
    rng=np.random.default_rng(41);g=VGroup()
    for _ in range(130):
        distance=rng.exponential(1.65)
        if distance>6.5:continue
        x=3.1-distance;y=rng.uniform(-1.65,1.65)
        g.add(Dot([x,y,0],radius=.045,color=YELLOW).set_opacity(.8))
    return g

def steering_paths():
    # Constant-speed extension; delayed heading relaxation makes the turn visible.
    paths=VGroup()
    for y,angle in [(-.65,-.9),(-.23,-.45),(.23,.45),(.65,.9)]:
        q=np.array([-3.15,y]);h=np.array([np.cos(angle),np.sin(angle)])
        pts=[np.r_[q,0]]
        for step in range(165):
            aim=np.array([3.65,y*.25])-q;aim/=np.linalg.norm(aim)
            if step>=32:
                h=.965*h+.035*aim;h/=np.linalg.norm(h)
            q=q+.043*h;pts.append(np.r_[q,0])
            if q[0]>=2.8:break
        paths.add(VMobject(color=BLUE,stroke_width=6).set_points_smoothly(pts))
    return paths

class S00Title(TitleCard):
    TITLE='Something Crosses the Gel'
    LESSON=LESSON

class S01Question(SpokenScene):
    def construct(self):
        self.add(gel())
        self.at('A floor plate');self.play(FadeIn(explant([3.9,0,0],GREY)),FadeIn(label('floor plate',3.9,1.45,size=34)),run_time=.4)
        self.at('a piece of');self.play(FadeIn(explant([-3.9,0,0])),FadeIn(label('dorsal spinal cord',-3.6,1.45,BLUE,34)),run_time=.4)
        self.at('sit apart');self.play(Create(DashedLine([-2.8,0,0],[2.8,0,0],color=GREY)),FadeIn(label('?',0,.6,size=42)),run_time=.4)
        self.at('How could one');self.play(FadeIn(label('How could one steer the other?',size=34)),run_time=.4);self.finish()

class S02Map(SpokenScene):
    def construct(self):
        b,p,t=cord();self.add(b,t)
        self.at('Start on the map');self.play(Indicate(b[4],color=BLUE),run_time=.6)
        self.at('axons grow');self.play(Create(p),run_time=1)
        self.at('toward the floor');self.play(Indicate(p,color=BLUE),b[3].animate.set_fill(YELLOW,.9),run_time=.7);self.finish()

class S03Lab(SpokenScene):
    def construct(self):
        b,p,t=cord();self.add(b,p,t)
        title=label('1988 · Jessell laboratory',y=3.55)
        self.at('In');self.play(FadeOut(t),FadeIn(title),run_time=.4)
        cuts=VGroup(SurroundingRectangle(b[4],buff=.18,color=BLUE),SurroundingRectangle(b[3],buff=.12,color=GREY))
        self.at('and colleagues');self.play(Create(cuts),run_time=.4)
        self.at('tested this');self.play(FadeOut(cuts),FadeOut(p),FadeOut(b[0]),FadeOut(b[1]),FadeOut(b[2]),FadeIn(gel()),
            ReplacementTransform(b[4],explant([-3.9,0,0])),ReplacementTransform(b[3],explant([3.9,0,0],GREY)),run_time=1);self.finish()

class S04Explant(SpokenScene):
    def construct(self):
        self.add(gel(),label('1988 · Jessell laboratory'))
        a=explant([-3.9,1.5,0]);b=explant([3.9,1.5,0],GREY);self.add(a,b)
        cuts=VGroup(Line([-4.8,.5,0],[-3,2.4,0],color=TEXT),Line([3,.5,0],[4.8,2.4,0],color=TEXT))
        self.at('They cut pieces');self.play(Create(cuts),run_time=.4);self.play(FadeOut(cuts),a.animate.shift(DOWN*1.5),b.animate.shift(DOWN*1.5),run_time=.7)
        self.at('Each piece was');self.play(FadeIn(label('explant',0,1.3,size=36)),Create(Line([-1,1.2,0],[-3.1,.5,0],color=TEXT)),Create(Line([1,1.2,0],[3.1,.5,0],color=TEXT)),run_time=.4)
        self.at('living tissue');self.play(FadeIn(label('Living tissue cultured outside the embryo',0,-2.2,size=34)),run_time=.4);self.finish()

class S05Gel(SpokenScene):
    def construct(self):
        a=explant([-3.9,0,0]);b=explant([3.9,0,0],GREY);self.add(a,b)
        self.at('They set the explants');g=gel();g.set_z_index(-1);self.play(Create(g),run_time=.8)
        self.at('collagen gel');self.play(FadeIn(label('collagen gel')),run_time=.3)
        self.at('Some held');self.play(FadeIn(label('dorsal explant',-3.9,1.45,BLUE,34)),run_time=.3)
        self.at('others floor plate');self.play(FadeIn(label('floor plate explant',3.6,1.45,size=34)),run_time=.3);self.finish()

class S06Predict(SpokenScene):
    def construct(self):
        self.add(assay())
        self.at('First');self.play(FadeIn(label('Control',0,-2.35)),run_time=.3)
        self.at('What should it');self.play(FadeIn(label('Alone, what does it do?',size=34)),run_time=.3);self.finish()
class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(assay(question=True),label('Control',0,-2.35));self.wait(5)
class S08Reveal(SpokenScene):
    def construct(self):
        self.add(assay(control=True));self.at('On its own');self.finish()
class S09Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(assay(control=True));self.wait(2.5)
class S10Floorplate(SpokenScene):
    def construct(self):
        self.add(assay());g=assay(True)
        self.at('Now');self.play(FadeIn(g[3]),run_time=.4)
        self.at('explant nearby');self.play(FadeIn(g[4]),run_time=.3)
        self.at('Bundles of');self.play(Create(bundles()),run_time=2);self.finish()
class S11Apart(SpokenScene):
    def construct(self):
        self.add(assay(True,True))
        bracket=VGroup(Line([-3,-1.6,0],[3,-1.6,0],color=TEXT),Line([-3,-1.4,0],[-3,-1.8,0],color=TEXT),Line([3,-1.4,0],[3,-1.8,0],color=TEXT))
        self.at('never touched');self.play(Create(bracket),FadeIn(label('No contact',0,-2.25,size=34)),run_time=.4)
        self.at('the effect');self.play(FadeIn(label('Something crosses the gel',size=34)),run_time=.3);self.finish()
class S12Chemo(SpokenScene):
    def construct(self):
        stage=assay(True);stage[2].set_y(2.35);stage[4].set_y(2.35);self.add(stage);dots=diffusion()
        self.at('A cue that');self.play(LaggedStart(*[FadeIn(d,shift=np.array([3.8,0,0])-d.get_center()) for d in dots],lag_ratio=.015),run_time=1.5)
        title=label('chemoattractant',c=YELLOW,size=36)
        self.at('is a');self.play(FadeIn(title),run_time=.3)
        self.at('Steering by');paths=steering_paths();self.play(Create(paths),run_time=1.1)
        self.at('cue is');self.play(Transform(title,label('chemotropism',c=GREEN,size=36)),Indicate(paths,color=BLUE),run_time=.7);self.finish()
class S13Bread(SpokenScene):
    def construct(self):
        w=walker(-3.5,-.5);smell=scent();self.add(bakery(),w,smell,Line([-6,-1.7,0],[6,-1.7,0],color=GREY))
        self.at('Picture smelling');self.play(smell.animate.shift(LEFT*.1),run_time=.4)
        self.at('You know which');self.play(Transform(w,walker(-3.5,-.5,facing=1)),run_time=.4);self.play(w.animate.shift(RIGHT*2.8),run_time=1.25)
        card=VGroup(Rectangle(width=1.5,height=1.3,color=TEXT).move_to([-5,.4,0]),label('recipe?',-5,1.3,size=34))
        self.at('but not the');self.play(FadeIn(card),run_time=.3);self.finish()
class S14Unlike(SpokenScene):
    def construct(self):
        w=walker(-1.5,-.5,BLUE,1);v=walker(-3,-.5,RED,-1)
        attracted=label('attracted',-1.5,-2.3,GREEN,34)
        repelled=label('repelled',-3,-3.1,RED,34)
        self.add(bakery(),scent(),w,v,attracted,repelled,
            Line([-6,-1.7,0],[6,-1.7,0],color=GREY))
        self.at('Unlike bread');self.play(FadeIn(label('Same cue · different responses',size=34)),run_time=.3)
        self.at('whether netrin');self.play(w.animate.shift(RIGHT*2.5),v.animate.shift(LEFT*1.8),
            attracted.animate.shift(RIGHT*2.5),repelled.animate.shift(LEFT*1.8),run_time=2.4,rate_func=linear);self.finish()
class S15Tiny(SpokenScene):
    def construct(self):
        p=explant([-3.5,0,0],GREY).scale(.14)
        t=tube(2.3,0).scale(3.1);t[1].set_opacity(0)
        scale=VGroup(Line([-4.05,-.65,0],[-2.95,-.65,0],color=TEXT),
            *[Line([x,-.53,0],[x,-.77,0],color=TEXT) for x in [-4.05,-2.95]])
        self.add(p,t,scale,label('floor plate',-3.5,.9,size=34),
            label('schematic scale',-3.5,-1.2,size=32),
            label('amount needed',2.3,-2.7,size=34),label('to purify',2.3,-3.25,size=34))
        warning=VGroup(label('Too little tissue',-3.5,-2.4,size=34),
            label('to purify from',-3.5,-2.95,size=34));self.add(warning)
        self.at('To name the molecule');self.play(FadeIn(label('Purify the cue',c=YELLOW,size=38)),run_time=.3)
        self.at('Floor plates are');self.play(Indicate(p,scale_factor=1.8),run_time=.5)
        self.at('far too small');self.play(Indicate(warning,color=TEXT),run_time=.5);self.finish()
class S16Chick(SpokenScene):
    def construct(self):
        rats=VGroup(*[explant([x,0,0]).scale(1.65) for x in [-4.7,-1.9]])
        brains=VGroup(*[brain([x,0,0],1.65) for x in [1.7,4.6]])
        self.add(rats,brains,label('1994',size=40),
            label('rat explants',-3.3,2,BLUE,34),
            label('embryonic chick brains',3.1,2,size=34),
            label('detector',-3.3,-2.6,BLUE,36),label('source',3.1,-2.6,size=36))
        self.at('kept rat explants');self.play(Indicate(rats,color=BLUE),run_time=.5)
        self.at('as the detector');self.play(Indicate(rats,color=BLUE),run_time=.3)
        self.at('searched embryonic');self.play(Indicate(brains,color=TEXT),run_time=.5);self.finish()
class S17Columns(SpokenScene):
    def construct(self):
        brains=VGroup(*[brain([x,y,0],1) for x in [-3.6,0,3.6] for y in [-1.5,1.1]])
        title=label('Embryonic chick brains × thousands',size=32);self.add(brains,title)
        self.at('Thousands of brains');self.play(Indicate(brains),run_time=.5)
        extract=chip('membrane extract',YELLOW,34).move_to([-4.4,1.8,0])
        self.at('The extract');self.play(ReplacementTransform(brains,extract),Transform(title,label('Purify by chromatography',size=32)),run_time=.5)
        cols=VGroup(*[column(x).scale(1.35) for x in [-1.4,1.5,4.4]])
        self.at('separated over');self.play(FadeIn(cols),run_time=.5)
        arrows=VGroup(Arrow([-3.3,1,0],[-2,1,0],color=YELLOW,buff=.05),*[Arrow([x+.6,.5,0],[x+2.25,.5,0],color=YELLOW,buff=.05) for x in [-1.4,1.5]])
        ts=VGroup(*[tube(x,-2.65).scale(.9) for x in [-1.4,1.5,4.4]])
        self.at('several');self.play(Create(arrows),FadeIn(ts),run_time=.5)
        drops=VGroup(*[Dot([x,-1.25,0],radius=.1,color=YELLOW) for x in [-1.4,1.5,4.4]])
        self.play(FadeIn(drops),run_time=.15);self.play(drops.animate.shift(DOWN*.65),run_time=.4);self.finish()
class S18Fractions(SpokenScene):
    def construct(self):
        xs=[-4.6,-1.4,1.8];ts=VGroup(*[tube(x,1.7).scale(1.2) for x in xs]);es=VGroup(*[explant([x,-.9,0]).scale(.95) for x in xs])
        self.add(ts,label('Test every fraction',size=34))
        self.at('every fraction');self.play(FadeIn(es),run_time=.4)
        arrows=VGroup(*[Arrow([x,.8,0],[x,-.2,0],color=YELLOW,buff=.05) for x in xs])
        self.at('went back onto');self.play(Create(arrows),run_time=.4)
        out=radial([-1.4,-.9,0],1.5,half_size=(.7125,.855))
        self.at('The axons reported');self.play(Create(out),FadeIn(label('×',-4.6,-2.7,RED,36)),FadeIn(label('×',1.8,-2.7,RED,36)),run_time=.5)
        self.at('which fractions');self.play(FadeIn(label('✓ keep',-1.4,-2.7,GREEN,32)),FadeIn(column(4.8,.4).scale(1.35)),FadeIn(label('next column',4.8,-2.4,size=34)),run_time=.3)
        self.play(ts[1].animate.move_to([4.8,2.9,0]).scale(.55),run_time=.7);self.finish()
class S19Two(SpokenScene):
    def construct(self):
        title=label('Two purified proteins',y=3.55,size=34)
        lanes=VGroup(*[Rectangle(width=3.5,height=4.6,color=GREY,fill_color=GREY,fill_opacity=.08).move_to([x,.3,0]) for x in [-2,2]])
        bands=VGroup(*[Rectangle(width=3,height=.4,color=YELLOW,fill_color=YELLOW,fill_opacity=.8).move_to([x,y,0]) for x,y in [(-2,1),(2,-.2)]])
        names=VGroup(label('protein 1',-2,2.9,YELLOW,34),label('protein 2',2,2.9,YELLOW,34));self.add(title,lanes,bands,names)
        self.at('Their sequences');self.play(FadeOut(lanes),FadeOut(bands),FadeOut(names),Transform(title,label('Related sequences · schematic',size=32)),run_time=.4)
        seq=VGroup(*[VGroup(label(name,-4.5,y,c,34),Rectangle(width=5.6,height=.44,color=c,fill_color=c,fill_opacity=.65).move_to([1,y,0])) for name,y,c in [('protein 1',1.9,YELLOW),('protein 2',.8,YELLOW)]])
        self.play(FadeIn(seq),run_time=.3)
        self.at('related to laminin');self.play(FadeIn(label('laminin',-4.5,-.65,size=34)),FadeIn(Rectangle(width=5.6,height=.44,color=GREY,fill_color=GREY,fill_opacity=.5).move_to([1,-.65,0])),run_time=.4)
        self.at('a matrix protein');self.play(FadeIn(label('matrix protein',0,-1.3,size=34)),run_time=.3)
        self.at('a worm protein');self.play(FadeIn(label('worm UNC-6',-4.5,-2.2,size=34)),FadeIn(Rectangle(width=5.6,height=.44,color=GREY,fill_color=GREY,fill_opacity=.5).move_to([1,-2.2,0])),run_time=.4);self.finish()
class S20Named(SpokenScene):
    def construct(self):
        es=VGroup(*[explant([x,-.25,0]).scale(1.45) for x in [-3.2,3.2]])
        self.add(es,label('Purified proteins → explant assay',size=36))
        a=chip('netrin-1',YELLOW,36).move_to([-3.2,2.2,0])
        b=chip('netrin-2',YELLOW,36).move_to([3.2,2.2,0])
        # Four bundled processes per explant; radial geometry implies outgrowth only.
        paths=[VGroup(*[Line([x+dx,-1.5,0],[x+dx*1.8,-2.6,0],
            color=BLUE,stroke_width=7) for dx in [-.75,-.25,.25,.75]]) for x in [-3.2,3.2]]
        self.at('The authors named');self.play(FadeIn(a),Create(paths[0]),run_time=.7)
        self.at('and');self.play(FadeIn(b),Create(paths[1]),run_time=.7)
        self.at('Each promoted');self.play(Indicate(paths[0],color=BLUE),Indicate(paths[1],color=BLUE),
            FadeIn(label('commissural outgrowth',0,-3.25,BLUE,36)),run_time=.9);self.finish()
class S21Predict2(SpokenScene):
    def construct(self):
        self.add(explant(ORIGIN).scale(1.5))
        self.at('Does promoting outgrowth');self.play(Create(radial(r=2.95,half_size=(1.125,1.35))),run_time=.8)
        self.at('prove that');self.play(FadeIn(label('Growth, or steering?',size=34)),run_time=.3)
        self.at('Think about what');self.play(FadeIn(label('Assay scored: outgrowth yes or no',0,-3.4,size=34)),run_time=.3);self.finish()
class S22Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(radial_stage(question=True));self.wait(5)
class S23Reveal2(SpokenScene):
    def construct(self):
        stage=radial_stage().shift(LEFT*1.4);self.add(stage)
        self.at('the assay scored');self.play(FadeIn(scorecard(second=False)),run_time=.4)
        self.at('not which way');self.play(FadeIn(scorecard(first=False)),run_time=.4)
        self.at('Outgrowth is not');self.play(FadeIn(label('Outgrowth is not direction',size=34)),run_time=.3);self.finish()
class S24Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(radial_stage(answer=True));self.wait(2.5)
class S25Companion(SpokenScene):
    def construct(self):
        b,p,t=cord()
        # Expand anatomy horizontally into the former side bands; retain large type.
        for obj in [b,p]:obj.stretch(1.25,0)
        for i in [1,6,8,10,12]:
            end=t[i].get_end().copy();end[0]*=1.25
            t[i].put_start_and_end_on(t[i].get_start(),end)
        t.remove(t[2],t[3],t[4])  # No axon label without its path.
        p.set_stroke(opacity=.35);self.add(b,p,t)
        glow=VGroup(*[RoundedRectangle(width=1.2+r,height=.5+r,corner_radius=.15,
            stroke_width=0,fill_color=YELLOW,fill_opacity=.04).move_to(b[3])
            for r in np.linspace(.15,1.05,9)])
        self.at('Floor plate cells');self.play(FadeIn(glow),b[3].animate.set_color(YELLOW).set_fill(YELLOW,.9),run_time=.4)
        dots=VGroup(*[Dot([x,-2.92,0],radius=.09,color=YELLOW) for x in [-.4,0,.4]])
        self.at('make');self.play(FadeIn(dots),FadeIn(label('netrin-1 RNA',0,-1.8,YELLOW,34)),Create(Line([0,-2.1,0],[0,-2.65,0],color=YELLOW)),run_time=.4);self.finish()
class S26Secrete(SpokenScene):
    def construct(self):
        stage=assay();stage[2].set_y(2.35);self.add(stage);cells=VGroup(*[Circle(radius=.7,color=GREY,fill_color=GREY,fill_opacity=.4).move_to([3.9+dx,dy,0]) for dx,dy in [(-.45,0),(.4,.65),(.4,-.65)]])
        self.at('cells engineered');self.play(FadeIn(cells),run_time=.4)
        dots=diffusion()
        self.at('to secrete netrin');self.play(FadeIn(label('netrin-secreting cells',3.5,2.35,YELLOW,34)),LaggedStart(*[FadeIn(d,shift=np.array([3.9,0,0])-d.get_center()) for d in dots],lag_ratio=.008),run_time=.9)
        self.at('attracted commissural');self.play(Create(steering_paths()),run_time=1.5)
        self.at('at a distance');self.play(FadeIn(label('Attraction at a distance',0,-2.7,GREEN,32)),run_time=.3);self.finish()
class S27Takeaway(SpokenScene):
    def construct(self):
        b,p,t=cord();self.add(b,p,t,label('Can attract at a distance',0,3.48,TEXT,32))
        self.at('netrin is what');self.play(FadeIn(chip('netrin',YELLOW,32).move_to([4.6,-1.2,0])),run_time=.4);self.finish()
class S28End(EndCard):
    LINE='Netrin can cross the gel and attract at a distance.'
