"""Chapter 1. COLOR MAP inherited from scenes.old.py:
BLUE receptors / taste identity; YELLOW ATP; TEAL CALHM1 / slow activation;
PURPLE CALHM3 / fast activation; GREEN fibre / approach; RED absent / aversion;
GREY outlines / membranes / axes. Taste tags: sweet BLUE, bitter RED,
umami PURPLE, sour GOLD, salty GREY. Shared map is kept here because TASK
also restricts editable existing files to scenes.py (CHAPTERS.md untouched).
Plots reuse 1-exp(-t/tau) from the reference and lesson; pulse is the lesson's
illustrative square voltage step, not a recorded action potential.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
TASTES = [('sweet', BLUE), ('bitter', RED), ('sour', GOLD), ('salty', GREY), ('umami', PURPLE)]

def label(s, p, size=28, color=TEXT):
    return T(s, size, color).move_to([*p, 0])

def heading(s):
    return label(s, (0, 3.05), 34)

def card(title, lines, color=BLUE, pos=(0, 0), width=5.2, height=4):
    box = RoundedRectangle(width=width, height=height, corner_radius=.22,
                           stroke_color=color, fill_color=color, fill_opacity=.07)
    txt = VGroup(T(title, 32, color), *[T(s, 26) for s in lines]).arrange(DOWN, buff=.3)
    txt.move_to(box)
    return VGroup(box, txt).move_to([*pos, 0])

def mouse(pos=(-2, -1), scale=1):
    body = Ellipse(width=3, height=1.65, color=GREY, fill_color=GREY, fill_opacity=.3)
    head = Circle(radius=.68, color=GREY, fill_color=BG, fill_opacity=1).move_to([1.3,.3,0])
    ear = Circle(radius=.34, color=GREY, fill_color=GREY, fill_opacity=.3).move_to([.95,.95,0])
    nose = Dot([1.99,.25,0], radius=.09, color=TEXT)
    eye = Dot([1.5,.5,0], radius=.065, color=TEXT)
    tail = ArcBetweenPoints([-1.4,-.1,0],[-2.5,.5,0],angle=-.8,color=GREY)
    feet = VGroup(Line([-.7,-.7,0],[-.4,-.95,0],color=GREY),Line([.6,-.7,0],[.9,-.95,0],color=GREY))
    return VGroup(tail,body,head,ear,nose,eye,feet).scale(scale).move_to([*pos,0])

def spout(pos=(3, -1)):
    pipe = VMobject(color=GREY, stroke_width=9).set_points_as_corners([[4,2,0],[4,-.4,0],[3,-.8,0]])
    drop = Dot([3,-1.02,0], color=BLUE, radius=.13)
    return VGroup(pipe,drop).shift(np.array([pos[0]-3,pos[1]+1,0]))

def questions():
    return VGroup(T('One signal or two?',46),T('Where can they be pulled apart?',32,GREY)).arrange(DOWN,buff=.75)


def rig(pos=(-1.3,-1.15), scale=1.35):
    m=mouse(pos,scale)
    nose=m[4].get_center(); tip=nose+RIGHT*.32
    pipe=VMobject(color=GREY,stroke_width=10).set_points_as_corners([tip+RIGHT*(.75*scale)+UP*(1.5*scale),tip+RIGHT*(.75*scale)+UP*(.5*scale),tip+UP*.15])
    drop=Dot(tip,radius=.12,color=BLUE)
    return m,VGroup(pipe,drop),Line(nose,tip,color=RED,stroke_width=6)

def bud():
    outline=Ellipse(width=7.1,height=4.8,color=GREY,fill_color=GREY,fill_opacity=.04).move_to([-.8,.15,0])
    cells=VGroup(*[Ellipse(width=1.1,height=3.6,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([x,.2,0]) for x in [-2.9,-1.5,-.1,1.3]])
    # Basal branches visibly terminate on every cell.
    fibre=VGroup(Line([-3.7,-2.3,0],[4.7,-2.3,0],color=GREEN,stroke_width=10),*[Line([x,-2.3,0],[x,-1.6,0],color=GREEN,stroke_width=7) for x in [-2.9,-1.5,-.1,1.3]])
    return VGroup(outline,cells,fibre)

def fibre_label(): return label('nerve fibre',(3.6,-2.85),26,GREEN)

def kinetics(short=False):
    end=30 if short else 1500
    ax=Axes(x_range=[0,end,10 if short else 500],y_range=[0,1,.5],x_length=10.8,y_length=4.8,axis_config={'color':GREY,'include_tip':False,'include_ticks':False}).move_to([.3,-.1,0])
    ticks=VGroup(*[M(str(v),26,GREY).next_to(ax.c2p(v,0),DOWN,buff=.12) for v in ([0,10,20,30] if short else [0,500,1000,1500])])
    yt=VGroup(*[M(str(v),26,GREY).next_to(ax.c2p(0,v),LEFT,buff=.15) for v in [0,.5,1]])
    labs=VGroup(ticks,label('time (ms)',(.3,-3.15),26,GREY),label('relative gate opening',(-6.15,0),26,GREY).rotate(PI/2),label('cultured cells · illustrative',(2,-3.58),26,GREY),yt)
    slow=ax.plot(lambda t:1-np.exp(-t/500),x_range=[0,end,end/300],color=TEAL,stroke_width=6,use_smoothing=False)
    return ax,labs,slow

def pulse(ax):
    a=ax.c2p(0,1.08); b=ax.c2p(5,1.08); end=ax.c2p(30,1.08)
    square=VMobject(color=GREY,stroke_width=4).set_points_as_corners([a,a+UP*.25,b+UP*.25,b,end])
    return VGroup(square,label('5 ms spike · illustrative step',(2.5,3.05),26,GREY))

def short_base(question=True):
    ax,l,c=kinetics(True)
    dot=Dot(ax.c2p(5,1-np.exp(-5/500)),radius=.09,color=YELLOW)
    read=label('about 1% open',(-1.8,-1.4),28,YELLOW)
    leader=Line(read.get_bottom(),dot.get_center()+UP*.12,color=YELLOW)
    name=label('CALHM1 alone',(3.1,-1.65),26,TEAL)
    scale=label('note the scale: 0–30 ms',(2.2,2.4),26,GOLD)
    g=VGroup(ax,l,c,pulse(ax),dot,read,leader,name,scale,Line(name.get_bottom(),ax.c2p(25,1-np.exp(-25/500))+UP*.08,color=TEAL))
    if question:g.add(label('Can a gate that slow keep up?',(0,3.58),30))
    return ax,g,dot

def closed_gap(fraction):
    # Slowly extend a bracket over the un-opened fraction during the question.
    start=np.array([.3,1.65,0]);end=start+RIGHT*(4.4*fraction)
    return VGroup(Line(start,end,color=YELLOW,stroke_width=4),
                  Line(start+DOWN*.15,start,color=YELLOW),
                  Line(end+DOWN*.15,end,color=YELLOW))

def gap_caption():
    return label('At 5 ms: ~99% still closed',(2.5,1.05),26,YELLOW)

def tested_route():
    return label('route tested here',(5.35,-.3),22,GREY)

def marker(ax,t,tau,color):
    pt=ax.c2p(t,1-np.exp(-t/tau))
    return VGroup(DashedLine(ax.c2p(t,0),pt,color=color),Dot(pt,color=color,radius=.09))

def pathway():
    specs=[('front of\ntongue',(-4.8,-2.6)),('geniculate\nganglion',(-4.8,-.7)),('solitary\nnucleus',(-4.8,1.4)),('parabrachial\nnucleus',(-1.6,1.4)),('gustatory\nthalamus',(1.65,1.4)),('insular\ncortex',(4.8,1.4)),('amygdala',(4.8,-1.1)),('hypothalamus',(-.1,-2.65))]
    nodes=VGroup(*[chip(s,GREY,size=26,pad=.2).move_to([*p,0]) for s,p in specs])
    tongue=VMobject(color=RED,fill_color=RED,fill_opacity=.18).set_points_smoothly([[-5.65,-2.1,0],[-5.7,-2.9,0],[-4.8,-3.2,0],[-3.9,-2.9,0],[-3.95,-2.1,0]])
    nodes[0][0].become(tongue)
    edges=VGroup()
    for k,(a,b) in enumerate([(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(3,6),(3,7)]):
        delta=nodes[b].get_center()-nodes[a].get_center();pa=nodes[a].get_boundary_point(delta);pb=nodes[b].get_boundary_point(-delta)
        ar=Arrow(pa,pb,buff=.13,color=PURPLE if k>=6 else GREY,stroke_width=3,tip_length=.16,max_tip_length_to_length_ratio=1)
        if k>=6: ar=VGroup(DashedLine(ar.get_start(),ar.get_end(),color=PURPLE),ar.get_tip())
        edges.add(ar)
    return nodes,edges

def dim_relay(n):
    target=n.copy().set_opacity(.5)
    target[0].set_fill(opacity=.05)
    return Transform(n,target)

def reveal_node(n):
    target=n.copy().set_opacity(1)
    target[0].set_fill(opacity=.12)
    return Transform(n,target)

def pathway_labels():
    return VGroup(label('rodents',(0,3.35),30),Line([-6.1,2.2,0],[-.25,2.2,0],color=GREY),label('brainstem',(-3.2,2.6),26,GREY),label('side branches',(1,-.55),26,PURPLE))

def cortex():
    outer=Ellipse(width=6.3,height=1.7,color=GREY,fill_color=GREY,fill_opacity=.07).move_to([0,2,0])
    sweet=chip('sweet field',BLUE,28).move_to([-1.45,2,0])
    bitter=chip('bitter field',GREY,28,fill_opacity=.03).move_to([1.45,2,0]).set_opacity(.5)
    return VGroup(outer,sweet,bitter)

def readouts():
    return VGroup(card('Recognition',['trained task'],BLUE,(-3.3,-1.6),5.4,2.1),card('Attraction',['licking'],GREEN,(3.3,-1.6),5.4,2.1))

def assay():
    c=cortex();r=readouts()
    a=chip('amygdala',PURPLE,28).move_to([3.3,.45,0])
    links=VGroup(Arrow(c[1].get_bottom(),r[0].get_top(),buff=.1,color=BLUE,tip_length=.17),Arrow(c[1].get_right(),a.get_left(),buff=.12,color=GREEN,tip_length=.17),Arrow(a.get_bottom(),r[1].get_top(),buff=.1,color=GREEN,tip_length=.17))
    drive=VGroup(Arrow([-4.7,2,0],[-2.9,2,0],buff=.08,color=BLUE),label('drive',(-4.1,2.5),26,BLUE))
    return c,r,a,links,drive

def silence(a):
    return VGroup(Cross(a[0],stroke_color=RED,stroke_width=6),label('silenced',(3.3,1.15),26,RED))

class S00Title(TitleCard):
    TITLE='Which Taste, and How Good?'
    LESSON='Taste from Tongue to Cortex'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28,GREY),T(self.TITLE,48,font=TITLE_FONT),Line(LEFT,RIGHT,color=GOLD)).arrange(DOWN,buff=.45)
        self.play(FadeIn(g),run_time=.5);self.finish()

class S01Q(SpokenScene):
    def construct(self):
        m,s,t=rig();count=label('Licks  0',(3,-2.75),32);self.add(m,s,count)
        self.at('mouse licks')
        for n in range(1,5):
            self.play(FadeIn(t),Transform(count,label(f'Licks  {n}',(3,-2.75),32)),run_time=.2);self.play(FadeOut(t),run_time=.2)
        self.at('what has');self.play(FadeIn(label('?',(-1.5,2),70)),run_time=.4);self.finish()

class S02Two(SpokenScene):
    def construct(self):
        m,s,t=rig(pos=(-1.4,-1.65),scale=1.15);self.add(m,s)
        left=card('Which taste?',[],BLUE,(-3,1.7),5,1.65);right=card('How much does\nit want it?',[],GREEN,(2.8,1.7),5.6,1.65)
        tails=VGroup(Polygon([-2,1,0],[-1.6,.45,0],[-1.3,1,0],color=BLUE,fill_color=BG,fill_opacity=1),Polygon([1,1,0],[.3,.4,0],[1.7,1,0],color=GREEN,fill_color=BG,fill_opacity=1))
        self.at('two questions');self.play(FadeIn(label('Two questions',(0,3.25),34)),run_time=.35)
        self.at('which taste');self.play(FadeIn(left),FadeIn(tails[0]),run_time=.4)
        self.at('how much');self.play(FadeIn(right),FadeIn(tails[1]),run_time=.4);self.finish()

class S03Question(SpokenScene):
    def construct(self):
        q=questions();self.add(q[0]);self.at('where can');self.play(FadeIn(q[1]),run_time=.5);self.finish()

class S04Identity(SpokenScene):
    def construct(self):
        c=card('Identity',[],BLUE,(0,.25),10,4.4);c[1].move_to([0,1.8,0]);self.add(c)
        tags=VGroup(*[chip(n,col,36).move_to([x,y,0]) for (n,col),(x,y) in zip(TASTES,[(-3,.6),(0,.6),(3,.6),(-1.5,-1.1),(1.5,-1.1)])])
        self.play(FadeIn(tags),run_time=.35);self.finish()

class S05Value(SpokenScene):
    def construct(self):
        c=card('Value',[],GREEN,(0,.15),10,4.5);c[1].move_to([0,1.85,0]);self.add(c)
        toward=Arrow([-4,.3,0],[-.8,.3,0],color=GREEN,buff=0,stroke_width=4);away=Arrow([.8,.3,0],[4,.3,0],color=RED,buff=0,stroke_width=4)
        self.at('value');self.play(GrowArrow(toward),FadeIn(label('attraction',(-2.5,1),32,GREEN)),run_time=.4)
        self.at('turns away');self.play(GrowArrow(away),FadeIn(label('aversion',(2.5,1),32,RED)),run_time=.4)
        self.at('how strongly');self.play(toward.animate.set_stroke(width=13),FadeIn(label('weak → strong',(0,-.5),28)),FadeIn(label('Valence: appetitive / aversive',(0,-1.6),30)),run_time=.5);self.finish()

class S06Cells(SpokenScene):
    def construct(self):
        b=bud();self.add(b[0],b[1],heading('Taste cells are not neurons'))
        self.at('hand their news');self.play(Create(b[2]),FadeIn(fibre_label()),run_time=.6);self.finish()

class S07Type2(SpokenScene):
    def construct(self):
        b=bud();self.add(b,fibre_label(),heading('Mouse · type II taste cells'),label('Schematic: predominant selectivity; some overlap',(0,-3.45),26,GREY))
        for phrase,i,name,col in [('to sweet',0,'sweet',BLUE),('to bitter',1,'bitter',RED),('to umami',2,'umami',PURPLE)]:
            self.at(phrase);self.play(b[1][i].animate.set_color(col).set_fill(col,opacity=.35),FadeIn(label(name,(-2.9+i*1.4,.65),26,col).rotate(PI/2)),run_time=.4)
        split=VGroup(*[Ellipse(width=.55,height=3.4,color=col,fill_color=col,fill_opacity=.65).move_to([x,.2,0]) for x,col in [(1.05,BLUE),(1.55,PURPLE)]])
        note=label('sweet +\numami',(4.6,.8),28);lead=Line([3.5,.8,0],[1.85,.8,0],color=TEXT)
        self.at('some cells');self.play(FadeIn(split),FadeIn(note),Create(lead),run_time=.45);self.finish()

class S08Type3(SpokenScene):
    def construct(self):
        cell=Ellipse(width=3,height=4.6,color=GOLD,fill_color=GOLD,fill_opacity=.15).move_to([-1,.1,0]);f=Line([-4,-2.2,0],[4.8,-2.2,0],color=GREEN,stroke_width=13)
        self.add(cell,f,heading('Type III · sour'),fibre_label())
        ves=VGroup(*[Circle(radius=.16,color=GREY,fill_color=GREY,fill_opacity=.5).move_to([-1+dx,-1.5+dy,0]) for dx,dy in [(-.5,0),(0,0),(.5,0),(-.25,.4),(.25,.4)]])
        self.at('conventional synapses');self.play(FadeIn(ves),FadeIn(label('vesicles',(3,-.6),28)),Create(Line([2,-.7,0],[-.4,-1.3,0],color=GREY)),FadeIn(label('conventional synapse',(0,-3.45),28)),run_time=.5);self.finish()

class S09Channel(SpokenScene):
    def construct(self):
        cell=Ellipse(width=4.8,height=3.7,color=BLUE,fill_color=BLUE,fill_opacity=.08).move_to([-1.5,.7,0]);f=RoundedRectangle(width=8,height=.8,corner_radius=.3,color=GREEN,fill_color=GREEN,fill_opacity=.15).move_to([0,-2.65,0]);ch=chip('CALHM1/3',TEAL,28).move_to([-1.5,-1.6,0])
        self.add(cell,f,heading('Type II taste cell'),label('nerve fibre',(4.5,-3.45),28,GREEN))
        self.at('no conventional');self.play(FadeIn(label('no conventional\nvesicular synapse',(-1.5,.8),30)),run_time=.4)
        dots=VGroup(*[Dot([-2+i*.5,ch.get_bottom()[1]-.1,0],radius=.11,color=YELLOW) for i in range(3)])
        self.at('they release');self.play(FadeIn(ch),FadeIn(dots),FadeIn(label('ATP',(2.5,-.7),30,YELLOW)),run_time=.4)
        self.at('through a channel');self.play(*[d.animate.shift(DOWN*.6) for d in dots],run_time=.65);self.finish()

class S10Slow(SpokenScene):
    def construct(self):
        ax,l,c=kinetics();self.add(ax,l,heading('CALHM1 alone'))
        self.at('opens slowly');self.play(Create(c),run_time=1.1)
        self.at('time constant');self.play(FadeIn(marker(ax,500,500,TEAL)),FadeIn(label('63% at 500 ms',(.2,.05),28,TEAL)),Create(Line(ax.c2p(500,1-np.exp(-1)),[-.9,.25,0],color=TEAL)),FadeIn(label('time constant > 500 ms',(1,-.6),30)),FadeIn(label('curve uses 500 ms',(1,-1.2),26,GREY)),run_time=.5);self.finish()

class S11Q(SpokenScene):
    def construct(self):
        ax,g,d=short_base();self.add(g);self.at('spike is brief');self.play(Indicate(d,color=YELLOW,scale_factor=1.7),run_time=.5)
        self.play(Create(closed_gap(.5)),FadeIn(gap_caption()),run_time=2.5);self.finish()

class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;ax,g,d=short_base();bracket=closed_gap(.5);self.add(g,bracket,gap_caption())
        self.play(Transform(bracket,closed_gap(1)),run_time=3,rate_func=linear)

class S13Fast(SpokenScene):
    def construct(self):
        ax,g,d=short_base(False);self.add(g)
        fast=ax.plot(lambda t:1-np.exp(-t/10),x_range=[0,30,.1],color=PURPLE,stroke_width=6,use_smoothing=False)
        name=label('CALHM1 + CALHM3',(2,.65),28,PURPLE)
        self.at('adding a');self.play(Create(fast),FadeIn(name),Create(Line(name.get_top(),ax.c2p(22,1-np.exp(-22/10))-DOWN*.02,color=PURPLE)),run_time=.8)
        self.at('opening to about');self.play(FadeIn(marker(ax,10,10,PURPLE)),FadeIn(label('10 ms · 63%',(.1,-.05),28,PURPLE)),Create(Line(ax.c2p(10,1-np.exp(-1)),[-.8,.15,0],color=PURPLE)),run_time=.4)
        self.at('not delays');self.play(Transform(g[1][3],label('cultured cells · not delays in a living mouse',(0,-3.58),26,GREY)),run_time=.4);self.finish()

class S14Ko(SpokenScene):
    def construct(self):
        self.add(heading('Mouse · Calhm3 deleted'))
        buds=VGroup(*[bud().scale(.59).move_to([x,.1,0]) for x in [-3.2,3.2]])
        self.add(buds,label('wild type',(-3.2,2.1),30,BLUE),label('knockout',(3.2,2.1),30,RED),label('nerve fibres',(0,-2),26,GREEN))
        dots=VGroup(*[Dot([-3.8+i*.4,-1.1,0],radius=.1,color=YELLOW) for i in range(4)]);self.add(dots,label('ATP released',(-3.2,-2.7),28,YELLOW))
        self.at('lacking that partner');self.play(*[d.animate.shift(DOWN*.6) for d in dots],run_time=.5)
        self.at('released no');self.play(FadeIn(label('No taste-evoked\nATP release',(3.2,-2.7),28,RED)),run_time=.4);self.finish()

class S15Ganglion(SpokenScene):
    def construct(self):
        n,e=pathway();self.add(n,e,pathway_labels());VGroup(*n[2:],*e[1:]).set_opacity(.18)
        self.at('front of the tongue');self.play(Indicate(n[0],color=RED),run_time=.5)
        self.at('geniculate ganglion');self.play(n[1].animate.set_color(BLUE),Create(e[0]),run_time=.5);self.finish()

class S16Relays(SpokenScene):
    def construct(self):
        n,e=pathway();self.add(n,e,pathway_labels());VGroup(*n[2:],*e[1:]).set_opacity(.18)
        self.at('brainstem relays');self.play(reveal_node(n[2]),reveal_node(n[3]),e[1].animate.set_opacity(1),e[2].animate.set_opacity(1),run_time=.5)
        self.at('the thalamus');self.play(reveal_node(n[4]),e[3].animate.set_opacity(1),run_time=.4)
        self.at('taste cortex');self.play(reveal_node(n[5]),e[4].animate.set_opacity(1),run_time=.4)
        self.at('to the amygdala');self.play(reveal_node(n[6]),reveal_node(n[7]),*[e[i].animate.set_opacity(1) for i in [5,6,7]],run_time=.5);self.finish()

class S17Sampled(SpokenScene):
    def construct(self):
        n,e=pathway();self.add(n,e,pathway_labels());self.at('three stations');self.play(*[dim_relay(n[i]) for i in [0,2,3,4,7]],e.animate.set_opacity(.5),FadeIn(label('Dimmed nodes: not tested here',(1.8,-3.4),26,GREY)),run_time=.4)
        for cue,i in [('the ganglion',1),('the cortex',5),('the amygdala',6)]:
            self.at(cue);self.play(n[i].animate.set_color(BLUE),run_time=.35)
        self.finish()

class S18Idea(SpokenScene):
    def construct(self):
        b=bud().scale(.78).move_to([-2.8,.3,0]);fl=label('nerve fibre',(-1.5,-2.15),28,GREEN);self.add(b,heading('The one idea'),fl)
        box=card('Identity begins with',['which taste-cell','population is driven'],BLUE,(3.2,.3),5.6,3.4);box[1][0].scale(1.06);box[1][1:].scale(1.18)
        sweet=label('sweet',(-4.5,2.4),28,BLUE)
        active=Line(b[2][1].get_start(),b[2][0].get_end(),color=BLUE,stroke_width=8)
        self.at('one idea');self.play(FadeIn(box),b[1][0].animate.set_color(BLUE).set_fill(BLUE,opacity=.5),b[2][1].animate.set_color(BLUE),Create(active),fl.animate.set_color(BLUE),FadeIn(sweet),run_time=.5);self.finish()

class S19Breadth(SpokenScene):
    def construct(self):
        self.add(heading('Mouse · response profiles'),label('Key:',(-3,2.45),26),label('sweet',(-1.5,2.45),28,BLUE),label('a second taste',(1.4,2.45),28,PURPLE),label('Schematic of the observed pattern · three example fibres',(0,-3.15),26,GREY),label('marks show responses, not amplitudes',(0,-3.6),26,GREY))
        panels=VGroup(*[card(title,[],GREY,(x,-.1),5.8,4.5) for x,title in [(-3.15,'Low strength'),(3.15,'High strength')]])
        for p in panels:p[1].move_to(p.get_center()+UP*1.7)
        self.add(panels)
        bars=VGroup();extra=VGroup()
        for x in [-3.15,3.15]:
            for i in range(3):
                y=.65-i*1.15;bars.add(label(f'Fibre {i+1}',(x-1.7,y),30),Rectangle(width=2.1,height=.4,color=BLUE,fill_color=BLUE,fill_opacity=1).move_to([x+.9,y,0]))
                if x>0 and i<2:extra.add(Rectangle(width=2.1,height=.4,color=PURPLE,fill_color=PURPLE,fill_opacity=1).move_to([x+.9,y-.46,0]))
        self.at('selectively at low');self.play(FadeIn(bars),run_time=.4)
        self.at('more broadly');self.play(FadeIn(extra),run_time=.5)
        self.at('not all');self.play(FadeIn(SurroundingRectangle(VGroup(bars[10],bars[11]),color=GOLD,buff=.16)),run_time=.4)
        self.finish()

class S20Value(SpokenScene):
    def construct(self):
        c=cortex();r=readouts();self.add(c,r,heading('Mouse assays'))
        self.at('sweet field');self.play(c[1][0].animate.set_fill(BLUE,opacity=.5),run_time=.35)
        self.at('drawn in');self.play(r[1][0].animate.set_fill(GREEN,opacity=.3),Transform(r[1][1][1],label('drawn in · licking',(3.3,-2),32,GREEN)),run_time=.4)
        self.at('block that field');self.play(FadeIn(Cross(c[1][0],stroke_color=RED)),FadeIn(label('blocked',(-1.45,.8),26,RED)),r[1][0].animate.set_fill(GREEN,opacity=.07),Transform(r[1][1][1],label('licking',(3.3,-2),32,GREEN)),run_time=.4)
        self.at('struggle to');self.play(Transform(r[0][1][1],label('recognition impaired',(-3.3,-2),30,RED)),r[0][0].animate.set_stroke(RED),run_time=.45);self.finish()

class S21Bitter(SpokenScene):
    def construct(self):
        c=cortex();c[1].set_color(GREY).set_opacity(.4);c[2].set_opacity(1).set_color(RED);c[2][0].set_fill(RED,opacity=.12);m,s,t=rig(pos=(-1.4,-1),scale=1.2);self.add(c,m,s,heading('Mouse assays'))
        self.at('bitter field');self.play(c[2][0].animate.set_fill(RED,opacity=.5),run_time=.3)
        self.at('turns away');self.play(m.animate.flip().shift(LEFT*.7),GrowArrow(Arrow([1,-2.8,0],[-2.5,-2.8,0],color=RED)),FadeIn(label('aversion',(0,-3.35),30,RED)),run_time=.5);self.finish()

class S22Open(SpokenScene):
    def construct(self):
        c,r,a,l,d=assay();self.add(c,r,a,l,d,heading('Mouse assays'))
        self.at('one manipulation');self.play(a[0].animate.set_stroke(PURPLE,width=6),run_time=.4)
        self.at('two readouts');self.play(Indicate(r[0][0],color=BLUE),Indicate(r[1][0],color=GREEN),run_time=.5);self.finish()

class S23Recognize(SpokenScene):
    def construct(self):
        c,r,a,l,d=assay();self.add(c,r,a,l,d,heading('Mouse assays'),tested_route())
        self.at('silence the amygdala');self.play(FadeIn(silence(a)),run_time=.45)
        self.at('still');self.play(r[0][0].animate.set_fill(BLUE,opacity=.35),run_time=.35)
        self.at('no longer');self.play(r[1][0].animate.set_stroke(GREY,opacity=.5).set_fill(BG,opacity=1),r[1][1].animate.set_opacity(.4),l[2].animate.set_opacity(.3),FadeIn(label('recognized; no longer drawn in',(0,-3.25),30)),run_time=.5);self.finish()

class S24Need(SpokenScene):
    def construct(self):
        m,s,t=rig(pos=(-2,-1.1),scale=.95);s.shift(RIGHT*2);self.add(m,s,heading('Body state can change the pull · mice'))
        gauge=Line([-3.5,1.6,0],[3.5,1.6,0],color=GREY,stroke_width=7);dot=Dot([-3.5,1.6,0],radius=.15,color=GREEN)
        self.add(gauge,dot,label('sated',(-3.5,2.2),28),label('need',(3.5,2.2),28,GREEN))
        start=m[4].get_center();end=s[1].get_center();arrow=Arrow(start,end-LEFT*.01,buff=.12,color=GREEN,stroke_width=3);self.add(arrow)
        self.at('pull changes');self.play(dot.animate.move_to([3.5,1.6,0]),arrow.animate.set_stroke(width=13),run_time=1.5);self.finish()

class S25Scope(SpokenScene):
    def construct(self):
        self.add(mouse((0,-1.2),.85),label('Mouse experiments',(0,2.65),30));self.play(FadeIn(label('Not a human map',(0,1.2),48,RED)),run_time=.4);self.finish()

class S26Take(SpokenScene):
    def construct(self):
        c,r,a,l,d=assay();self.add(c,r,a,l,d,tested_route(),heading('Which taste, and how good?'),label('mouse assays · behavioural dissociation',(0,-3.3),26,GREY))
        self.at('one cortical field');self.play(c[1][0].animate.set_fill(BLUE,opacity=.5),r[0][0].animate.set_fill(BLUE,opacity=.25),r[1][0].animate.set_fill(GREEN,opacity=.25),run_time=.4)
        self.at('silencing the amygdala');self.play(FadeIn(silence(a)),r[1][0].animate.set_stroke(GREY,opacity=.5).set_fill(BG,opacity=1),r[1][1].animate.set_opacity(.4),l[2].animate.set_opacity(.3),run_time=.5);self.finish()

class S27End(EndCard):
    LINE='Silencing the amygdala separates recognition and attraction in these mouse assays.'
    def construct(self):
        line=T('Silencing the amygdala separates\nrecognition and attraction\nin these mouse assays.',36,font=TITLE_FONT,line_spacing=1.2)
        self.add(T('biochemistrypedia.com',26,TEAL).move_to([0,-2,0]));self.play(FadeIn(line),run_time=.7);self.finish()
