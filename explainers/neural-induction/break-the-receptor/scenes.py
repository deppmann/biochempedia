"""Chapter 2, review revision.
COLOR MAP: GREY = epidermis/keratin and structural outlines; TEXT = uncommitted
cap outlines; ORANGE = skin labels; BLUE = neural fate/Smad; YELLOW = BMP only;
PURPLE = endoderm/organizer; ACT = activin; PINK = intact receptor; RED = jam/block;
MESO = mesoderm; PHOS = phosphate; TEXT = other ligands.
Protein cartoons are schematic blocks, never molecular structures. No traces.
"""
import numpy as np
from bp_style import *
ORANGE='#F29E4C'
PURPLE='#B58CD9'
PINK='#E58AC0'
MESO='#A5CA77'
PHOS='#F3A6DA'
ACT='#8E9CFF'   # activin: periwinkle, distinct from neural blue and teal

def cell(p, r=1.29, color=TEXT):
    return Circle(radius=r,stroke_color=color,stroke_width=3,
                  fill_color=color,fill_opacity=.02 if color==TEXT else .65).move_to(p)

def paint(c,color):
    return c.animate.set_stroke(color).set_fill(color,.65)

def grid_pos(spread=False):
    if spread:
        return [np.array([x,y,0]) for x,y in [(-4.15,1.3),(-.2,1.35),(3.95,1.3),(-3.9,-1.35),(.15,-1.35),(4.15,-1.35)]]
    return [np.array([x,y,0]) for y in (1.29,-1.29) for x in (-2.58,0,2.58)]

def cells(spread=False,color=TEXT):
    return VGroup(*[cell(p, 1.03 if spread else 1.29,color) for p in grid_pos(spread)])

def dish():
    return RoundedRectangle(width=11.8,height=5.45,corner_radius=.4,
                            color=GREY,stroke_width=2).move_to([0,-.05,0])

def heading(s,color=TEXT):
    return T(s,30,color).move_to([0,3.13,0])

def footer(s,color=TEXT):
    return T(s,28,color).move_to([0,-3.18,0])

def cap_stage(spread=False,color=TEXT):
    return VGroup(dish(),cells(spread,color))

def dimer(p=(0,2.25,0),name='BMP',size=1):
    lobes=VGroup(*[RoundedRectangle(width=.7,height=.55,corner_radius=.2,
          color=YELLOW,fill_color=YELLOW,fill_opacity=.35).shift(RIGHT*x) for x in (-.32,.32)])
    return VGroup(lobes,T(name,26,YELLOW).next_to(lobes,UP,buff=.12)).scale(size).move_to(p)

def receptor(x,kind=2,broken=False):
    color=RED if broken else PINK
    outside=RoundedRectangle(width=.9 if kind==2 else .65,height=1.5,
        corner_radius=.1 if kind==2 else .3,color=color,fill_color=color,fill_opacity=.25).move_to([x,.85,0])
    stem=Line([x,.1,0],[x,-1.95,0],color=color,stroke_width=7)
    domain=(Rectangle(width=1.25,height=.9,color=color,fill_color=color,fill_opacity=.3)
        if kind==2 else RoundedRectangle(width=1.0,height=.9,corner_radius=.3,color=color,fill_color=color,fill_opacity=.3)).move_to([x,-2.2,0])
    if broken: domain=VGroup()
    return VGroup(outside,stem,domain)

def mechanism(broken=False,ligand=True):
    membrane=VGroup(*[Line([-5.8,y,0],[5.8,y,0],color=GREY,stroke_width=3) for y in (0,.18)])
    r2=receptor(-1.1,2,broken); r1=receptor(1.1,1)
    labs=VGroup(T('type II',28,PINK).move_to([-3.05,1,0]),
                T('type I',28,PINK).move_to([2.95,1,0]),
                Line([-2.35,1,0],[-1.6,1,0],color=PINK),
                Line([1.48,1,0],[2.3,1,0],color=PINK))
    lig=dimer((0,2.25,0)) if ligand else VGroup()
    return VGroup(membrane,r2,r1,labs,lig)

def activation(color=PINK):
    return Arrow([-.42,-2.2,0],[.53,-2.2,0],buff=0,color=color,stroke_width=5)

def jam_result():
    return VGroup(cap_stage(color=BLUE),heading('Neural tissue',BLUE),footer('No mesoderm detected',MESO))

def question_one():
    return VGroup(cap_stage(),heading('Caps from injected embryos'),footer('What do they become?'))

def bmp_ligs():
    # In the medium between the scattered cells, well inside the dish rim.
    return VGroup(*[dimer((x,-.12,0),'BMP4') for x in (-2.05,2.05)])

def added_stage(question=False):
    g=VGroup(cap_stage(True),bmp_ligs(),heading('Separated cells + BMP4',YELLOW))
    if question: g.add(footer('What do these cells become?'))
    return g

def gene_marks(stage):
    # Per cell: a 'neural' label above a clear OFF switch (grey knob at the left, red OFF).
    marks=VGroup()
    for c in stage[0][1]:
        p=c.get_center()
        lab=T('neural',24,BLUE).move_to(p+[0,.4,0])
        pill=RoundedRectangle(width=1.2,height=.46,corner_radius=.23,color=TEXT,stroke_width=3,
                              fill_color=BG,fill_opacity=.85).move_to(p+[0,-.22,0])
        knob=Circle(radius=.16,color=TEXT,fill_color=TEXT,fill_opacity=1).move_to(p+[-.4,-.22,0])
        off=T('OFF',22,RED,weight=BOLD).move_to(p+[.2,-.22,0])
        marks.add(VGroup(lab,pill,knob,off))
    return marks

def skin_result():
    g=added_stage()
    for c in g[0][1]: c.set_stroke(GREY).set_fill(GREY,.65)
    g.add(gene_marks(g),footer('Epidermis  •  neural genes OFF  •  keratin ON',ORANGE))
    return g

def ectoderm():
    tissue=VGroup(*[RoundedRectangle(width=1.75,height=4.8,corner_radius=.2,
        color=TEXT,fill_opacity=.03).move_to([x,-.15,0]) for x in (-4.65,-2.79,-.93,.93,2.79,4.65)])
    dots=VGroup(*[Dot([x,y,0],radius=.15,color=YELLOW)
        for x in (-4.65,-2.79,-.93,.93,2.79,4.65) for y in (-1.65,-.15,1.35)])
    return tissue,dots

def blocked_ligand(name,color,x):
    lig=chip(name,color,28).move_to([x,2.1,0])
    arrow=Arrow([x,1.65,0],[x,.55,0],color=color,buff=.08)
    bar=Line([x-.36,.48,0],[x+.36,.48,0],color=RED,stroke_width=7)
    return VGroup(lig,arrow,bar)

def blocking_stage():
    # Two inputs into the same broad, schematic broken receptor.
    rec=RoundedRectangle(width=5.2,height=1.45,corner_radius=.2,color=RED,
          fill_color=RED,fill_opacity=.12).move_to([0,-.45,0])
    label=T('Broken receptor',30,RED).move_to([0,-.45,0])
    tail=DashedLine([0,-1.2,0],[0,-2.3,0],color=RED)
    cross=VGroup(Line([-.3,-2.1,0],[.3,-2.65,0],color=RED,stroke_width=6),
                 Line([.3,-2.1,0],[-.3,-2.65,0],color=RED,stroke_width=6))
    return VGroup(rec,label,tail,cross)

class S00Title(TitleCard):
    LESSON='Neural Induction: The Default Model'
    TITLE='Break the Receptor, Add the Ligand'
    def construct(self):
        title=VGroup(T('Break the Receptor,',46,font=TITLE_FONT),T('Add the Ligand',46,font=TITLE_FONT)).arrange(DOWN,buff=.2)
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28),title).arrange(DOWN,buff=.5)
        self.play(FadeIn(g),run_time=.5); self.finish()

class S01(SpokenScene):
    def construct(self):
        g=cap_stage(); self.add(g,heading('Break the receptor',RED))
        lab=T('animal cap',28).move_to([-4.7,0,0]); lead=Line([-3.65,0,0],[-2.7,0,0],color=TEXT)
        self.add(lab,lead)
        self.at('without adding'); f=footer('No new signal added'); self.play(FadeIn(f),run_time=.35)
        self.at('What will'); self.play(FadeOut(f),FadeIn(T('?',76).move_to([4.75,0,0])),FadeIn(footer('What will the animal cap become?')),run_time=.4)
        self.finish()

class S02(SpokenScene):
    def construct(self):
        ring=VGroup(*[cell([-3.35+1.93*np.cos(a),-.1+1.93*np.sin(a),0],.3)
                    for a in np.linspace(0,TAU,20,endpoint=False)])
        cap=VGroup(*[ring[i] for i in (3,4,5,6,7)])
        for c in cap: c.set_stroke(TEXT).set_fill(TEXT,.55)
        for i in (13,14,15,16,17): ring[i].set_stroke(PURPLE).set_fill(PURPLE,.45)
        cav=T('blastocoel',28).move_to([-3.35,-.1,0])
        end=T('endoderm',28,PURPLE).move_to([-3.35,-2.75,0])
        bl=T('blastula',28).move_to([-3.35,2.85,0])
        gas=Ellipse(width=3.9,height=4.5,color=TEXT).move_to([3.1,-.05,0])
        groove=Arc(radius=1.35,start_angle=PI*1.08,angle=PI*.84,color=GREY,stroke_width=7).stretch(.42,1).move_to([3.1,-1.35,0])
        lip=Arc(radius=.55,start_angle=PI*.6,angle=PI*.8,color=PURPLE,stroke_width=9).move_to([1.95,-1.35,0])
        org=T('organizer',28,PURPLE).move_to([.4,-2.7,0])
        leader=Line([.75,-2.45,0],[1.7,-1.7,0],color=PURPLE)
        orient=VGroup(T('dorsal',28).move_to([-.1,.95,0]),Arrow([.45,.55,0],[1.55,-.55,0],buff=0,stroke_width=7,color=TEXT),
                     T('ventral',28).move_to([6.05,.95,0]),Arrow([5.75,.55,0],[4.7,-.5,0],buff=0,stroke_width=7,color=TEXT))
        extras=VGroup(cav,end,bl,gas,groove,lip,org,leader,orient,T('gastrula',28).move_to([3.1,2.85,0]))
        label=T('animal cap = ectoderm',28,TEXT).move_to([-3.35,2.32,0])
        self.add(ring,extras,label)
        self.at('the animal cap'); self.play(cap.animate.shift(UP*.35),FadeOut(label),run_time=.4)
        # Cut the five cap cells out, carry them between the two embryos, then expand them into the dish.
        lifted=cap.copy(); self.add(lifted)
        cut=T('cap cut out',26,TEXT).move_to([0,3.35,0]); self.add(cut)
        self.play(FadeOut(cap),lifted.animate.scale(1.25).move_to([0,2.2,0]),run_time=.7)
        self.at('cultured in salt'); self.play(FadeOut(cut),run_time=.01)
        target=cap_stage(); self.play(FadeOut(ring),FadeOut(extras),FadeOut(label),FadeIn(target[0]),Transform(lifted,target[1]),run_time=.65)
        self.play(FadeIn(footer('Salt solution')),run_time=.25); self.finish()

class S03(SpokenScene):
    def construct(self):
        g=cap_stage(); h=heading('Intact animal cap'); f=footer('Salt solution'); self.add(g,h,f)
        self.at('it becomes epidermis'); self.play(*[paint(c,GREY) for c in g[1]],FadeOut(f),FadeIn(footer('Epidermis',ORANGE)),run_time=.45)
        offs=[(-.45,-.45),(.1,-.7),(.5,-.35),(-.15,-.2),(.4,.0)]
        marks=VGroup(*[Dot(c.get_center()+np.array([dx,dy,0]),radius=.1,color=TEXT) for c in g[1] for dx,dy in offs])
        tc=g[1][2].get_center()   # label sits inside the top-right cell, above its keratin dots
        k=T('keratin',28).move_to(tc+[0,.62,0]); line=Line(tc+[0,.35,0],tc+[.1,.02,0],color=TEXT,stroke_width=3)
        self.at('epidermal keratin'); self.play(FadeIn(marks),FadeIn(k),Create(line),run_time=.35)
        self.at('That is'); self.play(FadeOut(h),FadeIn(heading('Control')),run_time=.3); self.finish()

class S04(SpokenScene):
    def construct(self):
        g=mechanism(ligand=False); labs=g[3]; g.remove(labs); self.add(g,heading('BMP receptor pair'))
        lig=dimer((0,2.35,0)); self.add(lig)
        self.at('pairs of'); self.play(lig.animate.move_to([0,2.25,0]),run_time=.6)
        self.at('a type 2'); self.play(FadeIn(VGroup(labs[0],labs[2])),run_time=.25)
        self.at('a type 1'); self.play(FadeIn(VGroup(labs[1],labs[3])),run_time=.25)
        self.finish()

class S05(SpokenScene):
    def construct(self):
        g=mechanism(); self.add(g)
        # Show the causal activation that a kinase-less type II cannot perform.
        act=activation(); al=T('activates',26,PINK).move_to([0,-2.85,0]); self.add(act,al)
        sm=chip('Smad1 / 5 / 8',BLUE,28).move_to([4.2,-2.2,0])
        p=chip('P',PHOS,28).move_to([1.1,-2.2,0])
        self.at('The type 1 receptor'); self.play(FadeIn(sm),run_time=.3)
        self.at('phosphorylate'); self.add(p); self.play(p.animate.move_to(sm.get_top()+np.array([sm.width/2-.32,p.height/2-.04,0])),run_time=.7)
        smp=VGroup(sm,p)
        self.at('It moves'); self.play(g.animate.scale(.65).to_edge(UP,buff=.3),FadeOut(act),FadeOut(al),smp.animate.move_to([3.3,-.3,0]),run_time=.35)
        for lab in g[3][:2]: lab.scale(1/.65)
        g[3][0].next_to(g[3][2],LEFT,buff=.12)
        g[3][1].next_to(g[3][3],RIGHT,buff=.12)
        g[4][1].scale(1/.65); g[4][1].next_to(g[4][0],UP,buff=.1)
        nucleus=RoundedRectangle(width=10.6,height=2.6,corner_radius=.4,color=TEXT).move_to([0,-2.2,0])
        nl=T('nucleus',28).move_to([-4.2,-2.95,0])
        self.at('to the nucleus'); self.play(FadeIn(nucleus),FadeIn(nl),smp.animate.move_to([.6,-1.6,0]),run_time=.4)
        sm4=chip('Smad4',BLUE,28).move_to([0,-.3,0])
        self.at('with'); self.play(FadeIn(sm4),run_time=.2)
        self.play(sm4.animate.move_to(sm.get_center()+np.array([-(sm.width+sm4.width)/2+.03,0,0])),run_time=.4)
        # the joined pair, phosphate still attached, switches on target genes
        genes=VGroup(*[RoundedRectangle(width=1.5,height=.25,corner_radius=.08,color=BLUE,fill_color=BLUE,fill_opacity=.9).move_to([x,-2.8,0]) for x in (-.5,1.7)])
        self.play(FadeIn(genes),FadeIn(T('target genes',26,BLUE).move_to([4.0,-2.8,0])),run_time=.25); self.finish()

class S06(SpokenScene):
    def construct(self):
        g=mechanism(ligand=False); self.add(g,heading('Remove the kinase domain'))
        self.at('Now remove'); self.play(g[1][2].animate.shift(DOWN*.7).set_opacity(0),g[1][0].animate.set_color(RED),g[1][1].animate.set_color(RED),run_time=1)
        self.at('It still binds'); lig=dimer((0,2.35,0)); self.add(lig); self.play(lig.animate.move_to([0,2.25,0]),run_time=.5)
        self.at('still pairs'); self.play(Indicate(VGroup(g[1][0],g[2][0]),color=TEXT,scale_factor=1.08),run_time=.5); self.finish()

class S07(SpokenScene):
    def construct(self):
        g=mechanism(True); self.add(g,heading('A jammed signaling complex',RED))
        sm=chip('Smad',BLUE,28).move_to([4,-2.2,0]); path=activation(GREY)
        self.add(sm,path)
        # Dim only the receptor graphics; labels stay at full brightness.
        self.at('cannot pass'); self.play(g[0].animate.set_opacity(.38),g[1].animate.set_opacity(.38),g[2].animate.set_opacity(.38),g[4][0].animate.set_opacity(.38),FadeIn(footer('No phosphate added',RED)),Create(Line([-.35,-1.85,0],[.35,-2.55,0],color=RED,stroke_width=8)),run_time=.4)
        self.at('so it jams'); self.play(Indicate(g[2],color=RED),run_time=.5); self.finish()

def complex_view(broken,cx,top=2.65,sc=.98):
    """One receptor complex with labels beside the receptors; returns (graphics, labels)."""
    r2=receptor(-1.1,2,broken); r1=receptor(1.1,1)
    mem=VGroup(*[Line([-2.2,y,0],[2.2,y,0],color=GREY,stroke_width=3) for y in (0,.18)])
    lig=dimer((0,2.25,0))
    l2=T('type II',28,RED if broken else PINK).next_to(r2[0],LEFT,buff=.15)
    l1=T('type I',28,PINK).next_to(r1[0],RIGHT,buff=.15)
    graphics=VGroup(mem,r2,r1,lig[0]); labels=VGroup(l2,l1,lig[1])
    whole=VGroup(graphics,labels).scale(sc)
    whole.shift(np.array([cx-whole.get_center()[0],top-whole.get_top()[1],0]))
    return graphics,labels

class S08(SpokenScene):
    def construct(self):
        wg,wl=complex_view(False,-3.8); jg,jl=complex_view(True,3.8)
        self.add(wg,wl,jg,jl,heading('Dominant negative',RED).shift(UP*.3),
                 T('Working complex',28).move_to([-3.8,-2.95,0]),T('Jammed complex',28,RED).move_to([3.8,-2.95,0]))
        self.at('a broken copy'); self.play(Indicate(jg[1],color=RED,scale_factor=1.12),run_time=.5)
        arrow=Arrow([1.5,-.4,0],[-1.5,-.4,0],buff=0,color=RED,stroke_width=8,max_tip_length_to_length_ratio=.3)
        word=T('blocks',30,RED).next_to(arrow,UP,buff=.18)
        self.at('blocks the working'); self.play(GrowArrow(arrow),FadeIn(word),wg.animate.set_opacity(.38),run_time=.6)
        self.play(FadeIn(footer('Broken copy blocks working copies',RED).shift(DOWN*.35)),run_time=.3); self.finish()

class S09(SpokenScene):
    def construct(self):
        egg=cell([1,-.3,0],2.25); self.add(egg,heading('1994  •  Hemmati-Brivanlou & Melton'),T('frog egg',30).move_to([1,-3,0]))
        needle=VGroup(Polygon([-5.1,1.5,0],[-4.9,1.95,0],[-1.2,.4,0],[-1.35,.1,0],color=TEXT,fill_color=GREY,fill_opacity=.35),Line([-1.3,.25,0],[-.45,-.1,0],color=TEXT,stroke_width=4))
        self.add(needle)
        self.at('injected eggs'); self.play(needle.animate.shift(RIGHT*.65),run_time=.5)
        label=T('RNA for a broken receptor',28,RED).move_to([-2.5,2.15,0])
        payload=VGroup(*[RoundedRectangle(width=.24,height=.14,corner_radius=.04,color=RED,fill_color=RED,fill_opacity=1).move_to([-2.7+i*.45,.95-i*.2,0]) for i in range(3)])
        self.at('with RNA'); self.play(FadeIn(label),FadeIn(payload),run_time=.2); self.play(payload.animate.shift(RIGHT*2.5+DOWN*.8),run_time=.65); self.finish()

class S10(SpokenScene):
    def construct(self):
        self.add(blocking_stage(),heading('Built from an activin receptor'),blocked_ligand('activin',ACT,-1.6))
        self.at('also blocks'); self.play(FadeIn(blocked_ligand('related ligand',TEXT,1.6)),FadeIn(footer('Also blocks related ligands',RED)),run_time=.5); self.finish()

class S11(SpokenScene):
    def construct(self):
        self.add(cap_stage(),heading('Caps from injected embryos'))
        self.at('What do'); self.play(FadeIn(footer('What do they become?')),run_time=.3); self.finish()

class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question_one()); self.wait(5)

class S13(SpokenScene):
    def construct(self):
        g=question_one(); self.add(g)
        self.at('Neural tissue'); self.play(*[paint(c,BLUE) for c in g[0][1]],FadeOut(g[1]),FadeIn(heading('Neural tissue',BLUE)),FadeOut(g[2]),run_time=.45)
        self.at('no mesoderm detected'); self.play(FadeIn(footer('No mesoderm detected',MESO)),run_time=.35); self.finish()

class S14Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(jam_result()); self.wait(2.5)

class S15(SpokenScene):
    def construct(self):
        self.add(cap_stage(color=BLUE),heading('Neural tissue',BLUE))
        sent=T('Blocking a receptor, not adding a signal, made neural tissue.',28,t2c={'neural tissue':BLUE}).move_to([0,-3.3,0])
        self.at('Blocking a receptor'); self.play(FadeIn(sent),run_time=.35); self.finish()

class S16(SpokenScene):
    def construct(self):
        g=blocking_stage(); q=heading('Which signal keeps ectoderm as skin?'); self.add(g,q)
        self.at('The receptor blocks'); a=blocked_ligand('activin',ACT,-1.6); self.play(FadeIn(a),run_time=.35)
        self.at('and related'); rel=blocked_ligand('related ligand',TEXT,1.6); self.play(FadeIn(rel),run_time=.35)
        self.at('added to caps'); self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.15); stage=cap_stage(); self.add(stage,heading('Add activin',ACT))
        fa=T('Activin makes mesoderm',28,MESO); fb=T(', not skin',28,ORANGE); VGroup(fa,fb).arrange(RIGHT,buff=.06,aligned_edge=DOWN).move_to([0,-3.18,0])
        self.at('makes mesoderm'); self.play(*[paint(c,MESO) for c in stage[1]],FadeIn(fa),run_time=.35)
        self.at('not skin'); self.play(FadeIn(fb),run_time=.25); self.finish()

class S17(SpokenScene):
    def construct(self):
        tissue,dots=ectoderm(); self.add(tissue,dots,heading('Early ectoderm'),footer('BMP4 RNA',YELLOW))
        self.at('BMP4'); self.play(Indicate(dots,color=YELLOW,scale_factor=1.04),run_time=.4); self.finish()

class S18(SpokenScene):
    def construct(self):
        tissue,dots=ectoderm(); h=heading('Early ectoderm').shift(UP*.3); self.add(tissue,dots,h,footer('BMP4 RNA',YELLOW))
        dorsal=T('dorsal',28).move_to([-2.79,2.85,0]); ventral=T('ventral',28).move_to([2.79,2.85,0])
        self.at('cleared from'); self.play(FadeOut(VGroup(*dots[:9])),FadeIn(dorsal),FadeIn(ventral),run_time=.6)
        plate=RoundedRectangle(width=5.55,height=4.95,corner_radius=.3,color=BLUE,stroke_width=5).move_to([-2.79,-.15,0])
        self.at('the neural plate'); self.play(Create(plate),FadeOut(h),FadeIn(heading('Neural plate appears',BLUE).shift(UP*.3)),run_time=.5); self.finish()

class S19(SpokenScene):
    def construct(self):
        self.add(cap_stage(),heading('Test BMP4 directly'))
        self.at('would otherwise turn'); self.play(FadeIn(footer('Need cells that would turn neural',BLUE)),run_time=.35); self.finish()

class S20(SpokenScene):
    def construct(self):
        self.add(cap_stage(),heading('1989  •  Grunz & Tacke'))
        self.at('had found them'); self.play(Indicate(self.mobjects[0][1],color=TEXT,scale_factor=1.03),run_time=.5); self.finish()

class S21(SpokenScene):
    def construct(self):
        g=cap_stage(); self.add(g,heading('Separate the animal cap cells'))
        self.at('They separated'); targets=cells(True)
        rng=np.random.default_rng(7)
        # First the clump loosens: every cell shivers outward by its own amount ...
        mid=np.array([0,0,0])
        loosen=[]
        for c in g[1]:
            d=c.get_center()-mid; d=d/np.linalg.norm(d)
            loosen.append(c.animate(rate_func=there_and_back_with_pause).shift(d*.12+np.array([rng.uniform(-.1,.1),rng.uniform(-.1,.1),0])))
        self.play(*loosen,run_time=.4)
        # ... then the cells peel off one after another, drifting at different speeds.
        order=[5,0,3,2,4,1]
        anims=[]
        for k,i in enumerate(order):
            rt=rng.uniform(.8,1.2)
            anims.append(Succession(Wait(.15*k),Transform(g[1][i],targets[i],run_time=rt,path_arc=(-1 if i%2 else 1)*rng.uniform(.25,.7),rate_func=smooth)))
        self.play(*anims)
        self.at('lacking the'); self.play(FadeIn(footer('No calcium  •  no magnesium')),run_time=.35); self.finish()

class S22(SpokenScene):
    def construct(self):
        g=cap_stage(True); self.add(g,heading('Keep the cells apart'))
        cc=np.array([-1.45,-3.3,0])
        clk=Circle(radius=.42,color=TEXT,stroke_width=4).move_to(cc)
        ticks=VGroup(*[Line(cc+.34*np.array([np.sin(a),np.cos(a),0]),cc+.42*np.array([np.sin(a),np.cos(a),0]),color=TEXT,stroke_width=3) for a in np.arange(0,TAU,TAU/4)])
        hand=Line(cc,cc+UP*.33,color=YELLOW,stroke_width=5)
        hours=T('hours apart',28).next_to(clk,RIGHT,buff=.3); self.add(clk,ticks,hand,hours)
        self.at('They kept'); self.play(Rotate(hand,-TAU*.8,about_point=cc,rate_func=linear),run_time=1.85)
        self.at('then let'); self.play(FadeOut(VGroup(clk,ticks,hand,hours)),Transform(g[1],cells()),run_time=.7)
        self.at('The cells made'); self.play(*[paint(c,BLUE) for c in g[1]],FadeIn(footer('Separated cells → neural',BLUE)),run_time=.5); self.finish()

class S23(SpokenScene):
    def construct(self):
        # The new experiment starts already dissociated, rather than inheriting a blue clump.
        g=cap_stage(True); h=heading('1995  •  Wilson & Hemmati-Brivanlou'); self.add(g,h)
        self.at('and added'); ligs=bmp_ligs(); self.play(FadeIn(ligs,shift=DOWN*.45),FadeOut(h),FadeIn(heading('Separated cells + BMP4',YELLOW)),run_time=.6); self.finish()

class S24(SpokenScene):
    def construct(self):
        self.add(added_stage())
        self.at('What do'); self.play(FadeIn(footer('What do these cells become?')),run_time=.3); self.finish()

class S25Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(added_stage(True)); self.wait(5)

class S26(SpokenScene):
    def construct(self):
        g=added_stage(True); self.add(g)
        f=footer('Epidermis',ORANGE)
        self.at('Epidermis'); self.play(*[paint(c,GREY) for c in g[0][1]],FadeOut(g[3]),FadeIn(f),run_time=.45)
        self.at('Their'); self.play(FadeIn(gene_marks(g)),FadeOut(f),FadeIn(footer('Epidermis  •  neural genes OFF  •  keratin ON',ORANGE)),run_time=.35); self.finish()

class S27Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(skin_result()); self.wait(2.5)

class S28(SpokenScene):
    def construct(self):
        # Two tall dishes (about 65% of frame height) with separate rows for takeaway, dishes and result labels.
        cy=.4
        def panel(cx,spread=False):
            rim=RoundedRectangle(width=5.9,height=5.2,corner_radius=.3,color=GREY).move_to([cx,cy,0])
            pts=([(x,y) for y in (1.6,0,-1.6) for x in (-1.75,1.75)] if spread else
                 [(x,y) for y in (1.55,0,-1.55) for x in (-.88,.88)])
            cs=VGroup(*[cell([cx+x,cy+y,0],.62 if spread else .8) for x,y in pts])
            return VGroup(rim,cs)
        left=panel(-3.4); right=panel(3.4,True)
        self.add(left,right)
        a=T('Jam the receptor \u2192 cap turns neural.',28).move_to([0,3.58,0])
        a2=T('Add BMP4 back \u2192 separated cells return to skin.',28).move_to([0,-3.45,0])
        self.add(a)
        j1=T('Jammed receptor \u2192 ',28,RED); j2=T('Neural',30,BLUE); VGroup(j1,j2).arrange(RIGHT,buff=.2).move_to([-3.4,-2.65,0])
        self.at('jam the receptor'); self.play(FadeIn(j1),run_time=.3)
        self.at('a cap turns'); self.play(*[paint(c,BLUE) for c in left[1]],FadeIn(j2),run_time=.4)
        self.at('Add BMP4 back'); lig=dimer((3.4,cy,0),'BMP4'); self.play(FadeIn(lig),FadeIn(a2),run_time=.35)
        self.at('return to skin'); self.play(*[paint(c,GREY) for c in right[1]],FadeIn(T('Epidermis',30,ORANGE).move_to([3.4,-2.65,0])),run_time=.35); self.finish()

class S29End(EndCard):
    LINE='Jam the receptor and a cap turns neural.\nAdd BMP4 back and separated cells return to skin.'
    def construct(self):
        lines=VGroup(T('Jam the receptor and a cap turns neural.',32),T('Add BMP4 back and separated cells return to skin.',32)).arrange(DOWN,buff=.6)
        self.play(FadeIn(lines),run_time=.4); self.add(T('biochemistrypedia.com',26,TEAL).move_to([0,-2,0])); self.finish()
