"""One Type or Two? Four Ways to Count — review revision.
COLOR MAP: BLUE ganglion/type B; GOLD illustrative type A; YELLOW response;
TEAL expression; ORANGE same-cell; PURPLE shape; GREEN mosaic support;
GREY scaffolding; TEXT labels. Mosaics and evidence matches are schematic.
Coverage model: triangular-lattice density * pi * radius**2 = 4.
Response cue is exp(-(t-0.45)**2/.012), an illustrative response model.
Pie sectors are computed from the lesson's 85/11/4 percentages.
"""
import numpy as np
from bp_style import *

PURPLE='#B58CD9'
ORANGE='#F29E4C'
METHOD_COLORS=[YELLOW,TEAL,ORANGE,PURPLE]
METHOD_X=[-4.65,-1.55,1.55,4.65]
LIGHT='#BDC5D3'
RADIUS=np.sqrt(4/(np.pi*2/np.sqrt(3)))


def heading(text,color=TEXT):
    return T(text,34,color,font=TITLE_FONT).move_to([0,3.15,0])


def arr(a,b,color=GREY,w=4):
    return Arrow(a,b,buff=.1,color=color,stroke_width=w,tip_length=.18)


def gcell(color=BLUE,s=1):
    parts=[Circle(radius=.28,color=color,fill_color=color,fill_opacity=.4)]
    for dx in (-.6,0,.6):
        parts.append(Line([0,.2,0],[dx,.85,0],color=color,stroke_width=4))
        for off in (-.24,.24):
            parts.append(Line([dx,.85,0],[dx+off,1.3,0],color=color,stroke_width=3))
    parts.append(Line([0,-.28,0],[0,-1,0],color=color,stroke_width=4))
    return VGroup(*parts).scale(s)


def positions(second=False,weak=False):
    rng=np.random.default_rng(19)
    pts=[]
    for r in range(5):
        for c in range(5):
            p=np.array([c-2+(r%2)*.5-.2,(r-2)*np.sqrt(3)/2,0.])
            if second:
                a=11*DEGREES
                p=np.array([p[0]*np.cos(a)-p[1]*np.sin(a),p[0]*np.sin(a)+p[1]*np.cos(a),0])+[.2,.15,0]
            if weak:
                p+=np.r_[rng.uniform(-.35,.35,2),0]
            pts.append(p+[-1.55,-.05,0])
    return pts


def mosaic(second=False,discs=False,merged=False,weak=False):
    color=GOLD if merged or not second else BLUE
    g=VGroup()
    for p in positions(second,weak):
        dot=Dot(p,radius=.105,color=color)
        disc=Circle(radius=RADIUS,color=color,stroke_width=1.2,stroke_opacity=.35,
                    fill_color=color,fill_opacity=.075).move_to(p)
        g.add(VGroup(disc,dot) if discs else dot)
    return g


def large_mosaic(second=False,weak=False):
    return mosaic(second=second,weak=weak).shift(RIGHT*1.55).scale(1.25)


def counter(n):
    return VGroup(T('Arbors per point',26),T(str(n),64,GOLD),T('illustrative',26,LIGHT)).arrange(DOWN,buff=.22).move_to([4.5,0,0])


def question():
    return VGroup(heading('Treated as one type'),T('Pause and predict',38,GOLD).move_to([0,1.8,0]),
                  T('What happens to the spacing?',32).move_to([0,.4,0]),
                  T('And to the coverage?',32).move_to([0,-.65,0]),
                  VGroup(mosaic(),mosaic(second=True,merged=True)).scale(.42).move_to([0,-2.1,0]))


def lens(i,r=1.05):
    color=METHOD_COLORS[i]
    circle=Circle(radius=1,color=color,stroke_width=4,fill_color=color,fill_opacity=.07)
    if i==0:
        ts=np.linspace(0,1,81)
        pts=[[-.76+1.52*t,-.4+.95*np.exp(-(t-.45)**2/.012),0] for t in ts]
        cue=VMobject(color=color,stroke_width=4).set_points_as_corners(pts)
    elif i==1:
        vals=np.array([[.2,.85,.5],[.9,.3,.65],[.45,.7,.15]])
        cue=VGroup(*[Square(.37,stroke_width=0,fill_color=color,fill_opacity=float(vals[y,x])).move_to([(x-1)*.46,(y-1)*.46,0]) for y in range(3) for x in range(3)])
    elif i==2:
        cue=VGroup(Circle(.27,color=BLUE).move_to([.14,-.15,0]),Polygon([-.7,.6,0],[-.4,.72,0],[-.12,-.1,0],color=color,fill_color=color,fill_opacity=.15))
    else:
        cue=gcell(color,.58).move_to([0,0,0])
    handle=Line([.72,-.72,0],[1.16,-1.16,0],color=color,stroke_width=6)
    return VGroup(circle,cue,handle).scale(r)


def lenses(counts=False):
    labels=['Response','Expression','Same-cell','Shape']
    g=VGroup()
    for i,x in enumerate(METHOD_X):
        item=VGroup(lens(i,1.25).move_to([x,.85,0]),T(labels[i],28,METHOD_COLORS[i]).move_to([x,-1,0]))
        if i==2:
            item.add(T('RNA or shape',26,ORANGE).move_to([x,-1.55,0]))
        if counts:
            item.add(T(['32+','46','42','35+'][i],48,METHOD_COLORS[i]).move_to([x,-2.15,0]))
        g.add(item)
    return g


def evidence_lenses(y,r):
    g=VGroup()
    for i,x in enumerate(METHOD_X):
        g.add(VGroup(lens(i,r).move_to([x,y,0]),T(['Response','Expression','Same-cell','Shape'][i],26,METHOD_COLORS[i]).move_to([x,2.55,0])))
    return g


def study_title(i):
    return heading(['Light-response imaging','RNA sequencing','Same-cell recording','Electron microscopy'][i],METHOD_COLORS[i])


def study_count(i,count,detail,citation):
    return VGroup(T(count,66,METHOD_COLORS[i]).move_to([3,.65,0]),T(detail,28).move_to([3,-.65,0]),T(citation,26,LIGHT).move_to([0,-3.1,0]))


class S00Title(TitleCard):
    LESSON='Parallel Channels Out of the Eye'
    TITLE='One Type or Two? Four Ways to Count'
    def construct(self):
        self.add(T('BIOCHEMISTRYPEDIA',26,TEAL).move_to([0,2.3,0]),T(self.LESSON,28,LIGHT).move_to([0,1.35,0]))
        self.play(FadeIn(T('One Type or Two?',52,font=TITLE_FONT).move_to([0,0,0])),FadeIn(T('Four Ways to Count',38).move_to([0,-1.2,0])),run_time=.5)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        rng=np.random.default_rng(8)
        pts=rng.uniform([-3.3,-1.8],[3.3,1.8],(24,2)); pts-=pts.mean(axis=0)
        cloud=VGroup(*[Dot([x,y,0],radius=.14,color=BLUE) for x,y in pts])
        self.add(cloud,heading('One type or two?'))
        self.at('draws a group')
        self.play(Create(DashedVMobject(Ellipse(width=9,height=5.3,color=LIGHT),num_dashes=44)),run_time=.55)
        self.at('Is it one')
        self.play(Indicate(cloud,color=GOLD,scale_factor=1.04),run_time=.5)
        self.finish()


class S02Rule(SpokenScene):
    def construct(self):
        m=large_mosaic()
        self.add(m,heading('Recall the mosaic'))
        self.at('Recall the idea')
        self.play(FadeIn(T('one type',30,GOLD).move_to([-4,-2.8,0])),run_time=.3)
        self.at('spaces its cells')
        self.play(Indicate(m,color=GREEN,scale_factor=1.04),FadeIn(T('one mosaic',30,GOLD).move_to([0,-2.8,0])),run_time=.5)
        self.at('its own mosaic')
        self.play(FadeIn(T('one map',30,GOLD).move_to([4,-2.8,0])),run_time=.3)
        self.finish()


class S03One(SpokenScene):
    def construct(self):
        full=mosaic(discs=True)
        self.add(heading('One type',GOLD),mosaic())
        self.at('Here is one')
        self.play(FadeIn(VGroup(*[d[0] for d in full])),run_time=.6)
        self.at('keep their distance')
        gap=DoubleArrow([-3.75,-2.35,0],[-2.75,-2.35,0],buff=.1,color=GREEN)
        self.play(GrowFromCenter(gap),run_time=.3)
        self.at('and its arbors')
        self.play(FadeOut(gap),FadeIn(counter('≈ 4')),run_time=.4)
        self.finish()


class S04Cov(SpokenScene):
    def construct(self):
        full=mosaic(discs=True)
        # Select a point covered by exactly four finite-window arbors.
        p=np.array([-1.45,.15,0])
        candidates=[d for d in full if np.linalg.norm(d[1].get_center()-p)<RADIUS]
        assert len(candidates)==4
        cross=VGroup(Circle(.14,color=TEXT),Line([-.25,0,0],[.25,0,0]),Line([0,-.25,0],[0,.25,0])).move_to(p)
        count=counter(0)
        self.add(full,cross,count,heading('Coverage factor'))
        self.at('The coverage factor')
        self.play(FadeIn(T('Cell density × mean dendritic field area',28).move_to([0,-3.2,0])),run_time=.3)
        self.at('the number of arbors')
        for i,d in enumerate(candidates,1):
            new=counter(i)
            self.play(d[0].animate.set_stroke(GOLD,width=3,opacity=.85),ReplacementTransform(count,new),run_time=.3)
            count=new
        self.finish()


class S05Merge(SpokenScene):
    def construct(self):
        first=large_mosaic(); second=large_mosaic(second=True)
        title=heading('Two independent types')
        self.add(first,title)
        self.at('Now pour in')
        self.play(FadeIn(second,shift=UP*.6),run_time=.65)
        self.at('placed independently')
        self.play(Indicate(second,color=BLUE,scale_factor=1.04),run_time=.4)
        self.at('every cell the same')
        self.play(LaggedStart(*[d.animate.set_color(GOLD) for d in sorted(second,key=lambda d:d.get_x())],lag_ratio=.025),ReplacementTransform(title,heading('Treated as one type',GOLD)),run_time=.9)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        self.add(question())
        self.at('Predict')
        self.play(Indicate(self.mobjects[0][1],color=GOLD,scale_factor=1.04),run_time=.35)
        self.finish()


class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(question())
        track=Rectangle(width=10,height=.22,color=LIGHT,stroke_opacity=.4).move_to([0,-3.25,0])
        bar=Rectangle(width=10,height=.22,stroke_width=0,fill_color=GOLD,fill_opacity=1).move_to(track)
        remaining=ValueTracker(1)
        bar.add_updater(lambda m: m.stretch_to_fit_width(max(.02,10*remaining.get_value())).move_to([-5+max(.02,10*remaining.get_value())/2,-3.25,0]))
        self.add(track,bar)
        self.play(remaining.animate.set_value(0),run_time=5,rate_func=linear)
        bar.clear_updaters()


class S08Space(SpokenScene):
    def construct(self):
        a=large_mosaic(); b=large_mosaic(second=True)
        self.add(a,b,heading('Spacing less regular'))
        self.at('The spacing usually')
        self.play(Indicate(b,color=BLUE,scale_factor=1.02),run_time=.35)
        self.at('right beside',lead=.55)
        # Every mixed pair closer than this schematic threshold is marked.
        pairs=VGroup()
        for da in a:
            for db in b:
                dist=np.linalg.norm(da.get_center()-db.get_center())
                if dist<.60:
                    pairs.add(Ellipse(width=dist+.45,height=.45,color=RED,stroke_width=3).rotate(np.arctan2(*(db.get_center()-da.get_center())[1::-1])).move_to((da.get_center()+db.get_center())/2))
        self.play(Create(pairs),FadeIn(T('Examples: one gold + one blue',28,LIGHT).move_to([0,-3.1,0])),run_time=.5)
        self.finish()


class S09Add(SpokenScene):
    def construct(self):
        self.add(VGroup(mosaic(discs=True),mosaic(second=True,discs=True,merged=True)).scale(.88).shift(UP*.12),heading('Coverage adds'))
        count=counter('≈ 4'); self.add(count)
        self.at('coverage adds up')
        self.play(ReplacementTransform(count,counter('≈ 8')),run_time=.5)
        self.at('higher than either')
        self.play(FadeIn(T('4 + 4 ≈ 8  ·  equal illustrative types',28).move_to([0,-3.2,0])),run_time=.3)
        self.finish()


class S10Sign(SpokenScene):
    def construct(self):
        self.add(VGroup(mosaic(discs=True),mosaic(second=True,discs=True,merged=True)).scale(.88).shift(UP*.12),counter('≈ 8'),heading('High coverage'))
        self.at('can be a sign')
        self.play(FadeIn(T('Possible merge · not proof',30,GOLD).move_to([0,-2.7,0])),run_time=.3)
        self.play(FadeIn(T('Bae et al., 2018: coverage alone can mislead.',26,LIGHT).move_to([0,-3.35,0])),run_time=.25)
        self.finish()


class S11Weak(SpokenScene):
    def construct(self):
        regular=large_mosaic().scale(.88).shift(UP*.2); loose=large_mosaic(weak=True).scale(.88).shift(UP*.2)
        self.add(regular,heading('Weakly regular · still one type',GOLD),
                 T('A mosaic is strong support, not a strict rule',28,GREEN).move_to([0,-3.25,0]))
        self.at('But some real')
        disc=Circle(radius=RADIUS*1.1,color=GOLD,stroke_opacity=.5,fill_color=GOLD,fill_opacity=.08).move_to(loose[12])
        self.play(ReplacementTransform(regular,loose),FadeIn(disc),run_time=.6)
        self.at('are only')
        self.play(FadeIn(T('Some types are only weakly regular',28).move_to([0,-2.6,0])),run_time=.3)
        self.at('A mosaic is')
        self.play(Indicate(disc,color=GREEN,scale_factor=1.03),run_time=.3)
        self.finish()


class S12Methods(SpokenScene):
    def construct(self):
        ls=lenses()
        self.add(ls,heading('Four lenses · four separate studies'))
        self.at('a different part')
        self.play(LaggedStart(*[Indicate(l[0],color=c,scale_factor=1.05) for l,c in zip(ls,METHOD_COLORS)],lag_ratio=.15),run_time=.8)
        self.finish()


class S13Img(SpokenScene):
    def construct(self):
        l=lens(0,2.05).move_to([-3,.05,0])
        pending=chip('Group by\nlight response',YELLOW,30).move_to([3,.2,0])
        self.add(study_title(0),l,pending,T('Light → response',28,YELLOW).move_to([-3,-2.65,0]))
        self.at('by light response')
        self.play(Indicate(l[1],color=YELLOW,scale_factor=1.05),run_time=.4)
        self.at('and found')
        self.play(FadeOut(pending),FadeIn(study_count(0,'32+','functional types','Baden et al., 2016')),run_time=.35)
        self.finish()


class S14Seq(SpokenScene):
    def construct(self):
        l=lens(1,2.05).move_to([-3,.05,0])
        pending=chip('Group by\ngene expression',TEAL,30).move_to([3,.2,0])
        self.add(study_title(1),l,pending,T('Expression profiles',28,TEAL).move_to([-3,-2.65,0]))
        self.at('gene expression')
        self.play(Indicate(l[1],color=TEAL,scale_factor=1.05),run_time=.35)
        self.at('ended with')
        self.play(FadeOut(pending),FadeIn(study_count(1,'46','45 clusters + one split','Tran et al., 2019')),run_time=.35)
        self.finish()


def dot_blob(center,color,r=1.9):
    pts=[(-.65,.55),(.4,.8),(.65,.35),(-.6,-.3),(-.45,-.7),(.6,-.65),(.8,-.1)]
    return VGroup(Circle(r,color=color,fill_color=color,fill_opacity=.08),*[Dot([x*r*.65,y*r*.65,0],radius=.12,color=color) for x,y in pts]).move_to(center)


class S15Split(SpokenScene):
    def construct(self):
        blob=dot_blob([0,-.1,0],TEAL)
        title=heading('One RNA cluster')
        label=T('RNA cluster',30,TEAL).move_to([0,-2.45,0])
        self.add(blob,title,label)
        self.at('held two')
        right=dot_blob([2.9,-.1,0],TEAL)
        self.play(blob.animate.shift(LEFT*2.9),FadeIn(right,shift=LEFT*2.9),ReplacementTransform(title,heading('Two types inside one cluster')),FadeOut(label),
                  FadeIn(VGroup(arr([-2.9,-.9,0],[-2.9,.7,0],YELLOW),T('Dorsal',30,YELLOW).move_to([-2.9,2.15,0])),shift=RIGHT*2.9),
                  FadeIn(VGroup(arr([2.9,.7,0],[2.9,-.9,0],YELLOW),T('Ventral',30,YELLOW).move_to([2.9,2.15,0])),shift=LEFT*2.9),run_time=.65)
        self.at('known from function')
        self.play(FadeIn(T('Already known from function',28,YELLOW).move_to([0,-2.65,0])),run_time=.3)
        self.at('Clustering alone')
        self.play(FadeIn(T('Clustering alone missed the distinction',28).move_to([0,-3.3,0])),run_time=.3)
        self.finish()


class S16Same(SpokenScene):
    def construct(self):
        cell=gcell(BLUE,2.25).move_to([-.9,-.05,0])
        soma=cell[0].get_center()
        tip=soma+[-.5,.02,0]
        pipette=VGroup(Polygon(tip+[-2.65,2.1,0],tip+[-2.3,2.5,0],tip+[.02,.08,0],tip+[-.08,-.02,0],color=LIGHT,fill_color=LIGHT,fill_opacity=.08,stroke_width=2.5),
                       Line(tip+[-2.5,2.2,0],tip+[-.45,.4,0],color=TEXT,stroke_width=1.5,stroke_opacity=.65))
        title=study_title(2)
        tiles=VGroup(*[VGroup(chip(l,c,30),T('some cells',26,LIGHT).shift(DOWN*.7)).move_to([4,y,0]) for l,c,y in [('RNA',TEAL,1),('Shape',PURPLE,-1.4)]])
        self.add(cell,pipette,title,T('Cell-attached',26,ORANGE).move_to([-4.4,2.3,0]),T('Goetz et al., 2022',26,LIGHT).move_to([0,-3.25,0]))
        self.play(FadeIn(tiles),run_time=.3)
        self.at('and found')
        self.play(ReplacementTransform(title,heading('42 functional types',ORANGE)),run_time=.3)
        self.at('For some cells')
        self.play(Indicate(tiles,scale_factor=1.03),run_time=.3)
        self.at('they also read')
        self.play(*[GrowArrow(arr(soma,t.get_left()+UP*.2,c)) for t,c in zip(tiles,[TEAL,PURPLE])],run_time=.5)
        self.finish()


class S17C10(SpokenScene):
    def construct(self):
        cluster=Circle(2.05,color=TEAL,fill_color=TEAL,fill_opacity=.08).move_to([3.3,-.05,0])
        tag=T('one RNA\ncluster',30,TEAL).move_to([3.3,-.05,0])
        self.add(heading('Sustained ON direction-selective types',YELLOW),cluster,tag,T('Preferred direction',26,YELLOW).move_to([-3.3,-3.1,0]))
        sources=VGroup()
        for y,angle in zip((1.6,0,-1.6),(0,PI/2,PI)):
            d=np.array([np.cos(angle),np.sin(angle),0])*.6
            sources.add(VGroup(Circle(.72,color=YELLOW),arr(-d,d,YELLOW)).move_to([-3.3,y,0]))
        self.at('three sustained')
        # Each source carries its direction arrow from its first visible frame.
        self.play(FadeIn(sources),run_time=.5)
        self.at('shared one')
        self.play(*[GrowArrow(arr(s.get_right(),cluster.get_left()+UP*y*.5,TEAL)) for s,y in zip(sources,(1,0,-1))],run_time=.5)
        self.at('called')
        self.play(ReplacementTransform(tag,T('C10\none RNA cluster',30,TEAL).move_to(cluster)),run_time=.3)
        self.finish()


class S18Em(SpokenScene):
    def construct(self):
        box=Rectangle(width=10,height=4.1,color=PURPLE).move_to([0,.3,0])
        cells=VGroup(*[gcell(PURPLE,.95).move_to([x,-.15,0]) for x in [-3.6,-1.2,1.2,3.6]])
        self.add(study_title(3),box,cells,T('Reconstructed arbors',28,PURPLE).move_to([0,1.85,0]),
                 T('One small patch · schematic sample',26,LIGHT).move_to([0,-1.4,0]),
                 T('Bae et al., 2018',26,LIGHT).move_to([0,-3.4,0]))
        self.at('one small patch')
        self.play(Indicate(box,color=PURPLE,scale_factor=1.02),run_time=.3)
        self.at('supported at least')
        self.play(FadeIn(VGroup(T('47 clusters',38,PURPLE).move_to([-3,-2.55,0]),
                  arr([-.9,-2.55,0],[.9,-2.55,0],PURPLE),
                  T('35+ types',42,PURPLE).move_to([3,-2.55,0]))),run_time=.4)
        self.finish()


class S19Rival(SpokenScene):
    def construct(self):
        self.add(lenses(counts=True),heading('Not rival answers'))
        self.at('Each reflects')
        self.play(FadeIn(T('Method · preparation · resolution',29).move_to([0,-2.95,0])),run_time=.3)
        self.play(FadeIn(T('Authors interpret convergence on about 45 types',26,LIGHT).move_to([0,-3.55,0])),run_time=.25)
        self.finish()


class S20Trust(SpokenScene):
    def construct(self):
        ls=evidence_lenses(1.05,.85)
        chips=VGroup(*[chip(f'Type {i+1}',GOLD if i<4 else GREY,26).move_to([x,-1.85,0]) for i,x in enumerate([-5,-3,-1,1,3,5])])
        self.add(ls,chips,heading('Found by more than one method'),T('Illustrative matches across studies',26,LIGHT).move_to([0,-3.15,0]))
        # Local, non-converging groups keep the evidence links readable.
        matches=[(0,1),(0,2),(1,2),(2,3),(1,),(3,)]
        links=VGroup()
        for ch,methods in zip(chips,matches):
            for j in methods:
                links.add(Line(ls[j][0][0].get_bottom(),ch.get_top(),color=METHOD_COLORS[j],stroke_width=2.2,stroke_opacity=.7))
        self.at('more than one method')
        self.play(Create(links),run_time=.5)
        self.play(*[Indicate(c,color=GOLD,scale_factor=1.08) for c in chips[:4]],run_time=.4)
        self.finish()


def cone(color=GREY,s=.4):
    return VGroup(Polygon([-.32,.5,0],[.32,.5,0],[.17,-.35,0],[-.17,-.35,0],color=color,fill_color=color,fill_opacity=.25),Line([0,-.35,0],[0,-.65,0],color=color,stroke_width=3)).scale(s)


def fovea():
    surround=VGroup(*[cone(GREY,.6).move_to([1.9*np.cos(a),1.65+.55*np.sin(a),0]).set_opacity(.25) for a in np.linspace(0,TAU,10,endpoint=False)])
    surround.add(Ellipse(width=4.6,height=1.9,color=GREY,stroke_opacity=.18).move_to([0,1.65,0]))
    c=cone(YELLOW,1.4).move_to([0,1.55,0])
    b=VGroup(*[chip(t,LIGHT,26).move_to([x,-.65,0]) for x,t in [(-3,'ON midget bipolar'),(3,'OFF midget bipolar')]])
    g=VGroup(*[chip('Midget ganglion cell',BLUE,26).move_to([x,-2.55,0]) for x in [-3,3]])
    links=VGroup(*[arr(c.get_bottom(),t.get_top(),YELLOW) for t in b],*[arr(t.get_bottom(),u.get_top(),BLUE) for t,u in zip(b,g)])
    labels=VGroup(T('One L or M cone',26,YELLOW).move_to([3.2,2.65,0]),
                  VMobject(color=YELLOW,stroke_width=2).set_points_as_corners([[0,2.36,0],[0,2.65,0],[1.8,2.65,0]]),
                  T('private centre',28,GOLD).move_to([0,-.05,0]),
                  *[T('one to one',26,LIGHT).move_to([x,-1.75,0]) for x in [-4.35,4.35]])
    return VGroup(surround,c,b,g,links,labels)


class S21Fovea(SpokenScene):
    def construct(self):
        patch=VGroup(*[cone(GREY,.65).move_to([x*.55+(y%2)*.27,(y-3)*.66-.2,0]) for y in range(7) for x in range(-6,7)])
        self.add(heading('Macaque fovea'),patch,T('Packed with cones',28,LIGHT).move_to([0,-3.1,0]))
        self.at('In the')
        self.play(Indicate(patch,color=YELLOW,scale_factor=1.02),run_time=.35)
        self.at('one red or green')
        f=fovea()
        faint=f[2:5].copy().set_opacity(.22)
        self.play(FadeOut(patch),FadeOut(self.mobjects[2]),FadeIn(f[:2]),FadeIn(f[5][:3]),FadeIn(faint),run_time=.45)
        self.at('feeds its own')
        self.play(ReplacementTransform(faint,f[2:5]),FadeIn(f[5][3:]),FadeIn(T('Receptive-field centre pathway · schematic surround',26,LIGHT).move_to([0,-3.5,0])),run_time=.6)
        self.finish()


class S22Detail(SpokenScene):
    def construct(self):
        f=fovea(); title=heading('Private centre preserves fine detail')
        self.add(f,title)
        self.at('That private')
        pulse=Dot(f[1].get_center(),radius=.13,color=YELLOW)
        self.add(pulse)
        self.play(pulse.animate.move_to(f[2][0].get_center()),run_time=.45)
        self.play(pulse.animate.move_to(f[3][0].get_center()),run_time=.45)
        self.play(FadeOut(pulse),run_time=.15)
        self.at('Midget clusters')
        sectors=VGroup(); start=PI/2; center=np.array([-1.45,-.2,0])
        colors=[BLUE,ORANGE,PURPLE]
        for fraction,color in zip((.85,.11,.04),colors):
            sectors.add(Sector(radius=2.65,start_angle=start,angle=TAU*fraction,fill_color=color,fill_opacity=.9,stroke_color=BG,stroke_width=3).shift(center))
            start+=TAU*fraction
        labels=VGroup(T('Midget ≈ 85%',32,BG).move_to([-2.25,-.65,0]))
        # Leader endpoints are computed from wedge mid-angles.
        start=PI/2+TAU*.85
        for frac,text,y,color in [(.11,'Parasol 11%',1.1,ORANGE),(.04,'Other ≈ 4%',2.05,PURPLE)]:
            angle=start+TAU*frac/2
            p=center+2.65*np.array([np.cos(angle),np.sin(angle),0])
            labels.add(T(text,28,color).move_to([3.6,y,0]),Line(p,[2.2,y,0],color=color,stroke_width=2))
            start+=TAU*frac
        self.play(FadeOut(f),ReplacementTransform(title,heading('Sampled foveal ganglion cells')),FadeIn(sectors),run_time=.45)
        self.at('made up about')
        self.play(FadeIn(labels),run_time=.3)
        self.at('sampled foveal')
        self.play(FadeIn(T('Peng et al., 2019',26,LIGHT).move_to([3.4,-2.65,0])),run_time=.25)
        self.finish()


class S23Anc(SpokenScene):
    def construct(self):
        a=gcell(BLUE,1.85).move_to([-3.5,-.05,0]); b=gcell(BLUE,1.25).move_to([3.5,-.05,0])
        self.add(a,b,heading('Shared ancestry'),T('Mouse sustained alpha',28,BLUE).move_to([-3.5,2.55,0]),T('Macaque midget',28,BLUE).move_to([3.5,2.55,0]),T('Schematic sizes',26,LIGHT).move_to([0,-2.45,0]),T('Hahn et al., 2023',26,LIGHT).move_to([0,-3.45,0]))
        self.at('Shared ancestry')
        self.play(Create(DashedLine([-1.8,0,0],[2.3,0,0],color=LIGHT)),FadeIn(T('counterpart',26,LIGHT).move_to([.2,.5,0])),run_time=.4)
        self.at('does not mean')
        self.play(FadeIn(T('Shared ancestry ≠ shared size, frequency or job',28).move_to([0,-3,0])),run_time=.4)
        self.finish()


class S24Take(SpokenScene):
    def construct(self):
        ls=evidence_lenses(1.15,1.0)
        target=chip('Evidence for a type',GOLD,28).move_to([0,-.65,0])
        self.add(ls,heading('Combine the evidence'))
        self.at('Combine the evidence')
        links=VGroup(*[Line(l[0][0].get_bottom(),target.get_top()+RIGHT*(i-1.5)*.45,color=c,stroke_width=2.5) for i,(l,c) in enumerate(zip(ls,METHOD_COLORS))])
        self.play(Create(links),FadeIn(target),run_time=.5)
        self.at('A separate mosaic')
        panel=DashedVMobject(RoundedRectangle(width=10.8,height=1.8,corner_radius=.15,color=GREEN,stroke_opacity=.4).move_to([0,-2.2,0]),num_dashes=64)
        m=VGroup(*[Dot([x*.68+(r%2)*.34,(r-1.5)*.42-2.2,0],radius=.13,color=GREEN) for r in range(4) for x in range(-7,8)]).set_opacity(.38)
        self.play(FadeIn(panel),FadeIn(m),run_time=.4)
        self.at('strengthens the case')
        self.play(FadeIn(T('A mosaic adds support, but is not required',30,TEXT).move_to([0,-3.55,0])),run_time=.35)
        self.finish()


class S25End(EndCard):
    LINE='Agreement of response, shape and expression makes a type. A separate mosaic strengthens the case, but is not required.'
    def construct(self):
        lines=VGroup(T('Agreement of response, shape',36,font=TITLE_FONT),T('and expression makes a type.',36,font=TITLE_FONT),T('A separate mosaic strengthens the case,',32,GREEN),T('but is not required.',36,TEXT)).arrange(DOWN,buff=.35)
        self.add(lines,T('biochemistrypedia.com',26,TEAL).move_to([0,-3.1,0]))
        self.finish()
