"""Predicting Midline Mutants — revised chapter 6.

COLOR MAP: BLUE axon; RED Slit/repulsion; YELLOW Robo1/2;
PURPLE Comm; ORANGE Robo3; GREY midline; GOLD prediction/highlight;
GREEN netrin/DCC attraction. Paths are qualitative biological schematics,
not data traces or quantitative trajectories. No molecular structures.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
LESSON_TITLE = 'Crossing the Midline Once: Slit, Robo and Comm'

class TimedScene(SpokenScene):
    # Same word alignment as bp_style, without generating an unrequested sync.log.
    def at(self, phrase, lead=.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > .02:
            self.wait(rest)


def heading(text, color=TEXT):
    return T(text, 34, color, weight=BOLD).move_to([0, 3.22, 0])


def strip(x=0, y0=-3.05, y1=.65, w=.7):
    return RoundedRectangle(width=w, height=y1-y0, corner_radius=.12,
        stroke_color=GREY, fill_color=GREY, fill_opacity=.22).move_to([x,(y0+y1)/2,0])


def make_cone(x, y=-1.15, s=2.6):
    body = Circle(radius=.3*s, color=BLUE, fill_color=BLUE, fill_opacity=.48, stroke_width=4)
    fil = VGroup(*[Line(.27*s*np.array([np.cos(a),np.sin(a),0]),
        .58*s*np.array([np.cos(a),np.sin(a),0]),color=BLUE,stroke_width=4)
        for a in (-.8,-.3,.3,.8)])
    g=VGroup(body,fil)
    # Anchor the body, rather than the asymmetric group's bounding box.
    g.shift([x,y,0]); g.body=body
    return g


def robo_marks(cone, s=2.6, opacity=1):
    return VGroup(*[RoundedRectangle(width=.13*s,height=.28*s,corner_radius=.04*s,
        stroke_width=0,fill_color=YELLOW,fill_opacity=opacity)
        .move_to(cone.body.get_center()+.31*s*np.array([np.cos(a),np.sin(a),0]))
        for a in (-.65,0,.65)])


def push(a,b,color=RED):
    return Arrow(a,b,buff=0,color=color,stroke_width=7,tip_length=.25,
        max_tip_length_to_length_ratio=.35)


def stage(x=-4.2,slit=True,receptors=False,weak=False,full=False):
    top=2.25 if full else .65
    mid=VGroup(strip(y1=top),T('midline',26,GREY).move_to([0,-3.4,0]))
    if slit:
        mid.add(*[Dot([sx*.49,y,0],radius=.13,color=RED)
            for sx in (-1,1) for y in np.linspace(-2.7,top-.4,4)])
        mid.add(T('Slit',26,RED).move_to([.95,top-.15,0]))
    cone=make_cone(x)
    if receptors: cone.add(robo_marks(cone,opacity=.32 if weak else 1))
    ax=always_redraw(lambda: Line([-6.1,-1.15,0],cone.body.get_center(),color=BLUE,stroke_width=9))
    return mid,cone,ax


EDGES=[-6.45,-3.8,-2.45,-.8,.85,3.55,6.45]
HEADS=['Genotype','Slit at\nmidline','Hears\nbefore','Hears\nafter','Prediction','Observed']
COLORS=[TEXT,RED,YELLOW,YELLOW,TEXT,TEXT]


def cell(text,col,y=1.65,size=26,color=None,edges=EDGES,line_spacing=.12):
    # Wrap by measured glyph width, keeping every label at least 26 pt.
    width=edges[col+1]-edges[col]-.14
    lines=[]
    for paragraph in text.split('\n'):
        line=''
        for word in paragraph.split():
            candidate=(line+' '+word).strip()
            if T(candidate,size).width>width and line:
                lines.append(line); line=word
            else: line=candidate
        lines.append(line)
    m=T('\n'.join(lines),size,color or COLORS[col],line_spacing=line_spacing)
    if m.width>width+.01: raise ValueError('Cell too wide: '+text)
    return m.move_to([(edges[col]+edges[col+1])/2,y,0])


def ledger(values=None,y=1.65):
    g=VGroup()
    for x in EDGES: g.add(Line([x,y-.66,0],[x,y+1.25,0],color=GREY,stroke_width=1))
    for yy in (y-.66,y+.5,y+1.25):
        g.add(Line([EDGES[0],yy,0],[EDGES[-1],yy,0],color=GREY,stroke_width=1))
    for k,t in enumerate(HEADS): g.add(cell(t,k,y+.875))
    for k,t in enumerate(values or []):
        if t:g.add(cell(t,k,y))
    return g


def recross(x=3.2,y=-2.45,end=-1.5):
    return VGroup(DashedLine([x,y,0],[end,y,0],color=BLUE,stroke_width=4,dash_length=.14),
        Triangle(color=BLUE,fill_color=BLUE,fill_opacity=1).scale(.12).rotate(PI/2).move_to([end,y,0]),
        T('may recross',26,BLUE).move_to([-3.75,y-.4,0]))


def receptor_label(cone,text):
    p=cone.body.get_center()
    return VGroup(T(text,28,YELLOW).move_to(p+[0,1.3,0]),
        Line(p+[.2,1.06,0],p+[.65,.45,0],color=YELLOW,stroke_width=2))


def ladder(kind,cx=4.9):
    g=VGroup(*[Line([cx+d,-2.9,0],[cx+d,.35,0],color=BLUE,stroke_width=6) for d in (-.7,.7)])
    if kind=='robo':
        for y in np.linspace(-2.55,.05,9):g.add(Line([cx-.7,y,0],[cx+.7,y,0],color=BLUE,stroke_width=5))
    return g


QUESTION_CASES={1:('Fly comm','When does the axon\nhear Slit?'),
    2:('Fly robo;comm','What happens\nat the midline?'),
    3:('Fly: modest Comm\nin every neuron','Can it hear Slit\nafter crossing?')}


def question_frame(kind,show_prompt=True):
    name,prompt=QUESTION_CASES[kind]
    mid,cone,ax=stage(x=-3.9,full=True)
    # Prompt is adjacent to the growth cone, across the midline.
    g=VGroup(heading('Your prediction'),chip(name,PURPLE if kind==3 else GOLD,30).move_to([-3.75,1.8,0]),
        mid,ax,cone)
    if show_prompt:g.add(T(prompt,34,GOLD).move_to([3.55,-.6,0]))
    return g


def countdown(scene,kind):
    scene.camera.background_color=BG
    scene.add(question_frame(kind))
    track=RoundedRectangle(width=4.2,height=.18,corner_radius=.08,color=GREY).move_to([3.55,-2.35,0])
    bar=Rectangle(width=4.12,height=.12,stroke_width=0,fill_color=GOLD,fill_opacity=1).move_to(track)
    scene.add(track,bar,T('5 seconds to predict',26,GOLD).move_to([3.55,-1.85,0]))
    scene.play(bar.animate.stretch(.001,0,about_point=bar.get_left()),run_time=5,rate_func=linear)


class S00Title(TitleCard):
    LESSON=LESSON_TITLE
    TITLE='Predicting Midline Mutants'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),
            T('Crossing the Midline Once:\nSlit, Robo and Comm',28,GREY),
            T(self.TITLE,46,font=TITLE_FONT),Line(LEFT*1.3,RIGHT*1.3,color=GOLD,stroke_width=4))
        g.arrange(DOWN,buff=.45).move_to(ORIGIN)
        self.play(FadeIn(g),run_time=.65);self.finish()


class S01Question(TimedScene):
    def construct(self):
        self.add(heading('Predicting Midline Mutants'))
        boxes=VGroup(*[RoundedRectangle(width=11.5,height=1.3,corner_radius=.15,
            stroke_color=c,fill_color=c,fill_opacity=.08).move_to([0,y,0])
            for y,c in zip((1.65,0,-1.65),(RED,YELLOW,BLUE))])
        self.at('Can three questions');self.play(FadeIn(boxes),run_time=.5)
        for cue,txt,i,c in [('Is slit there','Is Slit there?',0,RED),
            ('Can the axon','Can the axon hear it?',1,YELLOW),
            ('When does it','When does it start hearing it?',2,BLUE)]:
            self.at(cue);self.play(FadeIn(T(txt,36,c).move_to(boxes[i])),run_time=.35)
        self.finish()


class S02Table(TimedScene):
    def construct(self):
        self.add(heading('Read the ledger'),ledger())
        mid,cone,ax=stage(receptors=True,weak=True);self.add(mid,ax,cone)
        self.at('Here is a ledger');self.play(Indicate(self.mobjects[1],scale_factor=1.015),run_time=.5)
        self.at('Each row is');self.play(FadeIn(cell('Wild type\ncommissural',0)),run_time=.5)
        self.at('Read across')
        a=push([-5.9,1.15,0],[5.9,1.15,0],GOLD)
        self.play(GrowArrow(a),FadeIn(T('read across, left to right',28,GOLD).move_to([3.65,.55,0])),run_time=.65)
        self.finish()


class S03Wt(TimedScene):
    def construct(self):
        self.add(heading('Wild type: commissural'),ledger(['Wild type\ncommissural','yes','','','','']))
        mid,cone,ax=stage(receptors=True,weak=True);self.add(mid,ax,cone)
        self.at('barely hears');self.play(FadeIn(cell('weakly',2)),cone.animate.shift(RIGHT*2),run_time=.65)
        self.at('and hears it');self.play(cone.animate.shift(RIGHT*5.3),run_time=.65)
        self.play(cone[-1].animate.set_opacity(1),FadeIn(cell('strongly',3)),run_time=.3)
        self.at('It crosses once');self.play(FadeIn(cell('crosses\nonce',4)),FadeIn(cell('crosses\nonce',5)),run_time=.4)
        self.finish()


class S04Ipsi(TimedScene):
    def construct(self):
        self.add(heading('Wild type: ipsilateral'),ledger(['Wild type\nipsilateral','','','','','']))
        mid,cone,ax=stage(receptors=True);self.add(mid,ax,cone)
        self.at('hears slit');self.play(*[FadeIn(cell('yes',i)) for i in (1,2)],cone.animate.shift(RIGHT*1.7),run_time=.4)
        self.at('from the start');self.play(FadeIn(cell('yes',3)),run_time=.3)
        self.at('It never crosses');self.play(cone.animate.shift(LEFT*1),GrowArrow(push([-.8,-.1,0],[-2.8,-.1,0])),
            FadeIn(cell('never\ncrosses',4)),FadeIn(cell('never\ncrosses',5)),run_time=.5)
        self.finish()


class S05Q1(TimedScene):
    def construct(self):
        f=question_frame(1,False);self.add(f[0],*f[2:])
        self.at('A fly mutant');self.play(FadeIn(f[1]),run_time=.4)
        self.at('Slit is there');self.play(Indicate(f[2],color=RED,scale_factor=1.03),run_time=.4)
        self.at('When does the');self.play(FadeIn(T(QUESTION_CASES[1][1],34,GOLD).move_to([3.55,-.6,0])),run_time=.4)
        self.finish()
class S06Pause(Scene):
    def construct(self):countdown(self,1)


class S07R1(TimedScene):
    def construct(self):
        self.add(heading('Fly comm'),ledger(['Fly\ncomm','yes','','yes','','']))
        mid,cone,ax=stage(receptors=True);self.add(mid,ax,cone)
        self.at('Too early');self.play(FadeIn(cell('too early',2)),run_time=.4)
        self.at('It is repelled');self.play(cone.animate.shift(RIGHT*1.9),run_time=.4)
        self.play(cone.animate.shift(LEFT*1.3),GrowArrow(push([-.8,.05,0],[-2.8,.05,0])),
            FadeIn(cell('repelled before crossing',4)),run_time=.5)
        self.at('almost no rungs');self.play(FadeIn(ladder('comm')),FadeIn(cell('almost\nno rungs',5)),run_time=.4)
        self.finish()


class S08Q2(TimedScene):
    def construct(self):
        f=question_frame(2,False);self.add(f[0],*f[2:])
        self.at('A fly lacking');self.play(FadeIn(f[1]),run_time=.4)
        self.at('Predict');self.play(FadeIn(T(QUESTION_CASES[2][1],34,GOLD).move_to([3.55,-.6,0])),run_time=.3)
        self.finish()
class S09Pause(Scene):
    def construct(self):countdown(self,2)


class S10R2(TimedScene):
    def construct(self):
        self.add(heading('Fly robo;comm'),ledger(['Fly\nrobo;comm','yes','','','','']))
        mid,cone,ax=stage(x=1.6,receptors=True,weak=True);self.add(mid,ax,cone)
        self.at('Like robo');self.play(FadeIn(cell('like robo',4)),run_time=.3)
        label=receptor_label(cone,'Robo2')
        self.at('is still there');self.play(FadeIn(label),FadeIn(cell('weakly\n(Robo2)',2)),FadeIn(cell('weakly\n(Robo2)',3)),run_time=.4)
        self.at('axons are pushed');self.play(cone.animate.shift(RIGHT*1.2),label.animate.shift(RIGHT*1.2),run_time=.55)
        self.at('some come back');self.play(FadeOut(label),FadeIn(recross(2.8)),cone.animate.shift(LEFT*4.5),FadeIn(cell('some\ncome back',5)),run_time=.7)
        self.finish()


class S11Q3(TimedScene):
    def construct(self):
        f=question_frame(3,False);self.add(f[0],*f[2:])
        self.at('Now');self.play(FadeIn(f[1]),run_time=.4)
        self.at('Can the axon');self.play(FadeIn(T(QUESTION_CASES[3][1],34,GOLD).move_to([3.55,-.6,0])),run_time=.4)
        self.finish()
class S12Pause(Scene):
    def construct(self):countdown(self,3)


class S13R3(TimedScene):
    def construct(self):
        self.add(heading('Comm persists in every neuron'),ledger(['Fly: modest\nComm','yes','','','','']))
        mid,cone,ax=stage(receptors=True,weak=True);self.add(mid,ax,cone)
        self.at('Only weekly');self.play(FadeIn(cell('weakly',2)),FadeIn(cell('weakly',3)),run_time=.4)
        label=receptor_label(cone,'Robo low')
        self.at('is kept low');self.play(FadeIn(label),run_time=.3)
        self.at('axons cross');self.play(FadeOut(label),cone.animate.shift(RIGHT*6.7),run_time=.65)
        self.at('may come back');self.play(FadeIn(recross(2.5)),FadeIn(cell('crosses;\nmay return',4)),run_time=.4)
        self.at('looks like robo');self.play(FadeIn(ladder('robo')),FadeIn(cell('robo-like\nladder',5)),run_time=.4)
        self.finish()


class S14Mouse(TimedScene):
    def construct(self):
        self.add(heading('Mouse: remove the Slit signal'),ledger())
        mid,cone,ax=stage(x=-2.3,slit=False);self.add(mid,ax,cone)
        self.at('With no slits');self.play(FadeIn(cell('Mouse: no\nSlit1, 2, 3',0,color=TEXT)),FadeIn(cell('no',1)),run_time=.4)
        self.at('no slit push');self.play(FadeIn(cell('nothing\nto hear',2)),FadeIn(cell('nothing\nto hear',3)),run_time=.35)
        self.at('so axons stall');self.play(cone.animate.shift(RIGHT*.43),FadeIn(cell('may stall\nor recross',4)),
            FadeIn(T('stall at midline',28,BLUE).move_to([-3.7,-2.05,0])),run_time=.5)
        self.at('or re')
        # Show the alternative on the same shaft: advance across, then return.
        self.play(cone.animate.shift(RIGHT*4.57),
            FadeIn(cell('many stall;\nsome recross',5)),run_time=.4)
        on_shaft=recross(1.8,y=-1.15,end=-3.8)
        on_shaft[-1].move_to([3.6,-2.45,0])
        self.add(Line([-6.1,-1.15,0],[2.7,-1.15,0],color=BLUE,stroke_width=9,stroke_opacity=.35))
        ax.add_updater(lambda m:m.set_opacity(.35))
        self.play(FadeIn(on_shaft),
            cone.animate.shift(LEFT*4.57),run_time=.4)
        self.finish()


class S15Mouse2(TimedScene):
    def construct(self):
        # A fresh ledger, with every old result absent from its first frame.
        self.add(heading('Mouse: remove Robo3'),ledger(['Mouse\nno Robo3','','','','','']))
        mid,cone,ax=stage(receptors=True);self.add(mid,ax,cone)
        self.at('With no');self.play(FadeIn(cell('yes',1)),run_time=.3)
        self.at('axons');self.play(FadeIn(cell('too early',2)),FadeIn(cell('yes',3)),cone.animate.shift(RIGHT*1.8),run_time=.4)
        self.at('almost none cross');self.play(cone.animate.shift(LEFT*1),GrowArrow(push([-.8,.05,0],[-2.8,.05,0])),
            FadeIn(cell('repelled before crossing',4)),FadeIn(cell('almost\nnone cross',5)),run_time=.5)
        self.finish()


TRIPLE=['Mouse: no\nRobo1, 2, 3','yes','no R1/2\nto hear','no R1/2\nto hear','','']

class S16Fail(TimedScene):
    def construct(self):
        self.add(heading('Where the rule fails',GOLD),ledger([TRIPLE[0],'','','','','']))
        self.add(Rectangle(width=12.9,height=1.23,color=GOLD).move_to([0,1.6,0]))
        mid,cone,ax=stage();self.add(mid,ax,cone)
        boxes=VGroup(*[chip(t,c,28).move_to([x,.15,0]) for t,c,x in
            [('Robo1',YELLOW,-4.8),('Robo2',YELLOW,-2.8),('Robo3',ORANGE,3.5)]])
        self.add(boxes)
        self.at('The last row');self.play(Indicate(self.mobjects[2],color=GOLD,scale_factor=1.01),run_time=.4)
        self.at('Remove');self.play(Create(Cross(boxes[0],stroke_color=RED,stroke_width=6)),run_time=.35)
        self.at('Robo two');self.play(Create(Cross(boxes[1],stroke_color=RED,stroke_width=6)),run_time=.35)
        self.at('Robo three');self.play(Create(Cross(boxes[2],stroke_color=RED,stroke_width=6)),run_time=.35)
        self.at('together');self.play(FadeIn(T('No repelling Robo1 or Robo2',28,YELLOW).move_to([3.5,-2.5,0])),run_time=.35)
        self.finish()


class S17Fail2(TimedScene):
    def construct(self):
        self.add(heading('Prediction: remove all three Robos',GOLD),ledger([TRIPLE[0],'','','','','']))
        mid,cone,ax=stage();self.add(mid,ax,cone)
        self.at('The rule predicts');self.play(FadeIn(cell('yes',1)),FadeIn(cell(TRIPLE[2],2)),FadeIn(cell(TRIPLE[3],3)),run_time=.4)
        self.at('some crossing returns');self.play(cone.animate.shift(RIGHT*7),FadeIn(cell('some crossing\nreturns',4)),run_time=.7)
        self.at('because the');self.play(FadeIn(recross(2.8)),FadeIn(T('May then stall\nor recross',28,TEXT).move_to([-3.7,.15,0])),run_time=.45)
        self.at('are gone');self.play(FadeIn(T('Early repulsion\nreceptors gone',28,YELLOW).move_to([3.55,.2,0])),run_time=.35)
        self.finish()


class S18Fail3(TimedScene):
    def construct(self):
        self.add(heading('Observed: crossing returns? ',GOLD),
            T('Mouse: no Robo1, Robo2 or Robo3',28,GOLD).move_to([0,2.55,0]),
            Line([0,2.05,0],[0,-3.45,0],color=GREY))
        # Full-height paired diagrams; same long shaft and left-to-right orientation.
        for cx,name in [(-3.3,'Spinal cord'),(3.3,'Hindbrain precerebellar')]:
            self.add(strip(cx,-2.15,1.3,.55),T(name,30).move_to([cx,1.85,0]),
                T('midline',26,GREY).move_to([cx,-2.55,0]))
        c1=make_cone(-4.9,-.4,2.6);c2=make_cone(1.3,-.4,2.6)
        a1=always_redraw(lambda:Line([-6.1,-.4,0],c1.body.get_center(),color=BLUE,stroke_width=9))
        a2=always_redraw(lambda:Line([.5,-.4,0],c2.body.get_center(),color=BLUE,stroke_width=9))
        self.add(a1,a2,c1,c2)
        self.at('In the spinal cord');self.play(Indicate(c1,scale_factor=1.04),run_time=.35)
        self.at('crossing partly returns');self.play(c1.animate.shift(RIGHT*3),
            FadeIn(VGroup(Rectangle(width=5.8,height=.8,color=GREY),
                T('Observed: partly returns',28,BLUE)).move_to([-3.3,-3.1,0])),run_time=.65)
        # Dashed return follows the existing shaft, behind the crossed cone.
        a1.clear_updaters().set_opacity(.35)
        self.add(DashedLine([-2.8,-.4,0],[-4.8,-.4,0],color=BLUE,stroke_width=5,dash_length=.14),
            push([-4.6,-.4,0],[-4.9,-.4,0],BLUE))
        self.at('In hindbrain');self.play(c2.animate.shift(RIGHT*.18),run_time=.6)
        self.at('it does not');self.play(FadeIn(VGroup(Rectangle(width=5.8,height=.8,color=GREY),
                T('Observed: does not return',28,RED)).move_to([3.3,-3.1,0])),run_time=.4)
        self.finish()


class S19Why(TimedScene):
    def construct(self):
        self.add(heading('Robo3 also strengthens attraction'))
        mid,cone,ax=stage(x=-3.7,full=True);self.add(mid,ax,cone)
        dcc=chip('DCC',GREEN,28).move_to([-2.9,.6,0])
        link=Line([-3.1,.28,0],[-3.1,-.8,0],color=GREEN,stroke_width=3)
        pull=push([-2.65,-1.15,0],[-1.65,-1.15,0],GREEN)
        contrast=T('No Robo3: weaker pull',28,GREEN).move_to([-3.6,1.65,0])
        self.add(dcc,link,pull,contrast)
        r3=chip('Robo3',ORANGE,28).move_to([-4.8,.6,0])
        self.at('must do more');self.play(Indicate(cone,scale_factor=1.05),run_time=.5)
        self.at('It also strengthens');self.play(FadeIn(r3),Create(Line([-4.5,.28,0],[-4,-.85,0],color=ORANGE)),Transform(pull,push([-2.65,-1.15,0],[-.7,-1.15,0],GREEN).set_stroke(width=13)),
            Transform(contrast,T('With Robo3: stronger pull',28,GREEN).move_to([-3.6,1.65,0])),run_time=.6)
        self.at('netrin attraction');self.play(FadeIn(T('netrin attraction',30,GREEN).move_to([-2.6,-2.6,0])),
            Indicate(dcc,scale_factor=1.05),run_time=.4)
        self.at('cannot replace');self.play(FadeIn(T('Removing Robo1 + Robo2\ncannot replace\nthis extra activity',28).move_to([3.55,.15,0])),run_time=.45)
        self.finish()


class S20Attr(TimedScene):
    def construct(self):
        self.add(heading('The rule covers repulsion only'))
        mid,cone,ax=stage(x=2.8,receptors=True,full=True);self.add(mid,ax,cone)
        covered=chip('Slit / Robo: covered',RED,28).move_to([3.55,2.2,0])
        outside=chip('netrin: not covered',GREEN,28).move_to([-3.6,2.2,0])
        self.add(covered,outside)
        self.at('covers repulsion only');self.play(Indicate(covered,scale_factor=1.04),run_time=.4)
        self.at('After crossing');self.play(Indicate(cone,scale_factor=1.07),run_time=.4)
        pull=push([2.8,-1.05,0],[.85,-1.05,0],GREEN)
        rep=push([2.8,-1.05,0],[5,-1.05,0],RED)
        beam=Line([1.2,.55,0],[5.5,.55,0],color=TEXT,stroke_width=5)
        pivot=Triangle(color=GREY,fill_color=GREY,fill_opacity=1).scale(.25).move_to([3.35,.22,0])
        self.at('pull and push');self.play(GrowArrow(pull),GrowArrow(rep),Create(beam),FadeIn(pivot),
            FadeIn(T('netrin pull',28,GREEN).move_to([1.55,-2.3,0])),FadeIn(T('Slit push',28,RED).move_to([5,-2.3,0])),run_time=.5)
        self.at('toward leaving');self.play(beam.animate.rotate(-.2,about_point=[3.35,.55,0]),
            Transform(rep,push([2.8,-1.05,0],[5.8,-1.05,0],RED).set_stroke(width=12)),run_time=.5)
        self.at('How that happens');self.play(FadeIn(T('?',48,GOLD).move_to([3.35,.95,0])),
            FadeIn(T('How the balance tips\nis still being\nworked out',28,TEXT).move_to([-3.5,-2.65,0])),run_time=.45)
        self.finish()


class S22Final(TimedScene):
    def construct(self):
        self.add(heading('What makes the crossing final?'))
        mid,cone,ax=stage(x=2.8,full=True);self.add(mid,ax,cone)
        marks=robo_marks(cone)
        self.at('changes a receptor');self.play(FadeIn(marks),FadeIn(T('receptor changed',30,YELLOW).move_to([3.5,1.8,0])),run_time=.5)
        # An unmistakable closed lock, mounted on the cone; no unanchored arc/dot.
        lock=VGroup(RoundedRectangle(width=.95,height=.72,corner_radius=.1,color=GOLD,fill_color=BG,fill_opacity=1).move_to([2.8,-1.25,0]),
            ArcBetweenPoints([2.46,-.9,0],[3.14,-.9,0],angle=-PI,color=GOLD,stroke_width=5),
            Line([2.8,-1.18,0],[2.8,-1.4,0],color=GOLD,stroke_width=5))
        self.at('keeps the change');self.play(FadeIn(lock),FadeIn(T('change kept',32,GOLD).move_to([3.5,-2.65,0])),run_time=.18)
        self.finish()


class S23FlyMouse(TimedScene):
    def construct(self):
        self.add(heading('Keep the change after crossing'),Line([0,2.55,0],[0,-3.2,0],color=GREY))
        fc=make_cone(-3.9,-.7,3.2);mc=make_cone(2.6,-.7,3.2)
        fr=robo_marks(fc,3.2,.3);mr=robo_marks(mc,3.2,.3);fc.add(fr);mc.add(mr)
        c=chip('Comm',PURPLE,30).move_to([-3.3,1.25,0]);r=chip('Robo3.1',ORANGE,30).move_to([3.3,1.25,0])
        self.add(T('Fly',34).move_to([-3.3,2.35,0]),T('Mouse',34).move_to([3.3,2.35,0]),fc,mc,c,r,
            Line([-6.1,-.7,0],fc.body.get_center(),color=BLUE,stroke_width=9),
            Line([.4,-.7,0],mc.body.get_center(),color=BLUE,stroke_width=9))
        self.at('In flies');self.play(Indicate(fc,scale_factor=1.04),run_time=.3)
        self.at('stops making');self.play(Create(Cross(c,stroke_color=RED)),fr.animate.set_opacity(1),
            FadeIn(T('Comm production OFF',30,TEXT).move_to([-3.3,-2.65,0])),run_time=.5)
        self.at('In mice');self.play(Indicate(mc,scale_factor=1.04),run_time=.3)
        self.at('disappears');self.play(FadeOut(r),mr.animate.set_opacity(1),
            FadeIn(T('Robo1 + Robo2 free',30,YELLOW).move_to([3.3,-2.65,0])),run_time=.5)
        self.finish()


FINAL_ROWS=[
 ['WT\ncommissural','yes','weak','strong','crosses once','crosses once'],
 ['WT\nipsilateral','yes','yes','yes','never crosses','never crosses'],
 ['Fly comm','yes','too early','yes','repelled early','almost no rungs'],
 ['Fly robo;comm','yes','weak\n(Robo2)','weak\n(Robo2)','like robo','some return'],
 ['Fly\nmodest Comm','yes','weak','weak','may return','robo-like\nladder'],
 ['Mouse\nno Slits','no','nothing\nto hear','nothing\nto hear','stall / recross','stall / recross'],
 ['Mouse\nno Robo3','yes','too early','yes','repelled early','almost none\ncross'],
 ['Mouse\nno Robo1–3','yes','no R1/2','no R1/2','crossing\nreturns','cord: partly\nhindbrain: no']]


FINAL_EDGES=[-6.45,-3.65,-2.15,-.5,1.15,3.65,6.45]
TABLE_TOP=2.75
TABLE_HEADER=.8
TABLE_STEP=.7

def row_y(j):
    return TABLE_TOP-TABLE_HEADER-(j+.5)*TABLE_STEP


def completed_ledger():
    g=VGroup();bottom=TABLE_TOP-TABLE_HEADER-8*TABLE_STEP
    for x in FINAL_EDGES:g.add(Line([x,bottom,0],[x,TABLE_TOP,0],color=GREY,stroke_width=1))
    for yy in [TABLE_TOP]+[TABLE_TOP-TABLE_HEADER-j*TABLE_STEP for j in range(9)]:
        g.add(Line([FINAL_EDGES[0],yy,0],[FINAL_EDGES[-1],yy,0],color=GREY,stroke_width=1))
    for k,t in enumerate(HEADS):g.add(cell(t,k,TABLE_TOP-TABLE_HEADER/2,size=28,edges=FINAL_EDGES,line_spacing=0))
    for j,row in enumerate(FINAL_ROWS):
        for k,t in enumerate(row):g.add(cell(t,k,row_y(j),size=28,edges=FINAL_EDGES,line_spacing=0))
    return g


class S24Take(TimedScene):
    def construct(self):
        qs=VGroup(T('Is Slit\nthere?',26,RED),T('Can the axon\nhear it?',26,YELLOW),
            T('When does it\nstart hearing it?',26,BLUE)).arrange(RIGHT,buff=1.4).move_to([0,3.22,0])
        self.add(qs,completed_ledger())
        rect=Rectangle(width=12.9,height=TABLE_STEP,color=GOLD,stroke_width=4).move_to([0,row_y(2),0])
        other=Rectangle(width=12.9,height=TABLE_STEP,color=GOLD,stroke_width=4).move_to([0,row_y(6),0])
        self.at('too hard too early');self.play(Create(rect),Create(other),run_time=.35)
        # A filled blue band replaces the two separated gold outlines.
        weak=Rectangle(width=12.9,height=2*TABLE_STEP,color=BLUE,stroke_width=5,
            fill_color=BLUE,fill_opacity=.12).move_to([0,(row_y(3)+row_y(4))/2,0])
        self.at('One pushed too weakly');self.play(FadeOut(rect),FadeOut(other),
            FadeIn(weak),run_time=.4)
        self.finish()


class S25End(EndCard):
    LINE='Too hard too early, it never crosses.\nToo weak after crossing, it may stall or cross again.'
    def construct(self):
        lines=VGroup(T('Too hard too early, it never crosses.',36,GOLD,font=TITLE_FONT),
            T('Too weak after crossing, it may stall or cross again.',34,BLUE,font=TITLE_FONT)).arrange(DOWN,buff=.7)
        lines.move_to([0,.35,0])
        self.add(lines,T('biochemistrypedia.com',26,TEAL).move_to([0,-1.8,0]));self.finish()
