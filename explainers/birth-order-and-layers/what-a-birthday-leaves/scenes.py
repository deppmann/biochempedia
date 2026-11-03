"""What a Birthday Leaves Behind — reviewed animation.
COLOR MAP: ORANGE early/deep cohort and Tbr1 marker; YELLOW second cohort
and Ctip2/Fezf2 marker; BLUE upper cohort and Satb2 marker; PURPLE progenitor;
PINK subplate tissue; GREEN third cohort (not assigned a marker here);
TEAL thymidine pulse; GABA mint interneurons, distinct from excitatory cohorts;
GREY tissue/axes/unassigned cells. Marker overlays do not recolour tissue bands.
Q is evaluated from the lesson's eleven-cycle illustrative preset, not fitted data.
"""
import numpy as np
from bp_style import *
ORANGE, PURPLE, PINK = '#F29E4C', '#B58CD9', '#E58FB4'
GABA = '#6FE0B5'
LESSON = 'Birth Order and Fate: Temporal Identity and the Inside-Out Cortex'
Q_VALUES = np.array([.1,.15,.2,.25,.3,.35,.4,.5,.65,.8,.8])

def nd(color,x,y,r=.24):
    return Circle(radius=r,stroke_color=color,stroke_width=2,fill_color=color,fill_opacity=.9).move_to([x,y,0])

def arr(a,b,color=GREY):
    return Arrow(a,b,buff=.10,color=color,stroke_width=3,tip_length=.18)

def label(s,x,y,color=TEXT,size=30):
    return T(s,size,color).move_to([x,y,0])

def head(s): return label(s,0,3.15,size=36)

def box(w,h,x,y,color=GREY):
    return RoundedRectangle(width=w,height=h,corner_radius=.16,color=color,stroke_width=2).move_to([x,y,0])

def column(coloured=True):
    ys=[-2.5,-1.5,-.5,.5,1.5,2.5]
    colors=[PINK,ORANGE,YELLOW,GREY,BLUE,BLUE]
    shell=Rectangle(width=3.6,height=6.3,color=GREY,stroke_width=2).move_to([-3.7,0,0])
    bands=VGroup(*[Rectangle(width=3.55,height=.94,stroke_width=0,fill_color=c,fill_opacity=.12).move_to([-3.7,y,0]) for c,y in zip(colors,ys)])
    rows=VGroup(*[VGroup(*[nd(c if coloured else GREY,x,y,.19) for x in [-4.65,-3.7,-2.75]]) for c,y in zip(colors,ys)])
    nums=VGroup(*[label(s,-5.95,y,GREY,36) for s,y in zip(['SP','6','5','4','3','2'],ys)])
    return VGroup(shell,bands,nums,rows)

def calendar(x=0,y=0,size=1):
    b=box(1.45,1.5,0,0,TEAL)
    bar=Line([-.7,.4,0],[.7,.4,0],color=TEAL)
    dots=VGroup(*[Dot([xx,yy,0],radius=.07,color=TEAL) for xx in [-.4,0,.4] for yy in [0,-.4]])
    return VGroup(b,bar,dots).scale(size).move_to([x,y,0])

def clock(x,y,r=1.45):
    return VGroup(Circle(radius=r,color=YELLOW,stroke_width=4).move_to([x,y,0]),Line([x,y,0],[x,y+r*.65,0],color=YELLOW,stroke_width=4),Line([x,y,0],[x+r*.5,y-r*.25,0],color=YELLOW,stroke_width=4))

def dish():
    return VGroup(Ellipse(width=10.8,height=4.9,color=GREY,stroke_width=4).move_to([0,-.15,0]),nd(PURPLE,0,-.15,.95))

def choices():
    return VGroup(label('A: deep-layer markers first, then later',0,-2.95,ORANGE),label('B: no order',0,-3.5,BLUE))

def prediction(): return VGroup(head('Pause and predict'),dish(),choices())

def forebrain():
    # Smooth schematic coronal section, confined to left two-thirds of the frame.
    points=[[-2.15,2.4,0],[-3.1,2.65,0],[-4.7,2.25,0],[-5.55,.8,0],[-5.3,-.8,0],[-4.5,-1.9,0],[-3.1,-2.25,0],[-2.1,-1.6,0],[-2.65,-.35,0],[-2.15,2.4,0]]
    left=VMobject(color=GREY,stroke_width=3).set_points_smoothly(points)
    right=left.copy().flip(UP,about_point=[-2,0,0])
    cortex=VGroup(ArcBetweenPoints([-5,1.9,0],[-2.4,2.5,0],angle=-.5,color=BLUE,stroke_width=9),ArcBetweenPoints([1,1.9,0],[-1.6,2.5,0],angle=.5,color=BLUE,stroke_width=9))
    ge=VGroup(*[Ellipse(width=1.65,height=1.2,color=GABA,fill_color=GABA,fill_opacity=.18).move_to([x,-1,0]) for x in [-3.55,-.45]])
    cells=VGroup(nd(GABA,-3.55,-1),nd(GABA,-.45,-1))
    return VGroup(left,right,cortex,ge,cells)

def anatomy_labels():
    return VGroup(label('cortex (dorsal)',-2.1,3.15,BLUE),label('ganglionic eminences',-2.1,-2.8,GABA),label('ventral forebrain',-2.1,-3.4,GREY))

def culture_results():
    early=VGroup(*[nd(ORANGE,x,y,.27) for x,y in [(-3,-.1),(-2.3,.55),(-2.3,-.75)]])
    late=VGroup(*[nd(BLUE,x,y,.27) for x,y in [(3,-.1),(2.3,.55),(2.3,-.75)]])
    labels=VGroup(label('deep-layer markers',-3,-2.65,ORANGE),label('later markers',3,-2.65,BLUE))
    time=VGroup(arr([-4.9,-3.1,0],[4.9,-3.1,0],TEXT),label('early culture',-3.4,-3.6),label('later culture',3.4,-3.6))
    credit=label('Shen and colleagues · Temple laboratory · 2006',0,2.7,GREY)
    return VGroup(early,late,labels,time,credit)

def options(shrunk=False):
    headers=VGroup(head('Open'),label('A: factor cascade',-3.3,2.25,YELLOW),label('B: gradual change\nin competence',3,2.05,PURPLE),Line([0,2.65,0],[0,-3.5,0],color=GREY))
    factors=VGroup(*[chip('factor '+str(i+1),YELLOW,30).move_to([-3.3,1-i*1.55,0]) for i in range(3)])
    links=VGroup(*[arr(factors[i].get_bottom(),factors[i+1].get_top(),YELLOW) for i in range(2)])
    menu=VGroup(*[Rectangle(width=w,height=.5,color=PURPLE,fill_color=PURPLE,fill_opacity=.25).move_to([2.8,.8-i*.8,0]) for i,w in enumerate([3.6,3.6,3.6])])
    if shrunk:
        for m,f in zip(menu,[1,.7,.4]): m.stretch(f,0)
    neurons=VGroup(nd(ORANGE,2.1,-2.1,.3),nd(BLUE,3.25,-2.1,.3))
    feedback=VMobject(color=TEXT,stroke_width=3).set_points_as_corners([[3.7,-2.1,0],[5.6,-2.1,0],[5.6,.8,0],[4.8,.8,0]])
    feedback=VGroup(feedback,arr([5.3,.8,0],[4.5,.8,0],TEXT))
    caption=label('feedback from\nneurons already made',3,-3.1,size=30)
    return VGroup(headers,factors,links,menu,neurons,feedback,caption)

class S00Title(TitleCard):
    TITLE='What a Birthday Leaves Behind'
    LESSON=LESSON
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.3,TEAL),label('Birth Order and Fate:\nTemporal Identity and the Inside-Out Cortex',0,.9,GREY,30))
        self.play(FadeIn(label(self.TITLE,0,-.9,size=42)),Create(Line([-1.5,-1.65,0],[1.5,-1.65,0],color=GOLD)),run_time=.7)
        self.finish()

class S01Q(SpokenScene):
    def construct(self):
        c=column();record=VGroup(calendar(2.6,.1,1.65),label('A layer records\na birthday',2.6,2.6,size=34));self.add(c,record)
        prompt=label('What else does\na birthday\nleave behind?',2.6,.8,YELLOW,40)
        self.at("A neuron's layer");self.play(Indicate(c[3],scale_factor=1.05),run_time=.6)
        self.at('What else does');self.play(FadeOut(record),FadeIn(prompt),run_time=.6)
        self.finish()

class S02Markers(SpokenScene):
    def construct(self):
        c=column(False);region=DashedVMobject(box(7.0,5.3,2.95,-.3,GREY),num_dashes=60)
        self.add(c,label('Identity beyond position',2.95,3.3,size=32),region)
        selected=VGroup(c[3][1][1],c[3][2][1],c[3][5][1])
        self.at('identity genes');self.play(*[m.animate.set_color(co).set_fill(co,.9) for m,co in zip(selected,[ORANGE,YELLOW,BLUE])],run_time=.6)
        self.at('serve as markers');self.play(Indicate(selected,scale_factor=1.2),run_time=.5)
        positions=[(3.8,1),(1,-1.5),(4,-1.8)]
        self.at('Markers read identity');self.play(*[m.animate.move_to([x,y,0]).scale(1.5) for m,(x,y) in zip(selected,positions)],c[0].animate.set_stroke(opacity=.4),c[1].animate.set_fill(opacity=.035),*[m.animate.set_opacity(0) for row in c[3] for m in row if m not in list(selected)],run_time=.8)
        self.at('without knowing position');self.play(*[FadeIn(label(s,x,y-.65,co)) for s,(x,y),co in zip(['Tbr1','Ctip2','Satb2'],positions,[ORANGE,YELLOW,BLUE])],run_time=.5)
        self.finish()

class S03Tbr1(SpokenScene):
    def construct(self):
        c=column(False);self.add(c,label('In mouse: Tbr1 level by layer',2.6,3.25,GREY,32))
        ys=[-2.5,-1.5,-.5,.5,1.5,2.5];bx=-1.4
        def bar(y,L,co): return Rectangle(width=L,height=.42,stroke_width=0,fill_color=co,fill_opacity=.9).move_to([bx+L/2,y,0])
        low=VGroup(*[bar(y,.5,GREY) for y in ys]);axis=Line([bx,-2.95,0],[bx,2.95,0],color=GREY,stroke_width=2)
        self.add(axis,low)
        self.at('is high')
        high=[bar(ys[0],3.9,ORANGE),bar(ys[1],3.9,ORANGE)]
        self.play(ReplacementTransform(low[0],high[0]),ReplacementTransform(low[1],high[1]),*[m.animate.set_fill(PINK,.9).set_stroke(ORANGE,5) for m in c[3][0]],*[m.animate.set_color(ORANGE).set_fill(ORANGE,.9) for m in c[3][1]],run_time=.6)
        self.at('subplate and');self.play(FadeIn(label('Tbr1 high:\nsubplate + layer 6',5.0,-2.0,ORANGE,30)),Create(Line([2.75,-2.9,0],[2.75,-1.1,0],color=ORANGE)),run_time=.6)
        self.finish()

class S04Ctip2(SpokenScene):
    def construct(self):
        c=column(False).scale(.87,about_point=[-3.7,0,0]).shift(UP*.45);self.add(c)
        cell=c[3][2][2]
        target=VGroup(box(5.6,1.5,3.4,-2.9,GREY),label('white matter /\nbelow cortex',3.4,-2.9,GREY))
        cortex=VGroup(label('cortex',3.4,2.7,GREY,36),Line([.6,2.2,0],[6.2,2.2,0],color=GREY,stroke_width=2),Line([.6,-2.1,0],[6.2,-2.1,0],color=GREY,stroke_width=2))
        self.add(target,cortex)
        self.at('are high');self.play(c[3][2].animate.set_color(YELLOW).set_fill(YELLOW,.9),run_time=.4)
        self.at('layer five neurons');self.play(FadeIn(label('Ctip2 / Fezf2',1.4,.6,YELLOW,36)),Create(Line(cell.get_right(),[-.2,.4,0],color=YELLOW)),run_time=.4)
        self.at('project below')
        x,y,_=cell.get_center()
        path=VMobject(color=YELLOW,stroke_width=4).set_points_as_corners([[x,y,0],[x+.35,y,0],[x+.35,-3.15,0],[.1,-3.15,0]])
        self.play(Create(path),GrowArrow(arr([-.3,-3.15,0],[.55,-3.15,0],YELLOW)),target[0].animate.set_color(YELLOW),target[1].animate.set_color(YELLOW),run_time=.8)
        self.finish()

class S05Satb2(SpokenScene):
    def construct(self):
        c=column(False);self.add(c)
        hemi=VGroup(Ellipse(width=3.2,height=4.3,color=GREY).move_to([4.4,.5,0]),DashedLine([1.8,-2,0],[1.8,3,0],color=GREY),label('midline',1.8,-2.5,GREY))
        self.add(hemi)
        l5=c[3][2][2];small=nd(BLUE,*l5.get_center()[:2],.10)
        self.at('marks');self.play(c[3][4][2].animate.set_color(BLUE),c[3][5][2].animate.set_color(BLUE),l5.animate.set_color(YELLOW),FadeIn(small),FadeIn(label('Satb2',.1,3.1,BLUE,36)),run_time=.5)
        axons=VGroup(*[arr([-2.5,y,0],[3.6,y,0],BLUE) for y in [2.5,1.5,-.5]])
        self.at('which send axons');self.play(Create(axons),run_time=.7)
        self.at('other hemisphere');self.play(FadeIn(label('other\nhemisphere',4.4,.5)),run_time=.4)
        bracket=VGroup(Line([-1.7,1.1,0],[-1.7,2.9,0],color=BLUE),Line([-1.7,2.9,0],[-1.3,2.9,0],color=BLUE),Line([-1.7,1.1,0],[-1.3,1.1,0],color=BLUE),label('mostly\nupper layers',-.1,.45,BLUE))
        self.at('Most sit');self.play(Create(bracket),run_time=.5)
        self.finish()

class S06Overlap(SpokenScene):
    def construct(self):
        c=column();self.add(c)
        fields=VGroup(*[Circle(radius=1.1,color=co,fill_color=co,fill_opacity=.26,stroke_width=2).move_to([x,1.7,0]) for x,co in [(1.8,ORANGE),(3.2,YELLOW),(4.6,BLUE)]])
        names=VGroup(*[label(sn,x,.3,co,30) for sn,x,co in [('Tbr1',1.3,ORANGE),('Ctip2',3.2,YELLOW),('Satb2',5.1,BLUE)]])
        # Bi-coloured cells in the column: one gene's colour inside another layer's cell.
        l6=c[3][1][2];l5=c[3][2][2]
        in6=nd(YELLOW,*l6.get_center()[:2],.09);in5=nd(BLUE,*l5.get_center()[:2],.09)
        tags=VGroup(label('Tbr1 + Ctip2',.5,-1.5,ORANGE,28),Line([-2.5,-1.5,0],[-.95,-1.5,0],color=ORANGE,stroke_width=2),label('Ctip2 + Satb2',.5,-.5,YELLOW,28),Line([-2.5,-.5,0],[-.95,-.5,0],color=YELLOW,stroke_width=2))
        self.at('Expression overlaps');self.play(FadeIn(fields),FadeIn(names),FadeIn(label('markers overlap',3.2,3.3,size=36)),FadeIn(in6),FadeIn(in5),FadeIn(tags),run_time=.7)
        self.at('position alone');self.play(FadeIn(label('Position does not\ndefine a class',3.9,-2.5,size=34)),run_time=.6)
        self.finish()

class S07Excit(SpokenScene):
    def construct(self):
        c=column();self.add(c,label('The cortical schedule\nso far',2.9,2.7,GREY,36))
        p=nd(PURPLE,-3.7,-3.35,.28)
        neuron=VGroup(nd(BLUE,2.6,.1,.55),label('excitatory neuron',2.6,1.0,BLUE,32))
        self.at('excitatory neurons');self.play(Indicate(c[3],scale_factor=1.05),FadeIn(neuron),run_time=.6)
        self.at('made by');self.play(FadeIn(p),FadeIn(label('dorsal progenitor',2,-2.6,PURPLE,34)),Create(arr([-.2,-2.6,0],[-3.25,-3.25,0],PURPLE)),Create(arr([-3.7,-3,0],[-3.7,-1.8,0],PURPLE)),run_time=.6)
        self.at('They release');self.play(FadeIn(chip('glutamate',BLUE,36).move_to([5.3,.1,0])),GrowArrow(arr([3.25,.1,0],[4.05,.1,0],BLUE)),run_time=.5)
        self.finish()

class S08Ge(SpokenScene):
    def construct(self):
        f=forebrain();a=anatomy_labels();self.add(f[:3],f[4],a[0],a[2],label('interneurons\nGABA',3.9,.2,GABA,36),Line([2.2,-.1,0],[.1,-1,0],color=GABA))
        self.at('In rodents');self.play(FadeIn(label('Rodent forebrain',3.9,2.3,GREY)),run_time=.4)
        self.at('ganglionic eminences');self.play(FadeIn(f[3]),FadeIn(a[1]),run_time=.6)
        self.finish()

class S09Travel(SpokenScene):
    def construct(self):
        f=forebrain();self.add(f,anatomy_labels(),label('Most cortical\nneurons · rodents',3.9,3,GREY),label('interneurons · GABA',3.8,-2.7,GABA))
        paths=[VMobject().set_points_smoothly([[-3.55,-1,0],[-5.05,-.1,0],[-4.9,1.5,0],[-3.5,2.45,0]]),VMobject().set_points_smoothly([[-.45,-1,0],[1.05,-.1,0],[.9,1.5,0],[-.5,2.45,0]])]
        self.at('They travel up');self.play(*[MoveAlongPath(c,p) for c,p in zip(f[4],paths)],*[Create(p.copy().set_stroke(GABA,2,.5)) for p in paths],run_time=1.3)
        self.at('a dorsal birthplace');self.play(FadeIn(label('dorsal goes with\nexcitatory (glutamate)',3.9,1.35,BLUE)),run_time=.5)
        self.at('a ventral');self.play(FadeIn(label('ventral goes with\ninhibitory (GABA)',3.9,-.65,GABA)),run_time=.5)
        self.finish()

class S10Mge(SpokenScene):
    def construct(self):
        f=forebrain().scale(.7).move_to([-3.75,.4,0]);self.add(f[:4],label('MGE interneurons',-3.5,3.1,GABA,36))
        ys=[-2,-1.2,-.4,.4,1.2,2]
        wall=VGroup(Rectangle(width=1.5,height=4.9,color=GREY).move_to([1.9,0,0]),*[Rectangle(width=1.45,height=.74,stroke_width=0,fill_color=co,fill_opacity=.12).move_to([1.9,y,0]) for co,y in zip([PINK,ORANGE,YELLOW,GREY,BLUE,BLUE],ys)])
        self.add(wall,label('cortical wall',1.9,3.1),label('medial ganglionic\neminence (MGE)',-3.7,-2.45,GABA))
        origin=f[3][1].get_center();source=nd(GABA,*origin[:2],.2);self.add(source)
        self.at('medial ganglionic eminence');self.play(Indicate(f[3][1],color=GABA),run_time=.6)
        early=source.copy().set_stroke(ORANGE,5);late=source.copy().set_stroke(BLUE,5)
        p1=ArcBetweenPoints(origin,[1.9,-1.2,0],angle=-.5,color=GABA);p2=ArcBetweenPoints(origin,[1.9,2,0],angle=-.5,color=GABA)
        self.at('follow a similar');self.add(early);self.play(Create(p1),MoveAlongPath(early,p1),run_time=.9)
        self.play(FadeIn(label('born earlier:\ndeep',4.6,-1.2,ORANGE)),Create(Line([2.2,-1.2,0],[3.15,-1.2,0],color=ORANGE)),run_time=.3)
        self.at('settling inside out');self.add(late);self.play(Create(p2),MoveAlongPath(late,p2),FadeIn(label('born later:\nupper',4.6,2,BLUE)),Create(Line([2.2,2,0],[3.15,2,0],color=BLUE)),run_time=.8)
        self.at('Not every interneuron');self.play(FadeIn(label('not every\ninterneuron\nfollows this',4.6,.4,YELLOW,32)),run_time=.4)
        self.finish()

class S11Open(SpokenScene):
    def construct(self):
        self.add(clock(-3.4,.3,2.2),nd(PURPLE,3.4,.3,2.2),label('fly: temporal\nfactor cascade',-3.4,-2.85,YELLOW,32),label('mouse progenitor',3.4,-2.85,PURPLE,32))
        self.at('question is still open');self.play(FadeIn(head('Does a mouse progenitor run a clock?')),run_time=.5)
        self.at('a mammalian progenitor');self.play(FadeIn(label('?',3.4,.3,YELLOW,110)),run_time=.5)
        self.finish()

class S12Predict(SpokenScene):
    def construct(self):
        g=prediction();self.add(g[1],label('One early progenitor · no cortex',0,2.7,PURPLE,34))
        self.at('Predict');self.play(FadeIn(g[0]),run_time=.3)
        self.at('one early progenitor');self.play(Indicate(g[1][1],color=PURPLE),run_time=.6)
        self.at('Does it still');self.play(FadeIn(g[2]),run_time=.5)
        self.finish()

class S13Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(prediction(),label('One early progenitor · no cortex',0,2.7,PURPLE,34));self.wait(5)

class S14Reveal(SpokenScene):
    def construct(self):
        d=dish();d[0].stretch(.9,1);r=culture_results();self.add(d,r[3],r[4])
        self.at("Sally Temple's laboratory");self.play(Indicate(d[1],color=PURPLE,scale_factor=1.04),run_time=.5)
        self.at('The clones made');self.play(LaggedStart(*[FadeIn(m,shift=LEFT*.4) for m in r[0]],lag_ratio=.15),FadeIn(r[2][0]),run_time=.7)
        self.at('before later markers');self.play(LaggedStart(*[FadeIn(m,shift=RIGHT*.4) for m in r[1]],lag_ratio=.15),FadeIn(r[2][1]),run_time=.7)
        self.finish()

class S15Lineage(SpokenScene):
    def construct(self):
        r=culture_results();d=dish();d[0].stretch(.9,1);self.add(d,r)
        self.at('a schedule within');self.play(FadeOut(r[4]),FadeIn(head('A schedule within the lineage')),FadeIn(calendar(0,1.45,.6)),run_time=.5)
        self.finish()

class S16Homolog(SpokenScene):
    def construct(self):
        self.add(label('fly temporal factors',-3.6,2.65,YELLOW,34),label('mouse homologs',2.7,2.65,PURPLE,34))
        fly=VGroup(*[chip(s,YELLOW,34).move_to([-3.6,y,0]) for s,y in [('Hunchback',1.2),('Seven-up',-.8)]])
        mouse=VGroup(*[chip(s,PURPLE,34).move_to([2.6,y,0]) for s,y in [('Ikaros',1.2),('COUP-TFs',-.8)]])
        self.add(fly)
        self.at('Relatives of');self.play(FadeIn(mouse),FadeIn(label('homologs',-.4,2,GREY)),*[Create(DoubleArrow(a.get_right()+RIGHT*.08,b.get_left()-RIGHT*.08,buff=.08,color=GREY,tip_length=.15)) for a,b in zip(fly,mouse)],run_time=.6)
        self.at('timing jobs');self.play(Create(Line([4.1,1.8,0],[4.1,-1.5,0],color=PURPLE)),FadeIn(label('timing\njobs',5.15,.2,PURPLE)),run_time=.5)
        self.at('but a full cascade');self.play(FadeIn(label('Full cascade not shown in cortex',0,-2.8,YELLOW,36)),run_time=.6)
        self.finish()

class S17Either(SpokenScene):
    def construct(self):
        g=options();self.add(g[0])
        self.at('It could be a cascade');self.play(FadeIn(g[1]),Create(g[2]),run_time=.6)
        self.at('a gradual change');self.play(FadeIn(g[3]),run_time=.5)
        self.at('in competence');self.play(g[3][1].animate.stretch(.7,0),g[3][2].animate.stretch(.4,0),run_time=.6)
        self.at('feedback from');self.play(FadeIn(g[4]),Create(g[5]),FadeIn(g[6]),run_time=.6)
        self.finish()

class S18Hold(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(options(True));self.wait(2.5)

def state_diagram():
    inputs=VGroup(chip('what it can make\n(competence)',PURPLE,30).move_to([-4,1,0]),chip('cues it reads',TEAL,30).move_to([-4,-1.2,0]))
    p=VGroup(nd(PURPLE,-.8,-.1,.9),label('state',-.8,-.1,size=32),label('progenitor',-.8,-1.6,PURPLE))
    links=VGroup(arr([-2.3,1,0],[-1.55,.4,0],PURPLE),arr([-2.5,-1.2,0],[-1.55,-.5,0],TEAL))
    output=VGroup(label('temporal\nidentity',2.15,-.1,ORANGE,34),arr([.25,-.1,0],[1.05,-.1,0],ORANGE))
    # A physical layer target, with the cell highlighted within it.
    layers=VGroup(*[Rectangle(width=1.4,height=.6,color=GREY,fill_color=co,fill_opacity=.15).move_to([5,y,0]) for y,co in [(1.4,BLUE),(.8,BLUE),(.2,GREY),(-.4,YELLOW),(-1,ORANGE),(-1.6,PINK)]])
    target=VGroup(layers,nd(ORANGE,5,-1,.2),arr([3.25,-.1,0],[4.2,-1,0],ORANGE),label('layer included',4.8,-2.6,ORANGE))
    return VGroup(inputs,p,links,output,target)

class S19Idea(SpokenScene):
    def construct(self):
        d=state_diagram();card=box(12.4,1.65,0,2.65,TEAL)
        sentence=label("The progenitor's state at a birthday sets\nthe neuron's temporal identity, its layer included.",0,2.65,size=32)
        self.add(card,d[1])
        self.at('one idea');self.play(FadeIn(sentence),run_time=.5)
        self.at("The progenitor's state");self.play(FadeIn(d[0]),Create(d[2]),run_time=.6)
        self.at("sets the neuron's");self.play(FadeIn(d[3]),run_time=.6)
        self.at('its layer included');self.play(FadeIn(d[4]),run_time=.5)
        self.finish()

def puzzles():
    cards=VGroup(*[box(3.95,5.8,x,0) for x in [-4.2,0,4.2]])
    titles=VGroup(*[label(s,x,2.3,size=32) for s,x in zip(['When?','What sets fate?','How many?'],[-4.2,0,4.2])])
    third=VGroup(label('cycling pool',4.2,1,GREY),nd(PURPLE,3.6,-.2,.3),nd(PURPLE,4.8,-.2,.3),label('daughters leave\nor keep cycling',4.2,-1.7,GREY))
    return VGroup(cards,titles,third)

def pulse():
    return VGroup(label('thymidine pulse',-4.2,1.25,TEAL),Line([-5.7,.2,0],[-2.7,.2,0],color=GREY),Rectangle(width=.4,height=.65,color=TEAL,fill_color=TEAL,fill_opacity=.8).move_to([-4.2,.5,0]),label('✓ birthdays',-4.2,-1.2,TEAL,34))

def graft():
    layers=VGroup(*[Rectangle(width=1.4,height=.25,stroke_width=0,fill_color=co,fill_opacity=.25).move_to([.8,1.13-i*.25,0]) for i,co in enumerate([BLUE,GREY,YELLOW,ORANGE])])
    host=VGroup(Rectangle(width=1.4,height=1.0,color=GREY,stroke_width=2).move_to([.8,.75,0]),layers)
    return VGroup(label('ferret graft',0,1.65,PURPLE,32),nd(PURPLE,-1.3,.75,.25),label('donor',-1.3,.1,PURPLE,26),arr([-.95,.75,0],[-.05,.75,0],PURPLE),host,nd(PURPLE,.8,.45,.17),label('host cortex',.8,.1,GREY,26))

def graft_claims():
    return VGroup(*[label(s,0,y,PURPLE) for s,y in [('✓ set late',-.85),('✓ cues included',-1.6),('✓ menu shortens',-2.35)]])

class S20Sum1(SpokenScene):
    def construct(self):
        p=puzzles();self.add(p)
        self.at('The pulse dated');self.play(FadeIn(pulse()),run_time=.5)
        self.at('showed laminar fate');self.play(FadeIn(graft()),run_time=.5)
        claims=graft_claims()
        self.at('set late');self.play(FadeIn(claims[0]),run_time=.3)
        self.at('cues included');self.play(FadeIn(claims[1]),run_time=.3)
        self.at('the menu shortens');self.play(FadeIn(claims[2]),run_time=.3)
        self.finish()

def mini_q():
    ax=Axes(x_range=[1,11,5],y_range=[0,1,.5],x_length=2.5,y_length=1.5,axis_config={'include_tip':False,'include_ticks':False,'color':GREY}).move_to([4.2,.3,0])
    line=VMobject(color=TEXT,stroke_width=3).set_points_as_corners([ax.c2p(i+1,q) for i,q in enumerate(Q_VALUES)])
    return VGroup(ax,line,label('✓ leaving fraction Q',4.2,-1.2,TEAL,30))

def q_chart():
    # Piecewise monotone cubic interpolation of the specified preset; no fitted data.
    from scipy.interpolate import PchipInterpolator
    ax=Axes(x_range=[1,11,1],y_range=[0,1,.5],x_length=10.3,y_length=4.6,axis_config={'color':GREY,'include_tip':False,'include_ticks':False}).move_to([.35,-.1,0])
    f=PchipInterpolator(np.arange(1,12),Q_VALUES)
    curve=ax.plot(lambda x:float(f(x)),x_range=[1,11,.025],color=TEXT,stroke_width=4,use_smoothing=False)
    ticks=VGroup(*[label(str(q),-5.25,ax.c2p(1,q)[1],YELLOW if q==.5 else GREY) for q in [0,.5,1]],*[label(str(i),ax.c2p(i,0)[0],-2.75,GREY) for i in [1,4,8,11]])
    threshold=DashedLine(ax.c2p(1,.5),ax.c2p(11,.5),color=YELLOW,stroke_width=2)
    dot=Dot(ax.c2p(8,.5),radius=.09,color=YELLOW)
    crossing=VGroup(label('Q = 0.5, cycle 8:\npool stops growing',3.15,-1.6,YELLOW),Line(ax.c2p(8,.5)+DOWN*.12,[2.6,-1.05,0],color=YELLOW))
    texts=VGroup(label('Q = fraction of daughters that leave the cycle',0,3.4,size=32),label('Q below 0.5: pool grows',-2.7,2.65,PURPLE),label('Q above 0.5: pool shrinks',2.9,2.65,ORANGE),label('cell cycle 1 to 11 (about E11 to E17)',0,-3.25),label('sketch, not a fitted curve',0,1.65,GREY,30))
    return VGroup(ax,curve,ticks,threshold,dot,crossing,texts)

class S21Sum2(SpokenScene):
    def construct(self):
        p=puzzles();g=graft();claims=graft_claims();base=VGroup(p,pulse(),g,claims);self.add(base)
        fly=VGroup(clock(0,.6,.65),label('fly: a temporal state\nis a factor cascade',0,-1.3,YELLOW))
        self.at('The fly showed');self.play(FadeOut(g),FadeOut(claims),FadeIn(fly),run_time=.45)
        mini=mini_q()
        self.at('And Q counted');self.play(FadeOut(p[2]),FadeIn(mini),run_time=.3)
        self.at('then spent');self.play(FadeOut(base),FadeOut(fly),FadeOut(mini),FadeIn(q_chart()),run_time=.55)
        self.finish()
        # Allow the fully defined chart to be read before the takeaway.
        self.wait(2)

class S22Take(SpokenScene):
    def construct(self):
        self.add(box(12.4,1.2,0,2.85,TEAL),label('A birthday is a timestamp.',0,2.85,TEAL,40))
        d=state_diagram();self.add(d[1],d[4][0])
        self.at('What the progenitor');self.play(Indicate(d[1][0],color=PURPLE),run_time=.3)
        self.at('can make then');self.play(FadeIn(d[0][0]),GrowArrow(d[2][0]),run_time=.4)
        self.at('the cues it reads');self.play(FadeIn(d[0][1]),GrowArrow(d[2][1]),run_time=.4)
        self.at('temporal identity');self.play(FadeIn(d[3]),FadeIn(d[4][1:]),run_time=.5)
        self.finish()

class S23End(EndCard):
    LINE='A birthday is a timestamp.'
    def construct(self):
        self.add(label(self.LINE,0,.5,TEAL,40),label('biochemistrypedia.com',0,-.7,TEAL,30));self.finish()
