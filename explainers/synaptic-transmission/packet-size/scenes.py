"""Chapter 5: model-computed response geometry and HH trace.
COLOR MAP: BLUE terminal; YELLOW ACh/packets/filling; GREEN voltage;
TEAL calcium; PURPLE magnesium; PINK receptors; ORANGE threshold/safety;
RED failure; GOLD highlight; GREY membranes/axes. Na+ YELLOW; K+ PURPLE. Proteins are schematics.
Model: g_rest=1, E_rest=-90, E_ACh=0, g_packet=q/90.
"""
import numpy as np
from bp_style import *
ORANGE='#F29E4C'
PINK='#E88FC0'
PURPLE='#B58CD9'
_BaseSpokenScene=SpokenScene
class SpokenScene(_BaseSpokenScene):
    def at(self,phrase,lead=.2,nth=0):
        target=self.t_of(phrase,nth)-lead
        if target-self.elapsed()>.02:self.wait(target-self.elapsed())

def label(s,x=0,y=3,size=30,color=TEXT):
    return T(s,size,color,line_spacing=1.1).move_to([x,y,0])
def dep(n,q=.4):return 90*n*q/(90+n*q)
def vx(v):return -5.1+(v+90)/90*10.2

def packet(full=True):
    pts=[[-.32,.23,0],[.1,.3,0],[.35,.02,0],[-.1,-.12,0],[-.32,-.3,0],[.2,-.3,0]]
    return VGroup(*[Dot(p,radius=.095,color=YELLOW) for p in pts[:6 if full else 3]])

def receptor(opened=False):
    # A large labelled schematic, not a structural molecular drawing.
    g=.55 if opened else .16
    bodies=VGroup(*[RoundedRectangle(width=1.0,height=3.35,corner_radius=.25,color=PINK,fill_opacity=.25).move_to([s*(.5+g/2),-.6,0]) for s in [-1,1]])
    pockets=VGroup(*[RoundedRectangle(width=.9,height=.62,corner_radius=.12,color=PINK,fill_color=BG,fill_opacity=1).move_to([s*1.16,.65,0]) for s in [-1,1]])
    gate=Line([-.36,-.85,0],[.36,-.85,0],color=PINK,stroke_width=12).set_opacity(0 if opened else 1)
    return VGroup(bodies,pockets,gate)
def large_receptor(opened=False):
    return receptor(opened).stretch(1.48,1,about_point=[0,-.6,0])
def large_ach_pair():return ach_pair().shift(UP*.6)
def ach_pair():return VGroup(*[chip('ACh',YELLOW,26,pad=.1).move_to([s*1.16,.65,0]) for s in [-1,1]])
def membrane():
    return VGroup(Rectangle(width=11.6,height=.65,color=GREY,fill_opacity=.2).move_to([0,-1.3,0]),label('muscle membrane',3.9,-2.0,28,GREY),label('nicotinic receptor · schematic',0,-3.5,30,PINK))
def terminal_edge():
    return VGroup(Line([-5.8,2.65,0],[5.8,2.65,0],color=BLUE,stroke_width=5).set_opacity(.5),label('terminal edge',-4.2,3.1,26,BLUE),label('cleft',4.7,1.8,28,GREY))
def rail():
    g=VGroup(Line([-5.1,-.65,0],[5.1,-.65,0],color=GREY,stroke_width=5))
    for v in [-90,-60,-30,0]:
        x=vx(v);g.add(Line([x,-.9,0],[x,-.4,0],color=GREY),label(f'{v} mV',x,-1.4,30))
    g.add(label('rest',-5.1,-2.05,28,GREY))
    return g
def marker(v,ghost=False):
    x=vx(v)
    if ghost:return VGroup(Square(.48,color=TEXT,fill_opacity=.2).rotate(PI/4).move_to([x,.65,0]),label('balance point',max(-3.8,min(3.8,x+1.5)),1.45,30))
    return VGroup(Dot([x,-.65,0],radius=.22,color=GREEN),label('Vm',x,-2.65,32,GREEN))
def rope(v,width=13):
    return Arrow([vx(v),.65,0],[5.1,.65,0],buff=.12,color=PINK,stroke_width=width,max_stroke_width_to_length_ratio=50)

BASE=-2.45
SCALE=.215
def by(v):return BASE+v*SCALE
def bar(n=60,x=-3.3,linear=False,q=.4,width=1.7):
    vals=[i*q if linear else dep(i,q) for i in range(n+1)]
    return VGroup(*[Rectangle(width=width,height=(vals[i+1]-vals[i])*SCALE,stroke_width=0,fill_color=GREEN,fill_opacity=.95 if i%2==0 else .48).move_to([x,by((vals[i+1]+vals[i])/2),0]) for i in range(n)])
def response_axes():
    g=VGroup(Line([-5.3,BASE,0],[-5.3,3.0,0],color=GREY),Line([-5.3,BASE,0],[5.7,BASE,0],color=GREY),label('response above rest (mV)',0,3.35,30))
    for v in [0,12,24]:g.add(label(str(v),-5.85,by(v),28),Line([-5.4,by(v),0],[-5.2,by(v),0],color=GREY))
    return g
def threshold():
    return VGroup(DashedLine([-5.25,by(12),0],[5.5,by(12),0],color=ORANGE),label('12 mV needed to fire',2.6,by(12)-.5,28,ORANGE))
def caveat():return label('Steady-state illustration; not a measured peak',0,-3.55,28)
def safety_stage(thr=True):
    g=VGroup(response_axes(),bar(),label('60 packets',2.4,2.5,34,YELLOW),label('about 19 mV',2.4,1.7,36,GREEN),caveat())
    if thr:g.add(threshold())
    return g

def factors(highlight=None):
    return VGroup(label('response ≈',-3.6,3.15,32),label('count, m',-.35,3.15,34,YELLOW if highlight!='size' else TEXT),label('×',1.3,3.15,34),label('size, q',3.15,3.15,34,GREEN if highlight!='count' else TEXT))
def small_receptor(x):
    return receptor().scale(.56).move_to([x,-.7,0])
QUESTION_X=[-4.9,-2.94,-.98,.98,2.94,4.9]
def question_receptors():
    return VGroup(*[receptor().scale(.72).stretch(1.5,1).move_to([x,-.85,0]) for x in QUESTION_X])
def question_state():
    recs=question_receptors()
    return VGroup(factors(),Rectangle(width=11.6,height=.5,color=GREY,fill_opacity=.2).move_to([0,-1.2,0]),recs[2],recs[4],label('Receptors removed',0,1.95,32,PINK),label('Which factor changes: count or size?',0,-3.35,36,YELLOW))
def packet_bars(q=.4):
    return VGroup(*[Rectangle(width=1.3,height=4.15*q/.4,color=GREEN,fill_opacity=.7).move_to([x,-2.0+2.075*q/.4,0]) for x in [-3.5,-1.2,1.2,3.5]])
def packet_plot():
    old=VGroup(*[DashedVMobject(b.copy().set_fill(opacity=0).set_stroke(GREY,2),num_dashes=28) for b in packet_bars()])
    return VGroup(old,Line([-4.7,-2,0],[-4.7,2.3,0],color=GREY),label('response per packet',0,2.55,28,GREEN),label('0',-5.1,-2,28),label('0.40 mV',-5.65,2.15,26),label('count m: 4 bars, unchanged (assumed)',0,-2.55,28,YELLOW))

class S00Title(TitleCard):
    LESSON='Synaptic Transmission and Quantal Release'
    TITLE='The Size of a Packet and the Margin of Safety'
    def construct(self):
        title=VGroup(T('The Size of a Packet',44,font=TITLE_FONT).move_to([0,.4,0]),T('and the Margin of Safety',44,font=TITLE_FONT).move_to([0,-.4,0]))
        self.add(label('BIOCHEMISTRYPEDIA',y=2.5,size=26,color=TEAL),label(self.LESSON,y=1.6,size=28),title,Line([-1.2,-1.4,0],[1.2,-1.4,0],color=GOLD));self.finish()

class S01Question(SpokenScene):
    def construct(self):
        term=Rectangle(width=5.4,height=2.0,color=BLUE,fill_opacity=.15).move_to([-3.1,2,0]);ves=Circle(.65,color=YELLOW).move_to([-3.1,1.8,0]);pk=packet().move_to(ves)
        mem=Rectangle(width=5.4,height=.5,color=GREY,fill_opacity=.2).move_to([-3.1,-1.8,0]);recs=VGroup(*[small_receptor(x).shift(DOWN*.8) for x in [-4.6,-3.1,-1.6]])
        q1=label('What sets\none packet’s size?',2.9,2,34);q2=label('How far above\nthreshold?',2.9,-.35,34);q2.align_to(q1,LEFT)
        self.add(term,ves,pk,mem,recs)
        self.at('What sets');self.play(ves.animate.move_to([-3.1,1,0]),pk.animate.move_to([-3.1,1,0]),FadeIn(q1),run_time=.6)
        opening=Arc(radius=.65,start_angle=-PI*.12,angle=PI*1.24,color=YELLOW).move_to([-3.1,1,0]);self.play(Transform(ves,opening),pk.animate.shift(DOWN*1.5),run_time=.7)
        self.at('how far above');mini=VGroup(Line([.6,-2.5,0],[5.4,-2.5,0],color=GREY),DashedLine([.6,-1.85,0],[5.4,-1.85,0],color=ORANGE),Rectangle(width=.7,height=1.25,color=GREEN,fill_opacity=.6).move_to([1.4,-1.875,0]),label('threshold',4.1,-1.45,26,ORANGE));self.play(FadeIn(q2),FadeIn(mini),run_time=.5);self.finish()

class S02Twothings(SpokenScene):
    def construct(self):
        self.add(label('Membrane and recording held steady',y=3.2,size=30))
        v1=Circle(1.0,color=YELLOW).move_to([-3,1.2,0]);v2=v1.copy().move_to([3,1.2,0]);p1=packet(False).move_to(v1);p2=packet().move_to(v2)
        rs=VGroup(*[small_receptor(x).scale(.65).move_to([x,-1.7,0]) for x in [-3,1.8,3,4.2]])
        self.add(v1,v2,p1,p2,rs,label('packet size q',0,-3.2,32,GREEN))
        self.at('How much transmitter');self.play(FadeIn(label('vesicle filling',y=2.4,size=34,color=YELLOW)),FadeIn(label('half-full',-3,-.1,28,YELLOW)),FadeIn(label('full',3,-.1,28,YELLOW)),Indicate(p2),run_time=.6)
        self.at('how many receptors')
        self.play(Indicate(rs),FadeIn(label('few',-3,-2.65,28,PINK)),FadeIn(label('many',3,-2.65,28,PINK)),FadeIn(label('receptors facing it',0,-.65,32,PINK)),run_time=.6);self.finish()

class S03Receptor(SpokenScene):
    def construct(self):
        r=large_receptor();a=large_ach_pair();a[0].move_to([-2.5,2.3,0]);a[1].move_to([2.5,2.3,0]);self.add(membrane(),terminal_edge(),r,a)
        self.at('Acetylcholine crosses');self.play(a.animate.shift(DOWN*.8),run_time=.7)
        self.at('binds nicotinic');self.play(Indicate(r[1]),run_time=.5)
        self.at('normally needs');self.play(a[0].animate.move_to([-1.16,1.25,0]),run_time=.5)
        self.at('acetylcholine molecules');self.play(a[1].animate.move_to([1.16,1.25,0]),run_time=.5)
        self.at('bound to open');self.play(Transform(r,large_receptor(True)),run_time=.5);self.finish()

class S04Reversal(SpokenScene):
    def construct(self):
        self.add(membrane(),large_receptor(True),large_ach_pair())
        ions=VGroup(Dot([-.13,2.2,0],radius=.13,color=YELLOW),Dot([.13,-2.65,0],radius=.13,color=PURPLE))
        self.at('channel passes');self.play(FadeIn(ions),FadeIn(label('Na⁺ inward',-4,1.7,28,YELLOW)),run_time=.3)
        self.at('and potassium');self.play(FadeIn(label('K⁺ outward',-4,.8,28,PURPLE)),run_time=.25)
        # Both ions traverse the same pore at the same time, on separate lanes.
        self.play(ions[0].animate.move_to([-.13,-2.65,0]),ions[1].animate.move_to([.13,2.2,0]),run_time=1.1,rate_func=linear)
        line=VGroup(Line([2.6,.8,0],[5.3,.8,0],color=GREY),Line([3.95,.6,0],[3.95,1.,0],color=TEXT),Arrow([3.1,.5,0],[3.1,.0,0],color=GREEN,buff=0),Arrow([4.8,.0,0],[4.8,.5,0],color=GREEN,buff=0),label('inward     outward',3.95,-.5,26))
        self.at('so its',lead=.35);self.play(FadeIn(label('reversal potential\n≈ 0 mV',3.9,2.1,30)),FadeIn(line),run_time=.3)
        self.at('current changes direction');self.play(Indicate(line,scale_factor=1.02),run_time=.35);self.finish()

class S05Recall(SpokenScene):
    def construct(self):
        self.add(rail(),marker(-90),label('The balance point',y=3,size=40));self.at('recall the balance');self.play(FadeIn(marker(-90,True)),run_time=.5);self.finish()
class S06Rule(SpokenScene):
    def construct(self):
        self.add(rail(),marker(-90),marker(-90,True),label('One compartment · no injected current',y=3.1,size=30))
        self.at('voltage moves toward');self.play(FadeIn(label('Vm → balance point',y=2.3,size=32,color=GREEN)),run_time=.4)
        formula=VGroup(label('Balance = sum(g × E) / sum(g)',y=-3.0,size=30),label('g = conductance; E = reversal potential',0,-3.55,26))
        self.at('an average');self.play(FadeIn(formula),run_time=.3)
        self.at('weighted by conductance');self.play(Indicate(formula[1],scale_factor=1.02),run_time=.4);self.finish()
class S07Pull(SpokenScene):
    def construct(self):
        self.add(rail(),marker(-90),marker(-90,True))
        self.at('Opening these channels');self.play(GrowArrow(rope(-90)),FadeIn(label('0 mV',5.1,1.45,30)),run_time=.5)
        self.at('adds a conductance');self.play(FadeIn(label('Added channel conductance pulls toward 0 mV',y=3,size=32,color=PINK)),run_time=.4);self.finish()
class S08Depol(SpokenScene):
    def construct(self):
        target=-90+dep(60);g=marker(-90,True);m=marker(-90);rp=rope(-90)
        self.add(rail(),g,m,rp,label('0 mV',5.1,1.45,30),label('Many channels open (about 60 packets)',y=3,size=32,color=PINK))
        self.at('balance point moves');self.play(Transform(g,marker(target,True)),Transform(rp,rope(target)),run_time=1.1)
        self.at('the voltage chases');self.play(Transform(m,marker(target)),run_time=.9)
        self.at('depolarizes');self.play(FadeIn(label('endplate depolarizes',0,-3.3,30,GREEN)),run_time=.3);self.finish()
class S09Ache(SpokenScene):
    def construct(self):
        r=large_receptor(True);a=large_ach_pair();self.add(membrane(),r,a)
        # Two lobes of one schematic enzyme settle against the docked ACh.
        enz=VGroup(*[RoundedRectangle(width=1.15,height=.85,corner_radius=.3,color=GREY,fill_opacity=.4).move_to([x,2.4,0]) for x in [-1.16,1.16]])
        bridge=Line([-1.16,2.4,0],[1.16,2.4,0],color=GREY,stroke_width=8)
        enz.add(bridge)
        self.at('An enzyme');self.play(FadeIn(enz),FadeIn(label('acetylcholinesterase',3.85,2.9,26)),Create(Line([1.8,2.55,0],[2.3,2.85,0],color=GREY)),run_time=.4)
        self.at('breaks down acetylcholine');self.play(enz.animate.shift(DOWN*.7),run_time=.35)
        pieces=VGroup(*[Rectangle(width=.32,height=.3,color=YELLOW,fill_opacity=.6).move_to([x,y,0]) for x,y in [(-1.4,1.25),(-.92,1.25),(.92,1.25),(1.4,1.25)]])
        cuts=VGroup(*[Line([x-.12,1.55,0],[x+.12,.95,0],color=TEXT,stroke_width=5) for x in [-1.16,1.16]])
        cut_label=label('ACh cut',3.7,.8,32,YELLOW)
        self.play(Create(cuts),run_time=.25);self.play(FadeOut(a),FadeOut(cuts),FadeIn(pieces),FadeIn(cut_label),run_time=.25)
        self.wait(1.05)
        self.at('ends each');self.play(pieces.animate.shift(UP*.65).set_opacity(.3),enz.animate.shift(UP*.7),Transform(r,large_receptor()),ReplacementTransform(cut_label,label('channel closes',3.7,.8,30,PINK)),run_time=.5);self.finish()
class S10Onepacket(SpokenScene):
    def construct(self):
        g=marker(-90,True);m=marker(-90);self.add(rail(),m,g,label('One packet',y=3.1,size=36,color=YELLOW),label('single packet, same scale reset',y=2.4,size=28))
        inset=VGroup(Rectangle(width=4.8,height=1.25,color=GREY).move_to([2,1.2,0]),label('magnified voltage step',2,1.55,28),Arrow([.3,.85,0],[3.7,.85,0],color=GREEN,buff=0),label('0.40 mV',2,.15,32,GREEN))
        leaders=VGroup(Line([-.4,1.0,0],[vx(-90+dep(1)),.65,0],color=GREY),Line([-.4,.6,0],[vx(-90+dep(1)),-.65,0],color=GREY))
        self.at('nudges the balance');self.play(Transform(g,marker(-90+dep(1),True)),Transform(m,marker(-90+dep(1))),FadeIn(inset),Create(leaders),run_time=.6)
        self.at('a fraction');self.play(Indicate(inset[-1]),run_time=.4);self.finish()
class S11More(SpokenScene):
    def construct(self):
        y=lambda v:-2.7+v*.3
        ax=VGroup(Line([-5.3,-2.7,0],[-5.3,3.1,0],color=GREY),Line([-5.3,-2.7,0],[-2.2,-2.7,0],color=GREY),label('response above rest (mV)',0,3.5,28))
        for v in [0,6,12,18]:ax.add(label(str(v),-5.85,y(v),28))
        bs=VGroup(*[Rectangle(width=1.7,height=(dep(i+1)-dep(i))*.3,stroke_width=0,fill_color=GREEN,fill_opacity=.95 if i%2==0 else .48).move_to([-3.3,y((dep(i+1)+dep(i))/2),0]) for i in range(60)])
        self.add(ax,label('60 packets',-3.3,-3.2,28,YELLOW));self.at('Each further packet')
        for i in range(5):self.play(FadeIn(bs[i]),run_time=.22)
        self.at('same conductance');self.play(FadeIn(label('Equal conductance per packet',1.8,2.7,28,PINK)),run_time=.2)
        self.play(LaggedStart(*[FadeIn(b) for b in bs[5:]],lag_ratio=.12),run_time=1.5)
        steps=VGroup()
        for x,h,txt in [(0,dep(1),'first packet\n0.40 mV'),(3.6,dep(60)-dep(59),'60th packet\nabout 0.25 mV')]:
            hh=h*6
            steps.add(Rectangle(width=1.1,height=hh,color=GREEN,fill_opacity=.6).move_to([x,-1.2+hh/2,0]),VGroup(Line([x+.7,-1.2,0],[x+.7,-1.2+hh,0],color=TEXT),Line([x+.6,-1.2,0],[x+.8,-1.2,0],color=TEXT),Line([x+.6,-1.2+hh,0],[x+.8,-1.2+hh,0],color=TEXT)),label(txt,x,-2.1,28,GREEN))
        self.at('moves the voltage less');self.play(FadeIn(steps),FadeIn(label('Steps magnified equally',2,1.8,26)),run_time=.4);self.finish()
class S12Why(SpokenScene):
    def construct(self):
        m=marker(-90);arrow=Arrow([vx(-90),.5,0],[5.1,.5,0],buff=0,color=GREEN)
        self.add(rail(),m,arrow,label('Replay the climb: driving force',y=3,size=36,color=GREEN),label('90 mV at rest → about 72 mV later',y=2.1,size=30),label('0 mV',5.1,1.15,30))
        self.at('As the voltage climbs');self.play(Transform(m,marker(-72)),Transform(arrow,Arrow([vx(-72),.5,0],[5.1,.5,0],buff=0,color=GREEN)),run_time=.75)
        self.at('driving force shrinks');self.play(Indicate(arrow,scale_factor=1.02),run_time=.5)
        self.at('the gap between');self.play(FadeIn(label('Driving force magnitude = distance to 0 mV',0,-3.3,30,GREEN)),run_time=.3);self.finish()
class S13Push(SpokenScene):
    def construct(self):
        v=-90+dep(60);self.add(rail(),marker(v),marker(v,True),label('Less driving force → less current',y=3.25,size=34,color=GREEN))
        old=rope(-90).shift(UP*1.5).set_opacity(.35);new=rope(v,5)
        self.add(old,label('first channel',0,2.65,28,PINK))
        self.at('newly opened channel');self.play(GrowArrow(new),FadeIn(label('newest channel',1,.05,28,PINK)),run_time=.4);self.finish()

# Reference HH simulator from action-potential/scenes.py.
def _rates(V):
    am=1. if abs(V+40)<1e-6 else .1*(V+40)/(1-np.exp(-(V+40)/10))
    bm=4*np.exp(-(V+65)/18);ah=.07*np.exp(-(V+65)/20);bh=1/(1+np.exp(-(V+35)/10))
    an=.1 if abs(V+55)<1e-6 else .01*(V+55)/(1-np.exp(-(V+55)/10))
    return am,bm,ah,bh,an,.125*np.exp(-(V+65)/80)
def hh_free():
    V=-65.;am,bm,ah,bh,an,bn=_rates(V);m=am/(am+bm);h=ah/(ah+bh);n=an/(an+bn);out=[];dt=.005
    for i in range(2000):
        t=i*dt;out.append((t,V));I=15 if .5<=t<1 else 0
        V+=dt*(I-120*m**3*h*(V-50)-36*n**4*(V+77)-.3*(V+54.4))
        am,bm,ah,bh,an,bn=_rates(V);m+=dt*(am*(1-m)-bm*m);h+=dt*(ah*(1-h)-bh*h);n+=dt*(an*(1-n)-bn*n)
    return np.array(out)

class S14Peak(SpokenScene):
    def construct(self):
        data=hh_free();P=lambda t,v:np.array([-4.8+t*.98,-2.45+(v+80)/130*4.95,0])
        ax=VGroup(Line(P(0,-80),P(10,-80),color=GREY),Line(P(0,-80),P(0,50),color=GREY),label('time (ms)',4.2,-2.95,28),label('mV',-5.65,3,28))
        for v in [-65,0,50]:ax.add(label(str(v),-5.65,P(0,v)[1],28),DashedLine(P(0,v),P(10,v),color=GREY).set_opacity(.4))
        peak=data[np.argmax(data[:,1])];pt=P(*peak)
        tr=VMobject(color=GREEN,stroke_width=4).set_points_as_corners([P(t,v) for t,v in data])
        self.add(ax,tr,label('rest −65 mV',-3.0,-2.2,28,GREEN),label('E_Na = +50 mV',2.6,2.95,30,YELLOW),label('Also: sodium inactivation and potassium current',0,-3.5,28))
        note=label('Na⁺ driving force\nshrinks as Vm rises',2.6,1.65,30,GREEN)
        self.at('same shrinking push');self.play(FadeIn(note),run_time=.3)
        self.at("spike's peak");self.play(FadeIn(label(f'peak ≈ {peak[1]:.0f} mV',-2.8,1.25,28,GREEN)),Create(VGroup(Line(pt+RIGHT*.5,P(peak[0],50)+RIGHT*.5,color=YELLOW),Line(pt+RIGHT*.4,pt+RIGHT*.6,color=YELLOW),Line(P(peak[0],50)+RIGHT*.4,P(peak[0],50)+RIGHT*.6,color=YELLOW))),FadeIn(label('gap',pt[0]+1.4,(pt[1]+2.5)/2,28,YELLOW)),run_time=.35)
        self.at('short of');self.play(Indicate(note,scale_factor=1.03),run_time=.3);self.finish()

def table(n):
    actual=dep(n)
    return VGroup(label(f'{n} packets',y=2.7,size=40,color=YELLOW),label('count × size',-3,1.5,32),label('balance point',3,1.5,32),label(f'{n*.4:.1f} mV',-3,.35,46,GREEN),label(f'{actual:.2f} mV' if n==4 else f'{actual:.1f} mV',3,.35,46,GREEN),label('about 2% less' if n==4 else 'about 20% less',3,-.75,32),label('Simple steady-state model · driving force 90 mV',0,-2.2,28),label('Packet size q = 0.40 mV · not a measured peak',0,-3.0,28))
class S15Small(SpokenScene):
    def construct(self):
        g=table(4);self.add(g[0:3],g[6:])
        self.at('In this simple model');self.play(FadeIn(g[3:5]),run_time=.4)
        self.at('small responses');self.play(FadeIn(g[5]),run_time=.35)
        self.at('size works');self.play(Indicate(g[3:5],scale_factor=1.04),run_time=.4);self.finish()
class S16Large(SpokenScene):
    def construct(self):
        self.add(response_axes(),caveat(),label('60 packets · count × size',-2.9,-2.85,26,YELLOW),label('balance point',1,-2.85,26))
        ideal=Rectangle(width=2,height=24*SCALE,color=GREY,fill_opacity=.08).move_to([-2.9,by(12),0]);actual=bar(x=1.0,width=2)
        self.at('For');self.play(Create(ideal),FadeIn(label('24.0',-2.9,1.8,32)),run_time=.6)
        self.at('a fifth below');gap=Rectangle(width=2,height=(24-dep(60))*SCALE,color=ORANGE,fill_opacity=.3).move_to([1,by((24+dep(60))/2),0])
        self.play(FadeIn(actual),FadeIn(gap),FadeIn(label('18.9 mV',3.5,1.25,34,GREEN)),FadeIn(label('about 20% less',3.6,2.45,28,ORANGE)),run_time=.8)
        self.at('numbers are on');self.play(Indicate(gap),run_time=.45);self.finish()
class S17Threshold(SpokenScene):
    def construct(self):
        self.add(safety_stage(False));self.at('margin of safety');self.play(Indicate(self.mobjects[0][1],scale_factor=1.03),run_time=.4)
        self.at('fires at');self.play(Create(threshold()),run_time=.45);self.finish()
class S18Sf(SpokenScene):
    def construct(self):
        self.add(safety_stage());self.at('safety factor');self.play(FadeIn(label('Safety factor',2.4,-.95,32,ORANGE)),run_time=.3)
        self.at('response divided');self.play(FadeIn(label('response / depolarization\nneeded to fire',2.4,-1.75,26,ORANGE)),run_time=.4);self.finish()
class S19Sfvalues(SpokenScene):
    def construct(self):
        self.add(response_axes(),caveat())
        ideal=Rectangle(width=3.3,height=24*SCALE,color=GREY,fill_opacity=.08).move_to([-2.65,by(12),0]);actual=bar(x=2.5,width=2.2)
        self.at('Simple multiplication');self.play(Create(ideal),FadeIn(label('24 / 12 = 2.0',-2.65,1.5,32,ORANGE)),FadeIn(label('count × size, 24 mV',-2.65,-2.85,26)),run_time=.45)
        self.at('The balance point');self.play(FadeIn(actual),FadeIn(label('≈ 19 / 12 ≈ 1.6',2.5,2.45,32,ORANGE)),FadeIn(label('balance point, about 19 mV',2.5,-2.85,26)),run_time=.45)
        self.add(DashedLine([-5.25,by(12),0],[5.5,by(12),0],color=ORANGE));self.finish()
class S20Margin(SpokenScene):
    def construct(self):
        self.add(safety_stage());h=(dep(60)-12)*SCALE
        band=Rectangle(width=3.2,height=h,color=ORANGE,fill_opacity=.22,stroke_width=0).move_to([-2.55,by((12+dep(60))/2),0])
        self.at('comfortably above');self.play(FadeIn(band),FadeIn(label('safety margin',-.15,by((12+dep(60))/2),28,ORANGE)),FadeIn(label('Safety factor ≈ 1.6',2.4,-1.25,32,ORANGE)),run_time=.45)
        self.at('margin to spare');self.play(Indicate(band,scale_factor=1.02),run_time=.4);self.finish()
class S21Round(SpokenScene):
    def construct(self):
        g=safety_stage();self.add(g)
        self.at('These round numbers');self.play(FadeIn(label('Illustrative round numbers',2.4,-1.25,28,ORANGE)),run_time=.35)
        self.at('A real junction');self.play(FadeOut(g[2]),FadeOut(g[3]),run_time=.25)
        self.play(FadeIn(label('Real junction:\nmore packets;\nmore needed to fire',2.4,1.75,30,ORANGE)),run_time=.35);self.finish()
class S22Predict(SpokenScene):
    def construct(self):
        q=question_state();recs=question_receptors()
        self.add(q[0],q[1],recs)
        # Visible grips latch onto four of six receptors before removal.
        tags=VGroup()
        for x in [QUESTION_X[i] for i in [0,1,3,5]]:
            tags.add(VGroup(Line([x,1.8,0],[x,1.25,0],color=GREY,stroke_width=6),Line([x,1.25,0],[x-.35,.85,0],color=GREY,stroke_width=6),Line([x,1.25,0],[x+.35,.85,0],color=GREY,stroke_width=6)))
        antibody_label=label('antibodies',0,2.35,28)
        self.at('Suppose antibodies');self.play(FadeIn(tags),FadeIn(antibody_label),run_time=.35)
        self.at('remove some');self.play(tags.animate.shift(DOWN*.5),run_time=.3);self.wait(.35)
        self.play(FadeOut(tags),FadeOut(antibody_label),*[FadeOut(recs[i]) for i in [0,1,3,5]],FadeIn(q[4]),run_time=.4)
        self.at('Which factor changes');self.play(FadeIn(q[5]),run_time=.35);self.finish()
class S23Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(question_state());self.wait(5)
class S24Reveal(SpokenScene):
    def construct(self):
        q=question_state();self.add(q)
        bs=packet_bars()
        self.at('The size falls');self.play(FadeOut(q),FadeIn(factors('size').shift(UP*.25)),FadeIn(packet_plot()),FadeIn(bs),run_time=.35)
        self.play(Transform(bs,packet_bars(.24)),FadeIn(label('size q ↓',5.35,.25,28,GREEN)),run_time=.65)
        self.at('fewer receptors');self.play(FadeIn(label('Fewer receptors open per packet',0,-3.35,30,PINK)),run_time=.35);self.finish()
class S25Count(SpokenScene):
    def construct(self):
        cause=label('Fewer receptors open per packet',0,-3.35,30,PINK)
        self.add(factors('count').shift(UP*.25),packet_plot(),packet_bars(.24),label('size q ↓',5.35,.25,28,GREEN),cause)
        count_cause=label('Count set by terminal and calcium',0,-3.35,30,YELLOW)
        self.at('the count stays');self.play(FadeOut(cause),FadeIn(count_cause),Indicate(self.mobjects[1][-1],scale_factor=1.02),run_time=.35)
        self.at('The terminal');self.play(Indicate(count_cause,scale_factor=1.02),run_time=.4);self.finish()
class S26Takeaway(SpokenScene):
    def construct(self):
        self.add(label('Membrane and recording held steady',y=3.25,size=30))
        out=chip('packet size, q',GREEN,44).move_to([0,-.55,0]);fill=chip('vesicle filling',YELLOW,36).move_to([-3.2,1.8,0]);rec=chip('receptors',PINK,36).move_to([3.2,1.8,0])
        self.add(out)
        self.at('So the size depends');self.play(Indicate(out,scale_factor=1.02),run_time=.3)
        self.at('vesicle filling');self.play(FadeIn(fill),GrowArrow(Arrow([-3.2,1.3,0],[-1,-.05,0],color=YELLOW)),run_time=.35)
        self.at('and receptors');self.play(FadeIn(rec),GrowArrow(Arrow([3.2,1.3,0],[1,-.05,0],color=PINK)),run_time=.35)
        self.at('big responses');self.play(FadeIn(label('Big responses fall short\nof count × size',y=-2.9,size=44,color=GREEN)),run_time=.45);self.finish()
class S27End(EndCard):
    LINE='Filling and receptors set size; large responses sum less than linearly.'
    def construct(self):
        self.add(label('Filling and receptors set size',y=1.4,size=40,color=GREEN),label('Big responses fall short\nof count × size',y=-.5,size=40),label('biochemistrypedia.com',y=-2.4,size=28,color=TEAL));self.finish()
