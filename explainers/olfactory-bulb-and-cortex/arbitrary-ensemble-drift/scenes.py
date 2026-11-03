"""Teaching an Arbitrary Ensemble, and a Code That Drifts.
COLOR MAP (from scenes.old.py, shared with the series):
BLUE sister 1 / imposed optogenetic cells; YELLOW sister 2;
TEAL glomerular input and natural cortical activity; GREEN learned meaning/reward;
ORANGE timing/aversive outcome; PURPLE granule inhibition; GOLD tracer/light;
GREY labels, axes, electrodes, inactive cells; RED only strike-through no.
The lesson supplies qualitative decoding endpoints, not numerical trajectories.
Dashed guides connect those endpoints in qualitative display coordinates;
no fitted kinetics or measured intermediate scores are implied.
"""
import numpy as np
from bp_style import *
ORANGE = '#F29E4C'
PURPLE = '#B58CD9'
# Population geometry and memberships reused from the reference animation.
POSITIONS = [(-1.8,.75),(-.7,1),(.5,.65),(1.7,1),(-1.5,-.65),(-.25,-.3),(.8,-.9),(1.8,-.3)]
ACTIVE = (0,3,5,6)
LATER = (1,3,5,7)

def label(s, x=0, y=3.05, color=TEXT, size=30):
    return T(s,size,color).move_to([x,y,0])

def sheet(x=0,y=0,w=8,h=4.8,indices=ACTIVE,color=BLUE,title='piriform cortex'):
    natural = color == TEAL
    points = [(-1.9,.9),(-1.1,-.8),(-.6,.35),(0,-1),(.4,1),(1,.1),(1.7,-.7),(1.9,.95),(-1.8,-.1),(.1,.15),(1.1,1.1),(-.8,1.1)] if natural else POSITIONS
    border=RoundedRectangle(width=w,height=h,corner_radius=.22,color=TEAL if natural else BLUE,stroke_width=2)
    cells=VGroup()
    for i,(a,b) in enumerate(points):
        center=[a*w/5.1,b*h/3.5,0]
        d=(Ellipse(width=.25*w/5.1,height=.46*h/3.5) if natural else Dot(radius=.16*w/5.1)).move_to(center)
        d.set_color(color if i in indices else GREY).set_fill(color if i in indices else GREY,opacity=1 if i in indices else .3)
        cells.add(d)
    name=label(title,0,h/2+.36,TEXT,26)
    return VGroup(border,cells,name).shift([x,y,0])

def activity(c,indices=ACTIVE,color=BLUE):
    return [d.animate.set_color(color if i in indices else GREY).set_fill(color if i in indices else GREY,opacity=1 if i in indices else .3)
            for i,d in enumerate(c[1])]

def beam(x=0,y=0,bright=False):
    return VGroup(Polygon([x-.18,y+2,0],[x+.18,y+2,0],[x+1,y+.3,0],[x-1,y+.3,0],
                          stroke_color=YELLOW if bright else GOLD,stroke_width=3 if bright else 2,
                          fill_color=YELLOW if bright else GOLD,fill_opacity=.85 if bright else .55),
                  label('light',x,y+2.35,GOLD,26))

def mouse(x=0,y=0):
    body=Ellipse(width=2.6,height=1.25,color=GREY,fill_color=GREY,fill_opacity=.3)
    head=Ellipse(width=.95,height=.85,color=TEXT,fill_color=BG,fill_opacity=1).move_to([1.35,.25,0])
    ear=Circle(radius=.28,color=TEXT).move_to([1.1,.8,0])
    eye=Dot([1.55,.4,0],radius=.055,color=TEXT)
    nose=Dot([1.84,.16,0],radius=.07,color=TEXT)
    tail=ArcBetweenPoints([-2.1,-.35,0],[-1.25,0,0],angle=-.6,color=GREY)
    legs=VGroup(*[Line([i,-.5,0],[i+.2,-.9,0],color=GREY,stroke_width=4) for i in (-.7,.7)])
    return VGroup(body,head,ear,eye,nose,tail,legs).shift([x,y,0])

def spout(x,y):
    return VGroup(Line([x,y+.8,0],[x,y+.1,0],color=GREEN,stroke_width=6),
                  Line([x,y+.1,0],[x-.35,y-.1,0],color=GREEN,stroke_width=6))

def pair_stage():
    mice=VGroup(mouse(-3.4,-.5),mouse(3,-.5))
    lights=VGroup(beam(-3.4,-.5),beam(3,-.5))
    water=VGroup(spout(-1.1,-.6),label('water spout',-3.3,-2.25,GREEN,28),Dot([-1.4,-.85,0],radius=.09,color=GREEN))
    grid=VGroup(*[Line([1+i*.65,-1.65,0],[1.3+i*.65,-2.05,0],color=ORANGE,stroke_width=4) for i in range(6)],label('shock grid',3,-2.65,ORANGE,28))
    return mice,lights,water,grid

def q1():
    return VGroup(label('What will each group learn?',0,3.1,size=36),label('Did they smell anything?',0,2.25,GOLD,32))

def prediction_stage():
    m,b,w,g=pair_stage()
    return VGroup(m,b,w,g).shift(DOWN*.65).set_opacity(.38)

# Only qualitative endpoints are supplied by the lesson. Vertical coordinates
# encode high / above chance / near chance, never invented numerical accuracy.
X0,X1,YHIGH,YCHANCE=-4.6,4.8,1.65,-1.55

def day_x(day):
    return X0+(day-1)/31*(X1-X0)

def graph():
    ax=VGroup(Arrow([X0,-2.15,0],[X0,2.25,0],buff=0,color=GREY),Arrow([X0,-2.15,0],[5.5,-2.15,0],buff=0,color=GREY))
    labs=VGroup(label('Accuracy (% correct)',-2.9,2.7,TEXT,28),label('day 1',X0,-2.6,TEXT,26),label('day 32',X1,-2.6,TEXT,26),label('days',.5,-2.6,TEXT,26),label('high',-5.35,1.65,TEXT,26))
    chance=VGroup(DashedLine([X0,YCHANCE,0],[5.4,YCHANCE,0],color=GREY),label('chance = 100 / N %',1.4,-1.85,TEXT,26))
    note=VGroup(label('Qualitative endpoints only — no measured trajectory',0,-3.1,TEXT,26),label('N = number of odours; chance = random guessing',0,-3.55,TEXT,26))
    return VGroup(ax,labs,chance,note)

def curve(color=TEAL,slow=False):
    end=.45 if slow else -1.45
    # A dashed connector is an endpoint guide, not a measured trace or kinetic fit.
    guide=DashedLine([X0,YHIGH,0],[X1,end,0],color=color,stroke_width=3,dash_length=.14)
    return VGroup(guide,Dot([X1,end,0],radius=.12,color=color))

def curve_label(slow=False,frozen=False):
    text=label('daily exposure' if slow else ('frozen day-1 decoder' if frozen else 'no daily exposure'),1.6 if slow else -.9,1.2 if slow else -.85,GREEN if slow else TEAL,26)
    leader=Line([1.6,1,0],[1.6,.85,0],color=GREEN) if slow else Line([-.9,-.62,0],[-.9,.35,0],color=TEAL)
    return VGroup(text,leader)

def startpoint():
    return Dot([X0,YHIGH,0],radius=.12,color=TEAL)

def q2():
    return VGroup(graph(),startpoint(),label('A month later?',1.4,1.65,size=36))

class S00Title(TitleCard):
    LESSON='From Glomeruli to Piriform Cortex'
    TITLE='Teaching an Arbitrary Ensemble, and a Code That Drifts'
    def construct(self):
        self.add(label(self.LESSON,0,2.65,TEAL,26))
        title=VGroup(T('Teaching an Arbitrary Ensemble,',font=TITLE_FONT,size=42),T('and a Code That Drifts',font=TITLE_FONT,size=42)).arrange(DOWN,buff=.28)
        fit(title,11.8,3).move_to([0,.4,0])
        self.play(FadeIn(title),run_time=.6)
        self.add(Line([-1,-1.5,0],[1,-1.5,0],color=GOLD,stroke_width=4))
        self.finish()

class S01Question(SpokenScene):
    def construct(self):
        c=sheet()
        self.add(c)
        self.at('an ensemble of neurons')
        self.play(*activity(c),run_time=.45)
        self.at('what happens if')
        self.play(FadeIn(label('An ensemble without an odour?',0,-3.05,size=32)),run_time=.5)
        self.finish()

class S02Choi(SpokenScene):
    def construct(self):
        c=sheet(indices=(),h=4.6,y=-.1,title='imposed ensemble — piriform cortex')
        self.add(c,label('Choi and colleagues, 2011',0,3.35,TEXT,28))
        self.at('colleagues expressed')
        self.play(FadeIn(label('Imposed ensemble — not a natural odour ensemble',0,-2.95,BLUE,26)),run_time=.3)
        self.at('in subsets of')
        self.play(*activity(c),FadeIn(label('Blue = expresses channelrhodopsin',0,-3.5,BLUE,26)),run_time=.35)
        self.at('in awake mice')
        self.play(FadeIn(label('awake mice',4.9,2.7,TEXT,26)),run_time=.25)
        self.finish()

class S03Chr2(SpokenScene):
    def construct(self):
        c=sheet(-1,-.35,w=8.8,h=5.6,indices=(),title='imposed ensemble — piriform cortex')
        self.add(c,label('Imposed ensemble — not a natural odour ensemble',-1,-2.8,BLUE,24),label('Blue = active (firing)',0,-3.55,BLUE,26))
        self.at('is a light')
        self.play(FadeIn(label('Channelrhodopsin: light-gated channel',0,3.35,BLUE,28)),run_time=.35)
        self.at('Light drives those')
        b=beam(-1,-.6,bright=True)
        self.play(FadeIn(b),*activity(c),*[Flash(c[1][i],color=BLUE,flash_radius=.4) for i in ACTIVE],run_time=.6)
        self.at('whatever the nose')
        # A side profile: forehead, curved bridge, projecting tip, nostril and upper lip.
        profile=VMobject(color=TEXT,stroke_width=4).start_new_path([4.8,1.5,0])
        profile.add_cubic_bezier_curve_to([5.15,1.25,0],[4.95,.9,0],[5.08,.65,0])
        profile.add_cubic_bezier_curve_to([5.25,.25,0],[5.85,.0,0],[5.8,-.2,0])
        profile.add_cubic_bezier_curve_to([5.75,-.45,0],[5.22,-.2,0],[5.18,-.5,0])
        profile.add_cubic_bezier_curve_to([5.1,-.7,0],[5.45,-.75,0],[5.35,-.95,0])
        nose=VGroup(profile,ArcBetweenPoints([5.38,-.2,0],[5.65,-.22,0],angle=-1.8,color=TEXT),
                    Line([4.65,.85,0],[4.95,.85,0],color=TEXT),label('nose',5.2,-1.45,TEXT,26),label('idle',5.2,-2,TEXT,26))
        self.play(FadeIn(nose),run_time=.35)
        self.finish()

class S04Pairing(SpokenScene):
    def construct(self):
        m,b,w,g=pair_stage()
        VGroup(m[0],b[0],w).scale(1.35,about_point=[-3.4,-.5,0])
        VGroup(m[1],b[1],g).scale(1.35,about_point=[3,-.5,0])
        self.add(m,label('light, then outcome',0,3.2,GOLD,32))
        self.at('In one group')
        self.play(FadeIn(b[0]),run_time=.3)
        self.at('paired with a reward')
        self.play(FadeOut(b[0]),FadeIn(w),run_time=.3)
        self.at('In another')
        self.play(FadeIn(b[1]),run_time=.2)
        self.wait(1)
        self.at('with a shock')
        self.play(FadeOut(b[1]),FadeIn(g),Flash(m[1].get_bottom(),color=ORANGE),run_time=.35)
        self.finish()

class S05Predict1(SpokenScene):
    def construct(self):
        self.add(prediction_stage())
        self.at('Pause and predict')
        q=q1()
        self.at('What will each group learn')
        self.play(FadeIn(q[0]),run_time=.35)
        self.at('Would that show')
        self.play(FadeIn(q[1]),run_time=.35)
        self.finish()

class S06Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(prediction_stage(),q1())
        self.wait(5)

class S07Learned(SpokenScene):
    def construct(self):
        m,b,w,g=pair_stage()
        self.add(m,label('TEST: light alone',0,3.2,GOLD,34))
        self.at('Paired with water')
        self.play(FadeIn(b[0]),run_time=.3)
        self.at('trigger licking')
        tongue=Line([-1.56,-.36,0],[-1.1,-.45,0],color=GREEN,stroke_width=7)
        self.play(Create(tongue),FadeIn(label('licking',-3.4,-2.6,GREEN,32)),run_time=.25)
        self.play(tongue.animate.scale(.35,about_point=tongue.get_start()),run_time=.18)
        self.play(tongue.animate.scale(2.85,about_point=tongue.get_start()),run_time=.18)
        self.at('Paired with shock')
        self.play(FadeIn(b[1]),run_time=.25)
        self.at('trigger flight')
        # Run left, away from the stimulation location, with alternating legs.
        self.play(m[1].animate.shift(LEFT*1.7),FadeIn(label('flight',3,-2.6,ORANGE,32)),GrowArrow(Arrow([3,-2,0],[.8,-2,0],color=ORANGE)),run_time=.55)
        self.play(m[1][6].animate.rotate(.4),run_time=.15)
        self.finish()

class S08Small(SpokenScene):
    def construct(self):
        a=sheet(-3.3,.3,5.5,4.2,indices=(0,5),title='imposed: 2 cells')
        b=sheet(3.3,.3,5.5,4.2,indices=(0,2,3,5,6),title='imposed: 5 cells')
        thin=Arrow([-4.7,-2.4,0],[-2,-2.4,0],color=GREEN,stroke_width=2)
        thick=Arrow([1.9,-2.4,0],[4.6,-2.4,0],color=GREEN,stroke_width=12,max_stroke_width_to_length_ratio=10)
        self.add(a,b,thin,thick)
        self.at('Small ensembles were enough')
        self.play(Indicate(a[1],color=BLUE),run_time=.3)
        self.at('a weaker response')
        self.play(FadeIn(label('small: weaker',-3.3,-3.2,GREEN,30)),run_time=.3)
        self.at('than larger ones')
        self.play(Indicate(thick,color=GREEN),FadeIn(label('larger: stronger',3.3,-3.2,GREEN,30)),run_time=.35)
        self.finish()

class S09Discriminate(SpokenScene):
    def construct(self):
        a=sheet(-3.3,.3,5.5,4.4,title='imposed ensemble 1')
        b=sheet(3.3,.3,5.5,4.4,indices=(1,2,4,7),title='imposed ensemble 2')
        self.add(a)
        self.at('different activated groups')
        self.play(FadeIn(b),GrowArrow(Arrow([-3.3,-2,0],[-4.5,-2.8,0],color=GREEN)),GrowArrow(Arrow([3.3,-2,0],[4.5,-2.8,0],color=GREEN)),FadeIn(label('mouse treats them differently',0,-3.35,GREEN,30)),run_time=.35)
        self.at('apart')
        self.play(FadeIn(label('discriminate',0,3.35,GREEN,30)),run_time=.25)
        self.finish()

class S10Sufficient(SpokenScene):
    def construct(self):
        c=sheet(-3.5,-.35,4.8,4.8,title='imposed ensemble')
        outcome=chip('outcome',GREEN,28).move_to([3.4,0,0])
        self.add(c)
        self.at('sufficient as a learned cue')
        self.play(FadeIn(label('Sufficient as a learned cue',0,3.1,GREEN,32)),run_time=.45)
        self.at('Paired with an outcome')
        self.play(FadeIn(outcome),run_time=.45)
        self.at('learn an association')
        self.play(GrowArrow(Arrow(c.get_right()+RIGHT*.1,outcome.get_left(),color=GREEN,buff=.2)),
                  FadeIn(label('once paired with an outcome',0,-3,GREY,26)),run_time=.5)
        self.finish()

class S11NotSmell(SpokenScene):
    def construct(self):
        m=mouse(-2.8,-1).scale(1.5)
        bubble=VGroup(Ellipse(width=5.1,height=3.3,color=TEXT).move_to([2.4,.9,0]),label('?',3.8,1,TEAL,48),Dot([-.3,-.8,0],color=GREY,radius=.14))
        waves=VGroup(*[ParametricFunction(lambda t,k=k: np.array([1.2+k*.65+.16*np.sin(t*5),.1+t,0]),t_range=[0,1.4],color=TEAL) for k in range(3)])
        self.add(m,bubble,waves)
        self.at('does not show')
        self.play(FadeIn(label('Smell not established',0,3.15,TEXT,36)),run_time=.35)
        self.at('The authors withheld')
        self.play(FadeIn(label('claim withheld by the authors',0,-3.1,GOLD,30)),run_time=.35)
        self.finish()

class S12NotWhere(SpokenScene):
    def construct(self):
        a=RoundedRectangle(width=3.8,height=4.8,color=TEAL).move_to([-3.5,0,0])
        self.add(a,label('piriform',-3.5,1.4,TEAL,34),label('own synapses?',-3.5,-1.3,TEXT,26))
        self.at('where the association is stored')
        self.play(FadeIn(label('Where is the association stored?',0,3.2,size=34)),run_time=.3)
        self.at('in piriform')
        self.play(FadeIn(label('?',-3.5,0,GOLD,64)),run_time=.3)
        self.at('in the areas')
        downstream=VGroup()
        for y,name in [(1.5,'amygdala'),(-1.5,'other areas')]:
            box=chip(name,GREY,30).move_to([3.4,y,0])
            downstream.add(box,Arrow([-1.6,y*.5,0],box.get_left(),color=TEAL,buff=.15),label('?',.7,y*.75+.45,GOLD,38))
        self.play(FadeIn(downstream),run_time=.4)
        self.finish()

class S13DriftQ(SpokenScene):
    def construct(self):
        c=sheet(0,-.25,8.5,4.3,color=TEAL,title='odour A in piriform')
        self.add(c,label('Teal ovals = natural odour-evoked activity',0,-2.85,TEAL,26))
        self.at('Now the last puzzle')
        self.play(FadeIn(label('day 1   · · ·   day 32',0,3.2,TEXT,32)),run_time=.35)
        self.at('pattern stay put')
        self.play(FadeIn(label('Does the pattern stay put?',0,-3.5,size=32)),run_time=.35)
        self.finish()

class S14Schoonover(SpokenScene):
    def construct(self):
        self.add(label('Schoonover and colleagues, 2021',0,3.2,TEXT,28))
        self.at('recorded single')
        setup=VGroup(label('one piriform neuron, same odour',0,2.3,TEAL,30))
        # A repeated illustrative event train only establishes the recording design;
        # no differing daily response is asserted before the prediction.
        for y,day in [(1,'day 1'),(-1.2,'day 32')]:
            setup.add(label(day,-5.2,y,TEXT,28),Line([-3.9,y,0],[5.4,y,0],color=GREY))
            for t in (.12,.36,.43,.72):
                x=-3.9+9.3*t
                setup.add(Line([x,y-.1,0],[x,y+.65,0],color=TEAL,stroke_width=4))
        setup.add(Arrow([-3.9,-2,0],[5.4,-2,0],color=GREY),label('time in trial →',.7,-2.45,TEXT,28),
                  label('rows = same neuron, recorded on different days',0,-3,TEXT,26),
                  label('Recording design only — illustrative events',0,-3.55,TEXT,26))
        self.play(Create(setup),run_time=.45)
        self.finish()

class S15Decoder(SpokenScene):
    def construct(self):
        c=sheet(-4.1,-.3,3.5,4.7,color=TEAL,title='odour A activity')
        box=chip('decoder',TEXT,34).move_to([.2,-.3,0])
        out=chip('odour A',TEAL,30).move_to([4.7,-.3,0])
        self.add(c)
        self.at('They used a decoder')
        self.play(FadeIn(box),GrowArrow(Arrow(c[0].get_right(),box.get_left(),buff=.2,color=TEAL)),run_time=.35)
        self.at('a program trained')
        a=chip('A',TEAL,28).move_to([-.8,2.1,0])
        b=chip('B',TEAL,28).move_to([1.2,2.1,0])
        examples=VGroup(label('train on known odours',1.6,3.15,TEXT,28),a,b,
                        Arrow(a.get_bottom(),box.get_top()+LEFT*.4,buff=.15,color=TEAL),
                        Arrow(b.get_bottom(),box.get_top()+RIGHT*.4,buff=.15,color=TEAL))
        self.play(FadeIn(examples),FadeIn(label('trained program',.2,-1.25,TEXT,26)),run_time=.35)
        self.at('to guess which')
        self.play(GrowArrow(Arrow(box.get_right(),out.get_left(),buff=.2,color=TEAL)),FadeIn(out),run_time=.35)
        self.at('from the recorded activity')
        self.play(Indicate(c[1],color=TEAL),run_time=.4)
        self.finish()

class S16Chance(SpokenScene):
    def construct(self):
        g=graph(); self.add(g[0],g[1],g[3])
        self.at('compared with chance')
        self.play(Create(g[2]),run_time=.6)
        self.at('random guessing')
        self.play(FadeIn(label('random guessing',0,.5,TEXT,32)),run_time=.45)
        self.finish()

class S17Predict2(SpokenScene):
    def construct(self):
        q=q2(); self.add(q[0])
        self.at('Pause and predict')
        self.add(label('Pause and predict',1.5,3.1,GOLD,28))
        self.at('Train the decoder')
        self.play(FadeIn(q[1]),run_time=.4)
        self.at('How well will')
        self.play(FadeIn(q[2]),run_time=.4)
        self.finish()

class S18Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(q2(),label('Pause and predict',1.5,3.1,GOLD,28))
        self.wait(5)

class S19Fell(SpokenScene):
    def construct(self):
        self.add(graph(),startpoint())
        self.at('It approached chance')
        self.play(Create(curve()),FadeIn(curve_label(frozen=True)),run_time=.6)
        self.at('responses had drifted')
        self.play(FadeIn(label('Responses drifted',1.2,2.2,TEAL,30)),run_time=.4)
        self.finish()

class S20Exposure(SpokenScene):
    def construct(self):
        self.add(graph(),startpoint(),curve(),curve_label())
        self.at('Daily exposure')
        self.play(FadeIn(curve_label(True)),run_time=.4)
        self.at('slowed the drift')
        self.play(Create(curve(GREEN,True)),run_time=.65)
        self.finish()

class S21NotPercept(SpokenScene):
    def construct(self):
        m=mouse(-3,-.6).scale(1.5)
        self.add(m,label('animal',-3,-2.7,TEXT,30),Line([.3,-3,0],[.3,2.6,0],color=GREY))
        self.at('Drift does not mean')
        self.play(FadeIn(label('Changed smell?',-3,2.65,TEXT,34)),FadeIn(label('not established',-3,1.8,GOLD,28)),run_time=.35)
        self.at('A decoder is a tool')
        self.add(label("outside the animal:\nexperimenter's tool",3.5,-1.8,TEXT,28))
        d=chip('decoder',TEXT,38).move_to([3.5,.2,0])
        self.play(FadeIn(d),run_time=.35)
        self.at('the experimenter holds')
        self.play(Indicate(d,color=TEXT),run_time=.35)
        self.finish()

class S22Downstream(SpokenScene):
    def construct(self):
        c=sheet(-3.7,-.3,4.5,4.8,color=TEAL,title='odour A — day 1')
        reader=chip('downstream\nreader',TEAL,28).move_to([.7,.4,0])
        out=chip('same\noutput',GREEN,28).move_to([4.6,.4,0])
        self.add(c,reader,label('Hypothesis',0,3.2,GOLD,34),Arrow(c[0].get_right(),reader.get_left(),color=TEAL,buff=.15))
        self.at('A downstream circuit')
        self.play(FadeIn(out),GrowArrow(Arrow(reader.get_right(),out.get_left(),color=GREEN,buff=.15)),run_time=.3)
        self.at('may read a moving population')
        self.play(*activity(c,LATER,TEAL),Transform(c[2],label('odour A — day 32',-3.7,2.46,TEXT,26)),run_time=.55)
        self.at('consistently')
        self.play(Indicate(out,color=GREEN,scale_factor=1.05),FadeIn(label('changing cells → consistent readout?',1,-3.3,TEXT,28)),run_time=.35)
        self.finish()

class S23Retrain(SpokenScene):
    def construct(self):
        # Reserve a separate right-hand panel so links cannot be read as plot data.
        plot=VGroup(graph(),startpoint(),curve(),curve_label(frozen=True))
        plot.scale(.85).shift(LEFT*1.8+DOWN*.1)
        self.add(plot)
        self.at('If decoders retrained each day')
        dots=VGroup(*[Dot([day_x(d),1.65,0],radius=.08,color=GREEN) for d in range(1,33)])
        dots.scale(.85,about_point=ORIGIN).shift(LEFT*1.8+DOWN*.1)
        self.play(FadeIn(dots),FadeIn(label('IF — hypothetical: daily decoders',0,3.3,GREEN,28)),run_time=.4)
        self.at('the information is there')
        cell=VGroup(Dot([3.9,.5,0],radius=.16,color=TEAL),label('cell 1',3.95,1.05,TEAL,22))
        a=chip('A',TEAL,24).move_to([5.95,.5,0])
        b=chip('B',TEAL,24).move_to([5.95,-1,0])
        link=Arrow([4.2,.5,0],[5.5,.5,0],color=GOLD,buff=.05)
        cue=VGroup(RoundedRectangle(width=3.4,height=4.5,corner_radius=.2,color=GREY).move_to([4.9,0,0]),
                   label('cell to odour link',4.9,1.85,TEXT,22),cell,a,b,link,
                   label('odours',5.95,-1.65,TEXT,22))
        self.play(FadeIn(cue),FadeIn(label('high each day',-.8,2.15,GREEN,26)),run_time=.3)
        self.at('the mapping changed')
        self.play(Transform(link,Arrow([4.2,.5,0],[5.5,-1,0],color=GOLD,buff=.05)),
                  FadeIn(label('mapping changed',4.9,-2,GOLD,22)),run_time=.65)
        self.at('That reading needs checks')
        self.play(FadeIn(label('Check: same cells\ntracked',4.9,-2.95,GOLD,22)),run_time=.35)
        self.finish()

class S24NotFixed(SpokenScene):
    def construct(self):
        a=sheet(-3.3,-.1,5.5,4.6,indices=ACTIVE,color=TEAL,title='odour A — day 1')
        b=sheet(3.3,-.1,5.5,4.6,indices=LATER,color=TEAL,title='odour A — day 32')
        self.add(a,label('same odour, day 1 vs day 32',0,3.3,TEXT,30))
        self.at('does not always light')
        rings=VGroup(*[Circle(radius=.26,color=GOLD,stroke_width=3).move_to(b[1][i]) for i in set(ACTIVE)^set(LATER)])
        self.play(FadeIn(b),Create(rings),run_time=.4)
        self.add(label('rings: cells whose activity changed',0,-2.9,GOLD,26))
        self.at('in these recordings')
        self.play(FadeIn(label('in these recordings',0,-3.5,TEXT,28)),run_time=.3)
        self.finish()

class S25Open(SpokenScene):
    def construct(self):
        c=sheet(0,-1,8,3.4,color=TEAL,title='odour A — moving code')
        self.add(c)
        self.at('What stays stable')
        self.play(FadeIn(label('What stays stable?',0,2.5,size=40)),run_time=.4)
        self.at('a moving code')
        self.play(*activity(c,LATER,TEAL),run_time=.55)
        self.at('an open question')
        self.play(FadeIn(label('Open question',0,-3.25,GOLD,28)),run_time=.4)
        self.finish()

class S26Takeaway(SpokenScene):
    def construct(self):
        a=sheet(-3.3,-.1,5.5,4.8,indices=ACTIVE,title='imposed ensemble')
        b=sheet(3.3,-.1,5.5,4.8,indices=ACTIVE,color=TEAL,title='odour A')
        self.add(a,b)
        self.at('can be taught meaning')
        self.play(FadeIn(label('Taught meaning',0,3.3,GREEN,34)),run_time=.3)
        self.at('itself moves over weeks')
        self.add(label('Moving pattern — over weeks',0,-3.2,TEAL,32))
        self.play(*activity(b,LATER,TEAL),run_time=.45)
        self.finish()

class S27End(EndCard):
    LINE="A scattered pattern can be taught meaning, and an odour's own pattern drifts over weeks."
    def construct(self):
        self.add(label('A scattered pattern can be taught meaning,',0,1.2,TEXT,34),label("and an odour's own pattern",0,.1,TEXT,34),label('drifts over weeks.',0,-1,TEXT,34),label('biochemistrypedia.com',0,-2.8,TEAL,26))
        self.finish()
