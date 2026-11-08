"""Replay to cause — word-timed chapter 2.
COLOR MAP (from scenes.old.py, shared with the chapter series):
 YELLOW active cells; BLUE light / opsin; GREEN intact or improved recall;
 RED silenced activity / failed recall; ORANGE engram candidate;
 PURPLE control; GOLD open question; GREY resting cells / structure.
No changes to CHAPTERS.md: TASK.md restricts source edits to this file.
Plots: co-firing values are the lesson's explicit teaching data. Raster is an
ordered illustrative spike table, not a published recording. LFP is computed
from a 200 Hz sinusoid in a 50 ms raised-cosine envelope plus a slower dip;
frequency and duration come from the lesson. Outcome bars are qualitative.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
ORANGE = '#F29E4C'


def label(s, x=0, y=3.05, size=30, color=TEXT):
    return T(s, size=size, color=color).move_to([x,y,0])


def arr(a,b,color=GREY,w=5,tip=.2):
    return Arrow(a,b,buff=.06,color=color,stroke_width=w,tip_length=tip,
                 max_tip_length_to_length_ratio=.45,max_stroke_width_to_length_ratio=12)


def cell(p,r=.26):
    p=np.array([p[0],p[1],0.])
    soma=Circle(radius=r,stroke_color=GREY,stroke_width=3,fill_color=GREY,fill_opacity=.25).move_to(p)
    stubs=VGroup()
    for ang in (100,215,325):
        d=np.array([np.cos(np.radians(ang)),np.sin(np.radians(ang)),0])
        stubs.add(Line(p+d*r,p+d*(r+.17),color=GREY,stroke_width=3))
    g=VGroup(soma,stubs); g.soma=soma; g.stubs=stubs
    return g


def st(c,s):
    col,op={'idle':(GREY,.25),'active':(YELLOW,.85),'silent':(RED,.1)}[s]
    return [c.soma.animate.set_stroke(col).set_fill(col,op),c.stubs.animate.set_stroke(col)]


def rat(x=0,y=0,scale=1,sleep=False):
    # Deliberately schematic animal, with eye closed when asleep.
    body=Ellipse(width=1.65,height=.85,color=GREY,fill_opacity=.25)
    head=Ellipse(width=.7,height=.6,color=GREY,fill_opacity=.25).move_to([.8,.12,0])
    ear=Circle(radius=.12,color=GREY,fill_color=BG,fill_opacity=1).move_to([.63,.29,0])
    tail=VMobject(color=GREY).set_points_as_corners([[-.75,-.05,0],[-1.15,-.2,0],[-1.45,-.1,0]])
    eye=Line([.87,.22,0],[1.03,.22,0],color=TEXT) if sleep else Dot([.95,.22,0],radius=.045,color=TEXT)
    return VGroup(body,head,ear,tail,eye).scale(scale).move_to([x,y,0])


# Exact word onsets, no per-scene padding; pipeline rounds to 15 fps.
class TimedScene(SpokenScene):
    def at(self, phrase, lead=0, nth=0):
        remaining=self.t_of(phrase,nth)-self.elapsed()
        if remaining>.001: self.wait(remaining)
    def finish(self):
        remaining=self.narration_s-self.elapsed()
        if remaining>.001: self.wait(remaining)


def ladder():
    corr=chip('correlation: goes with',TEXT,28).move_to([0,-2,0])
    suf=chip('turn on: enough',TEXT,28).move_to([-3,1.5,0])
    nec=chip('turn off: needed',TEXT,28).move_to([3,1.5,0])
    rails=VGroup(Line([-5.9,-2,0],[5.9,-2,0],color=GREY),Line([-5.9,1.5,0],[5.9,1.5,0],color=GREY))
    for c in (corr,suf,nec): c[0].set_fill(BG,1)
    return VGroup(rails,corr,suf,nec)


def climb(g,color=RED):
    return Arrow(g[1].get_top(),g[3].get_bottom(),buff=0,color=color)


def small_ladder(x=3.3,y=0):
    corr=chip('correlation',TEXT,26).move_to([x,y-1.1,0])
    suf=chip('turn on:\nenough',TEXT,26).move_to([x-1.4,y+1,0])
    nec=chip('turn off:\nneeded',TEXT,26).move_to([x+1.4,y+1,0])
    rails=VGroup(Line([x-2.65,y-1.1,0],[x+2.65,y-1.1,0],color=GREY),Line([x-2.65,y+1,0],[x+2.65,y+1,0],color=GREY))
    for c in (corr,suf,nec): c[0].set_fill(BG,1)
    return VGroup(rails,corr,suf,nec)


def cofire(silent=False):
    base=-1.9; height=4.35; xs=[-3.65,0,3.65]
    vals=[.02,.30,.10] if not silent else [.02,0,.02]
    axis=VGroup(Line([-5.2,base,0],[5.7,base,0],color=GREY),Line([-5.2,base,0],[-5.2,2.65,0],color=GREY))
    for v in (0,.1,.2,.3):
        y=base+height*v/.3
        axis.add(Line([-5.3,y,0],[-5.15,y,0],color=TEXT),label(f'{v:g}',-5.75,y,26))
    axis.add(label('co-firing of one pair (made-up scale)',0,3.25,28))
    bars=VGroup(); nums=VGroup(); blocks=VGroup()
    for x,v,txt in zip(xs,vals,['sleep before','task','sleep after']):
        h=max(.01,height*v/.3)
        bars.add(Rectangle(width=1.25,height=h,color=YELLOW,fill_opacity=.65).move_to([x,base+h/2,0]))
        nums.add(label(f'{v:.2f}',x,base+h+.25,26,YELLOW))
        box=RoundedRectangle(width=3.1,height=.7,corner_radius=.1,color=GREY).move_to([x,-2.65,0])
        block=VGroup(box,label(txt,x,-2.65,26))
        if txt=='task':
            track_icon=RoundedRectangle(width=1.55,height=.36,corner_radius=.16,color=GREY,stroke_width=3).move_to([x,-3.26,0])
            block.add(track_icon,Dot([x+.35,-3.26,0],radius=.08,color=YELLOW))
        else: block.add(label('z z',x,-3.26,30,GREY))
        blocks.add(block)
    return VGroup(axis,bars,nums,blocks,label('made-up numbers for teaching',0,-3.7,26,GREY))


def raster(mode=None):
    ys=np.linspace(-2.45,2.35,6)
    track=Line([-5.7,-2.6,0],[-5.7,2.5,0],color=GREY,stroke_width=7)
    rows=VGroup(); fields=VGroup()
    colors=[BLUE,PURPLE,GREEN,ORANGE,YELLOW,TEAL]
    for i,y in enumerate(ys):
        c=colors[i]
        fields.add(Ellipse(width=.5,height=.55,color=c,fill_opacity=.55).move_to([-5.7,y,0]))
        rows.add(VGroup(Line([-5.4,y,0],[5.8,y,0],color=c,stroke_opacity=.3),label(str(i+1),-4.7,y,26,c)))
    axes=VGroup(arr([-3.9,-2.9,0],[5.8,-2.9,0]),label('time: seconds during run',1,-3.4,26),label('place',-5.7,3,26))
    ticks=VGroup()
    if mode:
        for i,y in enumerate(ys):
            t=i if mode!='reverse' else 5-i
            x=-3.4+1.65*t if mode=='run' else -.7+.3*t
            ticks.add(Line([x,y-.18,0],[x,y+.18,0],color=YELLOW,stroke_width=5))
    return VGroup(track,fields,rows,axes),ticks


def wave(y=0,width=11,kind='full',slow=False,color=YELLOW,gain=1):
    # t in seconds: 200 waves/s, event centered at 40 ms, duration 50 ms.
    t=np.linspace(0,.12,1601)
    u=(t-.04)/.025
    envelope=np.where(np.abs(u)<=1,.5*(1+np.cos(np.pi*np.clip(u,-1,1))),0)
    v=-1.15*envelope
    if not slow: v=v+.42*envelope*np.sin(2*np.pi*200*t)
    if kind=='cut': v=np.where(t>.03,0,v)
    if kind=='long':
        u=(t-.055)/.04
        e=np.where(np.abs(u)<=1,.5*(1+np.cos(np.pi*np.clip(u,-1,1))),0)
        v=-1.15*e+.42*e*np.sin(2*np.pi*200*t)
    points=np.column_stack(((t/.12-.5)*width,y+gain*v,np.zeros(len(t))))
    return VMobject(color=color,stroke_width=3).set_points_as_corners(points)




def results(question=False):
    base=-2.05
    axis=VGroup(Line([-4.4,base,0],[4.8,base,0],color=GREY),Line([-4.4,base,0],[-4.4,1.85,0],color=GREY),label('next-day performance',0,2.2,28))
    low=Rectangle(width=1.65,height=1.45,color=RED,fill_opacity=.65).move_to([-2.6,base+.725,0])
    high=Rectangle(width=1.65,height=1.45 if question else 3.25,color=PURPLE,fill_opacity=0 if question else .65).move_to([2.6,base+(.725 if question else 1.625),0])
    labs=VGroup(label('ripple-cut',-2.6,-2.55,26,RED),label('control' if question else 'delayed control',2.6,-2.55,26,PURPLE),label('qualitative comparison',0,-3.45,26,GREY))
    extra=label('?',2.6,-1.3,48,GOLD) if question else VGroup(DashedLine([-4.3,1.2,0],[4.7,1.2,0],color=GREY),label('not impaired',2.6,1.65,26,PURPLE))
    return VGroup(axis,low,high,labs,extra)


def loop():
    det=chip('detector',TEXT,30).move_to([-3.4,1.8,0])
    stim=chip('stimulator',RED,30).move_to([3.4,1.8,0])
    lines=VGroup(arr([-4.3,-.7,0],[-4.3,1.3,0]),arr(det.get_right(),stim.get_left(),RED),VGroup(Line([4.4,1.3,0],[4.4,-.2,0],color=RED),Line([4.4,-.2,0],[-2.75,-.2,0],color=RED),arr([-2.75,-.2,0],[-2.75,-.8,0],RED)))
    return VGroup(det,stim,lines,label('ripple → detect → stimulate',0,-3.2,28))


def maze(x=-3.5,y=-1.6):
    return VGroup(Rectangle(width=2.4,height=1.8,color=GREY),Line([-.4,-.9,0],[-.4,.3,0],color=GREY),Line([.4,.9,0],[.4,-.3,0],color=GREY)).move_to([x,y,0])


END_LINE='Ripple-linked activity aids memory, in the tasks tested.'
def takeaway():
    return T(END_LINE,size=32,font=TITLE_FONT).move_to([0,.1,0])


class S00Title(TitleCard):
    LESSON='Plasticity, Networks and Consolidation'
    TITLE='Replay and Ripples: Correlation to Perturbation'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.5,26,TEAL),label(self.LESSON,0,1.5,28),T('Replay and Ripples:\nCorrelation to Perturbation',size=44,font=TITLE_FONT))
        self.wait(self.narration_s)


class S01(TimedScene):
    def construct(self):
        cs=VGroup(*[cell(p,.65) for p in [(-4,1.2),(-2.2,1.5),(-3,-.7)]])
        r=rat(3,.1,2,True)
        self.add(cs,r,label('z z z',3,1.7,36),label('Can the group be set going offline?',0,-2.7,34,GOLD))
        self.at('Could a group')
        self.play(*sum([st(c,'active') for c in cs],[]),run_time=.3)
        self.at('also be set going')
        self.play(*sum([st(c,'idle') for c in cs],[]),run_time=.2)
        self.play(*sum([st(c,'active') for c in cs],[]),run_time=.25)
        blocked=VGroup(DashedLine([-6,0,0],[-4.9,0,0],color=GREY),Line([-5.2,-.3,0],[-5.2,.3,0],color=RED),label('no outside cue',-3.6,-1.7,26,GREY))
        self.play(FadeIn(blocked),run_time=.25)
        self.finish()


class S02(TimedScene):
    def construct(self):
        brain=Ellipse(width=10.8,height=5.2,color=GREY,fill_opacity=.1)
        hip=Ellipse(width=2.8,height=1.3,color=YELLOW).move_to([-2,-.8,0])
        ctx=Ellipse(width=3.3,height=1.3,color=BLUE).move_to([2,1,0])
        self.add(brain,hip,ctx)
        self.at('One proposal'); self.play(FadeIn(label('one proposal · tested next',0,3.1,30,GOLD)),run_time=.25)
        self.at('the hippocampus'); self.play(FadeIn(label('hippocampus',-2,-.8,28)),run_time=.25)
        self.at('replays experience')
        path=CurvedArrow([-.55,-.8,0],[3.7,1,0],angle=1.5,color=YELLOW)
        self.play(Create(path),FadeIn(label('replay',2,-2.05,28,YELLOW)),run_time=.4)
        self.at('teaching the cortex'); self.play(FadeIn(label('cortex',2,1,28)),run_time=.35)
        self.finish()


class S03(TimedScene):
    def construct(self):
        g=ladder(); self.add(g)
        self.at('from correlation'); self.play(g[1][0].animate.set_stroke(GOLD),run_time=.25)
        self.at('turning ripple activity off'); self.play(g[3][0].animate.set_stroke(RED),GrowArrow(climb(g)),run_time=.4)
        self.finish()


class S04(TimedScene):
    def construct(self):
        rs=VGroup(*[rat(x,-1.1,1.5) for x in (-4.3,0,4.3)])
        self.add(rs)
        self.at('Matthew Wilson'); self.play(FadeIn(label('Wilson and McNaughton · 1994',0,3.1,32)),run_time=.3)
        self.at('recorded many')
        wires=VGroup(*[Line([x+1.1,-.8,0],[x+d,1.2,0],color=GREY) for x in (-4.3,0,4.3) for d in (-.4,0,.4)])
        self.play(Create(wires),run_time=.3)
        self.at('hippocampal cells')
        dots=VGroup(*[Dot([x+d,1.45+.3*(i%2),0],radius=.13,color=YELLOW) for x in (-4.3,0,4.3) for i,d in enumerate((-.6,-.2,.2,.6))])
        self.play(FadeIn(dots),FadeIn(label('many hippocampal cells',0,2.4,28,YELLOW)),run_time=.3)
        self.finish()


class S05(TimedScene):
    def construct(self):
        g=cofire(); self.add(g[0],g[4])
        for phrase,i in [('sleep before',0),('the task itself',1),('and sleep after',2)]:
            self.at(phrase); self.play(FadeIn(g[3][i]),FadeIn(g[1][i]),FadeIn(g[2][i]),run_time=.25)
        self.finish()


class S06(TimedScene):
    def construct(self):
        g=cofire(); self.add(g)
        self.at('Pairs that'); self.play(Indicate(g[1][1],scale_factor=1.03),run_time=.3)
        self.at('more in the sleep')
        # Compare only the sleep heights, below the task value and its label.
        bracket=VGroup(Line([-2.85,-1.61,0],[-.85,-1.61,0],color=GOLD),Line([.85,-1.61,0],[2.8,-1.61,0],color=GOLD),Line([-2.85,-1.74,0],[-2.85,-1.48,0],color=GOLD),Arrow([2.8,-1.61,0],[2.8,-.45,0],buff=0,color=GOLD),label('rise',2.15,-.75,28,GOLD))
        self.play(Create(bracket),g[1][2].animate.set_fill(YELLOW,1),run_time=.35)
        self.finish()


# Comparison panels keep all text at original point size; each has its own x labels.
def comparison():
    groups=VGroup()
    for j,(cx,vals,title) in enumerate([(-3.3,[.02,.3,.1],'task-active pair'),(3.3,[.02,0,.02],'task-silent pair')]):
        base=-1.8; h=3.8
        g=VGroup(label(title,cx,2.7,28),Line([cx-2.3,base,0],[cx+2.3,base,0],color=GREY))
        for v in (0,.1,.2,.3):
            y=base+h*v/.3
            g.add(label(f'{v:g}',cx-2.5,y,26,GREY))
        for x,v,txt in zip([cx-1.4,cx,cx+1.4],vals,['before','task','after']):
            bh=max(.01,h*v/.3)
            g.add(Rectangle(width=.7,height=bh,color=YELLOW,fill_opacity=.6).move_to([x,base+bh/2,0]),label(f'{v:.2f}',x,base+bh+.28,26,YELLOW),label(txt,x,-2.3,26))
        groups.add(g)
    groups.add(label('co-firing of one pair (made-up scale)',0,3.45,28),label('made-up numbers for teaching',0,-3.5,22,GREY))
    return groups


class S07(TimedScene):
    def construct(self):
        old=cofire(); self.add(old)
        self.at('Pairs that were silent')
        g=comparison()
        self.play(old.animate.scale(.53).move_to([-3.3,0,0]),run_time=.5)
        self.play(FadeOut(old),FadeIn(g),run_time=.15)
        self.at('showed no such rise'); self.play(FadeIn(label('no rise',3.3,-2.95,28,GOLD)),run_time=.3)
        self.finish()


class S08(TimedScene):
    def construct(self):
        g=comparison(); self.add(g)
        self.at('This was pairwise'); title=label('pairwise co-firing',0,3.45,30,GOLD)
        self.play(Transform(g[2],title),run_time=.2)
        self.at('and a correlation')
        # Retain bars at full text size in the left panel; replace right panel with ladder.
        l=small_ladder()
        self.play(FadeOut(g[1]),FadeIn(l),run_time=.3)
        self.play(l[1][0].animate.set_stroke(GOLD),run_time=.2)
        self.at('not a test of memory'); self.play(FadeIn(label('not a test of memory',0,-2.95,30,GOLD)),run_time=.25)
        self.finish()


class S09(TimedScene):
    def construct(self):
        g,_=raster()
        order=[3,0,5,1,4,2]
        ys=np.linspace(-2.45,2.35,6)
        # Each identity includes its matching field blob, so its colour travels with it.
        identities=VGroup(*[VGroup(g[1][i],g[2][i]) for i in range(6)])
        for i,row in enumerate(identities): row.shift(UP*(ys[order[i]]-ys[i]))
        self.add(g[0],g[3],identities)
        self.at('Later work read'); h=label('place cells along the track',.7,3.25,28); self.play(FadeIn(h),run_time=.2)
        self.at('Each row here')
        self.play(Indicate(identities[2][1],scale_factor=1),Indicate(identities[2][0],scale_factor=1.3,color=GREEN),run_time=.5)
        self.at('one place cell'); self.play(Transform(h,label('one row = one place cell',.7,3.25,28)),run_time=.25)
        self.at('sorted along the track')
        self.play(*[row.animate.shift(UP*(ys[i]-ys[order[i]])) for i,row in enumerate(identities)],Transform(h,label('rows ordered by place on track',.7,3.25,28)),run_time=1.05,rate_func=smooth)
        self.finish()


class S10(TimedScene):
    def construct(self):
        g,t=raster('run'); r=rat(-5.7,-2.45,.65); self.add(g,r,label('rows ordered by place on track',.7,3.25,28))
        self.at('During a run'); self.play(r.animate.move_to([-5.7,2.35,0]),LaggedStart(*[Create(x) for x in t],lag_ratio=.15),run_time=1.6,rate_func=linear)
        self.finish()


def replay_header(text): return label(text,0,3.25,28,YELLOW)
def compression():
    return VGroup(Line([-.85,-2.7,0],[.95,-2.7,0],color=YELLOW),Line([-.85,-2.55,0],[-.85,-2.85,0],color=YELLOW),Line([.95,-2.55,0],[.95,-2.85,0],color=YELLOW),label('same order, much faster',1,-3.05,26,YELLOW))


class S11(TimedScene):
    def construct(self):
        g,run=raster('run'); h=replay_header('after run · pause · compressed')
        self.add(g,run,rat(-5.7,2.35,.65),h)
        self.at('In pauses at the end')
        self.at('the sequence replayed')
        _,rev=raster('reverse'); run.set_opacity(.18)
        self.play(LaggedStart(*[Create(x) for x in reversed(list(rev))],lag_ratio=.1),Transform(h,replay_header('after run · reverse · compressed')),Transform(g[3][1],label('replay: a fraction of a second',1,-3.55,26)),run_time=.6)
        self.at('compressed in time'); self.play(FadeIn(label('Diba and Buzsáki · 2007',1,2.75,26)),Transform(h,replay_header('after run · reverse · compressed')),FadeIn(compression()),run_time=.25)
        self.finish()


class S11b(TimedScene):
    def construct(self):
        g,run=raster('run'); _,t=raster('forward'); run.set_opacity(.18)
        g[3][1].become(label('replay: a fraction of a second',1,-3.55,26))
        self.add(label('Diba and Buzsáki · 2007',1,2.75,26))
        self.add(g,run,compression(),rat(-5.7,-2.45,.65))
        self.at('Before runs'); self.play(FadeIn(replay_header('before run · forward · compressed')),run_time=.2)
        self.at('it played forward'); self.play(LaggedStart(*[Create(x) for x in t],lag_ratio=.1),run_time=.5)
        self.finish()


class S12(TimedScene):
    def construct(self):
        cs=VGroup(*[cell(p,.62) for p in [(-3.6,1.5),(-1.7,.8),(1.8,1.5),(3.6,.8)]])
        electrode=Line([0,2.7,0],[0,.3,0],color=TEXT,stroke_width=6)
        self.add(cs,electrode,label('CA1',-4.9,1.4,30))
        self.at('Much replay rides'); self.play(*sum([st(c,'active') for c in cs],[]),run_time=.25)
        self.at('sharp wave ripples'); self.play(FadeIn(label('sharp-wave ripple',0,3.25,32,YELLOW)),run_time=.2)
        self.at('in the local field potential')
        link=arr([0,.3,0],[0,-.35,0],TEXT)
        tr=wave(y=-.4,width=12,gain=1.7)
        self.play(GrowArrow(link),Create(tr),FadeIn(label('local field potential (LFP)',0,-3.5,34)),run_time=.6)
        self.at('the summed electrical signal')
        self.play(*sum([st(c,'active') for c in cs],[]),tr.animate.shift(LEFT*.5),run_time=.5)
        self.at('near an electrode'); self.play(Indicate(electrode,color=YELLOW),run_time=.3)
        self.finish()


class S13(TimedScene):
    def construct(self):
        tr=wave(y=-.4,width=12,gain=1.7); self.add(tr)
        target=wave(y=1.5,width=17,gain=2.7).shift(RIGHT*2.8)
        # Zoom the computed event, clipping only the inactive baseline to safe width.
        target=VMobject(color=YELLOW,stroke_width=3).set_points_as_corners([p for p in target.get_points() if -6<p[0]<6])
        self.at('A sharp wave ripple'); self.play(Transform(tr,target),run_time=.55)
        self.at('a slower sharp wave')
        self.play(FadeIn(label('sharp wave',-4.4,-1.5,30)),Create(Line([-3.8,-1.2,0],[-2.4,.1,0],color=GREY)),run_time=.25)
        self.at('a burst of very fast')
        self.play(FadeIn(label('ripple',3.8,2.6,30,YELLOW)),Create(Line([3,2.35,0],[.9,.3,0],color=YELLOW)),FadeIn(label('roughly 150 to 250 waves per second',0,3.35,28,YELLOW)),run_time=.3)
        self.at('It lasts tens')
        br=VGroup(Line([-3.6,-2.75,0],[3.5,-2.75,0],color=TEXT),Line([-3.6,-2.6,0],[-3.6,-2.9,0]),Line([3.5,-2.6,0],[3.5,-2.9,0]),label('tens of milliseconds',0,-3.35,28))
        self.play(Create(br),run_time=.25); self.finish()


class S14(TimedScene):
    def construct(self):
        g=loop(); baseline=Line([-5.5,-.8,0],[5.5,-.8,0],color=GREY,stroke_opacity=.3)
        self.add(g[0],g[1],g[2][0],g[2][1],g[3],baseline)
        self.at('A computer can detect')
        tr=wave(y=-.8,gain=1.3); start=tr.copy().pointwise_become_partial(tr,0,.18)
        self.play(Create(start),run_time=.35)
        self.at('as it starts'); self.play(g[0][0].animate.set_stroke(YELLOW),Transform(start,tr.copy().pointwise_become_partial(tr,0,.25)),run_time=.25)
        self.at('trigger a stimulus'); self.play(g[1][0].animate.set_fill(RED,.5),Create(g[2][2]),run_time=.25)
        self.at('that cuts it short')
        cut=wave(y=-.8,kind='cut',gain=1.3)
        self.play(Transform(start,cut),Create(Line([-2.75,-.4,0],[-2.75,-2.6,0],color=RED,stroke_width=5)),FadeIn(label('stimulus: ripple cut short',0,-3.2,28,RED)),FadeOut(g[3]),run_time=.3)
        self.finish()


class S15(TimedScene):
    def construct(self):
        g=results(True); self.add(g[0],g[3][0])
        self.at('do worse next day'); self.play(FadeIn(g[1]),run_time=.2)
        self.at('What control do you need'); self.play(FadeIn(g[2]),FadeIn(g[4]),FadeIn(g[3][1]),FadeIn(label('What control do you need?',0,3.15,30,GOLD)),run_time=.3)
        self.finish()


class S16Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        g=results(True); self.add(g[0],g[1],g[2],g[3][0],g[3][1],g[4],label('What control do you need?',0,3.15,30,GOLD),label('pause: what control?',0,-3.35,26,GREY)); self.wait(5)


class S17(TimedScene):
    def construct(self):
        g=loop(); g[2][2].become(arr([4.4,1.3,0],[4.4,-.8,0],RED)); tr=wave(y=-.8,gain=1.3,color=PURPLE)
        self.add(g[0],g[1],g[2][0],g[2][1],g[3],Line([-5.5,-.8,0],[5.5,-.8,0],color=GREY))
        self.at('Give another group'); self.play(FadeIn(label('delayed control',0,3.25,30,PURPLE)),run_time=.2)
        self.at('the same stimuli'); self.play(Transform(g[3],label('same number of stimuli',0,-3.2,28,PURPLE)),run_time=.25)
        self.at('each delayed after a ripple')
        start=tr.copy().pointwise_become_partial(tr,0,.18)
        self.play(Create(start),g[0][0].animate.set_stroke(YELLOW),run_time=.15)
        self.play(Transform(start,tr),run_time=.35)
        delay=VGroup(DoubleArrow([.5,-.2,0],[4.4,-.2,0],buff=0,color=PURPLE),label('delay',2.1,.25,28,PURPLE))
        self.play(Create(delay),run_time=.25)
        self.play(Create(g[2][2]),g[1][0].animate.set_fill(RED,.5),Create(Line([4.4,-.5,0],[4.4,-2.5,0],color=RED)),FadeIn(label('stimulus',4.2,-2.8,26,RED)),run_time=.2)
        self.at('so its ripples run'); self.play(Indicate(start,color=PURPLE,scale_factor=1.01),run_time=.25)
        self.finish()


class S18(TimedScene):
    def construct(self):
        g=results(); self.add(g[0],g[1],g[3][0],g[3][2])
        self.at('Gabrielle'); self.play(FadeIn(label('Girardeau and colleagues · 2009',0,3.25,30)),run_time=.25)
        self.at('Only the ripple'); self.play(FadeIn(g[2]),FadeIn(g[3][1]),FadeIn(g[4]),run_time=.3)
        self.at('group was impaired'); self.play(Indicate(g[1],color=RED,scale_factor=1.02),run_time=.2)
        self.finish()


class S19(TimedScene):
    def construct(self):
        g=results(); self.add(g)
        self.at('So the stimulation alone')
        rings=VGroup(*[SurroundingRectangle(g[i],color=GOLD,buff=.12) for i in (1,2)])
        same=label('same stimuli',0,.15,26,GOLD)
        self.play(Create(rings),FadeIn(same),run_time=.25)
        self.at('the deficit')
        # Transition the same bars left; restore text size after horizontal compression.
        left=g.copy(); texts=[m for m in left.get_family() if isinstance(m,Text)]
        widths=[m.width for m in texts]
        left.stretch(.53,0).shift(LEFT*3.2)
        for m,w in zip(texts,widths): m.stretch_to_fit_width(w)
        left[0][2].become(label('next-day performance',-3.2,2.5,26))
        left[3][2].become(label('qualitative comparison',-3.2,-3.45,26,GREY))
        left[3][0].become(label('ripple-cut',-4.58,-2.55,26,RED))
        left[3][1].become(label('delayed',-1.82,-2.55,26,PURPLE))
        left[4][1].become(label('not impaired',-1.82,1.65,26,PURPLE))
        l=small_ladder()
        self.play(Transform(g,left),FadeOut(rings),FadeOut(same),FadeIn(l),run_time=.25)
        ripple_note=label('ripple activity\nturned off',3.3,-2.65,28,RED)
        self.play(l[3][0].animate.set_stroke(RED),FadeIn(ripple_note),run_time=.15)
        self.finish()


class S20(TimedScene):
    def construct(self):
        old=wave(y=2.15,width=6,gain=1).shift(LEFT*2.8); self.add(old)
        self.at('Another group went'); self.play(FadeIn(label('Fernández-Ruiz and colleagues · 2019',0,3.3,28)),run_time=.2)
        self.at('Prolonging ripples')
        ghost=old.copy().set_stroke(GREY,opacity=.45); self.add(ghost)
        self.play(Transform(old,wave(y=2.15,width=6,kind='long',gain=1).shift(LEFT*2.8)),FadeIn(label('ripple prolonged',-2.8,2.85,28,YELLOW)),run_time=.35)
        self.at('in awake rats'); self.play(FadeIn(maze(-4.4,-1.8)),FadeIn(label('awake',-4.4,-3.05,28)),FadeIn(label('awake',-5.6,2.65,26)),run_time=.25)
        self.at('improved')
        bars=VGroup(Line([-2.5,-2.65,0],[.9,-2.65,0],color=GREY),Rectangle(width=.8,height=1.1,color=GREY,fill_opacity=.5).move_to([-1.8,-2.1,0]),Rectangle(width=.8,height=1.9,color=GREEN,fill_opacity=.7).move_to([.1,-1.7,0]),label('control',-1.8,-3.05,26),label('prolonged',.1,-3.05,26,GREEN),label('working memory',-1,-.55,26))
        l=small_ladder(3.1,.4)
        self.play(FadeIn(bars),FadeIn(l),run_time=.2)
        self.play(l[2][0].animate.set_stroke(GREEN),run_time=.1)
        self.finish()


class S21(TimedScene):
    def construct(self):
        tr=wave(y=1.5,width=10,kind='long',gain=.75)
        self.add(tr,maze(),label('awake · working memory',-3.4,-2.95,28))
        self.at('That tested awake ripples'); self.play(tr.animate.set_stroke(opacity=.2),run_time=.2)
        self.at('not consolidation during sleep')
        sleep=VGroup(rat(3,-1.2,1.5,True),label('z z z',3,.1,28),label('sleep: not tested',3,-2.95,28,RED),Line([1.2,-.3,0],[4.8,-2.2,0],color=RED,stroke_width=6))
        self.play(FadeIn(sleep),run_time=.3); self.finish()


class S22(TimedScene):
    def construct(self):
        events=VGroup(*[wave(y=y,width=10,gain=1) for y in (2.4,.55,-1.3)])
        seq=VGroup()
        routes=[(1,2,3,4),(4,2,1,3),(2,4,3,1)]
        for y,route in zip((2.4,.55,-1.3),routes):
            points=[np.array([-2.55+.5*i,y-.26-.07*i,0]) for i in range(4)]
            seq.add(VGroup(*[Line(a,b,color=YELLOW,stroke_width=3) for a,b in zip(points,points[1:])]))
            for point,n in zip(points,route):
                seq.add(VGroup(Dot(point,radius=.18,color=YELLOW),label(str(n),point[0],point[1],22,BG)))
        self.add(events,seq)
        self.at('One limit remains'); self.play(FadeIn(label('one limit',0,3.3,30,GOLD)),run_time=.2)
        self.at('Cutting ripples removes')
        cut=Line([-4,2.9,0],[.1,-2.9,0],color=RED,stroke_width=12)
        self.play(Create(cut),events.animate.set_stroke(opacity=.3),seq.animate.set_opacity(.25),run_time=.3)
        self.at('activity in general'); note=label('ripple-linked activity removed together',0,-3.45,28,RED); self.play(FadeIn(note),run_time=.2)
        self.at('not one'); self.play(Transform(note,label('not one specific route',0,-3.45,30,GOLD)),run_time=.2)
        self.finish()


class S23(TimedScene):
    def construct(self):
        g=ladder(); self.add(g)
        self.at('from correlation'); self.play(g[1][0].animate.set_stroke(GOLD),run_time=.2)
        self.at('to perturbation'); a=climb(g); self.play(GrowArrow(a),g[3][0].animate.set_stroke(RED),run_time=.25)
        self.at('Ripple linked activity'); self.remove(g,a); self.add(takeaway())
        self.finish()


class S24End(EndCard):
    LINE=END_LINE
    def construct(self):
        self.add(takeaway()); self.play(FadeIn(label('biochemistrypedia.com',0,-1,26,TEAL)),run_time=.3)
        self.wait(max(.01,self.narration_s-.3))
