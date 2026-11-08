"""Chapter 1: A Threshold Is Not a Count.

COLOR MAP (inherited verbatim in meaning from scenes.old.py):
BLUE inner hair cell, ribbon, vesicle pool; GREEN auditory nerve fibre/terminal;
RED lost/missing/crossed out; YELLOW threshold/test; TEAL indirect measures;
ORANGE noise; PURPLE transmitter; GOLD bound/highlight; GREY axes/outlines;
TEXT neutral labels. Ribbons remain BLUE to preserve the shared concept map.

The fibre model is the lesson's r(L)=200/(1+exp(-.22*(L-t-10))),
T=.05, b=60 or 2; threshold S/sqrt(B+S)>=1 on a .1 dB grid.
The on-screen shifts are computed means of 400 seeded populations;
the depicted population is one seeded illustrative realization.
Anatomical cartoons are schematic. Recovery curves are an explicitly labelled
illustrative model, NOT digitized mouse data; the 40 dB maximum is from Fig. 2
of Kujawa & Liberman 2009 (doi:10.1523/JNEUROSCI.2845-09.2009).
"""
import numpy as np
from bp_style import *

ORANGE = '#F29E4C'
PURPLE = '#B58CD9'


def p(x,y): return np.array([x,y,0.])
def lab(s,x=0,y=0,size=28,color=TEXT): return T(s,size,color).move_to(p(x,y))
def head(s,color=TEXT): return lab(s,0,3.12,32,color)
def readable(g):
    for m in g.get_family():
        if isinstance(m, Text) and m.font_size < 26:
            m.font_size=26
    return g
def arr(a,b,color=GREY):
    return Arrow(a,b,buff=.08,color=color,stroke_width=4,tip_length=.18)

# Exact population equations from Going deeper in lesson.mdx.
RNG=np.random.default_rng(1)
PARAM=np.sort(np.r_[RNG.uniform(0,10,10),RNG.uniform(15,40,6)])
BASE=np.r_[np.full(10,60.),np.full(6,2.)]
RANDOM_KEEP=np.sort(RNG.choice(16,8,replace=False))
SENSITIVE_KEEP=np.arange(8,16)

def rate(level): return 200/(1+np.exp(-.22*(np.asarray(level)[...,None]-PARAM-10)))

def model_shifts():
    rng=np.random.default_rng(1)
    levels=np.arange(-30,80.01,.1)
    shifts=[]
    for _ in range(400):
        t=np.r_[rng.uniform(0,10,10),rng.uniform(15,40,6)]
        b=np.r_[np.full(10,60.),np.full(6,2.)]
        r=200/(1+np.exp(-.22*(levels[:,None]-t-10)))
        thresholds=[]
        for k in [np.arange(16),rng.choice(16,8,replace=False),np.argsort(t)[8:]]:
            signal=.05*r[:,k].sum(axis=1)
            background=.05*b[k].sum()
            thresholds.append(levels[np.flatnonzero(signal/np.sqrt(background+signal)>=1)[0]])
        shifts.append(np.array(thresholds[1:])-thresholds[0])
    return np.mean(shifts,axis=0)

# Mean shifts: 2.0295 and 8.40325 dB, rounded as in the spoken script.
RANDOM_SHIFT,SENSITIVE_SHIFT=np.round(model_shifts()).astype(int)



# All geometry is schematic; blue blocks are synaptic ribbons, not protein structures.
def unit(x,y,missing=False):
    rib=RoundedRectangle(width=.32,height=.72,corner_radius=.06,color=BLUE,fill_opacity=.8).move_to(p(x,y+.35))
    ves=VGroup(*[Dot(p(x+dx,y+dy),radius=.11,color=BLUE) for dx,dy in [(-.36,.6),(.36,.6),(-.36,.28),(.36,.28)]])
    term=RoundedRectangle(width=1.05,height=.5,corner_radius=.18,color=GREEN,fill_opacity=.3).move_to(p(x,y-.48))
    fibre=Line(p(x,y-.73),p(x,y-2.0),color=GREEN,stroke_width=7)
    if missing:
        rib=DashedVMobject(rib.set_fill(opacity=0),num_dashes=12)
        ves.set_opacity(0)
        term=DashedVMobject(term.set_fill(opacity=0),num_dashes=14)
        fibre.set_opacity(.15)
    return VGroup(rib,ves,term,fibre)

def cell(damaged=False):
    body=RoundedRectangle(width=8,height=3.45,corner_radius=.7,color=BLUE,stroke_width=4,fill_opacity=.1).move_to(p(0,.75))
    hairs=VGroup(*[Line(p(x,2.48),p(x,2.88+(.18 if abs(x)<.4 else 0)),color=BLUE,stroke_width=5) for x in [-.8,-.4,0,.4,.8]])
    units=VGroup(*[unit(x,-.65,damaged and i%2==1) for i,x in enumerate([-2.7,-.9,.9,2.7])])
    return VGroup(body,hairs,units)

def question():
    c=cell()
    card=RoundedRectangle(width=10.5,height=3.6,corner_radius=.2,color=GREY,fill_color=BG,fill_opacity=1).move_to(p(0,-1.6))
    return VGroup(c,card,lab('?',0,-1,68,YELLOW),lab('How many ribbon synapses remain?',0,-2.5,32),head('32 kHz place · 8 weeks'))

def mouse():
    # Smooth silhouette, with the pinna behind the eye and a tapered snout.
    body=Ellipse(width=3.5,height=1.85,color=GREY,fill_opacity=.22).move_to(p(-.3,-.15))
    face=VMobject(color=GREY,fill_opacity=.22).set_points_smoothly([p(.5,.45),p(1,.65),p(1.65,.35),p(2.05,-.05),p(1.65,-.4),p(.6,-.6),p(.5,.45)])
    ear=Ellipse(width=.75,height=.95,color=GREY,fill_color=BG,fill_opacity=1).move_to(p(.75,.8))
    eye=Dot(p(1.4,.25),radius=.07,color=TEXT)
    feet=VGroup(Line(p(-1,-.95),p(-.4,-.95),color=GREY),Line(p(.7,-.65),p(1.3,-.85),color=GREY))
    tail=ArcBetweenPoints(p(-2,-.2),p(-2.8,.6),angle=-1.2,color=GREY)
    return VGroup(body,face,ear,eye,feet,tail)

def speaker():
    return VGroup(Rectangle(width=.7,height=2.3,color=ORANGE,fill_opacity=.15),Polygon(p(.35,.55),p(1.15,1.2),p(1.15,-1.2),p(.35,-.55),color=ORANGE,fill_opacity=.25))

def waves(x,y,color=ORANGE):
    return VGroup(*[Arc(radius=r,start_angle=-.7,angle=1.4,color=color,stroke_width=5).move_arc_center_to(p(x,y)) for r in [.6,1.,1.4]])

def cochlea():
    t=np.linspace(0,4.7*PI,160); r=np.linspace(.08,.9,len(t))
    return VMobject(color=BLUE,stroke_width=6).set_points_smoothly([p(float(a*np.cos(b)),float(a*np.sin(b))) for a,b in zip(r,t)])

def test_chart():
    # No fabricated measured trace: the displayed flat curve is a computed model
    # replicated at three frequencies, normalized to its own baseline.
    box=RoundedRectangle(width=5.4,height=4.8,corner_radius=.2,color=GREY)
    axis=VGroup(Line(p(-2,-1.4),p(2,-1.4),color=GREY),Line(p(-2,-1.4),p(-2,1.25),color=GREY))
    ref=DashedLine(p(-1.85,.1),p(1.9,.1),color=GREY,stroke_width=6)
    line=Line(p(-1.85,.1),p(1.9,.1),color=YELLOW,stroke_width=3)
    return VGroup(box,axis,ref,line,lab('hearing test',0,1.9,28,YELLOW),lab('frequency',0,-1.9,26),lab('baseline = current',0,.8,26),lab('model',0,-.75,26,GREY))

def tick(x,y):
    return VGroup(Line(p(x-.3,y),p(x-.05,y-.25),color=GREEN,stroke_width=7),Line(p(x-.05,y-.25),p(x+.45,y+.4),color=GREEN,stroke_width=7))

def population(keep=None,firing=False):
    keep=set(range(16) if keep is None else keep)
    g=VGroup()
    # Equal fibre lengths; the yellow mark encodes sensitivity on each fibre.
    # Positions use the actual model t parameters, not fabricated thresholds.
    for i,t in enumerate(PARAM):
        x=-5.5+i*11/15; col=GREEN if i in keep else GREY
        mark=-.6+2.6*t/40
        f=VGroup(Line(p(x,-2),p(x,2.05),color=col,stroke_width=5),Circle(radius=.13,color=col,fill_opacity=.4).move_to(p(x,2.05)),Line(p(x-.2,mark),p(x+.2,mark),color=YELLOW,stroke_width=5))
        if i not in keep: f.set_opacity(.22)
        g.add(f)
    return g

def pop_axis():
    return VGroup(arr(p(-5.7,-2.45),p(5.7,-2.45)),lab('more sensitive',-3.8,-2.9,26),lab('needs louder sound',3.5,-2.9,26))

def fibre_legend():
    return lab('yellow tick: relative sensitivity parameter',0,2.7,26,YELLOW)

def group_brackets():
    return VGroup(Line(p(-5.65,-2.3),p(1.25,-2.3),color=GREEN),Line(p(1.65,-2.3),p(5.65,-2.3),color=GREEN),lab('10 sensitive',-2.2,-2.7,28,GREEN),lab('6 less sensitive',3.65,-2.7,28,GREEN))

def responses():
    vals=rate(-8); g=VGroup()
    for i,r in enumerate(vals):
        x=-5.5+i*11/15
        h=3.2*r/vals[0]
        g.add(Line(p(x,-2),p(x,-2+h),color=GREEN,stroke_width=9))
    return g

def background():
    # Qualitative bands reflect the two spontaneous-rate groups (60 vs 2);
    # heights are illustrative, not a second quantitative response axis.
    bands=VGroup(Rectangle(width=7.1,height=2.1,color=GREY,stroke_width=0,fill_opacity=.18).move_to(p(-2.3,-.95)),Rectangle(width=4.6,height=.65,color=GREY,stroke_width=0,fill_opacity=.18).move_to(p(3.55,-1.675)))
    return VGroup(bands,lab('illustrative background',2.7,-1.5,26))

def quiet_scene():
    pop=population().set_opacity(.25)
    return VGroup(pop,background(),responses(),head('Quiet sound · population detection'),VGroup(lab('Sum across fibres sets the model threshold',0,-3.35,26),arr(p(-5.7,-2.45),p(5.7,-2.45)),lab('needs louder sound →',3.3,-2.85,26)))

def quiet_tone():
    return VGroup(waves(-4.8,2.45,YELLOW).scale(.3),lab('quiet tone',-2.5,2.5,28,YELLOW))

def pairs():
    a=population(RANDOM_KEEP).scale(.47).stretch_to_fit_height(4.6).move_to(p(-3.2,-.1))
    b=population(SENSITIVE_KEEP).scale(.47).stretch_to_fit_height(4.6).move_to(p(3.2,-.1))
    return VGroup(a,b,lab('random half removed',-3.2,2.7,28),lab('sensitive half removed',3.2,2.7,28),head('Which moves the threshold?'),lab('8 of 16 removed',-3.2,-2.85,28),lab('8 of 16 removed',3.2,-2.85,28))

def ruler():
    y=-.6
    g=VGroup(Line(p(-5.5,y),p(5.5,y),color=GREY,stroke_width=4))
    for n in [0,5,10]:
        x=-5.5+1.1*n
        g.add(Line(p(x,y-.2),p(x,y+.2),color=GREY),lab(str(n),x,y-.65,30))
    g.add(lab('threshold shift (dB)',0,-2,30,YELLOW),lab('model average · 400 seeded populations',0,2.1,28,GREY))
    return g

def link_icon(index):
    if index==0:
        return VGroup(RoundedRectangle(width=1.25,height=1.65,corner_radius=.35,color=BLUE,fill_opacity=.2),*[Line(p(x,.83),p(x,1.15),color=BLUE,stroke_width=4) for x in [-.35,0,.35]])
    if index==1:
        return VGroup(RoundedRectangle(width=.38,height=.8,corner_radius=.07,color=BLUE,fill_opacity=.75).move_to(p(0,.35)),RoundedRectangle(width=1.2,height=.45,corner_radius=.16,color=GREEN,fill_opacity=.25).move_to(p(0,-.6)),Line(p(0,-.83),p(0,-1.15),color=GREEN,stroke_width=5))
    return VGroup(Line(p(-1,0),p(1,0),color=GREEN,stroke_width=7),arr(p(-.7,-.45),p(.7,-.45),GREEN))

def chain():
    g=VGroup()
    for i,(x,s,c) in enumerate([(-4.2,'hair cell',BLUE),(0,'ribbon synapse',BLUE),(4.2,'nerve fibre',GREEN)]):
        box=RoundedRectangle(width=3.5,height=4.7,corner_radius=.4,color=c,stroke_width=4,fill_opacity=.06).move_to(p(x,0))
        icon=link_icon(i)
        icon.shift(p(x,.25)-icon[0].get_center())
        label=lab(s,x,-1.75,28,c)
        g.add(VGroup(box,icon,label))
    return g

def chain_arrows():
    return VGroup(arr(p(-2.4,0),p(-1.8,0)),arr(p(1.8,0),p(2.4,0)))

def compare_cell():
    c=cell(True).scale(.66).stretch_to_fit_height(4.6).move_to(p(-3.4,-.15))
    chart=test_chart().move_to(p(3.25,-.15))
    return VGroup(c,chart,lab('schematic: relative count',-3.4,-3.15,26))

class S00Title(TitleCard):
    LESSON='Hidden Hearing Loss, Gene Therapy and Regeneration'
    TITLE='A Threshold Is Not a Count'
    def construct(self):
        self.add(lab('BIOCHEMISTRYPEDIA',0,2.3,26,TEAL),lab('Hidden Hearing Loss,\nGene Therapy and Regeneration',0,1,28,GREY))
        self.play(Write(T(self.TITLE,48,font=TITLE_FONT).move_to(p(0,-.65))),Create(Line(p(-1,-1.6),p(1,-1.6),color=GOLD)),run_time=.8)
        self.finish()

class S01(SpokenScene):
    def construct(self):
        m=mouse().scale(1.12).move_to(p(-3.2,-.1)); sp=speaker().move_to(p(-5.7,1.4))
        chart=readable(test_chart().scale(.83)).move_to(p(3.4,.5))
        self.add(m,chart)
        self.at('passes its hearing test'); self.play(Create(tick(3.4,2.85)),run_time=.35)
        self.at('after loud noise'); self.play(FadeIn(sp),Create(waves(-4.9,1.4).scale(.6)),run_time=.4)
        self.at('Can its cochlea'); self.play(Create(cochlea().move_to(p(-2.3,-2.5))),FadeIn(lab('?',-.5,-2.4,60,YELLOW)),FadeIn(lab('cochlea',-4.4,-2.5,28,BLUE)),run_time=.4)
        self.finish()

class S02(SpokenScene):
    def construct(self):
        bar=Rectangle(width=1.1,height=.12,color=YELLOW,fill_opacity=.5).move_to(p(-3.6,-2.5))
        self.add(arr(p(-5,-2.5),p(-5,2.2)),lab('louder',-5,2.6,28),lab('quieter',-5,-3.05,28),bar,head('Sound level and response'))
        # Expected driven spike count from the population model as level rises.
        levels=np.linspace(-30,10,120); counts=.05*rate(levels).sum(axis=1)
        curve=VMobject(color=GREEN,stroke_width=5).set_points_as_corners([p(-.4+5.5*(l+30)/40,-1.7+3*c/counts[-1]) for l,c in zip(levels,counts)])
        response_axes=VGroup(Line(p(-.4,-1.7),p(5.2,-1.7),color=GREY),lab('model response',2.4,2.3,28,GREEN),lab('increasing sound level',2.4,-2.25,26))
        self.add(response_axes)
        self.at('quietest sound'); self.play(bar.animate.stretch_to_fit_height(2.7).move_to(p(-3.6,-1.15)),Create(curve),Create(Line(p(-4.25,.2),p(-2.95,.2),color=YELLOW,stroke_width=6)),FadeIn(lab('threshold',-2.9,.85,28,YELLOW)),run_time=.7)
        self.at('hearing test'); self.play(FadeOut(curve),FadeOut(response_axes),FadeIn(readable(test_chart().scale(.77)).move_to(p(2.5,.1))),run_time=.4)
        self.finish()

class S03(SpokenScene):
    def construct(self):
        c=cell(); self.add(c[:2],lab('inner hair cell',0,1.3,30,BLUE))
        self.at('to nerve'); self.play(FadeIn(VGroup(*[u[2:] for u in c[2]])),FadeIn(lab('nerve fibres',0,-3.15,28,GREEN)),run_time=.35)
        self.at('at ribbon synapses'); self.play(FadeIn(VGroup(*[u[0] for u in c[2]])),FadeIn(lab('ribbon synapse',-4.6,-1.5,28,BLUE)),Create(arr(p(-3.8,-1.3),p(-2.9,-.7),BLUE)),run_time=.35)
        self.at('The ribbon holds'); self.play(FadeIn(VGroup(*[u[1] for u in c[2]])),run_time=.35)
        self.at('ready supply'); self.play(FadeIn(lab('vesicle supply',3.9,1.1,28,BLUE)),Create(arr(p(3.8,.75),p(3.1,-.05),BLUE)),run_time=.35)
        self.finish()

class S04(SpokenScene):
    def construct(self):
        chamber=RoundedRectangle(width=6.6,height=5.2,corner_radius=.2,color=GREY).move_to(p(-3.2,-.1))
        self.add(chamber,mouse().scale(1.17).move_to(p(-3.2,-.5)),speaker().move_to(p(-5.45,1.3)),head('Kujawa and Liberman · 2009'))
        self.at('male mice'); self.play(FadeIn(lab('male CBA/CaJ mice',-3.2,-2.9,28)),run_time=.3)
        self.at('weeks old'); self.play(FadeIn(lab('16 weeks',3.3,2.1,28)),run_time=.3)
        self.at('The loud noise'); self.play(Create(waves(-4.7,1.3).scale(.6)),FadeIn(lab('8–16 kHz\n100 dB SPL',3.3,.6,34,ORANGE)),run_time=.35)
        clock=VGroup(Circle(radius=.82,color=ORANGE,stroke_width=5),Dot(radius=.06,color=ORANGE),Line(p(0,0),p(0,.6),color=ORANGE,stroke_width=5),Line(p(0,0),p(.5,-.25),color=ORANGE,stroke_width=5),*[Line(p(.68*np.sin(a),.68*np.cos(a)),p(.78*np.sin(a),.78*np.cos(a)),color=ORANGE) for a in np.arange(12)*PI/6]).move_to(p(3.3,-1.2))
        self.at('lasted two hours'); self.play(Create(clock),FadeIn(lab('2 hours',3.3,-2.55,34,ORANGE)),run_time=.35)
        self.finish()

class S05(SpokenScene):
    def construct(self):
        # Computed illustration, not invented experimental samples. At each
        # frequency use the lesson's identical population detector. The temporary
        # shift is an explicit Gaussian-in-log-frequency model with 40 dB maximum
        # (the maximum reported in Kujawa & Liberman 2009 Fig.2), not a fitted curve.
        levels=np.arange(-30,80.01,.1); sig=.05*rate(levels).sum(axis=1)
        th=levels[np.flatnonzero(sig/np.sqrt(.05*BASE.sum()+sig)>=1)[0]]
        freq=np.geomspace(4,64,120); base=np.full_like(freq,th-th)
        shift=40*np.exp(-.5*(np.log2(freq/32)/.8)**2)
        def curve(vals,color=YELLOW):
            return VMobject(color=color,stroke_width=5).set_points_as_corners([p(-4.8+9.6*np.log2(f/4)/4,-2.1+4*v/50) for f,v in zip(freq,vals)])
        self.add(head('Threshold recovery · illustrative model'),Line(p(-4.8,-2.1),p(4.8,-2.1),color=GREY),Line(p(-4.8,-2.1),p(-4.8,2.15),color=GREY),lab('threshold (dB relative to before)',0,2.6,26))
        for v in [0,20,40]: self.add(lab(str(v),-5.35,-2.1+4*v/50,28),Line(p(-4.9,-2.1+4*v/50),p(-4.7,-2.1+4*v/50),color=GREY))
        for f in [4,8,16,32,64]: self.add(lab(str(f),-4.8+9.6*np.log2(f/4)/4,-2.55,26))
        self.add(lab('frequency (kHz)',0,-3.05,28),curve(base),lab('before',-3.2,-1.6,28,YELLOW))
        raised=curve(shift,ORANGE)
        self.at('Thresholds rose'); self.play(Create(raised),FadeIn(lab('right after noise',2.1,1.9,28,ORANGE)),run_time=.65)
        recovered=curve(base)
        self.at('then returned'); self.play(TransformFromCopy(raised,recovered),FadeIn(lab('2 weeks = before',1.6,-1.55,28,YELLOW)),run_time=.7)
        self.at('The hair cells'); body=cell()[:2].scale(.23).move_to(p(-3,1.1))
        self.play(FadeIn(body),FadeIn(lab('hair cells intact',-.4,1.1,28,BLUE)),run_time=.4)
        self.finish()

class S06(SpokenScene):
    def construct(self):
        q=question(); self.add(q[0],q[1],q[2],q[4])
        self.at('what would you predict'); self.play(FadeIn(q[3]),run_time=.4); self.finish()

class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question()); self.wait(5)

class S08(SpokenScene):
    def construct(self):
        q=question(); self.add(q); target=cell(True)
        self.at('About half'); self.play(FadeOut(q),FadeIn(target),FadeIn(head('32 kHz place · 8 weeks')),run_time=.6)
        self.play(FadeIn(lab('about half lost · schematic: relative count',0,-3.2,28,BLUE)),run_time=.3)
        self.at('nerve terminals'); self.play(Indicate(VGroup(target[2][1][2],target[2][3][2]),color=GREEN),run_time=.5)
        self.finish()

class S09(SpokenScene):
    def construct(self):
        c=cell(True); title=head('32 kHz place · 8 weeks')
        self.add(c,title,lab('about half lost · schematic: relative count',0,-3.2,28,BLUE))
        self.at('Losing these synapses'); self.play(Indicate(c[2],scale_factor=1.02),run_time=.4)
        self.at('hair cells survive'); self.play(FadeIn(lab('hair cell intact',0,1.25,30,BLUE)),run_time=.3)
        self.at('called cochlear synaptopathy'); self.play(Transform(title,head('Cochlear synaptopathy')),run_time=.4); self.finish()

class S10(SpokenScene):
    def construct(self):
        g=compare_cell(); self.add(g,head('Half the synapses lost…'))
        self.at('leave the threshold'); self.play(FadeIn(lab('…same threshold?',0,2.55,30,YELLOW)),Indicate(g[1][3]),run_time=.4); self.finish()

class S11(SpokenScene):
    def construct(self):
        pop=population(); self.add(pop,pop_axis(),fibre_legend(),head('Fibres at one cochlear place',GREEN))
        self.at('differ in sensitivity'); self.play(LaggedStart(*[Indicate(f[2],color=YELLOW) for f in pop],lag_ratio=.02),run_time=.7)
        self.at('Some respond'); self.play(Indicate(pop[:2]),run_time=.5)
        self.at('others need louder sound'); self.play(Indicate(pop[-6:]),run_time=.5); self.finish()

class S12(SpokenScene):
    def construct(self):
        g=quiet_scene(); self.add(g[0],g[1],g[3],g[4])
        self.at('quiet sound'); self.play(FadeIn(quiet_tone()),Create(g[2]),run_time=.45)
        self.at('first stands out'); self.play(Indicate(g[2][:2],color=YELLOW),run_time=.5)
        self.at('background firing'); self.play(Indicate(g[1][0],scale_factor=1.01),run_time=.4); self.finish()

class S12b(SpokenScene):
    def construct(self):
        self.add(quiet_scene(),quiet_tone())
        rings=VGroup(*[Ellipse(width=.48,height=.7,color=YELLOW,stroke_width=4).move_to(p(-5.5+i*11/15,-2+3.2*rate(-8)[i]/rate(-8)[0])) for i in range(2)])
        bracket=VGroup(Line(p(-5.75,-2.2),p(-4.5,-2.2),color=YELLOW),Line(p(-5.75,-2.2),p(-5.75,-2.05),color=YELLOW),Line(p(-4.5,-2.2),p(-4.5,-2.05),color=YELLOW),lab('most sensitive fibres',-3.95,-2.8,26,YELLOW))
        self.at('only the most sensitive'); self.play(Create(rings),FadeIn(bracket),run_time=.4); self.finish()

class S13(SpokenScene):
    def construct(self):
        self.add(population(),fibre_legend(),head('16 fibres · illustrative model'))
        self.at('small model'); self.play(Create(group_brackets()),run_time=.4)
        caption=lab('Passive: fixed fibre response curves',0,-3.35,26)
        self.at('illustrative and passive'); self.play(FadeIn(caption),run_time=.35)
        self.at('not fitted'); self.play(Transform(caption,lab('Illustrative model · not fitted to mouse data',0,-3.35,26,YELLOW)),run_time=.35); self.finish()

class S14(SpokenScene):
    def construct(self):
        g=pairs(); a=population().scale(.47).stretch_to_fit_height(4.6).move_to(p(-3.2,-.1)); b=population().scale(.47).stretch_to_fit_height(4.6).move_to(p(3.2,-.1))
        self.add(a,b)
        self.at('Remove half'); self.play(Transform(a,g[0]),FadeIn(g[2]),FadeIn(g[5]),run_time=.5)
        self.at('or remove'); self.play(Transform(b,g[1]),FadeIn(g[3]),FadeIn(g[6]),run_time=.5)
        self.at('which moves'); self.play(FadeIn(g[4]),run_time=.35); self.finish()

class S15Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(pairs()); self.wait(5)

class S16(SpokenScene):
    def construct(self):
        self.add(ruler(),head('Random half removed'))
        self.at('about two decibels'); self.play(GrowArrow(arr(p(-5.5,.6),p(-5.5+1.1*RANDOM_SHIFT,.6),YELLOW)),FadeIn(lab('+2 dB',-3.3,1.2,42,YELLOW)),run_time=.5)
        self.at('five decibel steps'); self.play(Create(Line(p(-5.5,-.6),p(0,-.6),color=TEXT,stroke_width=8)),FadeIn(lab('one test step = 5 dB',0,-2.9,30)),run_time=.4); self.finish()

class S17(SpokenScene):
    def construct(self):
        self.add(ruler(),head('Most sensitive half removed'))
        self.at('about eight decibels'); self.play(GrowArrow(arr(p(-5.5,.6),p(-5.5+1.1*SENSITIVE_SHIFT,.6),YELLOW)),FadeIn(lab('+8 dB',3.3,1.2,42,YELLOW)),run_time=.5)
        self.at('more than one'); self.play(Create(Line(p(-5.5,-.6),p(0,-.6),color=TEXT,stroke_width=8)),Create(Line(p(0,-.6),p(5.5,-.6),color=YELLOW,stroke_width=8)),FadeIn(lab('more than one step · each step = 5 dB',0,-2.9,30)),run_time=.4); self.finish()

class S18(SpokenScene):
    def construct(self):
        self.add(head('Loud sound · illustrative model'))
        groups=VGroup(); bars=VGroup(); values=VGroup()
        for x,name,keep in [(-4,'intact',None),(0,'random half',RANDOM_KEEP),(4,'sensitive half',SENSITIVE_KEEP)]:
            groups.add(population(keep).scale(.3).stretch_to_fit_height(4.6).move_to(p(x,-.25)),lab(name,x,2.65,28))
            value=float(rate(80).sum() if keep is None else rate(80)[keep].sum())/float(rate(80).sum())
            bars.add(Rectangle(width=2.4,height=2.7*value,color=GREEN,fill_opacity=.65).move_to(p(x,-2.55+2.7*value/2)))
            values.add(lab(f'{value:.2f}',x,-2.95,30,GREEN))
        self.add(groups)
        self.at('a loud sound'); self.play(Indicate(groups[0],color=YELLOW,scale_factor=1.1),Create(waves(-5.6,1.1,YELLOW).scale(.6)),run_time=.45)
        self.at('halved in every case'); self.play(*[GrowFromEdge(b,DOWN) for b in bars],FadeIn(values),FadeIn(lab('Sound-driven response · fraction of intact',0,-3.5,26,GREEN)),*[groups[i].animate.stretch_to_fit_height(2.2).move_to(p(x,1.3)) for i,x in [(0,-4),(2,0),(4,4)]],run_time=.45); self.finish()

class S19(SpokenScene):
    def construct(self):
        g=chain(); self.add(g,chain_arrows(),head('Hearing runs through a chain'))
        self.at('Hearing runs through'); self.play(Indicate(g,scale_factor=1.01),run_time=.5)
        self.at('Hair cell'); self.play(Indicate(g[0][2]),run_time=.25)
        self.at('ribbons'); self.play(Indicate(g[1][2]),run_time=.25)
        self.at('nerve fiber'); self.play(Indicate(g[2][2]),run_time=.25); self.finish()

class S20(SpokenScene):
    def construct(self):
        g=chain(); self.add(g,chain_arrows(),head('Quiet sound · one sensitive path',YELLOW))
        # Three lanes each pass THROUGH all three stages; only one is bright.
        lanes=VGroup(*[Line(p(-5.8,y),p(5.8,y),color=YELLOW,stroke_width=5).set_opacity(.13) for y in [.25,-.2,-.65]])
        self.add(lanes)
        self.at('most sensitive links'); self.play(lanes[0].animate.set_opacity(1),run_time=.4)
        counter=chip('synapse count',BLUE,32).move_to(p(0,-3))
        self.at('It does not count'); self.play(FadeIn(counter),run_time=.2); self.play(Create(Line(counter.get_left()+LEFT*.08,counter.get_right()+RIGHT*.08,color=RED,stroke_width=2).set_opacity(.55)),run_time=.2)
        self.finish()

class S21(SpokenScene):
    def construct(self):
        g=compare_cell(); self.add(g,head('Noise-exposed mice'))
        self.at('lost many synapses'); self.play(Indicate(g[0][2],color=BLUE),run_time=.4)
        self.at('still passed'); self.play(Create(tick(3.25,2.55)),run_time=.35); self.finish()

class S22(SpokenScene):
    def construct(self):
        self.add(head('A repair puts back what is missing').shift(UP*.22))
        # Full-size text, common colours and linked boxes in two horizontal chains.
        for y in [1.15,-1.5]:
            for x in [-1.65,2.55]: self.add(arr(p(x-.25,y),p(x+.25,y)))
            for i,x in enumerate([-3.75,.45,4.65]):
                box=RoundedRectangle(width=3.25,height=2.1,corner_radius=.25,color=BLUE if i<2 else GREEN,fill_opacity=.06).move_to(p(x,y))
                icon=link_icon(i).scale(.4).move_to(p(x,y+.25))
                label=lab(['hair cell','ribbon synapse','nerve fibre'][i],x,y-.65,28,BLUE if i<2 else GREEN)
                if y<0 and i==0:
                    box=DashedVMobject(box.set_fill(opacity=0),num_dashes=24); icon.set_opacity(0)
                self.add(box,icon,label)
        missing=lab('missing cell',-3.75,-3.05,30,RED); self.add(missing)
        mol=DashedVMobject(RoundedRectangle(width=.48,height=.52,corner_radius=.05,color=BLUE,stroke_width=5,fill_opacity=.35),num_dashes=10).move_to(p(-3.75,1.4))
        self.add(mol,lab('surviving cell',-3.75,2.55,28,BLUE))
        self.at('a molecule'); self.play(FadeIn(lab('missing molecule',-.2,2.55,28,BLUE)),Create(arr(p(-1.6,2.4),p(-3.4,1.55),BLUE)),run_time=.35)
        self.at('or the cell itself'); self.play(Indicate(missing,color=RED),run_time=.35); self.finish()

class S23(SpokenScene):
    def construct(self):
        self.add(head('52 cochleas · Wu and colleagues, 2021'))
        bone=VMobject(color=GREY,fill_opacity=.12).set_points_smoothly([p(-5.8,1.8),p(-4.7,2.25),p(-3.7,1.6),p(-3.9,.7),p(-3.4,-.2),p(-4.4,-1.45),p(-5.6,-1.2),p(-6,.1),p(-5.8,1.8)])
        coil=cochlea().scale(.6).move_to(p(-4.8,.5))
        field=RoundedRectangle(width=3.9,height=4.5,corner_radius=.2,color=GREY).move_to(p(-1.1,0))
        fibres=VGroup()
        for i in range(12):
            x=-2.75+i*.3
            f=Line(p(x,-2.05),p(x,2.05),color=GREEN,stroke_width=6)
            if i in [1,3,4,6,8,10]: f=DashedLine(p(x,-2.05),p(x,2.05),color=GREY,stroke_width=3)
            fibres.add(f)
        self.add(bone,coil,field,fibres,arr(p(-4.1,.5),p(-3.3,.5)),lab('temporal bone',-4.7,-2.05,26))
        ear=VGroup(Arc(radius=1.55,start_angle=-PI/2,angle=PI*1.65,color=TEXT),Arc(radius=.9,start_angle=-PI/2,angle=PI*1.4,color=TEXT),Arc(radius=.4,start_angle=0,angle=PI*1.5,color=TEXT)).move_to(p(3.9,.4))
        living=VGroup(ear,lab('?',3.9,.4,64,YELLOW),lab('living ear:\nno synapse count',3.9,-2.6,28))
        self.add(living)
        self.at('nerve fiber loss'); self.play(Indicate(fibres,scale_factor=1.01),run_time=.4)
        self.at('after death'); self.play(FadeIn(lab('after death: fibre counts',-3,-2.75,28,GREEN)),run_time=.3)
        self.at('No one can count'); self.play(Indicate(living,scale_factor=1.01),run_time=.5); self.finish()

class S23b(SpokenScene):
    def construct(self):
        cards=VGroup(*[RoundedRectangle(width=5.8,height=5.5,corner_radius=.25,color=TEAL,fill_opacity=.06).move_to(p(x,-.2)) for x in [-3.15,3.15]])
        self.add(cards,head('Evidence from living ears'),lab('SP/AP ratio',-3.15,2.1,32),lab('Liberman 2016',-3.15,1.4,28),lab('ABR and EFR',3.15,2.1,32),lab('Guest 2018',3.15,1.4,28),arr(p(-3.15,-.9),p(-3.15,.7),TEAL),Line(p(1.4,-.1),p(4.9,-.1),color=TEAL,stroke_width=7),lab('higher',-3.15,-1.5,32,TEAL),lab('no association',3.15,-1.5,30,TEAL))
        self.at('only indirect signals'); self.play(FadeIn(lab('INDIRECT',-3.15,-2.45,30,TEAL)),FadeIn(lab('INDIRECT',3.15,-2.45,30,TEAL)),run_time=.35)
        self.at('the evidence'); self.play(Indicate(cards,scale_factor=1.01),run_time=.4); self.finish()

class S24(SpokenScene):
    def construct(self):
        self.add(head('Good news about sensitivity',YELLOW))
        # Purpose-built wide test card keeps its labels at full size.
        chart=VGroup(RoundedRectangle(width=5.6,height=2.55,corner_radius=.2,color=GREY).move_to(p(0,1.35)),lab('hearing test',0,2.18,28,YELLOW),Line(p(-2.2,.85),p(2.2,.85),color=GREY),Line(p(-2.2,.85),p(-2.2,1.8),color=GREY),DashedLine(p(-2.05,1.4),p(2.1,1.4),color=GREY,stroke_width=6),Line(p(-2.05,1.4),p(2.1,1.4),color=YELLOW,stroke_width=3),lab('frequency',0,.4,26))
        chart.shift(UP*.15)
        self.add(chart,lab('normal',-4.2,1.4,34,YELLOW))
        for i,(x,name,c) in enumerate([(-4.2,'hair cell',BLUE),(0,'ribbon synapse',BLUE),(4.2,'nerve fibre',GREEN)]):
            self.add(RoundedRectangle(width=3.5,height=2.75,corner_radius=.3,color=c,fill_opacity=.06).move_to(p(x,-1.6)),link_icon(i).scale(.65).move_to(p(x,-1.2)),lab(name,x,-2.5,28,c))
        self.add(chain_arrows().shift(DOWN*1.6))
        self.at('A normal threshold'); self.play(Create(tick(4,1.4)),run_time=.35)
        self.at('not a census'); self.play(FadeIn(lab('Not a census of synapses',0,-3.35,32)),run_time=.4); self.finish()

class S25End(EndCard):
    LINE='A normal threshold is not a census of synapses.'
