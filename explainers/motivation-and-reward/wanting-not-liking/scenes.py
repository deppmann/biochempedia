"""Wanting Is Not Liking — reviewed, word-timed animation.
COLOR MAP: YELLOW reward/food; BLUE cue; GREEN positive prediction error;
RED negative prediction error; TEAL DAT; PURPLE dopamine; GREY structure;
TEXT neutral marks. No molecular structures. Traces use the Gaussian response
kernel from scenes.old.py (schematic responses, not measured firing rates).
Runway positions are computed from one speed and explicit pause intervals.
"""
from bp_style import *
import numpy as np

PURPLE = '#B58CD9'
_BaseSpokenScene = SpokenScene


class SpokenScene(_BaseSpokenScene):
    # Same word alignment without modifying the existing sync.log artifact.
    def at(self, phrase, lead=.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > .02:
            self.wait(rest)


def heading(s, color=TEXT):
    return T(s, 36, color, weight=BOLD).move_to([0, 3.12, 0])


def face(reaction='neutral', scale=1, species='rat'):
    er = .48 if species == 'mouse' else .35
    ears = VGroup(*[Circle(er, color=GREY, fill_color=GREY, fill_opacity=.25).move_to([x, .94, 0]) for x in (-.79,.79)])
    head = Ellipse(width=2.05, height=2.45, color=GREY, fill_color=BG, fill_opacity=1)
    eyes = VGroup(*[Dot([x,.34,0],.075,color=TEXT) for x in (-.4,.4)])
    nose = Triangle(color=GREY,fill_color=GREY,fill_opacity=1).scale(.12).rotate(PI).move_to([0,-.23,0])
    whiskers = VGroup(*[Line([s*.48,-.35,0],[s*1.35,y,0],color=GREY,stroke_width=2) for s in (-1,1) for y in (-.1,-.56)])
    if reaction == 'tongue':
        mouth = VGroup(Line([-.3,-.61,0],[.3,-.61,0],color=TEXT),RoundedRectangle(width=.3,height=.46,corner_radius=.12,color=TEXT,fill_color=TEXT,fill_opacity=1).move_to([.10,-.87,0]))
    elif reaction == 'gape':
        mouth = Ellipse(width=.58,height=.68,color=TEXT,fill_color=BG,fill_opacity=1).move_to([0,-.8,0])
    else:
        mouth = Line([-.25,-.66,0],[.25,-.66,0],color=TEXT)
    return VGroup(ears,head,eyes,nose,whiskers,mouth).scale(scale)


def taste_drop(color):
    # A filled droplet, distinct from the round dopamine markers.
    return VMobject(color=color,fill_color=color,fill_opacity=1).set_points_as_corners([
        [0,.27,0],[-.18,-.04,0],[-.15,-.19,0],[0,-.25,0],
        [.15,-.19,0],[.18,-.04,0],[0,.27,0]])


def smile():
    return VGroup(Circle(.7,color=TEXT),Dot([-.23,.18,0],.055,color=TEXT),Dot([.23,.18,0],.055,color=TEXT),Arc(radius=.36,start_angle=PI,angle=PI,color=TEXT).shift(UP*.02))


def mouse():
    body=Ellipse(width=1.35,height=.62,color=GREY,fill_color=GREY,fill_opacity=.3)
    head=Circle(.32,color=GREY,fill_color=BG,fill_opacity=1).move_to([.65,.15,0])
    tail=VMobject(color=GREY).set_points_smoothly([[-.66,0,0],[-.96,-.06,0],[-1.12,.15,0],[-1.04,.3,0]])
    return VGroup(tail,body,head,Circle(.17,color=GREY).move_to([.5,.43,0]),Dot([.78,.22,0],.04,color=TEXT),*[Line([x,-.23,0],[x+.15,-.37,0],color=GREY) for x in (-.35,.3)])


def dish():
    return VGroup(Ellipse(width=1.25,height=.35,color=YELLOW),Arc(radius=.62,start_angle=PI,angle=PI,color=YELLOW).stretch(.35,1).shift(DOWN*.07),Dot([0,.13,0],.12,color=YELLOW))


# Identical face stage throughout the experimental comparison scenes.
FACE_POS = [-3.9,1.48,0]
FACE_SCALE = .79
COL = [-4.25,-.45,3.8]
ROW = [-1.16,-2.39]


def grid(down=None, up=None, unknown=False, active='down'):
    border=Rectangle(width=12.1,height=3.5,color=GREY,stroke_width=2).move_to([0,-1.36,0])
    lines=VGroup(*[Line([-6.05,y,0],[6.05,y,0],color=GREY) for y in (-.55,-1.78)],*[Line([x,-3.11,0],[x,.39,0],color=GREY) for x in (-2.45,1.65)])
    headers=VGroup(*[T(s,26,c).move_to([x,-.08,0]) for s,x,c in zip(('Dopamine','Seeks food','Face to sugar'),COL,(PURPLE,TEXT,TEXT))])
    rowlabels=VGroup(VGroup(T('Down',28,PURPLE),T('(neurotoxin, rats)',26)).arrange(DOWN,buff=.1).move_to([COL[0],ROW[0],0]),VGroup(T('Up',28,PURPLE),T('(DAT 10%, mice)',26)).arrange(DOWN,buff=.1).move_to([COL[0],ROW[1],0]))
    highlight=Rectangle(width=12.0,height=1.18,color=PURPLE,fill_color=PURPLE,fill_opacity=.08,stroke_width=3).move_to([0,ROW[0 if active=='down' else 1],0]) if active else VGroup()
    results=VGroup()
    if down:
        results.add(T('Falls',30).move_to([COL[1],ROW[0],0]))
        if down=='normal': results.add(T('Normal liking',28).move_to([COL[2],ROW[0],0]))
    if unknown: results.add(T('?',44).move_to([COL[2],ROW[0],0]))
    if up:
        results.add(T('Rises',30).move_to([COL[1],ROW[1],0]))
        if up=='same': results.add(T('No stronger',28).move_to([COL[2],ROW[1],0]))
    return VGroup(highlight,border,lines,headers,rowlabels,results)


def depleted_title():
    return T('Forebrain dopamine depleted',30,PURPLE).move_to([0,3.17,0])


def prompt():
    return VGroup(T('If dopamine carried pleasure,',28),T('what should the face do?',30)).arrange(DOWN,buff=.2).move_to([1.65,1.65,0])


def question_frame():
    return VGroup(grid(down='seeking',unknown=True),face(scale=FACE_SCALE).move_to(FACE_POS),Dot([-3.82,.78,0],.13,color=YELLOW),prompt(),depleted_title())


def response_trace(cx,cy,width=4,height=1,sign=1,color=PURPLE,center=.35):
    # Gaussian event-response kernel, same equation as the reference film.
    ts=np.linspace(0,1,201)
    vals=sign*np.exp(-((ts-center)/.055)**2)
    pts=[[cx+width*(t-.5),cy+height*v,0] for t,v in zip(ts,vals)]
    return VGroup(Line([cx-width/2,cy,0],[cx+width/2,cy,0],color=GREY,stroke_width=1.5),VMobject(color=color,stroke_width=4).set_points_as_corners(pts))


class S00Title(TitleCard):
    LESSON='Feeding, Motivation and Reward'
    TITLE='Wanting Is Not Liking'


class S01Question(SpokenScene):
    def construct(self):
        # Connected lobes and branched sulci form a recognisable brain silhouette.
        lobes=[Circle(.66).move_to([x,y,0]) for x,y in ((-1,-.1),(-.95,.65),(-.4,1.1),(.35,1.1),(.95,.6),(1,-.15),(.4,-.5),(-.4,-.5))]
        outline=Union(Circle(.95),*lobes,color=PURPLE,fill_color=PURPLE,fill_opacity=.17)
        fold_controls = [
            ((-1.12,.23),(-.62,.05),(-.95,.93),(-.34,.87)),
            ((-.65,-.28),(-.13,-.3),(-.5,.5),(-.03,.55)),
            ((.1,.98),(-.02,.45),(.95,.85),(.75,.19)),
            ((.15,-.38),(.7,-.32),(.2,.19),(.52,.32)),
        ]
        folds=VGroup(*[CubicBezier(*[np.array([x,y,0]) for x,y in pts],color=PURPLE,stroke_width=3) for pts in fold_controls])
        brain=VGroup(outline,folds).scale(1.4).move_to([-3.7,-.2,0])
        f=smile().scale(2.25).move_to([3.8,-.2,0])
        arrow=Arrow([-1.25,1.3,0],[1.6,1.3,0],color=PURPLE,buff=0)
        label=chip('Dopamine',PURPLE,30).move_to([0,2.15,0])
        self.add(brain,f,heading('Wanting is not liking'))
        self.at('dopamine the'); self.play(FadeIn(label),GrowArrow(arrow),run_time=.45)
        self.at('pleasure signal'); self.play(FadeIn(T('?',100).move_to([0,-.4,0])),run_time=.45)
        self.at("let's test it"); self.play(FadeIn(T('Let’s test it',32).move_to([0,-2.9,0])),run_time=.4)
        self.finish()


class S02Terms(SpokenScene):
    def construct(self):
        a=face(scale=1.05).move_to([-4.5,-.1,0]); food=dish().scale(1.15).move_to([-.95,-.1,0]); f=smile().scale(2.3).move_to([3.7,-.1,0])
        self.add(T('Wanting',42,YELLOW).move_to([-3,2.8,0]),T('Liking',42).move_to([3.7,2.8,0]),a,food,f,Line([.8,-3.1,0],[.8,3.15,0],color=GREY,stroke_width=1))
        self.at('wanting is'); self.play(GrowArrow(Arrow([-3.1,0,0],[-1.8,0,0],color=YELLOW,buff=0)),a.animate.shift(RIGHT*.2),FadeIn(T('the pull',32,YELLOW).move_to([-3,-2.75,0])),run_time=.6)
        self.at('liking is'); self.play(Indicate(f,color=YELLOW),FadeIn(T('the pleasure itself',32).move_to([3.7,-2.75,0])),run_time=.6)
        self.finish()


class S03Measure(SpokenScene):
    def construct(self):
        f=face(scale=1.75).move_to([0,-.2,0]); self.add(f,heading('How can we measure liking?'))
        self.at('without asking'); self.play(FadeIn(chip('Without asking',TEXT,28).move_to([4.2,1.2,0])),run_time=.4)
        self.at('watch its face'); self.play(f[2].animate.stretch(.12,1),run_time=.12); self.play(f[2].animate.stretch(1/.12,1),run_time=.12)
        self.play(Create(SurroundingRectangle(f[-1],color=YELLOW,buff=.25)),run_time=.45)
        self.finish()


class S04Faces(SpokenScene):
    def construct(self):
        a=face(scale=1.55).move_to([-3.25,0,0]); b=face(scale=1.55).move_to([3.25,0,0]); self.add(a,b)
        self.at('sweet tastes'); d=taste_drop(YELLOW).move_to([-4.8,1.4,0]); self.play(FadeIn(T('Sweet',34,YELLOW).move_to([-3.25,2.8,0])),FadeIn(d),run_time=.2); self.play(d.animate.move_to([-3.1,-1.1,0]),run_time=.5)
        self.at('tongue protrusions'); self.play(FadeOut(d),Transform(a,face('tongue',1.55).move_to([-3.25,0,0])),FadeIn(T('Tongue protrusion',28).move_to([-3.25,-2.45,0])),run_time=.4)
        self.at('bitter tastes'); d2=taste_drop(YELLOW).move_to([4.8,1.4,0]); self.play(FadeIn(T('Bitter',34,YELLOW).move_to([3.25,2.8,0])),FadeIn(d2),run_time=.2); self.play(d2.animate.move_to([3.25,-1.1,0]),run_time=.45)
        self.at('gapes'); self.play(FadeOut(d2),Transform(b,face('gape',1.55).move_to([3.25,0,0])),FadeIn(T('Gape',28).move_to([3.25,-2.45,0])),run_time=.4)
        self.at('scored from video'); vf=VGroup(VGroup(*[Rectangle(width=1.25,height=1.05,color=TEAL,stroke_width=2).move_to([x,-1.12,0]) for x in (-3.25,3.25)]),T('Taste reactivity  |  video scoring',28,TEAL).move_to([0,-3.22,0]))
        self.play(FadeIn(vf),run_time=.4); self.finish()


class S05Depleted(SpokenScene):
    def construct(self):
        rat=mouse().scale(1.3).move_to([-3.4,1.65,0]); food=dish().scale(1.2).move_to([3.5,1.6,0]); g=grid()
        self.add(rat,food,g,depleted_title())
        self.at('stopped seeking food'); self.play(rat.animate.flip(UP),FadeIn(T('Falls',30).move_to([COL[1],ROW[0],0])),run_time=.6)
        self.finish()


class S06Q(SpokenScene):
    def construct(self):
        self.add(grid(down='seeking'),face(scale=FACE_SCALE).move_to(FACE_POS),depleted_title())
        self.at('if dopamine'); self.play(FadeIn(prompt()),run_time=.45)
        self.at('what should their faces'); self.play(FadeIn(T('?',44).move_to([COL[2],ROW[0],0])),run_time=.35)
        self.at('sugar is placed'); d=Dot([-1.8,1.5,0],.13,color=YELLOW); self.play(FadeIn(d),run_time=.15); self.play(d.animate.move_to([-3.82,.78,0]),run_time=.75)
        self.finish()


class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question_frame())
        ring=Circle(.36,color=GREY,stroke_width=3).move_to([5.15,ROW[0],0])
        t=ValueTracker(0)
        arc=always_redraw(lambda: Arc(radius=.36,start_angle=PI/2,angle=-TAU*max(.001,1-t.get_value()/5),color=YELLOW,stroke_width=5).move_arc_center_to([5.15,ROW[0],0]))
        self.add(ring,arc); self.play(t.animate.set_value(5),run_time=5,rate_func=linear)


class S08Reveal(SpokenScene):
    def construct(self):
        f=face(scale=FACE_SCALE).move_to(FACE_POS); q=prompt(); mark=T('?',44).move_to([COL[2],ROW[0],0])
        self.add(grid(down='seeking'),f,q,mark,depleted_title())
        self.at('their faces showed'); self.play(Transform(f,face('tongue',FACE_SCALE).move_to(FACE_POS)),run_time=.4)
        self.at('normal liking reactions'); self.play(FadeOut(mark),FadeIn(T('Normal liking',28).move_to([COL[2],ROW[0],0])),FadeOut(q),run_time=.4)
        self.at('the seeking was gone'); self.play(Create(Line([COL[1]-.48,ROW[0]-.32,0],[COL[1]+.48,ROW[0]-.32,0],color=YELLOW,stroke_width=4)),run_time=.6)
        self.at('liking reactions remained')
        self.finish()


# Enlarged membrane panels. DAT labels have their own dark backing; membrane
# strokes are never drawn through their letters. Dots are schematic, not counts.
def synapse_panel(cx,title,mutant=False):
    top=RoundedRectangle(width=5.55,height=1.45,corner_radius=.12,color=GREY,fill_color=GREY,fill_opacity=.1).move_to([cx,1.4,0])
    bottom=RoundedRectangle(width=5.55,height=1.35,corner_radius=.12,color=GREY,fill_color=GREY,fill_opacity=.1).move_to([cx,-1.55,0])
    labs=VGroup(T(title,30,TEAL if mutant else TEXT).move_to([cx,2.72,0]),T('Terminal',26).move_to([cx,1.7,0]),T('Receiving cell',26).move_to([cx,-1.55,0]))
    dats=VGroup(*[chip('DAT',TEAL,26).move_to([cx+dx,.69,0]) for dx in (-1.8,-.6,.6,1.8)])
    for dat in dats: dat[0].set_fill(BG,1)
    pts=[(-2,-.1),(-1,-.55),(0,.05),(1.2,-.4),(2,-.05)]
    dots=VGroup(*[Dot([cx+x,y,0],.1,color=PURPLE) for x,y in pts])
    return VGroup(top,bottom,labs,dats,dots)


class S09Other(SpokenScene):
    def construct(self):
        normal=synapse_panel(-3.15,'Normal'); mutant=synapse_panel(3.15,'Low DAT')
        self.add(normal,mutant,heading('Dopamine up',PURPLE).move_to([0,3.4,0]))
        self.add(T('Up (DAT 10%, mice)',28,PURPLE).move_to([0,-3.15,0]))
        self.at('make little of'); self.play(*[FadeOut(d) for d in mutant[3][1:]],run_time=.5)
        lab=T('DAT ≈ 10% of normal',26,TEAL).move_to([3.85,1.15,0])
        self.play(FadeIn(lab),run_time=.3)
        self.at('extra dopamine stays')
        # Release sequentially from the open terminal edge into the gap.
        for x,y in ((-1.6,.1),(-.5,-.25),(.5,-.55),(1.7,.25)):
            d=Dot([3.15+x,.62,0],.1,color=PURPLE)
            self.add(d)
            self.play(d.animate.move_to([3.15+x,y,0]),run_time=.23,rate_func=linear)
        self.play(FadeIn(T('≈ 70% more extracellular striatal dopamine',27,PURPLE).move_to([0,-2.55,0])),run_time=.35)
        self.finish()


class S10Runway(SpokenScene):
    def construct(self):
        self.add(heading('Sweet-food runway'))
        ys=[1.15,-1.8]
        a=mouse().scale(.64).move_to([-4.3,ys[0],0]); b=mouse().scale(.64).move_to([-4.3,ys[1],0])
        for y,label,c in zip(ys,('Control','Low DAT'),(TEXT,TEAL)):
            self.add(Rectangle(width=11.4,height=2.65,color=GREY).move_to([0,y,0]),T(label,28,c).move_to([-4.6,y+.8,0]),dish().scale(.7).move_to([4.8,y,0]),Line([4,y-.85,0],[4,y+.55,0],color=YELLOW,stroke_width=4))
        self.add(a,b)
        # A single speed, 3 x 0.6-second control stops, zero low-DAT stops.
        speed=1.75; start=-4.3; finish=3.15; stops=((1.5,2.1),(2.9,3.5),(4.25,4.85))
        clock=ValueTracker(0)
        def distance(t,paused):
            lost=sum(max(0,min(t,e)-s) for s,e in stops) if paused else 0
            return min(finish-start,speed*max(0,t-lost))
        a.add_updater(lambda m: m.move_to([start+distance(clock.get_value(),True),ys[0],0]))
        b.add_updater(lambda m: m.move_to([start+distance(clock.get_value(),False),ys[1],0]))
        # Updater drives the same model through the independently timed labels.
        clock.add_updater(lambda m,dt:m.increment_value(dt)); self.add(clock)
        for y,paused in zip(ys,(True,False)):
            icon=VGroup(Circle(.15,color=TEXT),Line([0,0,0],[0,.1,0],color=TEXT)).move_to([3.05,y+.8,0])
            timer=DecimalNumber(0,num_decimal_places=1,font_size=26,mob_class=Text).move_to([3.7,y+.8,0])
            arrival=(finish-start)/speed+(1.8 if paused else 0)
            timer.add_updater(lambda m,cap=arrival:m.set_value(min(clock.get_value(),cap)))
            self.add(icon,timer)
        for s,e in stops:
            x=start+distance(s,True)
            tick=VGroup(Line([x-.08,ys[0]-.7,0],[x-.08,ys[0]-.4,0],color=YELLOW),Line([x+.08,ys[0]-.7,0],[x+.08,ys[0]-.4,0],color=YELLOW))
            tick.add_updater(lambda m,begin=s:m.set_opacity(1 if clock.get_value()>=begin else 0))
            self.add(tick)
        self.at('they reached sweet food')
        self.at('they ran no faster'); self.play(FadeIn(T('Same running speed',28).move_to([-.6,1.95,0])),FadeIn(T('Same running speed',28).move_to([-.6,-1.,0])),run_time=.3)
        self.at('they just paused less'); self.play(FadeIn(T('3 pauses',28,YELLOW).move_to([0,.12,0])),FadeIn(T('Fewer pauses: 0',28,TEAL).move_to([0,-2.83,0])),run_time=.3)
        self.finish(); clock.clear_updaters(); a.clear_updaters(); b.clear_updaters()


class S11Liking(SpokenScene):
    def construct(self):
        self.add(grid(down='normal',up='seeking',active='up'),face('tongue',FACE_SCALE,'mouse').move_to(FACE_POS),T('Sugar response: mice',30).move_to([1.8,1.9,0]),T('Peciña and colleagues, 2003',26).move_to([1.8,1.0,0]))
        self.at('were no stronger'); self.play(FadeIn(T('No stronger',28).move_to([COL[2],ROW[1],0])),run_time=.3)
        self.finish()


class S12Sum(SpokenScene):
    def construct(self):
        g=grid(down='normal',up='same',active=None).scale(1.04).shift(UP*1.35)
        self.add(g,heading('In these tests'),T('Wanting',32,YELLOW).move_to([-.47,2.05,0]),T('Liking',32).move_to([3.99,2.05,0]))
        self.at('dopamine moved wanting'); self.play(Create(Rectangle(width=4.264,height=g[1].height,color=YELLOW).move_to([-.416,g[1].get_y(),0])),run_time=.5)
        self.at('not liking'); self.play(g[3][2].animate.set_opacity(.3),g[5][1].animate.set_opacity(.3),g[5][3].animate.set_opacity(.3),FadeIn(Line([2.6,-2.65,0],[5.4,-2.65,0],color=TEXT)),FadeIn(T('Liking stayed level',28,TEXT).move_to([3.95,-2.2,0])),run_time=.5)
        self.finish()


class S13Rule(SpokenScene):
    def construct(self):
        cage=Rectangle(width=11.4,height=3.65,color=GREY).move_to([0,.55,0])
        light=Circle(.37,color=BLUE,fill_color=BLUE,fill_opacity=.35).move_to([-4.3,1.4,0]); place=Rectangle(width=2.4,height=.6,color=BLUE,fill_color=BLUE,fill_opacity=.15).move_to([3.7,-.65,0]); rat=mouse().scale(1.1).move_to([0,-.4,0])
        self.add(cage,light,place,rat,heading('Cues'),T('light',28,BLUE).move_to([-3.15,1.4,0]),T('place',28,BLUE).move_to([3.7,.05,0]))
        self.at('recall the burst'); trace=response_trace(0,-2.15,10.5,.65,center=.25); self.play(Create(trace),FadeIn(T('Dopamine',26,PURPLE).move_to([-4.5,-3.0,0])),FadeIn(T('cue',26,BLUE).move_to([-2.62,-2.85,0])),run_time=.5)
        self.at('cues gaining pull'); self.play(light.animate.set_fill(BLUE,.85),place.animate.set_fill(BLUE,.5),Create(Circle(.6,color=BLUE,stroke_width=6).move_to(light)),rat.animate.shift(RIGHT*1.0).rotate(.12),run_time=.6)
        self.play(FadeIn(chip('Compatible',TEXT,28).move_to([.4,1.65,0])),run_time=.3)
        self.at('wanting is debated'); self.play(FadeIn(chip('Wanting? Debated.',TEXT,28).move_to([2.55,-3.0,0])),run_time=.4)
        self.finish()


def person():
    return VGroup(Circle(.32,color=TEXT).move_to([0,.52,0]),RoundedRectangle(width=.92,height=.85,corner_radius=.3,color=TEXT).move_to([0,-.2,0]))


def scope():
    mutation=VGroup(chip('Lifelong mutation',TEAL,28),T('lifelong',26,TEAL)).arrange(DOWN,buff=.22).move_to([-3,1.6,0])
    drug=VGroup(chip('Acute drug',TEXT,28),T('acute',26)).arrange(DOWN,buff=.22).move_to([3,1.6,0])
    animal=VGroup(face(scale=.69).move_to([-3,-.2,0]),T('Animal face',28).move_to([-3,-1.48,0]))
    human=VGroup(person().scale(1.125).move_to([3,-.2,0]),T('Human report',28).move_to([3,-1.48,0]))
    return VGroup(heading('Keep the scope'),mutation,drug,animal,human,T('≠',42).move_to([0,1.6,0]),T('≠',42).move_to([0,-.2,0]))


class S14Scope(SpokenScene):
    def construct(self):
        s=scope(); self.add(s[0],s[1][0],s[2][0],s[3][0],s[4][0])
        self.at('a lifelong mutation'); self.play(FadeIn(s[1][1]),Indicate(s[1][0],color=TEAL),run_time=.4)
        self.at('not an acute drug'); self.play(FadeIn(s[5]),FadeIn(s[2][1]),run_time=.4)
        self.at("an animal's face"); self.play(FadeIn(s[3][1]),run_time=.35)
        self.at('not a human report'); self.play(FadeIn(s[6]),FadeIn(s[4][1]),run_time=.35)
        self.finish()


class S15Debate(SpokenScene):
    def construct(self):
        self.add(scope())
        readings=VGroup(chip('Willingness to work',TEXT,28),chip('Learning',TEXT,28)).arrange(RIGHT,buff=.55).move_to([0,-3.12,0])
        self.at('other researchers'); self.play(FadeIn(T('Other readings of the results',30).move_to([0,-2.3,0])),run_time=.4)
        self.at('willingness to work'); self.play(FadeIn(readings[0]),run_time=.3)
        self.at('or in learning'); self.play(FadeIn(readings[1]),run_time=.3)
        self.finish()


class S16Drugs(SpokenScene):
    def construct(self):
        a=synapse_panel(-3.15,'Drug A'); b=synapse_panel(3.15,'Drug B')
        self.add(a,b,heading('Different routes to dopamine up',PURPLE).move_to([0,3.4,0]))
        drugs=VGroup(*[chip('Drug',TEXT,26).move_to([cx+1.65,1.65,0]) for cx in (-3.15,3.15)])
        self.at('addictive drugs'); self.play(FadeIn(drugs),run_time=.35)
        self.at('raise dopamine')
        # Block every extracellular DAT mouth, below the opaque lettering.
        blocks=VGroup(*[VGroup(
            Line([d.get_x()-.24,.18,0],[d.get_x()+.24,.42,0],color=TEXT,stroke_width=5),
            Line([d.get_x()-.24,.42,0],[d.get_x()+.24,.18,0],color=TEXT,stroke_width=5)
        ) for d in a[3]])
        mechanism=VGroup(T('block',26).move_to([-3.15,-.35,0]),T('reverse',26).move_to([3.15,-.35,0]))
        self.play(Create(blocks),FadeIn(mechanism[0]),run_time=.3)
        # Molecules cannot return through the blocked mouths and accumulate.
        retained=VGroup(*[Dot([-3.15+x,.05,0],.1,color=PURPLE) for x in (-1.8,-.6,.6,1.8)])
        self.add(retained)
        self.play(*[d.animate.shift(DOWN*(.65+.12*(i%2))) for i,d in enumerate(retained)],run_time=.35,rate_func=linear)
        self.at('by different routes')
        arrows=VGroup(*[Arrow([3.15+x,1.12,0],[3.15+x,-.05,0],color=PURPLE,buff=0,stroke_width=4).set_z_index(2) for x in (-1.8,1.8)])
        b[3].set_z_index(3)
        self.play(*[GrowArrow(ar) for ar in arrows],FadeIn(mechanism[1]),run_time=.3)
        # Successive packets stream from the terminal, through reversed DAT.
        for packet in range(3):
            src=VGroup(*[Dot([3.15+x,1.12,0],.1,color=PURPLE).set_z_index(4) for x in (-1.8,1.8)])
            self.add(src)
            self.play(*[d.animate.move_to([d.get_x(),-.18-.27*packet,0]) for d in src],run_time=.32,rate_func=linear)

        self.finish()


def sensitization_stage():
    cue=Circle(.52,color=BLUE,fill_color=BLUE,fill_opacity=.45).move_to([-3.15,.0,0])
    f=smile().scale(1.7).move_to([3.15,0,0])
    rings=VGroup(*[Circle(r,color=BLUE,stroke_width=6,stroke_opacity=o).move_to(cue) for r,o in ((.8,.8),(1.1,.6),(1.4,.4),(1.7,.22))])
    labels=VGroup(T('Cue-triggered wanting',30,BLUE).move_to([-3.15,-2.3,0]),T('Liking',30).move_to([3.15,-2.3,0]),Line([1.8,-1.65,0],[4.5,-1.65,0],color=TEXT,stroke_width=3))
    return cue,f,rings,labels


class S17Sensitization(SpokenScene):
    def construct(self):
        cue,f,rings,labels=sensitization_stage(); self.add(cue,f,labels,heading('Incentive sensitization theory'))
        self.at('susceptible people'); self.play(FadeIn(T('In susceptible people',28).move_to([0,2.35,0])),run_time=.35)
        counter=chip('Trial 1',TEXT,28).move_to([0,1.25,0]); drug=chip('Drug',TEXT,28).move_to([0,.25,0])
        self.at('repeated use'); self.play(FadeIn(drug),FadeIn(counter),Create(rings[0]),run_time=.4)
        self.play(Transform(counter,chip('Trial 2',TEXT,28).move_to(counter)),Indicate(drug),Create(rings[1]),run_time=.45)
        self.at('wanting grow'); self.play(Transform(counter,chip('Trial 3',TEXT,28).move_to(counter)),Indicate(drug),Create(rings[2]),run_time=.45)
        self.play(Transform(counter,chip('Trial 4',TEXT,28).move_to(counter)),Indicate(drug),Create(rings[3]),run_time=.45)
        self.at('out of proportion to liking'); self.play(Indicate(labels[2],scale_factor=1,color=TEXT),FadeIn(T('Robinson and Berridge',26).move_to([0,-3.15,0])),run_time=.4)
        self.finish()


class S18Theory(SpokenScene):
    def construct(self):
        cue,f,rings,labels=sensitization_stage(); glow=VGroup(cue,rings); self.add(glow,f,labels,heading('One theory'))
        self.at('craving can outlast enjoyment'); self.play(f.animate.set_opacity(.12),FadeIn(T('Craving persists',30,BLUE).move_to([-3.15,-3.1,0])),run_time=.8)
        self.at('it is a theory'); self.play(glow.animate.scale(.65).move_to([-4,0,0]),FadeOut(f),FadeOut(labels),run_time=.4)
        self.at('other accounts exist'); alt=VGroup(T('Other accounts',30),*[chip(s,TEXT,28) for s in ('Habit','Prefrontal control','Withdrawal and stress')]).arrange(DOWN,buff=.35).move_to([2.15,-.2,0]); self.play(FadeIn(alt),run_time=.35)
        self.wait(2)
        self.finish()


class S19Takeaway(SpokenScene):
    def construct(self):
        main=VGroup(T('Dopamine moved wanting,',40,PURPLE),T('not liking.',40)).arrange(DOWN,buff=.2).move_to([0,2.,0])
        self.add(heading('In these tests'),main[0])
        self.at('not liking'); self.play(FadeIn(main[1]),run_time=.35)
        self.at('quick bursts'); b=VGroup(response_trace(-3.2,-.6,5.4,1.45,1,GREEN,.5),T('BURSTS',36,GREEN).move_to([-3.2,-1.2,0]),T('Better than predicted',32).move_to([-3.2,-1.9,0])); self.play(Create(b),run_time=.5)
        self.at('its pauses'); p=VGroup(response_trace(3.2,.85,5.4,1.45,-1,RED,.5),T('PAUSES',36,RED).move_to([3.2,-1.2,0]),T('Worse than predicted',32).move_to([3.2,-1.9,0])); self.play(Create(p),run_time=.5)
        self.at('not a direct measure'); self.play(FadeIn(T('Not a direct measure of pleasure',34).move_to([0,-3.05,0])),run_time=.5)
        self.finish()


class S20End(EndCard):
    LINE='In these tests, dopamine moved wanting, not liking.'
