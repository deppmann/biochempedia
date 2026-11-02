"""Two Counts: Side and Sign — reviewed redraw.
COLOR MAP: GREEN excitation; YELLOW increased drive; RED inhibition/lesion/weakness;
GOLD modulation; BLUE neural populations; YELLOW highlighted tract/spikes;
GREY anatomy; TEXT explanatory labels. No molecular structures.
Tick trains are qualitative signed-model illustrations, not measured rates:
r_i = baseline + delta * product(link signs); evenly spaced events over a
common unit time window. Baseline=6, delta=4, inhibitory signs=(-1,-1).
"""
import json
import os
from pathlib import Path
import numpy as np
from bp_style import *
from bp_style import SpokenScene as HouseSpokenScene


class SpokenScene(HouseSpokenScene):
    # The house logger prints the clock BEFORE waiting: negative 'late' values
    # are pending waits, not early pictures. Audit the actual clock AFTER waiting.
    # Keep audit output and all renderer intermediates outside the deliverables.
    def at(self, phrase, lead=0, nth=0):
        target = self.t_of(phrase, nth)
        if target > self.elapsed() + .001:
            self.wait(target - self.elapsed())
        audit = Path(os.environ.get('BG_CUE_AUDIT', '/tmp/bg-cue-audit.jsonl'))
        with audit.open('a') as f:
            f.write(json.dumps(dict(scene=os.environ['KX_SCENE_ID'], phrase=phrase,
                                    target=target, actual=self.elapsed()))+'\n')

    def finish(self):
        if self.elapsed() < self.narration_s:
            self.wait(self.narration_s-self.elapsed())


def label(s, x=0, y=3.15, size=28, color=TEXT):
    return T(s, size=size, color=color).move_to([x,y,0])


def path(points, color=YELLOW, width=6):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [np.array([x,y,0.]) for x,y in points])


def lesion(x,y):
    return VGroup(Circle(radius=.22,color=RED,stroke_width=4).move_to([x,y,0]),
                  Line([x-.12,y-.12,0],[x+.12,y+.12,0],color=RED,stroke_width=5),
                  Line([x-.12,y+.12,0],[x+.12,y-.12,0],color=RED,stroke_width=5))


CX=0

def anatomy():
    brain=Ellipse(width=4.8,height=1.9,color=GREY).move_to([CX,2.05,0])
    mid=DashedLine([CX,2.98,0],[CX,1.15,0],color=GREY,stroke_width=2)
    stem=VGroup(*[RoundedRectangle(width=w,height=h,corner_radius=.1,color=GREY,
                 fill_color=GREY,fill_opacity=.09).move_to([CX,y,0])
                 for w,h,y in [(1.3,.6,.8),(1.65,.7,.12),(1.25,.8,-.65)]])
    cord=RoundedRectangle(width=1.1,height=2,corner_radius=.15,color=GREY).move_to([CX,-2.12,0])
    def limbs(side):
        return VGroup(path([(CX+side*.6,-1.8),(CX+side*1.6,-1.8),(CX+side*3.0,-2.25)],BLUE,13),
                      path([(CX+side*.5,-2.4),(CX+side*1.4,-3.12),(CX+side*2,-3.12)],BLUE,13))
    sides=VGroup(label("Patient's right",-3.8,3.35,32),label("Patient's left",3.8,3.35,32),
                 label('Frontal view',0,3.35,32),
                 *[label('arm',side*3.55,-2.25,32) for side in [-1,1]],
                 *[label('leg',side*2.5,-3.33,32) for side in [-1,1]])
    return VGroup(brain,mid,stem,cord,limbs(-1),limbs(1),sides)


def crossing():
    return VGroup(path([(CX+.4,-.85),(CX-.4,-1.4)]),
                  path([(CX-.4,-.85),(CX+.4,-1.4)]))


def upper(side=1):
    return path([(CX+side*1.1,2.7),(CX+side*.85,1.9),(CX+side*.45,.8),
                 (CX+side*.4,.1),(CX+side*.4,-.85)])


def distal(side=-1,color=YELLOW):
    # Coloured paths follow the exact limb centrelines, ending on the limb.
    return VGroup(path([(CX+side*.4,-1.4),(CX+side*.4,-1.8),
                        (CX+side*1.6,-1.8),(CX+side*3,-2.25)],color),
                  path([(CX+side*.4,-1.8),(CX+side*.4,-2.4),
                        (CX+side*.5,-2.4),(CX+side*1.4,-3.12),
                        (CX+side*2,-3.12)],color),
                  Dot([CX+side*3,-2.25,0],radius=.08,color=color),
                  Dot([CX+side*2,-3.12,0],radius=.08,color=color))


def crossing_glow(x):
    return VGroup(*[x.copy().set_stroke(color=YELLOW,width=w,opacity=o)
                   for w,o in [(26,.08),(18,.14),(11,.28)]])


def tract():
    return VGroup(upper(),crossing()[0],distal())


def leader(s, x,y, px,py, color=TEXT,size=26):
    t=label(s,x,y,size,color)
    edge=t.get_left() if px<x else t.get_right()
    return VGroup(Line([px,py,0],edge+(.12*LEFT if px<x else .12*RIGHT),color=GREY,stroke_width=2),t)


def result_lines(first, second):
    return VGroup(label(first,4.65,1.35,28),label('below the lesion',4.65,.8,28),
                  label(second,4.65,-.2,32,RED))


def question1():
    return (anatomy(),crossing(),lesion(CX-.4,-.58),
            label('Which limbs\nare weak?',4.65,-.25,32),
            leader('Right pyramid',4.65,1.3,CX-.4,-.58))


def time_hint(y=-3.35):
    return label('Pause and answer',4.65,y,26,YELLOW)


def inhibit(a,b,y=.5):
    p=np.array([a+1.15,y,0]); q=np.array([b-1.15,y,0])
    return VGroup(Line(p,q,color=RED,stroke_width=6),
                  Line(q+UP*.25,q+DOWN*.25,color=RED,stroke_width=7),
                  chip('−',RED,32).move_to((p+q)/2+UP*.7))


def ticks(x,n):
    # Deterministic event times in a common [0,1] window, from the signed model.
    times=(np.arange(n)+.5)/n
    return VGroup(*[Line([x-1.1+2.2*t,-2.42,0],[x-1.1+2.2*t,-1.32,0],
                         color=YELLOW,stroke_width=4) for t in times])


def rate(i,fast=False,released=False):
    reached=fast and (i==0 or released)
    return int(6 + (4 * np.prod([-1]*i) if reached else 0))


def neurons(fast=False,released=False):
    nodes=VGroup(*[VGroup(Circle(radius=1.15,color=BLUE,fill_color=BLUE,
                    fill_opacity=(.65 if rate(i,fast,released)>6 else .08 if rate(i,fast,released)<6 else .28)),
                    label(c,0,0,44)).move_to([x,.5,0]) for i,(x,c) in enumerate(zip([-4,0,4],'ABC'))])
    trains=VGroup(*[ticks(x,rate(i,fast,released)) for i,x in enumerate([-4,0,4])])
    links=VGroup(inhibit(-4,0),inhibit(0,4))
    return nodes,trains,links


def circuit_labels(fast=False,released=False,heading='Any three cells in a row'):
    rates=[rate(i,fast,released) for i in range(3)]
    return VGroup(label(heading,0,3.25,30),label('Firing, over time',0,-.95,26),
         *[VGroup(Arrow([x-1.2,-2.62,0],[x+1.2,-2.62,0],buff=0,color=GREY,stroke_width=2),
                   label('fast' if r>6 else 'slow' if r<6 else 'baseline',x,-3.05,26,
                         YELLOW if r!=6 else TEXT)) for x,r in zip([-4,0,4],rates)])


def question2():
    n,t,l=neurons(True)
    return n,t,l,circuit_labels(True),label('What does the third neuron do?',0,2.4,30)


def count_card(which,x):
    box=RoundedRectangle(width=5.8,height=4.75,corner_radius=.2,color=BLUE,
                          fill_color=BLUE,fill_opacity=.08).move_to([x,-.35,0])
    if which==1:
        content=VGroup(label('Count 1 · crossings',x,1.35,30,YELLOW),
             label('One crossing',x,.5,30),label('flips the side',x,-.15,30),
             path([(x-1.2,-.8),(x+1.2,-2.05)]),path([(x+1.2,-.8),(x-1.2,-2.05)]),
             label('right',x-1.4,-2.4,26),label('left',x+1.4,-2.4,26))
    else:
        content=VGroup(label('Count 2 · inhibitions',x,1.35,30,RED),
             label('Each inhibition',x,.5,30),label('flips the sign',x,-.15,30),
             label('increase',x-1.5,-1.1,26,YELLOW),label('decrease',x+1.5,-2.05,26,RED),
             Arrow([x-1,-1.3,0],[x+1,-1.85,0],buff=.05,color=RED),chip('−',RED,30).move_to([x+.5,-1.1,0]))
    return VGroup(box,content)


class S00Title(TitleCard):
    LESSON='Descending Control and the Basal Ganglia'
    TITLE='Two Counts: Side and Sign'
    def construct(self):
        self.add(VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28),
            T(self.TITLE,48,font=TITLE_FONT),Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.4))
        self.wait(self.narration_s)


class S01Question(SpokenScene):
    def construct(self):
        a=anatomy(); self.add(a)
        self.at('stroke deep'); self.play(FadeIn(lesion(CX+.85,1.9)),run_time=.3)
        self.at('weakens the right'); self.play(a[4].animate.set_stroke(opacity=.2),run_time=.4)
        self.at('Why the opposite'); self.play(FadeIn(label('Why the\nopposite side?',4.65,.2,32)),run_time=.3)
        self.finish()


class S02Neck(SpokenScene):
    def construct(self):
        a=anatomy(); old=lesion(CX+.85,1.9).set_color(GREY).set_opacity(.35); self.add(a,old)
        self.at('cut through'); self.play(FadeIn(lesion(CX-.4,-1.6)),run_time=.3)
        self.at('weakens the right'); self.play(a[4].animate.set_stroke(opacity=.2),run_time=.4)
        self.at('on opposite sides'); txt=label('Lesions on\nopposite sides,',4.65,1.3,30); self.play(FadeIn(txt),run_time=.3)
        self.at('weakness on the same'); self.play(FadeIn(label('weakness on\nthe same side',4.65,-.15,30,RED)),run_time=.3)
        self.finish()


class S03Tract(SpokenScene):
    def construct(self):
        self.add(anatomy())
        self.at('Follow the tract'); self.play(Create(path([(CX+1.1,2.7),(CX+.85,1.9)])),run_time=.65)
        self.at('motor cortex'); self.play(FadeIn(leader('Motor cortex',4.55,2.7,CX+1.1,2.7)),run_time=.3)
        self.at('through the internal'); self.play(Create(path([(CX+.85,1.9),(CX+.45,1.1)])),
                       FadeIn(leader('Internal capsule',4.55,1.85,CX+.7,1.5)),run_time=.55)
        self.at('and the brainstem')
        for s,y,end in [('Cerebral peduncle',.8,.5),('Base of pons',.05,-.25),('Pyramid',-.7,-.85)]:
            start=1.1 if s=='Cerebral peduncle' else .5 if s=='Base of pons' else -.25
            self.play(Create(path([(CX+.4,start),(CX+.4,end)])),
                      FadeIn(leader(s,4.55,y,CX+.4,y)),run_time=.35)
        self.finish()


class S04Cross(SpokenScene):
    def construct(self):
        a=anatomy(); x=crossing(); self.add(a,upper(),upper(-1).set_stroke(opacity=.25))
        self.at('caudal medulla'); self.play(FadeIn(leader('Caudal medulla',4.65,.8,CX,-.65)),run_time=.3)
        self.at('most of its'); self.play(FadeIn(label('Most fibres',4.65,2,30,YELLOW)),run_time=.3)
        self.at('cross the midline'); self.play(Create(x),run_time=.55); self.play(Create(distal()),run_time=.45)
        self.at('That crossing is'); self.play(FadeIn(leader('Pyramidal\ndecussation',4.65,-.8,CX,-1.12)),
            FadeIn(label('Both pyramids cross',4.65,-2.4,26)),run_time=.4)
        self.finish()


class S05Above(SpokenScene):
    def construct(self):
        a=anatomy(); t=tract(); self.add(a,t,crossing()[1].set_opacity(.3))
        self.at('Damage above'); self.play(FadeIn(lesion(CX+.85,1.9)),run_time=.3)
        self.at('shows up'); self.play(ShowPassingFlash(upper().set_stroke(width=12),time_width=.5),run_time=.55)
        self.at('opposite side'); self.play(a[4].animate.set_stroke(opacity=.2),FadeIn(result_lines('One crossing','Opposite side')),run_time=.35)
        self.finish()


class S06Below(SpokenScene):
    def construct(self):
        a=anatomy(); x=crossing(); self.add(a,tract(),x)
        self.at('In the cord'); self.play(FadeIn(lesion(CX-.4,-1.6)),run_time=.3)
        self.at('already crossed'); self.play(Indicate(x,color=YELLOW,scale_factor=1.2),run_time=.5)
        self.at('damage there'); self.play(Create(distal(-1,RED)),
            a[4].animate.set_stroke(opacity=.2),FadeIn(result_lines('No crossing','Same side')),run_time=.55)
        self.finish()


class S07Count1(SpokenScene):
    def construct(self):
        card=count_card(1,0).scale(1.3)
        x=VGroup(card[1][3],card[1][4]); glow=crossing_glow(x)
        self.add(card)
        self.at('first count'); self.play(FadeIn(glow),run_time=.25)
        self.play(glow.animate.set_opacity(.15),rate_func=there_and_back,run_time=.8)
        self.at('between the damage'); self.play(card[0].animate.set_stroke(YELLOW,width=4),run_time=.3)
        self.at('crossing flips'); self.play(Indicate(x,color=YELLOW,scale_factor=1.15),run_time=.7)
        self.finish()


class S08Q1(SpokenScene):
    def construct(self):
        a,x,m,q,h=question1(); self.add(a,x)
        self.at('lesion sits'); self.play(FadeIn(m),run_time=.3)
        self.at('right pyramid'); self.play(FadeIn(h),run_time=.3)
        self.at('Which limbs'); self.play(FadeIn(q),run_time=.3); self.finish()


class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; a,x,m,q,h=question1()
        glow=crossing_glow(x); self.add(a,glow,x,m,q,h,time_hint())
        for i in range(5):
            d=label(str(5-i),4.65,-2.65,30,YELLOW); self.add(d)
            self.play(glow.animate.set_opacity(.25),rate_func=there_and_back,run_time=1)
            self.remove(d)


class S10Reveal1(SpokenScene):
    def construct(self):
        a,x,m,q,h=question1(); self.add(a,x,m,h)
        self.at('The left limbs'); self.play(a[5].animate.set_stroke(opacity=.2),FadeIn(label('Left limbs',4.65,.1,32,RED)),run_time=.4)
        self.at('crossing lies below'); self.play(Create(path([(CX-.4,-.83),(CX+.4,-1.4)])),Indicate(x,scale_factor=1.5,color=YELLOW),run_time=.6)
        self.play(Create(distal(1)),run_time=.35)
        self.at('so the side'); self.play(FadeIn(label('One crossing,\nopposite side',4.65,-1.6,28,YELLOW)),run_time=.3); self.finish()


def nuclei():
    outline=Ellipse(width=7.5,height=5.6,color=GREY).move_to([-1.5,-.25,0])
    blobs=VGroup(*[Ellipse(width=2.1,height=1.4,color=BLUE,fill_color=BLUE,fill_opacity=.25).move_to([x,y,0])
                   for x,y in [(-3.6,.9),(-.9,.9),(.6,-.8)]])
    return VGroup(outline,blobs)


def bg_notes():
    return VGroup(label('Basal ganglia',0,3.15,34,BLUE),label('Classic model',4.3,1.8,26),
                  label('Movement\ngoes ahead?',4.4,-.1,28))


class S11Bg(SpokenScene):
    def construct(self):
        a=anatomy(); opening=label('Second puzzle',3.6,.6,32); self.add(a,opening)
        self.at('The basal ganglia'); self.play(FadeOut(a),FadeOut(opening),FadeIn(nuclei()),FadeIn(label('Basal ganglia',0,3.15,34,BLUE)),run_time=.65)
        self.at('never reach'); gap=VGroup(DashedLine([-.3,-1.7,0],[-.3,-2.2,0],color=GREY),
            DashedLine([-.3,-2.65,0],[-.3,-2.95,0],color=GREY),lesion(-.3,-2.42),label('No direct link to spinal cord',0,-3.35,26))
        self.play(FadeIn(gap),run_time=.4)
        self.at('classic model'); self.play(FadeIn(label('Classic model',4.3,1.8,26)),run_time=.3)
        self.at('whether a movement'); self.play(FadeIn(label('Movement\ngoes ahead?',4.4,-.1,28)),
            Create(Line([-2.55,.9,0],[-1.95,.9,0],color=RED,stroke_width=7)),
            Create(Line([-1.95,.65,0],[-1.95,1.15,0],color=RED,stroke_width=7)),run_time=.4)
        self.finish()


class S12Bg2(SpokenScene):
    def construct(self):
        self.add(nuclei(),bg_notes())
        link=VGroup(Line([-2.55,.9,0],[-1.95,.9,0],color=RED,stroke_width=7),
                    Line([-1.95,.65,0],[-1.95,1.15,0],color=RED,stroke_width=7))
        self.add(link)
        self.at('rests on inhibition'); self.play(Indicate(link,color=YELLOW,scale_factor=1.2),FadeIn(label('Inhibition',-2.3,-.2,32,RED)),run_time=.4); self.finish()


class S13Abc(SpokenScene):
    def construct(self):
        n,t,l=neurons(); self.add(circuit_labels())
        self.at('Picture three neurons'); self.play(FadeIn(n),FadeIn(t),run_time=.55)
        self.at('first inhibits'); self.play(Create(l[0]),run_time=.5)
        self.at('second inhibits'); self.play(Create(l[1]),run_time=.5); self.finish()


class S14Q2(SpokenScene):
    def construct(self):
        n,t,l=neurons(); c=circuit_labels(); self.add(n,t,l,c)
        self.at('starts firing faster'); self.play(Transform(t[0],ticks(-4,rate(0,True))),n[0][0].animate.set_fill(opacity=.65),Transform(c,circuit_labels(True)),run_time=.45)
        self.at('What does the third'); self.play(FadeIn(label('What does the third neuron do?',0,2.4,30)),run_time=.3); self.finish()


class S15Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(*question2())
        hint=label('Pause and answer · 5',0,-3.55,26,YELLOW); self.add(hint)
        for i in range(5):
            self.play(Transform(hint,label('Pause and answer · '+str(5-i),0,-3.55,26,YELLOW)),run_time=.1); self.wait(.9)


class S16Reveal2(SpokenScene):
    def construct(self):
        n,t,l,c,q=question2(); self.add(n,t,l,c,q)
        # Complete removal before answer appears; no superimposed cross-fade.
        self.play(FadeOut(q),run_time=.2)
        self.at('third fires faster'); self.play(Indicate(n[0],color=YELLOW),run_time=.35)
        self.at('first holds'); self.play(l[0][2].animate.set_color(YELLOW),
            ShowPassingFlash(l[0][0].copy().set_color(YELLOW),time_width=.5),run_time=.3)
        self.play(Transform(t[1],ticks(0,rate(1,True,True))),n[1][0].animate.set_fill(opacity=.08),
            Transform(c[3][1],label('slow',0,-3.05,26,YELLOW)),run_time=.35)
        self.at('second lets go'); self.play(l[1][2].animate.set_color(YELLOW),
            ShowPassingFlash(l[1][0].copy().set_color(YELLOW),time_width=.5),run_time=.3)
        self.play(Transform(t[2],ticks(4,rate(2,True,True))),n[2][0].animate.set_fill(opacity=.65),
            FadeIn(label('C fires faster',0,2.4,30,YELLOW)),
            Transform(c[4][1],label('fast',4,-3.05,26,YELLOW)),run_time=.4)
        self.finish()


class S17Disinh(SpokenScene):
    def construct(self):
        n,t,l=neurons(True,True); l[0][2].set_color(YELLOW); l[1][2].set_color(YELLOW)
        self.add(n,t,l,circuit_labels(True,True))
        self.at('Inhibiting an inhibitor'); self.play(Indicate(l[0][2],scale_factor=1.3),Indicate(l[1][2],scale_factor=1.3),run_time=.65)
        self.at('releases its target'); self.play(Indicate(n[2],color=YELLOW),run_time=.55)
        self.at('That is disinhibition'); self.play(FadeIn(label('Disinhibition · two flips, direction kept',0,2.4,30,YELLOW)),run_time=.3); self.finish()


def sign_example(even=True):
    y=-.65 if even else -2.25
    xs=[-3,0,3] if even else [-3,3]
    signs=[(-1)**i for i in range(len(xs))]
    g=VGroup(*[Circle(radius=.35,color=BLUE).move_to([x,y,0]) for x in xs])
    for x,s in zip(xs,signs):
        g.add(Arrow([x,y-.23*s,0],[x,y+.23*s,0],buff=0,color=YELLOW if s>0 else RED,stroke_width=5,max_tip_length_to_length_ratio=.4))
    for a,b in zip(xs[:-1],xs[1:]):
        g.add(Line([a+.4,y,0],[b-.4,y,0],color=RED,stroke_width=5),Line([b-.4,y-.2,0],[b-.4,y+.2,0],color=RED,stroke_width=5),label('−',(a+b)/2,y+.4,30,RED))
    g.add(label('Even: direction kept' if even else 'Odd: direction reversed',0,y-.7,28))
    return g


def sign_card(even=None):
    box=RoundedRectangle(width=11.8,height=5.6,corner_radius=.2,color=BLUE,
                         fill_color=BLUE,fill_opacity=.08).move_to([0,-.25,0])
    chain=sign_example(even is True)
    # Fill the card with a large, legible chain and direction arrows.
    chain.scale(1.55).move_to([0,-.65,0])
    if even is None:
        chain[-1].become(label('One link flips the direction',0,-2.45,32))
    return VGroup(box,label('Count 2 · inhibitions flip the sign',0,1.8,34,RED),chain)


class S18Count2(SpokenScene):
    def construct(self):
        first=count_card(1,-3.1); second=count_card(2,3.1)
        self.add(first)
        self.at('second count'); self.play(FadeIn(second,shift=UP*.2),run_time=.3)
        cards=VGroup(first,second)
        self.at('Each inhibitory link'); self.remove(first,second); one=sign_card(); self.add(one)
        self.at('An even number'); self.remove(one); even=sign_card(True); self.add(even)
        self.at('An odd number'); self.remove(even); self.add(sign_card(False)); self.finish()


class S19Rule(SpokenScene):
    def construct(self):
        cards=VGroup(count_card(1,-3.1),count_card(2,3.1)); self.add(cards,label('Motor pathway',0,3.2,34))
        self.at('Put them together'); frame=RoundedRectangle(width=12.4,height=5.05,color=GREY).move_to([0,-.45,0]); self.play(Create(frame),run_time=.4)
        self.at('a motor pathway'); self.wait(.1)
        self.at('follow the chain'); chain=label('Follow the chain',0,2.4,28); self.play(FadeIn(chain),run_time=.3)
        self.at('lesion or drug'); self.remove(chain); self.play(FadeIn(label('Lesion or drug  →  muscle',0,2.4,30)),run_time=.25)
        self.at('Crossings set the side'); self.play(cards[0][0].animate.set_stroke(YELLOW,width=5),Indicate(cards[0][1][3],color=YELLOW),run_time=.5)
        self.at('Inhibitions set the sign'); self.play(cards[1][0].animate.set_stroke(RED,width=5),Indicate(cards[1][1][6],color=YELLOW),run_time=.5); self.finish()


def chosen_path():
    return VGroup(anatomy(),tract(),label('Some limits',4.65,1.8,34))


def direction_pic():
    return VGroup(label('Direction, not size',0,3.2,34),
        Arrow([-3,-2,0],[-3,1.8,0],buff=0,color=YELLOW,stroke_width=9),
        label('increase',-3,-2.8,32,YELLOW),Arrow([3,1.8,0],[3,-2,0],buff=0,color=RED,stroke_width=9),
        label('decrease',3,-2.8,32,RED),label('No magnitude scale',0,.1,28))


def fixed_pic():
    n,t,l=neurons(); c=circuit_labels(heading='Fixed link signs')
    return VGroup(n,t,l,c)


def opposing_pic():
    target=Circle(radius=1.15,color=BLUE,fill_color=BLUE,fill_opacity=.2).move_to([0,-1.2,0])
    return VGroup(label('Opposing routes',0,3.2,34),target,label('?',0,-1.2,56),
        Arrow([-5,1.4,0],[-1.15,-1.1,0],buff=.05,color=YELLOW,stroke_width=9),
        Arrow([5,1.4,0],[1.15,-1.1,0],buff=.05,color=RED,stroke_width=9),
        label('increase',-4.6,2.15,28,YELLOW),label('decrease',4.6,2.15,28,RED),
        label('?',-3,-1.5,40),label('?',3,-1.5,40))


def face_picture():
    # Frontal convention: patient right = screen left. Cortex markers sit in
    # actual cortex cartoons above the centred face, never on label chips.
    face=Ellipse(width=4.2,height=6.6,color=GREY).move_to([0,-.15,0])
    eyes=VGroup(Dot([-.65,-.35,0],color=TEXT),Dot([.65,-.35,0],color=TEXT))
    forehead=RoundedRectangle(width=2.5,height=.6,corner_radius=.15,color=BLUE,fill_color=BLUE,fill_opacity=.65).move_to([0,1.1,0])
    lower=VGroup(Line([-1.1,-1.9,0],[-.15,-1.9,0],color=BLUE,stroke_width=12),Line([.15,-1.9,0],[1.1,-1.9,0],color=BLUE,stroke_width=12))
    cortices=VGroup(*[Ellipse(width=1.8,height=.85,color=BLUE,fill_color=BLUE,fill_opacity=.2).move_to([x,2.4,0]) for x in [-3.7,3.7]])
    labels=VGroup(label('Right cortex',-3.7,3.2,28),label('Left cortex',3.7,3.2,28),label("Patient's right",-3.9,-3.25,26))
    arrows=VGroup(Arrow([-3.1,2.05,0],[-.6,1.43,0],buff=.1,color=YELLOW),
                   Arrow([3.1,2.05,0],[.6,1.43,0],buff=.1,color=YELLOW),
                   VGroup(path([(3.7,1.95),(2.4,1.3),(2.4,-2.5),(-.8,-2.5)],YELLOW,5),
                          Arrow([-.8,-2.5,0],[-.8,-2.02,0],buff=0,color=YELLOW,stroke_width=5,max_tip_length_to_length_ratio=.35)))
    return VGroup(face,eyes,forehead,lower,cortices,labels,arrows)


class S20Scope(SpokenScene):
    def switch(self,old,new):
        self.clear(); self.add(new)
    def construct(self):
        pic=chosen_path(); self.add(pic)
        self.at('one chosen path'); self.play(Transform(pic[-1],label('One chosen\npath',4.65,1.8,32)),pic[1].animate.set_color(YELLOW),run_time=.35)
        self.at('not its size'); new=direction_pic(); self.switch(pic,new); pic=new
        self.at('fixed sign'); new=fixed_pic(); self.switch(pic,new); pic=new
        self.play(Indicate(pic[2],color=YELLOW,scale_factor=1.06),run_time=.4)
        self.at('can still change'); live_n,live_t,_=neurons(True,True)
        self.play(Transform(pic[0],live_n),Transform(pic[1],live_t),
            Transform(pic[3],circuit_labels(True,True,heading='Neurons must still be able to respond')),run_time=.4)
        self.at('pull in opposite'); new=opposing_pic(); self.switch(pic,new); pic=new
        self.at('net effect depends'); strength=label('Net change needs both route strengths',0,-2.65,30); self.play(FadeIn(strength),run_time=.35); pic.add(strength)
        self.at('input from both sides'); new=face_picture(); self.switch(pic,new); pic=new
        self.at('cortical lesion'); self.play(FadeIn(lesion(3.7,2.4)),pic[6][1].animate.set_opacity(.18),pic[6][2][0].animate.set_stroke(opacity=.18),pic[6][2][1].animate.set_opacity(.18),run_time=.4)
        self.at('forehead is usually'); self.play(FadeIn(leader('Forehead\nusually relatively\nspared',-4.35,1.1,-1.25,1.1,BLUE,26)),run_time=.35)
        self.at('lower face'); self.play(pic[3][0].animate.set_opacity(.18),FadeIn(leader('Lower face\nweakens more',-4.3,-1.65,-1.1,-1.9,RED,26)),run_time=.35); self.finish()


class S21Takeaway(SpokenScene):
    def construct(self):
        # A quiet chain occupies the frame before the words arrive.
        self.add(VGroup(Dot([-3,-1.8,0],color=BLUE),Dot([0,-1.8,0],color=BLUE),Dot([3,-1.8,0],color=BLUE),
                        Arrow([-2.8,-1.8,0],[-.2,-1.8,0],color=YELLOW,buff=0),Arrow([.2,-1.8,0],[2.8,-1.8,0],color=YELLOW,buff=0)))
        self.at('Follow the chain'); self.play(FadeIn(label('Follow the chain,',0,.8,44)),run_time=.3)
        self.at('count what flips'); self.play(FadeIn(label('and count what flips.',0,-.3,44,YELLOW)),run_time=.3); self.finish()


class S22End(EndCard):
    LINE='Follow the chain, and count what flips.'
    def construct(self):
        self.add(label('biochemistrypedia.com',0,.8,38,TEAL),label('Next: The Brake and Its Two Routes',0,-.5,32))
        self.wait(self.narration_s)
