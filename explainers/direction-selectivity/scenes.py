"""Chapter 1: A Veto From the Null Side — review redraw.
COLOR MAP: YELLOW stimulus/questions; BLUE ganglion/excitation/spikes;
PURPLE starburst/dendrites; GREEN preferred/outward; RED inhibition/null;
GREY receptive field/axes; GOLD contacts; TEAL brand. No molecular structures.
Bars are computed from 4+4=8, 2-8=-6, 14-8=6 (illustrative).
Timing model: E(t)=max(0,1-|t-4|/1.5), I(t)=E(t-delay).
Spike strip samples positive E-I above .25; schematic, not a recording.
"""
import numpy as np
from bp_style import *
PURPLE='#B58CD9'


def label(s,x=0,y=3.1,size=32,color=TEXT):
    return T(s,size,color,line_spacing=1.0).move_to([x,y,0])


def arr(a,b,color=GREY,w=5,tip=.26):
    return Arrow(a,b,buff=0,color=color,stroke_width=w,tip_length=tip,
                 max_tip_length_to_length_ratio=.45,max_stroke_width_to_length_ratio=12)


def ganglion(c,scale=1):
    # An oval soma with a short fork and descending axon: never a starburst.
    g=VGroup(Ellipse(width=.9,height=.65,color=BLUE,fill_opacity=.35),
        Line([-.4,.1,0],[-.8,.45,0],color=BLUE),
        Line([-.8,.45,0],[-1.05,.65,0],color=BLUE),
        Line([-.8,.45,0],[-1.1,.3,0],color=BLUE),
        Line([.4,.1,0],[.9,.5,0],color=BLUE),
        Line([.9,.5,0],[1.15,.7,0],color=BLUE),
        Line([.9,.5,0],[1.2,.35,0],color=BLUE),
        Line([0,-.32,0],[0,-1,0],color=BLUE))
    return g.scale(scale).shift(np.array(c))


def sac(center,R=2.5,w=3.5):
    c=np.array(center,float); soma=Circle(radius=.23,color=PURPLE,fill_opacity=.85).move_to(c)
    branches=[]
    for th in np.arange(4)*TAU/4:
        d=np.array([np.cos(th),np.sin(th),0]); parts=[Line(c+.23*d,c+R*d)]
        for f,s in ((.42,1),(.7,-1)):
            p=c+d*f*R; a=th+s*.6
            parts.append(Line(p,p+.25*R*np.array([np.cos(a),np.sin(a),0])))
        branches.append(VGroup(*parts).set_stroke(PURPLE,w))
    return soma,branches


def raster(y,dense=True,x0=-1.2,x1=5.6,h=.8):
    times=np.linspace(.06,.95,17) if dense else [.35]
    return VGroup(Line([x0,y,0],[x1,y,0],color=GREY),
        *[Line([x0+(x1-x0)*t,y,0],[x0+(x1-x0)*t,y+h,0],color=BLUE,stroke_width=4) for t in times])


def intro(terms=False):
    g=VGroup(ganglion([-4.5,.3,0],1.15),label('ganglion\ncell',-4.5,-1.6,32,BLUE),
        raster(.65),raster(-2.0,False),
        arr([-1.2,2.05,0],[5.6,2.05,0],GREEN),
        arr([5.6,-.65,0],[-1.2,-.65,0],RED),
        label('illustrative spikes',2.2,-2.65,30,GREY))
    if terms:g.add(label('preferred direction',2.2,2.65,32,GREEN),label('null direction',2.2,-.05,32,RED))
    return g


def field():
    return VGroup(Ellipse(width=10.8,height=5.2,color=GREY),
        Circle(radius=.75,color=YELLOW,fill_opacity=.15).move_to([-2.5,0,0]),
        Circle(radius=.75,color=YELLOW,fill_opacity=.15).move_to([2.5,0,0]),
        label('A',-2.5,-1.15,36,YELLOW),label('B',2.5,-1.15,36,YELLOW),
        arr([-2,1.7,0],[2,1.7,0],GREEN,7,.35),label('preferred →',0,3.15,32,GREEN),
        label('receptive field',0,-3.1,32,GREY))

BASE=-2.55
UNIT=.335
SUM=4+4
PX=-2.0
NX=2.3


def bar(x,n,color=BLUE):
    return Rectangle(width=1.2,height=n*UNIT,stroke_color=color,fill_color=color,fill_opacity=.65).move_to([x,BASE+n*UNIT/2,0])


def chart(sumline=True):
    axis=VGroup(Line([-5.25,BASE,0],[-5.25,BASE+16*UNIT,0],color=GREY),Line([-5.25,BASE,0],[5.5,BASE,0],color=GREY))
    for n in (0,4,8,12,16):
        y=BASE+n*UNIT
        axis.add(Line([-5.35,y,0],[-5.15,y,0],color=GREY),label(str(n),-5.8,y,30,GREY))
    g=VGroup(axis,label('spikes',-5.1,3.35,32,BLUE),label('Illustrative, not Barlow and Levick’s data',0,-3.45,30,GREY))
    if sumline:g.add(DashedLine([-5.2,BASE+SUM*UNIT,0],[5.4,BASE+SUM*UNIT,0],color=GREY),label('simple sum',4.0,BASE+SUM*UNIT+.35,30,GREY))
    return g


def pair_slots(outlines=True):
    return VGroup(*([Rectangle(width=1.2,height=SUM*UNIT,color=GREY,stroke_opacity=.4).move_to([x,BASE+SUM*UNIT/2,0]) for x in (PX,NX)] if outlines else []),
        label('A then B',PX,-2.95,30,GREEN),label('B then A',NX,-2.95,30,RED))


def prediction():
    return VGroup(chart(),pair_slots(),label('Veto: which falls below 8?',.6,2.65,32,YELLOW),label('Boost: which rises above 8?',.6,1.95,32,YELLOW))


def deficit():
    return VGroup(label('2 · deficit −6',NX,-1.25,30,RED))


def found(title=True):
    g=VGroup(chart(),pair_slots(False),bar(PX,8,GREEN),bar(NX,2,RED),deficit())
    if title:g.add(label('The pattern Barlow and Levick found',.5,3.25,30))
    return g


def veto_frame():
    g=found(False);g[4].move_to([4.5,-2.2,0])
    return VGroup(g,label('veto',3.7,-.65,36,RED),arr([3.4,-.95,0],[2.85,-1.85,0],RED,4))


def bump(t,c):return max(0.,1-abs(t-c)/1.5)


def timing_panel(late=False,x=0,compact=False):
    # Fixed sample coordinates, with a 0.06 vertical display offset for coincidence.
    width=10 if compact else 5.1
    left=x-width/2; bottom=-1.85 if compact else -1.2; height=1.9 if compact else 2.3
    def p(t,v):return np.array([left+t/10*width,bottom+v*height,0])
    axes=VGroup(Line(p(0,0),p(10,0),color=GREY),Line(p(0,0),p(0,1.12),color=GREY))
    e=VMobject().set_points_as_corners([p(t,bump(t,4)) for t in np.linspace(0,10,201)]).set_stroke(BLUE,7)
    i=VMobject().set_points_as_corners([p(t,bump(t,6 if late else 4)) + (UP*.065 if not late else 0) for t in np.linspace(0,10,201)]).set_stroke(RED,3.5)
    labs=VGroup(label('excitation',x-1.3,bottom+height+.42,30,BLUE),label('inhibition',x+1.35,bottom+height+.42,30,RED),
        Line([x-1.3,bottom+height+.2,0],p(3.2,bump(3.2,4)),color=BLUE,stroke_width=1.5),
        Line([x+1.35,bottom+height+.2,0],p(6 if late else 4,1)+UP*.065,color=RED,stroke_width=1.5))
    if compact:
        labs=VGroup(DashedLine([-.4,.35,0],p(3.2,bump(3.2,4)),color=BLUE,stroke_width=1.5),
            DashedLine([5.4,-.6,0],p(6 if late else 4,1)+UP*.065,color=RED,stroke_width=1.5))
    sy=-2.65 if compact else -2.05
    spikes=VGroup(Line([left,sy,0],[left+width,sy,0],color=GREY))
    for t in np.arange(0,10,.28):
        if bump(t,4)-bump(t,6 if late else 4)>.25:
            spikes.add(Line([p(t,0)[0],sy,0],[p(t,0)[0],sy+.45,0],color=BLUE,stroke_width=4))
    return VGroup(axes,e,i,labs,spikes)


def timing_pair():
    return VGroup(timing_panel(False,-3.2),timing_panel(True,3.2),
        label('Simple circuit sketch · input strength, illustrative',0,3.25,30,GREY),
        label('overlap',-3.2,2.45,34,RED),label('lag',3.2,2.45,34,GREEN),
        label('spikes cancelled',-3.2,-2.65,30,RED),label('early spikes survive',3.2,-2.65,30,BLUE),
        label('time →',0,-3.3,30,GREY))


def motion_stage():
    return VGroup(Rectangle(width=4.2,height=2.1,color=RED,fill_opacity=.1).move_to([3.3,1.8,0]),
        ganglion([-.4,1.65,0],.65),label('excitation',-.8,.55,30,BLUE),
        label('inhibition',3.5,.55,30,RED),label('null side',3.4,2.55,30,RED),
        Dot([-.4,1.65,0],color=BLUE,radius=.13),Dot([3.2,1.65,0],color=RED,radius=.13),
        DashedLine([5.4,1.7,0],[5.4,-.6,0],color=RED,stroke_width=1.5),
        label('ganglion cell',-3.7,2.45,30,BLUE),Line([-2.25,2.25,0],[-.85,1.9,0],color=BLUE,stroke_width=1.5))


def wiring(active=False):
    shade=VGroup(Rectangle(width=3.5,height=4.55,color=RED,fill_opacity=.07,stroke_opacity=.35).move_to([3.1,.45,0]),label('null side',3.1,2.95,30,RED))
    cells=VGroup(); keys=VGroup(); dots=VGroup()
    for y in (1.35,-.5):
        s,b=sac([2.65,y,0],R=1.25)
        # The connected spoke is the original left spoke, not an extended line.
        cells.add(VGroup(s,*[b[j] for j in (0,1,3)]))
        keys.add(b[2].set_stroke(width=10 if active else 5))
        dots.add(Dot([1.4,y,0],radius=.115,color=GOLD))
    s,b=sac([-4.85,.4,0],R=1.1)
    weak=VGroup(s,*b,Dot([-3.75,.4,0],radius=.06,color=GOLD)).set_opacity(.28)
    gc=VGroup(Ellipse(width=5.8,height=3.6,color=GOLD,fill_opacity=.035).move_to([-1.15,.4,0]),ganglion([-1.15,.4,0],.8))
    labs=VGroup(label('ganglion cell',-1.15,-1.65,30,BLUE),
        label('dendrites of the\nganglion cell',-3.6,2.5,30,GOLD),Line([-2.4,2.2,0],[-1.65,2.15,0],color=GOLD),
        label('illustrative sketch',4.1,-3.45,30,GREY))
    return VGroup(shade,cells,weak,gc,keys,dots,labs)


def circuit_result(dense):
    return VGroup(raster(-2.6,dense,-3.7,1.4,.55),label('ganglion cell spikes, illustrative',-1.15,-3.05,30,BLUE))


def branch_arrows():
    return VGroup(*[arr([2.3,y+.2,0],[1.5,y+.2,0],PURPLE,6,.32) for y in (1.35,-.5)])

RULE='The strongest inhibition comes from dendrites\nthat prefer roughly the direction\nthe ganglion cell ignores.'
SCOPE='One ingredient; tuned excitation and timing\nalso contribute in some cells.'

class S00Title(TitleCard):
    TITLE='A Veto From the Null Side'
    LESSON='Computing Motion in the Retina'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2,30,TEAL),label(self.LESSON,0,1.1,34,GREY))
        self.play(FadeIn(label(self.TITLE,0,0,46)),Create(Line([-1.2,-1,0],[1.2,-1,0],color=GOLD)),run_time=.6);self.finish()

class S01Q(SpokenScene):
    def construct(self):
        g=intro();self.add(g[0],g[1],g[6],label('A Veto From the Null Side',0,3.25,36),g[2][0],g[3][0])
        dot=Dot([-1.2,2.05,0],radius=.18,color=YELLOW)
        self.at('fires hard');self.play(FadeIn(dot),GrowArrow(g[4]),run_time=.25)
        self.play(dot.animate.move_to([5.6,2.05,0]),Create(VGroup(*g[2][1:])),run_time=1.65,rate_func=linear)
        self.at('Moving left');self.play(dot.animate.move_to([5.6,-.65,0]),GrowArrow(g[5]),run_time=.2)
        self.play(dot.animate.move_to([-1.2,-.65,0]),Create(g[3][1]),run_time=1.4,rate_func=linear)
        self.at('How does it');self.play(FadeOut(dot),FadeIn(label('How does it know?',-3.8,-3.0,34,YELLOW)),run_time=.3);self.finish()

class S02Terms(SpokenScene):
    def construct(self):
        self.add(intro())
        self.at('preferred direction');self.play(FadeIn(label('preferred direction',2.2,2.65,32,GREEN)),run_time=.35)
        self.at('null direction');self.play(FadeIn(label('null direction',2.2,-.05,32,RED)),run_time=.35);self.finish()

class S03Bh(SpokenScene):
    def construct(self):
        self.add(intro(True))
        self.at('Barlow and Hill');self.play(FadeIn(label('Barlow and Hill · 1963 · rabbit retina',0,3.4,30)),run_time=.35);self.finish()

class S04Bl(SpokenScene):
    def construct(self):
        self.add(label('How does it work?',0,.5,52,YELLOW),label('Barlow and Levick · 1965',0,-1,36))
        self.at('Two years later');self.play(Create(Line([-3,-2,0],[3,-2,0],color=GOLD)),run_time=.6);self.finish()

class S05Flash(SpokenScene):
    def construct(self):
        f=field();self.add(f)
        self.at('two neighboring spots');self.play(Indicate(f[1]),Indicate(f[2]),run_time=.5)
        self.at('spot I');self.play(f[1].animate.set_fill(opacity=.95),run_time=.2);self.wait(.8)
        self.at('spot B');self.play(f[1].animate.set_fill(opacity=.15),f[2].animate.set_fill(opacity=.95),run_time=.2);self.wait(.8)
        self.at('one after the other');self.play(f[2].animate.set_fill(opacity=.15),run_time=.2);self.finish()

class S06Orders(SpokenScene):
    def construct(self):
        f=field();self.add(f)
        a=arr([-1.6,0,0],[1.6,0,0],GREEN,8,.4);p=label('A then B · preferred order',0,-2,32,GREEN)
        self.at('I then B');self.add(p);self.play(f[1].animate.set_fill(opacity=.95),GrowArrow(a),run_time=.3);self.wait(.55)
        self.play(f[1].animate.set_fill(opacity=.15),f[2].animate.set_fill(opacity=.95),run_time=.25)
        self.at('B then I');self.remove(p,a);self.add(label('B then A · null order',0,-2,32,RED))
        self.play(f[2].animate.set_fill(opacity=.95),GrowArrow(arr([1.6,0,0],[-1.6,0,0],RED,8,.4)),run_time=.3);self.wait(.55)
        self.play(f[2].animate.set_fill(opacity=.15),f[1].animate.set_fill(opacity=.95),run_time=.25);self.finish()

class S07Sum(SpokenScene):
    def construct(self):
        c=chart(False);a=bar(-2.6,4);b=bar(2.6,4)
        self.add(c,label('4 + 4 = 8',.4,2.7,40),a,b,label('A alone · 4',-2.6,-2.95,30),label('B alone · 4',2.6,-2.95,30))
        self.at('simply added');self.play(TransformFromCopy(a,bar(0,4)),TransformFromCopy(b,bar(0,4).shift(UP*4*UNIT)),FadeIn(label('A + B added',0,-2.95,30)),run_time=.8)
        self.at('dashed line');s=chart();self.play(Create(s[3]),FadeIn(s[4]),run_time=.4);self.finish()

class S08Predict(SpokenScene):
    def construct(self):
        g=prediction();self.add(g[0],g[1])
        self.at('Under a veto');self.play(FadeIn(g[2]),run_time=.3)
        self.at('Under a boost');self.play(FadeIn(g[3]),run_time=.3);self.finish()

class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(prediction(),label('Pause. Decide before you go on.',0,-.7,30,YELLOW))
        self.add(Line([-3,-1.65,0],[3,-1.65,0],color=GREY,stroke_width=3))
        self.play(Create(Line([-3,-1.65,0],[3,-1.65,0],color=YELLOW,stroke_width=7)),run_time=5,rate_func=linear)

class S10Reveal(SpokenScene):
    def construct(self):
        self.add(chart(),pair_slots(False),label('remainder = paired − sum',.7,3.25,30))
        self.at('A veto leaves');self.add(label('veto',NX,-1.45,32,RED));self.play(GrowFromEdge(bar(NX,2,RED),DOWN),run_time=.35)
        self.add(label('2 − 8 = −6',4.65,-1.3,30,RED),DoubleArrow([3.2,BASE+2*UNIT,0],[3.2,BASE+8*UNIT,0],buff=0,color=RED,tip_length=.16))
        self.at('A boost leaves');self.add(label('boost',PX,2.7,32,GREEN),bar(PX,14,GREEN))
        self.play(FadeIn(label('14 − 8 = +6',1.0,1.75,30,GREEN)),Create(DoubleArrow([-.9,BASE+8*UNIT,0],[-.9,BASE+14*UNIT,0],buff=0,color=GREEN,tip_length=.16)),run_time=.3);self.finish()

class S11Found(SpokenScene):
    def construct(self):
        b=bar(PX,14,GREEN);self.add(chart(),pair_slots(False),b,bar(NX,2,RED),deficit(),label('The pattern Barlow and Levick found',.6,3.25,30))
        self.at('found a big deficit');self.play(Indicate(self.mobjects[3]),run_time=.4)
        self.at('preferred order');self.play(Transform(b,bar(PX,8,GREEN)),run_time=.75);self.finish()

class S12Veto(SpokenScene):
    def construct(self):
        g=found();self.add(g)
        self.at('is a veto');v=veto_frame();self.play(FadeOut(g[-1]),g[4].animate.move_to([4.5,-2.2,0]),FadeIn(v[1]),GrowArrow(v[2]),run_time=.4);self.finish()

class S13Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(veto_frame());self.wait(2)

class S14Local(SpokenScene):
    def construct(self):
        self.add(field()[0],label('local veto',0,3.15,34,RED),label('small subunits',0,2.25,32),label('flat-ended line = veto',0,-3.15,30,RED))
        patches=[]
        for x in (-2.7,0,2.7):
            for y in (-.95,.95):
                patches.append(VGroup(RoundedRectangle(width=2.3,height=1.55,corner_radius=.15,color=GREY).move_to([x,y,0]),Line([x-.65,y,0],[x+.45,y,0],color=RED,stroke_width=5),Line([x+.45,y-.35,0],[x+.45,y+.35,0],color=RED,stroke_width=6)))
        self.at('They also inferred');self.play(LaggedStart(*[FadeIn(p) for p in patches],lag_ratio=.4),run_time=2.8);self.finish()

class S15Timing(SpokenScene):
    def construct(self):
        g=timing_pair();self.add(g[2],g[3],g[4],g[7],g[0][0],g[1][0],g[0][4][0],g[1][4][0])
        self.at('simple sketch');self.play(Create(g[0][1]),Create(g[1][1]),FadeIn(g[0][3]),FadeIn(g[1][3]),run_time=.65)
        self.at('To cancel excitation');self.play(Create(g[0][2]),Create(g[1][2]),run_time=.7)
        self.at('inhibition must overlap');self.play(FadeIn(g[5]),FadeIn(g[6]),*[Create(s) for s in g[1][4][1:]],run_time=.7);self.finish()

class S16Side(SpokenScene):
    def construct(self):
        self.add(motion_stage(),timing_panel(False,compact=True),label('input strength · illustrative',-2.8,-3.3,30,GREY),label('time →',4.6,-3.3,30,GREY))
        dot=Dot([5.1,1.65,0],radius=.18,color=YELLOW);self.add(dot)
        self.at('Null motion');self.add(arr([.5,3.3,0],[-3.8,3.3,0],RED));self.wait(.45)
        self.play(dot.animate.move_to([-4.7,1.65,0]),run_time=4.1,rate_func=linear)
        self.at('Call that');self.play(Indicate(self.mobjects[0][0],color=RED),run_time=.5);self.finish()

class S17Late(SpokenScene):
    def construct(self):
        g=timing_panel(False,compact=True);late=timing_panel(True,compact=True)
        self.add(motion_stage(),g,label('input strength · illustrative',-2.8,-3.3,30,GREY),label('time →',4.6,-3.3,30,GREY))
        dot=Dot([-4.7,1.65,0],radius=.18,color=YELLOW);self.add(dot)
        self.at('Preferred motion');self.add(arr([-3.8,3.3,0],[.5,3.3,0],GREEN),label('excitation leads',-3.9,.8,30,BLUE))
        self.play(Transform(g,late),run_time=.6)
        self.play(dot.animate.move_to([6.0,1.65,0]),run_time=4.1,rate_func=linear)
        self.at('a head start');self.play(Indicate(g[4],color=BLUE),run_time=.4);self.finish()

class S18Who(SpokenScene):
    def construct(self):
        box=Rectangle(width=6.4,height=5.1,color=RED,fill_opacity=.08).move_to([2.4,0,0]);self.add(box,label('null side',2.4,2.95,32,RED),ganglion([-3.3,.2,0],1.3),label('ganglion cell',-3.5,-2,32,BLUE))
        s,b=sac([2.4,0,0],R=1.8);q=label('?',2.4,0,64,YELLOW)
        self.at('were tentative');self.play(FadeIn(q),run_time=.2)
        self.at('Most of it');self.play(FadeOut(q),FadeIn(s),*[Create(v) for v in b],run_time=1.3)
        self.at('starburst amacrine cells');self.play(FadeIn(VGroup(label('starburst amacrine cell',2.4,-2.15,30,PURPLE),Line([3.7,-1.85,0],[3.1,-.65,0],color=PURPLE,stroke_width=1.5))),run_time=.3);self.finish()

class S19Sac(SpokenScene):
    def construct(self):
        s,b=sac([0,0,0],R=2.6);self.add(s,label('starburst amacrine cell',0,-3.3,32,PURPLE))
        self.at('dendrites radiate');self.play(*[Create(v) for v in b],run_time=1.2);self.finish()

class S20Branch(SpokenScene):
    def construct(self):
        s,b=sac([0,0,0],R=2.6);self.add(s,*b,label('starburst amacrine cell',0,-3.3,32,PURPLE));dot=Dot([2.6,0,0],radius=.18,color=YELLOW)
        inward=label('inward: little release',0,3.2,34,GREY)
        self.at('Each dendrite');self.add(inward,dot);self.play(*[v.animate.set_opacity(.35) for v in b],run_time=.25)
        self.play(dot.animate.move_to([.3,0,0]),run_time=2.0,rate_func=linear)
        self.at('most active');self.play(FadeOut(inward),FadeIn(label('outward: most active',0,3.2,34,GREEN)),run_time=.3)
        self.at('motion runs outward');self.play(dot.animate.move_to([2.6,0,0]),b[0].animate.set_stroke(width=12,opacity=1),run_time=2.1,rate_func=linear);self.finish()

class S21Wire(SpokenScene):
    def construct(self):
        w=wiring();self.add(w[0],w[1],w[2])
        self.at('a ganglion cell');self.play(FadeIn(w[3]),FadeIn(w[6]),run_time=.4)
        self.at('prefers rightward motion');self.play(GrowArrow(arr([-1.3,3.25,0],[.7,3.25,0],GREEN)),run_time=.3)
        self.at('wired mainly');self.play(Create(w[4]),FadeIn(w[5]),run_time=.65)
        self.at('point left');self.play(*[GrowArrow(a) for a in branch_arrows()],run_time=.4);self.finish()


def run_branch_case(scene,dense):
    w=wiring();scene.add(w,circuit_result(dense)[0][0],circuit_result(dense)[1])
    direction=GREEN if dense else RED
    arrow=arr([-1.4,3.25,0],[.8,3.25,0],direction) if dense else arr([.8,3.25,0],[-1.4,3.25,0],direction)
    starts=[np.array([1.4 if dense else 2.42,y,0]) for y in (1.35,-.5)]
    ends=[np.array([2.42 if dense else 1.4,y,0]) for y in (1.35,-.5)]
    spots=VGroup(*[Dot(p,radius=.17,color=YELLOW,fill_opacity=1) for p in starts])
    scene.at('Rightward motion' if dense else 'Leftward motion');scene.add(arrow,spots)
    scene.at('runs inward' if dense else 'runs outward')
    state=label('weaker inhibition' if dense else 'stronger inhibition',3.9,-2.05,30,RED)
    response=circuit_result(dense)[0]
    scene.add(state)
    scene.play(*[d.animate.move_to(p) for d,p in zip(spots,ends)],w[4].animate.set_stroke(width=3 if dense else 13,opacity=.23 if dense else 1),
        Create(VGroup(*response[1:])),run_time=3.0,rate_func=linear)
    scene.play(FadeOut(spots),run_time=.2)
    if dense:
        scene.at('excitation wins');scene.play(FadeIn(label(SCOPE,0,3.15,30,GREY)),FadeOut(arrow),FadeOut(w[6][1]),FadeOut(w[6][2]),w[0][1].animate.move_to([4.0,2.35,0]),run_time=.3)
    else:
        scene.at('stays quiet');scene.play(Indicate(response,color=BLUE),run_time=.4)
    scene.finish()

class S22Null(SpokenScene):
    def construct(self):run_branch_case(self,False)

class S23Pref(SpokenScene):
    def construct(self):run_branch_case(self,True)

class S24Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;w=wiring();w[4].set_stroke(width=3,opacity=.23)
        w[6].remove(w[6][1],w[6][2]);w[0][1].move_to([4.0,2.35,0])
        self.add(w,circuit_result(True),label('weaker inhibition',3.9,-2.05,30,RED),label(SCOPE,0,3.15,30,GREY));self.wait(2)

class S25Rule(SpokenScene):
    def construct(self):
        w=wiring();w[6].remove(w[6][-1])
        # Reserve a separate lower band for the rule; keep preference keys above the circuit.
        preferences=branch_arrows()
        diagram=VGroup(w,preferences).scale(.75,about_point=ORIGIN).shift(UP*.3)
        self.add(w)
        self.at('remember the sign');self.play(GrowArrow(arr([-4,3.0,0],[-2,3.0,0],GREEN)),FadeIn(label('ganglion cell prefers',-3,3.5,30,GREEN)),run_time=.3)
        self.at('strongest inhibition');self.play(w[4].animate.set_stroke(width=12),Indicate(w[5],color=GOLD),run_time=.5)
        self.at('dendrites that prefer roughly');self.play(FadeIn(label(RULE,0,-2.75,30)),*[GrowArrow(a) for a in preferences],GrowArrow(arr([4,3.0,0],[2,3.0,0],PURPLE)),FadeIn(label('dendrite preference',3,3.5,30,PURPLE)),run_time=.5);self.finish()

class S26End(EndCard):
    # TASK.md explicitly asks for the full shared rule on this card.
    LINE=RULE.replace('\n',' ')
    def construct(self):
        self.add(label('Remember the sign',0,2.2,34,GREEN))
        self.play(FadeIn(label('The strongest inhibition comes from\ndendrites that prefer roughly the direction\nthe ganglion cell ignores.',0,0,38)),run_time=.6)
        self.play(FadeIn(label('biochemistrypedia.com',0,-2,30,TEAL)),run_time=.3);self.finish()
