"""Chapter 6: Where the Rule Stops.
COLOR MAP: GREY uncommitted ectoderm/anatomy; BLUE neural; ORANGE skin;
YELLOW BMP/Smad1; GREEN Noggin/Chordin; TEAL FGF; PURPLE posterior identity;
PINK receptor; TEXT competence/Wnt/position. Schematics, no quantitative traces.
"""
import numpy as np
from bp_style import *
ORANGE = '#F29E4C'
PURPLE = '#B58CD9'
PINK = '#E58AC0'


def label(s, x=0, y=0, size=42, color=TEXT):
    return T(s, size=size, color=color).move_to([x,y,0])


def header(s):
    return label(s,y=3.35,size=42)


def box(s,x=0,y=0,color=TEXT,size=40):
    return chip(s,color,size).move_to([x,y,0])


def arrow(a,b,color=TEXT):
    return Arrow(a,b,buff=.12,color=color,stroke_width=5,max_tip_length_to_length_ratio=.3)


def cell(x,y,r=.5,color=GREY):
    return Circle(r,stroke_color=color,fill_color=color,fill_opacity=.3,stroke_width=4).move_to([x,y,0])


def paint(c,color):
    return c.animate.set_stroke(color).set_fill(color,.35)


def bar(colored=False,tall=False,cy=None):
    xs=[-3.8,0,3.8]
    h=4.2 if tall else 2.4
    if cy is None: cy=.15 if tall else .8
    ey=cy+h/2+.5
    boxes=VGroup(*[RoundedRectangle(width=3.55,height=h,corner_radius=.15,
        color=BLUE if colored and i==0 else GREY,fill_opacity=.18,
        fill_color=BLUE if colored and i==0 else GREY).move_to([x,cy,0]) for i,x in enumerate(xs)])
    ny=cy+h/2-.55 if tall else cy+.1
    names=VGroup(*[label(s,x,ny,40,BLUE if colored and i==0 else TEXT) for i,(x,s) in enumerate(zip(xs,['forebrain','hindbrain','spinal cord']))])
    ends=VGroup(label('HEAD',-5.1,ey),label('TAIL',5.1,ey),arrow([-3.9,ey,0],[3.9,ey,0]))
    return VGroup(boxes,names,ends)


def cement_chip(x=-4.3,y=-2.55):
    c=chip('cement gland',TEXT,32,pad=.14,fill_opacity=.3)
    c[0].set_stroke(GREY,3)
    return c.move_to([x,y,0])


def activation():
    b=bar(True)
    # Source arrow rises under the forebrain box; Noggin and Chordin chips sit on it in S06.
    start=box('ectoderm',-3.8,-3.35,GREY,34)
    act=arrow([-3.8,-2.95,0],[-3.8,-.42,0],GREEN)
    txt=label('activation',-1.1,-1.75,color=GREEN)
    trans=arrow([.1,-1.0,0],[5.7,-1.0,0],PURPLE)
    return VGroup(header('Activation → transformation'),b,start,act,txt,trans)


def epiblast():
    disc=Ellipse(width=12.4,height=5.55,color=GREY,fill_color=GREY,fill_opacity=.08).move_to([0,-.15,0])
    plate=Ellipse(width=3.4,height=3.7,color=BLUE,stroke_width=4).move_to([-3.4,-.15,0])
    name=label('future\nneural plate',-3.4,-.2,size=38,color=BLUE)
    return VGroup(disc,plate,name)


CH_POS=[(.0,.55),(1.55,.55),(.78,-.85)]


def chordin_cells():
    return VGroup(*[cell(x,y,.7) for x,y in CH_POS])


def exp_marks():
    cells=chordin_cells()
    xs=VGroup()
    for x,y in CH_POS:
        for a,b in [((-.33,.33),(.33,-.33)),((-.33,-.33),(.33,.33))]:
            xs.add(Line([x+a[0],y+a[1],0],[x+b[0],y+b[1],0],color=TEXT,stroke_width=7))
    tag=label('no neural\nmarkers',4.3,.2,size=40)
    return VGroup(xs,tag)


def experiment(result=False):
    e=epiblast()
    cells=chordin_cells()
    ch=label('Chordin cells',.78,1.75,color=GREEN)
    if result:
        mark=exp_marks(); out=label('not sufficient',3.1,-1.5,size=40)
    else:
        mark=label('?',3.6,-.15,size=84); out=label('Do those cells turn neural?',y=-3.35)
    return VGroup(header('1998 · Stern laboratory · chick'),e,cells,ch,mark,out)


def dial(high=True,s=1.0,cx=-3.1,cy=-.2,labels=True):
    c=np.array([cx,cy,0])
    sz=lambda n: max(28,n*s)
    ring=Circle(2.25*s,color=GREY,stroke_width=4).move_to(c)
    arc=Arc(radius=2*s,start_angle=PI/6,angle=2*PI/3,color=YELLOW,stroke_width=11).move_arc_center_to(c)
    needle=Line(c,c+np.array([1.65*s if high else -1.65*s,.95*s,0]),color=YELLOW,stroke_width=8)
    d1,d2=(.3,1.0) if s<.95 else (.45,1.2)
    g=VGroup(ring,arc,needle,Dot(c,color=YELLOW),label('Smad1',cx,cy-d1*s,size=sz(42),color=YELLOW),
        label('in the nucleus',cx,cy-d2*s,size=sz(38)))
    if labels:
        g.add(label('low · neural',cx-1.45*s,cy+2.65*s,size=sz(38),color=BLUE),
              label('high · skin',cx+1.85*s,cy+2.65*s,size=sz(38),color=ORANGE))
    return g


MX=-1.0


def mouse(tube=False,neural=False):
    # Longitudinal egg-cylinder body with an integral dashed anterior region.
    body=RoundedRectangle(width=2.9,height=6.0,corner_radius=1.2,color=GREY,
        fill_color=GREY,fill_opacity=.15).move_to([MX,-.55,0])
    cap=DashedVMobject(Ellipse(width=2.4,height=1.7,color=TEXT,stroke_width=4,fill_opacity=0).move_to([MX,1.45,0]),num_dashes=28)
    tub=RoundedRectangle(width=.55,height=3.2,corner_radius=.25,color=BLUE,
        fill_color=BLUE,fill_opacity=.55).move_to([MX,-1.1,0])
    head=label('HEAD',-3.7,1.9)
    tail=label('TAIL',-3.7,-3.0)
    defect_label=label('forebrain (missing)',4.2,1.45,size=38)
    leader=Line([1.75,1.45,0],[MX-.2,1.45,0],color=TEXT,stroke_width=4)
    return VGroup(body,cap,tub,head,tail,defect_label,leader)


class S00Title(TitleCard):
    LESSON='Neural Induction: The Default Model'
    TITLE='Where the Rule Stops'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',y=1.5,color=TEAL),label(self.TITLE,size=58),
                 label(self.LESSON,y=-1.5,size=36))
        self.finish()


class S01(SpokenScene):
    def construct(self):
        d=dial(); self.add(header('Where does the rule stop?'),d)
        node=box('skin / neural',3.6,.3)
        self.at('the dial'); self.play(FadeIn(node),GrowArrow(arrow([-.65,.3,0],[1.7,.3,0],YELLOW)),run_time=.45)
        self.at('choice between skin'); self.play(Indicate(node,color=TEXT),run_time=.45)
        self.at('in frog caps'); context=label('frog caps + embryos',3.4,2.2,size=38); self.play(FadeIn(context),run_time=.4)
        self.at('FGF is needed'); self.play(FadeIn(box('FGF-dependent input',3.3,-2,TEAL,36)),GrowArrow(arrow([3.3,-1.55,0],[3.3,-.2,0],TEAL)),run_time=.45)
        self.at('where else'); self.play(FadeIn(label('where · chick · mouse',y=-3.35,size=40)),run_time=.4)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        b=bar(tall=True); self.add(header('1 · Neural, but where?'),b)
        self.at('Noggin caps')
        cap=VGroup(Arc(radius=.35,start_angle=PI,angle=PI,color=GREEN).move_arc_center_to([-5.5,-3.4,0]),*[cell(x,-3.4,.1,GREY) for x in [-5.72,-5.5,-5.28]],label('Noggin-treated cap',-2.6,-3.45,size=36,color=GREEN))
        self.play(FadeIn(cap),run_time=.35)
        self.at('forebrain'); self.play(paint(b[0][0],BLUE),b[1][0].animate.set_color(BLUE),FadeIn(label('neural',-3.8,.95,color=BLUE)),run_time=.35)
        self.at('cement gland markers'); self.play(FadeIn(cement_chip()),FadeIn(label('non-neural · head end',-.1,-2.55,size=36)),run_time=.4)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        b=bar(True,tall=True)
        self.add(header('1 · Noggin-treated caps'),b,label('neural',-3.8,.95,color=BLUE),cement_chip(),
                 label('non-neural · head end',-.1,-2.55,size=36))
        self.at('no hindbrain'); self.play(Indicate(b[0][1],color=TEXT),run_time=.5)
        self.at('or spinal cord'); self.play(Indicate(b[0][2],color=TEXT),run_time=.5)
        self.at('cord markers'); self.play(FadeIn(label('no markers',0,.95,size=38)),FadeIn(label('no markers',3.8,.95,size=38)),run_time=.4)
        self.at('neural tissue'); self.play(Indicate(b[0][0],color=BLUE),run_time=.6)
        self.at('caps is'); self.play(FadeIn(label('anterior only',4.9,-2.55,color=BLUE)),run_time=.4)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        self.add(header('Nieuwkoop · two steps'))
        a=box('1 · activation',-3.3,.7,GREEN)
        b=box('2 · transformation',3.1,-1.3,BLUE)
        self.add(a,b,arrow([-1,.3,0],[.9,-.9,0]))
        self.at('activation'); self.play(Indicate(a,color=GREEN),run_time=.4)
        self.at('transformation'); self.play(Indicate(b,color=BLUE),run_time=.4)
        self.finish()


class S05(SpokenScene):
    def construct(self):
        a=activation(); a[1][0][0].set_color(GREY); a[1][1][0].set_color(TEXT)
        self.add(a[0],a[1],a[2],a[4])
        self.at('activation makes'); self.play(GrowArrow(a[3]),run_time=.4)
        self.at('neural and anterior'); self.play(paint(a[1][0][0],BLUE),a[1][1][0].animate.set_color(BLUE),run_time=.5)
        self.at('transformation shifts'); self.play(GrowArrow(a[5]),FadeIn(label('transformation',2.9,-1.75,color=PURPLE)),run_time=.45)
        self.at('toward hindbrain'); self.play(paint(a[1][0][1],PURPLE),a[1][1][1].animate.set_color(PURPLE),run_time=.5)
        self.at('and spinal cord'); self.play(paint(a[1][0][2],PURPLE),a[1][1][2].animate.set_color(PURPLE),run_time=.5)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        a=activation(); self.add(*a[:5])
        self.at('the BMP antagonists'); names=VGroup(chip('Noggin',GREEN,36,pad=.12).move_to([-3.8,-1.3,0]),chip('Chordin',GREEN,36,pad=.12).move_to([-3.8,-2.3,0]))
        for n in names:
            n[0].set_fill(BG,1); n[0].set_stroke(GREEN,3)
        self.play(FadeIn(names),run_time=.5)
        self.at('look like activators'); self.play(Indicate(a[3],color=GREEN),Indicate(names,color=GREEN),run_time=.6)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        b=bar(True); self.add(header('Candidates for transformation'),b)
        tail=[4.9,-.5,0]
        self.at('Wnt signals'); self.play(FadeIn(box('Wnt',-2.6,-2.95)),GrowArrow(arrow([-2.6,-2.5,0],tail)),run_time=.4)
        self.at('FgFS'); self.play(FadeIn(box('FGF',.4,-2.95,TEAL)),GrowArrow(arrow([.4,-2.5,0],tail,TEAL)),run_time=.4)
        self.at('retinoic acid'); self.play(FadeIn(box('retinoic acid',3.4,-2.95,size=36)),GrowArrow(arrow([3.4,-2.5,0],tail)),run_time=.4)
        self.at('leading candidates'); self.play(paint(b[0][1],PURPLE),paint(b[0][2],PURPLE),b[1][1].animate.set_color(PURPLE),b[1][2].animate.set_color(PURPLE),run_time=.5)
        self.finish()


class S08(SpokenScene):
    def construct(self):
        self.add(header('Mouse · spinal cord may differ'),label('TAIL · spinal cord progenitors',y=2.45,size=38))
        a=VGroup(*[cell(x,.5,.75) for x in [-4.9,-3.3,-1.7]])
        b=VGroup(*[cell(x,.5,.75) for x in [1.7,3.3,4.9]])
        self.add(a)
        l1=label('1 · posterior identity',-3.3,-1.1,size=38); l2=label('2 · neural',3.3,-1.1,size=38,color=BLUE)
        self.at('different order'); self.play(FadeIn(l1),FadeIn(l2),run_time=.4)
        self.at('may come from'); self.play(Indicate(a,color=GREY),run_time=.5)
        self.at('progenitors made'); self.play(*[paint(c,PURPLE) for c in a],l1.animate.set_color(PURPLE),run_time=.6)
        self.at('become neural'); self.play(GrowArrow(arrow([-.9,.5,0],[.9,.5,0])),TransformFromCopy(a,b),run_time=.4)
        self.play(*[paint(c,BLUE) for c in b],FadeIn(label('posterior first, neural second',y=-2.15,size=42)),run_time=.45)
        self.wait(.4)
        self.play(FadeIn(label('brain: neural first, then shifted',y=-3.2,size=38)),run_time=.4)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        e=epiblast(); self.add(header('2 · Chick epiblast'),e)
        self.at('blocking BMP anywhere')
        patches=VGroup(*[VGroup(cell(x,y,.45,YELLOW),label('BMP\nblocked',2.3,y,size=36,color=YELLOW)) for x,y in [(.5,1.5),(.5,0),(.5,-1.5)]])
        self.play(FadeIn(patches),run_time=.5)
        self.at('should make neural tissue'); self.play(FadeIn(label('Neural anywhere?',y=-3.35)),run_time=.4)
        self.finish()


class S10(SpokenScene):
    def construct(self):
        e=experiment(); self.add(e[0],e[1])
        self.at('made cordon'); self.play(FadeIn(e[2]),FadeIn(e[3]),run_time=.5)
        self.at('outside the future'); self.play(Indicate(e[2],color=GREEN),run_time=.5)
        self.at('future neural plate'); self.play(Indicate(e[1][1],color=BLUE),run_time=.5)
        self.at('do those cells'); self.play(FadeIn(e[4]),FadeIn(e[5]),run_time=.4)
        self.finish()


class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(experiment()); self.wait(5)


class S12(SpokenScene):
    def construct(self):
        e=experiment(); self.add(e)
        r=experiment(result=True)
        self.at('no'); self.play(FadeOut(e[4]),FadeOut(e[5]),run_time=.4)
        self.at('early neural markers'); self.play(FadeIn(r[4]),run_time=.5)
        self.at('blocking BMP'); self.play(Indicate(e[2],color=GREEN),run_time=.5)
        self.at('not sufficient'); self.play(FadeIn(r[5]),run_time=.4)
        self.finish()


class S13Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(experiment(result=True)); self.wait(2.5)


class S14(SpokenScene):
    def construct(self):
        self.add(header('Chick · after neural-inducing signals'),label('already received neural-inducing signals',y=2.35,size=38),
                 arrow([-.5,-2.5,0],[5.6,-2.5,0]),label('later →',2.5,-3.15,size=38))
        self.add(label('without Chordin',-3.9,.95,size=38),label('with Chordin',-3.9,-1.05,size=38,color=GREEN))
        early=VGroup(cell(-.5,.95,.56,BLUE),cell(-.5,-1.05,.56,BLUE)); self.add(early)
        self.at('did stabilize'); ch=box('Chordin',2.1,-.2,GREEN,38); self.play(FadeIn(ch),run_time=.35)
        self.at('stabilize early neural markers'); late=VGroup(cell(4.6,.95,.56,GREY),cell(4.6,-1.05,.56,BLUE))
        self.play(GrowArrow(arrow([.3,.95,0],[3.8,.95,0])),GrowArrow(arrow([.3,-1.05,0],[3.8,-1.05,0],GREEN)),FadeIn(late),run_time=.6)
        self.at('already received'); self.play(FadeOut(ch),FadeIn(label('markers persist longer',2.4,-1.85,size=36,color=BLUE)),run_time=.4)
        self.finish()


class S15(SpokenScene):
    def construct(self):
        self.add(header('2000 · Streit and colleagues · chick'))
        disc=Ellipse(width=9.6,height=3.5,color=GREY,fill_color=GREY,fill_opacity=.08).move_to([0,.3,0])
        pos=[(-2.7,.45),(-.8,-.05),(1.1,.55),(3.0,.05)]
        cells=VGroup(*[cell(x,y,.42) for x,y in pos])
        self.add(disc,cells,label('epiblast',0,2.35,size=38),arrow([-5.5,-2.7,0],[5.5,-2.7,0]),
                 label('before gastrulation',-2.7,-3.3,size=38),label('gastrulation',3.8,-3.3,size=38))
        self.at('looked earlier'); br=Line([-5.2,-2.45,0],[.7,-2.45,0],color=TEAL,stroke_width=8); self.play(Create(br),run_time=.4)
        self.at('signaling before gastrulation'); fg=box('FGF',-5.75,pos[0][1],TEAL)
        arrows=VGroup(arrow([-5.05,pos[0][1],0],[pos[0][0]-.48,pos[0][1],0],TEAL),*[arrow([x-1.5,y,0],[x-.48,y,0],TEAL) for x,y in pos[1:]])
        self.play(FadeIn(fg),LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=.2),run_time=.9)
        self.at('needed to begin'); self.play(*[paint(c,BLUE) for c in cells],run_time=.55)
        self.at('neural induction'); self.play(FadeIn(label('needed to begin neural induction',y=-1.7,size=38,color=TEAL)),run_time=.45)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        self.add(header('2001 · Wilson · Edlund laboratory'),label('epiblast cell',y=-2.8))
        c=cell(0,0,1.65); fg=box('FGF',-4.8,0,TEAL); self.add(c,fg,arrow([-4,0,0],[-1.8,0,0],TEAL))
        self.at('colleagues added'); gate=box('Wnt state A',0,2.2); self.play(FadeIn(gate),run_time=.4)
        self.at('its state decides'); neu=box('neural',5.3,1.3,BLUE); ar=arrow([1.9,.45,0],[3.85,1.05,0],BLUE)
        self.play(paint(c,BLUE),GrowArrow(ar),FadeIn(neu),run_time=.5)
        self.at('cells respond'); skin=box('epidermis\nskin',5.3,-1.3,ORANGE,36)
        self.play(Transform(gate,box('Wnt state B',0,2.2)),FadeOut(neu),FadeOut(ar),paint(c,ORANGE),GrowArrow(arrow([1.9,-.45,0],[3.85,-1.05,0],ORANGE)),FadeIn(skin),run_time=.6)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        d=dial(s=1.05,cx=-2.5,cy=-.2); node=box('skin or neural',4.5,-.2,TEXT,40)
        self.add(header('Chick · two more inputs'),d,node,arrow([0.0,-.2,0],[2.6,-.2,0],YELLOW))
        self.at('two more inputs'); self.play(Indicate(d[2],color=YELLOW),run_time=.5)
        self.at('one is early'); fg=box('early FGF',4.5,2.0,TEAL); self.play(FadeIn(fg),GrowArrow(arrow([4.5,1.55,0],[4.5,.35,0],TEAL)),run_time=.4)
        self.at('the other is'); w=box('Wnt state',4.5,-2.35); self.play(FadeIn(w),GrowArrow(arrow([4.5,-1.9,0],[4.5,-.75,0])),run_time=.4)
        self.at('lets cells answer'); self.play(FadeIn(label('cells can answer FGF',3.9,-3.4,size=36)),run_time=.4)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        m=mouse(); self.add(header('3 · Mouse embryo'),m[0],m[1],m[3],m[4])
        self.at('lacking both'); self.play(FadeIn(label('no Chordin\nno Noggin',4.2,-1.1,size=42,color=GREEN)),run_time=.4)
        self.at('severe forebrain defects'); self.play(FadeIn(m[5]),Create(m[6]),m[1].animate.set_opacity(.45),run_time=.5)
        self.finish()


class S19(SpokenScene):
    def construct(self):
        m=mouse(); m[1].set_opacity(.45)
        self.add(header('3 · Mouse · no Chordin / Noggin'),m[0],m[1],m[3],m[4],m[5],m[6])
        self.at('still form other'); self.play(FadeIn(m[2]),FadeIn(label('neural tissue\nstill forms\n(posterior)',4.2,-1.1,size=40,color=BLUE)),GrowArrow(arrow([2.2,-1.1,0],[MX+.4,-1.1,0],BLUE)),run_time=.5)
        self.at('normal forebrain'); self.play(Indicate(m[1],color=TEXT),FadeIn(label('needed for forebrain',4.2,.8,size=34)),run_time=.5)
        self.at('not for all'); self.play(Indicate(m[2],color=BLUE),run_time=.5)
        self.finish()


def summary():
    return VGroup(header('A fair summary'),box('Needed: frog neural plate',0,1.4,BLUE,48),
        box('Needed: mouse forebrain',0,-.3,BLUE,48),box('Not sufficient alone: chick epiblast',0,-2.0,TEXT,44),
        label('The frog results stand.',y=-3.3,size=44))


class S20(SpokenScene):
    def construct(self):
        s=summary(); self.add(s[0])
        self.at('inhibition is needed'); self.play(FadeIn(s[1]),run_time=.4)
        self.at('mouse forebrain'); self.play(FadeIn(s[2]),run_time=.4)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        s=summary(); self.add(*s[:3])
        self.at('not sufficient'); self.play(FadeIn(s[3]),run_time=.4)
        self.at('none of this'); self.play(FadeIn(s[4]),run_time=.4)
        self.finish()


class S22(SpokenScene):
    def construct(self):
        d=dial(s=.9,cx=.6,cy=-.2); self.add(header('Early frog caps · BMP says skin'),d)
        fate=box('skin',5.4,-.2,ORANGE); self.add(fate)
        self.at('BMP says skin'); self.play(GrowArrow(arrow([2.8,-.2,0],[4.4,-.2,0],YELLOW)),run_time=.5)
        self.at('turn its signal down')
        h1=label('outside the cell\nNoggin / Chordin',-5.0,1.65,size=32,color=GREEN)
        h2=label('at the membrane\nbroken receptor',-5.0,-.2,size=32,color=PINK)
        h3=label('inside the cell\nMAPK',-5.0,-2.1,size=32,color=TEAL)
        a1=arrow([-3.2,1.6,0],[-1.3,.9,0],GREEN); a2=arrow([-3.2,-.2,0],[-1.55,-.2,0],PINK); a3=arrow([-3.2,-2.0,0],[-1.3,-1.3,0],TEAL)
        self.play(LaggedStart(AnimationGroup(FadeIn(h1),GrowArrow(a1)),AnimationGroup(FadeIn(h2),GrowArrow(a2)),
            AnimationGroup(FadeIn(h3),GrowArrow(a3)),lag_ratio=.4),run_time=1.0)
        self.at('far enough'); self.play(Transform(d[2],dial(False,.9,.6,-.2)[2]),FadeOut(fate),run_time=.5)
        self.at('competent cells become'); self.play(FadeIn(box('neural',5.4,-.2,BLUE)),FadeIn(label('turn it down far enough → neural',y=-3.55,size=38)),run_time=.45)
        self.at('as long as other inputs'); fgb=box('FGF input\nintact',5.4,-2.3,TEAL,36); self.play(FadeIn(fgb),GrowArrow(arrow([5.4,-1.6,0],[5.4,-.75,0],TEAL)),run_time=.5)
        self.at('such as FGF'); self.play(Indicate(fgb,color=TEAL),run_time=.5)
        self.finish()


class S23(SpokenScene):
    def construct(self):
        d=dial(False,s=.76,cx=-2.7,cy=-.05,labels=False)
        self.add(label('BMP is one branch of the choice',y=3.5,size=42),d)
        node=VGroup(RoundedRectangle(width=3.4,height=1.1,color=TEXT).move_to([2.3,-.05,0]),label('skin / neural',2.3,-.05,size=40))
        self.add(node,arrow([-.85,-.05,0],[.65,-.05,0],YELLOW))
        self.at('choice between skin and neural'); self.play(Indicate(node,color=TEXT),run_time=.5)
        self.at('FGF and competence')
        inputs=VGroup(box('FGF signaling',2.3,1.75,TEAL,38),box('competence',2.3,-1.8,TEXT,38))
        self.play(FadeIn(inputs),GrowArrow(arrow([2.3,1.25,0],[2.3,.55,0],TEAL)),GrowArrow(arrow([2.3,-1.3,0],[2.3,-.65,0])),run_time=.5)
        self.at('in caps and embryos')
        self.play(FadeIn(label('BMP, FGF and competence shape skin-or-neural fate.',y=-3.45,size=36)),run_time=.4)
        self.at('where the tissue lies')
        outer=DashedVMobject(RoundedRectangle(width=12.6,height=5.3,corner_radius=.4,color=GREY))
        pos=label('where along the body',-3.0,2.2,size=36)
        self.play(Create(outer),FadeIn(pos),run_time=.5)
        self.at('how chick and mouse differ')
        tags=VGroup(label('chick',-5.3,-2.0,size=36),label('mouse',5.1,-2.0,size=36))
        self.play(FadeIn(tags),run_time=.4)
        self.finish()


class S24End(EndCard):
    LINE='BMP, FGF and competence shape the skin-or-neural choice.'
    def construct(self):
        self.add(label('BMP, FGF and competence',y=.6,size=48),label('shape the skin-or-neural choice.',y=-.5,size=48),label('biochemistrypedia.com',y=-2.1,size=36,color=TEAL))
        self.finish()
