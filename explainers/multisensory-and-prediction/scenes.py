"""Equation-computed chapter animation; final narration is unchanged.
COLOR MAP: BLUE vision; ORANGE touch; GREEN combined estimate;
TEAL precision; SELF mint teal predictable self-caused input; PURPLE sound;
YELLOW question / perceived location; RED scope limit; GREY axes.
"""
import numpy as np
from bp_style import *

ORANGE = '#F29E4C'
PURPLE = '#B58CD9'
SELF = '#2AE0A2'  # saturated mint teal, distinct from vision cyan
BASE = -2.0
MV, MH, SH = 50., 54., 4.


def comb(sv, sh=SH):
    pv, ph = 1/sv**2, 1/sh**2
    w = pv/(pv+ph)
    return w, w*MV+(1-w)*MH, np.sqrt(1/(pv+ph))


def gauss(h, mu, s):
    return np.exp(-.5*((h-mu)/s)**2)/(s*np.sqrt(2*np.pi))


def xp(h, blur=False):
    lo, hi = (20, 84) if blur else (36, 72)
    return -5.6+11.2*(h-lo)/(hi-lo)


def ct(text,size=30,color=TEXT,font=FONT,line_spacing=1.2):
    return VGroup(*[T(line,size,color,font=font) for line in text.split("\n")]).arrange(DOWN,buff=.22)


def head(s, color=TEXT):
    return T(s, 32, color, font=TITLE_FONT).move_to([0, 3.2, 0])


def axis(blur=False, sparse=False):
    lo, hi, step = (20, 84, 8) if blur else (36, 72, 4)
    g = VGroup(Line([-5.6, BASE, 0], [5.6, BASE, 0], color=GREY),
               Line([-5.6, BASE, 0], [-5.6, 2.05, 0], color=GREY))
    if sparse:
        step = 8
    for h in range(lo, hi+1, step):
        g.add(Line([xp(h,blur),BASE,0],[xp(h,blur),BASE-.14,0],color=GREY,stroke_width=3),
              M(str(h),26,GREY).move_to([xp(h,blur),BASE-.43,0]))
    g.add(T('bar height (mm)',28,GREY).move_to([0,-2.95,0]),
          T('likelihood',26,GREY).rotate(PI/2).move_to([-6.15,.1,0]))
    return g


def curve(mu,s,col,blur=False):
    lo, hi = (20,84) if blur else (36,72)
    hs=np.linspace(lo,hi,401)
    pts=[np.array([xp(h,blur),BASE+19*gauss(h,mu,s),0]) for h in hs]
    line=VMobject(stroke_color=col,stroke_width=5).set_points_smoothly(pts)
    fill=VMobject(stroke_width=0,fill_color=col,fill_opacity=.12)
    fill.set_points_as_corners(pts+[[xp(hi,blur),BASE,0],[xp(lo,blur),BASE,0],pts[0]])
    return VGroup(fill,line)


def labels(sv=2):
    return VGroup(T(f'vision · SD {sv:g} mm',28,BLUE).move_to([-3.8,2.55,0]),
                  T('touch · SD 4 mm',28,ORANGE).move_to([3.25,2.55,0]))


def graph(sv=2):
    blur=sv==8
    return VGroup(axis(blur),curve(50,sv,BLUE,blur),curve(54,4,ORANGE,blur),labels(sv))


def mark(h,col=GREEN,blur=False,dashed=False):
    cls=DashedLine if dashed else Line
    return cls([xp(h,blur),BASE,0],[xp(h,blur),1.8,0],color=col,stroke_width=5)


def sd_bracket(mu,sd,y,col,blur=False):
    x1,x2=xp(mu,blur),xp(mu+sd,blur)
    return VGroup(Line([x1,y,0],[x2,y,0],color=col,stroke_width=4),
        Line([x1,y-.12,0],[x1,y+.12,0],color=col),Line([x2,y-.12,0],[x2,y+.12,0],color=col),
        T(f'SD {sd:g} mm',26,col).move_to([(x1+x2)/2,y+.38,0]))


def question(blur=False):
    return VGroup(graph(8 if blur else 2),head('Predict. Where now?' if blur else 'Predict. Halfway?',YELLOW),
        mark(52,YELLOW,blur,True),T('?',36,YELLOW).move_to([xp(52,blur),2.0,0]))


def pause(scene,blur,seconds):
    scene.camera.background_color=BG
    scene.add(question(blur))
    if blur:
        scene.add(blur_icon(True))
    px = -3.7 if blur else 3.7
    label=T('Pause. Decide.',28,YELLOW).move_to([px,.9,0])
    ring=Circle(radius=.42,color=GREY).move_to([px,-.05,0])
    arc=Arc(radius=.42,start_angle=PI/2,angle=TAU,color=YELLOW).move_to(ring)
    scene.add(label,ring,arc)
    scene.play(Uncreate(arc),run_time=seconds,rate_func=linear)


def eye():
    return VGroup(Ellipse(width=1.8,height=.85,color=BLUE),Dot(radius=.23,color=BLUE))


def hand():
    return VGroup(RoundedRectangle(width=1.25,height=.85,corner_radius=.25,color=ORANGE,fill_color=ORANGE,fill_opacity=.2),
        *[Line([-.45+i*.3,.1,0],[-.45+i*.3,.65,0],color=ORANGE,stroke_width=9) for i in range(4)])


def rig():
    return VGroup(Rectangle(width=.9,height=4.8,color=GREY,fill_color=GREY,fill_opacity=.2),
        eye().move_to([-3.1,.9,0]),hand().move_to([.1,-1,0]),
        DashedLine([-2.15,.9,0],[-.48,.9,0],color=BLUE))


def blur_icon(blur=False):
    # A large continuous opacity envelope makes the lost bar edge visible.
    e=eye().scale(.95).move_to([-1.8,0,0])
    if blur:
        bar=VGroup(*[Rectangle(width=w,height=2.35,stroke_width=0,
            fill_color=BLUE,fill_opacity=o).move_to([.9,0,0])
            for w,o in [(w,.028*np.exp(-.5*(w/1.1)**2)) for w in np.linspace(.04,2.4,80)]])
    else:
        bar=Rectangle(width=.4,height=2.35,color=BLUE,fill_color=BLUE,fill_opacity=.9).move_to([.9,0,0])
    return VGroup(e,bar).move_to([3.65,.55,0])


def weights(w=.8,xs=(-2.5,2.5),base=-1.7,height=3.6):
    g=VGroup()
    for x,v,c,n in [(xs[0],w,BLUE,'vision'),(xs[1],1-w,ORANGE,'touch')]:
        g.add(VGroup(Rectangle(width=1.5,height=height*v,stroke_width=0,fill_color=c,fill_opacity=.8).move_to([x,base+height*v/2,0]),
            T(n,28,c).move_to([x,base-.45,0]),M(f'{v:.1f}',32,c).move_to([x,base+height*v+.38,0])))
    return g


def pulse(x0=-4.8,x1=4.8,y=-.8,amp=1.7):
    # Idealised self-generated input u(t); subtraction uses precisely the same u(t).
    ts=np.linspace(0,1,180)
    return VMobject(stroke_color=SELF,stroke_width=5).set_points_smoothly(
        [np.array([x0+(x1-x0)*t,y+amp*np.exp(-.5*((t-.5)/.12)**2),0]) for t in ts])


def self_picture(compact=False):
    if compact:
        h=hand().move_to([3.6,1.2,0])
        tr=pulse(1.2,5.8,-.9,1.2)
        arr=Arrow([3.6,.65,0],[3.6,-.15,0],color=ORANGE,buff=.05)
    else:
        h=hand().scale(1.5).move_to([-3.3,1.3,0])
        tr=pulse(-4.8,4.8,-1.2,1.7)
        arr=Arrow([-2.3,1.3,0],[-.2,.2,0],color=ORANGE,buff=.15)
    return VGroup(h,tr,arr)


class S00Title(TitleCard):
    LESSON='Combining Senses and Predicting Them'
    TITLE='Which Sense Do You Believe?'
    def construct(self):
        card=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28,GREY),
            T(self.TITLE,48,font=TITLE_FONT),Line(LEFT*1.3,RIGHT*1.3,color=GOLD)).arrange(DOWN,buff=.4)
        self.play(FadeIn(card),run_time=.6)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        r=rig()
        self.add(r[0],r[2])
        self.at('look at it')
        self.play(FadeIn(r[1]),Create(r[3]),run_time=.55)
        a=VGroup(Line([.46,1.3,0],[2.8,1.3,0],color=BLUE,stroke_width=5),T('eye',32,BLUE).move_to([3.7,1.3,0]))
        b=VGroup(Line([.46,2.05,0],[2.8,2.05,0],color=ORANGE,stroke_width=5),T('hand',32,ORANGE).move_to([3.7,2.05,0]))
        self.at('Your eyes')
        self.play(Create(a),run_time=.45)
        self.at('your hand')
        self.play(Create(b),run_time=.45)
        self.at('Which do you')
        self.play(FadeIn(T('Which do you believe?',40,YELLOW,font=TITLE_FONT).move_to([0,-3.05,0])),run_time=.45)
        self.finish()


class S02Nums(SpokenScene):
    def construct(self):
        self.add(axis(),head('Illustrative numbers'))
        self.at('Your eyes say')
        self.play(Create(mark(50,BLUE)),FadeIn(T('vision · 50 mm',28,BLUE).move_to([xp(50),2.48,0])),run_time=.6)
        self.at('Your hand says')
        self.play(Create(mark(54,ORANGE)),FadeIn(T('touch · 54 mm',28,ORANGE).move_to([xp(54),-3.5,0])),run_time=.6)
        self.finish()


class S03Wobble(SpokenScene):
    def construct(self):
        a,b=mark(50,BLUE),mark(54,ORANGE)
        labs=VGroup(T('vision · 50 mm',28,BLUE).move_to([xp(50),2.48,0]),T('touch · 54 mm',28,ORANGE).move_to([xp(54),-3.5,0]))
        self.add(axis(),head('Height likelihood for this trial'),a,b,labs)
        self.at('Each sense')
        self.play(a.animate.shift(LEFT*.12),b.animate.shift(RIGHT*.25),run_time=.35)
        self.play(a.animate.shift(RIGHT*.24),b.animate.shift(LEFT*.5),run_time=.35)
        self.play(Transform(a,mark(50,BLUE)),Transform(b,mark(54,ORANGE)),run_time=.35)
        self.at('Here vision')
        self.play(ReplacementTransform(a,curve(50,2,BLUE)),FadeOut(b),Transform(labs,VGroup(labels()[0])),run_time=.7)
        self.at('Its standard deviation')
        self.play(Create(sd_bracket(50,2,2.05,BLUE)),run_time=.5)
        self.finish()


class S04Touch(SpokenScene):
    def construct(self):
        self.add(axis(),head('Height likelihood for this trial'),curve(50,2,BLUE),labels()[0],sd_bracket(50,2,2.05,BLUE))
        self.at('Touch wobbles more')
        self.play(Create(curve(54,4,ORANGE)),FadeIn(labels()[1]),run_time=.7)
        self.at('standard deviation')
        self.play(Create(sd_bracket(54,4,.4,ORANGE)),run_time=.5)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        q=question()
        self.add(q[0])
        self.at('Predict')
        self.play(FadeIn(q[1]),Create(q[2]),FadeIn(q[3]),run_time=.6)
        self.finish()


class S06Pause(Scene):
    def construct(self):
        pause(self,False,5)


class S07Reveal(SpokenScene):
    def construct(self):
        q=question();self.add(q)
        self.at('It lands')
        self.play(FadeOut(q[1]),FadeOut(q[3]),Transform(q[2],mark(comb(2)[1])),run_time=1)
        self.at('at')
        self.play(FadeIn(head('50.8 mm · nearer vision',GREEN)),run_time=.45)
        self.finish()


class S08Weights(SpokenScene):
    def construct(self):
        self.add(head('Weights follow reliability'))
        vals=VGroup(chip('vision: variance 4 mm²',BLUE,30),chip('touch: variance 16 mm²',ORANGE,30)).arrange(RIGHT,buff=.8).move_to([0,2.25,0])
        self.add(vals)
        self.at('Each weight')
        self.play(Indicate(vals),run_time=.6)
        prec=VGroup()
        for x,h,col,s in [(-2.5,2.4,BLUE,'1/4'),(2.5,.6,ORANGE,'1/16')]:
            prec.add(VGroup(Rectangle(width=1.5,height=h,fill_color=col,fill_opacity=.8,stroke_width=0).move_to([x,-1.7+h/2,0]),M(s,32,col).move_to([x,-1.7+h+.4,0]),T('vision' if x<0 else 'touch',28,col).move_to([x,-2.15,0])))
        self.at('one over the variance')
        ratio=T('4 : 1\nprecision ratio',26,TEAL,line_spacing=1.3).move_to([0,.25,0])
        self.play(FadeIn(prec),FadeIn(ratio),run_time=.55)
        self.at('Vision gets')
        self.play(ReplacementTransform(prec,weights()),Transform(ratio,T('4/5 : 1/5',26,TEAL).move_to([0,.25,0])),run_time=.55)
        formula=VGroup(MarkupText('w<sub>V</sub> = (1/σ<sub>V</sub>²) / (1/σ<sub>V</sub>² + 1/σ<sub>H</sub>²)',font=FONT,font_size=32,color=TEAL),MarkupText('w<sub>H</sub> = 1 − w<sub>V</sub>',font=FONT,font_size=32,color=TEAL)).arrange(DOWN,buff=.18).move_to([0,-3.05,0])
        self.play(FadeIn(formula),run_time=.4)
        self.finish()


def step_bracket():
    # Enlarged inset of the 50-to-54 gap; the likelihood axis stays untruncated.
    y=2.05
    g=VGroup(Line([-4.2,y,0],[4.2,y,0],color=GREY,stroke_width=4))
    for x in np.linspace(-4.2,4.2,6):
        g.add(Line([x,y-.13,0],[x,y+.13,0],color=GREY,stroke_width=3))
    g.add(T('50',26,BLUE).move_to([-4.2,y+.48,0]),T('54',26,ORANGE).move_to([4.2,y+.48,0]),
        T('gap enlarged · five equal steps',26,GREY).move_to([2.1,1.5,0]))
    return g


class S09Move(SpokenScene):
    def construct(self):
        self.add(graph()[:3],head('Start at vision'),step_bracket())
        mk=mark(50);self.add(mk)
        self.at('Start at vision')
        self.play(Indicate(mk),run_time=.4)
        arrow=Arrow([-4.2,2.05,0],[-2.52,2.05,0],buff=0,color=GREEN,stroke_width=9,max_tip_length_to_length_ratio=.4)
        self.at('then move')
        self.play(Transform(mk,mark(50.8)),GrowArrow(arrow),FadeIn(T('one step = 0.8 mm',26,GREEN).move_to([-3.6,1.25,0])),run_time=.8)
        self.play(FadeIn(T('50 + 0.2 × (54 − 50) = 50.8 mm',30,GREEN).move_to([0,-3.5,0])),run_time=.4)
        self.finish()


class S10Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(graph()[:3],head('One fifth of the way toward touch'),step_bracket(),mark(50.8),
            Arrow([-4.2,2.05,0],[-2.52,2.05,0],buff=0,color=GREEN,stroke_width=9,max_tip_length_to_length_ratio=.4),
            T('50 + 0.2 × (54 − 50) = 50.8 mm',30,GREEN).move_to([0,-3.5,0]))
        self.wait(2)


class S11Narrow(SpokenScene):
    def construct(self):
        plot=VGroup(axis(),curve(50,2,BLUE),curve(54,4,ORANGE))
        labs=VGroup(T('vision · SD 2 mm',28,BLUE).move_to([2.7,2.55,0]),
            T('touch · SD 4 mm',28,ORANGE).move_to([2.7,1.98,0]),
            T('combined · SD 1.79 mm',28,GREEN).move_to([2.7,1.41,0]))
        self.add(head('The combined answer is steadier'),plot,labs[:2])
        cc=curve(comb(2)[1],comb(2)[2],GREEN)
        self.at('combined answer')
        self.play(Create(cc),FadeIn(labs[2]),run_time=.65)
        plot.add(cc)
        # Explicit second panel, after a full-size combined curve has been seen.
        small=VGroup(axis(sparse=True),curve(50,2,BLUE),curve(54,4,ORANGE),cc.copy()).stretch(.54,0).shift(LEFT*2.8)
        for p in small.get_family():
            if isinstance(p,Text):
                p.stretch(1/.54,0)
        bars=VGroup(T('variance (mm²)',28,GREY).move_to([3.5,2.0,0]))
        for i,(v,n,c) in enumerate([(16,'touch',ORANGE),(5,'halfway',GREY),(4,'vision',BLUE),(3.2,'weighted',GREEN)]):
            y=.95-i*.85
            bars.add(T(n,26,c).move_to([1.45,y,0]),Rectangle(width=v*.18,height=.4,stroke_width=0,fill_color=c,fill_opacity=.8).move_to([2.55+v*.09,y,0]),M(f'{v:g}',26,c).move_to([6,y,0]))
        tags=VGroup(T('vision · SD 2',22,BLUE),T('touch · SD 4',22,ORANGE),T('combined · SD 1.79',22,GREEN)).arrange(DOWN,buff=.2,aligned_edge=RIGHT).move_to([-1.2,1.6,0])
        self.at('steadier than either')
        self.play(Transform(plot,small),FadeOut(labs),FadeIn(tags),FadeIn(bars),run_time=.65)
        note=T('halfway = plain average of the two',26,GREY).move_to([3.45,-2.3,0])
        self.play(FadeIn(note),run_time=.25)
        self.at('if their errors')
        self.play(FadeIn(T('If the errors are independent',28,TEAL).move_to([0,-3.5,0])),run_time=.45)
        self.finish()


class S13Blur(SpokenScene):
    def construct(self):
        g=graph();pic=blur_icon()
        title=head('Now blur the picture')
        self.add(g,title,pic)
        self.at('blur the picture')
        self.play(Transform(g,graph(8)),Transform(pic,blur_icon(True)),run_time=1.6)
        self.at('Where does the answer')
        self.play(Transform(title,head('Predict. Where now?',YELLOW)),Create(mark(52,YELLOW,True,True)),
            FadeIn(T('?',36,YELLOW).move_to([xp(52,True),2,0])),run_time=.55)
        self.finish()


class S14Pause(Scene):
    def construct(self):
        pause(self,True,8)


class S15Swap(SpokenScene):
    def construct(self):
        self.add(graph(8),head('The weights swap'))
        mk=mark(52,YELLOW,True,True);self.add(mk)
        # Numerical derivation stays beside the curves throughout the reveal.
        nums=VGroup(T('variance: 64 and 16 mm²',26,TEAL),T('precision: 1/64 and 1/16',26,TEAL)).arrange(DOWN,buff=.22).move_to([3.15,1.55,0])
        bars=weights(.8,xs=(2.2,4.6),base=-.9,height=1.75)
        self.at('The weight swap')
        self.play(FadeIn(nums[0]),run_time=.3)
        self.play(FadeIn(nums[1]),run_time=.3)
        self.play(FadeIn(bars),run_time=.2)
        self.play(Transform(bars,weights(.2,xs=(2.2,4.6),base=-.9,height=1.75)),run_time=.55)
        self.at('The answer moves')
        self.play(Transform(mk,mark(comb(8)[1],GREEN,True)),run_time=1)
        self.at('much nearer touch')
        self.play(FadeIn(T('53.2 mm · nearer touch',30,GREEN).move_to([0,-3.5,0])),run_time=.45)
        self.finish()


class S16Alais(SpokenScene):
    def construct(self):
        sharp=Dot([-3,0,0],radius=.845,color=BLUE)
        blurred=VGroup(*[Circle(radius=r*1.3,stroke_width=0,fill_color=BLUE,fill_opacity=o).move_to([-3,0,0]) for r,o in [(1.9,.025),(1.7,.035),(1.5,.05),(1.3,.07),(1.1,.08),(.9,.09),(.7,.1),(.5,.1)]])
        speaker=VGroup(Rectangle(width=.8,height=1.8,color=PURPLE),Polygon([.4,.9,0],[1.5,1.6,0],[1.5,-1.6,0],[.4,-.9,0],color=PURPLE,fill_color=PURPLE,fill_opacity=.3)).scale(1.3).move_to([3,0,0])
        marker=Triangle(color=YELLOW,fill_opacity=1).scale(.24).rotate(PI).move_to([-3,-2.75,0])
        label=T('perceived location',28,YELLOW).move_to([-3,-3.35,0])
        self.add(head('Alais and Burr, 2004'),sharp,speaker,marker,label,T('schematic',22,GREY).move_to([0,2.65,0]))
        self.at('sound and sight')
        self.play(FadeIn(T('sight',30,BLUE).move_to([-3,2.75,0])),FadeIn(T('sound',30,PURPLE).move_to([3,2.75,0])),run_time=.45)
        self.at('Severe blur')
        self.play(ReplacementTransform(sharp,blurred),run_time=.4)
        self.at('let sound capture')
        self.play(marker.animate.move_to([3,-2.75,0]),label.animate.move_to([3,-3.35,0]),run_time=.4)
        self.finish()


def mini_rig(y,sight,touch,name):
    bar=Rectangle(width=.5,height=1.35,color=GREY,fill_color=GREY,fill_opacity=.25).move_to([2.6,y,0])
    e=eye().scale(.6).move_to([.1,y+.15,0]).set_opacity(1 if sight else .12)
    h=hand().scale(.65).move_to([3.5,y-.12,0]).set_opacity(1 if touch else .12)
    link=DashedLine([.75,y+.15,0],[2.32,y+.15,0],color=BLUE).set_opacity(1 if sight else .12)
    panel=Rectangle(width=.55,height=.85,color=BLUE,fill_color=BG,fill_opacity=1).move_to([1.55,y+.15,0]).set_opacity(1 if sight else .12)
    noise=VGroup(*[Dot([1.35+(i%3)*.2,y-.1+(i//3)*.2,0],radius=.032,color=BLUE) for i in range(9)]).set_opacity(1 if sight else 0)
    return VGroup(bar,e,h,link,panel,noise,T(name,28,GREEN if sight and touch else BLUE if sight else ORANGE).move_to([5.1,y,0]))


class S18Eb(SpokenScene):
    def construct(self):
        rigs=VGroup(mini_rig(1.85,True,False,'sight only'),mini_rig(0,False,True,'touch only'),mini_rig(-1.85,True,True,'both'))
        observers=VGroup(*[VGroup(Circle(radius=.18,color=GREY),RoundedRectangle(width=.45,height=.65,corner_radius=.12,color=GREY).shift(DOWN*.55)) for _ in range(4)]).arrange(RIGHT,buff=.22).move_to([-3.5,.2,0])
        self.add(head('Ernst and Banks, 2002'),observers,T('4 observers',30,GREY).move_to([-3.5,1.4,0]))
        self.at('tested the rule')
        self.play(FadeIn(rigs),run_time=.65)
        self.at('judging bar height')
        branches=VGroup(*[Arrow([-2,.2,0],[-1.05,y,0],color=GREY,buff=.08,stroke_width=3) for y in (1.85,0,-1.85)])
        self.play(*[GrowArrow(a) for a in branches],run_time=.45)
        self.at('by sight')
        self.play(FadeIn(T('noise on visual panel',28,BLUE).move_to([1.8,-3.35,0])),Indicate(rigs[0][4]),Indicate(rigs[2][4]),run_time=.5)
        self.finish()


class S19Eb2(SpokenScene):
    def construct(self):
        def xy(v):
            return np.array([-4.6+(v-50)*2.0,-1.8+(v-50)*1.05,0])
        ax=VGroup(Line([-4.9,-2,0],[3,-2,0],color=GREY),Line([-4.9,-2,0],[-4.9,2.3,0],color=GREY))
        identity=DashedLine(xy(50),xy(53.6),color=GREY,stroke_opacity=.4)
        self.add(head('Maximum-likelihood model'),ax,identity,
            T('predicted (arbitrary units)',26,GREEN).move_to([-1,-2.65,0]),
            T('measured (arbitrary units)',26,GREY).rotate(PI/2).move_to([-5.7,.1,0]),
            T('schematic, not data',26,GREY).move_to([0,-3.45,0]))
        pts=VGroup(*[Dot(xy(comb(s)[1]),radius=.1,color=GREEN) for s in (1,2,4,8)])
        # Small illustrative offsets express resemblance, never actual measurements.
        offsets=[[-.08,.17,0],[.1,-.16,0],[-.12,.18,0],[.12,-.13,0]]
        rings=VGroup(*[Circle(radius=.18,color=TEXT,stroke_width=3).move_to(p.get_center()+np.array(d)) for p,d in zip(pts,offsets)])
        box=RoundedRectangle(width=3.65,height=3.1,corner_radius=.15,color=GREY,fill_color=BG,fill_opacity=1).move_to([4.55,.1,0])
        model_key=VGroup(Square(side_length=.20,color=GREEN,fill_color=GREEN,fill_opacity=1).move_to([3.15,1.1,0]),
            T('model prediction',24,GREEN).move_to([4.8,1.1,0]),T('from single senses',22,GREEN).move_to([4.6,.6,0]))
        measured_key=VGroup(Circle(radius=.18,color=TEXT).move_to([3.15,-.35,0]),
            T('measured',24).move_to([4.75,-.15,0]),T('combined judgement',22).move_to([4.7,-.65,0]))
        self.at('Predictions built')
        self.play(FadeIn(pts),FadeIn(box),FadeIn(model_key),run_time=.65)
        self.at('closely resembled')
        self.play(FadeIn(rings),FadeIn(measured_key),run_time=.65)
        self.finish()


class S20Scope(SpokenScene):
    def construct(self):
        self.add(head('What this test can and cannot show'))
        self.at('One task')
        self.play(FadeIn(chip('one task',GREY,38,pad=.35).move_to([0,1.95,0])),run_time=.35)
        self.at('four people')
        self.play(FadeIn(chip('four people',GREY,38,pad=.35).move_to([0,.4,0])),run_time=.35)
        self.at('a behavioral fit')
        self.play(FadeIn(chip('a behavioural fit',GREEN,38,pad=.35).move_to([0,-1.15,0])),run_time=.35)
        self.at('It does not show')
        self.play(FadeIn(T('Where in the brain? Not shown.',32,RED).move_to([0,-2.95,0])),run_time=.5)
        self.finish()


class S21Turn(SpokenScene):
    def construct(self):
        old=graph();pic=self_picture()
        self.add(head('Some sensory input is caused by you'),old)
        self.at('Now one more fact')
        self.play(FadeOut(old),FadeIn(pic[0]),run_time=.65)
        self.add(T('hand sweeping in air',28,ORANGE).move_to([-3.3,2.55,0]),
            T('touching to measure is different',28,GREY).move_to([0,-3.35,0]))
        self.at('Some of what')
        self.play(pic[0].animate.shift(RIGHT*1.2),Create(pic[1]),GrowArrow(pic[2]),
            FadeIn(T('input caused by your own movement',28,SELF).move_to([0,-2.3,0])),run_time=1.1)
        self.finish()


class S22Rule1(SpokenScene):
    def construct(self):
        signal=chip('signal',TEAL,38,pad=.4).move_to([-3.8,.4,0])
        gauge=VGroup(Rectangle(width=5.3,height=.7,color=GREY),T('tells you about the world',30).move_to([0,1,0])).move_to([2,.65,0])
        fill=Rectangle(width=.2,height=.6,fill_color=GREEN,fill_opacity=.8,stroke_width=0).move_to([-.5,.3,0])
        self.add(head('One idea'),signal,gauge,
            ct('A signal is worth what it tells you\nabout the world.',34,font=TITLE_FONT,line_spacing=1.2).move_to([0,-2.4,0]))
        self.at('A signal is worth')
        self.play(GrowArrow(Arrow([-2.4,.4,0],[-.9,.4,0],color=SELF,buff=.1)),FadeIn(fill),run_time=.55)
        self.at('tells you about')
        self.play(fill.animate.stretch_to_fit_width(4.8).move_to([2,.3,0]),run_time=.7)
        self.finish()


class S23Rule2(SpokenScene):
    def construct(self):
        bars=weights(.5,base=-1.5,height=3.6)
        self.add(head('One event · reliability sets the weights'),bars,
            ct('For one event, the more reliable sense\ncounts for more.',32,GREEN,line_spacing=1.2).move_to([0,-3,0]))
        self.at('For one event')
        self.play(Indicate(bars),run_time=.45)
        self.at('the more reliable')
        self.play(Transform(bars,weights(.8,base=-1.5,height=3.6)),run_time=.85)
        self.finish()


class S24Rule3(SpokenScene):
    def construct(self):
        pic=self_picture();tr=pic[1]
        self.add(head('Some pathways subtract a prediction'),pic[0],tr,pic[2],
            T('self-caused input · schematic',28,SELF).move_to([1.2,2.65,0]),
            ct('Some pathways subtract a prediction\nof what your own movement causes.',32,TEAL,line_spacing=1.2).move_to([0,-2.9,0]))
        self.at('Part of what')
        self.play(pic[0].animate.shift(RIGHT*1.1),run_time=.7)
        self.at('Some pathways subtract')
        # Keep the original input as a visible before-state while equal pulses cancel.
        ghost=tr.copy().set_stroke(color=GREY,width=3,opacity=.4)
        prediction=pulse(-4.8,4.8,-1.2,1.7).set_stroke(color=TEAL,width=4)
        prediction.shift(UP*1.3)
        tag=T('− prediction',28,TEAL).move_to([3.9,1.45,0])
        self.play(Create(prediction),FadeIn(tag),FadeOut(pic[0]),FadeOut(pic[2]),run_time=.45)
        self.add(ghost)
        self.at('a prediction of it')
        self.play(prediction.animate.shift(DOWN*1.3),run_time=.35)
        self.play(Transform(tr,pulse(-4.8,4.8,-1.2,0)),
            Transform(prediction,pulse(-4.8,4.8,-1.2,0).set_stroke(color=TEAL,width=4)),run_time=.55)
        self.finish()


class S25Take(SpokenScene):
    def construct(self):
        bars=weights(.8,xs=(-4.5,-2.2),base=-1.5,height=3.5)
        pic=self_picture(True)
        left=ct('Weigh each sense\nby its reliability.',30,GREEN,line_spacing=1.2).move_to([-3.4,-2.8,0])
        right=ct('Which predictable results\nget subtracted?',30,TEAL,line_spacing=1.2).move_to([3.4,-2.8,0])
        self.add(head('Take this with you'),bars,pic,left,right)
        self.at('Weigh each sense')
        self.play(Indicate(bars),run_time=.5)
        self.play(Transform(bars,weights(.2,xs=(-4.5,-2.2),base=-1.5,height=3.5)),run_time=.7)
        self.at('then ask which')
        self.play(pic[0].animate.shift(RIGHT*.5),GrowArrow(Arrow([5.7,1.7,0],[5.7,-.4,0],color=SELF,buff=.1)),
            FadeIn(T('− prediction?',28,SELF).move_to([3.5,2.3,0])),run_time=.7)
        self.play(Transform(pic[1],pulse(1.2,5.8,-.9,0)),run_time=.8)
        self.finish()


class S26End(EndCard):
    # Preserve the closing question's conditional scope rather than assert universal cancellation.
    LINE='Weigh each sense by reliability; ask which self-caused results get subtracted.'
    def construct(self):
        line=ct('Weigh each sense by reliability.\nAsk which self-caused results get subtracted.',36,font=TITLE_FONT,line_spacing=1.3)
        self.play(FadeIn(line),run_time=.6)
        self.add(T('biochemistrypedia.com',26,TEAL).move_to([0,-1.8,0]))
        self.finish()
