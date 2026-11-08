"""Chapter 3. All quantitative traces use the reference Hodgkin–Huxley equations.
COLOR MAP: YELLOW sodium; BLUE potassium; GREEN membrane voltage;
RED inactivation/refractory; TEAL conductance; ORANGE driving force;
GREY axes, membrane, unassigned currents. Water is neutral white.
Clamp plots show baseline-subtracted ionic current, with a finite-rise capacitive
transient Cm*dV/dt displayed separately. These are model illustrations, not data.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

# Keep temporary render diagnostics outside the deliverables directory.
class SpokenScene(SpokenScene):
    def at(self, phrase, lead=0.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > .02:
            self.wait(rest)

ORANGE = "#F29E4C"
NA, K, VOLT, INACT = YELLOW, BLUE, GREEN, RED


# ---------------------------------------------------------------------------------------------
# Hodgkin-Huxley model (the lesson's constants: gNa 120, gK 36, leak 0.3 mS/cm2, Cm 1 uF/cm2, rest -65 mV,
# ENa +50, EK -77; leak reversal -54.4 is the standard value, used only inside the computed trace)
# ---------------------------------------------------------------------------------------------
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


FREE = hh_free()
CLAMP = hh_clamp()
GN_MAX = FREE[:, 2].max()
T_PEAK = FREE[FREE[:, 1].argmax(), 0]
T_MIN = FREE[FREE[:, 1].argmin(), 0]


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
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


def curve(ax, t, v, upto=None, color=VOLT, w=5, stride=8):
    if upto is not None:
        k = int(np.searchsorted(t, upto))
        t, v = t[:k], v[:k]
    t, v = t[::stride], v[::stride]
    m = VMobject(stroke_color=color, stroke_width=w)
    if len(t) >= 2:
        m.set_points_as_corners([ax.P(a, b) for a, b in zip(t, v)])
    return m



def txt(s,x=0,y=0,size=28,color=TEXT):
    return T(s,size,color).move_to([x,y,0])

def arrow(a,b,c=GREY):
    return Arrow(a,b,buff=.08,color=c,stroke_width=5)

def lock(x,y,color=VOLT):
    body=RoundedRectangle(width=.6,height=.48,corner_radius=.06,color=color,fill_opacity=.15).move_to([x,y,0])
    hoop=Arc(radius=.21,start_angle=0,angle=PI,color=color).move_to([x,y+.35,0])
    return VGroup(body,hoop)

def loop():
    p=[[0,2.6,0],[4.1,0,0],[0,-2.6,0],[-4.1,0,0]]
    labels=VGroup(txt('Voltage rises',0,2.6,32,VOLT),
        VGroup(txt('Sodium channels',4.1,.23,28,NA),txt('open',4.1,-.23,28,NA)),
        txt('Sodium flows in',0,-2.6,32,NA),
        VGroup(txt('More',-4.1,.23,28,VOLT),txt('depolarization',-4.1,-.23,28,VOLT)))
    lines=VGroup(*[ArcBetweenPoints(p1,p2,angle=-PI/3,color=GREY,stroke_width=5).add_tip(tip_length=.18)
        for p1,p2 in [([1.8,2.55,0],[4.1,.8,0]),([4.1,-.8,0],[1.9,-2.55,0]),
                     ([-1.9,-2.55,0],[-4.1,-.8,0]),([-4.1,.8,0],[-1.8,2.55,0])]])
    return labels,lines

class Bath:
    def __init__(self,wide=False):
        self.tub=VMobject(color=GREY,stroke_width=7).set_points_as_corners([[-3.8,1.7,0],[-3.4,-1.6,0],[2.6,-1.6,0],[3,1.7,0]])
        self.water=Polygon([-3.6,.5,0],[2.85,.5,0],[2.6,-1.5,0],[-3.4,-1.5,0],color=TEXT,fill_opacity=.12,stroke_width=0)
        self.level=VGroup(DashedLine([-3.6,.5,0],[2.85,.5,0],color=VOLT),txt('target level',.2,.9,26,VOLT))
        self.tap=VMobject(color=GREY,stroke_width=9).set_points_as_corners([[-4,2.8,0],[-2,2.8,0],[-2,1.9,0]])
        self.drain=Rectangle(width=.65 if wide else .28,height=.2,color=BG,fill_opacity=1).move_to([.9,-1.6,0])
        self.inflow=arrow([-2,1.9,0],[-2,.65,0],TEXT).set_stroke(width=12 if wide else 5)
        self.outflow=arrow([.9,-1.65,0],[.9,-2.8,0],TEXT).set_stroke(width=12 if wide else 5)
        self.all=VGroup(self.tub,self.water,self.level,self.tap,self.drain,self.inflow,self.outflow)

def meter(negative=False):
    base=VGroup(Line([5,-1.5,0],[5,2.2,0],color=GREY),Line([4.8,.3,0],[5.2,.3,0],color=GREY),txt('0',5.6,.3,26,GREY),txt('Tap flow',5.3,2.8,26))
    needle=arrow([5,.3,0],[5,-1.1 if negative else 1.8,0],TEXT)
    return base,needle

def clamp_diagram():
    axon=RoundedRectangle(width=7.7,height=2.2,corner_radius=.7,color=GREY,fill_opacity=.12).move_to([1,-1,0])
    wire=VGroup(Line([-2,-1,0],[3.5,-1,0],color=TEXT),Line([-2,-1,0],[-2,1.6,0],color=TEXT))
    amp=chip('Feedback amplifier',GREY,28).move_to([1.1,2.2,0])
    wire.add(Line([-2,1.6,0],[-2,2.2,0],color=TEXT),Line([-2,2.2,0],amp.get_left(),color=TEXT),
        Line(amp.get_right(),[5.7,2.2,0],color=GREY),Line([5.7,2.2,0],[5.7,.25,0],color=GREY))
    electrode=Dot([5.7,.25,0],radius=.08,color=GREY)
    pore=VGroup(Line([1.7,-.22,0],[1.7,.25,0],color=TEAL,stroke_width=9),Line([2.3,-.22,0],[2.3,.25,0],color=TEAL,stroke_width=9))
    return VGroup(axon,wire,amp,txt('squid axon',2.6,-1.65,28),pore,electrode,
        txt('outside electrode',3.8,1.3,26,GREY),txt('channels',2,.7,26,TEAL))

# Shared stage: the command has a 0.05 ms finite rise; all current values
# are baseline-subtracted (including the resting potassium current).
C=hh_clamp(T=12)
CT=C[:,0]+1
INA=-50*C[:,1]; IK=77*C[:,2]
TOTAL=INA+IK+.3*54.4
BASE=-65 # resting voltage for fixed-g calculation
RESTG=hh_clamp(T=.01)[0,1:]
RESTI=RESTG[0]*(-65-50)+RESTG[1]*(-65+77)+.3*(-65+54.4)
TOTAL=TOTAL-RESTI
LOW=5*C[:,1]+IK+.3*54.4-(RESTG[0]*(-65+5)+RESTG[1]*12+.3*(-65+54.4))
PA=Ax(-4.65,5.95,-2.95,1.15,0,13,-1500,2200)
VA=Ax(-4.65,5.95,1.92,2.65,0,13,-70,5)
PR=Ax(-4.65,5.95,-1.35,1.0,0,13,-1500,2200)

def stage(frozen=False,question=False,empty=False):
    pa=PR if question else PA
    axes=VGroup(Line(pa.P(0,-1500),pa.P(0,2200),color=GREY),Line(pa.P(0,0),pa.P(13,0),color=GREY),
        txt('outward',-5.65,pa.Y(900),26,GREY),txt('inward',-5.65,pa.Y(-500),26,GREY),
        txt('µA/cm²',-5.45,pa.Y(2000)+.38,26,GREY))
    for val in [-1000,0,2000]:
        axes.add(Line([pa.x0-.1,pa.Y(val),0],[pa.x0,pa.Y(val),0],color=GREY),
                 txt(str(val).replace('-', '−'),-5.25,pa.Y(val),26,GREY))
    axes.add(txt('time (ms)',5.05,pa.y0-.4,26,GREY))
    for t in [0,2,4,6,8,10,12]:
        axes.add(Line([pa.X(t),pa.y0,0],[pa.X(t),pa.y0-.09,0],color=GREY),txt(str(t),pa.X(t),pa.y0-.28,26,GREY))
    # Time is measured below the plot; the zero-current line stays inside the panel.
    # Put the axis title just above the right-hand end, separate from the numbers.
    axes[11].move_to([5.1,pa.y0+.25 if question else pa.y0-.65,0])
    axes.add(txt('If conductances stayed fixed' if frozen else
                 ('Current ?' if empty else 'Net ionic current · model illustration'),1.8,pa.y1+.27,26,GREY),
        txt('−65 mV',-5.6,VA.Y(-65),26,VOLT),txt('0 mV',-5.5,VA.Y(0),26,VOLT))
    t=np.arange(0,13,.002)
    v=-65+65*np.clip((t-1)/.05,0,1)
    return axes,curve(VA,t,v,stride=1)

def current(low=False,end=13,color=TEXT,axis=None):
    tt=np.r_[0,.999,CT]; yy=np.r_[0,0,LOW if low else TOTAL]
    mask=tt<=end
    return curve(axis or PA,tt[mask],yy[mask],color=color,stride=2)

def captrace(color=TEXT):
    t=np.arange(.95,1.15,.002)
    v=-65+65*np.clip((t-1)/.05,0,1)
    return curve(PA,t,np.gradient(v,t),color=color,stride=1)

def flat():
    jump=(sum(RESTG)+.3)*65
    return DashedVMobject(curve(PA,np.array([0,.999,1,13]),np.array([0,0,jump,jump]),color=TEXT,stride=1),num_dashes=60)

def predict1():
    return VGroup(txt('Pause · fixed conductances',0,3.25,30,TEAL),
                  txt('What does the current do?',1,-1.65,32))

def bath_inset(depleted=True):
    g=VGroup(RoundedRectangle(width=3.1,height=1.35,corner_radius=.15,color=GREY,fill_opacity=.1).move_to([-3.8,-2.5,0]),
        txt('outside bath',-3.8,-2.12,26,GREY),chip('Na+',NA,26).move_to([-4.6,-2.7,0]),
        chip('choline' if depleted else 'Na+',GREY if depleted else NA,26).move_to([-3.2,-2.7,0]))
    return g

def predict2():
    return VGroup(txt('Pause',0,3.25,30,TEAL),txt('Remove most outside sodium',1.7,-2.2,28,NA),
                  txt('What happens to the early current?',1.7,-2.85,28))

def scale_stage():
    ax=Ax(-5.85,5.85,0,1,-80,60,0,1)
    base=VGroup(Line(ax.P(-80,0),ax.P(52,0),color=GREY,stroke_width=10),
        txt('membrane voltage (mV)',-1.7,-.95,30,GREY))
    for v,label,y in [(-77,'E_K  −77',1.05),(-65,'rest  −65',-1.95),(0,'0',-.65),(50,'+50',-.65)]:
        base.add(Line([ax.X(v),-.32,0],[ax.X(v),.32,0],color=K if v==-77 else GREY,stroke_width=5),
                 txt(label,ax.X(v)+(.7 if v< -60 else 0),y,30,K if v==-77 else GREY))
        if v==-65: base.add(Line([ax.X(v),-.4,0],[ax.X(v),-1.6,0],color=GREY,stroke_width=2))
    return ax,base

def ena(ax,v):
    label='E_Na ≈ −5 mV' if v==-5 else ('E_Na  +50 mV' if v==50 else 'E_Na')
    return VGroup(Line([ax.X(v),-.35,0],[ax.X(v),1.65,0],color=NA,stroke_width=11),txt(label,ax.X(v)-.3,2.15,32,NA))


def early_bracket():
    return VGroup(Line(PA.P(1.15,-1370),PA.P(2.7,-1370),color=NA,stroke_width=4),
        Line(PA.P(1.15,-1370),PA.P(1.15,-1200),color=NA),Line(PA.P(2.7,-1370),PA.P(2.7,-1200),color=NA),
        txt('early, inward',PA.X(3.1)+1.55,PA.Y(-1270),26,NA))

def delayed_bracket():
    return VGroup(Line(PA.P(6,1250),PA.P(12,1250),color=K,stroke_width=4),
        Line(PA.P(6,1250),PA.P(6,1470),color=K),Line(PA.P(12,1250),PA.P(12,1470),color=K),
        txt('delayed, outward',PA.X(9),PA.Y(850),26,K))

def reversal_detail():
    # Magnify the net HH current honestly; the small knee is not an isolated Na trace.
    ax=Ax(2,5.8,-2.35,-1.25,1,1.8,0,450)
    mask=(CT>=1)&(CT<=1.8)
    return VGroup(Rectangle(width=5.2,height=2.3,color=GREY,stroke_width=1,fill_color=BG,fill_opacity=1).move_to([3.6,-1.7,0]),
        txt('First 0.8 ms after step',3.75,-.85,26),Line(ax.P(1,0),ax.P(1.8,0),color=GREY),
        Line(ax.P(1,0),ax.P(1,450),color=GREY),
        txt('0',1.65,-2.35,26,GREY),txt('400',1.5,ax.Y(400),26,GREY),txt('µA/cm²',3.5,-1.35,26,GREY),
        txt('1.0',2,-2.65,26,GREY),txt('1.8 ms',5.4,-2.65,26,GREY),
        curve(ax,CT[mask],LOW[mask],color=TEXT,stride=1))

class S00Title(TitleCard):
    TITLE='Holding the Voltage Still'
    LESSON='The Action Potential and Conduction'
    def construct(self):
        g=VGroup(txt('BIOCHEMISTRYPEDIA',size=22,color=TEAL),T(self.LESSON,24,GREY),T(self.TITLE,48,font=TITLE_FONT),Line(LEFT,RIGHT,color=GOLD)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.6); self.finish()

class S01Question(SpokenScene):
    def construct(self):
        ax=Ax(-5.7,5.7,-3,-1.3,0,10,-90,60)
        tr=curve(ax,FREE[:,0],FREE[:,1]).set_stroke(opacity=.3)
        self.add(tr)
        self.at('How do you watch')
        q=VGroup(T('How do you watch',34),T('a conductance change?',40,TEAL)).arrange(DOWN,buff=.3).move_to([0,1.5,0])
        self.play(FadeIn(q),Create(tr),run_time=.6)
        self.at('when the voltage')
        self.play(FadeIn(txt('when the voltage keeps running away?',0,-.3,30)),
            ShowPassingFlash(tr.copy().set_stroke(opacity=1),time_width=.25),run_time=1.3)
        self.finish()


class S02Loop(SpokenScene):
    def construct(self):
        l,a=loop()
        self.at('In a free axon'); self.play(FadeIn(l[0]),run_time=.5)
        self.at('there is a loop'); self.play(Create(a[0]),run_time=.5)
        self.at('Depolarization opens'); self.play(FadeIn(l[1]),Create(a[1]),run_time=.65)
        self.at('and their current'); self.play(FadeIn(l[2]),Create(a[2]),run_time=.5)
        self.at('depolarizes the membrane'); self.play(FadeIn(l[3]),Create(a[3]),run_time=.5)
        self.play(LaggedStart(*[ShowPassingFlash(x.copy().set_color(NA),time_width=.4) for x in a],lag_ratio=.15),run_time=.55)
        self.play(LaggedStart(*[ShowPassingFlash(x.copy().set_color(NA),time_width=.4) for x in a],lag_ratio=.1),run_time=.35)
        self.finish()

class S03Problem(SpokenScene):
    def construct(self):
        l,a=loop(); self.add(l,a)
        self.at('During a free spike')
        self.play(ShowPassingFlash(a.copy().set_color(NA)),run_time=.7)
        self.at('voltage and channel')
        self.play(Indicate(l[0],color=VOLT),Indicate(l[1],color=NA),run_time=.8)
        self.at('To see how')
        self.play(a.animate.set_stroke(opacity=.4).set_fill(opacity=0),FadeIn(chip('Ⅱ  frozen',GREY,28).move_to([0,0,0])),run_time=.5)
        self.at('hold the voltage')
        self.play(FadeIn(lock(0,1.5).scale(1.4)),Create(Line([0,2.15,0],[0,2.4,0],color=VOLT)),run_time=.5)
        self.finish()


class S04Bathtub(SpokenScene):
    def construct(self):
        b=Bath()
        self.at('Picture a leaky'); self.play(Create(b.tub),FadeIn(b.water),Create(b.tap),run_time=.6)
        self.play(FadeIn(b.drain),GrowArrow(b.outflow),run_time=.5)
        self.at('at one exact'); self.play(Create(b.level),run_time=.5)
        self.at('by adjusting'); self.play(GrowArrow(b.inflow),run_time=.6)
        self.finish()

class S05Drain(SpokenScene):
    def construct(self):
        b=Bath(); w=Bath(True); self.add(b.all)
        self.at('If the drain'); self.play(Transform(b.drain,w.drain),Transform(b.outflow,w.outflow),run_time=.7)
        self.at('you run the tap'); self.play(Transform(b.inflow,w.inflow),run_time=.7)
        self.at("The tap's flow"); m,n=meter(); self.play(FadeIn(m),GrowArrow(n),run_time=.6)
        self.at('tells you how'); self.play(FadeIn(txt('tap flow = drain leak',0,-3.25,30)),run_time=.5)
        self.finish()

class S06Crack(SpokenScene):
    def construct(self):
        b=Bath(True); self.add(b.all); m,n=meter(); self.add(m,n)
        # Mask the wall, then replace it with a visible jagged opening.
        gap=Line([2.75,-.65,0],[2.94,.25,0],color=BG,stroke_width=15)
        crack=VMobject(color=TEXT,stroke_width=5).set_points_as_corners([[2.94,.3,0],[2.6,.1,0],[2.9,-.12,0],[2.55,-.35,0],[2.76,-.65,0]])
        incoming=arrow([4.3,-.25,0],[2.1,-.25,0],TEXT)
        self.at('If water pours')
        self.play(FadeOut(b.outflow),Create(gap),Create(crack),GrowArrow(incoming),FadeIn(txt('crack',3.75,-1.1,26)),run_time=.65)
        self.at('the tap must')
        self.play(ReplacementTransform(b.inflow,arrow([-2,.65,0],[-2,1.9,0],TEXT)),Transform(n,meter(True)[1]),run_time=.7)
        self.at('like a pump'); self.play(FadeIn(txt('pump',-2.4,3.3,28)),run_time=.4)
        self.finish()


class S07Clamp(SpokenScene):
    def construct(self):
        # Retain three miniature physical objects from the bathtub analogy.
        def tub_icon(y):
            return VMobject(color=GREY,stroke_width=4).set_points_as_corners(
                [[-6.1,y+.5,0],[-5.9,y-.45,0],[-4.2,y-.45,0],[-4,y+.5,0]])
        icons=VGroup(
            VGroup(tub_icon(2.15),Line([-6,3.1,0],[-4.7,3.1,0],color=TEXT,stroke_width=6),arrow([-4.7,3.1,0],[-4.7,2.4,0],TEXT),txt('tap / pump',-5.1,1.3,26)),
            VGroup(tub_icon(.05),DashedLine([-6,.15,0],[-4.1,.15,0],color=VOLT),txt('water level',-5.1,-.8,26,VOLT)),
            VGroup(tub_icon(-1.9),Line([-5.35,-2.35,0],[-4.95,-2.35,0],color=BG,stroke_width=8),arrow([-5.15,-2.3,0],[-5.15,-2.85,0],TEXT),txt('drain / crack',-5.1,-3.25,26)))
        d=clamp_diagram()
        self.add(icons)
        self.at('The voltage clamp'); self.play(FadeIn(d),run_time=.6)
        self.at('A feedback amplifier')
        self.play(Create(Line([-4.1,2.1,0],d[2].get_left(),color=GREY)),Indicate(d[2],color=TEXT),run_time=.6)
        self.at('holds your chosen')
        read=VGroup(chip('membrane voltage',VOLT,28).move_to([1,-2.6,0]),txt('held at your chosen voltage',1,-3.3,28,VOLT))
        self.play(FadeIn(read),Create(VMobject(color=VOLT,stroke_width=2).set_points_as_corners([[-4.1,.4,0],[-3.3,.4,0],[-3.3,-2.6,0],[-.8,-2.6,0]])),run_time=.5)
        self.at('supplies whatever')
        link=VMobject(color=TEAL,stroke_width=2).set_points_as_corners([[-4,-2.35,0],[-3.3,-2.35,0],[-3.3,1,0],[1.1,1,0],[1.1,.3,0],[2,.3,0]])
        self.play(Create(link),Indicate(d[4],color=TEAL),ShowPassingFlash(d[1].copy().set_color(TEXT)),run_time=.6)
        self.finish()


class S08Capacitor(SpokenScene):
    def construct(self):
        self.add(clamp_diagram())
        self.at('Why does that')
        title=txt('Why does clamp current match channel current?',0,3.3,28)
        self.play(FadeIn(title),run_time=.4)
        self.at('The membrane is')
        plates=VGroup(Line([-4.4,.65,0],[.3,.65,0],color=GREY,stroke_width=14),Line([-4.4,-.65,0],[.3,-.65,0],color=GREY,stroke_width=14))
        labels=VGroup(txt('membrane capacitor',-1.8,3,34),txt('outside',-5.35,1.4,28,GREY),txt('inside',-5.35,-1.4,28,GREY))
        charge=VGroup(*[txt('+',x,1.35,40,VOLT) for x in [-3.8,-2.6,-1.4,-.2]],*[txt('−',x,-1.35,40,VOLT) for x in [-3.8,-2.6,-1.4,-.2]])
        self.play(*[FadeOut(m) for m in list(self.mobjects)],Create(plates),FadeIn(labels),run_time=.6)
        self.at('it takes current')
        eq=txt('capacitive current = Cm × dV/dt',0,-3.05,30)
        rampax=Ax(2,6,-1.1,1.3,0,3,-65,0)
        t=np.linspace(0,1.5,151); v=-65+65*t/1.5
        ramp=curve(rampax,t,v,color=VOLT,stride=1)
        flow=arrow([.85,-1.1,0],[.85,1.1,0],TEXT)
        status=txt('voltage changing',3.8,2.2,26,VOLT)
        self.play(FadeIn(eq),FadeIn(status),GrowArrow(flow),run_time=.3)
        self.at('while the voltage changes')
        self.play(Create(ramp),LaggedStart(*[FadeIn(c) for c in charge],lag_ratio=.07),run_time=1.5,rate_func=linear)
        self.play(FadeOut(flow),FadeOut(status),Create(Line(rampax.P(1.5,0),rampax.P(3,0),color=VOLT,stroke_width=5)),run_time=.45)
        flatlabel=VGroup(txt('voltage flat',5,.35,26,VOLT),txt('→ no current',5,-.15,26,VOLT))
        self.play(FadeIn(flatlabel),run_time=.25)
        self.finish()


class S09Fixed(SpokenScene):
    def construct(self):
        eq=txt('capacitive current = Cm × dV/dt',0,2.45,34); self.add(eq)
        self.at('Hold the voltage fixed')
        self.play(FadeIn(txt('dV/dt = 0',0,1.2,34,VOLT)),run_time=.5)
        self.at('the capacitor takes')
        self.play(FadeOut(eq),run_time=.2)
        self.play(FadeIn(txt('capacitive current = 0',0,2.45,34)),run_time=.25)
        self.at("the amplifier's current")
        arrows=VGroup(arrow([-4.3,-.8,0],[-1.1,-.8,0],TEXT),txt('=',0,-.8,42),arrow([1.1,-.8,0],[4.3,-.8,0],TEXT))
        self.play(FadeIn(arrows),FadeIn(txt('amplifier current',-2.8,-1.7,28)),FadeIn(txt('channel current',2.8,-1.7,28)),run_time=.5)
        self.play(FadeIn(txt('equal size',0,-2.7,30,TEAL)),run_time=.4); self.finish()


class S10Direction(SpokenScene):
    def construct(self):
        # The wire pierces the left end of the axon; the channel crosses its top membrane.
        axon=RoundedRectangle(width=7.8,height=3.2,corner_radius=.4,color=GREY,fill_opacity=.1).move_to([1.6,-.9,0])
        amp=chip('amplifier',GREY,30).move_to([-4.7,-.9,0])
        wire=Line(amp.get_right(),[.7,-.9,0],color=TEXT,stroke_width=5)
        channel=VGroup(Line([2.2,.35,0],[2.2,1.05,0],color=TEAL,stroke_width=9),Line([2.8,.35,0],[2.8,1.05,0],color=TEAL,stroke_width=9))
        self.add(axon,amp,wire,channel,txt('outside',4.6,1.3,28,GREY),txt('inside axon',3.7,-1.8,28,GREY))
        ch=arrow([2.5,-.5,0],[2.5,2.25,0],TEXT).set_stroke(width=8)
        am=arrow([-3.25,-.9,0],[.6,-.9,0],TEXT).set_stroke(width=8)
        chlabel=txt('channel current: OUT',1.6,3.15,30)
        amlabel=txt('amplifier supplies charge',-1.3,-3.1,30)
        self.at('When channel current')
        self.play(GrowArrow(ch),FadeIn(chlabel),run_time=.5)
        self.at('the amplifier supplies')
        self.play(GrowArrow(am),FadeIn(amlabel),run_time=.5)
        self.at('When it flows')
        self.play(FadeOut(am),FadeOut(amlabel),ReplacementTransform(ch,arrow([2.5,2.25,0],[2.5,-.5,0],TEXT).set_stroke(width=8)),
            FadeOut(chlabel),run_time=.5)
        self.play(FadeIn(txt('channel current: IN',1.6,3.15,30)),run_time=.2)
        self.at('the amplifier withdraws')
        self.play(GrowArrow(arrow([.6,-.9,0],[-3.25,-.9,0],TEXT).set_stroke(width=8)),FadeIn(txt('amplifier withdraws charge',-1.3,-3.1,30)),run_time=.5)
        self.finish()


class S11Predict(SpokenScene):
    def construct(self):
        a,v=stage(empty=True); self.add(a)
        self.at('step the voltage'); self.play(Create(v),run_time=.9)
        self.at('If the conductances'); self.play(FadeIn(predict1()),run_time=.6)
        self.finish()

class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(*stage(empty=True),predict1()); self.wait(3)

class S13Flat(SpokenScene):
    def construct(self):
        self.add(*stage(frozen=True)); q=predict1(); self.add(q)
        self.at('It would jump')
        jump=(sum(RESTG)+.3)*65
        tag=txt(f'+{jump:.0f} µA/cm² · steady',2.8,-.3,28)
        self.play(FadeOut(q),Create(flat()),FadeIn(tag),
            GrowArrow(arrow([2.8,-.6,0],PA.P(9,jump),TEXT)),run_time=.8)
        self.finish()

class S14Real(SpokenScene):
    def construct(self):
        a,v=stage(frozen=True); self.add(a,v); f=flat(); self.add(f)
        self.at('Here is what')
        self.play(FadeOut(f),FadeOut(a[-3]),run_time=.2)
        self.play(FadeIn(txt('Net ionic current · model illustration',1.8,PA.y1+.27,26,GREY)),FadeIn(txt('Current at a held voltage',0,3.25,28)),run_time=.35)
        self.at('with inward current'); self.play(Create(current(end=1.15)),Create(captrace()),run_time=1.2)
        self.finish()

class S15Blip(SpokenScene):
    def construct(self):
        self.add(*stage(),current(end=1.15)); c=captrace(); self.add(c)
        self.at('a brief blip'); self.play(Indicate(c,color=TEXT),run_time=.6)
        self.at('the membrane charging'); label=txt('Charging the membrane',0,3.25,28); self.play(FadeIn(label),run_time=.5)
        self.at('set it aside')
        self.play(c.animate.set_color(GREY).set_stroke(opacity=.35),FadeOut(label),run_time=.25)
        self.play(FadeIn(txt('Charging · set aside',0,3.25,28,GREY)),run_time=.25)
        self.finish()

class S16Inward(SpokenScene):
    def construct(self):
        self.add(*stage(),captrace(GREY).set_stroke(opacity=.35),current(end=1.15))
        self.at('an early inward'); self.play(Create(current(end=1.7)),run_time=.7)
        self.at('It grows fast'); self.play(Create(current(end=2.05)),run_time=.6)
        self.at('then dies away'); self.play(Create(current(end=3.4)),run_time=.7)
        self.at('though the voltage'); self.play(FadeIn(txt('Early inward current',0,3.25,30)),run_time=.5)
        self.finish()

class S17Outward(SpokenScene):
    def construct(self):
        self.add(*stage(),captrace(GREY).set_stroke(opacity=.35),current(end=3.4))
        self.at('a delayed outward'); self.play(FadeIn(txt('Delayed outward current',0,3.25,30)),run_time=.5)
        self.at('It rises slowly'); self.play(Create(current()),run_time=1.6)
        self.finish()

class S18Inference(SpokenScene):
    def construct(self):
        eq=VGroup(M('I =',52),M('g',52,color=TEAL),M('×',52),M('(Vm − E)',52,color=ORANGE)).arrange(RIGHT,buff=.35).move_to([0,1.0,0])
        self.add(eq)
        e=txt('E: equilibrium potential',2.4,2.7,28,ORANGE)
        self.at('Here is the key'); self.play(FadeIn(e),Create(Line([2.7,2.35,0],[2.7,1.55,0],color=ORANGE)),run_time=.4)
        force=eq[3]
        bracket=VGroup(Line(force.get_left()+DOWN*.65,force.get_right()+DOWN*.65,color=ORANGE),
            Line(force.get_left()+DOWN*.45,force.get_left()+DOWN*.65,color=ORANGE),
            Line(force.get_right()+DOWN*.45,force.get_right()+DOWN*.65,color=ORANGE))
        self.at('With the voltage')
        self.play(Create(bracket),FadeIn(lock(force.get_x()-.6,-.65,ORANGE)),Create(Line([force.get_x()-.6,.35,0],[force.get_x()-.6,-.05,0],color=ORANGE)),FadeIn(txt('fixed',force.get_x()+.55,-.65,30,ORANGE)),run_time=.5)
        self.at('the driving force')
        self.play(Indicate(bracket,color=ORANGE),run_time=.5)
        self.at('Only the conductance')
        glow=SurroundingRectangle(eq[1],buff=.17,color=TEAL,stroke_width=6)
        self.play(Create(glow),Indicate(eq[1],color=TEAL),FadeIn(txt('can change',eq[1].get_x(),0,30,TEAL)),run_time=.6)
        self.finish()


class S19Inference2(SpokenScene):
    def construct(self):
        card=VGroup(T('Fixed voltage',36,VOLT),T('+ changing current',36),T('= changing conductance',36,TEAL)).arrange(DOWN,buff=.6)
        self.at('So the conductance'); self.play(FadeIn(card),run_time=.5)
        self.at('opening and closing'); self.play(Indicate(card[2],color=TEAL),run_time=.7); self.finish()

class S20Which(SpokenScene):
    def construct(self):
        bath=RoundedRectangle(width=11.8,height=5.1,corner_radius=.4,color=NA,fill_color=NA,fill_opacity=.12).move_to([0,-.1,0])
        membrane=RoundedRectangle(width=9.8,height=2.1,corner_radius=.5,color=GREY,fill_color=BG,fill_opacity=1).move_to([0,-1.15,0])
        ions=VGroup(*[chip('Na+',NA,28).move_to([x,1.25,0]) for x in [-4,-2,0,2,4]])
        self.add(bath,membrane,ions,txt('outside bath',-4,2.0,28,NA),txt('axon',0,-1.15,32))
        self.at('which ions carry'); self.play(FadeIn(txt('Which ions carry these currents?',0,3.2,32)),run_time=.4)
        self.at('replaced most outside')
        replacements=VGroup(*[chip('choline',GREY,26).move_to(ions[i]) for i in range(1,5)])
        self.play(*[FadeOut(ions[i],shift=UP*.15) for i in range(1,5)],run_time=.3)
        self.play(bath.animate.set_color(GREY).set_fill(GREY,opacity=.17),FadeIn(replacements,shift=DOWN*.15),run_time=.75)
        self.at('the membrane passes'); self.play(FadeIn(txt('choline passes poorly',0,-3.1,30)),run_time=.4)
        self.finish()


class S21Predict2(SpokenScene):
    def construct(self):
        inset=bath_inset(False)
        self.add(*stage(question=True),current(axis=PR),inset)
        self.at('If sodium carries'); self.play(FadeIn(predict2()[0]),run_time=.4)
        self.at('what happens when')
        self.play(FadeOut(inset[3]),run_time=.15)
        self.play(FadeIn(bath_inset()[3]),FadeIn(VGroup(*list(predict2())[1:])),run_time=.4)
        self.finish()


class S22Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(*stage(question=True),current(axis=PR),bath_inset(),predict2()); self.wait(3)


class S23Reveal(SpokenScene):
    def construct(self):
        a,v=stage(); self.add(a,v)
        ghost=DashedVMobject(current(color=GREY),num_dashes=80).set_opacity(.75)
        legend=VGroup(DashedLine([-1.1,-.35,0],[-.3,-.35,0],color=GREY),txt('normal sea water',1.4,-.35,26,GREY),
            Line([-1.1,-.95,0],[-.3,-.95,0],color=TEXT),txt('low sodium',1.1,-.95,26))
        self.add(ghost,legend,txt('Low sodium: early current now outward',0,3.25,30))
        self.at('It reversed'); self.play(Create(current(True,end=3.4)),run_time=.6)
        self.at('The early current')
        # Shade the first millisecond and attach a leader to the small early knee.
        shade=Rectangle(width=PA.X(2)-PA.X(1),height=3.8,stroke_width=0,fill_color=NA,fill_opacity=.09).move_to([(PA.X(1)+PA.X(2))/2,-.9,0])
        i=abs(CT-1.45).argmin()
        leader=Arrow([-1.8,.6,0],PA.P(CT[i],LOW[i]),color=NA,buff=.1)
        self.play(FadeIn(shade),GrowArrow(leader),FadeIn(txt('early current now outward',-1.4,.95,26,NA)),
            FadeOut(legend),FadeIn(reversal_detail()),run_time=.6)
        # Keep explicit line-style labels outside the magnified region.
        self.add(txt('– – normal sea water',-1,-1.75,26,GREY),txt('━ low sodium',-.85,-2.35,26))
        self.at('The delayed outward')
        self.play(Create(current(True)),FadeIn(txt('delayed: little affected',3.5,.05,26,GREY)),run_time=1.1)
        self.finish()


class S24WhyReverse(SpokenScene):
    def construct(self):
        ax,b=scale_stage(); mark=ena(ax,50); self.add(b,mark)
        self.at('Less sodium outside'); self.play(FadeIn(txt('Less sodium outside',0,3.2,34,NA)),run_time=.4)
        self.at('equilibrium potential'); self.play(Transform(mark,ena(ax,35)),run_time=1.1)
        self.finish()


class S25Shift(SpokenScene):
    def construct(self):
        ax,b=scale_stage(); mark=ena(ax,35); self.add(b,mark)
        self.at('In the cold'); self.play(FadeIn(txt('Cold squid axon · 6.3 °C',0,3.2,32)),run_time=.4)
        self.at('a tenfold drop')
        self.play(FadeIn(txt('Tenfold fall · about 55 mV shift',0,-2.9,30,NA)),run_time=.4)
        self.at('moves it from')
        self.play(FadeOut(mark[1]),run_time=.15)
        moving=txt('E_Na',ax.X(35)-.3,2.15,32,NA); self.add(moving)
        dx=ax.X(-5)-ax.X(35)
        self.play(mark[0].animate.shift(RIGHT*dx),moving.animate.shift(RIGHT*dx),run_time=2.1,rate_func=smooth)
        self.play(FadeOut(moving),run_time=.15)
        self.play(FadeIn(ena(ax,-5)[1]),run_time=.2)
        self.finish()


class S26Above(SpokenScene):
    def construct(self):
        ax,b=scale_stage(); self.add(b,ena(ax,-5))
        step=VGroup(Dot([ax.X(0),0,0],radius=.1,color=VOLT),txt('held at 0 mV',ax.X(0),2.9,30,VOLT))
        self.at('A step to zero'); self.play(FadeIn(step),run_time=.4)
        self.at('sits above')
        # A close-up makes the five-millivolt interval readable at draft resolution.
        bracket=VGroup(Rectangle(width=4.9,height=2.15,color=GREY,stroke_width=2,fill_color=BG,fill_opacity=1).move_to([3.8,-2.25,0]),
            txt('voltage close-up',3.8,-1.45,26,GREY),
            Line([2,-2.65,0],[5.6,-2.65,0],color=GREY,stroke_width=4),
            Line([2.5,-2.9,0],[2.5,-2.3,0],color=NA,stroke_width=7),
            Line([5.1,-2.9,0],[5.1,-2.3,0],color=VOLT,stroke_width=5),
            DoubleArrow([2.5,-2.1,0],[5.1,-2.1,0],buff=0,color=ORANGE,stroke_width=4),
            txt('+5 mV',3.8,-1.76,28,ORANGE),txt('−5',2.5,-3.12,26,NA),txt('0',5.1,-3.12,26,VOLT))
        self.play(FadeIn(bracket),run_time=.5)
        self.at('So sodium flows')
        cell=VGroup(Line([-2.8,-2.5,0],[2,-2.5,0],color=GREY,stroke_width=10),
            txt('inside',-2,-3.1,26,GREY),txt('outside',-2,-1.95,26,GREY),
            arrow([-.7,-3.25,0],[-.7,-1.65,0],ORANGE),txt('sodium flows OUT',3.1,-2.1,30,NA))
        self.play(FadeOut(bracket),FadeIn(cell),run_time=.5)
        self.at('the early current')
        self.clear()
        a,v=stage()
        self.add(a,v,current(True),reversal_detail(),txt('Early current reverses',0,3.25,32,NA))
        # Opaque inset occupies the quiet lower-left plot region, clear of all axes.
        inset=VGroup(Rectangle(width=4.7,height=1.45,color=GREY,stroke_width=2,fill_color=BG,fill_opacity=1).move_to([-1.65,-2.05,0]),
            Line([-3.65,-2.05,0],[.3,-2.05,0],color=GREY,stroke_width=9),
            txt('inside',-2.8,-2.5,26,GREY),txt('outside',-2.8,-1.6,26,GREY),
            arrow([0,-2.6,0],[0,-1.5,0],ORANGE),txt('Na+ OUT',-.9,-2.5,24,NA))
        self.add(inset)
        i=abs(CT-1.45).argmin()
        self.play(GrowArrow(arrow([-1.5,.3,0],PA.P(CT[i],LOW[i]),NA)),run_time=.4)
        self.finish()


class S27Iv(SpokenScene):
    def construct(self):
        # Peak sodium component from the same HH gates, with complete curves.
        # Both curves fit in the complete plotted voltage and current ranges.
        ax=Ax(-4.55,5.85,-2.5,2.2,-30,52,-2000,2600)
        base=VGroup(Line(ax.P(-30,0),ax.P(52,0),color=GREY),Line(ax.P(-30,-2000),ax.P(-30,2600),color=GREY),
            txt('Peak early sodium current · HH model',0,3.2,30),txt('step voltage (mV)',1,-3.5,28,GREY),
            txt('µA/cm²',-5.45,2.65,26,GREY),txt('outward',-5.55,.8,26,GREY),txt('inward',-5.55,-2.05,26,GREY))
        for v in [-20,0,20,40,50]:
            base.add(Line(ax.P(v,-2000),ax.P(v,-2100),color=GREY),txt(('+' if v>0 else '')+str(v).replace('-', '−'),ax.X(v),-2.97,26,GREY))
        for i in [-2000,0,2000]:
            base.add(txt(str(i).replace('-', '−'),-5.25,ax.Y(i),26,GREY),Line(ax.P(-31,i),ax.P(-30,i),color=GREY))
        vs=np.linspace(-30,52,301)
        peaks=np.array([hh_clamp(v,T=4)[:,1].max() for v in vs])
        norm=DashedVMobject(curve(ax,vs,peaks*(vs-50),color='#F9E99A',stride=1),num_dashes=70)
        self.add(base)
        self.at('Plot the early'); self.play(Create(norm),FadeIn(txt('– – normal sea water',-1.5,2.35,28,'#F9E99A')),run_time=.8)
        self.at('It crosses zero')
        dot=Dot(ax.P(50,0),radius=.1,color=NA)
        label=txt('E_Na +50 mV',4.6,ax.Y(0)+.9,28,NA)
        leader=Line(ax.P(50,0)+UP*.15,label.get_bottom(),color=NA)
        self.play(FadeIn(dot),FadeIn(label),Create(leader),run_time=.5)
        self.at('Low sodium moved')
        self.play(FadeOut(label),run_time=.15)
        # Every intermediate curve and its crossing share the same reversal value.
        reversal=ValueTracker(50)
        shifting=always_redraw(lambda: curve(ax,vs,peaks*(vs-reversal.get_value()),color='#E3B43D',stride=1))
        dot.add_updater(lambda m: m.move_to(ax.P(reversal.get_value(),0)))
        label=txt('E_Na',ax.X(50),ax.Y(0)+.9,28,NA)
        label.add_updater(lambda m: m.move_to([ax.X(reversal.get_value()),ax.Y(0)+.9,0]))
        leader.add_updater(lambda m: m.put_start_and_end_on(ax.P(reversal.get_value(),0)+UP*.15,label.get_bottom()))
        self.add(shifting,label)
        self.play(reversal.animate.set_value(-5),norm.animate.set_stroke(opacity=.6),
            FadeIn(txt('━ low sodium',-1.7,1.7,28,'#E3B43D')),run_time=1.3)
        dot.clear_updaters(); label.clear_updaters(); leader.clear_updaters(); shifting.clear_updaters()
        self.play(FadeOut(label),run_time=.15)
        target=txt('E_Na ≈ −5 mV',ax.X(-5),ax.Y(0)+.9,28,NA)
        leader.put_start_and_end_on(ax.P(-5,0)+UP*.15,target.get_bottom())
        self.play(FadeIn(target),run_time=.2)
        self.finish()


class S28Sodium(SpokenScene):
    def construct(self):
        self.add(*stage(),current())
        self.at('That is just'); self.play(Indicate(current(end=2.8),color=TEXT),run_time=.6)
        self.at('So the early')
        self.play(FadeIn(txt('Early current assigned to Na+',0,3.25,32,NA)),FadeIn(early_bracket()),run_time=.5)
        self.finish()


class S29Potassium(SpokenScene):
    def construct(self):
        self.add(*stage(),current(),early_bracket())
        self.at('The delayed current')
        self.play(FadeIn(txt('Delayed current assigned to K+',0,3.25,32,K)),run_time=.4)
        self.at('assigned to potassium'); self.play(FadeIn(delayed_bracket()),run_time=.4)
        self.at('including tracer')
        self.clear()
        membrane=VGroup(Line([-5.7,0,0],[-1.3,0,0],color=GREY,stroke_width=22),Line([1.3,0,0],[5.7,0,0],color=GREY,stroke_width=22),
            Line([-1.3,-.45,0],[-1.3,.45,0],color=K,stroke_width=12),Line([1.3,-.45,0],[1.3,.45,0],color=K,stroke_width=12))
        self.add(membrane,txt('inside axon',-4,-1.6,28,GREY),txt('outside',-4,1.7,28,GREY),txt('K+ channel',2.6,.7,28,K),
            txt('Potassium leaving stimulated axons',0,3.2,32,K))
        stimulus=chip('stimulus',TEXT,28).move_to([-3.6,-2.85,0])
        self.add(stimulus)
        signal=VMobject(color=TEXT,stroke_width=5).set_points_as_corners([stimulus.get_top(),[-3.6,-1,0],[-1.3,0,0]])
        self.play(ShowPassingFlash(signal,time_width=.7),Flash([-1.3,0,0],color=K,flash_radius=.65),run_time=.65)
        self.at('potassium leaving')
        # A staggered stream repeatedly traverses the pore rather than drifting as a cluster.
        phase=ValueTracker(0)
        dots=VGroup(*[Dot(radius=.12,color=K) for _ in range(18)])
        for i,dot in enumerate(dots):
            dot.add_updater(lambda m,i=i: m.move_to([[-.65,0,.65][i%3],-2.5+(i*5/18+phase.get_value())%5,0]))
            dot.update()
        self.add(dots)
        self.play(phase.animate.set_value(5),run_time=3.2,rate_func=linear)
        for dot in dots: dot.clear_updaters()
        self.finish()


class S30Takeaway(SpokenScene):
    def construct(self):
        self.add(*stage(),current())
        self.at('Early inward current')
        self.play(FadeIn(early_bracket()),FadeIn(txt('Early inward current → Na+',0,3.25,30,NA)),run_time=.4)
        self.at('Delayed outward current')
        self.play(FadeIn(delayed_bracket()),FadeIn(txt('K+',PA.X(9),PA.Y(300),28,K)),run_time=.4)
        self.at('Both change with')
        self.clear()
        card=VGroup(T('Early inward current = Na+',34,NA),T('Delayed outward current = K+',34,K),T('Both change with time',32),T('at a fixed voltage.',32,VOLT)).arrange(DOWN,buff=.55)
        self.add(card); self.play(Indicate(card[2],color=TEXT,scale_factor=1.02),run_time=.4); self.finish()


class S31End(EndCard):
    LINE='Both change with time at a fixed voltage.'
