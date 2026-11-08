"""Why Capsaicin Feels Hot — reviewer fix round.
COLOR MAP: BLUE/cyan = cold/TRPM8; ORANGE = pain/heat/TRPV1;
YELLOW = signal/calcium; RED = knockout; GREEN = weakness; GREY = structure.
Calcium curves are computed categorical observations, R(t)=P*1[t>=stimulus],
P=0/1 for negative/positive pools. They are schematic, not measured kinetics.
The heat experiment uses the same rule with P=1[T>43] and a rising bath temperature.
"""
import numpy as np
from bp_style import *
ORANGE = '#F29E4C'
PAIN, COLD, SIG = ORANGE, BLUE, YELLOW


def label(s, x=0, y=0, size=30, color=TEXT):
    return T(s, size=size, color=color, line_spacing=.8).move_to([x,y,0])


def block(s,x,y,color=GREY,size=28):
    g=chip(s,color=color,size=size).move_to([x,y,0])
    g[0].set_fill(BG,opacity=1)
    return g


def arr(a,b,color=GREY):
    return Arrow([*a,0],[*b,0],buff=0,tip_length=.18,
                 max_tip_length_to_length_ratio=.16,color=color,stroke_width=4)


def gate(x=0,y=0,color=PAIN,opened=False,scale=1):
    membrane=VGroup(Line([-2.1,0,0],[-.62,0,0],color=GREY,stroke_width=10),
                    Line([.62,0,0],[2.1,0,0],color=GREY,stroke_width=10)).set_z_index(1)
    # Opening is a lateral separation of the two channel walls, never a sliding bar.
    walls=VGroup(*[RoundedRectangle(width=.48,height=2.6,corner_radius=.2,
                    color=color,fill_color=interpolate_color(ManimColor(BG),ManimColor(color),.35),
                    fill_opacity=1).move_to([s*(.65 if opened else .23),0,0]) for s in [-1,1]]).set_z_index(2)
    return VGroup(membrane,walls).scale(scale).shift([x,y,0])


def neuron(color=PAIN):
    soma=Circle(.8,color=color,fill_color=color,fill_opacity=.16).move_to([-4,.1,0])
    nucleus=Circle(.22,color=color).move_to(soma)
    axon=VGroup(Line([-3.2,.27,0],[.1,.27,0],color=color,stroke_width=5),
                Line([-3.2,-.07,0],[.1,-.07,0],color=color,stroke_width=5))
    ending=Ellipse(width=3.5,height=2.8,color=color,fill_color=color,fill_opacity=.06).move_to([1.7,.1,0])
    branches=VGroup(*[Line([-4.5,yy,0],[xx,yy+dy,0],color=color,stroke_width=4)
        for yy,xx,dy in [(.7,-5.7,1.1),(.1,-5.9,-.2),(-.5,-5.6,-1.3)]])
    # Channel is embedded in the upper terminal membrane; background masks the rim.
    mask=Rectangle(width=1.25,height=.45,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([1.7,1.5,0])
    ch=gate(1.7,1.5,color,scale=.65)
    return VGroup(branches,soma,nucleus,axon,ending,mask,ch)


def neuron_labels():
    return VGroup(label('sensory neuron',-3.2,-2.25,30),
        label('ending membrane',2,-2.25,28,GREY),arr((2,-1.95),(2,-1.3)))


def thermometer(x=3,y=0,cold=False):
    col=COLD if cold else PAIN
    return VGroup(RoundedRectangle(width=.5,height=3.3,corner_radius=.24,color=GREY).move_to([x,y,0]),
        Circle(.43,color=col,fill_color=col,fill_opacity=1).move_to([x,y-1.4,0]),
        Line([x,y-1.4,0],[x,y+.7,0],color=col,stroke_width=10),
        label('skin temperature',x,y-2.2,28),label('unchanged',x,y+2.2,30,col))


def pepper():
    body=VMobject(color=RED,fill_color=RED,fill_opacity=.85)
    body.set_points_smoothly([[-.7,1.55,0],[.3,1.45,0],[.85,.4,0],[.5,-.9,0],[-.6,-1.8,0],[-2,-2.1,0],[-1,-.9,0],[-.9,.4,0],[-.7,1.55,0]])
    stem=VMobject(color=GREEN,stroke_width=12).set_points_smoothly([[-.3,1.5,0],[-.25,2,0],[.2,2.3,0]])
    return VGroup(body,stem).shift(LEFT*1.8+UP*.3)


def leaf(x=-2.8,y=.1):
    outline=VMobject(color=COLD,fill_color=COLD,fill_opacity=.2,stroke_width=4)
    outline.set_points_smoothly([[0,-1.65,0],[-1.1,-.6,0],[-.95,.7,0],[0,1.9,0],[.95,.7,0],[1.1,-.6,0],[0,-1.65,0]])
    veins=VGroup(Line([0,-1.9,0],[0,1.65,0],color=COLD,stroke_width=4))
    for yy in [-.9,-.2,.5,1.05]:
        for sign in [-1,1]:
            veins.add(Line([0,yy,0],[sign*(.75 if yy<.8 else .4),yy+.45,0],color=COLD,stroke_width=2))
    return VGroup(outline,veins).shift([x,y,0])


def flame(x,y):
    # Separate Bezier curves preserve a sharp tip and an asymmetric flame lick.
    m=VMobject(color=PAIN,fill_color=PAIN,fill_opacity=.8)
    m.start_new_path([.1,1.35,0])
    m.add_cubic_bezier_curve_to([.15,.45,0],[.95,.05,0],[.6,-.6,0])
    m.add_cubic_bezier_curve_to([.25,-1.15,0],[-.65,-.9,0],[-.65,-.35,0])
    m.add_cubic_bezier_curve_to([-.7,.1,0],[-.25,.45,0],[.1,1.35,0])
    flick=VMobject(color=SIG,fill_color=SIG,fill_opacity=1,stroke_width=1)
    flick.start_new_path([.06,.35,0])
    flick.add_cubic_bezier_curve_to([.05,-.05,0],[.45,-.3,0],[.2,-.65,0])
    flick.add_cubic_bezier_curve_to([-.3,-.9,0],[-.4,-.25,0],[.06,.35,0])
    return VGroup(m,flick).scale(.55).shift([x,y,0])


def snow(x,y,r=.65):
    g=VGroup()
    for a in np.arange(6)*np.pi/3:
        v=np.array([np.cos(a),np.sin(a),0]);p=np.array([-v[1],v[0],0])
        g.add(Line(ORIGIN,r*v,color=COLD,stroke_width=4))
        for sign in [-1,1]:
            g.add(Line(.62*r*v,.43*r*v+sign*.22*r*p,color=COLD,stroke_width=3))
    return g.shift([x,y,0])


def dish(x=-3.6,y=0,scale=1):
    bowl=Ellipse(width=3,height=2,color=GREY,fill_color=GREY,fill_opacity=.1)
    cells=VGroup(*[Circle(.25,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([dx,dy,0])
        for dx,dy in [(-.65,.25),(.25,.4),(.7,-.25),(-.4,-.4)]])
    return VGroup(bowl,cells).scale(scale).shift([x,y,0])


def trace(x=.3,y=-2,w=5.1,h=4.3,positive=False,stimulus='capsaicin',mini=False):
    # Explicit categorical response model. A doubled stimulus coordinate gives a true step.
    def point(t,v): return np.array([x+w*t/4,y+.14+h*.8*v,0])
    axis=VGroup(Line([x,y,0],[x+w,y,0],color=GREY),Line([x,y,0],[x,y+h,0],color=GREY))
    ts=np.array([0,1.4-1e-7,1.4,4.]);rs=int(positive)*(ts>=1.4)
    curve=VMobject(color=SIG,stroke_width=4).set_points_as_corners([point(t,v) for t,v in zip(ts,rs)])
    mark=DashedLine([x+w*.35,y,0],[x+w*.35,y+h,0],color=PAIN,stroke_width=2)
    words=VGroup(label('time',x+w-.35,y-.38,26),label('calcium',x+.7,y+h+.4,26,SIG),
                 label(stimulus,x+w*.55,y+h+.4,26,PAIN)) if not mini else VGroup()
    return VGroup(axis,curve,mark,words)


def experiment(positive=False):
    return VGroup(dish(-3.5,0,1.35),label('HEK293 cells',-3.5,2.6,32),
                  trace(positive=positive),label('schematic calcium response',1,-3.15,26,GREY))


def pool_screen():
    g=VGroup(label('HEK293 cells: pool screen',0,3.15,34))
    for i,yy in enumerate([1.8,0,-1.8]):
        g.add(dish(-4.4,yy,.8),trace(-1.3,yy-.5,6.7,1,mini=True),
              label('capsaicin',1.05,yy+.72,26,PAIN),label('time',5.9,yy-.82,26))
    g.add(label('calcium',-1.85,1.8,26,SIG).rotate(PI/2))
    g.add(label('cDNA: copies of sensory neuron genes',0,-3.25,28))
    return g


def question():
    return VGroup(gate(1.2,0,COLD,True,1.65),block('chemical',-4,1.7,COLD,32),
        VGroup(snow(-4,-.8,.85),label('cool',-4,-2.1,32,COLD)),
        VGroup(arr((-2.65,1.7),(-.33,1.0),COLD),arr((-2.9,-.8),(-.33,-.6),COLD)),
        label('How will it feel on the skin?',0,-3.2,36))


def overview():
    boxes=VGroup(*[RoundedRectangle(width=3.8,height=4.8,corner_radius=.18,color=GREY,
        fill_color=GREY,fill_opacity=.06).move_to([x,-.25,0]) for x in [-4.1,0,4.1]])
    names=VGroup(*[label(s,x,1.5,34,SIG if i==0 else TEXT) for i,(s,x) in enumerate(zip(['report','route','volume'],[-4.1,0,4.1]))])
    # Visual placeholders echo line, destination, and gain without claiming a mechanism.
    marks=VGroup(arr((-5.25,.25),(-2.95,.25),SIG),
        VGroup(arr((-.95,.25),(.8,.25)),Dot([1,.25,0],radius=.13,color=GREY)),
        VGroup(*[Line([xx,-.2,0],[xx,hh,0],color=GREY,stroke_width=6) for xx,hh in [(3.4,.1),(4.1,.45),(4.8,.8)]]))
    return VGroup(label('Follow the line',0,3.1,46),boxes,names,marks)


def mouse(x=0,color=GREY,scale=1):
    body=Ellipse(width=2.5,height=1.5,color=color,fill_color=color,fill_opacity=.15)
    head=Circle(.55,color=color,fill_color=BG,fill_opacity=1).move_to([1.1,.4,0])
    ear=Circle(.3,color=color).move_to([1,1,0])
    eye=Dot([1.32,.52,0],radius=.05,color=TEXT)
    tail=VMobject(color=color,stroke_width=4).set_points_smoothly([[-1.25,0,0],[-1.75,.1,0],[-1.9,.6,0],[-1.5,.75,0]])
    feet=VGroup(*[Line([xx,-.5,0],[xx+.2,-.95,0],color=color,stroke_width=4) for xx in [-.7,.6]])
    return VGroup(body,head,ear,eye,tail,feet).scale(scale).shift([x,0,0])


def results(n=2):
    head=VGroup(label('TRPV1 knockout',1.5,3.1,38,PAIN),mouse(-4.5,scale=.52).shift(UP*2.7),
        mouse(-2.3,RED,.52).shift(UP*2.7),label('control / no TRPV1',-3.5,1.65,26))
    rows=VGroup()
    for yy,(s,v,c) in zip([.7,-.7,-2.1],[('Capsaicin pain behaviour','gone',RED),('Hot-plate heat response','partly impaired',PAIN),('Filament poke','normal',TEXT)][:n]):
        rows.add(VGroup(label(s,-2.65,yy,30),arr((.65,yy),(1.35,yy)),block(v,3.9,yy,c,30)))
    return VGroup(head,rows)


class S00Title(TitleCard):
    LESSON='Touch and Pain'
    TITLE='Why Capsaicin Feels Hot'
    def construct(self):
        self.add(label('TOUCH AND PAIN',0,1.5,28,GREY),label(self.TITLE,0,0,48),label('BIOCHEMISTRYPEDIA',0,-1.3,26,TEAL))
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        self.add(pepper(),thermometer(3.4,.1))
        self.at('carries no heat');self.play(Indicate(self.mobjects[1],color=SIG),run_time=.45)
        self.at('So why does',lead=.6);self.add(label('Why does it burn?',0,-3.25,42))
        self.finish()


class S02Hunt(SpokenScene):
    def construct(self):
        self.add(neuron(),neuron_labels(),label('Caterina, Julius and colleagues · 1997',0,3.1,30))
        self.at('looked for the protein')
        self.play(FadeIn(label('?',3.8,1.9,54,SIG)),Create(Line([3.45,1.8,0],[2.2,1.5,0],color=SIG)),run_time=.4)
        self.finish()


class S03Cells(SpokenScene):
    def construct(self):
        self.add(dish(0,0,2),label('HEK293 cells',0,2.7,38))
        self.at('do not normally respond');self.play(FadeIn(label('capsaicin → no response',0,-2.8,34,PAIN)),run_time=.35)
        self.finish()


class S04Pools(SpokenScene):
    def construct(self):
        s=pool_screen();self.add(s)
        self.at('They added pools')
        for yy in [1.8,0,-1.8]:
            p=block('cDNA pool',-3.1,yy+.65,SIG,22)
            self.play(FadeIn(p),run_time=.18)
            self.play(p.animate.move_to([-4.4,yy,0]),run_time=.38)
            self.play(FadeOut(p,scale=.6),s[1+[1.8,0,-1.8].index(yy)*4][1].animate.set_color(SIG),run_time=.2)
        self.at('copies of sensory');self.play(Indicate(s[-1],scale_factor=1.02),run_time=.4)
        self.at('and watched calcium');self.play(Indicate(s[-2]),run_time=.35)
        self.finish()


class S05Flat(SpokenScene):
    def construct(self):
        e=experiment();self.add(e,label('most pools',-3.5,-2.3,32,GREY))
        self.at('capsaicin did nothing');self.play(Indicate(e[2][1],scale_factor=1.01),run_time=.5)
        self.finish()


class S06Jump(SpokenScene):
    def construct(self):
        e=experiment();self.add(e)
        self.at('A positive pool');self.play(ReplacementTransform(e[2][1],trace(positive=True)[1]),run_time=.6)
        self.at('Splitting that pool');self.clear()
        levels=[2.65,.85,-.95,-2.75]
        root=block('positive pool',-2.5,levels[0],SIG,28);self.add(root)
        parent=root
        self.add(label('repeat the positive test',2.4,3.3,28),trace(1,2.3,4.7,.65,True,mini=True))
        for j,yy in enumerate(levels[1:]):
            if j==1:self.at('again and again')
            if j==2:self.at('left a single')
            prev=levels[j]
            winner=block(['½ pool','½ again','one cDNA'][j],-2.5,yy,SIG,28)
            loser=block('negative',-5.15,yy,GREY,26)
            self.play(GrowArrow(arr(parent.get_bottom()[:2],winner.get_top()[:2],SIG)),
                GrowArrow(arr(parent.get_left()[:2],loser.get_top()[:2])),FadeIn(winner),FadeIn(loser),
                Create(trace(1,yy-.35,4.7,.65,True,mini=True)),run_time=.45)
            parent=winner
        self.add(label('calcium · schematic positive tests',2.7,-3.5,26,SIG))
        self.finish()


class S07Named(SpokenScene):
    def construct(self):
        self.add(gate(scale=1.85))
        name=label('VR1',0,3,44,PAIN);self.add(name)
        self.at('now called');self.play(ReplacementTransform(name,label('TRPV1',0,3,44,PAIN)),run_time=.35)
        self.add(label('nonselective cation channel',0,-3,30,GREY));self.finish()


def heat_frame(hot=True):
    g=gate(-2,.1,PAIN,hot,1.05)
    t=trace(.55,-2.05,5.3,4.25,hot,'heat')
    temp=44 if hot else 37
    ty=lambda value:-1.75+(value-37)*.49
    meter=VGroup(RoundedRectangle(width=.42,height=3.8,corner_radius=.2,color=GREY).move_to([-5.35,.1,0]),
        Circle(.34,color=PAIN,fill_color=PAIN,fill_opacity=1).move_to([-5.35,-1.75,0]),
        Line([-5.35,-1.75,0],[-5.35,ty(temp),0],color=PAIN,stroke_width=9),
        DashedLine([-5.85,ty(43),0],[-4.75,ty(43),0],color=TEXT),label('43 °C',-4.2,ty(43),26),
        label(f'{temp} °C',-5.1,2.75,32,PAIN),label('bath\ntemperature',-5,-2.65,26))
    ions=VGroup(arr((-2,.9),(-2,-1.2),SIG),label('Ca2+ in',-2,-1.8,28,SIG)) if hot else VGroup()
    note=VGroup(label('cloned rat channel',-1.65,-3.5,28,GREY),
                label('foreign cell',2.1,-3.5,28,GREY))
    return VGroup(g,label('TRPV1',-2,2.75,34,PAIN),t,meter,ions,note)


class S08Heat(SpokenScene):
    def construct(self):
        h=heat_frame(False);self.add(h)
        self.at('Here is the surprise');self.play(Indicate(h[1]),run_time=.4)
        self.at('also opens with heat')
        ty=lambda value:-1.75+(value-37)*.49
        for value in [39,41,42,43]:
            h[3][5].become(label(f'{value} °C',-5.1,2.75,32,PAIN))
            self.play(h[3][2].animate.put_start_and_end_on([-5.35,-1.75,0],[-5.35,ty(value),0]),run_time=.3)
        self.at('above about')
        h[3][5].become(label('44 °C',-5.1,2.75,32,PAIN))
        self.play(h[3][2].animate.put_start_and_end_on([-5.35,-1.75,0],[-5.35,ty(44),0]),run_time=.35)
        hot=heat_frame(True)
        self.play(Transform(h[0],hot[0]),Create(hot[4]),ReplacementTransform(h[2][1],hot[2][1]),run_time=.45)
        self.finish()


class S08Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(heat_frame());self.wait(1)


class S09Hedge(SpokenScene):
    def construct(self):
        h=heat_frame();self.add(h)
        note=h[-1]
        self.at('That was the cloned rat channel')
        self.play(*[FadeOut(m) for m in h[:-1]],
            Transform(note,VGroup(label('cloned rat channel',0,.9,40,PAIN),
                                  label('foreign cell',0,0,40,TEXT))),run_time=.6)
        self.at('in a foreign cell');self.play(Indicate(note[1],scale_factor=1.03),run_time=.3)
        self.at('not human perception')
        self.add(label('not human perception',0,-.9,40,TEXT))
        self.wait(1.6)
        self.finish()


class S10Report(SpokenScene):
    def construct(self):
        n=neuron();self.add(n,label('TRPV1',1.7,3.05,36,PAIN),label('same sensory neuron',-3.3,-1.6,28))
        self.at('So capsaicin burns')
        self.play(FadeIn(block('capsaicin',-3,2.8,PAIN,30)),GrowArrow(arr((-1.65,2.8),(1.08,2.1),PAIN)),run_time=.4)
        self.at('noxious heat also')
        self.play(FadeIn(flame(5,2.05)),FadeIn(label('heat',5,3.2,30,PAIN)),GrowArrow(arr((4.4,2.25),(2.32,2.1),PAIN)),run_time=.35)
        self.play(Transform(n[-1],gate(1.7,1.5,PAIN,True,.65)),
            GrowArrow(arr((-1.4,.1),(-3.2,.1),SIG)),FadeIn(label('heat-sensitive neuron activity',1,-3.2,32,SIG)),run_time=.4)
        self.finish()


class S11Predict(SpokenScene):
    def construct(self):
        q=question();g=gate(1.2,0,COLD,False,1.65);self.add(label('Predict',0,3.1,40),g)
        self.at('A chemical opens');self.play(FadeIn(q[1]),GrowArrow(q[3][0]),Transform(g,q[0]),run_time=.4)
        self.at('cool temperatures also');self.play(FadeIn(q[2]),GrowArrow(q[3][1]),run_time=.4)
        self.at('How will it feel');self.add(q[4]);self.finish()


class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(label('Predict',0,3.1,40),question());self.wait(5)


class S13Cool(SpokenScene):
    def construct(self):
        n=neuron(COLD).center().shift(DOWN*.1);nl=label('cold-sensitive neurons',0,-2.8,32,COLD)
        self.add(n,label('Most likely cool',0,3.1,42,COLD))
        self.at('mainly drives');self.play(FadeIn(nl),run_time=.3)
        self.at('That chemical is menthol');self.play(FadeOut(n),FadeOut(nl),FadeIn(leaf(y=-.35)),FadeIn(label('menthol · mint',-2.8,2.05,32,COLD)),run_time=.4)
        self.at('Mint can feel cool');self.play(FadeIn(thermometer(3,.1,True)),run_time=.4)
        self.add(label('cooling feeling ≠ cooler skin',0,-3.25,32,COLD));self.finish()


class S14Trpm8(SpokenScene):
    def construct(self):
        g=gate(1.25,0,COLD,False,1.65);self.add(g,label('McKemy and colleagues · 2002',0,-3.2,28,GREY))
        self.at('Its receptor is called');self.play(FadeIn(label('TRPM8',0,3.1,44,COLD)),run_time=.3)
        self.add(block('menthol',-4,1.5,COLD,30),arr((-2.8,1.5),(-.3,.8),COLD))
        self.at('Cool temperatures open');self.play(FadeIn(snow(-4,-.8,.6)),FadeIn(label('cool / cold',-4,-2,30,COLD)),
            GrowArrow(arr((-2.8,-.8),(-.3,-.6),COLD)),Transform(g,gate(1.25,0,COLD,True,1.65)),run_time=.5)
        self.finish()


class S15Need(SpokenScene):
    def construct(self):
        panels=VGroup(*[RoundedRectangle(width=5.3,height=5.6,corner_radius=.2,color=GREY).move_to([x,0,0]) for x in [-3.1,3.1]])
        self.add(panels,label('foreign cell',-3.1,2.1,36),label('animal',3.1,2.1,36),dish(-3.1,.3,1.1),mouse(3.1,scale=1.1))
        self.at('what is enough');self.play(FadeIn(label('SUFFICIENT',-3.1,-2,36,SIG)),run_time=.3)
        self.at('Does the animal need it');self.play(FadeIn(label('NECESSARY?',3.1,-2,36,SIG)),run_time=.3)
        self.finish()


class S16Ko(SpokenScene):
    def construct(self):
        self.add(label('TRPV1',0,3.2,42,PAIN),mouse(-3,scale=1.65),mouse(3,scale=1.65),
            label('littermate control',-3,-2.2,30),label('VR1-null',3,-2.2,32,RED))
        self.at('and colleagues');self.add(label('Caterina and colleagues · 2000',0,-3.2,28,GREY))
        self.at('that gene out')
        gene=block('TRPV1 gene',3,2.65,PAIN,28);self.add(gene)
        self.play(gene[1].animate.set_opacity(.4),gene[0].animate.set_stroke(RED),
            FadeIn(block('no TRPV1',2.7,0,RED,28)),run_time=.4)
        self.finish()


class S17Result1(SpokenScene):
    def construct(self):
        r=results();self.add(r[0])
        self.at('The mice showed');self.add(r[1][0][0])
        self.at('no pain');self.play(GrowArrow(r[1][0][1]),FadeIn(r[1][0][2]),run_time=.3)
        self.at('Their detection');self.play(FadeIn(r[1][1][0]),run_time=.3)
        self.at('only partly impaired');self.play(GrowArrow(r[1][1][1]),FadeIn(r[1][1][2]),run_time=.3)
        self.finish()


class S18Result2(SpokenScene):
    def construct(self):
        r=results(3);self.add(r[0],r[1][0],r[1][1])
        self.at('Mechanical responses');self.add(r[1][2][0])
        self.at('were normal');self.play(GrowArrow(r[1][2][1]),FadeIn(r[1][2][2]),run_time=.3)
        self.at('the heat loss');self.play(Indicate(r[1][1][2][1],color=SIG,scale_factor=1.03),run_time=.4)
        self.at('So other sensors exist');self.add(label('Other sensors exist',0,-2.9,30,SIG))
        self.at('is not the pain receptor');self.add(label('TRPV1 ≠ the pain receptor',0,-3.5,30,PAIN));self.finish()


class S19Idea(SpokenScene):
    def construct(self):
        o=overview();self.add(o)
        self.at('Follow the line');self.play(Indicate(o[0]),run_time=.4);self.finish()


class S20Idea1(SpokenScene):
    def construct(self):
        o=overview();self.add(o)
        self.at('A sensory');self.play(o[1][0].animate.set_stroke(SIG,width=4),run_time=.3)
        active=label('active line',-4.1,-.65,28,SIG)
        strength=label('how strongly',-4.1,-1.5,28,SIG)
        self.at('which line is active');self.add(active)
        self.at('how strongly');self.play(o[3][0].animate.set_stroke(width=9),FadeIn(strength),run_time=.3)
        self.at('But it does not')
        # Expand the report slot, giving the complete statement its own readable space.
        self.play(FadeOut(VGroup(o[1],o[2],o[3],active,strength)),run_time=.25)
        self.clear();self.add(o[0])
        card=RoundedRectangle(width=11.5,height=4.6,corner_radius=.2,color=SIG).move_to([0,-.3,0])
        self.add(card,label('report',0,1.25,34,SIG),
            label('Firing identifies the active line\nand reports how strongly it fires;\nit need not uniquely identify\nwhat activated it.',0,-.65,32))
        self.finish()


class S21Idea2(SpokenScene):
    def construct(self):
        # Reuse the neuron ending and its embedded channel from the discovery scene.
        a=neuron(PAIN).scale(.62).center().move_to([-3.2,0,0])
        b=neuron(COLD).scale(.62).center().move_to([3.2,0,0])
        self.add(a,b,label('TRPV1',-3.2,-2.6,34,PAIN),label('TRPM8',3.2,-2.6,34,COLD))
        self.at('decide what can activate')
        self.play(FadeIn(label('capsaicin · heat · protons',-3.2,2.8,27,PAIN)),FadeIn(label('cool · menthol',3.2,2.8,30,COLD)),
            GrowArrow(arr((-3.2,2.4),a[-1].get_top()[:2]+UP[:2]*.1,PAIN)),
            GrowArrow(arr((3.2,2.4),b[-1].get_top()[:2]+UP[:2]*.1,COLD)),run_time=.35)
        self.add(snow(5.55,2.8,.36),label('protons lower the heat threshold',0,-3.25,30,TEXT));self.finish()


class S22Idea3(SpokenScene):
    def construct(self):
        o=overview();self.add(o,label('active line',-4.1,-.65,28,SIG),label('how strongly',-4.1,-1.5,28,SIG))
        self.at('The next two films');self.add(label('next films',0,-3.25,30,TEAL))
        self.at('where each line goes');self.add(label('where it goes',0,-1.3,28,SIG));self.play(o[1][1].animate.set_stroke(SIG,width=4),run_time=.25)
        self.at('who turns it up');self.add(label('who turns it up',4.1,-1.3,28,SIG));self.play(o[1][2].animate.set_stroke(SIG,width=4),run_time=.25)
        self.finish()


class S24Takeaway(SpokenScene):
    def construct(self):
        self.add(label('Firing identifies the active line;\nit need not uniquely identify what activated it.',0,2.7,32,SIG),
                 neuron().scale(.78).shift(DOWN*.15))
        q1=label('Which neurons were driven?',0,-2.35,34)
        q2=label('What can drive them?',0,-3.2,34)
        self.at('which neurons were driven');self.add(q1)
        self.at('what can drive them');self.add(q2);self.finish()


class S25End(EndCard):
    LINE='Ask which neurons were driven and what can drive them.'
    def construct(self):
        self.add(label('Ask which neurons were driven\nand what can drive them.',0,.5,42),
            label('biochemistrypedia.com',0,-1.6,32,TEAL))
        self.finish()
