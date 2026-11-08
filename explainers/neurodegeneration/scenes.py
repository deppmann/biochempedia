"""Chapter 1: Three Questions, Three Kinds of Evidence.

COLOR MAP (shared with the other chapters): BLUE = drug; YELLOW = placebo;
GREEN = less worsening/gap; RED = neuronal loss; GREY = schematic anatomy;
TEAL = evidence cards only; TEXT = proteins and variant dots; LIGHT = labels;
neutral grey question marks and grey rings = uncertainty and nearby variants.
Anatomical contours are schematic, not data curves. No quantitative traces.
"""
from bp_style import *

LESSON_TITLE = 'When Mature Neurons Fail: Neurodegeneration'
LIGHT = '#C5CBD5'


def label(s, x, y, size=28, color=TEXT):
    return T(s, size=size, color=color).move_to([x, y, 0])


def heading(s):
    return label(s, 0, 3.45, 32)


def leader(a, b):
    return Line([*a, 0], [*b, 0], color=LIGHT, stroke_width=2)


def brain():
    # One closed lateral silhouette; the midbrain/stem is part of its contour.
    pts = [(-5.9,-.5),(-6.05,.7),(-5.6,1.8),(-4.7,2.5),(-3.4,2.7),
           (-2.1,2.5),(-1.1,1.8),(-.65,.8),(-.9,-.3),(-1.5,-.9),
           (-1.4,-1.55),(-.9,-2.3),(-1.45,-2.55),(-2.05,-1.75),
           (-2.3,-1.1),(-3.2,-1.3),(-4.3,-1.1),(-5.4,-1),(-5.9,-.5)]
    outline = VMobject(color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.12)
    outline.set_points_smoothly([[x,1.1*y+.1,0] for x,y in pts])
    return outline


def glow(x,y,w,h):
    return VGroup(*[Ellipse(width=w*f,height=h*f,stroke_width=0,fill_color=RED,
                          fill_opacity=o).move_to([x,y,0])
                    for f,o in [(1.8,.07),(1.4,.13),(1,.65)]])


def ad_regions():
    return VGroup(glow(-3.5,-.65,.65,.85),glow(-2.7,.3,1.5,.4))


def ad_labels():
    return VGroup(label('entorhinal cortex\nlayer II',3,-.65,28),
                  label('CA1\nhippocampus',3,1.2,28),
                  leader((-3.1,-.65),(.95,-.65)),
                  leader((-1.85,.3),(1.7,1.2)))


def memory_loop():
    return VGroup(CurvedArrow([-3.85,-.3,0],[-2.9,.65,0],angle=-PI/1.5,color=TEXT),
                  CurvedArrow([-2.35,.05,0],[-3.2,-1.05,0],angle=-PI/1.5,color=TEXT))


def neuron(x=0,y=0):
    # A broad soma and short axon keep the neuron legible at teaching-video scale.
    # Total height 5.5 / 8 frame units (69%), with room for headings and captions.
    body = Circle(radius=2.25,color=LIGHT,stroke_width=3,fill_color=GREY,fill_opacity=.1).move_to([x,y+.1,0])
    arms=VGroup(*[Line([x+a,y+b,0],[x+c,y+d,0],color=LIGHT,stroke_width=4)
                  for a,b,c,d in [(-1.5,1.75,-2.5,2.85),(1.5,1.75,2.5,2.85),
                                 (-2.2,.2,-2.6,-.2),(2.2,.2,2.6,-.2),
                                 (-1.5,-1.55,-2.45,-1.9),(-2.45,-1.9,-2.45,-2.65)]])
    return VGroup(body,arms)


def specks(x,y):
    return VGroup(*[RoundedRectangle(width=.2,height=.13,corner_radius=.03,
                    color=TEXT,fill_opacity=.9).rotate(a).move_to([x+dx,y+dy,0])
                    for dx,dy,a in [(-.55,.4,.3),(.4,.55,-.4),(.55,-.35,.6),(-.25,-.35,-.2),(.05,.05,.5)]])


def plaque(x,y):
    return VGroup(*[RoundedRectangle(width=.4,height=.25,corner_radius=.06,
                    color=TEXT,fill_opacity=.65).rotate(a).move_to([x+dx,y+dy,0])
                    for dx,dy,a in [(-.6,.2,.3),(-.2,.5,-.4),(.35,.45,.5),(.6,-.15,-.3),(.05,-.1,.6),(-.35,-.45,-.2),(.3,-.55,.2)]])


def tangle(x,y):
    # Abstract thread bundle; no molecular or ribbon structure.
    return VGroup(*[VMobject(color=TEXT,stroke_width=4).set_points_smoothly(
        [[x-.75,y-.35+i*.17,0],[x-.3,y+.15+i*.12,0],
         [x+.2,y-.2+i*.13,0],[x+.75,y+.15+i*.15,0]]) for i in range(4)])


def evidence_card(question,source,y):
    box=RoundedRectangle(width=6,height=1.35,corner_radius=.16,color=TEAL,
                         fill_color=TEAL,fill_opacity=.08).move_to([3,y,0])
    return VGroup(box,label(question,3,y+.25,28),label(source,3,y-.34,26,LIGHT))


def cards():
    return VGroup(evidence_card('What builds up?','autopsy',1.8),
                  evidence_card('What can start it?','families',.1),
                  evidence_card('Does changing it help?','randomized trials in people',-1.6))


def card_state(card,active=False,dim=False):
    result=card.copy()
    result[0].set_stroke(TEAL,width=6 if active else 2.5,opacity=.55 if dim else 1)
    result[0].set_fill(TEAL,opacity=.24 if active else .04 if dim else .08)
    result[1:].set_opacity(.55 if dim else 1)
    return result


def pedigree():
    pos=[(-4.8,1.6),(-2.1,1.6),(-4.8,-.2),(-2.1,-.2),(-4.8,-2),(-2.1,-2)]
    people=VGroup(); marks=VGroup()
    for i,(x,y) in enumerate(pos):
        affected=i in (0,2,4)
        p=Square(side_length=.8) if i%2==0 else Circle(radius=.4)
        p.set_stroke(LIGHT,3).set_fill(RED if affected else BG,opacity=.65 if affected else 1)
        people.add(p.move_to([x,y,0]))
        if affected:
            marks.add(Dot([x-.12,y,0],radius=.1,color=TEXT))
    links=VGroup(*[leader(a,b) for a,b in [((-4.4,1.6),(-2.5,1.6)),
        ((-3.45,1.6),(-3.45,.7)),((-3.45,.7),(-4.8,.7)),((-4.8,.7),(-4.8,.2)),
        ((-4.4,-.2),(-2.5,-.2)),((-3.45,-.2),(-3.45,-1.1)),
        ((-4.8,-1.1),(-2.1,-1.1)),((-4.8,-1.1),(-4.8,-1.6)),((-2.1,-1.1),(-2.1,-1.6))]])
    legend=label('Filled: affected   •: variant',-3.45,2.65,26,LIGHT)
    return VGroup(links,people,legend),marks


def second_family():
    pos=[(1.05,-.45),(3.15,-.45),(1.05,-2),(3.15,-2)]
    g=VGroup(label('Second family',2.1,.35,28))
    for i,(x,y) in enumerate(pos):
        p=Square(side_length=.8) if i%2==0 else Circle(radius=.4)
        p.set_stroke(LIGHT,3).set_fill(RED if i in (0,2) else BG,opacity=.65 if i in (0,2) else 1)
        g.add(p.move_to([x,y,0]))
        if i in (0,2): g.add(Dot([x,y,0],radius=.1,color=TEXT))
    g.add(leader((1.45,-.45),(2.75,-.45)),leader((2.1,-.45),(2.1,-1.2)),
          leader((1.05,-1.2),(3.15,-1.2)),leader((1.05,-1.2),(1.05,-1.6)),leader((3.15,-1.2),(3.15,-1.6)))
    return g


def puzzle():
    left=neuron(-3,-.1); right=neuron(3,-.1)
    for cell in (left,right):
        for arm in cell[1][:2]:
            end=arm.get_end(); end[1]=2.3; arm.put_start_and_end_on(arm.get_start(),end)
        stub=cell[1][-1]; end=stub.get_end(); end[1]=-2.9
        stub.put_start_and_end_on(stub.get_start(),end)
    titles=VGroup(label('SOD1 family',-3,3.2,30),label('Most ALS: TDP-43 clumps',3,3.2,28))
    titles[0].align_to(left,LEFT)
    q=label('?',-3,.35,82,LIGHT)
    question=label('Will these neurons carry TDP-43 clumps?',0,-3.3,30)
    return VGroup(left,right,titles,q,specks(3,.3),question)


class S00Title(TitleCard):
    LESSON=LESSON_TITLE
    TITLE='Three Questions, Three Kinds of Evidence'
    def construct(self):
        self.add(heading('BIOCHEMISTRYPEDIA'),label('When Mature Neurons Fail:\nNeurodegeneration',0,1.65,28,LIGHT))
        self.play(FadeIn(label('Three Questions,\nThree Kinds of Evidence',0,-.3,48)),run_time=.6)
        self.add(Line([-1.4,-2,0],[1.4,-2,0],color=GOLD))
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        self.add(brain(),label('What causes them?  What might treat them?',0,-3.25,34))
        self.at('Three diseases')
        names=VGroup(label('Alzheimer disease',3.4,.35,30),label('Parkinson disease',3.4,-1.25,30),label('ALS',3.4,2.2,30))
        lines=VGroup(leader((-3.5,-.65),(1.45,.35)),leader((-1.65,-1.05),(1.45,-1.25)),leader((-2.4,2),(2.8,2.2)))
        self.play(LaggedStart(*[FadeIn(VGroup(n,l)) for n,l in zip(names,lines)],lag_ratio=.45),run_time=2.4)
        self.finish()


class S02Ad(SpokenScene):
    def construct(self):
        self.add(brain(),heading('Alzheimer disease'))
        r=ad_regions(); l=ad_labels()
        self.at('early losses include'); self.play(FadeIn(r[0]),run_time=.35)
        self.at('neurons of the'); self.play(FadeIn(l[0]),Create(l[2]),run_time=.35)
        self.at('and'); self.play(FadeIn(r[1]),run_time=.35)
        self.at('in the hippocampus'); self.play(FadeIn(l[1]),Create(l[3]),run_time=.35)
        self.finish()


class S03Memory(SpokenScene):
    def construct(self):
        self.add(brain(),ad_regions(),ad_labels(),heading('Alzheimer disease'))
        self.at('Both belong'); self.play(Create(memory_loop()),run_time=.4)
        self.at('circuit for new')
        self.play(FadeIn(label('Circuit for new declarative memories',0,-3.2,30)),run_time=.25)
        self.finish()


class S04Pd(SpokenScene):
    def construct(self):
        self.add(brain(),heading('Parkinson disease'))
        carry=label('Circuit for new declarative memories',0,-3.2,30); self.add(carry)
        self.wait(1); self.play(FadeOut(carry),run_time=.2)
        nigra=glow(-1.85,-1.12,.65,.45)
        self.at('the defining loss'); self.play(FadeIn(nigra),run_time=.35)
        self.at('dopamine neurons')
        self.play(FadeIn(label('Dopamine neurons',3.3,1.95,30)),Create(leader((-1.65,-.9),(1.3,1.95))),run_time=.35)
        self.at('in the substantia')
        striatum=Ellipse(width=1.3,height=.9,color=LIGHT,fill_color=GREY,fill_opacity=.35).move_to([-3.3,.9,0])
        tract=Arrow([-1.95,-.85,0],[-3.15,.48,0],color=LIGHT,buff=0,stroke_width=6)
        self.play(FadeIn(striatum),GrowArrow(tract),FadeIn(label('Striatum',-4.75,1.2,26)),
                  Create(leader((-4.15,1.2),(-3.95,.95))),
                  FadeIn(label('Substantia nigra\npars compacta',3.3,-.1,28)),
                  Create(leader((-1.5,-1.12),(1.25,-.1))),run_time=.45)
        self.at('in the midbrain')
        self.play(FadeIn(label('Midbrain',3.3,-2.05,26,LIGHT)),Create(leader((-1.6,-1.6),(2.1,-2.05))),run_time=.3)
        self.finish()


class S05Als(SpokenScene):
    def construct(self):
        self.add(heading('ALS'))
        cortex=Ellipse(width=3,height=1.3,color=LIGHT,fill_color=GREY,fill_opacity=.15).move_to([-3,1.8,0])
        cord=Circle(radius=1.25,color=LIGHT,fill_color=GREY,fill_opacity=.1).move_to([-3,-1.55,0])
        butterfly=VMobject(color=GREY,fill_color=GREY,fill_opacity=.45).set_points_smoothly(
            [[-3+x,-1.55+y,0] for x,y in [(-.65,.75),(-.25,.35),(0,.15),(.25,.35),(.65,.75),(.55,.1),(.8,-.6),(.3,-.75),(0,-.25),(-.3,-.75),(-.8,-.6),(-.55,.1),(-.65,.75)]])
        upper=Circle(radius=.2,color=TEXT,fill_opacity=.5).move_to([-3,1.8,0])
        lower=Circle(radius=.2,color=TEXT,fill_opacity=.5).move_to([-3.5,-2.1,0])
        self.add(cortex,cord,butterfly,upper,lower,label('Motor cortex',-3,2.8,26),
                 label('Spinal cord cross-section',-3,-3.15,26))
        self.at('motor neurons die')
        self.play(Transform(upper,DashedVMobject(upper.copy().set_color(RED),num_dashes=10)),
                  Transform(lower,DashedVMobject(lower.copy().set_color(RED),num_dashes=10)),run_time=.5)
        self.at('Upper ones')
        self.play(GrowArrow(Arrow([-3,1.45,0],[-3,-.25,0],buff=0,color=LIGHT)),
                  FadeIn(label('Upper motor neuron',2.2,1.8,28)),Create(leader((-2.75,1.8),(.2,1.8))),run_time=.4)
        self.at('Lower ones')
        self.play(FadeIn(glow(-3.5,-2.1,.6,.45)),FadeIn(label('Lower motor neuron',2.2,-.35,28)),
                  Create(leader((-3.25,-2.1),(.2,-.35))),FadeIn(label('Ventral horn',-5.3,-.6,26)),
                  Create(leader((-5.3,-.85),(-3.8,-1.9))),run_time=.35)
        self.at('send axons')
        self.play(GrowArrow(Arrow([-3.15,-2.1,0],[2.6,-2.1,0],buff=0,color=LIGHT)),run_time=.35)
        self.at('to muscle')
        muscle=RoundedRectangle(width=2.2,height=1.15,corner_radius=.25,color=LIGHT,fill_opacity=.15).move_to([3.9,-2.1,0])
        self.play(FadeIn(muscle),FadeIn(label('Muscle',3.9,-2.1,28)),run_time=.3)
        self.finish()


class S06Clumps(SpokenScene):
    def construct(self):
        self.add(heading('Alzheimer disease'),neuron(-3,-.1))
        single=RoundedRectangle(width=1.8,height=.6,corner_radius=.06,color=TEXT,fill_opacity=.7).move_to([3.2,1.8,0])
        self.add(single)
        self.at('a protein misfolds')
        self.play(Transform(single,Polygon([2.7,1.9,0],[3.1,1.55,0],[3.7,1.9,0],[3.3,2.05,0],color=TEXT,fill_opacity=.7)),run_time=.4)
        cluster=plaque(3.2,.3).scale(1.6)
        self.at('and clumps'); self.play(Transform(single,cluster),run_time=.5)
        self.at('amyloid plaques')
        self.play(FadeIn(label('amyloid-beta plaque\noutside neuron',3.2,2,28)),Create(leader((3.2,1.4),(3.2,1))),run_time=.35)
        self.at('tau tangles')
        self.play(Create(tangle(-3,.4).scale(1.8)),FadeIn(label('tau tangle\ninside neuron',3.2,-1.9,28)),
                  Create(leader((-1.5,.35),(1.4,-1.55))),run_time=.35)
        self.finish()


class S07Clumps2(SpokenScene):
    def construct(self):
        anatomy=VGroup(brain(),glow(-1.85,-1.12,.65,.45))
        title=heading('Parkinson disease'); self.add(anatomy,title)
        n=neuron(0,-.1)
        subtype=label('Substantia nigra neuron',0,-3.25,26,LIGHT)
        self.at('alpha')
        self.play(ReplacementTransform(anatomy,n),
                  Transform(title,label('Parkinson disease',0,3.25,30)),
                  FadeIn(subtype),run_time=.45)
        self.at('is the main protein')
        inclusion=Circle(radius=.7,color=TEXT,fill_opacity=.15).move_to([0,.4,0])
        filaments=VGroup(*[Line([-.5,.1+i*.2,0],[.5,.25+i*.2,0],color=TEXT,stroke_width=4) for i in range(3)])
        self.play(FadeIn(inclusion),Create(filaments),run_time=.35)
        protein_label=label('Lewy body filaments:\nmainly alpha-synuclein',0,-.95,24)
        self.at('filaments of')
        self.play(FadeIn(protein_label),run_time=.35)
        self.at('Mosta LS')  # aligner's joined words for "Most ALS"
        self.play(*[o.animate.shift(LEFT*3) for o in (n,title,subtype,inclusion,filaments,protein_label)],
                  FadeIn(neuron(3,-.1)),FadeIn(label('Most ALS',3,3.25,30)),
                  FadeIn(label('Spinal motor neuron',3,-3.25,26,LIGHT)),run_time=.3)
        self.at('has clumps of')
        self.play(FadeIn(specks(3,.3)),FadeIn(label('TDP-43',3,-1.25,28)),run_time=.35)
        self.finish()


class S08Autopsy(SpokenScene):
    def construct(self):
        n=neuron(-3,-.1); s=specks(-3,.3); card=cards()[0]
        self.add(n,s,heading('Three kinds of evidence'),card)
        self.at('an autopsy tells'); self.play(Indicate(card[0],color=TEAL),run_time=.4)
        self.at('what a clump'); self.play(Indicate(s,color=TEXT,scale_factor=1.2),run_time=.4)
        self.at('It does not')
        self.play(FadeIn(label('Does it kill?',3,-.9,38)),FadeIn(label('?',3,-2.1,70,LIGHT)),run_time=.4)
        self.finish()


class S09Family(SpokenScene):
    def construct(self):
        p,m=pedigree(); self.add(p,heading('Example: a dominant family'))
        note=label('Not every carrier falls ill\nby a given age.',2.9,-1.2,26,LIGHT)
        self.at('A gene variant'); self.play(FadeIn(m[0]),run_time=.3)
        self.at('passes from parent'); self.play(TransformFromCopy(m[0],m[1]),run_time=.4)
        self.at('to child'); self.play(TransformFromCopy(m[1],m[2]),run_time=.3)
        self.at('along with the illness'); self.play(FadeIn(note),run_time=.35)
        self.finish()


class S10Coseg(SpokenScene):
    def construct(self):
        p,m=pedigree(); self.add(p,m,label('Example: a dominant family',-3.4,3.45,26))
        note=label('Not every carrier falls ill\nby a given age.',2.9,-1.2,26,LIGHT); self.add(note)
        self.at('That traveling together'); self.play(Indicate(m,color=TEXT),run_time=.4)
        self.at('is called'); self.play(FadeOut(note),FadeIn(label('Cosegregation',-3.4,-2.85,30)),run_time=.35)
        self.at('strong evidence for')
        self.play(FadeIn(label('evidence for a cause',-3.4,-3.4,26)),FadeIn(cards()[1].shift(UP*2.8)),run_time=.35)
        nearby=VGroup(*[Circle(radius=.13,color=LIGHT,stroke_width=3).move_to(v.get_center()+RIGHT*.3) for v in m])
        self.at('a harmless variant nearby')
        self.play(FadeIn(nearby),FadeIn(label('○: nearby harmless variant',3,1.85,26,LIGHT)),run_time=.35)
        self.at('travel along too')
        caution=label('A nearby variant can travel too',3,1.25,24,LIGHT)
        self.play(FadeIn(caution),run_time=.35)
        self.at('A second family'); self.play(FadeIn(second_family()),run_time=.4)
        self.at('tests of what')
        self.play(FadeIn(chip('What does\nthe variant do?',TEXT,24).move_to([5,-1.2,0])),run_time=.35)
        self.finish()


class S11Question(SpokenScene):
    def construct(self):
        p=puzzle(); p[0].shift(RIGHT*3); p[3].shift(RIGHT*3); p[2][0].shift(RIGHT*3)
        self.add(p[0],p[3])
        self.at("family's ALS"); self.play(FadeIn(p[2][0]),run_time=.3)
        self.at('Most people with'); self.play(*[o.animate.shift(LEFT*3) for o in (p[0],p[3],p[2][0])],
                  FadeIn(p[1]),FadeIn(p[2][1]),FadeIn(p[4]),run_time=.4)
        self.at('Will this'); self.play(FadeIn(p[5]),run_time=.35)
        self.finish()


class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(puzzle())
        # Five dots disappear one per second without changing the comparison.
        dots=VGroup(*[Dot([0,1.5-i*.65,0],radius=.3,color=LIGHT) for i in range(5)])
        self.add(dots)
        for dot in dots:
            self.wait(.8); self.play(FadeOut(dot),run_time=.2)


class S13Reveal(SpokenScene):
    def construct(self):
        p=puzzle(); self.add(p)
        self.at('Now')  # transcript spelling of spoken "No."
        self.play(FadeOut(p[3]),FadeOut(p[5]),run_time=.2)
        self.play(FadeIn(label('No TDP-43 clumps in the SOD1 cases',0,-3.5,30)),run_time=.25)
        self.at('post mortem series')  # split by the aligner
        self.play(FadeIn(label('Postmortem series, 2007',3.3,-2.98,24,LIGHT)),run_time=.25)
        self.at('cases with')
        self.play(FadeIn(T('SOD1 = superoxide dismutase 1',size=22,color=LIGHT).move_to([-3,2.65,0]).align_to(p[2][0],LEFT)),run_time=.3)
        self.at('lacked')
        # Empty cytoplasm is the result; keep the reference specks visible beside it.
        self.play(p[0][0].animate.set_fill(opacity=0),run_time=.4)
        self.at('died anyway',lead=.15)
        dead=VGroup(*[DashedVMobject(part.copy().set_color(RED).set_fill(opacity=0),num_dashes=24,dashed_ratio=.5) for part in p[0].family_members_with_points()])
        self.play(p[0].animate.set_opacity(.08),FadeIn(dead),run_time=.45)
        self.play(FadeIn(label('Motor neurons\nstill died',-2.75,-1.05,27,RED)),run_time=.25)
        self.finish()
        self.wait(1.5)  # Keep the decisive loss state readable after the final word.


class S14Differ(SpokenScene):
    def construct(self):
        self.add(heading('A gene need not encode the deposit protein'))
        gene=chip('SOD1 gene',TEXT,28).move_to([-4.8,2.25,0])
        enzyme=chip('superoxide\ndismutase 1',TEXT,28).move_to([-1.5,2.25,0])
        deposit=chip('TDP-43 clump',TEXT,30).move_to([3.8,2.25,0])
        path=Arrow([-3.7,2.25,0],[-2.85,2.25,0],buff=0,color=LIGHT)
        neq=label('≠',1.25,2.25,48)
        context=label('Usual deposit protein',3.8,1.55,24,LIGHT)
        panel=RoundedRectangle(width=12.5,height=4.2,corner_radius=.16,color=LIGHT,fill_opacity=.03).move_to([0,-1.05,0])
        panel_title=label('Alzheimer disease: the three classic dominant genes',0,.7,28)
        self.add(gene,context,panel,panel_title)
        self.at('need not encode')
        self.play(GrowArrow(path),FadeIn(enzyme),FadeIn(neq),FadeIn(deposit),run_time=.45)
        self.at('In Alzheimer disease')
        self.play(FadeOut(context),Indicate(panel_title,color=TEXT),run_time=.5)
        app=VGroup(chip('APP',TEXT,28).move_to([-5,-.35,0]),label('precursor Abeta\nis cut from',-1.7,-.35,28))
        ps=VGroup(chip('PSEN1\nPSEN2',TEXT,28).move_to([-5,-2.05,0]),label('presenilin, core of\ngamma-secretase',-1.25,-2.05,27))
        self.at('the three classic')
        self.play(FadeIn(app),GrowArrow(Arrow([-4.3,-.35,0],[-3.25,-.35,0],buff=0,color=LIGHT)),
                  FadeIn(ps),GrowArrow(Arrow([-4.05,-2.05,0],[-2.95,-2.05,0],buff=0,color=LIGHT)),run_time=.45)
        self.at('all affect how')
        shared=chip('how Abeta is\nmade or processed',TEXT,28).move_to([4,-1.2,0])
        self.play(GrowArrow(Arrow([.1,-.35,0],[2.03,-.9,0],buff=0,color=LIGHT)),
                  GrowArrow(Arrow([.5,-2.05,0],[2.03,-1.5,0],buff=0,color=LIGHT)),FadeIn(shared),run_time=.4)
        self.finish()


class S15Trial(SpokenScene):
    def construct(self):
        c=cards(); c[0].become(card_state(c[0],dim=True)); c[1].become(card_state(c[1],dim=True))
        q=label('Will removing a protein\nafter onset help?',-3,2.3,30)
        self.add(q,c[0],c[1])
        people=VGroup(*[VGroup(Circle(radius=.12,color=LIGHT,fill_opacity=.8).move_to([x,.75,0]),
                    RoundedRectangle(width=.25,height=.4,corner_radius=.05,color=LIGHT,fill_opacity=.3).move_to([x,.4,0])) for x in [-4.1,-3.4,-2.7,-2]])
        arrows=VGroup(Arrow([-3,.1,0],[-4.4,-.8,0],buff=0,color=LIGHT),Arrow([-3,.1,0],[-1.6,-.8,0],buff=0,color=LIGHT))
        self.play(FadeIn(people[:2]),run_time=.4)
        self.at('removing a protein')
        self.play(FadeIn(people[2:]),run_time=.4)
        self.at('after onset')
        self.play(GrowArrow(arrows[0]),GrowArrow(arrows[1]),FadeIn(label('random',-3,-.65,26)),run_time=.4)
        self.at('Randomized trials in people')
        self.play(FadeIn(c[2]),run_time=.3)
        self.at('most direct test')
        groups=VGroup(chip('drug',BLUE,28).move_to([-4.4,-1.95,0]),chip('placebo',YELLOW,28).move_to([-1.6,-1.95,0]))
        self.play(FadeIn(groups),TransformFromCopy(people[:2],people[:2].copy().scale(.75).set_color(BLUE).move_to([-4.4,-1.25,0])),
                  TransformFromCopy(people[2:],people[2:].copy().scale(.75).set_color(YELLOW).move_to([-1.6,-1.25,0])),run_time=.4)
        self.at('judged on how',lead=.4)
        self.add(label('think · function · survive',-3,-2.95,27))
        self.finish()


class S16Rule(SpokenScene):
    def construct(self):
        c=cards().shift(LEFT*3); self.add(c,heading('What each kind of evidence can show'))
        self.at('Autopsy shows')
        self.play(*[Transform(c[i],card_state(c[i],active=i==0,dim=i!=0)) for i in range(3)],run_time=.35)
        self.at('Families can show')
        self.play(*[Transform(c[i],card_state(c[i],active=i==1,dim=i!=1)) for i in range(3)],run_time=.35)
        self.at('Trials test whether')
        self.play(*[Transform(c[i],card_state(c[i],active=i==2,dim=i!=2)) for i in range(3)],run_time=.35)
        self.at('what it costs')
        self.play(FadeIn(label('…and what it costs',0,-2.85,28)),run_time=.3)
        self.finish()


class S17Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        c=cards().shift(LEFT*3)
        for i in range(3): c[i].become(card_state(c[i],active=i==2,dim=i!=2))
        self.add(c,heading('What each kind of evidence can show'),label('…and what it costs',0,-2.85,28))
        self.wait(5)


class S18Takeaway(SpokenScene):
    def construct(self):
        one=VGroup(RoundedRectangle(width=11.7,height=2,corner_radius=.2,color=LIGHT).move_to([0,1.35,0]),label('What does this finding show?',0,1.35,40))
        two=VGroup(RoundedRectangle(width=11.7,height=2,corner_radius=.2,color=LIGHT).move_to([0,-1.35,0]),label('What can it not show?',0,-1.35,40))
        self.add(one)
        self.at('What does it show'); self.play(one[0].animate.set_fill(GREY,opacity=.18),run_time=.3)
        self.at('And what can'); self.play(FadeIn(two),run_time=.3)
        self.finish()


class S19End(EndCard):
    LINE='Ask two things of every finding.'
    def construct(self):
        line=T(self.LINE,size=40,font=TITLE_FONT)
        fit(line,max_w=11.5)
        sub=T('biochemistrypedia.com',size=26,color=TEAL)
        VGroup(line,sub).arrange(DOWN,buff=.4)
        self.add(line)
        self.play(FadeIn(sub),run_time=.4)
        self.finish()
