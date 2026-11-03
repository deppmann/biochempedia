"""Chapter 4: removal experiments, revised after the full-frame review.
COLOR MAP: YELLOW light / readouts / questions; BLUE rods and cones;
GREEN melanopsin / ipRGC relay; PURPLE targets; RED loss; GREY guides.
All traces are computed from the explicit schematic models below, not data.
"""
import json
import os
from pathlib import Path
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'

class TimedScene(SpokenScene):
    """Reveal at the actual word, without the shared 0.2 s anticipation.

    The old sync log printed elapsed BEFORE waiting, so negative entries were
    waiting time, not early reveals. Log the actual post-wait time for audit.
    """
    def _words(self):
        words = super()._words()
        merged = []
        i = 0
        while i < len(words):
            if i + 1 < len(words) and [words[i][1], words[i+1][1]] == ['in', 'trains']:
                merged.append((words[i][0], 'entrains')); i += 2
            else:
                merged.append(words[i]); i += 1
        return merged

    def at(self, phrase, lead=0, nth=0):
        target = self.t_of(phrase, nth)
        rest = target - self.elapsed()
        if rest > .001:
            self.wait(rest + 1 / config.frame_rate)
        with open('/tmp/pigment-cue-audit.jsonl', 'a') as f:
            f.write(json.dumps(dict(scene=os.environ['KX_SCENE_ID'], phrase=phrase,
                                   word_s=target, reveal_s=self.elapsed()))+'\n')

def arr(a,b,color=GREY,w=5,tip=.22):
    return Arrow(a,b,buff=.06,color=color,stroke_width=w,tip_length=tip,
                 max_tip_length_to_length_ratio=.45,max_stroke_width_to_length_ratio=12)
def cell(cx,cy,w,h,color=GREEN,fill=.15):
    return Ellipse(width=w,height=h,stroke_color=color,stroke_width=4,
                   fill_color=color,fill_opacity=fill).move_to([cx,cy,0])
def cross(center,s=.3):
    c=np.array(center,float)
    return VGroup(Line(c+[-s,-s,0],c+[s,s,0],color=RED,stroke_width=6),
                  Line(c+[-s,s,0],c+[s,-s,0],color=RED,stroke_width=6))
def label(s,x=0,y=3.1,size=28,color=TEXT):
    return T(s,size,color).move_to([x,y,0])
def eye_icon(cx,cy,w=2):
    e=Ellipse(width=w,height=w*.57,stroke_color=YELLOW,stroke_width=4).move_to([cx,cy,0])
    iris=Circle(radius=w*.24,stroke_width=0,fill_color=GREY,fill_opacity=.6).move_to(e)
    p=Circle(radius=w*.16,stroke_width=0,fill_color=BG,fill_opacity=1).move_to(e)
    g=VGroup(e,iris,p);g.pup=p
    return g

def scissors(x,y):
    return VGroup(Circle(radius=.12,color=RED).move_to([x-.18,y-.26,0]),
                  Circle(radius=.12,color=RED).move_to([x+.18,y-.26,0]),
                  Line([x-.18,y-.18,0],[x+.28,y+.3,0],color=RED),
                  Line([x+.18,y-.18,0],[x-.28,y+.3,0],color=RED))

def network():
    rc=chip('rods + cones',BLUE,28).move_to([-4.6,-1.1,0])
    body=cell(0,0,3.6,5.3)
    name=label('ipRGC',0,-1.9,32,GREEN)
    mel=chip('melanopsin',GREEN,28).move_to([0,1.05,0])
    relay=arr([-3.05,-1.1,0],[-1.7,-.4,0],BLUE,7)
    own=arr([0,3.1,0],[0,1.5,0],YELLOW)
    out=arr([1.9,0,0],[4,0,0],GREEN,8)
    targets=VGroup(chip('clock',PURPLE,30),chip('pupil',PURPLE,30)).arrange(DOWN,buff=1).move_to([5,0,0])
    return VGroup(rc,body,name,mel,relay,own,out,targets)

# Schematic actograms: onset=12 h for entrainment; tau=23.5 h for
# free running. An early-night pulse on day 4 DELAYS only days 5-7 by 2 h.
LEFT_X=-4.8
HOUR=9.6/24

def record(kind='entrain',blank=False):
    g=VGroup(label('running-wheel record',0,3.35,30),
             label('time of day (h)',0,-3.35,26),
             label('light–dark schedule',-3.8,2.87,26))
    g.add(Rectangle(width=4.8,height=.26,fill_color=YELLOW,fill_opacity=.6,stroke_width=0).move_to([-2.4,2.4,0]),
          Rectangle(width=4.8,height=.26,fill_color=GREY,fill_opacity=.3,stroke_width=0).move_to([2.4,2.4,0]),
          label('light',-2.4,1.99,26,YELLOW),label('dark',3.8,1.99,26,GREY))
    g.add(DashedLine([0,1.7,0],[0,-2.5,0],color=GREY,dash_length=.09),
          label('lights off',.85,2.88,26,GREY),label('days',-5.7,-.35,26,GREY).rotate(PI/2))
    ticks=VGroup()
    for day in range(7):
        y=1.45-day*.59
        g.add(Line([LEFT_X,y,0],[4.8,y,0],color=GREY,stroke_opacity=.25))
        onset=12-day*.5 if kind=='free' else 12+(2 if kind in ('shift','mask_shift') and day>3 else 0)
        for i,t in enumerate(np.arange(onset,onset+8,.42)):
            if kind in ('mask','mask_shift') and day==3 and 15<=t<=19 and i%4!=0:
                continue
            ticks.add(Line([LEFT_X+t*HOUR,y-.12,0],[LEFT_X+t*HOUR,y+.12,0],color=TEXT,stroke_width=3))
    for t in [0,12,24]:
        x=LEFT_X+t*HOUR
        g.add(Line([x,-2.35,0],[x,-2.52,0],color=GREY),label(str(t),x,-2.8,26))
    if kind in ('mask','mask_shift'):g[8].set_opacity(0)
    if not blank:g.add(ticks)
    return g,ticks

def pulse_marker():
    x=LEFT_X+13*HOUR; y=1.45-3*.59
    return VGroup(Line([x,y-.25,0],[x,y+.25,0],color=YELLOW,stroke_width=8),
                  label('light pulse',-2.9,y-.15,28,YELLOW),
                  arr([-1.7,y-.15,0],[x-.1,y,0],YELLOW,3,.12))

def shift_marker():
    y=-2.4
    return VGroup(DoubleArrow([0,y,0],[2*HOUR,y,0],buff=0,color=YELLOW,tip_length=.12),
                  label('delay (schematic)',-2.7,y,28,YELLOW))

# Piecewise-linear schematic pupil dynamics from the lesson's qualitative
# fast / slow / fading / held phenotypes. t is normalized seconds-to-minutes.
PUPIL={'wt':([0,.06,.2,1],[1,.28,.22,.22]),
       'ko':([0,.06,.2,1],[1,.28,.35,.8]),
       'rc':([0,.15,.55,.8,1],[1,.8,.25,.22,.22]),
       'none':([0,1],[1,1]),'abl':([0,.12,1],[1,.87,.87])}
def trace(kind,x=0,y=0,w=5,h=2,color=YELLOW,end=1):
    ts,vs=PUPIL[kind]
    return VMobject(color=color,stroke_width=4).set_points_as_corners(
        [[x+w*t,y+h*float(np.interp(t,ts,vs)),0] for t in np.linspace(0,end,150)])
def pupil_plot(kind='wt'):
    ax=VGroup(Line([-1.7,-2.3,0],[5.5,-2.3,0],color=GREY),
              Line([-1.7,-2.3,0],[-1.7,2.3,0],color=GREY),
              label('pupil size',-3,2.2,28,YELLOW),
              label('seconds → minutes',1.8,-2.85,28),
              label('schematic • steady bright light',1,-3.45,26,GREY),
              label('large',-2.5,1.8,26,GREY),label('small',-2.5,-1.8,26,GREY))
    return ax,trace(kind,-1.65,-2.1,6.9,4.1)

ROWS=[('wild type','yes','yes','entrains\nfull shifts','fast, held'),
      ('no melanopsin','yes','no','entrains\nsmaller shifts','fades'),
      ('no rod/cone\nsignalling','no','yes','entrains','slow, held'),
      ('triple mutant\nno Opn4\nGnat1, Cnga3','no','no','does not entrain\nfree-runs\nno masking','no significant\nreflex'),
      ('ipRGC ablation','intact','lost','impaired','much reduced')]
XS=[-4.9,-2.75,-.9,1.65,4.8]
YS=[1.85,.75,-.35,-1.65,-2.95]
def table(n=4,pending=None):
    g=VGroup(); rows=[]
    g.add(VGroup(*[label(t,x,2.95,26,TEXT) for t,x in zip(
        ['mouse','rod/cone\nrelay','melanopsin','clock','pupil'],XS)]),
        Line([-6.3,2.35,0],[6.3,2.35,0],color=GREY))
    for i in range(n):
        vals=list(ROWS[i])
        if pending==i:vals[3:]=['?','?']
        row=VGroup(*[label(t,x,YS[i],22 if i==3 and j==0 else 26,BLUE if j==1 else GREEN if j==2 else TEXT)
                     for j,(t,x) in enumerate(zip(vals,XS))])
        g.add(row);rows.append(row)
        g.add(Line([-6.3,YS[i]-(.7 if i==3 else .53),0],[6.3,YS[i]-(.7 if i==3 else .53),0],color=GREY,stroke_opacity=.25))
    return g,rows

def row_result(row,j,text,color=TEXT):
    row[j].become(label(text,XS[j],row[j].get_y(),22 if j==0 else 26,color))
    return FadeIn(row[j])

def small_plot(kind='wt',top=.85,bottom=-2.95):
    x=-2.2;w=7.6; h=top-bottom
    return VGroup(Line([x,bottom-.15,0],[x+w,bottom-.15,0],color=GREY),
                  Line([x,bottom-.15,0],[x,top+.2,0],color=GREY),
                  label('pupil size',-4.3,(top+bottom)/2,26,YELLOW),
                  label('seconds → minutes • schematic',1.5,bottom-.55,26,GREY)),trace(kind,x,bottom,w,h)

def predict():
    return VGroup(table(5,4)[0].scale(.92).shift(UP*.25),label('If rods + cones had their own route…?',0,3.65,28,YELLOW))

def numbers(question=True):
    g=VGroup(label('Made-up phase shifts',0,3.25,32,YELLOW))
    # Bars use the REMOVED concept's colour, as do the deficit brackets.
    for y,(s,v,c) in zip([1.8,.65,-.5,-1.65],
                         [('wild type',2,TEXT),('no melanopsin',.6,GREEN),
                          ('no rods + cones',1.8,BLUE),('ablation',0,RED)]):
        g.add(label(s,-4.55,y,28,c),label(f'{v:.1f} h',5.6,y,28,c))
        if v:g.add(Rectangle(width=v*2.25,height=.5,stroke_width=0,fill_color=c,fill_opacity=.75).move_to([-.8+v*1.125,y,0]))
    g.add(Line([-.8,2.2,0],[-.8,-2,0],color=GREY),
          DashedLine([3.7,2.2,0],[3.7,-2,0],color=GREY))
    if question:g.add(label('Do the single losses add up to losing both?',0,-3.1,28,YELLOW))
    return g

def loss_bracket(value,y,color,text):
    x=-.8+value*2.25
    return VGroup(Line([x,y+.35,0],[3.7,y+.35,0],color=color,stroke_width=4),
                  Line([x,y+.25,0],[x,y+.45,0],color=color),
                  Line([3.7,y+.25,0],[3.7,y+.45,0],color=color),
                  label(text,1.5,y+.65,26,color))

def saturation():
    ax=Axes(x_range=[0,1.4,.2],y_range=[0,1.12,.2],x_length=9.5,y_length=4.7,
            tips=False,axis_config={'color':GREY}).move_to([.65,-.15,0])
    # Lesson's illustrative ceiling model f(d)=min(d,1); combined drive=.3+.9.
    curve=ax.plot(lambda d:min(d,1),x_range=[0,1.35,.005],color=YELLOW,use_smoothing=False)
    labs=VGroup(label('One possible model • saturation site unknown',0,3.45,28,GREY),
                label('output (% of wild type)',-.7,2.85,28),
                label('total drive',.8,-3.25,28))
    for v in [0,.5,1]:
        labs.add(label(f'{int(v*100)}%',ax.c2p(0,v)[0]-.55,ax.c2p(0,v)[1],26))
    for v in [0,.6,1.2]:
        labs.add(label(f'{v:g}',ax.c2p(v,0)[0],ax.c2p(v,0)[1]-.4,26))
    ceiling=VGroup(DashedLine(ax.c2p(0,1),ax.c2p(1.35,1),color=GREY),
                   label('ceiling',-.2,2.25,28,YELLOW),
                   label('pupil min.\nor maximum\nphase shift',-5.4,.5,26,GREY))
    return ax,curve,VGroup(labs,ceiling)

class S00Title(TitleCard):
    LESSON='Melanopsin Cells: Light for the Clock and the Pupil'
    TITLE='Remove the Pigment, or Remove the Cell'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,26,GREY),
                 T('Remove the Pigment,\nor Remove the Cell',48,font=TITLE_FONT)).arrange(DOWN,buff=.55)
        self.play(FadeIn(g),run_time=.6);self.finish()
class S01Q(TimedScene):
    def construct(self):
        n=network();self.add(n)
        self.at('take it away');self.play(FadeIn(VGroup(scissors(1.35,1.05),scissors(-2.5,-.8),scissors(1.75,-1.5))),run_time=.45)
        self.at('But which part');self.play(FadeIn(label('Which part?',0,-3.25,36,YELLOW)),run_time=.4);self.finish()
class S02Three(TimedScene):
    def construct(self):
        n=network();self.add(n)
        cuts=VGroup(scissors(1.35,1.05),scissors(-2.6,-.85),scissors(1.7,-1.4))
        self.add(cuts)
        self.at('Remove the pigment');self.play(Indicate(cuts[0],color=RED),FadeIn(label('melanopsin',3.05,1.65,28,RED)),run_time=.4)
        self.at('remove the rods');self.play(Indicate(cuts[1],color=RED),FadeIn(label('rods and cones',-4.15,-.25,28,RED)),run_time=.4)
        self.at('or remove the cell');self.play(Indicate(cuts[2],color=RED),FadeIn(label('the cell',3.05,-1.65,28,RED)),run_time=.4);self.finish()
class S03Readout(TimedScene):
    def construct(self):
        g,t=record(blank=True);self.add(g)
        self.at('For the clock');self.play(Indicate(g[2],color=YELLOW),run_time=.4)
        self.at('watch');self.play(Create(t),run_time=.9);self.finish()
class S04Entrain(TimedScene):
    def construct(self):
        g,_=record();self.add(g)
        self.at('mouse entrains');self.play(FadeIn(label('entrains',3,2.88,28,YELLOW)),run_time=.35)
        self.at('keeps a fixed timing');self.play(Create(Line([0,1.6,0],[0,-2.2,0],color=YELLOW)),run_time=.5);self.finish()
class S05Free(TimedScene):
    def construct(self):
        g,t=record();self.add(g)
        self.at('free runs')
        # Remove old ticks first; never cross-fade two records of activity.
        self.remove(g);new,_=record('free');self.add(new,label('free-runs',3,2.88,28,YELLOW))
        self.at('It drifts');self.play(Create(DashedLine([0,1.45,0],[-1.2,-2.09,0],color=YELLOW)),run_time=.6);self.finish()
class S06Shift(TimedScene):
    def construct(self):
        g,_=record();self.add(g)
        self.at('a brief light pulse');self.play(FadeIn(pulse_marker()),run_time=.4)
        self.at('how far');self.remove(g);new,_=record('shift');self.add(new)
        self.play(FadeIn(shift_marker()),run_time=.45);self.finish()
class S07Mask(TimedScene):
    def construct(self):
        g,_=record();self.add(g)
        self.at('Bright light at night');g[8].set_opacity(0)
        x=LEFT_X+17*HOUR
        bar=Rectangle(width=4*HOUR,height=.3,fill_color=YELLOW,fill_opacity=1,stroke_width=0).move_to([x,2.4,0])
        self.play(FadeIn(bar),FadeIn(label('bright light at night',2,3.0,26,YELLOW)),run_time=.4)
        self.at('suppresses');self.remove(g);new,_=record('mask');self.add(new,bar)
        self.play(Create(DashedLine([x,2.2,0],[x,-.55,0],color=YELLOW)),run_time=.5)
        self.at('right away')
        self.play(FadeIn(label('masking: acute activity change',-2.8,.05,26,YELLOW)),run_time=.35)
        self.at('The same light')
        # Optional clock effect is shown on the subsequent onsets, separately
        # from the within-row masking gap caused by the bright light.
        later=VGroup()
        for day in range(4,7):
            y=1.45-day*.59
            later.add(arr([0,y,0],[.8,y,0],PURPLE,4,.13))
        self.play(Transform(new[-1],record('mask_shift')[1]),Create(later),FadeIn(label('may also shift the clock\n(measure separately)',-2.55,-1.65,26,PURPLE)),run_time=.5);self.finish()
class S08Pupil(TimedScene):
    def construct(self):
        eye=eye_icon(-4.4,-.2,2.5);ax,tr=pupil_plot();self.add(eye,ax)
        self.at('film the constriction')
        self.add(arr([-.7,1.6,0],[-.7,-.8,0],YELLOW,3),label('constriction',1.2,.45,28,YELLOW))
        self.play(eye.pup.animate.scale(.45),Create(tr),run_time=2.5);self.finish()
class S09Wt(TimedScene):
    def construct(self):
        tab,rows=table(1,0);ax,tr=small_plot();self.add(tab,ax)
        self.at('It entrains');self.play(row_result(rows[0],3,'entrains'),run_time=.35)
        self.at('shifts fully');self.play(row_result(rows[0],3,ROWS[0][3]),run_time=.35)
        self.at('pupil constricts');self.play(row_result(rows[0],4,ROWS[0][4]),Create(tr),run_time=1.1);self.finish()
class S10Ko(TimedScene):
    def construct(self):
        tab,_=table(1);ax,tr=small_plot();self.add(tab,ax,tr)
        self.at('Row two');self.remove(tab,ax,tr);tab,rows=table(2,1);ax,tr=small_plot('ko',top=-.05);self.add(tab,ax,small_plot('wt',top=-.05)[1].set_stroke(color=GREY,opacity=.5),label('wild-type reference',1.2,-.5,26,GREY))
        self.at('still entrains');self.play(row_result(rows[1],3,'entrains'),run_time=.35)
        self.at('smaller');self.play(row_result(rows[1],3,ROWS[1][3]),run_time=.35);self.finish()
class S11Ko2(TimedScene):
    def construct(self):
        eye=eye_icon(-4.4,-.2,2.5);ax,tr=pupil_plot('ko');self.add(eye,ax,label('no melanopsin',0,3.2,30,GREEN))
        self.at('Its pupil constricts');early=trace('ko',-1.65,-2.1,6.9,4.1,end=.2)
        self.play(Create(early),eye.pup.animate.scale(.45),run_time=.8)
        self.at('constriction fades');self.play(Transform(early,tr),eye.pup.animate.scale(1.8),FadeIn(label('fades',4.6,.55,28,YELLOW)),run_time=1.2);self.finish()
class S12Rc(TimedScene):
    def construct(self):
        tab,_=table(2);ax,tr=small_plot('ko',top=-.05);self.add(tab,ax,tr)
        self.at('Row three');self.remove(tab,ax,tr);tab,rows=table(3,2);ax,tr=small_plot('rc',top=-1.1);self.add(tab,ax,small_plot('wt',top=-1.1)[1].set_stroke(color=GREY,opacity=.5),label('wild type',-4.3,-2.45,26,GREY))
        self.at('It entrains');self.play(row_result(rows[2],3,ROWS[2][3]),run_time=.4)
        self.at('Its pupil is slower');self.play(row_result(rows[2],4,ROWS[2][4]),Create(tr),run_time=1.8);self.finish()
class S13Rc2(TimedScene):
    def construct(self):
        tab,_=table(3);ax,tr=small_plot('rc',top=-1.1);self.add(tab,ax,tr)
        self.add(small_plot('wt',top=-1.1)[1].set_stroke(color=GREY,opacity=.6))
        self.at('normal maximum');depth=-2.95+1.85*.22
        self.play(Create(DashedLine([-2.2,depth,0],[5.4,depth,0],color=TEXT)),
                  FadeIn(Dot([4.5,depth,0],color=YELLOW)),
                  FadeIn(label('same maximum depth in bright light',2.3,-1.2,26,YELLOW)),run_time=.5);self.finish()
class S14Triple(TimedScene):
    def construct(self):
        tab,_=table(3);ax,tr=small_plot('rc',top=-1.1);self.add(tab,ax,tr)
        self.at('Row four');self.remove(tab,ax,tr);tab,rows=table(4,3)
        rows[3][0].become(label('triple mutant',XS[0],YS[3],22));self.add(tab)
        self.at('It lacks melanopsin')
        self.play(row_result(rows[3],0,'triple mutant\nno Opn4',RED),run_time=.35)
        self.at('rod transducin')
        rows[3][0].become(label('triple mutant\nno Opn4, Gnat1',XS[0],YS[3],22,RED))
        self.at('cone channel subunit')
        rows[3][0].become(label(ROWS[3][0],XS[0],YS[3],22,RED));self.finish()
class S15Triple2(TimedScene):
    def construct(self):
        tab,rows=table(4,3);self.add(tab)
        self.at('It does not entrain');self.play(row_result(rows[3],3,'does not entrain'),run_time=.35)
        # Transcript spells this particular occurrence as one word.
        self.at('It freeruns');self.play(row_result(rows[3],3,'does not entrain\nfree-runs'),run_time=.35)
        self.at('shows no masking');self.play(row_result(rows[3],3,ROWS[3][3]),run_time=.35)
        self.at('no significant pupil');self.play(row_result(rows[3],4,ROWS[3][4]),
            Create(Line([-4.8,-3.1,0],[-4.8,-2.6,0],color=GREY)),
            Create(trace('none',-4.8,-3.1,2.2,.4)),
            FadeIn(label('pupil: no significant reflex',1.3,-2.8,28,YELLOW)),run_time=.55);self.finish()
class S16Read(TimedScene):
    def construct(self):
        tab,_=table(4);self.add(tab)
        def box(i,c):return Rectangle(width=12.7,height=1.4 if i==3 else 1.04,color=c,stroke_width=3).move_to([0,YS[i],0])
        boxes=VGroup(box(1,YELLOW),box(2,YELLOW))
        self.at('Either input alone');self.play(Create(boxes),run_time=.5)
        self.at('Lose both');self.play(FadeOut(boxes),Create(box(3,RED)),run_time=.45);self.finish()
class S17Predict(TimedScene):
    def construct(self):
        tab,_=table(4);self.add(tab.scale(.92).shift(UP*.25),label('Pause and predict',0,-3.5,28,YELLOW))
        self.at('Keep the rods');self.remove(tab);tab,rows=table(5,4);rows[4][2].become(label('?',XS[2],YS[4],26,GREEN));tab.scale(.92).shift(UP*.25);self.add(tab)
        self.at('kill');self.play(Transform(rows[4][2],T('lost',26*.92,GREEN).move_to(rows[4][2])),run_time=.35)
        self.at('what would you see');self.play(FadeIn(predict()[1]),run_time=.35);self.finish()
class S18Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(predict(),label('Pause and predict',0,-3.5,28,YELLOW));self.wait(5)
class S19Reveal1(TimedScene):
    def construct(self):
        tab,rows=table(5,4);self.add(tab)
        ghost=VGroup(rows[1][3].copy(),rows[1][4].copy()).set_opacity(.55)
        self.at('strong separate route');self.play(FadeIn(label('If a strong separate route existed',0,3.6,28,YELLOW)),run_time=.4)
        self.at('keep much');self.add(ghost);self.play(rows[4][3].animate.set_opacity(0),rows[4][4].animate.set_opacity(0),ghost.animate.shift(DOWN*(YS[1]-YS[4])),run_time=1);self.finish()
class S20Reveal2(TimedScene):
    def construct(self):
        # Evidence first, then the ablation row; no blank hypothetical cells.
        self.add(label('Güler and colleagues, 2008',0,3.35,32),
                 label('Opn4 disrupted by toxin gene • incomplete cell loss',0,2.7,28,RED))
        x=-4.8;y=-1.8;w=10;h=3.3
        self.add(Line([x,y,0],[x+w,y,0],color=GREY),Line([x,y,0],[x,y+h+.2,0],color=GREY),
                 label('pupil size',-4.5,2.05,26),label('seconds → minutes • schematic',0,-2.3,26,GREY))
        for kind,c,ly in [('wt',TEXT,-.7),('ko',GREEN,.1),('none',TEXT,1.92)]:
            self.add(trace(kind,x,y,w,h,c).set_stroke(opacity=.8 if kind=='none' else .45),label({'wt':'wild type','ko':'no melanopsin','none':'triple mutant'}[kind],3.5,ly,26,c))
        self.at('found something else');self.play(Create(trace('abl',x,y,w,h,RED)),FadeIn(label('ablation: some response remains',2.25,1.28,26,RED)),run_time=.9)
        self.at('deficits were larger');self.play(Create(VGroup(Line([5.55,-1.074,0],[5.55,1.071,0],color=RED),Line([5.35,-1.074,0],[5.65,-1.074,0],color=RED),Line([5.35,1.071,0],[5.65,1.071,0],color=RED),Line([5.35,.84,0],[5.65,.84,0],color=GREEN))),FadeIn(label('larger deficit than melanopsin loss alone',0,-2.95,28)),run_time=.4)
        self.at('close to those');self.play(FadeIn(label('Similar to triple mutant',0,-3.5,28)),run_time=.35)
        self.wait(.35);self.clear();self.add(table(5)[0],label('Güler 2008 • incomplete loss',0,3.6,28,RED));self.finish()
class S21Vision(TimedScene):
    def construct(self):
        tab,rows=table(5);self.add(tab)
        self.at('Pattern vision')
        # Keep all five rows, with the grating adjacent to the ablation row.
        self.play(tab.animate.scale(.8).shift(LEFT*1.3+UP*.35),run_time=.4)
        bars=VGroup(*[Rectangle(width=.18,height=1.1,fill_color=TEXT,fill_opacity=1,stroke_width=0).move_to([4.05+i*.36,-1.65,0]) for i in range(6)])
        self.play(FadeIn(bars),FadeIn(label('pattern vision',4.9,-.65,26)),run_time=.35)
        self.at('other ganglion cells');self.play(FadeIn(label('other ganglion\ncells',4.9,.25,24)),run_time=.3)
        self.at('remained');self.play(FadeIn(label('✓ remained',4.9,-2.65,32,GREEN)),run_time=.35);self.finish()
class S22Route(TimedScene):
    def construct(self):
        n=network();self.add(n)
        # The conjectured bypass is explicitly a dim question, not a claim.
        route=VMobject(color=GREY).set_points_smoothly([[-4.4,-1.8,0],[-3,-2.8,0],[0,-3,0],[3,-2.8,0],[3.8,-1.8,0]])
        branches=VGroup(*[DashedVMobject(VMobject(color=GREY).set_points_smoothly([[3.8,-1.8,0],[4,-.2 if y>0 else -1.2,0],[4.35,y,0]])) for y in [ .8,-.8]])
        bypass=VGroup(DashedVMobject(route),branches,label('separate route?',-3.8,-3.2,26,GREY)).set_opacity(.35)
        self.add(bypass)
        self.at('main route');self.play(n[1].animate.set_stroke(GREEN,8),n[6].animate.set_stroke(GREEN,13),
                    AnimationGroup(*[target[0].animate.set_stroke(PURPLE,5) for target in n[7]]),bypass.animate.set_opacity(0),
                    FadeIn(label('main route, in mice',0,-3.4,34,YELLOW)),run_time=.6);self.finish()

def comparison():
    def panel(x):
        rc=label('rods +\ncones',x-1.7,-1.5,26,BLUE)
        body=cell(x,.1,2.2,5)
        name=label('ipRGC',x,-1.8,28,GREEN)
        pigment=chip('pigment',GREEN,26,pad=.14).move_to([x,1.05,0])
        relay=arr([x-1.6,-.9,0],[x-1.05,-.4,0],BLUE,6)
        own=arr([x,2.7,0],[x,1.5,0],YELLOW)
        out=arr([x+1.15,.1,0],[x+1.75,.1,0],GREEN,7)
        targets=VGroup(label('clock',x+2.2,.65,26,PURPLE),label('pupil',x+2.2,-.4,26,PURPLE))
        return VGroup(rc,body,name,pigment,relay,own,out,targets)
    return panel(-3.4),panel(3.1)

def cut_pigment(n):
    n[3].set_opacity(.3);n[5].set_opacity(.2)
    return cross(n[5].get_center(),.22)
def cut_cell(n):
    # Cut the output at the edge, away from the cell name.
    for i in [1,2,3,4,5,6]:n[i].set_opacity(.2)
    return cross(n[6].get_center(),.28)
class S23Lesson1(TimedScene):
    def construct(self):
        l,r=comparison();self.add(l,r,label('pigment knockout',-3.4,3.25,30),label('cell ablation',3.1,3.25,30),cut_pigment(l))
        self.at('removes both inputs');self.play(Create(cut_cell(r)),run_time=.45)
        self.at('cannot say which input');self.play(FadeIn(label('Different questions',0,-3.35,34,YELLOW)),run_time=.4);self.finish()
class S24Predict2(TimedScene):
    def construct(self):
        # Context already visible, then values and question on their words.
        self.add(label('Predict: compare the losses',0,3.25,32,YELLOW),
                 label('wild type    no melanopsin    no rods + cones    ablation',0,0,28))
        self.at('Here are');self.clear();self.play(FadeIn(numbers(False)),run_time=.6)
        self.at('Do the two');self.play(FadeIn(numbers()[-1]),run_time=.4);self.finish()
class S25Pause2(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(numbers());cue=label('Pause and predict • 5',0,-2.5,26,TEAL);self.add(cue)
        for n in range(5,0,-1):
            cue.become(label(f'Pause and predict • {n}',0,-2.5,26,TEAL));self.wait(1)
class S26Reveal3(TimedScene):
    def construct(self):
        g=numbers(False);self.add(g)
        self.at('They do not');self.play(Create(loss_bracket(.6,.65,GREEN,'2.0 − 0.6 = 1.4 h')),Create(loss_bracket(1.8,-.5,BLUE,'2.0 − 1.8 = 0.2 h')),run_time=.7)
        self.at('Together the two single losses')
        terms=VGroup(T('melanopsin: 1.4',26,GREEN),T('+',26),T('rods + cones: 0.2',26,BLUE),T('= 1.6 h',28)).arrange(RIGHT,buff=.18).move_to([0,-2.6,0])
        self.play(FadeIn(terms),run_time=.5)
        self.at('smaller than');self.play(FadeIn(label('losing both = 2.0 h',1.5,-1.65,28,RED)),FadeIn(label('1.6 h < 2.0 h',0,-3.35,32,YELLOW)),run_time=.45);self.finish()
class S27Saturate(TimedScene):
    def construct(self):
        ax,c,labs=saturation();self.add(ax,c,labs)
        self.at('output saturates');self.play(Indicate(c,color=YELLOW),run_time=.6)
        self.at('A pupil cannot');e=eye_icon(3,-.65,1.6);self.play(FadeIn(e),run_time=.3);self.play(e.pup.animate.scale(.35),run_time=.6);self.finish()
class S28Saturate2(TimedScene):
    def construct(self):
        ax,c,l=saturation();self.add(ax,c,l)
        self.at('A phase shift');self.play(Indicate(l[1],color=YELLOW),run_time=.4)
        def point(d,v,text,where,col,leader):
            p=ax.c2p(d,v)
            return VGroup(Dot(p,color=col,radius=.1),label(text,*where,26,col),
                          Line(p,leader,color=col,stroke_width=2))
        self.at('Near a ceiling');self.play(FadeIn(point(.3,.3,'rods + cones alone: 30%',(.5,-1.6),BLUE,[-1.65,-1.5,0])),run_time=.4)
        self.at('stronger input alone');self.play(FadeIn(point(.9,.9,'melanopsin alone: 90%',(3.5,.55),GREEN,[2.15,.85,0])),run_time=.4)
        self.at('adding the other')
        a=np.array([2.9,ax.c2p(.9,.9)[1],0]);b=np.array([2.9,ax.c2p(1.2,1)[1],0])
        bracket=VGroup(Line(a,b,color=YELLOW,stroke_width=4),
            Line(a+LEFT*.1,a+RIGHT*.1,color=YELLOW),Line(b+LEFT*.1,b+RIGHT*.1,color=YELLOW))
        self.play(FadeIn(point(1.2,1,'both inputs: 100%',(4,2.25),YELLOW,[4,1.95,0])),
            Create(bracket),FadeIn(label('+10 points',4.4,(a[1]+b[1])/2,26,YELLOW)),run_time=.5);self.finish()
class S29Share(TimedScene):
    def construct(self):
        n=network();self.add(n,cut_pigment(n))
        self.at('other input can do alone');self.play(n[4].animate.set_stroke(BLUE,12),n[6].animate.set_stroke(GREEN,12),run_time=.6)
        self.at('does not show');self.play(FadeIn(label('Alone does not mean a share',0,-3.4,34,YELLOW)),run_time=.4);self.finish()

def timeline(y=0):
    return VGroup(arr([-5.3,y,0],[5.3,y,0],GREY),label('birth',-5,y-.45,26,GREY),label('adult',4.8,y-.45,26,GREY),
                  Line([-5,y-.12,0],[-5,y+.12,0],color=GREY),Line([4.8,y-.12,0],[4.8,y+.12,0],color=GREY))
class S30Limit(TimedScene):
    def construct(self):
        self.add(label('Germline ablation: gradual loss',0,3.35,34),label('Güler mice • schematic, no measured rates',0,2.65,26,GREY),timeline(-2.3))
        # Repeated age cohorts, each at a dated x position. Loss fraction rises
        # 0 -> 1/4 -> 1/2 -> 3/4 and remains incomplete; not a spatial cell map.
        cohorts=[]
        for x in [-4.5,-1.5,1.5,4.5]:
            group=VGroup(*[cell(x+(j%2-.5)*.65,.3+(j//2-.5)*1.25,.5,.9) for j in range(4)])
            self.add(group);cohorts.append(group)
        self.play(*[cohorts[i][j].animate.set_stroke(opacity=.3).set_fill(opacity=.04)
                    for i in range(1,4) for j in range(i)],run_time=1.2)
        self.at('weakened toxin gene');self.play(FadeIn(label('toxin gene at melanopsin locus',0,-3.35,28,RED)),run_time=.4)
        self.at('kills the cells gradually')
        for i in range(1,4):
            self.play(*[cohorts[i][j].animate.set_stroke(opacity=.12).set_fill(opacity=.018) for j in range(i)],run_time=.4)
        self.at('more are lost')
        # The dated cohorts carry the increasing loss without a floating curve.
        self.play(FadeIn(label('loss increases; some cells survive',0,1.9,28,RED)),run_time=.6);self.finish()
class S31Rewire(TimedScene):
    def construct(self):
        self.add(label('Loss during development',0,3.4,30,RED),timeline(2.7),cross([-3.7,2.7,0],.22))
        lost=cell(-4.2,.85,1.5,1.4).set_opacity(.2)
        survivor=cell(-4.2,-.85,1.5,1.4)
        target=chip('new target',PURPLE,28).move_to([3,.1,0])
        self.add(lost,cross([-3.4,.85,0],.22),label('lost cell',-2.4,.9,26,GREY),survivor,label('surviving cell',-1.9,-1.1,26,GREEN),target)
        self.at('can let targets rewire');self.play(GrowArrow(arr([-3.4,-.85,0],[1.6,.1,0],PURPLE,6)),run_time=.65)
        self.at('An ablation timed');self.play(FadeIn(timeline(-2.3)),run_time=.35)
        self.at('in adults');self.play(Create(cross([4.8,-2.3,0],.25)),FadeIn(label('adult-timed ablation',0,-3.3,30,YELLOW)),run_time=.4);self.finish()
class S32Take(TimedScene):
    def construct(self):
        l,r=comparison();self.add(l,r,label('remove pigment',-3.4,3.25,30),label('remove cell',3.1,3.25,30))
        self.at('Remove the pigment');self.play(Create(cut_pigment(l)),run_time=.45)
        self.at('relay carries on');self.play(l[4].animate.set_stroke(BLUE,10),l[6].animate.set_stroke(GREEN,10),FadeIn(label('relay carries on',-3.4,-3.3,28,GREEN)),run_time=.4)
        self.at('Remove the cell');self.play(Create(cut_cell(r)),run_time=.45)
        self.at('both inputs go');self.play(FadeIn(label('both inputs go',3.1,-3.3,28,RED)),run_time=.4);self.finish()
class S33End(EndCard):
    LINE='Remove the pigment, and the relay carries on.\nRemove the cell, and both inputs go.'
    def construct(self):
        # TASK explicitly allows the full contrast, overriding the old 12-word cap.
        a=label('Remove the pigment,\nand the relay carries on.',0,1.5,38,GREEN)
        b=label('Remove the cell,\nand both inputs go.',0,-1.25,38,RED)
        self.play(FadeIn(a),FadeIn(b),run_time=.5)
        self.add(label('biochemistrypedia.com',0,-3.2,26,TEAL));self.finish()
