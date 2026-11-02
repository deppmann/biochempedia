"""Chapter 3, reviewer fix round.
COLOR MAP: BLUE blood; YELLOW SFO/thirst neurons; ORANGE vasopressin;
GREEN activation/indicator; RED inhibition/deficit threshold; TEAL feedback
and incoming water; GOLD feedforward; GREY structure and axes.

Neural curves are explicitly schematic smooth-step models, using sigm/Ax/trace
from the reference film and the lesson's timing constraints; amplitudes are
arbitrary units, never reconstructed data. Saline recovery is partial.
The blood-only simulation solves D'=-G/tau, G'=kD-G/tau, I'=kD with
D(0)=1, G(0)=I(0)=0, k=1/min, tau=5 min. RK4 and an interpolated
first-zero event stop intake exactly. All model gauges carry explicit litre scales.
"""
import numpy as np
from bp_style import *

ORANGE = '#F29E4C'
BLOOD, NEUR, AVP, EXC, INH, FB, FF = BLUE, YELLOW, ORANGE, GREEN, RED, TEAL, GOLD
LIGHT = '#BEC5D2'

class Ax:
    def __init__(self,x0,x1,y0,y1,t0,t1,v0=0,v1=1):
        self.x0,self.x1,self.y0,self.y1,self.t0,self.t1,self.v0,self.v1=x0,x1,y0,y1,t0,t1,v0,v1
    def X(self,t): return self.x0+(t-self.t0)/(self.t1-self.t0)*(self.x1-self.x0)
    def Y(self,v): return self.y0+(v-self.v0)/(self.v1-self.v0)*(self.y1-self.y0)
    def P(self,t,v): return np.array([self.X(t),self.Y(v),0.])

def sigm(t,a,b):
    u=np.clip((t-a)/(b-a),0,1)
    return u*u*(3-2*u)

def trace(ax,f,a,b,color=NEUR,w=6,n=180):
    m=VMobject(stroke_color=color,stroke_width=w,fill_opacity=0)
    m.set_points_as_corners([ax.P(t,f(t)) for t in np.linspace(a,b,n)])
    return m

def fall(t): return .82-.65*sigm(t,0,1)
def saline(t): return fall(t)+.48*sigm(t,1,2.7)
def gut_fall(t): return .82-.65*sigm(t,107/60,107/60+.7)
def gut_rise(t): return .82+.65*sigm(t,.4,2.5)
def head(s,color=TEXT,size=34): return T(s,size,color,weight=BOLD).move_to([0,3.25,0])
def tag(s='schematic',x=5.35,y=-3.45): return T(s,26,LIGHT).move_to([x,y,0])
def label(s,x,y,color=TEXT,size=26): return T(s,size,color).move_to([x,y,0])
def bracket(x0,x1,y,text,color=NEUR,size=26):
    line=VGroup(Line([x0,y+.12,0],[x0,y,0],color=color),Line([x0,y,0],[x1,y,0],color=color),Line([x1,y,0],[x1,y+.12,0],color=color))
    return VGroup(line,label(text,(x0+x1)/2,y-.4,color,size))

def mouse():
    body=Ellipse(width=3.3,height=1.8,color=LIGHT,fill_color=LIGHT,fill_opacity=.13)
    face=Ellipse(width=1.35,height=1.15,color=LIGHT,fill_color=BG,fill_opacity=1).move_to([1.45,.35,0])
    ear=Circle(radius=.4,color=LIGHT,fill_color=BG,fill_opacity=1).move_to([1.03,.98,0])
    eye=Dot([1.65,.55,0],radius=.065,color=TEXT)
    nose=Dot([2.1,.25,0],radius=.06,color=TEXT)
    tail=ArcBetweenPoints([-1.6,-.05,0],[-2.35,.65,0],angle=-1,color=LIGHT)
    feet=VGroup(Line([-.7,-.8,0],[-.2,-.96,0],color=LIGHT),Line([.9,-.72,0],[1.3,-.94,0],color=LIGHT))
    return VGroup(body,face,ear,eye,tail,feet,nose)

def mouse_at(x,y,scale=1):
    m=mouse().scale(scale)
    m.shift(np.array([x,y,0])-m[0].get_center())
    return m

def implant(m):
    p=m[2].get_center()+UP*.15
    return VGroup(Line(p+UP*1.35,p+UP*.15,color=LIGHT,stroke_width=4),Rectangle(width=.16,height=.3,color=TEXT,fill_color=LIGHT,fill_opacity=1).move_to(p+UP*.25))

def spout(m,water=True,reach=True):
    mouth=m[-1].get_center()
    unit=max(.72,min(1.2,m[0].width/3.3))
    tip=mouth+RIGHT*(.12 if reach else .5)
    neck=tip+np.array([.4,.45,0])*unit
    center=neck+UP*.72*unit
    # Inverted drinking bottle: round reservoir, narrow neck, metal sipper.
    shell=VGroup(Ellipse(width=.72*unit,height=1.12*unit,color=LIGHT).move_to(center),
                 Rectangle(width=.22*unit,height=.3*unit,color=LIGHT,fill_color=LIGHT,fill_opacity=.5).move_to(neck))
    liquid=Ellipse(width=.56*unit,height=.72*unit,stroke_width=0,fill_color=TEAL,fill_opacity=.7).move_to(center+UP*.08*unit)
    pipe=VMobject(stroke_color=LIGHT,stroke_width=5).set_points_as_corners([neck+DOWN*.15*unit,tip+RIGHT*.24*unit+UP*.17*unit,tip])
    drop=VGroup(Dot(tip+DOWN*.13*unit,radius=.075*unit,color=TEAL),
                Triangle(stroke_width=0,fill_color=TEAL,fill_opacity=1).scale(.07*unit).move_to(tip+DOWN*.055*unit))
    return VGroup(shell,*([liquid] if water else []),pipe,*([drop] if water else []))

def tongue(m):
    p=m[-1].get_center()
    return Line(p+LEFT*.1+DOWN*.07,p+RIGHT*.18+DOWN*.07,color=ORANGE,stroke_width=4)

def drink_drop(m):
    return Dot(m[-1].get_center()+LEFT*.13+DOWN*.1,radius=.085,color=TEAL)

def neuron_cloud():
    return VGroup(*[Circle(radius=.34,color=NEUR,fill_color=GREEN,fill_opacity=.22).move_to([x,y,0]) for x,y in [(-1.05,.25),(0,.65),(1.05,.25),(-.63,-.7),(.63,-.7)]])

def cluster(x=2.7,y=-.1,scale=1.35): return neuron_cloud().scale(scale).move_to([x,y,0])
def optical(c,color=TEAL):
    x=c.get_center()[0]; top=c.get_top()[1]
    p=np.array([x,top+.45,0]); bottom=c.get_bottom()[1]-.1
    beam=Polygon(p,[c.get_left()[0]-.1,bottom,0],[c.get_right()[0]+.1,bottom,0],stroke_width=0,fill_color=color,fill_opacity=.23)
    fibre=VGroup(Line(p+UP*.8,p,color=LIGHT,stroke_width=5),Rectangle(width=.16,height=.28,color=LIGHT,fill_color=TEXT,fill_opacity=1).move_to(p+UP*.35))
    return VGroup(beam,fibre)

UPAX=Ax(-3.25,5.85,.65,2.45,-.5,5.3)
LOAX=Ax(-3.25,5.85,-2.35,-.7,-.5,5.3)

def water_marker():
    x=UPAX.X(0)
    return VGroup(DashedLine([x,2.5,0],[x,.65,0],color=TEXT),DashedLine([x,-.7,0],[x,-2.35,0],color=TEXT),label('water available, first lick',-.8,2.72,size=22))

def time_lanes(marker=True):
    g=VGroup(head('Neurons and blood: different time courses',size=32),label('SFO\nactivity\n(a.u.)',-5.15,1.7,NEUR),label('plasma\nosmolality',-5.15,-1.15,BLOOD),tag(x=5.15,y=-3.55))
    for ax in (UPAX,LOAX):
        g.add(Line(ax.P(-.5,0),ax.P(5.3,0),color=LIGHT),Line(ax.P(-.5,0),ax.P(-.5,1),color=LIGHT))
        for t in range(6):
            g.add(Line(ax.P(t,0),ax.P(t,0)+DOWN*.1,color=LIGHT),label(str(t),ax.X(t),ax.y0-.3,LIGHT))
    g.add(label('minutes after water access',1,-3.15,LIGHT))
    if marker: g.add(water_marker())
    return g

def down_bracket(): return bracket(UPAX.X(0),UPAX.X(1),.1,'down within 1 min',NEUR)

def blood_sample():
    p=LOAX.P(5,.8)
    return VGroup(Dot(p,radius=.13,color=BLOOD),Line(p+UP*.25,p+DOWN*.25,color=BLOOD,stroke_width=3),Line(p+UP*.25+LEFT*.16,p+UP*.25+RIGHT*.16,color=BLOOD),Line(p+DOWN*.25+LEFT*.16,p+DOWN*.25+RIGHT*.16,color=BLOOD),label('still raised\nat 5 min',3.8,-.95,BLOOD))

PANEL_X=(-4.35,0,4.35)
def candidate_question(): return head('What turns the neurons down?')
def candidate_panel(i,answered=False):
    x=PANEL_X[i]
    box=RoundedRectangle(width=4.05,height=5.65,corner_radius=.17,color=LIGHT).move_to([x,-.25,0])
    title=label(('water out\nof reach','empty spout','fluid into\nthe mouth')[i],x,2.0,size=28)
    m=mouse_at(x-.65,-.45,.75).stretch(1.8,1,about_point=[x-.65,-.45,0])
    m[4].scale(.3,about_point=m[4].get_start())
    b=spout(m,water=i!=1,reach=i!=0)
    if i==0:
        p=m[-1].get_center()+RIGHT*.25
        action=VGroup(Line(p+DOWN*1.25,p+UP*1.1,color=LIGHT,stroke_width=5),
                      *[Line(p+UP*y+LEFT*.1,p+UP*y+RIGHT*.1,color=LIGHT) for y in np.arange(-1.1,1.1,.25)])
    elif i==1:
        action=tongue(m)
    else:
        mouth=m[-1].get_center()
        action=VGroup(tongue(m),Line(mouth+RIGHT*.3+UP*.28,mouth+LEFT*.25+DOWN*.12,color=TEAL,stroke_width=7),drink_drop(m))
    q=label('?',x+1.25,-1.8,FF,44)
    if answered:
        VGroup(m,b,action).scale(.7,about_point=[x,.2,0]).shift(UP*.35)
    return VGroup(box,title,m,b,action,q)

def candidates(answered=()): return VGroup(*[candidate_panel(i,i in answered) for i in range(3)])

def shrink_candidate(panel):
    return VGroup(*panel[2:5]).animate.scale(.7,about_point=[panel[0].get_center()[0],.2,0]).shift(UP*.35)
def candidate_result(i):
    x=PANEL_X[i]; ax=Ax(x-1.55,x+1.55,-2.7,-1.3,0,1)
    if i<2:
        # The X belongs to the hypothetical fall, never to the performed action.
        ghost=trace(ax,fall,0,1,color=GREY,w=3).set_stroke(opacity=.4)
        cross=VGroup(Line([x-.35,-2.35,0],[x+.35,-1.65,0],color=RED,stroke_width=3),Line([x-.35,-1.65,0],[x+.35,-2.35,0],color=RED,stroke_width=3))
        return VGroup(ghost,trace(ax,lambda t:.82,0,1),cross,label('SFO activity:\nno fall',x,-1.12,NEUR,26))
    return VGroup(trace(ax,fall,0,1),label('SFO activity:\nfalls',x,-1.12,NEUR,26))

SAX=Ax(-5.65,5.8,-1.8,2.1,-.4,3)
def saline_axes():
    g=VGroup(head('Drinking concentrated saline'),label('SFO activity (a.u.)',-3.9,2.65,NEUR),tag('schematic: shape only',x=3.9,y=2.65),Line(SAX.P(-.4,0),SAX.P(3,0),color=LIGHT),Line(SAX.P(-.4,0),SAX.P(-.4,1),color=LIGHT),label('minutes after first lick',0,-2.55,LIGHT))
    for t in range(4):
        g.add(Line(SAX.P(t,0),SAX.P(t,0)+DOWN*.1,color=LIGHT),label(str(t),SAX.X(t),-2.12,LIGHT))
    g.add(DashedLine(SAX.P(0,0),SAX.P(0,1),color=LIGHT),DashedLine(SAX.P(1,0),SAX.P(1,1),color=LIGHT))
    return g

def saline_reference():
    return VGroup(trace(SAX,fall,-.4,3,w=10).set_stroke(opacity=.24),label('water reference',3.8,-.55,NEUR))

def gut_stage():
    m=mouse_at(-3.7,-.55,1.0)
    stomach=Ellipse(width=1.0,height=.72,color=TEAL,fill_color=TEAL,fill_opacity=.23).move_to([-3.6,-.65,0])
    mouth=m[-1].get_center()
    points=[[-5.65,1.95,0],[-5.65,.7,0],[-5.45,-1.4,0],[-4.5,-1.45,0],[-3.6,-.65,0]]
    tube=VMobject(stroke_color=TEAL,stroke_width=5).set_points_as_corners(points)
    c=cluster(3.05,1.1,.85); f=optical(c)
    connector=DashedLine(m[2].get_center()+RIGHT*.25,[1.8,1.4,0],color=LIGHT)
    ax=Ax(.7,5.9,-2.4,-.8,0,4)
    g=VGroup(m,stomach,tube,c,f,connector,label('stomach',-3.8,-1.9,TEAL),label('recording: SFO population',3.0,-.25,NEUR),label('water into stomach',-3.65,2.4,TEAL),Line(ax.P(0,0),ax.P(4,0),color=LIGHT),label('time after infusion',3.1,-2.9,LIGHT),tag())
    # Leader from the label to the organ, outside the mouse outline.
    g.add(Line([-3.8,-1.62,0],[-3.6,-1.02,0],color=TEAL))
    return g,tube,ax

GAX=Ax(-5.8,2.35,-1.5,2.15,0,4)
def gut_axes(title):
    g=VGroup(head(title,size=32),label('SFO calcium (a.u.)' if title.startswith('Hypertonic') else 'dehydrated mice: SFO calcium (a.u.)',-2.0,2.65,NEUR),Line(GAX.P(0,0),GAX.P(4,0),color=LIGHT),Line(GAX.P(0,0),GAX.P(0,1),color=LIGHT),label('minutes after infusion',-1.7,-2.15,LIGHT,24))
    for t in range(5):
        g.add(Line(GAX.P(t,0),GAX.P(t,0)+DOWN*.1,color=LIGHT),label(str(t),GAX.X(t),-1.78,LIGHT,24))
    return g

def blood_inset():
    x=4.8
    box=RoundedRectangle(width=3.65,height=5.8,corner_radius=.16,color=BLOOD).move_to([x,-.1,0])
    g=VGroup(box,label('Separate blood\nmeasurements',x,2.15,BLOOD,24),label('hydrated mice',x,1.3),label('blood collected',x,.65,BLOOD))
    ax=Ax(3.3,6.3,-.2,.2,0,6)
    g.add(Line(ax.P(0,0),ax.P(6,0),color=LIGHT),Line([ax.X(3),.15,0],[ax.X(6),.15,0],color=BLOOD,stroke_width=12))
    for t in (0,3,6): g.add(label(str(t),ax.X(t),-.55,LIGHT))
    g.add(label('minutes; 3 to about 6',x,-1.0,LIGHT,22),label('no detectable\nosmolarity change',x,-1.65,BLOOD,24),label('separate mice,\nseparate time axis',x,-2.4,LIGHT,22))
    return g

# Deterministic RK4 model with first-zero event, rather than a chosen animation endpoint.
def model_values():
    dt=.001; t=0.; z=np.array([1.,0.,0.]); rows=[(t,*z)]
    def rhs(v):
        d,g,_=v
        return np.array([-g/5,d-g/5,d])
    while z[0]>0:
        a=rhs(z); b=rhs(z+dt*a/2); c=rhs(z+dt*b/2); d=rhs(z+dt*c)
        new=z+dt*(a+2*b+2*c+d)/6
        if new[0]<=0:
            frac=z[0]/(z[0]-new[0]); z=z+frac*(new-z); z[0]=0; t+=dt*frac
            rows.append((t,*z)); break
        z=new; t+=dt; rows.append((t,*z))
    return np.array(rows)
MODEL=model_values(); STOP=MODEL[-1,0]
def state_at(t): return np.array([np.interp(t,MODEL[:,0],MODEL[:,i]) for i in range(4)])

# Gauges share a zero; blood has a 0–1 L scale, gut/intake a 0–2.5 L scale.
BAR_BOTTOM=-1.5; BAR_H=3.5; BAR_MAX=2.5
GAUGES=((-3.9,NEUR,'drunk'),(.15,TEAL,'gut water G'),(4.2,BLOOD,'blood deficit D'))
def value_bar(x,v,color):
    limit=1.0 if x==4.2 else BAR_MAX
    h=max(.008,min(v,limit)*BAR_H/limit)
    return Rectangle(width=1.25,height=h,stroke_width=0,fill_color=color,fill_opacity=.6).move_to([x,BAR_BOTTOM+h/2,0])

def gauge_stage():
    g=VGroup()
    for x,color,name in GAUGES:
        g.add(Rectangle(width=1.3,height=BAR_H,color=color).move_to([x,BAR_BOTTOM+BAR_H/2,0]),label(name,x,2.35,color))
        limit=1.0 if x==4.2 else BAR_MAX
        for v in ((0,.5,1) if x==4.2 else (0,1,2)):
            y=BAR_BOTTOM+v*BAR_H/limit
            g.add(Line([x+.68,y,0],[x+.82,y,0],color=LIGHT),label(str(v),x+1.05,y,LIGHT,24))
    g.add(label('litres',-5.9,-1.95,LIGHT,24),Line([-4.58,BAR_BOTTOM+BAR_H/BAR_MAX,0],[-3.22,BAR_BOTTOM+BAR_H/BAR_MAX,0],color=RED,stroke_width=4),label('1.00 L\ninitial deficit',-5.65,.25,RED,24))
    # Small but visible drinking animal; gauges are the principal subject here.
    m=mouse_at(-4.35,-3.03,.60); b=spout(m)
    g.add(m,b)
    return g,m

def gauge_numbers(d,g,total):
    return VGroup(label(f'{total:.2f} L',-3.9,-1.85,NEUR),label(f'{g:.2f} L',.15,-1.85,TEAL),label(f'{d:.2f} L',4.2,-1.85,BLOOD))
def model_bars(d,g,total): return VGroup(value_bar(-3.9,total,NEUR),value_bar(.15,g,TEAL),value_bar(4.2,d,BLOOD))
def blood_question(): return head('Blood only: how much would it drink?',size=33)
def question_stage(v=0):
    g,m=gauge_stage()
    return VGroup(g,model_bars(1,v,v),gauge_numbers(1,v,v),blood_question(),label('blood: not yet',4.2,-2.9,BLOOD),label('?',.15,.45,FF,72),tag(x=5.2)),m

def bowl():
    return VGroup(Polygon([-.7,.15,0],[.7,.15,0],[.48,-.45,0],[-.48,-.45,0],color=LIGHT,fill_color=LIGHT,fill_opacity=.15),Ellipse(width=1.4,height=.35,color=TEAL,fill_color=TEAL,fill_opacity=.75))

class S00Title(TitleCard):
    LESSON='Autonomic Control and the Hypothalamus'
    TITLE='Acting Before the Blood Changes'
    def construct(self):
        group=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL,weight=BOLD),T(self.LESSON.upper(),26,LIGHT),fit(T(self.TITLE,54,font=TITLE_FONT),max_w=12),Line(LEFT*1.4,RIGHT*1.4,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.4).move_to(ORIGIN)
        self.play(FadeIn(group),run_time=.4)
        self.finish()

class S01Question(SpokenScene):
    def construct(self):
        m=mouse_at(-3.35,-.35,1.45); b=spout(m); self.add(m,b,implant(m),tag())
        ax=Ax(1,5.9,-.3,1.9,0,1.5)
        self.add(label('thirst-neuron activity',3.2,2.5,NEUR),Line(ax.P(0,0),ax.P(1.5,0),color=LIGHT),trace(ax,fall,0,.001))
        self.at('thirst neurons go quiet'); self.play(Create(trace(ax,fall,0,1.5)),FadeIn(drink_drop(m)),run_time=1.0)
        self.add(label('within 1 min',3.5,-.8,NEUR))
        self.at('No change in the blood'); self.play(FadeIn(label('blood: no detected change',2.5,-2.0,BLOOD)),run_time=.25)
        self.at('So what has changed',lead=0); self.play(FadeIn(head('So what has changed?')),run_time=.25); self.wait(2.4); self.finish()

class S02Record(SpokenScene):
    def construct(self):
        m=mouse_at(-3.7,-.7,1.05); c=cluster(2.8,-.2,1.35)
        self.add(m,implant(m),c,DashedLine(m[2].get_center()+RIGHT*.2,c.get_left()+LEFT*.15,color=LIGHT),head('Recording a population'),tag())
        self.at('subfornical organ neurons'); self.play(FadeIn(label('subfornical organ (SFO)',2.8,-2.4,NEUR)),run_time=.3)
        self.at('using an'); self.play(FadeIn(optical(c)),FadeIn(label('fibre photometry',2.8,2.75)),run_time=.4)
        self.at('calcium indicator'); self.play(c.animate.set_fill(GREEN,.85),FadeIn(label('calcium indicator',-4.1,2.4,GREEN)),FadeIn(label('population calcium',2.8,-3.0,GREEN)),run_time=.35)
        self.play(c.animate.set_stroke(GREEN,5),run_time=.35); self.play(c.animate.set_stroke(NEUR,3),run_time=.35); self.wait(2.2); self.finish()

class S03Axes(SpokenScene):
    def construct(self):
        self.add(time_lanes(False),trace(UPAX,fall,-.5,0))
        self.at('marks when water'); self.play(Create(water_marker()),run_time=.4); self.finish()

class S04Top(SpokenScene):
    def construct(self):
        self.add(time_lanes(),trace(UPAX,fall,-.5,0))
        self.at('starts to fall'); self.play(Create(trace(UPAX,fall,0,1)),run_time=.8)
        self.at('Within a minute'); self.play(Create(trace(UPAX,fall,1,5.3)),FadeIn(down_bracket()),run_time=.5); self.finish()

class S05Bottom(SpokenScene):
    def construct(self):
        self.add(time_lanes(),trace(UPAX,fall,-.5,5.3),down_bracket())
        self.at('blood was sampled'); self.play(FadeIn(label('sampled separately',-4.95,-2.85,BLOOD,24)),run_time=.3)
        self.at('still raised'); self.play(FadeIn(blood_sample()),run_time=.35); self.finish()

class S06QCandidates(SpokenScene):
    def construct(self):
        p=candidates(); self.add(candidate_question(),tag(),p[0][0],p[1][0],p[2][0])
        # Pictures are present from the question; the named alternatives gain labels in turn.
        for panel in p: self.add(*panel[2:5],panel[-1])
        self.at('the site of water'); self.play(FadeIn(p[0][1]),run_time=.25)
        self.at('The licking'); self.play(FadeIn(p[1][1]),run_time=.25)
        self.at('the water itself'); self.play(FadeIn(p[2][1]),run_time=.25); self.finish()

class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(candidate_question(),candidates(),tag())
        dots=VGroup(*[Dot([x,-3.45,0],radius=.075,color=FF) for x in (-.4,0,.4)])
        self.add(label('Think',-1.2,-3.45,FF),dots)
        for d in dots: self.play(d.animate.set_opacity(.15),run_time=5/3,rate_func=linear)

class S08ASight(SpokenScene):
    def construct(self):
        p=candidates(); self.add(candidate_question(),p,tag())
        self.at('did not lower'); self.play(shrink_candidate(p[0]),FadeOut(p[0][-1]),FadeIn(candidate_result(0)),run_time=.4)
        self.at('did not either'); self.play(shrink_candidate(p[1]),FadeOut(p[1][-1]),FadeIn(candidate_result(1)),run_time=.4); self.finish()

class S09AFluid(SpokenScene):
    def construct(self):
        p=candidates(answered=(0,1)); self.add(candidate_question(),p,tag(),candidate_result(0),candidate_result(1)); self.remove(p[0][-1],p[1][-1])
        p[0][-1].set_opacity(0); p[1][-1].set_opacity(0)
        self.at('fluid going in'); self.play(p[2][0].animate.set_stroke(FF,5),shrink_candidate(p[2]),FadeOut(p[2][-1]),Create(candidate_result(2)),run_time=.4); self.finish()

class S10Saline(SpokenScene):
    def construct(self):
        self.add(saline_axes(),saline_reference(),trace(SAX,saline,-.4,0))
        self.at('lowers it at first'); self.play(Create(trace(SAX,saline,0,1)),run_time=.7)
        self.at('the fall reverses'); self.play(Create(trace(SAX,saline,1,3)),run_time=.7); self.finish()

class S11FastSlow(SpokenScene):
    def construct(self):
        self.add(saline_axes(),saline_reference(),trace(SAX,saline,-.4,3))
        self.at('fast signal'); self.play(FadeIn(bracket(SAX.X(0),SAX.X(1),-2.9,'fast signal:\nfluid going in',TEAL)),run_time=.3)
        self.at('slower one'); self.play(FadeIn(bracket(SAX.X(1),SAX.X(3),-2.9,'slower signal: what it contains',FF)),run_time=.3); self.finish()

class S12Gut(SpokenScene):
    def construct(self):
        g,tube,ax=gut_stage(); self.add(g,head('Bypass the mouth'))
        self.at('bypass the mouth'); self.play(Indicate(tube,color=TEAL),run_time=.4)
        self.at('water straight into');
        drops=VGroup(*[Dot(tube.point_from_proportion(a),radius=.09,color=TEAL) for a in (0,.17,.34)])
        self.add(drops)
        self.play(LaggedStart(*[MoveAlongPath(d,tube,rate_func=linear) for d in drops],lag_ratio=.25),Create(trace(ax,gut_fall,0,4)),run_time=1.6)
        self.remove(drops); self.wait(.8); self.finish()

class S13GutResult(SpokenScene):
    def construct(self):
        self.add(gut_axes('Water into the stomach'),tag(x=5.3,y=3.68),trace(GAX,gut_fall,0,107/60))
        self.at('the activity falls'); self.play(Create(trace(GAX,gut_fall,107/60,4)),run_time=.7)
        lat=bracket(GAX.X(0),GAX.X(107/60),-2.8,'latency 107 ± 15 s\n(mean ± SEM)',NEUR)
        # Move only the text to keep the wide label within the left plot.
        lat[1].move_to([(GAX.X(0)+GAX.X(107/60))/2,-3.3,0]); self.play(FadeIn(lat),run_time=.25)
        self.at('Separate blood measurements'); self.play(FadeIn(blood_inset()),run_time=.35); self.finish()

class S14GutSaline(SpokenScene):
    def construct(self):
        ax=Ax(GAX.x0,GAX.x1,GAX.y0,GAX.y1,0,4,0,1.6)
        self.add(gut_axes('Hypertonic saline into the stomach'),trace(ax,gut_fall,0,4,w=5).set_stroke(opacity=.25),label('water reference',-.1,-.8,NEUR),tag(x=5.3,y=3.68))
        c=cluster(4.35,.65,.85); self.add(c,label('SFO population',4.35,-1.3,NEUR),label('baseline',-4.5,ax.Y(.82)-.35,LIGHT),DashedLine(ax.P(0,.82),ax.P(4,.82),color=LIGHT))
        self.at('raises the activity'); self.play(Create(trace(ax,gut_rise,0,4)),c.animate.set_fill(GREEN,.9),run_time=.8); self.finish()

class S15Hold(SpokenScene):
    def construct(self):
        c=cluster(-4,1.0,.8); light=optical(c,GREEN)
        light[0].set_fill(GREEN,opacity=.4)
        off=Rectangle(width=1.25,height=.65,color=NEUR,fill_color=NEUR,fill_opacity=.35).move_to([1.8,-1.425,0])
        on=Rectangle(width=1.25,height=2.9,color=NEUR,fill_color=NEUR,fill_opacity=.85).move_to([4.7,-.3,0])
        self.add(head('Optogenetic activation',EXC),c,light[1],tag('schematic comparison',x=4.3,y=-3.55),label('intake after gut water',2.8,2.55,NEUR),Line([.3,-1.75,0],[6.1,-1.75,0],color=LIGHT),Line([.3,-1.75,0],[.3,1.95,0],color=LIGHT),off,label('light off',1.8,-2.15),label('usual satiation',1.9,-.65,NEUR,24))
        self.at('used light'); self.play(FadeIn(light[0]),c.animate.set_fill(GREEN,.9),FadeIn(label('light on',-5.75,1.2,GREEN,24)),run_time=.3)
        ax=Ax(-5.7,-2.2,-2.0,-.9,0,3)
        self.at('hold the neurons active'); self.play(Create(trace(ax,lambda t:.82,0,3)),FadeIn(label('SFO activity, held high',-3.9,-.65,NEUR)),run_time=.3)
        self.add(Line(ax.P(0,0),ax.P(3,0),color=LIGHT),label('time →',-3.8,-2.4,LIGHT))
        self.at('water in the gut'); self.play(FadeIn(label('gut water',-4,-3.0,TEAL)),run_time=.25)
        self.at('usual satiation'); self.play(GrowFromEdge(on,DOWN),FadeIn(label('light on',4.7,-2.15,GREEN)),FadeIn(label('Holding neurons active\nprevented satiation',2.85,-2.85,EXC,28)),run_time=.4); self.wait(2.2); self.finish()

class S16QBloodOnly(SpokenScene):
    def construct(self):
        g,m=question_stage(0); self.add(g); g[1].set_opacity(0); g[2].set_opacity(0)
        v=ValueTracker(0)
        self.add(always_redraw(lambda:model_bars(1,v.get_value(),v.get_value())),always_redraw(lambda:gauge_numbers(1,v.get_value(),v.get_value())))
        self.at('brain read only'); self.play(v.animate.set_value(.15),FadeIn(drink_drop(m)),run_time=1.2,rate_func=linear)
        self.at('How much would'); self.play(Indicate(g[-2],color=FF),run_time=.4); self.finish()

class S17Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; g,m=question_stage(.15); self.add(g); g[1].set_opacity(0); g[2].set_opacity(0)
        v=ValueTracker(.15)
        self.add(always_redraw(lambda:model_bars(1,v.get_value(),v.get_value())),always_redraw(lambda:gauge_numbers(1,v.get_value(),v.get_value())))
        drop=drink_drop(m); self.add(drop)
        for j in range(5):
            self.play(drop.animate.set_opacity(.2 if j%2 else 1),v.animate.set_value(.15+.02*(j+1)),run_time=1,rate_func=linear)

class S18ABloodOnly(SpokenScene):
    def construct(self):
        stage,m=gauge_stage(); self.add(stage,head('Fast drinking, slow absorption',size=33),label('illustrative model: k = 1/min; τ = 5 min',1.9,-3.0,LIGHT,24),label('u = kD; absorption = G/τ',1.9,-3.5,LIGHT,24))
        clock=ValueTracker(0)
        bars=always_redraw(lambda:model_bars(*state_at(clock.get_value())[1:]))
        nums=always_redraw(lambda:gauge_numbers(*state_at(clock.get_value())[1:]))
        timer=always_redraw(lambda:label(f'{clock.get_value():.1f} minutes',.4,2.85,LIGHT,24))
        drop=drink_drop(m); drop.add_updater(lambda d:d.set_opacity(.5+.5*np.cos(10*clock.get_value())))
        self.add(bars,nums,timer,drop)
        self.at('Too much'); self.play(clock.animate.set_value(1.4),run_time=1.8,rate_func=linear)
        self.at('Water reaches the blood'); self.play(clock.animate.set_value(3.1),run_time=1.3,rate_func=linear)
        self.at('keeps drinking'); self.play(clock.animate.set_value(STOP),run_time=.65,rate_func=linear)
        drop.clear_updaters(); self.remove(drop)
        self.add(label('stops at 2.48 L',-3.8,2.85,NEUR))
        self.wait(2.1); self.finish()

class S19OnItsWay(SpokenScene):
    def construct(self):
        # Keep the two physical gauges at exactly the positions and values of s18.
        stage,m=gauge_stage()
        # Each gauge contributes its rectangle, label, then 3 ticks and numbers.
        self.add(stage[8:24],model_bars(*MODEL[-1,1:])[1:],gauge_numbers(*MODEL[-1,1:])[1:],head('Count what is on its way',FF))
        eq=VGroup(label('predicted deficit',-3.75,1.7,FF,32),VGroup(T('=',38),T('D',38,BLOOD),T('−',38),T('G',38,TEAL)).arrange(RIGHT,buff=.18).move_to([-3.75,.85,0]),label('D: blood gauge',-3.75,-.1,BLOOD,28),label('− G: swallowed water\nawaiting absorption',-3.75,-1.0,TEAL,26))
        self.add(eq,label('The estimate is the blood, corrected for what is on its way.',0,-2.95,size=26),label('illustrative model; complete retention, no ongoing losses',0,-3.55,LIGHT))
        self.at('estimate must count'); self.play(Indicate(eq[3],color=TEAL),run_time=.35)
        self.finish(); self.wait(max(.1,4.5-self.elapsed()))

class S20Learned(SpokenScene):
    def construct(self):
        self.add(head('A learned cue can come before drinking',size=32),tag(x=5.3,y=3.7))
        cage=Rectangle(width=11.8,height=2.5,color=LIGHT).move_to([0,1.55,0]); m=mouse_at(-2.7,1.2,.78); b=bowl().scale(1.05).move_to([6.05,.9,0])
        ax=Ax(-5.6,5.65,-2.2,-.4,-1,3)
        f=lambda t:.8-.55*sigm(t,0,.8)
        self.add(cage,m,b,Line(ax.P(-1,0),ax.P(3,0),color=LIGHT),label('vasopressin (AVP) neurons',-3.4,-.05,AVP,26),trace(ax,f,-1,0,AVP),DashedLine(ax.P(2.3,0),ax.P(2.3,1),color=LIGHT),label('first lick',ax.X(2.3),-2.65,LIGHT),label('seconds after bowl arrives (schematic timing)',0,-3.4,LIGHT))
        self.at('In trained mice'); self.play(FadeIn(label('trained mice',3.5,2.35)),run_time=.25)
        self.at('when a water bowl arrived'); self.play(b.animate.move_to([.45,.9,0]),Create(trace(ax,f,0,1.8,AVP)),FadeIn(DashedLine(ax.P(0,0),ax.P(0,1),color=TEAL)),FadeIn(label('bowl arrives',ax.X(0),-2.65,TEAL)),run_time=.65)
        self.at('before any drinking'); self.play(FadeIn(label('dip before first lick',1.35,-.85,AVP)),Create(bracket(ax.X(.8),ax.X(2.3),-1.85,'',AVP)),run_time=.25)
        self.wait(3); self.finish()

class S21Kinds(SpokenScene):
    def construct(self):
        self.add(head('Two kinds of feedforward',FF))
        boxes=VGroup(*[RoundedRectangle(width=5.8,height=5.3,corner_radius=.18,color=FF).move_to([x,-.15,0]) for x in (-3.2,3.2)])
        m=mouse_at(-4,.15,.48); sp=spout(m); organ=Ellipse(width=.9,height=1.05,color=TEAL,fill_color=TEAL,fill_opacity=.25).move_to([-1.65,.15,0]); b=bowl().scale(1.25).move_to([3.2,.55,0])
        self.add(boxes,m,sp,drink_drop(m),organ,b)
        self.at('sense fluid going in'); self.play(FadeIn(label('sensed',-3.2,1.85,FF,38)),FadeIn(label('mouth and gut',-3.2,-1.7,size=32)),run_time=.3)
        self.at('predict it from'); self.play(FadeIn(label('predicted',3.2,1.85,FF,38)),FadeIn(label('learned cue',3.2,-1.7,size=32)),run_time=.3); self.finish()

class S22Limits(SpokenScene):
    def construct(self):
        c=cluster(-4,0,1.25); self.add(c,head('What was measured?'))
        rows=[T('population calcium; not spikes',28,NEUR),T('recorded in mice',30,TEXT),T('not the feeling of thirst',34,FF,weight=BOLD)]
        for r,y in zip(rows,(1.5,0,-1.5)): r.move_to([-.9,y,0],aligned_edge=LEFT)
        self.at('population calcium'); self.play(FadeIn(rows[0]),run_time=.3)
        self.at('recorded in mice'); self.play(FadeIn(rows[1]),run_time=.3)
        self.at('not the feeling'); self.play(FadeIn(rows[2]),run_time=.3); self.finish()

class S23Takeaway(SpokenScene):
    def construct(self):
        self.add(head('The blood, corrected for what is on its way',size=32))
        boxes=VGroup(*[RoundedRectangle(width=5.8,height=2.45,corner_radius=.17,color=c).move_to([x,1.25,0]) for x,c in ((-3.2,FB),(3.2,FF))]); self.add(boxes)
        self.at('Feedback reads'); self.play(FadeIn(label('Feedback\nreads the blood now',-3.2,1.25,FB,32)),run_time=.3)
        self.at('Feedforward reads'); self.play(FadeIn(label('Feedforward\nreads what is coming',3.2,1.25,FF,32)),FadeIn(label('mouth • gut • learned cues',3.2,-.55,FF,28)),run_time=.3)
        self.at('The estimate is'); self.play(FadeIn(label('The estimate = the blood,',0,-1.65,size=34)),run_time=.25)
        self.at('corrected for'); self.play(FadeIn(label('corrected for what is on its way.',0,-2.65,FF,34)),run_time=.25); self.finish()

class S24End(EndCard):
    LINE='Feedforward reads what is coming.'
