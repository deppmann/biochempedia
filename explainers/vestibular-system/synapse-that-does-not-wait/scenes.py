"""Chapter 2. All timing comes from the supplied transcript; script.json is untouched.
COLOR MAP shared with the reference chapter:
BLUE regular afferents/boutons; PURPLE irregular afferents/calyx;
YELLOW central vestibular neuron; GREEN active movement/prediction;
ORANGE passive motion; TEAL neck feedback; RED error; GREY anatomy/axes.
Chapter additions: TEXT potassium/vesicles; GOLD cleft electrical potential.
Nernst: E_K = (RT/F)*1000*ln(Kcleft/140), T=310.15 K.
No invented voltage traces: spike marks are schematic event symbols.
"""
import importlib.util
from pathlib import Path
import numpy as np
from bp_style import *

# Reuse the reference's anatomy and plotting/event helpers verbatim.
_spec = importlib.util.spec_from_file_location('vestibular_reference', Path(__file__).resolve().parent.parent / 'scenes.old.py')
_ref = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ref)
hair_cell, vesicles, arr, spike_train = _ref.hair_cell, _ref.vesicles, _ref.arr, _ref.spike_train
PURPLE = _ref.PURPLE


def label(text, x=0, y=3.05, size=30, color=TEXT):
    return T(text, size, color).move_to([x,y,0])


def cells():
    return (hair_cell(1).scale(1.55).move_to([-3,0,0]),
            hair_cell(2).scale(1.55).move_to([3,0,0]))


def leader(text,xy,end,color=GREY,size=28):
    t=label(text,*xy,size,color)
    start=t.get_left() if end[0]<xy[0] else t.get_right()
    return VGroup(t,Line(start,end,color=color,stroke_width=2))


def question():
    return VGroup(label('Pause and predict',y=3.4,color=GOLD,size=34),
        chip('no otoferlin',GREY,28).move_to([-3.4,2.35,0]),
        label('or',0,2.95,26,GREY),
        chip('no CaV1.3 (calcium channel)',GREY,26).move_to([3.25,2.35,0]),
        hair_cell(1).scale(1.75).move_to([0,-.2,0]),
        label('Can the calyx still fire?',y=-3.6,size=34,color=PURPLE))


def cleft():
    # Enlarged section: 1.4-unit cleft, only a thin slice of each cell.
    left=Rectangle(width=1.1,height=4.8,stroke_width=0,fill_color=GREY,fill_opacity=.15).move_to([-4.25,0,0])
    right=Rectangle(width=1.1,height=4.8,stroke_width=0,fill_color=PURPLE,fill_opacity=.15).move_to([-1.75,0,0])
    mem=VGroup(Line([-3.7,-2.4,0],[-3.7,2.4,0],color=GREY,stroke_width=8),
        Line([-2.3,-2.4,0],[-2.3,2.4,0],color=PURPLE,stroke_width=8))
    labs=VGroup(label('hair cell',-4.3,2.9,28,GREY),label('calyx',-1.65,2.9,28,PURPLE),
        label('cleft · enlarged',-3,-2.95,26,GREY))
    return VGroup(left,right,mem,labs)


def gauge(title,x,value,color=TEXT):
    bottom=-1.95; height=3.9
    box=Rectangle(width=.55,height=height,color=GREY).move_to([x,0,0])
    baseline=bottom+.3 if title=='cleft potential' else bottom+.07
    span=1.88-baseline
    fill=Rectangle(width=.43,height=max(.01,span*value),stroke_width=0,
        fill_color=color,fill_opacity=.8 if value>0 else 0)
    fill.move_to([x,baseline+fill.height/2,0])
    if title=='cleft K+':
        ticks=VGroup(label('20 mM',x,2.45,26),label('7 mM',x,-2.4,26))
    else:
        ticks=VGroup(label('positive',x,2.45,26,GOLD),
            Line([x-.38,baseline,0],[x+.38,baseline,0],color=GOLD,stroke_width=3),
            T('0 mV',22,GOLD).next_to([x+.38,baseline,0],RIGHT,buff=.12))
    return VGroup(box,fill,label(title,x,3.1,26,color),ticks)


def voltage(y=-1.4):
    x=5.55
    rail=Line([x,-1.95,0],[x,1.95,0],color=PURPLE,stroke_width=4)
    ptr=Triangle(color=PURPLE,fill_opacity=1).scale(.16).rotate(-PI/2).move_to([x-.32,y,0])
    return VGroup(rail,ptr,label('calyx V',x,3.1,26,PURPLE),
        label('more +',x,2.45,26,PURPLE),label('more −',x,-2.4,26,PURPLE))


def ek(k):
    return 8.314462618*310.15/96485.33212*1000*np.log(k/140.)


def evidence():
    g=VGroup(label('Keep the evidence apart',y=3.35,size=36))
    for y in [2.8,1.3,-.48,-2.55,-3.7]:
        g.add(Line([-6.1,y,0],[6.1,y,0],color=GREY,stroke_opacity=.4))
    entries=[('Mouse knockouts','calyx spikes survive knockouts',2.12,1.65),
        ('Young rat calyces','receptor potential rises faster with maturation;\nsome non-quantal',.87,.12),
        ('Turtle · dual patch','',-.86,-.86),('Model','cleft potential first',-2.92,-3.36)]
    for i,(name,desc,y,dy) in enumerate(entries):
        col=PURPLE if i<3 else GOLD
        name_label=T(name,28,GREY).move_to([-5.7,y,0],aligned_edge=LEFT)
        row=VGroup(name_label,label('measured' if i<3 else 'predicted',4.95,y,26,col))
        if desc:
            row.add(T(desc,24,col,line_spacing=.7).move_to([-5.7,dy,0],aligned_edge=LEFT))
        g.add(row)
    return g


class S00Title(TitleCard):
    LESSON='Balance: Two Codes for Every Head Movement'
    TITLE='A Synapse That Does Not Wait'

    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON.upper(),26,GREY),
            T(self.TITLE,46,font=TITLE_FONT),Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.35)
        self.play(FadeIn(g),run_time=.5); self.finish()


class S01Q(SpokenScene):
    def construct(self):
        c=hair_cell(1).scale(1.65).move_to([-2.6,0,0])
        prompt=label('Could this synapse\nhelp make them fast?',2.7,-1.5,34)
        self.add(c, prompt.copy().set_opacity(.25))
        self.at('Many irregular fibers')
        self.play(FadeIn(leader('irregular fibre',(-.1,-2.8),[-2.6,-2.5,0],PURPLE)),run_time=.4)
        self.at('type 1 hair cells')
        self.play(FadeIn(leader('type I hair cell',(2.5,1.8),[-1.9,.7,0])),run_time=.4)
        self.at('called a calyx')
        self.play(FadeIn(leader('calyx',(2,.5),[-1.2,-.3,0],PURPLE)),run_time=.4)
        self.at('Could this synapse')
        self.play(FadeIn(prompt),run_time=.4)
        self.finish()


class S02Cells(SpokenScene):
    def construct(self):
        c1,c2=cells(); self.add(c1,c2.copy().set_opacity(.2))
        self.add(label('type I',-3,3.15,34,GREY),label('type II',3,3.15,34,GREY))
        self.at('almost enclosed')
        self.play(FadeIn(leader('calyx',(-.2,-.6),[-1.7,-.5,0],PURPLE)),run_time=.4)
        self.at('A type 2 cell')
        self.play(FadeIn(c2),run_time=.5)
        self.at('with small boutons')
        self.play(FadeIn(leader('boutons',(5,-2.6),[4,-1,0],BLUE)),run_time=.4)
        self.finish()


class S03Central(SpokenScene):
    def construct(self):
        self.add(Ellipse(width=12.8,height=4.9,color=GREY,fill_opacity=.05),
            Ellipse(width=4.5,height=4.7,color=PURPLE,fill_opacity=.08),
            label('central zone',0,1.95,28,PURPLE),VGroup(label('peripheral zone',-4.25,2.65,26,GREY),
                Line([-4.25,2.4,0],[-4.25,1.8,0],color=GREY,stroke_width=2)),
            label('crista · schematic',y=3.45,size=26,color=GREY))
        central=VGroup(*[hair_cell(1).scale(.85).move_to([x,.1,0]) for x in [-1.05,1.05]])
        self.add(central)
        self.at('many irregular fibers')
        fibres=VGroup(*[Line([x,-1.5,0],[x,-2.15,0],color=PURPLE,stroke_width=5) for x in [-1.05,1.05]])
        self.play(Create(fibres),FadeIn(label('calyx-only fibres · irregular',0,-2.65,26,PURPLE)),run_time=.5)
        self.at('cells occur in both zones')
        peripheral=VGroup(hair_cell(1).scale(1.05).move_to([-4.25,-.15,0]),
            hair_cell(1).scale(1).move_to([3.15,-.15,0]),hair_cell(2).scale(1).move_to([5.05,-.15,0]))
        self.play(FadeIn(peripheral),run_time=.5)
        self.at('population pattern')
        self.play(FadeIn(label('Population pattern, not a rule',y=-3.35,size=28)),run_time=.4)
        self.finish()


class S05Shortcut(SpokenScene):
    def construct(self):
        c1,c2=cells(); self.add(c1,c2,label('type I',-3,2.7,28),label('type II',3,2.7,28))
        wrong=chip('type I: no vesicles?',RED,30).move_to([0,3.2,0]); self.add(wrong)
        self.at('Wrong')
        cross=Line(wrong.get_left(),wrong.get_right(),color=RED,stroke_width=4,stroke_opacity=.5)
        self.play(Create(cross),run_time=.3)
        self.at('Both types release')
        v=VGroup(vesicles(-3,-.4).scale(1.6),vesicles(3,-.4).scale(1.6))
        self.play(FadeOut(wrong),FadeOut(cross),FadeIn(v),FadeIn(label('Both release glutamate',y=3.2,size=32)),
            FadeIn(leader('ribbon + vesicles',(0,-1.5),[-2.65,-.5,0])),
            FadeIn(leader('bouton',(5,-2.7),[4,-1,0],BLUE)),run_time=.4)
        self.at('glutamate from vesicles')
        dots=VGroup(*[Dot([x+dx,-.75,0],radius=.09,color=TEXT) for x in [-3,3] for dx in [-.2,0,.2]])
        self.add(dots); self.play(dots.animate.shift(DOWN*.75),run_time=.8)
        self.finish()


class S07Less(SpokenScene):
    def construct(self):
        intro=VGroup(*cells()); self.add(intro,label('Sustained release',y=3.25,size=36))
        self.at('mature mouse tissue')
        self.play(FadeIn(label('Mature mouse utricle',y=-3.15,size=28,color=GREY)),run_time=.3)
        self.at('about 10 times less')
        self.play(FadeOut(intro),run_time=.25)
        self.add(Line([-4.4,-2.1,0],[5.5,-2.1,0],color=GREY),Line([-4.4,-2.1,0],[-4.4,2.2,0],color=GREY),
            label('sustained exocytosis',-1,2.45,28),label('(capacitance rise) · relative',-1,1.85,26,GREY),
            label('type I',-2.4,-2.6,28),label('type II',2.6,-2.6,28),label('schematic\nabout tenfold',4.65,.2,26,GREY))
        bars=VGroup(*[Rectangle(width=1.6,height=h,color=TEXT,fill_opacity=.65).move_to([x,-2.1+h/2,0]) for x,h in [(-2.4,.37),(2.6,3.5)]])
        self.play(*[GrowFromEdge(b,DOWN) for b in bars],run_time=.8); self.finish()


class S08Define(SpokenScene):
    def construct(self):
        c=hair_cell(1).scale(1.6).move_to([-4,0,0])
        box=RoundedRectangle(width=7,height=5.8,corner_radius=.2,color=PURPLE).move_to([2.5,0,0])
        preview=label('A second route',2.5,0,38,PURPLE)
        self.add(c,box,label('Non-quantal transmission',2.5,2.25,34,PURPLE),preview)
        self.at('change in calyx voltage')
        self.play(FadeOut(preview),c[2].animate.set_stroke(color=PURPLE,width=18),FadeIn(label('= a change in\ncalyx voltage',2.5,1,34)),
            GrowArrow(arr([-2.1,-1,0],[-2.1,1.45,0],PURPLE,w=9,tip=.4)),run_time=.5)
        self.at('no vesicle fusion')
        ves=Circle(radius=.34,color=TEXT).move_to([-.15,-.5,0])
        self.play(FadeIn(label('no vesicle fusion',2.7,-.5,34)),Create(ves),Create(Cross(ves,stroke_color=RED)),run_time=.4)
        self.at('no gap junctions')
        gap=VGroup(*[Line([x,-2.1,0],[x,-1.2,0],color=GREY,stroke_width=6) for x in [-.35,.05]])
        self.play(FadeIn(label('no gap junctions',2.7,-1.65,34)),Create(gap),Create(Cross(gap,stroke_color=RED)),run_time=.4)
        self.finish()


def clock(x,y):
    return VGroup(Circle(radius=.53,color=GREY).move_to([x,y,0]),Line([x,y,0],[x,y+.42,0],color=TEXT))


class S09Delay(SpokenScene):
    def construct(self):
        self.add(label('Chemical synapse · each step takes time',y=3.3,size=34))
        self.add(Rectangle(width=3.5,height=4.9,color=GREY,fill_opacity=.1).move_to([-4,0,0]),
            Rectangle(width=3.5,height=4.9,color=PURPLE,fill_opacity=.1).move_to([4,0,0]),
            label('presynaptic terminal',-4,2.75,26,GREY),label('postsynaptic cell',4,2.75,26,PURPLE),label('cleft',0,1.1,28,GREY))
        ves=Circle(radius=.45,color=TEXT).move_to([-3.6,0,0])
        receptor=VGroup(*[Rectangle(width=.22,height=.9,color=PURPLE,fill_opacity=.5).move_to([2.1,y,0]) for y in [-.55,.55]])
        vl=leader('vesicle',(-4,-1.4),[-3.6,-.45,0],TEXT)
        self.add(ves,receptor,vl,leader('receptor',(4,-1.4),[2.2,-.8,0],PURPLE))
        cs=VGroup(*[clock(x,-2.65) for x in [-4,0,4]]); self.add(cs)
        for x,txt in [(-4,'Fuse'),(0,'Cross'),(4,'Open')]: self.add(label(txt,x,-3.35,28))
        self.at('a vesicle must fuse')
        self.play(ves.animate.move_to([-2.3,0,0]),Rotate(cs[0][1],-PI*1.5,about_point=cs[0][0].get_center()),run_time=.75)
        fused=Arc(radius=.45,start_angle=-PI/2,angle=PI,color=TEXT).move_to([-2.2,0,0])
        self.play(ReplacementTransform(ves,fused),Transform(vl,leader('fused vesicle',(-4,-1.4),[-2.25,-.4,0],TEXT)),run_time=.25)
        dots=VGroup(*[Dot([-2.1,dy,0],radius=.11,color=TEXT) for dy in [-.3,0,.3]])
        glutamate=label('glutamate',-1.1,-.65,26)
        self.add(dots,glutamate)
        self.at('glutamate must cross')
        self.play(dots.animate.shift(RIGHT*4),glutamate.animate.shift(RIGHT*2.2),Rotate(cs[1][1],-PI*1.5,about_point=cs[1][0].get_center()),run_time=1.15)
        self.at('receptors must open')
        self.play(receptor[0].animate.shift(DOWN*.5).set_fill(PURPLE,opacity=1).set_stroke(TEXT,width=5),
            receptor[1].animate.shift(UP*.5).set_fill(PURPLE,opacity=1).set_stroke(TEXT,width=5),
            Rotate(cs[2][1],-PI*1.5,about_point=cs[2][0].get_center()),run_time=.7)
        self.at('Each step adds delay')
        self.play(*[FadeIn(label('+ delay',x,-1.85,28,GOLD)) for x in [-4,0,4]],run_time=.4)
        self.finish()


class S10Predict(SpokenScene):
    def construct(self):
        q=question(); self.add(q[0],q[4],q[5])
        self.at('Remove'); self.play(FadeIn(q[1]),run_time=.3)
        self.at('or a calcium channel'); self.play(FadeIn(q[2]),FadeIn(q[3]),run_time=.4)
        self.finish()


class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question()); self.wait(5)


def result():
    return VGroup(hair_cell(1).scale(1.45).move_to([-3.7,-.2,0]),
        spike_train(-.7,5.5,0,[.07,.31,.48,.76,.92],PURPLE,h=1.2),
        label('spike events · schematic',2.4,-.55,26,GREY))


class S12Reveal(SpokenScene):
    def construct(self):
        r=result(); self.add(r[0],label('no otoferlin or no CaV1.3',y=2.4,size=30,color=GREY),
            label('Spaiardi et al., 2022 · mature mouse utricle · in vitro',y=3.2,size=26,color=GREY))
        self.at('Yes'); self.play(Create(r[1]),FadeIn(r[2]),run_time=.6)
        self.play(FadeIn(label('Yes · the calyx still fires',2.4,-1.7,32,PURPLE)),run_time=.3)
        self.finish()


class S13Hedge(SpokenScene):
    def construct(self):
        self.add(result())
        self.at('spikes survive'); self.play(FadeIn(label('Spikes survive',2.4,2,36,PURPLE)),run_time=.3)
        self.at('not whether the signal')
        self.play(FadeIn(label('Normal signal: not tested',2.4,-1.25,28)),run_time=.3); self.finish()


class S14Cleft(SpokenScene):
    def construct(self):
        c=result()[0]; self.add(c)
        self.at('The cleft between')
        section=cleft().shift(RIGHT*3)
        section[3][2].become(label('enlarged section',0,-2.95,26,GREY))
        gap_label=label('cleft',0,-.5,28)
        self.play(FadeOut(c),FadeIn(section),FadeIn(gap_label),run_time=.55)
        self.at('very narrow')
        bracket=VGroup(Line([-.7,1.5,0],[.7,1.5,0],color=TEXT),
            *[Line([x,1.3,0],[x,1.7,0],color=TEXT) for x in [-.7,.7]],
            label('very\nnarrow',0,.7,26))
        self.play(FadeIn(bracket),run_time=.4); self.finish()


class S15Build(SpokenScene):
    def construct(self):
        g=cleft(); fast=gauge('cleft potential',.45,0,GOLD); slow=gauge('cleft K+',3,.0)
        self.add(g,fast,slow)
        self.at('hair cell depolarizes'); self.play(g[0].animate.set_fill(opacity=.35),run_time=.35)
        self.at('more potassium current')
        dots=VGroup(*[Dot([-4.1,1.35-i*.42,0],radius=.11,color=TEXT) for i in range(7)])
        self.add(dots,label('K+',-3,2.25,28))
        self.play(dots.animate.shift(RIGHT*1.1),run_time=1.4)
        self.at('Potassium slowly builds')
        more=VGroup(*[Dot([-3.45+(i%3)*.38,-1.8+(i//3)*.46,0],radius=.105,color=TEXT) for i in range(24)])
        self.play(LaggedStart(*[FadeIn(d) for d in more],lag_ratio=.12),Transform(slow,gauge('cleft K+',3,1)),
            run_time=2.4,rate_func=smooth); self.finish()


class S16Ek(SpokenScene):
    def construct(self):
        # Explicit axes at lower edge: no implicit zero-axis crossing.
        def pt(k,v): return np.array([-4.7+(k-5)/17*7.6,-2.35+(v+90)/50*4.8,0])
        self.add(Line(pt(5,-90),pt(22,-90),color=GREY),Line(pt(5,-90),pt(5,-40),color=GREY),
            label('Illustrative · 140 mM inside · 37 °C',y=3.25,size=28,color=GREY),
            label('E (K) · mV',-4.8,2.85,26),label('Cleft potassium (mM)',-.9,-3.2,28))
        for v in [-80,-60,-40]:
            self.add(label(str(v).replace('-','−'),-5.4,pt(5,v)[1],26,GREY))
        for k in [7,20]:
            q=pt(k,-90); self.add(Line(q+UP*.08,q+DOWN*.08,color=GREY),label(str(k),q[0],-2.75,26,GREY))
        curve=VMobject(color=TEXT,stroke_width=4).set_points_smoothly([pt(k,ek(k)) for k in np.linspace(5,22,160)])
        k=ValueTracker(7)
        dot=always_redraw(lambda:Dot(pt(k.get_value(),ek(k.get_value())),radius=.11,color=PURPLE))
        guides=always_redraw(lambda:VGroup(DashedLine(pt(k.get_value(),-90),dot.get_center(),color=GREY),
            DashedLine(pt(5,ek(k.get_value())),dot.get_center(),color=GREY)))
        read=always_redraw(lambda:VGroup(label(f'{k.get_value():.0f} mM',4.7,1,30),
            label(f'{ek(k.get_value()):.0f} mV'.replace('-','−'),4.7,0,32,PURPLE)))
        self.add(curve,guides,dot,read)
        self.at("and potassium's reversal potential")
        self.play(k.animate.set_value(20),run_time=1.5); self.finish()


class S17Rule(SpokenScene):
    def construct(self):
        self.add(gauge('cleft potential',.45,0,GOLD),gauge('cleft K+',3,1),voltage(-.8),
            label('Steady state',-3.8,3.1,30,GREY),label('Other conductances\nheld fixed',-3.8,1.9,28,GREY),
            label('E (K)',-3.8,.3,32),label('−80 → −52 mV',-3.8,-.5,32,PURPLE),
            label('7 → 20 mM raises E (K)',-3.8,-1.7,26),label('Direction only · no absolute calyx voltage',y=-3.2,size=26,color=GREY))
        v=self.mobjects[2]
        self.at('this shift tends')
        self.play(v[1].animate.set_y(1.25),Create(DashedLine([-2,-.4,0],[5.1,1.25,0],color=PURPLE,stroke_opacity=.45)),run_time=1.2)
        self.finish()


class S18Potential(SpokenScene):
    def construct(self):
        g=cleft(); fast=gauge('cleft potential',.45,0,GOLD); slow=gauge('cleft K+',3,1); v=voltage(0)
        self.add(g,fast,slow,v,label('K+ stays elevated',2.6,-3,26,GREY))
        arrow=arr([-1.4,.25,0],[-3.35,.25,0],TEXT); self.add(arrow,label('K+',-3,1.2,28))
        self.at('quickly'); self.play(Transform(fast,gauge('cleft potential',.45,.9,GOLD)),run_time=.25)
        self.at('Less potassium leaves')
        self.play(Transform(arrow,arr([-2,.25,0],[-2.85,.25,0],TEXT)),run_time=.5)
        self.at('or some enters'); self.play(Transform(arrow,arr([-3.35,.25,0],[-1.4,.25,0],TEXT)),run_time=.5)
        self.at('so it depolarizes'); self.play(v[1].animate.set_y(1.75),g[1].animate.set_fill(opacity=.35),run_time=.5)
        self.finish()


class S19Model(SpokenScene):
    def construct(self):
        a=chip('potassium',TEXT,34).move_to([-3,1.1,0]); b=chip('cleft potential',GOLD,34).move_to([3,1.1,0])
        self.add(a,b,label('Order in our explanation',y=2.7,size=34),
            arr([-5.5,-1.9,0],[5.5,-1.9,0],GREY),label('earlier',-4.9,-2.5,28,GREY),label('later',4.9,-2.5,28,GREY))
        self.at('in a model')
        self.play(Transform(self.mobjects[2],label('Model output · Govindaraju et al.',y=2.7,size=32,color=GOLD)),run_time=.3)
        self.at('the cleft potential acts first')
        self.play(MoveAlongPath(a,ArcBetweenPoints(a.get_center(),[3,1.1,0],angle=PI/3)),
            MoveAlongPath(b,ArcBetweenPoints(b.get_center(),[-3,1.1,0],angle=PI/3)),
            GrowArrow(arr([-3,.4,0],[-3,-1.7,0],GOLD)),run_time=.75)
        self.at('and potassium later'); self.play(GrowArrow(arr([3,.4,0],[3,-1.7,0],TEXT)),run_time=.4)
        self.at('That order is a prediction'); self.play(FadeIn(label('Not a measurement',y=-3.3,size=30,color=GOLD)),run_time=.4)
        self.finish()


class S20Evidence(SpokenScene):
    def construct(self):
        e=evidence(); self.add(*e[:6]); self.add(e[6].copy().set_opacity(.25),e[7].copy().set_opacity(.25)); self.add(e[8].copy().set_opacity(.15),e[9].copy().set_opacity(.15))
        self.at('Mouse knockouts'); self.play(FadeIn(e[6]),run_time=.4)
        self.at('young rat'); self.play(FadeIn(e[7]),run_time=.4); self.finish()


class S21Turtle(SpokenScene):
    def construct(self):
        e=evidence(); self.add(*e[:8]); self.add(e[8].copy().set_opacity(.15),e[9].copy().set_opacity(.15))
        self.at('turtle recordings'); self.play(FadeIn(e[8]),run_time=.3)
        self.at('both cells together')
        self.play(FadeIn(T('paired cells · ↔ both directions',24,PURPLE).move_to([-5.7,-1.3,0],aligned_edge=LEFT)),run_time=.3)
        self.at('a slow coupling')
        slow=VGroup(T('slow: fits potassium build-up',24).move_to([-5.7,-1.76,0],aligned_edge=LEFT),
            Line([1,-1.76,0],[4.5,-1.76,0],color=TEXT,stroke_width=7))
        slow[1].next_to(slow[0],RIGHT,buff=.3)
        self.play(Create(slow),run_time=.4)
        self.at('a much faster one')
        fast=VGroup(T('fast: proposed resistive coupling',24,PURPLE).move_to([-5.7,-2.21,0],aligned_edge=LEFT),
            Line([1,-2.21,0],[1.35,-2.21,0],color=PURPLE,stroke_width=7))
        fast[1].next_to(fast[0],RIGHT,buff=.3)
        self.play(Create(fast),FadeIn(e[9]),run_time=.4); self.finish(); self.wait(.8)


class S23Takeaway(SpokenScene):
    def construct(self):
        c=hair_cell(1).scale(1.6).move_to([-3.8,0,0])
        routes=VGroup(arr([-2.3,.4,0],[.1,1.8,0],TEXT),arr([-2.3,-.4,0],[.1,-1.8,0],PURPLE))
        preview_ves=vesicles(.8,1.6).scale(2.8).set_opacity(.25)
        preview_bars=VGroup(Line([.5,-2.45,0],[.5,-.95,0],color=GOLD,stroke_width=14),
            VMobject(color=PURPLE,stroke_width=9,fill_opacity=0).set_points_as_corners([[1,-2.45,0],[1.65,-2.45,0],[1.65,-1,0],[2.3,-1,0]])).set_opacity(.25).set_fill(opacity=0)
        self.add(c,routes,preview_ves,preview_bars,label('Two routes from a type I cell',y=3.2,size=36))
        self.at('One waits for vesicles')
        ves=vesicles(.8,1.6).scale(2.8)
        self.play(FadeIn(ves),FadeIn(label('Waits for vesicles',3.8,1.7,30)),run_time=.45)
        self.at('One does not')
        bars=VGroup(Line([.5,-2.45,0],[.5,-.95,0],color=GOLD,stroke_width=14),
            VMobject(color=PURPLE,stroke_width=9,fill_opacity=0).set_points_as_corners([[1,-2.45,0],[1.65,-2.45,0],[1.65,-1,0],[2.3,-1,0]]))
        self.play(Create(bars),FadeIn(label('Needs no vesicle',4.4,-1.7,30,PURPLE)),
            FadeIn(label('cleft potential → calyx voltage',3,-2.9,26,PURPLE)),run_time=.5); self.finish(); self.wait(1.5)


class S21End(EndCard):
    LINE='One route waits for vesicles. One does not.'

    def construct(self):
        g=VGroup(T(self.LINE,40,font=TITLE_FONT),T('biochemistrypedia.com',26,TEAL)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.5); self.finish()
