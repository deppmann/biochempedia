"""Prisms: Learning You Can Watch.
COLOR MAP: BLUE=prism/visual context; ORANGE=error/teacher;
GREEN=Purkinje cell; TEAL=deep nuclei/output; RED=damage;
YELLOW=movement/target/healthy learned correction; GREY=structure;
LILAC=slow adaptation (toy model k=.05, never patient data).
All adaptation traces and landings derive from E(n)=20*(1-k)**n.
The schematic reach reuses the reference reach_path equations.
"""
import numpy as np
from bp_style import *

ORANGE='#F29E4C'
LILAC='#D3ACFF'
CTX,ERR,PUR,NUC,WEAK,MOVE=BLUE,ORANGE,GREEN,TEAL,RED,YELLOW
E0,K=20.,.30

def P(x,y): return np.array([x,y,0.])
def errv(n,k=K): return E0*(1-k)**n

def poly(pts,color=MOVE,w=4):
    return VMobject(stroke_color=color,stroke_width=w).set_points_as_corners([P(*p) for p in pts])

def label(s,x,y,size=28,color=TEXT): return T(s,size,color).move_to(P(x,y))

def target(x=0,y=0,r=2.6):
    return VGroup(*[Circle(radius=r*f,color=MOVE,stroke_width=3).move_to(P(x,y)) for f in (1,.55,.12)],
      Line(P(x-r-.2,y),P(x+r+.2,y),color=GREY,stroke_opacity=.55),
      Line(P(x,y-r-.2),P(x,y+r+.2),color=GREY,stroke_opacity=.55))

def board():
    return VGroup(target(),Line(P(-5.1,0),P(5.1,0),color=GREY,stroke_opacity=.35),
      label('thrower’s left',-4.6,-2.6),label('thrower’s right',4.6,-2.6))

def landing(error): return P(error*.23,0)

def goggles():
    a=RoundedRectangle(width=.65,height=.42,corner_radius=.08,color=BLUE,fill_color=BLUE,fill_opacity=.25)
    b=a.copy().shift(RIGHT*.78)
    return VGroup(a,b,Line(P(.325,0),P(.455,0),color=BLUE)).move_to(P(-4.8,1.35))

def thrower():
    return VGroup(Circle(radius=.48,color=TEXT).move_to(P(-4.8,1.35)),
       poly([(-4.8,.87),(-4.8,-.65),(-5.45,-2)],TEXT),Line(P(-4.8,-.65),P(-4.05,-2),color=TEXT),
       poly([(-4.8,.35),(-3.9,.05),(-3.25,.6)],MOVE))

def off_question():
    return VGroup(target(2.4,-.15,2.4),thrower(),
      label('Goggles off. Where does it land?',0,3.15,34),
      label('Left of, on, or right of the bullseye?',0,-3.1,30))

def make_plot(x=2.7,y=.05,w=5.8,h=4.9,color=ERR):
    ax=Axes(x_range=[0,7,1],y_range=[0,20,5],x_length=w,y_length=h,tips=False,
      axis_config={'color':GREY,'include_numbers':False}).move_to(P(x,y))
    ls=VGroup(*[M(str(n),28,TEXT).next_to(ax.c2p(n,0),DOWN,buff=.12) for n in range(8)],
      *[M(str(n),28,TEXT).next_to(ax.c2p(0,n),LEFT,buff=.12) for n in (5,10,15,20)],
      label('error (cm right)',x,3.15,30,ERR),label('corrections / throws',x,-3.0,28),
      label('toy model, not patient data',0,-3.55,28))
    c=ax.plot(lambda n:errv(n),x_range=[0,7,.03],color=color,stroke_width=5,use_smoothing=False)
    return ax,ls,c

def paired_board():
    return VGroup(target(-3.8,0,2.5),label('target board',-3.8,3.15,30))

def paired_dot(n): return Dot(P(-3.8+errv(n)*.13,0),color=ERR,radius=.13)

def bodymap(damage=True,highlight=False):
    # Front view; brain inset is ABOVE the face, not goggles.
    rightarm=poly([(-.9,-.3),(-1.65,-.8),(-1.9,-2.1)],TEXT,5)
    leftarm=poly([(.9,-.3),(1.65,-.8),(1.9,-2.1)],MOVE if highlight else TEXT,8 if highlight else 5)
    body=VGroup(Circle(radius=.52,color=TEXT).move_to(P(0,.55)),
      RoundedRectangle(width=1.8,height=1.6,corner_radius=.25,color=TEXT).move_to(P(0,-.95)),rightarm,leftarm,
      Line(P(-.45,-1.75),P(-.65,-2.8),color=TEXT),Line(P(.45,-1.75),P(.65,-2.8),color=TEXT))
    brain=VGroup(Ellipse(width=3,height=1.45,color=GREY).move_to(P(0,2.45)),
      Ellipse(width=1.05,height=.6,color=GREY,fill_color=GREY,fill_opacity=.15).move_to(P(-.58,1.95)),
      Ellipse(width=1.05,height=.6,color=WEAK if damage else GREY,fill_color=WEAK,fill_opacity=.6 if damage else 0).move_to(P(.58,1.95)),
      label('brain, seen from behind',0,3.5,28),
      DashedLine(P(0,1.2),P(0,1.55),color=GREY))
    sides=VGroup(label('patient’s right arm',-4.05,-1.1,28),label('patient’s left arm',4.05,-1.1,28,MOVE if highlight else TEXT),
      Line(P(-2.6,-1.35),P(-1.8,-1.65),color=GREY),Line(P(2.6,-1.35),P(1.8,-1.65),color=MOVE if highlight else GREY))
    return VGroup(body,brain,sides)

def lesion_note():
    return VGroup(label('left cerebellar\nhemisphere lesion',4.3,2.2,28,WEAK),Line(P(2.45,1.95),P(1.15,1.95),color=WEAK))

def side_question(): return VGroup(bodymap(),lesion_note(),label('Which arm?',0,-3.45,38))

def route_base():
    mid=DashedLine(P(0,-3.35),P(0,3.2),color=GREY,stroke_opacity=.3)
    cb=chip('left cerebellum',WEAK,28).move_to(P(4.1,-.15))
    th=chip('right thalamus',NUC,28).move_to(P(-3.8,1.25))
    cx=chip('right motor cortex',NUC,28).move_to(P(-3.8,2.6))
    arm=chip('left arm',MOVE,28).move_to(P(4.0,-3.05))
    sides=VGroup(label('patient’s right',-3.8,3.4,28),label('patient’s left',3.8,3.4,28))
    # A continuous brainstem leads into one cord; screen-right is patient-left.
    stem=RoundedRectangle(width=3.2,height=3.3,corner_radius=.18,color=GREY).move_to(P(0,-.05))
    medulla=Rectangle(width=3.2,height=1.3,color=GREY).move_to(P(0,-1.05))
    cord=VGroup(stem,medulla,
      Rectangle(width=1.9,height=1.6,color=GREY).move_to(P(0,-2.5)),
      label('brainstem',0,1.98,28),
      label('spinal cord, left side',3.7,-2.05,26),
      Line(P(1.05,-2.25),P(2.05,-2.05),color=GREY))
    return mid,cb,th,cx,arm,sides,cord

def first_cross():
    return VGroup(poly([(2.55,-.15),(1.2,-.15),(1.2,.65),(-1.2,.65),(-2.1,.65),(-2.1,1.25)],NUC,5),
      Arrow(P(-2.1,1.25),P(-2.45,1.25),buff=0,color=NUC,stroke_width=5))

def crossing1():
    return label('crossing 1:\nmidbrain',0,1.15,26,NUC)

def relay(): return Arrow(P(-3.8,1.64),P(-3.8,2.2),buff=0,color=NUC)

class S00Title(TitleCard):
    TITLE='Prisms: Learning You Can Watch'
    LESSON='The Cerebellum'
    def construct(self):
        self.add(label('THE CEREBELLUM',0,1.7,32,TEAL))
        title=T(self.TITLE,46,font=TITLE_FONT);fit(title,max_w=12);title.move_to(P(0,.15))
        self.play(FadeIn(title),Create(Line(P(-1.5,-1),P(1.5,-1),color=GOLD)),run_time=.8)
        self.finish()

class S01(SpokenScene):
    def construct(self):
        person=thrower();g=goggles().set_opacity(.35)
        self.add(person,g,target(3,0,2.5))
        self.at('Can you watch')
        self.play(FadeIn(label('Can you watch the cerebellum learn?',0,3.2,34)),run_time=.4)
        self.at('Put on prism goggles')
        self.play(g.animate.set_opacity(1),run_time=.45)
        self.at('and throw')
        ball=Dot(P(-3.25,.6),color=MOVE,radius=.13)
        self.add(ball);self.play(ball.animate.move_to(P(-.4,.3)),run_time=.55)
        self.finish()

class S02(SpokenScene):
    def construct(self):
        # Retain the thrower as a small inset outside the target's footprint.
        person=VGroup(thrower(),goggles()).scale(.5).move_to(P(-5.4,1.6))
        self.add(board(),person)
        seen=target(0,0,1.4).set_color(BLUE).set_stroke(opacity=.65)
        self.at('The goggles shift')
        self.add(seen);self.play(seen.animate.shift(RIGHT*4.6),run_time=1.15)
        self.play(FadeIn(label('view through prisms',4.25,2.5,28,BLUE)),run_time=.35)
        self.at('the first throws')
        self.play(seen.animate.set_stroke(opacity=.3),run_time=.2)
        dot=Dot(P(-2.9,.15),color=ERR,radius=.16);self.add(dot)
        self.play(dot.animate.move_to(landing(E0)),run_time=.55)
        self.at('miss to the right')
        self.play(Create(DashedLine(P(.15,-.2),P(4.45,-.2),color=BLUE,stroke_opacity=.3)),
          FadeIn(label('first miss: 20 cm right',3.9,-1.95,28,ERR)),
          GrowArrow(Arrow(P(4.6,1.05),P(4.6,.22),color=BLUE,buff=0)),run_time=.35)
        self.finish()

class S03(SpokenScene):
    def construct(self):
        ax,ls,c=make_plot();d=paired_dot(0).set_color(MOVE)
        self.add(paired_board(),d,ax,ls)
        self.at('Each miss teaches')
        p0=Dot(ax.c2p(0,20),color=ERR,radius=.09)
        self.play(FadeIn(p0),run_time=.25)
        self.at('Throw by throw')
        # Each trace segment and pair of dots uses the same recurrence.
        previous=p0
        for n in range(1,8):
            if n==4: self.at('the misses walk')
            segment=ax.plot(lambda t:errv(t),x_range=[n-1,n,.03],color=ERR,stroke_width=5,use_smoothing=False)
            ghost=d.copy().set_color(ERR).set_opacity(.16);self.add(ghost)
            marker=Dot(ax.c2p(n,errv(n)),color=MOVE,radius=.1)
            self.play(d.animate.move_to(paired_dot(n).get_center()),Create(segment),
              FadeIn(marker),previous.animate.set_color(ERR),run_time=.32,rate_func=linear)
            previous=marker
        self.play(Indicate(d,color=MOVE),run_time=.35)
        self.finish()

class S04(SpokenScene):
    def construct(self):
        ax,ls,c=make_plot();self.add(paired_board(),ax,ls,c,
          *[Dot(ax.c2p(n,errv(n)),color=ERR,radius=.09) for n in range(8)])
        self.at('How much each error')
        a,b=ax.c2p(1,errv(1)),ax.c2p(2,errv(2))
        step=VGroup(Line(a,P(a[0],b[1]),color=MOVE,stroke_width=7),Line(P(a[0],b[1]),b,color=MOVE,stroke_width=4))
        boarddots=VGroup(paired_dot(1).set_color(MOVE),paired_dot(2).set_color(MOVE))
        self.play(Create(step),FadeIn(boarddots),
          FadeIn(label('1',-3.8+errv(1)*.13,.5,28,MOVE)),
          FadeIn(label('2',-3.8+errv(2)*.13,-.5,28,MOVE)),run_time=.5)
        self.at('Call it')
        note=label('k = 0.30',3.9,1.9,30,MOVE)
        self.play(FadeIn(note),Create(Line(P(2.65,1.8),P(a[0]+.08,(a[1]+b[1])/2),color=MOVE)),run_time=.3)
        self.at('the fraction of')
        self.play(FadeIn(label('30% of what is left\n14 → 9.8 cm',3.9,.75,28,MOVE)),run_time=.4)
        self.finish()

class S05(SpokenScene):
    def construct(self):
        self.add(off_question());g=goggles();self.add(g)
        self.at('Now take the goggles')
        self.play(g.animate.shift(UP*1.25),run_time=.7)
        self.play(FadeOut(g),run_time=.35)
        self.at('Where does the next')
        self.play(Indicate(self.mobjects[0][-1],color=MOVE),run_time=.5)
        self.finish()

class S06Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(off_question());self.wait(5)

class S07(SpokenScene):
    def construct(self):
        self.add(board(),label('Goggles off',0,3.2,34))
        ghost=Dot(landing(20),color=ERR,radius=.16).set_opacity(.3)
        self.add(ghost,label('first prism miss',4.45,.65,28,ERR))
        self.at('To the left')
        d=Dot(P(-1,0),color=MOVE,radius=.17);self.add(d)
        self.play(d.animate.move_to(landing(-(E0-errv(7)))),run_time=.55)
        self.at('The learned correction')
        self.play(GrowArrow(Arrow(P(0,0),d.get_center(),color=MOVE,buff=0,stroke_width=6)),run_time=.5)
        self.at('to a world')
        x=d.get_x();br=VGroup(Line(P(x,-2.9),P(0,-2.9),color=MOVE),Line(P(x,-2.85),P(x,-3.05),color=MOVE),Line(P(0,-2.85),P(0,-3.05),color=MOVE))
        self.play(Create(br),FadeIn(label('correction learned: about 18 cm left',-.9,-3.45,28,MOVE)),run_time=.5)
        self.at('That opposite miss')
        self.play(FadeIn(label('after-effect',-4.3,.8,32,MOVE)),run_time=.35)
        self.finish()

class S08(SpokenScene):
    def construct(self):
        eye=VGroup(Ellipse(width=2.6,height=1.3,color=BLUE),Circle(radius=.42,color=BLUE)).move_to(P(-4,.5))
        # Continuous forearm/palm/thumb/finger outline, no bin-like glyph.
        hand=poly([(3.2,-1.8),(3.2,-.2),(2.75,.35),(2.8,.65),(3.1,.65),(3.5,.25),
          (3.5,1.6),(3.75,1.75),(3.95,1.6),(3.95,.65),(4.1,1.8),(4.35,1.85),(4.5,1.6),
          (4.45,.6),(4.65,1.45),(4.9,1.5),(5.05,1.25),(4.9,.35),(5.1,.85),
          (5.35,.85),(5.4,.55),(4.9,-.65),(4.7,-1.8)],MOVE,5)
        link=Arrow(P(-2.4,.5),P(2.55,.5),buff=0,color=GREY,stroke_width=5)
        self.add(eye,hand,link,label('Includes shifts in where you see\nand feel your arm',0,-2.9,30),
          label('eye',-4,-.75,30,BLUE),label('hand',4.25,-2.15,30,MOVE))
        self.at('the mapping between')
        self.play(FadeIn(label('seeing',-4,1.85,32,BLUE)),FadeIn(label('moving',4.25,2.5,32,MOVE)),run_time=.4)
        self.at('was recalibrated')
        self.play(Transform(link,Arrow(P(-2.4,.5),P(2.55,1),buff=0,color=MOVE,stroke_width=6)),
          FadeIn(label('mapping recalibrated',0,3.3,34,MOVE)),run_time=.5)
        self.finish()

class S09(SpokenScene):
    def construct(self):
        full=landing(-(E0-errv(7)));ghost=Dot(full,color=MOVE,radius=.17).set_opacity(.3)
        d=Dot(full,color=MOVE,radius=.17)
        heading=label('Goggles off: after-effect',0,3.2,34)
        self.add(board(),ghost,d,heading,
          label('model after-effect',-4.4,.85,28,MOVE))
        self.at('Real after effects')
        self.at('are usually smaller')
        self.play(d.animate.shift(RIGHT*1.55),run_time=.7)
        self.play(FadeIn(label('smaller in real throwers',0,-3.35,30,MOVE)),run_time=.35)
        self.at('drop a deliberate')
        self.play(Transform(heading,label('Partly: deliberate aiming strategy is dropped',0,3.2,30)),run_time=.4)
        self.finish()

class S10(SpokenScene):
    def construct(self):
        self.add(RoundedRectangle(width=12.2,height=6.6,corner_radius=.2,color=GREY),
          label('Martin and colleagues, 1996',0,2.7,32),target(-3.7,-.65,1.65),
          label('prism throwing task',-3.7,-2.75,28))
        self.at('In people with damage')
        self.play(FadeIn(label('People with damage to the\nolivocerebellar system',2,-.1,32,WEAK)),run_time=.5)
        self.at('adaptation at this task')
        self.play(FadeIn(label('Prism adaptation\nimpaired',2,-1.75,34,ERR)),run_time=.5)
        self.finish()

class S11(SpokenScene):
    def construct(self):
        ax,ls,c=make_plot(x=-1.7,w=8.1,h=4.9,color=MOVE)
        self.add(ax,ls,c)
        healthy=label('healthy, k = 0.30',4.1,-1.75,28,MOVE)
        slowlabel=label('slow, k = 0.05\n(toy model)',4.4,1.65,28,LILAC)
        healthy.next_to(ax.c2p(7,errv(7)),RIGHT,buff=.3)
        self.add(healthy)
        self.at('a smaller')
        small=ax.plot(lambda n:errv(n,.05),x_range=[0,7,.03],color=LILAC,stroke_width=5,use_smoothing=False)
        slowlabel.next_to(ax.c2p(7,errv(7,.05)),RIGHT,buff=.3)
        self.play(Create(small),FadeIn(slowlabel),run_time=.9)
        self.at('The curve flattens')
        self.play(small.animate.set_stroke(width=7),run_time=.45)
        self.at('after the same number')
        # Replace full plot with a readable compact plot; keep cause beside result.
        self.play(FadeOut(Group(*self.mobjects)),run_time=.25)
        mini=Axes(x_range=[0,7,7],y_range=[0,20,10],x_length=3.7,y_length=3.6,tips=False,
          axis_config={'color':GREY}).move_to(P(-4.1,.5))
        curves=VGroup(*[mini.plot(lambda n,k=k:errv(n,k),x_range=[0,7,.03],color=col,stroke_width=4,use_smoothing=False) for k,col in ((K,MOVE),(.05,LILAC))])
        self.add(mini,curves,label('error (cm)',-4.2,3.2,28),label('0',-6,-1.65,28),label('7 throws',-2.4,-1.65,28),
          label('20',-6.5,2.3,28),label('0',-6.5,-1.25,28),
          label('healthy, k = 0.30',-4,-2.35,28,MOVE),label('slow, k = 0.05\n(toy model)',-4,-3.15,28,LILAC),
          label('healthy',-1.3,float(mini.c2p(7,errv(7))[1]),28,MOVE),
          label('slow',-1.5,float(mini.c2p(7,errv(7,.05))[1]),28,LILAC),
          target(3.3,.25,2.1),label('Goggles off after 7 corrections',2.65,3.2,28))
        fastpos=P(3.3-(E0-errv(7))*.18,.25);slowpos=P(3.3-(E0-errv(7,.05))*.18,.25)
        fast=Dot(fastpos,color=MOVE,radius=.15);slow=Dot(slowpos,color=LILAC,radius=.15)
        self.add(fast,label('healthy, k = 0.30\n18.4 cm left',.1,2.15,28,MOVE),Line(fastpos+UP*.2,P(.1,1.5),color=MOVE),
          label('off the board',.05,-.55,26,MOVE),
          Arrow(P(.05,-.3),fastpos+DOWN*.18,buff=0,color=MOVE,stroke_width=3))
        self.at('the after effect')
        self.play(FadeIn(slow),FadeIn(label('slow, k = 0.05\n6.0 cm left (toy model)',3.2,-2.45,28,LILAC)),
          Create(Line(slowpos+DOWN*.2,P(2.45,-1.95),color=LILAC)),run_time=.5)
        self.at('The model does not')
        self.play(FadeIn(label('Toy model: does not locate damage',2.45,-3.5,28)),run_time=.4)
        self.finish()

class S12(SpokenScene):
    def construct(self):
        # Reference reach equations, placed inside the safe frame.
        # Its overshoot is 25% of the reach, followed by three lateral swings.
        start,end=P(-5,-2.4),P(2.7,.3);d=end-start;L=np.linalg.norm(d);u=d/L;nrm=P(-u[1],u[0]);pts=[]
        for t in np.linspace(0,1,240):
            if t<.55:
                q=t/.55;along=1.25*(3*q*q-2*q*q*q);lat=.45*np.sin(np.pi*q)
            else:
                q=(t-.55)/.45;along=1.25-.25*q;lat=.65*np.sin(2*np.pi*3*q)*(1-q)
            pts.append(start+u*L*along+nrm*lat)
        path=VMobject(color=MOVE,stroke_width=5).set_points_as_corners(pts)
        hand=Dot(start,color=MOVE,radius=.17)
        cb=VGroup(Ellipse(width=.8,height=.55,color=WEAK),Ellipse(width=.8,height=.55,color=WEAK).shift(RIGHT*.65)).move_to(P(-5.1,2))
        self.add(target(2.7,.3,1.35),hand,label('target',4.95,-1.05,30,MOVE),
          label('one proposed contributor',0,3.35,32),label('schematic reach, seen from above',0,-3.35,28))
        self.at('lose the cerebellum\'s')
        self.play(FadeIn(cb),FadeIn(label('cerebellum:\nprediction lost',-2.8,2,28,WEAK)),run_time=.4)
        self.at('the arm leans')
        delay=VGroup(Line(P(-.9,-1.7),P(.9,-1.7),color=BLUE),Line(P(-.9,-1.55),P(-.9,-1.85),color=BLUE),
          Line(P(.9,-1.55),P(.9,-1.85),color=BLUE),label('visual correction:\nabout 0.1 s late or more',.1,-2.5,28,BLUE),
          DashedLine(P(0,-1.7),P(.3,-.8),color=BLUE))
        self.play(FadeIn(delay),run_time=.45)
        # A single moving dot and growing trace share the exact same path.
        # MoveAlongPath avoids stale updater positions at the final hold.
        trail=TracedPath(hand.get_center,stroke_color=MOVE,stroke_width=5)
        self.add(trail);self.bring_to_front(hand)
        self.at('Movements can overshoot')
        self.play(MoveAlongPath(hand,path),run_time=3.0,rate_func=linear)
        hand.move_to(end)
        trail.clear_updaters()
        self.finish()

class S13(SpokenScene):
    def construct(self):
        b=bodymap(False);self.add(b)
        self.at('A patient has a lesion')
        self.play(Transform(b,bodymap()),FadeIn(lesion_note()),run_time=.5)
        self.at('Which arm is')
        self.play(FadeIn(label('Which arm?',0,-3.45,38)),run_time=.4)
        self.finish()

class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(side_question());self.wait(5)

class S15(SpokenScene):
    def construct(self):
        b=side_question();self.add(b)
        self.at('The left arm')
        self.play(Transform(b[0],bodymap(highlight=True)),Transform(b[2],label('The left arm',0,-3.45,38,MOVE)),run_time=.5)
        self.at('Cerebellar output crosses')
        self.play(FadeOut(b),run_time=.2)
        mid,cb,th,cx,arm,sides,cord=route_base();self.add(mid,cb,sides,cord)
        self.play(Create(first_cross()),FadeIn(th),FadeIn(crossing1()),run_time=.8)
        self.at('which relays to')
        self.play(GrowArrow(relay()),FadeIn(cx),run_time=.6)
        self.finish()

class S16(SpokenScene):
    def construct(self):
        mid,cb,th,cx,arm,sides,cord=route_base()
        self.add(mid,cb,th,cx,sides,cord,first_cross(),relay(),crossing1())
        self.at('the corticospinal tract')
        # Route around the relay to keep the two distinct tracts apart.
        down=poly([(-5.61,2.6),(-5.85,2.6),(-5.85,-.35),(-1.45,-.35),(-1.45,-1.15)],MOVE,6)
        self.play(Create(down),run_time=.7)
        self.at('crosses back')
        cross=VGroup(poly([(-1.45,-1.15),(1.25,-1.5),(.65,-1.8),(.65,-3.05)],MOVE,6),
          Arrow(P(.65,-3.05),P(3.0,-3.05),buff=0,color=MOVE,stroke_width=6))
        self.play(Create(cross),FadeIn(arm),
          FadeIn(label('crossing 2:\ncaudal medulla',0,-.75,26,MOVE)),run_time=.8)
        self.at('Two crossings cancel')
        self.play(Indicate(arm,color=MOVE),FadeIn(label('same side',4.4,-2.45,26,MOVE)),run_time=.5)
        self.finish()

class S17(SpokenScene):
    def construct(self):
        self.add(label('The cerebellum',0,3,38),label('Helps learn predictions from error',0,1.65,32,MOVE))
        self.at('The takeaway')
        self.at('Damage can leave')
        self.play(FadeIn(label('Damage can mean more reliance\non late feedback',0,.05,32)),run_time=.5)
        self.at('one cause of clumsiness')
        self.play(FadeIn(label('One contributor to limb clumsiness',0,-1.55,32)),run_time=.4)
        self.at('on the same side')
        self.play(FadeIn(label('Same side: pathways cross twice',0,-3,32,MOVE)),run_time=.4)
        self.finish()

class S18End(EndCard):
    LINE='The cerebellum helps learn predictions from error.'
