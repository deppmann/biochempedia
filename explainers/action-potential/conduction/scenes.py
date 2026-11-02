"""Moving Down the Axon. All cues follow audio/words.json.
COLOR MAP: yellow sodium; blue potassium; green membrane voltage;
red inactivation/refractory; teal conductance; orange driving force;
grey membrane, myelin, axes. White arrows denote axial current;
blue water is an analogy, not an additional ionic species.
HH equations and Ax are reused verbatim from scenes.old.py.
"""
import os
import numpy as np
from bp_style import *

NA, K, VOLT, INACT = YELLOW, BLUE, GREEN, RED
ORANGE = "#F29E4C"

def _rates(V):
    am = 1.0 if abs(V + 40) < 1e-6 else 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
    bm = 4 * np.exp(-(V + 65) / 18)
    ah = 0.07 * np.exp(-(V + 65) / 20)
    bh = 1 / (1 + np.exp(-(V + 35) / 10))
    an = 0.1 if abs(V + 55) < 1e-6 else 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10))
    bn = 0.125 * np.exp(-(V + 65) / 80)
    return am, bm, ah, bh, an, bn


def hh_free(T=10.0, dt=0.005, stim=(0.5, 0.5, 15.0)):
    gNa, gK, gL, ENa, EK, EL = 120., 36., 0.3, 50., -77., -54.4
    V = -65.
    am, bm, ah, bh, an, bn = _rates(V)
    m, h, n = am / (am + bm), ah / (ah + bh), an / (an + bn)
    out = []
    for i in range(int(T / dt)):
        t = i * dt
        I = stim[2] if stim[0] <= t < stim[0] + stim[1] else 0.0
        gna, gk = gNa * m ** 3 * h, gK * n ** 4
        out.append((t, V, gna, gk))
        V += dt * (I - gna * (V - ENa) - gk * (V - EK) - gL * (V - EL))
        am, bm, ah, bh, an, bn = _rates(V)
        m += dt * (am * (1 - m) - bm * m); h += dt * (ah * (1 - h) - bh * h); n += dt * (an * (1 - n) - bn * n)
    return np.array(out)


def hh_clamp(Vc=0.0, T=7.5, dt=0.005):
    """gates relax at a held voltage, starting from rest: returns t, gNa(t), gK(t)."""
    V0 = -65.
    am, bm, ah, bh, an, bn = _rates(V0)
    m, h, n = am / (am + bm), ah / (ah + bh), an / (an + bn)
    out = []
    for i in range(int(T / dt)):
        am, bm, ah, bh, an, bn = _rates(Vc)
        out.append((i * dt, 120. * m ** 3 * h, 36. * n ** 4))
        m += dt * (am * (1 - m) - bm * m); h += dt * (ah * (1 - h) - bh * h); n += dt * (an * (1 - n) - bn * n)
    return np.array(out)


class Ax:
    """maps (t, y-value) to scene coordinates."""
    def __init__(self, x0, x1, y0, y1, t0, t1, v0, v1):
        self.x0, self.x1, self.y0, self.y1, self.t0, self.t1, self.v0, self.v1 = x0, x1, y0, y1, t0, t1, v0, v1

    def X(self, t):
        return self.x0 + (t - self.t0) / (self.t1 - self.t0) * (self.x1 - self.x0)

    def Y(self, v):
        return self.y0 + (v - self.v0) / (self.v1 - self.v0) * (self.y1 - self.y0)

    def P(self, t, v):
        return np.array([self.X(t), self.Y(v), 0.0])


# Shared geometry keeps the membrane faces joined as ONE tube.
XS = [-4.8, -2.4, 0, 2.4, 4.8]

def label(s, x=0, y=2.9, size=30, color=TEXT):
    if '\n' in s:
        return VGroup(*[T(line,size,color) for line in s.split('\n')]).arrange(DOWN,buff=.13).move_to([x,y,0])
    return T(s, size, color).move_to([x,y,0])

def arrow(a,b,color=TEXT,width=5):
    return Arrow([*a,0],[*b,0],buff=0,color=color,stroke_width=width,tip_length=.22)

def patch(x):
    core=Rectangle(width=2.4,height=2.4,stroke_width=0,fill_color=GREY,fill_opacity=.1).move_to([x,-.15,0])
    faces=VGroup(*[Rectangle(width=2.32,height=.26,stroke_width=0,fill_color=GREY,fill_opacity=.6).move_to([x,y,0]) for y in [-1.35,1.05]])
    return VGroup(core,faces)

def axon(active=None):
    a=VGroup(*[patch(x) for x in XS])
    if active is not None: a[active].set_color(NA).set_fill(NA,opacity=.3)
    a.add(RoundedRectangle(width=12.1,height=2.66,corner_radius=.25,color=GREY,stroke_width=3).move_to([0,-.15,0]))
    return a

def fire(p,color=NA,opacity=.3):
    return p.animate.set_color(color).set_fill(color,opacity=opacity)

def anatomy():
    return VGroup(label('inside the axon',0,-.8,28),label('outside',4.8,1.65,28))

def loop(x0,x1):
    # Two cubic bends keep the circuit within its two patches, with an axial
    # arrow pointing away from the source and a distinct exterior return.
    sign=np.sign(x1-x0)
    start=np.array([x0+sign*.65,1.38,0])
    outer=np.array([x1,1.38,0])
    path=VMobject(color=TEXT,stroke_width=4)
    path.start_new_path(start)
    path.add_cubic_bezier_curve_to(
        np.array([x0+sign*.65,2.25,0]),np.array([x1,2.25,0]),outer)
    path.add_cubic_bezier_curve_to(
        np.array([x1+sign*.55,.2,0]),np.array([x1+sign*.25,-.1,0]),np.array([x1,-.1,0]))
    path.add_line_to(np.array([x0+sign*.65,-.1,0]))
    path.add_cubic_bezier_curve_to(
        np.array([x0+sign*.4,-.1,0]),np.array([x0+sign*.65,.7,0]),start)
    axial=arrow((x0+sign*.7,-.1),(x1-sign*.15,-.1),width=4)
    return VGroup(path,axial)

def pore(x,y=1.05,color=NA,closed=False):
    g=VGroup(*[RoundedRectangle(width=.13,height=.65,corner_radius=.05,
       color=color,fill_color=color,fill_opacity=.6).move_to([x+d,y,0]) for d in [-.18,.18]])
    g.add(Line([x-.1,y-.22,0],[x+.1,y-.22,0],color=color,stroke_width=3))
    if closed:
        g.add(Line([x-.18,y+.05,0],[x+.13,y+.05,0],color=INACT,stroke_width=6),
              Dot([x+.13,y+.05,0],radius=.09,color=INACT))
    return g

def wraps(x):
    # Transparent lamellae wrap the tube; the axoplasm stays visible through
    # the centre instead of being masked with a background-coloured box.
    g=VGroup()
    for width,height,opacity in [(3.15,3.1,.10),(2.95,2.8,.10),(2.75,2.5,.10)]:
        g.add(RoundedRectangle(width=width,height=height,corner_radius=.45,
            color=GREY,stroke_width=2,fill_color=GREY,
            fill_opacity=opacity).move_to([x,0,0]))
    return g

def myelin(bare=False):
    tube=RoundedRectangle(width=12,height=2.1,corner_radius=.35,color=GREY,
        fill_color=GREY,fill_opacity=.12)
    a=VGroup(tube,wraps(-2),wraps(2))
    if bare: a[2].set_opacity(0)
    return a

def node(x):
    return VGroup(pore(x-.19),pore(x+.29),pore(x-.19,-1.05),pore(x+.29,-1.05))

def nodes(): return VGroup(*[node(x) for x in [-4,0,4]])

def node_glow(x):
    return VGroup(*[RoundedRectangle(width=.95,height=.75,corner_radius=.15,
        color=NA,fill_color=NA,fill_opacity=.35).move_to([x,y,0]) for y in [-1.05,1.05]])

def question_stage():
    return axon(2),label("Pause. Why doesn't the spike turn back?",y=3.2,size=32),VGroup(loop(0,-2.4),loop(0,2.4))

def bare_highlight():
    return RoundedRectangle(width=2.4,height=2.5,corner_radius=.2,color=TEAL,
       fill_color=TEAL,fill_opacity=.09).move_to([2,0,0])

def demy_stage():
    return VGroup(myelin(True),nodes(),bare_highlight()),label('Pause. Demyelinate one stretch:\nwhat happens?',y=2.8,size=32)

def leaks(x=2,y=1.05,color=TEXT):
    return VGroup(*[arrow((x+d,y),(x+d,y+.85),color,3) for d in [-.8,0,.8]])

class S00Title(TitleCard):
    LESSON='The Action Potential and Conduction'
    TITLE='Moving Down the Axon'

    def construct(self):
        brand=label('BIOCHEMISTRYPEDIA',y=2.1,size=26,color=TEAL)
        lesson=label(self.LESSON.upper(),y=1.2,size=26,color=GREY)
        title=T(self.TITLE,48,font=TITLE_FONT)
        rule=Line([-1.2,-.7,0],[1.2,-.7,0],color=GOLD,stroke_width=4)
        self.play(FadeIn(brand),FadeIn(lesson),run_time=.4)
        self.play(FadeIn(title),GrowFromCenter(rule),run_time=.7)
        self.finish()

class S01Question(SpokenScene):
    def construct(self):
        a=axon(); self.add(a,anatomy())
        self.at('fires at one',lead=0); self.play(fire(a[0]),run_time=.2)
        self.at('How does it'); self.add(label('How does the spike reach the far end?',y=2.9,size=32))
        self.at("why doesn't it"); self.add(label("Why doesn't it come back?",y=-2.6,size=34))
        self.finish()

class S02Spread(SpokenScene):
    def construct(self):
        a=axon(0); self.add(a,anatomy())
        self.at('Inward current'); self.play(GrowArrow(arrow((-4.8,2.3),(-4.8,0),NA)),FadeIn(label('inward Na+ current',-3.8,3,28,NA)),run_time=.6)
        self.at('spreads along'); self.play(Create(loop(-4.8,-2.4)),FadeIn(label('charges next patch',1.7,-2.85,30)),run_time=1.4)
        self.at('next stretch'); self.play(fire(a[1],VOLT,.25),run_time=.6)
        self.at('to threshold'); self.play(FadeIn(label('threshold',-2.4,-2.05,28,VOLT)),run_time=.35)
        self.finish()

class S03Chain(SpokenScene):
    def construct(self):
        a=axon(0); a[1].set_color(VOLT); self.add(a,anatomy())
        self.at('That stretch fires'); self.play(fire(a[1]),fire(a[0],INACT,.2),run_time=.6)
        c=loop(-2.4,0)
        self.at('its current spreads'); self.play(Create(c),run_time=1.2)
        self.at('The spike moves'); self.play(FadeOut(c),fire(a[1],INACT,.2),fire(a[2]),run_time=.6)
        self.at('patch by patch'); self.play(fire(a[2],INACT,.2),fire(a[3]),run_time=.4)
        self.play(fire(a[3],INACT,.2),fire(a[4]),run_time=.4); self.finish()

class S04Predict(SpokenScene):
    def construct(self):
        a,q,c=question_stage(); self.add(a,anatomy())
        caption=label('Current spreads both ways',y=-2.5,size=32)
        self.at('Here is a question'); self.play(FadeIn(caption),run_time=.4)
        inward=VGroup(arrow((0,2.75),(0,.45),NA),label('inward Na+ current',2.6,2.65,27,NA))
        self.at('Current spreads both ways'); self.play(Create(c),FadeIn(inward),run_time=1.2)
        self.at("So why doesn't"); self.play(FadeOut(caption),FadeOut(inward),run_time=.2)
        self.play(FadeIn(q),run_time=.25)
        self.finish()

class S05Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(*question_stage(),anatomy()); self.wait(float(os.environ['KX_DURATION']))

class S06Refractory(SpokenScene):
    def construct(self):
        a=axon(2); a[1].set_color(INACT).set_fill(INACT,opacity=.2); self.add(a)
        self.at('The membrane just behind'); self.play(Indicate(a[1],color=INACT),run_time=.7)
        p=pore(-2.4,-2.1,closed=True)
        self.at('Its sodium channels'); self.play(FadeIn(p),FadeIn(label('Na+ channels',-2.4,-3.25,28,NA)),run_time=.4)
        self.at('are inactivated'); self.play(FadeIn(label('inactivated',.1,-2.1,28,INACT)),run_time=.4)
        self.at('It is refractory'); self.play(FadeIn(label('refractory',-2.4,2.5,32,INACT)),run_time=.4)
        self.at('so it cannot'); self.play(GrowArrow(arrow((-.2,0),(-1.21,0))),FadeIn(label('no spike',-2.4,0,28)),run_time=.6)
        self.finish()

class S07BothWays(SpokenScene):
    def construct(self):
        a=axon(); self.add(a)
        title=label('No preferred direction',size=34)
        self.at('The axon itself'); self.play(FadeIn(title),run_time=.4)
        e=VGroup(Line([0,2.25,0],[0,.3,0],color=TEAL,stroke_width=8),
          Polygon([-.2,.4,0],[.2,.4,0],[0,0,0],color=TEAL,fill_opacity=1),label('stimulus electrode',2.5,1.9,28,TEAL))
        self.at('Stimulate the middle'); self.play(FadeIn(e),fire(a[2]),run_time=.5)
        self.at('spikes travel both ways'); self.play(FadeOut(e),fire(a[2],INACT,.2),fire(a[1]),fire(a[3]),FadeIn(label('refractory wake',y=-2.4,color=INACT)),run_time=.8)
        self.at('A spike travels away'); self.play(FadeOut(title),run_time=.2); self.play(fire(a[1],INACT,.2),fire(a[3],INACT,.2),fire(a[0]),fire(a[4]),FadeIn(label('always away from the start',size=34)),run_time=.8)
        self.finish()

# Tube widths are diameters, not two independent membrane rows.
def two_tubes(water=False):
    g=VGroup()
    for y,h,name in [(1.5,.65,'narrow'),(-1.1,2.2,'wide')]:
        tube=RoundedRectangle(width=11.8,height=h,corner_radius=.22,color=GREY,
           fill_color=BLUE if water else GREY,fill_opacity=.3).move_to([0,y,0])
        g.add(VGroup(tube,label(name,-4.7,y,28)))
    return g

def spread_arrows():
    return VGroup(arrow((-3.7,1.5),(-1,1.5)),arrow((-3.7,-1.1),(4.5,-1.1)))

def narrow_leaks():
    return VGroup(*[arrow((x,1.22),(x,.55),BLUE,3) for x in [-3.2,-2.3,-1.4]])

class S08Diameter(SpokenScene):
    def construct(self):
        self.add(two_tubes()); self.at('Speed depends'); self.play(FadeIn(label('Diameter',size=36)),run_time=.4)
        self.at('A wider axon'); self.play(Indicate(self.mobjects[0][1][0],color=TEXT),run_time=.5)
        self.at('lower internal resistance'); self.play(FadeIn(label('lower internal resistance',1,-2.75,28)),Create(Line([1,-2.45,0],[1,-2.2,0],color=TEXT)),run_time=.4)
        c=spread_arrows()
        self.at('so current spreads farther'); self.play(GrowArrow(c[0]),GrowArrow(c[1]),FadeIn(narrow_leaks().set_color(TEXT)),run_time=1.5)
        self.at('before leaking away'); self.play(c[0].animate.set_opacity(.3),run_time=.5); self.finish()

class S09Pipe(SpokenScene):
    def construct(self):
        self.add(two_tubes(True),spread_arrows()); self.at('Think of a wide pipe'); self.play(FadeIn(label('Water in pipes',size=34)),run_time=.4)
        holes=VGroup(*[Dot([x,1.2,0],radius=.08,color=BG) for x in [-3.2,-2.3,-1.4]])
        self.at('leaky one'); self.play(FadeIn(holes),FadeIn(narrow_leaks()),run_time=.4)
        self.at('Farther spread'); self.play(Indicate(self.mobjects[1][1],color=TEXT),run_time=.8)
        self.at('squid giant axon'); self.play(FadeIn(label('Unmyelinated: speed ∝ √diameter',y=-2.8,size=28)),run_time=.5); self.finish()

class S10Myelin(SpokenScene):
    def construct(self):
        a=myelin(); self.add(a[0]); self.at('The other way'); self.play(FadeIn(label('Myelin',size=36)),run_time=.4)
        self.at('glial membrane wrapped'); self.play(FadeIn(a[1]),run_time=.55); self.wait(.35); self.play(FadeIn(a[2]),run_time=.55)
        self.play(FadeIn(label('gap',0,-2.4,30,TEXT)),Create(Line([0,-2.1,0],[0,-1.35,0],color=TEXT)),run_time=.3); self.finish()

class S11Hose(SpokenScene):
    def construct(self):
        hose=RoundedRectangle(width=11.8,height=1.8,corner_radius=.4,
            color=GREY,fill_color=BLUE,fill_opacity=.35)
        positions=[-4,-2,0,2,4]
        holes=VGroup(*[Dot([x,.9,0],radius=.11,color=BG) for x in positions])
        jets=VGroup()
        for x in positions:
            stream=VMobject(color=BLUE,stroke_width=7)
            stream.start_new_path(np.array([x,.9,0]))
            stream.add_cubic_bezier_curve_to(*[np.array(p) for p in [[x,2.25,0],[x+.45,2.4,0],[x+.7,1.8,0]]])
            jets.add(VGroup(stream,Dot([x+.74,1.6,0],radius=.08,color=BLUE)))
        self.add(hose,holes,jets)
        self.at('Picture a leaky garden hose'); self.play(FadeIn(label('Garden hose analogy',y=-2.6,size=34)),run_time=.3)
        self.at('wrapped in tape')
        self.play(FadeIn(label('myelin',y=3,size=32)),run_time=.2)
        for i,x in enumerate(positions):
            tape=VGroup(*[Line([x+d,-1,0],[x+d+.25,1,0],color=GREY,stroke_width=13) for d in [-.35,0,.35]])
            self.play(Create(tape),run_time=.17)
            self.play(FadeOut(jets[i]),FadeOut(holes[i]),run_time=.13)
        self.at('Less current leaks out'); self.finish()

# Equal volume Q in different widths: height = Q / width.
TANKS=[(-3.7,3.2),(2.4,1.25)]
BOTTOM=-2.55

def water_target(level,height):
    return level.copy().stretch_to_fit_height(height).move_to([level.get_x(),BOTTOM+height/2,0])

def tanks():
    b,l,s=VGroup(),VGroup(),VGroup()
    for x,w in TANKS:
        b.add(VMobject(color=GREY,stroke_width=4).set_points_as_corners([[x-w/2,2,0],[x-w/2,BOTTOM,0],[x+w/2,BOTTOM,0],[x+w/2,2,0]]))
        l.add(Rectangle(width=w-.1,height=.08,stroke_width=0,fill_color=BLUE,fill_opacity=.5).move_to([x,BOTTOM+.04,0]))
        s.add(arrow((x,2.75),(x,1.6),BLUE))
    return b,l,s

def tank_names():
    return VGroup(label('unmyelinated: wide',-3.7,-3.1,27),label('myelinated: narrow',2.5,-3.1,27))

def fill_tanks(scene,levels,volume,duration):
    scene.play(*[Transform(l,water_target(l,volume/(w-.1))) for l,(x,w) in zip(levels,TANKS)],run_time=duration,rate_func=linear)

class S12Tank(SpokenScene):
    def construct(self):
        b,l,s=tanks(); self.add(b,l,tank_names())
        self.at('Myelin also lowers'); self.play(FadeIn(label('Lower capacitance: a narrower tank',y=3.35,size=30)),run_time=.4)
        self.at('Think of a narrow water tank'); self.play(FadeIn(s),run_time=.3); fill_tanks(self,l,1.7,1.3)
        self.at('The same'); self.play(FadeIn(label('same pour, same time',y=2.65,size=27)),run_time=.3); fill_tanks(self,l,4.4,1.6)
        self.finish()

class S13Tank2(SpokenScene):
    def construct(self):
        b,l,s=tanks(); self.add(b,l,tank_names())
        # Voltage meters schematically share the tank level Q/C; no invented voltage trace.
        meters,fills=VGroup(),VGroup()
        for x,w in TANKS:
            mx=x+w/2+.55
            meters.add(Line([mx,BOTTOM,0],[mx,2,0],color=GREY),
                DashedLine([mx-.28,.3,0],[mx+.28,.3,0],color=VOLT),
                label('rest',mx+.55,-2.25,26),label('threshold',mx+.98,.7,26,VOLT),label('voltage',mx+.75,1.8,26))
            fills.add(Rectangle(width=.18,height=.08,stroke_width=0,fill_color=VOLT,fill_opacity=1).move_to([mx-.2,BOTTOM+.04,0]))
        self.at('With less capacitance'); self.play(FadeIn(meters),FadeIn(fills),run_time=.5)
        self.at('the same charge'); self.play(FadeIn(s),FadeIn(label('same charge, higher voltage',y=3.35,size=32)),run_time=.35)
        def charge(q,seconds):
            self.play(*[Transform(l[i],water_target(l[i],q/(w-.1))) for i,(x,w) in enumerate(TANKS)],
                *[Transform(fills[i],water_target(fills[i],q/(w-.1))) for i,(x,w) in enumerate(TANKS)],run_time=seconds,rate_func=linear)
        charge(2.7,2.4)
        self.at('The voltage climbs'); charge(4.4,1.8); self.finish()

class S14Nodes(SpokenScene):
    def construct(self):
        self.add(myelin()); c=arrow((-4,0),(0,0))
        self.at('So current'); self.play(GrowArrow(c),run_time=1.5)
        self.at('The gaps are nodes'); self.play(FadeIn(label('nodes of Ranvier',0,2.8,32)),Create(Line([0,2.45,0],[0,1.5,0],color=TEXT)),run_time=.4)
        self.at('where sodium channels'); self.play(FadeIn(nodes()),FadeIn(label('Na+ channels',-4,-2.5,28,NA)),Create(Line([-4,-2.15,0],[-4,-1.4,0],color=NA)),run_time=.4)
        self.at('regenerate the spike')
        self.play(FadeIn(node_glow(-4)),run_time=.25)
        self.play(FadeIn(node_glow(0)),run_time=.25)
        self.play(Transform(c,arrow((-4,0),(4,0))),run_time=.3)
        self.play(FadeIn(node_glow(4)),run_time=.25); self.finish()

class S15Saltatory(SpokenScene):
    def construct(self):
        self.add(myelin(),nodes(),*[node_glow(x) for x in [-4,0,4]]); self.at('This is saltatory conduction'); self.play(FadeIn(label('Saltatory conduction',y=3.25,size=34)),run_time=.4)
        self.at('Latin for leap'); self.play(FadeIn(label('saltatory: “leap”',y=-2.65,size=28)),run_time=.4)
        hop=CurvedArrow([-4,1.65,0],[0,1.65,0],angle=-PI/2,color=NA)
        self.at('skips'); self.play(Create(hop),FadeIn(label('skips',-2,2.15,28,NA)),run_time=.8)
        self.at('Current does not'); self.play(GrowArrow(arrow((-4,0),(0,0))),run_time=.65); self.play(Indicate(self.mobjects[3],color=NA),run_time=.25)
        self.at('It flows through'); self.play(Create(CurvedArrow([0,1.65,0],[4,1.65,0],angle=-PI/2,color=NA)),run_time=.4); self.play(GrowArrow(arrow((0,0),(4,0))),run_time=1.2); self.play(Indicate(self.mobjects[4],color=NA),run_time=.3); self.finish()

def walker(x,y):
    return VGroup(Circle(radius=.17,color=TEXT).move_to([x,y+.7,0]),Line([x,y+.5,0],[x,y,0],color=TEXT),Line([x,y,0],[x-.3,y-.4,0],color=TEXT),Line([x,y,0],[x+.3,y-.4,0],color=TEXT),Line([x-.3,y+.15,0],[x+.3,y+.4,0],color=TEXT))

def train(x,y):
    g=VGroup()
    for j in range(2):
        cx=x+j*1.45
        g.add(RoundedRectangle(width=1.35,height=.8,corner_radius=.2,color=TEXT).move_to([cx,y,0]))
        for d in [-.4,0,.4]: g.add(Rectangle(width=.22,height=.25,color=TEXT).move_to([cx+d,y+.08,0]))
        for d in [-.4,.4]: g.add(Circle(radius=.13,color=TEXT).move_to([cx+d,y-.5,0]))
    g.add(Line([x-.8,y-.7,0],[x+2.3,y-.7,0],color=GREY)); return g

class S16Speeds(SpokenScene):
    def construct(self):
        self.add(label('Mammalian peripheral nerve',y=3.15,size=34),label('species and temperature affect values',y=-3.2,size=26),walker(-5.6,1.1))
        X=lambda v:-5+v/120*10.4
        axis=VGroup(Line([X(0),-2.25,0],[X(120),-2.25,0],color=GREY))
        for v in [0,40,80,120]: axis.add(label(str(v),X(v),-2.65,26),Line([X(v),-2.25,0],[X(v),-2.4,0],color=GREY))
        self.add(axis,label('m/s',6.1,-2.65,26))
        self.at('Speeds vary widely'); self.wait(.1)
        inset=VGroup(RoundedRectangle(width=5,height=1.25,corner_radius=.15,color=GREY).move_to([-.9,1.15,0]),
            Line([-3.1,1.35,0],[.9,1.35,0],color=TEXT,stroke_width=30),
            label('0.6',-3.1,.85,26),label('2 m/s',.9,.85,26),label('×33 inset',-.9,.85,25),
            DashedLine([X(2),0,0],[-3.4,.65,0],color=GREY))
        self.at('unmyelinated'); self.play(Create(Line([X(.6),0,0],[X(2),0,0],color=TEXT,stroke_width=40)),FadeIn(label('C fibres: 0.6–2 m/s',-.9,2.25,30)),FadeIn(inset),run_time=.4)
        self.at('walking pace'); self.play(Indicate(self.mobjects[2]),run_time=.4)
        self.at('The largest myelinated'); self.play(Create(Line([X(70),-1.4,0],[X(120),-1.4,0],color=TEXT,stroke_width=40)),FadeIn(label('Largest myelinated: 70–120 m/s',0,-.65,30)),FadeIn(train(-4,-1.25)),run_time=.8)
        bracket=VGroup(Line([5.9,1.7,0],[5.9,-1.4,0],color=TEXT),Line([5.6,1.7,0],[5.9,1.7,0],color=TEXT),Line([5.6,-1.4,0],[5.9,-1.4,0],color=TEXT))
        self.at('a hundred times faster'); self.play(FadeIn(label('~100×',4.2,1.15,38)),Create(bracket),run_time=.3); self.finish()

class S17PredictDemy(SpokenScene):
    def construct(self):
        a=myelin(); self.add(a,nodes())
        self.at('Now strip the myelin'); self.play(FadeOut(a[2]),FadeIn(bare_highlight()),run_time=1.1)
        self.at('What happens'); self.play(FadeIn(demy_stage()[1]),run_time=.4); self.finish()

class S18Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(*demy_stage()); self.wait(float(os.environ['KX_DURATION']))

class S19Demy(SpokenScene):
    def construct(self):
        self.add(myelin(True),nodes(),bare_highlight())
        name=label('run 1: slow',y=2.9,size=34); flow=arrow((0,0),(2,0)); leak=leaks()
        self.at('The bare stretch leaks current'); self.play(FadeIn(name),GrowArrow(flow),FadeIn(leak),run_time=.7)
        self.at('more membrane to charge'); self.play(FadeIn(label('more membrane to charge',y=-2.5,size=30)),flow.animate.set_opacity(.5),run_time=.5)
        # Pause before arrival; result holds >=1.5s even across the closely spaced alternatives.
        self.at('The next node'); self.play(Transform(flow,arrow((0,0),(3.6,0)).set_opacity(.3)),run_time=.45)
        glow=node_glow(4); self.play(FadeIn(glow),run_time=.2); self.wait(1.5)
        self.at('or not at all'); self.play(FadeOut(glow),FadeOut(flow),Transform(name,label('run 2: blocked',y=2.9,size=34)),run_time=.25)
        f=arrow((0,0),(2.4,0)); self.play(GrowArrow(f),run_time=.45)
        self.play(f.animate.scale(.35,about_point=ORIGIN).set_opacity(0),FadeIn(label('no spike',4,-1.95,28)),run_time=.5)
        self.at('Conduction slows or blocks'); self.wait(1.5); self.finish()

class S20Continuous(SpokenScene):
    def construct(self):
        self.add(myelin(True),nodes(),bare_highlight())
        self.at('It does not always block'); self.play(FadeIn(label('Some bare stretches conduct\nslowly and continuously',y=2.8,size=32)),run_time=.5)
        pores=VGroup(*[pore(x,y,color=NA if i%2==0 else K) for i,x in enumerate(np.linspace(1,3,5)) for y in [-1.05,1.05]])
        self.at('the bare stretch develops'); self.play(FadeIn(pores),run_time=.6)
        self.at('sodium and potassium currents'); self.play(FadeIn(label('sodium',.6,-2.05,28,NA)),FadeIn(label('potassium',3.1,-2.05,28,K)),run_time=.5)
        glow=RoundedRectangle(width=.7,height=1.85,corner_radius=.3,color=VOLT,fill_color=VOLT,fill_opacity=.3).move_to([1.2,0,0])
        self.at('Then it conducts slowly'); self.add(glow); self.play(glow.animate.move_to([2.8,0,0]),FadeIn(label('slow: about 1–2 m/s',y=-3,size=30)),run_time=2.4,rate_func=linear); self.finish()

CHECKS=['Overshoot?', 'Threshold?', 'All-or-none?', 'Refractoriness?', 'Travel?']
ANSWERS=['Sodium briefly pulls the balance point\nabove zero', 'Sodium feedback sustains itself',
         'Brief pushes from rest give spikes\nof about the same size',
         'Inactivated sodium channels\nneed time to recover',
         'Current spreads ahead, and refractory\nmembrane behind blocks the way back']

def checklist(done=0):
    g=VGroup()
    for i,name in enumerate(CHECKS):
        y=2.7-i*1.35
        answer=label(ANSWERS[i] if i<done else ' ',size=28)
        answer.move_to([-2.25,y,0],aligned_edge=LEFT)
        g.add(label('✓' if i<done else '○',-6,y,28,TEXT),T(name,28).move_to([-5.6,y,0],aligned_edge=LEFT),answer)
    return g

class S21Recap1(SpokenScene):
    def construct(self):
        c=checklist(); self.add(c); self.at('Back to the puzzles'); self.wait(.1)
        for phrase,n in [('sodium briefly pulls',1),('sodium feedback',2),('brief pushes from rest',3)]:
            self.at(phrase); self.play(Transform(c,checklist(n)),run_time=.45)
        self.finish()

class S22Recap2(SpokenScene):
    def construct(self):
        c=checklist(3); self.add(c)
        self.at('Inactivated sodium channels'); self.play(Transform(c,checklist(4)),run_time=.45)
        self.at('current spreads ahead'); self.play(Transform(c,checklist(5)),run_time=.45); self.finish()

class S23Takeaway(SpokenScene):
    def construct(self):
        self.at('Spread ahead'); self.play(FadeIn(label('Spread ahead, refractory behind.',y=1.1,size=38)),run_time=.5)
        self.at('Wider and myelinated'); self.play(FadeIn(label('Wider and myelinated means faster.',y=-1,size=38)),run_time=.5); self.finish()

class S24End(EndCard):
    def construct(self):
        self.play(FadeIn(label('biochemistrypedia.com',y=0,size=42,color=TEAL)),run_time=.5)
        self.finish()
