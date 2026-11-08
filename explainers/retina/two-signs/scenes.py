"""One Transmitter, Two Signs — reviewed animation.
COLOR MAP: YELLOW light; BLUE cone; TEAL glutamate (extracellular only);
LAVENDER cations (inward arrows); ORANGE G protein; GREEN ON/mGluR6;
PINK OFF/AMPA/kainate; RED inhibition/sign flips; GOLD retina;
IVORY APB; GREY membranes, axes and anatomical silhouettes.
All voltage traces use the reference exponential step model (onset .4, tau .13).
Relative units are explanatory models, not original experimental records.
"""
import importlib.util
from pathlib import Path
import numpy as np
from bp_style import *

_spec = importlib.util.spec_from_file_location('retina_reference', Path(__file__).resolve().parent.parent / 'scenes.old.py')
_ref = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ref)
Flow, Channel, arr = _ref.Flow, _ref.Channel, _ref.arr
ORANGE, PINK = _ref.ORANGE, _ref.PINK
CATION = '#C7B6FF'
DRUG = '#F2EEE8'


def label(s, x, y, color=TEXT, size=26):
    return T(s, size=size, color=color).move_to([x, y, 0])


def terminal(x=0, y=2.15, scale=1):
    body = RoundedRectangle(width=2.2*scale, height=.85*scale, corner_radius=.25,
                            color=BLUE, fill_color=BLUE, fill_opacity=.2).move_to([x,y,0])
    stem = Line([x,y+.42*scale,0], [x,y+.9*scale,0], color=BLUE, stroke_width=12)
    return VGroup(body, stem)


def dots(x=-3.3, many=True):
    # Glutamate never passes the membrane at y=-.3.
    pos = [(-.6,1.4),(0,1.25),(.6,1.4),(-.45,.8),(.35,.65),(-.15,.8)] if many else [(0,1.25)]
    return VGroup(*[Dot([x+dx,y,0],radius=.105,color=TEAL) for dx,y in pos])


def trace(sign, color, x0=1.25, x1=6.05, y=0, amp=1.3):
    ts=np.linspace(0,1,180)
    ys=y+sign*amp*(1-np.exp(-np.maximum(ts-.4,0)/.13))
    c=VMobject(color=color,stroke_width=5)
    c.set_points_as_corners([[x0+(x1-x0)*t,v,0] for t,v in zip(ts,ys)])
    return c


def plot_base(on=False):
    col=GREEN if on else PINK
    return VGroup(label('ON bipolar voltage' if on else 'OFF bipolar voltage',3.6,3.1,col,28),
        label('membrane voltage',3.6,2.5,size=26),
        label('depolarized ↑',3.6,1.95,GREY,26),
        Arrow([1.25,-1.5,0],[1.25,1.5,0],buff=0,color=GREY,stroke_width=2,tip_length=.15),
        Line([1.25,-1.5,0],[6.05,-1.5,0],color=GREY),
        DashedLine([1.25,0,0],[6.05,0,0],color=GREY,stroke_width=2),
        label('reference',5.15,.3,GREY,26),
        *[label(s,.8,y,GREY,26) for s,y in [('+1',1),('0',0),('−1',-1)]],
        label('time →',3.6,-2.8,GREY,26),
        label('model · relative units',3.6,-3.35,GREY,26))


def lightbar(y=-1.95, x0=1.25, x1=6.05):
    a=x0+.4*(x1-x0)
    return VGroup(Line([a,y,0],[x1,y,0],color=YELLOW,stroke_width=7),
                  label('light on',(a+x1)/2,y-.32,YELLOW,26))


def closeup(on=False, opened=False, dark=True):
    col=GREEN if on else PINK
    tx=-4.5 if on else -3.3
    # A cell body, rather than a labelled chip, gives the membrane a clear inside.
    cell=VMobject(color=col,stroke_width=3,fill_color=col,fill_opacity=.08)
    bottom=-2.65 if on else -2.4
    shoulder=-2.25 if on else -2.15
    cell.set_points_as_corners([[-6.1,-.3,0],[-6.1,shoulder,0],[-5.75,bottom,0],[-.8,bottom,0],[-.45,shoulder,0],[-.45,-.3,0]])
    base=VGroup(cell,terminal(tx,2.05),label('cone terminal',tx,3.2,BLUE),
        Line([-6.1,-.3,0],[-.45,-.3,0],color=GREY,stroke_width=7),
        label('ON bipolar' if on else 'OFF bipolar',-3.3,-2.3 if on else -2.1,col,28))
    tag=label('DARK' if dark else 'LIGHT',-1.35,2.65,GREY if dark else YELLOW,28)
    gap=ValueTracker(.6 if opened else 0)
    cx=-1.65 if on else -3.3
    channel=Channel(cx,-.3,gap,col,w=.38,h=.6)
    glu=dots(tx)
    receptor=_ref.bchip('mGluR6',GREEN,26).move_to([-4.65,-.3,0]) if on else VGroup(
        label('AMPA / kainate',-3.3,-1.25,PINK,28),label('ionotropic',-3.3,-1.7,PINK,26))
    go=chip('G protein (Go)',ORANGE,26).move_to([-4.25,-1.6,0])
    link=arr(receptor.get_bottom(),go.get_top(),ORANGE) if on else VGroup()
    clamp=VGroup(Line([cx-.65,.15,0],[cx-.65,-.9,0],color=RED,stroke_width=7),
                 Line([cx+.65,.15,0],[cx+.65,-.9,0],color=RED,stroke_width=7),
                 Line([cx-.65,-.9,0],[cx+.65,-.9,0],color=RED,stroke_width=7))
    brake=VGroup(clamp,arr(go.get_right(),[cx,-.95,0],RED))
    trp=label('TRPM1',cx,.65,GREEN,26)
    return dict(base=base,tag=tag,gap=gap,channel=channel,glu=glu,receptor=receptor,
                go=go,link=link,brake=brake,trp=trp)


def cations(cx):
    # Arrows distinguish ions from the round extracellular transmitter dots.
    return VGroup(arr([cx,.35,0],[cx,-.95,0],CATION,w=5),
                  label('cations in',cx+2,-.65,CATION,26))


def dark_scene(scene,on=False,full=True,brake=True):
    c=closeup(on,opened=not on)
    c['voltage']=trace(0,GREEN if on else PINK,y=-.65 if on else .65)
    scene.add(c['base'],c['tag'],plot_base(on),c['voltage'])
    if full:
        scene.add(c['channel'],c['glu'],c['receptor'])
        if on:
            scene.add(c['go'],c['link'],c['trp'])
            if brake: scene.add(c['brake'])
    return c


def ledger():
    head=label('One flash · follow the signs',0,3.25,size=34)
    boxes=VGroup(*[chip(s,col,28).move_to([x,y,0]) for s,col,x,y in [
        ('light +',YELLOW,-4.8,1.9),('cone voltage −',BLUE,-.6,1.9),('glutamate −',TEAL,4.2,1.9),
        ('OFF bipolar −',PINK,-3.3,-1.85),('ON bipolar +',GREEN,3.3,-1.85)]])
    links=VGroup(arr(boxes[0].get_right(),boxes[1].get_left(),RED),arr(boxes[1].get_right(),boxes[2].get_left(),TEAL),
        Arrow([3.4,1.5,0],[-3.3,-1.4,0],buff=.12,color=PINK,stroke_width=4),
        Arrow([4.2,1.5,0],[3.3,-1.4,0],buff=.12,color=RED,stroke_width=4))
    marks=VGroup(label('flip 1',-2.8,2.55,RED,28),
                 label('no flip',-1.3,.65,PINK,28),label('flip 2',5.15,.1,RED,28))
    return head,boxes,links,marks


def counters():
    return VGroup(label('1 flip: opposite to light',-3.3,-2.95,PINK,28),
                  label('2 flips: same sign as light',3.3,-2.95,GREEN,28))


def records():
    # Offset rows are shown in delta-voltage: the flat drug trace asserts no DC level.
    head=label('With APB + light: ON? OFF?',0,3.25,size=32)
    drug=chip('APB on',DRUG,26).move_to([5.15,2.55,0])
    rows=VGroup()
    for name,y,col in [('ON',.55,GREEN),('OFF',-1.25,PINK)]:
        rows.add(VGroup(label(name,-5.7,y,col,30),
            Line([-4.65,y-.75,0],[-4.65,y+.85,0],color=GREY),
            DashedLine([-4.65,y,0],[5.8,y,0],color=GREY,stroke_width=1.5)))
    axis=VGroup(label('membrane voltage change ↑ depolarized',-.6,2.55,size=26),
        label('time →',4.8,-3.15,GREY,26),label('model · relative units',-2.8,-3.15,GREY,26))
    ghost=VGroup(DashedVMobject(trace(1,GREEN,-4.65,5.8,.55,.65),num_dashes=38).set_opacity(.6),
                 DashedVMobject(trace(-1,PINK,-4.65,5.8,-1.25,.65),num_dashes=38).set_opacity(.6),
                 label('without drug',-2.8,1.6,GREEN,26),
                 label('without drug',-2.8,-.6,PINK,26))
    bar=lightbar(-2.45,-4.65,5.8)
    return dict(head=head,drug=drug,rows=rows,axis=axis,ghost=ghost,bar=bar)


def record_stage(scene,drug=True,light=True):
    r=records()
    scene.add(r['head'],r['rows'],r['axis'],r['ghost'])
    if drug: scene.add(r['drug'])
    if light: scene.add(r['bar'])
    return r


def eyecup():
    bowl=Arc(radius=2.65,start_angle=PI,angle=PI,color=GREY,stroke_width=9).shift(UP*.5)
    retina=Arc(radius=2.3,start_angle=PI,angle=PI,color=GOLD,stroke_width=12).shift(UP*.5)
    bath=Rectangle(width=7.2,height=4.5,color=GREY,fill_color=BLUE,fill_opacity=.17).move_to([0,-.3,0])
    cell=Circle(radius=.22,color=GREEN,fill_color=GREEN,fill_opacity=.45).move_to([.7,-1.65,0])
    electrode=VGroup(Line([2.6,2.4,0],[.7,-1.65,0],color=TEXT,stroke_width=3),
                     Line([2.8,2.4,0],[.7,-1.65,0],color=TEXT,stroke_width=3))
    labels=VGroup(label('perfused eyecup',0,-3.5,GREY,28),
        label('retina',-5.35,-1.45,GOLD,28),Line([-4.7,-1.45,0],[-2.1,-1.2,0],color=GOLD),
        label('recorded cell',5.2,-1.9,GREEN,26),Line([3.9,-1.9,0],[1.15,-1.98,0],color=GREEN),
        label('electrode',4.8,2.65,size=26))
    return VGroup(*[m.scale(1.2,about_point=ORIGIN) for m in (bath,bowl,retina,cell,electrode)],labels)


def mudpuppy():
    # Continuous tapered silhouette, four splayed feet and external gills.
    body=VMobject(color=GREY,fill_color=GREY,fill_opacity=.45,stroke_width=3)
    body.set_points_smoothly([[-4.4,.2,0],[-4.1,.85,0],[-3.3,1.05,0],[-2.5,.65,0],
        [-.5,.7,0],[1.4,.45,0],[3.1,.25,0],[4.7,1,0],[3.7,-.1,0],[2.1,-.5,0],
        [0,-.6,0],[-2.6,-.5,0],[-3.8,-.45,0],[-4.4,.2,0]])
    g=VGroup(body,Dot([-3.85,.45,0],radius=.09,color=TEXT))
    for x in [-1.9,.9]:
        for s in [-1,1]:
            leg=VMobject(color=GREY,stroke_width=16)
            leg.set_points_as_corners([[x,s*.4,0],[x+.25,s*1.25,0],[x-.25,s*1.65,0]])
            g.add(leg)
            for d in [-.25,0,.25]:
                g.add(Line([x-.25,s*1.6,0],[x-.6+d,s*(1.95+abs(d)),0],color=GREY,stroke_width=4))
    # Three gently curved filaments per side read as soft external gills.
    for side in [-1,1]:
        for dx in [-.25,0,.25]:
            gill=VMobject(color=GREY,stroke_width=4,stroke_opacity=.8)
            gill.set_points_smoothly([[-2.75+dx,side*.5,0],
                [-2.95+dx,side*.9,0],[-3.2+dx,side*1.22,0]])
            g.add(gill)
    return g.move_to([0,-.25,0])


class S00Title(TitleCard):
    LESSON='The Retina'
    TITLE='One Transmitter, Two Signs'

    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,1.55,TEAL,26),label(self.LESSON.upper(),0,.85,GREY,28))
        self.play(FadeIn(label(self.TITLE,0,-.15,size=48)),Create(Line([-1.3,-1,0],[1.3,-1,0],color=GOLD,stroke_width=4)),run_time=.6)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        cone=terminal(0,1.95,1.15)
        glu=dots(0).shift(DOWN*.1)
        state=label('DARK',-3,2.6,GREY,28)
        off=VGroup(Ellipse(width=3.25,height=1.05,color=PINK,fill_color=PINK,fill_opacity=.15),
                   label('OFF bipolar',0,0,PINK,28)).move_to([-3.5,-.5,0])
        on=VGroup(Ellipse(width=3.25,height=1.05,color=GREEN,fill_color=GREEN,fill_opacity=.15),
                  label('ON bipolar',0,0,GREEN,28)).move_to([3.5,-.5,0])
        cone_name=label('cone',0,3.25,BLUE,28)
        self.add(cone,cone_name)
        self.at('one transmitter')
        self.play(FadeIn(glu),run_time=.4)
        self.at('glutamate')
        self.play(FadeIn(label('glutamate',2.55,2.0,TEAL,28)),run_time=.4)
        self.at('More in the dark')
        self.play(FadeIn(state),run_time=.35)
        self.at('less in the light')
        self.play(Transform(glu,dots(0,False).shift(DOWN*.1)),Transform(state,label('LIGHT',-3,2.6,YELLOW,28)),run_time=.5)
        self.at('Yet some bipolar cells')
        self.play(FadeIn(off),FadeIn(on),GrowArrow(arr([-1,1.65,0],off.get_top(),PINK)),GrowArrow(arr([1,1.65,0],on.get_top(),GREEN)),
                  FadeIn(label('One transmitter, two signs?',0,3.25,size=34)),FadeOut(cone_name),run_time=.6)
        self.at('depolarize to light')
        self.play(Create(trace(1,GREEN,1.55,5.4,-2.1,.55)),FadeIn(lightbar(-2.4,1.55,5.4)),FadeIn(label('depolarizes',3.5,-1.2,GREEN,26)),run_time=.55)
        self.at('and others hyperpolarize')
        self.play(Create(trace(-1,PINK,-5.4,-1.55,-1.65,.55)),FadeIn(lightbar(-2.4,-5.4,-1.55)),FadeIn(label('hyperpolarizes',-3.5,-1.2,PINK,26)),run_time=.6)
        self.finish()


class S02Setup(SpokenScene):
    def construct(self):
        self.add(Line([0,-3.3,0],[0,3.3,0],color=GREY))
        groups=[]
        for x in [-3.25,3.25]:
            cone=terminal(x,1.8,.9)
            cells=VGroup()
            for dx,name,col in [(-1.35,'OFF',PINK),(1.35,'ON',GREEN)]:
                cx=x+dx
                cells.add(VGroup(Ellipse(width=1.1,height=1.7,color=col,fill_color=col,fill_opacity=.15).move_to([cx,-1.5,0]),
                    Line([cx,-.65,0],[cx,.1,0],color=col,stroke_width=5),label(name,cx,-1.5,col,28),
                    label('bipolar',cx,-2.7,col,26),arr([x+dx*.65,1.35,0],[cx,.1,0],col)))
            groups.append(VGroup(cone,cells))
        self.add(*[g[0] for g in groups])
        self.at('two bipolar cells')
        self.play(*[FadeIn(g[1]) for g in groups],run_time=.5)
        self.at('On the left')
        self.play(FadeIn(label('DARK',-3.25,3.2,GREY,32)),FadeIn(dots(-3.25).scale(.65,about_point=[-3.25,1.1,0]).shift(DOWN*.45)),run_time=.5)
        self.at('On the right')
        self.play(FadeIn(label('LIGHT',3.25,3.2,YELLOW,32)),FadeIn(dots(3.25,False).shift(DOWN*.5)),run_time=.5)
        self.finish()


class S03Off(SpokenScene):
    def construct(self):
        c=dark_scene(self,False,False)
        c['gap'].set_value(0)
        self.add(c['channel'])
        self.at('ionotropic glutamate receptors')
        self.play(FadeIn(c['receptor']),run_time=.5)
        self.at('Glutamate opens')
        self.play(FadeIn(c['glu']),FadeIn(label('glutamate',-5.05,1.25,TEAL,26)),c['gap'].animate.set_value(.6),run_time=.55)
        self.play(FadeIn(cations(-3.3)),run_time=.35)
        self.at('so in the dark')
        self.play(FadeIn(label('depolarized',3.6,1.15,PINK,30)),run_time=.4)
        self.finish()


class S04OffLight(SpokenScene):
    def construct(self):
        c=dark_scene(self)
        ions=cations(-3.3)
        self.add(ions)
        self.at('Light lowers glutamate')
        self.play(Transform(c['glu'],dots(-3.3,False)),Transform(c['tag'],label('LIGHT',-1.35,2.65,YELLOW,28)),FadeIn(lightbar()),
                  c['gap'].animate.set_value(0),FadeOut(ions),run_time=.35)
        self.at('the excitation fades')
        self.at('the cell hyperpolarizes')
        self.play(Transform(c['voltage'],trace(-1,PINK,y=.65)),FadeIn(label('hyperpolarized',3.6,-1.05,PINK,28)),run_time=.7)
        self.at('The sign is kept')
        self.play(FadeIn(label('Sign kept: less glutamate, lower voltage',-2.8,-2.7,PINK,26)),run_time=.4)
        self.finish()


class S05On(SpokenScene):
    def construct(self):
        c=dark_scene(self,True,False)
        c['voltage'].become(trace(0,GREEN,y=0))
        self.add(c['channel'])
        self.at('a different receptor')
        self.play(FadeIn(c['receptor']),run_time=.45)
        self.at('a metabolotropic one')
        self.play(FadeIn(VGroup(label('metabotropic',-1.95,1.35,GREEN,26),Line([-3.15,1.15,0],[-3.65,.1,0],color=GREY,stroke_width=2))),run_time=.45)
        self.at('In the dark')
        # Keep the dock clear: extracellular dots stop well above the receptor.
        c['glu'].remove(c['glu'][-1])
        self.play(FadeIn(c['glu']),FadeIn(label('glutamate',-2.15,2.05,TEAL,26)),run_time=.4)
        self.at('glutamate on this receptor')
        ligand=Dot([-4.65,.6,0],color=TEAL,radius=.12)
        self.add(ligand)
        self.play(ligand.animate.move_to([-4.65,.03,0]),c['receptor'][1].animate.set_fill(GREEN,.65).set_stroke(YELLOW,width=4),run_time=.55)
        self.at('activates a G protein')
        self.play(GrowArrow(c['link']),FadeIn(c['go']),run_time=.4)
        self.play(Indicate(c['go'],color=ORANGE,scale_factor=1.08),run_time=.35)
        self.finish()


class S06Brake(SpokenScene):
    def construct(self):
        c=dark_scene(self,True,True,False)
        # Put the low state and its label on screen before the short final sentence.
        self.add(label('hyperpolarized',3.6,-1.05,GREEN,28))
        self.at('holds a cation channel shut')
        self.play(Create(c['brake']),run_time=.6)
        self.play(FadeIn(label('held shut',-1.65,-1.75,RED,26)),run_time=.3)
        self.finish()


class S07OnLight(SpokenScene):
    def construct(self):
        c=dark_scene(self,True)
        self.at('Light lowers glutamate')
        self.play(Transform(c['glu'],dots(-4.5,False)),Transform(c['tag'],label('LIGHT',-1.35,2.65,YELLOW,28)),FadeIn(lightbar()),run_time=.55)
        self.at('activity falls')
        self.play(c['go'].animate.set_opacity(.35),c['link'].animate.set_opacity(.35),run_time=.5)
        self.at('comes off')
        self.play(FadeOut(c['brake'],shift=UP*.5),run_time=.45)
        self.at('the channel opens')
        self.play(c['gap'].animate.set_value(.6),run_time=.45)
        ions=VGroup(arr([-1.65,.25,0],[-1.65,-1.1,0],CATION),label('cations in',-1.65,-1.65,CATION,26))
        self.play(FadeIn(ions),run_time=.3)
        self.at('The cell depolarizes')
        self.play(Transform(c['voltage'],trace(1,GREEN,y=-.65)),FadeIn(label('depolarized',3.6,1.15,GREEN,28)),run_time=.7)
        self.at('The sign is inverted')
        self.play(FadeIn(label('Sign inverted: less glutamate, higher voltage',-2.55,-3.15,GREEN,26)),run_time=.4)
        self.finish()


class S08Ledger(SpokenScene):
    def construct(self):
        h,b,a,m=ledger()
        placeholders=VGroup(*[RoundedRectangle(width=box.width,height=box.height,
            corner_radius=.12,color=GREY,stroke_opacity=.25).move_to(box) for box in b])
        self.add(h,placeholders,b[0])
        self.at('The photoreceptor flips')
        self.play(FadeIn(b[1]),FadeIn(b[2]),GrowArrow(a[0]),GrowArrow(a[1]),FadeIn(m[0]),run_time=.7)
        self.at('The off cell adds')
        self.play(FadeIn(b[3]),GrowArrow(a[2]),FadeIn(m[1]),run_time=.6)
        self.at('The on cell adds')
        self.play(FadeIn(b[4]),GrowArrow(a[3]),FadeIn(m[2]),run_time=.6)
        self.finish()


class S09Even(SpokenScene):
    def construct(self):
        h,b,a,m=ledger()
        self.add(h,b,a,m)
        counts=counters()
        self.at('An even number of flips')
        self.play(Transform(m[0],label('1',-2.8,2.55,RED,28)),
                  Transform(m[2],label('2 = even',5.15,.1,GREEN,28)),FadeIn(counts[0]),run_time=.65)
        self.at('responds like light')
        self.play(FadeIn(counts[1]),Circumscribe(b[4],color=GREEN),run_time=.65)
        self.finish()


class S10Evidence(SpokenScene):
    def construct(self):
        animal=mudpuppy()
        animal_label=label('mudpuppy · a salamander',0,-2.95,GREY,30)
        q=label('How do we know the receptors differ?',0,3.15,size=32)
        self.add(q,animal,animal_label)
        self.at('Slaughter and Miller')
        cup=eyecup()
        self.play(animal.animate.scale(2.4,about_point=animal[1].get_center()).shift(RIGHT*3.3).set_opacity(0),
                  FadeIn(cup),FadeOut(animal_label),
                  Transform(q,label('Slaughter and Miller · 1981',0,3.3,size=30)),run_time=.8)
        self.finish()


class S11Drug(SpokenScene):
    def construct(self):
        # Put the bath at left, leaving a separate right-hand receptor inset.
        cup=eyecup().scale(.8,about_point=ORIGIN).shift(LEFT*1.45)
        self.add(cup,label('Slaughter and Miller · 1981',0,3.3,size=30))
        # APB follows curved pour paths and settles just over the retinal surface.
        settled=VGroup()
        paths=[]
        for i,theta in enumerate(np.linspace(3.55,4.65,9)):
            target=np.array([-1.45+2.05*np.cos(theta),.48+2.05*np.sin(theta),0])
            start=np.array([-3.45+.12*(i%3),1.95+.12*(i%2),0])
            dot=Dot(start,radius=.065,color=DRUG)
            path=CubicBezier(start,start+DOWN*.7,target+UP*.6,target)
            settled.add(dot)
            paths.append(path)
        self.at('They bathed the retina')
        self.add(settled)
        self.play(LaggedStart(*[MoveAlongPath(dot,path) for dot,path in zip(settled,paths)],
                             lag_ratio=.09),run_time=1.2)
        self.at('a glutamate mimic')
        self.play(FadeIn(chip('APB · glutamate mimic',DRUG,26).move_to([-3.35,2.55,0])),run_time=.4)
        self.at('acts on the on receptor')
        # Clear the anatomical callouts before the separate inset appears.
        self.play(FadeOut(cup[5][4]),FadeOut(cup[5][3]),FadeOut(cup[5][5]),run_time=.15)
        receptor=chip('ON receptor',GREEN,26).move_to([4.95,-.45,0])
        drug=chip('APB',DRUG,26).move_to([4.95,1.1,0])
        box=RoundedRectangle(width=3.1,height=3.25,corner_radius=.15,color=GREY,fill_color=BG,fill_opacity=1).move_to([4.95,.3,0])
        self.play(FadeIn(box),FadeIn(receptor),FadeIn(drug),run_time=.3)
        self.play(drug.animate.move_to([4.95,.2,0]),receptor[0].animate.set_fill(GREEN,.4),run_time=.45)
        self.finish()


class S12Predict(SpokenScene):
    def construct(self):
        r=record_stage(self,False,False)
        self.at('Add the drug')
        self.play(FadeIn(r['drug']),run_time=.4)
        self.at('then turn on a light')
        self.play(FadeIn(r['bar']),run_time=.4)
        self.at('What does the on cell do')
        self.play(Indicate(r['rows'][0][0],color=GREEN),run_time=.5)
        self.finish()


class S13Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        r=record_stage(self)
        prompt=label('Think · 5',0,3.25,size=32)
        self.remove(r['head'])
        self.add(prompt)
        for n in range(5,0,-1):
            self.play(Transform(prompt,label(f'Think · {n}   ON? OFF?',0,3.25,size=32)),run_time=.15)
            self.wait(.85)


class S14RevealOn(SpokenScene):
    def construct(self):
        r=record_stage(self)
        self.remove(r['head'])
        self.add(label('ON response abolished',0,3.25,GREEN,32))
        self.at('The on responses vanished')
        self.play(Create(trace(0,GREEN,-4.65,5.8,.55)),run_time=.7)
        self.finish()


class S15RevealOff(SpokenScene):
    def construct(self):
        r=record_stage(self)
        self.remove(r['head'])
        head=label('ON response abolished',0,3.25,GREEN,32)
        self.add(head,trace(0,GREEN,-4.65,5.8,.55))
        self.at('The off responses carried on')
        self.play(Create(trace(-1,PINK,-4.65,5.8,-1.25,.65)),run_time=.65)
        self.at('in the same retina')
        self.play(Transform(r['ghost'][3],label('OFF spared · same retina',2.5,-.6,PINK,26)),run_time=.45)
        self.at('different receptors')
        self.play(Transform(head,label('Two cells · different receptors',0,3.25,size=32)),run_time=.45)
        self.finish()


class S16Takeaway(SpokenScene):
    def construct(self):
        cone=terminal(0,2.1,.8)
        cone_label=label('cone',0,3.25,BLUE,28)
        off=chip('OFF bipolar',PINK,28).move_to([-3.5,.1,0])
        on=chip('ON bipolar',GREEN,28).move_to([3.5,.1,0])
        og=chip('OFF ganglion',PINK,28).move_to([-3.5,-1.4,0])
        ng=chip('ON ganglion',GREEN,28).move_to([3.5,-1.4,0])
        self.add(cone,cone_label)
        branches=VGroup(off,on,og,ng,arr([-.8,1.75,0],off.get_top(),PINK),arr([.8,1.75,0],on.get_top(),GREEN),
            arr(off.get_bottom(),og.get_top(),PINK),arr(on.get_bottom(),ng.get_top(),GREEN))
        self.add(branches)
        lighter=label('lighter',3.5,-2.5,GREEN,30)
        darker=label('darker',-3.5,-2.5,PINK,30)
        self.at('one for lighter')
        self.play(FadeIn(lighter),run_time=.35)
        self.at('one for darker')
        self.play(FadeIn(darker),run_time=.35)
        self.at('The takeaway')
        takeaway=VGroup(label('The receptor, not the molecule,',0,.55,size=38),label('sets the sign.',0,-.55,size=42))
        self.play(FadeOut(VGroup(cone,cone_label,branches,lighter,darker)),FadeIn(takeaway),run_time=.55)
        self.finish()


class S17End(EndCard):
    LINE='The receptor, not the molecule, sets the sign.'

    def construct(self):
        takeaway=VGroup(label('The receptor, not the molecule,',0,.6,size=38),
                        label('sets the sign.',0,-.5,size=42))
        self.add(takeaway)
        self.play(FadeIn(label('biochemistrypedia.com',0,-1.65,TEAL,26)),run_time=.45)
        self.finish()
