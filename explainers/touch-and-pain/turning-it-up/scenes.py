"""Turning the Report Up and Down: revised, word-synchronised teaching film.
COLOR MAP: BLUE touch; ORANGE pain/nociceptive route; YELLOW moving signal;
GREEN inhibition; RED injury/removal; GREY anatomy. No molecular structures.
Rasters are generated from a qualitative piecewise-rate event model, not data.
The 2/6-spike comparison is explicitly schematic, not a measured effect size.
"""
import numpy as np
from bp_style import *
ORANGE = '#F29E4C'
TOUCH, PAIN, SIG, STRUCT = BLUE, ORANGE, YELLOW, GREY

def label(s, x=0, y=3.05, size=30, color=TEXT):
    return T(s, size=size, color=color).move_to([x,y,0])


def box(s, x, y, color=GREY, size=28):
    lines=VGroup(*[T(t,size,TEXT) for t in s.split('\n')]).arrange(DOWN,buff=.13)
    r=RoundedRectangle(width=lines.width+.5,height=lines.height+.45,corner_radius=.16,
        color=color,fill_color=BG,fill_opacity=1)
    return VGroup(r,lines.move_to(r)).move_to([x,y,0])


def arr(a,b,c=GREY,w=5):
    return Arrow([*a,0],[*b,0],buff=0,color=c,stroke_width=w,max_tip_length_to_length_ratio=.15)


def inhibit(a,b,w=6):
    a,b=np.array([*a,0.]),np.array([*b,0.])
    v=b-a; v=v/np.linalg.norm(v); p=np.array([-v[1],v[0],0])*.23
    return VGroup(Line(a,b,color=GREEN,stroke_width=w),Line(b-p,b+p,color=GREEN,stroke_width=w))


def sign(s,x,y,c):
    return VGroup(Circle(.23,color=c,fill_color=BG,fill_opacity=1),T(s,38,c,weight=BOLD)).move_to([x,y,0])


def flow(scene,path,period=1.8,r=.09):
    """A travelling signal keeps the named path active during narration waits."""
    dot=Dot(path.get_start(),radius=r,color=SIG)
    dot.phase=0
    def update(m,dt):
        m.phase=(m.phase+dt/period)%1
        m.move_to(path.point_from_proportion(m.phase))
    dot.add_updater(update); scene.add(dot)
    return dot


def breathe(m):
    m.clock=0
    def update(obj,dt):
        obj.clock+=dt
        obj.set_stroke(opacity=.7+.3*np.sin(obj.clock*2)**2)
    m.add_updater(update)
    return m


def arm(burn=False):
    # Forearm broadens toward the elbow; wrist narrows into a palm and fingers.
    pts=[[-5,-2.3,0],[-5,1.2,0],[-2.5,1,0],[1.9,.3,0],[2.7,.3,0],
         [3.2,.9,0],[4.5,1,0],[5.2,.75,0],[5.5,.4,0],[5.3,.1,0],
         [5.6,-.25,0],[5.3,-.55,0],[5.45,-.9,0],[5.05,-1.2,0],
         [4.8,-1.55,0],[3.4,-1.65,0],[2.6,-1.2,0],[1.9,-1.15,0],[-2.5,-2.1,0]]
    skin=Polygon(*pts,color=RED if burn else GREY,fill_color=RED if burn else GREY,fill_opacity=.25)
    wrist=Line([2.35,.25,0],[2.35,-1.15,0],color=GREY)
    sleeve=Polygon([-5.7,-2.6,0],[-3.6,-2.4,0],[-3.2,1.55,0],[-5.7,1.8,0],
        color=TOUCH,fill_color=TOUCH,fill_opacity=.3)
    seam=Line([-3.45,-2.35,0],[-3.05,1.5,0],color=TOUCH,stroke_width=5)
    return VGroup(VGroup(skin,wrist),VGroup(sleeve,seam))


def shower(x=2,y=2.5):
    head=VGroup(Arc(radius=.7,start_angle=0,angle=PI,color=GREY),Line([-.7,0,0],[.7,0,0],color=GREY)).move_to([x,y,0])
    drops=VGroup(*[Line([x+i*.4,y-.4-j*.65,0],[x+i*.4-.12,y-.7-j*.65,0],color=TOUCH,stroke_width=5)
        for i in range(-2,3) for j in range(3)])
    return VGroup(head,drops)


def painbar(x,y,level=.2,name='pain'):
    outline=Rectangle(width=2.6,height=.35,color=PAIN).move_to([x,y,0])
    fill=Rectangle(width=2.5*level,height=.25,stroke_width=0,fill_color=PAIN,fill_opacity=1).move_to([x-1.25+1.25*level,y,0])
    return VGroup(outline,fill,label(name,x,y+.5,26,PAIN))


def setbar(b,level):
    return b[1].animate.stretch_to_fit_width(2.5*level).move_to(b[0].get_left()+RIGHT*(.05+1.25*level))


def dial(x,y,name,angle=-2.3,r=1.1):
    ring=Circle(r,color=GREY,stroke_width=4).move_to([x,y,0])
    ticks=VGroup(*[Line([x+(r-.12)*np.cos(a),y+(r-.12)*np.sin(a),0],
        [x+r*np.cos(a),y+r*np.sin(a),0],color=GREY) for a in np.linspace(-3.8,.65,9)])
    needle=Line([x,y,0],[x+.8*r*np.cos(angle),y+.8*r*np.sin(angle),0],color=SIG,stroke_width=7)
    return VGroup(ring,needle,ticks,label(name,x,y-r-.5,28))


def cornerdial(name):
    return dial(5.3,2.55,name,angle=.6,r=.48)


def turn(scene,d,angle=2.8,t=.5):
    scene.play(Rotate(d[1],angle,about_point=d[0].get_center()),run_time=t)


def levels(y=.1):
    ds=VGroup(*[dial(x,y,n) for x,n in zip([-4,0,4],['ending','dorsal horn','brainstem'])])
    path=Line([-5.6,2.35,0],[5.5,2.35,0],color=PAIN,stroke_width=5)
    return VGroup(VGroup(path,label('skin',-5.5,3,28),label('brain',5.2,3,28)),ds)


class Gate:
    """Planar circuit: touch above, pain below, interneuron in the middle.
    The inhibition of the transmission cell is the stated modern simplification.
    """
    def __init__(self,inter=True,removed=False):
        self.touch=VGroup(Line([-5.6,1.8,0],[-3.5,1.8,0],color=TOUCH,stroke_width=10),label('large / touch',-4.6,2.4,28,TOUCH))
        self.pain=VGroup(Line([-5.6,-2,0],[-3.5,-2,0],color=PAIN,stroke_width=6),label('small / pain',-4.6,-2.65,28,PAIN))
        self.t=box('transmission\ncell',3,1.8,PAIN,28)
        self.i=box('inhibitory\ninterneuron',-.7,-.2,GREEN,28)
        self.direct=VGroup(arr((-3.5,1.8),(self.t.get_left()[0],1.8),TOUCH),sign('+',.5,2.18,TOUCH))
        # Pain travels below the interneuron, then rises on the right.
        route=VMobject(color=PAIN,stroke_width=5).set_points_as_corners([[-3.5,-2,0],[3,-2,0],[3,self.t.get_bottom()[1],0]])
        tip=arr((3,.1),(3,self.t.get_bottom()[1]),PAIN)
        self.pdirect=VGroup(route,tip,sign('+',3.5,.35,PAIN))
        self.ti=VGroup(arr((-2.8,1.8),(-1.4,self.i.get_top()[1]),TOUCH),sign('+',-2.15,.95,TOUCH))
        self.pi=VGroup(inhibit((-2.8,-2),(-1.4,self.i.get_bottom()[1])),sign('−',-2.3,-1.25,GREEN))
        self.it=VGroup(inhibit((self.i.get_right()[0],-.2),(self.t.get_left()[0],1.25)),sign('−',1.1,.6,GREEN))
        self.up=arr((3,self.t.get_top()[1]),(3,3.45),PAIN,12)
        self.base=VGroup(self.touch,self.pain,self.direct,self.pdirect,self.t,self.up)
        self.inhib=VGroup(self.i,self.ti,self.pi,self.it)
        self.all=VGroup(self.base,*([self.inhib] if inter and not removed else []))


def question():
    return label('What does a light touch do?',0,-3.25,34)


def condition():
    return label('Rubbing helps only if added damping > direct excitation',0,-3.35,27,SIG)


def history_panel(x,modern=False):
    title='Simplified modern model' if modern else 'Melzack & Wall, 1965'
    border=RoundedRectangle(width=6.05,height=4.9,corner_radius=.18,color=GREY).move_to([x,-.1,0])
    heading=label(title,x,2.95,28)
    inc=VGroup(Line([x-2.6,1.3,0],[x-.2,1.3,0],color=TOUCH,stroke_width=7),
        Line([x-2.6,.1,0],[x-.2,.1,0],color=PAIN,stroke_width=5))
    ends=VGroup(Dot([x-.2,1.3,0],radius=.14,color=TOUCH),Dot([x-.2,.1,0],radius=.14,color=PAIN))
    cell=box('transmission\ncell',x+1.65,.7,PAIN,26)
    links=VGroup(arr((x,1.3),(cell.get_left()[0],.95),TOUCH),arr((x,.1),(cell.get_left()[0],.45),PAIN))
    inhib=box('inhibitory cell',x-1,-1.4,GREEN,26)
    if modern:
        damping=inhibit((x-1,inhib.get_top()[1]),(x+1.65,cell.get_bottom()[1]))
        minus=T('−',28,GREEN).move_to(damping[1].get_center()+RIGHT*.3)
    else:
        damping=VGroup(inhibit((x-.9,-.95),(x-.2,-.05)),inhibit((x-.9,-.95),(x-.2,1.15)))
        minus=VGroup(*[T('−',28,GREEN).move_to(link[1].get_center()+RIGHT*.3) for link in damping])
    caption='on the transmission cell' if modern else 'on incoming fibre terminals'
    return VGroup(border,heading,inc,ends,cell,links,inhib,damping,minus,label(caption,x,-3.05,26,GREEN))


def paw(x=-3.6,y=0):
    # Large hind paw: ankle taper, oval pad, three individually outlined toes.
    ankle=Polygon([x-.65,y+.6,0],[x+.65,y+.6,0],[x+.9,y+2.4,0],[x-.55,y+2.4,0],color=GREY,fill_color=GREY,fill_opacity=.2)
    pad=Ellipse(width=2.4,height=1.65,color=GREY,fill_color=GREY,fill_opacity=.3).move_to([x,y+.05,0])
    toes=VGroup(*[Ellipse(width=.7,height=.85,color=GREY,fill_color=GREY,fill_opacity=.25).move_to([x+dx,y-.65,0]) for dx in [-.75,0,.75]])
    foot=VGroup(ankle,pad,toes)
    mesh=VGroup(Line([x-1.7,y-1.15,0],[x+1.7,y-1.15,0],color=GREY),
        *[Line([x+dx,y-1.15,0],[x+dx-.35,y-1.5,0],color=GREY) for dx in np.arange(-1.3,1.7,.4)])
    probe=VGroup(Line([x,y-2.6,0],[x,y-1.1,0],color=TOUCH,stroke_width=6),Dot([x,y-1.1,0],radius=.1,color=TOUCH))
    return foot,probe,mesh


def mouse_circuit(x,y,scope=False):
    route=arr((x-2.5,y+.5),(x+1.2,y+.5),TOUCH,8)
    relay=Circle(.5,color=PAIN,fill_color=PAIN,fill_opacity=.2).move_to([x+1.7,y+.5,0])
    output=arr((x+1.7,y+1),(x+1.7,y+1.8),PAIN,10)
    old=Circle(.4,color=GREY,fill_color=GREY,fill_opacity=.15).move_to([x-.7,y-.9,0])
    cross=Cross(old,stroke_color=RED,stroke_width=5)
    return VGroup(route,relay,output,old,cross,label('touch',x-1.7,y+1.1,28,TOUCH),
        VGroup() if scope else label('pain line',x+.8,y+2.2,28,PAIN),label('inhibition removed',x,y-1.7,30,RED))


def scope_history(x):
    touch=Line([x-2.65,.1,0],[x+.05,.1,0],color=TOUCH,stroke_width=7)
    pain=Line([x-2.65,-1,0],[x+.05,-1,0],color=PAIN,stroke_width=5)
    terminals=VGroup(Dot([x+.05,.1,0],radius=.13,color=TOUCH),Dot([x+.05,-1,0],radius=.13,color=PAIN))
    relay=Circle(.46,color=PAIN).move_to([x+1.9,-.45,0])
    links=VGroup(arr((x+.2,.1),(x+1.44,-.25),TOUCH),arr((x+.2,-1),(x+1.44,-.65),PAIN))
    cell=Circle(.4,color=GREEN,fill_color=GREEN,fill_opacity=.3).move_to([x-1.1,-2,0])
    damp=VGroup(inhibit((x-.9,-1.7),(x+.05,-.05)),inhibit((x-.9,-1.7),(x+.05,-1.15)))
    # A single left-aligned line keeps the two descriptors on one baseline.
    caption=VGroup(T('inhibitory cell',24,GREEN),T('on fibre terminals',24,GREEN)).arrange(RIGHT,buff=.25)
    caption.move_to([x,-2.95,0]).align_to(touch,LEFT)
    return VGroup(touch,pain,terminals,relay,links,cell,damp,caption)


class S00Title(TitleCard):
    LESSON='Touch and Pain'
    TITLE='Turning the Report Up and Down'

class S01Q(SpokenScene):
    def construct(self):
        a=arm();self.add(a)
        self.at('Why can the same')
        self.play(FadeIn(label('Same touch: fine one day, painful the next?',0,2.9,34)),a[1].animate.shift(RIGHT*.6),run_time=.7)
        b=painbar(0,-3,.12,'day one: shirt');self.add(b)
        self.at('hurt the next');self.play(setbar(b,.85),Transform(b[2],label('day two: shirt',0,-2.5,26,PAIN)),run_time=.55)
        self.finish()

class S02Sunburn(SpokenScene):
    def construct(self):
        a=arm();b=painbar(-1,-3,.08,'shirt');c=painbar(3,-3,.35,'shower');self.add(a,b,c)
        day=label('day one',-4.8,2.8,28);self.add(day)
        self.at('a mild sunburn');self.play(Transform(a[0],arm(True)[0]),Transform(day,label('day two',-4.8,2.8,28)),FadeIn(label('mild sunburn',0,2.8,30,RED)),run_time=.55)
        self.at('a brushing shirt');self.play(a[1].animate.shift(RIGHT*.9),setbar(b,.7),run_time=.65)
        self.at('A shower');d=shower();self.play(FadeIn(d),run_time=.4)
        self.at('now hurts');self.play(d[1].animate.shift(DOWN*.6),setbar(c,.95),run_time=.7)
        self.finish()

class S03Terms(SpokenScene):
    def construct(self):
        a=arm(True).scale(.9).shift(DOWN*.25);d=shower(2,1.6);self.add(a,d)
        self.at('normally harmless touch');self.play(a[1].animate.shift(RIGHT*.5),run_time=.6)
        self.at('is allodynia');self.play(FadeIn(label('allodynia',-3,3,36,PAIN)),FadeIn(label('pain from a harmless touch',-3,2.4,26)),run_time=.45)
        self.at('Greater pain');self.play(d[1].animate.shift(DOWN*.4),run_time=.6)
        self.at('is hyperalgesia');self.play(FadeIn(label('hyperalgesia',3,3,36,PAIN)),FadeIn(label('more pain from a painful stimulus',3,2.4,26)),run_time=.5)
        breathe(a[0][0]);self.finish()

class S04Levels(SpokenScene):
    def construct(self):
        n=levels();self.add(n,label('Same stimulus, different report',0,-3,34))
        self.at('Same stimulus');d=flow(self,n[0][0],period=2)
        self.play(d.animate.scale(1.8),run_time=.6)
        self.at('different report');report=Dot([5.5,2.35,0],radius=.3,color=SIG)
        self.play(FadeIn(report),d.animate.scale(.45),run_time=.65)
        self.at('Its size can');self.play(report.animate.scale(.35),Rotate(n[1][0][1],2.8,about_point=n[1][0][0].get_center()),run_time=.6)
        self.at('at three levels');self.play(*[Rotate(k[1],2.6,about_point=k[0].get_center()) for k in n[1][1:]],run_time=.8)
        self.finish()

class S05Ending(SpokenScene):
    def construct(self):
        cd=cornerdial('ending');cd[1].rotate(-2.8,about_point=cd[0].get_center())
        skin=Rectangle(width=11.8,height=1.5,color=RED,fill_color=RED,fill_opacity=.17).move_to([0,-2.4,0])
        ending=VGroup(Line([-5,-1,0],[0,-1,0],color=PAIN,stroke_width=9),
            *[Line([0,-1,0],[x,-2.35,0],color=PAIN,stroke_width=6) for x in [-1,.1,1.2,2.3]])
        self.add(skin,ending,label('injured tissue',-3.7,-2.6,28,RED),cd)
        def response(y,n):
            # Constant stimulus, event count = floor(rate * one schematic window).
            return VGroup(Line([.2,y,0],[4.1,y,0],color=GREY),
                *[Line([x,y,0],[x,y+.55,0],color=PAIN,stroke_width=5) for x in np.linspace(.5,3.8,n)])
        before=response(1.35,2);state=label('before',.9,2.2,28)
        self.add(before,label('same small stimulus',-2.7,1.7,28,SIG),state,label('schematic response',1.8,3.15,26))
        self.at('First');turn(self,cd,2.8,.5)
        self.at('Injured tissue');self.play(Indicate(skin,color=RED,scale_factor=1.01),run_time=.6)
        self.at('such as bradykinin');b=box('bradykinin',-3,.2,RED,28);h=box('protons (H+)',.2,.2,RED,28)
        self.play(FadeIn(b),FadeIn(h),run_time=.5)
        self.at('which sensitize');self.play(b.animate.move_to([-1.1,-1.95,0]),h.animate.move_to([2,-2.65,0]),run_time=.5)
        self.play(Transform(before,response(1.35,6)),Transform(state,label('after',.9,2.2,28)),FadeIn(label('easier to fire',1.5,.65,28,PAIN)),run_time=.6)
        flow(self,ending[0],1.6);self.wait(2.1);self.finish()

class S06Horn(SpokenScene):
    def construct(self):
        cd=cornerdial('dorsal horn')
        cord=Ellipse(width=8.6,height=5.5,color=GREY,fill_color=GREY,fill_opacity=.08).move_to([-.7,-.4,0])
        # Closed butterfly-shaped grey matter with a labelled dorsal projection.
        inner=Polygon(*[[x,y,0] for x,y in [(-3,1.5),(-1.6,.5),(-.7,.25),(.2,.5),(1.6,1.5),(.9,-.1),(1.6,-1.8),(.1,-.8),(-.7,-.65),(-1.5,-.8),(-3,-1.8),(-2.3,-.1)]],
            color=GREY,fill_color=GREY,fill_opacity=.24)
        cell=box('pain relay',1,-.35,PAIN,30)
        touch=arr((-4.7,1),(-1.5,1),TOUCH,8)
        damping=inhibit((-1.5,1),(cell.get_left()[0],-.35))
        marker=Line([-2.3,2.5,0],[-2.2,1.05,0],color=GREY)
        self.add(cord,inner,cd,label('dorsal horn',-2.3,2.85,32),marker)
        self.at('Second');turn(self,cd,.5,.5)
        self.at('Here');self.play(GrowArrow(touch),Create(damping),FadeIn(cell),FadeIn(label('touch input',-3.3,1.5,28,TOUCH)),run_time=.55)
        flow(self,touch,1.3);breathe(cell[0]);self.finish()

class S07Shin(SpokenScene):
    def construct(self):
        # Tapered calf and ankle continue into a heel, instep and toes.
        leg=Polygon(*[[x,y,0] for x,y in [(-4.8,2.8),(-3.4,2.8),(-3.05,2.15),(-3.2,1.3),(-3.45,.3),(-3.65,-1.7),(-3.1,-2.05),(-2.5,-2.2),(-2.35,-2.65),(-4.25,-2.65),(-4.6,-2.25),(-4.35,-1.7),(-4.55,.1),(-4.95,1.5)]],
            color=GREY,fill_color=GREY,fill_opacity=.16)
        knee=Arc(radius=.5,start_angle=PI,angle=PI,color=GREY).move_to([-4.1,2.1,0])
        spot=Dot([-3.5,-.7,0],radius=.24,color=RED)
        # Continuous palm/finger/thumb silhouette, fingers resting on adjacent skin.
        hand=Polygon(*[[x,y,0] for x,y in [(-1.3,.25),(-2.1,.35),(-2.65,.85),(-3.2,1.18),(-3.42,1.12),(-3.35,.92),(-2.9,.55),(-3.48,.78),(-3.65,.68),(-3.6,.51),(-3,.25),(-3.55,.38),(-3.7,.23),(-3.6,.06),(-3.02,-.02),(-3.48,-.08),(-3.53,-.25),(-3.32,-.36),(-2.55,-.35),(-2.85,-.68),(-2.7,-.85),(-2.42,-.76),(-1.95,-.4),(-1.3,-.35)]],
            color=TOUCH,fill_color=TOUCH,fill_opacity=.3)
        rub=Dot([-3.45,.55,0],radius=.11,color=TOUCH)
        fibre=VMobject(color=TOUCH,stroke_width=5).set_points_as_corners([[-3.45,.55,0],[-2.1,1.65,0],[3.5,1.65,0],[3.5,2.4,0]])
        b=painbar(2.5,-.45,.9)
        self.add(leg,knee,b,label('shin',-4.2,3.25,30))
        self.at('Bang your shin');self.play(FadeIn(spot),run_time=.4)
        self.at('you rub it');self.play(FadeIn(hand),FadeIn(rub),run_time=.4)
        self.at('gentle rubbing');self.play(hand.animate.shift(UP*.22),run_time=.35)
        self.at('mainly excites');self.play(Create(fibre),FadeIn(label('touch fibres → cord',1,2.45,30,TOUCH)),
            FadeIn(label('model assumption:',1.6,-1.9,28)),FadeIn(label('nociceptor input held fixed',1.6,-2.5,28)),run_time=.45)
        flow(self,fibre,1.1)
        self.play(hand.animate.shift(DOWN*.22),setbar(b,.25),run_time=.45)
        self.at('It hurts less');self.play(Indicate(b[1],color=PAIN,scale_factor=1.03),run_time=.3)
        self.finish()

class S08Mw(SpokenScene):
    def construct(self):
        names=label('Ronald Melzack  •  Patrick Wall',0,2.4,38)
        theory=box('Gate control theory',0,-.1,PAIN,42)
        self.add(names,theory,label('Science, 1965',0,1.25,32,SIG))
        route=Line([-4,-2,0],[4,-2,0],color=PAIN,stroke_width=7)
        gate=VGroup(Line([0,-2.6,0],[0,-1.4,0],color=GREEN,stroke_width=10),label('spinal gate',0,-3.1,28,GREEN))
        self.add(route,gate);flow(self,route,2.5)
        self.at('Ronald');self.play(Indicate(names,scale_factor=1.02),run_time=.7)
        self.at('proposed a gate');self.play(Indicate(theory,color=SIG,scale_factor=1.03),run_time=.7)
        self.finish()

class S09Cells(SpokenScene):
    def construct(self):
        g=Gate(False);self.add(g.touch,g.pain)
        self.at('Picture two cells');self.play(Create(g.direct[0]),Create(g.pdirect[0]),run_time=.7)
        flow(self,g.touch[0],1.6)
        self.at('A transmission cell');self.play(FadeIn(g.t),FadeIn(g.direct[1]),FadeIn(g.pdirect[1]),run_time=.55)
        self.at('sends the signal up');self.play(GrowArrow(g.up),run_time=.5)
        self.at('excited by both');self.play(Indicate(g.touch,color=TOUCH),Indicate(g.pain,color=PAIN),run_time=.8)
        flow(self,g.pain[0],1.8);self.finish()

class S10Inter(SpokenScene):
    def construct(self):
        g=Gate(False);self.add(g.base)
        self.at('An inhibitory interneuron');self.play(FadeIn(g.i),run_time=.5)
        self.at('damps that cell');self.play(Create(g.it),run_time=.6)
        self.at('Touch');self.play(Create(g.ti),run_time=.6);flow(self,g.ti[0],1.6)
        self.at('Pain');self.play(Create(g.pi),run_time=.6)
        self.finish()

class S11Rub(SpokenScene):
    def construct(self):
        g=Gate();self.add(g.all)
        self.at('rubbing adds damping');self.play(g.touch[0].animate.set_stroke(width=15),g.i[0].animate.set_fill(GREEN,.35),run_time=.6)
        flow(self,g.ti[0],1.1)
        self.at('signal goes up');self.play(Transform(g.up,arr((3,g.t.get_top()[1]),(3,2.95),PAIN,4)),FadeIn(label('less signal',4.8,3,28,PAIN)),run_time=.55)
        self.finish()

class S12Cond(SpokenScene):
    def construct(self):
        g=Gate();self.add(g.all)
        self.at('touch also excites');self.play(g.direct[0].animate.set_stroke(width=10),run_time=.6)
        flow(self,g.direct[0],1.6)
        self.at('transmission cell directly');self.play(Indicate(g.t,scale_factor=1.03),run_time=.6)
        self.at('Rubbing helps only');self.play(g.ti[0].animate.set_stroke(width=10),g.it[0].animate.set_stroke(width=10),run_time=.55)
        flow(self,g.ti[0],1.3);flow(self,g.it[0][0],1.3)
        self.at('added damping wins');self.play(FadeIn(condition()),run_time=.45)
        self.finish()

class S12Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        g=Gate();g.direct[0].set_stroke(width=10);g.ti[0].set_stroke(width=10);g.it[0].set_stroke(width=10)
        self.add(g.all,condition());flow(self,g.direct[0],1.6);flow(self,g.ti[0],1.3);flow(self,g.it[0][0],1.3);self.wait(1.5)

class S12bHistory(SpokenScene):
    def construct(self):
        h=history_panel(-3.15);m=history_panel(3.15,True);self.add(h,m)
        self.at('In their');self.play(h[0].animate.set_color(SIG),run_time=.6)
        flow(self,h[2][0],1.6);flow(self,m[2][0],1.6)
        self.at('damping acted');self.play(Indicate(h[7],color=GREEN,scale_factor=1.03),run_time=.7)
        self.at('incoming fibers themselves');self.play(Indicate(h[3],color=SIG),run_time=.7)
        self.at('This circuit');self.play(h[0].animate.set_color(GREY),m[0].animate.set_color(SIG),run_time=.6)
        self.at('a simplified version');self.play(Indicate(m[7],color=GREEN,scale_factor=1.03),run_time=.6)
        self.finish()

class S13Predict(SpokenScene):
    def construct(self):
        g=Gate();self.add(g.all)
        self.at('remove the inhibitory');self.play(FadeOut(g.inhib),run_time=.7)
        self.at('What does a light touch');pulse=Dot(g.touch[0].get_start(),radius=.14,color=SIG);self.add(pulse)
        self.play(FadeIn(question()),pulse.animate.move_to([-1.8,1.8,0]),run_time=1,rate_func=linear)
        self.finish()

class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(Gate(False).all,question(),Dot([-1.8,1.8,0],radius=.14,color=SIG),label('Pause and predict',-.3,-.7,28,SIG))
        ring=Circle(.42,color=GREY).move_to([5,-.7,0]);dot=Dot([5.42,-.7,0],color=SIG,radius=.08)
        self.add(ring,dot);self.play(Rotate(dot,-TAU,about_point=ring.get_center()),run_time=5,rate_func=linear)

class S15Reveal(SpokenScene):
    def construct(self):
        g=Gate(False);q=question();self.add(g.all,q)
        self.at('Nothing damps touch');self.play(Transform(q,label('Nothing damps touch now',0,-3.25,32)),run_time=.5)
        flow(self,g.touch[0],1.5)
        self.at('Touch alone can drive');self.play(Transform(q,label('Touch alone now drives the cell',0,-3.25,32)),run_time=.45)
        d=Dot([-3.5,1.8,0],radius=.14,color=SIG);self.add(d)
        self.play(d.animate.move_to(g.t.get_left()),run_time=.8)
        self.play(FadeOut(d),g.t[0].animate.set_fill(PAIN,.3),run_time=.3)
        self.at('sending a signal up');self.play(g.up.animate.set_stroke(width=20),run_time=.6)
        flow(self,g.up,1.2);self.finish()

class S16Duan(SpokenScene):
    def construct(self):
        self.add(label('Duan and colleagues • 2014 • mice',0,3.2,34))
        horn=RoundedRectangle(width=10.3,height=5.4,corner_radius=.65,color=GREY).move_to([0,-.2,0])
        cells=VGroup(*[Circle(.38,color=GREEN,fill_color=GREEN,fill_opacity=.5).move_to([x,y,0]) for x,y in [(-3,.6),(0,.6),(3,.6),(-1.5,-1.4),(1.5,-1.4)]])
        neutral=VGroup(*[Circle(.3,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([x,y,0]) for x,y in [(-3,-1.3),(3,-1.3),(-1.5,.5),(1.5,.5)]])
        self.add(horn,cells,neutral,label('dynorphin-lineage inhibitory neurons',0,2.15,30,GREEN),label('mouse dorsal horn',0,-3.25,28))
        self.at('and colleagues');self.play(Indicate(cells,color=GREEN,scale_factor=1.03),run_time=.6)
        self.at('removed inhibitory neurons');self.play(cells.animate.set_color(GREY).set_opacity(.35),run_time=.6)
        crosses=VGroup(*[Cross(c,stroke_color=RED,stroke_width=4) for c in cells])
        self.play(Create(crosses),FadeIn(label('removed',0,-.45,30,RED)),run_time=.45)
        self.at('of the');self.play(Indicate(self.mobjects[4],color=GREEN,scale_factor=1.01),run_time=.6)
        breathe(horn);self.finish()

class S17Duan2(SpokenScene):
    def construct(self):
        foot,probe,mesh=paw();self.add(foot,probe,mesh,label('mouse hind paw',-3.7,3.5,30))
        self.at('light touch evoked');self.play(probe.animate.shift(UP*.1),run_time=.3)
        self.at('withdrawal');self.play(foot.animate.shift(UP*.65),GrowArrow(arr((-2.4,.7),(-1.6,1.7),PAIN,7)),FadeIn(label('withdrawal',-.5,2.1,28,PAIN)),run_time=.5)
        self.at('Touch input')
        circuit=mouse_circuit(3.25,.2)
        self.play(FadeIn(circuit),FadeIn(label('circuit interpretation',3.1,3.05,28)),run_time=.6)
        self.add(label('behavioural sign of allodynia (mice, this assay)',0,-3.35,28,PAIN))
        flow(self,circuit[0],1.3);self.finish()


class S17bScope(SpokenScene):
    def construct(self):
        hist=scope_history(-3.2)
        mouse=mouse_circuit(3.2,-.8,scope=True)
        self.add(hist,mouse,label('One form of spinal gating in mice',0,3.15,34),
            label('Melzack & Wall, 1965',-3.2,1.05,28),label('Mouse result',3.2,1.05,28))
        self.at('That tests one form');self.play(Indicate(mouse[1],color=PAIN,scale_factor=1.03),run_time=.6)
        flow(self,mouse[0],1.6)
        self.at('not the');self.play(FadeIn(label('Not proof of the 1965 diagram as drawn',0,2.3,30,TEXT)),run_time=.6)
        self.finish()


class S18Stem(SpokenScene):
    def construct(self):
        cd=cornerdial('brainstem');self.add(cd)
        pg=box('periaqueductal gray',-.6,2.5,GREY,30)
        rvm=box('rostral ventromedial medulla',-.6,.4,GREY,30)
        dh=box('dorsal horn',-.6,-2.4,PAIN,32)
        self.add(pg,rvm,dh)
        self.at('Third');turn(self,cd,.5,.5)
        self.at('It projects down');a=arr((-.6,pg.get_bottom()[1]),(-.6,rvm.get_top()[1]),GREY);b=arr((-.6,rvm.get_bottom()[1]),(-.6,dh.get_top()[1]),GREY)
        self.play(GrowArrow(a),GrowArrow(b),run_time=.65);flow(self,b,1.7)
        self.at('can turn its signals');self.play(FadeIn(label('turn signals up / down',2.5,-1.05,28)),
            GrowArrow(arr((-1.15,-1.5),(-1.15,-.75),PAIN)),GrowArrow(arr((-.05,-.75),(-.05,-1.5),GREEN)),b.animate.set_stroke(width=9),run_time=.65)
        self.finish()

# Qualitative rate model in a normalised time window: baseline 1/0.7,
# ON burst 1/0.17 for -1.6<t<0, OFF rate 0 there; both recover after t=0.
def raster_events(on):
    return np.r_[np.arange(-6.2,-1.6,.7),np.arange(-1.6,0,.17) if on else [],np.arange(.35,2.5,.7)]


def spikes(y,on,baseline=False):
    times=np.arange(-6.2,2.5,.7) if baseline else raster_events(on)
    return VGroup(*[Line([t+3.2,y-.48,0],[t+3.2,y+.48,0],color=PAIN if on else GREEN,stroke_width=4) for t in times])

class S19Onoff(SpokenScene):
    def construct(self):
        axis=arr((-3.3,-2.6),(5.8,-2.6),GREY,3)
        event=DashedLine([3.2,-2.6,0],[3.2,2.65,0],color=GREY)
        self.add(label('Rodents • schematic spike timing',-1,3.45,30),axis,event,
            label('withdrawal',3.2,-3.18,26),label('time',5.5,-3.18,26),label('before',-.7,-3.18,26))
        flow(self,axis,4,r=.07)
        on=spikes(1.65,True,True);off=spikes(-1.2,False,True)
        self.add(on,label('background rate',-1.15,2.5,26,PAIN))
        self.at('called on cells');self.play(FadeIn(label('ON cells',-4.9,1.65,30,PAIN)),run_time=.4)
        self.at('bursts just before');self.play(Transform(on,spikes(1.65,True)),Create(Line([1.6,2.45,0],[3.1,2.45,0],color=PAIN)),FadeIn(label('burst',2.3,2.85,26,PAIN)),run_time=.55)
        self.at('a withdrawal');self.play(FadeIn(off),FadeIn(label('background rate',-1.15,-.35,26,GREEN)),run_time=.5)
        self.add(label('returns to\nbaseline',4.65,.55,26))
        self.at('called off cells');self.play(FadeIn(label('OFF cells',-4.9,-1.2,30,GREEN)),run_time=.45)
        self.at('pauses just before');self.play(Transform(off,spikes(-1.2,False)),Create(Line([1.6,-.45,0],[3.1,-.45,0],color=GREEN)),FadeIn(label('pause',2.3,.0,26,GREEN)),run_time=.55)
        self.finish()

class S20Roles(SpokenScene):
    def construct(self):
        self.clear()
        stem=box('brainstem',0,2.65,GREY,34);horn=box('dorsal horn',0,-2.5,PAIN,34)
        self.add(stem,horn,label('classes defined by\nfiring pattern',3.9,2.65,26))
        off=VGroup(inhibit((-1,stem.get_bottom()[1]),(-1,horn.get_top()[1]),9),label('OFF cells',-3.6,.45,32,GREEN),label('turn down',-3.6,-.25,28,GREEN))
        on=VGroup(arr((1,stem.get_bottom()[1]),(1,horn.get_top()[1]),PAIN,9),label('ON cells',3.6,.45,32,PAIN),label('turn up',3.6,-.25,28,PAIN))
        self.at('Off cells suppress');self.play(Create(off),run_time=.7)
        breathe(off[0])
        self.at('on cells facilitate');self.play(Create(on),run_time=.7)
        self.at('Control runs both ways');self.play(horn[0].animate.set_fill(SIG,.25),run_time=.3);self.play(horn[0].animate.set_fill(BG,1),run_time=.3)
        self.finish()

class S21Evidence(SpokenScene):
    def construct(self):
        foot,probe,mesh=paw(x=-4.5,y=-.1)
        VGroup(foot,probe,mesh).scale(1.28,about_point=[-4.5,0,0])
        noc=box('nociception\n(neural encoding)',-.8,1.85,PAIN,28)
        pain=box('pain\n(an experience)',4.4,1.85,TEXT,28)
        self.add(foot,probe,mesh,label('mouse paw',-4.5,3.65,28))
        self.at('A withdrawing paw');self.play(foot.animate.shift(UP*.45),run_time=.5)
        self.at('indirect evidence');self.play(FadeIn(noc),GrowArrow(arr((-3.3,.4),(noc.get_left()[0],1.85),PAIN)),run_time=.6)
        self.at('By itself');self.play(FadeIn(pain),Create(DashedLine([noc.get_right()[0],1.85,0],[pain.get_left()[0],1.85,0],color=TEXT).add_tip(tip_length=.18)),FadeIn(label('?',2.2,2.5,36)),run_time=.6)
        self.at('does not show');self.play(FadeIn(label('A paw withdrawal is indirect evidence about pain',0,-3.25,28)),run_time=.6)
        self.finish()

class S22Takeaway(SpokenScene):
    def construct(self):
        ds=VGroup(*[dial(x,1.2,n,r=.9) for x,n in zip([-4,0,4],['ending','dorsal horn','brainstem'])])
        tags=VGroup(*[label(s,x,-.65,27,GREY) for x,s in zip([-4,0,4],['mediators','touch gate','ON / OFF cells'])])
        self.add(ds,tags)
        self.at('firing is');self.play(*[Rotate(d[1],2.8,about_point=d[0].get_center()) for d in ds],run_time=.55)
        self.at('a report');first=label('A nociceptor’s firing is a report.',0,-1.65,34,PAIN)
        self.play(FadeIn(first),*[Rotate(d[1],-2.8,about_point=d[0].get_center()) for d in ds],run_time=.7)
        self.at('Pain is what');self.play(first.animate.set_color(GREY),FadeIn(label('Pain is what the nervous system makes of it.',0,-2.65,32)),run_time=.6)
        self.finish()

class S23End(EndCard):
    LINE='Pain is what the nervous system makes of it.'
