"""Chapter 1: Three Questions, Not One.
COLOR MAP: RED = P2ry1-labelled subset / stopped breathing;
YELLOW = Npy2r-labelled subset / fast shallow breathing;
TEAL = optogenetic drive; BLUE = necessity test; PINK = unanswered question;
GREY = anatomy / unlabelled fibres; TEXT = GPR65-labelled cells;
GOLD = transient GPR65 response, never a breathing subset.
All plotted traces are computed qualitative models, never experimental data.
"""
import numpy as np
from bp_style import *
PINK = "#E58BC4"
LESSON = "Vagal Sensory Neurons: The Body Reports to the Brain"


def label(s, x, y, size=28, color=TEXT):
    # Explicitly centre separate lines, with generous consistent leading.
    lines = VGroup(*[T(t, size=size, color=color) for t in s.split('\n')])
    return lines.arrange(DOWN, buff=.14).move_to([x,y,0])


def arr(a,b,color=GREY):
    return Arrow(a,b,buff=.08,color=color,stroke_width=5,tip_length=.23)


def cell(x,y,color=TEXT,r=.23):
    return VGroup(Circle(r,color=color,fill_opacity=.18).move_to([x,y,0]),
                  Line([x+r,y,0],[x+r+.48,y,0],color=color,stroke_width=3))


def mouse(x=0,y=0,s=1):
    # A geometric mouse silhouette, no anatomical or molecular detail implied.
    g=VGroup(Ellipse(width=2.4,height=1.25,color=GREY,fill_opacity=.12),
             Circle(.48,color=GREY,fill_opacity=.12).move_to([1.1,.3,0]),
             Circle(.26,color=GREY,fill_opacity=.12).move_to([.95,.85,0]),
             Dot([1.3,.4,0],radius=.045,color=TEXT),
             Line([-1.15,-.1,0],[-1.9,.4,0],color=GREY),
             Line([-.6,-.58,0],[-.75,-.8,0],color=GREY),
             Line([.65,-.58,0],[.85,-.8,0],color=GREY))
    return g.scale(s).move_to([x,y,0])


def hopper(x,y):
    return VGroup(Polygon([x-.5,y+.7,0],[x+.5,y+.7,0],[x+.3,y-.5,0],
                          [x-.3,y-.5,0],color=GREY,fill_opacity=.12),
                  VGroup(*[Dot([x+d,y+.2,0],radius=.07,color=TEXT) for d in [-.22,0,.22]]))



def body_route(fibres=False):
    m=mouse(.8,-2.05,1.3)
    brain=RoundedRectangle(width=1.7,height=.8,corner_radius=.24,color=GREY,fill_opacity=.15).move_to([.3,2.55,0])
    bl=label('brainstem',2.5,2.55,28)
    # The stub starts inside the torso and joins the ascending nerve.
    stub=Line([.3,-2.05,0],[.3,-.9,0],color=GREY,stroke_width=10)
    if fibres:
        cable=VGroup(stub,*[arr([.3+d,-.9,0],[.3+d,2.1,0],GREY) for d in [-.27,0,.27]])
    else:
        cable=VGroup(stub,Line([.3,-.9,0],[.3,2.1,0],color=GREY,stroke_width=20))
    return VGroup(m,brain,bl,cable)


def breathing(x0,w,y,t_light=4,amp1=.02,per1=2,color=TEXT,amp0=.8):
    # Reference oscillator: phase += 2*pi*dt/period; displacement=A*sin(phase).
    pts=[]; phase=0.; prev=0.
    for t in np.linspace(0,8.5,501):
        amp,per=(amp0,2.) if t<t_light else (amp1,per1)
        phase+=2*np.pi*(t-prev)/per; prev=t
        pts.append([x0+w*t/8.5,y+amp*np.sin(phase),0])
    return VMobject(color=color,stroke_width=4).set_points_as_corners(pts)


def nerve(active=None):
    tube=RoundedRectangle(width=11.6,height=1.6,corner_radius=.35,color=GREY,fill_opacity=.08).move_to([0,1.5,0])
    fibres=VGroup(*[Line([-5.5,1.5+d,0],[5.5,1.5+d,0],color=GREY,stroke_width=7) for d in [-.5,0,.5]])
    if active is not None: fibres[active].set_color(RED if active==0 else YELLOW)
    light=VGroup(Line([-1,3.2,0],[-1,2.5,0],color=TEAL,stroke_width=7),
                 Polygon([-1,2.5,0],[-1.8,.7,0],[-.2,.7,0],stroke_width=0,fill_color=TEAL,fill_opacity=.18),
                 label('light on',.45,2.95,28,TEAL))
    return VGroup(tube,fibres,light)


def light_frame(second=False):
    return VGroup(nerve(2 if second else 0),
        breathing(-5.7,11.4,-1.15,amp1=.23 if second else .02,per1=.8 if second else 2,color=YELLOW if second else RED),
        label('breathing • schematic model',0,-2.5,28),
        label('fast and shallow' if second else 'stops',3.7,-.05,28,YELLOW if second else RED))


def channel(x=0,y=0):
    return VGroup(Line([x-.8,y,0],[x-.28,y,0],color=GREY,stroke_width=10),
                  Line([x+.28,y,0],[x+.8,y,0],color=GREY,stroke_width=10),
                  RoundedRectangle(width=.23,height=.95,corner_radius=.07,color=GREY).move_to([x-.22,y,0]),
                  RoundedRectangle(width=.23,height=.95,corner_radius=.07,color=GREY).move_to([x+.22,y,0]))


def columns(stage=3, compact=False, answered=False):
    g=VGroup()
    for i,x in enumerate([-4.3,0,4.3]):
        box=RoundedRectangle(width=3.8,height=2.7 if compact else 4.65,corner_radius=.15,color=GREY,stroke_width=2).move_to([x,1.45 if compact else .65,0])
        title=['Stimulus','Channel','Output'][i]+('' if answered else '?') if i<stage else '?'
        head=label(title,x,2.35,32,PINK)
        head.align_to(label('Stimulus?',x,2.35,32,PINK),UP)
        g.add(VGroup(box,head))
    return g


def col_icons(stage=3):
    g=VGroup()
    if stage>=2: g.add(channel(0,.7))
    if stage>=3:
        g.add(breathing(2.85,2.9,1.05,t_light=10,amp0=.3),hopper(4.3,-.5).scale(.65))
    return g


def grip_cloud(attached=True):
    # Solid handgrip with four finger loops and straps attached to the cell cloud.
    grip=VGroup(RoundedRectangle(width=2.8,height=.3,corner_radius=.14,color=TEXT,
                                fill_color=TEXT,fill_opacity=1).move_to([-3.35,2.12,0]),
                *[Circle(.22,color=TEXT,stroke_width=5).move_to([x,1.78,0])
                  for x in [-4.1,-3.6,-3.1,-2.6]],
                Line([-4.6,2.05,0],[-4.6,.65,0],color=TEXT,stroke_width=5),
                Line([-2.1,2.05,0],[-2.1,.65,0],color=TEXT,stroke_width=5))
    cloud=VGroup(Ellipse(width=5,height=3.5,color=TEXT,fill_opacity=.035).move_to([-3.35,-.85,0]))
    for x,y in [(-4.8,-.45),(-3.4,-.1),(-2.05,-.45),(-4.5,-1.5),(-3.1,-1.25),(-1.8,-1.55)]:
        cloud.add(cell(x,y,r=.27))
    cloud.add(label('labelled cells',-3.35,-2.15,28))
    if not attached: grip.shift(UP*.45)
    return VGroup(grip,cloud)


def question_rows():
    rows=VGroup()
    for y,t in zip([2.05,0,-2.05],['Stimulus?','Channel?','Output?']):
        rows.add(VGroup(RoundedRectangle(width=5,height=1.65,corner_radius=.15,color=GREY).move_to([3.65,y,0]),
                        label(t,3.65,y+.4,30,PINK)))
    return rows


def handle_frame(name=False, marks=0):
    g=VGroup(grip_cloud(),question_rows(),label('Cre line • genetic label',-3.35,3.15,28))
    if name: g.add(chip('receptor / channel name',color=TEXT,size=26).move_to([-3.35,-3.05,0]))
    for y in [2.05,0,-2.05][:marks]: g.add(label('not established',3.65,y-.3,28,PINK))
    return g


def unasked_channel(c):
    # This case tests food response and outputs; channel causality is left open.
    c[1][0]=DashedVMobject(c[1][0],num_dashes=32).set_opacity(.35)
    c[1][1].set_color(GREY).set_opacity(.5)
    return c


def channel_status(y=.6):
    return label('Route not\nestablished',0,y,26,GREY).set_opacity(.65)


def case_board(output=False,compact=False):
    g=unasked_channel(columns(compact=compact,answered=True))
    g.add(label('GPR65-labelled afferents',0,3.3,30))
    g.add(label('Food in the\nintestine',-4.3,1.15 if compact else .8,28),
          channel_status(1.15 if compact else .6))
    if output:
        g.add(label('Gastric contractions\nsuppressed',4.3,1.6 if compact else 1.15,26),
              label('anaesthetized mouse',4.3,.8 if compact else .3,26))
    return g


def feeding_mouse():
    return VGroup(mouse(-1.7,-1.65,1.2),hopper(1.1,-1.65).scale(1.3),
                  label('?',1.1,-.3,44,PINK),label('awake mouse',-1.7,-3.05,28))


def prediction():
    return VGroup(case_board(True,True),feeding_mouse(),label('Satiety?',-4.6,-.65,32,PINK),
                  label('Feeding: ?',4.3,-.65,30,PINK),label('How much will it eat?',3.9,-2.3,28,PINK))


def summary_base():
    g=unasked_channel(columns(answered=True))
    g.add(label('GPR65-labelled cells • three measurements',0,3.3,30),
          channel_status())
    return g


def summary_results():
    return VGroup(label('Food response\nYES',-4.3,.65,30),
        label('Gastric suppression\nYES',4.3,1.3,27),
        Line([2.7,.55,0],[5.9,.55,0],color=GREY),
        label('Feeding\nno measurable\nchange\n(assays tested)',4.3,-.45,26))


def summary():
    return VGroup(summary_base(),summary_results())


def evidence_base():
    c=columns(); c[1][0].set_color(PINK)
    return VGroup(c,label('stimulus evidence',-4.3,.6,26),label('still open',0,.6,30,PINK),label('output evidence',4.3,.6,26))


def evidence_links():
    return VGroup(*[VGroup(arr([x,-1.75,0],[x,-2.45,0],TEXT),label('own evidence',x,-2.75,26)) for x in [-4.3,0,4.3]])


class S00Title(TitleCard):
    LESSON=LESSON
    TITLE='Three Questions, Not One'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.25,26,TEAL),label('Vagal Sensory Neurons:\nThe Body Reports to the Brain',0,.9,28))
        self.play(FadeIn(label(self.TITLE,0,-.65,46)),run_time=.65)
        self.add(Line([-1.2,-1.5,0],[1.2,-1.5,0],color=GOLD,stroke_width=4))
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        route=body_route(); self.add(route)
        self.at('running from the body')
        self.play(ShowPassingFlash(route[3].copy().set_stroke(color=TEXT,width=22)),run_time=.8)
        self.at('Does it carry')
        self.play(FadeIn(label('One message,\nor many?',-3.8,.8,36,PINK)),run_time=.45)
        self.finish()


class S02Afferent(SpokenScene):
    def construct(self):
        r=body_route(); self.add(r)
        self.at('carries signals')
        f=body_route(True)[3]
        self.play(ReplacementTransform(r[3],f),run_time=.55)
        self.at('toward the brain')
        self.play(ShowPassingFlash(f.copy().set_color(TEXT)),run_time=.6)
        self.at('is called an')
        self.play(FadeIn(label('afferent',-3.7,.9,40)),FadeIn(label('body → brain',-3.7,0,28)),run_time=.4)
        self.finish()


class S03Intero(SpokenScene):
    def construct(self):
        r=body_route(True).shift(LEFT*2.9); self.add(r)
        # Three pre-drawn organ cartoons have separate label lanes.
        lung=VGroup(*[Ellipse(width=.65,height=1.15,color=GREY).move_to([1.5+d,1.55,0]) for d in [-.4,.4]],Line([1.5,2.45,0],[1.5,1.65,0],color=GREY))
        artery=VGroup(RoundedRectangle(width=1.9,height=.65,corner_radius=.2,color=GREY).move_to([1.5,-.05,0]),
                      VMobject(color=TEXT).set_points_as_corners([[.75,-.05,0],[1.1,-.05,0],[1.3,.18,0],[1.5,-.25,0],[1.7,-.05,0],[2.25,-.05,0]]))
        gut=VMobject(color=GREY,fill_opacity=.12).set_points_smoothly([[1.25,-1.2,0],[1.25,-1.65,0],[.85,-2,0],[1,-2.6,0],[2,-2.65,0],[2.35,-2.1,0],[2.2,-1.6,0],[1.7,-1.7,0],[1.65,-1.2,0]])
        organs=VGroup(VGroup(lung,label('lung volume',4.25,1.6,28)),VGroup(artery,label('blood pressure',4.25,-.05,28)),VGroup(gut,label('gut fullness',4.25,-2.05,28))).set_opacity(.3)
        self.add(organs)
        self.at('internal state')
        self.play(FadeIn(label('interoception',0,3.15,34)),run_time=.35)
        for cue,i in [('Lung volume',0),('blood pressure',1),('how full',2)]:
            self.at(cue); self.play(organs[i].animate.set_opacity(1).set_color(TEXT),run_time=.3)
        self.finish()


class S04Light1(SpokenScene):
    def construct(self):
        n=nerve(); tr=breathing(-5.7,11.4,-1.15,t_light=10)
        self.add(n[:2],tr,label('breathing • schematic model',0,-2.5,28))
        self.at('Light on one set')
        self.play(FadeIn(n[2]),n[1][0].animate.set_color(RED),run_time=.45)
        self.at('stops an')
        self.play(Transform(tr,breathing(-5.7,11.4,-1.15,color=RED)),FadeIn(label('stops',3.7,-.05,28,RED)),run_time=.5)
        self.at('mouse breathing')
        self.play(FadeIn(label('anaesthetized mouse',0,-3.2,28)),run_time=.25)
        self.finish()


class S05Light2(SpokenScene):
    def construct(self):
        f=light_frame(); self.add(f,label('anaesthetized mouse',0,-3.2,28))
        self.at('Light on another set')
        self.play(f[0][1][0].animate.set_color(GREY),f[0][1][2].animate.set_color(YELLOW),
                  Transform(f[1],breathing(-5.7,11.4,-1.15,t_light=10,color=GREY)),FadeOut(f[3]),run_time=.4)
        self.at('makes it breathe')
        self.play(Transform(f[1],breathing(-5.7,11.4,-1.15,amp1=.23,per1=.8,color=YELLOW)),FadeIn(label('fast and shallow',3.7,-.05,28,YELLOW)),run_time=.6)
        self.finish()


class S06Notone(SpokenScene):
    def construct(self):
        cable=Line([-5.7,2,0],[5.7,2,0],color=GREY,stroke_width=24)
        a=breathing(-5.8,5.1,-.8,color=RED); b=breathing(.7,5.1,-.8,amp1=.23,per1=.8,color=YELLOW)
        self.add(cable,a,b,label('stops',-3.25,-2.1,30,RED),label('fast and shallow',3.25,-2.1,30,YELLOW),label('schematic models • anaesthetized mouse',0,-3.2,26))
        fibres=VGroup(Line([-5.7,2.3,0],[5.7,2.3,0],color=YELLOW,stroke_width=7),Line([-5.7,2,0],[5.7,2,0],color=GREY,stroke_width=5),Line([-5.7,1.7,0],[5.7,1.7,0],color=RED,stroke_width=7))
        self.at('two subsets')
        self.play(ReplacementTransform(cable,fibres),run_time=.6)
        self.at('separate lines')
        self.play(GrowArrow(arr([-3.25,1.65,0],[-3.25,.2,0],RED)),GrowArrow(arr([3.25,2.35,0],[3.25,.2,0],YELLOW)),run_time=.5)
        self.finish()


class S08Col1(SpokenScene):
    def construct(self):
        c=columns(0); self.add(c)
        self.at('three questions')
        self.play(LaggedStart(*[Indicate(x[0],color=PINK) for x in c],lag_ratio=.12),run_time=.8)
        self.at('what stimulus')
        self.play(Transform(c[0][1],label('Stimulus?',-4.3,2.35,32,PINK)),run_time=.4)
        self.finish()


class S09Col2(SpokenScene):
    def construct(self):
        c=columns(1); self.add(c)
        self.at('Second')
        self.play(FadeIn(channel(0,.7)),run_time=.45)
        self.at('electrical current')
        self.play(Transform(c[1][1],label('Channel?',0,2.35,32,PINK)),GrowArrow(arr([0,1.6,0],[0,-.45,0],TEXT)),run_time=.45)
        self.finish()


class S10Col3(SpokenScene):
    def construct(self):
        c=columns(2); self.add(c,col_icons(2))
        self.at('Third')
        self.play(FadeIn(col_icons(3)[1:]),run_time=.4)
        self.at('what changes')
        self.play(Transform(c[2][1],label('Output?',4.3,2.35,32,PINK).align_to(label('Stimulus?',4.3,2.35,32,PINK),UP)),run_time=.4)
        self.finish()


class S11Suff(SpokenScene):
    def construct(self):
        c=columns(); icons=col_icons(); c[1][0].set_stroke(opacity=.22); c[1][1].set_opacity(.22); icons[0].set_stroke(opacity=.22)
        self.add(c,icons); c[2][0].set_color(TEXT)
        drive=VGroup(label('sufficiency • drive it',3.6,-2.65,28,TEAL),
                     arr([4.3,-2.22,0],[4.3,-.55,0],TEAL))
        remove=VGroup(label('necessity • remove it',3.65,3.35,28,BLUE),
                      arr([6.55,2.9,0],[5.35,1.05,0],BLUE))
        self.at('driving a population'); self.play(FadeIn(drive),run_time=.55)
        self.at('removing it'); self.play(FadeIn(remove),run_time=.55)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        b=evidence_base(); self.add(b)
        links=evidence_links()
        self.at('Each question')
        self.play(LaggedStart(*[FadeIn(x) for x in links],lag_ratio=.35),run_time=1.7)
        self.at('Some stay open')
        self.play(b[0][1][0].animate.set_stroke(width=5),Indicate(b[2],color=PINK,scale_factor=1.06),run_time=.6)
        self.at('An answer to one')
        self.play(FadeIn(label('Separate evidence • no answer transfers across',0,3.35,28,PINK)),run_time=.4)
        self.finish()


class S13Beat1(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(evidence_base(),evidence_links(),label('Separate evidence • no answer transfers across',0,3.35,28,PINK))
        self.wait(3)


class S14Handle(SpokenScene):
    def construct(self):
        h=grip_cloud(False); rows=question_rows()
        self.add(h[1],rows)
        self.at('How do researchers')
        self.play(FadeIn(h[0]),run_time=.6)
        self.at('With a genetic label')
        self.play(h[0].animate.shift(DOWN*.45),h[1].animate.set_color(TEXT),run_time=.6)
        self.at('usually a')
        self.play(FadeIn(label('Cre line • genetic label',-3.35,3.15,28)),run_time=.35)
        self.finish()


class S16Handle3(SpokenScene):
    def construct(self):
        f=handle_frame()
        for row in f[1]:
            row[0].set_stroke(opacity=.35); row[1].set_opacity(.35)
        self.add(f)
        self.at('A label is a handle')
        self.play(f[0].animate.shift(UP*.5),run_time=1.25)
        self.at('on a population')
        self.play(Indicate(f[0][0],color=TEXT,scale_factor=1.06),run_time=.55)
        self.at('it answers none')
        self.play(*[row[1].animate.set_opacity(.5) for row in f[1]],run_time=.5)
        self.finish()


class S17Handle4(SpokenScene):
    def construct(self):
        f=handle_frame(); self.add(f)
        self.at('a receptor or channel')
        self.play(FadeIn(chip('receptor / channel name',color=TEXT,size=26).move_to([-3.35,-3.05,0])),run_time=.45)
        # Arrows start outside the cloud; the name remains beside its cells.
        for cue,y in [('the natural stimulus',2.05),("the protein's causal role",0),('or the output',-2.05)]:
            self.at(cue)
            self.play(GrowArrow(arr([-.55,y,0],[1.05,y,0],PINK)),FadeIn(label('not established',3.65,y-.3,28,PINK)),run_time=.4)
        self.finish()


class S18Beat2(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(handle_frame(True,3),*[arr([-.55,y,0],[1.05,y,0],PINK) for y in [2.05,0,-2.05]])
        self.wait(3)


class S19Case(SpokenScene):
    def construct(self):
        # Continuous epithelial boundary: villi project into the labelled lumen.
        pts=[[-5.9,-2.1,0]]
        for x in [-4.7,-2.3,.1]:
            pts += [[x-.65,-2.1,0],[x-.65,.95,0]]
            pts += [[x+.65*np.cos(t),.95+.65*np.sin(t),0] for t in np.linspace(PI,0,30)]
            pts += [[x+.65,-2.1,0]]
        pts += [[1.5,-2.1,0]]
        wall=VMobject(color=GREY,stroke_width=5).set_points_as_corners(pts)
        self.add(wall,label('intestinal lumen',-2.3,2.9,30),label('villus',-4.7,-2.85,28),
                 Line([-4.7,-2.55,0],[-4.7,-1.5,0],color=GREY))
        box=VGroup(RoundedRectangle(width=3.8,height=4.8,corner_radius=.15,color=GREY).move_to([4.3,.25,0]),label('Stimulus',4.3,2.1,32,PINK))
        self.add(box)
        terminal=VGroup(Line([-2.3,-2.8,0],[-2.3,1,0],color=TEXT,stroke_width=6),Dot([-2.3,1,0],radius=.2,color=TEXT))
        self.at('afferents')
        self.play(Create(terminal),FadeIn(label('GPR65-labelled terminal',-2.2,-3.25,28)),run_time=.5)
        food=VGroup(*[Dot([x,.8,0],radius=.15,color=GOLD) for x in [-3.5,-1.1,1.3]])
        self.at('answer food')
        self.play(FadeIn(food),run_time=.2)
        self.play(food.animate.shift(DOWN*.45),terminal.animate.set_color(GOLD).set_stroke(width=10),
                  Flash([-2.3,1,0],color=GOLD,line_length=.25,flash_radius=.38),
                  run_time=.65)
        self.at('in the intestine')
        self.play(FadeIn(label('Food in the\nintestine',4.3,.45,30)),run_time=.35)
        self.finish()


class S20Case2(SpokenScene):
    def construct(self):
        self.add(case_board())
        tr=breathing(2.7,3.2,-.65,t_light=10,amp0=.35)
        self.add(tr,label('gastric contractions\nschematic model',4.3,-2.6,26))
        self.at('with light')
        self.play(FadeIn(label('light drive',4.3,-1.35,26,TEAL)),run_time=.3)
        self.at('suppressed stomach contractions')
        self.play(Transform(tr,breathing(2.7,3.2,-.65,amp0=.35,color=TEAL)),FadeIn(label('Gastric contractions\nsuppressed',4.3,1.15,26)),run_time=.5)
        self.at('in an')
        self.play(FadeIn(label('anaesthetized mouse',4.3,.3,26)),run_time=.25)
        self.finish()


class S21Predict(SpokenScene):
    def construct(self):
        self.add(case_board(True,True))
        self.at('This looks like')
        self.play(FadeIn(label('Satiety?',-4.6,-.65,32,PINK)),run_time=.35)
        self.at('In an awake mouse')
        self.play(FadeIn(feeding_mouse()),run_time=.5)
        self.at('what should driving')
        self.play(FadeIn(label('Feeding: ?',4.3,-.65,30,PINK)),FadeIn(label('How much will it eat?',3.9,-2.3,28,PINK)),run_time=.4)
        self.finish()


class S22Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(prediction()); self.wait(5)


class S23Reveal(SpokenScene):
    def construct(self):
        # Equal model I(t)=r*t, r=1 arbitrary unit. Dashed control is wider
        # than the teal centre stroke, so both identical model traces remain visible.
        axes=VGroup(Line([-4.8,-2.05,0],[4.8,-2.05,0],color=GREY),Line([-4.8,-2.05,0],[-4.8,2.65,0],color=GREY))
        yl=label('cumulative food eaten (schematic)',0,0,26).rotate(PI/2).move_to([-5.55,.3,0])
        self.add(axes,yl,label('time',4.6,-2.4,26),label('no numerical scale',-2.9,-2.4,26,GREY))
        p=np.array([[-4.8+8.4*t,-2.05+3.7*t,0] for t in np.linspace(0,1,160)])
        control=DashedVMobject(VMobject(color=GREY,stroke_width=13).set_points_as_corners(p),num_dashes=23,dashed_ratio=.65)
        driven=VMobject(color=TEAL,stroke_width=4).set_points_as_corners(p)
        self.at('In the assays tested',lead=0)
        self.play(Create(control),Create(driven),run_time=1.2,rate_func=linear)
        self.add(label('control',5.1,1.98,26,GREY),label('light drive',5.1,1.3,26,TEAL),
                 Line([3.6,1.98,0],[4.05,1.98,0],color=GREY),Line([3.6,1.3,0],[4.05,1.3,0],color=TEAL))
        self.at('driving them')
        self.play(FadeIn(VGroup(mouse(-3.1,3,.36),label('control',-1.45,3,26,GREY),mouse(.65,3,.36),label('light drive',2.55,3,26,TEAL))),run_time=.3)
        self.at('did not measurably')
        self.play(FadeIn(label('No measurable change in intake in these assays',0,-3.15,28)),run_time=.35)
        self.finish()


class S24Reveal2(SpokenScene):
    def construct(self):
        self.add(summary_base())
        results=summary_results()
        self.at('Yes to the stimulus'); self.play(FadeIn(results[0]),run_time=.4)
        self.at('yes to one output'); self.play(FadeIn(results[1]),Create(results[2]),run_time=.4)
        self.at('no to another'); self.play(FadeIn(results[3]),run_time=.4)
        self.finish()


class S26Scope(SpokenScene):
    def construct(self):
        self.add(summary())
        band=RoundedRectangle(width=12.4,height=1.1,corner_radius=.15,color=GREY,fill_opacity=.09).move_to([0,-2.75,0])
        words=VGroup()
        for t,x in zip(['organ','age','assay','anaesthetic state'],[-4.5,-1.5,1.5,4.5]):
            # An invisible common descender fixes all four labels to one baseline.
            word=T(t+' g',size=24)
            word[-1].set_opacity(0)
            word.shift(RIGHT*(x-word[:-1].get_center()[0]))
            word.shift(UP*(-2.9-word[-1].get_bottom()[1]))
            words.add(word)
        dim_words=words.copy().set_opacity(.4)
        for word in dim_words: word[-1].set_opacity(0)
        self.add(band,dim_words)
        for cue,i in [('the organ',0),('age',1),('assay',2),('anesthetic state',3)]:
            self.at(cue); self.play(FadeIn(words[i]),run_time=.22)
        self.finish()


class S27Take(SpokenScene):
    def construct(self):
        f=handle_frame(); self.add(f)
        # Small question icons keep the unknowns concrete without filling an answer.
        icons=VGroup(VGroup(*[Dot([3.65+dx,1.73+dy,0],radius=.1,color=GOLD) for dx,dy in [(-.28,0),(0,.16),(.28,0),(-.14,-.23),(.17,-.24)]]),channel(3.65,-.35).scale(.45),breathing(2.6,2.1,-2.4,t_light=10,amp0=.15,color=GREY))
        self.add(icons)
        for y in [2.05,0,-2.05]:
            self.add(arr([-.55,y,0],[1.23,y,0],PINK),label('?',.35,y+.35,26,PINK))
        for cue,i in [('Stimulus',0),('channel',1),('output',2)]:
            self.at(cue,lead=0); self.play(Indicate(f[1][i][1],color=TEXT,scale_factor=1.22),run_time=.28)
        self.at('A handle alone')
        self.play(FadeIn(label('Three questions. Separate evidence.',0,-3.2,30)),run_time=.4)
        self.finish()


class S28End(EndCard):
    LINE='A handle alone answers none of the three questions.'
