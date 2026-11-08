"""Followers, Glue and the Reader — reviewed animation.
COLOR MAP: BLUE pioneer axons; YELLOW guideposts; GREEN normal route/exit;
RED abnormal extension; PURPLE follower axons; GREY tissue; TEXT labels;
TEAL adhesion/reader proteins; GOLD cue. Paths are qualitative anatomical
schematics, never measured traces or simulated quantitative data.
"""
import numpy as np
import os
from pathlib import Path
from bp_style import *
from bp_style import SpokenScene as BaseSpokenScene
PURPLE = '#B58CD9'
LESSON = 'Pioneers, Guideposts and the Logic of Guidance Cues'

class SpokenScene(BaseSpokenScene):
    def at(self, phrase, lead=0, nth=0):
        # Log the actual post-wait animation onset against the aligned audio.
        target = self.t_of(phrase, nth)
        rest = target - lead - self.elapsed()
        if rest > .02: self.wait(rest)
        with open(Path(os.environ['KX_SCRIPT']).parent / 'sync.log', 'a') as log:
            log.write(f"{os.environ['KX_SCENE_ID']} {phrase!r} target={target:.3f} onset={self.elapsed():.3f} delta={self.elapsed()-target:+.3f}\n")

def label(s,x=0,y=3.15,size=32,color=TEXT):
    return T(s,size=size,color=color).move_to([x,y,0])

def path(points,color=PURPLE,width=8):
    return VMobject().set_points_as_corners([np.array([x,y,0]) for x,y in points]).set_stroke(color,width)

def cone(x,y,color=PURPLE):
    core=Circle(.22,stroke_width=0,fill_color=color,fill_opacity=1)
    spikes=VGroup(*[Line(.20*np.array([np.cos(a),np.sin(a),0]),.46*np.array([np.cos(a),np.sin(a),0]),color=color,stroke_width=4) for a in np.linspace(0,TAU,8,endpoint=False)])
    return VGroup(core,spikes).move_to([x,y,0]).set_z_index(5)

def bundles():
    return VGroup(*[VGroup(*[Line([x+d,-3,0],[x+d,2.55,0],color=GREY,stroke_width=7) for d in (-.12,.12)]) for x in (-3,0,3)])

def timer():
    return VGroup(Circle(.18,color=GREY),Line(ORIGIN,UP*.12,color=GREY)).move_to([6,3.2,0])

def two_panels(ghost=True,reach=False):
    panels=VGroup()
    for cx,title,missing in [(-3.25,'P removed','P'),(3.25,'A removed','A')]:
        border=RoundedRectangle(width=6.05,height=6.3,corner_radius=.15,stroke_color=GREY,stroke_opacity=.5).move_to([cx,-.2,0])
        neighbours=VGroup(*[VGroup(*[Line([cx+d+e,-2.65,0],[cx+d+e,1.9,0],color=GREY,stroke_width=5) for e in (-.08,.08)]) for d in (-2,2)])
        keep=Line([cx-.25 if missing=='P' else cx+.25,-2.65,0],[cx-.25 if missing=='P' else cx+.25,1.8,0],color=BLUE,stroke_width=9)
        names=VGroup(label('A',cx-.4,2.15,30,BLUE),label('P',cx+.4,2.15,30,BLUE))
        gx=cx+.25 if missing=='P' else cx-.25
        gone=VGroup(DashedLine([gx,-2.65,0],[gx,1.8,0],color=GREY,dash_length=.16,stroke_opacity=.6),label('×',gx,1.3,38,GREY))
        c=cone(cx-.8,-1.95).scale(.8)
        p=VGroup(border,label(title,cx,2.65,30),neighbours,keep,names,c,gone)
        if not ghost: gone.set_opacity(0)
        if reach:
            p.add(VGroup(*[Line([cx-.8,-1.85,0],[cx+d,-1.25,0],color=PURPLE,stroke_width=3) for d in (-2,2)]))
        panels.add(p)
    return panels

def normal_baseline():
    return VGroup(DashedVMobject(path([(-4.05,-1.95),(-2.65,-1.3),(-2.65,1.5)],GREY,3)),label('normal',-1.35,2.15,28,GREY))

def abnormal():
    return VGroup(path([(-4.05,-1.95),(-4.05,-1.35),(-4.5,-.8),(-4.1,-.25)],RED),path([(-4.05,-1.35),(-3.2,-.9),(-2.8,-.4)],RED)).set_z_index(1)

def failure_note(): return label('no neighbouring\nbundle taken',-3.25,-3.0,28,RED)

def both_chip():
    c=chip('A and P removed',GREY,30).move_to([0,-3.3,0]).set_z_index(8)
    c[0].set_fill(BG,opacity=1)
    return c

def prediction(): return VGroup(two_panels(reach=True),label('What did G do?'),timer(),both_chip())

def motor_panel(cx,title,mode='blank',wide=False):
    w=11.8 if wide else 3.95
    nerve_x=cx-2 if wide else cx-.85
    muscle_x=cx+2.5 if wide else cx+1.0
    base=VGroup(RoundedRectangle(width=w,height=6.25,corner_radius=.16,stroke_color=GREY,stroke_opacity=.5).move_to([cx,-.2,0]),label(title,cx,2.5,30 if wide else 28),VGroup(*[Line([nerve_x+d,-2.9,0],[nerve_x+d,1.55,0],color=GREY,stroke_width=6) for d in (-.24,.24)]),RoundedRectangle(width=2.0 if wide else .9,height=1.9 if wide else 1.4,corner_radius=.15,color=GREY,fill_opacity=.16).move_to([muscle_x,0,0]),label('muscle',muscle_x,-1.3 if wide else -1.05,32 if wide else 28,GREY))
    if mode=='blank': return VGroup(base,label('?',cx,0,60))
    pts=[(nerve_x,-2.8),(nerve_x,-.8),(muscle_x-.6,0)] if mode=='exit' else [(nerve_x,-2.8),(nerve_x,1.5)]
    return VGroup(base,path(pts),cone(*pts[-1]).scale(.65))

def beat_tag(cx=-4.2):
    return VGroup(chip('Beat',TEAL,28).move_to([cx+.15,-1.8,0]),Line([cx-.85,-1.8,0],[cx-.48,-1.8,0],color=TEAL,stroke_width=5))

def strip(third='blank'):
    return VGroup(motor_panel(-4.2,'normal','exit'),motor_panel(0,'Beat absent','stay'),motor_panel(4.2,'Beat absent +\nless Fasciclin II',third),beat_tag())

def gradient():
    bands=VGroup(*[Rectangle(width=.72,height=4.75,stroke_width=0,fill_color=GOLD,fill_opacity=.27+.045*i).move_to([-1.1+i*.72,0,0]) for i in range(10)])
    return VGroup(bands,label('less netrin',-.65,-2.75,28,GOLD),label('more netrin',4.8,-2.75,28,GOLD),label('netrin-1',3.8,2.85,32,GOLD))

def reader_scene(two=False,finished=False):
    g=VGroup(gradient(),label('one example; stated conditions',0,-3.35,28,GREY))
    y=1.15 if two else 0
    c=cone(1,y+.5) if finished else cone(-3,y if two else -.7)
    tag=chip('DCC',BLUE,28).move_to([-.1 if finished else -3,2.6 if finished else y+1,0])
    g.add(c,tag)
    if two:
        g.add(cone(-3,-1.15),chip('DCC + UNC5',BLUE,28).move_to([-3,-2.15,0]))
    return g

def toward(y=0):
    return VMobject().set_points_smoothly([np.array([x,z,0]) for x,z in [(-3,y-1.8),(-3,y-.7),(-2.6,y+.1),(-1,y+.5),(1,y+.5)]]).set_stroke(PURPLE,8)

class S00Title(TitleCard):
    LESSON=LESSON
    TITLE='Followers, Glue and the Reader'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.65,28,TEAL),label('Pioneers, Guideposts and\nthe Logic of Guidance Cues',0,1.35,30,GREY),label('Followers, Glue\nand the Reader',0,-.65,52))
        self.finish()

class S01Question(SpokenScene):
    def construct(self):
        b=bundles(); c=cone(-1.5,-2.4); self.add(b,c)
        self.at('meets many bundles'); self.play(c.animate.shift(UP*1.1),run_time=.8)
        touch=VGroup(*[Line([-1.5,-1.3,0],[x,-.65,0],color=PURPLE,stroke_width=4) for x in (-3,0)])
        self.at('Its filopodia'); self.play(Create(touch),b[0].animate.set_color(TEAL),b[1].animate.set_color(TEAL),run_time=.65)
        self.at('Why does it'); self.play(FadeIn(label('Why join just one?')),run_time=.4); self.finish()

class S02Terms(SpokenScene):
    def construct(self):
        ax=VGroup(*[Line([-1.7+d,-3,0],[-1.7+d,2.25,0],color=PURPLE,stroke_width=10) for d in (-.32,0,.32)])
        self.add(ax)
        self.at('they are'); self.play(FadeIn(label('fasciculated',-1.7,3,36,PURPLE)),run_time=.3)
        self.at('one leaves its bundle'); self.play(Transform(ax[2],path([(-1.38,-3),(-1.38,-.8),(2,.7),(2,2.25)],PURPLE,10)),run_time=.85)
        self.at('it'); self.play(FadeIn(label('defasciculates',3.7,1.15,34,PURPLE)),run_time=.3); self.wait(3); self.finish()

class S03G(SpokenScene):
    def construct(self):
        cns=RoundedRectangle(width=11.6,height=6.1,corner_radius=.7,color=GREY,fill_opacity=.06).shift(DOWN*.15)
        b=VGroup(*[VGroup(*[Line([x+d,-2.9,0],[x+d,2.3,0],color=GREY,stroke_width=6) for d in (-.08,.08)]) for x in (-4,-2,0,2,4)])
        self.add(cns,b,label('grasshopper embryonic CNS',0,3.25,32,GREY))
        g=VGroup(Circle(.3,color=PURPLE,fill_opacity=1).move_to([-4.8,-1.7,0]),path([(-4.5,-1.7),(-2,-1.7),(.5,-.6)]),cone(.5,-.6))
        self.at('followed a neuron'); self.play(FadeIn(g),run_time=.5)
        self.at('called'); self.play(FadeIn(label('G',-4.8,-2.4,34,PURPLE)),FadeIn(label('G',1.25,-.55,34,PURPLE)),run_time=.3); self.finish()

class S04Ap(SpokenScene):
    def construct(self):
        ax=VGroup(Line([-.7,-3,0],[-.7,2.5,0],color=BLUE,stroke_width=15),Line([.7,-3,0],[.7,2.5,0],color=BLUE,stroke_width=15)); c=cone(-3,-2)
        self.add(ax,c)
        self.at('joins one bundle'); self.play(c.animate.move_to([1.1,-1.4,0]),Create(path([(-4,-2),(-3,-2),(1.1,-1.4)])),run_time=.8)
        self.at('fascicle'); self.play(FadeIn(label('A/P fascicle')),run_time=.3)
        self.at('made of axons'); self.play(FadeIn(label('A',-1.5,2,38,BLUE)),FadeIn(label('P',1.8,2,38,BLUE)),run_time=.3)
        self.at('It grows along'); self.play(c.animate.move_to([1.1,1.4,0]),Create(path([(1.1,-1.4),(1.1,1.4)])),run_time=1.25); self.finish()

class S05Ablate(SpokenScene):
    def construct(self):
        p=two_panels(False); alive=VGroup(Line([-3,-2.1,0],[-3,1.8,0],color=BLUE,stroke_width=9),Line([3,-2.1,0],[3,1.8,0],color=BLUE,stroke_width=9)); self.add(p,alive)
        self.at('the team killed'); self.play(FadeOut(alive[0]),p[0][6].animate.set_opacity(1),Transform(p[0][1],label('P removed',-3.25,2.65,30)),run_time=.4)
        self.at('the neurons'); self.play(FadeOut(alive[1]),p[1][6].animate.set_opacity(1),Transform(p[1][1],label('A removed',3.25,2.65,30)),run_time=.35)
        self.at('or both'); self.play(FadeIn(both_chip()),run_time=.3); self.finish()

class S06Predict(SpokenScene):
    def construct(self):
        p=two_panels(); self.add(p,label('What did G do?'),both_chip())
        self.at('should take a neighbor'); self.play(*[Create(VGroup(*[Line([cx-.8,-1.85,0],[cx+d,-1.25,0],color=PURPLE,stroke_width=3) for d in (-2,2)])) for cx in (-3.25,3.25)],run_time=.7)
        self.at('What did G do'); self.play(FadeIn(timer()),run_time=.3); self.finish()

class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction()); self.wait(5)

class S08RevealP(SpokenScene):
    def construct(self):
        p=two_panels(); self.add(p,normal_baseline())
        self.at('failed to extend'); self.play(Create(path([(-4.05,-1.95),(-4.05,-1.35)])),p[0][5].animate.move_to([-4.05,-1.35,0]),run_time=.65)
        self.at('It wandered'); self.play(Create(abnormal()),p[0][5].animate.move_to([-4.1,-.25,0]).set_color(RED),run_time=1)
        self.at('took no other bundle'); self.play(FadeIn(failure_note()),run_time=.3); self.finish()

class S09RevealA(SpokenScene):
    def construct(self):
        p=two_panels(); p[0][5].move_to([-4.1,-.25,0]).set_color(RED); self.add(p,normal_baseline(),abnormal(),failure_note())
        self.at('Without only'); self.play(Create(path([(2.45,-1.95),(3.85,-1.3),(3.85,1.5)],GREEN)),p[1][5].animate.move_to([3.85,1.5,0]),run_time=1.25)
        self.at('behaved normally'); self.play(FadeIn(label('normal',3.25,-2.75,30,GREEN)),run_time=.3); self.wait(3); self.finish()

class S10Beat1(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(label('Which axons are needed?',0,3,38))
        for y,a,b,c in [(1.1,'A removed','normal',GREEN),(-1.15,'P removed','fails; no neighbouring\nbundle taken',RED)]:
            self.add(label(a,-3.5,y,36),label(b,1.7,y,34,c),Line([-5.7,y-.85,0],[5.7,y-.85,0],color=GREY))
        self.wait(3.5)

class S11Label(SpokenScene):
    def construct(self):
        b=bundles(); c=cone(-1.1,-1.4); name=label('G',-1.15,-2.15,32,PURPLE)
        tags=VGroup(*[chip('label',col,28).move_to([x,.45,0]) for x,col in [(-3,GREY),(0,TEAL),(3,GREY)]])
        receptor=Square(.3,color=TEAL,fill_opacity=.6).move_to([-.83,-1.13,0]); gc=VGroup(c,receptor,name)
        for tag in tags: tag[0].set_fill(BG,opacity=1)
        self.add(b,tags,gc,label('labeled pathway hypothesis',0,3.25,32))
        self.at('needs something particular'); self.play(Indicate(tags[1],color=TEAL),run_time=.5)
        self.at('labeled pathway hypothesis'); self.play(Indicate(receptor,color=TEAL),run_time=.5)
        self.at('Bundles carry surface labels'); self.play(Indicate(tags[1],color=TEAL),run_time=.3)
        self.at('growth cones recognize'); self.play(gc.animate.shift(RIGHT*.5+UP*.65),run_time=.65); self.finish()

class S12Fly(SpokenScene):
    def construct(self):
        embryo=Ellipse(width=7.5,height=5.85,color=GREY,fill_opacity=.1).move_to([-1.8,-.15,0])
        cord=VGroup(*[Line([-2+d,-2.7,0],[-2+d,2.4,0],color=BLUE,stroke_width=8) for d in (-.16,.16)])
        nerves=VGroup(*[path([(-2,y),(-.8,y+.15),(.3,y+.6)],BLUE,6) for y in (-1.8,-.9,0,.9,1.6)])
        self.add(embryo,cord,nerves,label('Drosophila embryo',0,3.25,34),label('schematic',-2,-3.35,28,GREY),label('motor nerve',3.4,.55,32,BLUE),Line([1.85,.55,0],[.3,.6,0],color=BLUE))
        self.at('adhesion molecules'); self.play(FadeIn(label('adhesion\nmolecules',3.4,-.8,34,TEAL)),nerves.animate.set_color(TEAL),run_time=.4)
        self.at('not a unique label'); self.play(FadeIn(label('not one unique\nlabel per bundle',3.4,-2.3,30)),run_time=.4); self.finish()

class S13Fas2(SpokenScene):
    def construct(self):
        a=Line([-5.6,1.25,0],[5.6,1.25,0],color=PURPLE,stroke_width=16); b=a.copy().shift(DOWN*2.5)
        la=label('axon',-4,1.9,34,PURPLE); lb=label('neighbouring axon',3,-1.95,32,PURPLE)
        top=chip('Fasciclin II',TEAL,30).move_to([0,.65,0]); bottom=chip('Fasciclin II',TEAL,30).move_to([0,-.65,0])
        links=VGroup(top,bottom,Line([0,1.25,0],top.get_top(),color=TEAL,stroke_width=5),Line([0,-1.25,0],bottom.get_bottom(),color=TEAL,stroke_width=5))
        self.add(a,b,la,lb,links[0],links[2],label('axon-to-axon adhesion',0,3.2,36))
        self.at('can bind'); self.play(FadeIn(links[1]),FadeIn(links[3]),Create(Line(top.get_bottom(),bottom.get_top(),color=TEAL,stroke_width=6)),run_time=.65)
        self.at('Without it'); self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in (a,b,la,lb) and m.get_center()[1]<2.5],FadeIn(label('Fasciclin II lost',0,0,34,TEAL)),run_time=.4)
        self.at('drift apart'); self.play(a.animate.shift(UP*1.05),la.animate.shift(UP*.65),b.animate.shift(DOWN*1.05),lb.animate.shift(DOWN*.85),run_time=.8); self.wait(3); self.finish()

class S14Gain(SpokenScene):
    def construct(self):
        p=motor_panel(0,'separate experiment','stay',True)
        p[1].become(path([(-2,-2.8),(-2,-1.2)])); p[2].move_to([-2,-1.2,0]); self.add(p)
        links=VGroup(*[chip('II',TEAL,30).move_to([-3.65,y,0]) for y in (-2,-.8,.4,1.5)])
        self.at('extra'); self.play(FadeIn(links),FadeIn(label('extra Fasciclin II',1,1.7,34,TEAL)),run_time=.5)
        self.at('motor axons'); self.play(Transform(p[1],path([(-2,-2.8),(-2,2.0)])),p[2].animate.move_to([-2,2.0,0]),run_time=1.1)
        self.at('They bypass'); self.play(FadeIn(label('continues past muscle',1.9,-2.3,36,RED)),Create(DashedLine([-1.7,0,0],[1.75,0,0],color=RED,dash_length=.15)),run_time=.35); self.finish()

class S15Amount(SpokenScene):
    def construct(self):
        diagrams=VGroup()
        for cx,sep,title in [(-3.35,1.0,'drift apart'),(3.35,.25,'stay stuck')]:
            diagrams.add(VGroup(*[Line([cx+d,-2.15,0],[cx+d,.1,0],color=PURPLE,stroke_width=13) for d in (-sep,sep)]),label(title,cx,-2.65,36),chip('II',TEAL,30).move_to([cx,-1,0]))
        self.add(diagrams,label('qualitative: two experiments',0,-3.4,32,GREY))
        rail=Line([-3.35,1.65,0],[3.35,1.65,0],color=TEAL,stroke_width=10)
        ticks=VGroup(*[Line([x,1.4,0],[x,1.9,0],color=TEAL,stroke_width=4) for x in np.linspace(-3.35,3.35,7)])
        knob=Triangle(color=TEXT,fill_opacity=1).scale(.23).rotate(PI).move_to([-3.35,2.25,0])
        self.at('amount of adhesion'); self.play(FadeIn(VGroup(rail,ticks,knob,label('adhesion',0,3.05,44,TEAL),label('low',-3.35,.85,34),label('high',3.35,.85,34))),run_time=.4)
        self.play(knob.animate.shift(RIGHT*6.7),run_time=.8); self.finish()

class S16Beat(SpokenScene):
    def construct(self):
        p=strip(); p[1][1:].set_opacity(0); self.add(p[0],p[1],p[2],label('Beat on motor axons',0,3.3,34))
        self.at('beaten path'); self.play(FadeIn(p[3]),run_time=.4)
        self.at('Without it'); self.play(Indicate(p[1][0][1],color=TEXT),run_time=.45)
        self.at('fail to leave'); self.play(p[1][1:].animate.set_opacity(1),run_time=.65); self.finish()

class S17Predict2(SpokenScene):
    def construct(self):
        p=strip(); self.add(p,label('What happens at the choice point?',0,3.3,32),timer())
        self.at('Now reduce'); self.play(Indicate(p[2][0][1],color=TEAL),run_time=.6)
        self.at('What happens'); self.play(Indicate(p[2][1],color=TEXT),run_time=.5); self.finish()

class S18Pause2(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(strip(),label('What happens at the choice point?',0,3.3,32),timer()); self.wait(5)

class S19Reveal2(SpokenScene):
    def construct(self):
        p=strip(); self.add(p,label('suppression, not complete rescue',0,3.3,30,GREEN))
        self.at('defect is suppressed'); self.play(FadeOut(p[2][1]),run_time=.3)
        self.at('can often leave'); self.play(Create(path([(3.35,-2.8),(3.35,-.8),(4.6,0)],GREEN)),FadeIn(cone(4.6,0,GREEN).scale(.65)),Create(path([(3.65,-2.8),(3.65,1.35)],PURPLE,5).set_opacity(.45)),run_time=.8)
        self.add(label('some axons',4.7,-1.9,28,GREEN)); self.wait(3); self.finish()

class S20Oppose(SpokenScene):
    def construct(self):
        # A schematic balance: beam pivot and triangle apex share (0,-.3).
        pivot=np.array([0,-.3,0])
        fulcrum=Polygon([-1.1,-2.8,0],[1.1,-2.8,0],pivot,color=GREY,fill_opacity=.4)
        beam=VGroup(Line([-5,-.3,0],[5,-.3,0],color=TEXT,stroke_width=10),RoundedRectangle(width=2.6,height=1.1,corner_radius=.1,color=TEAL,fill_opacity=.25).move_to([-3.8,.25,0]),RoundedRectangle(width=2.6,height=1.1,corner_radius=.1,color=GREEN,fill_opacity=.25).move_to([3.8,.25,0]))
        self.add(fulcrum,beam,label('axon adhesion',-3.6,2.75,34,TEAL),label('pull to exit',3.6,2.75,34,GREEN),chip('Beat absent',TEAL,30).move_to([3.6,1.7,0]),label('genetic suppression; direct binding untested',0,-3.35,28,GREY))
        self.at('Lowering adhesion'); self.play(FadeIn(label('Fasciclin II reduced',-3.5,1.65,30,TEAL)),beam[1].animate.stretch(.5,1,about_edge=DOWN),run_time=.65)
        self.at('makes up for'); self.play(Rotate(beam,-.25,about_point=pivot),run_time=.9)
        self.at('at least partly against'); self.play(FadeIn(label('favours leaving\nthe nerve',3.8,-2.35,30,GREEN)),run_time=.4); self.finish()

class S20bSidestep(SpokenScene):
    def construct(self):
        nerve=VGroup(*[Line([-4+d,-3,0],[-4+d,2.7,0],color=GREY,stroke_width=7) for d in (-.2,.2)])
        tissue=RoundedRectangle(width=4,height=4.7,corner_radius=.25,color=GOLD,fill_opacity=.13).move_to([3.4,-.1,0]); c=cone(-3.3,-1.8)
        trail=path([(-3.3,-2.8),(-3.3,-1.8)])
        beat=chip('Beat',TEAL,30).move_to([-2.4,-2.3,0]); anchor=Line([-3.3,-2.3,0],[-3.1,-2.3,0],color=TEAL,stroke_width=5)
        self.add(nerve,tissue,c,trail,beat,anchor,label('Sidestep',3.4,1.1,36,GOLD),label('motor nerve',-4,3.25,32,GREY))
        self.at('recognize'); self.play(Create(path([(-3.3,-1.8),(-3.3,-.6),(1.1,.3)])),c.animate.move_to([1.1,.3,0]),run_time=1.1)
        self.at('called sidestep'); self.play(Indicate(tissue,color=GOLD),run_time=.45); self.finish()

class S21Dcc(SpokenScene):
    def construct(self):
        r=reader_scene(); self.add(r,path([(-3,-1.8),(-3,-.7)]))
        self.at('simple comparison'); self.play(Indicate(r[3],color=BLUE),run_time=.5)
        self.at('can attract'); self.play(Create(toward()),MoveAlongPath(r[2],VMobject().set_points_smoothly([np.array(v) for v in [(-3,-.7,0),(-2.6,.1,0),(-1,.5,0),(1,.5,0)]])),r[3].animate.move_to([.5,1.55,0]),run_time=1.15); self.finish()

class S22Unc5(SpokenScene):
    def construct(self):
        r=reader_scene(True,True); self.add(r,toward(1.15),path([(-4.7,-1.8),(-3,-1.15)]))
        self.at('second receptor'); self.play(Indicate(r[5],color=BLUE),run_time=.5)
        self.at('can repel'); self.play(Create(path([(-3,-1.15),(-4,-.65),(-5.5,-.6)])),r[4].animate.move_to([-5.5,-.6,0]),r[5].animate.move_to([-4.8,-2.4,0]),run_time=.8); self.wait(3); self.finish()

class S22bState(SpokenScene):
    def construct(self):
        c=cone(-1,.1); tag=chip('DCC',BLUE,28).move_to([-1,1.05,0])
        turn=path([(-3,-.45),(-1,.1),(1,.5)])
        self.add(c,tag,turn,label('response can also flip',0,3.3,36),label('example: lower cAMP signaling can reverse attraction',0,-3.35,28,GREY))
        dial=VGroup(Arc(radius=.85,start_angle=0,angle=PI,color=TEAL),*[Line([3.5+.75*np.cos(a),1+.75*np.sin(a),0],[3.5+.95*np.cos(a),1+.95*np.sin(a),0],color=TEAL) for a in np.linspace(0,PI,5)])
        dial[0].move_to([3.5,1.42,0]); needle=Line([3.5,1,0],[2.85,1.45,0],color=TEXT,stroke_width=5)
        self.at('internal state'); self.play(FadeIn(dial),FadeIn(needle),FadeIn(label('internal state\ncAMP signaling',3.5,2.55,30,TEAL)),FadeIn(label('higher cAMP',2.15,.15,28)),FadeIn(label('lower cAMP',5,.15,28)),run_time=.4)
        self.at('flip the response'); self.play(Transform(turn,path([(-3,-.45),(-1,.1),(-3,.6),(-4.8,.6)])),c.animate.move_to([-4.8,.6,0]),tag.animate.move_to([-4.8,1.6,0]),Transform(needle,Line([3.5,1,0],[4.15,1.45,0],color=TEXT,stroke_width=5)),Indicate(dial,color=TEAL),FadeIn(label('lower cAMP → away',1.9,-1.8,34,TEAL)),run_time=.7); self.wait(3); self.finish()

class S23Message(SpokenScene):
    def construct(self):
        r=reader_scene(True,True); r[4].move_to([-5.5,-.6,0]); r[5].move_to([-4.8,-2.4,0])
        heading=label('A cue is a message',0,3.5,36)
        self.add(r,toward(1.15),path([(-4.7,-1.8),(-3,-1.15),(-4,-.65),(-5.5,-.6)]),heading)
        self.at('decide what it means'); self.play(Transform(heading,label('the reader decides',0,3.5,38)),run_time=.4); self.wait(3); self.finish()

class S24Takeaway(SpokenScene):
    def construct(self):
        b=VGroup(*[VGroup(*[Line([x+d,-3.15,0],[x+d,2.9,0],color=GREY,stroke_width=13) for d in (-.15,.15)]) for x in (-5.6,-3.7)]); c=cone(-3.05,-2.65).scale(1.3)
        self.add(b,c)
        self.at('followers choose'); self.play(Create(path([(-3.05,-2.65),(-3.05,2.25)],PURPLE,12)),c.animate.move_to([-3.05,2.25,0]),FadeIn(label('Followers choose\na bundle.',1.9,1.65,46,PURPLE)),run_time=.8)
        self.at('the reader decides'); self.play(FadeIn(label('The reader decides\nwhat a cue means.',1.9,-1.2,44)),run_time=.4); self.wait(3); self.finish()

class S25End(EndCard):
    LINE='Followers choose a bundle; the reader decides what a cue means.'
    def construct(self):
        self.add(label('Followers choose a bundle;',0,1.3,42,PURPLE),label('the reader decides\nwhat a cue means.',0,-.4,42),label('biochemistrypedia.com',0,-2.5,28,TEAL)); self.finish()
