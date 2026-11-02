"""Where Every Command Ends — reviewed animation.
COLOR MAP: BLUE neurons/axons/voltage; GREEN excitation/muscle force;
RED inhibition; YELLOW input/spikes/threshold; TEAL spindle; GREY structure.
All curves and voltage ratios are calculated from the stated dimensionless models.
"""
import os
import json
from pathlib import Path
import numpy as np
from bp_style import *


class SpokenScene(SpokenScene):
    # Keep the fixed audio timeline: the shared helper adds .4 s to every scene.
    # Cue diagnostics belong in temporary render storage, not the chapter sources.
    def at(self, phrase, lead=.2, nth=0):
        target = max(0., self.t_of(phrase, nth)-lead)
        with open('/tmp/motor-units-fix-sync.log', 'a') as f:
            f.write(f'{os.environ.get("KX_SCENE_ID")} {phrase!r} target={target:.3f} now={self.elapsed():.3f} late={max(0,self.elapsed()-target):.3f}\n')
        if target-self.elapsed() > .02:
            self.wait(target-self.elapsed())

    def finish(self):
        if self.narration_s-self.elapsed() > .001:
            self.wait(self.narration_s-self.elapsed())


def P(x,y): return np.array([x,y,0.])
def label(s,x,y,size=28,color=TEXT,font=FONT):
    # Pango positions actual subscripts, avoiding absent Unicode subscript glyphs.
    replacements={'Rᵢₙ':'R<sub>in</sub>','Iₜₕ':'I<sub>th</sub>','ΔVₜₕ':'ΔV<sub>th</sub>',
                  'Iₑff':'I<sub>eff</sub>','Aᵅ⁻ᵝ':'A<sup>α−β</sup>',
                  'A⁻ᵝ':'A<sup>−β</sup>','Aᵅ':'A<sup>α</sup>'}
    marked=s
    for old,new in replacements.items(): marked=marked.replace(old,new)
    mob=MarkupText(marked,font=font,font_size=size,color=color) if marked!=s else T(s,size,color,font=font)
    return mob.move_to(P(x,y))
def poly(points,color=BLUE,w=5):
    return VMobject(stroke_color=color,stroke_width=w).set_points_as_corners([P(*p) for p in points])
def neuron(x,y,r=.6):
    body=Circle(r,color=BLUE,fill_color=BLUE,fill_opacity=.2).move_to(P(x,y))
    dend=VGroup(*[Line(P(x-r*.85,y+d*r),P(x-r-.28,y+d*r*1.5),color=BLUE,stroke_width=4) for d in (-.55,0,.55)])
    return VGroup(body,dend)
def fibres(x=4,count=6):
    return VGroup(*[RoundedRectangle(width=2.6,height=.28,corner_radius=.12,color=GREY,fill_color=GREY,fill_opacity=.2).move_to(P(x,1.7-i*.55)) for i in range(count)])
def unit():
    n=neuron(-4.6,.2,.8); a=Line(P(-3.8,.2),P(-1.5,.2),color=BLUE,stroke_width=5)
    f=fibres(3.8,8)
    # Six owned fibres and two separate, dark fibres below the unit bracket.
    b=VGroup(*[poly([(-1.5,.2),(.2,f[i].get_y()),(2.5,f[i].get_y())]) for i in range(6)])
    return n,a,f,b

def cord():
    c=Circle(2.55,color=GREY,fill_color=GREY,fill_opacity=.08).move_to(P(-2.5,.1))
    h=Polygon(*[P(-2.5+dx,.1+dy) for dx,dy in [(-.2,.5),(-1.1,1.7),(-.85,.1),(-1.4,-1.4),(-.3,-.7),(.3,-.7),(1.4,-1.4),(.85,.1),(1.1,1.7),(.2,.5)]],color=GREY,fill_color=GREY,fill_opacity=.25)
    return VGroup(c,h,label('spinal cord',-2.5,3.35,30),label('dorsal',-2.5,2.95,26),label('ventral',-2.5,-2.9,26))

BOTTOM=-2.05
THRESH=1.65

def voltage(x,h=1.,width=.63):
    return Rectangle(width=width,height=max(.025,h),stroke_width=0,fill_color=BLUE,fill_opacity=.8).move_to(P(x,BOTTOM+h/2))
def gauge(x,h=.4):
    outline=Rectangle(width=.86,height=4.35,color=GREY,stroke_width=2).move_to(P(x,.125))
    line=DashedLine(P(x-.62,THRESH),P(x+.43,THRESH),color=YELLOW,dash_length=.1)
    return VGroup(outline,voltage(x,h),line)

def pool(hs=(.35,.35,.35),shared=False,question=False,units=True):
    g=VGroup(); bars=[]; cells=[]
    for i,(x,r,name) in enumerate(zip((-4.35,0,4.35),(.30,.46,.65),('small','medium','large'))):
        n=neuron(x-.65,.25,r); b=gauge(x+.52,hs[i]); cells.append(n); bars.append(b[1])
        col=VGroup(n,b,label(name,x, -2.43,28),label('threshold',x+1.65,THRESH,22,YELLOW))
        if units:
            count=(3,6,12)[i]
            fs=VGroup(*[RoundedRectangle(width=.54,height=.13,corner_radius=.05,color=GREY,fill_color=GREY,fill_opacity=.2).move_to(P(x-1.13+(j%2)*.63,-.9-(j//2)*.17)) for j in range(count)])
            col.add(fs,label(('weak unit','more fibres','strong unit')[i],x,-3.0,26,GREY))
        if i==2:
            col[2].shift(DOWN*.05)
            if units: col[-1].shift(DOWN*.05)
        g.add(col)
    if shared:
        bus=VGroup(label('shared input',0,3.35,30,YELLOW),Line(P(-5,2.85),P(4,2.85),color=YELLOW))
        bus.add(*[Arrow(P(x-.65,2.85),P(x-.65,1.06),buff=0,color=YELLOW,stroke_width=3) for x in (-4.35,0,4.35)])
        dial=VGroup(Arc(radius=.42,start_angle=-PI*.8,angle=PI*1.6,color=YELLOW).move_to(P(-5.8,3.15)),Line(P(-5.8,3.15),P(-5.6,3.44),color=YELLOW,stroke_width=4),label('input',-4.6,3.42,26,YELLOW))
        g.add(bus,dial)
    if question: g.add(label('Which fires first?',0,-3.5,32))
    return g,bars,cells

def prediction():
    g,bs,ns=pool(shared=True,question=True)
    g[4][1].rotate(-.7,about_point=P(-5.8,3.15))
    return g,bs,ns

def inputs():
    n=neuron(1,0,1.05); n.remove(n[1]); gs=[]
    for i,name in enumerate(('brain','muscle spindle (stretch)','skin pain receptor','rhythm circuit')):
        y=2.6-i*1.55
        landing=.75-i*.5
        end=P(1-np.sqrt(1.05**2-landing**2),landing)
        source=label(name,-4.6,y,26,TEAL if i==1 else TEXT)
        start=source.get_right()+RIGHT*.15
        # Horizontal first segment keeps labels beside their source; relay has its own landing point.
        relaypoint=P(-1.6,y)
        path=VMobject(color=TEAL if i==1 else BLUE,stroke_width=4).set_points_as_corners([start,relaypoint,end])
        tip=Arrow(relaypoint,end,color=TEAL if i==1 else BLUE,buff=0,stroke_width=4)
        group=VGroup(source,VGroup(path,tip))
        if i!=1:
            group.add(Circle(.18,color=BLUE,fill_color=BG,fill_opacity=1).move_to(relaypoint),label('interneuron',-1.3,y+(.4 if i==0 else -.4),26,GREY))
        gs.append(group)
    return n,gs

def inhibition_panel(x,h):
    return VGroup(gauge(x,h),label('threshold',x+1.58,THRESH,24,YELLOW))
def excitation(x):
    return VGroup(Arrow(P(x-1.1,-1.3),P(x-1.1,1.2),color=GREEN,buff=0),label('excitation',x-1.3,-2.6,26,GREEN))
def inhibition(x):
    return VGroup(Arrow(P(x+1.1,1.1),P(x+1.1,-1.2),color=RED,buff=0),label('inhibition',x+1.35,-2.65,26,RED))

class S00Title(TitleCard):
    LESSON='Motor Units, Reflexes and Locomotion'
    TITLE='Where Every Command Ends'
    def construct(self):
        title=fit(T(self.TITLE,54,font=TITLE_FONT),max_w=11.5).move_to(P(0,0))
        self.add(label('BIOCHEMISTRYPEDIA',0,1.8,26,TEAL),label(self.LESSON.upper(),0,1.1,26,GREY))
        self.play(FadeIn(title),Create(Line(P(-1.2,-.85),P(1.2,-.85),color=GOLD,stroke_width=4)),run_time=.6)
        self.finish()
    def finish(self):
        if self.narration_s>self.elapsed(): self.wait(self.narration_s-self.elapsed())

class S01Question(SpokenScene):
    def construct(self):
        def arm(x,heavy=False):
            # A tapered upper arm and forearm, with a rounded grip above each load.
            upper=Polygon(*[P(x+dx,y) for dx,y in [(-2.25,-2.25),(-1.72,-2.25),(-1.2,-.55),(-1.72,-.3)]],color=GREY,fill_color=GREY,fill_opacity=.25,stroke_width=4)
            fore=Polygon(*[P(x+dx,y) for dx,y in [(-1.72,-.3),(-1.2,-.55),(.48,1.1),(.15,1.5)]],color=GREY,fill_color=GREY,fill_opacity=.25,stroke_width=4)
            a=VGroup(upper,fore,Circle(.26,color=GREY,fill_color=GREY,fill_opacity=.3).move_to(P(x-1.48,-.4)))
            muscle=Ellipse(width=2.1,height=.5,color=GREEN,stroke_width=5).rotate(.79).move_to(P(x-.55,.5))
            hand=Ellipse(width=.8,height=.48,color=TEXT,fill_color=BG,fill_opacity=1).rotate(-.12).move_to(P(x+.55,1.32))
            fingers=VGroup(*[Arc(radius=.16,start_angle=-PI*.5,angle=PI,color=TEXT,stroke_width=3).move_to(P(x+.43+j*.15,1.29)) for j in range(3)])
            if heavy:
                body=RoundedRectangle(width=2.4,height=2.05,corner_radius=.18,color=GREY,fill_color=GREY,fill_opacity=.12,stroke_width=5).move_to(P(x+1.12,-.6))
                handle=poly([(x+.72,.43),(x+.72,1.3),(x+1.42,1.3),(x+1.42,.43)],TEXT,5)
                seams=VGroup(*[Line(P(x+dx,.39),P(x+dx,-1.59),color=GREY,stroke_width=3) for dx in (.32,1.92)])
                obj=VGroup(body,handle,seams)
            else:
                body=Polygon(*[P(x+dx,y) for dx,y in [(.95,1.83),(2.2,1.83),(2.06,.35),(1.09,.35)]],color=TEXT,fill_color=GREY,fill_opacity=.2,stroke_width=5)
                rim=Ellipse(width=1.25,height=.18,color=TEXT,stroke_width=4).move_to(P(x+1.575,1.83))
                handle=Arc(radius=.43,start_angle=PI/2,angle=PI,color=TEXT,stroke_width=5).move_to(P(x+.77,1.12))
                obj=VGroup(body,rim,handle)
            return VGroup(a,muscle,obj,hand,fingers)
        a,b=arm(-3.25),arm(3.25,True)
        self.add(Line(P(0,-2.65),P(0,3.25),color=GREY),a,b,label('cup',-3.3,2.85,34),label('suitcase',3.3,2.85,34))
        self.at('Lifting a cup'); self.play(a.animate.shift(UP*.25),run_time=.55)
        self.at('lifting a suitcase'); self.play(b.animate.shift(UP*.18),run_time=.8)
        self.add(label('light load',-3.3,-2.7,28,GREY),label('heavy load',3.3,-2.7,28,GREY))
        self.at('same muscle'); self.play(Indicate(a[1]),Indicate(b[1]),run_time=.5)
        self.at('Who decides',lead=.4); self.play(FadeIn(label('Who decides?',0,-3.45,38)),run_time=.2)
        self.finish()

class S02MotorNeuron(SpokenScene):
    def construct(self):
        c=cord(); n=neuron(-1.55,-.65,.25); n[0].set_fill(BLUE,opacity=1)
        glow=VGroup(*[Circle(r,stroke_width=0,fill_color=BLUE,fill_opacity=o).move_to(n[0]) for r,o in ((.42,.08),(.35,.16),(.29,.3))])
        n.add_to_back(glow)
        root=poly([(-1.3,-.65),(-.85,-1.35),(.3,-1.65),(4.8,-1.65)],BLUE,8)
        self.add(c)
        self.at('spinal cord'); self.play(Indicate(c[0]),run_time=.4)
        self.at('at cells'); self.play(FadeIn(n),Create(root),Flash(n[1],color=BLUE),run_time=.65)
        self.at('alpha motor neurons'); self.play(FadeIn(label('alpha motor neuron',3.35,.9,32,BLUE)),Create(Line(P(2.2,.5),P(-1.55,-.38),color=BLUE)),FadeIn(label('ventral root',3.4,-2.15,28)),Create(Line(P(3.4,-1.9),P(3.4,-1.65),color=TEXT)),run_time=.5)
        self.finish()

class S03Unit(SpokenScene):
    def construct(self):
        n,a,f,b=unit(); self.add(n,a,f,label('other fibres',4,-3.1,26,GREY))
        self.at("Each motor neuron's"); self.play(Indicate(n),run_time=.5)
        self.at('axon branches'); self.play(Create(b),run_time=1)
        self.at('The neuron and'); self.play(*[f[i].animate.set_stroke(BLUE).set_fill(BLUE,opacity=.3) for i in range(6)],run_time=.6)
        bracket=poly([(-5.85,2.45),(-5.85,-1.32),(5.35,-1.32),(5.35,2.45)],BLUE,3)
        self.at('one motor unit'); self.play(Create(bracket),FadeIn(label('motor unit: neuron + its fibres',0,3.2,32,BLUE)),run_time=.45)
        self.finish()

class S04Spike(SpokenScene):
    def construct(self):
        n,a,f,b=unit(); self.add(n,a,f,b,label('one motor unit',0,3.2,32,BLUE),label('other fibres',4,-3.1,26,GREY))
        for i in range(6): f[i].set_stroke(BLUE).set_fill(BLUE,opacity=.3)
        d=Dot(a.get_start(),color=YELLOW,radius=.16); self.add(d)
        self.at('One spike'); self.play(MoveAlongPath(d,a),run_time=.7,rate_func=linear); self.remove(d)
        ds=VGroup(*[Dot(p.get_start(),color=YELLOW,radius=.13) for p in b]); self.add(ds)
        self.play(*[MoveAlongPath(dot,path) for dot,path in zip(ds,b)],run_time=.65,rate_func=linear); self.remove(ds)
        self.at('every fiber'); self.play(*[f[i].animate.set_fill(GREEN,opacity=.8).set_stroke(GREEN).stretch(.9,0) for i in range(6)],run_time=.4)
        self.at('unit twitch'); self.play(*[f[i].animate.stretch(1/.9,0) for i in range(6)],run_time=.35)
        self.finish()

class S05Pool(SpokenScene):
    def construct(self):
        region=RoundedRectangle(width=5.1,height=5.3,corner_radius=.8,color=GREY,fill_color=GREY,fill_opacity=.08).move_to(P(-3.2,0))
        ns=VGroup(*[neuron(-3.5,y,r) for y,r in zip((1.55,0,-1.55),(.35,.5,.65))])
        ring=DashedVMobject(Ellipse(width=3.5,height=4.9,color=BLUE).move_to(P(-3.35,0)),num_dashes=40)
        f=fibres(4,7)
        paths=VGroup(*[poly([(-3.5+r,y),(-.7,y),(2.7,target)]) for y,r,target in zip((1.55,0,-1.55),(.35,.5,.65),(1.7,.05,-1.6))])
        self.add(region,ns,label('ventral horn · enlarged',-3.1,3.15,28))
        self.at('All the motor neurons'); self.play(Indicate(ns),run_time=.5)
        self.at('supply one muscle'); self.play(Create(paths),FadeIn(f),FadeIn(label('one muscle',4,2.7,30)),run_time=.6)
        self.at('motor pool'); self.play(Create(ring),FadeIn(label('motor pool',-3.2,-3.05,32,BLUE)),run_time=.4)
        self.finish()

class S06Converge(SpokenScene):
    def construct(self):
        n,gs=inputs(); self.add(n,label('motor neuron',1,-1.65,28,BLUE))
        for cue,g in zip(('the brain','stretch sensors','pain','rhythm circuits'),gs):
            self.at(cue); self.play(FadeIn(g),run_time=.32)
        self.add(label('Only the spindle arrow lands directly',0,-3.4,28,TEAL))
        self.finish()

class S07FinalPath(SpokenScene):
    def construct(self):
        n,gs=inputs(); self.add(n,*gs,label('motor neuron',1,-1.65,28,BLUE),label('Only the spindle arrow lands directly',0,-3.4,28,TEAL))
        self.at('All of them'); dots=VGroup(*[Dot(g[1][0].get_start(),color=YELLOW,radius=.12) for g in gs]); self.add(dots)
        self.play(*[MoveAlongPath(d,g[1][0]) for d,g in zip(dots,gs)],run_time=.8); self.remove(dots)
        self.play(*[g[1].animate.set_stroke(opacity=.3) for g in gs],Indicate(n),run_time=.2)
        ax=Arrow(P(2.05,0),P(4.1,0),color=BLUE,buff=0); f=fibres(5.1,3).scale(.55).move_to(P(5.2,0))
        self.at('the motor neurons'); self.play(GrowArrow(ax),FadeIn(f),FadeIn(label('muscle',5.2,-.95,28,GREY)),run_time=.6)
        self.at('called them'); self.play(FadeIn(label('the final common path',3.7,2.25,30,BLUE)),FadeIn(label('Sherrington',3.7,2.85,26,GREY)),Create(Line(P(3.7,1.9),P(3.2,.15),color=BLUE)),run_time=.5)
        self.finish()

class S08Bar(SpokenScene):
    def construct(self):
        n=neuron(-1.5,0,1.05); g=gauge(.8,1)
        self.add(n,label('motor neuron',-1.5,-1.75,28,BLUE))
        self.at('voltage as a bar'); self.play(FadeIn(VGroup(g[0],g[1])),FadeIn(label('voltage change\nfrom rest',3.6,-.2,30)),run_time=.6)
        self.at('line at threshold'); self.play(Create(g[2]),FadeIn(label('threshold',3.4,1.65,30,YELLOW)),run_time=.4)
        self.finish()

class S09Push(SpokenScene):
    def construct(self):
        g=inhibition_panel(-3.1,1); e=excitation(-3.1); self.add(g)
        self.at('Excitation pushes'); self.play(FadeIn(e),Transform(g[0][1],voltage(-3.1,3.35)),run_time=1.5)
        self.at('Inhibition holds'); self.play(FadeIn(inhibition(-3.1)),Transform(g[0][1],voltage(-3.1,1.6)),run_time=.8)
        self.finish()

class S09bShunt(SpokenScene):
    def construct(self):
        g=inhibition_panel(-3.1,1.6); self.add(g,excitation(-3.1),inhibition(-3.1))
        self.at('pulls the bar down'); self.play(Transform(g[0][1],voltage(-3.1,.7)),FadeIn(label('downward pull',-3.1,2.8,30,RED)),run_time=.65)
        right=inhibition_panel(3.15,.7)
        ghost=voltage(3.15,3.35).set_fill(BLUE,opacity=.12).set_stroke(BLUE,width=2,opacity=.5)
        channels=VGroup(*[VGroup(Line(P(3.58,y-.18),P(3.58,y+.18),color=BG,stroke_width=12),Line(P(3.46,y-.18),P(3.7,y-.18),color=RED,stroke_width=3),Line(P(3.46,y+.18),P(3.7,y+.18),color=RED,stroke_width=3),Arrow(P(3.29,y),P(4.38,y),color=RED,buff=0,stroke_width=4)) for y in (-1.3,-.5,.3)])
        self.at('open channels'); self.play(FadeIn(right),FadeIn(ghost),FadeIn(channels),FadeIn(label('inhibition opens channels',3.1,3.25,28,RED)),FadeIn(excitation(3.15)),run_time=.5)
        self.at('also blunt excitation'); self.play(Transform(right[0][1],voltage(3.15,1.65)),FadeIn(label('blunted rise',3.15,2.65,28,RED)),run_time=.55)
        self.play(FadeIn(label('less likely to fire',0,-3.5,30,RED)),run_time=.2)
        self.finish()

class S10Fire(SpokenScene):
    def construct(self):
        n=neuron(-3.7,0,.85); g=gauge(-1.6,1); f=fibres(4.6,3)
        ax=Line(P(-2.85,0),P(-2.3,0),color=BLUE)
        out=poly([(-2.3,0),(-2.3,-2.55),(1.6,-2.55),(1.6,.8),(3.3,.8)])
        branches=VGroup(*[Line(P(3.3,.8),f[i].get_left(),color=BLUE) for i in range(3)])
        self.add(n,g,f,ax,out,branches,label('threshold',.4,1.65,28,YELLOW),label('voltage change from rest',-2.5,-3.25,28),label('Steady or slowly rising input',0,3.35,28,GREY),label('net current × input resistance → threshold',0,2.75,30))
        self.at('net current'); self.play(Transform(g[1],voltage(-1.6,4.0)),run_time=1.65)
        self.at('cell fires'); d=Dot(out.get_start(),color=YELLOW,radius=.15); self.add(d)
        self.play(Flash(n[0],color=YELLOW),MoveAlongPath(d,out),run_time=.5); self.remove(d)
        self.play(f.animate.set_stroke(GREEN).set_fill(GREEN,opacity=.65).stretch(.9,0),run_time=.25)
        self.finish()

def question_pools():
    g=VGroup()
    for x,col in ((-2.4,GREEN),(2.4,RED)):
        g.add(DashedVMobject(Ellipse(width=3.3,height=2.3,color=BLUE).move_to(P(x,-1.6)),num_dashes=28))
        g.add(*[neuron(x+dx,-1.65+dy,r) for dx,dy,r in ((-.8,.4,.28),(.65,.4,.34),(0,-.5,.36))])
        g.add(Arrow(P(x+1.95,-2.6 if col==GREEN else -.7),P(x+1.95,-.7 if col==GREEN else -2.6),color=col,buff=0))
    return g

def questions(second=False):
    g=VGroup(label('1',-5.6,1.8,56,YELLOW),label('Which motor pools?',0,2.35,40),label('does the circuit push up or down?',0,1.5,34),label('Push up',-2.4,.45,38,GREEN),label('Down',2.4,.45,38,RED))
    g[4].align_to(g[3],UP)
    if second: g.add(label('2',-5.6,-1.9,56,YELLOW),label('Within a pool,',0,-1.45,36),label('which cells reach threshold first?',0,-2.4,36))
    return g

class S11TwoQuestions(SpokenScene):
    def construct(self):
        g=questions(); self.add(g,question_pools())
        self.at('Which motor pools'); self.play(Indicate(g[1],scale_factor=1.04),run_time=.6)
        self.finish()
class S12Second(SpokenScene):
    def construct(self):
        g=questions(True); pools=question_pools(); self.add(*g[:5],pools)
        self.at('within a pool'); self.play(FadeOut(pools),run_time=.15); self.play(FadeIn(VGroup(*g[5:])),run_time=.25)
        self.finish()
class S13Setup(SpokenScene):
    def construct(self):
        g,bs,ns=pool(); self.add(g,label('voltage change from rest',0,3.25,30))
        self.at('small cells'); self.play(Indicate(ns[0]),run_time=.4)
        self.at('weak units'); self.play(Indicate(g[0][5]),run_time=.4)
        self.at('large cells'); self.play(Indicate(ns[2]),run_time=.4)
        self.at('strong units'); self.play(Indicate(g[2][5]),run_time=.4)
        self.finish()
class S14Predict(SpokenScene):
    def construct(self):
        g,bs,ns=pool(shared=True); self.add(g)
        self.at('rises a little'); self.play(g[4][1].animate.rotate(-.7,about_point=P(-5.8,3.15)),run_time=1.1)
        self.at('Which cells fire'); self.play(FadeIn(label('Which fires first?',0,-3.5,32)),run_time=.3)
        self.finish()
class S15Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        g,_,_=prediction(); self.add(g); self.wait(5)
class S16Reveal(SpokenScene):
    def construct(self):
        g,bs,ns=pool(shared=True); g[4][1].rotate(-.7,about_point=P(-5.8,3.15)); self.add(g)
        # Equal I, R=[1,.5,.25], common threshold 3.7: crossing currents 3.7,7.4,14.8.
        drive=ValueTracker(.35); rs=np.array([1.,.5,.25])
        for b,x,r in zip(bs,(-3.83,.52,4.87),rs):
            b.add_updater(lambda m,x=x,r=r: m.become(voltage(x,min(4.1,drive.get_value()*r))))
        self.at('The small ones'); self.play(drive.animate.set_value(3.95),run_time=.45,rate_func=linear)
        self.play(Flash(ns[0][0],color=YELLOW),FadeIn(label('1st',-5,.25,24,YELLOW)),run_time=.2)
        self.play(drive.animate.set_value(7.9),run_time=.3,rate_func=linear)
        self.play(Flash(ns[1][0],color=YELLOW),FadeIn(label('2nd',-.65,.25,24,YELLOW)),run_time=.2)
        self.play(drive.animate.set_value(15.8),run_time=.3,rate_func=linear)
        self.play(Flash(ns[2][0],color=YELLOW),FadeIn(label('3rd',3.7,.25,24,YELLOW)),run_time=.25)
        for b in bs: b.clear_updaters()
        self.at('Many people guess'); thought=chip('Guess: big = strong = first?',GREY,26,pad=.1).move_to(P(0,-3.5)); self.play(FadeIn(thought),run_time=.25)
        self.at('big seems strong'); x=thought.get_left()[0]-.38
        rejection=VGroup(Line(P(x-.13,-3.63),P(x+.13,-3.37),color=RED,stroke_width=4),Line(P(x-.13,-3.37),P(x+.13,-3.63),color=RED,stroke_width=4))
        self.play(Create(rejection),run_time=.3)
        self.finish()
class S17Why(SpokenScene):
    def construct(self):
        g,bs,_=pool(shared=True,units=False); self.add(g)
        self.at('moves the voltage'); self.play(*[Transform(b,voltage(x,1.8*r)) for b,x,r in zip(bs,(-3.83,.52,4.87),(1,.5,.25))],run_time=.7)
        self.at('The same input'); self.play(*[Transform(b,voltage(x,3.6*r)) for b,x,r in zip(bs,(-3.83,.52,4.87),(1,.5,.25))],FadeIn(label('Same input, bigger voltage change in the small cell',0,-3.35,30,YELLOW)),*[FadeIn(label(s,x,-2.85,28,BLUE)) for s,x in zip(('100%','50%','25%'),(-4.35,0,4.35))],run_time=.7)
        self.finish()
class S18Resistance(SpokenScene):
    def construct(self):
        cells=VGroup(); exits=VGroup()
        for x,r,k in ((-3.3,1.1,3),(3.2,1.8,8)):
            center=P(x,.1)
            cell=VGroup(Circle(r,stroke_width=0,fill_color=BLUE,fill_opacity=.1).move_to(center))
            angles=np.linspace(0,TAU,k,endpoint=False)+(PI/8 if k==8 else 0)
            half_gap=.15/r
            for t in angles:
                cell.add(Arc(radius=r,start_angle=t+half_gap,angle=TAU/k-2*half_gap,arc_center=center,color=BLUE,stroke_width=9))
                d=P(np.cos(t),np.sin(t)); tangent=P(-np.sin(t),np.cos(t)); p=center+r*d
                exits.add(VGroup(*[Line(p+tangent*side*.15-d*.13,p+tangent*side*.15+d*.13,color=BLUE,stroke_width=4) for side in (-1,1)],Arrow(p-d*.25,p+d*.57,color=YELLOW,buff=0,stroke_width=4)))
            cells.add(cell)
        self.add(cells,label('small cell',-3.3,3.2,32,BLUE),label('large cell',3.2,3.2,32,BLUE))
        for x,r in ((-3.3,1.1),(3.2,1.8)):
            self.add(label('membrane',x,2.55,26,BLUE),Line(P(x,2.3),P(x+r*np.cos(PI*.55),.1+r*np.sin(PI*.55)),color=BLUE,stroke_width=2))
        self.at('fewer ways'); self.play(FadeIn(exits),FadeIn(label('fewer exits',-3.3,-1.65,28,YELLOW)),FadeIn(label('more exits',3.2,-2.3,28,YELLOW)),run_time=.6)
        self.at('input resistance is higher'); self.play(FadeIn(label('higher Rᵢₙ',-3.3,-2.8,32)),FadeIn(label('lower Rᵢₙ',3.2,-2.8,32)),run_time=.5)
        self.finish()
class S19Bathtub(SpokenScene):
    def construct(self):
        waters=[]; streams=VGroup()
        for x,k in ((-3.25,2),(3.25,6)):
            tub=poly([(x-2.15,1.6),(x-2.15,-1.9),(x+2.15,-1.9),(x+2.15,1.6)],GREY,7)
            tap=poly([(x-.8,2.15),(x-.8,2.8),(x,2.8),(x,2.25)],GREY,8)
            w=Rectangle(width=4.1,height=.35,stroke_width=0,fill_color=BLUE,fill_opacity=.5).move_to(P(x,-1.7)); waters.append(w)
            drains=VGroup()
            for dx in np.linspace(-1.65,1.65,k):
                drains.add(poly([(x+dx-.13,-1.7),(x+dx-.13,-2.2),(x+dx+.13,-2.2),(x+dx+.13,-1.7)],GREY,3))
                streams.add(Arrow(P(x+dx,-2.2),P(x+dx,-2.65),color=BLUE,buff=0,stroke_width=3))
            streams.add(Line(P(x,2.2),P(x,.5),color=BLUE,stroke_width=8))
            self.add(w,tub,tap,drains,label('2 drains' if k==2 else 'many drains',x,-2.95,28))
        self.add(label('same inflow',0,3.35,32,BLUE))
        self.at('fewer drains'); self.play(Indicate(waters[0]),run_time=.4)
        self.at('same inflow'); self.play(FadeIn(streams),run_time=.3)
        # Q=5.4, k=2 or 6, equilibrium h=Q/k.
        self.at('raises the water',lead=.5); self.play(*[Transform(w,Rectangle(width=4.1,height=5.4/k,stroke_width=0,fill_color=BLUE,fill_opacity=.5).move_to(P(x,-1.85+5.4/k/2))) for w,x,k in zip(waters,(-3.25,3.25),(2,6))],FadeIn(label('fewer drains = higher Rᵢₙ',0,-3.55,28,YELLOW)),run_time=.4)
        self.finish()
class S20Formula(SpokenScene):
    def construct(self):
        box=RoundedRectangle(width=10.8,height=4.45,corner_radius=.2,color=BLUE).move_to(P(0,.1))
        self.add(box,label('Steady or slowly rising input',0,3.05,30,GREY),label('ΔV = I × Rᵢₙ',0,1.2,60),label('Iₜₕ = ΔVₜₕ / Rᵢₙ',0,-.2,52),label('Equal required voltage changes',0,-1.55,30,GREY))
        self.at("Ohm's law"); self.play(Indicate(box),run_time=.5)
        self.at('Higher input resistance'); self.play(FadeIn(label('Higher Rᵢₙ → less current → earlier recruitment',0,-2.9,32,YELLOW)),run_time=.5)
        self.finish()
class S21Order(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,4.8,1],y_range=[0,3.4,1],x_length=10.5,y_length=4.6,axis_config={'include_ticks':False,'color':GREY}).move_to(P(.25,-.05))
        self.add(ax,label('The size principle',0,3.35,36,BLUE),label('Henneman · cats · 1957',3.5,2.75,26,GREY),label('shared input →',0,-2.85,28),label('units active',-5.4,2.9,26))
        for v in (1,2,3): self.add(label(str(v),ax.c2p(0,v)[0]-.3,ax.c2p(0,v)[1],26))
        # Recruitment from I_th=1/R, R=[1,.5,.25].
        self.at('That order')
        for i,(lo,hi,name) in enumerate(((1,2,'small'),(2,4,'medium'),(4,4.7,'large'))):
            pts=[ax.c2p(0 if i==0 else lo, i),ax.c2p(lo,i),ax.c2p(lo,i+1),ax.c2p(hi,i+1)]
            path=VMobject(color=BLUE,stroke_width=6).set_points_as_corners(pts)
            pos=ax.c2p((lo+hi)/2,i+1)+UP*.32
            self.play(Create(path),FadeIn(label(name,pos[0],pos[1],28,BLUE)),run_time=.5)
        self.at('strong tendency'); self.play(FadeIn(label('Shared input: a strong tendency, not a law',0,-3.5,28,YELLOW)),run_time=.4)
        self.finish()
class S22Catch(SpokenScene):
    def construct(self):
        a,b=neuron(-3.2,0,.8),neuron(3,0,1.7)
        self.add(a,b,label('small cell',-3.2,2.85,32,BLUE),label('large cell',3,2.85,32,BLUE))
        dots=VGroup(); arrows=VGroup()
        for x,r,k in ((-3.2,.8,3),(3,1.7,9)):
            for t in np.linspace(-PI*.45,PI*1.4,k):
                p=P(x+r*np.cos(t),r*np.sin(t)); d=P(np.cos(t),np.sin(t))
                dots.add(Dot(p,radius=.11,color=BLUE)); arrows.add(Arrow(p+d*.65,p,buff=.12,color=YELLOW,stroke_width=3))
        self.at('A large cell'); self.play(Indicate(b),run_time=.45)
        self.at('more synapses'); self.play(FadeIn(dots),FadeIn(label('more membrane, more synapses',0,-2.65,32,BLUE)),run_time=.45)
        self.at('collect more input'); self.play(*[GrowArrow(a) for a in arrows],run_time=.5)
        self.finish()
class S22bCondition(SpokenScene):
    def construct(self):
        # A in [1,10]. Exact log10 power laws: alpha=.5, beta=1 (lesson table).
        ax=Axes(x_range=[0,1,.5],y_range=[-1.05,.6,.5],x_length=6.5,y_length=4.3,axis_config={'include_ticks':False,'color':GREY}).move_to(P(-2.7,.1))
        self.add(ax,label('hypothetical example · log scales',0,3.45,32),label('cell size A →',-2.3,1.02,24),label('relative value',-4.65,2.98,26,GREY))
        for x,s in ((0,'1'),(.5,'3.16'),(1,'10')):
            p=ax.c2p(x,0); self.add(Line(p,p+DOWN*.1,color=GREY),label(s,p[0],p[1]-.27,24))
        cur=ax.plot(lambda x:.5*x,x_range=[0,1],color=YELLOW)
        res=ax.plot(lambda x:-x,x_range=[0,1],color=BLUE)
        prod=ax.plot(lambda x:-.5*x,x_range=[0,1],color=GREEN)
        self.at('In this simple model'); self.add(label('Equal ΔVₜₕ assumed',3.95,2.8,27,GREY))
        self.at('effective current grows'); self.play(Create(cur),Create(Line(ax.c2p(1,.5),P(3.25,1.75),color=YELLOW,stroke_width=2)),FadeIn(label('Iₑff ∝ Aᵅ',4.35,1.75,32,YELLOW,font='Georgia')),FadeIn(label('alpha: current growth = 0.5',3.9,1.1,24,YELLOW)),run_time=.8)
        self.at('input resistance falls'); self.play(Create(res),Create(Line(ax.c2p(1,-1),P(3.25,-1.9),color=BLUE,stroke_width=2)),FadeIn(label('Rᵢₙ ∝ A⁻ᵝ',4.35,-1.9,32,BLUE,font='Georgia')),FadeIn(label('beta: resistance fall = 1',3.9,-2.55,24,BLUE)),run_time=.6)
        self.play(Create(prod),Create(Line(ax.c2p(1,-.5),P(3.25,.15),color=GREEN,stroke_width=2)),FadeIn(label('ΔV ∝ Aᵅ⁻ᵝ',4.35,.15,32,GREEN,font='Georgia')),FadeIn(label('alpha < beta',4.2,-.95,30,YELLOW)),run_time=.6)
        self.at('Real current distributions'); self.play(FadeIn(label('Cat medial gastrocnemius: mean homonymous Ia effective current',0,-3.2,26,GREY)),FadeIn(label('was larger in high-resistance cells; pathway matters.',0,-3.65,26,GREY)),run_time=.4)
        self.finish()
class S22cStill(SpokenScene):
    def construct(self):
        g,bs,ns=pool(shared=True,units=False); self.add(g,label('input higher · equal thresholds assumed',0,-3.25,30,YELLOW))
        self.at('equal thresholds'); self.play(g[4][1].animate.rotate(-.8,about_point=P(-5.8,3.15)),run_time=.4)
        self.at('small cells still'); self.play(*[Transform(b,voltage(x,3.95*a**(-.5))) for b,x,a in zip(bs,(-3.83,.52,4.87),(1,2,4))],Flash(ns[0][0],color=YELLOW),run_time=.7)
        self.finish()
class S23Rate(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,8.2,1],y_range=[0,2.7,1],x_length=10.8,y_length=4.65,axis_config={'include_ticks':False,'color':GREY}).move_to(P(.2,.05))
        self.add(ax,label('one active motor unit · rate coding',0,3.35,34,BLUE),label('time →',0,-3.45,28),label('force',-5.5,2.85,28,GREEN),label('spikes',-5.3,-2.95,28,YELLOW))
        times=np.array([.2,1.65,3.1,3.45,3.8,4.15,4.5])
        def force(t):
            d=t-times; d=d[d>=0]; return float(np.sum((d/.32)*np.exp(1-d/.32)))
        sparse=ax.plot(force,x_range=[0,2.9,.01],color=GREEN)
        dense=ax.plot(force,x_range=[2.9,8.2,.01],color=GREEN)
        spikes=VGroup(*[Line(ax.c2p(t,0)+DOWN*.45,ax.c2p(t,0)+DOWN*.12,color=YELLOW,stroke_width=4) for t in times])
        self.at('add force'); self.play(Create(sparse),Create(VGroup(*spikes[:2])),run_time=.7)
        self.at('Active units fire faster'); self.play(Create(VGroup(*spikes[2:])),Create(dense),run_time=1.35)
        self.at('twitches add up'); self.play(FadeIn(label('Closer spikes: twitches add up',1.3,2.6,28,GREEN)),run_time=.25)
        self.finish()
class S24Takeaway(SpokenScene):
    def construct(self):
        title=VGroup(label('Every command ends as synaptic',0,2.25,36),label('current on motor neurons.',0,1.5,36,BLUE))
        self.add(title)
        self.at('Which pools go'); self.play(FadeIn(label('Which pools go up, which down?',0,.35,34)),run_time=.25)
        self.at('who fires first',lead=.85); self.play(FadeIn(label('Within a pool, who reaches threshold first?',0,-.95,32)),run_time=.25)
        self.play(FadeIn(label('Force grows by recruitment and faster firing.',0,-2.3,32,GREEN)),run_time=.25)
        self.finish()
class S25End(EndCard):
    LINE='Every command ends as current on motor neurons.'
    def construct(self):
        line=fit(T(self.LINE,40,font=TITLE_FONT),max_w=11.5).move_to(P(0,.25))
        self.play(FadeIn(line),FadeIn(label('biochemistrypedia.com',0,-.7,26,TEAL)),run_time=.4)
        self.finish()
    def finish(self):
        if self.narration_s>self.elapsed(): self.wait(self.narration_s-self.elapsed())
