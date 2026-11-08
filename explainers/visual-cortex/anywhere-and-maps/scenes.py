"""Anywhere in the Field, and Columns — review fix round.
COLOR MAP: BLUE cortical cells/spikes/tuning; YELLOW stimulus; GREEN ON/excitation;
RED OFF; PURPLE complex cells; ORANGE alternative input; GREY structure; GOLD title.
Orientation sheets use a cyclic hue key. All response traces are computed toy-model
illustrations, not recordings. Signed sum: six +1 ON squares, −0.5 OFF squares;
firing=max(0,sum−2). Pooling rectifies each sum before adding the responses.
"""
import colorsys
import numpy as np
from bp_style import *
PURPLE='#B58CD9'
ORANGE='#F29E4C'

class TimedSpoken(SpokenScene):
    # Keep the pipeline's cue matching without creating an unrequested sync.log.
    def at(self, phrase, lead=.2, nth=0):
        rest=self.t_of(phrase,nth)-lead-self.elapsed()
        if rest>.02: self.wait(rest)


def heading(s): return T(s,32,TEXT).move_to([0,3.3,0])

def grid(x=-3,size=.9,labels=True):
    g=VGroup()
    for col in range(3):
        column=VGroup()
        for row in range(6):
            c=GREEN if col==1 else RED
            sq=Square(side_length=size,color=c,stroke_width=1.5,fill_color=c,fill_opacity=.22).move_to([x+(col-1)*size,(2.5-row)*size,0])
            item=VGroup(sq)
            if labels: item.add(M('+1' if col==1 else '−0.5',26,c).move_to(sq))
            column.add(item)
        g.add(column)
    return g

def light(x=-3):
    return Rectangle(width=.86,height=5.35,color=YELLOW,stroke_width=3,fill_color=YELLOW,fill_opacity=.45).move_to([x,0,0])

def raster(rate=0,x=4.1,y=-1.6,width=3.3):
    n=int(round(max(0,rate)*4))
    return VGroup(Line([x-width/2,y,0],[x+width/2,y,0],color=GREY),
        VGroup(*[Line([p,y+.06,0],[p,y+.8,0],color=BLUE,stroke_width=4) for p in ([x] if n==1 else np.linspace(x-width/2+.1,x+width/2-.1,n))]),
        T('spikes · model',26,TEXT).move_to([x,y-.4,0]))

def meter(v=6):
    x=1.6; z=-.45
    return VGroup(Line([x,z-2.1,0],[x,z+2.1,0],color=GREY),
        Line([x-.15,z,0],[x+.8,z,0],color=GREY),M('0',26).move_to([x+1.05,z,0]),
        Rectangle(width=.5,height=max(.015,abs(v)*.35),stroke_width=0,fill_color=GREEN if v>=0 else RED,fill_opacity=.9).move_to([x+.3,z+v*.35/2,0]),
        M(f'sum {v:+g}',36).move_to([3.8,2.3,0]),
        DashedLine([x-.2,z+.7,0],[x+.75,z+.7,0],color=ORANGE),
        T('threshold 2',26,ORANGE).move_to([4,.25,0]))

def simple(v=6): return VGroup(grid(),light(),meter(v),raster(max(0,v-2)))
def q1(): return VGroup(heading('Slide the bar sideways.'),simple(),T('What does one sum do?',34).move_to([0,-3.3,0]))

def spot_event(before,after,sensitivity=1):
    # Pool separate rectified onset and offset channels: both changes excite.
    change=after-before
    return .25*sensitivity*(max(change,0)+max(-change,0))

def complex_rate(x,angle=90):
    # Broad spatial pooling envelope times a 180-degree-periodic orientation tuning.
    return .25+4*np.exp(-((x+3)/2.1)**2)*np.exp(3*(np.cos(2*(angle-90)*DEGREES)-1))

def complex_stage(x=-4.8,angle=90):
    field=Rectangle(width=5.8,height=5.7,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([-3,0,0])
    bar=Rectangle(width=.3,height=4.6,color=YELLOW,fill_color=YELLOW,fill_opacity=.9).rotate((angle-90)*DEGREES).move_to([x,0,0])
    return VGroup(field,bar,raster(complex_rate(x,angle)),T('complex cell',32,PURPLE).move_to([-3,3.2,0]))

def overlap(a,b,width): return max(0,min(a+width/2,b+width/2)-max(a-width/2,b-width/2))/width
CENTERS=(-4.3,-3.1,-1.9)

def pool_rates(x,angle=90):
    gain=np.exp(3*(np.cos(2*(angle-90)*DEGREES)-1))
    return [max(0,6*gain*(overlap(x,c,1.2)-.5*overlap(x,c-1.2,1.2)-.5*overlap(x,c+1.2,1.2))-2) for c in CENTERS]

def pooling(x=-3.1,angle=90):
    rates=pool_rates(x,angle); fs=VGroup(); bars=VGroup()
    for i,(c,y,r) in enumerate(zip(CENTERS,(2, .55,-.9),rates)):
        f=VGroup()
        for j in (-1,0,1):
            color=GREEN if j==0 else RED
            f.add(Rectangle(width=1.2,height=.9,color=color,stroke_width=2,fill_color=color,fill_opacity=(.85 if r>0 else .12) if j==0 else .12).move_to([c+1.2*j,y,0]))
        f.add(T(f'simple {i+1}',26,BLUE).move_to([1,y,0]))
        fs.add(f)
        bars.add(Rectangle(width=.15,height=.88,color=YELLOW,fill_color=YELLOW,fill_opacity=.95 if abs(x-c)<1.8 else 0,stroke_opacity=1 if abs(x-c)<1.8 else 0).rotate((angle-90)*DEGREES).move_to([x,y,0]))
    cx=chip('complex cell',PURPLE,32).move_to([4.3,.55,0])
    arrows=VGroup(*[Arrow([1.9,y,0],[cx.get_left()[0],.55+dy,0],color=GREEN,buff=.12,tip_length=.18,stroke_width=3) for y,dy in zip((2,.55,-.9),(.28,0,-.28))])
    outlines=VGroup(*[Rectangle(width=3.6,height=.6,color=GREY,stroke_width=1).move_to([c,-2.25,0]) for c in CENTERS])
    band=Rectangle(width=3.6,height=.6,color=GREEN,fill_color=GREEN,fill_opacity=.3).move_to([-3.1,-2.25,0])
    stim=Rectangle(width=.15,height=.6,color=YELLOW,fill_color=YELLOW,fill_opacity=1).rotate((angle-90)*DEGREES).move_to([x,-2.25,0])
    covered=VGroup(outlines,band,stim,T('covered ON region',26,GREEN).move_to([-3.1,-2.95,0]))
    return VGroup(fs,bars,cx,arrows,covered,raster(sum(rates),x=4.3,y=-1.6,width=3.2))

def hue(a): return '#'+''.join(f'{round(v*255):02x}' for v in colorsys.hsv_to_rgb((a%180)/180,.58,.92))
def sheet(kind='rat',center=(0,0,0),spacing=.78):
    rng=np.random.default_rng(42); g=VGroup()
    for row in range(7):
        for col in range(7):
            a=float(rng.choice([0,30,60,90,120,150])) if kind=='rat' else float((col//2*30+row//3*30)%180)
            if kind=='rat' and row==3 and col==3: a=90.
            if kind=='rat' and row==3 and col==4: a=30.
            p=np.array([(col-3)*spacing,(3-row)*spacing,0])+np.array(center)
            c=Circle(radius=spacing*.36,color=hue(a),fill_color=hue(a),fill_opacity=.7,stroke_width=1).move_to(p)
            d=np.array([np.cos(a*DEGREES),np.sin(a*DEGREES),0])*spacing*.25
            g.add(VGroup(c,Line(p-d,p+d,color=TEXT,stroke_width=3)))
    return g

def key():
    g=VGroup()
    for i,a in enumerate((0,30,60,90,120,150)):
        p=np.array([-3+i*1.2,-3.03,0]); d=np.array([np.cos(a*DEGREES),np.sin(a*DEGREES),0])*.17
        g.add(VGroup(Line(p-d,p+d,color=hue(a),stroke_width=5),T(f'{a}°',26).move_to(p+DOWN*.4)))
    return g

def maps():
    return VGroup(sheet('cat',(-3.25,0,0)),sheet('rat',(3.25,0,0)),T('cat · orderly patches',30).move_to([-3.25,3.05,0]),T('rat · speckled',30).move_to([3.25,3.05,0]),key())

def q2():
    rat=VGroup(*[Circle(radius=.76*.36,color=GREY,fill_color=GREY,fill_opacity=.18,stroke_width=1).move_to([3.5+(col-3)*.76,-.1+(3-row)*.76,0]) for row in range(7) for col in range(7)])
    return VGroup(T('Does tuning need\nneighbours that agree?',36,line_spacing=1.3).move_to([-3.1,.4,0]),rat,T('?',90,YELLOW).move_to(rat),T('rat cortex?',30).move_to([3.5,3.05,0]))

def countdown(scene,center):
    base=Circle(.32,color=GREY).move_to(center)
    arc=Arc(radius=.32,start_angle=PI/2,angle=TAU-.001,color=YELLOW,stroke_width=5).move_to(center)
    scene.add(base); scene.play(Create(arc),run_time=5,rate_func=linear)

class S00Title(TitleCard):
    LESSON='Visual Cortex'
    TITLE='Anywhere in the Field, and Columns'
    def construct(self):
        title=VGroup(T('Anywhere in the Field,',46,font=TITLE_FONT),T('and Columns',46,font=TITLE_FONT)).arrange(DOWN,buff=.22)
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T('VISUAL CORTEX',26),title,Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.35)
        self.add(g); self.finish()

class S01Question(TimedSpoken):
    def construct(self):
        self.at('take a simple'); self.add(q1()); self.finish()

class S02Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(q1()); countdown(self,[5.8,-3.2,0])

class S03Reveal(TimedSpoken):
    def construct(self):
        g=q1(); f=ValueTracker(0)
        # Sliding across two adjacent strips gives sum=6*(1-f)-3*f.
        # Derive both the meter and spikes from this same instantaneous sum.
        m=always_redraw(lambda: meter(round(6-9*f.get_value(),1)))
        r=always_redraw(lambda: raster(max(0,6-9*f.get_value()-2)))
        self.add(g[0],g[2],g[1][0],g[1][1],m,r)
        self.at('it falls')
        self.play(FadeOut(g[0]),FadeOut(g[2]),g[1][1].animate.shift(RIGHT*.9),f.animate.set_value(1),run_time=1.5)
        m.clear_updaters(); r.clear_updaters()
        self.at('falling silent'); self.play(Indicate(r[0],color=BLUE),run_time=.4); self.finish()

class S04Complex(TimedSpoken):
    def construct(self):
        g=complex_stage(); self.add(g,T('vertical bar = preferred angle',28,YELLOW).move_to([3.8,2.5,0]))
        self.at('a correctly oriented')
        self.play(g[1].animate.move_to([-3,0,0]),Transform(g[2],raster(complex_rate(-3))),run_time=.5)
        self.add(T('Responds across\nmuch of the field',28,PURPLE).move_to([3.8,1.2,0]))
        self.at('over much'); self.play(g[1].animate.move_to([-1.2,0,0]),Transform(g[2],raster(complex_rate(-1.2))),run_time=.5)
        self.wait(1.5); self.finish()

class S05Angle(TimedSpoken):
    def construct(self):
        g=complex_stage(-3,0); self.add(g,T('wrong angle',30,YELLOW).move_to([3.8,2.5,0]))
        wrong=self.mobjects[-1]
        self.at('answered spots')
        self.play(FadeOut(g[1]),FadeOut(wrong),Transform(g[2],raster(0)),run_time=.25)
        note=T('Overlapping ON / OFF responses\nExample, not every complex cell',26).move_to([0,-3.3,0]); self.add(note)
        # Two spatial examples shown together; each event has its own permanent
        # label and tick underneath, preventing detached after-response frames.
        spots=VGroup(Dot([-4.3,.6,0],radius=.25,color=YELLOW),Dot([-1.7,-.6,0],radius=.25,color=YELLOW))
        events=VGroup()
        self.at('turning a spot on')
        for x in (2.6,5):
            events.add(VGroup(T('spot ON',26,YELLOW).move_to([x,1.1,0]),raster(spot_event(0,1),x=x,y=-.1,width=1.8)[:2]))
        self.play(FadeIn(spots),FadeIn(events),FadeOut(g[2]),run_time=.2)
        self.at('turning it off')
        off=VGroup(*[VGroup(T('spot OFF',26,YELLOW).move_to([x,-1,0]),raster(spot_event(1,0),x=x,y=-2.15,width=1.8)[:2]) for x in (2.6,5)])
        # Hollow markers retain the two tested locations after light offset.
        hollow=VGroup(*[Circle(.25,color=YELLOW,stroke_width=2).move_to(p) for p in spots])
        self.play(FadeOut(spots),FadeIn(hollow),FadeIn(off),run_time=.2)
        self.at("a simple cell's")
        inset=grid(3.8,.55,False)
        labels=VGroup(T('simple cell',30,BLUE).move_to([3.8,2.35,0]),T('OFF',26,RED).move_to([2.7,-2.1,0]),T('ON',26,GREEN).move_to([3.8,-2.1,0]),T('OFF',26,RED).move_to([4.9,-2.1,0]))
        self.play(FadeOut(events),FadeOut(off),run_time=.13)
        self.play(FadeIn(inset),FadeIn(labels),run_time=.2)
        self.at('other complex cells')
        self.play(FadeOut(inset),FadeOut(labels),FadeOut(hollow),FadeOut(note),run_time=.15)
        self.play(FadeIn(spots),FadeIn(g[2]),FadeIn(T('Other complex cells: no small-spot response',28).move_to([0,-3.3,0])),run_time=.15)
        self.finish()

class S05bOnesum(TimedSpoken):
    def construct(self):
        g=simple(); polarity=T('bright bar',30,YELLOW).move_to([-3,3.25,0])
        self.add(g,polarity,T('Reverse the contrast, flip the sign',32).move_to([0,-3.3,0]))
        self.at('a dark one'); self.play(g[1].animate.set_fill('#020309',opacity=1).set_stroke(YELLOW),Transform(polarity,T('dark bar',30,YELLOW).move_to(polarity)),Transform(g[3],raster(0)),run_time=.35)
        self.at('the sum flips'); self.play(ReplacementTransform(g[2],meter(-6)),run_time=.3); self.finish()

class S06Pool(TimedSpoken):
    def construct(self):
        # Full-height vertical fields overlap in space; fade into separated rows
        # before the cut, so s07 starts with exactly the same vertical-strip layout.
        fs=VGroup(*[grid(0,.8,False).set_opacity(.65).move_to([x,y,0]) for x,y in ((-1.2,.4),(0,0),(1.2,-.4))])
        labels=VGroup(*[T(f'simple {i+1}',28,BLUE).move_to([4.4,y,0]) for i,y in enumerate((1.8,.2,-1.4))])
        leaders=VGroup(*[Line([x+1.2,y,0],[3.35,ly,0],color=GREY,stroke_width=1) for x,y,ly in ((-1.2,.4,1.8),(0,0,.2),(1.2,-.4,-1.4))])
        self.add(heading('Proposed pooling'),fs,labels,leaders)
        self.at('several simple cells'); self.play(Indicate(fs,scale_factor=1.02),run_time=.3)
        self.at('share one angle'); self.play(Indicate(VGroup(*[f[1] for f in fs]),color=GREEN,scale_factor=1.03),run_time=.4)
        note=T('The three fields overlap',28).move_to([0,-3.15,0])
        self.at('fields at slightly'); self.play(FadeIn(note),run_time=.2)
        self.wait(.7)
        g=pooling(-4.7)
        self.play(FadeOut(fs),FadeOut(labels),FadeOut(leaders),FadeOut(note),run_time=.3)
        self.play(FadeIn(g[0]),FadeIn(g[4]),run_time=.4); self.finish()

class S07Converge(TimedSpoken):
    def construct(self):
        g=pooling(-4.7); self.add(heading('Proposed pooling'),g[0],g[4])
        self.at('all of them'); self.play(FadeIn(g[2]),Create(g[3]),run_time=.4)
        self.at('where their responses'); self.play(Indicate(g[4][1],color=GREEN,scale_factor=1.02),run_time=.3)
        # Four readable states, with all arrows retained. Each response derives
        # from overlap of the bar with all three signed fields, then rectification.
        self.at('at least one'); self.play(FadeIn(g[1]),FadeIn(g[5]),run_time=.2)
        self.wait(1.6)
        for x,hold in ((-3.1,1.6),(-1.5,1.6),(-.35,1.5)):
            new=pooling(x)
            self.play(Transform(g[0],new[0]),Transform(g[1],new[1]),Transform(g[4],new[4]),Transform(g[5],new[5]),run_time=.25)
            self.wait(hold)
        self.finish()

class S08Keeps(TimedSpoken):
    def construct(self):
        g=pooling()
        # Reserve a clear block below the complex cell for the two conclusions.
        g[5].shift(DOWN*.95)
        self.add(heading('Proposed pooling'),g)
        a=T('Keeps orientation',28,PURPLE).move_to([4.1,-.35,0])
        b=T('Tolerates position',28,PURPLE).move_to([4.1,-1.05,0])
        def state(x,angle):
            n=pooling(x,angle); n[5].shift(DOWN*.95)
            return [Transform(g[i],n[i]) for i in (0,1,4,5)]
        self.at('keeps its preferred')
        self.play(FadeIn(a),*state(-3.1,0),run_time=.35)
        self.wait(.5)
        self.play(*state(-3.1,90),run_time=.35)
        self.at('gains tolerance')
        self.play(FadeIn(b),*state(-4.3,90),run_time=.45)
        self.play(*state(-1.9,90),run_time=.85); self.finish()

class S09Debate(TimedSpoken):
    def construct(self):
        g=pooling(); self.add(g[0],g[2],g[3],heading('Second step: still debated'))
        lgn=chip('LGN cell',ORANGE,30).move_to([-3.3,-2.65,0])
        direct=VGroup(DashedLine(lgn.get_right(),[6.2,-2.65,0],color=ORANGE,dash_length=.15),DashedLine([6.2,-2.65,0],[6.2,.55,0],color=ORANGE,dash_length=.15),DashedLine([6.2,.55,0],g[2].get_right(),color=ORANGE,dash_length=.1).add_tip(tip_length=.15))
        self.at('receive direct'); self.play(FadeIn(lgn),Create(direct),run_time=.4)
        self.add(T('direct input',28,ORANGE).move_to([.1,-3.2,0]))
        self.at('circuits within')
        loop=VGroup(*[Arc(radius=.32,start_angle=.2,angle=TAU-.6,color=PURPLE).add_tip(tip_length=.12).move_to([x,-.65,0]) for x in (3.4,5.25)])
        self.play(Create(loop),FadeIn(T('intracortical\ncircuits',28,PURPLE).move_to([4.5,-1.7,0])),run_time=.4); self.finish()

class S10Column(TimedSpoken):
    def construct(self):
        slab=Rectangle(width=8.5,height=5.3,color=GREY,fill_color=GREY,fill_opacity=.1).move_to([0,-.45,0])
        surface=Line([-4.25,2.2,0],[4.25,2.2,0],color=TEXT,stroke_width=5)
        self.add(slab,surface,heading('Cat and monkey cortex'),T('surface',28).move_to([3.2,2.55,0]))
        e=Line([-.8,2.7,0],[-.8,2.35,0],color=TEXT,stroke_width=4)
        self.at('an electrode'); self.play(Create(e),run_time=.2)
        self.add(T('electrode',28).move_to([-2.7,2.6,0]),VGroup(Line([-.8,1.9,0],[-.5,1.9,0],color=TEXT),Line([-.5,1.9,0],[-.5,2.2,0],color=TEXT)))
        self.at('going straight down')
        for i,y in enumerate(np.linspace(1.55,-2.65,8)):
            a=(86,92,90,85,94,88,91,87)[i]*DEGREES; d=np.array([np.cos(a),np.sin(a),0])*.2
            cell=VGroup(Circle(.25,color=BLUE,fill_color=BG,fill_opacity=1),Line(-d,d,color=TEXT,stroke_width=4)).move_to([-.8,y,0])
            self.play(e.animate.put_start_and_end_on([-.8,2.7,0],[-.8,y,0]),run_time=.21); self.add(cell)
        self.at('share an angle'); self.play(FadeIn(T('Similar preferred angles',28,BLUE).move_to([2.2,.7,0])),run_time=.25)
        outline=RoundedRectangle(width=1.15,height=5,corner_radius=.18,color=BLUE,stroke_width=2,stroke_opacity=.5).move_to([-.8,-.55,0])
        label=T('column',36,BLUE).next_to(outline,RIGHT,buff=.45)
        self.at('that is a column'); self.play(Create(outline),FadeIn(label),run_time=.3); self.wait(2); self.finish()

class S11Predict(TimedSpoken):
    def construct(self):
        self.at('does a cell'); self.add(q2()); self.finish()
class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(q2()); countdown(self,[-3.1,-2.4,0])

class S13Reveal(TimedSpoken):
    def construct(self):
        g=maps(); self.add(g)
        rat=g[1]
        self.at('sharply tuned cells'); self.play(Create(Circle(.34,color=TEXT,stroke_width=4).move_to(rat[24])),run_time=.35)
        self.at('preferred unrelated angles'); self.play(*[Create(Circle(.34,color=YELLOW,stroke_width=4).move_to(rat[i])) for i in (17,23,25,31)],run_time=.4); self.finish()

class S14Salt(TimedSpoken):
    def construct(self):
        g=maps(); self.add(g)
        self.at('this layout'); self.play(FadeOut(g[0]),FadeOut(g[2]),FadeOut(g[3]),FadeOut(g[4]),g[1].animate.scale(1.06).move_to(ORIGIN),run_time=.4)
        self.at('salt and pepper'); self.add(heading('salt-and-pepper'))
        self.at('tuning does not',lead=.5); self.play(FadeIn(T('Tuning does not need a map.',34).move_to([0,-3.25,0])),run_time=.2); self.finish()

class S15Why(TimedSpoken):
    def construct(self):
        rat=sheet('rat',(-3.5,0,0),.72)
        ax=Axes(x_range=[0,180,30],y_range=[0,40,10],x_length=5.1,y_length=5.4,tips=False,axis_config={'color':GREY,'include_ticks':True}).move_to([3.4,.1,0])
        # A period-180 von Mises orientation curve, explicitly illustrative.
        curve=ax.plot(lambda a: 40*np.exp(3*(np.cos(2*(a-90)*DEGREES)-1)),x_range=[0,180,1],color=hue(90),stroke_width=4,use_smoothing=False)
        labs=VGroup(T('illustrative tuning',28,BLUE).move_to([3.5,3.15,0]),T('bar angle',28).move_to([3.5,-3.2,0]),T('spikes/s',26).move_to([.25,3.25,0]))
        for a in (0,90,180): labs.add(T(f'{a}°',26).next_to(ax.c2p(a,0),DOWN,buff=.13))
        for r in (0,20,40): labs.add(T(str(r),26).next_to(ax.c2p(0,r),LEFT,buff=.15))
        ring=Circle(.31,color=TEXT,stroke_width=4).move_to(rat[24])
        start=ring.get_center()+np.array([1,1,0])*.31/np.sqrt(2)
        route=[start,[-3.14,.36,0],[-.85,.36,0],[-.85,2.55,0],[2.8,2.55,0],ax.c2p(90,40)]
        link=VGroup(*[DashedLine(a,b,color=hue(90),stroke_width=2,dash_length=.08) for a,b in zip(route,route[1:])])
        self.add(rat,ring,ax,curve,labs,link)
        self.at('tuning does not'); self.play(*[Create(Circle(.31,color=YELLOW,stroke_width=3).move_to(rat[i])) for i in (17,23,25,31)],run_time=.35)
        self.at('how each cell'); self.play(FadeIn(T('How each cell is tuned: not shown by this experiment',27).move_to([0,-3.65,0])),run_time=.3); self.finish()

class S16Takeaway(TimedSpoken):
    def construct(self):
        self.add(heading('The rule and its limit'))
        card=RoundedRectangle(width=12.2,height=5.9,corner_radius=.2,color=GREY,stroke_width=1).move_to([0,-.25,0])
        divider=Line([-5.8,-.2,0],[5.8,-.2,0],color=GREY,stroke_width=1)
        f=grid(0,.36,False).move_to([-4.3,1.25,0])
        simple_text=VGroup(T('Simple cell: one sum',30,BLUE),T('Layout largely sets preference',30)).arrange(DOWN,aligned_edge=LEFT,buff=.3).move_to([1.3,1.25,0])
        self.add(card,divider,f,simple_text)
        mini=VGroup(*[grid(0,.23,False).move_to([x,-1.9,0]) for x in (-5.35,-4.45,-3.55)])
        cx=Circle(.36,color=PURPLE,fill_color=PURPLE,fill_opacity=.3).move_to([-2,-1.9,0])
        arrows=VGroup(*[Arrow([x+.25,-2.65,0],[-2.2,-2.2,0],color=GREEN,buff=.06,tip_length=.12,stroke_width=2) for x in (-5.35,-4.45,-3.55)])
        complex_text=T('Complex cell: more than one sum',30,PURPLE).align_to(simple_text,LEFT).set_y(-1.9)
        lower=VGroup(mini,cx,arrows)
        self.add(lower)
        self.at('adds up the light'); self.play(Indicate(f[1],color=YELLOW,scale_factor=1.02),run_time=.4)
        self.at('layout largely sets'); self.play(Indicate(simple_text[1],scale_factor=1.03),run_time=.4)
        self.at('a complex cell'); self.play(Indicate(cx,color=PURPLE,scale_factor=1.08),FadeIn(complex_text),run_time=.35); self.finish()

class S17End(EndCard):
    LINE='One sum tunes a simple cell; a complex cell needs more.'
    def construct(self):
        line=VGroup(T('One sum tunes a simple cell;',38,font=TITLE_FONT),T('a complex cell needs more.',38,font=TITLE_FONT)).arrange(DOWN,buff=.3)
        sub=T('biochemistrypedia.com',26,TEAL).move_to([0,-1.7,0])
        self.add(line,sub); self.finish()
