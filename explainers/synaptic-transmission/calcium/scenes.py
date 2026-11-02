"""Calcium Sets the Count — reviewed animation.
COLOR MAP: BLUE terminal/action potential; YELLOW vesicles/transmitter;
GREEN response; TEAL calcium ions; PURPLE magnesium; GREY membranes/axes;
TEXT protein cartoons; GOLD slope/bend emphasis; RED reduced output.
All curves are computed: illustrative response (c/(1+c))^3.78,
and explicitly identified four-seat model (c/(1+c))^4. No measured dots.
"""
import os
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'


def label(s, x=0, y=0, color=TEXT, size=30):
    return T(s, size=size, color=color).move_to([x,y,0])


class Timed(SpokenScene):
    # Audio starts at scene time zero. No inherited lead or per-scene tail.
    def at(self, phrase, lead=0, nth=0):
        target = self.t_of(phrase, nth)
        if target-self.elapsed() > .001:
            self.wait(target-self.elapsed())
        with open('/tmp/calcium-sync.log', 'a') as f:
            f.write(f'{os.environ["KX_SCENE_ID"]}: {phrase}: {self.elapsed()-target:+.3f}\n')

    def finish(self):
        if self.narration_s > self.elapsed():
            self.wait(self.narration_s-self.elapsed())


def packet(radius=.16):
    return VGroup(*[Dot([radius*np.cos(a),radius*np.sin(a),0],radius=.07,color=YELLOW)
                    for a in np.linspace(0,2*PI,6,endpoint=False)],Dot(radius=.07,color=YELLOW))


def vesicle(x=0,y=.5,r=1):
    return VGroup(Circle(radius=r,color=YELLOW,stroke_width=5),packet(.32)).move_to([x,y,0])


def active(opened=True, docked=True, bound=False):
    membrane=VGroup(Line([-5.6,-1.65,0],[-3.3,-1.65,0],color=GREY,stroke_width=10),
                    Line([-2.3,-1.65,0],[5.6,-1.65,0],color=GREY,stroke_width=10))
    channel=VGroup(*[Rectangle(width=.22,height=1.1,color=TEXT,fill_opacity=.8).move_to([x,-1.65,0]) for x in (-3.3,-2.3)])
    if not opened: channel.add(Line([-3.3,-1.65,0],[-2.3,-1.65,0],color=TEXT,stroke_width=8))
    rng=np.random.default_rng(12)
    ions=VGroup(*[Dot([x,y,0],radius=.12,color=TEAL) for x,y in zip(rng.uniform(-5.1,5,26),rng.uniform(-3.05,-2.35,26))])
    names=VGroup(label('nerve terminal',3,2.75,BLUE,28),label('outside: high Ca²⁺',2.8,-3.3,TEAL,28),label('inside: low Ca²⁺',-3.7,.65,TEAL,28))
    v=vesicle(1,.0,1.45) if docked else VGroup()
    sensor=RoundedRectangle(width=.95,height=.65,corner_radius=.12,color=TEAL if bound else TEXT,fill_color=TEAL if bound else TEXT,fill_opacity=.35).move_to([1.8,-1.1,0])
    return VGroup(membrane,channel,ions,names,v,sensor)


def response(c,n=3.78,mg=False):
    c=np.asarray(c)/(2.5 if mg else 1)
    return (c/(1+c))**n


def plot(n=3.78,partial=False,panel=False):
    left,bottom=(.6,-2.5) if panel else (-3.65,-2.6)
    w,h=(4.7,4.9) if panel else (5.8,5.7)
    ax=Axes(x_range=[-2,1,1],y_range=[-8,.5,2],x_length=w,y_length=h,tips=False,
            axis_config={'color':GREY,'include_ticks':False})
    ax.shift(np.array([left,bottom,0])-ax.c2p(-2,-8))
    ticks=VGroup()
    for x,t in [(-2,'0.01'),(-1,'0.1'),(0,'1'),(1,'10')]:
        p=ax.c2p(x,-8); ticks.add(Line(p+UP*.07,p+DOWN*.07,color=GREY),label(t,p[0],bottom-.28,size=26))
    for y,t in [(-8,'10⁻⁸'),(-4,'10⁻⁴'),(0,'1')]:
        p=ax.c2p(-2,y);ticks.add(Line(p+LEFT*.07,p+RIGHT*.07,color=GREY),label(t,left-.70,p[1]+(.13 if y==-8 else 0),size=26))
    title='Four-seat model' if n==4 else 'Illustrative curve • low-Ca slope → 3.78'
    names=VGroup(label(title,2.1 if panel else 0,3.43,size=28),
                 label('calcium • log scale',left+w/2,bottom-.78,size=26),
                 (label('response • log scale',2.9,2.93,size=26) if panel else label('response • log scale',-6.05,bottom+h/2,size=26).rotate(PI/2)))
    def line(lo=-2,hi=1,color=GREEN,mg=False):
        xs=np.linspace(lo,hi,240)
        return VMobject(stroke_color=color,stroke_width=5).set_points_as_corners([ax.c2p(x,np.log10(response(10**x,n,mg))) for x in xs])
    axes=VGroup(Line(ax.c2p(-2,-8),ax.c2p(1,-8),color=GREY),Line(ax.c2p(-2,-8),ax.c2p(-2,.5),color=GREY))
    g=VGroup(axes,ticks,names,line(hi=-.65 if partial else 1))
    return ax,g,line


def dot_at(ax,x,n=3.78):
    return Dot(ax.c2p(x,np.log10(response(10**x,n))),radius=.085,color=GREEN)


def triangle(ax,n=3.78,x=-1.65,y=None,color=GOLD,small=False):
    y=np.log10(response(10**x,n)) if y is None else y
    run=.65 if small else 1
    a,b,c=ax.c2p(x,y),ax.c2p(x+run,y),ax.c2p(x+run,y+n*run)
    return VGroup(Line(a,b,color=color),Line(b,c,color=color),
        label('1 log unit' if not small else 'same run',(a[0]+b[0])/2,a[1]-.48,color,26),
        label('≈4 log units' if not small else 'same rise',c[0]+1.4,(b[1]+c[1])/2,color,26))


def side(lines,color=TEXT):
    return VGroup(*[label(t,4.25,1.85-i*.6,color,30) for i,t in enumerate(lines)])


def prediction(answer=False):
    ax,g,line=plot()
    x0=-1.5;x1=x0+np.log10(2)
    y0=np.log10(response(10**x0));y1=np.log10(response(10**x1))
    p,q=ax.c2p(x0,y0),ax.c2p(x1,y1)
    # Magnified brackets preserve the actual axis positions and log distance.
    marks=VGroup(dot_at(ax,x0),dot_at(ax,x1),DashedLine(ax.c2p(x0,-8),p,color=GREY),DashedLine(ax.c2p(x1,-8),q,color=GREY))
    bracket=VGroup(Line(ax.c2p(x0,-7.7),ax.c2p(x1,-7.7),color=GOLD,stroke_width=5),
        label('1×',p[0]-.45,-2.03,GOLD,26),label('2×',q[0]+.35,-2.03,GOLD,26))
    jump=VGroup(Arrow([q[0]+.23,p[1],0],[q[0]+.23,q[1],0],buff=0,color=GREEN,stroke_width=5),
        label('×14' if answer else '? times',q[0]+1.1,(p[1]+q[1])/2,GREEN,30))
    question=side(['Double calcium.', 'How much more', 'transmitter?'])
    return ax,VGroup(g,marks,bracket,jump,question)


def seats(filled=0,mg=False,panel=False):
    xs=np.linspace(-5.2,-1.5,4) if panel else np.linspace(-3.6,3.6,4)
    cx=-3 if panel else 0
    cups=VGroup(); ions=VGroup()
    for i,x in enumerate(xs):
        width=.43 if panel else .75
        cups.add(VMobject(color=GREY,stroke_width=6).set_points_as_corners([[x-width,-.4,0],[x-width,-1.35,0],[x+width,-1.35,0],[x+width,-.4,0]]))
        if i<filled: ions.add(Dot([x,-.83,0],radius=.27 if panel else .4,color=PURPLE if mg and i in (1,3) else TEAL))
    membrane=Line([xs[0]-.8,-1.7,0],[xs[-1]+.8,-1.7,0],color=GREY,stroke_width=8)
    v=vesicle(cx,1.15,1.25)
    return VGroup(cups,ions,membrane,v)


def fuse(scene,s,panel=False):
    cx=-3 if panel else 0
    # The docked vesicle and fusion arch stay above the illustrative seats.
    scene.play(s[3].animate.move_to([cx,.95,0]),run_time=.2)
    arch=Arc(radius=1.25,start_angle=0,angle=PI,color=YELLOW,stroke_width=6).shift([cx,-.25,0])
    dots=VGroup(*[packet().move_to([cx+dx,-2.05,0]) for dx in (-.7,0,.7)])
    split=VGroup(Line(s[2].get_left(),[cx-1.25,-1.7,0],color=GREY,stroke_width=8),Line([cx+1.25,-1.7,0],s[2].get_right(),color=GREY,stroke_width=8))
    scene.play(Transform(s[2],split),ReplacementTransform(s[3],arch),FadeIn(dots),FadeIn(label('fuses',cx,1.55,YELLOW,32)),run_time=.25)
    scene.play(dots.animate.shift(DOWN*.35),run_time=.3)


class S00Title(TitleCard):
    TITLE='Calcium Sets the Count'
    LESSON='Synaptic Transmission and Quantal Release'
    finish=Timed.finish

class S01Question(Timed):
    def construct(self):
        s=active(False);s.remove(s[5]);self.add(s)
        self.at('Why does a nerve')
        self.play(FadeIn(label('More calcium → more packets?',0,3.4,size=36)),FadeIn(label('?',1,1.9,YELLOW,64)),run_time=.4)
        self.at('more packets')
        self.play(Indicate(s[4],color=YELLOW),run_time=.5)
        self.finish()

class S02Channels(Timed):
    def construct(self):
        s=active(False);s.remove(s[5]);s[3].remove(s[3][2]);self.add(s)
        state=label('closed',-2.8,-.5,size=28);self.add(state)
        self.at('The action potential')
        pulse=VMobject(color=BLUE,stroke_width=6).set_points_as_corners([[-5,1,0],[-4.6,1,0],[-4.4,2,0],[-4.2,.5,0],[-4,1,0]])
        self.play(Create(pulse),FadeIn(label('action potential',-2,2.5,BLUE,30)),run_time=.25)
        self.play(pulse.animate.shift(RIGHT*1.6),run_time=.55)
        self.at('opens')
        self.play(Transform(s[1],active(True)[1]),Transform(state,label('open',-2.8,-.5,size=28)),FadeOut(pulse),run_time=.45)
        self.at('calcium channels')
        self.play(FadeIn(VGroup(label('voltage-gated',-3,1.5,size=30),label('calcium channel',-3,.85,size=30))),run_time=.3)
        self.finish()

class S03Inflow(Timed):
    def construct(self):
        s=active(True,False);s.remove(s[5]);self.add(s)
        self.at('Calcium flows in')
        ions=VGroup(*[Dot([-2.8+dx,-2.5,0],radius=.13,color=TEAL) for dx in (-.25,0,.25)])
        self.add(ions)
        self.play(ions.animate.move_to([-2.8,-.5,0]),run_time=1.1)
        self.at('down a steep gradient')
        more=ions.copy().shift(DOWN*2);self.add(more)
        self.play(more.animate.shift(UP*2),ions.animate.shift(UP*.6+RIGHT*.5),run_time=.8)
        self.finish()

class S04Primed(Timed):
    def construct(self):
        s=active();s.remove(s[5]);self.add(s)
        self.at('Nearby vesicles')
        self.play(Indicate(s[4],color=YELLOW),run_time=.6)
        self.at('docked and primed')
        self.play(FadeIn(label('docked and primed',2.8,2,YELLOW,32)),run_time=.4)
        self.finish()

class S05Sensor(Timed):
    def construct(self):
        s=active();self.add(s)
        self.at('Calcium binds')
        ion=Dot([-2.8,-.5,0],radius=.17,color=TEAL);self.add(ion)
        self.play(ion.animate.move_to([1.8,-1.1,0]),run_time=.9)
        self.play(s[5].animate.set_color(TEAL),run_time=.25)
        self.at('sensor protein')
        self.play(FadeIn(label('synaptotagmin',4.1,1.8,size=30)),FadeIn(label('calcium sensor',4.1,1.2,TEAL,28)),Create(Line([3.3,.7,0],[2.2,-.8,0],color=GREY)),run_time=.4)
        self.finish()

class S06Snare(Timed):
    def construct(self):
        membrane=Line([-5.5,-1.65,0],[5.5,-1.65,0],color=GREY,stroke_width=10)
        v=vesicle(0,1.4,1.1)
        v.add(RoundedRectangle(width=.6,height=.4,corner_radius=.07,color=TEXT).move_to([.65,.65,0]),Dot([.65,.65,0],radius=.16,color=TEAL))
        sensor=chip('Ca-bound sensor',TEAL,26).move_to([3,1.4,0])
        link=always_redraw(lambda: Line(v[2].get_right(),sensor.get_left(),color=TEAL))
        self.add(membrane,v,sensor,link)
        rod_width=ValueTracker(1)
        def snare_rods():
            top=v[0].get_bottom()[1]
            bottom=-1.65
            return VGroup(*[Rectangle(width=.18,height=top-bottom,color=TEXT,fill_opacity=.5).move_to([x*rod_width.get_value(),(top+bottom)/2,0]) for x in (-.65,-.22,.22,.65)])
        rods=always_redraw(snare_rods)
        self.at('the snare proteins')
        rod_label=label('SNARE rods',3,-.4,size=30)
        self.play(FadeIn(rods),FadeIn(rod_label),run_time=.4)
        self.at('finish zipping')
        for k in range(3):
            self.play(rod_width.animate.set_value(.8**(k+1)),v.animate.shift(DOWN*.18),run_time=.22)
        self.at('They pull the vesicle')
        self.play(v.animate.shift(DOWN*.9),rod_width.animate.set_value(.35),run_time=.8)
        self.at('into one')
        arch=Arc(radius=1.1,start_angle=0,angle=PI,color=YELLOW,stroke_width=6).move_to([0,-1.1,0])
        p=VGroup(*[packet().move_to([x,-1.5,0]) for x in (-.7,0,.7)])
        self.play(Transform(membrane,VGroup(Line([-5.5,-1.65,0],[-1.1,-1.65,0],color=GREY,stroke_width=10),Line([1.1,-1.65,0],[5.5,-1.65,0],color=GREY,stroke_width=10))),ReplacementTransform(v,arch),FadeOut(rods),FadeOut(rod_label),FadeOut(link),FadeOut(sensor),FadeIn(p),FadeIn(label('packet released',3,-2.5,YELLOW,34)),run_time=.25)
        self.play(p.animate.shift(DOWN*1.3),run_time=.45)
        self.finish()

class S07Needs(Timed):
    def construct(self):
        terminal=RoundedRectangle(width=10.8,height=1.5,color=BLUE,stroke_width=5).move_to([0,1.9,0])
        lever=Line([-4,-1.5,0],[4,-1.5,0],color=GREY,stroke_width=9)
        pivot=Triangle(color=GREY,fill_color=GREY,fill_opacity=.5).scale(.48).move_to([0,-2.1,0])
        ca=VGroup(*[Dot([x,y,0],radius=.22,color=TEAL) for x,y in [(-3,-1.1),(-3.55,-.65),(-2.45,-.65)]])
        self.add(terminal,label('nerve terminal',0,1.9,BLUE,34),lever,pivot,label('Release',0,3.25,size=40))
        self.at('calcium outside')
        self.play(FadeIn(ca),FadeIn(label('calcium needed',-3,.4,TEAL,32)),FadeIn(label('outside the terminal',0,-3.1,size=30)),run_time=.4)
        self.at('Magnesium opposes it')
        mg=VGroup(*[Dot([x,y,0],radius=.22,color=PURPLE) for x,y in [(3,-1.1),(3.55,-.65),(2.45,-.65)]])
        self.play(FadeIn(mg),FadeIn(label('magnesium opposes',3,.4,PURPLE,32)),run_time=.5)
        self.finish()

class S08Dr(Timed):
    def construct(self):
        nerve=Line([-5,2,0],[-2,2,0],color=BLUE,stroke_width=12)
        terminal=RoundedRectangle(width=2.5,height=1.2,color=BLUE).move_to([-2,1.6,0])
        muscle=RoundedRectangle(width=5,height=1.2,color=GREEN).move_to([-3,-.3,0])
        self.add(nerve,terminal,muscle,label('nerve',-4,2.6,BLUE,28),label('muscle',-3,-.3,GREEN,28))
        self.at('Dodge and')
        self.play(FadeIn(label('F. A. Dodge',2.8,1.8,size=36)),FadeIn(label('Rami Rahamimoff',2.8,.9,size=34)),run_time=.5)
        self.at('at the frog junction')
        self.play(FadeIn(label('frog neuromuscular junction',0,-1.6,size=32)),run_time=.4)
        self.at('in')
        self.play(Create(Line([-5,-2.7,0],[5,-2.7,0],color=GREY)),FadeIn(label('1967',0,-2.7,GOLD,42).add_background_rectangle(color=BG,buff=.2)),run_time=.4)
        self.finish()

class S09Axes(Timed):
    def construct(self):
        ax,g,line=plot();self.add(g[:3],dot_at(ax,-1.9))
        self.at('They changed calcium')
        self.play(FadeIn(dot_at(ax,-1.65)),run_time=.3)
        self.at('plotted the response')
        self.play(FadeIn(dot_at(ax,-1.4)),FadeIn(side(['Schematic of the', 'Dodge–Rahamimoff', 'result (1967)'])),run_time=.4)
        self.at('both on log scales')
        self.play(Indicate(g[1],color=GOLD),run_time=.6)
        self.finish()

class S10Steep(Timed):
    def construct(self):
        ax,g,line=plot(partial=True);self.add(g[:3],dot_at(ax,-1.9),dot_at(ax,-1.65))
        self.at('the points fall')
        self.play(LaggedStart(*[FadeIn(dot_at(ax,x)) for x in np.linspace(-1.4,-.65,5)],lag_ratio=.18),Create(g[3]),run_time=1.1)
        self.at('Its slope is near')
        self.play(Create(triangle(ax)),FadeIn(side(['Reported slope', '3.78 at low calcium', 'frog • 1967'],GREEN)),FadeIn(label('slope ≈4',-2.1,1.25,GOLD,30)),run_time=.5)
        self.finish()

class S11Bend(Timed):
    def construct(self):
        ax,g,line=plot(partial=True);self.add(g)
        self.at('As calcium nears')
        self.play(LaggedStart(*[FadeIn(dot_at(ax,x)) for x in np.linspace(-.5,1,8)],lag_ratio=.2),Create(line(-.65,1)),run_time=1.7)
        p=ax.c2p(0,np.log10(response(1)))
        self.play(Create(DashedLine(ax.c2p(0,-8),p,color=GOLD)),FadeIn(VGroup(label('normal calcium',4,.4,GOLD,30),Arrow([3.4,.05,0],p,buff=.1,color=GOLD))),run_time=.4)
        self.at('the line bends over')
        self.play(Create(line(-.25,1,color=GOLD)),run_time=.5)
        self.finish()

class S12Power(Timed):
    def construct(self):
        ax,g,line=plot();self.add(g,triangle(ax))
        self.at('release')
        self.play(FadeIn(side(['release ∝ [Ca]⁴', 'roughly, on the', 'steep part'],GREEN)),run_time=.4)
        self.at('roughly as the fourth power')
        self.play(Indicate(g[3],scale_factor=1),run_time=.5)
        self.finish()

class S13Predict(Timed):
    def construct(self):
        ax,g=prediction();self.add(g[0])
        self.at('double the calcium')
        self.play(FadeIn(g[1]),FadeIn(g[2]),FadeIn(g[3]),run_time=.5)
        self.at('How much more transmitter')
        self.play(FadeIn(g[4]),run_time=.4)
        self.finish()

class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        ax,g=prediction();self.add(g,label('Pause and guess',4.2,-1.4,GOLD,32))
        self.wait(5)

class S15Reveal(Timed):
    def construct(self):
        ax,g=prediction();self.add(g)
        self.at('far more than double')
        self.play(Transform(g[4],side(['Far more', 'than double.'],GREEN)),run_time=.4)
        self.at('With their measured slope')
        self.play(Transform(g[4],VGroup(label('2³·⁷⁸ ≈ 14',4.2,1.5,GREEN,48))),run_time=.4)
        self.at('about fourteen times')
        ax,new=prediction(True)
        g[3].become(new[3])
        self.play(Indicate(g[3][0],scale_factor=1.03),run_time=.4)
        self.finish()

class S16Modest(Timed):
    def construct(self):
        ax,g=prediction(True);g.remove(g[4]);self.add(g)
        self.at('a modest loss')
        self.play(FadeIn(side(['Less calcium', '2× → 1×'],TEXT)),run_time=.4)
        self.at('cut release sharply')
        x=-1.5+np.log10(2);y0=np.log10(response(10**-1.5));y1=np.log10(response(10**x))
        drop=Arrow(ax.c2p(x+.12,y1),ax.c2p(x+.12,y0),buff=0,color=GREEN,stroke_width=7)
        self.play(Transform(g[3],VGroup(drop,label('÷14',-1.1,-.4,GREEN,34))),FadeIn(label('≈14× less release',4.1,-.7,GREEN,30)),run_time=.5)
        self.finish()

class S17Seats(Timed):
    def construct(self):
        ax,g,line=plot();self.add(g)
        self.at('Why so steep')
        self.play(Indicate(g[3],scale_factor=1),run_time=.5)
        self.at('Picture four seats')
        self.play(FadeOut(g),FadeIn(seats()),FadeIn(label('One release site • four-seat picture',0,3.3,size=34)),run_time=.5)
        self.finish()

class S18Allfour(Timed):
    def construct(self):
        s=seats();self.add(s)
        self.at('In this picture')
        caption=label('A picture, not a measured count of sites',0,3.3,size=30)
        self.play(FadeIn(caption),run_time=.4)
        self.wait(.8)
        self.play(FadeOut(caption),run_time=.3)
        self.at('all four seats')
        self.play(FadeIn(seats(4)[1]),run_time=.6)
        self.at('at once')
        fuse(self,s)
        self.finish()

class S19Rare(Timed):
    def construct(self):
        s=seats();self.add(s)
        self.at('At low calcium')
        self.play(FadeIn(label('low calcium',0,3.2,TEAL,34)),run_time=.3)
        self.at('each seat is rarely filled')
        tally=label('occupancy: 0 of 4',0,-2.9,size=30);self.add(tally)
        # Seeded Bernoulli occupancy: observable low occupancy, not a molecular count.
        rng=np.random.default_rng(19)
        for k in range(6):
            mask=rng.random(4)<.18
            ions=VGroup(*[Dot([x,-.83,0],radius=.4,color=TEAL) for x,on in zip(np.linspace(-3.6,3.6,4),mask) if on])
            tally.become(label(f'{sum(mask)} of 4 occupied   •   all four: 0 / {k+1} samples',0,-2.9,size=30))
            self.play(Transform(s[1],ions),run_time=.1)
            self.wait(.2)
        self.at('All four at once')
        for k in range(4):
            mask=rng.random(4)<.18
            ions=VGroup(*[Dot([x,-.83,0],radius=.4,color=TEAL) for x,on in zip(np.linspace(-3.6,3.6,4),mask) if on])
            tally.become(label(f'{sum(mask)} of 4 occupied   •   all four: 0 / {k+7} samples',0,-2.9,size=30))
            self.play(Transform(s[1],ions),run_time=.1)
            self.wait(.2)
        self.finish()

class S20Line(Timed):
    def construct(self):
        ax,g,line=plot(n=4);self.add(g[:3])
        self.at('release grows very steeply')
        self.play(Create(g[3]),run_time=1)
        self.at('On log scales')
        self.play(Create(line(-2,-.7,color=GOLD)),Create(triangle(ax,n=4)),FadeIn(side(['Approaches 4', 'at lowest calcium'],GOLD)),run_time=.5)
        self.at('straight line of slope')
        self.play(Indicate(g[3],scale_factor=1),run_time=.4)
        self.finish()

class S21Full(Timed):
    def construct(self):
        ax,g,line=plot(n=4,panel=True);s=seats(panel=True);self.add(g,s,label('high calcium',-3,3.2,TEAL,32))
        self.at('the seats fill up')
        self.play(FadeIn(seats(4,panel=True)[1]),run_time=.5)
        self.at('Adding more calcium cannot help much')
        fuse(self,s,True)
        bend=line(-.25,1,color=RED).set_stroke(width=9)
        self.play(FadeIn(VGroup(label('adding calcium',-3,-2.95,RED,28),label('cannot help much',-3,-3.45,RED,28))),Create(bend),run_time=.3)
        self.at('so the line bends over')
        self.play(Indicate(bend,color=RED,scale_factor=1.03),run_time=.5)
        self.finish()

class S22Notcount(Timed):
    def construct(self):
        ax,g,line=plot(n=4);self.add(g)
        self.at('A model like this')
        # The low-calcium portions are parallel in the asymptotic model.
        # A stronger magnesium condition makes the vertical separation readable.
        lower=line(-1.55,-.45,color=PURPLE,mg=True).set_stroke(width=6)
        def slope_mark(x,y,color):
            a=ax.c2p(x,y); b=ax.c2p(x+.36,y); c=ax.c2p(x+.36,y+1.44)
            return VGroup(Line(a,b,color=color,stroke_width=4),Line(b,c,color=color,stroke_width=4),Line(c,a,color=color,stroke_width=3))
        marks=VGroup(slope_mark(-1.38,-5.62,GOLD),slope_mark(-1.38,-7.12,PURPLE))
        self.at('Adding magnesium lowered')
        self.play(Create(lower),Create(marks),FadeIn(side(['more magnesium', 'lower response'],PURPLE)),FadeIn(label('same slope',-.25,-1.85,GOLD,30)),run_time=.5)
        self.at('without changing the slope')
        self.play(Indicate(marks,scale_factor=1.04),run_time=.4)
        self.finish()

class S23Mg(Timed):
    def construct(self):
        ax,g,line=plot(n=4,panel=True);s=seats(4,panel=True);self.add(g,s,label('Competition at seats',-3,3.1,size=30))
        self.at('magnesium')
        mg=VGroup(Dot([-4.7,.1,0],radius=.3,color=PURPLE),Dot([-.8,.1,0],radius=.3,color=PURPLE));self.play(FadeIn(mg),run_time=.3)
        self.at('competing with calcium')
        self.play(Transform(s[1],seats(4,mg=True,panel=True)[1]),mg.animate.shift(DOWN*.8),TransformFromCopy(line(-1.55,-.45),line(-1.55,-.45,color=PURPLE,mg=True)),run_time=.65)
        self.play(FadeOut(mg),FadeIn(VGroup(label('magnesium competes',-3,-2.7,PURPLE,28),label('response lower',-3,-3.3,PURPLE,28))),run_time=.3)
        self.finish()

class S24Shaped(Timed):
    def construct(self):
        ax,g,line=plot(n=4,panel=True);self.add(g)
        statement=VGroup(label('Slope describes a curve,',-3,2.6,size=28),label('not a count of sites.',-3,2,size=28));self.add(statement)
        self.at('the slope does not count binding sites')
        self.play(Indicate(statement,scale_factor=1.02),run_time=.4)
        self.at('Saturation')
        bend=ax.c2p(.2,np.log10(response(10**.2,4)))
        self.play(Create(line(-.25,1,color=GOLD)),FadeIn(chip('saturation',TEXT,28).move_to([-3,.6,0])),Create(Circle(radius=.34,color=GOLD,stroke_width=5).move_to(bend)),run_time=.5)
        self.at('calcium spread')
        channel=VGroup(Line([-5.3,-1,0],[-3.4,-1,0],color=GREY,stroke_width=8),Line([-2.9,-1,0],[-.8,-1,0],color=GREY,stroke_width=8))
        dots=VGroup(*[Dot([-3.15+np.sin(i*2.4)*(.2+.08*i),-1.25-.065*i,0],radius=.1,color=TEAL).set_opacity(1-i/34) for i in range(22)])
        self.play(FadeIn(channel),LaggedStart(*[FadeIn(d) for d in dots],lag_ratio=.02),FadeIn(chip('calcium spread',TEXT,28).move_to([-3,-3.35,0])),run_time=.65)
        self.finish()

class S25Reading(Timed):
    def construct(self):
        self.add(label('“four calcium ions”',0,2,TEAL,44))
        self.at('a reading of one curve')
        self.play(FadeIn(label('a reading of one curve',0,.75,size=40)),FadeIn(label('in one preparation',0,-.15,size=34)),run_time=.5)
        self.at('not a molecular fact')
        self.play(FadeIn(label('not a molecular fact',0,-1.7,GOLD,38)),run_time=.5)
        self.finish()

class S26Takeaway(Timed):
    def construct(self):
        xs=(-3.9,-1.3,1.3,3.9)
        def membrane(released):
            pieces=VGroup()
            left=-5.5
            for i,x in enumerate(xs):
                if i in released:
                    pieces.add(Line([left,-.9,0],[x-.78,-.9,0],color=GREY,stroke_width=9))
                    left=x+.78
            pieces.add(Line([left,-.9,0],[5.5,-.9,0],color=GREY,stroke_width=9))
            return pieces
        def state(released):
            return VGroup(*[(Arc(radius=.78,start_angle=0,angle=PI,color=YELLOW,stroke_width=6).shift([x,-.9,0]) if i in released else vesicle(x,-.05,.78)) for i,x in enumerate(xs)])
        bar=membrane(set());vs=state(set())
        ions=VGroup(*[Dot([-5.9+(i%3)*.25,-2.8+(i//3)*.3,0],radius=.12,color=TEAL) for i in range(9)])
        entry=Arrow([-5.65,-1.9,0],[-5.65,.1,0],buff=0,color=TEAL,stroke_width=6)
        state_label=label('normal calcium: packets released',0,1.7,YELLOW,34)
        self.add(bar,vs,ions,entry,label('calcium entry',-4.5,-3.35,TEAL,28))
        self.at('calcium is a steep dial')
        self.play(FadeIn(label('Calcium is a steep dial on the count.',0,3.15,TEAL,38)),run_time=.4)
        packets=VGroup(*[packet(.22).move_to([x,-1.5,0]) for x in xs])
        self.play(Transform(bar,membrane(set(range(4)))),Transform(vs,state(set(range(4)))),FadeIn(packets),FadeIn(state_label),run_time=.3)
        self.play(packets.animate.shift(DOWN*.8),run_time=.4)
        self.at('Lose some calcium entry')
        # One release remains visible throughout the reduced-entry comparison.
        one=packet(.22).move_to([xs[0],-2.3,0])
        self.play(Transform(bar,membrane({0})),Transform(vs,state({0})),Transform(packets,VGroup(one)),FadeOut(ions[3:]),Transform(entry,Arrow([-5.65,-1.9,0],[-5.65,-.75,0],buff=0,color=TEAL,stroke_width=4)),Transform(state_label,label('reduced calcium entry: few released',0,1.7,YELLOW,34)),run_time=.4)
        self.at('lose many packets')
        self.play(Indicate(packets,scale_factor=1.2),run_time=.4)
        self.finish()

class S27End(EndCard):
    LINE='Calcium is a steep dial on the count.'
    finish=Timed.finish
