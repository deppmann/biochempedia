"""Take the Input Away — revised timed chapter.
COLOR MAP: YELLOW stimulus; GREEN CT/thin C fibres; PURPLE pleasantness;
BLUE imaging; RED cut/unsupported inference; GREY anatomy/large fibres.
Bars are ordinal schematics, never invented numerical observations.
The sole trace is the constant model f(stroking)=0 (no modulation),
qualitative and explicitly labelled, not an fMRI time series.
"""
from bp_style import *
import numpy as np
PURPLE = '#B58CD9'
GREY = '#BDC3CE'

def label(s,x,y,size=30,color=TEXT):
    return T(s,size,color).move_to([x,y,0])
def heading(s): return label(s,0,3.18,34)
def lead(a,b,color=GREY): return Line([*a,0],[*b,0],color=color,stroke_width=2)
def cross(x,y,r=.25):
    return VGroup(Line([x-r,y-r,0],[x+r,y+r,0],color=RED,stroke_width=5),Line([x-r,y+r,0],[x+r,y-r,0],color=RED,stroke_width=5))
def brush(x,y):
    return VGroup(Line([x,y+.9,0],[x,y+.2,0],color=YELLOW,stroke_width=9),Rectangle(width=1,height=.25,color=YELLOW,fill_opacity=1).move_to([x,y+.15,0]),*[Line([x-.4+i*.13,y,0],[x-.4+i*.13,y-.25,0],color=YELLOW,stroke_width=3) for i in range(7)])
def touch():
    sk=VGroup(RoundedRectangle(width=11.5,height=.8,corner_radius=.15,color=GREY,fill_opacity=.15).move_to([0,.1,0]),*[Line([x,.5,0],[x+.15,1.15,0],color=GREY,stroke_width=3) for x in np.linspace(-5.2,5.2,14)])
    ct=VGroup(Ellipse(width=1.1,height=.6,color=GREEN,fill_opacity=.25).move_to([-1,-.65,0]),VMobject(color=GREEN,stroke_width=6).set_points_as_corners([[-1,-.95,0],[-1,-2,0],[4.5,-2,0]]))
    return sk,ct,brush(-4,1.5),VGroup(label('CT afferent',2,-1.25,32,GREEN),lead((2,-1.55),(2,-2),GREEN))
def patient(x=0,kind='intact'):
    body=VGroup(Circle(radius=.42,color=GREY,fill_opacity=.15).move_to([x,1.75,0]),RoundedRectangle(width=1.7,height=3.4,corner_radius=.6,color=GREY,fill_opacity=.07).move_to([x,-.65,0]))
    large=VGroup(Line([x-.4,.6,0],[x-.4,-1.9,0],color=GREY,stroke_width=7),*[RoundedRectangle(width=.45,height=.45,corner_radius=.08,color=GREY,fill_opacity=.6).move_to([x-.4,.25-i*.75,0]) for i in range(3)])
    thin=Line([x+.4,.6,0],[x+.4,-1.9,0],color=GREEN,stroke_width=5)
    tract=Rectangle(width=.65,height=.45,color=GREY,fill_opacity=.12).move_to([x,-1.1,0])
    tract.set_opacity(0)
    if kind=='large': large.set_opacity(.05); body.add(DashedLine([x-.4,.6,0],[x-.4,-1.9,0],color=GREY),cross(x-.4,-.6))
    if kind=='thin':
        thin.set_opacity(.35)
        body.add(label('Many → few',x,2.5,24,GREEN))
    if kind=='cut':
        # Separate lateral cord mark: never cross the myelinated-fibre boxes.
        body.add(Sector(radius=.55,start_angle=-PI/2,angle=PI/2,color=RED,fill_opacity=.65).shift([x+.2,-.85,0]))
    return VGroup(body,large,thin,tract)
def fibre_rows(reduced=False):
    rows=VGroup()
    for y,s,col,n in [(1.95,'Large myelinated',GREY,2),(-.25,'Thin / C fibres',GREEN,4)]:
        lines=VGroup(*[Line([.5,y-.6-j*.43,0],[5.6,y-.6-j*.43,0],color=col,stroke_width=6) for j in range(n)])
        if reduced and col==GREEN:
            for l in lines[1:]: l.set_opacity(.05)
        rows.add(VGroup(label(s,3,y,30,col),lines))
    return rows

def ratings(question=True):
    title=heading('Predict: slow stroking' if question else 'Slow stroking: less pleasant')
    axis=VGroup(Arrow([-4.7,-2.35,0],[-4.7,2.25,0],buff=0,color=GREY),label('High',-5.65,2.05,28),label('Low',-5.65,-2.3,28),label('Pleasantness',-4.6,2.65,30,PURPLE))
    shells=VGroup(*[Rectangle(width=1.8,height=4.6,color=PURPLE).move_to([x,-.05,0]) for x in (-1.8,2.6)])
    names=VGroup(label('Carriers',-1.8,-2.75,30),label('Matched controls',2.6,-2.75,30))
    fills=VGroup(*[Rectangle(width=1.65,height=h,color=PURPLE,stroke_width=0,fill_opacity=.8).move_to([x,-2.32+h/2,0]) for x,h in [(-1.8,2.3),(2.6,4.35)]])
    foot=label('Schematic, not numerical ratings',0,-3.35,28,GREY)
    prompt=label('Which bar is taller, and by how much?',.5,2.55,28,YELLOW)
    return VGroup(title,axis,shells,names,foot,prompt),fills

def brain():
    # Lateral cutaway: posterior at left; insula deep behind the lateral fissure.
    outline=VMobject(color=GREY,fill_color=GREY,fill_opacity=.12).set_points_smoothly([[-4,-1.7,0],[-5,-.7,0],[-4.9,1,0],[-3.8,2,0],[-2,2.35,0],[-.2,2,0],[1.1,1,0],[1.4,-.1,0],[.6,-.6,0],[-.1,-1.6,0],[-1.8,-2,0],[-4,-1.7,0]])
    fissure=VMobject(color=GREY,stroke_width=5).set_points_smoothly([[-3.6,-.1,0],[-2.2,.2,0],[-.8,-.25,0],[.8,-.4,0]])
    ins=Ellipse(width=1.35,height=.8,color=BLUE,fill_color=BG,fill_opacity=1).move_to([-2.7,-.35,0])
    s1=VMobject(color=GREY,stroke_width=18,stroke_opacity=.4).set_points_smoothly([[-2.8,2.15,0],[-2.95,1.3,0],[-2.7,.6,0]])
    s2=Line([-1.6,-.6,0],[-.5,-.7,0],color=GREY,stroke_width=16,stroke_opacity=.4)
    labels=VGroup(label('S1',-3.9,2.3,30),lead((-3.6,2.2),(-2.8,1.9)),label('S2',1.9,-1.2,30),lead((1.5,-1.1),(-.6,-.7)),label('Posterior insula',-3.2,-2.6,30,BLUE),lead((-3.1,-2.2),(-2.7,-.8),BLUE))
    return VGroup(outline,fissure,ins,s1,s2,labels)

def caveat(dim=True):
    rows=VGroup()
    for y,s,col in [(1.6,'CT afferents',GREEN),(0,'Other thin C fibres',GREEN),(-1.6,'Other affected fibres',GREY)]:
        ls=VGroup(*[Line([-5.6,y-.5-j*.25,0],[-.8,y-.5-j*.25,0],color=col,stroke_width=5) for j in range(3)])
        if dim:
            for l in ls: l.set_stroke(opacity=.3)
        rows.add(VGroup(label(s,-3.2,y,30,col),ls))
    return VGroup(heading('Mutation affects more than CT afferents'),rows,label('Not a clean',3.2,.5,36,RED),label('removal',3.2,-.3,36,RED))

def cord():
    x=-3.7
    outer=Ellipse(width=4.4,height=5.2,color=GREY,fill_opacity=.12).move_to([x,0,0])
    mid=DashedLine([x,-2.45,0],[x,2.45,0],color=GREY,stroke_opacity=.5)
    wedge=Sector(radius=2.1,start_angle=-PI/2,angle=PI/2,color=RED,fill_opacity=.35).shift([x,0,0])
    cut=cross(x+1.2,-1.2,.45)
    dorsal=RoundedRectangle(width=1,height=1,corner_radius=.15,color=GREY,fill_opacity=.15).move_to([x,1.65,0])
    labs=VGroup(label('Dorsal columns',-3.8,2.9,28,GREY),lead((-3.8,2.65),(-3.7,2.15)),label('Anterolateral tract',-3.5,-3.0,28,GREY),lead((-2.6,-2.75),(-2.3,-1.8)),label('Spinal cord · schematic',-3.5,-3.45,28,GREY))
    return VGroup(outer,mid,wedge,cut,dorsal,labs)
def linked_senses(itch=False):
    senses=VGroup()
    for y,s in [(1.5,'Pain'),(.5,'Temperature')]+([(-.5,'Itch')] if itch else []):
        senses.add(VGroup(label(s,2.6,y,32,RED),lead((-2.45,-1),(0,y),RED)))
    return senses

def route_question():
    return VGroup(cord(),heading('Predict: cut one route'),linked_senses(),label('If this were the only route…',2.8,-1.3,28),label('Pleasantness',2.8,-2.15,34,PURPLE),label('ratings vanish?',2.8,-2.8,34,PURPLE))

def result(uncertain=False):
    axis=VGroup(Arrow([-5.1,-2.15,0],[-5.1,2.1,0],buff=0,color=GREY),label('High',-5.9,2,28),label('Low',-5.9,-2.1,28),label('Rated pleasantness',-3,2.55,28,PURPLE))
    bars=VGroup(); labs=VGroup()
    for x,s,v,h in [(-2.8,'Slow','0.3 cm/s',2.8),(.5,'Caress','3 cm/s',4.5),(3.8,'Fast','30 cm/s',2.7)]:
        bars.add(VGroup(*[Rectangle(width=.72,height=h,color=PURPLE,fill_color=PURPLE,fill_opacity=op).move_to([x+dx,-2.15+h/2,0]) for dx,op in [(-.45,.3),(.45,.95)]]))
        labs.add(label(s,x,-2.6,30,YELLOW),label(v,x,-3.1,28,YELLOW))
    key=VGroup(Rectangle(width=.3,height=.3,color=PURPLE,fill_opacity=.3).move_to([1,2.7,0]),label('Before',2,2.7,28),Rectangle(width=.3,height=.3,color=PURPLE,fill_opacity=.95).move_to([3.3,2.7,0]),label('After',4.2,2.7,28))
    note=label('Not significant ≠ unchanged' if uncertain else 'No significant change',0,3.2,34,RED if uncertain else PURPLE)
    return VGroup(note,axis,bars,labs,key,label('Schematic, not numerical ratings',0,-3.55,28,GREY))

def comparison(left_input=True,left_result=True,right=False,right_result=False):
    left=VGroup(label('INPUT REDUCED',-3.4,2.25,34,GREEN),label('Fewer thin fibres',-3.4,1.4,30),label('(CT and others)',-3.4,.85,28,GREY))
    fibres=VGroup()
    for i in range(5):
        fibres.add(Line([-5.8,.25-i*.24,0],[-4,.25-i*.24,0],color=GREEN,stroke_width=5))
    fibres.add(Arrow([-3.8,-.2,0],[-2.8,-.2,0],buff=.05,color=GREEN),Line([-2.6,-.2,0],[-1,-.2,0],color=GREEN,stroke_width=5))
    left.add(fibres)
    # Ordinal comparison: no invented numerical scale.
    outcome=VGroup(Line([-5.6,-2.15,0],[-1.2,-2.15,0],color=GREY),
        Rectangle(width=.7,height=1,color=PURPLE,fill_opacity=.85).move_to([-4.6,-1.65,0]),
        Rectangle(width=.7,height=1.7,color=PURPLE,fill_opacity=.35).move_to([-2.2,-1.3,0]),
        label('Carriers',-4.6,-2.45,24),label('Controls',-2.2,-2.45,24),label('Less pleasant',-3.4,-3.05,30,PURPLE))
    left.add(outcome)
    if not left_input:
        for m in left[1:4]: m.set_opacity(0)
    if not left_result: outcome.set_opacity(0)
    rightg=VGroup(label('ROUTE CUT',3.4,2.25,34,RED),label('Anterolateral tract cut',3.4,1.4,28),Ellipse(width=2,height=1.6,color=GREY,fill_opacity=.1).move_to([1.9,-.15,0]),Sector(radius=.75,start_angle=-PI/2,angle=PI/2,color=RED,fill_opacity=.4).shift([1.9,-.15,0]),cross(2.3,-.5,.22))
    outcome_r=VGroup(Line([3.5,-1.1,0],[5.7,-1.1,0],color=GREY),
        Rectangle(width=.65,height=1.3,color=PURPLE,fill_opacity=.3).move_to([4,-.45,0]),Rectangle(width=.65,height=1.3,color=PURPLE,fill_opacity=.95).move_to([5.2,-.45,0]),
        label('Before',4,-1.45,22),label('After',5.2,-1.45,22),label('Pleasantness survives',3.4,-2.2,30,PURPLE))
    source=label('Signal source unresolved',3.4,-3.05,28,GREY)
    rightg.add(outcome_r,source)
    if not right: rightg[:5].set_opacity(.35)
    if not right_result: outcome_r.set_opacity(0); source.set_opacity(0)
    return VGroup(heading('Input versus route'),left,Line([0,-3.4,0],[0,2.6,0],color=GREY),rightg)

class S00Title(TitleCard):
    TITLE='Take the Input Away'
    LESSON='Hairy Skin, Stroking and Affective Touch'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.2,28,TEAL),label(self.LESSON,0,1.25,30,GREY),label(self.TITLE,0,0,48),Line([-1.5,-.8,0],[1.5,-.8,0],color=GOLD,stroke_width=4))
        self.finish()
class S01Q(SpokenScene):
    def construct(self):
        sk,ct,b,lab=touch(); self.add(heading('What happens to pleasantness?'),sk,ct,b,lab)
        self.at('makes a stroke'); self.play(b.animate.shift(RIGHT*7),run_time=1.4,rate_func=linear)
        self.at('what happens'); self.play(ct.animate.set_stroke(opacity=.05).set_fill(opacity=0),run_time=.6)
        self.finish()
class S02People(SpokenScene):
    def construct(self):
        self.add(heading('Different losses, different tests'))
        ps=VGroup(*[patient(x) for x in (-4.3,0,4.3)])
        losses=VGroup(*[patient(x,k) for x,k in [(-4.3,'large'),(0,'thin'),(4.3,'cut')]])
        labs=VGroup(label('Large myelinated',-4.3,-2.8,28),label('fibres lost',-4.3,-3.35,28),label('Fewer thin fibres',0,-2.8,28),label('Tract cut',4.3,-2.8,28))
        self.add(ps)
        self.at('some people have lost',lead=0); self.play(Transform(ps,losses),FadeIn(labs),run_time=.5)
        self.finish()
class S03Olausson(SpokenScene):
    def construct(self):
        self.add(patient(-3,'large'),heading('The reverse case'),label('One patient',2.8,1.8,34))
        labs=VGroup(label('Large myelinated: absent',2.3,.6,30),lead((-3.4,.2),(-.7,.6)),label('Thin C fibres: intact',2.3,-1,32,GREEN),lead((-2.6,-1.5),(-.6,-1),GREEN))
        self.at('and colleagues'); self.play(FadeIn(label('Olausson and colleagues, 2002',0,-3.2,30,GREY)),run_time=.4)
        self.at('lacking large',lead=0); self.play(FadeIn(labs),run_time=.3)
        self.finish()
class S04Faint(SpokenScene):
    def construct(self):
        sk,ct,b,lab=touch(); self.add(sk,ct,b,lab,heading('Patient: no large fibres'))
        self.at('Stroking that excites'); self.play(b.animate.shift(RIGHT*7),run_time=1.8,rate_func=linear)
        self.at('produced a faint')
        self.play(FadeIn(VGroup(Ellipse(width=1.1,height=.45,color=PURPLE,stroke_opacity=.25,fill_color=PURPLE,fill_opacity=.1).move_to([-2.7,-3,0]),label('Pleasant, faint',.5,-3,34,PURPLE))),run_time=.5)
        self.finish()
class S05Insula(SpokenScene):
    def construct(self):
        g=brain(); self.add(g,heading('Brain · lateral cutaway'),label('Functional MRI · one patient',0,-3.4,30,GREY))
        self.at('insular activation'); self.play(g[2].animate.set_fill(BLUE,opacity=.65),run_time=.5)
        self.at('primary or secondary'); self.play(FadeIn(VGroup(label('S1 / S2',4,1.3,32),label('None',4,.5,32,GREY),label('detectable',4,-.05,30,GREY),lead((-2.7,1.2),(2.7,1.3)),lead((-.7,-.65),(2.7,1.3)))),run_time=.4)
        self.finish()
class S06Alone(SpokenScene):
    def construct(self):
        self.add(patient(-3,'large'),heading('What one patient can show'))
        self.at('One patient shows'); self.play(FadeIn(label('CT input',2,1.5,40,GREEN)),run_time=.4)
        self.at('can do without'); self.play(FadeIn(VGroup(label('✓ Can produce a sensation',2,.4,32,PURPLE),label('without large fibres',2,-.3,30,GREY))),run_time=.4)
        self.at('not that it is needed'); self.play(FadeIn(VGroup(label('? Needed?',2,-1.5,34,GREY),label('Not shown by one patient',2,-2.2,28,GREY))),run_time=.4)
        self.finish()
class S07Hsan(SpokenScene):
    def construct(self):
        p=patient(-3.8); fs=fibre_rows(); self.add(p,fs,heading('10 carriers · HSAN type V'))
        self.at('nerve growth factor'); self.play(FadeIn(VGroup(label('Nerve growth factor β mutation',0,-2.75,30),label('Morrison and colleagues, 2011',0,-3.4,30,GREY))),run_time=.4)
        self.at('They have fewer'); self.play(Transform(fs,fibre_rows(True)),p[2].animate.set_opacity(.05),run_time=.7)
        self.finish()
class S08Predict(SpokenScene):
    def construct(self):
        self.add(ratings()[0]); self.at('Predict'); self.finish()
class S09Pause(Scene):
    def construct(self): self.camera.background_color=BG; self.add(ratings()[0]); self.wait(5)
class S10Reveal(SpokenScene):
    def construct(self):
        g,fill=ratings(False); self.add(g)
        self.at('rated it less pleasant'); self.play(*[GrowFromEdge(b,DOWN) for b in fill],FadeOut(g[5]),run_time=.6)
        self.at('their posterior insula')
        b=brain(); b[2].set_stroke(GREY).set_fill(BG,opacity=1)
        self.play(FadeOut(g),FadeOut(fill),FadeIn(b),FadeIn(heading('Carriers: posterior insula')),run_time=.4)
        self.at('not modulated')
        # Qualitative response model: modulation is identically zero.
        trace=VMobject(color=BLUE,stroke_width=5).set_points_as_corners([[x,-.35,0] for x in np.linspace(-3.2,-2.2,40)])
        self.play(Create(trace),FadeIn(VGroup(lead((-2.1,-.35),(2.1,.1),GREY),label('No modulation',3.9,1,30,BLUE),label('by stroking',3.9,-.8,30),label('Qualitative schematic',2.4,-3.4,28,GREY))),run_time=.5)
        self.finish()
class S11Caveat(SpokenScene):
    def construct(self):
        g=caveat(False); self.add(g[0],g[1]); self.at('affects more than'); self.play(Transform(g[1],caveat()[1]),run_time=.6)
        self.at('not a clean removal'); self.play(FadeIn(g[2:]),run_time=.4); self.finish()
class S12Beat(Scene):
    def construct(self): self.camera.background_color=BG; self.add(caveat()); self.wait(2.5)
class S13Cut(SpokenScene):
    def construct(self):
        c=cord(); c[2].set_opacity(.1); c[3].set_opacity(0)
        self.add(c,heading('Cut a route'),label('Anterolateral',2.7,1.6,36,RED),label('cordotomy',2.7,.9,36,RED))
        self.at('cordotomy cuts'); self.play(c[2].animate.set_opacity(.4),c[3].animate.set_opacity(1),run_time=.5)
        self.at('to relieve'); self.play(FadeIn(VGroup(label('Pain and temperature',2.7,-.3,30),lead((-2.4,-1),(0,-.3),RED),label('Relieve intractable pain',2.7,-1.6,30))),run_time=.4); self.finish()
class S14Marshall(SpokenScene):
    def construct(self):
        self.add(cord(),heading('Marshall and colleagues, 2019'),label('19 adults · refractory cancer pain',2,2.25,28))
        tracks=VGroup()
        for y,s in [(.4,'Slow · 0.3 cm/s'),(-.8,'Caress · 3 cm/s'),(-2,'Fast · 30 cm/s')]:
            tracks.add(VGroup(Line([.2,y-.3,0],[5.8,y-.3,0],color=GREY),label(s,2,y+.15,28,YELLOW)))
        self.add(tracks)
        self.at('before and after'); self.play(FadeIn(label('Before → After',2.8,1.5,34,PURPLE)),run_time=.4)
        self.at('with a brush'); b=brush(4.5,.25).scale(.6,about_point=[4.5,.25,0]); self.play(FadeIn(b),run_time=.4)
        self.at('three speeds',lead=0)
        strokes=VGroup(*[Arrow([.5,y-.3,0],[5.5,y-.3,0],buff=0,color=YELLOW,stroke_width=5) for y in (.4,-.8,-2)])
        self.play(FadeOut(b),*[GrowArrow(stroke) for stroke in strokes],run_time=.6); self.finish()
class S15Predict(SpokenScene):
    def construct(self):
        g=route_question(); self.add(g[0],g[1]); self.at('Pain and temperature'); self.play(FadeIn(g[2]),run_time=.4)
        self.at('If pleasant touch'); self.play(FadeIn(g[3]),run_time=.4)
        self.at('what should the cut do'); self.play(FadeIn(g[4:]),run_time=.4); self.finish()
class S16Pause(Scene):
    def construct(self): self.camera.background_color=BG; self.add(route_question()); self.wait(5)
class S17Reveal(SpokenScene):
    def construct(self):
        c=cord(); senses=linked_senses(True); self.add(c,heading('Effects of the cut'))
        self.at('Pain'); self.play(FadeIn(senses[0]),run_time=.2)
        self.at('temperature'); self.play(FadeIn(senses[1]),run_time=.2)
        self.at('and itch'); self.play(FadeIn(senses[2]),run_time=.2)
        self.at('markedly disrupted'); self.play(senses.animate.set_opacity(.2),run_time=.4)
        self.at('pleasantness ratings'); self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.2)
        r=result(); self.play(FadeIn(r[1:]),run_time=.4)
        self.at('not significantly changed'); self.play(FadeIn(r[0]),run_time=.4); self.finish()
class S18Beat(Scene):
    def construct(self): self.camera.background_color=BG; self.add(result()); self.wait(2.5)
class S19Power(SpokenScene):
    def construct(self):
        r=result(); self.add(r); self.at('that is not proof'); self.play(Transform(r[0],result(True)[0]),run_time=.4)
        self.at('ratings did not vanish'); self.play(r[2].animate.set_stroke(width=4),run_time=.4); self.finish()
class S20Route(SpokenScene):
    def construct(self):
        c=cord(); self.add(c,heading('Proposed route'),label('Outside the cut tract',2.6,1.2,32),label('Hypothesis',2.6,.4,30,GREY))
        self.at('most likely the dorsal columns'); self.play(c[4].animate.set_color(PURPLE).set_fill(PURPLE,opacity=.5),FadeIn(VGroup(label('Dorsal columns',2.7,-.6,34,PURPLE),lead((-3.1,1.4),(.4,-.6),PURPLE))),run_time=.5); self.finish()
class S21Two(SpokenScene):
    def construct(self):
        g=comparison(left_input=False,left_result=False); self.add(g)
        self.at('With fewer thin',lead=0); self.play(Transform(g[1],comparison(left_result=False)[1]),run_time=.4)
        self.at('less pleasant',lead=0); self.play(Transform(g[1],comparison()[1]),run_time=.3); self.finish()
class S22Two2(SpokenScene):
    def construct(self):
        g=comparison(); self.add(g)
        self.at('Cordotomy cut',lead=0); self.play(Transform(g[3],comparison(right=True)[3]),run_time=.4)
        self.at('yet pleasantness survived',lead=0); self.play(Transform(g[3],comparison(right=True,right_result=True)[3][:6]),run_time=.4)
        self.at('Neither test shows',lead=0); self.play(FadeIn(comparison(right=True,right_result=True)[3][6]),run_time=.4); self.finish()
class S24Take(SpokenScene):
    def construct(self):
        self.add(heading('What the two tests tell us'))
        self.at('input seems'); self.play(FadeIn(label('Fewer thin fibres: less pleasant (contributes)',0,1.6,38,GREEN)),run_time=.4)
        self.at('is not needed'); self.play(FadeIn(label('Route cut: pleasantness survives (not needed)',0,-.1,38,PURPLE)),run_time=.4)
        self.at('C -tactile input',lead=0); self.play(FadeIn(label('CT input: still a candidate, route unresolved',0,-1.8,38)),run_time=.4)
        self.finish()
class S25End(EndCard):
    LINE='CT input: necessity and route remain unresolved.'
    def construct(self):
        self.add(label('CT input remains a candidate',0,1,40,GREEN),VGroup(label('Whether CT input is needed,',0,.05,36),label('and by which route, is unresolved',0,-.6,36)),label('biochemistrypedia.com',0,-1.5,28,TEAL)); self.finish()
