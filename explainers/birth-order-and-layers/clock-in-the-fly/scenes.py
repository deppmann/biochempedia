"""A Clock in the Fly: revised, word-timed schematic animation.
COLOR MAP: Hb/early ORANGE #F29E4C; Kr/second YELLOW; Pdm GREEN;
Cas BLUE; neuroblasts PURPLE #B58CD9; loss RED; structure GREY.
All diagrams are qualitative schematics; there are no plotted traces.
"""
from bp_style import *
from bp_style import SpokenScene as _SpokenScene
import numpy as np

ORANGE = '#F29E4C'
PURPLE = '#B58CD9'
COL = [ORANGE, YELLOW, GREEN, BLUE]
NAMES = ['Hunchback', 'Krüppel', 'Pdm', 'Castor']
SHORT = ['Hb', 'Kr', 'Pdm', 'Cas']
LESSON = 'Birth Order and Fate: Temporal Identity and the Inside-Out Cortex'

class SpokenScene(_SpokenScene):
    # Exact word times, with a short visual lead. Keep pipeline logs outside the project.
    def at(self, phrase, lead=.12, nth=0):
        target = max(0, self.t_of(phrase, nth)-lead)
        now = self.elapsed()
        with open('/tmp/clock-fix-sync.log', 'a') as f:
            f.write(f'{os.environ["KX_SCENE_ID"]} {phrase!r} target={target:.3f} now={now:.3f} late={max(0,now-target):.3f}\n')
        if target > now+.02:
            self.wait(target-now)


def label(s, x=0, y=3.1, size=28, color=TEXT):
    return T(s, size=size, color=color, line_spacing=.8).move_to([x,y,0])


def cell(c=PURPLE, r=.65, x=0, y=0):
    return Circle(radius=r, color=c, stroke_width=3, fill_color=c, fill_opacity=.24).move_to([x,y,0])


def neuron(c=GREY, x=0, y=0, name=None, dual=False, other=False):
    # Branched dendrites above a soma, one long axon below: never a person/tripod.
    soma = (Triangle(color=c, fill_color=c, fill_opacity=.28).scale(.32)
            if other else cell(c,.30))
    soma.move_to([0,.25,0])
    arbor=VGroup(Line([0,.5,0],[0,.95,0],color=c,stroke_width=3),
                 Line([0,.7,0],[-.38,.98,0],color=c,stroke_width=3),
                 Line([0,.7,0],[.38,.98,0],color=c,stroke_width=3),
                 Line([-.25,.88,0],[-.43,.83,0],color=c,stroke_width=3),
                 Line([.25,.88,0],[.43,.83,0],color=c,stroke_width=3))
    axon=VMobject(color=c,stroke_width=3).set_points_as_corners([[0,-.05,0],[0,-.5,0],[.22,-.8,0],[.48,-.8,0]])
    if other:
        axon.set_points_as_corners([[0,-.05,0],[-.25,-.4,0],[-.55,-.65,0],[-.8,-.65,0]])
        arbor.stretch(1.5,0)
    g=VGroup(soma,arbor,axon)
    if dual:
        for off in [-.16,0,.16]:
            h=np.sqrt(.27**2-off**2)
            g.add(Line([off,.25-h,0],[off,.25+h,0],color=BLUE,stroke_width=5))
    g.shift([x,y,0])
    if name: g.add(label(name,x,y+1.4,28,c))
    return g


def dial(r=2.35):
    sectors=VGroup(*[AnnularSector(inner_radius=r*.40,outer_radius=r,start_angle=PI/2-i*PI/2,
                        angle=-PI/2,fill_color=c,fill_opacity=.65,stroke_color=BG,stroke_width=5)
                        for i,c in enumerate(COL)])
    names=VGroup(*[label(s, r*.70*np.cos(PI/4-i*PI/2),r*.70*np.sin(PI/4-i*PI/2),28)
                   for i,s in enumerate(SHORT)])
    hand=Line(ORIGIN,[0,r*.8,0],color=TEXT,stroke_width=6)
    return VGroup(sectors,names,hand,Dot(ORIGIN,color=TEXT,radius=.10))


def birth_axis():
    return VGroup(Arrow([-3.3,-2.45,0],[5.7,-2.45,0],buff=0,color=GREY),
                  label('Birth order: 1st → 5th born',1.2,-3.05,28))


def lineage(colored=False):
    g=VGroup(cell(PURPLE,.95,-4.95,.35),label('NB7-1',-4.95,2.05,30,PURPLE))
    for i,x in enumerate([-2.9,-.85,1.2,3.25,5.3]):
        c=[ORANGE,ORANGE,YELLOW,GREEN,GREEN][i] if colored else GREY
        n=neuron(c,x,-.15,'U'+str(i+1),dual=colored and i==4)
        g.add(n)
    g.add(birth_axis())
    return g

GX=[-2.25,.15,2.55,4.95]
GY=[.6,-1.85]
GH=2.35
GRID_TOP=[0,3.4,0]

def grid():
    g=VGroup(label('Time: which window',1.3,3.4,28),
             Arrow([-3.35,3.0,0],[6.1,3.0,0],buff=0,color=GREY),
             label('Place: which\nneuroblast',-5.1,2.35,26))
    for x,s,c in zip(GX,['Hb','Kr','Pdm\nwithout Cas','Pdm + Cas'],[ORANGE,YELLOW,GREEN,GREEN]):
        g.add(label(s,x,2.35,26,c))
    for ri,(y,name) in enumerate(zip(GY,['NB7-1','Other NB\n(schematic)'])):
        g.add(label(name,-5.1,y,28,PURPLE))
        for i,x in enumerate(GX):
            dual=ri==0 and i==3
            oc=GREEN if dual else COL[i]
            g.add(Rectangle(width=2.3,height=GH,color=GREY,stroke_width=1.5).move_to([x,y,0]))
            g.add(label((['U1, U2','U3','U4','U5'] if ri==0 else ['A','B','C','D'])[i],x,y+.76,26,oc))
            n=neuron(oc,dual=dual,other=ri==1).scale(.58).move_to([x,y-.28,0])
            g.add(n)
    return g


def row_highlight():
    return Rectangle(width=12.15,height=GH+.03,color=PURPLE,stroke_width=5).move_to([0,GY[0],0])


def col_highlight(x=GX[0]):
    return Rectangle(width=2.33,height=GY[0]-GY[1]+GH+.03,color=ORANGE,stroke_width=5).move_to([x,(GY[0]+GY[1])/2,0])


def small_neurons(c, y, count=3, dual=False, xs=None, scale=.42):
    if xs is None: xs=np.linspace(.2,4.7,count)
    return VGroup(*[neuron(c,dual=dual).scale(scale).move_to([x,y,0]) for x in xs])


def extras(c, y, scale=.4, other=False, x0=-.8):
    # Open-ended cluster: a few cells, one fading, then an ellipsis. Schematic, not a count.
    step=1.25
    g=VGroup(*[neuron(c,other=other).scale(scale).move_to([x0+k*step,y,0]) for k in range(3)])
    ghost=neuron(c,other=other).scale(scale).move_to([x0+3*step,y,0]); ghost.set_opacity(.3)
    g.add(ghost, label('…',x0+4*step-.2,y,36,c))
    return g


def table_ys(fourth=False):
    return [1.65,-.2,-2.05] if not fourth else [1.6,.2,-1.2,-2.6]


def table(removed=False, question=False, result=False, fourth=False, kr=False):
    ys=table_ys(fourth)
    h=1.65 if not fourth else 1.35
    g=VGroup(label('Factors in the nervous system (schematic)',0,3.45,30),
             label('Condition',-4.9,2.85,28), label('What the lineages make',1.45,2.85,28))
    names=['Hb normal','Hb removed','Hb kept on']+(['Kr kept on'] if fourth else [])
    for y,s in zip(ys,names):
        g.add(RoundedRectangle(width=12.3,height=h,corner_radius=.10,color=GREY,stroke_width=2).move_to([0,y,0]))
        g.add(Line([-3.3,y-h/2,0],[-3.3,y+h/2,0],color=GREY,stroke_width=1.5))
        txt=label(s,0,y,28,RED if 'removed' in s else YELLOW if 'Kr' in s else ORANGE)
        txt.align_to(np.array([-5.85,y,0]),LEFT); g.add(txt)
    normal=VGroup()
    cols=[ORANGE,ORANGE,YELLOW,GREEN,GREEN]
    for i,x in enumerate([-.9,.4,1.7,3,4.3]):
        # Four-row table: grey the normal row so no yellow cell (third-born U3) sits above 'second-born' extras.
        c=GREY if fourth else cols[i]
        n=neuron(c,dual=(i==4 and not fourth)).scale(.40).move_to([x,ys[0]-.10,0])
        if fourth: n.set_opacity(.5)
        normal.add(n)
    normal.add(Arrow([-2.8,ys[0]-.15,0],[-1.6,ys[0]-.15,0],buff=0,color=GREY))
    g.add(normal)
    if removed:
        g.add(label('First-born identities lost (in the lineages examined)',1.45,ys[1],28,RED))
    if question: g.add(label('?',1.2,ys[2],48,YELLOW))
    if result:
        g.add(*result_row(ORANGE,'Extra first-born-like cells',ys[2],fourth))
    if kr:
        g.add(*result_row(YELLOW,'Extra second-born cells',ys[3],True))
    return g


def result_row(c, text, y, fourth):
    """Label above, open-ended cluster below, with padding from the box edges."""
    ly=y+(.40 if fourth else .45)
    iy=y-(.28 if fourth else .27)
    return [label(text,1.6,ly,26,c), extras(c,iy,.30 if fourth else .40)]


def prediction():
    return VGroup(table(True,True),label('Extra cells: early-born or late-born? Which lineage?',0,-3.35,28,YELLOW))


class S00Title(TitleCard):
    LESSON=LESSON
    TITLE='A Clock in the Fly'
    def construct(self):
        lesson=VGroup(T('Birth Order and Fate: Temporal Identity',size=26,color=GREY),T('and the Inside-Out Cortex',size=26,color=GREY)).arrange(DOWN,buff=.12)
        g=VGroup(label('BIOCHEMISTRYPEDIA',size=26,color=TEAL),lesson,
                 T(self.TITLE,size=52,font=TITLE_FONT),Line(LEFT*1.3,RIGHT*1.3,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.5).move_to(ORIGIN)
        self.add(g[:2]); self.play(FadeIn(g[2:]),run_time=.65); self.finish()


class S01Q(SpokenScene):
    def construct(self):
        c=cell(PURPLE,2.25,0,.25)
        self.add(c,label('Progenitor',0,3.15,32,PURPLE))
        menu=VGroup(*[chip(s,col,28).move_to([0,1.55-i*1.12,0]) for i,(s,col) in enumerate(zip(['early','middle','late'],[ORANGE,YELLOW,GREEN]))])
        self.add(menu)
        self.at("a progenitor's menu"); self.play(Indicate(menu,scale_factor=1.03),run_time=.3)
        self.at('changes with time'); self.play(FadeOut(menu[0],shift=DOWN*.2),run_time=.35)
        self.at('with'); self.play(FadeOut(menu[1],shift=DOWN*.2),run_time=.25)
        self.at('what actually changes'); self.play(FadeOut(menu[2]),FadeIn(label('?',0,.25,100,YELLOW)),run_time=.35)
        self.finish()


class S02Fly(SpokenScene):
    def construct(self):
        embryo=Ellipse(width=3.4,height=5.8,color=GREY).move_to([-4.3,-.1,0])
        cord=RoundedRectangle(width=.9,height=4.6,corner_radius=.2,color=PURPLE).move_to([-4.3,-.1,0])
        bars=VGroup(*[Line([-4.75,y,0],[-3.85,y,0],color=GREY) for y in np.linspace(-2,1.8,8)])
        mid=Line([-4.3,-2.4,0],[-4.3,2.2,0],color=GREY)
        self.add(embryo,cord,bars,mid,label('Fly embryo',-4.3,3.25,30))
        box=Rectangle(width=7.2,height=5.1,color=PURPLE).move_to([2,-.35,0])
        self.at('Each half segment')
        focus=Rectangle(width=.45,height=.54,color=YELLOW,fill_color=YELLOW,fill_opacity=.25).move_to([-4.075,.17,0])
        self.play(Create(focus),Create(Line(focus.get_right(),box.get_left(),color=GREY)),Create(box),FadeIn(label('One half-segment',2,3.25,28)),run_time=.4)
        self.at('about 30 neuroblasts')
        rng=np.random.RandomState(7)
        dots=VGroup(*[cell(PURPLE,.17+.13*rng.rand(),-.95+j*1.18+rng.uniform(-.14,.14),-2.2+i*.95+rng.uniform(-.1,.1)) for i in range(5) for j in range(6)])
        self.play(FadeIn(dots),FadeIn(label('~30 neuroblasts, each one identifiable',2,-3.3,28)),run_time=.4); self.finish()


class S03Bud(SpokenScene):
    def construct(self):
        xs=[-4.2,0,4.2]; NY=.95; NR=1.2; BR=.5; BY=NY-NR-BR-.12
        nbs=VGroup(*[cell(PURPLE,NR,x,NY) for x in xs])
        self.add(nbs[0],label('Same neuroblast, successive snapshots',0,3.4,30),label('Time 1',xs[0],NY+NR+.4,28))
        buds=[]; links=[]; titles=[]
        def mk(x):
            b=cell(PURPLE,BR,x,BY); l=Line([x,NY-NR,0],[x,BY+BR,0],color=PURPLE,stroke_width=4)
            t=label('Ganglion\nmother cell',x,BY-BR-.5,26,PURPLE)
            return b,l,t
        self.at('buds off')
        b,l,ttl=mk(xs[0]); buds.append(b); links.append(l); titles.append(ttl)
        self.play(FadeIn(b),Create(l),FadeIn(ttl),run_time=.45)
        self.at('one after another')
        for i in [1,2]:
            b,l,ttl=mk(xs[i]); buds.append(b); links.append(l); titles.append(ttl)
            self.play(FadeIn(nbs[i]),FadeIn(label('Time '+str(i+1),xs[i],NY+NR+.4,28)),FadeIn(b),Create(l),FadeIn(ttl),run_time=.35)
        self.at('divides into')
        for i,x in enumerate(xs):
            daughters=VGroup(cell(GREY,.38,x-.7,-1.95),cell(GREY,.38,x+.7,-1.95))
            fork=VGroup(Line([x,NY-NR,0],[x-.7,-1.57,0],color=GREY,stroke_width=4),Line([x,NY-NR,0],[x+.7,-1.57,0],color=GREY,stroke_width=4))
            self.play(ReplacementTransform(buds[i],daughters),ReplacementTransform(links[i],fork),FadeOut(titles[i]),run_time=.25)
        self.play(FadeIn(label('Two daughters per birth: neurons or glia',0,-3.15,30)),run_time=.25); self.finish()


class S04Doe(SpokenScene):
    def construct(self):
        c=dial().move_to([2.6,-.25,0]); self.add(c,label('2001',-3.8,3,36))
        for phrase,name,y in [('Taikako Ishiki','Takako Isshiki',1.65),('Brett Pearson','Bret Pearson',.55),('Scott Hallbrooke','Scott Holbrook',-.55),('Chris Do','Chris Doe',-1.65)]:
            self.at(phrase); self.play(FadeIn(label(name,-3.8,y,30)),run_time=.22)
        self.at('found a clock'); self.play(Rotate(c[2],angle=-TAU,about_point=[2.6,-.25,0]),run_time=.55)
        self.at('of transcription factors'); self.play(FadeIn(label('Transcription-factor clock',2.2,-3.15,28)),run_time=.3); self.finish()


class S05Four(SpokenScene):
    def construct(self):
        nb=cell(PURPLE,1.8,0,.1).set_fill(BG,1).set_z_index(2)
        self.add(nb,label('Neuroblast',0,-2.35,30,PURPLE),Arrow([-5.6,-3.05,0],[5.6,-3.05,0],buff=0,color=GREY),label('time',0,-3.5,28))
        old=None; oldname=None
        for i,phrase in enumerate(['Hunchback','then crepel','then PDM','then caster']):
            self.at(phrase)
            band=Rectangle(width=10.7,height=1.2,stroke_width=0,fill_color=COL[i],fill_opacity=.45).move_to([0,.1,0]).set_z_index(-1)
            name=label(NAMES[i],0,2.8,36,COL[i])
            acts=[FadeIn(band,shift=RIGHT*1.8),FadeIn(name)]
            if old is not None: acts += [FadeOut(old,shift=RIGHT*1.8),FadeOut(oldname)]
            self.play(*acts,run_time=.28); old=band; oldname=name
        self.finish()


class S06Keep(SpokenScene):
    def construct(self):
        # Three separate births; the parent remains purple as the temporal band changes.
        self.add(label('Birth colours persist in the progeny',0,3.4,30))
        xs=[-4.15,0,4.15]; buds=VGroup(); stalks=VGroup()
        for i,x in enumerate(xs):
            band=Rectangle(width=3.4,height=.8,stroke_width=0,fill_color=COL[i],fill_opacity=.35).move_to([x,1.4,0])
            nb=cell(PURPLE,.95,x,1.4).set_fill(BG,1)
            b=cell(COL[i],.5,x,-.9)
            self.add(band,nb,label(SHORT[i],x,2.7,28,COL[i]))
            buds.add(b); stalks.add(Line([x,.45,0],[x,-.4,0],color=COL[i],stroke_width=4))
        self.at('A ganglion mother cell'); self.play(FadeIn(buds),Create(stalks),run_time=.35)
        self.at('keeps the factor'); self.play(*[Indicate(b,color=COL[i],scale_factor=1.08) for i,b in enumerate(buds)],run_time=.4)
        self.at('was on'); self.play(FadeIn(label('Each cell retains its birth window',0,-2.75,28)),run_time=.3)
        self.at('So do its neurons')
        kids=VGroup(*[VGroup(*[neuron(COL[i]).scale(.85).move_to([x+dx,-.95,0]) for dx in [-.85,.85]]) for i,x in enumerate(xs)])
        self.play(*[ReplacementTransform(buds[i],kids[i]) for i in range(3)],FadeOut(stalks),run_time=.5); self.finish(); self.wait(1.4)


class S07Overlap(SpokenScene):
    def construct(self):
        self.add(label('Overlapping windows',0,3.3,32),Arrow([-5.8,-2.65,0],[5.8,-2.65,0],buff=0,color=GREY),label('time',0,-3.3,28))
        bands=VGroup()
        for i,c in enumerate(COL):
            x=-3.75+i*2.5; y=1.65-i*.93
            band=VGroup(Rectangle(width=3.75,height=.75,color=c,fill_color=c,fill_opacity=.32).move_to([x,y,0]),label(NAMES[i],x,y,28,c))
            bands.add(band)
        self.at('windows overlap'); self.play(LaggedStart(*[FadeIn(b,shift=RIGHT*.3) for b in bands],lag_ratio=.12),run_time=.65)
        zones=VGroup(*[Rectangle(width=1.25,height=3.9,stroke_width=0,fill_color=TEXT,fill_opacity=.08).move_to([-2.5+i*2.5,.3,0]).set_z_index(-1) for i in range(3)])
        self.at('sequence is an outline'); self.play(FadeIn(zones),run_time=.3); self.finish()


class S08Nb71(SpokenScene):
    def construct(self):
        g=lineage(); big=cell(PURPLE,2.15,0,-.1); name=label('One identified lineage',0,3,32,PURPLE)
        self.add(big,name)
        self.at('The neuroblast'); self.remove(name); name=label('NB7-1',0,3,32,PURPLE); self.add(name)
        self.at('first five motor neurons'); self.play(ReplacementTransform(big,g[0]),ReplacementTransform(name,g[1]),FadeIn(g[-1]),run_time=.45)
        self.play(LaggedStart(*[FadeIn(n,shift=RIGHT*.2) for n in g[2:7]],lag_ratio=.25),run_time=1.25)
        self.at('U1 to U5'); self.play(Indicate(VGroup(*[n[-1] for n in g[2:7]]),scale_factor=1.03),run_time=.3)
        self.at('in that order'); self.play(Indicate(g[-1],scale_factor=1.02),run_time=.3); self.finish()


class S09Windows(SpokenScene):
    def construct(self):
        g=lineage(); self.add(g,label('Idealized; windows overlap',0,3.2,28,GREY)); target=lineage(True)
        for phrase,ids,txt in [('U1 and U2',[2,3],'Hb'),('and U3',[4],'Kr'),('U4 comes',[5],'Pdm'),('U5 needs',[6],'Pdm + Cas')]:
            self.at(phrase); self.play(*[Transform(g[i],target[i]) for i in ids],run_time=.32)
            self.add(*[label(txt,[-2.9,-.85,1.2,3.25,5.3][i-2],-1.65,26,[ORANGE,ORANGE,YELLOW,GREEN][[2,3,4,5].index(ids[0]) if ids[0] <6 else 3]) for i in ids])
        self.finish()


class S10Grid(SpokenScene):
    def construct(self):
        g=grid(); self.add(g)
        self.at('Rows'); row=row_highlight(); self.play(FadeIn(row),run_time=.25)
        self.at('Columns'); self.play(FadeOut(row),run_time=.2)
        hl=col_highlight(); self.play(FadeIn(hl),run_time=.2)
        for x in GX[1:]: self.play(hl.animate.set_x(x),run_time=.22)
        self.finish()


class S11Grid2(SpokenScene):
    def construct(self):
        self.add(grid()); self.at('The same factor')
        self.play(FadeIn(col_highlight()),FadeIn(label('Same window; different neuron',0,-3.4,30,ORANGE)),run_time=.3); self.finish()


class S12Corr(SpokenScene):
    def construct(self):
        self.add(grid()); self.at('only a correlation'); self.play(FadeIn(label('Sequence: correlation',0,-3.4,30)),run_time=.3)
        self.at('To show the factors'); self.play(*[FadeOut(m) for m in list(self.mobjects)],FadeIn(table()),run_time=.4)
        self.at('take one away'); hl=RoundedRectangle(width=12.15,height=1.62,corner_radius=.1,color=RED,stroke_width=4).move_to([0,-.2,0]); self.play(FadeIn(hl),run_time=.25)
        self.at('keep it on'); self.play(hl.animate.set_y(-2.05).set_color(ORANGE),run_time=.25); self.finish()


class S13Embryo(SpokenScene):
    def construct(self):
        # The embryo sits centred until the nerve cord arrives, then slides left.
        embryo=Ellipse(width=3.8,height=5.6,color=GREY).move_to([0,-.2,0])
        ttl=label('Early embryo',0,3.3,30)
        bands=VGroup()
        for y,c,t in [(1.0,ORANGE,'Hunchback'),(-.55,YELLOW,'Krüppel')]:
            bands.add(VGroup(Rectangle(width=3.0,height=.7,color=c,fill_color=c,fill_opacity=.3).move_to([0,y,0]),label(t,0,y,28,c)))
        emb=VGroup(embryo,ttl,bands[0],bands[1]); emb.set_z_index(0)
        self.add(embryo,ttl)
        self.at('Hunchback'); self.play(FadeIn(bands[0]),run_time=.25)
        self.at('and Crapel'); self.play(FadeIn(bands[1]),run_time=.25)
        cord=VGroup(RoundedRectangle(width=3.4,height=5.1,corner_radius=.3,color=PURPLE).move_to([3.3,-.2,0]),
                    *[Line([1.6,y,0],[5.0,y,0],color=GREY) for y in [-1.8,-.7,.4,1.5]],
                    *[cell(PURPLE,.27,x,y) for x in [2.4,4.2] for y in [-2.2,-1.25,-.15,.95,1.95]])
        self.at('So the tests')
        self.play(emb.animate.shift(LEFT*3.5),FadeIn(cord),FadeIn(label('Nerve cord',3.3,3.3,30,PURPLE)),GrowArrow(Arrow([-1.2,0,0],[.8,0,0],color=GREY)),run_time=.55)
        self.at('nervous system itself'); self.play(FadeIn(label('Change factors here',3.3,-3.3,28,ORANGE)),run_time=.25); self.finish()


class S14Lost(SpokenScene):
    def construct(self):
        self.add(table()); self.at('Without Hunchback')
        self.play(FadeIn(RoundedRectangle(width=12.15,height=1.62,corner_radius=.1,color=RED,stroke_width=4).move_to([0,-.2,0])),run_time=.3)
        self.at('firstborn identities'); self.play(FadeIn(label('First-born identities lost (in the lineages examined)',1.45,-.2,28,RED)),run_time=.3); self.finish()


class S15Predict(SpokenScene):
    def construct(self):
        self.add(table(True)); self.at('Keep hunchback on'); self.play(FadeIn(label('?',1.2,-2.05,48,YELLOW)),run_time=.3)
        self.at('Do the extra cells'); q=label('Extra cells: early-born or late-born?',0,-3.35,28,YELLOW); self.play(FadeIn(q),run_time=.3)
        self.at('And of which lineage'); self.play(Transform(q,label('Extra cells: early-born or late-born? Which lineage?',0,-3.35,28,YELLOW)),run_time=.25); self.finish()


class S16Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction()); self.wait(5)


class S17Reveal(SpokenScene):
    def construct(self):
        self.add(table(True)); q=label('?',1.2,-2.05,48,YELLOW); self.add(q)
        lab,cl=result_row(ORANGE,'Extra first-born-like cells',-2.05,False)
        self.at('extra cells with'); 
        self.play(FadeOut(q),FadeIn(lab),FadeIn(cl),run_time=.4)
        self.at('extra cells resembled'); self.play(Transform(lab,label('NB7-1: extra U1/U2-like cells',1.6,-2.05+.45,26,ORANGE)),run_time=.3); self.finish()


class S18Own(SpokenScene):
    def construct(self):
        # Widen the Hb cells to make room for open-ended clusters in each lineage.
        RY=[.85,-1.75]
        self.add(label('Hunchback kept on → extra first-born-like cells (schematic)',0,3.4,28,ORANGE),label('Hb window',1.1,2.75,30,ORANGE))
        for y,name in zip(RY,['NB7-1','Other NB\n(schematic)']):
            self.add(Rectangle(width=12.2,height=2.45,color=GREY).move_to([0,y,0]),label(name,-4.85,y,28,PURPLE))
        a=extras(ORANGE,RY[0]-.15,.72,x0=-2.1); b=extras(ORANGE,RY[1]-.15,.72,other=True,x0=-2.1)
        self.at('Each lineage made'); self.play(FadeIn(a),FadeIn(b),run_time=.35)
        self.at('its own'); self.play(FadeIn(label('U1/U2-like',1.1,RY[0]+.95,26,ORANGE)),FadeIn(label('Distinct first-born type A',1.1,RY[1]+.95,26,ORANGE)),run_time=.3)
        self.at('did not make'); self.play(FadeIn(label('Same factor; each lineage retains its own type',0,-3.45,28)),run_time=.3); self.finish()


class S19Kr(SpokenScene):
    def construct(self):
        self.add(table(True,result=True,fourth=True))
        lab,cl=result_row(YELLOW,'Extra second-born cells',table_ys(True)[3],True)
        self.at('made extra'); self.play(FadeIn(lab),LaggedStart(*[FadeIn(n) for n in cl],lag_ratio=.15),run_time=.65); self.finish()


class S20Hold(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(table(True,result=True,fourth=True,kr=True)); self.wait(2.5)


class S21Late(SpokenScene):
    def construct(self):
        self.add(label('Doe laboratory · 2006',0,3.3,32))
        a=neuron(GREEN).scale(1.65).move_to([-2.5,-.15,0]); b=neuron(GREEN,dual=True).scale(1.65).move_to([2.5,-.15,0])
        self.add(a,b,label('U4',-2.5,2,30,GREEN),label('U5',2.5,2,30,GREEN))
        self.at('PDM and Castor'); self.play(FadeIn(label('Pdm',-2.5,-2.3,30,GREEN)),FadeIn(label('Pdm + Castor',2.5,-2.3,30,GREEN)),run_time=.3)
        self.at('specify'); self.play(FadeIn(label('Pdm and Castor mark U4 and U5',0,-3.3,28)),run_time=.3); self.finish()


class S22Program(SpokenScene):
    def construct(self):
        R=1.95; CY=.55; XS=[-4.4,0,4.4]
        self.add(label('Birth order: a genetic program (schematic)',0,3.4,34))
        clocks=VGroup(*[dial(R).move_to([x,CY,0]) for x in XS])
        self.add(clocks)
        self.add(label('Prolong',XS[0],-1.95,30,ORANGE),label('Break',XS[1],-1.95,30,RED),label('Rewire',XS[2],-1.95,30,BLUE))
        def pol(cx,deg,rf):
            a=np.deg2rad(deg); return np.array([cx+R*rf*np.cos(a),CY+R*rf*np.sin(a),0])
        # The clocks run from the first word, so the frame is never static.
        self.play(*[Rotate(c[2],-PI/2,about_point=c[3].get_center()) for c in clocks],run_time=1.3,rate_func=linear)
        self.at('genetic program')
        p=pol(XS[0],72,.80)
        lock=Line(p+LEFT*.22,p+RIGHT*.22,color=ORANGE,stroke_width=9)
        self.play(FadeIn(lock),FadeIn(label('Hb kept on',XS[0],-2.85,26,ORANGE)),run_time=.25)
        self.at('broken')
        q=pol(XS[1],62,.86)
        cross=VGroup(Line(q+np.array([-.17,-.17,0]),q+np.array([.17,.17,0]),color=RED,stroke_width=7),Line(q+np.array([-.17,.17,0]),q+np.array([.17,-.17,0]),color=RED,stroke_width=7))
        self.play(FadeIn(cross),FadeIn(label('Lose a window',XS[1],-2.85,26,RED)),run_time=.25)
        self.at('rewired')
        cp=pol(XS[2],45,.70)
        self.play(clocks[2][0][0].animate.set_fill(TEXT,.45),Transform(clocks[2][1][0],label('?',cp[0],cp[1],36,TEXT)),FadeIn(label('Reassign (schematic)',XS[2],-2.85,26,BLUE)),run_time=.3); self.finish(); self.wait(.7)


class S23Take(SpokenScene):
    def construct(self):
        # Shrink the grid toward its top edge so the two captions keep a 60 px bottom margin.
        K=.86
        sh=lambda m: m.scale(K,about_point=GRID_TOP)
        self.add(sh(grid())); self.at('place picks')
        self.play(FadeIn(sh(row_highlight())),FadeIn(label('Row = class: NB7-1 motor neurons',0,-2.65,28,PURPLE)),run_time=.25)
        self.at('Time'); member=label('Column = member: Hb → U1 / U2',0,-3.15,26,ORANGE); self.play(FadeIn(sh(col_highlight())),FadeIn(member),run_time=.25)
        self.at('picks the member'); self.play(Indicate(member,scale_factor=1.01),run_time=.25); self.finish()


class S24End(EndCard):
    LINE='Place picks the class of neuron; time picks the member.'
    def construct(self):
        g=VGroup(VGroup(T('Place picks the class of neuron;',size=40,font=TITLE_FONT),T('time picks the member.',size=40,font=TITLE_FONT)).arrange(DOWN,buff=.18),T('biochemistrypedia.com',size=26,color=TEAL)).arrange(DOWN,buff=.6)
        self.play(FadeIn(g),run_time=.6); self.finish()
