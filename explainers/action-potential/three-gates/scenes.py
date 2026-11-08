"""Three Gates, One Spike — word-synchronised functional cartoons.
COLOR MAP: yellow sodium; blue potassium; green Vm; red inactivation;
           teal conductance; orange driving force; grey axes/membrane.
The required series colour map takes precedence over orange/purple in two visual notes.
All traces and balance/current markers derive from the reference HH equations.
"""
import numpy as np
from bp_style import *
ORANGE = "#F29E4C"
NA, K, VOLT, INACT = YELLOW, BLUE, GREEN, RED

_plain_T = T

def T(text,size=30,color=TEXT,font=FONT,**kw):
    if 'gₙₐ' in text or 'gₖ' in text:
        return MarkupText(text.replace('gₙₐ','g<sub>Na</sub>').replace('gₖ','g<sub>K</sub>'),font=font,font_size=size,color=color,**kw)
    return _plain_T(text,size,color,font=font,**kw)

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


# Same reference equations; a 0.5 ms, 20 µA/cm² pulse gives the narration's
# rounded +40 mV peak and ~12-fold sodium/potassium conductance ratio.
FREE = hh_free(stim=(0.5, 0.5, 20.0))
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


# Shared geometry keeps successive shots registered.
def trace(ax, t, values, color, end=None, width=5):
    keep = (t <= ax.t1) if end is None else (t <= min(end, ax.t1))
    ids = np.where(keep)[0][::3]
    mob = VMobject(stroke_color=color, stroke_width=width)
    if len(ids)>1: mob.set_points_as_corners([ax.P(t[i],values[i]) for i in ids])
    return mob


def heading(txt, color=TEXT):
    return T(txt,30,color).move_to([0,3.45,0])


def arrow(a,b,color,width=6):
    return Arrow(a,b,buff=0,color=color,stroke_width=width,
        max_stroke_width_to_length_ratio=20,max_tip_length_to_length_ratio=.16)


def pore(fast=False,slow=True,potassium=False,mini=False):
    col=K if potassium else NA
    walls=VGroup(*[Line([-5.9,y,0],[5.9,y,0],color=GREY,stroke_width=12) for y in [-2.1,2.1]])
    xs=[0] if potassium else [-2.5,1.5]
    def door(x,opened,c):
        return Line([x,2.1,0],[x+4.2,2.1,0] if opened else [x,-2.1,0],color=c,stroke_width=18)
    gates=VGroup(door(0,fast,K)) if potassium else VGroup(door(-2.5,fast,NA),door(1.5,slow,INACT))
    names=['one slow gate'] if potassium else ['activation gate','inactivation gate']
    labels=VGroup(*[T(name,28,K if potassium else [NA,INACT][i]).move_to([x,-2.65,0]) for i,(x,name) in enumerate(zip(xs,names))])
    if mini:
        VGroup(walls,gates).scale(.40).move_to([3.55,1.65,0])
        labels=VGroup(T('activation',26,NA).move_to([2.4,.48,0]),T('inactivation',26,INACT).move_to([4.65,.48,0]))
    return VGroup(walls,gates,labels)


def gate_target(gate,opened):
    pivot=gate.get_start(); length=gate.get_length()
    return Line(pivot,pivot+([length,0,0] if opened else [0,-length,0]),color=gate.get_color(),stroke_width=gate.get_stroke_width())


def stream(scene,color=NA,seconds=1.5,mini=False):
    # An evenly spaced train remains inside the pore throughout the motion.
    x0,x1,y=(-5.2,5.2,0) if not mini else (1.5,5.6,1.65)
    phase=ValueTracker(0)
    count=6 if not mini else 3
    ions=VGroup(*[chip('K+' if color==K else 'Na+',color,26,pad=.09) for _ in range(count)])
    for i,ion in enumerate(ions):
        ion.add_updater(lambda m,i=i:m.move_to([x0+((i/count+phase.get_value())%1)*(x1-x0),y,0]))
    scene.add(ions)
    scene.play(phase.animate.set_value(.65),run_time=seconds,rate_func=linear)
    for ion in ions: ion.clear_updaters()
    scene.remove(ions)


VA=Ax(-4.9,5.6,.10,3.10,0,5,-85,55)
GA=Ax(-4.9,5.6,-2.3,-.15,0,5,0,42)
PK=int(FREE[:,1].argmax())
# Zero of ionic current gives dV/dt=0 after the stimulus; interpolate the
# adjacent numerical samples so the balance and voltage markers coincide.
BAL=(FREE[:,2]*50+FREE[:,3]*(-77)+.3*(-54.4))/(FREE[:,2]+FREE[:,3]+.3)
D=BAL-FREE[:,1]
i=np.where((FREE[:-1,0]>1)&(D[:-1]>0)&(D[1:]<=0))[0][0]
PEAK=float(FREE[i,0]+(FREE[i+1,0]-FREE[i,0])*D[i]/(D[i]-D[i+1]))
RISE=float(FREE[np.where(FREE[:,1]>-20)[0][0],0])
EARLY=PEAK+.65
CROSS=float(FREE[np.where((FREE[:,0]>PEAK)&(FREE[:,3]>FREE[:,2]))[0][0],0])
UNDER=float(FREE[FREE[:,1].argmin(),0])


def sample(t):
    return [float(np.interp(t,FREE[:,0],FREE[:,i])) for i in range(1,4)]


def railx(v): return -4.8+(v+77)/127*9.6


def stage(scene,t,show_ghost=True,peak_zoom=True):
    global VA,GA
    # Early scenes use 5 ms; expand to 8 ms before the undershoot sequence.
    extent=8 if t>=CROSS-.19 else 5
    VA=Ax(-4.9,5.6,.10,3.10,0,extent,-85,55)
    GA=Ax(-4.9,5.6,-2.3,-.15,0,extent,0,42)
    clock=ValueTracker(t)
    axes=VGroup(Line(VA.P(0,-85),VA.P(0,55),color=GREY),Line(GA.P(0,0),GA.P(0,42),color=GREY),Line(GA.P(0,0),GA.P(GA.t1,0),color=GREY))
    for v,c in [(50,NA),(0,GREY),(-65,GREY),(-77,K)]:
        axes.add(always_redraw(lambda v=v,c=c:DashedLine(VA.P(0,v),VA.P(clock.get_value(),v),color=c,stroke_opacity=.25)))
    labels=VGroup(T('E_Na +50',26,NA).move_to([-5.85,VA.Y(50),0]),T('0 mV',26,GREY).move_to([-5.85,VA.Y(0),0]),T('−65',26,GREY).move_to([-5.65,VA.Y(-65)+.12,0]),T('E_K −77',26,K).move_to([-5.85,VA.Y(-77)-.18,0]),T('Vm',26,VOLT).move_to([-5.8,2.35,0]),T('g',28,TEAL).move_to([-5.65,-.75,0]),T('mS/cm²',22,TEAL).move_to([-5.75,-1.15,0]),T('40',26,GREY).move_to([-5.4,GA.Y(40),0]),T('0',26,GREY).move_to([-5.35,GA.y0,0]))
    ticks=[0,1,2,3,4,5] if extent==5 else [0,2,4,6,8]
    for tt in ticks: labels.add(T(str(tt)+' ms' if tt==extent else str(tt),26,GREY).move_to([GA.X(tt),-2.57,0]))
    curves=VGroup(*[always_redraw(lambda ax=ax,col=col,j=j:trace(ax,FREE[:,0],FREE[:,j],col,clock.get_value())) for ax,col,j in [(VA,VOLT,1),(GA,NA,2),(GA,K,3)]])
    if abs(t-PEAK)<1e-7:
        # The real cursor stays at dV/dt=0; a faint model segment reveals the rounded apex.
        ids=(FREE[:,0]>=PEAK-.18)&(FREE[:,0]<=PEAK+.35)
        scene.add(trace(VA,FREE[ids,0],FREE[ids,1],VOLT,width=5).set_stroke(opacity=.32))
    # Panel-specific cursors never run through titles, legends or unit labels.
    cursor=always_redraw(lambda:VGroup(DashedLine(VA.P(clock.get_value(),-85),VA.P(clock.get_value(),55),color=GREY,stroke_opacity=.4),DashedLine(GA.P(clock.get_value(),0),GA.P(clock.get_value(),42),color=GREY,stroke_opacity=.4),Dot(VA.P(clock.get_value(),sample(clock.get_value())[0]),radius=.075,color=VOLT)))
    def curve_labels():
        tt=clock.get_value(); _,gn,gk=sample(tt)
        x=min(GA.X(tt)+.75,6.05)
        yn,yk=max(GA.Y(gn)+.12,GA.y0+.24),max(GA.Y(gk)+.12,GA.y0+.24)
        # Keep the leaders at the actual endpoints, separate the labels vertically.
        if abs(yn-yk)<.55:
            low=max(GA.y0+.24,(yn+yk)/2-.32)
            if gn>=gk: yn,yk=low+.64,low
            else: yn,yk=low,low+.64
        return VGroup(*[VGroup(Line(GA.P(tt,value),[x-.30,y,0],color=col,stroke_width=1.5),T(name,26,col).move_to([x,y,0]).set_z_index(5)) for value,y,col,name in [(gn,yn,NA,'Na+'),(gk,yk,K,'K+')]])
    direct=always_redraw(curve_labels)
    def ropes():
        _,gn,gk=sample(clock.get_value()); b=float(np.interp(clock.get_value(),FREE[:,0],BAL)); x=railx(b)
        # Same multiplier on both widths: the visible ratio is the conductance ratio.
        return VGroup(Line([-4.8,-3.05,0],[x,-3.05,0],color=K,stroke_width=max(.6,2*gk)),Line([x,-3.05,0],[4.8,-3.05,0],color=NA,stroke_width=max(.6,2*gn)))
    ghost=always_redraw(lambda:Circle(radius=.15,color=TEXT,stroke_width=3).move_to([railx(float(np.interp(clock.get_value(),FREE[:,0],BAL))),-3.05,0]))
    real=always_redraw(lambda:Dot([railx(sample(clock.get_value())[0]),-3.05,0],radius=.075,color=TEAL))
    key=VGroup(T('○ balance point',26,TEXT).move_to([-2.2,-3.55,0]),T('● Vm',26,TEAL).move_to([1.6,-3.55,0]))
    scene.add(axes,labels,curves,cursor,direct,always_redraw(ropes),T('E_K −77',26,K).move_to([-5.6,-3.05,0]),T('E_Na +50',26,NA).move_to([5.65,-3.05,0]),ghost,real,key)
    if peak_zoom and abs(t-PEAK)<1e-7:
        v,gn,gk=sample(PEAK)
        scene.add(T('K+ conductance · zoom',26,K).move_to([3.35,-.45,0]))
        for x,value,label in [(2.5,FREE[0,3],'rest'),(4.2,gk,'peak')]:
            scene.add(Line([x,-1.9,0],[x,-1.9+value*.28,0],color=K,stroke_width=18),T(label,26,K).move_to([x,-2.12,0]))
        scene.add(T(f'{gk:.1f}',26,K).move_to([5,-1.3,0]))
    return clock,ghost,key,curves


def progress(scene,clock,target,seconds=1): scene.play(clock.animate.set_value(target),run_time=seconds,rate_func=linear)


def note(text,color=TEXT,y=1.6):
    return T(text,28,color).move_to([3.0,y,0]).add_background_rectangle(color=BG,opacity=1,buff=.07)


def peak_reasons():
    return VGroup(note('K+ and leak stay open',K,2.65),
        VGroup(note('Inactivation is lowering gₙₐ',INACT,1.95),note('(since the rise)',INACT,1.43)),
        note('gₖ raised (since the rise)',K,.70))


def question():
    return VGroup(T('Pause and think',28,TEAL),T('Why does the peak stop',32),T('short of +50 mV?',32,NA)).arrange(DOWN,buff=.23).move_to([3.1,1.55,0])


def feedback(x=3.0,y=1.5,positive=True):
    color=NA if positive else INACT
    texts=['More depolarization','More gates open','More sodium in'] if positive else ['Depolarization','Inactivation','K+ gates open']
    nodes=VGroup(*[chip(v,color if positive else [VOLT,INACT,K][i],26,pad=.14) for i,v in enumerate(texts)])
    nodes[0].move_to([x,y+1.08,0]); nodes[1].move_to([x,y,0]); nodes[2].move_to([x,y-1.08,0])
    if positive:
        edges=VGroup(arrow(nodes[0].get_bottom(),nodes[1].get_top(),color,3),arrow(nodes[1].get_bottom(),nodes[2].get_top(),color,3),
            VMobject(color=color,stroke_width=3).set_points_as_corners([nodes[2].get_right(),[x+2.5,y-1.08,0],[x+2.5,y+1.08,0],nodes[0].get_right()+RIGHT*.6]),
            arrow(nodes[0].get_right()+RIGHT*.6,nodes[0].get_right(),color,3))
    else:
        nodes[1].move_to([x-1.35,y-.65,0]); nodes[2].move_to([x+1.35,y-.65,0])
        edges=VGroup(arrow(nodes[0].get_bottom()+LEFT*.4,nodes[1].get_top(),INACT,3),arrow(nodes[0].get_bottom()+RIGHT*.4,nodes[2].get_top(),K,3),
            arrow(nodes[1].get_left(),nodes[0].get_left(),INACT,3),arrow(nodes[2].get_right(),nodes[0].get_right(),K,3))
    return VGroup(edges,nodes,T('+' if positive else '−',36,color).move_to([x+1.9,y,0]))


class S00Title(TitleCard):
    TITLE='Three Gates, One Spike'
    LESSON='The Action Potential and Conduction'


class S01Question(SpokenScene):
    def construct(self):
        a=Ax(-5.3,-.5,-2.3,2.4,0,7.5,-1600,2200); b=Ax(.8,5.6,-2.3,2.4,0,7.5,-1600,2200)
        title=heading('Two currents after a voltage step'); self.add(title,T('Current (µA/cm²)',26).move_to([0,2.9,0]))
        for ax,col,name in [(a,NA,'Na+ inward'),(b,K,'K+ outward')]:
            self.add(Line(ax.P(0,-1600),ax.P(0,2200),color=GREY),Line(ax.P(0,0),ax.P(7.5,0),color=GREY),T('0',26,GREY).move_to([ax.x0-.25,ax.Y(0),0]),T(name,28,col).move_to([(ax.x0+ax.x1)/2,-2.8,0]),arrow([ax.x0,-3.5,0],[ax.x0,-2.95,0],TEAL,4))
        self.add(T('Voltage step at 0 ms · time →',26,TEAL).move_to([0,-3.5,0]),trace(b,CLAMP[:,0],CLAMP[:,2]*77,K).set_stroke(opacity=.2))
        self.at('Sodium conductance'); self.play(Create(trace(a,CLAMP[:,0],CLAMP[:,1]*(-50),NA)),run_time=2)
        self.at('Potassium turns'); self.play(Create(trace(b,CLAMP[:,0],CLAMP[:,2]*77,K)),run_time=1.8)
        self.at('What channel'); self.play(FadeOut(title),run_time=.15); self.play(FadeIn(heading('What channel does that?')),run_time=.25); self.finish(); self.wait(1.2)


class S02Processes(SpokenScene):
    def construct(self):
        ax=Ax(-5.2,4.8,-2.4,2.5,0,7.5,0,1)
        self.add(heading('Three processes · same time axis'),Line(ax.P(0,0),ax.P(7.5,0),color=GREY),Line(ax.P(0,0),ax.P(0,1),color=GREY),T('Gate variable: 0 to 1',26).move_to([-3.2,2.9,0]),T('Time after voltage step (ms)',28).move_to([0,-3.3,0]))
        for tt in [0,2,4,6]: self.add(T(str(tt),26,GREY).move_to([ax.X(tt),-2.75,0]))
        for i,name,col,cue,yy in [(0,'fast sodium activation',NA,'fast sodium activation',2.85),(2,'slower inactivation',INACT,'slower sodium inactivation',-1.6),(4,'slow potassium activation',K,'slow potassium activation',.8)]:
            a,b=_rates(0)[i:i+2]; aa,bb=_rates(-65)[i:i+2]; vals=a/(a+b)+(aa/(aa+bb)-a/(a+b))*np.exp(-(a+b)*CLAMP[:,0])
            self.at(cue); self.play(Create(trace(ax,CLAMP[:,0],vals,col)),FadeIn(T(name,28,col).move_to([1.7,yy,0])),run_time=.6)
        self.finish()


class S03NaChannel(SpokenScene):
    def construct(self):
        p=pore(); self.add(heading('Sodium channel · cartoon',NA),p[0])
        self.at('two gates'); self.play(Create(p[1]),run_time=.5)
        self.at('like two doors'); self.play(FadeIn(p[2]),run_time=.3); self.finish()


class S04Activation(SpokenScene):
    def construct(self):
        p=pore(); title=heading('At rest · activation gate shut',NA); self.add(p,title)
        self.at('snaps open'); self.play(Transform(p[1][0],gate_target(p[1][0],True)),Transform(title,heading('Depolarization · activation gate opens',VOLT)),run_time=.25); self.finish()


class S05Inactivation(SpokenScene):
    def construct(self):
        p=pore(); title=heading('At rest · inactivation gate open',INACT); self.add(p,title)
        self.at('shuts several'); self.play(Transform(p[1][0],gate_target(p[1][0],True)),run_time=.15)
        self.play(Transform(p[1][1],gate_target(p[1][1],False)),Transform(title,heading('Inactivation gate shuts slowly',INACT)),run_time=1.2); self.finish()


class S06Window(SpokenScene):
    def construct(self):
        p=pore(); status=heading('Sodium channel · cartoon',NA); self.add(p,status)
        self.at('Sodium passes'); self.play(Transform(p[1][0],gate_target(p[1][0],True)),run_time=.2)
        self.at('both are open'); self.play(Transform(status,heading('Both open · Na+ flows in',NA)),run_time=.2)
        stream(self,seconds=1.65)
        self.at('before the slow'); self.play(Transform(p[1][1],gate_target(p[1][1],False)),Transform(status,heading('Slow gate shut · flow stops',INACT)),run_time=.8)
        timeline=VGroup(Line([-3,-3.2,0],[3,-3.2,0],color=GREY),Line([-2,-3.05,0],[-2,-3.35,0],color=NA),Line([1,-3.05,0],[1,-3.35,0],color=NA),T('Brief window in time →',26,NA).move_to([0,-3.65,0]))
        self.play(FadeIn(timeline),run_time=.3); self.finish()


class S07KChannel(SpokenScene):
    def construct(self):
        p=pore(potassium=True,slow=False); status=heading('Potassium channel · cartoon',K); self.add(p,status,T('Squid delayed potassium channel',28,K).move_to([0,2.75,0]))
        self.at('delayed potassium channel'); self.play(Transform(status,heading('Depolarization · gate lags, then opens',K)),run_time=.2)
        self.at('behaves as if'); self.play(Transform(p[1][0],gate_target(p[1][0],True)),run_time=1)
        self.at('one slow gate'); self.play(Transform(status,heading('One slow gate · K+ flows out →',K)),run_time=.2); stream(self,K,2.7)
        self.play(FadeOut(status),run_time=.2); self.play(FadeIn(heading('Voltage falls: gate closes slowly',K)),Transform(p[1][0],gate_target(p[1][0],False)),run_time=1.4); self.wait(.8); self.finish()


class S08Caveat(SpokenScene):
    def construct(self):
        p=pore(fast=True); self.add(heading('This is a cartoon'),p)
        self.at('track the three processes'); self.play(p.animate.set_stroke(opacity=.45),run_time=.3)
        rows=VGroup(*[T(t,36,c) for t,c in [('m = sodium activation',NA),('h = not inactivated',INACT),('n = potassium activation',K)]]).arrange(DOWN,buff=.7)
        for i,cue in enumerate(['m','h','n']):
            self.at(cue)
            if i==0: self.remove(p)
            self.play(FadeIn(rows[i]),run_time=.2)
        self.finish()


class S09Powers(SpokenScene):
    def construct(self):
        def formula(ion,variable,power,col,x):
            g=T('g',54,col); sub=T(ion,28,col); core=T(' ∝ '+variable,54,col); exp=T(power,30,col)
            group=VGroup(g,sub,core,exp).arrange(RIGHT,buff=.07).move_to([x,2.1,0]); sub.shift(DOWN*.2); exp.shift(UP*.35)
            if ion=='Na': group.add(T('h',54,col).next_to(exp,RIGHT,buff=.08).shift(DOWN*.35))
            group.scale(1.25); return group,exp
        na,e1=formula('Na','m','3',NA,-3); kk,e2=formula('K','n','4',K,3); self.add(na,kk)
        c1=Circle(.27,color=TEXT).move_to(e1); c2=Circle(.27,color=TEXT).move_to(e2)
        self.at('Their powers'); self.play(Create(c1),Create(c2),run_time=.3)
        label=T('Fitted to the S-shaped onset',30).move_to([0,.6,0])
        self.at('fitted to the data'); self.play(FadeIn(label),Create(Line(c1.get_bottom(),[-1,.9,0],color=GREY)),Create(Line(c2.get_bottom(),[1,.9,0],color=GREY)),run_time=.3)
        ax=Ax(-3,3,-2.7,-.1,0,7.5,0,36); self.add(Line(ax.P(0,0),ax.P(7.5,0),color=GREY),trace(ax,CLAMP[:,0],CLAMP[:,2],K),T('n⁴ onset · time →',26,K).move_to([3.7,-2.4,0]))
        self.at('not counted from gates'); self.play(FadeIn(T('Not a gate count',36,TEXT).move_to([0,-3.35,0])),run_time=.3); self.finish()


class S10Setup(SpokenScene):
    def construct(self):
        clock,_,_,_=stage(self,.02); self.add(heading('Let the axon run free'))
        self.at('Now let the axon run free'); progress(self,clock,1.1,1.2)
        self.at('A ghost marker'); self.play(Indicate(self.mobjects[-4],color=TEXT),run_time=.5); self.finish()


class S11Rise(SpokenScene):
    def construct(self):
        clock,_,_,_=stage(self,1.1); p=pore(mini=True); self.add(p,heading('1 · The rise',VOLT))
        self.at('Activation gates open'); self.play(Transform(p[1][0],gate_target(p[1][0],True)),run_time=.25)
        self.at('sodium flows in'); stream(self,seconds=.7,mini=True)
        self.at('inside gets more positive'); progress(self,clock,RISE,.9)
        self.at('That opens more gates'); self.play(Indicate(p[1][0],color=NA),run_time=.5); self.finish()


class S12Feedback(SpokenScene):
    def construct(self):
        clock,_,_,_=stage(self,RISE); loop=feedback(); self.add(loop,heading('Positive feedback',NA))
        self.at('Sodium conductance soon'); progress(self,clock,PEAK-.25,1.3)
        self.at('The balance point leaps'); progress(self,clock,PEAK-.15,1.4)
        self.at('the voltage races'); progress(self,clock,PEAK-.10,1); self.finish()


class S13RiseSlow(SpokenScene):
    def construct(self):
        clock,_,_,_=stage(self,PEAK-.10); p=pore(fast=True,mini=True); self.add(p,heading('Slow processes begin during the rise'))
        self.at('Inactivation is already developing')
        gate=p[1][1]; pivot=gate.get_start(); length=gate.get_length()
        self.play(Transform(gate,Line(pivot,pivot+[length*.7,-length*.7,0],color=INACT,stroke_width=12)),run_time=.9)
        self.at('potassium gates start to open')
        self.play(FadeIn(note('K+ gates opening · gₖ zoom',K,-.45)),run_time=.3)
        zoom=Ax(2.0,5.0,-1.7,-.85,PEAK-.4,PEAK,0,3)
        keep=FREE[:,0]>=PEAK-.4
        self.add(Line(zoom.P(PEAK-.4,0),zoom.P(PEAK,0),color=GREY),always_redraw(lambda:trace(zoom,FREE[keep,0],FREE[keep,3],K,clock.get_value())),T('during the rise →',26,K).move_to([3.5,-2.03,0]))
        progress(self,clock,PEAK-.02,.8); self.finish()


class S14PredictPeak(SpokenScene):
    def construct(self):
        stage(self,PEAK-.02); self.add(heading('Predict the peak'),question()); self.at('Why does the spike'); self.play(Indicate(question(),scale_factor=1.02),run_time=.4); self.finish()


class S15Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; stage(self,PEAK-.02); self.add(heading('Predict the peak'),question())
        for i in range(7,0,-1):
            n=T(str(i),38,TEAL).move_to([2.6,-.4,0]); self.add(n); self.wait(1); self.remove(n)


class S16Peak(SpokenScene):
    def construct(self):
        _,_,key,_=stage(self,PEAK); self.remove(key); self.add(heading('2 · The peak · dV/dt = 0',VOLT))
        self.at('meets the balance point'); self.play(Create(Circle(.24,color=TEAL).move_to([railx(sample(PEAK)[0]),-3.05,0])),run_time=.4)
        v,gn,gk=sample(PEAK); ina=gn*abs(v-50); out=gk*abs(v+77)+.3*abs(v+54.4); x=railx(v)
        self.at('inward sodium current'); self.play(GrowArrow(arrow([x,-3.45,0],[4.8,-3.45,0],NA,ina/20)),FadeIn(T('Na+ → +50',22,NA).move_to([5.55,-3.55,0])),run_time=.4)
        self.at('equals outward potassium'); self.play(GrowArrow(arrow([x,-3.45,0],[-4.8,-3.45,0],K,out/20)),FadeIn(T('K+ + leak → −77',22,K).move_to([-.8,-3.75,0])),FadeIn(note('Equal currents at the peak',TEXT,2)),FadeIn(note('Width ∝ g × |Vm − E|',ORANGE,1.3)),run_time=.4); self.finish()


class S17PeakG(SpokenScene):
    def construct(self):
        stage(self,PEAK); self.add(heading('2 · The peak',VOLT))
        v,gn,gk=sample(PEAK)
        self.at('Sodium still has'); self.play(FadeIn(note('gₙₐ ≈ 12 × gₖ (model)',NA,2.35)),run_time=.3)
        # Numeric bracket exposes the small K conductance on the common scale.
        self.add(note(f'gₙₐ {gn:.1f} · gₖ {gk:.1f} mS/cm²',TEAL,1.7))
        self.at('its pull is weak'); self.play(FadeIn(note('Small Na+ driving force',ORANGE,.8)),run_time=.3)
        self.add(Line([railx(v),.25,0],[railx(50),.25,0],color=ORANGE,stroke_width=8),T('driving force',26,ORANGE).move_to([3.6,-.1,0])); self.finish()


class S18PeakWhy(SpokenScene):
    def construct(self):
        stage(self,PEAK); self.add(heading('Why below +50 mV?')); rows=peak_reasons()
        self.at('Potassium and leak'); self.play(FadeIn(rows[0]),run_time=.3)
        self.at('inactivation lowers sodium conductance'); self.play(FadeIn(rows[1]),run_time=.3)
        self.at('potassium conductance climbs'); self.play(FadeIn(rows[2]),run_time=.3); self.finish()


class S19PeakMain(SpokenScene):
    def construct(self):
        stage(self,PEAK); rows=peak_reasons(); self.add(rows,heading('Why below +50 mV? · in the model'))
        self.at('risen potassium conductance matters most'); self.play(Transform(rows[2],note('risen gₖ matters most (model)',K,.7)),run_time=.4)
        self.at('The peak is about')
        apex=VA.P(PEAK,sample(PEAK)[0]); tag=T('about +40 mV (model)',28,VOLT).move_to([-2.1,2.2,0])
        self.play(FadeIn(tag),Create(DashedLine(VA.P(0,sample(PEAK)[0]),apex,color=VOLT)),run_time=.3); self.finish()


class S20Fall(SpokenScene):
    def construct(self):
        clock,_,_,_=stage(self,PEAK,peak_zoom=False); self.add(heading('3 · The fall',VOLT))
        self.at('Sodium conductance collapses'); self.add(VGroup(T('Inactivation closes',28,INACT),T('Na+ channels',28,INACT)).arrange(DOWN,buff=.18).move_to([4.0,2.0,0]))
        progress(self,clock,PEAK+.42,2.8)
        self.at('potassium conductance keeps rising'); self.add(VGroup(T('K+ gates stay open',28,K),T('gₖ rises',28,K)).arrange(DOWN,buff=.18).move_to([4.0,.85,0])); progress(self,clock,EARLY,1.2); self.finish()


class S21Fall2(SpokenScene):
    def construct(self):
        clock,_,_,_=stage(self,EARLY); self.add(heading('3 · The fall',VOLT))
        self.at('The balance point drops'); progress(self,clock,EARLY+.13,1.2)
        self.at('so the voltage falls'); progress(self,clock,CROSS-.18,1)
        self.at('sodium may still have'); self.play(FadeIn(VGroup(T('gₙₐ still larger',28,NA),T('than gₖ',28,NA)).arrange(DOWN,buff=.18).move_to([4.15,1.6,0])),run_time=.3); self.finish()


class S22Fall3(SpokenScene):
    def construct(self):
        clock,_,_,_=stage(self,CROSS-.18); self.add(heading('3 · The fall',VOLT))
        self.at('Soon potassium becomes'); progress(self,clock,CROSS+.3,1.3); self.add(note('gₖ now larger than gₙₐ',K,1.6))
        self.at('the balance point sinks'); progress(self,clock,UNDER-.8,1.4); self.finish()


class S23Negative(SpokenScene):
    def construct(self):
        self.add(heading('Feedback: fast rise, slower ending'))
        pos=feedback(-3.1,1.4); neg=feedback(3.1,1.4,False); self.add(pos,neg)
        ax=Ax(-5.5,5.5,-3.1,-1.6,0,8,-85,55); self.add(trace(ax,FREE[:,0],FREE[:,1],VOLT),T('Model spike',26,VOLT).move_to([-4,-3.5,0]))
        self.at('This is negative feedback'); self.play(Indicate(neg[2],color=INACT),run_time=.4)
        self.at('The same depolarization'); self.play(Indicate(neg[1][0],color=VOLT),run_time=.4)
        self.at('also ends it'); self.play(Indicate(neg[0],color=INACT),run_time=.5)
        self.at('a little later'); self.add(T('Slower response lowers depolarization',28,INACT).move_to([2.1,-3.5,0])); self.finish()


class S24Undershoot(SpokenScene):
    def construct(self):
        clock,_,_,_=stage(self,UNDER-.8); self.add(heading('4 · The undershoot',VOLT),note('gₖ still above rest',K,2.1))
        self.at('Moment 4'); progress(self,clock,UNDER,1)
        self.at('Potassium conductance stays above rest'); self.play(Create(DashedLine(GA.P(0,FREE[0,3]),GA.P(GA.t1,FREE[0,3]),color=K)),run_time=.3)
        self.at('gates close slowly'); self.add(note('Slow gate closure',K,1.3))
        self.at('The balance point and voltage'); self.add(DashedLine([railx(-65),-3.3,0],[railx(-65),-2.8,0],color=GREY),T('rest',26,GREY).move_to([railx(-65),-2.65,0])); self.finish()


class S25Takeaway(SpokenScene):
    def construct(self):
        lines=VGroup(T('Fast sodium activation makes the rise.',26,NA),T('Slower inactivation and potassium activation end it.',26,K),T('Vm chases the balance point.',26,TEAL)).arrange(DOWN,buff=.12).move_to([0,3.1,0]); self.add(lines)
        va=Ax(-5.1,5.1,-.35,2.35,0,8,-85,55); ga=Ax(-5.1,5.1,-2.9,-.7,0,8,0,42)
        for ax in [va,ga]: self.add(Line([ax.x0,ax.y0,0],[ax.x1,ax.y0,0],color=GREY),Line([ax.x0,ax.y0,0],[ax.x0,ax.y1,0],color=GREY))
        self.add(trace(va,FREE[:,0],FREE[:,1],VOLT),trace(ga,FREE[:,0],FREE[:,2],NA),trace(ga,FREE[:,0],FREE[:,3],K),T('Vm (mV)',26,VOLT).move_to([-3.7,1.7,0]),T('g (mS/cm²)',26,TEAL).move_to([-3.5,-.95,0]),T('Na+',26,NA).move_to([5.6,-2.32,0]),T('K+',26,K).move_to([5.6,-2.86,0]),T('Time (ms)',26,GREY).move_to([0,-3.5,0]))
        for v,col,label in [(50,NA,'+50'),(0,GREY,'0'),(-77,K,'−77')]: self.add(T(label,26,col).move_to([-5.7,va.Y(v),0]),DashedLine(va.P(0,v),va.P(8,v),color=col,stroke_opacity=.2))
        self.add(T('40',26,GREY).move_to([-5.6,ga.Y(40),0]),T('0',26,GREY).move_to([-5.6,ga.Y(0),0]))
        for tt in [0,2,4,6,8]: self.add(T(str(tt),26,GREY).move_to([ga.X(tt),-3.23,0]))
        self.at('Fast sodium activation'); self.play(Indicate(lines[0],scale_factor=1.02),run_time=.4)
        self.at('Slower inactivation'); self.play(Indicate(lines[1],scale_factor=1.02),run_time=.4); self.finish()


class S26End(EndCard):
    LINE='Fast sodium activation starts the spike; slower processes end it.'
    def construct(self):
        self.add(VGroup(T('Fast sodium activation starts the spike;',36,NA),T('slower processes end it.',36,INACT),T('biochemistrypedia.com',26,TEAL)).arrange(DOWN,buff=.45)); self.finish()
