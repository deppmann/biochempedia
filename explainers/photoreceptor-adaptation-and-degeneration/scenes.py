"""Chapter 1, revision after the complete frame review.
COLOR MAP: YELLOW light; ORANGE calcium; PURPLE GCAPs/recoverin; TEAL channels/PDE;
GREEN cGMP/adaptation; PINK pigment; BLUE control/current; RED removed/spent;
GREY outlines. No molecular geometry. Traces use the reference impulse equation;
illustrative amplitudes and time constants are not fitted kinetic measurements.
Sensitivity curves are the lesson's mouse CONE fits, not rod knockout data.
"""
import numpy as np
from bp_style import *
ORANGE = '#F29E4C'
PURPLE = '#B58CD9'
PINK = '#E58FB0'
CTRL = dict(I0=48800, n=1.)
KO = dict(I0=12100, n=1.5)
LESSON = 'Calcium Feedback Sets Photoreceptor Gain, and When Photoreceptors Die'


def label(s, x=0, y=3.05, size=32, color=TEXT):
    return T(s, max(28,size), color, line_spacing=1.15).move_to([x,y,0])


def arrow(a,b,color=YELLOW):
    return Arrow(a,b,buff=.08,color=color,stroke_width=6,max_tip_length_to_length_ratio=.16)


def rod_cell(color=BLUE, s=1.):
    outer=RoundedRectangle(width=.75,height=1.7,corner_radius=.15,color=color,fill_opacity=.15).move_to([0,.85,0])
    body=RoundedRectangle(width=1.1,height=1.1,corner_radius=.4,color=color,fill_opacity=.15).move_to([0,-.55,0])
    return VGroup(outer,body,Line([0,-1.1,0],[0,-1.6,0],color=color)).scale(s)


def cone_cell(s=1.):
    outer=Polygon([-.55,0,0],[.55,0,0],[.18,1.7,0],[-.18,1.7,0],color=BLUE,fill_opacity=.15)
    body=RoundedRectangle(width=1.1,height=1.1,corner_radius=.4,color=BLUE,fill_opacity=.15).move_to([0,-.55,0])
    return VGroup(outer,body,Line([0,-1.1,0],[0,-1.6,0],color=BLUE)).scale(s)


def response(left,bottom,width,height,tau,color=BLUE,clip=None):
    ts=np.linspace(0,8,320)
    vals=height*(ts/tau)*np.exp(1-ts/tau)
    if clip is not None:
        vals=np.minimum(vals,clip) if height >= 0 else np.maximum(vals,clip)
    return VMobject(color=color,stroke_width=5).set_points_as_corners([[left+width*t/8,bottom+v,0] for t,v in zip(ts,vals)])


def logS(x,I0,n):
    return -np.log10(1+10**(n*(x-np.log10(I0))))


def gauge(frac=.7,x=3.9,y=0,h=4.9,w=1.35,spent=False):
    box=RoundedRectangle(width=w,height=h,corner_radius=.12,color=GREY).move_to([x,y,0])
    fill=Rectangle(width=w-.12,height=max(.02,(h-.12)*frac),stroke_width=0,fill_color=BLUE,fill_opacity=.85)
    fill.move_to([x,y-h/2+.06+fill.height/2,0])
    g=VGroup(box,fill)
    if spent:
        top=Rectangle(width=w-.12,height=max(.02,(h-.12)*(1-frac)),stroke_width=0,fill_color=RED,fill_opacity=.25)
        top.move_to([x,y+h/2-.06-top.height/2,0]); g.add(top)
    return g


def segment(open_count=3):
    body=RoundedRectangle(width=6.9,height=4.9,corner_radius=.55,color=GREY,fill_opacity=.05).move_to([-2,-.1,0])
    chans=VGroup(); dots=VGroup(); flow=VGroup()
    for i,x in enumerate([-4.25,-2,.25]):
        gap=.22 if i<open_count else 0
        chans.add(VGroup(*[Rectangle(width=.55,height=.85,color=TEAL,fill_color=TEAL,fill_opacity=.85).move_to([x+sign*(.275+gap),2.25,0]) for sign in [-1,1]]))
        if i<open_count:
            dots.add(Dot([x,1.4,0],radius=.16,color=GREEN))
            flow.add(arrow([x,.9,0],[x,-1.1,0],BLUE))
    return VGroup(body,chans,dots,flow)


def dark_frame(n=3,f=1):
    return VGroup(segment(n),gauge(f,x=2.7),label('outer segment',-2,-2.95,30,GREY),label('current still flowing',2.7,-2.95,28,BLUE))


def scale_frame():
    axis=NumberLine(x_range=[0,8,1],length=11.2,include_numbers=False,color=GREY).move_to([0,1.1,0])
    ends=VGroup(Star(n=5,outer_radius=.3,color=YELLOW,fill_opacity=1).move_to([-5.5,2.3,0]),Circle(radius=.35,color=YELLOW,fill_opacity=1).move_to([5.5,2.3,0]),label('starlight',-3.9,2.3),label('sunlight',3.9,2.3))
    ticks=VGroup(*[label('10'+str(i).translate(str.maketrans('0123456789','⁰¹²³⁴⁵⁶⁷⁸⁹')),-5.6+1.4*i,.5,28,GREY) for i in [0,2,4,6,8]])
    return VGroup(axis,ends,ticks,label('background light',0,-.25,30,YELLOW))


def prediction_channels(opened=True):
    gap=.18 if opened else 0
    return VGroup(*[Rectangle(width=.25,height=.5,color=TEAL,fill_color=TEAL,fill_opacity=.8).move_to([-3.6+sign*(.125+gap),.75,0]) for sign in [-1,1]])


def predict_frame():
    cell=rod_cell(s=1.6).move_to([-3.6,-.15,0]); cell.add(prediction_channels())
    lock=VGroup(RoundedRectangle(width=1.05,height=.75,corner_radius=.12,color=GREY),Arc(radius=.33,start_angle=0,angle=PI,color=GREY).shift(UP*.38)).move_to([-.75,1.1,0])
    return VGroup(cell,lock,label('fixed gain',-.75,.15),label('steady background',-3.3,3.1,30,YELLOW),arrow([-3.6,2.75,0],[-3.6,1.55,0]),label('What happens to the current?',1,-3,34),gauge(1,x=2.25),label('current\nstill flowing',4.7,0,30,BLUE))


def split_frame(reserve=.02,lowered=True):
    div=Line([0,-2.8,0],[0,2.65,0],color=GREY,stroke_opacity=.35)
    left=VGroup(rod_cell(s=1.1).move_to([-4.8,.15,0]),gauge(.02,-2,y=.15,h=3.7,w=1),label('fixed gain',-3.5,3.1),Line([-5.7,-2.1,0],[-.8,-2.1,0],color=BLUE))
    dial=VGroup(Arc(radius=.5,start_angle=0,angle=PI,color=GREEN).move_to([3.2,1.1,0]),Line([3.2,.85,0],[3.62,1.2,0],color=GREEN,stroke_width=5),label('gain',3.2,.35,28,GREEN))
    if lowered: dial[1].rotate(1.4,about_point=[3.2,.85,0])
    right=VGroup(rod_cell(s=1.1).move_to([1.45,.15,0]),gauge(reserve,5,y=.15,h=3.7,w=1),label('calcium feedback',3.4,3.1,30,ORANGE),dial)
    return VGroup(div,left,right,label('steady light on both cells',0,-3.05,30,YELLOW))


def reserve_label():
    return VGroup(label('current\nin reserve',3.45,-.9,28,BLUE),Line([4.25,-.9,0],[4.5,-.9,0],color=BLUE))


def plot_frame():
    # Coordinates explicitly place the horizontal axis at the BOTTOM, not log(S)=0.
    ax=Axes(x_range=[2,6,1],y_range=[-3,0,1],x_length=10.2,y_length=4.55,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([.45,.05,0])
    ax.x_axis.set_opacity(0)
    bottom=Line(ax.c2p(2,-3),ax.c2p(6,-3),color=GREY)
    ticks=VGroup()
    for i in range(2,7):
        p=ax.c2p(i,-3); ticks.add(Line(p,p+DOWN*.1,color=GREY),T('10'+str(i).translate(str.maketrans('0123456789','⁰¹²³⁴⁵⁶⁷⁸⁹')),28,GREY).next_to(p,DOWN,buff=.15))
    for y,s in [(0,'1'),(-1,'0.1'),(-2,'0.01'),(-3,'0.001')]:
        ticks.add(T(s,28,GREY).next_to(ax.c2p(2,y),LEFT,buff=.18))
    labs=VGroup(T('S/S_dark',30).rotate(PI/2).move_to([-6.25,0,0]),label('background light (photons/µm²/s)',.6,-3.05,28,GREY))
    return ax,VGroup(ax,bottom,ticks,labs)


def curve(ax,p,col=BLUE):
    # Stop at the plot floor instead of drawing outside the axes.
    xs=np.linspace(2,6,401); pts=[[ *ax.c2p(x,logS(x,**p)) ] for x in xs if logS(x,**p)>=-3]
    return VMobject(color=col,stroke_width=5).set_points_as_corners(pts)


class S00Title(TitleCard):
    TITLE='A Current That Light Can Use Up'
    LESSON=LESSON
    def construct(self):
        g=VGroup(label('BIOCHEMISTRYPEDIA',size=30,color=TEAL),T('Chapter 1 of 3',32,color=GREY),VGroup(T('A Current That Light',49,font=TITLE_FONT),T('Can Use Up',49,font=TITLE_FONT)).arrange(DOWN,buff=.35),Line(LEFT,RIGHT,color=GOLD)).arrange(DOWN,buff=.5)
        self.play(FadeIn(g),run_time=.6); self.finish()


class S01Q(SpokenScene):
    def construct(self):
        self.add(label('A Current That Light Can Use Up',y=3.1,size=32))
        night=VGroup(Rectangle(width=5.2,height=3.3,color=BLUE,fill_opacity=.12).move_to([-3,0,0]),*[Star(n=5,outer_radius=.12,color=YELLOW,fill_opacity=1).move_to([x,y,0]) for x,y in [(-4.6,.9),(-3.2,.3),(-1.4,1),(-4,-.7)]])
        day=VGroup(Rectangle(width=5.2,height=3.3,color=YELLOW,fill_opacity=.12).move_to([3,0,0]),Circle(radius=.55,color=YELLOW,fill_opacity=1).move_to([4,.7,0]),Rectangle(width=5.2,height=.65,color=GREEN,fill_opacity=.6).move_to([3,-1.3,0]))
        self.at('Your eyes work'); self.play(FadeIn(night),run_time=.5)
        self.at('bright sun'); self.play(FadeIn(day),run_time=.4)
        self.at('How can'); self.play(FadeIn(label('How can one cell cope with both?',y=-2.6,size=32)),run_time=.4); self.finish()


class S02Range(SpokenScene):
    def construct(self):
        f=scale_frame(); self.add(f)
        self.at('the light changes'); self.play(Indicate(f[0],color=YELLOW,scale_factor=1.03),run_time=.6)
        self.at('or more'); self.play(FadeIn(label('A hundred-million-fold or more · 10⁸',y=-2,size=34,color=YELLOW)),run_time=.3); self.finish()


class S03Rod(SpokenScene):
    def construct(self):
        self.add(label('Dark-adapted rod',y=3.1,size=36,color=BLUE),label('flash strength · a separate scale',y=2.5,size=30,color=YELLOW))
        axis=NumberLine(x_range=[0,2,1],length=9.4,include_numbers=False,color=GREY).move_to([0,1.35,0])
        self.add(axis,*[label(s,x,.85,28,GREY) for x,s in [(-4.7,'1×'),(0,'10×'),(4.7,'100×')]])
        br=BraceBetweenPoints([-4.7,1.7,0],[4.7,1.7,0],direction=UP,color=BLUE)
        self.at('rod goes'); self.play(GrowFromCenter(br),run_time=.35)
        for x,s in [(-4.6,'weak'),(0,'medium'),(4.6,'strong')]: self.add(label(s,x,.05,30,YELLOW),arrow([x,.55,0],[x,.3,0]))
        self.add(*[Line([x-.0,-.65,0],[x+3,-.65,0],color=GREY,stroke_opacity=.5) for x in [-6,-1.5,3]])
        self.at('barely responding'); self.play(Create(response(-6,-.65,3,-.35,.9)),run_time=.45)
        self.at('to saturated'); self.play(Create(response(-1.5,-.65,3,-1.25,.9)),Create(response(3,-.65,3,-3.5,.9,clip=-1.95)),FadeIn(label('saturated',4.6,-2.95,28,BLUE)),run_time=.6)
        self.at('range of flashes'); self.play(FadeIn(label('Two decades · roughly a hundredfold',y=-3.6,size=30)),run_time=.3); self.finish()


class S05Dark(SpokenScene):
    def construct(self):
        f=dark_frame(); self.add(f[0][0],f[2])
        self.at('In darkness'); self.play(FadeIn(f[0][1]),run_time=.4)
        self.at('holds channels open'); self.play(FadeIn(f[0][2]),FadeIn(label('cGMP',-2,3.15,32,GREEN)),run_time=.4)
        self.at('A steady dark current'); self.play(LaggedStart(*[GrowArrow(a) for a in f[0][3]],lag_ratio=.1),FadeIn(f[1]),FadeIn(f[3]),FadeIn(label('dark current',-2,-1.6,32,BLUE)),run_time=.65); self.finish()


class S06Light(SpokenScene):
    def construct(self):
        f=dark_frame(); cg=label('cGMP',-2,3.15,32,GREEN); self.add(f,cg,label('dark current',-2,-1.6,32,BLUE))
        p=chip('PDE',TEAL,size=30).move_to([-1.05,.35,0]); light=arrow([-5.8,3.25,0],[-4.25,2.45,0])
        self.at('Light activates'); self.play(GrowArrow(light),FadeIn(label('flash',-5.55,3.65,30,YELLOW)),FadeOut(cg),FadeIn(p),run_time=.5)
        self.at('breaks down'); self.play(*[ShrinkToCenter(d) for d in list(f[0][2])[1:]],GrowArrow(arrow([-1.4,.7,0],[-1.95,1.3,0],TEAL)),GrowArrow(arrow([-.45,.7,0],[.2,1.3,0],TEAL)),run_time=.55)
        self.at('and channels close'); self.play(Transform(f[0],segment(1)),Transform(f[1],gauge(.35,x=2.7)),run_time=.65)
        self.at('Each response switches off'); self.play(Indicate(f[1],scale_factor=1.03),run_time=.55); self.finish()


class S07Spend(SpokenScene):
    def construct(self):
        g=gauge(.7,x=0,w=2.3,h=5.8,spent=True); self.add(g,label('current still flowing',y=3.25,size=34,color=BLUE))
        self.at('light spends'); self.play(Transform(g,gauge(.35,x=0,w=2.3,h=5.8,spent=True)),GrowArrow(arrow([-4,1.5,0],[-1.2,1.5,0])),FadeIn(label('light',-3.2,2.1,32,YELLOW)),FadeIn(label('spent',2.7,1.4,34,RED)),run_time=.6)
        self.at('What is still flowing'); self.play(FadeIn(label('room for\nnext response',3.8,-1.9,32,BLUE)),Create(Line([1.2,-1.9,0],[2.1,-1.9,0],color=BLUE)),run_time=.4); self.finish()


class S08Gain(SpokenScene):
    def construct(self):
        tr=response(-5.4,.6,9.8,-2,.9)
        card=label('Gain = current one photon switches off,\nand for how long',0,2.75,34,GREEN)
        self.add(Line([-5.7,.6,0],[5.7,.6,0],color=GREY),tr,label('current (relative)',-3.7,1.25,28,BLUE),label('time →',4.7,-2.7,28,GREY))
        self.at('gain is'); self.play(FadeIn(card),run_time=.35)
        self.at('absorbed photon'); self.play(GrowArrow(arrow([-5.4,2,0],[-5.4,.75,0])),run_time=.3)
        self.at('switches off'); self.play(Create(Line([5.4,.6,0],[5.4,-1.4,0],color=TEXT)),Create(Line([5.2,.6,0],[5.6,.6,0])),Create(Line([5.2,-1.4,0],[5.6,-1.4,0])),FadeIn(label('how much\ncurrent',3.6,-.4,30)),Create(DashedLine([-4.3,-1.4,0],[5.2,-1.4,0],color=GREY,stroke_opacity=.5)),run_time=.4)
        self.at('for how long'); self.play(GrowFromCenter(BraceBetweenPoints([-5.4,-1.85,0],[.7,-1.85,0],direction=DOWN)),FadeIn(label('for how long',-2.35,-2.65,30)),run_time=.4); self.finish()


class S09Sens(SpokenScene):
    def construct(self):
        self.add(label('Sensitivity',y=3.1,size=40,color=GREEN),response(-5.4,1.3,10.8,-1.3,.7))
        self.at('response to a dim flash'); self.play(FadeIn(label('response to a dim flash',y=-.65,size=34,color=BLUE)),run_time=.4)
        self.at('divided by'); self.play(Create(Line([-4,-1.4,0],[4,-1.4,0],color=TEXT)),run_time=.3)
        self.at('the strength'); self.play(FadeIn(label('flash strength',y=-2.25,size=34,color=YELLOW)),run_time=.4); self.finish()


class S10Predict(SpokenScene):
    def construct(self):
        f=predict_frame(); self.add(f[0],f[6],f[7])
        self.at('gain never changed'); self.play(FadeIn(f[1]),FadeIn(f[2]),run_time=.4)
        self.at('a modest'); self.play(FadeIn(f[3]),GrowArrow(f[4]),run_time=.5)
        self.at('do to it'); self.play(FadeIn(f[5]),run_time=.3); self.finish()


class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(predict_frame()); self.wait(5)


class S12Reveal(SpokenScene):
    def construct(self):
        f=predict_frame(); self.add(f[0],f[1],f[2],f[3],f[4],f[6],f[7])
        sat=label('saturated for increments',.8,-3.05,34,RED)
        self.at('close nearly every'); self.play(Transform(f[6],gauge(.02,x=1.1)),Transform(f[7],label('current',1.1,2.85,30,BLUE)),Transform(f[0][3],prediction_channels(False)),FadeIn(sat),run_time=.65)
        test=VGroup(arrow([-.4,2.8,0],[-2.8,1.6,0]),label('brighter test flash',3.9,3.1,30,YELLOW))
        flat=VGroup(Line([-2.65,-1.65,0],[.2,-1.65,0],color=BLUE,stroke_width=6),label('no response to\nbrighter flash',-1.2,-2.35,28,BLUE))
        self.at('unable to signal'); self.add(f[4]); self.play(FadeIn(test),FadeIn(flat),run_time=.45)
        self.at('further brightening'); self.play(Indicate(flat[0],scale_factor=1.02),run_time=.3)
        self.at('Only dimming'); self.play(FadeOut(test),FadeOut(flat),FadeOut(sat),FadeOut(f[3]),f[4].animate.set_opacity(.15),Transform(f[6],gauge(.3,x=1.1)),Transform(f[0][3],prediction_channels()),FadeIn(label('light dims · channels reopen',0,-3.05,32,GREEN)),run_time=.65); self.finish()


class S14Turn(SpokenScene):
    def construct(self):
        f=split_frame(lowered=False); self.add(f)
        self.at('turns its own gain down'); self.play(Rotate(f[2][3][1],angle=1.4,about_point=[3.2,.85,0]),run_time=.8)
        self.at('background brightens'); self.play(Indicate(f[3],scale_factor=1.03),run_time=.35); self.finish()


class S15Reserve(SpokenScene):
    def construct(self):
        f=split_frame(); self.add(f)
        self.at('Calcium feedback'); self.play(Indicate(f[2][2],scale_factor=1.03),run_time=.35)
        self.at('While the light stays on'); self.play(Indicate(f[3],scale_factor=1.03),run_time=.3)
        c=VGroup(*[Rectangle(width=.22,height=.45,color=TEAL,fill_opacity=.8).move_to([1.45+sign*.11,1.4,0]) for sign in [-1,1]])
        self.at('reopens some channels'); self.add(c); self.play(c[0].animate.shift(LEFT*.18),c[1].animate.shift(RIGHT*.18),Transform(f[2][1],gauge(.55,5,y=.15,h=3.7,w=1)),FadeIn(reserve_label()),run_time=.6); self.finish()


class S16Trim(SpokenScene):
    def construct(self):
        f=split_frame(.55)
        for panel in [f[1],f[2]]: panel.scale(.75,about_point=[0,2.65,0])
        f[3].move_to([0,-3.5,0])
        reserve=label('current in reserve',3.1,-.8,28,BLUE)
        self.add(f,reserve)
        old=response(.65,-1.25,4.7,-1.15,1.4,GREY).set_stroke(opacity=.55)
        tr=old.copy().set_color(BLUE).set_stroke(opacity=1); self.add(old,tr)
        self.at('cuts and shortens'); self.play(Transform(tr,response(.65,-1.25,4.7,-.35,.35)),FadeIn(label('lower gain · shorter',3,-2.95,28,GREEN)),run_time=.8)
        self.at('Each photon does less'); self.play(Indicate(tr,scale_factor=1.02),run_time=.3); self.finish()


class S17Weber(SpokenScene):
    def construct(self):
        ax,b=plot_frame(); self.add(b,label('Weber behaviour · control cones, fit',y=3.3,size=32,color=BLUE))
        self.at('The result is called'); self.play(Create(curve(ax,CTRL)),run_time=.65)
        knee=np.log10(CTRL['I0']); p=ax.c2p(knee,np.log10(.5))
        kl=label('I₀ · half sensitivity',-.8,1.35,28,BLUE)
        ref=DashedLine(p,ax.c2p(6,np.log10(.5)-(6-knee)),color=YELLOW)
        rl=label('sensitivity ∝ 1/background',.3,-.55,28,YELLOW)
        self.at('On brighter backgrounds'); self.play(FadeIn(Dot(p,radius=.085,color=BLUE)),Create(DashedLine(p,ax.c2p(knee,-3),color=BLUE,stroke_opacity=.4)),FadeIn(kl),Create(Line(kl.get_right()+RIGHT*.12,p,color=BLUE)),run_time=.4)
        self.play(Create(ref),FadeIn(rl),Create(Line(rl.get_right()+RIGHT*.12,ax.c2p(5.7,np.log10(.5)-(5.7-knee)),color=YELLOW)),FadeIn(label('slope −1: 10× brighter → 10× less sensitive',0,-1.45,28,YELLOW)),run_time=.45)
        self.at('one over the background'); self.play(Indicate(ref,scale_factor=1.02),run_time=.3); self.finish()


class S18Contrast(SpokenScene):
    def construct(self):
        self.add(label('Contrast',y=3.15,size=40,color=YELLOW),label('Contrast = change in light / background',y=-2.5,size=34))
        pulse=VMobject(color=YELLOW,stroke_width=6).set_points_as_corners([[-5.5,.2,0],[-1,.2,0],[-1,1.7,0],[1,1.7,0],[1,.2,0],[5.5,.2,0]])
        self.add(pulse,label('background',-3.5,-.4,30,YELLOW),label('change in light',3.4,1.4,30,YELLOW),Line([1.4,.2,0],[1.4,1.7,0],color=TEXT),Line([1.2,.2,0],[1.6,.2,0]),Line([1.2,1.7,0],[1.6,1.7,0]))
        self.at('a change in light'); self.play(Indicate(pulse,scale_factor=1.02),run_time=.4)
        self.at('as a fraction'); self.play(Indicate(self.mobjects[1],scale_factor=1.02),run_time=.4); self.finish()


class S19Payoff(SpokenScene):
    def construct(self):
        self.add(label('Equal contrast · equal duration',y=3.25,size=34))
        xs=[-4.25,0,4.25]; ratios=[10,100,1000]
        cards=VGroup(*[VGroup(label(str(r)+' × I₀',x,2.5,30,YELLOW),Rectangle(width=3.6,height=1.6,color=YELLOW,fill_opacity=.07).move_to([x,1.25,0])) for x,r in zip(xs,ratios)])
        self.add(cards,label('idealised: fit extended beyond the data',y=-3.55,size=28,color=GREY))
        eq=label('n = 1 ideal · S/S_dark = 1/(1 + I/I₀)',y=-.3,size=30,color=BLUE); self.add(eq)
        self.at('On bright backgrounds'); self.play(Indicate(cards,scale_factor=1.01),run_time=.35)
        pulses=VGroup(*[VMobject(color=YELLOW,stroke_width=5).set_points_as_corners([[x-1.55,.8,0],[x-.45,.8,0],[x-.45,1.25,0],[x+.45,1.25,0],[x+.45,.8,0],[x+1.55,.8,0]]) for x in xs])
        self.at('small brief flashes'); self.play(Create(pulses),run_time=.5)
        self.at('the same contrast'); self.play(FadeOut(eq),run_time=.12); eq=label('C = 10% · same duration T · I ≫ I₀',y=-.3,size=30,color=YELLOW); self.play(FadeIn(eq),run_time=.28)
        # Dot counts are a schematic visual tally, not a linear count of photons.
        dots=VGroup(*[VGroup(*[Dot([x-1.4+(j%20)*.145,1.95-(j//20)*.12,0],radius=.04,color=YELLOW) for j in range(n)]) for x,n in zip(xs,[1,10,100])])
        self.at('Their photon count grows'); self.play(FadeOut(eq),run_time=.12); eq=label('flash photons = C × I × T',y=-.3,size=32,color=YELLOW); self.play(FadeIn(dots),FadeIn(eq),run_time=.43)
        self.at('while sensitivity falls'); self.play(FadeOut(eq),run_time=.12); eq=label('S(I) ∝ 1/I',y=-.3,size=32,color=BLUE); self.play(FadeIn(eq),run_time=.33)
        peaks=VGroup(*[response(x-1.85,-.9,3.7,-1.65*r/(1+r),.65) for x,r in zip(xs,ratios)])
        self.at('So their peak responses'); self.play(FadeOut(eq),run_time=.12); eq=label('peak ≈ S(I) × C × I × T',y=-.3,size=30); self.play(Create(peaks),FadeIn(eq),FadeIn(label('peak ≈ same',y=-3.0,size=30,color=BLUE)),Create(VGroup(Line([-4.25,-2.65,0],[4.25,-2.65,0],color=BLUE),Line([-4.25,-2.65,0],[-4.25,-2.53,0],color=BLUE),Line([4.25,-2.65,0],[4.25,-2.53,0],color=BLUE))),run_time=.48); self.finish()


class S20Remove(SpokenScene):
    def construct(self):
        c=rod_cell(s=1.55).move_to([-4.9,-.1,0]); g=chip('GCAP1 + GCAP2',PURPLE,size=30).move_to([.7,2.6,0]); a=arrow(g.get_left(),[-4.1,1.15,0],PURPLE)
        old=response(-3,-.25,8.7,-.45,.6,GREY).set_stroke(opacity=.5); tr=old.copy().set_color(BLUE).set_stroke(opacity=1)
        self.add(c,g,a,old,tr,label('one photon · darkness',1.8,1.2,32,GREEN))
        mid=a.get_center(); cross=VGroup(Line(mid+[-.35,-.35,0],mid+[.35,.35,0],color=RED,stroke_width=12),Line(mid+[-.35,.35,0],mid+[.35,-.35,0],color=RED,stroke_width=12))
        self.at('Now remove'); self.play(Create(cross),run_time=.45)
        self.at('In darkness'); self.play(Transform(tr,response(-3,-.25,8.7,-2.25,1.2)),FadeIn(label('about 5×, and slower',1.8,-3.05,32,RED)),FadeIn(label('rods lacking GCAP1 + GCAP2',1.8,3.35,30,RED)),run_time=.7); self.finish()


class S21Fail(SpokenScene):
    def construct(self):
        ax,b=plot_frame(); ctrl=curve(ax,CTRL)
        self.add(b,ctrl,label('Mouse cones · background response',y=3.3,size=32),label('control cones, fit',-3.2,2.65,28,BLUE))
        red=curve(ax,KO,RED)
        self.at('keeps less current'); self.play(Create(red),run_time=.45)
        # The unchanged voice-over bridges from rods; explicitly switch scope in the picture.
        note=T('Cones: reserve inferred; slope ≠ reserve; I₀ shift not significant.',24,GREY).move_to([0,-3.65,0])
        self.play(FadeIn(label('GCAPs + recoverin absent, cone fit',2.2,2.65,28,RED)),FadeIn(note),run_time=.3)
        self.at('sensitivity falls more steeply'); self.play(FadeIn(label('steeper fall',1,-.85,28,RED)),Create(arrow([2.4,-.85,0],ax.c2p(5.55,logS(5.55,**KO)),RED)),run_time=.45); self.finish()


class S22Scope(SpokenScene):
    def construct(self):
        r=rod_cell(s=1.3).move_to([-4.7,-.15,0]); c=cone_cell(s=1.3).move_to([-1.9,-.15,0]); g=gauge(.5,x=2.1)
        self.add(r,c,g,label('mouse rods and cones · ex vivo',y=3.15,size=34),label('rod',-4.7,-2.7,30),label('cone',-1.9,-2.7,30))
        self.at('mainly from mouse'); self.play(Indicate(VGroup(r,c),scale_factor=1.02),run_time=.4)
        self.at('A bright enough light'); self.play(GrowArrow(arrow([-.3,2.6,0],[-1.7,1.5,0])),Transform(g,gauge(.02,x=2.1)),FadeIn(label('can still\nsaturate',4.5,.5,34,RED)),run_time=.55)
        self.at('still saturate them'); self.play(Indicate(g,scale_factor=1.02),run_time=.3); self.finish()


class S22bBleach(SpokenScene):
    def construct(self):
        self.add(label('In bright light',y=3.15,size=38,color=YELLOW))
        pigment=VGroup(*[chip('pigment',PINK,size=42).move_to([x,1.4,0]) for x in [-4,0,4]])
        bleach=label('bleached pigment',y=.05,size=40,color=PINK)
        self.at('Pigment bleaching'); self.play(FadeIn(pigment),FadeIn(bleach),run_time=.4)
        self.at('using up visual pigment'); self.play(*[p.animate.set_opacity(.18) for p in pigment],run_time=.8)
        self.at('other mechanisms extend'); self.play(FadeIn(label('other mechanisms',y=-1.25,size=40)),GrowArrow(arrow([-4.7,-2.1,0],[4.7,-2.1,0],GREEN)),FadeIn(label('extend the range',y=-3,size=38,color=GREEN)),run_time=.6); self.finish()


class S23Next(SpokenScene):
    def construct(self):
        nodes=VGroup(chip('calcium',ORANGE,34).move_to([-3.8,1.9,0]),chip('GCAPs',PURPLE,34).move_to([3.8,1.9,0]),chip('cGMP',GREEN,34).move_to([3.8,-1.9,0]),chip('channels',TEAL,34).move_to([-3.8,-1.9,0]))
        links=VGroup(arrow(nodes[0].get_right(),nodes[1].get_left(),ORANGE),arrow(nodes[1].get_bottom(),nodes[2].get_top(),PURPLE),arrow(nodes[2].get_left(),nodes[3].get_right(),GREEN),arrow(nodes[3].get_top(),nodes[0].get_bottom(),TEAL))
        self.add(nodes,links)
        self.at('One feedback loop'); self.play(FadeIn(label('calcium feedback',0,0,34,ORANGE)),run_time=.35)
        # Cartoon scissors, centred on the calcium -> GCAP arrow.
        sc=VGroup(Circle(radius=.23,color=TEXT).move_to([-.3,3,0]),Circle(radius=.23,color=TEXT).move_to([.3,3,0]),Line([-.3,2.8,0],[.35,1.65,0],color=TEXT,stroke_width=5),Line([.3,2.8,0],[-.35,1.65,0],color=TEXT,stroke_width=5))
        self.at('The test is'); self.play(FadeIn(sc),run_time=.3)
        self.at('cut it'); self.play(links[0].animate.set_color(RED).set_opacity(.25),sc.animate.shift(DOWN*.2),run_time=.4); self.finish()


class S24Take(SpokenScene):
    def construct(self):
        g=gauge(1,x=0,w=2.2,h=5.6,spent=True); self.add(g,label('A limited current',y=3.25,size=36))
        self.at('light spends'); self.play(Transform(g,gauge(.45,x=0,w=2.2,h=5.6,spent=True)),GrowArrow(arrow([-4,1.5,0],[-1.15,1.5,0])),FadeIn(label('light',-3.2,2.15,32,YELLOW)),FadeIn(label('spent by light',3.4,1.5,32,RED)),run_time=.55)
        self.at('calcium feedback'); self.play(GrowArrow(arrow([4,-.8,0],[1.15,-.8,0],ORANGE)),FadeIn(label('calcium feedback',3.7,-.1,30,ORANGE)),run_time=.45)
        self.at('in reserve'); self.play(FadeIn(label('held in reserve',-3.7,-1.6,32,BLUE)),Create(Line([-1.2,-1.6,0],[-2.1,-1.6,0],color=BLUE)),run_time=.35); self.finish()


class S23End(EndCard):
    LINE='Calcium feedback helps keep some current in reserve.'
    def construct(self):
        self.add(label('Calcium feedback helps keep',y=.8,size=40),label('some current in reserve.',y=-.05,size=40),label('biochemistrypedia.com',y=-1.3,size=30,color=TEAL)); self.finish()
