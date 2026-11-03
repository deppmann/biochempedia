"""Chapter 3: A Reflex Is Not the Hurt.

COLOR MAP (shared with scenes.old.py): PURPLE = BLA ensemble; BLUE = reflex;
ORANGE = escape / avoidance / affective behaviour; YELLOW = noxious stimulus;
TEAL = innocuous touch / human prediction; GOLD = genetic tag;
RED = silencing / untested cause; GREY = neutral cells and anatomy.
All bars and gauges explicitly schematic: their heights are not effect sizes.
No invented data traces: the threshold diagram shows direction only.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
POS = [(-3.2,1.4),(-1.6,1.2),(0,1.5),(1.6,1.3),(3.2,1.4),
       (-3.1,0),(-1.7,-.2),(0,.1),(1.7,-.1),(3,.2),
       (-3.2,-1.4),(-1.5,-1.5),(.1,-1.3),(1.5,-1.5),(3.1,-1.4)]
ENS = [1,4,6,9,12,14]

def label(t,p,size=28,color=TEXT):
    return T(t,size,color).move_to(p)

def head(t):
    return VGroup(label(t,[0,3.22,0],32),
                  Line([-6.15,2.85,0],[6.15,2.85,0],color=GREY,stroke_opacity=.4))

def scope_tag():
    return label('male mice',[5.3,2.53,0],26,GREY)

def arrow(a,b,col=GREY):
    return Arrow(a,b,buff=.08,color=col,stroke_width=4,max_tip_length_to_length_ratio=.16)

def cell(p):
    soma=Circle(.3,stroke_color=GREY,stroke_width=3,fill_color=GREY,fill_opacity=.12)
    stubs=VGroup(*[Line(.3*np.array([np.cos(a),np.sin(a),0]),.58*np.array([np.cos(a),np.sin(a),0]),color=GREY,stroke_width=3) for a in (.5,2.4,4.2)])
    return VGroup(soma,stubs).move_to([p[0],p[1],0])

def field(state='grey'):
    frame=RoundedRectangle(width=8.1,height=4.65,corner_radius=.22,color=GREY,fill_color=GREY,fill_opacity=.035)
    cells=VGroup(*[cell(p) for p in POS])
    outlines=VGroup(*[DashedVMobject(Circle(.42,color=PURPLE,stroke_width=3),num_dashes=12).move_to(cells[i][0]) for i in ENS])
    outlines.set_opacity(0)
    f=VGroup(frame,cells,outlines).scale(1.06).move_to([1.7,-.3,0])
    if state in ('lit','ident'):
        for i in ENS:
            cells[i].set_color(PURPLE)
            cells[i][0].set_fill(PURPLE,.85 if state=='lit' else .12)
    if state=='silent':
        outlines.set_opacity(1)
    return f

def activate(f):
    return [f[1][i][0].animate.set_fill(PURPLE,.9).set_stroke(PURPLE) for i in ENS]+[f[1][i][1].animate.set_color(PURPLE) for i in ENS]

def paw():
    # Side view: foreleg tapers into a pad, with four separate rounded toes.
    outline=VMobject(color=BLUE,stroke_width=4,fill_color=BLUE,fill_opacity=.18)
    outline.set_points_smoothly([[-.65,1.65,0],[.2,1.65,0],[.25,.65,0],[.4,-.2,0],[.85,-.65,0],[1.02,-1.05,0],[.75,-1.4,0],[-.55,-1.45,0],[-.9,-1.1,0],[-.86,-.55,0],[-.72,.4,0],[-.65,1.65,0]])
    toes=VGroup(*[Ellipse(width=.5,height=.8,color=BLUE,fill_color=BG,fill_opacity=1).move_to([x,-1.35+.08*j,0]) for j,x in enumerate((-.55,-.05,.45,.9))])
    return VGroup(outline,toes).scale(1.08).move_to([-3.65,-.35,0])

def filament(p):
    contact=p[1][0].get_bottom(); x=contact[0]; y=contact[1]
    return VGroup(Line([x,-3.05,0],[x,y,0],color=TEAL,stroke_width=5),
                  RoundedRectangle(width=1.2,height=.22,corner_radius=.06,color=TEAL,fill_color=TEAL,fill_opacity=.3).move_to([x,-3.15,0]))

def prediction():
    p=paw(); f=filament(p)
    inset=field('silent').scale(.66).move_to([3.15,-.85,0])
    tags=VGroup(head('Predict'),scope_tag(),
                label('Does the paw still pull away?',[0,1.85,0],34),
                label('ensemble silenced',[3.15,1.02,0],28,PURPLE))
    return p,f,inset,tags

def person(col=GREY):
    h=Circle(.3,color=col,fill_color=col,fill_opacity=.22).shift(UP*.95)
    trunk=RoundedRectangle(width=.85,height=1.25,corner_radius=.25,color=col,fill_color=col,fill_opacity=.16)
    legs=VGroup(Line([-.22,-.6,0],[-.32,-1.45,0],color=col,stroke_width=7),Line([.22,-.6,0],[.32,-1.45,0],color=col,stroke_width=7))
    return VGroup(h,trunk,legs)

def mouse():
    body=Ellipse(width=2.6,height=1.5,color=GREY,fill_color=GREY,fill_opacity=.15)
    skull=Ellipse(width=1.15,height=1,color=GREY,fill_color=GREY,fill_opacity=.18).move_to([1.4,.3,0])
    ear=Circle(.28,color=GREY).move_to([1.18,.9,0])
    eye=Dot([1.7,.45,0],radius=.055,color=TEXT)
    tail=ArcBetweenPoints([-1.25,0,0],[-2.3,.3,0],angle=-1,color=GREY)
    feet=VGroup(*[Line([x,-.5,0],[x+.25,-.9,0],color=GREY,stroke_width=5) for x in (-.8,.7)])
    return VGroup(body,skull,ear,eye,tail,feet).scale(.8).move_to([-4.6,-.5,0])

def scanner():
    housing=RoundedRectangle(width=3.3,height=3.65,corner_radius=.6,color=GREY,fill_color=GREY,fill_opacity=.12)
    rim=Ellipse(width=2.65,height=3,color=TEXT).shift(UP*.05)
    bore=Ellipse(width=1.9,height=2.35,color=GREY,fill_color=BG,fill_opacity=1).shift(UP*.05)
    bed=RoundedRectangle(width=4.2,height=.25,corner_radius=.07,color=GREY,fill_color=GREY,fill_opacity=.7).move_to([-1,-.7,0])
    support=Line([-1.9,-.85,0],[-1.9,-1.8,0],color=GREY,stroke_width=6)
    # Supine patient: head enters the bore; torso and legs rest on the bed.
    patient=VGroup(Circle(.23,color=TEAL,fill_color=TEAL,fill_opacity=.3).move_to([-.35,-.3,0]),
                   RoundedRectangle(width=1.15,height=.32,corner_radius=.14,color=TEAL,fill_color=TEAL,fill_opacity=.25).move_to([-1.12,-.4,0]),
                   Line([-1.65,-.4,0],[-2.8,-.5,0],color=TEAL,stroke_width=8),
                   Line([-.75,-.36,0],[-1.65,-.48,0],color=TEAL,stroke_width=4))
    return VGroup(housing,rim,bore,bed,support,patient)

def gauge(x,col,txt):
    frame=RoundedRectangle(width=5.3,height=3.8,corner_radius=.22,color=col,fill_color=col,fill_opacity=.045).move_to([x,-.25,0])
    arc=Arc(radius=1.65,start_angle=0,angle=PI,color=col,stroke_width=5).move_arc_center_to([x,-.85,0])
    low=label('Low',[x-1.65,-1.4,0],26,col); high=label('High',[x+1.65,-1.4,0],26,col)
    tick=VGroup(Line([x-1.65,-.85,0],[x-1.42,-.85,0],color=col),Line([x+1.42,-.85,0],[x+1.65,-.85,0],color=col))
    needle=arrow([x,-.85,0],[x+1.2,.1,0],col)
    return VGroup(frame,arc,low,high,tick,needle,Dot([x,-.85,0],color=col),label(txt,[x,1.15,0],28,col))

class S00Title(TitleCard):
    LESSON='When Pain Persists'
    TITLE='A Reflex Is Not the Hurt'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28,GREY),T(self.TITLE,48,font=TITLE_FONT),Line(LEFT*1.2,RIGHT*1.2,color=GOLD)).arrange(DOWN,buff=.38)
        self.add(g); self.finish()

class S01Q(SpokenScene):
    def construct(self):
        p=paw().scale(.9).shift(DOWN*.2); f=filament(p)
        self.add(p,f,head('A reflex and a question'),label('touch',[-5.35,-2.8,0],28,TEAL))
        self.at('pulls away')
        self.play(p.animate.shift(UP*1.15),run_time=.55)
        self.at('Does that tell')
        self.play(FadeIn(label('Does that tell you\nhow much it hurts?',[2.5,.15,0],38,ORANGE)),run_time=.2)
        self.finish()

class S02Reflex(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,1,1],y_range=[0,1,1],x_length=5.7,y_length=3.8,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([-2.6,-.5,0])
        direction=arrow(ax.c2p(.15,.85),ax.c2p(.85,.2),BLUE)
        self.add(head('What was measured?'),ax,direction,
                 label('paw withdrawal threshold\n(lower = more sensitive)',[-2.6,2.05,0],28,BLUE),
                 label('before                 after injury',[-2.6,-2.6,0],26,GREY),
                 label('direction only · schematic',[-2.6,-3.35,0],26,GREY),
                 chip('reflex measure',BLUE,28).move_to([-2.55,-1.7,0]))
        tags=VGroup(*[chip(t,BLUE if j==0 else GREY,28) for j,t in enumerate(('behavioural readout','recordings','expression','immune assays'))]).arrange(DOWN,buff=.38).move_to([4.1,-.35,0])
        self.at('behavioral result'); self.play(FadeIn(tags),run_time=.25)
        self.at('A reflex is'); self.play(Indicate(direction,color=BLUE,scale_factor=1.03),run_time=.45)
        self.finish()

class S03Corder(SpokenScene):
    def construct(self):
        m=mouse(); f=field().scale(.9).move_to([1.9,-.25,0])
        scope=VGroup(Rectangle(width=.5,height=.65,color=TEXT,fill_color=TEXT,fill_opacity=.25),Line([0,-.3,0],[0,-.55,0],color=TEXT)).move_to([-3.65,.65,0])
        leader=VGroup(Line(scope.get_top(),[-2.25,1.7,0],color=TEXT),Line([-2.25,1.7,0],f[0].get_left()+UP*1.4,color=TEXT))
        self.add(head('Corder, Ahanonu and colleagues'),scope_tag(),m,scope,f,
                 label('what the scope sees',[.65,2.25,0],26),leader,
                 label('basolateral amygdala',[1.9,-2.75,0],28))
        sessions=label('repeated sessions',[1.9,-3.3,0],26,TEXT)
        self.at('repeated sessions')
        self.play(FadeIn(sessions),run_time=.3)
        self.play(Indicate(sessions,color=PURPLE,scale_factor=1.04),run_time=.5)
        self.finish()

class S04Ensemble(SpokenScene):
    def construct(self):
        f=field(); self.add(f,head('An ensemble for unpleasantness'),scope_tag())
        # A flame silhouette is a stimulus cartoon, not a chemical structure.
        flame=VMobject(color=YELLOW,fill_color=YELLOW,fill_opacity=.45)
        flame.set_points_smoothly([[-.8,-.7,0],[-.85,.1,0],[-.25,1.1,0],[0,.35,0],[.5,1.5,0],[.75,.3,0],[.8,-.6,0],[0,-1,0],[-.8,-.7,0]])
        flame.move_to([-4.7,.15,0])
        self.at('noxious stimuli')
        self.play(FadeIn(flame),FadeIn(label('noxious stimulus',[-4.7,-1.6,0],28,YELLOW)),*activate(f),run_time=.3)
        self.at('encoded their')
        self.play(FadeIn(label('ensemble encoding negative valence',[1.7,-3.15,0],28,PURPLE)),run_time=.2)
        self.finish()

class S05Injury(SpokenScene):
    def construct(self):
        f=field(); self.add(f,head('Light touch recruits the same ensemble'),scope_tag())
        injury=chip('after nerve\ninjury',RED,28).move_to([-4.6,1.2,0])
        self.at('After a nerve injury'); self.play(FadeIn(injury),run_time=.25)
        touch=VGroup(Line([-4.6,-1.2,0],[-4.6,-.1,0],color=TEAL,stroke_width=5),Ellipse(width=1.7,height=.35,color=GREY).move_to([-4.6,0,0]))
        self.at('innocuous stimuli'); self.play(FadeIn(touch),FadeIn(label('light touch',[-4.6,-1.7,0],28,TEAL)),run_time=.25)
        self.at('recruited the same'); self.play(*activate(f),FadeIn(label('same ensemble, now recruited by light touch',[1.0,-3.15,0],28,PURPLE)),run_time=.3)
        self.wait(3); self.finish()

class S06Silence(SpokenScene):
    def construct(self):
        f=field('lit'); self.add(f,head('Tag, then silence the ensemble'),scope_tag())
        rings=VGroup(*[Circle(radius=.43,color=GOLD,stroke_width=4).move_to(f[1][i][0]) for i in ENS])
        tag=label('activity-dependent\ntagging',[-4.7,.6,0],28,GOLD)
        self.at('tagged those neurons'); self.play(Create(rings),FadeIn(tag),run_time=.3)
        self.at('silenced them')
        self.play(*[f[1][i].animate.set_color(GREY).set_fill(GREY,.12) for i in ENS],FadeOut(rings),f[2].animate.set_opacity(1),Transform(tag,label('tagged cells\nsilenced',[-4.7,.6,0],30,PURPLE)),run_time=.3)
        self.add(label('dashed purple = tagged ensemble',[1.7,-3.15,0],28,PURPLE)); self.finish()

class S07Predict(SpokenScene):
    def construct(self):
        self.at('Predict'); self.add(*prediction()); self.finish()

class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(*prediction())
        self.add(label('Decide before you go on',[1.4,-2.85,0],28,TEAL))
        track=Line([-.9,-3.35,0],[5.8,-3.35,0],color=GREY,stroke_width=7)
        progress=Line([-.9,-3.35,0],[5.8,-3.35,0],color=TEAL,stroke_width=7)
        self.add(track); self.play(Create(progress),run_time=5,rate_func=linear)

class S09Reveal(SpokenScene):
    def construct(self):
        p=paw().scale(.8).move_to([-3.65,-1.35,0]); f=filament(p)
        inset=field('silent').scale(.29).move_to([-3.7,2.08,0])
        self.add(head('Reflex preserved; affective behaviour reduced'),scope_tag(),p,f,inset,
                 label('silenced',[-1.6,2.08,0],26,PURPLE),label('reflex\npreserved',[-5.55,.25,0],26,BLUE))
        self.at('Yes'); self.play(p.animate.shift(UP*.9),run_time=.5)
        # Relative heights only: no experimental effect magnitude is asserted.
        base=-2.35; xs=(1.3,4.5)
        ghosts=VGroup(*[DashedVMobject(Rectangle(width=1.1,height=3.3,color=ORANGE,stroke_opacity=.55).move_to([x,base+1.65,0]),num_dashes=24) for x in xs])
        bars=VGroup(*[Rectangle(width=1.1,height=3.3,color=ORANGE,fill_color=ORANGE,fill_opacity=.7).move_to([x,base+1.65,0]) for x in xs])
        chart=VGroup(Line([.1,base,0],[5.8,base,0],color=GREY),Line([.1,base,0],[.1,1.2,0],color=GREY),ghosts,
                     label('escape',[1.3,-2.8,0],28,ORANGE),label('avoidance',[4.5,-2.8,0],28,ORANGE),
                     label('affective behaviour reduced',[2.9,1.8,0],28,ORANGE),
                     label('direction only · schematic',[2.9,-3.35,0],26,GREY),
                     label('control',[2.9,1.1,0],26,GREY),Line([2.15,1.1,0],[1.85,.95,0],color=GREY))
        self.at('but escape'); self.play(FadeIn(chart),FadeIn(bars),run_time=.25)
        self.at('avoidance fell'); self.play(*[b.animate.stretch_to_fit_height(2.2).move_to([x,base+1.1,0]) for b,x in zip(bars,xs)],run_time=.5)
        self.wait(4); self.finish()

class S10Two(SpokenScene):
    def construct(self):
        left=gauge(-3,BLUE,'reflex withdrawal'); right=gauge(3,ORANGE,'affective behaviour')
        state=label('before silencing the ensemble',[0,2.35,0],30,PURPLE)
        self.add(head('Two measurements can come apart'),scope_tag(),left,right,
                 state,
                 label('male mice · nerve-injury model · chosen behaviours\nno verbal report; touch detection needs its own test',[0,-2.85,0],26,GREY))
        self.at('can come apart'); self.play(Indicate(left[5],color=BLUE),Transform(right[5],arrow([3,-.85,0],[1.8,.1,0],ORANGE)),Transform(state,label('after silencing the ensemble',[0,2.35,0],30,PURPLE)),run_time=.5)
        self.finish()

class S11Human(SpokenScene):
    def construct(self):
        s=scanner().scale(1.25).move_to([2,-.2,0])
        self.add(head('People: prediction from observation'),s,
                 chip('observational study',TEAL,28).move_to([-3.65,1.45,0]),
                 label('cause untested',[-3.65,.2,0],30,RED))
        self.at('these cell'); self.play(FadeIn(label('cell-type manipulation\nunavailable',[-3.65,-1.2,0],28)),run_time=.25)
        self.at('prediction'); self.play(FadeIn(label('prediction',[-3.65,-2.8,0],32,TEAL)),GrowArrow(arrow([-2.1,-2.6,0],[.3,-1.4,0],TEAL)),run_time=.25)
        self.finish()

class S12Baliki(SpokenScene):
    def construct(self):
        s=scanner().scale(.95).move_to([-3.7,.1,0])
        cohort=VGroup(*[person(TEAL).scale(.5).move_to([x,-2.55,0]) for x in (-5.1,-3.8,-2.5)])
        self.add(head('Baliki and colleagues'),s,cohort,label('baseline scan',[-3.7,2.3,0],28),label('adults · subacute back pain',[-3.8,-3.5,0],26,GREY))
        link=arrow([-1,.05,0],[2,.05,0],TEAL)
        timeline=VGroup(Line([-1,.05,0],[2,.05,0],color=GREY,stroke_opacity=.45),Line([2,-.15,0],[2,.25,0],color=GREY,stroke_opacity=.45),label('1 year',[.6,.7,0],32,TEAL).set_opacity(.6))
        self.add(timeline)
        self.at('year later'); self.play(GrowArrow(link),timeline.animate.set_opacity(1),run_time=.25)
        groups=VGroup(chip('recovering',TEAL,28).move_to([4.45,1.7,0]),chip('persisting',ORANGE,28).move_to([4.45,-1.4,0]),
                      person(TEAL).scale(.6).move_to([4.45,.35,0]),person(ORANGE).scale(.6).move_to([4.45,-2.7,0]),
                      arrow([2,.05,0],[3,1.4,0],TEAL),arrow([2,.05,0],[3,-1.3,0],ORANGE))
        self.at('they asked'); self.play(FadeIn(groups),run_time=.25); self.wait(4); self.finish()

class S13Cutoff(SpokenScene):
    def construct(self):
        self.add(head('Recovering did not mean pain-free'),
                 label('20% drop cutoff',[0,2,0],36,TEAL),
                 label('100% baseline pain',[-3.9,.95,0],28),label('80% at the cutoff',[2.5,.95,0],28))
        # Exact arithmetic at the cutoff: 100 - 20 = 80; not a cohort mean.
        before=Rectangle(width=4,height=1.2,color=GREY,fill_color=GREY,fill_opacity=.45).move_to([-3.9,-.2,0])
        remaining=Rectangle(width=3.2,height=1.2,color=ORANGE,fill_color=ORANGE,fill_opacity=.55).move_to([2.1,-.2,0])
        removed=DashedVMobject(Rectangle(width=.8,height=1.2,color=TEAL).move_to([4.1,-.2,0]),num_dashes=16)
        self.add(before,remaining,removed,arrow([-1.6,-.2,0],[.1,-.2,0],TEAL),label('still in pain',[2.1,-1.2,0],30,ORANGE),label('20 recovering  |  19 persisting',[0,-3.2,0],26,GREY))
        self.at('It did not'); self.play(FadeIn(label('Recovering ≠ pain-free',[0,-2.25,0],38,ORANGE)),run_time=.2); self.finish()

class S14Auc(SpokenScene):
    def construct(self):
        # Sagittal schematic, anterior at left: cortical mantle, separate
        # posterior cerebellum and a descending brainstem.
        brain=VMobject(color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.08)
        brain.set_points_smoothly([[-3.35,-.25,0],[-3.65,.25,0],[-3.5,1.05,0],[-2.9,1.65,0],[-1.8,1.95,0],[-.4,1.9,0],[.85,1.55,0],[1.8,.9,0],[2.15,.15,0],[1.9,-.5,0],[1.05,-.7,0],[.35,-.65,0],[-.1,-1.05,0],[-1.2,-1.1,0],[-1.85,-.7,0],[-2.5,-.6,0],[-3.35,-.25,0]])
        cerebellum=VMobject(color=GREY,stroke_width=3,fill_color=GREY,fill_opacity=.12)
        cerebellum.set_points_smoothly([[1.15,-.85,0],[1.8,-.65,0],[2.45,-.95,0],[2.65,-1.45,0],[2.2,-1.85,0],[1.5,-1.8,0],[1.05,-1.35,0],[1.15,-.85,0]])
        folia=VGroup(*[ArcBetweenPoints([1.4,y,0],[2.35,y-.1,0],angle=.35,color=GREY,stroke_opacity=.5) for y in (-1.02,-1.25,-1.48)])
        stem=VMobject(color=GREY,stroke_width=5).set_points_smoothly([[.55,-.85,0],[.8,-1.4,0],[.65,-1.85,0],[1,-2.35,0]])
        sulci=VGroup(*[ArcBetweenPoints(a,b,angle=.8,color=GREY,stroke_opacity=.45) for a,b in [([-2.6,1.2,0],[-1.8,.5,0]),([-.9,1.65,0],[-.4,.7,0]),([.7,1.3,0],[1.2,.6,0])]])
        anatomy=VGroup(brain,cerebellum,stem,sulci,folia).shift(DOWN*.35)
        a=Dot([-2.95,.35,0],radius=.16,color=TEAL); b=Dot([-2,-.6,0],radius=.16,color=TEAL)
        link=Line(a.get_center(),b.get_center(),color=TEAL,stroke_width=8)
        self.add(head('Baseline connectivity predicts persistence'),anatomy,a,b,link,
                 label('stronger baseline connectivity',[0,2.35,0],28,TEAL),
                 label('ROC area 0.83',[4.65,-2.15,0],32,TEAL))
        self.at('between'); self.play(FadeIn(label('medial prefrontal\ncortex',[-4.65,1.5,0],26)),Create(Line([-3.5,1.03,0],a.get_center(),color=GREY)),run_time=.25)
        self.at('nucleus accumbens'); self.play(FadeIn(label('nucleus accumbens',[-3.8,-2.25,0],26)),Create(Line([-2.2,-2,0],b.get_center(),color=GREY)),run_time=.25)
        self.at('predicted who persisted'); self.play(FadeIn(label('→ persisted',[4.65,-.7,0],32,ORANGE)),run_time=.25); self.finish()

class S15Meaning(SpokenScene):
    def construct(self):
        p=person(TEAL).scale(1.15).move_to([-3.25,-.1,0]); q=person(ORANGE).scale(1.15).move_to([3.25,-.1,0])
        # One illustrative pair, not patient measurements or individual risk scores.
        bars=VGroup(Rectangle(width=2,height=.35,color=TEAL,fill_color=TEAL,fill_opacity=.6).move_to([-3.25,1.9,0]),Rectangle(width=2,height=.85,color=ORANGE,fill_color=ORANGE,fill_opacity=.6).move_to([3.25,2.15,0]))
        self.add(head('ROC area 0.83: pair ordering'),p,q,bars,
                 label('connectivity\nscore',[0,2.1,0],26,GREY),label('illustrative\npair',[0,-.8,0],26,GREY),
                 label('recovering',[-3.25,-1.9,0],28,TEAL),label('persisting',[3.25,-1.9,0],28,ORANGE),label('<',[0,.4,0],64),
                 label('Persisting scores higher in 83% of pairs',[0,-2.5,0],28))
        self.at('not a cause'); self.play(FadeIn(label('not a cause',[-3.25,-3.25,0],28,RED)),run_time=.2)
        self.at("not one person's risk"); self.play(FadeIn(label("not one person's risk",[3.25,-3.25,0],28,RED)),run_time=.2); self.finish()

class S16Take(SpokenScene):
    def construct(self):
        self.add(head('What we know, and where'))
        rodent=label('rodent models: wiring, cord, immune cells',[0,2.35,0],28,TEXT)
        gang=chip('ganglion',GREY,28).move_to([-4.5,1.25,0]); cord=chip('dorsal horn',GREY,28).move_to([0,1.25,0]); brain=chip('brain',GREY,28).move_to([4.7,1.25,0])
        links=VGroup(arrow(gang.get_right(),cord.get_left()),arrow(cord.get_right(),brain.get_left()))
        self.add(rodent,gang,cord,brain,links)
        wiring=VGroup(label('changed',[-4.5,.3,0],28,TEAL),label('spontaneous\nfiring',[-4.5,-.45,0],26),Dot([-5.5,1.25,0],color=TEAL))
        inhibition=VGroup(label('changed',[0,.3,0],28,TEAL),label('lost inhibition',[0,-.35,0],26))
        immune=VGroup(cell((0,0)).scale(.55).move_to([2.3,.35,0]),Line([2.3,.65,0],[1,1.05,0],color=GREY),label('immune cells',[3.4,-.25,0],26),label('changed',[4.15,.4,0],28,TEAL))
        self.at('the wiring'); self.play(FadeIn(wiring),run_time=.2)
        self.at('the cord'); self.play(FadeIn(inhibition),run_time=.2)
        self.at('immune cells'); self.play(FadeIn(immune),FadeIn(label('conditional on sex, model, compartment',[0,-.95,0],26,TEXT)),run_time=.2)
        reflex=VGroup(arrow([-5.4,-2.25,0],[-2.4,-2.25,0],BLUE),label('reflex',[-3.9,-2.9,0],28,BLUE))
        dial=VGroup(Arc(radius=1.2,start_angle=0,angle=PI,color=ORANGE,stroke_width=5).shift([3.4,-3.35,0]),
                    arrow([3.4,-3.35,0],[2.45,-2.63,0],ORANGE),Dot([3.4,-3.35,0],radius=.07,color=ORANGE),
                    label('Low',[2.05,-3.65,0],26,ORANGE),label('High',[4.75,-3.65,0],26,ORANGE),
                    label('affective behaviour',[3.4,-1.95,0],26,ORANGE))
        self.at('In mice'); self.play(FadeIn(label('male mice: affective behaviour separable from reflex',[0,-1.5,0],28,TEXT)),FadeIn(reflex),FadeIn(dial),run_time=.25)
        self.at('In people'); self.play(FadeOut(reflex),FadeOut(dial),FadeIn(label('people: association and prediction',[0,-2.8,0],32,TEAL)),run_time=.25); self.finish()

class S17End(EndCard):
    LINE='A reflex and the hurt are two measurements, and they can come apart.'
    def construct(self):
        self.add(label('A reflex and the hurt\nare two measurements,\nand they can come apart.',[0,.3,0],42),label('biochemistrypedia.com',[0,-2.4,0],26,TEAL))
        self.wait(max(3.5,self.narration_s)); self.finish()
