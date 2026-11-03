"""Chapter 1, review fix round.
COLOR MAP: YELLOW light / clock / pupil; BLUE rod-cone relay;
GREEN ipRGC; GOLD melanopsin membrane badges; PURPLE brain / nuclei;
GREY ordinary cells / unavailable photoreceptors; TEXT labels / neutral output.
Actograms are generated schematic event records, not experimental data.
The checklist's trace icon is calculated from a first-order schematic response.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'


def label(text, x=0, y=3.05, size=30, color=TEXT):
    return T(text, size, color).move_to([x, y, 0])


def arr(a, b, color=GREY, w=5, tip=.2):
    return Arrow(a, b, buff=.04, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=.4)


def cell(x, y, w=.5, h=.5, color=GREY, fill=.18):
    return Ellipse(width=w, height=h, color=color, stroke_width=3,
                   fill_color=color, fill_opacity=fill).move_to([x,y,0])


def clock_icon(x, y, r=.7):
    c=np.array([x,y,0.])
    h=Line(c,c+[r*.6,r*.25,0],color=YELLOW,stroke_width=5)
    g=VGroup(Circle(radius=r,color=YELLOW,stroke_width=4).move_to(c),
             Line(c,c+[0,r*.7,0],color=YELLOW,stroke_width=4),h)
    g.h2=h; g.c=c
    return g


def eye_icon(x,y,w=2):
    e=Ellipse(width=w,height=w*.58,color=YELLOW,stroke_width=4).move_to([x,y,0])
    iris=Circle(radius=w*.23,color=GREY,fill_color=GREY,fill_opacity=.8).move_to([x,y,0])
    p=Circle(radius=w*.14,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([x,y,0])
    g=VGroup(e,iris,p); g.pup=p
    return g


def mouse(x,y,s=1):
    body=Ellipse(width=2.4,height=1.25,fill_color=GREY,fill_opacity=1,stroke_color=GREY)
    head=Circle(radius=.5,color=GREY,fill_opacity=1).move_to([1,.3,0])
    ear=Circle(radius=.28,color=GREY,fill_opacity=1).move_to([.8,.8,0])
    nose=Dot([1.5,.25,0],radius=.07,color=TEXT)
    tail=ArcBetweenPoints([-1.1,0,0],[-2,.6,0],angle=-PI/2,color=GREY,stroke_width=5)
    feet=VGroup(Line([-.7,-.5,0],[-1,-.85,0],color=TEXT,stroke_width=4),
                Line([.6,-.45,0],[1,-.75,0],color=TEXT,stroke_width=4))
    return VGroup(body,head,ear,nose,tail,feet).scale(s).move_to([x,y,0])


def retina(missing=False, many=False):
    # Light travels DOWN through ganglion and bipolar layers to the outer retina.
    xs=np.linspace(-4.8,.8,12)
    rods=VGroup()
    for i,x in enumerate(xs):
        col=GREY if missing else BLUE
        rod=(RoundedRectangle(width=.24,height=.85,corner_radius=.08,color=col,fill_opacity=.18)
             if i%2==0 else Triangle(color=col,fill_opacity=.18).stretch_to_fit_width(.32).stretch_to_fit_height(.85))
        rods.add(rod.move_to([x,-1.9,0]))
    bip=VGroup(*[VGroup(Line([x,-1.45,0],[x,1.4,0],color=BLUE,stroke_opacity=.55),
                       cell(x,0,.42,.6,BLUE,fill=.9)) for x in np.linspace(-4.5,.5,6)])
    gx=np.linspace(-5,1,24 if many else 10)
    gang=VGroup(*[cell(x,1.8,.22 if many else .48,.43 if many else .58) for x in gx])
    labs=VGroup(label('ganglion cells',3.6,1.8,30),label('bipolar cells',3.6,0,30,BLUE),
                label('rods and cones',3.6,-1.9,30,GREY if missing else BLUE))
    leaders=VGroup(*[Line([1.3,y,0],[2,y,0],color=GREY) for y in [1.8,0,-1.9]])
    return rods,bip,gang,VGroup(labs,leaders)


def rays():
    return VGroup(*[arr([x,3,0],[x,-2.5,0],YELLOW,w=2,tip=.13).set_opacity(.5)
                    for x in [-4.65,-2.25,.15]])


def brain_map():
    # One shared sagittal schematic. Brainstem continues the silhouette, without
    # a superimposed rectangle. Nuclei are teaching landmarks, not atlas geometry.
    pts=[[-4.9,-.5,0],[-5,1,0],[-4.2,2.2,0],[-2.7,2.65,0],[-1.2,2.4,0],
         [-.1,1.65,0],[.5,.8,0],[.25,-.1,0],[.8,-1.5,0],[.45,-2.25,0],
         [-.3,-2.1,0],[-.85,-.9,0],[-2,-.6,0],[-3.6,-.9,0],[-4.9,-.5,0]]
    outline=VMobject(color=PURPLE,stroke_width=4,fill_color=PURPLE,fill_opacity=.1)
    outline.set_points_smoothly(pts)
    folds=VGroup(*[ArcBetweenPoints([x,1.9,0],[x+.55,.7,0],angle=.8,color=PURPLE,stroke_opacity=.4)
                    for x in [-4.1,-3,-1.9]])
    labs=VGroup(label('brain',-3,2.95,30,PURPLE),label('brainstem',1.9,-1.85,28,PURPLE),
                Line([.5,-1.7,0],[.85,-1.85,0],color=PURPLE))
    return VGroup(outline,folds,labs)

SCN=np.array([-2.7,-.15,0]); OPN=np.array([-.45,.05,0])


def nucleus(p,paired=False):
    halo=Dot(p,radius=.52,color=PURPLE,fill_opacity=.15)
    dots=(VGroup(Dot(p+[-.17,0,0],radius=.16,color=PURPLE),Dot(p+[.17,0,0],radius=.16,color=PURPLE))
          if paired else Dot(p,radius=.23,color=PURPLE))
    return VGroup(halo,dots)


def scn_annotation():
    return VGroup(label('suprachiasmatic\nnucleus (SCN)',3.5,1.1,30,PURPLE),
                  Line(SCN+[.3,.1,0],[1.5,.9,0],color=PURPLE),
                  label('master clock',3.5,-.15,30,YELLOW))


def record(shift=False):
    # Events every .14 schematic time units after onset; six days, 24 h per row.
    x0=-4.7; span=9.6; onset=x0+span/2
    bar=VGroup(Rectangle(width=span/2,height=.35,color=TEXT,fill_opacity=.9).move_to([-2.3,2.15,0]),
               Rectangle(width=span/2,height=.35,color=GREY,fill_color=BLACK,fill_opacity=1).move_to([2.5,2.15,0]))
    labs=VGroup(label('lights on',-2.3,2.7,28),label('lights off',2.5,2.7,28),
                label('Day',-5.7,1.95,26),label('0 h',-4.7,1.65,26),
                label('12 h',.1,1.65,26),label('24 h',4.9,1.65,26),
                label('Schematic wheel record',0,-3.15,28,GREY))
    rows=VGroup()
    for i in range(6):
        y=1.1-i*.69
        delay=.95 if shift and i>=3 else 0
        ticks=VGroup(*[Line([onset+delay+j*.14,y-.18,0],[onset+delay+j*.14,y+.18,0],color=BLUE,stroke_width=3)
                      for j in range(24)])
        rows.add(VGroup(Line([x0,y,0],[4.9,y,0],color=GREY,stroke_opacity=.28),ticks,
                        label(str(i+1),-5.7,y,28)))
    return bar,labs,rows


def guide():
    return DashedLine([.1,1.4,0],[.1,-2.65,0],color=YELLOW,stroke_width=3)


def subdued(g):
    for m in g.family_members_with_points():
        m.set_stroke(opacity=.25)
        m.set_fill(opacity=m.get_fill_opacity()*.25)
    return g


def gauge(x=0,y=.5,s=1):
    box=RoundedRectangle(width=2,height=2.6,corner_radius=.15,color=YELLOW).move_to([x,y,0])
    bars=VGroup(*[Rectangle(width=1.35,height=.3,stroke_width=0,fill_color=YELLOW,fill_opacity=(i+1)/5)
                 .move_to([x,y-.85+i*.43,0]) for i in range(5)])
    return VGroup(box,bars).scale(s)


def ip_cell(extended=True):
    # Identical soma, dendrites and axon origin in s17, s18 and s22.
    soma=cell(0,-.7,3.6,4.2,GREEN,fill=.16)
    dendrites=VGroup()
    for sign in [-1,1]:
        dendrites.add(Line([sign*1.2,.9,0],[sign*2,1.6,0],color=GREEN,stroke_width=4),
                      Line([sign*2,1.6,0],[sign*2.7,1.45,0],color=GREEN,stroke_width=4),
                      Line([sign*2,1.6,0],[sign*2.3,2.05,0],color=GREEN,stroke_width=4))
    axon=(VGroup(arr([1.8,-.7,0],[5,-.7,0],GREEN,w=6),
                 label('to brain',3.8,-1.35,28,GREEN)) if extended else
          Line([1.8,-.7,0],[2.7,-.7,0],color=GREEN,stroke_width=6))
    return VGroup(dendrites,soma,axon,label('ipRGC',0,-.7,34,GREEN))


def input_parts():
    dots=VGroup(*[Dot([1.8*np.cos(a),-.7+2.1*np.sin(a),0],radius=.13,color=GOLD)
                  for a in np.linspace(2.5,4.2,5)])
    light=VGroup(arr([-5,-.35,0],[-1.85,-.35,0],YELLOW,w=7),label('light',-4.2,.25,30,YELLOW))
    pigment=VGroup(dots,label('melanopsin',-4,-2.15,30,GOLD),
                   Line([-2.55,-2.1,0],dots[-1].get_center(),color=GOLD,stroke_width=2))
    bp=VGroup(cell(0,2.55,.65,.85,BLUE,fill=.5),
              Line([0,3.4,0],[0,2.95,0],color=BLUE,stroke_width=4),
              arr([0,2.1,0],[0,1.4,0],BLUE,w=6),
              label('bipolar cell',2.5,2.75,30,BLUE),
              Line([.35,2.55,0],[1.1,2.7,0],color=BLUE),
              label('signal from\nrods and cones',-3.7,2.6,28,BLUE),
              Line([-2.15,2.3,0],[-.16,1.8,0],color=BLUE,stroke_width=2))
    return light,pigment,bp


def output_parts():
    br=chip('brain',PURPLE,34,fill_opacity=.25).move_to([5.1,-.7,0])
    out=Arrow([2.7,-.7,0],br.get_left(),buff=0,color=GREEN,stroke_width=7,tip_length=.2)
    return VGroup(out,br,label('one axon',3.2,-1.45,28,GREEN))


class S00Title(TitleCard):
    LESSON='Melanopsin Cells: Light for the Clock and the Pupil'
    TITLE='A Blind Mouse That Knows It Is Day'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.5,26,TEAL),
                 label('Melanopsin cells · Chapter 1',0,1.65,30,GREY),
                 VGroup(T('A Blind Mouse That',50),T('Knows It Is Day',50))
                 .arrange(DOWN,buff=.22).move_to(ORIGIN),
                 Line([-1.5,-1.55,0],[1.5,-1.55,0],color=GOLD,stroke_width=5))
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        # Side cutaway: the disabled photoreceptors line the back of the globe.
        globe=Circle(radius=2.35,color=YELLOW,stroke_width=4).move_to([2.8,0,0])
        lens=Ellipse(width=.45,height=1.6,color=TEXT,fill_color=TEXT,fill_opacity=.15).move_to([1.15,0,0])
        back=Arc(radius=2, start_angle=-PI/3, angle=2*PI/3,color=GREY,stroke_width=3).shift([2.8,0,0])
        rc=VGroup()
        for i,a in enumerate(np.linspace(-.95,.95,8)):
            pos=np.array([2.8+1.8*np.cos(a),1.8*np.sin(a),0])
            shape=(RoundedRectangle(width=.2,height=.5,corner_radius=.06,color=GREY)
                   if i%2==0 else Triangle(color=GREY).stretch_to_fit_width(.22).stretch_to_fit_height(.5))
            rc.add(shape.rotate(PI/2+a).move_to(pos))
        self.add(mouse(-3.8,0,1.4),globe,lens,back,rc,
                 label('retina',5.65,2.2,28,GREY),
                 Line([5.35,1.95,0],[4.45,1.15,0],color=GREY),
                 label('rods and cones: no function',2.8,-2.95,30),
                 Line([4.9,-1.05,0],[4.3,-2.65,0],color=GREY))
        self.at('Can it still'); self.play(FadeIn(label('Can it still tell day from night?',0,2.9,36,YELLOW)),run_time=.35)
        self.finish()


class S02Retina(SpokenScene):
    def construct(self):
        r,b,g,l=retina(); self.add(rays().set_stroke(width=5,opacity=.95),r,b,g)
        self.add(label('light',-5.65,2.8,28,YELLOW))
        self.add(label('Light passes through the inner layers first',0,3.35,28,YELLOW))
        self.at('rods and cones'); self.play(FadeIn(l[0][2]),Create(l[1][2]),run_time=.25)
        self.at('Bipolar cells'); self.play(FadeIn(l[0][1]),Create(l[1][1]),
            GrowArrow(arr([-3.5,-1.35,0],[-3.5,-.45,0],BLUE)),run_time=.3)
        self.at('to ganglion'); self.play(FadeIn(l[0][0]),Create(l[1][0]),
            GrowArrow(arr([-3.5,.4,0],[-3.5,1.35,0],BLUE)),run_time=.3)
        self.finish()


class S03Output(SpokenScene):
    def construct(self):
        # Carry the inverted retina on the left; output reaches a brain on the right.
        r,b,g,l=retina(); ret=VGroup(r,b,g).scale(.8).shift(LEFT*.8)
        self.add(ret,label('ganglion cells',-2.4,2.5,30),label('retina',-2.5,-2.4,30))
        br=brain_map()[:2].scale(.58).move_to([4.2,.4,0]); self.add(br,label('brain',4.2,-1.65,30,PURPLE))
        self.at('Ganglion cells'); self.play(g.animate.set_color(TEXT).set_fill(TEXT,.45),run_time=.35)
        junction=np.array([1.2,1.4,0])
        ax=VGroup(*[Line(c.get_top(),junction,color=TEXT,stroke_width=2) for c in g])
        self.at('Their axons'); self.play(Create(ax),FadeIn(label('optic nerve',1.8,2.4,30)),run_time=.5)
        self.at('to the brain'); self.play(GrowArrow(arr(junction,[2.55,.8,0],TEXT,w=7)),run_time=.35)
        self.finish()


class S04Mice(SpokenScene):
    def construct(self):
        self.add(label('Two papers · two mouse models',0,3.1,34,YELLOW))
        for x,name,model in [(-3.3,'Freedman et al.','rdta/cl mice'),(3.3,'Lucas et al.','rd/rd cl mice')]:
            r,b,g,l=retina(True)
            mini=VGroup(r,b,g).scale(.6).move_to([x,.2,0])
            panel=RoundedRectangle(width=5.9,height=5.6,corner_radius=.2,color=GREY).move_to([x,-.15,0])
            self.add(panel,mini,label('Science 1999',x,2.1,30),label(name,x,-1.75,30),label(model,x,-2.5,28))
        self.at('lack both'); self.play(FadeIn(label('rods and cones: no function',0,-3.35,30)),run_time=.3)
        self.finish()


class S05Wheel(SpokenScene):
    def construct(self):
        c=np.array([-.5,-.1,0]); r=2.65
        ring=Circle(radius=r,color=GREY,stroke_width=5).move_to(c)
        spokes=VGroup(*[Line(c,c+[r*np.cos(a),r*np.sin(a),0],color=GREY,stroke_opacity=.45)
                       for a in np.linspace(0,TAU,8,endpoint=False)])
        spokes.add(Dot(c+[r,0,0],radius=.1,color=BLUE))
        self.add(ring,spokes,mouse(-.4,-1.55,.7),label('Running-wheel turns',0,3.1,34,YELLOW))
        marker=Triangle(color=YELLOW,fill_opacity=1).scale(.15).rotate(PI/2).move_to([2.5,-.1,0])
        count=label('0',4.5,.1,48,BLUE)
        self.add(marker,count,label('turns',4.5,-.75,30,BLUE))
        self.at('Watch its')
        # A counter increments only when the marked wheel completes a turn.
        for i in range(1,3):
            self.play(Rotate(spokes,TAU,about_point=c),run_time=.45,rate_func=linear)
            self.play(Transform(count,label(str(i),4.5,.1,48,BLUE)),Flash(marker,color=YELLOW,flash_radius=.3),run_time=.15)
        self.finish()


class S06Actogram1(SpokenScene):
    def construct(self):
        bar,l,rows=record(); self.add(bar,l,rows.copy().set_opacity(.18))
        self.at('A mouse'); self.play(FadeIn(rows[0]),run_time=.3)
        self.at('runs in the dark'); self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]],lag_ratio=.15),run_time=.8)
        self.at('Each line'); self.play(Indicate(rows[2],color=YELLOW,scale_factor=1.02),run_time=.4)
        self.finish()


class S07Actogram2(SpokenScene):
    def construct(self):
        bar,l,rows=record(); self.add(bar,l,rows)
        self.at('Stack the days'); self.play(Indicate(rows,scale_factor=1.01,color=BLUE),run_time=.4)
        self.at('running starts'); self.play(Create(guide()),run_time=.4)
        self.at('clock looks locked'); self.play(Transform(l[-1],label('Looks locked to the light cycle',0,-3.15,30,YELLOW)),run_time=.3)
        self.finish()


class S08Clock(SpokenScene):
    def construct(self):
        bar,l,rows=record(); self.add(bar,*l[:-1],rows,guide())
        self.add(label('No rods or cones',0,3.4,30),label('Freedman et al., 1999 · schematic',0,-3.35,28))
        pulse=VGroup(Line([3.7,-.64,0],[4.6,-.64,0],color=YELLOW,stroke_width=9),
                     label('light on',5.75,-.64,26,YELLOW))
        self.at('In these'); self.play(FadeIn(pulse),run_time=.3)
        self.at('light still shifted')
        new=record(True)[2]
        self.play(*[Transform(rows[i][1],new[i][1]) for i in range(3,6)],run_time=.6)
        move=VGroup(arr([.1,-2.95,0],[1.05,-2.95,0],YELLOW,w=4),
                    label('onset moves later',3.6,-2.95,28,YELLOW))
        self.play(FadeIn(move),run_time=.25)
        self.finish()


class S09Melatonin(SpokenScene):
    def construct(self):
        header=label('Lucas et al., 1999 · rd/rd cl mice',0,3.2,30)
        self.add(header)
        brain=brain_map()[:2].scale(.42).move_to([-4,.4,0])
        pineal=np.array([-3.4,.25,0])
        gland=VGroup(brain,Dot(pineal,radius=.16,color=PURPLE))
        self.add(gland,label('pineal gland',-4,-1.35,28,PURPLE),
                 label('(in the brain)',-4,-1.9,26,PURPLE),
                 Line([-3.6,-1.05,0],pineal,color=PURPLE,stroke_width=2))
        base=-1.2
        dark=Rectangle(width=.8,height=2.6,color=GREEN,fill_opacity=.5).move_to([-.9,base+1.3,0])
        low=Rectangle(width=.8,height=1.1,color=GREEN,fill_opacity=.5).move_to([.9,base+.55,0])
        self.add(dark,label('dark',-.9,-1.65,28),label('light on',.9,-1.65,28,YELLOW),
                 label('melatonin',0,2.15,32,GREEN),label('schematic; no numeric scale',0,-2.55,26,GREY))
        self.at('suppressed melatonin'); self.play(FadeIn(low),GrowArrow(arr([-.5,.9,0],[.5,.1,0],YELLOW)),run_time=.45)
        self.at('Work on the pupil')
        e=eye_icon(4.5,.35,2.8)
        self.play(FadeIn(e),
                  Transform(header,label('melatonin: Lucas 1999 · rd/rd cl mice',-1.1,3.2,28)),
                  FadeIn(label('pupil work',4.5,-1.55,30,YELLOW)),
                  FadeIn(label('2001',4.5,-2.2,28,YELLOW)),run_time=.35)
        self.play(e.pup.animate.scale(.5),run_time=.4)
        self.finish()


class S10Something(SpokenScene):
    def construct(self):
        r,b,g,l=retina(True)
        # Keep light away from the open question over the two inner layers.
        light=VGroup(*[arr([x,3,0],[x,-2.5,0],YELLOW,w=3,tip=.13)
                       for x in [-4.65,.15]])
        self.add(light,r,b,g,l)
        q=label('?',-2.25,.9,80,YELLOW).set_height(2.5)
        self.at('So something'); self.play(FadeIn(q),run_time=.3)
        self.at('still measuring'); self.play(Indicate(g,color=YELLOW,scale_factor=1.03),run_time=.4)
        self.finish()


class S11Nonimage(SpokenScene):
    def construct(self):
        frame=Rectangle(width=4.5,height=3.1,color=GREY).move_to([-3.2,.35,0])
        picture=VGroup(Circle(radius=.35,color=YELLOW).move_to([-4.4,1.2,0]),
                        Polygon([-5,-.7,0],[-3.4,.7,0],[-1.3,-.7,0],color=GREY,fill_opacity=.25))
        VGroup(frame,picture).scale(1.25,about_point=[-3.2,.35,0])
        ga=gauge(3.2,.35,1.5)
        self.add(frame,picture,ga,label('image-forming',-3.2,-2.2,30),
                 label('brightness gauge',3.2,2.8,30,YELLOW))
        self.at('Responses like these'); self.play(Indicate(ga,color=YELLOW,scale_factor=1.04),run_time=.4)
        self.at('They are called',lead=.5); self.play(FadeIn(label('non-image-forming',3.2,-2.2,30)),run_time=.3)
        self.finish()


class S12Jobs(SpokenScene):
    def construct(self):
        self.add(label('non-image-forming',0,3.25,32),gauge(0,1.45,.875),
                 label('brightness gauge',3,1.6,30,YELLOW))
        ck=clock_icon(-3,-1.1,1.375); ey=eye_icon(3,-1.1,4)
        a1=arr([-.6,.4,0],[-2.5,-.1,0],YELLOW); a2=arr([.6,.4,0],[2.5,-.1,0],YELLOW)
        self.add(subdued(ck.copy()),subdued(ey.copy()),a1,a2)
        self.at('The first'); self.play(FadeIn(ck),FadeIn(label('body clock',-3,-2.8,32)),run_time=.35)
        self.at('setting the body'); self.play(Rotate(ck.h2,-PI/2,about_point=ck.c),run_time=.45)
        self.at('The second'); self.play(FadeIn(ey),FadeIn(label('pupil',3,-2.8,32)),run_time=.35)
        self.at('narrowing the pupil'); self.play(ey.pup.animate.scale(.45),run_time=.45)
        self.finish()


class S13Scn(SpokenScene):
    def construct(self):
        self.add(brain_map())
        self.at("The brain's"); self.play(FadeIn(nucleus(SCN,True)),run_time=.3)
        self.at('is the'); self.play(FadeIn(scn_annotation()),run_time=.3)
        self.add(label('Schematic locations',-2.5,-3.1,26,GREY))
        self.finish()


class S14Entrain(SpokenScene):
    def construct(self):
        self.add(brain_map(),nucleus(SCN,True),label('SCN',-3.4,-1.3,28,PURPLE),Line(SCN+[0,-.35,0],[-3.4,-1.05,0],color=PURPLE))
        ck=clock_icon(3.6,-.3,.8); eye=eye_icon(3.7,2.2,2.2)
        self.add(ck,eye,label('eye',5.5,2.2,28),label('body clock',3.6,-1.45,28))
        self.at('Light reaching'); self.play(GrowArrow(arr([2.5,2,0],SCN+[.35,.2,0],YELLOW)),run_time=.4)
        bar=VGroup(Rectangle(width=3,height=.4,color=YELLOW,fill_opacity=.6).move_to([-1.5,-2.6,0]),
                   Rectangle(width=3,height=.4,color=GREY,fill_opacity=.25).move_to([1.5,-2.6,0]),
                   label('day',-1.5,-3.15,28),label('night',1.5,-3.15,28))
        self.at('clock aligned'); self.play(FadeIn(bar),Rotate(ck.h2,-TAU,about_point=ck.c),run_time=.8)
        self.at('that is called'); self.play(FadeIn(label('photoentrainment',3.8,.95,30,YELLOW)),run_time=.3)
        self.finish()


class S15Opn(SpokenScene):
    def construct(self):
        e=eye_icon(4,1.9,2.8)
        self.add(brain_map(),e,label('pupil',4,3.05,30,YELLOW))
        self.at('The pupil reflex'); self.play(FadeIn(nucleus(OPN)),run_time=.25)
        # Dashed causal connector explicitly includes intervening brainstem steps.
        connector=DashedLine(OPN+[.2,.2,0],[2.6,1.9,0],color=PURPLE,stroke_width=4)
        self.at('driven from'); self.play(Create(connector),e.pup.animate.scale(.45),run_time=.4)
        self.at('the olivary'); self.play(FadeIn(VGroup(label('olivary pretectal\nnucleus (OPN)',3.5,.15,30,PURPLE),
             Line(OPN+[.15,-.15,0],[1.6,.1,0],color=PURPLE))),run_time=.3)
        self.add(label('Drives pupil reflex via\nother brainstem steps',3.8,-2.7,28))
        self.finish()


class S16Cells(SpokenScene):
    def construct(self):
        r,b,g,l=retina(True,True); self.add(rays(),r,b,g,l,label('Which cells measure light?',0,3.35,32,YELLOW))
        self.at('a small set'); self.play(g[4].animate.set_color(GREEN).set_fill(GREEN,.9),
                                         g[19].animate.set_color(GREEN).set_fill(GREEN,.9),
                                         FadeIn(label('a few among many',0,-3.05,32,GREEN)),run_time=.3)
        self.finish()


class S17Name(SpokenScene):
    def construct(self):
        c=ip_cell(); self.add(c[:-1])
        self.at('They are called',lead=.5); self.play(FadeIn(VGroup(label('intrinsically photosensitive',0,3.1,32,GREEN),label('retinal ganglion cell',0,2.55,32,GREEN))),run_time=.4)
        self.at('For short'); self.play(FadeIn(label('ipRGC',0,1.8,34,GREEN)),run_time=.35)
        self.finish()


class S18Two(SpokenScene):
    def construct(self):
        self.add(ip_cell()); light,pigment,bp=input_parts()
        self.at('Each makes'); self.play(FadeIn(light),FadeIn(pigment[0]),run_time=.35)
        self.at('pigment called'); self.play(FadeIn(pigment[1:]),run_time=.35)
        self.at('It also relays'); self.play(FadeIn(bp),run_time=.4)
        self.finish()


class S19Route(SpokenScene):
    def construct(self):
        self.add(label('in mice',0,3.15,36),label('retina',-4.5,3.15,28))
        boundary=RoundedRectangle(width=3.3,height=6,corner_radius=.4,color=GREY).move_to([-4.5,-.2,0])
        cs=VGroup(*[cell(-4.8,y,.6,.55,GREEN,fill=.5) for y in np.linspace(-2.3,2,6)])
        self.add(boundary,cs)
        # All axons enter a common bundle; no assignment of cell types to jobs.
        bundle=VGroup(*[Line(c.get_right(),[-1.5,0,0],color=GREEN,stroke_width=3) for c in cs])
        stem=Line([-1.5,0,0],[.6,0,0],color=GREEN,stroke_width=9)
        self.at('the main route'); self.play(Create(bundle),Create(stem),FadeIn(label('main route',-.9,.9,30,GREEN)),run_time=.4)
        self.at('the clock'); self.play(GrowArrow(arr([.6,0,0],[2.8,1.75,0],GREEN,w=6)),
            FadeIn(clock_icon(4,1.75,1.1)),FadeIn(label('clock',5.8,1.75,28)),run_time=.3)
        self.at('and the pupil'); self.play(GrowArrow(arr([.6,0,0],[2.6,-1.7,0],GREEN,w=6)),
            FadeIn(eye_icon(4,-1.7,2.8)),FadeIn(label('pupil',5.9,-1.7,28)),run_time=.3)
        minor=VGroup(DashedLine([-3,-2.6,0],[.2,-2.6,0],color=TEXT,stroke_width=4),
                     label('other routes, minor in mice',0,-3.25,28,TEXT))
        self.play(FadeIn(minor),run_time=.25)
        self.finish()


def question_icon(n):
    if n==1:
        # First-order response to a unit light step: r(t)=1-exp(-t/tau).
        ts=np.linspace(0,3,60); tau=.6
        pts=[[-5.5+t*.5,.2+.7*(1-np.exp(-t/tau)),0] for t in ts]
        return VMobject(color=GREEN,stroke_width=4).set_points_as_corners(pts)
    if n==2:
        return VGroup(arr([-5.7,0,0],[-4.7,0,0],YELLOW),label('V',-4.3,0,34,BLUE))
    return VGroup(cell(-5,0,1,.8,GREEN),Line([-5.5,-.5,0],[-4.5,.5,0],color=RED,stroke_width=6))


def question(n):
    texts=["What does the cell's own\nlight response look like?",'How does light become\na voltage?',
           'How do we know the clock and\npupil depend on these cells?']
    y=[1.65,-.3,-2.25][n-1]
    num=label(str(n)+'.',-3.5,y,38,YELLOW)
    txt=T(texts[n-1],36).move_to([-2.8,y,0],aligned_edge=LEFT)
    icon=question_icon(n).move_to([-5.1,y,0])
    return VGroup(icon,num,txt)


class S20Plan1(SpokenScene):
    def construct(self):
        self.add(label('Three questions come next',0,3.15,36,YELLOW),
                 VGroup(*[RoundedRectangle(width=12,height=1.6,corner_radius=.15,color=GREY,stroke_opacity=.4)
                          .move_to([0,y,0]) for y in [1.65,-.3,-2.25]]),question_icon(1).move_to([-5.1,1.65,0]))
        self.at('What does'); self.play(FadeIn(question(1)),run_time=.35)
        self.finish()


class S21Plan2(SpokenScene):
    def construct(self):
        self.add(label('Three questions come next',0,3.15,36,YELLOW),
                 VGroup(*[RoundedRectangle(width=12,height=1.6,corner_radius=.15,color=GREY,stroke_opacity=.4)
                          .move_to([0,y,0]) for y in [1.65,-.3,-2.25]]),question(1))
        self.at('How does light'); self.play(FadeIn(question(2)),run_time=.35)
        self.at('And how do'); self.play(FadeIn(question(3)),run_time=.35)
        self.finish()


class S22Take(SpokenScene):
    def construct(self):
        light,pigment,bp=input_parts()
        out=output_parts(); c=ip_cell(extended=False)
        # Centre the complete two-input / one-output picture and use its full height.
        diagram=VGroup(c,light,pigment,bp,out).scale_to_fit_height(6.6).move_to(ORIGIN)
        self.add(diagram)
        self.at('Two light signals'); self.play(Indicate(light[0],scale_factor=1.03),Indicate(bp[2],color=BLUE,scale_factor=1.03),run_time=.5)
        self.at('leave by one'); self.play(Indicate(out[0],color=GREEN,scale_factor=1.04),run_time=.45)
        self.finish()


class S23End(EndCard):
    LINE='Two light signals arrive at one cell, and leave by one exit.'

    def construct(self):
        self.add(label('Two light signals arrive at one cell,',0,.55,40),
                 label('and leave by one exit.',0,-.25,40),
                 label('biochemistrypedia.com',0,-1.55,26,TEAL))
        self.finish()
