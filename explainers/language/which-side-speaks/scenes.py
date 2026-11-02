"""Chapter 3, reviewed animation.
COLOR MAP: BLUE = strong right-handers; YELLOW = strong left-handers;
GREY = ambidextrous people and structure; TEXT = results and language function.
Filled dots = right-dominant; outlines = remaining people.
All proportions and counts computed from .04/.15/.27. Blood-flow traces are
explicitly schematic piecewise-linear scoring examples, not measured recordings.
"""
import numpy as np
from bp_style import *

R_RIGHT, R_LEFT = .04, .27
RIGHT_LIT = sorted(np.random.RandomState(3).choice(100, round(100*R_RIGHT), replace=False))
MIX_RIGHT_LIT = sorted(np.random.RandomState(13).choice(900, round(900*R_RIGHT), replace=False))
LEFT_LIT = sorted(np.random.RandomState(7).choice(100, round(100*R_LEFT), replace=False))

def heading(s): return T(s,32,font=TITLE_FONT).move_to([0,3.25,0])
def footer():
    return T('Made-up mixes for exercise; strong right- and left-handers only.',26,GREY).move_to([0,-3.45,0])
def dot(c,lit,r):
    return Circle(radius=r,stroke_color=c,stroke_width=1.8,fill_color=c,
                  fill_opacity=int(lit)).set_stroke(opacity=1 if lit else .4)
def light(d,c): return d.animate.set_fill(c,1).set_stroke(c,opacity=1)
def equal_layout(lit=False):
    groups=[]
    for x,c,chosen in [(-3.25,BLUE,RIGHT_LIT),(3.25,YELLOW,LEFT_LIT)]:
        groups.append(VGroup(*[dot(c,lit and k in chosen,.145).move_to(
            [x+(k%10-4.5)*.46,.3+(4.5-k//10)*.46,0]) for k in range(100)]))
    labs=VGroup(T('100 right-handers',28,BLUE).move_to([-3.25,2.8,0]),
                T('100 left-handers',28,YELLOW).move_to([3.25,2.8,0]))
    return *groups,labs

def question(): return T('Right-dominant: probably left-handed?',29).move_to([0,-2.35,0])
def legend(): return T('Filled dots = right-dominant',28).move_to([0,3.4,0])
def answer(): return T('27 of 31 ≈ 87% left-handed',34).move_to([0,-2.35,0])
def tally(): return T('31 filled dots = 4 blue + 27 yellow',28).move_to([0,3.4,0])

def mix_layout(lit=False):
    groups=[]
    # 20 rows; anisotropic spacing uses the entire available height.
    for n,cols,x,c,chosen in [(900,45,-.65,BLUE,MIX_RIGHT_LIT),
                              (100,5,5.35,YELLOW,LEFT_LIT)]:
        groups.append(VGroup(*[dot(c,lit and k in chosen,.09).move_to(
            [x+(k%cols-(cols-1)/2)*.24,.3+(9.5-k//cols)*.25,0]) for k in range(n)]))
    labs=VGroup(T('900 right-handers · 4% right-dominant',25,BLUE).move_to([-.8,2.95,0]),
                T('100 left-handers\n27% right-dominant',24,YELLOW).move_to([5.05,3.2,0]))
    return *groups,labs

def patient(probes=False):
    head=Ellipse(width=3.7,height=4.9,color=GREY,fill_color=GREY,fill_opacity=.09).move_to([0,.3,0])
    neck=VGroup(Line([-.65,-1.9,0],[-.65,-2.55,0],color=GREY),Line([.65,-1.9,0],[.65,-2.55,0],color=GREY),
        VMobject(color=GREY).set_points_as_corners([[-2.4,-3,0],[-.65,-2.55,0],[.65,-2.55,0],[2.4,-3,0]]))
    face=VGroup(*[Line([x-.12,.7,0],[x+.12,.7,0],color=GREY) for x in [-.65,.65]],
        Line([-.35,-.65,0],[.35,-.65,0],color=TEXT),Line([0,.5,0],[.15,-.1,0],color=GREY))
    pads=VGroup(*[RoundedRectangle(width=.4,height=.85,corner_radius=.08,color=TEXT,
        fill_color=GREY,fill_opacity=.8).move_to([x,1.45,0]) for x in [-1.7,1.7]]) if probes else VGroup()
    return VGroup(head,neck,face,pads)

def rate_chart(top=30,small=False):
    base=-2.15; height=4.6; x0=-4.7
    axes=VGroup(Line([x0,base,0],[5.8,base,0],color=GREY),Line([x0,base,0],[x0,base+height,0],color=GREY))
    ticks=VGroup()
    for v in range(0,top+1,10):
        yy=base+height*v/top
        ticks.add(Line([x0-.1,yy,0],[x0+.1,yy,0],color=GREY),T(f'{v}%',26,GREY).move_to([x0-.65,yy,0]))
    ylab=T('right-sided language' if small else '% with right-sided language',26).rotate(PI/2).move_to([-6.15,.2,0])
    bars=VGroup(); nums=VGroup(); labs=VGroup()
    for x,v,c,name in [(-2.8,4,BLUE,'Strong\nright-handers'),(.55,15,GREY,'Ambidextrous'),(3.9,27,YELLOW,'Strong\nleft-handers')]:
        h=height*v/top
        bar=Rectangle(width=1.9,height=h,color=c,fill_color=c,fill_opacity=.75).move_to([x,base+h/2,0])
        bars.add(bar); nums.add(T(f'{v}%',32,c).next_to(bar,UP,buff=.12));labs.add(T(name,26,c).move_to([x,-2.6,0]))
    return axes,ticks,ylab,bars,nums,labs

class S00Title(TitleCard):
    LESSON='Language and Lateralization'
    TITLE='Which Side Speaks, and How Sure?'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON.upper(),26,GREY),
            T('Which Side Speaks,\nand How Sure?',48,font=TITLE_FONT),Line(LEFT*1.2,RIGHT*1.2,color=GOLD)).arrange(DOWN,buff=.35)
        self.play(FadeIn(g),run_time=.6);self.finish()

class S01Question(SpokenScene):
    def construct(self):
        halves=VGroup(*[Ellipse(width=3.5,height=5.15,color=GREY,fill_color=GREY,fill_opacity=.13).move_to([x,.3,0]) for x in [-2,2]])
        self.add(halves,T('Left',28).move_to([-2,-2.65,0]),T('Right',28).move_to([2,-2.65,0]),
                 T('Diagram view: left hemisphere on the left',26,GREY).move_to([0,-3.3,0]))
        self.at('on the left')
        self.play(FadeIn(T('language,\nusually',28).move_to([-2,.7,0])),halves[0].animate.set_fill(TEXT,.28),run_time=.4)
        self.at('But how most')
        self.play(FadeIn(T('?? %',52).move_to([-2,-.5,0])),run_time=.4)
        self.at('what does handedness')
        self.play(FadeIn(T('One person?\nHandedness\ntells us…?',26).move_to([2,.4,0])),run_time=.4);self.finish()

class S02Method(SpokenScene):
    def construct(self):
        p=patient(True);pads=p[3];p.remove(pads);self.add(p)
        self.at('healthy adults');self.play(FadeIn(heading('326 healthy adults')),run_time=.3)
        self.at('ultrasound probes');self.play(FadeIn(pads),run_time=.4)
        self.at('over each temple')
        self.play(FadeIn(T('functional\ntranscranial\nDoppler',28).move_to([-4.3,.6,0])),run_time=.4)
        self.at('while they generated words')
        bubble=chip('words',TEXT,30).move_to([4,-.5,0])
        self.play(Transform(p[2][2],Ellipse(width=.55,height=.3,color=TEXT).move_to([0,-.65,0])),
            GrowArrow(Arrow([.45,-.65,0],[2.8,-.5,0],color=TEXT)),FadeIn(bubble),run_time=.4);self.finish()

class S03Method2(SpokenScene):
    def construct(self):
        p=patient(True).scale(.3).move_to([-4.65,2.25,0]);self.add(p)
        axes=VGroup(Line([-3.1,-2.15,0],[4.3,-2.15,0],color=GREY),Line([-3.1,-2.15,0],[-3.1,2.95,0],color=GREY))
        self.add(axes,T('blood-flow velocity (rise)',26).rotate(PI/2).move_to([-6.15,-.55,0]),
                 T('time, word generation starts →',26).move_to([.7,-2.75,0]),
                 T('Schematic scoring rule; not a recording',26,GREY).move_to([0,-3.4,0]))
        for pad,yy in zip(p[3],[-1.5,-1.85]):
            self.add(DashedLine(pad.get_bottom(),[-3.1,yy,0],color=GREY,stroke_opacity=.5))
        def trace(rise,c):
            xs=np.linspace(-3.05,3.45,100);h=np.interp(xs,[-3.05,-2.1,.8,3.45],[0,0,rise,rise])
            return VMobject(color=c,stroke_width=5).set_points_as_corners([[x,-2+v,0] for x,v in zip(xs,h)])
        a,b=trace(3.8,TEXT),trace(1.7,GREY)
        self.at('blood flow rises')
        self.play(Create(a),Create(b),FadeIn(T('left side',26).move_to([4.55,1.8,0])),FadeIn(T('right side',26,GREY).move_to([4.55,-.3,0])),run_time=.9)
        self.at('scored as')
        bracket=BraceBetweenPoints([2.4,-.3,0],[2.4,1.8,0],direction=RIGHT,color=TEXT)
        self.play(FadeIn(bracket),FadeIn(T('bigger rise\n= dominant',27).move_to([4.25,.75,0])),run_time=.4);self.finish()

class S04Rates(SpokenScene):
    def construct(self):
        ax,tk,yl,b,n,l=rate_chart();self.add(ax,tk,yl,l,heading('Language dominance by handedness'),
            T('One study, 326 adults; figures depend on the method',26,GREY).move_to([0,-3.35,0]))
        self.at('appeared in about');self.play(GrowFromEdge(b[0],DOWN),FadeIn(n[0]),run_time=.5)
        self.at('strong right');self.play(GrowFromEdge(b[1],DOWN),FadeIn(n[1]),run_time=.5)
        self.at('more than a quarter');self.play(GrowFromEdge(b[2],DOWN),FadeIn(n[2]),run_time=.6);self.finish()

class S05Most(SpokenScene):
    def construct(self):
        self.add(heading('Strong left-handers'))
        l=Rectangle(width=8.76,height=3.6,color=YELLOW,fill_color=YELLOW,fill_opacity=.65).move_to([-1.62,.25,0])
        r=Rectangle(width=3.24,height=3.6,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([4.38,.25,0])
        self.add(l,r,T('73%\nleft-dominant',36,BG).move_to(l),T('27%\nright-dominant',28).move_to(r))
        self.at('still speak');self.play(FadeIn(T('Most still left-dominant',34).move_to([0,2.7,0])),run_time=.4)
        self.at('raises the odds');self.play(FadeIn(T('Higher odds than right-handers (4%)',30).move_to([0,-2.4,0])),run_time=.4)
        self.at('does not make');self.play(Indicate(l,color=YELLOW),run_time=.6);self.finish()

class S06Q(SpokenScene):
    def construct(self):
        b,y,l=equal_layout();self.add(b,y,footer())
        self.at('equal numbers');self.play(FadeIn(l),run_time=.4)
        self.at('Pick one');self.play(FadeIn(T('Pick one right-dominant person',28).move_to([0,3.4,0])),run_time=.3)
        self.at('Is that person');self.play(FadeIn(question()),run_time=.4);self.finish()

class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(*equal_layout(),footer(),question(),T('Pick one right-dominant person',28).move_to([0,3.4,0]))
        track=Circle(radius=.25,color=GREY).move_to([6.25,-2.4,0]);progress=VMobject()
        progress.add_updater(lambda m: m.become(Arc(radius=.25,start_angle=PI/2,angle=-TAU*max(.001,t.get_value()),color=TEXT,stroke_width=5).move_arc_center_to([6.25,-2.4,0])))
        t=ValueTracker(0);self.add(track,progress);self.play(t.animate.set_value(1),run_time=5,rate_func=linear);progress.clear_updaters()

class S08Reveal(SpokenScene):
    def construct(self):
        b,y,l=equal_layout();key=legend();self.add(b,y,l,footer(),key)
        self.at('Yes');self.play(*[light(b[k],BLUE) for k in RIGHT_LIT],*[light(y[k],YELLOW) for k in LEFT_LIT],FadeIn(answer()),run_time=.5)
        self.at('Most right dominant')
        self.play(ReplacementTransform(key,tally()),run_time=.3)
        self.finish()

class S08bPause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(*equal_layout(True),footer(),tally(),answer());self.wait(1.5)

class S08cReveal2(SpokenScene):
    def construct(self):
        b,y,l=equal_layout(True)
        # Retain both populations and every filled dot; shrink only to make room for the two questions.
        for group in [b,y]:group.scale(.72).shift(UP*.4)
        self.add(b,y,l,footer(),heading('Two denominators, two questions'))
        first=T('Of right-dominant people, 87% are left-handed (27 of 31)',27).move_to([0,-1.95,0])
        second=T('Of left-handers, 27% are right-dominant (27 of 100)',27).move_to([0,-2.6,0])
        self.add(first)
        selected=VGroup(*[b[k] for k in RIGHT_LIT],*[y[k] for k in LEFT_LIT])
        # Each white ring encloses one member of the 31-person denominator.
        rings=VGroup(*[Circle(radius=.14,color=TEXT,stroke_width=2.5).move_to(d) for d in selected])
        self.add(rings)
        self.at('are not');self.play(FadeIn(second),Create(SurroundingRectangle(y,buff=.12,color=YELLOW)),run_time=.4)
        self.add(T('73% left-dominant',26,YELLOW).move_to([3.25,-1.3,0]))
        self.at('two different questions');self.play(Indicate(first,scale_factor=1.02),Indicate(second,scale_factor=1.02),run_time=.6);self.finish()

class S09Mix(SpokenScene):
    def construct(self):
        b,y,l=equal_layout();self.add(b,y,l,footer(),T('Change the mix',30,font=TITLE_FONT).move_to([0,3.6,0]))
        nb,ny,nl=mix_layout()
        # Match existing people to spaced destination dots; grow the additional 800.
        # Avoid ReplacementTransform's unequal-group crossfade of whole columns.
        destinations=np.linspace(0,899,100,dtype=int)
        extra=VGroup(*[nb[k] for k in range(900) if k not in destinations])
        self.at('Make it')
        self.play(FadeOut(l),run_time=.15)
        self.at('nine right')
        self.play(*[Transform(b[k],nb[j]) for k,j in enumerate(destinations)],
            *[Transform(y[k],ny[k]) for k in range(100)],
            *[GrowFromCenter(d) for d in extra],run_time=.8)
        self.play(FadeIn(nl),run_time=.2)
        self.at('The rates stay');self.play(Indicate(nl[0],color=BLUE,scale_factor=1.02),Indicate(nl[1],color=YELLOW,scale_factor=1.02),run_time=.5);self.finish()

class S10Flipped(SpokenScene):
    def construct(self):
        b,y,l=mix_layout();self.add(b,y,l,footer())
        self.at('Now fewer');self.play(*[light(b[k],BLUE) for k in MIX_RIGHT_LIT],*[light(y[k],YELLOW) for k in LEFT_LIT],run_time=.35)
        counts=VGroup(T('36 blue',28,BLUE).move_to([-1.6,-2.5,0]),T('27 yellow',26,YELLOW).move_to([5.15,-2.5,0]))
        self.play(FadeIn(counts),FadeIn(T('36 blue + 27 yellow = 63',29).move_to([-1.3,3.55,0])),run_time=.35)
        self.at('half of the');self.play(FadeIn(T('27 of 63 ≈ 43% left-handed',32).move_to([0,-2.95,0])),run_time=.35)
        self.at('are so many');self.play(Indicate(VGroup(*[b[k] for k in MIX_RIGHT_LIT]),scale_factor=1.03,color=BLUE),run_time=.7);self.finish()

class S11Same(SpokenScene):
    def construct(self):
        self.add(heading('Same rates: 4% and 27%'))
        a=VGroup(T('50/50 mix',32),T('87%',72),T('left-handed',30)).arrange(DOWN,buff=.3).move_to([-3.3,.1,0])
        b=VGroup(T('90/10 mix',32),T('43%',72),T('left-handed',30)).arrange(DOWN,buff=.3).move_to([3.3,.1,0])
        self.add(a,b,T('Among right-dominant people',28,GREY).move_to([0,2.35,0]))
        self.at('different base rate');self.play(Indicate(a[0]),Indicate(b[0]),run_time=.4)
        self.at('different answer');self.play(FadeIn(T('Different answer',48,font=TITLE_FONT).move_to([0,-2.95,0])),run_time=.35);self.finish()

class S12Surgeon(SpokenScene):
    def construct(self):
        # Diagram convention: the patient's left hemisphere is drawn on the left.
        head=Ellipse(width=3.8,height=4.7,color=GREY).move_to([-2.4,.25,0])
        neck=VGroup(Line([-3.05,-1.85,0],[-3.05,-2.65,0],color=GREY),
                    Line([-1.75,-1.85,0],[-1.75,-2.65,0],color=GREY))
        halves=VGroup()
        for side in [-1,1]:
            points=[[-.12,1.95,0],[-.8,1.85,0],[-1.25,1.2,0],[-1.28,.35,0],
                    [-.95,-.4,0],[-.25,-.7,0],[-.12,.2,0],[-.12,1.95,0]]
            h=VMobject(color=GREY,fill_color=GREY,fill_opacity=.2)
            h.set_points_smoothly([[side*abs(x)-2.4,y,0] for x,y,_ in points]).close_path()
            halves.add(h)
        self.add(head,neck,halves,
            T('L',28).move_to([-3.12,2.25,0]),T('R',28).move_to([-1.68,2.25,0]),
            T('Diagram view: L on the left',24,GREY).move_to([-2.4,-3.3,0]))
        qs=VGroup(*[T('?',38).move_to([x,.65,0]) for x in [-3.12,-1.68]])
        self.add(qs)
        odds=heading('Handedness gives odds');self.add(odds)
        self.at('Before epilepsy surgery')
        label=T('Before epilepsy surgery',28).move_to([2.8,2.25,0])
        vessel=VMobject(color=TEXT,stroke_width=6).set_points_as_corners(
            [[-2.85,-2.65,0],[-2.85,-1.65,0],[-3.12,-.9,0],[-3.12,-.55,0]])
        injection=VGroup(vessel,Arrow([.3,-2.25,0],[-2.85,-2.25,0],buff=0,color=TEXT),
            T('anaesthetic into\none carotid artery',28).move_to([3,-1.9,0]))
        self.play(ReplacementTransform(odds,heading('Language side tested directly')),
            FadeIn(label),Create(vessel),FadeIn(injection[1:]),run_time=.6)
        self.at('the side of language')
        res=VGroup(T('left',30).move_to(qs[0]),T('no',30).move_to(qs[1]))
        self.play(ReplacementTransform(qs,res),halves[0].animate.set_fill(TEXT,.55),
            FadeIn(T('Speech affected\nby left-side test',30).move_to([3,.5,0])),run_time=.5);self.finish()

class S13Takeaway(SpokenScene):
    def construct(self):
        ax,tk,yl,b,n,l=rate_chart(60,True)
        self.add(ax,tk,yl,l,heading('Which hemisphere speaks is a probability'))
        threshold=DashedLine([-4.7,-2.15+4.6*50/60,0],[5.8,-2.15+4.6*50/60,0],color=TEXT)
        self.add(threshold,T('Even split: 50%',27).move_to([3.85,2.1,0]))
        self.play(*[GrowFromEdge(bar,DOWN) for bar in b],FadeIn(n),
            FadeIn(T('All three remain below 50%',30).move_to([0,-3.3,0])),run_time=.6)
        self.at('a probability');self.play(Indicate(b[0],color=BLUE),run_time=.4)
        self.at('shifts the odds');self.play(Indicate(b[2],color=YELLOW),run_time=.6)
        self.finish()

class S14End(EndCard):
    LINE='Left-handedness shifts the odds without reversing them.'
    def construct(self):
        line=T(self.LINE,40,font=TITLE_FONT);fit(line,max_w=11.5)
        sub=T('biochemistrypedia.com',26,TEAL)
        VGroup(line,sub).arrange(DOWN,buff=.4)
        self.play(FadeIn(line),run_time=.5)
        self.play(FadeIn(sub),run_time=.3);self.finish()
