"""Chapter 2: A Ramp to a Bound, reviewed animation.

COLOR MAP: YELLOW = motion strength; BLUE = MT / sensory evidence;
PINK = running total / LIP firing; GOLD = bounds / model annotations;
GREEN = choice / eye movement; PURPLE = manipulation; ERROR = errors;
GREY = structure. All accumulator paths use dx=mu*dt+sqrt(SIG2*dt)*N.
mu=7.8125*coherence, SIG2=8000/log(9); latency=.200, motor=.070 s.
Mean RT=.270+a/mu*tanh(a*mu/SIG2). Near a=40, far a=50.
LIP curves are linear fit-based schematics (21.5..88.8 spikes/s/s),
not digitized recordings. Single-trial steps are explicitly schematic.
"""
import numpy as np
from bp_style import *

PINK='#E58AC0'
PURPLE='#B58CD9'
ERROR='#F5A35C'
SIG2=8000/np.log(9)
COHS=(0,3.2,6.4,12.8,25.6,51.2)


def poly(pts,color=PINK,w=4):
    return VMobject().set_points_as_corners([[x,y,0] for x,y in pts]).set_stroke(color,w).set_fill(opacity=0)


def label(s,x,y,size=28,color=TEXT):
    return T(s,size,color).move_to([x,y,0])


def head(s,color=TEXT): return label(s,0,3.42,30,color)


def axes(x0=-4.9,x1=5.65,y0=-2.85,y1=3.05):
    return VGroup(Line([x0,y0,0],[x1,y0,0],color=GREY),Line([x0,y0,0],[x0,y1,0],color=GREY))


def gx(t): return -4.9+10.55*t/2.2

def gy(v,two=True): return v/50*2.6


def graph(two=True,labels=True):
    a=axes()
    a.add(DashedLine([-4.9,0,0],[5.65,0,0],color=GREY,stroke_opacity=.5),label('start',4.9,-.3,26,GREY))
    if labels:
        a.add(label('time since dots appeared',.4,-3.47,28,GREY),label('running total',-6.05,.2,28,PINK).rotate(PI/2))
    return a


def bound(two=True,lower=False,correct=False,a=40,opacity=1):
    y=gy(-a if lower else a)
    return VGroup(Line([-4.9,y,0],[5.65,y,0],color=GOLD,stroke_width=3,stroke_opacity=opacity),
                  label('other choice' if lower else ('correct choice' if correct else 'bound'),4.35,y+(.28 if not lower else -.28),26,GOLD).set_opacity(opacity))


def smooth(mu,two=True):
    return poly([(gx(0),0),(gx(.2),0),(gx(.2+40/mu),gy(40))])


def sample(seed=1,mu=25,a=40):
    rng=np.random.RandomState(seed); t=.2; x=0.; out=[(0.,0.),(.2,0.)]
    for i in range(12000):
        nx=x+mu*.002+np.sqrt(SIG2*.002)*rng.normal(); nt=t+.002
        if abs(nx)>=a:
            target=np.sign(nx)*a
            nt=t+.002*(target-x)/(nx-x)
            out.append((nt,target)); break
        t,x=nt,nx
        if i%3==0: out.append((t,x))
    return np.array(out)


def trace(seed,mu=25,two=True,a=40,color=PINK):
    return poly([(gx(t),gy(v)) for t,v in sample(seed,mu,a) if t<=2.2],color,3)


def chosen(up=True,early=None):
    for seed in range(1,1000):
        p=sample(seed)
        if (p[-1,1]>0)==up and .35<p[-1,0]<1.7:
            if early is None or (p[-1,0]<.8)==early: return seed
    raise ValueError('No trial')

UP_E=chosen(True,True); UP_L=chosen(True,False); ERR_SEED=chosen(False)
# Same Brownian increments are replayed under both stopping rules.
def delay_seed(mu,delay):
    for seed in range(1,10000):
        n,f=sample(seed,mu,40),sample(seed,mu,50)
        if n[-1,1]>0 and f[-1,1]>0 and .32<n[-1,0]<.95 and f[-1,0]<1.4 and abs(f[-1,0]-n[-1,0]-delay)<.0005:
            return seed
    raise ValueError('No matching illustrative trial')

# Pinned seeds found by delay_seed: 230.114 ms and 24.779 ms extensions.
# The displayed traces are still integrated afresh from the model.
WEAK_DELAY=3607
STRONG_DELAY=46


def neuron(c,color=BLUE,s=1):
    c=np.array([*c,0]); g=VGroup(Circle(radius=.26*s,color=color,fill_opacity=.3).move_to(c))
    for a in (110,160,210,250):
        d=np.array([np.cos(np.radians(a)),np.sin(np.radians(a)),0])
        g.add(Line(c+d*.26*s,c+d*.78*s,color=color,stroke_width=3))
    g.add(Line(c+RIGHT*.26*s,c+RIGHT*s,color=color,stroke_width=3))
    return g


def brain(area='MT'):
    # Same large lateral silhouette and lobe boundaries in both appearances.
    outline=VMobject(color=GREY,fill_color=GREY,fill_opacity=.10)
    outline.set_points_smoothly([[-5.6,-.7,0],[-5.8,.6,0],[-5.3,1.8,0],[-4.2,2.45,0],[-2.7,2.65,0],[-1.2,2.35,0],[-.3,1.5,0],[-.1,.3,0],[-.7,-.8,0],[-2,-1.65,0],[-3.6,-1.8,0],[-5,-1.4,0],[-5.6,-.7,0]])
    sulci=VGroup(poly([(-3.5,2.3),(-3.9,1.5),(-3.45,.6)],GREY,2),poly([(-5,.2),(-3.8,.45),(-2.4,.1),(-.8,.6)],GREY,2),poly([(-1.6,2.1),(-2,1.3),(-1.7,.55)],GREY,2))
    lobes=VGroup(label('frontal',-4.7,1.15,26,GREY),label('parietal',-2.6,1.85,26,PINK if area=='LIP' else GREY),label('temporal',-3,-.95,26,GREY),label('front ←',-4.8,-2.25,26,GREY))
    loc=[-1.45,-.25,0] if area=='MT' else [-2.65,1.12,0]
    col=BLUE if area=='MT' else PINK
    spot=Ellipse(width=.9,height=.55,color=col,fill_opacity=.45).move_to(loc)
    tag=label(area,.9,2.3,36,col)
    leader=Line(spot.get_right(),tag.get_left()+LEFT*.12,color=col)
    return VGroup(outline,sulci,lobes),VGroup(spot,leader,tag)


def prediction_question(question=True):
    q=VGroup(label('What would its firing do',-.5,3.35,30),label('just before the eye moves?',-.5,2.85,30))
    ax=axes(y1=2.5)
    ax.add(label('firing rate',-6,.0,28,PINK).rotate(PI/2),label('time relative to eye movement',.2,-3.5,28,GREY),
           DashedLine([-4.9,-.65,0],[5.1,-.65,0],color=GREY,stroke_opacity=.5),label('start',-4.35,-.95,26,GREY))
    marker=VGroup(DashedLine([5.1,-2.85,0],[5.1,2.5,0],color=GREEN),label('eye movement',4.7,2.92,26,GREEN))
    return VGroup(q,ax,marker)


def prediction_lines(other=False):
    g=VGroup()
    # Response-aligned noiseless positive drifts; identical start level.
    for i,slope in enumerate((.45,.8,1.6)):
        start=4.8-2.4/slope
        xx=np.linspace(start,4.8,80)
        yy=-.65+slope*(xx-start)
        if other: yy=-.65-(.28+.11*i)*(xx-start)*slope
        g.add(poly(zip(xx,yy),BLUE if other else PINK,3 if other else 4).set_stroke(opacity=.65 if other else 1))
    return g


def dy(r): return -2.65+(r-20)/50*5.3

def dx(t,aligned=False): return -4.65+((t+.8) if aligned else t)/.8*8.65


def data_frame(aligned=False):
    g=axes(-4.65,4,-2.65,2.75)
    g.add(label('firing rate (spikes/s)',-6.1,0,26,PINK).rotate(PI/2),label('time from eye movement (ms)' if aligned else 'time from motion onset (ms)',0,-3.45,26,GREY))
    for r in (20,40,60): g.add(label(str(r),-5.05,dy(r),26,GREY))
    for t in ((-800,-600,-400,-200,0) if aligned else (0,200,400,600,800)):
        g.add(label(str(t),dx(t/1000,aligned),-3.02,26,GREY))
    g.add(head('Roitman & Shadlen, 2002 · fit-based schematic',GREY))
    return g


def data_points(c,i,aligned=False,early=False):
    slope=21.5+(88.8-21.5)*c/51.2
    base=35+(i-2.5)*.20 # tiny schematic offsets reveal the six overlapping strengths
    if aligned:
        tt=np.linspace(-min(.8,(62-base)/slope+.06),-.03,100)
        rr=62+slope*np.minimum(tt+.06,0)
    else:
        tt=np.linspace(0,.2 if early else min(.8,.2+(62-base)/slope),100)
        rr=base+slope*np.maximum(tt-.2,0)
    return np.c_[[dx(t,aligned) for t in tt],[dy(r) for r in rr]]


def data_lines(aligned=False,early=False):
    return VGroup(*[poly(data_points(c,i,aligned,early),PINK,3).set_stroke(opacity=.45+.55*i/5) for i,c in enumerate(COHS)])


def strength_labels(aligned=False):
    g=VGroup()
    if aligned:
        # Direct start labels have opaque backing so adjacent ramps stay clear.
        for i,c in enumerate(COHS):
            x,y=data_points(c,i,True)[0]
            tag=label(f'{c:g}%',x+.55,y,22,YELLOW)
            backing=Rectangle(width=tag.width+.12,height=tag.height+.08,
                              stroke_width=0,fill_color=BG,fill_opacity=1).move_to(tag)
            g.add(backing,tag,Dot([x,y,0],radius=.035,color=YELLOW))
    else:
        # Labels next to endpoints, split at their actual arrival positions.
        for i,c in enumerate(COHS):
            x,y=data_points(c,i)[-1]
            if i<4:
                dest=(5.15,-.9+i*.65)
            else: dest=(x+.15,2.38+i%2*.45)
            g.add(label(f'{c:g}%',*dest,26,YELLOW),Line([x,y,0],[dest[0]-.36,dest[1]-.12,0],color=GREY,stroke_width=1.1))
    return g


def data_caveat(): return label('averages, not single trials',.2,-2.15,28,TEXT)


def timing_table():
    g=VGroup(head('Noise changes the timing',PINK),label('invented numbers, from one model',0,2.7,28,GOLD),label('reaction time (RT)',0,2.12,28))
    xs=(-4.3,0,4.1)
    for x,s in zip(xs,('coherence','noiseless RT','noisy mean RT')): g.add(label(s,x,1.25,28,GREY))
    for y,c in zip((.3,-.85,-2),(51.2,12.8,3.2)):
        mu=7.8125*c; nl=270+40000/mu; rt=270+40000/mu*np.tanh(40*mu/SIG2)
        for x,s,col in zip(xs,(f'{c}%',f'{nl:,.0f} ms',f'≈ {round(rt/10)*10:,} ms'),(YELLOW,GREY,PINK)):
            g.add(label(s,x,y,32,col))
    g.add(RoundedRectangle(width=11.8,height=.85,corner_radius=.12,color=GOLD).move_to([0,-2,0]))
    return g


def near_far_panel(cy,mu,seed):
    # Both panels share the same 0..1400 ms time coordinate.
    pos=lambda t,v: (-4.7+7.3*t/1.4,cy+v/50*.97)
    g=VGroup(Line([-4.7,cy-1.12,0],[2.6,cy-1.12,0],color=GREY))
    for a in (-50,-40,40,50):
        y=pos(0,a)[1]
        g.add(DashedLine([-4.7,y,0],[2.6,y,0],color=GOLD,stroke_opacity=.35 if abs(a)==40 else 1))
    g.add(DashedLine([-4.7,cy,0],[2.6,cy,0],color=GREY,stroke_opacity=.4))
    for a,name in ((40,'near'),(50,'far')):
        p=sample(seed,mu,a); x,y=pos(*p[-1])
        g.add(poly([pos(t,v) for t,v in p],PINK,3).set_stroke(opacity=.45 if a==40 else 1),Dot([x,y,0],radius=.065,color=GREEN))
        # Place the two tags on opposite sides with leaders, avoiding paths.
        tx=x+(-.43 if a==40 else .5); ty=cy+(-.4 if a==40 else 1.28)
        g.add(label(name,tx,ty,26,GREEN),Line([x,y,0],[tx,ty+(-.15 if a==40 else -.18),0],color=GREEN,stroke_width=1.3))
    return g


def delay_plot():
    seed=WEAK_DELAY
    n,f=sample(seed,25,40),sample(seed,25,50)
    g=VGroup(graph(),
             Line([-4.9,gy(40),0],[5.65,gy(40),0],color=GOLD,stroke_opacity=.4),
             Line([-4.9,gy(-40),0],[5.65,gy(-40),0],color=GOLD,stroke_opacity=.4),trace(seed))
    for a in (-50,50):
        g.add(DashedLine([-4.9,gy(a),0],[5.65,gy(a),0],color=GOLD))
    g[0][3].move_to([-4.45,-.3,0])
    g.add(head('3.2% motion · bounds 40 → 50',YELLOW))
    return g,n,f


def ensemble():
    # Deliberately illustrative, matched paths: 3 errors near, 1 far.
    recovered=[]; stable=[]; wrong=[]
    for s in range(1,2000):
        n,f=sample(s),sample(s,a=50)
        if max(n[-1,0],f[-1,0])>1.75: continue
        if n[-1,1]<0<f[-1,1]: recovered.append(s)
        elif n[-1,1]>0 and f[-1,1]>0: stable.append(s)
        elif n[-1,1]<0 and f[-1,1]<0: wrong.append(s)
        if len(recovered)>=2 and len(stable)>=5 and wrong: break
    seeds=recovered[:2]+wrong[:1]+stable[:5]
    g=VGroup(head('8 illustrative weak-motion trials · invented',GOLD))
    for cx,a,title in ((-3.05,40,'near: 3 errors / 8'),(3.05,50,'far: 1 error / 8')):
        x0=cx-2.35; pos=lambda t,v: (x0+4.7*t/1.8,v/50*2.25)
        g.add(label(title,cx,2.95,28),axes(x0,cx+2.35,-2.65,2.45))
        for val in (-a,a):
            y=pos(0,val)[1]; g.add(Line([x0,y,0],[cx+2.35,y,0],color=GOLD))
        g.add(DashedLine([x0,0,0],[cx+2.35,0,0],color=GREY,stroke_opacity=.4))
        for s in seeds:
            p=sample(s,a=a); col=ERROR if p[-1,1]<0 else PINK
            g.add(poly([pos(t,v) for t,v in p],col,2),Dot([*pos(*p[-1]),0],radius=.05,color=col))
        g.add(label('time →',cx,-3,26,GREY))
    g.add(label('orange = error',0,-3.04,26,ERROR),
          label('selected examples; counts are not accuracy estimates',0,-3.55,26,GREY))
    return g


class S00Title(TitleCard):
    TITLE='A Ramp to a Bound'
    LESSON='Attention, Executive Control and Decisions'


class S01Question(SpokenScene):
    def construct(self):
        ax=axes(-4.9,5.5,-2.85,2.25)
        ax.add(label('evidence so far',-6,.0,28,PINK).rotate(PI/2),label('time',.4,-3.4,28,GREY))
        self.add(ax)
        self.at('When should a brain')
        q=VGroup(label('When should a brain stop collecting evidence',0,3.25,30),label('and commit to an answer?',0,2.7,30,GOLD))
        self.add(q)
        rng=np.random.RandomState(20); raw=rng.normal(0,.8,(6,40)); raw=np.r_[raw,-raw]
        paths=np.c_[np.zeros(12),np.cumsum(.65+raw,axis=1)]
        lines=VGroup(*[poly([(-4.9+i*.25,-2.4+v*.14) for i,v in enumerate(row)],PINK,2).set_stroke(opacity=.5) for row in paths])
        self.play(Create(lines),run_time=1.5); self.finish()


class S02Mt(SpokenScene):
    def construct(self):
        b,mt=brain(); b.shift(RIGHT*2.7)
        self.add(b,label('rhesus monkey · lateral view, schematic',0,-3.35,28,TEXT))
        self.at('evidence comes from'); self.play(b.animate.shift(LEFT*2.7),FadeIn(mt),run_time=.4)
        self.at('the middle temporal area'); self.add(label('middle temporal area',2.8,1.65,28,BLUE))
        self.at('whose neurons are tuned')
        ns=VGroup(neuron((1,.25),BLUE,.7),neuron((3.8,.25),BLUE,.7))
        curves=VGroup()
        for x,p in ((1,-.3),(3.8,.3)):
            curves.add(axes(x-.9,x+.9,.85,1.45),poly([(x+u,.86+.55*np.exp(-((u-p)/.3)**2/2)) for u in np.linspace(-.8,.8,60)],BLUE,3))
        links=VGroup(Arrow([-1.1,-.25,0],[.4,.1,0],color=BLUE,buff=.08),Arrow([1.9,.25,0],[3,.25,0],color=BLUE,buff=.08))
        self.play(FadeIn(ns),Create(curves),Create(links),run_time=.5)
        self.add(label('preferred direction →',2.5,-.8,26,BLUE))
        self.at('What adds it up')
        box=chip('adds it up?',GOLD,30).move_to([2.6,-2.5,0])
        self.play(Create(poly([(4.6,.25),(5.8,.25),(5.8,-2.5)],BLUE,3)),GrowArrow(Arrow([5.8,-2.5,0],[4.1,-2.5,0],color=BLUE,buff=.05)),FadeIn(box),run_time=.4)
        self.finish(); self.wait(1.5)


class S03Bound(SpokenScene):
    def construct(self):
        self.add(graph())
        self.at('The simplest rule'); self.play(Create(bound()),run_time=.5)
        self.at('Keep adding until'); self.play(Create(smooth(25),rate_func=linear),run_time=1.6)
        self.add(label('latency',-3.75,.42,26,GREY),Line([gx(.1),.25,0],[gx(.1),0,0],color=GREY))
        self.at('then act'); self.add(chip('act',GREEN,28).move_to([gx(1.8),1.3,0])); self.finish()


class S04Axes(SpokenScene):
    def construct(self):
        ramp=smooth(25); dot=Dot([gx(0),0,0],color=GREEN)
        self.add(graph(),bound(),ramp,label('latency',-3.75,.42,26,GREY),dot)
        self.at('Picture a graph'); self.play(MoveAlongPath(dot,ramp),run_time=1.2,rate_func=linear)
        self.at('time along the bottom'); self.play(Indicate(self.mobjects[0][-2]),run_time=.5)
        self.at('running total up'); self.play(Indicate(self.mobjects[0][-1]),run_time=.5); self.finish()


class S05Drift(SpokenScene):
    def construct(self):
        self.add(graph(),bound())
        self.at('The total drifts upward'); self.play(Create(smooth(25)),run_time=1.1)
        weak=label('weak drift',2.7,1.1,28,PINK)
        self.add(weak,Line([2.4,1.3,0],[gx(1.4),gy(30),0],color=PINK))
        self.at('Stronger motion'); self.play(Create(smooth(100)),run_time=1)
        self.add(label('strong drift',-2.9,2.75,28,PINK),Line([-2.65,2.5,0],[gx(.6),gy(40),0],color=PINK))
        self.at('reaches the bound sooner'); self.play(Flash([gx(.6),gy(40),0],color=GREEN),run_time=.5); self.finish()


class S06Wobble(SpokenScene):
    def construct(self):
        self.add(graph(),bound())
        self.at('Noise adds a wobble'); self.play(Create(trace(UP_E)),run_time=1.1)
        self.at('On some trials'); self.play(Create(trace(UP_L)),Create(trace(3)),run_time=1.2)
        self.at('and on others late')
        self.add(VGroup(*[Line([gx(sample(s)[-1,0]),-2.7,0],[gx(sample(s)[-1,0]),-2.95,0],color=GREEN,stroke_width=4) for s in (UP_E,UP_L,3)])); self.finish()


class S07TwoBounds(SpokenScene):
    def construct(self):
        self.add(graph(),bound(),trace(UP_E),trace(UP_L),trace(3))
        self.at('For a choice between two directions'); self.wait(.3)
        self.at('draw a second bound'); self.play(Create(bound(lower=True)),run_time=.8); self.finish()


class S08Error(SpokenScene):
    def construct(self):
        self.add(graph(),bound(correct=True),bound(lower=True),head('weak motion · illustrative trials',YELLOW))
        self.at('On weak motion trials')
        seeds=([s for s in range(1,100) if sample(s)[-1,1]>0 and .35<sample(s)[-1,0]<1.9][:4] + [s for s in range(1,100) if sample(s)[-1,1]<0 and .35<sample(s)[-1,0]<1.9][:2])
        paths=VGroup(*[trace(s) for s in seeds]); self.play(Create(paths),run_time=1.2)
        self.at('the wobble sometimes'); self.wait(.3)
        self.at('That is an error')
        self.play(*[paths[i].animate.set_color(ERROR) for i in (4,5)],Flash(paths[4].get_end(),color=ERROR),FadeIn(label('error',2,-1.45,32,ERROR)),run_time=.35)
        self.wait(3.1); self.finish()


class S09Name(SpokenScene):
    def construct(self):
        self.at('This is a')
        self.add(head('drift-to-bound model',GOLD),label('Without noise',0,2.35,30,GREY))
        eq1=label('time to bound = (bound − start) ÷ drift',0,1.25,32)
        eq2=VGroup(label('reaction time = latency + time to bound',0,-.05,30),label('+ motor delay',0,-.6,30))
        defs=VGroup(label('latency: before accumulation begins',0,-1.8,28,GREY),label('motor delay: bound reached → eye movement',0,-2.65,28,GREY))
        self.play(FadeIn(eq1),run_time=.5); self.wait(1.5)
        self.play(FadeIn(eq2),run_time=.5); self.play(FadeIn(defs),run_time=.4)
        self.wait(8); self.finish()


class S10Question(SpokenScene):
    def construct(self):
        g=prediction_question(); self.add(g)
        n=neuron((-3.6,1.55),PINK,.7)
        self.at('Suppose some neuron'); self.play(FadeIn(n),run_time=.4)
        self.at('What would its firing')
        self.play(FadeOut(n),run_time=.3)
        ring=Circle(radius=.35,color=GOLD).move_to([-.2,1,0]); self.play(Create(ring),run_time=.5); self.finish()


class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction_question())
        ring=Circle(radius=.42,color=GREY).move_to([0,1,0]); arc=Arc(radius=.42,start_angle=PI/2,angle=-TAU,color=GOLD,stroke_width=5).move_to([0,1,0])
        self.add(ring,arc,label('predict',0,.15,26,GOLD)); self.play(Uncreate(arc),run_time=5,rate_func=linear)


class S12Reveal(SpokenScene):
    def construct(self):
        g=prediction_question(); self.add(*g[1:])
        self.add(head('aligned to the eye movement',GREY))
        self.at('trials choosing the target'); self.add(label('choice toward response-field target',-.5,2.60,28,PINK))
        lines=prediction_lines()
        self.at('it should climb'); self.play(Create(lines[0]),run_time=.7)
        self.at('more steeply when'); self.play(Create(lines[1]),Create(lines[2]),run_time=.8)
        for txt,slope in zip(('weak','medium','strong'),(.45,.8,1.6)):
            x=4.8-2.4/slope
            self.add(label(txt,x-.45,-.18,26,PINK),Line([x,-.38,0],[x,-.60,0],color=PINK,stroke_width=1.2))
        self.at('about the same level')
        self.add(DashedLine([-4.9,1.75,0],[4.8,1.75,0],color=GOLD),label('about the same level',-.7,2.08,26,GOLD))
        self.at('The other choice'); self.play(Create(prediction_lines(True)),run_time=.7)
        self.add(label('other choice: different endpoints',.8,-2.45,26,BLUE)); self.finish()


class S13Lip(SpokenScene):
    def construct(self):
        b,lip=brain('LIP'); b.shift(RIGHT*2.7)
        self.add(b,head('Roitman & Shadlen · 2002'),
                 label('rhesus monkey · lateral view, schematic',0,-3.35,28,TEXT))
        self.at('Now the data'); self.wait(.2)
        self.at('recorded from the'); self.play(b.animate.shift(LEFT*2.7),FadeIn(lip),run_time=.5)
        self.add(label('lateral intraparietal',2.75,1.2,30,PINK),label('area',2.75,.62,30,PINK))
        self.at('in rhesus monkeys'); self.finish()


class S14Field(SpokenScene):
    def construct(self):
        n=neuron((-4.6,2.15),PINK,1.2)
        patch=Ellipse(width=3,height=3.4,color=PINK,fill_opacity=.12).move_to([3.9,-.8,0])
        targets=VGroup(Dot([-3.8,-.8,0],radius=.18,color=GREY),Dot([3.9,-.8,0],radius=.18,color=GREEN),Dot([0,-.8,0],radius=.09,color=TEXT))
        self.add(n,patch,targets,label('LIP neuron',-3,3.1,30,PINK),label('fixation',0,-1.4,28),label('target',-3.8,-1.4,28,GREY),label('target',3.9,-1.4,28,GREEN))
        self.at('Its neurons fire before')
        spikes=VGroup(*[Line([x,1.5,0],[x,2.25,0],color=PINK,stroke_width=4) for x in np.linspace(-.8,4.8,9)])
        self.play(GrowArrow(Arrow([-3.3,2.15,0],[-1.2,2.15,0],color=PINK,buff=.05)),Create(spikes),run_time=.5)
        self.add(label('spikes',2,2.85,28,PINK))
        self.at('an eye movement'); self.play(GrowArrow(Arrow([.2,-.8,0],[3.6,-.8,0],color=GREEN)),run_time=.45)
        self.at('in their response field'); self.add(label('response field',3.65,-2.85,30,PINK)); self.finish(); self.wait(1.6)


class S15Together(SpokenScene):
    def construct(self):
        self.add(data_frame(),data_lines(early=True))
        self.at('Averaged over many trials'); self.add(data_caveat())
        self.at('the lines lie together'); self.add(label('six motion strengths, overlapping',.6,2.6,28,PINK))
        self.at('for the first')
        self.add(Rectangle(width=2.16,height=5.3,stroke_width=0,fill_color=GREY,fill_opacity=.1).move_to([-3.57,0,0]),label('≈ 200 ms',-3.5,1.8,28,GREY)); self.finish()


class S16Ramp(SpokenScene):
    def construct(self):
        early=data_lines(early=True); self.add(data_frame(),early,data_caveat())
        self.at('Then they ramp'); self.play(Transform(early,data_lines()),run_time=1)
        self.at('The ramp is steeper'); self.add(strength_labels())
        self.at('when the monkey chose'); self.add(label('choice toward response-field target',.1,-1.5,28,GREEN)); self.finish()


class S17Level(SpokenScene):
    def construct(self):
        frame=data_frame(); lines=data_lines(); self.add(frame,lines,data_caveat())
        self.at('Lined up to the eye movement'); self.play(Transform(frame,data_frame(True)),Transform(lines,data_lines(True)),run_time=1)
        self.add(strength_labels(True),label('choice toward response-field target',.1,-1.80,26,GREEN))
        self.at('the firing reaches'); self.add(DashedLine([4,-2.65,0],[4,2.75,0],color=GREEN),label('eye movement',2.6,2.85,26,GREEN))
        self.at('about the same rate'); self.add(DashedLine([-4.65,dy(62),0],[4,dy(62),0],color=GOLD))
        self.at('The authors read this'); self.add(label('apparent threshold',-2,dy(62)+.28,28,GOLD)); self.finish(); self.wait(1.5)


class S18Averages(SpokenScene):
    def construct(self):
        self.add(head('One way an average ramp can arise (schematic)',GOLD))
        times=np.linspace(0,1,1001); thresholds=(.15,.38,.61,.84)
        self.add(label('4 example single trials',-3.25,2.55,28,PINK),label('many-trial average',3.25,2.55,30,PINK))
        for i,t in enumerate(thresholds):
            y=1.4-i*1.05
            self.add(poly([(-5.6,y),(-5.6+4.7*t,y),(-5.6+4.7*t,y+.55),(-.9,y+.55)],PINK,3))
        # An ensemble of steps at uniformly distributed times has E[H(t-U)]=t.
        avg=np.mean(times[:,None]>=np.linspace(0,1,1000)[None,:],axis=1)
        self.add(axes(1,5.7,-2.5,1.9),poly([(1+4.7*t,-2.1+3.7*v) for t,v in zip(times,avg)],PINK,4),label('time →',3.3,-3.05,28,GREY),label('time →',-3.2,-3.05,28,GREY))
        self.at('These are averages'); self.wait(.2)
        self.at('Single trials may look different'); self.add(label('Single trials may look different · see Going deeper',0,-3.58,26)); self.finish(); self.wait(2)


class S19Noise(SpokenScene):
    def construct(self):
        self.at('Noise also changes the timing'); self.add(timing_table())
        self.at('At weak motion'); self.play(Indicate(self.mobjects[0][-1]),run_time=.5)
        self.at('the wobble carries many trials'); self.wait(.2)
        self.at('sometimes the wrong one'); self.add(label('early arrivals can include errors',0,-3.15,28,ERROR)); self.finish()


class S20Noise2(SpokenScene):
    def construct(self):
        # Retain the highlighted weak row beside a full-height plot.
        table=VGroup(label('3.2% coherence',-4.65,2.4,28,YELLOW),label('reaction time (RT)',-4.65,1.65,26),label('noiseless: 1,870 ms',-4.65,.85,26,GREY),label('noisy: ≈ 700 ms',-4.65,.05,26,PINK),label('invented numbers',-4.65,-1.05,24,GOLD))
        table.add(RoundedRectangle(width=3.95,height=4.7,corner_radius=.12,color=GOLD).move_to([-4.65,.7,0]))
        self.add(table)
        pos=lambda t,v: (-1.9+7.5*t/2.2,v/50*2.6)
        plot=axes(-1.9,5.6,-2.85,3.05)
        for a,txt in ((40,'correct'),(-40,'other choice')):
            y=pos(0,a)[1]; plot.add(Line([-1.9,y,0],[5.6,y,0],color=GOLD),label(txt,4.3,y+(.28 if a>0 else -.28),26,GOLD))
        plot.add(DashedLine([-1.9,0,0],[5.6,0,0],color=GREY),label('start',4.9,-.3,26,GREY),label('relative total',-2.55,.2,26,PINK).rotate(PI/2),label('time since motion onset',1.8,-3.45,26,GREY))
        self.add(plot)
        self.at('With two bounds'); self.wait(.2)
        self.at('you never wait forever')
        for s in (UP_E,UP_L,ERR_SEED):
            p=sample(s); self.add(poly([pos(t,v) for t,v in p],ERROR if p[-1,1]<0 else PINK,3))
        error_end=pos(*sample(ERR_SEED)[-1])
        self.add(label('error',error_end[0]+.65,error_end[1]+.25,28,ERROR))
        self.at('So mean times are shorter'); self.play(Indicate(table),run_time=.5); self.finish()


class S21Raise(SpokenScene):
    def construct(self):
        g,n,f=delay_plot(); g[0].remove(g[0][-2]); far=VGroup(*list(g)[4:6]); moving=VGroup(*[Line([-4.9,gy(a),0],[5.65,gy(a),0],color=GOLD) for a in (-40,40)])
        self.add(*list(g)[:4],g[-1],moving)
        self.at('Now move both bounds'); self.play(Transform(moving,far),run_time=.7)
        self.add(label('correct choice',4.25,gy(50)+.26,26,GOLD),
                 label('other choice',4.35,gy(-50)+.27,26,GOLD),
                 label('near bound (40)',-3.25,gy(40)-.28,24,TEXT),
                 label('far bound (50)',-3.25,gy(50)+.26,24,GOLD))
        self.at('Choices get slower'); self.play(Create(trace(WEAK_DELAY,a=50)),run_time=.7)
        x1,x2=gx(n[-1,0]),gx(f[-1,0])
        marks=VGroup()
        for x,txt in ((x1,'near'),(x2,'far')):
            arrival=n[-1,0] if txt=='near' else f[-1,0]
            marks.add(DashedLine([x,-2.85,0],[x,gy(40 if txt=='near' else 50),0],color=GREEN,stroke_opacity=.5),Dot([x,-2.85,0],radius=.06,color=GREEN),label(f'{txt} {arrival*1000:.0f} ms',x+(-.65 if txt=='near' else .65),-2.35,26,GREEN))
        marks.add(Line([x1,-3.05,0],[x2,-3.05,0],color=GREEN),Line([x1,-2.9,0],[x1,-3.13,0],color=GREEN),Line([x2,-2.9,0],[x2,-3.13,0],color=GREEN),label('+230 ms', (x1+x2)/2,-3.48,30,GREEN))
        self.add(label('time (ms)',3.9,-3.48,28,GREY))
        self.add(marks); self.wait(2.8)
        self.at('and more accurate')
        self.clear()
        self.play(FadeIn(ensemble()),run_time=.5); self.finish(); self.wait(3)


class S22Weak(SpokenScene):
    def construct(self):
        self.add(head('Near bounds: faint · farther bounds: bright',GOLD))
        self.add(near_far_panel(1.22,400,STRONG_DELAY),near_far_panel(-1.45,25,WEAK_DELAY))
        for cy,c,mu in ((1.22,51.2,400),(-1.45,3.2,25)):
            n=270+40000/mu*np.tanh(40*mu/SIG2); f=270+50000/mu*np.tanh(50*mu/SIG2)
            self.add(label(f'{c}% motion',4.7,cy+1,28,YELLOW),label('mean reaction time',4.7,cy+.45,26),label(f'{n:.0f} → {f:.0f} ms',4.7,cy-.12,28,GREEN),label(f'+{round((f-n)/5)*5:.0f} ms',4.7,cy-.72,30,GREEN))
        for t in (0,400,800,1200):
            x=-4.7+7.3*(t/1000)/1.4
            self.add(label(str(t),x,-2.92,26,GREY))
        self.add(label('time since motion onset (ms)',-.9,-3.4,26,GREY),label('invented numbers, same model as the table',0,3.02,26,GOLD))
        self.at('The slowing is biggest'); self.wait(.15)
        self.at('at weak motion'); self.play(Indicate(self.mobjects[2]),run_time=.6)
        self.at('sets the time to the bound'); self.finish(); self.wait(2)


class S23Takeaway(SpokenScene):
    def construct(self):
        g,n,f=delay_plot(); self.add(g)
        self.at('A decision can be'); self.play(Create(trace(WEAK_DELAY,a=50)),run_time=1)
        self.at('that stops at a bound')
        self.add(label('near: fast, more errors',2.3,.85,28,TEXT),
                 label('far: slow, fewer errors',2.3,-.65,28,TEXT))
        # Each label connects to both bounds in its own stopping rule.
        for a in (-40,40):
            self.add(Line([4.55,.85,0],[5.25,gy(a),0],color=GOLD,stroke_width=2),
                     Dot([5.25,gy(a),0],radius=.055,color=GOLD))
        for a in (-50,50):
            self.add(Line([.15,-.65,0],[-.35,gy(a),0],color=GOLD,stroke_width=2),
                     Dot([-.35,gy(a),0],radius=.055,color=GOLD))
        self.at('The bound sets the trade')
        card=chip('speed ↔ accuracy',GREEN,32).move_to([-2.8,-1.4,0])
        self.play(FadeIn(card),run_time=.5); self.finish()


class S24End(EndCard):
    LINE='The bound helps set the trade between speed and accuracy.'
