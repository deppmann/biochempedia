"""Pressure and the Clock — word-synchronised chapter 1.

COLOR MAP shared with scenes.old.py (retained for subsequent chapters):
BLUE #58C4DD = CLOCK–BMAL1; ORANGE #F29E4C = PER/CRY;
WHITE/TEXT = DNA; TEAL #3FB8C0 = light pathway and SCN;
PURPLE #B58CD9 = internal clock, circadian wake drive and levels;
YELLOW #F5D547 = light; PINK #E879A8 = rods/cones;
GREEN #83C167 = on; RED #FC6255 = inhibition/problem;
GREY #8B93A1 = external day, outlines and de-emphasis.
Chapter extension: ORANGE = Process S (distinct from clock; no PER/CRY here).
All model curves use the lesson's illustrative two-process equations:
dS/dt=(1-S)/18 awake, -S/4 asleep; levels .67/.17 +
.12*cos(2*pi*(clock_hour-17)/24). No measured data implied.
"""
import numpy as np
from bp_style import *

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E879A8"

# Opaque chips and arrows adapted from the reference animation.
def bchip(text, color=BLUE, size=24, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=.14, width=c[0].width, height=c[0].height,
                            stroke_width=0, fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)

def arr(a, b, color=GREY, w=5, tip=.22):
    return Arrow(a, b, buff=.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=.45)

def level(t, upper=True):
    return (.67 if upper else .17) + .12*np.cos(2*np.pi*(np.asarray(t)-17)/24)

def model(end=55, single=False, forced=False, dt=.025):
    t = np.arange(7, end+dt/2, dt)
    s = np.zeros(len(t)); s[0] = .23
    sleep = np.zeros(len(t), dtype=bool)
    state = False
    for i in range(1, len(t)):
        hi = (level(t[i-1])+level(t[i-1],False))/2 if single else level(t[i-1])
        lo = hi if single else level(t[i-1],False)
        if not forced:
            if state and s[i-1] <= lo: state=False
            elif not state and s[i-1] >= hi: state=True
        sleep[i] = state
        s[i] = s[i-1]*np.exp(-dt/4) if state else 1-(1-s[i-1])*np.exp(-dt/18)
    return t,s,sleep

# Keep cues tied to actual audio, without the pipeline's pre-wait diagnostic log.
class TimedScene(SpokenScene):
    def at(self, phrase, lead=.15, nth=0):
        target = max(0, self.t_of(phrase, nth)-lead)
        if target > self.elapsed()+.02:
            self.wait(target-self.elapsed())

class Plot(VGroup):
    def __init__(self, end=55, x=-5.35, y=-2.6, w=11.15, h=5.05, labels=True):
        super().__init__(); self.end=end; self.x=x; self.y=y; self.w=w; self.h=h
        self.add(Line(self.p(7,0),self.p(end,0),color=GREY),
                 Line(self.p(7,0),self.p(7,1),color=GREY))
        if labels:
            self.add(T('pressure · illustrative units',26,ORANGE).rotate(PI/2).move_to([x-.7,y+h/2,0]))
            hrs=[7,19,31,43,55] if end==55 else ([7,19,31,38] if end==38 else [7,19,31])
            for hr in hrs:
                self.add(Line(self.p(hr,0),self.p(hr,-.025),color=GREY),
                         T(f'{hr%24:02d}:00',26,GREY).move_to(self.p(hr,-.09)))
            self.add(T(f'time of day · {end-7} h shown',26,GREY).move_to([x+w/2,y-.9,0]))
    def p(self,t,s): return np.array([self.x+self.w*(t-7)/(self.end-7),self.y+self.h*s,0])
    def curve(self,t,s,color=ORANGE,width=5):
        return VMobject(color=color,stroke_width=width).set_points_as_corners([self.p(a,b) for a,b in zip(t,s)])
    def threshold(self,upper=True):
        t=np.linspace(7,self.end,500)
        return self.curve(t,level(t,upper),PURPLE,4)
    def bands(self,t,state):
        g=VGroup(); start=None
        for i,on in enumerate(state):
            if on and start is None: start=t[i]
            if start is not None and (not on or i==len(t)-1):
                end=t[i]; width=self.p(end,0)[0]-self.p(start,0)[0]
                if width>0:g.add(Rectangle(width=width,height=self.h,stroke_width=0,fill_color=PURPLE,fill_opacity=.10).move_to((self.p(start,0)+self.p(end,1))/2))
                start=None
        return g

def legend(lower=False):
    g=VGroup(T('Process S · pressure',28,ORANGE).move_to([-3.7,3.25,0]),
             T('upper level · fall asleep',26,PURPLE).move_to([2.8,3.25,0]))
    if lower:g.add(T('lower level · wake',26,PURPLE).move_to([2.8,2.72,0]))
    return g

def question1():return T('More time awake, less sleepy?',38,font=TITLE_FONT).move_to([0,-2.95,0])
def question2():return T('Every lost hour back?',48,font=TITLE_FONT).move_to([0,1.7,0])

def clock(hour=22,center=(-3,0,0),radius=1.7,color=GREY):
    c=np.array(center,float)
    face=Circle(radius=radius,color=color,stroke_width=4).move_to(c)
    ticks=VGroup(*[Line(c+radius*.86*np.array([np.sin(k*PI/6),np.cos(k*PI/6),0]),c+radius*np.array([np.sin(k*PI/6),np.cos(k*PI/6),0]),color=color) for k in range(12)])
    theta=hour*PI/6
    hand=Line(c,c+radius*.70*np.array([np.sin(theta),np.cos(theta),0]),color=PURPLE,stroke_width=7)
    return VGroup(face,ticks,hand,Dot(c,color=PURPLE,radius=.08))

def person(slump=False):
    hx,hy=(3.25,1.0) if slump else (3.0,1.65)
    return VGroup(Circle(radius=.34,color=GREY).move_to([hx,hy,0]),
        Line([hx,hy-.34,0],[2.9,-.6,0],color=GREY,stroke_width=8),
        Line([2.9,-.6,0],[4,-.6,0],color=GREY,stroke_width=8),
        Line([4,-.6,0],[4,-1.9,0],color=GREY,stroke_width=8),
        Line([hx,.45,0],[4.45,-.1,0],color=GREY,stroke_width=7))

def opening(hour=5,amount=.9,slump=True,phase='near dawn · 5 AM'):
    face=clock(hour,(-3.7,.45,0))
    meter=RoundedRectangle(width=.85,height=4.1,corner_radius=.12,color=GREY).move_to([.1,.3,0])
    fill=Rectangle(width=.63,height=3.85*amount,stroke_width=0,fill_color=ORANGE,fill_opacity=.8).move_to([.1,-1.65+3.85*amount/2,0])
    desk=VGroup(Line([2.5,-.1,0],[5.6,-.1,0],color=GREY,stroke_width=5),Line([5.3,-.1,0],[5.3,-2,0],color=GREY,stroke_width=5))
    return VGroup(face,meter,fill,T('sleepiness',28,ORANGE).move_to([.1,2.85,0]),person(slump),desk,
        T(phase,28,GREY).move_to([-3.7,2.85,0]),
        T('12',26,GREY).move_to([-3.7,1.72,0]),T('6',26,GREY).move_to([-3.7,-.85,0]))

def empty_bars():
    return VGroup(*[Rectangle(width=10.4,height=1.15,color=GREY,stroke_opacity=.25).move_to([0,y,0]) for y in [-.2,-2]])

def countdown(scene, pos=(0,-2.9,0)):
    ring=Circle(radius=.58,color=GREY).move_to(pos)
    arc=Arc(radius=.58,start_angle=PI/2,angle=TAU,color=TEAL,stroke_width=7).move_to(ring)
    scene.add(ring,arc)
    scene.play(Uncreate(arc,rate_func=linear),run_time=5)

class S00Title(TitleCard):
    LESSON='Circadian Rhythms and Sleep'
    TITLE='Pressure and the Clock'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON.upper(),26,GREY),T(self.TITLE,52,font=TITLE_FONT),Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.32)
        self.play(FadeIn(g),run_time=.4);self.finish()

class S01Q1(TimedScene):
    def construct(self):
        g=opening(22,.30,False,'evening · 10 PM');self.add(g)
        self.at('Stay up all night')
        # The label follows the same continuous hour value as the hand.
        hour=ValueTracker(22)
        center=g[0][0].get_center()
        g[0][2].add_updater(lambda hand: hand.put_start_and_end_on(center,center+1.19*np.array([np.sin(hour.get_value()*PI/6),np.cos(hour.get_value()*PI/6),0])))
        def time_label(label):
            minutes=int(round(hour.get_value()*60))
            h,m=divmod(minutes,60);h%=24
            text=('midnight · 12 AM' if h==0 and m==0 else f'{h%12 or 12}:{m:02d} '+('PM' if h>=12 else 'AM'))
            label.become(T(text,28,GREY).move_to([-3.7,2.85,0]))
        g[6].add_updater(time_label)
        self.play(hour.animate.set_value(29),rate_func=linear,run_time=1.25)
        g[0][2].clear_updaters();g[6].clear_updaters()
        self.at('near dawn')
        target=opening()
        self.play(Transform(g[2],target[2]),Transform(g[4],target[4]),Transform(g[6],target[6]),run_time=.65)
        self.finish()

class S02Q2(TimedScene):
    def construct(self):
        g=opening();self.add(g)
        self.at('By early afternoon')
        target=opening(14,.48,False,'early afternoon · 2 PM')
        self.play(Rotate(g[0][2],-3*PI/2,about_point=g[0][0].get_center()),Transform(g[6],target[6]),run_time=1.1)
        self.at('you feel better')
        self.play(Transform(g[2],target[2]),Transform(g[4],target[4]),run_time=.35)
        self.at('How can more');self.play(FadeIn(question1()),run_time=.4)
        self.finish()

class S03Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(opening(14,.48,False,'early afternoon · 2 PM'),question1());countdown(self, (5.7,-2.9,0))

class S04Clue(TimedScene):
    def construct(self):
        self.add(T('hours awake',38,GREY).move_to([0,3.15,0]))
        base=-2.25
        bars=VGroup(*[Rectangle(width=2,height=5*n/31,color=GREY,fill_color=GREY,fill_opacity=.35).move_to([x,base+2.5*n/31,0]) for x,n in [(-4,22),(-.8,31)]])
        self.at('time awake');self.play(GrowFromEdge(bars[0],DOWN),FadeIn(T('dawn · 22 h',28,GREY).move_to([-4,-2.85,0])),run_time=.5)
        self.at('the afternoon');self.play(GrowFromEdge(bars[1],DOWN),FadeIn(T('afternoon · 31 h',28,GREY).move_to([-.8,-2.85,0])),run_time=.5)
        q=T('?',110,PURPLE).move_to([3.6,.2,0])
        self.at('Something else changed');self.play(FadeIn(q),run_time=.3)
        self.at('a clock');self.play(FadeOut(q),FadeIn(clock(14,(3.6,.2,0),1.8,PURPLE)),run_time=.45)
        self.finish()

class S05Pressure(TimedScene):
    def construct(self):
        p=Plot(end=31);self.add(p,T('Illustrative model · not measurements',26,GREY).move_to([0,3.25,0]))
        # One build/drain demonstration with the exact awake/asleep equations.
        # Start high to show the awake exponential approaching its ceiling clearly.
        t=np.linspace(7,25,300);s=1-.55*np.exp(-(t-7)/18)
        u=np.linspace(25,31,130);v=s[-1]*np.exp(-(u-25)/4)
        self.at('sleep pressure');self.play(FadeIn(T('Process S',30,ORANGE).move_to([-3,2.75,0])),run_time=.3)
        self.at('It builds');self.play(Create(p.curve(t[:120],s[:120]),rate_func=linear),run_time=1.4)
        self.at('then more slowly')
        self.play(Create(DashedLine(p.p(7,1),p.p(31,1),color=GREY)),FadeIn(T('ceiling',26,GREY).move_to([4.7,2.8,0])),Create(p.curve(t[119:],s[119:]),rate_func=linear),run_time=1)
        self.at('While you sleep')
        band=p.bands(np.array([25,31]),np.array([True,True]))
        self.play(FadeIn(band),FadeIn(T('asleep',26,PURPLE).move_to([4.5,-2.1,0])),Create(p.curve(u,v),rate_func=linear),run_time=1)
        self.finish()

class S06Clock1(TimedScene):
    def construct(self):
        room=RoundedRectangle(width=11.8,height=5.8,corner_radius=.15,color=GREY).move_to([0,-.25,0])
        door=Rectangle(width=1.5,height=3.5,color=GREY).move_to([-4.4,-1.3,0])
        window=VGroup(Rectangle(width=1.3,height=1.2,color=GREY),Line([-.7,-.7,0],[.7,.7,0],color=RED,stroke_width=5)).move_to([3.9,-1.2,0])
        head=Circle(radius=.65,color=GREY).move_to([-.7,1,0])
        body=VGroup(Line([-.7,.35,0],[-.7,-1.3,0],color=GREY,stroke_width=7),Line([-.7,-1.3,0],[-1.5,-2.6,0],color=GREY,stroke_width=7),Line([-.7,-1.3,0],[.1,-2.6,0],color=GREY,stroke_width=7))
        self.add(room,door,Dot([-3.9,-1.3,0],color=GREY),head,body,window,T('no windows',26,GREY).move_to([3.9,-2.25,0]))
        c=clock(9,(3.1,.95,0),1.25,PURPLE)
        self.at('a clock in')
        self.play(FadeIn(c),Create(Line([0,1,0],[1.7,1,0],color=PURPLE)),FadeIn(T('Process C: circadian clock, about 24 h',30,PURPLE).move_to([0,3.15,0])),run_time=.4)
        self.at('keeps a cycle');self.play(Rotate(c[2],-TAU,about_point=[3.1,.95,0],rate_func=linear),run_time=1.3)
        self.finish()

class S07Clock2(TimedScene):
    def construct(self):
        p=Plot(end=31,labels=False);self.add(p,T('circadian wake drive · illustrative units',30,PURPLE).move_to([.7,3.2,0]),clock(17,(-5.4,3.15,0),.42,PURPLE),arr([-4.85,3.15,0],[-3.7,3.15,0],PURPLE,w=3,tip=.14))
        for hr in [7,19,31]:self.add(T(f'{hr%24:02d}:00',26,GREY).move_to(p.p(hr,-.09)))
        self.add(T('time of day · 24 h shown',26,GREY).move_to([0,-3.5,0]))
        t=np.linspace(7,31,400);v=.5+.37*np.cos(TAU*(t-17)/24)
        self.at('toward waking');self.play(Create(p.curve(t,v,PURPLE)),run_time=.7)
        self.at('late afternoon and evening')
        peak=p.p(17,.87)
        self.play(FadeIn(Dot(peak,color=PURPLE)),FadeIn(T('late afternoon / evening',28,PURPLE).move_to([-.5,2.65,0])),run_time=.4)
        self.at('early morning',lead=0)
        trough=p.p(29,.13)
        self.play(FadeIn(Dot(trough,color=PURPLE)),FadeIn(T('early morning · 05:00',28,PURPLE).move_to([3.9,.25,0])),Create(Line(trough, [3.9,-.05,0],color=PURPLE)),run_time=.4)
        self.finish()

class S08Pic1(TimedScene):
    def construct(self):
        p=Plot();t,s,st=model();k=np.flatnonzero(st)[0]
        self.add(p,p.curve(t[:k],s[:k]),legend()[0])
        self.at('upper wavy line');self.play(Create(p.threshold()),run_time=.9)
        self.at('before you fall asleep');self.play(FadeIn(legend()[1]),FadeIn(Dot(p.p(t[k],s[k]),color=ORANGE,radius=.12)),run_time=.4)
        self.finish()

def moon(pos,r=.17):
    # One closed crescent path: no background disc can erase a graph trace.
    outer=[r*np.array([np.cos(a),np.sin(a),0]) for a in np.linspace(PI/3,5*PI/3,40)]
    inner=[np.array([r*.50-r*.72*np.sin(a),r*.866*np.cos(a),0]) for a in np.linspace(PI,0,32)]
    return VMobject(color=PURPLE,fill_color=PURPLE,fill_opacity=1,stroke_width=0).set_points_as_corners(outer+inner+[outer[0]]).move_to(pos)
def sun(pos,r=.14):
    return VGroup(Circle(radius=r,color=YELLOW,fill_opacity=1),*[Line((r*1.3)*np.array([np.cos(a),np.sin(a),0]),(r*1.9)*np.array([np.cos(a),np.sin(a),0]),color=YELLOW) for a in np.arange(0,TAU,PI/4)]).move_to(pos)
def event_icons(p,t,s,st):
    g=VGroup()
    for k in np.flatnonzero(np.diff(st.astype(int))!=0)+1:g.add(moon(p.p(t[k],s[k])) if st[k] else sun(p.p(t[k],s[k])))
    return g

def icon_legend():
    return VGroup(moon([-4.8,2.73,0]),T('asleep',26,PURPLE).move_to([-4,2.73,0]),sun([-2.8,2.73,0]),T('wake',26,YELLOW).move_to([-2.1,2.73,0]))

class S09Pic2(TimedScene):
    def construct(self):
        p=Plot();t,s,st=model();k=np.flatnonzero(st)[0]
        self.add(p,p.threshold(),p.curve(t[:k],s[:k]),legend())
        self.at('lower wavy line');self.play(Create(p.threshold(False)),run_time=.65)
        # Complete before 'Both lines', leaving a readable settled result.
        self.play(FadeIn(p.bands(t,st)),Create(p.curve(t[k-1:],s[k-1:]),rate_func=linear),run_time=2.65)
        self.at('before you wake');self.play(FadeIn(legend(True)[2]),FadeIn(event_icons(p,t,s,st)),FadeIn(icon_legend()),run_time=.4)
        self.at('Both lines');self.play(Indicate(VGroup(p.threshold(),p.threshold(False)),color=PURPLE,scale_factor=1),run_time=.5)
        self.finish()

def rule_card():
    border=RoundedRectangle(width=12.6,height=6.9,corner_radius=.2,color=GREY)
    title=T('The one idea',40,font=TITLE_FONT).move_to([0,2.95,0])
    scope=T("In the simple model of an adult’s undisturbed sleep:",30,GREY).move_to([0,2.15,0])
    texts=[('Sleep pressure climbs while you are awake',ORANGE),('and drains while you sleep.',ORANGE),('You fall asleep when it climbs to an upper level,',PURPLE),('and you wake when it drains to a lower one.',PURPLE),('The clock raises both levels by day',PURPLE),('and lowers them by night.',PURPLE)]
    lines=[T(txt,32,c).move_to([0,1.15-i*.73,0]) for i,(txt,c) in enumerate(texts)]
    return VGroup(border,title,scope,*lines)

class S10Rule1(TimedScene):
    def construct(self):
        g=rule_card();self.add(g[0],g[1])
        self.at('in the simple model');self.play(FadeIn(g[2]),run_time=.35)
        self.at('Sleep pressure climbs');self.play(FadeIn(g[3]),run_time=.35)
        self.at('and drains');self.play(FadeIn(g[4]),run_time=.35)
        self.finish()

class S11Rule2(TimedScene):
    def construct(self):
        g=rule_card();self.add(*g[:5])
        self.at('You fall asleep');self.play(FadeIn(g[5]),run_time=.4)
        self.at('You wake');self.play(FadeIn(g[6]),run_time=.4)
        self.at('The clock raises');self.play(FadeIn(g[7]),run_time=.4)
        self.at('and lowers');self.play(FadeIn(g[8]),run_time=.4)
        self.finish()

class S12Gap(TimedScene):
    def construct(self):
        a=Plot(end=31,x=-5.9,w=5.4,y=-1.8,h=4.35,labels=False)
        b=Plot(end=31,x=.6,w=5.4,y=-1.8,h=4.35,labels=False)
        self.add(a,b,T('one midway line',30,PURPLE).move_to([-3.2,3.2,0]),T('two levels',30,PURPLE).move_to([3.3,3.2,0]))
        for p in [a,b]:
            self.add(T('sleep pressure',26,ORANGE).rotate(PI/2).move_to([p.x-.43,.45,0]),T('time · 24 h',26,GREY).move_to([p.x+p.w/2,-2.6,0]))
            for hr in [7,19,31]:self.add(T(f'{hr%24:02d}',26,GREY).move_to(p.p(hr,-.08)))
        self.add(T('illustrative units',26,GREY).move_to([0,3.7,0]))
        t,s,st=model(end=31,single=True,dt=.1);u,v,states=model(end=31)
        k=np.flatnonzero(st)[0]
        # Early build answers the opening question with movement.
        self.play(Create(a.curve(t[:k],s[:k],width=7),rate_func=linear),run_time=1)
        self.at('replace them')
        self.play(Create(a.curve(t,(level(t)+level(t,False))/2,PURPLE)),Create(b.threshold()),Create(b.threshold(False)),run_time=.65)
        def bar(p,tt,ss):
            g=VGroup();start=0
            for i in range(1,len(tt)):
                if ss[i]!=ss[start] or i==len(tt)-1:
                    x0=p.p(tt[start],0)[0];x1=p.p(tt[i],0)[0]
                    g.add(Rectangle(width=max(.002,x1-x0),height=.33,stroke_width=0,fill_color=PURPLE if ss[start] else GREY,fill_opacity=.9 if ss[start] else .28).move_to([(x0+x1)/2,-3.05,0]));start=i
            return g
        self.add(T('awake / asleep',26,GREY).move_to([-3.2,-3.53,0]),T('awake / asleep',26,GREY).move_to([3.3,-3.53,0]))
        self.at('the model chatters')
        self.play(Create(a.curve(t[k-1:],s[k-1:],width=8),rate_func=linear),Create(bar(a,t,st),rate_func=linear),run_time=1.85)
        note=T('possible numerical chattering',26,GREY).move_to([-3.2,2.65,0])
        self.add(BackgroundRectangle(note,fill_color=BG,fill_opacity=.9),note)
        self.at('The gap keeps')
        # Clip the state bar at the very same model time as the curve.
        tracker=ValueTracker(7)
        trace=always_redraw(lambda:b.curve(u[u<=tracker.get_value()],v[u<=tracker.get_value()]) if np.sum(u<=tracker.get_value())>1 else VGroup())
        blocks=always_redraw(lambda:bar(b,u[u<=tracker.get_value()],states[u<=tracker.get_value()]))
        self.add(trace,blocks)
        self.play(tracker.animate.set_value(31),rate_func=linear,run_time=2.6)
        trace.clear_updaters();blocks.clear_updaters();self.finish()

def forced_setup():
    p=Plot(end=38,w=9.25);t,s,_=model(end=38,forced=True)
    return p,t,s

def excess(p,t,s,hour):
    val=float(np.interp(hour,t,s));lo=float(level(hour));x=p.p(hour,0)[0]
    y0=p.p(hour,lo)[1];y1=p.p(hour,val)[1]
    return VGroup(Line([x,y0,0],[x,y1,0],color=RED,stroke_width=7),Line([x-.15,y0,0],[x+.15,y0,0],color=RED,stroke_width=5),Line([x-.15,y1,0],[x+.15,y1,0],color=RED,stroke_width=5),Dot(p.p(hour,val),color=ORANGE,radius=.1))

def proxy_label(p,t,s,hour):
    x=p.p(hour,0)[0];y=p.p(hour,(float(np.interp(hour,t,s))+float(level(hour)))/2)[1]
    ly=p.p(hour,float(level(hour)))[1]-.48
    lab=T('excess',28,RED).move_to([x+1.1,ly,0])
    return VGroup(Line([x+.12,p.p(hour,float(level(hour)))[1],0],[x+.35,ly,0],color=RED),lab)
def forced_caption():
    return VGroup(T('illustrative',26,RED),T('sleepiness proxy',26,RED)).arrange(DOWN,buff=.10).move_to([-.1,-.6,0])
def crossing(p,t,s):
    k=np.flatnonzero(s>=level(t))[0];pt=p.p(t[k],s[k])
    label=T('would fall asleep here',26,GREY).move_to([-2.8,-1.9,0])
    return k,VGroup(Dot(pt,color=ORANGE,radius=.12),Line(pt,[-2.8,-1.55,0],color=GREY),label)

class S13Back1(TimedScene):
    def construct(self):
        p,t,s=forced_setup();k,cross=crossing(p,t,s)
        self.add(p,p.threshold(),legend())
        self.at('Back to the');self.play(Create(p.curve(t[:k+1],s[:k+1])),run_time=1.2)
        self.at('Staying up means');self.play(FadeIn(cross),run_time=.4)
        self.at('pressure crosses the upper level');self.play(Create(p.curve(t[k:][t[k:]<=29],s[k:][t[k:]<=29])),run_time=1.3)
        self.at('Near dawn');self.play(FadeIn(T('near dawn · 05:00',28,GREY).move_to([.4,2.65,0])),run_time=.35)
        self.at('So pressure sits');self.play(Create(excess(p,t,s,29)),FadeIn(proxy_label(p,t,s,29)),FadeIn(forced_caption()),run_time=.5)
        self.finish()

class S14Back2(TimedScene):
    def construct(self):
        p,t,s=forced_setup();_,cross=crossing(p,t,s)
        old=excess(p,t,s,29);label=proxy_label(p,t,s,29)
        self.add(p,p.threshold(),legend(),p.curve(t[t<=29],s[t<=29]),old,label,cross,forced_caption())
        self.at('By early afternoon')
        self.play(old.animate.set_opacity(.35),label.animate.set_opacity(.35),Create(p.curve(t[t>=29],s[t>=29])),FadeIn(T('early afternoon · 14:00',28,GREY).move_to([.4,2.65,0])),run_time=1.3)
        self.at('the clock has lifted');self.play(ShowPassingFlash(p.curve(t[t>=29],level(t[t>=29]),PURPLE,9)),run_time=.6)
        self.at('the excess has shrunk')
        ratio=(s[-1]-level(38))/(np.interp(29,t,s)-level(29))
        self.play(Create(excess(p,t,s,38)),FadeIn(proxy_label(p,t,s,38)),FadeIn(VGroup(T('about half',26,RED),T(f'({ratio:.0%}) of dawn',26,RED)).arrange(DOWN,buff=.1).move_to([5.1,.0,0])),Create(Line([4.05,.35,0],[4.35,.05,0],color=RED,stroke_width=2)),run_time=.4)
        self.finish()

class S15Q3(TimedScene):
    def construct(self):
        self.add(empty_bars());self.at('When you finally sleep');self.play(FadeIn(question2()),run_time=.5);self.finish()
class S16Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(question2(),T('8 hours lost…',30,GREY).move_to([0,.55,0]))
        self.add(Rectangle(width=10.4,height=.8,color=GREY,fill_color=GREY,fill_opacity=.25).move_to([0,-.35,0]),T('…how much extra sleep?',30,ORANGE).move_to([0,-1.35,0]))
        countdown(self)

class S17Reveal(TimedScene):
    def construct(self):
        q=question2();frames=empty_bars();self.add(q,frames)
        lost=Rectangle(width=10.4,height=1.7,color=GREY,fill_color=GREY,fill_opacity=.4).move_to([0,.6,0])
        extra=Rectangle(width=1.04,height=1.7,color=ORANGE,fill_color=ORANGE,fill_opacity=.6).move_to([-4.68,-1.85,0])
        self.at('recovery sleep');self.play(FadeOut(q),FadeOut(frames),GrowFromEdge(lost,LEFT),FadeIn(T('one night lost: about 8 h',34,GREY).move_to([0,2,0])),run_time=.45)
        self.at('nowhere near hour for hour');self.play(GrowFromEdge(extra,LEFT),FadeIn(VGroup(Line(extra.get_right(),[-3.2,-1.85,0],color=ORANGE),T('extra recovery sleep: under 1 h',30,ORANGE).move_to([.7,-1.85,0]))),run_time=.5)
        self.add(T('illustrative model comparison',26,GREY).move_to([0,3.1,0]))
        self.at('deeper sleep',lead=0)
        dark=Rectangle(width=.94,height=1.6,stroke_width=0,fill_color='#744B27',fill_opacity=1).move_to(extra)
        lab=T('deeper slow-wave sleep',32,ORANGE).move_to([.7,-3.2,0])
        self.play(FadeIn(dark),FadeIn(lab),Create(Line(extra.get_bottom(),[-3,-3.2,0],color=ORANGE)),run_time=.4)
        self.finish()

class S18Lesion1(TimedScene):
    def construct(self):
        # Ventral schematic: olfactory bulbs anterior, hemispheres, optic nerves,
        # crossing, and a narrowing brainstem posterior. Labels stay outside.
        outline=VMobject(color=GREY,fill_color=GREY,fill_opacity=.08,stroke_width=4)
        pts=[[-1.1,2.5,0],[-1.9,2.1,0],[-2.3,1,0],[-2.25,-.6,0],[-1.7,-1.8,0],[-.65,-2.2,0],[-.5,-3,0],[.5,-3,0],[.65,-2.2,0],[1.7,-1.8,0],[2.25,-.6,0],[2.3,1,0],[1.9,2.1,0],[1.1,2.5,0],[0,2.15,0],[-1.1,2.5,0]]
        outline.set_points_smoothly(pts)
        bulbs=VGroup(*[Ellipse(width=.9,height=1.25,color=GREY,fill_opacity=.1).move_to([x,2.35,0]) for x in [-.65,.65]])
        mid=Line([0,1.9,0],[0,1.35,0],color=GREY,stroke_opacity=.5)
        chiasm=VGroup(Line([-1.5,.3,0],[.95,-1.1,0],color=GREY,stroke_width=12),Line([1.5,.3,0],[-.95,-1.1,0],color=GREY,stroke_width=12))
        scn=VGroup(*[Ellipse(width=.82,height=.85,color=TEAL,fill_opacity=.85).move_to([x,.85,0]) for x in [-.49,.49]])
        self.add(outline,bulbs,mid,chiasm,T('rat brain · ventral schematic',30,GREY).move_to([0,3.45,0]),T('optic chiasm',28,GREY).move_to([4.2,-1.3,0]),Line([1,-.65,0],[2.9,-1.3,0],color=GREY),T('olfactory bulbs',26,GREY).move_to([-4.2,2.5,0]),Line([-1,2.5,0],[-2.8,2.5,0],color=GREY))
        self.at('In rats');self.play(FadeIn(scn),run_time=.35)
        self.at('suprachiasmatic nucleus')
        label=VGroup(T('suprachiasmatic',28,TEAL),T('nucleus (SCN)',28,TEAL)).arrange(DOWN,buff=.12).move_to([-4.35,.85,0])
        self.play(FadeIn(label),Create(Line([-2.65,.85,0],[-.95,.85,0],color=TEAL)),run_time=.4)
        self.at('just above the optic chiasm');self.play(Indicate(chiasm,scale_factor=1.05),run_time=.35)
        self.play(scn.animate.set_fill(GREY,.25).set_stroke(GREY),Create(Cross(scn,stroke_color=RED,stroke_width=7)),FadeIn(T('SCN destroyed',30,RED).move_to([4.2,1.3,0])),run_time=.45)
        self.finish()

class S19Lesion2(TimedScene):
    def construct(self):
        self.add(T('SCN destroyed · same rat',32,TEAL).move_to([0,3.2,0]))
        self.add(T('day',28,GREY).move_to([-2.6,2.45,0]),T('night',28,GREY).move_to([2.6,2.45,0]))
        for x,op in [(-2.6,.15),(2.6,.04)]:
            self.add(Rectangle(width=5.2,height=1.1,stroke_color=GREY,fill_color=GREY,fill_opacity=op).move_to([x,1.5,0]))
        positions=[(-4.7,.5),(-3.2,.7),(-1.3,.6),(.5,.6),(2.8,.5),(4.5,.7)]
        def blocks(y,factor=1,color=ORANGE):
            return VGroup(*[Rectangle(width=w*factor,height=.85,stroke_width=0,fill_color=color,fill_opacity=1).move_to([x,y,0]) for x,w in positions])
        base=blocks(1.5,color='#BD895B')
        self.at('Sleep scatters');self.play(FadeIn(base),FadeIn(T('usual scattered sleep',28,GREY).move_to([0,.65,0])),run_time=.6)
        self.at('after a spell without sleep')
        kept=Rectangle(width=2.1,height=.7,color=GREY).move_to([-4.15,-.25,0])
        hatch=VGroup(*[Line([x,-.58,0],[x+.45,.08,0],color=GREY,stroke_width=2) for x in np.arange(-5.15,-3.6,.25)])
        self.play(FadeIn(kept),Create(hatch),FadeIn(T('kept awake',26,GREY).move_to([-4.15,.4,0])),Create(arr([-3,-.25,0],[-1.85,-.25,0],GREY,w=3)),run_time=.4)
        self.play(FadeIn(T('recovery sleep',30,GREY).move_to([1,-.25,0])),FadeIn(Rectangle(width=10.4,height=1.1,color=GREY,stroke_opacity=.4).move_to([0,-1.35,0])),run_time=.4)
        recovery=blocks(-1.35,1.65,color='#BD895B')
        self.at('still slept more');self.play(FadeIn(recovery),FadeIn(T('more total sleep · same time span',28,ORANGE).move_to([0,-2.25,0])),run_time=.45)
        self.at('more deeply')
        self.play(recovery.animate.set_fill('#744B27',1),FadeIn(T('deeper (more slow-wave)',30,ORANGE).move_to([0,-2.85,0])),run_time=.3)
        self.at('deeply',lead=0)
        self.play(FadeIn(T('pressure still repaid',32,ORANGE).move_to([0,-3.45,0])),run_time=.25)
        self.finish()

class S20Take(TimedScene):
    def construct(self):
        p=Plot(y=-2.35,h=4.6);t,s,st=model()
        icons=icon_legend()
        self.add(p,p.bands(t,st),p.threshold(),p.threshold(False),p.curve(t,s),event_icons(p,t,s,st),icons)
        a=T('Pressure climbs and drains,',34,ORANGE).move_to([0,3.3,0])
        b=T('and the clock sets the levels.',34,PURPLE).move_to([0,2.65,0])
        self.at('Pressure climbs');self.play(FadeIn(a),run_time=.35)
        self.at('the clock sets');self.play(FadeOut(icons),FadeIn(b),run_time=.35)
        self.finish()
class S21End(EndCard):
    LINE='Pressure climbs and drains, and the clock sets the levels.'
