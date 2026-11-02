"""The Spike and Its Puzzles: chapter 1 (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
All voltage traces are computed from the supplied Hodgkin-Huxley equations.
The old-theory illustration caps the computed voltage at zero and retains its full return.

COLOR MAP (one color per concept, whole video)
  YELLOW = sodium: sodium current, sodium conductance, sodium's equilibrium line, the active stretch
  BLUE   = potassium: potassium current, potassium conductance, potassium's equilibrium line
  GREEN  = the membrane voltage trace
  RED    = inactivation / refractory
  TEAL   = conductance g in the rule (I = g x driving force)
  ORANGE = driving force in the rule
  GREY   = membrane, axes, rest and zero lines, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

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
        pulses = [stim] if isinstance(stim[0], (float, int)) else stim
        I = sum(p[2] for p in pulses if p[0] <= t < p[0] + p[1])
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


# The voltage remains GREEN; line styles distinguish stimulus protocols.
AX = Ax(-5.25, 5.75, -2.95, 3.05, 0, 24, -85, 50)
ZOOM = Ax(-5.25, 5.75, -2.95, 3.05, 6, 16, -85, 50)
MAIN = hh_free(T=24, stim=[(1., .3, 16.), (5., .3, 16.), (8., .3, 80.)])
TT, VV = MAIN[:, 0], MAIN[:, 1]
PEAK = int(VV.argmax())
ZERO = np.where((TT > 8) & (VV >= 0))[0][0]
START = np.where((TT > 8) & (VV >= -55))[0][0]
FALL = np.where((np.arange(len(TT)) > PEAK) & (VV < -65))[0][0]
MINIMUM = int(VV.argmin())
DOWNZERO = np.where((np.arange(len(TT)) > PEAK) & (VV <= 0))[0][0]
REST = hh_free(T=24, stim=(30., .3, 0.))


def label(text, x, y, size=28, color=TEXT):
    return T(text, size, color).move_to([x, y, 0]).add_background_rectangle(color=BG, opacity=1, buff=.06)


def dash(a, b, color=GREY):
    return DashedLine(a, b, color=color, stroke_width=1.6, dash_length=.12)


def graph(ax=AX, times=None):
    if times is None:
        times = [0, 4, 8, 12, 16, 20, 24] if ax is AX else [6, 8, 10, 12, 14, 16]
    axes = VGroup(Line(ax.P(ax.t0,-85), ax.P(ax.t0,50), color=GREY),
                  Line(ax.P(ax.t0,-85), ax.P(ax.t1,-85), color=GREY))
    ticks = VGroup()
    for v in [-80, -65, 0, 50]:
        ticks.add(M(f'{v:+d}' if v > 0 else str(v), 26, TEXT).next_to(ax.P(ax.t0,v), LEFT, buff=.15))
    for t in times:
        ticks.add(M(str(t),26,TEXT).move_to([ax.X(t),-3.24,0]))
    ticks.add(label('Vm (mV)',-5.0,3.5,26,GREY), label('time (ms)',4.9,-3.65,26,GREY))
    return VGroup(axes, ticks, dash(ax.P(ax.t0,0), ax.P(ax.t1,0)))


def segment(i=0, j=None, data=MAIN, ax=AX, color=VOLT, w=4):
    j = len(data)-1 if j is None else j
    d=data[i:j+1]
    d=d[(d[:,0]>=ax.t0)&(d[:,0]<=ax.t1)]
    return curve(ax,d[:,0],d[:,1],color=color,w=w,stride=2)


def callout(text, x, y, point, color=TEXT, size=28):
    lab=label(text,x,y,size,color)
    side = lab.get_bottom() if point[1] < y-.25 else lab.get_top() if point[1] > y+.25 else lab.get_left() if point[0]<x else lab.get_right()
    return VGroup(Line(side,point,color=color,stroke_width=1.7),lab)


def restline(ax=AX):
    return dash(ax.P(ax.t0,-65),ax.P(ax.t1,-65))


def restlabel(ax=AX):
    t=0.5 if ax is AX else 7.
    return (callout('rest, −65 mV',-3.65,-.65,ax.P(.5,-65)) if ax is AX
            else callout('rest, −65 mV',-3.8,-2.45,ax.P(t,-65)))


def stimulus(t, text, ax=AX, height=.35, color=GREY):
    # Stimulus lane sits just above the bottom axis, below the voltage range.
    x=ax.X(t)
    tick=Line([x,-2.92,0],[x,-2.92+height,0],color=color,stroke_width=4)
    lab=label(text,x,-3.65,26,color)
    return VGroup(tick,lab)


def nudges(count=2):
    return VGroup(*[stimulus(t,word,height=h) for t,word,h in [(1,'small',.12),(5,'small',.12),(8,'bigger',.6)][:count]])


def threshold(ax=AX):
    x,y=(1.6,-.5) if ax is AX else (-4.2,-1.15)
    return VGroup(dash(ax.P(ax.t0,-55),ax.P(ax.t1,-55)),
        callout('threshold',x,y,ax.P(TT[START],-55) if ax is AX else ax.P(7.5,-55)),
        label('(for this stimulus)',x,y-.4 if ax is AX else y+.5,26 if ax is AX else 22,GREY))


def shade(ax=ZOOM):
    d=MAIN[ZERO:DOWNZERO+1:2]
    return Polygon(ax.P(d[0,0],0),*[ax.P(t,v) for t,v in d[:,:2]],ax.P(d[-1,0],0),
        stroke_width=0,fill_color=VOLT,fill_opacity=.24)


def overshoot(ax=ZOOM, text='overshoot'):
    x=ax.X(TT[DOWNZERO])+.28; y0=ax.Y(0); y1=ax.Y(VV[PEAK])
    return VGroup(Line([x,y0,0],[x,y1,0],color=VOLT),
        Line([x-.12,y0,0],[x+.12,y0,0],color=VOLT),
        Line([x-.12,y1,0],[x+.12,y1,0],color=VOLT),
        label(text,min(x+1.4,4.5),(y0+y1)/2,28,VOLT))


def peaklabel(ax=ZOOM):
    return callout('peak, about +40 mV',3.4,2.9,ax.P(TT[PEAK],VV[PEAK]))


def riselabel(ax=ZOOM):
    i=np.where((TT>8)&(VV>=-25))[0][0]
    return callout('rising phase',-4.05,.3,ax.P(TT[i],VV[i]))


def falllabel(ax=ZOOM):
    i=np.where((np.arange(len(TT))>PEAK)&(VV<=-25))[0][0]
    return callout('falling phase',4.45,-.3,ax.P(TT[i],VV[i]))


def underlabel(ax=ZOOM):
    x=ax.X(TT[MINIMUM]); y0=ax.Y(-65); y1=ax.Y(VV[MINIMUM])
    return VGroup(Line([x,y0,0],[x,y1,0],color=VOLT),
        Line([x-.13,y0,0],[x+.13,y0,0],color=VOLT),
        Line([x-.13,y1,0],[x+.13,y1,0],color=VOLT),
        callout('undershoot',4.25,-1.65,np.array([x,(y0+y1)/2,0])))


def recovery(ax=ZOOM):
    i=np.searchsorted(TT,ax.t1)
    return callout('recovery continues →',3.7,-2.76,ax.P(TT[i],VV[i]),VOLT,size=24)


def stage(scene,end=None,ax=AX,rest=True):
    scene.add(graph(ax))
    if rest: scene.add(restline(ax),restlabel(ax))
    if end is not None: scene.add(segment(j=end,ax=ax))


def question():
    return VGroup(label('Pause',0,2.05,28,TEAL),label('A much bigger brief push:',0,.65,40),label('a bigger spike?',0,-.55,42))


def puzzles(count=4, compact=False):
    words=['Overshoot?','Threshold?','All-or-none?','Refractoriness?','Travel?']
    rows=VGroup()
    for i,w in enumerate(words[:count]):
        x=(-4.7 if i%2==0 else 1.8) if compact else (-4.7 if i%2==0 else 1.1)
        y=(2.25-(i//2)*.7) if compact else 1.75-(i//2)*2.6
        box=Square(side_length=.3,color=GREY).move_to([x,y,0])
        lab=T(w,32 if compact else 40).next_to(box,RIGHT,buff=.28)
        rows.add(VGroup(box,lab))
    return rows


class S00Title(TitleCard):
    LESSON='The Action Potential and Conduction'
    TITLE='The Spike and Its Puzzles'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.35,26,TEAL))
        self.play(FadeIn(label(self.LESSON,0,1.3,28,GREY)),FadeIn(label(self.TITLE,0,0,48)),run_time=.7)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        self.at('What does a nerve')
        self.play(FadeIn(label('What does a nerve signal look like?',0,.75,36)),run_time=.55)
        self.at('and what makes it')
        self.play(FadeIn(label('And what makes it?',0,-.65,36)),run_time=.5)
        self.finish()


class S02Axes(SpokenScene):
    def construct(self):
        g=graph()
        self.at('Here is the membrane')
        self.play(Create(g[0]),run_time=.8)
        self.at('potential of a model')
        self.play(FadeIn(g[1]),run_time=.6)
        self.at('over a few')
        self.play(Create(g[2]),run_time=.6)
        self.finish()


class S03Rest(SpokenScene):
    def construct(self):
        stage(self,rest=False)
        self.at('starts flat')
        self.play(Create(segment(j=599,data=REST)),run_time=1.2)
        self.at('This is rest')
        self.play(Create(restline()),FadeIn(restlabel()),run_time=.5)
        self.finish()


class S04Nudges(SpokenScene):
    def construct(self):
        stage(self,rest=True)
        self.add(segment(j=199))
        self.at('Now we nudge it')
        self.play(Create(nudges(1)),run_time=.35)
        self.at('A small nudge')
        self.play(Create(segment(199,999)),run_time=1.25)
        self.at('So does another')
        self.play(Create(nudges(2)[1]),Create(segment(999,1599)),run_time=1.1)
        self.finish()


class S05Threshold(SpokenScene):
    def construct(self):
        stage(self,1599); self.add(nudges())
        self.at('A slightly bigger nudge')
        self.play(Create(nudges(3)[2]),Create(segment(1599,START)),Create(threshold()[0]),run_time=1.6)
        self.at('For this stimulus')
        self.play(FadeIn(VGroup(*threshold()[1:])),run_time=.5)
        self.at('Past it')
        self.play(Create(segment(START,ZERO-60)),run_time=1.65)
        self.finish()


class S06Rise(SpokenScene):
    def construct(self):
        stage(self,ZERO-60,ZOOM)
        self.add(label('spike window · slow motion',.8,3.5,28,TEAL))
        self.at('It shoots up')
        self.play(Create(segment(ZERO-60,ZERO,ax=ZOOM)),run_time=.65)
        x0,x1=ZOOM.X(TT[START]),ZOOM.X(TT[ZERO])
        b=VGroup(Line([x0,-2.8,0],[x1,-2.8,0],color=TEXT),
            Line([x0,-2.7,0],[x0,-2.9,0],color=TEXT),
            Line([x1,-2.7,0],[x1,-2.9,0],color=TEXT),
            callout('less than 1 ms',.3,-2.55,[(x0+x1)/2,-2.8,0],size=26))
        self.at('in a fraction')
        self.play(FadeIn(b),run_time=.35)
        self.at('This is the rising')
        self.play(FadeIn(riselabel()),run_time=.5)
        self.finish()


class S07Peak(SpokenScene):
    def construct(self):
        stage(self,ZERO,ZOOM); self.add(riselabel())
        self.at('It crosses zero')
        self.play(Create(segment(ZERO,DOWNZERO,ax=ZOOM)),run_time=1.7)
        # Full positive lobe is now present, so its filled area is meaningful.
        self.play(FadeIn(shade()),run_time=.3)
        self.at('At the peak')
        self.play(FadeIn(peaklabel()),run_time=.5)
        self.at('Going past zero')
        self.play(FadeIn(overshoot()),run_time=.5)
        self.finish()


class S08Fall(SpokenScene):
    def construct(self):
        stage(self,DOWNZERO,ZOOM)
        self.add(shade(),peaklabel(),overshoot(),riselabel())
        self.at('Then the falling phase')
        self.play(Create(segment(DOWNZERO,FALL,ax=ZOOM)),FadeIn(falllabel()),run_time=2.2)
        self.at('past rest')
        self.play(Indicate(restline(ZOOM),color=VOLT),run_time=.5)
        self.finish()


class S09Undershoot(SpokenScene):
    def construct(self):
        # Keep the same spike window; explicitly mark recovery beyond its right edge.
        ax=ZOOM
        self.add(graph(ax),restline(ax),restlabel(ax),segment(j=FALL,ax=ax),
            shade(ax),peaklabel(ax),overshoot(ax),falllabel(ax))
        self.at('It dips below rest')
        self.play(Create(segment(FALL,MINIMUM,ax=ax)),run_time=1.7)
        self.at('That is the undershoot')
        self.play(FadeIn(underlabel(ax)),run_time=.5)
        self.at('Then it settles back')
        self.play(Create(segment(MINIMUM,ax=ax)),run_time=1.2)
        self.play(FadeIn(recovery(ax)),run_time=.35)
        self.finish()


class S10Name(SpokenScene):
    def construct(self):
        # Carry the same window and the recovery continuation into the recap.
        stage(self,len(MAIN)-1,ZOOM)
        self.add(threshold(ZOOM),riselabel(),falllabel(),peaklabel(),shade(),overshoot(),underlabel(),recovery())
        self.at('The whole event')
        self.play(FadeIn(label('Action potential (spike)',1.2,3.5,32)),run_time=.5)
        self.finish()


class S11History(SpokenScene):
    def construct(self):
        # Longitudinal cutaway, open at the left: the electrode enters axially.
        wall=VGroup(Line([-5,-2,0],[5.45,-2,0],color=GREY,stroke_width=3),
            Line([-5,2,0],[5.45,2,0],color=GREY,stroke_width=3),
            Ellipse(width=.65,height=4,color=GREY).move_to([-5,0,0]),
            Arc(radius=2,start_angle=-PI/2,angle=PI,color=GREY).stretch(.22,0).move_to([5.45,0,0]))
        interior=Rectangle(width=10.45,height=4,stroke_width=0,fill_color=GREY,fill_opacity=.09).move_to([.225,0,0])
        electrode=VGroup(Line([-6,0,0],[2.8,0,0],color=TEXT,stroke_width=3),Dot([2.8,0,0],radius=.055,color=TEXT))
        self.at('In')
        self.play(FadeIn(label('Hodgkin and Huxley, 1939',0,2.9,36)),FadeIn(interior),Create(wall),run_time=.65)
        self.at('recorded this')
        self.play(Create(electrode),run_time=.8)
        self.at('inside a squid')
        self.play(FadeIn(callout('fine electrode',.5,.7,[1.8,0,0])),
            FadeIn(label('squid giant axon · longitudinal cutaway',0,-2.45,30)),
            FadeIn(label('diameter: about 0.5 mm',0,2.3,26,GREY)),run_time=.5)
        self.at('The overshoot')
        self.play(FadeIn(label('The overshoot was a surprise.',0,-3.1,32,VOLT)),run_time=.5)
        self.finish()


class S12Theory(SpokenScene):
    def construct(self):
        ax=Ax(-5.25,5.75,-2.95,3.05,6,14,-85,50)
        self.add(graph(ax,[6,8,10,12,14]),restline(ax))
        old=MAIN.copy(); old[:,1]=np.clip(old[:,1],-65,0)
        self.at('The leading theory')
        self.play(Create(DashedVMobject(segment(data=old,ax=ax,color=TEXT).shift(LEFT*.12),num_dashes=75)),
            FadeIn(callout('old theory: stop near zero',2.9,-.35,ax.P(9.6,0)+LEFT*.12)),run_time=1.8)
        self.at('It did not')
        self.play(Create(segment(ax=ax)),run_time=2.)
        gap=overshoot(ax,'what the theory\nmissed')
        gap[-1].move_to([3.25,1.7,0])
        self.play(FadeIn(shade(ax)),FadeIn(peaklabel(ax)),FadeIn(gap),run_time=.4)
        self.wait(1.4)
        self.finish()


class S13Predict(SpokenScene):
    def construct(self):
        q=question()
        self.at('A question to hold'); self.play(FadeIn(q[0]),run_time=.4)
        self.at('If we push much harder'); self.play(FadeIn(q[1]),run_time=.6)
        self.at('will the spike'); self.play(FadeIn(q[2]),run_time=.6)
        self.finish()


class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question()); self.wait(3.)


class S15Reveal(SpokenScene):
    def construct(self):
        ax=Ax(-5.25,5.75,-2.95,3.05,0,10,-85,50)
        self.add(graph(ax,[0,2,4,6,8,10]),restline(ax),label('Brief pushes from rest',3.6,1.35,26))
        data=[hh_free(T=10,stim=(1.,.3,a)) for a in [24.,40.,80.]]
        # Solid, long dash, short dash: all three traces mean membrane voltage.
        traces=[segment(data=d,ax=ax,w=4) for d in data]
        traces[1]=DashedVMobject(traces[1],num_dashes=55)
        traces[2]=DashedVMobject(traces[2],num_dashes=110)
        positions=[(3.6,3.5),(0,3.5),(-2.7,3.5)]
        labs=[]
        for d,word,(x,y) in zip(data,['just threshold','bigger','much bigger'],positions):
            peak=d[d[:,1].argmax()]
            labs.append(callout(word,x,y,ax.P(*peak[:2]),size=28))
        # Three separate protocol lanes each mark the same onset, 1 ms.
        pushes=[]
        for word,h,y in [('small',.15,.65),('bigger',.3,-.15),('much bigger',.6,-.95)]:
            pushes.append(VGroup(Line([1.5,y,0],[2.8,y,0],color=GREY),
                Line([2.1,y,0],[2.1,y+h,0],color=TEXT,stroke_width=4),
                label(word,4.15,y+.12,26),label('1 ms',2.65,y-.25,22,GREY)))
        # The first trace establishes the baseline before the earlier spikes arrive.
        self.at('it comes sooner',lead=1.4)
        self.play(Create(traces[0]),FadeIn(labs[0]),Create(pushes[0]),run_time=.9)
        self.at('it comes sooner')
        self.play(Create(traces[1]),FadeIn(labs[1]),Create(pushes[1]),run_time=.45)
        self.play(Create(traces[2]),FadeIn(labs[2]),Create(pushes[2]),run_time=.45)
        self.at('but it is essentially')
        left=min(d[d[:,1].argmax(),0] for d in data)-.2
        right=max(d[d[:,1].argmax(),0] for d in data)+.2
        eq=VGroup(Line(ax.P(left,52.5),ax.P(right,52.5),color=VOLT),
            Line(ax.P(left,51),ax.P(left,54),color=VOLT),
            Line(ax.P(right,51),ax.P(right,54),color=VOLT),
            callout('same size',1.4,2.2,ax.P(right,52.5),VOLT),
            label('All-or-none',4.2,2.25,32,VOLT))
        self.play(FadeIn(eq),run_time=.5)
        self.at('With brief pushes')
        self.play(FadeIn(label('Same onset · increasing push',3.1,-1.65,24,GREY)),run_time=.5)
        self.at('This is all or none')
        self.play(Indicate(eq,color=VOLT),run_time=.6)
        self.finish()


class S16Pairs(SpokenScene):
    def construct(self):
        ax=Ax(-5.25,5.75,-2.95,3.05,0,12,-85,50)
        data=hh_free(T=12,stim=[(1.,.3,220.),(3.5,.3,24.)])
        # Both pulses fire from rest; the second, delivered after the first spike,
        # causes only a small passive deflection. Do not flatten computed voltage.
        cut=int(3.5/.005)
        self.add(graph(ax,[0,2,4,6,8,10,12]),restline(ax),label('Two brief pushes',1.6,3.5,30))
        self.add(segment(j=199,data=data,ax=ax))
        self.at('Now two pushes')
        self.play(Create(stimulus(1,'first',ax,.6)),run_time=.4)
        self.at('first fires')
        self.play(Create(segment(199,cut,data=data,ax=ax)),run_time=.95)
        self.at('second fails')
        tick=stimulus(3.5,'second',ax,.3,INACT)
        self.play(Create(tick),Create(segment(cut,data=data,ax=ax)),run_time=.7)
        self.play(FadeIn(callout('no second spike',2.45,-1.1,ax.P(5,data[1000,1]),INACT)),run_time=.25)
        self.at('This')
        self.play(FadeIn(callout('refractory',-.6,.25,ax.P(3.5,data[cut,1]),INACT)),run_time=.5)
        self.finish()


class S17Puzzles(SpokenScene):
    def construct(self):
        self.at('So we have puzzles')
        p=puzzles()
        self.play(FadeIn(label('Puzzles',0,2.9,44)),FadeIn(VGroup(*[r[0] for r in p])),run_time=.5)
        # Each question recalls its computed evidence in a large four-panel checklist.
        icons=[]
        for i in range(4):
            x=-4.7 if i%2==0 else 1.1
            top=.95-(i//2)*2.6
            ax=Ax(x,x+4.6,top-1.2,top,0,12,-85,50)
            if i==0:
                d=hh_free(T=12,stim=(1.,.3,80.))
                positive=d[d[:,1]>0][::2]
                area=Polygon(ax.P(positive[0,0],0),*[ax.P(t,v) for t,v in positive[:,:2]],
                    ax.P(positive[-1,0],0),stroke_width=0,fill_color=VOLT,fill_opacity=.3)
                icon=VGroup(dash(ax.P(0,0),ax.P(12,0)),area,segment(data=d,ax=ax,w=3))
            elif i==1:
                d=hh_free(T=12,stim=(1.,.3,24.))
                icon=VGroup(dash(ax.P(0,-55),ax.P(12,-55)),segment(data=d,ax=ax,w=3))
            elif i==2:
                icon=VGroup()
                for j,amp in enumerate([24.,40.,80.]):
                    line=segment(data=hh_free(T=12,stim=(1.,.3,amp)),ax=ax,w=3)
                    icon.add(line if j==0 else DashedVMobject(line,num_dashes=40+30*j))
            else:
                d=hh_free(T=12,stim=[(1.,.3,220.),(3.5,.3,24.)])
                icon=VGroup(segment(data=d,ax=ax,w=3),
                    Line(ax.P(1,-84),ax.P(1,-63),color=GREY,stroke_width=3),
                    Line(ax.P(3.5,-84),ax.P(3.5,-63),color=INACT,stroke_width=3))
            icons.append(icon)
        for phrase,row,icon in zip(['Why the overshoot','Why a threshold','Why all or none','Why refractoriness'],p,icons):
            self.at(phrase)
            self.play(FadeIn(row[1]),Create(icon),run_time=.45)
        self.finish()


class S18Travel(SpokenScene):
    def construct(self):
        self.add(label('Five puzzles',0,3.15,40),puzzles(4,True))
        ax=Ax(-5.9,5.9,-3.05,-.3,0,12,-80,50)
        tube=VGroup(Line([-6,-.1,0],[6,-.1,0],color=GREY),Line([-6,-3.3,0],[6,-3.3,0],color=GREY))
        # A translated HH pulse is a schematic travelling voltage profile, not a cable-speed claim.
        d=hh_free(T=12,stim=(1.,.3,220.))
        source=d[(d[:,0]>=.6)&(d[:,0]<=5)]
        position=ValueTracker(0)
        def travelling():
            t=5-source[::-1,0]+position.get_value()
            v=source[::-1,1]
            return VGroup(curve(ax,t,v,stride=1),
                Line(ax.P(t[-1],v[-1]),ax.P(12,v[-1]),color=VOLT,stroke_width=5))
        pulse=always_redraw(travelling)
        wake=Rectangle(width=.1,height=3.1,stroke_width=0,fill_color=GREY,fill_opacity=.22).move_to([-5.9,-1.7,0])
        self.at('And why does')
        self.play(FadeIn(puzzles(5,True)[4]),Create(tube),FadeIn(pulse),run_time=.45)
        self.at('the spike travel')
        self.add(wake)
        self.play(position.animate.set_value(6),wake.animate.stretch_to_fit_width(6).move_to([-2.9,-1.7,0]),run_time=1.65,rate_func=linear)
        self.at('without turning back')
        back=Arrow([-1,-1.3,0],[-3,-1.3,0],color=INACT,buff=0)
        cross=VGroup(Line([-2.25,-1.05,0],[-1.75,-1.55,0],color=INACT),Line([-2.25,-1.55,0],[-1.75,-1.05,0],color=INACT))
        self.play(FadeIn(back),Create(cross),FadeIn(label('refractory behind',-2.5,-2.7,28,TEXT)),
            GrowArrow(Arrow([3.8,-1.6,0],[5.4,-1.6,0],color=VOLT)),run_time=.45)
        self.finish()


class S19Promise(SpokenScene):
    def construct(self):
        p=puzzles(5,True)
        for row in p:
            row[0].set_stroke(opacity=.6)
            row[1].set_opacity(.6)
        self.add(label('Five puzzles',0,3.15,40),p)
        scale=Line([-5.2,-2.7,0],[5.2,-2.7,0],color=GREY,stroke_width=3)
        rest_x=-5.2+(-65+77)/(50+77)*10.4
        marker=VGroup(Line([rest_x,-3,0],[rest_x,-2.4,0],color=VOLT,stroke_width=6),
            label('rest −65 mV',rest_x,-2.05,26,VOLT))
        ropes=VGroup(Line([-5.2,-2.7,0],[rest_x,-2.7,0],color=K,stroke_width=7),Line([rest_x,-2.7,0],[5.2,-2.7,0],color=NA,stroke_width=7))
        ropes.add(*[Line([x,-2.77,0],[x+.1,-2.63,0],color=TEXT,stroke_width=1.0,stroke_opacity=.45) for x in np.arange(-5.17,5.1,.18)])
        self.at('One rule')
        self.play(Create(scale),Create(ropes),Create(marker),FadeIn(label('Vm moves toward the balance point',0,-.6,30)),
            FadeIn(label('set by the conductances',0,-1.1,30)),run_time=.5)
        self.at('three gates')
        self.play(FadeIn(label('Three gates',-2.5,-.1,28,TEAL)),
            FadeIn(label('E_K −77 mV',-4.45,-3.35,26,K)),FadeIn(label('E_Na +50 mV',4.45,-3.35,26,NA)),run_time=.35)
        self.at('a little cable theory')
        self.play(FadeIn(label('Cable theory',2.5,-.1,28,TEAL)),run_time=.35)
        self.at('all five',lead=.08)
        checks=VGroup(*[VGroup(Line(r[0].get_center()+[-.1,0,0],r[0].get_center()+[-.02,-.09,0],color=VOLT),
            Line(r[0].get_center()+[-.02,-.09,0],r[0].get_center()+[.13,.12,0],color=VOLT)) for r in p])
        self.play(*[r[1].animate.set_opacity(1) for r in p],
            *[r[0].animate.set_stroke(opacity=1) for r in p],
            LaggedStart(*[Create(c) for c in checks],lag_ratio=.08),run_time=.6)
        self.finish()


def takeaway():
    return VGroup(label('From rest, a brief push gives an all-or-none spike.',0,1.3,32),
        label('It has a threshold.',0,.3,38),label('It is briefly refractory.',0,-.7,38),
        label('Overshoot and travel: five puzzles, one rule, next.',0,-1.9,28,TEAL))


class S20Takeaway(SpokenScene):
    def construct(self):
        card=takeaway()
        self.at('A spike is all or none'); self.play(FadeIn(card[0]),run_time=.5)
        self.at('it has a threshold'); self.play(FadeIn(card[1]),run_time=.5)
        self.at('and it needs a rest'); self.play(FadeIn(card[2]),FadeIn(card[3]),run_time=.5)
        self.finish()


class S21End(EndCard):
    LINE='From rest: all-or-none, with a threshold, and briefly refractory.'
    def construct(self):
        self.add(takeaway(),label('biochemistrypedia.com',0,-3,26,TEAL))
        self.finish()
