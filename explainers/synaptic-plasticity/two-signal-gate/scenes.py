"""Chapter 2, review redraw.
COLOR MAP: YELLOW glutamate; BLUE (#58C4DD) AMPA; PURPLE NMDA;
ORANGE Mg2+; CALCIUM (#A8E66F, lime) Ca2+ (distinct from AMPA);
PINK voltage/depolarization; TEXT labels; GREY membrane; GOLD questions.
All quantitative curves/bars use Jahr–Stevens × GHK below. The pulse-train
accumulation is explicitly a schematic, without a numerical output claim.
"""
import os
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
PINK = '#E58FC0'
CALCIUM = '#A8E66F'
HELP = '#CDD2DD'


def unblocked(v):
    return 1 / (1 + np.exp(-.062*v)/3.57)


def inward(v):
    u = 2*96485.33212*(v/1000)/(8.314462618*308.15)
    return 2-.0001 if abs(u)<1e-7 else u*(2-.0001*np.exp(u))/np.expm1(u)


def entry(v):
    return unblocked(v)*inward(v)


def label(s,x=0,y=3,color=TEXT,size=30):
    return T(s,size=size,color=color,line_spacing=1.15).move_to([x,y,0])


def leader(s,x,y,point,color=HELP,size=28):
    t=label(s,x,y,color,size)
    a=Line(t.get_left() if point[0]<x-1 else (t.get_right() if point[0]>x+1 else (t.get_bottom() if point[1]<y else t.get_top())),point,color=color,buff=.12)
    return VGroup(a,t)


def channel(x=0,y=.2,color=PURPLE,h=3.2,w=2.2,corner=.3):
    # One connected silhouette, with a dark pore cut through its centre.
    body=RoundedRectangle(width=w,height=h,corner_radius=corner,color=color,
        fill_color=color,fill_opacity=.38,stroke_width=4).move_to([x,y,0])
    pore=Rectangle(width=w*.32,height=h+.04,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([x,y,0])
    return VGroup(body,pore)


def plug(x=-2,y=.2,r=.4):
    return VGroup(Circle(radius=r,color=ORANGE,fill_opacity=1).move_to([x,y,0]),
                  label('+',x,y,BG,28))


def gate(glu=True):
    mem=VGroup(Line([-5.9,.2,0],[-3.15,.2,0],color=GREY,stroke_width=14),
               Line([-.85,.2,0],[1.1,.2,0],color=GREY,stroke_width=14))
    g=VGroup(mem,channel(-2),label('NMDA',-4.5,-.65,PURPLE,32),
             label('outside',-4.6,2.6,HELP,28),label('inside spine',-3.8,-2.8,HELP,28))
    if glu:
        g.add(Dot([-2.85,1.65,0],radius=.16,color=YELLOW))
    return g


def ca_meter(value=0,question=False):
    rim=Rectangle(width=.85,height=3.8,color=CALCIUM).move_to([4.4,-.1,0])
    g=VGroup(rim,label('Ca²⁺ entry',4.35,2.65,CALCIUM,30),
             label('relative rate',4.35,2.15,HELP,26))
    for n in (0,1,4):
        y=-2+3.8*n/4
        g.add(label(str(n),3.55,y,HELP,26),Line([3.95,y,0],[4.05,y,0],color=HELP))
    if question:
        g.add(label('?',4.4,-.1,GOLD,64))
    elif value>0:
        g.add(Rectangle(width=.65,height=3.8*value/4,stroke_width=0,fill_color=CALCIUM,fill_opacity=.85).move_to([4.4,-2+1.9*value/4,0]))
    else:
        g.add(label('0',4.4,-1.6,CALCIUM,32))
    return g


def spine():
    head=RoundedRectangle(width=6,height=3.5,corner_radius=1.2,color=GREY,fill_opacity=.1).move_to([0,.45,0])
    neck=VGroup(Line([-.55,-1.3,0],[-.55,-2.5,0],color=GREY,stroke_width=6),Line([.55,-1.3,0],[.55,-2.5,0],color=GREY,stroke_width=6))
    dend=RoundedRectangle(width=11,height=.8,corner_radius=.25,color=GREY,fill_opacity=.1).move_to([0,-2.9,0])
    return VGroup(head,neck,dend)


def voltage_meter(v=-70,x=3.5):
    # Full-height meter, numerical labels stay outside the moving fill.
    g=VGroup(label('spine voltage (mV)',x,2.9,PINK,28),
        Rectangle(width=.7,height=3.8,color=PINK).move_to([x,-.05,0]))
    for n in (-70,-50,-30):
        y=-1.95+(n+70)/40*3.8
        g.add(label(str(n).replace('-','−'),x+1,y,HELP,26))
    h=max(.04,(v+70)/40*3.8)
    g.add(Rectangle(width=.5,height=h,stroke_width=0,fill_color=PINK,fill_opacity=.7).move_to([x,-1.95+h/2,0]))
    return g


def factors():
    g=VGroup()
    for x,txt,col,num in [(-4,'glutamate\nbound',YELLOW,'1'),(0,'fraction of\nblock cleared',ORANGE,'2'),(4,'inward push\non Ca²⁺',CALCIUM,'3')]:
        box=RoundedRectangle(width=3.25,height=3.5,corner_radius=.2,color=col,fill_color=col,fill_opacity=.1).move_to([x,.25,0])
        icon=Dot([x,1.35,0],radius=.24,color=col) if num=='1' else (plug(x,1.35,.25) if num=='2' else Arrow([x,1.75,0],[x,.9,0],color=col,buff=0))
        g.add(VGroup(box,icon,label(txt,x,-.45,col,30)))
    return g


def model_note(y=-2.3):
    return VGroup(label('Steady-flux model: Jahr–Stevens block × GHK Ca²⁺ flux',0,y,HELP,26),
        label('1 mM Mg²⁺ / 2 mM Ca²⁺ outside; 100 nM Ca²⁺ inside; 35 °C',0,y-.48,HELP,26),
        label('Ligand activation fixed; co-agonist present',0,y-.96,HELP,26))


def question_frame():
    return VGroup(gate(),plug(),label('−70 mV',.5,3,PINK,34),ca_meter(question=True),
                  label('Does any calcium get in?',0,-3.35,GOLD,34))


def scale_voltage():
    g=VGroup(Line([-5.2,-.3,0],[5.2,-.3,0],color=HELP))
    for n in (-90,-70,-50,0):
        x=-5.2+(n+90)/90*10.4
        g.add(Line([x,-.4,0],[x,-.2,0],color=HELP),label(str(n).replace('-','−'),x,-.8,HELP,28))
    g.add(label('membrane voltage (mV)',0,-1.4,HELP,28))
    return g


def rope(v=-70,g=0.285714,ampa=True):
    x=-5.2+(v+90)/90*10.4
    # Two braided ropes meet at the voltage marker; arrowheads show opposing pulls.
    ropes=VGroup()
    for start,end,col,width in [(-5.2,x,HELP,12),(x,5.2,BLUE,3+8*g)]:
        if col==BLUE and not ampa:
            continue
        ropes.add(Line([start,.1,0],[end,.1,0],color=col,stroke_width=width))
        for dy in (-.045,.045):
            ropes.add(Line([start,.1+dy,0],[end,.1+dy,0],color=BG,stroke_width=1))
        middle=(start+end)/2
        direction=-1 if col==HELP else 1
        ropes.add(Arrow([middle-direction*.35,.1,0],[middle+direction*.35,.1,0],
                        color=col,buff=0,stroke_width=3,max_tip_length_to_length_ratio=.35).shift(UP*.35))
    ropes.add(Dot([x,.1,0],radius=.19,color=PINK))
    return ropes


def rope_labels(ampa=True):
    g=VGroup(label('K⁺ rope ←',-3.6,1.35,HELP,30),label('reversal ≈ −90 mV',-3.6,.85,HELP,26))
    if ampa:
        g.add(label('→ AMPA rope',3.5,1.35,BLUE,30),label('reversal ≈ 0 mV',3.5,.85,BLUE,26))
    return g


class S00Title(TitleCard):
    LESSON='Synaptic Plasticity'
    TITLE='A Gate That Needs Two Signals'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.3,TEAL,26),label(self.LESSON.upper(),0,1.65,HELP,28))
        self.play(FadeIn(label('A Gate That Needs\nTwo Signals',0,0,TEXT,54)),Create(Line([-1.2,-1.6,0],[1.2,-1.6,0],color=GOLD)),run_time=.7)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        self.add(spine(),label('spine',0,.6,HELP,32))
        self.at('input fired')
        self.play(GrowArrow(Arrow([-5.5,2.6,0],[-2.4,1.6,0],color=YELLOW)),FadeIn(label('input',-4.8,3.2,YELLOW,32)),run_time=.6)
        self.at('own cell')
        self.play(GrowArrow(Arrow([5.4,-1.4,0],[3,-2.8,0],color=PINK)),FadeIn(label('cell',5.2,-.8,PINK,32)),run_time=.6)
        self.at('What molecule')
        self.play(FadeIn(label('?',0,-.3,GOLD,76)),run_time=.5)
        self.finish()


class S02Spine(SpokenScene):
    def construct(self):
        terminal=RoundedRectangle(width=6,height=1,corner_radius=.25,color=GREY).move_to([0,2.8,0])
        sp=spine(); sp[0].stretch_to_fit_height(2.6).move_to([0,0,0])
        syn=VGroup(sp,terminal,label('Schaffer terminal',0,2.85,HELP,30),label('spine',0,.3,HELP,30),label('CA1 dendrite',0,-2.9,HELP,28))
        geometry=VGroup(sp.copy(),terminal.copy())
        mini=geometry.copy().scale(.32).move_to([3,-.7,0])
        map_=VGroup(chip('CA3',HELP,36).move_to([-3,1,0]),chip('CA1',HELP,36).move_to([3,1,0]),Arrow([-2,1,0],[2,1,0],color=HELP),label('hippocampus',0,3,HELP,36),label('Schaffer collateral',0,-1.9,HELP,30))
        self.add(map_,mini)
        self.at('onto')
        self.play(FadeOut(map_),run_time=.2)
        self.play(Transform(mini,geometry),run_time=.9,rate_func=linear)
        self.at('The terminal')
        self.play(FadeIn(syn[2]),FadeIn(leader('cleft',4.8,1.9,[3,2.1,0],HELP)),run_time=.4)
        self.at('releases glutamate')
        dots=VGroup(*[Dot([x,2.35,0],radius=.14,color=YELLOW) for x in (-1,0,1)])
        self.add(dots)
        self.play(dots.animate.shift(DOWN*.65),FadeIn(leader('glutamate',-4.5,1.9,[-1.1,1.7,0],YELLOW)),run_time=.9)
        self.at('small bud')
        self.play(Indicate(mini[0][0],color=TEXT,scale_factor=1.02),FadeIn(syn[3]),FadeIn(syn[4]),run_time=.6)
        self.finish()


class S03Two(SpokenScene):
    def construct(self):
        self.add(Line([-6,0,0],[6,0,0],color=GREY,stroke_width=14),label('outside',0,3.1,HELP),label('inside spine',0,-3.1,HELP))
        self.at('Two kinds')
        a=channel(-3,0,BLUE,h=4.6,w=2.7); n=channel(3,0,h=4.6,w=2.7)
        self.play(FadeIn(a),FadeIn(n),run_time=.55)
        self.at('glutamate receptors')
        self.play(FadeIn(label('AMPA',-3,-2.7,BLUE,34)),FadeIn(label('NMDA',3,-2.7,PURPLE,34)),FadeIn(leader('pore',0,1.7,[2.9,.7,0],HELP,28)),run_time=.5)
        self.finish()


class S04Ampa(SpokenScene):
    def construct(self):
        c=channel(0,.2,BLUE,h=3.9,w=3)
        lid=Line([-.48,.2,0],[.48,.2,0],color=BLUE,stroke_width=12)
        d=Dot([-2.5,2.6,0],radius=.18,color=YELLOW)
        tag=leader('glutamate',-4.5,2.6,[-2.5,2.6,0],YELLOW)
        self.add(c,lid,d,tag,label('AMPA',0,-2.2,BLUE,34),label('outside',3.9,2.1,HELP),label('inside spine',3.9,-2.1,HELP))
        self.at('only glutamate')
        self.play(d.animate.move_to([-1.2,2.05,0]),Transform(tag,leader('glutamate',-4,2.6,[-1.2,2.05,0],YELLOW)),run_time=.6)
        self.at('to open')
        self.play(FadeOut(lid),GrowArrow(Arrow([0,1.9,0],[0,-1.8,0],color=HELP,buff=0)),run_time=.35)
        ion=chip('Na⁺',TEXT,34).move_to([0,1.5,0]); ion[0].set_fill(BG,1); self.add(ion)
        self.play(ion.animate.move_to([0,-1.55,0]),run_time=.7)
        self.remove(ion)
        self.at('They carry most')
        self.play(FadeIn(label('AMPA: needs only glutamate',0,-2.8,BLUE,30)),run_time=.4)
        self.at('the ordinary')
        self.play(FadeIn(label('ordinary EPSP',3.9,-.1,BLUE,32)),run_time=.5)
        self.finish()


class S05Nmda(SpokenScene):
    def construct(self):
        c=channel(0,.2,h=3.9,w=3); lid=Line([-.48,.2,0],[.48,.2,0],color=PURPLE,stroke_width=12)
        d=Dot([-2.6,2.7,0],radius=.18,color=YELLOW)
        self.add(c,lid,d,label('NMDA',0,-2.4,PURPLE,34),label('pore still closed',0,-3.05,HELP,30))
        self.at('also bind glutamate')
        self.play(d.animate.move_to([-1.2,2.05,0]),FadeIn(leader('glutamate',-4.2,2.8,[-1.2,2.05,0],YELLOW)),run_time=.6)
        self.at('They need')
        co=Dot([3.3,2.8,0],radius=.18,color=HELP); self.play(FadeIn(co),FadeIn(label('co-agonist',4.3,1.8,HELP,30)),run_time=.4)
        self.at('glycine or')
        self.play(co.animate.move_to([1.2,2.05,0]),FadeIn(leader('glycine or\nD-serine',4.3,.55,[1.2,2.05,0],HELP,28)),run_time=.6)
        self.at('normally present')
        self.play(FadeIn(label('normally present',4.3,-1.2,HELP,28)),run_time=.4)
        self.finish()


class S06Mg(SpokenScene):
    def construct(self):
        self.add(gate(),label('at rest • −70 mV',0,3.2,PINK,32))
        p=plug(-2,2.55)
        self.at('magnesium ion')
        t=leader('Mg²⁺',1.5,2.5,[-2,2.55,0],ORANGE,34)
        self.play(FadeIn(p),FadeIn(t),run_time=.4)
        self.at('sits in')
        self.play(p.animate.move_to([-2,.2,0]),FadeOut(t),run_time=.65)
        self.at('blocks it')
        self.play(FadeIn(leader('Mg²⁺ blocks\nthe pore',2.7,.8,[-2,.2,0],ORANGE,32)),FadeIn(label('no ions pass',2.8,-1.5,HELP,30)),run_time=.35)
        self.finish()


class S07Open(SpokenScene):
    def construct(self):
        p=plug(); self.add(gate(),p)
        self.at('Once the block clears')
        self.play(p.animate.move_to([.2,2.8,0]),FadeIn(leader('Mg²⁺',2.1,2.8,[.2,2.8,0],ORANGE,30)),run_time=.6)
        arrow=Arrow([-2,2,0],[-2,-2,0],color=HELP,buff=0); self.add(arrow)
        for cue,txt,col in [('they pass sodium','Na⁺',TEXT),('potassium','K⁺',TEXT),('and calcium','Ca²⁺',CALCIUM)]:
            self.at(cue)
            # Net K+ movement is outward in this voltage regime.
            start,end=([-2,-1.8,0],[-2,1.9,0]) if txt=='K⁺' else ([-2,1.9,0],[-2,-1.8,0])
            new=Arrow(start,end,color=col,buff=0)
            ion=chip(txt,col,34).move_to(start); ion[0].set_fill(BG,1); self.add(ion)
            self.play(Transform(arrow,new),ion.animate.move_to(end),run_time=.48)
            self.remove(ion)
        self.finish()


class S08Clear(SpokenScene):
    def construct(self):
        p=plug(); self.add(gate(),p)
        band=RoundedRectangle(width=11.7,height=1.1,corner_radius=.15,stroke_width=0,fill_color=PINK,fill_opacity=.12).move_to([0,-2.85,0])
        signs=label('−  −  −  −  −',0,-2.85,PINK,36); num=label('−70 mV',4.4,-2.85,PINK,32)
        self.at('Depolarization')
        self.play(FadeIn(label('Depolarization',1.3,3.2,PINK,34)),run_time=.4)
        self.at('Magnesium is positive')
        tag=leader('Mg²⁺',2.9,.9,[-2,.2,0],ORANGE,34)
        self.play(FadeIn(tag),run_time=.4)
        self.at('negative inside')
        self.play(FadeIn(band),FadeIn(signs),FadeIn(num),run_time=.4)
        self.at('Make the inside less negative')
        self.play(Transform(signs,label('−  −',0,-2.85,PINK,36)),FadeOut(num),band.animate.set_fill(PINK,.3),run_time=.6)
        self.play(FadeIn(label('−40 mV',4.4,-2.85,PINK,32)),run_time=.3)
        self.at('pushed out')
        self.play(p.animate.move_to([-.1,2.6,0]),Transform(tag,leader('Mg²⁺',2.7,2.3,[-.1,2.6,0],ORANGE,30)),run_time=.6)
        self.finish()


class S09Balance(SpokenScene):
    def construct(self):
        self.add(label('Where does depolarization come from?',0,3.1,TEXT,34),scale_voltage(),rope(ampa=False),rope_labels(False))
        self.at('depolarization come from')
        self.play(Indicate(self.mobjects[2][-1],color=PINK,scale_factor=1.25),run_time=.6)
        self.at('Recall the balance point')
        self.play(FadeIn(label('local balance point',0,-2.3,PINK,32)),run_time=.5)
        self.at('action potential lesson')
        self.play(Indicate(self.mobjects[1],color=PINK,scale_factor=1.01),run_time=1.3)
        self.at('tug of war')
        self.play(Indicate(self.mobjects[2],color=PINK,scale_factor=1.03),FadeIn(label('Rope thickness = open channels',0,-3.1,HELP,30)),run_time=.7)
        self.finish()


class S10Balance2(SpokenScene):
    def construct(self):
        r=rope(); self.add(scale_voltage(),r,rope_labels())
        self.at('isolated compartment')
        self.play(FadeIn(label('isolated compartment',0,3.25,HELP,28)),run_time=.35)
        self.at('fixed ohmic conductances')
        self.play(FadeIn(label('fixed ohmic conductances',0,2.65,HELP,28)),run_time=.35)
        self.at('no injected or axial current')
        self.play(FadeIn(label('no injected or axial current',0,2.05,HELP,28)),run_time=.35)
        self.at('voltage relaxes')
        self.play(Indicate(r[-1],color=PINK,scale_factor=1.3),run_time=.7)
        self.at('weighted average')
        self.play(FadeIn(M('V∞ = Σ(g × E) / Σg',size=34).move_to([0,-2.05,0])),run_time=.45)
        self.at("Each current's reversal potential")
        self.play(FadeIn(label('E = reversal potential',0,-2.7,HELP,28)),run_time=.4)
        self.at('proportion to its conductance')
        self.play(Transform(r,rope(-90/3,2)),FadeIn(label('g = conductance (open channels)',0,-3.3,HELP,28)),run_time=1)
        self.finish()


class S11AmpaRope(SpokenScene):
    def construct(self):
        r=rope(ampa=False); self.add(scale_voltage(),r,rope_labels(False),label('More open channels → stronger pull',0,3.1,TEXT,34))
        self.at('current reverses')
        self.play(Transform(r,rope()),FadeIn(VGroup(*rope_labels()[2:])),run_time=.6)
        self.at('many receptors open')
        chans=VGroup(*[channel(x,2.25,BLUE,h=1.05,w=.55,corner=.07) for x in np.linspace(-4.8,4.8,8)])
        self.play(LaggedStart(*[FadeIn(c) for c in chans],lag_ratio=.25),run_time=1.1)
        self.at('pull the local balance point')
        self.play(Transform(r,rope(-90/3,2)),FadeIn(label('toward 0 mV',2.7,-2.4,PINK,34)),run_time=2)
        self.finish()


class S12Bap(SpokenScene):
    def construct(self):
        soma=Circle(radius=1.05,color=GREY,fill_opacity=.15).move_to([-3.2,-1.1,0])
        ax=Line([-3.2,-2.15,0],[-3.2,-3.25,0],color=GREY,stroke_width=18)
        dend=VMobject(color=GREY,stroke_width=22).set_points_as_corners([[-3.2,-.1,0],[-2.3,1,0],[0,1.2,0],[3,1.2,0]])
        head=RoundedRectangle(width=2.3,height=1.7,corner_radius=.65,color=GREY,fill_opacity=.1).move_to([3,2.65,0])
        neck=VGroup(Line([2.75,1.2,0],[2.75,1.8,0],color=GREY,stroke_width=5),Line([3.25,1.2,0],[3.25,1.8,0],color=GREY,stroke_width=5))
        self.add(soma,ax,dend,head,neck,leader('cell body',-5.2,-.9,[-4.1,-1.1,0],HELP),leader('axon initial\nsegment',-.5,-2.8,[-3.2,-2.7,0],HELP),label('dendrite',-.3,.5,HELP),label('spine',5,2.7,HELP))
        p=Dot([-3.2,-2.8,0],radius=.22,color=PINK); trail=TracedPath(p.get_center,stroke_color=PINK,stroke_width=10)
        self.at('spike fired')
        self.add(p,trail); self.play(p.animate.move_to([-3.2,-1.1,0]),run_time=1.2)
        self.at('spreading back')
        path=VMobject().set_points_as_corners([[-3.2,-1.1,0],[-3.2,-.1,0],[-2.3,1,0],[0,1.2,0],[3,1.2,0],[3,2.65,0]])
        self.play(MoveAlongPath(p,path),run_time=1.8)
        self.at('depolarizes the spine')
        self.play(head.animate.set_color(PINK).set_fill(PINK,.4),Flash([3,2.65,0],color=PINK),run_time=.6)
        self.finish()


class S13Reports(SpokenScene):
    def construct(self):
        p=plug(); vm=voltage_meter(); self.add(gate(),p,vm)
        self.at('spine voltage reports')
        self.play(Indicate(vm[0],color=PINK,scale_factor=1.04),run_time=.7)
        self.at('postsynaptic cell')
        self.play(FadeIn(label('postsynaptic activity',0,-3.35,PINK,30)),run_time=.5)
        self.at('magnesium block reads')
        self.play(Transform(vm,voltage_meter(-30)),p.animate.move_to([-.4,2.65,0]),run_time=1.5)
        self.at('A spike is one source')
        self.play(FadeIn(label('backpropagating spike',-2,3.3,PINK,28)),run_time=.5)
        self.at('not the only one')
        self.play(FadeIn(label('AMPA input',-1.8,-2.1,BLUE,30)),run_time=.5)
        self.finish()


class S14Rule(SpokenScene):
    def construct(self):
        self.add(label('Ca²⁺ entry through NMDA receptors',0,3.15,CALCIUM,34))
        # Start with a physical signal pairing, rather than empty formula boxes.
        intro=VGroup(chip('glutamate',YELLOW,32).move_to([-3,.4,0]),chip('voltage',PINK,32).move_to([3,.4,0]),label('+',0,.4,TEXT,40))
        self.add(intro); b=factors()
        seeds=VGroup(*[box[1].copy() for box in b])
        self.at('product of three factors')
        self.play(FadeOut(intro),FadeIn(seeds),FadeIn(label('∝',-6,.25,TEXT,38)),FadeIn(label('×',-2,.25,TEXT,34)),FadeIn(label('×',2,.25,TEXT,34)),run_time=.4)
        self.at('First')
        self.play(FadeOut(seeds[0]),FadeIn(b[0]),run_time=.4)
        self.at('Second')
        self.play(FadeOut(seeds[1]),FadeIn(b[1]),run_time=.4)
        self.at('Third')
        self.play(FadeOut(seeds[2]),FadeIn(b[2]),run_time=.4)
        self.at('inward push')
        self.play(FadeIn(model_note()),run_time=.4)
        self.finish()


class S15Factors(SpokenScene):
    def construct(self):
        b=factors(); self.add(b,label('Ca²⁺ entry through NMDA receptors',0,3.15,CALCIUM,34),label('×',-2,.25,TEXT,34),label('×',2,.25,TEXT,34))
        self.at('active terminal')
        self.play(FadeIn(label('active terminal',-4,-2.5,YELLOW,30)),GrowArrow(Arrow([-4,-2.1,0],[-4,-1.55,0],color=YELLOW,buff=0)),run_time=.5)
        self.at('other two factors')
        self.play(Indicate(b[1],scale_factor=1.02),Indicate(b[2],scale_factor=1.02),run_time=.6)
        self.at('voltage of the postsynaptic membrane')
        brace=Brace(VGroup(b[1],b[2]),DOWN,color=PINK)
        self.play(GrowFromCenter(brace),FadeIn(label('postsynaptic voltage',2,-2.5,PINK,30)),run_time=.6)
        self.finish()


class S16Detector(SpokenScene):
    def construct(self):
        v=ValueTracker(-70)
        empty=gate(False); empty[4].move_to([-4,-1.75,0])
        mg=always_redraw(lambda: plug(-2+1.8*np.clip((v.get_value()+40)/20,0,1),
            .2+2.35*np.clip((v.get_value()+40)/20,0,1)))
        self.add(empty,mg,label('No glutamate bound',-1.8,3.2,YELLOW,32),ca_meter())
        rail=Line([-5.5,-2.2,0],[.5,-2.2,0],color=PINK,stroke_width=5)
        thumb=always_redraw(lambda: Dot([-5.5+(v.get_value()+70)/70*6,-2.2,0],radius=.18,color=PINK))
        read=always_redraw(lambda: label(f'{v.get_value():.0f} mV'.replace('-','−'),-1.8,-2.85,PINK,32))
        self.add(rail,thumb,read,label('−70',-5.5,-2.8,HELP,26),label('0',.5,-2.8,HELP,26))
        self.at('no glutamate')
        # Sweep throughout the explanation, with the Ca meter held at zero.
        self.play(v.animate.set_value(-32),run_time=3.1,rate_func=linear)
        self.at('at any voltage')
        self.play(v.animate.set_value(0),run_time=3.5,rate_func=linear)
        self.at('coincidence detector')
        self.play(FadeIn(label('coincidence detector',0,-3.4,PURPLE,32)),run_time=.4)
        self.finish()


class S17Table(SpokenScene):
    def construct(self):
        self.add(label('Glutamate + voltage',0,3.25,TEXT,34))
        for y in (2.6,1.6,.05,-2.05):
            self.add(Line([-6,y,0],[6,y,0],color=GREY))
        for x in (-2.3,1.9):
            self.add(Line([x,2.6,0],[x,-2.05,0],color=GREY))
        self.add(label('−70 mV',-.2,2.1,PINK,30),label('−30 mV',4,2.1,PINK,30),label('no glutamate',-4.2,.85,YELLOW,28),label('glutamate\nbound',-4.2,-.85,YELLOW,30),label('no Ca²⁺',-.2,.85,CALCIUM,30),label('no Ca²⁺',4,.85,CALCIUM,30),model_note(-2.55))
        self.at('glutamate bound')
        self.play(Indicate(self.mobjects[10],scale_factor=1.02),
                  FadeIn(label('≈ 1 in 20\nunblocked',-.2,-1,ORANGE,30)),run_time=.4)
        self.at('Depolarize the spine')
        self.play(Indicate(self.mobjects[8],color=PINK,scale_factor=1.05),run_time=.6)
        self.at('and about one')
        self.play(FadeIn(label('≈ 1 in 3\nunblocked',4,-.7,ORANGE,30)),FadeIn(label('≈ 4× Ca²⁺ rate',4,-1.65,CALCIUM,26)),run_time=.45)
        self.finish()


class S18Predict(SpokenScene):
    def construct(self):
        f=question_frame(); f[0][-1].set_opacity(0); f[-1].set_opacity(0)
        self.add(f); d=Dot([-2.85,2.8,0],radius=.16,color=YELLOW); self.add(d)
        self.at('Glutamate arrives')
        self.play(d.animate.move_to([-2.85,1.65,0]),run_time=1)
        self.at('near rest')
        self.play(Indicate(f[2],color=PINK,scale_factor=1.08),run_time=.5)
        self.at('Does any calcium')
        self.play(f[-1].animate.set_opacity(1),run_time=.4)
        self.finish()


class S19Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(question_frame(),label('Think…',.5,1.9,GOLD,30))
        dots=VGroup(*[Dot([x,.9,0],color=GOLD,radius=.1) for x in (-.1,.5,1.1)])
        for i in range(5):
            self.play(FadeIn(dots[i%3]),run_time=.25)
            self.wait(.5)
            self.play(FadeOut(dots[i%3]),run_time=.25)


class S20Reveal(SpokenScene):
    def construct(self):
        # Exact count: twenty receptors, one open. Grid occupies 6 frame units.
        receptors=VGroup(); plugs=VGroup()
        for row in range(4):
            for col in range(5):
                x=-5+col*1.8; y=2.2-row*1.5
                receptors.add(channel(x,y,h=1.05,w=.85))
                if row!=0 or col!=4:
                    plugs.add(plug(x,y,.18))
        population_title=label('−70 mV • glutamate bound',-1.4,3.25,YELLOW,30)
        cm=ca_meter()
        self.add(receptors,plugs,population_title,cm)
        self.at('A little')
        ring=Ellipse(width=1.3,height=1.4,color=CALCIUM,stroke_width=4).move_to(receptors[4])
        self.play(FadeIn(ring),run_time=.2)
        self.play(Indicate(ring,color=CALCIUM,scale_factor=1.2),run_time=.6)
        self.at('gate is graded')
        self.play(FadeIn(label('graded, not a switch',0,-3.3,CALCIUM,32)),run_time=.5)
        self.at('a few receptors are unblocked')
        self.play(Indicate(ring,color=CALCIUM,scale_factor=1.25),FadeOut(population_title),FadeIn(label('Glutamate bound • −70 mV • 1 in 20 unblocked',0,3.25,ORANGE,28)),run_time=1.2)
        self.at('lets in a trickle')
        dots=VGroup(*[Dot([2.2,2.8+i*.15,0],color=CALCIUM,radius=.08) for i in range(4)])
        self.add(dots)
        self.play(LaggedStart(*[d.animate.shift(DOWN*1.35) for d in dots],lag_ratio=.15),run_time=.65)
        self.play(Transform(cm,ca_meter(1)),run_time=.35)
        self.finish()


def calcium_axes():
    ax=Axes(x_range=[-80,40,20],y_range=[0,5,1],x_length=10.9,y_length=4.9,tips=False,
        axis_config={'color':HELP,'include_numbers':False}).move_to([.25,-.05,0])
    labs=VGroup(label('NMDA-mediated Ca²⁺ influx rate',0,3.35,CALCIUM,34),label('relative to −70 mV',-3.6,2.8,HELP,26),label('spine voltage (mV)',0,-3.2,HELP,28))
    for n in (-80,-60,-40,-20,0,20,40):
        labs.add(T(str(n).replace('-','−'),size=26,color=HELP).move_to(ax.c2p(n,0)+DOWN*.32))
    for n in (0,1,2,3,4,5):
        labs.add(T(str(n),size=26,color=HELP).move_to(ax.c2p(-80,n)+LEFT*.35))
    return ax,labs


def curve_label(text,x,y,point):
    t=label(text,x,y,GOLD,26).add_background_rectangle(color=BG,opacity=1,buff=.12)
    direction=point-t.get_center()
    start=t.get_boundary_point(direction)
    line=Line(start,point,color=GOLD,buff=.08,stroke_width=2)
    return VGroup(line,t).set_z_index(5)


class S21Curve(SpokenScene):
    def construct(self):
        ax,labs=calcium_axes(); ax.y_axis.set_opacity(0)
        self.add(ax,labs,Line(ax.c2p(-80,0),ax.c2p(-80,5),color=HELP),label('illustrative model • 1 mM external Mg²⁺',0,-3.65,HELP,26))
        peak=float(np.linspace(-80,40,2401)[np.argmax([entry(v) for v in np.linspace(-80,40,2401)])])
        def curve(a,b):
            return ax.plot(lambda v:entry(v)/entry(-70),x_range=[a,b,.3],color=CALCIUM,stroke_width=5,use_smoothing=False)
        self.at('more depolarization')
        self.play(Create(curve(-80,-70)),run_time=1)
        self.play(FadeIn(Dot(ax.c2p(-70,1),color=GOLD)),FadeIn(curve_label('−70: 1.0',-5.15,-.55,ax.c2p(-70,1))),run_time=.4)
        self.at('In this model')
        self.play(Create(curve(-70,-30)),run_time=2.5,rate_func=linear)
        self.play(FadeIn(Dot(ax.c2p(-30,entry(-30)/entry(-70)),color=GOLD)),FadeIn(curve_label('−30: 3.8',-2.45,1.8,ax.c2p(-30,entry(-30)/entry(-70)))),run_time=.4)
        self.at('calcium entry')
        self.play(Create(curve(-30,peak)),run_time=1.4,rate_func=linear)
        self.at('peaks near')
        self.play(FadeIn(Dot(ax.c2p(peak,entry(peak)/entry(-70)),color=GOLD)),FadeIn(label('peak ≈ −20 mV',1.7,2.8,GOLD,28)),run_time=.5)
        self.at('then falls')
        self.play(Create(curve(peak,40)),run_time=.8,rate_func=linear)
        self.add(curve_label('+40: 0.65',4.35,.35,ax.c2p(40,entry(40)/entry(-70))))
        self.finish()


class S22Why(SpokenScene):
    def construct(self):
        self.add(label('Third factor: inward push on Ca²⁺',0,3.25,CALCIUM,34))
        for x,v in [(-3,-70),(3,-30)]:
            self.add(channel(x,.1,h=3.6,w=2.4),label('−70 mV' if v==-70 else '−30 mV',x,-2.8,PINK,34),plug(x+1.4,2.25,.25))
        self.add(label('Mg²⁺ cleared • compare open pores',0,2.8,ORANGE,28))
        h1=4; h2=h1*inward(-30)/inward(-70)
        a=Arrow([-3,2.1,0],[-3,2.1-h1,0],color=CALCIUM,buff=0,stroke_width=9)
        b=Arrow([3,2.1,0],[3,2.1-h1,0],color=CALCIUM,buff=0,stroke_width=9)
        self.add(a,b)
        self.at('Depolarization weakens')
        self.play(Transform(b,Arrow([3,2.1,0],[3,2.1-h2,0],color=CALCIUM,buff=0,stroke_width=9)),run_time=2)
        self.finish()


# The rate chart uses unit=1 to fill its frame. The accumulation view uses
# compressed drawing units and explicitly marks its rescaled rate reference.
BASE=-2.3
UNIT=.25
SCHEMATIC_ACCUMULATION=float(sum(entry(v)/entry(-70) for v in np.linspace(-70,-30,7)))

def rate_axis(x=-4.7,unit=UNIT):
    g=VGroup(Line([x,BASE,0],[x,2.7,0],color=HELP),Line([x,BASE,0],[5.4,BASE,0],color=HELP))
    for n in (0,1,4):
        g.add(label(str(n),x-.45,BASE+n*unit,HELP,26),Line([x-.1,BASE+n*unit,0],[x+.1,BASE+n*unit,0],color=HELP))
    return g


def bar(x,n,w=1.5,unit=UNIT):
    h=max(.01,n*unit)
    return Rectangle(width=w,height=h,color=CALCIUM,fill_color=CALCIUM,fill_opacity=.8).move_to([x,BASE+h/2,0])


class S23Four(SpokenScene):
    def construct(self):
        self.add(label('Ca²⁺ entry rate (relative to −70 mV)',0,3.2,CALCIUM,32),rate_axis(unit=1),label('same receptor • steady-flux model',0,2.6,HELP,28))
        self.at('for the same receptor')
        self.play(GrowFromEdge(bar(-1.5,1,unit=1),DOWN),FadeIn(label('−70 mV',-1.5,-2.8,PINK,30)),run_time=.5)
        self.at('minus 30 instead')
        self.play(GrowFromEdge(bar(2.5,entry(-30)/entry(-70),unit=1),DOWN),FadeIn(label('−30 mV',2.5,-2.8,PINK,30)),run_time=.7)
        self.at('about four times')
        self.play(FadeIn(label('≈ 4×',2.5,1.95,CALCIUM,34)),run_time=.6)
        self.at('Where does the big difference')
        self.play(FadeIn(label('Where does the big difference come from?',0,-3.45,GOLD,28)),run_time=.5)
        self.finish()


def train_layout():
    channels=VGroup(*[channel(x,-.1,h=3.5,w=1.3) for x in (-4.7,-2.8,-.9)])
    for c in channels: c[1].set_z_index(1)
    pulses=VGroup(*[Line([x,2.3,0],[x,2.85,0],color=TEXT,stroke_width=4) for x in np.linspace(-5.6,.0,12)])
    return VGroup(channels,pulses,label('100 Hz • 10 ms between inputs',-2.8,3.35,TEXT,28),label('NMDA receptors',-2.8,-2.35,PURPLE,30),label('schematic summation • time slowed',-2.8,-3.25,HELP,26))


class S24Sum(SpokenScene):
    def construct(self):
        tr=train_layout(); vm=voltage_meter(-70,3.5)
        self.add(tr[0],tr[1],tr[2],tr[3],tr[4],vm)
        self.at('Mainly from summation')
        self.play(Indicate(tr[0],color=PURPLE,scale_factor=1.01),run_time=.7)
        self.at('During a fast train')
        self.play(LaggedStart(*[Indicate(p,color=YELLOW,scale_factor=1.15) for p in tr[1]],lag_ratio=.1),run_time=1.1)
        self.at('glutamate keeps arriving')
        for j in range(3):
            ds=VGroup(*[Dot([x,1.9,0],radius=.14,color=YELLOW) for x in (-5.1,-3.2,-1.3)]).set_z_index(2)
            self.add(ds)
            self.play(ds.animate.shift(DOWN*(.2+j*.15)),tr[0][j][0].animate.set_fill(PURPLE,.8),Transform(vm,voltage_meter(-60+j*10,3.5)),run_time=.65)
        self.at('depolarization builds')
        self.play(Transform(vm,voltage_meter(-30,3.5)),run_time=1.3)
        self.finish()


class S25Steep(SpokenScene):
    def construct(self):
        tr=train_layout()
        for c in tr[0]: c[0].set_fill(PURPLE,.8)
        self.add(tr[0],tr[1],tr[2],tr[3],label('spine voltage ≈ −30 mV',-2.8,-3.25,PINK,28))
        # The previous rate chart is compressed here to make room for accumulation.
        # The reference is a drawing comparison, not concentration units.
        self.add(label('Ca²⁺ in spine',3.6,3.35,CALCIUM,30),label('schematic accumulation',3.6,2.8,HELP,26),
                 Rectangle(width=1.2,height=4.8,color=CALCIUM).move_to([3.6,.1,0]),
                 DashedLine([2.7,BASE+4*UNIT,0],[4.5,BASE+4*UNIT,0],color=HELP),label('4× rate reference\n(rescaled)',4,-2.85,HELP,26),
                 Brace(Line([4.5,BASE+4*UNIT,0],[4.5,2.5,0]),RIGHT,color=HELP).set_opacity(.35),
                 label('headroom\nfor later',5.7,1,HELP,22).set_opacity(.6))
        fill=bar(3.6,1,w=1); self.add(fill)
        ds=VGroup(*[Dot([x,1.5,0],radius=.16,color=YELLOW) for x in (-5.1,-3.2,-1.3)]).set_z_index(2)
        self.at('receptors stay activated')
        self.play(FadeIn(ds),AnimationGroup(*[c[0].animate.set_fill(PURPLE,.95) for c in tr[0]]),run_time=1.2)
        self.at('responses summate')
        self.play(Transform(fill,bar(3.6,4,w=1)),ds.animate.shift(DOWN*.2),run_time=1.2)
        self.at('calcium in the spine')
        self.play(Transform(fill,bar(3.6,SCHEMATIC_ACCUMULATION,w=1)),run_time=1.9)
        self.finish()


class S26Takeaway(SpokenScene):
    def construct(self):
        self.add(label('NMDA • normal extracellular Mg²⁺',0,3.05,PURPLE,38))
        a=VGroup(RoundedRectangle(width=4.8,height=1.65,corner_radius=.2,color=YELLOW,fill_opacity=.12),
                 label('glutamate',color=YELLOW,size=44).move_to(ORIGIN)).move_to([-3.2,.8,0])
        b=VGroup(RoundedRectangle(width=5.4,height=1.65,corner_radius=.2,color=PINK,fill_opacity=.12),
                 label('depolarization',color=PINK,size=42).move_to(ORIGIN)).move_to([3,.8,0])
        self.at('normal magnesium levels')
        self.play(FadeIn(a),FadeIn(b),run_time=.6)
        self.at('a receptor')
        self.play(GrowArrow(Arrow([-3.2,-.15,0],[0,-1.75,0],color=YELLOW)),
                  GrowArrow(Arrow([3,-.15,0],[0,-1.75,0],color=PINK)),run_time=.7)
        self.at('glutamate and depolarization coincide')
        self.play(Indicate(a,scale_factor=1.03),Indicate(b,scale_factor=1.03),run_time=.6)
        self.play(FadeIn(label('much Ca²⁺',0,-2.6,CALCIUM,54)),run_time=.5)
        self.finish()


class S27End(EndCard):
    LINE='At normal magnesium,\nsubstantial calcium entry needs\nglutamate and depolarization together.'

    def construct(self):
        line=T(self.LINE,size=44,font=TITLE_FONT,line_spacing=1.5)
        fit(line,max_w=12)
        sub=T('biochemistrypedia.com',size=24,color=TEAL)
        VGroup(line,sub).arrange(DOWN,buff=.65)
        self.play(FadeIn(line,shift=UP*.15),run_time=self.beat(.3))
        self.play(FadeIn(sub),run_time=self.beat(.15))
        self.finish()
