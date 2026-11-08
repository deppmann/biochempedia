"""Following the Sign — word-aligned teaching film.

COLOR MAP (inherited from ../scenes.old.py):
BLUE = parallel fibres/context; ORANGE = climbing fibre/complex spike/teacher;
GREEN = Purkinje/simple spikes; TEAL = nucleus/output; RED = weakened synapse;
YELLOW = movement/learned correction; GREY = axes/neutral structure;
VIOLET = strengthening rule in fixed-sign mathematical examples.
The reference map takes precedence over the generic red-teacher visual note.
CHAPTERS.md is kept unchanged under TASK.md's edit-only restriction.
Evidence plots encode only the lesson's qualitative conditions (normalized schematic,
not digitized measurements). Timing uses its 120 ms and roughly 0.1 s values.
The fixed-sign example computes Δoutput = −Δweight × context, context=1;
the smooth context envelope reuses the reference's smooth(q)=3q²−2q³.
"""
import numpy as np
from bp_style import *

ORANGE = '#F29E4C'
RULE = '#C79EFF'
GREY = '#C3CBD5'
CTX, ERR, PUR, NUC, WEAK, MOVE = BLUE, ORANGE, GREEN, TEAL, RED, YELLOW


def P(x, y):
    return np.array([x, y, 0.])


def label(s, x=0, y=0, c=TEXT, size=28):
    return T(s, size, c).move_to(P(x,y))


def exc(a,b,c=GREY,w=4):
    return Arrow(P(*a),P(*b),buff=0,color=c,stroke_width=w,tip_length=.2)


def inh(a,b,c=PUR,w=5,bar=.22):
    a,b=P(*a),P(*b)
    d=(b-a)/np.linalg.norm(b-a); n=np.array([-d[1],d[0],0])
    return VGroup(Line(a,b,color=c,stroke_width=w),Line(b-n*bar,b+n*bar,color=c,stroke_width=w+1))


def poly(pts,c=GREY,w=4):
    m=VMobject(stroke_color=c,stroke_width=w)
    m.set_points_as_corners([P(*p) for p in pts]); return m


def box(s,c,x,y,w=3,h=1.25):
    r=RoundedRectangle(width=w,height=h,corner_radius=.15,color=c,fill_color=c,fill_opacity=.12)
    return VGroup(r,label(s,c=c,size=27)).move_to(P(x,y))


def synapse():
    dend=VGroup(Line(P(0,-2.7),P(0,1.3),color=PUR,stroke_width=15),
        Line(P(0,-1.3),P(-1.6,-.1),color=PUR,stroke_width=10),
        Line(P(0,-.7),P(1.7,.4),color=PUR,stroke_width=10))
    pf=Line(P(-5.5,1.3),P(4.9,1.3),color=CTX,stroke_width=7)
    dot=Dot(P(0,1.3),radius=.22,color=CTX)
    cf=poly([(4.9,-2.6),(1.1,-2.6),(-.55,-2.1),(.65,-1.5),(-.55,-.9),(.65,-.3),(.5,.3)],ERR,8)
    names=VGroup(label('parallel fibre',-3.8,1.9,CTX),label('Purkinje dendrite',-3,-2.6,PUR),
        label('climbing fibre / teacher',3.5,-3.2,ERR,26))
    return VGroup(dend,pf,dot,cf,names)


def sign_arrows():
    return VGroup(VGroup(exc((-1.6,1.65),(-1.6,2.65),CTX,7),label('Marr: stronger',-3.7,2.7,CTX,26)),
        VGroup(exc((1.6,2.65),(1.6,1.65),WEAK,7),label('Albus: weaker',3.8,2.7,WEAK,26)),label('?',0,2.3,TEXT,45))


def panels(n=0):
    g=VGroup()
    for i,x in enumerate([-4.25,0,4.25]):
        border=RoundedRectangle(width=4.05,height=5.8,corner_radius=.15,color=GREY).move_to(P(x,-.05))
        head=label(['Parallel fibres\nalone','Climbing fibre\nalone','Both inputs\npaired'][i],x,2.23,[CTX,ERR,TEXT][i],27)
        ax=VGroup(exc((x-1.25,-1.95),(x+1.6,-1.95)),exc((x-1.25,-1.95),(x-1.25,1.2)),
            label('parallel-fibre response',x-1.7,-.2,GREY,26).rotate(PI/2),
            label('before',x-.65,-2.32,GREY,26),label('>1 h',x+1.12,-2.32,GREY,26))
        mark=VGroup()
        for j,c in enumerate([CTX] if i==0 else [ERR] if i==1 else [CTX,ERR]):
            xx=x-.25+j*.14
            mark.add(Line(P(xx,-1.95),P(xx,-1.45),color=c,stroke_width=6))
        mark.add(label('pairing' if i==2 else 'stimulus',x+.25,-1.1,TEXT,26))
        if i==1: mark.add(label('measured response',x+.25,1.4,CTX,26))
        # Normalized response R=1-d H(t); d=0 for single inputs, .65 for pairing.
        ts=np.linspace(-1,2,150); r=1-(.65 if i==2 else 0)*(ts>=0)
        trace=poly([(x-1.15+.86*(t+1),-1.8+2.6*v) for t,v in zip(ts,r)],WEAK if i==2 else CTX,5)
        entry=VGroup(border,head,ax)
        if i<n: entry.add(mark,trace)
        g.add(entry)
    return g


def evidence_note():
    return label('Qualitative schematic • response measured at parallel fibres',0,3.35,GREY,26)


def strip(mode='question'):
    a=box('parallel-fibre\nsynapse',CTX,-4.35,.95,3.3,1.8)
    b=box('Purkinje cell\n(brake)',PUR,0,.95,3.3,1.8)
    c=box('nucleus',NUC,4.35,.95,3.3,1.8)
    if mode in ['question','answer']: a[0].set_fill(CTX,opacity=.025).set_stroke(CTX,opacity=.45)
    arrows=VGroup(exc((-2.65,.95),(-1.7,.95),CTX),inh((1.7,.95),(2.65,.95)))
    marks=VGroup()
    if mode in ['question','answer']:
        marks.add(label('weaker',-4.35,-.5,WEAK,30))
        if mode=='question': marks.add(label('?',4.35,-.65,NUC,54))
        else: marks.add(label('fires less',0,-.5,PUR,30),label('fires more',4.35,-.5,NUC,30))
    if mode=='down': marks.add(exc((4.35,-.25),(4.35,-1.5),WEAK,8),label('?',5.25,-.9,TEXT,48))
    if mode=='strong':
        a[0].set_fill(CTX,opacity=.5)
        marks.add(label('stronger',-4.35,-.5,CTX,30),label('fires more',0,-.5,PUR,30),label('fires less',4.35,-.5,NUC,30))
    g = VGroup(a,b,c,arrows,marks)
    if mode in ['question', 'down']: g.shift(DOWN*.95)
    return g


def brake_question(down=False):
    return label('What if output needs to fall?' if down else 'Does the nucleus fire more, or less?',0,3,TEXT,34)


def pedal(pressed=False):
    # Rounded shoe silhouette, separate sole and ankle opening, on a hinged brake.
    base=VGroup(Line(P(-1.6,-3.15),P(1.4,-3.15),color=GREY,stroke_width=5),Dot(P(-1.25,-3),radius=.12,color=GREY))
    lever=VGroup(Line(P(-1.25,-3),P(.9,-2.1),color=PUR,stroke_width=10),
        Line(P(.3,-2.05),P(1,-1.8),color=PUR,stroke_width=15))
    shoe=VMobject(color=MOVE,fill_color=MOVE,fill_opacity=.65,stroke_width=3)
    shoe.set_points_smoothly([P(-.95,-1.25),P(-.45,-1.22),P(-.3,-1.65),
        P(.25,-1.78),P(.9,-1.83),P(1.12,-2.01),P(1.03,-2.18),
        P(.5,-2.22),P(-.6,-2.03),P(-.94,-1.87),P(-.95,-1.25)])
    sole=poly([(-.9,-1.94),(-.6,-2.08),(.5,-2.27),(1.04,-2.23)],MOVE,5)
    ankle=Line(P(-.9,-1.4),P(-.47,-1.38),color=BG,stroke_width=5)
    moving=VGroup(lever,shoe,sole,ankle)
    if pressed: moving.rotate(-.3,about_point=P(-1.25,-3))
    drawing=VGroup(base,moving).scale(1.5,about_point=P(0,-3.15)).shift(UP*.12)
    drawing.stretch_to_fit_height(2.7).move_to(P(-.15,-1.45))
    return VGroup(*drawing,label('Purkinje cell brake',0,-3.12,PUR,26))


def timeline(stage=0):
    g=VGroup(exc((-5.6,-.8),(5.65,-.8)),label('time',5.1,-1.25,GREY,26),
        label('parallel-fibre activity',-3.4,2.65,CTX,28))
    ticks=VGroup(*[Line(P(x,-.75),P(x,1.65),color=CTX,stroke_width=7) for x in [-4.5,-2.9,-1.3,.3]])
    g.add(ticks)
    if stage>=1:
        g.add(Line(P(3.5,-.75),P(3.5,1.85),color=ERR,stroke_width=10),label('climbing-fibre error',3.6,2.65,ERR,26),
            SurroundingRectangle(ticks[2],color=MOVE,buff=.17),
            VGroup(DoubleArrow(P(-1.3,-1.7),P(3.5,-1.7),buff=0,color=GREY),label('about 120 ms',1.1,-2.2,TEXT,28)),
            label('Mouse flocculus • timing differs by region',0,-3.3,GREY,26))
    if stage>=2:
        g[-2].set_opacity(0)
        g.add(Line(P(-.5,-.75),P(-.5,2.2),color=MOVE,stroke_width=15),label('mistake made',-.5,3.35,MOVE,28),
            VGroup(DoubleArrow(P(-.5,-1.7),P(3.5,-1.7),buff=0,color=GREY),label('roughly 0.1 s',1.5,-2.2,TEXT,28)))
        # Highlight the preceding activity window, extending beneath the mistake mark.
        g[6].become(Rectangle(width=1.25,height=2.7,color=MOVE,fill_color=MOVE,fill_opacity=.1).move_to(P(-.95,.45)))
    return g


def raster(frequent=True,reduced=True):
    g=VGroup(label('Schematic of some recorded cells • one row per trial',0,3.35,GREY,26),
        label('time within trial →',0,-2.8,GREY,26))
    rows=VGroup()
    for i,y in enumerate([2.35,1.7,1.05,.1,-.55,-1.2,-1.85]):
        row=VGroup(Line(P(-3.8,y),P(3.5,y),color=GREY,stroke_opacity=.25))
        n=22 if i<3 or not reduced else 7
        for t in (np.arange(n)+.5)/n:
            row.add(Line(P(-3.7+7.1*t,y-.14),P(-3.7+7.1*t,y+.14),color=PUR,stroke_width=3))
        for t in ([.32] if i<3 or not frequent else [.2,.48,.76]):
            row.add(Line(P(-3.7+7.1*t,y-.2),P(-3.7+7.1*t,y+.3),color=ERR,stroke_width=8))
        rows.add(row)
    g.add(rows,DashedLine(P(-4,.6),P(3.7,.6),color=MOVE),label('load changed',5,.6,MOVE,26),
        label('before',-5,1.7,GREY,26),label('adapting',-5,-.2,GREY,26),label('adapted',-5,-1.55,GREY,26))
    return g


class S00Title(TitleCard):
    LESSON='The Cerebellum'
    TITLE='Following the Sign'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,1.4,TEAL,26),label(self.LESSON,0,.55,GREY,30),label(self.TITLE,0,-.6,TEXT,52))
        self.finish()


class S01(SpokenScene):
    def construct(self):
        s=synapse(); self.add(s)
        self.at('at a synapse'); self.play(Indicate(s[2]),run_time=.5)
        self.at('become a correction'); self.play(FadeIn(label('How does one small change at a synapse\nbecome a correction that arrives on time?',0,3,TEXT,28)),run_time=.5)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        s=synapse(); self.add(s)
        self.at('David'); self.play(FadeIn(label('David Marr • 1969',-3.3,3.15,TEXT,30)),run_time=.4)
        self.at('and James'); self.play(FadeIn(label('James Albus • 1971',3.3,3.15,TEXT,30)),run_time=.4)
        self.at('is a teacher'); self.play(Indicate(s[3],color=ERR),run_time=.6)
        self.at('But which way'); self.play(FadeOut(s[4][0]),FadeIn(label('Which way would it change a synapse?',0,2.25,TEXT,28)),run_time=.4)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        self.add(synapse()); a=sign_arrows()
        self.at('Mar'); self.play(FadeIn(a[0]),run_time=.45)
        self.at('Albus'); self.play(FadeIn(a[1]),FadeIn(a[2]),run_time=.45); self.finish()


class S04(SpokenScene):
    def construct(self):
        p=panels(); self.add(p,label('Ito and Kano • 1982 • rabbit cerebellum',0,3.35,TEXT,30))
        self.at('tested it in rabbits'); self.play(Indicate(p,scale_factor=1.01),run_time=.6)
        self.at('Compare three'); self.play(Indicate(VGroup(*[p[1] for p in panels()]),scale_factor=1.03),run_time=.6); self.finish()


class S05(SpokenScene):
    def construct(self):
        p=panels(); self.add(p,evidence_note())
        self.at('Parallel fibers alone'); self.play(Create(panels(1)[0][3]),run_time=.5)
        self.at('No lasting'); self.play(Create(panels(1)[0][4]),run_time=.6)
        self.play(FadeIn(label('Test conditions differ from strengthening protocols',0,-3.4,GREY,26)),run_time=.3); self.finish()


class S06(SpokenScene):
    def construct(self):
        self.add(panels(1),evidence_note()); q=panels(2)[1]
        self.at('Climbing fiber alone'); self.play(Create(q[3]),run_time=.5)
        self.at('No lasting'); self.play(Create(q[4]),run_time=.6); self.finish()


class S07(SpokenScene):
    def construct(self):
        self.add(panels(2),evidence_note()); q=panels(3)[2]
        self.at('The two together'); self.play(Create(q[3]),run_time=.5)
        self.at('response is smaller'); self.play(Create(q[4]),run_time=.7)
        self.at('at least an hour'); self.play(FadeIn(label('Smaller for at least 1 hour',0,-3.4,WEAK,30)),run_time=.4); self.finish()


class S08(SpokenScene):
    def construct(self):
        p=panels(3); note=evidence_note(); self.add(p,note,label('Smaller for at least 1 hour',0,-3.4,WEAK,30))
        self.at('only pairing'); self.play(p[2][0].animate.set_stroke(WEAK,width=5),run_time=.5)
        ltd=label('Long-term depression (LTD)',0,3.35,WEAK,30)
        self.at('This is cerebellar'); self.play(FadeOut(note),FadeIn(ltd),run_time=.5)
        # Keep the paired plot clear; reuse the full opposing sign arrows beside it.
        self.play(p.animate.scale(.78).shift(LEFT*1.25),run_time=.4)
        a=VGroup(VGroup(exc((5.5,.2),(5.5,1.35),CTX,7),label('Marr: stronger',5.1,1.85,CTX,26)),
            VGroup(exc((5.5,-.6),(5.5,-1.75),WEAK,7),label('Albus: weaker',5.1,-2.2,WEAK,26)))
        a.set_opacity(.25); self.add(a)
        self.at('the sign Albus',lead=0); self.play(a[1].animate.set_opacity(1),a[0].animate.set_opacity(.18),run_time=.4); self.finish()


class S09(SpokenScene):
    def construct(self):
        s=strip(); self.add(s)
        self.at('Does the nucleus'); self.play(FadeIn(brake_question()),run_time=.4); self.finish()


class S10Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(strip(),brake_question()); self.wait(5)


class S11(SpokenScene):
    def construct(self):
        s=strip(); q=brake_question(); self.add(s,q)
        self.at('More',lead=0); self.play(FadeOut(q),FadeOut(s[4][1]),s.animate.shift(UP*1.75),run_time=.4)
        p=pedal(True)
        self.at('other inputs unchanged'); self.play(FadeIn(label('Other inputs unchanged',0,3,GREY,28)),run_time=.4)
        self.at('The foot presses'); self.play(FadeIn(p),run_time=.4)
        self.at('brake less'); self.play(Transform(p,pedal()),FadeIn(label('fires less',0,.3,PUR,30)),run_time=.6)
        self.at('speeds up'); self.play(FadeIn(label('fires more',4.35,.3,NUC,30)),run_time=.4)
        self.at('Two negatives'); self.play(FadeIn(label('Two negatives\nmake a positive',3.7,-2.4,TEXT,28)),run_time=.4); self.finish()


class S12(SpokenScene):
    def construct(self):
        t=timeline(); self.add(*t[:3])
        self.at('But which'); self.play(LaggedStart(*[Create(x) for x in t[3]],lag_ratio=.25),run_time=1.5)
        self.at('It depends'); self.play(FadeIn(label('Timing depends on the region',0,3.4,GREY,28)),run_time=.4)
        self.at('In the flocculus'); self.play(FadeIn(timeline(1)[-1]),run_time=.4)
        self.at('those active'); self.play(Create(timeline(1)[6]),run_time=.4)
        self.at('before the climbing'); self.play(Create(timeline(1)[4]),FadeIn(timeline(1)[5]),FadeIn(timeline(1)[7]),run_time=.6); self.finish()


class S13(SpokenScene):
    def construct(self):
        t=timeline(1); self.add(t)
        q=timeline(2)
        self.at('a visual error'); self.play(FadeOut(t[7]),Create(q[-3]),FadeIn(q[-2]),run_time=.5)
        self.at('roughly a tenth'); self.play(FadeIn(q[-1]),run_time=.5); self.finish()


class S14(SpokenScene):
    def construct(self):
        t=timeline(2); self.add(t)
        self.at('carry the context'); self.play(Indicate(t[6],color=MOVE,scale_factor=1.15),FadeIn(label('Context when the\nmistake was made',-3.7,-2,CTX,28)),Create(poly([(-.95,-.95),(-2.1,-1.35),(-3.7,-1.35)],CTX,3)),run_time=.7); self.finish()


class S15(SpokenScene):
    def construct(self):
        t=VGroup(exc((-5.6,.6),(5.6,.6)),label('parallel-fibre activity',-3.7,2.65,CTX,26),
            *[Line(P(x,.65),P(x,2.1),color=CTX,stroke_width=6) for x in [-4.5,-2.9,-1.3,.3]],
            Line(P(-.5,.65),P(-.5,2.25),color=MOVE,stroke_width=15),label('mistake made',-.5,2.65,MOVE,26),
            Line(P(3.5,.65),P(3.5,2.1),color=ERR,stroke_width=9),label('late error',4.5,2.65,ERR,26),
            Rectangle(width=1.25,height=1.7,color=MOVE,fill_color=MOVE,fill_opacity=.1).move_to(P(-.95,1.4)))
        self.add(t,label('Next trial • same context',0,3.4,CTX,28))
        ax=VGroup(exc((-5,-2.5),(5.7,-2.5)),exc((-5,-2.5),(-5,.5)),label('nucleus firing',-5.8,-.85,NUC,26).rotate(PI/2),label('time',5.2,-2.95,GREY,26))
        late=3.5
        self.add(ax,DashedLine(P(late,-2.5),P(late,2.6),color=ERR),label('old error time',5,-.2,ERR,26))
        self.add(DashedLine(P(-4.9,-1.9),P(5.3,-1.9),color=GREY),label('trial 1',-3.9,-2.2,GREY,26))
        # ΔN=-Δw*c(t); normalized smooth context pulse, fixed other inputs.
        xs=np.linspace(-4.9,5.3,180)
        def smooth(q): return 3*q*q-2*q*q*q
        def context(x):
            return smooth((x+3.5)/2) if -3.5<x<-1.5 else smooth((.5-x)/2) if -1.5<=x<.5 else 0
        curve=poly([(x,-1.9+1.9*context(x)) for x in xs],NUC,6)
        self.at('before the late'); self.play(Create(curve),FadeIn(label('trial 2',1.2,-.65,NUC,28)),run_time=1)
        self.at('need not wait'); self.play(FadeIn(label('Schematic • exact timing depends on the circuit',0,-3.5,GREY,26)),run_time=.4); self.finish()


class S16(SpokenScene):
    def construct(self):
        self.add(label('Gilbert and Thach • 1977',0,3.4,TEXT,32))
        handle=VGroup(Line(P(0,-2.65),P(0,2.05),color=GREY,stroke_width=22),RoundedRectangle(width=.7,height=2.6,corner_radius=.2,color=TEXT,fill_color=GREY,fill_opacity=.7).move_to(P(0,.3)))
        grip=VGroup(poly([(-3,2.2),(-1.8,2.2),(-1.2,1.55),(.5,1.55),(.7,1.15),(-.65,.85)],MOVE,16),poly([(-3,-2.1),(-1.8,-2.1),(-1.2,-.95),(.5,-.95),(.7,-.5),(-.65,-.2)],MOVE,16),Line(P(-1.8,-2.1),P(-1.8,2.2),color=MOVE,stroke_width=18))
        assembly=VGroup(handle,grip,label('handle',1.25,-2.4,GREY,28),Line(P(.3,-2.4),P(.75,-2.4),color=GREY)).shift(RIGHT*.65)
        self.add(assembly,label('monkey’s grip\n(schematic gripper)',-4.7,.2,MOVE,26),DashedLine(P(.65,-2.8),P(.65,2.55),color=MOVE),label('set position',1.9,2.7,MOVE,28))
        a=exc((1.65,.7),(4.6,.7),MOVE,10); cap=label('load',4,1.35,MOVE,30)
        self.at('Monkeys returned',lead=0); self.play(GrowArrow(a),FadeIn(cap),assembly.animate.shift(RIGHT*.7),run_time=.45)
        self.at('to a set position',lead=0); self.play(assembly.animate.shift(LEFT*.7),FadeOut(a),FadeOut(cap),run_time=.65)
        self.at('the load changed',lead=0); self.play(GrowArrow(exc((1.65,.7),(5.7,.7),MOVE,15)),FadeIn(label('different load',4.3,1.35,MOVE,30)),assembly.animate.shift(RIGHT*.6),run_time=.65)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        cs=VGroup(Line(P(-3,0),P(-3,2),color=ERR,stroke_width=13),label('complex spikes',-3,-.7,ERR,32))
        ss=VGroup(Line(P(3,0),P(3,.8),color=PUR,stroke_width=4),label('simple spikes',3,-.7,PUR,32))
        self.at('Climbing fiber events'); self.play(Create(cs),run_time=.5)
        self.at('ordinary output'); self.play(Create(ss),run_time=.5)
        self.at('In some recorded cells'); self.play(FadeOut(cs),FadeOut(ss),run_time=.25)
        g=raster(False,False); self.play(FadeIn(g),run_time=.5)
        self.at('grew more frequent'); self.remove(g); g=raster(True,False); self.add(g); self.play(Indicate(g[3],color=MOVE,scale_factor=1),run_time=.7)
        self.at('fell',lead=0); self.remove(g); g=raster(); self.add(g); self.play(Indicate(g[2][-1],color=PUR,scale_factor=1),run_time=.6)
        self.at('stayed lower'); self.play(FadeIn(VGroup(Line(P(3.8,-.1),P(3.8,-2.1),color=PUR),label('lower, and\nstays lower',5.1,-1.5,PUR,26))),run_time=.4); self.finish()


class S18(SpokenScene):
    def construct(self):
        self.add(raster())
        self.at('That pattern fits'); self.play(FadeIn(label('more error\nsignals',5,-.05,ERR,26)),Create(poly([(3.65,.4),(3.9,.4),(3.9,-.8),(3.65,-.8)],ERR,4)),FadeIn(label('lasting drop',5,-1.65,PUR,26)),Create(Line(P(3.8,-1.65),P(2.8,-1.65),color=PUR)),run_time=.5)
        self.at('does not measure'); self.play(FadeIn(label('Fits the model; not a synapse measurement',0,-3.5,GREY,26)),run_time=.4); self.finish()


class S19(SpokenScene):
    def construct(self):
        s=strip('answer'); self.add(s)
        self.at('only release'); self.play(Indicate(s[1]),run_time=.5)
        self.at('What if the output needs to fall',lead=0); self.remove(s); self.add(strip('down')); self.play(FadeIn(brake_question(True)),run_time=.4); self.finish()


class S20Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(strip('down'),brake_question(True)); self.wait(5)


class S21(SpokenScene):
    def construct(self):
        s=strip('down'); self.add(s); p=pedal()
        ticks=VGroup(*[Line(P(x,2),P(x,2.7),color=CTX,stroke_width=7) for x in [-5.3,-4.5,-3.7]])
        self.at('One way'); self.play(LaggedStart(*[Create(t) for t in ticks],lag_ratio=.25),run_time=.65)
        self.at('strengthen the same'); self.remove(s); s=strip('strong').shift(UP*.8); self.add(*s[:4],s[4][0]); self.play(Indicate(s[0],color=CTX),run_time=.4)
        self.at('brake'); self.play(FadeIn(p),FadeIn(s[4][1]),run_time=.3); self.play(Transform(p,pedal(True)),FadeIn(s[4][2]),GrowArrow(exc((5.4,-1.3),(5.4,-2.4),NUC,8)),run_time=.6)
        self.at('Parallel fiber activity'); self.play(Indicate(ticks,color=CTX),FadeIn(label('Long-term potentiation • one route',1.6,3.3,CTX,28)),run_time=.8)
        self.at('can do that'); self.play(Indicate(s[0],color=CTX),run_time=.5)
        self.at('Other circuit changes'); self.play(FadeIn(label('Other circuit changes\ncan also lower output',3.8,-3.1,GREY,26)),run_time=.4); self.finish()


def signplots():
    g=VGroup()
    for i,cx in enumerate([-3.25,3.25]):
        ax=VGroup(exc((cx-2.2,-2.3),(cx+2.65,-2.3)),exc((cx-2.2,-2.3),(cx-2.2,2)),label('output',cx-2.65,.1,GREY,26).rotate(PI/2),label('learning',cx+.4,-2.8,GREY,26),label('Output up' if i==0 else 'Output down',cx,2.45,TEXT,30))
        xs=np.linspace(0,1,80); direction=1 if i==0 else -1
        # Target y=±t; weakening gives -Δw=t (up) or zero if target is down.
        target=DashedVMobject(poly([(cx-2+4.3*t,-.1+direction*1.6*t) for t in xs],MOVE,10),num_dashes=18,dashed_ratio=.6)
        rule=poly([(cx-2+4.3*t,-.1+1.6*(t if i==0 else 0)) for t in xs],NUC,3)
        strong=poly([(cx-2+4.3*t,-.1-1.6*t) for t in xs],RULE,3)
        g.add(VGroup(ax,target,rule,strong))
    return g


class S22(SpokenScene):
    def construct(self):
        g=signplots(); self.add(label('One fixed-sign channel • other inputs fixed',0,3.5,GREY,28),g[0][0],g[1][0],g[0][1],g[1][1])
        self.add(label('━ target',-4,-3.45,MOVE,26),label('━ weaken only',-.2,-3.45,NUC,26),label('━ strengthen',3.9,-3.45,RULE,26))
        self.at('weakening alone'); self.play(Create(g[0][2]),Create(g[1][2]),FadeIn(label('weaken only: fits',-3.2,1.8,NUC,26)),FadeIn(label('weaken only: stays flat',3.25,.45,NUC,26)),run_time=.7)
        self.at('Strengthening can reverse'); self.play(Create(g[1][3]),run_time=.7); self.finish()


class S23(SpokenScene):
    def construct(self):
        self.add(label('The rule has limits',0,3.35,TEXT,36))
        cards=VGroup(*[box(t,GREY,0,y,11.7,1.85) for t,y in [('TASK  •  Teacher gated by the task',1.85),('LTD  •  Learning without detectable LTD',-.4),('REWARD  •  Climbing fibres also signal reward',-2.65)]])
        for c,text in zip(cards,['TASK  •  Teacher gated by the task','LTD  •  Learning without detectable LTD','REWARD  •  Climbing fibres also signal reward']):
            c[1].become(label(text,c[1].get_x(),c[1].get_y(),TEXT,32))
        self.at('The teacher works'); self.play(FadeIn(cards[0]),run_time=.5)
        self.at('Mice without'); self.play(FadeIn(cards[1]),run_time=.5)
        self.at('also signal reward'); self.play(FadeIn(cards[2]),run_time=.5); self.finish()


class S24(SpokenScene):
    def construct(self):
        # Full-size causal diagram is present from the first word.
        context=box('eligible context',CTX,-4.35,3.05,3.4,.65)
        error=box('timed error',ERR,.1,3.05,3,.65)
        s=strip('answer').shift(UP*.8)
        self.add(context,error,*s[:4],label('Other inputs fixed',4.5,3.05,GREY,26))
        links=VGroup(exc((-4.35,2.7),(-4.35,2.3),CTX),exc((-1.4,3.05),(-3.7,2.3),ERR))
        self.add(links)
        p=pedal(True); self.add(p)
        self.at('a well'); self.play(Indicate(error,scale_factor=1.04),run_time=.4)
        self.at('can weaken'); self.play(FadeIn(s[4][0]),Indicate(s[0],color=WEAK),run_time=.5)
        self.at('less break'); self.play(FadeIn(s[4][1]),Transform(p,pedal()),run_time=.5)
        self.at('more output'); self.play(FadeIn(s[4][2]),run_time=.4)
        self.at('before the late'); self.play(FadeIn(label('Ready ahead of\nlate feedback',4.3,-1.3,NUC,28)),run_time=.4)
        self.play(FadeIn(label('Unpaired activity\ncan do the reverse',-4.3,-1.5,CTX,26)),FadeIn(label('Timing varies\nMouse flocculus: ~120 ms',-4.3,-2.65,GREY,26)),run_time=.4); self.finish()


class S25End(EndCard):
    LINE='In this model, timed errors weaken synapses so correction arrives early.'
    def construct(self):
        self.add(label('In this model, timed errors weaken synapses\nso correction arrives early.',0,.3,TEXT,36),label('biochemistrypedia.com',0,-1.2,TEAL,26)); self.finish()
