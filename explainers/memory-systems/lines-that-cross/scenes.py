"""Lines That Cross: reviewer polish round.
COLOR MAP: controls GREY; amnesic BLUE; Parkinson's ORANGE;
classification/performance PURPLE; reportable memory BLUE; chance TEXT dashed;
dopamine ORANGE; preserved GREEN; absent RED; gold only title ornament.
VALS are the lesson's invented worked example, not published measurements.
Learning traces interpolate from chance to these endpoints; the response trace
is an explicitly schematic difference of exponentials. No traced/sketched data.
"""
import numpy as np
from bp_style import *
from bp_style import SpokenScene as BaseSpokenScene

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
GCOL = {'ctrl': GREY, 'am': BLUE, 'pd': ORANGE}
VALS = {'ctrl': (70, 80), 'am': (68, 40), 'pd': (52, 78)}
CHANCE = np.array([50., 25.])


class SpokenScene(BaseSpokenScene):
    # Retain word alignment without creating an unrequested sync.log artifact.
    def at(self, phrase, lead=.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > .02:
            self.wait(rest)


def label(s, pos, size=28, color=TEXT):
    return T(s, size, color).move_to(pos)


def head(s):
    return label(s, [0, 3.63, 0], 28)


def note(s, y=-3.62):
    return label(s, [0, y, 0], 26)


def legend(y=-1.85, compact=False):
    g=VGroup(*[VGroup(Line(LEFT*.2, RIGHT*.2, color=GCOL[k], stroke_width=5),
                           T(n, 28, GCOL[k])).arrange(RIGHT, buff=.15)
                   for k,n in [('ctrl','Controls'),('am','Amnesic'),('pd',"Parkinson’s")]])
    if compact:
        return g.arrange(DOWN,aligned_edge=LEFT,buff=.22).move_to([-3.3,-1.7,0])
    return g.arrange(RIGHT,buff=.6).move_to([0,y,0])


def axis_base(a, title, xcenter, ticks=(0,25,50,75,100)):
    g=VGroup(a,label(title,[xcenter,3.06,0],30),
             T('% correct',30,GREY).rotate(PI/2).move_to(a.c2p(0,50)+LEFT*.9))
    for v in ticks:
        g.add(T(str(v),26,GREY).next_to(a.c2p(0,v),LEFT,buff=.12))
    return g


class Learning:
    def __init__(self, full=False):
        x=-.1 if full else -3.4
        w=10.8 if full else 4.6
        self.axes=a=Axes(x_range=[0,50,10],y_range=[0,100,25],x_length=w,y_length=5.6,
                         axis_config={'color':GREY,'include_tip':False}).move_to([x,-.05,0])
        self.base=axis_base(a,'Classification',x)
        self.base.add(label('Trials 1–50',[x,-3.07,0],28,GREY))
        for v in (50,):
            self.base.add(T(str(v),26,GREY).next_to(a.c2p(v,0),DOWN,buff=.12))
        # A two-point endpoint difference separates grey and blue without inventing data.
        self.curves={k:a.plot(lambda t,k=k: np.interp(t,[0,50],[50,VALS[k][0]]),
                              x_range=[0,50,1],color=c,stroke_width=5)
                     for k,c in GCOL.items()}
        self.curves['ctrl']=DashedVMobject(self.curves['ctrl'],num_dashes=20)
        self.all=VGroup(self.base,*self.curves.values())


class Questionnaire:
    def __init__(self, full=False, values=None):
        self.values=values or {k:v[1] for k,v in VALS.items()}
        x=0 if full else 3.45
        w=10 if full else 4.5
        self.axes=a=Axes(x_range=[0,4,1],y_range=[0,100,25],x_length=w,y_length=5.6,
                         axis_config={'color':GREY,'include_tip':False}).move_to([x,-.05,0])
        self.base=axis_base(a,'Questionnaire',x)
        self.bars={}
        self.names=VGroup()
        for i,k in enumerate(GCOL,1):
            v=self.values[k]
            self.bars[k]=Rectangle(width=.7 if not full else 1.15,height=5.6*v/100,
                                   color=GCOL[k],fill_opacity=.65).move_to(a.c2p(i,v/2))
            self.names.add(label({'ctrl':'C','am':'A','pd':'P'}[k] if not full else
                                 {'ctrl':'Controls','am':'Amnesic','pd':"Parkinson’s"}[k],
                                 a.c2p(i,0)+DOWN*.35,26,GCOL[k]))
        self.base.add(self.names)
        self.questions=VGroup(*[label('?',a.c2p(i,55),42,GCOL[k]) for i,k in enumerate(GCOL,1)])


def baseline(a, value, text, left=0, right=None):
    xmax=a.x_range[1] if right is None else right
    line=DashedLine(a.c2p(left,value),a.c2p(xmax,value),color=TEXT,stroke_width=2)
    # Put the key in the clear upper corner, outside the marks and bars.
    txt=T(text,28).add_background_rectangle(color=BG,opacity=1,buff=.07)
    txt.move_to([a.get_center()[0],2.24,0] if a.width < 6 else
                a.c2p((left+xmax)/2,value)+DOWN*.3)
    shade=Polygon(a.c2p(left,0),a.c2p(xmax,0),a.c2p(xmax,value),a.c2p(left,value),
                  stroke_width=0,fill_color=GREY,fill_opacity=.045).set_z_index(-1)
    return VGroup(shade,line,txt)


def panels(revealed=(), model=False, question=False, chance=False):
    l,r=Learning(),Questionnaire()
    g=VGroup(l.all,r.base,legend(compact=True))
    g.add(*[r.bars[k] for k in revealed])
    if model:
        r.base[1].move_to([3.45,2.32,0])
        g.add(head('Simple difficulty model · one common capacity'))
        # Separate line in the open space above the right chart.
        g.add(label('harder?',[3.45,3.08,0],30,BLUE))
    else:
        g.add(head('Illustrative scores · not the published figure'))
    if question:
        g.add(r.questions)
    if chance:
        g.add(baseline(l.axes,50,'50% = guessing'),baseline(r.axes,25,'25% = guessing'))
    return g,l,r


def crossing(corrected=False, teaser=False):
    a=Axes(x_range=[0,1,1],y_range=[0,100,25],x_length=8.9,y_length=5.25,
           axis_config={'color':GREY,'include_tip':False}).move_to([-.1,.125,0])
    title='% of controls’ gain above chance' if corrected else '% correct'
    ylab=label(title,[-.1,2.95,0],28) if teaser else T(title,26).rotate(PI/2).move_to([-6.25,0,0])
    base=VGroup(a,ylab,
                label('Task 1' if teaser else 'Classification',[-4.55,-2.85,0],28),
                label('Task 2' if teaser else 'Questionnaire',[4.35,-2.85,0],28))
    if not teaser:
        base.add(legend(3.1))
    for v in (0,25,50,75,100):
        base.add(T(str(v),28,GREY).next_to(a.c2p(0,v),LEFT,buff=.15))
    curves=VGroup(); numbers=VGroup()
    for k in (('am','pd') if teaser else ('ctrl','am','pd')):
        vals=np.array(VALS[k],dtype=float)
        if corrected:
            vals=100*(vals-CHANCE)/(np.array(VALS['ctrl'])-CHANCE)
        ln=Line(a.c2p(0,vals[0]),a.c2p(1,vals[1]),color=GCOL[k],stroke_width=5)
        if k=='ctrl': ln=DashedVMobject(ln,num_dashes=22)
        curves.add(VGroup(ln,*[Dot(a.c2p(i,v),radius=.065,color=GCOL[k]) for i,v in enumerate(vals)]))
        if k!='ctrl' or (not teaser and not corrected):
            for i,v in enumerate(vals):
                # Labels outside endpoints, with room before numeric y ticks.
                offset=(UP*(.52 if k=='ctrl' else (.12 if k=='am' else -.12))+RIGHT*.5) if i else (RIGHT*.7+UP*((-.48 if k=='am' else .9) if corrected else (-.5 if k=='am' else (-.48 if k=='pd' else .52))))
                txt=label(str(round(v)),a.c2p(i,v)+offset,28,GCOL[k])
                # Endpoint-adjacent values need no leader through neighbouring dots.
                numbers.add(txt)
    return base,curves,a,numbers


def pulse(a, corrected=False):
    am,pd=[np.array(VALS[k],dtype=float) for k in ('am','pd')]
    if corrected:
        am,pd=[100*(v-CHANCE)/(np.array(VALS['ctrl'])-CHANCE) for v in (am,pd)]
    x=(am[0]-pd[0])/((pd[1]-pd[0])-(am[1]-am[0]))
    return Flash(a.c2p(x,np.interp(x,[0,1],am)),color=TEXT,flash_radius=.32)


def brain_outline():
    # Schematic side view: lobed contour, central groove, small brainstem.
    pts=[[-2.8,-.7,0],[-3,-.1,0],[-2.7,.9,0],[-2,1.45,0],[-1,1.7,0],
         [0,1.55,0],[1,1.5,0],[2,1,0],[2.7,.4,0],[2.8,-.3,0],[2.1,-1,0],
         [1.3,-1.15,0],[.8,-1.55,0],[.2,-1.35,0],[-.3,-1,0],[-1.8,-1.05,0],[-2.8,-.7,0]]
    outline=VMobject(color=GREY,stroke_width=3).set_points_smoothly(pts)
    grooves=VGroup(*[ArcBetweenPoints(p,q,angle=.7,color=GREY,stroke_opacity=.5)
                     for p,q in [([-1.7,1,0],[-1.9,-.4,0]),([-.5,1.2,0],[-.8,-.5,0]),
                                 ([.8,1.1,0],[.4,-.6,0]),([1.8,.5,0],[1.1,-.6,0])]])
    return VGroup(outline,grooves)


def task_screen():
    frame=RoundedRectangle(width=12,height=5.8,corner_radius=.2,color=GREY).move_to([0,.1,0])
    cards=VGroup(*[VGroup(RoundedRectangle(width=2.3,height=2.0,corner_radius=.12,color=PURPLE,fill_opacity=.1),
                          T(c,44,PURPLE)).move_to([x,.8,0]) for c,x in zip('ABC',[-3.2,0,3.2])])
    buttons=VGroup(chip('Outcome 1',PURPLE,30),chip('Outcome 2',PURPLE,30)).arrange(RIGHT,buff=1.7).move_to([0,-1.65,0])
    return VGroup(frame,cards,buttons,label('cue cards',[0,2.55,0],28,PURPLE),
                  label('two possible outcomes',[0,-2.5,0],28))


def result(ok, x,y, report=False):
    word=('reports' if ok else 'cannot report') if report else ('response' if ok else 'no response')
    return VGroup(chip('+' if ok else '−',GREEN if ok else RED,28),T(word,28)).arrange(RIGHT,buff=.23).move_to([x,y,0])


ROW_Y=[1.1,-.55,-2.2]
COL_X=[-.05,4]

def grid(rows=2,filled=0,question=False):
    g=VGroup(head('Bechara and colleagues · 1995 · three patients'))
    for text,x,c in [('Damage',-4.55,GREY),('Sweat\nresponse',COL_X[0],PURPLE),('Report the\npairing',COL_X[1],BLUE)]:
        g.add(label(text,[x,2.55,0],29,c))
    g.add(Line([-6.3,1.95,0],[6.3,1.95,0],color=GREY))
    for i in range(rows):
        y=ROW_Y[i]
        g.add(label(['Amygdalae','Hippocampi','Both'][i],[-4.55,y,0],30),
              Line([-6.3,y-.82,0],[6.3,y-.82,0],color=GREY,stroke_opacity=.45))
        if i<filled:
            g.add(result(i==1,COL_X[0],y),result(i==0,COL_X[1],y,True))
        elif question and i==2:
            g.add(label('?', [COL_X[0],y,0],40),label('?', [COL_X[1],y,0],40))
    return g


def timer(scene):
    tag=label('Pause and predict',[0,3.6,0],26,TEAL)
    rail=Line([-6.3,-3.77,0],[6.3,-3.77,0],color=GREY,stroke_width=3)
    bar=Line([-6.3,-3.77,0],[6.3,-3.77,0],color=TEAL,stroke_width=5)
    tag.set_z_index(10)
    scene.add_foreground_mobject(tag)
    scene.add(rail)
    scene.play(Create(bar),run_time=5,rate_func=linear)


class S00Title(TitleCard):
    LESSON='Memory Systems'
    TITLE='Lines That Cross'

    def construct(self):
        self.add(VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON.upper(),28,GREY),T(self.TITLE,54,font=TITLE_FONT),Line(LEFT*1.2,RIGHT*1.2,color=GOLD)).arrange(DOWN,buff=.4))
        self.finish()


class S01(SpokenScene):
    def construct(self):
        base,lines,a,_=crossing(teaser=True)
        self.add(base,note('Watch one experiment'),label('Group A',[-3.15,1.6,0],28,BLUE),label('Group B',[-3.15,-.35,0],28,ORANGE))
        self.at('two lines')
        self.play(Create(lines),run_time=1.1)
        self.at('memory has')
        self.play(FadeIn(head('More than one memory system?')),run_time=.4)
        self.at('Watch one experiment')
        self.play(Transform(base[-1],base[-1].copy()),run_time=.2)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        screen=task_screen();self.add(screen,note('Predict an outcome from cue cards'))
        self.at('In')
        self.play(FadeIn(head('Knowlton, Mangels & Squire · 1996')),run_time=.5)
        self.at('gave people')
        self.play(Indicate(screen[1],color=PURPLE,scale_factor=1.04),run_time=.5)
        self.at('weather prediction task')
        self.play(Indicate(screen[2],color=PURPLE,scale_factor=1.04),run_time=.5)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        s=task_screen();self.add(s,head('Learn from probabilistic feedback'),note('Illustrative probabilities · no cue is certain'))
        self.at('Cue cards appeared')
        self.play(LaggedStart(*[c[0].animate.set_fill(PURPLE,opacity=.55) for c in s[1]],lag_ratio=.4),run_time=1.2)
        self.at('person guessed')
        cursor=Triangle(color=TEXT,fill_opacity=1).scale(.18).rotate(PI).next_to(s[2][0],UP,buff=.14)
        feedback=chip('Correct',GREEN,30).move_to([4.5,-1.6,0])
        self.play(FadeIn(cursor),s[2][0][0].animate.set_fill(PURPLE,opacity=.6),run_time=.45)
        self.play(FadeIn(feedback),Flash(s[2][0],color=GREEN,flash_radius=.9),run_time=.5)
        self.at('Each card predicted')
        bars=VGroup()
        for c,p in zip(s[1],[.7,.6,.55]):
            x=c.get_x();w=2.25
            bars.add(Rectangle(width=w,height=.22,color=GREY).move_to([x,-.5,0]),
                     Rectangle(width=w*p,height=.22,color=PURPLE,fill_opacity=.9).move_to([x-w*(1-p)/2,-.5,0]),
                     label(f'{p:.0%}',[x,-.94,0],28,PURPLE))
        self.play(FadeOut(feedback),FadeIn(bars),run_time=.6)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        l=Learning(full=True);self.add(l.base,head('Feedback accumulates across trials'),note('Illustrative learning trace · not the published figure'))
        # Twenty simulated hit/miss strips generated deterministically from the same linear learning model.
        rng=np.random.default_rng(41);strips=VGroup()
        for t in np.linspace(1,50,20):
            p=np.interp(t,[0,50],[.5,.7]);hits=rng.random(8)<p
            strip=VGroup(*[Line(l.axes.c2p(t,j*12+3),l.axes.c2p(t,j*12+9),
                               color=GREEN if hit else RED,stroke_width=3,stroke_opacity=.45)
                           for j,hit in enumerate(hits)])
            strips.add(strip)
        self.at('No single trial')
        self.play(LaggedStart(*[FadeIn(s) for s in strips],lag_ratio=.05),run_time=1.8)
        self.at('learned gradually')
        self.play(Create(l.curves['ctrl']),run_time=1.3)
        self.finish()


class S05(SpokenScene):
    def construct(self):
        paper=RoundedRectangle(width=10.6,height=5.9,corner_radius=.15,color=BLUE).move_to([0,.1,0])
        self.add(paper,note('Recall the training sessions themselves'))
        self.at('Afterwards')
        self.play(FadeIn(head('After training: a questionnaire')),run_time=.5)
        rows=VGroup()
        for i,y in enumerate([1.4,-.15,-1.7],1):
            rows.add(label(f'{i}.  About the training …',[-1.2,y+.35,0],28),
                     VGroup(*[Square(.48,color=BLUE) for _ in range(4)]).arrange(RIGHT,buff=1.15).move_to([0,y-.25,0]))
        self.at('a questionnaire')
        self.play(FadeIn(rows),run_time=.6)
        self.at('about the training')
        self.play(FadeIn(label('Illustrative design',[3.35,2.65,0],26,GREY)),run_time=.4)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        self.add(head('Three groups'),note('Parkinson’s disease: dopamine input to striatum falls'))
        for phrase,name,k,x in [('controls','Controls','ctrl',-4.4),('patients','Amnesic','am',0),('patients with',"Parkinson’s",'pd',4.4)]:
            person=VGroup(Circle(.46,color=GCOL[k]),RoundedRectangle(width=1.65,height=1.65,corner_radius=.4,color=GCOL[k]).shift(DOWN*1.35)).scale(1.2 if k!='pd' else 1).move_to([x,.65 if k!='pd' else 1.3,0])
            self.at(phrase)
            self.play(FadeIn(person),FadeIn(label(name,[x,-1.3 if k!='pd' else -.33,0],30,GCOL[k])),run_time=.45)
        self.at('whose striatum')
        # All anatomy and dopamine marks stay in the Parkinson's column.
        brain=brain_outline().scale(.48).move_to([4.45,-2.0,0])
        region=Ellipse(width=.6,height=.35,color=ORANGE,fill_opacity=.65).move_to([4.6,-2.05,0])
        tag=label('Striatum',[4.65,-2.98,0],28,ORANGE)
        leader=Line(region.get_bottom(),tag.get_top(),color=ORANGE)
        arrows=VGroup(*[Arrow([3.35,-1.5-j*.28,0],[4.3,-1.88-j*.16,0],
                            color=ORANGE,buff=.03,stroke_width=8,
                            max_tip_length_to_length_ratio=.22) for j in range(3)])
        self.play(FadeIn(brain),FadeIn(region),FadeIn(tag),Create(leader),Create(arrows),
                  FadeIn(label('Dopamine',[4.4,-1.03,0],28,ORANGE)),run_time=.6)
        self.at('loses dopamine input')
        self.play(arrows[0].animate.set_opacity(.1),arrows[1].animate.set_opacity(.25),
                  arrows[2].animate.set_stroke(width=2).set_opacity(.45),run_time=.9)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        l=Learning(full=True);self.add(l.base,legend(),head('Learning classification over the first 50 trials'),note('Illustrative pattern · not the published figure'))
        self.at('Over the first')
        self.play(Create(l.curves['ctrl']),Create(l.curves['am']),run_time=2)
        self.at('controls and')
        self.play(l.curves['am'].animate.set_stroke(width=7),run_time=.4)
        self.at('failed to learn')
        self.play(Create(l.curves['pd']),run_time=.6)
        self.finish()


class S08(SpokenScene):
    def construct(self):
        l=Learning(full=True);lg=legend();self.add(l.all,lg)
        small=Learning();r=Questionnaire();r.base[1].move_to([3.45,2.32,0])
        self.at('simplest difficulty model')
        self.play(Transform(l.all,small.all),Transform(lg,legend(compact=True)),FadeIn(r.base),FadeIn(r.questions),FadeIn(head('Simple difficulty model · one common capacity')),run_time=.65)
        self.at('Suppose the questionnaire')
        self.play(Indicate(r.base[1],color=BLUE,scale_factor=1.04),run_time=.5)
        self.at('harder task')
        self.play(FadeIn(label('harder?',[3.45,3.08,0],30,BLUE)),run_time=.4)
        self.at('failed the easier')
        self.play(Indicate(l.all[-1],color=ORANGE,scale_factor=1.01),run_time=.4)
        self.at('How should they')
        self.play(FadeIn(note('How should they do on the questionnaire?')),Indicate(r.questions,color=TEXT,scale_factor=1.1),run_time=.6)
        self.finish()


class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        g,_,_=panels(model=True,question=True)
        # The timer's tag takes the title slot in both pauses.
        g.remove(g[-3])
        g.scale(.93).shift(UP*.2)
        self.add(g,note('How should they do on the questionnaire?',y=-3.32));timer(self)


class S10(SpokenScene):
    def construct(self):
        g,l,r=panels(model=True,question=True);self.add(g)
        cap=note('One common capacity predicts failure on both tasks');self.add(cap)
        self.at('they should fail')
        self.play(Indicate(r.questions,color=TEXT,scale_factor=1.08),run_time=.45)
        self.at('Instead')
        self.play(FadeOut(r.questions),GrowFromEdge(r.bars['pd'],DOWN),Transform(cap,note('Instead, Parkinson’s patients remembered the training')),run_time=.65)
        # Establish control reference before its gain enters the formula.
        self.play(GrowFromEdge(r.bars['ctrl'],DOWN),FadeIn(label('80%',[r.axes.c2p(1,80)[0],1.6,0],28,GREY)),run_time=.4)
        self.finish()


class S11(SpokenScene):
    def construct(self):
        g,l,r=panels(('ctrl','pd'),model=True);self.add(g,note('Training memory and classification come apart · controls: 80%'))
        self.at('severely impaired memory')
        self.play(GrowFromEdge(r.bars['am'],DOWN),run_time=.65)
        self.at('Yet they learned')
        self.play(l.curves['am'].animate.set_stroke(width=9),l.curves['ctrl'].animate.set_opacity(.25),l.curves['pd'].animate.set_opacity(.25),run_time=.65)
        self.finish()


class S12(SpokenScene):
    def construct(self):
        base,lines,a,nums=crossing();self.add(base,lines[0],head('No single order of difficulty fits both groups'))
        # Start with the amnesic line: the opening sentence already describes its order.
        self.add(lines[1])
        self.at('no single order')
        self.play(Create(lines[2]),run_time=1)
        self.at('Each group does')
        self.play(FadeIn(nums),run_time=.5)
        self.at('the lines cross')
        am,pd=[np.array(VALS[k],dtype=float) for k in ('am','pd')]
        x=(am[0]-pd[0])/((pd[1]-pd[0])-(am[1]-am[0]))
        ring=Circle(radius=.36,color=TEXT,stroke_width=5).move_to(a.c2p(x,np.interp(x,[0,1],am)))
        self.play(FadeIn(ring),run_time=.2)
        self.play(ring.animate.scale(1.35),run_time=1.0,rate_func=there_and_back)
        self.wait(1.4)
        self.at('group averages')
        cap=note('Group averages · against the simplest difficulty account')
        self.play(FadeOut(ring),FadeIn(cap),run_time=.45)
        self.at('rather than ruling out')
        self.play(FadeOut(cap),run_time=.15)
        self.play(FadeIn(note('Does not rule out every single-capacity account')),run_time=.3)
        self.finish()


def die(face):
    spots={1:[(0,0)],3:[(-.25,-.25),(0,0),(.25,.25)],5:[(-.25,-.25),(-.25,.25),(0,0),(.25,-.25),(.25,.25)]}
    return VGroup(Square(.95,color=TEXT,fill_color=BG,fill_opacity=1),
                  *[Dot([x,y,0],radius=.065,color=TEXT) for x,y in spots[face]]).move_to([6.15,1.6,0])


class S13(SpokenScene):
    def construct(self):
        g,l,r=panels(('ctrl','am','pd'));self.add(g,note('Some correct answers come from guessing'))
        d=die(1)
        self.at('Now a trap')
        self.play(FadeIn(d),FadeIn(label('guessing',[5.9,.72,0],26)),run_time=.4)
        self.play(Rotate(d,PI/2),run_time=.3)
        self.play(Transform(d,die(3)),run_time=.25)
        self.wait(.7)
        self.at('right by guessing')
        self.play(Rotate(d,-PI/2),run_time=.3)
        self.play(Transform(d,die(5)),run_time=.25)
        self.finish()


class S14(SpokenScene):
    def construct(self):
        g,l,r=panels(('ctrl','am','pd'));self.add(g,die(5),label('guessing',[5.9,.72,0],26),note('Expected score from guessing · illustrative design'))
        self.at('guessing alone gets')
        self.play(FadeIn(baseline(l.axes,50,'50% = guessing')),run_time=.6)
        self.at('it gets a quarter')
        self.play(FadeIn(baseline(r.axes,25,'25% = guessing')),run_time=.6)
        self.finish();self.wait(1.5)


class S15(SpokenScene):
    def construct(self):
        r=Questionnaire(full=True);self.add(r.base,*r.bars.values(),baseline(r.axes,25,'25% = chance'))
        # The equation has its own wide band; labels sit beside individual arrows.
        formula=label('relative score = (patient − chance) / (control − chance)',[0,3.55,0],28)
        self.add(note('Measure the gain above chance, then compare it with controls'))
        arrows=VGroup()
        for i,k in enumerate(GCOL,1):
            x=i+.34
            arrow=DoubleArrow(r.axes.c2p(x,25),r.axes.c2p(x,VALS[k][1]),buff=0,color=GCOL[k],tip_length=.1,stroke_width=4)
            arrows.add(arrow)
            txt=label('control − chance' if k=='ctrl' else 'patient − chance',
                      r.axes.c2p(i,VALS[k][1])+UP*.48,26,GCOL[k])
            arrows.add(txt)
        self.at('measure each score')
        self.play(Create(arrows),run_time=.6)
        self.at('as a share')
        self.play(FadeIn(formula),run_time=.6)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        self.add(head('Invented example · questionnaire'),note('Patient 40% · controls 80% · chance 25%'))
        a=Axes(x_range=[0,3,1],y_range=[0,100,25],x_length=6.3,y_length=4.85,axis_config={'color':GREY,'include_tip':False}).move_to([-2,-.15,0])
        for v in (0,25,50,80,100):
            self.add(T(str(v),28,GREY).next_to(a.c2p(0,v),LEFT,buff=.15))
        def bar(x,lo,hi,col):
            return Rectangle(width=1.2,height=4.85*(hi-lo)/100,color=col,fill_opacity=.7).move_to(a.c2p(x,(hi+lo)/2))
        p,c=bar(1,0,40,BLUE),bar(2,0,80,GREY)
        reading=label('40 / 80 = 50%',[3.5,1.6,0],34,BLUE)
        self.add(a,p,c,reading,label('Patient',a.c2p(1,0)+DOWN*.4,28,BLUE),label('Controls',a.c2p(2,0)+DOWN*.4,28,GREY))
        self.at('looks like half')
        self.play(Indicate(reading,color=BLUE,scale_factor=1.02),run_time=.3)
        self.at('shrinks')
        b=baseline(a,25,'25% = chance')
        self.play(FadeIn(b),Transform(p,bar(1,25,40,BLUE)),Transform(c,bar(2,25,80,GREY)),
                  FadeOut(reading),run_time=.8)
        self.play(FadeIn(label('15 / 55 = 27%',[3.5,1.6,0],34,BLUE)),run_time=.2)
        self.add(label('Gains above chance',[3.5,.65,0],28),label('(40 − 25) / (80 − 25)',[3.5,-.15,0],27))
        self.finish();self.wait(1.5)


class S17(SpokenScene):
    def construct(self):
        base,lines,a,nums=crossing();heading=head('Illustrative scores · raw → corrected')
        self.add(base,lines,nums,heading)
        ghost=lines.copy().set_opacity(.18);self.add(ghost)
        newbase,newlines,_,newnums=crossing(True)
        self.at('how big a loss')
        self.play(FadeOut(base[1]),FadeIn(newbase[1]),Transform(lines,newlines),FadeOut(nums),run_time=1.5)
        self.play(FadeIn(newnums),FadeIn(label('Faint lines: raw scores',[1.8,-1.95,0],26,GREY)),run_time=.3)
        self.at('controls beat chance')
        cap=note('Needs controls above chance')
        self.play(FadeIn(cap),run_time=.4)
        self.at('cannot change which')
        self.play(FadeOut(cap),run_time=.15)
        self.play(FadeIn(note('Same order on each task, so the lines still cross\n(needs controls above chance)',y=-3.43)),run_time=.3)
        self.at('crossing stays')
        self.play(pulse(a,True),run_time=.6)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        brain=brain_outline().scale(1.15).move_to([0,-.7,0])
        region=Ellipse(width=1.1,height=.65,color=ORANGE,fill_opacity=.55).move_to([-.4,-.8,0])
        box=chip('Learning from feedback',PURPLE,28).move_to([0,2.7,0])
        self.add(brain,region,box,label('Striatum',[-.5,-1.6,0],28,ORANGE),note('First 50 trials · see Going deeper'))
        others=VGroup(*[Ellipse(width=.85,height=.45,color=ORANGE,fill_opacity=.2).move_to([x,y,0]) for x,y in [(-2,-.2),(1.8,-1),(1.3,.2)]])
        connector=DashedLine(box.get_bottom(),region.get_top(),color=PURPLE,dash_length=.07)
        self.add(connector)
        self.at('damages more than')
        tag=label('Other regions\naffected',[4.6,-1,0],28,ORANGE)
        self.play(FadeIn(others),FadeIn(tag),Create(VGroup(Line([2.5,.5,0],[2.5,-1.5,0],color=ORANGE),Line([2.3,.5,0],[2.5,.5,0],color=ORANGE),Line([2.3,-1.5,0],[2.5,-1.5,0],color=ORANGE),Line([2.5,-1,0],tag.get_left(),color=ORANGE))),run_time=.7)
        self.at('separable learning processes')
        self.play(Indicate(box,color=TEXT,scale_factor=1.02),run_time=.5)
        self.at('without pinning each')
        self.play(connector.animate.set_opacity(.35),run_time=.5)
        self.finish()


class S19(SpokenScene):
    def construct(self):
        g=grid(2);self.add(g,note('Two measures of learning, in three patients'))
        self.at('a second crossing')
        self.play(Indicate(g[0],color=TEXT,scale_factor=1.02),run_time=.5)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        self.add(head('Pairing: signal → stimulus'))
        self.add(note('Pair a tone with an aversive stimulus; measure two outcomes'))
        signal=VGroup(chip('Tone',TEXT,34),*[Arc(radius=.5+j*.2,start_angle=-.7,angle=1.4,color=TEXT).shift(RIGHT*(1+j*.07)) for j in range(3)]).move_to([-3.4,1,0])
        stim=chip('Aversive stimulus',RED,32).move_to([3.1,1,0])
        self.at('A signal')
        self.play(FadeIn(signal),run_time=.4)
        self.at('paired with')
        self.play(GrowArrow(Arrow(signal.get_right(),stim.get_left(),color=GREY,buff=.2)),FadeIn(stim),run_time=.6)
        self.at('sweat response')
        ax=Axes(x_range=[0,5,1],y_range=[0,1,1],x_length=5.4,y_length=2.1,axis_config={'color':GREY,'include_tip':False}).move_to([-3,-1.3,0])
        trace=ax.plot(lambda t:0 if t<1 else 1.4*(np.exp(-(t-1)/2)-np.exp(-(t-1)/.25)),x_range=[0,5,.03],color=PURPLE)
        self.play(FadeIn(ax),Create(trace),FadeIn(label('Typical sweat response',[-3,-2.7,0],28,PURPLE)),run_time=.6)
        self.add(label('schematic',[-3,-3.13,0],26,GREY))
        self.at('report the pairing')
        bubble=VGroup(RoundedRectangle(width=5.1,height=2.1,corner_radius=.3,color=BLUE),label('Tone → stimulus',[0,0,0],32,BLUE)).move_to([3.2,-1.35,0])
        self.play(FadeIn(bubble),FadeIn(label('Can report the pairing?',[3.2,-2.8,0],28,BLUE)),run_time=.5)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        self.add(grid(2),note('Amygdala damage: report without conditioned sweat response'))
        self.at('could report the pairing')
        self.play(FadeIn(result(True,4,ROW_Y[0],True)),run_time=.45)
        self.at('no conditioned response')
        self.play(FadeIn(result(False,COL_X[0],ROW_Y[0])),run_time=.45)
        self.finish()


class S22(SpokenScene):
    def construct(self):
        self.add(grid(2,1),note('Hippocampal damage: conditioned response without report'))
        self.at('showed the reverse')
        self.play(FadeIn(result(True,COL_X[0],ROW_Y[1])),FadeIn(result(False,4,ROW_Y[1],True)),run_time=.5)
        self.finish()


class S23(SpokenScene):
    def construct(self):
        g=grid(2,2);self.add(g,note('What happens after damage to both structures?'))
        self.at('Predict the third')
        self.play(Transform(g,grid(3,2,True)),run_time=.45)
        self.finish()


class S24Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        g=grid(3,2,True);g.remove(g[0]);self.add(g,note('What happens after damage to both structures?',y=-3.32));timer(self)


class S25(SpokenScene):
    def construct(self):
        g=grid(3,2,True);self.add(g,note('Damage to both: neither response nor report'))
        self.at('learned neither')
        self.play(FadeOut(g[-2]),FadeOut(g[-1]),FadeIn(result(False,COL_X[0],ROW_Y[2])),FadeIn(result(False,4,ROW_Y[2],True)),run_time=.45)
        self.finish();self.wait(1.5)


def synthesis():
    g=VGroup(head('Two crossings · in these studies'))
    for x,title,c in [(-3.3,'Reported (declarative)',BLUE),(3.3,'Shown in performance',PURPLE)]:
        box=RoundedRectangle(width=6.1,height=5.6,corner_radius=.2,color=c).move_to([x,-.05,0])
        g.add(box,label(title,[x,2.25,0],30,c))
    for x,rows,c in [(-3.3,[('Bechara · single patients','Hippocampal damage'),('Knowlton · group averages','Amnesia')],BLUE),
                     (3.3,[('Bechara · single patients','Amygdala damage'),('Knowlton · group averages',"Parkinson’s disease")],PURPLE)]:
        for y,(study,damage) in zip([.9,-1.45],rows):
            g.add(label(study,[x,y+.35,0],26,GREY),label('Lost with',[x,y-.15,0],28),label(damage,[x,y-.75,0],30,c))
    return g


class S26(SpokenScene):
    def construct(self):
        g=synthesis();self.add(g,note('Single patients and group averages · suggestive, not proof'))
        self.at('memory that could be reported')
        self.play(g[1].animate.set_fill(BLUE,opacity=.12),run_time=.4)
        self.at('memory shown in performance')
        self.play(g[3].animate.set_fill(PURPLE,opacity=.12),run_time=.4)
        self.at('depended on different structures')
        self.play(Indicate(VGroup(g[7],g[10],g[13],g[16]),scale_factor=1.02,color=TEXT),run_time=.5)
        self.finish()


class S27End(EndCard):
    LINE='In these studies, reportable memory and memory shown in performance failed separately, after damage to different structures.'

    def construct(self):
        self.add(head('In these studies'))
        line=T('Reportable memory and memory\nshown in performance failed separately,\nafter damage to different structures.',size=36,font=TITLE_FONT,line_spacing=1.3)
        self.add(line,label('Single patients and group averages;\nsuggestive, not proof',[0,-2.15,0],28,GREY),label('biochemistrypedia.com',[0,-3.2,0],26,TEAL))
        self.finish();self.wait(3)
