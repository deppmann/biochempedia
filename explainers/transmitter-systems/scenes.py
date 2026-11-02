"""Three Steps, One Drug. Schematic icons only; no quantitative traces.
COLOR MAP: ORANGE source; YELLOW transmitter; BLUE receptor; TEAL removal;
PURPLE drug; GREEN stronger inhibition; RED weaker/block; GOLD question; GREY membrane.
"""
import numpy as np
from bp_style import *
ORANGE='#F29E4C'
PURPLE='#B58CD9'


def heading(s,color=TEXT):
    return T(s,32,color).move_to([0,3.55,0])

def arr(a,b,color=GREY):
    return Arrow(a,b,buff=.03,color=color,stroke_width=5,tip_length=.2)

def xmark(p,r=.25):
    p=np.array(p)
    return VGroup(Line(p+[-r,-r,0],p+[r,r,0],color=RED,stroke_width=6),Line(p+[-r,r,0],p+[r,-r,0],color=RED,stroke_width=6))

def dot(pos,color=YELLOW,r=.28):
    return Dot(pos,radius=r,color=color)

def channel(x=-2.8,y=-1.35):
    return VGroup(*[RoundedRectangle(width=.32,height=1.0,corner_radius=.1,color=BLUE,fill_opacity=.4).move_to([x+dx,y,0]) for dx in [-.28,.28]])

def gpcr(x=.8,y=-1.35):
    return RoundedRectangle(width=.65,height=1.05,corner_radius=.15,color=BLUE,fill_opacity=.35).move_to([x,y,0])

def synapse(labels=False,gaba=False,notch_visible=False):
    term=RoundedRectangle(width=10.8,height=1.3,corner_radius=.3,color=ORANGE,fill_opacity=.12).move_to([0,1.95,0])
    membrane=Rectangle(width=10.8,height=.22,color=GREY,fill_opacity=.4).move_to([0,-1.5,0])
    cell=RoundedRectangle(width=10.8,height=1.2,corner_radius=.15,color=GREY,fill_opacity=.06).move_to([0,-2,0])
    ch=channel(); gp=gpcr(); tr=RoundedRectangle(width=.7,height=.8,corner_radius=.1,color=TEAL,fill_opacity=.3).move_to([4,1.3,0])
    notch=Circle(.13,color=PURPLE).move_to([-3.25,-1.25,0]).set_opacity(1 if notch_visible else 0)
    g=VGroup(term,membrane,cell,ch,gp,tr,notch)
    if labels:
        g.add(T('1 Released • source',26,ORANGE).move_to([-3.7,3.15,0]),T('2 Read • readers',26,BLUE).move_to([0,3.15,0]),T('3 Removed',26,TEAL).move_to([3.8,3.15,0]))
    if gaba:
        # Target labels sit below the membrane; docking labels sit above it.
        g.add(T('GABA',30,YELLOW).move_to([-3.8,1.8,0]),T('GABA-A',26,BLUE).move_to([-2.8,-2.2,0]),T('GABA-B',26,BLUE).move_to([.8,-2.2,0]),T('GAT1',26,TEAL).move_to([4,.65,0]))
    return g

NAMES=['baclofen','bicuculline','diazepam','tiagabine']
def drug_positions():
    return [(.8,-.4,0),(-2.8,-.4,0),(-5,-.65,0),(4,2.05,0)]
TARGETS=[(.8,-.82,0),(-2.8,-.85,0),(-3.25,-1.25,0),(4,1.3,0)]
def drug(i):
    p=drug_positions()[i]
    c=chip(NAMES[i],PURPLE,size=26,pad=.13).move_to(p)
    start=c.get_bottom() if i!=2 else c.get_right()
    return VGroup(Line(start,TARGETS[i],color=PURPLE,stroke_width=3),c)
def drugset():
    return VGroup(*[drug(i) for i in range(4)])
def drug_arrow(i,up=True):
    c=drug(i)[1]; x=c.get_left()[0]-.25 if i==2 else c.get_right()[0]+.25; y=c.get_y()
    return arr([x,y-.28 if up else y+.28,0],[x,y+.28 if up else y-.28,0],GREEN if up else RED)

def quiz():
    anatomy=VGroup(synapse(False,True,True),drugset()).scale(.72).shift(DOWN*1.45)
    return VGroup(anatomy[0],anatomy[1],T('Mature synapse: GABA inhibits',26).move_to([0,-3.65,0]),T('Stronger or weaker?',36,GOLD).move_to([1.7,2.75,0]),T('Decide for each drug',28,GOLD).move_to([1.7,1.9,0]),Circle(1.55,color=GOLD,stroke_width=9).move_to([-4.6,2.05,0]))

def heart(x):
    dish=RoundedRectangle(width=4,height=3,corner_radius=.35,color=GREY,fill_color=BLUE,fill_opacity=.1).move_to([x,.3,0])
    h=Polygon(*[[x+a,b,0] for a,b in [(-.85,.6),(-.85,1.1),(-.45,1.4),(0,1.1),(.45,1.4),(.85,1.1),(.85,.6),(0,-.3)]],color=RED,fill_opacity=.5)
    nerve=VMobject(color=ORANGE,stroke_width=6).set_points_as_corners([[x-1,2.6,0],[x-.6,2.1,0],[x-.45,1.4,0]])
    return VGroup(dish,h,nerve)
def hearts():
    return VGroup(heart(-3),heart(3))
def pulse(s,h,fast=False):
    s.play(h.animate.scale(1.14),run_time=.13 if fast else .28)
    s.play(h.animate.scale(1/1.14),run_time=.13 if fast else .45)
def transfer():
    return VMobject(color=YELLOW,stroke_width=7).set_points_as_corners([[-1.3,1.3,0],[-.8,2.2,0],[.8,2.2,0],[1.4,.2,0]])

def key(color=YELLOW):
    return VGroup(Circle(.35,color=color,stroke_width=8).shift(LEFT*.8),Line([-.45,0,0],[.9,0,0],color=color,stroke_width=8),Line([.6,0,0],[.6,-.25,0],color=color,stroke_width=8),Line([.9,0,0],[.9,-.25,0],color=color,stroke_width=8))
def lock():
    box=RoundedRectangle(width=2.6,height=3,corner_radius=.2,color=BLUE,fill_opacity=.12).move_to([.5,0,0])
    shackle=Arc(radius=.7,start_angle=0,angle=PI,color=BLUE,stroke_width=7).move_to([.5,1.85,0])
    slot=Circle(.25,color=BLUE,fill_color=BG,fill_opacity=1).move_to([.9,0,0])
    return VGroup(box,shackle,slot)
def broom():
    handle=Line([4,2,0],[4,.1,0],color=TEAL,stroke_width=9)
    head=Polygon([3.65,.1,0],[4.35,.1,0],[4.8,-1.2,0],[3.2,-1.2,0],color=TEAL,fill_opacity=.35)
    bristles=VGroup(*[Line([x,-.35,0],[x,-1.2,0],color=TEAL,stroke_width=3) for x in [3.6,3.85,4.1,4.35]])
    return VGroup(handle,head,bristles)
def analogy(labels=False):
    g=VGroup(key().scale(1.5).move_to([-4,0,0]),lock(),broom())
    if labels:
        g.add(T('transmitter',30,YELLOW).move_to([-4,-2.4,0]),T('receptor',30,BLUE).move_to([.5,-2.4,0]),T('off switch:',28,TEAL).move_to([4,-2.15,0]),T('enzyme or\ntransporter',28,TEAL).move_to([4,-2.9,0]))
    return g

def focus_base():
    term=RoundedRectangle(width=10.8,height=2.2,corner_radius=.35,color=ORANGE,fill_opacity=.1).move_to([0,1.75,0])
    # Axon visibly joins the terminal at the left edge.
    axon=VGroup(Line([-6.6,1.8,0],[-2.8,1.8,0],color=ORANGE,stroke_width=5),Line([-6.6,2.5,0],[-2.8,2.5,0],color=ORANGE,stroke_width=5))
    mem=Rectangle(width=10.8,height=.25,color=GREY,fill_opacity=.4).move_to([0,-1.7,0])
    cell=Rectangle(width=10.8,height=1.4,color=GREY,fill_opacity=.06).move_to([0,-2.5,0])
    return VGroup(term,axon,mem,cell)
def vesicle():
    return Circle(.7,color=ORANGE,fill_opacity=.1).move_to([-2.8,1.8,0])

def receptor_stage(right=False):
    band=Rectangle(width=12,height=.3,color=GREY,fill_opacity=.4)
    ch=channel().scale(1.8).move_to([-3,0,0]); gp=gpcr().scale(1.8).move_to([3,0,0])
    if right:
        ch[0].shift(LEFT*.2);ch[1].shift(RIGHT*.2)
    g=VGroup(band,ch,gp.set_opacity(1 if right else .2),T('outside',26,GREY).move_to([-5.5,1,0]),T('inside',26,GREY).move_to([-5.5,-1,0]),T('ionotropic',34,BLUE).move_to([-3,2.9,0]),T('milliseconds',32).move_to([-3,-3.15,0]))
    return g

def ideas(n=1):
    g=VGroup(heading('The idea',GOLD),T('Classify by the main step a drug changes.',36,BLUE).move_to([0,2.45,0]))
    cs=VGroup(*[chip(t,c,size=32) for t,c in [('release',ORANGE),('reading',BLUE),('removal',TEAL)]]).arrange(RIGHT,buff=.6).move_to([0,1.4,0])
    # Text baselines, rather than variable glyph bounds, determine the row.
    for c in cs:
        c[0].stretch_to_fit_height(.68)
        c[1].move_to(c[0].get_center())
    g.add(cs)
    if n>=2:g.add(VGroup(T('How much depends on how much',36,PURPLE),T('of its target it fills.',36,PURPLE)).arrange(DOWN,buff=.22).move_to([0,-.55,0]))
    if n>=3:g.add(VGroup(T('What it does to a disease',36,GOLD),T('is a separate question.',36,GOLD)).arrange(DOWN,buff=.22).move_to([0,-2.8,0]))
    return g

class S00Title(TitleCard):
    LESSON='Transmitter Systems and Drugs'
    TITLE='Three Steps, One Drug'
class S01(SpokenScene):
    def construct(self):
        stage=synapse(False,True,True);ds=drugset()
        self.add(stage);self.at('Four drugs');self.play(FadeIn(ds),run_time=.5)
        self.at('opposite effects');self.play(GrowArrow(arr([-1.2,.1,0],[-1.2,.95,0],GREEN)),GrowArrow(arr([2.3,.95,0],[2.3,.1,0],RED)),run_time=.4)
        self.at('What decides');self.play(FadeIn(T('Which way does each push?',40,GOLD).move_to([0,-3.25,0])),run_time=.3);self.wait(2);self.finish()
class S02(SpokenScene):
    def construct(self):
        h=heart(-3);self.add(h);self.at('reported');self.play(FadeIn(heading('1921 • Otto Loewi')),run_time=.3)
        pulse(self,h[1],True);pulse(self,h[1],True)
        self.at('by stimulating')
        stimulus=VGroup(T('stimulate vagus',32,GOLD).move_to([1.6,2.3,0]),arr([-.1,2.3,0],[-3.65,2.1,0],GOLD))
        self.play(FadeIn(stimulus),Indicate(h[2],color=GOLD,scale_factor=1.05),run_time=.3)
        self.play(FadeIn(T('beat slows',36,YELLOW).move_to([1.6,.5,0])),run_time=.2)
        pulse(self,h[1]);self.wait(.4);pulse(self,h[1]);self.finish()
class S03(SpokenScene):
    def construct(self):
        hs=hearts();self.add(hs[0]);self.at('He moved');self.play(FadeIn(hs[1]),Create(transfer()),run_time=.4)
        drops=VGroup(*[dot([-1.3,1.3,0],r=.16) for _ in range(3)])
        self.play(LaggedStart(*[MoveAlongPath(d,transfer()) for d in drops],lag_ratio=.2),hs[1][0].animate.set_fill(YELLOW,.25),Succession(*[Indicate(hs[1][1],scale_factor=1.13,run_time=.35) for _ in range(3)]),Indicate(hs[0][1],scale_factor=1.13),run_time=1.1);self.remove(*drops)
        self.at('that heart slowed');self.play(FadeIn(T('slower',30,YELLOW).move_to([3,-1.7,0])),run_time=.2)
        for _ in range(2):self.play(Indicate(hs[0][1],scale_factor=1.13),Indicate(hs[1][1],scale_factor=1.13),run_time=.65)
        self.finish()
class S04(SpokenScene):
    def construct(self):
        hs=hearts();hs[1][0].set_fill(YELLOW,.25);self.add(hs,transfer(),T('slower',30,YELLOW).move_to([3,-1.7,0]))
        self.at('Its own nerve');self.play(hs[1][2].animate.set_color(GOLD).set_stroke(width=10),FadeIn(T('not stimulated',28,GOLD).move_to([3.8,2.65,0])),run_time=.25)
        self.at('The first nerve');self.play(FadeIn(chip('The message is a chemical',YELLOW,size=36).move_to([0,-2.8,0])),run_time=.25);self.finish()
class S05(SpokenScene):
    def construct(self):
        self.add(heading('A chemical message',YELLOW))
        glass=VGroup(Polygon([-1,1.3,0],[1,1.3,0],[0,0,0],color=TEAL),Polygon([0,0,0],[-1,-1.3,0],[1,-1.3,0],color=TEAL),Polygon([-.65,-1.1,0],[.65,-1.1,0],[0,-.5,0],color=YELLOW,fill_opacity=.8),Line([-1.1,1.4,0],[1.1,1.4,0],color=TEAL),Line([-1.1,-1.4,0],[1.1,-1.4,0],color=TEAL)).move_to([4,0,0])
        for cue,obj,txt,x in [('imitate it',key(PURPLE).scale(1.5).move_to([-4,0,0]),'imitate',-4),('block it',xmark([0,0,0],1),'block',0),('make it last',glass,'make it last',4)]:
            self.at(cue);self.play(FadeIn(VGroup(obj,T(txt,32).move_to([x,-2.4,0]))),run_time=.25)
        self.finish()
class S06(SpokenScene):
    def construct(self):
        self.add(focus_base());v=vesicle();d=dot([-2.8,1.8,0],r=.33)
        self.at('Follow one molecule');self.play(FadeIn(v),FadeIn(d),FadeIn(T('one molecule',30,YELLOW).move_to([.1,1.75,0])),run_time=.4)
        self.play(v.animate.shift(DOWN*.3),d.animate.shift(DOWN*.3),run_time=.8)
        self.at('Three things');self.play(FadeIn(heading('Three steps',GOLD)),run_time=.3);self.finish()
class S07(SpokenScene):
    def construct(self):
        base=focus_base();v=vesicle().shift(DOWN*.3);d=dot([-2.8,1.5,0],r=.33);self.add(base,v,d)
        self.at('First');self.play(FadeIn(heading('1 Released • source',ORANGE)),run_time=.25)
        self.at('released from');self.play(v.animate.move_to([-2.8,1.35,0]),d.animate.move_to([-2.8,1.35,0]),run_time=.3)
        self.at('a spike arrives');blip=VGroup(Line([-6.6,2.15,0],[-5.9,2.15,0],color=GOLD,stroke_width=16),dot([-5.9,2.15,0],GOLD,.25));self.add(blip);self.play(blip.animate.shift(RIGHT*3.1),run_time=.55)
        opening=Arc(radius=.7,start_angle=0,angle=PI,color=ORANGE).move_to([-2.8,.95,0])
        gap=Line([-3.5,.65,0],[-2.1,.65,0],color=BG,stroke_width=8)
        self.play(ReplacementTransform(v,opening),FadeIn(gap),FadeOut(blip),run_time=.2);self.wait(.25);self.play(d.animate.move_to([-2.8,-.15,0]),run_time=.4);self.finish()
class S08(SpokenScene):
    def construct(self):
        d=dot([-2.8,-.15,0],r=.33);ch=channel(-2.8,-1.65);self.add(focus_base(),d)
        self.at('Second');self.play(FadeIn(ch),FadeIn(heading('2 Read • readers',BLUE)),run_time=.3)
        self.at('read by a receptor');self.play(d.animate.move_to([-2.8,-1,0]),run_time=.5);self.finish()
class S09(SpokenScene):
    def construct(self):
        g=receptor_stage();self.add(g[0],g[2],g[3],g[4]);self.at('Some receptors');self.play(FadeIn(g[1]),run_time=.2)
        self.at('ion channels');self.play(FadeIn(g[5]),run_time=.2)
        tx=dot([-3,1.8,0],r=.25);self.add(tx);self.play(tx.animate.move_to([-3,1.1,0]),run_time=.25)
        self.at('that open');self.play(g[1][0].animate.shift(LEFT*.2),g[1][1].animate.shift(RIGHT*.2),run_time=.25)
        ions=VGroup(*[dot([-3,y,0],TEXT,.12) for y in [.7,.3,-.1]])
        label=T('ions',28,TEXT).move_to([-1.75,-1.5,0]);self.add(ions);self.play(ions.animate.shift(DOWN*1.5),FadeIn(label),FadeIn(g[6]),run_time=.5);self.finish()
class S10(SpokenScene):
    def construct(self):
        g=receptor_stage(True);self.add(g[0],g[1],*g[3:]);self.at('Others are');self.play(FadeIn(g[2]),FadeIn(T('metabotropic • GPCR',32,BLUE).move_to([3,2.9,0])),run_time=.4)
        tx=dot([3,1.8,0],r=.25);self.add(tx);self.play(tx.animate.move_to([3,1.05,0]),run_time=.3)
        self.at('through messengers');protein=chip('G protein',BLUE,size=28).move_to([3,-1.6,0]);self.play(FadeIn(protein),GrowArrow(arr([3,-.9,0],[3,-1.2,0],BLUE)),run_time=.3)
        ds=VGroup(*[dot([x,-2.4,0],GREEN,.14) for x in [2.3,3,3.7]])
        self.play(LaggedStart(*[FadeIn(d) for d in ds],lag_ratio=.3),run_time=.6)
        self.at('over tens');self.play(FadeIn(T('tens of milliseconds\nto minutes',32).move_to([3,-3.2,0])),run_time=.3);self.finish()
class S11(SpokenScene):
    def construct(self):
        self.add(synapse());d=dot([-2,.2,0]);d2=dot([3,.1,0]);self.add(d,d2)
        self.at('Third');self.play(FadeIn(heading('3 Removed • off switch',TEAL)),run_time=.25)
        enzyme=VGroup(Arc(radius=.5,start_angle=PI/4,angle=1.5*PI,color=TEAL,stroke_width=9).move_to([-2,.2,0]),T('enzyme',28,TEAL).move_to([-2,-.75,0]))
        self.at('an enzyme');self.play(FadeIn(enzyme),run_time=.2)
        self.play(ReplacementTransform(d,VGroup(dot([-2.2,.4,0],GREY,.13),dot([-1.8,-.1,0],GREY,.13))),run_time=.3)
        self.at('a transporter');self.play(FadeIn(T('transporter',28,TEAL).move_to([4.1,2.95,0])),d2.animate.move_to([4,1.3,0]),run_time=.4)
        self.at('pulls it back');self.play(d2.animate.move_to([4,2.1,0]),GrowArrow(arr([4.65,.65,0],[4.65,2.1,0],TEAL)),run_time=.6);self.finish()
class S12(SpokenScene):
    def construct(self):
        self.add(heading('Three slots for every transmitter',GOLD))
        for cue,txt,col,x,example in [('Source','source',ORANGE,-4.3,'spike'),('readers','readers',BLUE,0,'receptor'),('off switch','off switch',TEAL,4.3,'transporter\nor enzyme')]:
            self.at(cue);self.play(FadeIn(chip(txt,col,size=44).move_to([x,.8,0])),FadeIn(T(example,32,col).move_to([x,-1.1,0])),run_time=.2)
        self.finish()
class S13(SpokenScene):
    def construct(self):
        a=analogy(True);self.add(heading('A key, a lock, a cleaner',GOLD))
        self.at('a key');self.play(FadeIn(a[0]),FadeIn(a[3]),run_time=.2)
        self.at('a lock');self.play(FadeIn(a[1]),FadeIn(a[4]),run_time=.2)
        self.at('a cleaner');self.play(FadeIn(a[2]),FadeIn(a[5]),FadeIn(a[6]),run_time=.2)
        self.at('sweeps keys away');k=key().scale(.6).move_to([4.5,-.9,0]);self.add(k);self.play(Rotate(a[2],.3,about_point=[4,2,0]),k.animate.shift(RIGHT*1.4),run_time=.5);self.play(k.animate.shift(RIGHT*1.2).set_opacity(0),run_time=.35);self.finish()
class S14(SpokenScene):
    def construct(self):
        a=analogy();self.add(a);k=key(PURPLE).scale(.65).move_to([-3,1.2,0]);self.at('A copy');self.play(FadeIn(k),run_time=.2)
        self.at('turns the lock');self.play(k.animate.shift(np.array([.9,0,0])-k[1].get_end()),run_time=.4);self.play(Rotate(k,PI/3,about_point=[.9,0,0]),a[1][0].animate.set_fill(GREEN,.5),run_time=.5)
        self.at('an agonist');self.play(FadeIn(heading('Agonist',PURPLE)),run_time=.2);self.finish()
class S15(SpokenScene):
    def construct(self):
        a=analogy();self.add(a);k=key(PURPLE).scale(.65).move_to([-3,1.4,0]).set_z_index(3);self.at('A key that fits');self.play(FadeIn(k),run_time=.2);self.play(k.animate.shift(np.array([.9,0,0])-k[1].get_end()),run_time=.35)
        self.at('will not turn');self.play(FadeIn(T('no turn',30,RED).move_to([.5,-2.3,0])),run_time=.15)
        stop=k[0].get_left()-np.array([.1,0,0]);self.play(a[0].animate.shift(stop-a[0][1].get_end()),run_time=.35);self.play(a[0].animate.shift(LEFT*.55),Indicate(k,color=RED,scale_factor=1),run_time=.25)
        self.at('competitive antagonist');self.play(FadeIn(heading('Competitive antagonist',PURPLE)),run_time=.2);self.finish()
class S16(SpokenScene):
    def construct(self):
        a=analogy();a[0].scale(.65/1.5);a[0].shift(np.array([.9,0,0])-a[0][1].get_end());a[0].rotate(PI/12,about_point=[.9,0,0]);self.add(a)
        stiff=T('stiff',28,GREY).move_to([.5,-2.3,0]);self.add(stiff)
        self.at('Oil in');oil=dot([2.5,2.3,0],PURPLE,.25);site=Circle(.16,color=PURPLE).move_to([1.75,.4,0]);self.add(oil,site,T('other site',28,PURPLE).move_to([2.9,1.2,0]),Line([2.05,1.0,0],[1.9,.4,0],color=PURPLE))
        self.wait(1);self.play(oil.animate.move_to([1.75,.4,0]),run_time=.4)
        self.at('turns more easily');self.play(FadeOut(stiff),Rotate(a[0],PI/4,about_point=[.9,0,0]),a[1][0].animate.set_fill(GREEN,.55),run_time=.5)
        self.at('positive allosteric');self.play(FadeIn(heading('Positive allosteric modulator',PURPLE)),run_time=.25);self.finish()
class S17(SpokenScene):
    def construct(self):
        a=analogy();a[0].scale(.65/1.5);self.add(a);self.at('Stopping the cleaner');self.play(Create(xmark([4,0,0],.7)),run_time=.25)
        ks=VGroup(*[key().scale(.65).move_to([x,-1.9,0]) for x in [2.4,3.9,5.4]])
        self.play(FadeIn(ks),run_time=.2)
        self.at('reuptake blocker');self.play(FadeIn(heading('Reuptake blocker or enzyme inhibitor',PURPLE)),run_time=.25)
        for k in [a[0],ks[0],ks[1]]:
            self.play(k.animate.shift(np.array([.9,0,0])-k[1].get_end()),run_time=.3);self.play(Rotate(k,PI/3,about_point=[.9,0,0]),a[1][0].animate.set_fill(GREEN,.5),run_time=.25)
            self.play(FadeOut(k),run_time=.1)
        self.finish()
class S18(SpokenScene):
    def construct(self):
        base=synapse(True,True);self.add(base)
        self.at('fast inhibitory transmitter');note=T('Fast inhibition',32,YELLOW).move_to([0,.1,0]);self.play(FadeIn(note),run_time=.3)
        self.at('four drugs');self.play(FadeOut(note),run_time=.2)
        for label,target in [(base[7],base[0]),(base[8],VGroup(base[3],base[4])),(base[9],base[5])]:
            self.play(label.animate.set_color(GOLD),Indicate(target,color=GOLD,scale_factor=1.02),run_time=.45)
            self.play(label.animate.set_color([ORANGE,BLUE,TEAL][[base[7],base[8],base[9]].index(label)]),run_time=.15)
        self.finish()
class S19(SpokenScene):
    def construct(self):
        base=synapse(False,True);self.add(base)
        self.at('activates');self.play(FadeIn(drug(0)),base[4].animate.set_fill(GREEN,.5),run_time=.4)
        self.at('sits in');self.play(FadeIn(drug(1)),run_time=.4)
        self.at('without opening');self.play(FadeIn(T('closed',26,RED).move_to([-2.8,.25,0])),run_time=.2);self.finish()
class S20(SpokenScene):
    def construct(self):
        base=synapse(False,True);self.add(base)
        self.at('binds a different site');base[6].set_opacity(1);self.play(FadeIn(drug(2)),Indicate(base[6],color=PURPLE),run_time=.4)
        self.at('strengthens');self.play(Indicate(base[3],color=GREEN),run_time=.35)
        self.at('blocks');self.play(FadeIn(drug(3)),Create(xmark([4,1.3,0],.22)),run_time=.4);self.finish()
class S21(SpokenScene):
    def construct(self):
        q=quiz();self.add(q[0],q[1]);self.at('mature synapse');self.play(FadeIn(q[2]),run_time=.25)
        self.at('Which drugs');self.play(FadeIn(VGroup(*q[3:])),run_time=.3);self.finish()
class S22Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;q=quiz();self.add(*q[:-1]);ring=q[-1];self.add(ring)
        self.play(Uncreate(ring),rate_func=linear,run_time=5)
class S23(SpokenScene):
    def construct(self):
        ds=drugset();base=synapse(False,True,True);self.add(base,ds,T('Model: receiving cell, mature synapse',26).move_to([0,-3.25,0]))
        self.at('make it stronger');self.play(*[ds[i][1].animate.set_color(GREEN) for i in [0,2,3]],*[GrowArrow(drug_arrow(i)) for i in [0,2,3]],run_time=.3)
        self.at('weakens it');self.play(ds[1][1].animate.set_color(RED),GrowArrow(drug_arrow(1,False)),run_time=.3)
        self.at('causes seizures');note=heading('Bicuculline: seizures in animals',RED);self.play(FadeIn(note),run_time=.25)
        self.at('On terminals');self.play(FadeOut(note),FadeIn(heading('Baclofen can also reduce release',ORANGE)),run_time=.2)
        pre=gpcr(-.8,1.3);tag=T('GABA-B',26,BLUE).move_to([-.8,2.2,0]);release=T('release down',28,ORANGE).move_to([1.8,.2,0])
        self.play(FadeIn(pre),FadeIn(tag),FadeIn(release),GrowArrow(arr([-.8,.78,0],[-.8,-.2,0],ORANGE)),run_time=.3)
        self.at('cut GABA release');self.play(Indicate(pre,color=ORANGE,scale_factor=1.05),run_time=.3)
        self.at('so circuits');self.play(FadeIn(T('Circuits can differ',30,GOLD).move_to([0,2.95,0])),run_time=.2);self.wait(2);self.finish()
class S24(SpokenScene):
    def construct(self):
        ds=drugset();self.add(synapse(False,True,True),ds)
        self.at('Same transmitter');self.play(FadeIn(heading('Same transmitter • opposite effects',YELLOW)),run_time=.3)
        self.at('which step');self.play(*[FadeOut(m) for m in self.mobjects if m is not ds],run_time=.25)
        labels=VGroup(*[T(t,34,c).move_to([x,2.3,0]) for t,c,x in [('Release',ORANGE,-4.3),('Reading',BLUE,0),('Removal',TEAL,4.3)]])
        targets=[(0,.8,0),(0,-.4,0),(0,-1.6,0),(4.3,.8,0)]
        # Clear target leaders when changing from anatomy to a table.
        self.play(FadeIn(labels),FadeIn(T('none of these four',26,GREY).move_to([-4.3,.8,0])),*[FadeOut(d[0]) for d in ds],*[d[1].animate.move_to(p) for d,p in zip(ds,targets)],run_time=.5)
        self.at('which direction');self.play(*[GrowArrow(arr([x+1.45,y-.3,0],[x+1.45,y+.3,0],GREEN)) for x,y,_ in [targets[0],targets[2],targets[3]]],GrowArrow(arr([1.45,-.1,0],[1.45,-.7,0],RED)),FadeIn(T('Arrows show the effect on inhibition',28,GREY).move_to([0,-3,0])),run_time=.3);self.finish()
class S25(SpokenScene):
    def construct(self):
        g=ideas();self.add(g[0]);self.at('classify a drug');self.play(FadeIn(g[1]),run_time=.3)
        for cue,c in zip(['Release','reading','or removal'],g[2]):
            self.at(cue);self.play(FadeIn(c),c[0].animate.set_fill(c[0].get_color(),.55),run_time=.2);self.play(c[0].animate.set_fill(c[0].get_color(),.16),run_time=.3)
        self.finish()
class S26(SpokenScene):
    def construct(self):
        self.add(ideas());self.at('depends on');self.play(FadeIn(ideas(2)[3]),run_time=.3);self.finish()
class S27(SpokenScene):
    def construct(self):
        self.add(ideas(2));self.at('a separate question');self.play(FadeIn(ideas(3)[4]),run_time=.3);self.finish()
class S28(SpokenScene):
    def construct(self):
        g=ideas(3);self.add(g);self.at('The takeaway');self.play(FadeOut(g),FadeIn(heading('Next: how much?',TEAL)),run_time=.25)
        self.at('find the step');self.play(FadeIn(T('Find the step,',44,GOLD).move_to([0,1.1,0])),run_time=.25)
        self.at('the direction');self.play(FadeIn(T('and the direction.',44,GOLD).move_to([0,-.1,0])),FadeIn(T('Then ask how much of the target is filled.',30,TEAL).move_to([0,-2.5,0])),run_time=.25);self.finish()
class S29End(EndCard):
    LINE='Find the step a drug changes, and the direction it pushes.'
