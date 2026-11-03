"""Report It Twice — review fix round.
COLOR MAP: BLUE #58C4DD regular afferents; PURPLE #B58CD9 irregular afferents;
TEXT neutral head motion and central neurons; GREY axes, feedback and scope.
All curves are sampled equations. Gamma renewal intervals: k=1/CV²,
scale=CV²/100. Thresholds are the lesson's exact random-window count data.
Fourier replay / peak-locked spikes are computed teaching models, not recordings.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'


def label(s,x,y,c=TEXT,size=28):
    return T(s,size,c).move_to([x,y,0])

def title(s): return label(s,0,3.15,size=36)
def foot(s): return label(s,0,-3.28,GREY,26)
def badge(y=-2.65): return chip('Pause and predict',TEXT,28).move_to([0,y,0])

def head_icon(scale=1):
    face=Circle(radius=.62,color=TEXT,fill_opacity=.12,stroke_width=4)
    nose=Triangle(stroke_width=0,fill_color=TEXT,fill_opacity=1).scale(.17).move_to([0,.7,0])
    return VGroup(face,nose).scale(scale)

def turn_arrow(center,r=1):
    a=Arc(radius=r,start_angle=PI*.15,angle=PI*.7,color=TEXT,stroke_width=5)
    a.add_tip(tip_length=.2)
    return a.move_arc_center_to(center)

def trace(fn,y,color=TEXT,height=1,width=10.5):
    return VMobject(color=color,stroke_width=4).set_points_as_corners([
        [-width/2+width*t,y+height*fn(t),0] for t in np.linspace(0,1,601)])

def spike_train(x0,x1,y,positions,color,h=.75):
    return VGroup(Line([x0,y,0],[x1,y,0],color=GREY,stroke_width=2),
        VGroup(*[Line([x0+(x1-x0)*t,y,0],[x0+(x1-x0)*t,y+h,0],color=color,stroke_width=3)
                 for t in positions if 0<=t<=1]))

def gamma_spikes(cv,seed=4,n=24):
    rng=np.random.default_rng(seed)
    ts=np.cumsum(rng.gamma(1/cv**2,cv**2/100,n*3))
    return ts[ts<n/100]/(n/100)

def canal():
    # Three semicircular loops, a schematic organ, never a molecular structure.
    return VGroup(*[Ellipse(width=w,height=h,color=TEXT,stroke_width=6).rotate(a)
                   for w,h,a in [(2,2.6,0),(1,2.7,.8),(1,2.7,-.8)]],
                  Dot([0,-1.15,0],radius=.2,color=TEXT))

def organ_panel(x,is_canal=True):
    icon=canal() if is_canal else VGroup(
        Ellipse(width=2.6,height=1.5,color=TEXT,fill_opacity=.12,stroke_width=5),
        DoubleArrow(LEFT*1.6,RIGHT*1.6,color=TEXT).shift(UP*1.2))
    icon.scale(.85).move_to([x,.6,0])
    wires=VGroup()
    for dx,c,n in [(-1.1,BLUE,'regular'),(1.1,PURPLE,'irregular')]:
        wires.add(Line([x,-.45,0],[x+dx,-1.4,0],color=c,stroke_width=8),
                  Line([x+dx,-1.4,0],[x+dx,-2.05,0],color=c,stroke_width=8),
                  label(n,x+dx,-2.45,c,26))
    return VGroup(icon,label('Canals' if is_canal else 'Otoliths',x,2.65,size=34),
        label('rotation' if is_canal else 'linear acceleration + tilt',x,2.17,GREY,26),wires)

def prediction_cards():
    g=VGroup(title('Which detects a small, slow turn first?'))
    for x,n,c,gain,cv in [(-3.15,'Regular',BLUE,'0.5','0.05'),(3.15,'Irregular',PURPLE,'1.5','0.5')]:
        b=RoundedRectangle(width=5.6,height=3.7,corner_radius=.2,color=c,fill_opacity=.08).move_to([x,.45,0])
        g.add(VGroup(b,label(n,x,1.8,c,34),label('gain  '+gain,x,.8,c,32),label('CV  '+cv,x,-.1,c,32)))
    g.add(label('×3 gain     ·     ×10 CV',3.15,-.95,PURPLE,26),
          label('Both near 100 spikes/s at rest',0,-1.85,GREY,28),badge(-2.5),foot('Made-up model fibres'))
    return g

def threshold_cards(short=False):
    g=VGroup()
    for x,n,c,v,division in [(-3.15,'Regular',BLUE,7.1 if short else 1.3,'0.65 / 0.5'),
                            (3.15,'Irregular',PURPLE,10.9 if short else 3.3,'5.0 / 1.5')]:
        box=RoundedRectangle(width=5.6,height=3.8,corner_radius=.2,color=c,fill_color=c,fill_opacity=.14).move_to([x,0,0])
        g.add(VGroup(box,label(n,x,1.25,c,34),label(f'{v:.1f}°/s',x,.25,c,54),
            label('1 s: '+('1.3°/s' if x<0 else '3.3°/s') if short else division+(' ≈ 1.3' if x<0 else ' ≈ 3.3'),x,-.9,GREY if short else c,30)))
    return g

_rng=np.random.default_rng(19)
_PHASES=_rng.uniform(0,2*np.pi,6)
def motion(t,variant=0):
    return sum(np.sin(2*np.pi*[1,3,7,13,23,37][k]*t+_PHASES[k]+variant*(k+1)*.6)/np.sqrt(k+1) for k in range(6))*.25

def event_times(variant=0):
    ts=np.linspace(.02,.98,1000)
    ys=np.array([motion(t,variant) for t in ts])
    # Prominent positive peaks select the strongest model events.
    return ts[1:-1][(ys[1:-1]>ys[:-2]) & (ys[1:-1]>ys[2:]) & (ys[1:-1]>.25)]

def replay_stack():
    return VGroup(*[trace(motion,y,TEXT,.65,10.8) for y in [2.1,1.15,.2,-.75,-1.7]])

def timing_question():
    return VGroup(title('Can spike timing tell motions apart?'),
        replay_stack().stretch(.85,1).shift(UP*.2),
        badge(-2.65),label('Five replays of the same head motion',0,-3.4,GREY,24))

def callout(level=0):
    g=VGroup(title('Two overlapping channels'),
        RoundedRectangle(width=12.3,height=5.25,corner_radius=.2,color=GREY).move_to([0,.05,0]))
    for y in [1.0,-.65]:
        g.add(Line([-5.9,y,0],[5.9,y,0],color=GREY,stroke_width=1))
    # Consistent two-column rows. Earlier rows persist in every following scene.
    g.add(label('CANALS · Regular',-3.6,1.85,BLUE,28),label('CANALS · Irregular',-3.6,.2,PURPLE,28),
          label('Tested central neurons',-3.6,-1.5,size=26))
    if level>=1:
        g.add(label('Steady rate follows turn speed',2.05,2.15,BLUE,27),
              trace(lambda t:.45*np.sin(2*PI*t),1.5,BLUE,.5,5.5).shift(RIGHT*2.1))
    if level>=2:
        g.add(label('Higher gain · response to change',2.05,.62,PURPLE,24),
              label('Precise spike timing',2.05,.05,PURPLE,24),
              spike_train(-.7,4.85,-.48,event_times(),PURPLE,.22))
    if level>=3:
        g.add(label('Self-made response largely canceled',2.05,-1.25,size=26),
              label('Needs matching neck feedback',2.05,-1.95,GREY,26))
    return g

def closing():
    return VGroup(title('Report It Twice'),label('Regular',-4.7,2.25,BLUE,28),
        spike_train(-5.7,5.7,1.2,gamma_spikes(.05),BLUE,.65),
        label('Irregular',-4.6,.65,PURPLE,28),spike_train(-5.7,5.7,-.4,gamma_spikes(.5,seed=19),PURPLE,.65),
        label('Two overlapping channels report every head turn.',0,-1.25,size=30),
        label('Fast reports are thought to help hold the world still.',0,-1.95,size=28),
        label('Matching neck feedback: mainly the surprise passes on.',0,-2.6,size=26),
        foot('Tested neurons · may help spare intended turns · reflex role still open'))

class S00Title(TitleCard):
    LESSON='Balance: Two Codes for Every Head Movement'
    TITLE='Report It Twice'
    def construct(self):
        self.add(VGroup(T('BIOCHEMISTRYPEDIA',26,GREY),T(self.LESSON,28),
            T(self.TITLE,54,font=TITLE_FONT)).arrange(DOWN,buff=.5))
        self.finish()

class S01Q(SpokenScene):
    def construct(self):
        world=VGroup(*[Rectangle(width=1.5,height=h,color=GREY,fill_opacity=.12).move_to([x,-1.5+h/2,0])
                      for x,h in [(-4.9,3.3),(-3.1,2.4),(3.1,2.7),(4.9,3.5)]])
        torso=VGroup(Circle(radius=.45,color=TEXT).move_to([0,1.55,0]),
            Line([0,1.1,0],[0,-.75,0],color=TEXT,stroke_width=7),
            Line([0,.6,0],[-.8,-.15,0],color=TEXT,stroke_width=6),
            Line([0,.6,0],[.8,-.15,0],color=TEXT,stroke_width=6))
        def legs(sign):
            return VGroup(
                VMobject(color=TEXT,stroke_width=7).set_points_as_corners(
                    [[0,-.75,0],[sign*.6,-1.35,0],[sign*1.1,-2.25,0]]),
                VMobject(color=TEXT,stroke_width=7).set_points_as_corners(
                    [[0,-.75,0],[-sign*.65,-1.65,0],[-sign*.2,-2.0,0]]))
        leg=legs(1)
        self.add(world,torso,leg,label('Severe loss in both balance organs',0,3.15,size=32),
                 label('How does a healthy balance nerve prevent this?',0,-3.15,size=28))
        self.at('world bounce')
        for sign in [-1,1,-1,1,-1,1]:
            self.play(world.animate.shift(UP*(1.1*sign)),Transform(leg,legs(sign)),
                      torso.animate.shift(UP*(.12*sign)),run_time=.33)
        self.finish()

class S04Organs(SpokenScene):
    def construct(self):
        a,b=organ_panel(-3.15),organ_panel(3.15,False)
        self.add(a,b,foot('Every organ sends both kinds'))
        self.at('Each organ')
        self.play(Indicate(a[3],color=BLUE),Indicate(b[3],color=PURPLE),run_time=.7)
        self.finish()

class S05Canal(SpokenScene):
    def construct(self):
        g=organ_panel(0).scale(1.12).shift(DOWN*.15)
        self.add(g,title('Canal fibres · head rotation'))
        # Remove panel headings to make room for the large chapter-focus title.
        self.remove(g); g.remove(g[1],g[2]); self.add(g)
        self.at('head rotation')
        self.play(Rotate(g[0],PI/9),run_time=.6)
        self.finish()

class S06Rest(SpokenScene):
    def construct(self):
        self.add(title('Head still · both near 100 spikes/s'),
            label('Regular',-4.6,2.1,BLUE,32),label('Irregular',-4.5,-.25,PURPLE,32),
            spike_train(-5.7,5.7,.6,gamma_spikes(.05),BLUE,1.05),
            spike_train(-5.7,5.7,-1.8,gamma_spikes(.5),PURPLE,1.05),
            foot('Made-up gamma spike trains · 0.24 s shown'))
        self.at('ticks like a clock')
        self.play(Indicate(self.mobjects[3],color=BLUE),run_time=.6)
        self.finish()

class S08Slow(SpokenScene):
    def construct(self):
        sine=lambda t:np.sin(2*PI*t)
        axes=VGroup(Line([-5.4,1.25,0],[5.4,1.25,0],color=GREY),
            Line([-5.4,-1.45,0],[5.4,-1.45,0],color=GREY))
        v=trace(sine,1.25,TEXT,.7)
        r=trace(sine,-1.45,BLUE,.7)
        self.add(title('A slow head turn'),axes,v,
            label('Head velocity · degrees per second',0,2.45,size=28),
            label('Regular rate · spikes per second',0,-.05,BLUE,28),
            label('0',-5.85,1.25,GREY,26),label('100',-5.95,-1.45,GREY,26),
            foot('Sine teaching model · rate = 100 + 0.5 × velocity · time →'))
        self.at('regular')
        self.play(Create(r),run_time=.7)
        self.at('rate rises')
        ts=np.linspace(0,1,4001)
        # Four seconds of 100 + 10 sin(2πt) spikes/s; display every twentieth spike.
        cum=np.cumsum(4*(100+10*np.sin(2*PI*ts)))/4000
        events=np.interp(np.arange(10,cum[-1],20),cum,ts)
        ticks=VGroup(*[Line([-5.25+10.5*t,-1.45+.7*sine(t),0],
                           [-5.25+10.5*t,-1.1+.7*sine(t),0],color=BLUE) for t in events])
        self.play(Create(ticks),run_time=.7)
        self.finish()

class S09Fast(SpokenScene):
    def construct(self):
        pulse=lambda t:np.exp(-((t-.5)/.045)**2)
        reg=trace(pulse,-.25,BLUE,.55)
        irr=trace(pulse,-1.85,PURPLE,1.05)
        self.add(title('A sudden change'),trace(pulse,1.45,TEXT,.65),
            label('Head velocity',-3.7,2.45,size=28),
            label('Regular · lower gain',-3.5,.45,BLUE,28),reg,
            label('event',1.05,1.85,GREY,26),
            Line([0,1.0,0],[0,1.45,0],color=GREY),
            foot('Teaching model · sharp velocity pulse · time →'))
        t=np.linspace(0,1,2000); rate=3+100*np.exp(-((t-.5)/.045)**2)
        cum=np.cumsum(rate)/2000
        ev=np.interp(np.arange(.5,cum[-1],1),cum,t)
        self.at('irregular fiber')
        self.play(Create(irr),FadeIn(label('Irregular · higher gain',-3.5,-1.0,PURPLE,28)),
                  Create(spike_train(-5.25,5.25,-2.7,ev,PURPLE,.5)),run_time=.7)
        self.at('spikes lock')
        self.play(Indicate(irr,color=PURPLE,scale_factor=1.02),run_time=.5)
        self.finish()

class S11Paradox(SpokenScene):
    def construct(self):
        g=prediction_cards()
        g.remove(g[0],*g[3:])
        self.add(title('Lower gain, better detection?'),g,
            label('Small, slow turns',0,-2.1,size=32),foot('Gain alone does not set the detection threshold'))
        self.at('lower gain')
        self.play(Indicate(g[0],color=BLUE),run_time=.6)
        self.finish()

class S12Predict(SpokenScene):
    def construct(self):
        g=prediction_cards(); self.add(g)
        self.at('three times the gain')
        self.play(Indicate(g[3],color=PURPLE),run_time=.6)
        self.finish()

class S13Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(prediction_cards()); self.wait(5)

class S14Rule(SpokenScene):
    def construct(self):
        self.add(title('A rate change must stand out'),
            label('threshold = rate noise / gain',0,1.85,size=42),
            label('One standard deviation shift · 1 s window',0,.9,GREY,28),
            label('Regular gain: 0.5',-3.15,-.05,BLUE,30),
            label('Irregular gain: 1.5',3.15,-.05,PURPLE,30),
            foot('Made-up gamma counting decoder · random window'))
        self.at('stands out')
        self.play(FadeIn(label('Rate noise',0,-.9,size=28)),run_time=.35)
        self.at('made up counting')
        self.play(FadeIn(label('0.65 spikes/s',-3.15,-1.9,BLUE,36)),
                  FadeIn(label('5.0 spikes/s',3.15,-1.9,PURPLE,36)),run_time=.6)
        self.finish()

class S15Answer(SpokenScene):
    def construct(self):
        g=threshold_cards()
        self.add(title('Threshold for a small turn · 1 s'),g,
            label('Lower threshold detects a smaller turn',0,-2.55,GREY,28),foot('Made-up gamma-process model · not measured thresholds'))
        self.at('fiber wins')
        self.play(g[0][0].animate.set_fill(BLUE,opacity=.3).set_stroke(BLUE,width=7),
                  FadeIn(label('Lower threshold',-3.15,-1.48,BLUE,26)),run_time=.5)
        self.finish()

class S16Window(SpokenScene):
    def construct(self):
        g=threshold_cards()
        bar=Rectangle(width=10,height=.4,color=TEXT,fill_opacity=.7).move_to([0,2.25,0])
        track=Rectangle(width=10,height=.4,color=GREY,stroke_width=2).move_to(bar)
        wlabel=label('1 s window',0,2.77,GREY,26)
        ratio=label('Regular advantage: about 2.6-fold',0,-2.5,BLUE,28)
        self.add(title('Less time to count spikes'),g,track,bar,wlabel,ratio,
                 foot('Made-up model · not measured thresholds'))
        self.at('tenth of a second')
        newbar=Rectangle(width=1,height=.4,color=TEXT,fill_opacity=.7).move_to([-4.5,2.25,0])
        self.play(Transform(bar,newbar),
                  Transform(wlabel,label('0.1 s window',0,2.77,GREY,26)),run_time=.6)
        self.at('both thresholds rise')
        new=threshold_cards(True)
        self.play(FadeOut(g),FadeIn(new),
                  Transform(ratio,label('Regular advantage: about 1.5-fold',0,-2.5,BLUE,28)),run_time=.5)
        self.at('lead shrinks')
        self.play(Indicate(ratio,color=BLUE,scale_factor=1.03),run_time=.5)
        self.finish()

class S17Repeat(SpokenScene):
    def construct(self):
        stack=replay_stack()
        self.add(title('Same jittery head motion, replayed'),stack,
            foot('Computed motion · five schematic replays'))
        self.at('Replay the same')
        self.play(LaggedStart(*[Indicate(x,color=TEXT,scale_factor=1.01) for x in stack],lag_ratio=.15),run_time=1.4)
        self.finish()

class S18Predict(SpokenScene):
    def construct(self):
        g=timing_question(); self.add(g)
        self.at('could their timing')
        self.play(Indicate(g[0],color=PURPLE),run_time=.6)
        self.finish()

class S19Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(timing_question()); self.wait(5)

class S20Reveal(SpokenScene):
    def construct(self):
        self.add(title('Different motion, different timing'),
            label('A',-6,1.85,size=42),label('B',-6,-.65,size=42),
            trace(motion,1.9,TEXT,.65),trace(lambda t:motion(t,1),-.6,TEXT,.65),
            foot('Lacquaniti et al., 2023 · computed illustration, not recordings'))
        def repeats(v,y):
            return VGroup(*[spike_train(-5.25,5.25,y-j*.28,event_times(v),PURPLE,.22) for j in range(3)])
        self.at('precisely timed spikes')
        self.play(Create(repeats(0,1.0)),run_time=.6)
        self.at('different motions apart')
        self.play(Create(repeats(1,-1.5)),run_time=.6)
        self.at('Irregular at rest')
        self.play(FadeIn(label('Irregular at rest, precise when it matters',0,-2.65,PURPLE,28)),run_time=.5)
        self.finish()

class S22Fade(SpokenScene):
    def construct(self):
        self.add(title('A long turn at constant speed'),
            label('Head velocity',-3.9,2.55,size=28),label('Regular',0,.65,BLUE,28),
            label('Irregular',0,-1.15,PURPLE,28),
            foot('Teaching model · exponential canal adaptation · time →'))
        for y,c in [(1.45,TEXT),(-.15,BLUE),(-2,PURPLE)]:
            self.add(Line([-5.25,y,0],[5.25,y,0],color=GREY,stroke_width=1))
        self.add(label('rest',5.85,-.15,BLUE,26),label('rest',5.85,-2,PURPLE,26))
        self.at('long turn')
        self.play(Create(trace(lambda t:.65 if t>=.08 else 0,1.45,TEXT)),run_time=.8)
        self.at('signal fades')
        self.play(Create(trace(lambda t:0 if t<.08 else .95*np.exp(-(t-.08)/.22),-.15,BLUE)),
                  Create(trace(lambda t:0 if t<.08 else 1.25*np.exp(-(t-.08)/.075),-2,PURPLE)),run_time=1.6)
        self.finish()

class S24Idea(SpokenScene):
    def construct(self):
        self.add(callout())
        h=head_icon(.43).move_to([5.65,3.1,0]); self.add(h)
        self.at('head motion')
        self.play(Rotate(h,-PI/6),run_time=.4)
        self.at('two overlapping channels')
        self.play(Indicate(self.mobjects[0][4],color=BLUE),
                  Indicate(self.mobjects[0][5],color=PURPLE),run_time=.6)
        self.at('whoever caused it')
        self.play(FadeIn(foot('The peripheral nerve reports motion, whoever caused it')),run_time=.4)
        self.finish()

class S25Regular(SpokenScene):
    def construct(self):
        self.add(callout())
        self.at('regular fibers')
        full=callout(1)
        self.play(FadeIn(VGroup(*full[7:])),run_time=.7)
        self.finish()

class S26Irregular(SpokenScene):
    def construct(self):
        self.add(callout(1))
        self.at('Irregular fibers')
        full=callout(2)
        self.at('higher gain')
        self.play(FadeIn(full[9]),run_time=.4)
        self.at('more response')
        self.play(Indicate(full[9],color=PURPLE,scale_factor=1.02),run_time=.4)
        self.at('well timed spikes')
        self.play(FadeIn(full[10]),Create(full[11]),run_time=.5)
        self.play(FadeIn(label('Otoliths: same contrast for acceleration and tilt',0,-2.85,GREY,26)),
                  FadeIn(foot('Regularity is a continuum')),run_time=.5)
        self.finish()

class S27Central(SpokenScene):
    def construct(self):
        summary=callout(2); self.add(summary)
        self.at('head posture neurons')
        summary3=callout(3)
        self.play(FadeIn(VGroup(*summary3[12:])),run_time=.4)
        self.at('your own turn')
        # Zoom from the completed summary into the central comparison.
        self.play(FadeOut(summary),FadeOut(VGroup(*summary3[12:])),run_time=.25)
        self.add(title('Tested head-posture neurons'),
            head_icon(1.25).move_to([-4.55,1.4,0]),turn_arrow([-4.55,1.4,0],1.05),
            chip('Vestibular-only neuron',TEXT,28).move_to([1.5,2.2,0]),
            Line([-.75,1.55,0],[3.8,1.55,0],color=GREY),
            Line([1.5,1.9,0],[1.5,1.55,0],color=GREY),
            Line([-.75,1.55,0],[-.75,1.1,0],color=GREY),
            Line([3.8,1.55,0],[3.8,1.1,0],color=GREY),
            label('Needs matching neck feedback',1.5,.85,GREY,26),
            label('Same turn size',-4.4,-.1,GREY,26),
            label('Passive',-.75,.2,size=28),label('Self-made',3.8,.2,size=28),
            label('40 spikes/s',-.75,-.4,size=28),
            Rectangle(width=1.5,height=1.8,color=GREY,fill_opacity=.5).move_to([-.75,-1.65,0]),
            foot('Made-up response modulation · same 20°/s turn'))
        self.at('largely canceled')
        self.play(GrowFromEdge(Rectangle(width=1.5,height=.18,color=GREY,fill_opacity=.5).move_to([3.8,-2.46,0]),DOWN),
                  FadeIn(label('4 spikes/s',3.8,-1.85,size=28)),run_time=.5)
        self.at('neck feedback matches')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.25)
        self.play(FadeIn(callout(3)),FadeIn(foot('Needs matching neck feedback · tested neurons')),run_time=.5)
        self.finish()

class S29Takeaway(SpokenScene):
    def construct(self):
        g=closing(); self.add(g)
        self.at('are thought to help')
        self.play(Indicate(g[6],color=TEXT,scale_factor=1.02),run_time=.6)
        self.at('Muting matched')
        self.play(Indicate(g[7],color=TEXT,scale_factor=1.02),run_time=.6)
        self.at('may help')
        self.play(Indicate(g[8],color=GREY,scale_factor=1.02),run_time=.6)
        self.finish()

class S23End(EndCard):
    LINE='Two overlapping channels report every head turn.'
    def construct(self):
        self.add(closing())
        self.finish()
