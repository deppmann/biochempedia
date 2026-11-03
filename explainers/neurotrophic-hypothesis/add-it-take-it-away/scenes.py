"""Chapter 3: Add It, Take It Away.
COLOR MAP: BLUE neurons; GREEN survival; RED loss / antiserum / blockade;
YELLOW NGF; TEAL possible births; PURPLE receptor; GREY anatomy / references.
All anatomy, populations and age windows are schematic, not measurements.
No experimental traces or molecular structures are drawn.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
GA = 2.399963

def disk_pts(n, sp, center):
    return [np.array([center[0]+sp*np.sqrt(k+.5)*np.cos(k*GA),
                      center[1]+sp*np.sqrt(k+.5)*np.sin(k*GA),0]) for k in range(n)]

def dot(p, color=BLUE, r=.24, op=.85):
    return Circle(r, color=color, fill_color=color, fill_opacity=op).move_to(p)

def ganglion(center=(0,0,0), n=16, sp=.47, radius=.25):
    return VGroup(*[dot(p,r=radius) for p in disk_pts(n,sp,center)])

def label(s,p,color=TEXT,size=28):
    return T(s,size,color).move_to(p)

def heading(s,color=TEXT):
    return T(s,34,color,font=TITLE_FONT).move_to([0,3.05,0])

def leader(a,b,color=GREY):
    return Line(a,b,color=color,stroke_width=2)

def antibody(p=(0,0,0),color=RED,width=8):
    # One continuous V on top of a stem, round caps, so the junction is clean.
    kw=dict(color=color,stroke_width=width,cap_style=CapStyleType.ROUND)
    arms=VMobject(**kw).set_points_as_corners([[-.45,.5,0],[0,0,0],[.45,.5,0]])
    arms.joint_type=LineJointType.ROUND
    stem=Line([0,-.65,0],[0,0,0],**kw)
    return VGroup(stem,arms).move_to(p)

def animal(kind='mouse',p=(0,0,0),height=3.8):
    # Closed silhouette with a separate face, ear and eye; no intersecting circles.
    pts=[[-2,-.6,0],[-2.2,.2,0],[-1.7,1,0],[-.6,1.25,0],[.7,.9,0],
         [1.3,1.1,0],[1.9,.65,0],[2.35,.1,0],[1.6,-.2,0],[.9,-.55,0],
         [.8,-.9,0],[-.1,-.9,0],[-.3,-.7,0],[-1.2,-.75,0],[-1.4,-1,0],[-2,-1,0]]
    body=VMobject(color=GREY,fill_color=GREY,fill_opacity=.16,stroke_width=4)
    body.set_points_smoothly([np.array(v) for v in pts+[pts[0]]])
    ear=Ellipse(width=.5,height=.75,color=GREY,fill_color=BG,fill_opacity=1).move_to([1.15,.95,0])
    eye=dot([1.75,.5,0],TEXT,.065)
    tail=CubicBezier(np.array([-2,-.6,0]),np.array([-3,-.5,0]),np.array([-3.1,-1.4,0]),np.array([-3.9,-.9,0]),color=GREY,stroke_width=4)
    if kind=='rabbit':
        ear.stretch(2.8,1,about_point=ear.get_bottom())
        ear2=ear.copy().shift(LEFT*.35)
        ear=VGroup(ear2,ear)
        tail=dot([-2,-.6,0],GREY,.25)
    if kind=='guinea pig':
        tail=VGroup(); ear.scale(.65)
    if kind=='rat':
        ear.scale(.65)
    return VGroup(body,ear,eye,tail).set(height=height).move_to(p)

def embryo(p=(-2,0,0),height=5):
    body=VMobject(color=GREY,stroke_width=16)
    body.set_points_smoothly([np.array(v) for v in [[.6,1.4,0],[-.5,1.5,0],[-1.2,.8,0],[-1.3,-.4,0],[-.6,-1.4,0],[.4,-1.2,0],[.65,-.5,0]]])
    head=Ellipse(width=1.15,height=1.4,color=GREY,fill_color=BG,fill_opacity=1).move_to([.7,1.3,0])
    eye=dot([.95,1.5,0],GREY,.08)
    return VGroup(body,head,eye).set(height=height).move_to(p)

def syringe(color=YELLOW):
    barrel=Rectangle(width=1.2,height=.5,color=color,fill_color=color,fill_opacity=.3)
    needle=Line([.6,0,0],[1.5,0,0],color=color,stroke_width=3)
    plunger=VGroup(Line([-1.2,0,0],[-.6,0,0],color=color,stroke_width=5),Line([-1.2,-.35,0],[-1.2,.35,0],color=color,stroke_width=5))
    return VGroup(barrel,needle,plunger)

def _chain_raw(n=7,sp=.2,r=.16,dy=1.45):
    nodes=VGroup(*[ganglion([0,y,0],n,sp,r) for y in [-dy,0,dy]])
    cord=Line([0,-dy-.35,0],[0,dy+.35,0],color=BLUE,stroke_width=3)
    return VGroup(cord,nodes)

CHAIN_H=_chain_raw().height

def chain(p=(0,0,0),height=4.3,grown=False):
    """Sympathetic chain. grown=True: same dot size and scale, more dots, wider nodes, wider spacing."""
    s=height/CHAIN_H
    g=_chain_raw(11,.3,.14,1.95) if grown else _chain_raw()
    return g.scale(s).move_to(p)

def ghost(g):
    return g.copy().set_color(GREY).set_fill(opacity=0).set_stroke(opacity=.4,width=2)

def damaged(g,keep=2):
    result=g.copy()
    for i,d in enumerate(result):
        if i>=keep: d.scale(.22).set_color(RED).set_opacity(.4)
    return result

def result_stage(done=True,caption=True):
    c=chain([-2.5,.15,0]); ref=ghost(c)
    if done:
        c[0].set_opacity(.15)
        for cluster in c[1]:
            for d in cluster: d.scale(.2).set_color(RED).set_opacity(.4)
    labs=VGroup(heading('Necessity',RED),label('Sympathetic ganglia',[1.6,1.5,0],BLUE,32),
        label('Newborn mouse + antiserum',[1.6,.65,0],RED,28),
        label('Original size',[-4.6,-2.45,0],GREY,26),leader([-4,-2.1,0],[-3,-1.5,0]))
    cap=label('Immunosympathectomy',[1.4,-1.5,0],RED,32)
    return VGroup(ref,c,labs,cap if caption else VGroup())

def age_stage(question=True):
    left=ganglion([-3,.25,0],16,.43,.25)
    right=ganglion([3,.25,0],16,.43,.25)
    refs=VGroup(ghost(left),ghost(right))
    left=damaged(left,1)
    line=Line([-4.8,-2.1,0],[4.8,-2.1,0],color=GREY,stroke_width=4)
    knob=Triangle(color=YELLOW,fill_color=YELLOW,fill_opacity=1).scale(.18).rotate(PI).move_to([4.7,-1.8,0])
    texts=VGroup(label('Newborn',[-3,-2.7,0]),label('Older',[3,-2.7,0]),label('Age',[0,-2.7,0],GREY,26),
        label('Sympathetic ganglia',[0,2.1,0],BLUE,30),label('Same antiserum',[0,-3.3,0],RED,26))
    q=heading('Same effect?' if question else 'Much less effect')
    return VGroup(refs,left,right,line,knob,texts,q)

def windows(full=True):
    """Returns dict of parts. full=True builds every piece (for the end beat)."""
    axis=Arrow([-5.5,-1.9,0],[5.6,-1.9,0],buff=0,color=GREY)
    axlabels=VGroup(label('Earlier',[-4.7,-2.45,0],GREY),label('Birth',[1.6,-2.45,0],GREY),
        label('Age',[5,-2.45,0],GREY),label('Schematic, no dates',[0,-3.15,0],GREY,26))
    tick=Line([1.6,-2.05,0],[1.6,-1.75,0],color=GREY)
    def bar(x,y,w,text):
        r=RoundedRectangle(width=w,height=1,corner_radius=.12,color=YELLOW,fill_color=YELLOW,fill_opacity=.18).move_to([x,y,0])
        return VGroup(r,label(text,[x,y,0],BLUE,25))
    sensory=bar(-2.6,.15,5.6,'NGF-dependent sensory' if full else 'Sensory')
    sym=bar(1.6,-1.0,4.4,'Sympathetic')
    hit=label('Antiserum destroys neurons here',[0,1.55,0],RED,28)
    return dict(axis=axis,axlabels=axlabels,tick=tick,sensory=sensory,sym=sym,hit=hit)

def windows_all():
    w=windows()
    return VGroup(*w.values())

class S00Title(TitleCard):
    LESSON='The Neurotrophic Hypothesis Tested'
    TITLE='Add It, Take It Away'

class S01Q(SpokenScene):
    def construct(self):
        g=ganglion(n=18,sp=.51,radius=.3)
        self.add(g,label('Ganglion',[0,2.8,0],BLUE,36),label('Neurons',[-4.4,-1.5,0],BLUE),leader([-3.4,-1.5,0],g[17].get_left()))
        self.at('a protein')
        protein=chip('Protein',YELLOW,30).move_to([-4.3,1.3,0])
        self.play(FadeIn(protein),run_time=.4)
        self.at('You add it')
        # The protein chip drops onto the + sign of the add-it chip.
        add=chip('+  Add it',YELLOW,30).move_to([-4.3,0,0])
        plus_x=add[1][0].get_center()[0]
        self.play(FadeIn(add),protein.animate.move_to([plus_x,1.2,0]),run_time=.5)
        self.play(Create(Arrow([plus_x,.8,0],[plus_x,.45,0],buff=0,color=YELLOW,stroke_width=5,tip_length=.17)),run_time=.3)
        self.at('you take it away')
        self.play(FadeIn(chip('−  Take it away',RED,28).move_to([4.3,0,0])),run_time=.4)
        self.at('Each test')
        self.play(FadeIn(label('Each test shows something different',[0,-3.25,0],GREY,27)),run_time=.4)
        self.finish()

class S02Found(SpokenScene):
    def construct(self):
        chick=embryo([-3,.2,0],5)
        tumour=Circle(.48,color=GREY,fill_color=GREY,fill_opacity=.7).move_to([-2,-.7,0])
        tube_body=RoundedRectangle(width=1.5,height=3,corner_radius=.3,color=GREY).move_to([3.7,0,0])
        self.add(chick,label('Chick embryo',[-3,3.1,0],GREY,30))
        self.at('grafted into')
        self.play(FadeIn(tumour),FadeIn(label('Mouse tumour',[.35,-.7,0],GREY,28)),Create(leader([-1.5,-.7,0],[-.95,-.7,0])),run_time=.5)
        self.at('drew in')
        fibres=VGroup(*[CubicBezier(np.array([-4,y,0]),np.array([-3.3,y+.45,0]),np.array([-2.5,-.1,0]),np.array([-2.2,-.6,0]),color=BLUE,stroke_width=4) for y in [-1.4,-.6,.2,1]])
        self.play(Create(fibres),run_time=.7)
        self.at('sensory and sympathetic')
        self.play(FadeIn(label('Sensory + sympathetic fibres',[-2.7,-3,0],BLUE,27)),run_time=.4)
        self.play(FadeIn(tube_body),run_time=.5)
        self.at('Stanley Cohen')
        self.play(FadeIn(label('Stanley Cohen',[3.7,2.1,0],GREY,26)),run_time=.35)
        self.at('purified the activity')
        fill=Rectangle(width=1.3,height=1.25,color=YELLOW,fill_color=YELLOW,fill_opacity=.4).move_to([3.7,-.4,0])
        self.play(FadeIn(fill),FadeIn(label('Purified protein',[3.7,-2.1,0],YELLOW,30)),run_time=.6)
        self.finish()

class S03Q2(SpokenScene):
    def construct(self):
        self.add(animal(p=(0,-.6,0),height=4.5))
        self.at('The question here')
        self.play(FadeIn(T('What does the protein do\nin a normal animal?',36,font=TITLE_FONT,line_spacing=1.1).move_to([0,2.6,0])),run_time=.5)
        self.finish()

def definition(title,body,x):
    color=YELLOW if title=='Sufficient' else RED
    box=RoundedRectangle(width=5.9,height=6.6,corner_radius=.2,color=color,fill_color=color,fill_opacity=.05).move_to([x,0,0])
    name=T(title,42,color)
    # align the first (capital) letter's baseline so both headings sit at the same height
    name.shift(RIGHT*(x-name.get_center()[0])+UP*(2.2-name[0].get_bottom()[1]))
    text=VGroup(*[T(l,34) for l in body.split('\n')]).arrange(DOWN,buff=.22).move_to([x,.5,0])
    diagram=VGroup(chip('+ NGF' if title=='Sufficient' else '− NGF',color,30),T('→',34),T('Effect' if title=='Sufficient' else 'No effect',30)).arrange(RIGHT,buff=.2).move_to([x,-1.8,0])
    return VGroup(box,name,text,diagram)

class S04Suff(SpokenScene):
    def construct(self):
        d=definition('Sufficient','Enough by itself\nto produce an effect',-3.1)
        self.add(d[0],d[1],d[2])
        self.at('enough by itself')
        self.play(FadeIn(d[3]),run_time=.6)
        self.finish()

class S05Nec(SpokenScene):
    def construct(self):
        a=definition('Sufficient','Enough by itself\nto produce an effect',-3.1)
        b=definition('Necessary','No effect\nwithout it',3.1)
        self.add(a,b[0],b[1],b[2])
        self.at('the effect does not happen')
        self.play(FadeIn(b[3]),run_time=.6)
        self.at('Each experiment')
        self.play(Indicate(a[0],scale_factor=1.01),Indicate(b[0],scale_factor=1.01),run_time=.6)
        self.finish()

class S06Add(SpokenScene):
    def construct(self):
        mouse=animal(p=(1,-.2,0),height=4.2)
        inj=syringe().move_to([-4.7,.1,0])
        self.add(mouse,heading('Sufficiency',YELLOW))
        self.at('In 1960')
        self.play(FadeIn(label('Levi-Montalcini & Booker · 1960',[0,-3.15,0],GREY,27)),run_time=.5)
        self.at('gave the purified protein')
        self.play(FadeIn(inj),FadeIn(label('Young mouse',[1,-2.6,0],GREY,29)),FadeIn(chip('+ purified protein',YELLOW,28).move_to([-3.8,1.8,0])),run_time=.4)
        self.play(inj.animate.shift(RIGHT*2.4),run_time=.65)
        self.play(inj[2].animate.shift(RIGHT*.45),FadeIn(dot([-1.1,.1,0],YELLOW,.12)),run_time=.4)
        self.finish()

class S07Big(SpokenScene):
    def construct(self):
        mouse=animal(p=(-1,-.3,0),height=3.6).set_stroke(opacity=.35)
        c=chain([-1,-.3,0],3.3); ref=ghost(c); ref.set_stroke(opacity=.55,width=3)
        big=chain([-1,-.3,0],3.3,grown=True)
        self.add(heading('Sufficiency',YELLOW),mouse,c,ref,label('Young mouse',[-4.7,2.2,0],GREY,30),label('Normal size',[-4.7,-2.6,0],GREY,28),leader([-3.5,-2.35,0],[-1.7,-1.9,0]))
        self.at('greatly enlarged')
        self.play(Transform(c[1],big[1]),Transform(c[0],big[0]),FadeIn(label('Sympathetic ganglia:\ngreatly enlarged',[4.6,1.9,0],BLUE,30)),run_time=.9)
        self.at('Injected into chick embryos')
        old=list(self.mobjects)[1:]
        chick=embryo([-3,0,0],4.5)
        sensory=ganglion([-.2,.2,0],9,.26,.18)
        sym=chain([2,-.4,0],3.1)
        refs=VGroup(ghost(sensory),ghost(sym))
        self.play(*[FadeOut(m) for m in old],FadeIn(chick),FadeIn(sensory),FadeIn(sym),FadeIn(refs),FadeIn(label('Chick embryo',[-3,-2.9,0],GREY,28)),run_time=.5)
        self.at('sensory and sympathetic')
        labs=VGroup(label('Sensory ganglia',[.8,2.15,0],BLUE,28),leader([.8,1.85,0],[-.5,1.55,0]),label('Sympathetic\nganglia',[4.7,.1,0],BLUE,27),leader([3.4,.1,0],[2.7,.1,0]))
        self.play(FadeIn(labs),run_time=.4)
        self.at('overgrow')
        sensory_big=ganglion([-.2,.2,0],15,.3,.18)
        sym_big=chain([2,-.4,0],3.1*1.0,grown=True)
        self.play(Transform(sensory,sensory_big),Transform(sym[1],sym_big[1]),Transform(sym[0],sym_big[0]),run_time=.8)
        self.finish()

class S08Limit(SpokenScene):
    def construct(self):
        C=[0,-.15,0]
        # Normal-size ganglion (10 neurons) and the grown one (same neurons spread 1.4x wider, plus new dots).
        normal=disk_pts(10,.34,C)
        grown_pts=disk_pts(17,.34*1.4,C)
        r_n,r_g=.2,.28
        ghost_dots=VGroup(*[Circle(r_n,color=GREY,stroke_width=3).move_to(p).set_stroke(opacity=.7) for p in normal])
        ring=DashedVMobject(Circle(1.45,color=GREY,stroke_width=4).move_to(C),num_dashes=36)
        g=VGroup(*[dot(p,r=r_g) for p in grown_pts])
        extra=[g[i] for i in range(10,17)]
        new=max(extra,key=lambda d:d.get_center()[0]); g.remove(new)
        orig=[d for d in g if any(np.allclose(d.get_center(),p) for p in grown_pts[:10])]
        saved=min(orig,key=lambda d:d.get_center()[0])
        far=max([d for d in g if d is not saved],key=lambda d:d.get_center()[0]*.6-d.get_center()[1])
        self.add(heading('A bigger ganglion'),ring,ghost_dots)
        self.at('bigger ganglion')
        self.play(FadeIn(g),run_time=.8)
        self.bring_to_front(ring,ghost_dots)
        ring_pt=np.array([C[0]+1.45*np.cos(PI*1.25),C[1]+1.45*np.sin(PI*1.25),0])
        self.play(FadeIn(label('Normal size',[-4.6,-2.45,0],GREY,28)),Create(leader([-3.5,-2.3,0],ring_pt)),
                  FadeIn(label('Enlarged ganglion',[4.3,-2.2,0],BLUE,28)),Create(leader([2.8,-2.2,0],far.get_right()+RIGHT*.05,BLUE)),run_time=.5)
        self.at('neurons were saved')
        self.play(Indicate(saved,color=BLUE),FadeIn(label('Saved?',[-4.5,1.5,0],BLUE,36)),Create(leader([-3.6,1.2,0],saved.get_left(),BLUE)),run_time=.5)
        self.at('or born')
        self.play(FadeIn(new),FadeIn(label('Born?',[4.5,1.5,0],TEAL,36)),Create(leader([3.6,1.2,0],new.get_right(),TEAL)),run_time=.5)
        self.at('needs counts')
        count=VGroup(*[Line([x,-3.3,0],[x,-2.8,0],color=TEXT) for x in [2.5,2.7,2.9,3.1]])
        self.play(FadeIn(label('Needs counts',[-.7,-3.05,0],TEXT,36)),FadeIn(count),Create(leader([1.5,-3.05,0],[2.3,-3.05,0])),run_time=.4)
        self.finish()

class S09Anti(SpokenScene):
    def construct(self):
        dish=Ellipse(width=11.3,height=5.7,color=GREY).move_to([0,-.3,0])
        ngfs=VGroup(*[chip('NGF',YELLOW,28).move_to([x,.6,0]) for x in [-3.6,-.2,3.2]])
        cells=VGroup(*[dot([x,-1.2,0],r=.3) for x in [-3.6,-.2,3.2]])
        fibres=VGroup(*[CubicBezier(np.array([x,-1,0]),np.array([x-.6,-.6,0]),np.array([x+.6,-.2,0]),np.array([x,.1,0]),color=BLUE,stroke_width=4) for x in [-3.6,-.2,3.2]])
        self.add(heading('Necessity',RED),dish,label('Culture dish',[-4.2,2.3,0],GREY,28),ngfs,cells,fibres)
        self.at('raised an')
        self.play(Create(fibres),run_time=.5)
        self.at('serum containing antibodies')
        abs=VGroup(*[antibody([x,1.0,0]).scale(.65) for x in [-2.45,.95,4.35]])
        self.play(FadeIn(abs),FadeIn(label('Antiserum',[0,2.25,0],RED,28)),run_time=.5)
        self.at('against one molecule')
        self.play(*[a.animate.shift(DOWN*.4) for a in abs],run_time=.65)
        self.at('It blocked')
        self.play(fibres.animate.set_color(GREY).set_stroke(opacity=.3).set_fill(opacity=0),FadeIn(label('Activity blocked',[0,-2.3,0],RED,32)),run_time=.6)
        self.finish()

class S10Inject(SpokenScene):
    def construct(self):
        mouse=animal(p=(-2.0,-.1,0),height=4.1)
        flank=np.array([mouse[0].get_left()[0]+.3,mouse[0].get_center()[1]+.25,0])
        inj=syringe(RED).scale(.7)
        inj.shift(flank+LEFT*1.0-inj[1].get_end())   # needle tip 1.6 left of the flank
        comparison=VGroup(animal('rat',(5.3,1.55,0),1.15),animal('rabbit',(5.3,-.35,0),1.7),animal('guinea pig',(5.3,-2.2,0),1.1))
        self.add(mouse,heading('Antiserum',RED),label('Newborn mouse',[-1.9,-2.75,0],GREY,30),comparison.set_opacity(.35),label('Comparison',[5.2,2.8,0],GREY,28))
        self.at('injected it into')
        self.play(FadeIn(inj),run_time=.3)
        self.play(inj.animate.shift(RIGHT*1.0),run_time=.5)
        plunge=inj[2].animate.shift(RIGHT*.45)
        drip=VGroup(*[Circle(.07,color=RED,fill_color=RED,fill_opacity=.9).move_to(flank+np.array([dx,-.2-dy,0])) for dx,dy in [(.0,0),(.12,.28),(-.1,.5)]])
        self.play(plunge,FadeIn(drip),run_time=.4)
        self.at('with rats')
        self.play(comparison[0].animate.set_opacity(1),FadeIn(label('Rat',[5.3,.8,0],GREY,26)),run_time=.3)
        self.at('other mammals')
        self.play(comparison[1:].animate.set_opacity(1),FadeIn(label('Rabbit',[5.3,-1.45,0],GREY,26)),FadeIn(label('Guinea pig',[5.3,-3.0,0],GREY,26)),run_time=.4)
        self.finish()

class S11Result(SpokenScene):
    def construct(self):
        s=result_stage(False,False); self.add(s)
        self.at('were destroyed')
        target=result_stage(True,False)[1]
        self.play(Transform(s[1],target),run_time=2.5)
        self.at('became known as')
        self.play(FadeIn(result_stage()[3]),run_time=.5)
        self.finish()

class S12Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(result_stage()); self.wait(3)

class S13Predict(SpokenScene):
    def construct(self):
        s=age_stage(); s[4].shift(LEFT*9.4)
        # Newborn baseline and its damage use the same population as the older comparison.
        healthy=ganglion([-3,.25,0],16,.43,.25)
        pred=heading('Predict')
        self.add(s[0],healthy,s[3],s[4],s[5],pred)
        self.at('Give the same')
        self.play(Transform(healthy,s[1]),run_time=.8)
        self.at('older animals')
        self.play(s[4].animate.shift(RIGHT*9.4),FadeIn(s[2]),run_time=.7)
        self.at('Does it destroy')
        self.play(FadeOut(pred),FadeIn(s[6]),run_time=.4)
        self.finish()

class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(age_stage()); self.wait(5)

class S15Reveal(SpokenScene):
    def construct(self):
        s=age_stage(); self.add(s)
        self.at('much less effect')
        self.play(FadeOut(s[6]),Transform(s[2],damaged(s[2],14)),run_time=.4)
        self.play(FadeIn(heading('Much less effect')),run_time=.35)
        self.at('a developmental window')
        self.play(FadeOut(s[5][3]),run_time=.2)
        self.play(FadeIn(label('A window of dependence',[0,2.1,0],YELLOW,27)),run_time=.2)
        self.finish()

class S16Window(SpokenScene):
    def construct(self):
        w=windows(False)
        self.add(heading('Windows of dependence'),w['axis'],w['axlabels'],w['tick'],w['sym'])
        self.at('differs between populations')
        self.play(Indicate(w['sym'],scale_factor=1.03),FadeIn(w['sensory']),run_time=.6)
        self.at('NGF dependent sensory')
        full=windows()['sensory']
        self.play(Transform(w['sensory'][1],full[1]),run_time=.4)
        self.play(Indicate(w['sensory'],scale_factor=1.03),run_time=.5)
        self.at('earlier exposure')
        self.play(FadeIn(w['hit']),run_time=.5)
        self.finish()

class S17Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(heading('Windows of dependence'),windows_all()); self.wait(3)

class S18Doubt(SpokenScene):
    def construct(self):
        ngf=chip('NGF',YELLOW,38).move_to([-4,1.2,0])
        ab=antibody([-2.5,1.2,0])
        neuron=Circle(1.8,color=BLUE,fill_color=BLUE,fill_opacity=.16).move_to([1.8,-.7,0])
        other=Square(.65,color=PURPLE,fill_color=PURPLE,fill_opacity=.4).move_to([1.8,1.1,0])
        self.add(heading('The specificity doubt',RED),ngf,ab,neuron,label('Neuron',[1.8,-2.95,0],BLUE,30))
        self.at('carries a doubt')
        self.play(FadeIn(label('Possible off-target harm',[-3.3,-1.1,0],RED,27)),run_time=.4)
        self.at('might kill neurons')
        self.play(FadeIn(other),run_time=.35)
        self.at('binding something on them')
        self.play(ab.animate.move_to([1.8,1.9,0]),run_time=.65)
        self.play(neuron.animate.set_color(RED).set_fill(RED,opacity=.3),run_time=.4)
        self.at('other than')
        self.play(FadeIn(label('Other surface\ntarget?',[4.8,1.2,0],TEXT,30)),Create(leader([3.5,1.2,0],[2.2,1.1,0],PURPLE)),run_time=.4)
        self.finish()

class S19Q(SpokenScene):
    def construct(self):
        ngf=chip('NGF',YELLOW,60).scale(1.35).move_to([-2.9,-.9,0])
        ab=antibody([2.6,-.7,0],GREY,10).scale(2.1)
        ab_lab=label('Antibody',[2.6,-3.2,0],GREY,32)
        self.add(ngf,ab,ab_lab)
        self.at('how would you remove')
        q=T('Remove NGF\nwith no antibody?',44,font=TITLE_FONT,line_spacing=1.1).move_to([0,2.1,0])
        self.play(FadeIn(q),run_time=.5)
        self.at('without using an antibody')
        r=1.55
        ring=Circle(r,color=RED,stroke_width=10).move_to(ab.get_center())
        slash=Line(ab.get_center()+r*np.array([-.707,.707,0]),ab.get_center()+r*np.array([.707,-.707,0]),color=RED,stroke_width=10)
        self.play(Create(ring),Create(slash),run_time=.6)
        self.finish()

class S20Take(SpokenScene):
    def construct(self):
        self.add(heading('Add it. Take it away.'))
        top=RoundedRectangle(width=11.8,height=2.1,corner_radius=.2,color=YELLOW).move_to([0,1,0])
        bottom=RoundedRectangle(width=11.8,height=2.1,corner_radius=.2,color=RED).move_to([0,-1.6,0])
        self.add(top,bottom)
        self.at('adding')
        self.play(FadeIn(label('+ NGF',[-4.3,1.25,0],YELLOW,32)),run_time=.35)
        self.at('enough to enlarge')
        self.play(FadeIn(label('Enough to enlarge the ganglia',[1.1,1.3,0],TEXT,29)),FadeIn(label('Saved or born? Still open.',[1.1,.5,0],GREY,26)),run_time=.5)
        self.at('Taking it away')
        self.play(FadeIn(label('− NGF',[-4.3,-1.4,0],RED,32)),run_time=.35)
        self.at('it is necessary')
        self.play(FadeIn(label('Necessary',[1.1,-1.3,0],TEXT,32)),run_time=.35)
        self.at('if the antibody')
        self.play(FadeIn(label('If the antibody is clean',[1.1,-2.1,0],RED,28)),run_time=.35)
        self.finish()

class S21Next(SpokenScene):
    def construct(self):
        bar=Line([-5,0,0],[5,0,0],color=GREY,stroke_width=6)
        blocks=VGroup(*[Rectangle(width=1.2,height=1,color=GREY,fill_color=GREY,fill_opacity=.45).move_to([x,0,0]) for x in [-3.5,-1.1,1.5,3.6]])
        self.add(heading('Genetics'),bar,blocks,label('Ngf gene',[0,1.5,0],YELLOW,36))
        self.at('Settling that doubt')
        self.play(Indicate(blocks,scale_factor=1.02),run_time=.35)
        self.at('took genetics')
        self.play(Create(Cross(blocks[1],stroke_color=RED,stroke_width=8)),FadeIn(label('Delete the gene, no antibody needed',[0,-1.7,0],TEXT,32)),run_time=.5)
        self.finish()
        self.wait(2.1)  # Readable silent tail; renderer pads audio without touching script.

class S22End(EndCard):
    LINE='Add NGF: ganglia grow. Remove it: necessary, if the antibody is clean.'
    def construct(self):
        # The complete result is present from the first frame: no black inter-card gap.
        self.add(heading('Add it. Take it away.'))
        self.add(label('Add NGF → ganglia grow',[0,1.3,0],YELLOW,38),
                 label('Remove NGF → needed for survival',[0,0,0],TEXT,34),
                 label('Necessity, if the antibody is clean',[0,-1.3,0],RED,32),
                 label('biochemistrypedia.com',[0,-3,0],TEAL,26))
        self.wait(self.narration_s+.4)
