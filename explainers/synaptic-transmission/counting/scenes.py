"""Counting with Zeros — revised, word-aligned animation.
COLOR MAP: BLUE release sites; YELLOW packets and m; GREEN direct response;
RED failures; TEAL calcium; GREY structure; TEXT explanatory labels.
All curves use Poisson/Gaussian equations. Trials use seeded Bernoulli draws.
"""
import math
import numpy as np
from bp_style import *

SECONDARY = '#CBD1DD'

def label(s, y=2.9, color=TEXT, size=32, x=0):
    return T(s, size, color).move_to([x,y,0])

def eq(s,y=0,size=36,color=TEXT,x=0):
    return M(s,size,color).move_to([x,y,0])

class Timed(SpokenScene):
    def at(self,phrase,lead=0,nth=0):
        super().at(phrase,lead=lead,nth=nth)


def methods(previews=True):
    g=VGroup()
    for x,name,color in [(-3.15,'Direct method',GREEN),(3.15,'Failure method',RED)]:
        box=RoundedRectangle(width=5.8,height=5.5,corner_radius=.2,color=color).move_to([x,-.05,0])
        group=VGroup(box,label(name,2.1,color,34,x))
        if previews:
            text='Average response\n÷ packet size' if x<0 else 'Fraction of zeros\nfailures / trials'
            group.add(label(text,-.2,TEXT,40,x))
        g.add(group)
    return g


def lamps(on=(), y=.15):
    on=set(on); g=VGroup()
    for i in range(100):
        x=-5.8+(i%10)*.56; yy=y+2.34-(i//10)*.52
        lit=i in on
        glow=Circle(radius=.225,stroke_width=0,fill_color=YELLOW,fill_opacity=.16 if lit else 0)
        bulb=Circle(radius=.15,color=YELLOW if lit else BLUE,stroke_width=1.6,
                    fill_color=YELLOW if lit else BLUE,fill_opacity=1 if lit else .16)
        g.add(VGroup(glow,bulb).move_to([x,yy,0]))
    return g


def stage(on=()):
    return VGroup(lamps(on),label('N = 100 release sites',3.2,BLUE,32,x=-3.25))


def impulse():
    return VGroup(Arrow([.3,2.0,0],[-.55,2.0,0],buff=0,color=BLUE),
                  label('Impulse',2.6,BLUE,30,x=1.7))


def side(lines,color=TEXT):
    return VGroup(*[label(t,y,color,size,x=3.1) for t,y,size in lines])


def prediction():
    return VGroup(stage(),side([('Average release',1.7,32),('m = 1',.75,48),
                               ('packet per impulse',-.15,30),('How often is',-1.45,32),('nothing released?',-2.2,32)],YELLOW))


def readings():
    cells=VGroup()
    for x,n in zip([-4.5,-1.5,1.5,4.5],[1,0,2,0]):
        box=RoundedRectangle(width=2.35,height=2.0,corner_radius=.15,color=RED if n==0 else GREEN).move_to([x,1,0])
        tokens=VGroup(*[Circle(radius=.24,color=YELLOW,fill_color=YELLOW,fill_opacity=.85).move_to([x, .65+j*.65,0]) for j in range(n)])
        cells.add(VGroup(box,tokens,eq(str(n),-.35,36,RED if n==0 else GREEN,x)))
    return cells


def jar(n=0):
    body=RoundedRectangle(width=4,height=3.8,corner_radius=.2,color=SECONDARY,fill_color=BLUE,fill_opacity=.08).move_to([-2.4,.6,0])
    lid=Rectangle(width=4.3,height=.25,color=BLUE,fill_opacity=1,fill_color=BLUE).move_to([-2.4,2.6,0])
    base=RoundedRectangle(width=5,height=1.1,corner_radius=.2,color=SECONDARY).move_to([-2.4,-2.05,0])
    coins=VGroup(*[Circle(radius=.4,color=YELLOW,fill_color=YELLOW,fill_opacity=.8).move_to([-2.4,-.8+j*.9,0]) for j in range(n)])
    return VGroup(body,lid,base,coins,eq(str(n),-2.05,44,GREEN,-2.4),label(f'{n} packets',.7,GREEN,44,x=3.4))


def hist(predicted=False):
    # Expected trials per 0.05 mV bin: integral is 200 trials.
    ax=Axes(x_range=[-.5,2.1,.4],y_range=[0,20,5],x_length=10.8,y_length=4.65,
            tips=False,axis_config={'color':SECONDARY,'include_ticks':False}).move_to([.2,.05,0])
    ax.y_axis.set_opacity(0)
    ax.add(Line(ax.c2p(-.5,0),ax.c2p(-.5,20),color=SECONDARY,stroke_width=2))
    sigma=.14 if predicted else .24
    def component(x,k):
        s=sigma+.012*k
        return 200*math.exp(-1)/math.factorial(k)*.05*np.exp(-.5*((x-.4*k)/s)**2)/(s*np.sqrt(2*np.pi))
    parts=VGroup()
    if predicted:
        for k in range(5):
            xs=np.linspace(-.5,2.1,200)
            pts=[ax.c2p(xs[0],0),*[ax.c2p(x,component(x,k)) for x in xs],ax.c2p(xs[-1],0)]
            curve=VMobject(color=RED if k==0 else BLUE,fill_color=RED if k==0 else BLUE,fill_opacity=.25,stroke_width=2)
            curve.set_points_as_corners(pts).close_path();parts.add(curve)
    trace=ax.plot(lambda x:sum(component(x,k) for k in range(9)),x_range=[-.5,2.1,.012],color=GREEN,use_smoothing=False)
    xt=VGroup(*[eq(f'{k*.4:.1f}',ax.c2p(0,0)[1]-.35,28,SECONDARY,ax.c2p(k*.4,0)[0]) for k in range(5)])
    yt=VGroup(*[eq(str(n),ax.c2p(0,n)[1],26,SECONDARY,ax.get_left()[0]-.4) for n in [0,5,10,15,20]])
    units=label('Trials / 0.05 mV bin',2.85,SECONDARY,28,x=-3.6)
    xlabel=label('Response amplitude (mV)',-3.35,SECONDARY,30)
    return VGroup(ax,parts,trace,xt,yt,units,xlabel)


def takeaway():
    box=RoundedRectangle(width=11.8,height=5.7,corner_radius=.25,color=TEAL,fill_color=TEAL,fill_opacity=.08)
    text=label('The zeros reveal the average, but only when\nrelease chances are small, as in low calcium.',.05,TEXT,36)
    return VGroup(box,text)

class S00Title(TitleCard):
    TITLE='Counting with Zeros'
    LESSON='Synaptic Transmission and Quantal Release'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',2.4,TEAL,30),label('Synaptic Transmission and Quantal Release',1.4,SECONDARY,30))
        title=label(self.TITLE,-.1,TEXT,54)
        self.play(FadeIn(title),run_time=.6);self.finish()

class S01Question(Timed):
    def construct(self):
        self.add(hist())
        self.at('How do you count')
        self.play(FadeIn(label('How do you count packets when the bumps blur together?',3.4,TEXT,29)),run_time=.3)
        self.finish()

class S02M(Timed):
    def construct(self):
        self.add(label('Mean quantal content',3.0),readings())
        self.at('the mean quantal content')
        self.play(FadeIn(eq('m',-1.35,48,YELLOW,x=-3.8)),run_time=.3)
        self.at('the average number')
        self.play(FadeIn(eq('(1 + 0 + 2 + 0) / 4 = 0.75',-2.2,34,YELLOW)),
                  FadeIn(label('packets per impulse',-2.95,YELLOW,30)),run_time=.5)
        self.add(label('Not the m of sodium gates',-1.35,TEXT,40,x=.3))
        self.finish()

class S03Two(Timed):
    def construct(self):
        self.add(methods())
        self.at('different assumptions')
        self.play(FadeIn(label('Different assumptions',-3.25,SECONDARY,34)),run_time=.4);self.finish()

class S04Direct(Timed):
    def construct(self):
        j=jar();self.add(label('Direct method',3.3,GREEN),j)
        self.at('Every response')
        for n in [1,2,3]:
            coin=Circle(radius=.4,color=YELLOW,fill_color=YELLOW,fill_opacity=.8).move_to([-2.4,3.1,0])
            self.add(coin);self.play(coin.animate.move_to([-2.4,-.8+(n-1)*.9,0]),run_time=.3)
            self.remove(coin,j);j=jar(n);self.add(j);self.wait(.15)
        self.add(label('Whole number of packets',-3.15,SECONDARY,32));self.finish()

class S05Divide(Timed):
    def construct(self):
        self.add(label('Direct method',3.1,GREEN))
        self.at('the average response')
        self.play(FadeIn(label('Mean response (EPP; failures included)',1.9,GREEN,38)),FadeIn(label('EPP = endplate potential',1.1,TEXT,40)),run_time=.35)
        self.at('divided by the size')
        self.play(Create(Line([-5.6,.5,0],[5.6,.5,0],color=SECONDARY)),FadeIn(label('Mean miniature = size of one packet',-.35,GREEN,32)),run_time=.4)
        self.at('gives the average count')
        self.play(FadeIn(eq('= m',-2,48,YELLOW)),run_time=.35);self.finish()

class S06Zeros(Timed):
    def construct(self):
        cells=readings();self.add(label('Include every trial',3.05),cells,eq('Omit zeros: (1 + 2) / 2 = 1.50',-1.4,32,SECONDARY))
        self.at('each failure')
        self.play(*[cells[i][0].animate.set_stroke(RED,5) for i in [1,3]],run_time=.25)
        self.at('response of zero')
        self.play(FadeIn(eq('All trials: 3 / 4 = 0.75',-2.35,36,YELLOW)),FadeIn(label('Leaving out failures overestimates m',-3.15,RED,28)),run_time=.3);self.finish()

class S07Needs(Timed):
    def construct(self):
        self.add(label('Direct method: two assumptions',3.0,GREEN),label('m = mean response / packet size',2.1,YELLOW,32))
        self.at('evoked packets')
        a=chip('Evoked packets = miniatures',YELLOW,36).move_to([0,.7,0]);self.play(FadeIn(a),run_time=.35)
        blocks=VGroup(*[Rectangle(width=1.4,height=.7,color=GREEN,fill_color=GREEN,fill_opacity=.7).move_to([x,-1.5,0]) for x in [-3,-1]])
        self.add(blocks)
        self.at('add linearly')
        self.play(blocks[0].animate.move_to([2,-1.85,0]),blocks[1].animate.move_to([2,-1.15,0]),FadeIn(label('Packets add linearly: 1 + 1 = 2',-2.95,GREEN,34)),run_time=.55);self.finish()

class S08Trick(Timed):
    def construct(self):
        m=methods();self.add(m)
        self.at('The second way');self.play(m[1][0].animate.set_stroke(RED,5),run_time=.4)
        self.at('only the failures');self.play(FadeIn(eq('0  0  0',-1.6,48,RED,3.15)),run_time=.35);self.finish()

class S09Lamps(Timed):
    def construct(self):
        s=stage();self.add(s[0],side([('100 lamps',1,40),('One lamp',-.2,32),('per release site',-1,32)],BLUE))
        self.at('release sites');self.play(FadeIn(s[1]),run_time=.4);self.finish()

class S10Chance(Timed):
    def construct(self):
        s=stage();self.add(s)
        self.at('On each impulse');p=impulse();self.play(FadeIn(p),run_time=.25)
        self.at('chance to flash');self.play(p.animate.shift(LEFT*.6),Transform(s[0],lamps([13,67])),run_time=.35);self.remove(p)
        self.add(side([('Each site: p = 0.01',1.8,30),('m = N × p',.75,38),('100 × 0.01 = 1',-.15,32)],YELLOW))
        self.at('independently of the others');self.play(FadeIn(side([('Independent sites',-1.25,30),('Same chance',-2.15,30),('on every trial',-2.8,30)],SECONDARY)),run_time=.35);self.finish()

class S11Flash(Timed):
    def construct(self):
        s=stage([13,67]);self.add(s)
        self.at('A flash');self.play(Create(Circle(radius=.3,color=YELLOW).move_to(s[0][67])),run_time=.3)
        self.at('one packet released');self.play(FadeIn(side([('Flash',.9,44),('= 1 packet',-.2,44)],YELLOW)),run_time=.3);self.finish()

class S12Dark(Timed):
    def construct(self):
        s=stage();c=side([('All-dark / trials',.6,30),('0 / 0',-.5,48)],RED);self.add(s,c)
        self.at('A failure means');p=impulse();self.play(FadeIn(p),run_time=.25)
        self.at('every single site');self.play(p.animate.shift(LEFT*.6),run_time=.3);self.remove(p)
        self.play(Transform(c,side([('All-dark / trials',.6,30),('1 / 1',-.5,48),('No site flashed',-1.8,30)],RED)),run_time=.25);self.finish()

class S13Rarer(Timed):
    def construct(self):
        s=stage();self.add(s)
        track=Line([.4,1.55,0],[5.8,1.55,0],color=SECONDARY);knob=Dot([.4,1.55,0],color=YELLOW,radius=.13)
        self.add(track,knob,label('Average packets / impulse',2.8,YELLOW,28,x=3.1))
        self.add(*[label(t,.95,YELLOW,28,x=x) for t,x in zip(['0.5','1','2','4'],[.4,2.2,4,5.8])])
        ticker=label('All-dark / trials',-.05,RED,34,x=3.1)
        count=label('0 / 0',-.85,RED,40,x=3.1);self.add(ticker,count)
        # The arrow sits outside the grid, clear of its heading and lamps.
        arrow=Arrow([.2,2.15,0],[-.35,2.15,0],buff=0,color=BLUE);self.add(arrow)
        self.at('more packets released')
        rng=np.random.default_rng(1128)
        for m,x,expected in zip([.5,1,2,4],[.4,2.2,4,5.8],[61,37,14,2]):
            knob.move_to([x,1.55,0]);failures=0
            for j in range(50):
                on=np.flatnonzero(rng.random(100)<m/100).tolist();failures+=not on
                self.remove(count,s[0]);s[0].become(lamps(on));self.add(s[0])
                count=label(f'{failures} / {j+1} = {failures/(j+1):.0%}',-.85,RED,40,x=3.1);self.add(count)
                # One complete displayed trial per draft frame, no counter morphs.
                self.wait(1/15)
            row=label(f'{m:g}: {failures}/50 = {failures/50:.0%}',-1.5-[.5,1,2,4].index(m)*.6,TEXT,40,x=3.1)
            self.add(row)
            self.wait(.25)
        self.add(label('Model failure rates:\n61%, 37%, 14%, 2%',-3.1,RED,30,x=-3.25))
        self.wait(.8);self.finish()

class S14Multiply(Timed):
    def construct(self):
        bulbs=VGroup(*[Circle(radius=.43,color=BLUE,fill_color=BLUE,fill_opacity=.15).move_to([x,1.65,0]) for x in [-4.8,-1.6,1.6,4.8]])
        self.add(label('Independent release sites',3.1,BLUE,34),bulbs)
        self.at('Each site stays dark')
        factors=VGroup(*[eq('1 − p',.5,38,RED,x) for x in [-4.8,-1.6,1.6,4.8]])
        self.play(LaggedStart(*[FadeIn(f) for f in factors],lag_ratio=.2),run_time=.8)
        self.at('The sites are independent')
        self.play(*[b.animate.set_stroke(RED,3) for b in bulbs],run_time=.3)
        self.at('multiply those chances')
        terms=VGroup(eq('(1 − p)',size=48,color=RED),eq('× (1 − p)',size=48,color=RED),eq('× …',size=48,color=RED)).arrange(RIGHT,buff=.22).move_to([0,-.65,0])
        self.play(LaggedStart(*[FadeIn(term) for term in terms],lag_ratio=.6),run_time=.9)
        self.play(FadeIn(eq('= (1 − p)^N',-2,52,RED)),run_time=.35);self.finish()

class S14bSmall(Timed):
    def construct(self):
        self.add(label('All sites dark',3.0,RED,34),eq('(1 − p)^N',1.7,46,RED),eq('N × p = m',-1.25,46,YELLOW),label('Average packets per impulse',-2.2,YELLOW,32))
        self.at('When p is small');self.play(FadeIn(label('Valid when p is small',.65,RED,40,x=2.8)),run_time=.25)
        self.at('comes very close');self.play(FadeIn(eq('≈ e^(−N × p)',.55,44,RED,x=-3.4)),run_time=.35)
        self.at('e to the minus');self.play(FadeIn(eq('= e^(−m)',-.35,44,RED)),run_time=.3);self.finish()

class S14cFormula(Timed):
    def construct(self):
        self.add(label('Failure method',3.1,RED,38),eq('P(failure) ≈ e^(−m)',1.85,40,RED))
        self.at('fraction of failures');self.play(FadeIn(eq('m = −ln(failures / trials)',.35,36,YELLOW)),run_time=.4)
        self.at('The formula is on screen');self.play(FadeIn(label('Independent sites • small chances',-1.45,SECONDARY,32)),FadeIn(label('Same conditions on every trial pooled',-2.5,SECONDARY,30)),run_time=.4);self.finish()

class S15Predict(Timed):
    def construct(self):
        p=prediction();self.add(p[0],VGroup(*p[1][:3]))
        self.at('How often');self.play(FadeIn(VGroup(*p[1][3:])),run_time=.4);self.finish()

class S16Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(prediction(),label('Think about it',3.25,SECONDARY,30,x=3.1))
        ring=Circle(radius=.22,color=TEAL).move_to([5.5,3.2,0]);self.play(Create(ring),run_time=5,rate_func=linear)

class S17Reveal(Timed):
    def construct(self):
        self.add(label('m = 1 packet per impulse',3.1,YELLOW,36))
        tiles=VGroup(*[RoundedRectangle(width=.38,height=.35,corner_radius=.06,color=RED if i<37 else BLUE,fill_color=RED if i<37 else BLUE,fill_opacity=.25 if i<37 else .8).move_to([-5.7+(i%20)*.6,1.65-(i//20)*.52,0]) for i in range(100)])
        self.add(tiles,label('100 trials: 37 dark failures, 63 with release',-1.25,SECONDARY,30))
        self.at('More than a third');self.play(FadeIn(label('Fraction of trials with nothing released',-2.15,RED,32)),FadeIn(eq('e^(−1) = 0.37  (more than a third)',-3.05,32,RED)),run_time=.4);self.finish()

class S18Pulled(Timed):
    def construct(self):
        counts=[0]*7+[1]*7+[2]*4+[3]*2
        cells=VGroup()
        for i,k in enumerate(counts):
            x=-5.5+(i%10)*1.22;y=1.5-(i//10)*2.1
            b=RoundedRectangle(width=1,height=1.65,corner_radius=.1,color=RED if k==0 else BLUE).move_to([x,y,0])
            cells.add(VGroup(b,eq(str(k),y,42,RED if k==0 else YELLOW,x)))
        self.add(label('20 illustrative trials: packets released',3.15,SECONDARY,32),cells,eq('First 14: 7 / 14 = 0.50',-2.1,32,YELLOW),label('7 zeros (35%); mean across all 20 ≈ 1',-3.05,SECONDARY,30))
        mean=self.mobjects[2]
        self.at('pulled up by trials');self.remove(mean);self.add(eq('All 20: 21 / 20 = 1.05',-2.1,32,YELLOW))
        self.play(*[cells[i][0].animate.set_stroke(YELLOW,5) for i in range(14,20)],run_time=.6);self.finish()

class S19Why(Timed):
    def construct(self):
        self.add(methods(False))
        direct=label('q = packet size',.5,GREEN,40,x=-3.15)
        failure=label('q = packet size',.5,RED,40,x=3.15)
        self.add(direct,failure,label('Mean response / q',-1,GREEN,36,x=-3.15),label('Fraction of zeros',-1,RED,36,x=3.15))
        self.at('never uses the size')
        strike=Line(failure.get_left()+LEFT*.12,failure.get_right()+RIGHT*.12,color=RED,stroke_width=3)
        self.play(Create(strike),FadeIn(label('No size measurement',-2,SECONDARY,34,x=3.15)),run_time=.4);self.finish()

class S20Wrong(Timed):
    def construct(self):
        m=methods(False);self.add(m,label('Example: true m = 1',3.25,YELLOW,34))
        mini=Rectangle(width=.8,height=.6,color=GREEN,fill_color=GREEN,fill_opacity=.8).move_to([-4.4,.3,0]);ev=mini.copy().move_to([-1.9,.3,0]);self.add(mini,ev,label('Miniature',-.55,GREEN,34,x=-4.4),label('Evoked',-.55,GREEN,34,x=-1.9),label('Count zeros',.7,RED,36,x=3.15))
        self.at('differed in size');self.play(ev.animate.stretch_to_fit_height(1.2).shift(UP*.3),FadeIn(label('Twice the packet size',-1.35,YELLOW,34,x=-3.15)),run_time=.45)
        self.at('would go wrong');self.play(m[0][0].animate.set_stroke(RED,5),FadeIn(label('Direct m = 2.0',-2.25,RED,40,x=-3.15)),run_time=.35)
        self.at('The failure method would not');self.play(m[1][0].animate.set_stroke(GREEN,5),FadeIn(label('Failure m = 1.0',-.5,YELLOW,40,x=3.15)),run_time=.35)
        self.at('failures can still');self.play(FadeIn(label('Reliable detection\nof failures',-1.85,GREEN,38,x=3.15)),run_time=.35);self.finish()

class S21Agree(Timed):
    def construct(self):
        self.add(label('Two estimates of average packets / impulse',3.15,TEXT,32))
        axis=NumberLine(x_range=[0,2,.5],length=10,include_numbers=False,color=SECONDARY).move_to([0,-1.4,0]);self.add(axis)
        self.add(*[eq(f'{v:g}',-1.95,30,SECONDARY,axis.n2p(v)[0]) for v in [0,.5,1,1.5,2]])
        a=VGroup(Rectangle(width=5,height=.72,color=GREEN,fill_color=GREEN,fill_opacity=.4).move_to([-2.5,1.3,0]),label('Direct m = 1.00',1.3,TEXT,34,x=-2.5))
        b=VGroup(Rectangle(width=4.95,height=.72,color=RED,fill_color=RED,fill_opacity=.4).move_to([2.475,.35,0]),label('Failure m = 0.99',.35,TEXT,34,x=2.475));self.add(a,b)
        self.at('agree');self.play(b.animate.shift(LEFT*5),run_time=.7)
        self.at('supports two things');self.play(FadeIn(label('Agreement supports the assumptions',-2.95,YELLOW,38)),run_time=.35);self.finish()

class S22Evidence(Timed):
    def construct(self):
        self.add(label('Agreement supports…',3.1,YELLOW,40),label('Direct 1.00 ≈ Failure 0.99',2.05,SECONDARY,38))
        self.at('the same units');self.play(FadeIn(chip('✓ Same packet units',YELLOW,46).move_to([0,.4,0])),run_time=.4)
        self.at('many small independent chances');self.play(FadeIn(chip('✓ Many small, independent chances',BLUE,42).move_to([0,-1.9,0])),run_time=.4);self.finish()
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.25)

class S23Worked(Timed):
    def construct(self):
        # Start clear; the previous scene has already faded its check marks.
        self.at('recording of')
        self.play(FadeIn(label('Made-up recording',3.1,SECONDARY,40)),FadeIn(eq('200 stimuli • 74 failures',1.9,40)),run_time=.3)
        self.play(FadeIn(eq('q = 0.40 mV; mean EPP = 0.40 mV',.8,34,GREEN)),run_time=.3)
        self.play(FadeIn(label('Mean EPP counts failures as zero',-.1,SECONDARY,36)),run_time=.25)
        self.at('the two estimates');self.play(FadeIn(eq('Direct: 0.40 / 0.40 = 1.00',-1.4,40,YELLOW)),run_time=.3)
        self.at('both come out');self.play(FadeIn(eq('Failure: −ln(74 / 200) = 0.99',-2.8,40,YELLOW)),run_time=.3);self.finish()

class S24Poisson(Timed):
    def construct(self):
        h=hist(True);preview=hist(False)[2];self.add(h[0],preview,*h[3:])
        self.at('predicts how many trials');self.play(FadeIn(h[1]),Transform(preview,h[2]),run_time=.6)
        tags=VGroup()
        for k in range(4):
            target=h[0].c2p(.4*k, [10.5,9.7,4.5,1.4][k])
            text=label(f'k = {k}',1.5-k*.75,RED if k==0 else BLUE,28,x=4.1)
            tags.add(text,Line(text.get_left(),target,color=RED if k==0 else BLUE,stroke_width=1.5))
        self.add(tags,label('k = packets; red = failures',2.25,SECONDARY,28,x=2.9))
        self.at('the Poisson distribution');self.play(FadeIn(eq('P(k) = e^(−m) × m^k / k!',3.65,30,YELLOW)),run_time=.3)
        self.play(FadeIn(label('m = 1: P(0) = 0.37 → 74 / 200',2.95,RED,28,x=2.3)),run_time=.3);self.finish()

class S25Small(Timed):
    def construct(self):
        bulbs=VGroup(*[Circle(radius=.7,color=BLUE,fill_color=YELLOW,fill_opacity=p*10).move_to([x,1.3,0]) for x,p in zip([-4,0,4],[.02,.01,.04])]);self.add(bulbs,label('Each site’s chance must be small',3.1,BLUE,36))
        self.at("Each site's chance");self.play(FadeIn(VGroup(*[eq(t,-.05,36,YELLOW,x) for t,x in zip(['p₁ = 0.02','p₂ = 0.01','p₃ = 0.04'],[-4,0,4])])),run_time=.4)
        self.at('Small not equal');self.play(FadeIn(label('Small, not equal',-1.4,YELLOW,40)),FadeIn(eq('m = p₁ + p₂ + p₃ + …',-2.65,38,YELLOW)),run_time=.4);self.finish()

class S26Normalca(Timed):
    def construct(self):
        s=stage();self.add(s,label('Calcium',2.7,TEAL,34,x=3.3))
        track=Rectangle(width=.6,height=2.5,color=TEAL).move_to([3.3,.8,0]);bar=Rectangle(width=.5,height=.3,color=TEAL,fill_color=TEAL,fill_opacity=1).move_to([3.3,-.25,0]);self.add(track,bar)
        self.at('restore normal calcium');self.play(bar.animate.stretch_to_fit_height(2.3).move_to([3.3,.8,0]),run_time=.8)
        self.at('tens of packets');rng=np.random.default_rng(27);self.add(label('Tens of packets',-1.2,YELLOW,32,x=3.3))
        for _ in range(3):
            on=rng.choice(100,size=int(rng.integers(30,41)),replace=False).tolist();self.play(Transform(s[0],lamps(on)),run_time=.3)
        self.add(label('Size of each chance:\ncheck, don’t assume',-2.5,SECONDARY,28,x=3.3));self.finish()

class S27Vanish(Timed):
    def construct(self):
        rng=np.random.default_rng(27);s=stage(rng.choice(100,35,replace=False));self.add(s)
        c=side([('All-dark / trials',1.1,30),('0 / 25',0,46)],RED);self.add(c)
        self.at('Failures vanish')
        for n in [50,75,100]:
            self.remove(c);c=side([('All-dark / trials',1.1,30),(f'0 / {n}',0,46)],RED);self.add(c)
            self.play(Transform(s[0],lamps(rng.choice(100,35,replace=False))),run_time=.4)
        self.at('Low calcium');self.play(Transform(s[0],lamps()),FadeOut(c),FadeIn(side([('Low calcium',1.8,38),('Failures common',.6,32),('enough to measure',-.2,30)],TEAL)),run_time=.45)
        self.play(Transform(s[0],lamps([23])),run_time=.25);self.play(Transform(s[0],lamps()),FadeIn(side([('All-dark / trials',-1.65,34),('37 / 100',-2.65,46)],RED)),run_time=.3);self.finish()

class S28Takeaway(Timed):
    def construct(self):
        self.add(label('Low calcium',2.75,TEAL,42),chip('Small release chances',YELLOW,38).move_to([0,1.15,0]),chip('Common failures',RED,38).move_to([0,-.7,0]))
        self.at('It makes the chances small');self.play(Indicate(self.mobjects[1],color=YELLOW),run_time=.5)
        self.at('as the mathematics needs');self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.25)
        self.play(FadeIn(takeaway()),run_time=.4);self.finish()
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.25)

class S29End(EndCard):
    LINE='The zeros reveal the average, but only when\nrelease chances are small, as in low calcium.'
    def construct(self):
        self.play(FadeIn(takeaway()),run_time=.5);self.add(label('biochemistrypedia.com',-3.3,TEAL,28));self.finish()
