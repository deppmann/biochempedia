"""Computed teaching illustrations; no experimental data.
COLOR MAP: YELLOW stimulus; GREEN neuronal output; BLUE flank/behaviour;
RED manipulation; GREY structure; TEAL graded potential; PURPLE smell.
Rate: linear interpolation of (0,50),(15,40),(30,20),(45,8), SD=5.
Histograms: integrated Gaussian bin masses. Observer: Phi(d'/sqrt(2)).
Psychometric family: .5+.5 Phi((x-threshold)/width), illustrative units.
Pooling: sqrt(N/(1+(N-1)rho)). Spike trains: seeded rate-model samples.
"""
from bp_style import *
import numpy as np
from scipy.special import ndtr
GREY = '#BEC5D1'


def label(s, x=0, y=0, c=TEXT, size=30):
    return T(s,size,c).move_to([x,y,0])


def heading(s,c=TEXT): return label(s,0,3.28,c,36)
def rate(x): return float(np.interp(x,[0,15,30,45],[50,40,20,8]))
def baseline(a,b,y): return Line([a,y,0],[b,y,0],color=GREY,stroke_width=2)
def train(xs,y,h=.45,color=GREEN):
    return VGroup(*[Line([x,y,0],[x,y+h,0],color=color,stroke_width=3) for x in xs])
def clear_to(scene,*mobs):
    scene.play(*[FadeOut(m) for m in list(scene.mobjects)],run_time=.2)
    scene.add(*mobs)


def tuning():
    ax=Axes(x_range=[0,45,15],y_range=[0,55,25],x_length=10.4,y_length=5.15,tips=False,
        axis_config={'color':GREY,'include_ticks':False}).move_to([.15,-.12,0])
    curve=VMobject(color=GREEN,stroke_width=5).set_points_as_corners([ax.c2p(x,rate(x)) for x in [0,15,30,45]])
    labs=VGroup(label('angle (degrees)',.15,-3.5,YELLOW),label('rate (spikes/s)',-3.7,2.77,GREEN))
    for x in [0,15,30,45]: labs.add(label(str(x),*(ax.c2p(x,0)+DOWN*.3)[:2]))
    for y in [0,25,50]: labs.add(label(str(y),*(ax.c2p(0,y)+LEFT*.43)[:2]))
    return VGroup(ax,curve,labs),ax


def noise(ax,x,c=GREY):
    a,b=ax.c2p(x,rate(x)-5),ax.c2p(x,rate(x)+5)
    return VGroup(Line(a,b,color=c,stroke_width=4),Line(a+LEFT*.12,a+RIGHT*.12,color=c),Line(b+LEFT*.12,b+RIGHT*.12,color=c))


def pair_marks(ax):
    groups=VGroup()
    for xs,c,name,y in [([2,6],YELLOW,'peak · 2° / 6°',2.75),([20,24],BLUE,'flank · 20° / 24°',1.25)]:
        mid=ax.c2p(np.mean(xs),rate(np.mean(xs)))
        txt=T(name,30,c).move_to([mid[0],y,0])
        groups.add(VGroup(*[Dot(ax.c2p(x,rate(x)),radius=.1,color=c) for x in xs],
            *[noise(ax,x,c) for x in xs],txt,Line(txt.get_bottom(),mid+UP*.15,color=c)))
    return groups


def prediction():
    b,ax=tuning()
    b[2][1].rotate(PI/2).move_to([-6.15,.15,0])
    return VGroup(b,pair_marks(ax),heading('Peak or flank?'),label('Both pairs 4° apart · noise SD = 5',-.6,-1.9))


def hist_pair(angles=(2,6),center=(0,-.1,0),width=10.4,height=4.7,bells=False,details=True):
    means=[rate(a) for a in angles]; lo=min(means)-15; hi=max(means)+15
    ax=Axes(x_range=[lo,hi,5],y_range=[0,.09,.03],x_length=width,y_length=height,tips=False,
        axis_config={'color':GREY,'include_ticks':False}).move_to(center)
    curves=VGroup(); ml=VGroup(); labs=VGroup()
    for mu,c in zip(means,[YELLOW,BLUE]):
        if bells:
            h=ax.plot(lambda x:np.exp(-.5*((x-mu)/5)**2)/(5*np.sqrt(2*PI)),x_range=[lo,hi,.15],color=c,stroke_width=4)
        else:
            h=VGroup()
            for a in np.arange(lo,hi,1):
                density=ndtr((a+1-mu)/5)-ndtr((a-mu)/5)
                p=ax.c2p(a+.5,density/2)
                h.add(Rectangle(width=width*.96/(hi-lo),height=max(.001,height*density/.09),
                    stroke_color=c,stroke_width=1.6,fill_color=c,fill_opacity=.025).move_to(p))
        curves.add(h); ml.add(DashedLine(ax.c2p(mu,0),ax.c2p(mu,.081),color=c))
    for x in range(int(np.ceil(lo/10)*10),int(hi)+1,10):
        labs.add(label(str(x),*(ax.c2p(x,0)+DOWN*.3)[:2],size=30))
    if details:
        # Mean labels follow separate leaders to avoid the narrow gap between means.
        for i,(mu,c) in enumerate(zip(means,[YELLOW,BLUE])):
            pos=ax.c2p(mu,.084)+np.array([1.6 if i==0 else -1.6,.28,0])
            txt=T(f'mean {mu:.1f}',30,c).move_to(pos)
            labs.add(txt,Line(txt.get_bottom(),ax.c2p(mu,.079),color=c))
    return VGroup(ax,curves,ml,labs),ax,means


def hist_legend(angles=(2,6),y=2.65):
    return VGroup(label(f'blue: {angles[1]}°',-3.2,y,BLUE),label(f'yellow: {angles[0]}°',3.2,y,YELLOW))

def sd_bar(ax,mu,y=.038,txt=True):
    bar=DoubleArrow(ax.c2p(mu-2.5,y),ax.c2p(mu+2.5,y),buff=0,color=TEXT,tip_length=.1)
    g=VGroup(bar)
    if txt:
        t=T('noise (SD) = 5',30).next_to(bar,DOWN,buff=.4)
        t.add_background_rectangle(color=BG,opacity=1,buff=.07)
        g.add(t,Line(t.get_top()+UP*.06,bar.get_center()+DOWN*.07,color=GREY))
    return g


def psych_axes(xname='stimulus difference (illustrative units)'):
    ax=Axes(x_range=[0,5,1],y_range=[.5,1,.25],x_length=10.3,y_length=4.7,tips=False,
        axis_config={'color':GREY,'include_ticks':False}).move_to([.25,0,0])
    labs=VGroup(label(xname,.3,-3.08,YELLOW),label('correct',-5.1,2.78))
    for y in [.5,.75,1]: labs.add(label(f'{int(y*100)}%',*(ax.c2p(0,y)+LEFT*.6)[:2]))
    for x in [0,1,2,3,4,5]: labs.add(label(str(x),*(ax.c2p(x,.5)+DOWN*.3)[:2]))
    return VGroup(ax,labs),ax

def curve(ax,threshold=2,width=1,c=BLUE):
    return ax.plot(lambda x:.5+.5*ndtr((x-threshold)/width),x_range=[0,5,.025],color=c,stroke_width=5)

def comparison_labels(ax):
    n=label('neuron (from spike counts)',2.2,-.95,GREEN)
    m=label('behaviour',-1.2,1.65,BLUE)
    return VGroup(n,Line(n.get_right(),ax.c2p(3.75,.5+.5*ndtr((3.75-2.42)/1.05)),color=GREEN),
        m,Line(m.get_right(),ax.c2p(2.7,.5+.5*ndtr(.7)),color=BLUE))


def monkey():
    ears=VGroup(*[Circle(.35,color=GREY,fill_color=BG,fill_opacity=1).move_to([x,0,0]) for x in [-.8,.8]])
    head=Ellipse(width=1.6,height=1.8,color=GREY,fill_color=GREY,fill_opacity=.12)
    muzzle=Ellipse(width=.8,height=.65,color=GREY).shift(DOWN*.37)
    eyes=VGroup(*[Dot([x,.3,0],radius=.06,color=TEXT) for x in [-.27,.27]])
    return VGroup(ears,head,muzzle,eyes)


def dot_field(center=(2.3,-.05,0),radius=2.3,coherence=.3):
    rng=np.random.default_rng(12); pts=[]
    while len(pts)<50:
        p=rng.uniform(-radius*.87,radius*.87,2)
        if np.linalg.norm(p)<radius*.85: pts.append(p)
    dots=VGroup(); trails=VGroup()
    for i,p in enumerate(pts):
        coherent=i<round(coherence*50); c=YELLOW if coherent else GREY
        q=np.array([*p,0])+np.array(center)
        dots.add(Dot(q,radius=.055,color=c))
        theta=0 if coherent else rng.uniform(0,2*PI)
        trails.add(Line(q-.23*np.array([np.cos(theta),np.sin(theta),0]),q,color=c,stroke_width=2))
    return VGroup(Circle(radius,color=GREY).move_to(center),dots,trails)


def move_dots(f,coherence):
    rng=np.random.default_rng(3); anim=[]
    for i,(d,t) in enumerate(zip(f[1],f[2])):
        theta=0 if i<round(coherence*50) else rng.uniform(0,2*PI)
        delta=.25*np.array([np.cos(theta),np.sin(theta),0])
        anim.extend([d.animate.shift(delta),t.animate.shift(delta)])
    return anim


def brain_diagram():
    pts=[[-5.5,-.2,0],[-5.4,.8,0],[-4.7,1.55,0],[-3.5,1.8,0],[-2.1,1.35,0],[-1.3,.5,0],[-1.6,-.3,0],[-2.3,-.9,0],[-3.2,-1.1,0],[-3.7,-.7,0],[-4.8,-.9,0],[-5.5,-.2,0]]
    outline=VMobject(color=GREY,fill_color=GREY,fill_opacity=.1).set_points_smoothly(pts)
    stem=Line([-3.5,-.9,0],[-3.2,-1.7,0],color=GREY,stroke_width=10)
    mt=Dot([-2,-.2,0],radius=.16,color=GREEN)
    electrode=Line([-1,2.3,0],mt.get_center(),color=TEXT,stroke_width=4)
    lab=VGroup(label('MT',-1.15,-1.2,GREEN),Line([-1.35,-1,0],mt.get_center(),color=GREEN))
    visual=Ellipse(width=.65,height=1.1,color=BLUE,fill_color=BLUE,fill_opacity=.25).move_to([-1.85,.45,0])
    cues=VGroup(visual,label('front',-5.2,2.15),label('back · visual',-2.85,2.15),label('monkey brain · side view',-3.4,-2.25,size=30))
    return VGroup(outline,stem,mt,electrode,lab,cues)


def neurons():
    g=VGroup()
    for k in range(12):
        x=-5.25+(k%3)*3.65; y=1.65-(k//3)*1.1
        rng=np.random.default_rng(55+k)
        ts=np.sort(rng.uniform(x+.4,x+2.5,9+k%5))
        g.add(VGroup(Circle(.23,color=GREEN,fill_color=GREEN,fill_opacity=.15).move_to([x,y,0]),train(ts,y-.15,.35)))
    return g


def pool_plot():
    ax=Axes(x_range=[1,25,6],y_range=[0,5.3,1],x_length=9.7,y_length=4.55,tips=False,
        axis_config={'color':GREY,'include_ticks':False}).move_to([.15,-.05,0])
    independent=ax.plot(lambda n:np.sqrt(n),x_range=[1,25,.1],color=GREEN,stroke_width=5)
    shared=ax.plot(lambda n:np.sqrt(n/(1+(n-1)*.35)),x_range=[1,25,.1],color=BLUE,stroke_width=5)
    monkeyline=DashedLine(ax.c2p(1,1.6),ax.c2p(25,1.6),color=YELLOW)
    labs=VGroup(label('neurons pooled',.2,-3.05),label('sensitivity / one neuron',-2.7,2.68))
    for x in [1,7,13,19,25]: labs.add(label(str(x),*(ax.c2p(x,0)+DOWN*.3)[:2]))
    for y in [0,1,3,5]: labs.add(label(str(y),*(ax.c2p(1,y)+LEFT*.4)[:2]))
    one_label=label('one neuron',-3.1,.25)
    one=VGroup(Dot(ax.c2p(1,1),color=TEXT),one_label,Line(one_label.get_left()+LEFT*.12,ax.c2p(1,1)+RIGHT*.1,color=TEXT))
    il=label('independent noise',1.2,1.8,GREEN)
    il.add(Line(il.get_right(),ax.c2p(21,np.sqrt(21)),color=GREEN))
    sl=label('shared noise',2.7,-.2,BLUE)
    sl.add(Line(sl.get_bottom(),ax.c2p(20,np.sqrt(20/(1+19*.35))),color=BLUE))
    ml=label('monkey: one neuron or a few',1.3,-1.3,YELLOW)
    return VGroup(ax,labs,one),independent,shared,monkeyline,il,sl,ml


class S00Title(TitleCard):
    TITLE='The Flank and the Monkey'
    LESSON='Principles of Sensory Coding'
    def construct(self):
        g=VGroup(label('BIOCHEMISTRYPEDIA',0,1.6,TEAL,30),label(self.LESSON,0,.8,size=32),
            T(self.TITLE,48,font=TITLE_FONT).move_to([0,-.1,0]),Line([-1.4,-.9,0],[1.4,-.9,0],color=GOLD))
        self.add(g); self.wait(3)


class S01Question(SpokenScene):
    def construct(self):
        b,ax=tuning(); self.add(b,heading('Where does a neuron discriminate best?'))
        self.at('at the peak'); p=Dot(ax.c2p(0,50),radius=.13,color=YELLOW)
        self.play(FadeIn(p),FadeIn(label('peak at 0°',-2.6,2.1,YELLOW)),run_time=.35)
        self.at('is that where'); self.play(FadeIn(label('Fires most = tells apart best?',-.7,-1.8,YELLOW,34)),run_time=.35); self.finish()


class S02Curve(SpokenScene):
    def construct(self):
        b,ax=tuning(); self.add(b,heading('Made-up neuron'))
        self.at('angle of a'); stim=VGroup(Line([-4.8,1.15,0],[-3.5,1.15,0],color=YELLOW,stroke_width=7),label('bar at 0° (stimulus)',-3.1,.65,YELLOW),DashedLine([-4.8,1.3,0],ax.c2p(0,50),color=YELLOW))
        self.play(FadeIn(stim),run_time=.35)
        self.at('its rates'); ex=VGroup()
        for x in [0,15,30,45]:
            p=ax.c2p(x,rate(x)); ex.add(Dot(p,color=GREEN),label(str(int(rate(x))),*(p+RIGHT*.38+UP*.25)[:2],c=GREEN))
        self.play(FadeOut(stim),FadeIn(ex),FadeIn(label('straight lines between points',2.1,2.05)),run_time=.4)
        self.at('each carries noise'); self.play(FadeIn(VGroup(*[noise(ax,x) for x in [0,15,30,45]])),FadeIn(label('noise: ±5 spikes/s (1 SD)',2,1.15)),run_time=.4); self.finish()


class S03Hist(SpokenScene):
    def construct(self):
        h,ax,mu=hist_pair(); self.add(h,heading('Repeated 1-second trials'),hist_legend(),label('spike count in 1 s',0,-3.13),label('probability density',-6.1,0).rotate(PI/2))
        self.at('draw a histogram'); self.play(Indicate(h[1],scale_factor=1.01),run_time=.6)
        self.at('for each'); self.play(FadeIn(sd_bar(ax,mu[0])),run_time=.35)
        self.at('overlapping histograms'); self.play(Indicate(h[1],scale_factor=1.01),run_time=.5); self.finish()


class S04Dprime(SpokenScene):
    def construct(self):
        h,ax,mu=hist_pair(); self.add(h,heading('Gap measured in noise units'),hist_legend(),label('spike count in 1 s',0,-3.1),label('probability density',-6.1,0).rotate(PI/2))
        self.at('gap between the'); gap=DoubleArrow(ax.c2p(mu[1],.069),ax.c2p(mu[0],.069),buff=0,color=TEXT,tip_length=.1)
        txt=label('gap',-3,.6); self.play(Create(gap),FadeIn(txt),Create(Line(txt.get_right(),gap.get_left(),color=TEXT)),run_time=.35)
        self.at('measured in units'); self.play(FadeIn(sd_bar(ax,mu[0])),run_time=.35)
        self.at('that gap is'); self.play(FadeIn(label('d′ = change in mean rate ÷ noise',0,-3.65,size=32)),run_time=.2); self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        b,ax=tuning(); b[2][1].rotate(PI/2).move_to([-6.15,.15,0]); marks=pair_marks(ax); self.add(b,heading('Peak or flank?'))
        self.at('near the peak'); self.play(FadeIn(marks[0]),run_time=.3)
        self.at('the steep flank'); self.play(FadeIn(marks[1]),run_time=.3)
        self.at('the same angle'); self.play(FadeIn(label('Both pairs 4° apart · noise SD = 5',-.6,-1.9)),run_time=.3); self.finish()


class S06Pause(Scene):
    def construct(self): self.camera.background_color=BG; self.add(prediction()); self.wait(5)


class S07Reveal(SpokenScene):
    def construct(self):
        panels=VGroup(); axes=[]; means=[]
        for angles,x,title,c in [((2,6),-3.25,'Peak',YELLOW),((20,24),3.25,'Flank',BLUE)]:
            h,ax,mu=hist_pair(angles,(x,.1,0),5.6,4.5,bells=True,details=False); axes.append(ax); means.append(mu)
            g=VGroup(h,label(title,x,3.25,c,36),VGroup(label(f'{angles[1]}°',x-.65,2.65,BLUE),label(f'{angles[0]}°',x+.65,2.65,YELLOW)))
            for i,(m,col) in enumerate(zip(mu,[YELLOW,BLUE])):
                pos=ax.c2p(m,.084)+np.array([.85 if i==0 else -.85,.05,0])
                t=label(f'{m:.1f}',*pos[:2],c=col)
                g.add(t,Line(t.get_bottom(),ax.c2p(m,.077),color=col))
            sd=sd_bar(ax,mu[0],.033,False); st=label('SD = 5',x-1.8,.65)
            g.add(sd,st,Line(st.get_right(),sd.get_left(),color=GREY),label('spike count in 1 s',x,-3.05))
            panels.add(g)
        self.add(panels)
        self.at('the means sit'); self.play(*[FadeIn(label(f'gap {abs(m[0]-m[1]):.1f} · d′ ≈ {abs(m[0]-m[1])/5:.1f}',x,-3.65,c)) for m,x,c in zip(means,[-3.25,3.25],[YELLOW,BLUE])],run_time=.35)
        self.at('the peak is'); self.play(ReplacementTransform(panels[0][1],label('Peak: highest rate',-3.25,3.25,YELLOW,32)),run_time=.3)
        self.at('not where it'); self.play(ReplacementTransform(panels[1][1],label('Flank: best discrimination',3.25,3.25,BLUE,28)),run_time=.3); self.finish()


class S08Psycho(SpokenScene):
    def construct(self):
        b,ax=psych_axes(); self.add(b,heading('Psychometric curve'),label('model illustration',2.8,2.78))
        self.at('has its own'); self.play(Create(curve(ax)),run_time=.6)
        self.at('guessing gives'); self.play(Create(DashedLine(ax.c2p(0,.5),ax.c2p(5,.5),color=GREY)),FadeIn(label('50%: chance',2.8,-1.85)),run_time=.35)
        self.at('a common threshold'); p=ax.c2p(2,.75)
        self.play(Create(DashedLine(ax.c2p(0,.75),p,color=YELLOW)),Create(DashedLine(p,ax.c2p(2,.5),color=YELLOW)),FadeIn(Dot(p,color=YELLOW)),FadeIn(label('75% threshold',2.4,.05,YELLOW)),FadeIn(label('threshold difference = 2',0,-3.65,YELLOW)),run_time=.5); self.finish()


class S09Assume(SpokenScene):
    def construct(self):
        h,ax,mu=hist_pair(center=(-1.5,0,0),width=7.4,height=4.6,bells=True,details=False)
        self.add(h,heading('Assumptions'),label('spike count in 1 s',-1.5,-3.2),label('bell-shaped',-1.5,2.55))
        self.add(VGroup(*[label(t,4.35,y,size=30) for t,y in [('✓ fixed window',1.7),('✓ bell-shaped',.6),('✓ independent',-.5),('✓ same SD = 5',-1.6)]])); self.finish()


class S10Bridge(SpokenScene):
    def construct(self):
        h,_,_=hist_pair(center=(-4,.35,0),width=3.4,height=3.6,bells=True,details=False)
        self.add(h,heading('For these assumptions'),label('counts: two intervals',-4,2.55))
        box=chip('Ideal observer',GREEN,32).move_to([.1,.35,0]); out=VGroup(label('% correct',4.5,.65,BLUE,36),label('50 → 100%',4.5,-.1,BLUE))
        self.at('an ideal observer'); self.play(FadeIn(box),GrowArrow(Arrow([-2.2,.35,0],[-1.6,.35,0],buff=0)),run_time=.3)
        self.at('scores'); self.play(FadeIn(out),GrowArrow(Arrow([1.85,.35,0],[3,.35,0],buff=0)),run_time=.3)
        self.at('by d prime'); self.play(FadeIn(label('proportion correct = Φ(d′ ÷ √2)',0,-2.45,size=34)),FadeIn(label('Φ: standard normal cumulative distribution',0,-3.05)),FadeIn(label('75% correct needs d′ ≈ 0.95',0,-3.65,YELLOW)),run_time=.25); self.finish()


class S11Neurometric(SpokenScene):
    def construct(self):
        b,ax=psych_axes(); self.add(b,curve(ax),heading('One scale for neuron and behaviour'),label('model illustration',0,-3.65))
        self.at('the neuron'); self.play(Create(curve(ax,2.42,1.05,GREEN)),run_time=.5)
        self.at('neurometric curve'); self.play(FadeIn(comparison_labels(ax)),run_time=.3); self.finish()


class S12Britten(SpokenScene):
    def construct(self):
        f=dot_field(); m=monkey().scale(1.25).move_to([-3.85,-.15,0])
        low=label('30% of dots move together',2.3,2.65,YELLOW)
        targets=VGroup(chip('←',YELLOW,36).move_to([-5.3,1.65,0]),chip('→',YELLOW,36).move_to([-2.4,1.65,0]))
        self.add(f,m,low,heading('Which way did it drift?'),label('Britten, Shadlen, Newsome & Movshon · 1992',0,-3.65))
        self.at('made that comparison'); self.play(*move_dots(f,.3),run_time=.65)
        self.at('rhesus monkeys'); self.play(FadeIn(targets),run_time=.3)
        high=dot_field(coherence=.9)
        self.at('judged which'); self.play(ReplacementTransform(f,high),ReplacementTransform(low,label('90% of dots move together',2.3,2.65,YELLOW)),run_time=.3)
        self.play(*move_dots(high,.9),GrowArrow(Arrow([1.4,-2.7,0],[3.2,-2.7,0],color=YELLOW)),GrowArrow(Arrow([-3.25,.65,0],[-2.55,1.25,0],color=YELLOW,buff=0)),run_time=.65); self.finish()



class S13Record(SpokenScene):
    def construct(self):
        b=brain_diagram(); f=dot_field((3.4,.4,0),2.15,1)
        self.add(b[0],b[1],b[5],f,heading('Recording during the task'))
        self.at('they recorded'); self.play(FadeIn(VGroup(b[2],b[3],b[4])),run_time=.35)
        self.at('with the display'); rf=Circle(1.55,color=BLUE).move_to([3,-.25,0])
        self.play(Create(rf),Create(DashedLine(b[2].get_center(),rf.get_left(),color=BLUE)),run_time=.3)
        self.play(f.animate.scale(1.55/2.15).move_to([3,-.25,0]),run_time=.45)
        self.add(label('receptive field',3,-2.25,BLUE),label('preferred direction',3,2.25,YELLOW),Arrow([2.2,1.65,0],[3.8,1.65,0],color=YELLOW))
        self.play(*move_dots(f,1),run_time=.4); self.finish()


class S14Result(SpokenScene):
    def construct(self):
        title=heading('Same trials, same dots'); self.add(title)
        # Seeded Gaussian count observations from the fixed-window model.
        rng=np.random.default_rng(11); counts=np.rint(rng.normal(25,5,4)).astype(int)
        rows=VGroup()
        for i,n in enumerate(counts):
            y=1.6-i*1.05; xs=np.sort(rng.uniform(-3.5,3.6,n))
            rows.add(VGroup(label(f'trial {i+1}',-5,y+.2),baseline(-3.5,3.6,y),train(xs,y),label(f'{n} spikes',5,y+.2,GREEN)))
        self.add(rows,label('spike counts in 1 s · same stimulus',0,-3.1))
        self.at('they built'); b,ax=psych_axes('motion coherence (relative units)')
        clear_to(self,b,heading('Same trials, same dots'),label('schematic comparison · not experimental data',0,-3.65))
        title=self.mobjects[-2]
        n=curve(ax,2.42,1.05,GREEN); self.play(Create(n),FadeIn(label('neuron',1.8,-.1,GREEN)),run_time=.65)
        self.at('under those conditions'); self.play(Create(curve(ax)),Create(Line([-.2,1.65,0],ax.c2p(2.7,.5+.5*ndtr(.7)),color=BLUE)),Create(Line([2.5,-.1,0],ax.c2p(3.75,.5+.5*ndtr((3.75-2.42)/1.05)),color=GREEN)),run_time=.6)
        self.play(FadeOut(title),FadeIn(heading('Neuron and monkey: similar sensitivity')),FadeIn(label('monkey',-1.3,1.65,BLUE)),run_time=.3)
        self.at('most neurons'); self.play(FadeIn(label('typical neuron: close, not identical',2,-1.65,GREEN)),run_time=.3); self.finish()


def choice_question():
    neuron=VGroup(Circle(.75,color=GREEN,fill_color=GREEN,fill_opacity=.15),train([-1,-.7,-.1,.15,.5,.65],-1.55,.55)).move_to([-3.5,.15,0])
    return VGroup(heading('Did one neuron decide?'),neuron,label('?',0,.3,YELLOW,88),monkey().scale(1.8).move_to([3.3,.2,0]),
        VGroup(chip('yes: it made the choice',TEXT,30),chip('no: it carries signal',TEXT,30)).arrange(DOWN,buff=.18).move_to([0,-2.25,0]))


class S15Predict(SpokenScene):
    def construct(self): self.add(choice_question()); self.finish()


class S16Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; prompt=label('Pause and think',0,-3.6,YELLOW,30); self.add(choice_question(),prompt)
        for _ in range(5):
            self.play(prompt.animate.set_opacity(.35),run_time=.5)
            self.play(prompt.animate.set_opacity(1),run_time=.5)


class S17Reveal(SpokenScene):
    def construct(self):
        ns=neurons().set_opacity(.4); recorded=ns[4]; recorded.set_opacity(1); recorded[0].set_stroke(YELLOW,5)
        self.add(ns,heading('One recorded neuron among many'),label('recorded neuron',-.2,2.65,YELLOW),Line([-.2,2.4,0],recorded[0].get_top(),color=YELLOW))
        self.at('it holds'); self.play(Indicate(recorded,color=YELLOW),run_time=.4)
        self.at('that is signal'); self.play(FadeIn(label('Signal, not cause.',0,-2.75,BLUE,52)),run_time=.3); self.finish()


class S18Corr(SpokenScene):
    def construct(self):
        ns=neurons(); self.add(ns,heading('Many neurons · the same dots'))
        self.at('a good readout'); clear_to(self,heading('Pool by preferred direction · then compare'))
        for x,c,direction,phase in [(-3.5,GREEN,'← preferred',0),(3.5,BLUE,'preferred →',1)]:
            self.add(label(direction,x,2.5,c))
            rng=np.random.default_rng(140+phase)
            arrays=[]
            for i,y in enumerate([1.45,.6,-.25]):
                counts=rng.poisson(1.2+.6*phase,16); arrays.append(counts)
                xs=np.concatenate([np.full(n,x-2+j*.26)+rng.uniform(0,.2,n) for j,n in enumerate(counts)])
                self.add(train(xs,y,.32,c))
            avg=np.mean(arrays,axis=0); pts=[[x-2+j*.26,-1.9+v*.23,0] for j,v in enumerate(avg)]
            self.add(Arrow([x,-.5,0],[x,-1,0],color=c),VMobject(color=c).set_points_as_corners(pts),label('averaged rate',x,-2.35,c))
        self.add(label('compare the two pooled rates',0,-3.35,size=34))
        self.at('with independent noise'); b,ind,sh,ml,il,sl,mt=pool_plot()
        clear_to(self,b,heading('Suitable readout · independent noise'),label('illustration · similarly informative neurons',0,-3.65))
        self.play(Create(ind),FadeIn(il),run_time=.8)
        self.at('the monkey shows'); self.play(Create(ml),run_time=.25); self.play(FadeIn(mt),run_time=.25); self.finish()


class S19Shared(SpokenScene):
    def construct(self):
        self.add(heading('Shared ups and downs'),label('time →',.5,-2.45,size=34))
        bands=[(-3.8,-2.3),(-.65,.85),(2.55,4.05)]; rows=VGroup()
        # Stratified samples of a piecewise rate: 8 spikes/band, 1 in each gap.
        # The shared high/low state is identical; individual event times differ.
        for k,y in enumerate([1.5,.2,-1.1]):
            rng=np.random.default_rng(90+k); xs=[]
            for a,b in bands: xs.extend(np.linspace(a+.08,b-.08,8)+rng.uniform(-.045,.045,8))
            for a,b in [(-4.5,-3.8),(-2.3,-.65),(.85,2.55),(4.05,4.6)]: xs.append(rng.uniform(a+.05,b-.05))
            rows.add(VGroup(label(f'neuron {k+1}',-5.6,y+.2),baseline(-4.5,4.6,y),train(xs,y,.6)))
        self.add(rows)
        self.at('shared noise rises'); self.play(FadeIn(VGroup(*[Rectangle(width=b-a,height=3.7,stroke_width=0,fill_color=BLUE,fill_opacity=.18).move_to([(a+b)/2,.5,0]) for a,b in bands])),run_time=.35)
        self.at('averaging cannot'); self.play(FadeIn(label('The shared part survives averaging.',0,2.6,BLUE,34)),run_time=.25)
        self.wait(.4)
        b,ind,sh,ml,il,sl,mt=pool_plot(); clear_to(self,b,heading('Illustrative model with shared noise'),label('schematic',0,-3.65))
        self.add(ind,il,ml,label('monkey',3.6,-1.45,YELLOW)); self.play(Create(sh),FadeIn(sl),run_time=.45); self.finish()


class S20Causal(SpokenScene):
    def construct(self):
        b=brain_diagram(); f=dot_field((3.5,.6,0),1.5,.3)
        self.add(b,f,heading('Microstimulation biases choices'),label('Salzman, Britten & Newsome · 1990',0,-3.65),label('dot drift →',.1,.55,YELLOW))
        self.at('microstimulating area'); tip=b[2].get_center()
        pulse=VMobject(color=RED,stroke_width=5).set_points_as_corners([tip+[-.8,.7,0],tip+[-.5,.7,0],tip+[-.5,1.1,0],tip+[-.2,1.1,0],tip+[-.2,.7,0],tip+[0,.7,0],tip])
        self.play(Create(pulse),Flash(tip,color=RED),run_time=.35)
        self.add(label('MT neurons prefer →',3.2,-1.3,GREEN))
        self.at('bias the'); self.play(*move_dots(f,.3),run_time=.3)
        # Directional illustration only: no invented numerical effect size.
        bars=VGroup(label('proportion of → choices',2.8,-1.95,size=28))
        for y,name,fraction,c in [(-2.5,'before',.5,GREY),(-3.05,'during',.7,RED)]:
            left=.9; width=4.5
            bars.add(label(name,-.05,y,c,size=28),Rectangle(width=width,height=.3,color=GREY,stroke_width=1).move_to([left+width/2,y,0]),Rectangle(width=width*fraction,height=.3,stroke_width=0,fill_color=c,fill_opacity=.85).move_to([left+width*fraction/2,y,0]))
        self.add(bars,label('schematic choice shift',-3.6,-3,RED,size=28)); self.finish()


class S21Lines(SpokenScene):
    def construct(self):
        self.add(heading('How is taste coded?'))
        # Aligned full-height comparison panels.
        self.add(RoundedRectangle(width=5.7,height=5.3,color=GREY).move_to([-3.15,-.1,0]),RoundedRectangle(width=5.7,height=5.3,color=GREY).move_to([3.15,-.1,0]))
        rng=np.random.default_rng(39); fibre=VGroup(Circle(.25,color=GREEN).move_to([-5.5,.4,0]),baseline(-5.2,-.8,.4),train(np.sort(rng.uniform(-5,-1,18)),.4,.55))
        self.add(fibre)
        self.at('by one line'); self.play(FadeIn(label('labelled line',-3.15,2.1,GREEN,34)),run_time=.25)
        self.add(label('sweet fibre',-3.15,1.25,GREEN),Arrow([-3.15,0,0],[-3.15,-.8,0],color=GREEN),label('brain reads: sweet',-3.15,-1.6,GREEN))
        self.at('a pattern across'); self.add(label('population code',3.15,2.1,BLUE,34),label('sweet        other taste',3.15,1.3))
        for i,(v,w) in enumerate(zip([.95,.25,.7,.15],[.2,.8,.3,.85])):
            y=.55-i*.58
            self.add(label(str(i+1),.9,y,size=30))
            for x,value,c in [(1.35,v,GREEN),(3.9,w,BLUE)]:
                self.add(Rectangle(width=value*1.5,height=.25,color=c,fill_color=c,fill_opacity=.7).move_to([x+value*.75,y,0]))
        self.add(label('pattern = sweet',3.15,-2.05,BLUE))
        self.at('that argument'); self.play(FadeIn(label('The argument continues.',0,-3.4,size=36)),run_time=.3); self.finish()


class S22Takeaway(SpokenScene):
    def construct(self):
        b,ax=tuning(); self.add(b)
        self.at('keep the one'); box=VGroup(RoundedRectangle(width=7.8,height=1.35,color=TEAL,fill_color=BG,fill_opacity=1).move_to([2,2.45,0]),label('rate = tuning curve(stimulus) + fluctuation',2,2.7,size=28),label('noise = SD',2,2.16,size=30))
        self.play(FadeIn(box),run_time=.3)
        self.at('a spike means'); self.play(FadeIn(VGroup(label('peak: shallow, fires most',-2.3,-.35,YELLOW),Line([-3.7,0,0],ax.c2p(4,rate(4)),color=YELLOW))),run_time=.3)
        self.at('small changes'); seg=Line(ax.c2p(15,40),ax.c2p(30,20),color=BLUE,stroke_width=8)
        dots=VGroup(*[Dot(ax.c2p(x,rate(x)),color=BLUE,radius=.12) for x in [20,24]])
        self.play(Create(seg),FadeIn(dots),FadeIn(label('flank: steep',3.4,1.15,BLUE)),run_time=.35)
        self.at('against the noise'); gap=DoubleArrow(ax.c2p(28,rate(24)),ax.c2p(28,rate(20)),buff=0,color=BLUE,tip_length=.1)
        self.play(Create(gap),FadeIn(VGroup(Line(ax.c2p(30,rate(22)-5),ax.c2p(30,rate(22)+5),color=TEXT,stroke_width=4),*[Line(ax.c2p(30,y)+LEFT*.12,ax.c2p(30,y)+RIGHT*.12,color=TEXT) for y in [rate(22)-5,rate(22)+5]])),FadeIn(label('rate gap',.95,.8,BLUE)),FadeIn(label('±5 (SD)',3.45,-.45)),Create(DashedLine(ax.c2p(20,rate(20)),ax.c2p(28,rate(20)),color=BLUE)),Create(DashedLine(ax.c2p(24,rate(24)),ax.c2p(28,rate(24)),color=BLUE)),run_time=.3)
        self.add(VGroup(label('Small angle change →',-2.1,-1.2,size=30),label('large rate change against noise',-1.7,-1.85,size=30))); self.finish()


class S23End(EndCard):
    LINE='Discrimination depends on rate change against noise, not peak firing.'
    def construct(self):
        self.add(label('Discrimination depends on',0,1,size=44),label('rate change against noise,',0,.1,BLUE,44),label('not peak firing.',0,-.8,size=44),label('biochemistrypedia.com',0,-2,TEAL,30)); self.wait(3.5)
