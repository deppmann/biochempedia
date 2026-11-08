"""Silence First: schematic cartoons, not molecular structures.
COLOR MAP: BLUE = receptor DNA / gene identity and candidate enzyme (key shape);
GREY = silent gene bodies, histones, nuclear structure; RED = repressive marks;
GREEN = expressed allele; ORANGE = receptor RNA / expression event;
TEAL = chromosome identifiers / interactive cue; GOLD = question / title accent.
Quantitative bar heights are computed from the reported counts, 662 and 212.
"""
from bp_style import *
import numpy as np
import os
from pathlib import Path

ORANGE = '#F29E4C'
PURPLE = '#B58CD9'


class TimedScene(SpokenScene):
    """Cue on the spoken word, with actual (post-wait) timing diagnostics."""
    def at(self, phrase, lead=-0.05, nth=0):
        word = self.t_of(phrase, nth)
        target = max(0, word - lead)
        if target > self.elapsed():
            self.wait(target - self.elapsed())
        log = Path(os.environ['KX_SCRIPT']).parent / 'actual_cues.log'
        with log.open('a') as f:
            f.write(f'{os.environ["KX_SCENE_ID"]} | {phrase} | word={word:.3f} visual={self.elapsed():.3f} delta={self.elapsed()-word:+.3f}\n')


def head(s, color=TEXT):
    return T(s, 32, color).move_to([0, 3.12, 0])


def foot(s, color=TEXT):
    return T(s, 28, color).move_to([0, -3.1, 0])


def arr(a, b, color=GREY):
    return Arrow(a, b, buff=.14, color=color, stroke_width=4)


def tile(color=GREY, s=1.15, op=.25):
    return RoundedRectangle(corner_radius=.12, width=s, height=s,
                            stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=op)


def genes():
    return VGroup(*[tile(s=1.55).move_to([x,y,0])
                    for x,y in [(-4,1.4),(0,1.4),(4,1.4),(-4,-1.6),(0,-1.6),(4,-1.6)]])


def flag(x=0, y=0):
    return VGroup(Line([x,y,0],[x,y+.65,0],color=RED,stroke_width=4),
                  Polygon([x,y+.65,0],[x+.42,y+.49,0],[x,y+.32,0],
                          color=RED,fill_opacity=1))


def histone(x=0,y=0,marked=False):
    # A bead with a single thick cartoon DNA line winding around it; no atoms/bonds.
    bead=Circle(radius=.7,color=GREY,fill_color=GREY,fill_opacity=.3)
    dna=ParametricFunction(lambda t: np.array([.92*np.cos(t), .44*np.sin(t)+.10*(t/PI-2),0]),
                           t_range=[0,4*PI],color=BLUE,stroke_width=7)
    ends=VGroup(Line([-.92,-.2,0],[-1.25,-.4,0],color=BLUE,stroke_width=7),
                Line([.92,.2,0],[1.25,.4,0],color=BLUE,stroke_width=7))
    tail=Line([.2,.64,0],[.35,1.12,0],color=GREY,stroke_width=5)
    g=VGroup(bead,dna,ends,tail)
    if marked: g.add(flag(.35,1.12))
    return g.move_to([x,y,0])


def mark_band(x,y,dense=False):
    # Qualitative texture, never a numerical mark count or measured ratio.
    band=Rectangle(width=3.65,height=.38,color=RED,fill_color=RED,
                   fill_opacity=.68 if dense else .14,stroke_width=0).move_to([x,y,0])
    if dense:
        band.add(*[Line([x-1.7+i*.17,y-.16,0],[x-1.55+i*.17,y+.16,0],
                        color=RED,stroke_width=2) for i in range(20)])
    return band


def allele_pair(marked=False):
    pair=VGroup()
    for x,active in [(-3.25,True),(3.25,False)]:
        c=GREEN if marked and active else GREY if marked else BLUE
        box=RoundedRectangle(width=4.5,height=1.5,corner_radius=.15,color=c,
                              fill_color=c,fill_opacity=.22).move_to([x,.3,0])
        g=VGroup(box,T('P2',44,c).move_to(box))
        if marked:
            g.add(mark_band(x,1.6,not active),
                  T('fewer repressive marks' if active else 'more repressive marks',26,RED).move_to([x,2.2,0]),
                  T('active allele' if active else 'inactive partner',30,c).move_to([x,-.95,0]))
        pair.add(g)
    return pair


def rna(x=-3.25,y=-1.85):
    return VGroup(*[Line([x-1+i*.42,y,0],[x-.8+i*.42,y+.25,0],color=ORANGE,stroke_width=6)
                    for i in range(5)],T('RNA',28,ORANGE).move_to([x,y-.55,0]))


def timeline_row(y,first,second):
    g=VGroup(arr([-5.5,y-.65,0],[5.5,y-.65,0]),
             chip(first,ORANGE if first=='expression' else RED,32).move_to([-3,y,0]),
             chip(second,ORANGE if second=='expression' else RED,32).move_to([3,y,0]),
             T('time →',26,GREY).move_to([4.6,y-1.05,0]))
    return g


def timelines():
    return VGroup(head('Predict: which timeline?',GOLD),
                  timeline_row(1.65,'expression','marks'),
                  timeline_row(-.9,'marks','expression'),
                  T('?',46,GOLD).move_to([0,-2.9,0]))


def answer():
    g=timelines();g[0].become(head('Silence appears to come first',RED));g[1].set_opacity(.22)
    g[3].become(foot('Initial repression: not explained by the winner alone'))
    g.add(T('data suggest',26,GREY).move_to([0,-.15,0]))
    return g


def nucleus():
    return Ellipse(width=11.3,height=5.6,color=GREY,stroke_width=3,
                   fill_color=GREY,fill_opacity=.04).move_to([0,-.15,0])


SPREAD=[(-3.7,1),(-2.7,-1.2),(-.7,1),(1,-1.2),(3.2,1),(3.7,-1)]
PACKED=[(-2,.7),(-1.25,.7),(-1.62,-.05),(1.3,-.8),(2.05,-.8),(1.67,-.05)]
CHROM=[BLUE,TEAL,GOLD,BLUE,TEAL,GOLD]


def nuclear_genes(packed=False):
    return VGroup(*[VGroup(tile(c,.64,.3),tile(GREY,.44,.8))
                    .move_to([x,y,0]) for (x,y),c in zip(PACKED if packed else SPREAD,CHROM)])


def foci():
    return VGroup(*[Circle(radius=1.03,color=RED,fill_color=RED,fill_opacity=.10)
                    .move_to([x,y,0]) for x,y in [(-1.62,.35),(1.67,-.4)]])


def rim():
    dots=VGroup(*[Dot([5.22*np.cos(a),-.15+2.45*np.sin(a),0],radius=.075,color=TEAL)
                  for a in np.linspace(.15,PI-.15,34)])
    label=T('lamin B receptor',26,TEAL).move_to([4.2,2.7,0])
    return VGroup(dots,label,Line([3.9,2.4,0],[3.4,1.7,0],color=TEAL,stroke_width=2))


def key(label=False):
    g=VGroup(Circle(radius=.42,color=BLUE,stroke_width=8).move_to([-.9,0,0]),
             Line([-.48,0,0],[1,0,0],color=BLUE,stroke_width=8),
             Line([.5,0,0],[.5,-.4,0],color=BLUE,stroke_width=8),
             Line([.95,0,0],[.95,-.4,0],color=BLUE,stroke_width=8))
    if label:g.add(T('Lsd1',30,BLUE).move_to([-.15,-.95,0]))
    return g


def bars(compact=False):
    # Common zero, exact linear scale: 4.25 units / 662 detected receptor genes.
    baseline=Line([-4.9,-2.15,0],[1.1 if compact else 5.5,-2.15,0],color=GREY)
    axis=VGroup(baseline,Line([-4.9,-2.15,0],[-4.9,2.45,0],color=GREY),
                T('0',26).move_to([-5.25,-2.15,0]),
                T('receptor genes detected',26).rotate(PI/2).move_to([-6.3,0,0]))
    for v in (200,400,600):
        y=-2.15+4.25*v/662
        axis.add(Line([-5,y,0],[-4.8,y,0],color=GREY),T(str(v),26,GREY).move_to([-5.5,y,0]))
    result=VGroup(axis)
    for x,v,label,c in [(-2.45,662,'control',BLUE),(2.45,212,'Lsd1 knockout',RED)]:
        h=4.25*v/662
        if compact: x = -3.4 if v==662 else -.3
        b=Rectangle(width=1.7 if compact else 2.25,height=h,color=c,fill_color=c,fill_opacity=.65).move_to([x,-2.15+h/2,0])
        result.add(VGroup(b,M(str(v),34,c).next_to(b,UP,buff=.12),T(label,28,c).move_to([x,-2.6,0])))
    return result


def assay_sub():
    return T('E18.5 · whole olfactory epithelium · RNA assay',26,GREY).move_to([0,3.25,0])


def methyl_case(n,x):
    base=chip('lysine',GREY,32,pad=.45).move_to([x,-.65,0])
    badges=VGroup(*[chip('methyl',RED,26,pad=.13).move_to([x,.45+i*.68,0]) for i in range(n)])
    return VGroup(base,badges,T(f'{n} methyl '+('group' if n==1 else 'groups'),28).move_to([x,2.65,0]))


class S00Title(TitleCard):
    TITLE='Silence First'
    LESSON='One Receptor per Neuron: How Olfactory Neurons Choose'
    def construct(self):
        self.add(T('BIOCHEMISTRYPEDIA',26,TEAL).move_to([0,2,0]),
                 T('One Receptor per Neuron:\nHow Olfactory Neurons Choose',32,TEXT).move_to([0,.75,0]))
        self.play(Write(T(self.TITLE,58,font=TITLE_FONT).move_to([0,-1,0])),
                  Create(Line([-1.3,-2,0],[1.3,-2,0],color=GOLD)),run_time=.8)
        self.finish()


class S01(TimedScene):
    def construct(self):
        g=VGroup(*[tile(s=1.4).move_to([x,y,0]) for x,y in [(-4,1.9),(0,0),(4,1.9),(-4,-1.9),(0,-1.9),(4,-1.9),(0,1.9)]])
        self.add(g,head('Receptor genes'))
        self.at('one gene wins');self.play(g[1].animate.set_color(GREEN).set_fill(GREEN,.65),run_time=.4)
        self.at('does the winner');self.play(FadeIn(T('?',78,GOLD).move_to([2,0,0])),run_time=.4)
        self.at('Or was the silence');self.play(Indicate(VGroup(g[0],g[2],g[3],g[4],g[5],g[6]),color=GREY,scale_factor=1.05),run_time=.6)
        self.finish()


class S02(TimedScene):
    def construct(self):
        pos=[(-4,0),(0,0),(4,0)]
        hs=VGroup(*[histone(x,y) for x,y in pos])
        for h in hs: h[1].stretch(1.25,0)
        self.add(hs,head('Heterochromatin',RED),foot('DNA wrapped around histone beads',BLUE))
        tight=VGroup(*[histone(x,y) for x,y in [(-2.65,.7),(0,-1),(2.65,.7)]])
        self.at('is tightly packed');self.play(Transform(hs,tight),run_time=.8)
        self.at('silenced chromatin');self.play(FadeIn(T('tightly packed · silent',30,RED).move_to([0,-2.3,0])),run_time=.4)
        self.at('Certain chemical marks')
        fs=VGroup(*[flag(*h[3].get_end()[:2]) for h in hs])
        self.play(LaggedStart(*[GrowFromPoint(f,f.get_bottom()) for f in fs],lag_ratio=.2),run_time=.8)
        self.finish()


class S03(TimedScene):
    def construct(self):
        funnel=Polygon([-1.7,1.65,0],[1.7,1.65,0],[.3,-.35,0],[-.3,-.35,0],color=GREY,fill_opacity=.18)
        tubes=VGroup(*[RoundedRectangle(width=2.5,height=1.6,corner_radius=.3,color=c).move_to([x,-1.7,0]) for x,c in [(-3,RED),(3,GREY)]])
        cells=VGroup(*[Circle(radius=.22,color=BLUE,fill_color=BLUE,fill_opacity=.6).move_to([x,2.15,0]) for x in [-.8,.8]])
        self.add(funnel,tubes,cells,head('Olfactory neurons'),T('marked',28,RED).move_to([-3,-2.85,0]),T('other',28).move_to([3,-2.85,0]))
        self.at('and colleagues');self.play(FadeIn(T('Magklara and\ncolleagues, 2011',26).move_to([4.2,1.2,0])),run_time=.3)
        self.at('sorted')
        paths=[VMobject().set_points_as_corners([c.get_center(),[0,-.2,0],[(-3 if i==0 else 3),-1.7,0]]) for i,c in enumerate(cells)]
        self.play(LaggedStart(*[MoveAlongPath(c,p) for c,p in zip(cells,paths)],lag_ratio=.15),run_time=1.2)
        self.at('from mice aged');self.play(FadeIn(T('Mice aged 6–10 weeks',28).move_to([4.2,.25,0])),run_time=.4)
        self.finish()


class S04(TimedScene):
    def construct(self):
        tube=VMobject(color=GREY,stroke_width=4).set_points_as_corners([[-4.6,1,0],[-4.6,-2.55,0],[4.6,-2.55,0],[4.6,1,0]])
        h=histone(0,-.9,True).scale(.65); others=VGroup(histone(-3,-1.1),histone(3,-1.1)).scale(.85)
        # The antibody's lower tip binds directly to the histone tail.
        anchor=h[3].point_from_proportion(.7)
        grab=VGroup(Line(anchor+[-.48,.9,0],anchor+[0,.45,0],color=GOLD,stroke_width=7),
                    Line(anchor+[.48,.9,0],anchor+[0,.45,0],color=GOLD,stroke_width=7),
                    Line(anchor+[0,.45,0],anchor,color=GOLD,stroke_width=7))
        grab.shift(UP*.85)
        label=T('antibody',28,GOLD).move_to([3,2.65,0])
        dna_target=others[0][2][0].get_start()
        self.add(tube,h,others,grab,label,T('DNA',28,BLUE).move_to([-5.4,-.4,0]),
                 Line([-5,-.4,0],dna_target,color=BLUE))
        self.at('pulled down');self.play(grab.animate.shift(DOWN*.85),run_time=.6)
        # The bottom of the selected DNA clears the open rim at y=1.
        self.at('wrapped around histones');self.play(VGroup(h,grab).animate.shift(UP*2.95),run_time=1.2)
        self.at('carrying a chosen mark');self.play(Indicate(h[-1],color=RED),run_time=.5)
        self.at('This is chromatin');self.play(FadeIn(foot('Chromatin immunoprecipitation')),run_time=.5)
        self.finish()


class S05(TimedScene):
    def construct(self):
        g=VGroup(*[tile(GREY,1.65).move_to([x,.5,0]) for x in [-4,0,4]])
        self.add(g,head('Receptor genes'))
        self.at('were enriched');self.play(*[FadeIn(mark_band(x,1.6,True)) for x in [-4,0,4]],run_time=.5)
        self.at('two repressive marks');self.play(FadeIn(VGroup(chip('H3K9me3',RED,32),chip('H4K20me3',RED,32)).arrange(RIGHT,buff=1).move_to([0,-1.1,0])),run_time=.5)
        self.at('Their data suggested');self.play(FadeIn(foot('Data suggest: silencing → detectable expression',RED)),run_time=.5)
        self.finish()


class S06(TimedScene):
    def construct(self):
        p=allele_pair();self.add(p[0],head('One receptor gene'))
        self.at('they compared');self.play(FadeIn(p[1],shift=RIGHT*.2),run_time=.4)
        self.at('two alleles');self.play(FadeIn(foot('Two alleles of P2')),run_time=.4)
        self.finish()


class S07(TimedScene):
    def construct(self):
        p=allele_pair();q=allele_pair(True);self.add(p)
        self.at('The active allele');self.play(p[0][0].animate.set_color(GREEN).set_fill(GREEN,.22),p[0][1].animate.set_color(GREEN),FadeIn(VGroup(q[0][2],q[0][3],q[0][4])),run_time=.55)
        self.at('less of the repressive marks');self.play(FadeIn(rna()),run_time=.5)
        self.at('its inactive partner');self.play(p[1][0].animate.set_color(GREY).set_fill(GREY,.22),p[1][1].animate.set_color(GREY),FadeIn(VGroup(q[1][2],q[1][3],q[1][4])),run_time=.55)
        self.finish()


class S08(TimedScene):
    def construct(self):
        winner=tile(GREEN,1.6).move_to([0,1.3,0])
        rivals=VGroup(*[tile(GREY,1.3).move_to([x,-1.3,0]) for x in [-4,0,4]])
        picture=VGroup(winner,rivals,T('chosen gene',30,GREEN).move_to([0,2.45,0]),foot('Common picture: winner silences its neighbours'))
        self.add(picture)
        self.at('A common picture');self.play(*[GrowArrow(arr([0,.4,0],[x,-.55,0],RED)) for x in [-4,0,4]],run_time=.55)
        self.at('silences the others');self.play(rivals.animate.set_fill(GREY,.6),run_time=.5)
        self.at('If the winner')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],FadeIn(timelines()[1]),run_time=.55)
        self.at('when should the marks');self.play(FadeIn(timelines()[0]),FadeIn(timelines()[2]),FadeIn(timelines()[3]),run_time=.5)
        self.finish()


class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(timelines())
        track=Line([-3,-3.45,0],[3,-3.45,0],color=GREY,stroke_width=5)
        progress=Line([-3,-3.45,0],[-2.99,-3.45,0],color=GOLD,stroke_width=7)
        self.add(track,progress);self.play(Transform(progress,Line([-3,-3.45,0],[3,-3.45,0],color=GOLD,stroke_width=7)),run_time=5,rate_func=linear)


class S10(TimedScene):
    def construct(self):
        g=timelines();self.add(g)
        self.at('Only after');self.play(Indicate(g[1],color=ORANGE,scale_factor=1.02),run_time=.55)
        self.at('Instead');self.play(g[1].animate.set_opacity(.22),Indicate(g[2],color=RED,scale_factor=1.02),FadeOut(g[3]),run_time=.55)
        self.at('come first');self.play(Transform(g[0],head('Silence appears to come first',RED)),FadeIn(T('data suggest',26,GREY).move_to([0,-.15,0])),run_time=.5)
        self.at('the winner did not');self.play(FadeIn(foot('Broad silence: not started by the winner alone')),run_time=.5)
        self.at('by itself');self.play(Indicate(g[2],color=RED,scale_factor=1.02),run_time=.4)
        self.finish()


class S11Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(answer());self.wait(2.5)


class S12(TimedScene):
    def construct(self):
        self.add(allele_pair(True))
        self.at('cannot settle');self.play(FadeIn(T('≠',64,RED).move_to([0,-2.5,0])),run_time=.4)
        self.at('Comparing two alleles');self.play(FadeIn(T('association',44).move_to([-3.25,-2.5,0])),run_time=.4)
        self.at('is an association');self.play(FadeIn(T('cause',44).move_to([3.25,-2.5,0])),run_time=.4)
        self.finish()


class S13(TimedScene):
    def construct(self):
        a=chip('Less repression',GREEN,38,pad=.65).move_to([-3.3,0,0]);b=chip('Expression',ORANGE,38,pad=.65).move_to([3.5,0,0])
        self.add(a,b,head('Which change starts the choice?',GOLD))
        self.at('the chosen allele');self.play(Indicate(a,color=GREEN,scale_factor=1.03),run_time=.4)
        self.at('It does not say');self.play(GrowArrow(arr([-3.3,1.3,0],[3.5,1.3,0])),FadeIn(T('marks drop, then expression?',30).move_to([0,2.05,0])),run_time=.5)
        self.at('which change starts');self.play(GrowArrow(arr([3.5,-1.3,0],[-3.3,-1.3,0])),FadeIn(T('expression, then marks drop?',30).move_to([0,-2.1,0])),FadeIn(T('?',52,GOLD).move_to([0,-3,0])),run_time=.5)
        self.finish()


class S14(TimedScene):
    def construct(self):
        g=nuclear_genes();self.add(nucleus(),g,head('Silent receptor genes',RED),foot('Grey = silent · green = expressed'))
        self.at('separate line of evidence');self.play(Indicate(g,scale_factor=1.02,color=GREY),run_time=.4)
        self.at('gathered together');self.play(*[t.animate.move_to([x,y,0]) for t,(x,y) in zip(g,PACKED)],run_time=.8)
        self.finish()


class S15(TimedScene):
    def construct(self):
        g=nuclear_genes(True);title=head('Receptor genes gather into foci');bottom=foot('Border colours = different chromosomes')
        self.add(nucleus(),g,title)
        self.at('and colleagues');self.play(Transform(title,head('Clowney and colleagues, 2012')),run_time=.4)
        self.at('different chromosomes');self.play(FadeIn(bottom),run_time=.4)
        self.at('a few dense foci');self.play(FadeIn(foci()),FadeIn(T('dense foci',30,RED).move_to([0,-2,0])),run_time=.5)
        self.at('as neurons mature');self.play(Transform(bottom,foot('As neurons mature → dense foci')),run_time=.4)
        self.finish()


class S16(TimedScene):
    def construct(self):
        g=nuclear_genes(True);f=foci();r=rim()
        # Keep the same two foci as s15, but spread their contents before compaction.
        for i,t in enumerate(g):
            center=np.array([-1.62,.35,0] if i<3 else [1.67,-.4,0])
            t.move_to(center+(t.get_center()-center)*1.8)
        for spot in f: spot.scale(1.45)
        self.add(nucleus(),g,f,r,head('Receptor leaves the rim'))
        self.at('in step with')
        self.play(FadeOut(r),*[t.animate.move_to([x,y,0]) for t,(x,y) in zip(g,PACKED)],
                  *[spot.animate.scale(1/1.45) for spot in f],run_time=2.15)
        self.finish()


class S17(TimedScene):
    def construct(self):
        g=nuclear_genes(True);f=foci();r=rim();count=foot('Normal choice: 1 receptor on',GREEN).shift(DOWN*.25)
        g[0][1].set_color(GREEN).set_fill(GREEN,.8)
        self.add(nucleus(),g,f,head('Restore the rim protein'),count)
        self.at('Forcing');self.play(FadeIn(r),run_time=.5)
        self.at('broke up the foci');self.play(FadeOut(f),*[t.animate.move_to([x,y,0]) for t,(x,y) in zip(g,[(-3.5,.65),(-2.6,-1.2),(-.7,.8),(1,-1.2),(3,.65),(3.5,-1.1)])],run_time=.65)
        self.at('singular expression was disrupted');self.play(*[g[i][1].animate.set_color(GREEN).set_fill(GREEN,.8) for i in [0,2,4]],Transform(count,foot('Foci broken up → 3 receptors on at once',GREEN).shift(DOWN*.25)),run_time=.6)
        self.finish()


class S18(TimedScene):
    def construct(self):
        g=genes();k=key(True).move_to([-4.5,-.1,0]);k[-1].set_opacity(0);title=head('How does one gene escape?');self.add(g,title,foot('Grey = silent · green = released / expressed'))
        self.at('every gene starts silent');self.play(Indicate(g,color=GREY,scale_factor=1.02),run_time=.4)
        self.at('something must let');self.play(Indicate(g[1],color=GOLD,scale_factor=1.06),run_time=.5)
        self.at('In the model');self.play(Transform(title,head('Model: a candidate key',BLUE)),run_time=.4)
        self.at('candidate key');self.play(FadeIn(k),run_time=.35)
        self.at('is the enzyme');self.play(k.animate.move_to([-1.5,.25,0]),run_time=.6)
        self.play(k[-1].animate.set_opacity(1),g[1].animate.set_color(GREEN).set_fill(GREEN,.65),run_time=.45)
        self.finish()


class S19(TimedScene):
    def construct(self):
        tissue=VGroup(RoundedRectangle(width=8.5,height=4.05,corner_radius=.2,color=GREY,fill_color=GREY,fill_opacity=.15),
                      *[Line([x,-2.025,0],[x,2.025,0],color=GREY,stroke_width=2) for x in [-2.5,-1.25,1.25,2.5]],
                      Line([-4.25,0,0],[4.25,0,0],color=GREY,stroke_width=2)).move_to([0,-.1,0])
        k=key(True).move_to([0,-.05,0]);lab=T('mouse olfactory epithelium',30).move_to([0,2.45,0])
        self.add(tissue,k,lab)
        self.at('and colleagues');self.play(FadeIn(head('Lyons and colleagues, 2013')),run_time=.3)
        self.at('deleted it early');cross=Cross(k,stroke_color=RED,stroke_width=7);self.play(Create(cross),Transform(lab,T('Olfactory epithelium · Lsd1 deleted early',30).move_to([0,2.45,0])),run_time=.5)
        self.at('then read the')
        dust=VGroup(*[Square(side_length=.48,color=GREY,fill_color=GREY,fill_opacity=.7).move_to([x,y,0]) for x,y in [(-4.7,-.7),(-3.7,-.45),(-2.7,-.85),(-4.9,-1.55),(-3.85,-1.55),(-2.6,-1.65),(-4.4,-2.25),(-3.15,-2.3)]])
        pestle=RoundedRectangle(width=.95,height=2.8,corner_radius=.2,color=TEXT,fill_color=GREY,fill_opacity=.4).rotate(-.4).move_to([-3.7,.7,0])
        self.play(ReplacementTransform(tissue,dust),FadeOut(k),FadeOut(cross),FadeIn(pestle),run_time=.4)
        self.play(pestle.animate.shift(DOWN*.55),run_time=.22);self.play(pestle.animate.shift(UP*.3+RIGHT*.35),run_time=.22)
        self.at('the RNA');self.play(GrowArrow(arr([-.9,-.65,0],[1.1,-.65,0])),FadeIn(rna(3.45,-.3).scale(1.65)),run_time=.35)
        self.at('whole tissue');self.play(FadeIn(foot('Grind whole tissue → measure pooled RNA')),run_time=.35)
        self.finish()


class S20(TimedScene):
    def construct(self):
        b=bars();self.add(assay_sub(),b[0],b[1],b[2][2])
        start=b[1][0].copy().move_to([2.45,b[1][0].get_y(),0]).set_color(RED)
        self.add(start)
        self.at('detected about');self.play(Transform(start,b[2][0]),FadeIn(b[2][1]),run_time=.5)
        self.at('a third as many');self.play(FadeIn(T('212 / 662 = 32%',30,RED).move_to([2.45,1.5,0])),run_time=.4)
        self.at('Early loss impaired');self.play(FadeIn(foot('Early loss impairs initiation of receptor expression')),run_time=.5)
        self.finish()


class S21(TimedScene):
    def construct(self):
        dep=chip('Dependence',BLUE,42,pad=.5).move_to([0,1.3,0])
        self.add(head('Chemistry calls for care',RED),dep,T('RNA assay: 662 → 212',30,BLUE).move_to([0,2.45,0]))
        self.at('not mechanism');self.play(FadeIn(T('≠',64,RED).move_to([0,0,0])),FadeIn(chip('Mechanism',GREY,42,pad=.5).move_to([0,-1.5,0])),run_time=.5)
        self.at('chemistry gives');self.play(FadeIn(foot('Next: can Lsd1 remove the methyl groups?')),run_time=.5)
        self.finish()


class S22(TimedScene):
    def construct(self):
        cases=VGroup(*[methyl_case(n,x) for n,x in [(1,-4),(2,0),(3,4)]])
        k=key().scale(.7).move_to([-5.3,-1.65,0]);self.add(cases,k,foot('Lsd1 (drawn as a key)',BLUE))
        # A key tooth contacts each stack; the badges slide along the shaft into its ring.
        self.at('can remove')
        self.play(k.animate.shift(cases[0][1][0].get_center()-k[3].get_end()),run_time=.3)
        self.play(cases[0][1][0].animate.move_to(k[0].get_center()).scale(.2).set_opacity(0),run_time=.65)
        self.at('or two methyl')
        self.play(k.animate.shift(cases[1][1][0].get_center()-k[3].get_end()),run_time=.3)
        self.play(cases[1][1][0].animate.move_to(k[0].get_center()).scale(.2).set_opacity(0),run_time=.5)
        self.play(k.animate.shift(UP*.68),run_time=.2)
        self.play(cases[1][1][1].animate.move_to(k[0].get_center()).scale(.2).set_opacity(0),run_time=.5)
        self.at('It cannot remove')
        self.play(k.animate.shift(cases[2][1][0].get_center()-k[3].get_end()),run_time=.3)
        self.play(k.animate.shift(LEFT*1.15+DOWN*.45),
                  FadeIn(T('3 stay',30,RED).move_to([4,-2,0])),run_time=.6,rate_func=rush_from)
        self.play(k.animate.shift(RIGHT*.45),run_time=.25)
        self.play(k.animate.shift(LEFT*.45),Indicate(cases[2][1],color=RED,scale_factor=1.08),run_time=.4)
        self.finish()


class S23(TimedScene):
    def construct(self):
        h=histone(0,-.1,True).scale(1.5);k=key(True).move_to([-3.4,.3,0])
        k[-1].next_to(VGroup(*k[:4]),UP,buff=.25)
        bottom=foot('Lsd1 alone');self.add(h,k,head('Trimethyl mark stays',RED),bottom)
        self.at('cannot strip');self.play(k.animate.shift(RIGHT*2.7+UP*.7),run_time=.35)
        self.play(k.animate.shift(LEFT*.9+DOWN*.4),Indicate(h[-1],color=RED,scale_factor=1.08),run_time=.4)
        self.at('another demethylase')
        unknown=VGroup(DashedVMobject(RoundedRectangle(width=4,height=1.65,corner_radius=.2,color=BLUE),num_dashes=30),T('?',48,BLUE)).move_to([3.7,.3,0])
        self.play(VGroup(h,k).animate.shift(LEFT*1.65),FadeIn(unknown),run_time=.5)
        self.at('or an intermediate');self.play(Transform(bottom,foot('Another enzyme or an intermediate step may be needed')),run_time=.5)
        self.finish()


class S24(TimedScene):
    def construct(self):
        b=bars();sub=assay_sub();self.add(b,sub)
        self.at('bulk tissue');self.play(Indicate(sub,color=TEXT,scale_factor=1.02),run_time=.35)
        self.at('depends on the assay');self.play(FadeIn(foot('Counts depend on the assay and sampled cells')),run_time=.4)
        self.at('So the key');k=key().move_to([4.3,1.1,0]);self.play(Transform(b,bars(compact=True)),FadeIn(k,shift=LEFT*.4),run_time=.35)
        self.at('is shorthand');self.play(FadeIn(T('Lsd1-dependent\nstep',28,BLUE).move_to([4.15,-.1,0])),FadeIn(T('direct action\nnot shown',26,TEXT).move_to([4.15,-1.8,0])),run_time=.4)
        self.at('dependent step');self.play(Indicate(k,color=BLUE,scale_factor=1.03),run_time=.35)
        self.finish()


class S25(TimedScene):
    def construct(self):
        g=VGroup(*[tile(GREY,1.2).move_to([x,y,0]) for x,y in [(-5,.6),(-3.5,.6),(-5,-1),(-3.5,-1)]])
        self.add(g)
        self.at('broad silence comes first');self.play(FadeIn(T('Silence first',34,RED).move_to([-4.25,2.4,0])),FadeIn(T('Broad repression',28,TEXT).move_to([-4.25,-2.6,0])),run_time=.4)
        self.at('a key is needed');self.play(FadeIn(key(True).scale(1.2).move_to([0,.4,0])),FadeIn(T('Candidate key',32,BLUE).move_to([0,2.4,0])),run_time=.4)
        self.at('to escape it');self.play(FadeIn(T('Lsd1-dependent\nstep',28,TEXT).move_to([0,-2.25,0])),run_time=.4)
        winner=tile(GREEN,1.65).move_to([4.25,.3,0])
        self.at('The winner acts later');self.play(FadeIn(winner),FadeIn(T('Winner later',34,GREEN).move_to([4.25,2.4,0])),run_time=.4)
        self.at('quieting rivals');self.play(FadeIn(T('Quiets rivals',28,RED).move_to([4.25,-1.35,0])),run_time=.4)
        self.at('holding its place');self.play(Create(RoundedRectangle(width=2.1,height=2.1,corner_radius=.18,color=GREEN,stroke_width=4).move_to(winner)),FadeIn(T('Holds the choice',28,TEXT).move_to([4.25,-2.6,0])),run_time=.4)
        self.finish()


class S26End(EndCard):
    LINE='The broad silence comes first.'
    def construct(self):
        self.add(T(self.LINE,44,font=TITLE_FONT).move_to([0,.5,0]),
                 T('biochemistrypedia.com',30,TEXT).move_to([0,-.7,0]))
        self.finish()
