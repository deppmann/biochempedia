"""Hubs That Compete — schematic teaching animation, synced to final audio.

COLOR MAP: TEAL enhancers/hub outlines; GREEN receptor genes (dim before choice);
ORANGE receptor RNA; BLUE Lhx2; YELLOW Ebf; PURPLE Ldb1/Bptf feedback;
GREY nuclei/chromosomes; TEXT citations. Chromosome identity: three teal tints.
Hub circles denote spatial clusters, never molecular structures.
Contact heat map: explicitly schematic distance-decay model with symmetric hotspots;
not measured data. Neuron counts illustrate direction, not effect size.
"""
import numpy as np
from bp_style import *

ORANGE='#F29E4C'
PURPLE='#B58CD9'
TINTS=[TEAL,'#71D5BC','#7FAED6']


def tile(color=GREEN,s=.7,op=.35):
    return RoundedRectangle(corner_radius=.08,width=s,height=s,stroke_color=color,
        stroke_width=2.5,fill_color=color,fill_opacity=op)


def nucleus(w=11.5,h=5.8,y=0):
    return Ellipse(width=w,height=h,stroke_color=GREY,stroke_width=2,
        fill_color=GREY,fill_opacity=.035).move_to([0,y,0])


def head(text,color=TEXT):
    return T(text,30,color).move_to([0,3.18,0])


def foot(text,color=TEXT,size=26):
    return T(text,size,color).move_to([0,-3.15,0])


def glow(p,color=GREEN,r=.55):
    return VGroup(*[Circle(radius=r*k,stroke_width=0,fill_color=color,
        fill_opacity=.025+.025*(4-i)).move_to(p) for i,k in enumerate([1.8,1.5,1.2,1])])


def chromosome(x,color=GREY):
    return RoundedRectangle(width=.55,height=4.8,corner_radius=.24,
        stroke_color=color,fill_color=color,fill_opacity=.12).move_to([x,0,0])


def islands():
    cs=VGroup(*[chromosome(x,c) for x,c in zip([-4.7,0,4.7],TINTS)])
    es=VGroup(*[VGroup(*[tile(c,.38,.85).move_to([x,y,0])
        for y in [-1.8,-.9,0,.9,1.8]]) for x,c in zip([-4.7,0,4.7],TINTS)])
    return cs,es


def hub(x=0,y=0,scale=1,active=False):
    ring=Circle(radius=1.15,color=TEAL,stroke_width=3,fill_color=TEAL,fill_opacity=.04)
    gene=tile(GREEN,.72,.85 if active else .25)
    es=VGroup(*[tile(TEAL,.42,.8).move_to([.92*np.cos(a),.92*np.sin(a),0])
        for a in [PI/2,7*PI/6,11*PI/6]])
    return VGroup(ring,gene,es).scale(scale).move_to([x,y,0])


def dim_hub(h):
    h[0].set_fill(opacity=.015).set_stroke(opacity=.23)
    h[1].set_fill(opacity=.08).set_stroke(opacity=.23)
    h[2].set_fill(opacity=.14).set_stroke(opacity=.23)
    return h


def competitors(dim=False):
    hs=VGroup(hub(-3.5,-.45,1.05),hub(0,.3,1.05,dim),hub(3.5,-.45,1.05))
    if dim:
        dim_hub(hs[0]); dim_hub(hs[2])
    return hs


def gene_names():
    return VGroup(*[T(t,26,GREEN).move_to([x,y,0]) for t,x,y in
        [('Olfr A',-3.5,-2.05),('Olfr B',0,-1.3),('Olfr C',3.5,-2.05)]])


def question(predict=False):
    # Alternatives have separate frames; neither is an asserted hub count.
    opts=VGroup()
    for x,label,many in [(-3,'One hub?',False),(3,'Several hubs?',True)]:
        box=Ellipse(width=4.7,height=3.5,color=GREY,stroke_opacity=.55).move_to([x,-.45,0])
        rings=VGroup(*[Circle(radius=.53 if many else 1.05,color=TEAL,stroke_opacity=.65)
            .move_to([x+dx,y,0]) for dx,y in ([(-.8,-.3),(.8,-.3),(0,-1.4)] if many else [(0,-.65)])])
        opts.add(VGroup(box,rings,T(label,26,GREY).move_to([x,.8,0])))
    return VGroup(head('One immature neuron'),VGroup(),
        T('One hub, or several?',38,YELLOW).move_to([0,2.2,0]),opts,
        foot('Predict' if predict else 'Hub number unknown',YELLOW if predict else TEXT))


def readouts():
    left=VGroup(RoundedRectangle(width=5.3,height=4.5,color=TEAL).move_to([-3, .65,0]),
        T('Multiome cells',30,TEAL).move_to([-3,2.3,0]),
        chip('RNA',ORANGE,size=28).move_to([-3,1.1,0]),
        chip('Open chromatin',TEAL,size=28).move_to([-3,-.25,0]))
    right=VGroup(RoundedRectangle(width=5.3,height=4.5,color=GREY).move_to([3,.65,0]),
        T('Separate nuclei',30).move_to([3,2.3,0]),
        chip('Dip-C',TEAL,size=28).move_to([3,1.1,0]),
        chip('Contact maps',TEAL,size=28).move_to([3,-.25,0]))
    model=chip('Combined analysis, inference',TEXT,size=28).move_to([0,-2.8,0])
    arrows=VGroup(Arrow([-3,-1.6,0],[-1.5,-2.45,0],buff=.12,color=TEXT),
        Arrow([3,-1.6,0],[1.5,-2.45,0],buff=.12,color=TEXT))
    return left,right,model,arrows


def contact_grid():
    # A toy contact model, not data: cis distance decay plus sparse trans hotspots.
    n=10
    values=np.fromfunction(lambda i,j: .08+.8*np.exp(-np.abs(i-j)/1.0),(n,n))
    for i,j in [(1,6),(3,8),(2,7)]:
        values[i,j]=values[j,i]=.68
    g=VGroup(*[Square(side_length=.58,stroke_width=.4,stroke_color=GREY,
        fill_color=interpolate_color(ManimColor('#102731'),ManimColor('#8CECE0'),float(values[i,j])),
        fill_opacity=1).move_to([(j-4.5)*.6-1.3,(4.5-i)*.6,0])
        for i in range(n) for j in range(n)])
    return g


def map_labels():
    return VGroup(T('Chromosomes',26).move_to([-1.3,-3.3,0]),
        T('Chromosomes',26).rotate(PI/2).move_to([-4.9,0,0]))


class S00Title(TitleCard):
    TITLE='Hubs That Compete'
    LESSON='One Receptor per Neuron: How Olfactory Neurons Choose'
    def construct(self):
        g=VGroup(T('One Receptor per Neuron:\nHow Olfactory Neurons Choose',26,TEXT),
            T(self.TITLE,54,font=TITLE_FONT),Line(LEFT*1.2,RIGHT*1.2,color=GOLD)).arrange(DOWN,buff=.45)
        self.play(FadeIn(g),run_time=.6); self.finish()


class S01(SpokenScene):
    def construct(self):
        gs=VGroup(*[tile(GREEN,1.2,.25).move_to([x,-.15,0]) for x in [-3.6,0,3.6]])
        lights=VGroup(*[glow(g.get_center(),r=.9) for g in gs])
        self.add(nucleus(h=5.2),lights,gs,head('Receptor genes',GREEN))
        self.at('Once a few'); self.play(gs.animate.set_fill(GREEN,.4),run_time=.5)
        self.at('how does just'); self.play(*[FadeIn(T('?',54,YELLOW).move_to([x,1.5,0])) for x in [-3.6,0,3.6]],run_time=.4)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        path=VMobject(color=GREY,stroke_width=6).set_points_smoothly([[-4,-1.4,0],[-3,2,0],[0,2.3,0],[3,0,0]])
        enhancer=tile(TEAL,.8,.8).move_to([-4,-1.4,0]); gene=tile(GREEN,1,.25).move_to([3,0,0])
        lab=T('Enhancer',28,TEAL).next_to(enhancer,DOWN,buff=.3)
        self.add(path,enhancer,gene,T('Receptor gene',28,GREEN).move_to([3,1.2,0]))
        self.at('An enhancer'); self.play(FadeIn(lab),run_time=.35)
        self.at('that raises'); loop=VMobject(color=GREY,stroke_width=6).set_points_smoothly([[1.8,0,0],[-2,2.5,0],[-2,-2.5,0],[3,0,0]])
        self.play(Transform(path,loop),enhancer.animate.move_to([1.8,0,0]),lab.animate.move_to([.4,-.9,0]),run_time=.7)
        self.at('of a gene'); self.play(gene.animate.set_fill(GREEN,.9),FadeIn(glow(gene.get_center(),r=.8)),
            FadeIn(chip('RNA',ORANGE).move_to([4.7,-1.6,0])),
            GrowArrow(Arrow([3.4,-.5,0],[4.4,-1.25,0],color=ORANGE)),
            FadeIn(T('More transcription',26,GREEN).move_to([4.2,-2.4,0])),run_time=.55); self.finish()


class S03(SpokenScene):
    def construct(self):
        cs,es=islands(); self.add(cs)
        self.at('The receptor genes'); self.play(FadeIn(es),run_time=.5)
        self.at('which the field'); label=T('The Greek Islands',30,TEAL).move_to([-2.4,2.9,0])
        self.play(FadeIn(label),GrowArrow(Arrow([-3.9,2.65,0],[-4.7,1.95,0],buff=.08,color=TEAL)),run_time=.4); self.finish()


def trans_pair():
    return chromosome(-2,GREY),chromosome(2,TINTS[2])


def touch(a,b):
    return [a.animate.rotate(-.45).shift(RIGHT*.85),b.animate.rotate(.45).shift(LEFT*.85)]


class S04(SpokenScene):
    def construct(self):
        a,b=trans_pair(); self.add(a,b)
        self.at('Contacts in trans'); self.play(*touch(a,b),run_time=.65)
        self.at('between different'); self.play(FadeIn(glow([0,1.9,0],TEAL,.38)),
            FadeIn(T('In trans: between chromosomes',28).move_to([0,2.95,0])),run_time=.35); self.finish()


class S05(SpokenScene):
    def construct(self):
        cs=VGroup(*[chromosome(x,c) for x,c in zip([-4.7,-3.5,4.7],TINTS)])
        es=VGroup(*[tile(c,.65,.85).move_to([x,y,0]) for x,y,c in zip([-4.7,-3.5,4.7],[1.5,-1.5,.4],TINTS)])
        target=hub(.6,0,2.1)
        gene=target[1].copy().move_to([4.7,-1.5,0])
        lab=head('Hub',TEAL)
        self.add(cs,es,gene)
        self.at('A hub is'); self.wait(.3)
        self.play(*[es[i].animate.move_to(target[2][i]) for i in range(3)],
            gene.animate.move_to(target[1]),run_time=1.35)
        self.play(Create(target[0]),FadeIn(lab),run_time=.5)
        self.at('often from different'); self.play(cs.animate.set_opacity(.32),run_time=.35)
        self.at('An active hub'); self.play(gene.animate.set_fill(GREEN,.95),FadeIn(glow(gene.get_center(),r=1)),
            Transform(lab,head('Active hub',TEAL)),FadeIn(T('Receptor gene',26,GREEN).move_to([.6,-1.85,0])),run_time=.55)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        a=chromosome(-2.5,TINTS[0]); b=chromosome(2.5,TINTS[2]);
        e=VGroup(glow([-2.5,0,0],TEAL,.6),Dot([-2.5,0,0],radius=.25,color=TEAL))
        g=VGroup(glow([2.5,0,0],GREEN,.6),Dot([2.5,0,0],radius=.25,color=GREEN))
        labels=VGroup(T('Enhancer',28,TEAL).move_to([-2.9,3.2,0]),T('Receptor gene',28,GREEN).move_to([2.9,3.2,0]))
        leaders=VGroup(Line([-2.9,2.9,0],[-2.5,.35,0],color=TEAL),Line([2.9,2.9,0],[2.5,.35,0],color=GREEN))
        self.add(nucleus(),a,b,e,g,labels,leaders)
        self.at('and colleagues'); self.play(FadeIn(foot('Markenscoff-Papadimitriou and colleagues, 2014')),run_time=.35)
        self.at('to contacts'); self.play(a.animate.shift(RIGHT*2),e.animate.shift(RIGHT*2),b.animate.shift(LEFT*2),g.animate.shift(LEFT*2),
            Transform(leaders[0],Line([-2.9,2.9,0],[-.5,.35,0],color=TEAL)),
            Transform(leaders[1],Line([2.9,2.9,0],[.5,.35,0],color=GREEN)),run_time=.75)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        a,b=trans_pair(); self.add(a,b)
        p=chip('Bptf',PURPLE,size=30).move_to([-3.5,1.5,0]).set_z_index(5)
        self.at('A chromatin remodeler'); self.play(FadeIn(p),FadeIn(head('Bptf: chromatin remodeler',PURPLE)),run_time=.4)
        self.at('helped make')
        # The moving pusher stays against the left chromosome as both tips converge.
        push=Arrow([-2.8,1.5,0],[-2.3,1.5,0],buff=0,color=PURPLE).set_z_index(4)
        self.play(GrowArrow(push),run_time=.2)
        self.play(p.animate.move_to([-1.6,1.9,0]),Transform(push,Arrow([-.95,1.9,0],[-.3,1.9,0],buff=0,color=PURPLE).set_z_index(4)),*touch(a,b),run_time=1)
        self.play(FadeIn(glow([0,1.9,0],PURPLE,.4)),FadeIn(foot('Facilitated contacts',PURPLE)),run_time=.35); self.finish()


class S08(SpokenScene):
    def construct(self):
        h=hub(scale=1.7,active=True)
        enh_label=T('Enhancers',28,TEAL).move_to([0,2.8,0])
        self.add(h,enh_label)
        self.at('Disrupting the contacts')
        broken=VGroup(*[Arc(radius=1.95,start_angle=a,angle=PI/3,color=TEAL,stroke_opacity=.5)
            for a in [0,2*PI/3,4*PI/3]])
        self.play(FadeOut(h[0]),FadeIn(broken),
            *[h[2][i].animate.shift(d) for i,d in enumerate([UP*.45,LEFT*1.1,RIGHT*1.1])],
            h[1].animate.set_fill(GREEN,.18),run_time=.85)
        self.at('weak expression')
        gs=VGroup(*[tile(GREEN,.85,.22).move_to([x,-1,0]) for x in [-3.4,0,3.4]])
        self.play(FadeOut(broken),*[h[2][i].animate.move_to([x,1.2,0]) for i,x in enumerate([-3.4,0,3.4])],
            ReplacementTransform(h[1],gs[1]),FadeIn(gs[0]),FadeIn(gs[2]),
            FadeIn(T('Receptor genes: weak expression',28,GREEN).move_to([0,-2,0])),
            FadeIn(foot('Disrupted contacts: associated with weak expression',size=24)),run_time=.5)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        bar=RoundedRectangle(width=10,height=1.6,corner_radius=.15,color=TEAL,fill_color=TEAL,fill_opacity=.3).move_to([0,0,0])
        notches=VGroup(*[Rectangle(width=1.6,height=.5,color=TEXT,fill_color=BG,fill_opacity=1).move_to([x,.8,0]) for x in [-2,2]])
        self.add(bar,notches,T('Enhancer',30,TEAL).move_to([0,-1.6,0]))
        self.at('What builds the hubs'); q=head('What builds the hubs?'); self.play(FadeIn(q),run_time=.3)
        a=chip('Lhx2',BLUE,size=34).move_to([-2,1.8,0]); b=chip('Ebf',YELLOW,size=34).move_to([2,1.8,0])
        self.at('Two transcription factors'); self.play(FadeOut(q),FadeIn(a),FadeIn(b),run_time=.4)
        self.at('bind cooperatively'); self.play(FadeOut(notches),a.animate.move_to([-2,1.2,0]),b.animate.move_to([2,1.2,0]),
            Create(Line([-.95,1.2,0],[.95,1.2,0],color=YELLOW,stroke_width=6)),
            FadeIn(glow([0,1.2,0],YELLOW,.7)),run_time=.35)
        self.at('with a set spacing'); self.play(GrowFromCenter(DoubleArrow([-2,2.15,0],[2,2.15,0],buff=0,color=TEXT)),
            FadeIn(T('Set motif spacing',28).move_to([0,2.8,0])),run_time=.4); self.finish()


class S10(SpokenScene):
    def construct(self):
        # Areas 65:114; distance solved from the exact two-circle overlap = 63/65.
        R=2.65; r=R*np.sqrt(65/114)
        def area(d):
            a=np.arccos(np.clip((d*d+r*r-R*R)/(2*d*r),-1,1))
            b=np.arccos(np.clip((d*d+R*R-r*r)/(2*d*R),-1,1))
            return r*r*a+R*R*b-.5*np.sqrt(max(0,(-d+r+R)*(d+r-R)*(d-r+R)*(d+r+R)))
        lo,hi=R-r,R+r
        for _ in range(60):
            mid=(lo+hi)/2
            if area(mid)>PI*r*r*63/65: lo=mid
            else: hi=mid
        d=(lo+hi)/2
        big=Circle(radius=R,color=BLUE,fill_color=BLUE,fill_opacity=.12).move_to([-.8,.1,0])
        small=Circle(radius=r,color=YELLOW,fill_color=YELLOW,fill_opacity=.12).move_to([-.8+d,.1,0])
        self.add(big,small,T('Lhx2: 114 peaks',28,BLUE).move_to([-3.8,2.8,0]),
            T('Ebf: 65 peaks',28,YELLOW).move_to([3.9,2.5,0]),
            T('2 Ebf-only',26,YELLOW).move_to([4.7,-1,0]),
            Line([3.6,-.8,0],[small.get_right()[0]-.04,.1,0],color=YELLOW))
        self.at('Nearly every'); self.play(FadeIn(T('63 of 65\nalso bound\nby Lhx2',26).move_to([.45,.2,0])),run_time=.4)
        self.at('was also bound'); self.play(FadeIn(foot('63 of 114 Lhx2 peaks overlap')),run_time=.45); self.finish()


class S11(SpokenScene):
    def construct(self):
        gene=tile(GREEN,1,.35).move_to([2.5,1.45,0])
        enh=VGroup(*[tile(TEAL,.65,.85).move_to([x,1.45,0]) for x in [-4.8,-3.8,-2.8]])
        cells=VGroup(*[Circle(radius=.42,color=GREY).move_to([x,y,0]) for y in [-.6,-1.8] for x in [-2.4,-.8,.8,2.4]])
        dots=VGroup(*[tile(GREEN,.34,.85).move_to(c) for c in cells])
        state=T('Without array',28).move_to([-3.8,2.55,0])
        self.add(gene,cells,dots[0],dots[1],state,T('Receptor gene',28,GREEN).move_to([3.8,2.55,0]),
            T('Neurons that chose this gene',28).move_to([0,.25,0]),foot('Choice frequency · schematic'))
        self.at('An inserted array'); self.wait(.45); self.play(FadeIn(enh),run_time=.35)
        with_array=T('With enhancer array',28,TEAL).move_to([-2.5,2.55,0])
        self.play(FadeOut(state),run_time=.15)
        self.play(enh.animate.shift(RIGHT*3.5),FadeIn(with_array),run_time=.65)
        self.at('raised how often'); self.play(gene.animate.set_fill(GREEN,.95),FadeIn(dots[2]),FadeIn(dots[3]),run_time=.55)
        self.at('That is a'); self.play(FadeOut(with_array),FadeIn(T('Add enhancers: gene chosen more often (schematic)',28).move_to([0,3.1,0])),run_time=.4); self.finish()


class S12(SpokenScene):
    def construct(self):
        g=contact_grid(); labels=map_labels()
        caption=T('Monahan, Horta\nand Lomvardas\n2019\n\nSchematic',26).move_to([4,-.5,0])
        # The diagonal is present during the author introduction, avoiding an empty grid.
        diag=VGroup(*[g[i*10+i] for i in range(10)])
        self.add(diag,labels,caption,T('In situ Hi-C',30).move_to([4,2,0]))
        self.at('then extended'); self.play(LaggedStart(*[FadeIn(g[i*10+j]) for i in range(10) for j in range(10) if i!=j],lag_ratio=.009),run_time=1.15)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        pts=[np.array([4.9*np.cos(a),2.4*np.sin(a),0]) for a in np.linspace(0,TAU,18,endpoint=False)]
        cs=VGroup(*[VGroup(RoundedRectangle(width=.42,height=.65,corner_radius=.15,color=GREY),tile(TEAL,.32,.9)).move_to(p) for p in pts])
        self.add(cs)
        self.at('Receptor clusters'); self.play(FadeIn(head('18 chromosomes')),run_time=.3)
        self.at('contacted one another'); lines=VGroup(*[Line(pts[i],pts[(i+7)%18],color=TEAL,stroke_opacity=.85,stroke_width=4) for i in range(18)])
        self.play(LaggedStart(*[Create(l) for l in lines],lag_ratio=.025),run_time=.8); self.bring_to_front(cs); self.finish()


class S14(SpokenScene):
    def construct(self):
        h=hub(scale=2.15,active=True); self.add(h)
        a=chip('Lhx2',BLUE,size=30).move_to([-4,2,0]); b=chip('Ldb1',PURPLE,size=30).move_to([4,2,0])
        self.at('The factors'); self.play(FadeIn(a),run_time=.3)
        self.at('and'); self.play(FadeIn(b),run_time=.3)
        self.at('regulated how'); self.play(a.animate.move_to([-3.9,0,0]),b.animate.move_to([3.9,0,0]),run_time=.5)
        # A rigid crossbar and two jaws slide shut around the lower islands.
        y=-.989; x=1.713
        bridge=VGroup(Line([-x,y-.65,0],[x,y-.65,0],color=PURPLE,stroke_width=13),
            *[VMobject(color=c,stroke_width=10).set_points_as_corners([
                [dx-.46,y+.35,0],[dx-.46,y-.65,0],[dx+.46,y-.65,0],[dx+.46,y+.35,0]])
              for dx,c in [(-x,BLUE),(x,PURPLE)]])
        bridge.shift(DOWN*.7)
        self.at('assemble and'); self.play(FadeIn(bridge),run_time=.15)
        self.play(bridge.animate.shift(UP*.7),run_time=.3)
        self.play(h[0].animate.set_stroke(width=6),Indicate(bridge,scale_factor=1.04),
            FadeIn(foot('Regulated assembly and maintenance',TEAL)),run_time=.35); self.finish()



class S15(SpokenScene):
    def construct(self):
        g=contact_grid(); labels=map_labels(); caption=foot('In situ Hi-C · schematic'); self.add(g,labels,caption)
        cells=VGroup(*[Ellipse(width=.86,height=.6,color=GREY,stroke_opacity=.6).move_to([(j-4.5)*1.1,(2.5-i)*.8-.15,0]) for i in range(6) for j in range(10)])
        self.at('But a contact map'); self.play(FadeOut(g),FadeOut(labels),FadeOut(caption),FadeIn(cells),run_time=.7)
        self.at('is an average'); self.play(FadeIn(head('Population average',YELLOW)),run_time=.35)
        self.at('It cannot show'); self.play(cells.animate.set_stroke(opacity=.35),FadeIn(foot('Many cells combined; individual hubs unresolved')),run_time=.4); self.finish()


class S16(SpokenScene):
    def construct(self):
        q=question(); self.add(q[0])
        self.at('So look inside'); self.play(FadeIn(q[3]),run_time=.5)
        self.at('Is there one'); self.play(FadeIn(q[2]),FadeIn(q[4]),run_time=.4); self.finish()


class S17Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question(True)); self.wait(5)


class S18(SpokenScene):
    def construct(self):
        hs=competitors(); self.add(nucleus(w=12.5),hs,gene_names(),
            head('Several hubs, inferred, in one developing neuron'),foot('Pourmorady and colleagues, 2024'))
        self.at('Several before'); self.play(LaggedStart(*[AnimationGroup(h[1].animate.set_fill(GREEN,.8),FadeIn(glow(h[1].get_center(),r=.7))) for h in hs],lag_ratio=.25),run_time=1)
        self.finish()


class S19(SpokenScene):
    def construct(self):
        left,right,model,arrows=readouts()
        self.add(left[0],left[1],right[0],right[1],
            VGroup(*[Line([-4.7,y,0],[-1.3,y,0],color=GREY,stroke_opacity=.3) for y in [-.8,-1.1,-1.4]]),
            VGroup(*[Square(.35,color=TEAL,fill_opacity=.18,fill_color=TEAL).move_to([x,y,0]) for x in [2.5,3,3.5] for y in [-.65,-1,-1.35]]))
        self.at('RNA'); self.play(FadeIn(left[2]),run_time=.3)
        self.at('and open chromatin'); self.play(FadeIn(left[3]),run_time=.3)
        self.at('contact maps'); self.play(FadeIn(right[2]),FadeIn(right[3]),FadeIn(model),GrowArrow(arrows[0]),GrowArrow(arrows[1]),run_time=.45); self.finish()


class S20Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(*readouts()); self.wait(2.5)


def rna_marks():
    return VGroup(*[chip('RNA',ORANGE,size=26,pad=.12).move_to(p) for p in [[-2,1.9,0],[2,1.9,0]]])


def suppression_scene():
    marks=rna_marks()
    for m,x in zip(marks,[-3,3]): m.move_to([x,1.1,0])
    return VGroup(nucleus(w=12.5),competitors(True),marks,T('Winner: Olfr B',26,GREEN).move_to([0,-1.7,0]))


class S21(SpokenScene):
    def construct(self):
        hs=competitors(); self.add(nucleus(w=12.5),hs,gene_names())
        title=head('Two further steps'); self.add(title)
        self.at('First'); self.play(Transform(title,head('Step 1: RNA',ORANGE)),hs[1][1].animate.set_fill(GREEN,.95),
            FadeIn(T('Winner',28,GREEN).move_to([0,2.45,0])),run_time=.4)
        r=rna_marks(); starts=VGroup(*[m.copy().move_to([0,.5,0]) for m in r])
        self.at('receptor RNA'); self.play(FadeIn(starts),run_time=.25)
        routes=VGroup(*[Arrow([(-.5 if i==0 else .5),.8,0],r[i].get_center(),buff=.4,color=ORANGE) for i in range(2)])
        self.at('suppressed transcription'); self.play(*[MoveAlongPath(starts[i],ArcBetweenPoints([0,.5,0],r[i].get_center(),angle=(-1 if i==0 else 1)*PI/3)) for i in range(2)],
            *[GrowArrow(a) for a in routes],run_time=.85)
        self.at('at a distance'); self.play(*[starts[i].animate.move_to([x,1.1,0]) for i,x in enumerate([-3,3])],
            *[Transform(routes[i],Arrow([(-.5 if i==0 else .5),.8,0],[x,1.1,0],buff=.4,color=ORANGE)) for i,x in enumerate([-3,3])],Transform(hs[0],dim_hub(hs[0].copy())),Transform(hs[2],dim_hub(hs[2].copy())),run_time=.6); self.finish()


class S22(SpokenScene):
    def construct(self):
        stage=suppression_scene(); self.add(stage)
        qs=VGroup(*[VGroup(DashedVMobject(RoundedRectangle(width=.8,height=.8,corner_radius=.16,color=RED),num_dashes=12),T('?',32,RED)).move_to([x,1.9,0]) for x in [-3.35,3.35]])
        self.at('The machinery behind'); self.play(*[stage[2][i].animate.move_to([x,1.9,0]) for i,x in enumerate([-2,2])],FadeIn(qs),
            *[GrowArrow(Arrow([sign*2.55,1.9,0],[sign*2.9,1.9,0],buff=0,color=ORANGE)) for sign in [-1,1]],
            *[GrowArrow(Arrow([sign*3.35,1.45,0],[sign*3.5,.9,0],buff=0,color=GREY)) for sign in [-1,1]],run_time=.4)
        self.at('is still unidentified'); self.play(FadeIn(head('Mechanism unidentified',RED)),run_time=.35); self.finish()


class S23(SpokenScene):
    def construct(self):
        # The protein is outside a smaller nucleus; the RNA-to-protein arrow crosses its boundary.
        n=nucleus(w=7.6,h=5.3).shift(LEFT*1.8)
        h=hub(-1.8,0,1.7,True); r=chip('RNA',ORANGE,size=28).move_to([.95,.8,0])
        p=chip('Receptor\nprotein',GREEN,size=28).move_to([4.4,1.1,0])
        self.add(n,h,r,Arrow([-1.1,.7,0],r.get_left(),buff=.08,color=ORANGE),T('Winner',28,GREEN).move_to([-1.8,-2.15,0]))
        self.at('Second'); self.play(FadeIn(head('Step 2: protein',GREEN)),run_time=.3)
        self.at('translation of the'); self.play(GrowArrow(Arrow(r.get_right(),p.get_left(),buff=.08,color=ORANGE)),
            FadeIn(p),FadeIn(T('Translation',26,ORANGE).move_to([2.2,2.2,0])),run_time=.6)
        self.at('then'); back=CurvedArrow(p.get_bottom(),[-.4,-1.2,0],angle=-PI/4,color=GREEN)
        self.play(Create(back),h[0].animate.set_stroke(GREEN,width=8),FadeIn(glow(h[1].get_center(),r=.9)),run_time=.6)
        self.at('at the winning'); self.play(FadeIn(foot('Stabilized transcription',GREEN)),run_time=.3); self.finish()


class S24(SpokenScene):
    def construct(self):
        # A new stage: three vertically ordered, causal steps, not the old hub diagram.
        one=chip('1  Hubs compete',TEAL,size=34).move_to([0,2.25,0])
        two=chip("2  Winner's RNA quiets rivals",ORANGE,size=34).move_to([0,0,0])
        three=chip('3  Protein stabilizes',GREEN,size=34).move_to([0,-2.25,0])
        self.add(one)
        self.at('So competition'); self.play(GrowArrow(Arrow([0,1.65,0],[0,.65,0],color=ORANGE)),FadeIn(two),run_time=.6)
        self.at('and protein then'); self.play(GrowArrow(Arrow([0,-.65,0],[0,-1.65,0],color=GREEN)),FadeIn(three),run_time=.6)
        self.at('One receptor per'); self.play(FadeIn(foot('Endpoint, not every stage',TEXT)),run_time=.4); self.finish()


class S25End(EndCard):
    LINE='One receptor per neuron is the endpoint.'

    def construct(self):
        line=T(self.LINE,40,font=TITLE_FONT)
        fit(line,max_w=11.5)
        sub=T('biochemistrypedia.com',26,TEAL)
        VGroup(line,sub).arrange(DOWN,buff=.5)
        self.play(FadeIn(line),run_time=.5)
        self.play(FadeIn(sub),run_time=.3)
        self.finish()
