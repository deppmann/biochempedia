"""Labelled schematic cartoons only; no molecular structures.
COLOR MAP: BLUE=TMC1/2; TEAL=partners; YELLOW=current/ions;
PINK=mutation; GREEN=supported result; RED=unresolved; GREY=outlines;
GOLD=proposed pore; TEXT=experimental actions. Shared with scenes.old.py.
Only current trace: computed I(t)=N*i*Popen=0 in the absent-current case.
Association connectors are schematic, not molecular bonds or native geometry.
"""
import numpy as np
from bp_style import *
PINK = '#F2789F'


def heading(s):
    return T(s, 32).move_to([0, 3.12, 0])


def label(s, x, y, color=TEXT, size=28):
    return T(s, size, color).move_to([x,y,0])


def popen(size=36, color=TEXT):
    p=T('P',size,color)
    sub=T('open',26,color).next_to(p,RIGHT,buff=.03).shift(DOWN*.23)
    return VGroup(p,sub)


def counter(s, color=GREY):
    t=popen(color=color) if s=='P' else T(s,36,color)
    b=RoundedRectangle(width=max(1.35,t.width+.55),height=.85,corner_radius=.14,color=color,fill_opacity=.1)
    return VGroup(b,t.move_to(b))


def counters(y=1.5):
    return VGroup(*[counter(s) for s in ('N','i','P')]).arrange(RIGHT,buff=1.0).move_to([0,y,0])


def formula():
    return VGroup(T('I = N × i ×',34),popen(34)).arrange(RIGHT,buff=.14)


def channel(x=0,y=0,h=3.4, name='TMC1',tag='mouse'):
    walls=VGroup(*[RoundedRectangle(width=.85,height=h,corner_radius=.17,color=BLUE,
        fill_opacity=.22,stroke_width=4).move_to([x+d,y,0]) for d in (-.8,.8)])
    return VGroup(walls,label(name,x,y-h/2-.4,BLUE),label(tag,x,y+h/2+.35,GREY,26))


def dim(card):
    # Labels retain full contrast; only the card background dims.
    return card[0].animate.set_fill(GREY,opacity=.03).set_stroke(GREY)


def cards(y=-.2):
    return VGroup(*[chip(s,TEAL,30,pad=.32) for s in ('CIB2','TMIE','LHFPL5')]).arrange(RIGHT,buff=1.0).move_to([0,y,0])


def partner_stage(title='Mouse cochlear hair cells'):
    return VGroup(heading(title),counters(),cards())


def blob():
    return VGroup(Ellipse(width=7.6,height=4.9,color=GREY,fill_opacity=.18),
                  label('cryo-EM density map',0,-2.95,GREY))


def assembly():
    # Paired broad walls: same icon family as mouse schematics.
    main=channel(0,.75,2.8,'TMC-1 ×2','worm')
    calm=VGroup(*[chip('CALM-1',TEAL,28,pad=.3).move_to([x,-2.15,0]) for x in (-1.7,1.7)])
    tmie=VGroup(*[chip('TMIE',TEAL,28,pad=.3).move_to([x,.5,0]) for x in (-3.8,3.8)])
    return VGroup(main,calm,tmie,label('CALM-1 ×2',0,-3,TEAL),label('TMIE ×2',4,1.6,TEAL))


def prediction():
    rods=VGroup(*[RoundedRectangle(width=.8,height=h,corner_radius=.22,color=GREY,
        fill_opacity=.10).move_to([x,-2.5+h/2,0]) for x,h in [(-5.2,3.4),(-3.9,4.3),(-2.6,5.2)]])
    dots=VGroup(*[Dot([x,-2.15+j*.64,0],radius=.10,color=BLUE) for x,n in [(-5.2,4),(-3.9,6),(-2.6,7)] for j in range(n)])
    prot=VGroup(chip('TMC1',BLUE,28).move_to([-1.05,1.8,0]),Line([-1.65,1.5,0],[-2.2,1.2,0],color=BLUE))
    ax=Axes(x_range=[0,5,1],y_range=[-1,1,1],x_length=5.1,y_length=3.6,
        axis_config={'include_ticks':False,'color':GREY},tips=False).move_to([3.2,-.1,0])
    # Zero response to bundle deflection, N*i*Popen = 0. No invented amplitudes.
    trace=ax.plot(lambda t:0.0,x_range=[0,5],color=YELLOW)
    bar=Line(ax.c2p(1,.8),ax.c2p(4,.8),color=TEXT,stroke_width=6)
    graph=VGroup(ax,trace,bar,label('deflect bundle',3.4,1.9),
        label('Current (pA)',3.1,2.5),label('0',.25,-.1,YELLOW),label('time',5.3,-2.3,GREY),
        label('schematic',3.1,-2.3,GREY),label('I = 0',3.1,.4,YELLOW))
    return VGroup(heading('Without TMIE: predict'),rods,VGroup(dots,prot),graph,
        label('Protein there, still no current. Why?',0,-3.55,RED),label('stereocilia',-3.9,-2.95,GREY,26))


def complex_group():
    ch=channel(-1,0,3.3)
    partners=VGroup(chip('TMIE',TEAL,28).move_to([-4,.5,0]),
        chip('LHFPL5',TEAL,28).move_to([2,.5,0]),chip('CIB2',TEAL,28).move_to([-1,-2.75,0]))
    pore=VGroup(DashedVMobject(Ellipse(width=.6,height=2.7,color=GOLD),num_dashes=20),
        label('proposed pore',1.9,-1.6,GOLD,26),Line([-.7,-1.1,0],[.6,-1.6,0],color=GOLD))
    pore[0].move_to([-1,0,0])
    return VGroup(ch,partners,pore)


class S00Title(TitleCard):
    TITLE='A Pore Inside a Complex'
    LESSON="The Hair Cell's Transduction Channel"


class S01Q(SpokenScene):
    def construct(self):
        ch=channel(0,0,4.3); ch[2].move_to([2,2.15,0])
        ps=VGroup(chip('TMIE',TEAL,30).move_to([-3.8,.2,0]),chip('LHFPL5',TEAL,30).move_to([3.8,.2,0]),chip('CIB2',TEAL,30).move_to([0,2.65,0]))
        self.add(ch,ps)
        self.at('lines the pore'); self.play(Indicate(ch[0]),run_time=.5)
        self.at('why does'); self.play(Indicate(ps,color=TEAL),FadeIn(label('Why are partners needed?',0,-3.2,RED,34)),run_time=.5)
        self.finish()


class S02Worm(SpokenScene):
    def construct(self):
        absent=VGroup(RoundedRectangle(width=4.4,height=3.7,corner_radius=.2,color=GREY),label('Native mammalian\nstructure unavailable',0,0,GREY))
        self.add(absent,heading('Looking for a native structure'))
        # Closed, tapered tube around a gentle S-shaped centreline.
        t=np.linspace(0,1,90)
        center=np.column_stack((1.05*np.sin(2*PI*t),2.25-4.5*t,np.zeros_like(t)))
        tangent=np.gradient(center,axis=0); normal=np.column_stack((-tangent[:,1],tangent[:,0],np.zeros_like(t)))
        normal/=np.linalg.norm(normal,axis=1)[:,None]
        radius=.24*np.sin(PI*t)**.65*(1-.48*t)
        outline=np.vstack((center+normal*radius[:,None],(center-normal*radius[:,None])[::-1]))
        body=VMobject(color=TEXT,stroke_width=2.5,fill_color=TEAL,fill_opacity=.18).set_points_as_corners(outline).close_path()
        worm=VGroup(body,Dot(center[3],radius=.045,color=GREY),Dot(center[-5],radius=.025,color=GREY),label('C. elegans',3,1),label('head',1,2.3,GREY,22),label('tail',-1,-2.3,GREY,22))
        self.at('was available'); self.play(FadeOut(absent),FadeIn(worm),run_time=.65)
        self.at('and colleagues'); self.play(FadeIn(label('Jeong, Clark and colleagues, 2022',0,-3.15)),run_time=.35)
        self.at('turned to'); self.play(Indicate(worm,color=TEAL,scale_factor=1.03),run_time=.45)
        self.finish()


class S03Cryo(SpokenScene):
    def construct(self):
        tiles=VGroup(*[VGroup(Rectangle(width=1.55,height=1.55,color=GREY),Ellipse(width=.85,height=1.05,color=BLUE,fill_opacity=.25).rotate(a)) for a in np.linspace(0,PI,6)]).arrange_in_grid(rows=2,cols=3,buff=.25)
        self.add(heading('Native worm complex: cryo-EM'),tiles,label('particle images',0,-2.5,GREY))
        self.at('purified the native'); self.play(Indicate(tiles,color=BLUE),run_time=.5)
        mp=VGroup(Ellipse(width=3.5,height=4.4,color=GREY,fill_opacity=.2).move_to([4,0,0]),label('density map',4,-2.6,GREY))
        arrow=VGroup(Arrow([-.4,0,0],[1.8,0,0],color=TEXT),label('combine',.7,.6))
        self.at('and solved'); self.play(tiles.animate.scale(.85).move_to([-3.5,0,0]),FadeOut(self.mobjects[2]),GrowArrow(arrow[0]),FadeIn(arrow[1]),FadeIn(mp),run_time=.65)
        self.at('microscopy'); self.play(Indicate(mp,color=TEXT),run_time=.4)
        self.finish()


class S04Assembly(SpokenScene):
    def construct(self):
        b=blob(); a=assembly(); self.add(heading('Worm complex: two copies each'),b)
        self.at('main assembly'); self.play(FadeIn(a[0][0]),b[0].animate.set_fill(opacity=.05),run_time=.35)
        self.at('TMC1'); self.play(FadeOut(b),FadeIn(a[0][1]),FadeIn(a[0][2]),run_time=.25)
        self.at('CALM1'); self.play(FadeIn(a[1]),FadeIn(a[3]),run_time=.25)
        self.at('TMIE'); self.play(FadeIn(a[2]),FadeIn(a[4]),run_time=.25)
        self.finish()


class S05Calm(SpokenScene):
    def construct(self):
        a=chip('CALM-1',TEAL,44,pad=.65).move_to([-3.7,.3,0]); b=chip('CIB2',TEAL,44,pad=.65).move_to([3.7,.3,0])
        ar=DoubleArrow([-1.7,.3,0],[2,.3,0],color=TEAL,buff=0)
        self.add(heading('Relatives in the complex'),a,b,ar,label('worm',-3.7,-1.3,GREY),label('mouse',3.7,-1.3,GREY),label('orthologue\n(same ancestry)',0,1.6,TEAL))
        self.at('worm relative'); self.play(Indicate(ar,color=TEAL),run_time=.5)
        self.at('mammalian protein'); self.play(FadeIn(label('CALM-1: worm relative of mouse CIB2',0,-2.8)),run_time=.4)
        self.finish()


class S06Model(SpokenScene):
    def construct(self):
        # Separate columns make the measured vs model distinction readable.
        worm=VGroup(channel(-3.3,.1,3,'TMC-1','worm'),chip('CALM-1',TEAL,28).move_to([-4,-2.6,0]),chip('TMIE',TEAL,28).move_to([-1.9,-2.6,0]))
        human=VGroup(*[DashedVMobject(RoundedRectangle(width=.85,height=3,corner_radius=.17,color=BLUE),num_dashes=16).move_to([x,.1,0]) for x in (2.5,4.1)],label('TMC1',3.3,-1.8,BLUE),chip('CIB2',TEAL,28).move_to([2.3,-2.6,0]),chip('TMIE',TEAL,28).move_to([4.4,-2.6,0]),label('human',3.3,2,GREY))
        self.add(heading('Human complex: model, not measured'),worm,label('solid: worm, measured',-3.3,2.5,GREY))
        self.at('human complex'); self.play(FadeIn(human),run_time=.5)
        self.at('a model'); self.play(FadeIn(label('dashed: human, model',3.3,2.5,GREY)),run_time=.4)
        self.at('not a measurement'); self.play(Indicate(human,color=RED,scale_factor=1.02),run_time=.4)
        self.finish()


class S07Cib2(SpokenScene):
    def construct(self):
        s=partner_stage(); self.add(s)
        self.at('three factors'); self.play(Indicate(s[1]),run_time=.4)
        case=label('Cib2-null cochlear hair cells',0,-1.4)
        self.at('Without CIB2'); self.play(dim(s[2][0]),FadeIn(case),run_time=.5)
        self.at('no detectable'); self.play(s[1][0].animate.set_color(RED),FadeIn(label('N falls?',-4,1.5,RED)),FadeIn(label('Endogenous tags: TMC1 / TMC2\nnot detected in stereocilia',0,-2.35,BLUE)),FadeIn(label('Staining is not a count',0,-3.35,RED,26)),run_time=.4)
        self.at('So the'); self.play(s[1][0].animate.shift(DOWN*.3),FadeIn(label('i and P: not tested here',0,.65,GREY,26)),run_time=.4)
        self.play(FadeIn(label('Build, deliver or hold? Unresolved.',0,2.35,GREY,26)),run_time=.35)
        self.finish()


class S08Tmie(SpokenScene):
    def construct(self):
        s=partner_stage(); self.add(s)
        self.at('Without TMIE'); self.play(dim(s[2][1]),FadeIn(label('Tmie-null outer hair cells',0,-1.4)),run_time=.45)
        self.at('could not be detected'); self.play(s[1][0].animate.set_color(RED).shift(DOWN*.3),FadeIn(label('N falls?',-4,1.5,RED)),FadeIn(label('Tagged TMC1 not detected in stereocilia',0,-2.35,BLUE)),FadeIn(label('Staining is not a count',0,-3.2,RED)),run_time=.5)
        self.finish()


class S09Predict(SpokenScene):
    def construct(self):
        p=prediction(); self.add(p[0],p[1],p[5],label('Predict',3,0,RED,44))
        self.at('still reaches'); self.play(FadeIn(p[2]),run_time=.5)
        self.at('yet gives'); self.play(FadeOut(self.mobjects[3]),FadeIn(p[3]),run_time=.5)
        self.at('What does'); self.play(FadeIn(p[4]),run_time=.4)
        self.finish()


class S10Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        p=prediction(); p[0].become(heading('Pause and think'))
        self.add(p); self.wait(5)


class S11Reveal(SpokenScene):
    def construct(self):
        s=partner_stage('TMIE: more than delivery'); s[2][1].set_color(YELLOW)
        self.add(s,label('TMC1 localized, still no current',0,-1.5,RED),label('Protein localized; working channel not established',0,-3.1,RED,26))
        self.at('more than getting'); self.play(Indicate(s[2][1],color=YELLOW),run_time=.4)
        for cue,word,idx in [('build','build',0),('couple','couple',1),('gate a','gate',2)]:
            c=s[1][idx]
            link=Line(s[2][1].get_top(),c.get_bottom(),color=YELLOW,stroke_width=1.5)
            tag=label('? '+word,c.get_x(),2.28,RED,26)
            self.at(cue); self.play(Create(link),FadeIn(tag),run_time=.22)
        self.finish()


class S12Mut(SpokenScene):
    def construct(self):
        s=partner_stage('Neonatal outer hair cells'); self.add(s)
        self.at('mutations'); self.play(s[2][1].animate.set_color(PINK),FadeIn(label('Deafness-linked TMIE mutation',0,-1.5,PINK)),run_time=.4)
        self.at('lowered the unitary'); self.play(s[1][1].animate.set_color(YELLOW),FadeIn(label('i decreases: smaller unitary current',0,-2.7,YELLOW)),run_time=.4)
        a=channel(-3,0,3.1,'TMC2','normal'); b=channel(3,0,3.1,'TMC2','Tmie mutant')
        a[2].move_to([-3,2.3,0]); b[2].move_to([3,2.3,0])
        normal=VGroup(*[Dot([-3,.65+j*.4,0],radius=.12,color=YELLOW) for j in range(3)])
        mutant=VGroup(*[Dot([3,.65+j*.4,0],radius=.12,color=YELLOW) for j in range(3)])
        stream_labels=VGroup(label('Ca²+ stream',-4.6,.4,YELLOW,24),label('Ca²+ stream',4.6,.4,YELLOW,24),
            Line([-3.5,.55,0],[-3.15,.65,0],color=YELLOW),Line([3.5,.55,0],[3.15,.65,0],color=YELLOW))
        panel=VGroup(heading('TMC2-only: calcium permeability'),a,b,stream_labels,label('TMIE mutation',3,-2.55,PINK,26),label('schematic traffic; direction of change unspecified',0,-3.25,GREY,26),normal,mutant)
        self.at('In cells where'); self.play(*[FadeOut(m) for m in list(self.mobjects)],FadeIn(panel),run_time=.45)
        self.at('they changed'); self.play(normal.animate.shift(DOWN*1.9),mutant.animate.shift(DOWN*1.9),stream_labels.animate.shift(DOWN*1.9),FadeIn(label('?',3,.3,RED,44)),FadeIn(label('changed; direction\nnot specified',0,-.45,RED,24)),run_time=1.25)
        self.finish()


class S13Limit(SpokenScene):
    def construct(self):
        ch=channel(0,.2,3.7); tm=chip('TMIE',TEAL,34).move_to([-3.4,.2,0]); bond=Line(tm.get_right(),[-1.3,.2,0],color=TEAL)
        self.add(heading('TMIE and pore properties'),ch,tm,bond)
        self.at('shapes the'); self.play(FadeIn(label('✓ Shapes pore\nproperties',-3.1,-2.7,GREEN,30)),Indicate(tm),run_time=.5)
        self.at('without being shown'); self.play(FadeIn(label('× Not shown to\nbe the pore',3.1,-2.7,RED,30)),run_time=.4)
        self.finish()


class S14Lhfpl5(SpokenScene):
    def construct(self):
        h=heading('LHFPL5 and the tip link')
        rod=VGroup(*[RoundedRectangle(width=.8,height=h,corner_radius=.2,color=GREY,fill_opacity=.1).move_to([x,-2.6+h/2,0]) for x,h in [(-6,2.5),(-2,4.9)]])
        pcd=chip('PCDH15',TEXT,28).move_to([-4.55,.77,0]); part=chip('LHFPL5',TEAL,28).move_to([-4.55,-.55,0])
        tip=Line([-6,-.1,0],[-2,2.3,0],color=TEXT,stroke_width=6)
        # Opaque chip seats the named tip-link protein on the link.
        pcd[0].set_fill(BG,opacity=1)
        bond=Line(pcd.get_bottom(),part.get_top(),color=TEAL,stroke_width=5)
        part.shift(DOWN*.45)
        bound=label('PCDH15–LHFPL5\nbound',3,1.7,TEAL,28)
        question=VGroup(counter('i').move_to([3,.5,0]),label('?',3,-.6,RED,44))
        self.add(h,rod,tip,label('tip link',-4.6,2.35),pcd,part,label('schematic attachment',-3,-3.15,GREY,26),question)
        self.at('binds'); self.play(Create(bond),part.animate.shift(UP*.45),run_time=.5)
        self.at('protein'); self.play(Indicate(pcd,color=TEXT),FadeIn(bound),run_time=.4)
        self.at('Without it'); self.play(dim(part),FadeOut(question),FadeOut(bound),FadeIn(label('Lhfpl5-null / Tmhs-null',2.8,2.3,RED,26)),run_time=.4)
        # Two large evidence panels with independent qualitative i counters.
        one=VGroup(RoundedRectangle(width=6,height=2.4,corner_radius=.2,color=GREY).move_to([2.7,.55,0]),label('2012 Tmhs-null\nXiong and colleagues',2.7,1.2,TEXT,28),counter('i').move_to([1.1,-.05,0]),label('smaller events',3.5,-.05,YELLOW,26))
        self.at('and colleagues'); self.play(FadeIn(one),run_time=.4)
        self.at('smaller'); self.play(one[2].animate.set_color(YELLOW).shift(DOWN*.1),run_time=.4)
        self.at('events in'); self.play(Indicate(one[1],color=YELLOW,scale_factor=1.02),run_time=.4)
        two=VGroup(RoundedRectangle(width=6,height=2.1,corner_radius=.2,color=GREY).move_to([2.7,-1.9,0]),label('Later Lhfpl5-null\nTMC1-only channels',2.7,-1.5,TEXT,28),counter('i').move_to([1.1,-2.45,0]),label('unchanged',3.5,-2.45,GREEN,26))
        self.at('Later recordings'); self.play(FadeIn(two[0]),FadeIn(two[1]),FadeIn(two[2]),run_time=.4)
        self.at('only channels'); self.play(Indicate(two[1]),run_time=.4)
        self.at('found no change'); self.play(two[2].animate.set_color(GREEN),FadeIn(two[3]),run_time=.4)
        self.at('molecular effect'); self.play(FadeOut(rod),FadeOut(tip),FadeOut(bond),FadeOut(pcd),FadeOut(part),FadeOut(self.mobjects[6]),FadeIn(label('Also coupling\nand activation',-3,-1.6,TEAL,28)),run_time=.4)
        self.at('still open'); self.play(FadeIn(label('Molecular effect still open',0,-3.4,RED,28)),run_time=.35)
        self.finish()


class S15Complex(SpokenScene):
    def construct(self):
        ch=channel(-4,.2,3.3)
        partners=VGroup(*[chip(n,TEAL,30).move_to([-.8,y,0]) for n,y in [('CIB2',1.6),('TMIE',0),('LHFPL5',-1.6)]])
        cs=VGroup(*[counter(n).move_to([4.8,y,0]) for n,y in [('N',1.6),('i',0),('P',-1.6)]])
        pore=DashedVMobject(Ellipse(width=.6,height=2.7,color=GOLD),num_dashes=20).move_to([-4,.2,0])
        boundary=RoundedRectangle(width=6.6,height=5.5,corner_radius=.35,color=TEAL,fill_opacity=.025).move_to([-2.8,-.1,0])
        self.add(heading('One current, one complex'),boundary,ch,partners,cs,pore,label('proposed pore',-4,-2.5,GOLD,26),label('complex · schematic inventory',-2.8,-3.3,TEAL,26),label('Dashed: factor not isolated',3.5,-2.8,RED,24))
        links=VGroup(*[DashedLine(p.get_right(),cs[i].get_left(),color=RED) for i,p in enumerate(partners)])
        self.at('current you measure'); self.play(FadeIn(links),run_time=.4)
        self.at('belongs to the complex'); self.play(Indicate(boundary,color=TEAL,scale_factor=1.02),run_time=.5)
        self.at('one protein'); self.play(Indicate(VGroup(ch,partners),color=TEAL,scale_factor=1.01),run_time=.4)
        self.finish()


class S16Open(SpokenScene):
    def construct(self):
        c=complex_group().shift(DOWN*.5)
        pcd=chip('PCDH15',TEXT,28).move_to([-4.7,2,0]); tip=Line([-5.9,3.6,0],pcd.get_top(),color=TEXT,stroke_width=6)
        # End at a labelled contact on the outer wall; no line crosses the bar.
        end=np.array([-2.225,.65,0]); start=pcd.get_right()
        mid=(start+end)/2
        path=VGroup(DashedLine(start,end,color=RED),Dot(end,radius=.07,color=RED),
            label('?',mid[0],mid[1],RED,40).set_background_stroke(color=BG,width=8),label('contact?',-3.25,.65,RED,24),Line([-2.55,.65,0],end,color=RED,stroke_width=1.5))
        self.add(c,pcd,tip,label('tip link',-4.1,3.05,size=26),label('Force coupling remains open',2.8,2.4,RED,28))
        self.at('one question open'); self.play(Create(path),run_time=.5)
        self.at('How does'); self.play(FadeIn(heading('How does force reach the pore?')),run_time=.4)
        self.at('force from'); self.play(Indicate(path,color=RED,scale_factor=1.02),run_time=.45)
        self.finish()


class S17Take(SpokenScene):
    def construct(self):
        names=['Localization · N?','Loss · N / i / P?','Rescue · N / i / P?','Permeation · i / selectivity','Accessibility · i / selectivity','Activity alone · i / P']
        # P in the rung text is defined by the proper subscript formula beside it.
        rails=VGroup(*[Line([x,-3.15,0],[x,2.55,0],color=GREY,stroke_width=4) for x in (.35,6.25)])
        rs=VGroup(*[chip(n,GREY,26,pad=.25).move_to([3.3,-2.7+i*.95,0]) for i,n in enumerate(names)])
        eq=formula().move_to([-3.3,.8,0])
        self.add(heading('The evidence ladder'),rails,rs,eq,label('P = probability\nof being open',-3.3,-.5,GREY,28),label('Which factor\ndid it test?',-3.3,-2.1,YELLOW,32))
        self.at('which factor'); self.play(Indicate(eq,color=YELLOW),run_time=.45)
        # Illuminate at the start of the sentence, sustaining >3 seconds.
        self.at('The case'); self.play(*[rs[i].animate.set_color(GREEN) for i in (3,4,5)],*[rs[i].animate.set_color(TEXT) for i in (0,1,2)],run_time=.4)
        self.at('several rungs together'); self.play(Indicate(VGroup(*rs[3:]),color=GREEN,scale_factor=1.01),run_time=.4)
        self.finish()


class S18End(EndCard):
    LINE='The case for the pore rests on several rungs together.'
