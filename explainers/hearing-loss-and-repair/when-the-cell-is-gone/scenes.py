"""Chapter 3: data marks are computed from reported values; cells are cartoons.
COLOR MAP: BLUE hair cells; GREEN nerve; RED loss/invalid claim;
YELLOW thresholds/trial endpoint; GOLD improvement bound; GREY supporting
cells/structure; TEXT neutral labels; TEAL interactive cue.
"""
from bp_style import *


def heading(s, color=TEXT):
    return T(s,32,color,font=TITLE_FONT).move_to([0,3.12,0])


def arrow(a,b,color=GREY):
    return Arrow(a,b,buff=.05,color=color,stroke_width=5,tip_length=.18)


def child(color=GREY):
    return VGroup(Circle(.18,color=color,fill_opacity=.8).shift(UP*.65),
        RoundedRectangle(width=.44,height=.7,corner_radius=.1,color=color,fill_opacity=.35).shift(UP*.1),
        *[Line([x,-.22,0],[x,-.7,0],color=color,stroke_width=5) for x in (-.13,.13)])


def cohort(n=0):
    return VGroup(*[child(YELLOW if i<n else GREY).scale(1.3).move_to([-5+i%6*2,1.55-(i//6)*2,0]) for i in range(12)])


def hair(x=0,y=0,s=1,bundle=True,color=BLUE,short=False):
    body=RoundedRectangle(width=1.15,height=2.2,corner_radius=.25,color=color,fill_opacity=.22)
    hairs=VGroup(*[Line([dx,1.1,0],[dx,1.1+h*(.4 if short else .65),0],color=BLUE,stroke_width=5)
        for dx,h in ((-.32,.38),(0,.55),(.32,.7))])
    if not bundle: hairs.set_opacity(0)
    # Fixed body centre makes conversion preserve the epithelial baseline.
    return VGroup(body,hairs).scale(s,about_point=ORIGIN).shift([x,y,0])


def ghost(x,y,s):
    return DashedVMobject(RoundedRectangle(width=1.15*s,height=2.2*s,corner_radius=.25*s),num_dashes=24).set_color(RED).move_to([x,y,0])


def tissue():
    return VGroup(hair(-3,.1,1.75,False,GREY),hair(3,.1,1.75,False,GREY),ghost(0,.1,1.75),
        Line([-4.7,-1.825,0],[4.7,-1.825,0],color=GREY),
        T('Supporting cell',26,GREY).move_to([-3,-2.2,0]),T('Supporting cell',26,GREY).move_to([3,-2.2,0]),
        T('Hair cell lost',28,RED).move_to([0,-2.95,0]))


# y is a linear mapping of the reported ABR dB values. Baseline is censored.
Y=lambda db:-2.5+.045*db

def scale_view(value=False,question=False,bound=False):
    axis=VGroup(Line([-5,Y(0),0],[-5,2.7,0],color=GREY),
        *[VGroup(Line([-5.12,Y(d),0],[-4.88,Y(d),0],color=GREY),T(str(d),26,GREY).move_to([-5.6,Y(d),0])) for d in (0,20,40,60,80,95)],
        T('ABR threshold (dB), higher = worse hearing',28,YELLOW).move_to([0,3.25,0]),
        T('Baseline',28).move_to([-2.8,-3.12,0]),T('Week 26',28).move_to([.3,-3.12,0]))
    ceiling=VGroup(DashedLine([-4.8,Y(95),0],[4.7,Y(95),0],color=GREY),T('Test ceiling: 95 dB',26,GREY).move_to([3.1,1.35,0]))
    baseline=VGroup(arrow([-2.8,Y(95),0],[-2.8,2.3,0],YELLOW),T('> 95 dB',28,YELLOW).move_to([-2.8,2.65,0]))
    result=VGroup(Dot([.3,Y(58),0],radius=.13,color=YELLOW),T('58 dB',28,YELLOW).move_to([-.7,Y(58)-.45,0]))
    # An open top marks the unknown baseline; the improvement points DOWN.
    bracket=VGroup(Line([1.1,Y(58),0],[1.1,Y(95),0],color=GOLD,stroke_width=5),
        Line([.3,Y(58),0],[1.1,Y(58),0],color=GOLD,stroke_width=5),
        DashedLine([1.1,Y(95),0],[1.1,2.65,0],color=GOLD),
        arrow([1.5,2.55,0],[1.5,Y(58),0],GOLD),
        VGroup(T('Improvement',30,GOLD),T('> 37 dB',34,GOLD)).arrange(DOWN,buff=.3).move_to([3.3,.5,0]))
    g=VGroup(axis,ceiling,baseline,result,bracket)
    if not value: result.set_opacity(0)
    if not bound: bracket.set_opacity(0)
    if question: g.add(T('What does this tell you\nabout the improvement?',28).move_to([2.7,-1.65,0]))
    return g


def ridge(x=0,y=-.2,s=1,converted=0):
    return VGroup(*[hair(x+(i-2)*1.08*s,y,.8*s,i<converted,BLUE if i<converted else GREY,True) for i in range(5)])


def day_panels():
    left=VGroup(T('Postnatal day 1',30).move_to([-3.2,2.9,0]),chip('ATOH1',TEXT,28).move_to([-3.2,2.1,0]),
        ridge(-3.2,-.25,1,4).stretch_to_fit_height(3.8).move_to([-3.2,-.15,0]),T('Hair-cell-like',28,BLUE).move_to([-3.2,-2.4,0]),T('Greater epithelial ridge',26,GREY).move_to([-3.2,-2.9,0]))
    right=VGroup(T('Postnatal day 8',30).move_to([3.2,2.9,0]),
        RoundedRectangle(width=5.6,height=4.9,corner_radius=.2,color=GREY).move_to([3.2,-.25,0]),T('?',90).move_to([3.2,0,0]))
    return VGroup(left,right)


def mature(bundle=True,contact=True):
    cells=VGroup(hair(-3,.6,1.75,False,GREY),hair(3,.6,1.75,False,GREY),hair(0,.6,1.75,bundle,BLUE,True))
    fibre=VMobject(color=GREEN,stroke_width=8).set_points_as_corners([[-5.5,-3.2,0],[-3,-3.2,0],[0,-2.8,0]])
    touch=DashedLine([0,-2.8,0],[0,-1.325,0],color=GREEN,dash_length=.14,stroke_width=8)
    labels=VGroup(VGroup(VGroup(T('Reprogrammed',24,BLUE),T('supporting cell',24,BLUE)).arrange(DOWN,buff=.12).move_to([-4.4,-1.95,0]),
            VMobject(color=BLUE,stroke_width=2).set_points_as_corners([[-3.1,-1.9,0],[-1,-1.55,0],[-.5,-1.3,0]])),
        T('Nerve fibre',28,GREEN).move_to([-3.5,-2.65,0]),Line([-3.5,-2.9,0],[-3.5,-3.15,0],color=GREEN))
    if not contact: touch.set_opacity(0)
    return VGroup(cells,fibre,touch,labels)


class S00Title(TitleCard):
    LESSON='Hidden Hearing Loss, Gene Therapy and Regeneration'
    TITLE='Reading the Trial, and When the Cell Is Gone'
    def construct(self):
        self.add(T('BIOCHEMISTRYPEDIA',26,TEAL).move_to([0,2.3,0]),
            T(self.LESSON,26,GREY).move_to([0,1.4,0]))
        self.play(FadeIn(T('Reading the Trial,\nand When the Cell Is Gone',46,font=TITLE_FONT).move_to([0,-.3,0])),run_time=.6)
        self.finish()


class S01(SpokenScene):
    def construct(self):
        c=cohort(); self.add(c)
        self.at("met a trial's"); self.play(*[c[i].animate.set_color(YELLOW) for i in range(9)],run_time=.5)
        self.at('Does that mean'); self.play(FadeIn(T('?',80).move_to([0,2.5,0])),FadeIn(T('Most of their hearing came back?',34).move_to([0,-2.1,0])),run_time=.4)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        self.add(cohort(),heading('12 children'))
        card=VGroup(RoundedRectangle(width=11.8,height=1.85,corner_radius=.2,color=GREY).move_to([0,-2.45,0]),
            T('DB-OTO · New England Journal of Medicine',30).move_to([0,-1.85,0]),
            T('Open-label · single group',28,GREY).move_to([0,-2.45,0]),
            T('OTOF-related profound deafness',28).move_to([0,-3.05,0]))
        self.at('The DBOTO trial'); self.play(FadeIn(card),run_time=.4); self.finish()


class S03(SpokenScene):
    def construct(self):
        c=cohort();self.add(c,heading('Week 24 endpoint'))
        self.at('9 met');self.play(*[c[i].animate.set_color(YELLOW) for i in range(9)],run_time=.5)
        self.add(T('9 of 12 children',32,YELLOW).move_to([0,-1.7,0]))
        self.at('an average of');self.play(FadeIn(VGroup(T('Endpoint: average threshold',32,YELLOW),T('70 dB HL or better',36,YELLOW)).arrange(DOWN,buff=.25).move_to([0,-2.75,0])),run_time=.4)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        c=cohort(9);self.add(c)
        self.at('3 of 12');self.play(Create(VGroup(*[RoundedRectangle(width=.9,height=2.0,corner_radius=.15,color=YELLOW).move_to(c[i]) for i in range(3)])),run_time=.45)
        self.at('average normal sensitivity');self.play(FadeIn(heading('3 of 12 · average normal sensitivity')),FadeIn(T('3 children',32,YELLOW).move_to([0,-2.4,0])),run_time=.4);self.finish()


class S05(SpokenScene):
    def construct(self):
        self.add(cohort(9),heading('9 / 12',YELLOW))
        a=chip('Share of children',TEXT,30).move_to([-3.2,-1.85,0]);b=chip('Share of hearing',TEXT,30).move_to([3.2,-1.85,0])
        b[0].stretch_to_fit_height(a[0].height);b[1].set_y(a[1].get_y())
        blank=Rectangle(width=3.5,height=.55,color=GREY).move_to([3.2,-2.55,0])
        self.add(a,b,blank,T('9 / 12',38,YELLOW).move_to([-3.2,-2.55,0]))
        self.at('It is not');self.play(Create(Cross(blank,stroke_color=RED,stroke_width=8)),run_time=.4);self.wait(2);self.finish()


class S06(SpokenScene):
    def construct(self):
        g=scale_view();self.add(g[0],T('Wang and colleagues · 2024',26,GREY).move_to([1,-2,0]))
        self.at("one child's baseline");self.play(Create(g[1]),run_time=.4)
        self.at('above the test ceiling');self.play(FadeIn(g[2]),run_time=.5);self.finish()


class S07(SpokenScene):
    def construct(self):
        g=scale_view(True);self.add(g[0:3])
        self.at('the threshold was');self.play(FadeIn(g[3]),run_time=.4)
        self.at('What does that tell');self.play(FadeIn(T('What does this tell you\nabout the improvement?',28).move_to([2.7,-1.65,0])),run_time=.4);self.finish()


class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(scale_view(True,True));self.wait(5)


class S09(SpokenScene):
    def construct(self):
        g=scale_view(True);self.add(g)
        self.at('more than');g[4].set_opacity(1);self.play(g[2].animate.set_opacity(.65),Create(g[4]),run_time=.5)
        self.at('The true baseline');self.play(FadeIn(T('True baseline never measured',28).move_to([1,-1.9,0])),run_time=.4);self.finish()


class S10(SpokenScene):
    def construct(self):
        self.add(scale_view(True,bound=True))
        self.at('A floor on');self.play(FadeIn(T('Lower bound',30,GOLD).move_to([3.2,-1.1,0])),run_time=.4)
        self.at('a percentage of hearing');p=T('%',90).move_to([5.15,.15,0]);self.play(FadeIn(p),run_time=.25);self.play(Create(Line(p.get_corner(DL),p.get_corner(UR),color=RED,stroke_width=3)),run_time=.4);self.finish()


class S11(SpokenScene):
    def construct(self):
        g=tissue();self.add(g)
        self.at('When the hair cell');self.play(FadeIn(heading('The hair cell is gone',RED)),run_time=.4)
        self.at('putting back its gene');gene=chip('Gene',TEXT,28).move_to([0,2.3,0]);a=arrow([0,1.9,0],[0,.65,0]);self.play(FadeIn(gene),GrowArrow(a),run_time=.4)
        self.at('cannot help');self.play(Create(VGroup(Line([-.35,.95,0],[.35,1.55,0],color=RED,stroke_width=7),Line([-.35,1.55,0],[.35,.95,0],color=RED,stroke_width=7))),run_time=.4);self.finish()


class S11b(SpokenScene):
    def construct(self):
        g=tissue();self.add(g,heading('A new hair cell has to be made',BLUE))
        source=T('Supporting cell',28,BLUE).move_to([-3,-2.25,0])
        self.remove(g[4]);self.add(source,T('Perhaps?',30).move_to([.2,2.35,0]),
            arrow([-1.9,.45,0],[-.9,.45,0],BLUE).set_opacity(.5))
        g[0].set_fill(BLUE,opacity=.5).set_stroke(BLUE,width=6)
        self.at('has to be made');self.play(Transform(g[0],hair(-3,.1,1.75,True,BLUE,True)),run_time=1)
        self.remove(source);self.add(T('Hair-cell-like',28,BLUE).move_to([-3,-2.25,0]))
        self.at('perhaps from a surviving');self.play(Indicate(g[0],color=BLUE,scale_factor=1.03),run_time=.6);self.finish()


class S12(SpokenScene):
    def construct(self):
        gap=ghost(0,.1,1.75);damage=T('After noise damage',28,RED).move_to([0,-2.3,0])
        self.add(Line([-4.7,-1.825,0],[4.7,-1.825,0],color=GREY),heading('Adult quail · auditory epithelium'),hair(-3,.1,1.75),hair(3,.1,1.75),gap,damage,
            T('Ryals & Rubel · 1988',26,GREY).move_to([0,-3.15,0]))
        self.at('In adult quail');new=hair(0,.1,1.75);new[0].set_fill(BLUE,opacity=.45)
        self.play(FadeOut(gap),GrowFromEdge(new,DOWN),FadeOut(damage),run_time=1.5)
        self.at('within');self.play(FadeIn(T('Counts within 5% of the original',30,BLUE).move_to([0,-2.5,0])),run_time=.4);self.finish()


class S13(SpokenScene):
    def construct(self):
        left=VGroup(T('Adult mammalian cochlea',28).move_to([-3.3,3.2,0]),hair(-4.85,.1,1.75).stretch_to_fit_width(.95),hair(-1.75,.1,1.75).stretch_to_fit_width(.95),ghost(-3.3,.1,1.75).stretch_to_fit_width(.95),VGroup(T('No spontaneous',28,RED),T('replacement',28,RED)).arrange(DOWN,buff=.15).move_to([-3.3,-2.55,0]))
        right=VGroup(T('Vestibular · guinea-pig utricle',26).move_to([3.3,3.2,0]),hair(1.75,.1,1.75).stretch_to_fit_width(.95),hair(4.85,.1,1.75).stretch_to_fit_width(.95),ghost(3.3,.1,1.75).stretch_to_fit_width(.95),T('After gentamicin damage',26,RED).move_to([3.3,-2.5,0]))
        self.add(left,right,Line([-6,-1.825,0],[6,-1.825,0],color=GREY))
        self.at('One mammalian exception');self.play(Indicate(right[0],color=BLUE),run_time=.5)
        self.at('in the guinea pig utricle');self.play(FadeOut(right[3]),GrowFromEdge(hair(3.3,.1,1.75).stretch_to_fit_width(.95),DOWN),FadeOut(right[4]),run_time=.9)
        self.add(T('Hair cells reappear',28,BLUE).move_to([3.3,-2.5,0]))
        self.add(T('Forge and colleagues · 1993',28).move_to([3.3,-3.1,0]));self.wait(3.2);self.finish()


class S14(SpokenScene):
    def construct(self):
        r=ridge(0,.1,2.2);br=VGroup(Line([-5.7,-1.836,0],[5.7,-1.836,0],color=GREY),*[Line([x,-1.6,0],[x,-1.836,0],color=GREY) for x in (-5.7,5.7)])
        self.add(r,br,T('Newborn mouse · postnatal day 1',30,font=TITLE_FONT).move_to([-1.2,3.12,0]),T('Nonsensory cells, greater epithelial ridge',28,GREY).move_to([0,-2.45,0]))
        self.at('the factor');self.play(FadeIn(chip('ATOH1',TEXT,28).move_to([5,2.8,0])),run_time=.4)
        self.at('pushes');self.play(LaggedStart(*[Transform(r[i],ridge(0,.1,2.2,i+1)[i]) for i in range(4)],lag_ratio=.65),run_time=2.4)
        self.at('greater epithelial ridge');self.play(Indicate(br,color=BLUE,scale_factor=1.03),run_time=.6)
        self.at('toward hair cells');self.play(FadeIn(T('Hair-cell-like · short bundles',28,BLUE).move_to([0,-3.15,0])),run_time=.4);self.finish()


class S14b(SpokenScene):
    def construct(self):
        self.add(day_panels(),T('Would the same factor work as well?',28).move_to([0,-3.2,0]));self.at('the same factor');self.finish()


class S14cPause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(day_panels(),T('Would the same factor work as well?',28).move_to([0,-3.2,0]));self.wait(4)


class S15(SpokenScene):
    def construct(self):
        # Two separate day-8 conditions: retain the first result throughout.
        a=ridge(-3.2,-.2,1,1).stretch_to_fit_height(3.6).move_to([-3.2,-.05,0]);b=ridge(3.2,-.2,1,0).stretch_to_fit_height(3.6).move_to([3.2,-.05,0])
        self.add(heading('Postnatal day 8 · mouse · cartoon'),a,T('ATOH1 alone',30).move_to([-3.2,2.15,0]),
            T('Very few',30,BLUE).move_to([-3.2,-2.6,0]),T('Fewer than 5 per 200 µm',26).move_to([-3.2,-3.1,0]),
            Line([-5.6,-1.95,0],[5.6,-1.95,0],color=GREY),
            T('Greater epithelial ridge · schematic cells, not yield ratios',22,GREY).move_to([0,-2.15,0]))
        self.at('Adding two more factors');self.play(FadeIn(b),FadeIn(T('ATOH1 + GFI1 + POU4F3',26).move_to([3.2,2.15,0])),run_time=.4)
        self.at('gave many more');self.play(LaggedStart(*[Transform(b[i],ridge(3.2,-.2,1,5).stretch_to_fit_height(3.6).move_to([3.2,-.05,0])[i]) for i in range(5)],lag_ratio=.45),run_time=1.3)
        self.add(T('Many more',30,BLUE).move_to([3.2,-2.6,0]),T('About 50–60 per 200 µm',26).move_to([3.2,-3.1,0]))
        self.add(T('Iyer et al. · 2022 · counted at day 15',22,GREY).move_to([0,2.65,0]))
        self.wait(3.2);self.finish()


class S15b(SpokenScene):
    def construct(self):
        title=heading('Selected hair-cell gene regions')
        self.add(title,T('Untreated mice · accessibility cartoon',26,GREY).move_to([0,2.5,0]))
        def gates(x,closed):
            group=VGroup()
            for i in range(3):
                cx=x+(i-1)*1.65
                frame=RoundedRectangle(width=1.35,height=3.4,corner_radius=.1,color=GREY).move_to([cx,-.5,0])
                is_closed=i<closed
                # Hinged doors: open leaves swing aside; closed leaves block the entry.
                door=Line([cx-.58,1.08,0],[cx+.58 if is_closed else cx-.95,-2.08 if is_closed else -1.7,0],color=GREY if is_closed else BLUE,stroke_width=6)
                cue=VGroup()
                if is_closed:
                    cue.add(RoundedRectangle(width=.52,height=.42,corner_radius=.06,color=TEXT,fill_opacity=.18).move_to([cx,-.5,0]),
                        Arc(radius=.2,start_angle=0,angle=PI,color=TEXT).move_to([cx,-.15,0]))
                else:
                    cue.add(arrow([cx-.35,-.5,0],[cx+.4,-.5,0],BLUE))
                group.add(VGroup(frame,door,cue))
            return group
        a=gates(-3.3,0);b=gates(3.3,0)
        self.add(a,b,T('Postnatal day 1',28).move_to([-3.3,1.75,0]),T('Postnatal day 8',28).move_to([3.3,1.75,0]),
            T('Open · accessible',26,BLUE).move_to([-3.3,-2.65,0]))
        self.at('less accessible with age');self.play(Transform(b,gates(3.3,2)),run_time=.6)
        self.add(T('Less accessible',24).move_to([2.45,-2.65,0]),T('Open',24,BLUE).move_to([4.95,-2.65,0]),
            T('Door cartoon: access to a gene region',26,GREY).move_to([0,-3.35,0]))
        self.at('chromatin a candidate barrier');self.play(Transform(title,heading('Chromatin: a candidate barrier')),run_time=.4);self.finish()


class S16(SpokenScene):
    def construct(self):
        g=mature(False,False);self.add(g[0],g[3][0],T('Mature mouse · organ of Corti',32,font=TITLE_FONT).move_to([0,3.5,0]))
        self.at('grew rudimentary bundles');self.play(Transform(g[0][2],hair(0,.6,1.75,True,BLUE,True)),run_time=.6)
        self.at('Nerve fibers');self.play(Create(g[1]),FadeIn(g[3][1:]),run_time=.4)
        self.at('to contact them');g[2].set_opacity(1);self.play(Create(g[2]),FadeIn(T('Reported contact',28,GREEN).move_to([2.3,-2,0])),run_time=.4);self.wait(2);self.finish()


class S17(SpokenScene):
    def construct(self):
        g=mature();self.add(g,T('Mature mouse · organ of Corti',32,font=TITLE_FONT).move_to([0,3.5,0]))
        self.at('Whether those contacts');self.play(Indicate(g[2],color=GREEN,scale_factor=1.15),run_time=.4)
        self.at('working synapses');self.play(FadeIn(T('Working synapse?',30,GREEN).move_to([2.5,-1.95,0])),run_time=.4)
        self.at('the unsettled step');self.add(T('Unsettled',30).move_to([3.1,-2.65,0]));self.finish()


def chain(y,missing):
    xs=(-4,0,4); names=('Hair cell','Ribbon synapse','Nerve fibre')
    links=VGroup(*[VGroup(RoundedRectangle(width=3.3,height=1.2,corner_radius=.25,color=BLUE,stroke_width=5).move_to([x,y,0]),T(name,28).move_to([x,y,0])) for x,name in zip(xs,names)])
    if missing:
        links[0][0].become(DashedVMobject(links[0][0],num_dashes=18).set_color(RED));links[0][1].set_color(RED)
    connectors=VGroup(*[Line([x+1.65,y,0],[x+2.35,y,0],color=GREY,stroke_width=5) for x in (-4,0)])
    return VGroup(links,connectors)


class S18(SpokenScene):
    def construct(self):
        a=chain(1.6,False);b=chain(-1.4,True)
        a[0][1][0].set_color(GOLD)
        self.add(a,T('Living cell · being done in children',30).move_to([0,3.05,0]),
            T('Otoferlin replaced, in a living cell',28,GOLD).move_to([0,.55,0]))
        self.at('a surviving cell');self.play(Indicate(a[0][1][0],color=GOLD),run_time=.5)
        self.at('Rebuilding the cell');self.play(FadeIn(b),FadeIn(T('Hair cell gone · ?',30,RED).move_to([-3.6,-2.45,0])),run_time=.4)
        self.add(T('Rebuilding cells: still being tested in animals',30).move_to([0,-3.2,0]))
        self.wait(3.2);self.finish()


class S19End(EndCard):
    LINE='Replacing a link in a living cell is being done in children.\nRebuilding the cell is still being tested in animals.'
    def construct(self):
        self.add(VGroup(T('Replacing a link in a living cell',36,font=TITLE_FONT),T('is being done in children.',36,font=TITLE_FONT)).arrange(DOWN,buff=.3).move_to([0,1.25,0]),
            VGroup(T('Rebuilding the cell is still',36,BLUE,font=TITLE_FONT),T('being tested in animals.',36,BLUE,font=TITLE_FONT)).arrange(DOWN,buff=.3).move_to([0,-1,0]),
            T('biochemistrypedia.com',26,TEAL).move_to([0,-2.8,0]));self.finish()
