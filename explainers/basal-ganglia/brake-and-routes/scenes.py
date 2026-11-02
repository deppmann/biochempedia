"""The Brake and Its Two Routes — reviewed redraw.
COLOR MAP: BLUE neural populations; RED inhibition/brake/akinesia;
GREEN excitation/toward movement; GOLD SNc/dopamine; YELLOW firing/counting;
TEXT labels and schematic notes. Historical bars and ticks are qualitative,
not measurements. Sign counts are computed from signed classic-model routes.
"""
from bp_style import *
import numpy as np

NOTE = '#C5CBD5'
LOW, MID, HIGH = .035, .23, .65
TAKEAWAY = 'Inhibit an inhibitor, and you release its target.'
SIGN = {'direct': [1, -1, -1], 'indirect': [-1, -1, -1, 1, -1]}

# Same word timing, without modifying the read-only sync.log during this round.
class SpokenScene(SpokenScene):
    def at(self, phrase, lead=.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > .02:
            self.wait(rest)


def label(text, x=0, y=3.35, size=30, color=TEXT):
    return T(text, size, color).move_to([x, y, 0])


def node(text, x, y, w=3.5, h=.82, color=BLUE):
    box = RoundedRectangle(width=w, height=h, corner_radius=.13,
                           stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=MID)
    name = T(text, 28).move_to(box)
    return VGroup(box, name).move_to([x, y, 0])


def signed_arrow(start, end, sign=None, offset=RIGHT*.4, color=None):
    c = color or (RED if sign == -1 else GREEN if sign == 1 else NOTE)
    a = Arrow(start, end, buff=0, color=c, stroke_width=6,
              max_tip_length_to_length_ratio=.22)
    out = VGroup(a)
    if sign is not None:
        badge=chip('−' if sign < 0 else '+', c, 44, pad=.16,fill_opacity=.3)
        badge[0].stretch_to_fit_width(max(.82,badge[0].width))
        badge[0].stretch_to_fit_height(max(.68,badge[0].height))
        out.add(badge.move_to((np.array(start)+np.array(end))/2+offset))
    return out


def link(a, b, sign=None, offset=RIGHT*.4):
    p, q = a.get_center(), b.get_center()
    v = q-p
    def clip(m):
        return min(m.width/2/abs(v[0]) if abs(v[0]) > 1e-6 else 1e9,
                   m.height/2/abs(v[1]) if abs(v[1]) > 1e-6 else 1e9)
    u = v/np.linalg.norm(v)
    return signed_arrow(p+v*clip(a)+u*.06, q-v*clip(b)-u*.06, sign, offset)


def rename(scene, n, text):
    # Crossfade labels; never morph unrelated text into scrambled glyphs.
    new = T(text, 28).move_to(n[0])
    scene.play(FadeOut(n[1]), run_time=.12)
    scene.play(FadeIn(new), run_time=.18)
    n.submobjects[1] = new


def train(n, count=6):
    if not getattr(n, '_tick_label', False):
        n[1].shift(UP*.18)
        n._tick_label = True
    # Eight fixed slots make sparse and dense trains directly comparable.
    slots = np.linspace(-1.15, 1.15, 8)
    active = set(np.linspace(0, 7, count, dtype=int))
    return VGroup(*[Line([x,-.12,0],[x,.12,0], stroke_width=5,
                         color=YELLOW if i in active else '#404653')
                    for i,x in enumerate(slots)]).move_to(n[0].get_center()+DOWN*.23)


def foot(lifted=False):
    # Separate anatomical metaphor: ankle, heel, rounded toe and a flat sole.
    # The entire shoe moves; the pedal always stays below the sole.
    shoe = Polygon([-1.65,.5,0],[-.7,.5,0],[-.65,.05,0],
                   [.95,-.04,0],[1.55,-.2,0],[1.65,-.42,0],
                   [1.45,-.55,0],[-1.65,-.55,0],
                   color=RED, fill_color=RED, fill_opacity=.45, stroke_width=4)
    shoe.move_to([-2.7,-2.0+( .65 if lifted else 0),0])
    pedal=Line([-4.4,-2.7,0],[-.95,-2.7,0],color=NOTE,stroke_width=8)
    hinge=Dot([-4.4,-2.7,0],radius=.10,color=NOTE)
    return VGroup(shoe,pedal,hinge)


class Circuit:
    def __init__(self, indirect=False, lifted=False, dual=False, dopamine=False,
                 direct=True, placeholder=False):
        self.c=node('Cortex',-2.7,2.75 if dual else 2.95)
        self.s=node('Striatum',-2.7,1.05 if dual else 1.5,4.0 if dual else 3.5)
        self.b=node('GPi',-2.7,-.25 if dual else -.35)
        self.t=node('Thalamus',-2.7,-3.25)
        self.f=foot(lifted)
        # A wide curved return keeps the cortical destination visible throughout.
        self.back=CurvedArrow([-4.55,-3.25,0],[-4.55,self.c.get_y(),0],angle=-PI/1.9,
                              color=NOTE,stroke_width=5,tip_length=.18)
        self.cs=link(self.c,self.s)
        self.d=link(self.s,self.b,-1,LEFT*.55)
        self.bt=signed_arrow([-4.75,self.b.get_y(),0],[-4.75,-3.2,0],-1,LEFT*.50)
        self.g=node('' if placeholder else 'GPe',3.1,1.05 if dual else 1.5,2.7)
        self.n=node('' if placeholder else 'STN',3.1,-.85,2.7)
        self.sg=link(self.s,self.g,-1,UP*.49)
        self.gn=link(self.g,self.n,-1,RIGHT*.48)
        self.nb=link(self.n,self.b,1,DOWN*.52)
        self.parts=[self.back,self.cs,self.c,self.s,self.b,self.t,self.bt,self.f]
        if direct: self.parts += [self.d]
        if indirect: self.parts += [self.g,self.n,self.sg,self.gn,self.nb]
        self.dual=dual
        if dual:
            self.s[1].become(T('Striatum',26).move_to([-2.7,1.73,0]))
            self.d1=node('D1 cells',-3.7,1.05,1.8,.70)
            self.d2=node('D2 cells',-1.7,1.05,1.8,.70)
            self.parts += [self.d1,self.d2]
            self.parts.remove(self.cs)
            self.cs=VGroup(Line([-4.45,2.75,0],[-4.9,2.75,0],color=NOTE,stroke_width=4),
                Line([-4.9,2.75,0],[-4.9,1.05,0],color=NOTE,stroke_width=4),
                Arrow([-4.9,1.05,0],[-4.7,1.05,0],buff=0,color=NOTE,stroke_width=4))
            self.parts.append(self.cs)
        self.sc=node('SNc',3.1,2.75,2.7,color=GOLD)
        self.da=signed_arrow([1.65,2.75,0],[-.4,1.95,0],color=GOLD)
        self.da.add(Line([-.4,1.95,0],[-3.9,1.95,0],color=GOLD,stroke_width=4))
        self.daname=label('dopamine',.4,3.03,26,GOLD)
        self.da1=signed_arrow([-3.9,1.95,0],[-3.9,1.48,0],1,LEFT*.48)
        self.da2=signed_arrow([-1.4,1.95,0],[-1.4,1.48,0],-1,RIGHT*.48)
        if dopamine: self.parts += [self.sc,self.da,self.daname,self.da1,self.da2]
    def add(self, scene): scene.add(*self.parts)
    def activity(self, scene, gpi=False):
        scene.add(train(self.s,7),train(self.g,2),train(self.n,7))
        if gpi: scene.add(train(self.b,7))
        scene.add(label('Firing ticks: schematic',2.6,-3.3,26,NOTE))
    def loss(self):
        self.d[0].set_stroke(width=3,opacity=.5)
        self.d[1][0].set_fill(opacity=.22).set_stroke(opacity=.85)
        self.d[1][1].set_opacity(1)
        for e in [self.sg,self.gn,self.nb]: e[0].set_stroke(width=9)
        self.g[0].set_fill(opacity=LOW)
        self.n[0].set_fill(opacity=HIGH)


def column(named=False):
    return [node(t,-2.7,y) for t,y in zip(
        ['Cortex','Striatum' if named else 'Input stage',
         'GPi' if named else 'Output stage','Thalamus'],[2.95,1.5,-.35,-3.25])]


def loopback(ns):
    return CurvedArrow([-4.55,-3.25,0],[-4.55,2.95,0],angle=-PI/1.9,
                       color=NOTE,stroke_width=5,tip_length=.18)


def counter(scene, text, old=None, x=2.5, y=-2.3, color=YELLOW):
    new=label(text,x,y,30,color)
    if old is None: scene.play(FadeIn(new),run_time=.24)
    else: scene.play(FadeOut(old),FadeIn(new),run_time=.24)
    return new


def pulse(scene, e, color=YELLOW):
    scene.play(Indicate(e[0],color=color,scale_factor=1.02),
               Indicate(e[1],color=color,scale_factor=1.28),run_time=.42)
    e[1][0].set_fill(color,opacity=.55)


def early_key(scene, text='Cortex → striatum\nGPi → thalamus\nThalamus → cortex'):
    title=label('Circuit key',2.8,.55,32,NOTE)
    lines=label(text,2.8,-.65,28,NOTE)
    scene.add(title,lines)


def dim_thalamus(box):
    return box.animate.set_fill('#151C27',opacity=1).set_stroke('#36505D',width=2)


def da_state():
    d=Circuit(True,dual=True,dopamine=True)
    d.d1[0].set_fill(GREEN,opacity=.5)
    d.d2[0].set_fill(RED,opacity=.5)
    return d


def question():
    return label('Dopamine:\ntoward movement or away?',3,-2.05,28)


def chain(which):
    names=['SNc\nDA','Striatum\n'+which]
    names += ['GPi','Thalamus'] if which=='D1' else ['GPe','STN','GPi','Thalamus']
    widths=[1.05,1.5]+([1.8,2.1] if which=='D1' else [.9,.9,.9,1.55])
    gap=(13.5-sum(widths))/(len(widths)-1)
    x=-6.75; ns=[]
    for i,(name,w) in enumerate(zip(names,widths)):
        n=node(name,x+w/2,0,w,1.6,GOLD if i==0 else BLUE)
        n[1].become(fit(T(name,24),w-.1).move_to(n[0]))
        ns.append(n); x+=w+gap
    es=[link(a,b,sign,UP*1.35) for a,b,sign in zip(ns,ns[1:],SIGN['direct' if which=='D1' else 'indirect'])]
    es[0][1][0].set_fill(GOLD,opacity=.8).set_stroke(GOLD,width=4)
    es[0][1][1].set_color(BG)
    return ns,es


class S00Title(TitleCard):
    LESSON='Descending Control and the Basal Ganglia'
    TITLE='The Brake and Its Two Routes'

    def construct(self):
        brand=label('BIOCHEMISTRYPEDIA',0,1.5,26,TEAL)
        lesson=label(self.LESSON.upper(),0,.8,26,NOTE)
        title=fit(T(self.TITLE,48,font=TITLE_FONT),11.8).move_to([0,-.1,0])
        rule=Line([-1.2,-.8,0],[1.2,-.8,0],color=GOLD,stroke_width=4)
        self.play(FadeIn(brand),FadeIn(lesson),run_time=.45)
        self.play(FadeIn(title),Create(rule),run_time=.55)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        q=label('How can nuclei with no line to the cord\ndecide whether a movement goes ahead?',0,2.9,32)
        outline=Ellipse(width=7.5,height=5.6,color=GREY).move_to([-1.5,-.25,0])
        nuclei=VGroup(*[Ellipse(width=2.1,height=1.4,color=BLUE,fill_color=BLUE,fill_opacity=.25)
                         .move_to([x,y,0]) for x,y in [(-3.6,.9),(-.9,.9),(.6,-.8)]])
        picture=VGroup(outline,nuclei).scale(.86).move_to([-2.65,-.3,0])
        cord=node('Spinal cord',4.0,-1.65,3.4,1.3)
        gap=DashedLine(picture.get_right()+RIGHT*.1,cord.get_left()+UP*.35,color=NOTE,stroke_width=4)
        cross=Cross(stroke_color=RED,stroke_width=5).scale(.22).move_to(gap)
        self.add(q,picture,cord,gap,cross,
                 label('Deep nuclei',-2.65,-3.25,30,BLUE),label('No descending link',3.9,.6,26,NOTE))
        self.at('How can nuclei'); self.play(Indicate(nuclei,color=YELLOW),run_time=.6)
        self.finish()


class S02Column(SpokenScene):
    def construct(self):
        ns=column(); early_key(self,'Cortex · top\nInput · receives\nOutput · sends'); self.add(label('A loop through deep nuclei',2.25,2.7,28,NOTE))
        self.at('Start with a picture')
        self.play(LaggedStart(*[FadeIn(n[0]) for n in ns],lag_ratio=.15),run_time=.8)
        self.at('The cortex is');self.play(FadeIn(ns[0][1]),run_time=.35)
        self.at('then an input');self.play(FadeIn(ns[1][1]),run_time=.35)
        self.finish()


class S03Stages(SpokenScene):
    def construct(self):
        ns=column();early_key(self);self.add(*[n[0] for n in ns],ns[0][1],ns[1][1])
        a=link(ns[2],ns[3]); cs=link(ns[0],ns[1]); io=link(ns[1],ns[2]);back=loopback(ns)
        self.add(cs,io,label('Cortex → input → output',2.15,1.8,28,NOTE))
        self.at('An output stage');self.play(FadeIn(ns[2][1]),run_time=.35)
        self.at('feeds the thalamus');self.play(Create(a),FadeIn(ns[3][1]),run_time=.45)
        self.at('which sends an arrow');self.play(Create(back),run_time=.65)
        self.at('closing a loop')
        self.play(Succession(*[Indicate(m,color=YELLOW,scale_factor=1.04) for m in [ns[0],cs,ns[1],io,ns[2],a,ns[3],back]]),run_time=1.2)
        self.finish()


class S04Names(SpokenScene):
    def construct(self):
        ns=column();self.add(*ns,link(ns[2],ns[3]),loopback(ns),link(ns[0],ns[1]),link(ns[1],ns[2]))
        self.at('input stage is');rename(self,ns[1],'Striatum')
        self.play(FadeIn(label('Striatum · input stage\nCorpus striatum',2.4,1.5,28)),run_time=.3)
        self.at('internal globus pallidus');rename(self,ns[2],'GPi')
        text=label('GPi\nInternal globus pallidus',2.4,-.35,28)
        leader=Line(ns[2].get_right()+RIGHT*.1,text.get_left()+LEFT*.1,color=NOTE,stroke_width=3)
        self.play(FadeIn(text),Create(leader),run_time=.4);self.finish()


class S05Brake(SpokenScene):
    def construct(self):
        d=Circuit();early_key(self,'−  Inhibition\nTicks · firing at rest');self.add(d.c,d.cs,d.s,d.b,d.t,d.back)
        self.add(label('Steady output at rest',2.5,1.4,30,NOTE))
        self.at('are inhibitory');self.play(Create(d.bt),run_time=.4)
        self.at('fire steadily');self.play(FadeIn(train(d.b,5)),run_time=.45)
        self.at('held down');self.play(dim_thalamus(d.t[0]),run_time=.4)
        self.at('like a foot');self.play(FadeIn(d.f),run_time=.5)
        self.add(label('Firing ticks: schematic',2.5,-3.3,26,NOTE));self.finish()


class S06Lift(SpokenScene):
    def construct(self):
        d=Circuit();d.add(self);self.add(train(d.b,5));early_key(self,'−  Inhibition\nBrighter thalamus · released')
        self.at('In the classic model');self.play(FadeIn(label('Classic model',2.4,2.4,30,NOTE)),run_time=.3)
        self.at('movement needs');self.play(d.f[0].animate.shift(UP*.65),d.t[0].animate.set_fill(opacity=HIGH),
            FadeIn(label('Movement needs\nthe brake lifted',2.5,-1.6,32,GREEN)),run_time=.6)
        self.finish()


class S07Routes(SpokenScene):
    def construct(self):
        d=Circuit(True,lifted=True,placeholder=True)
        self.add(d.c,d.cs,d.s,d.b,d.t,d.back,d.bt,d.f)
        self.at('Two roots run')
        self.play(Create(d.d),FadeIn(d.g),FadeIn(d.n),Create(d.sg),Create(d.gn),Create(d.nb),run_time=.9)
        self.add(label('Two routes',3.1,2.4,30))
        self.at('are inhibitory');pulse(self,d.d);pulse(self,d.sg)
        self.finish()


class S08Direct(SpokenScene):
    def construct(self):
        d=Circuit();d.add(self);self.add(train(d.b,5))
        early_key(self,'−  Striatum → GPi\n−  GPi → thalamus')
        self.at('direct route');self.play(d.d[0].animate.set_stroke(YELLOW,width=9),FadeIn(label('Direct route',2.7,2.5,32)),run_time=.3)
        self.at('with D1 receptors');rename(self,d.s,'Striatum · D1')
        self.at('inhibit the');pulse(self,d.d)
        self.at('inhibits the thalamus');pulse(self,d.bt)
        self.finish()


class S09Direct2(SpokenScene):
    def construct(self):
        d=Circuit();d.s[1].become(T('Striatum · D1',28).move_to(d.s));d.add(self)
        self.add(label('Direct route',2.6,2.5,32))
        early_key(self,'−  Inhibit the brake\n−  Release its target')
        self.at('Two inhibitions')
        c=counter(self,'1 flip',x=2.6,y=-2.35)
        pulse(self,d.d)
        c=counter(self,'2 flips',c,x=2.6,y=-2.35)
        pulse(self,d.bt)
        self.at('even number')
        c=counter(self,'2 flips · even',c,x=2.6,y=-2.35,color=GREEN)
        self.at('More striatal firing');self.play(FadeIn(train(d.s,7)),d.s[0].animate.set_fill(opacity=HIGH),run_time=.35)
        self.at('releases the thalamus');self.play(d.f[0].animate.shift(UP*.65),d.t[0].animate.set_fill(opacity=HIGH),run_time=.45)
        self.at('toward movement');c=counter(self,'2 flips · even · toward movement',c,x=2.6,y=-2.35,color=GREEN)
        self.finish()


class S10Indirect(SpokenScene):
    def construct(self):
        d=Circuit(True,lifted=True,direct=False,placeholder=True);d.add(self)
        self.at('indirect route takes')
        self.play(Indicate(VGroup(d.sg,d.gn,d.nb),color=YELLOW,scale_factor=1.02),FadeIn(label('Indirect route',2.8,2.6,32)),run_time=.55)
        self.at('with D2 receptors');rename(self,d.s,'Striatum · D2')
        self.at('inhibit the external');rename(self,d.g,'GPe');pulse(self,d.sg)
        self.finish()


class S11Indirect2(SpokenScene):
    def construct(self):
        d=Circuit(True,lifted=True,direct=False,placeholder=True)
        d.s[1].become(T('Striatum · D2',28).move_to(d.s));d.g[1].become(T('GPe',28).move_to(d.g));d.add(self)
        self.add(label('Indirect route',2.8,2.6,32))
        self.at('inhibits the subthalamic');rename(self,d.n,'STN');pulse(self,d.gn)
        self.at('excites the');pulse(self,d.nb)
        self.finish()


class S12Walk(SpokenScene):
    def construct(self):
        d=Circuit(True,lifted=True,direct=False);d.s[1].become(T('Striatum · D2',28).move_to(d.s));d.add(self)
        self.add(label('Indirect route',2.8,2.6,32),label('Firing ticks: schematic',2.6,-3.3,26,NOTE))
        self.at('D2 neurons fire more');self.play(FadeIn(train(d.s,7)),d.s[0].animate.set_fill(opacity=HIGH),run_time=.4)
        self.at('GPE fires less');self.play(FadeIn(train(d.g,2)),d.g[0].animate.set_fill(opacity=LOW),run_time=.4)
        self.at('freed STN fires more');self.play(FadeIn(train(d.n,7)),d.n[0].animate.set_fill(opacity=HIGH),run_time=.4)
        self.finish()


class S13Walk2(SpokenScene):
    def construct(self):
        d=Circuit(True,lifted=True,direct=False);d.s[1].become(T('Striatum · D2',28).move_to(d.s));d.add(self)
        d.g[0].set_fill(opacity=LOW);d.n[0].set_fill(opacity=HIGH);d.activity(self)
        self.add(label('Indirect route',2.8,2.6,32))
        self.at('fires more');self.play(FadeIn(train(d.b,7)),d.b[0].animate.set_fill(opacity=HIGH),run_time=.45)
        self.at('held down harder');self.play(d.f[0].animate.shift(DOWN*.65),dim_thalamus(d.t[0]),run_time=.55)
        self.finish()


class S14Three(SpokenScene):
    def construct(self):
        d=Circuit(True,direct=False);d.s[1].become(T('Striatum · D2',28).move_to(d.s));d.add(self);d.activity(self,True)
        d.t[0].set_fill('#151C27',opacity=1).set_stroke('#36505D',width=2)
        self.at('Three inhibitions')
        c=None
        for i,e in enumerate([d.sg,d.gn,d.bt],1):
            c=counter(self,f'{i} flip'+('s' if i>1 else ''),c,x=2.8,y=-2.1);pulse(self,e)
        self.at('odd number');c=counter(self,'3 flips · odd',c,x=2.8,y=-2.1,color=RED)
        self.at('away from movement');self.play(FadeIn(label('Away from movement',2.8,2.6,30,RED)),run_time=.35)
        self.finish()


class S15Dopamine(SpokenScene):
    def construct(self):
        d=Circuit(True,dual=True);d.add(self)
        self.at('add dopamine');self.play(FadeIn(d.sc),run_time=.35)
        self.at('from the substantia');self.play(Create(d.da),FadeIn(d.daname),run_time=.5)
        self.at('It acts on the first box')
        particles=VGroup(*[Dot(d.da[0].get_start(),radius=.08,color=GOLD) for _ in range(5)])
        self.add(particles)
        self.play(LaggedStart(*[p.animate.move_to(d.s.get_top()+RIGHT*(i-2)*.55) for i,p in enumerate(particles)],lag_ratio=.12),run_time=.8)
        self.remove(particles)
        self.at('one more link');self.play(Create(d.da1),Create(d.da2),run_time=.5)
        self.finish()


class S16Da2(SpokenScene):
    def construct(self):
        d=Circuit(True,dual=True,dopamine=True);d.add(self)
        self.add(label('Classic model',2.9,-2.8,30,NOTE))
        self.at('dopamine excites');self.play(d.d1[0].animate.set_fill(GREEN,opacity=.5),Indicate(d.da1[1],color=GREEN),
            FadeIn(label('excites',-3.7,2.15,26,GREEN)),run_time=.5)
        self.at('inhibits the');self.play(d.d2[0].animate.set_fill(RED,opacity=.5),Indicate(d.da2[1],color=RED),
            FadeIn(label('inhibits',-1.6,2.15,26,RED)),run_time=.5)
        self.finish()


class S17Q(SpokenScene):
    def construct(self):
        d=da_state();d.add(self);self.add(label('Classic model',3,-3.2,30,NOTE))
        self.at('Acting through each receptor');self.play(Indicate(d.da1[1]),Indicate(d.da2[1]),run_time=.6)
        self.at('does dopamine push');self.play(FadeIn(question()),run_time=.4);self.finish()


class S18Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;d=da_state();d.add(self)
        self.add(label('Classic model',3,-3.2,30,NOTE),question());self.wait(5)


class S19Reveal(SpokenScene):
    def construct(self):
        ns,es=chain('D1');self.add(*es,*ns,label('D1 · Classic model',0,3.2,32,NOTE))
        self.at('Toward movement both ways');self.play(FadeIn(label('Toward movement · both ways',0,-3.0,32,GREEN)),run_time=.35)
        self.at('Through D1')
        c=counter(self,'0 flips',x=0,y=-1.65)
        for sign,e in zip(SIGN['direct'],es):
            self.play(Indicate(e[1],color=GOLD if e is es[0] else YELLOW,scale_factor=1.25),run_time=.22)
            count=sum(s<0 for s in SIGN['direct'][:es.index(e)+1])
            c=counter(self,f'{count} flips',c,x=0,y=-1.65)
        self.at('adds no flip');self.play(FadeIn(label('Dopamine +: 0   ·   route: 2   ·   even',0,2.35,28)),run_time=.35)
        assert np.prod(SIGN['direct'])==1;self.finish()


class S20Reveal2(SpokenScene):
    def construct(self):
        ns,es=chain('D2');self.add(*es,*ns,label('D2 · Classic model',0,3.2,32,NOTE))
        self.at('its own inhibition');pulse(self,es[0],GOLD)
        c=counter(self,'1 flip · dopamine',x=0,y=-1.65,color=GOLD)
        self.at('adds one flip')
        count=1
        for s,e in zip(SIGN['indirect'][1:],es[1:]):
            pulse(self,e)
            count+=int(s<0)
            c=counter(self,f'{count} flips'+(' · + adds none' if s>0 else ''),c,x=0,y=-1.65)
        self.at('Four flips');c=counter(self,'4 flips · even · toward movement',c,x=0,y=-1.65,color=GREEN)
        self.play(FadeIn(label('STN → GPi: + adds no flip',0,2.65,28,GREEN)),run_time=.35)
        assert np.prod(SIGN['indirect'])==1;self.finish()


class S21Loss(SpokenScene):
    def construct(self):
        d=da_state();d.add(self);self.add(train(d.b,7),train(d.g,2),train(d.n,7),label('Classic model',2.9,-3.1,28,NOTE))
        self.at('The two actions agree');self.play(Indicate(d.da1[1]),Indicate(d.da2[1]),run_time=.45)
        self.at('losing dopamine');self.play(d.sc.animate.set_opacity(.18),d.da.animate.set_opacity(.18),
            d.da1.animate.set_opacity(.3),d.da2.animate.set_opacity(.3),run_time=.5)
        self.at('less movement');self.play(FadeIn(label('Dopamine loss →\nless movement',2.9,-2.15,29,RED)),run_time=.35)
        self.at('direct route weakens');self.play(d.d[0].animate.set_stroke(width=3,opacity=.5),run_time=.4)
        self.at('indirect strengthens');self.play(*[e[0].animate.set_stroke(width=9) for e in [d.sg,d.gn,d.nb]],
            d.g[0].animate.set_fill(opacity=LOW),d.n[0].animate.set_fill(opacity=HIGH),
            FadeIn(label('less firing',3.1,1.8,26,NOTE)),FadeIn(label('more firing',3.1,-1.55,26,NOTE)),run_time=.45)
        self.finish()


class S22Two(SpokenScene):
    def construct(self):
        d=Circuit(True,dual=True);d.loss();d.add(self)
        self.add(label('Dopamine loss\nClassic model',2.9,2.6,29,NOTE))
        self.at('brake fires more');self.play(FadeIn(train(d.b,7)),d.b[0].animate.set_fill(opacity=HIGH),run_time=.4)
        self.at('Less inhibition from')
        self.remove(d.d)
        force1=signed_arrow(d.d1.get_left()+LEFT*.07,[-4.35,-1.5,0],color=RED)
        force1[0].set_stroke(width=3)
        less=label('Less\ninhibition',-5.65,-.22,24,RED)
        self.play(FadeIn(less),Create(force1),run_time=.4)
        self.at('more excitation from')
        force2=signed_arrow(d.n.get_bottom()+DOWN*.05,[-1.05,-2.0,0],color=GREEN)
        force2[0].set_stroke(width=10)
        more=label('More excitation',1.0,-2.15,26,GREEN)
        self.play(FadeIn(more),Create(force2),d.f[0].animate.shift(DOWN*.12),run_time=.5)
        self.finish()


class S23Akinesia(SpokenScene):
    def construct(self):
        d=Circuit(True,dual=True,direct=False);d.f[0].shift(DOWN*.20);d.f[1:].shift(DOWN*.12);d.add(self);d.t[0].set_fill('#151C27',opacity=1).set_stroke('#36505D',width=2)
        self.add(train(d.b,7))
        self.at('held down harder')
        self.play(FadeIn(label('Held down harder',2.75,-2.0,30,RED)),
            FadeIn(label('Akinesia\nClassic model’s prediction',2.75,-2.95,28,NOTE)),run_time=.4)
        self.at('movement is hard to start');self.play(FadeIn(label('Movement is\nhard to start',2.8,2.5,30)),run_time=.4)
        self.finish()


class S24History(SpokenScene):
    def construct(self):
        heading=label('The dopamine-loss premise rests on a measurement',0,3.15,30)
        citation=label('Ehringer and Hornykiewicz, 1960',0,2.45,28,NOTE)
        note=label('Schematic · arbitrary units, not measured values',0,1.85,24,NOTE)
        for m in [heading,citation,note]: m.align_to(LEFT*5.1,LEFT)
        self.add(heading,citation,note)
        base=Line([-4.7,-2.65,0],[5.7,-2.65,0],color=NOTE,stroke_width=4)
        axis=Arrow([-4.7,-2.65,0],[-4.7,1.35,0],buff=0,color=NOTE,stroke_width=4)
        axisname=label('Striatal dopamine',-5.8,-.35,26,NOTE).rotate(PI/2)
        self.add(base,axis,axisname)
        ctrl=Rectangle(width=2.5,height=3.7,color=BLUE,fill_color=BLUE,fill_opacity=.65).move_to([-1.95,-.8,0])
        pd=ctrl.copy().move_to([3.1,-.8,0])
        self.at('rests on a measurement');self.play(FadeIn(ctrl),FadeIn(pd),
            FadeIn(label('Control',-1.95,-3.0,28)),FadeIn(label('Parkinson’s',3.1,-3.0,28)),run_time=.5)
        self.at('greatly reduced')
        self.play(pd.animate.stretch_to_fit_height(.65).align_to(base,DOWN),run_time=.7)
        self.finish()


class S25Takeaway(SpokenScene):
    def construct(self):
        ns=[node(name,x,0,2.8,1.3) for name,x in [('Striatum',-4.7),('GPi',0),('Thalamus',4.7)]]
        es=[link(ns[0],ns[1],-1,UP*.95),link(ns[1],ns[2],-1,UP*.95)]
        self.add(*ns)
        self.at('Inhibit');self.play(Create(es[0]),run_time=.4)
        self.at('an inhibitor');self.play(Create(es[1]),run_time=.4)
        self.at('you release its target');self.play(ns[2][0].animate.set_fill(opacity=HIGH),run_time=.5)
        self.finish()


class S26End(EndCard):
    LINE=TAKEAWAY

    def construct(self):
        line=fit(T(self.LINE,40,font=TITLE_FONT),11.7).move_to([0,.3,0])
        sub=label('biochemistrypedia.com',0,-.65,26,NOTE)
        self.play(FadeIn(line),run_time=.5)
        self.play(FadeIn(sub),run_time=.35)
        self.finish()
