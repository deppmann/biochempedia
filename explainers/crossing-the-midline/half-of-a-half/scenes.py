"""Chapter 3: dose, genetic interaction and shared receptors.
COLOR MAP: BLUE axons/growth cones; RED Slit and wrong crossings;
YELLOW all fly Robos; GREY midline/structure; GOLD mean/highlight.
PURPLE Comm and ORANGE vertebrate Robo3 reserved by the series.
No molecular structures. Normal quantiles below use the lesson's illustrative fit.
"""
from bp_style import *
import numpy as np

_style_chip = chip
def chip(*args, **kwargs):
    g = _style_chip(*args, **kwargs)
    g[0].set_fill(BG, opacity=1)
    return g
from statistics import NormalDist

# Local timing avoids the shared helper's pre-wait diagnostic file and 0.2 s
# anticipation. Round to video frames, and preserve about 1 s after spoken words.
class TimedScene(SpokenScene):
    def at(self, phrase, lead=0, nth=0):
        target = self.t_of(phrase, nth)
        if target > self.elapsed():
            self.wait(target-self.elapsed())

    def finish(self, hold=1):
        import os, json
        from pathlib import Path
        words=json.loads((Path(os.environ['KX_SCRIPT']).parent/'audio/words.json').read_text())[os.environ['KX_SCENE_ID']]
        end=max(self.narration_s, (words[-1][1]+hold) if words else self.narration_s)
        if end>self.elapsed(): self.wait(end-self.elapsed())


def label(s,x=0,y=3.15,color=TEXT,size=30):
    return T(s,size=size,color=color).move_to([x,y,0])


def midline(x=0,w=.8,y0=-2.8,y1=2.8):
    return RoundedRectangle(width=w,height=y1-y0,corner_radius=.12,
        color=GREY,fill_color=GREY,fill_opacity=.24).move_to([x,(y0+y1)/2,0]).set_z_index(-5)


def cone(x,y,r=1.2):
    body=Circle(radius=r,color=BLUE,fill_color=BLUE,fill_opacity=.16).move_to([x,y,0])
    fil=VGroup(*[Line([x+r*np.cos(a),y+r*np.sin(a),0],
        [x+(r+.55)*np.cos(a),y+(r+.55)*np.sin(a),0],color=BLUE,stroke_width=4)
        for a in np.linspace(-1.1,1.1,5)])
    return VGroup(body,fil)


def dock_pair():
    membrane=Line([-5,-2.1,0],[1,-2.1,0],color=BLUE,stroke_width=12)
    stalk=RoundedRectangle(width=.75,height=3.2,corner_radius=.15,color=YELLOW,
        fill_color=YELLOW,fill_opacity=.15).move_to([-2,-.5,0])
    cup=Arc(radius=.72,start_angle=PI,angle=PI,color=YELLOW,stroke_width=8).move_to([-2,1.4,0])
    slit=chip('Slit',RED,34).move_to([-4.8,2.35,0])
    return VGroup(membrane,stalk,cup,slit,label('Robo',-2,-2.7,YELLOW,34))


def ladder(kind,x):
    collapsed=kind=='slit'
    width=.55 if collapsed else 3.4
    rails=VGroup(*[Line([x+dx,-2.65,0],[x+dx,2.65,0],color=BLUE,stroke_width=9)
                   for dx in (-width/2,width/2)])
    rungs=VGroup(*[Line([x-width/2,y,0],[x+width/2,y,0],color=BLUE,stroke_width=10)
                   for y in np.linspace(-2.25,2.25,8)])
    if collapsed:
        rungs=VGroup(*[VMobject(color=BLUE,stroke_width=5).set_points_smoothly(
            [[x+dx,-2.65,0],[x+dx+.08,-1.2,0],[x+dx-.06,1,0],[x+dx,2.65,0]])
            for dx in np.linspace(-.4,.4,6)])
    return VGroup(midline(x,1.2 if collapsed else .65,-2.8,2.8),rails,rungs)


def questions():
    return VGroup(ladder('robo',-3.5),ladder('slit',3.5),
        label('robo1 mutant',-3.5,-3.2),label('slit null',3.5,-3.2),
        label('?',0,0,size=76),label('Why do the null mutants look different?',y=3.35,size=30))

# Common large chart: 0..40%, six units tall including annotation band.
NULL=100*(1-.98*.96)
def chart_axes(question=False):
    ax=Axes(x_range=[0,4,1],y_range=[0,40,10],x_length=10.2,y_length=5,
        tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([.1,.2,0])
    g=VGroup(ax,label('Made-up segment errors',y=3.35,size=32))
    for v in (0,10,20,30,40):
        g.add(T(str(v),26,color=GREY).next_to(ax.c2p(0,v),LEFT,buff=.18))
    g.add(label('segments with wrong crossings, %',x=-6.15,y=.2,size=26).rotate(PI/2))
    return ax,g


def error_bar(ax,x,val,name):
    b=Rectangle(width=1.15,height=5*val/40,stroke_width=0,fill_color=BLUE,fill_opacity=.85).move_to(ax.c2p(x,val/2))
    # Value labels inside a dark plate above the null line, with a short leader.
    p=ax.c2p(x,10 if val<10 else val+3)
    value=T(f'{val:g}%',30).move_to(p)
    leader=Line(b.get_top()+UP*.05,value.get_bottom()+DOWN*.08,color=GREY)
    return VGroup(b,value,leader,T(name,26).move_to(ax.c2p(x,0)+DOWN*.45))


def error_chart(third=False,reveal=False,null=True,question=False):
    ax,g=chart_axes()
    g.add(error_bar(ax,1,2,'slit/+'),error_bar(ax,2,4,'robo/+'))
    if third:
        g.add(T('slit/+ robo/+',26).move_to(ax.c2p(3,0)+DOWN*.45))
        if reveal:
            g.add(error_bar(ax,3,32,'slit/+ robo/+'))
        else:
            g.add(DashedVMobject(Rectangle(width=1.15,height=3.9,color=GREY).move_to(ax.c2p(3,15.6))),
                  T('?',60).move_to(ax.c2p(3,19)))
        if null:
            # End before the value-label columns; null label lives in the bottom band.
            line=DashedLine(ax.c2p(.15,NULL),ax.c2p(3.7,NULL),color=GREY)
            g.add(line,label('what independent errors would give: about 6%',y=-3.4,size=27))
            g.add(T('5.9%',26,color=GREY).next_to(line,RIGHT,buff=.12))
    if question:
        g[1].become(label('What would a much bigger number mean?',y=3.35,size=30))
    return g

# Same normal guidance-margin model as Going deeper. Fit the two given points;
# every dot is a fixed quantile sample, not a hand-picked outcome.
NORM=NormalDist()
SIGMA=(.5-.25)/(NORM.inv_cdf(.32)-NORM.inv_cdf(.03))
THRESH=.5+SIGMA*NORM.inv_cdf(.03)
OFFSETS=np.array([SIGMA*NORM.inv_cdf((i+.25)/50) for i in range(50)])

def threshold_stage(mean=.5,colored=False,subtitle='One possible threshold model'):
    ax=NumberLine(x_range=[-.2,1,.2],length=11,include_ticks=True,
                  include_numbers=False,color=GREY).move_to([0,-1.7,0])
    g=VGroup(ax,label(subtitle,y=3.3,size=32))
    for x in (-.2,0,.2,.4,.6,.8,1):
        g.add(T(f'{x:g}',26,color=GREY).next_to(ax.n2p(x),DOWN,buff=.2))
    g.add(label('push in one segment',y=-2.8,size=30))
    cut=DashedLine(ax.n2p(THRESH)+DOWN*.1,ax.n2p(THRESH)+UP*3.7,color=RED)
    g.add(cut,T('threshold ≈ 0.167',28,color=RED).move_to([ax.n2p(THRESH)[0]-1.25,2.35,0]))
    mark=Line(ax.n2p(mean)+DOWN*.1,ax.n2p(mean)+UP*3.4,color=GOLD,stroke_width=3)
    g.add(mark,T(f'mean = {mean:g}',28,color=GOLD).move_to([ax.n2p(mean)[0]+.7,2.05,0]))
    dots=VGroup()
    for i,offset in enumerate(OFFSETS):
        p=mean+offset
        # Stack in five staggered lanes: y has no probabilistic meaning.
        dots.add(Dot(ax.n2p(p)+UP*(.35+.34*(i%5)),radius=.085,
                     color=RED if colored and p<THRESH else BLUE))
    g.add(dots,label('each dot = one segment',x=-3.55,y=-3.4,size=27),
          label('red = wrong crossing',x=3.45,y=-3.4,size=27,color=RED))
    count=int(np.sum(mean+OFFSETS<THRESH))
    if colored:
        g.add(label(f'{count} of 50 wrong crossings',y=1.15,size=32,color=RED))
    else: g.add(label('50 segments',y=1.15,size=27))
    # Text plates prevent marker lines from striking through the labels.
    for text_mob in (g[-1], g[11], g[13]):
        if isinstance(text_mob, Text):
            text_mob.add_to_back(BackgroundRectangle(text_mob, color=BG, fill_opacity=1, buff=.08))
    return g,dots


def factors(s=1,r=1):
    g=VGroup(label('Slit × Robo1 = push',y=3.25,size=36),
        label('Toy calculation, not measured signal',y=-3.3,size=28),
        label('Other Robos ignored',y=2.65,size=26,color=GREY))
    for x,name,val,c in ((-4,'Slit',s,RED),(0,'Robo1',r,YELLOW),(4,'push',s*r,BLUE)):
        base=-2.4
        outline=Rectangle(width=1.7,height=4,color=GREY,stroke_opacity=.6).move_to([x,base+2,0])
        bar=Rectangle(width=1.7,height=4*val,color=c,fill_color=c,fill_opacity=.8).move_to([x,base+2*val,0])
        g.add(outline,bar,label(name,x,2.05,c,30),label({1:'1',.5:'1/2',.25:'1/4'}[val],x,base+4*val+(-.38 if val==1 else .3),size=30,color=BG if val==1 else TEXT))
    g.add(label('×',-2,-.4,size=44),label('=',2,-.4,size=44))
    return g

class S00Title(TitleCard):
    LESSON='Crossing the Midline Once: Slit, Robo and Comm'
    TITLE='A Quarter of the Push, Many Times the Errors'
    def construct(self):
        g=VGroup(label('BIOCHEMISTRYPEDIA',y=2, color=TEAL,size=28),
            label('Crossing the Midline Once',y=1.15,size=30,color=GREY),
            label('A Quarter of the Push,',y=.15,size=46),
            label('Many Times the Errors',y=-.65,size=46),
            Line([-1.5,-1.5,0],[1.5,-1.5,0],color=GOLD,stroke_width=4))
        self.play(FadeIn(g),run_time=.5);self.wait(2.5)

class S01Question(TimedScene):
    def construct(self):
        c=cone(-2,0,1.8);rb=chip('Robo',YELLOW,32).move_to([-.65,.2,0]);mid=midline(3,1.4)
        self.add(mid,c,rb,label('growth cone',-2,-2.7,BLUE),label('midline',3,-3.2,GREY))
        self.at('keeps axons off');self.play(c.animate.shift(LEFT*.4),rb.animate.shift(LEFT*.4),run_time=.6)
        self.at('where is the repellent');self.play(FadeIn(label('?',3,.4,size=84)),
            FadeIn(label('where is the repellent?',y=3.3,size=34)),run_time=.4);self.finish()

class S02Cell(TimedScene):
    def construct(self):
        sheets=VGroup(*[Rectangle(width=3.8,height=4.8,color=GREY,fill_color=BG,fill_opacity=1).rotate(a).move_to([-3.2+i*.18,0,0])
                         for i,a in enumerate((-.12,.12,0))])
        cover=VGroup(label('Cell',-2.84,1.55,size=54),label('1999',-2.84,.45,size=36),label('Slit',-2.84,-.6,RED,42),
                     Line([-4,-1.4,0],[-1.7,-1.4,0],color=GOLD))
        self.add(sheets,cover)
        cells=VGroup(*[Ellipse(width=1.25,height=1.5,color=GREY,fill_color=GREY,fill_opacity=.35).move_to([1.3,y,0]) for y in (-1.65,0,1.65)])
        self.at('It is slit');self.play(FadeIn(cells),FadeIn(label('midline glia',1.3,-3,GREY,28)),run_time=.5)
        dots=VGroup(*[Dot([1.8,y,0],radius=.14,color=RED) for y in (-1.8,-.8,.2,1.2,2.1)])
        self.at('secreted by');self.add(dots);self.play(dots.animate.shift(RIGHT*2.6),
            FadeIn(label('Slit (secreted)',3.8,3.1,RED,30)),run_time=1.2);self.finish()

class S03Brose(TimedScene):
    def construct(self):
        g=dock_pair().scale(1.1).shift(RIGHT*2)
        self.add(g,label('Brose, Bland and colleagues · 1999',y=3.3,size=30))
        self.at('bind');self.play(g[3].animate.move_to(g[2].get_center()+UP*.38),run_time=.55)
        self.play(Flash(g[2].get_center(),color=GOLD,flash_radius=1),
                  FadeIn(label('binds',3,1.2,GOLD,34)),run_time=.4);self.finish()

class S04Repel(TimedScene):
    def construct(self):
        gel=RoundedRectangle(width=11.5,height=5.4,corner_radius=.3,color=GREY,fill_color=GREY,fill_opacity=.07)
        source=chip('Slit2 cells',RED,32).move_to([4,0,0])
        explant=Circle(radius=.75,color=BLUE,fill_color=BLUE,fill_opacity=.3).move_to([-.8,0,0])
        glow=Circle(radius=1.5,color=RED,fill_color=RED,fill_opacity=.13).move_to(source)
        self.add(gel,glow,source,explant,label('spinal motor explant in a gel',y=3.25,size=32))
        paths=VGroup()
        for y in np.linspace(-2.1,2.1,7):
            p=VMobject(color=BLUE,stroke_width=5).set_points_smoothly([[-.8,0,0],[-1.25,y*.3,0],[-2.5,y*.8,0],[-5,y,0]])
            paths.add(p)
        self.at('Recombinant');self.play(Create(paths),run_time=2.1)
        self.at('embryonic spinal');self.play(Indicate(paths,color=BLUE,scale_factor=1.03),run_time=.6)
        self.add(label('axons grow away from Slit2',y=-3.25,size=30,color=BLUE));self.finish()


def chromosomes():
    g=VGroup(label('Kidd, Bland and Goodman',y=3.3,size=30))
    for x,name,c in ((-3,'slit',RED),(3,'robo',YELLOW)):
        for j,dx in enumerate((-.8,.8)):
            bar=RoundedRectangle(width=.65,height=3.8,corner_radius=.2,color=GREY).move_to([x+dx,.15,0])
            badge=chip(name,c,28).move_to([x+dx,.15,0])
            g.add(bar,badge)
            if j==0:
                # One clean cross over the missing copy, outside the gene label.
                centre=np.array([x+dx,1.25,0])
                g.add(Line(centre+[-.23,-.23,0],centre+[.23,.23,0],color=RED,stroke_width=5),
                      Line(centre+[-.23,.23,0],centre+[.23,-.23,0],color=RED,stroke_width=5))
    return g

class S05Genetics(TimedScene):
    def construct(self):
        self.add(chromosomes())
        captions=VGroup(label('slit/+   and   robo/+',y=-2.55,size=34),
            label('Heterozygote: missing one copy',y=-3.25,size=28))
        self.at('missing one copy');self.play(FadeIn(captions),run_time=.4)
        self.at('called heterozygotes');self.play(Indicate(captions[1],color=GOLD,scale_factor=1.03),run_time=.4);self.finish()

class S06Numbers(TimedScene):
    def construct(self):
        self.add(label('Made-up numbers',y=3.3,size=36))
        grid=VGroup(*[RoundedRectangle(width=.95,height=.8,corner_radius=.08,color=BLUE,fill_color=BLUE,fill_opacity=.15) for _ in range(50)]).arrange_in_grid(rows=5,cols=10,buff=.18)
        self.add(grid)
        self.at('Score');self.play(LaggedStart(*[Indicate(g,color=GOLD,scale_factor=1.02) for g in grid],lag_ratio=.01),run_time=1)
        self.at('for wrong crossings');self.play(FadeIn(label('50 segments per genotype',y=-3.2,size=32)),run_time=.4);self.finish()

class S07Singles(TimedScene):
    def construct(self):
        ax,g=chart_axes();self.add(g)
        self.at('of slit');self.wait(.92);self.play(FadeIn(error_bar(ax,1,2,'slit/+')),run_time=.3)
        self.at('of Robo');self.wait(.78);self.play(FadeIn(error_bar(ax,2,4,'robo/+')),run_time=.3);self.finish()

class S08Q(TimedScene):
    def construct(self):
        g=error_chart();self.add(g)
        self.at('remove one copy');self.play(Transform(g,error_chart(True,null=False)),run_time=.45)
        self.at('you would expect');self.play(Transform(g,error_chart(True)),run_time=.5)
        self.at('What would');self.play(Transform(g,error_chart(True,question=True)),run_time=.4);self.finish()

class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(error_chart(True,question=True));self.wait(5)

class S10Reveal(TimedScene):
    def construct(self):
        g=error_chart(True,question=True);self.add(g)
        self.at('result is');self.wait(.72)
        self.play(Transform(g,error_chart(True,True)),run_time=.65)
        self.at('far more');self.play(FadeIn(label('about 5× expected',x=1.4,y=2.55,color=GOLD,size=30)),
            Create(VGroup(Line([3.9,-1.55,0],[3.9,1.7,0],color=GOLD),Line([3.7,-1.55,0],[4.1,-1.55,0],color=GOLD),Line([3.7,1.7,0],[4.1,1.7,0],color=GOLD))),run_time=.4);self.finish()

class S11Push(TimedScene):
    def construct(self):
        g=factors();self.add(g)
        self.at('each factor scale');self.play(Transform(g,factors(.5,1)),run_time=.6)
        self.add(label('one Slit copy lost',x=-4,y=-2.9,color=RED,size=26));self.finish()

class S12Quarter(TimedScene):
    def construct(self):
        g=factors(.5,1);self.add(g)
        self.at('half the push');self.play(Indicate(g[12],color=GOLD),run_time=.4)
        self.at('One missing copy of each');self.play(Indicate(g[8],color=GOLD),run_time=.4)
        self.at('leaves a quarter');self.play(Transform(g,factors(.5,.5)),FadeIn(label('1 → 1/2 → 1/4',y=-2.9,size=30,color=GOLD)),run_time=.35);self.finish()

class S13Nothresh(TimedScene):
    def construct(self):
        ax=Axes(x_range=[0,1,.25],y_range=[0,6,1],x_length=4.8,y_length=4.6,tips=False,
                axis_config={'include_ticks':False,'color':GREY}).move_to([-3.4,.1,0])
        self.add(ax,label('Linear toy: errors track lost push',y=3.35,size=32),
            label('lost push',-3.4,-2.9,size=28),label('errors, %',-4.4,2.8,size=28),
            label('scaled so half the push lost gives 3%',y=-3.5,size=27))
        for y in (0,3,6):self.add(T(str(y),26,color=GREY).next_to(ax.c2p(0,y),LEFT,buff=.15))
        for x,s in ((0,'0'),(.5,'1/2'),(.75,'3/4'),(1,'1')):self.add(T(s,26).next_to(ax.c2p(x,0),DOWN,buff=.15))
        comparison=VGroup()
        for x,val,name in ((2,4.5,'linear toy'),(4.8,32,'made-up result')):
            b=Rectangle(width=1.25,height=4.6*val/32,color=BLUE,fill_color=BLUE,fill_opacity=.8).move_to([x,-2.2+2.3*val/32,0])
            comparison.add(b,label(f'{val:g}%',x,b.get_top()[1]+.35,size=30),label(name,x,-2.7,size=26))
        self.at('errors simply tracked');self.play(Create(ax.plot(lambda x:6*x,x_range=[0,1],color=BLUE)),FadeIn(comparison),run_time=.6)
        for x,y,s in ((.5,3,'3%'),(.75,4.5,'4.5%')):
            self.add(Dot(ax.c2p(x,y),color=GOLD),T(s,28,color=GOLD).next_to(ax.c2p(x,y),UL,buff=.12))
        self.at('Then the double');self.play(Indicate(comparison[0],color=GOLD),run_time=.4);self.finish()

class S14Thresh(TimedScene):
    def construct(self):
        g,d=threshold_stage();self.add(g);self.remove(d)
        self.at('Segments vary');self.play(FadeIn(d),run_time=.6);self.finish()

class S15Half(TimedScene):
    def construct(self):
        g,_=threshold_stage();self.add(g)
        self.at('Few fail');target,td=threshold_stage(.5,True)
        self.remove(g[-1]);g.remove(g[-1]);self.add(target[-1])
        self.play(*[dot.animate.set_color(td[i].get_color()) for i,dot in enumerate(g[-3])],run_time=.35);self.finish()

class S16QuarterFail(TimedScene):
    def construct(self):
        g,dots=threshold_stage(.5,True);self.add(g)
        self.at('With a quarter');target,td=threshold_stage(.25,True)
        self.play(Transform(dots,td),Transform(g[12],target[12]),
            FadeOut(g[13]),FadeIn(target[13]),FadeOut(g[-1]),run_time=.7)
        self.at('Many segments');self.play(FadeIn(target[-1]),run_time=.35);self.finish()

class S17Meaning(TimedScene):
    def construct(self):
        g,_=threshold_stage(.25,True);self.add(g)
        qualifier=label('Dose data alone do not prove this model',y=2.8,size=28,color=TEXT)
        # Qualifier is present for this entire interpretive beat.
        self.add(BackgroundRectangle(qualifier,color=BG,fill_opacity=1,buff=.12),qualifier)
        self.at('genetic interaction');self.play(Transform(g[1],label('Genetic interaction',y=3.35,size=34)),run_time=.4)
        self.at('A shared pathway');self.play(Indicate(g[2],color=GOLD,scale_factor=1.03),run_time=.4);self.finish()

class S18Ligand(TimedScene):
    def construct(self):
        g=dock_pair().scale(1.2).shift(LEFT*.15+DOWN*.15);right=ladder('slit',3.5)
        self.add(g,right,label('slit null',3.5,-3.45,size=30))
        self.at('binding data');self.play(g[3].animate.move_to(g[2].get_center()+UP*.38),run_time=.65)
        self.at('a ligand');self.play(FadeIn(label('ligand',-3.9,2.9,RED,30)),run_time=.3)
        self.at('on a receptor');self.play(Indicate(g[1],color=YELLOW),run_time=.35);self.finish()

class S19Q2(TimedScene):
    def construct(self):
        self.add(questions());self.at('One puzzle remains');self.finish()

class S20Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(questions());self.wait(5)


def three_receptors():
    body=RoundedRectangle(width=10.8,height=5.5,corner_radius=1.1,color=BLUE,
        fill_color=BLUE,fill_opacity=.12).move_to([0,-.1,0])
    receptors=VGroup(*[chip(n,YELLOW,32).move_to([x,1.6,0]) for x,n in ((-3.4,'Robo1'),(0,'Robo2'),(3.4,'Robo3'))])
    return VGroup(body,receptors)

class S21Three(TimedScene):
    def construct(self):
        g=three_receptors().scale(.72).shift(LEFT*1.8)
        mid=midline(4.2,1.0,-2.7,2.7)
        self.add(g[0],mid,label('growth cone',-1.8,3.3,BLUE,32),label('midline',4.2,-3.25,GREY,28))
        self.at('Flies have');self.play(FadeIn(g[1]),run_time=.6)
        note=VGroup(label('fly Robo3 ≠ mouse Robo3',x=-1.8,y=-2.7,size=26,color=GREY))
        self.at('three');self.play(FadeIn(note),run_time=.35)
        self.at('Losing');self.play(g[1][0].animate.set_opacity(.3),run_time=.5)
        path=Arrow([1.8,-.8,0],[5.8,-.8,0],color=BLUE,stroke_width=10,buff=0)
        self.at('axons cross freely');self.play(GrowArrow(path),run_time=.65);self.finish()

class S22Rest(TimedScene):
    def construct(self):
        self.add(midline(0,1.2),label('midline',0,-3.25,GREY,28))
        c=cone(0,-1.45,.9)
        rb=chip('Robo2',YELLOW,28).move_to([.15,-1.25,0]);moving=VGroup(c,rb)
        slit=chip('Slit',RED,30).move_to([2.7,1.9,0])
        self.add(moving,slit,label('Robo2 still hears Slit',y=3.3,size=32))
        r3=chip('Robo3',YELLOW,26).move_to([-4,1.3,0])
        self.add(r3,label('positions axons',-4,.5,YELLOW,26),label('in the rails',-4,0,YELLOW,26))
        self.at('still hears slit');self.play(slit.animate.move_to([1.65,-.35,0]),run_time=.6)
        out=VMobject(color=BLUE,stroke_width=8).set_points_smoothly([[0,-1.45,0],[1.5,-1.45,0],[3.7,-1.0,0]])
        self.at('pushed out');self.play(Create(out),moving.animate.shift(RIGHT*3.7+UP*.45),
            slit.animate.move_to([4.8,.1,0]),run_time=.8)
        back=VMobject(color=BLUE,stroke_width=8).set_points_smoothly([[3.7,-1,0],[4.1,.3,0],[2.6,1.35,0],[-1.7,1.35,0]])
        self.at('crossing back');self.play(Create(back),MoveAlongPath(moving,back),FadeOut(slit),run_time=.65)
        self.finish(hold=1.5)

class S22bDouble(TimedScene):
    def construct(self):
        left=ladder('robo',-2.5);lab=label('robo1 mutant',-2.5,-3.25,size=28)
        self.add(left,ladder('slit',2.5),lab,label('slit null',2.5,-3.25,size=28),label('Remove Robo1 and Robo2',y=3.35,size=32))
        self.at('together');self.play(Transform(left,ladder('slit',-2.5)),FadeOut(lab),
            FadeIn(label('robo1, robo2 double mutant',-2.5,-3.25,size=26)),run_time=.55)
        self.at('looks much like');self.play(Indicate(left,color=BLUE,scale_factor=1.02),run_time=.3)
        self.finish(hold=1.4)

class S23SlitNull(TimedScene):
    def construct(self):
        mid=midline(0,2.6)
        receptors=VGroup(*[chip(n,YELLOW,30).move_to([3.9,y,0]) for y,n in ((1.8,'Robo1'),(0,'Robo2'),(-1.8,'Robo3'))])
        slit=chip('Slit',RED,32).move_to([-3.9,0,0])
        self.add(mid,receptors,slit,label('midline',0,-3.25,GREY,30))
        self.at('Losing slit');self.play(FadeOut(slit),FadeIn(chip('no Slit',RED,32).move_to(slit)),receptors.animate.set_opacity(.6),run_time=.5)
        self.add(label('receptors idle',y=3.3,size=32))
        axons=VGroup(*[VMobject(color=BLUE,stroke_width=7).set_points_smoothly([[x,-2.6,0],[x+.1,-1.2,0],[x-.08,1.1,0],[x,2.6,0]]) for x in np.linspace(-.75,.75,7)])
        self.at('Axons at');self.play(FadeIn(axons),run_time=.3);self.finish(hold=1.5)

class S24Take(TimedScene):
    def construct(self):
        s=chip('Slit',RED,32).move_to([0,2.8,0])
        rs=VGroup(*[chip(n,YELLOW,30).move_to([x,1.1,0]) for x,n in ((-3.8,'Robo1'),(0,'Robo2'),(3.8,'Robo3'))])
        arrows=VGroup(*[Arrow(s.get_bottom(),r.get_top(),color=YELLOW,buff=.2) for r in rs])
        self.add(s,rs,arrows,label('The takeaway',y=-.15,size=34,color=GOLD))
        self.at('the ligand is shared');self.play(FadeIn(label('The ligand is shared',x=-2.8,y=-1.05,size=30)),run_time=.35)
        self.at('receptors share');self.play(FadeIn(label('Receptors share the work',x=2.8,y=-1.05,size=30)),run_time=.35)
        # A small loss moves the push marker across the threshold.
        axis=Line([-4,-2.35,0],[4,-2.35,0],color=GREY)
        cut=Line([0,-2.7,0],[0,-1.9,0],color=RED,stroke_width=5)
        dot=Dot([.8,-2.35,0],radius=.13,color=BLUE)
        self.at('Near');self.play(FadeIn(VGroup(axis,cut,dot)),
            FadeIn(label('threshold',0,-1.7,RED,26)),run_time=.35)
        self.at('small losses');self.play(dot.animate.shift(LEFT*1.6).set_color(RED),
            FadeIn(label('Small losses can make large effects',y=-3.2,size=32)),run_time=.55)
        self.finish(hold=1.8)

class S25End(EndCard):
    LINE='Near a threshold, small losses can make large effects.'
