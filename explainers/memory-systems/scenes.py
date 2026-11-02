"""Chapter 1: Two Ways of Remembering.

COLOR MAP (from scenes.old.py; shared across chapters)
BLUE=declarative / questionnaire; PURPLE=skill / classification; TEAL=working memory;
GREY=controls / frames; ORANGE=amnesic patients; GOLD=Parkinson's patients;
YELLOW=chance; GREEN=kept / pass; RED=lost / fail; TEXT=central claim.
CHAPTERS.md remains unchanged under the task's edit-only-scenes.py restriction.
"""
import numpy as np
from bp_style import *

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

# Reference-film helpers, preserved with the same geometry and colours.
def tick(c=GREEN, s=0.2, w=6):
    return VGroup(Line([-s, 0, 0], [-s*.3, -s*.8, 0], color=c, stroke_width=w),
                  Line([-s*.3, -s*.8, 0], [s, s*.9, 0], color=c, stroke_width=w))

def cross(c=RED, s=0.2, w=6):
    return VGroup(Line([-s,-s,0],[s,s,0],color=c,stroke_width=w),
                  Line([-s,s,0],[s,-s,0],color=c,stroke_width=w))

def arr(a,b,color=GREY,w=5):
    return Arrow(a,b,buff=.05,color=color,stroke_width=w,tip_length=.22,
                 max_tip_length_to_length_ratio=.45,max_stroke_width_to_length_ratio=12)

def label(s,x,y,size=28,c=TEXT):
    return T(s,size,c).move_to([x,y,0])

def box(x,y,w,h,c=GREY):
    return RoundedRectangle(width=w,height=h,corner_radius=.2,stroke_color=c,
                            fill_color=c,fill_opacity=.07,stroke_width=3).move_to([x,y,0])

def star_pair(center=ORIGIN,r=2):
    # Analytic five-point star geometry, rather than a hand-drawn outline.
    return VGroup(*[Star(n=5,outer_radius=r*k,inner_radius=r*.44*k,
                         color=PURPLE,stroke_width=3).move_to(center) for k in (1,.79)])

def hand_pen(p):
    # Side view of a writing grip: separated curled fingers and an opposing thumb.
    g=VGroup(
        Polygon([1.05,.32,0],[2,.18,0],[2.13,.92,0],[1.18,1.02,0],color=ORANGE,fill_color=ORANGE,fill_opacity=.7),
        RoundedRectangle(width=.95,height=.92,corner_radius=.24,color=ORANGE,fill_color=ORANGE,fill_opacity=1).move_to([.94,.77,0]))
    for i in range(4):
        finger=RoundedRectangle(width=.82-i*.07,height=.23,corner_radius=.1,
                                color=BG,fill_color=ORANGE,fill_opacity=1,stroke_width=2)
        finger.rotate(-.22).move_to([.55+i*.10,1.24-i*.27,0])
        g.add(finger,Line([.45+i*.10,1.28-i*.27,0],[.56+i*.10,1.16-i*.27,0],color=BG,stroke_width=2))
    g.add(Line([0,0,0],[.72,1.58,0],color=TEXT,stroke_width=9),
          Line([0,0,0],[.10,.22,0],color=GREY,stroke_width=6),
          RoundedRectangle(width=.88,height=.29,corner_radius=.13,color=BG,stroke_width=2,
                           fill_color=ORANGE,fill_opacity=1).rotate(-.65).move_to([.98,.77,0]))
    return g.shift(np.array(p,dtype=float))


def brain(x=0,y=0,scale=1):
    lobes=VGroup(*[Ellipse(width=2.3,height=4.5,color=GREY,fill_color=GREY,fill_opacity=.13).move_to([a,0,0]) for a in (-1.2,1.2)])
    temporal=VGroup(); medial=VGroup()
    for side in (-1,1):
        # Inferior view: anterior is up; temporal tissue is lateral, mid/anterior.
        temporal.add(VMobject(color=BLUE,fill_color=BLUE,fill_opacity=.16).set_points_smoothly([
            [side*.55,-.85,0],[side*1.55,-.95,0],[side*2,.1,0],
            [side*1.65,1.3,0],[side*.72,1.05,0],[side*.55,-.85,0]]))
        medial.add(Ellipse(width=.34,height=1.45,color=RED,fill_color=RED,fill_opacity=.7)
                   .rotate(-side*.10).move_to([side*.85,.15,0]))
    return VGroup(lobes,temporal,medial).scale(scale).move_to([x,y,0])


def learning_plot():
    # Illustrative exponential practice law; deterministic within-day scatter.
    # These are model values, never H.M.'s measured data.
    axes=VGroup(Line([-4.9,-2,0],[-4.9,2.35,0],color=GREY),Line([-4.9,-2,0],[5.25,-2,0],color=GREY))
    for v in (0,10,20,30):
        y=-2+v/30*4.2
        axes.add(Line([-5.02,y,0],[-4.9,y,0],color=GREY),label(str(v),-5.45,y,26,GREY))
    days=VGroup(*[label(f'Day {i+1}',x,-2.45,28) for i,x in enumerate((-3.4,0,3.4))])
    base=VGroup(axes,days,label('Errors per attempt · model',0,3.15,30,PURPLE),label('Schematic of the shape, not the original data',0,-3.15,26,GREY))
    def pt(t,v): return [-4.6+t*9.5/17,-2+v/30*4.2,0]
    ts=np.linspace(0,17,200); vals=3+25*np.exp(-ts/5.5)
    curve=VMobject(color=PURPLE,stroke_width=6).set_points_as_corners([pt(t,v) for t,v in zip(ts,vals)])
    dots=VGroup(*[Dot(pt(t,3+25*np.exp(-t/5.5)+.75*np.sin(t*2.3)),radius=.075,color=PURPLE) for t in range(18)])
    return base,VGroup(curve,dots)


def bubble(x,y,text=''):
    g=VGroup(RoundedRectangle(width=3.05,height=.95,corner_radius=.2,color=BLUE).move_to([x,y,0]),VMobject(color=BLUE).set_points_as_corners([[x-.65,y-.47,0],[x-.85,y-.7,0],[x-.2,y-.47,0]]))
    if text: g.add(label(text,x,y,26,BLUE))
    return g


def speech_days():
    return VGroup(*[bubble(x,y,'Never done\nthis before') for x,y in ((-2.9,2.95),(0,1.55),(3.4,.65))])


def glowing_curve(curve):
    return VGroup(curve[0].copy().set_stroke(PURPLE,width=24,opacity=.08),curve[0].copy().set_stroke(PURPLE,width=15,opacity=.18),curve.copy().set_stroke(width=8))

Q1='Why could he not tell anyone about it?'
Q2='What second result would rule out\n“the failed task was just harder” ?'


def puzzle_plot():
    base,curve=learning_plot()
    base[2].set_opacity(0)
    return VGroup(base,glowing_curve(curve),bubble(3.45,.85),label('?',3.45,.85,46,BLUE),label(Q1,0,3.15,30),label('Kept a record',-.4,.4,28,PURPLE))


def memory_cards(named=False):
    g=VGroup()
    for x,c,title,gloss in ((-3.2,BLUE,'Recall and report','Bring to mind and state'),(3.2,PURPLE,'Performance','Show it by doing')):
        g.add(VGroup(box(x,0,5.9,6.1,c),label(title,x,2.35,30,c),label(gloss,x,1.35,26,c)))
    return g


def event_icons():
    table=VGroup(Line([-1.3,-.2,0],[1.3,-.2,0],color=BLUE,stroke_width=6),Line([-1.1,-.2,0],[-1.1,-1.3,0],color=BLUE),Line([1.1,-.2,0],[1.1,-1.3,0],color=BLUE),Ellipse(width=1,height=.3,color=BLUE).move_to([-.2,0,0]),Circle(.48,color=BLUE).move_to([.9,.9,0]),Line([.9,.9,0],[.9,1.25,0],color=BLUE),Line([.9,.9,0],[1.15,.9,0],color=BLUE)).move_to([-3,.25,0])
    spider=VGroup(Ellipse(width=.7,height=1.05,color=BLUE,fill_color=BLUE,fill_opacity=.3))
    for side in (-1,1):
        for i in range(4):
            y=.4-i*.25
            spider.add(VMobject(color=BLUE).set_points_as_corners([[side*.25,y,0],[side*.8,y+.25-i*.1,0],[side*1.35,y-.2-i*.1,0]]))
    spider.move_to([3,.25,0])
    return VGroup(table,label('Episodic · events',-3,-1.55,28,BLUE),spider,label('8 legs · semantic facts',3,-1.55,28,BLUE))


def task_table(reverse=False,questions=True):
    g=VGroup(label('Recall',.2,2,30,BLUE),label('Drawing',4,2,30,PURPLE),Line([-6,1.45,0],[6,1.45,0],color=GREY),label('H.M.',-4.4,.65,32,ORANGE),label('FAIL',.2,.65,32,RED),label('PASS',4,.65,32,GREEN),label('Hypothetical\nreverse case',-4.4,-1.05,28,GREY))
    if questions: g.add(label('PASS' if reverse else '?',.2,-1.05,32,GREEN if reverse else GREY),label('FAIL' if reverse else '?',4,-1.05,32,RED if reverse else GREY))
    return g


def crossing():
    axes=VGroup(Line([-3.7,-2.45,0],[-3.7,2.65,0],color=GREY),Line([-3.7,-2.45,0],[3,-2.45,0],color=GREY),label('Result',-5.3,2.9,28),label('PASS',-4.65,2.1,28,GREEN),label('FAIL',-4.65,-1.9,28,RED),label('Recall',-2.8,-2.95,28,BLUE),label('Drawing',2.1,-2.95,28,PURPLE))
    hm=Line([-2.8,-1.9,0],[2.1,2.1,0],color=ORANGE,stroke_width=7)
    rev=Line([-2.8,2.1,0],[2.1,-1.9,0],color=GREY,stroke_width=7)
    dots=VGroup(*[Dot(p,radius=.12,color=c) for line,c in ((hm,ORANGE),(rev,GREY)) for p in (line.get_start(),line.get_end())])
    names=VGroup(label('H.M.',4.25,2.1,28,ORANGE),label('Hypothetical\nreverse case',4.35,-1.35,28,GREY),Line([2.25,-1.9,0],[3,-1.35,0],color=GREY))
    return VGroup(axes,hm,rev,dots,names)

class S00Title(TitleCard):
    LESSON='Memory Systems'
    TITLE='Two Ways of Remembering'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON.upper(),28,GREY),T(self.TITLE,46,font=TITLE_FONT),Line(LEFT*1.4,RIGHT*1.4,color=GOLD)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.7); self.wait(1.6); self.play(FadeOut(g),run_time=.6); self.finish()

class S01(SpokenScene):
    def construct(self):
        stars=star_pair([-3.65,-.35,0],2.8); hand=hand_pen([-3.65,.85,0]).scale(1.2,about_point=[-3.65,.85,0])
        self.add(stars,hand)
        self.at('Can a man')
        self.play(FadeIn(label('Can a man get better\nevery day and never\nremember doing it?',2.9,.85,36)),run_time=.6)
        self.at('get better')
        self.play(hand.animate.shift(DOWN*.25),run_time=.5)
        self.at('One patient did')
        self.play(FadeIn(label('One patient did.',2.9,-1.6,38,ORANGE)),run_time=.4); self.finish()

class S02(SpokenScene):
    def construct(self):
        b=brain(-1.8,0,1.15); self.add(b[0],b[1],label('Front',-1.8,3.15,28),label('Back',-1.8,-3.05,28),label('View from below · schematic',0,-3.55,26,GREY))
        self.at('In 1953'); self.play(FadeIn(label('1953',3.8,2.5,48)),FadeIn(label('Temporal lobes',3.65,.85,28,BLUE)),FadeIn(label('Inner (medial) tissue\nboth sides',3.8,-.65,28,RED)),run_time=.4)
        self.at('removed tissue'); self.play(FadeIn(b[2][0]),run_time=.5)
        self.at('both temporal lobes'); self.play(FadeIn(b[2][1]),Create(Line([1.7,-.15,0],[-.6,.15,0],color=RED)),run_time=.5); self.finish()

class S03(SpokenScene):
    def construct(self):
        self.add(label('H.M.',-4.6,2.9,48,ORANGE))
        clock=Circle(2.05,color=GREY).move_to([-2,0,0]); hand=Line([-2,0,0],[-2,1.75,0],color=TEXT,stroke_width=6)
        ticks=VGroup(*[Line(np.array([-2,0,0])+1.85*np.array([np.cos(a),np.sin(a),0]),np.array([-2,0,0])+2*np.array([np.cos(a),np.sin(a),0]),color=GREY) for a in np.linspace(0,TAU,12,endpoint=False)])
        self.add(clock,ticks,hand,Line([-2,0,0],[-.95,.2,0],color=GREY,stroke_width=5))
        cup=VGroup(RoundedRectangle(width=1.2,height=1.2,corner_radius=.15,color=BLUE),Arc(radius=.35,start_angle=-PI/2,angle=PI,color=BLUE).move_to([.8,0,0]),label('New event',0,-1.05,28,BLUE)).move_to([3.3,1,0])
        arrow=arr([3,-1.5,0],[3,.1,0],BLUE)
        self.at('new events'); self.play(FadeIn(cup),GrowArrow(arrow),FadeIn(label('Attention',3,-2.2,28,BLUE)),run_time=.45)
        self.at('within minutes'); self.play(Rotate(hand,angle=-PI/2,about_point=[-2,0,0]),FadeIn(label('a few minutes',-2,-2.65,28)),run_time=.7)
        self.at('attention moved on'); self.play(Rotate(arrow,angle=-PI/2,about_point=[3,-1.5,0]),FadeOut(cup),run_time=.7); self.finish()

class S04(SpokenScene):
    def construct(self):
        mirror=VGroup(box(0,0,11.5,5.6,GREY),Rectangle(width=11.15,height=5.25,color=GREY,fill_color=BLUE,fill_opacity=.06),Line([4.8,1.3,0],[5.3,1.8,0],color=GREY),Line([4.5,1.3,0],[5.15,1.95,0],color=GREY)); stars=star_pair([-1,-.3,0],2.1)
        self.add(mirror,stars,label('Brenda Milner, Montreal',0,3.25,32),label('Mirror',4.2,2.3,28,GREY))
        reflected=hand_pen(ORIGIN).flip(UP).scale(.9).move_to([3.5,-.25,0]); self.add(reflected)
        center=Star(n=5,outer_radius=2.1*.895,inner_radius=2.1*.44*.895).move_to([-1,-.3,0])
        pts=[center.point_from_proportion(t)+np.array([.22*np.sin(44*t),.22*np.cos(38*t),0]) for t in np.linspace(0,1,201)]
        trace=VMobject(color=TEXT,stroke_width=5).set_points_as_corners(pts)
        preview=VMobject(color=TEXT,stroke_width=5).set_points_as_corners(pts[:18]); self.add(preview)
        self.at('mirror drawing task'); self.play(Indicate(mirror,scale_factor=1.01),run_time=.4)
        hand=hand_pen(pts[0]).scale(.5,about_point=pts[0]); self.at('He traced between'); self.play(FadeIn(hand),run_time=.35)
        self.at('two outlines'); offset=hand.get_center()-pts[0]
        self.play(FadeOut(preview),Create(trace),UpdateFromAlphaFunc(hand,lambda m,a:m.move_to(trace.point_from_proportion(a)+offset)),reflected.animate.shift(LEFT*.25),run_time=1.2)
        def inside(point,vertices):
            x,y=point[:2]; hit=False
            for a,b in zip(vertices,np.roll(vertices,-1,axis=0)):
                if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]: hit=not hit
            return hit
        errors=[p for p in pts[::8] if not inside(p,stars[0].get_vertices()) or inside(p,stars[1].get_vertices())]
        self.at('seeing his hand'); self.play(FadeIn(VGroup(*[cross(s=.13,w=5).move_to(p) for p in errors[:5]])),FadeIn(label('Reflected hand',3.4,-1.65,28,ORANGE)),run_time=.4)
        self.at('only in a mirror'); self.play(FadeIn(box(0,-3.05,9.5,.55,GREY)),FadeIn(label('Direct view blocked',0,-3.05,26,GREY)),run_time=.4); self.finish()

class S05(SpokenScene):
    def construct(self):
        base,curve=learning_plot(); self.add(base)
        self.at('Across'); self.play(Create(curve[0]),FadeIn(curve[1]),run_time=1.7)
        self.at('he improved'); self.play(Indicate(curve,scale_factor=1.01,color=PURPLE),run_time=.5); self.finish()

class S06(SpokenScene):
    def construct(self):
        base,curve=learning_plot(); base[2].scale(.82).move_to([2,3.25,0]); self.add(base,curve)
        self.at('did not remember'); self.play(LaggedStart(*[FadeIn(b) for b in speech_days()],lag_ratio=.12),run_time=.7); self.finish()

class S07(SpokenScene):
    def construct(self):
        base,curve=learning_plot(); base[2].scale(.82).move_to([2,3.25,0]); bubbles=speech_days(); bubbles.set_stroke(opacity=.4); self.add(base,curve,bubbles)
        self.at('kept a record'); self.play(Transform(curve,glowing_curve(curve)),FadeIn(label('Kept a record',-.4,.4,28,PURPLE)),run_time=.6)
        self.at('Why could he not'); self.play(FadeOut(bubbles),FadeOut(base[2]),FadeIn(bubble(3.45,.85)),FadeIn(label('?',3.45,.85,46,BLUE)),FadeIn(label(Q1,0,3.15,30)),run_time=.5); self.finish()

class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(puzzle_plot()); self.wait(5)

class S09(SpokenScene):
    def construct(self):
        p=puzzle_plot(); self.add(p)
        self.at('The record showed up'); self.play(FadeOut(p[4]),FadeOut(p[3]),run_time=.35)
        self.at('how well he drew'); self.play(FadeIn(label('Performance',-.7,1.15,32,PURPLE)),run_time=.4)
        self.at('recall and report'); self.play(FadeIn(label('Recall and report',3.45,1.9,28,BLUE)),Create(cross(s=.45).move_to(p[2])),run_time=.5); self.finish()

class S10(SpokenScene):
    def construct(self):
        cards=memory_cards()
        report=bubble(-3.2,-.05); report.add(*[Line([-4,y,0],[-2.4,y,0],color=BLUE) for y in (.16,-.06)])
        doing=hand_pen(ORIGIN).scale(.85).move_to([3.2,-.05,0])
        cards[0].add(report); cards[1].add(doing); self.add(cards)
        self.at('two ways of remembering'); self.play(Indicate(cards[0],scale_factor=1.01,color=BLUE),Indicate(cards[1],scale_factor=1.01,color=PURPLE),run_time=.6)
        self.at('badly damaged only one'); self.play(cards[0].animate.set_color(GREY),FadeIn(label('Severely impaired',-3.2,-1.4,30,RED)),FadeIn(label('Kept',3.2,-1.4,36,GREEN)),run_time=.6); self.finish()

class S11(SpokenScene):
    def construct(self):
        panel=box(0,0,11.8,6.3,GREY); heading=label('Recall and report',0,2.5,34,BLUE); self.add(panel,heading)
        self.at('bring to mind'); self.play(FadeIn(label('Bring to mind and state',0,1.55,28,BLUE)),run_time=.4)
        self.at('is declarative'); new=label('Declarative memory',0,2.5,34,BLUE); self.play(FadeOut(heading),run_time=.15); self.play(FadeIn(new),run_time=.2)
        icons=event_icons(); self.at('events'); self.play(FadeIn(icons[:2]),run_time=.4)
        self.at('facts about the world'); self.play(FadeIn(icons[2:]),run_time=.4); self.finish()

class S12(SpokenScene):
    def construct(self):
        icons=event_icons(); self.add(box(0,0,11.8,6.3,GREY),label('Declarative memory',0,2.5,34,BLUE),icons)
        self.at('could almost never'); self.play(icons[0].animate.set_color(GREY),icons[1].animate.set_color(GREY),FadeIn(label('New declarative learning: severely impaired',0,-2.2,28,RED)),run_time=.5)
        self.at('new declarative memories'); self.play(FadeIn(label('Older facts: largely spared',0,-2.85,28,GREEN)),run_time=.4); self.finish()

class S13(SpokenScene):
    def construct(self):
        heading=label('Performance',0,2.65,34,PURPLE)
        hand=hand_pen([-5.15,.15,0]).scale(.8,about_point=[-5.15,.15,0])
        skill=VGroup(hand,label('Skills',-4.4,-1.1,28,PURPLE))
        habit=VGroup(Arc(radius=.82,start_angle=.3,angle=5.4,color=PURPLE).add_tip().move_to([-1.5,.4,0]),label('Habits',-1.5,-1.1,28,PURPLE))
        prime=VGroup(arr([.5,.2,0],[2.4,.2,0],PURPLE),Line([.4,.55,0],[1.2,.55,0],color=PURPLE),Line([.3,.85,0],[1,.85,0],color=PURPLE),label('Priming',1.4,-1.1,28,PURPLE))
        eye=VGroup(ArcBetweenPoints([3.8,.3,0],[5.4,.3,0],angle=-1,color=PURPLE),ArcBetweenPoints([3.8,.3,0],[5.4,.3,0],angle=1,color=PURPLE),Dot([4.6,.3,0],color=PURPLE),label('♪',3.8,1.25,44,PURPLE),label('Conditioning',4.4,-1.1,26,PURPLE))
        icons=VGroup(skill,habit,prime,eye)
        for icon in icons: icon.save_state(); icon.set_opacity(.18)
        self.add(box(0,0,12.2,6.4,PURPLE),heading,icons)
        self.at('is non'); self.play(FadeOut(heading),run_time=.15); self.play(FadeIn(label('Nondeclarative memory',0,2.65,34,PURPLE)),run_time=.2)
        for phrase,icon in (('skills',skill),('habits',habit),('priming',prime),('simple conditioning',eye)):
            self.at(phrase); self.play(Restore(icon),run_time=.3)
        self.at('He kept his skill learning')
        frame=Rectangle(width=2.6,height=3.7,color=GREEN).move_to([-4.4,-.1,0])
        self.play(Create(frame),FadeIn(label('H.M. kept this',-4.4,-2.45,26,GREEN)),FadeIn(star_pair([-4.4,-1.6,0],.28),shift=RIGHT*.7),run_time=.6); self.finish()

class S14(SpokenScene):
    def construct(self):
        self.add(box(0,0,12,6.6,TEAL),label('Working memory',0,2.75,36,TEAL))
        paper=box(-3,.9,5,2.5,TEAL)
        rings=VGroup(*[Line([x,1.95,0],[x,2.3,0],color=TEAL,stroke_width=5) for x in (-4.6,-3.8,-3,-2.2,-1.4)])
        self.at('Working memory'); self.play(Create(paper),Create(rings),run_time=.4)
        self.at('a few items for seconds'); self.play(FadeIn(label('5 8 2 7',-3,.9,56,TEAL)),run_time=.4)
        keys=VGroup()
        for n in range(1,10):
            x=2.1+(n-1)%3*1.25; y=1.55-(n-1)//3*1.12
            keys.add(VGroup(box(x,y,1.08,1.02,TEAL),label(str(n),x,y,40,TEAL)))
        self.at('phone number while you dial')
        loop=Arc(radius=.44,start_angle=.3,angle=5.3,color=TEAL).add_tip().set(width=.95).move_to([.35,.95,0])
        self.play(FadeIn(keys),Create(loop),FadeIn(label('Rehearsing',-.1,-.65,24,TEAL)),FadeIn(label('Phone keypad',3.35,-1.65,26,TEAL)),run_time=.4)
        self.play(LaggedStart(*[Indicate(keys[i-1],color=TEXT,scale_factor=1.12) for i in (5,8,2,7)],lag_ratio=.6),run_time=1)
        # Horizontal span scale gives the illustrative normal band its own right end.
        x0=-5.1; x1=.65; y=-1.65
        axis=VGroup(Line([x0,-2.25,0],[x1,-2.25,0],color=GREY),label('Digits remembered',-2.25,-2.95,26))
        for n in (0,2,4,6,8,10):
            x=x0+(x1-x0)*n/10
            axis.add(Line([x,-2.25,0],[x,-2.36,0],color=GREY),label(str(n),x,-2.58,22,GREY))
        band=Rectangle(width=2.875,height=.92,stroke_opacity=0,fill_color=GREEN,fill_opacity=.18).move_to([-.7875,y,0])
        normal=label('Normal\nrange',-.05,y,22,GREEN)
        bar=Rectangle(width=.05,height=.45,color=GREEN,fill_color=GREEN,fill_opacity=.85).move_to([x0+.025,y,0])
        self.at('His was normal'); self.play(FadeIn(axis),FadeIn(band),FadeIn(normal),FadeIn(bar),run_time=.25)
        self.play(bar.animate.stretch_to_fit_width(4.025).move_to([x0+2.0125,y,0]),FadeIn(label('Digit span: normal',3.35,-2.75,28,GREEN)),run_time=.7); self.finish()


class S15(SpokenScene):
    def construct(self):
        rails=VGroup(Line([-2.4,-2.6,0],[-2.4,2.6,0],color=GREY),Line([-.1,-2.6,0],[-.1,2.6,0],color=GREY),*[Line([-2.4,y,0],[-.1,y,0],color=GREY) for y in (-2.1,0,2.1)])
        self.add(rails,label('A difficulty difference?',0,3.25,34))
        self.at('Perhaps recall tests'); self.play(FadeIn(label('Recall',1.4,2.1,30,BLUE)),FadeIn(label('Mirror drawing',2,-2.1,30,PURPLE)),FadeIn(label('Intermediate task',2,0,26,GREY)),run_time=.5)
        self.at('simply harder'); self.play(GrowArrow(arr([-3.1,-2.3,0],[-3.1,2.3,0],GREY)),FadeIn(label('Harder?',-4.3,.8,28,GREY)),run_time=.4)
        self.at('brain damage hurts hard tasks first'); self.play(Create(cross(s=.3).move_to([3.7,2.1,0])),FadeIn(label('H.M. fails here',4.6,1.35,26,RED)),Create(tick(s=.3).move_to([4.3,-2.1,0])),FadeIn(label('H.M. passes',4.6,-2.8,26,GREEN)),Create(DashedLine([-2.7,1,0],[.3,1,0],color=RED)),FadeIn(label('Damage cuts off here?',2.35,.8,26,RED)),run_time=.6)
        self.add(label('Single dissociation · one patient, one failed task',0,-3.5,26,GREY)); self.finish()

class S16(SpokenScene):
    def construct(self):
        self.add(task_table()); self.at('What second result'); self.play(FadeIn(label(Q2,0,-2.65,28)),run_time=.6); self.finish()

class S17Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(task_table(),label(Q2,0,-2.65,28)); self.wait(5)

class S18(SpokenScene):
    def construct(self):
        table=task_table(); question=label(Q2,0,-2.65,28); self.add(table,question)
        self.at('A patient with damage somewhere else'); self.play(FadeOut(question),run_time=.4)
        self.at('who fails the task'); self.play(Transform(table[-1],label('FAIL',4,-1.05,32,RED)),run_time=.4)
        self.at('passes the task he failed'); self.play(Transform(table[-2],label('PASS',.2,-1.05,32,GREEN)),run_time=.4)
        self.at('he failed'); plot=crossing(); self.play(FadeOut(table),FadeIn(plot[0]),FadeIn(plot[4]),run_time=.4)
        self.play(Create(plot[1]),FadeIn(plot[3][:2]),run_time=.65)
        self.play(Create(plot[2]),FadeIn(plot[3][2:]),run_time=.65)
        self.wait(5); self.finish()

class S19(SpokenScene):
    def construct(self):
        plot=crossing(); self.add(plot)
        self.at('Here is the one idea'); self.play(FadeIn(label('The one idea',0,3.35,36,GOLD)),run_time=.4)
        self.at('Memory systems'); self.play(FadeOut(plot),FadeIn(label('Memory systems are told apart',0,.8,44)),run_time=.4)
        self.at('by crossed failures'); self.play(FadeIn(label('by crossed failures.',0,-.45,44)),Create(Line([-1.7,-2.8,0],[1.7,-1.65,0],color=ORANGE,stroke_width=8)),Create(Line([-1.7,-1.65,0],[1.7,-2.8,0],color=GREY,stroke_width=8)),run_time=.4); self.finish()


def structure_brain(x,damaged):
    outline=VGroup(*[Ellipse(width=1.85,height=4.35,color=GREY,fill_color=GREY,fill_opacity=.08).move_to([x+s*1.05,.6,0]) for s in (-1,1)])
    regions=VGroup()
    for name,c,y in (('X',BLUE,1.35),('Y',PURPLE,-.35)):
        for side in (-1,1):
            region=Ellipse(width=.75,height=1.05,color=c,fill_color=c,fill_opacity=.65 if name==damaged else .15).move_to([x+side*.95,y,0]); regions.add(region)
            if name==damaged: regions.add(cross(s=.21).move_to(region))
    return VGroup(outline,regions,label('Structure X',x,3.2,28,BLUE),label('Structure Y',x,-1.75,28,PURPLE),Line([x,2.9,0],[x+.65,1.7,0],color=BLUE),Line([x,-1.65,0],[x+.65,-.7,0],color=PURPLE))

class S20(SpokenScene):
    def construct(self):
        left=structure_brain(-3.35,'X'); right=structure_brain(3.35,'Y'); self.add(left)
        self.at('impairs task'); self.play(FadeIn(label('Task A',-4.45,-2.55,28,BLUE)),Create(cross(s=.35).move_to([-4.45,-3.1,0])),run_time=.4)
        self.at('spares task'); self.play(FadeIn(label('Task B',-1.95,-2.55,28,PURPLE)),Create(tick(s=.35).move_to([-1.95,-3.1,0])),run_time=.4)
        self.at('Damage elsewhere'); self.play(FadeIn(right),run_time=.25)
        self.play(FadeIn(label('Task A',1.95,-2.55,28,BLUE)),FadeIn(label('Task B',4.45,-2.55,28,PURPLE)),Create(tick(s=.35).move_to([1.95,-3.1,0])),Create(cross(s=.35).move_to([4.45,-3.1,0])),run_time=.5); self.finish()


def dial(x,y,c,angle=.8,r=1.9):
    end=np.array([x,y,0])+r*.77*np.array([np.cos(angle),np.sin(angle),0])
    return VGroup(Circle(r,color=c).move_to([x,y,0]),Line([x,y,0],end,color=c,stroke_width=8),Dot([x,y,0],color=c),*[Line(np.array([x,y,0])+r*.88*np.array([np.cos(a),np.sin(a),0]),np.array([x,y,0])+r*np.array([np.cos(a),np.sin(a),0]),color=c) for a in np.linspace(-.5,3.6,9)])

class S21(SpokenScene):
    def construct(self):
        one=dial(0,0,GREY,r=2.5); title=label('One shared capacity',0,3.1,36); self.add(one,title)
        self.at('Then weakening'); self.play(Rotate(one[1],angle=-1.7,about_point=ORIGIN),run_time=.9)
        self.at('cannot explain both'); mark=cross(s=1.5); self.play(Create(mark),run_time=.5)
        self.at('The tasks rely')
        panel=box(0,0,12,6.7,GREY)
        pair=VGroup(dial(-3,.2,BLUE,angle=2.6),dial(3,.2,PURPLE,angle=.35),label('Process 1',-3,2.65,32,BLUE),label('Process 2',3,2.65,32,PURPLE))
        self.play(FadeOut(one),FadeOut(title),FadeOut(mark),run_time=.2)
        self.remove(one,title,mark)
        self.play(FadeIn(panel),FadeIn(pair),run_time=.2)
        self.at('at least partly',lead=.45); self.play(FadeIn(label('Strong evidence, not proof',0,-2.7,30,GOLD)),run_time=.25)
        self.at('separable processes'); self.play(Indicate(pair[0][1],scale_factor=1.03),Indicate(pair[1][1],scale_factor=1.03),run_time=.4); self.finish()

class S22(SpokenScene):
    def construct(self):
        plot=crossing(); self.add(plot)
        self.at('That crossing'); self.play(Indicate(VGroup(plot[1],plot[2]),scale_factor=1.01),run_time=.4)
        self.at('double dissociation'); self.play(FadeIn(label('Double dissociation',0,3.35,36)),run_time=.4)
        # Translate and compress only the geometry vertically; preserve all label sizes.
        self.at('It shows each structure')
        target=plot.copy()
        target.stretch(.70,1).shift(UP*.65)
        for m in target.get_family():
            if isinstance(m,Text): m.stretch(1/.70,1)
        self.play(Transform(plot,target),run_time=.5)
        self.at('needed for its task'); self.play(FadeIn(label('Needed, in this experiment: shown',0,-2.35,30,GREEN)),run_time=.4)
        self.at('not that the memory'); self.play(FadeIn(label('Where it is stored: not shown?',0,-3.15,30,GREY)),run_time=.4); self.finish()

class S23(SpokenScene):
    def construct(self):
        self.add(label('Needed, not stored.',0,1.1,48),Line([-4,0,0],[4,0,0],color=GOLD))
        self.at('the key to reading'); self.play(FadeIn(label('The key to reading\nevery lesion study',0,-1.1,38,GOLD)),run_time=.5); self.finish()

class S24End(EndCard):
    LINE='Crossed failures show a structure is needed, not that it stores.'
    def construct(self):
        self.add(label('Crossed failures show a structure is needed,',0,.7,32),label('not that it stores.',0,-.2,38),label('biochemistrypedia.com',0,-1.6,26,TEAL)); self.finish()
