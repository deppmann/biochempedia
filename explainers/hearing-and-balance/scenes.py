"""One Cell, One Switch — reviewer fix round.

COLOR MAP: TEAL hair cell; BLUE endolymph / cochlear wall / afferent circuits;
YELLOW potassium / sound / upper tip-link half; GOLD lower tip-link half;
GREEN open channels / increased response; RED decreased response;
PURPLE calcium; ORANGE sodium; GREY probes and neutral structure.
Curves: P(x)=1/(1+9 exp(-x)); V=(80*g_top-90*g_base)/(g_top+g_base).
The balance cartoon lets basal conductance vary qualitatively as
g_base=3.25+0.6*(g_top-1); it is not a fit to a particular hair cell.
The bundle is a schematic, not a census of the illustrative 10% open fraction.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'


def label(s, x=0, y=3.2, size=30, color=TEXT):
    return T(s, size=size, color=color).move_to([x,y,0])


def note(*lines):
    return VGroup(*[T(s,size=26,color=TEXT) for s in lines]).arrange(DOWN,buff=.13).move_to([0,-3.35,0])


class Timed(SpokenScene):
    # Same word synchronization as bp_style, without modifying its shared sync.log.
    def at(self, phrase, lead=.2, nth=0):
        delay=self.t_of(phrase,nth)-lead-self.elapsed()
        if delay>.02: self.wait(delay)


def bundle(lean=0, opened=2, links=True, channels=True):
    body=RoundedRectangle(width=3.7,height=1.7,corner_radius=.6,
        color=TEAL,fill_color=TEAL,fill_opacity=.17).move_to([-3.5,-1.85,0])
    rods,threads,gates=VGroup(),VGroup(),VGroup()
    tops=[]
    for i in range(6):
        x=-5.0+.57*i; h=1.45+.37*i
        top=np.array([x+lean*h,-1+h,0]); tops.append(top)
        rods.add(Line([x,-1,0],top,color=TEAL,stroke_width=15))
    for i in range(5):
        a=tops[i]; b=tops[i+1]+DOWN*.20
        mid=(a+b)/2+(DOWN*.18 if lean<0 else ORIGIN)
        # Separate threads terminate on the SIDE of each taller neighbour.
        threads.add(VGroup(Line(a,mid,color=GOLD,stroke_width=5),Line(mid,b,color=YELLOW,stroke_width=5)))
        gates.add(RoundedRectangle(width=.31,height=.23,corner_radius=.04,
            color=GREEN if i<opened else GREY,fill_color=GREEN if i<opened else BG,
            fill_opacity=1,stroke_width=3).move_to(a))
    return VGroup(body,rods,threads if links else VGroup(),gates if channels else VGroup())


def big_bundle(lean=0, opened=2, links=True, channels=True):
    return bundle(lean,opened,links,channels).shift(RIGHT*3.3)


def probe(side=1,lean=0):
    # Blunt probe ends exactly on an outer stereocilium, not in mid-air.
    if side==1:
        tip=np.array([-5+lean*1.45,.45,0]); start=tip+LEFT*1.0
    else:
        tip=np.array([-2.15+lean*3.3,2.3,0]); start=tip+RIGHT*1.0
    return VGroup(Line(start,tip,color=GREY,stroke_width=13),
        Line(tip+UP*.17,tip+DOWN*.17,color=TEXT,stroke_width=6))


def voltage(g): return (80*g-90*3.25)/(g+3.25)


def meter(g=1):
    # Inward current magnitude, normalized to g_top=10, from the voltage model.
    frac=g*(80-voltage(g))/(10*(80-voltage(10)))
    rest=1*(80-voltage(1))/(10*(80-voltage(10)))
    x=.35; bottom=-2.45; height=4.7
    box=Rectangle(width=.65,height=height,color=GREY).move_to([x,bottom+height/2,0])
    fill=Rectangle(width=.51,height=max(.03,height*frac),stroke_width=0,fill_color=GREEN,
        fill_opacity=.9).move_to([x,bottom+max(.03,height*frac)/2,0])
    return VGroup(box,fill,DashedLine([x-.55,bottom+height*rest,0],[x+.55,bottom+height*rest,0],color=YELLOW),
        label('current in',x,2.8,26),label('rest',x+.05,bottom+height*rest+.4,26,YELLOW),label('0',x,-2.85,26))


def voltage_trace(state=0):
    axes=Axes(x_range=[0,6,1],y_range=[-90,0,30],x_length=4.5,y_length=4.8,tips=False,
        axis_config={'include_ticks':False,'color':GREY}).move_to([3.85,-.1,0])
    # Retain the first response while appending the second response.
    vals=[(0,voltage(1)),(1,voltage(1))]
    if state>=1: vals += [(1,voltage(3)),(2.7,voltage(3))]
    if state>=2: vals += [(2.7,voltage(1)),(4,voltage(1))]
    if state>=3: vals += [(4,voltage(0)),(6,voltage(0))]
    line=VMobject().set_points_as_corners([axes.c2p(t,v) for t,v in vals]).set_stroke(TEAL,5)
    g=VGroup(axes,DashedLine(axes.c2p(0,-50),axes.c2p(6,-50),color=YELLOW,stroke_width=2),line,
        label('voltage (mV)',3.8,2.8,28),label('time →',3.85,-2.9,26))
    for v in [-90,-50,0]:
        g.add(label(str(v),1.18,axes.c2p(0,v)[1],26,YELLOW if v==-50 else TEXT))
    return g


def question_frame():
    return VGroup(bundle(),probe(-1),meter(),voltage_trace(2),
        label('What happens to the current?',0,3.45,32))


def cell():
    body=RoundedRectangle(width=2.4,height=3.4,corner_radius=.8,color=TEAL,
        fill_color=BG,fill_opacity=1,stroke_width=6).move_to([0,-1,0])
    rods=VGroup(*[Line([x,.7,0],[x,h,0],color=TEAL,stroke_width=13)
        for x,h in [(-.72,1.65),(0,2.15),(.72,2.65)]])
    links=VGroup(Line([-.72,1.65,0],[0,1.95,0],color=YELLOW,stroke_width=4),
        Line([0,2.15,0],[.72,2.45,0],color=YELLOW,stroke_width=4))
    return VGroup(body,rods,links)


def potassium(where):
    if where=='top':
        # Crowd the full panel, keeping text and flow callouts unobscured.
        pts=[(x,y) for x in np.arange(-5.9,6.0,.48)
             for y in np.arange(.95,3.21,.36)
             if not (abs(x)<1.5 or
                     (-5.8<x<-2.35 and 2.0<y<3.05) or
                     (2.0<x<5.9 and 2.4<y<3.05) or
                     (1.65<x<5.8 and 1.0<y<2.25))]
        pts += [(-.65,-.1),(.45,-.35),(-.6,-1.8),(.4,-2.1),(-.55,-2.25)]
    else: pts=[(-5,-2.1),(5.8,-1.85)]
    return VGroup(*[Dot([x,y,0],radius=.065,color=YELLOW) for x,y in pts])


def endo_sodium():
    return VGroup(*[Dot([x,y,0],radius=.065,color=ORANGE)
        for x,y in [(-5.5,1.5),(-2,2.85),(5.7,3.1)]])


def peri_key():
    return VGroup(label('low K⁺',-4.9,-1.02,27,YELLOW),
        label('high Na⁺',-3.1,-1.02,27,ORANGE))


def sodium():
    return VGroup(*[Dot([x,y,0],radius=.065,color=ORANGE)
        for x in [-5.8,-4.9,-4,-3.1,-2.2,2.2,3.1,4,4.9,5.8]
        for y in ([-1.5,-2.4] if x<0 else [-1.4,-2.05])])


def fluid_cell(endo=False,peri=False):
    upper=Rectangle(width=12.5,height=2.6,stroke_width=0,fill_color=BLUE,fill_opacity=.24).move_to([0,2,0])
    lower=Rectangle(width=12.5,height=3.5,stroke_width=0,fill_color=ORANGE,fill_opacity=.12).move_to([0,-1.05,0])
    wall=VGroup(Line([-6.25,.7,0],[-1.2,.7,0],color=BLUE,stroke_width=12),
        Line([1.2,.7,0],[6.25,.7,0],color=BLUE,stroke_width=12))
    g=VGroup(upper,lower,wall,cell(),label('endolymph',-4.1,2.75,30,BLUE),
        label('perilymph',-4.1,-.55,30,BLUE))
    if endo:g.add(VGroup(potassium('top'),endo_sodium()),label('K⁺-rich',-4.1,2.25,28,YELLOW))
    if peri:g.add(potassium('base'),sodium(),peri_key())
    return g


def top_flow():
    # Enter the tallest stereocilium at its tip; leave every rod visible.
    return Arrow([.72,3.5,0],[.72,2.65,0],buff=0,color=YELLOW,stroke_width=9,tip_length=.20,
        max_stroke_width_to_length_ratio=50,max_tip_length_to_length_ratio=.3)


def top_flow_label():
    return VGroup(label('K⁺ in',3.65,1.95,30,YELLOW),
        label('push about 130 mV',3.65,1.4,30,YELLOW),
        Line([2.0,2.13,0],[.86,3.0,0],color=YELLOW,stroke_width=3))


def top_gate():
    return RoundedRectangle(width=.26,height=.18,corner_radius=.04,color=GREEN,
        fill_color=GREEN,fill_opacity=1).move_to([.72,2.65,0])


def base_flow():
    return Arrow([.35,-1.8,0],[3.2,-1.8,0],buff=0,color=YELLOW,stroke_width=9,tip_length=.22)


def basal_gate():
    return RoundedRectangle(width=.44,height=.68,corner_radius=.08,color=YELLOW,
        fill_color=BG,fill_opacity=1,stroke_width=5).move_to([1.2,-1.8,0])


def basal_conductance(g): return 3.25 + .6*(g-1)


def balance_voltage(g):
    gb=basal_conductance(g)
    return (80*g-90*gb)/(g+gb)


def v_y(g): return -2.5+(balance_voltage(g)+90)/170*5.2


def voltage_stage(g=1,lower=False,upper=True):
    x=1.05; y=v_y(g)
    scale=VGroup(Line([x,-2.5,0],[x,2.7,0],color=GREY,stroke_width=5))
    for value in [-90,0,80]:
        yy=-2.5+(value+90)/170*5.2
        scale.add(Line([x-.15,yy,0],[x+.15,yy,0],color=GREY,stroke_width=4),
            label(f'{value:+d} mV' if value else '0 mV',-.05,yy,27))
    marker=Dot([x,y,0],radius=.17,color=TEAL)
    label_y=max(-1.15,y)
    marker_label=VGroup(label('cell voltage',4.25,label_y,28,TEAL),
        label(f'about {balance_voltage(g):.0f} mV',4.25,label_y-.48,28,TEAL))
    join=Line([x+.2,y,0],[2.75,label_y,0],color=TEAL,stroke_width=3)
    up=Arrow([1.7,y+.08,0],[1.7,2.7,0],buff=0,color=GREEN,stroke_width=5+3*g,tip_length=.2,max_stroke_width_to_length_ratio=50)
    # Keep the basal pull legible even near its equilibrium voltage.
    down=Arrow([2.4,max(y-.08,-1.55),0],[2.4,-2.5,0],buff=0,color=YELLOW,stroke_width=3+3*basal_conductance(g),tip_length=.2,max_stroke_width_to_length_ratio=100,max_tip_length_to_length_ratio=.35)
    gobj=VGroup(scale,marker,marker_label,join)
    if upper:gobj.add(up,label('transduction\nchannels',4.55,2.15,28,GREEN))
    if lower:gobj.add(down,label('basal K⁺\nchannels',4.55,-2.4,28,YELLOW))
    return gobj


class S00Title(TitleCard):
    LESSON='Hearing and Balance'
    TITLE='One Cell, One Switch'
    def construct(self):
        g=VGroup(label('BIOCHEMISTRYPEDIA',0,1.1,26,TEAL),label(self.LESSON.upper(),0,.5,28),
            label(self.TITLE,0,-.5,54)).add(Line([-1.2,-1.3,0],[1.2,-1.3,0],color=GOLD,stroke_width=4))
        self.add(g); self.finish()


def listener():
    # Human profile faces left, toward the source from the first frame.
    outline=VMobject().set_points_smoothly([[3.4,-1.4,0],[3.6,-.8,0],[4.2,-.1,0],[4.3,1,0],
        [3.8,1.9,0],[2.7,2.15,0],[1.9,1.55,0],[1.85,.9,0],[1.48,.35,0],
        [1.82,.2,0],[1.85,-.35,0],[2.45,-.65,0],[2.45,-1.4,0]]).set_stroke(TEXT,5)
    return VGroup(outline,Arc(radius=.26,start_angle=-PI/2,angle=PI*1.4,color=TEAL).move_to([3.3,.55,0]),
        Dot([2.06,1.0,0],radius=.06,color=TEXT),Line([2,-.12,0],[2.32,-.12,0],color=GREY),
        Line([1.6,-1.8,0],[4.8,-1.8,0],color=GREY,stroke_width=5))


def violin_icon():
    pts=[[-.45,-1.3,0],[-.85,-.9,0],[-.8,-.3,0],[-.4,.05,0],[-.65,.5,0],[-.55,.95,0],
         [0,1.12,0],[.55,.95,0],[.65,.5,0],[.4,.05,0],[.8,-.3,0],[.85,-.9,0],[.45,-1.3,0],[-.45,-1.3,0]]
    body=VMobject().set_points_smoothly(pts).set_stroke(YELLOW,5).set_fill(YELLOW,.16)
    neck=Rectangle(width=.22,height=1.3,color=YELLOW,fill_color=YELLOW,fill_opacity=.4).move_to([0,1.65,0])
    strings=VGroup(*[Line([x,-1.1,0],[x,2.25,0],color=TEXT,stroke_width=1.2) for x in [-.06,0,.06]])
    return VGroup(body,neck,strings).move_to([-4,0,0])


class S01Question(Timed):
    def construct(self):
        head=listener(); violin=violin_icon(); self.add(head)
        self.at('a violin'); self.play(FadeIn(violin),run_time=.4)
        waves=VGroup(*[Arc(radius=r,start_angle=-.45,angle=.9,color=YELLOW,stroke_width=4).shift(LEFT*3.3) for r in [1.2,1.7,2.2]])
        self.play(LaggedStart(*[Create(w) for w in waves],lag_ratio=.15),run_time=.7)
        self.at('your head'); self.play(VGroup(*head[:4]).animate.rotate(.10,about_point=[3,-1.4,0]),run_time=.65)
        # "How?" is in final TTS but omitted by the aligner: anchor to the preceding words.
        self.at('toward it'); self.wait(.72)
        self.play(FadeIn(label('One cell, hearing and balance?',0,-2.8,36,TEAL)),run_time=.25)
        self.finish()


class S02Bundle(Timed):
    def construct(self):
        head=listener(); self.add(head)
        ear_point=np.array([3.3,.55,0])
        ear=VGroup(Arc(radius=.75,start_angle=-PI/2,angle=PI*1.6,color=BLUE),
            Arc(radius=.4,start_angle=-PI/2,angle=PI*1.4,color=BLUE))
        self.at('On top')
        zoom=Circle(radius=.35,color=BLUE,stroke_width=6).move_to(ear_point)
        self.add(zoom)
        self.play(zoom.animate.scale(4),FadeOut(head),run_time=.35)
        cochlea=VMobject().set_points_smoothly([[.85*np.exp(-.13*t)*np.cos(t),
            .85*np.exp(-.13*t)*np.sin(t),0] for t in np.linspace(0,4*PI,100)]).set_stroke(BLUE,6)
        self.play(zoom.animate.move_to(ORIGIN),FadeIn(ear),FadeIn(cochlea),run_time=.25)
        self.wait(.25)
        b=big_bundle(links=False,channels=False)
        self.at('hair cell'); self.play(FadeOut(zoom),FadeOut(ear),ReplacementTransform(cochlea,b[0]),
            FadeIn(label('hair cell',3.5,-1.9,30,TEAL)),
            Create(Line([2.55,-1.9,0],[1.65,-1.9,0],color=TEAL)),run_time=.4)
        self.at('a bundle'); self.play(FadeIn(b[1][0]),FadeIn(label('hair bundle',-3.9,2.6,32,TEAL)),
            Create(Line([-2.7,2.4,0],[-1.7,.45,0],color=TEAL)),run_time=.4)
        self.at('stiff stereocilia'); self.play(FadeIn(label('stereocilia',3.9,1.4,30,TEAL)),run_time=.35)
        self.at('graded in height')
        self.play(LaggedStart(*[Create(rod) for rod in list(b[1])[1:]],lag_ratio=.3),
            Create(Line([2.6,1.4,0],[1.15,2.0,0],color=TEAL)),run_time=1.1)
        self.finish()


class S03Links(Timed):
    def construct(self):
        b=bundle(links=False,channels=False); self.add(b)
        self.at('tip links'); self.play(FadeIn(bundle(channels=False)[2]),run_time=.4)
        # Large isolated cartoon of ONE two-part thread, with leaders to each half.
        a=np.array([.7,-1.4,0]); mid=np.array([2.6,.15,0]); z=np.array([4.5,1.7,0])
        inset=VGroup(Line(a,mid,color=GOLD,stroke_width=10),Line(mid,z,color=YELLOW,stroke_width=10),
            label('tip link',2.7,2.8,34,YELLOW),label('protocadherin 15',2.4,-2.25,28,GOLD),
            label('cadherin 23',4.5,.05,28,YELLOW),
            Line([1.7,-.55,0],[2.0,-1.95,0],color=GOLD),Line([3.65,1.0,0],[4.4,.4,0],color=YELLOW))
        self.at('each shorter'); self.play(FadeIn(inset),run_time=.45)
        self.finish()


class S04Rest(Timed):
    def construct(self):
        enlarge=lambda b:b.scale(1.16).move_to([-3.65,.1,0])
        b=enlarge(bundle(channels=False)); self.add(b,label('At rest',0,3.3,36))
        self.at('some tension'); self.play(Indicate(b[2],color=YELLOW,scale_factor=1.05),run_time=.5)
        self.at('some channels'); self.play(Transform(b,enlarge(bundle())),run_time=.5)
        self.at('already open'); self.play(FadeIn(label('some open at rest',3.2,1.5,32,GREEN)),run_time=.45)
        self.at('only a few'); self.play(FadeIn(VGroup(label('This example: a few open',3.2,.2,28),
            label('Outer hair cells:',3.2,-1,28),label('nearer half',3.2,-1.55,28))),run_time=.4)
        self.finish()


class S05Toward(Timed):
    def construct(self):
        b=bundle(); m=meter(); v=voltage_trace(); p=probe(); self.add(b,m,v)
        self.at('Push the bundle'); self.play(FadeIn(p),run_time=.35)
        self.at('toward its tallest'); self.play(Transform(b,bundle(.27)),Transform(p,probe(1,.27)),run_time=.65)
        self.at('The links'); self.play(Indicate(b[2],color=YELLOW,scale_factor=1.05),run_time=.45)
        self.at('more channels open'); self.play(Transform(b,bundle(.27,5)),Transform(m,meter(3)),run_time=.5)
        self.at('the cell depolarizes'); self.play(Transform(v,voltage_trace(1)),FadeIn(label('depolarizes',-3.5,3.35,32,GREEN)),run_time=.6)
        self.finish()


class S06Predict(Timed):
    def construct(self):
        b=bundle(.27,5); p=probe(1,.27); m=meter(3); v=voltage_trace(1); self.add(b,p,m,v)
        self.at('Now push'); self.play(Transform(b,bundle()),Transform(p,probe(-1)),Transform(m,meter()),Transform(v,voltage_trace(2)),run_time=.8)
        self.at('What happens'); self.play(FadeIn(label('What happens to the current?',0,3.45,32)),run_time=.4)
        self.finish()


class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question_frame(),label('Think…',-3.5,-3.35,28,GOLD)); self.wait(5)


class S08Reveal(Timed):
    def construct(self):
        f=question_frame(); self.add(f)
        self.at('The few channels'); self.play(FadeOut(f[4]),run_time=.3)
        self.at('at rest close'); self.play(Transform(f[0],bundle(-.24,0)),Transform(f[1],probe(-1,-.24)),run_time=.6)
        self.at('less current'); self.play(Transform(f[2],meter(0)),run_time=.4)
        self.at('the cell hyperpolarizes'); self.play(Transform(f[3],voltage_trace(3)),FadeIn(label('hyperpolarizes',-3.5,3.35,32,RED)),
            FadeIn(label('bounded by the K⁺ floor',3.8,-3.48,25,YELLOW)),run_time=.5)
        self.finish()


class S09Lopsided(Timed):
    def construct(self):
        axes=Axes(x_range=[-3,5,1],y_range=[0,1,.2],x_length=10.6,y_length=4.9,tips=False,
            axis_config={'include_ticks':False,'color':GREY}).move_to([.25,.55,0])
        p=lambda x:1/(1+9*np.exp(-x))
        curve=axes.plot(p,x_range=[-3,5,.025],color=TEAL,stroke_width=6,use_smoothing=False)
        names=VGroup(label('transduction conductance / maximum',0,3.35,29),
            label('0',-5.45,-1.9,26),label('1',-5.45,3.0,26),
            label('away',-4.3,-2.42,26),label('bundle displacement',0,-2.42,26),label('toward',4.8,-2.42,26))
        self.add(axes,names,curve,note('Illustrative: small resting open fraction', 'Voltage also depends on other conductances'))
        rest=Dot(axes.c2p(0,.1),radius=.10,color=YELLOW)
        self.at('less room to reduce')
        down=Arrow(axes.c2p(-1.5,.1),axes.c2p(-1.5,0),buff=0,color=RED,stroke_width=13,tip_length=.18,max_tip_length_to_length_ratio=.4,max_stroke_width_to_length_ratio=50)
        self.play(FadeIn(rest),Create(DashedLine(axes.c2p(-3,.1),axes.c2p(5,.1),color=YELLOW)),GrowArrow(down),
            FadeIn(label('rest',-.4,-.95,27,YELLOW)),FadeIn(label('can only close\nwhat is open',-2.2,-.65,28,RED)),run_time=.65)
        self.at('than to increase'); self.play(GrowArrow(Arrow(axes.c2p(3.6,.1),axes.c2p(3.6,1),buff=0,color=GREEN,stroke_width=8)),
            FadeIn(label('more can open',2.2,1.0,28,GREEN)),run_time=.65)
        self.finish()


class S10Fluids(Timed):
    def construct(self):
        c=cell(); self.add(c,label('What carries the current?',0,3.55,32))
        self.at('two ends'); self.play(ReplacementTransform(c,fluid_cell()),run_time=.65)
        self.finish()


class S11Endo(Timed):
    def construct(self):
        self.add(fluid_cell())
        self.at('The top'); self.play(Indicate(self.mobjects[0][0],color=BLUE,scale_factor=1),run_time=.4)
        dots=VGroup(potassium('top'),endo_sodium())
        self.at('rich in potassium'); self.play(FadeIn(dots),FadeIn(label('K⁺-rich',-4.1,2.25,28,YELLOW)),run_time=.4)
        # Gentle diffusion, not a net flux before the channels are discussed.
        dots.add_updater(lambda m,dt: m.shift(UP*(.025*np.sin(self.elapsed()*3)*dt)))
        self.at('in the cochlea'); self.play(FadeIn(label('about +80 mV',4.1,2.7,32,BLUE)),
            FadeIn(note('Endocochlear potential', 'Made by the cochlea’s wall')),run_time=.4)
        self.finish()


class S12Peri(Timed):
    def construct(self):
        self.add(fluid_cell(True),label('about +80 mV',4.1,2.7,32,BLUE))
        self.at('The base faces'); self.play(FadeIn(potassium('base')),FadeIn(sodium()),run_time=.4)
        self.at('low in potassium'); self.play(FadeIn(peri_key()),run_time=.4)
        self.finish()


class S13In(Timed):
    def construct(self):
        self.add(fluid_cell(True,True),label('+80 mV',4.1,2.7,32,BLUE))
        self.at('the inside'); self.play(FadeIn(label('−50 mV',0,-1.2,28,TEAL)),run_time=.4)
        self.at('far more negative'); self.play(FadeIn(note('Illustrative voltages; both against perilymph')),run_time=.4)
        self.at('potassium is pushed'); self.play(GrowArrow(top_flow()),FadeIn(top_gate()),
            FadeIn(top_flow_label()),run_time=.5)
        self.finish()


class S14Out(Timed):
    def construct(self):
        self.add(fluid_cell(True,True),top_flow(),top_gate(),top_flow_label())
        self.at('Across the base'); self.play(FadeIn(basal_gate()),run_time=.4)
        self.at('leaves through'); self.play(GrowArrow(base_flow()),FadeIn(label('K⁺ channels',3.9,-1.05,28,YELLOW)),
            FadeIn(label('K⁺ out · 40 mV',3.9,-2.45,30,YELLOW)),run_time=.5)
        self.at('In this steady picture'); self.play(FadeIn(note('Steady K⁺-dominated two-current approximation',
            '130 mV top / 40 mV base → about 3× basal conductance')),run_time=.4)
        self.finish()


class S15Battery(Timed):
    def construct(self):
        fluids=fluid_cell(True,True)
        # Give the wall battery its own cleared callout area.
        dots=fluids[6][0]
        for d in list(dots):
            if -5.9<d.get_x()<-2.3 and d.get_y()<1.85: dots.remove(d)
        self.add(fluids,top_flow(),top_gate(),basal_gate(),base_flow())
        path=VMobject().set_points_as_corners([[.72,3.5,0],[.72,2.65,0],[0,.7,0],[.35,-1.8,0],[3.2,-1.8,0]])
        particles=VGroup(*[Dot(radius=.10,color=YELLOW) for _ in range(9)])
        phase=ValueTracker(0)
        for i,d in enumerate(particles):
            d.add_updater(lambda m,i=i: m.move_to(path.point_from_proportion((phase.get_value()+i/9)%1)))
        self.at('potassium runs downhill'); self.add(particles)
        # Continue the stream through the battery reveal and the final hold.
        phase.add_updater(lambda m,dt:m.increment_value(dt*.35)); self.add(phase)
        battery=VGroup(Rectangle(width=1.4,height=1.3,color=BLUE,fill_color=BG,fill_opacity=1).move_to([-4.1,.7,0]),
            Line([-4.4,.2,0],[-4.4,1.2,0],color=BLUE,stroke_width=7),
            Line([-3.9,.4,0],[-3.9,1,0],color=BLUE,stroke_width=10))
        self.at('The battery'); self.play(FadeIn(battery),run_time=.45)
        self.at('in the wall'); self.play(FadeIn(label('battery in the wall',-4.1,1.62,25,BLUE)),
            Create(Line([-4.1,1.4,0],[-4.1,1.05,0],color=BLUE)),run_time=.4)
        self.finish()


class S16Balance(Timed):
    def construct(self):
        b=bundle(channels=False).scale(1.16).move_to([-3.65,.1,0]); stage=voltage_stage()
        self.add(b,*stage[:4],note('Steady two-conductance cartoon; no injected or other current'))
        self.at('voltage settles'); self.play(Indicate(stage[1],color=TEAL),run_time=.5)
        self.at('Open transduction channels'); self.play(GrowArrow(stage[4]),FadeIn(stage[5]),run_time=.6)
        self.finish()


class S17Slide(Timed):
    def construct(self):
        enlarge=lambda b:b.scale(1.16).move_to([-3.65,.1,0])
        b=enlarge(bundle()); stage=voltage_stage(lower=True); self.add(b,*stage[:6],
            note('Steady state; qualitative; no injected or other current', 'Real basal conductances vary with voltage'))
        self.at('Basal potassium channels'); self.play(GrowArrow(stage[6]),FadeIn(stage[7]),run_time=.55)
        # Regroup the same objects before moving; never morph text into a new rope.
        self.remove(*stage); self.add(stage)
        self.at('Moving the bundle'); self.play(Transform(b,enlarge(bundle(.28,5))),Transform(stage,voltage_stage(3,True)),run_time=1.05)
        self.at('top pull directly'); self.play(Transform(b,enlarge(bundle(-.24,0))),Transform(stage,voltage_stage(.08,True)),run_time=.85)
        self.wait(2.1); self.finish()


class S18Release(Timed):
    def construct(self):
        body=RoundedRectangle(width=10.8,height=3.25,corner_radius=.45,color=TEAL,
            fill_color=TEAL,fill_opacity=.16).move_to([0,1.45,0])
        nerve=RoundedRectangle(width=10.8,height=1.1,corner_radius=.35,color=BLUE,
            fill_color=BLUE,fill_opacity=.22).move_to([0,-2.1,0])
        gates=VGroup(*[RoundedRectangle(width=.65,height=.28,corner_radius=.05,color=GREY,
            fill_color=BG,fill_opacity=1,stroke_width=4).move_to([x,-.18,0]) for x in [-2,2]])
        ribbon=RoundedRectangle(width=.42,height=1.4,corner_radius=.1,color=GREY,
            fill_color=GREY,fill_opacity=.6).move_to([0,.7,0])
        vesicles=VGroup(*[Circle(radius=.22,color=TEAL,fill_color=TEAL,fill_opacity=.3).move_to([x,y,0])
            for x,y in [(-.6,1.3),(.6,1.3),(-.6,.7),(.6,.7)]])
        labels=VGroup(label('hair cell',-3.8,2.55,32,TEAL),label('vesicles',2.7,1.4,28,TEAL),
            Line([1.6,1.4,0],[.85,1.3,0],color=TEAL),label('ribbon synapse',-3.8,1,28),
            Line([-2.3,1,0],[-.25,1,0],color=GREY),label('afferent fibre',0,-2.1,30,BLUE))
        self.add(body,nerve,gates,ribbon,vesicles,labels,
            note('Mature cochlear hair cell, graded release;', 'spikes start in the nerve fibre'))
        self.at('Depolarization'); self.play(body.animate.set_stroke(GREEN),FadeIn(label('depolarization',0,2.55,28,GREEN)),run_time=.5)
        self.at('opens calcium channels'); self.play(gates.animate.set_color(PURPLE),
            FadeIn(label('Ca²⁺ channels',3.6,-.95,28,PURPLE)),Create(Line([2.5,-.8,0],[2.15,-.35,0],color=PURPLE)),run_time=.5)
        ca=VGroup(*[Dot([x,-.9-j*.28,0],radius=.11,color=PURPLE) for x in [-2,2] for j in range(3)])
        self.at('calcium entry'); self.add(ca); self.play(ca.animate.shift(UP*1.65),run_time=.65)
        self.at('transmitter release'); self.play(*[v.animate.move_to([(-.28 if i%2==0 else .28),-.12,0]) for i,v in enumerate(vesicles)],run_time=.45)
        tx=VGroup(*[Dot([x,-.35,0],radius=.12,color=TEAL) for x in [-.65,-.4,-.15,.15,.4,.65]])
        self.play(FadeOut(vesicles),FadeOut(labels[1]),FadeOut(labels[2]),FadeIn(tx),
            FadeIn(label('transmitter',-3.6,-.95,28,TEAL)),run_time=.2)
        self.play(tx.animate.shift(DOWN*.9),run_time=.45)
        self.wait(2.1); self.finish()


def idea_card(lean=0):
    length=.55+5.5*abs(lean)
    b=bundle(lean,channels=False).scale(1.10).move_to([0,0,0])
    return VGroup(b,label('A hair cell’s first response reports',0,3.25,34,TEAL),
        label('which way',-4.3,1.35,30),label('how far',4.3,1.35,30),
        DoubleArrow([-5.4,.5,0],[-3.2,.5,0],buff=0,color=TEAL),
        DoubleArrow([3.2,.5,0],[3.2+length,.5,0],buff=0,color=TEAL),
        Line([3.2,.25,0],[3.2,.75,0],color=TEAL),Line([3.2+length,.25,0],[3.2+length,.75,0],color=TEAL),
        note('Initial response; adaptation and membrane dynamics', 'shape it over time'))


class S19Idea(Timed):
    def construct(self):
        c=idea_card(); self.add(c)
        self.at('which way'); self.play(Transform(c[0],idea_card(.24)[0]),Indicate(c[4]),run_time=.65)
        self.at('how far'); target=idea_card(-.12)
        self.play(Transform(c[0],target[0]),*[Transform(c[i],target[i]) for i in range(5,8)],run_time=.65)
        self.at('its bundle'); target=idea_card(-.28)
        self.play(Transform(c[0],target[0]),*[Transform(c[i],target[i]) for i in range(5,8)],run_time=.55)
        self.finish()


class S20Takeaway(Timed):
    def construct(self):
        self.add(idea_card(-.28))
        self.at('what pushes'); self.play(FadeIn(label('mechanics',-4.4,-.9,30,YELLOW)),
            FadeIn(label('what pushes\nwhich bundle',-4.4,-1.75,26,YELLOW)),
            GrowArrow(Arrow([-3,-.8,0],[-1.7,-.8,0],buff=0,color=YELLOW)),run_time=.5)
        self.at('the circuits'); self.play(FadeIn(label('circuits',4.4,-.9,30,BLUE)),
            FadeIn(label('where · when\nwhich side',4.4,-1.75,26,BLUE)),
            GrowArrow(Arrow([1.7,-.8,0],[3,-.8,0],buff=0,color=BLUE)),run_time=.5)
        self.wait(2.1); self.finish()


class S21End(EndCard):
    LINE="A hair cell's first response reports which way, and how far, its bundle is pushed."
    def construct(self):
        # FIXES.md explicitly replaces the older twelve-word house-rule ending.
        self.add(label('A hair cell’s first response reports',0,1.3,38,TEAL),
            label('which way, and how far,',0,.25,42),label('its bundle is pushed.',0,-.8,42),
            label('biochemistrypedia.com',0,-2.35,28,TEAL))
        self.finish()
