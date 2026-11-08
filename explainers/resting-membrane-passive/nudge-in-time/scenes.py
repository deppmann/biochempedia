"""A Nudge Takes Time: review fixes and seven-item polish round.
COLOR MAP: BLUE #58C4DD K+; ORANGE #F29E4C Na+; YELLOW #F5D547 Vm;
GREEN #83C167 balance/rules; GREY #8B93A1 structure; TEAL #3FB8C0 input.
Water is transparent teal. No molecular structures. Every trace solves the RC model.
C=200 pF, g=10 nS, I=-100 pA, rest=-71.2 mV, tau=20 ms.
"""
import numpy as np
from bp_style import *

ORANGE = '#F29E4C'
REST, CURRENT, CAP, LEAK = -71.2, -100., 200., 10.


def response(t, g=LEAK, off=60., cap=CAP):
    t = np.asarray(t)
    tau = cap/g
    return CURRENT/g*np.where(t<0, 0, np.where(t<=off,
        1-np.exp(-np.maximum(t,0)/tau),
        (1-np.exp(-off/tau))*np.exp(-(t-off)/tau)))


def label(txt, x, y, size=28, color=TEXT):
    return T(txt,size,color).move_to([x,y,0])


def heading(txt):
    return label(txt,0,3.25,32)


def curve(fn, p, a, b, color=YELLOW, width=5):
    ts=np.linspace(a,b,max(2,int(abs(b-a)*8)))
    return VMobject(stroke_color=color,stroke_width=width).set_points_as_corners([p(t,float(fn(t))) for t in ts])


def bracket(a,b,color=GREEN):
    a,b=np.array(a),np.array(b)
    return VGroup(Line(a,b,color=color,stroke_width=3),
                  Line(a+LEFT*.12,a+RIGHT*.12,color=color,stroke_width=3),
                  Line(b+LEFT*.12,b+RIGHT*.12,color=color,stroke_width=3))


class Trace:
    def __init__(self, small=False, final=False, absolute=True, tall=False):
        self.small=small
        self.x0,self.x1=(1.25,6.1) if small else (-4.8,5.9)
        self.top,self.bottom=((2.25,-2.7) if tall else (1.65,-2.65)) if small else (1.5,-2.95)
        self.p=lambda t,dv:np.array([self.x0+(t+10)/120*(self.x1-self.x0),self.top+dv/12*(self.top-self.bottom),0])
        self.axes=VGroup(Line(self.p(-10,0),self.p(-10,-12),color=GREY),
            Line(self.p(-10,-12),self.p(110,-12),color=GREY),
            label('Vm (mV)' if absolute else 'ΔV (mV)',self.x0+.7,self.top+.45,26,YELLOW),
            label('time (ms)',self.x1-.6,2.95 if small and tall else self.bottom-.65,26,GREY))
        for t in (0,60,100):
            self.axes.add(label(str(t),self.p(t,0)[0],self.bottom-.27,26,GREY))
        self.axes.add(label('−71.2' if absolute else '0',self.x0-.65,self.top,26,YELLOW))
        self.rest=curve(lambda t:0,self.p,-10,0)
        self.guide=DashedLine(self.p(-10,0),self.p(110,0),color=GREY,stroke_opacity=.5)
        if final:self.axes.add(self.final(absolute=absolute))
    def final(self,absolute=True):
        y=self.p(0,-10)[1]
        return VGroup(DashedLine(self.p(-10,-10),self.p(110,-10),color=GREEN,stroke_opacity=.65),
            label('−81.2' if absolute else '−10',self.x0-.65,y,26,GREEN))
    def path(self,a=-10,b=110,g=LEAK,off=60.,color=YELLOW,cap=CAP):
        return curve(lambda t:response(t,g,off,cap),self.p,a,b,color)
    def current(self,step=True,ended=False):
        p=lambda t,i:[self.p(t,0)[0],3.05+i/100*.65,0]
        pts=[p(-10,0),p(0,0)]
        if step:
            pts += [p(0,-100),p(60,-100)]
            if ended:pts += [p(60,0),p(110,0)]
        else:pts += [p(110,0)]
        return VGroup(VMobject(stroke_color=TEAL,stroke_width=5).set_points_as_corners(pts),
            label('I (pA)',-5.75,3.5,26,TEAL),label('0',-5.5,3.05,26,GREY),
            *([label('−100',-5.65,2.4,26,TEAL)] if step else []))


def cell_picture():
    cell=Ellipse(width=3.4,height=4.1,color=GREY,fill_color=TEAL,fill_opacity=.05).move_to([-3.8,-.2,0])
    pip=Polygon([-6.1,3.1,0],[-5.5,3.35,0],[-4.55,1.4,0],color=TEXT,fill_color=GREY,fill_opacity=.25)
    arrow=Arrow([-5.65,2.8,0],[-4.6,1.45,0],color=TEAL,buff=0)
    return VGroup(cell,pip,arrow)


def question_frame():
    tr=Trace()
    q=VGroup(label('Pause. Does Vm jump',1,-.05,38,YELLOW),
             label('when the current step begins?',1,-.8,32,YELLOW))
    ring=Circle(radius=.3,color=GREEN).move_to([3,-1.85,0])
    return VGroup(tr.axes,tr.current(),tr.rest,q,ring)


class S00Title(TitleCard):
    LESSON='The Resting Membrane and Passive Signals'
    TITLE='A Nudge Takes Time'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28,GREY),
          T(self.TITLE,54,font=TITLE_FONT),Line(LEFT*1.2,RIGHT*1.2,color=GOLD)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.6);self.finish()


class S01Question(SpokenScene):
    def construct(self):
        pic=cell_picture();tr=Trace(small=True)
        # Empty voltage panel and flat current until the step is introduced in s03.
        flat=Line([1.25,2.9,0],[6.1,2.9,0],color=TEAL,stroke_width=4)
        self.add(pic,tr.axes,flat,label('I (pA)',1.9,3.35,26,TEAL))
        self.at('Push a small')
        self.play(Indicate(pic[-1],color=TEAL),run_time=.7)
        self.at('Does the voltage')
        self.play(FadeIn(label('Does the voltage jump?',-3.4,-3,30,YELLOW)),run_time=.4)
        self.finish()


class S02Clamp(SpokenScene):
    def construct(self):
        tr=Trace();self.add(tr.axes,tr.current(step=False),tr.rest)
        pic=cell_picture().scale(.22).move_to([5,1,0]);self.add(pic)
        self.at('In Current Clamp')
        self.play(FadeIn(label('current clamp',1.5,3.5,30)),run_time=.3)
        self.at('you set the current')
        self.play(FadeIn(label('you set I',1.5,2.65,28,TEAL)),run_time=.3)
        self.at('you record its voltage')
        self.play(FadeIn(label('you record Vm',.8,-.7,34,YELLOW)),run_time=.3);self.finish()


class S03Step(SpokenScene):
    def construct(self):
        tr=Trace();cur=tr.current(step=False);self.add(tr.axes,cur,tr.rest)
        self.at('small negative step')
        self.remove(cur);new=tr.current();self.add(*new[1:]);self.play(Create(new[0]),run_time=.5)
        self.at('pushes the voltage down')
        self.play(GrowArrow(Arrow([-.5,.5,0],[-.5,-.8,0],color=YELLOW,buff=0)),
            FadeIn(label('voltage moves down',2,-.2,30,YELLOW)),run_time=.4);self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        q=question_frame();self.add(q[0],q[1],q[2])
        self.at('does the voltage jump')
        self.play(FadeIn(q[3]),FadeIn(q[4]),run_time=.4);self.finish()


class S05Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        q=question_frame();self.add(q)
        self.play(Uncreate(q[-1]),run_time=5,rate_func=linear)


class S06Reveal(SpokenScene):
    def construct(self):
        tr=Trace();self.add(tr.axes,tr.current(),tr.rest,tr.guide)
        self.at('it starts moving')
        self.play(Create(tr.path(0,12)),run_time=1.4,rate_func=linear)
        self.at('steeply at first')
        self.play(Create(tr.path(12,30)),run_time=.8,rate_func=linear)
        self.at('then bending over')
        self.play(Create(tr.path(30,60)),FadeIn(tr.final()),run_time=1,rate_func=linear);self.finish()


class S07Off(SpokenScene):
    def construct(self):
        tr=Trace(final=True);cur=tr.current();self.add(tr.axes,cur,tr.path(-10,60),tr.guide)
        self.at('When the step ends')
        self.remove(cur);new=tr.current(ended=True);self.add(*new[1:]);self.play(Create(new[0]),run_time=.35)
        self.at('it relaxes back')
        self.play(Create(tr.path(60,110)),run_time=2.2,rate_func=linear);self.finish()


def membrane():
    block=Rectangle(width=11.4,height=1.15,color=GREY,fill_color=GREY,fill_opacity=.65)
    core=Rectangle(width=11.4,height=.62,stroke_width=0,fill_color=TEXT,fill_opacity=.4)
    charges=VGroup(*[label('+' if y>0 else '−',x,y,34,YELLOW)
        for y in (-1.05,1.05) for x in np.linspace(-4.9,4.9,9)])
    labs=VGroup(label('outside • salty solution',0,2.45,34),label('inside • salty solution',0,-2.45,34),
        label('thin membrane',0,-1.65,28,GREY))
    return VGroup(block,core),charges,labs


class S08Why(SpokenScene):
    def construct(self):
        pic=cell_picture().scale(.65).move_to([0,0,0]);self.add(pic)
        block,charges,labs=membrane()
        self.at('membrane stores charge')
        self.play(FadeOut(pic),FadeIn(block),FadeIn(charges),FadeIn(labs),run_time=.8)
        self.at('two salty solutions')
        self.play(Indicate(labs[0]),Indicate(labs[1]),run_time=.6)
        self.at('a capacitor')
        self.play(FadeIn(heading('capacitor (C)')),run_time=.3);self.finish()


class S09Parallel(SpokenScene):
    def construct(self):
        wires=VGroup(Line([-3.5,2.5,0],[3,2.5,0],color=GREY),Line([-3.5,-2.5,0],[3,-2.5,0],color=GREY))
        cap=VGroup(Line([-3.5,2.5,0],[-3.5,.3,0],color=GREY),Line([-3.5,-.3,0],[-3.5,-2.5,0],color=GREY),
            Line([-4.4,.3,0],[-2.6,.3,0],color=YELLOW,stroke_width=5),Line([-4.4,-.3,0],[-2.6,-.3,0],color=YELLOW,stroke_width=5))
        resistor=VGroup(Line([3,2.5,0],[3,.85,0],color=GREY),Rectangle(width=.6,height=1.7,color=TEXT).move_to([3,0,0]),Line([3,-.85,0],[3,-2.5,0],color=GREY))
        self.add(wires,cap,label('C',-4.9,0,34,YELLOW),label('outside',0,3.05,30),label('inside',0,-3.05,30),label('membrane',-5,-1.2,26,GREY))
        self.at('leak channels are resistors')
        self.play(Create(resistor),FadeIn(VGroup(label('leak = resistor',4.65,.25,26),label('(g_total)',4.65,-.35,26,GREEN))),run_time=.6)
        self.at('side by side')
        self.play(Indicate(cap),Indicate(resistor),run_time=.5);self.finish()


class Tank:
    def __init__(self,x=-3.7,width=3.7,drain_width=12):
        self.x,self.w=x,width
        self.bottom,self.top=-2.65,2.65
        self.outline=VGroup(Line([x-width/2,self.top,0],[x-width/2,self.bottom,0],color=GREY,stroke_width=4),
            Line([x-width/2,self.bottom,0],[x+width/2,self.bottom,0],color=GREY,stroke_width=4),
            Line([x+width/2,self.bottom,0],[x+width/2,self.top,0],color=GREY,stroke_width=4))
        self.drain=Line([x+.55,-2.65,0],[x+.55,-3.05,0],color=GREY,stroke_width=drain_width)
        self.hose=VGroup(Line([x-1.2,3.1,0],[x-.45,3.1,0],color=TEAL,stroke_width=10),
            Arrow([x-.45,3.1,0],[x-.45,2.4,0],color=TEAL,stroke_width=8,buff=0,max_tip_length_to_length_ratio=.25))
    def hose_labels(self):
        return VGroup(label('injected current',self.x+1.15,2.95,24,TEAL),
                      label('size of I',self.x+1.15,2.48,24,TEAL))
    def stream(self,level=lambda:0):
        # Droplets travel from the nozzle to the instantaneous water surface.
        phase=[0.]
        drops=VGroup()
        def update(m,dt):
            phase[0]=(phase[0]+dt*1.3)%1
            top=2.35;bottom=-2.6+4.7*level()
            m.become(VGroup(*[Dot([self.x-.45,top-(top-bottom)*((i/9+phase[0])%1),0],
                                 radius=.045,color=TEAL) for i in range(9)]))
        update(drops,0)
        drops.add_updater(update)
        return drops
    def water(self,f):
        h=max(.012,4.7*f)
        return Rectangle(width=self.w-.1,height=h,stroke_width=0,fill_color=TEAL,fill_opacity=.55).move_to([self.x,-2.6+h/2,0])
    def flow(self,f):
        # Same length/width as inflow at f=1; grows with extra pressure/level.
        f=max(.001,f)
        return Arrow([self.x+.55,-3.05,0],[self.x+.55+.75*f,-3.05,0],color=TEAL,stroke_width=8*f,buff=0,max_tip_length_to_length_ratio=.25)
    def dot(self,f):
        return Dot([self.x+.9,-2.6+4.7*f,0],color=YELLOW,radius=.08)


def tank_base(f=0,hose=True,drain_label=True,compact_trace=False):
    tank=Tank();tr=Trace(small=True,tall=not compact_trace)
    if compact_trace:tr.axes[3].move_to([5.5,1.95,0])
    water=tank.water(f)
    group=VGroup(tank.outline,tank.drain,water,tr.axes,tr.guide,
        label('level = size of ΔV',-3.7,-3.6,26,YELLOW),
        label('(up even though Vm goes down)',2.5,-3.6,26,YELLOW))
    if hose:group.add(tank.hose,tank.hose_labels(),tank.stream(lambda: water.height/4.7))
    if drain_label:group.add(label('leak (g_total)',-4.65,-3.03,26,GREEN))
    return tank,tr,water,group


def animate_tank(scene,start,end,seconds):
    tank,tr,water,base=tank_base(1-np.exp(-start/20))
    flow=tank.flow(1-np.exp(-start/20));dot=tank.dot(1-np.exp(-start/20))
    scene.add(base,flow,dot,tr.path(-10,start,off=1000))
    time=ValueTracker(start)
    water.add_updater(lambda m:m.become(tank.water(1-np.exp(-time.get_value()/20))))
    flow.add_updater(lambda m:m.become(tank.flow(1-np.exp(-time.get_value()/20))))
    dot.add_updater(lambda m:m.become(tank.dot(1-np.exp(-time.get_value()/20))))
    growing=always_redraw(lambda:tr.path(start,time.get_value()+.001,off=1000))
    point=always_redraw(lambda:Dot(tr.p(time.get_value(),float(response(time.get_value(),off=1000))),color=YELLOW,radius=.09))
    scene.add(growing,point)
    scene.play(time.animate.set_value(end),run_time=seconds,rate_func=linear)
    for m in (water,flow,dot,growing,point):m.clear_updaters()
    return tank,tr


class S10Tank(SpokenScene):
    def construct(self):
        tank,tr,water,base=tank_base(0,hose=False,drain_label=False)
        self.add(tr.axes,tr.guide)
        self.at('Picture a')
        self.play(Create(tank.outline),Create(tank.drain),run_time=.6)
        self.at('The water level')
        self.play(FadeIn(water),FadeIn(base[5]),FadeIn(base[6]),run_time=.4)
        self.at("tank's width")
        width=DoubleArrow([-5.5,2.95,0],[-1.9,2.95,0],buff=0,color=GREY)
        self.play(GrowArrow(width),FadeIn(label('width = C',-3.7,3.45,30)),run_time=.4);self.finish()


class S11Tank2(SpokenScene):
    def construct(self):
        tank,tr,water,base=tank_base(0,hose=False,drain_label=False);self.add(base)
        self.at('The drain is')
        self.play(FadeIn(label('leak (g_total)',-4.65,-3.03,26,GREEN)),run_time=.3)
        self.at('outflow grows')
        # Demonstrate the proportional rule without filling the tank before inflow.
        self.play(Indicate(tank.drain,color=GREEN),FadeIn(label('outflow ∝ level',-3.7,.35,28,TEAL)),run_time=.5)
        self.at('The injected current')
        self.play(Create(tank.hose),FadeIn(tank.hose_labels()),run_time=.5)
        self.add(tank.stream());self.finish()


class S12First(SpokenScene):
    def construct(self):
        tank,tr,water,base=tank_base(0);self.add(base,tr.rest)
        note=label('no extra outflow yet',-3.7,-.5,28)
        self.at('nothing extra drains')
        self.play(FadeIn(note),run_time=.3)
        self.at('All the inflow')
        self.remove(*self.mobjects)
        tank,tr=animate_tank(self,0,6,1.6)
        p=tr.p(5,float(response(5,off=1000)))
        b=bracket(tr.p(5,0)+RIGHT*.18,p+RIGHT*.18,YELLOW)
        self.play(Create(b),FadeIn(label('steep start',3.9,.5,28,YELLOW)),run_time=.3);self.finish()


class S13Slope(SpokenScene):
    def construct(self):
        tank,tr,water,base=tank_base(1-np.exp(-6/20))
        self.add(base,tr.path(-10,6,off=1000),tank.dot(1-np.exp(-6/20)))
        self.at('starting slope')
        tangent=curve(lambda t:-.5*t,tr.p,0,18,TEAL)
        self.play(Create(tangent),run_time=.4)
        self.at('current divided by capacitance')
        self.play(FadeIn(label('initial slope = I / C',3.65,3.5,28,TEAL)),
            FadeIn(label('−100 pA / 200 pF',4.25,.65,26,TEAL)),run_time=.25)
        self.play(FadeIn(label('= −0.5 mV per ms',4.25,.15,26,TEAL)),
            Create(Line(tr.p(12,-6),tr.p(12,-6)+RIGHT*.35,color=TEAL,stroke_width=2)),run_time=.2);self.finish()


class S14Rise(SpokenScene):
    def construct(self):
        self.at('As the level rises')
        animate_tank(self,6,75,3.6)
        self.at('so the level')
        self.finish()


class S15Plateau(SpokenScene):
    def construct(self):
        tank,tr,water,base=tank_base(1);self.add(base,tr.path(-10,110,off=1000),tank.flow(1),tank.dot(1))
        self.at('drain carries all')
        self.play(FadeIn(label('outflow = inflow',-3.7,.5,30,TEXT)),run_time=.4)
        self.at('That is the plateau')
        guide=DashedLine(tr.p(-10,-10),tr.p(110,-10),color=GREEN)
        self.play(Create(guide),FadeIn(label('plateau',4.7,tr.p(0,-10)[1]-.35,28,GREEN)),run_time=.4);self.finish()


# A magnified central ruler with off-scale endpoints. Ropes have fixed conductance
# thickness; their lengths change with marker position, never with a fictitious y axis.
def rope(a,b,color,width):
    a,b=np.array(a),np.array(b)
    ts=np.linspace(0,1,220)
    pts=[a+(b-a)*t+UP*.045*np.sin(t*26*TAU) for t in ts]
    return VMobject(stroke_color=color,stroke_width=width).set_points_as_corners(pts)


def ropes(v=REST,ghost=False,pull=True,reminder=False):
    x=lambda vv:-4.4+(vv+86)/20*8.8
    marker=Dot([x(v),.3,0],radius=.14,color=YELLOW)
    ruler=VGroup(Line([-5.9,-1.5,0],[5.9,-1.5,0],color=GREY))
    for vv in (-85,-80,-75,-70):
        xx=x(vv);ruler.add(Line([xx,-1.4,0],[xx,-1.65,0],color=GREY),label(str(vv),xx,-1.95,26,GREY))
    group=VGroup(ruler,label('Vm (mV) • magnified near rest',0,-2.45,28,YELLOW))
    group.add(rope([-5.9,.3,0],marker.get_center(),BLUE,10),rope(marker.get_center(),[5.9,.3,0],ORANGE,2),
        label('K+ rope → EK',-4.35,1.7,28,BLUE),label('Na+ rope → ENa',4.35,1.7,28,ORANGE),
        label('−95 mV (off scale)',-4.35,1.15,26,BLUE),label('+60.6 mV (off scale)',4.35,1.15,26,ORANGE),
        marker,label('marker (Vm now)',x(v),2.65,28,YELLOW),
        Line([x(v),2.35,0],marker.get_center()+UP*.2,color=YELLOW,stroke_width=2))
    if pull:
        group.add(Arrow([x(v),-.75,0],[x(v)-1.4,-.75,0],buff=0,color=TEAL,stroke_width=7),
            label('injected current',x(v)-.7,-1.12,26,TEAL))
    if ghost:
        group.add(Circle(radius=.25,color=GREEN,stroke_width=5).move_to([x(-81.2),.3,0]),
            label('balance point',x(-81.2),-.28,28,GREEN),
            Line([x(-81.2),-.07,0],[x(-81.2),.02,0],color=GREEN,stroke_width=2))
    if reminder:group.add(label('Ropes pull toward each ion’s mark; thickness = conductance.',0,3.45,28))
    return group,marker,x


def leak_tag():
    return label('g_total = 10 nS • ohmic model, fixed leak',0,-2.98,28,GREEN)


class S16Ropes(SpokenScene):
    def construct(self):
        base,_,_=ropes(pull=False,reminder=True);self.add(base)
        self.at('injected current is')
        full,_,_=ropes(reminder=True);self.play(ReplacementTransform(base,full),run_time=.4);self.finish()


class S17Shift(SpokenScene):
    def construct(self):
        base,_,x=ropes();self.add(base)
        self.at('The ropes stretch')
        new,_,_=ropes(ghost=True)
        self.remove(base);self.add(new)
        self.play(Flash([x(-81.2),.3,0],color=GREEN,flash_radius=.45),run_time=.35)
        self.wait(1)
        val=ValueTracker(0)
        moving=always_redraw(lambda:ropes(REST+float(response(val.get_value(),off=1000)),ghost=True)[0])
        self.remove(new);self.add(moving)
        self.play(val.animate.set_value(100),run_time=1.6,rate_func=linear);moving.clear_updaters()
        self.at('balance point shifts')
        moving[1].move_to([0,3.5,0])
        # Keep the original ruler visible; project both displacement endpoints onto it.
        br=VGroup(Line([x(-81.2),-2.95,0],[x(REST),-2.95,0],color=GREEN,stroke_width=4),
            Line([x(-81.2),-3.08,0],[x(-81.2),-2.82,0],color=GREEN),
            Line([x(REST),-3.08,0],[x(REST),-2.82,0],color=GREEN),
            *[DashedLine([x(v),-1.5,0],[x(v),-2.25,0],color=GREEN,stroke_width=1.5)
              for v in (-81.2,REST)],
            label('−81.2',x(-81.2),-2.55,24,GREEN),label('−71.2',x(REST),-2.55,24,YELLOW))
        # The numeric conductance arrives with the cell example in s19.
        self.play(FadeIn(br),run_time=.3)
        self.at('current divided by')
        self.play(FadeIn(label('shift = I / g_total',0,-3.55,30,GREEN)),run_time=.3);self.finish()


class S18Rin(SpokenScene):
    def construct(self):
        rr,_,_=ropes(-81.2,ghost=True);self.add(rr)
        self.at('input resistance')
        self.play(FadeIn(label('input resistance',0,-2.98,32)),run_time=.3)
        self.at('It is')
        self.play(FadeIn(label('Rin = ΔV / I = 1 / g_total',0,-3.55,34,GREEN)),run_time=.3);self.finish()


class S19RinCell(SpokenScene):
    def construct(self):
        rr,_,_=ropes(-81.2,ghost=True);self.add(rr)
        self.at('For our cell')
        self.play(FadeIn(leak_tag(),shift=RIGHT*.5),run_time=.35)
        self.at('that is')
        self.play(FadeIn(label('1 / 10 nS = 100 MΩ',0,-3.55,38,GREEN)),run_time=.3);self.finish()


class S20Follow(SpokenScene):
    def construct(self):
        rr,_,x=ropes();self.add(rr,leak_tag())
        self.at('balance point moves')
        target,_,_=ropes(ghost=True);self.remove(rr);self.add(target)
        self.play(Flash([x(-81.2),.3,0],color=GREEN,flash_radius=.4),run_time=.3)
        self.at('voltage follows it')
        val=ValueTracker(0);moving=always_redraw(lambda:ropes(REST+float(response(val.get_value(),off=1000)),ghost=True)[0])
        self.remove(target);self.add(moving)
        self.play(val.animate.set_value(90),run_time=2.5,rate_func=linear);moving.clear_updaters();self.finish()


class S21Tau(SpokenScene):
    def construct(self):
        tr=Trace(final=True);main=tr.path(-10,110,off=1000)
        self.add(tr.axes,tr.guide,main)
        self.at('time constant')
        self.play(FadeIn(label('τ = Rin × C = C / g_total',.5,3.15,38,GREEN)),run_time=.3)
        self.at('It equals capacitance')
        slower=tr.path(-10,110,off=1000,cap=400,color=ORANGE)
        caplab=label('larger C: slower',2.8,.7,28,ORANGE)
        self.play(Create(slower),FadeIn(caplab),ShowPassingFlash(main.copy().set_stroke(TEAL,8),time_width=.5),run_time=.8)
        self.at('divided by total leak')
        fast=tr.path(-10,110,g=20,off=1000,color=GREEN)
        self.play(FadeOut(slower),FadeOut(caplab),Create(fast),FadeIn(label('τ = C / g_total',2.7,-.8,28,GREEN)),run_time=.8);self.finish()


def tau_flag(tr,n):
    t=20*n;p=tr.p(t,float(response(t,off=1000)))
    # Labels above rest, so the dotted guides never run through their type.
    return VGroup(DashedLine(tr.p(t,0),p,color=GREEN,stroke_width=2),Dot(p,color=GREEN,radius=.09),
        label(f'{n}τ: {100*(1-np.exp(-n)):.0f}%',p[0],tr.top+.8,28,GREEN))


class S22Pct(SpokenScene):
    def construct(self):
        tr=Trace(final=True);self.add(tr.axes,tr.path(-10,110,off=1000),tr.guide,label('final',5.1,tr.p(0,-10)[1]-.35,26,GREEN))
        self.at('In one time constant')
        self.play(Create(tau_flag(tr,1)),run_time=.4)
        self.at('voltage gets about')
        self.play(Create(bracket(tr.p(20,0)+LEFT*.18,tr.p(20,float(response(20,off=1000)))+LEFT*.18)),run_time=.4)
        self.at('Not all of it')
        self.play(FadeIn(tau_flag(tr,2)),run_time=.35)
        self.play(FadeIn(tau_flag(tr,3)),run_time=.35);self.finish()


class S23TauCell(SpokenScene):
    def construct(self):
        tr=Trace(final=True);self.add(tr.axes,tr.path(-10,110,off=1000),tr.guide)
        self.at('For our cell')
        self.play(FadeIn(label('200 pF / 10 nS = 20 ms',-.9,3.25,34,GREEN)),run_time=.25)
        self.at('the time constant')
        p=tr.p(20,float(response(20,off=1000)))
        b=bracket(tr.p(20,0)+RIGHT*.35,p+RIGHT*.35)
        self.play(Create(b),FadeIn(Dot(p,color=GREEN,radius=.09)),Create(DashedLine([tr.x0,p[1],0],p,color=GREEN)),
            FadeIn(label('−77.52',tr.x0-.7,p[1],26,GREEN)),
            FadeIn(label('ΔV = −6.32 mV',p[0]+2.3,(p[1]+tr.top)/2,30,GREEN)),
            FadeIn(label('63% of the final −10 mV change',-.4,2.55,28,GREEN)),
            Create(DashedLine(p,tr.p(20,-12),color=GREEN)),
            FadeIn(label('20 ms',p[0],tr.bottom-.72,28,GREEN)),run_time=.35);self.finish()


class S24MoreLeak(SpokenScene):
    def construct(self):
        # Hold the completed comparison for an extra 1.2 s; narration is unchanged.
        tr=Trace(small=True,absolute=False,final=True,tall=True)
        a=Tank(-4.75,2.1,12);b=Tank(-1.9,2.1,24)
        self.add(tr.axes,a.outline,a.drain,a.hose,a.water(1),a.flow(1),b.outline,b.drain,b.hose,b.water(0),
            label('this cell',-4.75,-3.5,28,YELLOW),label('more leak',-1.9,-3.5,28,GREEN),
            label('same I, same C',-3.2,3.65,26),tr.path(-10,110,off=1000),
            DashedLine(tr.p(-10,-5),tr.p(110,-5),color=GREEN),label('−5',tr.x0-.65,tr.p(0,-5)[1],26,GREEN))
        self.at('More leak means')
        time=ValueTracker(0);water=b.water(0);flow=b.flow(0)
        water.add_updater(lambda m:m.become(b.water(.5*(1-np.exp(-time.get_value()/10)))))
        flow.add_updater(lambda m:m.become(b.flow(1-np.exp(-time.get_value()/10))))
        trace=always_redraw(lambda:tr.path(0,time.get_value()+.001,g=20,off=1000,color=GREEN))
        self.add(water,flow,trace)
        self.play(time.animate.set_value(65),run_time=1.65,rate_func=linear)
        for m in (water,flow,trace):m.clear_updaters()
        self.at('reached sooner')
        self.play(FadeIn(label('smaller, faster',3.9,3.5,30,GREEN)),run_time=.25)
        self.wait(2.8);self.finish()


# Exact finite square-pulse RC solutions, normalized to equal isolated peaks.
# This comparison varies C at fixed leak; the input scale changes to keep peak fixed.
def pulse(t,on,tau):
    dur=10.;u=np.asarray(t)-on
    return np.where(u<0,0,np.where(u<=dur,(1-np.exp(-np.maximum(u,0)/tau))/(1-np.exp(-dur/tau)),np.exp(-(u-dur)/tau)))


def sum_point(t,v):return np.array([-4.9+t/80*10.7,-2.65+v*2.6,0])


def summation(tau=20):
    p=sum_point
    axes=VGroup(Line(p(0,0),p(80,0),color=GREY),Line(p(0,0),p(0,1.7),color=GREY),
        label('voltage change (ΔV)',-2.6,1.55,30,YELLOW),label('time',5.5,-3.25,28,GREY),label('0',-5.4,-2.65,28,GREY),
        label('input',-5.8,2.95,28,TEAL),Line([-4.9,2.55,0],[5.8,2.55,0],color=GREY,stroke_opacity=.5))
    one=curve(lambda t:pulse(t,5,tau),p,0,80,GREY,3)
    two=curve(lambda t:pulse(t,25,tau),p,0,80,GREY,3)
    total=curve(lambda t:pulse(t,5,tau)+pulse(t,25,tau),p,0,80,YELLOW,5)
    inp=VMobject(stroke_color=TEAL,stroke_width=4).set_points_as_corners([[-4.9+t/80*10.7,2.55+.6*i,0] for t,i in [(0,0),(5,0),(5,1),(15,1),(15,0),(25,0),(25,1),(35,1),(35,0),(80,0)]])
    return axes,one,two,total,inp


def sum_labels():
    return VGroup(label('each input alone',3.8,.65,28,GREY),label('sum',3.8,.05,30,YELLOW))


class S25Linger(SpokenScene):
    def construct(self):
        axes,one,two,total,inp=summation();self.add(axes,inp)
        self.at('A change also lingers')
        self.play(Create(one),FadeIn(sum_labels()[0]),run_time=1.2,rate_func=linear)
        self.at('inputs close together')
        self.play(Create(two),run_time=.7,rate_func=linear)
        self.at('overlap and add')
        p=sum_point(35,1);q=sum_point(35,1+float(pulse(35,5,20)))
        self.play(Create(total),FadeIn(sum_labels()[1]),Create(bracket(p+RIGHT*.25,q+RIGHT*.25,YELLOW)),
            FadeIn(label('extra height',1,1.3,28,YELLOW)),run_time=.7);self.finish()


class S26Summation(SpokenScene):
    def construct(self):
        axes,one,two,total,inp=summation();legend=sum_labels();self.add(axes,one,two,total,inp,legend)
        self.at('temporal summation')
        title=label('temporal summation',1,3.65,30)
        self.play(FadeIn(title),run_time=.3)
        self.at('A longer time constant')
        ghost=total.copy().set_stroke(GREY,3,.7);self.add(ghost)
        _,o2,t2,s2,_=summation(40)
        self.play(Transform(one,o2),Transform(two,t2),Transform(total,s2),run_time=.9)
        self.at('window for overlap')
        xx=sum_point(25,0)[0]
        short=sum_point(25,float(pulse(25,5,20)))
        long=sum_point(25,float(pulse(25,5,40)))
        self.remove(legend)
        # Direct residual labels stay to the left of the second-input line.
        longlab=label('long τ:\nmore left',xx-.95,-1.42,22,GREEN)
        shortlab=label('short τ:\nless left',xx-.95,-2.15,22,TEXT)
        self.play(Create(DashedLine([xx,1.2,0],[xx,-2.65,0],color=GREEN)),
            FadeIn(Dot(short,color=GREY,radius=.09)),FadeIn(Dot(long,color=GREEN,radius=.09)),
            Create(Line(short+LEFT*.05,[xx-.3,-1.85,0],color=GREY,stroke_width=2)),
            Create(Line(long+LEFT*.05,[xx-.3,-1.15,0],color=GREEN,stroke_width=2)),
            FadeIn(shortlab),FadeIn(longlab),
            FadeIn(label('sum • longer τ',4.25,.1,28,YELLOW)),
            FadeIn(label('short τ (before)',4.05,-2.38,24,TEXT)),
            Create(Line(sum_point(60,float(pulse(60,5,20)+pulse(60,25,20))),
                        sum_point(60,float(pulse(60,5,20)+pulse(60,25,20)))+DOWN*.35,color=GREY)),
            FadeIn(label('small steps, fixed leak • same isolated peak',0,-3.555,26,GREEN)),run_time=.4);self.finish()


class S27Takeaway(SpokenScene):
    def construct(self):
        panels=VGroup(*[RoundedRectangle(width=5.8,height=5.9,corner_radius=.2,color=GREY).move_to([x,-.15,0]) for x in (-3.15,3.15)])
        self.add(panels,label('total leak',0,3.35,38))
        self.at('The total leak')
        # Both diagrams establish what the two panels will explain from the first frame.
        leftp=lambda t,dv:np.array([-5.6+t/65*4.8,.25+dv*.18,0])
        rightp=lambda t,dv:np.array([.7+t/65*4.8,.25+dv*.18,0])
        a=curve(lambda t:response(t,off=1000),leftp,0,65)
        b=curve(lambda t:response(t,off=1000),rightp,0,65)
        self.add(a,b,DashedLine(leftp(0,-10),leftp(65,-10),color=GREEN),
            bracket(rightp(20,0),rightp(20,float(response(20,off=1000)))))
        self.at('how big a nudge')
        self.play(FadeIn(label('how big',-3.15,2.15,38,YELLOW)),FadeIn(label('Rin = 1 / g_total',-3.15,1.2,30,GREEN)),
            FadeIn(label('plateau level',-3.15,-2.35,30,GREEN)),run_time=.3)
        self.at('how fast the voltage')
        self.play(FadeIn(label('how fast',3.15,2.15,38,YELLOW)),FadeIn(label('τ = C / g_total',3.15,1.2,30,GREEN)),
            FadeIn(label('63% at one τ',3.15,-2.35,30,GREEN)),run_time=.3);self.finish()


class S28End(EndCard):
    LINE='Total leak sets nudge size and how fast the voltage responds.'
    def construct(self):
        self.add(label('Total leak sets nudge size',0,1,40,YELLOW),
            label('and how fast the voltage responds.',0,-.2,40,YELLOW),
            label('biochemistrypedia.com',0,-1.8,28,TEAL))
        self.finish()
