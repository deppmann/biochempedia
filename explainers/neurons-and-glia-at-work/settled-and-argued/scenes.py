"""Settled and Argued — review polish round.
COLOR MAP: YELLOW neurons; BLUE potassium; GREEN astrocytes; TEAL prompts;
PURPLE glutamate/transporters; PINK calcium; RED deletion; GREY structure.
Traces are explicitly illustrative models, never represented as study recordings.
Pulse: first-order clearance dC/dt=-C/tau after a release impulse.
Response: normalized difference of exponentials, identical control/KO parameters.
Seizure illustration: a deterministic gated oscillation, not measured EEG.
"""
import numpy as np
from bp_style import *

NEUR, KC, ASTRO, BAD = YELLOW, BLUE, GREEN, RED
GLU, CA = '#B896F4', '#FF94C2'
LIGHT = '#C9CFDA'

class TimedScene(SpokenScene):
    # The shared sync.log records pre-wait time, not actual cue onset. Use exact
    # word onsets, with no anticipatory lead; keep task read-only files untouched.
    def at(self, phrase, lead=0, nth=0):
        target = self.t_of(phrase, nth)
        rest = target-self.elapsed()
        if rest > .001:
            self.wait(rest)


def txt(s,x,y,size=28,color=TEXT):
    return T(s,size,color,line_spacing=1.15).move_to([x,y,0])

def head(s,color=TEXT):
    return txt(s,0,3.4,34,color)

def line(a,b,color=LIGHT,w=2):
    return Line([*a,0],[*b,0],color=color,stroke_width=w)

def arrow(a,b,color=GLU):
    return Arrow([*a,0],[*b,0],buff=.08,color=color,stroke_width=5)

def cross(x,y,s=.22):
    return VGroup(line((x-s,y-s),(x+s,y+s),BAD,5),line((x-s,y+s),(x+s,y-s),BAD,5))

def badge(s,color,size=28):
    g=chip(s,color,size);g[0].set_fill(BG,opacity=1);return g

def emphasis(g,alpha):
    g.set_stroke(opacity=alpha)
    g[0].set_fill(opacity=0)
    g[1].set_fill(ASTRO,opacity=.3*alpha)
    g[2].set_fill(opacity=0)
    return g

def box(w,h,x,y,color=LIGHT):
    return RoundedRectangle(width=w,height=h,corner_radius=.18,color=color,
        fill_color=color,fill_opacity=.06).move_to([x,y,0])

def astro_cell():
    # One continuous cup-shaped astrocyte, used at every scale in this film.
    sheath=VMobject(color=ASTRO,stroke_width=22)
    sheath.set_points_smoothly([[1.8,2,0],[-.6,2.35,0],[-2.6,1.65,0],
        [-3,0,0],[-2.6,-1.65,0],[-.6,-2.35,0],[1.8,-2,0]])
    soma=Ellipse(width=1.8,height=1.8,color=ASTRO,fill_color=ASTRO,fill_opacity=.3).move_to([-2.5,0,0])
    branches=VGroup()
    for a,b,c in [((-2.7,1),(-3.7,1.8),(-4.15,1.65)),
                  ((-3,.3),(-4.1,.8),(-4.45,1.2)),
                  ((-3,-.6),(-4,-1.1),(-4.35,-.8)),
                  ((-2.4,-1.7),(-3.4,-2.4),(-3.85,-2.2))]:
        branches.add(line(a,b,ASTRO,6),line(b,c,ASTRO,3))
    # Fine side branches carry spatially independent calcium microdomains.
    for a,b in [((-3.45,1.6),(-3.1,2.02)),
                ((-3.8,.65),(-3.65,1.12)),
                ((-3.65,-.9),(-3.35,-.48)),
                ((-3.05,-2.15),(-2.9,-1.68))]:
        branches.add(line(a,b,ASTRO,2.5))
    return VGroup(sheath,soma,branches)

def synapse(labels=True):
    cell=astro_cell()
    pre=Ellipse(width=3.5,height=1.5,color=NEUR,fill_color=NEUR,fill_opacity=.1).move_to([.1,1,0])
    post=box(3.5,1.3,.1,-1.05,NEUR)
    g=VGroup(cell,pre,post)
    if labels:
        g.add(txt('presynaptic\nterminal',.1,1,26,NEUR),txt('postsynaptic\ncell',.1,-1.05,26,NEUR),
            txt('astrocyte',-3.1,2.75,28,ASTRO),txt('cleft',3,.05,28,LIGHT),
            line((2.5,.05),(1.1,.05)))
    return g

def particles():
    return VGroup(*[Dot([x,.02,0],radius=.095,color=GLU) for x in [-.75,-.05,.65]])

def flicker(dots):
    for i,d in enumerate(dots):
        d.phase=i*2.399
        d.frequency=4.1+i*1.37
        def update(m,dt):
            m.phase += dt*m.frequency
            m.set_fill(opacity=.18+.82*max(0,np.sin(m.phase))**2)
        d.add_updater(update)
    return dots


def ca_dots():
    return VGroup(*[Dot([x,y,0],radius=.075,color=CA) for x,y in
        [(-3.28,1.81),(-3.73,.89),(-3.50,-.69),(-2.97,-1.91),
         (-3.91,1.73),(-4.25,1.0),(-4.16,-.95),(-3.63,-2.30)]])


# Shared large stage: 5.7 units tall (about 75% of the safe frame).
STAGE_SCALE=1.2

def stage_point(x,y):
    return np.array([(x+1.3)*STAGE_SCALE,y*STAGE_SCALE,0])


def stage_synapse(labels=True):
    g=synapse(False).scale(STAGE_SCALE,about_point=ORIGIN).shift(RIGHT*1.3*STAGE_SCALE)
    if labels:
        g.add(txt('astrocyte',-4.8,2.8,28,ASTRO),
              txt('presynaptic\nterminal',*stage_point(.1,1)[:2],26,NEUR),
              txt('postsynaptic\ncell',*stage_point(.1,-1.05)[:2],26,NEUR),
              txt('cleft',5.2,.05,28,LIGHT),line((4.6,.05),(3.1,.05)))
    return g


def stage_calcium():
    return ca_dots().scale(STAGE_SCALE,about_point=ORIGIN).shift(RIGHT*1.3*STAGE_SCALE)


def knockout(center=(0,0),scale=1):
    return astro_cell().scale(scale).move_to([*center,0])

def pulse_value(t):
    return .025 + (np.exp(-(t-1)/.48) if t >= 1 else 0)

def curve(points,color=GLU,w=5):
    return VMobject(color=color,stroke_width=w).set_points_as_corners(points)

def pulse_panel():
    # Panel coordinates; no inferred physical units or measured amplitudes.
    ax=VGroup(line((1.9,-2.1),(6,-2.1)),line((1.9,-2.1),(1.9,1.75)))
    labels=VGroup(txt('outside glutamate',4,2.25,28,GLU),txt('time (schematic)',4,-2.65,26),
        txt('low',1.4,-1.95,26),txt('rise',1.4,1.3,26))
    ts=np.linspace(0,4,241)
    pts=[[2+t*.93,-2+3.2*pulse_value(t),0] for t in ts]
    path=curve(pts)
    dot=Dot(pts[0],radius=.11,color=GLU)
    for item in (ax,path,dot):
        item.stretch(.65,0,about_point=np.array([6.5,0,0]))
    labels=VGroup(txt('outside glutamate',4.95,2.25,26,GLU),
        txt('time (schematic)',4.95,-2.95,26),
        txt('low',3.85,-2.4,26),txt('rise',3.95,1.6,26))
    return VGroup(ax,labels,path,dot)

def syn_left():
    return synapse(False).scale(1.2).move_to([-.55,0,0])

def question():
    return VGroup(box(11.7,5.8,0,0),txt('Pause',0,2.1,30,TEAL),
        txt('Does a null result\nprove no release?',0,.25,46))

def ko_context():
    cell=stage_synapse(False)
    title=txt('IP3R2 deleted',0,3.35,34,BAD)
    receptor=badge('IP3R2',CA,26).move_to(stage_point(-2.25,0))
    x=cross(-1.14,0,.48)
    return VGroup(cell,title,receptor,x,txt('adult mice',5,2.6,30),
        txt('astrocyte',-4.9,2.65,28,ASTRO))

def field():
    cells=VGroup(*[emphasis(astro_cell().scale(.33).move_to([x,y,0]),.3)
        for y in [1.15,-1.2] for x in [-4.6,-1.55,1.55,4.6]])
    return cells

def subgroup():
    g=field();emphasis(g[1],1);return g

def glow(x,y):
    return VGroup(*[Dot([x,y,0],radius=r,color=GLU,fill_opacity=o,stroke_width=0)
        for r,o in [(.34,.08),(.24,.16),(.14,.8)]])

def hot_pair(x,y):
    return VGroup(glow(x+2.35,y+.45),glow(x+2.35,y-.45))

def lists():
    frames=VGroup(box(5.8,4.7,-3.1,.95,ASTRO),box(5.8,4.7,3.1,.95,GLU))
    titles=VGroup(txt('Settled',-3.1,2.65,38,ASTRO),txt('Argued',3.1,2.65,38,GLU))
    left=VGroup(txt('Astrocytes clear',-3.1,1.55,32),txt('K+ and glutamate',-3.1,.65,32,ASTRO),
        txt('shares still debated',-3.1,-.55,28,LIGHT))
    right=VGroup(txt('Fast gliotransmission',3.1,1.55,29,GLU),
        txt('IP3R2 null result',3.1,.55,28),txt('VGLUT1 subgroup',3.1,-.35,28))
    return VGroup(frames,titles,left,right)

class S00Title(TitleCard):
    LESSON='Neurons and Glia at Work'
    TITLE='Settled and Argued'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON.upper(),26,LIGHT),
            T(self.TITLE,54,font=TITLE_FONT),Line(LEFT*1.3,RIGHT*1.3,color=GOLD)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.5);self.finish()

class S01Question(TimedScene):
    def construct(self):
        self.add(stage_synapse())
        self.at('astrocytes clear')
        k=chip('K+',KC,28).move_to([5,-2.4,0])
        self.play(FadeIn(k),run_time=.3)
        self.at('glutamate')
        d=particles().scale(STAGE_SCALE,about_point=ORIGIN).shift(RIGHT*1.56);label=txt('glutamate',5.1,1.7,28,GLU)
        leader=line((4.2,1.45),(2.4,.18),GLU)
        self.play(FadeIn(d),FadeIn(label),Create(leader),run_time=.3)
        self.play(d.animate.shift(LEFT*2),FadeOut(k),run_time=.5)
        self.play(FadeOut(d),FadeOut(label),FadeOut(leader),run_time=.2)
        self.at('do they also')
        self.play(FadeIn(txt('Fast signals of their own?',0,-3.5,34)),run_time=.3)
        self.finish()

class S02Glu(TimedScene):
    def construct(self):
        self.add(syn_left(),head('Small space outside → big change outside'))
        self.add(txt('astrocyte + synapse',-.55,-3.25,28,ASTRO))
        p=pulse_panel();self.add(p[0],p[1],p[3])
        self.at('glutamate follows')
        self.play(Create(p[2]),MoveAlongPath(p[3],p[2]),run_time=1.9,rate_func=linear)
        self.at('even more sharply')
        self.play(Indicate(p[2],color=GLU),run_time=.6);self.finish()

class S03Why(TimedScene):
    def construct(self):
        p=pulse_panel();self.add(syn_left(),p[0],p[1],p[3])
        title=head('Low between releases',GLU);self.add(title)
        self.at('transporters keep')
        gate=badge('transporter',GLU,26).move_to([-1.3,-3.25,0])
        self.play(FadeIn(gate),Create(line((-1.3,-2.9),(-1.6,-2.55),GLU)),run_time=.3)
        self.at('each release makes')
        baseline=curve([[2,-2+3.2*.025,0],[2+.93,-2+3.2*.025,0]]).stretch(.65,0,about_point=np.array([6.5,0,0]))
        self.play(Create(baseline),p[3].animate.move_to(baseline.get_end()),run_time=.35)
        self.at('large')
        peak=[6.5+.65*(2+.93-6.5),-2+3.2*pulse_value(1),0]
        rise=curve([baseline.get_end(),peak])
        self.play(Create(rise),p[3].animate.move_to(peak),
            Transform(title,head('Brief local rise',GLU)),run_time=.15)
        self.at('brief rise')
        tail=curve([[6.5+.65*(2+t*.93-6.5),-2+3.2*pulse_value(t),0] for t in np.linspace(1,4,180)])
        self.play(Create(tail),MoveAlongPath(p[3],tail),run_time=.75,rate_func=linear)
        self.play(Transform(title,head('Low between releases',GLU)),run_time=.2);self.finish()

class S04Glt(TimedScene):
    def construct(self):
        self.add(stage_synapse(False),txt('astrocyte',-4.8,2.8,28,ASTRO),
            txt('presynaptic\nterminal',5.0,.9,26,NEUR),
            line((3.95,.9),(3.1,1.05),NEUR),
            txt('postsynaptic cell',1.68,-1.26,26,NEUR))
        a=badge('GLT-1',GLU,26).move_to(stage_point(-2.25,0))
        b=badge('GLT-1',GLU,26).move_to(stage_point(.1,1))
        self.at('most of the')
        self.play(FadeIn(a),run_time=.3)
        self.at('astrocytes')
        label=txt('GLT-1 in\nastrocytes\nmost of it',-4.9,-.15,28,GLU)
        self.play(FadeIn(label),Create(line((-3.5,0),(-2.45,0),GLU)),run_time=.35)
        self.at('with a smaller')
        label2=VGroup(txt('GLT-1 in terminals',4.8,3.25,26,GLU),txt('a little',4.8,2.65,26,GLU))
        self.play(FadeIn(b),FadeIn(label2),Create(line((4.15,2.45),(2.4,1.45),GLU)),run_time=.35)
        self.finish()

class S05Seizure(TimedScene):
    def construct(self):
        self.add(synapse(False).scale(.96).move_to([-3.35,0,0]))
        gate=badge('GLT-1',GLU,28).move_to([-3.3,-2.85,0]);self.add(gate,box(5.4,4.8,3.3,-.15))
        self.at('deleting')
        self.play(gate.animate.set_opacity(.3),FadeIn(head('~80% of GLT-1 protein lost',BAD)),run_time=.3)
        self.play(Transform(gate,badge('GLT-1 (~80% lost)',GLU,26).move_to([-3.3,-2.85,0])),run_time=.2)
        self.at('from astrocytes')
        self.play(FadeIn(txt('inducible astrocyte deletion',-3.3,-3.6,26,BAD)),run_time=.3)
        self.at('seizures')
        self.add(txt('Seizures',3.3,1.6,32,BAD),txt('illustration · not recorded EEG',3.3,-.85,26,LIGHT))
        ts=np.linspace(0,4,500)
        # Gated oscillatory model, explicitly non-data.
        ys=[.16*np.sin(8*t)+.75*np.sin(31*t)*np.exp(-((t-2.0)/.65)**8) for t in ts]
        wave=curve([[.9+t*1.18,.35+y,0] for t,y in zip(ts,ys)],BAD)
        self.play(Create(wave),run_time=.65)
        self.at('early death')
        self.play(FadeIn(txt('→ mice died early',3.3,-1.85,30,BAD)),run_time=.3);self.finish()

class S06Open(TimedScene):
    def construct(self):
        self.add(stage_synapse())
        self.at('now the open')
        self.play(FadeIn(txt('Do astrocytes release glutamate?',0,-3.5,34)),run_time=.3)
        self.at('also release glutamate')
        d=VGroup(*[Dot([-2.3+i*.25,-.15,0],radius=.1,color=GLU) for i in range(3)])
        a=arrow((-2.2,-.15),(1.2,-.15));q=txt('?',1.55,-.15,38,GLU)
        self.play(FadeIn(d),GrowArrow(a),FadeIn(q),run_time=.3)
        self.at('acts quickly')
        self.play(d.animate.shift(RIGHT*2.8),run_time=.25)
        self.at('this is called')
        self.play(FadeIn(txt('gliotransmission',4.95,-1.1,26,GLU)),
            Create(line((3.6,-.9),(2.8,-.25),GLU)),run_time=.3);self.finish()

class S07Calcium(TimedScene):
    def construct(self):
        self.add(stage_synapse())
        self.at('astrocytes show')
        ca=stage_calcium()
        self.at('calcium signals')
        self.play(FadeIn(ca),FadeIn(txt('calcium',-5.0,-1.65,30,CA)),run_time=.3)
        flicker(ca)
        self.at('in principle')
        self.play(FadeIn(txt('Could calcium trigger release?',0,-3.35,32,CA)),run_time=.3)
        self.at('could trigger release')
        # Enclosed process extends from the soma towards the cleft. The vesicle
        # has visible cytoplasm around it rather than sitting on an outline.
        process=RoundedRectangle(width=1.5,height=.65,corner_radius=.28,
            color=ASTRO,fill_color=ASTRO,fill_opacity=.25).move_to([-.4,.08,0])
        ves=Circle(radius=.13,color=GLU,fill_color=GLU,fill_opacity=.3).move_to([-.05,.08,0])
        trigger=Dot([-1.45,.08,0],radius=.08,color=CA)
        link=DashedLine([-1.45,.08,0],[-.3,.08,0],color=CA).add_tip(tip_length=.12)
        q=txt('?',-.85,.08,30,CA)
        q.add_background_rectangle(color=BG,opacity=1,buff=.04)
        self.play(FadeIn(process),FadeIn(ves),FadeIn(trigger),Create(link),FadeIn(q),run_time=.3)
        self.at('as it does')
        terminal_ves=Circle(radius=.18,color=GLU).move_to([2.7,1.25,0])
        self.play(FadeIn(terminal_ves),FadeIn(txt('vesicle in\na terminal',5.05,2.4,28,GLU)),
            Create(line((4.05,2.1),(2.85,1.4),GLU)),run_time=.3);self.finish()

class S08Test(TimedScene):
    def construct(self):
        cell=stage_synapse(False);self.add(cell)
        alabel=txt('astrocyte',-4.9,2.65,28,ASTRO);self.add(alabel)
        self.at('deleted a receptor')
        r=badge('IP3R2',CA,26).move_to(stage_point(-2.25,0));x=cross(-1.14,0,.48)
        self.play(FadeIn(r),Create(x),run_time=.3)
        self.at('stored calcium')
        store=txt('stored calcium',5.05,1.7,28,CA)
        self.play(FadeIn(store),run_time=.3)
        self.at('receptor type')
        title=txt('IP3R2 deleted',0,3.35,30,BAD)
        self.play(FadeIn(title),run_time=.3)
        self.at('hippocampal transmission')
        self.play(Transform(cell,synapse(False).scale(.96).move_to([-3.35,0,0])),
            r.animate.move_to([-4.26,0,0]),x.animate.move_to([-4.26,0,0]),
            alabel.animate.move_to([-3.3,-3.1,0]),store.animate.move_to([-3.3,2.75,0]),
            title.animate.move_to([-3.3,3.4,0]),run_time=.25)
        axes=VGroup(line((.7,-1.9),(6,-1.9)),line((.7,-1.9),(.7,1.5)))
        self.add(axes,txt('excitatory synaptic response',3.3,2.5,26),txt('(schematic · normalized)',3.3,1.95,26),txt('time',3.3,-2.4,26))
        ts=np.linspace(0,4,220)
        ys=np.where(ts>=.6,np.exp(-(ts-.6)/.8)-np.exp(-(ts-.6)/.12),0)
        pts=[[.8+1.25*t,-1.85+3.8*y,0] for t,y in zip(ts,ys)]
        control=curve(pts,LIGHT,8);ko=DashedVMobject(curve(pts,ASTRO,4),num_dashes=35)
        self.play(Create(control),Create(ko),run_time=.6)
        self.at('did not change')
        self.play(FadeIn(txt('No significant change',3.3,3.15,28)),
            FadeIn(txt('control —   KO - -',3.3,-3.1,26,ASTRO)),run_time=.3);self.finish()

class S09Predict(TimedScene):
    def construct(self):
        self.add(question());self.at('does that prove');self.finish()

class S10Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(question())
        ring=Circle(radius=.4,color=TEAL,stroke_width=8).move_to([0,-1.9,0])
        track=ring.copy().set_color(LIGHT).set_stroke(opacity=.3).set_fill(opacity=0);self.add(track,ring)
        self.play(Uncreate(ring),run_time=5,rate_func=linear)

class S11Reveal(TimedScene):
    def construct(self):
        g=ko_context();self.add(g[0],g[1],g[2],g[3],g[5])
        self.at('in adult mice');self.play(FadeIn(g[4]),run_time=.3)
        self.at('still showed')
        ca=stage_calcium()
        label=txt('calcium still\npresent',-5.0,-.1,28,CA)
        self.play(FadeIn(ca),FadeIn(label),run_time=.3);flicker(ca)
        self.at('calcium fluctuations')
        self.wait(.8)
        self.at('mostly in their')
        self.play(FadeOut(g[5]),FadeIn(txt('fine processes',-4.9,-2.55,28,CA)),run_time=.3);self.finish()

class S12Reveal2(TimedScene):
    def construct(self):
        g=ko_context();self.add(g)
        ca=stage_calcium();self.add(flicker(ca))
        self.at('so the null')
        self.play(FadeOut(g[5]),FadeIn(txt('No effect found\nin these tests',5.25,-1.8,26)),run_time=.3)
        self.at('cannot exclude effects')
        self.play(FadeIn(txt('calcium remains\ncould still act',-4.9,-.1,28,CA)),run_time=.3)
        self.finish()

class S13Subgroup(TimedScene):
    def construct(self):
        # Explicit zoom out from the same single cell into a schematic field.
        cell=astro_cell().move_to([-1.2,-.1,0]);self.add(cell)
        self.at('a later study')
        f=field();self.add(txt('schematic field · fraction not estimated',0,3.15,26,LIGHT));self.play(Transform(cell,f[1]),FadeIn(VGroup(*[f[i] for i in range(8) if i!=1])),run_time=.65)
        self.at('found a subgroup')
        self.play(cell.animate.set_stroke(opacity=1),FadeIn(txt('a subgroup',-1.55,2.75,30,GLU)),
            Create(line((-1.55,2.35),(-1.55,1.8),GLU)),run_time=.3)
        self.at('adult mouse')
        self.play(FadeIn(txt('Adult mouse hippocampus',0,-3.15,30)),run_time=.3)
        self.at('with synaptic')
        self.play(FadeIn(txt('VGLUT1-positive · release machinery',0,-2.5,28,GLU)),run_time=.3)
        self.finish()

class S14Vglut(TimedScene):
    def construct(self):
        self.add(head('Glutamate hotspots (sensor signal)',GLU))
        before=astro_cell().scale(.65).move_to([-3.3,0,0])
        after=astro_cell().scale(.65).move_to([3.3,0,0]);self.add(before,after)
        hb=hot_pair(-3.3,0);ha=hot_pair(3.3,0);self.add(hb,ha)
        self.add(txt('Before',-3.3,2.3,30),txt('After',3.3,2.3,30),line((0,-2.6),(0,2.6)))
        self.at('deleting a vesicular')
        gate=chip('VGLUT1',GLU,28).move_to([3.1,-2.45,0]);self.play(FadeIn(gate),run_time=.3)
        self.at('from astrocytes')
        self.play(Create(cross(4.5,-2.45)),run_time=.3)
        self.at('the glutamate hotspots')
        self.play(FadeOut(ha),FadeIn(txt('astrocytic VGLUT1 deleted',0,-3.25,28,BAD)),run_time=.6);self.finish()

class S15Scope(TimedScene):
    def construct(self):
        self.add(subgroup(),txt('a subgroup',-1.55,2.75,30,GLU),line((-1.55,2.35),(-1.55,1.8),GLU))
        self.at('that is positive')
        self.play(FadeIn(txt('Positive evidence',3.7,2.6,32,GLU)),
            GrowArrow(arrow((2.1,2.25),(-.5,1.3))),run_time=.3)
        self.at('but in one')
        self.play(FadeIn(txt('One subgroup',-3.2,-2.8,32,GLU)),
            FadeIn(txt('One species: mouse',3,-2.8,32)),run_time=.3);self.finish()

class S16Neither(TimedScene):
    def construct(self):
        self.add(astro_cell().scale(.84).move_to([-3.9,-.35,0]),
                 astro_cell().scale(.84).move_to([3.9,-.35,0]))
        self.add(txt('IP3R2 deleted',-3.6,2.55,30,BAD),
                 txt('astrocytic VGLUT1 deleted',3.6,2.55,26,BAD),
                 line((0,-3.35),(0,2.65)))
        self.at('neither study')
        self.play(FadeIn(head('Neither study refutes the other')),run_time=.3)
        self.at('different manipulations')
        bridge=txt('Different\nmanipulations,\ndifferent\nquestions',0,.1,26)
        bridge.add_background_rectangle(color=BG,opacity=1,buff=.16)
        self.play(FadeIn(bridge),
            FadeIn(txt('what each tested\ncalcium pathway',-3.6,-3.0,28,CA)),
            FadeIn(txt('what each tested\nrelease machinery',3.6,-3.0,28,GLU)),run_time=.3)
        self.finish()

class S17Takeaway(TimedScene):
    def construct(self):
        c=lists();self.add(c[0],c[1])
        self.at('so keep two')
        self.at('astrocytes clear');self.play(FadeIn(c[2][0]),FadeIn(c[2][1]),run_time=.3)
        self.at('is settled');self.play(FadeIn(c[2][2]),run_time=.3)
        self.at('fast signaling');self.play(FadeIn(c[3]),run_time=.3);self.finish()

class S18Takeaway2(TimedScene):
    def construct(self):
        self.play(FadeIn(lists()),FadeIn(txt('one adult mouse subgroup · one region\nstated conditions',0,-3.05,32,TEXT)),run_time=.3)
        self.at('your design problem')
        self.play(FadeIn(txt('Design the next test',0,-2.15,36,TEAL)),run_time=.3)
        self.finish()

class S19End(EndCard):
    LINE='Astrocytes clearing K+ and glutamate is settled.\nFast astrocyte signalling is still argued.'
    def construct(self):
        a=txt('Astrocytes clearing K+ and glutamate is settled.',0,.85,32,ASTRO)
        b=txt('Fast astrocyte signalling is still argued.',0,-.35,34,GLU)
        self.play(FadeIn(a),FadeIn(b),run_time=.5)
        self.add(txt('biochemistrypedia.com',0,-2,26,TEAL));self.finish()
