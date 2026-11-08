"""Chapter 1, reviewer polish round.
COLOR MAP: BLUE = retinal axons / EphA; ORANGE = ephrin-A repellent;
YELLOW = lure / comparison; RED = cut / missed prey; GREY = anatomy;
GOLD = temporal identity; slate = nasal identity. Opaque cyan, gold,
slate, mint and lavender identify individual axons (not receptor amounts).
Gradient amount is computed as 0.08 + 0.82*f, as in scenes.old.py.
Rank positions are computed by sorting receptor levels, not traced by hand.
"""
import numpy as np
from bp_style import *
from bp_style import SpokenScene as BaseSpokenScene
ORANGE = '#F29E4C'
SLATE = '#BAC6DB'
IDS = [GOLD, BLUE, '#9CE0BB', '#C8B5F2', SLATE]
LESSON = "Topographic Maps: Sperry's Eye and Eph Gradients"

class SpokenScene(BaseSpokenScene):
    # The old log recorded lateness BEFORE waiting. Audit AFTER waiting instead,
    # without modifying sync.log (the fix task restricts output files).
    def at(self, phrase, lead=0, nth=0):
        target = self.t_of(phrase, nth) - lead
        rest = target - self.elapsed()
        if rest > .02:
            self.wait(rest)
        error = self.elapsed() - target
        assert abs(error) < .14, (phrase, target, self.elapsed())
        print(f'CUE {self.__class__.__name__}: {phrase!r}, error={error:+.3f}s')

def label(s,x,y,size=28,color=TEXT):
    return T(s,size,color).move_to([x,y,0])

def line(a,b,c=BLUE,w=5):
    return Line(a,b,color=c,stroke_width=w)

def cell(x,y,c=BLUE,r=.16):
    # Opaque dark underlay prevents loss against a bright gradient.
    return VGroup(Circle(radius=r+.055,stroke_width=0,fill_color=BG,fill_opacity=1),
        Circle(radius=r,stroke_color=c,stroke_width=3,fill_color=c,fill_opacity=1)).move_to([x,y,0])

def gradient(x,y,length=8,height=1.3,color=ORANGE,vertical=False):
    g=VGroup()
    for i in range(48):
        f=i/47
        g.add(Rectangle(width=height if vertical else length/48+.008,
            height=length/48+.008 if vertical else height,stroke_width=0,
            fill_color=color,fill_opacity=.08+.82*f).move_to([
                x if vertical else x-length/2+length*(i+.5)/48,
                y+length/2-length*(i+.5)/48 if vertical else y,0]))
    g.add(Rectangle(width=height if vertical else length,height=length if vertical else height,
        stroke_color=color,stroke_width=2).move_to([x,y,0]))
    return g

def tuft(x,y,c=BLUE):
    segs=[([x,y+.42,0],[x+dx,y+dy,0]) for dx,dy in [(-.25,-.18),(0,-.36),(.25,-.18)]]
    return VGroup(*[line(a,b,BG,10) for a,b in segs],*[line(a,b,c,5) for a,b in segs])

def newt(rotated=True):
    body=Ellipse(width=6.2,height=2.1,stroke_color=GREY,fill_color=GREY,fill_opacity=.4).move_to([.6,-.3,0])
    tail=Polygon([3,-.1,0],[6,-1.1,0],[2.9,-1.05,0],color=GREY,fill_opacity=.4)
    legs=VGroup()
    for x,dx,y in [(-.9,-.7,-2.1),(-.9,.45,1.4),(2,.8,-2.1),(2,-.35,1.4)]:
        knee=np.array([x+dx,-.3+(y+.3)*.65,0]); end=np.array([x+dx*1.35,y,0])
        legs.add(VMobject(stroke_color=GREY,stroke_width=14).set_points_as_corners([[x,-.3,0],knee,end]))
        for d in [-.18,0,.18]:
            legs.add(line(end,end+np.array([d,.22 if y>0 else -.22,0]),GREY,5))
    spots=VGroup(*[Dot([x,-.1,0],radius=.12,color=RED) for x in [-.8,.2,1.2,2.2]])
    eye=VGroup(Circle(radius=.36,color=TEXT,fill_color=TEXT,fill_opacity=1),
        line([0,0,0],[0,.27,0],BG,8)).move_to([-3.65,.43,0])
    if rotated: eye.rotate(PI)
    head=VGroup(Ellipse(width=2.9,height=1.9,stroke_color=GREY,fill_color=GREY,fill_opacity=.55).move_to([-3.1,-.05,0]),eye,
        line([-4.35,-.35,0],[-3.5,-.35,0],GREY,3))
    return VGroup(tail,legs,body,spots,head)

PIVOT=np.array([-1.9,-.05,0])
def lure():
    return VGroup(line([-3.65,2.75,0],[-3.65,2.05,0],YELLOW,3),
        Ellipse(width=.55,height=.23,color=YELLOW,fill_opacity=1).move_to([-3.65,1.95,0]))

def wrong():
    return VGroup(CurvedArrow([-4.65,.25,0],[-3.4,-1.9,0],angle=1.1,color=RED),
        label('miss',-4.6,-2.45,28,RED),
        line([-3.55,-2,0],[-3.15,-2.4,0],RED,6),line([-3.55,-2.4,0],[-3.15,-2,0],RED,6))

def calendar(week):
    return VGroup(RoundedRectangle(width=1.9,height=1.55,corner_radius=.12,color=SLATE),
        label('WEEK',0,.4,26,SLATE),label(str(week),0,-.25,42)).move_to([4.9,1.95,0])

def experiment(week=3,down=False):
    n=newt()
    if down: n[-1].rotate(.85,about_point=PIVOT)
    return VGroup(n,lure(),calendar(week),wrong() if down else VGroup())

def strike(scene,n,c,week,keep=False):
    miss=wrong()
    # Replace the entire counter atomically: morphing numeral glyphs left debris.
    scene.remove(c)
    c.become(calendar(week))
    scene.add(c)
    scene.play(Rotate(n[-1],.85,about_point=PIVOT),FadeIn(miss),run_time=.25)
    scene.wait(.42)
    if not keep:
        scene.play(Rotate(n[-1],-.85,about_point=PIVOT),FadeOut(miss),run_time=.22)

def map_base(grad=False):
    r=gradient(-5,0,4.4,.7,BLUE,True) if grad else RoundedRectangle(width=.7,height=4.4,corner_radius=.1,color=GREY).move_to([-5,0,0])
    t=gradient(1.3,-2,8.8,1.25) if grad else RoundedRectangle(width=8.8,height=1.25,corner_radius=.1,color=GREY).move_to([1.3,-2,0])
    names=VGroup(label('retina',-5,2.85),label('sending side',-5,2.42,26,SLATE),
        label('nasal',-6.1,1.8,26,SLATE),label('temporal',-5,-2.65,26,GOLD),
        label('target',1.3,-3.35,28),label('anterior / front',-1.65,-2.95,26,SLATE),
        label('posterior / back',4.25,-2.95,26,SLATE))
    return VGroup(r,t,names)

def fibre(i,branch=False):
    f=i/4; y=-1.65+3.3*f; x=-2.35+7.3*f; c=IDS[i]
    path=VMobject(stroke_color=c,stroke_width=4).set_points_as_corners([[-4.6,y,0],[x,-.9,0],[x,-1.58 if branch else -2,0]])
    return VGroup(path,cell(-5,y,c),tuft(x,-2,c) if branch else cell(x,-2,c))

def map_fibres(branch=False):
    return VGroup(*[fibre(i,branch) for i in range(5)])

def molecule_labels():
    return VGroup(label('EphA: receptor',-2,2.6,28,BLUE),label('ephrin-A: repellent',1.9,.65,28,ORANGE),
        label('brighter = more',2.5,2.6,26,SLATE),
        label('low',-5.9,1.1,26,BLUE),label('high',-5.9,-1.3,26,BLUE),
        label('low',-2.4,-.4,26,ORANGE),label('high',4.95,-.4,26,ORANGE))

QUESTION='How does an axon know where to stop?'
def panels(stage=0):
    g=VGroup()
    for i in range(3):
        x=-4.35+i*4.35; c=[BLUE,ORANGE,YELLOW][i]
        p=VGroup(RoundedRectangle(width=4.05,height=4.7,corner_radius=.15,color=GREY).move_to([x,.1,0]),
            label(f'{i+1}. '+['Labels','Gradients','Neighbours'][i],x,2,28,c))
        if stage>=i+1:
            if i==0:
                p.add(label('cell    target site',x,1.15,26,SLATE))
                for j in range(3):
                    yy=.4-j*.8
                    p.add(chip(str(j+1),BLUE,26).move_to([x-1.05,yy,0]),
                        Arrow([x-.52,yy,0],[x+.5,yy,0],color=BLUE,buff=.05),
                        chip(str(j+1),BLUE,26).move_to([x+1.05,yy,0]))
                p.add(label('one tag ↔ one site',x,-1.95,26,SLATE))
            elif i==1:
                p.add(label('amount of a',x,1.15,26),label('molecule',x,.7,26),gradient(x,-.15,3.35,.95),
                    label('low',x-1.1,-.95,26,ORANGE),label('high',x+1.1,-.95,26,ORANGE))
                for f in [0,.5,1]:
                    xx=x-1.5+3*f
                    p.add(line([xx,-1.25,0],[xx,-1.4,0],SLATE,2),label(str(f).rstrip('0').rstrip('.') if f else '0',xx,-1.65,26))
                p.add(label('position → value',x,-1.95,26,SLATE))
            else:
                p.add(label('other retinal axons',x,1.15,26),label('arriving in the target',x,.7,26))
                for j in range(3):
                    xx=x-1.05+j*1.05; yy=-.25-j*.5
                    p.add(line([xx,-1.5,0],[xx,yy,0],YELLOW,5),tuft(xx,yy,YELLOW))
                p.add(label('relative positions',x,-1.95,26,SLATE))
        g.add(p)
    return g


def reveal_panel(scene,p,i,stage,duration=.65):
    # Keep the border and heading stable; never morph text into new diagram parts.
    content=VGroup(*panels(stage)[i][2:])
    scene.play(FadeIn(content),run_time=duration)
    scene.remove(content)
    p[i].add(*content)

# Rank model: descending receptor amount occupies successive low-to-high ligand slots.
LEVELS=np.array([1,.75,.5,.3,.15])
ORDER=np.argsort(-LEVELS)
RANK=np.argsort(ORDER)
SLOTS=np.linspace(-1.7,5.2,5)
def rank_token(i,x,y):
    return VGroup(cell(x,y,IDS[i]),line([x+.35,y,0],[x+.35+LEVELS[i]*1.5,y,0],BLUE,9))

def rank_base():
    return VGroup(label('Rank the axons by EphA level',0,3.05,34),
        label('most',-5.55,1.95,26,BLUE),label('least',-5.55,-1.4,26,BLUE),
        gradient(1.75,-2.25,8.4,1.15),
        VGroup(*[Rectangle(width=.8,height=.9,stroke_color=SLATE,stroke_width=1,stroke_opacity=.5).move_to([x,-2.25,0]) for x in SLOTS]),
        label('low repellent / front',-.7,-3.1,26,ORANGE),
        label('high / back',4.7,-3.1,26,ORANGE),
        label('Coarse map • chick and mouse • simplified model',0,-3.6,26,SLATE))

def rank_result():
    b=rank_base()
    tokens=VGroup(*[rank_token(i,-4.7,1.8-.78*int(RANK[i])) for i in range(5)])
    tips=VGroup(*[tuft(SLOTS[int(RANK[i])],-2.25,IDS[i]) for i in range(5)])
    return VGroup(b,tokens,tips,label('place = rank among axons, against the slope',1.1,.55,28,YELLOW))

class S00Title(TitleCard):
    LESSON=LESSON
    TITLE='A Rank Against a Slope'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2,26,TEAL),
            label('Topographic Maps: Sperry’s Eye and Eph Gradients',0,1.2,28,SLATE),
            label(self.TITLE,0,-.1,48),line([-1.2,-.9,0],[1.2,-.9,0],GOLD))
        self.wait(3)

def anatomy():
    # 4.7 units tall: roughly 60% of the frame, shared across both views.
    n=newt(False).stretch(1.27,1).shift(DOWN*.25)
    eye=n[-1][1].get_center()
    brain=cell(-1.8,.05,SLATE,.24)
    nerve=line(eye+RIGHT*.32,brain.get_center(),BLUE,8)
    return n,brain,nerve

class S01Question(SpokenScene):
    def construct(self):
        n,brain,nerve=anatomy()
        question=label('Why does it never learn to aim again?',0,3.25,34)
        self.add(n,brain,nerve,question,label('eye',-5.55,1.5,28),
            line([-5,1.2,0],n[-1][1].get_center(),TEXT,2),
            label('brain',-1.3,1.5,28),line([-1.4,1.2,0],brain.get_center(),TEXT,2))
        self.at('upside down')
        arrow=CurvedArrow([-4.3,.6,0],[-3,.6,0],angle=-PI,color=YELLOW)
        self.play(Create(arrow),Rotate(n[-1][1],PI),run_time=.7)
        self.at('let its nerve regrow')
        self.remove(nerve)
        self.play(Create(nerve),run_time=.9)
        self.at('Why does it'); self.play(Indicate(question,scale_factor=1.03),run_time=.4)
        self.finish()

class S02Sperry(SpokenScene):
    def construct(self):
        n,brain,nerve=anatomy()
        self.add(n,brain,nerve,label('Sperry, 1943',0,3.25,36),label('eye',-5.55,1.5,28),
            line([-5,1.2,0],n[-1][1].get_center(),TEXT,2),label('brain',-1.3,1.5,28),
            line([-1.4,1.2,0],brain.get_center(),TEXT,2))
        self.at('rotated the eyes')
        a=CurvedArrow([-4.3,.6,0],[-3,.6,0],angle=-PI,color=YELLOW)
        self.play(Create(a),Rotate(n[-1][1],PI),FadeIn(label('180°',-3.65,-1.5,28,YELLOW)),run_time=1)
        self.at('He cut')
        cut=VGroup(line([-2.8,.6,0],[-2.45,-.2,0],RED,6),line([-2.8,-.2,0],[-2.45,.6,0],RED,6))
        txt=label('optic nerve cut',-.6,-.85,28,RED)
        # Retain the two stumps so the nerve remains anatomically anchored.
        stumps=VGroup(line(nerve.get_start(),[-2.95,.18,0],BLUE,8),
            line([-2.3,.1,0],nerve.get_end(),BLUE,8))
        self.remove(nerve); self.add(stumps)
        self.play(Create(cut),FadeIn(txt),run_time=.35)
        self.at('let it regrow')
        self.remove(txt)
        self.play(FadeOut(cut),FadeIn(label('optic nerve regrows',-.3,-.85,28,BLUE)),
            Create(nerve),run_time=1.1)
        self.finish()

class S03Lure(SpokenScene):
    def construct(self):
        n=newt(); self.add(n,label('Sperry, 1943',2.5,3.15,30,SLATE))
        self.at('a lure held'); self.play(FadeIn(lure()),FadeIn(label('lure',-2.1,2.15,28,YELLOW)),run_time=.4)
        self.at('turn its head'); self.play(Rotate(n[-1],.85,about_point=PIVOT),FadeIn(wrong()),run_time=.65)
        self.finish()

class S04Predict(SpokenScene):
    def construct(self):
        n=newt(); c=calendar(0)
        self.add(n,lure(),c,label('Random wiring, matched by use?',0,3.25,34))
        self.at('If the'); strike(self,n,c,1)
        self.at('at random'); strike(self,n,c,2)
        self.at('then'); strike(self,n,c,3)
        self.at('weeks of missed prey'); strike(self,n,c,4,keep=True)
        self.finish()

class S05Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(experiment(4,True),label('Pause: what should missed prey teach?',0,3.25,32))
        for i in range(5,0,-1):
            t=VGroup(label('reveal in',4.9,.6,26,YELLOW),label(str(i),4.9,-.1,38,YELLOW)); self.add(t); self.wait(1); self.remove(t)

class S06Reveal(SpokenScene):
    def construct(self):
        n=newt(); c=calendar(4); self.add(n,lure(),c)
        self.at('To aim correctly'); prompt=label('Would practice correct its aim?',0,3.25,34); self.add(prompt)
        self.at('it never learned')
        answer=label('The newt never learned to aim correctly',0,3.25,32,TEXT)
        self.play(ReplacementTransform(prompt,answer),FadeIn(label('Never corrected',1.3,-2.95,36,RED)),run_time=.4)
        self.at('It kept making'); strike(self,n,c,5)
        self.at('as long as'); strike(self,n,c,6,keep=True)
        self.finish()

class S07Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(experiment(6,True),label('Never corrected',1,-2.95,36,RED),label('Same wrong turn, week after week',0,3.25,34))
        for i in [2,1]:
            t=VGroup(label('next in',4.9,.6,26,YELLOW),label(str(i),4.9,-.1,38,YELLOW))
            self.add(t); self.wait(1); self.remove(t)

class S08Reading(SpokenScene):
    def construct(self):
        eye=Circle(radius=2.1,color=GREY,fill_color=GREY,fill_opacity=.15).move_to([-4.1,0,0])
        cols=[GOLD,BLUE,'#C8B5F2']; ys=[-1.4,0,1.4]
        self.add(eye,label('rotated eye',-4.1,2.85,32),label('original brain sites',3.9,2.85,32),
            RoundedRectangle(width=.8,height=4.6,corner_radius=.1,color=GREY).move_to([4.4,0,0]),
            Arrow([-5.5,1,0],[-5.5,-1,0],color=YELLOW,buff=0),label('original up ↓',-4,-2.9,28,YELLOW),
            label('Fibres return to matching sites',1,-3.5,28,SLATE))
        dots=VGroup(*[cell(-3.25,y,c) for y,c in zip(ys,cols)])
        sites=VGroup(*[cell(4.4,-y,c) for y,c in zip(ys,cols)])
        self.add(dots,sites)
        self.at('Each regrown fiber')
        paths=VGroup(*[line([-3,y,0],[4.15,-y,0],c,5) for y,c in zip(ys,cols)])
        self.play(LaggedStart(*[Create(p) for p in paths],lag_ratio=.15),run_time=1.35)
        self.at('its old place'); self.play(Indicate(sites,scale_factor=1.08),run_time=.5)
        self.finish()

class S09Map(SpokenScene):
    def construct(self):
        self.add(map_base(),label('An ordered map',0,3.45,34),
            label('optic tectum: fish, amphibians, birds',1.1,2.05,26,SLATE),
            label('superior colliculus: mammals',1.1,1.5,26,SLATE))
        self.at('Neighboring cells'); self.play(LaggedStart(*[Create(f) for f in map_fibres()],lag_ratio=.12),run_time=1.8)
        self.at('neighboring places'); self.play(Indicate(self.mobjects[0][1],scale_factor=1.02),run_time=.4)
        self.finish()

class S10Axis(SpokenScene):
    def construct(self):
        f=map_fibres(); self.add(map_base(),f)
        self.at('Temporal retina'); a=label('temporal → anterior',1,2.7,32,GOLD)
        self.play(FadeIn(a),Indicate(f[0],color=GOLD),run_time=.6)
        self.at('maps to the front'); self.play(Indicate(f[0][-1],color=GOLD),run_time=.5)
        self.at('Nasal retina')
        self.play(FadeOut(a),f[0][0].animate.set_stroke(opacity=.3),
            f[0][1].animate.set_opacity(.3),f[0][2].animate.set_opacity(.3),
            FadeIn(label('nasal → posterior',1,2.7,32,SLATE)),
            f[4].animate.set_color(SLATE).set_stroke(width=7),run_time=.5)
        self.at('maps to the back'); self.play(Indicate(f[4][-1],color=SLATE),run_time=.4)
        self.finish()

def growth_cone():
    fan=VMobject(stroke_color=BLUE,fill_color=BLUE,fill_opacity=.45,stroke_width=4)
    fan.set_points_smoothly([[-.7,0,0],[.2,.75,0],[1,.9,0],[1.35,.35,0],[1.3,-.4,0],[.8,-.85,0],[0,-.55,0],[-.7,0,0]])
    fingers=VGroup(*[line(a,b,BLUE,5) for a,b in [([.2,.7,0],[.3,1.3,0]),([.9,.85,0],[1.35,1.35,0]),([1.3,.35,0],[1.95,.6,0]),([1.25,-.3,0],[1.95,-.5,0]),([.8,-.8,0],[1.2,-1.35,0])]])
    return VGroup(line([-5,0,0],[-.7,0,0],BLUE,10),fan,fingers)

class S11Growthcone(SpokenScene):
    def construct(self):
        cone=growth_cone(); title=label('growth cone',.6,2.2,34,BLUE)
        self.add(cone,title,label('axon',-3.5,.65,28,BLUE))
        self.at('the moving tip'); self.play(cone.animate.shift(RIGHT*.35),run_time=.5)
        self.at('senses only what is close')
        ring=DashedVMobject(Circle(radius=1.9,color=YELLOW)).move_to([.85,0,0])
        reach=label('local reach',1,-2.5,30,YELLOW)
        self.play(Create(ring),FadeIn(reach),run_time=.6)
        self.at('Yet the map')
        self.play(VGroup(cone,ring).animate.scale(.5).move_to([-.6,.2,0]),Transform(title,label('growth cone',1.35,1.55,30,BLUE)),FadeOut(reach),
            FadeIn(gradient(1,-2.1,10,1.25)),FadeIn(label('retina',-5,2.1,30)),
            FadeIn(RoundedRectangle(width=.7,height=3.1,corner_radius=.1,color=GREY).move_to([-5,.2,0])),run_time=.65)
        self.add(line([-4.65,.2,0],cone[0].get_start(),BLUE,5),
            cell(-5,.2,BLUE),label('local reach',1.35,-1.05,26,YELLOW),
            label('whole target, front to back →',1,-3.2,30))
        self.finish()

class S12Three(SpokenScene):
    def construct(self):
        p=panels(1); self.add(label(QUESTION,0,3.15,34))
        self.at('Three ways'); self.play(FadeIn(p),run_time=.6)
        self.finish()

class S13Labels(SpokenScene):
    def construct(self):
        p=panels(1); self.add(p,label(QUESTION,0,3.15,34))
        self.at('Labels'); self.play(Indicate(p[0][1],scale_factor=1.05),run_time=.5)
        self.at('one matching tag'); self.play(Indicate(VGroup(*p[0][3:]),scale_factor=1.02),run_time=.7)
        self.finish()

class S14Gradients(SpokenScene):
    def construct(self):
        p=panels(1); self.add(p,label(QUESTION,0,3.15,34))
        self.at('Gradients'); reveal_panel(self,p,1,2)
        self.at('gives each position'); self.play(Indicate(VGroup(*p[1][-7:]),scale_factor=1.02),run_time=.6)
        self.finish()

class S15Neighbours(SpokenScene):
    def construct(self):
        p=panels(2); self.add(p,label(QUESTION,0,3.15,34))
        self.at('Neighbors'); reveal_panel(self,p,2,3)
        self.at('relative to the axons'); self.play(Indicate(VGroup(*p[2][4:-1]),color=YELLOW,scale_factor=1.02),run_time=.65)
        self.finish()

class S16Both(SpokenScene):
    def construct(self):
        p=panels(3)
        p[2].remove(p[2][2],p[2][3])
        p[2].add(label('axon tips',4.35,.9,28,YELLOW))
        self.add(p,label('Chick and mouse',0,3.15,34),label('gradient + neighbours: both are used',0,-3.5,30,YELLOW))
        self.at('uses gradients'); self.play(FadeOut(p[0]),p[1].animate.move_to([-2.4,-.25,0]),p[2].animate.move_to([2.4,-.25,0]),run_time=.5)
        self.at('and neighbors together'); self.play(FadeIn(label('+',0,-.25,42,YELLOW)),run_time=.4)
        self.finish()

def slope_base(grad=False):
    r=gradient(-4,.2,4.4,.7,BLUE,True) if grad else RoundedRectangle(width=.7,height=4.4,corner_radius=.1,color=GREY).move_to([-4,.2,0])
    t=gradient(1.3,-.6,7.2,1.25) if grad else RoundedRectangle(width=7.2,height=1.25,corner_radius=.1,color=GREY).move_to([1.3,-.6,0])
    names=VGroup(label('retina',-4,3.15,28),label('sending side',-4,2.72,26,SLATE),
        label('nasal',-5.15,1.95,26,SLATE),label('temporal',-4,-2.55,26,GOLD),
        label('target',1.3,-2.15,28),label('anterior / front',-1.1,-1.6,26,SLATE),
        label('posterior / back',3.65,-1.6,26,SLATE))
    return VGroup(r,t,names)

def retinal_slope():
    return VGroup(gradient(-4,.2,4.4,.7,BLUE,True),
        Rectangle(width=.7,height=1.1,stroke_color=SLATE,stroke_width=1.5,stroke_opacity=.5).move_to([-4,1.85,0]))

def slope_labels():
    return VGroup(label('EphA: receptor',-.8,2.35,28,BLUE),
        label('ephrin-A: repellent',1.3,.85,28,ORANGE),
        label('brighter = more',2.8,3.1,26,SLATE),
        label('low',-5.15,1.1,26,BLUE),label('high',-5.15,-1.2,26,BLUE),
        label('low',-1.8,.3,26,ORANGE),label('high',4.4,.3,26,ORANGE))

class S17Slopes(SpokenScene):
    def construct(self):
        b=slope_base(); r,t=b[0],b[1]; ml=slope_labels(); self.add(b,ml[2])
        self.at('Each axon carries'); self.play(FadeOut(r),FadeIn(retinal_slope()),run_time=.7)
        self.at('called'); self.play(FadeIn(ml[0]),FadeIn(ml[3]),FadeIn(ml[4]),run_time=.4)
        self.at('The target carries'); self.play(FadeOut(t),FadeIn(gradient(1.3,-.6,7.2,1.25)),run_time=.7)
        self.at('a repellent'); self.play(FadeIn(ml[1]),FadeIn(ml[5]),FadeIn(ml[6]),run_time=.45)
        self.finish()

class S18Rule(SpokenScene):
    def construct(self):
        b=slope_base(True); b[0].become(retinal_slope())
        self.add(b,slope_labels())
        self.at('low at the front'); self.play(Indicate(self.mobjects[1][5],scale_factor=1.1),run_time=.4)
        self.at('high at the back'); self.play(Indicate(self.mobjects[1][6],scale_factor=1.1),run_time=.4)
        self.at('The axon with the most receptor')
        branch=tuft(-1.65,-.6,GOLD).scale(1.4)
        path=VMobject(stroke_color=GOLD,stroke_width=5).set_points_as_corners([
            [-3.65,-1.45,0],[-2.8,-1.45,0],[-2.8,.15,0],branch.get_top()])
        axon=VGroup(path,cell(-4,-1.45,GOLD),branch)
        self.play(FadeIn(axon),run_time=.6)
        self.at('ends where it is lowest'); self.play(FadeIn(label('More receptor, less ligand',1.3,1.65,32)),run_time=.4)
        self.finish()

class S19Rank(SpokenScene):
    def construct(self):
        self.add(rank_base())
        tokens=VGroup(*[rank_token(i,-4.7,1.8-.78*[2,0,4,1,3][i]) for i in range(5)])
        self.add(tokens,label('More receptor, less ligand',1.5,1.8,30))
        self.at('More receptor'); self.play(*[tokens[i].animate.move_to(rank_token(i,-4.7,1.8-.78*int(RANK[i])).get_center()) for i in range(5)],run_time=1.15)
        self.at('but where each axon lands')
        for i in ORDER[:3]:
            tip=tuft(-3.1,1.8-.78*int(RANK[i]),IDS[i]); self.add(tip)
            self.play(tip.animate.move_to(tuft(SLOTS[int(RANK[i])],-2.25,IDS[i]).get_center()),run_time=.5)
        self.at('depends on the other axons')
        for i in ORDER[3:]:
            tip=tuft(-3.1,1.8-.78*int(RANK[i]),IDS[i]); self.add(tip)
            self.play(tip.animate.move_to(tuft(SLOTS[int(RANK[i])],-2.25,IDS[i]).get_center()),run_time=.4)
        self.play(FadeIn(label('place = rank among axons, against the slope',1.1,.55,28,YELLOW)),run_time=.3)
        self.finish()

class S20Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(rank_result()); self.wait(3)

class S21Takeaway(SpokenScene):
    def construct(self):
        bar=gradient(0,-2.6,10,.7)
        for segment in bar[:-1]:
            segment.set_fill(opacity=segment.get_fill_opacity()*.35)
        bar[-1].set_stroke(opacity=.3)
        bg=VGroup(bar,
            *[tuft(x,-2.6,IDS[i]).scale(1.25).set_opacity(.65) for i,x in enumerate(np.linspace(-4.4,4.4,5))])
        self.add(bg,label('The takeaway',0,2.85,32,SLATE),label('Coarse front-to-back map • chick and mouse',0,-3.35,26,SLATE))
        self.at("an axon's place")
        first=VGroup(label("An axon's place is not an address",0,1.45,44),label('in its own receptor level.',0,.55,44))
        self.play(FadeIn(first),run_time=.5)
        self.at('It is a rank')
        second=VGroup(label('It is a rank,',0,-.65,48,YELLOW),label('set against a slope.',0,-1.55,48,YELLOW))
        self.play(FadeIn(second),run_time=.5)
        self.finish()

class S22End(EndCard):
    LINE="An axon's place is a rank, set against a slope."
