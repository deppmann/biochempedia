"""Pass On the Surprise: revised, word-aligned teaching diagrams.
COLOR MAP: BLUE peripheral/regular afferents; PURPLE irregular timing channel;
YELLOW central neurons/response; GREEN motor command/prediction;
TEAL actual neck feedback; ORANGE passive turns; RED mismatch/hearing loss;
WHITE implant stimulation. GREY structural axes (captions use bright INK).
Models: rate-integrated spike trains r=12+18*exp(-((t-.5)/.17)^2),
with seeded renewal noise for distinct spike timing; 40/4 spikes/s and 2/.2
sensitivity example from lesson; normalized exponential adaptation schematic
using the lesson's 24-trial group constant, with explicitly schematic catch rise.
Implant pulse timing integrates the same rotation waveform, with uniform pulses.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
TEALN = '#3FB8C0'
INK = '#D4D9E2'


def lab(s, x=0, y=0, c=TEXT, n=34):
    return T(s, n, c).move_to([x,y,0])

def heading(s): return lab(s, 0, 3.28, n=38)
def footer(s): return lab(s, 0, -3.4, INK, 36)
def arr(a,b,c=GREY,w=5):
    return Arrow(a,b,buff=.08,color=c,stroke_width=w,tip_length=.2,
                 max_tip_length_to_length_ratio=.3)
def box(w,h,x,y,c=GREY):
    return RoundedRectangle(width=w,height=h,corner_radius=.18,
                            stroke_color=c,fill_color=c,fill_opacity=.06).move_to([x,y,0])
def head_icon(c=GREEN, scale=1):
    face=Circle(radius=.62,color=c,stroke_width=5,fill_color=c,fill_opacity=.13)
    nose=Triangle(stroke_width=0,fill_color=c,fill_opacity=1).scale(.17).move_to([0,.73,0])
    return VGroup(face,nose).scale(scale)
def turn_arrow(center,c,clockwise=True,r=2.25):
    # Signed angle agrees with Rotate(-angle): clockwise turn; CCW reflex.
    arc=Arc(radius=r,start_angle=PI*.88 if clockwise else PI*.12,
            angle=-PI*.76 if clockwise else PI*.76,color=c,stroke_width=6,
            fill_opacity=0)
    arc.add_tip(tip_length=.22)
    arc.move_arc_center_to(center)
    return arc

def head_stage(pose=0):
    h=head_icon(GREEN,3.7).move_to([-.8,.1,0])
    h.rotate(pose,about_point=[-.8,.1,0])
    neck=VGroup(Line([-1.4,-2.05,0],[-1.4,-2.75,0],color=TEALN,stroke_width=13),
                Line([-.2,-2.05,0],[-.2,-2.75,0],color=TEALN,stroke_width=13))
    return VGroup(h,neck,lab('neck',-.8,-2.98,TEALN,32))
def head_labels(muted=False):
    a=turn_arrow([-.8,.1,0],GREEN,True,2.52)
    r=turn_arrow([-.8,.1,0],GREY if muted else YELLOW,False,2.85)
    if muted: r=DashedVMobject(r,num_dashes=22)
    # Labels are adjacent to different arc ends, with separated leader lines.
    al=lab('your turn',3.85,1.45,GREEN,34)
    rl=VGroup(lab('head-steadying',3.85,.05,GREY if muted else YELLOW,32),
              lab('reflex',3.85,-.5,GREY if muted else YELLOW,32))
    lead1=Line([2.6,1.45,0],[1.65,1.05,0],color=GREEN)
    lead2=Line([2.25,-.25,0],[2.12,.35,0],color=GREY if muted else YELLOW)
    return a,r,VGroup(al,rl,lead1)

def bell(t): return np.exp(-((t-.5)/.17)**2)
def positions(seed=0,irregular=False,device=False):
    ts=np.linspace(0,1,6001)
    rate=12+18*bell(ts)
    if irregular: rate=12+28*bell(ts)+np.maximum(0,np.gradient(bell(ts),ts))*.7
    cum=np.cumsum(rate)/6000
    rng=np.random.RandomState(seed)
    levels=[]; q=.4
    while q<cum[-1]:
        levels.append(q)
        q+=1 if device else rng.uniform(.55,1.45)
    return np.interp(levels,cum,ts)
def spikes(x0,x1,y,seed=0,c=BLUE,h=.45,irregular=False,device=False):
    ps=positions(seed,irregular,device)
    baseline=Line([x0,y,0],[x1,y,0],color=c,stroke_width=2)
    marks=VGroup(*[Line([x0+(x1-x0)*t,y,0],[x0+(x1-x0)*t,y+h,0],color=c,stroke_width=3)
                   for t in ps])
    return VGroup(baseline,marks)
def envelope(y):
    return ParametricFunction(lambda t: [-5.25+10.5*t,y+.65*bell(t),0],
                              t_range=[0,1,.01],color=INK,stroke_width=3)
def neuron(radius=1.5,center=(0,0,0),lit=False):
    cell=Circle(radius=radius,color=YELLOW,stroke_width=5,fill_color=YELLOW,
                fill_opacity=.6 if lit else .07).move_to(center)
    rays=VGroup(*[Line(np.array(center)+radius*np.array([np.cos(a),np.sin(a),0]),
                       np.array(center)+(radius+min(.35,radius*.35))*np.array([np.cos(a),np.sin(a),0]),
                       color=YELLOW,stroke_width=4) for a in np.arange(6)*TAU/6])
    return VGroup(cell,rays)

def condition_card(x,title,kind):
    c=ORANGE if kind==0 else GREEN if kind==1 else RED
    g=VGroup(box(3.85,5.1,x,-.1,c),lab(title,x,2.05,c,30))
    h=head_icon(c,.85).move_to([x,.9,0]); h.rotate(-.45)
    g.add(h,turn_arrow([x,.9,0],c,True,.72))
    g.add(lab('motor command',x,-.05,GREEN,28))
    if kind: g.add(arr([x-1.3,-.55,0],[x+1.3,-.55,0],GREEN))
    if kind==0:
        g.add(lab('none',x,-.55,INK,28))
        # Cover a central part of the command arrow to make the absent command explicit.
        g[-1].add_background_rectangle(color=BG,opacity=1,buff=.04)
    g.add(lab('neck feedback',x,-1.15,TEALN,28))
    end=x+1.3 if kind!=2 else x+.1
    g.add(arr([x-1.3,-1.65,0],[end,-1.65,0],TEALN))
    g.add(lab('no prediction' if kind==0 else '✓ match' if kind==1 else '× mismatch',x,-2.3,c,30))
    return g

def comparison():
    return VGroup(heading('Which drive the neuron strongly?'),
                  condition_card(-4.15,'Passive turn',0),
                  condition_card(0,'Active, matched',1),
                  condition_card(4.15,'Active, mismatched',2))
def chart_base():
    g=VGroup(heading('Which drive the neuron strongly?'),
             lab('response modulation, spikes/s',0,1.45,INK,34))
    for x,s,c in [(-3.65,'Passive turn',ORANGE),(0,'Active, matched',GREEN),(3.65,'Active, mismatched',RED)]:
        g.add(lab(s,x,2.35,c,28))
    g.add(Line([-5.6,-2.4,0],[5.5,-2.4,0],color=INK),Line([-5.6,-2.4,0],[-5.6,.75,0],color=INK))
    for v in [0,20,40]:
        y=-2.4+3*v/40
        g.add(lab(str(v),-6,y,INK,30),Line([-5.68,y,0],[-5.52,y,0],color=INK))
        if v: g.add(DashedLine([-5.5,y,0],[5.4,y,0],color=GREY,stroke_opacity=.4))
    g.add(footer('Made-up numbers · 20°/s turn'))
    return g

def response_bar(x,v):
    h=3*v/40
    return VGroup(Rectangle(width=1.25,height=h,color=YELLOW,fill_color=YELLOW,fill_opacity=.75)
                  .move_to([x,-2.4+h/2,0]),lab(str(v),x,-2.8,YELLOW,32))

def cohort(x0=-5.25,dx=1.5,y=.9,scale=1):
    people=VGroup()
    for i in range(8):
        c=RED if i<7 else INK
        h=Circle(radius=.19,color=c,fill_color=c,fill_opacity=.85).move_to([0,.36,0])
        body=RoundedRectangle(width=.5,height=.7,corner_radius=.12,color=c,fill_color=c,
                              fill_opacity=.7 if i<7 else .06).move_to([0,-.22,0])
        p=VGroup(h,body)
        if i<3: p.add(lab('!',0,-.2,BG,28))
        people.add(p.scale(scale).move_to([x0+i*dx,y,0]))
    return people

class S00Title(TitleCard):
    LESSON='Balance: Two Codes for Every Head Movement'
    TITLE='Pass On the Surprise'
    def construct(self):
        self.add(lab('BIOCHEMISTRYPEDIA',0,2.1,TEAL,32),lab(self.LESSON,0,1.1,INK,32))
        self.play(Write(T(self.TITLE,48,font=TITLE_FONT)),run_time=1.2)
        self.add(Line([-1.2,-.8,0],[1.2,-.8,0],color=GOLD,stroke_width=4))
        self.finish()
class S01Q(SpokenScene):
    def construct(self):
        h=head_stage(); a,r,labels=head_labels()
        self.add(heading("Why doesn't the reflex fight you?"),h,labels)
        self.at('turn your own'); self.play(Rotate(h[0],-PI/3,about_point=[-.8,.1,0]),Create(a),run_time=.55)
        self.at('the reflex'); self.play(Create(r),run_time=.45)
        self.at('not fight you'); self.play(FadeIn(lab('?',-4.5,1.8,YELLOW,72)),run_time=.25)
        self.finish()
class S02Problem(SpokenScene):
    def construct(self):
        h=head_stage(-PI/3); a,r,labels=head_labels()
        self.add(heading('A disturbance?'),h,a,r,labels,lab('?',-4.5,1.8,YELLOW,72))
        self.at('a disturbance'); self.play(Indicate(r,color=YELLOW),run_time=.5)
        self.at('Your own turn'); self.play(Rotate(h[0],-.4,about_point=[-.8,.1,0]),run_time=.7)
        self.finish()
class S03Afferents(SpokenScene):
    def construct(self):
        g1=spikes(-5.25,5.25,.1,3); g2=spikes(-5.25,5.25,-2.1,29)
        self.add(heading('Does the ear tell them apart?'),lab('Self-made turn',0,2.4,GREEN),
                 lab('Matched imposed turn',0,.0,ORANGE).shift(UP*.05),
                 envelope(1.25),envelope(-1.2),g1.shift(UP*.55),g2,
                 lab('rate envelope',-3.9,1.8,INK,28),lab('rate envelope',-3.9,-.7,INK,28),
                 lab('Similar rates; different spike times',0,-2.72,INK,34),
                 footer('monkeys, schematic · Cullen and Minor, 2002'))
        # Replace the lower label position so neither envelope nor spike row crosses it.
        self.mobjects[2].move_to([0,-.05,0])
        self.at('In alert monkeys'); self.play(Indicate(g1),run_time=.4)
        self.at('canal afferents'); self.play(Indicate(g2),run_time=.4)
        self.at('responded to both')
        # Mark a clearly separated pair of spike times, with faint vertical guides.
        i=max(range(1, min(len(g1[1]),len(g2[1]))-1),
              key=lambda j: abs(g1[1][j].get_x()-g2[1][j].get_x()))
        highlight=VGroup(*[VGroup(
            Circle(radius=.13,color=YELLOW).move_to(g[1][i].get_top()),
            DashedLine([g[1][i].get_x(),-2.15,0],
                       [g[1][i].get_x(),1.18,0],color=YELLOW,stroke_width=2,stroke_opacity=.5))
            for g in (g1,g2)])
        self.play(FadeIn(highlight),run_time=.35)
        self.finish()
class S04Central(SpokenScene):
    def construct(self):
        ear=box(3.1,4.6,-4,.05,BLUE)
        cell=neuron(2.12,(2.6,-.15,0),False)
        self.add(heading('Cancellation is central'),ear,lab('ear',-4,1.7,BLUE,38),
                 Arc(radius=.95,start_angle=-PI*.65,angle=PI*1.5,color=BLUE,stroke_width=6).move_to([-4,-.25,0]),
                 box(6.2,5.25,2.65,0),lab('brainstem',2.65,2.42,INK,32),cell,
                 lab('cancel here',2.65,-2.82,YELLOW,36))
        incoming=arr([-2.35,0,0],[.12,0,0],BLUE)
        self.at('So'); self.play(GrowArrow(incoming),run_time=.35)
        self.at('must happen'); self.play(cell[0].animate.set_fill(YELLOW,.6),run_time=.5)
        self.finish()
class S05Vo(SpokenScene):
    def construct(self):
        cell=neuron(2.52,(0,-.1,0),True)
        ha=arr([-4.3,1.15,0],[-2.78, .65,0],BLUE)
        ea=arr([-4.3,-1.15,0],[-2.78,-.65,0],INK).set_opacity(.25)
        state=lab('HEAD: responds',-4.65,2.6,BLUE,32)
        self.add(heading('Vestibular-only neurons'),cell,ha,ea,state,
                 lab('head motion',-4.65,1.8,BLUE,32),lab('eye movement',-4.65,-1.85,INK,32),
                 arr([2.95,0,0],[3.65,0,0],YELLOW),lab('neck',4.65,.3,TEALN,36),lab('muscles',4.65,-.3,TEALN,36),
                 lab('Thought to drive the head-steadying reflex',0,-2.98,INK,32),footer('Roy and Cullen, 2004'))
        self.at('recorded'); self.play(Indicate(ha,color=BLUE),run_time=.35)
        self.at('thought to drive')
        ea.set_opacity(1)
        self.play(cell[0].animate.set_fill(YELLOW,.07),ha.animate.set_opacity(.25),
                  Transform(state,lab('EYE: no response',-4.65,2.6,INK,32)),Indicate(ea,color=TEXT),run_time=.4)
        self.at('the neck reflex'); self.play(Indicate(self.mobjects[8],color=YELLOW),run_time=.35)
        self.finish()
class S07Clues(SpokenScene):
    def construct(self):
        expected=box(5,1.2,-3.3,.25,GREEN)
        actual=box(5,1.2,3.3,.25,TEALN)
        self.add(heading('Two clues to a self-made turn'),box(5,1.05,-3.3,2.05,GREEN),
                 lab('motor command',-3.3,2.05,GREEN,36),box(5,1.05,3.3,2.05,TEALN),
                 lab('neck stretch',3.3,2.05,TEALN,36),expected,actual,
                 lab('expected neck stretch',-3.3,.25,GREEN,30),lab('actual neck stretch',3.3,.25,TEALN,30),
                 DashedLine([-3.3,1.45,0],[-3.3,.9,0],color=GREEN,stroke_width=5),
                 arr([3.3,1.45,0],[3.3,.9,0],TEALN),
                 box(7.8,1.4,0,-2.05,YELLOW),lab('brain compares:   ✓ match',0,-2.05,YELLOW,36),
                 arr([-3.3,-.45,0],[-1.6,-1.3,0],GREEN),arr([3.3,-.45,0],[1.6,-1.3,0],TEALN))
        self.at('the motor command'); self.play(Indicate(self.mobjects[1]),run_time=.45)
        self.at('which predicts'); self.play(Indicate(expected,color=GREEN),run_time=.6)
        self.at('The other'); self.play(Indicate(actual,color=TEALN),run_time=.6)
        self.at('actual sense of stretch'); self.play(Indicate(self.mobjects[12],color=YELLOW),run_time=.5)
        self.finish()
class S08Predict(SpokenScene):
    def construct(self):
        g=comparison(); self.add(g,footer('Pause: predict the central response'))
        self.at('A passive turn'); self.play(Indicate(g[1],scale_factor=1.025),run_time=.6)
        self.at('An active turn with matching'); self.play(Indicate(g[2],scale_factor=1.025),run_time=.6)
        self.at('An active turn with mismatched'); self.play(Indicate(g[3],scale_factor=1.025),run_time=.6)
        self.at('Which ones drive'); self.play(Indicate(g[0],scale_factor=1.02),run_time=.5)
        self.finish()
class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(comparison(),footer('Pause: predict'))
        ring=Circle(radius=.23,color=GREEN,stroke_width=5).move_to([2.2,-3.3,0])
        self.add(ring)
        full=ring.copy()
        self.play(UpdateFromAlphaFunc(ring, lambda m,a: m.pointwise_become_partial(full,0,1-a)),
                  run_time=5,rate_func=linear)
class S10Reveal(SpokenScene):
    def construct(self):
        self.add(chart_base())
        qs=[lab('?',x,-.8,INK,60) for x in [-3.65,0,3.65]]; self.add(*qs)
        self.at('The passive turn'); self.play(FadeOut(qs[0]),GrowFromEdge(response_bar(-3.65,40),DOWN),run_time=.5)
        self.at('with mismatched feedback'); self.play(FadeOut(qs[2]),GrowFromEdge(response_bar(3.65,40),DOWN),run_time=.5)
        self.at('Only the matched'); self.play(FadeOut(qs[1]),GrowFromEdge(response_bar(0,4),DOWN),run_time=.5)
        self.finish()
class S11Numbers(SpokenScene):
    def construct(self):
        self.add(heading('Sensitivity = response ÷ turn speed'),footer('Made-up numbers · 20°/s turn'))
        # Values sit on the same ticked axis; derive the result before naming it.
        self.add(Line([-5.7,-.8,0],[-1.65,-.8,0],color=INK),
                 Line([-5.7,-.8,0],[-5.7,1.65,0],color=INK),
                 lab('spikes/s',-3.8,2.55,INK,32))
        for v in (0,20,40):
            y=-.8+2.4*v/40
            self.add(Line([-5.8,y,0],[-5.6,y,0],color=INK),lab(str(v),-6.12,y,INK,26))
        for x,v,label,c in [(-4.8,40,'passive',ORANGE),(-2.6,4,'matched',GREEN)]:
            h=2.4*v/40
            self.add(Rectangle(width=1.05,height=h,color=YELLOW,fill_color=YELLOW,fill_opacity=.7)
                     .move_to([x,-.8+h/2,0]),lab(str(v),x,-.8+h+.29,YELLOW,34),
                     lab(label,x,-1.25,c,30))
        self.add(lab('40 ÷ 20 = 2.0',2.5,1.8,YELLOW,36),lab('4 ÷ 20 = 0.2',2.5,.95,YELLOW,36),
                 lab('spikes/s per °/s',2.5,0,INK,32))
        self.at('nearly all'); self.play(FadeIn(lab('1 − (0.2 ÷ 2.0) = 0.9',0,-2.0,GREEN,38)),run_time=.35)
        self.at('the response'); self.play(FadeIn(lab('90% cancelled',0,-2.75,GREEN,42)),run_time=.35)
        self.finish()
class S12NotOff(SpokenScene):
    def construct(self):
        self.add(heading('Matched active turn: central muting'),
                 lab('central response, spikes/s',0,2.55,YELLOW,34))
        baseline=-.35
        self.add(Line([-3.7,baseline,0],[5.3,baseline,0],color=INK),
                 Line([-3.7,baseline,0],[-3.7,1.65,0],color=INK))
        for v in (0,20,40):
            y=baseline+2*v/40
            self.add(lab(str(v),-4.08,y,INK,26),Line([-3.8,y,0],[-3.6,y,0],color=INK))
        for x,v in [(-1.8,40),(2.8,4)]:
            h=2*v/40
            self.add(Rectangle(width=1.65,height=h,color=YELLOW,fill_color=YELLOW,fill_opacity=.15 if v==40 else .8)
                     .move_to([x,baseline+h/2,0]),lab(str(v),x,baseline+h+.28,YELLOW,32))
        self.add(lab('passive',-5.25,1.05,INK,28),lab('reference',-5.25,.55,INK,28),
                 lab('matched active',2.8,1.4,GREEN,30))
        train=spikes(-5.2,5.2,-2.65,8,h=.7)
        bracket=VGroup(Line([-5.2,-1.65,0],[5.2,-1.65,0],color=BLUE),
                       Line([-5.2,-1.65,0],[-5.2,-1.85,0],color=BLUE),
                       Line([5.2,-1.65,0],[5.2,-1.85,0],color=BLUE))
        self.add(lab('ear afferents, unchanged',0,-1.28,BLUE,32),bracket,train,
                 footer('Central muting does not switch off the ear'))
        self.at('the ear switching off'); self.play(Indicate(train,color=BLUE),run_time=.45)
        self.at('The afferents kept firing'); self.play(ShowPassingFlash(train.copy().set_stroke(width=7)),run_time=.65)
        self.finish()
class S13NotFeel(SpokenScene):
    def construct(self):
        h=head_stage(-PI/3-.4); a,r,labels=head_labels(True)
        self.add(heading('A possible help to the head reflex'),h,a,r,labels)
        self.add(lab('quiet',3.85,-1.05,INK,28))
        # Retain the final intended-turn pose from S02 across the intervening diagrams.
        self.at('This muting may help'); self.play(Indicate(r,color=GREY),run_time=.4)
        self.at('from opposing'); self.play(Rotate(h[0],-.45,about_point=[-.8,.1,0]),run_time=.65)
        self.at('stop sensing')
        sensing=VGroup(lab('ear → brain',3.95,-1.6,BLUE,34),lab('still felt',3.95,-2.2,BLUE,34),
                       arr([.9,-1.2,0],[2.45,-1.6,0],BLUE))
        self.play(FadeIn(sensing),FadeIn(lab('You still feel the turn',0,-3.45, TEXT,36)),run_time=.4)
        self.finish()
class S15Brooks(SpokenScene):
    def construct(self):
        h=head_icon(GREEN,2.65).move_to([-3,-.45,0])
        a=turn_arrow([-3,-.45,0],GREEN,True,2.15)
        # Counter-rotation makes the load's opposition explicit.
        resistance=turn_arrow([-3,-.45,0],RED,False,2.65)
        dial=Circle(radius=.85,color=INK).move_to([3,-1.15,0])
        pointer=Line([3,-1.15,0],[2.55,-.55,0],color=RED,stroke_width=7)
        cerebellum=Ellipse(width=2.6,height=1.6,color=INK).move_to([3,1.12,0])
        marker=neuron(.48,(3,1.12,0),True)
        self.add(heading('A prediction must stay right'),h,a,dial,pointer,resistance,cerebellum,marker,
                 lab('your turn',-3,2.6,GREEN,34),lab('resistive load',3,-2.35,RED,32),
                 lab('Rostral fastigial neurons',3,2.55,YELLOW,30),
                 lab('monkeys · cerebellum, output nucleus',0,-2.92,INK,30),
                 footer('Brooks, Carriot and Cullen, 2015'))
        self.at('a cerebellar output nucleus'); self.play(Indicate(marker),run_time=.4)
        self.at('Their monkeys turned'); self.play(Rotate(h,-.55),Rotate(pointer,.4,about_point=[3,-1.15,0]),run_time=.8)
        self.at('against a resistive load'); self.play(Indicate(resistance,color=RED),run_time=.6)
        self.finish()

def adaptation():
    ax=Axes(x_range=[0,100,20],y_range=[0,1.1,.5],x_length=9.4,y_length=4.0,tips=False,
            axis_config={'color':INK,'include_ticks':False}).move_to([.55,.1,0])
    g=VGroup(ax,heading('Adaptation to a resistive load'),
             lab("neuron's vestibular sensitivity (relative)",0,2.55,INK,32))
    for v in [0,1]: g.add(lab(str(v),ax.c2p(0,v)[0]-.4,ax.c2p(0,v)[1],INK,30))
    for n in [0,20,40,60,80,100]:
        p=ax.c2p(n,0); g.add(lab(str(n),p[0],p[1]-.35,INK,30))
    g.add(lab('trials',.6,-2.8,INK,32))
    return ax,g

def adaptation_curve(ax):
    return ax.plot(lambda n:.12+.88*np.exp(-n/24),x_range=[0,80,.5],color=YELLOW,stroke_width=6)
def catch_objects(ax):
    low=.12+.88*np.exp(-80/24)
    return VGroup(DashedLine(ax.c2p(80,0),ax.c2p(80,.95),color=RED),
                  lab('load removed',3.65,1.9,RED,32),
                  Line(ax.c2p(80,low),ax.c2p(82,.64),color=YELLOW,stroke_width=6),
                  lab('rose again',5.52,.1,YELLOW,26))
class S16Fell(SpokenScene):
    def construct(self):
        ax,g=adaptation(); curve=adaptation_curve(ax); catch=catch_objects(ax)
        self.add(g,footer('schematic, not data'),Dot(ax.c2p(0,1),color=YELLOW,radius=.07))
        self.at('As the animals adapted'); self.play(Create(curve),run_time=2)
        self.at('the load was suddenly removed'); self.play(FadeIn(VGroup(*catch[:2])),run_time=.35)
        self.at('it rose again'); self.play(Create(catch[2]),FadeIn(catch[3]),run_time=.5)
        self.finish()
class S17Corr(SpokenScene):
    def construct(self):
        ax,g=adaptation()
        caption=footer('Recordings, correlational')
        self.add(g,adaptation_curve(ax),catch_objects(ax),lab('schematic, not data',-.4,1.4,INK,30),caption)
        self.at('They show what'); self.play(Indicate(self.mobjects[1],scale_factor=1.015),run_time=.4)
        self.at('not that they caused')
        self.play(Transform(caption,footer('Does not establish a cause of learning')),run_time=.4)
        self.finish()
class S18Implant(SpokenScene):
    def construct(self):
        # Ear context, three leads, electrodes, and named branches are present together.
        ear=Ellipse(width=1.25,height=5.1,color=INK,stroke_width=4).move_to([.15,-.15,0])
        self.add(heading('Vestibular implant'),ear,box(2.9,4.6,-4.6,0),lab('implant',-4.6,0,TEXT,38),
                 lab('ear / nerve',2.7,2.5,INK,32),footer('Both ears have lost their signal'))
        branches=VGroup()
        for y,s in [(1.2,'anterior canal branch'),(-.35,'lateral canal branch'),(-1.9,'posterior canal branch')]:
            branches.add(Line([-3.1,y*.7,0],[.2,y,0],color=TEXT,stroke_width=4),
                         Dot([.2,y,0],radius=.13,color=TEXT),
                         Line([.4,y,0],[5.7,y,0],color=BLUE,stroke_width=7),
                         lab(s,3.05,y+.43,BLUE,30))
        self.add(branches,lab('3 electrodes',-2.1,-2.78,TEXT,32))
        self.at('a vestibular implant'); self.play(Indicate(self.mobjects[2]),run_time=.4)
        self.at('the canal branches'); self.play(ShowPassingFlash(branches.copy().set_stroke(width=8)),run_time=.8)
        self.at('both ears have lost'); self.play(Indicate(self.mobjects[5],scale_factor=1.02),run_time=.4)
        self.finish()
class S19Code(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,1,1],y_range=[0,1.1,1],x_length=9.4,y_length=1.45,tips=False,
                axis_config={'include_ticks':False,'color':INK}).move_to([.65,1.4,0])
        v=ax.plot(lambda t:bell(t),x_range=[0,1,.01],color=TEXT,stroke_width=4)
        train=spikes(-4.05,5.35,-.65,c=TEXT,h=.85,device=True)
        self.add(heading('Head rotation → pulse rate'),ax,v,
                 lab('head velocity',-4.4,2.5,INK,32),lab('time →',4.8,.4,INK,30),
                 train,lab('implant pulses: rate follows rotation',0,-1.15,TEXT,32),
                 lab('otolith: no signal',-3,-2.35,INK,32),
                 DashedLine([.2,-2.35,0],[5.35,-2.35,0],color=GREY),
                 footer('Rotation only · not the natural two-channel code'))
        self.at('varies its pulses'); self.play(ShowPassingFlash(train.copy().set_stroke(width=7)),run_time=1)
        self.at('does not recreate'); self.play(Indicate(self.mobjects[-1],scale_factor=1.02),run_time=.4)
        self.at('no otolith signal'); self.play(Indicate(self.mobjects[7],color=INK),run_time=.5)
        self.finish()
class S20Cost(SpokenScene):
    def construct(self):
        self.add(heading('Eight adults: benefit and cost'),box(5.7,5.15,-3.15,-.1),box(5.7,5.15,3.15,-.1),
                 lab('Posture + gait',-3.15,1.95,TEXT,36),lab('Implanted-ear hearing',3.15,1.95,TEXT,30),
                 footer('Chow and colleagues, 2021'))
        # Five measured endpoints; two highlighted, not five participants.
        measures=VGroup(*[Rectangle(width=.7,height=1.3,color=GREEN if i<2 else GREY,
                                    fill_color=GREEN,fill_opacity=.65 if i<2 else .04)
                          .move_to([-5.15+i, .4,0]) for i in range(5)])
        people=cohort(1.18,.57,.35,.85)
        self.add(measures,people,lab('2 of 5 measures',-3.15,-1.05,GREEN,34),
                 lab('improved at 6 months',-3.15,-1.7,INK,30),
                 lab('7 of 8 reduced',3.15,-1.05,RED,34),lab('! severe in 3',3.15,-1.75,RED,32))
        self.at('some balance measures improved'); self.play(Indicate(measures,scale_factor=1.03),run_time=.6)
        self.at('Hearing in the implanted ear'); self.play(Indicate(people,scale_factor=1.05),run_time=.5)
        self.at('fell'); self.play(Indicate(self.mobjects[-2],color=RED),run_time=.4)
        self.finish()
class S21Feas(SpokenScene):
    def construct(self):
        people=cohort(y=1.4,scale=1.6)
        f=chip('feasibility',BLUE,size=40).move_to([-2.9,-.5,0])
        t=chip('trade-off',RED,size=40).move_to([2.9,-.5,0])
        bracket=VGroup(Line([-5.75,.25,0],[5.75,.25,0],color=INK),
                       Line([-5.75,.25,0],[-5.75,.6,0],color=INK),
                       Line([5.75,.25,0],[5.75,.6,0],color=INK))
        self.add(heading('The same eight adults'),people,f,t,
                 lab('Benefit for everyone remains unproven',0,-2.25,INK,36),
                 footer('Chow and colleagues, 2021'))
        self.add(bracket)
        self.at('feasibility'); self.play(Indicate(f,color=BLUE),run_time=.45)
        self.at('and a tradeoff'); self.play(Indicate(t,color=RED),run_time=.45)
        self.at('works for everyone'); self.play(Indicate(self.mobjects[4],color=INK,scale_factor=1.02),run_time=.45)
        self.finish()
class S22Takeaway(SpokenScene):
    def construct(self):
        a=spikes(-5.7,5.7,1.45,4,h=.4)
        b=spikes(-5.7,5.7,.15,15,PURPLE,.55,True)
        cell=neuron(.5,(0,-1.6,0),True)
        condition=lab('neck feedback = prediction',0,-.6,GREEN,34)
        self.add(heading('Report motion on two channels'),
                 lab('steady, precise rate channel',0,2.45,BLUE,32),a,
                 lab('higher-gain, timing channel',0,1.0,PURPLE,32),b,
                 condition,cell,Arrow([0,-.82,0],[0,-.98,0],buff=0,color=GREEN,stroke_width=4,tip_length=.12,max_tip_length_to_length_ratio=.5),
                 lab('Pass on mainly the surprise',0,-2.65,YELLOW,48),
                 lab('(matched neck feedback, tested neurons)',0,-3.35,INK,28))
        self.at('two channels'); self.play(Indicate(a),Indicate(b),run_time=.5)
        self.at('Where neck feedback matches'); self.play(Indicate(condition),run_time=.45)
        self.at('these head posture neurons'); self.play(Indicate(cell),run_time=.4)
        self.at('pass on mainly the surprise'); self.play(Indicate(self.mobjects[-2],scale_factor=1.025),run_time=.4)
        self.finish()
class S21End(EndCard):
    LINE='When neck feedback matches the prediction, these neurons pass on mainly the surprise.'
    def construct(self):
        self.add(heading('Pass On the Surprise'))
        g=VGroup(lab('When neck feedback matches the prediction,',0,1,GREEN,38),
                 lab('these neurons pass on mainly the surprise.',0,-.15,YELLOW,40))
        self.play(FadeIn(g),run_time=.5)
        self.add(lab('biochemistrypedia.com',0,-2.65,TEAL,32))
        self.finish()
