"""Chapter 6: Where Is the Netrin?

COLOR MAP (from ../scenes.old.py; shared chapter palette):
YELLOW netrin; BLUE growth cone / axon; TEAL DCC; PURPLE UNC5;
ORANGE cyclic AMP; PINK DCC antibody; GREEN attraction / supported course;
RED repulsion / blocked signal; GREY anatomy / de-emphasized objects.
Only scenes.py and requested review outputs are authored here; CHAPTERS.md is unchanged.
Plots: C=k/r; occupancy=C/(C+Kd); adaptation is a schematic first-order
baseline reset, R(t)=sum H(t-ti)*exp(-(t-ti)/tau), not experimental data.
Anatomical outlines and axon routes are schematics reused from the reference film.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
PINK = '#E58BD0'


def label(text, x=0, y=0, color=TEXT, size=26):
    return T(text, max(26, size), color).move_to([x, y, 0])


def heading(text):
    return label(text, 0, 3.15, size=32)


def smooth(points):
    m = VMobject()
    m.set_points_smoothly([np.array(p, float) for p in points])
    return m


def body(center, scale=1):
    # Same disc and filopodia as the reference film.
    c = np.array(center, float)
    disc = Circle(radius=scale, color=BLUE, stroke_width=5,
                  fill_color=BLUE, fill_opacity=.22).move_to(c)
    fil = VGroup()
    for deg in [0, 150, 180, 210]:
        u = np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0])
        fil.add(Line(c + scale*u, c + 1.3*scale*u, color=BLUE, stroke_width=4))
    return VGroup(disc, fil)


def cord(center=(-2.5, -.25, 0), scale=1.34, floor=True, progenitor=True, wrong=False):
    # Reference film's transverse map, enlarged and with a broader VZ domain.
    c = np.array(center, float)
    def p(x, y):
        return c + np.array([x, y, 0])*scale
    outline = Ellipse(width=4.6*scale, height=4.5*scale, color=GREY, stroke_width=3).move_to(c)
    mid = DashedLine(p(0, 2.15), p(0, -2.15), color=GREY, stroke_width=1.5)
    canal = Ellipse(width=.55*scale, height=1.5*scale, color=GREY).move_to(p(0, .55))
    fp = RoundedRectangle(width=.65*scale, height=.28*scale, corner_radius=.06,
                          color=GREY, fill_color=GREY, fill_opacity=.3).move_to(p(0, -2.05))
    vz = VGroup(*[Dot(p(x, y), radius=.09*scale, color=GREY)
                 for x in [-.48, .48] for y in [-.75, -.35, .05, .45, .85]])
    anatomy = VGroup(outline, mid, canal, fp, vz)
    # Analytic ellipse coordinates for the pial deposit band.
    theta = np.linspace(2.65, 4.5, 18)
    deposits = VGroup(*[Dot(p(side*abs(2.16*np.cos(t)), 2.1*np.sin(t)), radius=.06*scale, color=YELLOW)
                        for side in [-1,1] for t in theta])
    fcue = VGroup(*[Dot(p(x, -2.05), radius=.075*scale, color=YELLOW) for x in [-.2, 0, .2]])
    source = VGroup(*[Polygon(*[p(x,y) for x,y in pts], color=YELLOW,
        stroke_width=1, fill_color=YELLOW, fill_opacity=.27) for pts in [
        [(-.38,1.05),(-.85,.9),(-1.0,.25),(-.85,-.7),(-.35,-1.6),(-.23,-.6),(-.3,.3)],
        [(.38,1.05),(.85,.9),(1.0,.25),(.85,-.7),(.35,-1.6),(.23,-.6),(.3,.3)]]],
        vz.copy().set_color(YELLOW))
    points = [(-1.55, 1.4), (-1.9, .55), (-1.7, -.65), (-.85, -1.8), (.4, -2.0), (1.55, -1)]
    if wrong:
        points = [(-1.55, 1.4), (-1.65, .6), (-.7, .1), (-.95, .8), (-.25, 1.35)]
    route = smooth([p(x, y) for x, y in points]).set_stroke(BLUE, 6)
    tip = body(p(*points[-1]), .15*scale)
    neurons = VGroup(*[Dot(p(x, 1.4), radius=.12*scale, color=BLUE) for x in [-1.55, 1.55]])
    return VGroup(anatomy, deposits if progenitor else VGroup(), fcue if floor else VGroup(),
                  source if progenitor else VGroup(), route, tip, neurons)


def map_base(scene, floor=True, progenitor=True, route=True, center=(-2.5, -.25, 0), scale=1.34, wrong=False):
    m = cord(center, scale, floor, progenitor, wrong)
    scene.add(m[0], m[6])
    if route:
        scene.add(m[4], m[5])
    return m


def map_labels():
    return VGroup(label('dorsal neurons',3.7,2.15,BLUE),
        label('floor plate',3.7,-2.6,GREY),
        label('progenitors\naround the canal',3.7,.9,YELLOW),
        Arrow([1.7,.8,0],[-1.45,.35,0],color=GREY,buff=.12),
        label('pial surface',3.7,-.95,GREY),
        Arrow([2,-1.15,0],[.25,-1.75,0],color=GREY,buff=.12),
        Arrow([1.95,2.05,0],[-.42,1.63,0],color=BLUE,buff=.12),
        Arrow([2.3,-2.75,0],[-2.15,-3,0],color=GREY,buff=.12))


def gradient(center=(-2.5,-.25,0), scale=1.34):
    # Exact circle/square intersections clip the computed inverse-distance field.
    c=np.array(center); boundary=Ellipse(width=4.56*scale,height=4.46*scale).move_to(c)
    cells=VGroup()
    for x in np.arange(-2.3,2.31,.24):
        for y in np.arange(-2.25,2.26,.24):
            if (x/2.3)**2+(y/2.25)**2<1.2:
                r=max(.25,np.hypot(x,y+2.05))
                tile=Square(side_length=.245*scale).move_to(c+np.array([x,y,0])*scale)
                clipped=Intersection(boundary,tile,stroke_width=0,fill_color=YELLOW,
                                     fill_opacity=min(.65,.38/r))
                cells.add(clipped)
    return cells.set_z_index(-2)


def dish_stage():
    gel=RoundedRectangle(width=12,height=6.1,corner_radius=.35,color=GREY,
                         fill_color=GREY,fill_opacity=.04).move_to([0,-.2,0])
    bead=Dot([-4.6,0,0],radius=.32,color=YELLOW)
    cone=body([2,0,0],1.75)
    contours=VGroup(*[Arc(radius=r,start_angle=-.55,angle=1.1,arc_center=[-4.6,0,0],
        color=YELLOW,stroke_opacity=.65/r,stroke_width=5) for r in [1,2.2,3.6,4.5]])
    return VGroup(gel,bead,cone,contours)


def binding_plot(compact=False):
    axes=Axes(x_range=[-2.35,2.35,1],y_range=[0,1,.5],x_length=10.6,y_length=5.25,
              tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([.25,-.15,0])
    axes.y_axis.set_opacity(0)
    axes.add(Line(axes.c2p(-2.35,0),axes.c2p(-2.35,1),color=GREY))
    curve=axes.plot(lambda u:10**u/(1+10**u),x_range=[-2.35,2.35,.02],color=TEAL)
    labs=VGroup(label('bound',-5.55,3.05,TEAL),label('concentration / Kd (log scale)',0,-3.45,GREY))
    for u,t in [(-2,'0.01'),(0,'1'),(2,'100')]:
        labs.add(label(t,*axes.c2p(u,0)[:2],GREY).shift(DOWN*.3))
    for v,t in [(0,'0'),(.5,'½'),(1,'1')]:
        labs.add(label(t,*axes.c2p(-2.35,v)[:2],GREY).shift(LEFT*.38))
    kd=DashedLine(axes.c2p(0,0),axes.c2p(0,1),color=YELLOW,stroke_opacity=.5)
    return VGroup(axes,curve,labs,kd)


def prediction_frame():
    p=binding_plot()
    # Keep the true binding coordinates above; compare the tiny differences below
    # on one common, enlarged scale (100 scene units per bound fraction).
    p[0].stretch_to_fit_height(3.0).move_to([.25,.8,0])
    p[1].become(p[0].plot(lambda u:10**u/(1+10**u),x_range=[-2.35,2.35,.02],color=TEAL))
    p[2].become(VGroup(label('bound',-5.6,2.65,TEAL)))
    for v,t in [(0,'0'),(.5,'½'),(1,'1')]:
        p[2].add(label(t,*p[0].c2p(-2.35,v)[:2],GREY).shift(LEFT*.38))
    for u,t in [(-2,'0.01'),(0,'1'),(2,'100')]:
        p[2].add(label(t,*p[0].c2p(u,0)[:2],GREY).shift(DOWN*.28))
    p[2].add(label('concentration / Kd (log scale)',0,-1.28,GREY))
    p[3].become(DashedLine(p[0].c2p(0,0),p[0].c2p(0,1),color=YELLOW,stroke_opacity=.5))
    pairs=VGroup()
    for u,x,t in [(-2,-4.3,'0.01 Kd'),(0,0,'Kd'),(2,4.3,'100 Kd')]:
        c=10**u; a=p[0].c2p(u,c/(1+c)); v=u+np.log10(1.1)
        b=p[0].c2p(v,1.1*c/(1+1.1*c))
        width=100*(1.1*c/(1+1.1*c)-c/(1+c))
        start=np.array([x-width/2,-2.65,0]); end=start+RIGHT*width
        inset=VGroup(RoundedRectangle(width=3.75,height=1.2,corner_radius=.12,color=GREY)
            .move_to([x,-2.35,0]),label(t,x,-2.02,YELLOW),
            Line(start,end,color=YELLOW,stroke_width=5),
            Line(start+DOWN*.17,start+UP*.17,color=GREY,stroke_width=3),
            Line(end+DOWN*.17,end+UP*.17,color=YELLOW,stroke_width=3))
        pairs.add(VGroup(Dot(a,radius=.085,color=GREY),Dot(b,radius=.055,color=YELLOW),inset))
    return VGroup(p,pairs,heading('Same 10% cue: C and 1.1 C'),
        label('Where is the bound difference largest?',0,3.65,size=28),
        label('Bound differences · one common enlarged scale',0,-3.45,GREY))


def table_frame():
    g = VGroup(heading('Bound receptors on the two sides'))
    for x, s in [(-4.2,'background'),(-1.6,'far side'),(.9,'near side'),(4,'difference')]:
        g.add(label(s,x,2.15,GREY,24))
    for i,c in enumerate([.01,1,100]):
        y = 1.05-i*1.35
        a,b = c/(1+c),1.1*c/(1+1.1*c)
        g.add(label(['0.01 × Kd','Kd','100 × Kd'][i],-4.2,y,size=26),
              label(f'{100*a:.2f}%' if i!=1 else f'{100*a:.1f}%',-1.6,y,TEAL,28),
              label(f'{100*b:.2f}%' if i!=1 else f'{100*b:.1f}%',.9,y,TEAL,28),
              label(f'{100*(b-a):.1f} points',4,y,YELLOW if i==1 else GREY,26))
    g.add(RoundedRectangle(width=11.7,height=1,corner_radius=.12,color=YELLOW,stroke_width=3).move_to([0,-.3,0]))
    return g


def receptor_panel(p=.6,q=.4,x=0,y=-.2,scale=1):
    # Discrete cartoon counts, not a measurement of receptor number.
    cone=body([x,y,0],1.38*scale)
    receptors=VGroup()
    for side,prob in [(-1,p),(1,q)]:
        for i in range(10):
            rec=Rectangle(width=.26*scale,height=.29*scale,color=TEAL,stroke_width=2,
                fill_color=YELLOW if i<round(10*prob) else BG,fill_opacity=1)
            rec.move_to([x+side*1.95*scale,y+(i-4.5)*.36*scale,0])
            receptors.add(rec)
    return VGroup(cone,receptors)


def receptor_legend(y=-3.2):
    return VGroup(Rectangle(width=.24,height=.28,color=TEAL,fill_color=YELLOW,fill_opacity=1).move_to([-2.2,y,0]),
        label('bound',-1.35,y,YELLOW),
        Rectangle(width=.24,height=.28,color=TEAL,fill_color=BG,fill_opacity=1).move_to([.8,y,0]),
        label('empty',1.7,y,TEAL))


def deletion_frame(question=False):
    a=cord((-3.25,-.45,0),1.22,floor=False)
    b=cord((3.25,-.45,0),1.22,progenitor=False)
    # Dim reference paths describe what 'on course' means, without revealing results.
    g=VGroup(*[m[j] for m in [a,b] for j in [0,1,2,3,6]],
        label('floor plate source off',-3.25,2.65,RED),
        label('progenitor source off',3.25,2.65,RED))
    for m in [a,b]:
        g.add(m[4].copy().set_stroke(BLUE,width=5,opacity=.45).set_fill(opacity=0),
            m[5].copy().scale(1.6).set_color(BLUE).set_opacity(.65))
    if question:
        g.add(heading('If the floor plate gradient guides…'),
              label('Which deletion hurts more?',0,-3.55,size=30))
    return g


def wandering(center=(-3.25,-.4,0),scale=1.2):
    c=np.array(center)
    paths=VGroup()
    for pts in [ [(-1.55,1.4),(-1.7,.65),(-.8,.2),(-.9,.9)],
                 [(-1.3,1.45),(-1.7,.45),(-1.45,-.35)],
                 [(1.5,1.4),(1.8,.5),(.95,.15),(1.1,.85)],
                 [(1.25,1.4),(1.6,.3),(1.4,-.65)]]:
        path=smooth([c+np.array([x,y,0])*scale for x,y in pts]).set_stroke(BLUE,5)
        paths.add(VGroup(path,body(path.get_end(),.12*scale)))
    return paths


def hindbrain_panel():
    # Tissue panel deliberately has no spinal-cord outline or central canal.
    panel=RoundedRectangle(width=5.5,height=4.6,corner_radius=.25,color=GREY).move_to([3.25,-.45,0])
    fibres=wandering((3.25,-.4,0),1.04)
    return VGroup(panel,fibres,label('hindbrain',3.25,2.3,GREY),
                  label('same pattern',3.25,-3,BLUE))


def third_study_frame():
    m=cord((-3.25,-.4,0),1.2,progenitor=False)
    return VGroup(m[0],m[2],m[6],wandering(),hindbrain_panel(),
        heading('2017 · third study'),label('progenitor source off',-3.25,2.5,RED),
        label('many off course / stalled',-3.25,-3.3,BLUE))


class S00Title(TitleCard):
    TITLE = 'Where Is the Netrin?'
    LESSON = 'Netrin and DCC: One Cue, Two Answers'

    def construct(self):
        # The stock card has a 20 pt brand; this chapter uses 22 pt throughout.
        brand=T('BIOCHEMISTRYPEDIA',22,TEAL,weight=BOLD)
        lesson=T(self.LESSON.upper(),22,GREY)
        title=T(self.TITLE,54,font=TITLE_FONT)
        rule=Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)
        group=VGroup(brand,lesson,title,rule).arrange(DOWN,buff=.32)
        self.play(FadeIn(brand),FadeIn(lesson),run_time=.65)
        self.play(Write(title),GrowFromCenter(rule),run_time=1.15)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        m=map_base(self)
        self.at('Is netrin')
        self.play(FadeIn(gradient()),FadeIn(m[2]),run_time=.65)
        self.at('a gradient')
        a=label('gradient from the midline?',3.35,1.65,YELLOW,25)
        self.play(FadeIn(a),run_time=.3)
        self.at('or a path')
        self.play(FadeIn(m[1]),FadeIn(label('path along the pia?',3.35,-.5,YELLOW,25)),run_time=.65)
        self.finish()


class S02Map(SpokenScene):
    def construct(self):
        m=map_base(self); labs=map_labels()
        self.add(m[1],m[2],labs[0],labs[4],labs[5],labs[6])
        self.at('Return to the map')
        self.at('the floor plate')
        self.play(Indicate(m[0][3],color=YELLOW),FadeIn(labs[1]),GrowArrow(labs[7]),run_time=.45)
        self.at('the progenitors')
        self.play(FadeIn(m[3]),FadeIn(labs[2]),GrowArrow(labs[3]),run_time=.5)
        self.finish()


class S03Dish(SpokenScene):
    def construct(self):
        d=dish_stage(); self.add(d[0],d[1],d[3],label('netrin bead',-4.4,-1.1,YELLOW))
        self.at('Start in a dish')
        self.at('A growth cone')
        self.play(FadeIn(d[2]),run_time=.4)
        self.at('on its two sides')
        self.play(FadeIn(label('near',-.2,-2.4,TEAL)),FadeIn(label('far',4.2,-2.4,TEAL)),
            Create(Line([.25,-1.55,0],[.25,-2.05,0],color=TEAL)),
            Create(Line([3.75,-1.55,0],[3.75,-2.05,0],color=TEAL)),run_time=.4)
        self.finish()


class S04Bead(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[1,10,1],y_range=[0,1,.2],x_length=10.3,y_length=5.1,
            tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([.3,-.1,0])
        curve=ax.plot(lambda r:1/r,x_range=[1,10,.02],color=YELLOW)
        self.add(ax,curve,heading('C = k / r'),label('concentration',-3.7,2.8,YELLOW),
            label('distance from bead',0,-3,GREY),
            label('Ideal case: steady small source, no cue lost',0,-3.6,GREY))
        marks=VGroup()
        for r,x,t in [(4,-1.2,'near: 100 µm'),(4.4,3.1,'far: 110 µm')]:
            point=ax.c2p(r,1/r)
            marks.add(Dot(point,color=YELLOW),label(t,x,1.1,YELLOW),
                      Line([x,.8,0],point,color=GREY))
        self.at('Around a small source')
        self.at('like a bead')
        self.play(FadeIn(marks),run_time=.45)
        self.at('concentration falls')
        dot=Dot(ax.c2p(1,1),color=YELLOW,radius=.12); self.add(dot)
        self.play(MoveAlongPath(dot,curve),run_time=.95)
        self.finish()


class S05Rule(SpokenScene):
    def construct(self):
        d=dish_stage(); self.add(d)
        w=DoubleArrow([.25,2.1,0],[3.75,2.1,0],color=BLUE,buff=0)
        r=DoubleArrow([-4.6,-2.45,0],[.25,-2.45,0],color=GREY,buff=0)
        self.add(heading('fractional difference ≈ w / r'),w,r,
            label('w = 10 µm',2,2.65,BLUE),label('r = 100 µm',-2.2,-2.95,GREY),
            DashedLine([-4.6,-.4,0],[-4.6,-2.45,0],color=GREY),
            DashedLine([.25,-.2,0],[.25,-2.45,0],color=GREY))
        self.at('The fractional difference')
        self.at('its width'); self.play(Indicate(w,color=BLUE),run_time=.35)
        self.at('its distance'); self.play(Indicate(r,color=GREY),run_time=.35)
        self.finish()


class S06Numbers(SpokenScene):
    def construct(self):
        self.add(heading('Two sides of a 10 µm growth cone'))
        for x,title in [(-3.2,'100 µm from source'),(3.2,'1 mm from source')]:
            self.add(label(title,x,2.3,GREY),body([x,.8,0],.65),
                label('near',x-1,-2.6,TEAL),label('far',x+1,-2.6,TEAL))
        def bars(x,r):
            # C=k/r: common absolute scale; the distant cue is tenfold lower.
            hs=[2.8*100/r,2.8*100/(r+10)]
            return VGroup(*[Rectangle(width=.7,height=h,color=YELLOW,fill_color=YELLOW,fill_opacity=.85)
                .move_to([x+dx,-2.1+h/2,0]) for dx,h in zip([-1,1],hs)])
        self.at('Close in'); self.play(FadeIn(bars(-3.2,100)),run_time=.4)
        self.at('sees about'); self.play(FadeIn(label('≈10% difference',-3.2,-3.25,YELLOW,30)),run_time=.35)
        self.at('A millimeter away'); self.play(FadeIn(bars(3.2,1000)),run_time=.4)
        self.at('about 1%'); self.play(FadeIn(label('≈1% difference',3.2,-3.25,YELLOW,30)),run_time=.35)
        self.finish()


class S07Occupancy(SpokenScene):
    def construct(self):
        p=receptor_panel(.6,.5,scale=1.35)
        self.add(p,heading('Bound receptors'),receptor_legend(),
            label('near',-2.63,2.6,TEAL),label('far',2.63,2.6,TEAL))
        self.at('But a growth cone')
        self.at('measures bound receptors'); self.play(Indicate(p[1],color=YELLOW,scale_factor=1.02),run_time=.5)
        self.at('not netrin itself'); self.finish()


class S08Kd(SpokenScene):
    def construct(self):
        p=binding_plot(); self.add(p,heading('fraction bound = C / (C + Kd)'))
        self.at('The Kd')
        self.at('fills half')
        point=p[0].c2p(0,.5)
        guide=VGroup(DashedLine(p[0].c2p(-2.35,.5),point,color=YELLOW),
            Dot(point,color=YELLOW),label('Kd: half filled',3,-.5,YELLOW,28))
        self.play(FadeIn(guide),run_time=.45); self.finish()


class S09Predict(SpokenScene):
    def construct(self):
        g=prediction_frame(); self.add(g[0],g[2],g[3],g[4])
        self.at('Give it the same')
        for phrase,i in [('far below',0),('at it',1),('far above',2)]:
            self.at(phrase); self.play(FadeIn(g[1][i]),run_time=.25)
        self.at('Where is the bound'); self.play(Indicate(g[3],scale_factor=1.03),run_time=.4)
        self.finish()


class S10Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(prediction_frame(),label('Think about it',3.6,.15,GREY,28))
        self.wait(5)


class S11Reveal(SpokenScene):
    def construct(self):
        table=table_frame()
        self.add(table)
        self.at('At the KD')
        self.play(Indicate(table[-1],color=YELLOW),run_time=.6)
        self.at('far below it')
        self.play(Indicate(VGroup(*table[5:9]),color=YELLOW,scale_factor=1.04),run_time=.6)
        self.at('Far above it')
        self.play(Indicate(VGroup(*table[13:17]),color=YELLOW,scale_factor=1.04),run_time=.6)
        self.finish()


class S12Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(table_frame())
        self.wait(2.5)


class S13Noise(SpokenScene):
    def construct(self):
        rng=np.random.default_rng(5)
        panels=VGroup(receptor_panel(.1,0,-3.25,-.35,1.22),receptor_panel(1,.9,3.25,-.35,1.22))
        title=heading('Binding fluctuates')
        for panel in panels: panel[0].stretch_to_fit_height(4.6)
        self.add(panels,title,receptor_legend(-3.55))
        counts=VGroup()
        for x,t,a,b in [(-3.25,'far below Kd',1,0),(3.25,'far above Kd',10,9)]:
            self.add(label(t,x,2.75,GREY),label('near',x-2.38,2.25,TEAL),label('far',x+2.38,2.25,TEAL))
            counts.add(label(f'{a} vs {b}',x,-2.9,YELLOW))
        self.add(counts)
        self.at('Binding is noisy')
        self.at('molecules arrive')
        # Finite illustrative samples. Random receptor identities; final samples explicitly
        # show ties and reversed order, making loss of a one-receptor difference visible.
        def flicker(a,b,c,d):
            changes=[]
            for panel,ns in zip(panels,[(a,b),(c,d)]):
                for side,n in enumerate(ns):
                    chosen=set(rng.choice(10,n,replace=False))
                    for i in range(10):
                        changes.append(panel[1][side*10+i].animate.set_fill(YELLOW if i in chosen else BG,1))
            self.play(*changes,Transform(counts[0],label(f'{a} vs {b}',-3.25,-2.9,YELLOW)),
                Transform(counts[1],label(f'{c} vs {d}',3.25,-2.9,YELLOW)),run_time=.24)
        for ns in [(0,1,9,10),(1,1,9,9),(1,0,10,9),(0,1,9,10)]: flicker(*ns)
        self.at('A tiny difference')
        self.play(Transform(title,heading('A tiny difference can be lost')),run_time=.2)
        for ns in [(1,1,9,9),(0,1,9,10),(0,0,10,10)]: flicker(*ns)
        self.finish()


class S14Adapt(SpokenScene):
    def construct(self):
        left=Axes(x_range=[-2,2,1],y_range=[0,1,.5],x_length=5.15,y_length=5.1,
            tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([-3.3,-.2,0])
        left.y_axis.set_opacity(0); left.add(Line(left.c2p(-2,0),left.c2p(-2,1),color=GREY))
        curve=left.plot(lambda u:10**u/(1+10**u),x_range=[-2,2,.02],color=TEAL)
        band=Polygon(*[left.c2p(x,y) for x,y in [(-.4,0),(.4,0),(.4,1),(-.4,1)]],
            stroke_width=0,fill_color=YELLOW,fill_opacity=.16)
        kd=DashedLine(left.c2p(0,0),left.c2p(0,1),color=YELLOW)
        ax=Axes(x_range=[0,8,1],y_range=[0,1.3,.5],x_length=5.2,y_length=4.5,
            tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([3.35,.1,0])
        title=heading('Most signal near Kd'); kdtag=label('Kd',-3.3,-3.15,YELLOW)
        self.add(left,curve,band,kd,ax,label('bound',-5.3,2.8,TEAL),label('response',2.3,2.1,BLUE),
            kdtag,label('C / Kd (log)',-3.3,-3.6,GREY),
            label('time →',3.4,-3.55,GREY),title)
        self.at('A fixed detector')
        self.at('the most signal'); self.play(Indicate(band,color=YELLOW),run_time=.35)
        self.at('Adapting'); self.play(Transform(title,heading('Adaptation resets the baseline')),
            Transform(kdtag,label('Kd stays fixed',-3.3,-3.15,YELLOW)),run_time=.3)
        def response(t): return .15+sum(np.exp(-(t-ti)/.65) if t>=ti else 0 for ti in [1,4.5])
        baseline=DashedLine(ax.c2p(0,.15),ax.c2p(8,.15),color=GREY)
        self.at('resetting its baseline'); self.add(baseline)
        # Shared time tracker drives BOTH computed traces, so a response never
        # precedes the background step that causes it.
        clock=ValueTracker(0)
        def response_trace():
            ts=sorted(set(list(np.arange(0,max(.02,clock.get_value()),.025))+[clock.get_value()]+
                [t for ti in [1,4.5] for t in [ti-.001,ti] if t<=clock.get_value()]))
            return VMobject(color=BLUE,stroke_width=4).set_points_as_corners([ax.c2p(t,response(t)) for t in ts])
        def bg_trace():
            end=max(.001,clock.get_value()); pts=[ax.c2p(0,-.13)]
            level=-.13
            for ti in [1,4.5]:
                if ti<=end: pts.extend([ax.c2p(ti,level),ax.c2p(ti,level+.07)]); level+=.07
            pts.append(ax.c2p(end,level))
            return VMobject(color=YELLOW,stroke_width=3).set_points_as_corners(pts)
        trace=always_redraw(response_trace); bg=always_redraw(bg_trace)
        self.add(trace,bg,label('background steps',3.4,-2.9,YELLOW))
        self.at('respond again'); self.play(clock.animate.set_value(8),run_time=2.4,rate_func=linear)
        self.at('It cannot remove',lead=.35)
        limit=label('binding limit stays',3.35,2.75,YELLOW,28)
        self.play(FadeIn(limit),Indicate(kd,color=YELLOW),Indicate(band,color=YELLOW),run_time=.3)
        self.finish()


class S15Embryo(SpokenScene):
    def construct(self):
        m=map_base(self)
        self.at('Now the embryo')
        self.play(FadeIn(heading('Back to the embryo')),run_time=.4)
        self.at('made in two places')
        self.play(FadeIn(m[2]),FadeIn(m[3]),run_time=.6)
        self.finish()


class S16Sources(SpokenScene):
    def construct(self):
        m=map_base(self); self.add(m[2],m[3])
        self.at('Floor plate cells')
        self.play(Indicate(m[2],color=YELLOW),FadeIn(label('floor plate',3.6,-2.6,YELLOW)),
            GrowArrow(Arrow([2,-2.65,0],[-2.1,-3,0],color=GREY,buff=.1)),run_time=.45)
        self.at('So do progenitors')
        self.play(Indicate(m[3],color=YELLOW),FadeIn(label('ventricular zone\n(ventral and\nintermediate)',3.65,.7,YELLOW,28)),
            GrowArrow(Arrow([1.6,.6,0],[-1.3,.2,0],color=GREY,buff=.1)),run_time=.5)
        self.at('a broad stretch'); self.play(Indicate(m[3],color=YELLOW,scale_factor=1.04),run_time=.45)
        self.finish()


class S17Path(SpokenScene):
    def construct(self):
        m=map_base(self); self.add(m[2],m[3])
        fibres=VGroup()
        # Both sides terminate exactly on the same analytic pial ellipse.
        for side in [-1,1]:
            for t in np.linspace(2.65,4.45,7):
                x=2.16*np.cos(t); y=2.1*np.sin(t)
                fibres.add(Line([-2.5+side*.6*1.34,-.25+(.8-(t-2.65)*.8)*1.34,0],
                    [-2.5+side*abs(x)*1.34,-.25+y*1.34,0],color=GREY,stroke_width=1.5))
        self.at('The progenitors'); self.play(Create(fibres),run_time=.55)
        packets=VGroup(*[Dot(f.get_start(),color=YELLOW,radius=.08) for f in fibres])
        self.at('send netrin out'); self.add(packets)
        self.play(*[MoveAlongPath(d,f) for d,f in zip(packets,fibres)],run_time=.9)
        self.at('It builds up')
        self.play(LaggedStart(*[FadeIn(d) for d in m[1]],lag_ratio=.08),FadeOut(packets),run_time=1)
        self.at('surface'); self.play(FadeIn(label('pial surface',3.7,-.7,GREY,28)),
            GrowArrow(Arrow([2,-.85,0],[.1,-1.8,0],color=GREY,buff=.1)),run_time=.35)
        self.at('along the commissural'); self.play(Indicate(m[4],color=BLUE,scale_factor=1.02),run_time=.5)
        self.finish()


class S18Two(SpokenScene):
    def construct(self):
        m=map_base(self); self.add(m[2],heading('Two candidate ways to guide'))
        self.at('two candidate ways')
        self.at('One is a gradient')
        field=gradient(); self.play(FadeIn(field),FadeIn(label('chemotropism',3.6,.9,YELLOW,32)),
            FadeIn(label('a model to test\nin the embryo',3.6,-.45,GREY,28)),run_time=.65)
        self.at('That is chemotropism'); self.play(Indicate(field,scale_factor=1),run_time=.5)
        self.finish()


class S19Hapto(SpokenScene):
    def construct(self):
        m=map_base(self,route=False); self.add(m[1],m[2],heading('Two candidate ways to guide'),
            label('haptotaxis',3.6,.9,YELLOW,32),label('a model to test\nin the embryo',3.6,-.45,GREY,28))
        t0,t1=2.65,4.15
        def pos(t): return [-2.5+2.16*np.cos(t)*1.34,-.25+2.1*np.sin(t)*1.34,0]
        tip=body(pos(t0),.22); self.add(tip)
        path=ParametricFunction(lambda t:np.array(pos(t)),t_range=[t0,t1])
        self.at('Guidance by netrin'); self.play(MoveAlongPath(tip,path),run_time=1.7)
        self.at('is called haptotaxis'); self.finish()


class S202017(SpokenScene):
    def construct(self):
        g=deletion_frame(); self.add(*g[:10],*g[12:],heading('2017 · source deletions in mice'))
        self.at('In 2017')
        self.at('two groups deleted'); self.play(FadeIn(g[10]),run_time=.35)
        self.at('one source at a time'); self.play(FadeIn(g[11]),
            Indicate(g[3],color=YELLOW,scale_factor=1.02),run_time=.45)
        self.at('A conditional deletion',lead=0)
        self.play(FadeIn(label('conditional deletion: only in chosen cells',0,-3.55,GREY,28)),run_time=.35)
        self.finish()


class S21Predict2(SpokenScene):
    def construct(self):
        g=deletion_frame(True)
        self.add(*g[:-2])
        self.at('If a floor plate gradient')
        self.play(FadeIn(g[-2]),Indicate(VGroup(g[12],g[13]),color=BLUE,scale_factor=1.02),run_time=.4)
        self.at('which deletion')
        self.play(FadeIn(g[-1]),run_time=.45)
        self.finish()


class S22Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(deletion_frame(True))
        self.wait(5)


class S23Reveal2(SpokenScene):
    def construct(self):
        g=deletion_frame(); self.add(g,heading('2017 · source deletions in mice'))
        expected=label('Predicted: more errors',-3.25,-3.5,GREY,28)
        self.at('The floor plate deletion'); self.add(expected)
        self.at('It did not')
        m=cord((-3.25,-.45,0),1.22,floor=False)
        self.remove(expected,g[13])
        self.play(Create(m[4]),FadeIn(m[5]),FadeIn(label('most axons on course',-3.25,-3.5,BLUE,28)),run_time=.55)
        self.at('most commissural axons'); self.play(Indicate(m[4],scale_factor=1.01),run_time=.4)
        self.at('stayed on course'); self.finish()


class S24Reveal3(SpokenScene):
    def construct(self):
        g=third_study_frame(); title=heading('2017 · progenitor deletion')
        self.add(g[0],g[1],g[2],g[3],g[6],g[7],title)
        self.at('Without progenitor netrin')
        self.at('many commissural axons'); self.play(Indicate(g[3],scale_factor=1.02),run_time=.4)
        self.at('went off course')
        self.at('A third study'); self.play(FadeIn(g[4]),Transform(title,g[5]),run_time=.55)
        self.at('in the hindbrain'); self.finish()


class S25Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(third_study_frame()); self.wait(2.5)


class S26Cannot(SpokenScene):
    def construct(self):
        self.add(heading('A deletion shows which source, not how it is read'))
        diagrams=VGroup()
        for x,kind in [(-3.25,'surface path'),(3.25,'short gradient near the pia')]:
            panel=RoundedRectangle(width=5.7,height=4.7,corner_radius=.2,color=GREY).move_to([x,-.2,0])
            surface=Line([x-2.3,-1.6,0],[x+2.3,-1.6,0],color=GREY,stroke_width=7)
            dots=VGroup(*[Dot([xx,-1.42,0],color=YELLOW,radius=.09) for xx in np.linspace(x-2.2,x+2.2,20)])
            diagrams.add(VGroup(panel,surface,dots,label(kind,x,2.55,YELLOW,26),label('pia',x,-2.9,GREY)))
        field=VGroup()
        for i in range(18):
            field.add(Rectangle(width=4.6,height=.16,stroke_width=0,fill_color=YELLOW,
                fill_opacity=.5*np.exp(-i*.22)).move_to([3.25,-1.25+i*.17,0]))
        diagrams[1].add(field)
        surface_axon=smooth([[-5.3,-1.12,0],[-4.4,-1.04,0],[-3.5,-1.12,0],[-2.35,-1.08,0]]).set_stroke(BLUE,6)
        surface_tip=body([-2.35,-1.08,0],.32)
        gradient_axon=smooth([[1.3,1.65,0],[1.8,1.35,0],[2.25,.75,0],[2.85,.1,0]]).set_stroke(BLUE,6)
        gradient_tip=body([2.85,.1,0],.38)
        diagrams[0].add(surface_axon,surface_tip)
        diagrams[1].add(gradient_axon,gradient_tip)
        self.add(diagrams)
        self.at('A deletion shows')
        self.at('A path'); self.play(Indicate(surface_tip,color=BLUE,scale_factor=1.08),run_time=.25)
        self.at('and a short'); self.play(Indicate(gradient_tip,color=BLUE,scale_factor=1.08),run_time=.25)
        self.at('both fit',lead=.3); self.play(FadeIn(label('✓ fits',-3.25,1.15,GREEN,36)),
            FadeIn(label('✓ fits',4.6,1.4,GREEN,36)),run_time=.2)
        self.finish()


class S27Floorplate(SpokenScene):
    def construct(self):
        m=map_base(self,floor=False); self.add(m[1],m[3])
        self.at('Nor is the floor plate idle')
        floor=cord()[2].set_opacity(.4)
        self.play(FadeIn(floor),FadeIn(label('contributes, with\nprogenitor netrin',3.6,.4,YELLOW,30)),run_time=.55)
        self.at('In the spinal cord')
        self.play(FadeIn(label('2019 · spinal cord',3.6,1.8,GREY,28)),run_time=.35)
        self.at('still contributes'); self.play(Indicate(floor,color=YELLOW,scale_factor=1.1),run_time=.4)
        self.finish()


class S28Scope(SpokenScene):
    def construct(self):
        box=RoundedRectangle(width=12.1,height=4.3,corner_radius=.2,color=GREY).move_to([0,.9,0])
        line=label('Much of the netrin that matters\nseems to act near where\nprogenitors lay it down',0,1.05,YELLOW,38)
        self.add(box,label('3 · Where the cue acts',0,2.55,size=32),line)
        self.at('much of the netrin')
        self.at('near where progenitors'); self.play(Indicate(line,scale_factor=1.02),run_time=.4)
        self.at('That holds'); self.play(FadeIn(label('mouse spinal cord + hindbrain',0,-.65,GREY,30)),run_time=.4)
        self.at('In the spinal cord',lead=.25); self.play(
            box.animate.stretch_to_fit_height(6.0).move_to([0,.05,0]),
            FadeIn(label('The floor plate keeps a part',0,-1.8,YELLOW,36)),
            FadeIn(label('mouse spinal cord',0,-2.65,GREY,30)),run_time=.45)
        self.finish()


class S29Next(SpokenScene):
    def construct(self):
        m=map_base(self,route=False,center=(0,-.2,0),scale=1.36)
        self.add(m[1],m[2],m[3],heading('Next: crossing the midline'))
        pts=[[-2.1,1.7,0],[-2.65,.5,0],[-2.3,-1.3,0],[-1.15,-2.55,0],
             [0,-2.95,0],[1.1,-2.8,0],[2.1,-1.5,0],[2.25,-.5,0]]
        path=smooth(pts).set_stroke(BLUE,6); tip=body(pts[0],.22); self.add(tip)
        self.at('After crossing')
        self.play(Create(path),MoveAlongPath(tip,path),run_time=1.3,rate_func=linear)
        self.at('do not turn back'); self.play(Indicate(tip,color=BLUE),run_time=.4)
        self.at('the next lesson'); self.finish()


class S30Takeaway(SpokenScene):
    def construct(self):
        m=map_base(self,center=(-3.6,-.2,0),scale=1.15); self.add(m[1],m[2],m[3])
        self.add(*[RoundedRectangle(width=6.1,height=.75,corner_radius=.12,color=GREY)
            .move_to([3.25,y,0]) for y in [2.3,1.4]])
        self.add(label('1 · Netrin is the cue',3.25,2.3,size=28),
            label('2 · The reader sets the response',3.25,1.4,size=26))
        box=RoundedRectangle(width=6,height=3.7,corner_radius=.16,color=YELLOW).move_to([3.25,-1.1,0])
        text=label('Netrin marks a place;\nthe growth cone decides\nwhat to do there.',3.25,-1.1,YELLOW,31)
        self.at('netrin marks a place'); self.play(FadeIn(box),FadeIn(text),Indicate(m[1],color=YELLOW),run_time=.45)
        self.at('the growth cone decides'); self.play(Indicate(m[5],color=BLUE),run_time=.45)
        self.finish()


class S31End(EndCard):
    LINE = 'Netrin marks a place; the growth cone decides.'

    def construct(self):
        self.add(label('Netrin marks a place;\nthe growth cone decides.',0,.65,YELLOW,49),
            label('Next: crossing the midline',0,-1.3,size=34),
            label('biochemistrypedia.com',0,-2.65,TEAL,26))
        self.finish()
