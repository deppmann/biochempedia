"""Chapter 1: The Cue Marks the Place — reviewed fix round.
COLOR MAP: TEAL growth cones; YELLOW cue/protein; RED pain/temperature;
BLUE muscle stretch; GREY anatomy and membranes; TEXT labels; GOLD emphasis.
All axon paths and cone fans are schematic anatomy, not measured traces.
No quantitative plots or molecular structures are drawn.
"""
import numpy as np
from bp_style import *

# Use the actual word onset, not the default anticipatory lead. Log AFTER
# waiting so the audit records the time at which a visual really starts.
class SpokenScene(SpokenScene):
    def at(self, phrase, lead=0, nth=0):
        target = self.t_of(phrase, nth)
        self._last_cue = target
        if target - self.elapsed() > .02:
            self.wait(target - self.elapsed())
        with open('/tmp/semaphorins-fix-cues.log', 'a') as f:
            f.write(f'{os.environ["KX_SCENE_ID"]} {phrase!r}: target={target:.2f} actual={self.elapsed():.2f}\n')

    def finish(self):
        # Preserve the final named result for at least two readable seconds.
        end = max(self.narration_s + .4, getattr(self, '_last_cue', 0) + 2.5)
        if end > self.elapsed():
            self.wait(end-self.elapsed())


def label(s, x=0, y=0, size=30, color=TEXT):
    return T(s, size, color).move_to([x,y,0])


def heading(s):
    return label(s, y=3.2, size=34)


def cone(x=0, y=0, r=1.6, collapsed=False):
    # Fan with radiating filopodia; always the same cartoon at every scale.
    base = np.array([x-.65*r,y,0])
    a = .07 if collapsed else .87
    pts = [base+[0,.12*r,0]] + [base+r*np.array([np.cos(t),np.sin(t),0]) for t in np.linspace(a,-a,17)] + [base+[0,-.12*r,0]]
    shaft = Line(base+[-1.05*r,0,0],base,color=TEAL,stroke_width=7)
    body = Polygon(*pts,color=TEAL,fill_color=TEAL,fill_opacity=.32,stroke_width=3)
    hairs = VGroup(*[Line(base+r*np.array([np.cos(t),np.sin(t),0]),base+(r+.17*r)*np.array([np.cos(t),np.sin(t),0]),color=TEAL,stroke_width=2) for t in np.linspace(-a,a,7)]) if not collapsed else VGroup()
    return VGroup(shaft,body,hairs)


def cue_dots(points):
    return VGroup(*[Dot([x,y,0],radius=.075,color=YELLOW) for x,y in points])


def spinal():
    # Centred, six-unit-high section. Ventral shading follows the real ellipse.
    cx,cy,rx,ry=0,.15,2.8,3.0
    outline=Ellipse(width=2*rx,height=2*ry,color=GREY,fill_opacity=.08).move_to([cx,cy,0])
    horns=Polygon(*[[x,y+cy,0] for x,y in [(-1.55,2),(-.55,.6),(.55,.6),(1.55,2),(1.1,.1),(1.65,-1.8),(.55,-1),(-.55,-1),(-1.65,-1.8),(-1.1,.1)]],color=GREY,fill_opacity=.18)
    dorsal=label('dorsal horn',4.65,2.1,size=36,color=TEXT)
    ventral=label('ventral horn',4.65,-2.35,size=36,color=TEXT)
    leaders=VGroup(Line([3.15,2.1,0],[1.55,2.1,0],color=GREY),Line([3.1,-2.35,0],[1.65,-1.65,0],color=GREY))
    anatomy=VGroup(outline,horns,dorsal,ventral,leaders)
    motor=VGroup(Dot([1,-1.4,0],radius=.16,color=TEXT),Line([1.2,-1.4,0],[3.2,-.95,0],color=TEXT),label('motor neurons',4.65,-.95,size=34,color=TEXT))
    red=VMobject(color=RED,stroke_width=5).set_points_as_corners([[-4.3,1.55,0],[-2.15,1.55,0],[-1.5,1.55,0],[-1.25,1.3,0]])
    red=VGroup(red,Dot([-1.25,1.3,0],radius=.14,color=RED))
    blue=VMobject(color=BLUE,stroke_width=10).set_points_smoothly([[-4.3,1.1,0],[-2,1.1,0],[-.45,.7,0],[.15,-.4,0],[1,-1.4,0]])
    lower=[np.array([cx+rx*np.cos(t),cy+ry*np.sin(t),0]) for t in np.linspace(np.pi,2*np.pi,65)]
    wall=Polygon(*lower,color=YELLOW,fill_color=YELLOW,fill_opacity=.19,stroke_width=2)
    return anatomy,motor,red,blue,wall


POSITIONS=[(-2.25,1.05),(2.45,1.05),(-2.25,-1.25),(2.45,-1.25)]
def dish():
    rim=Ellipse(width=11.2,height=5.65,color=GREY,fill_opacity=.055).move_to([0,-.15,0])
    cs=VGroup(*[cone(x,y,1.05) for x,y in POSITIONS])
    return rim,cs


def membranes():
    return VGroup(*[Rectangle(width=.3,height=.13,color=GREY,fill_opacity=.85).move_to([x,y,0]) for x,y in [(-3.25,1.65),(.1,1.7),(3.25,1.65),(-.3,-.25),(3.9,-.35),(-3.6,-.4)]])


def question_frame():
    rim,cs=dish()
    mem=membranes()
    VGroup(rim,cs,mem).scale(.8).shift(DOWN*.65)
    q1=label('Any membrane?',y=3.15,size=46)
    q2=label('What molecule?',y=2.12,size=46)
    return rim,cs,q1,q2,mem


def rule_card():
    box=RoundedRectangle(width=12.5,height=5.6,corner_radius=.2,color=GOLD,fill_opacity=.045)
    a=label('The cue marks the place.',y=1.1,size=52,color=YELLOW)
    b=label('The growth cone decides\nwhat it means.',y=-.85,size=50,color=TEAL)
    return box,a,b


def rule_rows(n=3, compact=False):
    # Identical left alignment on all questions and all answers.
    data=[('Answers at all?','Needs the receptor'),('Which way?','Internal state: e.g. cyclic GMP'),('Turn or collapse?','Depends on assay conditions')]
    rows=VGroup()
    for i,(q,a) in enumerate(data[:n]):
        y=(3.15-i*.7) if compact else (2.3-i*1.05)
        h=.62 if compact else .94
        box=RoundedRectangle(width=12.2,height=h,corner_radius=.12,color=GREY,fill_opacity=.04).move_to([0,y,0])
        qt=label(q,size=28).move_to([-5.75,y,0],aligned_edge=LEFT)
        ans=label(a,size=27,color=TEAL).move_to([-.9,y,0],aligned_edge=LEFT)
        rows.add(VGroup(box,qt,ans))
    return rows


def receptor_demo():
    gc=cone(.1,-1.0,2.65)
    # Large open socket seated on the upper cone surface, with an inward stem.
    socket=VMobject(color=TEXT,stroke_width=8).set_points_as_corners([
        [.05,1.18,0],[.05,.62,0],[.8,.62,0],[.8,1.18,0]])
    stem=Line([.425,.62,0],[.425,.05,0],color=TEXT,stroke_width=8)
    name=label('receptor',2.55,1.0,size=34)
    leader=Line([1.55,1.0,0],[.9,.9,0],color=TEXT,stroke_width=2)
    return gc,VGroup(socket,stem,name,leader)


class S00Title(TitleCard):
    LESSON='Semaphorins and Repulsion'
    TITLE='The Cue Marks the Place'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',y=2.0,size=28,color=TEAL),label(self.LESSON,y=1.15,size=30))
        title=label(self.TITLE,y=-.1,size=48)
        self.play(FadeIn(title),Create(Line([-2,-1,0],[2,-1,0],color=GOLD)),run_time=.6)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        anatomy,motor,red,blue,wall=spinal()
        self.add(anatomy)
        r=Line([-4.3,1.55,0],[-2.2,1.55,0],color=RED,stroke_width=5)
        b=Line([-4.3,1.1,0],[-2.2,1.1,0],color=BLUE,stroke_width=10)
        self.at('Two kinds of sensory')
        self.play(Create(r),Create(b),run_time=1.5)
        self.at('One kind stops')
        self.play(ReplacementTransform(r,red),run_time=.7)
        self.at('The other runs')
        self.play(ReplacementTransform(b,blue),FadeIn(motor),run_time=.8)
        self.at('What sorts them')
        self.play(FadeIn(label('What sorts them?',y=-3.3,size=40)),run_time=.3)
        self.finish()


class S02Classes(SpokenScene):
    def construct(self):
        ganglion=RoundedRectangle(width=12,height=5.85,corner_radius=.7,color=GREY,fill_opacity=.04).move_to([0,-.2,0])
        self.add(ganglion,heading('Dorsal root ganglion'))
        red=VGroup(Circle(1.05,color=RED,fill_opacity=.3).move_to([-3,-.15,0]),Line([-1.95,-.15,0],[-.4,-.15,0],color=RED,stroke_width=5))
        blue=VGroup(Circle(1.4,color=BLUE,fill_opacity=.3).move_to([2.65,-.15,0]),Line([4.05,-.15,0],[5.4,-.15,0],color=BLUE,stroke_width=10))
        self.at('The ones that stop')
        self.play(FadeIn(red),run_time=.5)
        self.at('pain and temperature')
        self.play(FadeIn(label('pain + temperature',-3,1.9,30,RED)),run_time=.25)
        self.at('nerve growth factor')
        self.play(FadeIn(VGroup(chip('NGF',RED,30),chip('TrkA',RED,30)).arrange(RIGHT,buff=.35).move_to([-3,-2.35,0])),run_time=.35)
        self.at('The ones that go on')
        self.play(FadeIn(blue),run_time=.5)
        self.at('muscle stretch')
        self.play(FadeIn(label('muscle stretch',2.65,1.9,30,BLUE)),run_time=.25)
        self.at('neurotrophin')
        self.play(FadeIn(VGroup(chip('NT-3',BLUE,30),chip('TrkC',BLUE,30)).arrange(RIGHT,buff=.35).move_to([2.65,-2.35,0])),run_time=.35)
        self.finish()


class S03Wall(SpokenScene):
    def construct(self):
        anatomy,motor,r,b,wall=spinal()
        self.add(anatomy,motor)
        self.at('The ventral cord')
        self.play(FadeIn(wall),run_time=.6)
        self.at('inhibits sensory axon growth')
        words=label('ventral cord:\nreleases an inhibitor\nof sensory axon growth',-4.5,-1.25,27,YELLOW)
        self.play(FadeIn(words),Create(VMobject(color=YELLOW).set_points_as_corners([[-4.4,-2.05,0],[-4.4,-2.3,0],[-1.7,-2.3,0]])),run_time=.5)
        self.at('walls as well as roads')
        self.play(Indicate(wall,color=YELLOW,scale_factor=1),run_time=1)
        self.finish()


class S04Assay(SpokenScene):
    def construct(self):
        rim,cs=dish()
        title=heading('The collapse assay')
        culture=label('Chick sensory neurons on laminin',y=-3.35,size=28)
        citation=label('Raper and Kapfhammer, 1990',y=3.2,size=28)
        self.add(rim,title)
        self.at('To find a wall')
        self.play(Create(cs),run_time=1.4)
        self.at('grew chick')
        self.play(FadeOut(title),FadeIn(citation),FadeIn(culture),Indicate(cs,scale_factor=1.015),run_time=.6)
        self.at('Then they added')
        # Nothing added until the named membrane suspension.
        self.at('membranes from')
        mem=membranes()
        self.play(FadeIn(mem),run_time=.25)
        self.at('embryonic brain')
        self.play(Indicate(mem,scale_factor=1),
            Transform(citation,label('Brain membranes',y=3.2,size=30)),
            Transform(culture,label('Raper and Kapfhammer, 1990',y=-3.35,size=28)),
            Create(Arrow([1.8,2.95,0],[.15,1.95,0],color=TEXT,buff=.15)),run_time=.4)
        self.finish()


class S05Collapse(SpokenScene):
    def construct(self):
        rim,cs=dish();mem=membranes()
        title=heading('The collapse assay')
        self.add(rim,cs,mem,title)
        self.at('Within minutes')
        timer=label('within minutes',-3.6,-3.35,28)
        self.play(FadeIn(timer),run_time=.25)
        self.at('folded into thin tips')
        self.play(*[Transform(cs[i],cone(x,y,1.05,True)) for i,(x,y) in enumerate(POSITIONS[:3])],run_time=.9)
        self.at('That is collapse')
        text=label('collapse',y=3.2,size=32,color=TEAL)
        self.play(FadeOut(title),FadeIn(text),run_time=.25)
        self.at('The fraction that collapsed')
        count=label('3 of 4 collapsed',2.25,-3.35,30,TEAL)
        self.play(FadeIn(count),run_time=.25)
        self.at('Remove the membranes')
        wash=VGroup(*[Arrow([-5,y,0],[5,y,0],buff=0,color=BLUE,stroke_width=3) for y in [.45,-.6]])
        wash_label=label('wash out',y=3.2,size=30,color=BLUE)
        self.play(FadeOut(text),FadeIn(wash_label),Create(wash),mem.animate.shift(RIGHT*.65).set_opacity(0),run_time=.7)
        self.at('the effect reverses')
        self.play(FadeOut(wash),FadeOut(count),*[Transform(cs[i],cone(x,y,1.05)) for i,(x,y) in enumerate(POSITIONS[:3])],run_time=.65)
        self.play(FadeIn(label('reversible',2.25,-3.35,30,TEAL)),run_time=.2)
        # Keep the wash label through recovery so a three-second sample catches it.
        self.wait(2.0)
        self.play(FadeOut(wash_label),run_time=.2)
        self.finish()


class S06Q(SpokenScene):
    def construct(self):
        rim,cs,q1,q2,mem=question_frame();self.add(rim,cs,mem)
        self.at('Would any membrane')
        self.play(FadeIn(q1),run_time=.3)
        self.at('And what kind')
        self.play(FadeIn(q2),run_time=.3)
        self.finish()


class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(*question_frame());self.wait(5)


def control_plate(x,y,title,collapsed=False):
    rim=Ellipse(width=2.65,height=3.6,color=GREY,fill_opacity=.06).move_to([x,y,0])
    gc=cone(x+.45,y,1.02,collapsed)
    mem=VGroup(*[Rectangle(width=.22,height=.11,color=GREY,fill_opacity=.9).move_to([x+dx,y+dy,0]) for dx,dy in [(-.7,1.2),(.35,1.35),(.65,-1.2),(-.65,-1.2)]])
    return VGroup(rim,gc,mem,label(title,x,y+2.08,28))


class S08Reveal(SpokenScene):
    def construct(self):
        self.add(heading('Which membranes cause collapse?'))
        # Positive control retained from the preceding brain-membrane assay.
        brain=control_plate(-4.55,-.1,'Brain',True)
        self.add(brain,label('collapse',-4.55,-2.25,28,TEAL))
        liver=control_plate(-1.5,-.1,'Liver')
        fibro=control_plate(1.5,-.1,'Fibroblasts')
        treated=control_plate(4.55,-.1,'Brain')
        self.at('Membranes from liver')
        self.play(FadeIn(liver),run_time=.3)
        self.at('fibroblasts')
        self.play(FadeIn(fibro),run_time=.3)
        self.at('did not cause collapse')
        stays=label('stay spread',0,-2.25,28,TEAL)
        self.play(FadeIn(stays),run_time=.25)
        self.at('Heat and trypsin')
        treatment=label('Heat / trypsin',4.55,2.6,27,YELLOW)
        self.play(FadeIn(treated),FadeIn(treatment),run_time=.35)
        self.at('destroyed the activity')
        self.play(FadeIn(label('stays spread',4.55,-2.25,28,TEAL)),run_time=.25)
        self.at('a protein')
        self.play(FadeIn(chip('A protein',YELLOW,36).move_to([0,-3.15,0])),run_time=.3)
        self.finish()


class S09Collapsin(SpokenScene):
    def construct(self):
        self.add(heading('Purifying the inhibitor'),label('Luo, Raible and Raper, 1993',y=-3.2,size=30))
        # A deliberately abstract soft-edged glyph, no structural interpretation.
        pts=[[(2.7+.22*np.cos(3*t))*np.cos(t),(2.15+.18*np.sin(5*t))*np.sin(t),0] for t in np.linspace(0,TAU,60)]
        blob=VMobject(color=YELLOW,fill_color=YELLOW,fill_opacity=.23).set_points_smoothly(pts).close_path()
        self.at("Raper's group purified")
        self.play(GrowFromCenter(blob),FadeIn(label('about 100 kilodaltons',y=-2.55,size=30,color=YELLOW)),run_time=.65)
        self.at('Collapsin')
        name=label('collapsin',size=46,color=YELLOW)
        self.play(FadeIn(name),run_time=.3)
        self.at('called')
        self.play(Transform(name,label('Sema3A',size=46,color=YELLOW)),run_time=.45)
        self.at('a semaphorin')
        self.play(FadeIn(label('a semaphorin',y=-.95,size=30,color=YELLOW)),run_time=.3)
        self.finish()


def retina_frame(collapsed=True):
    cs=VGroup(cone(-2.65,-.1,2.35),cone(3.8,-.1,2.35,collapsed))
    dots=cue_dots([(x,y) for x in [-5.45,-3.9,-2.3,-.8,1,2.55,4.15,5.65] for y in [-2.35,2.15]])
    labs=VGroup(label('retinal growth cone',-3.15,3,30,TEAL),label('sensory growth cone',3.15,3,30,TEAL),label('collapsin / Sema3A',y=-3.5,size=30,color=YELLOW),label('did not respond',-3.15,-2.8,28,TEAL))
    return cs,dots,labs


class S10Retina(SpokenScene):
    def construct(self):
        cs,dots,labs=retina_frame(False)
        self.add(cs,dots,labs[2])
        self.at('Then came a first clue')
        self.play(Indicate(cs[0],scale_factor=1.02),run_time=.5)
        self.at('from the retina')
        self.play(FadeIn(labs[0]),run_time=.25)
        self.at('did not respond')
        self.play(FadeIn(labs[3]),FadeIn(labs[1]),Transform(cs[1],cone(3.8,-.1,2.35,True)),run_time=.7)
        self.finish()


class S11Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(*retina_frame());self.wait(2)


class S12Rule(SpokenScene):
    def construct(self):
        box,a,b=rule_card()
        previous=VGroup(*retina_frame())
        self.add(previous)
        self.at('Here is the idea')
        self.at('The cue marks')
        self.play(FadeOut(previous),FadeIn(box),FadeIn(a),FadeIn(heading('The rule to carry through')),run_time=.35)
        self.at('The growth cone decides')
        self.play(FadeIn(b),run_time=.4)
        # Eight full seconds with BOTH lines readable; narration unchanged.
        self.wait(8)
        self.finish()


class S13Hear(SpokenScene):
    def construct(self):
        rows=rule_rows(1,compact=True).shift(DOWN*.5);gc,rec=receptor_demo()
        self.add(heading('The growth cone’s answer'),gc)
        self.at('Does a growth cone')
        self.play(FadeIn(rows[0][:2]),run_time=.3)
        self.at('it needs the receptor')
        self.play(FadeIn(rec),FadeIn(rows[0][2]),run_time=.4)
        self.finish()


class S14Sign(SpokenScene):
    def construct(self):
        rows=rule_rows(2,compact=True).shift(DOWN*.5);gc,rec=receptor_demo()
        self.add(heading('The growth cone’s answer'),rows[0],gc,rec)
        self.at('Which way does')
        self.play(FadeIn(rows[1][:2]),run_time=.3)
        self.at('depends on its internal')
        self.play(FadeIn(rows[1][2]),gc[1].animate.set_fill(TEAL,opacity=.65),run_time=.4)
        self.finish()


class S15Layout(SpokenScene):
    def construct(self):
        rows=rule_rows(compact=True).shift(DOWN*.5);gc,rec=receptor_demo()
        title=heading('The growth cone’s answer')
        self.add(title,rows[:2],gc,rec)
        self.at('does it turn')
        self.play(FadeOut(gc),FadeOut(rec),FadeIn(rows[2][:2]),run_time=.3)
        self.at('In typical assays')
        compact=rule_rows(compact=True)
        self.play(FadeOut(title),ReplacementTransform(rows[:2],compact[:2]),ReplacementTransform(rows[2][:2],compact[2][:2]),FadeIn(compact[2][2]),run_time=.4)
        subtitle=label('Typical outcomes under assay conditions',y=1.03,size=28)
        self.play(FadeIn(subtitle),run_time=.25)
        left=cone(0,0,2.1).move_to([-3.1,-.9,0])
        right=cone(0,0,2.1).move_to([3.1,-.9,0])
        # Density increases toward the upper edge, above the left cone.
        grad=cue_dots([(-5.5+i*(4.8/max(n-1,1)),.05+j*.18) for j,n in enumerate([2,4,9,17]) for i in range(n)])
        self.at('a gradient from one side')
        self.play(FadeIn(left),FadeIn(grad),run_time=.3)
        self.at('turns it away')
        turned=left.copy().rotate(-.4).move_to([-3.1,-.9,0])
        self.play(Transform(left,turned),FadeIn(label('gradient: turns away',-3.15,-2.65,27)),run_time=.65)
        around=cue_dots([(3.1+2.5*np.cos(a),-.8+1.5*np.sin(a)) for a in np.linspace(0,TAU,18,endpoint=False)])
        self.at('A high dose all round')
        self.play(FadeIn(right),FadeIn(around),run_time=.35)
        self.at('can fold it up')
        self.play(Transform(right,cone(0,0,2.1,True).move_to([3.1,-.9,0])),run_time=.7)
        self.at('where the preparation')
        self.play(FadeIn(label('where collapse is supported',3.1,-2.65,26)),run_time=.3)
        # Accumulate the final factors on their own spoken word onsets.
        for phrase,s,x in [('Lay out','Layout',-4.7),('dose','dose',-2),('exposure','exposure',.65),('the cell','cell',3.45)]:
            self.at(phrase, nth=1 if phrase == 'dose' else 0)
            self.play(FadeIn(chip(s,TEXT,30).move_to([x,-3.35,0])),run_time=.2)
        self.finish()


class S16Limits(SpokenScene):
    def construct(self):
        self.add(heading('The growth cone’s answer'),rule_rows())
        self.at('The rule has limits')
        self.play(FadeIn(label('The rule has limits',y=-.85,size=34,color=YELLOW)),run_time=.3)
        for phrase,s,x in [('which cue is made','Which cue',-3.8),('where','Where',0),('how much','How much',3.8)]:
            self.at(phrase)
            self.play(FadeIn(chip(s,YELLOW,30).move_to([x,-1.9,0])),run_time=.25)
        self.at('other cues share')
        self.play(FadeIn(label('In the cord, other cues share the work.',y=-3.1,size=32)),run_time=.35)
        self.finish()


class S17Takeaway(SpokenScene):
    def construct(self):
        anatomy,motor,red,blue,wall=spinal()
        self.add(anatomy,motor)
        self.at('Back to the two axons')
        self.play(Create(red),Create(blue),run_time=1)
        self.at('One wall')
        cue=label('ventral cord cue\n(Sema3A)',-4.45,-1.5,29,YELLOW)
        self.play(FadeIn(wall),FadeIn(cue),Create(Line([-2.8,-1.5,0],[-1.65,-1.5,0],color=YELLOW)),run_time=.5)
        self.at('the same cue stops')
        turn=VMobject(color=RED,stroke_width=5).set_points_as_corners([[-4.3,1.55,0],[-2.1,1.55,0],[-1.25,.75,0],[-.7,.15,0]])
        stopped=VGroup(turn,Line([-.92,.15,0],[-.48,.15,0],color=RED,stroke_width=9))
        self.play(Transform(red,stopped),run_time=.7)
        self.at('barely affects the other')
        self.play(Indicate(blue,color=BLUE,scale_factor=1.02),FadeIn(label('Same cue, two answers.',y=-3.35,size=40)),run_time=.5)
        self.finish()


class S18End(EndCard):
    LINE='The cue marks the place; the growth cone decides what it means.'
    def construct(self):
        self.add(*rule_card())
        self.play(FadeIn(label('biochemistrypedia.com',y=-3.2,size=28,color=TEAL)),run_time=.4)
        self.finish()
