"""Chapter 5: Same Receptor, Opposite Turn.
COLOR MAP (shared with scenes.old.py):
YELLOW netrin; BLUE growth cone/axon; TEAL DCC; PURPLE UNC5;
ORANGE cAMP/internal state; PINK anti-DCC; GREEN attraction;
RED repulsion/blocked signal; GREY anatomy/pipette/ghost paths.
Laminin is a GREY substrate with a text label; calcium is TEXT.
All curved biological schematics reuse the reference helpers and paths;
there are no quantitative plots or invented response curves in this chapter.
"""
import importlib.util
from pathlib import Path
import numpy as np
from bp_style import *

_spec = importlib.util.spec_from_file_location('reference', Path(__file__).resolve().parent.parent / 'scenes.old.py')
ref = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ref)
ORANGE, PINK = ref.ORANGE, ref.PINK
# Schematic trajectories illustrate direction only; they are not experimental traces.
# The only concentration field is computed as C(r) proportional to 1/r.
C = np.array([-1.2, -.25, 0.])
SRC = np.array([4.8, 1.2, 0.])
TOWARD = [C, [-.1,-.15,0], [1.25,.4,0], [2.7,1.,0]]
AWAY = [C, [-1.65,-.9,0], [-2.4,-1.5,0], [-3.2,-1.85,0]]

# Keep word-level alignment without creating an unrequested sync.log artifact.
class Aligned(SpokenScene):
    def at(self, phrase, lead=.2, nth=0):
        rest=self.t_of(phrase,nth)-lead-self.elapsed()
        if rest>.02: self.wait(rest)


def text(s, x=0, y=3.15, color=TEXT, size=30):
    return T(s, size=size, color=color).move_to([x,y,0])


def cone(c=C, scale=1.35, blocked=False, antibody=False):
    c=np.array(c,float)
    g=VGroup(ref.body(c,scale),ref.cups(c,ref.DCC_A,TEAL,scale))
    if blocked:
        p=chip('PKA',ORANGE,size=26).move_to(c)
        g.add(p,Line(p.get_corner(DL),p.get_corner(UR),color=RED,stroke_width=5))
    if antibody: g.add(ref.caps(c,ref.DCC_A,scale))
    return g


def ghost(g, opacity):
    # Preserve open cup geometry; set_opacity would fill open arcs.
    for m in g.family_members_with_points():
        m.set_stroke(opacity=opacity)
        m.set_fill(opacity=m.get_fill_opacity()*opacity)
    return g


def source(c=SRC, compact=False):
    c=np.array(c)
    f=.65 if compact else 1.
    return VGroup(Polygon(c+f*np.array([.15,.12,0]),c+f*np.array([1.15,1.35,0]),c+f*np.array([.8,1.6,0]),
                         color=GREY,fill_color=GREY,fill_opacity=.45),
                  Dot(c,radius=.19,color=YELLOW),
                  text('netrin',c[0],c[1]-.6,YELLOW,26))


def gradient():
    # Isoconcentration arcs: radius r = k/C for steady point diffusion.
    arcs=VGroup()
    for r in [1.,2.,3.2,4.6,6.,7.4]:
        a=Arc(radius=r,start_angle=PI+.02,angle=.52,arc_center=SRC,
              color=YELLOW,stroke_width=3,stroke_opacity=max(.45,min(.9,2/r)))
        arcs.add(a)
    return arcs.set_z_index(-3)


def assay(scene, blocked=False, antibody=False):
    g=cone(blocked=blocked,antibody=antibody)
    scene.add(ref.smooth([[-1.2,2.6,0],[-1.2,1.1,0],C]).set_stroke(BLUE,10).set_z_index(-2),g,source())
    return g


def travel(scene,mobs,points,duration):
    full=ref.smooth(points).set_stroke(BLUE,10).set_fill(opacity=0).set_z_index(-2)
    trail=full.copy(); trail.pointwise_become_partial(full,0,.001)
    scene.add(trail)
    group=VGroup(*mobs); last=[np.array(points[0],float)]
    def step(m,a):
        trail.pointwise_become_partial(full,0,max(a,.001))
        pos=trail.get_end(); group.shift(pos-last[0]); last[0]=pos.copy()
    scene.play(UpdateFromAlphaFunc(VGroup(group,trail),step),run_time=duration)
    return trail


def puff(scene):
    arcs=gradient()
    scene.play(LaggedStart(*[Create(a) for a in arcs],lag_ratio=.08),run_time=.55)
    scene.play(FadeOut(arcs),run_time=.2)


def choices2():
    return VGroup(*[chip(s,GREY,size=26) for s in
        ['attraction only','repulsion only','both','neither']]).arrange(RIGHT,buff=.24).move_to([0,-3.05,0])


def options(scene):
    assay(scene,blocked=True); scene.add(gradient())
    scene.add(text('Toward, away, or no turn?',size=36))
    scene.add(text('PKA blocked',-3.8,2.1,RED,26))
    scene.add(VGroup(*[chip(s,GREY,size=27) for s in ['toward','away','no turn']]).arrange(RIGHT,buff=.65).move_to([0,-3.05,0]))


def antibody_label():
    return VGroup(text('anti-DCC',-4.3,1.65,PINK,28),
        Line([-3.35,1.5,0],[-1.9,1.6,0],color=PINK,stroke_width=2))


def antibody_question(scene):
    assay(scene,blocked=True,antibody=True)
    scene.add(text('What should anti-DCC block?',size=34),antibody_label(),choices2())


def repelled(scene):
    g=assay(scene,blocked=True)
    g.shift(np.array(AWAY[-1])-C)
    scene.add(ref.smooth(AWAY).set_stroke(BLUE,10).set_z_index(-2),text('repulsion',color=RED,size=36))


def both(scene,result=True):
    groups=[]
    scene.add(text('Both turns need DCC' if result else 'What happens with anti-DCC?',size=32,color=TEAL))
    for y,blocked,title in [(1.35,False,'normal'),(-1.6,True,'PKA blocked')]:
        scene.add(RoundedRectangle(width=12.3,height=2.8,corner_radius=.15,color=GREY,stroke_opacity=.45).move_to([0,y,0]))
        c=np.array([-2.9,y-.12,0]); end=np.array([1.6,y-.12,0])
        g=cone(c,.84,blocked,True)
        scene.add(g,text(title,-4.65,y+.85,RED if blocked else TEXT,26),
            text('anti-DCC',3.55,y-1.,PINK,26),
            source([4.4,y+.15,0],compact=True),
            Line([-5.8,c[1],0],c,color=BLUE,stroke_width=7).set_z_index(-2))
        # These are explicitly counterfactual direction schematics, not data.
        points=[c,c+[1.,0,0],c+[2.5,.75,0]] if not blocked else [c,c+[-.5,-.5,0],c+[-1.5,-.85,0]]
        bend=ref.smooth(points).set_stroke(GREEN if not blocked else RED,6,opacity=.85).set_z_index(-1)
        cross=Cross(stroke_color=RED,stroke_width=4).scale(.22).move_to(c+([2.2,.65,0] if not blocked else [-1.1,-.75,0]))
        scene.add(bend,cross)
        leader=Line([2.75,y-.95,0],g[-1][0].get_center(),color=PINK,stroke_width=2)
        leader.add_updater(lambda m,g=g,y=y: m.put_start_and_end_on([2.75,y-.95,0],g[-1][0].get_center()))
        scene.add(leader)
        groups.append((g,c,end))
        if result:
            g.shift(end-c); leader.update(); scene.add(Line(c,end,color=BLUE,stroke_width=7).set_z_index(-2))
    return groups


def map_group():
    tissue=ref.cord([-1.6,0,0],1.2,progenitor=True,floor=True)
    pts=[(-1.55,1.4),(-1.9,.55),(-1.7,-.65),(-.85,-1.62),(-.45,-1.92),(0,-2.03),(.65,-1.85),(1.55,-1.)]
    tissue[2].become(ref.smooth([np.array([-1.6,0,0])+1.2*np.array([x,y,0]) for x,y in pts]).set_stroke(BLUE,6))
    tags=VGroup(text('dorsal neurons',-1.6,3.15,BLUE,26),text('pial surface',-5.35,-.85,GREY,26),
        text('floor plate',-1.6,-3.2,GREY,26),text('ventricular zone',3.7,1.4,GREY,26),text('central canal',3.7,.1,GREY,26))
    links=VGroup(Line([-4.5,-.7,0],[-4.3,-.4,0],color=GREY),
        Line([2,1.4,0],[-1.02,1.1,0],color=GREY),Line([2,.1,0],[-1.6,.65,0],color=GREY))
    return VGroup(tissue,tags,links)


def retina(scene,axons=True,cue=False,laminin=False):
    # One continuous retinal section with an optic nerve opening.
    outline=VMobject(color=GREY,stroke_width=4)
    outline.set_points_as_corners([[-6,1,0],[-.7,1,0],[-.7,-3,0],[.7,-3,0],[.7,1,0],[6,1,0]])
    lower=VGroup(Line([-6,-1.8,0],[-.7,-1.8,0],color=GREY),Line([.7,-1.8,0],[6,-1.8,0],color=GREY))
    scene.add(outline,lower,text('retina in section',-3.8,3.1,GREY,30),
        text('inner surface',-4.4,2.25,GREY,26),Line([-4.4,1.95,0],[-4.4,1,0],color=GREY),
        text('exit',1.7,-3.2,GREY,26),Line([1.25,-3.,0],[.4,-2.5,0],color=GREY))
    lines=VGroup()
    for x,y in [(-1.9,1.35),(-2.9,1.85),(-3.9,1.35)]:
        lines.add(Line([-5.8,y,0],[x,y,0],color=BLUE,stroke_width=5),ref.body(np.array([x,y,0]),.22))
    lines.add(Arrow([-1.65,1.5,0],[-.2,1.5,0],color=BLUE,buff=.05))
    if axons: scene.add(lines)
    dots=VGroup(*[Dot([x,y,0],radius=.09,color=YELLOW) for x in [-.35,0,.35] for y in [.65,-.2,-1,-1.8,-2.6]])
    if cue: scene.add(dots)
    coat=VGroup(Line([-6,1.04,0],[-.7,1.04,0],color=GREY,stroke_width=12),Line([.7,1.04,0],[6,1.04,0],color=GREY,stroke_width=12))
    if laminin: scene.add(coat)
    return lines,dots,coat


class S00Title(TitleCard):
    LESSON='Netrin and DCC: One Cue, Two Answers'
    TITLE='Same Receptor, Opposite Turn'
    def construct(self):
        title=T(self.TITLE,size=50,font=TITLE_FONT); fit(title,max_w=12.)
        g=VGroup(text('BIOCHEMISTRYPEDIA',color=TEAL,size=26),T(self.LESSON,size=26,color=GREY),title,Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.2)
        self.finish()


class S01Question(Aligned):
    def construct(self):
        g=assay(self)
        self.add(text('Same receptor. Opposite turn?',size=36))
        self.at('turn toward netrin')
        self.play(Create(ref.smooth(TOWARD).set_stroke(GREY,5)),FadeIn(text('toward?',1.8,2.1,GREEN,28)),run_time=.6)
        self.at('and away')
        self.play(Create(ref.smooth(AWAY).set_stroke(GREY,5)),FadeIn(text('away?',-4.5,-2.45,RED,28)),run_time=.55)
        self.finish()


class S02Map(Aligned):
    def construct(self):
        m=map_group(); self.add(m)
        box=SurroundingRectangle(m[0][3],color=BLUE,buff=.15)
        self.at('then zoom into')
        self.play(Create(box),run_time=.25)
        dish=RoundedRectangle(width=12.1,height=5.9,corner_radius=.7,color=GREY).move_to([0,-.3,0])
        g=cone([0,-.55,0],1.65)
        self.play(FadeOut(m),Transform(box,dish),FadeIn(g),run_time=.8)
        self.add(text('culture dish',y=3.1,size=32),Line([-5.5,-.55,0],[-1.6,-.55,0],color=BLUE,stroke_width=9).set_z_index(-2))
        self.finish()


class S03Layers(Aligned):
    def construct(self):
        c=np.array([-2.,-.4,0]); self.add(cone(c,1.85))
        self.at('Receptors are one layer')
        self.play(FadeIn(text('receptors',3.5,2.2,TEAL,32)),Create(Line([2.1,2.1,0],[-.7,1.8,0],color=TEAL)),run_time=.45)
        self.at('internal state')
        self.play(FadeIn(ref.dots(c,1.85)),FadeIn(text('internal state',3.5,-.35,ORANGE,32)),Create(Line([1.9,-.35,0],[-1.2,-.35,0],color=ORANGE)),run_time=.4)
        self.add(text('cAMP, calcium...',3.5,-1.25,ORANGE,27))
        self.finish()


class S04Assay(Aligned):
    def construct(self):
        self.add(cone(),ref.smooth([[-1.2,2.6,0],[-1.2,1.1,0],C]).set_stroke(BLUE,10).set_z_index(-2),text('Turning assay',size=36))
        self.at('a fine pipette'); self.play(FadeIn(source()),run_time=.4)
        self.at('puffs short'); puff(self)
        self.at('regular pulses'); puff(self)
        self.at('beside one growth cone')
        self.play(FadeIn(gradient()),FadeIn(text('higher concentration',3.45,-2.45,YELLOW,26)),run_time=.45)
        self.add(Arrow([2.8,-2.1,0],[3.8,.65,0],color=YELLOW,buff=.1))
        self.finish()


class S05Imaging(Aligned):
    def construct(self):
        self.add(text('Time-lapse assay · schematic',size=32),source())
        start=np.array([-4.,-1.5,0]); end=np.array([1.8,.6,0]); d=end-start
        path=ref.smooth([start,[-1.7,-1.4,0],end]).set_stroke(BLUE,8)
        self.add(ghost(cone(start,.7),.4),text('time 0',-4.,-2.9,GREY,26))
        # Stacked image-frame outlines keep the time-lapse cue explicit.
        self.add(VGroup(*[RoundedRectangle(width=2.1,height=1.8,corner_radius=.1,color=GREY,stroke_opacity=.3).move_to([1.5+.15*i,.55+.13*i,0]) for i in range(3)]))
        self.at('Time lapse imaging')
        self.play(Create(path),FadeIn(cone(end,.7)),FadeIn(text('later',2.3,-1.2,BLUE,26)),run_time=.7)
        self.at('which way')
        baseline=DashedLine(start,[2.3,-1.5,0],color=GREY)
        angle=np.arctan2(d[1],d[0])
        self.play(Create(baseline),Create(Line(start,end,color=GREY,stroke_opacity=.5)),Create(Arc(radius=2.1,start_angle=0,angle=angle,arc_center=start,color=TEXT)),FadeIn(text(f'turn angle: {np.degrees(angle):.0f}°',-.8,-2.5,size=27)),run_time=.5)
        self.finish()


class S061997(Aligned):
    def construct(self):
        g=assay(self); self.add(text('1997',size=36))
        self.at('used frog spinal neurons'); self.play(FadeIn(text('frog spinal neurons',y=-3.1,size=28)),run_time=.4)
        self.at('turned toward'); travel(self,[g],TOWARD,1.1)
        self.play(FadeIn(text('attraction',-3.9,2.15,GREEN,30)),run_time=.25)
        self.finish()


class S07Lower(Aligned):
    def construct(self):
        c=np.array([0,-.35,0]); self.add(cone(c,2.15))
        camp=chip('cAMP',ORANGE,size=30).move_to([-1.25,-.4,0]); pka=chip('PKA',ORANGE,size=30).move_to([1.25,-.4,0])
        ar=Arrow([-.4,-.4,0],[.4,-.4,0],color=ORANGE,buff=.02)
        self.at('Next they blocked'); self.play(FadeIn(camp),FadeIn(pka),GrowArrow(ar),run_time=.6)
        self.at('They blocked PKA'); self.play(Create(Line(pka.get_corner(DL),pka.get_corner(UR),color=RED,stroke_width=7)),FadeIn(text('PKA blocked',y=-3.1,color=RED,size=30)),run_time=.5)
        self.at('the enzyme'); self.play(Indicate(ar,color=ORANGE),run_time=.6)
        self.finish()


class S08Predict(Aligned):
    def construct(self):
        assay(self,blocked=True); self.add(text('PKA blocked',-3.8,2.1,RED,26))
        self.at('they puffed'); puff(self); self.add(gradient())
        self.at('Toward away'); self.play(FadeIn(text('Toward, away, or no turn?',size=36)),FadeIn(VGroup(*[chip(s,GREY,size=27) for s in ['toward','away','no turn']]).arrange(RIGHT,buff=.65).move_to([0,-3.05,0])),run_time=.45)
        self.finish()


class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; options(self); self.wait(5)


class S10Reveal(Aligned):
    def construct(self):
        g=assay(self,blocked=True)
        # Hold the same label, at full opacity, throughout the turn and S11.
        self.at('turned away')
        self.add(text('repulsion',color=RED,size=36))
        travel(self,[g],AWAY,1.05)
        self.at('Attraction had become repulsion')
        self.finish()


class S11Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; repelled(self); self.wait(2.5)


class S12Predict2(Aligned):
    def construct(self):
        assay(self,blocked=True)
        self.at('add an antibody'); self.play(FadeIn(ref.caps(C,ref.DCC_A,1.35)),FadeIn(antibody_label()),run_time=.5)
        self.at('what should the antibody block'); self.play(FadeIn(text('What should anti-DCC block?',size=34)),FadeIn(choices2()),run_time=.4)
        self.finish()


class S13Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; antibody_question(self); self.wait(5)


class S14Reveal2(Aligned):
    def construct(self):
        groups=both(self,False)
        self.at('It stopped both turns')
        self.play(*[g.animate.shift(end-c) for g,c,end in groups],*[Create(Line(c,end,color=BLUE,stroke_width=7).set_z_index(-2)) for g,c,end in groups],run_time=1.4)
        self.at('Both needed'); self.play(Transform(self.mobjects[0],text('Both turns need DCC',color=TEAL,size=32)),run_time=.3)
        self.finish()


class S15Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; both(self); self.wait(2.5)


class S16Meaning(Aligned):
    def construct(self):
        c=np.array([-2.,-.35,0]); self.add(cone(c,1.7),source(),text('DCC: same receptor',y=3.15,color=TEAL,size=32),text('in this system',y=-3.1,size=28))
        sw=chip('cAMP high',ORANGE,size=28).move_to(c)
        ar=Arrow([.5,.1,0],[3.4,.9,0],color=GREEN,buff=0)
        lab=text('toward',1.8,1.3,GREEN,28)
        self.at("The cell's cyclic"); self.play(FadeIn(sw),GrowArrow(ar),FadeIn(lab),run_time=.5)
        self.at('chose the direction')
        self.play(Transform(sw,chip('cAMP low',ORANGE,size=28).move_to(c)),Transform(ar,Arrow([3.4,-.4,0],[.5,-1.8,0],color=RED,buff=0)),Transform(lab,text('away',2.2,-2.05,RED,28)),run_time=.6)
        self.add(text('PKA off',-2.,-2.5,RED,26))
        self.finish()


class S17Limit(Aligned):
    def construct(self):
        self.add(text('Netrin marks a place; the growth cone decides.',size=30),text('1   Does not set the range of the cue',y=2.2,color=GREY,size=28),text('2   Receptors plus internal state',y=1.35,color=GREY,size=30),text('3   Steering is only one netrin job',y=.5,color=GREY,size=28))
        self.at('second limit'); self.play(self.mobjects[2].animate.set_color(ORANGE),run_time=.4)
        c=np.array([-.8,-1.65,0]); g=cone(c,1.2)
        # Keep the receptor label attached as the larger cone moves away.
        label=text('DCC',-3.65,-.65,TEAL,28)
        leader=Line([-3.15,-.8,0],g[1].get_left(),color=TEAL,stroke_width=2)
        leader.add_updater(lambda m: m.put_start_and_end_on([-3.15,-.8,0],g[1].get_left()))
        self.at('A growth cone')
        self.play(FadeIn(g),FadeIn(label),Create(leader),FadeIn(Dot([4.,-1.3,0],color=YELLOW,radius=.2)),FadeIn(text('netrin',4.,-2.05,YELLOW,26)),run_time=.4)
        self.at('repelled',lead=0)
        self.play(g.animate.shift(LEFT*1.35),GrowArrow(Arrow([2.8,-2.65,0],[.1,-2.65,0],color=RED,buff=0,stroke_width=7)),FadeIn(text('away',1.45,-3.2,RED,30)),run_time=.6)
        self.finish()


class S18Scope(Aligned):
    def construct(self):
        self.add(cone([-3.5,-.3,0],1.5),text('frog growth cone',-3.5,2.8,BLUE,28),text('one system',-3.5,-2.8,size=32))
        self.at('not a rule for every')
        others=ghost(VGroup(cone([1.2,-.25,0],.9),cone([4.6,-.25,0],.9)),.6)
        self.play(FadeIn(others),FadeIn(text('other axons: not tested here',2.8,2.8,GREY,28)),FadeIn(text('?',1.2,-2.3,size=40)),FadeIn(text('?',4.6,-2.3,size=40)),run_time=.6)
        self.finish()


class S19Calcium(Aligned):
    def construct(self):
        c=np.array([-2.7,-.4,0]); self.add(cone(c,1.7),text('Calcium can change the response',size=32))
        ions=VGroup(*[Dot(c+[x,y,0],radius=.12,color=TEXT) for x,y in [(-.6,-.3),(.5,.35),(.2,-.85),(-.4,.6)]])
        self.at('Calcium can also'); self.play(FadeIn(ions),FadeIn(text('Ca2+',-2.7,-.4,size=32)),run_time=.25)
        self.add(text('Reported in frog spinal neurons',3.,1.8,GREY,26),text('cAMP/cGMP ratio',3.,.8,ORANGE,28),Arrow([3,.25,0],[3,-.5,0],color=GREY,buff=0),text('L-type calcium channels',3.,-1.,size=26))
        self.at('change the response'); self.play(Indicate(ions,color=TEXT),run_time=.4)
        self.finish()


class S20Eye(Aligned):
    def construct(self):
        lines,_,_=retina(self)
        self.at('Retinal axons run'); self.play(Indicate(lines,color=BLUE),run_time=.7)
        self.at('to the exit'); self.play(GrowArrow(Arrow([0,1.2,0],[0,-2.1,0],color=BLUE,buff=0)),run_time=.7)
        self.finish()


class S21Disk(Aligned):
    def construct(self):
        _,cues,_=retina(self)
        self.at('That exit is'); self.play(FadeIn(text('optic disk',3.8,.25,size=32)),FadeIn(text('(optic nerve head)',3.8,-.4,GREY,26)),Create(Line([2.25,.25,0],[.4,.65,0],color=GREY)),run_time=.5)
        self.at('where'); self.play(FadeIn(cues),FadeIn(text('netrin-1',3.8,-1.1,YELLOW,28)),Create(Line([2.7,-1.1,0],[.3,-1.,0],color=YELLOW)),run_time=.5)
        self.finish()


class S22Mutants(Aligned):
    def construct(self):
        retina(self,axons=False)
        # The failed exit is visible throughout the description of the mutant.
        tips=[(-.45,1.4),(.25,1.95),(-.25,2.5)]
        shafts=VGroup(*[Line([-3.,y,0],[x,y,0],color=BLUE,stroke_width=5).set_z_index(-1) for x,y in tips])
        ends=VGroup(*[ref.body(np.array([x,y,0]),.22) for x,y in tips])
        self.add(shafts,ends,text('mouse: no netrin-1 or no DCC',2.3,3.,RED,28),
            text('mutant: fail to exit',3.6,2.05,RED,26),
            text('normal: axons exit',3.7,.1,GREEN,26),Arrow([4,-.25,0],[4,-1.3,0],color=BLUE,buff=0))
        self.at('the axons still reach'); self.play(Indicate(ends,color=BLUE),run_time=.5)
        self.at('But they fail'); self.play(Indicate(ends,color=RED),run_time=.5)
        self.finish()


class S23Laminin(Aligned):
    def construct(self):
        g=assay(self); d=ref.dots(C); self.add(d,text('frog retina',size=32))
        # A top-down substrate strip covers the entire trajectory, including its tip.
        strip=RoundedRectangle(width=11.9,height=5.6,corner_radius=.2,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([0,-.45,0]).set_z_index(-5)
        self.at('laminin 1 lowers'); self.play(FadeIn(strip),FadeIn(text('laminin-1 substrate',3.7,-3.,GREY,26)),FadeOut(d),FadeIn(text('cAMP low',-3.9,2.1,ORANGE,28)),run_time=.5)
        self.at('It turns'); ghost=ref.smooth(TOWARD).set_stroke(GREEN,5,opacity=.45); self.play(Create(ghost),run_time=.4)
        self.at('into repulsion'); self.play(FadeOut(ghost),run_time=.15); travel(self,[g],AWAY,.7)
        self.add(text('repulsion',2.,-1.5,RED,30))
        self.finish()


class S24Model(Aligned):
    def construct(self):
        _,cues,coat=retina(self)
        self.at('Laminin lies'); self.play(Create(coat),FadeIn(text('laminin',-3.4,-.1,GREY,27)),Create(Line([-3.4,.25,0],[-3.4,1,0],color=GREY)),run_time=.5)
        self.at("In the author's model"); self.play(FadeIn(text('Proposed model',3.7,3.1,size=30)),run_time=.4)
        self.at('netrin repels')
        # Leave a clear central corridor for the downward axon path.
        cues=VGroup(*[Dot([x,y,0],radius=.08,color=YELLOW) for x in [-.48,.48] for y in [-.5,-1.3,-2.]])
        overlap=VGroup(*[Dot([x,1.08,0],radius=.09,color=YELLOW) for x in [-1.65,-1.3,-.95]])
        self.play(FadeIn(cues),FadeIn(overlap),FadeIn(text('netrin-1',3.7,-1.1,YELLOW,27)),Create(Line([2.6,-1.1,0],[.48,-1.3,0],color=YELLOW)),run_time=.5)
        self.at('That may help push')
        c=np.array([-.9,1.4,0]); g=ref.body(c,.25); self.add(g)
        travel(self,[g],[c,[-.35,.6,0],[0,-.8,0],[0,-2.2,0]],1.1)
        self.add(text('netrin without laminin',3.7,-2.3,YELLOW,26))
        self.finish()


class S25Takeaway(Aligned):
    def construct(self):
        self.add(text('Netrin marks a place.',y=2.9,color=YELLOW,size=38),text('Receptors plus internal state',y=1.85,size=36),text('decide the turn.',y=.95,size=36))
        c=np.array([0,-1.6,0]); self.add(cone(c,.9),text('DCC',0,-3.2,TEAL,28),Dot([5.,-.5,0],radius=.2,color=YELLOW),text('netrin',5.,-1.1,YELLOW,26))
        self.at('with its receptors'); self.play(Indicate(self.mobjects[4],color=TEAL),run_time=.4)
        self.at('in some cells'); self.play(FadeIn(text('cAMP high',-3.9,-.65,ORANGE,26)),GrowArrow(Arrow([1.5,-.7,0],[3.6,-.4,0],color=GREEN,buff=0)),FadeIn(text('toward',2.7,-1.1,GREEN,26)),FadeIn(text('cAMP low',-3.9,-1.6,ORANGE,26)),GrowArrow(Arrow([-1.5,-2.4,0],[-3.6,-2.8,0],color=RED,buff=0)),FadeIn(text('away',-4.4,-2.8,RED,26)),run_time=.5)
        self.finish()


class S26End(EndCard):
    LINE='Receptors plus internal state decide the turn.'
    def construct(self):
        line=T(self.LINE,size=38,font=TITLE_FONT); fit(line,max_w=12.)
        self.add(line,text('biochemistrypedia.com',y=-1.,color=TEAL,size=26))
        self.finish()
