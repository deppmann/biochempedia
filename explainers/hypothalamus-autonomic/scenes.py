"""Correction, Threshold and Gain — reviewer fix round.
COLOR MAP: BLUE plasma/blood; YELLOW thirst and sensory neurons; ORANGE AVP/P;
PURPLE Q; GREEN integration; RED opposition; TEAL feedback/cursor;
GOLD feedforward; GREY anatomy and axes. All response curves are computed.
"""
import numpy as np
from bp_style import *

ORANGE = '#F29E4C'
PURPLE = '#B6A0FF'
BLOOD, NEUR, AVP, EXC, INH, FB, FF = BLUE, YELLOW, ORANGE, GREEN, RED, TEAL, GOLD
THR, GAIN = 284., .43

def avp(p, threshold=THR, gain=GAIN):
    return gain * max(p-threshold, 0.)

class Ax:
    def __init__(self,x0,x1,y0,y1,t0,t1,v0,v1):
        self.x0,self.x1,self.y0,self.y1,self.t0,self.t1,self.v0,self.v1=x0,x1,y0,y1,t0,t1,v0,v1
    def X(self,t): return self.x0+(t-self.t0)/(self.t1-self.t0)*(self.x1-self.x0)
    def Y(self,v): return self.y0+(v-self.v0)/(self.v1-self.v0)*(self.y1-self.y0)
    def P(self,t,v): return np.array([self.X(t),self.Y(v),0.])

AX=Ax(-5.35,5.6,-2.45,2.6,276,294,-1,5)
PQ=Ax(-5.35,5.6,-2.45,2.6,276,294,-1,9)

def poly(a,pts,color,w=6):
    m=VMobject(stroke_color=color,stroke_width=w)
    return m.set_points_as_corners([a.P(x,y) for x,y in pts])
def dashed(p,q,color=GREY): return DashedLine(p,q,color=color,stroke_width=2.5,dash_length=.12)
def arr(p,q,color=GREY): return Arrow(p,q,buff=.09,color=color,stroke_width=4,tip_length=.2)
def label(s,y=3.25,color=TEXT,size=30): return T(s,size,color).move_to([0,y,0])
def leader(text,pos,target,color=TEXT,size=26):
    t=T(text,size,color).move_to(pos)
    delta=np.array(target)-t.get_center()
    if abs(delta[0])/max(t.width,.01)>abs(delta[1])/max(t.height,.01):
        start=t.get_right() if delta[0]>0 else t.get_left()
    else: start=t.get_top() if delta[1]>0 else t.get_bottom()
    line=Line(start,target,color=color,stroke_width=2)
    return VGroup(line,t)
def card(title,body,color,w=4.3,h=1.7,body_size=28):
    box=RoundedRectangle(width=w,height=h,corner_radius=.16,color=color,fill_color=color,fill_opacity=.09)
    title=T(title,30,color,weight=BOLD).move_to([0,h*.24,0])
    body=T(body,body_size,TEXT).move_to([0,-h*.15,0])
    return VGroup(box,VGroup(title,body))
def sigm(t,t0,t1):
    u=np.clip((t-t0)/(t1-t0),0,1)
    return u*u*(3-2*u)
def noisy(t,seed,amp):
    return amp*(np.sin(7.1*t+seed)*.5+np.sin(13.3*t+2*seed)*.3+np.sin(23.9*t+3*seed)*.2)

def axes(a=AX):
    g=VGroup(Line(a.P(276,0),a.P(294,0),color=GREY),Line(a.P(276,a.v0),a.P(276,a.v1),color=GREY))
    for p in (276,280,284,288,292):
        g.add(Line(a.P(p,0)+UP*.07,a.P(p,0)+DOWN*.1,color=GREY),M(str(p),26).move_to([a.X(p),-2.82,0]))
    for v in ((-1,0,1,3,5) if a is AX else (0,3,6,9)):
        g.add(Line(a.P(276,v)+LEFT*.08,a.P(276,v)+RIGHT*.08,color=GREY),M(str(v),26).move_to([-5.83,a.Y(v),0]))
    g.add(T('Plasma osmolality (mOsm/kg)',28,BLOOD).move_to([0,-3.35,0]),T('Vasopressin (pmol/L)',28,AVP).move_to([-3.6,3.17,0]))
    return g

def curve(threshold=THR,gain=GAIN,color=AVP,a=AX):
    return poly(a,[(276,avp(276,threshold,gain)),(threshold,0),(294,avp(294,threshold,gain))],color)
def numbers():
    th=leader('Threshold 284 mOsm/kg',[-2.5,-.5,0],AX.P(284,0),TEXT)
    ga=leader('Gain 0.43 pmol/L per mOsm/kg',[-.4,2.25,0],AX.P(290,avp(290)),AVP)
    return VGroup(th,ga)
def study(): return T('One regression • healthy adults • illustrative',26).move_to([.2,3.6,0])
def graph(nums=True):
    g=VGroup(axes(),curve())
    if nums: g.add(numbers(),study())
    return g

def pq_labels():
    return VGroup(T('P',30,AVP,weight=BOLD).move_to([5.95,PQ.Y(avp(294,280,.43)),0]),T('Q',30,PURPLE,weight=BOLD).move_to([5.95,PQ.Y(avp(294,284,.86)),0]),
        T('280',26,AVP).move_to([PQ.X(280),PQ.Y(0)+.36,0]),T('284',26,PURPLE).move_to([PQ.X(284),PQ.Y(0)+.36,0]))
def pq():
    # Q first: P's entire flat segment remains visible on top of Q's.
    return VGroup(axes(PQ),curve(284,.86,PURPLE,PQ),curve(280,.43,AVP,PQ),pq_labels())
def below_question():
    return VGroup(graph(),Dot(AX.P(282,0),radius=.12,color=TEAL),T('?',38,TEAL).move_to(AX.P(282,0)+DOWN*.48),T('Below threshold:\ndoes vasopressin change?',28).move_to([-2,1.1,0]))
def marker(p):
    top=max(avp(p,280,.43),avp(p,284,.86))
    return VGroup(dashed(PQ.P(p,0),PQ.P(p,top+.8)),T('?',36).move_to(PQ.P(p,top+1.25)))
def pq_questions():
    return VGroup(pq(),marker(281),marker(290),label('Who releases more at each marker?',3.58,size=28),T('281',26).move_to([PQ.X(281)+.3,-2.3,0]),T('290',26).move_to([PQ.X(290),-2.3,0]))

POS=[[-3.45,1.65,0],[3.45,1.65,0],[0,-1.6,0]]
def effector(which):
    text='Vasopressin (AVP) to kidney: saves water' if which==0 else 'Thirst → drinking: water in'
    return chip(text,AVP if which==0 else NEUR,27,pad=.18).move_to([0,-1.45 if which==0 else -2.35,0])
def loop(stage=0,negative=False):
    a=card('Held steady','Plasma osmolality' if stage>=1 else '',BLOOD).move_to(POS[0])
    b=card('Senses','SFO + OVLT → MnPO' if stage>=2 else '',NEUR).move_to(POS[1])
    c=card('Pushes back','',GREY,w=10.6,h=2.8).move_to(POS[2]); c[1][0].move_to([0,-.65,0])
    if stage>=3: c.add(effector(0),effector(1))
    paths=VGroup(arr([-1.2,1.65,0],[1.2,1.65,0]),arr([3.45,.75,0],[2,-.15,0]),arr([-2,-.15,0],[-3.45,.75,0],INH if negative else GREY))
    g=VGroup(a,b,c,paths)
    if negative: g.add(negative_badge(),label('Negative feedback',3.25,FB,34))
    return g

def negative_badge():
    p=np.array([-2.75,.3,0])
    circ=Circle(radius=.46,color=INH,fill_color=BG,fill_opacity=1).move_to(p)
    return VGroup(circ,T('−',48,INH).move_to(p),T('Osmolality falls',28,BLOOD).move_to([-4.75,.3,0]))

class S00Title(TitleCard):
    LESSON='Autonomic Control and the Hypothalamus'
    TITLE='Correction, Threshold and Gain'

class S01Question(SpokenScene):
    def construct(self):
        # Bright side-view mouse, continuous tapered tail and a true teardrop.
        fur='#C8CDD5'
        body=Ellipse(width=4.7,height=3.15,color=fur,fill_color=fur,fill_opacity=.5).move_to([-1.25,-.3,0])
        head=Ellipse(width=2.05,height=1.65,color=fur,fill_color=fur,fill_opacity=.6).move_to([1.35,.4,0])
        ear=Circle(radius=.65,color=fur,fill_color=fur,fill_opacity=.55).move_to([.8,1.62,0])
        inner=Circle(radius=.37,color=fur,stroke_width=2).move_to(ear)
        path=VMobject().set_points_smoothly([[-3.5,-.55,0],[-4.4,-1.25,0],[-5.45,-1.55,0],[-5.95,-.85,0],[-5.7,-.2,0]])
        tail=VGroup(*[Line(path.point_from_proportion(i/50),path.point_from_proportion((i+1)/50),color=fur,stroke_width=12*(1-i/50)+1) for i in range(50)])
        eye=Dot([1.7,.72,0],radius=.085,color=BG)
        nose=Dot([2.35,.22,0],radius=.1,color=fur)
        whiskers=VGroup(*[Line([2.05,.25,0],[2.8,y,0],color=fur,stroke_width=2) for y in (-.2,.3,.75)])
        foot=Line([-.4,-1.9,0],[.6,-1.9,0],color=fur,stroke_width=7)
        mouse=VGroup(tail,body,head,ear,inner,eye,nose,whiskers,foot)
        spout=VGroup(Line([3.2,3,0],[3.2,1.25,0],color=BLOOD,stroke_width=15),Line([3.2,1.25,0],[2.65,.95,0],color=BLOOD,stroke_width=15))
        drop=VMobject(color=BLOOD,fill_color=BLOOD,fill_opacity=1,stroke_width=2)
        drop.start_new_path(np.array([0,.27,0]))
        drop.add_cubic_bezier_curve_to([-.08,.08,0],[-.25,-.08,0],[-.18,-.22,0])
        drop.add_cubic_bezier_curve_to([-.1,-.39,0],[.1,-.39,0],[.18,-.22,0])
        drop.add_cubic_bezier_curve_to([.25,-.08,0],[.08,.08,0],[0,.27,0])
        drop.move_to([2.65,.62,0])
        self.add(mouse,spout,drop)
        self.at('starts to drink'); self.play(drop.animate.shift(DOWN*.25),run_time=.3)
        a=Ax(-3.3,5.35,.4,2.4,-1,5,0,1); b=Ax(-3.3,5.35,-2.3,-.3,-1,5,0,1)
        f=lambda t: .9*(1-sigm(t,0,1))+.08*sigm(t,0,1)+noisy(t,1.3,.025)*(1-sigm(t,0,1))+noisy(t,.4,.015)
        base=VGroup(Line(a.P(-1,0),a.P(5,0),color=GREY),Line(b.P(-1,0),b.P(5,0),color=GREY),T('Thirst neurons\ncontinuous',27,NEUR).move_to([-4.9,1.5,0]),T('Blood\ntwo samples',27,BLOOD).move_to([-4.9,-1.35,0]),label('Schematic • not measured data',3.55,size=26))
        tr=poly(a,[(t,f(t)) for t in np.linspace(-1,5,160)],NEUR)
        ticks=VGroup(dashed(a.P(0,1),b.P(0,0)))
        for t,name in ((0,'First lick'),(1,'1 min'),(5,'5 min')):
            ticks.add(Line(b.P(t,0)+UP*.08,b.P(t,0)+DOWN*.12,color=GREY),T(name,26).move_to([a.X(t),-2.75,0]))
        self.at('within a minute'); self.play(FadeOut(mouse),FadeOut(spout),FadeOut(drop),FadeIn(base),Create(tr),FadeIn(ticks),run_time=.65)
        self.at('yet its blood')
        samples=VGroup(*[Dot(b.P(t,.78),radius=.12,color=BLOOD) for t in (-1,5)])
        self.play(FadeIn(samples),FadeIn(T('Still raised',28,BLOOD).move_to([4.9,-.3,0])),run_time=.4)
        self.at('what are they reading'); self.play(FadeIn(label('What are they reading?',2.95,NEUR,32)),run_time=.4); self.finish()

class S02Loop(SpokenScene):
    def construct(self):
        base=loop(); self.add(base)
        self.at('held steady'); self.play(Indicate(base[0],color=BLOOD),run_time=.4)
        self.at('plasma osmolality')
        filled=loop(1)
        held=card('Held steady','Plasma osmolality',BLOOD,w=4.3,h=2.6).move_to(POS[0])
        held[1][1].move_to([-3.45,1.65,0]); filled[0].become(held)
        filled[3][2].become(arr([-2,-.15,0],[-2.25,.35,0]))
        self.play(Transform(base,filled),run_time=.5)
        # The drop is attached to the regulated-variable card, never a stray inset.
        drop=Ellipse(width=2.0,height=.65,color=BLOOD,fill_color=BLOOD,fill_opacity=.12).move_to([-3.45,.85,0])
        dots=VGroup(*[Dot([-3.45+x,.85+y*.6,0],radius=.075,color=BLOOD) for x,y in [(-.55,.1),(-.1,.25),(.4,.1),(.65,-.1),(0,-.22)]])
        self.at('concentration of'); self.play(FadeIn(drop),run_time=.3)
        self.at('dissolved particles'); self.play(FadeIn(dots),FadeIn(T('Dissolved particles',26,BLOOD).move_to([-3.45,3.35,0])),run_time=.4); self.finish()

class S04Sensors(SpokenScene):
    def construct(self):
        # Sagittal schematic: anterior is left; highlighted front wall borders the ventricle.
        brain=VMobject(color=GREY,fill_color=GREY,fill_opacity=.07,stroke_width=4)
        brain.set_points_smoothly([[-5.8,-1.2,0],[-6,0,0],[-5.5,1.9,0],[-4.1,2.75,0],[-2.2,2.9,0],[-.6,2.25,0],[.15,1,0],[.1,-.5,0],[-.7,-1.5,0],[-1.1,-2.65,0],[-1.9,-2.65,0],[-2.05,-1.5,0],[-3.8,-1.3,0],[-5.8,-1.2,0]])
        cerebellum=Ellipse(width=1.8,height=1.5,color=GREY).move_to([-.6,-1.1,0])
        vent=Polygon([-3.7,1.3,0],[-2.7,1.65,0],[-2.3,.65,0],[-2.8,-1.15,0],[-3.7,-.9,0],color=BLOOD,fill_color=BLOOD,fill_opacity=.14)
        wall=Line([-3.7,-.9,0],[-3.7,1.3,0],color=NEUR,stroke_width=7)
        spots=VGroup(Dot([-3.7,1.3,0],color=NEUR,radius=.14),Dot([-3.7,-.9,0],color=NEUR,radius=.14))
        sfo=card('SFO','Subfornical organ',NEUR,w=5.1,h=1.2,body_size=27).move_to([3.5,2.25,0])
        ovlt=card('OVLT','Organum vasculosum of\nthe lamina terminalis',NEUR,w=5.1,h=1.6,body_size=27).move_to([3.5,.4,0])
        mnpo=card('MnPO','Median preoptic nucleus',EXC,w=5.1,h=1.2,body_size=27).move_to([3.5,-1.5,0])
        # Both sensor names visible from the first spoken letters.
        anatomy=VGroup(brain,cerebellum,vent,wall,spots,sfo,ovlt,
            Line(spots[0].get_center(),sfo.get_left(),color=NEUR),Line(spots[1].get_center(),ovlt.get_left(),color=NEUR),
            leader('Third ventricle',[-1.4,3.3,0],[-2.9,.8,0],BLOOD,28),
            leader('Lamina terminalis',[-4.4,-2.5,0],[-3.7,-.35,0],NEUR,28),T('Front',26).move_to([-5.6,3.3,0]))
        self.add(anatomy)
        self.at('front wall'); self.play(Indicate(wall,color=NEUR),run_time=.5)
        # One barrier with two gaps; all signal paths stay on its brain side.
        barrier=VGroup(*[Line([-.9,lo,0],[-.9,hi,0],color=GREY,stroke_width=7) for lo,hi in ((-2.8,-2.45),(-.95,.95),(2.45,2.8))])
        s2=card('SFO','Subfornical organ',NEUR,w=4.1,h=1.3,body_size=27).move_to([-.9,1.7,0])
        o2=card('OVLT','Organum vasculosum of\nthe lamina terminalis',NEUR,w=4.8,h=1.4,body_size=25).move_to([-.9,-1.7,0])
        vessel=VGroup(Line([-5.7,-2.8,0],[-5.7,2.8,0],color=BLOOD,stroke_width=6),Line([-4.9,-2.8,0],[-4.9,2.8,0],color=BLOOD,stroke_width=6),T('Blood',30,BLOOD).move_to([-5.3,3.3,0]))
        headers=VGroup(T('Blood–brain barrier',28).move_to([-.9,3.3,0]),T('Gaps at SFO and OVLT',28).move_to([-1,-3.25,0]),T('Brain side',28).move_to([4.4,3.3,0]))
        self.at('they sample the blood'); self.play(FadeOut(anatomy),FadeIn(vessel),FadeIn(barrier),FadeIn(headers),FadeIn(s2),FadeIn(o2),run_time=.7)
        arrows=VGroup(arr([-4.8,1.7,0],[-3.05,1.7,0],BLOOD),arr([-4.8,-1.7,0],[-3.25,-1.7,0],BLOOD))
        self.at('blood directly'); self.play(*[GrowArrow(a) for a in arrows],run_time=.4)
        self.at('barrier is incomplete'); self.play(Indicate(s2[0]),Indicate(o2[0]),run_time=.5)
        m2=card('MnPO','Median preoptic\nnucleus',EXC,w=4.0,h=1.8,body_size=28).move_to([4.25,0,0])
        signals=VGroup(arr([1.2,1.7,0],[2.2,.5,0],EXC),arr([1.4,-1.7,0],[2.2,-.5,0],EXC))
        self.at('a third site'); self.play(FadeIn(m2),*[GrowArrow(a) for a in signals],FadeIn(T('Intact here',28).move_to([-2.7,0,0])),run_time=.4)
        self.at('integrates their signals'); self.play(Indicate(signals,color=EXC),FadeIn(T('Integrates',30,EXC).move_to([4.25,-1.45,0])),run_time=.5); self.finish()

class S05Effectors(SpokenScene):
    def construct(self):
        g=loop(2); self.add(g)
        self.at('two effectors'); self.play(Indicate(g[2]),run_time=.4)
        self.at('saves water',lead=.68); self.play(FadeIn(effector(0)),run_time=.4)
        self.at('thirst takes water'); self.play(FadeIn(effector(1)),run_time=.4); self.finish()

class S06Negative(SpokenScene):
    def construct(self):
        g=loop(3); self.add(g)
        self.at('both lower'); self.play(g[3][2].animate.set_color(INH),FadeIn(negative_badge()),run_time=.4)
        self.at('opposes the error'); self.play(Indicate(g[0],color=BLOOD),run_time=.4)
        self.at('negative feedback'); self.play(FadeIn(label('Negative feedback',3.25,FB,34)),run_time=.4); self.finish()

class S07Comparator(SpokenScene):
    def construct(self):
        g=loop(3); self.add(g)
        q=chip('Comparator?',TEXT,28).move_to([0,3.2,0])
        self.at('separate comparator'); self.play(FadeIn(q),run_time=.4)
        self.at('spread across'); self.play(FadeOut(q),g[1][0].animate.set_fill(NEUR,.28),run_time=.4)
        self.at('sensing and integrating'); self.play(Indicate(g[1],color=NEUR),FadeIn(label('Distributed comparison',3.25,NEUR,30)),run_time=.4)
        end=VGroup(T('System response:',28),T('threshold',28,TEXT),T('+ gain',28,AVP)).arrange(RIGHT,buff=.15).move_to([0,-3.45,0])
        self.at('summarize the result'); self.play(FadeIn(end),run_time=.4); self.finish()

class S09Graph(SpokenScene):
    def construct(self):
        self.add(axes(),study())
        flat=poly(AX,[(276,0),(284,0)],AVP)
        rising=poly(AX,[(284,0),(294,avp(294))],AVP)
        cursor=Dot(AX.P(276,0),color=TEAL,radius=.12); self.add(cursor)
        self.at('raise osmolality'); self.play(Create(flat),MoveAlongPath(cursor,flat),rate_func=linear,run_time=1.2)
        self.at('record vasopressin'); self.play(Indicate(cursor),run_time=.4)
        self.at('plot is flat'); self.play(Indicate(flat),FadeIn(numbers()[0]),run_time=.5)
        self.at('then rises'); self.play(Create(rising),MoveAlongPath(cursor,rising),FadeIn(numbers()[1]),rate_func=linear,run_time=.65)
        self.play(FadeOut(cursor),run_time=.2); self.finish()

class S10TwoNumbers(SpokenScene):
    def construct(self):
        g=VGroup(axes(),curve(),numbers()[1],study()); self.add(g)
        knee=Dot(AX.P(284,0),color=TEXT,radius=.13)
        self.at('the knee'); self.play(FadeIn(knee),run_time=.3)
        th=leader('Threshold 284 mOsm/kg\nWhen release starts',[-2.5,-.35,0],AX.P(284,0),TEXT,28)
        self.at('the threshold'); self.play(FadeIn(th),run_time=.3)
        self.at('release starts'); self.play(Indicate(knee),run_time=.3)
        triangle=poly(AX,[(286,avp(286)),(291,avp(286)),(291,avp(291))],YELLOW,6)
        rise=T('rise',26,YELLOW).move_to(AX.P(291,avp(288.5))+RIGHT*.45)
        run=T('run',26,YELLOW).move_to(AX.P(288.5,avp(286))+DOWN*.26)
        self.at('the slope'); self.play(Create(triangle),FadeIn(rise),FadeIn(run),run_time=.4)
        self.at('the gain'); self.play(FadeIn(T('Gain: how much',28,AVP).move_to([3,-2.2,0])),run_time=.3); self.finish()

class S11QBelow(SpokenScene):
    def construct(self):
        g=below_question(); g[1].move_to(AX.P(277,0)); g[2].move_to(AX.P(277,0)+DOWN*.48); self.add(g)
        self.at('suppose osmolality rises'); self.play(g[1].animate.move_to(AX.P(282,0)),g[2].animate.move_to(AX.P(282,0)+DOWN*.48),run_time=1.2); self.finish()

class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(below_question()); self.wait(5)

class S13ABelow(SpokenScene):
    def construct(self):
        g=below_question(); self.add(g)
        self.at('below threshold'); self.play(Transform(g[-1],T('No osmotic release\nbelow threshold',28,AVP).move_to([-3.2,1.25,0])),FadeOut(g[2]),run_time=.4)
        self.at('the line does not')
        # Expand the negative range so the entire rejected 276–284 extension is visible.
        a=Ax(-5.35,5.6,-2.45,2.6,276,294,-4,5)
        new=VGroup(Line(a.P(276,0),a.P(294,0),color=GREY),Line(a.P(276,-4),a.P(276,5),color=GREY),curve(a=a),
            T('Vasopressin (pmol/L)',28,AVP).move_to([-3.6,3.17,0]),T('Plasma osmolality (mOsm/kg)',28,BLOOD).move_to([0,-3.35,0]),study(),
            leader('Threshold 284 mOsm/kg',[1,-.65,0],a.P(284,0),TEXT),leader('Gain 0.43 pmol/L per mOsm/kg',[.4,2.25,0],a.P(290,avp(290)),AVP),
            T('No osmotic release\nbelow threshold',28,AVP).move_to([-3.2,1.25,0]))
        for p in (276,280,284,288,292):
            new.add(Line(a.P(p,0)+UP*.06,a.P(p,0)+DOWN*.08,color=GREY),M(str(p),26).move_to([a.X(p),-2.82,0]))
        for v in (-3,-1,0,3,5): new.add(M(str(v),26).move_to([-5.85,a.Y(v),0]))
        ext=DashedVMobject(poly(a,[(276,GAIN*(276-THR)),(284,0)],GREY,4),num_dashes=24)
        cross=Cross(stroke_color=INH,stroke_width=7).scale(.7).move_to(a.P(279,-1.8))
        self.play(FadeOut(g),FadeIn(new),Create(ext),Create(cross),FadeIn(T('−',40,INH).move_to(a.P(281,GAIN*(281-THR)))),FadeIn(T('not allowed (negative)',26,INH).move_to([-2.6,-2.15,0])),run_time=.5); self.finish()

class S14TwoPeople(SpokenScene):
    def construct(self):
        self.add(axes(PQ),label('Two hypothetical people',3.58,size=28))
        p=curve(280,.43,AVP,PQ); q=curve(284,.86,PURPLE,PQ)
        self.at('person p'); self.play(Create(p),FadeIn(pq_labels()[0]),FadeIn(pq_labels()[2]),run_time=.5)
        pl=leader('P: lower threshold',[-3.5,-.55,0],PQ.P(280,0),AVP,28)
        self.at('lower threshold'); self.play(FadeIn(pl),run_time=.3)
        self.at('person q'); self.play(Create(q),FadeIn(pq_labels()[1]),FadeIn(pq_labels()[3]),run_time=.5); self.bring_to_front(p)
        self.at('steeper gain'); self.play(FadeIn(leader('Q: steeper gain',[2.2,2.45,0],PQ.P(292,avp(292,284,.86)),PURPLE,28)),run_time=.3); self.finish()

class S15QPq(SpokenScene):
    def construct(self):
        self.add(pq())
        self.at('just above'); self.play(FadeIn(marker(281)),FadeIn(T('281',26).move_to([PQ.X(281)+.3,-2.3,0])),run_time=.3)
        self.at('who releases more'); self.play(FadeIn(label('Who releases more at each marker?',3.58,size=28)),run_time=.3)
        self.at('far above both'); self.play(FadeIn(marker(290)),FadeIn(T('290',26).move_to([PQ.X(290),-2.3,0])),run_time=.3); self.finish()

class S16Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(pq_questions()); self.wait(5)

class S17APq(SpokenScene):
    def construct(self):
        self.add(pq())
        near=VGroup(dashed(PQ.P(281,0),PQ.P(281,1.6)),Dot(PQ.P(281,avp(281,280,.43)),color=AVP,radius=.12),leader('P 0.43',[-3.5,-.55,0],PQ.P(281,.43),AVP,28))
        self.at('just above'); self.play(FadeIn(near),run_time=.3)
        near_title=label('At 281 mOsm/kg: P releases more',3.58,AVP,28)
        self.at('p does'); self.play(FadeIn(near_title),run_time=.3)
        zero=VGroup(Dot(PQ.P(281,0),color=PURPLE,radius=.1),leader('Q 0',[-1.5,-1.1,0],PQ.P(281,0),PURPLE,28))
        self.at('q has not'); self.play(FadeIn(zero),run_time=.3)
        self.at('far above both'); self.play(FadeOut(near),FadeOut(zero),FadeOut(near_title),run_time=.2)
        # Match the lesson's worked check; the picture clarifies 'above both'.
        far=VGroup(dashed(PQ.P(290,0),PQ.P(290,avp(290,284,.86))),Dot(PQ.P(290,avp(290,280,.43)),color=AVP,radius=.1),Dot(PQ.P(290,avp(290,284,.86)),color=PURPLE,radius=.1),T('290',26).move_to([PQ.X(290),-2.3,0]))
        self.play(FadeIn(far),run_time=.3)
        self.at('q does'); self.play(FadeIn(T('Above the crossing: Q releases more',28,PURPLE).move_to([1.7,2.55,0])),run_time=.3)
        vals=T(f'At 290: P {avp(290,280,.43):.2f} | Q {avp(290,284,.86):.2f} pmol/L',26).move_to([0,3.6,0])
        self.at('steeper line wins')
        cross=VGroup(Dot(PQ.P(288,3.44),color=TEXT,radius=.1),leader('Crossing: 288, 3.44',[.6,.75,0],PQ.P(288,3.44),TEXT,27))
        self.play(FadeIn(cross),FadeIn(vals),run_time=.4); self.finish()

class S18OneNumber(SpokenScene):
    def construct(self):
        point=PQ.P(288,3.44)
        glow=VGroup(*[Dot(point,radius=r,color=TEXT,fill_opacity=o,stroke_width=0) for r,o in ((.4,.06),(.28,.1),(.18,.2),(.09,1))])
        self.add(pq(),glow,leader('288, 3.44',[.45,.6,0],point,TEXT,28))
        c=chip('Set point?',TEXT,30).move_to([3.75,-1.15,0])
        self.at('a set point'); self.play(FadeIn(c),run_time=.3)
        self.at('cannot describe'); x=Cross(c,stroke_color=INH,stroke_width=6); self.play(Create(x),run_time=.3)
        self.at('at least two')
        remain=1.5-(self.elapsed()-(self.t_of('cannot describe')-.2))
        if remain>0: self.wait(remain)
        self.play(FadeOut(c),FadeOut(x),FadeIn(chip('Threshold + gain',TEXT,30).move_to(c)),run_time=.3); self.finish()

class S19Rule(SpokenScene):
    def construct(self):
        # Keep the full plot; the equation is a single connected card above it.
        a=Ax(-5.35,5.6,-2.1,1.8,276,294,-1,5)
        g=VGroup(Line(a.P(276,0),a.P(294,0),color=GREY),Line(a.P(276,-1),a.P(276,5),color=GREY),curve(a=a),T('Vasopressin (AVP)',28,AVP).move_to([-3.75,2.12,0]),T('Plasma osmolality (mOsm/kg)',28,BLOOD).move_to([0,-2.8,0]),T('One regression • healthy adults • illustrative',26).move_to([0,-3.4,0]))
        for p in (276,284,294): g.add(M(str(p),26).move_to([a.X(p),-2.25,0]))
        equation=T('Vasopressin (AVP) = gain × max(osmolality − threshold, 0)',36)
        equation.stretch_to_fit_width(12.1).move_to([0,3.05,0])
        box=RoundedRectangle(width=12.55,height=1.0,corner_radius=.15,color=AVP,fill_color=BG,fill_opacity=1).move_to(equation)
        self.add(g,box,equation)
        self.at('the line is measured'); self.play(Indicate(g[2],color=AVP),run_time=.4)
        slope=leader('gain',[.4,1.8,0],a.P(290,avp(290)),AVP,30)
        self.at('output is the gain'); self.play(FadeIn(slope),run_time=.3)
        bracket=VGroup(Line(a.P(284,0)+DOWN*.25,a.P(292,0)+DOWN*.25,color=FF,stroke_width=4),Line(a.P(284,0)+DOWN*.15,a.P(284,0)+DOWN*.35,color=FF),Line(a.P(292,0)+DOWN*.15,a.P(292,0)+DOWN*.35,color=FF),T('osmolality − threshold',28,FF).move_to([a.X(288),-1.95,0]))
        self.at('how far osmolality'); self.play(Create(bracket),run_time=.4)
        self.at('past threshold'); self.play(GrowArrow(arr(a.P(292,0),a.P(292,avp(292)),AVP)),FadeIn(T('output',28,AVP).move_to([a.X(292)+.6,a.Y(1.6),0])),FadeIn(T('Below threshold: zero',28).move_to([-3.1,-.7,0])),run_time=.4); self.finish()

class S20Estimate(SpokenScene):
    def construct(self):
        estimate=card('The estimate','Blood now + what is on its way',TEXT,w=10.8,h=1.75,body_size=30).move_to([0,.3,0]); self.add(estimate)
        blood=card('Blood now','Measured osmolality',BLOOD,w=5.0,h=1.7,body_size=28).move_to([-3.25,-2.4,0])
        ff=card('What is coming','Swallowed water /\nlearned cue',FF,w=5.0,h=1.7,body_size=28).move_to([3.25,-2.4,0])
        self.add(blood[0].copy().set_stroke(opacity=.2).set_fill(opacity=.02),ff[0].copy().set_stroke(opacity=.2).set_fill(opacity=.02))
        self.at('acting on an estimate'); self.play(Indicate(estimate),run_time=.4)
        response=chip('AVP / thirst',AVP,34,pad=.26).move_to([0,3,0])
        self.play(GrowArrow(arr([0,1.2,0],[0,2.5,0],AVP)),FadeIn(response),run_time=.3)
        self.at('feedback reads'); self.play(FadeIn(blood),GrowArrow(arr([-3.25,-1.5,0],[-2,-.65,0],FB)),FadeIn(T('Feedback',30,FB).move_to([-4.4,-1.05,0])),run_time=.5)
        self.at('feedforward adds'); self.play(FadeIn(ff),GrowArrow(arr([3.25,-1.5,0],[2,-.65,0],FF)),FadeIn(T('Feedforward',30,FF).move_to([4.4,-1.05,0])),run_time=.5); self.finish()

class S21Channels(SpokenScene):
    def construct(self):
        center=chip('Hypothalamus',TEXT,38).move_to([0,2.8,0]); self.add(center)
        n=card('Autonomic nerves','Heart rate',NEUR,w=5.4,h=1.6,body_size=30).move_to([-3.25,-.9,0])
        h=card('Pituitary hormones','Vasopressin',AVP,w=5.4,h=1.6,body_size=30).move_to([3.25,-.9,0])
        wire=VMobject(color=NEUR,stroke_width=5).set_points_as_corners([[-1,2.35,0],[-3.25,1.7,0],[-3.25,-.05,0]])
        vessel=VGroup(Line([1,2.35,0],[3.05,-.05,0],color=AVP,stroke_width=5),Line([1.35,2.35,0],[3.4,-.05,0],color=AVP,stroke_width=5))
        self.at('through nerves'); self.play(Create(wire),FadeIn(n),run_time=.4)
        pulse=Dot([-1,2.35,0],color=NEUR,radius=.1); self.add(pulse); self.play(MoveAlongPath(pulse,wire),run_time=.4); self.remove(pulse)
        self.at('often in seconds'); self.play(FadeIn(T('Often',30,NEUR).move_to([-3.25,-2.15,0])),Create(Line([-4.25,-3.15,0],[-2.25,-3.15,0],color=NEUR,stroke_width=8)),FadeIn(T('seconds',30,NEUR).move_to([-3.25,-2.7,0])),run_time=.4)
        self.at('through hormones'); self.play(Create(vessel),FadeIn(h),run_time=.4)
        self.at('usually build'); self.play(FadeIn(T('Usually',30,AVP).move_to([3.25,-2.15,0])),Create(Line([.9,-3.15,0],[5.6,-3.15,0],color=AVP,stroke_width=8)),FadeIn(T('minutes to hours',30,AVP).move_to([3.25,-2.7,0])),run_time=.6); self.finish()

def takeaway():
    return VGroup(card('Threshold','When',TEXT,w=5.2,h=2).move_to([-2.85,1.5,0]),card('Gain','How much',AVP,w=5.2,h=2).move_to([2.85,1.5,0]),card('The estimate','The blood, corrected for what is on its way',FF,w=11,h=2,body_size=30).move_to([0,-1.5,0]))

class S22Takeaway(SpokenScene):
    def construct(self):
        g=takeaway()
        for c in g:
            c[0].set_stroke(opacity=.35).set_fill(opacity=.03)
            c[1].set_opacity(.35)
        self.add(g)
        self.at('threshold says when'); self.play(Transform(g[0],takeaway()[0]),run_time=.3)
        self.at('gain says how much'); self.play(Transform(g[1],takeaway()[1]),run_time=.3)
        self.at('keep the word estimate'); self.play(Transform(g[2],takeaway()[2]),run_time=.3)
        self.at('thirst neurons'); self.play(Indicate(g[2],color=NEUR),run_time=.4); self.finish()

class S21End(EndCard):
    LINE='Threshold says when. Gain says how much. Keep the word estimate.'
    def construct(self):
        self.add(takeaway(),T('biochemistrypedia.com',26,TEAL).move_to([0,-3.15,0])); self.finish()
