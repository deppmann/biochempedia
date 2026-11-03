"""Word-cued chapter, redrawn after the twenty-item review.
COLOR MAP: BLUE vision; ORANGE touch; GREEN sum/cell response; TEAL precision;
PURPLE sound; YELLOW question; RED blocker/teaching; GREY axes/scope;
GOLD electric stimulus/receptor input; COPY command and negative image.
BRUSH is a lighter tint of COPY for delayed unipolar-brush-cell signals.
All response traces use explicit time-bin values from the lesson's illustrative
linear model. Basis curves are schematic overlapping Gaussian filters, not data.
Spike glyphs are analytic Gaussian timing symbols, not voltage recordings.
"""
import json
from pathlib import Path
import numpy as np
from bp_style import *
from bp_style import SpokenScene as _SpokenScene
COPY = '#9EACEB'
BRUSH = '#CFD7FF'
ORANGE = '#F29E4C'
PURPLE = '#B58CD9'

class SpokenScene(_SpokenScene):
    def at(self, phrase, lead=0, nth=0):
        # Record AFTER waiting. Shared bp_style logs its pre-wait time, which
        # misleadingly looks early. No changes to the shared pipeline/log files.
        target = self.t_of(phrase, nth)
        rest = target - self.elapsed()
        if rest > 0:
            self.wait(rest)
        with open('/tmp/fish-cue-audit.jsonl', 'a') as f:
            f.write(json.dumps(dict(scene=os.environ['KX_SCENE_ID'], phrase=phrase,
                                   target=target, actual=self.elapsed()))+'\n')

def p(x,y): return np.array([x,y,0.])
def label(s,y=3.15,c=TEXT,size=30,x=0): return T(s,size,c).move_to(p(x,y))
def base(y=0,x0=-5.2,x1=5.2): return DashedLine(p(x0,y),p(x1,y),color=GREY,stroke_width=2)
def bins(vals,y=0,scale=.32,x0=-5.2,w=10.4,color=GOLD):
    # No artificial end caps: nonzero endpoint values remain at their values.
    edges=np.linspace(x0,x0+w,len(vals)+1)
    points=[p(edges[0],y+scale*vals[0])]
    for i,v in enumerate(vals):
        if i: points.append(p(edges[i],y+scale*v))
        points.append(p(edges[i+1],y+scale*v))
    return VMobject(color=color,stroke_width=5).set_points_as_corners(points)
def pulse(y=0,color=GOLD,amp=6,scale=.32): return bins([0,amp,0],y,scale,color=color)
def tick(y=0,x=-5.2,caption=True):
    g=VGroup(Line(p(x,y),p(x,y+.65),color=COPY,stroke_width=5))
    if caption: g.add(label('command',y-.35,COPY,26,x=x+.45))
    return g

def time_axis(y=-3.1,text='time after command →',x=0):
    return label(text+'  ·  arbitrary units',y,TEXT,26,x=x)
def pointer(text,x,y,tx,ty,color=TEXT,size=26):
    t=label(text,y,color,size,x=x)
    start=t.get_bottom() if ty<y else t.get_top()
    return VGroup(t,Arrow(start,p(tx,ty),buff=.10,color=color,stroke_width=2,max_tip_length_to_length_ratio=.16))

def fish(x=-2,y=1,scale=1):
    body=Ellipse(width=4.4,height=1.65,color=TEXT,fill_color=TEXT,fill_opacity=.10)
    tail=Polygon(p(-2.05,0),p(-3,.8),p(-3,-.8),color=TEXT,fill_color=TEXT,fill_opacity=.15)
    eye=Dot(p(1.5,.27),radius=.08,color=TEXT)
    return VGroup(body,tail,eye).scale(scale).move_to(p(x,y))
def fields():
    # Rings centred at the tail, not around the animal's entire body.
    return VGroup(*[Arc(radius=r,start_angle=-PI/2,angle=PI,color=GOLD,
                       stroke_opacity=.55,stroke_width=2).rotate(PI).move_to(p(-4.5,1.25))
                   for r in [.55,.95,1.35]])
def fish_stage():
    return VGroup(fish(-1.7,1.1,1.25),fish(4.5,1.8,.52),fields())
def weak_trace(y=-2.2):
    # The weak outside event overlaps the self-pulse: 6 + .8 in a sub-bin.
    return bins([0,0,6,6,6.8,6,0,0],y,.27)

def circuit():
    cmd=chip('command',COPY,30).move_to(p(-4.55,2.35))
    organ=chip('electric organ',GOLD,30).move_to(p(3.35,2.35))
    lobe=chip('electrosensory\nlobe',TEXT,30,pad=.3).move_to(p(3.2,-1.8))
    rec=chip('receptors',GOLD,30).move_to(p(-4.55,-1.8))
    a=Arrow(cmd.get_right(),organ.get_left(),color=COPY,buff=.15,stroke_width=5)
    b=VMobject(color=COPY,stroke_width=5).set_points_as_corners([p(-1.9,2.35),p(-1.9,.2),p(3.2,.2)])
    b=VGroup(b,Arrow(p(3.2,.2),lobe.get_top(),color=COPY,buff=.1,stroke_width=5))
    c=Arrow(rec.get_right(),lobe.get_left(),color=GOLD,buff=.15,stroke_width=5)
    return cmd,organ,lobe,rec,a,b,c

def prediction():
    g=VGroup(label('Predict.',3.15,YELLOW,38),
             label('What does the command alone now do in the lobe?',2.45,TEXT,28),
             base(-.2),DashedVMobject(pulse(-.2,scale=.29),num_dashes=45).set_opacity(.65),
             tick(-.2),label('?',-.6,YELLOW,72),
             label('previous paired stimulus',1.9,GOLD,26,x=2.9))
    opts=VGroup(*[chip(t,YELLOW,28,pad=.25).move_to(p(x,-2.35))
                  for t,x in [('excited',-4),('no change',0),('inhibited',4)]])
    return VGroup(g,opts,time_axis(-3.25))

def mirror_state():
    gold=DashedVMobject(pulse(0,scale=.36),num_dashes=48).set_opacity(.8)
    return VGroup(label('Command alone after pairing',3.2,COPY,32),base(0),gold,
                  pulse(0,COPY,-6,.36),tick(0),
                  label('paired stimulus',2.55,GOLD,26,x=.4),
                  label('level before pairing',.38,TEXT,26,x=4.1),
                  label('excited',1.2,TEXT,26,x=-4.2),
                  label('inhibited',-1.5,TEXT,26,x=-4.2),time_axis(-3.25))

def learned_state():
    return VGroup(label('Command alone: newly learned mirror',3.2,COPY,30),base(0),tick(0),
                  DashedVMobject(bins([0,3,6],0,.32,w=7.8).add_line_to(p(2.6,0)),num_dashes=45).set_opacity(.75),
                  bins([0,-3,-6],0,.32,w=7.8,color=COPY).add_line_to(p(2.6,0)),
                  pointer('paired stimulus',3.3,2.65,1.3,1.92,GOLD),
                  pointer('learned mirror',2.8,-2.65,1.3,-1.92,COPY),time_axis(-3.35))

class S00Title(TitleCard):
    LESSON='Combining Senses and Predicting Them'
    TITLE='A Fish That Learns to Cancel Its Own Pulse'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',2.1,TEAL,28),
                 label(self.LESSON,1.25,TEXT,30),
                 label('A Fish That Learns to Cancel',.05,TEXT,44),
                 label('Its Own Pulse',-.9,TEXT,44),
                 Line(p(-1.5,-1.75),p(1.5,-1.75),color=GOLD,stroke_width=4))
        self.wait(4.5)

class S01Q(SpokenScene):
    def construct(self):
        stage=fish_stage(); self.add(stage[0],stage[1],time_axis(-2.75,'time →'))
        self.at('electric fish'); self.play(Create(stage[2]),run_time=.45)
        self.at('own pulses'); self.play(Create(weak_trace()),FadeIn(pointer('self-pulse',-3.75,-.35,-2.3,-.58,GOLD)),run_time=.55)
        self.at('Why does every')
        self.play(FadeIn(pointer('weak outside signal',3.6,.1,.65,-.36,GOLD)),
                  Create(DashedLine(p(4.1,1.35),p(1.7,.9),color=GOLD)),
                  FadeIn(label('How can the weak signal be heard?',-3.25,YELLOW,30)),run_time=.65)
        self.finish()

class S02Rec(SpokenScene):
    def construct(self):
        g=fish_stage(); self.add(g,weak_trace(),time_axis(-3.3,'time →'))
        dots=VGroup(*[Dot(p(x,1.2),radius=.12,color=GOLD) for x in [-3.7,-2.8,-1.9,-1,-.1]])
        self.at('Each pulse'); self.play(Indicate(g[2],color=GOLD,scale_factor=1.1),run_time=.5)
        self.at('also stimulates'); self.play(FadeIn(dots),run_time=.45)
        self.at('passive'); self.play(FadeIn(pointer('passive electroreceptors',-.8,2.8,-1.9,1.25,GOLD)),
                                       dots.animate.scale(1.35),run_time=.6)
        self.play(dots.animate.scale(1/1.35),run_time=.4)
        self.at('weak fields'); self.play(Create(Arrow(p(3.9,1.3),p(.15,1.2),color=GOLD,buff=.1)),
                                          FadeIn(label('weak fields\nfrom outside',.35,GOLD,28,x=3.65)),run_time=.5)
        self.play(Indicate(dots,color=GOLD,scale_factor=1.25),run_time=.65); self.finish()

class S04Copy(SpokenScene):
    def construct(self):
        a,b,c,d,e,f,g=circuit(); self.add(a,d,g,c,label('One command, two destinations',3.3,TEXT,32))
        self.at('fires the electric'); self.play(FadeIn(b),GrowArrow(e),run_time=.5)
        dot=Dot(e.get_start(),color=COPY,radius=.12); self.add(dot)
        self.play(MoveAlongPath(dot,e),run_time=.55); self.remove(dot)
        self.at('also copied'); self.play(Create(f),run_time=.45)
        path=VMobject().set_points_as_corners([p(-1.9,2.35),p(-1.9,.2),p(3.2,.2),c.get_top()])
        dot=Dot(p(-1.9,2.35),color=COPY,radius=.12); self.add(dot)
        self.play(MoveAlongPath(dot,path),run_time=.8); self.remove(dot); self.finish()

class S05Bell(SpokenScene):
    def construct(self):
        self.add(base(1),base(-1.4),label('receptor input',2.8,GOLD,30),
                 label('effect of command copy',-.35,COPY,30),label('Bell, 1981',-3.25,TEXT,28))
        a=bins([0,6,0,0],1,.2); b=bins([0,-1.2,-.6,0],-1.4,.4,color=COPY)
        self.add(a,b,time_axis(-2.65))
        self.at('not fixed'); self.play(Indicate(b,color=COPY,scale_factor=1.03),run_time=.55)
        self.at('changed to match'); self.play(Transform(a,bins([0,0,4,0],1,.3)),run_time=.55)
        self.play(Transform(b,bins([0,-.2,-1.7,0],-1.4,.4,color=COPY)),run_time=.65)
        self.finish()

class S06Para(SpokenScene):
    def construct(self):
        a,b,c,d,e,f,g=circuit(); self.add(a,b,c,d,e,f,g)
        self.at('the key test'); self.play(FadeIn(label('The key test',3.3,YELLOW,32)),run_time=.4)
        cross=VGroup(Line(p(5,2),p(5.6,2.7),color=RED,stroke_width=6),Line(p(5,2.7),p(5.6,2),color=RED,stroke_width=6))
        self.at('the fish'); self.play(FadeIn(pointer('neuromuscular blocker',3.7,.95,5.2,2,RED)),Create(cross),run_time=.6)
        self.at('still issues')
        dot=Dot(e.get_start(),color=COPY,radius=.13); self.add(dot)
        path=VMobject().set_points_as_corners([p(-1.9,2.35),p(-1.9,.2),p(3.2,.2),c.get_top()])
        copydot=Dot(p(-1.9,2.35),color=COPY,radius=.13); self.add(copydot)
        self.play(MoveAlongPath(dot,e),MoveAlongPath(copydot,path),run_time=1); self.remove(dot,copydot)
        self.at('no longer fires'); self.play(Create(Line(p(-.7,-3),p(5.5,-3),color=GOLD,stroke_width=4)),
                                              FadeIn(label('no organ pulse  ·  time →',-3.45,GOLD,26,x=2.5)),run_time=.45)
        self.finish()

class S07Pair(SpokenScene):
    def construct(self):
        self.add(label('Repeated pairing',3.2,TEXT,32),label('command',2.35,COPY,28,x=-4.8),
                 label('lobe response',-.8,GREEN,28,x=-4.5),base(-2.4),time_axis(-3.25))
        commands=VGroup(*[tick(1.3,x,False) for x in [-4.7,-1.8,1.1,4]])
        pulses=VGroup(*[bins([0,6,0],.2,.18,x0=x,w=2.4) for x in [-5.1,-2.2,.7,3.6]])
        responses=VGroup(*[bins([0,6,0],-2.4,.18,x0=x,w=2.4,color=GREEN) for x in [-5.1,-2.2,.7,3.6]])
        self.add(commands)
        name=label('artificial stimulus',-.4,GOLD,28,x=2.7)
        self.at('artificial stimulus'); self.play(LaggedStart(*[Create(m) for m in pulses],lag_ratio=.18),
                                                   Create(responses),FadeIn(name),run_time=1)
        self.at('mimics a pulse'); self.play(Indicate(pulses,color=GOLD,scale_factor=1.03),run_time=.5)
        self.at('switch the stimulus'); self.play(FadeOut(pulses),FadeOut(responses),FadeOut(name),
                                                 FadeIn(label('stimulus OFF',.15,GREY,30)),
                                                 Create(bins([0,0,0],-2.4,color=COPY)),run_time=.55)
        self.finish()

class S08Predict(SpokenScene):
    def construct(self):
        g=prediction(); self.add(g[0][2:5],g[0][6],g[2])
        self.at('Predict'); self.play(FadeIn(g[0][0]),run_time=.35)
        self.at('What does the'); self.play(FadeIn(g[0][1]),FadeIn(g[0][5]),FadeIn(g[1]),run_time=.5); self.finish()
class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction()); self.wait(5)

class S10Mirror(SpokenScene):
    def construct(self):
        g=mirror_state(); self.add(g[0],g[1],g[2],g[4],g[5],g[6],g[9])
        self.at('a mirror'); self.play(Create(g[3]),run_time=.6)
        self.at('stimulus excited'); self.play(FadeIn(g[7]),Indicate(g[2],color=GOLD,scale_factor=1.01),run_time=.55)
        self.at('alone inhibits'); self.play(FadeIn(g[8]),Indicate(g[3],color=COPY,scale_factor=1.01),run_time=.6); self.finish()

class S11Neg(SpokenScene):
    def construct(self):
        g=mirror_state(); self.add(g[0],g[1],g[2],g[3],g[4],g[5],g[6],g[9])
        self.at('negative image'); name=pointer('negative image',3.2,-2.5,1,-2.16,COPY)
        self.play(FadeIn(name),run_time=.45)
        real=pulse(0,scale=.36)
        self.at('Added to the')
        self.play(FadeOut(g[0]),FadeOut(g[2]),Create(real),
                  FadeIn(label('Adding the real input',3.2,TEXT,32)),run_time=.25)
        self.wait(1.5)
        self.at('it cancels')
        # Actual linear superposition: both components retain identity as their
        # deviations converge to the computed sum (0,6,0)+(0,-6,0).
        self.play(Transform(real,pulse(0,amp=0,scale=.36)),Transform(g[3],pulse(0,COPY,0,.36)),
                  FadeOut(name),FadeOut(g[5]),run_time=.75)
        self.remove(real,g[3]); self.add(bins(np.array([0,6,0])+np.array([0,-6,0]),0,color=GREEN))
        self.play(FadeIn(pointer('input + negative image',0,1.15,0,0,GREEN)),run_time=.3)
        self.wait(1.5); self.finish()

class S12Learned(SpokenScene):
    def construct(self):
        g=learned_state(); self.add(g[1],g[2],g[3],g[5],g[7],label('A different paired input',3.2,GOLD,32))
        self.at('It was learned'); self.play(Indicate(g[2],color=COPY,scale_factor=1.04),run_time=.5)
        self.at('whatever stimulus'); self.play(g[3].animate.set_opacity(.35),
                                               FadeIn(label('command alone',2.65,COPY,28,x=-3.2)),run_time=.35)
        self.play(Create(g[4]),FadeIn(g[6]),run_time=.85); self.finish()
class S13Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(learned_state()); self.wait(2)

class S14How(SpokenScene):
    def construct(self):
        self.add(label('How does one command become a mirror',3.15,TEXT,32),
                 label('with the right timing?',2.45,YELLOW,34),base(.1),tick(.1),
                 time_axis(-3.25))
        bracket=BraceBetweenPoints(p(-4.9,.6),p(-1.75,.6),direction=UP,color=YELLOW)
        self.add(bracket,label('?',1.7,YELLOW,48,x=-3.2))
        self.at('Kennedy and colleagues'); self.play(FadeIn(label('Kennedy and colleagues, 2014',-2.55,TEXT,28)),run_time=.45)
        self.at('recorded in'); self.play(FadeIn(label('awake, paralysed fish',-1.2,TEXT,32)),run_time=.5); self.finish()

def bank():
    rows=VGroup()
    for i in range(8):
        y=2.1-i*.64; color=COPY if i<5 else BRUSH
        xs=np.linspace(-3.55,2.2,120); mu=-3.1+i*.68
        ys=.48*np.exp(-.5*((xs-mu)/.55)**2)
        trace=VMobject(color=color,stroke_width=4).set_points_as_corners([p(x,y+v) for x,v in zip(xs,ys)])
        rows.add(VGroup(Dot(p(-3.9,y),radius=.1,color=color),trace,
                        Arrow(p(2.25,y),p(3.45,.85-i*.30),buff=.04,color=color,stroke_width=3.2,tip_length=.22,max_tip_length_to_length_ratio=.25)))
    return rows

def bank_labels():
    granule=label('granule\ncells',1.1,COPY,26)
    granule.next_to(BraceBetweenPoints(p(-4.35,2.55),p(-4.35,-.6),direction=LEFT),LEFT,buff=.22)
    brush=label('unipolar\nbrush\ncells',-1.7,BRUSH,26)
    brush.next_to(BraceBetweenPoints(p(-4.35,-.65),p(-4.35,-2.55),direction=LEFT),LEFT,buff=.22)
    return VGroup(granule,
                  BraceBetweenPoints(p(-4.35,2.55),p(-4.35,-.6),direction=LEFT,color=COPY),
                  brush,
                  BraceBetweenPoints(p(-4.35,-.65),p(-4.35,-2.55),direction=LEFT,color=BRUSH),
                  Line(p(-3.65,2.65),p(-3.65,-2.6),color=COPY,stroke_width=3),
                  label('command',2.98,COPY,26,x=-3.65),
                  label('time after command →',-3.05,TEXT,26,x=-.4),
                  label('schematic overlapping filters · arbitrary units',-3.55,TEXT,26))
class S15Delays(SpokenScene):
    def construct(self):
        g=bank(); names=bank_labels(); self.add(names[4:])
        self.at('Granule cells'); self.play(Create(g[:5]),FadeIn(names[:2]),run_time=.8)
        self.at('different delays'); self.play(LaggedStart(*[Indicate(r[1],color=COPY,scale_factor=1.02) for r in g[:5]],lag_ratio=.1),run_time=.7)
        self.at('Unipolar brush cells'); self.play(Create(g[5:]),FadeIn(names[2:4]),run_time=.85); self.finish()
class S16Basis(SpokenScene):
    def construct(self):
        g=bank(); self.add(g,bank_labels())
        cell=chip('medium\nganglion\ncell',TEXT,28,pad=.48).move_to(p(4.85,-.2))
        self.at('Together'); self.play(FadeIn(cell),run_time=.45)
        self.at('temporal basis'); self.play(FadeIn(label('temporal basis',3.25,COPY,32,x=1.4)),run_time=.5)
        self.at('each peaking'); self.play(LaggedStart(*[Indicate(r[1],color=COPY,scale_factor=1.03) for r in g],lag_ratio=.1),run_time=1.05); self.finish()

def spike(x,y,width=.7,height=1.6,color=RED,filled=True):
    xs=np.linspace(x-2.5*width,x+2.5*width,100)
    ys=height*np.exp(-.5*((xs-x)/width)**2)
    g=VMobject(color=color,stroke_width=4).set_points_as_corners([p(a,y+b) for a,b in zip(xs,ys)])
    if filled:
        fill=VMobject(fill_color=color,fill_opacity=.3,stroke_width=0).set_points_as_corners([p(xs[0],y)]+[p(a,y+b) for a,b in zip(xs,ys)]+[p(xs[-1],y),p(xs[0],y)])
        return VGroup(fill,g)
    return g

def rule_input(amp=6): return bins([0,amp,0],-.9,.38,x0=-5.4,w=4.2,color=COPY)
class S17Rule1(SpokenScene):
    def construct(self):
        a=rule_input(); self.add(label('Two rules set input strength',3.45,TEXT,34),
                                base(-.9),a,label('active input',1.8,COPY,28,x=-3.3),
                                time_axis(-3.25))
        self.at('An input'); self.play(Indicate(a,color=COPY,scale_factor=1.03),run_time=.45)
        self.at('followed shortly'); self.play(Create(BraceBetweenPoints(p(-2.6,1),p(.4,1),direction=UP,color=TEXT)),
                                              FadeIn(label('within a short window',2.2,TEXT,26,x=-.5)),run_time=.5)
        broad=spike(1,-.9,.53,2.1)
        self.at('a broad spike'); self.play(Create(broad),FadeIn(pointer('dendritic teaching spike',2.8,2.7,1,1.2,RED)),
                                            Create(spike(4.8,-.9,.045,1.1,GREY,False)),
                                            FadeIn(pointer('output spikes\nno effect',4.65,.95,4.8,.2,TEXT)),run_time=.65)
        self.at('is weakened'); self.play(Transform(a,rule_input(2)),
                                           FadeIn(chip('1  weaken',RED,32,pad=.3).move_to(p(-3.2,-2.45))),
                                           FadeIn(pointer('anti-Hebbian',-3,-1.7,-3.3,-.14,RED)),run_time=.6); self.finish()

class S18Rule2(SpokenScene):
    def construct(self):
        self.add(label('Every active input',3.2,COPY,34),label('active inputs',2.45,COPY,30),
                 base(.25),time_axis(-3.35))
        g=VGroup(*[bins([0,3,0],.25,.42,x0=-5.6+i*3.8,w=3,color=COPY) for i in range(3)])
        self.add(g)
        self.at('every active input'); self.play(Indicate(g,color=COPY,scale_factor=1.02),run_time=.45)
        self.at('strengthened a little'); self.play(*[Transform(g[i],bins([0,4.3,0],.25,.42,x0=-5.6+i*3.8,w=3,color=COPY)) for i in range(3)],
                                                   FadeIn(chip('2  strengthen',COPY,34,pad=.3).move_to(p(0,-.45))),
                                                   *[FadeIn(label('+',1.7,GREEN,52,x=x)) for x in [-5.6,-1.8,2]],run_time=.65)
        self.at('whether or not')
        c1=chip('cell fires',TEXT,36,pad=.32).move_to(p(-3,-1.65)); c2=chip('cell silent',TEXT,36,pad=.32).move_to(p(3,-1.65))
        self.play(FadeIn(c1),FadeIn(c2),Create(spike(-3,-2.95,.035,.5,GREY,False)),
                  Create(Line(p(1.7,-2.95),p(4.3,-2.95),color=GREY)),run_time=.6); self.finish()

# Averaged boost eta*10 minus depression eta*response. All initial weights
# are 10; a pulse with inhibition in flank bins illustrates rare-spike growth.
# Finite training deliberately retains residual modulation.
def learn(n):
    stimulus=np.array([-1.,6.,-1.]); w=np.full(3,10.)
    for _ in range(n): w += .12*(10-(w+stimulus))
    return w,w+stimulus
class S19Learn(SpokenScene):
    def construct(self):
        self.add(label('Simplified time-bin model · averaged learning',3.6,TEXT,28),
                 label('active inputs',2.6,COPY,28,x=-4.3),
                 label('cell response',-.9,GREEN,28,x=-4.3),
                 label('response, arbitrary units',-2.8,TEXT,26),
                 label('time bin after command →',-3.4,TEXT,28))
        w,r=learn(0); a=bins(w,.4,.14,color=COPY); b=bins(r,-2.5,.10,color=GREEN)
        self.add(a,b); count=label('pulse 1',-.3,TEXT,28,x=4.6); self.add(count)
        # Pulse 1 keeps equal initial strengths; the first update is pulse 2.
        self.at('weakens or strengthens'); self.play(Transform(a,bins(learn(1)[0],.4,.14,color=COPY)),
                                                   Transform(b,bins(learn(1)[1],-2.5,.10,color=GREEN)),
                                                   Transform(count,label('pulse 2',-.3,TEXT,28,x=4.6)),run_time=.65)
        broad=spike(.3,1.9,.55,.65); narrow=spike(2.55,1.9,.065,.65,GREY,False)
        teaching=VGroup(broad,narrow,pointer('dendritic teaching spike',.1,2.95,.3,2.5,RED),
                        pointer('output: no effect',4.4,2.95,2.55,2.5,TEXT))
        self.at('broad teaching spikes'); self.play(FadeIn(teaching),run_time=.55)
        self.at('With enough'); self.play(FadeOut(teaching),run_time=.35)
        for n in [5,10]:
            w,r=learn(n); self.play(Transform(a,bins(w,.4,.14,color=COPY)),Transform(b,bins(r,-2.5,.10,color=GREEN)),
                                   Transform(count,label(f'pulse {n}',-.3,TEXT,28,x=4.6)),run_time=.6)
        self.at('learning shrinks'); w,r=learn(20)
        self.play(Transform(a,bins(w,.4,.14,color=COPY)),Transform(b,bins(r,-2.5,.10,color=GREEN)),
                  Transform(count,label('pulse 20',-.3,TEXT,28,x=4.6)),run_time=.7); self.finish()

# Worked example: separate zero-centred change and absolute-response panels.
def sum_state():
    top=VGroup(label('Change from pre-learning response',3.4,TEXT,30),base(2),
               pulse(2,scale=.14),pulse(2,COPY,-6,.14),
               bins([0,0,0],2,color=GREEN),
               pointer('pulse effect',3.75,2.95,1.1,2.84,GOLD),
               pointer('learned change',3.8,1.05,1.1,1.16,COPY),
               label('near-zero residual, in this simplified example',.6,GREEN,26))
    ticks=VGroup(*[label(t,2+v*.14,TEXT,28,x=-5.95) for t,v in [('+6',6),('0',0),('−6',-6)]],
                  Line(p(-5.5,1.1),p(-5.5,2.9),color=GREY))
    # The absolute panel spans 2.8 units (35% of the frame). Bars now use
    # a 0.19 scale, nearly twice the former height, with a separate change axis.
    y0=-2.65; unit=.19; baseline=y0+10*unit
    bottom=VGroup(label('Absolute response',.08,TEXT,30,x=-3.65),
                  base(baseline).set_stroke(width=5),
                  bins([10,10,10],y0,unit,color=GREEN).set_stroke(width=3),
                  label('10',baseline,TEXT,30,x=-5.95),label('0',y0,TEXT,30,x=-5.95))
    for x,lo,hi,color,txt in [(-3.6,0,10,GREY,'10'),(-1.2,4,10,COPY,'−6'),(1.2,4,10,GOLD,'+6')]:
        bar=Rectangle(width=1.15,height=(hi-lo)*unit,color=color,fill_color=color,fill_opacity=.35).move_to(p(x,y0+(lo+hi)*unit/2))
        bottom.add(bar,label(txt,-.4,color,32,x=x))
    bottom.add(label('= 10',-1.65,GREEN,36,x=3.75),
               label('baseline response',-.4,GREEN,26,x=3.7),
               Arrow(p(-1.2,baseline-.05),p(-1.2,y0+4*unit+.05),color=COPY,buff=0,stroke_width=4),
               Arrow(p(1.2,y0+4*unit+.05),p(1.2,baseline-.05),color=GOLD,buff=0,stroke_width=4),
               Line(p(5.45,-2.65),p(5.45,.45),color=GREY),
               label('change',-1.2,TEXT,28,x=6.6).rotate(PI/2),
               *[label(t,baseline+v*unit,TEXT,28,x=6.05) for t,v in [('+6',6),('0',0),('−6',-6)]])
    foot=VGroup(label('All synapses stay excitatory',-3.2,TEXT,28),
                label('arbitrary units, middle time bin · time after command →',-3.7,TEXT,26))
    return top,ticks,bottom,foot
class S20Sum(SpokenScene):
    def construct(self):
        g,t,b,f=sum_state(); self.add(g[0],g[1],g[2],g[5],t,f[1])
        self.at('learning shrinks'); self.play(Indicate(g[2],color=GOLD,scale_factor=1.02),run_time=.45)
        self.at('command alone now dips'); self.play(Create(g[3]),FadeIn(g[6]),run_time=.65)
        self.at('pulse excited'); self.play(Create(g[4]),FadeIn(g[7]),run_time=.45)
        self.play(FadeIn(b),FadeIn(f[0]),run_time=.65); self.finish()
class S20bBeat(Scene):
    def construct(self):
        self.camera.background_color=BG; g,t,b,f=sum_state(); self.add(g,t,b,f); self.wait(2)

class S21Scope(SpokenScene):
    def construct(self):
        f=fish(-3.3,.7,1.1); model=chip('model',COPY,36,pad=.4).move_to(p(4,.7))
        self.add(label('What the evidence covers',3.15,TEXT,34),f,model,
                 label('paralysed',-.8,RED,30,x=-3.3))
        self.at('built on these recordings'); self.play(Create(Arrow(p(.3,.7),model.get_left(),color=TEXT,buff=.1)),
                                                        FadeIn(label('recordings,\nthen model',1.85,TEXT,28,x=1.4)),run_time=.55)
        self.at('learned to cancel'); self.play(Indicate(model,color=COPY,scale_factor=1.04),run_time=.55)
        self.at('The limit'); self.play(FadeIn(label('paralysed fish + a model',-2.25,TEXT,34)),run_time=.55)
        self.play(FadeIn(label('not a swimming fish',-3.1,RED,30)),run_time=.4); self.finish()

class S22Take(SpokenScene):
    def construct(self):
        self.add(label('Take this with you',3.3,YELLOW,34),base(-.5),
                 label('baseline',-.15,TEXT,26,x=4.65),time_axis(-3.45))
        a=chip('command copy',COPY,30,pad=.3).move_to(p(-3.8,2))
        b=chip('learned, timed\nnegative image',COPY,28,pad=.4).move_to(p(3,2))
        # Context retained from the prior reveal while the closing words begin.
        ghost=DashedVMobject(pulse(-.5,scale=.26),num_dashes=40).set_opacity(.55); self.add(ghost)
        self.at('a copy of'); self.play(FadeIn(a),run_time=.45)
        self.at('the circuit learns'); self.play(GrowArrow(Arrow(a.get_right(),b.get_left(),color=COPY)),FadeIn(b),run_time=.55)
        self.at('negative image'); self.play(Create(pulse(-.5,COPY,-6,.26)),run_time=.55)
        self.at('expected input')
        self.add(pointer('residual at baseline',0,-2.85,0,-.5,GREEN))
        self.play(FadeOut(ghost),Create(pulse(-.5,scale=.26)),
                  Create(bins([0,0,0],-.5,color=GREEN)),run_time=.4)
        self.wait(1.75); self.finish()
class S23End(EndCard):
    LINE='The circuit learns to reduce the expected input’s central effect.'

    def construct(self):
        line=VGroup(label('The circuit learns to reduce',.6,TEXT,38),
                    label('the expected input’s central effect.',-.2,TEXT,38))
        self.play(FadeIn(line),run_time=.45)
        self.play(FadeIn(label('biochemistrypedia.com',-1.35,TEAL,28)),run_time=.3)
        self.finish()
