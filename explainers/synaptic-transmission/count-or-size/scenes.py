"""Count or size: reviewer fix round.

COLOR MAP: BLUE terminal/stimulus; YELLOW count/ACh/vesicle filling;
GREEN voltage response; TEAL calcium/junction; PINK size/receptors;
ORANGE threshold; RED antibodies/failure/block; GREY muscle/axes.
All bars use the steady-state model, all traces use normalized double
exponentials. Calcium/train models are explicitly illustrative cartoons.
"""
import numpy as np
from bp_style import *
ORANGE = '#F29E4C'
PINK = '#E88FC0'


def label(s, x=0, y=3.15, size=30, color=TEXT):
    return T(s, size, color).move_to([x, y, 0])


def response(k, q):
    return 90*k*q/(90+k*q)


def arrow(a, b, color=YELLOW, w=5):
    return Arrow(a, b, buff=.06, color=color, stroke_width=w)


def backed(s, x, y, size=26, color=ORANGE):
    t = label(s, x, y, size, color)
    t.add_background_rectangle(color=BG, opacity=1, buff=.07)
    return t


def fibre(x=0, y=0, w=5, h=2.5):
    body = RoundedRectangle(width=w, height=h, corner_radius=.25,
        stroke_color=GREY, fill_color=GREY, fill_opacity=.16).move_to([x,y,0])
    bands = VGroup(*[Line([x+dx,y-h*.35,0], [x+dx,y+h*.35,0],
        color=GREY, stroke_opacity=.35) for dx in np.linspace(-w/2+.4,w/2-.4,7)])
    return VGroup(body, bands)


def formula():
    box = RoundedRectangle(width=11.8, height=5.4, corner_radius=.25, color=GREY)
    words = VGroup(label('response',-4.1,.8,40,GREEN), label('≈',-1.9,.8,40),
        label('count (k)',.05,.8,40,YELLOW), label('×',2.25,.8,40),
        label('size (q)',4.25,.8,40,PINK))
    return VGroup(box,words)


def glosses():
    return VGroup(label('count: how many packets on this impulse',0,-.5,30,YELLOW),
        label('size: response to one packet',0,-1.35,30,PINK),
        label('A small-response approximation',0,-2.15,26,GREY))


# Same scale and baselines in s07–s14, including the rescue comparison.
BASE = -1.35
SCALE = .185


def panel(x, q, ks=(60,45), width=4.8, first_only=False, ghost=None):
    left, right = x-width/2, x+width/2
    axes = VGroup(Line([left,BASE,0],[right,BASE,0],color=GREY),
        Line([left,BASE,0],[left,BASE+20*SCALE,0],color=GREY))
    for v in (0,10,20):
        y = BASE+v*SCALE
        axes.add(Line([left-.09,y,0],[left,y,0],color=GREY),label(str(v),left-.35,y,26,GREY))
    y = BASE+12*SCALE
    th = VGroup(DashedLine([left,y,0],[right,y,0],color=ORANGE),
        backed('12 mV threshold (illustrative)',x,2.4,22))
    bars, values, names = VGroup(), VGroup(), VGroup()
    for i,k in enumerate(ks):
        bx = left+1.25+i*2.0
        h = response(k,q)*SCALE
        bar = Rectangle(width=.85,height=h,stroke_width=0,
            fill_color=GREEN if response(k,q)>=12 else RED,fill_opacity=.9).move_to([bx,BASE+h/2,0])
        bars.add(bar)
        values.add(label(f'{response(k,q):.1f}',bx,BASE+h+(.28 if response(k,q)>=12 else -.3),28,GREEN if response(k,q)>=12 else TEXT))
        if response(k,q) > 16:
            values[-1].move_to([bx,BASE+h-.3,0]).set_color(TEXT)
        if ghost is not None and i == 1:
            # Place the rescued value beside both bar outlines.
            values[-1].move_to([bx+.92,BASE+h-.28,0])
        names.add(label(('first' if i==0 else 'later')+f' · {k}',bx,BASE-.35,26,YELLOW))
    outlines = VGroup()
    if ghost is not None:
        for i,k in enumerate(ks):
            h=response(k,ghost)*SCALE
            outlines.add(Rectangle(width=1.04,height=h,color=PINK,stroke_width=2,
                fill_opacity=0).move_to([left+1.25+i*2,BASE+h/2,0]))
    if first_only:
        for g in (bars,values,names):
            g[1:].set_opacity(0)
    return VGroup(axes,th,bars,values,names,outlines)


def comparison(first_only=False, later_k=45, restored=False):
    n=panel(-3.15,.4,(60,later_k),first_only=first_only)
    m=panel(3.05,.27 if restored else .24,(60,later_k),first_only=first_only,
        ghost=.24 if restored else None)
    heading=VGroup(label('normal · size 0.40',-3.15,2.85,28,GREEN),
        label('myasthenic · size '+('0.27' if restored else '0.24'),3.05,2.85,28,PINK),
        label('response above rest (mV)',0,3.4,28,GREEN),
        label('count (k): packets on each impulse · illustrative model',0,-2.15,26,YELLOW))
    return VGroup(n,m,heading)


def firing():
    return VGroup(fibre(-3.1,-2.95,4.8,.75),fibre(3.05,-2.95,4.8,.75),
        backed('muscle: fires → fires',-3.1,-2.95,26,GREEN),
        backed('muscle: fires → fails',3.05,-2.95,26,RED))


def train(ks, q=.4, title=''):
    # Large six-impulse chart shared by rapid and slow examples.
    left,right,base,sc=-5.45,5.8,-2.25,.215
    ax=VGroup(Line([left,base,0],[right,base,0],color=GREY),
        Line([left,base,0],[left,base+20*sc,0],color=GREY))
    for v in (0,10,20):
        ax.add(label(str(v),left-.4,base+v*sc,26,GREY))
    th=VGroup(DashedLine([left,base+12*sc,0],[right,base+12*sc,0],color=ORANGE),
        backed('12 mV · illustrative threshold',-2.4 if max(response(k,q) for k in ks)<12 else 2.8,base+12*sc,26))
    bars=VGroup()
    for i,k in enumerate(ks):
        h=response(k,q)*sc
        bars.add(Rectangle(width=.7,height=h,fill_color=GREEN if response(k,q)>=12 else RED,
            fill_opacity=.9,stroke_width=0).move_to([-4.45+i*1.85,base+h/2,0]))
        ax.add(label(str(i+1),-4.45+i*1.85,base-.35,26,GREY))
    return VGroup(ax,th,bars,label(title,0,3.3,32,BLUE),
        label('response above rest (mV)',0,2.65,28,GREEN),
        label('impulse number →',0,-2.95,26,GREY))


def synapse(few=False):
    terminal=RoundedRectangle(width=11.2,height=1.95,corner_radius=.35,
        color=BLUE,fill_color=BLUE,fill_opacity=.12).move_to([0,1.65,0])
    muscle=fibre(0,-1.85,11.2,2.25)
    rec=VGroup()
    for x in ((-3,3) if few else (-3,-1,1,3)):
        rec.add(VGroup(Line([x-.2,-.55,0],[x-.2,-1.05,0],color=PINK,stroke_width=7),
            Line([x+.2,-.55,0],[x+.2,-1.05,0],color=PINK,stroke_width=7),
            Line([x-.2,-1.05,0],[x+.2,-1.05,0],color=PINK,stroke_width=7)))
    names=VGroup(label('nerve terminal',0,2.1,28,BLUE),label('muscle fibre',0,-2.45,28,GREY),
        label('acetylcholine receptors',0,-1.65,28,PINK),
        Line([-2.35,-1.65,0],[-3,-1.65,0],color=PINK),
        Line([-3,-1.65,0],[-3,-1.12,0],color=PINK))
    return VGroup(terminal,muscle,rec,names)


def antibody(x,y):
    return VGroup(Line([x,y-.3,0],[x,y,0],color=RED,stroke_width=6),
        Line([x,y,0],[x-.24,y+.22,0],color=RED,stroke_width=6),
        Line([x,y,0],[x+.24,y+.22,0],color=RED,stroke_width=6))


def trace(amp=1,x=-1,y=-1.3,w=6,events=(.35,1.35,2.35)):
    f=lambda t: np.exp(-t/.22)-np.exp(-t/.04)
    peak=max(f(t) for t in np.linspace(.001,1,400))
    xs=np.linspace(0,3,500)
    pts=[[x+t*w/3,y+amp*sum(f(t-b)/peak if t>=b else 0 for b in events),0] for t in xs]
    return VMobject(color=GREEN,stroke_width=4).set_points_as_corners(pts)


def prediction():
    pulses=VGroup(*[Line([x,-1.9,0],[x,.2,0],color=BLUE,stroke_width=5) for x in np.linspace(-5.4,5.4,11)])
    return VGroup(label('20 Hz · rapid stimulation',0,3.1,34,BLUE),
        label('What happens to the count',0,1.95,36,YELLOW),label('during the train?',0,1.15,36,YELLOW),
        pulses,label('50 ms between impulses',0,-2.55,28,GREY),label('Pause and predict',0,-3.25,30,TEAL))


def ca_dots(n=9, y=1.2):
    return VGroup(*[Dot([-2.4+(i%5)*1.1,y-(i//5)*.55,0],radius=.13,color=TEAL) for i in range(n)])


def calcium_scene():
    box=RoundedRectangle(width=11,height=4.3,corner_radius=.35,color=BLUE,
        fill_color=BLUE,fill_opacity=.1).move_to([0,.2,0])
    ticks=VGroup(*[VGroup(Line([x,-1.2,0],[x,-.55,0],color=BLUE,stroke_width=5),
        label(str(i+1),x,-1.6,26,BLUE)) for i,x in enumerate((-4.3,-1.5,1.5,4.3))])
    return VGroup(box,label('terminal · calcium (Ca²⁺)',0,2.75,32,TEAL),ticks,
        label('impulses →',0,-2.35,28,BLUE),label('20 Hz · calcium left over adds up',0,-3.15,28,TEAL))


def table(rows=0):
    # Persistent skeleton, consistent row positions, room for caution and assumptions.
    skeleton=VGroup(label('Recording → mechanism',0,3.25,36),
        label('recording',-3.4,2.45,30),label('points to',2.7,2.45,30),
        Line([-6,2,0],[6,2,0],color=GREY),Line([-6,-.05,0],[6,-.05,0],color=GREY),
        Line([-6,-2,0],[6,-2,0],color=GREY),Line([.1,2,0],[.1,-2,0],color=GREY),
        label('myasthenia gravis',-3.25,1.55,30,PINK),label('Lambert-Eaton',-3.25,-.5,30,BLUE))
    row1=VGroup(label('size down',-3.25,.95,32,PINK),label('count normal',-3.25,.35,30,YELLOW),
        label('size side',2.9,1.5,34,PINK),label('receptors or',2.9,.95,28),label('vesicle filling',2.9,.4,28))
    row2=VGroup(label('count down',-3.25,-1.1,32,YELLOW),label('size normal',-3.25,-1.65,30,PINK),
        label('count side',2.9,-.7,34,YELLOW),label('release from terminal',2.9,-1.4,28,BLUE))
    note=VGroup(label('Assumes resting potential, membrane properties',0,-2.5,26,GREY),
        label('and recording site unchanged',0,-3,26,GREY))
    if rows<1: row1.set_opacity(0); note.set_opacity(0)
    if rows<2: row2.set_opacity(0)
    return VGroup(skeleton,row1,row2,note)


def electrical():
    cells=VGroup(*[RoundedRectangle(width=5,height=3.9,corner_radius=.4,
        color=c,fill_color=c,fill_opacity=.12).move_to([x,.55,0]) for x,c in ((-3,BLUE),(3,GREY))])
    channel=Rectangle(width=1.25,height=.8,color=TEAL,fill_color=BG,fill_opacity=1).move_to([0,.35,0])
    names=VGroup(label('electrical synapse',0,3.15,36),label('cell 1',-3,1.85,30,BLUE),
        label('cell 2',3,1.85,30,GREY),label('no vesicles',-3,-.9,28),label('no vesicles',3,-.9,28),
        label('gap junction',0,-1.95,28,TEAL),Line([0,-1.6,0],[0,-.05,0],color=TEAL))
    return VGroup(cells,channel,names)


class S00Title(TitleCard):
    TITLE='Count or Size? Two Weaknesses and a Synapse with No Packets'
    LESSON='Synaptic Transmission and Quantal Release'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.85,26,TEAL),label(self.LESSON,0,2.15,28,GREY))
        title=VGroup(T('Count or Size?',48,font=TITLE_FONT),T('Two Weaknesses and a',36,font=TITLE_FONT),
            T('Synapse with No Packets',36,font=TITLE_FONT)).arrange(DOWN,buff=.3)
        self.play(FadeIn(title),run_time=.6)
        self.add(Line([-1,-2,0],[1,-2,0],color=GOLD)); self.wait(self.narration_s-.6)


class S01Question(SpokenScene):
    def construct(self):
        self.add(label('How can a recording tell them apart?',0,3.1,36),
            fibre(-3.1,-.2,5.4,4.4),fibre(3.1,-.2,5.4,4.4),
            label('disease A',-3.1,1.25,34),label('disease B',3.1,1.25,34))
        self.at('muscles weak'); self.play(FadeIn(VGroup(label('weak',-3.1,-.2,42,RED),label('weak',3.1,-.2,42,RED))),run_time=.4)
        self.at('How can'); self.play(FadeIn(VGroup(label('?',-3.1,-1.5,48,YELLOW),label('?',3.1,-1.5,48,YELLOW))),run_time=.4)
        self.finish()


class S02Rule(SpokenScene):
    def construct(self):
        f=formula(); self.add(f)
        g=glosses()
        self.at('The response'); self.play(Indicate(f[1][0],color=GREEN),run_time=.4)
        self.at('roughly count'); self.play(FadeIn(g[0]),run_time=.35)
        self.at('size'); self.play(FadeIn(g[1:]),run_time=.35)
        self.finish()


class S03Below(SpokenScene):
    def construct(self):
        p=train((60,56,52,48,45,38),q=.24,title='When the response falls short')
        self.add(p)
        self.at('falls below'); self.play(Indicate(p[1],color=ORANGE),run_time=.5)
        self.at('to fire'); self.play(Indicate(p[2][1:],color=RED),run_time=.4)
        self.finish()


class S04Mg(SpokenScene):
    def construct(self):
        s=synapse(); self.add(s,label('myasthenia gravis',0,3.3,34,PINK))
        ab=VGroup(antibody(-5,.05),antibody(-4,.05))
        source=label('antibodies in blood',-3.8,.1,28,RED)
        self.at('antibodies in'); self.play(FadeIn(source),run_time=.3)
        self.play(FadeOut(source),FadeIn(ab),run_time=.3)
        self.at('target the'); self.play(Transform(ab,VGroup(antibody(-3,-.25),antibody(3,-.25))),run_time=.7)
        self.play(s[2][1:3].animate.set_opacity(.12),run_time=.5)
        self.finish()


class S05Smaller(SpokenScene):
    def construct(self):
        s=synapse(); s[2][1:3].set_opacity(.12)
        ab=VGroup(antibody(-3,-.25),antibody(3,-.25))
        self.add(s,ab,label('myasthenia gravis · size falls',0,3.3,32,PINK))
        self.at('Fewer receptors'); self.play(Indicate(s[2][::3],color=PINK),run_time=.5)
        f=formula()
        # A shallow card covers only the terminal, retaining the reduced receptor picture.
        f[0].stretch_to_fit_height(1.55).move_to([0,1.7,0]).set_fill(BG,opacity=1)
        f[1].shift(UP*.9)
        self.at('a smaller'); self.play(FadeIn(f),run_time=.4)
        self.play(f[1][4].animate.scale(.82),run_time=.25)
        self.add(label('size (q) ↓ · response to one packet',0,-3.45,30,PINK))
        self.finish()


class S06Toyka(SpokenScene):
    def construct(self):
        self.add(label('Patient-serum immunoglobulin → mouse',0,3.3,32))
        tube=VGroup(RoundedRectangle(width=.65,height=1.1,corner_radius=.1,color=GREY),
            Rectangle(width=.5,height=.55,fill_color=RED,fill_opacity=.5,stroke_width=0).shift(DOWN*.2)).move_to([-4.6,2.3,0])
        # Filled profile: pointed snout, round ear, eye, feet and a long curved tail.
        body=Ellipse(width=1.3,height=.55,stroke_color=GREY,fill_color=GREY,fill_opacity=1)
        head=Polygon([.4,.18,0],[.76,.13,0],[.99,-.05,0],[.52,-.2,0],
            color=GREY,fill_opacity=1)
        ear=Circle(radius=.16,color=GREY,fill_opacity=1).move_to([.5,.28,0])
        eye=Dot([.74,.06,0],radius=.035,color=BG)
        feet=VGroup(*[Line([x,-.2,0],[x+.16,-.31,0],color=GREY,stroke_width=5) for x in (-.35,.3)])
        tail=VMobject(color=PINK,stroke_width=3).set_points_smoothly(
            [[-.6,0,0],[-.9,.05,0],[-1.15,.3,0],[-1.4,.22,0]])
        mouse=VGroup(body,head,ear,eye,feet,tail).move_to([-1.5,2.45,0])
        syringe=VGroup(Rectangle(width=.8,height=.23,color=RED),Line([.4,0,0],[.85,0,0],color=GREY)).move_to([-3.6,2.1,0])
        self.add(tube,mouse,label('mouse',.4,2.45,28,GREY),syringe)
        # Labelled columns retain the control throughout the transfer.
        for x,name in ((-3.1,'control'),(3.1,'serum-treated')):
            self.add(RoundedRectangle(width=5.7,height=4.7,corner_radius=.2,color=GREY).move_to([x,-.65,0]),
                label(name,x,1.15,32),label('receptors (R)',x,.45,28,PINK))
        rec=VGroup(*[chip('R',PINK,28).move_to([-4.5+i*1.3,-.25,0]) for i in range(3)])
        control=trace(.75,x=-5.35,y=-2.25,w=4.4)
        self.add(rec,control,label('miniature endplate potentials',0,-3.35,30,GREEN))
        self.at('moved into'); self.play(syringe.animate.shift(RIGHT*1.2),run_time=.55)
        r2=rec.copy().shift(RIGHT*6.2); tr=trace(.75,x=.85,y=-2.25,w=4.4)
        self.play(FadeIn(r2),Create(tr),run_time=.45)
        self.at('smaller miniatures'); self.play(Transform(tr,trace(.38,x=.85,y=-2.25,w=4.4)),run_time=.5)
        self.at('fewer receptors'); self.play(FadeOut(r2[1:]),run_time=.4)
        self.finish()


class S07First(SpokenScene):
    def construct(self):
        p=panel(-3.1,.4,first_only=True)
        self.add(p,label('response above rest (mV)',-2.9,3.35,28,GREEN),
            label('normal · size (q) = 0.40 mV',-2.9,2.85,28,PINK),
            label('steady-state model',3.1,2.5,30),label('driving force: 90 mV',3.1,1.8,28,GREY),
            label('fixed packet count',3.1,-2,28,GREY))
        self.at('the first impulse'); self.play(FadeIn(label('count (k) = 60 packets',3.1,.9,30,YELLOW)),run_time=.4)
        self.at('Cut the size'); self.play(Transform(p,panel(-3.1,.24,first_only=True)),
            FadeIn(backed('myasthenic · size (q) = 0.24 mV',-2.9,2.85,28,PINK)),run_time=.6)
        self.at('that response still'); self.play(FadeIn(VGroup(label('12.4 mV · model response',3.1,0,30,GREEN),
            label('what the membrane reaches',3.1,-.65,26,GREY))),run_time=.4)
        self.at('but barely'); self.play(Indicate(p[2][0],color=ORANGE),run_time=.4)
        self.finish()


class S08Rundown(SpokenScene):
    def construct(self):
        c=comparison(first_only=True); self.add(c)
        moving=comparison(later_k=60)
        # Reveal a copy of the initial response, then shrink the later state.
        self.at('release runs down'); self.play(Transform(c,moving),run_time=.7)
        count=label('count (k): 60 packets',0,-3.05,32,YELLOW); self.add(count)
        self.at('a quarter fewer'); self.play(Transform(c,comparison()),
            Transform(count,label('count (k): 60 → 45 packets · 25% fewer',0,-3.05,32,YELLOW)),run_time=1)
        self.finish()


class S09Fails(SpokenScene):
    def construct(self):
        c=comparison(); f=firing(); self.add(c,f)
        self.at('The normal'); self.play(f[0].animate.stretch(.85,0),run_time=.25)
        self.play(f[0].animate.stretch(1/.85,0),run_time=.25)
        self.at('drops below threshold'); self.play(Indicate(c[1][2][1],color=RED),run_time=.5)
        self.at('and fails'); self.play(f[1].animate.set_color(RED),run_time=.3)
        self.at('Real counts'); self.play(FadeOut(c[2][2]),FadeIn(label('Real counts fluctuate around their mean (m)',0,3.4,28,GREY)),run_time=.4)
        self.at('can fail even');
        example=VGroup(RoundedRectangle(width=11.8,height=.55,corner_radius=.12,color=RED,fill_color=BG,fill_opacity=1),
            label('Hypothetical early impulse: 56 packets → 11.7 mV · fails',0,0,26,RED)).move_to([0,-2.22,0])
        self.play(FadeIn(example),run_time=.4)
        self.finish()


class S10Fatigue(SpokenScene):
    def construct(self):
        c=comparison(); f=firing(); self.add(c,f)
        self.at('This is'); self.play(Transform(c[2][2],label('fatigable weakness',0,3.4,32,RED)),run_time=.4)
        self.at('work at first'); self.play(Indicate(c[1][2][0],color=GREEN),run_time=.5)
        self.at('weaken with'); self.play(Indicate(c[1][2][1],color=RED),run_time=.4)
        self.finish()


class S11Drug(SpokenScene):
    def construct(self):
        s=synapse(few=True); self.add(s)
        self.add(label('drug: blocks acetylcholinesterase',0,3.3,32,RED))
        enzyme=chip('acetylcholinesterase',GREY,28).move_to([0,.05,0])
        cross=VGroup(Line([0,0,0],[.38,.38,0],color=RED,stroke_width=6),
            Line([0,.38,0],[.38,0,0],color=RED,stroke_width=6)).next_to(enzyme,RIGHT,buff=.12)
        self.add(enzyme)
        self.at('Drugs that block'); self.play(Create(cross),run_time=.45)
        ach=VGroup(*[Dot([x,1.1,0],radius=.09,color=YELLOW) for x in (-3.3,-3,-2.7,2.7,3,3.3)])
        self.at('let each'); self.play(FadeIn(ach),run_time=.3)
        self.play(ach.animate.shift(DOWN*.95),run_time=.45)
        self.at('acetylcholine last'); self.play(Transform(s[3][0],label('acetylcholine (ACh) · one packet released',0,2.1,28,YELLOW)),run_time=.35)
        self.play(ach.animate.shift(DOWN*.35),run_time=.4)
        self.add(label('ACh remains in the cleft',0,-3.45,28,YELLOW))
        self.play(ach.animate.shift(LEFT*.12),run_time=.45)
        self.play(ach.animate.shift(RIGHT*.24),run_time=.45)
        self.finish()


class S12Restore(SpokenScene):
    def construct(self):
        s=synapse(few=True); self.add(s,label('ACh lingers · remaining receptors',0,3.3,32,YELLOW))
        ach=VGroup(*[Dot([x,-.2,0],radius=.1,color=YELLOW) for x in (-3.2,-2.8,2.8,3.2)]); self.add(ach)
        self.at('It reaches more'); self.play(ach.animate.shift(DOWN*.4),run_time=.6)
        c=comparison()
        notes=VGroup(label('illustrative · size partly restored',0,-2.8,30,PINK),
            label('pink outlines: before drug',0,-3.35,26,PINK))
        self.at('That raises'); self.play(FadeOut(Group(*self.mobjects)),FadeIn(c),FadeIn(notes),run_time=.4)
        self.at('part of the way'); self.play(Transform(c,comparison(restored=True)),run_time=.6)
        self.finish()


class S13Le(SpokenScene):
    def construct(self):
        s=synapse(); self.add(s,label('Lambert-Eaton syndrome',0,3.3,34,BLUE))
        ca=VGroup(*[Dot([x,-.1,0],radius=.1,color=TEAL) for x in (-3,-1,1,3)])
        self.add(ca,label('calcium entry ↑',0,.25,28,TEAL))
        self.at('the fault'); self.play(s[0].animate.set_stroke(GOLD,7),ca.animate.shift(UP*1.2),run_time=.6)
        self.finish()


class S14Lowcount(SpokenScene):
    def construct(self):
        s=synapse(); self.add(s,label('Lambert-Eaton · calcium entry reduced',0,3.3,32,BLUE))
        ch=VGroup(*[Rectangle(width=.6,height=.4,color=TEAL,fill_color=BG,fill_opacity=1).move_to([x,.68,0]) for x in (-3,3)])
        ab=VGroup(antibody(-3,.25),antibody(3,.25))
        self.add(ch,label('Ca²⁺ channels',0,1.3,28,TEAL))
        self.at('Antibodies against'); self.play(FadeIn(ab),run_time=.4)
        ca=VGroup(*[Dot([x,-.15,0],radius=.12,color=TEAL) for x in (-3.45,-2.55,2.55,3.45)])
        stops=VGroup(*[Line([x-.22,.4,0],[x+.22,.4,0],color=RED,stroke_width=5) for x in (-3.45,-2.55,2.55,3.45)])
        self.at('cut calcium entry'); self.play(FadeIn(ca),run_time=.3)
        self.play(ca.animate.shift(UP*.38),FadeIn(stops),run_time=.35)
        self.play(ca.animate.shift(DOWN*.18),run_time=.35)
        self.add(label('Ca²⁺ stopped outside',0,-.15,28,TEAL))
        self.at('So the count'); self.play(FadeOut(Group(*self.mobjects)),run_time=.2)
        p=panel(-2.7,.4,(20,20)); self.add(p,
            label('response above rest (mV)',-2.7,3.4,28,GREEN),label('low count from the start',-2.7,2.85,30,YELLOW),
            label('count (k): 20 packets',3.25,1.85,30,YELLOW),label('size (q): 0.40 mV',3.25,1,30,PINK),
            label('7.3 mV · model',3.25,.15,32,RED),label('outline: normal count 60',2.65,-2.7,28,GREY))
        h=response(60,.4)*SCALE
        ghost=Rectangle(width=1.05,height=h,color=GREY,stroke_width=2).move_to([-3.85,BASE+h/2,0]); self.add(ghost)
        self.finish()


class S15Predict(SpokenScene):
    def construct(self):
        p=prediction(); self.add(p[0:3],p[4:])
        self.at('stimulate rapidly'); self.play(LaggedStart(*[FadeIn(l) for l in p[3]],lag_ratio=.1),run_time=1.2)
        self.at('What happens'); self.play(Indicate(p[1:3],color=YELLOW),run_time=.5)
        self.finish()


class S16Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(prediction()); self.wait(5)


class S17Reveal(SpokenScene):
    def construct(self):
        s=calcium_scene(); dots=ca_dots(12); self.add(s)
        self.at('It rises'); self.play(FadeIn(label('count ↑',4.3,1.1,34,YELLOW)),run_time=.3)
        self.at('Calcium leftover'); self.play(FadeIn(dots[:3]),Indicate(s[2][0],color=BLUE),run_time=.4)
        self.at('from one impulse'); self.play(FadeIn(dots[3:6]),Indicate(s[2][1],color=BLUE),run_time=.4)
        self.at('adds to'); self.play(FadeIn(dots[6:9]),Indicate(s[2][2],color=BLUE),run_time=.4)
        self.play(FadeIn(dots[9:]),Indicate(s[2][3],color=BLUE),run_time=.4)
        self.finish()


def calcium_meter(level=1):
    x,y=5.65,-1.6
    outline=Rectangle(width=.5,height=1.8,color=TEAL).move_to([x,y+.9,0])
    fill=Rectangle(width=.38,height=max(.02,level*1.68),stroke_width=0,
        fill_color=TEAL,fill_opacity=.9).move_to([x,y+.06+level*1.68/2,0])
    return VGroup(outline,fill,label('calcium',x,.65,22,TEAL))


def le_train(ks,title):
    p=train(ks,title=title)
    # Reserve a separate strip beside the plot for the calcium indicator.
    p[:3].stretch(.82,0,about_point=[-5.9,0,0])
    p.add(label('Lambert-Eaton fibre',0,2.12,26,BLUE))
    return p


class S18Steep(SpokenScene):
    def construct(self):
        ca=np.linspace(1,1.14,6); ks=20*ca**4
        p=le_train(ks,'20 Hz · rapid train · illustrative model')
        meter=calcium_meter(.2)
        self.add(p[:2],p[3:],p[2][0],meter)
        self.at('release rises steeply'); self.play(FadeIn(label('release rises steeply with calcium',0,-3.5,28,TEAL)),run_time=.4)
        self.at('a little extra calcium')
        for i,b in enumerate(p[2][1:],1):
            self.play(GrowFromEdge(b,DOWN),Transform(meter,calcium_meter(.2+i*.15)),run_time=.25)
        self.finish()


class S19Slow(SpokenScene):
    def construct(self):
        p=le_train(np.linspace(20,17,6),'Slow stimulation · decrement')
        meter=calcium_meter(.5)
        self.add(p[:2],p[3:],p[2][0],meter)
        self.at('a shrinking response')
        for b in p[2][1:]:
            # Calcium clears before the next impulse; each impulse adds a brief pulse.
            self.play(Transform(meter,calcium_meter(.03)),run_time=.18)
            self.play(GrowFromEdge(b,DOWN),Transform(meter,calcium_meter(.5)),run_time=.18)
        self.play(Transform(meter,calcium_meter(.03)),run_time=.2)
        self.at('Calcium clears'); self.play(FadeIn(label('calcium clears between impulses',0,-3.5,28,TEAL)),run_time=.3)
        self.at('rundown wins'); self.play(Indicate(p[2][-1],color=RED),run_time=.4)
        self.finish()


class S20Fingerprints(SpokenScene):
    def construct(self):
        t=table(); self.add(t)
        self.at('the two diseases'); self.play(Indicate(t[0][7:],color=TEXT),run_time=.6)
        self.finish()


class S21Sizeside(SpokenScene):
    def construct(self):
        t=table(); self.add(t); r=table(1)
        self.at('A smaller size'); self.play(Transform(t[1][:2],r[1][:2]),run_time=.4)
        self.at('points to'); self.play(Transform(t[1][2],r[1][2]),run_time=.4)
        self.at('That means'); self.play(Transform(t[1][3:],r[1][3:]),Transform(t[3],r[3]),run_time=.4)
        self.finish()


class S22Countside(SpokenScene):
    def construct(self):
        t=table(1); self.add(t); r=table(2)
        self.at('A lower count'); self.play(Transform(t[2][:2],r[2][:2]),run_time=.4)
        self.at('points to release'); self.play(Transform(t[2][2:],r[2][2:]),run_time=.4)
        self.finish()


class S23Caution(SpokenScene):
    def construct(self):
        t=table(2); self.add(t)
        # Reflow the size-side explanation, keeping both diagnostic rows intact.
        self.at('One caution'); self.play(t[1][2:].animate.shift(LEFT*.75),run_time=.4)
        v=Circle(radius=.35,color=YELLOW).move_to([5.2,1.15,0])
        filling=VGroup(*[Dot([x,.98,0],radius=.055,color=YELLOW) for x in (5.05,5.2,5.35)])
        vesicle_label=VGroup(label('half-filled',5.25,.55,22,YELLOW),label('vesicle',5.25,.2,22,YELLOW))
        self.at('Poorly filled vesicles'); self.play(FadeIn(VGroup(v,filling,vesicle_label)),run_time=.4)
        self.play(Transform(t[1][4],label('poor filling → size ↓',2.4,.4,26,YELLOW)),run_time=.4)
        self.at('pair the recording'); self.play(t[3].animate.shift(UP*.15),
            FadeIn(label('Pair with a receptor count',0,-3.5,30,PINK)),run_time=.4)
        self.finish()


class S24Electrical(SpokenScene):
    def construct(self):
        e=electrical(); self.add(e)
        self.at('gap junctions'); self.play(Indicate(e[1],color=TEAL),run_time=.6)
        self.finish()


class S25Nopackets(SpokenScene):
    def construct(self):
        e=electrical(); self.add(e)
        a=arrow([-4,.35,0],[4,.35,0]); current=label('current',0,1.25,30,YELLOW)
        # Open channel walls: current passes between them without crossing a box edge.
        e[1].become(VGroup(Rectangle(width=1.25,height=.8,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([0,.35,0]),
            Line([-.625,.75,0],[.625,.75,0],color=TEAL),
            Line([-.625,-.05,0],[.625,-.05,0],color=TEAL)))
        self.at('Current passes directly'); self.play(GrowArrow(a),FadeIn(current),run_time=.6)
        labels=VGroup()
        for i,word in enumerate(('vesicle count','quantal size','release failures')):
            text=label(word,0,-2.15-i*.6,30,GREY)
            strike=Line(text.get_left(),text.get_right(),color=RED,stroke_width=3)
            labels.add(VGroup(text,strike))
        self.at('there is no'); self.play(FadeOut(e[2][-2:]),FadeIn(labels),run_time=.4)
        self.finish()


class S25bStillsize(SpokenScene):
    def construct(self):
        e=electrical(); e[2][4].set_opacity(0); self.add(e)
        # An illustrative, scaled response: current arrives before the voltage changes.
        threshold=VGroup(DashedLine([.9,.3,0],[5.2,.3,0],color=ORANGE),backed('12 mV threshold',3.1,.3,26))
        self.add(threshold,label('illustrative response above rest (mV)',0,-2.7,28,GREEN),
            label('0',.75,-.75,26,GREY),label('time →',3.3,-1.2,26,GREY))
        a=arrow([-4,.65,0],[1,.65,0]); tr=trace(.65,x=1.05,y=-.75,w=4.1,events=(.35,))
        self.at('coupled response'); self.play(GrowArrow(a),run_time=.35); self.play(Create(tr),run_time=.5)
        self.at('too small'); self.play(FadeIn(label('too small to fire cell 2',0,-3.4,30,RED)),run_time=.4)
        self.finish()


class S26Rectify(SpokenScene):
    def construct(self):
        e=electrical(); self.add(e)
        a=arrow([-4,.52,0],[4,.52,0]); b=arrow([4,.17,0],[-4,.17,0])
        self.at('very fast'); self.play(GrowArrow(a),run_time=.35)
        self.at('both ways'); self.play(GrowArrow(b),FadeIn(label('both ways · same junction',0,-2.65,30,YELLOW)),run_time=.4)
        self.at('Some rectify'); self.play(a.animate.set_stroke(width=10),b.animate.set_stroke(width=5),run_time=.5)
        self.at('more easily'); self.play(FadeIn(label('rectifying: more easily one way',0,-3.35,30,YELLOW)),run_time=.4)
        self.finish()


class S27Takeaway(SpokenScene):
    def construct(self):
        f=formula(); self.add(f,label('chemical synapse',0,3.3,32,BLUE),glosses()[:2])
        self.at('the response'); self.play(Indicate(f[1],color=GREEN),run_time=.6)
        self.at('Ask which'); self.play(FadeIn(label('Which one moved: count, size, or both?',0,-3.3,34)),run_time=.5)
        self.finish()


class S28End(EndCard):
    LINE='Ask which one moved: count, size, or both.'
