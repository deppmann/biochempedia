"""Chapter 6, revision after frame review.
COLOR MAP: BLUE unchosen gene / WT; RED repression / lost potency;
GREEN chosen gene / gained response; TEAL enhancer hubs; ORANGE receptor / mutant;
PURPLE feedback lock; GOLD title; GREY guides; YELLOW odorant / pocket.
All ligand shapes and seven-bar receptor bundles are cartoons, never structures.
All dose traces: Hill slope 1, zero baseline, normalized own maximum 1.
"""
import numpy as np
from bp_style import *
ORANGE='#F29E4C'
PURPLE='#B58CD9'


def head(s): return T(s,30).move_to([0,3.2,0])
def tile(color=BLUE,s=.7,op=.35):
    return RoundedRectangle(width=s,height=s,corner_radius=.1,color=color,fill_color=color,fill_opacity=op)
def arr(a,b,color=GREY): return Arrow(a,b,buff=.12,color=color,stroke_width=4)
def lead(a,b,color=GREY): return Line(a,b,color=color,stroke_width=2)
def pocket():
    body=Polygon([-2,-2.3,0],[2,-2.3,0],[2,2.3,0],[.9,2.3,0],[.9,.3,0],[-.9,.3,0],[-.9,2.3,0],[-2,2.3,0],color=ORANGE,fill_color=ORANGE,fill_opacity=.22,stroke_width=5)
    return VGroup(body,T('receptor',30,ORANGE).move_to([0,-1.4,0]))
def inset():
    return RoundedRectangle(width=1.65,height=1.65,corner_radius=.2,color=YELLOW,fill_color=YELLOW,fill_opacity=.12).move_to([0,1.3,0])
def insect():
    return VGroup(*[RoundedRectangle(width=2.25,height=2.25,corner_radius=.3,color=ORANGE,fill_color=ORANGE,fill_opacity=.25).move_to([x,y,0]) for x,y in [(-1.5,1.5),(1.5,1.5),(1.5,-1.5),(-1.5,-1.5)]])
def gpcr():
    # Seven simple rounded bars, no ribbons or atomic geometry.
    bars=VGroup(*[RoundedRectangle(width=.47,height=3.6,corner_radius=.22,color=ORANGE,fill_color=ORANGE,fill_opacity=.32).move_to([i*.57, .3-.13*i*i,0]) for i in range(-3,4)])
    return VGroup(bars,RoundedRectangle(width=1.1,height=.9,corner_radius=.15,color=YELLOW,fill_color=BG,fill_opacity=1).move_to([0,.7,0]))
def odor(name,roundish=False):
    shape=(Ellipse(width=1.15,height=.85) if roundish else RoundedRectangle(width=1.5,height=.48,corner_radius=.12)).set_color(YELLOW).set_fill(YELLOW,.55)
    return VGroup(shape,T(name,26,YELLOW).next_to(shape,DOWN,buff=.15))
def neuron():
    soma=Ellipse(width=2.8,height=2.7,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([0,-1.55,0])
    stem=Line([0,-.2,0],[0,1,0],color=GREY,stroke_width=7)
    cilia=VGroup(*[Line([0,1,0],[x,2.35,0],color=GREY,stroke_width=5) for x in [-3,0,3]])
    rec=VGroup(*[tile(ORANGE,.55).move_to([x,2.05,0]) for x in [-2.3,0,2.3]])
    return VGroup(soma,stem,cilia,rec)
def lock_icon():
    return VGroup(Arc(radius=.35,start_angle=0,angle=PI,color=PURPLE,stroke_width=6).move_to([0,.3,0]),RoundedRectangle(width=.95,height=.7,corner_radius=.1,color=PURPLE,fill_color=PURPLE,fill_opacity=.3).move_to([0,-.15,0]),Dot([0,-.15,0],color=PURPLE))


def graph(relative=False,cursor_ticks=False,span=False):
    ax=Axes(x_range=[-2,2,1],y_range=[0,1,.5],x_length=10.3,y_length=5.2,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([0,-.05,0])
    ax.y_axis.set_opacity(0)  # Axes' default origin is 1 mM on this log-dose axis.
    left=Line(ax.c2p(-2,0),ax.c2p(-2,1),color=GREY)
    vals=[(-2,'0.01'),(-1,'0.1'),(0,'1'),(1,'10'),(2,'100')]
    ticks=VGroup(*[M(v,26).next_to(ax.c2p(x,0),DOWN,buff=.13) for x,v in vals if not (cursor_ticks and x==0) and not(span and x==1)])
    yt=VGroup(*[M(v,26).next_to(ax.c2p(-2,y),LEFT,buff=.16).shift(UP*.12 if y==0 else UP*0) for y,v in [(0,'0'),(.5,'0.5'),(1,'1')]])
    xl=T('dose / wild-type EC50 (log scale)' if relative else 'propionate dose (mM; log scale)',26).move_to([0,-3.4,0])
    yl=T('fraction of own maximum',26).rotate(PI/2).move_to([-6.25,0,0])
    legend=VGroup(T('wild type',26,BLUE),T('F155A',26,ORANGE)).arrange(DOWN,aligned_edge=LEFT,buff=.12).move_to([-3.9,2.1,0])
    model=T('MODEL • Hill slope 1 • zero baseline • own maximum = 1',26,GREY).move_to([0,3.55,0])
    ks=(1,6.5) if relative else (.824,12.3)
    curves=VGroup(*[ax.plot(lambda x,k=k:10**x/(k+10**x),x_range=[-2,2,.02],color=c,stroke_width=5) for k,c in zip(ks,[BLUE,ORANGE])])
    return VGroup(ax,left,ticks,yt,xl,yl,legend,model),curves,ax

def readings(ax,answer=False):
    x=np.log10(.824); p=ax.c2p(x,.5); low=ax.c2p(x,.824/(12.3+.824))
    wt=T('WT 0.50',26,BLUE).move_to(p+[-1.55,.65,0])
    read=T('F155A 0.063 (model)' if answer else 'F155A ?',26,ORANGE).move_to([2.8,-2.25,0] if answer else [2.2,-2.23,0])
    g=VGroup(DashedLine(ax.c2p(x,0),ax.c2p(x,1),color=YELLOW),Dot(p,color=BLUE,radius=.08),wt,lead(wt.get_bottom(),p,BLUE),M('0.824 mM',26,YELLOW).next_to(ax.c2p(x,0),DOWN,buff=.13),read)
    if answer: g.add(Dot(low,color=ORANGE,radius=.085),lead(read.get_left(),low,ORANGE))
    else: g.add(T('?',32,ORANGE).move_to(low))
    return g

def ec_span(ax):
    a=ax.c2p(np.log10(.824),.5); b=ax.c2p(np.log10(12.3),.5)
    lab=T('about 15-fold',26,YELLOW).move_to((a+b)/2+[2.4,-.65,0])
    return VGroup(DoubleArrow(a,b,buff=0,color=YELLOW,stroke_width=4),Dot(b,color=ORANGE,radius=.085),lab,M('12.3 mM',26,ORANGE).next_to(ax.c2p(np.log10(12.3),0),DOWN,buff=.13))

def question_frame(answer=False,span=False):
    base,c,ax=graph(cursor_ticks=True,span=span)
    q=T('At the WT EC50, what fraction does F155A give?',28).move_to([0,3.0,0])
    g=VGroup(base,c if answer else VGroup(c[0]),readings(ax,answer),q)
    if span: g.add(ec_span(ax))
    return g

class S00Title(TitleCard):
    LESSON='One Receptor per Neuron: How Olfactory Neurons Choose'
    TITLE='What the Choice Buys: a Pocket'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T('One Receptor per Neuron:\nHow Olfactory Neurons Choose',26,GREY),T('What the Choice Buys:\na Pocket',48,font=TITLE_FONT),Line(LEFT,RIGHT,color=GOLD)).arrange(DOWN,buff=.35)
        self.play(FadeIn(g),run_time=.6); self.finish()

class S01(SpokenScene):
    def construct(self):
        n=neuron(); self.add(n,head('one receptor type'))
        lab=T('same receptor',28,ORANGE).move_to([3.8,2.85,0]); cil=T('cilia',28).move_to([-3.8,2.85,0])
        self.add(lab,lead(lab.get_bottom(),n[3][2].get_top(),ORANGE),cil,lead(cil.get_bottom(),[-2.8,2.25,0]))
        mol=VGroup(*[odor('',j%2==0).move_to([x,y,0]) for j,(x,y) in enumerate([(-4.8,1),(-5,-.6),(-3.7,-2),(4.8,1),(5,-.6),(3.7,-2),(-2.7,-3),(2.7,-3)])])
        self.at('Does that mean'); self.play(FadeIn(mol),FadeIn(T('?',70,YELLOW).move_to([1.9,-1,0])),run_time=.5); self.finish()

class S02(SpokenScene):
    def construct(self):
        n=neuron(); h=head('one receptor type'); self.add(n,h)
        self.at('one kind of receptor')
        selected=n[3][1]; rest=VGroup(n[0],n[1],n[2],n[3][0],n[3][2])
        self.play(FadeOut(rest),selected.animate.scale(4).move_to([0,0,0]),run_time=.8)
        self.play(Transform(selected,pocket()),run_time=.5)
        self.at('binding pocket'); self.play(FadeIn(inset()),Transform(h,head('binding pocket').set_color(YELLOW)),run_time=.35); self.finish()

class S03(SpokenScene):
    def construct(self):
        self.add(pocket(),inset(),head('one pocket, different odours'))
        a=odor('odour A').move_to([-3.8,1.3,0]); b=odor('odour B',True).move_to([3.8,1.3,0]); a[1].move_to([-3.8,.3,0]); b[1].move_to([3.8,.3,0]); self.add(a,b)
        self.at('one pocket'); self.play(a[0].animate.move_to([0,1.3,0]),run_time=.3)
        self.wait(1)
        self.at('does not mean'); self.play(a[0].animate.move_to([-3.8,1.3,0]),b[0].animate.move_to([0,1.3,0]),run_time=.35)
        self.wait(1); self.finish()

class S04(SpokenScene):
    def construct(self):
        p=insect(); marker=Dot(p[0].get_corner(UL)+[.25,-.25,0],color=YELLOW,radius=.14); group=VGroup(p,marker)
        self.add(group,T('Del Mármol, Yedlin and Ruta • 2021',26).move_to([0,-3.4,0]),T('cartoon, not a cryo-EM map',26).move_to([0,-2.95,0]))
        self.at('solved structures'); self.play(group.animate.rotate(.12).scale(.93),run_time=1)
        self.at('insect receptor'); h=head('bristletail insect receptor'); self.play(FadeIn(h),run_time=.4)
        self.at('called'); self.play(Transform(group,VGroup(insect(),Dot([-2.3,2.3,0],color=YELLOW,radius=.14))),Transform(h,head('bristletail receptor • MhOR5')),run_time=.45); self.finish()

class S05(SpokenScene):
    def construct(self):
        p=insect(); pore=Circle(radius=.35,color=GREY,fill_color=BG,fill_opacity=1,stroke_width=4)
        lab=T('odorant-gated ion channel',30,ORANGE).move_to([0,-3.15,0]); self.add(p,pore,head('MhOR5 • four subunits'))
        self.at('four identical subunits'); self.play(LaggedStart(*[Indicate(x,color=YELLOW) for x in p],lag_ratio=.18),run_time=1.4)
        self.at('itself an'); self.play(FadeIn(lab),pore.animate.scale(2.5).set_color(YELLOW).set_fill(YELLOW,.35),*[x.animate.shift(x.get_center()*.07) for x in p],run_time=.55); self.finish()

class S06(SpokenScene):
    def construct(self):
        p=insect().move_to([-2.8,0,0]); site=p[1].get_center(); well=RoundedRectangle(width=1.6,height=1.3,corner_radius=.2,color=YELLOW).move_to(site)
        self.add(p,well,T('MhOR5 tetramer',28,ORANGE).move_to([-2.8,3.1,0]),T('cartoon shapes, not structures',26).move_to([0,-3.35,0]))
        caption=T('one pocket on each subunit',26).move_to([3.2,-1.7,0]); self.add(caption,lead(caption.get_left(),well.get_right(),YELLOW))
        a=odor('eugenol').move_to([3.2,1.7,0]); b=odor('DEET',True).move_to([3.2,.1,0])
        self.at('plant compound'); self.play(FadeIn(a),run_time=.3)
        self.play(a[0].animate.move_to(site),a[1].animate.next_to(well,DOWN,buff=.5),run_time=.35)
        self.at('repellent'); self.play(FadeIn(b),run_time=.3)
        self.at('same pocket'); self.play(a.animate.move_to([3.2,1.7,0]).set_opacity(.25),b[0].animate.move_to(site),b[1].animate.next_to(well,DOWN,buff=.5),run_time=.4)
        self.at('chemically unrelated'); self.play(FadeIn(T('chemically unrelated',28,YELLOW).move_to([3.2,-2.5,0])),run_time=.4); self.finish()

class S07(SpokenScene):
    def construct(self):
        p=insect().scale(.94).move_to([-3.2,-.15,0]); self.add(p,T('insect channel',28,ORANGE).move_to([-3.2,2.8,0]))
        self.at('not a template'); self.play(FadeIn(head('contrast, not a template')),run_time=.4)
        self.at('Mammals use'); r=gpcr().move_to([3,-.1,0])
        self.play(FadeIn(r,shift=LEFT*.3),FadeIn(T('mammalian GPCR',28,ORANGE).move_to([3,2.8,0])),run_time=.5)
        self.add(T('seven bars = seven helices • cartoon, not a structure',26).move_to([0,-3.25,0])); self.finish()

class S08(SpokenScene):
    def construct(self):
        p=gpcr().move_to([0,.3,0]); self.add(p,T('Billesbølle and colleagues • 2023',26).move_to([0,-3.45,0]),T('cartoon, not a structure • PDB 8F76 reference',26).move_to([0,-2.95,0]))
        self.at('solved the active'); self.play(Rotate(p,angle=.16),run_time=.65)
        self.at('human receptor'); self.play(FadeIn(head('human OR51E2 • seven helices')),run_time=.4)
        self.at('bound to propionate'); lig=tile(YELLOW,.55,.7).move_to(p[1]); lab=T('propionate',28,YELLOW).move_to([3.8,1.1,0])
        self.play(FadeIn(lig),run_time=.25)
        self.play(Rotate(VGroup(p,lig),angle=-.10),run_time=.4)
        self.play(FadeIn(lab),Create(lead(lab.get_left(),lig.get_right(),YELLOW)),run_time=.3); self.finish()

class S09(SpokenScene):
    def construct(self):
        p=gpcr().move_to([0,.55,0]); lig=tile(YELLOW,.5,.7).move_to(p[1]); self.add(p,lig,head('human OR51E2'))
        self.at('purified'); lab=T('purified receptor',28).move_to([-4,1,0]); self.play(FadeIn(lab),Create(lead(lab.get_right(),p.get_left())),run_time=.35)
        self.at('engineered complex'); self.play(FadeIn(T('engineered complex',28).move_to([3.9,-2.6,0])),run_time=.35)
        self.at('with a'); g=chip('mini G protein',TEAL,28).move_to([0,-2.45,0]); self.play(FadeIn(g),Create(lead(p.get_bottom(),g.get_top(),TEAL)),run_time=.5); self.finish()

class S10(SpokenScene):
    def construct(self):
        self.add(head('odorant receptor repertoires'),T('human structure here; earlier chapters used mouse',27).move_to([0,-3.1,0]))
        for x,name in [(-3,'human'),(3,'mouse')]: self.add(T(name,32).move_to([x,2.5,0]),Line([x-2,-2.3,0],[x+2,-2.3,0],color=GREY))
        self.at('Humans carry'); bar=Rectangle(width=2.2,height=1.6,color=ORANGE,fill_color=ORANGE,fill_opacity=.5).move_to([-3,-1.5,0]); self.play(GrowFromEdge(bar,DOWN),FadeIn(M('≈ 400',42,ORANGE).move_to([-3,.2,0])),run_time=.6)
        self.at('Mice carry'); bar2=Rectangle(width=2.2,height=4,color=ORANGE,fill_color=ORANGE,fill_opacity=.5).move_to([3,-.3,0]); self.play(GrowFromEdge(bar2,DOWN),FadeIn(M('≈ 1,000',42,ORANGE).move_to([3,2.0,0])),run_time=.6); self.finish()

class S11(SpokenScene):
    def construct(self):
        # Equal-size cartoons before/after: assay gain does not establish a wider pocket.
        p=gpcr().move_to([-2.4,0,0]); self.add(p,head('longer-chain fatty acids • cAMP assay'))
        f=T('F155',28,ORANGE).move_to([-5,1.3,0]); l=T('L158',28,ORANGE).move_to([.3,1.3,0]); self.add(f,l,lead(f.get_right(),[-2.95,.7,0],ORANGE),lead(l.get_left(),[-1.85,.7,0],ORANGE),Dot([-2.95,.7,0],color=ORANGE),Dot([-1.85,.7,0],color=ORANGE))
        chain=odor('longer chain').move_to([3.9,1,0]).set_opacity(.45); status=T('wild type\nno response',32,GREY).move_to([3.8,-.9,0]); self.add(chain,status)
        self.at('two pocket mutants'); self.play(Transform(f,T('F155A',28,ORANGE).move_to(f)),Transform(l,T('L158A',28,ORANGE).move_to(l)),run_time=.4)
        self.at('gained responses'); target=T('mutants: response\ncAMP rises ↑',30,GREEN).move_to(status)
        self.play(FadeOut(status),run_time=.15)
        self.play(chain.animate.set_opacity(1),FadeIn(target),run_time=.3)
        self.at('fatty acids'); self.play(FadeIn(T('assay result; pocket geometry not inferred',26).move_to([0,-3.1,0])),run_time=.35); self.finish()

class S12(SpokenScene):
    def construct(self):
        base,c,ax=graph(); base[6][1].set_opacity(0); self.add(base,c[0],head('Simply a better receptor?').move_to([0,3.0,0]))
        self.at('Take the mutant'); self.play(base[6][1].animate.set_opacity(1),run_time=.35)
        self.at('give it propionate'); self.play(Indicate(base[4],color=YELLOW),run_time=.45); self.finish()

class S13(SpokenScene):
    def construct(self):
        base,c,ax=graph(cursor_ticks=True); self.add(base,c[0])
        half=DashedLine(ax.c2p(-2,.5),ax.c2p(2,.5),color=GREY)
        definition=T('EC50: half-max dose',28).move_to([2.6,.8,0]); self.at('dose giving'); self.play(Create(half),FadeIn(definition),run_time=.4)
        self.at('At the wild type'); self.play(FadeIn(readings(ax)),FadeOut(definition),run_time=.5)
        self.at('what fraction'); self.play(FadeIn(T('At the WT EC50, what fraction does F155A give?',28).move_to([0,3,0])),run_time=.35); self.finish()

class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question_frame())
        text=T('Pause: predict',28,YELLOW).move_to([2.8,-.8,0]); track=Rectangle(width=4.4,height=.22,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([2.8,-1.25,0]); bar=Rectangle(width=4.4,height=.22,color=YELLOW,fill_color=YELLOW,fill_opacity=1).move_to(track); self.add(text,track,bar)
        self.play(bar.animate.stretch(.001,0,about_point=bar.get_left()),run_time=5,rate_func=linear)

class S15(SpokenScene):
    def construct(self):
        q=question_frame(); self.add(q)
        self.at('about 6'); a=question_frame(True); self.play(Transform(q,a),run_time=.6)
        self.at('its EC50'); self.play(Transform(q,question_frame(True,True)),run_time=.55); self.finish()

class S16Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question_frame(True,True)); self.wait(2.5)

class S17(SpokenScene):
    def construct(self):
        # Retain the quantitative graph; add the complementary assay result beside a pocket.
        ax=Axes(x_range=[-2,2,1],y_range=[0,1,.5],x_length=5.0,y_length=3.8,tips=False,axis_config={'include_ticks':False,'color':GREY}).move_to([-3,.1,0])
        ax.y_axis.set_opacity(0)
        c=VGroup(*[ax.plot(lambda x,k=k:10**x/(k+10**x),x_range=[-2,2,.02],color=col,stroke_width=4) for k,col in [(.824,BLUE),(12.3,ORANGE)]])
        self.add(ax,c,Line(ax.c2p(-2,0),ax.c2p(-2,1),color=GREY),T('propionate • model',28,YELLOW).move_to([-3,2.5,0]))
        for x,v in [(-2,'0.01'),(0,'1'),(2,'100')]: self.add(M(v,26).next_to(ax.c2p(x,0),DOWN,buff=.15))
        for y,v in [(0,'0'),(.5,'0.5'),(1,'1')]: self.add(M(v,26).next_to(ax.c2p(-2,y),LEFT,buff=.15).shift(UP*.12 if y==0 else UP*0))
        self.add(T('dose (mM)',26).move_to([-3,-2.55,0]),T('MODEL: Hill 1 • baseline 0 • own max 1',26).move_to([0,-3.4,0]))
        legend=VGroup(T('wild type',24,BLUE),T('F155A',24,ORANGE)).arrange(DOWN,aligned_edge=LEFT,buff=.12).move_to([-4.4,1.35,0]); self.add(legend)
        p=gpcr().scale(.65).move_to([3.4,.8,0]); longer=RoundedRectangle(width=.65,height=.18,corner_radius=.06,color=YELLOW,fill_color=YELLOW,fill_opacity=.6).move_to(p[1])
        self.add(p,longer,head('F155A • selectivity shift'),T('longer chain • cartoon',26,YELLOW).move_to([3.4,2.6,0]))
        baseline=Line([1.9,-1.85,0],[5.0,-1.85,0],color=GREY)
        before=Rectangle(width=.6,height=.06,color=BLUE,fill_color=BLUE,fill_opacity=.6).move_to([2.4,-1.82,0]); after=Rectangle(width=.6,height=.06,color=ORANGE,fill_color=ORANGE,fill_opacity=.6).move_to([4.4,-1.82,0])
        assay=VGroup(baseline,before,after,T('WT',24,BLUE).move_to([2.4,-2.15,0]),T('F155A',24,ORANGE).move_to([4.4,-2.15,0]))
        self.add(assay)
        self.at('lost potency'); self.play(FadeIn(T('propionate potency ↓',28,RED).move_to([-3,-2.95,0])),run_time=.4)
        self.at('gained responses'); self.play(Transform(after,Rectangle(width=.6,height=.85,color=ORANGE,fill_color=ORANGE,fill_opacity=.6).move_to([4.4,-1.425,0])),FadeIn(T('longer-chain response ↑',28,GREEN).move_to([3.2,-2.8,0])),run_time=.4)
        self.at('selectivity shifted'); self.play(Indicate(p[1],color=YELLOW),run_time=.5); self.finish()

class S18(SpokenScene):
    def construct(self):
        base,c,ax=graph(True); old=ax.plot(lambda x:10**x/(12.3/.824+10**x),x_range=[-2,2,.02],color=ORANGE,stroke_width=4)
        self.add(base,c[0],old,T('same curves; dose in units of the wild-type EC50',27).move_to([0,3,0]))
        # Separate lanes in the empty left field; arrow lengths retain the log-dose spans.
        a=ax.c2p(0,.5); b=ax.c2p(np.log10(12.3/.824),.5)
        ar=DoubleArrow([a[0]-4.8,.9,0],[b[0]-4.8,.9,0],buff=0,color=GREY)
        label=T('first table ≈ 15-fold',26,GREY).move_to([-3.15,1.3,0]); self.add(ar,label)
        self.at('A second table'); self.play(old.animate.set_stroke(opacity=.3),Create(c[1]),run_time=.5)
        self.at('a smaller one'); b2=ax.c2p(np.log10(6.5),.5)
        tag=T('second table ≈ 6.5-fold',26,YELLOW).move_to([-3.15,.05,0])
        self.play(FadeIn(DoubleArrow([a[0]-4.8,-.35,0],[b2[0]-4.8,-.35,0],buff=0,color=YELLOW)),FadeIn(tag),run_time=.45); self.finish()

class S19(SpokenScene):
    def construct(self):
        # The entire assay remains visible: EC50 belongs to the downstream response.
        names=['ligand','receptor','G protein','cAMP']; xs=[-5.2,-1.7,1.8,5.0]
        nodes=VGroup(*[chip(n,YELLOW if j==0 else (ORANGE if j==1 else TEAL),28).move_to([x,.3,0]) for j,(n,x) in enumerate(zip(names,xs))])
        links=VGroup(*[arr(nodes[j].get_right(),nodes[j+1].get_left()) for j in range(3)])
        binds=T('binds',26,YELLOW).move_to([-3.5,.9,0])
        binding=VGroup(T('binding constant',26,GREY),T('not measured',24,GREY)).arrange(DOWN,buff=.12).move_to([-1.7,-1.3,0]).set_opacity(.65)
        self.add(nodes,links,binds,binding,lead(nodes[1].get_bottom(),binding.get_top()),head('functional assay • cultured cells'))
        self.at('functional values'); mark=T('read EC50 here',28,YELLOW).move_to([4.8,-1.2,0]); self.play(FadeIn(mark),Create(lead(mark.get_top(),nodes[-1].get_bottom(),YELLOW)),run_time=.4)
        self.at('not binding constants'); self.play(FadeIn(T('functional EC50 ≠ binding constant',34,YELLOW).move_to([0,-2.6,0])),run_time=.5); self.finish()

class S20(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,1,.5],y_range=[0,1,.5],x_length=7.1,y_length=5.6,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([-2.4,-.15,0])
        # Constant assay baseline model, deliberately separated from the x axis.
        flat=ax.plot(lambda x:.14,x_range=[0,1,.01],color=TEAL,stroke_width=6)
        self.add(ax,T('dose',28).move_to([-2.4,-3.3,0]),T('response',28).rotate(PI/2).move_to([-6.35,-.15,0]),head('a flat response does not identify the cause').move_to([0,3.5,0]))
        self.at('flat response'); self.play(Create(flat),FadeIn(T('no response',28,TEAL).move_to([-2.8,-1.55,0])),run_time=.4)
        for cue,s,y in [('cannot bind','no binding?',1.8),('Coupling','no coupling?',.6),('trafficking','no trafficking?',-.6),('the assay','assay failure / ceiling?',-1.8)]:
            self.at(cue); self.play(FadeIn(T(s,28,YELLOW).move_to([3.5,y,0])),run_time=.3)
        self.finish()

class S21(SpokenScene):
    def construct(self):
        self.add(head('silence → competition → stable choice'))
        panels=[]
        for i,(x,col,name) in enumerate([(-4.25,RED,'silenced'),(0,TEAL,'competing'),(4.25,PURPLE,'locked in')]):
            g=VGroup(RoundedRectangle(width=3.75,height=5.8,corner_radius=.2,color=col,fill_color=col,fill_opacity=.07).move_to([x,-.15,0]),T(name,30,col).move_to([x,-2.4,0]))
            if i==0:
                for j in range(6):
                    t=tile(BLUE,.85).move_to([x+(j%2-.5)*1.4,1.8-(j//2)*1.25,0]); g.add(t,Line(t.get_corner(DL),t.get_corner(UR),color=RED,stroke_width=7))
            elif i==1:
                for dx,y in [(-.85,.5),(.85,.5),(0,1.9)]: g.add(Circle(radius=.65,color=TEAL).move_to([x+dx,y,0]),tile(ORANGE,.7).move_to([x+dx,y,0]))
                g.add(arr([-.8,-.5,0],[0,-1.3,0],TEAL),arr([.8,-.5,0],[0,-1.3,0],TEAL))
            else:
                g.add(tile(GREEN,1.4,.8).move_to([x,1.3,0]),lock_icon().move_to([x,-.7,0]),Arc(radius=1.1,start_angle=.2,angle=TAU-.5,color=PURPLE,stroke_width=5).add_tip(tip_length=.2).move_to([x,1.3,0]))
            panels.append(g); self.add(g)
        for cue,j in [('Silence every gene',0),('a few compete',1),('Lock in the winner',2)]:
            self.at(cue); self.play(Indicate(panels[j],color=[RED,TEAL,PURPLE][j],scale_factor=1.025),run_time=.45)
        self.finish()

class S22(SpokenScene):
    def construct(self):
        gene=chip('one gene',GREEN,28).move_to([-5,.4,0]); lock=lock_icon().scale(.55).move_to([-5,.95,0])
        rec=gpcr().scale(.55).move_to([-1.8,.5,0])
        zoom=RoundedRectangle(width=1.8,height=1.65,corner_radius=.18,color=YELLOW,fill_color=YELLOW,fill_opacity=.12).move_to([1.4,.65,0])
        leaders=VGroup(DashedLine(rec[1].get_corner(UR),zoom.get_corner(UL),color=YELLOW),DashedLine(rec[1].get_corner(DR),zoom.get_corner(DL),color=YELLOW))
        od=VGroup(RoundedRectangle(width=.85,height=.22,corner_radius=.08,color=YELLOW,fill_color=YELLOW,fill_opacity=.55).move_to([4.8,1.4,0]),Ellipse(width=.7,height=.5,color=YELLOW,fill_color=YELLOW,fill_opacity=.55).move_to([4.8,.55,0]),Triangle(color=YELLOW,fill_color=YELLOW,fill_opacity=.55).scale(.3).move_to([4.8,-.35,0]))
        labels=VGroup(T('receptor',28,ORANGE).move_to([-1.8,-1.7,0]),T('pocket zoom',28,YELLOW).move_to([1.4,-1.7,0]),T('response',28,GREEN).move_to([4.8,-1.7,0]))
        self.add(gene,lock,T('locked',26,PURPLE).move_to([-3.85,1.05,0]),head('the choice gives the neuron its pocket'))
        self.at('one receptor'); self.play(FadeIn(rec),GrowArrow(arr(gene.get_right(),rec.get_left())),FadeIn(labels[0]),run_time=.4)
        self.at("receptor's pocket"); self.play(FadeIn(zoom),Create(leaders),FadeIn(labels[1]),run_time=.4)
        self.at('which molecules'); self.play(FadeIn(od),FadeIn(T('odours',26,YELLOW).move_to([4.8,2.15,0])),GrowArrow(arr(zoom.get_right(),[4.2,.65,0],YELLOW)),run_time=.4)
        self.at('neuron responds'); self.play(FadeIn(labels[2]),FadeIn(T('the pocket sets which molecules evoke a response',30).move_to([0,-3,0])),run_time=.4); self.finish()

class S23End(EndCard):
    LINE="The chosen receptor's pocket decides which molecules the neuron responds to."
    def construct(self):
        lines=VGroup(*[T(s,38,font=TITLE_FONT) for s in ["The chosen receptor's pocket decides",'which molecules the neuron responds to.']]).arrange(DOWN,buff=.2)
        sub=T('biochemistrypedia.com',26,TEAL).move_to([0,-1.5,0]); self.play(FadeIn(lines),run_time=.6); self.play(FadeIn(sub),run_time=.4); self.finish()
