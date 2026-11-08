"""Timing in the bulb: all plots are schematic, never experimental traces.
COLOR MAP (reference scenes.old.py; kept here because CHAPTERS.md is read-only
under this task's edit-only restriction): BLUE sister 1; YELLOW sister 2;
TEAL shared glomerular input / cortex; GREEN mean rate / learned meaning;
ORANGE timing; PURPLE interneurons / inhibition; GOLD experimental light;
GREY axes, breath, electrodes, labels; RED strike-through only.
OUTPUT pale grey = generic output cells; TYPE1 pink / TYPE2 sage = tufted / mitral.
Breath equation, tick/cluster helpers, circuit curves and cortical sheet are
reused directly from the reference. Ordinal rate bars illustrate the narrated
qualitative finding; they are explicitly not measured values.
"""
from bp_style import *
import importlib.util
import numpy as np

_spec = importlib.util.spec_from_file_location('reference', Path(__file__).parent.parent / 'scenes.old.py')
ref = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ref)
ORANGE, PURPLE = ref.ORANGE, ref.PURPLE
bez, ticks, cluster, inhibition = ref.bez, ref.ticks, ref.cluster, ref.inhibition


def label(s, y=3.05, size=30, color=TEXT, x=0):
    return T(s, size, color).move_to([x,y,0])


def wave(x0=-5.5, x1=5.5, y=0, amplitude=1.3):
    # Same normalized respiratory equation as the reference timing_panel.
    ph=np.linspace(0,1,160)
    return VMobject(color=GREY,stroke_width=4).set_points_smoothly([
        np.array([x0+(x1-x0)*t,y+amplitude*np.sin(2*np.pi*t-np.pi/2),0]) for t in ph])


def glomeruli():
    return VGroup(*[Circle(.48,color=TEAL,fill_color=TEAL,fill_opacity=.8 if i in (0,2,3) else .08)
                   .move_to([-4+i*2,1.2,0]) for i in range(5)])


# Circuit cartoons use neutral output-cell colour; blue/yellow are sisters only.
OUTPUT = "#B6C5D4"
TYPE1, TYPE2 = "#E79CBA", "#9FBF80"

def on_path(text, x, y, color, size=28):
    # An opaque backing lets the label sit directly on its own signal path.
    return label(text,y,size,color,x).add_background_rectangle(color=BG,opacity=1,buff=.07)


def circuit():
    a=RoundedRectangle(width=8,height=1.6,corner_radius=.5,color=OUTPUT,fill_color=OUTPUT,fill_opacity=.4).move_to([-1.8,1.6,0])
    b=RoundedRectangle(width=8,height=1.6,corner_radius=.5,color=PURPLE,fill_color=PURPLE,fill_opacity=.3).move_to([1.8,-1.6,0])
    names=VGroup(label('mitral / tufted dendrite',2.75,28,OUTPUT,-1.8),label('granule dendrite',-2.75,28,PURPLE,1.8))
    out=Arrow([-1.5,.8,0],[-1.5,-.8,0],buff=0,color=OUTPUT,stroke_width=7,max_tip_length_to_length_ratio=.2)
    path=CubicBezier([1.2,-.8,0],[3.3,-.8,0],[3.3,.8,0],[1.2,.8,0],color=PURPLE,stroke_width=7)
    # Broad terminal bar lies on the lower boundary of the output dendrite.
    back=VGroup(path,Line([.75,.8,0],[1.65,.8,0],color=PURPLE,stroke_width=10))
    contact=VGroup(*[Circle(.3,color=TEXT,stroke_width=2,stroke_opacity=.5).move_to([x,y,0]) for x,y in ((-1.5,.8),(-1.5,-.8),(1.2,.8),(1.2,-.8))])
    return VGroup(a,b,names,out,back,contact)


def transmitters():
    return VGroup(on_path('glutamate',-1.5,0,OUTPUT),on_path('GABA',2.78,0,PURPLE))


def lateral():
    cells=VGroup(*[Circle(.48,color=OUTPUT,fill_color=OUTPUT,fill_opacity=.2).move_to([x,1.7,0]) for x in (-4,0,4)])
    g=Circle(.5,color=PURPLE,fill_color=PURPLE,fill_opacity=.2).move_to([0,-2.15,0])
    dend=VGroup(*[Line([x,1.22,0],[x,.2,0],color=OUTPUT,stroke_width=7) for x in (-4,0,4)],
                *[Line([x-1.2,.4,0],[x+1.2,.4,0],color=OUTPUT,stroke_width=7) for x in (-4,0,4)])
    branches=VGroup(Line([0,-1.65,0],[0,-.8,0],color=PURPLE,stroke_width=7),
                    *[bez((0,-1.1),(x,-.65),.15).set_color(PURPLE) for x in (-4,0,4)])
    names=VGroup(label('mitral cells',2.65,30,OUTPUT),label('lateral dendrites',.9,28,OUTPUT,2.0),label('granule cell (no axon)',-3.05,28,PURPLE))
    return VGroup(cells,g,dend,branches,names)


def sisters(identified=True):
    gl=Circle(.7,color=TEAL,fill_color=TEAL,fill_opacity=.35).move_to([0,1.55,0])
    cs=(BLUE,YELLOW) if identified else (OUTPUT,OUTPUT)
    cells=VGroup(*[Circle(.5,color=c,fill_color=c,fill_opacity=.35).move_to([x,-1.3,0]) for x,c in zip((-3,3),cs)])
    dend=VGroup(*[bez((x,-.8),(-.3 if x<0 else .3,1),.2).set_color(c) for x,c in zip((-3,3),cs)])
    names=VGroup(*[label(('sister ' if identified else 'cell ')+str(i+1),-2.35,28,c,x) for i,(x,c) in enumerate(zip((-3,3),cs))])
    gt=label('one glomerulus',1.65,28,TEAL,-3.4)
    leader=Line([-1.9,1.6,0],[-.85,1.6,0],color=TEAL)
    return VGroup(gl,cells,dend,names,gt,leader)


def timing(empty=False, neutral=False):
    x0,x1=-3.7,5.7
    breath=VGroup(wave(x0,x1,1.5,.8),label('inhalation',2.55,28,GREY,-1.35),label('exhalation',2.55,28,GREY,3.35))
    cs=(OUTPUT,OUTPUT) if neutral else (BLUE,YELLOW)
    names=VGroup(*[label(('cell '+chr(65+i)) if neutral else 'sister '+str(i+1),y,28,c,-5.1) for i,(y,c) in enumerate(zip((-.3,-1.6),cs))])
    rows=VGroup(*[Line([x0,y,0],[x1,y,0],color=GREY,stroke_opacity=.45) for y in (-.3,-1.6)])
    axis=VGroup(Arrow([x0,-2.4,0],[x1,-2.4,0],buff=0,color=GREY),label('one breathing cycle',-3.15,28,GREY,1),DashedLine([x0,-2.4,0],[x0,2.3,0],color=GREY,stroke_opacity=.4))
    spikes=VGroup() if empty else VGroup(ticks(x0,x1,-.3,cluster(.32),cs[0],.65),ticks(x0,x1,-1.6,cluster(.61),cs[1],.65))
    return VGroup(breath,names,rows,axis,spikes)


def comparison(changed=False):
    # Illustrative offset baseline phases; odour shifts +.22 / -.08.
    # Counts remain four per row. No experimental values or absolute phase order implied.
    panels=VGroup(); spikes=VGroup()
    for j,(x0,x1) in enumerate(((-3.8,.3),(1.6,5.7))):
        panels.add(label('baseline' if j==0 else 'odour',2.0,30,GREY,(x0+x1)/2),wave(x0,x1,1.1,.5),
                   DashedLine([x0,-2.1,0],[x0,1.6,0],color=GREY,stroke_opacity=.4))
        for i,(y,c) in enumerate(((-.45,BLUE),(-1.7,YELLOW))):
            panels.add(Line([x0,y,0],[x1,y,0],color=GREY,stroke_opacity=.35))
            ph=(.38 if i==0 else .46) + ((.22 if i==0 else -.08) if changed and j else 0)
            spikes.add(ticks(x0,x1,y,cluster(ph,step=.035),c,.65))
        panels.add(Arrow([x0,-2.5,0],[x1,-2.5,0],buff=0,color=GREY))
    names=VGroup(label('sister 1',-.45,28,BLUE,-5.1),label('sister 2',-1.7,28,YELLOW,-5.1))
    footer=label('one breathing cycle per condition • schematic',-3.15,28,GREY)
    return VGroup(panels,names,spikes,footer)


def prediction():
    boxes=VGroup(*[RoundedRectangle(width=5.6,height=4.4,corner_radius=.15,color=GREY).move_to([x,-.1,0]) for x in (-3,3)])
    headings=VGroup(label('Mean rate',2.5,30,GREEN,-3),label('Timing against breath',2.5,30,ORANGE,3))
    left=VGroup(Line([-4.9,-1.2,0],[-.7,-1.2,0],color=GREY),Line([-4.9,-1.2,0],[-4.9,1.4,0],color=GREY),label('odours',-1.85,28,GREY,-2.8),T('rate',28,GREY).rotate(PI/2).move_to([-5.45,.2,0]))
    right=VGroup(wave(2,5.5,1.1,.4),Line([2,-.2,0],[5.5,-.2,0],color=BLUE),Line([2,-1.05,0],[5.5,-1.05,0],color=YELLOW),
                 label('sister 1',-.2,28,BLUE,1.1),label('sister 2',-1.05,28,YELLOW,1.1),label('one breathing cycle',-1.85,28,GREY,3.5))
    q=label('Match or differ?',-3,34)
    return VGroup(boxes,headings,left,right,q)


def rate_panel():
    bars=VGroup()
    # Explicit ordinal illustrative tuning model, with a shared odour term and cell-specific offset.
    tuning=np.array([1.,2.5,1.6,2.9]); second=.82*tuning+.32
    for i,(a,b) in enumerate(zip(tuning,second)):
        x=-3.7+i*2.7
        for off,h,c in [(-.28,a,BLUE),(.28,b,YELLOW)]:
            bars.add(Rectangle(width=.42,height=h,color=c,fill_color=c,fill_opacity=.8).move_to([x+off,-1.8+h/2,0]))
    axes=VGroup(Line([-4.8,-1.8,0],[5.4,-1.8,0],color=GREY),Line([-4.8,-1.8,0],[-4.8,1.5,0],color=GREY),T('mean spike rate',28,GREY).rotate(PI/2).move_to([-5.65,-.1,0]))
    od=VGroup(*[label('odour '+v,-2.3,28,GREY,-3.7+i*2.7) for i,v in enumerate('ABCD')])
    key=VGroup(*[VGroup(Square(.22,color=c,fill_color=c,fill_opacity=1).move_to([x,2.15,0]),label('sister '+str(i+1),2.15,28,c,x+1)) for i,(x,c) in enumerate(((-4.5,BLUE),(-.7,YELLOW)))])
    return VGroup(bars,axes,od,key,label('Schematic • no measured scale',-3.15,28,GREY))


def caveats():
    return VGroup(chip('anaesthetized',GREY,28).move_to([-3,3,0]),chip('mitral + tufted pooled',GREY,28).move_to([3,3,0]))


def sniff_base():
    return VGroup(wave(amplitude=1.8),label('One sniff',3.15,34,ORANGE),
                  Arrow([-5.5,-2.25,0],[5.5,-2.25,0],buff=0,color=GREY),
                  label('cycle start',-3.05,28,GREY,-4.8),label('cycle end',-3.05,28,GREY,4.8),label('time',-3.05,28,GREY),
                  DashedLine([-5.5,-2.25,0],[-5.5,2.1,0],color=GREY),DashedLine([5.5,-2.25,0],[5.5,2.1,0],color=GREY))


class S00Title(TitleCard):
    LESSON='From Glomeruli to Piriform Cortex'
    TITLE='More Than a Map: Timing in the Bulb'
    def construct(self):
        # House card with readable type rather than shrinking the long title.
        self.add(label('BIOCHEMISTRYPEDIA',2.5,22,TEAL),label(self.LESSON,1.65,28,GREY))
        self.play(FadeIn(VGroup(label('More Than a Map:',.35,46),label('Timing in the Bulb',-.65,46))),run_time=.8)
        self.add(Line([-1.3,-1.65,0],[1.3,-1.65,0],color=GOLD))
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        self.add(glomeruli(),wave(y=-1.2,amplitude=1),label('active glomeruli',2.7,30,TEAL),label('sniff',-2.8,30,GREY))
        self.at('Is that all')
        self.play(FadeIn(label('All the cortex receives?',3.4,32)),run_time=.5)
        self.finish()


class S02Richer(SpokenScene):
    def construct(self):
        g=glomeruli(); self.add(g,wave(y=-1.4,amplitude=.8),label('active glomeruli',2.7,30,TEAL),label('sniff',-3.1,28,GREY))
        pg=Dot([0,0,0],radius=.25,color=PURPLE); link=inhibition([0,.2,0],[0,.65,0])
        self.at('the bulb reshapes')
        self.play(FadeIn(pg),Create(link),run_time=.4)
        self.at('with inhibition')
        self.play(g[2].animate.set_fill(TEAL,.12),FadeIn(label('inhibition',.0,30,PURPLE,2)),run_time=.5)
        self.at('carries timing')
        self.play(FadeIn(label('timing',-2.5,30,ORANGE,3.8)),Create(ticks(-5.5,5.5,-1.4,[.23,.69],ORANGE,.75)),run_time=.5)
        self.finish()


class S03Dd(SpokenScene):
    def construct(self):
        c=circuit(); self.add(c[0],c[1],c[2],c[5])
        self.at('a reciprocal')
        self.play(FadeIn(label('Reciprocal dendrodendritic contact',3.35,32)),Create(VGroup(c[3],c[4])),run_time=.7)
        self.at('one dendrite')
        self.play(Indicate(c[3],color=OUTPUT),run_time=.5)
        self.at('and back')
        self.play(Indicate(c[4],color=PURPLE),run_time=.4)
        self.finish()


class S04Transmitters(SpokenScene):
    def construct(self):
        c=circuit(); t=transmitters(); self.add(c,label('Reciprocal dendrodendritic contact',3.35,32))
        self.at('releases glutamate')
        self.play(Indicate(c[3],color=OUTPUT),FadeIn(t[0]),c[1].animate.set_fill(PURPLE,.7),run_time=.6)
        self.at('releases GABA')
        self.play(Indicate(c[4],color=PURPLE),FadeIn(t[1]),run_time=.6)
        self.finish()


class S05Recurrent(SpokenScene):
    def construct(self):
        c=circuit(); self.add(c,transmitters())
        self.at('The loop')
        self.play(c[0].animate.set_fill(OUTPUT,.85),Indicate(c[3],color=OUTPUT),run_time=.45)
        self.play(c[1].animate.set_fill(PURPLE,.85),run_time=.35)
        self.at('can inhibit')
        self.play(Indicate(c[4],color=PURPLE),run_time=.4)
        self.play(c[0].animate.set_fill(OUTPUT,.1),FadeIn(label('Recurrent inhibition',3.35,34,PURPLE)),run_time=.45)
        self.finish()


class S06Lateral(SpokenScene):
    def construct(self):
        p=lateral(); self.add(p)
        self.at('touches many')
        self.play(Indicate(p[3],color=PURPLE),run_time=.4)
        self.play(p[0][1].animate.set_fill(OUTPUT,.95),run_time=.35)
        ex=Arrow([.65,.4,0],[.65,-.8,0],buff=0,color=OUTPUT,stroke_width=6)
        self.play(GrowArrow(ex),FadeIn(on_path('glutamate',.65,-.2,OUTPUT)),p[1].animate.set_fill(PURPLE,.8),run_time=.5)
        self.at('also inhibit')
        back=VGroup(*[VGroup(Line([x,-.65,0],[x,.4,0],color=PURPLE,stroke_width=7),Line([x-.45,.4,0],[x+.45,.4,0],color=PURPLE,stroke_width=10),on_path('GABA',x,-.25,PURPLE)) for x in (-4,4)])
        self.play(FadeIn(back),run_time=.4)
        self.play(*[p[0][i].animate.set_fill(OUTPUT,.05) for i in (0,2)],FadeIn(label('Lateral inhibition',3.4,34,PURPLE)),run_time=.5)
        self.finish()


class S06bNotOnly(SpokenScene):
    def construct(self):
        gl=Circle(1.25,color=TEAL,fill_color=TEAL,fill_opacity=.15).move_to([2,0,0])
        pg=Circle(.65,color=PURPLE,fill_color=PURPLE,fill_opacity=.12).move_to([-2.7,0,0])
        self.add(gl,pg,label('glomerulus',2,30,TEAL,2),label('periglomerular cell',-1.3,30,PURPLE,-2.7))
        self.at('not the only')
        self.play(pg.animate.set_fill(PURPLE,.9),run_time=.35)
        self.at('source of this')
        self.play(Create(inhibition([-2.05,0,0],[.7,0,0])),gl.animate.set_fill(TEAL,.65),FadeIn(label('Not granule cells alone',3.15,34,PURPLE)),run_time=.6)
        self.finish()


class S07NotRetina(SpokenScene):
    def construct(self):
        cells=VGroup(*[Circle(.5,color=OUTPUT,fill_opacity=.3,fill_color=OUTPUT).move_to([x,1.15,0]) for x in (-5.3,-3.5,-1.7)])
        dend=VGroup(*[VGroup(Line([x,.65,0],[x,-.25,0],color=OUTPUT,stroke_width=6),Line([x-.65,-.25,0],[x+.65,-.25,0],color=OUTPUT,stroke_width=6)) for x in (-5.3,-3.5,-1.7)])
        gc=Dot([-3.5,-1.95,0],radius=.5,color=PURPLE)
        branches=VGroup(*[bez((-3.5,-1.45),(x,-.25),.2).set_color(PURPLE) for x in (-5.3,-3.5,-1.7)])
        ring=VGroup(Circle(2,color=PURPLE,fill_color=PURPLE,fill_opacity=.25),Circle(.8,color=GREEN,fill_color=GREEN,fill_opacity=.35),T('+',64,GREEN,weight=BOLD),*[T('−',54,PURPLE,weight=BOLD).move_to([x,y,0]) for x,y in ((0,1.4),(0,-1.4),(1.4,0),(-1.4,0))]).move_to([3.5,.1,0])
        self.add(cells,dend,gc,branches,ring,label('bulb circuit',2.65,32,OUTPUT,-3.5),label('retina: centre–surround',2.65,30,TEXT,3.5),label('centre excited (+)',-2.5,28,GREEN,3.5),label('surround inhibited (−)',-3.15,28,PURPLE,3.5))
        self.at('lateral inhibition')
        self.play(Indicate(branches,color=PURPLE),FadeIn(label('The bulb is not a retina',3.35,34)),run_time=.4)
        self.at('But the bulb')
        self.play(FadeIn(T('≠',60).move_to([0,0,0])),run_time=.5)
        self.finish()


class S07bWhy(SpokenScene):
    def construct(self):
        gl=VGroup(*[Circle(.4,color=TEAL).move_to([x,y,0]) for x,y in [(-5.2,1.9),(-2.6,2.1),(-4.3,.1),(-1.2,.6),(-1.5,-1.6)]])
        cell=Circle(.5,color=OUTPUT,fill_color=OUTPUT,fill_opacity=.4).move_to([-4.4,-2.1,0])
        ring=VGroup(Circle(1.5,color=GREY),Dot(radius=.2,color=GREY)).move_to([3.4,.2,0]).set_opacity(.4)
        self.add(gl,cell,ring,label('glomeruli',3.2,30,TEAL,-3.5),label('mitral cell',-3.1,28,OUTPUT,-4.4),label('neighbour ring',-2,30,GREY,3.4))
        self.at('influenced by')
        self.play(Create(VGroup(*[Line(cell.get_top(),gl[i].get_bottom(),color=TEAL) for i in (0,1,3)])),run_time=.6)
        self.at('not a ring',lead=0)
        d=1.5/np.sqrt(2)
        self.play(Create(Line([3.4-d,.2-d,0],[3.4+d,.2+d,0],color=RED,stroke_width=6)),run_time=.2)
        self.finish()


class S08Sniff(SpokenScene):
    def construct(self):
        self.add(sniff_base())
        self.at('breathing in')
        self.play(FadeIn(label('inhalation',2.35,28,GREY,-2.8)),run_time=.35)
        self.at('breathing out')
        self.play(FadeIn(label('exhalation',2.35,28,GREY,2.8)),run_time=.35)
        self.finish()


class S09Phase(SpokenScene):
    def construct(self):
        self.add(sniff_base(),label('inhalation',2.35,28,GREY,-2.8),label('exhalation',2.35,28,GREY,2.8))
        ph=.23; x=-5.5+11*ph; y=1.8*np.sin(2*np.pi*ph-np.pi/2)
        self.at('phase is')
        self.play(Create(ticks(-5.5,5.5,y,[ph],ORANGE,1)),run_time=.3)
        bracket=VGroup(Line([-5.5,1.5,0],[x,1.5,0],color=ORANGE),*[Line([v,1.35,0],[v,1.65,0],color=ORANGE) for v in (-5.5,x)],label('phase',1.95,30,ORANGE,(-5.5+x)/2))
        self.at('where in that cycle')
        self.play(Create(DashedLine([x,1.5,0],[x,y+.5,0],color=ORANGE)),FadeIn(bracket),run_time=.35)
        self.finish()


class S10Uchida(SpokenScene):
    def construct(self):
        p=timing(empty=True,neutral=True); self.add(p,label('Schematic • not sister-cell data',-3.65,28,GREY))
        self.at('A review')
        self.play(FadeIn(label('Uchida and colleagues • 2014 review',3.35,28)),run_time=.35)
        self.at('relative timing')
        self.play(Create(ticks(-3.7,5.7,-.3,cluster(.32),OUTPUT,.65)),run_time=.4)
        self.at('activity in the bulb')
        self.play(Create(ticks(-3.7,5.7,-1.6,cluster(.61),OUTPUT,.65)),run_time=.4)
        self.at('conveys')
        self.play(Indicate(p[0],color=ORANGE,scale_factor=1.02),run_time=.4)
        self.finish()


class S11Debated(SpokenScene):
    def construct(self):
        p=timing(neutral=True)
        # Full-size plot above a broad, readable downstream cortex destination.
        p.remove(p[3]); p.shift(UP*.1)
        self.add(p)
        ctx=chip('downstream cortex',TEAL,36,pad=.3).move_to([3,-2.9,0])
        ar=Arrow([-.8,-2.9,0],[.5,-2.9,0],buff=0,color=TEAL,stroke_width=6)
        self.at('downstream circuits')
        self.play(FadeIn(ctx),GrowArrow(ar),run_time=.4)
        self.at('debated',lead=.1)
        self.play(FadeIn(label('?',-2.9,52,ORANGE,-1.7)),FadeIn(label('Use of timing: debated',3.35,34)),run_time=.2)
        self.finish()


class S12TwoTypes(SpokenScene):
    def construct(self):
        # Two vertically stacked cycles, colours distinct from sisters; phases are illustrative.
        self.add(label('Fukunaga and colleagues • 2012',3.35,28),label('Schematic phases • one sniff per row',-3.3,28,GREY))
        rows=VGroup()
        for y,name,c in ((1.4,'tufted',TYPE1),(-1.2,'mitral',TYPE2)):
            rows.add(wave(-3.6,5.5,y,.7),label(name,y,32,c,-5),label('different phase of one sniff',y-1.05,28,GREY,1))
        self.add(rows)
        self.at('cells lock')
        self.play(Create(ticks(-3.6,5.5,1.4,cluster(.15),TYPE1,.8)),run_time=.4)
        self.at('opposite phases')
        self.play(Create(ticks(-3.6,5.5,-1.2,cluster(.65),TYPE2,.8)),run_time=.4)
        self.at('parallel channels')
        self.play(FadeIn(label('Parallel channels',2.7,32,ORANGE)),run_time=.35)
        self.finish()


class S13SisterQ(SpokenScene):
    def construct(self):
        p=sisters(False); self.add(p,label('Two cells, one input?',3.25,34))
        self.at('share one glomerulus')
        self.play(Indicate(p[0],color=TEAL),run_time=.5)
        self.at('send the same message')
        self.play(FadeIn(label('Same message?',-3.25,34)),run_time=.4)
        self.finish()


class S14Dhawale(SpokenScene):
    def construct(self):
        self.add(sisters(False))
        self.at('and colleagues')
        self.play(FadeIn(label('Dhawale and colleagues • 2010',3.25,30)),run_time=.3)
        probes=VGroup(Line([-4.5,.1,0],[-3.6,-1.25,0],color=GREY,stroke_width=6),Line([4.5,.1,0],[3.6,-1.25,0],color=GREY,stroke_width=6))
        self.at('recorded in')
        self.play(Create(probes),FadeIn(label('electrode',.5,28,GREY,-4.9)),FadeIn(label('electrode',.5,28,GREY,4.9)),run_time=.35)
        self.at('adult mice')
        self.play(FadeIn(label('adult anaesthetized mice',-3.25,30)),run_time=.3)
        self.finish()


class S15LightId(SpokenScene):
    def construct(self):
        p=sisters(False); self.add(p)
        beam=Polygon([-.35,3.3,0],[-1.1,1.1,0],[1.1,1.1,0],[.35,3.3,0],stroke_width=0,fill_color=GOLD,fill_opacity=.2)
        self.at('method found')
        self.play(FadeIn(beam),p[0].animate.set_fill(GOLD,.8),run_time=.5)
        self.at('recorded cells')
        identified=sisters()
        for c in identified[1]: c.set_fill(c.get_color(),.9)
        self.play(*[Transform(p[i],identified[i]) for i in (1,2,3)],run_time=.5)
        self.at('one parent glomerulus')
        self.play(FadeIn(label('Identified by shared input',-3.25,30,GOLD)),run_time=.4)
        self.finish()


class S16ByInput(SpokenScene):
    def construct(self):
        self.add(sisters())
        self.at('sisters were defined')
        self.play(Indicate(self.mobjects[0][0],color=TEAL),run_time=.4)
        self.at('not by how')
        self.play(FadeIn(label('Odour response was not the selection rule',-3.25,30,GREY)),run_time=.4)
        self.finish()


class S17Predict(SpokenScene):
    def construct(self):
        p=prediction(); self.add(p[0],p[2],p[3])
        self.at('Pause and predict')
        self.play(FadeIn(label('Sisters share one input',3.15,30,GOLD)),run_time=.5)
        self.at('their rates match')
        self.play(FadeIn(p[1][0]),run_time=.4)
        self.at('their timing against')
        self.play(FadeIn(p[1][1]),FadeIn(p[4]),run_time=.4)
        self.finish()


class S18Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(prediction(),label('Sisters share one input',3.15,30,GOLD))
        self.wait(5)


class S19Rates(SpokenScene):
    def construct(self):
        p=rate_panel(); self.add(p[1],p[2],p[3],p[4])
        self.at('mean spikes')
        self.play(FadeIn(p[0]),run_time=.7)
        self.at('were correlated')
        self.play(FadeIn(label('Correlated tuning, not equal rates',3.15,32,GREEN)),run_time=.5)
        self.finish()


class S20Timing(SpokenScene):
    def construct(self):
        p=comparison(); self.add(p,label('Odour-dependent timing shifts',3.15,32,ORANGE))
        self.at('breathing cycle')
        self.play(Indicate(p[0],color=GREY,scale_factor=1.01),run_time=.35)
        self.at('shifted the timing')
        self.play(Transform(p[2],comparison(True)[2]),run_time=.8)
        self.finish()


class S21Address(SpokenScene):
    def construct(self):
        p=comparison(True); self.add(p)
        self.at('Rate made')
        bars=VGroup(*[Rectangle(width=.3,height=h,color=c,fill_color=c,fill_opacity=.85).move_to([x,2.4+h/2,0]) for x,h,c in ((-1.9,.62,BLUE),(-1.45,.7,YELLOW))],label('Mean rate: alike',2.8,28,GREEN,1.2))
        self.play(FadeIn(bars),run_time=.2)
        self.at('Timing did not')
        self.play(FadeOut(bars),Indicate(p[2][2:],color=ORANGE),run_time=.4)
        self.at('a shared address')
        self.play(*[FadeOut(m) for m in self.mobjects],run_time=.2)
        self.play(FadeIn(sisters()),FadeIn(label('A shared address',3.25,34,GOLD)),run_time=.3)
        self.at('not a shared message')
        self.play(FadeIn(label('not a shared message',-3.25,34,ORANGE)),run_time=.4)
        self.finish()


class S22Limits(SpokenScene):
    def construct(self):
        p=comparison(True); self.add(p)
        tags=caveats()
        self.at('within its limits')
        self.play(Indicate(p[2],color=GREY,scale_factor=1.01),run_time=.35)
        self.at('mice were')
        self.play(FadeIn(tags[0]),run_time=.4)
        self.at('mitral and tufted')
        self.play(FadeIn(tags[1]),run_time=.4)
        self.finish()


class S23State(SpokenScene):
    def construct(self):
        p=comparison(True); tags=caveats(); self.add(p,tags)
        # Both limitations point to one enclosure spanning both conditions.
        both=DashedVMobject(RoundedRectangle(width=10.1,height=5.2,corner_radius=.12).move_to([.95,-.2,0]),num_dashes=75).set_color(GREY)
        self.at('may reflect cell type')
        pooled=DashedLine([3,2.65,0],[3,2.4,0],color=GREY)
        self.play(Create(both),Create(pooled),FadeIn(label('cell type?',3.65,30,GREY,3)),run_time=.4)
        self.at('or state')
        state=DashedLine([-3,2.65,0],[-3,2.4,0],color=GREY)
        self.play(Create(state),FadeIn(label('state?',3.65,30,GREY,-3)),run_time=.4)
        self.finish()


class S24Takeaway(SpokenScene):
    def construct(self):
        g=VGroup(*[Circle(.4,color=TEAL,fill_color=TEAL,fill_opacity=.65).move_to([-5.6+i*.9,1.7,0]) for i in range(5)])
        w=wave(-5.8,-1.5,-.6,.8)
        border=RoundedRectangle(width=5.6,height=5.3,corner_radius=.25,color=GREY).move_to([3.35,0,0])
        # Fixed cortical cells: drift changes membership, never anatomical positions.
        cells=VGroup(*[Dot([1.35+c*1.3,1.6-r*1.55,0],radius=.18,color=GREY).set_opacity(.4) for r in range(3) for c in range(4)])
        self.add(g,w,border,cells,label('bulb input',3.25,30,TEAL,-3.6),label('piriform cortex',3.25,30,TEAL,3.35),Arrow([-.9,0,0],[.4,0,0],buff=0,color=TEAL))
        self.at('a timed map')
        self.play(Create(ticks(-5.8,-1.5,-.6,[.23,.69],ORANGE,.75)),run_time=.4)
        self.at('shaped by inhibition')
        pg=Dot([-3.8,.6,0],radius=.24,color=PURPLE)
        links=VGroup(inhibition([-3.8,.8,0],[-3.8,1.25,0]),inhibition([-3.6,.5,0],[-2.8,-.3,0]))
        self.play(FadeIn(pg),Create(links),g[2].animate.set_fill(TEAL,.1),FadeIn(label('inhibition',-2.4,30,PURPLE,-3.6)),run_time=.5)
        self.at('a distributed code')
        self.play(*ref.activity(cells,(0,3,5,10)),run_time=.5)
        self.at('its network reshapes')
        status=label('distributed → reshaped',-3.15,28,TEAL,3.35)
        self.play(*ref.activity(cells,(0,2,3,5,7,10)),FadeIn(status),run_time=.6)
        self.at('that drifts')
        self.play(*ref.activity(cells,(1,2,5,6,9,11)),Transform(status,label('reshaped → drifting',-3.15,28,TEAL,3.35)),run_time=.65)
        self.finish()


class S25End(EndCard):
    LINE='A timed map shaped by inhibition goes in; a distributed, reshaped, drifting code comes out.'
    def construct(self):
        self.add(label('A timed map shaped by inhibition goes in;',.65,40),label('a distributed, reshaped, drifting code comes out.',-.4,40),label('biochemistrypedia.com',-1.8,28,TEAL))
        self.finish()

