"""Following One Glomerulus: qualitative schematics, never measured spatial data.

COLOR MAP (reference scenes.old.py): BLUE = sister cell 1; YELLOW = sister
cell 2; TEAL = glomeruli / cortical activity; GREEN = mean rate / learned
meaning / reward; ORANGE = timing / aversion; PURPLE = inhibition;
GOLD = tracer / experimental light; GREY = structure; RED = rejection.
All tissue strokes, routing paths and chemical coordinates are explicitly
schematic. No quantitative traces or molecular structures are drawn.
"""
import numpy as np
from bp_style import *

LIGHT = '#D1D6DF'
POSITIONS = [(-1.8,.75),(-.7,1.0),(.5,.65),(1.7,1.0),
             (-1.5,-.65),(-.25,-.3),(.8,-.9),(1.8,-.3)]
ACTIVE = (0,3,5,6)


def heading(text):
    return T(text,34).move_to([0,3.12,0])


def strike(mob):
    return Line(mob.get_left()+.06*RIGHT, mob.get_right()-.06*RIGHT,
                color=RED,stroke_width=5)


def glom(p=(0,1.65,0), radius=.42):
    return Circle(radius=radius,color=TEAL,stroke_width=3,
                  fill_color=GOLD,fill_opacity=.7).move_to(p)


def tag(text, p):
    label=T(text,26,LIGHT).move_to(p)
    label.add_background_rectangle(color=BG,opacity=1,buff=.06)
    return label.set_z_index(10)


def targets():
    panels=VGroup(*[RoundedRectangle(width=5.5,height=4.6,corner_radius=.18,
                    color=GREY,stroke_width=2.5).move_to([x,-.35,0]) for x in (-3.15,3.15)])
    labels=VGroup(T('piriform cortex',32,LIGHT).move_to([-3.15,2.35,0]),
                  T('cortical amygdala',32,LIGHT).move_to([3.15,2.35,0]))
    return panels,labels


def tracer():
    marker=glom((-3,3.25,0),.26)
    label=T('one glomerulus (tracer)',30,GOLD).move_to([.35,3.25,0])
    # Routes run around the tissue labels, not through their letters.
    routes=VGroup()
    for x in (-5.55,5.55):
        route=VMobject(color=GOLD,stroke_width=1.6)
        route.set_points_as_corners([[-3,2.98,0],[-3,2.83,0],[x,2.83,0],[x,1.95,0]])
        routes.add(route)
    return VGroup(routes,marker,label)


def axons(x, patchy=False):
    """Seeded curved axon segments: same mark style, different spatial arrangement.

    These are illustrative tissue drawings, not sampled biological counts.
    The diffuse arrangement is stratified across the entire tissue; cluster
    coordinates show qualitative patchiness only. Nothing is a fitted trace.
    """
    rng=np.random.default_rng(29 if patchy else 17)
    routes=VGroup()
    if not patchy:
        points=[(a+rng.uniform(-.15,.15), b+rng.uniform(-.15,.15))
                for a in np.linspace(-2.1,2.1,7)
                for b in np.linspace(-1.95,1.15,6)]
    else:
        points=[]
        for cx,cy in ((-1.3,.65),(1.28,.55),(0,-1.3)):
            outline=DashedVMobject(Ellipse(width=2.18,height=1.65,
                color=GOLD,stroke_width=1.4).move_to([x+cx,cy,0]),num_dashes=22).set_opacity(.55)
            routes.add(outline)
            for _ in range(25):
                angle=rng.uniform(0,TAU); radius=np.sqrt(rng.uniform(0,.82))
                points.append((cx+.95*radius*np.cos(angle),cy+.66*radius*np.sin(angle)))
    for i,(a,b) in enumerate(points):
        angle=rng.uniform(0,TAU)
        length=rng.uniform(.35,.58) if patchy else rng.uniform(.72,.98)
        direction=np.array([np.cos(angle),np.sin(angle),0])
        normal=np.array([-np.sin(angle),np.cos(angle),0])
        center=np.array([x+a,b,0])
        bend=rng.uniform(-.16,.16)*normal
        start,end=center-direction*length/2,center+direction*length/2
        segment=CubicBezier(start,center-direction*length*.15+bend,
                            center+direction*length*.15+bend,end,
                            color=GOLD,stroke_width=2.3)
        routes.add(segment)
        if i % 7 == 0:
            branch_start=segment.point_from_proportion(.55)
            branch_end=branch_start+direction*length*.32+normal*length*.25
            routes.add(CubicBezier(branch_start,branch_start+direction*length*.12,
                branch_end-direction*length*.1,branch_end,color=GOLD,stroke_width=2.3))
    return routes


def panel_tags():
    return VGroup(*[tag('schematic',[x+1.65,-2.38,0]) for x in (-3.15,3.15)])


def rule_labels():
    return VGroup(T('diffuse (scatter)',30,GOLD).move_to([-3.15,-2.92,0]),
                  T('patches',30,GOLD).move_to([3.15,-2.92,0]))


def comparison(scene, both=True, rules=False):
    panels,labels=targets()
    diffuse,patches=axons(-3.15),axons(3.15,True)
    scene.add(panels,labels,tracer(),diffuse,panel_tags())
    if both: scene.add(patches)
    if rules: scene.add(rule_labels())
    return panels,labels,diffuse,patches


def prediction():
    panels,labels=targets()
    unknowns=VGroup(*[T('?',94,GOLD).move_to([x,-.4,0]) for x in (-3.15,3.15)])
    question=T('Patches or diffuse spread?',34).move_to([0,-3.0,0])
    return VGroup(panels,labels,tracer(),unknowns,question)


def field(active=False):
    border=RoundedRectangle(width=10.5,height=4.3,corner_radius=.2,color=GREY).move_to([0,.05,0])
    cells=VGroup(*[Dot([a*2.3,b*1.65,0],radius=.22,
                   color=TEAL if active and i in ACTIVE else GREY,
                   fill_opacity=1 if active and i in ACTIVE else .55) for i,(a,b) in enumerate(POSITIONS)])
    title=T('piriform cortex',32,LIGHT).move_to([0,2.6,0])
    label=T('neurons',30,LIGHT).move_to([-3.7,-2.55,0])
    leader=Line([-3.7,-2.28,0],[-3.45,-1.36,0],color=LIGHT,stroke_width=1.5)
    return VGroup(border,cells,title,label,leader,tag('schematic',[4.1,-1.8,0]))


def receptive():
    cell=Circle(radius=.9,color=TEAL,fill_color=TEAL,fill_opacity=.35).move_to([-2.65,0,0])
    ring=Circle(radius=1.06,color=TEAL).move_to(cell)
    name=T('one piriform neuron',30,LIGHT).move_to([-2.8,-1.65,0])
    rows=VGroup(*[chip('odour '+c,LIGHT,32).move_to([1.55,1.8-i*1.2,0]) for i,c in enumerate('ABCD')])
    ticks=VGroup(*[T('✓',34,TEAL).move_to([3.05,1.8-i*1.2,0]) for i in (0,2,3)])
    # Each response reaches a distinct point on the outer ring.
    landings=[cell.get_center()+1.09*np.array([np.cos(a),np.sin(a),0])
              for a in (PI/4,0,-PI/4)]
    arrows=VGroup(*[Arrow(rows[i].get_left()+.08*LEFT,landing,
                   color=TEAL,buff=0,stroke_width=2.6)
                   for i,landing in zip((0,2,3),landings)])
    return VGroup(cell,ring,name),rows,ticks,arrows


def single_tissue():
    panel=RoundedRectangle(width=11.5,height=4.8,color=GREY).move_to([0,-.15,0])
    routes=axons(0).stretch(1.95,0).move_to([0,-.15,0])
    return VGroup(panel,routes,tag('schematic',[4.55,-2.2,0]))


class S00Title(TitleCard):
    TITLE='Following One Glomerulus'
    LESSON='From Glomeruli to Piriform Cortex'

    def construct(self):
        title=fit(T(self.TITLE,54,font=TITLE_FONT),max_w=11.5)
        lesson=T(self.LESSON,30,LIGHT).move_to([0,1.05,0])
        brand=T('BIOCHEMISTRYPEDIA',30,TEAL).move_to([0,2.15,0])
        rule=Line([-1.5,-.85,0],[1.5,-.85,0],color=GOLD,stroke_width=4)
        self.add(brand,lesson)
        self.play(FadeIn(title),Create(rule),run_time=.45)
        self.wait(3.55)


class S01Question(SpokenScene):
    def construct(self):
        g=glom((0,1.9,0),.9)
        box=RoundedRectangle(width=10.5,height=2.5,color=GREY).move_to([0,-1.85,0])
        q=T('?',110,GOLD).move_to([0,.2,0])
        self.add(g,box,q,T('olfactory bulb',32,LIGHT).move_to([-3,1.9,0]),
                 T('piriform cortex',34,LIGHT).move_to([0,-2.25,0]))
        self.at('where would')
        self.play(Indicate(g,color=GOLD,scale_factor=1.08),run_time=.65)
        self.finish()


class S02Logic(SpokenScene):
    def construct(self):
        inputs=VGroup(*[glom((x,1.15,0),.57).set_fill(TEAL,.2) for x in (-3,0,3)])
        names=VGroup(*[T('input '+c,30,LIGHT).move_to([x,2.05,0]) for x,c in zip((-3,0,3),'ABC')])
        box=RoundedRectangle(width=10.8,height=3.0,color=GREY).move_to([0,-1.25,0])
        patches=VGroup(*[Rectangle(width=2.1,height=1.8,color=TEAL,fill_opacity=.1,fill_color=TEAL).move_to([x,-1.25,0]) for x in (-3,0,3)])
        arrows=VGroup(*[Arrow([x,.5,0],[x,-.3,0],color=TEAL,buff=.08) for x in (-3,0,3)])
        self.add(inputs,names,box,heading('If the bulb’s map were kept…').shift(UP*.38),
                 T('piriform cortex',32,LIGHT).move_to([0,-3.12,0]),
                 T('olfactory bulb',30,LIGHT).move_to([-3.57,2.7,0],aligned_edge=LEFT))
        self.at('topographic map')
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a),FadeIn(p)) for a,p in zip(arrows,patches)],lag_ratio=.15),run_time=.8)
        self.at('Then one')
        dashed=DashedVMobject(patches[1].copy().set_color(GOLD),num_dashes=20)
        self.play(inputs[1].animate.set_fill(GOLD,.7),FadeOut(patches[1]),Create(dashed),run_time=.45)
        self.at('one patch')
        self.play(Indicate(dashed,color=GOLD,scale_factor=1.05),run_time=.5)
        self.finish()


class S03Sosulski(SpokenScene):
    def construct(self):
        row=VGroup(*[glom((x,-.4,0),.82).set_fill(TEAL,.15) for x in (-4,-2,0,2,4)])
        # A tapered hollow tube with a gold-filled reservoir and narrow tip.
        pip=VGroup(Polygon([1.0,2.55,0],[1.42,2.3,0],[.08,.43,0],[-.03,.48,0],
                           color=LIGHT,fill_color=GREY,fill_opacity=.18,stroke_width=2.5),
                   Line([1.1,2.32,0],[.43,1.32,0],color=GOLD,stroke_width=7))
        self.add(row,heading('Sosulski and colleagues, 2011'),
                 T('olfactory bulb',34,LIGHT).move_to([0,-1.85,0]),
                 T('single glomerulus • adult mouse',30,LIGHT).move_to([0,-3,0]))
        self.at('They put')
        self.play(FadeIn(pip),run_time=.4)
        self.at('tracer into')
        drop=Dot([.04,.43,0],radius=.13,color=GOLD)
        self.add(drop)
        self.play(drop.animate.move_to(row[2]),row[2].animate.set_fill(GOLD,.75),run_time=.5)
        self.play(FadeOut(drop),pip.animate.shift(UP*.4+RIGHT*.3).set_opacity(0),run_time=.35)
        self.finish()


class S04FiveDays(SpokenScene):
    def construct(self):
        self.add(heading('Follow the tracer over five days'))
        line=Line([-4.8,.2,0],[4.8,.2,0],color=GREY,stroke_width=3)
        ticks=VGroup(*[VGroup(Line([x,-.05,0],[x,.45,0],color=GREY),
                     T(str(i+1),38,LIGHT).move_to([x,-.6,0])) for i,x in enumerate(np.linspace(-4.8,4.8,5))])
        self.add(line,ticks,T('days after tracer injection',32,LIGHT).move_to([0,1.6,0]))
        self.at('Five days later')
        self.play(LaggedStart(*[t.animate.set_color(GOLD) for t in ticks],lag_ratio=.35),run_time=.9)
        self.at('they imaged')
        self.play(FadeIn(chip('image labelled axons',GOLD,34).move_to([0,-2.2,0])),run_time=.4)
        self.finish()


class S05TwoTargets(SpokenScene):
    def construct(self):
        p,l=targets(); self.add(p,tracer())
        self.at('two targets')
        self.play(Indicate(p,color=GOLD,scale_factor=1.01),run_time=.4)
        self.at('piriform cortex')
        self.play(FadeIn(l[0]),p[0].animate.set_stroke(LIGHT,3),run_time=.35)
        self.at('cortical amygdala')
        self.play(FadeIn(l[1]),p[1].animate.set_stroke(LIGHT,3),run_time=.35)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        p,l=targets(); self.add(p,l,tracer())
        self.at('Pause and predict')
        q=T('Pause and predict',34).move_to([0,-3,0])
        self.play(FadeIn(q),run_time=.35)
        self.at('will the axons')
        self.play(FadeIn(T('?',94,GOLD).move_to([-3.15,-.4,0])),
                  Transform(q,T('Patches or diffuse spread?',34).move_to([0,-3,0])),run_time=.45)
        self.at('Must both targets')
        self.play(FadeIn(T('?',94,GOLD).move_to([3.15,-.4,0])),run_time=.35)
        self.finish()


class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(prediction())
        cue=T('Do both targets agree?  •  Pause the video',30,LIGHT).move_to([0,-3.58,0])
        self.add(cue)
        progress=Line([-5.8,-3.78,0],[-5.8+.01,-3.78,0],color=GOLD,stroke_width=3)
        self.add(progress)
        self.play(progress.animate.put_start_and_end_on([-5.8,-3.78,0],[5.8,-3.78,0]),run_time=9,rate_func=linear)


class S08Piriform(SpokenScene):
    def construct(self):
        p,l=targets(); self.add(p,l,tracer(),panel_tags())
        self.at('the axons')
        self.play(Create(axons(-3.15)),run_time=.5)
        self.at('spread diffusely')
        self.play(FadeIn(rule_labels()[0]),run_time=.35)
        self.at('no apparent')
        self.play(Indicate(p[0],color=GOLD,scale_factor=1.01),run_time=.5)
        self.finish()


class S09Amygdala(SpokenScene):
    def construct(self):
        p,l,d,a=comparison(self,False); self.add(rule_labels()[0])
        self.at('same glomerulus')
        self.play(Indicate(self.mobjects[2][1],color=GOLD,scale_factor=1.15),run_time=.35)
        self.at('gave stereotyped')
        self.play(Create(a),FadeIn(rule_labels()[1]),run_time=.75)
        self.finish()


class S10TwoRules(SpokenScene):
    def construct(self):
        p,l,d,a=comparison(self,rules=True)
        self.at('One tracer')
        self.play(Indicate(self.mobjects[2][1],color=GOLD,scale_factor=1.15),run_time=.35)
        self.at('two different rules')
        self.play(Indicate(p[0],color=GOLD,scale_factor=1.02),run_time=.55)
        self.play(Indicate(p[1],color=GOLD,scale_factor=1.02),run_time=.55)
        self.finish()


class S11NotSingleRandom(SpokenScene):
    def construct(self):
        p,l,d,a=comparison(self)
        proposed=T('random everywhere?',34,LIGHT).move_to([0,-3.08,0])
        self.at('at random everywhere')
        self.play(FadeIn(proposed),run_time=.35)
        self.at('The cortical amygdala')
        self.play(p[1].animate.set_stroke(GOLD,4),run_time=.35)
        self.at('shows it does not')
        self.play(Create(strike(proposed)),run_time=.5)
        self.finish()


class S12OneTarget(SpokenScene):
    def construct(self):
        p,l,d,a=comparison(self)
        title=T('Scatter belongs to one target',28).move_to([0,-3.6,0])
        self.at('scatter is not')
        self.play(FadeIn(title),run_time=.35)
        labels=rule_labels()
        self.at('It was seen')
        self.play(FadeIn(labels[0]),p[0].animate.set_stroke(GOLD,3),run_time=.35)
        self.at('not in the')
        self.play(FadeIn(labels[1]),p[1].animate.set_stroke(GOLD,3),run_time=.35)
        self.finish()


class S13WhyBoth(SpokenScene):
    def construct(self):
        self.add(single_tissue(),heading('tracer image: piriform cortex'))
        self.at('where axons go')
        self.play(Indicate(self.mobjects[0][1],color=GOLD,scale_factor=1.01),run_time=.45)
        self.at('does not show')
        self.play(FadeIn(chip('axon paths are not synapses',LIGHT,34).move_to([0,-3.12,0])),run_time=.45)
        self.finish()


class S14Stettler(SpokenScene):
    def construct(self):
        f=field(); self.add(f,T('Stettler and Axel, 2009',32,LIGHT).move_to([0,3.32,0]),
              T('imaging field, living mouse',30,LIGHT).move_to([0,-3.15,0]))
        self.at('imaged odor responses')
        puff=chip('odour',TEAL,30).move_to([3.4,-2.6,0])
        self.play(FadeIn(puff),run_time=.35)
        self.play(*[f[1][i].animate.set_color(TEAL).set_opacity(.85) for i in ACTIVE],run_time=.7)
        self.play(*[f[1][i].animate.set_color(GREY).set_opacity(.55) for i in ACTIVE],run_time=.7)
        self.finish()


class S15Dispersed(SpokenScene):
    def construct(self):
        f=field(); self.add(f,T('imaging field, living mouse',30,LIGHT).move_to([0,3.32,0]))
        puff=chip('odour',TEAL,30).move_to([3.4,-2.6,0])
        self.at('An odor')
        self.play(FadeIn(puff),run_time=.3)
        self.at('activated a dispersed')
        self.play(*[f[1][i].animate.set_color(TEAL).set_opacity(1) for i in ACTIVE],run_time=.55)
        self.at('scattered across')
        self.play(FadeIn(T('dispersed ensemble',34,TEAL).move_to([0,-3.3,0])),run_time=.4)
        self.finish()


class S16RfDef(SpokenScene):
    def construct(self):
        cell,rows,ticks,arrows=receptive(); self.add(cell,rows)
        self.at('receptive field')
        self.play(FadeIn(heading('Receptive field')),run_time=.35)
        self.at('that excite it')
        self.play(FadeIn(ticks),*[GrowArrow(a) for a in arrows],cell[0].animate.set_fill(TEAL,.8),run_time=.45)
        self.finish()


class S17RfScatter(SpokenScene):
    def construct(self):
        cell,rows,ticks,arrows=receptive(); self.add(cell,rows,ticks,arrows,heading('Receptive field'))
        self.at('chemically dissimilar')
        rings=VGroup(*[SurroundingRectangle(rows[i],color=GOLD,buff=.10,corner_radius=.16) for i in (0,2,3)])
        self.play(Create(rings),run_time=.55)
        self.play(FadeIn(T('unrelated chemistry, illustrative',32,LIGHT).move_to([0,-3.1,0])),run_time=.4)
        self.finish()


class S18RfDiscont(SpokenScene):
    def construct(self):
        # Axes and positions are qualitative illustrations, with no numerical data.
        axes=VGroup(Arrow([-5.2,-2.25,0],[5.3,-2.25,0],buff=0,color=GREY,stroke_width=2),
                    Arrow([-5.2,-2.25,0],[-5.2,2.25,0],buff=0,color=GREY,stroke_width=2))
        pts=[(-3.8,1.25),(0,-1.25),(3.8,1.1)]
        dots=VGroup(*[Dot([x,y,0],radius=.16,color=TEAL) for x,y in pts])
        labels=VGroup(*[T('odour '+c,30,TEAL).move_to([x,y+(.42 if c=='C' else -.43),0]) for c,(x,y) in zip('ACD',pts)])
        neutral=VGroup(*[Dot([x,y,0],radius=.13,color=GREY) for x,y in [(-2,.2),(-.7,.5),(1.2,.2),(2.15,.55),(-3,-1.3),(3,-1.3)]])
        b=T('B',30,LIGHT).move_to([-2,-.25,0])
        self.add(axes,dots,labels,neutral,b,heading('One neuron’s receptive field'),
             T('chemical feature 1',30,LIGHT).move_to([0,-2.7,0]),
             T('chemical feature 2',30,LIGHT).rotate(PI/2).move_to([-5.85,0,0]),
             T('chemical space (schematic)',30,LIGHT).move_to([0,-3.4,0]))
        self.at('discontinuous')
        self.play(*[Flash(d,color=TEAL,flash_radius=.3,line_length=.08) for d in dots],run_time=.6)
        self.finish()


class S19NotNone(SpokenScene):
    def construct(self):
        f=field().shift(UP*.25); self.add(f)
        q=T('?  No chemical information?',30,LIGHT).move_to([2.65,-3.15,0])
        self.at('This does not')
        self.play(FadeIn(q),FadeIn(T('✓  No spatial map',30,TEAL).move_to([-3.6,-3.15,0])),run_time=.45)
        self.finish()


class S20NotRandom(SpokenScene):
    def construct(self):
        tissue=single_tissue()
        diffuse=T('diffuse',38,GOLD).move_to([-1.7,3.1,0])
        random=T('random',38,LIGHT).move_to([1.8,3.1,0])
        self.add(tissue,diffuse,random,T('piriform cortex',32,LIGHT).move_to([0,-3.15,0]))
        self.at('not the same')
        self.play(Create(strike(random)),run_time=.45)
        self.finish()


class S21Chen(SpokenScene):
    def construct(self):
        # Same source neurons collateralize to a common piriform position and
        # matched targets elsewhere. These are explicitly non-topographic routes.
        sources=VGroup(*[Circle(radius=.3,color=TEAL,fill_color=TEAL,fill_opacity=.4).move_to([-4.6,y,0]) for y in (1.35,0,-1.35)])
        pir=RoundedRectangle(width=5.4,height=2.15,color=GREY).move_to([2.9,1.25,0])
        other=RoundedRectangle(width=5.4,height=2.15,color=GREY).move_to([2.9,-1.55,0])
        p_label=T('piriform cortex',32,LIGHT).move_to([2.9,2.05,0])
        o_label=T('matched targets elsewhere',30,LIGHT).move_to([2.9,-2.15,0])
        target=Dot([3.4,.55,0],radius=.14,color=TEAL)
        position=VGroup(T('one anterior–posterior',28,LIGHT),
                        T('position',28,LIGHT)).arrange(DOWN,buff=.08).move_to([2.9,1.25,0])
        target2=Dot([3.4,-1.35,0],radius=.14,color=TEAL)
        routes=VGroup()
        for i,s in enumerate(sources):
            # Separate source stems branch before either target box. The lower
            # collateral stays below piriform's bottom edge (y=.175).
            junction=np.array([-3.35+i*.4,s.get_y(),0])
            upper=VMobject(color=TEAL,stroke_width=2.5)
            upper.set_points_as_corners([junction,[-.45,.46+i*.15,0],target.get_center()])
            lower=VMobject(color=TEAL,stroke_width=2.5)
            lower.set_points_as_corners([junction,[-1.65+i*.32,-.8-i*.3,0],target2.get_center()])
            routes.add(Line(s.get_right(),junction,color=TEAL,stroke_width=2.5),upper,lower)
        self.add(sources,pir,other,p_label,o_label,
                 T('bulb neurons',30,LIGHT).move_to([-4.6,2.4,0]),
                 T('Chen and colleagues, 2022',32,LIGHT).move_to([0,3.35,0]),
                 T('single-neuron barcoding • schematic',30,LIGHT).move_to([0,-3.5,0]))
        self.at('found spatial')
        self.play(Create(routes),FadeIn(target),FadeIn(target2),FadeIn(position),run_time=.75)
        self.at('It was not')
        self.play(FadeIn(T('Routing structure; no map of odour chemistry',30,LIGHT).move_to([0,-2.95,0])),run_time=.4)
        self.finish()


class S22Takeaway(SpokenScene):
    def construct(self):
        p,l,d,a=comparison(self,rules=True)
        self.at('scatter is real')
        self.play(Indicate(p[0],color=GOLD,scale_factor=1.01),run_time=.5)
        self.at('Next comes')
        # Keep both pattern labels; question occupies its own row below.
        self.play(FadeIn(T('How can a scatter keep chemistry?',32,TEAL).move_to([0,-3.58,0])),run_time=.5)
        self.finish()


class S23End(EndCard):
    LINE='The scatter is real, and it belongs to piriform cortex.'

    def construct(self):
        line=fit(T(self.LINE,40,font=TITLE_FONT),max_w=11.5)
        sub=T('biochemistrypedia.com',30,TEAL)
        VGroup(line,sub).arrange(DOWN,buff=.5)
        self.play(FadeIn(line),run_time=.45)
        self.play(FadeIn(sub),run_time=.3)
        self.finish()
