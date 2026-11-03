"""A Label Is Not a Wire — revised chapter animation.
COLOR MAP: BLUE genome / names; YELLOW axons / cones; GREY anatomy / axes;
ORANGE EphA receptor; PURPLE ephrin-A cue; TEAL rules; GREEN activity;
RED unknown / blockade / removal; GOLD title rule. The position palette encodes
retinal origin consistently in all maps, plots, and arbors (not cell type).
All quantitative traces are calculated from the lesson's threshold model.
"""
import numpy as np
from math import erf, sqrt
from bp_style import *
from bp_style import SpokenScene as _SpokenScene, chip as _chip

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
POSITION = ['#58C4DD', '#65C6A6', '#D4CF73', '#F29E4C', '#D598C8']

class SpokenScene(_SpokenScene):
    # Wait for the actual word onset. The shared helper's log records the time
    # BEFORE waiting, not the reveal time; do not treat that as a reveal log.
    def at(self, phrase, lead=0, nth=0):
        rest = self.t_of(phrase, nth) - self.elapsed()
        if rest > 0.001:
            self.wait(rest)

def chip(text, color=BLUE, size=28, **kw):
    c=_chip(text,color,size=size,**kw)
    c[0].set_fill(BG,opacity=1)
    return c

def heading(s, color=TEXT):
    return T(s, 34, color).move_to([0, 3.12, 0])

def statement(s, color=TEXT):
    return T(s, 44, color)

def cell(r=.28, color=YELLOW):
    return Circle(radius=r, color=color, stroke_width=3, fill_opacity=.3)

def poscolor(x):
    z=np.clip(x,0,1)*(len(POSITION)-1); i=min(int(z),len(POSITION)-2)
    return interpolate_color(ManimColor(POSITION[i]),ManimColor(POSITION[i+1]),z-i)

def path(points, color=YELLOW, width=4):
    return VMobject(color=color, stroke_width=width).set_points_smoothly([np.array(p,dtype=float) for p in points])

def toggle(on=True, scale=1):
    body=RoundedRectangle(width=1.2,height=.55,corner_radius=.25,color=BLUE,fill_opacity=.3)
    knob=Dot([.3 if on else -.3,0,0],radius=.19,color=TEXT)
    return VGroup(body,knob).scale(scale)

def genome_strip():
    return VGroup(chip('whole genome',BLUE,28),VGroup(*[Rectangle(width=.18,height=.34,color=BLUE,fill_opacity=.3+(j%3)*.2) for j in range(12)]).arrange(RIGHT,buff=.035)).arrange(DOWN,buff=.22)

def leg():
    # Seated profile: a broad horizontal thigh, round patella, tapered calf,
    # ankle and foot. Rotation is about the knee, not the centre of the drawing.
    thigh=path([[-5.6,1.9,0],[-4.8,1.5,0],[-2,1.4,0],[-.9,.9,0]],GREY,48)
    seat=VGroup(Line([-5.8,1,0],[-2.7,1,0],color=GREY,stroke_width=7),Line([-5.1,1,0],[-5.1,-2.8,0],color=GREY,stroke_width=6))
    knee=np.array([-.9,.9,0]); calf=Polygon([-.93,1,0],[-.5,.65,0],[-.6,-.7,0],[-1.03,-2.4,0],[-1.4,-2.4,0],[-1.38,-.7,0],color=GREY,fill_opacity=.55,stroke_width=3)
    foot=path([[-1.2,-2.3,0],[-1.1,-2.7,0],[.05,-2.75,0],[.5,-2.6,0]],GREY,18)
    shin=VGroup(calf,foot)
    patella=Ellipse(width=.35,height=.65,color=TEXT,fill_opacity=.4).move_to([-.55,.8,0])
    tendon=Line([-.55,.4,0],[-.58,.1,0],color=YELLOW,stroke_width=7)
    hammer=VGroup(Line([2.4,1.9,0],[.8,1,0],color=TEXT,stroke_width=7),RoundedRectangle(width=.3,height=.75,corner_radius=.1,color=BLUE,fill_opacity=1).move_to([.8,1,0]))
    labels=VGroup(T('tendon',28,YELLOW).move_to([1.3,-.2,0]),Line([.55,-.2,0],[-.4,.2,0],color=YELLOW))
    return VGroup(thigh,shin,patella,hammer,seat,tendon,labels)

def muscle(x,label):
    outline=Ellipse(width=1.45,height=3.8,color=GREY,fill_opacity=.15).move_to([x,-.1,0])
    fibres=VGroup(*[path([[x+d,1.5,0],[x+d*.8,0,0],[x+d,-1.7,0]],GREY,2) for d in [-.4,-.2,0,.2,.4]])
    return VGroup(outline,fibres,T(label,28).move_to([x,-2.45,0]))

def sign(s,p,color):
    return VGroup(Circle(radius=.35,color=color,stroke_opacity=.5,fill_opacity=.13).move_to(p),T(s,46,color).move_to(p))

def circuit(inhib=False):
    quad=muscle(-5,'quadriceps'); cord=VGroup(RoundedRectangle(width=5.1,height=5.3,corner_radius=.5,color=GREY,fill_opacity=.07).move_to([.8,-.1,0]),T('spinal cord',28,GREY).move_to([.8,-3.05,0]))
    spindle=VGroup(Ellipse(width=.43,height=.9,color=BLUE,fill_opacity=.3).move_to([-5,1,0]),path([[-5.12,1.3,0],[-4.9,1.15,0],[-5.12,.95,0],[-4.9,.75,0]],BLUE,3))
    # Distinct horizontal sensory and low motor routes; boutons touch soma.
    sensory=VGroup(spindle,path([[-4.8,1.1,0],[-3,1.1,0],[-1.5,1.1,0],[-.35,1.1,0]],BLUE,5),Dot([-.35,1.1,0],radius=.11,color=BLUE),T('sensory neuron (Ia)',28,BLUE).move_to([-2.8,1.85,0]),T('muscle spindle',26,BLUE).move_to([-4.7,2.6,0]))
    motor=VGroup(cell(.35).move_to([0,1.1,0]),path([[0,.75,0],[-.5,-1.15,0],[-3,-1.15,0],[-4.65,-1.15,0]],YELLOW,4),Dot([-4.65,-1.15,0],radius=.1,color=YELLOW),T('motor neuron',28,YELLOW).move_to([1.3,1.85,0]))
    plus=sign('+',[-.85,.45,0],GREEN)
    labels=VGroup()
    g=VGroup(quad,cord,sensory,motor,plus,labels)
    if inhib:
        inter=cell(.23,GREY).move_to([1.25,-.1,0]); motor2=cell(.35).move_to([2.5,-1.25,0]); ham=muscle(5.25,'hamstring')
        route=VGroup(path([[-.7,1.1,0],[-.6,1.55,0],[.65,1.2,0],[1.02,-.1,0]],BLUE,4),Dot([1.02,-.1,0],radius=.1,color=BLUE),inter,path([[1.48,-.1,0],[2,-.4,0],[2.5,-.9,0]],GREY,4),Dot([2.5,-.9,0],radius=.11,color=GREY),motor2,path([[2.85,-1.25,0],[3.8,-1.25,0],[4.9,-1.25,0]],YELLOW,4),Dot([4.9,-1.25,0],radius=.1,color=YELLOW),ham,T('inhibitory interneuron',26,GREY).move_to([.2,-2.3,0]),Line([.8,-1.98,0],[1.23,-.38,0],color=GREY),sign('−',[2.9,-.35,0],RED))
        g.add(route)
    return g

def brain():
    # Schematic lateral silhouette with frontal bulge, cerebellum, and stem.
    pts=[[-5.9,-.4,0],[-6,1.1,0],[-5.4,2.4,0],[-3.9,2.8,0],[-2,2.6,0],[-1,1.7,0],[-.9,.1,0],[-1.15,-.45,0],[-1.05,-1.15,0],[-1.55,-1.65,0],[-2.4,-1.55,0],[-2.65,-1.1,0],[-2.4,-2.4,0],[-3,-2.5,0],[-3.4,-1,0],[-4.5,-1.3,0],[-5.9,-.4,0]]
    outline=path(pts,YELLOW,4).set_fill(YELLOW,.08)
    folds=VGroup(*[path([[-5.5+i*.7,.1,0],[-5.6+i*.7,1.1,0],[-5.1+i*.7,1.8,0]],GREY,2) for i in range(5)])
    folds.add(path([[-2.7,-.4,0],[-1.9,-.6,0],[-1.15,-.45,0]],GREY,2))
    for y in [-.85,-1.05,-1.25]:folds.add(path([[-2.4,y,0],[-1.8,y-.15,0],[-1.15,y,0]],GREY,2))
    rng=np.random.default_rng(7); dots=VGroup()
    for x,y in rng.uniform([-5.7,-.6],[-1.5,2.4],(320,2)):
        if ((x+3.7)/2.3)**2+((y-.9)/1.6)**2<1:dots.add(Dot([x,y,0],radius=.022,color=YELLOW))
    return VGroup(outline,folds,dots,Dot([-3.8,-.55,0],radius=.07,color=TEAL),T('human brain',28,YELLOW).move_to([-3.7,-3.12,0]))

def counters(n):
    data=[('86 billion\nneurons',YELLOW),('≈ 100 trillion synapses\n10¹⁴',GREY),('≈ 20,000\nprotein-coding genes',BLUE)]
    return VGroup(*[T(t,30,c,line_spacing=.9).move_to([3.1,2.25-i*1.55,0]) for i,(t,c) in enumerate(data[:n])])

def naming_question():
    one=VGroup(cell(1.4),RoundedRectangle(width=2.4,height=.8,corner_radius=.15,color=BLUE).move_to([0,-2,0]),T('?',40,BLUE).move_to([0,-2,0]))
    for a in np.linspace(0,TAU,9)[:-1]:one.add(Line(1.4*np.array([np.cos(a),np.sin(a),0]),2.15*np.array([np.cos(a),np.sin(a),0]),color=YELLOW,stroke_width=4))
    return VGroup(heading('Is naming the problem?',RED),one)

def named_crowd():
    crowd=VGroup()
    for i in range(48):
        x=-5.6+(i%8)*1.6;y=2.25-(i//8)*.92;c=cell(.21).move_to([x,y,0])
        tag=Square(side_length=.2,color=poscolor(i/47),fill_opacity=1).move_to([x+.32,y-.15,0])
        # A distinct numeric code makes identity explicit even for nearby hues.
        code=T(f'{i+1:02}',26,BLUE).move_to([x+.44,y+.3,0])
        crowd.add(VGroup(c,VGroup(tag,code)))
    return crowd

def retina():
    slices=VGroup();r=2.6;cx=-3.9
    for i in range(80):
        x0=-r+2*r*i/80;x1=-r+2*r*(i+1)/80
        ya=np.sqrt(max(0,r*r-x0*x0));yb=np.sqrt(max(0,r*r-x1*x1))
        slices.add(Polygon([cx+x0,-ya,0],[cx+x1,-yb,0],[cx+x1,yb,0],[cx+x0,ya,0],stroke_width=0,fill_color=ORANGE,fill_opacity=.12+.7*10**(i/79)/10))
    return VGroup(slices,Circle(radius=r,color=ORANGE).move_to([cx,0,0]),T('retina · EphA receptor',28,ORANGE).move_to([cx,-3,0]),T('receptor level: low → high',26,ORANGE).move_to([cx,-3.5,0]))

def target():
    bars=VGroup(*[Rectangle(width=6.5/60,height=5.2,stroke_width=0,fill_color=PURPLE,fill_opacity=.1+.7*10**(-i/59)).move_to([-.5+6.5*(i+.5)/60,0,0]) for i in range(60)])
    return VGroup(bars,T('midbrain target · ephrin-A cue',26,PURPLE).move_to([2.75,-3,0]),T('high cue → low cue',26,PURPLE).move_to([2.75,-3.5,0]))

def map_stage():
    return VGroup(retina(),target())

def map_sources():
    return VGroup(*[Dot([-6.5+5.2*x,1.45-2.9*x,0],radius=.13,color=poscolor(x)) for x in np.linspace(.1,.9,5)])

def ordered_axons():
    g=VGroup()
    for x in np.linspace(.1,.9,5):
        y=1.45-2.9*x;end=[-.5+6.5*x,y,0]
        g.add(VGroup(Line([-1.1,y,0],end,color=poscolor(x),stroke_width=4),Dot(end,radius=.13,color=poscolor(x))))
    return g

def cone(p):
    return VGroup(Triangle(color=YELLOW,fill_opacity=1).scale(.14).rotate(-PI/2),*[Line([.08,y*.035,0],[.27,y*.1,0],color=YELLOW,stroke_width=2) for y in [-2,-1,0,1,2]]).move_to(p)

def rule_card(n,title):
    return VGroup(T(f'RULE {n}',32,TEAL),T(title,46,TEAL),Line([-4,0,0],[4,0,0],color=TEAL)).arrange(DOWN,buff=.65)

def branches(tight=False):
    g=VGroup()
    for j,y in enumerate([1.8,0,-1.8]):
        col=poscolor(j/2);c=cell(.35,col).move_to([-5.6,y,0]);trunk=Line([-5.25,y,0],[-1.6,y,0],color=col,stroke_width=4)
        if tight:
            # A single shaft ends in a short tuft, within a compact target patch.
            trunk=Line([-5.25,y,0],[3.7,y,0],color=col,stroke_width=4)
            fan=VGroup(Ellipse(width=1.25,height=.72,color=col,stroke_opacity=.4,fill_opacity=.08).move_to([4.35,y,0]))
            fan.add(*[path([[3.7,y,0],[4.05,y+d*.5,0],[4.75,y+d,0]],col,3) for d in np.linspace(-.23,.23,7)])
        else:
            fan=VGroup(*[path([[-1.6,y,0],[1,y+d*.4,0],[5.6,y+d,0]],col,3) for d in np.linspace(-1.1,1.1,7)])
        g.add(VGroup(c,trunk,fan))
    return g

def fish():
    body=path([[-3.7,.2,0],[-2.3,2.1,0],[.5,2.3,0],[3.9,1.4,0],[5.8,.4,0],[5.1,-.6,0],[3.7,-1.4,0],[.4,-1.6,0],[-2.5,-1,0],[-3.7,.2,0]],ORANGE,4).set_fill(ORANGE,.17)
    tail=Polygon([-3.7,.2,0],[-6,1.9,0],[-5.5,.1,0],[-6,-1.7,0],color=ORANGE,fill_opacity=.3)
    fin=VGroup(Polygon([-.8,2.05,0],[.6,2.9,0],[2.5,2.03,0],color=ORANGE,fill_opacity=.2),path([[.7,.1,0],[-.5,-.6,0],[1.8,-.5,0]],ORANGE,3),Arc(radius=1.05,start_angle=-1.1,angle=2.2,color=ORANGE).move_to([3.5,.3,0]))
    eye=VGroup(Circle(radius=.48,color=ORANGE,fill_color=BG,fill_opacity=1),Dot(radius=.17,color=TEXT)).move_to([4.5,.7,0])
    br=chip('brain',GREY,26).move_to([.2,.7,0]); nerve=Line([4,.7,0],[1,.7,0],color=YELLOW,stroke_width=6)
    return VGroup(body,tail,eye,br,nerve,fin)

def test_question():
    return VGroup(heading('Which part of the map survives?',RED),chip('rough order?',TEXT,40,pad=.5).move_to([-3.3,0,0]),chip('fine precision?',TEXT,40,pad=.5).move_to([3.3,0,0]),T('cut optic nerve + tetrodotoxin in the eye',28,GREY).move_to([0,1.8,0]))

def panel(x,wide=False,title='untreated',top=2.9,bottom=-2.7):
    # Five ordered origins and color-matched landing centres. Wide arbors overlap
    # neighbours without reversing their centres. Anatomy is schematic.
    g=VGroup(T(title,28).move_to([x,top,0]));height=top-bottom-1.4
    for j in range(5):
        y=top-.95-j*height/4;col=poscolor(j/4)
        soma=cell(.17,col).move_to([x-2.45,y,0]);line=Line([x-2.28,y,0],[x-.35,y,0],color=col,stroke_width=3)
        fan=VGroup(*[path([[x-.35,y,0],[x+.65,y+d*.4,0],[x+2.1,y+d,0]],col,2.5) for d in np.linspace(-.72 if wide else -.15,.72 if wide else .15,5)])
        g.add(VGroup(soma,line,fan,Dot([x+1.2,y,0],radius=.065,color=col)))
    return g

def comparison(wide=True):
    return VGroup(panel(-3.3,False,'untreated goldfish'),panel(3.3,wide,'tetrodotoxin'))

def embryo(x,y,scale=1):
    yolk=Ellipse(width=2,height=1.55,color=ORANGE,fill_opacity=.2).move_to([x,y-.2,0])
    body=path([[x-1.05,y+.05,0],[x-1.2,y+.65,0],[x-.9,y+1.03,0],[x-.2,y+1.12,0],[x+.65,y+.8,0],[x+1.25,y+.2,0],[x+1.65,y-.12,0],[x+2,y+.2,0],[x+1.77,y-.38,0],[x+1.4,y-.42,0],[x+.85,y+.05,0],[x+.2,y+.42,0],[x-.55,y+.3,0],[x-1.05,y+.05,0]],ORANGE,3.5).set_fill(ORANGE,.2)
    eye=VGroup(Circle(radius=.28,color=ORANGE,fill_color=BG,fill_opacity=1),Dot(radius=.1,color=TEXT)).move_to([x-.75,y+.65,0])
    return VGroup(yolk,body,eye).scale(scale,about_point=[x,y,0])

def embryo_comparison(results=True):
    g=VGroup(heading('zebrafish embryo · first map',ORANGE))
    for x,title in [(-3.3,'untreated'),(3.3,'tetrodotoxin')]:
        g.add(embryo(x-.35,1.3,.8),T(title,28).move_to([x,2.6,0]))
        if x>0:g.add(chip('no spikes',RED,26).move_to([5.25,1.9,0]))
    if results:
        g.add(panel(-3.3,False,'ordered map',top=.15,bottom=-2.7),panel(3.3,False,'ordered map',top=.15,bottom=-2.7),T('small, tight arbors · in the early window measured',28,TEAL).move_to([0,-3.25,0]))
    return g

def case_cards():
    g=VGroup(heading('Different conditions · different outcomes',TEAL))
    for x,title,context,wide in [(-3.3,'adult goldfish','regrowing a map',True),(3.3,'zebrafish embryo','building a first map',False)]:
        g.add(T(title,30,ORANGE).move_to([x,2.3,0]),T(context,28).move_to([x,1.6,0]),panel(x,wide,'TTX: order kept',top=.8,bottom=-2.4),T('wide endings' if wide else 'small endings',30,TEAL).move_to([x,-2.6,0]))
    g.add(T('Age and developmental context may matter',28,GREY).move_to([0,-3.35,0]))
    return g

# N=200, F=10, sigma=.1: local linearisation of Gaussian fractional
# threshold-reading error, exactly as in the lesson sketch. Seed is illustrative.
XX=np.linspace(0,1,200)
YY=XX+np.random.default_rng(12).normal(0,.1/np.log(10),200)
RHO=float(np.corrcoef(np.argsort(np.argsort(XX)),np.argsort(np.argsort(YY)))[0,1])
PPAIR=.5*(1+erf((1/199)/(.1/np.log(10)*2)))

def scatter_stage(noisy=True,stats=True,inset=True):
    g=VGroup(T('simple model · not measured anatomy',28,TEAL).move_to([0,3.35,0]))
    ax=Axes(x_range=[-.06,1.06,.5],y_range=[-.1,1.1,.5],x_length=6.4,y_length=5.2,tips=False,axis_config={'include_ticks':False,'stroke_color':GREY}).move_to([-2.45,-.15,0])
    labels=VGroup(T('retinal position, nasal → temporal',26).move_to([-2.3,-3.5,0]),T('landing position in target',26).rotate(PI/2).move_to([-6.3,0,0]))
    for v in [0,1]:
        labels.add(T(str(v),26).move_to(ax.c2p(v,-.16)),T(str(v),26).move_to(ax.c2p(-.11,v)))
    dots=VGroup(*[Dot(ax.c2p(x,y),radius=.035,color=poscolor(x)) for x,y in zip(XX,YY if noisy else XX)])
    params=T('N = 200 axons · F = 10 (tenfold)',26).move_to([-2.4,2.65,0])
    g.add(ax,labels,params,dots)
    if noisy:g.add(T('σ = 0.1 · 10% reading error',26,RED).move_to([3.85,1.45,0]))
    if stats:g.add(T(f'overall rank order: {RHO:.2f}',28,TEAL).move_to([3.85,2.55,0]),T('adjacent pairs: ≈ 53%',28,RED).move_to([3.85,1.95,0]))
    if inset:
        # Four actual adjacent model points, expanded with both coordinates.
        inds=np.arange(96,100);xmin=XX[96]-.003;xmax=XX[99]+.003;ymin=min(YY[inds])-.008;ymax=max(YY[inds])+.008
        box=Rectangle(width=4.1,height=3.65,color=GREY).move_to([3.85,-.8,0]);g.add(box,T('neighbours, magnified',26).move_to([3.85,.8,0]))
        for i in inds:
            p=np.array([2.35+(XX[i]-xmin)/(xmax-xmin)*2.9,-2.2+(YY[i]-ymin)/(ymax-ymin)*2.25,0])
            g.add(Dot(p,radius=.08,color=poscolor(XX[i])),T(str(i+1),26,poscolor(XX[i])).next_to(p,UP,buff=.13))
        for i in inds[:-1]:
            if YY[i]>YY[i+1]:
                a=np.array([2.35+(XX[i]-xmin)/(xmax-xmin)*2.9,-2.2+(YY[i]-ymin)/(ymax-ymin)*2.25,0]);b=np.array([2.35+(XX[i+1]-xmin)/(xmax-xmin)*2.9,-2.2+(YY[i+1]-ymin)/(ymax-ymin)*2.25,0]);g.add(Ellipse(width=abs(b[0]-a[0])+.45,height=abs(b[1]-a[1])+.75,color=RED,stroke_width=2).move_to((a+b)/2))
        zoom=Rectangle(width=.65,height=1,color=RED).move_to(ax.c2p(.49,.5));g.add(zoom,DashedLine(zoom.get_right(),box.get_left(),color=RED),T('circles: swapped pairs',26,RED).move_to([3.85,-3,0]))
    return g

class S00Title(TitleCard):
    LESSON='The Wiring Problem: How a Brain Gets Built'
    TITLE='A Label Is Not a Wire'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,26,GREY),T(self.TITLE,50,font=TITLE_FONT),Line(LEFT,RIGHT,color=GOLD)).arrange(DOWN,buff=.45)
        self.play(FadeIn(g),run_time=.6);self.finish()

class S01(SpokenScene):
    def construct(self):
        l=leg();q=heading('How does a brain wire itself?',RED)
        self.add(q,l.copy().set_opacity(.28));self.at('Start with');self.play(FadeIn(l),run_time=.6);self.finish()

class S02(SpokenScene):
    def construct(self):
        l=leg();self.add(l,heading('One small circuit',TEAL))
        self.at('Tap the tendon');self.play(l[3].animate.rotate(.6,about_point=[2.4,1.9,0]).shift(LEFT*.15+DOWN*.05),run_time=.45)
        # Put hammer head in visible contact with the tendon.
        self.play(l[3].animate.shift(np.array([-.4,.28,0])-l[3][1].get_center()),run_time=.25)
        self.at('and the leg');self.play(Rotate(l[1],.8,about_point=[-.9,.9,0]),run_time=.5)
        self.wait(2.6);self.play(Rotate(l[1],-.8,about_point=[-.9,.9,0]),run_time=.5);self.finish()

class S03(SpokenScene):
    def construct(self):
        c=circuit();self.add(c[0],c[1]);self.at('A sensory neuron');self.play(FadeIn(c[2]),run_time=.7)
        self.at('excites');self.play(Create(c[3][1]),FadeIn(c[3][0],c[3][2],c[3][3],c[4]),run_time=.8);self.finish()

class S04(SpokenScene):
    def construct(self):
        c=circuit(True);self.add(*c[:6]);self.at('Through an inhibitory');self.play(FadeIn(c[6]),run_time=.8)
        self.at('it also quiets');self.play(c[6][-1].animate.scale(1.25),rate_func=there_and_back,run_time=.7);self.finish()

class S05(SpokenScene):
    def construct(self):
        c=circuit(True);self.add(c);self.at('The right partners');self.play(c[4].animate.scale(1.3),c[6][-1].animate.scale(1.3),rate_func=there_and_back,run_time=.8)
        self.at('Development built');self.play(FadeIn(heading('right partner · right sign',TEAL)),run_time=.4);self.finish()

class S06(SpokenScene):
    def construct(self):
        c=circuit(True);self.add(c);self.at('Now scale up');self.play(c.animate.scale(.006).move_to([-3.8,-.55,0]),run_time=1.2)
        self.at('A human brain');b=brain();self.play(FadeOut(c),FadeIn(b[0],b[1],b[3],b[4]),run_time=.5)
        self.at('has about');self.play(FadeIn(b[2]),FadeIn(counters(1)),run_time=.6);self.finish()

class S07(SpokenScene):
    def construct(self):
        self.add(brain(),counters(1));self.at('They are joined');self.play(FadeIn(counters(2)[1]),run_time=.6);self.finish()

class S08(SpokenScene):
    def construct(self):
        self.add(brain(),counters(2));self.at('The genome');self.play(FadeIn(genome_strip().move_to([3.1,-2.8,0])),run_time=.5)
        self.at('has about');self.play(FadeIn(counters(3)[2]),run_time=.5);self.finish()

class S09(SpokenScene):
    def construct(self):
        genome=genome_strip().move_to([3.1,-2.8,0]);self.add(genome,heading('Could the genome list the connections?',RED))
        scroll=VGroup(RoundedRectangle(width=4.2,height=5.4,corner_radius=.14,color=GREY,fill_opacity=.12),*[Line([-1.7,y,0],[1.7,y,0],color=GREY,stroke_width=2) for y in np.linspace(-2.35,2.35,20)]).move_to([3.2,-.3,0])
        self.at('Could the genome');self.play(genome.animate.move_to([-3.5,0,0]),GrowFromEdge(scroll,UP),FadeIn(T('wiring list',30).move_to([3.2,2.7,0])),run_time=1);self.finish()

class S10(SpokenScene):
    def construct(self):
        self.add(heading('Can the genome list every connection?'))
        sliver=Rectangle(width=.02,height=.85,color=BLUE,fill_opacity=1).move_to([0,1.2,0]);self.add(sliver,T('whole genome ≈ 6 × 10⁹ bits',30,BLUE).move_to([0,2.1,0]))
        scroll=VGroup(Rectangle(width=4.2,height=2.35,color=GREY,fill_opacity=.08),*[Line([-1.8,y,0],[1.8,y,0],color=GREY,stroke_width=2) for y in np.linspace(-1,1,10)]).move_to([0,-.6,0]);self.add(scroll)
        self.at('the list would');bar=Rectangle(width=12.3,height=1.0,color=GREY,fill_opacity=.35).move_to([0,-.4,0])
        arrows=VGroup(Arrow([-5.2,-.4,0],[-6.5,-.4,0],buff=0,color=GREY),Arrow([5.2,-.4,0],[6.5,-.4,0],buff=0,color=GREY))
        self.play(ReplacementTransform(scroll,bar),Create(arrows),FadeIn(T('wiring list ≈ 4 × 10¹⁵ bits',30).move_to([0,-1.35,0])),run_time=.65)
        self.at('a million times');self.play(FadeIn(chip('≈ 10⁶ times too big',RED,40).move_to([0,-2.7,0])),run_time=.4);self.finish()

class S11(SpokenScene):
    def construct(self):
        q=naming_question();self.add(q);self.at('So is');self.play(q[1].animate.scale(1.05),rate_func=there_and_back,run_time=.7);self.finish()

class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(naming_question());self.wait(5)

class S13(SpokenScene):
    def construct(self):
        switches=VGroup(*[toggle().scale(.65).move_to([-5.3+(i%10)*1.18,1.9-(i//10)*.72,0]) for i in range(37)])
        first_position=switches[0].copy();switches[0].scale(4).move_to([0,1,0])
        counter=M('2',70,BLUE).move_to([0,-1.7,0]);self.add(switches[0],counter,heading('One switch · two labels',BLUE))
        self.at('names are cheap');self.play(Transform(self.mobjects[2],heading('Names are cheap',BLUE)),run_time=.3)
        self.at('Each extra');self.play(Transform(switches[0],first_position),run_time=.25)
        for i in range(1,5):self.play(FadeIn(switches[i]),Transform(counter,M(f'{2**(i+1):,}',46,BLUE).move_to(counter)),run_time=.25)
        self.at('doubles the number');
        # All 37 switches are earned, with successive computed doublings.
        for i in range(5,37):self.play(FadeIn(switches[i]),Transform(counter,M(f'{2**(i+1):,}',46,BLUE).move_to(counter)),run_time=.067)
        self.play(FadeIn(T('2³⁷ labels · 37 switches',30,BLUE).move_to([0,-2.5,0])),FadeIn(VGroup(Line([-5,-3.05,0],[5,-3.05,0],color=GREY),T('86 billion — passed',28,TEAL).move_to([0,-3.5,0]))),run_time=.3);self.wait(3.3);self.finish()

class S14(SpokenScene):
    def construct(self):
        c=named_crowd();self.add(heading('Every neuron can have a distinct name',BLUE),VGroup(*[v[0] for v in c]));self.at('give every neuron');self.play(LaggedStart(*[FadeIn(v[1]) for v in c],lag_ratio=.035),run_time=1.25);self.finish()

class S15(SpokenScene):
    def construct(self):
        me=VGroup(cell(1.1),Square(side_length=.36,color=BLUE,fill_opacity=1).move_to([.8,-.5,0])).move_to([-4.8,0,0]);self.add(me,heading('A name identifies a cell',BLUE))
        cloud=VGroup(*[cell(.075,GREY).move_to([-.6+(i%20)*.34,2.15-(i//20)*.34,0]) for i in range(280)])
        self.add(cloud.copy().set_opacity(.25))
        self.at('It does not');lines=VGroup(*[DashedLine([-3.9,0,0],cloud[i].get_center(),color=GREY,stroke_width=1.5).set_opacity(.4) for i in range(0,280,19)])
        self.play(FadeIn(cloud),Create(lines),FadeIn(VGroup(chip('?  86 billion?',RED,36).move_to([2.6,0,0]),T('which partners?',32,RED).move_to([2.6,-3.1,0]))),run_time=.7);self.wait(3.1);self.finish()

class S16(SpokenScene):
    def construct(self):
        self.add(statement('A label is not a wire.',TEAL));self.finish()
class S17Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(statement('A label is not a wire.',TEAL));self.wait(1.5)

class S18(SpokenScene):
    def construct(self):
        g=VGroup(genome_strip().scale(1.7).move_to([0,.8,0]),Arrow([0,-.5,0],[0,-1.5,0],color=TEAL,buff=0,tip_length=.2),chip('rules',TEAL,40).move_to([0,-2.1,0]));self.add(g,heading('The genome stores rules',TEAL))
        self.at('The first');self.play(FadeOut(g),FadeIn(retina()),Transform(self.mobjects[1],heading('Rule 1 · graded labels',TEAL)),run_time=.6);self.finish()

class S19(SpokenScene):
    def construct(self):
        r=retina();self.add(r,heading('Rule 1 · graded labels',TEAL));blank=VGroup(Rectangle(width=6.5,height=5.2,color=GREY,fill_opacity=.03).move_to([2.75,0,0]),T('midbrain target',28,GREY).move_to([2.75,-3,0]));self.add(blank)
        self.at('Retinal ganglion cells');self.play(FadeIn(map_sources()),run_time=.6)
        self.at('carry a receptor');self.play(r[0].animate.set_opacity(.9),rate_func=there_and_back,run_time=.5);self.finish()

class S20(SpokenScene):
    def construct(self):
        self.add(retina(),map_sources(),heading('Rule 1 · graded labels',TEAL));self.at('Their target');self.play(FadeIn(target()),run_time=.6)
        self.at('opposing gradient');self.play(Create(Arrow([.1,-1.9,0],[5.6,-1.9,0],color=PURPLE,buff=0)),run_time=.5);self.finish()

class S21(SpokenScene):
    def construct(self):
        self.add(heading('Rule 2 · local rules',TEAL));trunk=Line([-6,0,0],[-1.5,0,0],color=YELLOW,stroke_width=9)
        tip=VGroup(Ellipse(width=3,height=3.5,color=YELLOW,fill_opacity=.2),*[path([[.7,y*.38,0],[1.6,y*.6,0],[2.1,y*.78,0]],YELLOW,4) for y in [-2,-1,0,1,2]]).move_to([.6,0,0]).scale(1.3);self.add(trunk,tip.copy().set_opacity(.25))
        self.at('Each growing tip');self.play(FadeIn(tip),run_time=.5)
        self.at('the growth cone');self.play(FadeIn(T('growth cone',30,YELLOW).move_to([.6,-2.95,0])),run_time=.4)
        self.at('reads only');cue=VGroup(*[Dot([x,y,0],radius=.075,color=PURPLE) for x,y in [(3.6,2.0),(3.8,.6),(3.9,-.6),(3.7,-2),(4.7,1.3),(4.8,-1)]])
        self.play(FadeIn(cue),Wiggle(tip),FadeIn(T('local ephrin-A cue',28,PURPLE).move_to([4.1,-3.5,0])),run_time=.8);self.finish()

class S22(SpokenScene):
    def construct(self):
        self.add(map_stage(),map_sources(),heading('Receptor level changes the response',TEAL));xs=np.linspace(.1,.9,5);cones=VGroup(*[cone([-.2,1.45-2.9*x,0]) for x in xs]);self.add(cones)
        self.at('Axons with more receptor');self.play(*[c.animate.shift(RIGHT*.4) for c in cones],run_time=.7)
        self.at('are kept away');
        # High-receptor tips recoil at high cue, then advance toward lower cue.
        self.play(*[c.animate.shift(LEFT*.4) for c in cones[3:]],run_time=.35)
        self.play(*[MoveAlongPath(c,path([[c.get_x(),c.get_y(),0],[.8,c.get_y()+.15,0],[-.5+6.5*x,c.get_y(),0]])) for c,x in zip(cones,xs)],run_time=1.25)
        self.play(FadeOut(cones),Create(ordered_axons()),run_time=.5);self.wait(3.1);self.finish()

class S23(SpokenScene):
    def construct(self):
        corner=T('toy model',26,TEAL).move_to([5.5,3.3,0]);ax=Axes(x_range=[0,1,.5],y_range=[0,4,1],x_length=9.4,y_length=5.2,tips=False,axis_config={'include_ticks':False}).move_to([-.1,-.2,0]);R=10**.6
        curve=ax.plot(lambda y:R*10**(-y),x_range=[0,1],color=ORANGE);threshold=Line(ax.c2p(0,1),ax.c2p(1,1),color=GREY)
        labels=VGroup(T('receptor × cue (product)',26).rotate(PI/2).move_to([-5.6,-.2,0]),T('position in target (high cue → low cue)',26).move_to([0,-3.15,0]),T('product for one axon',28,ORANGE).move_to([1.1,1.8,0]),Line([-.5,1.55,0],ax.c2p(.25,R*10**(-.25)),color=ORANGE,stroke_width=2))
        for v in [0,1,2,3,4]:labels.add(T(str(v),26).move_to(ax.c2p(-.045,v)))
        for v in [0,1]:labels.add(T(str(v),26).move_to(ax.c2p(v,-.24)))
        self.add(corner,ax,labels,curve)
        self.at('each axon settles');self.wait(.1)
        self.at('receptor times');self.play(FadeIn(M('receptor × cue = threshold',30).move_to([-.8,3.1,0])),Create(threshold),FadeIn(VGroup(T('threshold',28,GREY).move_to([5.1,-.9,0]),Line([4.8,-1.1,0],ax.c2p(.98,1),color=GREY,stroke_width=2))),FadeIn(Dot(ax.c2p(.6,1),color=YELLOW,radius=.12)),run_time=.5)
        self.at('That rule');stage=map_stage();a=ordered_axons();old=list(self.mobjects)
        # Replace the whole graph in one cut: no orphaned leader or ghost labels.
        self.remove(*old);self.add(stage,map_sources(),corner.copy())
        self.play(Create(a),run_time=.5)
        self.at('Real maps also');self.play(FadeIn(chip('competition + more cues',TEAL,28).move_to([1.2,3.25,0])),run_time=.4)
        tips=VGroup(*[cone(a[i][1].get_center()) for i in range(5)]);self.add(tips);self.play(tips[2].animate.shift(RIGHT*.55+DOWN*.25),tips[3].animate.shift(LEFT*.55+UP*.25),rate_func=there_and_back,run_time=.8);self.finish()

class S24(SpokenScene):
    def construct(self):
        initial=scatter_stage(False,False,False);self.add(*initial[:4]);dots=initial[4]
        self.at('Now take');self.play(LaggedStart(*[FadeIn(VGroup(*dots[i:i+40])) for i in range(0,200,40)],lag_ratio=.2),run_time=1.3)
        self.at('Suppose each reading');noisy=scatter_stage(True,False,False);self.play(FadeIn(noisy[5]),Transform(dots,noisy[4]),run_time=1.1)
        self.at('overall order stays high');final=scatter_stage();self.play(FadeIn(final[6]),run_time=.4)
        self.at('neighboring pairs');self.play(*[FadeIn(m) for m in final[8:]],run_time=.7)
        self.at('only about');self.play(FadeIn(final[7]),run_time=.4);self.finish()

class S25Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(scatter_stage());self.wait(2)

class S26(SpokenScene):
    def construct(self):
        self.add(rule_card(3,'overproduce, then select'));self.finish()

class S27(SpokenScene):
    def construct(self):
        b=branches();self.add(heading('Overproduce branches',TEAL),VGroup(*[VGroup(v[0],v[1]) for v in b]));self.at('Each axon branches');self.play(Create(VGroup(*[v[2] for v in b])),run_time=1.3);self.finish()

class S28(SpokenScene):
    def construct(self):
        cells=VGroup(*[cell(.58).move_to([-4.8+(i%4)*3.2,1.8-(i//4)*1.8,0]) for i in range(12)])
        self.add(heading('Neighbouring retinal cells',GREEN),cells,T('a wave of shared activity',30,GREEN).move_to([0,-3.15,0]))
        self.at('neighboring cells');self.play(LaggedStart(*[AnimationGroup(*[Flash(cells[i].get_center(),color=GREEN,flash_radius=.78) for i in [col,col+4,col+8]]) for col in range(4)],lag_ratio=.3),run_time=1.5)
        self.at('fire together');self.play(*[Indicate(cells[i],color=GREEN,scale_factor=1.3) for i in [2,6,10]],run_time=.9);self.finish()

class S29(SpokenScene):
    def construct(self):
        ys=[2, .7,-.6];sources=VGroup(*[cell(.3).move_to([-5.6,y,0]) for y in ys]);targets=VGroup(*[cell(.35,GREY).move_to([5,y,0]) for y in [1.1,0,-1.1]])
        lines=VGroup(*[path([[-5.3,y,0],[-1,y,0],[4.65,t,0]],YELLOW,4) for y in ys for t in [1.1,0,-1.1]])
        stranger=path([[-5.3,-2.3,0],[-1,-2.3,0],[4.65,0,0]],YELLOW,3)
        self.add(sources,targets,lines,stranger,cell(.3).move_to([-5.6,-2.3,0]),heading('Activity tests the connections',TEAL),T('target cells',28,GREY).move_to([5,-2.1,0]))
        self.at('fires in step');self.play(FadeIn(T('fires in step',28,GREEN).move_to([-3.8,2.7,0])),*[MoveAlongPath(Dot(radius=.09,color=GREEN),l,remover=True) for l in lines],run_time=.8)
        self.at('together they drive');self.play(*[Indicate(t,color=GREEN,scale_factor=1.4) for t in targets],run_time=.6)
        self.at('Such branches');self.play(lines.animate.set_stroke(GREEN,width=6),run_time=.5)
        self.at('Branches among strangers');self.play(FadeIn(T('out of step',28,RED).move_to([-3.8,-3.1,0])),MoveAlongPath(Dot(radius=.1,color=RED),stranger,remover=True),run_time=.7)
        self.at('tend to retract');short=path([[-5.3,-2.3,0],[-4.4,-2.3,0],[-3.6,-2.3,0]],RED,3);self.play(Transform(stranger,short),run_time=.65);self.play(FadeOut(stranger),run_time=.2);self.finish()

class S30(SpokenScene):
    def construct(self):
        b=branches(True).shift(UP*.5);self.add(b,heading('Connections form → tissue measures',GREEN))
        self.at('so the genome');g=genome_strip().move_to([-3.8,-2.8,0]);lst=VGroup(T('connection list',28,GREY),*[Line([-1.1,0,0],[1.1,0,0],color=GREY) for _ in range(3)]).arrange(DOWN,buff=.15).move_to([2.3,-2.65,0]);self.play(FadeIn(g,lst),run_time=.4)
        self.at('never has to');self.play(FadeIn(T('×',56,RED).move_to([4.6,-2.7,0])),run_time=.3);self.wait(3);self.finish()

class S31(SpokenScene):
    def construct(self):
        f=fish();self.add(f,heading('Goldfish · optic nerve regeneration',ORANGE));self.at('regrow a cut')
        gap=VGroup(Line([4,.7,0],[3,.7,0],color=YELLOW,stroke_width=6),Line([2,.7,0],[1,.7,0],color=YELLOW,stroke_width=6));cut=VGroup(Line([2.2,.35,0],[2.8,1.05,0],color=RED,stroke_width=4),Line([2.2,1.05,0],[2.8,.35,0],color=RED,stroke_width=4),T('cut',28,RED).move_to([2.5,1.6,0]));self.remove(f[4]);self.add(gap,cut);self.wait(.45)
        self.play(Create(Line([3,.7,0],[2,.7,0],color=YELLOW,stroke_width=6)),FadeOut(cut),run_time=.9);self.finish()

class S32(SpokenScene):
    def construct(self):
        f=fish().scale(.85).shift(UP*.55);self.add(f,heading('Block spikes during regrowth',RED));box=RoundedRectangle(width=8.9,height=1.3,corner_radius=.1,color=GREY).move_to([0,-2.25,0]);base=Line([-4,-2.45,0],[4,-2.45,0],color=GREEN,stroke_width=3)
        # Schematic event trace: Gaussian spike kernels at five firing times.
        tx=np.linspace(-4,4,1000);voltage=-2.45+.55*sum(np.exp(-((tx-event)/.045)**2) for event in [-3,-1.5,0,1.5,3])
        spikes=VMobject(color=GREEN,stroke_width=3).set_points_as_corners([np.array([x,v,0]) for x,v in zip(tx,voltage)])
        self.add(box,base,spikes,T('optic nerve recording (schematic)',28,GREY).move_to([0,-3.25,0]));self.at('Block every spike')
        eye=f[2].get_center();needle=VGroup(Line(eye+UP*.35,eye+UP*1.0+LEFT*.5,color=TEXT,stroke_width=3),Rectangle(width=.3,height=.65,color=RED,fill_opacity=.3).rotate(.6).move_to(eye+UP*1.3+LEFT*.65))
        self.play(FadeIn(needle),FadeOut(spikes),FadeIn(VGroup(Circle(radius=.47,color=RED,stroke_width=4).move_to(eye),chip('no spikes',RED,26).move_to([3.8,-.2,0]),Line(eye+DOWN*.45,[3.8,.12,0],color=RED))),run_time=.5)
        self.at('with tetrodotoxin');self.play(FadeIn(T('tetrodotoxin',28,RED).move_to([4.95,2.4,0])),run_time=.4)
        self.at('while the axons');self.play(f[4].animate.set_stroke(width=9),rate_func=there_and_back,run_time=.8);self.finish()

class S33(SpokenScene):
    def construct(self):
        q=test_question();self.add(q[0],q[3]);self.at('the rough order');self.play(FadeIn(q[1]),run_time=.4)
        self.at('or the fine');self.play(FadeIn(q[2]),run_time=.4);self.finish()

class S34Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(test_question());counter=T('Think · 5 seconds',30,TEAL).move_to([0,-2.3,0]);self.add(counter)
        for n in range(5,0,-1):
            counter.become(T(f'Think · {n} seconds',30,TEAL).move_to([0,-2.3,0]));self.wait(1)

class S35(SpokenScene):
    def construct(self):
        c=comparison();
        for v in c[1][1:]:
            v[2].set_opacity(0);v[1].put_start_and_end_on(v[1].get_start(),v[3].get_center())
        self.add(c[0],T('tetrodotoxin',28).move_to([3.3,2.9,0]));self.at('The axons still');self.play(FadeIn(VGroup(*c[1][1:])),run_time=.8)
        self.at('in roughly');self.play(FadeIn(T('same colour order',30,TEAL).move_to([0,-3.2,0])),run_time=.4);self.finish()

class S36(SpokenScene):
    def construct(self):
        c=comparison();
        for v in c[1][1:]:
            v[2].set_opacity(0);v[1].put_start_and_end_on(v[1].get_start(),v[3].get_center())
        self.add(c);self.at('their branches stayed');self.play(*[c[1][i][2].animate.set_opacity(1).set_stroke(width=3) for i in range(1,6)],run_time=.8)
        self.at('instead of clustering');self.play(FadeIn(chip('✓ rough order',TEAL,30).move_to([-3.3,-3.2,0])),FadeIn(chip('× fine precision',RED,30).move_to([3.3,-3.2,0])),run_time=.5);self.wait(2.5);self.finish()

class S37(SpokenScene):
    def construct(self):
        c=VGroup(panel(-3.3,False,'untreated goldfish',bottom=-1.65),panel(3.3,True,'tetrodotoxin',bottom=-1.65));self.add(c);a=T('cues → rough order\n(probably)',30,PURPLE).move_to([3.3,-2.85,0]);b=T('activity → sharp endings',30,GREEN).move_to([-3.3,-2.85,0]);self.at('Molecular cues');self.play(FadeIn(a),run_time=.4)
        self.at('Activity');self.play(FadeIn(b),run_time=.4);self.wait(3);self.finish()

class S38(SpokenScene):
    def construct(self):
        base=embryo_comparison(False);large=VGroup(heading('zebrafish embryo · first map',ORANGE))
        for x,title in [(-3.3,'untreated'),(3.3,'tetrodotoxin')]:
            large.add(embryo(x-.35,-.4,1.7),T(title,28).move_to([x,2.6,0]))
        self.add(large);stamp=chip('no spikes',RED,26).move_to([5.15,-2.5,0])
        self.at('block spikes');self.play(FadeIn(stamp),run_time=.4)
        self.at('The map formed');result=embryo_comparison();self.play(Transform(large,VGroup(*base[:-1])),Transform(stamp,base[-1]),FadeIn(result[-3],result[-2],result[-1]),run_time=.7)
        self.at('single arbors stayed');self.play(*[result[-2][i][2].animate.set_stroke(width=4) for i in range(1,6)],rate_func=there_and_back,run_time=.6);self.wait(2.2);self.finish()

class S39(SpokenScene):
    def construct(self):
        c=case_cards();self.add(c);self.at('these fish also');self.play(c[1].animate.scale(1.06),c[5].animate.scale(1.06),rate_func=there_and_back,run_time=.5)
        self.at('regrowing a map');self.play(c[2].animate.set_color(TEAL),run_time=.3)
        self.at('versus building');self.play(c[6].animate.set_color(TEAL),run_time=.3);self.finish()

class S40Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(case_cards());self.wait(2.5)

class S41(SpokenScene):
    def construct(self):
        a=T('The genome stores rules.',48,TEAL).move_to([0,1.8,0]);g=genome_strip().move_to([-3,-.3,0]);self.add(a,g)
        self.at('and the tissue');self.play(FadeIn(T('The tissue measures the rest.',44,GREEN).move_to([0,-2.3,0])),Create(Arrow([-1,-.3,0],[1,-.3,0],color=TEAL)),FadeIn(VGroup(*[cell(.3,GREEN).move_to([x,y,0]) for x,y in [(2,0),(3,-.6),(4,.4)]])),run_time=.6);self.wait(3.1);self.finish()

class S42(SpokenScene):
    def construct(self):
        self.add(heading('Three acts',TEAL),VGroup(*[Circle(radius=.75,color=TEAL,fill_opacity=.07).move_to([x,0,0]) for x in [-3.3,0,3.3]]));cards=[chip('1   where cells go',TEAL,40).move_to([0,1.7,0]),chip('2   how axons find their targets',TEAL,36).move_to([0,-.2,0]),chip('3   who survives',TEAL,40).move_to([0,-2.1,0])]
        self.at('where cells go');self.play(FadeOut(self.mobjects[1]),FadeIn(cards[0],shift=RIGHT*.2),run_time=.25)
        self.at('how axons');self.play(FadeIn(cards[1],shift=RIGHT*.2),run_time=.25)
        self.at('and who');self.play(FadeIn(cards[2],shift=RIGHT*.2),run_time=.25);self.wait(3.1);self.finish()

class S43End(EndCard):
    LINE='The genome stores rules, and the tissue measures the rest.'
    def construct(self):
        line=T(self.LINE,40,font=TITLE_FONT);fit(line,max_w=11.5)
        sub=T('biochemistrypedia.com',26,TEAL)
        group=VGroup(line,sub).arrange(DOWN,buff=.5);self.add(line)
        self.play(FadeIn(sub),run_time=.4);self.finish()

