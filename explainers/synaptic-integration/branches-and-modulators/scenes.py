"""Chapter 6, review fix round.
COLOR MAP: BLUE neuron; GREEN excitation/NMDA; RED fast inhibitory synapse;
GREY structure/leak/total conductance; YELLOW voltage; TEAL threshold;
PURPLE KCNQ; GOLD modulation; ORANGE nearby branch.
Calculated illustrations: passive C=200 pF, gL=10 nS, EL=-65 mV,
gK=2 nS, EK=-90 mV, I=100 pA. KCNQ-open rest = -69.17 mV.
NMDA block B(V)=1/(1+exp(-.062V)/3.57), illustrative Mg=1 mM.
Logistic comparison is normalized, not digitized data. PIP2 exponential
half-time 5 s is illustrative. Rasters are illustrative counts, not recordings.
"""
import numpy as np
from bp_style import *
from bp_style import SpokenScene as BaseSpokenScene
PURPLE='#B58BE8'
ORANGE='#F3A45C'
OPEN=(10*-65+2*-90)/12

class SpokenScene(BaseSpokenScene):
    # Same word timing as the pipeline, without creating an unrequested sync.log.
    def at(self,phrase,lead=.2,nth=0):
        rest=self.t_of(phrase,nth)-lead-self.elapsed()
        if rest>.02: self.wait(rest)

def label(s,x=0,y=0,size=28,color=TEXT):
    return T(s,size,color).move_to([x,y,0])
def heading(s): return label(s,0,3.15,30)
def path(pts,color=YELLOW,width=5):
    return VMobject(color=color,stroke_width=width).set_points_as_corners(pts)
def curve(fn,p,lo=0,hi=1,color=YELLOW,width=5):
    return path([p(t,fn(t)) for t in np.linspace(lo,hi,241)],color,width)
def vx(v): return -5.3+(v+90)/90*10.6
def B(v): return 1/(1+np.exp(-.062*v)/3.57)

def gauge(v=OPEN,k=True,exc=False):
    a=VGroup(Line([-5.3,-.8,0],[5.3,-.8,0],color=GREY))
    for val in [-90,-65,0]:
        x=vx(val); a.add(Line([x,-.94,0],[x,-.66,0],color=GREY),label(str(val).replace('-','−'),x,-1.28,26))
    a.add(label('membrane voltage (mV)',0,-1.88,26))
    d=Dot([vx(v),-.8,0],radius=.17,color=YELLOW)
    # The horizontal bottom line represents summed conductance, not a force vector.
    bottom=Line([-4.8,-2.65,0],[4.8 if k else 3.2,-2.65,0],color=GREY,stroke_width=18 if k else 10)
    er=Line(d.get_center(),[5.3,1.8,0],color=GREEN,stroke_width=3+28*B(v))
    kr=Line([-5.3,1.8,0],d.get_center(),color=PURPLE,stroke_width=12)
    return VGroup(a,d,bottom,er if exc else VGroup(),kr if k else VGroup())
def dial(x=3.8,y=2.35):
    return VGroup(Circle(radius=.43,color=GOLD).move_to([x,y,0]),Line([x,y,0],[x+.28,y+.25,0],color=GOLD,stroke_width=5),label('modulator',x,y+.75,26,GOLD))
def tree():
    n=[[-5,2.65,0],[-5,.35,0],[-5,-2.55,0],[-1.8,1.55,0],[-1.8,-1.85,0],[1.2,-.1,0],[4.6,-2,0]]
    e=[(0,3),(1,3),(2,4),(3,5),(4,5),(5,6)]
    tr=VGroup(VGroup(*[Line(n[a],n[b],color=BLUE,stroke_width=12) for a,b in e]),Circle(radius=.72,color=BLUE,fill_color=BLUE,fill_opacity=.2).move_to([5.1,-2.3,0]))
    return tr,n

def patches(n):
    g=VGroup()
    for a,b in [(0,3),(1,3),(2,4),(3,5),(4,5),(5,6)]:
        p=(np.array(n[a])+n[b])/2
        box=RoundedRectangle(width=1.55,height=1.0,corner_radius=.12,color=GREY,fill_color=BG,fill_opacity=1).move_to(p)
        g.add(VGroup(box,Line(p+[-.58,-.25,0],p+[.58,-.25,0],color=GREY),Line(p+[-.58,.32,0],p+[-.08,-.25,0],color=GREY,stroke_width=4),Line(p+[-.08,-.25,0],p+[.58,.32,0],color=GREEN,stroke_width=4),Dot(p+[-.08,-.25,0],radius=.09,color=YELLOW)))
    return g

def graph(ylabel=True):
    # Square data coordinates, 5.6 units high; labels use the side margins.
    p=lambda x,y:np.array([-2.75+5.6*x,-2.45+5.6*y,0])
    ax=VGroup(Line(p(0,0),p(1,0),color=GREY),Line(p(0,0),p(0,1),color=GREY))
    xl=label('expected response',.05,-2.98,28)
    sub=label('sum of separate responses',.05,-3.48,26)
    yl=label('measured response\n(both together)',-4.95,.3,26)
    diag=DashedLine(p(0,0),p(1,1),color=GREY,dash_length=.13)
    lin=label('linear',3.6,2.8,27)
    return VGroup(ax,xl,sub,*([yl] if ylabel else [])),p,VGroup(diag,lin)
def model_note(): return label('normalized illustration · not digitized data',0,3.65,26,GREY)
def sig(x):
    f=lambda z:1/(1+np.exp(-12*(z-.47)))
    return .95*(f(x)-f(0))/(f(1)-f(0))
def dots(p): return VGroup(*[Dot(p(x,x),radius=.075,color=TEXT) for x in np.linspace(.1,.9,9)])
def sigdots(p): return VGroup(*[Dot(p(x,sig(x)),radius=.075,color=ORANGE) for x in np.linspace(.06,.96,15)])
def comparison():
    ax,p,d=graph(); return VGroup(ax,d,model_note(),dots(p)),p

def baseline_panel():
    p=lambda t,v:np.array([.5+5*t/80,-2.8+v*.17,0])
    a=VGroup(Line(p(0,0),p(80,0),color=GREY),label('KCNQ-open response',3,-.25,26,PURPLE),label('voltage change',3,-3.25,26),curve(lambda t:100/12*(1-np.exp(-t/(200/12))),p,0,80,PURPLE))
    a.add(label('current step',3,.4,26),Line(p(0,0),p(0,10),color=GREY),path([[.5,-1,0],[1,-1,0],[1,-.7,0],[5,-.7,0],[5,-1,0],[5.5,-1,0]],GREY,3))
    return a

def question_frame():
    g=gauge(k=False)
    g[2].set_opacity(0)
    for m in list(g[0].submobjects):
        if isinstance(m,Text): g[0].remove(m)
    # Position the geometry using its voltage marker, independent of labels.
    g.scale(.58)
    g.shift(np.array([-4.45,.55,0])-g[1].get_center())
    g.add(label('voltage →',-3.25,-.15,26))
    target=g[1].get_center()
    electrode=VGroup(Line([-.9,2.15,0],target+[.35,.3,0],color=GREY,stroke_width=7),label('electrode',-.6,2.65,26),Arrow(target+[.35,.3,0],target,buff=0,color=YELLOW))
    q=label('Pause. What happens to the response\nto the same current step?',0,3.3,28)
    return VGroup(g,electrode,q,baseline_panel())

def step_path():
    return path([[-2.8,1.75,0],[-2.3,1.75,0],[-2.3,2.35,0],[5.2,2.35,0],[5.2,1.75,0],[5.8,1.75,0]],GREY,4)
def rasters(before='before',after='after'):
    g=VGroup(step_path(),label('same injected current',1.4,2.9,26))
    for y,n,name,col in [(.45,8,before,TEXT),(-1.65,14,after,YELLOW)]:
        g.add(label(name,-4.65,y,26,col),Line([-2.8,y,0],[5.8,y,0],color=GREY),VGroup(*[Line([x,y-.6,0],[x,y+.6,0],color=col,stroke_width=4) for x in np.linspace(-2.2,5.1,n)]))
    g.add(label('illustrative spike counts',1.4,-2.85,26,GREY)); return g

class S00Title(TitleCard):
    LESSON='Integration, Inhibition and Neuromodulation'
    TITLE='Branches and Modulators Change the Ropes'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.4,26,TEAL),label(self.LESSON,0,1.5,26,GREY))
        self.play(FadeIn(label('Branches and Modulators\nChange the Ropes',0,-.1,46)),Create(Line([-1.2,-1.7,0],[1.2,-1.7,0],color=GOLD)),run_time=.8); self.finish()

class S01Question(SpokenScene):
    def construct(self):
        g=gauge(v=-65,k=False,exc=True); self.add(g,label('NMDA rope',3.4,2.1,28,GREEN),heading('What if voltage strengthens a rope?'))
        self.at('a rope grows'); self.play(g[1].animate.move_to([vx(-40),-.8,0]),Transform(g[3],Line([vx(-40),-.8,0],[5.3,1.8,0],color=GREEN,stroke_width=3+28*B(-40))),run_time=1.2)
        self.at('or a modulator'); self.play(FadeIn(dial(-3,1.9)),Transform(self.mobjects[2],heading('What if a modulator changes the ropes?')),run_time=.65); self.finish()

class S02Dendrite(SpokenScene):
    def construct(self):
        tr,n=tree(); ps=patches(n); self.add(tr,ps,label('Each dendritic patch has its own ropes',0,3.55,30))
        self.at('passes current'); arrows=VGroup()
        # Follow the branch through its junction, clipping at each patch box.
        def edge(center, junction):
            delta=junction-center
            return center+delta*min(.83/abs(delta[0]) if delta[0] else np.inf,
                                    .56/abs(delta[1]) if delta[1] else np.inf)
        for a,b,j in [(0,3,3),(1,3,3),(2,4,4),(3,5,5),(4,5,5)]:
            junction=np.array(n[j]); start=edge(ps[a].get_center(),junction); end=edge(ps[b].get_center(),junction)
            u=(junction-start)/np.linalg.norm(junction-start)
            w=(end-junction)/np.linalg.norm(end-junction)
            arrows.add(VGroup(path([start,junction,end],YELLOW,3),
                Arrow(start+u*.22,start,buff=0,color=YELLOW,stroke_width=3,max_tip_length_to_length_ratio=.65),
                Arrow(end-w*.22,end,buff=0,color=YELLOW,stroke_width=3,max_tip_length_to_length_ratio=.65)))
        start=edge(ps[5].get_center(),np.array(n[6]))
        end=tr[1].get_center(); delta=end-start
        end=end-delta/np.linalg.norm(delta)*.79
        arrows.add(Arrow(start,end,buff=0,color=YELLOW,stroke_width=3))
        self.play(FadeIn(arrows),run_time=.8); self.finish()

class S03Filter(SpokenScene):
    def construct(self):
        tr,n=tree(); ps=patches(n); self.add(tr,ps)
        self.at('patches set'); self.play(Indicate(ps,color=YELLOW,scale_factor=1.03),run_time=.5)
        p=lambda t,v:np.array([-4.6+t/80*10,-2.6+v*4.3,0])
        # Alpha impulse followed by a second identical low-pass RC stage;
        # convolution gives t² exp(-t/tau), with spatial attenuation exp(-.55).
        local=lambda t:(t/8)*np.exp(1-t/8)
        remote=lambda t:np.exp(-.55)*np.e/2*(t/8)**2*np.exp(-t/8)
        ax=VGroup(Line(p(0,0),p(80,0),color=GREY),Line(p(0,0),p(0,1),color=GREY),label('voltage change',-3.7,2.2,26),label('time',5.3,-3.1,26))
        self.at('The length constant'); self.play(FadeOut(ps),tr.animate.scale(.32).move_to([3.5,2.1,0]),FadeIn(ax),Create(curve(local,p,0,80,TEXT,4)),FadeIn(label('local bump',-2,1.7,26)),FadeIn(label('length constant → smaller',-2,3.2,28,YELLOW)),run_time=.7)
        self.at('and the capacitance'); self.play(FadeIn(label('capacitance → broader',-2,2.65,28,YELLOW)),run_time=.4)
        self.at('shrink and smooth'); self.play(Create(curve(remote,p,0,80,YELLOW)),FadeIn(label('at soma',1,-.45,28,YELLOW)),run_time=1.1); self.finish()

class S04Polsky(SpokenScene):
    def construct(self):
        self.add(heading('Polsky, Mel & Schiller'),label('Nature Neuroscience · 2004',0,2.55,26),label('thin dendrite · confocal-guided sites',0,-2.7,28,BLUE))
        branch=Line([-5.8,-1,0],[5.8,-1,0],color=BLUE,stroke_width=26)
        sites=VGroup(*[VGroup(Line([x-1.2,1.9,0],[x,-.8,0],color=GREY,stroke_width=9),Dot([x,-1,0],radius=.23,color=GREEN),label('site '+str(i+1),x,-1.8,28,GREEN)) for i,x in enumerate([-2.5,2.5])])
        self.add(branch,sites)
        beat=label('site 1 alone',0,.3,32,GREEN)
        self.at('two sites'); self.play(FadeIn(beat),sites[0][1].animate.scale(1.6),run_time=.4)
        self.at('pyramidal neurons'); self.play(Transform(beat,label('site 2 alone',0,.3,32,GREEN)),sites[0][1].animate.scale(1/1.6),sites[1][1].animate.scale(1.6),run_time=.4)
        self.at('then both together',lead=.55); self.play(Transform(beat,label('both together',0,.3,32,GREEN)),sites[0][1].animate.scale(1.6),run_time=.3); self.wait(2); self.finish()

class S05Graph(SpokenScene):
    def construct(self):
        ax,p,d=graph(False); self.add(ax[0],model_note())
        self.at('Along the bottom'); self.play(FadeIn(VGroup(*ax[1:])),run_time=.6); self.finish()
class S06Graph2(SpokenScene):
    def construct(self):
        ax,p,d=graph(); self.add(*ax[:3],model_note())
        self.at('Up the side'); self.play(FadeIn(ax[3]),run_time=.5)
        self.at('A point on'); self.play(Create(d[0]),FadeIn(d[1]),FadeIn(Dot(p(.6,.6),radius=.075,color=TEXT)),run_time=.8); self.finish()
class S07Linear(SpokenScene):
    def construct(self):
        ax,p,d=graph(); self.add(ax,d,model_note(),Dot(p(.6,.6),radius=.075,color=TEXT).set_z_index(10))
        self.at('Inputs far apart'); self.play(FadeIn(VGroup(*[Dot(p(x,x),radius=.075,color=TEXT) for x in np.linspace(.1,.9,9) if abs(x-.6)>.01])),FadeIn(label('different branches\nor far apart',4.7,.25,26)),Create(Line(p(.74,.74),[3.3,.65,0],color=TEXT)),run_time=.8); self.finish()
class S08Sigmoid(SpokenScene):
    def construct(self):
        g,p=comparison(); self.add(g,sigdots(p))
        self.at('Nearby inputs'); self.play(FadeIn(label('same thin branch,\nnearby',4.65,-1.25,26,ORANGE)),Create(Line(p(.65,sig(.65)),[3.4,-.85,0],color=ORANGE)),run_time=.65)
        for phrase,a,b in [('rose slowly',0,.35),('then steeply',.35,.64),('then leveled off',.64,1)]:
            self.at(phrase); self.play(Create(curve(sig,p,a,b,ORANGE)),run_time=.45)
        self.finish()
class S09Subunits(SpokenScene):
    def construct(self):
        tr,n=tree(); outlines=VGroup()
        for line in tr[0]:
            box=RoundedRectangle(width=line.get_length()*.48,height=.6,corner_radius=.25,color=ORANGE,stroke_width=3).rotate(line.get_angle()).move_to(line.get_center()); outlines.add(box)
        self.add(tr)
        self.at('location set'); self.play(FadeIn(heading('Location sets the combination rule')),run_time=.4)
        self.at('thin branches'); self.play(LaggedStart(*[FadeIn(o) for o in outlines],lag_ratio=.28),run_time=1.5)
        self.at('separate integrating subunits'); self.play(FadeIn(label('separate integrating subunits',0,-3.3,28,ORANGE)),run_time=.4); self.finish()
class S10Nmda(SpokenScene):
    def construct(self):
        g,p=comparison(); self.add(g,curve(sig,p,color=ORANGE))
        self.at('The steep phase'); self.play(Create(curve(sig,p,.35,.64,YELLOW,10)),FadeIn(label('local regenerative\nevent',4.65,.25,26,YELLOW)),Create(Line(p(.5,sig(.5)),[3.3,.25,0],color=YELLOW)),run_time=.6)
        self.at('receptors are thought',lead=.55); self.play(FadeIn(chip('NMDA',GREEN,28).move_to([4.7,2,0])),FadeIn(label('thought to\ntake part',4.7,1.1,26,GREEN)),GrowArrow(Arrow([3.8,1.8,0],p(.57,sig(.57)),color=GREEN,buff=.1)),run_time=.65); self.finish()

class S11NmdaRope(SpokenScene):
    def construct(self):
        g=gauge(v=-65,k=False,exc=True); self.add(g,label('bottom line',0,-3.25,28,GREY))
        gate=RoundedRectangle(width=2.1,height=1.3,corner_radius=.4,color=GREEN,fill_color=BG,fill_opacity=1).move_to([4.5,2.35,0])
        self.add(gate,label('NMDA',4.5,2.65,28,GREEN))
        glu=chip('glutamate',GREEN,26).move_to([1.6,2.95,0]); co=chip('co-agonist',GREEN,26).move_to([4.9,3.35,0])
        self.at('glutamate and'); self.play(FadeIn(glu),Create(Line([2.4,2.85,0],[3.45,2.55,0],color=GREEN)),run_time=.4)
        self.at('have bound'); self.play(FadeIn(co),Create(Line([4.9,3,0],[4.9,2.95,0],color=GREEN)),run_time=.4)
        mouth=np.array([4.5,1.6,0])
        self.add(Line(gate.get_bottom(),mouth,color=GREEN,stroke_width=4))
        mg=chip('Mg²⁺',GREY,26).move_to(mouth).set_z_index(2); mg[0].set_fill(BG,opacity=1); self.add(mg)
        v=ValueTracker(-65); rope=always_redraw(lambda:Line([vx(v.get_value()),-.8,0],mouth,color=GREEN,stroke_width=3+28*B(v.get_value())))
        self.remove(g[3]); self.add(rope); rope.set_z_index(-1)
        self.at('thickens as'); self.play(v.animate.set_value(-48),g[1].animate.move_to([vx(-48),-.8,0]),run_time=1.1)
        self.at('Depolarization pushes out'); self.play(v.animate.set_value(-40),g[1].animate.move_to([vx(-40),-.8,0]),mg.animate.move_to(mouth*.62+np.array([vx(-40),-.8,0])*.38),run_time=1.1); self.finish()
class S12Outrun(SpokenScene):
    def construct(self):
        g=gauge(v=-65,k=False); self.add(g[0],g[1],heading('Over this range'))
        self.add(Line([vx(-65),-1.02,0],[vx(-40),-1.02,0],color=YELLOW),Line([vx(-65),-.95,0],[vx(-65),-1.09,0],color=YELLOW),Line([vx(-40),-.95,0],[vx(-40),-1.09,0],color=YELLOW))
        v=ValueTracker(-65)
        rope=always_redraw(lambda:Line([vx(v.get_value()),-.8,0],[5.3,1.8,0],color=GREEN,stroke_width=3+28*B(v.get_value())))
        drive=always_redraw(lambda:Arrow([vx(v.get_value()),-2.45,0],[5.3,-2.45,0],color=TEXT,buff=0,stroke_width=3))
        def pull_vector():
            start=np.array([vx(v.get_value()),-.8,0]); end=np.array([5.3,1.8,0])
            unit=(end-start)/np.linalg.norm(end-start)
            normal=np.array([-unit[1],unit[0],0])*.5
            origin=start+(end-start)*.32+normal
            return Arrow(origin,origin+unit*(-v.get_value())*B(v.get_value())*.32,color=GREEN,buff=0,stroke_width=7)
        pull=always_redraw(pull_vector)
        self.add(rope,drive,pull,label('driving force',3,-2.95,26),label('pull',.5,1.55,28,GREEN),label('NMDA rope',4.7,2.3,28,GREEN))
        self.at('it thickens faster'); self.play(v.animate.set_value(-48),g[1].animate.move_to([vx(-48),-.8,0]),run_time=1.5)
        self.at('its pull grows'); self.play(v.animate.set_value(-40),g[1].animate.move_to([vx(-40),-.8,0]),run_time=.8); self.finish()
class S13Mod(SpokenScene):
    def construct(self):
        g=gauge(); d=dial(3.7,1.75); self.add(g,d,label('KCNQ',-4.8,2.2,28,PURPLE),label('standing conductance',0,-3.25,28,GREY))
        fast=Line(g[1].get_center(),[5.3,1.4,0],color=RED,stroke_width=10); lab=label('fast synapse',3.5,.25,28,RED)
        self.at('A fast synapse'); self.play(Create(fast),FadeIn(lab),run_time=.4)
        self.at('A modulator'); self.play(FadeOut(fast),FadeOut(lab),run_time=.35)
        self.at('can instead change'); self.play(Rotate(d[1],-.9,about_point=d[0].get_center()),g[4].animate.set_stroke(width=5),g[2].animate.set_stroke(width=12),run_time=1); self.finish()
class S14Kcnq(SpokenScene):
    def construct(self):
        g=gauge(); self.add(g,heading('sympathetic neuron'),label('KCNQ (M-current)',-3.8,2.4,28,PURPLE),label('near E_K',-5.7,.65,26,PURPLE),label('bottom line',0,-3.25,26,GREY))
        ach=chip('acetylcholine',GOLD,26).move_to([2.1,2.35,0]); r=chip('M1 · Gq-coupled',GOLD,26).move_to([1.4,1,0])
        self.at('coupled'); self.play(FadeIn(ach),run_time=.4)
        self.at('muscarinic receptors'); self.play(FadeIn(r),GrowArrow(Arrow(ach.get_bottom(),r.get_top(),color=GOLD,buff=.08)),GrowArrow(Arrow(r.get_left(),g[4].get_center(),color=GOLD,buff=.15)),run_time=.6)
        self.at('potassium channels'); self.play(FadeOut(g[4]),g[1].animate.move_to([vx(-65),-.8,0]),Transform(g[2],gauge(k=False)[2]),run_time=.8); self.wait(2); self.finish()
class S15Pip2(SpokenScene):
    def construct(self):
        self.add(heading('Suh, Inoue, Meyer & Hille · Science · 2006'))
        membrane=Line([-5.5,2.05,0],[5.5,2.05,0],color=GREY,stroke_width=10)
        lip=VGroup(*[chip('PIP2',GOLD,26).move_to([x,2.55,0]) for x in [-3.5,-1.2,1.2]])
        self.add(membrane,label('membrane',5.2,1.65,24,GREY),lip,chip('KCNQ',PURPLE,28).move_to([4.2,2.55,0]))
        p=lambda t,i:np.array([-4.5+t*.48,-2.55+i*3.5,0])
        ax=VGroup(Line(p(0,0),p(20,0),color=GREY),Line(p(0,0),p(0,1.13),color=GREY),label('KCNQ current',-4,1.65,28,PURPLE),label('before',-5.4,.95,26),label('0',-4.9,-2.55,26),label('time after depletion',.3,-3.2,28),label('illustrative kinetics',2,1.3,26,GREY),DashedLine(p(0,1),p(20,1),color=GREY))
        self.add(ax)
        self.at('depleting the membrane'); self.play(LaggedStart(*[FadeOut(lipid,shift=UP*.3) for lipid in lip],lag_ratio=.65),run_time=2)
        decay=lambda t:np.exp(-np.log(2)*t/5)
        self.at('enough to suppress'); self.play(Create(curve(decay,p,0,8,PURPLE,6)),run_time=2.1)
        self.at('lipid itself'); self.play(Indicate(membrane,color=GOLD),Create(curve(decay,p,8,20,PURPLE,6)),run_time=2.2); self.finish()
class S16Predict(SpokenScene):
    def construct(self):
        f=question_frame(); k=gauge()[4].scale(.58,about_point=ORIGIN)
        # Match the transformed gauge exactly.
        original=gauge(k=False); shift=f[0][1].get_center()-original[1].get_center()*.58
        k.shift(shift); kl=label('KCNQ',-5.4,2.4,28,PURPLE); self.add(f[0],k,kl,f[3])
        self.at('removes a potassium rope'); self.play(FadeOut(k),FadeOut(kl),run_time=.7)
        self.at('What happens'); self.play(FadeIn(VGroup(f[1],f[2])),run_time=.6); self.finish()
class S17Pause(Scene):
    def construct(self): self.camera.background_color=BG; self.add(question_frame()); self.wait(5)
class S18Reveal(SpokenScene):
    def construct(self):
        # Continue the removed-rope state: the bottom line and voltage now respond.
        g=gauge(k=False); g[1].move_to([vx(OPEN),-.8,0]); bottom=gauge()[2]; g.remove(g[2]); self.add(g,bottom,heading('fixed-conductance passive approximation'),label('bottom line: total conductance',0,-3.25,28,GREY))
        self.at('raises the resting voltage'); self.play(g[1].animate.move_to([vx(-67),-.8,0]),run_time=1.5)
        self.at('shrinks the bottom line'); self.play(bottom.animate.put_start_and_end_on([-4.8,-2.65,0],[3.2,-2.65,0]).set_stroke(width=10),g[1].animate.move_to([vx(-65),-.8,0]),run_time=1.1)
        self.at('The same sustained'); self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.3)
        p=lambda t,v:np.array([-4.65+t/80*9.6,-2.25+v*.44,0])
        ax=VGroup(Line(p(0,0),p(80,0),color=GREY),Line(p(0,0),p(0,11),color=GREY),label('time after current step (ms)',.3,-3.08,26),label('voltage change\nfrom own rest',-5.3,3.1,26),label('fixed-conductance passive approximation',1,3.55,26))
        for t in [0,20,40,60,80]: ax.add(label(str(t),p(t,0)[0],-2.65,26))
        for v in [0,5,10]: ax.add(label(str(v),-5.05,p(0,v)[1],26))
        ax.add(label('mV',-5.6,2,26))
        self.play(FadeIn(ax),Create(curve(lambda t:100/12*(1-np.exp(-t/(200/12))),p,0,80,TEXT)),FadeIn(label('KCNQ open',3,.65,26)),run_time=.6)
        self.at('larger steady change'); self.play(Create(curve(lambda t:10*(1-np.exp(-t/20)),p,0,80,YELLOW)),FadeIn(label('KCNQ closed',3,2.65,26,YELLOW)),run_time=.7)
        marks=VGroup()
        for tau,amp,col,dx,dy in [(200/12,100/12,TEXT,-.85,.7),(20,10,YELLOW,.8,1.1)]:
            pos=p(tau,amp*(1-np.exp(-1))); marks.add(Dot(pos,color=col,radius=.1),DashedLine(p(tau,0),pos,color=col),label('63%',pos[0]+dx,pos[1]+dy,26,col))
        self.at('takes longer'); self.play(FadeIn(marks),run_time=.5)
        self.play(FadeIn(label('Synaptic EPSP need not grow: less excitatory driving force',0,-3.6,26)),run_time=.3); self.wait(1.5); self.finish()
class S19More(SpokenScene):
    def construct(self):
        g=rasters('before','muscarinic\nagonist'); g[1].move_to([1.4,1.35,0]); self.add(*g[:5],g[-1])
        self.at('increases excitability'); self.play(FadeIn(VGroup(*g[5:-1])),run_time=.5)
        self.at('fires more'); self.play(FadeIn(heading('Closing KCNQ increases excitability')),run_time=.4); self.finish()
class S20D1(SpokenScene):
    def construct(self):
        g=rasters('before','after dopamine\naxon stimulation'); g[1].move_to([1.4,1.35,0])
        self.add(heading('Dopamine · D1 receptors'),label('Lahiri & Bevan · Neuron · 2020',0,-3.5,26),*g[:5],g[-1])
        self.at('mouse striatal neurons'); self.play(FadeIn(label('mouse striatum',-4.5,2.4,26,BLUE)),run_time=.4)
        self.at('firing to the same'); self.play(FadeIn(VGroup(*g[5:-1])),run_time=.7); self.finish()
class S21D1Time(SpokenScene):
    def construct(self):
        self.add(heading('One bout of dopamine-axon stimulation'))
        self.add(Line([-4.7,-2.25,0],[5.7,-2.25,0],color=GREY),Line([-4.7,-2.25,0],[-4.7,1.95,0],color=GREY),label('firing rate',-4.5,2.25,28),label('baseline',-3.5,-1.55,26),Line([-4.7,-1,0],[5.7,-1,0],color=GREY),label('stimulation',-4.5,-2.85,26,GOLD),label('at least 10 minutes',3.8,-2.85,26),label('time axis compressed · schematic timing',0,-3.5,26,GREY),Line([3.7,-2.4,0],[3.7,-2.1,0],color=TEXT))
        self.at('rose within'); self.play(GrowArrow(Arrow([-4,-1,0],[-4,1.7,0],color=YELLOW,buff=0)),FadeIn(label('within hundreds\nof milliseconds',-1.5,.2,28,YELLOW)),run_time=.6)
        self.at('After one bout'); self.play(GrowArrow(Arrow([-4,1.7,0],[5.8,1.7,0],color=YELLOW,buff=0)),FadeIn(label('raised firing persists',1.4,2.35,28,YELLOW)),run_time=.8); self.finish()
class S22D1Rule(SpokenScene):
    def construct(self):
        self.add(label('Which conductance or active current changed?',0,3.55,30))
        g=gauge(); g[4].set_opacity(0); self.add(g[0],g[1],g[2])
        for x in [-5,-1,2,5]:
            self.add(Line([x,1.6,0],g[1].get_center(),color=GREY,stroke_width=7),label('?',x,2.05,40,GREY))
        self.at('synaptic receptors blocked'); self.play(FadeIn(label('receptor blockers',-3.2,2.85,26)),run_time=.4)
        self.at('and drift'); self.play(FadeIn(label('matched current-only control trials',2.4,2.85,26)),run_time=.4)
        self.at('must have changed'); self.play(FadeIn(label('same current, more spikes',0,-3.25,30,YELLOW)),run_time=.5)
        self.at('A spike count'); self.play(Indicate(VGroup(*[m for m in self.mobjects if isinstance(m,Text) and m.text=='?']),color=GOLD),run_time=.7); self.finish()
class S23Takeaway(SpokenScene):
    def construct(self):
        # Tall summary panels, with readable geometry rather than scaled text.
        self.add(label('NMDA ropes can\ngrow with voltage',-3.3,2.85,30,GREEN),label('Modulators change\nthe ropes themselves',3.3,2.85,30,GOLD),Line([0,-2.2,0],[0,3.5,0],color=GREY))
        def panel(x,v,k):
            p=lambda v: x-2.55+(v+90)/90*5.1
            d=Dot([p(v),-.7,0],radius=.15,color=YELLOW)
            return VGroup(Line([x-2.55,-.7,0],[x+2.55,-.7,0],color=GREY),d,Line(d.get_center(),[x+2.55,1.7,0],color=GREEN if not k else GREY,stroke_width=3+28*B(v) if not k else 10),Line([x-2.55,1.7,0],d.get_center(),color=PURPLE,stroke_width=12) if k else VGroup(),label('voltage →',x,-1.4,26))
        left=panel(-3.3,-65,False); right=panel(3.3,OPEN,True); right[2].set_opacity(0); right[3].set_color(GREY); d=dial(5.2,-.05); d[2].move_to([4.6,-2,0]); self.add(left,right,d,label('standing rope',2.1,1.8,26,GREY))
        self.at('rope grow with voltage'); self.play(left[1].animate.shift(RIGHT*1.42),Transform(left[2],Line(left[1].get_center()+RIGHT*1.42,[-.75,1.7,0],color=GREEN,stroke_width=3+28*B(-40))),run_time=.9)
        self.at('Modulators change'); self.play(Rotate(d[1],-.9,about_point=d[0].get_center()),right[3].animate.set_stroke(width=3,opacity=.3),run_time=.9)
        self.at('The rule tells'); self.play(FadeIn(label('The rule tells you what kind of change to look for.',0,-3.15,30)),run_time=.6); self.finish()
class S24End(EndCard):
    LINE='NMDA ropes can grow with voltage; modulators change the ropes themselves.'
    def construct(self):
        self.add(label('NMDA ropes can grow with voltage;\nmodulators change the ropes themselves.',0,.4,38),label('biochemistrypedia.com',0,-1.3,26,TEAL)); self.finish()
