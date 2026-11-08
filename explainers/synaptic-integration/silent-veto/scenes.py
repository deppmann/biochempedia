"""Chapter 4: computed passive-cell responses, timed to the final narration.
COLOR MAP: GREEN excitation/current; RED shunt; GREY leak/axes;
YELLOW voltage and without-shunt comparison; TEAL threshold.
All traces solve C dV/dt = sum(g*(E-V)) + I, C=200 pF.
"""
import numpy as np
from bp_style import *
EL, EE, EI, THR = -65., 0., -65., -50.
C, GL, GE, GI = 200., 10., 5., 10.

def vss(gL,gE,gI):
    return (gL*EL+gE*EE+gI*EI)/(gL+gE+gI)

def txt(s,x=0,y=2.9,size=30,color=TEXT):
    return T(s,size=size,color=color).move_to([x,y,0])

def curve(ax,xs,ys,color=YELLOW,width=5):
    return VMobject(color=color,stroke_width=width).set_points_as_corners(
        [ax.c2p(float(x),float(y)) for x,y in zip(xs,ys)])

def plot(xr,yr,w,h,center,xticks,yticks,xlabel='time (ms)',ylabel='mV'):
    ax=Axes(x_range=xr,y_range=yr,x_length=w,y_length=h,tips=False,
        axis_config={'color':GREY,'include_ticks':False}).move_to([*center,0])
    # Explicit labels: no implicit tiny Manim tick text or top-axis ticks.
    ax.x_axis.set_opacity(0)
    labs=VGroup(Line(ax.c2p(xr[0],yr[0]),ax.c2p(xr[1],yr[0]),color=GREY))
    for t in xticks:
        pt=ax.c2p(t,yr[0]);labs.add(Line(pt+UP*.055,pt+DOWN*.055,color=GREY),M(str(t),26,GREY).move_to(pt+DOWN*.25))
    for v in yticks:
        pt=ax.c2p(xr[0],v);labs.add(Line(pt+LEFT*.055,pt+RIGHT*.055,color=GREY),M(str(v).replace('-', '−'),26,GREY).move_to(pt+LEFT*.44))
    labs.add(txt(xlabel,center[0],center[1]-h/2-.65,26,GREY),
             txt(ylabel,center[0]-w/2+.55,center[1]+h/2+.28,26,GREY))
    return ax,labs

def question(n):
    lines=['Pause. What does the shunt', 'do at rest?'] if n==1 else ['Pause. Excitation plus shunt from rest:', 'where does the marker settle?']
    return VGroup(*[T(s,38,YELLOW) for s in lines]).arrange(DOWN,buff=.16).move_to([0,-2.9,0])

class RopeStage:
    def __init__(self,v=EL,exc=False,shunt=False,compact=False):
        self.v=ValueTracker(v);self.x=lambda v:-5.2+(v+65)*10.4/65
        self.y=1.65 if compact else .25
        top=2.55 if compact else 2.05
        bottom=.45 if compact else -1.8
        self.axis=VGroup(Line([-5.7,self.y,0],[5.7,self.y,0],color=GREY),
            DashedLine([self.x(THR),self.y-.3,0],[self.x(THR),top-.05,0],color=TEAL),
            txt('threshold −50 mV',-.6,3.4,26,TEAL),
            Line([self.x(THR),3.25,0],[self.x(THR),top+.05,0],color=TEAL,stroke_width=2),
            txt('−65 mV',-6.,self.y+.55,26,GREY),txt('0 mV',5.2,self.y-.48,26,GREEN))
        self.leak=VGroup(Dot([self.x(EL),top,0],radius=.12,color=GREY),txt('leak · 10 nS',-4.6,top+.45,26,GREY))
        self.lr=always_redraw(lambda:Line([self.x(EL),top,0],[self.x(self.v.get_value()),self.y,0],color=GREY,stroke_width=6))
        self.exc=VGroup(Dot([self.x(EE),top,0],radius=.12,color=GREEN),txt('excitation · 5 nS',4.3,top+.45,26,GREEN))
        self.er=always_redraw(lambda:Line([self.x(EE),top,0],[self.x(self.v.get_value()),self.y,0],color=GREEN,stroke_width=6))
        self.shunt=VGroup(Dot([self.x(EI),bottom,0],radius=.14,color=RED),txt('shunt · 10 nS',-3.4,bottom,26,RED))
        def rope():
            end=[self.x(self.v.get_value()),self.y,0]
            if abs(self.v.get_value()-EL)<.01:
                return VMobject(color=RED,stroke_width=6).set_points_smoothly([[self.x(EI),bottom,0],[-5.9,bottom+.2,0],[-5.9,self.y-.3,0],end])
            return Line([self.x(EI),bottom,0],end,color=RED,stroke_width=9)
        self.sr=always_redraw(rope)
        self.dot=always_redraw(lambda:Dot([self.x(self.v.get_value()),self.y,0],radius=.27,color=YELLOW))
        self.base=VGroup(self.axis,self.leak,self.lr,self.dot)
        self.active_exc=exc;self.active_shunt=shunt
    def add(self,s):
        s.add(self.base)
        if self.active_exc:s.add(self.exc,self.er)
        if self.active_shunt:s.add(self.shunt,self.sr)
    def move(self,s,target,duration=1.):
        s.play(self.v.animate.set_value(target),run_time=duration,
            rate_func=lambda u:(1-np.exp(-5*u))/(1-np.exp(-5)))

def trace_axes():
    ax,labs=plot([0,40,10],[0,26,10],10.4,4.8,(.2,-.05),[0,10,20,30,40],[0,10,20],ylabel='change from rest (mV)')
    return ax,labs

def response(ax,gi):
    t=np.linspace(0,40,401);dv=vss(GL,GE,gi)-EL
    return curve(ax,t,dv*(1-np.exp(-t/(C/(GL+GE+gi)))),RED if gi else YELLOW)

def pulse_values(t,tau,second=True):
    return 2*np.exp(-t/tau)+(np.where(t>=10,2*np.exp(-(t-10)/tau),0) if second else 0)

def pulse_trace(ax,tau,start=0,end=30,second=True):
    t=np.linspace(start,end,301)
    if start<10<=end and second:t=np.sort(np.r_[t,10-1e-6,10])
    v=pulse_values(t,tau,second)
    if start==0:t=np.r_[0,t];v=np.r_[0,v]
    return curve(ax,t,v,YELLOW if tau==20 else RED)

def pulse_panel():
    ax,labs=plot([0,30,10],[0,4,1],10.2,4.7,(.25,-.05),[0,10,20,30],[0,2,4],ylabel='depolarization (mV)')
    labs[-1].shift(UP*.22)
    labs.add(txt('without shunt · τ = 20 ms',-2.7,3.35,26,YELLOW),txt('with shunt · τ = 10 ms',3.05,3.35,26,RED))
    return ax,labs,pulse_trace(ax,20),pulse_trace(ax,10)

def small_voltage_panel(kind='step'):
    return plot([0,40,20],[-65,-40,10],9.6,1.85,(.35,-1.95),[0,20,40],[-65,-50],ylabel='Vm (mV)')

def spark_at(p):
    return VGroup(*[Line(p+.12*np.array([np.cos(a),np.sin(a),0]),p+.35*np.array([np.cos(a),np.sin(a),0]),color=YELLOW,stroke_width=4) for a in np.linspace(0,2*PI,9)[:-1]])

class S00Title(TitleCard):
    LESSON='Integration, Inhibition and Neuromodulation'
    TITLE='Inhibition That Moves Nothing at Rest'
    def construct(self):
        brand=T('BIOCHEMISTRYPEDIA',22,TEAL)
        lesson=T(self.LESSON.upper(),22,GREY)
        title=VGroup(T('Inhibition That Moves',44,font=TITLE_FONT),T('Nothing at Rest',44,font=TITLE_FONT)).arrange(DOWN,buff=.22)
        rule=Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)
        VGroup(brand,lesson,title,rule).arrange(DOWN,buff=.35)
        self.play(FadeIn(brand),FadeIn(lesson),run_time=.4)
        self.play(FadeIn(title),GrowFromCenter(rule),run_time=.5)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        ax,labs=plot([0,40,10],[-70,-40,10],10.3,4.4,(.25,-.65),[0,20,40],[-65,-50],ylabel='Vm (mV)')
        self.add(ax,labs,txt('Can an input stop a spike without moving',y=3.3,size=32),txt("a resting cell's voltage at all?",y=2.7,size=32))
        self.at('Can an input')
        line=curve(ax,[0,40],[EL,EL]);self.play(Create(line),run_time=.5)
        self.at('stop a spike')
        self.play(Create(DashedLine(ax.c2p(0,THR),ax.c2p(40,THR),color=TEAL)),FadeIn(txt('threshold',3.7,.55,26,TEAL)),run_time=.4)
        self.at("resting cell's")
        self.play(FadeIn(txt('rest −65 mV',3.6,-1.9,28,YELLOW)),run_time=.4)
        # Turn the resting voltage into the rope marker, bridging the new scale.
        st=RopeStage();marker=Dot([st.x(EL),st.y,0],radius=.27,color=YELLOW)
        self.play(Transform(line,marker),FadeOut(Group(*[m for m in self.mobjects if m is not line])),run_time=.9)
        self.remove(line);self.add(st.dot)
        self.play(FadeIn(st.axis),FadeIn(st.leak),FadeIn(st.lr),run_time=.45)
        self.finish()

class S02Setup(SpokenScene):
    def construct(self):
        st=RopeStage();st.add(self)
        rest_label=txt('Resting cell',0,-2.9,34,YELLOW);self.add(rest_label)
        self.at('Our cell starts')
        self.play(Indicate(st.dot),run_time=.4)
        self.at('Alone')
        self.play(Create(st.er),FadeIn(st.exc),run_time=.5)
        self.at('would carry it')
        ghostv=ValueTracker(EL)
        ghost=always_redraw(lambda:Circle(radius=.3,color=YELLOW,stroke_width=4).set_stroke(opacity=.85).set_fill(opacity=0).move_to([st.x(ghostv.get_value()),st.y,0]))
        self.add(ghost)
        self.play(FadeOut(rest_label),FadeIn(txt('excitation alone · passive prediction',0,-2.25,28,YELLOW)),ghostv.animate.set_value(THR),run_time=.65)
        self.at('past threshold')
        spark=spark_at(np.array([st.x(THR),st.y+.1,0]))
        self.play(Create(spark),FadeIn(txt('spike at crossing',.2,2.4,28,YELLOW)),ghostv.animate.set_value(vss(GL,GE,0)),run_time=.5)
        self.at('would fire')
        self.play(FadeIn(txt('−43.3 mV',0,-3.4,32,YELLOW)),run_time=.25)
        self.finish()

class S03Shunt(SpokenScene):
    def construct(self):
        # Excitation and its ghost result have been cleared. The real cell is at rest.
        st=RopeStage();st.add(self)
        self.add(txt('Resting cell · −65 mV',0,-3,32,YELLOW))
        self.at('inhibitory rope')
        self.play(Create(st.sr),FadeIn(st.shunt[0]),run_time=.5)
        self.at('of ten')
        self.play(FadeIn(st.shunt[1]),run_time=.3)
        self.at('tied exactly at rest')
        self.play(Indicate(st.shunt[0],color=RED,scale_factor=2),FadeIn(txt('peg = rest = −65 mV',1.8,-1.8,28,RED)),run_time=.6)
        self.finish()

class S04Predict1(SpokenScene):
    def construct(self):
        RopeStage(shunt=True).add(self)
        self.at('First')
        self.play(FadeIn(question(1)),run_time=.3)
        self.finish()

class S05Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        RopeStage(shunt=True).add(self);self.add(question(1));self.wait(5)

class S06Reveal1(SpokenScene):
    def construct(self):
        st=RopeStage(shunt=True,compact=True);st.add(self)
        ax,labs=small_voltage_panel();self.add(ax,labs)
        self.at('Nothing')
        self.play(Create(curve(ax,[0,40],[EL,EL])),run_time=.5)
        self.at('where the marker sits')
        self.play(Indicate(st.dot),run_time=.5)
        self.at('The trace stays')
        eq=VGroup(M('(−650',30,GREY),M('− 650)',30,RED),M('/ (10',30,GREY),M('+ 10)',30,RED),M('= −65 mV',30,YELLOW)).arrange(RIGHT,buff=.13).move_to([.6,-.2,0])
        self.play(FadeIn(eq),run_time=.4)
        self.finish()

class S07Predict2(SpokenScene):
    def construct(self):
        st=RopeStage();st.add(self)
        self.at('start again from rest');self.play(Indicate(st.dot),run_time=.4)
        self.at('switch on')
        self.play(Create(st.er),Create(st.sr),FadeIn(st.exc),FadeIn(st.shunt),run_time=.6)
        self.at('Where does the marker')
        self.play(FadeIn(question(2)),run_time=.3)
        self.finish()

class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        RopeStage(exc=True,shunt=True).add(self);self.add(question(2));self.wait(5)

class S09Reveal2(SpokenScene):
    def construct(self):
        st=RopeStage(exc=True,shunt=True,compact=True);st.add(self)
        ax,labs=small_voltage_panel();self.add(ax,labs)
        threshold=DashedLine(ax.c2p(0,THR),ax.c2p(40,THR),color=TEAL)
        self.add(threshold,txt('passive model',4.1,-.65,26,GREY))
        t=np.linspace(0,40,401)
        no=EL+(vss(GL,GE,0)-EL)*(1-np.exp(-t/(C/(GL+GE))))
        yes=EL+(vss(GL,GE,GI)-EL)*(1-np.exp(-t/(C/(GL+GE+GI))))
        self.at('Toward minus')
        self.play(Create(DashedVMobject(curve(ax,t,no),num_dashes=45)),run_time=.5)
        crossing=-(C/(GL+GE))*np.log(1-(THR-EL)/(vss(GL,GE,0)-EL))
        spark=spark_at(ax.c2p(crossing,THR));self.add(spark)
        self.add(txt('without shunt',-1.4,-.7,26,YELLOW))
        self.play(Create(curve(ax,t,yes,RED)),st.v.animate.set_value(vss(GL,GE,GI)),FadeOut(spark),FadeIn(txt('with shunt',2.8,-3.16,26,RED)),run_time=.9)
        self.at('below threshold')
        self.play(FadeIn(txt('−52.0 mV',2.9,-2.35,28,RED)),FadeIn(M('−1300 / 25 = −52.0 mV',28,YELLOW).move_to([1.3,-.05,0])),run_time=.3)
        self.at('never fires')
        self.play(FadeIn(txt('no spike',1.,-.65,30,TEXT)),run_time=.25)
        self.finish()

class S10Why(SpokenScene):
    def construct(self):
        zero=M('10 × 0',48,RED).move_to([2.4,1.25,0])
        top=M('5 × 65 +',48,GREEN).move_to([-1.7,1.25,0])
        den=M('15',50,GREY).move_to([0,-.8,0])
        box=SurroundingRectangle(zero,color=RED,buff=.16)
        self.add(txt('Change from rest',y=3.2,size=38),M('ΔV =',44,YELLOW).move_to([-5.1,.35,0]),top,zero,Line([-3.7,.35,0],[4.7,.35,0],color=GREY),den,
            txt('65 mV: excitation’s driving force',0,2.35,28,GREEN),txt('15 = leak 10 + excitation 5',0,-1.8,30,GREY))
        self.at('top line term')
        self.play(Create(box),run_time=.3)
        self.at('is zero')
        target=M('0',48,RED).move_to(zero)
        self.play(Transform(zero,target),Transform(box,SurroundingRectangle(target,color=RED,buff=.16)),Create(Arrow([3.5,.65,0],[2.7,1.05,0],buff=.05,color=RED)),run_time=.4)
        self.at('adds nothing')
        self.play(Transform(top,M('325 +',48,GREEN).move_to(top)),run_time=.35)
        self.at('bottom line')
        self.play(Transform(den,M('15 + 10 = 25',50,RED).move_to(den)),run_time=.5)
        self.at('total conductance')
        self.play(FadeIn(txt('total conductance (nS)',0,-2.8,30,RED)),run_time=.3)
        self.finish()

class S11Cut(SpokenScene):
    def construct(self):
        ax,labs=plot([0,4,1],[0,25,10],8.8,4.6,(.4,-.2),[],[0,10,20],xlabel='',ylabel='')
        self.add(txt('Depolarization (mV)',y=3.35,size=32))
        h=lambda v:v*4.6/25
        b1=Rectangle(width=1.8,height=h(vss(GL,GE,0)-EL),color=YELLOW,fill_opacity=.4).move_to(ax.c2p(1,(vss(GL,GE,0)-EL)/2))
        b2=Rectangle(width=1.8,height=h(13),color=RED,fill_opacity=.4).move_to(ax.c2p(3,6.5))
        self.add(ax,labs,b1,txt('21.7 mV',-1.8,2.7,30,YELLOW),txt('without shunt',-1.8,-3.15,28,YELLOW),txt('with shunt',2.6,-3.15,28,RED))
        self.at('depolarization falls')
        self.play(Indicate(b1),run_time=.4)
        self.at('to thirteen')
        self.play(GrowFromEdge(b2,DOWN),FadeIn(txt('13.0 mV',2.6,.4,30,RED)),run_time=.35)
        p1=ax.c2p(2,21.6667);p2=ax.c2p(2,13)
        self.play(Create(DoubleArrow(p1,p2,buff=0,color=TEXT)),FadeIn(txt('× 15/25 = 0.60',3.7,1.8,28)),Create(Line((p1+p2)/2,[2.1,1.8,0],color=TEXT,stroke_width=2)),run_time=.25)
        self.finish()

class S12Name(SpokenScene):
    def construct(self):
        ax,labs=trace_axes();self.add(ax,labs,curve(ax,[0,40],[0,0]))
        self.at('shunting inhibition')
        self.play(FadeIn(txt('Shunting inhibition',y=3.4,size=36,color=RED)),run_time=.4)
        self.at('moves nothing at rest')
        self.play(FadeIn(txt('at rest: no change',0,.4,34,YELLOW)),FadeIn(chip('tied exactly at rest',RED,26).move_to([2.2,-1.,0])),run_time=.4)
        self.finish()

class S13Shows(SpokenScene):
    def construct(self):
        ax,labs=trace_axes();flat=curve(ax,[0,40],[0,0]);self.add(ax,labs,flat,txt('Shunting inhibition',y=3.4,size=36,color=RED))
        self.add(DashedLine(ax.c2p(0,15),ax.c2p(40,15),color=TEAL),txt('threshold +15 mV',-1.6,1.2,26,TEAL))
        self.at('something else tries')
        onset=Arrow(ax.c2p(0,7),ax.c2p(0,.5),buff=0,color=GREEN)
        self.play(FadeOut(flat),Create(onset),FadeIn(txt('excitation on',-3.6,1.9,26,GREEN)),run_time=.3)
        self.play(Create(DashedVMobject(response(ax,0),num_dashes=50)),FadeIn(txt('without shunt',2.9,2.05,28,YELLOW)),run_time=.8)
        self.at('Then it cuts')
        self.play(Create(response(ax,GI)),FadeIn(txt('with shunt · 13.0 mV',2.6,-.55,28,RED)),run_time=.7)
        self.finish()

class S14Rope(SpokenScene):
    def construct(self):
        st=RopeStage(shunt=True);st.add(self)
        self.add(txt('Tied at rest',0,-3.,34,RED))
        self.at('rope tied');self.play(Indicate(st.shunt[0]),run_time=.4)
        self.at('holds the marker back')
        self.play(FadeIn(st.exc),Create(st.er),run_time=.4)
        self.at('another rope drags')
        st.move(self,vss(GL,GE,GI),.7)
        start=np.array([st.x(-52),st.y,0]);end=np.array([st.x(EL),-1.8,0])
        arrow=Arrow(start,end,buff=.24,color=RED,stroke_width=9)
        self.play(Create(arrow),run_time=.3)
        self.play(FadeIn(txt('130 pA back toward rest',1.6,-1.5,30,RED)),FadeIn(txt('10 nS × 13 mV',1.6,-2.2,28,RED)),run_time=.3)
        self.finish()

class S15Resistance(SpokenScene):
    def construct(self):
        formula=M('R = 1 / total g',48).move_to([0,2.2,0])
        gbar=Rectangle(width=3.2,height=.6,color=RED,fill_opacity=.7).move_to([.2,.4,0])
        rbar=Rectangle(width=5.8,height=.6,color=YELLOW,fill_opacity=.7).move_to([.2,-1.7,0])
        glabel=txt('total g',-4.4,.4,32,RED);rlabel=txt('R',-4.4,-1.7,36,YELLOW)
        self.add(txt('Input resistance',y=3.4,size=38),formula,gbar,rbar,glabel,rlabel)
        self.at('lowers input resistance')
        self.play(gbar.animate.stretch_to_fit_width(6.4),rbar.animate.stretch_to_fit_width(2.9),run_time=.6)
        # Full-height comparison panels; input icons occupy a separate header row.
        panels=[]
        for x in (-3.25,3.25):
            ax,labs=plot([0,40,20],[0,24,10],4.9,2.85,(x,-1.05),[0,20,40],[0,10,20],ylabel='depolarization (mV)')
            labs[-1].move_to([x,.72,0])
            panels.append((ax,labs))
        def pair_labels(ax):
            return VGroup(T('without shunt',26,YELLOW).move_to(ax.c2p(27,22)),
                          T('with shunt',26,RED).move_to(ax.c2p(28,5)))
        self.at('synaptic conductance')
        syn=VGroup(Line([-5.4,1.45,0],[-4.2,1.45,0],color=GREY,stroke_width=7),
            Rectangle(width=.35,height=.45,color=GREEN,fill_opacity=.35).move_to([-4.8,1.45,0]),
            Arrow([-4.8,1.98,0],[-4.8,1.7,0],buff=0,color=GREEN),txt('synapse',-3.05,1.45,28,GREEN))
        ax,labs=panels[0]
        self.play(formula.animate.scale(36/48).move_to([0,2.8,0]),
            gbar.animate.stretch_to_fit_width(3.3).stretch_to_fit_height(.38).move_to([-2.8,2.15,0]),
            rbar.animate.stretch_to_fit_width(1.65).stretch_to_fit_height(.38).move_to([3.1,2.15,0]),
            glabel.animate.scale(26/32).move_to([-5.3,2.15,0]),rlabel.animate.scale(26/36).move_to([1.8,2.15,0]),
            FadeIn(syn),FadeIn(ax),FadeIn(labs),run_time=.4)
        self.play(Create(response(ax,0)),Create(response(ax,GI)),run_time=.4)
        self.add(pair_labels(ax))
        self.at('injected current')
        pip=Polygon([1.05,1.85,0],[1.3,2.0,0],[2.1,1.25,0],[2.06,1.16,0],color=GREEN,fill_opacity=.25)
        elec=VGroup(pip,txt('electrode',3.9,1.8,26,GREEN),
            Arrow([3.25,1.2,0],[2.2,1.2,0],buff=0,color=GREEN),txt('current',4.35,1.2,26,GREEN))
        ax,labs=panels[1];t=np.linspace(0,40,301)
        self.play(FadeIn(elec),FadeIn(ax),FadeIn(labs),run_time=.25)
        self.play(Create(curve(ax,t,200/GL*(1-np.exp(-t/(C/GL))))),Create(curve(ax,t,200/(GL+GI)*(1-np.exp(-t/(C/(GL+GI)))),RED)),run_time=.4)
        self.add(pair_labels(ax))
        self.finish()

class S16Rule(SpokenScene):
    def construct(self):
        bottom=M('15 + 10',54,RED).move_to([.8,-1,0])
        self.add(txt('The shunt changed only the bottom line.',y=3,size=34),M('ΔV =',48,YELLOW).move_to([-4,.4,0]),M('325 + 0',54).move_to([.8,1.4,0]),Line([-2.4,.4,0],[4,.4,0],color=GREY),bottom)
        self.at('changed only')
        box=SurroundingRectangle(bottom,color=RED,buff=.3)
        self.play(Create(box),run_time=.3)
        self.at('bottom line')
        self.play(Indicate(box,color=RED,scale_factor=1.08),run_time=.4)
        self.finish()

class S17Tau(SpokenScene):
    def construct(self):
        den=txt('total g',.5,.4,44,RED)
        tau=VGroup(M('τ',52,YELLOW),T('eff',26,YELLOW).shift(DOWN*.15),M('=',48)).arrange(RIGHT,buff=.1).move_to([-4.1,1.3,0])
        g=Rectangle(width=2,height=.45,color=RED,fill_opacity=.5).move_to([-2.6,-1.6,0])
        t=Rectangle(width=3.8,height=.45,color=YELLOW,fill_opacity=.5).move_to([2.6,-1.6,0])
        self.add(txt('Time constant',y=3.1,size=40),tau,M('C',54).move_to([.5,2.,0]),Line([-1.8,1.3,0],[3.,1.3,0],color=GREY),den,g,t,txt('total g',-2.6,-2.35,30,RED),txt('τ',2.6,-2.35,36,YELLOW))
        self.at('second thing')
        self.play(Indicate(den),run_time=.3)
        self.at('shortens the time constant')
        self.play(g.animate.stretch_to_fit_width(4.),t.animate.stretch_to_fit_width(1.9),den.animate.scale(1.2),Create(Arrow([4.7,-.8,0],[3.7,-1.6,0],color=YELLOW,buff=.1)),FadeIn(txt('τ shrinks',4.6,-.2,30,YELLOW)),run_time=.7)
        self.finish()

class S18Cellb(SpokenScene):
    def construct(self):
        st=RopeStage(vss(GL,GE,GI),exc=True,shunt=True,compact=True);st.add(self)
        ax,labs=small_voltage_panel();self.add(ax,labs)
        self.at('switch off the excitation')
        self.play(FadeOut(st.exc),FadeOut(st.er),run_time=.4)
        self.at('return to rest')
        t=np.linspace(0,40,401)
        clock=ValueTracker(0)
        decay=always_redraw(lambda:curve(ax,np.linspace(0,max(clock.get_value(),.001),201),EL+13*np.exp(-np.linspace(0,max(clock.get_value(),.001),201)/10),RED))
        cursor=always_redraw(lambda:Dot(ax.c2p(clock.get_value(),EL+13*np.exp(-clock.get_value()/10)),radius=.08,color=RED))
        st.v.add_updater(lambda v:v.set_value(EL+13*np.exp(-clock.get_value()/10)))
        self.add(st.v);self.bring_to_back(st.v)
        self.add(decay,cursor)
        self.play(clock.animate.set_value(40),run_time=1.6,rate_func=linear)
        st.v.clear_updaters()
        self.at('With the leak')
        self.play(FadeIn(txt('τ = 200 pF / 20 nS = 10 ms',.9,-.65,28,YELLOW)),run_time=.4)
        self.at("half the leak's")
        self.play(Create(DashedVMobject(curve(ax,t,EL+13*np.exp(-t/20)),num_dashes=40)),FadeIn(txt('leak only · 20 ms',-.9,-1.25,26,YELLOW)),FadeIn(txt('shunt · 10 ms',3.,-1.25,26,RED)),run_time=.5)
        self.add(txt('all three open: 200/25 = 8 ms',2.1,.35,26,GREY))
        self.finish()

class S19Recall(SpokenScene):
    def construct(self):
        # Keep the rope scale above a large chapter-2 bookmark.
        st=RopeStage(shunt=True,compact=True);st.add(self)
        ax,labs=plot([0,30,10],[0,4,2],7.0,2.2,(1.2,-1.8),[0,10,20,30],[0,2,4],ylabel='mV')
        labs[-1].move_to([-2.65,-.95,0])
        panel=VGroup(ax,labs,pulse_trace(ax,10),txt('Cell B · τ = 10 ms · 2.74 mV',1.2,.05,28,RED))
        self.at('cell B')
        self.play(FadeIn(panel,shift=RIGHT*.4),run_time=.6)
        self.finish()

class S20Pulses(SpokenScene):
    def construct(self):
        ax,labs,a,b=pulse_panel();self.add(ax,labs)
        self.at('two brief pulses')
        first=VGroup(pulse_trace(ax,20,end=10,second=False),pulse_trace(ax,10,end=10,second=False))
        self.play(Create(first),run_time=.65)
        self.at('ten milliseconds apart')
        gap=DoubleArrow(ax.c2p(0,3.6),ax.c2p(10,3.6),buff=0,color=GREEN)
        self.play(Create(gap),FadeIn(txt('10 ms',-3.1,2.25,28,GREEN)),run_time=.35)
        self.at('Less of the first')
        # Residual brackets at 10 ms are offset to either side of the discontinuity.
        remaining=VGroup()
        for tau,x,col in [(20,8.7,YELLOW),(10,11.3,RED)]:
            val=2*np.exp(-10/tau)
            remaining.add(DoubleArrow(ax.c2p(x,0),ax.c2p(x,val),buff=0,color=col,stroke_width=3),
                txt(f'{val:.2f} mV',-3.35 if tau==20 else .55,-1.75,26,col))
        self.play(Create(remaining),run_time=.4)
        self.at('for the second')
        self.play(Create(pulse_trace(ax,20,start=10-1e-6)),Create(pulse_trace(ax,10,start=10-1e-6)),run_time=.65)
        self.play(FadeIn(txt('3.21 mV',-.2,1.65,28,YELLOW)),FadeIn(txt('2.74 mV',-2.9,.75,28,RED)),Create(Line(ax.c2p(10,2+2*np.exp(-1)),[-2.,.75,0],color=RED,stroke_width=2)),Create(Line(ax.c2p(10,2+2*np.exp(-.5)),[-1.1,1.65,0],color=YELLOW,stroke_width=2)),run_time=.25)
        self.finish()

class S21Jump(SpokenScene):
    def construct(self):
        ax,labs,a,b=pulse_panel();self.add(ax,labs,a,b)
        self.at('idealized case')
        self.play(FadeIn(txt('instantaneous pulses',3.3,2.5,28,GREEN)),run_time=.3)
        self.at('each jump stays')
        # Brackets sit beside the actual jumps; the complete traces stay visible.
        brackets=VGroup()
        for time in (0,10):
            for tau,dx in ((20,.8),(10,2.0)):
                base=0 if time==0 else 2*np.exp(-10/tau)
                col=YELLOW if tau==20 else RED
                x=time+dx
                lo=ax.c2p(x,base);hi=ax.c2p(x,base+2)
                brackets.add(Line(lo,hi,color=col,stroke_width=3),
                    Line(lo+LEFT*.075,lo+RIGHT*.075,color=col),
                    Line(hi+LEFT*.075,hi+RIGHT*.075,color=col))
            # One shared measurement labels the equal coloured brackets.
            label=T('2 mV each',26,TEXT).move_to(ax.c2p(time+4.8,3.75))
            brackets.add(label)
        self.play(Create(brackets),run_time=.4)
        self.at('Only the tail')
        self.play(FadeOut(brackets),run_time=.2)
        tail=pulse_trace(ax,10,start=10.05);tail.set_stroke(width=8)
        anchor=ax.c2p(24,float(pulse_values(np.array([24]),10)[0]))
        self.play(Create(tail),FadeIn(txt('shorter tail',3.5,.05,30,TEXT)),
            Create(Line([3.5,-.25,0],anchor,color=TEXT,stroke_width=2)),run_time=.4)
        self.finish()

class S22Real(SpokenScene):
    def construct(self):
        # Alpha current, peak at 1 ms: I=100*(t/td)*exp(1-t/td) pA.
        # Voltage is its analytic convolution with exp(-t/tau)/C.
        t=np.linspace(0,15,601);td=1.;amp=100.
        current=amp*(t/td)*np.exp(1-t/td)/1000 # nA
        def resp(tau):
            k=1/td-1/tau
            return amp*np.e/(C*td)*np.exp(-t/tau)*(1-(1+k*t)*np.exp(-k*t))/k**2
        upper,ul=plot([0,15,5],[0,.12,.05],10.,2.,(.35,1.65),[0,5,10,15],[0,.1],xlabel='',ylabel='current (nA)')
        lower,ll=plot([0,15,5],[0,1.3,.5],10.,2.,(.35,-1.45),[0,5,10,15],[0,.5,1],ylabel='EPSP (mV)')
        self.add(upper,ul,lower,ll,txt('synaptic current',2.9,3.1,30,GREEN))
        self.at('synaptic current flows')
        self.play(Create(curve(upper,t,current,GREEN)),FadeIn(txt('few ms',-2.2,2.3,28,GREEN)),run_time=.6)
        self.at('While it flows')
        va=resp(20);vb=resp(10)
        self.play(Create(curve(lower,t,va)),FadeIn(txt('without shunt',3.45,-.1,26,YELLOW)),run_time=.6)
        self.at('shunt drains charge')
        self.play(Create(curve(lower,t,vb,RED)),FadeIn(txt('with shunt',3.5,-2.15,26,RED)),run_time=.6)
        self.at('peak is smaller')
        pa=float(va.max());pb=float(vb.max());x=float(t[vb.argmax()])
        # Offset the measurement into the clear space after the peaks.
        measure_x=9.5
        self.play(Create(DashedLine(lower.c2p(0,pa),lower.c2p(measure_x+.3,pa),color=YELLOW)),
            Create(DashedLine(lower.c2p(x,pb),lower.c2p(measure_x,pb),color=RED)),
            Create(DoubleArrow(lower.c2p(measure_x,pb),lower.c2p(measure_x,pa),buff=0,color=TEXT,
                tip_length=.065,max_tip_length_to_length_ratio=.3,
                max_stroke_width_to_length_ratio=25,stroke_width=3)),
            FadeIn(txt('smaller peak',3.9,-.64,28)),
            Create(Line([2.55,-.85,0],lower.c2p(measure_x,pb),color=TEXT,stroke_width=2)),run_time=.4)
        self.finish()

class S23Takeaway(SpokenScene):
    def construct(self):
        # Both pictures persist throughout the takeaway; no text-only blackout.
        left,ll=plot([0,30,10],[-70,-50,10],4.5,4.3,(-3.35,-.25),[0,15,30],[-65,-50],ylabel='Vm (mV)')
        right,rl=plot([0,30,10],[0,4,2],4.5,4.3,(3.25,-.25),[0,10,30],[0,2,4],ylabel='EPSP (mV)')
        ll[-1].move_to([-3.35,1.6,0]);rl[-1].move_to([3.25,1.6,0])
        self.add(left,ll,right,rl,curve(left,[0,30],[EL,EL]),pulse_trace(right,20),pulse_trace(right,10),Line([0,-3.2,0],[0,3.3,0],color=GREY))
        self.at('A shunt tied at rest')
        self.play(FadeIn(txt('Tied exactly at rest',-3.35,3.2,30,RED)),run_time=.3)
        self.at('moves nothing at rest')
        self.play(FadeIn(txt('at rest: no change',-3.35,2.55,28,YELLOW)),run_time=.3)
        self.at('It shows itself')
        self.play(FadeIn(txt('smaller EPSP',3.25,3.2,30,RED)),run_time=.3)
        self.at('less summation')
        self.play(FadeIn(txt('less summation',3.25,2.55,28,RED)),run_time=.3)
        self.finish()

class S24End(EndCard):
    LINE='A shunt moves nothing at rest, yet shrinks EPSPs and summation.'
    def construct(self):
        lines=VGroup(T('A shunt moves nothing at rest,',38,font=TITLE_FONT),T('yet shrinks EPSPs and summation.',38,font=TITLE_FONT)).arrange(DOWN,buff=.3)
        self.play(FadeIn(lines),run_time=.5)
        self.play(FadeIn(txt('biochemistrypedia.com',y=-2.1,size=26,color=TEAL)),run_time=.3)
        self.finish()
