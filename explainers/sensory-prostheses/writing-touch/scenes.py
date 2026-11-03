"""Writing Touch: Addresses, Then Patterns.

COLOR MAP (shared verbatim in meaning with ../scenes.old.py):
BLUE hardware; YELLOW current and stimulation; TEAL information/pattern;
PURPLE #B58CD9 neurons/cortex; GREEN participant meeting an endpoint;
ORANGE #F29E4C zoom; RED caution/is-not; TEXT percepts/people;
GREY outlines and labels. CHAPTERS.md is read-only under TASK.md's edit scope.

Plots use Hobbs et al. 2025, doi:10.1088/1741-2552/adc2d4,
Methods 2.4–2.5 and Results 3.1 (PMC13571258). No invented ratings:
s13 shows categorical outcomes for all 28 electrodes, grouped by result,
not individual choice-score magnitudes. Charge comparison is qualitative,
explicitly schematic: no unsupported participant-specific numerical values.
Hand fields and cortex are explicitly schematic, not anatomical measurements.

FACT-CHECK LOG (RECHECK item 3; checked 2026-11-03):
https://pmc.ncbi.nlm.nih.gov/articles/PMC13571258/ section 3.1, figure 2:
28 electrodes total; 9 significantly favored biomimetic, 3 favored linear.
The remaining 28 - 9 - 3 = 16 had no significant preference (reported as
57%); 9 / 28 = 32% rounded. Thus all three displayed categories are sourced.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'

# Use separately centered lines for multiline cards and annotations.
_style_text = T

def T(text, size=30, color=TEXT, font=FONT, **kw):
    if '\n' not in text:
        return _style_text(text,size,color,font=font,**kw)
    kw.pop('should_center',None)
    spacing=kw.pop('line_spacing',1.0)
    lines=VGroup(*[(_style_text(line,size,color,font=font,**kw) if line else
                    Rectangle(width=.01,height=.25,stroke_opacity=0,fill_opacity=0))
                   for line in text.split('\n')])
    return lines.arrange(DOWN,buff=.22*spacing)


# Reused model helpers from the earlier film.
def poly(points, color, fill=0.0, w=3, fill_color=None):
    m = VMobject()
    m.set_points_as_corners([np.array([x, y, 0.]) for x, y in points])
    return m.set_stroke(color, w).set_fill(fill_color or color, fill)


def contact(x, y, size=.36, color=BLUE):
    return Square(side_length=size, stroke_color=color, stroke_width=3,
                  fill_color=color, fill_opacity=.55).move_to([x, y, 0])


def arr(a, b, color=GREY, w=5, tip=.22):
    return Arrow(a, b, buff=.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=.45,
                 max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=.14, width=c[0].width, height=c[0].height,
                            stroke_width=0, fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def heading(text):
    return T(text, 32).move_to([0, 3.12, 0])


def foot(text):
    return T(text, 26, GREY).move_to([0, -3.35, 0])


def hand(x=3.35, y=0, scale=1):
    # Polygonal hand cartoon, wrist through thumb and four separate fingers.
    pts=[(-.9,-2.25),(-1,-.7),(-1.6,.25),(-1.7,.7),(-1.4,.88),
         (-.9,.3),(-.85,1.85),(-.7,2.13),(-.43,2.13),(-.33,1.86),
         (-.3,.8),(-.22,2.5),(-.05,2.72),(.2,2.72),(.32,2.45),(.35,.85),
         (.45,2.15),(.6,2.35),(.83,2.35),(.95,2.1),(.95,.65),
         (1.05,1.55),(1.22,1.72),(1.44,1.65),(1.53,1.42),
         (1.35,-.5),(.95,-1.25),(.9,-2.25),(-.9,-2.25)]
    return poly(pts,GREY,.08,3).scale(scale).shift([x,y,0])


def cortex():
    return RoundedRectangle(width=1.65,height=4.85,corner_radius=.4,color=PURPLE,
                            fill_color=PURPLE,fill_opacity=.18).move_to([-3.7,-.1,0])


def electrodes():
    return VGroup(*[contact(-3.98+i*.56,y,.36) for y in (-.8,-.1,.6) for i in range(2)])


def fields():
    return VGroup(*[Ellipse(width=1.1,height=1.25,color=TEXT,fill_color=TEXT,
                           fill_opacity=.25,stroke_width=2).move_to([x,y,0])
                    for x,y in ((2.95,-.2),(3.45,.05),(3.92,.3))])


def map_base():
    return VGroup(cortex(),hand(3.4,-.15,1.12),
                  T('sensory cortex',29,PURPLE).move_to([-3.7,2.85,0]),
                  T('felt in the hand',29).move_to([3.4,3.15,0]),
                  foot('Hand fields · schematic'))


def timers(compact=False):
    panels=VGroup()
    for x,name,value in ((-3.15,'without feedback','20.9 s'),(3.15,'with touch feedback','10.2 s')):
        cy,h,ly,ny=(1.8,1.85,2.27,1.55) if compact else (.25,4.7,1.7,.15)
        box=RoundedRectangle(width=5.55,height=h,corner_radius=.22,color=GREY,
                             fill_color=GREY,fill_opacity=.07).move_to([x,cy,0])
        label=T(name,28,BLUE if x>0 else GREY).move_to([x,ly,0])
        num=M(value,44 if compact else 88).move_to([x,ny,0])
        panels.add(VGroup(box,label,num))
    return panels


def predict_frame():
    return VGroup(heading('By what percentage did task time fall?'),timers(),
                  bchip('? %',TEXT,58).move_to([4.6,-2.95,0]),
                  T('Choose your baseline first.',30,YELLOW).move_to([-1.3,-2.95,0]))


def rule_box(second=False):
    first=T('Map the fields.\nTest what can be told apart.',43,line_spacing=1.15,
            should_center=True).move_to([0,1.05,0])
    box=RoundedRectangle(width=11.8,height=2.25,corner_radius=.25,color=TEAL,
                         fill_color=TEAL,fill_opacity=.08).move_to(first)
    g=VGroup(box,first)
    if second:
        g.add(T('Send each group of neurons\nthe right pattern.',44,TEAL,
                line_spacing=1.15,should_center=True).move_to([0,-1.55,0]))
    return g


class S00Title(TitleCard):
    LESSON='Restoring Senses: Implants, Prostheses and Optogenetic Vision'
    TITLE='Writing Touch: Addresses, Then Patterns'

    def construct(self):
        brand=T('BIOCHEMISTRYPEDIA',26,TEAL).move_to([0,2.5,0])
        lesson=T('Restoring Senses: Implants, Prostheses\nand Optogenetic Vision',27,GREY,
                 should_center=True).move_to([0,1.3,0])
        title=T('Writing Touch:\nAddresses, Then Patterns',49,font=TITLE_FONT,
                should_center=True).move_to([0,-.5,0])
        rule=Line([-1.2,-2.2,0],[1.2,-2.2,0],color=GOLD,stroke_width=4)
        self.add(brand,lesson)
        self.play(FadeIn(title),Create(rule),run_time=.6)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        base=map_base()
        base[3].become(T('touch in a hand?',29).move_to([3.4,3.15,0]))
        self.add(base)
        q=T('?',140,YELLOW).move_to([0,.1,0])
        self.at('Can stimulating')
        self.play(FadeIn(q),run_time=.35)
        self.at('And does it help')
        self.play(ReplacementTransform(base[4],T('Does it help?',36).move_to([0,-3.2,0])),run_time=.35)
        self.finish()


class S02Address(SpokenScene):
    def construct(self):
        base=map_base(); es=electrodes(); f=fields()[0]
        base[4].become(foot('Flesher and colleagues, 2016 · schematic'))
        self.add(base)
        scope=T('One man\nspinal cord injury',29,should_center=True).move_to([0,1.8,0])
        self.at('In one man')
        self.play(FadeIn(scope),run_time=.35)
        self.at('electrodes in sensory cortex',lead=.45)
        self.play(FadeIn(es),run_time=.3)
        link=arr(es[3].get_right(),f.get_left(),YELLOW)
        self.at('evoked sensations',lead=.35)
        self.play(es[3].animate.set_color(YELLOW),GrowArrow(link),
                  FadeIn(f.set_fill(TEXT,.7)),run_time=.4)
        self.at('felt in the hand')
        self.play(Indicate(f,color=YELLOW,scale_factor=1.08),run_time=.35)
        self.finish()


class S03Field(SpokenScene):
    def construct(self):
        base=map_base(); es=electrodes(); fs=fields()
        self.add(base,es)
        link=arr(es[3].get_right(),fs[0].get_left(),YELLOW)
        self.at('A responsive electrode')
        self.play(es[3].animate.set_color(YELLOW),run_time=.3)
        self.at('evokes touch')
        self.play(GrowArrow(link),FadeIn(fs[0]),run_time=.4)
        label=VGroup(T('projected field',30).move_to([0,1.7,0]),
                     Line([1.5,1.5,0],[2.7,.45,0],color=GREY,stroke_width=2))
        self.at('its projected field')
        self.play(FadeIn(label),run_time=.3)
        self.at('Fields can overlap')
        self.play(es[3].animate.set_color(BLUE),es[5].animate.set_color(YELLOW),
                  Transform(link,arr(es[5].get_right(),fs[1].get_left(),YELLOW)),FadeIn(fs[1]),run_time=.35)
        # A third electrode addresses a third, overlapping region before amplitude varies.
        self.play(es[5].animate.set_color(BLUE),es[1].animate.set_color(YELLOW),
                  Transform(link,arr(es[1].get_right(),fs[2].get_left(),YELLOW)),FadeIn(fs[2]),run_time=.35)
        rail=Line([-.8,-2.2,0],[-.8,-.5,0],color=GREY)
        level=Rectangle(width=.38,height=.5,color=YELLOW,fill_opacity=.85).move_to([-.8,-1.95,0])
        barlabel=T('amplitude',27,YELLOW).move_to([.2,-2.65,0])
        branch=poly([(-3.24,-.8),(-2.3,-.8),(-2.3,-1.95),(-1.05,-1.95)],YELLOW,w=3)
        self.at('change with stimulation')
        self.play(FadeIn(rail),FadeIn(level),FadeIn(barlabel),Create(branch),run_time=.3)
        self.play(Transform(level,Rectangle(width=.38,height=1.7,color=YELLOW,fill_opacity=.9).move_to([-.8,-1.35,0])),
                  fs[2].animate.scale(1.5).set_fill(TEXT,.8),run_time=.65)
        self.at('So each electrode')
        self.play(FadeOut(label),ReplacementTransform(base[4],
                  T('Projected field = approximate address',32).move_to([0,-3.3,0])),run_time=.35)
        self.finish()


class S04Feedback(SpokenScene):
    def construct(self):
        self.add(heading('Does feedback help a task?'))
        upper=poly([(.5,1.65),(.85,1.95),(2.95,.35),(2.6,-.05),(.5,1.65)],BLUE,.28,4)
        lower=poly([(2.6,.35),(2.95,.45),(3.8,-.9),(3.4,-1.15),(2.6,.35)],BLUE,.28,4)
        joints=VGroup(*[Circle(radius=.28,color=BLUE,fill_color=BG,fill_opacity=1).move_to(pos)
                         for pos in ((.7,1.75,0),(2.75,.25,0),(3.6,-1,0))])
        palm=RoundedRectangle(width=1.8,height=.45,corner_radius=.1,color=BLUE,
                               fill_color=BLUE,fill_opacity=.35).move_to([3.6,-1.2,0])
        left=poly([(2.65,-1.2),(2.65,-2.25),(2.9,-2.25)],BLUE,w=8)
        right=poly([(4.55,-1.2),(4.55,-2.25),(4.3,-2.25)],BLUE,w=8)
        arm=VGroup(upper,lower,joints,palm,left,right)
        block=Square(side_length=.9,color=TEXT,fill_color=TEXT,fill_opacity=.2).move_to([3.6,-1.95,0])
        motor=bchip('motor cortex',PURPLE,32).move_to([-3.9,1.65,0])
        sensory=bchip('sensory cortex',PURPLE,32).move_to([-3.9,-1.9,0])
        drive=Arrow(motor.get_right(),joints[0].get_center(),buff=0,
                    color=YELLOW,stroke_width=5,tip_length=.22)
        feedback=arr(block.get_left(),sensory.get_right(),YELLOW)
        feedback_label=T('touch feedback',30,YELLOW).move_to([-.1,-2.7,0])
        VGroup(arm,block,motor,sensory,drive,feedback,feedback_label).scale(
            1.15,about_point=np.array([0,-.35,0]))
        self.add(arm,block,motor,drive)
        self.at('Does feedback')
        self.play(FadeIn(sensory),GrowArrow(feedback),
                  FadeIn(feedback_label),run_time=.45)
        self.at('The same man moved')
        self.play(left.animate.shift(RIGHT*.25),right.animate.shift(LEFT*.25),run_time=.3)
        self.play(arm.animate.shift(UP*.25),block.animate.shift(UP*.25),
                  drive.animate.put_start_and_end_on(drive.get_start(),drive.get_end()+UP*.25),
                  feedback.animate.put_start_and_end_on(feedback.get_start()+UP*.25,feedback.get_end()),
                  run_time=.35)
        # Finished loop holds for more than three seconds, including the decoding clause.
        self.finish()


class S05Times(SpokenScene):
    def construct(self):
        ts=timers()
        dials=VGroup()
        for x in (-3.15,3.15):
            dial=VGroup(Circle(radius=1.05,color=GREY),
                        Line([x,.15,0],[x,.95,0],color=GREY),
                        Line([x,.15,0],[x+.6,-.2,0],color=GREY))
            dial[0].move_to([x,.15,0]);dials.add(dial)
        self.add(heading('Median task time · one participant'),
                 foot('Flesher and colleagues, 2021'),ts[0][0],ts[1][0],ts[1][1],dials)
        self.at('With touch feedback')
        self.play(Indicate(ts[1][0],color=BLUE,scale_factor=1.02),run_time=.35)
        self.at('fell from')
        self.play(FadeOut(dials[0]),FadeIn(ts[0][1]),FadeIn(ts[0][2]),run_time=.35)
        self.at('to')
        self.play(FadeOut(dials[1]),FadeIn(ts[1][2]),run_time=.35)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        frame=predict_frame();self.add(frame[1])
        self.at('Predict')
        self.play(FadeIn(frame[2]),run_time=.3)
        self.at('By what percentage')
        self.play(FadeIn(frame[0]),run_time=.3)
        self.at('Choose your baseline')
        self.play(FadeIn(frame[3]),run_time=.3)
        self.play(*[Indicate(p[0],color=YELLOW,scale_factor=1.025) for p in frame[1]],run_time=.8)
        self.finish()


class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        frame=predict_frame();self.add(frame)
        # Keep the requested silent thinking pause still.
        self.wait(5)


class S08Reveal(SpokenScene):
    def construct(self):
        ts=timers(compact=True)
        ts[0][0].set_stroke(YELLOW,4)
        self.add(ts,T('baseline',27,YELLOW).move_to([-3.15,.65,0]))
        difference=M('20.9 − 10.2 = 10.7 s',40).move_to([0,-.25,0])
        fraction=M('10.7 / 20.9 × 100',40).move_to([0,-1.35,0])
        answer=bchip('51.2 %',TEXT,52).move_to([0,-2.75,0])
        self.at('About')
        self.play(FadeIn(difference),run_time=.25)
        self.play(FadeIn(fraction),run_time=.25)
        self.play(FadeIn(answer),run_time=.3)
        self.at('measured against')
        self.play(Indicate(ts[0][0],color=YELLOW,scale_factor=1.025),run_time=.45)
        self.at('The working is on screen')
        self.play(Indicate(fraction,color=YELLOW,scale_factor=1.02),run_time=.4)
        self.finish()


class S09Scope(SpokenScene):
    def construct(self):
        ts=timers();self.add(ts,heading('One participant · medians'))
        self.at('But these are')
        self.play(*[Indicate(p[2],color=TEXT,scale_factor=1.02) for p in ts],run_time=.4)
        self.at('They show feedback helped him')
        self.play(FadeIn(T('Feedback helped him.',40).move_to([0,-2.6,0])),run_time=.35)
        self.at('not a population effect')
        self.play(FadeIn(T('Not a population effect.',35,RED).move_to([0,-3.35,0])),run_time=.35)
        self.finish()


class S10Valle(SpokenScene):
    def construct(self):
        h=hand(1,-.45,1.08)
        es=VGroup(*[contact(-4.1,y,.46) for y in (1.0,.0,-1.0)])
        fs=VGroup(*[Ellipse(width=.78,height=.95,color=TEXT,fill_color=TEXT,
                           fill_opacity=.08).move_to([x,0,0]) for x in (.05,.9,1.75)])
        self.add(heading('Patterns across addresses'),h,es,
                 T('electrodes',28,BLUE).move_to([-4.1,2.15,0]),
                 foot('Valle and colleagues, 2025 · Two people · schematic'))
        self.at('Patterns across addresses')
        self.play(FadeIn(fs),run_time=.4)
        self.at('several electrodes stimulated together')
        self.play(es.animate.set_color(YELLOW),fs.animate.set_fill(TEXT,.7),run_time=.4)
        edge=Rectangle(width=2.7,height=.2,color=TEXT,fill_opacity=1).move_to([.9,0,0])
        edge_label=T('edge',36).move_to([4.6,.4,0])
        leader=Line([3.8,.3,0],[2.35,.1,0],color=TEXT)
        self.at('a tactile edge')
        self.play(FadeIn(edge),FadeIn(edge_label),Create(leader),run_time=.35)
        motion=T('apparent\nmotion',34,should_center=True).move_to([4.7,-.65,0])
        pointer=arr([-.3,1.0,0],[.4,1.,0],TEXT)
        self.at('Sequences evoked apparent motion')
        self.play(FadeOut(edge),FadeOut(edge_label),FadeOut(leader),
                  es.animate.set_color(BLUE),fs.animate.set_fill(TEXT,.08),run_time=.2)
        self.play(FadeIn(motion),run_time=.2)
        self.add(pointer)
        for i in range(3):
            animations=[es[i].animate.set_color(YELLOW),fs[i].animate.set_fill(TEXT,.85),
                        pointer.animate.move_to([fs[i].get_x(),.9,0])]
            if i:
                animations += [es[i-1].animate.set_color(BLUE),fs[i-1].animate.set_fill(TEXT,.08)]
            self.play(*animations,run_time=.45)
        self.finish()


class S11Second(SpokenScene):
    def construct(self):
        box=rule_box();self.add(heading('Addresses, then patterns'),box)
        self.at('This is the second half')
        self.play(Indicate(box[0],color=TEAL,scale_factor=1.02),run_time=.35)
        self.at('Send each group')
        self.play(FadeIn(rule_box(True)[2]),run_time=.4)
        self.finish()


def pulse_plot(x,biomimetic):
    # Hobbs simple train: 80/40/80 uA for 0.2/0.6/0.2 s. Fixed 250 Hz.
    # Non-biomimetic amplitude follows 0.2-s ramp, 0.6-s plateau, 0.2-s ramp.
    # Each train is normalized to its own peak; every fifth pulse is drawn.
    origin=np.array([x-2.05,-2.35,0]);width=4.1;height=4.15
    axes=VGroup(Line(origin,origin+[width+.1,0,0],color=GREY),
                Line(origin,origin+[0,height+.15,0],color=GREY))
    pulses=VGroup()
    for t in np.arange(0,1,.004)[::5]:
        amp=(1. if t<.2 or t>=.8 else .5) if biomimetic else .025+.975*min(t/.2,1.,(1-t)/.2)
        xx=origin+np.array([width*t,0,0])
        pulses.add(Line(xx,xx+[0,height*amp,0],color=TEAL if biomimetic else GREY,stroke_width=2))
    title=T('Biomimetic' if biomimetic else 'Non-biomimetic',29,TEAL if biomimetic else GREY).move_to([x,2.95,0])
    ticks=VGroup()
    for yy,label in ((height,'peak'),(height*.5,'lower')):
        pos=origin+np.array([0,yy,0])
        ticks.add(Line(pos+LEFT*.08,pos+RIGHT*.08,color=GREY),
                  T(label,26,GREY).next_to(pos,LEFT,buff=.14))
    xlabel=T('time during one press (schematic)',26,GREY).move_to([x,-2.95,0])
    return VGroup(axes,pulses,title,ticks,xlabel)


class S12Bio(SpokenScene):
    def construct(self):
        bio=pulse_plot(-2.9,True);control=pulse_plot(3.55,False)
        # All axes, ticks and units accompany the traces from their first frame.
        ylabel=T('Pulse amplitude / peak',27).rotate(PI/2).move_to([-6.55,-.15,0])
        self.add(bio,control,ylabel,T('Biomimicry',30).move_to([0,3.55,0]),
                 T('Fixed pulse spacing · every fifth pulse shown',26,GREY).move_to([0,-3.62,0]))
        self.at('One strategy')
        self.play(Indicate(bio[2],color=TEAL,scale_factor=1.02),run_time=.3)
        self.at('Here the scheme')
        self.play(FadeIn(T('lower level\nbetween',27,TEAL).move_to([-2.9,.55,0])),
                  FadeIn(T('follows depth',27,GREY).move_to([3.55,2.35,0])),run_time=.35)
        onset=VGroup(T('onset',27,TEAL).move_to([-4.45,2.4,0]),arr([-4.45,2.12,0],[-4.6,1.8,0],TEAL,w=3,tip=.12))
        offset=VGroup(T('offset',27,TEAL).move_to([-1.35,2.4,0]),arr([-1.35,2.12,0],[-1.25,1.8,0],TEAL,w=3,tip=.12))
        self.at('strongest at contact')
        self.play(FadeIn(onset),FadeIn(offset),run_time=.35)
        self.finish()


class S13Hobbs(SpokenScene):
    def construct(self):
        title=heading('Which pattern felt closer to a real press?')
        subtitle=T('Three people · 28 electrodes · one mark per electrode',27,GREY).move_to([0,2.45,0])
        self.add(title,subtitle,foot('Hobbs and colleagues, 2025'))
        # Grouped categorical marks; counts are data, not invented rating heights.
        rows=VGroup()
        for y,n,label,col in ((1.35,9,'Biomimetic closer',TEAL),(.0,16,'No clear preference',GREY),(-1.35,3,'Non-biomimetic closer',GREY)):
            name=T(label,29,col).move_to([-3.9,y+.23,0])
            count=T(f'{n} of 28 electrodes'+(' · 32%' if n==9 else ''),27,col).move_to([-3.9,y-.35,0])
            marks=VGroup(*[Rectangle(width=.35,height=.6,color=col,fill_opacity=.8).move_to([-.65+i*.43,y,0]) for i in range(n)])
            rows.add(VGroup(name,count,marks))
        self.add(rows)
        self.at('In three people')
        self.play(Indicate(subtitle,color=TEXT,scale_factor=1.01),run_time=.3)
        self.at('on some electrodes')
        self.play(Indicate(rows[0][2],color=TEAL,scale_factor=1.025),run_time=.4)
        self.at('It also needed less charge')
        # Qualitative comparison only: bar lengths do not encode a numeric ratio.
        self.play(FadeOut(rows),FadeOut(subtitle),
                  Transform(title,heading('Same felt intensity: which needed less charge?')),
                  run_time=.25)
        ctitle=T('Same felt intensity',43).move_to([0,2,0])
        note=T('Charge comparison · schematic',27,GREY).move_to([0,-2.6,0])
        bars=VGroup()
        for y,w,label,col in ((.65,5.5,'Non-biomimetic',GREY),(-.9,3.65,'Biomimetic',TEAL)):
            bars.add(T(label,31,col).move_to([-3.9,y,0]),
                     Rectangle(width=w,height=.65,color=col,fill_opacity=.7).move_to([-.8+w/2,y,0]))
        less=T('less charge',30,TEAL).move_to([4.25,-.9,0])
        self.play(FadeIn(ctitle),FadeIn(bars),FadeIn(less),FadeIn(note),run_time=.4)
        self.finish()


class S14NotLaw(SpokenScene):
    def construct(self):
        self.add(heading('Biomimicry'))
        tag=bchip('Evidence-backed strategy',TEAL,44).move_to([0,1.0,0])
        self.at('That supports a strategy')
        self.play(FadeIn(tag),run_time=.4)
        caution=T('Closer copying\n≠ always better',48,RED,should_center=True).move_to([0,-1.45,0])
        self.at('It is not a law')
        self.play(FadeIn(caution),run_time=.4)
        self.finish()


def takeaway_lines():
    return VGroup(T("Map where each electrode’s touch is felt;\ntest what the person can tell apart.",35,
                    should_center=True,line_spacing=1.1).move_to([0,-1.95,0]),
                  T('Then send each group a pattern it can read.',33,TEAL).move_to([0,-3.1,0]))


class S15Takeaway(SpokenScene):
    def construct(self):
        # Compact diagram sits above two dedicated text lanes; no cross-fade leftovers.
        diagram=VGroup(cortex(),hand(3.4,-.15,1.12),electrodes()).scale(.65).move_to([0,1.15,0])
        fs=fields().scale(.65).shift([-1.25,1.2,0])
        lines=takeaway_lines()
        # Start legible and brighten immediately, including the very first frame.
        self.add(diagram,lines[0].set_opacity(.65))
        self.play(lines[0].animate.set_opacity(1),run_time=.35)
        self.at('map where each')
        self.play(FadeIn(fs),run_time=.35)
        self.at('Then send each group')
        self.play(FadeIn(lines[1]),run_time=.4)
        self.finish()


class S16End(EndCard):
    LINE='Map where each electrode’s touch is felt; test what can be told apart. Then send each group a pattern it can read.'

    def construct(self):
        line=T("Map where each electrode’s touch is felt;\ntest what can be told apart.\n\nThen send each group a pattern it can read.",35,
               font=TITLE_FONT,should_center=True,line_spacing=1.15)
        line.move_to([0,.35,0])
        sub=T('biochemistrypedia.com',27,TEAL).move_to([0,-2.6,0])
        self.add(line,sub)
        self.finish()
