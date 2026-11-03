"""Reading the Ladder: anatomical schematics, not simulated trajectories.
COLOR MAP: BLUE #58C4DD axons; RED #FC6255 repellent / blocked;
YELLOW #F5D547 Robo; GREY #8B93A1 midline and structure;
GOLD #D4A843 traced axon; PURPLE #B58CD9 Comm; ORANGE #F29E4C Robo3.
Activity bars are illustrative definitions (100%, reduced, zero), not data.
"""
import numpy as np
from bp_style import *

LESSON = 'Crossing the Midline Once: Slit, Robo and Comm'


def label(txt, x, y, color=TEXT, size=30):
    return T(txt, size, color).move_to([x,y,0])


def header(txt, color=TEXT):
    return label(txt,0,3.45,color,32)


def route(points, color=GOLD, width=10):
    return VMobject(color=color,stroke_width=width).set_points_as_corners(
        [np.array([x,y,0]) for x,y in points])


def strip(x=0,y0=-3,y1=3,w=.5):
    return Rectangle(width=w,height=y1-y0,color=GREY,fill_color=GREY,
                     fill_opacity=.15,stroke_width=1).move_to([x,(y0+y1)/2,0])


def blocked(center, size=.3):
    c=np.array(center)
    return VGroup(*[Line(c+[-size,s*size,0],c+[size,-s*size,0],
                        color=RED,stroke_width=6) for s in (-1,1)])


def ladder(kind='normal',cx=0,cy=-.1,h=6,w=4,stain=False,glow=False):
    c=YELLOW if stain else BLUE
    rails=VGroup(*[Line([cx+dx,cy-h/2,0],[cx+dx,cy+h/2,0],
                       color=c,stroke_width=11) for dx in (-w/2,w/2)])
    rungs=VGroup()
    if kind in ('normal','robo'):
        for i in range(3):
            for f in (.3,.7):
                y=cy-h/2+(i+f)*h/3
                rungs.add(Line([cx-w/2,y,0],[cx+w/2,y,0],color=c,
                    stroke_width=21 if kind=='robo' else 6,
                    stroke_opacity=.23 if stain else 1))
    if kind=='comm':
        rungs.add(Line([cx-w/2,cy-.7,0],[cx+w/2,cy-.7,0],color=c,
                      stroke_width=4,stroke_opacity=.28))
    if kind=='slit':
        rails=VGroup(Line([cx,cy-h/2,0],[cx,cy+h/2,0],color=BLUE,stroke_width=85))
    halo=VGroup()
    if glow or stain:
        halo=VGroup(*[a.copy().set_stroke(width=25,opacity=.08) for a in rails],
                    *[a.copy().set_stroke(width=16,opacity=.06) for a in rungs])
    g=VGroup(halo,rails,rungs)
    g.rails,g.rungs=rails,rungs
    return g


def cone(x,y,s=1.7,left=False,n=0,dim=False):
    body=Circle(radius=.3*s,color=BLUE,fill_color=BLUE,fill_opacity=.45,stroke_width=3)
    fil=VGroup(*[Line(.3*s*np.array([np.cos(a),np.sin(a),0]),
                      .65*s*np.array([np.cos(a),np.sin(a),0]),color=BLUE,stroke_width=3)
                 for a in (-.8,-.3,.3,.8)])
    marks=VGroup(*[Rectangle(width=.12*s,height=.24*s,stroke_width=0,
        fill_color=YELLOW,fill_opacity=.4 if dim else 1).move_to(
        .36*s*np.array([np.cos(a),np.sin(a),0]))
        for a in ([0] if n==1 else np.linspace(-1,1,n))])
    g=VGroup(body,fil,marks)
    if left: g.rotate(PI)
    g.shift([x,y,0]); g.body=body; g.marks=marks
    return g


def embryo(kind='normal'):
    outline=Ellipse(width=3.6,height=6.2,color=GREY,fill_color=GREY,fill_opacity=.08)
    segs=VGroup(*[ArcBetweenPoints([-1.7*np.sqrt(1-(y/3.1)**2),y,0],
                              [1.7*np.sqrt(1-(y/3.1)**2),y,0],angle=.15,color=GREY,
                        stroke_opacity=.4) for y in (-2,-1,0,1,2)])
    cord=ladder(kind,h=5,w=1.1,cy=0,glow=True)
    return VGroup(outline,segs,cord)


def rail_label():
    b=Brace(Line([2.13,-2.9,0],[2.13,2.7,0]),RIGHT,buff=.1,color=GREY)
    return VGroup(b,label('rails',3.25,0,BLUE))


def timer(x,y,early=False):
    c=RED if early else GREY
    ring=Circle(radius=.43,color=c,fill_color=BG,fill_opacity=1).move_to([x,y,0])
    hands=VGroup(Line([x,y,0],[x,y+.3,0],color=c),
                 Line([x,y,0],[x+(.27 if early else -.22),y,0],color=c))
    return VGroup(ring,hands)


def logic(case=0):
    mid=strip(-4.6,-2.8,2.8)
    dots=VGroup(*[Dot([-4.08,y,0],radius=.13,color=RED) for y in (-1.5,0,1.5)])
    a=cone(-1.9,0,2,left=True,n=1)
    shaft=Line(a.body.get_center(),[1.1,0,0],color=BLUE,stroke_width=10)
    clock=timer(.1,0,case==3)
    small=Rectangle(width=.24,height=.34,fill_color=YELLOW,fill_opacity=1,
                    stroke_width=0).move_to([-2.15,-.62,0])
    labs=VGroup(label('midline',-4.6,-3.25,GREY),
                label('repellent',-4.2,2.35,RED),
                label('receptor',-2,1.2,YELLOW),
                label('EARLY' if case==3 else 'timing',.1,-1.2,RED if case==3 else GREY))
    lead=Line([-2.3,.9,0],[-2.62,.2,0],color=YELLOW,stroke_width=2)
    g=VGroup(mid,dots,shaft,a,small,clock,labs,lead)
    if case==1: g.add(blocked(a.marks.get_center(),.34))
    if case==2:
        dots.set_opacity(.15); g.add(blocked([-4.08,0,0],.4))
    g.axon=a; g.dots=dots; g.clock=clock
    return g


CASES={1:'Main receptor lost',2:'No repellent',3:'Receptor works too early'}


def question_frame(case):
    panel=logic(case)
    blank=ladder('empty',cx=4.3,cy=1.1,h=3.4,w=2.4).set_color(GREY).set_opacity(.45)
    q=label('?',4.3,1.1,size=90)
    return VGroup(panel,blank,q,header(CASES[case]))


def pause(scene,case):
    scene.camera.background_color=BG
    g=question_frame(case)
    scene.add(g, label('Pause and predict',4.3,-1.3,TEAL,30))
    opts=VGroup(*[label(t,4.3,y,size=28) for t,y in
                 [('thick rungs',-2),('one bundle',-2.6),('no rungs',-3.2)]])
    scene.add(opts)
    # A continuously draining ring makes the five-second prediction interval visible.
    base=Circle(radius=.58,color=GREY).move_to([1.5,1.7,0])
    scene.add(base)
    for k in range(5,0,-1):
        digit=label(str(k),1.5,1.7,TEAL,32)
        arc=Arc(radius=.58,start_angle=PI/2,angle=-TAU*k/5,color=TEAL,stroke_width=7).move_arc_center_to([1.5,1.7,0])
        nxt=Arc(radius=.58,start_angle=PI/2,angle=-TAU*max(.001,k-1)/5,
                color=TEAL,stroke_width=7).move_arc_center_to([1.5,1.7,0])
        scene.add(digit,arc); scene.play(Transform(arc,nxt),run_time=1,rate_func=linear)
        scene.remove(digit,arc)


def backtrace():
    return route([(-2,-2.9),(-2,-.5),(2,-.5),(2,1.4),(-2,1.4),(-2,2.8)])


def ipsitrace():
    return route([(-2,-2.9),(-2,-1.9),(2,-1.9),(2,-1.1)],width=8)


def stain_bracket():
    b=Brace(Line([-2,2.96,0],[2,2.96,0]),UP,buff=.05,color=YELLOW)
    # One shared bracket explicitly applies both populations to both rails.
    return VGroup(b,label('ipsilateral axons + axons already across',0,3.53,YELLOW,28))


def time_strip():
    g=VGroup(Line([-5.6,-2.25,0],[5.6,-2.25,0],color=GREY,stroke_width=3))
    for x,txt in [(-3.8,'before crossing'),(0,'crossing'),(3.8,'after crossing')]:
        g.add(Line([x,-2.13,0],[x,-2.37,0],color=GREY),label(txt,x,-2.8,size=28))
    return g


class S00Title(TitleCard):
    TITLE='Reading the Ladder'
    LESSON=LESSON
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',28,TEAL),T(self.LESSON,28),
                 T(self.TITLE,54,font=TITLE_FONT)).arrange(DOWN,buff=.5)
        self.play(FadeIn(g),run_time=.8); self.finish()


class S01Question(SpokenScene):
    def construct(self):
        e=embryo().shift(LEFT*3.7)
        q=VGroup(T('Which genes let an axon',32),T('cross only once?',36)).arrange(DOWN).move_to([2.1,.3,0])
        self.add(e,q,label('fly embryo',-3.7,-3.5,GREY,28))
        self.at('cross only once')
        self.play(Indicate(e[2],scale_factor=1.05,color=BLUE),run_time=.7)
        self.at('Look at the nerve cord')
        self.play(FadeOut(q),FadeOut(e[0]),FadeOut(e[1]),
                  *[FadeOut(m) for m in self.mobjects if isinstance(m,Text)],
                  e[2].animate.stretch_to_fit_height(6).stretch_to_fit_width(4).move_to([0,-.1,0]),run_time=1.8)
        self.add(header('ventral nerve cord',BLUE)); self.finish()


class S02Ladder(SpokenScene):
    def construct(self):
        l=ladder(glow=True); labs=rail_label()
        self.add(l,labs,header('Axon stain',BLUE))
        self.at('Stained for its axons')
        self.play(ShowPassingFlash(l.rails.copy().set_stroke(color=TEXT,width=16),time_width=.5),run_time=2)
        self.at('Two long rails')
        self.play(l.rungs.animate.set_opacity(.2),Indicate(labs,color=BLUE,scale_factor=1.02),run_time=.8)
        self.finish()


class S03Rungs(SpokenScene):
    def construct(self):
        l=ladder(glow=True); l.rungs.set_opacity(.2)
        self.add(l,rail_label())
        b=Brace(Line([-2.15,-3.1,0],[-2.15,-1.1,0]),LEFT,buff=.12)
        tx=VGroup(T('one segment',28),T('= 2 rungs',28)).arrange(DOWN).next_to(b,LEFT,buff=.15)
        self.at('In each segment')
        self.add(b,tx)
        for i in range(3):
            self.play(l.rungs[2*i:2*i+2].animate.set_opacity(1),
                      VGroup(b,tx).animate.shift(UP*(0 if i==0 else 2)),run_time=.8)
        self.at('These rungs are')
        self.play(FadeIn(header('commissures',BLUE)),run_time=.5); self.finish()


class S04Normal(SpokenScene):
    def construct(self):
        l=ladder(); body=Dot([-2,-2.9,0],radius=.17,color=GOLD)
        a=cone(-2,-2.7,.7); p=route([(-2,-2.9),(-2,-.5),(2,-.5),(2,2.8)])
        self.add(l,body,a,header('Normal: cross once'))
        self.at('Most commissural axons')
        self.play(Create(p),MoveAlongPath(a,p),run_time=3,rate_func=linear)
        self.at('on the far side')
        arrow=Arrow([2,1,0],[2,2,0],color=GOLD,buff=0,stroke_width=7)
        self.play(FadeIn(label('cross once → turn → far rail',0,-3.55,size=32)),GrowArrow(arrow),run_time=.5)
        self.finish()


class S05Screen(SpokenScene):
    def construct(self):
        kinds=['normal','robo','comm','slit']
        es=VGroup(*[embryo(k).stretch_to_fit_height(5.6).stretch_to_fit_width(2.8).move_to([x,0,0])
                    for k,x in zip(kinds,(-4.8,-1.6,1.6,4.8))])
        self.add(es,header('A screen for disturbed ladders · 1993'),
                 label('Seeger, Tear, Ferres-Marco, Goodman, 1993',0,-3.5,size=28))
        self.at('reported a screen')
        for i in (1,2,3):
            self.play(Circumscribe(es[i],color=GOLD,buff=.08),run_time=.85)
        self.finish()


class S06Lof(SpokenScene):
    def construct(self):
        # Definition examples only: no measurements or inferred mutant activities.
        axis=VGroup(Line([-3.9,-2.3,0],[-3.9,2.6,0],color=GREY),
                    Line([-3.9,-2.3,0],[5.5,-2.3,0],color=GREY))
        self.add(axis,label('gene activity',-4.8,.2,size=30).rotate(PI/2),
                 label('100%',-4.6,2.6,size=28),label('0',-4.3,-2.3,size=28),header('Loss of function'))
        bars=VGroup()
        for x,h,txt in [(-2,4.8,'normal'),(1,1.8,'reduced'),(4,.035,'abolished')]:
            bar=Rectangle(width=1.25,height=h,color=BLUE,fill_color=BLUE,fill_opacity=.7).move_to([x,-2.3+h/2,0])
            bars.add(bar); self.add(bar,label(txt,x,-2.7,size=28))
        caption=label('loss of function = activity reduced or abolished',0,-3.5,size=28)
        self.add(caption,label('illustrative activity',1,2.8,GREY,28))
        self.at('loss of function mutants')
        self.play(Indicate(caption,scale_factor=1.01,color=BLUE),run_time=.6)
        self.at('activity is reduced')
        self.play(Indicate(bars[1],scale_factor=1.04,color=BLUE),run_time=.7)
        self.at('or lost')
        self.play(Indicate(bars[2],scale_factor=1.1,color=BLUE),run_time=.5)
        self.at('These were strong losses')
        tag=label('strong loss',4,-1.6,RED,28)
        self.play(FadeIn(tag),run_time=.4); self.finish()


class S07Logic(SpokenScene):
    def construct(self):
        g=logic().shift(RIGHT*1.7)
        self.add(header('Repellent → receptor → timing'),g[0],g[2],g[3][0:2])
        self.at('The midline makes')
        self.play(FadeIn(g[1]),FadeIn(g[6][0:2]),run_time=.8)
        self.at('Axons carry a receptor')
        self.play(FadeIn(g[3].marks),FadeIn(g[4]),FadeIn(g[6][2]),Create(g[7]),run_time=.7)
        self.at('Something in the axon')
        self.play(FadeIn(g[5]),FadeIn(g[6][3]),run_time=.7); self.finish()


class S08Q1(SpokenScene):
    def construct(self):
        g=question_frame(1); self.add(g)
        self.at('Axons lose their main receptor')
        self.play(Indicate(g[0][-1],scale_factor=1.1),run_time=.6)
        self.at('What does')
        self.play(Indicate(g[2],scale_factor=1.1,color=TEAL),run_time=.6); self.finish()


class S09Pause(Scene):
    def construct(self): pause(self,1)


class S10Robo(SpokenScene):
    def construct(self):
        l=ladder('empty'); self.add(l,strip(),header('roundabout (robo)'),
            label('Axons are much less repelled',0,-3.55,size=30))
        self.at('Ipsilateral axons cross')
        ipsi=ipsitrace()
        il=label('ipsilateral',-3.25,-1.9,GOLD,28)
        self.play(Create(ipsi),FadeIn(il),run_time=1.1)
        self.at('Commissural axons cross')
        first=route([(-2,-2.9),(-2,-.5),(2,-.5),(2,1.4)])
        self.play(Create(first),FadeIn(label('commissural',-3.25,.1,GOLD,28)),run_time=1)
        self.at('and then cross back')
        self.play(Create(route([(2,1.4),(-2,1.4),(-2,2.8)])),run_time=1)
        self.at('The rungs thicken')
        r=ladder('robo').rungs
        self.play(FadeIn(r),run_time=.6); self.bring_to_front(ipsi,first)
        self.finish()


class S11RoboName(SpokenScene):
    def construct(self):
        p=backtrace(); i=ipsitrace()
        self.add(ladder('robo'),strip(),p,i,header('roundabout (robo)'),
            label('ipsilateral',-3.25,-1.9,GOLD,28),label('commissural',-3.25,.1,GOLD,28))
        self.at('called roundabout')
        self.play(Indicate(p,scale_factor=1,color=TEXT),run_time=.8)
        self.at('Its axons circle back')
        self.play(ShowPassingFlash(p.copy().set_color(TEXT),time_width=.5),run_time=1.5); self.finish()


class S12Q2(SpokenScene):
    def construct(self):
        g=question_frame(2); self.add(g)
        self.at('makes no repellent')
        self.play(Indicate(g[0][-1],scale_factor=1.2),run_time=.6)
        self.at('the latter')
        self.play(Indicate(g[2],color=TEAL,scale_factor=1.1),run_time=.5); self.finish()


class S13Pause(Scene):
    def construct(self): pause(self,2)


def slit_start():
    l=ladder('empty')
    return VGroup(l,strip(),header('slit'),label('enter and remain',3.9,0,BLUE,30))


class S14Slit(SpokenScene):
    def construct(self):
        g=slit_start(); self.add(g)
        self.at('axons that reach the midline')
        entrants=VGroup(*[route([(s*2,y),(0,y),(0,y+1)],BLUE,12)
                          for s,y in [(-1,-2.5),(1,-1.1),(-1,.3),(1,1.6)]])
        self.play(LaggedStart(*[Create(m) for m in entrants],lag_ratio=.3),run_time=2)
        self.at('They enter')
        self.play(Create(Line([0,-3.1,0],[0,2.9,0],color=BLUE,stroke_width=32)),run_time=.7)
        self.at('and do not leave')
        self.play(Indicate(g[-1],color=BLUE,scale_factor=1.03),run_time=.6); self.finish()


class S15SlitCollapse(SpokenScene):
    def construct(self):
        g=slit_start(); l=g[0]
        bundle=Line([0,-3.1,0],[0,2.9,0],color=BLUE,stroke_width=32)
        self.add(g,bundle)
        self.at('Over time')
        self.play(l.rails[0].animate.shift(RIGHT*2),l.rails[1].animate.shift(LEFT*2),
                  bundle.animate.set_stroke(width=85),FadeOut(g[-1]),run_time=3)
        self.at('single bundle')
        self.play(FadeIn(label('two rails merge',-3.1,1,BLUE,30)),
                  FadeIn(label('one midline bundle',3.1,-1,BLUE,30)),
                  Create(Line([1,-1,0],[.65,-1,0],color=BLUE)),
                  Create(Line([-1.45,1,0],[-.65,1,0],color=BLUE)),run_time=.5)
        self.at('This is the slit mutant')
        self.play(Indicate(g[2],color=BLUE,scale_factor=1.05),run_time=.6); self.finish()


class S16Q3(SpokenScene):
    def construct(self):
        g=question_frame(3); self.add(g)
        self.at('Commissural axons have')
        self.play(Indicate(g[0].axon.marks,color=YELLOW,scale_factor=1.15),run_time=.6)
        self.at('before they cross')
        self.play(Indicate(g[0].clock,color=RED,scale_factor=1.15),run_time=.7)
        self.at('What now')
        self.play(Indicate(g[2],color=TEAL,scale_factor=1.1),run_time=.5); self.finish()


class S17Pause(Scene):
    def construct(self): pause(self,3)


class S18Comm(SpokenScene):
    def construct(self):
        # Same early cone as the question; the cord is never shown with normal rungs.
        g=logic(3); self.add(g,header('Receptor works too early'))
        self.at('They are pushed away')
        push=Arrow([-3.7,.65,0],[-.8,.65,0],color=RED,buff=0)
        moving=VGroup(g[2],g.axon,g[4],g[5],g[6][2:4],g[7])
        self.play(GrowArrow(push),moving.animate.shift(RIGHT*1.3),run_time=1.2)
        self.at('Almost no axon crosses')
        l=ladder('comm')
        # Slide the close view aside and bring the full cord in from the right.
        self.play(g.animate.scale(.65).shift(LEFT*2.4).set_opacity(0),
                  FadeOut(push),FadeIn(l,shift=RIGHT*3),
                  *[FadeOut(m) for m in self.mobjects if isinstance(m,Text)],
                  run_time=1)
        self.remove(g)
        self.add(header('Almost no crossing',BLUE))
        self.at('the rungs nearly vanish')
        self.play(Indicate(l.rungs,scale_factor=1.02,color=BLUE),run_time=.7); self.finish()


class S19CommName(SpokenScene):
    def construct(self):
        l=ladder('comm'); title=header('Almost no crossing',BLUE)
        self.add(l,title)
        self.at('This is commissureless')
        self.play(Transform(title,header('commissureless (comm)')),run_time=.5)
        self.at('The name says it')
        # Four equally tall columns use the full height; the small normal reference is narrow.
        xs=(-5.1,-1.8,1.6,5)
        comm=ladder('comm',cx=xs[3],w=2.2)
        self.play(Transform(l,comm),FadeOut(title),
            FadeIn(ladder('normal',cx=xs[0],w=1.7)),
            FadeIn(ladder('robo',cx=xs[1],w=2.2)),
            FadeIn(ladder('slit',cx=xs[2],w=2.2)),
            *[FadeIn(label(t,x,3.4,size=28)) for x,t in zip(xs,('normal','robo','slit','comm'))],run_time=1.2)
        self.play(FadeIn(label('nearly no rungs',5,-3.55,BLUE,28)),run_time=.4); self.finish()


class S20Clone(SpokenScene):
    def construct(self):
        # Eight extracellular domain cartoons, followed by one membrane span.
        mem=Rectangle(width=5,height=.3,color=BLUE,fill_color=BLUE,fill_opacity=.2).move_to([3,-1.65,0])
        stem=Line([3,-3,0],[3,2.9,0],color=YELLOW,stroke_width=8)
        domains=VGroup()
        for i in range(8):
            txt='Ig' if i<5 else 'FN'
            box=RoundedRectangle(width=1.15,height=.43,corner_radius=.1,
                color=YELLOW,fill_color=BG,fill_opacity=1,stroke_width=3)
            domains.add(VGroup(box,T(txt,22,YELLOW)).move_to([3,2.65-i*.52,0]))
        rec=VGroup(stem,domains)
        labs=VGroup(label('5 Ig + 3 FN domains',-2.9,1.8,YELLOW,32),
                    label('outside',5,1,GREY,28),label('inside',5,-2.5,GREY,28),
                    label('membrane',-.9,-1.65,BLUE,28),
                    label('one membrane span',-2.9,-.5,YELLOW,30))
        self.add(mem,rec,labs,header('Robo · 1998',YELLOW),
                 label('Kidd, Tear, Goodman and colleagues',0,-3.5,size=28))
        self.at('In 1998')
        self.play(ShowPassingFlash(stem.copy().set_color(TEXT),time_width=.5),run_time=2.4)
        self.at('cloned robo')
        self.play(Indicate(domains,color=YELLOW,scale_factor=1.04),run_time=.6)
        self.at('It encodes a receptor')
        self.play(Indicate(rec,color=YELLOW,scale_factor=1.02),run_time=.7)
        self.at('spans the membrane once')
        self.play(Circumscribe(Line([3,-1.95,0],[3,-1.35,0]),color=YELLOW,buff=.15),run_time=1); self.finish()


class S21Timing(SpokenScene):
    def construct(self):
        mid=strip(0,-1.8,2.6)
        a=cone(-3.3,-.7,2.7,n=5)
        tail=Line([-5.7,-.7,0],a.body.get_center(),color=BLUE,stroke_width=10)
        self.add(mid,a,tail,time_strip(),header('When is Robo present?',YELLOW),
                 label('ipsilateral: Robo from the start',0,-3.5,YELLOW,30),
                 label('ipsilateral axon',-3.4,2.85,BLUE),label('midline',0,2.95,GREY,28),
                 label('Robo present',3.5,1.1,YELLOW,34),
                 label('before crossing',3.5,.35,YELLOW,30),
                 VGroup(*[Rectangle(width=.28,height=.5,stroke_width=0,
                     fill_color=YELLOW,fill_opacity=1).move_to([2.5+i*.5,-.65,0]) for i in range(5)]))
        self.at('Axons that never cross')
        self.play(a.animate.shift(UP*1.9),Transform(tail,route([(-5.7,-.7),(-3.3,-.7),(-3.3,1.2)],BLUE,10)),run_time=1.5)
        self.at('from the start')
        self.play(Indicate(a.marks,color=YELLOW,scale_factor=1.1),run_time=.7); self.finish()


class S22Timing2(SpokenScene):
    def construct(self):
        # Leave an open viewing window around the crossing cone and its few receptors.
        mid=VGroup(strip(0,-1.8,-.65),strip(0,1.5,2.6),label('midline',0,2.75,GREY,28))
        a=cone(-3.8,.4,2.7,n=2)
        tail=always_redraw(lambda:Line([-5.7,.4,0],a.body.get_center(),color=BLUE,stroke_width=9))
        lo=label('few Robo while crossing',-3,2,YELLOW,30)
        self.add(mid,a,tail,time_strip(),lo,header('Commissural axon',BLUE))
        self.at('Axons that do cross')
        self.play(a.animate.shift(RIGHT*7.2),run_time=2.2,rate_func=linear)
        self.at('only after they have crossed')
        many=cone(0,0,2.7,n=5).marks.move_to(a.marks)
        self.play(Transform(a.marks,many),FadeOut(lo),
                  FadeIn(label('many Robo after crossing',3.5,2,YELLOW,30)),run_time=.6); self.finish()


def stain_key():
    key=VGroup()
    for y,opacity,txt in [(1.1,1,'bright: more Robo'),(-.1,.23,'dim: little Robo')]:
        key.add(Line([-6,y+.5,0],[-3.2,y+.5,0],color=YELLOW,
                     stroke_width=10,stroke_opacity=opacity),
                label(txt,-4.6,y,YELLOW,26))
    return key


def rung_pointer():
    return VGroup(label('dim rung',4.6,.95,YELLOW,32),
                  Arrow([4.6,.5,0],[1.1,.3,0],buff=0,color=YELLOW))


class S23Stain(SpokenScene):
    def construct(self):
        l=ladder(glow=True); self.add(l,header('Robo protein stain',YELLOW))
        self.at('Picture the latter')
        self.play(Transform(l,ladder(stain=True)),FadeIn(stain_key()),
                  FadeIn(rung_pointer()),run_time=1.2)
        self.at('The rails are bright')
        self.play(ShowPassingFlash(l.rails.copy().set_stroke(color=TEXT,width=14),time_width=.4),run_time=1.1)
        self.at('They hold ipsilateral axons')
        self.play(*[FadeOut(m) for m in self.mobjects if isinstance(m,Text)],FadeIn(stain_bracket()),run_time=.5)
        self.at('and axons already across')
        self.play(Indicate(l.rails,scale_factor=1,color=YELLOW),run_time=.8); self.finish()


class S24StainRungs(SpokenScene):
    def construct(self):
        l=ladder(stain=True); self.add(l,stain_bracket(),stain_key(),rung_pointer())
        self.at('The rungs')
        self.play(Indicate(l.rungs[3],scale_factor=1,color=YELLOW),run_time=.5)
        self.at('are much dimmer')
        self.play(FadeIn(label('crossing: dim rungs',0,-3.55,YELLOW,30)),run_time=.4); self.finish()


class S25Take(SpokenScene):
    def construct(self):
        # Only the traced axon is gold; unused segments stay faint yellow.
        l=ladder(stain=True,cy=0,h=6.6,w=5.4)
        l.rungs.set_opacity(.1)
        l.rails.set_opacity(.12)
        self.add(l,header('The same axon',GOLD))
        up=route([(-2.7,-3.3),(-2.7,-.44)],GOLD,12).set_opacity(.45)
        across=route([(-2.7,-.44),(2.7,-.44)],GOLD,12).set_opacity(.45)
        far=route([(2.7,-.44),(2.7,3.3)],GOLD,20)
        self.at('The same axon')
        self.play(Create(up),run_time=.6)
        self.at('while it crosses')
        self.play(Create(across),FadeIn(label('little Robo',-4.8,.8,GOLD,32)),
                  GrowArrow(Arrow([-4.8,.35,0],[-1.6,-.44,0],buff=0,color=GOLD)),run_time=.8)
        self.at('and a lot')
        self.play(Create(far),FadeIn(label('high Robo',4.7,1.5,GOLD,32)),
                  GrowArrow(Arrow([4.7,1.05,0],[2.7,.8,0],buff=0,color=GOLD)),run_time=.7)
        self.at('That is what')
        takeaway=VGroup(T('deaf until',30),T('crossed',30)).arrange(DOWN,buff=.15).move_to([-4.8,-1.9,0])
        self.play(FadeIn(takeaway),run_time=.4)
        self.at('a much weaker response')
        self.play(FadeIn(label('weaker response ≠ no response',0,-3.6,size=28)),run_time=.4); self.finish()


class S26End(EndCard):
    LINE='The same axon carries little Robo while crossing and a lot once across.'
    def construct(self):
        l=ladder(stain=True,cx=-4.8,cy=.3,h=4.8,w=2.1)
        line=VGroup(T('The same axon carries',34,font=TITLE_FONT),
                    T('little Robo while crossing',34,font=TITLE_FONT),
                    T('and a lot once across.',38,font=TITLE_FONT)).arrange(DOWN,buff=.3).move_to([1.4,.3,0])
        self.play(FadeIn(l),FadeIn(line),run_time=.6)
        self.add(label('biochemistrypedia.com',0,-2.7,TEAL,28)); self.finish()
