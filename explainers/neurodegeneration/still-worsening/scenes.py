"""Chapter 2, reviewer fix round.
COLOR MAP: BLUE drug; YELLOW placebo; GREEN gap/less worsening;
RED worsening/incorrect readings/adverse effects; GREY neutral; TEAL evidence.
Clinical and PET traces interpolate measured endpoints, not intermediate data.
ALS bars and cognition arrows indicate direction only, never invented quantities.
"""
import numpy as np
from bp_style import *

DRUG, PLC = 1.21, 1.66
K, Y0 = 2.4, -2.65

def label(s,x,y,size=28,color=TEXT):
    return T(s,size,color).move_to([x,y,0])

def heading(s): return label(s,0,3.15,34)

def person(color):
    return VGroup(Circle(.19,color=color,fill_opacity=1,fill_color=color).shift(UP*.72),
        RoundedRectangle(width=.58,height=1.05,corner_radius=.18,color=color,fill_color=color,fill_opacity=.4))

def cohort(color,x):
    return VGroup(*[person(color).shift(RIGHT*i*.95) for i in range(3)]).move_to([x,-.25,0])

def trial():
    return VGroup(heading('Clarity AD · 1,795 people'),
        label('Mild cognitive impairment or mild dementia',0,2.3,28),
        label('Amyloid confirmed',0,1.65,28,TEAL),cohort(BLUE,-3).scale(1.65).move_to([-3,-.5,0]),cohort(YELLOW,3).scale(1.65).move_to([3,-.5,0]),
        label('lecanemab',-3,-2.2,32,BLUE),label('placebo',3,-2.2,32,YELLOW))

def timeline():
    return VGroup(Line([-4.65,Y0,0],[3.1,Y0,0],color=GREY),
        label('0',-4.65,-3.05,26),label('18 months',3.1,-3.05,26))

def graph(lines=False,shade=True):
    x=-4.65
    axis=label('Change in CDR-SB (points; up = worse)',-6.05,-.1,26,GREY).rotate(PI/2)
    base=VGroup(timeline(),Line([x,Y0,0],[x,Y0+K*2.05,0],color=GREY),axis)
    for v in [0,.5,1,1.5,2]:
        yy=Y0+K*v
        base.add(Line([x-.12,yy,0],[x,yy,0],color=GREY),label(f'{v:.1f}',x-.48,yy,26,GREY))
    curves=VGroup(*[ParametricFunction(lambda t,v=v: np.array([x+7.75*t/18,Y0+K*v*t/18,0]),t_range=[0,18],color=c,stroke_width=6) for v,c in [(PLC,YELLOW),(DRUG,BLUE)]])
    ends=VGroup(label('placebo +1.66',4.65,Y0+K*PLC+.15,27,YELLOW),label('lecanemab +1.21',4.65,Y0+K*DRUG-.15,27,BLUE))
    gap=Polygon([x,Y0,0],[3.1,Y0+K*PLC,0],[3.1,Y0+K*DRUG,0],stroke_width=0,fill_color=GREEN,fill_opacity=.18)
    foot=label('Schematic lines; measured endpoints at 18 months',0,-3.55,26,GREY)
    if lines:
        if shade: base.add(gap)
        base.add(curves,ends,foot)
    else: base.add(Dot([x,Y0,0],color=BLUE),Dot([x+.2,Y0,0],color=YELLOW))
    return base,curves,ends,gap,foot

def question1(): return VGroup(graph()[0],heading('Did the treated group get better?'))

def still():
    b,c,e,g,f=graph(True,False)
    # Measure worsening from the actual zero baseline, not an endpoint guide.
    rise=Arrow([2.6,Y0+.12,0],[2.6,Y0+K*DRUG-.25,0],buff=0,color=RED,stroke_width=5)
    note=label('Lecanemab: +1.21 above 0\nstill worse than start',-.55,1.9,28,RED)
    return VGroup(b,heading('Slower worsening is still worsening'),rise,note),c

def comparison(split=False):
    # One undivided bar until the narration calls for its split.
    x=-3.9; bottom=-2.65
    whole=Rectangle(width=1.7,height=PLC*K,color=YELLOW,fill_color=YELLOW,fill_opacity=.4).move_to([x,bottom+PLC*K/2,0])
    low=Rectangle(width=1.7,height=DRUG*K,color=BLUE,fill_color=BLUE,fill_opacity=.35).move_to([x,bottom+DRUG*K/2,0])
    top=Rectangle(width=1.7,height=(PLC-DRUG)*K,color=GREEN,fill_color=GREEN,fill_opacity=.5).move_to([x,bottom+(PLC+DRUG)*K/2,0])
    bar=VGroup(low,top) if split else whole
    return VGroup(heading('Two amounts of decline'),bar,label('Placebo decline',x,-3.15,28,YELLOW),label('1.66 points',x,1.8,30,YELLOW)),low,top

def lifted_gap():
    return VGroup(Rectangle(width=1.7,height=(PLC-DRUG)*K,color=GREEN,fill_color=GREEN,fill_opacity=.5).move_to([1,-2.65+(PLC-DRUG)*K/2,0]),label('0.45-point gap',1,-.95,30,GREEN))

def split_notes():
    x=-2.85
    def bracket(y1,y2):
        return VGroup(Line([x,y1,0],[x+.22,y1,0],color=GREY),Line([x+.22,y1,0],[x+.22,y2,0],color=GREY),Line([x,y2,0],[x+.22,y2,0],color=GREY))
    topy=Y0+K*PLC; mid=Y0+K*DRUG
    a=label('0.45 gap',-.95,(topy+mid)/2,30,GREEN).align_to([-2.2,0,0],LEFT)
    b=label('1.21 still worsened\n(lecanemab group)',.45,(Y0+mid)/2,29,BLUE).align_to([-2.2,0,0],LEFT)
    formula=label('0.45 ÷ 1.66 ≈ 0.27',1.3,-2.1,32).align_to([-2.2,0,0],LEFT)
    result=label('About 27% relative slowing',1,-2.9,30,GREEN).align_to([-2.2,0,0],LEFT)
    return VGroup(bracket(mid,topy),bracket(Y0,mid),a,b),VGroup(formula,result)

def pet(small=False):
    x,y,w,k=(-4.85,-1.75,3.5,.17) if small else (-4.65,-2.25,7.5,.235)
    axis=label('Change in amyloid PET (centiloids)',x-1.2,.15,26,GREY).rotate(PI/2)
    base=VGroup(Line([x,y,0],[x+w,y,0],color=GREY),Line([x,y,0],[x,y+20*k+.15,0],color=GREY),axis,
        label('240 weeks',x+w-.7,y-.45,26,GREY))
    for v in [0,10,20]:
        yy=y+k*v; base.add(Line([x-.1,yy,0],[x,yy,0],color=GREY),label(str(v),x-.45,yy,26,GREY))
    curves=VGroup(*[ParametricFunction(lambda t,v=v: np.array([x+w*t/240,y+k*v*t/240,0]),t_range=[0,240],color=c,stroke_width=5) for v,c in [(19.3,YELLOW),(11.6,BLUE)]])
    if small:
        title=label('Amyloid PET',-3.3,2.35,30)
        nums=VGroup(label('placebo +19.3',-3,-2.7,26,YELLOW),label('drug +11.6',-3,-3.2,26,BLUE))
    else:
        title=heading('A4 · amyloid PET')
        nums=VGroup(label('placebo +19.3',4.65,2.3,27,YELLOW),label('drug +11.6',4.55,.45,27,BLUE),
            label('(19.3 − 11.6) / 19.3 = about 40%',0,-3.15,30,GREEN))
    return VGroup(base,title,nums),curves

def thinking_choices():
    return VGroup(label('Thinking',3.25,2.35,32),label('Cognitive composite',3.25,1.6,27,GREY),
        chip('Slower decline',TEXT,size=30).move_to([3.25,.35,0]),chip('No slower decline',TEXT,size=30).move_to([3.25,-1,0]))

def cognition_question():
    b,c=pet(True)
    return VGroup(b,c,thinking_choices(),heading('Did thinking decline more slowly?'))

def als():
    # Labelled abstract strands: schematic pairing, not molecular geometry.
    wave=FunctionGraph(lambda x:.12*np.sin(x*5),x_range=[-4,4],color=GREY,stroke_width=7).shift(UP*1.35)
    target=VGroup(wave,label('SOD1 mRNA',5.3,1.35,26,GREY))
    strand=VGroup(FunctionGraph(lambda x:.12*np.sin(x*5),x_range=[-2.5,2.5],color=BLUE,stroke_width=8),
        *[Rectangle(width=.28,height=.32,color=BLUE,fill_color=BLUE,fill_opacity=1).move_to([x,-.22,0]) for x in np.arange(-2.1,2.2,.6)])
    strand.move_to([-.6,2.15,0])
    tag=VGroup(chip('tofersen',BLUE,size=32).move_to([-4.7,2.3,0]),Line([-3.6,2.3,0],[-3.15,2.15,0],color=BLUE))
    return VGroup(heading('SOD1-mutant ALS'),target,strand,tag)

def marker_panel(x,title,extra=''):
    # Ordinal comparison only: no quantitative tofersen endpoint was supplied.
    base=VGroup(label(title,x,.65,28),Line([x-2,-2.5,0],[x+2,-2.5,0],color=GREY))
    if extra: base.add(label(extra,x,.1,26,GREY))
    bars=VGroup()
    for dx,h,col,name in [(-.8,2.4,YELLOW,'placebo'),(.8,1.2,BLUE,'tofersen')]:
        bars.add(Rectangle(width=.8,height=h,color=col,fill_color=col,fill_opacity=.45).move_to([x+dx,-2.5+h/2,0]),label(name,x+dx,-2.95,26,col))
    return VGroup(base,bars)

def als_bars():
    return VGroup(marker_panel(-3.2,'SOD1 in spinal fluid'),marker_panel(3.1,'Neurofilament light in plasma','released by damaged axons'),label('Schematic: lower than placebo; bar heights are not measured values',0,-3.5,26,GREY))

def mri():
    icon=VGroup(RoundedRectangle(width=4.6,height=5.2,corner_radius=.3,color=GREY),
        Ellipse(width=3.8,height=4.65,color=GREY,fill_color=GREY,fill_opacity=.2),
        Ellipse(width=1.05,height=1.3,color=RED,fill_color=RED,fill_opacity=.65).shift(UR*.65)).move_to([-3.7,-.15,0])
    patch=icon[2].get_right()
    call=VGroup(Arrow([-.5,1.35,0],patch,color=RED,buff=.12),label('Swelling or fluid (ARIA)',2.5,1.6,30,RED),label('Brain MRI',-3.7,-3.05,28))
    nums=VGroup(label('76-week trial · participants with ARIA',2.3,.5,26),label('donanemab 24.0%',2.3,-.55,34,BLUE),label('placebo 2.1%',2.3,-1.5,34,YELLOW),label('Edema or effusion',2.3,-2.5,27,GREY))
    return VGroup(heading('Donanemab · adverse effects'),icon,call,nums)

def evidence_cards():
    cards=VGroup()
    for q,e,y in [('What builds up?','autopsy',1.9),('What can start it?','families',0),('Does changing it help?','randomized trials in people',-1.9)]:
        cards.add(VGroup(RoundedRectangle(width=11.2,height=1.55,corner_radius=.15,color=GREY).move_to([0,y,0]),label(q,0,y+.32,32),label(e,0,y-.35,32)))
    return cards

class S00Title(TitleCard):
    TITLE='Slower Worsening Is Still Worsening'
    LESSON='When Mature Neurons Fail: Neurodegeneration'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.4,28,TEAL),label(self.LESSON,0,1.55,27,GREY))
        title=VGroup(T('Slower Worsening',48),T('Is Still Worsening',48)).arrange(DOWN,buff=.18).move_to([0,-.05,0])
        self.play(FadeIn(title),Create(Line([-2,-1.6,0],[2,-1.6,0],color=GOLD)),run_time=.55)
        self.wait(max(.1,self.narration_s-self.elapsed()))

class S01Question(SpokenScene):
    def construct(self):
        cells=VGroup()
        for x in [-4.65,4.65]:
            soma=Circle(.65,color=GREY,fill_color=GREY,fill_opacity=.3).move_to([x,-.5,0])
            nucleus=Circle(.19,color=GREY).move_to(soma)
            branches=VGroup()
            for dx,dy in [(-1,.9),(-1,-1),(1,.9),(1,-1)]:
                root=np.array([x+dx*.45,-.5+dy*.45,0])
                tip=np.array([x+dx*1.25,-.5+dy*1.5,0])
                branches.add(Line(root,tip,color=GREY,stroke_width=4),
                    Line(tip,tip+np.array([-.35,dy*.3,0]),color=GREY),
                    Line(tip,tip+np.array([.35,dy*.3,0]),color=GREY))
            cells.add(VGroup(branches,soma,nucleus,label('Neuron',x,-2.65,30,GREY)))
        plaque=VGroup(*[Circle(.8,color=GREY,fill_color=GREY,fill_opacity=.65).shift(p+DOWN*.4) for p in [LEFT*.6,RIGHT*.6,UP*.55,DOWN*.55]])
        def antibody(x,y):
            return VGroup(Line([0,.65,0],[0,0,0],color=BLUE,stroke_width=8),Line([0,0,0],[-.48,-.48,0],color=BLUE,stroke_width=8),Line([0,0,0],[.48,-.48,0],color=BLUE,stroke_width=8)).move_to([x,y,0])
        antibodies=VGroup(antibody(-2.1,2.2),antibody(0,2.2),antibody(2.1,2.2))
        plaque_label=label('Amyloid plaque',0,-2.55,30,GREY)
        self.add(cells,plaque,plaque_label)
        self.at('A drug'); self.play(FadeIn(antibodies),run_time=.3)
        self.at('clears amyloid')
        self.play(*[a.animate.move_to([x,y,0]) for a,x,y in zip(antibodies,[-1.05,0,1.05],[.95,1.5,.95])],run_time=.6)
        self.wait(.3)
        bound=VGroup(plaque,antibodies)
        self.play(bound.animate.scale(.25,about_point=[0,-.4,0]),run_time=1.2)
        self.at('Does that help')
        self.play(FadeOut(bound),FadeOut(plaque_label),FadeIn(heading('Does that help the person?')),run_time=.4); self.finish()

class S02Trial(SpokenScene):
    def construct(self):
        panel=trial(); self.add(panel)
        self.at('The antibody'); self.play(Indicate(panel[5],color=BLUE),run_time=.6)
        self.at('In a large trial'); self.play(Indicate(panel[0],color=TEAL),run_time=.6); self.finish()

class S03Duration(SpokenScene):
    def construct(self):
        self.add(trial()); self.at('Both groups'); self.play(Create(timeline()),run_time=.8); self.finish()

class S04Scale(SpokenScene):
    def construct(self):
        ruler=VGroup(Rectangle(width=1.2,height=5.3,color=GREY,fill_opacity=.1,fill_color=GREY).move_to([-2,0,0]))
        for v in range(0,19,3):
            y=-2.65+5.3*v/18
            ruler.add(Line([-2.6,y,0],[-1.65,y,0],color=GREY),label(str(v),-3.1,y,28))
        self.add(heading('Thinking and daily function'),ruler)
        self.at("a clinician's rating"); self.play(FadeIn(label("Clinician's rating",1.7,1.8,32,TEAL)),run_time=.4)
        self.at('higher means worse'); self.play(GrowArrow(Arrow([-.7,-2.65,0],[-.7,2.65,0],color=RED,buff=0)),FadeIn(label('higher = worse',2,.05,34,RED)),run_time=.6)
        self.at('The graph shows'); self.play(FadeOut(Group(*self.mobjects)),FadeIn(graph()[0]),run_time=.6); self.finish()

class S05Question(SpokenScene):
    def construct(self):
        self.add(graph()[0]); self.at('Here is a question'); self.play(FadeIn(question1()[1]),run_time=.4); self.finish()
class S06Pause(Scene):
    def construct(self): self.camera.background_color=BG; self.add(question1()); self.wait(5)
class S07Reveal(SpokenScene):
    def construct(self):
        b,c,e,g,f=graph(); q=question1()[1]; self.add(b,q)
        # Transcript spells the spoken "No" as "Now"; match its first timestamp.
        self.at('Now'); self.play(Create(c),FadeOut(q),run_time=1.3)
        self.at('both groups got worse'); self.play(FadeIn(e),FadeIn(f),run_time=.4)
        self.at('The treated group'); self.play(FadeIn(g),run_time=.5); self.finish()
class S08Share(SpokenScene):
    def construct(self):
        old=graph(True)[0]; self.add(old); whole,_,_=comparison()
        self.at('To compare them'); self.play(FadeOut(old),FadeIn(whole),run_time=.5)
        gap=lifted_gap(); source=gap[0].copy().move_to([-3.9,Y0+K*(PLC+DRUG)/2,0])
        self.at('take the gap'); self.add(source); self.play(Transform(source,gap[0]),run_time=.65)
        self.at('as a share'); self.play(FadeIn(gap[1]),run_time=.3); self.finish()
class S09Quarter(SpokenScene):
    def construct(self):
        whole,_,_=comparison(); gap=lifted_gap(); self.add(whole,gap)
        split,_,_=comparison(True); notes,formula=split_notes()
        self.at('The gap'); self.play(ReplacementTransform(whole,split),FadeOut(gap),FadeIn(notes),run_time=.65)
        self.at('That share'); self.play(FadeIn(formula),run_time=.5); self.finish()
class S10Not(SpokenScene):
    def construct(self):
        cards=VGroup(*[chip(t,GREY,size=36).move_to([0,y,0]) for t,y in [('Gain in memory',2),('Share of patients helped',0),('Prognosis',-2)]])
        self.add(cards)
        self.at('a gain in memory'); self.play(Create(Line(cards[0].get_left()+LEFT*.1,cards[0].get_right()+RIGHT*.1,color=RED,stroke_width=7)),run_time=.35)
        self.at('the share of patients'); self.play(Create(Line(cards[1].get_left()+LEFT*.1,cards[1].get_right()+RIGHT*.1,color=RED,stroke_width=7)),run_time=.35)
        self.at("anyone's prognosis"); self.play(Create(Line(cards[2].get_left()+LEFT*.1,cards[2].get_right()+RIGHT*.1,color=RED,stroke_width=7)),run_time=.35)
        self.wait(2)
        self.play(FadeOut(Group(*self.mobjects)),FadeIn(chip('Compares two amounts of decline',GREEN,size=36).move_to(ORIGIN)),run_time=.45)
        self.wait(1.5); self.finish()
class S11Still(SpokenScene):
    def construct(self):
        panel,c=still(); self.add(panel)
        self.at('Slower worsening'); self.play(GrowArrow(panel[2]),Indicate(panel[3],color=RED),run_time=1.2)
        self.at('It did not stop'); self.play(Indicate(c[1],color=RED,scale_factor=1.08),Indicate(panel[3],color=RED),run_time=1); self.finish()
class S11bBeat(Scene):
    def construct(self): self.camera.background_color=BG; self.add(still()[0]); self.wait(3)
class S12A4(SpokenScene):
    def construct(self):
        people=cohort(GREY,0).scale(2.65).move_to([0,-.25,0])
        self.add(heading('A4 study · solanezumab · 240 weeks'),people)
        self.at('It enrolled older adults'); self.play(FadeIn(label('Ages 65–85',0,2.15,32)),run_time=.4)
        self.at('whose thinking was still normal'); self.play(FadeIn(label('Cognitively unimpaired',0,-2.65,32)),run_time=.4)
        self.at('but whose brains'); self.play(FadeIn(label('Elevated amyloid',0,-3.35,32,TEAL)),run_time=.4)
        self.finish(); self.wait(.5)
class S13Pet(SpokenScene):
    def construct(self):
        b,c=pet(); self.add(b[0],b[1])
        self.at('On PET scans'); self.play(Create(c),run_time=1.2)
        self.at('It rose more slowly'); self.play(FadeIn(b[2]),FadeIn(label('Schematic trajectories; measured 240-week changes',0,2.65,26,GREY)),run_time=.4); self.finish()
class S14Question(SpokenScene):
    def construct(self):
        b,c=pet(True); self.add(b,c)
        self.at('Predict'); self.play(FadeIn(thinking_choices()),FadeIn(cognition_question()[3]),run_time=.45); self.finish()
class S15Pause(Scene):
    def construct(self): self.camera.background_color=BG; self.add(cognition_question()); self.wait(5)
class S16Reveal(SpokenScene):
    def construct(self):
        b,c=pet(True); self.add(b,c,label('Thinking',3.2,2.35,32),label('Cognitive composite',3.2,1.65,28))
        arrows=VGroup(Arrow([2.1,.9,0],[2.1,-.85,0],color=BLUE,buff=0,stroke_width=10),Arrow([4.4,.9,0],[4.4,-1.15,0],color=YELLOW,buff=0,stroke_width=10))
        self.at('Both groups declined'); self.play(Create(Line([1.4,.9,0],[5.2,.9,0],color=GREY)),GrowArrow(arrows[0]),GrowArrow(arrows[1]),run_time=.5)
        self.add(label('drug',2.1,-1.6,27,BLUE),label('placebo',4.4,-1.6,27,YELLOW),label('↓ worse',5.6,.1,26,RED),label('Direction only; not to scale',3.2,-2.15,26,GREY))
        self.at('did not demonstrate'); self.play(Create(VGroup(Line([2.1,-2.4,0],[2.1,-2.55,0],color=TEXT),Line([2.1,-2.55,0],[4.4,-2.55,0],color=TEXT),Line([4.4,-2.55,0],[4.4,-2.4,0],color=TEXT))),FadeIn(label('Difference not\nstatistically significant',3.2,-3.05,27)),run_time=.5); self.finish()
class S17Als(SpokenScene):
    def construct(self):
        a=als(); self.add(a)
        self.at('shows the same'); self.play(a[2].animate.shift(DOWN*.5),a[3][1].animate.put_start_and_end_on([-3.6,2.3,0],[-3.15,1.65,0]),run_time=.8)
        bars=als_bars()
        self.at('lowered S'); self.play(FadeIn(bars[0]),FadeIn(bars[2]),run_time=.35)
        self.at('It also lowered'); self.play(FadeIn(bars[1]),run_time=.5); self.finish()
class S18Als2(SpokenScene):
    def construct(self):
        bars=als_bars().set_opacity(.45); self.add(heading('SOD1-mutant ALS'),bars)
        card=chip('Clinical measures at 28 weeks: no improvement shown',TEXT,size=30).move_to([0,2,0])
        self.at('But over'); self.play(bars.animate.shift(DOWN*.15),FadeIn(card),run_time=.5); self.finish()
class S19Rung(SpokenScene):
    def construct(self):
        cards=evidence_cards(); self.add(cards)
        self.at('That is the treatment question'); self.play(cards[2][0].animate.set_color(TEAL),run_time=.4)
        self.at('A marker can guide'); self.play(cards[2][0].animate.set_color(GREY),cards[1][0].animate.set_color(TEAL).set_fill(TEAL,opacity=.22),run_time=.45)
        self.play(Indicate(cards[1],color=TEAL,scale_factor=1.05),run_time=1.3)
        self.at('a clinical outcome'); self.play(cards[1][0].animate.set_color(GREY).set_fill(BG,opacity=0),cards[2][0].animate.set_color(TEAL).set_fill(TEAL,opacity=.22),run_time=.45)
        self.play(Indicate(cards[2],color=TEAL,scale_factor=1.05),run_time=1.1); self.finish()
class S20Cost(SpokenScene):
    def construct(self):
        p=mri(); self.add(p[0],p[1][0:2],p[2][2])
        self.at('Another antibody'); self.play(Indicate(p[0],color=BLUE),FadeIn(p[3]),run_time=.5)
        self.at('Brain swelling'); self.play(FadeIn(p[1][2]),FadeIn(p[2][0:2]),run_time=.5)
        self.at('far more common'); self.play(Indicate(p[3][1],color=BLUE),Indicate(p[3][2],color=YELLOW),run_time=.7); self.finish()
class S21Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(heading('Different drugs · different trials'),label('Cost: donanemab · ARIA',-3.5,2.3,28),label('Benefit: lecanemab · CDR-SB',3,2.3,28))
        y=-2.15
        for x,v,col,name in [(-4.4,24,BLUE,'donanemab'),(-2.4,2.1,YELLOW,'placebo')]:
            h=v*.13
            self.add(Rectangle(width=1,height=h,color=col,fill_color=col,fill_opacity=.45).move_to([x,y+h/2,0]),label(f'{v:.1f}%',x,y+h+.35,28,col),label(name,x,-2.65,26,col))
        self.add(label('76 weeks · participants with ARIA',-3.5,-3.3,26,GREY))
        x=.6; w=3.05; k=2.1
        self.add(Line([x,y,0],[x+w,y,0],color=GREY),Line([x,y,0],[x,1.65,0],color=GREY),label('points; up = worse',3,1.85,26,GREY))
        for v in [0,.5,1,1.5]:
            yy=y+k*v
            self.add(Line([x-.1,yy,0],[x,yy,0],color=GREY),label(f'{v:.1f}',x-.35,yy,22,GREY))
        for v,col,name in [(PLC,YELLOW,'placebo'),(DRUG,BLUE,'lecanemab')]:
            yy=y+k*v
            txt=label(name,5.25,yy,26,col)
            self.add(ParametricFunction(lambda t,v=v:np.array([x+w*t/18,y+k*v*t/18,0]),t_range=[0,18],color=col,stroke_width=5),
                Line([x+w+.12,yy,0],txt.get_left()+LEFT*.15,color=col,stroke_width=2),txt)
        self.add(label('0.45 points less worsening',3,-2.7,27,GREEN),label('Schematic · 18-month endpoints',3,-3.3,26,GREY)); self.wait(5)
class S22Takeaway(SpokenScene):
    def construct(self):
        self.add(heading('Read two amounts of decline'))
        bars=VGroup()
        for x,v,col,name in [(-4.6,DRUG,BLUE,'lecanemab'),(-2.3,PLC,YELLOW,'placebo')]:
            h=v*2.3
            bars.add(Rectangle(width=1.2,height=h,color=col,fill_color=col,fill_opacity=.4).move_to([x,-2.5+h/2,0]),label(f'+{v:.2f}',x,-2.1+h,28,col),label(name,x,-3.05,27,col))
        self.at('Read a trial'); self.play(FadeIn(bars),run_time=.5)
        x=.4; y=-.6; w=2.2; k=.09
        marker=VGroup(label('Marker',1.6,2,32,TEAL),label('Amyloid on PET',1.6,1.35,26),Line([x,y,0],[x+w,y,0],color=GREY))
        for v,col in [(19.3,YELLOW),(11.6,BLUE)]: marker.add(ParametricFunction(lambda t,v=v:np.array([x+w*t/240,y+k*v*t/240,0]),t_range=[0,240],color=col))
        marker.add(label('Schematic A4 endpoints',1.6,-1.25,26,GREY))
        human=VGroup(label('Person',5,2,32),label('Thinking',5,1.35,28),Arrow([5,.65,0],[5,-.7,0],color=RED),label('Declined',5,-1.25,27,RED))
        self.at('keep a change'); self.play(FadeIn(marker),run_time=.45)
        self.at('apart from'); self.play(FadeIn(human),Create(Line([3.15,-.1,0],[3.55,.3,0],color=TEXT,stroke_width=5)),Create(Line([3.45,-.1,0],[3.85,.3,0],color=TEXT,stroke_width=5)),FadeIn(label('A marker is not the person',3.25,-2.35,30)),run_time=.5); self.finish()
class S23End(EndCard):
    LINE='Slower worsening is still worsening; a marker is not the person.'
    def construct(self):
        self.add(VGroup(T('Slower worsening is still worsening;',40),T('a marker is not the person.',40)).arrange(DOWN,buff=.2).move_to([0,.4,0]),label('biochemistrypedia.com',0,-1.25,30,'#76E3EB'))
        self.wait(self.narration_s)
