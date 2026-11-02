"""Three Channels and the Availability Budget.
COLOR MAP: ORANGE Nav1.7; TEAL_C Nav1.8/current; PURPLE Nav1.9;
RED toxin/inactivated; GREEN availability; TEXT spike/current; GREY membrane/axes.
All traces are computed: reference PCHIP spike, analytic m*h current kinetics,
Boltzmann availability and exponential relaxation toward its steady state.
"""
from bp_style import *
import numpy as np
from scipy.interpolate import PchipInterpolator

ORANGE = '#F29E4C'
TEAL_C = '#3FB8C0'
PURPLE = '#B58CD9'

# Use exact word starts; keep review diagnostics outside the chapter's allowed files.
class SpokenScene(SpokenScene):
    def at(self, phrase, lead=0, nth=0):
        target = self.t_of(phrase, nth) - lead
        late = self.elapsed() - target
        with open('/tmp/availability-cues.log', 'a') as out:
            out.write(f'{os.environ.get("KX_SCENE_ID")} {phrase!r} target={target:.3f} late={late:.3f}\n')
        if late < -.02:
            self.wait(-late)


def heading(s, c=TEXT):
    return T(s, 32, c, font=TITLE_FONT).move_to([0, 3.38, 0])


def subtitle(s, c=TEXT):
    return T(s, 28, c).move_to([0, 2.68, 0])


def lines(ss, c=TEXT, size=26):
    return VGroup(*[T(s, size, c) for s in ss]).arrange(DOWN, buff=.16)


def arr(a, b, c=GREY):
    return Arrow(a, b, buff=.06, color=c, stroke_width=4, max_tip_length_to_length_ratio=.2)


def gate(x, y, state='ready', color=GREEN, scale=1):
    # Continuous walls; the gate/plug is a separate object, never a rotated wall.
    w, ht = .6*scale, 1.35*scale
    walls = VGroup(*[RoundedRectangle(width=.18*scale, height=ht,
        corner_radius=.06*scale, color=color, fill_color=BG, fill_opacity=1)
        .move_to([x+side*w/2, y, 0]) for side in [-1, 1]])
    if state == 'open':
        inside = arr([x,y+ht*.38,0], [x,y-ht*.38,0], color)
    elif state == 'inactive':
        walls.set_color(GREY).set_opacity(.6)
        inside = RoundedRectangle(width=w*.85, height=ht*.3,
            corner_radius=.06*scale, color=RED, fill_color=RED, fill_opacity=.8).move_to([x,y,0])
    else:
        inside = Line([x-w*.35,y,0],[x+w*.35,y,0],color=color,stroke_width=6)
    return VGroup(walls, inside)


def membrane(named=True):
    bg = VGroup(heading('Nociceptor membrane'))
    # A curved cell boundary, with gaps occupied by large membrane channels.
    for lo,hi in [(-6.2,-4.8),(-3.2,-.8),(.8,3.2),(4.8,6.2)]:
        for yy in [-.46,.46]:
            bg.add(Line([lo,yy,0],[hi,yy,0],color=GREY,stroke_width=9))
    bg.add(T('outside',26,GREY).move_to([-5.3,1.95,0]),
           T('cell interior',26,GREY).move_to([-4.9,-3.15,0]))
    gs = VGroup(*[gate(x,0,color=c,scale=2.15) for x,c in zip([-4,0,4],[ORANGE,TEAL_C,PURPLE])])
    lab = VGroup(*[T(n,32,c).move_to([x,-2.05,0]) for x,n,c in zip([-4,0,4],['Nav1.7','Nav1.8','Nav1.9'],[ORANGE,TEAL_C,PURPLE])])
    return bg, gs, lab


class Plot(VGroup):
    """Explicit left-only axes: no auto-positioned axis at the right boundary."""
    def __init__(self, xr, yr, origin, width, height, xticks, yticks):
        super().__init__()
        self.xr,self.yr,self.origin,self.w,self.ht=xr,yr,np.array([*origin,0.]),width,height
        self.add(Line(self.c2p(xr[0],yr[1]),self.c2p(xr[0],yr[0]),color=GREY),
                 Line(self.c2p(xr[0],yr[0]),self.c2p(xr[1],yr[0]),color=GREY))
        for v in xticks:
            p=self.c2p(v,yr[0]); self.add(Line(p+UP*.06,p+DOWN*.06,color=GREY),T(str(v).replace('-','−'),26,GREY).next_to(p,DOWN,buff=.14))
        for v in yticks:
            p=self.c2p(xr[0],v); self.add(Line(p+LEFT*.06,p+RIGHT*.06,color=GREY),T(f'{v:g}'.replace('-','−'),26,GREY).next_to(p,LEFT,buff=.14))
    def c2p(self,x,y):
        return self.origin+np.array([(x-self.xr[0])/(self.xr[1]-self.xr[0])*self.w,(y-self.yr[0])/(self.yr[1]-self.yr[0])*self.ht,0])
    def plot(self,fn,x_range=None,color=TEXT,stroke_width=5,**kw):
        a,b,step=x_range if x_range is not None else [*self.xr,(self.xr[1]-self.xr[0])/250]
        return VMobject(color=color,stroke_width=stroke_width,fill_opacity=0,**kw).set_points_as_corners([self.c2p(t,float(fn(t))) for t in np.linspace(a,b,max(3,int((b-a)/step)+1))])


def spike_fn():
    pts=[(0,0),(.45,.02),(.62,.30),(.78,1),(.95,.74),(1.15,.46),(1.5,.40),(1.85,.02),(2.1,-.14),(2.6,0),(3,0)]
    return PchipInterpolator(*zip(*pts))


def spike_panel():
    ax=Plot([0,3],[-85,40],[-5.5,-2.5],7.4,4.8,[0,1,2,3],[-80,-40,0,40])
    f=lambda t:-70+100*spike_fn()(t)
    cv=ax.plot(f)
    labels=VGroup(T('mV',26,GREY).move_to([-6.1,2.65,0]),T('time (ms)',26,GREY).move_to([-1.8,-3.17,0]),T('Reference spike model • schematic contributions',26,GREY).move_to([0,-3.55,0]))
    return ax,cv,labels,f


def rest_panel():
    box=RoundedRectangle(width=3.7,height=4.9,corner_radius=.15,color=GREY).move_to([4.35,-.1,0])
    rest=Line([2.9,-.6,0],[5.8,-.6,0],color=PURPLE,stroke_width=5)
    return VGroup(box,T('Nav1.9',30,PURPLE).move_to([4.35,1.8,0]),T('Rest',28).move_to([4.35,1.1,0]),rest,
        T('−65 mV',26,PURPLE).move_to([4.35,-1.15,0]),arr([4.35,-.45,0],[4.35,.55,0],PURPLE),
        lines(['steady inward','influence'],PURPLE,26).move_to([4.35,-2.05,0]))


def transient(t): return 1.8*(1-np.exp(-t/.18))*np.exp(-t/.8)
def persistent(t): return .24*(1-np.exp(-t/.45))*(.65+.35*np.exp(-t/10))


def current_panel():
    ax=Plot([0,8],[0,1.1],[-5.4,-2.4],11,4.45,[0,2,4,6,8],[0,.5,1])
    lab=VGroup(T('relative inward current',26,GREY).move_to([-3.5,2.35,0]),T('time (ms)',28,GREY).move_to([.1,-3.15,0]),T('Illustrative gate kinetics • shared relative scale',26,GREY).move_to([0,-3.55,0]))
    return ax,VGroup(ax,lab),ax.plot(transient),ax.plot(persistent)


def h(v,mid=-65,k=7): return 1/(1+np.exp((v-mid)/k))


def availability():
    ax=Plot([-90,-40],[0,1],[-5.55,-2.35],7.75,4.5,[-90,-80,-70,-60,-50,-40],[0,.5,1])
    lab=VGroup(T('Available fraction',26,GREY).rotate(PI/2).move_to([-6.55,-.1,0]),T('Resting voltage (mV)',26,GREY).move_to([-1.6,-3.12,0]))
    return ax,lab,ax.plot(h,color=ORANGE,stroke_width=6)


def curve_base(title='Steady-state availability', sub=None):
    ax,lab,cv=availability()
    base=VGroup(ax,lab,cv,heading(title),T('Illustrative Nav1.7-like • tetrodotoxin sensitive • not every sodium channel',26,GREY).move_to([0,-3.55,0]))
    if sub: base.add(subtitle(sub))
    return ax,base


def marker(ax,v,c=GREEN,dot=True):
    g=VGroup(DashedLine(ax.c2p(v,0),ax.c2p(v,1),color=c,stroke_width=2))
    if dot: g.add(Dot(ax.c2p(v,h(v)),color=c,radius=.09))
    return g


def band(ss,c=TEXT,y=.8):
    return lines(ss,c,26).move_to([4.4,y,0])


def prediction():
    ax,base=curve_base('Same channels • different resting voltages')
    marks=VGroup(marker(ax,-70,GREEN,False),marker(ax,-55,TEAL_C,False))
    labels=VGroup(band(['Low rest','−70 mV'],GREEN,1.3),band(['High rest','−55 mV'],TEAL_C,-.2))
    q=subtitle('Which has more available?')
    return ax,base,marks,labels,q


def cost_box(low=True,high=True):
    rows=VGroup()
    for yes,c,y,ss in [(low,GREEN,1.25,['Low: −70 → −65 mV','h: 0.67 → 0.50','Kept: 0.74 ≈ ¾']),
                       (high,TEAL_C,-.85,['High: −55 → −50 mV','h: 0.19 → 0.10','Kept: 0.54 ≈ ½'])]:
        box=RoundedRectangle(width=4.05,height=1.8,corner_radius=.1,color=c,stroke_opacity=.5).move_to([4.35,y,0])
        rows.add(VGroup(box,lines(ss,c,26).move_to(box)) if yes else box)
    return rows


def field(opened=False):
    gs=VGroup(*[gate(x,y,'open' if opened and i<14 else ('ready' if i<14 else 'inactive'),scale=.72)
        for i,(x,y) in enumerate([(x,y) for y in [1.8,.45,-.9,-2.25] for x in [-5,-3.25,-1.5,.25,2]])])
    legend=VGroup()
    for yy,state,c,ss in [(1.55,'ready',GREEN,['closed','and ready']),(-.1,'open',GREEN,['open:','inward flow']),(-1.8,'inactive',RED,['inactivated','stays shut'])]:
        legend.add(gate(3.45,yy,state,c,.65),lines(ss,c,26).move_to([5,yy,0]))
    return gs,legend


def mini_gauge(value,x=4.35,y=-.5,width=3.25,height=.38):
    outline=Rectangle(width=width,height=height,color=GREEN).move_to([x,y,0])
    fill=Rectangle(width=max(.01,(width-.08)*value),height=height-.08,stroke_width=0,fill_color=GREEN,fill_opacity=.75).align_to(outline,LEFT).shift(RIGHT*.04).set_y(y)
    return VGroup(outline,fill)


class S00Title(TitleCard):
    TITLE='Three Channels and the Availability Budget'
    LESSON='Nociceptors and the Sodium Channels of Pain'
    def construct(self):
        self.add(T('BIOCHEMISTRYPEDIA',26,TEAL).move_to([0,2.2,0]),T(self.LESSON,26,GREY).move_to([0,1.35,0]))
        self.play(FadeIn(lines(['Three Channels and','the Availability Budget'],TEXT,48).move_to([0,-.2,0])),run_time=.8)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        bg,gs,_=membrane(); self.add(bg,gs)
        self.at('Which of them'); self.play(FadeIn(T('Which builds the spike?',34).move_to([0,-2.3,0])),run_time=.4)
        self.finish()


class S02Three(SpokenScene):
    def construct(self):
        bg,gs,lab=membrane(); self.add(bg,gs)
        self.at('Nociceptor spikes')
        self.play(LaggedStart(*[FadeIn(l) for l in lab],lag_ratio=.75),run_time=1.6)
        self.finish()


class S03Names(SpokenScene):
    def construct(self):
        bg,gs,lab=membrane(); self.add(bg,gs,lab)
        for phrase,i in [('are',0),('and',1),('The third is',2)]:
            self.at(phrase)
            self.play(*[g.animate.set_opacity(1 if j==i else .18) for j,g in enumerate(gs)],
                      *[l.animate.set_opacity(1 if j==i else .25) for j,l in enumerate(lab)],
                      Indicate(gs[i],scale_factor=1.15,color=[ORANGE,TEAL_C,PURPLE][i]),run_time=.5)
        self.finish()


class S04Ttx(SpokenScene):
    def construct(self):
        bg,gs,lab=membrane()
        for g in gs: g.scale(1.08)
        self.add(bg,gs,lab)
        toxin=RoundedRectangle(width=1.15,height=.52,corner_radius=.2,color=RED,fill_color=RED,fill_opacity=.9).move_to([-4,2.3,0])
        label=T('tetrodotoxin',28,RED).move_to([-2.2,2.3,0])
        self.at('tetrodotoxin'); self.add(label,toxin)
        self.play(toxin.animate.move_to([-4,1.05,0]),Transform(gs[1],gate(0,0,'open',TEAL_C,2.32)),Transform(gs[2],gate(4,0,'open',PURPLE,2.32)),run_time=.65)
        bracket=VGroup(Line([-.7,-2.55,0],[4.7,-2.55,0],color=TEAL_C),*[Line([x,-2.4,0],[x,-2.55,0],color=TEAL_C) for x in [-.7,4.7]],T('tetrodotoxin resistant',28,TEAL_C).move_to([2,-2.95,0]))
        self.at('tetrodotoxin resistant'); self.play(FadeIn(bracket),run_time=.3)
        bracket.set_opacity(1)
        self.finish()


class S05Pore(SpokenScene):
    def construct(self):
        self.add(heading('Outer pore • schematic binding'))
        pores=VGroup(gate(-3,-.2,'ready',ORANGE,3.2),gate(2.7,-.2,'open',TEAL_C,3.2))
        self.add(pores,T('Sensitive pore',30,ORANGE).move_to([-3,-2.8,0]),T('Resistant pore',30,TEAL_C).move_to([2.7,-2.8,0]))
        # Labelled schematic tokens, without molecular geometry. The sensitive
        # token starts seated between the walls; the resistant token stays clear.
        a=RoundedRectangle(width=1.05,height=.55,corner_radius=.12,color=RED,fill_color=RED,fill_opacity=.85).move_to([-3,1.25,0])
        b=a.copy().move_to([4.7,2.05,0])
        self.add(a,b,lines(['guanidinium','group'],RED,22).move_to([-5.35,1.25,0]),
                 T('guanidinium group',22,RED).move_to([4.55,2.65,0]))
        # Residue ticks project from the inner faces of both pore walls.
        sensitive=VGroup(*[Line([x,1.05,0],[x+d,1.05,0],color=ORANGE,stroke_width=6)
                          for x,d in [(-3.68,.22),(-2.32,-.22)]])
        tick=Line([3.38,.65,0],[3.65,.65,0],color=TEAL_C,stroke_width=6)
        residue=lines(['weaker-grip','residue'],TEAL_C,26).move_to([5,.65,0])
        self.at('carry'); self.play(FadeIn(sensitive),FadeIn(tick),FadeIn(residue),run_time=.35)
        bounce=arr([2.7,2.25,0],[4.05,2.25,0],RED)
        self.at('weaken the'); self.play(GrowArrow(bounce),run_time=.5)
        self.at('so the toxin'); self.play(b.animate.shift(RIGHT*.25),run_time=.35,rate_func=there_and_back)
        self.add(T('conducting',28,TEAL_C).move_to([2.7,-3.4,0])); self.finish()


class S06Spike(SpokenScene):
    def construct(self):
        ax,cv,labels,f=spike_panel(); self.add(heading('Contributing to the spike'),ax,cv,labels)
        up=ax.plot(f,[.45,.78,.005],ORANGE,8)
        top=ax.plot(f,[.78,.96,.005],TEAL_C,8); shoulder=ax.plot(f,[1.15,1.5,.005],TEAL_C,8)
        self.at('and a'); self.play(Create(up),FadeIn(T('Nav1.7',28,ORANGE).move_to([-4,1.45,0])),run_time=.5)
        self.at('and', nth=1); self.play(Create(top),Create(shoulder),FadeIn(T('Nav1.8',28,TEAL_C).move_to([4.1,1.2,0])),run_time=.4)
        self.add(T('shoulder',28,TEAL_C).move_to([4.1,.25,0]),Line([3.1,.25,0],ax.c2p(1.35,f(1.35)),color=TEAL_C)); self.finish()


class S07Nine(SpokenScene):
    def construct(self):
        ax,cv,labels,f=spike_panel(); self.add(heading('Spike versus resting influence'),ax,cv,labels)
        self.at('mainly sets'); self.play(FadeIn(rest_panel()),run_time=.6); self.finish()


class S08Transient(SpokenScene):
    def construct(self):
        ax,base,cv,_=current_panel(); self.add(heading('Two kinds of current'),base,cv)
        self.at('a transient current'); self.play(FadeIn(subtitle('Transient • builds the spike')),run_time=.4)
        self.at('then inactivates'); self.play(Create(ax.plot(transient,[.7,4,.02],GREEN,7)),run_time=.6)
        self.add(T('within milliseconds',28,GREEN).move_to([2.5,.4,0]),arr([1,.2,0],ax.c2p(3,transient(3)),GREEN)); self.finish()


class S09Persistent(SpokenScene):
    def construct(self):
        ax,base,trans,per=current_panel(); trans.set_stroke(opacity=.25)
        self.add(heading('Persistent current'),base,trans,per)
        self.at('A persistent current'); self.play(Indicate(per,scale_factor=1.02),run_time=.5)
        self.at('Its inactivation'); self.play(FadeIn(subtitle('Inactivation: slow or incomplete')),run_time=.4); self.finish()


class S10Whichone(SpokenScene):
    def construct(self):
        ax,base,trans,per=current_panel(); trans.set_stroke(opacity=.25)
        head=heading('Persistent current'); self.add(head,base,trans,per)
        self.at('supplies a'); self.play(per.animate.set_color(PURPLE),Transform(head,heading('Nav1.9 supplies persistent current',PURPLE)),run_time=.5)
        self.at('Its slow gating'); self.play(FadeOut(base),FadeOut(trans),FadeOut(per),run_time=.25)
        sx,sp,sl,_=spike_panel(); panel=rest_panel()
        self.add(sx,sp,sl,panel)
        # Persistent current remains visible in a small, explicitly tagged record.
        small=Plot([0,8],[0,1.1],[3,-2.2],2.6,.6,[],[])
        self.remove(panel[-1]); self.add(small,small.plot(persistent,color=PURPLE,stroke_width=4),T('persistent',26,PURPLE).move_to([4.35,-2.65,0]))
        self.at('at rest'); self.play(Indicate(panel[3],scale_factor=1.04,color=PURPLE),run_time=.5); self.finish()


class S11Availability(SpokenScene):
    def construct(self):
        gs,legend=field(); self.add(heading('Availability'),gs,legend,subtitle('14 / 20 ready = 70%',GREEN))
        self.at('Availability is'); self.play(Indicate(gs[:14],scale_factor=1.02,color=GREEN),run_time=.6); self.finish()


class S12Cannot(SpokenScene):
    def construct(self):
        gs,legend=field(); counter=subtitle('14 / 20 ready = 70%',GREEN)
        self.add(heading('Availability'),gs,legend,counter)
        self.at('cannot open'); self.play(Indicate(gs[14:],scale_factor=1.05,color=RED),run_time=.45)
        self.at('when the membrane'); opened,_=field(True)
        self.play(Transform(gs,opened),Transform(counter,subtitle('Depolarizing step: 14 / 20 can open',GREEN)),run_time=.65); self.finish()


class S13Setby(SpokenScene):
    def construct(self):
        ax,base=curve_base(); cv=base[2]; self.add(*[x for x in base if x is not cv])
        formula=subtitle('h(V) = 1 / (1 + exp[(V − V½) / k])')
        self.at('Availability depends'); self.add(formula); self.play(Create(cv),run_time=1.4)
        t=ValueTracker(0)
        # Illustrative relaxation at fixed voltage toward its calculated h∞.
        val=lambda:h(-70)+(.95-h(-70))*np.exp(-t.get_value()/ .5)
        dot=always_redraw(lambda:Dot(ax.c2p(-70,val()),color=GREEN,radius=.11))
        info=always_redraw(lambda:band(['Held: −70 mV',f'Ready: {val():.2f}','settling → steady'],GREEN,.7))
        self.at('Hold one voltage'); self.add(marker(ax,-70,GREEN,False),dot,info)
        self.play(t.animate.set_value(2),run_time=1.75,rate_func=linear)
        self.at('availability settles'); self.play(t.animate.set_value(5),run_time=.5); self.finish()


class S14Params(SpokenScene):
    def construct(self):
        ax,base=curve_base(); self.add(base)
        midpoint=VGroup(marker(ax,-65),band(['V½ = −65 mV','h = 0.50'],GREEN,1.1))
        self.at('The curve has'); self.play(FadeIn(midpoint),run_time=.5)
        p,q=ax.c2p(-65,.82),ax.c2p(-58,.82)
        bracket=VGroup(Line(p,q,color=GREEN),Line(p+DOWN*.12,p+UP*.12,color=GREEN),Line(q+DOWN*.12,q+UP*.12,color=GREEN))
        k_label=T('k',26,GREEN).next_to(bracket,UP,buff=.14)
        self.at('a slope factor'); self.play(Create(bracket),FadeIn(k_label),run_time=.4)
        self.at('the slope is'); self.play(Transform(k_label,T('k ≈ 7 mV',26,GREEN).next_to(bracket,UP,buff=.14)),run_time=.35)
        self.at('Other subtypes')
        ghost=DashedVMobject(ax.plot(lambda v:h(v,-46),color=TEAL_C,stroke_width=3),num_dashes=36).set_stroke(opacity=.45)
        self.play(FadeIn(ghost),FadeIn(band(['Nav1.8: needs','its own','measured curve'],TEAL_C,-1.3)),run_time=.6)
        self.finish()


class S15Downhill(SpokenScene):
    def construct(self):
        ax,base=curve_base(); self.add(base); v=ValueTracker(-78)
        self.add(always_redraw(lambda:marker(ax,v.get_value())),
            always_redraw(lambda:band([f'Ready: {h(v.get_value()):.2f}'],GREEN,1)),
            always_redraw(lambda:mini_gauge(h(v.get_value()),y=.2)),
            always_redraw(lambda:band([f'Rest: {v.get_value():.0f} mV'],GREEN,-.7)))
        self.at('The more'); self.play(v.animate.set_value(-50),run_time=2.9,rate_func=linear); self.finish()


class S16Predict(SpokenScene):
    def construct(self):
        ax,base,marks,labels,q=prediction(); self.add(base)
        self.at('One rests low'); self.play(Create(marks[0]),FadeIn(labels[0]),run_time=.45)
        self.at('one rests high'); self.play(Create(marks[1]),FadeIn(labels[1]),run_time=.45)
        self.at('Which has more'); self.play(FadeIn(q),run_time=.35); self.finish()


class S17Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        ax,base,marks,labels,q=prediction(); self.add(base,marks,labels,q,band(['Pause and predict'],TEXT,-1.5)); self.wait(5)


class S18Reveal(SpokenScene):
    def construct(self):
        ax,base,marks,labels,_=prediction(); self.add(base,marks,labels,subtitle('V½ = −65 mV • k = 7 mV'))
        self.at('The low one'); self.play(FadeIn(Dot(ax.c2p(-70,h(-70)),color=GREEN)),run_time=.4)
        self.at('About two'); labels[0].become(band(['Low rest: −70 mV','h = 0.67 ≈ ⅔'],GREEN,1.3))
        self.at('against about'); labels[1].become(band(['High rest: −55 mV','h = 0.19 ≈ ⅕'],TEAL_C,-.2))
        self.play(FadeIn(Dot(ax.c2p(-55,h(-55)),color=TEAL_C)),run_time=.4); self.finish()


class S19Step(SpokenScene):
    def construct(self):
        ax,base=curve_base(sub='Same held step: +5 mV'); lo=marker(ax,-70); hi=marker(ax,-55,TEAL_C)
        self.add(base,lo,hi)
        pending=VGroup(band(['Low rest: −70 mV','h = 0.67'],GREEN,1.25),band(['High rest: −55 mV','h = 0.19'],TEAL_C,-.85)); self.add(pending)
        self.at('The low one'); pending[0].become(cost_box(True,False)[0])
        self.play(Transform(lo,marker(ax,-65)),run_time=.65); self.finish()


class S20Cost(SpokenScene):
    def construct(self):
        ax,base=curve_base(sub='Same held step: +5 mV'); hi=marker(ax,-55,TEAL_C)
        low=cost_box(True,False)[0]; high=cost_box(False,True)[1]
        self.add(base,marker(ax,-65),hi,low,high)
        # Transcript calls 'one' 'wind'; the unambiguous first two words are exact.
        self.at('The high'); high.become(cost_box(False,True)[1])
        self.play(Transform(hi,marker(ax,-50,TEAL_C)),run_time=.65)
        self.at('same step costs'); base[-1].become(subtitle('Step cost does not determine firing')); self.finish()


class S21Illustrative(SpokenScene):
    def construct(self):
        ax,base=curve_base(sub='Step cost does not determine firing'); costs=cost_box(); self.add(base,costs)
        self.at('Those midpoints'); self.play(FadeOut(costs),base[2].animate.set_stroke(opacity=.5),run_time=.4)
        alts=VGroup(*[ax.plot(lambda v,m=m:h(v,m),color=GREY,stroke_width=3).set_stroke(opacity=.4) for m in [-75,-55,-45]])
        dot=Dot(ax.c2p(-65,.5),color=ORANGE)
        tag=T('Illustrative V½',26,ORANGE).move_to([-.7,1.35,0])
        leader=Line(tag.get_bottom(),ax.c2p(-65,.5)+UP*.12,color=ORANGE)
        self.play(Create(alts),FadeIn(dot),FadeIn(tag),Create(leader),run_time=.6)
        self.at('The midpoint is'); self.play(FadeIn(band(['Measure a real','neuron’s curve'],TEXT,.2)),run_time=.5)
        base[-1].become(subtitle('direction holds, size does not')); self.finish()


class S22TwoThings(SpokenScene):
    def construct(self):
        self.add(heading('Depolarization does two things'),T('Closer to threshold',28).move_to([-3.25,2.5,0]),T('Fewer channels left to open',28).move_to([3.3,2.5,0]))
        panels=VGroup(*[RoundedRectangle(width=6,height=5.65,corner_radius=.15,color=GREY).move_to([x,-.55,0]) for x in [-3.25,3.25]])
        self.add(panels); v=ValueTracker(-70)
        ax=Plot([0,1],[-75,-45],[-5.3,-2.65],4.3,4.1,[],[-70,-60,-50]); self.add(ax,T('mV',26,GREY).move_to([-5.75,1.85,0]))
        threshold_y=ax.c2p(0,-50)[1]
        threshold_label=T('threshold (movable)',26,GREY).move_to([-3.1,threshold_y,0])
        self.add(DashedLine(ax.c2p(0,-50),ax.c2p(1,-50),color=GREY),
                 BackgroundRectangle(threshold_label,color=BG,fill_opacity=1,buff=.08),threshold_label)
        self.add(always_redraw(lambda:Line(ax.c2p(0,v.get_value()),ax.c2p(1,v.get_value()),color=PURPLE,stroke_width=6)),
            always_redraw(lambda:T(f'Rest: {v.get_value():.0f} mV',26,PURPLE).move_to([-3,-3.05,0])))
        outline=Rectangle(width=1.65,height=3.8,color=GREEN).move_to([3.3,-.5,0]); self.add(outline)
        self.add(always_redraw(lambda:Rectangle(width=1.5,height=3.65*h(v.get_value()),stroke_width=0,fill_color=GREEN,fill_opacity=.75).move_to([3.3,-2.33+3.65*h(v.get_value())/2,0])),always_redraw(lambda:T(f'{h(v.get_value()):.0%} available',30,GREEN).move_to([3.3,-2.95,0])))
        self.add(T('Available: 67% → 19%',26,GREEN).move_to([3.3,1.85,0]))
        self.wait(1)
        self.at('It closes'); self.play(v.animate.set_value(-55),run_time=1.2,rate_func=linear)
        self.at('and it costs'); self.play(Indicate(outline,scale_factor=1.03),run_time=.35); self.finish()


class S23Order(SpokenScene):
    def construct(self):
        self.add(heading('Ask in this order'))
        steps=[('1   Channel','What changed in the channel?',ORANGE,1.6),('2   Rest and availability','Resting potential and ready fraction',GREEN,-.35),('3   Firing','Whether the neuron fires',TEXT,-2.3)]
        # The first card is filled from the outset; no empty card placeholders.
        cards=[]
        for title,desc,c,y in steps:
            box=RoundedRectangle(width=11.5,height=1.65,corner_radius=.15,color=c).move_to([0,y,0])
            cards.append(VGroup(box,T(title,34,c).move_to([0,y+.3,0]),T(desc,28).move_to([0,y-.35,0])))
        self.add(cards[0]); self.at('What happened'); self.play(Indicate(cards[0],scale_factor=1.02),run_time=.4)
        self.at('then to rest'); self.play(FadeIn(cards[1]),run_time=.4)
        self.at('then to firing'); self.play(FadeIn(cards[2]),run_time=.4); self.finish()


class S24Takeaway(SpokenScene):
    def construct(self):
        self.add(heading('Availability is a reversible reserve'))
        v=ValueTracker(-70)
        outline=RoundedRectangle(width=2.6,height=5.3,corner_radius=.15,color=GREEN).move_to([-3.7,-.35,0]); self.add(outline)
        self.add(always_redraw(lambda:Rectangle(width=2.4,height=5.1*h(v.get_value()),stroke_width=0,fill_color=GREEN,fill_opacity=.7).move_to([-3.7,-2.9+2.55*h(v.get_value()),0])),
                 always_redraw(lambda:T(f'Available: {h(v.get_value()):.0%}',36,GREEN).move_to([2.2,.45,0])),
                 always_redraw(lambda:T(f'Resting voltage: {v.get_value():.0f} mV',28).move_to([2.2,-.1,0])))
        label=lines(['Sustained depolarization','−70 → −55 mV'],TEXT,28).move_to([2.2,1.65,0]); self.add(label,T('Illustrative Nav1.7-like curve',26,GREY).move_to([0,-3.55,0]))
        trace=Plot([0,2],[-75,-50],[.1,-2.65],4.8,.85,[],[-70,-55])
        trace_v=lambda t:-70+15*min(t,1) if t<=1 else -55-15*(t-1)
        self.add(trace,trace.plot(trace_v,color=PURPLE,stroke_width=4),
                 T('Resting voltage (mV)',22,GREY).move_to([2.5,-3.05,0]))
        phase=ValueTracker(0)
        self.add(always_redraw(lambda:Dot(trace.c2p(phase.get_value(),v.get_value()),color=PURPLE,radius=.08)))
        self.at('but a'); self.play(phase.animate.set_value(1),v.animate.set_value(-55),run_time=1.5,rate_func=linear)
        self.at('when the membrane'); label.become(lines(['Return to negative voltage','−55 → −70 mV'],TEXT,28).move_to([2.2,1.65,0]))
        self.play(phase.animate.set_value(2),v.animate.set_value(-70),run_time=2.2,rate_func=linear)
        self.at('The budget shows'); self.play(FadeIn(lines(['A step’s cost','≠ a firing prediction'],TEXT,32).move_to([2.2,-1.05,0])),run_time=.6); self.finish()


class S25End(EndCard):
    LINE='Availability is a reversible budget: it shows what a step costs, not whether the neuron fires.'
    def construct(self):
        self.add(lines(['Availability is a reversible budget:','it shows what a step costs,','not whether the neuron fires.'],TEXT,38).move_to([0,.4,0]),T('biochemistrypedia.com',26,TEAL).move_to([0,-1.7,0])); self.finish()
