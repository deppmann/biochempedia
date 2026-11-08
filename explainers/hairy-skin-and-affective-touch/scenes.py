"""Chapter 1, reviewer fix round.
COLOR MAP: YELLOW stimulus / caress band / next-chapter handoff;
GREEN human CT firing; PURPLE pleasantness; BLUE recording electrode;
RED unsupported causal link; GREY anatomy, axes, myelinated comparisons.
All traces are computed model shapes, not digitised data. The counterexample
uses A=.95(1-exp(-4t))/(1-exp(-4)), B=.95t, and exactly A-B, on ONE scale.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'


def bell(x):
    return float(np.exp(-((x-.5)/.62)**2))


def rise(x):
    return .12+.76*(x+1)/3


def heading(s, color=TEXT):
    return T(s, 32, color).move_to([0,3.35,0])


def note(s='model shapes; no numerical firing scale'):
    return T(s,26,GREY).move_to([0,-3.65,0])


def skin():
    arm=Polygon([-5.6,-.8,0],[-5.6,.25,0],[-3.9,.55,0],[4.6,.65,0],
                [5.6,.35,0],[5.6,-1.2,0],[4.5,-1.4,0],[-3.9,-1.1,0],
                color=GREY,fill_opacity=.18,stroke_width=3)
    hairs=VGroup(*[Line([x,.5,0],[x+.13,1.05,0],color=GREY,stroke_width=3)
                   for x in np.linspace(-4.5,4.5,13)])
    labels=VGroup(T('forearm (hairy skin)',28).move_to([0,-.45,0]),
                  T('wrist',26,GREY).move_to([-5,-1.65,0]),
                  T('elbow',26,GREY).move_to([5,-1.65,0]))
    return VGroup(arm,hairs,labels)


def brush(x=-4.5):
    handle=Line([x,2.65,0],[x,1.9,0],color=YELLOW,stroke_width=9)
    head=RoundedRectangle(width=.95,height=.28,corner_radius=.06,
                          color=YELLOW,fill_opacity=.5).move_to([x,1.75,0])
    br=VGroup(*[Line([x+d,1.6,0],[x+d,.7,0],color=YELLOW,stroke_width=3)
                for d in np.linspace(-.38,.38,8)])
    return VGroup(handle,head,br)


def path():
    return VGroup(Line([-4.5,-2.05,0],[4.5,-2.05,0],color=GREY),
                  *[Line([x,-1.94,0],[x,-2.16,0],color=GREY)
                    for x in np.linspace(-4.5,4.5,11)],
                  Dot([-4.5,.5,0],color=YELLOW),Dot([4.5,.5,0],color=YELLOW),
                  M('10 cm',28).move_to([0,-2.5,0]))


class TimerGlyph(Text):
    def __init__(self, text, **kwargs):
        super().__init__(text, font=MONO, **kwargs)


def timer(v):
    # DecimalNumber otherwise falls back to a serif font for the digit glyphs.
    return DecimalNumber(v,num_decimal_places=2,mob_class=TimerGlyph,
                         font_size=36,color=YELLOW).move_to([-.4,-3.15,0])


def person(c):
    return VGroup(Circle(.3,color=c,fill_opacity=.25).move_to([0,.75,0]),
                  RoundedRectangle(width=.95,height=1.35,corner_radius=.3,
                                   color=c,fill_opacity=.18).move_to([0,-.3,0]))


class Plot:
    def __init__(self,cx=0,cy=-.05,w=10.5,h=4.8,label='CT afferents',
                 color=GREEN,ylabel='firing (model shape)'):
        self.cx,self.cy,self.w,self.h=cx,cy,w,h
        self.axes=VGroup(Line(self.p(-1,0),self.p(2,0),color=GREY),
                         Line(self.p(-1,0),self.p(-1,1.03),color=GREY))
        ticks=VGroup(*[M(s,26,GREY).move_to(self.p(x,0)+DOWN*.31)
                      for x,s in [(-.522878745,'0.3'),(.477121255,'3'),(1.477121255,'30')]])
        yl=T(ylabel,26,GREY).rotate(PI/2).move_to([cx-w/2-.55,cy,0])
        self.title=T(label,28,color).move_to([cx,cy+h/2+.43,0])
        self.frame=VGroup(self.axes,ticks,
                          T('speed (cm/s, log)',26,GREY).move_to([cx,cy-h/2-.77,0]),
                          self.title,yl)
        self.band=Rectangle(width=w/3,height=h,stroke_width=0,
                            fill_color=YELLOW,fill_opacity=.12).move_to(self.p(.5,.5))
        self.bandlabel=T('1–10 cm/s',26,YELLOW).move_to(self.p(.5,.88))
    def p(self,x,y):
        return np.array([self.cx-self.w/2+(x+1)/3*self.w,
                         self.cy-self.h/2+y*self.h,0])
    def curve(self,f=bell,c=GREEN):
        return ParametricFunction(lambda x:self.p(x,f(x)),t_range=[-1,2,.012],
                                  color=c,stroke_width=5)


def pair():
    l=Plot(-3.25,w=4.65,label='CT firing')
    r=Plot(3.25,w=4.65,label='average pleasantness',color=PURPLE,
           ylabel='pleasantness rating\n(model shape)')
    return l,r


def prediction(second=False):
    l,r=pair()
    l.title.become(T('myelinated afferents recorded',26,GREY).move_to([-3.25,2.65,0]))
    r.title.become(T('CT curve?',28,GREEN).move_to([3.25,2.65,0]))
    # Both axes measure firing; the empty right panel is the student's workspace.
    r.frame[-1].become(T('firing (model shape)',26,GREY).rotate(PI/2).move_to([.375,-.05,0]))
    box=DashedVMobject(Rectangle(width=4.4,height=4.35,color=GREEN,
                       stroke_width=2).move_to([3.25,-.25,0]),num_dashes=50)
    prompt='What shape would show a preference?' if second else 'If CT fibres worked the same way, what shape?'
    return VGroup(l.frame,l.curve(rise,GREY),r.frame,box,heading(prompt),note())


def ct_frame(takeaway=False):
    p=Plot()
    title=heading('The shape, not a higher firing rate, sets CT apart',GREEN) if takeaway else heading('A preferred stroke speed')
    # Band text is inside the band but below the peak, with a clear background.
    bandlabel=T('1–10 cm/s',26,YELLOW).move_to(p.p(.5,.72))
    return VGroup(p.band,p.frame,p.curve(),bandlabel,title,note())


def logic():
    l=Plot(-3.65,w=3.8,label='myelinated firing',color=GREY)
    r=Plot(3.65,w=3.8,label='ratings',color=PURPLE,ylabel='predicted rating')
    arrow=Arrow([-1.4,.1,0],[.8,.1,0],color=GREY,buff=.05)
    return l,r,VGroup(l.frame,l.curve(rise,GREY),r.frame,arrow,
                      T('read-out',26).move_to([-.3,.65,0]),note())


def idea(stage=0):
    # Separate axes preserve the distinction between firing and rated pleasantness.
    l=Plot(-3.45,cy=-.15,w=4.3,h=4.0,label='CT firing')
    r=Plot(3.25,cy=-.15,w=4.3,h=4.0,label='average pleasantness',color=PURPLE,
           ylabel='pleasantness rating\n(model shape)')
    g=VGroup(heading('CT input: prime candidate for pleasant touch',GREEN) if stage else heading('The one idea'),
             l.band,l.frame,l.curve(),
             VGroup(),  # Reserved for the final removal cue; no stray comparison caption.
             note('Recorded classes • soft-brush strokes • group averages'))
    if stage>=1:
        g.add(r.band,r.frame,r.curve(c=PURPLE))
    else:
        g.add(T('Human hairy skin',32).move_to([3.2,.65,0]),
              T('Tuned to\ncaress speeds',32,GREEN).move_to([3.2,-.7,0]))
    return l,r,g


class S00Title(TitleCard):
    LESSON='Hairy Skin, Stroking and Affective Touch'
    TITLE='The Fibre That Prefers a Caress'


class S01Q(SpokenScene):
    def construct(self):
        self.add(skin(),heading('Does a fibre’s speed preference explain a caress?'))
        b=brush(); self.add(b)
        self.at('Brush a forearm'); self.play(b.animate.shift(RIGHT*2.7),run_time=1.3,rate_func=linear)
        self.at('then at a caress'); self.play(b.animate.shift(RIGHT*3.2),run_time=.65,rate_func=linear)
        self.at('then fast'); self.play(b.animate.shift(RIGHT*3.1),run_time=.25,rate_func=linear)
        self.at('One touch'); self.play(FadeIn(T('One touch fibre seems to care how fast you stroke',30).move_to([0,-2.5,0])),run_time=.4)
        self.at('Could that be'); self.play(FadeIn(T('Could that explain why a caress feels nice?',30).move_to([0,-3.25,0])),run_time=.4)
        self.finish()


class S02Path(SpokenScene):
    def construct(self):
        self.add(skin(),brush(4.5),heading('Put the speeds in your hand'))
        self.at('Mark a'); self.play(Create(path()),run_time=.9); self.finish()


class S03Caress(SpokenScene):
    def construct(self):
        b=brush(); self.add(skin(),path(),b,heading('3 cm/s • a slow caress',YELLOW))
        t=timer(0); self.add(t,M('s',28,YELLOW).move_to([.85,-3.15,0]))
        self.at('a brush crosses'); self.play(b.animate.shift(RIGHT*9),ChangeDecimalToValue(t,10/3),run_time=10/3,rate_func=linear)
        self.finish()


class S04Swipe(SpokenScene):
    def construct(self):
        b=brush(); t=timer(0)
        arm=VGroup(skin(),path(),b,t,M('s',28,YELLOW).move_to([.85,-3.15,0]))
        h=heading('30 cm/s • quick swipe',YELLOW); self.add(arm,h)
        self.at('Ten times faster')
        # 0.33 s of physical time is shown for 1.33 s, so the motion is readable.
        slow=T('shown at one quarter speed',26,YELLOW).move_to([0,2.85,0])
        self.add(slow)
        self.play(b.animate.shift(RIGHT*9),ChangeDecimalToValue(t,1/3),run_time=4/3,rate_func=linear)
        self.at('Ten times slower'); self.remove(h,slow,b,t)
        b=brush(); t=timer(0); crawl=heading('0.3 cm/s • crawl • time-lapse ×22',YELLOW)
        self.add(b,t,crawl)
        self.play(b.animate.shift(RIGHT*9),ChangeDecimalToValue(t,100/3),run_time=1.5,rate_func=linear)
        self.at('over half'); self.clear()
        rows=VGroup(*[VGroup(M(v,34,YELLOW),T(desc,30),M(tm,34,YELLOW)).arrange(RIGHT,buff=.7)
                      for v,desc,tm in [('30 cm/s','quick swipe','0.33 s'),('3 cm/s','slow caress','3.3 s'),('0.3 cm/s','crawl','33 s')]]).arrange(DOWN,buff=.65)
        self.add(heading('The same 10 cm path'),rows,T('physical crossing times',28,GREY).move_to([0,-2.65,0]))
        self.finish()


class S05Ltmr(SpokenScene):
    def construct(self):
        self.add(heading('Low-threshold mechanoreceptor (LTMR)'),
                 T('a sensory neuron responding to gentle force',30).move_to([0,2.45,0]))
        fast=Line([-5.2,.5,0],[5.2,.5,0],color=GREY,stroke_width=5)
        wraps=VGroup(*[RoundedRectangle(width=1.1,height=.55,corner_radius=.16,color=GREY,
                             fill_opacity=.35).move_to([x,.5,0]) for x in [-4,-2,0,2,4]])
        slow=Line([-5.2,-2,0],[5.2,-2,0],color=GREEN,stroke_width=3)
        self.add(fast,wraps,slow,
                 T('fast • myelinated',30,GREY).move_to([0,1.3,0]),
                 T('myelin',28,GREY).move_to([2,-.25,0]),
                 Line([2,.05,0],[2,.25,0],color=GREY),
                 T('slow • unmyelinated',30,GREEN).move_to([0,-1.3,0]),
                 T('Hairy skin contains both',30).move_to([0,-3.1,0]))
        self.at('fast'); f=Dot(fast.get_start(),color=TEXT); self.add(f)
        self.play(MoveAlongPath(f,fast),run_time=.45,rate_func=linear)
        self.at('and slow'); d=Dot(slow.get_start(),color=GREEN); self.add(d)
        self.play(MoveAlongPath(d,slow),run_time=1.15,rate_func=linear)
        self.finish()



class S06Ct(SpokenScene):
    def construct(self):
        self.add(heading('C-tactile (CT) afferent',GREEN),
                 T('human sensory neuron',28).move_to([0,2.65,0]))
        fast=Line([-5,.7,0],[5,.7,0],color=GREY,stroke_width=3)
        wraps=VGroup(*[RoundedRectangle(width=1.1,height=.5,corner_radius=.15,color=GREY,
                        fill_opacity=.3).move_to([x,.7,0]) for x in [-4,-2,0,2,4]])
        ax=Line([-5,-2.1,0],[5,-2.1,0],color=GREEN,stroke_width=3)
        self.add(fast,wraps,ax,T('myelinated • fast comparison',28,GREY).move_to([0,1.65,0]))
        self.at('with a thin'); self.play(FadeIn(T('CT • thin, unmyelinated axon',30,GREEN).move_to([0,-1.3,0])),run_time=.4)
        self.at('It conducts slowly')
        d=Dot(ax.get_start(),radius=.13,color=GREEN); f=Dot(fast.get_start(),radius=.13,color=TEXT)
        self.add(d,f,T('same distance • schematic timing',28,GREY).move_to([0,-3.45,0]))
        self.play(MoveAlongPath(d,ax,run_time=1.5,rate_func=linear),
                  Succession(MoveAlongPath(f,fast,run_time=.35,rate_func=linear),
                             FadeIn(T('fast • arrived',26,GREY).move_to([4.5,.05,0]),run_time=.15),Wait(1)),run_time=1.5)
        self.add(T('slow • arrived',26,GREEN).move_to([4.5,-2.75,0]))
        self.finish()


def recording():
    # A continuous fibre connects the receptive field to the peripheral nerve.
    sk=RoundedRectangle(width=7,height=1.15,corner_radius=.2,color=GREY,
                         fill_opacity=.15).move_to([-2.6,1.25,0])
    hairs=VGroup(*[Line([x,1.8,0],[x+.1,2.18,0],color=GREY) for x in np.linspace(-5.6,.3,12)])
    field=Ellipse(width=2.2,height=.65,color=GREEN,fill_opacity=.15).move_to([-3,1.5,0])
    nerve=RoundedRectangle(width=7,height=1,corner_radius=.2,color=GREY,
                            fill_opacity=.15).move_to([-2.6,-1.45,0])
    ax=VMobject(color=GREEN,stroke_width=3).set_points_as_corners([[-3,1.2,0],[-3,-1.45,0],[.8,-1.45,0]])
    electrode=Line([.8,.75,0],[-.6,-1.45,0],color=BLUE,stroke_width=5)
    wire=VMobject(color=BLUE,stroke_width=3).set_points_as_corners([[.8,.75,0],[1.5,.75,0],[1.5,-.4,0],[2,-.4,0]])
    # Seeded inhomogeneous Poisson model, gated to field occupancy.
    grid=np.linspace(0,1,2001)
    rate=np.where((grid>=.32)&(grid<=.72),11+24*np.exp(-((grid-.52)/.1)**2),0)
    hazard=np.cumsum(rate)/2000
    thresholds=np.cumsum(np.random.default_rng(9).exponential(size=40))
    events=np.interp(thresholds[thresholds<hazard[-1]],hazard,grid)
    raster=VGroup(*[Line([2+4*t,-.9,0],[2+4*t,.1,0],color=GREEN,stroke_width=4) for t in events])
    labels=VGroup(T('forearm skin',28).move_to([-.8,1.0,0]),
                  T('receptive field',28,GREEN).move_to([-4.65,-.35,0]),
                  Line([-4.65,-.05,0],[-3.75,1.3,0],color=GREEN),
                  T('skin nerve',28).move_to([-4.65,-2.3,0]),
                  T('one axon',28,GREEN).move_to([-1.4,-2.3,0]),
                  T('electrode',28,BLUE).move_to([1,2.2,0]),
                  Line([.95,1.95,0],[.8,.75,0],color=BLUE),
                  T('spikes from\none axon',28,GREEN).move_to([4,1.15,0]),
                  Line([2,-1.15,0],[6,-1.15,0],color=GREY),
                  Arrow([2,-1.6,0],[6,-1.6,0],color=GREY,buff=0),
                  T('time →',26,GREY).move_to([4,-2.1,0]))
    raster.event_times=events
    return VGroup(sk,hairs,field,nerve,ax,labels),VGroup(electrode,wire),raster


class S07Micro(SpokenScene):
    def construct(self):
        base,e,r=recording(); self.add(base,heading('Microneurography',BLUE))
        self.at('records single axons'); self.play(Create(e),run_time=.55)
        self.play(LaggedStart(*[Create(t) for t in r],lag_ratio=.12),run_time=1)
        self.at('in an awake'); self.play(FadeIn(T('recording from an awake person',28).move_to([0,-3.2,0])),run_time=.4)
        self.finish()


class S08Loken(SpokenScene):
    def construct(self):
        base,e,r=recording(); self.add(base,e,heading('Microneurography',BLUE))
        self.at('and colleagues'); self.play(FadeIn(T('Löken, Wessberg, Morrison, McGlone and Olausson, 2009',26).move_to([0,-3.25,0])),run_time=.4)
        self.at('while a soft')
        # Brush lane ends left of the electrode. Spikes occur ONLY in the field.
        b=brush().scale(.5); b.move_to([-5.5,1.99,0]); self.add(b)
        speed=T('3 cm/s',28,YELLOW).move_to([-5.1,2.95,0]); self.add(speed)
        self.play(b.animate.shift(RIGHT*1.4),run_time=.4,rate_func=linear)
        r.set_opacity(0); self.add(r)
        def reveal_spikes(group, alpha):
            for tick,t in zip(group,group.event_times):
                tick.set_opacity(1 if alpha >= (t-.32)/.4 else 0)
        self.play(b.animate.shift(RIGHT*2.2),UpdateFromAlphaFunc(r,reveal_spikes),run_time=1.3,rate_func=linear)
        # Stop at the field edge as the field-gated raster finishes.
        self.finish()


class S09Myel(SpokenScene):
    def construct(self):
        p=Plot(label='myelinated afferents recorded',color=GREY)
        self.add(p.frame,note())
        self.at('fired harder'); self.play(Create(p.curve(rise,GREY)),run_time=1.4); self.finish()


class S10Predict(SpokenScene):
    def construct(self):
        g=prediction(); self.add(*g[:4],g[-1])
        self.at('Predict'); self.play(FadeIn(g[4]),run_time=.4)
        self.at('What shape would show')
        self.remove(g[4])
        self.add(heading('What shape would show a preference?'))
        self.finish()


class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        g=prediction(True); self.add(g)
        self.remove(g[-1]); self.add(T('Pause. Sketch the curve.',28,YELLOW).move_to([0,-3.65,0]))
        # Hold the question still; a newly drawn progress bar began as a stray dot.
        self.wait(5)


class S12Reveal(SpokenScene):
    def construct(self):
        p=Plot(); self.add(p.frame,heading('A preferred stroke speed'),note())
        self.at('firing traced'); self.play(Create(p.curve()),run_time=1.1)
        self.at('It was highest'); self.play(FadeIn(p.band),FadeIn(T('1–10 cm/s',26,YELLOW).move_to(p.p(.5,.72))),run_time=.5)
        self.finish()


class S13Shape(SpokenScene):
    def construct(self):
        self.add(ct_frame(True))
        p=Plot()
        arrows=VGroup(Arrow(p.p(-.2,.35)+LEFT*.45,p.p(-.75,.04)+LEFT*.45,color=GREEN,buff=.04),
                      Arrow(p.p(1.2,.35)+RIGHT*.45,p.p(1.75,.04)+RIGHT*.45,color=GREEN,buff=.04))
        self.at('Slower and faster'); self.play(Create(arrows),run_time=.5); self.finish()


class S14Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(ct_frame(True)); self.wait(2.5)


class S15Ratings(SpokenScene):
    def construct(self):
        l,r=pair(); self.add(l.band,l.frame,l.curve(),note())
        pp=person(PURPLE).scale(.65).move_to([1.75,.85,0])
        # A temporary rating instrument occupies the future rating panel.
        scale=VGroup(Line([2.8,-1.2,0],[5.4,-1.2,0],color=PURPLE),
                     *[Line([x,-1.05,0],[x,-1.35,0],color=PURPLE) for x in np.linspace(2.8,5.4,5)],
                     T('-10',26,PURPLE).move_to([2.8,-1.65,0]),T('+10',26,PURPLE).move_to([5.4,-1.65,0]),
                     T('unpleasant → pleasant',26,PURPLE).move_to([3.6,-2.3,0]),
                     T('different volunteers',28,PURPLE).move_to([3.25,2.65,0]))
        b=VGroup(brush().scale(.5).move_to([3.8,.9,0]),
                 RoundedRectangle(width=2.7,height=.35,corner_radius=.1,color=GREY,fill_opacity=.18).move_to([4.2,.2,0]))
        self.at('A separate group'); self.play(FadeIn(pp),FadeIn(scale),run_time=.4)
        self.at('rated the same'); self.add(b); self.play(b.animate.shift(RIGHT*.8),run_time=.6)
        self.at('Their average pleasantness'); self.play(FadeOut(pp),FadeOut(scale),FadeOut(b),FadeIn(r.frame),run_time=.35)
        self.play(Create(r.curve(c=PURPLE)),run_time=1)
        self.at('highest over'); self.play(FadeIn(r.band),run_time=.4); self.finish()


class S16Only(SpokenScene):
    def construct(self):
        l,r=pair(); self.add(l.band,l.frame,l.curve(),r.band,r.frame,r.curve(c=PURPLE),note())
        # Two schematic rising comparisons represent the recorded myelinated classes.
        grey=VGroup(l.curve(rise,GREY),
                    DashedVMobject(l.curve(lambda x:.8*rise(x)+.12,GREY),num_dashes=24))
        labels=VGroup(T('myelinated\n(recorded classes)',24,GREY).move_to([-1.4,2.25,0]),
                      Line([-1.4,1.91,0],l.p(1.8,rise(1.8)),color=GREY),
                      T('CT ✓',34,GREEN).move_to([-4.5,2.05,0]))
        self.at('Of the'); self.play(Create(grey),FadeIn(labels),run_time=.5)
        self.at('only the'); self.play(Indicate(l.curve(),color=GREEN),Indicate(r.curve(c=PURPLE),color=PURPLE),run_time=.6)
        self.add(T('Of the recorded classes',28,GREEN).move_to([-3.25,3.35,0]),
                 T('✓ same rated shape',28,PURPLE).move_to([3.25,3.35,0]))
        self.finish()


class S17Logic(SpokenScene):
    def construct(self):
        l,r,g=logic(); h=heading('Why does the shape matter?'); self.add(g,h)
        self.at('Suppose only'); self.play(Transform(h,heading('Suppose rising firing drove the ratings…')),run_time=.4)
        self.finish()


class S18Logic2(SpokenScene):
    def construct(self):
        l,r,g=logic(); self.add(g,heading('More firing → more pleasant?'))
        c=r.curve(rise,GREY)
        self.at('ratings would rise'); self.play(Create(c),run_time=.7)
        pred=T('predicted if\nfiring alone\ndrove it',26,GREY).move_to([5.65,0,0])
        lead=Line([5.4,.6,0],r.p(1.8,rise(1.8)),color=GREY)
        self.add(pred,lead)
        self.at('They do not')
        actual=VGroup(T('actual\nratings',26,PURPLE).move_to(r.p(-.5,.86)),
                      Line(r.p(0,.86),r.p(.25,bell(.25)),color=PURPLE))
        x=r.p(.5,rise(.5))
        cross=VGroup(Line(x+[-.16,-.16,0],x+[.16,.16,0],color=RED,stroke_width=5),
                     Line(x+[-.16,.16,0],x+[.16,-.16,0],color=RED,stroke_width=5))
        self.play(c.animate.set_stroke(opacity=.45),Create(r.curve(c=PURPLE)),FadeIn(actual),Create(cross),run_time=.6)
        self.finish()


class S19Suspect(SpokenScene):
    def construct(self):
        g=ct_frame(); self.add(g)
        self.at('obvious candidate'); self.play(Transform(g[4],heading('Caress-tuned fibre: prime suspect',GREEN)),run_time=.4)
        self.at('not a proven cause'); self.play(FadeIn(chip('cause?',RED,30).move_to([4,1.55,0])),run_time=.4)
        self.finish()


class S20Limits(SpokenScene):
    def construct(self):
        a=person(GREEN).scale(2).move_to([-3.25,.1,0]); b=person(PURPLE).scale(2).move_to([3.25,.1,0])
        self.add(a,b,heading('Two separate groups'),
                 T('recorded',32,GREEN).move_to([-3.25,-2.5,0]),
                 T('rated',32,PURPLE).move_to([3.25,-2.5,0]))
        self.at('different people'); self.play(Transform(self.mobjects[2],heading('Different people')),run_time=.25)
        self.at('other signals combined')
        ps=[Plot(cx,cy=-.1,w=2.85,h=4.65,label=lab,color=col,ylabel='signal (model)')
            for cx,lab,col in [(-4.7,'A: levels off',GREY),(0,'B: keeps rising',GREY),(4.7,'A − B',PURPLE)]]
        def a_fn(x):
            t=(x+1)/3
            return .95*(1-np.exp(-4*t))/(1-np.exp(-4))
        def b_fn(x):
            return .95*(x+1)/3
        funcs=[a_fn,b_fn,lambda x:a_fn(x)-b_fn(x)]
        new=VGroup(heading('In principle: other signals can combine'),
                   note('model counterexample, not a measured mechanism'),
                   *[p.frame for p in ps],T('−',40).move_to([-2.35,2.65,0]),T('=',40).move_to([2.35,2.65,0]))
        self.remove(*list(self.mobjects)); self.add(new)
        self.play(*[Create(p.curve(f,c)) for p,f,c in zip(ps,funcs,[GREY,GREY,PURPLE])],run_time=.9)
        self.finish()


class S21Idea(SpokenScene):
    def construct(self):
        l,r,g=idea(); context=VGroup(*skin()[:2],brush()).scale(.38).move_to([3.25,-.4,0])
        self.add(l.frame,l.curve(),g[4],g[5],heading('The one idea'),context)
        self.at('recorded in human'); self.play(FadeIn(T('Human hairy skin',32).move_to([3.2,.65,0])),run_time=.4)
        self.at('fired most'); self.play(FadeOut(context),FadeIn(l.band),FadeIn(T('Tuned to\ncaress speeds',32,GREEN).move_to([3.2,-.7,0])),run_time=.5)
        self.finish()


class S22Idea2(SpokenScene):
    def construct(self):
        l,r,g=idea(); self.add(g)
        old=VGroup(g[-2],g[-1])
        self.at('Average pleasantness'); self.play(FadeOut(old),FadeIn(r.frame),Create(r.curve(c=PURPLE)),FadeIn(r.band),
                 Transform(g[0],heading('Average pleasantness ratings follow the same curve',PURPLE)),run_time=.7)
        self.at('prime candidate'); self.play(Transform(g[0],heading('CT input: prime candidate for pleasant touch',GREEN)),run_time=.4)
        self.finish()


class S23Take(SpokenScene):
    def construct(self):
        l,r,g=idea(1); self.add(g)
        g[0].become(heading('CT input: prime candidate for pleasant touch',GREEN))
        self.at('Only taking'); self.play(FadeIn(T('Only removal can show need',28,YELLOW).move_to([0,2.75,0])),run_time=.4)
        self.at('whether it is needed'); self.play(Transform(g[0],heading('→ Take the Input Away',YELLOW)),run_time=.3)
        self.finish()


class S24End(EndCard):
    LINE='The caress-tuned fibre is a prime suspect, not a proven cause.'
    def construct(self):
        self.add(T('The caress-tuned fibre is a prime suspect,',36).move_to([0,.6,0]),
                 T('not a proven cause.',36).move_to([0,-.15,0]),
                 T('→ Take the Input Away',30,YELLOW).move_to([0,-1.4,0]),
                 T('biochemistrypedia.com',26,TEAL).move_to([0,-2.4,0]))
        self.finish()
