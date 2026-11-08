"""Adding Up Noisy Evidence — chapter 1.
COLOR MAP: YELLOW coherent motion / signal; BLUE evidence pooling;
PINK LIP / parietal firing; GOLD bounds / annotations; GREEN choices;
PURPLE manipulation; RED impairment; GREY random motion / structure.
All curves are model calculations, not recorded data. Behaviour uses the
lesson's symmetric DDM: a=40, mu=7.8125*c, sigma²=8000/log(9).
Tally: independent N(.65,.8²) increments, mean=.65n, SD=.8sqrt(n).
"""
import numpy as np
from bp_style import *
PINK = '#E58AC0'
PURPLE = '#B58CD9'


def poly(pts, color=GREY, w=4):
    return VMobject().set_points_as_corners([np.array([x,y,0.]) for x,y in pts]).set_stroke(color,w).set_fill(opacity=0)


def label(s,x,y,size=28,color=TEXT):
    return T(s,size,color).move_to([x,y,0])


def axes(x0,x1,y0,y1):
    return VGroup(Line([x0,y0,0],[x1,y0,0],color=GREY),Line([x0,y0,0],[x0,y1,0],color=GREY))


def arrow(a,b,color=YELLOW):
    return Arrow([*a,0],[*b,0],buff=0,color=color,stroke_width=4,tip_length=.14)


def dotfield(coh=.032, white=False):
    # Identical 70%-height aperture and position in every dot scene.
    cx,cy,w,h,n=-2.,0.,7.,5.6,94
    rng=np.random.RandomState(3)
    box=Rectangle(width=w,height=h,color=GREY,stroke_width=2).move_to([cx,cy,0])
    dots=VGroup(); velocities=[]
    for i in range(n):
        a=0 if i<round(coh*n) else rng.uniform(0,TAU)
        d=Dot([cx+rng.uniform(-w/2+.2,w/2-.2),rng.uniform(-h/2+.2,h/2-.2),0],radius=.055,
              color=TEXT if white else (YELLOW if i<round(coh*n) else GREY))
        dots.add(d); velocities.append(.7*np.array([np.cos(a),np.sin(a),0]))
    def update(m,dt):
        for d,v in zip(m,velocities):
            d.shift(v*dt); p=d.get_center()
            if p[0]>cx+w/2-.1: d.shift(LEFT*(w-.2))
            if p[0]<cx-w/2+.1: d.shift(RIGHT*(w-.2))
            if p[1]>h/2-.1: d.shift(DOWN*(h-.2))
            if p[1]<-h/2+.1: d.shift(UP*(h-.2))
    dots.add_updater(update)
    g=VGroup(box,dots); g.velocities=velocities
    return g


def motion_key(white=False):
    return VGroup(arrow((2.3,1.4),(4.7,1.4),TEXT if white else YELLOW),
                  label('coherent motion',3.8,2.,26,TEXT if white else YELLOW))


def slider(value=3.2):
    x=lambda v:-4.8+5.6*(v-3.2)/48
    return VGroup(Line([-4.8,-3.15,0],[.8,-3.15,0],color=GREY),
                  Dot([x(value),-3.15,0],radius=.12,color=YELLOW),
                  label('3.2%',-4.8,-3.6,26,YELLOW),label('51.2%',.8,-3.6,26,YELLOW),
                  label(f'{value:.1f}%',3.8,-2.5,34,YELLOW))


def behavior():
    c=np.linspace(0,51.2,240); mu=7.8125*c; a=40; sig2=8000/np.log(9)
    p=1/(1+np.exp(-2*mu*a/sig2))
    rt=np.empty_like(mu); rt[0]=.270+a*a/sig2
    rt[1:]=.270+a/mu[1:]*np.tanh(a*mu[1:]/sig2)
    panels=[]
    for x0,x1,title,vals,lo,hi in [(-5.,-.8,'accuracy (% correct)',p,.5,1.),(1.8,6.,'reaction time (ms)',rt,.3,.75)]:
        y0,y1=-2.8,2.8
        ax=axes(x0,x1,y0,y1)
        curve=poly([(x0+(x1-x0)*cc/51.2,y0+(v-lo)/(hi-lo)*(y1-y0)) for cc,v in zip(c,vals)],GREEN,6)
        texts=VGroup(label(title,(x0+x1)/2,3.3,28,GREEN),label('coherence (%)',(x0+x1)/2,-3.6,26,GREY),
                      label('0%',x0,-3.15,26,GREY),label('51.2%',x1,-3.15,26,GREY))
        ticks=VGroup(*[label(s,x0-.6,y,26,GREY) for s,y in zip(('50','100') if lo==.5 else ('300','750'),(y0,y1))])
        panels.append(VGroup(ax,curve,texts,ticks))
    return VGroup(*panels)


FX=lambda n:-4.9+8.4*n/40
FY=lambda v:-2.1+.12*v


def bracket(x,lo,hi,color=GREY):
    return VGroup(Line([x,lo,0],[x,hi,0],color=color,stroke_width=4),
                  Line([x-.12,lo,0],[x+.12,lo,0],color=color),Line([x-.12,hi,0],[x+.12,hi,0],color=color))


def fan():
    rng=np.random.RandomState(20)
    # Independent traces: do not manufacture cancellation by pairing opposite noise.
    paths=np.c_[np.zeros(12),np.cumsum(rng.normal(.65,.8,(12,40)),axis=1)]
    traces=VGroup(*[poly([(FX(i),FY(v)) for i,v in enumerate(row)],GREY,1.8).set_stroke(opacity=.55) for row in paths])
    mean=poly([(FX(i),FY(.65*i)) for i in range(41)],YELLOW,6)
    n=np.linspace(0,40,200)
    band=Polygon(*[np.array([FX(v),FY(.65*v+.8*np.sqrt(v)),0]) for v in n],
                 *[np.array([FX(v),FY(.65*v-.8*np.sqrt(v)),0]) for v in n[::-1]],stroke_width=0,fill_color=GREY,fill_opacity=.12)
    labs=VGroup(label('samples added',-.7,-2.95,28,GREY),label('running total',-3.7,3.15,28,GREY))
    return VGroup(axes(-4.9,3.5,-2.1,2.6),traces,mean,labs,band)


def spreads():
    return VGroup(*[bracket(FX(n),FY(.65*n-.8*np.sqrt(n)),FY(.65*n+.8*np.sqrt(n))) for n in (10,40)])


def question():
    return VGroup(label('Watch 4 times as long.',0,1.65,40),
                  label('Is the total 4 times as reliable?',0,.45,36,GOLD),
                  label('reliable = signal ÷ noise',0,-.75,30,YELLOW))


class S00Title(TitleCard):
    LESSON='Attention, Executive Control and Decisions'
    TITLE='Adding Up Noisy Evidence'


class S01Question(SpokenScene):
    def construct(self):
        f=dotfield(coh=.128,white=True)
        self.add(f,label('How does noise become a choice?',0,3.3,32,GOLD))
        self.at('A monkey watches'); self.finish()


class S02Coherence(SpokenScene):
    def construct(self):
        f=dotfield(coh=.512); key=motion_key(); s=slider(51.2)
        self.add(f,key,s,label('coherence = % moving together',0,3.3,30,YELLOW),
                 label('Gold: viewer guide only',3.8,-.2,26,GREY),label('Monkey sees no colours',3.8,-.7,26,GREY))
        self.at('Some dots move together'); self.play(Indicate(key,scale_factor=1.05),run_time=.4)
        self.at('The share moving together')
        v=ValueTracker(51.2)
        read=always_redraw(lambda: label(f'{v.get_value():.1f}%',3.8,-2.5,34,YELLOW))
        self.remove(s[4]); self.add(read)
        # Readout, slider and gold-dot count follow the same coherence value.
        angles=np.random.RandomState(81).uniform(0,TAU,len(f[1]))
        def tint(m):
            for i,d in enumerate(m):
                coherent=i<round(v.get_value()/100*len(m))
                d.set_color(YELLOW if coherent else GREY)
                a=0 if coherent else angles[i]
                f.velocities[i]=.7*np.array([np.cos(a),np.sin(a),0])
        f[1].add_updater(tint)
        self.play(v.animate.set_value(3.2),s[1].animate.move_to([-4.8,-3.15,0]),run_time=1.1)
        self.at('is called coherence'); self.finish()


class S03Answer(SpokenScene):
    def construct(self):
        f=dotfield(); self.add(f,slider(),motion_key(),label('Choose a target',0,3.3,32,GREEN))
        targets=VGroup(Dot([-6.1,0,0],radius=.15,color=GREEN),Dot([6.,0,0],radius=.15,color=GREEN))
        eye=Ellipse(width=2.,height=.9,color=GREEN).move_to([3.7,-.6,0])
        pupil=Dot([3.7,-.6,0],radius=.2,color=GREEN)
        self.at('The monkey answers'); self.play(FadeIn(targets),FadeIn(eye),FadeIn(pupil),run_time=.3)
        self.at('quick eye movement'); self.play(pupil.animate.shift(RIGHT*.55),run_time=.15)
        self.play(FadeIn(label('saccade',3.8,-1.5,30,GREEN)),run_time=.2)
        self.at('one of two targets'); self.play(Indicate(targets[1],scale_factor=1.6),run_time=.4); self.finish()


class S04Curves(SpokenScene):
    def construct(self):
        g=behavior()
        self.at('Stronger motion gives')
        self.play(FadeIn(g[1][0]),FadeIn(g[1][2]),FadeIn(g[1][3]),run_time=.25)
        self.at('faster and'); self.play(Create(g[1][1]),run_time=.45)
        self.at('more accurate choices'); self.play(FadeIn(g[0][0]),FadeIn(g[0][2]),FadeIn(g[0][3]),Create(g[0][1]),run_time=.55)
        self.at('With no net motion')
        chance=VGroup(Dot([-5,-2.8,0],color=GOLD),Line([-5,-2.8,0],[-4.1,-1.1,0],color=GOLD),label('chance',-3.35,-.85,28,GOLD))
        self.play(FadeIn(chance),run_time=.3); self.finish()


class S05Neuron(SpokenScene):
    def construct(self):
        # Lateral schematic: frontal pole left, occipital pole right, cerebellum below.
        outline=poly([(-5.9,-.4),(-6, .7),(-5.6,1.65),(-4.8,2.25),(-3.6,2.5),(-2.4,2.2),(-1.7,1.4),(-1.65,.4),(-2.2,-.35),(-3.,-.6),(-3.7,-1.1),(-4.8,-.9),(-5.9,-.4)],GREY,4)
        outline.set_points_smoothly([np.array([x,y,0.]) for x,y in [(-5.9,-.4),(-6,.7),(-5.6,1.65),(-4.8,2.25),(-3.6,2.5),(-2.4,2.2),(-1.7,1.4),(-1.65,.4),(-2.2,-.35),(-3.,-.6),(-3.7,-1.1),(-4.8,-.9),(-5.9,-.4)]])
        cb=Ellipse(width=1.5,height=1.1,color=GREY,fill_opacity=.15).move_to([-2.5,-.9,0])
        folds=VGroup(*[Arc(radius=.5,start_angle=.1,angle=2.5,color=GREY).stretch(.5,1).move_to([-2.75+i*.3,-.9,0]) for i in range(3)])
        sulci=VGroup(poly([(-4.1,2.25),(-4.3,1.6),(-3.95,.8)],GREY,2),poly([(-2.5,1.9),(-2.9,1.2),(-2.5,.4)],GREY,2),poly([(-5.5,.25),(-4.5,.45),(-3.6,.2)],GREY,2))
        patch=Ellipse(width=1.,height=.65,color=PINK,fill_opacity=.4).move_to([-2.95,1.6,0])
        lobes=VGroup(label('frontal',-5.1,1.05,22,GREY),label('parietal',-3.25,2.35,22,GREY),label('occipital',-2.35,.1,22,GREY))
        self.add(outline,cb,folds,sulci,lobes,label('monkey brain · side view',-3.8,-1.95,26,GREY))
        self.at('Meanwhile')
        ax=axes(1.3,6.2,-1.9,1.95)
        labs=VGroup(label('firing rate (spikes/s)',.1,.1,26,PINK).rotate(PI/2),label('average of many trials',3.75,2.65,26,PINK),label('time (s)',3.75,-2.9,28,GREY),
                    label('30',.8,-1.4,26,GREY),label('65',.8,1.6,26,GREY),label('0',1.3,-2.3,26,GREY),label('1.6',6.2,-2.3,26,GREY))
        self.at('averaged over many trials'); self.play(FadeIn(ax),FadeIn(labs),run_time=.3)
        self.at('parietal cortex')
        lip=VGroup(label('LIP · parietal',-1.8,3.25,28,PINK),Line([-1.8,2.9,0],[-2.75,1.9,0],color=PINK),Line([-2.45,1.6,0],[1.3,1.95,0],color=PINK,stroke_width=2))
        self.play(FadeIn(patch),FadeIn(lip),run_time=.3)
        self.at('fires faster and faster')
        ramp=poly([(1.3+4.9*t/1.6,-1.4+(25*max(0,t-.2))*3/35) for t in np.linspace(0,1.6,120)],PINK,6)
        onset=VGroup(Line([1.3,-1.9,0],[1.3,-2.05,0],color=GOLD),label('motion onset',1.5,-3.4,26,GOLD),Line([1.5,-3.1,0],[1.3,-2.5,0],color=GOLD))
        self.play(Create(ramp),FadeIn(onset),run_time=.7)
        self.at('Is it making'); self.play(FadeIn(label('Is this neuron deciding?',-2.6,-2.7,30,GOLD)),run_time=.3); self.finish()


class S06Glimpse(SpokenScene):
    def construct(self):
        f=dotfield(); self.add(f,label('One glimpse: 3.2% coherence',0,3.3,32,YELLOW),label('Gold: viewer guide only',3.8,-2.5,26,GREY),label('Monkey sees no colours',3.8,-3.,26,GREY))
        self.at('Any single moment'); self.wait(.25); f[1].clear_updaters()
        trails=VGroup(*[Line(d.get_center()-v*.3,d.get_center(),color=d.get_color(),stroke_width=2) for d,v in zip(f[1],f.velocities)])
        self.play(Create(trails),run_time=.25)
        self.at('a weak hint')
        # Unequal arrows at scattered positions: no symmetric compass glyph.
        rng=np.random.RandomState(61)
        directions=VGroup()
        for x,y in ((2.7,1.1),(4.15,.9),(5.1,.7),(2.65,-.05),(4.2,-.15),(5.2,-.45)):
            a=rng.uniform(0,TAU); length=rng.uniform(.65,1.1)
            directions.add(arrow((x,y),(x+length*np.cos(a),y+length*np.sin(a)),GREY))
        self.play(GrowArrow(arrow((2.8,2.2),(3.2,2.2))),FadeIn(label('signal',4.25,2.2,28,YELLOW)),
                  FadeIn(directions),FadeIn(label('noise',3.8,-1.35,30,GREY)),run_time=.35)
        self.at('buried in noise'); self.finish()


class S07Tally(SpokenScene):
    def construct(self):
        f=dotfield(); self.add(f,label('Add each glimpse',0,3.3,32,YELLOW),motion_key())
        x=3.9; rail=Line([2.,-.4,0],[5.8,-.4,0],color=GREY)
        ticks=VGroup(*[Line([v,-.52,0],[v,-.28,0],color=GREY) for v in np.linspace(2.,5.8,9)])
        texts=VGroup(label('left',2.,-1.,28,GREY),label('right',5.6,-1.,28,GREY),label('0',x,-1.,26,GREY),label('running total',3.9,-2.15,30,YELLOW))
        marker=Triangle(color=YELLOW,fill_opacity=1).scale(.12).rotate(PI).move_to([x,.05,0])
        self.at('keep a running total'); self.play(Create(rail),FadeIn(ticks),FadeIn(texts),FadeIn(marker),run_time=.3)
        self.at('Count each glimpse')
        # Seven Gaussian glimpses: two left steps and five right, with a net drift.
        for dx in np.random.RandomState(55).normal(.65,.8,7)*.45:
            nx=x+dx; step=Line([x,-.4,0],[nx,-.4,0],color=YELLOW,stroke_width=6)
            tick=Line([nx,-.62,0],[nx,-.18,0],color=YELLOW)
            self.play(Create(step),Create(tick),marker.animate.move_to([nx,.05,0]),run_time=.22); x=nx
        self.finish()


class S08Cancel(SpokenScene):
    def construct(self):
        g=fan(); self.add(g[0],g[3])
        self.at('Hints toward the true direction')
        self.play(Create(g[2]),FadeIn(label('mean signal',4.95,.55,28,YELLOW)),run_time=.8)
        self.at('The random jiggle'); self.play(Create(g[1]),FadeIn(g[4]),run_time=.8)
        self.at('so it partly cancels')
        self.play(FadeIn(spreads()),FadeIn(label('spread',4.6,1.5,28,GREY)),
                  FadeIn(label('t',FX(10),-2.55,26)),FadeIn(label('4t',FX(40),-2.55,26)),run_time=.35); self.finish()


class S09Question(SpokenScene):
    def construct(self):
        g=fan(); q=question(); self.add(g)
        self.at('Here is a question')
        # Crossfade the complete chart away; no masked lines behind the quiz.
        self.play(FadeOut(g),FadeIn(q[0]),FadeIn(q[2]),run_time=.2)
        self.at('You watch four times'); self.play(Indicate(q[0],scale_factor=1.02),run_time=.3)
        self.at('Is your running total'); self.play(FadeIn(q[1]),run_time=.3); self.finish()


class S10Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question())
        ring=Circle(radius=.5,color=GREY,stroke_width=3).move_to([0,-2.35,0])
        remaining=ValueTracker(1.)
        arc=always_redraw(lambda: Arc(radius=.5,start_angle=PI/2,angle=-TAU*max(.001,remaining.get_value()),color=GOLD,stroke_width=7).move_arc_center_to([0,-2.35,0]))
        self.add(ring,arc); self.play(remaining.animate.set_value(0),run_time=5,rate_func=linear)


class S11Reveal(SpokenScene):
    def construct(self):
        q=question(); self.add(q)
        self.at('it is only twice')
        answer=VGroup(label('Twice as reliable.',0,1.3,48,YELLOW),label('reliable = signal ÷ noise',0,-.25,30),label('4 ÷ 2 = 2',0,-1.6,38,YELLOW))
        self.play(FadeOut(q),FadeIn(answer),run_time=.3); self.finish()


class S12Why(SpokenScene):
    def construct(self):
        g=fan(); g[3][0].move_to([-3.5,-2.95,0]); self.add(g)
        times=VGroup(*[VGroup(DashedLine([FX(n),-2.1,0],[FX(n),FY(.65*n),0],color=GOLD),Dot([FX(n),FY(.65*n),0],color=YELLOW),label(s,FX(n),-2.55,28,GOLD)) for n,s in ((10,'t'),(40,'4t'))])
        self.add(times)
        self.at('The signal grows')
        sig=VGroup(bracket(FX(10)-.25,FY(0),FY(6.5),YELLOW),bracket(4.05,FY(0),FY(26),YELLOW),label('signal ×4',5.15,-.5,28,YELLOW))
        self.play(FadeIn(sig),run_time=.35)
        self.at('The noise grows too')
        noise=VGroup(spreads(),label('1 spread',-4.05,FY(6.5+.8*np.sqrt(10)),26,GREY),Line([FX(10)-.45,FY(6.5+.8*np.sqrt(10)),0],[FX(10)-.13,FY(6.5+.8*np.sqrt(10)),0],color=GREY),
                     label('2 spreads',4.95,1.5,26,GREY),Line([3.65,1.5,0],[3.95,1.5,0],color=GREY),label('noise ×2',4.95,2.15,28,GREY))
        self.play(FadeIn(noise),run_time=.35)
        self.at('square root of time'); self.play(FadeIn(label('signal ÷ noise: 4 ÷ 2 = 2',2.15,-3.5,28,YELLOW)),run_time=.3); self.finish()


class S13Rule(SpokenScene):
    def construct(self):
        # Parameterize by sqrt(n): smooth origin, all points exactly y=sqrt(n).
        ax=axes(-4.9,0.,-2.1,2.45)
        root=poly([(-4.9+4.9*u*u/4,-2.1+2.1*u) for u in np.linspace(0,2,300)],YELLOW,6)
        self.add(ax,root,label('reliability',-3.8,3.15,30,YELLOW),label('samples added (n)',-2.45,-3.2,28,GREY))
        self.at('Assume each glimpse')
        cond=VGroup(label('same mean signal',3.35,2.6,28),label('independent noise',3.35,2.,28),label('same spread',3.35,1.4,28),label('(finite variance)',3.35,.9,26,GREY))
        self.play(FadeIn(cond),run_time=.35)
        self.at('Reliability here means')
        self.play(FadeIn(label('signal ÷ noise',3.35,-.1,32,YELLOW)),FadeIn(label('noise = standard deviation',3.35,-.75,26,GREY)),
                  FadeIn(label('Not percent correct',3.35,-1.55,28,GOLD)),run_time=.35)
        self.at('It grows as')
        marks=VGroup()
        for n in (1,4):
            x=-4.9+4.9*n/4; y=-2.1+2.1*np.sqrt(n)
            marks.add(DashedLine([x,-2.1,0],[x,y,0],color=GREY),Dot([x,y,0],color=YELLOW),label(str(n),x,-2.55,28),label(str(int(np.sqrt(n))),-5.5,y,28,YELLOW),DashedLine([-4.9,y,0],[x,y,0],color=GREY))
        self.play(FadeIn(marks),FadeIn(label('reliability ∝ √n',3.35,-2.75,34,YELLOW)),run_time=.4); self.finish()


class S14Behaviour(SpokenScene):
    def construct(self):
        c=np.linspace(0,51.2,240); mu=7.8125*c; a=40; sig2=8000/np.log(9)
        rt=np.empty_like(mu); rt[0]=.270+a*a/sig2
        rt[1:]=.270+a/mu[1:]*np.tanh(a*mu[1:]/sig2)
        curve=poly([(-4.4+8.8*cc/51.2,-2.6+(v-.3)/.45*1.5) for cc,v in zip(c,rt)],GREEN,5)
        self.add(axes(-4.4,4.4,-2.6,-1.1),curve,
                 label('reaction time (ms)',-6.05,-1.85,25,GREEN).rotate(PI/2),
                 label('750',-5.05,-1.1,26,GREY),label('300',-5.05,-2.6,26,GREY),
                 label('0%',-4.4,-3.,26,GREY),label('51.2%',4.4,-3.,26,GREY),
                 label('coherence (%)',0,-3.,26,GREY),label('Running total: weak vs strong motion',0,3.55,30,YELLOW))
        panels=VGroup()
        # Deterministic mean accumulation, equal level, mu proportional to coherence.
        for cx,mu,name in ((-3.4,1.,'weak motion'),(3.4,4.,'strong motion')):
            x0,x1=cx-2.4,cx+2.4; y0,y1=.3,2.25
            t_hit=4/mu
            line=poly([(x0+4.8*t/4,y0+1.95*mu*t/4) for t in np.linspace(0,t_hit,80)],YELLOW,5)
            panels.add(axes(x0,x1,y0,y1),line,DashedLine([x0,2.25,0],[x1,2.25,0],color=GOLD),
                       label(name,cx,2.95,26,YELLOW),label('time →',cx,.05,26,GREY),
                       label('longer' if mu==1 else 'sooner',x0+4.8*t_hit/4+(-.65 if mu==1 else .75),.85,26,GOLD),
                       DashedLine([x0+4.8*t_hit/4,y0,0],[x0+4.8*t_hit/4,2.25,0],color=GOLD))
        self.add(panels)
        self.at('Weak motion gives'); self.play(Indicate(panels[1],scale_factor=1.03),run_time=.35)
        self.at('takes longer')
        # Highlight low-coherence region on the transformed, computed RT curve.
        highlight=SurroundingRectangle(VGroup(*[Dot(curve.point_from_proportion(v),radius=.03) for v in np.linspace(0,.14,12)]),color=YELLOW,buff=.15)
        self.play(Create(highlight),FadeIn(label('weak motion → longer wait',0,-3.45,28,YELLOW)),run_time=.35); self.finish()


class S15Trade(SpokenScene):
    def construct(self):
        pivot=np.array([0,.3,0]); angle=ValueTracker(.13)
        fulcrum=Polygon([-1,-2.6,0],[1,-2.6,0],pivot,color=GREY,fill_opacity=.2)
        def scale_group():
            a=angle.get_value(); left=pivot+np.array([-4.1*np.cos(a),-4.1*np.sin(a),0]); right=pivot+np.array([4.1*np.cos(a),4.1*np.sin(a),0])
            beam=Line(left,right,color=GREY,stroke_width=7)
            pans=VGroup()
            for p,name,col in ((left,'time',GREY),(right,'accuracy',GREEN)):
                pans.add(Line(p,p+DOWN*1.3,color=col),Line(p+DOWN*1.3+LEFT*.9,p+DOWN*1.3+RIGHT*.9,color=col,stroke_width=4),label(name,p[0],p[1]-1.75,30,col))
                if name=='time':
                    c=p+DOWN*.7; pans.add(Circle(radius=.43,color=col).move_to(c),Line(c,c+UP*.3,color=col),Line(c,c+RIGHT*.22,color=col))
                else:
                    pans.add(*[Circle(radius=r,color=col).move_to(p+DOWN*.7) for r in (.43,.27,.08)])
            return VGroup(beam,pans)
        scale=always_redraw(scale_group)
        title=label('Waiting longer',0,3.1,38,GOLD)
        self.add(fulcrum,scale,title)
        self.at('Waiting longer'); self.at('buys accuracy'); self.play(angle.animate.set_value(-.19),run_time=.65)
        self.at('costs time'); self.wait(.2)
        self.at('a brain that adds')
        scale.clear_updaters(); g=fan()
        self.play(FadeOut(fulcrum),FadeOut(scale),FadeOut(title),FadeIn(g),run_time=.2)
        self.at('when to stop')
        # The bound is above every plotted sample and the mean (not a crossed bound).
        self.play(Create(DashedLine([-4.9,2.65,0],[3.5,2.65,0],color=GOLD,stroke_width=4)),FadeIn(label('When to stop?',4.8,3.15,30,GOLD)),run_time=.3); self.finish()


def vertical_neuron(x,y,s=1):
    c=np.array([x,y,0])
    g=VGroup(Circle(radius=.3*s,color=BLUE,fill_opacity=.3).move_to(c))
    for dx,dy in ((-.9,.7),(-.3,.9),(.35,.85),(.9,.6)):
        g.add(Line(c+np.array([dx*.3,dy*.3,0])*s,c+np.array([dx,dy,0])*s,color=BLUE,stroke_width=3))
    g.add(Line(c+DOWN*.3*s,c+DOWN*1.15*s,color=BLUE,stroke_width=4))
    return g


class S16Neurons(SpokenScene):
    def construct(self):
        g=fan(); self.add(g)
        self.at('across neurons')
        xs=(-4.8,-1.6,1.6,4.8)
        cells=VGroup(*[vertical_neuron(x,1.65,1.05) for x in xs])
        dest=vertical_neuron(0,-1.9,1.)
        # Separate axons meet a pooling junction; one small arrow reaches the soma.
        connections=VGroup(*[poly([(x,.44),(x,-.45),(0,-.85)],BLUE,2) for x in xs],Line([0,-.85,0],[0,-1.05,0],color=BLUE),arrow((0,-1.05),(0,-1.59),BLUE))
        rng=np.random.RandomState(45); t=np.linspace(0,1,90)
        # Sixteen independent samples per input are represented by their mean;
        # four such inputs pool downstream. The common evoked bump is preserved.
        raw=rng.normal(0,1,(4,16,90))
        signal=.55*np.exp(-.5*((t-.55)/.17)**2)
        inputs=signal+raw.mean(axis=1)
        traces=VGroup()
        for x,row in zip(xs,inputs):
            # Traces sit to the right of their vertical axons, with a visible gap.
            traces.add(poly([(x+.18+1.4*u,-.05+.55*r) for u,r in zip(t,row)],YELLOW,2.5))
        pooled=signal+raw.mean(axis=(0,1))
        output=poly([(.35+2*u,-2.9+.55*r) for u,r in zip(t,pooled)],YELLOW,3)
        self.play(FadeOut(g),FadeIn(cells),FadeIn(dest),Create(connections),run_time=.45)
        self.play(Create(traces),Create(output),FadeIn(label('if the noise is independent',0,3.35,30,GOLD)),run_time=.5)
        self.at('effects of attention matter'); self.play(FadeIn(label('signals combine',4.,-1.75,30,BLUE)),FadeIn(label('cleaner pooled signal',4.6,-2.9,26,YELLOW)),run_time=.3); self.finish()


class S17Takeaway(SpokenScene):
    def construct(self):
        g=fan(); g[3][1].move_to([-3.3,2.85,0]); self.add(g)
        self.at('Adding up noisy evidence'); self.play(FadeIn(label('Add up noisy evidence',0,3.4,34,YELLOW)),run_time=.3)
        self.at('the signal adds in step'); self.play(g[2].animate.set_stroke(width=8),FadeIn(label('signal adds in step',4.8,-1.1,28,YELLOW)),run_time=.3)
        self.at('the noise partly cancels'); self.play(g[1].animate.set_stroke(opacity=.3),FadeIn(label('The signal adds in step; the noise partly cancels.',0,-3.5,28)),run_time=.3); self.finish()


class S18End(EndCard):
    LINE='Adding up noisy evidence makes it more reliable.'
