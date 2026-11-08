"""A Fibre That Fires at Rest — reviewed animation.
COLOR MAP: BLUE = cool/TRPM8; ORANGE = warm; GOLD = bath temperature;
GREY = anatomy/context; RED = loss; GREEN = report. Temperature band:
deep blue / light blue / orange / red. All ticks and curves are computed
from the inherited illustrative rate model, not experimental recordings.
"""
import numpy as np
from bp_style import *

ORANGE = '#F29E4C'
WARM, COOL, STIM = ORANGE, BLUE, GOLD
T_RAMP0, T_RAMP1, T_END = 4., 6.5, 10.
def rate_warm(t):
    return .3 + 5.7 * min(1., max(0., (t-4)/2.5))
def rate_cool(t):
    return 3.5 - 2.8 * min(1., max(0., (t-4)/2.5))
def rate_cooling(t):
    return 7.-rate_cool(t)
def rest(t): return 3.5
def warm_rest(t): return .3
def spike_times(rate):
    # Regular integrated-rate raster: sparse low-rate ticks remain visible.
    ts=np.arange(0,10,.002)
    integral=np.cumsum([rate(t) for t in ts])*.002
    targets=np.arange(.1, integral[-1], 1.)
    return ts[np.searchsorted(integral,targets)]
def X(t): return -5.7+1.14*t
def label(s,y=3.05,color=TEXT,size=32): return T(s,size,color).move_to([0,y,0])
def note(): return label('constructed schematic',-3.25,GREY,26)
def raster(rate=rest,y=.1,color=COOL,h=2.,x0=-5.7,x1=5.7):
    xx=lambda t:x0+(x1-x0)*t/10
    axis=Line([x0,y-h/2,0],[x1,y-h/2,0],color=GREY,stroke_width=2)
    ticks=VGroup(*[Line([xx(t),y-h/2+.08,0],[xx(t),y+h/2,0],color=color,stroke_width=4) for t in spike_times(rate)])
    return VGroup(axis,ticks)
def stimulus(word='warming',y=-1.3):
    col=COOL if word=='cooling' else WARM if word=='warming' else GREY
    bar=Rectangle(width=X(10)-X(4),height=.14,stroke_width=0,fill_color=col,fill_opacity=1).move_to([(X(4)+X(10))/2,y,0])
    return VGroup(bar,T(word,26,col).next_to(bar,DOWN,buff=.13))
def replace_ticks(scene,r,new,seconds=.4):
    # Separate fades avoid intermediate morphs that invent ghost spikes.
    scene.play(FadeOut(r[1]),run_time=seconds/2)
    r.remove(r[1]); r.add(new[1])
    scene.play(FadeIn(r[1]),run_time=seconds/2)
def rateplot(rate):
    y0=-3.3
    axes=VGroup(Line([-5.7,y0,0],[5.7,y0,0],color=GREY),Line([-5.7,y0,0],[-5.7,-1.6,0],color=GREY))
    curve=VMobject(color=COOL,stroke_width=5).set_points_as_corners([[X(t),y0+rate(t)*.18,0] for t in np.linspace(0,10,251)])
    return VGroup(axes,curve,T('0',26,GREY).move_to([-6,-3.3,0]),T('rate (spikes per second)',26,GREY).move_to([-3.6,-1.95,0]),T('time →',26,GREY).move_to([5,-3.65,0]))
def question():
    return VGroup(label('What can this fibre report',2.9,size=34),label('that a silent one cannot?',2.2,size=34),raster(y=-.2,h=3.6),label('firing at rest',-2.7,COOL,30))
def paw(x=0,y=0,thermal=False):
    # Long wrist, narrow palm and four separated slender digits: forepaw silhouette.
    shapes=VGroup(RoundedRectangle(width=1.25,height=2.2,corner_radius=.3).move_to([0,-.35,0]))
    for i,(height,offset) in enumerate([(1.2,-.1),(1.65,.12),(1.5,.04),(1.,-.18)]):
        shapes.add(RoundedRectangle(width=.32,height=height,corner_radius=.15).move_to([-.6+i*.4,.9+offset,0]))
    shapes.add(Ellipse(width=.4,height=.95).rotate(-.55).move_to([-.85,.1,0]))
    shapes.set_stroke(GREY,2).set_fill(GREY,.35)
    if thermal:
        shapes.set_fill(color=[COOL,GOLD,WARM],opacity=.85)
    return shapes.move_to([x,y,0])
def plate_paw():
    p=paw(0,.2).scale(1.1)
    plate=Rectangle(width=3.8,height=.35,stroke_color=WARM,fill_color=WARM,fill_opacity=.3).move_to([0,-1.55,0])
    return VGroup(p,plate,T('mouse forepaw',26,GREY).move_to([3,.3,0]))
def puzzle():
    return VGroup(label('Why would a cold channel',2.6,size=36),label('matter for warmth?',1.95,WARM,36))
def thermal_band():
    return VGroup(*[VGroup(Rectangle(width=2.8,height=.2,stroke_width=0,fill_color=c,fill_opacity=1).move_to([-4.2+i*2.8,2.65,0]),T(w,26,c).move_to([-4.2+i*2.8,3.12,0])) for i,(w,c) in enumerate(zip(['cold','cool','warm','noxious heat'],['#5879ED',COOL,WARM,RED]))])
def bath():
    tub=RoundedRectangle(width=7.8,height=3.8,corner_radius=.2,stroke_color=GREY,fill_color=COOL,fill_opacity=.08).move_to([-1.5,-.3,0])
    skin=RoundedRectangle(width=2.8,height=1.2,corner_radius=.2,stroke_color=GREY,fill_color=GREY,fill_opacity=.3).move_to([-3,-.5,0])
    nerve=Line([-1.6,-.5,0],[4,-.5,0],color=COOL,stroke_width=7)
    electrode=VGroup(Line([3.6,-.5,0],[3.6,1.4,0],color=TEXT,stroke_width=4),Line([3.6,1.4,0],[5.6,1.4,0],color=TEXT,stroke_width=4))
    labs=VGroup(T('bath',28,GREY).move_to([-4.5,1.1,0]),T('skin patch',28,GREY).move_to([-3,-1.55,0]),T('nerve',28,COOL).move_to([.2,-1.1,0]),T('recording electrode',28).move_to([3.9,2.05,0]))
    return VGroup(tub,skin,nerve,electrode,labs)
def pair_labels(a='cool line',b='warm line',col=WARM):
    return VGroup(T(a,28,COOL).move_to([-3.8,2.45,0]),T(b,28,col).move_to([-3.8,-.05,0]))
def pair(a=rest,b=rest,second=WARM):
    return VGroup(raster(a,y=1.25,h=1.65),raster(b,y=-1.25,h=1.65,color=second))

class S00Title(TitleCard):
    LESSON='Hot, Warm, Cool and Cold'
    TITLE='A Fibre That Fires at Rest'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28,GREY),T(self.TITLE,46,font=TITLE_FONT),Line(LEFT*1.3,RIGHT*1.3,color=GOLD)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.5); self.finish()
class S01Q(SpokenScene):
    def construct(self):
        g=plate_paw(); self.add(g,label('A Fibre That Fires at Rest',3,size=36))
        self.at('lack a',lead=0)
        self.play(FadeIn(chip('cold-and-menthol channel absent',COOL,26).move_to([0,-2.7,0])),run_time=.35)
        self.at('gentle warming',lead=0)
        self.play(g[1].animate.set_fill(WARM,.8),g[0].animate.set_fill(WARM,.35),run_time=.6)
        self.finish()
class S02Fail(SpokenScene):
    def construct(self):
        g=plate_paw().scale(.8).move_to([0,-.35,0]); g[1].set_fill(WARM,.6)
        self.add(g,chip('mice lacking TRPM8',COOL,26).move_to([0,-2.8,0]))
        self.at('They failed',lead=0)
        title=label('No warmth report',2.8,RED,36); self.play(FadeIn(title),run_time=.3)
        self.at('Why would',lead=0)
        self.play(FadeOut(title),FadeIn(puzzle()),run_time=.4); self.finish()
class S03Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(plate_paw().scale(.8).move_to([0,-.35,0]),puzzle(),chip('mice lacking TRPM8',COOL,26).move_to([0,-2.8,0])); self.wait(3)
class S04Transducer(SpokenScene):
    def construct(self):
        skin=RoundedRectangle(width=11.8,height=5.3,corner_radius=.2,stroke_color=GREY,fill_color=GREY,fill_opacity=.08).move_to([0,-.3,0])
        ending=RoundedRectangle(width=7.2,height=3.2,corner_radius=1.,stroke_color=COOL,stroke_width=6).move_to([.6,-.4,0])
        gate=VGroup(*[Rectangle(width=.32,height=1.3,color=COOL,fill_opacity=1).move_to([x,1.2,0]) for x in [-.3,.5]])
        title=label('transducer',3.1,COOL,34)
        self.add(skin,ending,gate,T('skin',28,GREY).move_to([-4.8,-2.3,0]),T('nerve ending',28,COOL).move_to([.6,-1.35,0]),title)
        self.at('a stimulus',lead=0)
        self.play(GrowArrow(Arrow([-4,2.1,0],[-.4,1.45,0],color=GOLD)),FadeIn(T('stimulus in',28,GOLD).move_to([-4,1.55,0])),run_time=.4)
        self.at('electrical signal',lead=0)
        self.play(GrowArrow(Arrow([.4,.2,0],[3.2,.2,0],color=COOL)),FadeIn(label('electrical signal out',-3.5,COOL,28)),run_time=.4)
        self.at('the candidates',lead=0)
        self.play(Transform(title,label('candidate transducers: ion channels',3.1,COOL,32)),Indicate(gate),FadeIn(T('ion channel',26,COOL).move_to([2.7,1.9,0])),Create(Line([1.5,1.7,0],[.7,1.4,0],color=COOL)),run_time=.5); self.finish()
class S05Line(SpokenScene):
    def construct(self):
        skin=Rectangle(width=.55,height=3.9,color=GREY,fill_opacity=.25).move_to([-5.4,-.45,0])
        cord=RoundedRectangle(width=.9,height=3.9,corner_radius=.25,color=GREY).move_to([5.3,-.45,0])
        fibres=VGroup(*[Line([-5.1,y,0],[4.85,y,0],color=COOL if i==1 else GREY,stroke_width=7 if i==1 else 4) for i,y in enumerate([.9,-.45,-1.8])])
        self.add(thermal_band(),skin,cord,fibres,T('skin',28,GREY).move_to([-5.4,-2.8,0]),T('spinal cord',28,GREY).move_to([5.2,-2.8,0]),Arrow([-1,2.2,0],[1,2.2,0],color=GREY),T('temperature',26,GREY).move_to([0,1.85,0]))
        self.at('A line',lead=0); self.play(FadeIn(T('line: sensory fibre + what it reports',28,COOL).move_to([.3,-.02,0])),run_time=.35)
        self.at('A channel',lead=0)
        gate=VGroup(*[Line([x,-.8,0],[x,-.1,0],color=COOL,stroke_width=7) for x in [-4.95,-4.55]])
        self.play(Create(gate),FadeIn(chip('channel',COOL,26).move_to([-3.5,-1.1,0])),Create(Line([-4.7,-.8,0],[-4.3,-1.1,0],color=COOL)),run_time=.4); self.finish()
class S06Fibres(SpokenScene):
    def construct(self):
        bare=Circle(.6,color=COOL,fill_opacity=.3).move_to([-3.3,.7,0])
        sheath=VGroup(Circle(1.15,color=GREY,fill_opacity=.12),Circle(.77,color=GREY,fill_opacity=.2)).move_to([3.3,.7,0])
        self.add(bare,T('C fibre',36,COOL).move_to([-3.3,2.8,0]),Line([-5.4,-1.5,0],[-1.2,-1.5,0],color=COOL,stroke_width=7))
        self.at('They are thin',lead=0)
        self.play(FadeIn(sheath),FadeIn(T('Aδ fibre',34,GREY).move_to([3.3,2.8,0])),FadeIn(T('thin • unmyelinated',28,COOL).move_to([-3.3,-.5,0])),FadeIn(T('thinly myelinated',28,GREY).move_to([3.3,-.8,0])),Create(Line([1.2,-1.5,0],[5.4,-1.5,0],color=GREY,stroke_width=14)),run_time=.4)
        self.at('and slow',lead=0)
        slow=Dot([-5.2,-1.5,0],color=COOL); fast=Dot([1.4,-1.5,0],color=TEXT)
        self.add(slow,fast,T('slow',28,COOL).move_to([-3.3,-2.4,0]),T('faster',28,GREY).move_to([3.3,-2.4,0]))
        self.play(slow.animate.shift(RIGHT*1.2),fast.animate.shift(RIGHT*3.8),run_time=.75); self.finish()
class S07Trpm8(SpokenScene):
    def construct(self):
        b=thermal_band(); membrane=Line([-3.1,-.3,0],[.3,-.3,0],color=GREY,stroke_width=6)
        gate=VGroup(*[Rectangle(width=.5,height=2.5,color=COOL,fill_opacity=.8).move_to([x,-.3,0]) for x in [-1.9,-.9]])
        self.add(b,membrane,gate)
        self.at('gentle cooling',lead=0)
        self.play(*[b[i].animate.set_opacity(.22) for i in [0,2,3]],Indicate(b[1]),Create(Line([-1.4,2.4,0],[-1.4,1.05,0],color=COOL)),run_time=.4)
        self.at('established transducer',lead=0); self.play(FadeIn(chip('TRPM8',COOL,38).move_to([-1.4,-2.4,0])),run_time=.4); self.finish()
class S08Silent(SpokenScene):
    def construct(self):
        r=raster(lambda t:0,y=.3,h=4.); self.add(label('Silent at rest',3,COOL,36),r,note())
        self.at('a change',lead=0); self.play(FadeIn(stimulus('stimulus',-2.05)),run_time=.3)
        self.at('starting to fire',lead=0); replace_ticks(self,r,raster(lambda t:0 if t<4 else 1.3,y=.3,h=4.)); self.finish()
class S09Study(SpokenScene):
    def construct(self):
        prep=bath(); self.add(prep,label('Mouse forepaw • skin–nerve preparation',-3.05,GREY,30))
        self.at('one study',lead=0); self.play(FadeIn(label('2020',3.1,size=36)),run_time=.25)
        self.at('recorded single',lead=0); self.play(Indicate(prep[3]),run_time=.5); self.finish()
class S10Bath(SpokenScene):
    def construct(self):
        p=paw(-3.4,0,True).scale(1.5)
        b=VGroup(RoundedRectangle(width=4.7,height=3.8,corner_radius=.2,stroke_color=GREY,fill_color=COOL,fill_opacity=.08).move_to([3.1,0,0]),RoundedRectangle(width=1.7,height=.9,corner_radius=.15,stroke_color=GREY,fill_color=GREY,fill_opacity=.3).move_to([2.4,-.4,0]),Line([3.25,-.4,0],[5.3,-.4,0],color=COOL,stroke_width=6))
        self.add(p,b,label('Awake mouse forepaw',3.15,size=32))
        self.at('Skin measured',lead=0)
        scale=VGroup(*[Rectangle(width=.3,height=.26,stroke_width=0,fill_color=interpolate_color(ManimColor(COOL),ManimColor(WARM),i/19),fill_opacity=1).move_to([-5.8,-2.1+i*.2,0]) for i in range(20)])
        self.play(FadeIn(scale),FadeIn(T('26',26,GOLD).move_to([-5.8,-2.6,0])),FadeIn(T('28 °C',26,GOLD).move_to([-5.8,2.2,0])),FadeIn(T('26 to 28 °C',30,GOLD).move_to([-3.2,-3,0])),run_time=.4)
        self.at('used a bath',lead=0); self.play(FadeIn(T('27 °C bath',30,GOLD).move_to([3.1,-3,0])),run_time=.4); self.finish()
class S11Predict(SpokenScene):
    def construct(self):
        q=question(); self.add(q[2],q[3])
        self.at('What can it report',lead=0); self.play(FadeIn(q[0]),FadeIn(q[1]),run_time=.4); self.finish()
class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question()); self.wait(5)
class S13Reveal(SpokenScene):
    def construct(self):
        p=pair(second=COOL); self.add(p[0],T('the same fibre',28,COOL).move_to([-3.8,2.5,0]))
        self.at('both directions',lead=0); self.play(FadeIn(p[1]),FadeIn(T('the same fibre',28,COOL).move_to([-3.8,0,0])),run_time=.3)
        self.at('Faster for one',lead=0); self.play(FadeIn(stimulus('cooling',.25)),run_time=.15); replace_ticks(self,p[0],raster(rate_cooling,y=1.25,h=1.65),.25)
        self.at('slower for',lead=0); self.play(FadeIn(stimulus('warming',-2.25)),run_time=.15); replace_ticks(self,p[1],raster(rate_cool,y=-1.25,h=1.65),.25)
        self.wait(1); self.finish()
class S14Cool(SpokenScene):
    def construct(self):
        self.add(raster(y=-.1,h=4.,x0=-5.7,x1=1.2),T('ongoing activity',28,COOL).move_to([-2.3,2.35,0]),T('raster: constructed schematic',26,GREY).move_to([-2.3,-2.6,0]))
        self.at('degree bath',lead=0); self.play(FadeIn(T('27 °C bath',32,GOLD).move_to([3.9,1.65,0])),run_time=.3)
        self.add(VGroup(T('about 19%',32),T('of temperature-',26,GREY),T('sensitive fibres',26,GREY),T('0.2 to 6 Hz',32,COOL),T('at rest',26,COOL)).arrange(DOWN,buff=.2).move_to([3.9,-.55,0]))
        self.at('These were',lead=0); self.play(FadeIn(label('cool-sensitive C fibres',3.1,COOL,36)),run_time=.4); self.finish()
class S15Rate(SpokenScene):
    def construct(self):
        r=raster(y=.65,h=3.6); plot=rateplot(rest); self.add(label('cool-sensitive C fibre',3.15,COOL,34),r,plot)
        self.at('Cooling makes',lead=0)
        self.play(FadeIn(stimulus('cooling',-1.38)),run_time=.2); replace_ticks(self,r,raster(rate_cooling,y=.65,h=3.6),.4)
        self.play(Transform(plot,rateplot(rate_cooling)),run_time=.4); self.finish()
class S16Warm(SpokenScene):
    def construct(self):
        r=raster(y=.65,h=3.6); plot=rateplot(rest); self.add(label('cool-sensitive C fibre',3.15,COOL,34),r,plot)
        self.at('Warming made',lead=0); self.play(FadeIn(stimulus('warming',-1.38)),run_time=.2); replace_ticks(self,r,raster(rate_cool,y=.65,h=3.6),.4)
        self.play(Transform(plot,rateplot(rate_cool)),run_time=.4); self.finish()
class S17Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(label('cool-sensitive C fibre',3.15,COOL,34),raster(rate_cool,y=.65,h=3.6),rateplot(rate_cool),stimulus('warming',-1.38)); self.wait(3)
class S18Warmfibre(SpokenScene):
    def construct(self):
        p=pair(rate_cool,warm_rest); self.add(p[0],pair_labels('cool-sensitive C fibre','warm-excited C fibre'),stimulus('warming',-2.35))
        self.at('A second',lead=0); self.play(FadeIn(p[1]),run_time=.35)
        self.at('Warming made',lead=0); replace_ticks(self,p[1],raster(rate_warm,y=-1.25,h=1.65,color=WARM),.4); self.wait(2.); self.finish()
class S19Hidden(SpokenScene):
    def construct(self):
        thumb=raster(y=.1,h=1.7,x0=-5.7,x1=-.9)
        panel=VGroup(RoundedRectangle(width=5.5,height=2.4,corner_radius=.2,color=GREY,fill_color=GREY,fill_opacity=.1).move_to([3,.1,0]),T('not seen',36,GREY).move_to([3,.3,0]),T('32 °C bath',28,GOLD).move_to([3,-.5,0]))
        self.add(thumb,T('27 °C bath',30,GOLD).move_to([-3.3,1.65,0]),T('ongoing activity',28,COOL).move_to([-3.3,-1.3,0]),panel,label('Cool-sensitive C fibres',3.1,COOL,36),label('observation, not a zero-firing trace',-2.8,GREY,28))
        self.finish()
class S20Vestib(SpokenScene):
    def construct(self):
        loop=Circle(1.05,color=GREY,stroke_width=7).move_to([-3.8,1.2,0])
        marker=Dot([-3.8,2.25,0],color=TEXT,radius=.15)
        fibre=Line([-2.75,1.2,0],[4.7,1.2,0],color=GREY,stroke_width=6)
        r=raster(y=-1.35,h=1.8,color=GREY)
        state=T('firing at rest',28,GREY).move_to([1.2,1.8,0])
        head=VMobject(color=GREY,stroke_width=3).set_points_as_corners([[x,y,0] for x,y in [(-5.3,-.15),(-5.5,1.5),(-5.1,2.5),(-4.4,2.8),(-3.4,2.7),(-2.8,2.2),(-2.6,1.65),(-2.2,1.3),(-2.65,1.1),(-2.5,.75),(-2.8,.55),(-2.8,.05),(-3.3,-.2),(-3.35,-.45)]])
        self.add(head,loop,marker,fibre,r,label('semicircular-canal afferent',3.4,GREY,32),T('canal loop',26,GREY).move_to([-1,2.7,0]),Line([-2,2.5,0],[-3.15,2.05,0],color=GREY),state)
        self.at('rotation can speed',lead=0)
        fast_state=T('faster',28,GREY).move_to([1.2,2.25,0])
        turn=T('turn one way →',28,GREY).move_to([1.5,.5,0]); self.play(FadeOut(state),FadeIn(fast_state),FadeIn(turn),Rotate(marker,.65,about_point=loop.get_center()),run_time=.35); replace_ticks(self,r,raster(rate_cooling,y=-1.35,h=1.8,color=GREY),.35)
        self.at('or slow',lead=0); self.play(FadeOut(fast_state),FadeIn(T('slower',28,GREY).move_to([1.2,1.8,0])),FadeOut(turn),FadeIn(T('← turn the other way',28,GREY).move_to([1.5,.05,0])),Rotate(marker,-1.3,about_point=loop.get_center()),run_time=.35); replace_ticks(self,r,raster(rate_cool,y=-1.35,h=1.8,color=GREY),.35); self.finish()
class S21Idea1(SpokenScene):
    def construct(self):
        p=pair(rest,warm_rest); heading=label('The one idea',3.25,size=36)
        self.add(p,pair_labels(),heading)
        self.at('Skin temperature',lead=0)
        self.play(FadeIn(stimulus('warming',-2.25)),run_time=.15)
        replace_ticks(self,p[0],raster(rate_cool,y=1.25,h=1.65),.3); replace_ticks(self,p[1],raster(rate_warm,y=-1.25,h=1.65,color=WARM),.3)
        self.at('a few lines',lead=0)
        message=label('Skin temperature is read from a few lines at once',-3.45,size=29)
        self.play(FadeIn(message),run_time=.3)
        self.at('not one channel',lead=0); self.play(FadeIn(label('not one channel per feeling',3.25,GREY,30)),FadeOut(heading),run_time=.3); self.finish()
class S22Idea2(SpokenScene):
    def construct(self):
        p=pair(second=COOL)
        self.add(p,pair_labels('cool line, cooling','cool line, warming',COOL),chip('TRPM8',COOL,26).move_to([4.7,2.65,0]),Line([4.7,2.25,0],[4.7,2.05,0],color=COOL),T('One cool line can signal both ways',30).move_to([-1.6,3.25,0]))
        self.at('speeds up',lead=0); self.play(FadeIn(stimulus('cooling',.25)),run_time=.15); replace_ticks(self,p[0],raster(rate_cooling,y=1.25,h=1.65),.25)
        self.at('and slows',lead=0); self.play(FadeIn(stimulus('warming',-2.25)),run_time=.15); replace_ticks(self,p[1],raster(rate_cool,y=-1.25,h=1.65),.25); self.finish()
class S23Idea3(SpokenScene):
    def construct(self):
        channel=chip('TRPM8',COOL,34).move_to([-3.7,0,0])
        line=VGroup(Line([-5.7,0,0],[-4.7,0,0],color=COOL,stroke_width=8),Line([-2.6,0,0],[1,0,0],color=COOL,stroke_width=8))
        tag=T('cool line',30,COOL).move_to([-.9,.7,0]); leader=Line([-.9,.45,0],[-.9,.08,0],color=COOL)
        outs=VGroup(chip('cool',COOL,36).move_to([4,1.8,0]),chip('warm',WARM,36).move_to([4,-1.8,0]))
        arrows=VGroup(Arrow([1,0,0],[2.9,1.8,0],color=COOL,buff=.1),Arrow([1,0,0],[2.9,-1.8,0],color=WARM,buff=.1))
        self.add(line,channel,tag,leader,label('A channel supplies activity to a line',3.1,size=32))
        self.at('matters for everything',lead=0); self.play(Create(arrows),FadeIn(outs),run_time=.5)
        self.at('losing a cool channel',lead=0); self.play(Create(Cross(channel,stroke_color=RED,stroke_width=6)),line.animate.set_opacity(.2),arrows.animate.set_opacity(.2),outs.animate.set_opacity(.35),run_time=.5)
        self.at('can cost warmth',lead=0); self.play(FadeIn(label('Losing a cool channel can cost warmth',-3.05,WARM,32)),run_time=.35); self.finish()
class S24Scope(SpokenScene):
    def construct(self):
        p=paw(-4,0).scale(1.5)
        box=DashedVMobject(RoundedRectangle(width=5,height=4,corner_radius=.2,color=GREY),num_dashes=40).move_to([3.4,0,0])
        self.add(p,label('Mouse forepaw result',3.1,size=36))
        self.at('The circuit',lead=0)
        lines=VGroup(*[Line([-2.6,y,0],[-.4,y,0],color=c,stroke_width=5) for y,c in [(.55,COOL),(-.55,WARM)]])
        lines.add(*[Line([-.4,y,0],[-.1,0,0],color=c,stroke_width=4) for y,c in [(.55,COOL),(-.55,WARM)]])
        gap=DashedLine([-.1,0,0],[.9,0,0],color=GREY)
        self.play(Create(lines),Create(gap),Create(box),FadeIn(T('?',32,GREY).move_to([.2,.55,0])),FadeIn(T('reads the lines',30,GREY).move_to([3.4,.7,0])),run_time=.5)
        self.at('has not been identified',lead=0); self.play(FadeIn(T('not identified',32,GREY).move_to([3.4,-.5,0])),run_time=.4); self.finish()
class S25Take(SpokenScene):
    def construct(self):
        r=raster(y=.3,h=4.); self.add(r,note().move_to([0,-3.55,0]),label('The picture to keep',3.15,size=38))
        self.at('can say warmer',lead=0); self.play(FadeIn(stimulus('warming',-2.05)),run_time=.15); replace_ticks(self,r,raster(rate_cool,y=.3,h=4.),.35)
        self.at('by going quiet',lead=0); self.play(FadeIn(label('warmer, said by going quiet',-3.0,WARM,38)),run_time=.3)
        self.wait(max(0,3-(self.elapsed()-(self.t_of('can say warmer')+.5)))); self.finish()
class S26End(EndCard):
    LINE='A fibre firing at rest can signal warmth by slowing.'
