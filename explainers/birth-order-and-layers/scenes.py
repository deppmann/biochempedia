"""The Wall of the Brain: reviewer fix round.
COLOR MAP: PURPLE progenitors/cycle; PINK preplate/MZ/layer 1;
LAVENDER subplate; ORANGE layer 6/early cohort; GOLDEN layer 5;
YELLOW layer 4; GREEN layer 3; BLUE layer 2/later cohort;
TEAL generic neuron/timestamp; GREY surrounding tissue; RED rejected cause.
All anatomy and cell counts are qualitative schematics, not data traces.
"""
from bp_style import *

ORANGE = '#F29E4C'
PURPLE = '#B58CD9'
PINK = '#E58FB4'
LAVENDER = '#8B82BC'
GOLDEN = '#DAB976'
import numpy as np
SH = 1.5                      # wall shift: the wall is now centred-left with a wide annotation column
WL, WR, WC = -4.0, 1.0, -1.5  # wall left edge, right edge, centre x
GUT = -4.5                    # left gutter for layer numbers and VZ/SVZ
LX = 1.95                     # left edge of the annotation column
RC = 4.45                     # centre of the annotation column
YT, YB = 3.0, -3.0
def S(x): return x+SH
# Stable anatomy: layer 1 above cortical plate; subplate below it; SVZ and VZ below.
LAYERS = [(1,2.65,PINK),(2,2.0,BLUE),(3,1.35,GREEN),
          (4,.7,YELLOW),(5,.05,GOLDEN),(6,-.6,ORANGE)]

def txt(s,x,y,size=28,color=TEXT,**kw):
    return T(s,size,color,**kw).move_to([x,y,0])

def nd(c,x,y,r=.28):
    return Circle(radius=r,stroke_color=c,stroke_width=3,fill_color=c,fill_opacity=.85).move_to([x,y,0])

def neuron(c,x,y,r=.28):
    soma=nd(c,x,y,r)
    branches=VGroup(*[Line([x+dx*r,y+dy*r,0],[x+dx*r*1.65,y+dy*r*1.65,0],color=c,stroke_width=3)
                       for dx,dy in [(-1,0),(1,0),(0,1),(0,-1)]])
    return VGroup(branches,soma)

def arr(a,b,c=TEXT):
    return Arrow(a,b,buff=.1,color=c,stroke_width=3,tip_length=.18)

def label(s,y,c=TEXT,x=None,lead=True,size=30):
    t=T(s,size,c); x=LX if x is None else x
    t.move_to([x+t.width/2,y,0])
    if lead:
        return VGroup(Line([WR+.06,y,0],[x-.1,y,0],color=c,stroke_width=2,stroke_opacity=.75),t)
    return t

def band(y,h,c,opacity=.22):
    return Rectangle(width=5,height=h,stroke_color=c,stroke_width=2,
                     fill_color=c,fill_opacity=opacity).move_to([WC,y,0])

def edge_labels():
    return VGroup(txt('pia',WC,3.4),Line([WC,3.2,0],[WC,3.02,0],color=TEXT),
                  txt('ventricle',WC,-3.4),Line([WC,-3.2,0],[WC,-3.02,0],color=TEXT))

def wall(zones=True,split=False,plate=False,edges=True):
    g=VGroup(Rectangle(width=5,height=6,stroke_color=GREY,stroke_width=2).move_to([WC,0,0]))
    if edges: g.add(edge_labels())
    if zones:
        g.add(band(-2.65,.65,PURPLE),band(-1.92,.65,PURPLE),
              txt('VZ',GUT,-2.65,26),txt('SVZ',GUT,-1.92,26))
    if split: g.add(band(2.65,.45,PINK),band(-1.18,.35,LAVENDER))
    if plate: g.add(band(.7,3.25,GREY))
    return g

def fibre():
    return Line([S(-3.8),-2.65,0],[S(-3.8),2.98,0],color=PURPLE,stroke_width=5)

def preplate():
    return VGroup(band(2.55,.6,PINK),*[nd(PINK,x,2.55,.16) for x in [S(-4.6),S(-3.55),S(-2.5),S(-1.45)]])

def sheets():
    return VGroup(band(2.65,.45,PINK),band(-1.18,.35,LAVENDER))

def cp_bracket(text='cortical plate\nlayers 2–6'):
    b=VGroup(Line([S(-.25),-.92,0],[S(-.05),-.92,0]),Line([S(-.05),-.92,0],[S(-.05),2.32,0]),Line([S(-.25),2.32,0],[S(-.05),2.32,0])).set_color(TEXT)
    return VGroup(b,label(text,.8,lead=False,x=LX))

def layer_wall(fill=True):
    g=wall(True,True)
    for n,y,c in LAYERS:
        if n!=1: g.add(band(y,.62,c,.26 if fill else .02))
        g.add(txt(str(n),GUT,y,28,c))
    g.add(label('subplate',-1.18,LAVENDER))
    return g

def menu(x=0,y=0):
    box=RoundedRectangle(width=5.0,height=4.6,corner_radius=.18,stroke_color=PURPLE,fill_color=PURPLE,fill_opacity=.07).move_to([x,y,0])
    rows=VGroup()
    for i,(s,c) in enumerate([('deep: layer 6',ORANGE),('deep: layer 5',GOLDEN),('layer 4',YELLOW),('upper: layers 3, 2',BLUE)]):
        yy=y+1.55-i*1.02
        rows.add(VGroup(Line([x-2.1,yy,0],[x-1.65,yy,0],color=c,stroke_width=7),txt(s,x+.1,yy,28,c)))
    return VGroup(box,rows)

def strike(row):
    return Line(row.get_left()+LEFT*.05,row.get_right()+RIGHT*.05,color=TEXT,stroke_width=4)

def menu_final():
    m=menu(-2.8,0)
    m[1][0].set_opacity(.55); m[1][1].set_opacity(.55)
    return VGroup(m,strike(m[1][0]),strike(m[1][1]),txt('progenitor’s menu',-2.8,2.9,32,PURPLE),
                  txt('in normal\ndevelopment',3.2,1.3,30),txt('fewer choices\nwith time',3.2,-.6,30),
                  arr([-5.3,-2.85,0],[-.3,-2.85,0]),txt('time',-2.8,-3.3))

class S00Title(TitleCard):
    LESSON='Birth Order and Fate: Temporal Identity and the Inside-Out Cortex'
    TITLE='The Wall of the Brain'
    def construct(self):
        self.add(txt('BIOCHEMISTRYPEDIA',0,2,28,TEAL),txt('Birth Order and Fate: Temporal Identity\nand the Inside-Out Cortex',0,.8,28))
        self.play(FadeIn(txt(self.TITLE,0,-.9,48)),run_time=.7)
        self.finish()

class S01Q(SpokenScene):
    def construct(self):
        self.add(wall(False,edges=False),neuron(TEAL,S(-3.8),-2.65,.38),
                 txt('excitatory\nneuron',-5.0,-2.65,28,TEAL),Line([-4.15,-2.65,0],[S(-3.8)-.65,-2.65,0],color=TEAL,stroke_width=2))
        path=DashedLine([S(-3.8),-1.9,0],[S(-3.8),2.55,0],color=TEAL,dash_length=.13)
        self.add(path,txt('?',S(-3.8)+.5,.5,52))
        self.at('is born at the bottom')
        brk=VGroup(Line([S(-.25),-2.97,0],[S(-.05),-2.97,0]),Line([S(-.05),-2.97,0],[S(-.05),-1.6,0]),Line([S(-.25),-1.6,0],[S(-.05),-1.6,0])).set_color(PURPLE)
        self.play(FadeIn(band(-2.65,.65,PURPLE)),FadeIn(band(-1.92,.65,PURPLE)),FadeIn(brk),FadeIn(label('birth zones',-2.28,PURPLE,lead=False)),run_time=.5)
        self.at('ventricle',lead=.15)
        self.play(FadeIn(txt('ventricle',WC,-3.4)),run_time=.3)
        self.at('so how do')
        self.play(FadeIn(txt('How do the layers\nget in order?',RC,1,34)),run_time=.5)
        self.finish()

def two_lobes(d,R,color=PURPLE,y0=.3):
    xs=np.linspace(-(d+R),d+R,180)
    h=np.maximum(np.sqrt(np.clip(R**2-(xs-d)**2,0,None)),np.sqrt(np.clip(R**2-(xs+d)**2,0,None)))
    pts=[[x,y0+v,0] for x,v in zip(xs,h)]+[[x,y0-v,0] for x,v in zip(xs[::-1],h[::-1])]
    m=VMobject(stroke_color=color,stroke_width=3,fill_color=color,fill_opacity=.85)
    m.set_points_as_corners(pts+[pts[0]])
    return m

class S02Notch(SpokenScene):
    def construct(self):
        a=two_lobes(0,1.45); self.add(a,txt('one division',0,3.0,34))
        self.at('can make two sisters')
        # A real pinch: the cell elongates and the waist narrows until two sisters touch.
        self.play(UpdateFromAlphaFunc(a,lambda m,al: m.become(two_lobes(1.1*al,1.45-.35*al))),run_time=1.0,rate_func=smooth)
        left=nd(PURPLE,-1.1,.3,1.1); right=nd(PURPLE,1.1,.3,1.1)
        self.remove(a); self.add(left,right)
        self.at('different')
        lab_l=txt('Notch on',-1.1,-1.55,32,GREEN); lab_r=txt('Notch off\n(Numb)',1.1,-1.75,32,YELLOW)
        self.play(left.animate.set_color(GREEN),right.animate.set_color(YELLOW),FadeIn(lab_l),FadeIn(lab_r),run_time=.4)
        self.at('a division',lead=.1)
        gl=VGroup(left,lab_l); gr=VGroup(right,lab_r)
        self.play(gl.animate.shift(LEFT*1.9),gr.animate.shift(RIGHT*1.9),run_time=.8)
        self.at('yes or no alone')
        self.play(FadeIn(txt('a yes or no, alone',0,1.9,32)),run_time=.4)
        self.at('cannot say which division')
        self.play(FadeIn(txt('Which division was it?',0,-3,34)),run_time=.4)
        self.finish()

class S03Tenth(SpokenScene):
    def construct(self):
        stem=nd(PURPLE,-5.2,2.55,.55)
        self.add(stem,txt('stem cell',-3.4,2.55,28,PURPLE))
        self.at('that makes ten different daughters')
        daughters=VGroup()
        for i in range(10):
            x=-4.8+(i%5)*2.4; y=.65-(i//5)*2.6
            c=TEAL if i in [0,9] else GREY
            d=VGroup(nd(c,x,y,.57),txt(str(i+1),x,y,32))
            # Each daughter appears only after the preceding copy has finished.
            self.play(TransformFromCopy(stem,d),run_time=.22)
            daughters.add(d)
        self.at('what tells the tenth daughter')
        self.play(FadeIn(txt('?',5.65,-1.95,44,TEAL)),FadeIn(txt('Ten daughters, ten types?',1.6,2.55,32)),run_time=.4)
        self.at('she is not the first')
        self.play(Indicate(daughters[0]),Indicate(daughters[9]),run_time=.7)
        self.finish()

class S04Slice(SpokenScene):
    def construct(self):
        # Curved side-view embryo head, snout and neck; forebrain is the dorsal rostral bulge.
        head=VMobject(color=GREY,stroke_width=4).set_points_smoothly([
            [-4,-2,0],[-4.9,-.6,0],[-4.6,1.4,0],[-3.3,2.5,0],[-1.8,2.25,0],
            [-.7,1.3,0],[-.5,.45,0],[.25,-.1,0],[-.2,-.65,0],[-1.2,-.8,0],[-1.6,-2,0]])
        brain=Ellipse(width=2.5,height=2.0,color=PURPLE,stroke_width=4).move_to([-2.8,1.2,0])
        eye=nd(GREY,-1.15,.1,.2)
        strip=Rectangle(width=.45,height=1.5,color=YELLOW,stroke_width=4).move_to([-2.1,1.4,0])
        group=VGroup(head,brain,eye,strip,txt('mouse embryo head',-2.8,-2.7,30),txt('forebrain',2,1.8,32,PURPLE),arr([.5,1.7,0],[-1.55,1.4,0],PURPLE))
        self.add(group)
        self.at('embryonic mouse forebrain')
        tissue=VGroup(*[Circle(radius=.13,color=GREY,stroke_opacity=.4).move_to([S(x),y,0]) for x in [-4.9,-4.1,-3.3,-2.5,-1.7,-.9] for y in [-2.6,-1.8,-1,-.2,.6,1.4,2.2]])
        self.play(FadeOut(group),TransformFromCopy(strip,wall(False,edges=False)),FadeIn(tissue),FadeIn(label('forebrain wall',.4,lead=False)),run_time=.9)
        self.at('the ventricle is')
        self.play(FadeIn(txt('ventricle (bottom)',4.4,-2.7)),GrowArrow(arr([2.6,-2.7,0],[1.1,-3.0,0])),run_time=.4)
        self.at('bottom',lead=-.5)
        # Unambiguous cue just before pia (mis-transcribed as 'pyre').
        self.play(FadeIn(txt('pia (top)',4.4,2.8)),GrowArrow(arr([3.0,2.8,0],[1.1,3.0,0])),run_time=.35)
        self.finish()

class S05Vz(SpokenScene):
    def construct(self):
        self.add(wall(False))
        self.at('the ventricular zone')
        self.play(FadeIn(band(-2.65,.65,PURPLE)),FadeIn(label('ventricular zone',-2.65,PURPLE)),run_time=.5)
        cells=VGroup(*[nd(PURPLE,S(x),-2.65,.24) for x in [-4.7,-3.8,-2.1]])
        self.at('many of its progenitors')
        self.play(FadeIn(cells),run_time=.5)
        self.at('are radial glia')
        self.play(Create(fibre()),FadeIn(label('radial glia',-.5,PURPLE,lead=False)),Create(Line([S(-3.7),-2.45,0],[LX-.1,-.5,0],color=PURPLE,stroke_width=2)),run_time=1)
        self.at('they divide')
        daughter=nd(PURPLE,S(-3.2),-2.65,.24)
        self.play(TransformFromCopy(cells[1],daughter),run_time=.8)
        self.at('send a long')
        self.play(Indicate(cells[1]),run_time=.6)
        self.finish()

class S06Svz(SpokenScene):
    def construct(self):
        self.add(wall(False),band(-2.65,.65,PURPLE),txt('VZ',GUT,-2.65,26),nd(PURPLE,S(-3.8),-2.65))
        self.at('just above sits')
        self.play(FadeIn(band(-1.92,.65,PURPLE)),FadeIn(label('subventricular zone',-1.92,PURPLE)),run_time=.6)
        self.add(txt('SVZ',GUT,-1.92,26))
        d=nd(PURPLE,S(-3.8),-2.65,.28)
        self.at('intermediate progenitors')
        self.add(d)
        self.play(d.animate.move_to([S(-3.2),-1.92,0]),run_time=.7)
        tag=label('intermediate\nprogenitor',-.1,PURPLE,lead=False)
        leader=Line([S(-2.9),-1.8,0],[LX-.1,-.1,0],color=PURPLE,stroke_width=2)
        self.at('daughters of radial glia')
        self.play(FadeIn(tag),Create(leader),run_time=.4)
        self.at('divide there')
        d2=nd(PURPLE,S(-3.2),-1.92,.28)
        spindle=Line([S(-3.9),-1.92,0],[S(-2.5),-1.92,0],color=TEXT,stroke_width=3)
        self.add(d2,spindle)
        self.play(d.animate.set_x(S(-3.8)),d2.animate.set_x(S(-2.6)),run_time=1.5)
        self.at('to make neurons')
        ntag=VGroup(txt('neurons',S(-3.2),-1.1,28,TEAL),Line([S(-3.2),-1.2+.0,0],[S(-3.2),-1.43,0],color=TEAL,stroke_width=2))
        self.play(ReplacementTransform(d,neuron(TEAL,S(-3.8),-1.92)),ReplacementTransform(d2,neuron(TEAL,S(-2.6),-1.92)),FadeOut(spindle),FadeOut(tag),FadeOut(leader),FadeIn(ntag),run_time=.5)
        self.wait(.8)
        self.finish()

class S07Preplate(SpokenScene):
    def construct(self):
        self.add(wall())
        old=VGroup(neuron(TEAL,S(-3.8),-1.92),neuron(TEAL,S(-2.6),-1.92),txt('neurons',S(-3.2),-1.1,28,TEAL),Line([S(-3.2),-1.2,0],[S(-3.2),-1.43,0],color=TEAL,stroke_width=2))
        self.add(old)
        self.at('the first neurons')
        self.play(FadeIn(preplate()),FadeOut(old),run_time=.8)
        self.at('this is the preplate')
        self.play(FadeIn(label('preplate',2.55,PINK)),run_time=.4)
        self.finish()

class S08Split(SpokenScene):
    def construct(self):
        upper=VGroup(band(2.7,.3,PINK),nd(PINK,S(-4.6),2.7,.13),nd(PINK,S(-2.5),2.7,.13))
        lower=VGroup(band(2.4,.3,PINK),nd(PINK,S(-3.55),2.4,.13),nd(PINK,S(-1.45),2.4,.13))
        p=VGroup(upper,lower)
        pre_label=label('preplate',2.55,PINK)
        self.add(wall(),p,pre_label)
        n=VGroup(*[neuron(TEAL,S(x),.9,.24) for x in [-4,-2.8,-1.6]])
        nlab=label('next neurons',.9,TEAL)
        self.at('the next neurons arrive')
        self.add(n,nlab); self.play(n.animate.set_y(2.55),nlab.animate.set_y(1.95),run_time=1.3)
        self.at('in the middle')
        self.play(Indicate(n,color=TEAL,scale_factor=1.3),run_time=.55)
        self.at('wedge it apart')
        # Play the split on the main wall; the arriving neurons stay teal and named.
        self.play(upper.animate.shift(DOWN*.05),lower.animate.shift(DOWN*3.58).set_color(LAVENDER),
                  n.animate.set_y(.7),nlab.animate.set_y(.7),FadeOut(pre_label),run_time=1.4)
        self.play(FadeIn(label('sheet pushed apart',1.5,TEAL,lead=False)),run_time=.3)
        self.wait(.5)
        self.finish()

class S09Split2(SpokenScene):
    def construct(self):
        self.add(wall(True,True))
        self.at('the top half becomes')
        self.play(FadeIn(label('marginal zone',2.65,PINK)),run_time=.4)
        self.at('future layer')
        self.play(FadeIn(label('future layer 1',2.05,PINK,lead=False)),run_time=.4)
        self.at('home of the')
        cells=VGroup(*[nd(PINK,S(x),2.65,.16) for x in [-4.4,-3.2,-2]])
        self.play(FadeIn(cells),FadeIn(label('Cajal–Retzius cells',1.4,PINK,lead=False)),Create(Line([S(-1.8),2.55,0],[LX-.1,1.4,0],color=PINK)),run_time=.4)
        self.at('the bottom half')
        self.play(FadeIn(label('subplate',-1.18,LAVENDER)),run_time=.4)
        self.finish()

class S10Cp(SpokenScene):
    def construct(self):
        self.add(wall(True,True),label('marginal zone',2.65,PINK),label('subplate',-1.18,LAVENDER))
        self.at('between them')
        self.play(FadeIn(band(.7,3.25,GREY)),run_time=.5)
        self.at('the cortical plate')
        b=cp_bracket('cortical plate'); self.play(FadeIn(b),run_time=.4)
        self.at('becomes layers')
        self.play(FadeIn(label('layers 2–6',.1,lead=False)),run_time=.4)
        n=neuron(TEAL,S(-3.8),-2.65,.3)
        self.at('each new neuron')
        self.add(n); self.play(Create(fibre()),run_time=.4)
        self.at('climbs up from below')
        self.play(n.animate.set_y(.1),run_time=1.5)
        self.finish()

class S11Number(SpokenScene):
    def construct(self):
        self.add(wall(True,True))
        self.at('layers are numbered')
        self.play(LaggedStart(*[FadeIn(txt(str(n),GUT,y,28,c)) for n,y,c in LAYERS],lag_ratio=.2),run_time=1.7)
        self.at('layer 1 on top')
        self.play(FadeIn(label('1: from the early preplate',2.65,PINK)),run_time=.4)
        self.at('in the cortical plate')
        self.play(FadeIn(cp_bracket()),FadeIn(label('subplate',-1.18,LAVENDER)),run_time=.4)
        self.at('made the other way')
        curve=CurvedArrow([S(-4.6),-.6,0],[S(-4.6),2.0,0],angle=-PI/3,color=TEXT,stroke_width=4)
        self.play(Create(curve),FadeIn(nd(TEXT,S(-4.6),-.6,.07)),run_time=.6)
        self.at('from six up to two')
        for n,y,c in reversed(LAYERS[1:]):
            self.play(FadeIn(band(y,.62,c)),FadeIn(neuron(c,S(-2.7),y,.2)),run_time=.35)
            self.wait(.65)
        self.play(FadeIn(label('6 first → 2 last',-2.45,YELLOW,lead=False)),run_time=.3)
        self.wait(2)
        self.finish()

class S14P1(SpokenScene):
    def construct(self):
        self.add(layer_wall())
        for x,y in [(-4.2,-.6),(-2.8,.7),(-1.4,2)]:
            self.add(neuron(TEAL,S(x),y,.27),txt('?',S(x)+.52,y+.62,52,TEXT))
        self.at('the map raises three puzzles')
        self.play(FadeIn(txt('Three puzzles',RC,2.65,34)),run_time=.4)
        self.at('first who came first')
        self.play(FadeIn(txt('1  Who was\nborn first?',RC,.5,34)),run_time=.4)
        self.at('how can you tell')
        self.play(FadeIn(txt('How can you tell?',RC,-2.5,30)),run_time=.4)
        self.finish()

class S15P2(SpokenScene):
    def construct(self):
        p=nd(PURPLE,-1.6,-.25,1.6); self.add(p,txt('progenitor',-1.6,-2.2,30,PURPLE))
        self.at('second record or cause')
        self.play(FadeIn(txt('2  Record or cause?',0,3,36)),run_time=.4)
        cal=VGroup(Rectangle(width=1.65,height=1.55,color=TEXT),Rectangle(width=1.65,height=.35,color=TEXT,fill_color=TEXT,fill_opacity=.3).shift(UP*.6),
                   *[Line([x,-.75,0],[x,.4,0],color=TEXT,stroke_width=2) for x in [-.3,.3]],
                   *[Line([-.8,y,0],[.8,y,0],color=TEXT,stroke_width=2) for y in [-.35,.05]]).move_to([-1.6,-.25,0])
        self.at('carry its own schedule')
        self.play(FadeIn(cal),FadeIn(txt('its own calendar?',-3.8,1.8,30)),Create(Line([-3.1,1.5,0],[-2.2,.55,0],color=TEXT)),run_time=.5)
        cells=VGroup(*[nd(GREY,x,y,.5) for x,y in [(3.8,1.2),(4.4,-.3),(3.8,-1.8)]])
        arrows=VGroup(*[arr([3.1,y,0],[.2,-.25,0]) for y in [1.2,-.3,-1.8]])
        self.at('do its surroundings decide')
        self.play(FadeIn(cells),Create(arrows),FadeIn(txt('surroundings?',3.6,-2.8,30)),run_time=.7)
        self.finish()

class S16P3(SpokenScene):
    def construct(self):
        def pool(n):
            positions=[(-4.3,1.1),(-3.05,-.45),(-4.3,-2)] if n==3 else [(-4.3+(i%2)*1.3,1.1-(i//2)*1.55) for i in range(n)]
            return VGroup(*[nd(PURPLE,x,y,.52) for x,y in positions])
        def output(n):
            return VGroup(*[neuron(TEAL,2+(i%3)*1.25,1.1-(i//3)*1.1,.34) for i in range(n)])
        CAPY=-3.45
        p=pool(3); self.add(p,txt('progenitor pool',-3.7,2.3,30,PURPLE),txt('neurons made',3.2,2.3,30,TEAL),arr([-.9,0,0],[1,0,0]))
        self.at('third how many of each')
        self.play(FadeIn(txt('3  How many of each?',0,3.3,34)),run_time=.35)
        self.at('how does one pool')
        a=output(1); cap=txt('a few',3.2,CAPY,30,TEAL)
        self.play(TransformFromCopy(p[0],a),FadeIn(cap),run_time=.65)
        self.at('then many')
        b=output(4); grown=pool(6)
        self.play(ReplacementTransform(a,b),ReplacementTransform(p,grown),
                  Transform(cap,txt('more',3.2,CAPY,30,TEAL)),run_time=.65)
        self.at('first grows')
        pool_cap=txt('grows',-3.7,CAPY,34,'#D9B8F5',weight=BOLD)
        self.play(grown.animate.scale(1.06),FadeIn(pool_cap),run_time=.3)
        self.play(grown.animate.scale(1/1.06),run_time=.3)
        self.at('then shrinks')
        self.play(ReplacementTransform(grown,pool(3)),ReplacementTransform(b,output(10)),
                  Transform(pool_cap,txt('shrinks',-3.7,CAPY,34,'#D9B8F5',weight=BOLD)),
                  Transform(cap,txt('many leaving a shrinking pool',1,CAPY,28,TEAL)),run_time=1.2)
        self.wait(2)
        self.finish()

class S17Idea(SpokenScene):
    def construct(self):
        title=txt('A birthday marks a time',0,3.5,34)
        # Build the diagram in its own coordinates, then enlarge it to fill the frame.
        birthday=chip('birthday',TEAL,30).move_to([-3.5,1.8,0])
        p=nd(PURPLE,-3.5,-.8,1.0); plab=txt('progenitor state',-3.5,-2.3,30,PURPLE)
        time_arrow=arr([-1.9,1.8,0],[1,1.8,0],TEAL); time_lab=txt('time',2,1.8,34,TEAL)
        state_arrow=arr([1,1.4,0],[-2.7,-.1,0],TEAL); at_that=txt('at that time',1.6,.7,30,TEAL)
        n=neuron(BLUE,2,-.8,.65)
        set_arrow=arr([-2.3,-.8,0],[.9,-.8,0],PURPLE)
        stack=VGroup(*[Rectangle(width=1.5,height=.36,color=c,fill_color=c,fill_opacity=.55).move_to([4.5,-.8+1.08-.18-i*.36,0]) for i,c in enumerate([PINK,BLUE,GREEN,YELLOW,GOLDEN,ORANGE])])
        brace=Brace(stack,LEFT,buff=.06,color=BLUE)
        link=Line([2.7,-.8,0],brace.get_tip(),color=BLUE,stroke_width=3)
        tid=txt('temporal identity',2.4,-2.2,30,BLUE); inc=txt('(its layer included)',2.4,-2.75,28)
        grp=VGroup(birthday,p,plab,time_arrow,time_lab,state_arrow,at_that,n,set_arrow,stack,brace,link,tid,inc)
        grp.scale(1.2).move_to([0,-.2,0])
        self.add(title,birthday,p,plab)
        self.at('a birthday marks a time')
        self.play(GrowArrow(time_arrow),FadeIn(time_lab),run_time=.6)
        self.at("the progenitor's state")
        self.play(Create(state_arrow),FadeIn(at_that),run_time=.6)
        self.at('sets the')
        self.play(TransformFromCopy(p,n),Create(set_arrow),run_time=.6)
        self.at("neuron's temporal identity")
        self.play(FadeIn(tid),FadeIn(inc),FadeIn(stack),FadeIn(brace),Create(link),run_time=.5)
        self.finish()

class S18Idea2(SpokenScene):
    def construct(self):
        n=neuron(TEAL,-4,1.4,.75)
        clock=VGroup(Circle(radius=.35,color=TEXT),Line(ORIGIN,UP*.25,color=TEXT),Line(ORIGIN,RIGHT*.2,color=TEXT)).move_to([-4,1.4,0])
        layer=Rectangle(width=2,height=.6,color=BLUE,fill_color=BLUE,fill_opacity=.3).move_to([-3,-2.1,0])
        cause=arr([-4,.3,0],[-3,-1.7,0],TEAL)
        self.add(n,clock,layer,txt('layer',-3,-2.7,28,BLUE))
        self.at('the birthday instructs nothing')
        cross=VGroup(Line([-4.1,-.8,0],[-3.3,-.1,0],color=RED,stroke_width=5),Line([-4.1,-.1,0],[-3.3,-.8,0],color=RED,stroke_width=5))
        self.play(Create(cause),Create(cross),FadeIn(txt('instructs nothing',-3.8,3,30)),run_time=.5)
        self.at('it is a time stamp')
        self.play(FadeIn(txt('just a timestamp',-4,-.3,28,TEAL)),FadeOut(cause),FadeOut(cross),run_time=.4)
        ring=Circle(radius=1.3,color=PURPLE,stroke_width=10).move_to([2.4,.9,0])
        start=Line([2.4,2.05,0],[2.4,2.5,0],color=TEXT,stroke_width=3)
        clockwise=CurvedArrow([2.7,2.5,0],[3.9,1.3,0],angle=-PI/2,color=TEXT)
        self.at('in ferret')
        self.play(Create(ring),Create(start),Create(clockwise),FadeIn(txt('start / division',2.3,3.05,28)),FadeIn(txt('final\ncell cycle',2.4,.9,28,PURPLE)),run_time=.6)
        self.at('laminar fate becomes fixed')
        late=Arc(radius=1.3,start_angle=PI,angle=-PI/2,color=YELLOW,stroke_width=15).move_arc_center_to([2.4,.9,0])
        self.play(Create(late),FadeIn(txt('layer fate fixed here\n(ferret grafts)',2.7,-1.2,28,YELLOW)),Create(Line([1.3,1.6,0],[.8,-.6,0],color=YELLOW)),run_time=.6)
        self.at('late in the final cell cycle')
        self.play(FadeIn(txt('last quarter before division',2.7,-2.2,27)),run_time=.4)
        self.at('migration and later programs')
        route=CurvedArrow([-2.7,1.1,0],[-1.95,-2.1,0],angle=-PI/3,color=TEAL,stroke_width=3)
        self.play(Create(route),FadeIn(txt('migration + later programs',0,-3.35,28)),run_time=.7)
        self.finish()

class S19Idea3(SpokenScene):
    def construct(self):
        p=nd(PURPLE,0,0,1.0); self.add(p,txt('progenitor state',0,3,34,PURPLE))
        m=menu(-3.7,-.1)
        # Keep the labelled menu adjacent to, and connected to, the progenitor.
        self.at('that state has two parts')
        self.play(FadeIn(txt('competence',-3.7,2.6,30,PURPLE)),run_time=.4)
        self.at('what the progenitor can still make')
        self.play(FadeIn(m),Create(Line([-1.2,0,0],[-1,0,0],color=PURPLE)),run_time=.5)
        self.at('its competence')
        self.play(Indicate(m[0]),run_time=.4)
        neighbors=VGroup(*[nd(GREY,x,y,.5) for x,y in [(3.8,1.4),(4.5,0),(3.8,-1.4)]])
        arrows=VGroup(*[arr([3,y,0],[1.15,0,0]) for y in [1.4,0,-1.4]])
        self.at('the cues it reads')
        self.play(FadeIn(neighbors),Create(arrows),FadeIn(txt('cues',3.8,-2.6,32)),run_time=.5)
        self.wait(2)
        self.finish()

class S20Idea4(SpokenScene):
    def construct(self):
        self.add(layer_wall())
        early=neuron(ORANGE,S(-4.2),-2.65,.25); late=neuron(BLUE,S(-2),-2.65,.25)
        self.add(early)
        self.at('the earlier the birthday')
        self.play(early.animate.set_y(-.6),run_time=1.1)
        self.at('the deeper the layer')
        self.add(late)
        self.play(late.animate.set_y(2),run_time=1.2)
        self.play(FadeIn(txt('earlier birthday,\ndeeper layer',RC,-2.3,30)),run_time=.4)
        self.at('the neuron keeps maturing')
        halo=DashedVMobject(Circle(radius=.5,color=BLUE).move_to([S(-2),2,0]),num_dashes=16)
        self.play(Create(halo),FadeIn(label('maturation continues',2,BLUE)),run_time=.5)
        self.finish()

class S21Idea5(SpokenScene):
    def construct(self):
        m=menu(-2.8,0)
        self.add(m,txt('progenitor’s menu',-2.8,2.9,32,PURPLE))
        self.at('in normal development')
        self.play(FadeIn(txt('in normal\ndevelopment',3.2,1.3,30)),run_time=.4)
        self.at("the progenitor's menu gets shorter")
        self.play(Create(strike(m[1][0])),m[1][0].animate.set_opacity(.55),run_time=.4)
        self.wait(1)
        self.play(Create(strike(m[1][1])),m[1][1].animate.set_opacity(.55),run_time=.4)
        self.wait(1)
        self.at('with time')
        self.play(Create(arr([-5.3,-2.85,0],[-.3,-2.85,0])),FadeIn(txt('time',-2.8,-3.3)),FadeIn(txt('fewer choices\nwith time',3.2,-.6,30)),run_time=.4)
        self.finish()

class S22Hold(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(menu_final())
        self.wait(5)

class S23Take(SpokenScene):
    def construct(self):
        self.add(layer_wall(),txt('The takeaway',RC,3,34))
        self.add(txt('Cortical-plate neurons\nare born near the ventricle\nand climb.',RC,1.1,28,TEAL))
        n=neuron(TEAL,S(-3.8),-2.65,.28)
        self.at('cortical plate neurons')
        self.add(n,fibre())
        self.at('and climb')
        self.play(n.animate.set_y(-.6),run_time=.9)
        self.at('layers six to two')
        self.play(Create(CurvedArrow([S(-4.8),-.6,0],[S(-4.8),2,0],angle=-PI/3,color=TEXT)),run_time=.6)
        self.at('are made in that order')
        self.play(FadeIn(txt('Mouse cortical plate:\nlayers 6 to 2 are made\nin that order.',RC,-2.7,28,YELLOW)),run_time=.5)
        self.wait(2.5)
        self.finish()

class S24End(EndCard):
    LINE='Mouse cortical-plate neurons climb; layers form 6 first, 2 last.'
    def construct(self):
        self.add(txt('Mouse cortical-plate neurons climb;\nlayers form 6 first, 2 last.',0,.5,38),txt('biochemistrypedia.com',0,-1.2,28,TEAL))
        self.finish()
