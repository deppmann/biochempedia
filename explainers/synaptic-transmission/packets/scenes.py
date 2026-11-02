"""Chapter 2: word-timed, equation-computed quantal-release teaching film.
COLOR MAP (shared with scenes.old.py): BLUE presynaptic terminal; YELLOW
acetylcholine / quantum / vesicle filling; GREEN muscle voltage response;
TEAL calcium; PURPLE magnesium; PINK receptors; ORANGE firing threshold;
RED failure; GOLD fault highlight; GREY membranes, axes, secondary labels.
The histogram is an illustrative model, not historical experimental data:
N=200, Poisson mean 1, q=.40 mV; independent packet SD=.048 mV,
recording SD=.025 mV. Conditional Gaussian bins use Gaussian CDF differences (0.08 mV bins).
Response traces reuse the reference's normalized difference of exponentials.
"""
import math
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
PINK = '#E88FC0'
ORANGE = '#F29E4C'


def label(s, x=0, y=3.0, color=TEXT, size=28):
    return T(s, size=size, color=color).move_to([x,y,0])


def arrow(a,b,c=GREY):
    return Arrow(a,b,buff=.12,color=c,stroke_width=4)


_F = lambda s: np.exp(-s/.22)-np.exp(-s/.04)
_PEAK = max(_F(s) for s in np.linspace(.001,1,400))


def trace(n=1,x=-5.7,y=-1.8,w=11.4,h=2.8,onset=.22,color=GREEN):
    # x is normalized time, in the same units as the reference model.
    ts=np.linspace(0,1.6,480)
    ys=[n*h*(_F(t-onset)/_PEAK if t>=onset else 0) for t in ts]
    return VMobject(color=color,stroke_width=4).set_points_as_corners(
        [[x+w*t/1.6,y+v,0] for t,v in zip(ts,ys)])


def vesicle(x=0,y=0,r=.45,filled=True):
    ring=Circle(radius=r,color=YELLOW,stroke_width=3).move_to([x,y,0])
    dots=VGroup()
    if filled:
        for i in range(49 if r>1 else 13):
            count=49 if r>1 else 13
            a=i*2.39996; rad=r*.73*np.sqrt(i/count)
            dots.add(Dot([x+rad*np.cos(a),y+rad*np.sin(a),0],radius=r*(.04 if r>1 else .08),color=YELLOW))
    return VGroup(ring,dots)


# Large teaching diagrams; all positions stay inside the safe frame.
LIGHT = '#C6CDD8'

def terminal(cx=-3.3):
    return RoundedRectangle(width=5.5,height=4.5,corner_radius=.5,
        color=BLUE,fill_color=BLUE,fill_opacity=.10).move_to([cx,.25,0])


def stocked(cx=-3.3):
    return VGroup(*[vesicle(cx-2.1+(i%8)*.6,-1.25+(i//8)*.95,.19) for i in range(32)])


def divider():
    return Line([0,-2.8,0],[0,3.35,0],color=GREY,stroke_opacity=.35)


def rain(cx,n):
    rng=np.random.default_rng(18+n)
    return VGroup(*[Line([cx+x,y,0],[cx+x-.08,y-.52,0],color=BLUE,
        stroke_width=3 if n>10 else 6,stroke_opacity=.48 if n>10 else 1)
        for x,y in zip(rng.uniform(-2.35,2.35,n),rng.uniform(-2.0,2.4,n))])


def rain_panel():
    return VGroup(divider(),label('normal calcium',-3.3,3,TEAL),rain(-3.3,65),
        trace(x=-5.95,y=-2.45,w=5.25,h=4.4))


def frog_junction():
    muscle=RoundedRectangle(width=3.5,height=.65,corner_radius=.18,color=GREEN,
        fill_color=GREEN,fill_opacity=.2).move_to([3.3,-1.8,0])
    ending=RoundedRectangle(width=2,height=.7,corner_radius=.25,color=BLUE,
        fill_color=BLUE,fill_opacity=.15).move_to([3.3,-.85,0])
    nerve=Line([3.3,.4,0],[3.3,-.5,0],color=BLUE,stroke_width=7)
    return VGroup(muscle,ending,nerve,label('frog junction',3.3,-2.5,LIGHT,28))


def release(scene,cx,number,rt=.4):
    # Fusion is a local membrane flash followed by transmitter dots in the cleft.
    tick=arrow([cx-2.35,1.5,0],[cx-1.2,1.5,0],BLUE)
    scene.play(GrowArrow(tick),run_time=rt*.22)
    if number:
        vs=VGroup(*[vesicle(cx+(j-(number-1)/2)*.62,-1.6,.22) for j in range(number)])
        flashes=VGroup(*[Arc(radius=.3,start_angle=0,angle=PI,color=YELLOW,
            stroke_width=6).move_to([cx+(j-(number-1)/2)*.62,-2,0]) for j in range(number)])
        dots=VGroup(*[Dot([cx+(j-(number-1)/2)*.62+(i-2)*.09,-2.08,0],
            radius=.045,color=YELLOW) for j in range(number) for i in range(5)])
        scene.add(vs)
        scene.play(vs.animate.shift(DOWN*.35),run_time=rt*.22)
        scene.remove(vs); scene.add(flashes,dots)
        scene.play(dots.animate.shift(DOWN*.55),FadeOut(flashes),run_time=rt*.36)
        scene.remove(dots)
    else:
        scene.wait(rt*.58)
    scene.play(FadeOut(tick),run_time=rt*.2)


COUNTS=[0,1,0,2,0,1,3,0,1]

def small_trials(failures=False):
    g=VGroup()
    for i,n in enumerate(COUNTS):
        row,col=divmod(i,3); x=-4.35+col*4.35; y=2.25-row*2.15
        box=RoundedRectangle(width=3.95,height=1.85,corner_radius=.12,color=GREY,
            stroke_width=2).move_to([x,y,0])
        t=trace(n,x=x-1.7,y=y-.48,w=3.4,h=.24,color=GREEN if n else (RED if failures else LIGHT))
        mark=Line([x-1.23,y-.73,0],[x-1.23,y-.54,0],color=BLUE,stroke_width=4)
        lab=label('failure',x,y+.55,RED,26) if n==0 else VGroup()
        g.add(VGroup(box,mark,t,lab))
        if not failures: lab.set_opacity(0)
    return g


# Poisson weights with Gaussian packet variability and independent recording noise.
HX=-5.55; HY=-2.25; HW=11.25; HH=5.2
Q=.40; N=200; MU=1.0; MAXX=1.52; MAXY=80

def hp(x,y): return np.array([HX+HW*(x+.04)/MAXX,HY+HH*y/MAXY,0])


def hist_axes(stage=4):
    axes=VGroup(Line([HX,HY,0],hp(1.46,0),color=LIGHT),
        Line([HX,HY,0],[HX,HY+HH,0],color=LIGHT))
    for k in range(4):
        pt=hp(k*Q,0)
        axes.add(Line(pt+DOWN*.07,pt+UP*.07,color=LIGHT),
            label(['0','0.4','0.8','1.2'][k],pt[0],HY-.35,LIGHT,26))
        if k: axes.add(label(['','q','2q','3q'][k],pt[0],HY-.82,GREEN,26))
    for v in [0,20,40,60,80]:
        axes.add(label(str(v),HX-.42,hp(0,v)[1],LIGHT,26))
    return axes


def hist_labels():
    return VGroup(label('response amplitude (mV)',.25,-3.5,LIGHT,26),
        T('number of trials',size=26,color=LIGHT).rotate(PI/2).move_to([-6.5,.35,0]))


def model_title():
    return label('Illustrative quantal model (200 trials)',.1,3.5,LIGHT,28)


def zero_bar(height=N*math.exp(-MU)):
    return Rectangle(width=HW*.08/MAXX,height=HH*height/MAXY,color=RED,
        fill_color=RED,fill_opacity=.7).move_to(hp(0,height/2))


def bin_values(k,mini=False):
    sd=.063 if mini else math.sqrt(k*.048**2+.025**2)
    bw=.04 if mini else .08
    edges=k*Q+np.arange(-3.5 if not mini else -6.5,4.5 if not mini else 7.5)*bw
    weight=N*math.exp(-MU)*MU**k/math.factorial(k)
    vals=[weight*(math.erf((b-k*Q)/(sd*math.sqrt(2)))-math.erf((a-k*Q)/(sd*math.sqrt(2))))/2
        for a,b in zip(edges[:-1],edges[1:])]
    if mini:
        # An independent spontaneous distribution, normalized explicitly for comparison.
        scale=max(v for _,_,v in bin_values(1))/max(vals)
        vals=[v*scale for v in vals]
    return list(zip(edges[:-1],edges[1:],vals))


def bump(k,color=GREEN,mini=False):
    bars=VGroup()
    for a,b,val in bin_values(k,mini):
        if val<.015: continue
        bars.add(Rectangle(width=HW*(b-a)/MAXX,height=HH*val/MAXY,
            stroke_width=2.7 if mini else .7,color=YELLOW if mini else color,
            fill_color=color,fill_opacity=0 if mini else .55).move_to(hp((a+b)/2,val/2)))
    return bars


def histogram(stage=4,overlay=False):
    g=VGroup(hist_axes(),hist_labels(),model_title())
    if stage>=1: g.add(zero_bar())
    for k in range(1,min(stage,4)): g.add(bump(k))
    if overlay: g.add(bump(1,mini=True))
    return g


def smooth_hump():
    # A possible continuous gamma-shaped model: zero density at zero, one mode.
    xs=np.linspace(0,1.46,250)
    ys=(xs/.5)**3*np.exp(3-6*xs)*43
    return DashedVMobject(VMobject(color=LIGHT,stroke_width=5).set_points_as_corners(
        [hp(x,y) for x,y in zip(xs,ys)]),num_dashes=40)


def predict_question():
    return label('Smooth flow turned down: what shape?',0,3.5,TEXT,29)


def formula():
    main=VGroup(label('response',-4.1,.85,GREEN,40),label('≈',-1.8,.85,TEXT,42),
        label('count',-.15,.85,BLUE,40),label('×',1.6,.85,TEXT,42),label('size',3.65,.85,GREEN,40))
    return VGroup(main,label('on average:  EPP ≈ m × q',0,-.05,TEXT,30),
        label('m = average count',-2.5,-.8,BLUE,26),label('q = miniature size',2.7,-.8,GREEN,26))


def count_diagram():
    term=RoundedRectangle(width=3.4,height=.85,corner_radius=.25,color=BLUE,
        fill_color=BLUE,fill_opacity=.15).move_to([-.8,2.7,0])
    return VGroup(term,label('nerve terminal',-.8,2.7,BLUE,26),
        arrow([-.15,2.2,0],[-.15,1.25,0],BLUE),
        chip('calcium',TEAL,26).move_to([-4.75,2.7,0]),
        arrow([-3.8,2.7,0],[-2.6,2.7,0],TEAL))


def size_diagram():
    rec=VGroup(*[RoundedRectangle(width=.36,height=.72,corner_radius=.09,color=PINK,
        fill_color=PINK,fill_opacity=.5).move_to([4.4+i*.51,2.65,0]) for i in range(3)])
    return VGroup(vesicle(2.85,2.65,.57),rec,label('receptors',4.9,3.4,PINK,26),
        arrow([2.85,1.98,0],[3.5,1.25,0],GREEN),
        arrow([4.8,2.15,0],[3.85,1.25,0],GREEN),
        label('vesicle',2.85,3.4,YELLOW,26))


def count_samples():
    g=VGroup(label('packet count',-3.15,-1.65,BLUE,28))
    for j,n in enumerate([0,1,2]):
        x=-4.8+1.65*j
        box=RoundedRectangle(width=1.4,height=1.1,corner_radius=.12,color=GREY).move_to([x,-2.65,0])
        g.add(box,label(str(n),x,-2.4,RED if not n else YELLOW,26))
        for k in range(n): g.add(vesicle(x+(k-(n-1)/2)*.4,-2.9,.15))
    return g


def size_sample():
    return VGroup(label('miniature',3.4,-1.65,GREEN,28),
        trace(x=1.2,y=-3.1,w=4.5,h=1.0),Line([1.2,-3.1,0],[5.7,-3.1,0],color=GREY))


def jar():
    body=RoundedRectangle(width=3,height=3.7,corner_radius=.3,color=LIGHT,
        fill_color=GREY,fill_opacity=.15).move_to([-2.5,.35,0])
    # A warm, draped cloth conceals the contents; folds distinguish it from glass.
    cloth_color='#9F8CA6'
    cloth=Polygon([-3.85,2.18,0],[-1.15,2.18,0],[-.94,-1.05,0],
        [-1.65,-.86,0],[-2.5,-1.12,0],[-3.3,-.86,0],[-4.06,-1.05,0],
        color=cloth_color,fill_color=cloth_color,fill_opacity=1,stroke_width=2)
    folds=VGroup(*[Line([x,2.1,0],[x+dx,-.8,0],color='#6E6077',stroke_width=3)
        for x,dx in [(-3.35,-.22),(-2.5,.06),(-1.65,.22)]])
    lid=Rectangle(width=3.3,height=.25,color=LIGHT,fill_color=cloth_color,
        fill_opacity=1).move_to([-2.5,2.25,0])
    scale=RoundedRectangle(width=4.4,height=1.0,corner_radius=.15,color=TEXT).move_to([-2.5,-2.15,0])
    return VGroup(body,cloth,folds,lid,scale,label('scale',-2.5,-3,LIGHT,28))


def coin_reference():
    coin=Circle(radius=.55,color=GOLD,fill_color=GOLD,fill_opacity=.35).move_to([3,1.8,0])
    return VGroup(coin,label("one coin's weight",3,.6,GOLD,29),
        label('1 weight unit',3,-.1,LIGHT,28))


def quantum_view(filled=False):
    # Keep the entire histogram on the right, with labels re-set at readable size.
    g=VGroup()
    def qp(x,y): return np.array([.65+5.25*(x+.04)/MAXX,-1.7+3.9*y/80,0])
    g.add(Line(qp(-.04,0),qp(1.46,0),color=LIGHT),
        Line(qp(-.04,0),qp(-.04,80),color=LIGHT))
    for k in range(4):
        vals=[(-.04,.04,N*math.exp(-MU))] if k==0 else bin_values(k)
        for a,b,v in vals:
            if v<.015: continue
            g.add(Rectangle(width=5.25*(b-a)/MAXX,height=3.9*v/80,
                color=RED if k==0 else GREEN,fill_color=RED if k==0 else GREEN,
                fill_opacity=.55,stroke_width=.7).move_to(qp((a+b)/2,v/2)))
        g.add(label(['0','q','2q','3q'][k],qp(k*Q,0)[0],-2.1,LIGHT,26))
    g.add(label('response amplitudes',3.3,2.85,GREEN,28),
        label('200 trials',3.3,2.35,LIGHT,26))
    return VGroup(vesicle(-3.65,.25,2.4,filled),g)


class S00Title(TitleCard):
    TITLE='Turn Release Down to See the Packets'
    LESSON='Synaptic Transmission and Quantal Release'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.7,TEAL,22),label(self.LESSON,0,1.85,GREY,25))
        title=T('Turn Release Down\nto See the Packets',size=50,font=TITLE_FONT,line_spacing=1.1)
        self.play(FadeIn(title),Create(Line([-1.2,-1.5,0],[1.2,-1.5,0],color=GOLD)),run_time=.7)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        t=trace(); self.add(t,label('evoked response',0,2.7,GREEN))
        self.at("If the nerve's response")
        self.play(Create(Line([-5.7,-2,0],[5.7,-2,0],color=GREY)),run_time=.4)
        self.at("why can't you")
        self.play(FadeIn(label('Where are the miniatures?',0,-3, TEXT,32)),run_time=.5)
        self.finish()


class S02Downpour(SpokenScene):
    def construct(self):
        term=terminal(); vs=stocked(); self.add(divider(),term,vs)
        self.at('In normal calcium'); self.play(FadeIn(label('normal calcium',-3.3,3.15,TEAL)),run_time=.3)
        impulse=arrow([-6,2.05,0],[-4.65,2.05,0],BLUE)
        self.at('one impulse'); self.play(GrowArrow(impulse),run_time=.3)
        self.at('releases dozens')
        # The bottom part of the terminal box is a bounded cleft cutaway.
        membrane=Line([-6,-1.35,0],[-.6,-1.35,0],color=LIGHT,stroke_width=4)
        cleft=Rectangle(width=5.35,height=.55,stroke_width=0,fill_color=GREY,
            fill_opacity=.13).move_to([-3.3,-1.66,0])
        self.add(cleft,membrane,label('cleft',-3.3,-2.45,LIGHT,26))
        for row in range(4):
            wave=VGroup(*vs[row*8:(row+1)*8])
            flashes=VGroup(*[Arc(radius=.23,start_angle=0,angle=PI,color=YELLOW,
                stroke_width=6).move_to([-5.4+j*.6,-1.35,0]) for j in range(8)])
            dots=VGroup(*[Dot([-5.4+j*.6+(i-1)*.09,-1.5,0],radius=.045,color=YELLOW)
                for j in range(8) for i in range(3)])
            self.play(*[v.animate.move_to([-5.4+j*.6,-1.16,0]) for j,v in enumerate(wave)],run_time=.18)
            self.play(FadeOut(wave),FadeIn(flashes),FadeIn(dots),run_time=.12)
            self.play(dots.animate.shift(DOWN*.29),FadeOut(flashes),run_time=.18)
            self.remove(dots)
        self.finish()



class S03Merge(SpokenScene):
    def construct(self):
        self.add(divider(),label('normal calcium',-3.3,3,TEAL))
        t=trace(x=-5.95,y=-2.45,w=5.25,h=4.4)
        self.at('They merge'); self.play(Create(t),run_time=1.2)
        self.at('like a downpour'); r=rain(-3.3,65)
        self.play(FadeIn(r,shift=DOWN*.4),run_time=.65); self.bring_to_front(t); self.finish()


class S04Drizzle(SpokenScene):
    def construct(self):
        self.add(rain_panel()); r=rain(3.3,9)
        self.at('To count drops'); self.play(LaggedStart(*[FadeIn(d,shift=DOWN*.4) for d in r],lag_ratio=.05),run_time=.7)
        self.at('you need a drizzle'); self.play(FadeIn(label('drizzle',3.3,3,BLUE)),run_time=.35); self.finish()


class S05Lowca(SpokenScene):
    def construct(self):
        r=rain(3.3,9); self.add(rain_panel(),r)
        self.at('So'); self.play(FadeIn(label('José del Castillo · Bernard Katz',0,-3.35,LIGHT,28)),run_time=.4)
        self.at('lowered calcium'); self.play(FadeIn(label('low calcium',3.3,3.1,TEAL)),run_time=.35)
        self.at('raised magnesium'); self.play(FadeIn(label('high magnesium',3.3,2.45,PURPLE)),run_time=.35)
        self.at('frog junction'); self.play(FadeOut(r),FadeIn(frog_junction()),run_time=.45); self.finish()


class S06Trickle(SpokenScene):
    def construct(self):
        self.add(divider(),terminal(),terminal(3.3),stocked(),
            label('normal calcium',-3.3,3.15,TEAL),label('low calcium',3.3,3.4,TEAL),
            label('high magnesium',3.3,2.8,PURPLE))
        # A filled reserve remains inside the right terminal; only selected vesicles fuse.
        self.add(VGroup(*[vesicle(1.4+i*.6,.6,.2) for i in range(7)]))
        self.at('That cut')
        reading=label('impulse 1: 0 packets',3.3,-3.15,RED,28); self.add(reading)
        for i,n in enumerate([0,1,0,2]):
            if i: self.play(Transform(reading,label(f'impulse {i+1}: {n} packet'+('' if n==1 else 's'),
                3.3,-3.15,RED if n==0 else YELLOW,28)),run_time=.08)
            release(self,3.3,n,.38)
        self.finish()


class S07Failure(SpokenScene):
    def construct(self):
        grid=small_trials(); impulse_label=label('nerve impulse',-4.35,3.5,BLUE,26)
        self.at('Now'); self.add(impulse_label)
        leader=VMobject(color=BLUE,stroke_width=2).set_points_as_corners(
            [[-5.7,3.5,0],[-6.5,3.5,0],[-6.5,1.58,0],[-5.58,1.58,0]])
        self.add(leader)
        for b in grid:
            self.play(FadeIn(b[0]),Create(b[1]),run_time=.10)
            self.play(Create(b[2]),run_time=.14)
        self.at('failure',lead=0)
        for i,n in enumerate(COUNTS):
            if n==0: grid[i][3].set_opacity(1)
        self.play(*[grid[i][2].animate.set_color(RED) for i,n in enumerate(COUNTS) if n==0],
            *[FadeIn(grid[i][3]) for i,n in enumerate(COUNTS) if n==0],run_time=.25)
        self.finish()


class S08Sort(SpokenScene):
    def construct(self):
        grid=small_trials(True)
        impulse=label('nerve impulse',-4.35,3.5,BLUE,26)
        self.add(grid,impulse)
        self.at('When a response'); self.play(Indicate(grid[1][2],scale_factor=1.06),run_time=.5)
        counter=VGroup(label('many more impulses:',1.7,3.5,LIGHT,28),
            label('9',4.45,3.5,LIGHT,28))
        self.at('stimulated many times'); self.play(FadeIn(counter),run_time=.2)
        # All 200 trials have an individual card; unsorted cards stream in first.
        values=COUNTS+list(np.random.default_rng(42).permutation([0]*70+[1]*70+[2]*36+[3]*15))
        cards=VGroup()
        for i,n in enumerate(values):
            x=-5.95+(i%20)*.625; y=2.25-(i//20)*.48
            card=VGroup(Rectangle(width=.49,height=.34,color=RED if n==0 else GREEN,stroke_width=1),
                trace(n,x=-.20,y=-.09,w=.40,h=.055,color=RED if n==0 else GREEN)).move_to([x,y,0])
            cards.add(card)
        self.play(*[Transform(g,cards[i]) for i,g in enumerate(grid)],FadeOut(impulse),run_time=.3)
        self.remove(grid); self.add(*cards[:9])
        # Reveal cards in batches, updating the counter to the exact visible count.
        for start in range(9,200,24):
            end=min(start+24,200)
            self.play(LaggedStart(*[FadeIn(c,shift=UP*.16) for c in cards[start:end]],lag_ratio=.025),
                Transform(counter[1],label(str(end),4.45,3.5,LIGHT,28)),run_time=.12)
        self.at('sorted the sizes')
        slots=[0]*4; moves=[]
        for c,n in zip(cards,values):
            j=slots[n]; slots[n]+=1
            moves.append(c.animate.move_to([-5.98+3.2*n+(j%5)*.54,2.35-(j//5)*.32,0]).scale(.86))
        self.play(*moves,run_time=.8)
        names=VGroup(*[label(t,-4.9+3.2*i,-3.15,RED if i==0 else GREEN,28)
            for i,t in enumerate(['failures','small','larger','largest'])])
        self.play(FadeIn(names),run_time=.2)
        self.finish()
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.2)


class S09Axes(SpokenScene):
    def construct(self):
        a=hist_axes(); labs=hist_labels()
        self.at('Picture a histogram'); self.play(Create(a),run_time=.8)
        self.at('Response size'); self.play(FadeIn(labs[0]),run_time=.5)
        self.at('number of trials'); self.play(FadeIn(labs[1]),run_time=.5); self.finish()


class S10Predict(SpokenScene):
    def construct(self):
        self.add(hist_axes(),hist_labels())
        self.at('If release were'); self.play(FadeIn(predict_question()),run_time=.5); self.finish()


class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(hist_axes(),hist_labels(),predict_question()); self.wait(5)


class S12Hump(SpokenScene):
    def construct(self):
        self.add(hist_axes(),hist_labels()); hump=smooth_hump()
        self.at('One simple'); self.play(Create(hump),run_time=1.2)
        self.at('smooth spread'); self.play(FadeIn(label('One possible smooth-flow model',0,3.5,LIGHT,28)),
            FadeIn(label('no all-or-none step',2.1,2.65,LIGHT,28)),run_time=.45)
        marks=VGroup(*[Line(hp(k*Q,65),hp(k*Q,70),color=GREEN,stroke_width=4) for k in range(1,4)])
        spans=VGroup(*[DoubleArrow(hp(k*Q,67.5),hp((k+1)*Q,67.5),buff=.12,color=GREEN)
            for k in range(1,3)])
        self.at('The telling sign'); self.play(Create(marks),Create(spans),
            FadeIn(label('packet prediction: peaks one q apart',1,1.65,GREEN,28)),run_time=.6); self.finish()


class S13Notthat(SpokenScene):
    def construct(self):
        hump=smooth_hump(); title=label('One possible smooth-flow model',0,3.5,LIGHT,28)
        self.add(hist_axes(),hist_labels(),hump,title)
        self.at('That is not'); self.play(hump.animate.set_opacity(.25),run_time=.4)
        self.at('Watch the trials')
        dots=VGroup(); stacks=[0]*4
        for k in [1,0,2,1,0,3,1,2,0,1,0,1]:
            pos=hp(k*Q,4+stacks[k]*4); stacks[k]+=1
            d=Dot([pos[0],3.15,0],radius=.075,color=RED if k==0 else GREEN)
            self.add(d); self.play(d.animate.move_to(pos),run_time=.10); dots.add(d)
            if len(dots)==1: self.remove(hump,title); self.add(model_title())
        self.finish()


class S14Zero(SpokenScene):
    def construct(self):
        self.add(histogram(0))
        self.at('A tall bar'); self.play(GrowFromEdge(zero_bar(),DOWN),run_time=1.2)
        self.at('These are the failures'); self.play(FadeIn(label('failures',-3.95,2.55,RED,28)),run_time=.4); self.finish()


class S15One(SpokenScene):
    def construct(self):
        self.add(histogram(1)); b=bump(1)
        self.at('A bump grows'); self.play(LaggedStart(*[GrowFromEdge(v,DOWN) for v in b],lag_ratio=.025),run_time=1.1)
        self.at('The miniature histogram')
        mini=bump(1,mini=True).shift(RIGHT*1.2)
        labs=VGroup(label('spontaneous miniatures',hp(Q,0)[0],1.5,YELLOW,28),
            label('independent model; scaled to match',.9,.85,LIGHT,26))
        self.play(FadeIn(mini),FadeIn(labs),run_time=.3)
        self.play(mini.animate.shift(LEFT*1.2),run_time=.9); self.finish()


class S16Twothree(SpokenScene):
    def construct(self):
        self.add(histogram(2))
        self.at('A smaller bump'); self.play(LaggedStart(*[GrowFromEdge(v,DOWN) for v in bump(2)],lag_ratio=.03),run_time=.9)
        self.at('A smaller one'); self.play(LaggedStart(*[GrowFromEdge(v,DOWN) for v in bump(3)],lag_ratio=.03),run_time=.9); self.finish()


class S17Broad(SpokenScene):
    def construct(self):
        self.add(histogram(4)); braces=VGroup()
        for k in range(1,4):
            sd=math.sqrt(k*.048**2+.025**2); top=bump(k).get_top()[1]+.20
            left=hp(k*Q-2*sd,0); right=hp(k*Q+2*sd,0); left[1]=right[1]=top
            braces.add(VGroup(Line(left,right,color=GREEN,stroke_width=3),
                Line(left+DOWN*.1,left+UP*.1,color=GREEN),Line(right+DOWN*.1,right+UP*.1,color=GREEN)))
        self.at('The bumps are broad'); self.play(Create(braces),run_time=.6)
        self.at('one unit is'); self.play(FadeIn(label('q varies from packet to packet',.7,2.15,GREEN,28)),run_time=.4)
        self.at('recording has noise'); self.play(FadeIn(label('recording noise',.7,1.45,LIGHT,28)),run_time=.4); self.finish()


class S18Packets(SpokenScene):
    def construct(self):
        guides=VGroup(*[DashedLine(hp(k*Q,0),hp(k*Q,76),color=LIGHT,stroke_opacity=.3) for k in range(4)])
        self.add(guides,histogram(4))
        labs=VGroup(label('0 packets',-3.85,2.7,RED,26))
        for k in range(1,4):
            labs.add(label(f'{k} packet'+('' if k==1 else 's'),hp(k*Q,0)[0],bump(k).get_top()[1]+.4,YELLOW,26))
        self.at('the sizes cluster'); self.play(LaggedStart(*[FadeIn(l) for l in labs],lag_ratio=.25),run_time=1.1)
        self.at('comes in packets'); self.play(Indicate(labs,scale_factor=1.03),run_time=.7); self.finish()


class S19Quantum(SpokenScene):
    def construct(self):
        self.add(quantum_view())
        self.at('Each packet'); self.play(FadeIn(label('one quantum',-3.65,3.3,YELLOW,32)),run_time=.4)
        self.at('Its effect on the muscle'); self.play(GrowArrow(arrow([.1,-2.8,0],[.65+5.25*(Q+.04)/MAXX,-1.7+3.9*max(v for _,_,v in bin_values(1))/80,0],GREEN)),run_time=.5)
        self.at('the miniature'); self.play(FadeIn(label('quantal size, q = one miniature',0,-3.15,GREEN,30)),run_time=.4); self.finish()


class S20Vesicle(SpokenScene):
    def construct(self):
        view=quantum_view(); self.add(view,label('one quantum',-3.65,3.3,YELLOW,32))
        self.at('A quantum holds'); dots=vesicle(-3.65,.25,2.4)[1]
        self.play(LaggedStart(*[FadeIn(d) for d in dots],lag_ratio=.02),run_time=.7)
        self.at('thousands of acetylcholine'); self.play(FadeIn(label('thousands of acetylcholine molecules',0,-2.95,YELLOW,28)),
            FadeIn(label('not to scale',-3.65,-2.42,LIGHT,26)),run_time=.5)
        self.at('later tied'); self.play(FadeIn(label("one quantum: one vesicle’s contents (tied later)",0,-3.5,YELLOW,28)),run_time=.5); self.finish()


class S21Notone(SpokenScene):
    def construct(self):
        self.add(quantum_view(True),label('one quantum',-3.65,3.3,YELLOW,32))
        d=Dot([-3.65,.25,0],radius=.22,color=YELLOW); self.add(d)
        self.at('It is not'); self.play(d.animate.move_to([-1.6,-2.75,0]),run_time=.3)
        self.at('one molecule'); self.play(Create(Cross(d,stroke_color=RED,scale_factor=2)),
            FadeIn(label('not one molecule',.65,-2.75,RED,32)),run_time=.35); self.finish()


class S22Coins(SpokenScene):
    def construct(self):
        self.add(jar(),label('weight: ?',-2.5,-2.15,GOLD,28))
        self.at('Think of coins'); coins=VGroup(*[Circle(radius=.28,color=GOLD,fill_color=GOLD,
            fill_opacity=1).move_to([-2.5+(i-1)*.65,3.25,0]) for i in range(3)])
        self.play(FadeIn(coins),run_time=.3)
        self.at('dropped into a jar')
        for c in coins:
            self.play(c.animate.move_to([-2.5,2.12,0]),run_time=.2); self.remove(c)
        hidden=label('coins hidden inside',3,1.3,LIGHT,29)
        self.at('You cannot see'); self.play(FadeIn(hidden),
            FadeIn(label('read the weight',3,-.1,GOLD,29)),run_time=.4)
        self.wait(max(0,self.narration_s-self.elapsed()))
        self.play(FadeOut(hidden),run_time=.2); self.finish()


class S23Count(SpokenScene):
    def construct(self):
        ref=coin_reference(); self.add(jar(),ref)
        reading=label('1 coin',-2.5,-2.15,GOLD,30)
        self.at('every reading'); self.play(FadeIn(reading),run_time=.25)
        self.at("one coin's weight"); self.play(Indicate(ref[0]),run_time=.4)
        self.play(Transform(reading,label('2 coins',-2.5,-2.15,GOLD,30)),run_time=.3); self.wait(.4)
        self.at('you can count'); self.play(Transform(reading,label('3 coins',-2.5,-2.15,GOLD,30)),run_time=.3)
        steps=VGroup(*[label(t,3,-1.1-i*.65,GOLD,28) for i,t in enumerate(['1 coin → 1 unit','2 coins → 2 units','3 coins → 3 units'])])
        self.play(FadeIn(steps),run_time=.3); self.finish(); self.wait(.8)


class S24Idea(SpokenScene):
    def construct(self):
        f=formula().set_opacity(.28); self.add(f)
        self.at('That gives'); self.play(FadeIn(label('one guiding idea',0,2.8,TEXT,34)),run_time=.4)
        self.at('Each response'); self.play(f[0][0].animate.set_opacity(1),f[0][1].animate.set_opacity(1),run_time=.3)
        self.at('the count'); self.play(f[0][2].animate.set_opacity(1),f[0][3].animate.set_opacity(1),run_time=.3)
        self.at('the size'); self.play(f[0][4].animate.set_opacity(1),run_time=.3)
        self.play(VGroup(*f[1:]).animate.set_opacity(1),run_time=.3); self.finish()


class S25Countside(SpokenScene):
    def construct(self):
        self.add(formula()); d=count_diagram()
        self.at('The nerve terminal'); self.play(FadeIn(VGroup(d[0],d[1])),run_time=.4)
        self.at('sets the count'); self.play(GrowArrow(d[2]),run_time=.3)
        self.at('Calcium sets'); self.play(FadeIn(d[3]),GrowArrow(d[4]),run_time=.4); self.finish()


class S26Sizeside(SpokenScene):
    def construct(self):
        self.add(formula(),count_diagram()); d=size_diagram()
        self.at('One'); self.play(FadeIn(d[0]),FadeIn(d[5]),run_time=.4)
        self.at('acting on the receptors'); self.play(FadeIn(d[1]),FadeIn(d[2]),run_time=.4)
        self.at('sets the size'); self.play(GrowArrow(d[3]),GrowArrow(d[4]),Create(size_sample()),run_time=.4); self.finish()


class S27Limit1(SpokenScene):
    def construct(self):
        self.add(formula(),count_diagram(),size_diagram())
        self.at('Big responses'); self.play(FadeIn(label('≈ because big responses fall short',0,-2,LIGHT,28)),run_time=.5)
        self.at('A later chapter'); self.play(FadeIn(label('(see chapter 5, the size of a packet)',0,-2.9,LIGHT,28)),run_time=.4); self.finish()


class S28Limit2(SpokenScene):
    def construct(self):
        self.add(formula(),count_diagram(),size_diagram()); row=VGroup()
        for i,n in enumerate([0,1,2,0,3,0]):
            x=-4.9+i*1.95
            b=RoundedRectangle(width=1.7,height=1.15,corner_radius=.1,color=GREY).move_to([x,-2,0])
            # Bars share a zero baseline, so their mean is a meaningful horizontal marker.
            bar=Rectangle(width=.55,height=max(.012,n*.30),color=YELLOW,fill_color=YELLOW,
                fill_opacity=.65).move_to([x,-2.5+n*.15,0])
            row.add(VGroup(b,bar,label(str(n),x,-1.2,RED if n==0 else YELLOW,26)))
        self.at('The count is random'); self.play(LaggedStart(*[FadeIn(t) for t in row],lag_ratio=.12),run_time=1.0)
        self.at('What we track'); mean=DashedLine([-5.6,-2.2,0],[5.4,-2.2,0],color=BLUE,stroke_width=3)
        self.play(Create(mean),FadeIn(label('m',6.05,-2.2,BLUE,28)),FadeIn(label('m (the average): (0+1+2+0+3+0) / 6 = 1',0,-3.05,BLUE,28)),run_time=.5); self.finish(); self.wait(.7)


class S29Takeaway(SpokenScene):
    def construct(self):
        self.add(formula())
        self.at('So when transmission'); self.play(FadeIn(label('When transmission changes, ask first:',0,2.8,TEXT,32)),run_time=.4)
        self.at('Did the count'); self.play(FadeIn(label('Did the count change, the size, or both?',0,-2,TEXT,31)),run_time=.35)
        chips=VGroup(*[chip(t,c,28).move_to([x,-3.1,0]) for t,c,x in [('count',BLUE,-2.7),('size',GREEN,0),('both',TEXT,2.7)]])
        self.play(FadeIn(chips),run_time=.35); self.finish()


class S30End(EndCard):
    LINE='Turn release down and the response shows up in whole packets.'
    def construct(self):
        self.add(label('Turn release down:',0,1.7,TEXT,40),
            label('the response shows up in whole packets.',0,.65,YELLOW,34),
            label('Did the count change, the size, or both?',0,-1.1,TEXT,30),
            label('biochemistrypedia.com',0,-2.7,TEAL,26))
        self.finish()
