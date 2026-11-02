"""Read as Stretch — reviewed animation, second draft.
COLOR MAP: GREY/bright grey = anatomy and remaining cues; BLUE = primary spindle
ending and spikes; YELLOW = vibration/capsaicin; ORANGE = felt position;
PURPLE = secondary endings; RED = severe loss / chilli; TEAL = branding.
All spike trains are computed by a phase accumulator: phase'=r0+k*stretch,
with optional zero-mean periodic timing modulation. Units are illustrative,
not measured rates. Response bands are schematic, not quantitative data.
Arm endpoints, length dimensions, joint arcs and winding are geometric models.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
LIGHT = '#C3C9D3'
E = np.array([0., -2., 0.])
S = np.array([-5.6, -2., 0.])
L = 4.65


def text(s, x=0, y=0, size=30, color=TEXT, font=FONT):
    return T(s, size, color, font=font).move_to([x,y,0])


def heading(s, color=TEXT):
    return text(s,0,3.15,34,color,TITLE_FONT)


def arr(a,b,color=LIGHT,w=4):
    return Arrow(a,b,buff=.08,color=color,stroke_width=w,tip_length=.2,
                 max_tip_length_to_length_ratio=.3)


def leader(a,b,color=LIGHT):
    return Line(a,b,color=color,stroke_width=2)


def pol(c, deg, length):
    a=np.radians(deg)
    return np.array(c)+length*np.array([np.cos(a),np.sin(a),0])


def fore(angle=70,color=LIGHT,dashed=False):
    end=pol(E,angle,L)
    line=(DashedLine(E,end,color=color,stroke_width=10,dash_length=.19) if dashed
          else Line(E,end,color=color,stroke_width=17))
    return VGroup(line,Circle(radius=.17,color=color,fill_opacity=.25).move_to(end))


def arm(angle=70):
    return VGroup(Line(S,E,color=LIGHT,stroke_width=18),fore(angle),
                  Circle(radius=.19,color=TEXT,fill_color=BG,fill_opacity=1).move_to(E))


def attachments(angle=70,back=False):
    if back:
        return S+np.array([.8,-.72,0]), E+np.array([-.22,-.72,0])
    return S+np.array([1.5,1.2,0]), pol(E,angle,1.05)


def muscle(angle=70,back=False):
    a,b=attachments(angle,back)
    join=a+.78*(b-a)
    return VGroup(Line(a,join,color=LIGHT,stroke_width=29),
                  Line(join,b,color=TEXT,stroke_width=8))


def contact(angle=70,back=False):
    a,b=attachments(angle,back)
    return a+.91*(b-a)


def vibrator(angle=70,back=False):
    p=contact(angle,back)
    d=DOWN if back else UP
    box=RoundedRectangle(width=.8,height=.48,corner_radius=.08,
        color=YELLOW,fill_color=YELLOW,fill_opacity=.35).move_to(p+d*.31)
    return VGroup(box,Line(p,p+d*.13,color=YELLOW,stroke_width=6))


def rig(angle=70,back=False,device=True):
    out=VGroup(arm(angle),muscle(angle,back))
    if device: out.add(vibrator(angle,back))
    return out


def staged(obj):
    """Shared enlarged, centred anatomy; keep all overlays in the same coordinates."""
    return obj.scale(1.16, about_point=E).shift([1.3,-.25,0])


def staged_point(p):
    return E+1.16*(np.array(p)-E)+np.array([1.3,-.25,0])


def fixed_label():
    return VGroup(text('real forearm:\nfixed',4.8,1.1,30,LIGHT),
                  leader([3.8,.95,0],staged_point(pol(E,70,3.3))))


def eye(closed=False):
    if closed:
        lid=ArcBetweenPoints([-1,0,0],[1,0,0],angle=PI/3,color=LIGHT,stroke_width=5)
        lashes=VGroup(*[Line([x,-.18,0],[x*1.1,-.47,0],color=LIGHT,stroke_width=3)
                        for x in [-.65,0,.65]])
        return VGroup(lid,lashes)
    return VGroup(ArcBetweenPoints([-1.1,0,0],[1.1,0,0],angle=PI/2.4,color=LIGHT,stroke_width=4),
                  ArcBetweenPoints([-1.1,0,0],[1.1,0,0],angle=-PI/2.4,color=LIGHT,stroke_width=4),
                  Circle(radius=.38,color=BLUE,fill_opacity=.4),Dot(radius=.16,color=TEXT))


def spindle(width=9,y=.5):
    cap=Ellipse(width=width,height=1.8,color=LIGHT,fill_color=LIGHT,fill_opacity=.06).move_to([0,y,0])
    fibre=RoundedRectangle(width=width-.6,height=.36,corner_radius=.15,
        color=LIGHT,fill_color=LIGHT,fill_opacity=.2).move_to([0,y,0])
    # A projected helix with occluded back halves: alternating arcs wrap the fibre.
    wraps=VGroup()
    for x in np.linspace(-1.45,1.45,7):
        wraps.add(Arc(start_angle=-PI/2,angle=PI,radius=.33,color=BLUE,
                      stroke_width=5).stretch(.38,0).move_to([x,y,0]))
    return VGroup(cap,fibre,wraps)


def cutaway():
    shell=Ellipse(width=10.6,height=4.1,color=LIGHT,fill_color=LIGHT,fill_opacity=.05).move_to([0,.5,0])
    ordinary=VGroup(*[Line([-4.3,y,0],[4.3,y,0],color=LIGHT,stroke_width=13) for y in [-.85,1.85]])
    sp=spindle(8.4,.5)
    return VGroup(shell,ordinary,sp)


def cutaway_labels():
    return VGroup(text('biceps muscle',0,3.15,34),
        text('muscle spindle',0,-.04,30,BLUE),
        text('ordinary fibres',-3.5,-2,30,LIGHT),leader([-3.5,-1.7,0],[-3.5,-.85,0]))


def spike_times(stretch=0., phase=0.):
    # Integrate r(t)=6+12*stretch+0.9*sin(4*pi*t+phase).
    # The sinusoid integrates to zero over the one-unit observation window.
    t=np.linspace(0,1,4001)
    rate=6+12*stretch+.9*np.sin(4*PI*t+phase)
    accum=np.cumsum(rate)*(t[1]-t[0])
    return np.interp(np.arange(1,int(round(6+12*stretch))+1)-.35,accum,t)


def raster(stretch=0,y=-2.75,x0=-4.9,width=9.8,phase=0):
    times=spike_times(stretch,phase)
    return VGroup(Line([x0,y,0],[x0+width,y,0],color=LIGHT,stroke_width=2),
        *[Line([x0+width*t,y,0],[x0+width*t,y+.52,0],color=BLUE,stroke_width=4) for t in times])


def dimension(angle=70):
    a,b=attachments(angle)
    a=a+UP*.57; b=b+UP*.57
    return VGroup(Line(a,b,color=BLUE,stroke_width=3),
        Line(a+DOWN*.13,a+UP*.13,color=BLUE,stroke_width=3),
        Line(b+DOWN*.13,b+UP*.13,color=BLUE,stroke_width=3))


def prediction():
    # Two tangential arrows share an arc outside the hand's radius.
    a1=Arc(radius=5.05,start_angle=np.radians(73),angle=np.radians(22),arc_center=E,
           color=ORANGE,stroke_width=5).add_tip(tip_length=.2)
    a2=Arc(radius=5.05,start_angle=np.radians(65),angle=np.radians(-25),arc_center=E,
           color=ORANGE,stroke_width=5).add_tip(tip_length=.2)
    return VGroup(heading('Which way will the elbow seem to move?'),
        staged(rig(device=False)).shift(DOWN*.85),staged(a1).shift(DOWN*.85),staged(a2).shift(DOWN*.85),
        text('more bent',-2.4,2.05,30,ORANGE),text('straighter',4.9,.1,30,ORANGE))


def angle_card():
    return VGroup(staged(rig()),staged(fore(30,ORANGE,True)),
        heading('Biceps tendon vibration · during contraction'),
        staged(Arc(radius=2.35,start_angle=np.radians(30),angle=np.radians(40),arc_center=E,color=ORANGE,stroke_width=5)),
        text('40°',3.9,-.25,38,ORANGE,MONO),
        text('in that experiment',4.45,-2.3,30,LIGHT),
        text('not a standard size',0,-3.3,34,ORANGE))


def estimate():
    box=chip('limb position\nestimate',ORANGE,38,pad=.48).move_to([3.55,.45,0])
    src=chip('spindle signals\nof muscle length',BLUE,34,pad=.42).move_to([-3.6,.45,0])
    arrow=arr(src.get_right(),box.get_left(),BLUE,12)
    card=text('Limb position is an estimate,\nbuilt mainly from spindle signals of muscle length.',0,2.7,32,TEXT)
    return VGroup(src,arrow,box,card)


class S00Title(TitleCard):
    LESSON="Proprioception: Sensing the Body's Own Position"
    TITLE='Read as Stretch'
    def construct(self):
        self.add(text('BIOCHEMISTRYPEDIA',0,2.5,30,TEAL),
                 text("Proprioception:\nSensing the Body's Own Position",0,1,30,LIGHT))
        self.play(FadeIn(text(self.TITLE,0,-.9,54,TEXT,TITLE_FONT)),run_time=.6)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        a=arm().set_color(TEXT)
        screen=RoundedRectangle(width=12,height=5.8,corner_radius=.15,color=LIGHT,
            stroke_opacity=.35,fill_color=BG,fill_opacity=.22).move_to([0,-.15,0])
        table=VGroup(Line([-6,-2.45,0],[6,-2.45,0],color=LIGHT,stroke_width=6),
                     Line([-5,-2.45,0],[-5,-3.45,0],color=LIGHT,stroke_width=5),
                     Line([5,-2.45,0],[5,-3.45,0],color=LIGHT,stroke_width=5))
        self.add(a,table,screen,eye(True).move_to([4.4,2.2,0]))
        self.at('close your eyes')
        self.at("where's your elbow")
        q=text('Where is your elbow?',-1,1.2,44,TEXT,TITLE_FONT)
        q.add_background_rectangle(color=BG,opacity=.9,buff=.18)
        self.play(FadeIn(q),run_time=.25)
        self.at('but how')
        self.play(Indicate(a[2],color=ORANGE,scale_factor=1.5),run_time=.45)
        self.finish()


class S02Spindle(SpokenScene):
    def construct(self):
        g=cutaway(); labels=cutaway_labels()
        self.add(g[0],g[1],labels[0])
        self.at('stretch sensors')
        self.play(FadeIn(g[2]),run_time=.45)
        self.at('muscle spindles')
        self.play(FadeIn(labels[1]),run_time=.3)
        self.at('they sit alongside')
        self.play(FadeIn(labels[2:]),run_time=.35)
        self.finish()


class S03Stretch(SpokenScene):
    def construct(self):
        g=cutaway(); lab=cutaway_labels(); r=raster()
        self.add(g,lab,r,text('sensory ending firing · spikes',0,-3.35,30,BLUE))
        self.at('stretch the muscle')
        # Baseline remains visible while the muscle begins lengthening.
        self.play(g.animate.stretch(1.12,0),run_time=1.3)
        self.at('sensory endings')
        self.play(Indicate(g[2][2],color=BLUE,scale_factor=1.05),run_time=.4)
        self.at('fire faster')
        self.play(FadeOut(r),FadeIn(raster(1)),run_time=.5)
        self.finish()


class S04Ia(SpokenScene):
    def construct(self):
        sp=spindle(11,0).stretch(2.4,1)
        self.add(sp,text('intrafusal fibre',3.9,-2.55,30,LIGHT),
                 leader([3.9,-2.2,0],[3.9,-.45,0]))
        self.at('the primary ending')
        self.play(Indicate(sp[2],color=BLUE,scale_factor=1.08),run_time=.45)
        self.at('called')
        self.play(FadeIn(text('primary ending · type Ia',0,3.1,36,BLUE,TITLE_FONT)),
                  Create(leader([0,2.6,0],[0,.92,0],BLUE)),run_time=.35)
        self.at('small')
        self.play(sp.animate.stretch(1.045,0),rate_func=lambda t:.5-.5*np.cos(12*PI*t),run_time=1.45)
        self.add(text('small, rapid stretches',0,-3.15,30,BLUE))
        self.finish()


class S05Vibrator(SpokenScene):
    def construct(self):
        sp=spindle(8.5,.4).stretch(1.4,1)
        # Tendon continues the intrafusal axis into the device contact.
        tendon=Line([4.25,.4,0],[5.3,.4,0],color=TEXT,stroke_width=8)
        dev=RoundedRectangle(width=1,height=.55,corner_radius=.08,color=YELLOW,
             fill_color=YELLOW,fill_opacity=.3).move_to([5,.74,0])
        small=rig().scale(.48).move_to([-4.5,2.35,0])
        self.add(sp,tendon,text('muscle spindle',0,2.05,32,BLUE),
                 small,text('elbow still',-.8,2.65,30,LIGHT),
                 raster(),text('sensory ending firing · spikes',0,-3.35,30,BLUE))
        self.at('a vibrator')
        self.play(FadeIn(dev),run_time=.3)
        self.at('on a tendon')
        self.play(FadeIn(text('tendon',5,-.5,30,LIGHT)),
                  Create(leader([5,-.25,0],[5,.3,0])),run_time=.3)
        self.at('many tiny stretches')
        ripples=VGroup(*[Arc(radius=r,start_angle=PI*.68,angle=PI*.64,color=YELLOW,stroke_width=4)
                        .move_to([3.7-i*.5,.4,0]) for i,r in enumerate([.32,.5,.68])])
        self.play(FadeIn(ripples),sp.animate.stretch(1.035,0),
                  rate_func=lambda t:.5-.5*np.cos(12*PI*t),run_time=.9)
        self.add(ripples.set_stroke(opacity=1).set_fill(opacity=0))
        self.at('every second')
        self.play(FadeOut(self.mobjects[5]),FadeIn(raster(1)),run_time=.4)
        self.finish()


class S06Setup(SpokenScene):
    def construct(self):
        self.add(staged(rig()))
        self.at('goodwin')
        self.play(FadeIn(heading('Goodwin, McCloskey and Matthews · 1972')),run_time=.4)
        self.at('biceps tendon')
        self.play(FadeIn(text('biceps tendon',-3.5,.9,32,YELLOW)),
                  Create(leader([-2,.7,0],staged_point(contact()+UP*.05),YELLOW)),run_time=.35)
        self.at('at')
        self.play(FadeIn(text('100 Hz',4.9,-.35,36,YELLOW,MONO)),
                  Create(leader([4,-.35,0],staged(vibrator())[0].get_top(),YELLOW)),run_time=.3)
        self.at('the elbow')
        self.play(FadeIn(fixed_label()),run_time=.35)
        self.finish()


class S07Front(SpokenScene):
    def construct(self):
        a=staged(arm()); m=staged(muscle()); d=staged(dimension())
        self.add(a,m,heading('Biceps · in front of the elbow'),d,
                 text('muscle length',-3,1.25,32,BLUE))
        self.at('the biceps')
        self.at('it gets longer')
        self.play(Transform(a,staged(arm(25))),Transform(m,staged(muscle(25))),Transform(d,staged(dimension(25))),run_time=1.65)
        self.wait(.45)
        self.play(Transform(a,staged(arm())),Transform(m,staged(muscle())),Transform(d,staged(dimension())),run_time=.7)
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        self.add(prediction())
        self.at('predict')
        self.at('if the brain')
        self.play(Indicate(self.mobjects[0][1][1],color=BLUE,scale_factor=1.03),run_time=.5)
        self.at('which way')
        self.play(Indicate(self.mobjects[0][2:4],color=ORANGE,scale_factor=1.02),run_time=.55)
        self.finish()


class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(prediction())
        self.wait(5)


class S10Reveal(SpokenScene):
    def construct(self):
        ghost=staged(fore(70,ORANGE,True))
        self.add(staged(rig()),ghost,heading('Felt position',ORANGE),fixed_label())
        self.at('toward a straighter arm')
        self.play(Transform(ghost,staged(fore(30,ORANGE,True))),run_time=1.1)
        self.at('subjects')
        self.at('the vibrated muscle')
        self.play(FadeIn(text('consistent with a stretched biceps',0,-3.25,36,ORANGE)),run_time=.4)
        self.finish()


class S11Triceps(SpokenScene):
    def construct(self):
        # A broad posterior muscle and a tendon leader make the back side explicit.
        back=staged(muscle(back=True))
        back[0].set_stroke(width=42)
        device=staged(vibrator(back=True)).scale(1.25)
        ghost=staged(fore(70,ORANGE,True))
        ghost_label=text('felt position',4.8,1.65,32,ORANGE)
        ghost_leader=leader([3.6,1.55,0],staged_point(pol(E,70,3.9)),ORANGE)
        self.add(staged(arm()),back,device,heading('Triceps · behind the elbow'),
                 text('triceps',-3.5,-1.35,32,LIGHT),
                 leader([-3.5,-1.65,0],back[0].get_center()),
                 text('tendon vibration',4.5,-3.15,30,YELLOW),
                 leader([3,-3.1,0],device.get_right(),YELLOW),ghost_label,
                 ghost_leader)
        self.at('vibrate the triceps')
        self.play(Indicate(device,color=YELLOW,scale_factor=1.08),run_time=.35)
        self.at('behind the elbow')
        self.add(ghost)
        self.at('seemed more bent')
        self.play(Transform(ghost,staged(fore(115,ORANGE,True))),
                  ghost_label.animate.move_to([-3.5,1.4,0]),
                  Transform(ghost_leader,leader([-2.2,1.4,0],staged_point(pol(E,115,3.5)),ORANGE)),run_time=.7)
        self.finish()


class S12Size(SpokenScene):
    def construct(self):
        g=angle_card(); ghost=staged(fore(70,ORANGE,True))
        self.add(g[0],g[2],ghost)
        self.at('during contraction')
        self.at('the error could reach')
        self.at('40 degrees')
        self.play(Transform(ghost,g[1]),Create(g[3]),FadeIn(g[4]),run_time=.6)
        self.at('in that experiment')
        self.play(FadeIn(g[5]),run_time=.25)
        self.at('it is not')
        self.play(FadeIn(g[6]),run_time=.35)
        self.finish()


class S13Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(angle_card())
        self.wait(2)


class S14Fooled(SpokenScene):
    def construct(self):
        box=chip('position\nestimate',ORANGE,36,pad=.4).move_to([3.5,0,0])
        r1=raster(1,y=1.2,x0=-5.7,width=4.8,phase=0)
        r2=raster(1,y=-1.8,x0=-5.7,width=4.8,phase=PI)
        labels=VGroup(text('real stretch',-3.3,2.15,32,LIGHT),text('vibrator',-3.3,-.85,32,YELLOW))
        arrows=VGroup(arr([-.65,1.5,0],box.get_left()+UP*.4,BLUE,7),
                      arr([-.65,-1.5,0],box.get_left()+DOWN*.4,BLUE,7))
        self.add(r1,r2,labels,heading('No label of the cause'))
        self.at("a spindle's firing")
        self.at('no label')
        self.play(FadeIn(box),Create(arrows),FadeIn(text('same read-out:\nstretch',3.5,-2,32,ORANGE)),run_time=.45)
        self.at('with the arm')
        self.play(FadeIn(text('equal mean rate · different timing · schematic',0,-3.3,30,LIGHT)),run_time=.35)
        self.at('the brain')
        self.play(Indicate(box,color=ORANGE,scale_factor=1.04),run_time=.45)
        self.finish()


class S15Rule(SpokenScene):
    def construct(self):
        g=estimate()
        self.add(g)
        self.at('the one idea')
        self.at('limb position')
        self.play(Indicate(g[2],color=ORANGE,scale_factor=1.03),run_time=.4)
        self.at('built mainly')
        self.play(Indicate(g[0],color=BLUE,scale_factor=1.03),
                  Indicate(g[1],color=BLUE,scale_factor=1.03),run_time=.5)
        self.add(text('muscle length → spindle signals\n→ estimated position',0,-2.45,34,BLUE))
        self.finish()


class S16Estimate(SpokenScene):
    def construct(self):
        g=estimate(); self.add(g)
        # Three distinct edge targets; tails sit immediately above aligned labels.
        for phrase,label,x,target in [('skin','skin',-.7,2.5),('joint','joint',2.15,3.55),
                                      ('motor command','motor command',5,4.6)]:
            self.at(phrase)
            t=text(label,x,-2.6,32,LIGHT)
            a=arr([x,-2.12,0],[target,g[2].get_bottom()[1]-.08,0],LIGHT,4)
            self.play(FadeIn(t),GrowArrow(a),run_time=.3)
        self.finish()


class S17Halves(SpokenScene):
    def construct(self):
        divider=Line([0,-3.45,0],[0,3.45,0],color=GREY,stroke_width=2)
        # Transform the complete assembly together, preserving tendon contact.
        left=rig(device=False).scale(.78).move_to([-3.55,.15,0])
        left.shift(LEFT*(left[0][2].get_center()[0]+2.35))
        full=rig().scale(.78).move_to(left)
        # Align assemblies by elbow rather than their different bounding boxes.
        full.shift(left[0][2].get_center()-full[0][2].get_center())
        ghost=fore(70,ORANGE,True).scale(.78,about_point=E).shift(left[0][2].get_center()-E)
        target=fore(55,ORANGE,True).scale(.78,about_point=E).shift(left[0][2].get_center()-E)
        e=eye().scale(1.12).move_to([3.5,1.35,0])
        movement=chip('accurate movement',LIGHT,28).move_to([3.5,-2,0])
        self.add(divider,left,text('still, unseen arm',-3.5,3.05,30,LIGHT),e,
                 text('vision',3.5,2.5,30,LIGHT),movement)
        cues=VGroup()
        for name,x,tx in [('skin',1.2,2.1),('joint',3.6,3.8),('motor\ncommand',5.45,4.9)]:
            cues.add(text(name,x,-.1,30,LIGHT),arr([x,-.65,0],[tx,-1.55,0],LIGHT,2))
        self.play(FadeIn(cues),run_time=.4)
        self.at('in a still')
        self.at('vibrating one tendon')
        self.play(FadeIn(full[2]),run_time=.35)
        self.at('usually biases')
        self.add(ghost)
        self.play(Transform(ghost,target),run_time=.85)
        self.at('typical direction')
        self.play(FadeIn(text('toward muscle lengthening',-3.5,-2.4,30,ORANGE)),run_time=.35)
        self.at('not a guaranteed response')
        self.play(FadeIn(text('not guaranteed',-3.5,-3.25,38,ORANGE)),run_time=.35)
        self.at('proprioceptive input')
        self.play(FadeIn(text('severe proprioceptive loss',3.5,3.3,30,RED)),run_time=.35)
        self.at('on vision')
        self.play(GrowArrow(arr([2.7,.7,0],[2.7,-1.45,0],BLUE,10)),
                  FadeIn(text('major visual compensation',3.5,-3.25,30,BLUE)),run_time=.45)
        self.finish()


class S18Link(SpokenScene):
    def construct(self):
        self.add(Line([0,-3.45,0],[0,3.45,0],color=GREY),
                 text('Touch and pain',-3.5,3.1,32),text('Proprioception',3.5,3.1,32))
        # Context on both halves from the beginning, then inputs/results on their words.
        membrane=VGroup(*[Line([-6.1,y,0],[-.9,y,0],color=LIGHT,stroke_width=5) for y in [.25,-.2]])
        channel=chip('TRPV1',LIGHT,30).move_to([-3.5,.03,0])
        channel[0].set_fill(BG,opacity=1)
        right=rig(device=False).scale(.48).move_to([3.5,-1,0])
        full=rig().scale(.48).move_to(right)
        full.shift(right[0][2].get_center()-full[0][2].get_center())
        sp=spindle(4.5,1.1).shift(RIGHT*3.5)
        source=text('vibrator → spindle ending',3.5,2.3,30,YELLOW)
        drive=arr(full[2].get_top()+UP*.05,[3.5,.25,0],YELLOW)
        follow=text('follow the line',0,-3.3,36,BLUE)
        into_fibre=arr([-2.6,-.3,0],[-1.5,-1.6,0],BLUE,7)
        self.add(membrane,right,channel,full[2],sp,source,drive,into_fibre,
                 text('pain fibre\nmembrane',-4.65,-1.1,30,LIGHT),
                 follow)
        self.at('in touch and pain')
        self.at('capsaicin opened')
        # Curved tapered chilli silhouette with stalk, wholly within the safe frame.
        pepper=VMobject(color=RED,fill_color=RED,fill_opacity=.9,stroke_width=3)
        pepper.set_points_smoothly([[-5.5,2.25,0],[-4.95,2.35,0],[-4.65,1.8,0],
            [-4.95,1.2,0],[-5.9,.85,0],[-5.45,1.5,0],[-5.5,2.25,0]])
        stalk=ArcBetweenPoints([-5.25,2.25,0],[-5.65,2.7,0],angle=PI/3,color=GREEN,stroke_width=6)
        self.play(FadeIn(VGroup(pepper,stalk)),FadeIn(text('capsaicin',-2.6,1.95,30,YELLOW)),
                  GrowArrow(arr([-2.6,1.5,0],[-3.2,.5,0],YELLOW)),run_time=.45)
        self.at('on pain')
        self.play(Indicate(channel,color=YELLOW,scale_factor=1.05),run_time=.35)
        self.at('it felt hot')
        self.play(FadeIn(text('burning, no heat',-3.5,-2.4,32,ORANGE)),run_time=.35)
        self.at('here')
        self.play(Indicate(right,color=LIGHT,scale_factor=1.02),run_time=.3)
        self.at('a vibrator drives')
        self.play(Indicate(full[2],color=YELLOW,scale_factor=1.08),
                  Indicate(sp[2],color=BLUE,scale_factor=1.06),run_time=.4)
        self.at('while the joint')
        self.play(FadeIn(text('felt movement · joint still',3.5,-2.4,30,ORANGE)),
                  Indicate(follow,color=BLUE,scale_factor=1.04),run_time=.4)
        self.finish()


def response_axes(title):
    return VGroup(heading(title),
        Line([-.6,-2.3,0],[5.7,-2.3,0],color=LIGHT,stroke_width=3),
        Line([-.6,-2.3,0],[-.6,1.7,0],color=LIGHT,stroke_width=3),
        text('response to vibration, schematic',2.45,-2.75,30,LIGHT),
        text('qualitative tendency · no numerical scale',0,-3.4,30,LIGHT))


def response_row(label,color,y,extent,jitter=False):
    lab=text(label,-3.6,y,30,color,TITLE_FONT)
    band=Rectangle(width=extent,height=.48,color=color,fill_color=color,fill_opacity=.38).move_to([-.6+extent/2,y,0])
    out=VGroup(lab,band)
    if jitter:
        # Overlapping uncertainty-style bands: endpoints deliberately carry no ranking.
        out.add(Line([-.6+extent-.48,y,0],[-.6+extent+.48,y,0],color=color,stroke_width=5),
                *[Line([-.6+extent+delta,y-.12,0],[-.6+extent+delta,y+.12,0],color=color,stroke_width=3)
                  for delta in [-.48,.48]])
    return out


class S19Caveat(SpokenScene):
    def construct(self):
        axes=response_axes('Primary endings · likely carriers')
        p=response_row('primary · type Ia',BLUE,1.1,4.9)
        s=response_row('secondary · type II',PURPLE,-1.25,2.9)
        self.add(axes,p,s)
        self.at('one caveat')
        self.at('primary endings')
        self.at('in a small')
        self.play(FadeIn(text('Roll and Vedel · 1982 · small leg-muscle sample',0,2.3,30,LIGHT)),run_time=.35)
        self.at('they tended')
        self.play(Indicate(p[1],color=BLUE,scale_factor=1.04),run_time=.45)
        self.at('low amplitude vibration')
        self.play(FadeIn(text('low-amplitude vibration',2.25,-.15,30,YELLOW)),run_time=.35)
        self.at('secondary endings')
        self.play(Indicate(s[1],color=PURPLE,scale_factor=1.04),run_time=.45)
        self.finish()


class S20Caveat2(SpokenScene):
    def construct(self):
        axes=response_axes('Contracting muscle · responses overlap')
        self.add(axes)
        self.at('in contracting muscle')
        p=response_row('primary · type Ia',BLUE,1.1,4.25,True)
        self.play(FadeIn(p),run_time=.3)
        self.at('secondary endings')
        s=response_row('secondary · type II',PURPLE,-.05,4.35,True)
        self.play(FadeIn(s),run_time=.35)
        self.at('tendon organs')
        tendon=response_row('tendon organs',LIGHT,-1.25,4.2,True)
        self.play(FadeIn(tendon),run_time=.35)
        self.at('so primary endings')
        self.play(FadeIn(text('not shown to act alone',0,2.3,32,BLUE)),run_time=.4)
        self.finish()


class S21Takeaway(SpokenScene):
    def construct(self):
        ghost=staged(fore(70,ORANGE,True))
        self.add(staged(rig()),heading('A still limb can feel moved',ORANGE),fixed_label())
        self.at('vibrating one tendon')
        self.play(Indicate(self.mobjects[0][2],color=YELLOW,scale_factor=1.08),run_time=.45)
        self.at('feel moved')
        self.add(ghost)
        self.play(Transform(ghost,staged(fore(30,ORANGE,True))),run_time=.7)
        self.at('the brain reads')
        self.play(FadeIn(text('extra spindle firing → stretch',0,-3.25,32,BLUE)),run_time=.45)
        self.finish()


class S22End(EndCard):
    LINE='Vibrating one tendon can make a still limb feel moved:\nthe brain reads the extra spindle firing as stretch.'
    def construct(self):
        # Reviewer explicitly requests the full takeaway, overriding the original 12-word card.
        self.add(text('Vibrating one tendon can make\na still limb feel moved:',0,1.65,38,TEXT,TITLE_FONT),
                 text('the brain reads the extra\nspindle firing as stretch.',0,-.55,38,ORANGE,TITLE_FONT),
                 text('biochemistrypedia.com',0,-2.85,30,TEAL))
        self.finish()
