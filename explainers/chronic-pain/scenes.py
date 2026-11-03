"""A Touch That Hurts — reviewed redraw.
COLOR MAP: BLUE withdrawal/reflex/threshold; TEAL innocuous touch;
ORANGE #F29E4C unpleasantness; PURPLE #B58CD9 BLA; YELLOW noxious;
GOLD tag/immune highlight; RED cuts; GREY neutral anatomy; TEXT signals.
Threshold trajectories interpolate the lesson's qualitative signature table,
not measurements. The inhibition plot solves its passive conductance equation.
"""
import numpy as np
from bp_style import *
from bp_style import SpokenScene as BaseSpokenScene
ORANGE='#F29E4C'
PURPLE='#B58CD9'

class SpokenScene(BaseSpokenScene):
    def at(self, phrase, lead=0, nth=0):
        # Cue at actual word onset; do not modify the existing pipeline sync log.
        rest=self.t_of(phrase,nth)-self.elapsed()-lead
        if rest>.02: self.wait(rest)


def label(s,x=0,y=3.15,size=32,color=TEXT):
    return T(s,size,color).move_to([x,y,0])

def centered_lines(text,x=0,y=0,size=30,color=TEXT):
    return VGroup(*[T(line,size,color) for line in text.split('\n')]).arrange(DOWN,buff=.14).move_to([x,y,0])

def arr(a,b,color=GREY,w=4):
    return Arrow(a,b,buff=.08,color=color,stroke_width=w,tip_length=.2)

def foot():
    ankle=Polygon([-1,1.8,0],[-.1,1.8,0],[.05,.05,0],[1.25,-.1,0],[1.25,-.48,0],[-1,-.48,0],color=BLUE,fill_color=BLUE,fill_opacity=.38)
    toes=VGroup(*[Line([x,-.15,0],[x+.08,-.43,0],color=BLUE) for x in (.65,.9)])
    return VGroup(ankle,toes)

def assay():
    # Macro view: the leg enters from above; the whole foot can lift freely.
    paw=foot().shift(UP*.25)
    mesh=VGroup(*[Line([-5.7,y,0],[5.7,y,0],color=GREY,stroke_width=2) for y in (-.3,-.55,-.8)],
                *[Line([x,-.3,0],[x+.45,-.8,0],color=GREY,stroke_width=2) for x in np.arange(-5.7,5.3,.4)])
    fil=VMobject(color=TEAL,stroke_width=4).set_points_as_corners([[.6,-2.8,0],[.6,-1.2,0],[.4,-.25,0]])
    return paw,mesh,fil

def bend(fil):
    return fil.copy().set_points_as_corners([[.6,-2.8,0],[.85,-1.25,0],[.4,-.25,0]])

def neuron():
    soma=Circle(.7,color=TEXT,fill_color=TEXT,fill_opacity=.12).move_to([-1.8,0,0])
    dend=VGroup(*[Line([-2.4,0,0],[-3.6,y,0],color=GREY,stroke_width=5) for y in (-.9,0,.9)])
    ax=Line([-1.1,0,0],[5,0,0],color=TEXT,stroke_width=5)
    return VGroup(soma,dend,ax)

def spikes(scene,line,count=3,seconds=1.1):
    # A persistent train: no sampled firing frame becomes a silent axon.
    if not hasattr(line,'train'):
        dots=VGroup(*[Dot(radius=.13,color=TEXT) for _ in range(count)])
        for i,dot in enumerate(dots):
            dot.phase=i/count
            dot.move_to(line.point_from_proportion(dot.phase))
            def advance(m,dt):
                m.phase=(m.phase+dt*.65)%1
                m.move_to(line.point_from_proportion(m.phase))
            dot.add_updater(advance)
        line.train=dots
        scene.add(dots)
    scene.wait(seconds)

def levels(lit=False):
    nodes=VGroup(*[chip(s,TEXT if lit else GREY,size=28,pad=.28).move_to([x,.1,0]) for x,s in [(-4.2,'Dorsal root\nganglion'),(0,'Dorsal horn\nspinal cord'),(4.2,'Brain')]])
    links=VGroup(arr(nodes[0].get_right(),nodes[1].get_left()),arr(nodes[1].get_right(),nodes[2].get_left()))
    return VGroup(links,nodes)

def large_levels(lit=False):
    c=GOLD if lit else GREY
    nodes=VGroup(*[VGroup(RoundedRectangle(width=3.5,height=2.5,corner_radius=.18,color=c,fill_color=c,fill_opacity=.22 if lit else .06).move_to([x,-.2,0]),centered_lines(name,x,-.2,32,c)) for x,name in [(-4.2,'Dorsal root\nganglion'),(0,'Dorsal horn\nspinal cord'),(4.2,'Brain')]])
    links=VGroup(*[arr(nodes[i].get_right(),nodes[i+1].get_left(),c) for i in (0,1)])
    return VGroup(links,nodes)

def question():
    h=label('Which would you pick?',size=38)
    doors=VGroup()
    for x,s in [(-3.3,'Alarm stuck on'),(3.3,'Nervous system\nchanged')]:
        box=RoundedRectangle(width=5.3,height=4.9,corner_radius=.15,color=GREY,fill_color=BG,fill_opacity=1).move_to([x,-.2,0])
        title=label(s,x,-1.55,30)
        if x<0:
            icon=VGroup(Arc(radius=.75,start_angle=0,angle=PI,color=ORANGE).move_to([x,.8,0]),Line([x-.8,.4,0],[x+.8,.4,0],color=ORANGE),Dot([x,.15,0],color=ORANGE),
                        *[Line([x+dx,1,0],[x+dx*1.2,1.4,0],color=ORANGE) for dx in (-1,1)])
        else:
            pts=[np.array([x+dx,y,0]) for dx,y in [(-1,.4),(0,1.3),(1,.3),(0,-.25)]]
            icon=VGroup(*[Line(pts[a],pts[b],color=TEXT,stroke_width=4) for a,b in [(0,1),(1,2),(0,3),(3,2),(1,3)]],*[Dot(p,radius=.13,color=TEXT) for p in pts])
        doors.add(VGroup(box,title,icon))
    return h,doors,label('?',y=-.2,size=60)

def threshold_plot():
    ax=Axes(x_range=[-1,5,1],y_range=[0,1.2,.2],x_length=10.2,y_length=5.3,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([.65,.05,0])
    words=VGroup(label('Withdrawal threshold',y=3.5,size=30,color=BLUE),label('Higher = needs more force',y=2.96,size=26),
        label('high',-5.5,2.15,26),label('low',-5.5,-2.1,26),label('Before',-4.45,-2.95,26),label('Days',-1.05,-2.95,26),label('Weeks',4.05,-2.95,26),label('Time after surgery',1.3,-3.48,26),label('Illustrative shape, not data',-3.8,-3.48,26,GREY))
    surgery=VGroup(DashedLine(ax.c2p(0,0),ax.c2p(0,1.08),color=GREY),label('surgery',-2.75,2.3,26))
    # Piecewise linear interpolation of the lesson's before/days/weeks states.
    def graph(points,color):
        p=np.array(points); t=np.linspace(p[0,0],p[-1,0],240)
        return VMobject(color=color,stroke_width=5).set_points_as_corners([ax.c2p(x,y) for x,y in zip(t,np.interp(t,p[:,0],p[:,1]))])
    sham=graph([(-1,1),(5,1)],GREY)
    inj=graph([(-1,1),(0,1),(1,.22),(5,.22)],BLUE)
    return ax,words,surgery,sham,inj,graph

class S00Title(TitleCard):
    LESSON='When Pain Persists'
    TITLE='A Touch That Hurts'

class S01Q(SpokenScene):
    def construct(self):
        self.add(label('Why does the same touch now make it pull away?',size=33))
        groups=[]
        for x,s in [(-3.3,'Before injury'),(3.3,'Days after injury')]:
            p,m,f=assay(); g=VGroup(p,m,f).scale(.48).move_to([x,-.15,0]); groups.append((p,m,f,g))
            self.add(g,label(s,x,2,30))
        self.add(label('Hind-paw close-up',y=-3.1,size=28,color=GREY))
        self.at('a light touch'); self.play(Indicate(groups[0][2],color=TEAL),run_time=.4)
        self.add(label('ignores',-3.3,-2.35,32,BLUE))
        self.at('makes it pull away'); self.play(groups[1][0].animate.shift(UP*.8),run_time=.4)
        self.add(label('pulls away',3.3,-2.35,32,BLUE)); self.finish()

class S02Floor(SpokenScene):
    def construct(self):
        p,m,f=assay(); self.add(p,m,label('Rat hind paw · close-up'),label('Before surgery',-3.5,.7,30),label('Wire-mesh floor',-3.5,-1.35,28,GREY))
        self.at('A thin filament'); self.play(Create(f),run_time=.5)
        self.add(label('filament',2.4,-2,28,TEAL),Line([1.55,-2,0],[.7,-2,0],color=TEAL))
        self.at('presses up against'); self.play(Transform(f,bend(f)),run_time=.5)
        self.at('The paw stays down'); self.play(FadeIn(label('Paw stays down',3.7,1,30,BLUE)),run_time=.3); self.finish()

class S03Sni(SpokenScene):
    def construct(self):
        self.add(label('Spared nerve injury'),label('nerve to the paw',2.6,2,28),Line([0,2.5,0],[0,1,0],color=GREY,stroke_width=12))
        branches=VGroup(*[Line([0,1,0],[x,-1.9,0],color=GREY,stroke_width=9) for x in (-3.6,0,3.6)])
        self.add(branches,*[chip('paw skin',GREY,28).move_to([x,-2.7,0]) for x in (-3.6,0,3.6)])
        self.at('are cut')
        for i in (0,1):
            a,b=branches[i].get_start(),branches[i].get_end()
            gap=VGroup(Line(a,a+.45*(b-a),color=GREY,stroke_width=9),Line(a+.62*(b-a),b,color=GREY,stroke_width=9))
            self.remove(branches[i]); self.add(gap,label('cut',(-3.6 if i==0 else 0),-.7,28,RED))
        self.at('one is spared'); self.play(branches[2].animate.set_color(TEAL),FadeIn(label('SPARED',4.5,-.5,32,TEAL)),run_time=.4); self.finish()

class S04Lift(SpokenScene):
    def construct(self):
        self.add(label('Days after injury · same filament',size=32))
        # Before/after comparison remains visible throughout the short payoff.
        for x,s,lift in [(-3.2,'Touch',False),(3.2,'Lift',True)]:
            p,m,f=assay(); g=VGroup(p,m,f).scale(.5).move_to([x,-.2,0]); self.add(g,label(s,x,-2.2,30,BLUE))
            if lift: p.shift(UP*.8); self.add(arr([4.5,-.1,0],[4.5,1,0],BLUE))
        self.at('the paw lift'); self.wait(.2); self.finish(); self.wait(.9)

class S05Allodynia(SpokenScene):
    def construct(self):
        self.add(label('Allodynia',y=3.15,size=46,color=TEAL))
        self.add(RoundedRectangle(width=5.6,height=4.8,corner_radius=.2,color=TEAL).move_to([-3.15,0,0]),
                 RoundedRectangle(width=5.6,height=4.8,corner_radius=.2,color=BLUE).move_to([3.15,0,0]))
        p=foot().scale(.7).move_to([3.15,.8,0])
        floor=VGroup(Line([1.4,0,0],[4.9,0,0],color=GREY),*[Line([x,0,0],[x+.2,-.2,0],color=GREY) for x in np.arange(1.4,4.8,.3)])
        filament=VMobject(color=TEAL,stroke_width=3).set_points_as_corners([[3.6,-1.35,0],[3.6,-.5,0],[3.35,0,0]])
        self.add(p,floor,filament)
        self.at('pain from a stimulus'); self.play(FadeIn(label('Pain from a stimulus\nthat normally\ndoes not hurt',-3.15,.2,34)),run_time=.4)
        self.at('A rat cannot tell us'); self.play(FadeIn(label('A rat cannot tell us',3.15,-1.9,28)),run_time=.3)
        self.at('the paw lift stands in'); self.play(p.animate.shift(UP*.55),FadeOut(filament),GrowArrow(arr([5.15,.2,0],[5.15,1.1,0],BLUE)),FadeIn(label('Paw lift: the rodent stand-in',y=-3.1,size=32,color=BLUE)),run_time=.4); self.finish()

class S06Threshold(SpokenScene):
    def construct(self):
        self.add(label('Increasing filament stiffness',size=34),label('✓ lift     × no lift',y=-3.3,size=28,color=BLUE))
        xs=(-4.5,-1.5,1.5,4.5); cols=VGroup()
        for j,x in enumerate(xs):
            cols.add(VGroup(Line([x,-.1,0],[x,2,0],color=TEAL,stroke_width=2+j*2),RoundedRectangle(width=1.4,height=.35,corner_radius=.13,color=BLUE).move_to([x,2.2,0])))
        self.at('The touches come'); self.play(LaggedStart(*[FadeIn(c) for c in cols],lag_ratio=.15),run_time=1)
        self.at('pressed over repeated trials')
        patterns=['××××','✓×××','✓×✓×','✓✓✓✓']
        for k in range(4):
            self.play(*[c[0].animate.shift(UP*.15) for c in cols],run_time=.12)
            self.play(*[c[0].animate.shift(DOWN*.15) for c in cols],*[FadeIn(label(patterns[j][k],x+(k-1.5)*.46,-1.05,34,BLUE)) for j,x in enumerate(xs)],run_time=.22)
        self.add(label('% lifts',-5.8,-1.95,26),*[label(s,x,-1.95,30,BLUE) for x,s in zip(xs,['0','25','50','100'])])
        self.at('half the time'); self.play(Create(RoundedRectangle(width=2.5,height=4.7,corner_radius=.15,color=BLUE).move_to([1.5,.15,0])),run_time=.4)
        self.at('That is the withdrawal threshold'); self.play(FadeIn(label('Withdrawal threshold · repeated trials',y=-2.65,size=28,color=BLUE)),run_time=.3); self.finish()

class S07Curve(SpokenScene):
    def construct(self):
        ax,w,s,sham,inj,g=threshold_plot(); self.add(ax,w,s)
        self.at('it stays flat'); self.play(Create(sham),FadeIn(label('Sham',5,2.15,28,GREY)),run_time=.6)
        self.at('In injured rats it falls'); self.play(Create(inj),FadeIn(label('Injured',4.7,-1.15,28,BLUE)),run_time=1.3); self.finish()

class S08Reverse(SpokenScene):
    def construct(self):
        ax,w,s,sham,inj,g=threshold_plot(); self.add(ax,w,s,sham,inj,label('Sham',5,2.15,28,GREY),label('Injured',5.2,-.4,26,BLUE))
        self.at('a treatment'); marker=VGroup(arr(ax.c2p(2,0),ax.c2p(2,.4),TEXT),label('Treatment',-1.2,-2.25,26),Line([-.15,-2.25,0],[.5,-2.25,0],color=TEXT)); self.play(FadeIn(marker),run_time=.3)
        # Keep the exact original curve and add a response after treatment.
        self.at('it pushes that curve back up'); self.remove(inj); self.add(g([(-1,1),(0,1),(1,.22),(2,.22)],BLUE)); rise=g([(2,.22),(2.8,.88)],BLUE)
        self.play(Create(rise),run_time=.65)
        peak=ax.c2p(2.8,.88)
        self.play(FadeIn(centered_lines('reversed the\nallodynia',4.6,.9,27,BLUE)),Create(Line([3.15,.9,0],peak,color=BLUE)),run_time=.25)
        self.at('often only for a while'); sag=g([(2.8,.88),(3.1,.88),(4.3,.28),(5,.22)],BLUE)
        # Erase only the future untreated segment; the pre-treatment curve is unchanged.
        self.play(Create(sag),FadeIn(label('often only for a while',3.45,-2.25,27,BLUE)),Create(Line([4.3,-2.02,0],ax.c2p(4.6,.25),color=BLUE)),run_time=.65); self.finish(); self.wait(.6)

class S09Others(SpokenScene):
    def construct(self):
        cards=[]
        data=[('Allodynia','Pain from a stimulus\nthat normally\ndoes not hurt',TEAL),('Hyperalgesia','More pain from\na stimulus that\nalready hurts',YELLOW),('Spontaneous pain','Pain with no\napplied stimulus',TEXT)]
        for x,(name,desc,c) in zip((-4.3,0,4.3),data):
            box=RoundedRectangle(width=4,height=5.5,corner_radius=.15,color=c).move_to([x,0,0])
            title=label(name,x,2,28,c); desc=label(desc,x,-.25,28)
            icon=VGroup(Ellipse(width=1.3,height=.25,color=GREY).move_to([x,.8,0]),Line([x,1.65,0],[x,1,0],color=c,stroke_width=3 if x<0 else 8))
            if x==0: icon.add(Polygon([x-.15,1.15,0],[x,1,0],[x+.15,1.15,0],color=YELLOW,fill_color=YELLOW,fill_opacity=1))
            if x==4.3: icon=VGroup(Ellipse(width=1.3,height=.25,color=GREY).move_to([x,.8,0]),label('no touch',x,1.5,26))
            cards.append(VGroup(box,title,desc,icon))
        self.add(cards[0]); self.at('Hyperalgesia'); self.play(FadeIn(cards[1]),run_time=.4)
        self.at('Spontaneous pain'); self.play(FadeIn(cards[2]),FadeIn(label('Hard to measure\nin animals',4.3,-1.85,26,GREY)),run_time=.4); self.finish()

class S10Reflex(SpokenScene):
    def construct(self):
        p,m,f=assay(); p.scale(.8,about_edge=DOWN)
        self.add(p,m,f,label('What is measured?',size=36))
        self.at('report a withdrawal threshold'); self.play(p.animate.shift(UP*.55),FadeOut(f),run_time=.4)
        tag=label('Withdrawal threshold',3.5,1.5,29,BLUE); self.add(tag,Line([1.35,.8,0],[1.75,1.3,0],color=BLUE))
        pin=VGroup(Polygon([5.3,-.6,0],[5.9,-.6,0],[5.75,-.9,0],[5.95,-1.05,0],[5.25,-1.05,0],[5.45,-.9,0],color=GOLD,fill_color=GOLD,fill_opacity=1),Line([5.6,-1.05,0],[5.3,-1.65,0],color=GOLD,stroke_width=6))
        self.at('which is a reflex'); self.play(FadeIn(label('A withdrawal reflex',3.5,.65,29,BLUE)),FadeIn(pin),run_time=.3)
        self.at('Hold on to that'); self.play(Indicate(pin,color=GOLD),FadeIn(label('Hold on to this',3.4,-1.2,30,GOLD)),run_time=.4); self.finish()


class S11Predict(SpokenScene):
    def construct(self):
        h,d,q=question(); self.add(h,d,q)
        self.at('an alarm that never switched off'); self.play(Indicate(d[0][2],color=ORANGE),run_time=.4)
        self.at('a changed nervous system'); self.play(Indicate(d[1][2],color=TEXT),run_time=.4); self.finish()

class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(*question(),label('Pause and decide',y=-3.15,size=28))
        ring=Circle(.32,color=GREY).move_to([0,-2.2,0]); progress=Arc(radius=.32,start_angle=PI/2,angle=-TAU,color=GOLD).move_to(ring)
        self.add(ring); self.play(Create(progress),run_time=5,rate_func=linear)

class S13Reveal(SpokenScene):
    def construct(self):
        h,d,q=question(); n=neuron().scale(1.25).move_to([0,-.1,0]); self.add(h,d,q)
        self.at('The answer is both'); both=label('Both',size=42); self.add(n); self.bring_to_back(n)
        self.play(Succession(FadeOut(h,run_time=.15),FadeIn(both,run_time=.15)),FadeOut(q),FadeIn(n),d[0].animate.shift(LEFT*8),d[1].animate.shift(RIGHT*8),run_time=.65); self.remove(d); h=both
        silent=label('Before: silent',y=-2.2,size=32,color=GREY); self.add(silent)
        self.at('After injury'); after=label('After injury',size=38)
        self.play(Succession(FadeOut(h,run_time=.15),FadeIn(after,run_time=.15)),FadeOut(silent),run_time=.35); h=after
        self.at('sensory neurons fire'); self.play(n[0].animate.set_fill(TEXT,.65),run_time=.2); spikes(self,n[2],seconds=.7)
        self.at('with no stimulus'); self.add(label('No applied stimulus',y=-1.4,size=32,color=TEAL)); spikes(self,n[2],seconds=1)
        self.at('the alarm wiring itself has changed'); changed=label('The alarm wiring has changed',size=36)
        self.play(Succession(FadeOut(h,run_time=.15),FadeIn(changed,run_time=.15)),n[2].animate.set_color(GOLD),n[1].animate.set_color(GOLD),run_time=.3); spikes(self,n[2],seconds=.9); self.finish()

class S14Idea(SpokenScene):
    def construct(self):
        m=large_levels(); self.add(m,label('The one idea',size=38))
        self.at('the one idea'); self.play(Indicate(m[0],color=GREY,scale_factor=1.03),run_time=.8)
        self.at('After a nerve injury'); self.play(FadeIn(label('After nerve injury, pain persists:',y=2,size=32)),run_time=.3)
        self.at('the rules of the system have changed'); self.add(label('The rules of the system have changed.',y=-2.3,size=36))
        self.play(LaggedStart(*[Indicate(n,color=GREY,scale_factor=1.04) for n in m[1]],lag_ratio=.3),run_time=1.3); self.finish()


class S15Ganglion(SpokenScene):
    def construct(self):
        n=neuron().stretch(1.4,1); self.add(n,chip('Dorsal root ganglion',TEXT,28).move_to([-1.8,2,0]),Line([-1.8,1.6,0],[-1.8,.75,0],color=TEXT),chip('Cord',GREY,28).move_to([5,1.8,0]),Line([5,1.4,0],[5,.1,0],color=GREY),label('Skin: no touch',-4,-1.7,30,TEAL),Line([-4,-1,0],[-4,1,0],color=GREY),Line([-4,0,0],[-3.6,0,0],color=GREY))
        self.at('sensory neurons'); self.play(n[0].animate.set_color(GOLD).set_fill(GOLD,.3),run_time=.3)
        self.at('make signals'); self.play(n[0].animate.set_fill(TEXT,.6),run_time=.2); spikes(self,n[2],seconds=.6)
        self.at('with no stimulus'); spikes(self,n[2],seconds=.9); self.finish()

class S16Cord(SpokenScene):
    def construct(self):
        self.add(label('Dorsal horn · in rats',size=36))
        # At Vth=-50, gE=(gL*(EL-Vth)+gI*(EI-Vth))/(Vth-EE).
        needed=lambda ei:((-65+50)+(ei+50))/-50
        y=lambda g:-2+5*g
        axis=VGroup(Line([-3.9,-2,0],[-3.9,1.9,0],color=GREY),Line([-3.9,-2,0],[.4,-2,0],color=GREY))
        threshold=DashedLine([-3.8,y(needed(-70)),0],[.4,y(needed(-70)),0],color=TEXT)
        tl=label('Needed input: 0.7',-1.6,2.4,28)
        newtl=label('Needed input: 0.3',-1.6,2.4,28)
        bar=Rectangle(width=1.1,height=2,color=TEAL,fill_color=TEAL,fill_opacity=.65).move_to([-2,-1,0])
        inhibition=Rectangle(width=.65,height=3.5,color=TEXT,fill_color=TEXT,fill_opacity=.85).move_to([-5.4,-.25,0])
        reduced=inhibition.copy().stretch(.3,1,about_edge=DOWN)
        below=label('Below threshold',3.5,-2.4,28,GREY)
        n=neuron().scale(.57).move_to([3.5,-.3,0])
        self.add(axis,threshold,tl,bar,inhibition,n,below,label('Inhibition',-5.3,2.4,26),label('Same touch: 0.4',-1.7,-2.65,28,TEAL),label('Pain-signalling\nneuron',3.5,1.7,30),label('Illustrative model, not a recording',y=-3.4,size=26,color=GREY))
        self.at('loses inhibition'); self.play(Transform(inhibition,reduced),threshold.animate.shift(DOWN*(y(.7)-y(needed(-50)))),FadeOut(tl),FadeIn(newtl),FadeOut(below),run_time=.8)
        self.at('In a simple model'); self.play(Indicate(inhibition,color=TEXT,scale_factor=1.04),run_time=.4)
        self.at('a light touch'); self.play(Indicate(bar,color=TEAL,scale_factor=1.04),run_time=.4)
        self.at('used to fall short'); self.play(Indicate(threshold,color=TEXT,scale_factor=1.02),run_time=.4)
        self.at('can then fire'); self.add(label('fires',3.5,-2.4,32)); self.play(n[0].animate.set_fill(TEXT,.8),run_time=.2); spikes(self,n[2],seconds=.7); self.finish()


class S17Immune(SpokenScene):
    def construct(self):
        self.add(label('In rodents',size=36))
        boxes=VGroup(*[chip(name,TEXT,34,pad=.45).move_to([x,.1,0]) for x,name in [(-3.2,'Dorsal root ganglion'),(3.2,'Dorsal horn')]])
        self.add(boxes,label('Ganglion compartment',-3.2,-1.1,28),label('Cord compartment',3.2,-1.1,28))
        cells=VGroup(*[Circle(.32,color=GOLD,fill_color=GOLD,fill_opacity=.5).move_to([x+dx,1.45,0]) for x in (-3.2,3.2) for dx in (-.7,.7)])
        stems=VGroup(*[Line([x+dx,1.12,0],[x+dx,.65,0],color=GOLD) for x in (-3.2,3.2) for dx in (-.7,.7)])
        self.at('immune cells'); self.play(FadeIn(cells),Create(stems),FadeIn(label('Immune cells',y=2.4,size=30,color=GOLD)),run_time=.4)
        self.at('help hold that change'); self.play(*[b[0].animate.set_color(GOLD).set_fill(GOLD,.2) for b in boxes],FadeIn(label('Help hold the change',y=-2,size=32)),run_time=.4)
        self.at('differ with sex and compartment'); self.play(FadeIn(label('Routes differ with sex and compartment',y=-3,size=30)),Indicate(cells,color=GOLD,scale_factor=1.06),run_time=.6); self.finish()


class S18Brain(SpokenScene):
    def construct(self):
        cord=chip('Spinal cord',GREY,30).move_to([-1,-1.4,0]); brain=chip('Brain',GREY,32).move_to([-1,1.9,0])
        touch=chip('Touch in',TEAL,28).move_to([-5,-1.4,0]); p=foot().scale(.5).move_to([3.5,-1.3,0])
        loop=VGroup(arr(touch.get_right(),cord.get_left(),BLUE),arr(cord.get_right(),[2.7,-1.4,0],BLUE),label('reflex: paw lifts',3.5,-2.8,30,BLUE))
        up=arr([-1.6,-.9,0],[-1.6,1.4,0],ORANGE); down=arr([-.4,1.4,0],[-.4,-.9,0],GREY,w=3)
        needle=Line([3.9,1.5,0],[3.45,1.95,0],color=ORANGE,stroke_width=5)
        dial=VGroup(Arc(radius=.8,start_angle=0,angle=PI,color=ORANGE).move_to([3.9,1.9,0]),needle,label('low',2.9,1.25,26,ORANGE),label('high',5,1.25,26,ORANGE),label('Unpleasantness',3.9,3.05,30,ORANGE),arr(brain.get_right(),[3,2,0],ORANGE))
        self.add(cord,brain,touch,p,loop)
        self.at('separate brain circuits'); self.play(brain[0].animate.set_color(TEXT).set_fill(TEXT,.4),brain[1].animate.set_color(TEXT),p.animate.shift(UP*.5),FadeIn(dial),GrowArrow(up),GrowArrow(down),FadeIn(label('to brain',-3,.4,28,ORANGE)),FadeIn(label('descending',1.25,.4,28)),run_time=.5)
        self.at('how unpleasant'); self.play(Transform(needle,Line([3.9,1.5,0],[4.4,2.05,0],color=ORANGE,stroke_width=5)),run_time=.7)
        self.at('apart from the reflex'); self.play(Indicate(loop,color=BLUE,scale_factor=1.02),run_time=.5)
        pulse=Dot(radius=.1,color=BLUE); pulse.phase=0
        def travel(m,dt):
            m.phase=(m.phase+dt*.65)%1
            m.move_to(loop[1].point_from_proportion(m.phase))
        pulse.add_updater(travel); self.add(pulse)
        self.finish(); self.wait(max(0,9-self.elapsed()))


class S19Scope(SpokenScene):
    def construct(self):
        self.add(label('Where the evidence comes from',size=36))
        for x in (-3.1,3.1): self.add(RoundedRectangle(width=5.6,height=3.9,corner_radius=.2,color=GREY).move_to([x,.35,0]))
        self.add(label('Rodents',-3.1,1.6,38),label('People',3.1,1.6,38))
        self.at('rodent nerve injury models'); self.play(FadeIn(centered_lines('Nerve-injury models\nLink-by-link in rats\nAcross different experiments',-3.1,-.1,27)),run_time=.4)
        self.at('In people'); self.play(Indicate(self.mobjects[4],color=GREY,scale_factor=1.02),run_time=.3)
        self.at('the evidence is association'); self.play(FadeIn(centered_lines('Association\nCausation not established',3.1,-.1,28)),run_time=.3)
        self.add(centered_lines('Not established here for nociplastic pain or arthritis.\nOngoing input and changed processing can coexist.',y=-2.6,size=28,color=GREY)); self.finish(); self.wait(1)

class S20Take(SpokenScene):
    def construct(self):
        m=large_levels(); self.add(m,label('The takeaway',size=36))
        cells=VGroup(*[Circle(.22,color=GOLD,fill_color=GOLD,fill_opacity=.6).move_to([x+dx,1.5,0]) for x in (-4.2,0) for dx in (-.55,.55)])
        dial=VGroup(Arc(radius=.48,start_angle=0,angle=PI,color=GOLD).move_to([4.2,1.5,0]),Line([4.2,1.25,0],[4.5,1.65,0],color=GOLD,stroke_width=4))
        stems=VGroup(*[Line([x+dx,1.27,0],[x+dx,1.05,0],color=GOLD) for x in (-4.2,0) for dx in (-.55,.55)])
        self.at('the alarm wiring changed'); self.play(Transform(m,large_levels(True)),FadeIn(cells),Create(stems),FadeIn(dial),run_time=.6)
        self.at('and so did the rules'); self.play(FadeIn(label('The wiring changed, and so did the rules.',y=-2.1,size=34)),run_time=.4)
        self.play(Indicate(m[0],color=GOLD,scale_factor=1.04),run_time=.7); self.finish()


class S21End(EndCard):
    LINE='The wiring changed, and so did the rules.'
