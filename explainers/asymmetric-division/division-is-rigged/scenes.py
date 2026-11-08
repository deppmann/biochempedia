"""Chapter 6 revision.
COLOR MAP: BLUE neuroblast / self-renewal; GREEN GMC / differentiating output;
RED mutant tissue / failure; YELLOW Numb; TEXT Prospero / Brat cargo;
GREY unknown cells / anatomy; TEAL Notch; GOLD timing / emphasis.
All model traces: N(r)=(1+f)**r; N(0)=1. Tissue cartoons are schematic.
"""
import numpy as np
from bp_style import *

# Preserve the pipeline's word cues without changing its sync.log artifact.
class SpokenScene(SpokenScene):
    def at(self, phrase, lead=.2, nth=0):
        rest=self.t_of(phrase,nth)-lead-self.elapsed()
        if rest>.02: self.wait(rest)

def cell(c,r,color=GREY,op=.17):
    return Circle(radius=r,stroke_color=color,stroke_width=4,fill_color=color,fill_opacity=op).move_to(c)
def arr(a,b,color=GREY,w=4):
    return Arrow(a,b,buff=0,color=color,stroke_width=w,tip_length=.2,max_tip_length_to_length_ratio=.35)
def label(s,x=0,y=0,size=30,color=TEXT):
    return T(s,size=size,color=color).move_to([x,y,0])
def head(s): return label(s,y=3.15,size=34)
def mass(x=0,y=0,r=.7):
    # A single continuous lobed tissue outline (no overlapping Venn circles).
    theta=np.linspace(0,2*PI,100)
    points=[[x+r*(1+.12*np.cos(5*q))*np.cos(q),y+r*(1+.12*np.cos(5*q))*np.sin(q),0] for q in theta]
    return Polygon(*points,color=RED,fill_color=RED,fill_opacity=.28,stroke_width=4)
def question():
    return VGroup(head('50 rounds: how many neuroblasts?'),
        label('round 0 → 50 · start with 1 neuroblast',0,2.3,28),
        chip('perfect sorting · f = 0',BLUE,size=28).move_to([-3.1,.9,0]),
        chip('1 in 10 leaks · f = 0.10',BLUE,size=28).move_to([3.1,.9,0]),
        label('?',-3.1,-.65,82,BLUE),label('?',3.1,-.65,82,BLUE))
def model_axes():
    ax=Axes(x_range=[0,50,10],y_range=[0,125,25],x_length=9.5,y_length=5.3,tips=False,
            axis_config={'color':GREY,'include_ticks':True}).move_to([.55,.05,0])
    labs=VGroup(label('rounds',.55,-3.12,26),
        label('average neuroblasts (start = 1)',-5.8,0,26).rotate(PI/2))
    for n in range(0,126,25): labs.add(T(str(n),size=26).next_to(ax.c2p(0,n),LEFT,buff=.16))
    for n in range(10,51,10): labs.add(T(str(n),size=26).next_to(ax.c2p(n,0),DOWN,buff=.12))
    return ax,labs

def host_set(dead=False):
    """Two host-tissue circles; when dead they are dimmed red and crossed out."""
    hosts=VGroup(cell([3.8,.9,0],.85),cell([3.8,-1.4,0],.85))
    crosses=VGroup()
    if dead:
        hosts.set_color(RED).set_fill(RED,.05).set_stroke(RED,width=3,opacity=.55)
        for c in hosts:
            o=c.get_center()
            crosses.add(VGroup(Line(o+[-.5,.5,0],o+[.5,-.5,0],color=RED,stroke_width=7),Line(o+[-.5,-.5,0],o+[.5,.5,0],color=RED,stroke_width=7)))
    names=VGroup(label('host dies' if dead else 'host tissue',3.8,2.1,27,RED if dead else TEXT),
                 label('host dies' if dead else 'host tissue',3.8,-2.6,27,RED if dead else TEXT))
    return hosts,names,crosses

def growth_reveal():
    hosts,names,crosses=host_set(True)
    return VGroup(head('Transplanted mutant brain tissue'),mass(-.8,-.1,1.7),
        mass(-4.8,1.2,.35).set_opacity(.45),label('start: 1×',-4.8,2,28),
        label('>100× starting size',-.8,2.3,32,RED),
        hosts,names,crosses,
        arr([1.15,.5,0],[2.8,.9,0],RED),arr([1.15,-.7,0],[2.8,-1.4,0],RED),
        label('size schematic · fold change shown numerically',0,-3.45,24))

def number_table():
    g=VGroup(head('Average neuroblasts · starting from 1'))
    xs=[-3.8,0,3.8]
    for x,s in zip(xs,['Leak fraction f','25 rounds','50 rounds']):
        g.add(label(s,x,2.15,26,GREY))
    for j,f in enumerate([0,.02,.05,.10,.20]):
        y=1.25-j*.75
        # Values computed directly; formatting follows the requested precision.
        vals=[f'{f:.2f}',f'{(1+f)**25:.1f}',f'{(1+f)**50:,.0f}' if f>=.1 else f'{(1+f)**50:.1f}']
        for x,s in zip(xs,vals):
            g.add(label(s,x,y,30,BLUE if f==.1 else TEXT))
    g.add(label('Illustrative model · single lineages vary',0,-3,24,GREY))
    return g


def clabel(txt,x,y,size=32,color=TEXT):
    """Centred multi-line label: every line is centred on the column (Text left-aligns its lines)."""
    lines=[T(t,size=size,color=color) for t in txt.split('\n')]
    g=VGroup(*lines).arrange(DOWN,buff=.1,aligned_edge=ORIGIN)
    return g.move_to([x,y,0])
def header(txt,x,y,size=32,color=GOLD):
    """Header text placed by baseline, so descenders (g, y) do not shift it."""
    t=T(txt,size=size,color=color)
    desc=T('gx',size=size).height-T('xx',size=size).height if any(c in txt for c in 'gjpqy') else 0
    return t.move_to([x,y,0]).shift(DOWN*desc/2)

def study_table(second=False):
    g=VGroup(head('Mouse studies · Numb + Numblike removed'))
    xs=[-4.75,-1.85,1.35,4.95]
    for x,txt in zip(xs,['Study','Where','When','Progenitors']): g.add(header(txt,x,2.1))
    rows=[['Petersen et al.\n2002','nervous\nsystem','early','used up']]
    if second: rows.append(['Li et al.\n2003','dorsal\nforebrain','from E9.5\n(later peak of\nneurogenesis)','over-\nproliferate'])
    for j,row in enumerate(rows):
        y=.7-j*2.45
        for k,(x,txt) in enumerate(zip(xs,row)): g.add(clabel(txt,x,y,32,RED if k==3 else TEXT))
    for y in [1.55,-.45,-3]: g.add(Line([-6.2,y,0],[6.2,y,0],color=GREY,stroke_opacity=.5))
    return g

class S00Title(TitleCard):
    LESSON='Asymmetric Division: Numb and the Neuroblast'
    TITLE='When the Division Is Rigged'
    def construct(self):
        # House title geometry, with a readable two-line lesson label.
        self.add(label('BIOCHEMISTRYPEDIA',0,2.1,24,TEAL))
        self.add(label('Asymmetric Division:\nNumb and the Neuroblast',0,1,26,GREY))
        self.play(FadeIn(label(self.TITLE,0,-.5,42)),run_time=.65)
        self.add(Line([-1,-1.3,0],[1,-1.3,0],color=GOLD,stroke_width=4))
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        self.add(head('What if cargo is not sorted?'))
        a=cell([-2,.1,0],1.55,BLUE);b=cell([2,.1,0],1.05,BLUE)
        dots=VGroup(Dot([-2.4,.5,0],color=YELLOW,radius=.14),Dot([2.3,.4,0],color=YELLOW,radius=.14),Dot([-1.5,-.4,0],color=TEXT,radius=.14),Dot([1.6,-.3,0],color=TEXT,radius=.14))
        self.add(a,b,dots,label('Numb',-4.8,.7,28,YELLOW),Line([-4,.7,0],[-2.6,.5,0],color=YELLOW),label('Prospero',4.8,-.6,28),Line([3.8,-.6,0],[1.8,-.3,0],color=TEXT))
        self.at('fails to sort')
        self.play(a.animate.shift(LEFT*.2),b.animate.shift(RIGHT*.2),run_time=.65)
        self.at('And why')
        self.play(FadeIn(label('Why can one small error grow so large?',0,-2.65,34)),run_time=.35)
        self.add(label('blue: neuroblast · green: GMC · red: mutant / overgrown',0,-3.4,22))
        self.finish()

class S02Cg(SpokenScene):
    def construct(self):
        self.add(label('2005',0,2.2,64,GOLD),label('Emmanuel Caussinus\nCayetano Gonzalez',0,.25,46),chip('Transplant test',GREY,size=36).move_to([0,-2.25,0]))
        self.at('ran a transplant');self.play(Indicate(self.mobjects[-1],color=GOLD),run_time=.5);self.finish()

def fly_outline(x=0,y=0,k=1.0):
    """One clean fly silhouette: abdomen, thorax, head and two wings merged into a single outline."""
    parts=[Ellipse(width=1.5,height=2.4).move_to([x,y-1.1,0]),
           Ellipse(width=1.5,height=1.5).move_to([x,y+.55,0]),
           Circle(radius=.5).move_to([x,y+1.7,0]),
           Ellipse(width=.95,height=3.1).rotate(.55).move_to([x-1.15,y-.05,0]),
           Ellipse(width=.95,height=3.1).rotate(-.55).move_to([x+1.15,y-.05,0])]
    out=Union(*parts,color=GREY,stroke_width=5,fill_color=GREY,fill_opacity=.1)
    return out.scale(k,about_point=[x,y,0])

class S03Tissue(SpokenScene):
    def construct(self):
        brain=mass(0,0,2.1)
        self.add(head('Mutant larval brain tissue'),brain)
        genes=[]
        for name,x,y in [('pins',-4.3,1.4),('miranda',4.3,1.4),('numb',-4.3,-1.3),('prospero',4.3,-1.3)]:
            genes.append(VGroup(chip(name+' loss',RED,size=28).move_to([x,y,0]),Line([x*.64,y,0],[np.sign(x)*2,y*.6,0],color=RED)))
        for cue,g in zip(['from pins','Miranda','numb','or prospero'],genes):
            self.at(cue);self.play(FadeIn(g),run_time=.2)
        self.at('mutants',lead=.1)
        fly=fly_outline(0,.05)
        cap=label('adult fly · transplant host',0,-2.95,32)
        self.play(*[FadeOut(g) for g in genes],FadeIn(fly),FadeIn(cap),brain.animate.scale(.24).move_to([0,-.95,0]),run_time=.9)
        self.add(label('mutant tissue',-3.7,-.95,28,RED),Line([-2.5,-.95,0],[-.55,-.95,0],color=RED))
        self.finish()

class S04Growth(SpokenScene):
    def construct(self):
        g=growth_reveal();tissue=mass(-.8,-.1,.35)
        hosts,names,_=host_set(False)
        _,dnames,crosses=host_set(True)
        arrows=VGroup(g[8],g[9])
        self.add(g[0],g[2],g[3],g[-1],tissue)
        n=ValueTracker(1);counter=always_redraw(lambda:label(f'{n.get_value():.0f}× starting size',-.8,2.3,32,RED));self.add(counter)
        self.at('tissue grew')
        self.play(Transform(tissue,g[1]),n.animate.set_value(100),run_time=2.2,rate_func=linear)
        self.remove(counter);self.add(g[4])
        self.at('invaded other tissues')
        self.play(FadeIn(hosts),FadeIn(names),FadeIn(arrows),run_time=.6)
        self.at('killed its hosts')
        self.play(hosts.animate.set_color(RED).set_fill(RED,.05).set_stroke(RED,width=3,opacity=.55),
                  FadeIn(crosses),Transform(names,dnames),run_time=.6);self.finish()
class S05Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(growth_reveal());self.wait(2)

class S06Bmk(SpokenScene):
    def construct(self):
        self.add(label('2006',0,2.4,62,GOLD),label('Jörg Betschinger\nKarl Mechtler\nJürgen Knoblich',0,.2,42),label('Brat + Prospero',0,-2.5,36))
        self.at('studied');self.play(Indicate(self.mobjects[-1],color=GOLD),run_time=.4);self.finish()

class S07Mutants(SpokenScene):
    def construct(self):
        self.add(head('brat or prospero mutants'))
        parent=cell([0,.4,0],1.5,BLUE);nblab=label('neuroblast',0,-1.5,30,BLUE);self.add(parent,nblab)
        self.at('both daughters')
        daughters=VGroup(cell([-2,.4,0],1.25,BLUE),cell([2,.4,0],1.25,BLUE))
        self.play(ReplacementTransform(parent,daughters),run_time=.6)
        self.at('grew like neuroblasts');self.play(daughters.animate.scale(1.1),run_time=.5)
        self.at('formed brain')
        self.play(ReplacementTransform(daughters,mass(0,.3,2.05)),FadeOut(nblab),FadeIn(label('brain tumour',0,-2.5,34,RED)),run_time=.7);self.finish()

class S08Brat(SpokenScene):
    def construct(self):
        self.add(head('Later work · type II lineage'))
        xs=[-4,0,4]
        normal=VGroup(*[cell([x,1.3,0],.65,c) for x,c in zip(xs,[BLUE,GREY,GREEN])],arr([-3.2,1.3,0],[-.8,1.3,0]),arr([.8,1.3,0],[3.2,1.3,0]))
        self.add(normal,label('neuroblast',-4,2.3,28,BLUE),label('intermediate progenitor',0,2.3,26),label('GMC',4,2.3,28,GREEN),label('normal maturation',0,.25,28))
        ip=cell([0,-1.5,0],.8,GREY)
        self.at('Later work')
        pulse=Dot([-4,1.3,0],radius=.13,color=GOLD);self.add(pulse)
        self.play(pulse.animate.move_to([0,1.3,0]),run_time=.5)
        self.play(pulse.animate.move_to([4,1.3,0]),run_time=.5);self.remove(pulse)
        self.at('Brat');self.play(FadeIn(label('Brat loss',-4,-1.5,32,RED)),FadeIn(ip),run_time=.4)
        self.at('intermediate progenitors');self.play(FadeIn(label('immature progenitor',0,-2.8,27)),run_time=.3)
        self.at('fail to mature')
        self.play(ip.animate.set_color(BLUE).set_fill(BLUE,.25),GrowArrow(arr([1,-1.5,0],[2.5,-1.5,0],RED)),FadeIn(label('neuroblast\nidentity',4,-1.5,30,BLUE)),run_time=.6)
        self.finish()

class S09Pros(SpokenScene):
    def construct(self):
        self.add(head('Prospero loss · type I lineage'),label('neuroblast → GMC',-3.7,2.25,32),cell([-5.3,0,0],.85,BLUE),label('neuroblast',-5.3,-1.3,26,BLUE),arr([-4.3,0,0],[-3.5,0,0]))
        g=cell([-2.7,0,0],.7,GREEN);self.add(g,clabel('ganglion\nmother cell',-2.7,-1.6,28,GREEN))
        self.at('arise from')
        clones=VGroup(cell([-.3,.85,0],.5,GREEN),cell([-.3,-.85,0],.5,GREEN))
        ar1=VGroup(arr([-1.9,.25,0],[-.95,.7,0],GREEN,3),arr([-1.9,-.25,0],[-.95,-.7,0],GREEN,3))
        self.play(TransformFromCopy(g,clones),FadeIn(ar1),run_time=.45)
        self.at('ganglion',lead=.1)
        more=VGroup(*[cell([2.0,y,0],.38,GREEN) for y in [1.45,.5,-.5,-1.45]])
        ar2=VGroup(*[arr([.3,sy*.85,0],[1.5,y,0],GREEN,3) for sy,ys in [(1,[1.45,.5]),(-1,[-.5,-1.45])] for y in ys])
        self.play(TransformFromCopy(clones,more),FadeIn(ar2),FadeIn(label('keeps dividing',1.1,-2.75,30,RED)),run_time=.45)
        self.at('cells',lead=.1)
        self.play(FadeIn(mass(5.2,0,1.25)),FadeIn(label('tumour',5.2,-1.85,30,RED)),run_time=.45);self.finish()

class S10Why(SpokenScene):
    def construct(self):
        self.add(label('A small leak at every division',0,2,38),arr([0,1.2,0],[0,.2,0],BLUE),label('more than 100-fold?',0,-.6,46,BLUE),label('Illustrative model\nnot a measurement',0,-2.5,36,GOLD))
        self.at('grow');self.play(Indicate(self.mobjects[2],color=BLUE),run_time=.4);self.finish()

class S11Model(SpokenScene):
    def construct(self):
        nb=cell([-3.9,.2,0],1.6,BLUE);counter=label('round 0',-3.9,2.35,32,GOLD)
        self.add(head('Perfect sorting'),nb,counter,label('neuroblast',-3.9,-1.85,30,BLUE),label('Nothing dies or stops.',0,-3.2,28))
        self.at('divides once per round');self.play(nb.animate.stretch(1.15,0),run_time=.4);self.play(nb.animate.stretch(1/1.15,0),run_time=.4)
        self.at('each small daughter')
        outputs=[]
        for i in range(3):
            daughter=cell([-1.0,.2,0],.75,GREEN)
            self.play(*[c.animate.shift(RIGHT*2.8) for c in outputs],
                      TransformFromCopy(nb,daughter),
                      Transform(counter,label(f'round {i+1}',-3.9,2.35,32,GOLD)),run_time=.4)
            outputs.append(daughter)
        self.at('ganglion mother cell');self.play(FadeIn(label('GMC output · one per round',1.8,-1.3,28,GREEN)),run_time=.3);self.finish()

class S12Leak(SpokenScene):
    def construct(self):
        a=cell([-3.8,.3,0],1.4,BLUE);b=cell([3.9,.3,0],.95,GREY)
        counter=label('round 1',0,2.45,30,GOLD)
        leftlab=label('neuroblast',-3.8,2.3,28,BLUE);rightlab=label('small daughter',3.9,2.3,28)
        chance=chip('chance f',GOLD,size=30).move_to([0,.3,0])
        self.add(head('Leaky sorting'),a,b,counter,leftlab,rightlab,label('Nothing dies or stops.',0,-3.25,28))
        self.at('has a chance');self.play(FadeIn(chance),run_time=.3)
        self.at('staying a neuroblast');self.play(b.animate.set_color(BLUE).set_fill(BLUE,.25),run_time=.5)
        self.at('Every neuroblast divides')
        kids=VGroup(cell([-1.1,.3,0],.85,GREEN),cell([4.3,.3,0],.85,GREEN))
        self.play(Transform(a,cell([-3.8,.3,0],1.4,BLUE)),Transform(b,cell([1.6,.3,0],1.4,BLUE)),TransformFromCopy(a,kids[0]),TransformFromCopy(b,kids[1]),FadeOut(chance),FadeOut(leftlab),FadeOut(rightlab),Transform(counter,label('round 2',0,2.45,30,GOLD)),run_time=.8)
        self.add(label('neuroblast',-3.8,-1.5,26,BLUE),label('GMC',-1.1,-1.5,26,GREEN),label('neuroblast',1.6,-1.5,26,BLUE),label('GMC',4.3,-1.5,26,GREEN))
        self.add(label('Every neuroblast divides in the next round',0,-2.6,30))
        self.finish()

class S13Predict(SpokenScene):
    def construct(self):
        q=question();self.add(q[0],q[1],cell([-3.1,-.65,0],.65,BLUE),cell([3.1,-.65,0],.65,BLUE))
        self.at('with perfect sorting');self.play(FadeIn(q[2]),FadeIn(q[4]),run_time=.22)
        self.at('How many if');self.play(FadeIn(q[3]),FadeIn(q[5]),run_time=.22);self.finish()
class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(question())
        ring=Circle(radius=.6,color=GOLD).move_to([0,-2.4,0]);self.add(ring)
        for n in range(5,0,-1):
            num=label(str(n),0,-2.4,44,GOLD);self.add(num);self.wait(1);self.remove(num)

class S15Perfect(SpokenScene):
    def construct(self):
        self.add(head('Perfect sorting · f = 0'))
        L=-4.9
        top=Axes(x_range=[0,50,25],y_range=[0,2,1],x_length=10.6,y_length=1.55,tips=False,axis_config={'color':GREY}).move_to([0,0,0]).move_to([L+5.3,1.4,0],aligned_edge=ORIGIN)
        bot=Axes(x_range=[0,50,25],y_range=[0,100,50],x_length=10.6,y_length=2.3,tips=False,axis_config={'color':GREY}).move_to([L+5.3,-1.45,0])
        self.add(top,bot,label('neuroblasts',L,2.65,28,BLUE).align_to([L,0,0],LEFT),label('cumulative neurons or glia*',L,.2,28,GREEN).align_to([L,0,0],LEFT))
        for n in [0,1,2]:self.add(T(str(n),size=26).next_to(top.c2p(0,n),LEFT,buff=.2))
        for n in [0,50,100]:self.add(T(str(n),size=26).next_to(bot.c2p(0,n),LEFT,buff=.2))
        for n in [0,25,50]:self.add(T(str(n),size=26).next_to(bot.c2p(n,0),DOWN,buff=.15))
        self.add(label('rounds',L+5.3,-3.45,26))
        self.at('still');self.play(Create(top.plot(lambda r:1,x_range=[0,50],color=BLUE,stroke_width=6)),FadeIn(label('1 neuroblast, round 0 to 50',L+5.3,2.05,28,BLUE).shift(RIGHT*0)),run_time=.6)
        self.at('output just adds up')
        self.play(Create(bot.plot(lambda r:2*r,x_range=[0,50],color=GREEN)),FadeIn(label('50 GMCs → 100 neurons or glia',L+3.1,-.55,28,GREEN)),run_time=1.2)
        self.add(Dot(bot.c2p(50,100),color=GREEN,radius=.09),label('*each GMC divides once, all survive',L+3.0,-1.05,24));self.finish()

class S16Leaky(SpokenScene):
    def construct(self):
        ax,labs=model_axes();self.add(ax,labs)
        self.add(label('f = 0.10 · average × (1 + f) each round',0,3.2,30,BLUE))
        worked=label('1 → 1.10 → 1.21 → …',0,2.45,28,BLUE);self.add(worked)
        flat=ax.plot(lambda r:1,x_range=[0,50],color=GREEN);self.add(flat,label('f = 0: 1',3.6,-2.15,26,GREEN))
        self.at('neuroblasts multiply')
        tracker=ValueTracker(0)
        curve=always_redraw(lambda:ax.plot(lambda r:1.1**r,x_range=[0,max(.01,int(tracker.get_value()))],color=BLUE))
        dot=always_redraw(lambda:Dot(ax.c2p(int(tracker.get_value()),1.1**int(tracker.get_value())),color=BLUE,radius=.07))
        counter=always_redraw(lambda:T(f'{1.1**int(tracker.get_value()):.1f}',size=28,color=BLUE).next_to(ax.c2p(int(tracker.get_value()),1.1**int(tracker.get_value())),UP,buff=.2))
        self.add(curve,dot,counter)
        self.play(tracker.animate.set_value(20),run_time=2.4,rate_func=linear)
        self.at('The count compounds');self.play(FadeOut(worked),tracker.animate.set_value(50),run_time=1.55,rate_func=linear)
        self.remove(counter);self.add(T('117',size=32,color=BLUE).next_to(ax.c2p(50,1.1**50),LEFT,buff=.2));self.finish()

class S17Numbers(SpokenScene):
    def construct(self):
        table=number_table();self.add(table);self.at('the average passes');self.play(Indicate(VGroup(*table[13:16]),color=BLUE),run_time=.65);self.finish()
class S18Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(number_table());self.wait(2.5)
class S19Caveat(SpokenScene):
    def construct(self):
        self.add(head('What the model can say'))
        first=label('Illustrative round counts',0,1.7,36);self.add(first)
        self.at('not measured');self.play(Transform(first,label('Illustrative, not measured',0,1.7,36)),run_time=.3)
        self.at('The model counts');self.play(FadeIn(label('Counts neuroblasts, not tissue size',0,-.8,36)),run_time=.3)
        self.at('not a fit');self.play(FadeIn(label('Not a fit to the transplant data',0,-2.5,36,GOLD)),run_time=.3);self.finish()
class S20Point(SpokenScene):
    def construct(self):
        ax,labs=model_axes();self.add(ax,labs,label('Illustrative model · f = 0.10',0,3.2,32,GOLD))
        self.at('small leak');self.play(Create(ax.plot(lambda r:1.1**r,x_range=[0,50],color=BLUE)),run_time=1.3)
        self.at('compounded');self.play(Indicate(ax,color=BLUE,scale_factor=1),run_time=.5)
        self.at('more than')
        cross=np.log(100)/np.log(1.1)
        self.play(Create(DashedLine(ax.c2p(0,100),ax.c2p(50,100),color=RED,stroke_width=4)),FadeIn(Dot(ax.c2p(cross,100),radius=.13,color=GOLD)),FadeIn(label('100×',-3.5,1.9,30,RED)),FadeIn(label('about round 49',2,2.45,28,GOLD)),Create(Line([3.7,2.25,0],ax.c2p(cross,100),color=GOLD)),run_time=.5);self.finish()

class S21Mammals(SpokenScene):
    def construct(self):
        self.add(head('Mouse embryo cortex · schematic'))
        wall=RoundedRectangle(width=9,height=4.7,corner_radius=.3,color=GREY,fill_color=GREY,fill_opacity=.09).move_to([0,-.1,0])
        self.add(wall,label('pial surface',0,2.5,28),label('ventricular zone',0,-2.95,30))
        for x in [-3,-1,1,3]:self.add(Line([x,-1.25,0],[x+.2,1.75,0],color=GREY),cell([x,-1.65,0],.38,GREY))
        numb=chip('Numb',YELLOW,size=30).move_to([-1.7,-.55,0]);numb[0].set_fill(BG,opacity=1)
        like=chip('Numblike',YELLOW,size=30).move_to([1.7,-.55,0]);like[0].set_fill(BG,opacity=1)
        self.at('Mice have');self.play(FadeIn(numb),Create(Line([-1.7,-.9,0],[-1,-1.3,0],color=YELLOW)),run_time=.3)
        self.at('second relative');self.play(FadeIn(like),Create(Line([1.7,-.9,0],[1,-1.3,0],color=YELLOW)),run_time=.3);self.finish()
class S22Early(SpokenScene):
    def construct(self):
        tab=study_table();self.add(*tab[:8],*tab[9:]);self.at('used up progenitors');self.play(FadeIn(tab[8]),run_time=.35);self.finish()
class S23Later(SpokenScene):
    def construct(self):
        tab=study_table(True);self.add(*tab[:9],*tab[13:]);self.at('dorsal forebrain');self.play(FadeIn(VGroup(*tab[9:11])),run_time=.35)
        self.at('studied across');self.play(FadeIn(tab[11]),run_time=.35)
        self.at('made progenitors');self.play(FadeIn(tab[12]),run_time=.35);self.finish()
class S23bDiffer(SpokenScene):
    def construct(self):
        self.add(study_table(True));self.at('where and when');self.play(Create(RoundedRectangle(width=6.1,height=5.4,corner_radius=.2,color=GOLD).move_to([.02,-.3,0])),run_time=.4)
        self.at('not settled');self.play(FadeIn(label('Which difference matters?',0,-3.4,28,GOLD)),run_time=.3);self.finish()

class S24Other(SpokenScene):
    def construct(self):
        self.add(head('Numb has other jobs'))
        a=cell([-4.3,.4,0],1);b=cell([-2.1,.4,0],1)
        junction=VGroup(a,b,Line([-3.2,-.15,0],[-3.2,.95,0],color=YELLOW,stroke_width=9),label('junctions',-3.2,-1.1,30),label('between progenitors',-3.2,-1.85,26))
        membrane=VMobject(color=GREY,stroke_width=5).set_points_smoothly([[.8,1.2,0],[2,1.2,0],[2.2,.9,0],[2.15,.1,0],[3,-.3,0],[3.85,.1,0],[3.8,.9,0],[4,1.2,0],[5.2,1.2,0]])
        ves=cell([3,.2,0],.48,YELLOW)
        endo=VGroup(membrane,ves,label('endocytosis',3,-1.85,30))
        self.add(junction,endo)
        self.at('other jobs');self.play(ves.animate.move_to([3,-.8,0]),run_time=.65)
        self.at('not automatically');self.play(FadeIn(label('Mouse phenotype ≠ automatic Notch veto',0,-3.1,30,TEAL)),run_time=.3);self.finish()

class S25Onward(SpokenScene):
    def construct(self):
        self.add(head('Which neuron type?'))
        g=cell([0,-.9,0],1.7,GREEN);lab=label('GMC',0,-2.9,30,GREEN);self.add(g,lab)
        a=cell([-2.3,-1.0,0],1.1,GREEN);b=cell([2.3,-1.0,0],1.1,GREEN)
        self.at('makes two sisters different');self.play(ReplacementTransform(g,VGroup(a,b)),FadeOut(lab),run_time=.6)
        self.add(chip('Numb',YELLOW,size=26).move_to([-2.3,-1.0,0]),label('no Numb',2.3,-1.0,24,GREY),label('?',-2.3,-2.8,60),label('?',2.3,-2.8,60))
        self.at('which of many neuron types')
        tags=VGroup(*[chip('type '+c,TEXT,size=26).move_to([x,y,0]) for c,x,y in [('A',-2.2,2.15),('B',0,2.15),('C',2.2,2.15),('D',-2.2,1.3),('E',0,1.3),('F',2.2,1.3)]])
        lines=VGroup(*[DashedLine([sx*.9,.95,0],[sx*2.0,.2,0],color=GREY,stroke_opacity=.95,stroke_width=4,dash_length=.14,dashed_ratio=.6) for sx in (-1,1)])
        self.play(FadeIn(tags),FadeIn(lines),run_time=.4);self.finish()
class S26Birth(SpokenScene):
    def construct(self):
        cells=VGroup(*[cell([x,.7,0],.85,GREEN) for x in [-3,0,3]])
        self.add(head('Which neuron type?'),cells,arr([-4.7,-1,0],[4.7,-1,0],GOLD),label('time of birth',0,-1.65,32,GOLD),label('early',-4.5,-1.65,28),label('late',4.5,-1.65,28))
        for x in [-3,0,3]:self.add(label('born',x,1.95,28))
        self.at('when a cell was born');self.play(Indicate(cells,color=GOLD),run_time=.4)
        self.at('next lesson');self.play(FadeIn(label('Next lesson: birth order and fate',0,-2.9,34,TEAL)),run_time=.3);self.finish()

TAKEAWAY='A rigged division leaks self-renewal\ninto the wrong daughter.\nCompounded, a small leak can multiply\nthe dividing cells.'
class S27Takeaway(SpokenScene):
    def construct(self):
        self.add(head('Sorting failure leaks self-renewal'))
        a=cell([-4.5,0,0],1.6,BLUE);b=cell([-1.2,0,0],1.05,GREY)
        daughter_label=label('wrong daughter',-1.2,1.55,28);self.add(a,b,daughter_label,label('neuroblast',-4.5,-1.95,30,BLUE))
        self.at('leaks');self.play(b.animate.set_color(BLUE).set_fill(BLUE,.25),run_time=.45)
        self.at('Compounded')
        kids=VGroup(cell([1.9,0,0],.58,BLUE),cell([3.2,0,0],.58,BLUE))
        arrow=arr([.05,0,0],[1.1,0,0],BLUE);again=label('divides again',2.6,.95,26,BLUE)
        self.play(TransformFromCopy(b,kids),FadeOut(daughter_label),GrowArrow(arrow),FadeIn(again),run_time=.5)
        self.at('multiply')
        many=VGroup(*[cell([x,0,0],.58,BLUE) for x in [1.9,3.2,4.5,5.8]])
        self.play(ReplacementTransform(kids,many),FadeIn(label('A small leak can multiply the dividing cells.',0,-2.7,36,BLUE)),run_time=.5)
        self.add(label('Illustrative model · neuroblast count, not tissue size',0,-3.4,24,GOLD));self.finish()
class S28End(EndCard):
    LINE=TAKEAWAY
    def construct(self):
        self.add(label(self.LINE,0,.3,36),label('biochemistrypedia.com',0,-2.7,26,TEAL));self.wait(8.5);self.finish()
