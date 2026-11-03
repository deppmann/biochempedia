"""Chapter 3: A Brief Current That Holds a Press.
COLOR MAP (from scenes.old.py; shared across the series):
ORANGE Merkel cell; PURPLE SA1 ending/fibre; BLUE Piezo2/cell current;
YELLOW spikes; GREEN depolarizing light/steady charge; RED loss;
TEAL candidate transmitter; GOLD caution/transient charge; GREY axes/held touch.
CHAPTERS.md is left unchanged because TASK.md limits source edits to scenes.py.
Curves: I=20+350 exp(-t/8) pA, t in ms, reused from scenes.old.py.
Raster helper and cell geometry also reuse that reference. Model rasters are
computed with a fixed-threshold/reset leaky integrate-and-fire model, never data.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
ORANGE = '#F29E4C'


def label(s, y=3.1, color=TEXT, size=30):
    return T(s, size, color).move_to([0, y, 0])


def cell(cx=0, cy=0, s=1):
    return RoundedRectangle(corner_radius=.55*s, width=2*s, height=1.7*s,
        stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE,
        fill_opacity=.22).move_to([cx,cy,0])


def ticks(ts, y, x0=-5.5, x1=5.5, end=1, h=.7):
    return VGroup(*[Line([x0+(x1-x0)*t/end,y-h/2,0],
        [x0+(x1-x0)*t/end,y+h/2,0],color=YELLOW,stroke_width=4) for t in ts if 0<t<end])


def spike_times():
    # The seeded gamma interval model from the earlier film's hold raster.
    rng=np.random.default_rng(7)
    return np.cumsum(.12+rng.gamma(1.2,.5,20))


def lif(random=False):
    # Dimensionless passive membrane: dv/dt=-v+drive; threshold 1, reset 0.
    # Constant suprathreshold drive=2, or Poisson packets of variable amplitude.
    rng=np.random.default_rng(17); dt=.001; v=0.; out=[]
    for t in np.arange(0,10,dt):
        v += dt*(-v+(0 if random else 2))
        if random and rng.random()<4*dt: v+=rng.uniform(.4,1.3)
        if v>=1: out.append(t); v=0
    return out


def current(t): return 20+350*np.exp(-np.asarray(t)/8)


def trace(t0=0,t1=40,x0=-5.25,x1=5.6,y0=-1.8,height=4):
    pts=[[x0+(x1-x0)*t/80,y0+height*current(t)/400,0] for t in np.linspace(t0,t1,240)]
    return VMobject(color=BLUE,stroke_width=5).set_points_as_corners(pts)


def plot_base():
    axes=VGroup(Line([-5.25,-1.8,0],[5.6,-1.8,0],color=GREY),
        Line([-5.25,-1.8,0],[-5.25,2.4,0],color=GREY))
    labs=VGroup(T('current (pA)',26).move_to([-4.3,2.75,0]),
        T('time since press onset (ms)',26).move_to([2.7,-2.65,0]),
        *[T(str(v),26).move_to([-5.25+10.85*v/80,-2.15,0]) for v in (0,40,80)])
    # The 20 pA tick is close to zero; displace its text and use a leader.
    for v,yy in [(0,-1.96),(20,-1.25),(370,1.9)]:
        y=-1.8+4*v/400
        axes.add(Line([-5.4,y,0],[-5.25,y,0],color=TEXT))
        labs.add(T(str(v),26).move_to([-5.95,yy,0]))
        if v==20: axes.add(Line([-5.65,yy,0],[-5.4,y,0],color=TEXT))
    return VGroup(axes,labs)


def settled():
    dash=DashedVMobject(trace(40,80),num_dashes=32)
    tau=8; yy=-1.8+4*current(tau)/400; xx=-5.25+10.85*tau/80
    nums=VGroup(T('370 pA peak',26,BLUE).move_to([-2.8,2.15,0]),
        T('20 pA steady',26,BLUE).move_to([3.7,-1.15,0]),
        T('time constant: 8 ms',26).move_to([1.4,1.4,0]),
        VMobject(color=TEXT).set_points_as_corners([[-.3,1.15,0],[xx,1.15,0],[xx,yy,0]]),Dot([xx,yy,0],radius=.07,color=TEXT),
        T('dashed: assumed to continue',26,GOLD).move_to([0,-3.2,0]))
    return VGroup(plot_base(),trace(),dash,nums)


# The 1 s overview preserves a linear time axis; an onset inset resolves the peak.
CP=lambda t,i: [-4.9+10.4*t/1000,-.35+3.0*i/400,0]

def charge_areas(limit=1000):
    ts=np.unique(np.r_[np.linspace(0,min(80,limit),160),np.linspace(min(80,limit),limit,90)])
    return VGroup(
        Polygon(CP(0,0),CP(limit,0),CP(limit,20),CP(0,20),color=GREEN,fill_opacity=.7,stroke_width=0),
        Polygon(CP(0,20),*[CP(t,current(t)) for t in ts],CP(limit,20),color=GOLD,fill_opacity=.7,stroke_width=0))


def charge_stage(question=True):
    note=label('Thought experiment: plateau assumed to last 1 s',3.4,GOLD,26)
    axes=VGroup(Line(CP(0,0),CP(1000,0),color=GREY),Line(CP(0,0),CP(0,400),color=GREY))
    axis=VGroup(label('time since press onset, 0 to 1 s',-.9,TEXT,26))
    for v,yy in [(0,-.4),(20,.4),(370,2.4)]:
        axes.add(Line(np.array(CP(0,v))+LEFT*.12,CP(0,v),color=TEXT))
        axis.add(T(str(v),26).move_to([-5.65,yy,0]))
        if v==20: axes.add(Line([-5.35,.3,0],CP(0,20),color=TEXT))
    axis.add(T('pA',26).move_to([-5.7,2.95,0]))
    ts=np.unique(np.r_[np.linspace(0,80,250),np.linspace(80,1000,100)])
    curve=VMobject(color=BLUE,stroke_width=4).set_points_as_corners([CP(t,current(t)) for t in ts])
    # Onset magnification, explicitly labelled; every point is from I(t).
    ip=lambda t,i: [-2.7+3.4*t/60,1.1+1.45*i/400,0]
    inset=VGroup(Rectangle(width=4.1,height=2.15,color=GREY,fill_color=BG,fill_opacity=1).move_to([-1,1.92,0]),
        T('onset: 0–60 ms',26).move_to([-1,2.7,0]),
        Polygon(ip(0,0),ip(60,0),ip(60,20),ip(0,20),fill_color=GREEN,fill_opacity=.7,stroke_width=0),
        Polygon(ip(0,20),*[ip(t,current(t)) for t in np.linspace(0,60,180)],ip(60,20),fill_color=GOLD,fill_opacity=.7,stroke_width=0),
        VMobject(color=BLUE,stroke_width=3).set_points_as_corners([ip(t,current(t)) for t in np.linspace(0,60,180)]))
    names=VGroup(); bars=VGroup()
    for y,name,c in [(-1.65,'Transient excess',GOLD),(-2.4,'Steady',GREEN)]:
        names.add(T(name,26,c).move_to([-3.85,y,0]))
        bars.add(Rectangle(width=4.8,height=.55,stroke_color=c,fill_opacity=0).move_to([1,y,0]))
    names.add(T('full bar\n= 20 pC',26).move_to([4.8,-2.0,0]))
    q=label('Which part brings in more charge?',-3.3,TEXT,30)
    timer=M('0.00 s',28).move_to([4.2,2.95,0])
    return VGroup(note,axes,charge_areas(),curve,axis,inset,names,bars,q if question else VGroup(),timer)


def charge_fills(t):
    out=VGroup()
    for y,q,c in [(-1.65,2.8*(1-np.exp(-t/8)),GOLD),(-2.4,20*t/1000,GREEN)]:
        w=max(.00001,4.8*q/20)
        out.add(Rectangle(width=w,height=.55,stroke_width=0,fill_color=c,fill_opacity=.8).move_to([-1.4+w/2,y,0]))
    return out


def lif_detail(random=False):
    rng=np.random.default_rng(17); dt=.001; v=0.; pts=[]; spikes=[]; packets=[]
    for t in np.arange(0,10,dt):
        v+=dt*(-v+(0 if random else 2))
        if random and rng.random()<4*dt:
            amp=rng.uniform(.4,1.3); v+=amp; packets.append((t,amp))
        if v>=1:
            pts.append((t,1)); spikes.append(t); v=0
        pts.append((t,v))
    return pts,spikes,packets


def model_voltage(random=False,y=1.25,x0=-5.5,x1=5.5):
    pts,spikes,packets=lif_detail(random)
    p=lambda t,v:[x0+(x1-x0)*t/10,y+.7*v,0]
    curve=VMobject(color=TEAL if random else BLUE,stroke_width=2.5).set_points_as_corners([p(t,v) for t,v in pts])
    threshold=DashedLine(p(0,1),p(10,1),color=TEXT,dash_length=.12)
    return VGroup(threshold,curve)


def model_stage(question=True,regular=True):
    title=label('Schematic integrate-and-fire model outputs',3.35,TEXT,28)
    rule=label('Noise-free • fixed threshold • reset',2.8,TEXT,26)
    lines=VGroup(*[Line([-5.5,y,0],[5.5,y,0],color=GREY) for y in (.55,-1.8)])
    labs=VGroup(label('Steady current above threshold',2.35,BLUE,26),label('Random packets of transmitter',-.55,TEAL,26))
    reg=VGroup(model_voltage(),ticks(lif(),.55,end=10,h=.65)) if regular else VGroup()
    q=label('What could randomly timed packets do?',-3.1,TEXT,28) if question else VGroup()
    # Blank packet and voltage tracks deliberately hold the prediction back.
    blank=VGroup(DashedLine([-5.5,-1.05,0],[5.5,-1.05,0],color=TEAL),
        T('packet / voltage track: predict',26).move_to([0,-2.5,0]))
    return VGroup(title,rule,lines,labs,reg,q,blank)


def contact():
    a=cell(0,1.45,1.4)
    b=RoundedRectangle(width=5.8,height=.65,corner_radius=.15,stroke_color=PURPLE,
        fill_color=PURPLE,fill_opacity=.3).move_to([0,-1.4,0])
    labs=VGroup(T('Merkel cell',28,ORANGE).move_to([0,3.1,0]),T('afferent ending',28,PURPLE).move_to([0,-2.5,0]))
    return VGroup(a,b,labs)


def accounts(which=2):
    g=VGroup()
    for x,tag,name,receptor in [(-3.25,'mouse touch domes','noradrenaline','beta-2 (β2)'),(3.25,'rodent whiskers','protons','ASIC3')][:which]:
        a=cell(x,1.6,.8).stretch_to_fit_width(4.6)
        b=Rectangle(width=4.6,height=.7,stroke_color=PURPLE,fill_color=PURPLE,fill_opacity=.3).move_to([x,-1.35,0])
        rec=chip(receptor,PURPLE,26).move_to([x,-1.35,0]); rec[1].set_color(TEXT)
        ar=VGroup(DashedLine([x,.85,0],[x,rec.get_top()[1]+.14,0],color=TEAL,dash_length=.13),
            Triangle(color=TEAL,fill_color=TEAL,fill_opacity=1).scale(.1).rotate(PI).move_to([x,rec.get_top()[1]+.12,0]))
        tx=VGroup(T(tag,30).move_to([x,2.95,0]),T(name,26,TEAL).move_to([x+1.25,.35,0]),rec,
            T('proposed account',26,GOLD).move_to([x,-2.15,0]))
        # Label sits beside the pathway; use two lines for the longer name.
        if name=='noradrenaline': tx[1].become(T('noradrenaline',26,TEAL).move_to([x+.6, .35,0])); ar.shift(LEFT*1.1); rec.shift(LEFT*1.1)
        # Both ends share the receptor's x coordinate, including after centering.
        g.add(VGroup(a,b,ar,tx))
    if which==1: g.shift(RIGHT*3.25)
    return g


class S00Title(TitleCard):
    LESSON='Merkel Cells: Touch Receptors That Are Not Neurons'
    TITLE='A Brief Current That Holds a Press'
    def construct(self):
        self.play(FadeIn(label('BIOCHEMISTRYPEDIA',2.1,TEAL,22)),run_time=.3)
        lesson=T('Merkel Cells: Touch Receptors\nThat Are Not Neurons',26,GREY).move_to([0,1,0])
        title=T('A Brief Current\nThat Holds a Press',48,font=TITLE_FONT).move_to([0,-.7,0])
        self.play(FadeIn(lesson),Write(title),run_time=1.2); self.finish()

class S01Q(SpokenScene):
    def construct(self):
        c=cell(-1,-.1,2.3)
        pip=Polygon([1,.6,0],[4.8,2.6,0],[5.2,2,0],color=TEXT,fill_color=GREY,fill_opacity=.3)
        self.add(c,pip,label('Merkel cell',-2.65,ORANGE),T('recording pipette',28).move_to([3.8,-.1,0]),Line([3,.3,0],[3,1.2,0],color=TEXT))
        self.at('you might expect'); self.play(FadeIn(label('Does its current last?',3.2,TEXT,36)),run_time=.4)
        self.at('Does it'); self.finish()

class S02Cultured(SpokenScene):
    def construct(self):
        self.add(plot_base(),label('Cultured Merkel cells • mouse pups',3.35,TEXT,28))
        start=VGroup(T('press starts',26).move_to([-2.8,-.8,0]),Arrow([-3.5,-1,0],[-5.25,-1.8,0],color=TEXT,buff=.05))
        self.at('In cultured'); self.play(Create(trace(0,.7)),FadeIn(start),run_time=.5)
        self.at('pressing evokes'); self.play(Create(trace(.7,8)),run_time=1.2); self.finish()

class S03Settle(SpokenScene):
    def construct(self):
        self.add(plot_base(),trace(0,8),label('Cultured Merkel cells • mouse pups',3.35,TEXT,28))
        self.at('It inactivates'); self.play(Create(trace(8,24)),run_time=1)
        self.at('then settles'); s=settled(); self.play(Create(trace(24,40)),Create(s[2]),FadeIn(s[3]),run_time=.7); self.finish()

class S04Twentieth(SpokenScene):
    def construct(self):
        self.add(settled())
        plateau=VGroup(Line([.2,-1.5,0],[5.5,-1.5,0],color=GREEN,stroke_width=7),Line([.2,-1.4,0],[.2,-1.65,0],color=GREEN),Line([5.5,-1.4,0],[5.5,-1.65,0],color=GREEN))
        peak=VGroup(Line([-5.05,-1.8,0],[-5.05,1.9,0],color=GOLD,stroke_width=7),T('peak 370 pA',26,GOLD).move_to([-3.5,.65,0]))
        self.at('The steady part'); self.play(Create(plateau),Create(peak),run_time=.5)
        self.at('only about'); self.play(FadeIn(label('Steady = 20 / 370 ≈ 5.4% of peak',.15,TEXT,30)),run_time=.4); self.finish()

class S05Puzzle(SpokenScene):
    def construct(self):
        p=lambda t,i:[-5.1+10.4*t/1000,.8+1.8*i/400,0]
        ts=np.r_[np.linspace(0,80,180),np.linspace(80,1000,100)]
        g=VGroup(Line(p(0,0),p(1000,0),color=TEXT),Line(p(0,0),p(0,400),color=TEXT),VMobject(color=BLUE,stroke_width=4).set_points_as_corners([p(t,current(t)) for t in ts]),
            T('370 pA',26,BLUE).move_to([-3.7,2.5,0]),T('20 pA',26,BLUE).move_to([4,1.35,0]))
        self.add(g,label('Merkel-cell current',3.3,BLUE,28),ticks(spike_times(),-1.6,end=9,h=1.3),label('SA1 through the hold • schematic',-2.8,PURPLE,28),T('?',46,GOLD).move_to([0,-.25,0]))
        self.at('So how can'); self.play(Create(Line([-5.1,-2.4,0],[5.3,-2.4,0],color=TEXT)),FadeIn(label('press onset → whole hold',-3.4,TEXT,26)),run_time=.35); self.finish()

class S06Charge(SpokenScene):
    def construct(self):
        base=plot_base(); base[1][1].move_to([2.7,-2.55,0])
        self.add(base,trace(),DashedVMobject(trace(40,80),num_dashes=32),label('Compare charge: area under current',3.35,TEXT,30))
        xs=np.linspace(0,80,250); p=lambda t,i:[-5.25+10.85*t/80,-1.8+4*i/400,0]
        band=Polygon(p(0,0),p(80,0),p(80,20),p(0,20),color=GREEN,fill_opacity=.7,stroke_width=0)
        peak=Polygon(p(0,20),*[p(t,current(t)) for t in xs],p(80,20),color=GOLD,fill_opacity=.6,stroke_width=0)
        self.at('Compare charge'); self.play(FadeIn(band),FadeIn(T('steady part',26,GREEN).move_to([3,-1.05,0])),run_time=.4)
        self.at('Charge is the'); self.play(FadeIn(peak),FadeIn(T('transient excess',26,GOLD).move_to([-1,1.3,0])),run_time=.4)
        self.play(FadeIn(label('I(t) = 20 + 350 exp(−t / 8 ms) pA',-3.05,TEXT,26)),FadeIn(label('Hypothetical extrapolation from group means',-3.55,TEXT,26)),run_time=.25); self.finish()

class S07Predict(SpokenScene):
    def construct(self):
        g=charge_stage(); self.add(*g[:8],g[9])
        self.at('Predict'); self.wait(.2)
        self.at('Which part brings'); self.play(FadeIn(g[8]),run_time=.4); self.finish()

class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(charge_stage()); self.wait(5)

class S09Reveal(SpokenScene):
    def construct(self):
        g=charge_stage(False); self.add(g[0],g[1],g[3],g[4],g[5],g[6],g[7])
        clock=ValueTracker(.001)
        shades=always_redraw(lambda:charge_areas(clock.get_value()))
        bars=always_redraw(lambda:charge_fills(clock.get_value()))
        timer=always_redraw(lambda:M(f'{clock.get_value()/1000:.2f} s',28).move_to([4.2,2.95,0]))
        self.add(shades,bars,timer)
        self.at('The small'); self.play(clock.animate.set_value(140),run_time=1.8,rate_func=linear)
        marker=VGroup(DashedLine(CP(140,0),CP(140,150),color=TEXT),T('140 ms\nsteady has\ncaught up',26).move_to([3.55,1.5,0]))
        self.play(FadeIn(marker),run_time=.2); self.wait(.6)
        self.at('In this thought'); self.play(FadeIn(label('Transient ≈ 2.8 pC     Steady = 20 pC',-3.0,TEXT,26)),run_time=.2)
        self.play(clock.animate.set_value(300),run_time=1.5,rate_func=linear)
        self.at('it carries'); self.play(FadeOut(marker),clock.animate.set_value(1000),FadeIn(label('About 88% steady • assumed 1 s plateau',-3.6,GREEN,26)),run_time=.8,rate_func=linear); self.finish()

class S10Why(SpokenScene):
    def construct(self):
        x=lambda t:-5+10.5*t/1000; y=lambda q:-2+4.7*q/22
        axes=VGroup(Line([x(0),y(0),0],[x(1000),y(0),0],color=TEXT),Line([x(0),y(0),0],[x(0),y(22),0],color=TEXT))
        a=VMobject(color=GOLD,stroke_width=5).set_points_as_corners([[x(t),y(2.8*(1-np.exp(-t/8))),0] for t in np.r_[np.linspace(0,80,160),np.linspace(80,1000,100)]])
        b=Line([x(0),y(0),0],[x(1000),y(20),0],color=GREEN,stroke_width=5)
        self.add(axes,label('Cumulative charge (pC)',3.35,TEXT,30),T('0',26).move_to([-5,-2.4,0]),T('1000',26).move_to([5.5,-2.4,0]),label('time since press onset (ms)',-2.95,TEXT,26),*[T(str(q),26).move_to([-5.6,y(q),0]) for q in (0,10,20)])
        ip=lambda t,q:[-3.7+3.3*t/100,.6+1.4*q/3]
        inset=VGroup(Rectangle(width=4.4,height=2.4,color=GREY,fill_color=BG,fill_opacity=1).move_to([-2,1.55,0]),T('transient: 0–100 ms',26,GOLD).move_to([-2,2.45,0]),Line([*ip(0,0),0],[*ip(100,0),0],color=TEXT),Line([*ip(0,0),0],[*ip(0,3),0],color=TEXT),VMobject(color=GOLD,stroke_width=4).set_points_as_corners([[*ip(t,2.8*(1-np.exp(-t/8))),0] for t in np.linspace(0,100,180)]),T('0',26).move_to([-3.7,.3,0]),T('100',26).move_to([-.4,.3,0]))
        self.at("The peak's charge"); self.play(Create(a),FadeIn(inset),run_time=1.1)
        self.play(FadeIn(T('2.8 pC',26,GOLD).move_to([3,-1.05,0])),run_time=.3)
        self.at('A steady current'); self.play(Create(b),run_time=1.3)
        cross=140.; marker=VGroup(Dot([x(cross),y(2.8),0],color=TEXT,radius=.09),DashedLine([x(cross),y(2.8),0],[x(cross),y(0),0],color=TEXT),T('140',26).move_to([x(cross),-2.4,0]),T('steady keeps adding',26,GREEN).move_to([3.5,2.7,0]))
        self.play(FadeIn(marker),FadeIn(label('Crossover ≈ 140 ms',-3.5,GREEN,26)),run_time=.4); self.finish()

class S11Mislead(SpokenScene):
    def construct(self):
        self.at('Peaks mislead'); self.play(FadeIn(T('Peaks mislead\nabout holds.',50,font=TITLE_FONT)),run_time=.5); self.finish()

class S12Small(SpokenScene):
    def construct(self):
        c=cell(0,.1,1.75)
        charge=Rectangle(width=1.8,height=1.6,fill_color=BLUE,fill_opacity=.6,stroke_width=0).move_to(c)
        charge_label=T('charge on the\nmembrane',26).move_to([0,-1.95,0])
        self.add(c,charge,label('Illustrative passive linear membrane',3.3,TEXT,28),charge_label,label('Steady-state illustration, not a Merkel-cell voltage prediction',-2.8,GOLD,26),label('Real channel currents change with voltage',-3.4,TEXT,26))
        leak=VGroup(Arrow([1.8,.1,0],[3.4,-.5,0],color=BLUE,buff=.05),T('leaks away',26,BLUE).move_to([4.7,-.5,0]))
        self.at('But the membrane'); self.play(FadeIn(leak),run_time=.4)
        self.at('brief charge drains'); self.play(charge.animate.stretch(.02,1,about_edge=DOWN),run_time=.8)
        self.at('A steady current'); self.play(FadeOut(leak),VGroup(c,charge,charge_label).animate.shift(LEFT*3.6),run_time=.4)
        inflow=Arrow([-3.6,2.7,0],[-3.6,1.65,0],color=BLUE,buff=.05)
        plateau=VGroup(Line([-.7,1.3,0],[5.5,1.3,0],color=BLUE,stroke_width=5),Line([-.7,.8,0],[-.7,2,0],color=TEXT),Line([-.7,.8,0],[5.5,.8,0],color=TEXT),T('20 pA, steady',26,BLUE).move_to([2.3,2,0]),T('time →',26).move_to([4.5,.35,0]))
        self.play(GrowArrow(inflow),Create(plateau),charge.animate.stretch(50,1,about_edge=DOWN),run_time=.5)
        text=VGroup(M('Assumed R = 1 GΩ',26),M('IR = 20 mV above rest',26,GREEN)).arrange(DOWN,buff=.4).move_to([1.8,-.8,0])
        self.play(FadeIn(text),run_time=.4); self.finish()

class S13Ca(SpokenScene):
    def construct(self):
        top=2.3
        c=RoundedRectangle(width=7,height=4.9,corner_radius=.55,
            stroke_color=ORANGE,stroke_width=5,fill_color=ORANGE,
            fill_opacity=.2).move_to([0,-.15,0])
        self.add(c,label('Proposed amplification',3.3,GOLD,30),T('+ 20 mV illustrative depolarization',28,GREEN).move_to([0,-.3,0]))
        self.at('voltage gated calcium channels')
        # Mask short membrane segments to seat the proposed channels in the edge.
        gaps=VGroup(*[Rectangle(width=.8,height=.18,stroke_width=0,
            fill_color=BG,fill_opacity=1).move_to([x,top,0]) for x in (-2.2,0,2.2)])
        ch=VGroup(*[DashedVMobject(Rectangle(width=.8,height=.85,color=BLUE),num_dashes=12).move_to([x,top,0]) for x in (-2.2,0,2.2)])
        channel_label=T('Voltage-gated calcium channels\nproposed',26,BLUE).move_to([0,1.15,0])
        leaders=VGroup(*[Line([x,1.65,0],[x,1.87,0],color=BLUE) for x in (-2.2,0,2.2)])
        self.play(FadeIn(gaps),Create(ch),FadeIn(channel_label),Create(leaders),run_time=.5)
        self.at('That is a'); self.play(FadeIn(label('Proposal • not proven',-3.15,GOLD,30)),run_time=.4); self.finish()

class S14Clue(SpokenScene):
    def construct(self):
        self.add(label('SA1 spikes • zoom into the hold',3.1,TEXT,32))
        self.at('There is a'); self.play(Create(ticks(spike_times(),.2,end=9,h=3.2)),run_time=.7)
        self.at('in the timing'); self.play(Create(Line([-5.5,-2,0],[5.5,-2,0],color=TEXT,stroke_width=4)),FadeIn(label('during the hold • time, not to scale',-2.6,TEXT,26)),FadeIn(label('Schematic intervals',-3.25,PURPLE,26)),run_time=.4); self.finish()

class S15Cv(SpokenScene):
    def construct(self):
        ts=spike_times(); ts=ts[ts<9]; gaps=np.diff(ts); mean=gaps.mean(); sd=gaps.std()
        self.add(ticks(ts,1.95,end=9,h=1.3),label('Schematic gaps between SA1 spikes',3.2,TEXT,30))
        # Enlarge the first five actual intervals using one common length scale.
        scale=3.5; mx=-5.3
        gapbars=VGroup(*[Line([mx,.9-.35*i,0],[mx+scale*gap,.9-.35*i,0],
            color=TEAL,stroke_width=8) for i,gap in enumerate(gaps[:5])])
        self.at('Irregularity can'); self.play(Create(gapbars),FadeIn(T('First five gaps • enlarged',26,TEAL).move_to([2.5,1.05,0])),run_time=.5)
        sy=-1.65; ex=mx+scale*sd
        sdbracket=VGroup(Line([mx,sy,0],[ex,sy,0],color=GOLD,stroke_width=4),
            Line([mx,sy-.12,0],[mx,sy+.12,0],color=GOLD),
            Line([ex,sy-.12,0],[ex,sy+.12,0],color=GOLD))
        worked=VGroup(DashedLine([mx,-1.05,0],[mx+scale*mean,-1.05,0],color=TEXT,stroke_width=4,dash_length=.12),
            T(f'mean = {mean:.2f}',26).move_to([-1.8,-1.05,0]),sdbracket,
            T(f'SD = {sd:.2f}',26,GOLD).move_to([-1.8,sy,0]))
        self.at('Divide the'); self.play(FadeIn(worked),FadeIn(T('CV = SD / mean interval',26).move_to([2.6,.25,0])),FadeIn(T(f'{sd:.2f} / {mean:.2f} ≈ {sd/mean:.2f}',26).move_to([2.6,-.35,0])),run_time=.4)
        self.at('by their mean'); self.play(Create(ticks(np.arange(.3,9,.6),-2.45,end=9,h=.6)),FadeIn(label('0 = a metronome • equal gaps',-3.25,TEXT,28)),run_time=.4); self.finish()


class S16Predict(SpokenScene):
    def construct(self):
        g=model_stage(); self.add(g[0],g[2],g[6])
        self.at('a fixed threshold'); self.play(FadeIn(g[1]),Create(g[4][0][0]),run_time=.4)
        self.at('a steady current'); self.play(FadeIn(g[3][0]),Create(g[4][0][1]),Create(g[4][1]),run_time=1.3)
        self.at('What could'); self.play(FadeIn(g[5]),run_time=.3)
        self.at('randomly timed packets'); self.play(FadeIn(g[3][1]),run_time=.3); self.finish()

class S17Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(model_stage()); self.wait(5)

class S18Reveal(SpokenScene):
    def construct(self):
        g=model_stage(False); g[2][1].shift(DOWN*.45); self.add(g)
        pts,spikes,packets=lif_detail(True)
        packetblocks=VGroup(*[Rectangle(width=.06,height=.13*amp,fill_color=TEAL,fill_opacity=1,stroke_width=0).move_to([-5.5+11*t/10,-.85,0]) for t,amp in packets])
        random=VGroup(model_voltage(True,y=-1.95),ticks(spikes,-2.25,end=10,h=.5),packetblocks)
        self.at('One possible result'); blank=g[6]; self.play(FadeOut(blank),Create(random),run_time=1); g.remove(blank)
        cv=np.std(np.diff(spikes))/np.mean(np.diff(spikes))
        cvtag=label('One simulated run • time, not to scale',-3.1,TEXT,26)
        self.play(FadeIn(cvtag),run_time=.3)
        self.at('And light on');
        # Preserve the model beside reported summary data, without inventing data.
        model=VGroup(g,random,cvtag)
        panel=VGroup(RoundedRectangle(width=5.7,height=5.5,corner_radius=.2,color=GREEN),T('Light on Merkel cells',28,GREEN).move_to([0,1.9,0]),T('Reported SA1 hold',28).move_to([0,1.15,0]),T('CV ≈ 1.17',38).move_to([0,.25,0]),T('12 units',30).move_to([0,-.55,0]),T('Individual spike times\nnot available',28).move_to([0,-1.7,0])).move_to([3.25,0,0])
        # Rebuild a legible model panel rather than shrinking its text.
        left=VGroup(RoundedRectangle(width=5.7,height=5.5,corner_radius=.2,color=TEAL).move_to([-3.25,0,0]),T('Random-release model',28,TEAL).move_to([-3.25,2,0]),model_voltage(True,y=.4,x0=-5.7,x1=-.8),ticks(spikes,-.3,x0=-5.7,x1=-.8,end=10,h=1),T('One simulated run',26).move_to([-3.25,-1.3,0]),T('Schematic • time, not to scale',26).move_to([-3.25,-2,0]))
        self.play(FadeOut(g),FadeOut(cvtag),FadeOut(random[2]),run_time=.2)
        self.play(Transform(random[0],left[2]),Transform(random[1],left[3]),run_time=.3)
        self.play(FadeIn(left[0]),FadeIn(left[1]),FadeIn(left[4]),FadeIn(left[5]),FadeIn(panel),run_time=.2); self.finish()

class S19Notproof(SpokenScene):
    def construct(self):
        r=VGroup(ticks(lif(True),0,end=10,h=1.5),label('Schematic model output',-1.25,TEXT,28)); title=label('Consistent with a synapse • not proof',3.2,GOLD,30); self.add(r)
        self.at('That is a clue'); self.play(FadeIn(title),run_time=.4)
        stem=Line([0,-2.5,0],[0,-.8,0],color=PURPLE,stroke_width=10)
        branches=VGroup(*[Line([0,-.8,0],[x,1.3,0],color=PURPLE,stroke_width=8) for x in (-4,0,4)])
        cells=VGroup(*[cell(x,1.95,.65) for x in (-4,0,4)])
        self.at('A branched ending'); self.play(FadeOut(r),Transform(title,label('Another source of irregularity: a branched ending',3.2,TEXT,28)),Create(stem),Create(branches),FadeIn(cells),run_time=.7)
        self.at('several spike sites'); self.play(FadeIn(VGroup(*[Dot([x,1.3,0],radius=.15,color=YELLOW) for x in (-4,0,4)])),FadeIn(T('Merkel cells',26,ORANGE).move_to([-4, .65,0])),run_time=.4)
        self.at('could add irregularity'); self.play(FadeIn(label('Yellow dots: possible spike-initiation sites',-3.2,TEXT,26)),run_time=.4); self.finish()

class S20Synapse(SpokenScene):
    def construct(self):
        self.add(contact(),T('contact magnified',28).move_to([3.9,-.35,0]),Line([2.0,-.35,0],[1.0,-.35,0],color=TEXT)); self.at('So what crosses'); self.play(FadeIn(T('?',60,GOLD).move_to([0,-.35,0])),run_time=.4)
        self.at('That is still'); self.play(FadeIn(label('What crosses the synapse?',-3.3,TEXT,32)),run_time=.4); self.finish()

class S21Na(SpokenScene):
    def construct(self):
        g=accounts(1); self.at('In mouse touch domes'); self.play(FadeIn(g[0][0]),FadeIn(g[0][1]),FadeIn(g[0][3][0]),run_time=.5)
        self.at('toward noradrenaline'); self.play(Create(g[0][2]),FadeIn(g[0][3][1]),FadeIn(g[0][3][3]),run_time=.5)
        self.at('receptors'); self.play(FadeIn(g[0][3][2]),run_time=.3)
        self.at('The channel it'); self.play(FadeIn(label('Downstream channel: unknown',-3,GOLD,28)),run_time=.4); self.finish()

class S22Asic(SpokenScene):
    def construct(self):
        g=accounts(); old=label('Downstream channel: unknown',-3,GOLD,28); first=accounts(1)[0]; self.add(first,old)
        self.at('In rodent whiskers'); self.play(Transform(first,g[0]),FadeOut(old),FadeIn(g[1][0]),FadeIn(g[1][1]),FadeIn(g[1][3][0]),run_time=.6)
        self.at('attributed to'); self.play(Create(g[1][2]),FadeIn(g[1][3][1]),FadeIn(g[1][3][3]),run_time=.5)
        self.at('channels instead'); self.play(FadeIn(g[1][3][2]),FadeIn(label('Competing accounts in different preparations',-3,GOLD,26)),run_time=.4); self.finish()

class S23Open(SpokenScene):
    def construct(self):
        self.add(accounts(),label('Competing accounts in different preparations',-2.9,GOLD,26))
        self.at('Neither account'); self.play(FadeIn(label('Open question',-3.5,TEXT,30)),run_time=.5); self.finish()

class S24Take(SpokenScene):
    def construct(self):
        c=cell(-3,.5,1.85); ending=RoundedRectangle(width=4.2,height=2,corner_radius=.35,color=PURPLE,fill_color=PURPLE,fill_opacity=.4).move_to([3,.5,0])
        self.add(c,ending,label('In mouse touch domes',3.2,TEXT,30))
        self.at('The ending feels'); self.play(FadeIn(T('Feels the change',30,PURPLE).move_to([3,-1.6,0])),run_time=.4)
        self.at('holds the press'); self.play(FadeIn(T('Mainly holds the press',28,ORANGE).move_to([-3,-1.6,0])),run_time=.4)
        self.at('How it signals'); self.play(FadeIn(T('?',54,GOLD).move_to([0,1.5,0])),FadeIn(label('How it signals is still open',-2.5,GOLD,28)),FadeIn(label('A small steady current can dominate charge',-3.25,GREEN,28)),run_time=.5); self.finish()

class S25End(EndCard):
    LINE='In mouse touch domes, the Merkel cell mainly holds the press.'
    def construct(self):
        line=T('In mouse touch domes,\nthe Merkel cell mainly holds the press.',36,font=TITLE_FONT).move_to([0,.5,0])
        self.play(FadeIn(line),run_time=.5)
        self.add(label('Peaks mislead about holds.',-1.2,GREEN,30),label('biochemistrypedia.com',-2.4,TEAL,26)); self.finish()
