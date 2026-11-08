"""Made, Then Lost — chapter 4, review revision.
COLOR MAP: BLUE neurons; GREEN survival / normal; RED death / disruption;
YELLOW NGF; TEAL production; PURPLE TrkA; GREY tissue / axes.
The schematic is computed by piecewise linear interpolation. The lesson anchors
E13.5=1 and E15.5=.85. The later .45 endpoint and unnumbered postnatal
coordinate are illustrative, NOT a measured age or magnitude. No late data claimed.
Neuron cartoons and qualitative comparison bars do not encode measured counts.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'

def label(s,p,size=28,color=TEXT): return T(s,size,color).move_to(p)
def head(s,color=TEXT): return label(s,[0,3.18,0],32,color)
def dot(p,color=BLUE,r=.32,op=.95):
    return Circle(radius=r,stroke_color=color,stroke_width=3,fill_color=color,fill_opacity=op).move_to(p)
def cross(p,s=.5):
    p=np.array(p,float)
    return VGroup(Line(p+[-s,-s,0],p+[s,s,0],color=RED,stroke_width=7),Line(p+[-s,s,0],p+[s,-s,0],color=RED,stroke_width=7))
def cluster(y=0, radius=.42):
    return VGroup(*[dot([x,z+y,0],r=radius) for z in [1,-1] for x in [-1.8,0,1.8]])
def mouse(scale=1.0,at=(0,0,0)):
    """Side-view mouse facing right. g.neck = the top of the neck, behind the ear."""
    pts=[(-2.2,-.4),(-1.2,.5),(0,.85),(1.2,.8),(2.0,.95),(2.7,.65),(3.2,.1),(3.15,-.15),(2.6,-.45),(1.8,-.75),(.8,-1.1),(-.5,-1.25),(-1.6,-1.1),(-2.3,-.8)]
    P=lambda q: np.array([q[0],q[1],0.])
    body=VMobject(stroke_color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.14).set_points_smoothly([P(q) for q in pts]+[P(pts[0])])
    ear=Ellipse(width=.85,height=1.15,stroke_color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.14).rotate(-.3).move_to(P((1.45,1.2)))
    eye=dot(P((2.55,.42)),TEXT,.08); nose=dot(P((3.17,.08)),TEXT,.07)
    whisk=VGroup(*[Line(P((2.95,y0)),P(e),color=GREY,stroke_width=2.5) for y0,e in [(.0,(3.85,.35)),(-.05,(3.9,-.1)),(-.1,(3.75,-.45))]])
    legs=VGroup(Line(P((-1.5,-1.15)),P((-1.7,-1.65)),color=GREY,stroke_width=7),Line(P((1.3,-.95)),P((1.45,-1.6)),color=GREY,stroke_width=7),
                Line(P((-1.8,-1.65)),P((-1.45,-1.65)),color=GREY,stroke_width=7),Line(P((1.35,-1.6)),P((1.75,-1.6)),color=GREY,stroke_width=7))
    tail=VMobject(color=GREY,stroke_width=4).set_points_smoothly([P(q) for q in [(-2.25,-.5),(-3.1,-1.0),(-3.9,-.7),(-4.4,.1),(-4.5,.9)]])
    g=VGroup(body,ear,eye,nose,whisk,legs,tail)
    c=g.get_center(); neck=P((.95,.5))-c
    g.shift(-c).scale(scale).shift(np.array(at,float))
    g.neck=neck*scale+np.array(at,float)
    return g
def evidence(bax=False, filled=True):
    title=head('Two knockouts' if not bax else 'Genetic evidence')
    headers=VGroup(label('Mutant',[-4.5,2.25,0]),label('Sympathetic',[-.6,2.25,0]),label('Many sensory',[3.7,2.25,0]))
    line=Line([-6,1.75,0],[6,1.75,0],color=GREY)
    names=VGroup(label('NGF-null',[-4.5,.9,0],32,YELLOW),label('TrkA-null',[-4.5,-.6,0],32,PURPLE))
    result=VGroup(*[label('lost',[x,y,0],34,RED) for y in [.9,-.6] for x in [-.6,3.7]])
    g=VGroup(title,headers,line,names,result)
    if bax:
        g.add(label('Bax-null',[-4.5,-2.1,0],32,RED),label('kept',[-.6,-2.1,0],34,GREEN))
    return g

# Plot coordinates reserve a separate right-hand rail for line-end labels.
AGES=np.array([13.5,15.5,19.5,26.5]); RATIOS=np.array([1,.85,.62,.45])
def plot():
    ax=Axes(x_range=[13.5,27.5,2],y_range=[0,1.15,.2],x_length=8.65,y_length=5.4,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([-.3,.05,0])
    labs=VGroup(label('Neuron number\n(relative to normal)',[-5.8,.15,0],26).rotate(PI/2),label('Embryonic → postnatal age',[.1,-3.55,0],28),label('schematic, not data',[3.7,3.35,0],26,GREY))
    tick=Line(ax.c2p(13.5,1)+LEFT*.1,ax.c2p(13.5,1)+RIGHT*.1,color=GREY)
    labs.add(tick,label('normal\n= 100%',[-5.5,2.15,0],26,GREEN))
    return ax,labs

def age_tick(ax,x,s):
    return VGroup(Line(ax.c2p(x,0)+UP*.08,ax.c2p(x,0)+DOWN*.08,color=GREY),label(s,ax.c2p(x,0)+DOWN*.36,26))
def age_labels(ax,early=False):
    g=VGroup(age_tick(ax,19.5,'Birth'),age_tick(ax,26.5,'later postnatal'))
    if early: g.add(age_tick(ax,13.5,'E13.5'))
    return g

def curves(ax,end=26.5):
    xs=list(AGES[AGES<end])+[end]
    return (VMobject(color=GREEN,stroke_width=6).set_points_as_corners([ax.c2p(x,1) for x in xs]),VMobject(color=PURPLE,stroke_width=6).set_points_as_corners([ax.c2p(x,np.interp(x,AGES,RATIOS)) for x in xs]))
def normal(ax): return Line(ax.c2p(13.5,1),ax.c2p(26.5,1),color=GREEN,stroke_width=6)
def endlabels(ax):
    return VGroup(label('Normal',ax.c2p(26.5,1)+RIGHT*.85,28,GREEN),label('TrkA-null',ax.c2p(26.5,.45)+RIGHT*1,28,PURPLE))
def gap(ax,x=15.5,lo=.85,hi=1,color=TEXT,pad=.02):
    a=ax.c2p(x,lo+pad); b=ax.c2p(x,hi-pad)
    return VGroup(Line(a,b,color=color,stroke_width=3),Line(a+LEFT*.12,a+RIGHT*.12,color=color),Line(b+LEFT*.12,b+RIGHT*.12,color=color))
def deficit(ax):
    # Offset the bracket from the actual two curves; short leaders mark its endpoints.
    g=gap(ax,16,.85,1)
    g.add(label('≈15% fewer',[-1.5,1.67,0],26,PURPLE))
    return g

def complete_plot():
    ax,labs=plot(); n,m=curves(ax)
    return VGroup(ax,labs,age_labels(ax,True),age_tick(ax,15.5,'E15.5'),n,m,endlabels(ax),deficit(ax))
def prediction(): return chip('TrkA-null: what shape?',PURPLE,28).move_to([-.8,3.2,0])
def prediction_plot():
    ax,labs=plot()
    return VGroup(ax,labs,age_labels(ax),normal(ax),endlabels(ax)[0],prediction())
def meaning():
    ax,_=plot()
    text=label('Produced, then lost',[.1,1.1,0],28,RED)
    bracket=gap(ax,24.5,float(np.interp(24.5,AGES,RATIOS)),1,RED,pad=.035)
    # Separate word above the bracket midpoint, left of the terminal legend.
    survival=label('survival',[3.2,1.35,0],26,RED)
    return VGroup(text,bracket,survival)
def reasoning():
    # A new comparison layout retains the same computed time course, with all
    # labels re-typeset at full size rather than shrinking the text with the plot.
    ax=Axes(x_range=[13.5,27.5,2],y_range=[0,1.15,.2],x_length=6.2,y_length=3.3,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([-2,.75,0])
    n,m=curves(ax)
    labs=VGroup(label('schematic, not data',[-2.4,2.65,0],26,GREY),label('Neuron number',[-6.35,.1,0],26).rotate(PI/2),label('normal\n= 100%',[-5.75,2.05,0],26,GREEN),label('Age',[-2,-1.75,0],26),label('Normal',ax.c2p(26.5,1)+RIGHT*.82,26,GREEN),label('TrkA-null',ax.c2p(26.5,.45)+RIGHT*.88,26,PURPLE))
    ticks=VGroup(age_tick(ax,13.5,'E13.5'),age_tick(ax,19.5,'Birth'),age_tick(ax,26.5,'later'))
    p=VGroup(ax,n,m,labs,ticks)
    boxes=VGroup(*[chip(s,GREY,26) for s in ['Too few precursors?','Failed differentiation?','Excess death?']]).arrange(DOWN,buff=.5).move_to([4.55,.85,0])
    return p,boxes

def inhib(a,b):
    a,b=np.array(a,float),np.array(b,float); d=(b-a)/np.linalg.norm(b-a); p=np.array([-d[1],d[0],0])
    return VGroup(Line(a,b,color=YELLOW,stroke_width=6),Line(b+p*.38,b-p*.38,color=YELLOW,stroke_width=9))
def brake():
    cell=Circle(radius=2.6,color=BLUE,fill_color=BLUE,fill_opacity=.08).move_to([2.55,-.05,0])
    death=chip('Bax-dependent\ndeath program',RED,30).move_to([2.55,-.05,0])
    ngf=chip('NGF signalling',YELLOW,30).move_to([-4.5,-.05,0])
    bar=inhib(ngf.get_right(),death.get_left()+LEFT*.1)
    return cell,death,ngf,bar
def held(c): return [c[0].animate.set_stroke(opacity=.45).set_fill(RED,.05),c[1].animate.set_opacity(.7)]
def live(c): return [c[0].animate.set_stroke(opacity=1).set_fill(RED,.3),c[1].animate.set_opacity(1)]
def dimmed(c): return [c[0].animate.set_stroke(opacity=.3).set_fill(YELLOW,.03),c[1].animate.set_opacity(.3)]
def bright(c): return [c[0].animate.set_stroke(opacity=1).set_fill(YELLOW,.16),c[1].animate.set_opacity(1)]

class S00Title(TitleCard):
    LESSON='The Neurotrophic Hypothesis Tested'
    TITLE='Made, Then Lost'
    def construct(self):
        self.add(label(self.TITLE,[0,.7,0],54),label(self.LESSON,[0,-.5,0],28,GREY),Line([-1,-1.2,0],[1,-1.2,0],color=GOLD)); self.wait(self.narration_s)

class S01Q(SpokenScene):
    def construct(self):
        g=VGroup(*[dot([x,y,0],r=.6) for y in [1.5,-1.5] for x in [-1.8,0,1.8]]); g[1:].set_opacity(.13)
        m=mouse(.34,[-4.8,1.25,0]); rec=chip('TrkA',PURPLE,28).move_to([4.7,1.25,0])
        self.add(head('Made, Then Lost'),g,m,rec,cross(rec.get_top()+UP*.35,.23))
        self.at('is born'); self.play(FadeIn(label('Too few sympathetic neurons',[0,-3,0],30,BLUE)),run_time=.4)
        self.at('never made'); self.play(FadeIn(chip('Never\nmade?',TEAL,28).move_to([-4.7,-.65,0])),run_time=.3)
        self.at('or made'); self.play(FadeIn(chip('Made, then\nlost?',RED,28).move_to([4.7,-.65,0])),run_time=.3); self.finish()

class S02Ko(SpokenScene):
    def construct(self):
        gene=VGroup(*[Rectangle(width=1.65,height=1.1,color=BLUE,fill_color=BLUE,fill_opacity=.18) for _ in range(5)]).arrange(RIGHT,buff=.08).move_to([0,.85,0])
        self.add(gene,label('gene',[-4.9,1.9,0],32),Line([-4.75,.2,0],[-4.75,1.5,0],color=TEAL,stroke_width=7))
        self.at('a knockout mouse'); self.play(FadeIn(head('Knockout')),run_time=.3)
        self.at('gene disrupted'); self.play(Create(cross(gene[2].get_center(),.65)),run_time=.4)
        self.at('no working protein'); self.play(FadeIn(chip('No working protein',RED,34).move_to([0,-1.25,0])),run_time=.4)
        self.at('no antibody'); self.play(FadeIn(label('No antibody involved',[0,-2.9,0],32)),run_time=.4); self.finish()

class S03Ngf(SpokenScene):
    def construct(self):
        m=mouse(1.3,[0,-.55,0]); tag=chip('NGF',YELLOW,36).move_to([-1.6,2.15,0])
        bp=m[0].get_points(); bp=bp[np.abs(bp[:,0]+1.6)<.15]; top=bp[np.argmax(bp[:,1])]
        lead=Line(tag.get_bottom(),top,color=YELLOW,stroke_width=4)
        self.add(m,head('Crowley and colleagues · 1994'))
        self.at('reported mice'); self.play(FadeIn(tag),Create(lead),run_time=.35)
        self.at('lacking'); self.play(Create(cross(tag.get_center(),.5)),FadeIn(label('NGF-null',[0,-3.05,0],38,YELLOW)),run_time=.4); self.finish()

class S04Trka(SpokenScene):
    def construct(self):
        membrane=Rectangle(width=11.5,height=1.05,color=GREY,fill_color=GREY,fill_opacity=.4).move_to([0,-.35,0])
        rec=RoundedRectangle(width=1.25,height=3,corner_radius=.15,color=PURPLE,fill_color=PURPLE,fill_opacity=.65).move_to([0,-.35,0])
        self.add(head('Smeyne, Klein, Barbacid\nand colleagues · 1994'),membrane,rec,label('outside',[-4.5,1.35,0],28),label('inside',[-4.5,-2.35,0],28),label('membrane',[4.5,-1.45,0],28,GREY),label('TrkA',[2.3,.3,0],34,PURPLE),Line([.7,.3,0],[1.55,.3,0],color=PURPLE))
        self.at('lacking a working'); self.play(Create(cross([0,-.35,0],.9)),run_time=.5)
        self.at('the receptor for'); self.play(FadeIn(chip('NGF',YELLOW,30).move_to([0,2,0])),run_time=.4); self.finish()

class S05Loss(SpokenScene):
    def construct(self):
        e=evidence(); self.add(*e[:4])
        self.at('lose sympathetic neurons'); self.play(FadeIn(VGroup(e[4][0],e[4][2])),run_time=.4)
        self.at('many sensory neurons'); self.play(FadeIn(VGroup(e[4][1],e[4][3])),run_time=.4)
        self.at('antibody doubt'); self.play(FadeIn(label('✓ Genetic necessity',[0,-2.6,0],34,GREEN)),run_time=.4); self.finish()

class S06Sens(SpokenScene):
    def construct(self):
        small=VGroup(*[dot([x,.6,0],r=.45) for x in [-5.2,-3.9,-2.6,-1.0]])
        large=VGroup(dot([2.2,.5,0],r=.78),dot([4.6,.5,0],r=.78))
        trka=VGroup(*small[:3],large[0])
        self.add(head('Sensory neurons'),small,large,label('small',[-3.1,2,0],32),label('large',[3.4,2,0],32))
        brk=VGroup(Line([-5.7,-.25,0],[-2.1,-.25,0],color=PURPLE,stroke_width=4),Line([-5.7,-.25,0],[-5.7,-.05,0],color=PURPLE,stroke_width=4),Line([-2.1,-.25,0],[-2.1,-.05,0],color=PURPLE,stroke_width=4))
        self.at('express track a'); self.play(trka.animate.set_stroke(PURPLE,width=6),FadeIn(brk),FadeIn(label('TrkA+\npain · temperature',[-3.9,-1.15,0],28,PURPLE)),run_time=.4)
        self.at('mostly small neurons'); self.play(trka.animate.set_fill(RED,.1),FadeIn(label('TrkA-negative',[-.3,-1.15,0],26,BLUE)),FadeIn(label('mostly spared',[4.6,-1.0,0],30,GREEN)),run_time=.5)
        self.play(*[c.animate.set_stroke(PURPLE,width=6,opacity=.9) for c in trka],run_time=.01)
        self.at('sense pain'); self.play(Indicate(VGroup(*small[:3]),color=PURPLE),run_time=.4); self.finish()

class S07Still(SpokenScene):
    def construct(self):
        self.add(evidence()); self.at('cannot say'); self.play(FadeIn(chip('Made versus lost? Unanswered.',TEAL,30).move_to([0,-2.6,0])),run_time=.4); self.finish()

class S08Fagan(SpokenScene):
    def construct(self):
        def snap(x,n,y=.3,k=1.0,r=.27):
            blob=Ellipse(width=3.7*k,height=2.5*k,color=BLUE,fill_color=BLUE,fill_opacity=.08).move_to([x,y,0])
            spots=[(-.9,.5),(0,.5),(.9,.5),(-.9,-.5),(0,-.5),(.9,-.5)]
            ds=VGroup(*[dot([x+a*k,y+b*k,0],r=r*k) if i<n else Circle(radius=r*k,stroke_color=GREY,stroke_width=2,stroke_opacity=.5).move_to([x+a*k,y+b*k,0]) for i,(a,b) in enumerate(spots)])
            return VGroup(blob,ds)
        single=snap(0,6,k=1.2)
        self.add(head('Fagan, Landis, Barbacid\nand colleagues · 1996'),single)
        cl=label('count neurons: 6',[0,-1.9,0],30,BLUE)
        self.at('counted one ganglion'); self.play(LaggedStart(*[Indicate(c,color=TEXT) for c in single[1]],lag_ratio=.12),FadeIn(cl),run_time=.9)
        snaps=VGroup(snap(-4.4,6),snap(0,5),snap(4.4,4))
        ages=VGroup(*[label(t,[x,-1.55,0],30) for x,t in [(-4.4,'E13.5'),(0,'E15.5'),(4.4,'Birth')]])
        cnt=VGroup(*[label(t,[x,-2.2,0],28,BLUE) for x,t in [(-4.4,'count: 6'),(0,'count: 5'),(4.4,'count: 4')]])
        note=label('schematic cartoon, not data',[0,-3.1,0],26,GREY)
        self.at('a series of ages',lead=.5); self.play(FadeOut(single),FadeOut(cl),FadeIn(snaps),FadeIn(ages),FadeIn(cnt),FadeIn(note),run_time=.7); self.finish()

class S09Scg(SpokenScene):
    def construct(self):
        m=mouse(1.0,[0,-.7,0]); mark=dot(m.neck,BLUE,.2)
        self.add(m)
        top=m.neck+np.array([-.6,2.3,0])
        call=VGroup(Line(m.neck+UP*.2,top+DOWN*.3,color=BLUE),label('superior cervical\nganglion',top+np.array([-1.9,.3,0]),28,BLUE))
        self.at('superior cervical ganglion'); self.play(FadeIn(mark),FadeIn(call),run_time=.5)
        self.at('top of the neck'); self.play(FadeOut(m),FadeOut(mark),FadeOut(call),run_time=.2)
        neck=VGroup(Line([-4,-2.7,0],[-2.7,2.2,0],color=GREY,stroke_width=7),Line([0,-2.7,0],[-1.3,2.2,0],color=GREY,stroke_width=7))
        big=Ellipse(width=1.2,height=2.2,color=BLUE,fill_color=BLUE,fill_opacity=.35).move_to([-.35,.9,0])
        self.play(FadeIn(neck),FadeIn(big),FadeIn(label('Neck · enlarged',[-2,-3.1,0],28,GREY)),Create(Line(big.get_right(),[2,.9,0],color=BLUE)),FadeIn(label('superior cervical\nganglion',[3.8,.9,0],30,BLUE)),run_time=.5); self.finish()

class S10Axes(SpokenScene):
    def construct(self):
        ax,labs=plot(); self.add(ax,labs[2])
        self.at('here are'); self.play(Create(ax),run_time=.5)
        self.at('neuron number'); self.play(FadeIn(VGroup(labs[0],*labs[3:])),run_time=.4)
        self.at('embryonic and postnatal'); self.play(FadeIn(labs[1]),FadeIn(age_labels(ax)),run_time=.4); self.finish()

class S11Predict(SpokenScene):
    def construct(self):
        ax,labs=plot(); self.add(ax,labs,age_labels(ax),normal(ax),endlabels(ax)[0])
        self.at('predict'); self.play(FadeIn(prediction()),run_time=.4); self.finish()

class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction_plot(),label('Think: relative to normal',[0,0,0],28,GREY)); self.wait(5)

class S13R1(SpokenScene):
    def construct(self):
        g=cluster(.25,.4); self.add(head('Without TrkA',PURPLE),g)
        ticks=VGroup(*[label(s,[x,-2.8,0],28,GREEN) for x,s in [(-4.2,'✓ Neurogenesis'),(0,'✓ Neuronal markers'),(4.2,'✓ Initial axon growth')]])
        self.at('neurogenesis'); self.play(FadeIn(ticks[0]),Indicate(g,color=TEAL),run_time=.4)
        markers=VGroup(*[dot(c.get_center()+UP*.09,TEAL,.09) for c in g])
        self.at('neuronal markers'); self.play(FadeIn(markers),FadeIn(ticks[1]),run_time=.4)
        axons=VGroup(*[Line(c.get_bottom(),c.get_bottom()+DOWN*.65+RIGHT*.3,color=BLUE,stroke_width=4) for c in g])
        self.at('initial axon growth'); self.play(Create(axons),FadeIn(ticks[2]),run_time=.5); self.finish()

class S14R2(SpokenScene):
    def construct(self):
        ax,labs=plot(); self.add(ax,labs,age_labels(ax),normal(ax),endlabels(ax)[0])
        pts=VGroup(dot(ax.c2p(13.5,1),GREEN,.14),Circle(radius=.23,color=PURPLE,stroke_width=4).move_to(ax.c2p(13.5,1)))
        self.at('the two counts match'); self.play(FadeIn(pts),FadeIn(label('same count',[-2.9,1.45,0],28,PURPLE)),run_time=.4)
        self.at('embryonic day'); self.play(FadeIn(age_tick(ax,13.5,'E13.5')),run_time=.4)
        self.at('ganglion forms'); self.play(Indicate(pts,scale_factor=1.3),run_time=.4); self.finish()

class S15R3(SpokenScene):
    def construct(self):
        ax,labs=plot(); self.add(ax,labs,age_labels(ax,True),normal(ax),endlabels(ax)[0])
        n,m=curves(ax,15.5)
        self.at('by embryonic'); self.play(FadeIn(age_tick(ax,15.5,'E15.5')),Create(m),run_time=.7)
        self.at('fewer neurons'); self.play(FadeIn(deficit(ax)),run_time=.4)
        _,mm=curves(ax)
        self.at('gap keeps growing'); self.play(Transform(m,mm),FadeIn(endlabels(ax)[1]),run_time=.8); self.finish()

class S16Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(complete_plot()); self.wait(4)

class S17Mean(SpokenScene):
    def construct(self):
        self.add(complete_plot()); a=meaning()
        self.at('then lost'); self.play(FadeIn(a[0]),run_time=.4)
        self.at('what failed'); self.play(FadeIn(VGroup(*a[1:])),run_time=.4); self.finish()

class S18Sig(SpokenScene):
    def construct(self):
        p,b=reasoning(); self.add(head('Why the curve matters'),p)
        self.at('signature evidence'); self.play(FadeIn(b),run_time=.5); self.finish()

class S19Single(SpokenScene):
    def construct(self):
        p,b=reasoning(); self.add(head('Why the curve matters'),p,b)
        # Schematic bars compare conditions; they are not numerical measurements.
        key=VGroup(label('Normal',[2.6,-2.2,0],26,GREEN),label('TrkA-null',[4.8,-2.2,0],26,PURPLE),label('schematic bars',[-5.0,-2.2,0],26,GREY))
        def bars(y,wa,wb):
            return VGroup(*[Rectangle(width=w,height=.24,color=c,fill_color=c,fill_opacity=1).move_to([x,y,0]) for x,c,w in [(2.6,GREEN,wa),(4.8,PURPLE,wb)]])
        dividing=bars(-2.75,1.2,1.2); dying=bars(-3.35,.45,1.3)
        dlabel=label('Dividing cells: same',[-2.5,-2.75,0],28); ylabel=label('Dying nuclei: more',[-2.5,-3.35,0],28,RED)
        self.at('counts of dividing'); self.play(FadeIn(key),FadeIn(dividing),FadeIn(dlabel),run_time=.5)
        self.at('more neurons were dying'); self.play(FadeIn(dying),FadeIn(ylabel),b[0].animate.set_opacity(.3),b[1].animate.set_opacity(.3),b[2].animate.set_color(RED),run_time=.5)
        self.at('division was normal'); self.play(Indicate(dividing,scale_factor=1.12),run_time=.5); self.finish()

class S20How(SpokenScene):
    def construct(self):
        cell,death,ngf,bar=brake(); self.add(head('Holding off death'),cell,ngf,death,bar)
        self.play(*held(death),run_time=.01)
        self.at('get too little'); self.play(*dimmed(ngf),FadeOut(bar),cell.animate.set_stroke(RED),run_time=.5)
        self.at('die by a death'); self.play(*live(death),cell.animate.set_fill(RED,.12),run_time=.5)
        self.at('needs the protein'); self.play(Indicate(death,scale_factor=1.1,color=RED),run_time=.6); self.finish()

class S21Bax(SpokenScene):
    def construct(self):
        e=evidence(True); self.add(*e[:5])
        self.at('keep sympathetic neurons'); self.play(FadeIn(VGroup(*e[5:])),run_time=.4)
        self.at('in culture'); self.play(FadeOut(e),run_time=.25)
        dishes=VGroup(*[Ellipse(width=5.5,height=3.5,color=GREY).move_to([x,-.2,0]) for x in [-3.05,3.05]])
        wt=VGroup(*[dot([x,y,0],r=.28) for x,y in [(-4,.4),(-2.2,.4),(-3.1,-.8)]])
        bx=VGroup(*[VGroup(dot([x,y,0],GREEN,.2),Line([x+.2,y,0],[x+.55,y+.1,0],color=GREEN,stroke_width=3)) for x,y in [(2.2,.4),(4,.4),(3.1,-.8)]])
        self.play(FadeIn(head('Survival after NGF withdrawal')),FadeIn(dishes),FadeIn(wt),FadeIn(bx),FadeIn(label('Wild type',[-3,2,0],30)),FadeIn(label('Bax-null',[3,2,0],30,RED)),run_time=.35)
        self.at('they survive'); self.play(Indicate(bx,color=GREEN),run_time=.3)
        self.at('is withdrawn'); self.play(FadeIn(chip('NGF withdrawn',YELLOW,28).move_to([0,-2.55,0])),wt.animate.set_opacity(.12),FadeIn(label('alive; small, short axons',[3,-3.25,0],28,GREEN)),run_time=.5); self.finish()

class S22Holds(SpokenScene):
    def construct(self):
        cell,death,ngf,bar=brake(); cell.set_stroke(RED).set_fill(RED,.12)
        cap=label('NGF holds back a Bax-dependent death program',[0,-3.2,0],30)
        self.add(head('Holding off death'),cell,death,ngf,cap)
        self.play(*dimmed(ngf),run_time=.01)
        self.at('ngf works'); self.play(*bright(ngf),Create(bar),cell.animate.set_stroke(GREEN).set_fill(BLUE,.08),run_time=.5)
        self.at('holding back'); self.play(*held(death),run_time=.5); self.finish()

class S23Take(SpokenScene):
    def construct(self):
        g=cluster(.4,.38); self.add(head('Without TrkA',PURPLE),g)
        self.at('are made'); self.play(FadeIn(label('Made',[0,2.3,0],32,TEAL)),run_time=.3)
        br=VGroup(Line([2.7,-.1,0],[2.7,-1.1,0],color=RED,stroke_width=4),Line([2.7,-.1,0],[2.55,-.1,0],color=RED,stroke_width=4),Line([2.7,-1.1,0],[2.55,-1.1,0],color=RED,stroke_width=4))
        self.at('then lost'); self.play(VGroup(*g[3:]).animate.set_opacity(.13).set_color(RED),FadeIn(br),FadeIn(label('Then lost',[4.2,-.6,0],32,RED)),run_time=.4)
        self.at('ngf acts'); self.play(FadeIn(label('NGF is a survival factor',[0,-2.45,0],32,YELLOW)),FadeIn(label('✓ Remove factor, more die',[0,-3.25,0],28,GREEN)),run_time=.35); self.finish()

class S24End(EndCard):
    LINE='Without TrkA: made, then lost. NGF keeps neurons alive.'
    def construct(self):
        self.add(label('Without TrkA: made, then lost.\nNGF keeps neurons alive.',[0,.3,0],40),label('biochemistrypedia.com',[0,-1.4,0],26,TEAL)); self.wait(self.narration_s)
