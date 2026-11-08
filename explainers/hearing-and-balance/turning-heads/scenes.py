"""Turning Heads, Steady Eyes — word-timed teaching schematics.

COLOR MAP (from ../scenes.old.py; TASK limits edits to this file):
YELLOW sound / moving stimulus; BLUE membranes, canal walls and relay boxes;
ORANGE high frequency; PURPLE low frequency; TEAL hair cells;
GREEN excitation / active output; GOLD stiffness / heavy load;
GREY outlines, labels and de-emphasis; RED inhibition / loss.
All plotted traces use the lesson's approximate rate–velocity relationship:
tau * dr/dt + (r - r_rest) = k * velocity(t), with illustrative tau = 0.22 s.
Values and spike counts are normalized illustrations, not recordings.
Anatomical curves are geometric schematics, not molecular structures.
"""
import numpy as np
from bp_style import *

ORANGE = '#F29E4C'
PURPLE = '#B58CD9'


def label(s, x=0, y=3.05, color=TEXT, size=30):
    return T(s, size=size, color=color).move_to([x, y, 0])


# Reused staircase cell model from the earlier film.
def haircell(h=1.3, w=.7, color=TEAL, sw=4):
    body = RoundedRectangle(corner_radius=w*.42, width=w, height=h,
        stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=.3).move_to([0,h/2,0])
    k=max(.34,h*.7)
    bundle=VGroup(*[Line([dx*w,h,0],[dx*w,h+k*f,0],color=color,stroke_width=sw)
        for dx,f in ((-.30,.45),(0,.72),(.30,1))])
    g=VGroup(body,bundle)
    g.body,g.bundle=body,bundle
    return g


def canal(x=0,y=0,r=2.05):
    wall=Circle(r,color=BLUE,stroke_width=24).move_to([x,y,0])
    lumen=Circle(r,color=BG,stroke_width=13).move_to([x,y,0])
    swelling=Ellipse(width=1.35,height=.9,color=BLUE,fill_color=BG,fill_opacity=1,stroke_width=4).move_to([x,y-r,0])
    fluid=VGroup(*[Dot([x+r*np.cos(a),y+r*np.sin(a),0],radius=.07,color=YELLOW)
        for a in np.linspace(.25,5.9,12)])
    fluid.set_z_index(3)
    return VGroup(wall,lumen,swelling,fluid)


def cupula():
    base=RoundedRectangle(width=7.4,height=.25,corner_radius=.1,color=BLUE,fill_opacity=.3).move_to([0,-1.7,0])
    cells=VGroup(*[haircell(h=1.0,w=.65).shift([x,-1.58,0]) for x in (-2,0,2)])
    flap=RoundedRectangle(width=6.5,height=2.1,corner_radius=.5,color=BLUE,fill_color=BLUE,fill_opacity=.19).move_to([0,.3,0])
    return VGroup(base,cells,flap)


def bent_cupula(g,dx=.65):
    out=g.copy()
    for c in out[1]:
        c.bundle.apply_matrix([[1,dx,0],[0,1,0],[0,0,1]],about_point=c.body.get_top())
    out[2].apply_matrix([[1,dx*.5,0],[0,1,0],[0,0,1]],about_point=g[2].get_bottom())
    return out


def spikes(x,y,count=9,width=4.3,color=GREEN):
    baseline=Line([x-width/2,y,0],[x+width/2,y,0],color=GREY,stroke_width=2)
    # Events at equal intervals: a resting or illustrative constant-rate train.
    train=VGroup(*[Line([a,y,0],[a,y+.65,0],color=color,stroke_width=3)
        for a in np.linspace(x-width/2+.15,x+width/2-.15,count)]) if count else VGroup()
    return VGroup(baseline,train)


def paired(left=9,right=9,lost=False):
    a=canal(-3.25,.35,1.5); b=canal(3.25,.35,1.5)
    if lost:
        # Stroke-only de-emphasis preserves the same hollow fill on both canals.
        a[0].set_stroke(GREY,opacity=.35).set_fill(opacity=0)
        a[1].set_fill(opacity=0)
        a[2].set_stroke(GREY,opacity=.35)
        a[3].set_color(GREY).set_opacity(.35)
    names=VGroup(label('Left horizontal canal',-3.25,2.3,size=28),label('Right horizontal canal',3.25,2.3,size=28))
    rates=VGroup(spikes(-3.25,-2.2,left,width=4.6),spikes(3.25,-2.2,right,width=4.6))
    head=VGroup(Ellipse(width=11.8,height=4.8,color=GREY,stroke_opacity=.5).move_to([0,.2,0]),
        Polygon([-.3,2.55,0],[0,2.95,0],[.3,2.55,0],color=GREY))
    return VGroup(a,b,names,rates,head)


def gaze(theta=0,eyeangle=0,fixate=False):
    rot=np.array([[np.cos(theta),-np.sin(theta),0],[np.sin(theta),np.cos(theta),0],[0,0,1]])
    outline=Circle(2.15,color=GREY,stroke_width=4).shift([0,-.5,0])
    nose=Polygon([-.23,1.55,0],[0,2.0,0],[.23,1.55,0],color=GREY,fill_opacity=.3)
    nose.rotate(theta,about_point=[0,-.5,0])
    eyes=VGroup(); lines=VGroup()
    for x in (-.85,.85):
        center=rot@np.array([x,.9,0])+np.array([0,-.5,0])
        eye=Circle(.52,color=TEXT,fill_color=TEXT,fill_opacity=.09).move_to(center)
        direction=np.array([-np.sin(theta+eyeangle),np.cos(theta+eyeangle),0])
        if fixate:
            direction=np.array([0,2.9,0])-center; direction/=np.linalg.norm(direction)
        pupil=Dot(center+.26*direction,radius=.15,color=TEAL)
        eyes.add(VGroup(eye,pupil))
        if fixate: lines.add(Line(pupil.get_center(),[0,2.9,0],color=YELLOW,stroke_width=2))
    return VGroup(outline,nose,eyes,lines)


def picture():
    box=Rectangle(width=2.25,height=.65,color=GOLD).move_to([0,2.9,0])
    return VGroup(box,Dot([0,2.9,0],color=YELLOW,radius=.1),label('picture on the wall',3.7,2.9,GOLD,28))


def turn_arrow(x=0,y=0,r=.85,right=False):
    return Arc(radius=r,start_angle=PI*.2 if not right else PI*.8,
        angle=PI*.65 if not right else -PI*.65,color=YELLOW,stroke_width=5).add_tip(tip_length=.2).shift([x,y,0])


def small_head(x=0,y=0):
    return VGroup(Circle(.55,color=GREY),Polygon([-.12,.5,0],[0,.8,0],[.12,.5,0],color=GREY)).shift([x,y,0])


def predict_frame():
    return VGroup(paired(0,9,True),small_head().scale(1.45).move_to([0,.35,0]),label('Head still',0,-.85,size=28),
        label('What does the brain think is happening?',0,3.35,size=30))


def otolith():
    base=RoundedRectangle(width=6.6,height=.2,corner_radius=.07,color=BLUE,fill_opacity=.3).move_to([0,-1.8,0])
    cells=VGroup(*[haircell(h=1,w=.65).shift([x,-1.7,0]) for x in (-2,0,2)])
    gel=RoundedRectangle(width=6,height=.65,corner_radius=.18,color=BLUE,fill_color=BLUE,fill_opacity=.4).move_to([0,-.15,0])
    crystals=VGroup(*[Square(.24,color=GOLD,fill_color=GOLD,fill_opacity=.85).rotate(PI/4).move_to([x,.25,0]) for x in np.linspace(-2.5,2.5,9)])
    return VGroup(base,cells,VGroup(gel,crystals))


def shear(g,dx=-.7):
    out=g.copy();out[2].shift(RIGHT*dx)
    for c in out[1]:
        c.bundle.apply_matrix([[1,dx,0],[0,1,0],[0,0,1]],about_point=c.body.get_top())
    return out


def profile():
    # Upright profile facing right; the entire outline rotates during tilt.
    return VGroup(Ellipse(width=2.6,height=3.6,color=GREY,stroke_width=4),
        Polygon([1.1,.7,0],[1.75,.2,0],[1.15,.05,0],color=GREY,fill_color=BG,fill_opacity=1),
        Dot([.95,.8,0],color=TEAL,radius=.12),
        Line([-.7,-1.5,0],[-.7,-2.2,0],color=GREY),Line([.65,-1.5,0],[.65,-2.2,0],color=GREY))


def node(s,x,y):
    return chip(s,BLUE,size=28).move_to([x,y,0])


def link(a,b,color=GREEN):
    d=b.get_center()-a.get_center()
    if abs(d[1])>abs(d[0]): start,end=(a.get_top(),b.get_bottom()) if d[1]>0 else (a.get_bottom(),b.get_top())
    else: start,end=(a.get_right(),b.get_left()) if d[0]>0 else (a.get_left(),b.get_right())
    return Arrow(start,end,buff=.1,color=color,stroke_width=4,tip_length=.18)


def circuit():
    # Every node has the same coordinates throughout all three teaching steps.
    c=node('Left horizontal canal',-3.35,-2.9)
    v=node('Left vestibular nucleus',-3.35,-1.45)
    a=node('Right abducens nucleus',3.35,-1.45)
    r=node('Right lateral rectus',3.35,.55)
    o=node('Left oculomotor nucleus',-3.35,.05)
    m=node('Left medial rectus',-3.35,1.4)
    er=VGroup(Circle(.7,color=TEXT),Dot(color=TEAL,radius=.21)).move_to([3.35,2.55,0])
    el=VGroup(Circle(.7,color=TEXT),Dot(color=TEAL,radius=.21)).move_to([-3.35,2.8,0])
    inter=chip('interneuron',GREEN,size=26).move_to([.6,-.5,0])
    path=Arrow(inter.get_left(),o.get_right(),buff=.1,color=GREEN,stroke_width=4,tip_length=.2)
    return dict(c=c,v=v,a=a,r=r,o=o,m=m,er=er,el=el,inter=inter,path=path)


def circuit_base(scene,stage=0):
    q=circuit()
    scene.add(DashedLine([0,-3.2,0],[0,-1.1,0],color=GREY,stroke_opacity=.5),
        label('midline',.65,-3.4,GREY,26),
        small_head().scale(1.6).move_to([0,2.1,0]),
        turn_arrow(0,2.1,.65),label('left turn',0,.8,YELLOW,28))
    if stage>=1: scene.add(q['c'],q['v'],q['a'],link(q['c'],q['v']),link(q['v'],q['a']))
    if stage>=2:
        q['er'][1].shift(RIGHT*.3)
        scene.add(q['r'],link(q['a'],q['r']),q['er'],link(q['r'],q['er']),label('right eye',3.35,3.5,TEAL,28))
    return q


class S00Title(TitleCard):
    LESSON='Hearing and Balance'
    TITLE='Turning Heads, Steady Eyes'


class S01Question(SpokenScene):
    def construct(self):
        t=ValueTracker(0); h=always_redraw(lambda:gaze(t.get_value(),-t.get_value(),True))
        self.add(h,picture()); self.at('Turn your head')
        self.play(t.animate.set_value(PI/6),run_time=1.1)
        self.at('eyes stay fixed'); self.play(Indicate(h[3],color=YELLOW),run_time=.5)
        self.at('How does the ear'); self.play(FadeIn(label('How does the ear do that?',0,-3.2,size=32)),run_time=.4)
        self.finish()


class S02Same(SpokenScene):
    def construct(self):
        h=haircell(h=2.8,w=1.4).move_to([0,-.1,0]).set_z_index(5); self.add(h)
        self.at('Same switch'); self.play(FadeIn(label('Same switch, new front end',0,3.3)),run_time=.4)
        self.at('a semi circular canal')
        c=canal(0,.1,2.35)
        self.play(FadeIn(c),h.animate.scale(.22).move_to([0,-2.25,0]),FadeIn(label('Semicircular canal',4.45,1.5,BLUE,30)),run_time=.7)
        self.at('fluid filled ring'); self.play(FadeIn(label('Fluid-filled ring',4.4,.55,YELLOW,28)),run_time=.4)
        self.finish()


class S03Cupula(SpokenScene):
    def construct(self):
        c=canal(0,.1,2.35); h=haircell(h=.6,w=.3).move_to([0,-2.25,0]); self.add(c,h)
        self.at('In its swelling')
        marker=SurroundingRectangle(c[2],color=GOLD,buff=.12)
        zoom=label('ampulla → zoom',3.8,-2.1,GOLD,28)
        self.play(Create(marker),FadeIn(zoom),run_time=.25)
        g=cupula().scale(1.15).shift(DOWN*.35)
        self.play(FadeOut(c),FadeOut(h),FadeOut(marker),FadeOut(zoom),FadeIn(g),run_time=.65)
        self.at('hair bundles sit')
        txt=label('Hair bundles',-4.6,-2.9,TEAL,30)
        self.play(FadeIn(txt),GrowArrow(Arrow(txt.get_top(),g[1][0].bundle.get_center(),color=TEAL,buff=.15)),run_time=.4)
        self.at('gelatinous flap'); self.play(Indicate(g[2],color=BLUE,scale_factor=1.01),run_time=.35)
        self.at('called the cupula')
        txt2=label('Cupula',3.9,2.2,BLUE,32)
        self.play(FadeIn(txt2),GrowArrow(Arrow(txt2.get_bottom(),g[2].get_top()+RIGHT*2,color=BLUE,buff=.12)),run_time=.45)
        self.finish()


class S04Lag(SpokenScene):
    def construct(self):
        c=canal(-3.65,.1,2); g=cupula().stretch_to_fit_width(5.3).stretch_to_fit_height(4.7).move_to([3.35,-.1,0])
        self.add(c,g,label('Cupula',3.25,2.95,BLUE,30),
            DashedLine(c[2].get_right(),g[2].get_center(),color=GOLD).set_z_index(-1),
            label('ampulla → zoom',-.4,-2.9,GOLD,26))
        self.at('When the head turns')
        a=turn_arrow(-3.65,.1,2.45)
        self.play(Create(a),FadeIn(label('head turns',-3.65,3.05,YELLOW,30)),Rotate(VGroup(c[0],c[1],c[2]),.5,about_point=[-3.65,.1,0]),run_time=.75)
        self.at('the fluid lags behind')
        f=turn_arrow(-3.65,.1,1.35,True)
        self.play(Create(f),FadeIn(label('fluid lags',-3.65,-.15,YELLOW,28)),Rotate(c[3],-.35,about_point=[-3.65,.1,0]),run_time=.7)
        target=bent_cupula(g,dx=.75)
        self.at('bends the cupula'); self.play(Transform(g[2],target[2]),run_time=.55)
        self.at('pushes the bundles')
        tip=label('bundles tip',4.7,-2.9,TEAL,30)
        pointer=Arrow(tip.get_top(),target[1][2].bundle.get_center(),color=TEAL,buff=.12)
        self.play(Transform(g[1],target[1]),FadeIn(tip),GrowArrow(pointer),run_time=.55)
        self.finish()


class S05Velocity(SpokenScene):
    def construct(self):
        # Normalized stimulus and a first-order afferent response: tau dr/dt + r = v.
        ts=np.linspace(0,8,401); vel=np.sin(2*PI*(ts-1)/6)*np.sin(PI*np.clip((ts-1)/6,0,1))**2
        vel[(ts<1)|(ts>7)]=0
        rate=np.zeros_like(ts); dt=ts[1]-ts[0]
        for i in range(1,len(ts)): rate[i]=rate[i-1]+dt/.22*(vel[i]-rate[i-1])
        def plot(y,values,color):
            axis=VGroup(Line([-4.7,y,0],[5.7,y,0],color=GREY),Line([-4.7,y-1.05,0],[-4.7,y+1.1,0],color=GREY))
            trace=VMobject(color=color,stroke_width=5).set_points_as_corners([[t*1.3-4.7,y+v,0] for t,v in zip(ts,values)])
            return axis,trace
        ax,v=plot(1.35,vel,YELLOW); bx,r=plot(-1.65,rate,GREEN)
        self.add(ax,bx,label('Head velocity (left = up)',0,2.95,YELLOW,30),label('Firing rate · roughly velocity',0,-.45,GREEN,30),
            label('0',-5.2,1.35,size=28),label('rest',-5.45,-1.65,size=28),
            label('time → (s)',4.6,-3.5,size=28),label('illustrative; normalized',-3,-3.5,GREY,26))
        for y in (1.35,-1.65):
            for t in (0,4,8): self.add(label(str(t),t*1.3-4.7,y-1.2,size=26))
        self.at('During everyday head movements'); self.play(Create(v),run_time=1.4)
        self.at('nerve fibers signal'); self.play(Create(r),run_time=.85)
        self.at('roughly how fast'); self.play(Indicate(r,color=GREEN,scale_factor=1.02),run_time=.5)
        self.finish()


class S06Rest(SpokenScene):
    def construct(self):
        g=paired(); self.add(g[0],g[2][0],g[3][0],g[4])
        self.at('They fire even at rest'); self.play(FadeIn(label('resting firing',-3.25,-2.85,GREEN,28)),run_time=.45)
        self.at('Canals on opposite sides'); self.play(FadeIn(g[1]),FadeIn(g[2][1]),FadeIn(g[3][1]),FadeIn(label('resting firing',3.25,-2.85,GREEN,28)),run_time=.65)
        self.finish()


class S07Pair(SpokenScene):
    def construct(self):
        g=paired(); self.add(g)
        self.at('A turn to the left'); self.play(Create(turn_arrow(0,.4,1.1)),FadeIn(label('Head turns left',0,3.35,YELLOW,30)),run_time=.5)
        self.at('excites the left canal'); self.play(Transform(g[3][0],spikes(-3.25,-2.2,17,4.6)),FadeIn(label('excited',-3.25,-2.95,GREEN,30)),run_time=.5)
        self.at('inhibits the right'); self.play(Transform(g[3][1],spikes(3.25,-2.2,5,4.6,RED)),FadeIn(label('inhibited',3.25,-2.95,RED,30)),run_time=.5)
        self.finish()


class S08Vor(SpokenScene):
    def construct(self):
        self.add(gaze().scale(.65).move_to([0,1.2,0]))
        skeleton=VGroup(*[RoundedRectangle(width=4.4,height=.65,color=GREY,stroke_opacity=.4).move_to([x,y,0]) for x,y in [(-3.25,-2.65),(-3.25,-1.15),(3.25,-1.15)]])
        self.at('The canals drive'); self.play(FadeIn(skeleton),run_time=.5)
        self.at('the vestibulocular reflex'); self.play(FadeIn(label('Vestibulo-ocular reflex (VOR)',0,3.3,size=34)),run_time=.45)
        self.at('keeps the eyes still'); self.play(Indicate(self.mobjects[0],color=TEAL,scale_factor=1.03),run_time=.5)
        self.finish()


class S09Step1(SpokenScene):
    def construct(self):
        q=circuit_base(self)
        self.add(label('VOR · step 1',-3.35,3.25,size=32))
        self.at('In a left turn'); self.play(FadeIn(q['c']),run_time=.5)
        self.at('left vestibular nucleus'); self.play(GrowArrow(link(q['c'],q['v'])),FadeIn(q['v']),run_time=.6)
        self.at('excites the right'); self.play(GrowArrow(link(q['v'],q['a'])),FadeIn(q['a']),run_time=.7)
        self.finish()


class S10Step2(SpokenScene):
    def construct(self):
        q=circuit_base(self,stage=1)
        self.add(q['er'],label('right eye',3.35,3.5,TEAL,28))
        self.at('It drives the right')
        self.play(GrowArrow(link(q['a'],q['r'])),FadeIn(q['r']),GrowArrow(link(q['r'],q['er'])),run_time=.6)
        self.at('the right eye turns')
        pull=Arrow([3.4,2.55,0],[4.55,2.55,0],color=TEAL,buff=.1)
        self.play(q['er'][1].animate.shift(RIGHT*.3),GrowArrow(pull),run_time=.6)
        self.finish()


class S11Step3(SpokenScene):
    def construct(self):
        q=circuit_base(self,stage=2)
        self.at('Abducens interneurons cross')
        self.play(GrowArrow(link(q['a'],q['inter'])),FadeIn(q['inter']),run_time=.5)
        # The destination appears with its incoming MLF arrow, never afterwards.
        self.play(FadeIn(q['o']),GrowArrow(q['path']),FadeIn(label('MLF',.1,.1,GREEN,28)),run_time=.7)
        self.at('left oculomotor nucleus'); self.play(Indicate(q['o'],color=BLUE,scale_factor=1.01),run_time=.35)
        self.add(q['el'],label('left eye',-3.35,3.65,TEAL,26))
        self.at('which turns the left eye')
        self.play(FadeIn(q['m']),GrowArrow(link(q['o'],q['m'])),GrowArrow(link(q['m'],q['el'])),run_time=.5)
        self.play(q['el'][1].animate.shift(RIGHT*.3),run_time=.4)
        self.finish()


class S12Both(SpokenScene):
    def construct(self):
        t=ValueTracker(0); h=always_redraw(lambda:gaze(t.get_value(),-t.get_value(),True))
        self.add(h,picture())
        self.at('Both eyes turn right'); self.play(FadeIn(label('Eyes right →',3.9,-1.6,TEAL,30)),run_time=.4)
        self.at('as the head turns left'); self.play(t.animate.set_value(PI/6),FadeIn(label('← Head left',-3.9,-2.9,YELLOW,30)),run_time=.8)
        self.finish()


class S13Predict(SpokenScene):
    def construct(self):
        g=paired(); self.add(g)
        self.at('Now the left inner ear'); lost=paired(0,9,True)
        self.play(Transform(g[0],lost[0]),FadeOut(g[3][0][1]),run_time=1.8)
        self.at('The head is still'); self.play(FadeIn(small_head().scale(1.45).move_to([0,.35,0])),FadeIn(label('Head still',0,-.85,size=28)),run_time=.4)
        self.at('What does the brain'); self.play(FadeIn(label('What does the brain think is happening?',0,3.35,size=30)),run_time=.4)
        self.finish()


class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(predict_frame())
        prompt=label('Pause and predict · 5',0,-3.2,GOLD,30); self.add(prompt)
        for i in range(5,0,-1):
            prompt.become(label(f'Pause and predict · {i}',0,-3.2,GOLD,30)); self.wait(1)


class S15Reveal(SpokenScene):
    def construct(self):
        g=predict_frame(); self.add(g)
        self.at("The right side's resting firing"); self.play(FadeOut(g[3]),Indicate(g[0][3][1],color=GREEN,scale_factor=1.05),run_time=.6)
        self.at('now unmatched'); self.play(FadeIn(label('Unmatched resting firing',0,3.35,GREEN,32)),run_time=.4)
        self.at('The brain reads a turn')
        self.play(Create(turn_arrow(0,.2,1.1,True)),FadeIn(label('Perceived turn right →',0,-3.15,YELLOW,30)),run_time=.5)
        self.finish()


class S16Vertigo(SpokenScene):
    def construct(self):
        # Large close-up makes pupil excursions plainly visible at draft resolution.
        eyes=VGroup(*[VGroup(Ellipse(width=3.3,height=1.7,color=TEXT),Dot([0,0,0],color=TEAL,radius=.38)).move_to([x,.65,0]) for x in (-2.05,2.05)])
        pupils=VGroup(*[e[1] for e in eyes])
        window=VGroup(Rectangle(width=1.4,height=1.8,color=BLUE),Line([-.7,0,0],[.7,0,0],color=BLUE),Line([0,-.9,0],[0,.9,0],color=BLUE)).move_to([-5.35,.5,0])
        door=VGroup(Rectangle(width=1.35,height=2.7,color=GREY),Dot([.45,0,0],color=GOLD)).move_to([5.3,.1,0])
        pic=VGroup(Rectangle(width=1.5,height=.8,color=GOLD),Line([-.6,-.25,0],[.1,.25,0],color=GOLD)).move_to([0,2.7,0])
        room=VGroup(window,door,pic,Line([-6.3,-1.65,0],[6.3,-1.65,0],color=GREY))
        head=Ellipse(width=8.3,height=4.7,color=GREY,fill_color=BG,fill_opacity=1).move_to([0,.25,0])
        eyes.stretch_to_fit_height(2.15)
        self.add(room,head,eyes,label('Head still',5.05,-2.1,size=28))
        slow=label('slow drift left ←',-2.8,3.4,TEAL,30); fast=label('quick jerk right →',2.8,3.4,YELLOW,30)
        self.at('The eyes drift slowly left'); self.play(FadeIn(slow),pupils.animate.shift(LEFT*.65),run_time=1.25,rate_func=linear)
        self.at('with quick jerks'); self.play(FadeIn(fast),pupils.animate.shift(RIGHT*.65),run_time=.3)
        self.play(pupils.animate.shift(LEFT*.65),run_time=1.2,rate_func=linear); self.play(pupils.animate.shift(RIGHT*.65),run_time=.3)
        self.at('The room seems to spin')
        self.play(Rotate(room,.13),Create(turn_arrow(-5.35,.5,1.1)),FadeIn(label('room seems to spin',0,-2.65,YELLOW,28)),run_time=.45)
        self.play(Rotate(room,-.26),run_time=.6)
        self.play(Rotate(room,.26),run_time=.6)
        self.play(pupils.animate.shift(LEFT*.65),run_time=1.2,rate_func=linear); self.play(pupils.animate.shift(RIGHT*.65),run_time=.3)
        self.at('one mechanism of vertigo'); self.play(FadeIn(label('One mechanism of vertigo',0,-3.35,size=32)),run_time=.4)
        self.finish()


class S17Otolith(SpokenScene):
    def construct(self):
        h=profile().scale(1.45).move_to([-2.8,-.5,0])
        u=Ellipse(width=1.8,height=.4,color=BLUE).move_to([-2.6,.2,0]); s=Ellipse(width=.4,height=1.5,color=BLUE).move_to([-1.75,-.65,0])
        organs=VGroup(h,u,s,label('Utricle · roughly horizontal',2.9,.6,BLUE,28),label('Saccule · roughly vertical',2.9,-1,BLUE,28),
            Line(u.get_right(),[.3,.6,0],color=BLUE),Line(s.get_right(),[.3,-1,0],color=BLUE),label('orientation when upright',2.5,-2.45,GREY,26))
        self.add(organs,label('Otolith organs',0,3.3,size=34))
        both=VGroup(Line([.25,1.65,0],[5.7,1.65,0],color=YELLOW),Line([.25,1.65,0],[.25,1.25,0],color=YELLOW),Line([5.7,1.65,0],[5.7,-.6,0],color=YELLOW))
        gravity=label('gravity',0,2.75,YELLOW,30)
        self.at('sense gravity'); self.play(FadeIn(both),FadeIn(gravity),run_time=.4)
        self.at('and straight line acceleration')
        self.play(Transform(gravity,label('gravity and straight-line acceleration',0,2.75,YELLOW,30)),run_time=.45)
        self.at('Their bundles are capped')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.25)
        g=otolith().scale(1.5).move_to([0,-.6,0]); self.play(FadeIn(g),run_time=.4)
        self.at('crystal loaded membrane'); self.play(FadeIn(label('Crystal-loaded membrane',0,2.55,GOLD,32)),GrowArrow(Arrow([0,2.1,0],g[2].get_top(),color=GOLD,buff=.1)),run_time=.4)
        self.finish()


class S18Tilt(SpokenScene):
    def construct(self):
        h=profile().scale(1.1).move_to([-4.5,-.1,0]); g=otolith().scale(.95).move_to([2.55,-.65,0])
        self.add(h,g,label('back ←',-4.7,-2.8,YELLOW,28),label('Crystal-loaded membrane',2.6,2.4,GOLD,30))
        self.at('Tilt the head back')
        self.play(Rotate(h,PI/6),GrowArrow(Arrow([-1.7,1.4,0],[-1.7,-1.3,0],color=YELLOW)),FadeIn(label('gravity',-.9,-2.1,YELLOW,28)),run_time=.8)
        self.at('that heavy membrane slides backward')
        self.play(Transform(g,shear(g,-.9)),GrowArrow(Arrow([4,1.5,0],[1.1,1.5,0],color=GOLD)),FadeIn(label('slides backward',2.65,1.95,GOLD,30)),run_time=1)
        self.finish()


def aircraft():
    body=Polygon([-2,0,0],[1.6,0,0],[2,.25,0],[1.4,.55,0],[-.4,.55,0],[-1,1.2,0],[-1.35,1.2,0],[-1.1,.55,0],[-1.8,.55,0],[-2.2,.9,0],color=GREY,fill_opacity=.45)
    return VGroup(body,*[Circle(.16,color=TEXT).move_to([x,-.17,0]) for x in (-1.2,1.1)])


class S19Plane(SpokenScene):
    def construct(self):
        p=aircraft().move_to([-3.5,2.05,0]); runway=Line([-6.2,1.12,0],[6.2,1.12,0],color=GREY)
        p.shift(UP*(1.12-p.get_bottom()[1])); g=otolith().scale(1.3).move_to([0,-1.4,0])
        self.add(p,runway,g)
        self.at('Accelerate forward')
        speed=VGroup(Arrow([-1,3.1,0],[4.5,3.1,0],color=YELLOW),label('accelerating forward',1.7,3.5,YELLOW,30))
        self.play(FadeIn(speed),p.animate.shift(RIGHT*5),run_time=2.8,rate_func=lambda t:t*t)
        self.at('it slides backward too'); self.play(Transform(g,shear(g,-.85)),GrowArrow(Arrow([2,.15,0],[-2,.15,0],color=GOLD)),run_time=.7)
        self.at('Without a view outside')
        cabin=RoundedRectangle(width=6.4,height=2.45,corner_radius=.2,color=GREY,fill_color=BG,fill_opacity=1).move_to([-.9,2.05,0])
        # Side view: filled torso, bent legs, arm, and a seat with headrest.
        seat=VGroup(RoundedRectangle(width=.38,height=1.7,corner_radius=.12,color=GREY,fill_opacity=.5).move_to([-1.95,2.1,0]),
            RoundedRectangle(width=1.75,height=.25,corner_radius=.1,color=GREY,fill_opacity=.5).move_to([-1.15,1.25,0]),
            RoundedRectangle(width=.7,height=.35,corner_radius=.12,color=GREY,fill_opacity=.5).move_to([-2,2.95,0]))
        person=VGroup(Circle(.31,color=TEAL,fill_color=TEAL,fill_opacity=1).move_to([-1.35,2.8,0]),
            Polygon([-1.55,2.45,0],[-1.05,2.45,0],[-.7,1.5,0],[-1.2,1.4,0],color=TEAL,fill_color=TEAL,fill_opacity=1),
            VMobject(color=TEAL,stroke_width=15).set_points_as_corners([[-1,1.45,0],[.15,1.45,0],[.4,.95,0],[.85,.95,0]]),
            VMobject(color=TEAL,stroke_width=9).set_points_as_corners([[-1.2,2.25,0],[-.6,1.85,0],[0,1.85,0]]))
        self.play(p.animate.scale(.72).move_to([4.8,2.05,0]),Transform(speed,VGroup(Arrow([3.2,2.8,0],[6.2,2.8,0],color=YELLOW),label('accelerating forward',4.65,3.4,YELLOW,26))),FadeIn(cabin),FadeIn(seat),FadeIn(person),run_time=.5)
        self.at('feel tipped back'); self.play(Rotate(person,.3,about_point=[-1,1.45,0]),FadeIn(label('Feels tipped back',-1.2,3.55,YELLOW,30)),run_time=.5)
        self.finish()


def rate_panel(x,turning):
    # Same illustrative first-order rate/velocity model as s05, now for a brief tilt.
    t=np.linspace(0,4,161); v=np.sin(PI*np.clip(t/3,0,1))**2 if turning else np.zeros_like(t)
    v[t>3]=0; r=np.zeros_like(t)
    for i in range(1,len(t)): r[i]=r[i-1]+.025/.22*(v[i]-r[i-1])
    axis=VGroup(Line([x-1.45,-2.25,0],[x+1.45,-2.25,0],color=GREY),
        Line([x-1.45,-2.35,0],[x-1.45,-.65,0],color=GREY),
        label('rest',x-1.05,-2.7,GREY,28),label('time →',x+.9,-2.7,GREY,28))
    trace=VMobject(color=GREEN,stroke_width=5).set_points_as_corners([[x-1.45+.725*a,-2.25+b*1.45,0] for a,b in zip(t,r)])
    return VGroup(axis,trace)


class S20Ambiguous(SpokenScene):
    def construct(self):
        l=otolith().scale(.65).move_to([-3.25,1.3,0]); r=otolith().scale(.65).move_to([3.25,1.3,0])
        self.add(l,r,label('Tilt back',-3.25,3.25,YELLOW,32),label('Accelerate forward',3.25,3.25,YELLOW,32))
        self.at('an otolith organ alone'); self.play(Transform(l,shear(l,-.5)),Transform(r,shear(r,-.5)),run_time=.6)
        self.at('cannot tell tilt from acceleration'); self.play(FadeIn(label('Same membrane shear',0,2.55,GOLD,30)),run_time=.4)
        cl=canal(-5.1,-1.25,.95); cr=canal(1.4,-1.25,.95)
        self.at('A tilt also rotates the head'); self.play(FadeIn(cl),FadeIn(cr),Create(turn_arrow(-5.1,-1.25,1.18)),run_time=.6)
        self.at('the canals feel rotation')
        self.play(FadeIn(rate_panel(-2.65,True)),FadeIn(rate_panel(3.85,False)),FadeIn(label('no canal signal',3.85,-.15,GREEN,28)),FadeIn(label('rate rises',-2.65,-.15,GREEN,28)),FadeIn(label('no rotation',1.4,.05,GREY,28)),run_time=.5)
        self.add(label('Canals help tell them apart',0,-3.35,size=32))
        self.finish()


def closing_row(name,mechanics,y):
    n=T(name,size=30,color=BLUE).move_to([-5.65,y,0],aligned_edge=LEFT)
    m=T(mechanics,size=30,color=YELLOW).move_to([-2.25,y,0],aligned_edge=LEFT)
    cell=haircell(h=1.2,w=.7).move_to([3.25,y,0]); txt=T('hair cell',size=30,color=TEAL).move_to([3.8,y,0],aligned_edge=LEFT)
    return VGroup(n,m,cell,txt)


class S21Close1(SpokenScene):
    def construct(self):
        self.add(label('Organ',-4.8,3.05,size=30),label('Mechanics in front',-.5,3.05,size=30),label('Same cell',4.35,3.05,size=30))
        rows=VGroup(*[closing_row(n,m,y) for n,m,y in [('Cochlea','A wave',1.8),('Canals','A ring of fluid',-.4),('Otoliths','A heavy membrane',-2.6)]])
        self.add(rows.copy().set_opacity(.22))
        self.at('One switch'); self.play(FadeIn(VGroup(*[row[2:].copy() for row in rows])),run_time=.4)
        for phrase,row in zip(['A wave','a ring of fluid','a heavy membrane'],rows):
            self.at(phrase); self.play(FadeIn(row),run_time=.4)
        self.finish()


class S22Close2(SpokenScene):
    def construct(self):
        c=chip('Circuits',BLUE,size=38).move_to([0,2.5,0]); self.add(c)
        a=label('which cells are active',-3.35,.55,TEAL,30); b=label('how the two sides compare',3.25,.55,TEAL,30)
        # Align the first glyphs' feet: both are non-descenders, so this aligns baselines.
        b.shift(UP*(a[0].get_bottom()[1]-b[0].get_bottom()[1]))
        # Aligned outputs; arrows use distinct ports and avoid both text labels.
        self.at('And circuits that read'); self.play(Indicate(c,scale_factor=1.04),run_time=.4)
        self.at('which cells are active')
        cells=VGroup(*[haircell(h=1.75,w=.85).move_to([x,-1.65,0]) for x in (-4.8,-3.35,-1.9)])
        cells[0].set_opacity(.3); cells[2].set_opacity(.3)
        self.play(GrowArrow(Arrow(c.get_left(),a.get_top(),color=TEAL,buff=.15)),FadeIn(a),FadeIn(cells),run_time=.5)
        self.at('how the two sides compare')
        rings=VGroup(canal(2.05,-1.4,.95),canal(4.65,-1.4,.95),spikes(2.05,-3.2,12,2.1),spikes(4.65,-3.2,5,2.1))
        self.play(GrowArrow(Arrow(c.get_right(),b.get_top(),color=TEAL,buff=.15)),FadeIn(b),FadeIn(rings),run_time=.5)
        self.finish()


class S23End(EndCard):
    LINE='Same hair cell; mechanics and circuits decide what it reports.'
