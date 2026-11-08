"""Moving a Birthday: revised experimental schematics.
COLOR MAP: purple #B58CD9 progenitor/S phase; yellow #F5D547 G2/fixed;
orange #F29E4C deep fate; blue #58C4DD upper fate and host cues;
teal #3FB8C0 thymidine/graft label; grey #BAC2D0 tissue; red rejected fate.
Diagrams are qualitative experimental schematics, not measured trajectories.
"""
from bp_style import *
import numpy as np
import os
from pathlib import Path

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
GREY = '#BAC2D0'
LESSON = 'Birth Order and Fate: Temporal Identity and the Inside-Out Cortex'


class ExactTiming:
    # Shared finish() adds .4 s per beat. Here audio is the scene's clock.
    def finish(self):
        remaining = self.narration_s - self.elapsed()
        if remaining > 0.001:
            self.wait(remaining)


class TimedSpoken(ExactTiming, SpokenScene):
    def at(self, phrase, lead=0, nth=0):
        target = self.t_of(phrase, nth)
        rest = target - self.elapsed()
        if rest > .001:
            self.wait(np.ceil(rest * config.frame_rate) / config.frame_rate + 1e-6)
        # Log actual cue arrival AFTER waiting, rather than the misleading
        # pre-wait negative lateness in the shared implementation.
        with open(Path(os.environ['KX_SCRIPT']).parent / 'sync.log', 'a') as log:
            log.write(f"{os.environ['KX_SCENE_ID']} {phrase!r} target={target:.3f} actual={self.elapsed():.3f} delta={self.elapsed()-target:+.3f}\n")


def label(s, x=0, y=0, size=34, color=TEXT):
    return T(s, size=size, color=color, line_spacing=1.15).move_to([x, y, 0])


def arrow(a, b, color=BLUE):
    return Arrow(a, b, buff=.04, color=color, stroke_width=7, tip_length=.24)


def cell(x=0, y=0, r=.65, color=PURPLE, tag=False):
    c = Circle(radius=r, color=color, stroke_width=5, fill_color=color, fill_opacity=.22).move_to([x,y,0])
    return VGroup(c, Dot([x,y,0], radius=r*.24, color=TEAL)) if tag else c


def neuron(x, y, color=BLUE, tag=True):
    return VGroup(cell(x,y,.25,color,tag),
                  Line([x,y+.25,0],[x,y+.6,0],color=color,stroke_width=4),
                  Line([x,y-.25,0],[x,y-.6,0],color=color,stroke_width=4))


def calendar(x, y, txt='birthday', col=TEAL, w=3.2, h=2.8):
    box=RoundedRectangle(width=w,height=h,corner_radius=.16,color=col,fill_color=col,fill_opacity=.12).move_to([x,y,0])
    line=Line([x-w/2,y+h*.23,0],[x+w/2,y+h*.23,0],color=col,stroke_width=4)
    rings=VGroup(*[Line([x+dx,y+h*.42,0],[x+dx,y+h*.6,0],color=col,stroke_width=6) for dx in [-w*.25,w*.25]])
    return VGroup(box,line,rings,label(txt,x,y-.25,32,col))


def divider():
    return Line([0,-2.9,0],[0,2.8,0],color=GREY,stroke_opacity=.35,stroke_width=2)


def tissue(x=3, y=.2):
    g=VGroup()
    for dx,dy in [(-2.25,1.7),(2.25,1.7),(0,-2.1)]:
        patch=RoundedRectangle(width=1.05,height=.65,corner_radius=.18,color=BLUE,fill_color=BLUE,fill_opacity=.28).move_to([x+dx,y+dy,0])
        g.add(patch)
    return g


def environment(x=3,y=.2):
    return VGroup(tissue(x,y),
        arrow([x-1.75,y+1.45,0],[x-.85,y+.6,0]),
        arrow([x+1.75,y+1.45,0],[x+.85,y+.6,0]),
        arrow([x,y-1.75,0],[x,y-.95,0]))


def split(ghost=False, clock=True):
    a=cell(-3.2,.2,1.45); b=cell(3.2,.2,1.45)
    left=VGroup(a,label('Own schedule',-3.2,-2.55,36,PURPLE))
    if clock:left.add(calendar(-3.2,.2,'',PURPLE,1.6,1.55))
    right=VGroup(b,label('Surroundings',3.2,-2.55,36,BLUE))
    if ghost:right.set_opacity(.22)
    return VGroup(divider(),left,right)


def cortex(title='newborn host', x=0, top=2.55, bottom=-3.05, width=10, deep_op=.14):
    """Separated bands: action left, all anatomical labels in the right column."""
    mid=(top+bottom)/2
    box=Rectangle(width=width,height=top-bottom,color=GREY,stroke_width=2).move_to([x,mid,0])
    g=VGroup(box)
    for yy,hh,col,txt,op in [(top-1.05,1.15,BLUE,'layers 2 / 3',.14),(bottom+2.5,1.1,ORANGE,'deep layers',deep_op),(bottom+.6,1.05,PURPLE,'ventricular zone',.14)]:
        g.add(Rectangle(width=width-.04,height=hh,stroke_width=0,fill_color=col,fill_opacity=op).move_to([x,yy,0]),label(txt,x+width*.18,yy,32,col))
    g.add(label(title,x,top+.48,34))
    return g


def steps(active=None, y=3.05):
    g=VGroup(arrow([-6.3,y,0],[6.3,y,0],GREY))
    for i,name in enumerate(['Pulse','Harvest','Graft','Read']):
        col=YELLOW if i==active else GREY
        box=RoundedRectangle(width=2.6,height=.95,corner_radius=.12,color=col,fill_color=BG,fill_opacity=1).move_to([-4.65+3.1*i,y,0])
        g.add(VGroup(box,label(name,-4.65+3.1*i,y,32,col)))
    return g


def embryo(x=1.5,y=-.35):
    e=Ellipse(width=4.3,height=4.65,color=GREY,stroke_width=3).move_to([x,y,0])
    cs=VGroup(*[cell(x+dx,y+dy,.48,PURPLE) for dx,dy in [(-.9,.9),(.8,.9),(-.9,-.8),(.8,-.8)]])
    return VGroup(e,cs,label('donor embryo',x,y+2.65,34),label('early: deep-layer stage',x,y-2.65,32,ORANGE))


ROW=[1.6,-.6]
LEG=-2.35


def comparison(first=False, second=False, heading='Predict: where do the daughters settle?'):
    g=VGroup(label(heading,0,3.4,38))
    for idx,y in enumerate(ROW):
        col=PURPLE if idx==0 else YELLOW
        g.add(RoundedRectangle(width=12.9,height=2.0,corner_radius=.15,color=GREY,stroke_opacity=.55).move_to([0,y,0]),
              label('Moved in S phase' if idx==0 else 'Moved late in cycle',-3.65,y+.42,34,col))
        # These are neutral, empty anatomical answer slots until the reveal.
        for yy,cc,txt in [(y+.5,BLUE,'upper 2 / 3'),(y-.5,ORANGE,'deep layers')]:
            g.add(Rectangle(width=6.0,height=.85,color=cc,stroke_opacity=.7,fill_color=cc,fill_opacity=.08).move_to([3.2,yy,0]),label(txt,4.6,yy,32,cc))
        if (idx==0 and first) or (idx==1 and second):
            yy=y+.5 if idx==0 else y-.5
            cc=BLUE if idx==0 else ORANGE
            g.add(cell(1.3,yy,.24,cc,True),label('mostly upper' if idx==0 else 'mostly deep',-3.65,y-.45,34,cc))
            if idx==0:g.add(cell(2.35,yy,.24,BLUE))
    g.add(Dot([-4.65,LEG,0],radius=.12,color=TEAL),label('graft label',-3.35,LEG,32,TEAL),cell(-.3,LEG,.16,BLUE),label('host neuron',1.3,LEG,32,BLUE))
    return g


def reverse_question():
    g=VGroup(label('Predict: what do they make?',0,3.5,38),
        cell(-4.3,1.2,1.1,YELLOW,True),label('late progenitor',-4.3,-.3,36,YELLOW),
        arrow([-2.7,1.2,0],[-.6,1.2,0],YELLOW),
        RoundedRectangle(width=6.4,height=3.7,corner_radius=.15,color=GREY).move_to([3.3,1.1,0]),
        label('young host',3.3,2.3,38),label('(younger than the donor)',3.3,1.6,32),
        Rectangle(width=6.0,height=1.2,color=ORANGE,fill_color=ORANGE,fill_opacity=.25).move_to([3.3,.2,0]),label('deep-layer cues',3.3,.2,36,ORANGE))
    for x,txt,co in [(-3.4,'upper layers',BLUE),(3.4,'deep layers',ORANGE)]:
        g.add(RoundedRectangle(width=6.2,height=1.2,corner_radius=.12,color=co).move_to([x,-1.85,0]),label('○  '+txt,x,-1.85,38,co))
    return g


def countdown(scene, build, cx=0, cy=-3.4, r=.48):
    scene.camera.background_color=BG
    scene.add(build())
    # Intentional 5 s thinking interval: a shrinking ring with a large digit, question in place.
    track=Circle(radius=r,color=GREY,stroke_width=8,stroke_opacity=.35).move_to([cx,cy,0])
    def arc(frac):
        return Arc(radius=r,start_angle=PI/2,angle=max(2*PI*frac,1e-3),arc_center=[cx,cy,0],color=YELLOW,stroke_width=10)
    ring=arc(1.0)
    scene.add(track,ring)
    for n in range(5,0,-1):
        tick=label(str(n),cx,cy,36,YELLOW)
        scene.add(tick)
        scene.play(UpdateFromAlphaFunc(ring,lambda m,al,n=n:m.become(arc((n-al)/5))),run_time=1,rate_func=linear)
        scene.remove(tick)


def kit():
    # One filled silhouette, enlarged, with ear and tail so it reads as a ferret.
    pts=[[-5.9,-.65,0],[-5.3,-.4,0],[-4.85,.25,0],[-4,.6,0],[-3.2,.55,0],[-2.65,1.05,0],[-2.5,1.55,0],[-2.1,1.15,0],[-1.45,.9,0],[-1.05,.4,0],[-1.55,.03,0],[-2.3,-.05,0],[-2.7,-.55,0],[-3.6,-.9,0],[-4.8,-.85,0]]
    p=Polygon(*pts,color=GREY,fill_color=GREY,fill_opacity=.65,stroke_width=3)
    tail=CubicBezier([-5.8,-.6,0],[-6.2,-.9,0],[-6.3,-.1,0],[-6.4,.2,0],color=GREY,stroke_width=10)
    body=VGroup(tail,p,Dot([-1.9,.72,0],radius=.08,color=BG))
    body.scale(1.2,about_point=[-3.5,.3,0]).shift(RIGHT*.45+UP*.15)
    return VGroup(body,label('newborn ferret',-3.4,-2.0,36),label('after birth',-3.4,-2.7,32,TEAL))


NX=[.8,1.8,2.8]


def ferret_cortex(done=False):
    g=VGroup(kit(),cortex('visual cortex',3.6,2.55,-3.05,6.6))
    # Anatomical text stays in the right of this panel; cell action on the left.
    if done:g.add(neuron(NX[1],1.5,BLUE,False),cell(NX[0],-2.45,.3))
    return g


MX=1.2


def menu(lost=False):
    box=RoundedRectangle(width=7.8,height=5.8,corner_radius=.2,color=PURPLE,fill_color=PURPLE,fill_opacity=.06)
    g=VGroup(box,label('Late progenitor: fate menu',0,2.05,36,PURPLE),label('deep layers',-.4,.55,38,ORANGE),label('upper layers',0,-1.15,38,BLUE))
    if lost:
        g[2].set_color(GREY).set_opacity(.75)
        g.add(chip('lost',ORANGE,size=32).move_to([2.55,.55,0]))
    return g.shift(RIGHT*MX)


class S00Title(ExactTiming,TitleCard):
    LESSON=LESSON
    TITLE='Moving a Birthday'
    def construct(self):
        self.add(VGroup(label('BIOCHEMISTRYPEDIA',size=28,color=TEAL),label('Birth Order and Fate:\nTemporal Identity and the Inside-Out Cortex',size=30),T(self.TITLE,size=54,font=TITLE_FONT),Line(LEFT*1.5,RIGHT*1.5,color=GOLD)).arrange(DOWN,buff=.6))
        self.finish()


class S01Q(TimedSpoken):
    def construct(self):
        self.add(neuron(-3,.45,BLUE,False).scale(3),calendar(2.5,.45),label('A birthday predicts a layer',0,3,36))
        self.at('but is the')
        self.play(FadeIn(label('Cause or record?',0,-2.7,44,YELLOW)),run_time=.45)
        self.finish()


class S02Two(TimedSpoken):
    def construct(self):
        self.add(split(True,False),label('Two explanations',0,3.1,36))
        self.at('carry its own')
        self.play(FadeIn(calendar(-3.2,.2,'',PURPLE,1.6,1.55)),run_time=.6)
        self.finish()


class S03Two2(TimedSpoken):
    def construct(self):
        self.add(split(),label('Two explanations',0,3.1,36),tissue(3.2))
        self.at('or the surroundings')
        env=environment(3.2)
        self.play(*[GrowArrow(a) for a in list(env)[1:]],run_time=.65)
        self.finish()


class S04Mcc(TimedSpoken):
    def construct(self):
        self.add(label('McConnell and Kaznowski · 1991',0,3.15,36),divider(),cell(-3.2,.2,1.45),calendar(-3.2,.2,'',PURPLE,1.6,1.55),cell(3.2,.2,1.45),environment(3.2),label('donor: supplies the cells',-3.2,-2.55,32,PURPLE),label('host: receives the graft',3.2,-2.55,32,BLUE))
        self.at('set the two')
        self.play(GrowArrow(arrow([-1.4,.2,0],[1.4,.2,0],YELLOW)),run_time=.65)
        self.at('in ferrets')
        self.play(FadeIn(label('Ferret cortex',0,-3.3,30)),run_time=.3)
        self.finish()


class S05Why(TimedSpoken):
    def construct(self):
        self.add(ferret_cortex())
        p=cell(1.4,-2.45,.34); self.add(p)
        self.at('keeps making neurons')
        self.play(p.animate.stretch(1.5,0),run_time=.3)
        a=cell(NX[0],-2.45,.3); b=cell(NX[1],-2.45,.3)
        self.play(ReplacementTransform(p,VGroup(a,b)),run_time=.55)
        n=neuron(NX[1],-2.45,BLUE,False)
        self.play(ReplacementTransform(b,n),run_time=.2)
        self.play(n.animate.set_y(1.5),run_time=1.0)
        self.finish()


class S06Why2(TimedSpoken):
    def construct(self):
        self.add(ferret_cortex(True))
        self.at('a newborn kit')
        self.play(FadeIn(label('newborn host',-3.4,3.2,38,BLUE)),run_time=.35)
        self.at('host cortex')
        self.play(FadeIn(label('(older than the donor)',-3.4,2.6,32)),run_time=.35)
        self.at('at the upper')
        self.play(Indicate(self.mobjects[0][1][1],color=BLUE,scale_factor=1.03),run_time=.5)
        late=VGroup(neuron(NX[0],-2.45,BLUE,False),neuron(NX[2],-2.45,BLUE,False))
        self.play(FadeIn(late),run_time=.2)
        self.play(late[0].animate.set_y(1.5),late[1].animate.set_y(1.5),run_time=.9)
        self.finish()


class S07Steps(TimedSpoken):
    def construct(self):
        self.add(label('Four steps: follow the labeled cells',0,2.7,38))
        # A tall timeline, with grey named placeholders visible from its first frame.
        g=steps(y=.2)
        for obj in list(g)[1:]:obj[0].stretch(2.8,1)
        self.add(g,label('label → harvest → move → locate',0,-2.4,34,GREY))
        self.at('they ran the')
        self.play(Create(g[0]),run_time=.7)
        self.finish()


class S08S1(TimedSpoken):
    def construct(self):
        e=embryo(2,-.45)
        self.add(steps(0),e[0],e[1],label('donor embryo',2,2.1,34))
        self.at('pulse a donor')
        tag=label('tritiated\nthymidine',-3.75,.6,36,TEAL)
        a=arrow([-2.2,.6,0],[-.25,.6,0],TEAL)
        self.play(FadeIn(tag),GrowArrow(a),run_time=.65)
        self.at('a stage that')
        self.play(FadeIn(e[3]),run_time=.45)
        self.at('only cells in')
        dots=VGroup(*[Dot(e[1][i].get_center(),radius=.15,color=TEAL) for i in [0,3]])
        self.play(FadeIn(dots),FadeIn(label('S phase',-3.75,-1.7,34,PURPLE)),run_time=.5)
        self.finish()


class S09S2(TimedSpoken):
    def construct(self):
        self.add(steps(1))
        e=embryo(-4,-.4)
        # Harvest context, then branch into two physically different cycle states.
        e.remove(e[2],e[3]); e.scale(.52).move_to([-4,-.3,0]); self.add(e,label('donor\nembryo',-4,1.75,30))
        p=cell(-4,-.3,.55,PURPLE,True)
        self.at('harvest the cells')
        self.add(p); self.play(p.animate.move_to([-1.9,-.3,0]),run_time=.7)
        self.at('soon after the pulse')
        self.add(Line([2.7,2.1,0],[3.45,2.1,0],color=PURPLE,stroke_width=6))
        a=cell(1.15,1.05,1.05,PURPLE,True)
        self.play(TransformFromCopy(p,a),GrowArrow(arrow([-1.2,.15,0],[-.05,1.05,0],PURPLE)),FadeIn(label('short delay\nS phase',4,1.05,34,PURPLE)),run_time=.65)
        self.at('or later')
        b=cell(1.15,-1.65,1.05,YELLOW,True)
        self.play(TransformFromCopy(p,b),GrowArrow(arrow([-1.2,-.7,0],[-.05,-1.65,0],YELLOW)),FadeIn(label('longer delay\nG2',4,-1.65,34,YELLOW)),run_time=.65)
        self.add(Line([2.7,-2.8,0],[5.3,-2.8,0],color=YELLOW,stroke_width=6))
        self.finish()


class S10S3(TimedSpoken):
    def construct(self):
        bar=steps(2); c=cortex('newborn host',1.2,1.55,-3.1,9.1)
        self.add(bar,c)
        p=cell(-4.8,-1.9,.55,PURPLE,True); self.add(p)
        self.at('them into a')
        graft_arrow=arrow([-4,-1.9,0],[-1.7,-2.45,0],YELLOW)
        self.play(GrowArrow(graft_arrow),p.animate.move_to([-1,-2.45,0]),run_time=.9)
        self.at('fourth find')
        self.play(Transform(bar,steps(3)),FadeOut(p),FadeOut(graft_arrow),run_time=.3)
        # Readout method, deliberately no neuron or selected destination.
        lens=VGroup(Circle(radius=.65,color=TEAL,stroke_width=5).move_to([-1,.4,0]),Line([-.5,-.1,0],[.1,-.7,0],color=TEAL,stroke_width=7))
        self.play(FadeIn(lens),run_time=.3)
        self.play(lens.animate.shift(DOWN*1.5),run_time=.7)
        self.add(label('Find labeled neurons; note layer',0,-3.55,32,TEAL))
        self.finish()


class S11Key(TimedSpoken):
    def construct(self):
        self.add(label('Final cycle inside the newborn host',0,3.2,36))
        zone=RoundedRectangle(width=12,height=4.4,corner_radius=.15,color=GREY,fill_color=PURPLE,fill_opacity=.12).move_to([0,-.55,0])
        self.add(zone,label('ventricular zone',3.65,-2.3,34,PURPLE),label('newborn host',3.65,1,34,BLUE))
        p=cell(-4.7,-.5,.8,PURPLE,True); self.add(p,label('S-phase graft',-4.3,2,32,PURPLE))
        self.at('a cell grafted')
        self.play(GrowArrow(arrow([-4,1.5,0],[-3.35,.4,0],PURPLE)),p.animate.move_to([-2,-.5,0]),run_time=.85)
        self.at('finishes its cycle')
        seq=VGroup(chip('S',PURPLE,size=34),label('→',size=34),chip('G2',YELLOW,size=34),label('→',size=34),chip('mitosis',YELLOW,size=34)).arrange(RIGHT,buff=.3).move_to([1.5,2,0])
        mini=VGroup(Arc(radius=.72,start_angle=PI,angle=-PI,color=PURPLE,stroke_width=8),Arc(radius=.72,start_angle=0,angle=-PI*.8,color=YELLOW,stroke_width=8),Arc(radius=.72,start_angle=-PI*.8,angle=-PI*.2,color=GREY,stroke_width=8)).move_to([3.7,-.45,0])
        self.play(FadeIn(seq[0]),FadeIn(mini),run_time=.25)
        self.play(FadeIn(seq[1]),FadeIn(seq[2]),p[0].animate.set_color(YELLOW),run_time=.4)
        self.play(FadeIn(seq[3]),FadeIn(seq[4]),p.animate.stretch(1.35,0),run_time=.5)
        self.at('so its daughter')
        daughters=VGroup(cell(-2.7,-.5,.62,PURPLE,True),cell(-.9,-.5,.62,PURPLE,True))
        self.play(ReplacementTransform(p,daughters),run_time=.55)
        self.play(FadeIn(label('born in the host',-1.8,-2.2,34,TEAL)),run_time=.25)
        self.finish()


class S12Predict(TimedSpoken):
    def construct(self):
        q=comparison(); self.add(q)
        self.at('moved in s phase')
        self.play(Indicate(q[2],scale_factor=1.03),run_time=.4)
        self.at('and if they')
        self.play(Indicate(q[8],scale_factor=1.03),run_time=.4)
        self.finish()


class S13Pause(Scene):
    def construct(self):countdown(self,comparison)


class S14Reveal(TimedSpoken):
    def construct(self):
        q=comparison(); self.add(q)
        self.at('mostly settled')
        p=cell(-.3,ROW[0],.24,BLUE,True); self.add(p)
        self.play(p.animate.move_to([1.3,ROW[0]+.5,0]),FadeIn(label('mostly upper',-3.65,ROW[0]-.45,34,BLUE)),run_time=.85)
        self.at("like the host's")
        self.play(FadeIn(cell(2.35,ROW[0]+.5,.24,BLUE)),run_time=.4)
        self.finish()


class S15Reveal2(TimedSpoken):
    def construct(self):
        self.add(cortex(),label('Final cycle in the newborn host',0,-3.6,32))
        p=cell(-1.8,-2.45,.53,PURPLE,True)
        cycling=VGroup(label('cycling graft',-1.8,-1.25,32,PURPLE),Line([-1.8,-1.55,0],[-1.8,-1.88,0],color=PURPLE,stroke_width=3))
        self.add(p,cycling)
        self.at('they finished')
        self.play(Indicate(p,color=PURPLE,scale_factor=1.12),run_time=.5)
        self.at('its cues could')
        cues=VGroup(arrow([-4.5,-1.75,0],[-2.4,-2.3,0]),arrow([.8,-1.75,0],[-1.2,-2.3,0]))
        caption=VGroup(label('host cues, partly known',-2,0,32,BLUE),Line([-3,-.35,0],[-3.6,-1.8,0],color=BLUE,stroke_width=3))
        self.play(*[GrowArrow(a) for a in cues],FadeIn(caption),run_time=.45)
        self.at('before they divided')
        daughters=VGroup(neuron(-2.35,-2.45,BLUE),cell(-1,-2.45,.32,PURPLE,True))
        self.play(p[0].animate.set_color(YELLOW),run_time=.15)
        self.play(FadeOut(cues),FadeOut(caption),FadeOut(cycling),ReplacementTransform(p,daughters),run_time=.3)
        self.play(daughters[0].animate.set_y(1.5),run_time=.55)
        self.add(label('graft daughter',-3.25,.25,32,TEAL),Line([-3.25,.6,0],[-2.55,1.15,0],color=TEAL,stroke_width=3))
        self.finish()


class S16Reveal3(TimedSpoken):
    def construct(self):
        self.add(comparison(True))
        self.at('mostly settled')
        p=cell(-.3,ROW[1],.24,ORANGE,True); self.add(p)
        self.play(p.animate.move_to([1.3,ROW[1]-.5,0]),FadeIn(label('mostly deep',-3.65,ROW[1]-.45,34,ORANGE)),run_time=.75)
        self.at('fixed before the move')
        self.play(FadeIn(label('fixed before the move',0,-3.3,36,YELLOW)),run_time=.35)
        self.finish()


class S17Hold(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(comparison(True,True),label('fixed before the move',0,-3.3,36,YELLOW)); self.wait(2.5)


class S18Commit(TimedSpoken):
    def construct(self):
        center=np.array([0,.25,0]); r=2.35
        # Clockwise schematic only: arc spans are NOT phase-duration data.
        s=Arc(radius=r,start_angle=PI,angle=-PI*.95,arc_center=center,color=PURPLE,stroke_width=24)
        g=Arc(radius=r,start_angle=PI*.05,angle=-PI*.82,arc_center=center,color=YELLOW,stroke_width=24)
        m=Arc(radius=r,start_angle=-PI*.77,angle=-PI*.23,arc_center=center,color=GREY,stroke_width=24)
        direction=CurvedArrow([-1.15,1.45,0],[1.15,1.45,0],angle=-PI*.65,color=GREY,stroke_width=5)
        self.add(s,g,m,direction,label('Final cell cycle',0,3.25,36),label('S phase',-3.9,1.65,36,PURPLE),label('G2',3.65,-.25,36,YELLOW),label('division',-3.8,-1.95,32))
        self.add(Line([-2.65,1.65,0],[-1.8,1.75,0],color=PURPLE,stroke_width=3),Line([2.5,-.25,0],[2.85,-.25,0],color=YELLOW,stroke_width=3))
        self.add(Line([-2.65,-1.95,0],[-1.95,-1.15,0],color=GREY,stroke_width=3))
        self.at('still responds')
        self.play(FadeIn(label('host-responsive',-4.4,.75,32,PURPLE)),Create(Line([-2.45,.75,0],[-2.15,.95,0],color=PURPLE,stroke_width=3)),run_time=.45)
        self.at('fixed by a later stage')
        soft=VGroup(*[Arc(radius=r,start_angle=.36-i*.04,angle=-.055,arc_center=center,color=interpolate_color(ManimColor(PURPLE),ManimColor(YELLOW),i/14),stroke_width=30) for i in range(15)])
        self.play(FadeIn(soft),Create(Line([2,-1.15,0],[2.55,-1.15,0],color=YELLOW,stroke_width=3)),FadeIn(label('laminar fate fixed',4.6,-1.15,32,YELLOW)),FadeIn(label('before division',4.6,-1.8,32,YELLOW)),run_time=.55)
        self.at('the exact moment')
        self.play(FadeIn(label('Inferred loss of laminar responsiveness;\nprecise timing unresolved',0,-3.1,32,GREY)),run_time=.45)
        self.finish()


class S19Cues(TimedSpoken):
    def construct(self):
        CUE='#8FE3FF'
        self.add(label('Progenitor state',0,3.5,40))
        # S-phase outcome row with a small layer glyph.
        gy=-2.95
        glyph=VGroup(Rectangle(width=1.5,height=.4,stroke_width=0,fill_color=BLUE,fill_opacity=.4).move_to([1.2,gy+.2,0]),
                     Rectangle(width=1.5,height=.4,stroke_width=0,fill_color=ORANGE,fill_opacity=.3).move_to([1.2,gy-.2,0]),
                     Rectangle(width=1.5,height=.8,color=GREY,stroke_width=2).move_to([1.2,gy,0]),
                     cell(1.2,gy+.2,.13,BLUE,True))
        thumb=VGroup(RoundedRectangle(width=13.2,height=1.3,corner_radius=.12,color=PURPLE).move_to([0,gy,0]),
                     label('S-phase graft',-4.6,gy,32,PURPLE),arrow([-2.5,gy,0],[-.1,gy,0],CUE),glyph,label('mostly layers 2 / 3',4.2,gy,30,BLUE))
        self.add(thumb)
        clockbox=RoundedRectangle(width=4.2,height=4.1,corner_radius=.18,color=PURPLE,fill_color=PURPLE,fill_opacity=.14,stroke_width=6).move_to([-4.6,.55,0])
        clock=VGroup(Circle(radius=1.3,color=PURPLE,stroke_width=8).move_to([-4.6,.95,0]),Line([-4.6,.95,0],[-4.6,1.95,0],color=PURPLE,stroke_width=10),Line([-4.6,.95,0],[-3.8,.95,0],color=PURPLE,stroke_width=10))
        self.add(clockbox,clock,label('sealed clock',-4.6,-.95,36,PURPLE),label('+',-2.0,.55,56))
        self.at('cues count as')
        c=cell(-.2,.5,1.0)
        arrows=VGroup(*[Arrow(a,b,buff=.03,color=CUE,stroke_width=16,tip_length=.38,max_tip_length_to_length_ratio=.5) for a,b in [([-1.6,2.55,0],[-.75,1.2,0]),([1.2,2.55,0],[.35,1.2,0]),([-.2,-1.75,0],[-.2,-.65,0])]])
        self.play(FadeIn(c),*[GrowArrow(a) for a in arrows],FadeIn(label('host cues',1.6,-1.2,36,CUE)),FadeIn(label('=',1.9,.5,56)),FadeIn(label('progenitor\nstate',4.4,.5,44)),run_time=.6)
        self.at('not only a clock')
        self.play(Indicate(clockbox,scale_factor=1.04),Indicate(arrows,scale_factor=1.04),run_time=.6)
        self.finish()


class S20Back(TimedSpoken):
    def construct(self):
        self.add(label('Reverse the age contrast',0,3,38))
        a=VGroup(cell(-3.3,.2,1.15,PURPLE,True),label('early donor',-3.3,-1.65,36,PURPLE))
        b=VGroup(RoundedRectangle(width=4.5,height=3,color=BLUE).move_to([3.2,.2,0]),label('newborn host',3.2,.2,34,BLUE))
        self.add(a,b,arrow([-1.7,.2,0],[.7,.2,0],YELLOW))
        self.at('the other way')
        aa=VGroup(cell(-3.3,.2,1.15,YELLOW,True),label('late donor',-3.3,-1.65,36,YELLOW))
        bb=VGroup(RoundedRectangle(width=4.5,height=3,color=ORANGE).move_to([3.2,.2,0]),label('young host',3.2,.2,34,ORANGE))
        self.play(a.animate.shift(UP*.5),b.animate.shift(DOWN*.5),run_time=.12)
        aa.shift(UP*.5); bb.shift(DOWN*.5)
        self.play(FadeOut(a),FadeOut(b),run_time=.1)
        self.play(FadeIn(aa),FadeIn(bb),run_time=.2)
        self.finish()


class S21Predict2(TimedSpoken):
    def construct(self):
        q=reverse_question()
        self.add(*list(q)[:7],q[9],q[11])
        self.at('which offers')
        self.play(FadeIn(q[7]),FadeIn(q[8]),run_time=.45)
        self.at('what do they')
        self.play(FadeIn(q[10]),FadeIn(q[12]),run_time=.4)
        self.finish()


class S22Pause(Scene):
    def construct(self):countdown(self,reverse_question)


class S23Reveal4(TimedSpoken):
    def construct(self):
        self.add(label('Frantz and McConnell · 1996',0,3.5,38),cortex('young host',2.4,2.05,-3.1,8.6,deep_op=.4))
        # Host premise remains visible, including the expected deep destination.
        self.add(label('deep-layer cues',-4.65,.7,34,ORANGE),arrow([-4.65,.15,0],[-1.4,-.5,0],ORANGE),Circle(radius=.32,color=ORANGE,stroke_opacity=.6).move_to([0,-.6,0]),label('expected: deep layers',2.4,-3.6,32,ORANGE))
        p=cell(-4.65,-1.55,.65,YELLOW,True)
        donor=label('late donor',-4.65,-2.65,34,YELLOW)
        self.add(p,donor)
        self.at('the late progenitors')
        move_arrow=arrow([-3.8,-1.55,0],[-1.0,-2.5,0],YELLOW)
        self.play(FadeOut(donor),GrowArrow(move_arrow),p.animate.move_to([0,-2.5,0]),run_time=.55)
        self.at('still made')
        n=neuron(0,-2.5,BLUE)
        self.play(ReplacementTransform(p,n),run_time=.2)
        self.play(n.animate.set_y(1),FadeOut(move_arrow),run_time=.65)
        self.play(FadeIn(label('still upper',1.2,1.0,30,'#8FE3FF')),run_time=.25)
        self.finish()


class S24Menu(TimedSpoken):
    def construct(self):
        m=menu(); self.add(m)
        self.at('they had lost')
        full=menu(True)
        self.play(m[2].animate.set_color(GREY).set_opacity(.75),FadeIn(full[4]),run_time=.55)
        self.at('could not answer')
        x0=-2.9
        cue=arrow([-5.6,.55,0],[x0,.55,0],ORANGE)
        self.add(label('young host\ncues',-5.0,1.9,34,ORANGE))
        self.play(GrowArrow(cue),run_time=.35)
        rebound=arrow([x0,.55,0],[-5.6,-.8,0],ORANGE)
        self.play(FadeOut(cue),run_time=.15)
        self.play(GrowArrow(rebound),run_time=.3)
        self.finish()


class S25Hold(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(menu(True),label('young host\ncues',-5.0,1.9,34,ORANGE),arrow([-2.9,.55,0],[-5.6,-.8,0],ORANGE)); self.wait(2.5)


class S26Mouse(TimedSpoken):
    def construct(self):
        self.add(divider(),label('Ferret experiments',-3.25,3.15,36),label('ferret: competence narrows',-3.25,2.35,30,PURPLE),cell(-4.8,.25,.75,PURPLE),cell(-1.75,.25,.75,YELLOW),label('earlier',-4.8,1.55,32,PURPLE),label('later',-1.75,1.55,32,YELLOW))
        self.at('narrowed one way')
        self.play(GrowArrow(arrow([-3.95,.25,0],[-2.6,.25,0],PURPLE)),run_time=.5)
        self.at('mouse study found')
        panel=VGroup(label('2019 mouse study',3.25,3.15,36),label('some progenitors (not all)',3.25,2.35,30,TEAL),cell(1.75,.25,.75,PURPLE),cell(4.8,.25,.75,YELLOW),label('earlier',1.75,1.55,32,PURPLE),label('later',4.8,1.55,32,YELLOW))
        self.play(FadeIn(panel),run_time=.55)
        self.at('moved into a younger')
        self.play(FadeIn(label('younger host',3.25,-3.55,32,BLUE)),run_time=.35)
        self.at('can return to')
        ret=CurvedArrow([4.8,-.6,0],[1.75,-.6,0],angle=-PI,color=TEAL,stroke_width=8,tip_length=.3)
        self.play(Create(ret),FadeIn(label('return to earlier states',3.25,-2.7,30,TEAL)),run_time=.65)
        self.finish()


class S27Take(TimedSpoken):
    def construct(self):
        box=RoundedRectangle(width=13.2,height=7.3,corner_radius=.2,color=TEAL,fill_color=TEAL,fill_opacity=.04)
        self.add(box,label('The takeaway',0,3.0,34,TEAL))
        rows=['A record, not a cause','Schedule and surroundings both count','Host cues count until laminar fate is fixed','Then the menu usually shortens']
        ys=[1.75,.45,-.85,-2.15]
        rules=VGroup(*[Line([-5.9,y,0],[5.9,y,0],color=GREY,stroke_opacity=.3) for y in [1.1,-.2,-1.5]])
        self.add(rules)
        cues=['birthday is a record','both','host cues count','menu usually shortens']
        for text,y,cue in zip(rows,ys,cues):
            self.at(cue)
            t=label(text,0,y,44,TEAL if y==ys[0] else TEXT).align_to(box,LEFT).shift(RIGHT*.8)
            self.play(FadeIn(t,shift=UP*.08),run_time=.4)
        self.finish()


class S28End(ExactTiming,EndCard):
    LINE='The birthday is a record.'
    def construct(self):
        line=T(self.LINE,size=42,font=TITLE_FONT)
        sub=label('biochemistrypedia.com',size=30,color=TEAL)
        VGroup(line,sub).arrange(DOWN,buff=.55)
        self.add(line,sub)
        self.finish()
