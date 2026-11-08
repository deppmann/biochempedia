"""Cut axons and disease: reviewed animation.
COLOR MAP: BLUE Sarm1-null; YELLOW Sarm1 present; GREEN injury protection;
RED degeneration/overreach; TEAL evidence/test design; GREY structure; TEXT labels.
Survival traces are illustrative empirical survival models, not measured data:
S(t) = 100 * count(event times > t)/N. Normalized ages and deterministic
quantiles make two close, nonidentical step curves; no numerical age claim.
"""
import numpy as np
from bp_style import *

LESSON_TITLE = 'When Mature Neurons Fail: Neurodegeneration'
_BaseSpokenScene = SpokenScene
class SpokenScene(_BaseSpokenScene):
    # Same word alignment without writing an unrequested sync.log artifact.
    def at(self, phrase, lead=.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > .02:
            self.wait(rest)

def heading(s):
    return T(s,34,font=TITLE_FONT).move_to([0,3.1,0])

def centered_text(text,size=32,color=TEXT):
    # Centre each line separately; Pango's multiline layout is left aligned.
    return VGroup(*[T(line,size,color) for line in text.split('\n')]).arrange(DOWN,buff=.18)

def label(s,x,y,color=TEXT,size=32):
    return centered_text(s,size,color).move_to([x,y,0])

def panel(text,w=5.6,h=1.55,color=GREY,size=30):
    box=RoundedRectangle(width=w,height=h,corner_radius=.18,color=color,fill_opacity=.09)
    return VGroup(box,centered_text(text,size,color).move_to(box))

def neuron(x=0,y=0,scale=1):
    soma=Circle(.42,color=TEXT,fill_opacity=.2)
    dend=VGroup()
    for dy in [-.35,0,.35]:
        dend.add(Line([-.3,dy*.7,0],[-.85,dy*2,0],color=TEXT,stroke_width=4),
                 Line([-.65,dy*1.7,0],[-1.05,dy*1.7+.23,0],color=TEXT,stroke_width=3))
    ax=Line([.42,0,0],[2.1,0,0],color=TEXT,stroke_width=6)
    terminals=VGroup(*[Line([2.1,0,0],[2.55,d,0],color=TEXT,stroke_width=3) for d in [-.4,0,.4]])
    dend.stretch(.48,1)
    return VGroup(soma,dend,ax,terminals).scale(scale).move_to([x,y,0])

def nerve(fragmented=False):
    sheath=RoundedRectangle(width=11.8,height=4.8,corner_radius=.7,color=GREY,fill_opacity=.06)
    bg=VGroup(*[Line([-5.4,y,0],[5.4,y,0],color=GREY,stroke_width=3).set_opacity(.55) for y in [-1.5,-.85,1.4]])
    soma=Circle(.65,color=YELLOW,fill_opacity=.2).move_to([-4.8,.3,0])
    proximal=Line([-4.15,.3,0],[-1.35,.3,0],color=YELLOW,stroke_width=11)
    distal=(VGroup(*[Ellipse(width=.49,height=.3,color=RED,fill_opacity=.7).move_to([x,.3,0]) for x in np.linspace(-.65,5.05,10)]) if fragmented else Line([-.8,.3,0],[5.4,.3,0],color=YELLOW,stroke_width=11))
    return VGroup(sheath,bg,soma,proximal,distal)

def cut_mark():
    return VGroup(*[Line([-1.4,y,0],[-.85,y+.5,0],color=RED,stroke_width=6) for y in [-.2,.25]])

def mouse():
    # One continuous silhouette: no intersecting head/body/ear circles.
    outline=VMobject(color=GREY,stroke_width=3,fill_color=BG,fill_opacity=1)
    outline.start_new_path(np.array([-1.1,-.25,0]))
    outline.add_cubic_bezier_curve_to(np.array([-1.55,1.,0]),np.array([.15,1.,0]),np.array([.55,.5,0]))
    outline.add_cubic_bezier_curve_to(np.array([.55,1.05,0]),np.array([1.05,1.05,0]),np.array([1.,.5,0]))
    outline.add_cubic_bezier_curve_to(np.array([1.3,.4,0]),np.array([1.65,.05,0]),np.array([1.65,-.1,0]))
    outline.add_cubic_bezier_curve_to(np.array([1.4,-.35,0]),np.array([.9,-.4,0]),np.array([.55,-.42,0]))
    outline.add_cubic_bezier_curve_to(np.array([-.15,-.65,0]),np.array([-1.,-.65,0]),np.array([-1.1,-.25,0]))
    tail=ArcBetweenPoints([-1.1,-.25,0],[-2.,.25,0],angle=-PI/2,color=GREY,stroke_width=3)
    feet=VGroup(Line([-.6,-.5,0],[-.2,-.5,0],color=GREY),Line([.6,-.42,0],[1.,-.42,0],color=GREY))
    return VGroup(tail,outline,feet,Dot([1.2,.23,0],radius=.045,color=TEXT))

def disease_diagram(degenerate=False):
    cord=RoundedRectangle(width=1.3,height=3.4,corner_radius=.4,color=GREY,fill_opacity=.15).move_to([-4.8,0,0])
    muscle=RoundedRectangle(width=1.6,height=3.4,corner_radius=.4,color=GREY,fill_opacity=.15).move_to([4.7,0,0])
    axons=VGroup()
    for y in [-1,0,1]:
        if degenerate:
            axons.add(Polygon([-4.1,y+.09,0],[.5,y+.04,0],[2,y,0],[.5,y-.04,0],[-4.1,y-.09,0],color=RED,fill_opacity=1,stroke_width=0))
            axons.add(VGroup(*[Ellipse(width=.3,height=.16,color=RED,fill_opacity=.8).move_to([x,y,0]) for x in [2.5,3.2,3.8]]))
        else:
            axons.add(Line([-4.1,y,0],[3.9,y,0],color=TEXT,stroke_width=6))
    return VGroup(cord,axons,muscle)

def survival_axes():
    ax=Axes(x_range=[0,1,.25],y_range=[0,100,50],x_length=7.2,y_length=4.4,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([-1.9,.1,0])
    ticks=VGroup(*[label(str(v),-6.05,ax.c2p(0,v)[1],size=28) for v in [0,50,100]])
    labels=VGroup(label('percent alive',-2.0,2.65,size=28),label('age →',-1.9,-2.65,size=28))
    return ax,VGroup(ax,ticks,labels)

def survival_curves(ax):
    # Empirical survival evaluated on event quantiles, in normalized age units.
    q=np.arange(1,25)/25
    base=.57+.11*np.log(q/(1-q))
    groups=[]
    for k,col in enumerate([YELLOW,BLUE]):
        times=np.sort(base+(.025*np.sin(np.arange(24)*1.7) if k else 0))
        pts=[ax.c2p(0,100)]
        for i,t in enumerate(times):
            pts += [ax.c2p(float(t),100*(24-i)/24),ax.c2p(float(t),100*(23-i)/24)]
        pts.append(ax.c2p(1,0))
        curve=VMobject(color=col,stroke_width=4).set_points_as_corners(pts)
        groups.append(DashedVMobject(curve,num_dashes=38) if k else curve)
    return VGroup(*groups)

def legend():
    return VGroup(label('Sarm1 present',3.9,1.9,YELLOW,28),label('Sarm1-null',3.9,1.35,BLUE,28),label('(dashed)',3.9,.85,BLUE,28))

def question_frame():
    ax,g=survival_axes()
    return VGroup(g,heading('Will removing Sarm1 help?'),label('longer  /  same  /  shorter',3.7,0,TEAL,30),label('schematic',3.7,-1,GREY,28))

def summary_cards(count=3):
    data=[('Sarm1 loss protects cut axons','Flies and mice',GREEN),('No gain in measured disease outcomes','This SOD1G93A model;\nneed in disease not shown',TEAL),('Benefit in human ALS','Not tested here',GREY)]
    cards=VGroup()
    for i,(title,sub,col) in enumerate(data[:count]):
        height,y=(2.7,1.15-i*3.0) if count==2 else (1.95,1.65-i*2.1)
        box=RoundedRectangle(width=12.3,height=height,corner_radius=.18,color=col,fill_opacity=.1).move_to([0,y,0])
        txt=VGroup(T(title,34,col),centered_text(sub,32,TEXT)).arrange(DOWN,buff=.2).move_to(box)
        cards.add(VGroup(box,txt))
    return cards

class S00Title(TitleCard):
    TITLE='Cut axons, ALS, and what a negative result means'
    LESSON=LESSON_TITLE
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.8,TEAL,28),label(self.LESSON,0,1.9,GREY,28))
        title=VGroup(T('Cut axons, ALS, and what',46,font=TITLE_FONT),T('a negative result means',46,font=TITLE_FONT)).arrange(DOWN,buff=.3)
        self.play(FadeIn(title),Create(Line([-2,-1.8,0],[2,-1.8,0],color=GOLD)),run_time=.6)
        self.finish()

class S01Question(SpokenScene):
    def construct(self):
        row=VGroup(*[neuron(0,y,1.8) for y in [1.65,-.15,-1.95]])
        self.add(row,heading('Why do some fail while neighbours survive?'),label('motor neurons',0,-3,TEAL,32))
        self.at('some neurons fail'); self.play(row[0].animate.set_opacity(.06),row[2].animate.set_opacity(.06),run_time=.6)
        self.at('test one idea'); self.play(Indicate(row[1],color=TEXT,scale_factor=1.05),run_time=.5)
        self.finish()

class S02Cut(SpokenScene):
    def construct(self):
        n=nerve(); n[4].put_start_and_end_on([-1.35,.3,0],[5.4,.3,0]); self.add(n,heading('Injury: one highlighted axon'))
        self.at('axon is cut'); self.play(Create(cut_mark()),Transform(n[4],nerve()[4]),run_time=.45)
        self.at('cell body'); self.play(FadeIn(label('cell body',-4.7,-2.95,GREY)),run_time=.25)
        self.at('breaks into fragments'); self.play(Transform(n[4],nerve(True)[4]),FadeIn(label('◷ within days',2.4,-.55,RED,32)),run_time=.5)
        self.finish()

class S03Active(SpokenScene):
    def construct(self):
        n=nerve(True); self.add(n,cut_mark())
        passive=label('passive wasting',0,2.8,GREY,36); self.add(passive)
        self.at('It is not'); cross=Line(passive.get_left(),passive.get_right(),color=RED,stroke_width=6); self.play(Create(cross),run_time=.25)
        active=label('active program',0,2.8,RED,38)
        self.at('an active destruction program'); self.play(FadeOut(passive),FadeOut(cross),FadeIn(active),run_time=.35)
        self.play(Indicate(n[4],color=RED),run_time=.5)
        self.finish()

class S04Sarm(SpokenScene):
    def construct(self):
        self.add(heading('After a cut: mice'),label('normal mouse',-3,2.2,YELLOW),label('Sarm1-null mouse',3,2.2,BLUE))
        self.add(mouse().scale(.55).move_to([-3,1.35,0]),mouse().scale(.55).move_to([3,1.35,0]))
        nerves=VGroup(*[nerve().stretch_to_fit_width(5.55).stretch_to_fit_height(3.7).move_to([x,-1,0]) for x in [-3,3]])
        self.add(nerves)
        cuts=VGroup(*[cut_mark().scale(.47).move_to([x-.5,-.75,0]) for x in [-3,3]])
        self.at('removing one gene'); self.play(Create(cuts),run_time=.3)
        self.at('keeps the'); self.play(FadeIn(label('two weeks',0,-3.25,GREEN,32)),run_time=.25)
        target=nerve(True).stretch_to_fit_width(5.55).stretch_to_fit_height(3.7).move_to([-3,-1,0])
        self.play(Transform(nerves[0][4],target[4]),nerves[1][4].animate.set_color(GREEN),run_time=.6)
        self.finish()

class S05Als(SpokenScene):
    def construct(self):
        self.add(heading('ALS: motor axons degenerate'),label('spinal cord',-4.8,2.35),label('muscle',4.7,2.35))
        d=disease_diagram().stretch_to_fit_height(3.8).shift(UP*.15); self.add(d)
        self.at('Axons also degenerate'); self.play(Transform(d[1],disease_diagram(True).stretch_to_fit_height(3.8).shift(UP*.15)[1]),run_time=.7)
        m=mouse().scale(.85).move_to([-2.9,-2.65,0])
        card=panel('Sarm1-null\nALS model',5.3,1.5,BLUE,34).move_to([2.3,-2.65,0])
        self.at('to remove'); self.play(FadeIn(m),FadeIn(card),GrowArrow(Arrow(m.get_right()+RIGHT*.15,card.get_left(),color=BLUE,buff=.12)),run_time=.4)
        self.finish()

class S06Model(SpokenScene):
    def construct(self):
        m=mouse().scale(1.65).move_to([-3.3,.25,0])
        protein=panel('mutant human\nSOD1',4.3,2.0,TEXT,38).move_to([3.8,.55,0])
        self.add(m,heading('SOD1G93A mice'),protein)
        self.add(label('overexpression',3.8,-1.,TEAL,34),Arrow(m.get_right()+RIGHT*.12,protein.get_left(),color=GREY,buff=.15))
        self.at('develop motor neuron disease'); self.play(FadeIn(panel('motor neuron disease',12,1.6,RED,40).move_to([0,-2.65,0])),run_time=.45)
        self.finish()

class S07Question(SpokenScene):
    def construct(self):
        self.add(question_frame()); self.at('Predict'); self.finish()

class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question_frame()); self.wait(5)

def measure_icon(kind):
    if kind==0: return mouse().scale(.22)
    if kind==1:
        # Symbol of a recording, not a simulated or measured quantitative trace.
        return VGroup(Line([-.4,-.22,0],[-.4,.22,0],color=GREY),Line([-.4,0,0],[.4,0,0],color=GREY),label('∿',0,0,TEAL,36))
    return VGroup(Rectangle(width=.7,height=.4,color=GREY),*[Dot([x,y,0],radius=.045,color=TEAL) for x,y in [(-.2,.1),(0,-.1),(.2,.06)]])

class S09Reveal(SpokenScene):
    def construct(self):
        ax,g=survival_axes(); q=heading('Will removing Sarm1 help?'); self.add(g,q,legend())
        self.at('Now'); self.play(Create(survival_curves(ax)),run_time=.6)
        self.play(Transform(q,heading('No survival benefit detected')),FadeIn(label('schematic, not the real data',-2.,-3.3,GREY,28)),run_time=.3)
        for i,(cue,txt) in enumerate([('Nor did','behaviour'),('nerve recording','nerve recording'),('tissue measures','tissue')]):
            y=.1-i*.8
            row=VGroup(measure_icon(i).move_to([2.5,y,0]),label(txt,4.7,y,size=30))
            self.at(cue); self.play(FadeIn(row),run_time=.25)
        self.add(label('No benefit detected\non the measures tested',4.25,-2.65,TEAL,30)); self.finish()

class S10Meaning(SpokenScene):
    def construct(self):
        c=panel('Sarm1',3,1,TEXT,38).move_to([0,2.6,0]); self.add(c)
        left=panel('Needed after a cut ✓',5.7,1.65,GREEN,30).move_to([-3,.2,0])
        right=panel('Needed in this disease?\nnot shown',5.7,1.65,GREY,30).move_to([3,.2,0]); right[0]=DashedVMobject(right[0],num_dashes=35)
        self.at('Needed after a cut'); self.play(Create(Line(c.get_bottom(),left.get_top(),color=GREEN)),FadeIn(left),run_time=.45)
        self.at('does not mean'); self.play(Create(Line(c.get_bottom(),right.get_top(),color=GREY)),FadeIn(right),run_time=.45)
        self.at('may die by'); self.play(GrowArrow(Arrow(right.get_bottom(),[1,-2,0],color=RED)),FadeIn(label('Motor neurons may die\nby another route',0,-2.65,RED,34)),run_time=.5)
        self.finish()

class S11Limit(SpokenScene):
    def construct(self):
        ax,g=survival_axes(); plot=VGroup(g,survival_curves(ax)); self.add(plot,legend(),heading('Limits of this result'),label('schematic,\nnot the real data',3.9,-.3,GREY,28))
        self.at('one mouse model'); self.play(FadeIn(label('One SOD1 overexpression model, not human ALS',0,-3.3,TEAL,30)),run_time=.4)
        self.finish()

class S12Overreach(SpokenScene):
    def construct(self):
        bubble=RoundedRectangle(width=11.6,height=3.7,corner_radius=.4,color=GREY,fill_opacity=.08).move_to([0,.85,0])
        claim=label('“Axon degeneration\ndoes not matter in ALS”',0,.95,TEXT,54)
        speaker=VGroup(Circle(.3,color=TEXT),Arc(radius=.6,start_angle=0,angle=PI,color=TEXT).shift(DOWN*.8)).move_to([-4.8,-2.5,0])
        tail=Line([-4,-1,0],[-4.7,-1.8,0],color=GREY)
        self.add(bubble,claim,speaker,tail,label('a colleague',-2.5,-2.8,GREY,30))
        self.at('Now'); self.play(FadeIn(panel('GOES TOO FAR',5.6,1,RED,36).move_to([2.5,-2,0]),scale=1.15),run_time=.4)
        self.finish()

class S13Next(SpokenScene):
    def construct(self):
        self.add(heading('Proposed test • same mice'))
        d=disease_diagram().scale(.54).move_to([-3.2,.1,0])
        animal=mouse().scale(.8).move_to([-3.2,-2.55,0])
        self.add(d,animal,label('whole animal',-3.2,-3.35,size=30))
        self.add(label('cell bodies',-5.8,1.7,size=28),label('axons',-3.2,1.7,size=28),label('junctions',-.7,1.7,size=28))
        junctions=VGroup(*[Circle(.16,color=GREY).move_to(d[1][i].get_end()) for i in range(3)])
        self.add(junctions)
        rows=[('measures axons','1. Axon counts',1.4,d[1]),('nerve muscle contacts','2. Neuromuscular junctions',.3,junctions),('nerve muscle contacts','3. Motor unit estimates',-1.,VGroup(d[0],d[1],junctions)),('cell bodies','4. Motor neuron counts',-2.,d[0]),('as well as survival','5. Onset and survival',-3.,animal)]
        previous=None
        for cue,txt,y,part in rows:
            self.at(cue)
            text=label(txt,3.15,y,TEAL,28)
            # Persistent lights and leaders remain visible in sampled frames.
            leader=Line(text.get_left()+LEFT*.15,part.get_right()+RIGHT*.1,color=TEAL,stroke_width=2)
            anim=[FadeIn(text),part.animate.set_color(TEAL),Create(leader)]
            if previous is not None: anim.append(FadeOut(previous))
            self.play(*anim,run_time=.25)
            previous=leader
        self.finish()

class S14Next2(SpokenScene):
    def construct(self):
        self.add(heading('Genotype hidden from scorers'))
        head=Circle(.57,color=TEXT).move_to([-4.7,1.2,0]); eyes=VGroup(*[Dot([x,1.28,0],radius=.05) for x in [-4.9,-4.5]])
        visor=RoundedRectangle(width=1.1,height=.35,corner_radius=.1,color=TEAL,fill_opacity=.4).move_to([-4.7,1.28,0])
        body=RoundedRectangle(width=1.6,height=1.8,corner_radius=.3,color=GREY).move_to([-4.7,-.1,0])
        cage=RoundedRectangle(width=4.2,height=2.6,corner_radius=.15,color=GREY).move_to([1.1,1,0])
        m=mouse().scale(.7).move_to([1.1,.8,0])
        self.add(head,eyes,visor,body,cage,m,label('scorer',-4.7,-1.5,size=30),label('mouse 17 • coded',1.1,2.05,TEAL,28),Arrow([-3.6,1,0],[-1.3,1,0],color=GREY),panel('genotype covered',4.3,.75,GREY,28).move_to([1.1,-.7,0]))
        card=panel('Second model\n(for example TDP-43)',8.8,2.0,TEAL,34).move_to([1,-2.35,0])
        card[1].move_to([2.25,-2.35,0])
        card.add(mouse().scale(.72).move_to([-1.7,-2.35,0]))
        self.at('test is repeated'); self.play(FadeIn(card,shift=RIGHT),run_time=.5)
        self.finish()

class S15Cards(SpokenScene):
    def construct(self):
        cards=summary_cards(2)
        self.add(heading('What each result supports'),cards[0])
        self.at('Losing'); self.play(Indicate(cards[0],color=GREEN,scale_factor=1.02),run_time=.3)
        self.at('In this model'); self.play(FadeIn(cards[1]),run_time=.3)
        self.finish()

class S16Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        old=summary_cards(2); cards=summary_cards()
        self.add(heading('What each result supports'),old)
        self.play(Transform(old[0],cards[0]),Transform(old[1],cards[1]),FadeIn(cards[2]),run_time=.6); self.wait(4.4)

class S17Takeaway(SpokenScene):
    def construct(self):
        a=panel('Supported: Sarm1 loss protects cut axons.\nNot shown: benefit in this ALS model.',12.3,2.2,TEAL,36).move_to([0,2.1,0]); self.add(a)
        b=panel('Open: axon loss vs cell-body death;\nother models; human ALS',12.3,1.9,GREY,36).move_to([0,-.3,0])
        self.at('what it leaves open'); self.play(FadeIn(b),run_time=.4)
        self.at('Then design'); self.play(GrowArrow(Arrow([0,-1.35,0],[0,-2.05,0],color=GREEN,buff=0)),FadeIn(panel('Next test: measure both, repeat across models',12.3,1.25,GREEN,32).move_to([0,-2.85,0])),run_time=.45)
        self.finish()

class S18End(EndCard):
    LINE='Needed after a cut does not mean needed in this disease.'
    def construct(self):
        lines=VGroup(*[T(t,46,font=TITLE_FONT) for t in ['Needed after a cut','does not mean','needed in this disease.']]).arrange(DOWN,buff=.3).move_to([0,.6,0])
        self.add(lines,label('biochemistrypedia.com',0,-2.65,TEAL,30)); self.finish()
