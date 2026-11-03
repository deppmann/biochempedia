"""Comm: The Gate Is in the Axon — reviewed animation.
COLOR MAP: BLUE axons; RED Slit/blocked; YELLOW Robo; PURPLE Comm;
GREEN fluorescent GFP tag only; GREY organelles; GOLD emphasis.
Paths are anatomical schematics, not quantitative data or model traces.
"""
from bp_style import *
from bp_style import SpokenScene as BaseSpokenScene
import numpy as np

PURPLE = '#B58CD9'

class SpokenScene(BaseSpokenScene):
    # Log AFTER the wait: the shared logger's `now` is a pre-wait diagnostic.
    # Keep the verification log outside the deliverables permitted by TASK.md.
    def at(self, phrase, lead=0, nth=0):
        target = self.t_of(phrase, nth) - lead
        if target > self.elapsed():
            self.wait(np.ceil((target-self.elapsed())*config.frame_rate)/config.frame_rate)
        with open('/tmp/gate-in-the-axon-sync.jsonl','a') as f:
            f.write(json.dumps(dict(scene=os.environ['KX_SCENE_ID'],phrase=phrase,
                                   spoken_s=target,visual_s=self.elapsed(),
                                   error_s=self.elapsed()-target))+'\n')


def label(s,x=0,y=3.15,color=TEXT,size=32):
    return T(s,size=size,color=color).move_to([x,y,0])


def cross(m):
    x,y,_=m.get_center(); w=m.width/2+.1; h=m.height/2+.1
    return VGroup(Line([x-w,y-h,0],[x+w,y+h,0],color=RED,stroke_width=5),
                  Line([x-w,y+h,0],[x+w,y-h,0],color=RED,stroke_width=5))


def ladder(kind,cx=0,cy=0,h=4.8,w=1.8):
    g=VGroup()
    if kind=='slit':
        w=.5
    for dx in (-w/2,w/2):
        g.add(Line([cx+dx,cy-h/2,0],[cx+dx,cy+h/2,0],color=BLUE,stroke_width=7))
    fs=(.18,.36,.56,.76) if kind=='normal' else (.12,.25,.4,.55,.7,.85) if kind=='robo' else (.16,.33,.5,.67,.84) if kind=='slit' else ()
    for f in fs:
        y=cy-h/2+f*h
        g.add(Line([cx-w/2,y,0],[cx+w/2,y,0],color=BLUE,stroke_width=6))
        if kind=='robo':
            g.add(Line([cx+w/2,y,0],[cx-w/2,y+.5,0],color=BLUE,stroke_width=4))
    return g


def cone(x=-2.8,y=0,s=3.7,n=5,opacity=1,facing=1):
    body=Ellipse(width=.62*s,height=.7*s,color=BLUE,fill_color=BLUE,fill_opacity=.32,stroke_width=4)
    fil=VGroup(*[Line([.24*s,np.sin(a)*.3*s,0],[.57*s,np.sin(a)*.6*s,0],color=BLUE,stroke_width=4) for a in (-1,-.4,.4,1)])
    rb=VGroup(*[RoundedRectangle(width=.13*s,height=.11*s,corner_radius=.06,stroke_width=1,stroke_color=YELLOW,fill_color=YELLOW,fill_opacity=opacity).move_to([.28*s,(i-(n-1)/2)*.14*s,0]) for i in range(n)])
    g=VGroup(body,fil,rb)
    if facing==-1: g.flip(UP)
    g.shift([x,y,0]); g.body=body; g.rb=rb
    return g


def midline(x=0,h=5.6):
    bar=RoundedRectangle(width=.65,height=h,corner_radius=.16,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([x,0,0])
    dots=VGroup(*[Dot([x+dx,y,0],radius=.13,color=RED) for dx in (-.48,.48) for y in (-2,-1,1,2)])
    return VGroup(bar,dots,label('Slit',x,3.15,RED),label('midline',x,-3.15,GREY,30))


def stage(x=-3,n=5,opacity=1,post=False,s=3.7):
    c=cone(x,s=s,n=n,opacity=opacity,facing=-1 if post else 1)
    # Solid axon behind the cone, never drawn through a receptor chip.
    a=always_redraw(lambda: Line([-6.2,0,0],c.body.get_center(),color=BLUE,stroke_width=9))
    return midline(),c,a


def post_stage(n=2):
    # Shared enlarged, centered stage for the continuous s19–s21 sequence.
    c=cone(1.6,s=4.7,n=n,facing=-1)
    m=midline(-2.2)
    a=always_redraw(lambda: Line([-5.8,0,0],c.body.get_center(),color=BLUE,stroke_width=9))
    return m,c,a


def q1():
    g=VGroup(label('Which phenotype?',size=38))
    for x,k,name in [(-4.3,'robo','robo'),(0,'comm','comm')]:
        g.add(ladder(k,x,h=4.6),label(name,x,-3,size=32))
    g.add(RoundedRectangle(width=2.8,height=4.6,corner_radius=.2,color=GREY).move_to([4.3,0,0]),label('?',4.3,0,size=78),label('robo; comm',4.3,-3,size=32))
    return g


def neurons():
    g=VGroup()
    for y in (-1.65,0,1.65):
        cell=Circle(radius=.5,color=BLUE,fill_color=BLUE,fill_opacity=.15).move_to([-5.1,y,0])
        ax=Arrow([-4.6,y,0],[-.9,y,0],color=BLUE,stroke_width=5,buff=0,max_tip_length_to_length_ratio=.07)
        g.add(VGroup(cell,ax))
    return g


def q2():
    ns=neurons()
    comms=VGroup(*[Dot(c[0].get_center(),radius=.28,color=PURPLE) for c in ns])
    ml=VGroup(Line([-.65,-2.3,0],[-.65,2.3,0],color=GREY,stroke_width=10),label('midline',-.65,-2.7,GREY,30))
    box=RoundedRectangle(width=3.4,height=4.5,corner_radius=.2,color=GREY).move_to([3.5,0,0])
    return VGroup(label('Comm in every neuron',-2.8,3.15,PURPLE,32),ns,comms,label('modest level',-3.1,-2.7,PURPLE,34),box,label('?',3.5,0,size=80),label('Predict the ladder',3.5,-3.15,size=30),ml)


def circuit(y=.8):
    cm=chip('Comm',PURPLE,38).move_to([-3.5,y,0])
    r=chip('Robo1',YELLOW,38).move_to([3,y,0])
    line=Line([-2.1,y,0],[1.5,y,0],color=PURPLE,stroke_width=6)
    bar=Line([1.5,y-.4,0],[1.5,y+.4,0],color=PURPLE,stroke_width=6)
    return VGroup(cm,line,bar,r)


def sorting():
    # Fixed cell geometry across s16–s19, with space below for the short timeline.
    cell=Ellipse(width=12,height=5.35,color=BLUE,fill_color=BLUE,fill_opacity=.07).move_to([0,.15,0])
    gol=VGroup(*[RoundedRectangle(width=1.35-.15*i,height=.18,corner_radius=.06,color=GREY,fill_color=GREY,fill_opacity=.4).move_to([-4.25,.35+i*.3,0]) for i in range(3)])
    end=Circle(radius=.65,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([-.7,-.9,0])
    ly=Circle(radius=.75,color=GREY,fill_color=GREY,fill_opacity=.4).move_to([3,-.9,0])
    labs=VGroup(label('Golgi',-4.25,1.55,GREY,30),label('late endosome',-.7,-1.95,GREY,30),label('lysosome',3,.08,GREY,30),label('surface',4.1,1.55,BLUE,30))
    return VGroup(cell,gol,end,ly,labs)


def cargo(x=-3.3,y=.5):
    r=chip('Robo',YELLOW,30,pad=.15).move_to([x,y,0])
    r[0].set_fill(BG,opacity=1)
    return r


def surface_route():
    return VGroup(DashedLine([-3.25,.5,0],[5.3,.5,0],color=GREY,stroke_width=3),
                  Arrow([4.8,.5,0],[5.3,.5,0],buff=0,color=GREY),label('route to surface',1.7,1.05,GREY,30))


def unknown():
    box=RoundedRectangle(width=11.5,height=4.4,corner_radius=.3,color=PURPLE,fill_color=PURPLE,fill_opacity=.07).move_to([0,.1,0])
    cir=circuit(y=-.3)
    # Unknown inhibitory activity, represented by a question on the link.
    q=label('?',-.3,.55,PURPLE,60)
    return VGroup(box,label('Second Comm activity',y=1.65,color=PURPLE,size=38),cir,q)


class S00Title(TitleCard):
    TITLE='Comm: The Gate Is in the Axon'
    LESSON='Crossing the Midline Once: Slit, Robo and Comm'
    def construct(self):
        brand=label('BIOCHEMISTRYPEDIA',y=2.95,color=TEAL,size=30)
        lesson=label('Crossing the Midline Once: Slit, Robo and Comm',y=1.9,size=28)
        title=T('Comm: The Gate\nIs in the Axon',size=52,font=TITLE_FONT,line_spacing=1.2).move_to([0,-.25,0])
        rule=Line([-1.3,-2.35,0],[1.3,-2.35,0],color=GOLD,stroke_width=4)
        self.play(FadeIn(brand),FadeIn(lesson),run_time=.3)
        self.play(FadeIn(title),GrowFromCenter(rule),run_time=.6)
        self.finish()

class S01Question(SpokenScene):
    def construct(self):
        l=ladder('comm',0,h=4.8,w=3.6); self.add(l,label('comm mutant',0,-3.15,size=34))
        self.at('slit is still'); m=midline(); self.play(FadeIn(m[:3]),run_time=.45)
        self.at('robo is still made')
        marks=VGroup(*[chip('Robo',YELLOW,32).move_to([x,y,0]) for x,y in [(-4,.8),(4,-.8)]])
        caps=VGroup(*[Rectangle(width=.24,height=.7,color=YELLOW,fill_color=YELLOW,fill_opacity=1).move_to([x,y,0]) for x,y in [(-1.8,.8),(1.8,-.8)]])
        leaders=VGroup(Line([-3,.8,0],[-2,.8,0],color=YELLOW),Line([3,-.8,0],[2,-.8,0],color=YELLOW))
        self.play(FadeIn(marks),FadeIn(caps),Create(leaders),run_time=.5)
        self.at('Yet almost no axon crosses'); self.play(Indicate(l,color=BLUE),run_time=.6)
        self.at('Why'); self.play(FadeIn(label('Why?',3.9,1.55,GOLD,54)),run_time=.3); self.finish()

class S02Rule(SpokenScene):
    def construct(self):
        m,c,a=stage(s=4.5); self.add(a,m,c,label('Before crossing',-3.4,3.15,size=34))
        meter=VGroup(Rectangle(width=3.5,height=.35,color=GREY).move_to([3.6,-.1,0]),Rectangle(width=3.2,height=.23,stroke_width=0,fill_color=RED,fill_opacity=1).move_to([3.5,-.1,0]),label('Slit repulsion',3.6,.8,RED,32),label('low',2.2,-.75,size=30),label('high',5,-.75,size=30))
        self.at('too early'); self.play(FadeIn(meter),FadeIn(label('too early?',-3,-2.7,size=36)),run_time=.5)
        self.at('keep Robo down')
        cm=chip('Comm',PURPLE,34).move_to([-3,2.2,0]); link=VGroup(Line([-2.2,1.6,0],[-1.9,.8,0],color=PURPLE,stroke_width=5),Line([-2.2,.72,0],[-1.6,.88,0],color=PURPLE,stroke_width=5))
        self.play(FadeIn(cm),Create(link),run_time=.55); self.finish()

class S03Test(SpokenScene):
    def construct(self):
        self.add(label('Test the gate with genetics',size=40))
        cards=VGroup()
        for x,num,txt in [(-3.1,'1','Remove both\nrobo and comm'),(3.1,'2','Add Comm to\nevery neuron')]:
            cards.add(VGroup(RoundedRectangle(width=5.4,height=3.7,corner_radius=.2,color=GREY).move_to([x,.2,0]),label(num,x,1.25,GOLD,48),label(txt,x,-.25,size=34)))
        self.at('How would you test'); self.play(FadeIn(cards),run_time=.7)
        self.at('In'); self.play(FadeIn(label('1998',y=-2.3,size=36)),run_time=.35)
        # Cue uses the stable year token before the mis-transcribed proper name.
        self.wait(max(0,4.46-self.elapsed()))
        self.play(FadeIn(label('Tear, Goodman & colleagues',y=-3.15,size=32)),run_time=.35)
        self.at('two experiments'); self.play(Indicate(cards,color=GOLD,scale_factor=1.02),run_time=.5); self.finish()

class S04Q1(SpokenScene):
    def construct(self):
        self.add(q1()); self.at('First'); self.play(Indicate(self.mobjects[0][7],color=GOLD),run_time=.5); self.finish()

class S05Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(q1()); self.wait(5)

class S06Rev1(SpokenScene):
    def construct(self):
        g=q1(); self.add(g); self.at('It looks like')
        self.play(FadeOut(g[5]),FadeOut(g[6]),FadeIn(ladder('robo',4.3,h=4.6)),run_time=.7)
        self.at('Follow it'); self.play(Circumscribe(VGroup(g[1],g[2]),color=GOLD),run_time=.7); self.finish()

class S07Step1(SpokenScene):
    def construct(self):
        m,c,a=stage(); self.add(a,m,c,label('1 · comm mutant',-3.2,3.15,size=34))
        self.at('robo is too high'); self.play(Indicate(c.rb,color=YELLOW),FadeIn(label('Robo high',-3,-2.5,YELLOW,34)),run_time=.6)
        self.at('Axons are repelled early'); self.play(c.animate.shift(LEFT*.65),GrowArrow(Arrow([-.6,1.9,0],[-2.5,1.9,0],buff=0,color=RED)),run_time=.8)
        self.at('do not cross'); self.play(FadeIn(label('No crossing',3.6,0,RED,40)),run_time=.35); self.finish()

class S08Step2(SpokenScene):
    def construct(self):
        m,c,a=stage(); self.add(a,m,c,label('2 · robo; comm',-3.2,3.15,size=34))
        r=chip('Robo1',YELLOW,34).move_to([3.4,1.4,0]); self.add(r)
        self.at('there is no'); self.play(Create(cross(r)),FadeOut(c.rb),run_time=.55)
        self.at('to be too high'); self.play(FadeIn(label('None to be\ntoo high',3.4,-.6,size=34)),run_time=.4); self.finish()

class S09Step3(SpokenScene):
    def construct(self):
        cir=circuit(1.65); self.add(cir,label('3 · Remove the switch',y=3.15,size=36))
        self.at('With'); absent=VGroup(cross(cir[3]),label('absent',3,.65,YELLOW,30))
        self.play(FadeIn(absent),run_time=.45)
        self.at('losing comm changes nothing')
        self.play(Create(cross(cir[0])),Transform(cir[1],DashedLine([-2.1,1.65,0],[1.5,1.65,0],color=GREY)),FadeOut(cir[2]),run_time=.5)
        cut=VGroup(Line([-.6,1.3,0],[-.2,2,0],color=RED,stroke_width=6),Line([-.15,1.3,0],[.25,2,0],color=RED,stroke_width=6)); self.add(cut)
        self.at('The embryo shows only')
        self.play(FadeIn(VGroup(ladder('robo',-3,-1,h=2.9),ladder('robo',3,-1,h=2.9),label('robo',-3,-3.15,size=32),label('robo; comm',3,-3.15,size=32),label('=',0,-1,size=60))),run_time=.65); self.finish()

class S10Epi(SpokenScene):
    def construct(self):
        cir=circuit(1.25); self.add(cir)
        self.at('This reasoning is called'); self.play(FadeIn(label('Epistasis',size=44)),run_time=.5)
        self.at('turns another down'); self.play(Indicate(cir[1:3],color=PURPLE),run_time=.6)
        self.at('the double looks like')
        tiles=VGroup(ladder('robo',-3,-1.1,h=2.3),label('robo; comm',-3,-2.65,size=30),ladder('robo',3,-1.1,h=2.3),label('robo',3,-2.65,size=30),label('=',0,-1.1,size=60))
        self.play(FadeIn(tiles),run_time=.5)
        rule=label("Double mutant looks like the downstream gene’s mutant",y=-3.35,size=30)
        self.at('the downstream gene')
        highlight=SurroundingRectangle(cir[3],color=GOLD,buff=.12,corner_radius=.15)
        self.play(Create(highlight),FadeIn(label('downstream',3,.3,YELLOW,30)),FadeIn(rule),run_time=.55); self.wait(3.2); self.finish()

class S11Q2(SpokenScene):
    def construct(self):
        g=q2(); self.add(g[1],g[7]); self.at('Second experiment'); self.play(FadeIn(g[4:7]),run_time=.5)
        self.at('every neuron'); self.play(FadeIn(g[0]),FadeIn(g[2]),run_time=.55)
        self.at('a modest level'); self.play(FadeIn(g[3]),run_time=.4); self.at('What happens'); self.play(Indicate(g[5],color=GOLD),run_time=.5); self.finish()

class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; g=q2(); self.add(g)
        for n in (5,4,3,2,1):
            p=label('Predict · '+str(n),3.5,-3.15,GOLD,30)
            if n==5: self.remove(g[6])
            self.add(p); self.wait(1); self.remove(p)

class S13Rev2(SpokenScene):
    def construct(self):
        g=q2(); self.add(g)
        marks=VGroup(*[RoundedRectangle(width=.3,height=.65,corner_radius=.08,color=YELLOW,fill_color=YELLOW,fill_opacity=1).move_to([-4.65,y,0]) for y in (-1.65,0,1.65)])
        self.add(marks); self.at('falls'); self.play(marks.animate.set_opacity(.12),run_time=.65)
        l=ladder('robo',3.5,h=4.5,w=2.4)
        self.at('looks like robo'); self.play(FadeOut(g[4:7]),FadeIn(l),run_time=.6)
        self.at('Ipsilateral axons cross')
        ip=VMobject(color=GOLD,stroke_width=8).set_points_as_corners([[2.3,-1.6,0],[2.3,-.9,0],[4.7,-.9,0]])
        self.play(Create(ip),FadeIn(label('cross',3.5,-3.15,GOLD,30)),run_time=.85)
        self.at('commissural axons')
        re=VMobject(color=GOLD,stroke_width=8).set_points_as_corners([[2.3,.2,0],[4.7,.2,0],[4.7,1.1,0],[2.3,1.1,0]])
        self.play(Create(re),FadeIn(label('recross',3.5,2.65,GOLD,30)),run_time=1.15); self.wait(1.3); self.finish()

class S14Deaf(SpokenScene):
    def construct(self):
        cs=VGroup(*[cone(-3.8,y,s=1.9,n=3) for y in (-1.65,0,1.65)])
        ml=midline(-.7); self.add(cs,ml,label('Comm everywhere',-3.5,3.15,PURPLE,32))
        self.at('turns slit hearing down'); self.play(*[c.rb.animate.set_opacity(.25) for c in cs],FadeIn(label('Weak hearing',-3.7,-3.15,YELLOW,30)),run_time=.65)
        self.at('Much stronger'); self.play(FadeIn(VGroup(ladder('slit',3.8,h=3.7),label('stronger Comm',3.8,2.6,PURPLE,30),label('slit-like collapse',3.8,-2.4,BLUE,30),label('reported',3.8,-3.15,GOLD,32))),run_time=.65); self.finish()

class S15Notcue(SpokenScene):
    def construct(self):
        cir=circuit(); self.add(cir)
        self.at('not a second cue'); self.play(FadeIn(label('Comm sets how much Robo, and when',size=36,color=PURPLE)),run_time=.5)
        self.at('how much robo'); self.play(FadeIn(label('How much Robo',2.5,-1.15,YELLOW,38)),run_time=.4)
        self.at('and when'); self.play(FadeIn(label('When',3,-2.5,YELLOW,38)),run_time=.4); self.wait(3.2); self.finish()

class S16Sort(SpokenScene):
    def construct(self):
        s=sorting(); self.add(s,cargo(-2.7,.5))
        self.at('How does it do that'); self.play(Indicate(s[1],color=YELLOW),run_time=.55)
        self.at('In'); year=label('2002',y=3.2,size=36); self.play(FadeIn(year),run_time=.35)
        self.wait(max(0,3.56-self.elapsed()))
        self.play(FadeIn(label('Keleman, Dickson & colleagues',y=-3.15,size=32)),run_time=.4)
        self.at('sorting model'); self.play(Transform(year,label('Sorting model · 2002',y=3.2,size=36)),run_time=.4); self.finish()

class S17Made(SpokenScene):
    def construct(self):
        self.add(sorting(),cargo(-2.7,.5))
        self.at('is made in commissural neurons'); self.play(FadeIn(chip('Comm',PURPLE,32).move_to([-2.2,1.6,0])),run_time=.45)
        self.at('for a short time')
        segments=VGroup(*[Rectangle(width=3.3,height=.44,color=GREY,stroke_width=2).move_to([x,-2.95,0]) for x in (-3.5,0,3.5)])
        labs=VGroup(*[label(txt,x,-3.5,size=28) for x,txt in [(-3.5,'before'),(0,'crossing'),(3.5,'after')]])
        self.play(FadeIn(segments),FadeIn(labs),FadeIn(label('Short time',y=3.15,color=PURPLE,size=36)),run_time=.4)
        self.at('before and during crossing')
        bar=Rectangle(width=6.8,height=.4,stroke_width=0,fill_color=PURPLE,fill_opacity=.65).move_to([-1.75,-2.95,0])
        self.play(FadeIn(bar),FadeIn(label('Comm made',-1.75,-2.95,TEXT,27)),run_time=.65); self.wait(3.2); self.finish()


class S18Divert(SpokenScene):
    def construct(self):
        s=sorting(); route=surface_route(); cm=chip('Comm',PURPLE,32).move_to([-2.2,1.65,0]); r=cargo(-2.9,.5)
        self.add(s,route,cm,label('Sorting newly made Robo',y=3.2,size=36))
        self.at('Inside the neuron'); self.play(FadeIn(r),run_time=.4)
        self.at('it meets newly made'); self.play(r.animate.move_to([-1.7,.5,0]),cm.animate.move_to([-1.7,1.25,0]),run_time=.9)
        self.at('It diverts it away')
        bend=VMobject(color=PURPLE,stroke_width=5).set_points_smoothly([[-1.7,.5,0],[-1.2,.1,0],[-.7,-.9,0]])
        self.play(Create(bend),r.animate.move_to([-.7,-.9,0]),run_time=1.2)
        self.at('late endosomes'); self.play(Indicate(s[2],color=YELLOW),run_time=.5)
        self.at('lysosomes'); self.play(r.animate.move_to([3,-.9,0]),GrowArrow(Arrow([.1,-.9,0],[2,-.9,0],color=PURPLE,buff=0)),run_time=.7); self.finish()

class S19Destroyed(SpokenScene):
    def construct(self):
        s=sorting(); r=cargo(3,-.9); self.add(s,r,surface_route())
        self.at('robo is destroyed')
        destroyed=VGroup(label('destroyed',3,-2.95,YELLOW,38),Line([3,-1.7,0],[3,-2.55,0],color=YELLOW))
        self.play(r.animate.scale(.2).set_opacity(0),FadeIn(destroyed),run_time=.65)
        self.remove(r)
        self.at('The growth cone crosses')
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not destroyed],
                  Transform(destroyed,label('Robo destroyed in lysosome',1.8,3.15,YELLOW,30)),run_time=.25)
        m,c,a=post_stage(); c.shift(LEFT*5.6); c.flip(UP,about_point=c.body.get_center()); self.add(a,m,c)
        self.play(c.animate.shift(RIGHT*5.6),run_time=1.15)
        self.remove(c); c=cone(1.6,s=4.7,n=2,facing=-1); self.add(c)
        self.at('little robo'); self.play(FadeIn(label('little Robo',1.6,-2.7,YELLOW,36)),run_time=.3); self.wait(3.2); self.finish()

class S20After(SpokenScene):
    def construct(self):
        m,c,a=post_stage(); cm=chip('Comm',PURPLE,34).move_to([4.5,1.8,0]); low=label('little Robo',1.6,-2.7,YELLOW,36); self.add(a,m,c,cm,low)
        self.at('Once the axon has crossed'); self.play(Indicate(c,color=BLUE,scale_factor=1.03),run_time=.45)
        self.at('stops making'); self.play(FadeOut(cm),FadeIn(label('Comm production stops',1.8,3.15,PURPLE,32)),run_time=.9)
        self.at('Robo reaches')
        r=cargo(-4,-.65); self.add(r)
        self.play(r.animate.move_to([.28,-.65,0]),run_time=.7)
        self.play(FadeOut(r),Transform(c,cone(1.6,s=4.7,n=5,facing=-1)),FadeOut(low),run_time=.4)
        self.wait(3.2); self.finish()

class S21Repel(SpokenScene):
    def construct(self):
        m,c,a=post_stage(n=5); self.add(a,m,c)
        self.at('Now the slit')
        d=Dot([-1.7,.15,0],color=RED,radius=.18); self.add(d)
        self.play(d.animate.move_to(c.rb[2].get_center()),run_time=.65)
        glow=SurroundingRectangle(c.rb,color=RED,buff=.15,corner_radius=.18,stroke_width=7)
        self.at('repels it'); self.play(FadeIn(glow),run_time=.2)
        self.play(FadeOut(d),FadeOut(glow),run_time=.2)
        path=VMobject(color=BLUE,stroke_width=8).set_points_smoothly([[1.6,0,0],[2.25,.25,0],[2.9,1.35,0]])
        self.play(c.animate.rotate(-2*PI/3).move_to([2.65,1.05,0]),Create(path),GrowArrow(Arrow([-.4,-1.7,0],[2.3,-1.7,0],color=RED,buff=0)),run_time=1)
        self.add(label('Turns away',2.3,-2.7,RED,36)); self.wait(3.2); self.finish()

class S22Real(SpokenScene):
    def construct(self):
        self.add(label('Sorting in living embryos',size=38))
        rows=VGroup()
        for y,txt in [(1.35,'without Comm'),(-1.55,'with Comm')]:
            soma=Circle(radius=.8,color=BLUE,fill_color=BLUE,fill_opacity=.12).move_to([-2.6,y,0])
            tip=cone(4.2,y,s=1.8,n=0)
            rows.add(VGroup(soma,Line([-1.8,y,0],[4.2,y,0],color=BLUE,stroke_width=8),tip,label(txt,-4.9,y,PURPLE,30)))
        self.add(rows,label('cell body',-2.6,-3.15,BLUE,30),label('axon tip',4.2,-3.15,BLUE,30))
        self.at('Sorting is real'); self.play(Indicate(rows,color=BLUE,scale_factor=1.01),run_time=.5)
        self.at('In Living Embryos'); evidence=label('Keleman et al., 2005',y=2.55,size=30); self.play(FadeIn(evidence),run_time=.4)
        signals=VGroup(*[VGroup(Dot([-2.6,y,0],radius=.46,color=GREEN,fill_opacity=.12),Dot([-2.6,y,0],radius=.3,color=GREEN,fill_opacity=.3),Dot([-2.6,y,0],radius=.17,color=GREEN)) for y in (1.35,-1.55)])
        self.at('stops a tagged robo'); self.play(*[FadeIn(signal) for signal in signals],Transform(evidence,label('Tagged Robo-GFP · Keleman et al., 2005',y=2.55,color=GREEN,size=30)),run_time=.5)
        self.at('from reaching the axon tip')
        self.play(signals[0].animate.move_to([4.2,1.35,0]),Indicate(signals[1],color=GREEN),run_time=1.05)
        self.add(label('reaches tip',1.7,.55,GREEN,30),label('stays in cell body',-.7,-2.5,GREEN,30),label('tip dark',4.2,-2.5,GREY,30)); self.wait(3.5); self.finish()

class S23Notall(SpokenScene):
    def construct(self):
        self.add(chip('Robo variant',YELLOW,38).move_to([-3.3,.5,0]),chip('Comm',PURPLE,34).move_to([-3.3,2,0]))
        self.at('not the whole story'); self.play(FadeIn(label('Sorting is not the whole story',size=36)),run_time=.45)
        self.at('cannot be sorted'); ar=Arrow([-3.3,-.2,0],[-3.3,-1.8,0],buff=0,color=GREY)
        self.play(GrowArrow(ar),run_time=.3); self.play(Create(cross(ar)),FadeIn(label('sorting blocked',-3.3,-2.65,size=30)),run_time=.35)
        self.at('develop normally'); self.play(FadeIn(ladder('normal',3,h=4.5)),FadeIn(label('variant Robo + Comm:\nnormal',3,-2.9,BLUE,30)),run_time=.65); self.finish()

class S24Still(SpokenScene):
    def construct(self):
        title=label('Sorting is not the whole story',size=36); self.add(title)
        left=VGroup(ladder('normal',-3.5,h=3.7),label('variant Robo + Comm:\nnormal',-3.5,-2.8,BLUE,30))
        right=VGroup(ladder('normal',3.5,h=3.7),label('variant Robo + Comm',3.5,-2.6,size=30))
        self.add(left,right)
        self.at('still need COM to cross'); self.play(Transform(right[0],ladder('comm',3.5,h=3.7)),Transform(right[1],label('variant Robo, no Comm',3.5,-2.6,size=30)),FadeIn(label('no rungs',3.5,-3.25,RED,32)),run_time=.6)
        self.at('at least one more way'); old=[m for m in self.mobjects if m is not title]; self.play(*[FadeOut(m) for m in old],FadeIn(unknown()),run_time=.6); self.finish()

class S25Debate(SpokenScene):
    def construct(self):
        self.add(unknown(),label('Sorting is not the whole story',size=36)); self.at('remains debated'); self.play(FadeIn(label('Still debated',y=-2.8,color=GOLD,size=44)),run_time=.5); self.wait(.8); self.finish()

class S26Take(SpokenScene):
    def construct(self):
        m=midline(1.3); c=cone(-2.8,s=4.8,n=2); a=Line([-6,0,0],c.body.get_center(),color=BLUE,stroke_width=9); self.add(a,m,c)
        self.at('For prediction'); self.play(FadeIn(label('The result to use',-3.2,3.15,size=34)),run_time=.45)
        self.at('While comm is present'); cm=chip('Comm present',PURPLE,32).move_to([4.4,1.8,0]); self.play(FadeIn(cm),run_time=.45)
        self.at('stays low'); self.play(FadeIn(label('Robo1 stays low',4.4,0,YELLOW,32)),run_time=.4)
        self.at('only weakly'); self.play(FadeIn(label('Slit hearing:\nweak',4.4,-1.8,YELLOW,34)),run_time=.4); self.finish()

class S27End(EndCard):
    LINE='While Comm is present, Robo1 stays low,\nso the axon hears Slit only weakly.'
    def construct(self):
        self.add(label('The rule to keep',y=2.5,color=GOLD,size=34))
        line=T(self.LINE,size=40,font=TITLE_FONT,line_spacing=1.35).move_to([0,.3,0])
        fit(line,max_w=12)
        self.play(FadeIn(line),run_time=.6)
        self.play(FadeIn(label('biochemistrypedia.com',y=-2,color=TEAL,size=30)),run_time=.3); self.wait(4.5); self.finish()
