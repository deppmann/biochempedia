"""Chapter 2: word-synchronized, computed voltage and conductance teaching film.
COLOR MAP: YELLOW sodium; BLUE potassium; GREEN membrane voltage;
RED inactivation/refractory; TEAL conductance; ORANGE driving force;
GREY axes, membrane and leak. White filled diamond = balance point.
Script visual notes' older purple/orange/teal assignments yield to the series map.
"""
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


# The balance is the zero-current solution of the same HH membrane equation.
REST_NA, REST_K = FREE[0, 2:4]
def balance(gn, gk, gl=0.3):
    return (50*gn - 77*gk - 54.4*gl)/(gn+gk+gl)
REST = balance(REST_NA, REST_K)


# Local cue implementation avoids writing the pipeline's ancillary sync.log.
_BaseSpokenScene = SpokenScene
class SpokenScene(_BaseSpokenScene):
    def at(self, phrase, lead=.12, nth=0):
        remaining = self.t_of(phrase, nth) - lead - self.elapsed()
        if remaining > .02:
            self.wait(remaining)


def label(text, y=-2.45, color=TEXT, size=32):
    return T(text, size=size, color=color).move_to([0,y,0])


def tick_label(text,x,y,color):
    txt=T(text,26,color).move_to([x,y,0])
    return VGroup(BackgroundRectangle(txt,fill_color=BG,fill_opacity=1,buff=.025),txt).set_z_index(10)


class Scale:
    """Shared, full-height rope stage; widths depend only on conductance."""
    def __init__(self,v=REST,gn=REST_NA,gk=REST_K,ghost=False,
                 x0=-5.2,x1=5.2,lo=-77,hi=50,rest=False,leak=False):
        self.v,self.gn,self.gk=ValueTracker(v),ValueTracker(gn),ValueTracker(gk)
        self.b=ValueTracker(balance(gn,gk))
        self.x=lambda q:x0+(q-lo)/(hi-lo)*(x1-x0)
        self.y=-.2
        self.x0,self.x1=x0,x1
        self.base=VGroup(Line([x0,self.y,0],[x1,self.y,0],color=GREY,stroke_width=3))
        for val in [lo,hi]+([0] if lo<0<hi else []):
            xx=self.x(val)
            self.base.add(Line([xx,self.y-.21,0],[xx,self.y+.21,0],color=GREY,stroke_width=3))
            if val==0:self.base.add(tick_label('0 mV',xx,-1.65,GREY))
        if rest:
            xx=self.x(-65)
            self.base.add(DashedLine([xx,self.y-.2,0],[xx,self.y+.4,0],color=VOLT),
                tick_label('rest  −65 mV',max(x0+.8,xx),-1.65,VOLT))
        if hi==50:
            self.ends=VGroup(
                VGroup(T('potassium  E_K',28,K),M('−77 mV',30,K)).arrange(DOWN,buff=.14).move_to([x0+.65,2.94,0]),
                VGroup(T('sodium  E_Na',28,NA),M('+50 mV',30,NA)).arrange(DOWN,buff=.14).move_to([x1-.65,2.94,0]))
        else:
            self.ends=VGroup(T('E_K  −77 mV',30,K).move_to([x0+.65,2.85,0]),
                T('zoom: −77 to −50 mV',28,TEAL).move_to([2.4,3.2,0]))
        self.ropek=always_redraw(lambda:self.band(x0,self.x(self.v.get_value()),1.35,K,self.gk.get_value()))
        self.ropena=always_redraw(lambda:self.band(self.x(self.v.get_value()),x1,-1.05,NA,self.gn.get_value()))
        self.ropel=always_redraw(lambda:self.band(self.x(self.v.get_value()),self.x(-54.4),-1.95,GREY,.3))
        self.ropes=VGroup(self.ropek,self.ropena)
        if leak:self.ropes.add(self.ropel)
        # Direct marker label avoids leaders crossing rest or zero tick labels.
        self.marker=always_redraw(lambda:VGroup(
            Dot([self.x(self.v.get_value()),self.y,0],radius=.17,color=VOLT),
            tick_label('Vm',np.clip(self.x(self.v.get_value())+.58,x0+.55,x1-.45),.15,VOLT)))
        self.ghost=always_redraw(lambda:VGroup(
            Square(side_length=.34,color=TEXT,fill_color=TEXT,fill_opacity=1,stroke_width=2).rotate(PI/4).move_to([self.x(self.b.get_value()),.48,0]),
            Line([self.x(self.b.get_value()),.74,0],[(x0+x1)/2,1.94,0],color=TEXT,stroke_width=2),
            T('balance point',30,TEXT).move_to([(x0+x1)/2,2.2,0])))
        self.marker.set_z_index(4);self.ghost.set_z_index(5)
        self.all=VGroup(self.base,self.ends,self.ropes,self.marker)
        if ghost:self.all.add(self.ghost)
    @staticmethod
    def width(g):return 9+78*g/(g+.6)
    def band(self,a,b,y,color,g):
        width=self.width(g)
        if y>0:
            points=[[a,y,0],[b,y,0],[b,self.y,0]]
        elif y>-1.5:
            points=[[a,self.y,0],[a,y,0],[b,y,0]]
        else:
            points=[[a,y,0],[b,y,0]]
        return VMobject(stroke_color=color,stroke_width=width,fill_opacity=0).set_points_as_corners(points)
    def add(self,scene):scene.add(self.all);return self
    def chase(self,scene,target,duration=1):
        scene.play(self.v.animate.set_value(target),run_time=duration,
            rate_func=lambda a:(1-np.exp(-6*a))/(1-np.exp(-6)))


def formula(y=-2.5):
    top=VGroup(M('g_K E_K',29,K),M('+',29),M('g_Na E_Na',29,NA)).arrange(RIGHT,buff=.2)
    bottom=VGroup(M('g_K',29,K),M('+',29),M('g_Na',29,NA)).arrange(RIGHT,buff=.3)
    top.move_to([.6,y+.35,0]);bottom.move_to([.6,y-.38,0])
    bar=Line([top.get_left()[0]-.1,y,0],[top.get_right()[0]+.1,y,0],color=GREY)
    return VGroup(M('Vm =',29,VOLT).next_to(bar,LEFT,buff=.3),top,bar,bottom,
        T('leak joins later',26,GREY).move_to([4.7,y,0]))


def question():
    return VGroup(chip('Pause and predict',TEAL,size=26).move_to([0,3.25,0]),
        T('Sodium conductance rises far above potassium’s.',28,NA).move_to([0,-2.25,0]),
        T('Where does the balance point go?',34).move_to([0,-3.05,0]))


def spike(split=False):
    ax=Ax(-5.1,-.8 if split else 2.5,-2.8,2.8,0,10,-90,55)
    axes=VGroup(Line(ax.P(0,-90),ax.P(0,55),color=GREY),Line(ax.P(0,-90),ax.P(10,-90),color=GREY))
    for val,txt in [(0,'0 mV'),(-65,'−65 mV'),(40,'+40 mV')]:
        axes.add(DashedLine(ax.P(0,val),ax.P(10,val),color=GREY,stroke_opacity=.4),
            T(txt,26,GREY).next_to(ax.P(0,val),LEFT,buff=.12))
    axes.add(T('time (ms)',26,GREY).move_to([ax.X(7),-3.3,0]))
    trace=curve(ax,FREE[:,0],FREE[:,1],stride=3)
    return ax,axes,trace


class S00Title(TitleCard):
    LESSON='The Action Potential and Conduction'
    TITLE='Tug of War: Why the Voltage Goes Where It Goes'
    def construct(self):
        title=VGroup(T('Tug of War',48,font=TITLE_FONT),T('Why the Voltage Goes Where It Goes',32,font=TITLE_FONT)).arrange(DOWN,buff=.3)
        group=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,26,GREY),title,Line(LEFT,RIGHT,color=GOLD)).arrange(DOWN,buff=.4)
        self.play(FadeIn(group),run_time=.6);self.finish()


class S01Question(SpokenScene):
    def construct(self):
        ax,axes,tr=spike();self.add(axes,tr)
        peak=FREE[FREE[:,1].argmax()]
        self.add(T('rise',26,VOLT).move_to([ax.X(1.25),.3,0]),
            T('fall',26,VOLT).move_to([ax.X(4.7),1.3,0]))
        self.at('At the peak');self.play(Create(Circle(radius=.3,color=VOLT).move_to(ax.P(peak[0],peak[1]))),run_time=.35)
        inside=T('inside positive',26,VOLT).move_to([.8,3.22,0])
        self.at('turns positive');self.play(FadeIn(inside),Create(Line(inside.get_left(),ax.P(peak[0],peak[1])+.3*UP,color=VOLT)),run_time=.35)
        self.at('What could pull');self.play(FadeIn(VGroup(T('What could',32),T('pull it there?',32)).arrange(DOWN).move_to([4.6,.1,0])),run_time=.3);self.wait(2.2);self.finish()


class S02Scale(SpokenScene):
    def construct(self):
        s=Scale();self.add(label('Voltage scale',color=GREY));self.at('Start with');self.play(Create(s.base),run_time=1)
        self.at('At the left');self.play(FadeIn(s.ends[0]),Create(Line([-5.2,.02,0],[-5.2,2.38,0],color=K,stroke_width=6)),run_time=.5)
        self.at('At the right');self.play(FadeIn(s.ends[1]),Create(Line([5.2,.02,0],[5.2,2.38,0],color=NA,stroke_width=6)),run_time=.5);self.finish()


class S03Equilibrium(SpokenScene):
    def construct(self):
        s=Scale(v=-77);self.add(s.base,s.ends,s.marker)
        card=label('Equilibrium potential: no net push',size=32)
        self.at('An equilibrium potential');self.play(FadeIn(card),run_time=.3)
        zero=T('K: zero push',28,K).move_to([-4.5,1.75,0])
        self.play(FadeIn(zero),Flash([s.x(-77),s.y,0],color=K),run_time=.55)
        self.at('where an ion');self.play(FadeOut(zero),s.v.animate.set_value(50),run_time=.65)
        self.at('no net push');self.play(FadeIn(T('Na: zero push',28,NA).move_to([4.2,1.75,0])),Flash([s.x(50),s.y,0],color=NA),run_time=.5);self.finish()


class S04Ropes(SpokenScene):
    def construct(self):
        s=Scale();self.add(s.base,s.ends)
        self.at('A marker');self.play(FadeIn(s.marker),run_time=.4)
        self.at('membrane potential');self.play(FadeIn(label('membrane potential',color=VOLT)),run_time=.35)
        self.at("Each ion's");self.play(FadeIn(s.ropes),run_time=.6);self.finish()


class S05Pull(SpokenScene):
    def construct(self):
        s=Scale(gn=.12).add(self)
        # Pulse brightness continuously without changing the conductance widths.
        phase=ValueTracker(0)
        pulse=lambda m:m.set_stroke(opacity=.72+.28*np.cos(2*PI*phase.get_value()))
        s.ropek.add_updater(pulse);s.ropena.add_updater(pulse)
        a=VGroup(Arrow([s.x(REST)-.05,s.y+.1,0],[s.x(REST)-.8,s.y+.1,0],color=K,buff=0,stroke_width=8),
            Arrow([s.x(REST)+.05,s.y-.12,0],[s.x(REST)+.8,s.y-.12,0],color=NA,buff=0,stroke_width=8)).set_z_index(6)
        self.at("Each rope's");self.add(a)
        card=label('pull = current',y=-2.6,size=36)
        self.play(FadeIn(card),phase.animate.set_value(.5),run_time=.5,rate_func=linear)
        remaining=max(.1,self.narration_s-self.elapsed()-.15)
        self.play(phase.animate.set_value(phase.get_value()+remaining),run_time=remaining,rate_func=linear)
        self.finish()


class S06Conductance(SpokenScene):
    def construct(self):
        s=Scale(gn=.12).add(self)
        self.at('First conductance');self.play(FadeIn(label('rope thickness = conductance (g)',y=-3.05,color=TEAL)),run_time=.4)
        pores=VGroup(*[VGroup(Line([-.28,-.22,0],[-.28,.22,0],color=NA),Line([.28,-.22,0],[.28,.22,0],color=NA),Line([-.28,0,0],[.28,0,0],color=NA)) for _ in range(3)]).arrange(RIGHT,buff=.4).move_to([1,-2.2,0])
        self.at('how open');self.play(FadeIn(pores),run_time=.4)
        self.at('More open channels');self.play(*[FadeOut(p[2]) for p in pores],s.gn.animate.set_value(1.2),run_time=1)
        self.play(s.gn.animate.set_value(.3),run_time=.6);self.finish()


class S07Distance(SpokenScene):
    def construct(self):
        s=Scale(gn=.3).add(self)
        self.at('the distance');self.play(FadeIn(label('distance = Vm − E',color=ORANGE)),run_time=.35)
        gap=always_redraw(lambda:VGroup(
            Line([s.x(-77),-2.12,0],[s.x(s.v.get_value()),-2.12,0],color=ORANGE,stroke_width=4),
            Line([s.x(-77),-2.02,0],[s.x(-77),-2.22,0],color=ORANGE),
            Line([s.x(s.v.get_value()),-2.02,0],[s.x(s.v.get_value()),-2.22,0],color=ORANGE),
            T('gap = Vm − E_K',30,ORANGE).move_to([-2.5,-3.12,0])))
        self.at('The farther the marker');self.add(gap)
        s.ropek.add_updater(lambda m:m.set_stroke(opacity=.55+.45*(s.v.get_value()+77)/77))
        self.play(s.v.animate.set_value(0),run_time=1.35)
        self.at('the harder');self.play(Indicate(gap,color=ORANGE,scale_factor=1),run_time=.5);self.finish()


class S08Equation(SpokenScene):
    def construct(self):
        s=Scale(v=0,gn=.3).add(self)
        eq=VGroup(M('I =',36),M('g',36,TEAL),M('×',36),M('(Vm − E)',36,ORANGE)).arrange(RIGHT,buff=.23).move_to([0,-2.15,0])
        self.at('So current equals');self.play(FadeIn(eq),run_time=.5)
        bracket=Brace(eq[3],DOWN,color=ORANGE,buff=.12)
        self.at('and the driving');self.play(GrowFromCenter(bracket),FadeIn(T('driving force',28,ORANGE).next_to(bracket,DOWN,buff=.12)),run_time=.5);self.finish()


def current_arrows(v):
    # Explicit filled arrows: both length AND shaft width proportional to g|V-E|.
    def arrow(force,direction,color,cx):
        length=force*.037;half=force*.0032
        points=[(0,-half),(length-.35,-half),(length-.35,-2*half),(length,0),(length-.35,2*half),(length-.35,half),(0,half)]
        return Polygon(*[[cx+direction*x,-2.1+y,0] for x,y in points],color=color,fill_color=color,fill_opacity=1,stroke_width=0)
    return VGroup(arrow(v+77,-1,K,-.4),arrow(50-v,1,NA,.4))


class S09Arrows(SpokenScene):
    def construct(self):
        s=Scale(v=0,gn=.3,gk=.3).add(self)
        self.at('with equal conductances');self.play(FadeIn(T('equal g',28,TEAL).move_to([0,3.15,0])),run_time=.35)
        arrows=current_arrows(0)
        self.at("Sodium's end");self.play(FadeIn(arrows[1]),FadeIn(T('50 mV: pulls Vm up',28,NA).move_to([3,-3,0])),run_time=.4)
        self.at("Potassium's is");self.play(FadeIn(arrows[0]),FadeIn(T('77 mV: pulls Vm down',28,K).move_to([-3,-3,0])),run_time=.4)
        self.at('So potassium pulls');self.play(s.v.animate.set_value(-3),run_time=.65);self.finish()


class S10Balance(SpokenScene):
    def construct(self):
        s=Scale(v=-3,gn=.3,gk=.3).add(self)
        arrows=always_redraw(lambda:current_arrows(s.v.get_value()));self.add(arrows)
        self.add(T('pulls Vm down',28,K).move_to([-3,-3,0]),T('pulls Vm up',28,NA).move_to([3,-3,0]))
        self.at('The marker slides');self.play(s.v.animate.set_value(-13.5),run_time=2.25)
        s.b.set_value(-13.5);self.play(FadeIn(s.ghost),run_time=.3)
        self.at('That spot');self.play(Indicate(s.ghost[0],color=TEXT,scale_factor=1.3),run_time=.5);self.finish()


class S11Average(SpokenScene):
    def construct(self):
        s=Scale(v=-13.5,gn=.3,gk=.3,ghost=True).add(self);s.b.set_value(-13.5)
        self.at('The balance point');self.play(FadeIn(formula()),run_time=.4);self.finish()


class S12Weights(SpokenScene):
    def construct(self):
        s=Scale(v=-13.5,gn=.3,gk=.3,ghost=True).add(self);s.b.set_value(-13.5)
        f=formula();self.add(f)
        self.at('weighted by its conductance');self.play(Circumscribe(f[1][0],color=K),Circumscribe(f[3][0],color=K),s.gk.animate.set_value(.6),run_time=.8)
        self.at('The more open');self.play(s.gk.animate.set_value(1.2),Circumscribe(f[1][0],color=K),run_time=.7)
        self.at('the closer');target=balance(.3,1.2,0);self.play(s.b.animate.set_value(target),s.v.animate.set_value(target),run_time=1.1);self.finish()


class S13Chase(SpokenScene):
    def construct(self):
        start=balance(.3,1.2,0);s=Scale(v=start,gn=.3,gk=1.2,ghost=True).add(self);s.b.set_value(start)
        self.at('When a conductance changes');self.play(s.gn.animate.set_value(2),run_time=.8)
        self.at('the balance point jumps');target=balance(2,1.2,0);self.play(s.b.animate.set_value(target),run_time=.25)
        self.at('The voltage chases');s.chase(self,target,1.3);self.finish()


class S14Rest(SpokenScene):
    def construct(self):
        s=Scale(v=-58,ghost=True,rest=True).add(self)
        self.at('At rest');self.play(FadeIn(label('rest',color=VOLT)),run_time=.4)
        self.at('potassium has');self.play(Indicate(s.ropek,color=K,scale_factor=1.07),run_time=.65)
        self.at('the balance point');s.chase(self,REST,2)
        self.at('at about');self.play(Flash([s.x(-65),s.y,0],color=VOLT),run_time=.65);self.finish()


def zoom_stage(scene):
    z=Scale(v=REST,lo=-77,hi=-50)
    scene.add(z.base,z.ends,z.ropek,z.marker)
    # The sodium end is off this magnified axis: no false sodium endpoint.
    rest=VGroup(Line([z.x(-65),z.y-.21,0],[z.x(-65),z.y+.21,0],color=VOLT),
        T('rest  −65 mV',28,VOLT).move_to([z.x(-65)+1.6,.65,0]))
    scene.add(rest)
    return z


class S15RestWhy(SpokenScene):
    def construct(self):
        s=Scale(v=REST,ghost=True,rest=True).add(self)
        self.at('That is about')
        badge=chip('zoom in',TEAL,size=26).move_to([2.5,-2.5,0]);self.play(FadeIn(badge),run_time=.3)
        # Remove offscreen sodium before a clean fade; never morph text glyphs.
        s.all.clear_updaters(recursive=True)
        na_end=s.ends[1]
        self.play(FadeOut(s.ropena),FadeOut(na_end),run_time=.15)
        s.ropes.remove(s.ropena);s.ends.remove(na_end)
        self.play(FadeOut(s.all),run_time=.2)
        self.clear();z=zoom_stage(self)
        bracket=BraceBetweenPoints([z.x(-77),-.45,0],[z.x(-65),-.45,0],direction=DOWN,color=ORANGE)
        self.play(GrowFromCenter(bracket),FadeIn(T('12 mV',32,ORANGE).next_to(bracket,DOWN,buff=.15)),run_time=.4)
        self.at('mainly because of leak');self.play(FadeIn(z.ropel),run_time=.45)
        self.at('a path that');self.play(FadeIn(T('leak: always open',28,GREY).move_to([2.6,-2.65,0])),run_time=.4);self.finish()


class S16Leak(SpokenScene):
    def construct(self):
        z=zoom_stage(self);self.add(z.ropel)
        self.at('In the squid model');self.play(FadeIn(Arrow([z.x(REST),-.05,0],[5.2,-.05,0],color=NA,buff=0,stroke_width=7,max_tip_length_to_length_ratio=.03)),FadeIn(T('Na end offscreen →',26,NA).move_to([2.7,-.5,0])),run_time=.35)
        self.at('leak conductance');self.play(FadeIn(T('g_leak = 0.3 mS/cm²',28,GREY).move_to([2.6,-2.65,0])),run_time=.4)
        self.at('resting potassiums',lead=0);self.play(FadeIn(T('g_K ≈ 0.37 mS/cm²',28,K).move_to([-2.9,2.3,0])),Indicate(z.ropel,color=GREY,scale_factor=1.04),Indicate(z.ropek,color=K,scale_factor=1.04),run_time=.7)
        self.at('leaks equilibrium potential');self.play(Create(Line([z.x(-54.4),z.y-.21,0],[z.x(-54.4),z.y+.21,0],color=GREY)),FadeIn(T('E_leak ≈ −54 mV',28,GREY).move_to([4.2,.65,0])),run_time=.5)
        self.finish()


class S17Predict(SpokenScene):
    def construct(self):
        s=Scale(ghost=True,rest=True).add(self);q=question()
        self.at('Now a question');self.play(FadeIn(q[0]),run_time=.3)
        self.at('Suppose sodium');self.play(FadeIn(q[1]),run_time=.35)
        self.at('Where does');self.play(FadeIn(q[2]),FadeIn(T('?',28,TEAL).move_to([s.x(REST)+.55,.48,0])),run_time=.35);self.finish()


class S18Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        s=Scale(ghost=True,rest=True).add(self);self.add(question(),T('?',28,TEAL).move_to([s.x(REST)+.55,.48,0]))
        self.wait(float(os.environ.get('KX_DURATION','3')))


class S19Reveal(SpokenScene):
    def construct(self):
        s=Scale(ghost=True,rest=True).add(self)
        self.at('It slides toward');self.play(s.gn.animate.set_value(.4),s.b.animate.set_value(balance(.4,REST_K)),run_time=1.1)
        self.at('With enough sodium');self.play(s.gn.animate.set_value(20*REST_K),FadeIn(T('g_Na : g_K = 20 : 1',30,TEAL).move_to([0,-2.15,0])),run_time=.6)
        positive=Rectangle(width=5.2-s.x(0),height=1.4,stroke_width=0,fill_color=VOLT,fill_opacity=.13).move_to([(5.2+s.x(0))/2,s.y,0]).set_z_index(-1)
        self.at('passes zero',lead=0);target=balance(20*REST_K,REST_K)
        self.play(s.b.animate.set_value(target),FadeIn(positive),FadeIn(label('overshoot',y=-2.65,color=VOLT)),Flash([s.x(0),s.y,0],color=VOLT),run_time=.7)
        self.at('and the voltage');s.chase(self,target,1.05)
        self.play(FadeIn(T('g_Na > about 1.5 × g_K (ignoring leak)',28,TEAL).move_to([0,-3.25,0])),run_time=.3);self.wait(3);self.finish()


class S20MoreK(SpokenScene):
    def construct(self):
        start=balance(20*REST_K,REST_K);s=Scale(v=start,gn=20*REST_K,ghost=True,rest=True).add(self)
        self.at('If potassium conductance');self.play(s.gn.animate.set_value(REST_NA),s.gk.animate.set_value(2.5),run_time=1)
        self.at('the point would');target=balance(REST_NA,2.5);self.play(s.b.animate.set_value(target),run_time=.45)
        self.at('drop below rest');self.play(FadeIn(label('below rest',color=VOLT)),run_time=.25);s.chase(self,target,1.1);self.finish()


class S21Rule(SpokenScene):
    def construct(self):
        s=Scale(v=-53,ghost=True,rest=True).add(self)
        self.at('With no stimulus');self.play(FadeIn(label('With no stimulus',color=GREY)),run_time=.4)
        self.at('the voltage moves');self.play(FadeIn(label('Vm moves toward the balance point',y=-3.15,color=VOLT)),run_time=.4)
        s.chase(self,REST,1.3);self.finish()


class LinkedSpike:
    """Computed spike beside the same readable, full-height rope layout."""
    def __init__(self,scene,low=False):
        ax=Ax(-5.3,-2.1,-2.8,2.8,0,10,-90,55)
        axes=VGroup(Line(ax.P(0,-90),ax.P(0,55),color=GREY),Line(ax.P(0,-90),ax.P(10,-90),color=GREY))
        for v,txt in [(0,'0 mV'),(-65,'−65 mV'),(40,'+40 mV')]:
            axes.add(DashedLine(ax.P(0,v),ax.P(10,v),color=GREY,stroke_opacity=.4),T(txt,26,GREY).next_to(ax.P(0,v),LEFT,buff=.12))
        axes.add(T('time (ms)',26,GREY).move_to([-3.7,-3.3,0]))
        scene.add(axes,curve(ax,FREE[:,0],FREE[:,1],stride=3))
        endpoint=T_MIN if low else T_PEAK
        start=T_PEAK if low else max(0,T_PEAK-.7)
        self.t=ValueTracker(start)
        def row():return np.array([np.interp(self.t.get_value(),FREE[:,0],FREE[:,i]) for i in range(1,4)])
        self.row=row;self.endpoint=endpoint;self.ax=ax
        r=row();s=Scale(v=r[0],gn=r[1],gk=r[2],ghost=True,rest=True,x0=-.65,x1=5.85)
        # A shared relative scale preserves the computed conductance ratio.
        s.width=lambda g:7+78*g/max(.8,row()[1],row()[2])
        def sync(m):
            v,gn,gk=row();s.v.set_value(v);s.gn.set_value(gn);s.gk.set_value(gk);s.b.set_value(balance(gn,gk))
        s.all.add_updater(sync);s.add(scene)
        dot=always_redraw(lambda:Dot(ax.P(self.t.get_value(),row()[0]),radius=.12,color=VOLT))
        scene.add(dot)
        self.circle=Circle(radius=.27,color=VOLT).move_to(ax.P(endpoint,np.interp(endpoint,FREE[:,0],FREE[:,1])))


class S22Overshoot(SpokenScene):
    def construct(self):
        p=LinkedSpike(self)
        self.at('In this squid model');self.play(Create(p.circle),run_time=.35)
        self.at('a big');self.play(p.t.animate.set_value(p.endpoint),run_time=1.5,rate_func=linear)
        self.at('makes the overshoot');self.play(FadeIn(T('overshoot',32,VOLT).move_to([3.6,-2.5,0])),run_time=.35);self.finish()


class S23Undershoot(SpokenScene):
    def construct(self):
        p=LinkedSpike(self,True)
        self.at('potassium conductance');self.play(p.t.animate.set_value(p.endpoint),run_time=1.5,rate_func=linear)
        self.at('staying above rest');self.play(FadeIn(T('g_K above rest',28,K).move_to([3.6,-2.3,0])),run_time=.3)
        self.at('makes the undershoot');self.play(Create(p.circle),FadeIn(T('undershoot',32,VOLT).move_to([3.6,-3.1,0])),run_time=.4);self.finish()


class S24Questions(SpokenScene):
    def construct(self):
        # Crop the computed trace to the left; muted rope bands carry the motif.
        ax=Ax(-5.3,-2.1,-2.8,2.8,0,10,-90,55)
        axes=VGroup(Line(ax.P(0,-90),ax.P(0,55),color=GREY),Line(ax.P(0,-90),ax.P(10,-90),color=GREY)).set_opacity(.3)
        tr=curve(ax,FREE[:,0],FREE[:,1],stride=3).set_stroke(opacity=.3)
        s=Scale(v=0,gn=.5,gk=.5,x0=-.65,x1=5.85)
        # Freeze backdrop opacity: always_redraw would otherwise reset it.
        for rope in s.ropes:rope.clear_updaters();rope.set_stroke(opacity=.25)
        self.add(axes,tr,s.ropes)
        q1=VGroup(T('What makes the',32),T('conductances change?',32)).arrange(DOWN,buff=.15).move_to([2.65,.1,0])
        q2=VGroup(T('Why only',32),T('for a moment?',32)).arrange(DOWN,buff=.15).move_to([2.65,-2.5,0])
        self.at('What makes them change');self.play(FadeIn(BackgroundRectangle(q1,fill_color=BG,fill_opacity=.95,buff=.2)),FadeIn(q1),run_time=.35)
        self.at('And why only');self.play(FadeIn(BackgroundRectangle(q2,fill_color=BG,fill_opacity=.95,buff=.2)),FadeIn(q2),run_time=.35);self.wait(2.2);self.finish()


class S25Takeaway(SpokenScene):
    def construct(self):
        s=Scale(ghost=True,rest=True).add(self)
        self.at('The voltage chases');self.play(FadeIn(label('Vm chases the balance point',color=VOLT)),run_time=.35)
        self.at('set by the conductances');self.play(FadeIn(label('conductance-weighted average of E_K, E_Na and E_leak',y=-3.12,size=26)),run_time=.35)
        self.at('Change a conductance');self.play(s.gn.animate.set_value(.8),run_time=.5)
        self.at('and the point moves');target=balance(.8,REST_K);self.play(s.b.animate.set_value(target),run_time=.25);s.chase(self,target,.65);self.finish()


class S26End(EndCard):
    LINE='The voltage chases a balance point, set by the conductances.'
