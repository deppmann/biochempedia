"""Neighbours Compare: reviewed animation.
COLOR MAP: YELLOW light/input; GREEN response/output; BLUE comparisons;
RED inhibition/cut; GREY anatomy/axes; TEXT labels; TEAL brand.
Feedforward bars computed from E - .2*(left E + right E).
Recurrent bars solve r + .2*(left r + right r) = E on a long row.
"""
import numpy as np
from bp_style import *


def label(s, x, y, color=TEXT, size=28):
    return T(s, size=size, color=color).move_to([x,y,0])


def unit(x,y,r=.7,color=GREY):
    return RegularPolygon(6, radius=r, color=color, fill_color=color, fill_opacity=.16).move_to([x,y,0])


def inhib(a,b,w=4):
    a,b=np.array(a,float),np.array(b,float)
    v=(b-a)/np.linalg.norm(b-a); p=np.array([-v[1],v[0],0])*.13
    return VGroup(Line(a,b,color=RED,stroke_width=w),Line(b-p,b+p,color=RED,stroke_width=w))


def trace(state='steady'):
    # Qualitative experimental states, not invented measured firing rates.
    xs=np.linspace(2.1,5.7,181)
    level=np.ones_like(xs)*.9
    if state=='fell': level[xs>=3.55]=-.15
    if state=='recovered': level[(xs>=3.0)&(xs<4.25)]=-.15
    return VMobject(color=GREEN,stroke_width=5).set_points_as_corners(
        [[x,y,0] for x,y in zip(xs,level)])


def experiment(lit=False,state='steady',links=False):
    xs=[-5,-2.7,-.4]
    units=VGroup(*[unit(x,.45,.95,BLUE if i==1 else GREY) for i,x in enumerate(xs)])
    lights=VGroup(*[VGroup(Rectangle(width=1.2,height=.45,stroke_width=0,fill_color=YELLOW,
          fill_opacity=1).move_to([x,2.65,0]),Arrow([x,2.3,0],[x,1.48,0],buff=0,color=YELLOW)) for x in xs])
    for i in [0,2]: lights[i].set_opacity(1 if lit else 0)
    connections=VGroup(inhib([-4.04,.45,0],[-3.65,.45,0]),inhib([-1.36,.45,0],[-1.75,.45,0]))
    if not links: connections.set_opacity(0)
    electrode=VGroup(Polygon([-2.77,.15,0],[-2.62,-.25,0],[-2.05,-1.55,0],[-1.8,-1.55,0],
                            color=TEXT,fill_color=TEXT,fill_opacity=.5),
                      Line([-1.92,-1.55,0],[-1.92,-2.1,0],color=TEXT),
                      label('microelectrode',-2.0,-2.45,size=28))
    axes=VGroup(Line([1.85,-1.4,0],[5.9,-1.4,0],color=GREY),
                Arrow([1.85,-1.4,0],[1.85,1.7,0],buff=0,color=GREY),
                label('time →',4,-1.85,GREY),label('firing rate',3.9,2.15,GREEN,32),
                label('qualitative',3.9,1.65,GREY,26))
    names=VGroup(VGroup(label('recorded unit',-4.3,-1.05,BLUE),Line([-3.8,-.8,0],[-3.1,-.2,0],color=BLUE)),label('same steady light',-2.7,3.35,YELLOW,28))
    return VGroup(units,lights,connections,electrode,axes,trace(state),names)


def question():
    panels=VGroup(*[RoundedRectangle(width=5.8,height=4.6,corner_radius=.18,color=GREY)
                      .move_to([x,0,0]) for x in [-3.15,3.15]])
    left=VGroup(unit(-4.65,.15,.85),unit(-1.65,.15,.85),inhib([-3.8,.15,0],[-2.5,.15,0]),
                label('Circuit connections',-3.15,-1.6,RED,32))
    right=VGroup(unit(3.15,-.5,.9),
       *[Arrow([3.15,1.65,0],[x,.45,0],buff=0,color=YELLOW,stroke_width=5) for x in [1.5,3.15,4.8]],
       label('Stray light in the eye',3.15,-1.6,YELLOW,30))
    return VGroup(label('Circuit, or stray light?',0,3.3,size=38),panels,left,right)


X=np.array([-4.,-2.4,-.8,.8,2.4,4.])
E=np.array([10.,10.,10.,20.,20.,20.])
O=E-.2*(np.r_[10,E[:-1]]+np.r_[E[1:],20])
SCALE=.105
IBASE,OBASE=.65,-2.85


def bar(x,v,base,color,outline=False):
    return Rectangle(width=.85,height=SCALE*v,stroke_color=color,stroke_width=2 if outline else 0,
       fill_color=color,fill_opacity=0 if outline else .88).move_to([x,base+SCALE*v/2,0])


def output(i):
    return VGroup(bar(X[i],O[i],OBASE,GREEN),label(str(int(O[i])),X[i],OBASE+SCALE*O[i]+.23,GREEN,30))


def row(stage=0):
    inputs=VGroup(*[VGroup(bar(x,e,IBASE,YELLOW),label(str(int(e)),x,IBASE+.26,BG,30)) for x,e in zip(X,E)])
    axes=VGroup(Line([-6,IBASE,0],[6,IBASE,0],color=GREY),Line([-6,OBASE,0],[6,OBASE,0],color=GREY),
        label('0',-6.25,OBASE,GREY,26))
    names=VGroup(label('light (made-up units)',0,3.35,YELLOW,28),
                 label('response (made-up units)',0,-.85,GREEN,28))
    eq=label('output = own − 0.2 × (left + right)',0,-.05,size=28)
    foot=label('Made-up units · feedforward toy model · row continues',0,-3.5,GREY,22)
    ghosts=VGroup(*[VGroup(bar(x,v,IBASE,YELLOW,True),label(str(v),x,IBASE+.26,YELLOW,28),
                 label('…',x,IBASE-.3,TEXT,34)) for x,v in [(-5.6,10),(5.6,20)]])
    outs=VGroup(*[output(i) for i in ([0,1,4,5] if stage==1 else range(6) if stage==2 else [])])
    return VGroup(inputs,axes,names,eq,foot,ghosts,outs)


def references(both=True):
    g=VGroup()
    for v,s,x in [(6,'dim plateau 6',-4.3),(12,'bright plateau 12',3.9)][:2 if both else 1]:
        y=OBASE+v*SCALE
        g.add(DashedLine([-5.9,y,0],[5.9,y,0],color=BLUE,stroke_width=2,dash_length=.1),
              label(s,x,-1.5 if v==6 else -.7,BLUE,26))
    return g


def prediction():
    return VGroup(label('Above or below the dim plateau?',0,-.04,BLUE,32),
                  SurroundingRectangle(row()[0][2],color=BLUE,buff=.08),
                  label('?',X[2],-2.05,BLUE,42))


def comparisons(plateau=False):
    g=VGroup()
    for base,lo,hi in [(IBASE,10,20),(OBASE,4,14)]:
        y0,y1=base+lo*SCALE,base+hi*SCALE
        for x,y in [(-.8,y0),(.8,y1)]:
            g.add(DashedLine([x,y,0],[0,y,0],color=BLUE,dash_length=.08))
        g.add(Line([0,y0,0],[0,y1,0],color=BLUE,stroke_width=4),
              *[Line([-.12,y,0],[.12,y,0],color=BLUE) for y in [y0,y1]])
    g.add(label('step 10',0,3.0,BLUE,28),label('step 10',.25,-.62,BLUE,28))
    if plateau:
        for base,lo,hi in [(IBASE,10,20),(OBASE,6,12)]:
            y0,y1=base+lo*SCALE,base+hi*SCALE
            for x,y in [(-2.4,y0),(2.4,y1)]:
                g.add(DashedLine([x,y,0],[4.85,y,0],color=BLUE,dash_length=.1,stroke_opacity=.65))
            g.add(Line([4.85,y0,0],[4.85,y1,0],color=BLUE,stroke_width=4),
                  *[Line([4.73,y,0],[4.97,y,0],color=BLUE) for y in [y0,y1]],
                  label('gap '+str(hi-lo),5.65,3.05 if base==IBASE else (y0+y1)/2,BLUE,26))
    return g


class S00Title(TitleCard):
    LESSON='Principles of Sensory Coding'
    TITLE='Neighbours Compare'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,1.55,TEAL,26),
                 label(self.LESSON,0,.8,GREY,30),
                 T(self.TITLE,size=54,font=TITLE_FONT).move_to([0,-.2,0]),
                 Line([-1.5,-1,0],[1.5,-1,0],color=GOLD,stroke_width=4))
        self.wait(3)


class S01Question(SpokenScene):
    def construct(self):
        patches=VGroup(*[Rectangle(width=1.55,height=2.3,stroke_width=0,fill_color=YELLOW,
                   fill_opacity=.43 if i<3 else .95).move_to([x,1.15,0]) for i,x in enumerate(X)])
        units=VGroup(*[unit(x,-1.15,.78) for x in X])
        reports=VGroup(*[Rectangle(width=.3,height=.55 if i<3 else 1.15,stroke_width=0,
                      fill_color=GREEN,fill_opacity=1).move_to([x,-1.55+(.55 if i<3 else 1.15)/2,0]) for i,x in enumerate(X)])
        self.add(patches,units)
        self.at('Each receptor'); self.play(FadeIn(reports),run_time=.5)
        self.at('so how'); self.play(FadeIn(label('How does the eye mark an edge?',0,3.2,size=36)),
                    Create(DashedLine([0,2.5,0],[0,-2.15,0],color=BLUE)),run_time=.5)
        self.at('Neighbors compare'); self.play(Indicate(VGroup(units[2],units[3]),color=BLUE),run_time=.6)
        self.finish()


class S02Eye(SpokenScene):
    def construct(self):
        # Dorsal silhouette: broad horseshoe shield, tapering abdomen and telson.
        shield=VMobject(color=GREY,fill_color=GREY,fill_opacity=.7).set_points_smoothly(
          [[-2,-.3,0],[-2.4,1,0],[-1.9,2.2,0],[0,2.9,0],[1.9,2.2,0],[2.4,1,0],[2,-.3,0],
           [1.2,.05,0],[0,.35,0],[-1.2,.05,0],[-2,-.3,0]])
        abdomen=Polygon([-1.4,.3,0],[1.4,.3,0],[1,-1.3,0],[.45,-1.85,0],[-.45,-1.85,0],[-1,-1.3,0],
                         color=GREY,fill_color=GREY,fill_opacity=.65)
        tail=Polygon([-.16,-1.7,0],[.16,-1.7,0],[0,-3.1,0],color=GREY,fill_opacity=.8,fill_color=GREY)
        eye=Ellipse(width=.27,height=.63,color=BLUE,fill_color=BLUE,fill_opacity=1).move_to([1.65,1.35,0])
        animal=VGroup(shield,abdomen,tail,eye,label('Limulus',-3.6,1.1,size=34))
        self.add(animal)
        self.at('has a compound eye')
        self.play(animal.animate.scale(.25).move_to([-5.45,2.6,0]),run_time=.45)
        self.remove(animal[-1]); self.add(label('Limulus',-5.45,3.55,size=28))
        centers=[(-2.8+1.8*c,2.4-1.9*r) for r in range(3) for c in range(3)]
        grid=VGroup(*[unit(x,y,.8) for x,y in centers])
        self.play(FadeIn(grid,scale=.4),Create(Line(eye.get_center(),[-3.65,2.4,0],color=BLUE)),run_time=.45)
        self.at('Each unit'); self.play(grid[2].animate.set_color(BLUE).set_fill(BLUE,.35),run_time=.25)
        self.at('an ommatidium')
        self.play(FadeIn(label('ommatidium',4.0,2.4,BLUE,30)),
                  Create(Line([1.6,2.4,0],[2.65,2.4,0],color=BLUE)),run_time=.25)
        # Fibre lanes leave the right side of every hexagon, then run in clear inter-row corridors.
        fibres=VGroup()
        for i,(x,y) in enumerate(centers):
            r,c=divmod(i,3); lane=y-.9-.07*c
            p=VMobject(color=GREEN if i==2 else GREY,stroke_width=4 if i==2 else 1.7)
            p.set_points_as_corners([[x+.58,y-.4,0],[x+.98,lane,0],[2.0+.14*i,lane,0],
                                    [2.0+.14*i,-2.65,0],[3.65+.14*i,-2.85,0]])
            fibres.add(p)
        bundle=RoundedRectangle(width=2.2,height=1.0,corner_radius=.2,color=GREEN,fill_color=GREEN,fill_opacity=.12).move_to([4.4,-2.85,0])
        self.at('sends its own'); self.play(Create(fibres),run_time=.6)
        self.at('the optic nerve'); self.play(Create(bundle),FadeIn(label('optic nerve',4.55,-1.65,GREEN,30)),run_time=.3)
        self.finish()


class S03Record(SpokenScene):
    def construct(self):
        e=experiment(); self.add(e[0],e[6][0],label('Hartline, Wagner and Ratliff · 1956',0,-3.3,size=28))
        self.at('recorded one'); self.play(FadeIn(e[3]),run_time=.5)
        self.at('Steady light'); self.play(FadeIn(e[1]),FadeIn(e[6][1]),run_time=.4)
        self.at('a steady discharge'); self.play(Create(e[4]),Create(e[5]),run_time=.5)
        self.finish()


class S04Neighbours(SpokenScene):
    def construct(self):
        e=experiment(); self.add(e)
        self.at('they lit'); self.play(e[1][0].animate.set_opacity(1),e[1][2].animate.set_opacity(1),run_time=.45)
        self.at('fell',lead=0); self.play(Transform(e[5],trace('fell')),run_time=.4)
        self.wait(2.2)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        q=question(); self.add(q[0],q[1])
        self.at('the circuit'); self.play(FadeIn(q[2]),run_time=.4)
        self.at('stray light'); self.play(FadeIn(q[3]),run_time=.4)
        self.finish()


class S06Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(question(),label('Pause and think · Your guess?',0,-3.1,BLUE,32)); self.wait(5)


class S07Cut(SpokenScene):
    def construct(self):
        # Expanded cutting view: separated ommatidia and long exposed connections.
        xs=[-4.5,0,4.5]; y=1.25
        units=VGroup(*[unit(x,y,1.35,BLUE if i==1 else GREY) for i,x in enumerate(xs)])
        lights=VGroup(*[VGroup(
            Rectangle(width=1.3,height=.35,stroke_width=0,fill_color=YELLOW,fill_opacity=1).move_to([x,3.4,0]),
            Arrow([x,3.1,0],[x,2.48,0],buff=0,color=YELLOW)) for x in xs])
        connections=VGroup(inhib([-3.12,y,0],[-1.38,y,0],6),inhib([3.12,y,0],[1.38,y,0],6))
        electrode=VGroup(Polygon([-.07,.95,0],[.08,.55,0],[-.65,-1.25,0],[-.9,-1.25,0],
            color=TEXT,fill_color=TEXT,fill_opacity=.5),
            Line([-.78,-1.25,0],[-.78,-2.05,0],color=TEXT),
            label('microelectrode',-2.1,-2.15,size=28))
        rate=trace('fell').shift(DOWN*2)
        axes=VGroup(Line([1.85,-3.4,0],[5.9,-3.4,0],color=GREY),
            Arrow([1.85,-3.4,0],[1.85,-.6,0],buff=0,color=GREY),
            label('time →',4,-3.7,GREY,24),label('firing rate · qualitative',4,-.35,GREEN,26))
        self.add(units,lights,connections,electrode,axes,rate,
            label('recorded unit',-3.0,-.65,BLUE,28),
            Line([-1.9,-.6,0],[-.7,.15,0],color=BLUE))
        scissors=VGroup(Circle(.2,color=TEXT,stroke_width=5).move_to([-.4,.24,0]),
             Circle(.2,color=TEXT,stroke_width=5).move_to([-.4,-.24,0]),
             Line([-.25,.2,0],[.48,-.32,0],color=TEXT,stroke_width=6),
             Line([-.25,-.2,0],[.48,.32,0],color=TEXT,stroke_width=6)).scale(3)
        self.at('cut the lateral')
        for i,x in enumerate([-2.25,2.25]):
            scissors.move_to([x,y+.15,0]); self.play(FadeIn(scissors),run_time=.15)
            self.play(scissors.animate.stretch(.25,1),run_time=.2)
            halves=VGroup(Line([x-.87,y,0],[x,y,0],color=RED,stroke_width=6),
                          Line([x,y,0],[x+.87,y,0],color=RED,stroke_width=6))
            self.remove(connections[i]); self.add(halves)
            self.play(halves[0].animate.shift(LEFT*.22+DOWN*.3),
                      halves[1].animate.shift(RIGHT*.22+DOWN*.3),FadeOut(scissors),run_time=.35)
            scissors.stretch(4,1)
        self.wait(1)
        self.at('no longer inhibited'); self.play(Transform(rate,trace('recovered').shift(DOWN*2)),run_time=.6)
        self.at('through connections'); self.play(FadeIn(label('Inhibition needs\nthe connections',-3.3,-3.1,RED,28)),run_time=.4)
        self.finish()


class S08Rule(SpokenScene):
    def construct(self):
        units=VGroup(*[unit(x,.45,1.1) for x in [-3.7,0,3.7]])
        self.add(units,label('A left–right slice through the eye',0,-3.5,GREY,28))
        self.at('its own light'); self.play(Create(Arrow([0,2.8,0],[0,1.6,0],color=YELLOW,buff=0)),
                       FadeIn(label('own light',0,3,YELLOW,28)),run_time=.35)
        self.at('minus a share')
        self.play(Create(inhib([-2.55,.45,0],[-1.15,.45,0])),Create(inhib([2.55,.45,0],[1.15,.45,0])),
                  FadeIn(label('output = own light − share × neighbours’ light',0,-1.65,size=30)),run_time=.4)
        self.at("of its neighbor's light"); self.play(FadeIn(label('share = 0.2 here',0,-2.75,RED,34)),run_time=.3)
        self.finish()


class S09Row(SpokenScene):
    def construct(self):
        r=row(); self.add(r[1],r[2])
        self.at('a row of units'); self.play(FadeIn(r[0]),run_time=.5)
        self.at('dim on the left'); self.play(Indicate(r[0][:3],color=YELLOW),run_time=.4)
        self.at('bright on the right'); self.play(Indicate(r[0][3:],color=YELLOW),run_time=.4)
        self.at('row continues'); self.play(FadeIn(r[5]),FadeIn(r[4]),run_time=.4)
        self.at('The numbers stay'); self.play(FadeIn(r[3]),run_time=.4)
        self.finish()


class S10Plateaus(SpokenScene):
    def construct(self):
        r=row(); self.add(r); self.remove(r[3],r[2][1]); self.add(label('response (made-up units)',0,-.5,GREEN,28))
        rings=VGroup(*[SurroundingRectangle(row()[0][i],color=BLUE,buff=.07) for i in [1,4]])
        self.at('each uniform region'); self.play(Create(rings),run_time=.4)
        self.at('inhibited by')
        calc=label('10 − 0.2 × (10 + 10) = 6     20 − 0.2 × (20 + 20) = 12',0,-.06,size=26)
        self.play(FadeIn(calc),run_time=.4)
        self.at('Both plateaus drop')
        self.remove(calc); self.play(FadeOut(rings),run_time=.15)
        outlines=VGroup(*[bar(X[i],E[i],OBASE,GREY,True) for i in [0,1,4,5]])
        drops=VGroup()
        for i,s in [(0,'−4'),(5,'−8')]:
            x=X[i]+(-.6 if i==0 else .6)
            drops.add(Arrow([x,OBASE+E[i]*SCALE,0],[x,OBASE+O[i]*SCALE,0],buff=0,color=RED),
                      label(s,x+(-.42 if i==0 else .42),OBASE+(E[i]+O[i])*SCALE/2,RED,28))
        self.add(outlines); self.play(*[GrowFromEdge(output(i),DOWN) for i in [0,1,4,5]],Create(drops),run_time=.6)
        self.wait(1); self.finish()


class S11Predict(SpokenScene):
    def construct(self):
        r=row(1); self.add(r); self.remove(r[3],r[2][1]); self.add(label('response (made-up units)',-3.6,-.85,GREEN,28))
        q=prediction(); self.add(references(False))
        self.at('Now'); self.play(FadeIn(q),run_time=.4)
        self.finish()


class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        r=row(1); self.add(r); self.remove(r[3],r[2][1]); self.add(label('response (made-up units)',-3.6,-.85,GREEN,28)); self.add(references(False),prediction())
        self.add(label('Pause and think · Your guess?',2.2,-.85,BLUE,26)); self.wait(5)


def arrow_pair(target):
    # Two subtractions from the named neighbours, held as a complete pair.
    g=VGroup()
    for source in [target-1,target+1]:
        amount=.2*E[source]
        a=[X[source],.47,0]; b=[X[target],.47,0]
        g.add(Arrow(a,b,buff=.18,color=RED,stroke_width=7 if amount==4 else 3),
              label(f'−{int(amount)}', (X[source]+X[target])/2,.02,RED,30))
    return g


class S13Reveal(SpokenScene):
    def construct(self):
        r=row(1); self.add(r); self.remove(r[3],r[2][1]); self.add(label('response (made-up units)',-3.6,-.85,GREEN,28)); self.add(references())
        r[4].move_to([0,-3.7,0])
        self.at('Below'); self.play(GrowFromEdge(output(2),DOWN),FadeIn(label('−2',X[2],-3.08,BLUE,26)),run_time=.5)
        pair=arrow_pair(2)
        self.at('Its bright neighbor'); self.play(FadeIn(pair),run_time=.4)
        self.at('the bright unit'); self.play(FadeOut(pair),GrowFromEdge(output(3),DOWN),
                  FadeIn(label('+2',X[3]+.85,-1.0,BLUE,30)),run_time=.4)
        pair2=arrow_pair(3); self.play(FadeIn(pair2),run_time=.35)
        self.finish()


class S14Meaning(SpokenScene):
    def construct(self):
        r=row(2); self.add(r); self.remove(r[3]); self.remove(r[2][0],r[2][1])
        self.add(label('light (made-up units)',-3.7,3.35,YELLOW,28),label('response (made-up units)',-3.6,-.7,GREEN,28))
        self.at('The step across'); self.play(Create(comparisons()),run_time=.6)
        self.finish()


class S15Contrast(SpokenScene):
    def construct(self):
        r=row(2); self.add(r); self.remove(r[3],r[2][0],r[2][1])
        self.add(label('light (made-up units)',-3.7,3.35,YELLOW,28),label('response (made-up units)',-3.6,-.7,GREEN,28),comparisons())
        self.at('uniform regions'); self.play(FadeIn(comparisons(True)[-12:]),run_time=.4)
        self.at('So the edge')
        values=label('Contrast: input 0.33 · plateaus 0.33 · edge 0.56',0,.0,BLUE,28)
        self.play(FadeIn(values),run_time=.35)
        self.remove(r[4]); self.add(
            label('Plateau contrast unchanged; edge contrast rises to 0.56',0,-3.18,TEXT,24),
            label('Made-up units · feedforward toy model · row continues',0,-3.66,GREY,22))
        self.wait(4.1); self.finish()


def recurrent_chart():
    n=100; stimulus=np.r_[np.full(n//2,10.),np.full(n//2,20.)]
    A=np.eye(n)+.2*np.eye(n,k=1)+.2*np.eye(n,k=-1)
    stimulus[0]-=.2*10/1.4; stimulus[-1]-=.2*20/1.4
    values=np.linalg.solve(A,stimulus)[47:53]
    xs=np.linspace(-3.85,1.25,6); base=-2.55; scale=.23
    g=VGroup(Line([-4.4,base,0],[1.8,base,0],color=GREY),label('0',-4.65,base,GREY,26))
    for x,v in zip(xs,values):
        g.add(Rectangle(width=.85,height=v*scale,stroke_width=0,fill_color=GREEN,fill_opacity=.85)
              .move_to([x,base+v*scale/2,0]),label(f'{v:.1f}',x,base+v*scale+.25,GREEN,30))
    for v,x in [(10/1.4,-4.2),(20/1.4,-.5)]:
        y=base+v*scale
        g.add(DashedLine([-4.4,y,0],[1.8,y,0],color=BLUE,stroke_opacity=.5),
              label(f'plateau\nabout {v:.1f}',-5.45,y,BLUE,26))
    g.add(label('response (made-up units)',-2.1,2.7,GREEN,28),
          label('Bar values are approximate',-2.1,-3.65,GREY,26),label('edge contrast ≈ 0.51',-2.3,-3.15,BLUE,30))
    links=VGroup()
    for i in range(5):
        x,y=xs[i],xs[i+1]
        links.add(CurvedArrow([x+.08,1.9,0],[y-.08,1.9,0],angle=-.5,color=RED,stroke_width=3,tip_length=.13),
                  CurvedArrow([y-.08,2.2,0],[x+.08,2.2,0],angle=-.5,color=RED,stroke_width=3,tip_length=.13))
        # Leaders tie the network nodes to the corresponding computed outputs.
    for x,v in zip(xs,values):
        links.add(Dot([x,1.9,0],color=GREEN,radius=.04),
                  Line([x,base+v*scale+.55,0],[x,1.8,0],color=GREY,stroke_width=1))
    return g,links


def retina():
    box=RoundedRectangle(width=4.15,height=4.4,corner_radius=.15,color=GREY).move_to([4.25,-.25,0])
    cells=VGroup(*[Circle(.19,color=YELLOW).move_to([x,.9,0]) for x in [3,4.2,5.4]])
    horizontal=Rectangle(width=2.9,height=.25,color=RED,fill_color=RED,fill_opacity=.3).move_to([4.2,0,0])
    outputcell=Circle(.23,color=GREEN).move_to([4.2,-1.15,0])
    return VGroup(box,label('vertebrate retina',4.25,1.5,size=27),cells,horizontal,outputcell,
        *[Line([x,.71,0],[x,.14,0],color=GREY) for x in [3,4.2,5.4]],
        Line([4.2,-.13,0],[5.95,-.13,0],color=RED),
        Line([5.95,-.13,0],[5.95,-1.15,0],color=RED),
        inhib([5.95,-1.15,0],[4.48,-1.15,0]),
        label('receptors',4.25,2.1,YELLOW,26),VMobject(color=YELLOW).set_points_as_corners([[5.25,2.1,0],[6.05,2.1,0],[6.05,.9,0],[5.6,.9,0]]),
        label('horizontal cell',4.25,-.45,RED,26),label('output cell',4.25,-1.7,GREEN,26),
        label('builds the surround',4.25,-2.85,RED,26))


class S16Caveat(SpokenScene):
    def construct(self):
        chart,links=recurrent_chart(); self.add(chart,label('Recurrent model · thresholds omitted',0,3.4,size=30))
        self.at('The full model'); self.play(FadeIn(label('uses neighbours’ outputs',4.25,3.4,RED,26).shift(DOWN*.6)),run_time=.35)
        self.at("each neighbor's output"); self.play(Create(links),run_time=.6)
        self.at('the result still holds'); self.play(Indicate(chart[6:10],color=BLUE),run_time=.5)
        self.at('In the vertebrate retina'); self.play(FadeIn(retina()),run_time=.5)
        self.finish()


class S17Takeaway(SpokenScene):
    def construct(self):
        r=row(2)
        r[6].shift(UP*.5); r[1][1:].shift(UP*.5)
        r[2][1].move_to([0,-.05,0])
        self.add(r); self.remove(r[3],r[4])
        self.add(label('Made-up units · feedforward toy model · row continues',0,-3.7,GREY,22))
        self.at('Lateral inhibition'); self.play(FadeIn(label('Lateral inhibition',4.6,3.35,RED,26)),run_time=.35)
        self.at('discounts uniform regions'); self.play(*[r[6][i].animate.set_opacity(.5) for i in [0,1,4,5]],run_time=.5)
        self.at('differences stand out')
        glow=SurroundingRectangle(VGroup(r[6][2][0],r[6][3][0]),color=BLUE,buff=.1,stroke_width=7)
        self.play(Create(glow),FadeIn(label('Uniform regions discounted; differences stand out.',0,-3.0,size=30)),run_time=.5)
        self.remove(r[2][1]); self.add(label('Edge pair: step kept, plateaus pulled together',0,-.05,BLUE,28))
        self.at('Neighbors compare'); self.play(glow.animate.set_stroke(width=4),run_time=.4)
        self.finish()


class S18End(EndCard):
    LINE='Lateral inhibition discounts uniform regions,\nso differences stand out.'
    def construct(self):
        line=VGroup(*[T(part,size=40,font=TITLE_FONT) for part in self.LINE.split('\n')]).arrange(DOWN,buff=.3)
        line.move_to([0,.35,0]); self.add(line,label('biochemistrypedia.com',0,-1.25,TEAL,28))
        self.wait(3.5)
