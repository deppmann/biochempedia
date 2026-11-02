"""Two Ways Out: Blood and Wires — review redraw.
COLOR MAP: yellow = hypothalamic neurons; blue = acetylcholine / cholinergic
axons; red = sympathetic noradrenaline (and hot tap); orange = blood and
circulating hormones / vasopressin; green = releasing peptides; grey-violet = feedback;
white bar-and-X = pharmacological block; grey = anatomical structure.
No molecular structures. Heart-rate graph is a qualitative causal model,
r = r_intrinsic + sympathetic_drive - vagal_brake*(1-block), not fitted data.
Its ordinal ticks deliberately make no numerical beats/minute prediction.
"""
import numpy as np
from bp_style import *
ORANGE = '#F29E4C'
BLOOD = AVP = ORANGE
NEUR = YELLOW
PEPTIDE = GREEN
FEEDBACK = '#B9A8CF'

def lab(s,x,y,size=28,color=TEXT):
    return T(s,size,color,line_spacing=.85).move_to([x,y,0])

def box(s,x,y,w=3,h=1,color=GREY,size=28):
    t=lab(s,x,y,size,color)
    assert t.width < w-.10, (s,t.width,w)
    assert t.height < h-.08, (s,t.height,h)
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.16,color=color,fill_opacity=.09).move_to([x,y,0]),t)

def line(points,color=GREY,w=4):
    return VMobject(stroke_color=color,stroke_width=w).set_points_as_corners([[x,y,0] for x,y in points])

def arrow(a,b,color=GREY,w=5):
    return Arrow([*a,0],[*b,0],buff=0,stroke_width=w,color=color,tip_length=.2)

def head(s): return lab(s,0,3.25,32)
def dots(x,y,color=AVP,n=5):
    return VGroup(*[Dot([x+(i%3)*.19,y+(i//3)*.18,0],radius=.065,color=color) for i in range(n)])
def tube(x0,x1,y):
    return VGroup(*[Line([x0,y+d,0],[x1,y+d,0],color=BLOOD,stroke_width=4) for d in [-.2,.2]])
def minus(x,y):
    return VGroup(Circle(radius=.22,color=FEEDBACK).move_to([x,y,0]),line([(x-.13,y),(x+.13,y)],FEEDBACK,4))
def blocker(x,y):
    return VGroup(RoundedRectangle(width=1.8,height=.65,corner_radius=.1,color=TEXT,fill_color=BG,fill_opacity=1).move_to([x,y,0]),lab('Atropine',x,y,26),line([(x-.3,y-.48),(x+.3,y-.82)],TEXT),line([(x+.3,y-.48),(x-.3,y-.82)],TEXT))
def receptor(x,y,color=BLUE):
    return line([(x-.20,y+.22),(x-.20,y-.15),(x+.2,y-.15),(x+.2,y+.22)],color,6)

def anatomy(labels=True):
    # Closed sagittal brain silhouette; the two stalk branches meet lobe tops.
    outline=VMobject(color=GREY,fill_opacity=.08).set_points_smoothly([[-3.6,.9,0],[-4.0,1.9,0],[-3.0,2.65,0],[-1.0,2.8,0],[1.7,2.2,0],[2.6,1.1,0],[1.6,.25,0],[.0,.15,0],[-2.2,.3,0],[-3.6,.9,0]]).close_path()
    hyp=Ellipse(width=3.25,height=.9,color=NEUR,fill_opacity=.12).move_to([0,.95,0])
    stalk=VGroup(line([(-.18,.5),(-.18,-.65),(-.95,-1.175)]),line([(.18,.5),(.18,-.65),(1.45,-1.175)]))
    ant=Ellipse(width=2.5,height=1.65,color=GREY,fill_opacity=.15).move_to([-.95,-2,0])
    post=Ellipse(width=1.8,height=1.65,color=GREY,fill_opacity=.15).move_to([1.45,-2,0])
    g=VGroup(outline,hyp,stalk,ant,post)
    if labels:
        g.add(lab('Hypothalamus',0,1,30,NEUR),lab('Stalk',1.55,-.45),line([(.3,-.45),(.9,-.45)]),lab('Anterior pituitary',-3.5,-3),line([(-1.7,-2.4),(-2.7,-2.8)]),lab('Posterior pituitary',3,-3),line([(1.5,-2.5),(2.5,-2.8)]))
    return g

def inset(which):
    a=anatomy(False).scale(.29).move_to([4.7,1.55,0])
    a[3 if which=='Anterior' else 4].set_color(BLOOD).set_fill(BLOOD,.5)
    # Small silhouette, full-size readable caption below.
    return VGroup(a,lab(which+' lobe',4.6,.35,26))

def speedbar():
    g=VGroup(line([(-5.3,-1.25),(5.3,-1.25)],GREY,4))
    for x,s in [(-4.5,'Seconds'),(-.2,'Minutes'),(4.5,'Hours')]:
        g.add(line([(x,-1.1),(x,-1.4)]),lab(s,x,-1.8,28))
    g.add(Dot([-4.5,-1.25,0],radius=.16,color=NEUR),line([(-.2,-1.25),(4.5,-1.25)],BLOOD,10),lab('vasopressin: minutes',-.9,-2.5,26,BLOOD),lab('cortisol, thyroid hormone: hours',2.0,-3.12,26,BLOOD))
    return g

def routes():
    h=box('Hypothalamus',0,2.2,4,1,NEUR)
    a=box('Wires\noften seconds',-3.3,.45,5.4,1.4,NEUR,30)
    b=box('Blood\nusually minutes to hours',3.3,.45,5.8,1.4,BLOOD,28)
    return VGroup(h,a,b,arrow((-1.2,1.7),(-3.3,1.15),NEUR),arrow((1.2,1.7),(3.3,1.15),BLOOD),speedbar())

def posterior():
    nuclei=VGroup(lab('Supraoptic\nnucleus (SON)',-3.8,2.15,26,NEUR),lab('Paraventricular\nnucleus (PVN)',-.1,2.15,26,NEUR))
    cells=VGroup(Dot([-3.4,.85,0],radius=.19,color=NEUR),Dot([-1.7,.85,0],radius=.19,color=NEUR))
    nuclei.add(line([(-3.8,1.55),(-3.4,1.05)],NEUR,2),line([(-.1,1.55),(-1.7,1.05)],NEUR,2))
    stalk=VGroup(line([(-3.9,.5),(-3.9,-1.7)]),line([(-1.2,.5),(-1.2,-1.7)]),lab('Stalk',-.2,-.4,26))
    lobe=Ellipse(width=5.6,height=1.9,color=GREY,fill_opacity=.1).move_to([-2.5,-2,0])
    ax=VGroup(line([(-3.4,.85),(-3.4,-.6),(-3.2,-1.4),(-3.2,-2.0)],NEUR,6),line([(-1.7,.85),(-1.7,-.6),(-1.9,-1.4),(-1.9,-2)],NEUR,6))
    terminals=VGroup(Dot([-3.2,-2,0],radius=.13,color=NEUR),Dot([-1.9,-2,0],radius=.13,color=NEUR))
    blood=tube(-5.6,1,-2.2)
    return VGroup(nuclei,cells,stalk,lobe,ax,terminals,blood,lab('Posterior pituitary',-2.7,-3.25,28),lab('Blood',.5,-2.85,26,BLOOD),inset('Posterior'))

def capbed(x,y):
    g=VGroup()
    for dy in [-.22,.22]:
        g.add(VMobject(color=BLOOD,stroke_width=4).set_points_smoothly([[x-1.1,y,0],[x-.65,y+dy,0],[x,y-dy,0],[x+.65,y+dy,0],[x+1.1,y,0]]))
    return g

def portal():
    cells=VGroup(*[Dot([x,2.15,0],radius=.15,color=NEUR) for x in [-3.2,-2.5,-1.8]])
    ax=VGroup(*[line([(x,2.15),(x,1.25)],NEUR,5) for x in [-3.2,-2.5,-1.8]])
    me=RoundedRectangle(width=3.2,height=.9,corner_radius=.18,color=GREY,fill_opacity=.08).move_to([-2.5,1.25,0])
    bed1=capbed(-2.5,1.05)
    stalk=VGroup(line([(-3.25,.65),(-3.25,-1.5)]),line([(-1.75,.65),(-1.75,-1.5)]))
    veins=VGroup(line([(-2.75,1.05),(-2.75,-1.8)],BLOOD,6),line([(-2.25,1.05),(-2.25,-1.8)],BLOOD,6))
    lobe=RoundedRectangle(width=4.2,height=1.65,corner_radius=.3,color=GREY).move_to([-2.5,-2.0,0])
    bed2=capbed(-2.5,-1.8)
    return VGroup(cells,ax,me,bed1,stalk,veins,lobe,bed2,lab('Hypothalamic neurons',-2.5,2.7,28,NEUR),lab('Anterior pituitary',-2.5,-2.65,26),inset('Anterior'))

def axis():
    hyp=box('Hypothalamus · PVN',-2.5,2.2,5.1,.85,NEUR,28)
    pit=box('Anterior pituitary',-2.5,.05,5.1,.85)
    adrenal=box('Adrenal cortex',-2.5,-2.05,5.1,.85)
    a=VGroup(arrow((-2.5,1.77),(-2.5,1.24),PEPTIDE),box('Portal blood',-2.5,1.0,2.9,.48,BLOOD,26),arrow((-2.5,.76),(-2.5,.48),BLOOD))
    b=arrow((-2.5,-.38),(-2.5,-1.62),BLOOD)
    crh=lab('Corticotropin-releasing\nhormone (CRH)',2.7,1.3,26,PEPTIDE)
    acth=lab('Adrenocorticotropic\nhormone (ACTH)',2.7,-.9,26,BLOOD)
    labels=VGroup(crh,acth)
    out=VGroup(arrow((.05,-2.05),(1,-2.05),BLOOD),box('Cortisol',2.5,-2.05,2.9,.85,BLOOD))
    fb=VGroup(line([(4,-2.05),(5.8,-2.05),(5.8,2.7),(.55,2.7),(.55,2.2)],FEEDBACK),arrow((1.05,2.2),(.55,2.2),FEEDBACK),line([(5.8,.05),(.55,.05)],FEEDBACK),arrow((1.05,.05),(.55,.05),FEEDBACK),minus(.4,2.2),minus(.4,.05))
    return VGroup(hyp,pit,adrenal,a,b,labels,out,fb)

def chain(y=0,gang=0,second=GREY):
    cns=box('CNS',-5.3,y,1.4,1.3)
    first=VGroup(Dot([-4.5,y,0],radius=.16,color=BLUE),line([(-4.5,y),(gang-.35,y)],BLUE,7))
    g=Circle(radius=.4,color=GREY).move_to([gang,y,0])
    post=VGroup(Dot([gang+.12,y,0],radius=.14,color=second),line([(gang+.12,y),(4.35,y)],second,7))
    organ=RoundedRectangle(width=1.4,height=1.5,corner_radius=.25,color=GREY,fill_opacity=.1).move_to([5.05,y,0])
    return VGroup(cns,first,g,post,organ)

def question(blocked=False):
    g=VGroup(head('Atropine · large dose'),box('Heart',-3,0,5,2.8),box('Sweat gland',3,0,5,2.8),lab('Vagus (parasympathetic)',-3,2.35,26,BLUE),arrow((-3,1.95),(-3,1.1),BLUE))
    for x in [-3,3]:
        g[1 if x<0 else 2][1].move_to([x,-.9,0])
        g.add(receptor(x,.9),lab('Muscarinic receptor',x,-.35,26,BLUE))
        if blocked: g.add(blocker(x,.9))
    g.add(lab('Heart rate?',-3,-2.1,32),lab('Sweating?',3,-2.1,32))
    return g

class S00Title(TitleCard):
    LESSON='Autonomic Control and the Hypothalamus'
    TITLE='Two Ways Out: Blood and Wires'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28),T('Two Ways Out:',48,font=TITLE_FONT),T('Blood and Wires',48,font=TITLE_FONT),Line(LEFT,RIGHT,color=GOLD)).arrange(DOWN,buff=.32)
        self.add(g); self.finish()

class S01Question(SpokenScene):
    def construct(self):
        a=anatomy(); self.add(a,head('How does it leave? How fast?'))
        self.at('has a correction'); self.play(Indicate(a[1],color=NEUR),run_time=.65)
        self.at('How does it'); self.play(Indicate(a[2],color=NEUR),run_time=.65); self.finish()

class S02TwoSpeeds(SpokenScene):
    def construct(self):
        r=routes(); self.add(r)
        self.at('Nerves often'); self.play(Indicate(r[1],color=NEUR),run_time=.6)
        self.at('Hormone effects'); self.play(Indicate(r[2],color=BLOOD),run_time=.7)
        self.at('over minutes'); self.play(ShowPassingFlash(r[5][8].copy()),run_time=.7); self.finish()

class S03Posterior(SpokenScene):
    def construct(self):
        p=posterior(); self.add(p,head('Vasopressin: made in SON and PVN'))
        self.at('Large neurons'); self.play(Indicate(p[1],color=NEUR),run_time=.6)
        self.at('make it'); d=dots(-3.5,.85); self.play(FadeIn(d),run_time=.35)
        self.at('Their axons'); self.play(d.animate.move_to([-3.2,-2,0]),run_time=1.0)
        self.at('straight into'); self.play(d.animate.move_to([-3.0,-2.2,0]),run_time=.4); self.play(d.animate.shift(RIGHT*3),run_time=.7); self.finish()

class S05Stores(SpokenScene):
    def construct(self):
        p=posterior(); self.add(p,head('Made in neurons · released from the lobe'),dots(-2.8,-2.2))
        tag=VGroup(lab('Stores and releases',3.6,-1.2,28,AVP),line([(1.6,-1.55),(-.2,-2)],AVP))
        self.at('stores and releases'); self.play(FadeIn(tag),run_time=.4)
        self.at('does not make'); self.play(Indicate(p[1],color=NEUR,scale_factor=1.5),FadeIn(VGroup(lab('Made here',-2.55,1.3,26,NEUR),line([(-3.0,1.15),(-3.3,1.0)],NEUR,2),line([(-2.1,1.15),(-1.8,1.0)],NEUR,2))),run_time=.65); self.finish()

class S07Anterior(SpokenScene):
    def construct(self):
        p=portal(); p[6:8].set_opacity(.25)
        self.add(p,head('Releasing hormones enter portal blood'))
        self.at('by blood'); self.play(Indicate(p[3],color=BLOOD),run_time=.5)
        self.at('Neurons release'); self.play(Indicate(p[0],color=NEUR),run_time=.45)
        self.at('peptides into'); d=VGroup(*[Dot([x,1.25,0],radius=.075,color=PEPTIDE) for x in [-3.2,-2.5,-1.8]]); self.add(d); self.play(d.animate.shift(DOWN*.2),FadeIn(VGroup(lab('Peptides = releasing hormones',1.9,-.55,26,PEPTIDE),line([(-.7,-.35),(-1.15,.1),(-1.8,1.05)],PEPTIDE,2))),run_time=.65)
        self.at('median eminence'); self.play(FadeIn(VGroup(lab('Median eminence',1.8,1.55,26),line([(-.9,1.25),(-.1,1.55)]))),run_time=.4); self.finish()

class S08Portal(SpokenScene):
    def construct(self):
        p=portal(); self.add(p,head('Portal system: two capillary beds in series'))
        self.add(lab('First capillary bed',1.15,1.75,26,BLOOD),lab('at median eminence',1.15,1.15,26),line([(-1.4,1.05),(-.4,1.5)]),lab('Portal veins',-.4,-.15,28,BLOOD),lab('Second capillary bed',-2.5,-3.25,26,BLOOD),line([(-4.35,-1.8),(-5,-1.8),(-5,-3.0),(-4.65,-3.0)]))
        self.at('Portal veins'); self.play(Indicate(p[5],color=BLOOD),run_time=.45)
        d=dots(-2.7,1.05,PEPTIDE,n=6); self.add(d)
        self.at('carry them'); self.play(d.animate.move_to([-2.5,-1.8,0]),run_time=1.2)
        self.at('second capillary bed'); self.play(Indicate(p[7],color=BLOOD),run_time=.5)
        self.at('They arrive concentrated'); self.play(FadeIn(lab('Concentrated',.8,-1.5,26,PEPTIDE)),run_time=.4)
        self.at('general circulation');
        # The same six particles spread over a larger compartment (comparison).
        general=VGroup(RoundedRectangle(width=3.2,height=1.4,corner_radius=.15,color=BLOOD).move_to([4.5,-1.5,0]),lab('General circulation',3.8,-.45,26,BLOOD),lab('Same amount, diluted',3.65,-2.65,26,PEPTIDE))
        spread=VGroup(*[Dot([3.2+i*.5,-1.5+(.25 if i%2 else -.25),0],radius=.065,color=PEPTIDE) for i in range(6)])
        self.play(FadeIn(general),TransformFromCopy(dots(-2.7,-1.8,PEPTIDE,n=6),spread),run_time=.85); self.finish()

class S09Hpa(SpokenScene):
    def construct(self):
        a=axis(); self.add(head('Stress axis · HPA'),a[0],a[1],a[2])
        self.at('paraventricular nucleus'); self.play(Indicate(a[0],color=NEUR),run_time=.5)
        self.at('releases'); self.play(Create(a[3]),FadeIn(a[5][0]),run_time=.65)
        self.at('That drives'); self.play(Indicate(a[1],color=BLOOD),run_time=.55)
        self.at('adrenocorticotropic hormone'); self.play(GrowArrow(a[4]),FadeIn(a[5][1]),run_time=.65); self.finish()

class S10Cortisol(SpokenScene):
    def construct(self):
        a=axis(); self.add(head('Cortisol turns the axis down'),a[:6])
        self.at('drives cortisol'); self.play(FadeIn(a[6]),Indicate(a[2],color=BLOOD),run_time=.6)
        self.at('Cortisol feeds back'); self.play(Create(a[7]),FadeIn(lab('Negative feedback',2.6,-3.1,28,FEEDBACK)),run_time=.8)
        self.at('turns the axis'); self.play(a[3:6].animate.set_opacity(.35),run_time=.65); self.finish()

class S11SameLoop(SpokenScene):
    def construct(self):
        self.add(head('Same loop · different hormone'))
        for x,first,second,out in [(-3.2,'CRH','ACTH','Cortisol'),(3.2,'TRH','TSH','Thyroid hormone')]:
            self.add(box('Hypothalamus',x,2.15,4.5,.8,NEUR,26),box('Anterior pituitary',x,.1,4.5,.8,GREY,26),box('Adrenal cortex' if x<0 else 'Thyroid',x,-1.85,4.5,.8,GREY,26),arrow((x,1.75),(x,.5),PEPTIDE),lab(first,x+.75,1.15,26,PEPTIDE),arrow((x,-.3),(x,-1.45),BLOOD),lab(second,x+.75,-.9,26,BLOOD),lab(out,x,-2.8,30,BLOOD),line([(x-2.4,-2.8),(x-2.7,-2.8),(x-2.7,2.15),(x-2.3,2.15)],FEEDBACK),minus(x-2.6,2.15),line([(x-2.7,.1),(x-2.3,.1)],FEEDBACK),minus(x-2.6,.1))
        self.at('a hormone'); self.play(Indicate(self.mobjects[8],color=BLOOD),run_time=.5); self.finish()

class S12Wires(SpokenScene):
    def construct(self):
        c=chain(.25); c[0][0].stretch_to_fit_height(2.8); c[4].stretch_to_fit_height(2.8); c[2].scale(1.6); self.add(c,head('The usual autonomic chain'),lab('Brainstem / spinal cord',-4.1,-1.7,26),lab('Preganglionic neuron',-2.6,2.2,28,BLUE),lab('Postganglionic neuron',2.35,2.2,28),lab('Ganglion',0,-1.7,28),lab('Target organ',4.8,-1.7,28),lab('The adrenal medulla breaks this pattern later',0,-3.1,28))
        self.at('two neurons'); self.play(Indicate(c[1]),Indicate(c[3]),run_time=.65)
        self.at('in a ganglion'); self.play(Create(Circle(radius=.85,color=NEUR).move_to([0,.25,0])),run_time=.5)
        self.at('on the target'); self.play(Create(Circle(radius=.4,color=NEUR).move_to([4.35,.25,0])),run_time=.5); self.finish()

class S13Rule1(SpokenScene):
    def construct(self):
        self.add(head('Rule 1 · ACh → nicotinic in every ganglion'))
        gs=VGroup()
        for y,name,target in [(2,'Parasympathetic','Organ'),(.55,'Sympathetic','Organ'),(-.9,'Sweat gland','Gland'),(-2.35,'Adrenal medulla','Blood')]:
            self.add(lab(name,-4.6,y+.45,26),line([(-3.4,y),(-.3,y)],BLUE,7),box(target,4.7,y,2.2,.9,GREY,26))
            g=Circle(radius=.3,color=BLUE).move_to([0,y,0]); gs.add(g)
            
            if name=='Adrenal medulla':
                self.add(arrow((.3,y),(3.6,y),BLOOD),lab('Chromaffin cell',1.8,-3.2,26),line([(.7,-2.95),(.2,-2.6)],GREY,2))
            else:
                self.add(line([(.3,y),(3.6,y)],GREY,5))
        self.add(gs)
        self.add(line([(.65,2.35),(.95,2.35),(.95,-2.7),(.65,-2.7)],BLUE),lab('Preganglionic',-2,-3.2,26,BLUE))
        self.at('same everywhere'); self.play(Indicate(gs,color=BLUE),run_time=.65)
        self.at('acetylcholine'); self.play(FadeIn(lab('ACh',-1.9,2.7,26,BLUE)),run_time=.4)
        self.at('nicotinic receptors'); self.play(Indicate(gs,color=BLUE),run_time=.6); self.finish()

class S14Rule2(SpokenScene):
    def construct(self):
        self.add(head('Rule 2 · receptors on the target'))
        a=chain(1.45,gang=2.7,second=BLUE); b=chain(-1.85,gang=-2.8,second=RED)
        icons=[]
        for c,y,color,name in [(a,1.45,BLUE,'Muscarinic'),(b,-1.85,RED,'Adrenergic\n(alpha, beta)')]:
            c[0][0].stretch_to_fit_height(2.45)
            c[4].stretch_to_fit_height(2.65).stretch_to_fit_width(2.5).move_to([4.95,y,0])
            c[2].scale(1.35)
            icon=receptor(4.15,y+.35,color).scale(1.7)
            c[3][1].put_start_and_end_on(c[3][1].get_start(),[3.81,y+.35,0])
            label=lab(name+'\nreceptor' if name=='Muscarinic' else 'Adrenergic\nreceptor\n(alpha, beta)',4.95,y-.55,22,color)
            icons.append(VGroup(icon,label))
        self.add(a,b,*icons,lab('Parasympathetic',-2.4,2.65,28,BLUE),lab('Most sympathetic',-2.4,-.6,28,RED),lab('ACh',3.25,2.2,26,BLUE),lab('Noradrenaline',.3,-1.05,26,RED))
        self.at('The second'); self.play(Indicate(icons[0]),Indicate(icons[1]),run_time=.6)
        self.at('Parasympathetic'); self.play(Indicate(a[3],color=BLUE),run_time=.6)
        self.at('muscarinic receptors'); self.play(Indicate(icons[0],color=BLUE),run_time=.6)
        self.at('Most sympathetic'); self.play(Indicate(b[3],color=RED),run_time=.6)
        self.at('adrenergic receptors'); self.play(Indicate(icons[1],color=RED),run_time=.6); self.finish()

class S16QAtropine(SpokenScene):
    def construct(self):
        q=question(); self.add(q)
        blocks=VGroup(*[blocker(x,2.25) for x in [-3,3]])
        self.at('Atropine blocks'); self.add(blocks); self.play(*[b.animate.shift(DOWN*1.35) for x,b in zip([-3,3],blocks)],run_time=.8)
        self.at('heart rate'); self.play(Indicate(q[-2]),run_time=.45)
        self.at('to sweating'); self.play(Indicate(q[-1]),run_time=.45); self.finish()

class S17Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question(True),lab('Pause and think',0,-3.1,30)); self.wait(5)

class S18AHeart(SpokenScene):
    def construct(self):
        self.add(head('Atropine removes the vagal brake'))
        vagus=line([(-5.7,1.45),(.2,1.45)],BLUE,7)
        pacemaker=box('Heart’s own pacemaker',3.3,1.45,5.4,1.25,GREY,28)
        tonic=lab('Tonic vagal activity, even at rest',-2.5,.4,26,BLUE)
        self.add(lab('Vagus (parasympathetic)',-3.2,2.45,26,BLUE),vagus,pacemaker,tonic,receptor(.6,1.45))
        brake=box('Brake',-.65,1.45,1.45,.65,BLUE,26); self.add(brake)
        block=VGroup(box('Atropine',-4.7,1.05,1.8,.65,TEXT,26),line([(-3.8,1.05),(-1.5,1.05)],TEXT,2))
        # Qualitative tonic-drive model; ordinate values are symbolic, never bpm data.
        def rate(t): return .35 + .45*float(t>=.4)
        def p(t,r): return [-3.8+8.8*t,-2.25+2.0*r,0]
        axes=VGroup(line([(-3.8,-.5),(-3.8,-2.25),(5,-2.25)]),lab('Heart rate (beats/min)',-2,-.25,26),lab('Time →',4.5,-2.8,26),lab('resting',-4.8,-1.55,26),lab('higher',-4.8,-.65,26),lab('Qualitative model · no numerical prediction',0,-3.55,26))
        baseline=VMobject(color=GREY,stroke_width=5).set_points_as_corners([p(0,rate(0)),p(.399,rate(0))]); self.add(axes,baseline)
        self.at('At a large'); self.play(FadeIn(block),brake.animate.shift(UP*1.1+RIGHT*.75).set_opacity(.6),vagus.animate.set_opacity(.2),run_time=.8)
        self.add(DashedLine([-.28,-2.25,0],[-.28,-.6,0],color=GREY),lab('Atropine',-.28,-2.8,26))
        self.at('rises',lead=0); ts=np.r_[.399,.4,np.linspace(.4,1,60)]; trace=VMobject(color=TEXT,stroke_width=6).set_points_as_corners([p(t,rate(t)) for t in ts]); self.play(Create(trace),run_time=.9)
        self.at('own pacemaker'); self.play(Indicate(pacemaker,color=TEXT),run_time=.6)
        self.at('on all the time'); self.play(Indicate(baseline,color=BLUE),run_time=.65)
        self.at('even at rest'); self.play(Indicate(tonic,color=BLUE),run_time=.5); self.finish()

class S19ASweat(SpokenScene):
    def construct(self):
        c=chain(.7,gang=-2.6,second=BLUE); c[0][0].stretch_to_fit_height(3.3); c[2].scale(1.7); c[4].stretch_to_fit_height(3.3)
        rec=receptor(4.35,.7).scale(1.35)
        rec_label=VGroup(lab('Muscarinic\nreceptor',3.0,-.35,26,BLUE),line([(3.9,-.1),(4.35,.42)],BLUE,2))
        block=VGroup(box('Atropine',2.25,2.3,1.8,.65,TEXT,26),line([(3.15,2.3),(3.7,2.3),(4.35,1.05)],TEXT,2),line([(4.13,.9),(4.57,.5)],TEXT),line([(4.57,.9),(4.13,.5)],TEXT))
        self.add(c,head('Exception 1: sympathetic but cholinergic'),lab('Preganglionic',-3.6,2.55,26,BLUE),lab('Chain ganglion',-2.6,-.7,28),lab('ACh',.3,1.65,30,BLUE),lab('Sweat gland',4.8,-1.55,28),rec,rec_label,block)
        drops=VGroup(*[Dot([5+i*.2,-2.25,0],color=BLUE,radius=.09) for i in range(3)]); self.add(drops)
        self.at('Sweating stops'); self.play(FadeOut(drops),FadeIn(lab('Sweating stops',0,-2.9,32)),run_time=.5)
        self.at('sympathetic'); self.play(Indicate(c[2],color=BLUE,scale_factor=1.4),run_time=.8)
        self.at('acetylcholine'); self.play(ShowPassingFlash(c[3][1].copy().set_stroke(width=12)),run_time=.85)
        self.at('muscarinic receptors'); self.play(Indicate(rec,color=BLUE,scale_factor=1.5),run_time=.8); self.finish()

class S20Taps(SpokenScene):
    def construct(self):
        self.add(head('Heart rate = the balance'))
        handles=[]
        for x,c,s in [(-3.4,BLUE,'Cold · parasympathetic'),(3.4,RED,'Hot · sympathetic')]:
            self.add(lab(s,x,2.35,26,c),line([(x-1,.65),(x-1,1.65),(x+.6,1.65),(x+.6,.65)],c,12),line([(x-.5,1.85),(x-.5,1.65)],c,6),line([(x-.9,1.85),(x-.1,1.85)],c,6))
            handles.append(self.mobjects[-1])
        self.add(line([(-5,.2),(-4,-2.2),(4,-2.2),(5,.2)],GREY,6),lab('Analogy only · at rest the cold tap runs stronger',0,-3.2,28))
        cold=Line([-2.8,.65,0],[-2.8,-1.4,0],color=BLUE,stroke_width=18)
        hot=Line([4,.65,0],[4,-1.4,0],color=RED,stroke_width=7)
        water=Polygon([-4.4,-1.3,0],[-4,-2.2,0],[4,-2.2,0],[4.4,-1.3,0],stroke_width=0,fill_color=interpolate_color(ManimColor(BLUE),ManimColor(RED),.3),fill_opacity=.65)
        self.add(cold,hot,water)
        self.at('steady sympathetic'); self.play(Indicate(hot,color=RED),run_time=.55)
        self.at('at a balance'); self.play(Indicate(water),run_time=.55)
        self.at('two taps'); self.play(Rotate(handles[1],PI/4),hot.animate.set_stroke(width=16),water.animate.set_fill(interpolate_color(ManimColor(BLUE),ManimColor(RED),.6)),run_time=.8); self.finish()

class S21Adrenal(SpokenScene):
    def construct(self):
        self.add(head('Exception 2 · adrenal medulla'),box('CNS',-5.2,.9,1.7,1.6),line([(-4.35,.9),(-.8,.9)],BLUE,8),lab('Preganglionic axon',-2.7,2.05,28,BLUE),lab('ACh → nicotinic',-2.6,-.15,28,BLUE),receptor(-.8,.9))
        cell=RoundedRectangle(width=4.8,height=2.4,corner_radius=.4,color=GREY,fill_opacity=.12).move_to([1.6,.9,0]); self.add(cell)
        old=lab('Second neuron',1.6,1.0,30); new=lab('Chromaffin cell\nadrenal medulla',1.6,1.0,28); self.add(old)
        blood=tube(-.8,5.7,-.5); self.add(blood,lab('Blood',5.1,-1.3,28,BLOOD))
        self.at('second neuron'); self.play(Indicate(old),run_time=.5)
        self.at('become a gland'); self.play(FadeOut(old),run_time=.18); self.play(FadeIn(new),run_time=.25)
        self.at('releases adrenaline'); self.play(FadeIn(lab('Adrenaline + noradrenaline',1.5,-2.5,30,BLOOD)),run_time=.3)
        d=dots(2.8,.15,BLOOD,n=6)
        self.at('into the blood'); self.add(d); self.play(d.animate.move_to([3.0,-.5,0]),run_time=.4); self.play(d.animate.shift(RIGHT*1.8),run_time=.65); self.finish()

class S22Pvn(SpokenScene):
    def construct(self):
        self.add(head('One nucleus, three routes'))
        p=box('Paraventricular nucleus (PVN)',0,1.9,7.5,1.1,NEUR,30); self.add(p)
        routes=[(-4.3,'Portal blood','CRH\n(parvocellular)',BLOOD),(0,'Posterior lobe','Vasopressin\n(magnocellular)',BLOOD),(4.3,'Brainstem +\nspinal cord','To preganglionic\nneurons',NEUR)]
        targets=[]
        for x,name,tag,c in routes:
            t=box(name,x,-.8,3.8,1.6,c,28); targets.append(VGroup(arrow((x*.3,1.35),(x,0),c),t,lab(tag,x,-2.35,26,c)))
        self.at('paraventricular nucleus'); self.play(Indicate(p,color=NEUR),run_time=.5)
        for cue,i in [('portal blood',0),('posterior lobe',1),('descending autonomic',2)]:
            self.at(cue); self.play(GrowArrow(targets[i][0]),FadeIn(targets[i][1:]),run_time=.55)
        self.finish()

class S23Takeaway(SpokenScene):
    def construct(self):
        r=routes(); self.add(r,head('Two routes out · two rules · two exceptions'))
        self.at('Nerves often'); self.play(Indicate(r[1],color=NEUR),run_time=.6)
        self.at('Hormone effects'); self.play(Indicate(r[2],color=BLOOD),run_time=.6); self.finish()

class S21End(EndCard):
    LINE='Nerves: often seconds. Hormones: usually minutes to hours.'
    def construct(self):
        self.add(routes(),head('Nerves: often seconds · Hormones: usually minutes to hours'))
        self.finish()
