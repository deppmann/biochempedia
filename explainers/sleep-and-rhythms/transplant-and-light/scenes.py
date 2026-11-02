"""Chapter 2. Idealized actograms; computed delayed-feedback and temperature curves.
COLOR MAP: BLUE=CLOCK-BMAL1/cold water; ORANGE=PER-CRY;
TEXT=DNA; TEAL=SCN/melanopsin/tract; PURPLE=internal time;
YELLOW=light/shifts; PINK=rods/cones; GREEN=target/activation;
RED=lesion/inhibition/hot water; GREY=external day/structure.
"""
import numpy as np
from bp_style import *
from bp_style import SpokenScene as PipelineSpokenScene

PURPLE='#B58CD9'
ORANGE='#F29E4C'
PINK='#E879A8'
DNA=TEXT

class SpokenScene(PipelineSpokenScene):
    # Keep diagnostic output in render scratch, not the chapter's deliverables.
    def at(self, phrase, lead=.2, nth=0):
        target=self.t_of(phrase,nth)-lead
        rest=target-self.elapsed()
        if rest>.02: self.wait(rest)


def bchip(text,color=BLUE,size=28,**kw):
    c=chip(text,color,size=size,**kw)
    back=RoundedRectangle(corner_radius=.14,width=c[0].width,height=c[0].height,
                          stroke_width=0,fill_color=BG,fill_opacity=1).move_to(c)
    return VGroup(back,*c)

def arr(a,b,color=GREY,w=5):
    return Arrow(a,b,buff=0,color=color,stroke_width=w,tip_length=.2,
                 max_tip_length_to_length_ratio=.35)

def tbar(a,b):
    a,b=np.array(a,float),np.array(b,float)
    d=(b-a)/np.linalg.norm(b-a); p=np.array([-d[1],d[0],0])*.3
    return VGroup(Line(a,b,color=RED,stroke_width=5),Line(b-p,b+p,color=RED,stroke_width=7))

def heading(text,color=TEXT): return T(text,32,color).move_to([0,3.15,0])

def lamp(center,scale=1):
    c=Circle(.27*scale,color=YELLOW,fill_opacity=.45,stroke_width=3)
    r=VGroup(*[Line(UP*.4*scale,UP*.58*scale,color=YELLOW,stroke_width=3).rotate(k*PI/4,about_point=ORIGIN) for k in range(8)])
    return VGroup(c,r).move_to(center)

def breathe(sun):
    # A subtle continuous light cue keeps the narrated holds visually alive.
    halo=Circle(sun[0].radius*1.7,color=YELLOW,stroke_width=0,
                fill_opacity=.12).move_to(sun[0])
    halo.add_updater(lambda m,dt:m.set_fill(opacity=.10+.07*np.sin(TAU*getattr(m,'pulse_t',0)/2)))
    def advance(m,dt): m.pulse_t=getattr(m,'pulse_t',0)+dt
    halo.add_updater(advance)
    sun.add_to_back(halo)
    return sun


def actogram(period=24,scattered=False,width=10.8,height=4.6,center=(0,0,0),rows=12,lesion=None,color=PURPLE,axis=True):
    """Double-plot one continuous 0.5 h sampled signal, modulo its period.
    Uniform seeded events illustrate arrhythmia, not measured experimental data.
    """
    grid,marks=VGroup(),VGroup(); rng=np.random.default_rng(73)
    for r in range(rows):
        y=height/2-r*height/(rows-1)
        grid.add(Line([-width/2,y,0],[width/2,y,0],color=GREY,stroke_opacity=.22,stroke_width=1))
        random=scattered or (lesion is not None and r>=lesion)
        events=rng.random(144)<.2 if random else None
        row=VGroup()
        for j in range(96):
            absolute=r*24+j*.5
            # Seed per absolute sample so both daily panels describe the same signal.
            active=(np.random.default_rng(73000+int(absolute*2)).random()<.2) if random else ((absolute-12)%period<5)
            if active:
                x=-width/2+width*(j+.5)/96
                row.add(Line([x,y-.075,0],[x,y+.075,0],color=color,stroke_width=3))
        marks.add(row)
    labels=VGroup()
    if axis:
        for h in (0,24,48): labels.add(M(str(h),26,GREY).move_to([-width/2+width*h/48,-height/2-.28,0]))
        labels.add(T('clock time (h)',26,GREY).move_to([0,-height/2-.68,0]))
        labels.add(T('days',26,GREY).rotate(PI/2).move_to([-width/2-.48,0,0]))
    return VGroup(grid,marks,labels).shift(np.array(center))

def hamster(center,scale=.65):
    head=Ellipse(width=1.6,height=1.3,color=GREY,fill_opacity=.1)
    ears=VGroup(*[Circle(.25,color=GREY,fill_opacity=.1).move_to([x,.6,0]) for x in (-.55,.55)])
    eyes=VGroup(*[Dot([x,.12,0],radius=.045,color=TEXT) for x in (-.32,.32)])
    nose=Triangle(color=GREY,fill_opacity=1).scale(.09).rotate(PI).move_to([0,-.25,0])
    return VGroup(head,ears,eyes,nose).scale(scale).move_to(center)

def graft_stage(restored=False,question=True):
    host=hamster([-5,1.6,0]); donor=hamster([-5,-.75,0])
    labels=VGroup(T('host: wild type',26).move_to([-4.8,2.55,0]),T('donor: tau/tau',26,PURPLE).move_to([-4.8,-1.6,0]),T('about 20 h',26,PURPLE).move_to([-4.8,-2.03,0]))
    socket=RoundedRectangle(width=1.2,height=.5,corner_radius=.1,color=TEAL).move_to([-5,.72,0])
    tissue=bchip('graft',TEAL,26,pad=.12).move_to(socket if restored else [-3.65,-.75,0])
    cross=Cross(socket,stroke_color=RED,stroke_width=5)
    if restored: cross.set_opacity(0); socket.set_opacity(0)
    arrow=arr([-3.65,-.4,0],[-4.4,.72,0],TEAL)
    data=actogram(20,scattered=not restored,width=7.8,height=4.25,center=[1.75,-.12,0],rows=10)
    q=heading('Whose period comes back?' if question else 'Returned rhythm: about 20 h',YELLOW if question else PURPLE)
    note=T('activity persists · rhythm gone' if not restored else 'Ralph and colleagues, 1990',26,GREY).move_to([1.5,2.55,0])
    mini=actogram(20,width=2.2,height=.7,center=[-4.85,-2.7,0],rows=5,axis=False)
    return VGroup(host,donor,labels,socket,tissue,cross,arrow,data,q,note,mini)

def countdown(scene,center):
    bg=Circle(.33,color=GREY,stroke_width=3).move_to(center)
    ring=Arc(radius=.33,start_angle=PI/2,angle=TAU,color=YELLOW,stroke_width=6).move_arc_center_to(center)
    scene.add(bg,ring)
    scene.play(Uncreate(ring),run_time=5,rate_func=linear)


def cell_stage(on=False,wide=False,bound=False):
    # A focused nucleus view; cytoplasm is opened only when proteins accumulate.
    nuc=RoundedRectangle(width=11.8,height=4.6 if wide else 5.7,corner_radius=.5,color=GREY,fill_opacity=.05).move_to([0,1 if wide else 0,0])
    nl=T('nucleus',28,GREY).move_to([-4.7,2.7 if wide else 2.35,0])
    dna=Line([-5,-.2,0],[5,-.2,0],color=DNA,stroke_width=5)
    eb=bchip('E-box',DNA,28).move_to([-2.7,-.2,0])
    genes=bchip('Per and Cry genes',GREEN if on else GREY,28).move_to([2.7,-.2,0])
    pair=VGroup(bchip('CLOCK',BLUE),bchip('BMAL1',BLUE)).arrange(RIGHT,buff=.1).move_to([-2.7,.72,0])
    # Contact stems make binding to the E-box visible.
    stems=VGroup(*[Line([x,.35,0],[x,.12,0],color=BLUE,stroke_width=4) for x in (-3.2,-2.2)])
    drive=arr([-.9,-.2,0],[.6,-.2,0],GREEN if on else GREY)
    pc=VGroup(bchip('PER',ORANGE),bchip('CRY',ORANGE)).arrange(RIGHT,buff=.12).move_to([-2.7,1.9,0] if bound else [2.7,-2.4,0])
    bar=tbar([-2.7,1.53,0],[-2.7,1.15,0])
    bl=T('brake',28,RED).move_to([-.5,1.9,0])
    if not wide:
        dna.shift(DOWN*1.4); eb.shift(DOWN*1.4); genes.shift(DOWN*1.4)
        pair.move_to([-2.7,.1,0])
        stems=VGroup(*[Line([x,-.3,0],[x,-1.22,0],color=BLUE,stroke_width=5) for x in (-3.2,-2.2)])
        drive.shift(DOWN*1.4)
        bar=tbar([-2.7,1.53,0],[-2.7,.52,0])
        nl.move_to([-4.7,2.55,0])
    base=VGroup(nuc,nl,dna,eb,genes,pair,stems,drive)
    return base,pc,bar,bl


def delayed_feedback(a=1.,K=.5,n=6,d=.35,tau=3.,T_end=96.,dt=.01):
    N,lag=int(T_end/dt),int(tau/dt); x=np.zeros(N); x[0]=.05
    for i in range(1,N):
        xd=x[i-1-lag] if i-1-lag>=0 else .05
        x[i]=x[i-1]+dt*(a/(1+(xd/K)**n)-d*x[i-1])
    return np.arange(N)*dt,x

def shower_data():
    # The same Hill-repression model drives the analogy, with a transport delay
    # prepended. Dimensionless temperature, not a fitted plumbing experiment.
    t,x=delayed_feedback(T_end=42)
    tm=np.arange(0,45,.01)
    return tm,np.interp(tm-3,t,x,left=.05)

def shower(small=False):
    pts=[(-5,-1),(-5,1.6),(-3.5,1.6),(-3.5,.3),(-2,.3),(-2,1.6),(-.5,1.6),(-.5,.3),(1,.3),(1,1.6),(3,1.6),(3,.7)]
    pipe=VMobject(color=GREY,stroke_width=11).set_points_as_corners([np.array([x,y,0]) for x,y in pts])
    tap=VGroup(Circle(.35,color=GREY),Line([-.3,0,0],[.3,0,0],color=TEXT,stroke_width=6)).move_to([-5,-1,0])
    head=Arc(radius=.6,start_angle=0,angle=PI,color=GREY,stroke_width=8).move_to([3,.5,0])
    water=VGroup(*[Line([2.55+i*.22,.1,0],[2.55+i*.22,-2.1,0],color=BLUE,stroke_width=4) for i in range(5)])
    g=VGroup(pipe,tap,head,water)
    if small: g.scale(.43).move_to([-3.6,1.15,0])
    return g

def shower_plot():
    ox,oy,w,h=-.6,-2.5,6.25,4.65
    t,x=shower_data(); target=.702 # replaced by the equilibrium root below
    roots=np.linspace(.01,2,20000); target=roots[np.argmin(abs(1/(1+(roots/.5)**6)-.35*roots))]
    def point(tm,val): return np.array([ox+w*tm/45,oy+h*val/2.1,0])
    axes=VGroup(Line([ox,oy,0],[ox+w,oy,0],color=GREY),Line([ox,oy,0],[ox,oy+h,0],color=GREY),T('water temperature',28,BLUE).move_to([2.5,2.65,0]),T('time · schematic model',26,GREY).move_to([2.5,-3.05,0]))
    guide=DashedLine(point(0,target),point(45,target),color=GREEN)
    axes.add(guide,T('target',26,GREEN).move_to([5.4,point(0,target)[1]+.25,0]))
    path=VMobject(color=BLUE,stroke_width=5).set_points_as_corners([point(tm,v) for tm,v in zip(t[::8],x[::8])])
    return axes,path,t,x,target

def live_shower(scene,start):
    s=shower(True); p,path,t,x,target=shower_plot(); tracker=ValueTracker(start)
    trace=VMobject(color=BLUE,stroke_width=5)
    trace.add_updater(lambda m:m.pointwise_become_partial(path,0,max(.0001,tracker.get_value()/45)))
    dot=Dot(radius=.085,color=BLUE)
    dot.add_updater(lambda m:m.move_to([-.6+6.25*tracker.get_value()/45,-2.5+4.65*np.interp(tracker.get_value(),t,x)/2.1,0]))
    # Trace and water share the SAME current model value.
    s[3].add_updater(lambda m:m.set_color(BLUE if np.interp(tracker.get_value(),t,x)<target else RED))
    scene.add(s,p,trace,dot)
    hot=T('hot',26,RED).move_to([-5.4,-.55,0]); cold=T('cold',26,BLUE).move_to([-5.4,.05,0])
    delay=VGroup(Line([-5.8,2.2,0],[-1.65,2.2,0],color=YELLOW),T('pipe delay',26,YELLOW).move_to([-3.7,2.65,0]))
    scene.add(hot,cold,delay)
    return VGroup(s,p,trace,dot,hot,cold,delay),tracker

def per_plot():
    t,x=delayed_feedback()
    minima=np.where((x[1:-1]<x[:-2]) & (x[1:-1]<=x[2:]))[0]+1
    start,end=minima[-3],minima[-2]
    t,x=t[start:end+1]-t[start],x[start:end+1]
    points=np.array([[-5.6+11.3*tm/t[-1],-1.5+3.9*v/2.1,0] for tm,v in zip(t,x)])
    axes=VGroup(Line([-5.6,-1.5,0],[5.7,-1.5,0],color=GREY),Line([-5.6,-1.5,0],[-5.6,2.45,0],color=GREY),T('PER level',30,ORANGE).move_to([-4.4,3.1,0]))
    path=VMobject(color=ORANGE,stroke_width=5).set_points_as_corners(points[::8])
    steps=VGroup()
    for name,f,y in [('transcription',.08,2.6),('translation',.28,2.95),('modification',.48,2.35),('nuclear entry',.68,2.95),('degradation',.88,2.35)]:
        point=points[int(f*(len(points)-1))]
        lab=T(name,26,GREY).move_to([point[0],y,0])
        steps.add(lab,Line(lab.get_bottom()+DOWN*.08,point+UP*.12,color=GREY,stroke_width=1.5))
    bracket=VGroup(Line([-5.6,-2.15,0],[5.7,-2.15,0],color=PURPLE),Line([-5.6,-1.95,0],[-5.6,-2.35,0],color=PURPLE),Line([5.7,-1.95,0],[5.7,-2.35,0],color=PURPLE),T('about a day',30,PURPLE).move_to([0,-2.7,0]),T('steep repression · schematic model',26,GREY).move_to([0,-3.35,0]))
    return axes,path,steps,bracket


def temperature_curve(shift=0):
    hours=np.linspace(18,36,241)
    return VMobject(color=PURPLE,stroke_width=4).set_points_as_corners([np.array([-5.55+(h-18)*11.1/18,-1.85-.5*np.cos(TAU*(h-30-shift*18/11.1)/24),0]) for h in hours])

def phase_stage(morning=False):
    def x(h):return -5.55+(h-18)*11.1/18
    title=heading('Example: habitual sleep 00:00–08:00',GREY)
    bar=Rectangle(width=11.1,height=1.05,color=GREY,fill_opacity=.12).move_to([0,1.45,0])
    wake=30.5 if morning else 32
    sleep=Rectangle(width=x(wake)-x(24),height=1.05,color=PURPLE,fill_opacity=.3).move_to([(x(24)+x(wake))/2,1.45,0])
    sl=T('sleep',28,PURPLE).move_to([(x(24)+x(wake))/2,1.45,0])
    ticks=VGroup(*[M(label,26,GREY).move_to([x(h),.55,0]) for h,label in [(18,'18:00'),(24,'00:00'),(30,'06:00'),(36,'12:00')]])
    low=VGroup(DashedLine([x(30),-2.4,0],[x(30),.18,0],color=PURPLE),DashedLine([x(30),.9,0],[x(30),2.35,0],color=PURPLE))
    ll=T('temperature low ≈06:00',26,PURPLE).move_to([2.1,2.65,0])
    hours=np.linspace(18,36,241)
    curve=temperature_curve()
    yl=T('body temperature',28,PURPLE).move_to([-3.7,-2.75,0])
    yaxis=arr([-6.1,-2.35,0],[-6.1,-1.05,0],GREY)
    sunhour=31 if morning else 23
    sun=breathe(lamp([x(sunhour),-.25,0],.62))
    ray=Line([x(sunhour),.13,0],[x(sunhour),.9,0],color=YELLOW,stroke_width=3)
    sunlabel=T('07:00 · up since 06:30' if morning else '23:00 · evening',26,YELLOW).move_to([3.65 if morning else -3.3,-.85,0])
    if morning: sunlabel=VGroup(T('07:00',26,YELLOW).move_to([3.8,-.65,0]),T('up since 06:30',26,YELLOW).move_to([3.8,-1.15,0]))
    if morning: title=heading('Same sleeper · awake early this morning',GREY)
    base=VGroup(title,bar,sleep,sl,ticks,low,ll,curve,yl,yaxis)
    light=VGroup(sun,ray,sunlabel)
    q=T('Earlier or later?',36,YELLOW).move_to([0,-3.15,0])
    return base,light,q


class S00Title(TitleCard):
    LESSON='Circadian Rhythms and Sleep'
    TITLE='A Clock You Can Transplant, and How Light Sets It'
    def construct(self):
        brand=T('BIOCHEMISTRYPEDIA',26,TEAL).move_to([0,2.5,0])
        lesson=T(self.LESSON.upper(),26,GREY).move_to([0,1.65,0])
        title=VGroup(T('A Clock You Can Transplant,',44,font=TITLE_FONT),T('and How Light Sets It',44,font=TITLE_FONT)).arrange(DOWN,buff=.3).move_to(ORIGIN)
        rule=Line([-1.2,-1.6,0],[1.2,-1.6,0],color=GOLD,stroke_width=4)
        self.play(FadeIn(brand),FadeIn(lesson),run_time=.4)
        self.play(FadeIn(title),Create(rule),run_time=.7); self.finish()

class S01Q1(SpokenScene):
    def construct(self):
        p=actogram(center=[0,-.05,0]); after=actogram(lesion=6,center=[0,-.05,0])
        title=heading('Rat · daily drinking and running')
        brain=VGroup(Ellipse(width=2.2,height=1.05,color=GREY),Arc(radius=.42,start_angle=-PI/2,angle=PI,color=GREY).stretch(.75,0)).move_to([4.9,2.9,0])
        pair=VGroup(*[Dot([4.65+i*.45,2.72,0],radius=.16,color=TEAL) for i in range(2)])
        lab=T('SCN pair',26,TEAL).move_to([2.8,2.9,0])
        title.move_to([-1.7,3.35,0])
        before=T('before\nlesion',26,GREY).move_to([6.1,1.4,0])
        self.add(p,brain,pair,lab,title,before)
        self.at('Destroy'); self.play(Create(Cross(pair,stroke_color=RED,stroke_width=5)),run_time=.45)
        self.at('one tiny pair'); self.play(Indicate(pair,color=RED),run_time=.7)
        self.at('above the optic'); self.play(Indicate(brain,scale_factor=1.08),run_time=.7)
        self.at('daily rhythms'); self.play(LaggedStart(*[Indicate(r,scale_factor=1.01) for r in p[1][:6]],lag_ratio=.1),run_time=1.3)
        self.at('vanish')
        marker=Line([-5.4,-.05,0],[5.4,-.05,0],color=RED,stroke_width=2)
        aft=T('after\nlesion',26,RED).move_to([6.1,-1.5,0])
        self.play(ReplacementTransform(p,after),Create(marker),FadeIn(aft),run_time=.7)
        self.at('Is that'); self.play(Transform(title,T('Clock or relay?',34,YELLOW).move_to([-1,3.25,0])),run_time=.5)
        self.finish()

class S02Relay(SpokenScene):
    def construct(self):
        p=actogram(lesion=6,width=5.8,height=4.65,center=[-3.1,-.05,0])
        site=Circle(.65,color=TEAL,fill_opacity=.08).move_to([3,1.35,0])
        fibers=VGroup(*[Line([.3,1.35+d,0],[5.8,1.35+d,0],color=GREY,stroke_width=3) for d in (-.2,0,.2)])
        sl=T('SCN',28,TEAL).move_to([3,2.35,0]); boxes=VGroup(bchip('clock?',PURPLE),bchip('relay?',GREY)).arrange(RIGHT,buff=.6).move_to([3,-.75,0])
        self.add(p,heading('Drinking continues; daily timing vanishes'),site,fibers,sl,boxes)
        cite=T('Stephan and Zucker, 1972',26,GREY).move_to([-3,2.65,0]); self.add(cite)
        self.at('The rats'); self.play(Indicate(p[1][7:]),run_time=1)
        self.at('Yet a lesion'); self.play(Indicate(site,color=RED),run_time=.6)
        self.at('cuts passing')
        cut=VGroup(*[Line(a,b,color=GREY,stroke_width=3) for d in (-.2,0,.2) for a,b in [([.3,1.35+d,0],[2.6,1.35+d,0]),([3.4,1.35+d,0],[5.8,1.35+d,0])]])
        self.play(Transform(fibers,cut),Create(Cross(site,stroke_color=RED)),run_time=.6)
        self.at('cannot tell')
        bracket=VGroup(Line([1.35,-1.45,0],[4.65,-1.45,0],color=YELLOW),Line([1.35,-1.45,0],[1.35,-1.15,0],color=YELLOW),Line([4.65,-1.45,0],[4.65,-1.15,0],color=YELLOW))
        note=T('a lesion alone\ncannot tell',28,YELLOW).move_to([3,-2.25,0])
        self.play(Create(bracket),FadeIn(note),run_time=.5); self.finish()

class S03Tau(SpokenScene):
    def construct(self):
        left=actogram(width=5.2,height=4.5,center=[-3.2,-.1,0]); right=actogram(20,width=5.2,height=4.5,center=[3.2,-.1,0])
        self.add(left,right,heading('A fast clock labels whose time it is'),T('wild type ≈24 h',28,PURPLE).move_to([-3.2,2.6,0]),T('tau/tau ≈20 h',28,PURPLE).move_to([3.2,2.6,0]))
        self.at('a mutation'); self.play(Indicate(right[1],scale_factor=1.01),run_time=.8)
        self.at('run fast'); self.play(LaggedStart(*[Indicate(r,scale_factor=1.05) for r in right[1]],lag_ratio=.07),run_time=1)
        self.at('which labels'); self.play(FadeIn(T('tau/tau: starts earlier each day',28,PURPLE).move_to([0,-3.65,0])),run_time=.4); self.finish()

class S04Graft(SpokenScene):
    def construct(self):
        g=graft_stage(); self.add(g[0],g[2][0],g[3],g[7],g[9],T('SCN',26,TEAL).move_to([-3.65,.72,0]))
        self.at('Destroy'); self.play(Create(g[5]),run_time=.5)
        self.at('or'); self.play(Indicate(g[3],color=TEAL),run_time=.6)
        self.at('then graft'); self.play(FadeIn(g[1]),FadeIn(g[2][1:]),FadeIn(g[4]),FadeIn(g[10]),run_time=.6)
        self.at('from a donor'); self.play(GrowArrow(g[6]),FadeOut(g[5]),g[3].animate.set_opacity(0),g[4].animate.move_to(g[3]),run_time=.9)
        self.at('whose period'); self.play(FadeIn(g[8]),run_time=.5); self.finish()

class S05Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; g=graft_stage(); g[5].set_opacity(0); g[4].move_to(g[3]); g[3].set_opacity(0); self.add(g)
        countdown(self,[6.15,3.15,0])

class S06Reveal(SpokenScene):
    def construct(self):
        g=graft_stage(True,False); g[7][1].set_opacity(0); self.add(g)
        ghost=actogram(24,width=7.8,height=4.25,center=[1.75,-.12,0],rows=10,color=GREY,axis=False)[1].set_opacity(.2)
        self.add(ghost)
        self.at('The'); g[7][1].set_opacity(1)
        self.play(LaggedStart(*[FadeIn(row) for row in g[7][1]],lag_ratio=.10),run_time=.65)
        self.at('donors'); self.play(Indicate(g[7][1],color=PURPLE,scale_factor=1.025),Indicate(g[10],color=PURPLE),run_time=1.1)
        self.at('A relay')
        note=T('relay would give ≈24 h',28,GREY).move_to([1.8,-3.55,0]); self.play(FadeIn(note),Indicate(ghost,scale_factor=1.01),run_time=1.4)
        self.at('A clock imposes'); self.play(Indicate(g[10],color=PURPLE),Indicate(g[7][1],scale_factor=1.015),run_time=1.1); self.finish()

class S07Loop1(SpokenScene):
    def construct(self):
        base,pc,bar,bl=cell_stage(); pair=base[5]; stems=base[6]; base.remove(pair,stems)
        self.add(base,heading('How does a cell keep time?',PURPLE))
        self.at('Two proteins'); pair[0].move_to([-4,1.5,0]); pair[1].move_to([.1,1.5,0]); self.play(FadeIn(pair),run_time=.6)
        self.at('pair up'); target=cell_stage()[0][5]
        bracket=VGroup(Line([-4.2,.8,0],[-1.2,.8,0],color=BLUE),T('pair',26,BLUE).move_to([-2.7,1.1,0]))
        self.play(Transform(pair,target),Create(stems),FadeIn(bracket),run_time=.45)
        self.at('switch on'); on=cell_stage(True)[0]; self.play(Transform(base[4],on[4]),Transform(base[-1],on[-1]),run_time=.65); self.finish()

class S08Loop2(SpokenScene):
    def construct(self):
        base,pc,bar,bl=cell_stage(True,True); focus=cell_stage(True)[0]; self.add(focus); self.play(ReplacementTransform(focus,base),run_time=.4); self.add(T('cytoplasm',28,GREY).move_to([-4.6,-3.2,0]))
        production=arr([2.7,-.65,0],[2.7,-1.9,0],ORANGE)
        extras=VGroup(*[bchip(n,ORANGE,26).move_to([x,-2.4,0]) for n,x in [('PER',-4),('CRY',-2.3),('PER',-.6)]])
        self.at('proteins'); self.play(GrowArrow(production),FadeIn(pc),run_time=.4)
        self.at('build up'); self.play(LaggedStart(*[FadeIn(c) for c in extras],lag_ratio=.15),run_time=.55)
        self.at('bind each other'); self.play(pc.animate.arrange(RIGHT,buff=.02).move_to([2.7,-2.4,0]),run_time=.4)
        self.at('and enter',lead=.7)
        # Turn the bound pair vertically so it fits the open corridor between
        # the activator and genes without shrinking any text.
        self.play(pc.animate.arrange(DOWN,buff=.02).move_to([0,-1.3,0]),run_time=.5)
        self.wait(.65)  # Visible pause at the nuclear envelope.
        self.play(pc.animate.move_to([0,1.9,0]),run_time=.55)
        self.play(pc.animate.arrange(RIGHT,buff=.02).move_to([2.7,1.9,0]),run_time=.35)
        self.finish()

class S09Loop3(SpokenScene):
    def construct(self):
        base,pc,bar,bl=cell_stage(True); pc.move_to([2.7,1.9,0]); wide=cell_stage(True,True)[0]; self.add(wide,pc)
        self.at('There they stop'); self.play(ReplacementTransform(wide,base),pc.animate.move_to([-2.7,1.9,0]),Create(bar),FadeIn(bl),run_time=.8)
        self.at('switch off'); off=cell_stage(False)[0]
        stop=tbar([-.45,1.5,0],[-.45,-1.6,0])
        self.play(Transform(base[4],off[4]),Transform(base[7],off[7]),Create(stop),run_time=.55)
        self.at('That is'); self.play(Indicate(bl,color=RED),run_time=.8); self.finish()

class S10Loop4(SpokenScene):
    def construct(self):
        base,pc,bar,bl=cell_stage(False,bound=True); stop=tbar([-.45,1.5,0],[-.45,-1.6,0]); self.add(base,pc,bar,bl,stop)
        self.at('broken down')
        fragments=VGroup(*[Square(.15,color=ORANGE,fill_opacity=.6).move_to([-3.5+i*.3,1.9+(i%2)*.15,0]) for i in range(6)])
        label=T('degraded',28,ORANGE).move_to([-4.6,1.9,0])
        self.play(ReplacementTransform(pc,fragments),FadeIn(label),FadeOut(bar),FadeOut(bl),FadeOut(stop),run_time=.6)
        self.at('come off'); self.play(fragments.animate.set_opacity(.3),run_time=.6)
        self.at('new cycle begins')
        arc=TipableVMobject(color=PURPLE,stroke_width=4).set_points_smoothly([np.array(p) for p in [(-2.7,1.98,0),(-.8,2.15,0),(4.7,1.8,0),(5.1,.6,0),(4.9,-.8,0),(3.2,-1.1,0)]]).add_tip(tip_length=.2)
        lab=bchip('about 24 h',PURPLE,30,pad=.12).move_to([1.3,2.1,0]); on=cell_stage(True)[0]
        self.play(Create(arc),FadeOut(fragments),FadeOut(label),FadeIn(lab),Transform(base[4],on[4]),Transform(base[7],on[7]),run_time=.9); self.finish()

class S11Shower1(SpokenScene):
    def construct(self):
        s=shower(); self.add(s,heading('Why cycle instead of settling?',YELLOW))
        self.add(T('cold',28,BLUE).move_to([-5.6,-1.6,0]),T('hot',28,RED).move_to([-4.4,-1.6,0]))
        self.at('Think of a shower'); self.play(Indicate(s[2],scale_factor=1.12),run_time=.5)
        self.at('long pipe'); self.play(ShowPassingFlash(s[0].copy().set_color(YELLOW),time_width=.8),run_time=1); self.finish()

class S12Shower2(SpokenScene):
    def construct(self):
        g,v=live_shower(self,0); note=T('still cold',30,BLUE).move_to([-3.8,-2,0]); self.add(note)
        self.at('turn toward hot'); self.play(g[0][1].animate.rotate(-PI/4),v.animate.set_value(1.3),run_time=.65,rate_func=linear)
        self.at('nothing changes'); self.play(v.animate.set_value(2),Indicate(g[-1],color=YELLOW),run_time=1.25,rate_func=linear)
        self.at('turn further'); self.play(g[0][1].animate.rotate(-PI/4),v.animate.set_value(3),run_time=.65,rate_func=linear)
        self.at('hot water arrives'); self.remove(note); self.play(v.animate.set_value(5),run_time=1.2,rate_func=linear)
        self.at('you have overshot'); self.play(v.animate.set_value(12),run_time=1.55,rate_func=linear); self.finish()

class S13Shower3(SpokenScene):
    def construct(self):
        g,v=live_shower(self,12)
        self.at('Feedback that is'); self.play(v.animate.set_value(23),run_time=2.2,rate_func=linear)
        self.at('keeps overshooting'); self.play(v.animate.set_value(45),run_time=1.5,rate_func=linear)
        self.at('In the clock'); axes,path,steps,bracket=per_plot()
        # Both old and new traces are visible during this crossfade.
        self.play(FadeOut(g),FadeIn(axes),FadeIn(path),run_time=.8)
        self.at('these steps together')
        self.play(FadeIn(steps),run_time=.3)
        self.at('set a cycle'); self.play(FadeIn(bracket),run_time=.3); self.finish()

class S14Light1(SpokenScene):
    def construct(self):
        center=np.array([-1.8,-.5,0]); r=2.3
        dial=Circle(r,color=PURPLE,stroke_width=5).move_to(center)
        ticks=VGroup(*[Line(center+(r-.15)*np.array([np.sin(TAU*h/24),np.cos(TAU*h/24),0]),center+r*np.array([np.sin(TAU*h/24),np.cos(TAU*h/24),0]),color=GREY,stroke_width=3) for h in range(24)])
        nums=VGroup(*[M(str(h),28,GREY).move_to(center+(r+.4)*np.array([np.sin(TAU*h/24),np.cos(TAU*h/24),0])) for h in (0,6,12,18)])
        hand=Line(center,center+UP*2.2,color=PURPLE,stroke_width=7)
        self.add(dial,ticks,nums,hand,heading('Near 24 h · not exactly 24 h',PURPLE))
        self.at('not exactly')
        ghosts=VGroup(); tags=VGroup()
        # Directional schematic of accumulating phase error, no assigned period.
        for i,a in enumerate((.18,.38,.58)):
            h=Line(center,center+2.2*np.array([np.sin(a),np.cos(a),0]),color=PURPLE,stroke_width=4,stroke_opacity=.55+i*.2)
            ghosts.add(h); tags.add(T('day '+str(i+1),26,PURPLE).move_to(center+[1.65+i*.75,2.15-i*.62,0]))
        self.play(LaggedStart(*[AnimationGroup(FadeIn(h),FadeIn(t)) for h,t in zip(ghosts,tags)],lag_ratio=.35),hand.animate.rotate(-.58,about_point=center),run_time=1.1)
        self.at('light resets'); sun=lamp([3.5,-1.5,0],1.2)
        pull=CurvedArrow(sun.get_left(),center+RIGHT*r,angle=-PI/5,color=YELLOW)
        self.play(FadeIn(sun),Create(pull),hand.animate.rotate(.58,about_point=center),run_time=.85); self.finish()

class S15Light2(SpokenScene):
    def construct(self):
        # Enlarged cross-section: incident light meets inner ganglion layer first.
        eye=Ellipse(width=6.1,height=5.6,color=GREY,fill_opacity=.035).move_to([-3.05,0,0])
        lens=Ellipse(width=.55,height=2.1,color=GREY).move_to([-5.4,0,0])
        cells=VGroup(*[Circle(.16,color=TEAL,fill_opacity=.3).move_to([-2.25,y,0]) for y in (-1,0,1)])
        rc=VGroup(*[RoundedRectangle(width=.18,height=.4,corner_radius=.05,color=PINK,fill_opacity=.2).move_to([-1.5,y,0]) for y in (-1.4,-.7,0,.7,1.4)])
        gang=T('ganglion cells',28,TEAL).move_to([-3.7,1.9,0]); lead=Line([-2.9,1.7,0],[-2.25,1.2,0],color=TEAL)
        halos=VGroup(*[Circle(.32,color=TEAL,stroke_width=0,fill_opacity=.18).move_to(c) for c in cells])
        rodhalos=VGroup(*[Ellipse(width=.44,height=.68,color=PINK,stroke_width=0,fill_opacity=.12).move_to(c) for c in rc])
        rodlabel=T('rods and cones',26,PINK).move_to([-3.6,-2.3,0]); rodline=Line([-2.2,-2.1,0],[-1.5,-1.65,0],color=PINK)
        scn=bchip('SCN',TEAL,38).move_to([4.7,0,0])
        route=DashedLine([-.8,0,0],[3.8,0,0],color=GREY)
        self.add(eye,lens,cells,rc,gang,lead,rodlabel,rodline,scn,route)
        self.at('retinal ganglion cells'); self.play(FadeIn(halos),cells.animate.set_fill(TEAL,.9),run_time=.55)
        self.at('sense light themselves'); self.play(GrowArrow(arr([-6,0,0],[-2.55,0,0],YELLOW)),run_time=.6)
        self.at('pigment called')
        mel=T('melanopsin',30,TEAL).move_to([.5,2.5,0]); ml=VMobject(color=TEAL).set_points_as_corners([np.array(v) for v in [(-.5,2.4,0),(-2.25,2.4,0),(-2.25,1.2,0)]])
        self.play(FadeIn(mel),Create(ml),run_time=.55)
        self.at('Their axons')
        ax=VGroup(*[VMobject(color=TEAL,stroke_width=4).set_points_as_corners([np.array([-2.1,y,0]),np.array([-.5,y*.4,0]),np.array([1.2,y*.14,0]),np.array([3.85,y*.14,0])]) for y in (-1,0,1)])
        nerve=RoundedRectangle(width=1,height=.65,corner_radius=.25,color=TEAL).move_to([1.2,0,0])
        self.play(Create(ax),FadeIn(nerve),FadeOut(route),run_time=.8)
        self.at('reach the clock')
        self.play(FadeIn(T('retinohypothalamic tract',28,TEAL).move_to([2.2,-1.2,0])),FadeIn(rodhalos),rc.animate.set_fill(PINK,.6),Transform(rodlabel,T('rods and cones help too',26,PINK).move_to([-3,-2.3,0])),run_time=.6); self.finish()

class S16Phase1(SpokenScene):
    def construct(self):
        base,light,q=phase_stage(); self.add(base)
        self.at('When the light'); self.play(ShowPassingFlash(base[7].copy().set_color(YELLOW),time_width=.4),run_time=1)
        self.at('biological evening'); self.play(FadeIn(light),run_time=.6)
        self.at('day is not over'); self.play(Indicate(light[0],scale_factor=1.15),run_time=.7)
        self.at('clock runs later')
        arrow=arr([1.85,2.15,0],[2.85,2.15,0],YELLOW)
        base[6].become(T('temperature low → later',26,PURPLE).move_to([2.1,2.65,0])); self.add(T('phase delay → later',32,YELLOW).move_to([0,-3.35,0]))
        self.play(base[5].animate.shift(RIGHT),Transform(base[7],temperature_curve(1)),GrowArrow(arrow),run_time=.65)
        self.add(T('direction only',26,GREY).move_to([-3.8,2.55,0])); self.finish()

class S17Phase2(SpokenScene):
    def construct(self):
        base,light,q=phase_stage(True); self.add(base,light)
        self.at('Light in your'); self.play(Indicate(light[0],scale_factor=1.15),run_time=.6)
        self.at('day began early'); self.play(ShowPassingFlash(base[7].copy().set_color(YELLOW)),run_time=.8)
        self.at('Which way'); self.play(FadeIn(q),run_time=.5); self.finish()

class S18Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; base,light,q=phase_stage(True); self.add(base,light,q)
        countdown(self,[4.6,-3.15,0])

class S19Phase3(SpokenScene):
    def construct(self):
        base,light,q=phase_stage(True); self.add(base,light)
        self.at('Earlier')
        arrow=arr([1.85,2.15,0],[.85,2.15,0],YELLOW)
        base[6].become(T('temperature low → earlier',26,PURPLE).move_to([2.1,2.65,0])); self.add(T('phase advance ← earlier',32,YELLOW).move_to([0,-3.35,0]))
        self.play(base[5].animate.shift(LEFT),Transform(base[7],temperature_curve(-1)),GrowArrow(arrow),run_time=.65)
        self.add(T('direction only',26,GREY).move_to([-3.8,2.55,0]))
        self.at('the switchover')
        original=DashedLine([1.85,-2.35,0],[1.85,.3,0],color=GREY)
        sw=T('delay | advance',28,YELLOW).move_to([2.7,-2.65,0]); self.play(Transform(base[6],T('baseline low ≈06:00',26,GREY).move_to([2.1,2.65,0])),FadeOut(base[5]),Transform(base[7],temperature_curve()),Create(original),FadeIn(sw),run_time=.6)
        self.at('daily low'); self.play(Indicate(Dot([1.85,-2.35,0],color=PURPLE),scale_factor=1.5),run_time=.7)
        self.at('early morning hours'); self.play(ShowPassingFlash(base[7].copy().set_color(YELLOW),time_width=.35),run_time=.8); self.finish()

class S20Drift(SpokenScene):
    def construct(self):
        # Two scales: a true 24 h timeline and an explicitly magnified endpoint.
        title=heading('Study mean: 24.18 h',PURPLE)
        d=arr([-5.6,1.8,0],[4.5,1.8,0],GREY)
        c=arr([-5.6,.8,0],[-5.6+10.1*24.18/24,.8,0],PURPLE)
        labels=VGroup(T('24.00 h day',28,GREY).move_to([-3.8,2.25,0]),T('24.18 h clock',28,PURPLE).move_to([-3.8,1.25,0]))
        zoom=VGroup(Rectangle(width=.55,height=1.45,color=GREY).move_to([4.55,1.3,0]),arr([4.55,.5,0],[3.1,.05,0],GREY))
        gap=Line([1,-.2,0],[5.2,-.2,0],color=PURPLE,stroke_width=8)
        magnify=T('0.18 h = 10.8 min · enlarged',26,PURPLE).move_to([3.1,-.65,0])
        self.add(title,d,c,labels,T('Czeisler and colleagues, 1999',26,GREY).move_to([0,2.7,0]))
        self.at('a little longer'); self.play(Create(zoom),Create(gap),FadeIn(magnify),run_time=.65)
        self.at('For a clock')
        calc=M('0.18 × 60 = 10.8 min',28,PURPLE).move_to([-2.9,-.45,0]); self.play(FadeIn(calc),FadeIn(M('24.18 − 24.00 = 0.18 h',26,PURPLE).move_to([-2.9,.1,0])),run_time=.5)
        # The morning/evening values are illustrative, not measured. Equal scale,
        # explicit ticks, and difference fixed by the computed intrinsic excess.
        u=.085; zero=.4; y=-1.7
        axis=VGroup(Line([-5.7,y,0],[5.7,y,0],color=GREY),*[VGroup(Line([zero+m*u,y-.08,0],[zero+m*u,y+.08,0],color=GREY),M(str(m),26,GREY).move_to([zero+m*u,y-.42,0])) for m in (-60,-30,0,30,60)])
        scale=T('minutes · idealized light shifts',26,GREY).move_to([0,-2.7,0]); self.add(axis,scale)
        morning=arr([zero,y+.15,0],[zero-40.8*u,y+.15,0],YELLOW)
        evening=arr([zero-40.8*u,y+.5,0],[zero-10.8*u,y+.5,0],ORANGE)
        join=DashedLine([zero-40.8*u,y+.15,0],[zero-40.8*u,y+.5,0],color=GREY)
        self.add(Line([zero,y,0],[zero,y+.15,0],color=GREY))
        self.at('morning advance'); self.play(GrowArrow(morning),FadeIn(T('morning, advance · 40.8 min',26,YELLOW).move_to([3.2,-1.25,0])),run_time=.55)
        self.at('outweigh the evening delay'); self.play(Create(join),GrowArrow(evening),FadeIn(T('evening, delay · 30 min',26,ORANGE).move_to([-2.4,-.82,0])),run_time=.6)
        self.play(FadeIn(T('net advance 10.8 min/day',30,YELLOW).move_to([0,-3.25,0])),run_time=.5); self.finish()

class S21Take(SpokenScene):
    def construct(self):
        self.add(heading('Keep this'))
        animal=hamster([-5.1,1.8,0],.55); tissue=bchip('SCN',TEAL,26,pad=.12).move_to([-3.7,1.8,0]); graft=VGroup(animal,tissue,arr([-4.4,1.8,0],[-4.1,1.8,0],TEAL))
        loop=Arc(radius=.55,start_angle=PI/4,angle=1.7*PI,color=PURPLE).add_tip(tip_length=.16).move_to([-4.5,-.35,0])
        sun=lamp([-4.5,-2.55,0],.9)
        self.at('The'); self.play(FadeIn(graft),FadeIn(T('SCN imposes its own period.',32,TEAL).move_to([.6,1.8,0])),run_time=.6)
        self.at('A gene loop'); self.play(Create(loop),FadeIn(T('A gene loop keeps its time.',32,PURPLE).move_to([.6,-.35,0])),run_time=.6)
        self.at('Daily light'); self.play(FadeIn(sun),FadeIn(T('Daily light keeps it on the day.',32,YELLOW).move_to([.6,-2.55,0])),run_time=.6); self.finish()

class S22End(EndCard):
    LINE='The SCN sets the period; light keeps it on the day.'
    def construct(self):
        lines=VGroup(T('The SCN sets the period;',40,font=TITLE_FONT),T('light keeps it on the day.',40,font=TITLE_FONT)).arrange(DOWN,buff=.3)
        self.play(FadeIn(lines),run_time=.8)
        self.play(FadeIn(T('biochemistrypedia.com',26,TEAL).move_to([0,-1.6,0])),run_time=.4); self.finish()
