"""The Gap, Seen — revision after the 20-item frame review.
COLOR MAP (shared across chapters): BLUE first/injected cell; YELLOW neighbour;
GREEN membranes/separate cells; ORANGE fused cytoplasm; RED blur/stopped;
TEAL channels/small tracer/signals; MAGENTA dextran; VIOLET electron beam;
GREY apparatus/nuclei. All diagrams schematic except the stated scale ratios.
"""
import importlib.util
from pathlib import Path
import numpy as np
from bp_style import *

ORANGE = '#F29E4C'
MAGENTA = '#E070C0'
VIOLET = '#B28DFF'

# Reuse the actual chapter-one evidence icons, without modifying that chapter.
_spec = importlib.util.spec_from_file_location('chapter_one_icons', Path(__file__).resolve().parent.parent / 'scenes.py')
_ch1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ch1)

class Speech(SpokenScene):
    def at(self, phrase, lead=.2, nth=0):
        # The normal implementation also writes sync.log. Keep all revision outputs
        # within the task's explicit allowlist by doing the same timing in memory.
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > .02:
            self.wait(rest)


def txt(s, x=0, y=0, c=TEXT, size=30):
    return T(s, size=size, color=c).move_to([x,y,0])


def arrow(a,b,c=TEXT):
    return Arrow([*a,0],[*b,0],buff=.06,color=c,stroke_width=3,tip_length=.16)


def line(a,b,c=GREEN,w=6):
    return Line([*a,0],[*b,0],color=c,stroke_width=w)


def box(x,y,w,h,c=GREY,fill=.12):
    return RoundedRectangle(width=w,height=h,corner_radius=.2,stroke_color=c,stroke_width=3,
                            fill_color=c,fill_opacity=fill).move_to([x,y,0])


def path(points,c=TEAL,w=5):
    return VMobject(stroke_color=c,stroke_width=w).set_points_as_corners([np.array([*p,0.]) for p in points])


def contact():
    ring=DashedVMobject(Circle(radius=2.1,color=RED,stroke_width=4).move_to([3.4,-.2,0]),num_dashes=32)
    return VGroup(line((3.4,2.6),(3.4,-.07),BLUE,14),line((3.4,-.33),(3.4,-3),YELLOW,14),ring)


def evidence():
    icons=[_ch1.icon_cell(),_ch1.icon_embryo()[:3],_ch1.icon_chain()]
    names=['whole cells','embryos','signal direction']
    out=VGroup()
    for g,n,y in zip(icons,names,[1.85,-.15,-2.15]):
        g.scale_to_fit_height(1.35).move_to([-5,y,0])
        out.add(VGroup(g,txt(n,-3.3,y,size=26)))
    return out


class S00Title(TitleCard):
    LESSON='Seeing Neurons: Golgi, Cajal and the Neuron Doctrine'
    TITLE='The Gap, Seen'


class S01Q(Speech):
    def construct(self):
        g=contact(); icons=evidence()
        self.add(g,icons,txt('The Gap, Seen',0,3.35,size=36))
        self.at('none reached')
        ars=VGroup(*[arrow((-1.8,y),(3.1,-.2),GREEN) for y in [1.85,-.15,-2.15]])
        self.play(*[GrowArrow(a) for a in ars],run_time=.5)
        self.at('the membrane')
        contact_label=VGroup(txt('contact',5.25,.5,c=GREEN,size=28),arrow((4.8,.25),(3.5,-.2),GREEN))
        self.add(contact_label)
        self.at('what would it take')
        self.play(FadeOut(icons),FadeOut(ars),g.animate.move_to([0,0,0]),
                  FadeOut(contact_label),run_time=.45)
        self.add(txt('What would it take?',0,-3.45,c=RED,size=32))
        self.finish()


def prediction():
    banner=txt('What would you see at the membrane?',0,3.35,c=TEAL,size=36)
    ps=VGroup()
    for x,c,n in [(-3.3,ORANGE,'If Golgi were right'),(3.3,GREEN,'If Cajal were right')]:
        ps.add(VGroup(box(x,-.25,5.9,5.65,c,.05),txt(n,x,2.1,c,size=30),txt('?',x,-.4,c,size=120)))
    return VGroup(banner,ps)


class S02Predict(Speech):
    def construct(self):
        p=prediction(); self.add(p)
        self.at('what would you see')
        self.play(Indicate(p[1][0][0],scale_factor=1.015),run_time=.5)
        self.at('and if')
        self.play(Indicate(p[1][1][0],scale_factor=1.015),run_time=.5)
        self.finish()


class S03Pause(NarratedScene):
    def construct(self):
        self.add(prediction())
        cue=txt('Think',0,-3.45,c=TEAL,size=26); self.add(cue)
        dots=VGroup(*[Dot([x,-3.45,0],radius=.07,color=TEAL) for x in [.7,.95,1.2,1.45,1.7]])
        self.add(dots)
        for d in dots:
            self.play(d.animate.set_opacity(.15),run_time=.9)
        self.finish()


def fused():
    xs=np.linspace(-6,6,140)
    widths=.55+1.45*np.exp(-((abs(xs)-3.5)/1.45)**2)
    pts=[(x,w-.1,0) for x,w in zip(xs,widths)]+[(x,-w-.1,0) for x,w in zip(xs[::-1],widths[::-1])]
    return Polygon(*pts,stroke_color=GREEN,stroke_width=6,fill_color=ORANGE,fill_opacity=.23)


class S04Rev1(Speech):
    def construct(self):
        shape=fused()
        self.add(txt('If Golgi were right',0,3.35,c=ORANGE,size=34),shape)
        self.at('the outer membrane')
        self.add(txt('outer membrane',-3.8,2.65,c=GREEN,size=28),arrow((-3.8,2.35),(-3.8,1.9),GREEN))
        self.play(Create(shape.copy().set_fill(opacity=0)),run_time=.65)
        self.at('runs on around both')
        self.add(txt('continuous cytoplasm',0,-2.6,c=ORANGE,size=30))
        self.at('and no membrane')
        self.add(txt('no membrane across the junction',0,-3.3,size=28),arrow((0,-2.25),(0,-.1)))
        self.finish()


def separate():
    # Close view of facing tips: the cleft is a prominent full-height space.
    a=box(-3.55,-.25,4.7,5.2,BLUE); b=box(3.55,-.25,4.7,5.2,YELLOW)
    ml=line((-1.2,-2.85),(-1.2,2.35),GREEN,10); mr=line((1.2,-2.85),(1.2,2.35),GREEN,10)
    return VGroup(a,b,ml,mr,txt('gap (not to scale)',0,2.85,size=28),
                  DoubleArrow([-1.15,2.45,0],[1.15,2.45,0],buff=0,color=TEXT,tip_length=.13))


class S05Rev2(Speech):
    def construct(self):
        g=separate(); self.add(txt('If Cajal were right',0,3.4,c=GREEN,size=34),g[0],g[1])
        self.at('two membranes')
        self.play(Create(g[2]),Create(g[3]),run_time=.5)
        self.at('across a gap')
        self.add(g[4],g[5])
        self.at('each cytoplasm')
        self.add(txt('cytoplasm',-3.3,-.25,c=BLUE,size=30),txt('cytoplasm',3.3,-.25,c=YELLOW,size=30))
        self.at('at its own membrane')
        self.add(txt('each stops at its own membrane',0,-3.4,c=GREEN,size=28))
        self.finish()


class S06Beat(NarratedScene):
    def construct(self):
        self.add(separate(),txt('If Cajal were right',0,3.4,c=GREEN,size=34),
                 txt('cytoplasm',-3.3,-.25,c=BLUE),txt('cytoplasm',3.3,-.25,c=YELLOW),
                 txt('each stops at its own membrane',0,-3.4,c=GREEN,size=28))
        self.finish()


class S07Em(Speech):
    def construct(self):
        self.add(txt('transmission electron microscope',0,3.4,c=VIOLET,size=34))
        source=box(0,2.25,2,.6,VIOLET,.3)
        screen=box(0,-2.6,5.2,.5,GREY,.3)
        tissue=VGroup(box(-1.05,0,2,.85,BLUE,.25),box(1.05,0,2,.85,YELLOW,.25))
        self.add(source,tissue,screen,txt('source',3,2.25,c=VIOLET,size=28),
                 txt('thin section',3.9,0,size=28),txt('screen',3.9,-2.6,size=28),
                 txt('two cells in nervous tissue',0,-3.4,size=28))
        self.at('electron microscope')
        beams=VGroup(*[arrow((x,1.9),(x,.55),VIOLET) for x in [-.65,0,.65]],
                     *[arrow((x,-.55),(x,-2.25),VIOLET) for x in [-.65,0,.65]])
        self.play(LaggedStart(*[GrowArrow(b) for b in beams],lag_ratio=.08),run_time=.8)
        self.at('in thin sections')
        self.play(Indicate(tissue,scale_factor=1.04),run_time=.5)
        self.finish()


def frog_icon():
    return VGroup(*[Circle(radius=.5,stroke_color=BLUE,fill_color=BLUE,fill_opacity=.2).move_to([x,y,0])
                    for x,y in [(-1,.4),(0,.9),(1,.25),(.4,-.5),(-.75,-.7)]])


def worm_icon():
    return VGroup(line((-2.5,0),(2.5,0),YELLOW,6),
                  *[Ellipse(width=.6,height=1.2,color=YELLOW).move_to([x,0,0]) for x in [-2,-1,0,1,2]])


class S081955(Speech):
    def construct(self):
        self.add(txt('1955',0,3.2,c=TEAL,size=58),txt('De Robertis and Bennett',0,2.3,size=34))
        for x,icon,label in [(-3.3,frog_icon(),'frog: sympathetic ganglia'),(3.3,worm_icon(),'earthworm: nerve cord')]:
            icon.scale_to_fit_width(4.8)
            if icon.height > 3.1: icon.scale_to_fit_height(3.1)
            icon.move_to([x,-.1,0])
            self.add(box(x,-.5,6,4.8),icon,txt(label,x,-2.35,size=26))
        self.finish()


class S091956(Speech):
    def construct(self):
        self.add(txt('1956',0,3.2,c=TEAL,size=58),txt('Sanford Palay',0,2.25,size=36),box(0,-.5,8.2,4.8))
        brain=VGroup(Ellipse(width=4.3,height=2.6,color=GREY,fill_color=GREY,fill_opacity=.2),
                     Ellipse(width=1.4,height=1.3,color=GREY).move_to([-2,-.7,0]),
                     Ellipse(width=.8,height=.7,color=GREY).move_to([2.2,.15,0]),
                     path([(-1.4,.6),(-.5,.2),(.3,.6),(1.2,.1)],GREY,4))
        brain.move_to([0,-.4,0]); self.add(brain,txt('rat brain',0,-2.4,size=30))
        self.finish()


# Chemical micrograph geometry: 0.6 units = 20 nm, blur diameter 6 = 200 nm.
# Vesicle diameter 1.2 = 40 nm. The EM frame spans the full cell regions.
HG=.3
CY=-.2

def micro():
    return VGroup(box(-3.35,CY,6.1,4.9,BLUE,.16),box(3.35,CY,6.1,4.9,YELLOW,.16),
                  line((-HG,-2.65),(-HG,2.25)),line((HG,-2.65),(HG,2.25)))


def cleft():
    return VGroup(txt('cleft: 10 to 20 nm',0,3.35,size=30),
                  arrow((-1,2.8),(-.32,2.35)),arrow((1,2.8),(.32,2.35)))


def vesicles():
    pts=[(-.9,1.55),(-.9,.2),(-.9,-1.15),(-2.35,.9),(-2.35,-.45),(-2.35,-1.8),
         (-3.65,1.55),(-3.65,.2),(-3.65,-1.15),(-4.95,.9),(-4.95,-.45),(-4.95,-1.8)]
    return VGroup(*[Circle(radius=.6,stroke_color=BLUE,stroke_width=3,fill_color=BLUE,fill_opacity=.22).move_to([x,y,0]) for x,y in pts])


def density():
    return Rectangle(width=.24,height=3.9,stroke_color=TEXT,stroke_width=2.5,
                     fill_color='#050609',fill_opacity=1).move_to([.46,CY,0])


def micro_labels():
    return VGroup(txt('terminal',-3.4,2.65,c=BLUE,size=28),txt('receiving cell',3.4,2.65,c=YELLOW,size=28),cleft())


class S10Saw(Speech):
    def construct(self):
        g=micro(); self.add(g[0],g[1],txt('chemical synapse',0,3.35,c=GREEN,size=34))
        self.at('two membranes'); self.play(Create(g[2]),run_time=.4)
        self.at('stayed separate'); self.play(Create(g[3]),run_time=.4)
        self.at('across a cleft')
        self.remove(self.mobjects[2]); self.add(cleft())
        self.at('10 to 20')
        self.add(txt('membrane',-3.4,-3.25,c=GREEN,size=28),txt('membrane',3.4,-3.25,c=GREEN,size=28),
                 arrow((-2.3,-3),(-.4,-2.4),GREEN),arrow((2.3,-3),(.4,-2.4),GREEN))
        self.finish()


class S11Signs(Speech):
    def construct(self):
        self.add(micro(),micro_labels())
        self.at('small vesicles')
        self.play(FadeIn(vesicles()),run_time=.45)
        self.add(txt('vesicles (~40 nm)',-3.6,-3.3,c=BLUE,size=28),arrow((-3.6,-3),(-3.65,-1.8),BLUE))
        self.at('the receiving membrane')
        self.add(density())
        self.at('also looks thickened')
        self.add(txt('dark membrane thickening',3.5,-3.3,size=28),arrow((2.5,-3),(.5,-2.15)))
        self.finish()


class S12Why(Speech):
    def construct(self):
        g=VGroup(micro(),vesicles(),density()); self.add(g)
        ring=DashedVMobject(Circle(radius=3,color=RED,stroke_width=4).move_to([0,CY,0]),num_dashes=36)
        veil=Circle(radius=3,stroke_width=0,fill_color=RED,fill_opacity=.35).move_to([0,CY,0])
        labels=VGroup(txt('blur: about 200 nm',-3.6,3.35,c=RED,size=28),txt('cleft: about 20 nm',3.6,3.35,size=28),
                      arrow((2.7,3.05),(.1,1.6)))
        self.at('under light')
        self.add(veil,ring,labels)
        self.at('inside one blur')
        self.play(Indicate(ring,scale_factor=1.02),run_time=.55)
        self.at('replaced the blur')
        self.play(FadeOut(veil),FadeOut(ring),FadeOut(labels),run_time=.6)
        self.at('with two membranes')
        self.add(cleft(),txt('two separate membranes',0,-3.3,c=GREEN,size=32))
        self.finish()


class S13Settled(Speech):
    def construct(self):
        xs=[-5.3,-1,5.3]
        self.add(txt('The question, settled',0,3.4,c=GREEN,size=36),line((-6,-.1),(6,-.1),GREY,5))
        for x,year,label,c,y in zip(xs,['1873','1906','1955 / 56'],['black reaction','Nobel Prize','electron microscopy'],[BLUE,GREY,GREEN],[-1.1,-2.3,-1.1]):
            self.add(line((x,-.3),(x,.1),c,5),Dot([x,-.1,0],radius=.13,color=c),
                     txt(year,x,y,c,size=32),txt(label,max(-4.6,min(4.6,x)),y-.6,c,size=28))
        self.add(line((-5.3,.3),(-5.3,2.3),BLUE,3),line((5.3,.3),(5.3,2.3),GREEN,3))
        self.at('80 years')
        br=DoubleArrow([-5.3,2.3,0],[5.3,2.3,0],buff=0,color=TEXT,tip_length=.2)
        self.play(GrowFromCenter(br),run_time=.6); self.add(txt('about 80 years',0,2.85,size=34))
        self.finish()


# Enlarged docked hemichannels: membrane centres +/- .4, gap .8;
# full channel length 2.2, with a visibly open lumen. Protein cartoons, not structures.
def junction():
    g=VGroup(*[Rectangle(width=6,height=5.1,stroke_width=0,fill_color=c,fill_opacity=.12).move_to([x,-.2,0]) for x,c in [(-3.4,BLUE),(3.4,YELLOW)]],
                 Rectangle(width=12.8,height=5.1,stroke_color=GREY,stroke_width=2).move_to([0,-.2,0]))
    for x in [-.4,.4]:
        g.add(line((x,2.35),(x,.32)),line((x,-.72),(x,-2.75)))
    return g


def halves():
    out=VGroup()
    for s in [-1,1]:
        h=VGroup()
        for y in [.48,-.88]:
            h.add(box(s*.55,y,1.1,.38,TEAL,.5))
        # visible wall divisions indicate separate protein subunits in side view
        h.add(line((s*.36,.3),(s*.36,.66),TEAL,2),line((s*.73,-1.06),(s*.73,-.7),TEAL,2))
        out.add(h)
    return out


def lumen():
    return Rectangle(width=2.2,height=.96,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([0,-.2,0])


def ring_six():
    g=VGroup()
    for k in range(6):
        a=k*PI/3
        g.add(box(.65*np.cos(a),.65*np.sin(a),.48,.48,TEAL,.35))
    return g


def junction_labels():
    return VGroup(txt('gap: a few nm',0,-3.35,size=28),arrow((0,-3.05),(0,-2.6)),
                  txt('cell 1',-4.5,-2.2,c=BLUE,size=28),txt('cell 2',4.5,-2.2,c=YELLOW,size=28))


class S14Elec(Speech):
    def construct(self):
        self.add(junction(),junction_labels(),txt('electrical synapse',0,3.35,c=TEAL,size=34))
        hs=halves()
        # Begin assembly with the first words, so the opening has a subject.
        self.play(FadeIn(hs[0].shift(LEFT*.5)),FadeIn(hs[1].shift(RIGHT*.5)),run_time=.35)
        self.play(hs[0].animate.shift(RIGHT*.5),hs[1].animate.shift(LEFT*.5),run_time=.65)
        self.add(lumen())
        self.at('channels called')
        self.add(txt('gap junction',0,2.75,c=TEAL,size=30),
                 txt('hemichannel',-2.4,1.4,c=TEAL,size=26),txt('hemichannel',2.4,1.4,c=TEAL,size=26),
                 arrow((-1.6,1.15),(-.65,.7),TEAL),arrow((1.6,1.15),(.65,.7),TEAL))
        self.at('gap junctions')
        inset=ring_six().scale(1.15).move_to([-2.65,-.5,0])
        self.add(inset,txt('six connexins',-2.65,-1.85,c=TEAL,size=26),
                 txt('open lumen',3.7,.1,c=TEAL,size=28),arrow((2.7,-.1),(0,-.2),TEAL))
        self.finish()


class S15Pass(Speech):
    def construct(self):
        self.add(junction(),halves(),junction_labels(),txt('ions and small molecules',0,3.35,c=TEAL,size=34),
                 txt('open channel',0,2.75,c=TEAL,size=28))
        # A continuous stream through the lumen throughout the entire spoken line.
        dots=VGroup()
        for k in range(12):
            d=Dot(radius=.09,color=TEAL)
            def flow(m,dt,k=k):
                m.phase=(getattr(m,'phase',k/12)+dt/3.2)%1
                m.move_to([-5.7+11.4*m.phase,-.2+.05*np.sin(k),0])
            d.add_updater(flow); flow(d,0); dots.add(d)
        self.add(dots); self.at('pass straight'); self.finish()


def injection_question():
    pip=Polygon([-4.9,1.7,0],[-4.6,1.8,0],[-3.5,.35,0],[-3.55,.2,0],
                stroke_color=TEXT,stroke_width=3,fill_color=TEXT,fill_opacity=.3)
    return VGroup(junction(),halves(),txt('Does a pore bring back the network?',0,3.35,c=ORANGE,size=34),
                  txt('What would you inject?',0,-3.35,size=32),txt('?',-4,-1.3,size=68),pip)


class S16Predict(Speech):
    def construct(self):
        g=injection_question(); self.add(*g[:3])
        self.at('what would you inject')
        self.add(*g[3:]); self.play(g[-1].animate.shift(RIGHT*.15+DOWN*.15),run_time=.6)
        self.finish()


class S17Pause(NarratedScene):
    def construct(self):
        g=injection_question(); self.add(g)
        self.play(g[-1].animate.shift(RIGHT*.15+DOWN*.15),run_time=2.3,rate_func=there_and_back)
        self.play(g[-1].animate.shift(RIGHT*.15+DOWN*.15),run_time=2.3,rate_func=there_and_back)
        self.finish()


ROW_Y=-.2

def row():
    cells=VGroup(*[box(x,ROW_Y,3.6,5.1,c) for x,c in [(-4,YELLOW),(0,BLUE),(4,YELLOW)]])
    chans=VGroup()
    for x in [-2,2]:
        chans.add(VGroup(
            Rectangle(width=1.2,height=.26,stroke_color=TEAL,stroke_width=2,fill_color=TEAL,fill_opacity=.5).move_to([x,.1,0]),
            Rectangle(width=1.2,height=.26,stroke_color=TEAL,stroke_width=2,fill_color=TEAL,fill_opacity=.5).move_to([x,-.5,0])))
    # Erase only the pore openings in the cell outlines, then draw their walls.
    for x in [-2.2,-1.8,1.8,2.2]:
        cells.add(Rectangle(width=.12,height=.34,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([x,-.2,0]))
    labels=VGroup(*[txt(n,x,-3.3,c=c,size=28) for x,n,c in [(-4,'neighbour',YELLOW),(0,'injected cell',BLUE),(4,'neighbour',YELLOW)]])
    pip=Polygon([-.6,2.2,0],[-.35,2.3,0],[.05,1.35,0],[0,1.2,0],stroke_color=TEXT,fill_color=TEXT,fill_opacity=.3)
    return VGroup(cells,chans,labels,pip)


def tracer_positions(n=16):
    # Deterministic, legible concentration depiction; transport paths are schematic.
    return [(-1.25+(k%4)*.8,-1.9+(k//4)*.85) for k in range(n)]


class S18Rev1(Speech):
    def construct(self):
        self.add(row(),txt('small tracer, such as Neurobiotin',0,3.35,c=TEAL,size=32))
        keep=VGroup(*[Dot([x,y,0],radius=.09,color=TEAL) for x,y in tracer_positions()])
        self.at('a small tracer'); self.add(keep)
        moving=VGroup(); anims=[]
        for s in [-1,1]:
            for k in range(5):
                start=(s*.7,-.2)
                d=Dot([*start,0],radius=.09,color=TEAL); moving.add(d)
                p=path([start,(s*1.5,-.2),(s*2.5,-.2),(s*(3+k*.48),-1.6+(k%3)*1.1)])
                anims.append(MoveAlongPath(d,p,rate_func=linear))
        self.at('passes through'); self.add(moving)
        self.play(LaggedStart(*anims,lag_ratio=.035),run_time=2.4)
        stream=VGroup()
        for side in [-1,1]:
            for k in range(3):
                d=Dot(radius=.09,color=TEAL)
                def flow(m,dt,side=side,k=k):
                    m.phase=(getattr(m,'phase',k/3)+dt/1.8)%1
                    m.move_to([side*(.8+2.5*m.phase),-.2,0])
                d.add_updater(flow); flow(d,0); stream.add(d)
        self.add(stream)
        self.finish()


class S19Rev2(Speech):
    def construct(self):
        self.add(row(),txt('10 kDa dextran, nearly 5 nm',0,3.35,c=MAGENTA,size=32))
        dots=VGroup(*[Dot([x,y,0],radius=.28,color=MAGENTA) for x,y in [(-.8,.6),(.7,.55),(-.7,-1.25),(.65,-1.2),(0,-.15)]])
        self.at('10 kilodalton'); self.add(dots)
        self.at('nearly 5')
        self.add(txt('vertebrate connexin pore: about 1.5 nm',0,2.75,c=TEAL,size=26),
                 arrow((2.6,2.45),(2,-.2),TEAL))
        self.at('stays in the injected cell')
        stop=VGroup(line((-1.7,-.6),(-1.7,.2),RED,7),line((1.7,-.6),(1.7,.2),RED,7))
        self.add(stop,txt('stopped',0,-2.35,c=RED,size=28))
        self.play(dots[-1].animate.move_to([1.05,-.2,0]),run_time=.45)
        self.play(dots[-1].animate.move_to([.7,-.2,0]),run_time=.45)
        self.finish()


def syncytium():
    outline=Ellipse(width=9.3,height=4.8,stroke_color=GREEN,stroke_width=6,fill_color=ORANGE,fill_opacity=.12).move_to([-1.1,-.25,0])
    nuclei=VGroup(*[Ellipse(width=.6,height=.85,stroke_color=GREY,fill_color=GREY,fill_opacity=.4).move_to([x,y,0]) for x,y in [(-3.5,.5),(-.9,-1),(1.9,.6)]])
    return VGroup(outline,nuclei)


def em_inset():
    # Small inset, same full-height membrane convention as the chemical schematic.
    fr=box(4.65,-1.2,3.4,3.15,GREY,.02)
    cells=VGroup(*[Rectangle(width=1.55,height=3.15,stroke_width=0,fill_color=c,fill_opacity=.25).move_to([x,-1.2,0]) for x,c in [(3.75,BLUE),(5.55,YELLOW)]])
    return VGroup(fr,cells,line((4.5,-2.775),(4.5,.375)),line((4.8,-2.775),(4.8,.375)),
                  txt('two membranes',4.65,1.05,c=GREEN,size=26),txt('cleft',4.65,-3.25,size=26),
                  arrow((4.65,-3),(4.65,-2.55)),txt('electron microscope',4.65,1.75,c=VIOLET,size=26))


def spread_dots(final=False):
    rs=np.random.RandomState(4)
    ds=VGroup(); targets=[]
    for k in range(18):
        x=-4.8+rs.uniform(-.1,.1); y=-.25+rs.uniform(-.35,.35)
        tx=-4.5+7.2*k/17; ty=.95*np.sin(k*2.4)
        ds.add(Dot([tx if final else x,ty if final else y,0],radius=.14,color=MAGENTA))
        targets.append([tx,ty,0])
    return ds,targets


class S20Rev3(Speech):
    def construct(self):
        syn=syncytium(); ds,targets=spread_dots()
        nuc_label=VGroup(txt('many nuclei',-2.9,-3.3,size=28),arrow((-2.9,-3),(-.9,-1.45)))
        injection_label=VGroup(txt('injection',-4.5,2.5,c=MAGENTA,size=26),arrow((-4.5,2.2),(-4.8,.2),MAGENTA))
        self.add(syn,txt('syncytium: one shared cytoplasm',0,3.35,c=GREEN,size=32),nuc_label)
        self.at('shared cytoplasm'); self.add(ds,injection_label)
        self.at('would spread')
        time=txt('time →',0,2.5,c=MAGENTA,size=30); self.add(time)
        # Start locally and expand across the continuous space over several seconds.
        self.play(*[d.animate.move_to(t) for d,t in zip(ds,targets)],run_time=2.4,rate_func=linear)
        self.at('electron microscope')
        # Retain the large syncytium at left; reserve a genuinely small inset at right.
        group=VGroup(syn,ds)
        self.play(group.animate.scale(.68).move_to([-2.6,-.25,0]),FadeOut(nuc_label),FadeOut(injection_label),run_time=.5)
        inset=em_inset(); self.add(inset[0],inset[1],inset[-1])
        self.at('two membranes'); self.add(*inset[2:])
        self.finish()


class S21Beat(NarratedScene):
    def construct(self):
        ds,_=spread_dots(True)
        self.add(VGroup(syncytium(),ds).scale(.68).move_to([-2.6,-.25,0]),em_inset(),
                 txt('syncytium: one shared cytoplasm',0,3.35,c=GREEN,size=32),txt('time →',0,2.5,c=MAGENTA,size=30))
        self.finish()


class S22Scope(Speech):
    def construct(self):
        self.add(junction(),halves(),txt('in vertebrates',0,3.35,size=34),
                 txt('coupling through regulated pores,',0,-3.05,c=TEAL,size=28),
                 txt('not one fused net',0,-3.6,c=TEAL,size=28))
        # Small dismissed alternative; the regulated junction remains the subject.
        nodes=[(-5.7,1.3),(-4.4,1.4),(-3,.9),(-5.5,-.5),(-4.3,.35),(-3.1,-.6)]
        edges=[(0,1),(1,2),(0,4),(1,4),(2,4),(3,4),(4,5),(3,5)]
        net=VGroup(*[line(nodes[a],nodes[b],ORANGE,4) for a,b in edges],
                   *[Dot([x,y,0],radius=.14,color=ORANGE) for x,y in nodes])
        self.add(net,txt("Golgi's network",-4.3,2.1,c=ORANGE,size=26))
        self.at('does not exist')
        self.add(line((-5.6,1.6),(-3,-.5),RED,4),line((-5.6,-.5),(-3,1.6),RED,4))
        self.at('coupling through')
        state=txt('OPEN',3.9,.9,c=TEAL,size=30)
        pointer=arrow((2.8,.6),(0,-.2),TEAL)
        self.add(state,pointer)
        flow=Dot([-.9,-.2,0],radius=.12,color=TEAL); self.add(flow)
        self.play(flow.animate.shift(RIGHT*2),run_time=.6,rate_func=linear)
        self.at('can close')
        self.remove(flow)
        gate=line((0,-.65),(0,.25),RED,9)
        self.remove(state,pointer)
        self.add(gate,txt('CLOSED',3.9,.9,c=RED,size=30),arrow((2.8,.6),(0,-.2),RED)); self.finish()


def fused_tubes():
    # A single boolean-unioned outline: three fibres become one wide tube.
    parts=[RoundedRectangle(width=3.8,height=1.25,corner_radius=.6).move_to([-2.4,-.15,0])]
    for y in [-2,0,2]:
        a=np.array([-5.8,y,0]); b=np.array([-3.5,-.15,0]); delta=b-a
        parts.append(Rectangle(width=np.linalg.norm(delta)+.25,height=.46).rotate(np.arctan2(delta[1],delta[0])).move_to((a+b)/2))
        parts.append(Circle(radius=.23).move_to(a))
    outline=Union(*parts,stroke_color=GREEN,stroke_width=5,fill_color=ORANGE,fill_opacity=.22)
    fibres=VGroup(*[path([(-5.8,y),(-3.5,-.15),(-2.8,-.15+offset),(-.65,-.15+offset)],ORANGE,3)
                    for y,offset in [(-2,-.28),(0,0),(2,.28)]])
    return VGroup(outline,fibres)


def continuous_net():
    # Union the tubular paths BEFORE stroking: no discrete nodes or cell borders.
    pts=[(1.1,1.7),(3.2,2),(5.9,1.4),(1.5,-.1),(3.4,.1),(5.7,-.4),(1.1,-2),(3.3,-1.6),(6,-2)]
    edges=[(0,1),(1,2),(1,4),(3,4),(4,5),(3,6),(4,7),(7,8)]
    parts=[Circle(radius=.2).move_to([*p,0]) for p in pts]
    for a,b in edges:
        p=np.array([*pts[a],0]); q=np.array([*pts[b],0]); d=q-p
        parts.append(Rectangle(width=np.linalg.norm(d),height=.4).rotate(np.arctan2(d[1],d[0])).move_to((p+q)/2))
    return Union(*parts,stroke_color=GREEN,stroke_width=4,fill_color=ORANGE,fill_opacity=.24)


class S23Scope2(Speech):
    def construct(self):
        self.add(txt('exceptions outside vertebrates',0,3.35,c=ORANGE,size=34),
                 txt('in these animals',0,-3.4,size=28))
        # Carry a useful silhouette from the first frame; reveal each panel at its name.
        sq=fused_tubes()
        sq_label=txt('squid giant axon',-3.35,2.7,size=28)
        sq_group=VGroup(sq,sq_label).shift(RIGHT*3.1)
        self.add(sq_group)
        self.at('fused fibers')
        self.play(Indicate(sq[1],scale_factor=1.015),run_time=.7)
        fibre_label=txt('fibres merge into one tube',-.2,-2.7,c=ORANGE,size=26)
        self.add(fibre_label)
        self.at('a comb')
        self.play(sq_group.animate.shift(LEFT*3.1),fibre_label.animate.shift(LEFT*3.1),
                  FadeIn(continuous_net()),run_time=.5)
        self.add(txt('comb jelly nerve net',3.5,2.7,size=28))
        self.at('shares one membrane')
        self.add(txt('one continuous membrane',3.5,-2.7,c=GREEN,size=26))
        self.finish()


class S24Take(Speech):
    def construct(self):
        # Two distinct contact cases, large and central, with two outlines per pair.
        touch=VGroup(*[Ellipse(width=2.6,height=4.8,stroke_color=c,stroke_width=4,fill_color=c,fill_opacity=.12).move_to([x,-.2,0]) for x,c in [(-4.65,BLUE),(-2.05,YELLOW)]])
        pore=VGroup(box(1.85,-.2,2.5,4.8,BLUE),box(4.65,-.2,2.5,4.8,YELLOW),
                    line((2.9,0),(3.6,0),TEAL,6),line((2.9,-.4),(3.6,-.4),TEAL,6))
        self.add(txt('A touch is not a fusion',0,3.35,size=36),touch,
                 txt('touch: two cell boundaries',-3.35,-3.15,c=GREEN,size=26))
        # Clear the two membrane segments only where the pore lumen crosses.
        for x in [3.1,3.4]:
            pore.add(Rectangle(width=.09,height=.28,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([x,-.2,0]))
        self.at('and neither is a pore')
        self.add(pore,txt('pore: a regulated opening',3.35,-3.15,c=TEAL,size=26),txt('and neither is a pore',3.35,2.7,size=28))
        self.at('separate cells')
        self.clear()
        self.add(txt('Separate cells, specialized contacts',0,3.35,c=GREEN,size=34))
        cells=VGroup(*[Circle(radius=1.2,stroke_color=GREEN,stroke_width=5,fill_color=c,fill_opacity=.2).move_to([x,y,0]) for x,y,c in [(-4.6,1.1,BLUE),(0,-1.6,YELLOW),(4.6,1.1,BLUE)]])
        self.add(cells)
        self.at('specialized contacts')
        branch1=path([(-3.8,.2),(-2.8,-.65),(-1.2,-1.6)],BLUE,10)
        self.play(Create(branch1),run_time=.5)
        self.add(line((-1.27,-1.9),(-1.27,-1.3),GREEN,5))
        self.at('are what development')
        branch2=path([(1.1,-1.1),(2.3,-.5),(3.45,.8)],YELLOW,10)
        self.play(Create(branch2),run_time=.9)
        self.add(line((3.45,.5),(3.45,1.1),GREEN,5),txt('development grows branches to contacts',0,-3.4,c=GREEN,size=28))
        self.finish()


class S25End(EndCard):
    LINE='Separate cells, joined at specialized contacts.'
