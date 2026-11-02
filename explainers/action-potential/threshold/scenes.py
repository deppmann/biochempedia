"""Chapter 5: threshold and refractoriness; every physiological trace uses HH equations.

COLOR MAP: YELLOW sodium; BLUE potassium; GREEN membrane voltage;
RED inactivation/refractory; TEAL conductance; ORANGE driving force;
GREY membrane, leak, axes and reference lines. Illustrative current tallies
are explicitly not quantitative HH current measurements.
"""
import os
import numpy as np
from bp_style import *
ORANGE = "#F29E4C"
NA, K, VOLT, INACT = YELLOW, BLUE, GREEN, RED

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

def curve(ax, t, v, upto=None, color=VOLT, w=5, stride=8):
    if upto is not None:
        k = int(np.searchsorted(t, upto))
        t, v = t[:k], v[:k]
    t, v = t[::stride], v[::stride]
    m = VMobject(stroke_color=color, stroke_width=w)
    if len(t) >= 2:
        m.set_points_as_corners([ax.P(a, b) for a, b in zip(t, v)])
    return m


def experiment(T=20., pulses=(), jump=None, gk_max=36., dt=.01, jumps=()):
    """Same HH Euler update as hh_free; add paired stimuli / initial displacement.

    Columns: time, Vm, gNa, gK, h, n, m. A jump changes Vm alone at 1 ms.
    """
    V = -65.
    am,bm,ah,bh,an,bn = _rates(V)
    m,h,n = am/(am+bm), ah/(ah+bh), an/(an+bn)
    out=[]
    jump_steps={round(t/dt):v for t,v in jumps}
    for i in range(round(T/dt)):
        t=i*dt
        if i in jump_steps:
            V=jump_steps[i]
        if jump is not None and i == round(1/dt):
            V=jump
        gna,gk=120*m**3*h,gk_max*n**4
        out.append((t,V,gna,gk,h,n,m))
        I=sum(a for s,d,a in pulses if s <= t < s+d)
        V += dt*(I-gna*(V-50)-gk*(V+77)-.3*(V+54.4))
        am,bm,ah,bh,an,bn=_rates(V)
        m+=dt*(am*(1-m)-bm*m)
        h+=dt*(ah*(1-h)-bh*h)
        n+=dt*(an*(1-n)-bn*n)
    return np.array(out)


SMALL = experiment(T=8,jump=-60)
LARGE = experiment(T=8,jump=-53)
NORMAL = experiment(T=12,pulses=((0,.3,80),))
# Partial K block; no model-specific percentage is asserted on screen.
BLOCKED = experiment(T=12,pulses=((0,.3,80),),gk_max=24.)
COUNTER = experiment(T=8,jump=-58.6)
SECOND = 120.
ABSOLUTE = experiment(T=20,pulses=((1,.5,24),(5,.5,SECOND)))
RELATIVE = experiment(T=20,pulses=((1,.5,24),(9,.5,SECOND)))
INTRO = experiment(T=24,jumps=((1,-60),(9,-62),(17,-53)))


def lab(text,x=0,y=0,size=28,color=TEXT):
    return T(text,size,color).move_to([x,y,0])


def dash(a,b,color=GREY):
    return DashedLine(a,b,color=color,stroke_width=2,dash_length=.10)


def trace(data,ax,color=VOLT,w=4,lo=None,hi=None):
    a=data
    if lo is not None: a=a[a[:,0]>=lo]
    if hi is not None: a=a[a[:,0]<=hi]
    # A ruler panel ends at 0 mV; stop the computed curve at its upper edge.
    a=a[(a[:,1]>=ax.v0)&(a[:,1]<=ax.v1)]
    return curve(ax,a[:,0],a[:,1],color=color,w=w,stride=2)


BIG = Ax(-5.1,5.6,-2.6,2.35,0,15,-85,55)
PAIR = Ax(-5.0,2.6,-2.55,2.3,0,20,-80,55)
MINI = Ax(1.1,5.25,-2.6,2.65,0,8,-68,0)
TEA_AX = Ax(-5.1,5.5,-2.6,2.4,0,12,-80,55)


def axes(ax):
    g=VGroup(Line(ax.P(ax.t0,ax.v0),ax.P(ax.t0,ax.v1),color=GREY),
             Line(ax.P(ax.t0,ax.v0),ax.P(ax.t1,ax.v0),color=GREY),
             dash(ax.P(ax.t0,-65),ax.P(ax.t1,-65)))
    for v in [-65,0]:
        if ax.v0<=v<=ax.v1:
            g.add(lab(str(v).replace('-', '−'),ax.x0-.52,ax.Y(v),26,GREY))
    g.add(lab('Vm (mV)',ax.x0+.35,ax.y1+.42,26,GREY),
          lab('time (ms)',ax.x1-.65,ax.y0-.76,26,GREY))
    for t in [ax.t0,(ax.t0+ax.t1)/2]:
        g.add(lab(str(int(t)),ax.X(t),ax.y0-.32,26,GREY))
    return g


def ruler(target=-60,leak=False):
    g=axes(MINI)
    levels=[(-60,'−60',GREY),(-53,'−53',GREY)] if not leak else [(-60,'−60',GREY)]
    for v,name,c in levels:
        g.add(dash(MINI.P(0,v),MINI.P(8,v),c),lab(name,5.85,MINI.Y(v),26,c))
    if leak:
        # Keep the -60 number on its own line; the equilibrium has a short ruler.
        y=MINI.Y(-54.4)
        g.add(DashedLine(MINI.P(0,-54.4),MINI.P(6,-54.4),color=GREY,
                         stroke_width=3,dash_length=.22),
              lab('E_leak ≈ −54',3.7,y+.42,26,GREY),
              Line(MINI.P(1,-60),MINI.P(1,-54.4),color=GREY,stroke_width=3),
              Line(MINI.P(.7,-54.4),MINI.P(1.3,-54.4),color=GREY,stroke_width=3))
    return g


def pore(x,y=0,state='open',color=NA):
    walls=VGroup(Line([x-.16,y-.25,0],[x-.16,y+.25,0],color=color,stroke_width=6),
                 Line([x+.16,y-.25,0],[x+.16,y+.25,0],color=color,stroke_width=6))
    if state=='open':
        gate=Line([x+.2,y-.22,0],[x+.43,y-.22,0],color=INACT if color==NA else color,stroke_width=5)
    else:
        gate=Line([x-.16,y-.18,0],[x+.16,y-.18,0],color=INACT if state=='inactivated' else color,stroke_width=6)
    return VGroup(walls,gate)


def channel_row(n=2,total=6):
    spacing=4.1/(total-1)
    return VGroup(*[pore(-5.65+j*spacing,1.55,'open' if j<n else 'closed') for j in range(total)])


def channel_legend():
    g=VGroup()
    for x,state in [(-5.5,'open'),(-3.7,'closed'),(-1.65,'inactivated')]:
        g.add(pore(x,-2.65,state).scale(.65),lab(state,x,-3.2,26,INACT if state=='inactivated' else NA))
    return g


def voltage_chip(v):
    return chip(f'{v} mV'.replace('-', '−'),VOLT,28).move_to([-3.35,.55,0])


def arrow(amount,y,color):
    return Arrow([-5.8,y,0],[-5.8+amount*.63,y,0],buff=0,color=color,stroke_width=7,tip_length=.18)


def tally(v=-60,n=2,opposing=True,leak=False):
    base=VGroup(lab('Illustrative current units',-3.35,2.85,28,GREY),
                voltage_chip(v),Line([-6,1.55,0],[-.75,1.55,0],color=GREY,stroke_width=8),
                channel_row(n),channel_legend(),ruler(v,leak))
    ina=VGroup(arrow(n,-.55,NA),lab(f'Na+ inward: {n}',-3.25,-.12,28,NA))
    opp=VGroup(arrow(4 if n==6 else 3,-1.65,K),
               lab(f'K+ + leak outward: {4 if n==6 else 3}',-3.25,-1.23,26,K))
    return base,ina,opp


def net_label(inward=True):
    return lab('net inward' if inward else 'net: 1 outward',-2.4,-2.12,28,NA if inward else GREY)


def side_gates(shut=4):
    row=VGroup(lab('Na+ channels',4.5,2.5,28,NA),lab('slow (inactivation) gate',4.55,1.9,26,GREY))
    row.add(VGroup(*[pore(x,y,'inactivated' if i<shut else 'open')
        for i,(x,y) in enumerate([(3.9,1.0),(5.1,1.0),(3.9,.1),(5.1,.1)])]))
    row.add(pore(3.5,-1.0,'open'),lab('open',4.8,-1,26,NA),
            pore(3.5,-1.85,'inactivated'),lab('shut',4.8,-1.85,26,INACT))
    return row


def pulse_marks(ax,second):
    g=VGroup()
    for t,strong in [(1,False),(second,True)]:
        x=ax.X(t)
        g.add(Arrow([x,-3.35 if strong else -3.05,0],[x,ax.Y(-80)+.1,0],buff=0,
                    color=INACT if strong else GREY,stroke_width=6 if strong else 3,tip_length=.13))
    g.add(lab('push',ax.X(1)+.48,-3.18,26,GREY),
          lab('strong push',ax.X(second)+.95,-3.37,26,INACT))
    return g


def first_reference():
    d=experiment(T=9,pulses=((1,.5,24),)); d[:,0]+=8
    return DashedVMobject(trace(d,PAIR,color=GREY,w=2),num_dashes=55).set_opacity(.65)


def tea_question():
    normal=DashedVMobject(trace(NORMAL,TEA_AX,color=GREY,w=3),num_dashes=70)
    return VGroup(axes(TEA_AX),normal,trace(NORMAL,TEA_AX,color=K,lo=1.1,hi=3.4,w=7),
        lab('What happens to the falling phase?',0,3.25,32),
        pore(3.3,1.3,'open',K),chip('TEA',K,28).move_to([4.65,1.3,0]),
        lab('Block K+ channels',3.9,.4,28,K))


def tea_stage():
    return VGroup(axes(TEA_AX),DashedVMobject(trace(NORMAL,TEA_AX,color=GREY,w=3),num_dashes=85),
                  lab('normal: dashed',-2.5,3.28,26,GREY),lab('K+ blocked: solid',2.5,3.28,26,K))


def ramp_data():
    """Voltage ramp under clamp; boundary from free HH trials at each gate state."""
    dt=.05;V=-65.;am,bm,ah,bh,an,bn=_rates(V)
    m,h,n=am/(am+bm),ah/(ah+bh),an/(an+bn)
    rows=[];bounds=[]
    def fires(v0,state):
        v=v0;mm,hh,nn=state
        for j in range(1000):
            v+=.01*(-120*mm**3*hh*(v-50)-36*nn**4*(v+77)-.3*(v+54.4))
            if v>0: return True
            am,bm,ah,bh,an,bn=_rates(v)
            mm+=.01*(am*(1-mm)-bm*mm);hh+=.01*(ah*(1-hh)-bh*hh);nn+=.01*(an*(1-nn)-bn*nn)
        return False
    for i in range(601):
        t=i*dt;V=-65+.4*t
        rows.append((t,V,h,n))
        if i%20==0:
            lo,hi=-65.,0.
            for j in range(12):
                mid=(lo+hi)/2
                if fires(mid,(m,h,n)): hi=mid
                else: lo=mid
            bounds.append((t,hi))
        am,bm,ah,bh,an,bn=_rates(V)
        m+=dt*(am*(1-m)-bm*m);h+=dt*(ah*(1-h)-bh*h);n+=dt*(an*(1-n)-bn*n)
    return np.array(rows),np.array(bounds)


def threshold_value():
    lo,hi=-60.,-53.
    for _ in range(16):
        mid=(lo+hi)/2
        if experiment(T=12,jump=mid)[:,1].max()>0: hi=mid
        else: lo=mid
    return hi


THRESHOLD=threshold_value()


def recovery_data():
    rows=[]
    for gap in np.unique(np.r_[np.arange(0,6.8,.2),np.arange(6.8,12.01,.025),np.arange(12.2,30.01,.2)]):
        d=experiment(T=gap+12,pulses=((1,.5,24),(1+gap,.5,SECOND)))
        v=d[:,1]; inds=np.where((v[1:-1]>v[:-2])&(v[1:-1]>=v[2:]))[0]+1
        # Exclude the first AP and any pulse-evoked graded bump below 0 mV.
        inds=[i for i in inds if d[i,0]>max(4.5,gap+1.1) and v[i]>0]
        rows.append((gap,max([v[i]+65 for i in inds],default=0)))
    return np.array(rows)


class S00Title(TitleCard):
    LESSON='The Action Potential and Conduction'
    TITLE='Threshold and Refractoriness'


class S01Question(SpokenScene):
    def construct(self):
        ax=Ax(-5.1,5.6,-2.6,2.4,0,24,-70,45)
        self.add(axes(ax),lab('Why does a slightly bigger nudge fire?',0,3.25,32))
        for t in [1,9,17]:
            self.add(Arrow([ax.X(t),-3.35,0],ax.P(t,-65),buff=0,
                           color=NA,stroke_width=7,tip_length=.17))
        self.at('Why does a')
        self.play(Create(trace(INTRO,ax,hi=16,w=6)),run_time=1.65)
        self.at('while a slightly')
        self.play(Create(trace(INTRO,ax,lo=16,w=6)),run_time=2.0)
        self.finish()


class S02Nudge(SpokenScene):
    def construct(self):
        b,_,_=tally(-65,0);_,i,o=tally(-60,2);self.add(b)
        self.at('Nudge the membrane')
        self.play(Transform(b[1],voltage_chip(-60)),Create(trace(SMALL,MINI,hi=1.02)),run_time=2.9)
        self.at('A few sodium')
        self.play(LaggedStart(*[Transform(b[3][j],channel_row(2)[j]) for j in range(2)],lag_ratio=.55),run_time=1.65)
        self.at('a little sodium')
        self.play(GrowArrow(i[0]),FadeIn(i[1]),run_time=1.4)
        self.finish()


class S03Tally1(SpokenScene):
    def construct(self):
        b,i,o=tally(leak=True);self.add(b,i,trace(SMALL,MINI,hi=1.02))
        ka=VGroup(arrow(3.6,-1.65,K),lab('K+ outward',-3.25,-1.23,28,K))
        leak=VGroup(Arrow([-.9,-2.15,0],[-1.6,-2.15,0],buff=0,color=GREY),lab('leak inward',-3.4,-2.15,26,GREY))
        self.at('Potassium current flows')
        self.play(GrowArrow(ka[0]),FadeIn(ka[1]),run_time=1.7)
        self.at('Leak is still')
        self.play(GrowArrow(leak[0]),FadeIn(leak[1]),run_time=1.0)
        self.at('below its equilibrium')
        self.play(Indicate(b[5][-1],color=GREY),run_time=1.4)
        self.at('Together they give')
        self.play(ReplacementTransform(ka,o),FadeOut(leak),run_time=1.5)
        self.finish()


class S04Tally1b(SpokenScene):
    def construct(self):
        b,i,o=tally();self.add(b,i,o,trace(SMALL,MINI,hi=1.02))
        self.at('Net current is')
        self.play(FadeIn(net_label(False)),run_time=1.3)
        self.at('so the voltage')
        self.play(Create(trace(SMALL,MINI,lo=1.02)),run_time=2.25)
        self.at('Nothing happens')
        self.play(Indicate(Dot(MINI.P(7.5,SMALL[-1,1]),color=VOLT)),run_time=.6)
        self.finish()


class S05Nudge2(SpokenScene):
    def construct(self):
        b,_,_=tally(-65,0);_,i,o=tally(-53,6);self.add(b)
        self.at('Now nudge')
        self.play(Transform(b[1],voltage_chip(-53)),Create(trace(LARGE,MINI,hi=1.02)),run_time=2.8)
        self.at('More sodium channels')
        self.play(LaggedStart(*[Transform(b[3][j],channel_row(6)[j]) for j in range(6)],lag_ratio=.14),
                  GrowArrow(i[0]),FadeIn(i[1]),run_time=1.5)
        self.at('inward current beats')
        self.play(GrowArrow(o[0]),FadeIn(o[1]),FadeIn(net_label()),run_time=1.3)
        self.finish()


class S06Feedback(SpokenScene):
    def construct(self):
        b,i,o=tally(-53,6);self.add(b,i,o,net_label(),trace(LARGE,MINI,hi=1.02))
        self.at('The voltage rises')
        self.play(Create(trace(LARGE,MINI,lo=1.02,hi=2)),run_time=1.1)
        self.at('which opens still')
        # Add representative available pores as the feedback recruits more channels.
        self.play(Transform(b[3],channel_row(8,8)),
                  Create(CurvedArrow([-5.95,.5,0],[-5.95,1.3,0],angle=-PI/2,color=NA)),
                  Create(CurvedArrow([-.85,1.3,0],[-.85,.5,0],angle=-PI/2,color=NA)),run_time=1.9)
        self.at('Inward current grows')
        self.play(Transform(i[0],arrow(7.3,-.55,NA)),Transform(i[1],lab("Na+ inward: grows",-3.25,-.12,28,NA)),run_time=1.0)
        self.at('faster than potassium')
        self.play(Transform(i[0],arrow(8,-.55,NA)),Transform(o[0],arrow(4.8,-1.65,K)),Transform(o[1],lab("K+ + leak outward: grows",-3.25,-1.23,26,K)),
                  Create(trace(LARGE,MINI,lo=2,hi=3)),run_time=2.2)
        self.add(lab('↑ spike continues',4.1,2.65,26,VOLT))
        self.finish()


class S07Define(SpokenScene):
    def construct(self):
        self.add(ruler(),trace(LARGE,MINI,hi=3),lab('↑ spike continues',4.1,2.65,26,VOLT))
        self.at('That is threshold')
        y=MINI.Y(THRESHOLD)
        self.play(FadeIn(lab('Threshold',-3.3,2.8,40)),Create(dash(MINI.P(0,THRESHOLD),MINI.P(8,THRESHOLD),NA)),
                  FadeIn(lab('threshold',-1.0,y+.35,28,NA)),run_time=.9)
        self.add(Line([.0,y+.35,0],MINI.P(0,THRESHOLD),color=NA))
        self.at('sodium feedback sustains')
        self.play(FadeIn(lab('Sodium feedback\nsustains itself',-3.4,.5,32,NA)),run_time=1.5)
        self.at('the rise runs')
        self.play(Indicate(trace(LARGE,MINI,lo=1.6,hi=2.8),color=VOLT),run_time=1)
        self.finish()


class S08NotNet(SpokenScene):
    def construct(self):
        ax=Ax(1.3,5.6,-2.6,2.4,0,8,-68,0)
        na=arrow(3,-.2,NA);opp=arrow(2,-1.5,K)
        labels=VGroup(lab('Na+ inward',-3.1,.3,30,NA),lab('K+ + leak outward',-3.1,-1,28,K))
        title=lab('Inward now: enough?',-2.9,2.4,32)
        initial=trace(COUNTER,ax,hi=3.8); tail=trace(COUNTER,ax,lo=3.8)
        counter=lab('Opposing current outgrows it',-2.9,-2.45,27,INACT)
        self.add(axes(ax),na,opp,labels,title)
        self.at('Inward current at')
        self.play(Create(initial),run_time=1.3)
        self.at('is not enough')
        self.play(Transform(opp,arrow(4.5,-1.5,K)),Create(tail),FadeIn(counter),run_time=1.65)
        self.at('What matters is')
        self.play(FadeOut(counter),FadeOut(initial),FadeOut(tail),
                  Transform(title,lab("Can inward excess persist?",-2.9,2.4,30)),
                  Transform(na,arrow(3,-.2,NA)),Transform(opp,arrow(2,-1.5,K)),run_time=.45)
        self.at('sodium keeps outgrowing')
        self.play(Transform(na,arrow(8,-.2,NA)),Transform(opp,arrow(4,-1.5,K)),Create(trace(LARGE,ax,hi=3)),
                  FadeIn(lab('Sustained inward excess',-2.9,-2.45,28,NA)),run_time=2.3)
        self.finish()


class S09Moves(SpokenScene):
    def construct(self):
        ax=Ax(-5.1,5.5,-2.55,1.55,0,30,-68,-35);r,b=ramp_data()
        self.add(Line(ax.P(0,-68),ax.P(0,-35),color=GREY),Line(ax.P(0,-68),ax.P(30,-68),color=GREY),
                 lab('−65',-5.65,ax.Y(-65),26,GREY),lab('time (ms)',4.8,-3.25,26,GREY),
                 lab('Threshold can move',0,3.3,34))
        def boundary_at(end):
            # Draw only the elapsed portion: no flat continuation ahead of it.
            end=max(1.,end)
            t=b[b[:,0]<=end,0]
            return DashedVMobject(curve(ax,t,np.interp(t,b[:,0],b[:,1]),
                                       color=GREY,stride=1,w=3),num_dashes=max(3,int(end*2)))
        boundary=boundary_at(0)
        ramp=curve(ax,r[:201,0],r[:201,1],stride=1)
        th_label=lab('threshold',4.8,ax.Y(b[0,1])+.35,28,GREY)
        self.add(boundary,lab(f'{b[0,1]:.0f}'.replace('-','−'),-5.65,ax.Y(b[0,1]),26,GREY),
                 th_label)
        row=VGroup(*[pore(x,2.4) for x in [-3.8,-2.8,-1.8,-.8]])
        kp=pore(3.3,2.4,'closed',K)
        self.add(row,kp,lab('Na+: slow gate open → shut',-2.8,1.8,26,INACT),lab('K+',4.2,2.4,28,K))
        self.at('So threshold is')
        self.play(Indicate(boundary),run_time=1.4)
        self.at('A slow depolarization')
        self.play(Create(ramp),Transform(boundary,boundary_at(10)),
                  th_label.animate.move_to([4.8,ax.Y(np.interp(10,b[:,0],b[:,1]))+.35,0]),run_time=1.25)
        self.at('inactivates sodium channels')
        self.play(LaggedStart(*[Transform(row[i],pore(x,2.4,'inactivated')) for i,x in enumerate([-3.8,-2.8,-1.8,-.8])],lag_ratio=.3),
                  Transform(ramp,curve(ax,r[:401,0],r[:401,1],stride=1)),Transform(boundary,boundary_at(20)),
                  th_label.animate.move_to([4.8,ax.Y(np.interp(20,b[:,0],b[:,1]))+.35,0]),run_time=1.5)
        self.at('opens potassium channels')
        self.play(Transform(kp,pore(3.3,2.4,'open',K)),FadeIn(lab('opens',5.3,2.4,26,K)),
                  Transform(ramp,curve(ax,r[:,0],r[:,1],stride=1)),Transform(boundary,boundary_at(30)),
                  th_label.animate.move_to([4.8,ax.Y(b[-1,1])+.35,0]),run_time=.85)
        self.at('raising it')
        self.play(Indicate(boundary),run_time=.5)
        self.add(Line(ax.P(29.5,b[-1,1]),ax.P(30.3,b[-1,1]),color=GREY),
                 lab(f'{b[-1,1]:.0f}'.replace('-','−'),6.05,ax.Y(b[-1,1]),26,GREY))
        self.wait(2.6)
        self.finish()


class S10AllOrNone(SpokenScene):
    def construct(self):
        self.add(axes(BIG),lab('Size is set by channels and equilibrium potentials',0,3.43,30),
                 lab('not the stimulus',0,2.92,28))
        self.at('Once the rise')
        self.play(Create(trace(LARGE,BIG,hi=3.2)),run_time=1.9)
        self.at('the spike runs')
        self.play(Create(trace(LARGE,BIG,lo=3.2)),run_time=1.6)
        self.at('Its size is')
        self.play(Create(VGroup(Line(BIG.P(5.8,-65),BIG.P(5.8,40),color=VOLT),
                  Line(BIG.P(5.5,40),BIG.P(6.1,40),color=VOLT),Line(BIG.P(5.5,-65),BIG.P(6.1,-65),color=VOLT))),
                  FadeIn(lab('size set here',.8,.1,28,VOLT)),run_time=.6)
        self.at('the channels')
        self.play(FadeIn(pore(3.3,.9)),FadeIn(lab('channels',4.7,.9,28,NA)),run_time=.65)
        self.at('the equilibrium potentials')
        self.play(Create(dash(BIG.P(0,50),BIG.P(15,50),NA)),FadeIn(lab('E_Na = +50',3.4,BIG.Y(50)-.3,26,NA)),
                  Create(dash(BIG.P(0,-77),BIG.P(15,-77),K)),FadeIn(lab('E_K = −77',3.5,BIG.Y(-77)+.75,26,K)),run_time=1)
        self.finish()


class S11AllOrNone2(SpokenScene):
    def construct(self):
        ax=Ax(-5.1,5.6,-2.55,2.1,0,10,-80,55)
        a=hh_free(T=10,stim=(1,.3,24));b=hh_free(T=10,stim=(1,.3,80))
        self.add(axes(ax),lab('All-or-none',0,3.35,40))
        self.at('With brief pushes')
        self.play(Create(trace(a,ax)),FadeIn(lab('small brief push: solid',2.6,1.6,27,VOLT)),FadeIn(lab('small',-4.95,-3.25,26,VOLT)),
                  GrowArrow(Arrow([ax.X(1),-3.1,0],[ax.X(1),-2.6,0],color=VOLT,buff=0)),run_time=1.2)
        self.at('a bigger push')
        self.play(Create(DashedVMobject(trace(b,ax,color=NA),num_dashes=95)),FadeIn(lab('large brief push: dashed',2.6,.8,27,NA)),FadeIn(lab('large',-2.95,-3.35,26,NA)),
                  GrowArrow(Arrow([ax.X(1)+.2,-3.4,0],[ax.X(1)+.2,-2.6,0],color=NA,buff=0)),run_time=1.8)
        self.at('Its size stays')
        self.play(FadeIn(lab('Similar heights; earlier with a bigger push',0,2.65,28)),run_time=1.1)
        self.at('That is all')
        self.play(Indicate(self.mobjects[1]),run_time=.7)
        self.finish()


class S12Absolute(SpokenScene):
    def construct(self):
        row=side_gates(0);self.add(axes(PAIR),row,pulse_marks(PAIR,5),lab('Absolute refractory: no second spike',0,3.35,32,INACT))
        self.at('Right after a')
        self.play(Create(trace(ABSOLUTE,PAIR,hi=3.2)),run_time=1.1)
        self.play(Create(trace(ABSOLUTE,PAIR,lo=3.2,hi=5)),Transform(row,side_gates(4)),run_time=.9)
        self.at('most inactivation gates')
        self.play(Indicate(row[2],color=INACT),run_time=1.5)
        self.at('No stimulus')
        self.play(Indicate(pulse_marks(PAIR,5)[1],color=INACT),run_time=1.2)
        self.at('fires a second')
        inset=Ax(-1.5,2.15,.1,1.35,4.8,7.5,-78,-55)
        self.play(Create(trace(ABSOLUTE,PAIR,lo=5)),run_time=1.2)
        self.add(lab('Graded bump: enlarged',.3,1.8,24),
                 Line(inset.P(4.8,-78),inset.P(4.8,-55),color=GREY),
                 lab('−55',-2.02,inset.Y(-55),22,GREY),
                 lab('−78',-2.02,inset.Y(-78),22,GREY),
                 trace(ABSOLUTE,inset,lo=4.8,hi=7.5,w=5))
        self.at('the absolute refractory')
        self.play(Indicate(row[2],color=INACT),run_time=1)
        self.wait(2.5)
        self.finish()


class S13Relative(SpokenScene):
    def construct(self):
        row=side_gates(4);self.add(axes(PAIR),row,trace(RELATIVE,PAIR,hi=9),pulse_marks(PAIR,9),
                                 first_reference(),lab('Relative refractory',0,3.35,36,INACT))
        self.at('As those gates')
        self.play(LaggedStart(*[Transform(row[2][i],side_gates(1)[2][i]) for i in [3,2,1]],lag_ratio=.65),run_time=2.0)
        self.at('a stronger stimulus')
        self.play(Indicate(pulse_marks(PAIR,9)[1],color=INACT),run_time=.8)
        self.at('can fire a')
        self.play(Create(trace(RELATIVE,PAIR,lo=9)),run_time=1.1)
        self.at('often a smaller')
        self.play(FadeIn(lab('smaller',.7,1.6,28,VOLT)),
                  Create(Line([-.1,1.55,0],PAIR.P(RELATIVE[RELATIVE[:,0]>9][np.argmax(RELATIVE[RELATIVE[:,0]>9,1]),0],RELATIVE[RELATIVE[:,0]>9,1].max()),color=VOLT)),run_time=.7)
        self.at('the relative refractory')
        self.play(Indicate(row[2][0],color=INACT),run_time=1)
        self.finish()


class S14RelativeWhy(SpokenScene):
    def construct(self):
        gates=VGroup(lab('Na+ slow gates',4.5,2.35,28,NA),
                     pore(3.8,1.45,'inactivated'),pore(5.2,1.45,'open'),
                     lab('shut',3.8,.88,26,INACT),lab('open',5.2,.88,26,NA))
        self.add(axes(PAIR),gates,trace(RELATIVE,PAIR),pulse_marks(PAIR,9),first_reference(),
                 lab('Why a stronger push?',0,3.35,36))
        self.at('A stronger push')
        self.play(Indicate(pulse_marks(PAIR,9)[1],color=INACT),run_time=1.3)
        self.at('some sodium channels')
        self.play(FadeIn(lab('Some Na+ still\ninactivated',4.5,-.05,28,INACT)),
                  Indicate(gates[1],color=INACT),run_time=1.5)
        self.at('potassium conductance is',lead=0)
        self.play(FadeIn(pore(4.5,-1.0,'open',K)),
                  FadeIn(lab('K+ conductance\nstill raised',4.5,-2.05,28,K)),run_time=.45)
        self.finish()


class S15Full(SpokenScene):
    def construct(self):
        d=recovery_data();ax=Ax(-4.9,5.6,-2.25,2.2,0,20,0,115)
        onset=d[d[:,1]>0][0,0]
        self.add(lab('Second-spike height above rest (mV)',0,3.4,32),
                 lab('Same strong second push at every interval',0,2.85,26,GREY))
        for lo,hi,col in [(0,onset,INACT),(onset,14,NA),(14,20,VOLT)]:
            self.add(Rectangle(width=ax.X(hi)-ax.X(lo),height=4.45,stroke_width=0,fill_color=col,fill_opacity=.10).move_to([(ax.X(lo)+ax.X(hi))/2,-.025,0]))
        self.add(Line(ax.P(0,0),ax.P(20,0),color=GREY),Line(ax.P(0,0),ax.P(0,115),color=GREY),
                 lab('0',-5.4,-2.25,26,GREY),lab('100',-5.55,ax.Y(100),26,GREY),
                 lab('interval between pushes (ms)',.5,-3.3,28,GREY),
                 lab('absolute:\nno spike',-3.0,-.8,26,INACT),lab('relative:\nsmaller; needs\nstronger push',.3,-.8,26,NA),
                 lab('full size again',3.6,.6,28,VOLT))
        for t in [0,4,8,12,16,20]: self.add(lab(str(t),ax.X(t),-2.65,26,GREY))
        # Magnify the computed rising stretch without inventing a smooth spike onset.
        zoom=Ax(-4.05,-1.65,.1,1.65,7,12,75,110)
        recovered=d[(d[:,0]>=onset)&(d[:,0]<=12)]
        detail=VGroup(
            Rectangle(width=3.35,height=2.45,stroke_color=GREY,stroke_width=1,
                      fill_color=BG,fill_opacity=1).move_to([-3.12,1.03,0]),
            lab('Relative: enlarged',-3.05,2.02,22,NA),
            Line(zoom.P(7,75),zoom.P(12,75),color=GREY),
            Line(zoom.P(7,75),zoom.P(7,110),color=GREY),
            lab('80',-4.45,zoom.Y(80),22,GREY),
            lab('110',-4.45,zoom.Y(110),22,GREY),
            lab('7',zoom.X(7),-.12,22,GREY),lab('12 ms',zoom.X(12),-.12,22,GREY),
            curve(zoom,recovered[:,0],recovered[:,1],stride=1,w=4))

        self.at('At long intervals')
        self.play(Create(curve(ax,d[d[:,0]<=20,0],d[d[:,0]<=20,1],stride=1)),run_time=1.1)
        for gap,name in [(4,'4 ms'),(8,'8 ms')]:
            height=d[np.argmin(abs(d[:,0]-gap)),1]
            self.add(Dot(ax.P(gap,height),radius=.085,color=TEXT),lab(name,ax.X(gap)+.4,ax.Y(height)+.3,26))
        self.at('full size again')
        self.add(detail)
        self.play(Indicate(trace_recovery := curve(ax,d[(d[:,0]>=onset)&(d[:,0]<=12),0],
                         d[(d[:,0]>=onset)&(d[:,0]<=12),1],stride=1,color=NA,w=6)),run_time=.5)
        self.remove(trace_recovery)
        self.wait(.7)
        self.finish()


class S16PredictTea(SpokenScene):
    def construct(self):
        q=tea_question();self.add(*q[:4])
        self.at('One more question')
        self.play(Indicate(q[2],color=K),run_time=.8)
        self.at('Block the potassium')
        self.play(FadeIn(q[4:]),run_time=1.7)
        self.at('What happens to')
        self.play(Indicate(q[2],color=K),run_time=1.2)
        self.finish()


class S17Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(tea_question(),lab('Pause',3.8,-.6,42,TEAL))
        # Keep the question still; an unobtrusive time bar marks the three-second pause.
        self.add(Line([2.3,-1.3,0],[5.3,-1.3,0],color=GREY,stroke_width=6))
        self.play(Create(Line([2.3,-1.3,0],[5.3,-1.3,0],color=TEAL,stroke_width=7)),
                  run_time=float(os.environ.get('KX_DURATION','3')),rate_func=linear)


class S18Tea(SpokenScene):
    def construct(self):
        self.add(tea_stage());peak=BLOCKED[BLOCKED[:,1].argmax(),0]
        self.at('From the same')
        self.play(FadeIn(Dot(TEA_AX.P(0,-65),radius=.09,color=K)),run_time=1.3)
        self.at('the rise is')
        self.play(Create(trace(BLOCKED,TEA_AX,color=K,hi=peak)),run_time=1.3)
        self.at('The fall is')
        self.play(Create(trace(BLOCKED,TEA_AX,color=K,lo=peak,hi=9)),run_time=1.2)
        self.at('relying on')
        self.play(FadeIn(lab('inactivation + leak',2.5,.7,28,INACT)),run_time=1.1)
        self.at('so the spike')
        self.play(FadeIn(lab('broader spike',-.3,1.5,30,K)),
                  Create(Line([-1.9,1.5,0],TEA_AX.P(1.8,np.interp(1.8,BLOCKED[:,0],BLOCKED[:,1])),color=K)),run_time=1.0)
        self.finish()


class S19Tea2(SpokenScene):
    def construct(self):
        self.add(tea_stage(),trace(BLOCKED,TEA_AX,color=K,hi=9))
        self.at('The undershoot is')
        self.play(Create(trace(BLOCKED,TEA_AX,color=K,lo=9)),run_time=1.0)
        # Bracket each actual computed minimum, with a magnified tail inset.
        inset=Ax(.2,5.4,-.6,1.8,3,12,-77,-74.5)
        self.add(lab('Undershoot: enlarged',2.8,2.25,28),
                 Line(inset.P(3,-77),inset.P(3,-74.5),color=GREY),
                 lab('−75',-.4,inset.Y(-75),26,GREY),lab('−77',-.4,inset.Y(-77),26,GREY),
                 DashedVMobject(trace(NORMAL,inset,color=GREY,lo=3),num_dashes=50),trace(BLOCKED,inset,color=K,lo=3))
        a=NORMAL[NORMAL[:,1].argmin()];b=BLOCKED[BLOCKED[:,1].argmin()]
        x=inset.X(7)
        self.play(Create(VGroup(Line([x,inset.Y(a[1]),0],[x,inset.Y(b[1]),0],color=K,stroke_width=5),
                  dash(inset.P(a[0],a[1]),[x,inset.Y(a[1]),0]),
                  dash(inset.P(b[0],b[1]),[x,inset.Y(b[1]),0],K),
                  Dot(inset.P(a[0],a[1]),radius=.06,color=GREY),
                  Dot(inset.P(b[0],b[1]),radius=.06,color=K))),
                  FadeIn(lab('shallower undershoot',2.8,-1.25,28,K)),run_time=.65)
        self.add(Line([2.8,-1,0],[x,inset.Y(b[1]),0],color=K))
        self.at('raised potassium conductance')
        self.play(Indicate(trace(BLOCKED,inset,color=K,lo=3),color=K),run_time=1.3)
        self.finish()


class S20Takeaway(SpokenScene):
    def construct(self):
        def thumb(data,y):
            ax=Ax(-5.9,-2.6,y-.6,y+.6,0,float(data[-1,0]),-80,55)
            return VGroup(Line(ax.P(0,-65),ax.P(ax.t1,-65),color=GREY),trace(data,ax))
        self.add(lab('Three things to keep',0,3.25,38))
        self.at('Threshold is sodium')
        self.play(Create(thumb(LARGE,1.8)),FadeIn(lab('Threshold: sodium feedback\nsustains itself',1.6,1.8,30,NA)),run_time=1.8)
        self.at('Inactivation makes refractoriness')
        self.play(Create(thumb(RELATIVE,0)),FadeIn(lab('Inactivation makes\nrefractoriness',1.6,0,30,INACT)),run_time=1.8)
        self.at('Blocking potassium broadens')
        ax=Ax(-5.9,-2.6,-2.4,-1.2,0,12,-80,55)
        self.play(Create(thumb(BLOCKED,-1.8)),Create(DashedVMobject(trace(NORMAL,ax,color=GREY),num_dashes=35)),
                  FadeIn(lab('Blocking K+ broadens\nthe spike',1.6,-1.8,30,K)),run_time=1.8)
        self.finish()


class S21End(EndCard):
    LINE='Sodium feedback sustains spikes;\ninactivation makes refractoriness.'
