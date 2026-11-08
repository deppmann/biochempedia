"""Mammals mute Robo, and also clear it.
COLOR MAP: BLUE axon/growth cone; RED Slit/blocked; YELLOW Robo1/2;
PURPLE Comm; ORANGE Robo3; GREY anatomy/compartments; GOLD title/sensory pathway;
GREEN netrin/DCC; TEAL Ndfip1/2. Paths are schematic anatomy, not data
traces or molecular structures. No quantitative model is implied.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
LESSON = 'Crossing the Midline Once: Slit, Robo and Comm'


def label(s, x=0, y=3.1, color=TEXT, size=30):
    return T(s, size=size, color=color).move_to([x,y,0]).add_background_rectangle(color=BG, opacity=1, buff=.07)


def route(points, color=BLUE, width=7):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [np.array([x,y,0]) for x,y in points])


def cone(x,y,s=1,color=BLUE):
    body=Circle(radius=.26*s,color=color,fill_color=color,fill_opacity=.65)
    fil=VGroup(*[Line(.26*s*np.array([np.cos(a),np.sin(a),0]),
                    .52*s*np.array([np.cos(a),np.sin(a),0]),color=color,stroke_width=3)
                for a in (-.8,-.3,.3,.8)])
    return VGroup(body,fil).move_to([x,y,0])


def wide_cone(x,y,w):
    body=Ellipse(width=w,height=2.25,color=BLUE,fill_color=BLUE,fill_opacity=.5).move_to([x,y,0])
    fil=VGroup(*[Line([x+w/2-.15,y+d,0],[x+w/2+.45,y+1.3*d,0],color=BLUE,stroke_width=3)
                for d in (-.65,-.2,.2,.65)])
    return VGroup(body,fil)


def cross(x,y,size=.18):
    return VGroup(Line([x-size,y-size,0],[x+size,y+size,0],color=RED,stroke_width=5),
                  Line([x-size,y+size,0],[x+size,y-size,0],color=RED,stroke_width=5))


def cord(slit=False):
    g=VGroup(Ellipse(width=11.7,height=5.5,color=GREY,fill_color=GREY,fill_opacity=.04).shift(DOWN*.15),
        RoundedRectangle(width=.85,height=4.65,corner_radius=.15,color=GREY,
                         fill_color=GREY,fill_opacity=.25).shift(DOWN*.15),
        label('floor plate',0,-3.15,GREY,26))
    if slit:
        g.add(VGroup(*[Dot([x,y,0],radius=.12,color=RED) for x in (-.9,.9) for y in (-1.5,-.7,.7,1.5)]),
              label('Slit',0,2.55,RED,28))
    return g


def leader(a,b,color=GREY):
    return Line([*a,0],[*b,0],color=color,stroke_width=2)


def deletion(names,y=2.2):
    xs=np.linspace(-3.9,3.9,len(names)) if len(names)>1 else [0]
    g=VGroup()
    for name,x in zip(names,xs):
        tag=chip(name,RED,28).move_to([x,y,0])
        tag[0].set_fill(BG,opacity=1)
        g.add(VGroup(tag,cross(x+1.02,y)))
    return g


def prediction():
    anatomy=cord()
    anatomy[2].move_to([1.35,-2.2,0])
    return VGroup(anatomy,route([(-5,.05),(-2.4,.05)]),cone(-2.4,.05,1.5),
        label('?',1.9,.05,size=62),label('What should the axons do?',y=-3.45,size=32))


def q1():
    return VGroup(prediction(),deletion(['Slit1','Slit2','Slit3']),
                  label('All three Slit genes removed',y=3.2,size=33))


def explant(x,crossed=False):
    tissue=Rectangle(width=1.25,height=2.0,color=GREY,fill_color=GREY,fill_opacity=.45).move_to([x-1.4,.0,0])
    g=VGroup(tissue)
    if crossed:
        g.add(Rectangle(width=.23,height=2.0,color=TEXT,fill_color=TEXT,fill_opacity=.7).move_to([x-.88,0,0]))
    return g


def growth(x,short=False,ghost=False):
    length=.48 if short else 2.05
    paths=VGroup()
    for i,y in enumerate((-.8,-.27,.27,.8)):
        pts=[(x-.77,y),(x-.47,y+.12*(-1)**i),(x-.77+length*.65,y+.22*(-1)**i),
             (x-.77+length,y+.35*(-1)**i)]
        r=route(pts,GREY if ghost else BLUE,3 if ghost else 5)
        paths.add(DashedVMobject(r,num_dashes=15) if ghost else r)
    return paths


def dish(x,crossed=False,cells=False):
    g=VGroup(RoundedRectangle(width=5.7,height=4.7,corner_radius=.3,color=GREY,
                  fill_color=GREY,fill_opacity=.05).move_to([x,-.1,0]),explant(x,crossed),
        label('explant with floor plate' if crossed else 'dorsal explant',x,3.15,size=27),
        label('postcrossing axons' if crossed else 'no floor plate · precrossing',x,2.55,BLUE,26))
    if cells:
        g.add(VGroup(*[Dot([x+1.98+dx,y,0],radius=.15,color=RED)
                    for dx,y in ((0,0),(.25,.27),(.25,-.27),(-.12,.3),(-.12,-.3))]),
              label('Slit2 cells',x+1.55,-1.7,RED,26))
    if crossed:
        g.add(label('floor plate',x-1,-1.8,GREY,26),leader((x-.88,-1.08),(x-1,-1.48)))
    return g


def dishes(cells=False):
    return VGroup(dish(-3.05,False,cells),dish(3.05,True,cells))


def q2():
    return VGroup(dishes(True),label('?',-2.6,.1,size=62),label('?',3.5,.1,size=62),
        label('Which axons should Slit affect?',y=-3.15,size=33))


def membrane(deep=False):
    return VGroup(Rectangle(width=11.5,height=3.0 if deep else 2.4,stroke_opacity=0,fill_color=BLUE,
                     fill_opacity=.07).move_to([0,-1.5 if deep else -1.2,0]),
        Line([-5.75,0,0],[5.75,0,0],color=BLUE,stroke_width=10),
        label('axon membrane',0,-1.5,BLUE,28))


def receptor(name,x,y=0):
    # A labelled cartoon receptor with a stem through the membrane.
    tag=chip(name,YELLOW,30).move_to([x,y+.65,0])
    tag[0].set_fill(BG,opacity=1)
    return VGroup(Line([x,y-.5,0],[x,y+.25,0],color=YELLOW,stroke_width=7),tag)


def cap(x,y=1.48,w=2.35):
    # Domed cover with a descending rim, rather than a flat bar.
    return VGroup(ArcBetweenPoints([x-w/2,y,0],[x+w/2,y,0],angle=-PI,color=ORANGE,stroke_width=13),
                  Line([x-w/2,y,0],[x-w/2,y-.35,0],color=ORANGE,stroke_width=10),
                  Line([x+w/2,y,0],[x+w/2,y-.35,0],color=ORANGE,stroke_width=10))


def covers():
    return VGroup(cap(-2.7),cap(2.7),label('Robo3: response muted',y=3.15,color=ORANGE,size=32))


def odd_receptor(x,y=0):
    return VGroup(Line([x,y-.5,0],[x,y+.4,0],color=ORANGE,stroke_width=8),
        RoundedRectangle(width=.8,height=1.25,corner_radius=.38,color=ORANGE,
                         fill_color=ORANGE,fill_opacity=.3).move_to([x,y+.9,0]))


def q3():
    anatomy=cord(True)
    anatomy[-1].move_to([1.65,2.05,0])
    return VGroup(anatomy,route([(-5.2,0),(-2.65,0)],width=10),cone(-2.65,0,2.2),
        label('Robo1 / Robo2\nstill made',-3.2,-1.35,YELLOW,27),
        label('Robo3 removed',-3.4,1.8,ORANGE,29),
        label('?',2.5,0,size=62),label('Predict: will the axon cross?',y=3.2,size=32))


def ladder(x,y=0,h=4.4,kind='comm'):
    g=VGroup(*[Line([x+d,y-h/2,0],[x+d,y+h/2,0],color=BLUE,stroke_width=7) for d in (-.65,.65)])
    for yy in np.linspace(y-h/2+.4,y+h/2-.4,6):
        rung=Line([x-.65,yy,0],[x+.65,yy,0],color=GREY,stroke_width=3)
        g.add(DashedVMobject(rung,num_dashes=6).set_opacity(.6))
    return g


class S00Title(TitleCard):
    LESSON=LESSON
    TITLE='Mammals Mute Robo,\nand Also Clear It'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',y=2.7,color=TEAL,size=26),
                 label('Crossing the Midline Once:\nSlit, Robo and Comm',y=1.3,color=GREY,size=28))
        self.play(FadeIn(T(self.TITLE,size=47,font=TITLE_FONT).move_to([0,-.7,0])),run_time=.6)
        self.add(Line([-1.3,-2.5,0],[1.3,-2.5,0],color=GOLD,stroke_width=4))
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        c=cone(-4.6,.2,1.5)
        self.add(cord(),label('mouse spinal cord',y=3.2,size=33),c,route([(-5.4,.2),(-4.6,.2)]))
        self.at('has been found')
        self.play(FadeIn(chip('Comm: some insects',PURPLE,26).move_to([3.45,-3.2,0])),run_time=.4)
        self.at('So how does')
        self.play(Create(route([(-4.6,.2),(-1.7,.2)])),c.animate.move_to([-1.7,.2,0]),run_time=.9)
        self.at('stay deaf')
        self.play(FadeIn(label('Deaf until it crosses?',2.8,-1.5,size=31)),run_time=.4)
        self.finish()


class S02Three(SpokenScene):
    def construct(self):
        self.add(label('fly',-3.3,3.1,size=34),label('mouse',3.1,3.1,size=34),
                 Line([0,-2.9,0],[0,2.9,0],color=GREY))
        self.at('The fly has')
        self.play(FadeIn(chip('one slit gene',RED,29).move_to([-3.3,2,0])),run_time=.4)
        fc=wide_cone(-3.3,-1.2,3.4)
        fr=receptor('Robo',-3.3,-1.2)
        self.play(FadeIn(fc),FadeIn(fr),run_time=.5)
        self.at('Mice have')
        genes=VGroup(*[chip('Slit'+str(i),RED,26).move_to([x,2,0]) for i,x in enumerate((1.1,3.1,5.1),1)])
        self.play(FadeIn(genes),FadeIn(wide_cone(3.1,-1.2,4.4)),run_time=.5)
        self.at('conventional Robo')
        self.play(FadeIn(label('receptors on growth cone',3.1,-2.9,YELLOW,26)),run_time=.3)
        self.at('Robo one')
        self.play(FadeIn(receptor('Robo1',2,-1.2)),run_time=.25)
        self.at('and Robo two')
        self.play(FadeIn(receptor('Robo2',4.2,-1.2)),run_time=.25)
        self.finish()


class S03Earlier(SpokenScene):
    def construct(self):
        c=cone(-4.7,.2,1.3)
        self.add(cord(),c,route([(-5.3,.2),(-4.7,.2)]),label('mouse spinal cord',y=3.2,size=30))
        self.at('mice lacking')
        self.play(FadeIn(deletion(['Slit1','Slit2'],1.7)),run_time=.5)
        self.at('had no defect')
        path=route([(-4.7,.2),(-1.5,.2),(1.3,-.7),(3.8,-.7),(4.5,-1.6)])
        self.play(Create(path),MoveAlongPath(c,path),run_time=1.4)
        self.play(FadeIn(label('normal commissural guidance',y=-2.6,size=30)),run_time=.35)
        self.finish()


class S04Q1(SpokenScene):
    def construct(self):
        self.add(prediction())
        cite=label('Long, Tessier-Lavigne and colleagues · 2004',y=3.2,color=GREY,size=26)
        self.at('In 2004')
        self.add(cite)
        self.at('removed all three')
        self.play(FadeIn(deletion(['Slit1','Slit2','Slit3'])),run_time=.35)
        self.play(FadeOut(cite),run_time=.1)
        self.play(FadeIn(label('All three Slit genes removed',y=3.2,size=33)),run_time=.15)
        self.at('Use the three questions')
        questions=label('Is Slit there?   Can it hear?\nWhen does hearing start?',y=-1.5,size=28)
        self.play(FadeIn(questions),run_time=.25)
        self.at('What should the axons')
        self.play(FadeOut(questions),run_time=.3)
        self.finish()


class S05Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(q1()); self.wait(5)


class S06Rev1(SpokenScene):
    def construct(self):
        c=cone(-4.7,.3,1.9)
        anatomy=cord()
        anatomy[0].stretch_to_fit_height(6.1)
        anatomy[1].stretch_to_fit_height(5.4)
        anatomy[2].move_to([0,-3.5,0])
        self.add(anatomy,label('No Slit → no Slit push',y=3.2,color=RED,size=33),
                 c,route([(-5.3,.3),(-4.7,.3)]))
        self.at('though other cues remain')
        self.play(FadeIn(label('other cues remain',-3.5,-1.65,GREY,27)),run_time=.4)
        self.at('The axons still reach')
        p=route([(-4.7,.3),(0,.3)])
        self.play(Create(p),MoveAlongPath(c,p),run_time=1.2)
        self.at('drawn by netrin')
        # Netrin spreads away from the floor plate; attraction points back to it.
        field=VGroup(*[Arrow([side*.5,y,0],[side*3.4,y+dy,0],
            color=GREEN,buff=0,stroke_width=3).set_opacity(.6)
            for side in (-1,1) for y,dy in ((-.65,-.9),(.95,.9))])
        dots=VGroup(*[Dot([side*x,y,0],radius=.065,color=GREEN).set_opacity(a)
            for side in (-1,1) for x,a in ((.65,.9),(1.4,.65),(2.2,.4),(3.0,.2))
            for y in (-.7,-1.2)])
        self.play(FadeIn(dots),FadeIn(field),
                  GrowArrow(Arrow([-4.6,.7,0],[-.55,.7,0],color=GREEN,buff=0,stroke_width=7)),
                  FadeIn(label('netrin · toward floor plate',0,2.5,GREEN,27)),run_time=.5)
        self.finish()


class S07Rev1b(SpokenScene):
    def construct(self):
        self.add(label('No Slit → no Slit push',y=3.2,color=RED,size=32),
            Ellipse(width=6.8,height=5.5,color=GREY).move_to([-2.65,-.15,0]),
            RoundedRectangle(width=.6,height=4.6,corner_radius=.15,color=GREY,
                fill_color=GREY,fill_opacity=.25).move_to([-1.1,-.15,0]),
            label('mouse floor plate',-2.3,-3.2,GREY,26),
            Line([1.1,-2.9,0],[1.1,2.6,0],color=GREY))
        self.at('Many stalled')
        self.play(Create(route([(-5.2,.3),(-1.1,.3)])),FadeIn(cone(-1.1,.3,1.2)),
            FadeIn(label('stall',-2.1,1,BLUE,28)),run_time=.6)
        slit=VGroup(*[Line([x,.7,0],[x,1.9,0],color=BLUE,stroke_width=5) for x in (3,3.7,4.4)])
        self.play(FadeIn(slit),FadeIn(label('fly slit mutant: stalls',3.7,2.5,size=26)),run_time=.25)
        self.at('Others crossed')
        p=route([(-5.2,-1.1),(.1,-1.1),(.1,-2),(-1.2,-2)])
        c=cone(-5.2,-1.1,1.0);self.add(c)
        self.play(Create(p),MoveAlongPath(c,p),run_time=.85)
        robo=VGroup(*[Line([x,-2.4,0],[x,-1.2,0],color=BLUE,stroke_width=5) for x in (3,4.4)],
            *[Line([3,y,0],[4.4,y,0],color=BLUE,stroke_width=4) for y in (-2.2,-1.8,-1.4)])
        self.play(FadeIn(robo),FadeIn(label('fly robo mutant: recrosses',3.7,-.65,size=26)),
            FadeIn(label('turn back',-2.8,-2.3,BLUE,27)),run_time=.3)
        self.finish()


class S08Zou(SpokenScene):
    def construct(self):
        spinal=RoundedRectangle(width=2,height=4.5,corner_radius=.3,color=GREY,fill_color=GREY,fill_opacity=.15)
        self.add(spinal,label('embryonic rat spinal cord',y=3.15,size=32))
        self.at('a culture experiment')
        self.play(Circumscribe(spinal,color=GREY),run_time=.4)
        self.at('and colleagues grew')
        self.play(FadeIn(label('Zou and colleagues',y=-3.1,color=GREY,size=28)),run_time=.35)
        a=Rectangle(width=.9,height=1.5,color=TEXT,fill_color=GREY,fill_opacity=.6).move_to([-.5,.9,0])
        b=a.copy().move_to([.5,-.9,0])
        self.at('pieces of embryonic')
        self.play(Create(a),Create(b),run_time=.5)
        self.at('called explants')
        self.play(a.animate.scale(1.4).move_to([-3.05,0,0]),b.animate.scale(1.4).move_to([3.05,0,0]),
                  FadeOut(spinal),run_time=.65)
        self.at('in a gel')
        gel=VGroup(*[RoundedRectangle(width=5.7,height=4.7,corner_radius=.3,color=GREY,
                           fill_color=GREY,fill_opacity=.05).move_to([x,-.1,0]) for x in (-3.05,3.05)])
        self.play(FadeIn(gel),FadeIn(label('explants in collagen gel',y=2.55,size=29)),run_time=.4)
        self.finish()


class S09Zou2(SpokenScene):
    def construct(self):
        self.add(dishes(),label('netrin added to dorsal explants',-3.05,-3.1,GREEN,26))
        self.at('Dorsal explants gave')
        self.play(Create(growth(-3.05)),run_time=1.2)
        self.at('Explants that kept')
        self.play(Circumscribe(self.mobjects[0][1][1],color=TEXT),run_time=.6)
        self.at('plate gave axons')
        self.play(Create(growth(3.05)),run_time=1)
        self.finish()


class S10Q2(SpokenScene):
    def construct(self):
        self.add(dishes())
        self.at('Each kind sat beside')
        # Add only the Slit2 cells and their adjacent labels.
        self.play(*[FadeIn(VGroup(*dish(x,c,True)[4:6])) for x,c in ((-3.05,False),(3.05,True))],run_time=.6)
        self.at('Which axons should')
        self.play(FadeIn(VGroup(*q2()[1:])),run_time=.5)
        self.finish()


class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(q2()); self.wait(5)


class S12Rev2(SpokenScene):
    def construct(self):
        self.add(dishes(True))
        self.add(label('dashed = control-cell outgrowth',y=-3.1,color=GREY,size=28))
        self.at('held back the growth')
        # Matched controls give a visible baseline; the two Slit2 results grow together.
        self.play(Create(growth(-3.05,ghost=True)),Create(growth(3.05,ghost=True)),
                  Create(growth(-3.05)),Create(growth(3.05,short=True)),run_time=1.5)
        bracket=VGroup(Line([2.28,1.3,0],[2.76,1.3,0],color=BLUE,stroke_width=3),
                       Line([2.28,1.18,0],[2.28,1.42,0],color=BLUE),
                       Line([2.76,1.18,0],[2.76,1.42,0],color=BLUE),label('short',3.1,1.85,BLUE,27))
        self.play(FadeIn(bracket),run_time=.3)
        self.at('Axons that had not crossed')
        self.play(Circumscribe(self.mobjects[0][0][1],color=BLUE),run_time=.6)
        self.finish()


class S13Same(SpokenScene):
    def construct(self):
        self.add(dishes(True),growth(-3.05),growth(3.05,short=True))
        # A single caption block, with separate leads from the two preparations.
        self.at('These were different axons')
        captext=label('Different axons',y=-3.15,size=32)
        self.play(FadeIn(captext),Create(leader((-3.05,-2.48),(-1.5,-2.88))),
                  Create(leader((3.05,-2.48),(1.5,-2.88))),run_time=.5)
        self.at('crossing goes with')
        self.play(FadeOut(captext),run_time=.15)
        self.play(FadeIn(label('Crossing goes with a different Slit response',y=-3.15,size=29)),run_time=.35)
        self.finish()


class S14Robo3(SpokenScene):
    def construct(self):
        stage=VGroup(membrane(deep=True),
                     receptor('Robo1',-3.4).scale(1.45,about_point=[-3.4,0,0]),
                     receptor('Robo2',3.4).scale(1.45,about_point=[3.4,0,0])).shift(DOWN*.35)
        self.add(stage,label('Before crossing',y=3.15,size=33))
        self.at('An unusual member')
        odd=odd_receptor(0).scale(1.45,about_point=ORIGIN).shift(DOWN*.35)
        self.play(FadeIn(odd),run_time=.55)
        self.at('called Robo3')
        self.play(FadeIn(label('Robo3 · also called Rig-1',0,2.65,ORANGE,30)),run_time=.25)
        self.finish()


class S15Sabatier(SpokenScene):
    def construct(self):
        self.add(cord(),route([(-5,0),(-.5,0)]),cone(-.5,0,1.3))
        self.at('In 2004')
        self.add(label('Sabatier, Tessier-Lavigne and colleagues · 2004',y=3.2,color=GREY,size=26))
        self.at('found on commissural axons')
        self.play(Create(route([(-5,0),(-.5,0)],ORANGE,10)),
                  FadeIn(label('Robo3 on this axon',-3,1.3,ORANGE,29)),
                  Create(leader((-3,1),(-3,.15),ORANGE)),run_time=.5)
        self.at('before they cross')
        self.play(FadeIn(label('before crossing',-3,-1.7,ORANGE,30)),run_time=.3)
        self.finish()


class S16Q3(SpokenScene):
    def construct(self):
        g=q3()
        self.add(g[0],g[1],g[2],g[4],g[5],g[6])
        self.at('Remove Robo three')
        self.play(Circumscribe(g[4],color=ORANGE),run_time=.4)
        self.at('Slit is present')
        self.play(Circumscribe(g[0][-1],color=RED),run_time=.4)
        self.at('Robo one and Robo two')
        self.play(FadeIn(g[3]),run_time=.3)
        self.at('Predict')
        self.play(Circumscribe(g[5],color=TEXT),run_time=.4)
        self.finish()


class S17Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(q3()); self.wait(5)


class S18Rev3(SpokenScene):
    def construct(self):
        cs=VGroup(cone(-5,.7,1.2),cone(-5,-.7,1.2))
        self.add(cord(True),label('Without Robo3',y=3.2,color=ORANGE,size=33),cs)
        self.at('Almost no commissural')
        a=route([(-5,.7),(-.95,.7)])
        b=route([(-5,-.7),(-.95,-.7)])
        self.play(Create(a),Create(b),MoveAlongPath(cs[0],a),MoveAlongPath(cs[1],b),run_time=1.3)
        self.at('They approach the floor plate')
        a=route([(-.95,.7),(-.95,1.95)])
        b=route([(-.95,-.7),(-.95,-1.95)])
        self.play(Create(a),Create(b),MoveAlongPath(cs[0],a),MoveAlongPath(cs[1],b),
                  FadeIn(label('Slit heard too early',-3.3,-2.4,RED,28)),run_time=1)
        self.at('They hear Slit too early')
        self.play(Circumscribe(self.mobjects[-1],color=RED),run_time=.4)
        self.finish()


class S19Comm(SpokenScene):
    def construct(self):
        self.add(label('mouse: no Robo3',-3.15,3.1,ORANGE,30),
                 label('fly: comm mutant',3.15,3.1,PURPLE,30))
        self.add(RoundedRectangle(width=.6,height=4.5,corner_radius=.15,color=GREY,
                    fill_color=GREY,fill_opacity=.25).move_to([-2,0,0]),
                 route([(-5,.7),(-2.8,.7),(-2.8,2)]),cone(-2.8,2,1),
                 route([(-5,-.7),(-2.8,-.7),(-2.8,-2)]),cone(-2.8,-2,1))
        self.at('That resembles')
        self.play(FadeIn(ladder(3.15)),run_time=.5)
        self.add(label('longitudinal tracts',3.15,-2.7,BLUE,26),
                 label('missing rungs: no crossing',3.15,-3.25,GREY,26),
                 label('no crossing',-3.15,-3.1,BLUE,28))
        self.finish()


class S20Mute(SpokenScene):
    def construct(self):
        rs=VGroup(*[receptor(name,x).scale(1.35,about_point=[x,0,0]).shift(DOWN*.35)
                    for name,x in (('Robo1',-2.7),('Robo2',2.7))])
        mem=membrane(deep=True).shift(DOWN*.35)
        self.add(mem,rs,odd_receptor(0).scale(1.35,about_point=ORIGIN).shift(DOWN*.35),
                 label('Robo3',0,2.3,ORANGE,31),
                 label('cartoon of the effect, not a known contact',y=-3.55,size=27))
        self.at('does not clear')
        self.play(*[Indicate(r,color=YELLOW,scale_factor=1.04) for r in rs],run_time=.6)
        self.at('It blunts their response')
        self.play(FadeIn(covers(),shift=DOWN*.25),run_time=.6)
        self.at('they stay in the membrane')
        self.play(Circumscribe(mem[1],color=BLUE),run_time=.5)
        self.finish()


def mouse_panel():
    return VGroup(label('mouse',3.1,3.2,size=33),
        Rectangle(width=5.5,height=2.1,stroke_opacity=0,fill_color=BLUE,fill_opacity=.07).move_to([3.1,-1.35,0]),
        Line([.4,-.3,0],[5.8,-.3,0],color=BLUE,stroke_width=9),
        receptor('Robo1/2',3.1,-.3),cap(3.1,1.0,2.5),
        label('Robo3 cap',3.1,2.7,ORANGE,28),
        label('muted at the surface',3.1,-2.8,ORANGE,28))


class S21Mute2(SpokenScene):
    def construct(self):
        self.add(label('fly',-3.1,3.2,size=33),mouse_panel(),
                 Line([0,-3.4,0],[0,3.4,0],color=GREY))
        golgi=chip('Golgi',GREY,28).move_to([-4.8,1.8,0])
        comm=chip('Comm',PURPLE,28).move_to([-2.1,.15,0])
        dest=RoundedRectangle(width=3,height=1.35,corner_radius=.4,color=GREY,
                              fill_color=GREY,fill_opacity=.1).move_to([-3.1,-1.45,0])
        rb=chip('Robo1',YELLOW,28).move_to([-4.8,1.0,0])
        rb[0].set_fill(BG,opacity=1)
        # A complete default route from Golgi to the cell surface is visible first.
        surface=Line([-.5,.3,0],[-.5,2.3,0],color=BLUE,stroke_width=8)
        normal_route=route([(-4.8,1.0),(-3.5,1.0),(-.65,1.0)],YELLOW,4)
        tip=Arrow([-1.3,1,0],[-.55,1,0],color=YELLOW,buff=0)
        self.add(golgi,dest,label('lysosome',-3.1,-2.5,GREY,28),
                 surface,label('surface',-1.25,2.3,BLUE,26),normal_route,tip,rb,
                 label('+ another inhibitory\nactivity',-3.15,-3.2,PURPLE,26))
        self.at('lowers Robo one by sorting')
        self.play(rb.animate.move_to([-3.5,1,0]),run_time=.35)
        self.play(FadeIn(comm),normal_route.animate.set_opacity(.4),tip.animate.set_opacity(.4),
                  GrowArrow(Arrow([-3.5,.65,0],[-3.1,-.65,0],color=PURPLE,buff=0)),run_time=.35)
        self.play(rb.animate.move_to([-3.1,-1.45,0]),run_time=.7)
        self.at('at least one other way')
        self.play(rb.animate.set_opacity(.25),run_time=.3)
        self.at('mutes it')
        self.play(Circumscribe(self.mobjects[1][4],color=ORANGE),run_time=.5)
        self.finish()


class S21bNdfip(SpokenScene):
    def construct(self):
        cell=RoundedRectangle(width=7.25,height=5.6,corner_radius=.35,color=BLUE,
                              fill_color=BLUE,fill_opacity=.04).move_to([-2.225,-.25,0])
        self.add(cell,label('commissural neuron before crossing',y=3.2,size=32))
        membrane_line=Line([1.4,-2.9,0],[1.4,2.5,0],color=BLUE,stroke_width=9)
        self.add(membrane_line,label('axon surface',3.9,-2.6,BLUE,28))
        surface=chip('Robo1',YELLOW,28).move_to([1.4,.5,0])
        surface[0].set_fill(BG,opacity=1)
        self.add(Line([1.05,.5,0],[1.75,.5,0],color=YELLOW,stroke_width=6),surface,
            cap(0,0,2.0).rotate(-PI/2).move_to([2.6,.5,0]),
            label('Robo3',3.8,2.3,ORANGE,28),leader((3.8,1.95),(2.9,1.3),ORANGE))
        new=chip('new Robo1',YELLOW,28).move_to([-3.7,1.5,0])
        endo=RoundedRectangle(width=3.2,height=1.9,corner_radius=.35,color=GREY,
                              fill_color=GREY,fill_opacity=.15).move_to([-2.4,-1.35,0])
        self.at('Mammals also clear some')
        self.play(FadeIn(new),FadeIn(endo),FadeIn(label('endosome',-2.4,-2.65,GREY,28)),run_time=.4)
        self.at('Proteins called')
        nd=chip('Ndfip1/2',TEAL,27).next_to(new,DOWN,buff=.15)
        self.play(FadeIn(nd),run_time=.4)
        self.at('send it to be degraded')
        cargo=VGroup(new,nd)
        self.play(GrowArrow(Arrow([-3.7,.2,0],[-2.4,-.6,0],color=TEAL,buff=0)),
                  cargo.animate.move_to([-2.4,-1.3,0]),run_time=.75)
        self.play(cargo.animate.set_opacity(.25),FadeIn(label('degradation',-2.4,-3.3,TEAL,28)),run_time=.35)
        # The other branch reaches the contiguous axon surface in smaller amount.
        survivor=chip('Robo1',YELLOW,28).move_to([-.4,1.5,0])
        survivor[0].set_fill(BG,opacity=1)
        self.play(FadeIn(survivor),GrowArrow(Arrow([-.1,1.5,0],[1.05,1.5,0],color=YELLOW,buff=0)),run_time=.3)
        self.play(survivor.animate.move_to([1.4,.5,0]),run_time=.45)
        self.remove(surface)
        self.add(label('less reaches surface;\nstill muted',3.9,-1.1,YELLOW,27))
        self.finish()


def form_stage():
    return VGroup(cord(),label('before crossing',-3.3,-2.2,GREY,28),
                  label('after crossing',3.3,-2.2,GREY,28),label('Robo3 splice forms',y=3.2,color=ORANGE,size=33))


class S22Forms(SpokenScene):
    def construct(self):
        self.add(form_stage())
        c=cone(-2.4,0,1.3)
        pre=route([(-5.2,0),(-2.4,0)],ORANGE,9)
        tag=chip('Robo3.1',ORANGE,30).move_to([-3.4,1.2,0])
        link=leader((-3.4,.8),(-3.4,.1),ORANGE)
        self.add(pre,c)
        self.at('Two splice forms')
        self.play(FadeIn(tag),Create(link),run_time=.45)
        self.at('the form present before crossing')
        p=route([(-2.4,0),(0,0)],ORANGE,9)
        self.play(Create(p),MoveAlongPath(c,p),run_time=.9)
        self.at('disappears afterwards')
        p2=route([(0,0),(4.6,0)],BLUE,9)
        self.play(Create(p2),MoveAlongPath(c,p2),pre.animate.set_color(BLUE),p.animate.set_color(BLUE),
                  FadeOut(tag),FadeOut(link),run_time=.9)
        self.finish()


class S23Forms2(SpokenScene):
    def construct(self):
        self.add(form_stage(),route([(-5.2,0),(4.6,0)]),cone(4.6,0,1.3))
        self.at('A second form appears')
        self.play(Create(route([(.6,0),(4.6,0)],ORANGE,10)),
                  FadeIn(chip('Robo3.2',ORANGE,30).move_to([3.2,1.2,0])),
                  Create(leader((3.2,.8),(3.2,.1),ORANGE)),run_time=.65)
        self.at('helps keep them')
        self.play(GrowArrow(Arrow([4,-1,0],[.8,-1,0],color=BLUE,buff=0)),
                  Create(cross(.8,-1,.23)),FadeIn(label('no recrossing',3.2,-1.6,size=29)),run_time=.5)
        self.finish()


class S24Netrin(SpokenScene):
    def construct(self):
        self.add(label('Strengthening netrin attraction',y=3.2,size=33))
        # A persistent before/after comparison makes the change measurable by eye.
        for x in (-3.1,3.1):
            self.add(Rectangle(width=5.5,height=2.1,stroke_opacity=0,fill_color=BLUE,
                        fill_opacity=.07).move_to([x,-1.05,0]),
                     Line([x-2.7,0,0],[x+2.7,0,0],color=BLUE,stroke_width=9))
        self.add(label('without Robo3',-3.1,2.4,GREY,29),label('with Robo3',3.1,2.4,ORANGE,29))
        self.at('has a second job')
        self.play(FadeIn(chip('DCC',GREEN,30).move_to([-3.1,.55,0])),
                  GrowArrow(Arrow([-3.1,-.5,0],[-3.1,-2.2,0],color=GREEN,stroke_width=3,buff=0)),
                  FadeIn(label('netrin pull',-3.1,-2.85,GREEN,28)),run_time=.5)
        self.at('works with the netrin receptor')
        self.play(FadeIn(chip('DCC',GREEN,30).move_to([3.9,.55,0])),
                  FadeIn(odd_receptor(2.25)),FadeIn(label('Robo3',2.25,1.9,ORANGE,27)),
                  Create(Line([2.65,.65,0],[3.2,.65,0],color=GREEN,stroke_width=4)),run_time=.6)
        self.at('strengthens netrin attraction')
        self.play(GrowArrow(Arrow([3.5,-.5,0],[3.5,-2.2,0],color=GREEN,stroke_width=13,buff=0)),
                  FadeIn(label('stronger netrin pull',3.1,-2.85,GREEN,28)),run_time=.7)
        self.finish()


class S25Human(SpokenScene):
    def construct(self):
        self.add(chip('Human ROBO3',ORANGE,33).move_to([0,3.15,0]))
        head=Ellipse(width=5.2,height=4.6,color=GREY,fill_color=GREY,fill_opacity=.04).move_to([-3,-.15,0])
        eyes=VGroup(*[VGroup(Ellipse(width=1.6,height=.9,color=TEXT),Dot(radius=.18,color=BLUE)).move_to([x,.5,0]) for x in (-4.15,-1.85)])
        self.at('The same gene matters')
        self.play(FadeIn(head),FadeIn(eyes),run_time=.4)
        self.at('Mutations in human')
        self.play(FadeIn(chip('mutated',RED,27).move_to([3.2,3.15,0])),run_time=.35)
        self.at('horizontal gaze palsy')
        # Arrow runs across the eyes, above the pupil centres, with a block at its end.
        self.play(Create(DoubleArrow([-5,.95,0],[-1,.95,0],color=BLUE,buff=0)),
                  Create(Line([-1, .65,0],[-1,1.25,0],color=RED,stroke_width=8)),
                  FadeIn(label('horizontal gaze palsy',-3,-2.9,size=28)),run_time=.5)
        self.at('progressive scoliosis')
        pts=[(3.1+.65*np.sin(1.6*y),y) for y in np.linspace(-2,2,60)]
        spine=route(pts,GREY,8)
        vertebrae=VGroup(*[Line([3.1+.65*np.sin(1.6*y)-.25,y,0],
             [3.1+.65*np.sin(1.6*y)+.25,y,0],color=GREY,stroke_width=5) for y in np.linspace(-2,2,16)])
        self.play(Create(spine),FadeIn(vertebrae),FadeIn(label('progressive scoliosis',3.1,-2.9,size=28)),run_time=.65)
        self.finish()


def brain_panel(x,patient=False):
    box=RoundedRectangle(width=5.1,height=5.5,corner_radius=.55,color=GREY,
                         fill_color=GREY,fill_opacity=.06).move_to([x,-.15,0])
    mid=DashedLine([x,-2.05,0],[x,2.45,0],color=GREY)
    # Separate crossing levels for motor (descending) and sensory (ascending).
    motor=[(x-1.4,2),(x-1.4,.8),(x+1.4,-.5),(x+1.4,-2.2)]
    sensory=[(x-1.4,-2.2),(x-1.4,-.8),(x+1.4,.5),(x+1.4,2)]
    paths=VGroup(route(motor,BLUE,7),route(sensory,GOLD,7))
    labels=VGroup(label('motor',x-1.35,1.55,BLUE,26),
                  label('sensory',x-1.35,-1.55,GOLD,26))
    if patient:
        ghosts=VGroup(*[DashedVMobject(p,num_dashes=22).set_opacity(.6) for p in paths])
        paths=VGroup(route([(x-1.4,2),(x-1.4,.8),(x-.25,.2)],BLUE,7),
                      route([(x-1.4,-2.2),(x-1.4,-.8),(x-.25,-.2)],GOLD,7))
        return VGroup(box,mid,ghosts,paths,labels)
    return VGroup(box,mid,paths,labels)


class S26Human2(SpokenScene):
    def construct(self):
        normal=brain_panel(-3.05)
        self.add(normal[0],normal[1],label('normal brainstem',-3.05,3.3,size=29),
                 label('patient brainstem',3.05,3.3,size=29))
        patient=brain_panel(3.05,True)
        self.add(patient[0],patient[1])
        self.at('motor and sensory pathways')
        self.play(Create(normal[2]),FadeIn(normal[3]),run_time=.7)
        self.at('normally cross in the brainstem')
        self.play(Circumscribe(normal[2]),run_time=.5)
        self.at('appear uncrossed')
        self.play(FadeIn(patient[2]),Create(patient[3]),FadeIn(patient[4]),
                  FadeIn(label('appear uncrossed',3.05,-2.45,size=28)),run_time=.65)
        self.finish()


class S27Take(SpokenScene):
    def construct(self):
        self.add(label('Until the axon crosses',y=3.25,size=35))
        for x,name in ((-3.15,'fly'),(3.15,'mouse')):
            self.add(RoundedRectangle(width=5.8,height=5.5,corner_radius=.3,color=GREY,
                         fill_color=GREY,fill_opacity=.04).move_to([x,-.2,0]),label(name,x,2.1,size=33))
        self.add(chip('Comm',PURPLE,32).move_to([-3.15,1.3,0]),
            label('sorting\n+ another activity',-3.15,-.15,PURPLE,29),
            Arrow([-3.15,-.85,0],[-3.15,-1.6,0],color=PURPLE,buff=0),
            label('lowers Robo1',-3.15,-2.25,YELLOW,30))
        self.at('both mute their')
        self.play(FadeIn(chip('Robo3',ORANGE,32).move_to([3.15,1.3,0])),
                  FadeIn(label('mutes Robo1 / Robo2',3.15,.3,ORANGE,29)),run_time=.4)
        self.at('clear some of them')
        self.play(FadeIn(chip('Ndfip1/2',TEAL,30).move_to([3.15,-.9,0])),
                  FadeIn(label('clear some Robo1',3.15,-2.25,TEAL,29)),
                  Create(Line([3.15,-1.3,0],[3.15,-1.8,0],color=TEAL,stroke_width=4)),run_time=.4)
        self.at('until the axon has crossed')
        self.play(Circumscribe(self.mobjects[0]),run_time=.5)
        self.finish()


class S28End(EndCard):
    LINE='Mouse axons mute Robo receptors\nand clear some until crossing.'
    def construct(self):
        self.add(label('UNTIL CROSSING',y=2.6,color=ORANGE,size=28))
        self.play(FadeIn(T(self.LINE,size=44,font=TITLE_FONT).move_to([0,.2,0])),run_time=.5)
        self.add(label('biochemistrypedia.com',y=-2.4,color=TEAL,size=27))
        self.finish()
