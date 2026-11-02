"""Word-synchronised chapter, revised against the review and eight polish items.
COLOR MAP: YELLOW juice/reward/r; BLUE tone/light/cue; GREEN burst/positive error;
RED omission/negative error; TEAL prediction V; PURPLE dopamine neuron;
GREY schematic frames; TEXT baseline spikes. No molecular structures.
All spike trains are seeded inhomogeneous Poisson models: baseline 6 Hz,
burst 30 Hz for .18 s, omission 1.5 Hz for .35 s (reduced, never forced silent).
Histograms are counts of the displayed spikes / trials / bin width.
Prediction arithmetic: delta = r + V(next) - V(this), gamma=1.
"""
import numpy as np
from bp_style import *

LIGHT_GREY='#B9C0CD'
XS=[-4.7,-2.35,0,2.35,4.7]
LABELS=['waiting','tone','delay','juice','over']
VALUES=[0,1,1,1,0]


def heading(s,color=TEXT):
    return T(s,32,color).move_to([0,3.45,0])


def eqrow(parts,size=32,buff=.12):
    return VGroup(*[M(s,size,c) for s,c in parts]).arrange(RIGHT,buff=buff)


def rule():
    return eqrow([('δ =',GREEN),('r',YELLOW),('+',TEXT),('V(next moment)',TEAL),('−',TEXT),('V(this moment)',TEAL)],28).move_to([0,3.2,0])


def arithmetic(r,vnext,vnow):
    d=r+vnext-vnow
    return eqrow([('δ =',GREEN if d>0 else RED if d<0 else TEXT),(str(r),YELLOW),('+',TEXT),(str(vnext),TEAL),('−',TEXT),(str(vnow),TEAL),('= '+('+' if d>0 else '−' if d<0 else '')+str(abs(d)),GREEN if d>0 else RED if d<0 else TEXT)],36).move_to([0,3.2,0])


def monkey():
    ears=VGroup(*[Circle(.38,color=GREY,fill_opacity=.2).move_to([x,.8,0]) for x in (-.85,.85)])
    head=Circle(.9,color=GREY,fill_opacity=.18).move_to([0,.8,0])
    face=Ellipse(width=1.25,height=1.05,color=TEXT,fill_color=BG,fill_opacity=1).move_to([0,.6,0])
    eyes=VGroup(Dot([-.25,.95,0],radius=.06,color=TEXT),Dot([.25,.95,0],radius=.06,color=TEXT))
    body=Ellipse(width=1.6,height=1.9,color=GREY,fill_opacity=.15).move_to([0,-1,0])
    mouth=Line([.05,.25,0],[.45,.25,0],color=TEXT)
    return VGroup(body,ears,head,face,eyes,mouth)


def speaker():
    return VGroup(Rectangle(width=.6,height=1.1,color=BLUE),Polygon([.3,.55,0],[.95,.95,0],[.95,-.95,0],[.3,-.55,0],color=BLUE,fill_opacity=.25))


def waves(origin=(-3.9,.65,0)):
    # Shared arc centre preserves three distinct radii.
    return VGroup(*[Arc(radius=r,start_angle=-.65,angle=1.3,arc_center=origin,color=BLUE,stroke_width=4) for r in (.45,.8,1.15)])


def spout():
    return VGroup(Line([0,1,0],[0,0,0],color=LIGHT_GREY,stroke_width=7),Line([0,0,0],[-.55,0,0],color=LIGHT_GREY,stroke_width=7))


def drop():
    return Polygon([0,.32,0],[-.18,-.02,0],[-.13,-.2,0],[.13,-.2,0],[.18,-.02,0],color=YELLOW,fill_opacity=1,stroke_width=0)


def rig():
    m=monkey().scale(1.75).shift([2.5,-.05,0])
    s=speaker().scale(1.65).move_to([-4.3,.65,0])
    # Long horizontal delivery tube ends just above the mouth, clear of the face.
    p=VGroup(Line([5.25,2.45,0],[5.25,.65,0],color=LIGHT_GREY,stroke_width=8),
             Line([5.25,.65,0],[3.29,.65,0],color=LIGHT_GREY,stroke_width=8),
             Line([3.29,.65,0],[3.29,.48,0],color=LIGHT_GREY,stroke_width=8))
    return VGroup(m,s,p)


def neuron_icon():
    return VGroup(*[Line([0,0,0],[.95*np.cos(a),.95*np.sin(a),0],color=PURPLE,stroke_width=4) for a in (2.1,2.8,3.7,4.3)],Line([0,0,0],[1.45,0,0],color=PURPLE,stroke_width=5),Circle(.32,color=PURPLE,fill_color=PURPLE,fill_opacity=.45),Dot([1.5,0,0],radius=.1,color=PURPLE))


def electrode():
    n=neuron_icon().scale(3.1).shift([-2,.05,0])
    e=VGroup(Line([-.65,2.65,0],[-1.94,.55,0],color=LIGHT_GREY,stroke_width=7),
             Polygon([-2.04,.35,0],[-2.03,.7,0],[-1.8,.56,0],color=TEXT,fill_color=TEXT,fill_opacity=1),
             Line([-.65,2.65,0],[1.8,2.65,0],color=LIGHT_GREY,stroke_width=3))
    return VGroup(n,e)


def spike_times(burst=True,seed=13):
    rng=np.random.default_rng(seed); ts=np.arange(0,3,.005)
    rate=np.full(len(ts),6.)
    if burst: rate[(ts>=1.5)&(ts<1.68)]=30
    return ts[rng.random(len(ts))<rate*.005]


def trace(burst=False,x0=-5.3,width=10.6,y=-2.8):
    times=spike_times(burst)
    return VGroup(Line([x0,y,0],[x0+width,y,0],color=GREY),*[Line([x0+t/3*width,y-.16,0],[x0+t/3*width,y+.3,0],color=GREEN if burst and 1.5<=t<1.68 else TEXT,stroke_width=3) for t in times])


def raster(mode='reward',tone=False,neutral=False):
    rng=np.random.default_rng(1994); dt=.005; ts=np.arange(-1,2,dt)
    event=0
    rate=np.full(len(ts),6.)
    if not neutral: rate[(ts>=event)&(ts<event+.18)]=30
    if mode=='omit': rate[(ts>=1)&(ts<1.35)]=1.5
    rows=VGroup(); alltimes=[]
    def xx(t): return -4.8+(t+1)*3.5
    for i in range(12):
        spikes=ts[rng.random(len(ts))<rate*dt]; alltimes.extend(spikes)
        y=2.2-i*.23
        rows.add(VGroup(*[Line([xx(t),y-.085,0],[xx(t),y+.085,0],color=GREEN if not neutral and event<=t<event+.18 else TEXT,stroke_width=2.8) for t in spikes]))
    edges=np.arange(-1,2.001,.1); counts,_=np.histogram(alltimes,edges)
    bars=VGroup()
    for t,c in zip(edges[:-1],counts):
        h=max(.012,c/(12*.1)*.027)
        bars.add(Rectangle(width=.32,height=h,stroke_width=0,fill_color=GREEN if not neutral and event-1e-6<=t<event+.18 else LIGHT_GREY,fill_opacity=.85).move_to([xx(t+.05),-1.82+h/2,0]))
    axes=VGroup(Line([-4.8,-1.82,0],[5.7,-1.82,0],color=GREY),Line([-4.8,-1.82,0],[-4.8,-.55,0],color=GREY),T('trials',28,LIGHT_GREY).rotate(PI/2).move_to([-6,1,0]),T('spikes/s',28,LIGHT_GREY).rotate(PI/2).move_to([-6,-1.25,0]))
    for v in (0,20,40):
        axes.add(M(str(v),26,LIGHT_GREY).move_to([-5.2,-1.82+v*.027,0]))
    for t in (-1,0,1,2):
        axes.add(Line([xx(t),-1.82,0],[xx(t),-1.94,0],color=GREY),M(str(t),28).move_to([xx(t),-2.2,0]))
    axes.add(T('time (s from tone)' if tone else 'time (s from juice)',28,LIGHT_GREY).move_to([.5,-2.78,0]),T('schematic spikes • histogram from the same ticks',28,LIGHT_GREY).move_to([0,-3.4,0]))
    events=VGroup()
    for t,lab,col in ([(0,'tone',BLUE),(1,'juice due' if mode=='omit' else 'juice',YELLOW)] if tone else [(0,'juice',YELLOW)]):
        events.add(DashedLine([xx(t),-1.82,0],[xx(t),2.42,0],color=col,stroke_width=2),T(lab,28,col).move_to([xx(t),2.62,0]))
    return VGroup(rows,bars,axes,events)


def trial(values=None,bracket=True):
    values=[0]*5 if values is None else values
    boxes=VGroup(); bars=VGroup(); labels=VGroup()
    for i,(x,lab,v) in enumerate(zip(XS,LABELS,values)):
        col=BLUE if i==1 else YELLOW if i==3 else LIGHT_GREY
        b=RoundedRectangle(width=2.05,height=.85,corner_radius=.12,color=col,fill_opacity=.1).move_to([x,-1.35,0])
        boxes.add(VGroup(b,T(lab,32,col).move_to(b)))
        h=max(.025,2.65*v)
        bars.add(Rectangle(width=1.2,height=h,stroke_width=0,fill_color=TEAL,fill_opacity=.8).move_to([x,-.75+h/2,0]))
        labels.add(M('V = '+str(v),32,TEAL).move_to([x,-.42+2.65*v,0]))
    axes=VGroup(Line([-6.05,-.75,0],[-6.05,1.9,0],color=TEAL),T('V',32,TEAL).move_to([-6.05,2.4,0]),M('0',32,TEAL).move_to([-6.4,-.75,0]),M('1',32,TEAL).move_to([-6.4,1.9,0]))
    if bracket:
        axes.add(DoubleArrow([-2.35,-2.05,0],[2.35,-2.05,0],buff=0,color=LIGHT_GREY),T('1 s delay',32,LIGHT_GREY).move_to([0,-2.5,0]))
    return VGroup(boxes,bars,labels,axes)


def large_strip():
    boxes=trial()[0]
    for i,b in enumerate(boxes):
        b[0].stretch_to_fit_height(3.7); b.move_to([XS[i],-.15,0]); b[1].move_to([XS[i],-1.3,0])
        if i==1: b.add(speaker().scale(.6).move_to([XS[i],.45,0]))
        elif i==3: b.add(drop().scale(2).move_to([XS[i],.45,0]))
        elif i==2: b.add(Circle(.43,color=LIGHT_GREY).move_to([0,.45,0]),Line([0,.45,0],[0,.78,0],color=TEXT),Line([0,.45,0],[.3,.3,0],color=TEXT))
        elif i==0: b.add(T('…',52,LIGHT_GREY).move_to([XS[i],.45,0]))
        else: b.add(T('✓',48,LIGHT_GREY).move_to([XS[i],.45,0]))
    return VGroup(boxes,DoubleArrow([-2.35,-2.5,0],[2.35,-2.5,0],buff=0,color=LIGHT_GREY),T('1 s delay',30,LIGHT_GREY).move_to([0,-3,0]))


def strip_highlight(i,col=TEXT):
    return SurroundingRectangle(trial()[0][i],buff=.07,color=col,stroke_width=4)


def step(i,col=TEAL,compact=False):
    x1,x2=XS[i],XS[i+1]; y1=-.75+2.65*VALUES[i]; y2=-.75+2.65*VALUES[i+1]
    mid=(x1+x2)/2
    path=VGroup(Line([x1,y1,0],[mid,y1,0],color=col,stroke_width=6),Line([mid,y1,0],[mid,y2 if y1!=y2 else y2+.015,0],color=col,stroke_width=6),Arrow([mid,y2,0],[x2,y2,0],buff=0,color=col,stroke_width=6,max_tip_length_to_length_ratio=.18))
    if compact: path.scale(.86,about_point=ORIGIN).shift(UP*.35)
    return path


def math_strip():
    return trial(VALUES,False).scale(.86,about_point=ORIGIN).shift(UP*.35)


def readout(r='—',change='—',delta='—'):
    return VGroup(*[VGroup(T(lab,28,col).move_to([-2.3,y,0]),M(str(v),30,col).move_to([2.6,y,0])) for lab,v,col,y in [('reward r',r,YELLOW,-2),('V next − V this',change,TEAL,-2.6),('error δ',delta,GREEN if delta=='+1' else TEXT,-3.2)]])


def omission_question():
    st=trial(VALUES).scale(.83,about_point=ORIGIN).shift(DOWN*.25)
    mark=T('?',82,TEXT).move_to([1.95,2.38,0])
    q=heading('What happens when the juice is due?')
    # A compact, labelled rig sits beside the question, above the strip.
    m=monkey().scale(.48).shift([4.7,1.4,0]); p=spout().scale(.55).shift([5.25,1.58,0])
    dry=VGroup(m,p,T('empty spout',28,YELLOW).move_to([4.7,2.8,0]),Line([4.7,2.5,0],[5.15,2.15,0],color=YELLOW),speaker().scale(.5).move_to([-4.3,1.8,0]))
    return VGroup(st,mark,q,dry)


def light_icon():
    return VGroup(Circle(.22,color=BLUE,fill_opacity=.4),*[Line([.32*np.cos(a),.32*np.sin(a),0],[.52*np.cos(a),.52*np.sin(a),0],color=BLUE,stroke_width=3) for a in np.arange(0,TAU,TAU/8)]).move_to([-4.5,.05,0])


LIGHT_X=-4.8
TONE_X=1.2
JUICE_X=4.2


def light_strip():
    st=VGroup()
    for x,l,c,w in zip([LIGHT_X,TONE_X,2.7,JUICE_X],['light','tone','delay','juice'],[BLUE,BLUE,LIGHT_GREY,YELLOW],[2.4,1.4,1.4,1.4]):
        st.add(VGroup(RoundedRectangle(width=w,height=3.4,corner_radius=.15,color=c,fill_opacity=.12).move_to([x,-.7,0]),T(l,30,c).move_to([x,-1.65,0])))
    st[0].add(light_icon().move_to([LIGHT_X,-.05,0]))
    st[1].add(speaker().scale(.55).move_to([TONE_X,-.15,0]))
    st[3].add(drop().scale(1.6).move_to([JUICE_X,-.2,0]))
    return st


def gaps():
    # Cue-to-cue distances share one linear scale: 2 s is twice 1 s.
    return VGroup(DoubleArrow([LIGHT_X,-2.65,0],[TONE_X,-2.65,0],buff=.05,color=LIGHT_GREY),T('2 s',30).move_to([-1.8,-3.1,0]),DoubleArrow([TONE_X,-2.65,0],[JUICE_X,-2.65,0],buff=.05,color=LIGHT_GREY),T('1 s delay',30).move_to([2.7,-3.1,0]))


def cue_burst(x,y=1.5):
    # Positive model error at a cue changes the seeded rate from 6 to 30 Hz.
    times=spike_times(True,1994)
    return VGroup(*[Line([x+(t-1.59)*3,y-.3,0],[x+(t-1.59)*3,y+.3,0],color=GREEN,stroke_width=4) for t in times if 1.5<=t<1.68])


class S00Title(TitleCard):
    TITLE='The Tone and the Juice'
    LESSON='Feeding, Motivation and Reward'


class S01Question(SpokenScene):
    def construct(self):
        r=rig(); self.add(r)
        self.at('A sound comes'); self.play(Create(waves((-3.5,.65,0)).scale(1.25,about_point=[-3.5,.65,0])),run_time=.45)
        self.at('before juice'); d=drop().move_to([3.29,.48,0]); self.play(FadeIn(d),run_time=.15); self.play(d.animate.move_to([3.29,.36,0]),run_time=.45); self.play(FadeOut(d),run_time=.15)
        self.at('when does a'); self.play(FadeIn(heading('When does the neuron fire?')),run_time=.35); self.finish()


class S02Setup(SpokenScene):
    def construct(self):
        e=electrode(); e[1].shift(UP*.6); self.add(e,monkey().scale(1.08).shift([4.4,.05,0]),heading('single dopamine neuron',PURPLE),T('electrode',30,TEXT).move_to([.65,2.25,0]))
        self.at('recorded'); self.play(e[1].animate.shift(DOWN*.6),run_time=.5)
        self.at('in the midbrain'); self.play(FadeIn(T('single-unit recording',32).move_to([1.6,-2.4,0])),FadeIn(T('monkey midbrain • schematic',28,LIGHT_GREY).move_to([0,-3.1,0])),run_time=.35); self.finish()


class S03Electrode(SpokenScene):
    def construct(self):
        e=electrode().scale(.85).shift(LEFT*.4+UP*.5); self.add(e,heading('single-unit recording'))
        m=monkey().scale(1.05).shift([4.4,.35,0]); p=spout().scale(.7).shift([5.25,.68,0]); self.add(m,p,T('electrode',28,TEXT).move_to([.6,2.25,0]))
        self.at('picks up its spikes'); tr=trace(); self.play(Create(tr),FadeIn(T("one neuron's spikes",30).move_to([0,-2,0])),run_time=.6)
        self.at('drops of juice'); d=drop().move_to([4.865,.68,0]); self.play(FadeIn(d),run_time=.15); self.play(d.animate.move_to([4.865,.6,0]),Transform(tr,trace(True)),run_time=.55); self.play(FadeOut(d),run_time=.15)
        self.add(T('schematic spikes',28,LIGHT_GREY).move_to([0,-3.5,0])); self.finish()


class S04Raster(SpokenScene):
    def construct(self):
        r=raster(neutral=True); self.add(r[2],heading('One row, one trial; one tick, one spike'))
        self.at('each row'); self.play(LaggedStart(*[FadeIn(row) for row in r[0]],lag_ratio=.05),run_time=.65)
        self.at('each tick'); self.play(Indicate(r[0][4],color=TEXT,scale_factor=1.1),run_time=.35)
        self.at('lined up'); self.play(Create(r[3]),FadeIn(r[1]),run_time=.4); self.finish()


class S05Before(SpokenScene):
    def construct(self):
        r=raster(neutral=True); self.add(r,heading('A • juice without warning',YELLOW))
        self.at('juice arrives'); self.play(Indicate(r[3],color=YELLOW,scale_factor=1.02),run_time=.3)
        self.at('of the recorded neurons'); self.play(FadeIn(T('about 3/4 of neurons • two monkeys',28).move_to([0,2.96,0])),run_time=.3)
        self.at('brief burst'); new=raster(); self.play(Transform(r[0],new[0]),Transform(r[1],new[1]),run_time=.4); self.finish()


class S06After(SpokenScene):
    def construct(self):
        r=raster(); h=heading('A • juice without warning',YELLOW); self.add(r,h)
        self.at('a sound began'); self.play(FadeOut(h),FadeOut(r[0]),FadeOut(r[1]),FadeOut(r[3]),run_time=.25)
        new=raster('tone',True,True); self.play(FadeIn(new[0]),FadeIn(new[1]),FadeIn(new[3]),ReplacementTransform(r[2],new[2]),FadeIn(heading('B • learned tone → juice',BLUE)),run_time=.35)
        self.at('the burst came'); colored=raster('tone',True); self.play(Transform(new[0],colored[0]),Transform(new[1],colored[1]),run_time=.5)
        self.add(T('Mirenowicz and Schultz, 1994',28,LIGHT_GREY).move_to([0,2.96,0])); self.finish()


class S07After2(SpokenScene):
    def construct(self):
        r=raster('tone',True); self.add(r,heading('B • learned tone → juice',BLUE),T('Mirenowicz and Schultz, 1994',28,LIGHT_GREY).move_to([0,2.96,0]))
        self.at('little or no burst'); self.play(Create(Rectangle(width=.85,height=4.3,color=YELLOW).move_to([2.35,.3,0])),run_time=.4); self.finish()


class S08Why(SpokenScene):
    def construct(self):
        st=large_strip(); self.add(st,heading('Why should the burst move?'))
        self.at('Picture one trial'); self.play(Indicate(st[0],color=TEXT,scale_factor=1.015),run_time=.5); self.finish()


class S09Strip(SpokenScene):
    def construct(self):
        st=large_strip(); self.add(st)
        self.at('Waiting'); h=SurroundingRectangle(st[0][0],buff=.05,color=TEXT); self.play(Create(h),run_time=.2)
        self.at('then the tone'); self.play(Transform(h,SurroundingRectangle(st[0][1],buff=.05,color=BLUE)),run_time=.2)
        self.at('delay'); self.play(Transform(h,SurroundingRectangle(st[0][2],buff=.05,color=TEXT)),Indicate(st[2]),run_time=.2)
        self.at('then the juice'); self.play(Transform(h,SurroundingRectangle(st[0][3],buff=.05,color=YELLOW)),run_time=.2); self.finish()


class S10Predict(SpokenScene):
    def construct(self):
        big=large_strip(); self.add(big)
        self.at('Give each moment'); st=trial(); self.play(ReplacementTransform(big,st),run_time=.4)
        self.at('its own prediction'); self.play(Transform(st,trial(VALUES)),run_time=.65)
        self.at('still to come'); self.play(FadeIn(heading('prediction of reward still to come',TEAL)),run_time=.25); self.finish()


class S11Before(SpokenScene):
    def construct(self):
        st=trial(VALUES); self.add(st,heading('prediction of reward still to come',TEAL))
        self.at('prediction to zero'); self.play(Create(strip_highlight(0,TEAL)),Indicate(st[2][0]),run_time=.35)
        self.at('simplifying choice'); self.play(FadeIn(T('model choice',26,TEXT).move_to([-4.7,-.03,0])),run_time=.3)
        self.at('unpredictable times'); self.play(FadeIn(T('tone timing: unpredictable',30,BLUE).move_to([0,-3.2,0])),run_time=.3); self.finish()


class S12During(SpokenScene):
    def construct(self):
        st=trial(VALUES); self.add(st,heading('prediction of reward still to come',TEAL))
        self.at('prediction is high'); self.play(Indicate(st[1][1:4],color=TEAL,scale_factor=1.03),Indicate(st[2][1:4],scale_factor=1.05),run_time=.55); self.finish()


class S13Afterjuice(SpokenScene):
    def construct(self):
        st=trial(VALUES); self.add(st,heading('prediction of reward still to come',TEAL))
        self.at('prediction drops back'); self.play(Create(step(3)),run_time=.6)
        self.at('trial is over'); self.play(Create(strip_highlight(4,TEAL)),Indicate(st[2][4]),run_time=.3); self.finish()


class S14Rule(SpokenScene):
    def construct(self):
        st=math_strip(); rr=rule(); ro=readout().shift(RIGHT*2.5); self.add(st,ro)
        self.at('The error'); self.play(FadeIn(rr[0]),run_time=.2)
        self.at('reward that arrived'); self.play(FadeIn(rr[1]),run_time=.25)
        self.at('plus the change'); self.play(FadeIn(rr[2:]),run_time=.35)
        # Brackets touch the waiting and tone boxes and name the equation terms.
        links=VGroup()
        for i,term in [(0,'V(this)'),(1,'V(next)')]:
            bracket=Brace(st[0][i],DOWN,buff=.04,color=TEXT)
            label=T(term,28,TEXT).next_to(bracket,DOWN,buff=.07)
            links.add(bracket,label)
        self.play(FadeIn(links),FadeIn(T('no discounting here',30,TEXT).move_to([3.4,2.52,0])),run_time=.3); self.finish()



class S15Tone(SpokenScene):
    def construct(self):
        st=math_strip(); ro=readout(); self.add(st,ro)
        self.at('At the tone'); self.play(Create(SurroundingRectangle(st[0][1],buff=.05,color=BLUE)),run_time=.2)
        self.at('no reward arrives'); self.play(Transform(ro[0],readout(0)[0]),run_time=.25)
        self.at('prediction jumps up'); self.play(Create(step(0,TEAL,True)),Transform(ro[1],readout(0,'1 − 0 = +1')[1]),run_time=.45)
        self.at('That jump'); self.play(FadeIn(arithmetic(0,1,0)),Transform(ro[2],readout(0,'1 − 0 = +1','+1')[2]),run_time=.25)
        self.at('a burst'); self.play(Create(cue_burst(-3.05,2.65)),run_time=.3); self.finish()


class S16Delay(SpokenScene):
    def construct(self):
        st=math_strip(); ro=readout(); self.add(st,ro)
        self.at('During the delay'); self.play(Create(step(1,TEAL,True)),Transform(ro,readout(0,'1 − 1 = 0',0)),Create(trace(False,3.5,2.3,2.65)),FadeIn(T('steady firing',28).move_to([4.65,2.1,0])),run_time=.35)
        self.at('No error'); self.play(FadeIn(arithmetic(0,1,1)),run_time=.25); self.finish()


class S17Juice(SpokenScene):
    def construct(self):
        st=math_strip(); ro=readout(); self.add(st,ro)
        self.at('At the juice'); self.play(Create(SurroundingRectangle(st[0][3],buff=.05,color=YELLOW)),run_time=.2)
        self.at('reward arrives'); d=drop().scale(1.3).move_to([2.02,2.65,0]); self.play(FadeIn(d),FadeOut(st[2][3]),Transform(ro[0],readout(1)[0]),run_time=.25)
        self.at('prediction falls'); self.play(d.animate.move_to([2.02,-.18,0]),Create(step(3,TEAL,True)),Transform(ro[1],readout(1,'0 − 1 = −1')[1]),run_time=.65)
        self.at('They cancel'); self.play(FadeOut(d),FadeIn(st[2][3]),FadeIn(arithmetic(1,0,1)),Transform(ro[2],readout(1,'0 − 1 = −1',0)[2]),run_time=.3)
        self.at('No burst'); self.play(Create(trace(False,3.5,2.3,2.65)),FadeIn(T('no burst',28,TEXT).move_to([4.65,2.1,0])),run_time=.25); self.finish()


class S18Goodnews(SpokenScene):
    def construct(self):
        self.add(heading('Two routes to the same kind of error'))
        # Both routes use the same icon, explanation, arrow and error columns.
        def row(y,label,col,icon):
            return VGroup(icon,T(label,32,col).move_to([-.1,y,0]),Arrow([2.4,y,0],[3.4,y,0],color=GREEN),T('error',38,GREEN).move_to([4.6,y,0]))
        tonebox=chip('tone',BLUE,28).move_to([-4.5,.45,0])
        prediction=VGroup(Line([-5.6,.95,0],[-4.5,.95,0],color=TEAL,stroke_width=6),
            Line([-4.5,.95,0],[-4.5,2.05,0],color=TEAL,stroke_width=6),
            Line([-4.5,2.05,0],[-3.4,2.05,0],color=TEAL,stroke_width=6),
            M('0',28,TEAL).move_to([-5.7,1.35,0]),M('1',28,TEAL).move_to([-3.3,2.4,0]),tonebox)
        top=row(1.45,'news of reward\nto come',BLUE,prediction)
        self.add(top[0],top[1])
        self.at('makes an error'); self.play(FadeIn(top[2:]),run_time=.35)
        self.at('reward itself does'); bottom=row(-1.35,'reward arrives',YELLOW,drop().scale(2.3).move_to([-4.5,-1.35,0])); self.play(FadeIn(bottom),FadeIn(T('the same kind of error',36,GREEN).move_to([0,-3.1,0])),run_time=.4); self.finish()


class S19Q(SpokenScene):
    def construct(self):
        q=omission_question(); self.add(q[0],q[3])
        self.at('the tone sounds'); self.play(Create(waves((-3.7,1.8,0)).scale(.55,about_point=[-3.7,1.8,0])),run_time=.3)
        self.at('never comes'); self.play(FadeIn(q[1]),Indicate(q[3][2],color=YELLOW),run_time=.3)
        self.at('What happens'); self.play(FadeIn(q[2]),run_time=.3); self.finish()


class S20Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(omission_question())
        a=ValueTracker(TAU)
        ring=always_redraw(lambda: Arc(radius=.55,start_angle=PI/2,angle=max(.001,a.get_value()),arc_center=[1.95,2.38,0],color=BLUE,stroke_width=5))
        self.add(ring); self.play(a.animate.set_value(0),run_time=5,rate_func=linear)


class S21Reveal(SpokenScene):
    def construct(self):
        q=omission_question(); self.add(q)
        self.at('prediction still falls'); p=step(3,RED).scale(.83,about_point=ORIGIN).shift(DOWN*.25); self.play(Create(p),FadeOut(q[1]),run_time=.55)
        self.at('no reward'); self.play(FadeOut(q[2]),FadeIn(arithmetic(0,0,1)),run_time=.3)
        self.at('error is negative'); self.play(Create(SurroundingRectangle(q[0][0][3],buff=.06,color=RED)),run_time=.3); self.finish()


class S22Dip(SpokenScene):
    def construct(self):
        r=raster('omit',True); self.add(r)
        self.at('Firing pauses'); self.play(FadeIn(heading('pause at the time juice was due',RED)),run_time=.25)
        self.at('time the juice'); self.play(Create(Rectangle(width=1.22,height=4.3,color=RED).move_to([2.95,.3,0])),run_time=.35)
        self.at('recorded it'); self.play(FadeIn(T('Hollerman and Schultz, 1998',28,LIGHT_GREY).move_to([0,2.96,0])),run_time=.25); self.finish()


class S23Light(SpokenScene):
    def construct(self):
        st=light_strip(); light=st[0].copy(); toneonly=VGroup(*[box.copy() for box in st[1:]]); b=cue_burst(TONE_X); tag=heading('after learning, tone only',BLUE); self.add(toneonly,b,tag,T('in the model',28,TEAL).move_to([4.6,2.65,0]))
        self.at('add a light'); self.play(FadeIn(light),run_time=.35)
        self.at('unpredictable times'); self.play(FadeIn(T('unpredictable',30,BLUE).move_to([LIGHT_X,2.5,0])),run_time=.25)
        self.at('before the tone'); self.play(FadeIn(gaps()),run_time=.35)
        self.at('burst moves'); self.play(b.animate.shift(LEFT*6),Transform(tag,heading('after learning with light',BLUE)),run_time=.65); self.finish()


class S24Earliest(SpokenScene):
    def construct(self):
        st=light_strip(); self.add(st,gaps(),heading('after learning with light',BLUE),cue_burst(LIGHT_X),T('in the model',28,TEAL).move_to([4.6,2.65,0]))
        self.at('tone is already expected'); self.play(st[1][2].animate.shift(DOWN*.55),Transform(st[1][0],DashedVMobject(st[1][0].copy(),num_dashes=28)),FadeIn(T('already\nexpected',24,BLUE).move_to([TONE_X,.5,0])),run_time=.35)
        self.at('adds no error'); self.play(FadeIn(M('δ = 0',32,TEXT).move_to([TONE_X,2.3,0])),FadeIn(M('δ = +1',32,GREEN).move_to([LIGHT_X,2.3,0])),run_time=.3)
        self.at('first cue'); self.play(Create(SurroundingRectangle(st[0],buff=.08,color=GREEN)),run_time=.35); self.finish()


class S25Caution(SpokenScene):
    def construct(self):
        self.add(heading('What does a recording establish?'),T('recorded firing',34).move_to([-3.5,2,0]),trace(True,-5.6,4.2,.8))
        self.at('firing matches the error'); self.play(FadeIn(M('δ = +1',40,GREEN).move_to([3.5,.8,0])),Create(DoubleArrow([-1,.8,0],[1.7,.8,0],color=GREEN)),FadeIn(T('correlation',32,LIGHT_GREY).move_to([0,-.25,0])),run_time=.4)
        self.at('Does the burst'); self.play(FadeIn(VGroup(RoundedRectangle(width=10.5,height=2.1,corner_radius=.15,color=GREY).move_to([0,-2.1,0]),T('Does the burst teach?     ?',42).move_to([0,-2.1,0]))),run_time=.35); self.finish()


def rat_icon():
    return VGroup(Ellipse(width=2.5,height=1.25,color=LIGHT_GREY,fill_opacity=.15),Circle(.45,color=LIGHT_GREY,fill_opacity=.15).move_to([1.2,.25,0]),Circle(.2,color=LIGHT_GREY).move_to([1.2,.7,0]),Dot([1.4,.3,0],radius=.05,color=TEXT),Line([-1.25,0,0],[-1.85,-.4,0],color=LIGHT_GREY))


def experiment_panel(x,stim=False):
    border=RoundedRectangle(width=5.9,height=3.8,corner_radius=.15,color=GREY).move_to([x,.1,0])
    label=T('B • light → burst at reward' if stim else 'A • no imposed burst',28,GREEN if stim else TEXT).move_to([x,1.55,0])
    a=chip('A',BLUE,30).move_to([x-1.9,.65,0]); arrow=Arrow([x-1.1,.65,0],[x+.15,.65,0],color=TEXT,buff=.03); juice=drop().scale(1.2).move_to([x+.6,.65,0]); jl=T('juice',28,YELLOW).move_to([x+1.7,.65,0])
    cue=VGroup(chip('+ X',BLUE,28).move_to([x-1.8,-.35,0]),Arrow([x-1.2,-.35,0],[x-.2,.45,0],buff=.06,color=BLUE)); lab=T('responding to X • schematic',25).move_to([x,-1.35,0]); axis=Line([x+.1,-.85,0],[x+2.3,-.85,0],color=LIGHT_GREY)
    # Qualitative comparison only: lengths do not claim measured experimental values.
    height=.85 if stim else .22
    bar=Rectangle(width=.5,height=height,fill_color=GREEN if stim else GREY,fill_opacity=.85,stroke_width=0).move_to([x+1.2,-.85+height/2,0])
    return VGroup(border,label,a,arrow,juice,jl,cue,lab,axis,bar)


class S26Steinberg(SpokenScene):
    def construct(self):
        a=experiment_panel(-3.15); b=experiment_panel(3.15,True)
        self.add(heading('Steinberg and colleagues, 2013',LIGHT_GREY),a[:6])
        self.at('a cue added'); self.play(FadeIn(a[6]),run_time=.25)
        self.at('learned poorly'); self.play(FadeIn(a[7:]),run_time=.3)
        self.at('burst imposed with light'); self.play(FadeIn(b[:7]),run_time=.35)
        rat=rat_icon().scale(.48).move_to([1.5,-2.65,0])
        neuron=neuron_icon().scale(.6).move_to([4.7,-2.65,0])
        fibre=VGroup(Line([1.9,-1.95,0],[1.9,-2.45,0],color=BLUE,stroke_width=6),Line([1.9,-1.95,0],[4.45,-1.95,0],color=BLUE,stroke_width=4),Line([4.45,-1.95,0],[4.45,-2.55,0],color=BLUE,stroke_width=5))
        nl=T('midbrain neuron',24,PURPLE).move_to([4.75,-3.3,0]); self.play(FadeIn(rat),FadeIn(neuron),Create(fibre),FadeIn(nl),run_time=.3)
        glow=Dot([4.45,-2.65,0],radius=.23,color=BLUE,fill_opacity=.8)
        self.at('at reward'); self.play(Indicate(b[4],color=YELLOW),FadeIn(glow),Flash([4.45,-2.65,0],color=BLUE,line_length=.25,flash_radius=.35),run_time=.4)
        self.at('respond to it more'); self.play(FadeIn(b[7:]),run_time=.35)
        self.at('an imposed burst is enough'); self.play(FadeIn(T('imposed burst: enough',30,GREEN).move_to([-3.15,-2.65,0])),run_time=.3)
        self.at('natural bursts are needed'); self.play(FadeIn(T('natural bursts needed?\nNot established here.',26,LIGHT_GREY).move_to([-3.15,-3.35,0])),run_time=.3); self.finish()


class S27Takeaway(SpokenScene):
    def construct(self):
        st=trial(VALUES); self.add(st)
        self.at('reward plus the change'); eq=rule(); self.play(FadeIn(eq),run_time=.4)
        self.at('After training'); new=light_strip(); self.play(FadeOut(st),FadeIn(new),run_time=.5)
        self.at('first cue'); self.play(Create(SurroundingRectangle(new[0],buff=.08,color=GREEN)),FadeIn(cue_burst(LIGHT_X)),FadeIn(T('burst at the first cue',30,GREEN).move_to([-3.8,2.4,0])),FadeIn(T('nothing else predicted',34,GREEN).move_to([0,-3.1,0])),run_time=.4); self.finish()


class S28End(EndCard):
    LINE='The error is the reward plus the change in prediction.'
